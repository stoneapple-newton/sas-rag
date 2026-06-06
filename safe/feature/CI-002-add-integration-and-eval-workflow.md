# CI-002 - Add Integration and Eval Workflow

Type: Feature Story
Parent: [GitHub Actions CI](../feature-github-actions-ci.md)
Capability: Delivery and operations
Sprint: Delta
Points: 5
Status: Proposed
Dependencies: EVAL-002, SCHEMA-002
Wiki: [CI Quality Gates](../../docs/wiki/ci-quality-gates.md), [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md)

## Story

As a release owner, I want integration and eval checks in CI, so that MCP and retrieval regressions are visible before release.

## Detail

Extend CI to run MCP contract tests and the evaluation smoke suite once those pieces exist.

## Acceptance Criteria

- Workflow runs MCP contract tests once tools exist.
- Workflow runs the eval smoke suite or documented subset.
- Eval output is published in logs or artifacts for review.

## Implementation Notes

- Avoid requiring remote HTTP deployment.
- Keep secrets optional or use protected CI configuration.
- Make eval runtime acceptable for PR use.

## Done Evidence

- CI integration/eval workflow.
- Sample eval output artifact or log.
- Release readiness note using CI results.
