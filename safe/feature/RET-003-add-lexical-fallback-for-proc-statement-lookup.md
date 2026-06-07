# RET-003 - Add Lexical Fallback for PROC/Statement Lookup

Type: Feature Story
Parent: [Hybrid Retrieval Profile](../feature-hybrid-retrieval-profile.md)
Capability: Retrieval and grounding
Sprint: Gamma
Points: 5
Status: Ready
Dependencies: RET-002, EVAL-001
Wiki: [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md), [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md)

## Story

As a SAS user, I want exact PROC and statement terms handled reliably, so that symbol-like queries are not missed by semantic retrieval alone.

## Detail

Add a lexical retrieval path or fallback for SAS identifiers such as procedure names, statements, options, and macro keywords.

## Acceptance Criteria

- Retrieval can prioritize exact or lexical matches for PROC and statement names.
- Fallback behavior is visible in trace or result metadata.
- Benchmark includes examples where lexical fallback improves retrieval.

## Implementation Notes

- Do not replace semantic retrieval; combine or fallback based on query shape.
- Include PROC SQL and DATA step statement cases.
- Use benchmark results to confirm value before expanding complexity.

## Done Evidence

- Before/after benchmark examples.
- Search result payload marking lexical contribution.
- Trace or log showing fallback activation.
