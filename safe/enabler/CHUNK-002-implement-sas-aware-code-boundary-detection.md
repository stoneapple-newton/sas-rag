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
Primary chunks should stay semantic and complete; secondary lexical chunks can be added later for oversized examples.
Setup statements should be retained as dependency metadata rather than treated as unrelated snippets.

## Acceptance Criteria

- Boundary detection recognizes `PROC ... RUN;`, `PROC ... QUIT;`, `DATA ... RUN;`, and `%MACRO ... %MEND;`.
- Boundary detection recognizes obvious DS2 package, method, and class bodies.
- `LIBNAME`, `FILENAME`, `OPTIONS`, and `ODS` setup statements attach to the following executable chunk when context indicates dependency.
- Nearby comments stay with the code block they explain.
- Unit cases cover PROC, DATA step, macro, and mixed prose/code examples.

## Implementation Notes

- Treat this as code/example chunking, not full SAS parsing.
- Keep behavior conservative when syntax is incomplete.
- Preserve comments that explain the code block.
- Emit specific chunk types for `proc`, `data_step`, `macro`, `ds2`, and `example`.
- Keep reference, concept/tutorial, and code/example retrieval separable for exact syntax, explanation, and example-biased search.
- Preserve full parent blocks for long PROC or DATA steps while allowing secondary statement-group chunks if needed.

## Done Evidence

- Unit tests for PROC, DATA step, macro, and mixed examples.
- Manual inspection notes for representative chunks.
- Retrieval smoke query against a SAS example.
