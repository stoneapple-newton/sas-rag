from __future__ import annotations

import json
from pathlib import Path

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from sas_rag.ingestion.chroma_index import (
    create_openai_embeddings,
    document_ids,
    index_chunks_to_chroma,
    load_chunk_documents,
    query_chroma,
)


class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        return [
            float(text.lower().count("proc")),
            float(text.lower().count("sql")),
            float(text.lower().count("data")),
            float(text.lower().count("graph")),
        ]


def _chunk(chunk_id: str, priority: str, text: str) -> dict:
    return {
        "chunk_id": chunk_id,
        "text": text,
        "metadata": {
            "chunk_id": chunk_id,
            "source_uri": f"docs/sas-documents/{chunk_id}.pdf",
            "title": "SAS SQL Procedure User's Guide",
            "version": "9.4",
            "section_path": "SAS SQL Procedure User's Guide > Page 1",
            "source_type": "pdf",
            "content_hash": "abc123",
            "page": 1,
            "source_family": "proc-sql",
            "local_path": f"docs/sas-documents/{chunk_id}.pdf",
            "priority": priority,
        },
    }


def _chunks_path(tmp_path: Path) -> Path:
    chunks_path = tmp_path / "chunks.jsonl"
    records = [
        _chunk("p0-a", "P0", "PROC SQL joins tables."),
        _chunk("p1-a", "P1", "Graph procedure reference."),
        _chunk("p0-b", "P0", "DATA step syntax."),
    ]
    chunks_path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
    return chunks_path


def test_load_chunk_documents_filters_by_priority(tmp_path: Path) -> None:
    documents, total_chunks, skipped_chunks = load_chunk_documents(_chunks_path(tmp_path), priority="P0")

    assert total_chunks == 3
    assert skipped_chunks == 1
    assert [document.metadata["chunk_id"] for document in documents] == ["p0-a", "p0-b"]


def test_document_ids_require_chunk_id() -> None:
    with pytest.raises(ValueError, match="chunk_id"):
        document_ids([Document(page_content="missing", metadata={})])


def test_create_openai_embeddings_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        create_openai_embeddings(load_env=False)


def test_index_chunks_to_chroma_and_query(tmp_path: Path) -> None:
    persist_directory = tmp_path / "chroma"
    report = index_chunks_to_chroma(
        chunks_path=_chunks_path(tmp_path),
        persist_directory=persist_directory,
        collection_name="test_collection",
        embeddings=FakeEmbeddings(),
        embedding_model="fake",
        priority="P0",
        reset=True,
        batch_size=1,
    )

    assert report.total_chunks == 3
    assert report.indexed_chunks == 2
    assert report.skipped_chunks == 1

    results = query_chroma(
        persist_directory=persist_directory,
        collection_name="test_collection",
        embeddings=FakeEmbeddings(),
        query="PROC SQL",
        k=1,
    )

    assert len(results) == 1
    assert results[0]["metadata"]["chunk_id"] == "p0-a"
    assert results[0]["metadata"]["priority"] == "P0"
