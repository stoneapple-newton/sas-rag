# ING-003 - Ingest Prioritized SAS 9.4 Docs Batch

Type: Feature Story
Parent: [Official SAS Docs Ingestion](../feature-official-sas-docs-ingestion.md)
Capability: Corpus ingestion and provenance
Sprint: Beta
Points: 8
Status: Proposed
Dependencies: ING-002, PARSE-002, PROV-002
Wiki: [SAS Corpus](../../docs/wiki/sas-corpus.md), [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md)

## Story

As a SAS RAG user, I want prioritized SAS 9.4 documentation indexed, so that common SAS questions can be answered from official sources.

## Detail

Scale the proven ingestion slice to the P0 SAS 9.4 source whitelist. The batch should cover macro, PROC SQL, DATA step, language concepts, and base programming references.

## Acceptance Criteria

- Prioritized P0 source families from ING-001 are ingested.
- Parse failure rate is reported and remains below the PI threshold for prioritized sources.
- Ingestion report lists loaded, skipped, failed, and unchanged sources.
- Retrieval smoke test covers macro, PROC SQL, DATA step, and language reference topics.

## Implementation Notes

- Batch execution must be repeatable.
- Avoid adding community or third-party material in PI 1.
- Persist source-level status for audit and troubleshooting.

## Done Evidence

- Batch ingestion report.
- Source coverage summary.
- Smoke retrieval transcript for representative SAS topics.
