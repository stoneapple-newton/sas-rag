from __future__ import annotations

import logging
import re

from sas_rag.ingestion.models.records import DocumentUnit, NormalizedUnit

logger = logging.getLogger(__name__)


_HORIZONTAL_WHITESPACE = re.compile(r"[ \t]+")
_TOO_MANY_BLANK_LINES = re.compile(r"\n{3,}")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [_HORIZONTAL_WHITESPACE.sub(" ", line).strip() for line in text.split("\n")]
    normalized = "\n".join(line for line in lines if line)
    return _TOO_MANY_BLANK_LINES.sub("\n\n", normalized).strip()


def normalize_unit(unit: DocumentUnit) -> NormalizedUnit:
    original_len = len(unit.text)
    text = normalize_text(unit.text)
    normalized_len = len(text)

    section_path = " > ".join(unit.heading_path)
    markdown = f"# {unit.source.title}\n\n## Page {unit.page}\n\n{text}\n"

    logger.debug(f"Normalized unit: {unit.source.source_id} page {unit.page} (text: {original_len} -> {normalized_len} chars)")

    return NormalizedUnit(
        source=unit.source,
        page=unit.page,
        markdown=markdown,
        section_path=section_path,
    )
