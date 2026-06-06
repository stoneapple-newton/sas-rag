from __future__ import annotations

import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings


@dataclass(frozen=True)
class ChromaIndexReport:
    chunks_path: str
    persist_directory: str
    collection_name: str
    embedding_model: str
    priority_filter: str | None
    reset: bool
    total_chunks: int
    indexed_chunks: int
    skipped_chunks: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_chunk_documents(chunks_path: Path, priority: str | None = None) -> tuple[list[Document], int, int]:
    documents: list[Document] = []
    total_chunks = 0
    skipped_chunks = 0

    with chunks_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            total_chunks += 1
            item = json.loads(line)
            text = item.get("text")
            metadata = item.get("metadata")
            if not isinstance(text, str) or not isinstance(metadata, dict):
                raise ValueError(f"Invalid chunk record at line {line_number}")
            if priority and metadata.get("priority") != priority:
                skipped_chunks += 1
                continue
            documents.append(Document(page_content=text, metadata=_sanitize_metadata(metadata)))

    return documents, total_chunks, skipped_chunks


def document_ids(documents: Iterable[Document]) -> list[str]:
    ids: list[str] = []
    for document in documents:
        chunk_id = document.metadata.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            raise ValueError("Every indexed document must include a non-empty chunk_id")
        ids.append(chunk_id)
    return ids


def create_openai_embeddings(model: str | None = None, load_env: bool = True) -> OpenAIEmbeddings:
    if load_env:
        load_dotenv()
    embedding_model = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for Chroma indexing. Add it to .env or the environment.")
    return OpenAIEmbeddings(model=embedding_model)


def index_chunks_to_chroma(
    chunks_path: Path,
    persist_directory: Path,
    collection_name: str,
    embeddings: Embeddings,
    embedding_model: str,
    priority: str | None = None,
    reset: bool = False,
    batch_size: int = 256,
) -> ChromaIndexReport:
    if not chunks_path.exists():
        raise FileNotFoundError(f"Missing chunks file: {chunks_path}")
    if reset and persist_directory.exists():
        shutil.rmtree(persist_directory)
    persist_directory.mkdir(parents=True, exist_ok=True)

    documents, total_chunks, skipped_chunks = load_chunk_documents(chunks_path, priority=priority)
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )

    for start in range(0, len(documents), batch_size):
        batch = documents[start : start + batch_size]
        vectorstore.add_documents(batch, ids=document_ids(batch))

    return ChromaIndexReport(
        chunks_path=str(chunks_path),
        persist_directory=str(persist_directory),
        collection_name=collection_name,
        embedding_model=embedding_model,
        priority_filter=priority,
        reset=reset,
        total_chunks=total_chunks,
        indexed_chunks=len(documents),
        skipped_chunks=skipped_chunks,
    )


def query_chroma(
    persist_directory: Path,
    collection_name: str,
    embeddings: Embeddings,
    query: str,
    k: int = 5,
) -> list[dict[str, Any]]:
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )
    results = vectorstore.similarity_search_with_score(query, k=k)
    return [
        {
            "score": score,
            "text": document.page_content,
            "metadata": document.metadata,
        }
        for document, score in results
    ]


def write_report(report: ChromaIndexReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")


def _sanitize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in metadata.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            sanitized[key] = value
        else:
            sanitized[key] = str(value)
    return sanitized
