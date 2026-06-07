# PARSE-001 - Create Loader Adapter Interface for HTML/PDF/Text

Type: Enabler Story
Parent: [Parser Adapter Layer](../enabler-parser-adapter-layer.md)
Capability: Corpus ingestion and provenance
Sprint: Alpha
Points: 5
Status: Done
Dependencies: ING-001
Wiki: [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md), [SAS Corpus](../../docs/wiki/sas-corpus.md)

## Story

As a data engineer, I want parser adapters behind a common interface, so that source-specific parsing can change without rewriting ingestion orchestration.

## Detail

Create a parser boundary that accepts source metadata and emits normalized document units. The interface should accommodate HTML, PDF, and plain text source types even if PI 1 starts with the easiest official source format.

## Acceptance Criteria

- Interface accepts source metadata and returns normalized document units.
- HTML, PDF, and plain text are represented as supported source types, even if only one is fully implemented first.
- Adapter output includes raw text, source metadata, and structural hints when available.

## Implementation Notes

- Do not bind ingestion orchestration to a specific parser library.
- Make parser failures reportable.
- Preserve structure signals for chunking.

## Done Evidence

- `SourceAdapter` Protocol defined in `src/sas_rag/ingestion/pdf_adapter.py`.
- `PdfAdapter` implements `SourceAdapter` with `source_type = "pdf"` and `load()` method.
- `run_ingestion()` uses adapter polymorphically via `PdfAdapter()` instance.
