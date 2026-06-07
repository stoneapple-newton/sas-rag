# Parser Adapter Layer

Type: Enabler
Capability: Corpus ingestion and provenance
Priority: P0
Sprint target: Alpha/Beta
Owner role: Data Engineer
Status: Done
Dependencies: ING-001

## Intent

Create a loader and normalization layer that can support SAS documentation formats without coupling ingestion logic to one parser implementation.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| PARSE-001 | Enabler | Create loader adapter interface for HTML/PDF/text | 5 | Alpha | ING-001 |
| PARSE-002 | Enabler | Normalize extracted text and headings | 5 | Alpha | PARSE-001, PROV-001 |
| PARSE-003 | Enabler | Capture parser errors and skipped-source reports | 3 | Beta | PARSE-001 |

## Story Details

### PARSE-001 - Create loader adapter interface for HTML/PDF/text

As a data engineer, I want parser adapters behind a common interface, so that source-specific parsing can change without rewriting ingestion orchestration.

Acceptance criteria:
- Interface accepts source metadata and returns normalized document units.
- HTML, PDF, and plain text are represented as supported source types, even if only one is fully implemented first.
- Adapter output includes raw text, source metadata, and structural hints when available.

### PARSE-002 - Normalize extracted text and headings

As a retrieval engineer, I want normalized text and headings, so that chunking can preserve meaningful SAS documentation structure.

Acceptance criteria:
- Extracted text has predictable whitespace and heading boundaries.
- Heading path is available for downstream provenance and chunking.
- Code examples remain distinguishable from prose when parser output exposes that signal.

### PARSE-003 - Capture parser errors and skipped-source reports

As a product and tech lead, I want parse errors and skipped sources reported, so that source coverage decisions are visible during sprint demos.

Acceptance criteria:
- Parser failures do not crash the whole batch unless configured as fatal.
- Report includes failed source, error reason, and ingestion status.
- Skipped sources are distinguishable from failed sources.

## Definition of Done

- Adapter interface is documented.
- Normalized output supports provenance and chunking stories.
- Parse failures are reported clearly.

Current status:
- Done for the PDF-first PI 1 corpus.
- HTML/text adapters remain future extension points behind the existing adapter interface.
