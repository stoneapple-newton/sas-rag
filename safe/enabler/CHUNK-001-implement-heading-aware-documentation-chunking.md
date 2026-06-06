# CHUNK-001 - Implement Heading-Aware Documentation Chunking

Type: Enabler Story
Parent: [Structure-Aware Chunking](../feature-structure-aware-chunking.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 5
Status: Proposed
Dependencies: PARSE-002, PROV-002
Wiki: [Chunking Strategy](../../docs/wiki/chunking-strategy.md), [Provenance Schema](../../docs/wiki/provenance-schema.md)

## Story

As a SAS RAG user, I want documentation chunks aligned to headings, so that retrieved passages contain coherent source context.

## Detail

Use heading hierarchy as the primary split boundary for official SAS documentation, with size fallback only when sections are too large.

## Acceptance Criteria

- Chunker splits documentation on heading hierarchy before size fallback.
- Chunk size limits are configurable.
- Section path from parser output is preserved in chunk metadata.

## Implementation Notes

- Keep chunks coherent for definitions and examples.
- Preserve source headings for citations.
- Record fallback splits clearly enough for debugging.

## Done Evidence

- Chunk sample showing heading path.
- Config sample for chunk limits.
- Test covering heading split and size fallback.
