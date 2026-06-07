# RET-002 - Add Semantic Search with Metadata Filters

Type: Feature Story
Parent: [Hybrid Retrieval Profile](../feature-hybrid-retrieval-profile.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 5
Status: Done
Dependencies: RET-001
Wiki: [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md), [Provenance Schema](../../docs/wiki/provenance-schema.md)

## Story

As a coding agent, I want semantic search with filters, so that queries can be narrowed by source family, version, section, or source type.

## Detail

Expose a retrieval service API that accepts a natural-language query, top-k, and optional metadata filters. Return ranked chunks with citation-ready metadata.

## Acceptance Criteria

- Search supports top-k semantic retrieval.
- Search accepts metadata filters for required provenance fields where applicable.
- Results include text, score, chunk ID, title, source URI, version, and section path.

## Implementation Notes

- Keep result shape stable because MCP tools will depend on it.
- Include empty-result behavior.
- Trace query, filters, result count, and retriever profile when observability is enabled.

## Done Evidence

- Search test with and without metadata filter.
- Example result payload.
- Retrieval smoke output for SAS 9.4 content.
