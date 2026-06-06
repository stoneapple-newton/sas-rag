# ING-003 - Ingest Prioritized SAS 9.4 Docs Batch

Type: Feature Story
Parent: [Official SAS Docs Ingestion](../feature-official-sas-docs-ingestion.md)
Capability: Corpus ingestion and provenance
Sprint: Beta
Points: 8
Status: In Progress
Dependencies: ING-002, PARSE-002, PROV-002
Wiki: [SAS Corpus](../../docs/wiki/sas-corpus.md), [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md)

## Story

As a SAS RAG user, I want prioritized SAS 9.4 documentation indexed, so that common SAS questions can be answered from official sources.

## Detail

Scale the proven ingestion slice to the P0 SAS 9.4 source whitelist. The batch should cover macro, PROC SQL, DATA step, language concepts, and base programming references, then index the emitted chunks through LangChain into persistent local Chroma.

## Acceptance Criteria

- Prioritized P0 source families from ING-001 are ingested.
- P0 chunks are converted to LangChain `Document` records and written to Chroma through `langchain-chroma`.
- Parse failure rate is reported and remains below the PI threshold for prioritized sources.
- Ingestion report lists loaded, skipped, failed, and unchanged sources.
- Retrieval smoke test covers macro, PROC SQL, DATA step, and language reference topics.

## Implementation Notes

- Batch execution must be repeatable.
- Avoid adding community or third-party material in PI 1.
- Persist source-level status for audit and troubleshooting.
- Use one configured embedding model consistently for indexing and querying.
- Store Chroma path and collection name in environment/config, defaulting to `data/chroma` and `sas_94_docs`.

## Done Evidence

- Batch ingestion report: `data/ingestion/runs/latest/report.json`.
- Source coverage summary: 22 PDFs loaded, 16,698 pages parsed, 17,135 chunks emitted, 0 failed sources.
- Chroma collection build report: `data/ingestion/runs/latest/chroma_report.json`.
- First P0 index run: 8,953 chunks indexed to `sas_94_docs`; 8,182 non-P0 chunks skipped.
- Smoke retrieval evidence exists for PROC SQL joins.
- Remaining evidence: add smoke retrieval transcripts for macro, DATA step, and language reference topics.
