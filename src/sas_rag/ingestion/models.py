from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_PROVENANCE_FIELDS = {
    "chunk_id",
    "source_uri",
    "title",
    "version",
    "section_path",
    "source_type",
    "content_hash",
}


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    title: str
    source_uri: str
    local_path: str
    source_family: str
    sas_version: str
    priority: str
    source_type: str
    ingestion_status: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceRecord":
        return cls(**data)

    def path(self, repo_root: Path) -> Path:
        return (repo_root / self.local_path).resolve()


@dataclass(frozen=True)
class DocumentUnit:
    source: SourceRecord
    page: int
    text: str
    heading_path: tuple[str, ...]


@dataclass(frozen=True)
class NormalizedUnit:
    source: SourceRecord
    page: int
    markdown: str
    section_path: str


@dataclass(frozen=True)
class ChunkRecord:
    chunk_id: str
    text: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"chunk_id": self.chunk_id, "text": self.text, "metadata": self.metadata}

    def validate_provenance(self) -> None:
        missing = REQUIRED_PROVENANCE_FIELDS - set(self.metadata)
        if missing:
            raise ValueError(f"Chunk {self.chunk_id} missing metadata fields: {sorted(missing)}")


@dataclass
class SourceReport:
    source_id: str
    title: str
    status: str
    pages_loaded: int = 0
    chunks_emitted: int = 0
    content_hash: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IngestionReport:
    sources: list[SourceReport] = field(default_factory=list)

    def add(self, source_report: SourceReport) -> None:
        self.sources.append(source_report)

    def summary(self) -> dict[str, int]:
        statuses: dict[str, int] = {}
        for source in self.sources:
            statuses[source.status] = statuses.get(source.status, 0) + 1
        statuses["chunks_emitted"] = sum(source.chunks_emitted for source in self.sources)
        statuses["pages_loaded"] = sum(source.pages_loaded for source in self.sources)
        return statuses

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "sources": [source.to_dict() for source in self.sources],
        }
