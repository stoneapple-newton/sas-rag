from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from sas_rag.ingestion.models import DocumentUnit, SourceRecord


class PdfAdapter:
    source_type = "pdf"

    def load(self, source: SourceRecord, repo_root: Path) -> list[DocumentUnit]:
        pdf_path = source.path(repo_root)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Missing PDF source: {pdf_path}")

        reader = PdfReader(str(pdf_path))
        units: list[DocumentUnit] = []
        for page_index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue
            units.append(
                DocumentUnit(
                    source=source,
                    page=page_index,
                    text=text,
                    heading_path=(source.title, f"Page {page_index}"),
                )
            )
        return units
