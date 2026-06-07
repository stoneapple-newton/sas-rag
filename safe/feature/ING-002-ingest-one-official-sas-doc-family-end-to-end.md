# ING-002 - Ingest One Official SAS Doc Family End to End

Type: Feature Story
Parent: [Official SAS Docs Ingestion](../feature-official-sas-docs-ingestion.md)
Capability: Corpus ingestion and provenance
Sprint: Alpha
Points: 5
Status: Proposed
Dependencies: ING-001, PARSE-001, PROV-001
Wiki: [SAS Corpus](../../docs/wiki/sas-corpus.md), [Ingestion Pipeline](../../docs/wiki/ingestion-pipeline.md), [Provenance Schema](../../docs/wiki/provenance-schema.md)

## Story

As a data engineer, I want one official SAS documentation family to ingest end to end, so that the pipeline proves source loading, parsing, chunking, embedding, and persistence before scaling out.

## Detail

Use a single whitelisted SAS 9.4 documentation family as the vertical slice. The story should prove the full path from source inventory through parser adapter, normalized document units, chunk emission, provenance validation, LangChain `Document` conversion, OpenAI embeddings, and local Chroma persistence.

## Acceptance Criteria

- One whitelisted SAS 9.4 doc family is loaded from local or configured source input.
- Pipeline emits chunks with required provenance metadata and stable chunk IDs.
- Chunks are converted to LangChain `Document` objects with provenance in metadata.
- Chunks are embedded through configurable LangChain embeddings, using OpenAI as the default.
- Chunks are written through `langchain-chroma` to the local Chroma index without duplicate records on rerun.
- A demo query retrieves content from the ingested source.

## Implementation Notes

- Prefer a small, high-authority source family that supports several benchmark questions.
- Keep provider and storage paths config-driven.
- Capture ingestion counts for loaded, skipped, failed, and indexed chunks.
- Use dedicated LangChain integration packages: `langchain-openai` for embeddings and `langchain-chroma` for Chroma persistence.
- Keep parsing/chunking independent from LangChain so extraction artifacts remain testable before embedding.

## Done Evidence

- Ingestion command output or report.
- Sample indexed chunk with provenance.
- LangChain `Document` sample showing page content and metadata.
- Retrieval smoke query result with citation metadata.
