# CHUNK-002 - Implement SAS-Aware Code Boundary Detection

Type: Enabler Story
Parent: [Structure-Aware Chunking](../feature-structure-aware-chunking.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 8
Status: Proposed
Dependencies: PARSE-002
Wiki: [Chunking Strategy](../../docs/wiki/chunking-strategy.md), [SAS Corpus](../../docs/wiki/sas-corpus.md)

## Story

As a coding agent, I want SAS examples chunked by SAS-native boundaries, so that explanations do not mix unrelated procedures, DATA steps, or macros.

## Detail

Detect SAS code boundaries in official documentation examples. Boundaries should preserve meaningful SAS blocks and nearby comments.

## Acceptance Criteria

- Boundary detection recognizes `PROC ... RUN;`, `PROC ... QUIT;`, `DATA ... RUN;`, and `%MACRO ... %MEND;`.
- Nearby comments stay with the code block they explain.
- Unit cases cover PROC, DATA step, macro, and mixed prose/code examples.

## Implementation Notes

- Treat this as code/example chunking, not full SAS parsing.
- Keep behavior conservative when syntax is incomplete.
- Preserve comments that explain the code block.

## Done Evidence

- Unit tests for PROC, DATA step, macro, and mixed examples.
- Manual inspection notes for representative chunks.
- Retrieval smoke query against a SAS example.
