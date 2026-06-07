from __future__ import annotations

import asyncio
import json
from pathlib import Path

from langchain_core.embeddings import Embeddings

from sas_rag.ingestion.chroma_index import index_chunks_to_chroma
from sas_rag.mcp_server.schemas import SCHEMA_VERSION
from sas_rag.mcp_server.server import create_server, validate_startup_configuration
from sas_rag.mcp_server.tools import search_sas_docs_payload


class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        lowered = text.lower()
        return [
            float(lowered.count("proc")),
            float(lowered.count("sql")),
            float(lowered.count("macro")),
            float(lowered.count("data")),
        ]


def _write_chunks(tmp_path: Path) -> Path:
    chunks_path = tmp_path / "chunks.jsonl"
    records = [
        {
            "chunk_id": "sql-1",
            "text": "PROC SQL joins tables with FROM and WHERE clauses.",
            "metadata": {
                "chunk_id": "sql-1",
                "source_uri": "docs/sas-documents/sqlproc.pdf",
                "title": "SAS SQL Procedure User's Guide",
                "version": "9.4",
                "section_path": "SQL Procedure > Joins",
                "source_type": "pdf",
                "content_hash": "abc123",
                "page": 10,
                "source_family": "proc-sql",
                "priority": "P0",
            },
        },
        {
            "chunk_id": "macro-1",
            "text": "The %LET statement creates a macro variable.",
            "metadata": {
                "chunk_id": "macro-1",
                "source_uri": "docs/sas-documents/mcrolref.pdf",
                "title": "SAS Macro Language Reference",
                "version": "9.4",
                "section_path": "Macro Language > %LET",
                "source_type": "pdf",
                "content_hash": "def456",
                "page": 82,
                "source_family": "macro",
                "priority": "P0",
            },
        },
    ]
    chunks_path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
    return chunks_path


def _index(tmp_path: Path) -> Path:
    persist_directory = tmp_path / "chroma"
    index_chunks_to_chroma(
        chunks_path=_write_chunks(tmp_path),
        persist_directory=persist_directory,
        collection_name="test_collection",
        embeddings=FakeEmbeddings(),
        embedding_model="fake",
        reset=True,
    )
    return persist_directory


def test_search_sas_docs_contract_success(tmp_path: Path) -> None:
    persist_directory = _index(tmp_path)

    payload = search_sas_docs_payload(
        query="PROC SQL join",
        top_k=1,
        filters={"source_family": "proc-sql"},
        persist_directory=persist_directory,
        collection_name="test_collection",
        embeddings=FakeEmbeddings(),
    )

    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["error"] is None
    assert len(payload["results"]) == 1
    assert payload["results"][0]["rank"] == 1
    assert payload["results"][0]["citation"]["chunk_id"] == "sql-1"
    assert payload["results"][0]["citation"]["source_uri"] == "docs/sas-documents/sqlproc.pdf"


def test_search_sas_docs_contract_validation_error() -> None:
    payload = search_sas_docs_payload(query="", top_k=0, embeddings=FakeEmbeddings())

    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["results"] == []
    assert payload["error"]["code"] == "validation_error"
    assert payload["error"]["details"]["errors"]


def test_create_server_registers_search_tool() -> None:
    server = create_server()
    tools = asyncio.run(server.list_tools())

    assert server.name == "sas-rag"
    assert [tool.name for tool in tools] == ["search_sas_docs"]


def test_startup_validation_fails_without_chroma_index(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("sas_rag.mcp_server.server.settings.openai_api_key", "test-key")
    monkeypatch.setattr("sas_rag.mcp_server.server.settings.sas_rag_chroma_path", str(tmp_path / "missing"))

    try:
        validate_startup_configuration()
    except FileNotFoundError as exc:
        assert "Missing Chroma index" in str(exc)
    else:
        raise AssertionError("Expected missing Chroma index to fail startup validation")
