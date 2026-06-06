# EVAL-003 - Add Regression Threshold Report

Type: Enabler Story
Parent: [Benchmark Dataset](../enabler-benchmark-dataset.md)
Capability: Retrieval and grounding
Sprint: Delta
Points: 3
Status: Proposed
Dependencies: EVAL-002, OBS-002
Wiki: [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md), [CI Quality Gates](../../docs/wiki/ci-quality-gates.md)

## Story

As a release owner, I want regression thresholds reported, so that quality drops are visible before release.

## Detail

Compare current evaluation results to the accepted baseline and report regressions clearly for release readiness.

## Acceptance Criteria

- Report compares current results to the chosen baseline.
- Report flags core metric drops above the agreed PI threshold.
- Delta sprint release candidate includes the report as demo evidence.

## Implementation Notes

- Default threshold follows the overall plan unless changed in release governance.
- Include both improved and regressed metrics.
- Keep report format stable for CI artifacts.

## Done Evidence

- Regression report sample.
- Baseline comparison reference.
- Delta release candidate note.
