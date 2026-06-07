from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal

from langchain_core.embeddings import Embeddings
from pydantic import ValidationError

from sas_rag.config import settings
from sas_rag.ingestion.chroma_index import create_openai_embeddings
from sas_rag.mcp_server.schemas import Citation, SearchResult, SearchSasDocsRequest, SearchSasDocsResponse, ToolError
from sas_rag.retrieval.search import format_citation, search_with_filters

logger = logging.getLogger(__name__)


def search_sas_docs_payload(
    *,
    query: str,
    top_k: int = 5,
    filters: dict[str, Any] | None = None,
    schema_version: str = "1.0",
    persist_directory: Path | None = None,
    collection_name: str | None = None,
    embeddings: Embeddings | None = None,
) -> dict[str, Any]:
    """Return the versioned payload for the read-only search_sas_docs MCP tool."""
    try:
        request = SearchSasDocsRequest(
            schema_version=schema_version,
            query=query,
            top_k=top_k,
            filters=filters,
        )
    except ValidationError as exc:
        return _error_response(
            code="validation_error",
            message="Invalid search_sas_docs request.",
            details={"errors": exc.errors()},
        )

    try:
        embedding_function = embeddings or create_openai_embeddings()
        resolved_persist_directory = persist_directory or Path(settings.sas_rag_chroma_path)
        resolved_collection_name = collection_name or settings.sas_rag_chroma_collection

        logger.info(
            "MCP search_sas_docs started",
            extra={
                "query": request.query,
                "top_k": request.top_k,
                "filters": request.filters,
                "collection_name": resolved_collection_name,
            },
        )
        raw_results = search_with_filters(
            persist_directory=resolved_persist_directory,
            collection_name=resolved_collection_name,
            embeddings=embedding_function,
            query=request.query,
            k=request.top_k,
            filters=dict(request.filters) if request.filters else None,
        )
    except (FileNotFoundError, RuntimeError) as exc:
        logger.warning("MCP search_sas_docs configuration failed: %s", exc)
        return _error_response(code="configuration_error", message=str(exc))
    except Exception as exc:
        logger.exception("MCP search_sas_docs failed")
        return _error_response(code="internal_error", message=str(exc))

    response = SearchSasDocsResponse(
        results=[
            SearchResult(
                rank=rank,
                score=float(result["score"]),
                text=str(result["text"]),
                citation=Citation(**format_citation(result)),
                metadata=dict(result["metadata"]),
            )
            for rank, result in enumerate(raw_results, start=1)
        ]
    )
    logger.info(
        "MCP search_sas_docs completed",
        extra={"query": request.query, "result_count": len(response.results)},
    )
    return response.model_dump(mode="json")


def _error_response(
    *,
    code: Literal["validation_error", "not_found", "insufficient_evidence", "configuration_error", "internal_error"],
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return SearchSasDocsResponse(
        results=[],
        error=ToolError(code=code, message=message, details=details),
    ).model_dump(mode="json")
