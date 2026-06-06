# CITE-001 - Return Citations from Retrieved Chunks

Type: Feature Story
Parent: [Citation Assembler](../feature-citation-assembler.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 5
Status: Proposed
Dependencies: RET-001, PROV-002
Wiki: [Citation Grounding](../../docs/wiki/citation-grounding.md), [Provenance Schema](../../docs/wiki/provenance-schema.md)

## Story

As a SAS RAG user, I want search results to include citations, so that I can verify the official source behind each answer.

## Detail

Transform retrieved chunk metadata into a consistent citation structure that MCP tools and answer composition can reuse.

## Acceptance Criteria

- Retrieval results include source title, source URI, version, section path, and chunk ID.
- Citation fields are generated from provenance rather than prompt-only text.
- Missing citation metadata fails validation before answer assembly.

## Implementation Notes

- Keep citation formatting deterministic.
- Include chunk ID for machine use and source title/section for human use.
- Coordinate with unsupported-answer behavior.

## Done Evidence

- Search result with citation object.
- Test covering missing citation metadata.
- Example citation format documented.
