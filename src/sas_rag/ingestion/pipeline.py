from __future__ import annotations

import json
import logging
from pathlib import Path

from sas_rag.ingestion.checksum import ChecksumRegistry
from sas_rag.ingestion.chunker import chunk_unit, file_hash
from sas_rag.ingestion.models.records import ChunkRecord, IngestionReport, SourceReport
from sas_rag.ingestion.normalizer import normalize_unit
from sas_rag.ingestion.pdf_adapter import PdfAdapter
from sas_rag.ingestion.whitelist import load_whitelist

logger = logging.getLogger(__name__)


def validate_chunks(chunks: list[ChunkRecord], source_id: str) -> tuple[list[ChunkRecord], list[dict]]:
    """Validate all chunks and return (valid_chunks, rejections)."""
    valid: list[ChunkRecord] = []
    rejections: list[dict] = []

    for chunk in chunks:
        try:
            chunk.validate_provenance()
            valid.append(chunk)
        except ValueError as exc:
            rejection = {
                "chunk_id": chunk.chunk_id,
                "source_id": source_id,
                "reason": str(exc),
                "metadata_keys": list(chunk.metadata.keys()) if chunk.metadata else [],
            }
            rejections.append(rejection)
            logger.warning(f"Chunk validation failed: {rejection}")

    return valid, rejections


def run_ingestion(
    repo_root: Path,
    whitelist_path: Path,
    output_dir: Path,
    source_dir: Path | None = None,
    max_chars: int = 4000,
    skip_unchanged: bool = True,
) -> IngestionReport:
    logger.info("Starting ingestion", extra={
        "whitelist": str(whitelist_path),
        "output_dir": str(output_dir),
        "source_dir": str(source_dir) if source_dir else None,
        "max_chars": max_chars,
        "skip_unchanged": skip_unchanged,
    })

    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir = output_dir / "normalized"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    chunks_path = output_dir / "chunks.jsonl"

    # Load checksum registry for re-ingestion detection
    registry = ChecksumRegistry(output_dir / "checksum_registry.json")
    logger.debug(f"Checksum registry: {registry.summary()}")

    records = load_whitelist(whitelist_path)
    logger.debug(f"Loaded {len(records)} records from whitelist")

    if source_dir is not None:
        records = [
            record
            for record in records
            if Path(record.local_path).parent.as_posix() == source_dir.as_posix().replace("\\", "/")
        ]
        logger.debug(f"Filtered to {len(records)} records for source_dir: {source_dir}")

    adapter = PdfAdapter()
    report = IngestionReport()
    all_chunks: list[ChunkRecord] = []
    all_rejections: list[dict] = []

    for source in records:
        logger.debug(f"Processing source: {source.source_id}")

        if source.ingestion_status not in {"ready", "loaded"}:
            logger.info(f"Skipping source {source.source_id}: status={source.ingestion_status}")
            report.add(SourceReport(source_id=source.source_id, title=source.title, status="skipped"))
            continue

        try:
            source_path = source.path(repo_root)
            source_hash = file_hash(source_path)

            # Check if source has changed
            classification = registry.classify_source(source.source_id, source_hash)
            logger.debug(f"Source {source.source_id}: {classification} (hash={source_hash[:16]}...)")

            if classification == "unchanged" and skip_unchanged:
                logger.info(f"Skipping unchanged source: {source.source_id}")
                report.add(SourceReport(
                    source_id=source.source_id,
                    title=source.title,
                    status="unchanged",
                    content_hash=source_hash,
                ))
                continue

            units = adapter.load(source, repo_root)
            logger.debug(f"Source {source.source_id}: loaded {len(units)} pages")

            source_chunks: list[ChunkRecord] = []
            source_markdown: list[str] = []
            for unit in units:
                normalized = normalize_unit(unit)
                source_markdown.append(normalized.markdown)
                source_chunks.extend(chunk_unit(normalized, source_hash, max_chars=max_chars))

            logger.debug(f"Source {source.source_id}: emitted {len(source_chunks)} raw chunks")

            # Validate chunks before accepting them
            valid_chunks, rejections = validate_chunks(source_chunks, source.source_id)
            all_chunks.extend(valid_chunks)
            all_rejections.extend(rejections)

            logger.debug(f"Source {source.source_id}: {len(valid_chunks)} valid, {len(rejections)} rejected")

            normalized_path = normalized_dir / f"{source.source_id}.md"
            normalized_path.write_text("\n\n".join(source_markdown), encoding="utf-8")
            report.add(
                SourceReport(
                    source_id=source.source_id,
                    title=source.title,
                    status="loaded",
                    pages_loaded=len(units),
                    chunks_emitted=len(valid_chunks),
                    chunks_rejected=len(rejections),
                    content_hash=source_hash,
                )
            )
            logger.info(f"Source {source.source_id} processed successfully", extra={
                "pages": len(units),
                "chunks": len(valid_chunks),
                "rejected": len(rejections),
                "classification": classification,
            })

            # Update registry with current checksum
            registry.set(source.source_id, source_hash)

        except Exception as exc:  # Keep batch reporting complete across parser failures.
            logger.error(f"Source {source.source_id} failed: {exc}", extra={
                "source_id": source.source_id,
                "error": str(exc),
            })
            report.add(
                SourceReport(
                    source_id=source.source_id,
                    title=source.title,
                    status="failed",
                    error=f"{type(exc).__name__}: {exc}",
                )
            )

    # Save updated registry
    registry.save()

    logger.info("Writing chunks to disk", extra={
        "total_chunks": len(all_chunks),
        "total_rejected": len(all_rejections),
    })
    with chunks_path.open("w", encoding="utf-8") as handle:
        for chunk in all_chunks:
            handle.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")

    # Write rejection report if any chunks were rejected
    if all_rejections:
        rejections_path = output_dir / "rejections.json"
        rejections_path.write_text(json.dumps({
            "total_rejected": len(all_rejections),
            "rejections": all_rejections,
        }, indent=2), encoding="utf-8")
        logger.warning(f"Wrote {len(all_rejections)} chunk rejections to {rejections_path}")

    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    logger.info("Ingestion complete", extra={"report": report.summary()})
    return report
