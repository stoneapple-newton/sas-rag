from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from sas_rag.ingestion.chroma_index import create_openai_embeddings, index_chunks_to_chroma, query_chroma, write_report
from sas_rag.ingestion.pipeline import run_ingestion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest local official SAS PDF documents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest-pdfs", help="Parse, normalize, chunk, and report SAS PDFs.")
    ingest.add_argument("--source-dir", default="docs/sas-documents", help="Repo-relative source PDF directory.")
    ingest.add_argument("--whitelist", default="data/source_whitelist.json", help="Source whitelist JSON path.")
    ingest.add_argument("--out", default="data/ingestion/runs/latest", help="Output directory for artifacts.")
    ingest.add_argument("--max-chars", type=int, default=4000, help="Maximum characters per emitted chunk.")

    index = subparsers.add_parser("index-chroma", help="Embed chunk JSONL records and persist them to Chroma.")
    index.add_argument("--chunks", default="data/ingestion/runs/latest/chunks.jsonl", help="Chunk JSONL path.")
    index.add_argument("--priority", default="P0", help="Optional priority filter. Use an empty value for all chunks.")
    index.add_argument("--persist-directory", default=None, help="Chroma persist directory.")
    index.add_argument("--collection-name", default=None, help="Chroma collection name.")
    index.add_argument("--report", default="data/ingestion/runs/latest/chroma_report.json", help="Index report path.")
    index.add_argument("--batch-size", type=int, default=256, help="Documents per Chroma add batch.")
    index.add_argument("--reset", action="store_true", help="Delete the persist directory before indexing.")

    query = subparsers.add_parser("query-chroma", help="Run a similarity query against persisted Chroma.")
    query.add_argument("query", help="Search query.")
    query.add_argument("--persist-directory", default=None, help="Chroma persist directory.")
    query.add_argument("--collection-name", default=None, help="Chroma collection name.")
    query.add_argument("--k", type=int, default=5, help="Number of results.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    repo_root = Path.cwd()
    if args.command == "ingest-pdfs":
        report = run_ingestion(
            repo_root=repo_root,
            whitelist_path=repo_root / args.whitelist,
            output_dir=repo_root / args.out,
            source_dir=Path(args.source_dir),
            max_chars=args.max_chars,
        )
        print(json.dumps(report.to_dict()["summary"], indent=2))
    elif args.command == "index-chroma":
        load_dotenv()
        embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        priority = args.priority or None
        persist_directory = Path(args.persist_directory or os.getenv("SAS_RAG_CHROMA_PATH", "data/chroma"))
        collection_name = args.collection_name or os.getenv("SAS_RAG_CHROMA_COLLECTION", "sas_94_docs")
        report = index_chunks_to_chroma(
            chunks_path=repo_root / args.chunks,
            persist_directory=repo_root / persist_directory,
            collection_name=collection_name,
            embeddings=create_openai_embeddings(embedding_model),
            embedding_model=embedding_model,
            priority=priority,
            reset=args.reset,
            batch_size=args.batch_size,
        )
        write_report(report, repo_root / args.report)
        print(json.dumps(report.to_dict(), indent=2))
    elif args.command == "query-chroma":
        load_dotenv()
        embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        persist_directory = Path(args.persist_directory or os.getenv("SAS_RAG_CHROMA_PATH", "data/chroma"))
        collection_name = args.collection_name or os.getenv("SAS_RAG_CHROMA_COLLECTION", "sas_94_docs")
        results = query_chroma(
            persist_directory=repo_root / persist_directory,
            collection_name=collection_name,
            embeddings=create_openai_embeddings(embedding_model),
            query=args.query,
            k=args.k,
        )
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
