# RET-001 - Create Chroma-Backed Vector Index

Type: Feature Story
Parent: [Hybrid Retrieval Profile](../feature-hybrid-retrieval-profile.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 5
Status: Proposed
Dependencies: ING-002, PROV-002
Wiki: [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md), [Chroma Index](../../docs/wiki/chroma-index.md)

## Story

As a developer, I want a persistent local Chroma index, so that indexed SAS documentation can be queried across local runs.

## Detail

Create the local vector-store foundation for PI 1. The index should support repeatable local development and be configurable for tests.

## Acceptance Criteria

- Chroma collection is created from ingested chunks.
- Embedding provider is configurable with OpenAI as the default.
- Index path and collection name are configurable for local development and tests.

## Implementation Notes

- Keep indexing code separate from MCP transport.
- Store provenance metadata alongside embedded text.
- Avoid hardcoding API keys, paths, or provider names outside config defaults.

## Done Evidence

- Index build command output.
- Chroma collection metadata sample.
- Local query proving persisted index reuse.
