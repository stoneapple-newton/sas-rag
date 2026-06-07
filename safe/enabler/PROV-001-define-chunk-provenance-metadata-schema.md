# PROV-001 - Define Chunk Provenance Metadata Schema

Type: Enabler Story
Parent: [Provenance Schema](../feature-provenance-schema.md)
Capability: Corpus ingestion and provenance
Sprint: Alpha
Points: 3
Status: Proposed
Dependencies: ING-001
Wiki: [Provenance Schema](../../docs/wiki/provenance-schema.md), [Citation Grounding](../../docs/wiki/citation-grounding.md)

## Story

As a retrieval engineer, I want a required provenance schema, so that every chunk carries enough evidence for citation, filtering, and debugging.

## Detail

Define the metadata contract for every indexed chunk. This schema is the bridge between ingestion, retrieval filters, citations, benchmark labels, and MCP tool outputs.

## Acceptance Criteria

- Required fields include `chunk_id`, `source_uri`, `title`, `version`, `section_path`, `source_type`, and content hash.
- Optional fields for page, heading level, product area, and source family are documented.
- Schema is documented in human-readable Markdown and is suitable for validation in tests.

## Implementation Notes

- Keep required fields minimal but sufficient.
- Prefer names that map cleanly to Chroma metadata and MCP outputs.
- Use wiki notes for examples and future schema changes.

## Done Evidence

- Published schema note.
- Example metadata payload.
- Review with ingestion and citation stories.
