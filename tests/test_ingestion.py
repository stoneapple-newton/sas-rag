from __future__ import annotations

import json
from pathlib import Path

import pytest

from sas_rag.ingestion.chunker import chunk_unit, stable_chunk_id
from sas_rag.ingestion.models.records import NormalizedUnit, SourceRecord
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

    # Heading-aware chunking splits on "# Title" and "## Page 1" headings
    assert len(chunks) == 2
    for chunk in chunks:
        chunk.validate_provenance()
        assert chunk.metadata["source_uri"] == "docs/sas-documents/sqlproc.pdf"
        assert chunk.metadata["version"] == "9.4"

    # Second chunk should contain the PROC SQL content and have SAS block metadata
    content_chunk = chunks[1]
    assert "PROC SQL" in content_chunk.text
    assert content_chunk.metadata.get("sas_block_count") == 1
    assert content_chunk.metadata.get("sas_block_types") == ["proc"]


def test_chunk_validate_provenance_fails_on_missing_fields() -> None:
    from sas_rag.ingestion.models.records import ChunkRecord

    incomplete = ChunkRecord(
        chunk_id="bad-chunk",
        text="incomplete",
        metadata={"chunk_id": "bad-chunk", "source_uri": "test"},
    )
    with pytest.raises(ValueError, match="missing metadata fields"):
        incomplete.validate_provenance()


def test_chunk_validate_provenance_passes_when_complete() -> None:
    from sas_rag.ingestion.models.records import ChunkRecord

    complete = ChunkRecord(
        chunk_id="good-chunk",
        text="complete",
        metadata={
            "chunk_id": "good-chunk",
            "source_uri": "docs/test.pdf",
            "title": "Test",
            "version": "9.4",
            "section_path": "Test > Page 1",
            "source_type": "pdf",
            "content_hash": "abc123",
        },
    )
    complete.validate_provenance()
