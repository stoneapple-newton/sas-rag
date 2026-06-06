from __future__ import annotations

import argparse
import json
from pathlib import Path

from sas_rag.ingestion.pipeline import run_ingestion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest local official SAS PDF documents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest-pdfs", help="Parse, normalize, chunk, and report SAS PDFs.")
    ingest.add_argument("--source-dir", default="docs/sas-documents", help="Repo-relative source PDF directory.")
    ingest.add_argument("--whitelist", default="data/source_whitelist.json", help="Source whitelist JSON path.")
    ingest.add_argument("--out", default="data/ingestion/runs/latest", help="Output directory for artifacts.")
    ingest.add_argument("--max-chars", type=int, default=4000, help="Maximum characters per emitted chunk.")
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


if __name__ == "__main__":
    main()
