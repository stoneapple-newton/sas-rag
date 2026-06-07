from __future__ import annotations

import hashlib

from sas_rag.ingestion.models import ChunkRecord, NormalizedUnit


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_hash(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_chunk_id(source_id: str, section_path: str, ordinal: int, text: str) -> str:
    basis = f"{source_id}|{section_path}|{ordinal}|{content_hash(text)}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24]


def split_markdown(markdown: str, max_chars: int) -> list[str]:
    if len(markdown) <= max_chars:
        return [markdown.strip()]

    paragraphs = [part.strip() for part in markdown.split("\n\n") if part.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0
    for paragraph in paragraphs:
        paragraph_size = len(paragraph) + 2
        if current and current_size + paragraph_size > max_chars:
            chunks.append("\n\n".join(current).strip())
            current = []
            current_size = 0
        if paragraph_size > max_chars:
            chunks.extend(_split_long_paragraph(paragraph, max_chars))
            continue
        current.append(paragraph)
        current_size += paragraph_size
    if current:
        chunks.append("\n\n".join(current).strip())
    return chunks


def _split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    return [paragraph[index : index + max_chars].strip() for index in range(0, len(paragraph), max_chars)]


def chunk_unit(unit: NormalizedUnit, source_content_hash: str, max_chars: int = 4000) -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    for ordinal, text in enumerate(split_markdown(unit.markdown, max_chars=max_chars), start=1):
        chunk_id = stable_chunk_id(unit.source.source_id, unit.section_path, ordinal, text)
        metadata = {
            "chunk_id": chunk_id,
            "source_uri": unit.source.source_uri,
            "title": unit.source.title,
            "version": unit.source.sas_version,
            "section_path": unit.section_path,
            "source_type": unit.source.source_type,
            "content_hash": source_content_hash,
            "page": unit.page,
            "source_family": unit.source.source_family,
            "local_path": unit.source.local_path,
            "priority": unit.source.priority,
        }
        chunk = ChunkRecord(chunk_id=chunk_id, text=text, metadata=metadata)
        chunk.validate_provenance()
        chunks.append(chunk)
    return chunks
