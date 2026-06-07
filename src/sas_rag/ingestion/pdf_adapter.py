from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol

from pypdf import PdfReader

from sas_rag.ingestion.models.records import DocumentUnit, SourceRecord

logger = logging.getLogger(__name__)


class SourceAdapter(Protocol):
    source_type: str

    def load(self, source: SourceRecord, repo_root: Path) -> list[DocumentUnit]: ...


class PdfAdapter:
    source_type = "pdf"

    def load(self, source: SourceRecord, repo_root: Path) -> list[DocumentUnit]:
        pdf_path = source.path(repo_root)
        logger.info(f"Loading PDF: {pdf_path}")

        if not pdf_path.exists():
            raise FileNotFoundError(f"Missing PDF source: {pdf_path}")

        reader = PdfReader(str(pdf_path))
        units: list[DocumentUnit] = []
        empty_pages = 0

        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                empty_pages += 1
                continue
            units.append(
                DocumentUnit(
                    source=source,
                    page=page_index,
                    text=text,
                    heading_path=(source.title, f"Page {page_index}"),
                )
            )

        logger.info(f"PDF loaded: {len(units)} pages with text, {empty_pages} empty pages skipped")
        return units
