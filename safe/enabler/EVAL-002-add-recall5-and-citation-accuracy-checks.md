# EVAL-002 - Add Recall@5 and Citation Accuracy Checks

Type: Enabler Story
Parent: [Benchmark Dataset](../enabler-benchmark-dataset.md)
Capability: Retrieval and grounding
Sprint: Gamma
Points: 5
Status: Proposed
Dependencies: EVAL-001, RET-002, CITE-001
Wiki: [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md), [Observability and Evals](../../docs/wiki/observability-and-evals.md)

## Story

As a QA engineer, I want automated retrieval and citation checks, so that quality can be compared across chunking, embedding, and prompt changes.

## Detail

Implement the first metric suite for PI 1: recall@5 for labeled retrieval and citation accuracy or support pass rate for grounded outputs.

## Acceptance Criteria

- Eval reports recall@5 for labeled questions.
- Eval reports citation accuracy or citation-support pass rate.
- Eval output is usable in CI and LangSmith experiment review.

## Implementation Notes

- Keep metrics deterministic where possible.
- Separate retrieval-only and answer/citation evaluation.
- Make output readable in local terminal and CI logs.

## Done Evidence

- Eval command output.
- Example metric report.
- LangSmith experiment or local comparison record.
