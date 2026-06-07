from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from sas_rag.config import settings
from sas_rag.ingestion.chroma_index import create_openai_embeddings, index_chunks_to_chroma, query_chroma, write_report
from sas_rag.ingestion.pipeline import run_ingestion
from sas_rag.logging_config import configure_logging
from sas_rag.retrieval.explain import explain_sas_file
from sas_rag.retrieval.search import format_citation, search_with_filters

logger = logging.getLogger(__name__)


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

    search = subparsers.add_parser("search", help="Search with optional metadata filters.")
    search.add_argument("query", help="Search query.")
    search.add_argument("--source-family", default=None, help="Filter by source family.")
    search.add_argument("--chunk-type", default=None, help="Filter by chunk type (concept, syntax, example, etc.).")
    search.add_argument("--priority", default=None, help="Filter by priority.")
    search.add_argument("--persist-directory", default=None, help="Chroma persist directory.")
    search.add_argument("--collection-name", default=None, help="Chroma collection name.")
    search.add_argument("--k", type=int, default=5, help="Number of results.")
    search.add_argument("--citations", action="store_true", help="Return citation-ready output.")

    explain = subparsers.add_parser("explain-sas-code", help="Explain a SAS code file using retrieved docs.")
    explain.add_argument("file", help="Path to .sas file.")
    explain.add_argument("--persist-directory", default=None, help="Chroma persist directory.")
    explain.add_argument("--collection-name", default=None, help="Chroma collection name.")
    explain.add_argument("--k", type=int, default=3, help="Number of evidence chunks per topic.")
    explain.add_argument("--citations", action="store_true", help="Return citation-ready evidence.")
    explain.add_argument("--out", default=None, help="Optional JSON output path.")
    return parser


def main() -> None:
    configure_logging()
    args = build_parser().parse_args()
    repo_root = Path.cwd()

    logger.info("CLI command started", extra={
        "command": args.command,
        "cli_args": vars(args),
    })

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
        embedding_model = settings.openai_embedding_model
        priority = args.priority or None
        persist_directory = Path(args.persist_directory or settings.sas_rag_chroma_path)
        collection_name = args.collection_name or settings.sas_rag_chroma_collection
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
        embedding_model = settings.openai_embedding_model
        persist_directory = Path(args.persist_directory or settings.sas_rag_chroma_path)
        collection_name = args.collection_name or settings.sas_rag_chroma_collection
        results = query_chroma(
            persist_directory=repo_root / persist_directory,
            collection_name=collection_name,
            embeddings=create_openai_embeddings(embedding_model),
            query=args.query,
            k=args.k,
        )
        print(json.dumps(results, indent=2))
    elif args.command == "search":
        embedding_model = settings.openai_embedding_model
        persist_directory = Path(args.persist_directory or settings.sas_rag_chroma_path)
        collection_name = args.collection_name or settings.sas_rag_chroma_collection
        filters: dict[str, str] = {}
        if args.source_family:
            filters["source_family"] = args.source_family
        if args.chunk_type:
            filters["chunk_type"] = args.chunk_type
        if args.priority:
            filters["priority"] = args.priority
        results = search_with_filters(
            persist_directory=repo_root / persist_directory,
            collection_name=collection_name,
            embeddings=create_openai_embeddings(embedding_model),
            query=args.query,
            k=args.k,
            filters=filters if filters else None,
        )
        if args.citations:
            results = [format_citation(r) for r in results]
        print(json.dumps(results, indent=2))
    elif args.command == "explain-sas-code":
        embedding_model = settings.openai_embedding_model
        persist_directory = Path(args.persist_directory or settings.sas_rag_chroma_path)
        collection_name = args.collection_name or settings.sas_rag_chroma_collection
        embeddings = create_openai_embeddings(embedding_model)

        def _search_fn(query: str, k: int, filters: dict[str, str] | None) -> list[dict]:
            return search_with_filters(
                persist_directory=repo_root / persist_directory,
                collection_name=collection_name,
                embeddings=embeddings,
                query=query,
                k=k,
                filters=filters,
            )

        report = explain_sas_file(Path(args.file), search_fn=_search_fn)
        if args.citations:
            for exp in report.get("explanations", []):
                if "evidence" in exp:
                    exp["evidence"] = [format_citation(r) for r in exp["evidence"]]
        if args.out:
            out_path = repo_root / args.out
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
            print(f"Report written to {out_path}")
        else:
            print(json.dumps(report, indent=2, default=str))

    logger.info("CLI command completed", extra={"command": args.command})


if __name__ == "__main__":
    main()
