# PARSE-003 - Capture Parser Errors and Skipped-Source Reports

Type: Enabler Story
Parent: [Parser Adapter Layer](../enabler-parser-adapter-layer.md)
Capability: Corpus ingestion and provenance
Sprint: Beta
Points: 3
Status: Proposed
Dependencies: PARSE-001
Wiki: [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md)

## Story

As a product and tech lead, I want parse errors and skipped sources reported, so that source coverage decisions are visible during sprint demos.

## Detail

Add structured reporting around parser failures, skipped sources, and fatal ingestion errors. This avoids silent corpus gaps.

## Acceptance Criteria

- Parser failures do not crash the whole batch unless configured as fatal.
- Report includes failed source, error reason, and ingestion status.
- Skipped sources are distinguishable from failed sources.

## Implementation Notes

- Include source URI or source ID in every error.
- Keep reports readable for sprint demos.
- Make failure behavior configurable for local smoke versus release ingestion.

## Done Evidence

- Parser error report sample.
- Skipped-source report sample.
- Batch run showing nonfatal handling.
