# PARSE-002 - Normalize Extracted Text and Headings

Type: Enabler Story
Parent: [Parser Adapter Layer](../enabler-parser-adapter-layer.md)
Capability: Corpus ingestion and provenance
Sprint: Alpha
Points: 5
Status: Done
Dependencies: PARSE-001, PROV-001
Wiki: [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md), [Chunking Strategy](../../docs/wiki/chunking-strategy.md)

## Story

As a retrieval engineer, I want normalized text and headings, so that chunking can preserve meaningful SAS documentation structure.

## Detail

Normalize parser output into predictable text and heading paths before chunking. This improves citation readability and chunk stability.

## Acceptance Criteria

- Extracted text has predictable whitespace and heading boundaries.
- Heading path is available for downstream provenance and chunking.
- Code examples remain distinguishable from prose when parser output exposes that signal.

## Implementation Notes

- Keep normalization deterministic.
- Avoid destructive cleanup that removes SAS syntax or examples.
- Preserve enough heading hierarchy for section-level citations.

## Done Evidence

- `normalize_text()` and `normalize_unit()` implemented in `src/sas_rag/ingestion/normalizer.py`.
- Deterministic whitespace cleanup and heading path construction.
- `NormalizedUnit` includes `section_path = " > ".join(heading_path)` for downstream provenance.
