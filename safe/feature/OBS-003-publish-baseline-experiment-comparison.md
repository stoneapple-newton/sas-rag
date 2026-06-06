# OBS-003 - Publish Baseline Experiment Comparison

Type: Feature Story
Parent: [LangSmith Observability](../feature-langsmith-observability.md)
Capability: Delivery and operations
Sprint: Delta
Points: 3
Status: Proposed
Dependencies: OBS-002, EVAL-002
Wiki: [Observability and Evals](../../docs/wiki/observability-and-evals.md), [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md)

## Story

As a release owner, I want a baseline experiment comparison, so that Delta release decisions include measured retrieval and citation quality.

## Detail

Publish the PI baseline comparison for retrieval and citation metrics using the benchmark dataset and the configured tracing/evaluation flow.

## Acceptance Criteria

- Baseline experiment is identified.
- Current eval results are compared against baseline.
- Regression summary is linked or included in release readiness notes.

## Implementation Notes

- Keep the baseline stable once chosen for Delta.
- Include any metric gaps or known limitations.
- Use this result in the final PI system demo.

## Done Evidence

- Baseline comparison report.
- Release readiness note.
- Link or reference to experiment run.
