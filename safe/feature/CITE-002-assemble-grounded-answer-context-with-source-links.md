# CITE-002 - Assemble Grounded Answer Context with Source Links

Type: Feature Story
Parent: [Citation Assembler](../feature-citation-assembler.md)
Capability: Retrieval and grounding
Sprint: Gamma
Points: 5
Status: Ready
Dependencies: CITE-001, RET-002
Wiki: [Citation Grounding](../../docs/wiki/citation-grounding.md), [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md)

## Story

As a coding agent, I want answer context assembled with source links, so that generated explanations stay tied to retrieved SAS evidence.

## Detail

Build the answer context packet from retrieved chunks and citations. The composer should receive evidence, metadata, and citation references in a predictable structure.

## Acceptance Criteria

- Answer composer receives only retrieved evidence and citation metadata needed for the response.
- Final answer includes citations for supported claims.
- Citation format is consistent across MCP tools.

## Implementation Notes

- Keep answer composition separate from low-level retrieval.
- Prefer concise evidence windows over dumping every retrieved token.
- Preserve source links and section paths in final responses.

## Done Evidence

- Example grounded answer with citations.
- Test covering multi-source citation assembly.
- Trace showing retrieved evidence used in answer context.
