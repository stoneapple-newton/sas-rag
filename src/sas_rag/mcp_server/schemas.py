from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


SCHEMA_VERSION = "1.0"


class ToolError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: Literal["validation_error", "not_found", "insufficient_evidence", "configuration_error", "internal_error"]
    message: str
    details: dict[str, Any] | None = None


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str | None = None
    title: str | None = None
    source_uri: str | None = None
    version: str | None = None
    section_path: str | None = None
    page: int | None = None
    source_family: str | None = None
    chunk_type: str | None = None
    score: float | None = None


class SearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rank: int = Field(ge=1)
    score: float
    text: str
    citation: Citation
    metadata: dict[str, Any]


class SearchSasDocsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = SCHEMA_VERSION
    query: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)
    filters: dict[str, str | int | float | bool] | None = None


class SearchSasDocsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = SCHEMA_VERSION
    results: list[SearchResult] = Field(default_factory=list)
    error: ToolError | None = None

