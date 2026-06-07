from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from sas_rag.config import settings
from sas_rag.logging_config import configure_logging
from sas_rag.mcp_server.tools import search_sas_docs_payload

logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    server = FastMCP(
        "sas-rag",
        instructions=(
            "Read-only SAS 9.4 documentation retrieval tools. "
            "Use citations from tool responses when answering SAS questions."
        ),
    )

    @server.tool(
        name="search_sas_docs",
        description="Search the local official SAS 9.4 documentation index with optional metadata filters.",
        structured_output=True,
    )
    def search_sas_docs(
        query: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
        schema_version: str = "1.0",
    ) -> dict[str, Any]:
        return search_sas_docs_payload(
            query=query,
            top_k=top_k,
            filters=filters,
            schema_version=schema_version,
        )

    return server


def validate_startup_configuration() -> None:
    persist_directory = Path(settings.sas_rag_chroma_path)
    collection_db = persist_directory / "chroma.sqlite3"
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required for live MCP retrieval.")
    if not collection_db.exists():
        raise FileNotFoundError(
            f"Missing Chroma index at {collection_db}. "
            "Create it with: uv run python -m sas_rag.ingestion.cli index-chroma"
        )
    logger.info(
        "MCP startup configuration validated",
        extra={
            "persist_directory": str(persist_directory),
            "collection_name": settings.sas_rag_chroma_collection,
        },
    )


def main() -> None:
    configure_logging()
    validate_startup_configuration()
    logger.info("Starting SAS RAG MCP server over stdio")
    create_server().run("stdio")


if __name__ == "__main__":
    main()
