from __future__ import annotations

from pydantic import BaseModel, Field


class IngestionConfig(BaseModel):
    source_dir: str = Field(default="docs/sas-documents")
    whitelist_path: str = Field(default="data/source_whitelist.json")
    output_dir: str = Field(default="data/ingestion/runs/latest")
    max_chars: int = Field(default=4000, ge=100, le=10000)


class ChromaIndexConfig(BaseModel):
    chunks_path: str
    persist_directory: str = Field(default="data/chroma")
    collection_name: str = Field(default="sas_94_docs")
    embedding_model: str = Field(default="text-embedding-3-small")
    priority: str | None = None
    reset: bool = False
    batch_size: int = Field(default=256, ge=1, le=1000)
