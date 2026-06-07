from __future__ import annotations

import json
from pathlib import Path

from sas_rag.ingestion.chunker import chunk_unit, file_hash
from sas_rag.ingestion.models import ChunkRecord, IngestionReport, SourceReport
from sas_rag.ingestion.normalizer import normalize_unit
from sas_rag.ingestion.pdf_adapter import PdfAdapter
from sas_rag.ingestion.whitelist import load_whitelist


def run_ingestion(
    repo_root: Path,
    whitelist_path: Path,
    output_dir: Path,
    source_dir: Path | None = None,
    max_chars: int = 4000,
) -> IngestionReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir = output_dir / "normalized"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    chunks_path = output_dir / "chunks.jsonl"

    records = load_whitelist(whitelist_path)
    if source_dir is not None:
        records = [
            record
            for record in records
            if Path(record.local_path).parent.as_posix() == source_dir.as_posix().replace("\\", "/")
        ]

    adapter = PdfAdapter()
    report = IngestionReport()
    all_chunks: list[ChunkRecord] = []

    for source in records:
        if source.ingestion_status not in {"ready", "loaded"}:
            report.add(SourceReport(source_id=source.source_id, title=source.title, status="skipped"))
            continue

        try:
            source_path = source.path(repo_root)
            source_hash = file_hash(source_path)
            units = adapter.load(source, repo_root)
            source_chunks: list[ChunkRecord] = []
            source_markdown: list[str] = []
            for unit in units:
                normalized = normalize_unit(unit)
                source_markdown.append(normalized.markdown)
                source_chunks.extend(chunk_unit(normalized, source_hash, max_chars=max_chars))

            normalized_path = normalized_dir / f"{source.source_id}.md"
            normalized_path.write_text("\n\n".join(source_markdown), encoding="utf-8")
            all_chunks.extend(source_chunks)
            report.add(
                SourceReport(
                    source_id=source.source_id,
                    title=source.title,
                    status="loaded",
                    pages_loaded=len(units),
                    chunks_emitted=len(source_chunks),
                    content_hash=source_hash,
                )
            )
        except Exception as exc:  # Keep batch reporting complete across parser failures.
            report.add(
                SourceReport(
                    source_id=source.source_id,
                    title=source.title,
                    status="failed",
                    error=f"{type(exc).__name__}: {exc}",
                )
            )

    with chunks_path.open("w", encoding="utf-8") as handle:
        for chunk in all_chunks:
            handle.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")

    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return report
