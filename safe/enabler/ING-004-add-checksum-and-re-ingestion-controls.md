# ING-004 - Add Checksum and Re-Ingestion Controls

Type: Enabler Story
Parent: [Official SAS Docs Ingestion](../feature-official-sas-docs-ingestion.md)
Capability: Corpus ingestion and provenance
Sprint: Beta
Points: 5
Status: Proposed
Dependencies: ING-002, PROV-002
Wiki: [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md), [Provenance Schema](../../docs/wiki/provenance-schema.md)

## Story

As a data engineer, I want checksum-based re-ingestion controls, so that unchanged sources are not repeatedly duplicated or needlessly reprocessed.

## Detail

Add source and chunk hashing so ingestion can detect unchanged, changed, and new sources. This protects local Chroma indexes from duplicate logical chunks.

## Acceptance Criteria

- Source checksum or content hash is captured during ingestion.
- Unchanged source reruns are detected and reported.
- Changed sources can be reprocessed while preserving traceability to prior chunk versions.
- Duplicate chunk creation is prevented in local persisted Chroma runs.

## Implementation Notes

- Use deterministic hash inputs.
- Report unchanged sources separately from skipped or failed sources.
- Coordinate hash fields with the provenance schema.

## Done Evidence

- Rerun report showing unchanged source detection.
- Duplicate-prevention test or smoke result.
- Example changed-source processing note.
