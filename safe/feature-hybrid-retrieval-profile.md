# Hybrid Retrieval Profile

Type: Feature
Capability: Retrieval and grounding
Priority: P0
Sprint target: Beta/Gamma
Owner role: ML/RAG Engineer
Status: Proposed
Dependencies: ING-002, CHUNK-001, PROV-002

## Intent

Provide a retrieval layer that combines semantic search with metadata filters and lexical lookup for precise SAS procedure, statement, and concept queries.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| RET-001 | Feature | Create Chroma-backed vector index | 5 | Beta | ING-002, PROV-002 |
| RET-002 | Feature | Add semantic search with metadata filters | 5 | Beta | RET-001 |
| RET-003 | Feature | Add lexical fallback for PROC/statement lookup | 5 | Gamma | RET-002, EVAL-001 |

## Story Details

### RET-001 - Create Chroma-backed vector index

As a developer, I want a persistent local Chroma index, so that indexed SAS documentation can be queried across local runs.

Acceptance criteria:
- Chroma collection is created from ingested chunks.
- Embedding provider is configurable with OpenAI as the default.
- Index path and collection name are configurable for local development and tests.

### RET-002 - Add semantic search with metadata filters

As a coding agent, I want semantic search with filters, so that queries can be narrowed by source family, version, section, or source type.

Acceptance criteria:
- Search supports top-k semantic retrieval.
- Search accepts metadata filters for required provenance fields where applicable.
- Results include text, score, chunk ID, title, source URI, version, and section path.

### RET-003 - Add lexical fallback for PROC/statement lookup

As a SAS user, I want exact PROC and statement terms handled reliably, so that symbol-like queries are not missed by semantic retrieval alone.

Acceptance criteria:
- Retrieval can prioritize exact or lexical matches for PROC and statement names.
- Fallback behavior is visible in trace or result metadata.
- Benchmark includes examples where lexical fallback improves retrieval.

## Definition of Done

- Retrieval service can query indexed SAS 9.4 chunks locally.
- Search results expose provenance required by citation stories.
- Recall metrics are captured against the benchmark when available.
