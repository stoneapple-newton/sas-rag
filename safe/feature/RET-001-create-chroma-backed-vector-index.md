# RET-001 - Create Chroma-Backed Vector Index

Type: Feature Story
Parent: [Hybrid Retrieval Profile](../feature-hybrid-retrieval-profile.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 5
Status: Done
Dependencies: ING-002, PROV-002
Wiki: [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md), [Chroma Index](../../docs/wiki/chroma-index.md)

## Story

As a developer, I want a persistent local Chroma index, so that indexed SAS documentation can be queried across local runs.

## Detail

Create the local vector-store foundation for PI 1 using LangChain and persistent Chroma. The index should support repeatable local development and be configurable for tests.

## Acceptance Criteria

- Chroma collection is created from ingested chunks.
- Chroma collection is created through the `langchain-chroma` integration.
- Embedding provider is configurable through LangChain embeddings with OpenAI as the default.
- Index path and collection name are configurable for local development and tests.
- Retrieval smoke test uses the same embedding model that built the index.

## Implementation Notes

- Keep indexing code separate from MCP transport.
- Convert ingestion chunks to LangChain `Document` objects before indexing.
- Store provenance metadata alongside embedded text.
- Avoid hardcoding API keys, paths, or provider names outside config defaults.
- Prefer dedicated LangChain packages over legacy community vector-store imports: `langchain-core`, `langchain-openai`, and `langchain-chroma`.

## Done Evidence

- Index build command: `uv run python -m sas_rag.ingestion.cli index-chroma --chunks data/ingestion/runs/latest/chunks.jsonl --priority P0 --reset`.
- Chroma report: `data/ingestion/runs/latest/chroma_report.json`.
- Collection: `sas_94_docs` under `data/chroma`.
- Embedding model: `text-embedding-3-small`.
- Indexed count: 8,953 P0 chunks from 17,135 total chunks; 8,182 non-P0 chunks skipped.
- Persisted collection count check returned 8,953 records.
- Smoke query `PROC SQL join syntax` returned citation metadata from `docs/sas-documents/sqlproc.pdf`, including `chunk_id`, `title`, `source_uri`, `section_path`, and `page`.
