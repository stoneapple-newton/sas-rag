from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


def build_filter_dict(filters: dict[str, Any]) -> dict[str, Any] | None:
    """Build Chroma-compatible filter from metadata filters."""
    if not filters:
        return None

    # Chroma supports simple equality filters and $and/$or operators
    chroma_filters: dict[str, Any] = {}
    for key, value in filters.items():
        if value is not None:
            chroma_filters[key] = value

    return chroma_filters if chroma_filters else None


def search_with_filters(
    persist_directory: Path,
    collection_name: str,
    embeddings: Embeddings,
    query: str,
    k: int = 5,
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Search Chroma with optional metadata filters.

    Args:
        persist_directory: Path to Chroma persistence directory
        collection_name: Name of the Chroma collection
        embeddings: Embedding function
        query: Search query string
        k: Number of results to return
        filters: Optional metadata filters (e.g., {"source_family": "macro", "priority": "P0"})

    Returns:
        List of result dictionaries with score, text, and metadata
    """
    logger.info("Searching with filters", extra={
        "query": query,
        "k": k,
        "filters": filters,
    })

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )

    filter_dict = build_filter_dict(filters) if filters else None

    if filter_dict:
        logger.debug(f"Applying metadata filter: {filter_dict}")
        results = vectorstore.similarity_search_with_score(query, k=k, filter=filter_dict)
    else:
        results = vectorstore.similarity_search_with_score(query, k=k)

    logger.debug(f"Query returned {len(results)} results")

    formatted_results = []
    for document, score in results:
        result = {
            "score": float(score),
            "text": document.page_content,
            "metadata": document.metadata,
        }
        formatted_results.append(result)

    return formatted_results


def search_by_source_family(
    persist_directory: Path,
    collection_name: str,
    embeddings: Embeddings,
    query: str,
    source_family: str,
    k: int = 5,
) -> list[dict[str, Any]]:
    """Convenience function to search within a specific source family."""
    return search_with_filters(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embeddings=embeddings,
        query=query,
        k=k,
        filters={"source_family": source_family},
    )


def search_by_chunk_type(
    persist_directory: Path,
    collection_name: str,
    embeddings: Embeddings,
    query: str,
    chunk_type: str,
    k: int = 5,
) -> list[dict[str, Any]]:
    """Convenience function to search for specific chunk types (e.g., 'example', 'syntax')."""
    return search_with_filters(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embeddings=embeddings,
        query=query,
        k=k,
        filters={"chunk_type": chunk_type},
    )


def format_citation(result: dict[str, Any]) -> dict[str, Any]:
    """Extract citation-ready fields from a search result."""
    metadata = result.get("metadata", {})
    return {
        "chunk_id": metadata.get("chunk_id"),
        "title": metadata.get("title"),
        "source_uri": metadata.get("source_uri"),
        "version": metadata.get("version"),
        "section_path": metadata.get("section_path"),
        "page": metadata.get("page"),
        "source_family": metadata.get("source_family"),
        "chunk_type": metadata.get("chunk_type"),
        "score": result.get("score"),
    }
