# PROV-003 - Validate Provenance Completeness During Ingestion

Type: Feature Story
Parent: [Provenance Schema](../feature-provenance-schema.md)
Capability: Corpus ingestion and provenance
Sprint: Beta
Points: 3
Status: Proposed
Dependencies: PROV-002
Wiki: [Provenance Schema](../../docs/wiki/provenance-schema.md), [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md)

## Story

As a QA engineer, I want automated provenance validation during ingestion, so that incomplete chunks never enter the index silently.

## Detail

Add a validation gate between chunk emission and indexing. Invalid chunks should be rejected with actionable reporting.

## Acceptance Criteria

- Ingestion validates every chunk before indexing.
- Validation failures include source URI and reason.
- Ingestion summary reports total chunks, valid chunks, and rejected chunks.
- Tests cover at least one valid and one invalid metadata payload.

## Implementation Notes

- Validation should be deterministic and suitable for CI.
- Do not attempt to repair missing provenance silently.
- Include validation results in batch ingestion reports.

## Done Evidence

- Provenance validation test output.
- Ingestion report showing validation counts.
- Example rejected chunk error.
