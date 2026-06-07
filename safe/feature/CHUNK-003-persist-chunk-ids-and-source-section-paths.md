# CHUNK-003 - Persist Chunk IDs and Source Section Paths

Type: Feature Story
Parent: [Structure-Aware Chunking](../feature-structure-aware-chunking.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 3
Status: Done
Dependencies: CHUNK-001, PROV-001
Wiki: [Chunking Strategy](../../docs/wiki/chunking-strategy.md), [Provenance Schema](../../docs/wiki/provenance-schema.md)

## Story

As a retrieval engineer, I want stable chunk IDs and section paths, so that citations and benchmark labels survive repeated indexing.

## Detail

Persist chunk identity and section hierarchy through the vector-store metadata layer. The same unchanged source section should produce the same logical chunk ID across reruns.
Chunk identity should also account for chunk type so prose/reference chunks and code/example chunks can coexist without collision.
Chunk metadata should support parent-child retrieval and atomic SAS reference-object lookup.

## Acceptance Criteria

- Chunk IDs remain stable for unchanged source content and section context.
- Section paths are stored in vector metadata.
- Chunk type, product/version fields, and source priority are stored in vector metadata.
- Section type, SAS object type/name, keywords, valid context, parent chunk ID, and index category are stored when available.
- Re-indexing the same source does not create duplicate logical chunks.

## Implementation Notes

- Chunk IDs should be derived from stable source and content inputs.
- Section paths should preserve enough heading context for citations.
- Coordinate with benchmark labels that reference expected chunks.
- Include chunk type in benchmark labels where the same source section emits both prose and example chunks.
- Reference-object chunk IDs should derive from stable source, SAS object type/name, version, and section path.

## Done Evidence

- Rerun comparison showing stable IDs.
- Chroma metadata sample.
- Retrieval result showing section path.
