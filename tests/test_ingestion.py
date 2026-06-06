from __future__ import annotations

import json
from pathlib import Path

from sas_rag.ingestion.chunker import chunk_unit, stable_chunk_id
from sas_rag.ingestion.models import NormalizedUnit, SourceRecord
from sas_rag.ingestion.whitelist import load_whitelist


def _source() -> SourceRecord:
    return SourceRecord(
        source_id="sqlproc",
        title="SAS SQL Procedure User's Guide",
        source_uri="docs/sas-documents/sqlproc.pdf",
        local_path="docs/sas-documents/sqlproc.pdf",
        source_family="proc-sql",
        sas_version="9.4",
        priority="P0",
        source_type="pdf",
        ingestion_status="ready",
    )


def test_load_whitelist_validates_required_fields(tmp_path: Path) -> None:
    whitelist = tmp_path / "source_whitelist.json"
    whitelist.write_text(json.dumps([_source().__dict__]), encoding="utf-8")

    records = load_whitelist(whitelist)

    assert records[0].source_id == "sqlproc"
    assert records[0].source_type == "pdf"


def test_stable_chunk_id_is_deterministic() -> None:
    first = stable_chunk_id("sqlproc", "SQL > Page 1", 1, "PROC SQL syntax")
    second = stable_chunk_id("sqlproc", "SQL > Page 1", 1, "PROC SQL syntax")

    assert first == second


def test_chunk_unit_emits_required_provenance() -> None:
    unit = NormalizedUnit(
        source=_source(),
        page=1,
        markdown="# SAS SQL Procedure User's Guide\n\n## Page 1\n\nPROC SQL syntax",
        section_path="SAS SQL Procedure User's Guide > Page 1",
    )

    chunks = chunk_unit(unit, source_content_hash="abc123", max_chars=4000)

    assert len(chunks) == 1
    chunks[0].validate_provenance()
    assert chunks[0].metadata["source_uri"] == "docs/sas-documents/sqlproc.pdf"
    assert chunks[0].metadata["version"] == "9.4"
