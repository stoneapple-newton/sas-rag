from __future__ import annotations

import hashlib
import logging
import re
from typing import Any

from sas_rag.ingestion.models.records import ChunkRecord, NormalizedUnit

logger = logging.getLogger(__name__)


# Heading detection patterns for SAS documentation
_HEADING_PATTERNS = [
    re.compile(r"^(?:PART\s+\d+|Chapter\s+\d+\s*/\s*.+)$", re.IGNORECASE),
    re.compile(r"^(?:Overview|Syntax|Examples?|Details|See Also|References?)$", re.IGNORECASE),
    re.compile(r"^(?:Definition|Concept|Procedure|Statement):?\s+.+$", re.IGNORECASE),
]

# SAS code block boundaries
_SAS_BLOCK_START = re.compile(
    r"^\s*(PROC\s+\w+|DATA\s+\w+|%MACRO\s+\w+)", re.IGNORECASE | re.MULTILINE
)
_SAS_BLOCK_END = re.compile(
    r"^\s*(RUN\s*;|QUIT\s*;|%MEND\s*\w*)", re.IGNORECASE | re.MULTILINE
)


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


def _is_heading_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    for pattern in _HEADING_PATTERNS:
        if pattern.match(stripped):
            return True
    # Heuristic: short line, no period, title case or all caps
    if len(stripped) < 80 and not stripped.endswith("."):
        if stripped.istitle() or stripped.isupper():
            return True
    return False


def detect_chunk_type(text: str) -> str:
    text_upper = text.upper()
    lines = text.strip().split("\n")
    first_line = lines[0].strip().upper() if lines else ""

    # Check for SAS code blocks
    has_proc = "PROC " in text_upper and "RUN;" in text_upper
    has_data = "DATA " in text_upper and "RUN;" in text_upper
    has_macro = "%MACRO" in text_upper and "%MEND" in text_upper

    if has_proc or has_data or has_macro:
        # Distinguish examples from syntax definitions
        if first_line.startswith(("PROC ", "DATA ", "%MACRO")):
            return "syntax"
        return "example"

    # Check for tables (option tables, argument tables)
    if "|" in text and text.count("\n") > 2:
        lines_with_pipes = sum(1 for line in lines if "|" in line)
        if lines_with_pipes >= 3:
            return "option_table"

    # Check for syntax/argument definitions
    if any(keyword in first_line for keyword in ["SYNTAX:", "ARGUMENT", "OPTION", "DEFAULT"]):
        return "syntax"

    # Check for concept/tutorial content
    if any(keyword in text_upper for keyword in ["OVERVIEW", "CONCEPT", "UNDERSTANDING", "INTRODUCTION"]):
        return "concept"

    # Check for troubleshooting
    if any(keyword in text_upper for keyword in ["ERROR", "WARNING", "TROUBLESHOOT", "CAUTION"]):
        return "troubleshooting"

    return "concept"


def split_on_headings(text: str, max_chars: int) -> list[tuple[str, str | None]]:
    """Split text on heading boundaries, returning (section_text, heading) pairs."""
    lines = text.split("\n")
    sections: list[tuple[str, str | None]] = []
    current_lines: list[str] = []
    current_heading: str | None = None

    for line in lines:
        if _is_heading_line(line):
            if current_lines:
                sections.append(("\n".join(current_lines).strip(), current_heading))
            current_heading = line.strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(("\n".join(current_lines).strip(), current_heading))

    # If no headings found, return the whole text
    if len(sections) <= 1:
        return [(text, None)]

    # Further split oversized sections
    result: list[tuple[str, str | None]] = []
    for section_text, heading in sections:
        if len(section_text) <= max_chars:
            result.append((section_text, heading))
        else:
            # Split oversized section by paragraphs
            result.extend(_split_by_paragraphs(section_text, max_chars, heading))

    return result


def _split_by_paragraphs(text: str, max_chars: int, heading: str | None) -> list[tuple[str, str | None]]:
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
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

    return [(chunk, heading) for chunk in chunks]


def _split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    return [paragraph[index : index + max_chars].strip() for index in range(0, len(paragraph), max_chars)]


def extract_sas_blocks(text: str) -> list[dict[str, Any]]:
    """Extract SAS code blocks with their boundaries."""
    blocks: list[dict[str, Any]] = []
    lines = text.split("\n")
    current_block: list[str] = []
    block_type: str | None = None
    in_block = False

    for line in lines:
        if not in_block:
            match = _SAS_BLOCK_START.search(line)
            if match:
                in_block = True
                block_type = match.group(1).upper().split()[0]
                if block_type.startswith("%"):
                    block_type = "macro"
                elif block_type == "DATA":
                    block_type = "data_step"
                else:
                    block_type = "proc"
                current_block = [line]
            else:
                current_block.append(line)
        else:
            current_block.append(line)
            if _SAS_BLOCK_END.search(line):
                blocks.append({
                    "type": block_type,
                    "text": "\n".join(current_block).strip(),
                    "lines": len(current_block),
                })
                current_block = []
                in_block = False

    if current_block and in_block:
        blocks.append({
            "type": block_type or "code",
            "text": "\n".join(current_block).strip(),
            "lines": len(current_block),
        })

    return blocks


def chunk_unit(
    unit: NormalizedUnit,
    source_content_hash: str,
    max_chars: int = 4000,
    heading_aware: bool = True,
) -> list[ChunkRecord]:
    logger.debug(f"Chunking unit: {unit.source.source_id} page {unit.page}")

    chunks: list[ChunkRecord] = []

    if heading_aware:
        sections = split_on_headings(unit.markdown, max_chars=max_chars)
    else:
        sections = [(unit.markdown, None)]

    logger.debug(f"Split into {len(sections)} sections (heading_aware={heading_aware}, max_chars={max_chars})")

    for ordinal, (section_text, heading) in enumerate(sections, start=1):
        chunk_type = detect_chunk_type(section_text)
        chunk_id = stable_chunk_id(unit.source.source_id, unit.section_path, ordinal, section_text)

        # Build section path with heading if available
        section_path = unit.section_path
        if heading and heading not in section_path:
            section_path = f"{section_path} > {heading}"

        metadata: dict[str, Any] = {
            "chunk_id": chunk_id,
            "source_uri": unit.source.source_uri,
            "title": unit.source.title,
            "version": unit.source.sas_version,
            "section_path": section_path,
            "source_type": unit.source.source_type,
            "content_hash": source_content_hash,
            "page": unit.page,
            "source_family": unit.source.source_family,
            "local_path": unit.source.local_path,
            "priority": unit.source.priority,
            "chunk_type": chunk_type,
        }

        # Detect SAS blocks within the chunk
        sas_blocks = extract_sas_blocks(section_text)
        if sas_blocks:
            metadata["sas_block_types"] = [block["type"] for block in sas_blocks]
            metadata["sas_block_count"] = len(sas_blocks)

        chunk = ChunkRecord(chunk_id=chunk_id, text=section_text, metadata=metadata)
        chunk.validate_provenance()
        chunks.append(chunk)

    logger.debug(f"Emitted {len(chunks)} validated chunks for {unit.source.source_id} page {unit.page}")
    return chunks
