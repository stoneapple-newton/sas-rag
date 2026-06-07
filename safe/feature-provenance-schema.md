# Provenance Schema

Type: Feature
Capability: Corpus ingestion and provenance
Priority: P0
Sprint target: Alpha/Beta
Owner role: Data Engineer
Status: Proposed
Dependencies: None

## Intent

Define and enforce source metadata so every retrieved answer can cite authoritative SAS material and every chunk can be traced back to its origin.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| PROV-001 | Enabler | Define chunk provenance metadata schema | 3 | Alpha | ING-001 |
| PROV-002 | Feature | Attach provenance to every emitted chunk | 5 | Alpha | PROV-001, PARSE-001 |
| PROV-003 | Feature | Validate provenance completeness during ingestion | 3 | Beta | PROV-002 |

## Story Details

### PROV-001 - Define chunk provenance metadata schema

As a retrieval engineer, I want a required provenance schema, so that every chunk carries enough evidence for citation, filtering, and debugging.

Acceptance criteria:
- Required fields include `chunk_id`, `source_uri`, `title`, `version`, `section_path`, `source_type`, and content hash.
- Optional fields for page, heading level, product area, and source family are documented.
- Schema is documented in human-readable Markdown and is suitable for validation in tests.

### PROV-002 - Attach provenance to every emitted chunk

As a retrieval user, I want every chunk to carry provenance, so that search results and answers can identify their SAS source.

Acceptance criteria:
- Parser and chunker outputs include required provenance fields.
- Missing required fields fail fast during sample ingestion.
- Chunk IDs are deterministic for unchanged source content and section context.

### PROV-003 - Validate provenance completeness during ingestion

As a QA engineer, I want automated provenance validation during ingestion, so that incomplete chunks never enter the index silently.

Acceptance criteria:
- Ingestion validates every chunk before indexing.
- Validation failures include source URI and reason.
- Ingestion summary reports total chunks, valid chunks, and rejected chunks.
- Tests cover at least one valid and one invalid metadata payload.

## Definition of Done

- Required metadata schema is documented.
- Validation is part of ingestion.
- No indexed PI 1 chunk lacks required provenance.
