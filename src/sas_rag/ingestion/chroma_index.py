from __future__ import annotations

import json
import logging
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from sas_rag.config import settings

logger = logging.getLogger(__name__)


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
    duplicate_chunks: int

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


def create_openai_embeddings(model: str | None = None) -> OpenAIEmbeddings:
    embedding_model = model or settings.openai_embedding_model
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required for Chroma indexing. Add it to .env or the environment.")
    return OpenAIEmbeddings(model=embedding_model, api_key=settings.openai_api_key)


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
    logger.info("Starting Chroma indexing", extra={
        "chunks_path": str(chunks_path),
        "persist_directory": str(persist_directory),
        "collection_name": collection_name,
        "embedding_model": embedding_model,
        "priority": priority,
        "reset": reset,
    })

    if not chunks_path.exists():
        raise FileNotFoundError(f"Missing chunks file: {chunks_path}")
    if reset and persist_directory.exists():
        logger.info(f"Resetting Chroma directory: {persist_directory}")
        shutil.rmtree(persist_directory)
    persist_directory.mkdir(parents=True, exist_ok=True)

    documents, total_chunks, skipped_chunks = load_chunk_documents(chunks_path, priority=priority)
    logger.debug(f"Loaded {len(documents)} documents for indexing (total={total_chunks}, skipped={skipped_chunks})")

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )

    existing_ids = set(vectorstore.get()["ids"])
    logger.debug(f"Found {len(existing_ids)} existing documents in collection")

    new_documents = [doc for doc in documents if doc.metadata.get("chunk_id") not in existing_ids]
    duplicate_chunks = len(documents) - len(new_documents)

    logger.info(f"Indexing {len(new_documents)} new documents (duplicates skipped: {duplicate_chunks})")

    for start in range(0, len(new_documents), batch_size):
        batch = new_documents[start : start + batch_size]
        logger.debug(f"Indexing batch {start // batch_size + 1}/{(len(new_documents) - 1) // batch_size + 1}, size={len(batch)}")
        vectorstore.add_documents(batch, ids=document_ids(batch))

    logger.info("Chroma indexing complete", extra={
        "total_chunks": total_chunks,
        "indexed_chunks": len(new_documents),
        "skipped_chunks": skipped_chunks,
        "duplicate_chunks": duplicate_chunks,
    })

    return ChromaIndexReport(
        chunks_path=str(chunks_path),
        persist_directory=str(persist_directory),
        collection_name=collection_name,
        embedding_model=embedding_model,
        priority_filter=priority,
        reset=reset,
        total_chunks=total_chunks,
        indexed_chunks=len(new_documents),
        skipped_chunks=skipped_chunks,
        duplicate_chunks=duplicate_chunks,
    )


def query_chroma(
    persist_directory: Path,
    collection_name: str,
    embeddings: Embeddings,
    query: str,
    k: int = 5,
) -> list[dict[str, Any]]:
    logger.info(f"Querying Chroma: '{query}' (k={k})")

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )
    results = vectorstore.similarity_search_with_score(query, k=k)

    logger.debug(f"Query returned {len(results)} results")

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
