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
Preserve syntax blocks, tables, examples, and nearby explanatory prose before applying token-size fallback.
Create parent chunks by logical page or major section and child chunks by SAS documentation section type.

## Acceptance Criteria

- Chunker splits documentation on heading hierarchy before size fallback.
- Chunk size limits are configurable.
- Section path from parser output is preserved in chunk metadata.
- Oversized sections are split deterministically without separating examples from their explanatory context.
- Config supports defaults for syntax/reference, concept docs, white papers, code examples, local SAS code, and option tables.

## Implementation Notes

- Keep chunks coherent for definitions and examples.
- Preserve source headings for citations.
- Record fallback splits clearly enough for debugging.
- Emit `concept`, `syntax`, `argument`, `option_table`, `example`, `troubleshooting`, or `migration` chunk types when the heading context makes the type clear.
- Use approximate defaults: 250-600 tokens for syntax/reference children, 500-900 for concept children, 700-1,200 for white-paper children, and no arbitrary split for complete examples.

## Done Evidence

- Chunk sample showing heading path.
- Config sample for chunk limits.
- Test covering heading split and size fallback.
