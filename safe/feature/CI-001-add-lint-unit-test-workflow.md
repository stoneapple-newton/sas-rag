# CI-001 - Add Lint/Unit Test Workflow

Type: Feature Story
Parent: [GitHub Actions CI](../feature-github-actions-ci.md)
Capability: Delivery and operations
Sprint: Alpha
Points: 3
Status: Done
Dependencies: DEV-001
Wiki: [CI Quality Gates](../../docs/wiki/ci-quality-gates.md), [Developer Environment](../../docs/wiki/developer-environment.md)

## Story

As a maintainer, I want basic CI checks, so that obvious failures are caught before merge.

## Detail

Add the first CI workflow for dependency installation and local checks. The workflow should mirror documented developer commands where practical.

## Acceptance Criteria

- Workflow installs dependencies with `uv`.
- Workflow runs unit tests and any configured lint/type checks.
- Workflow documentation states required local equivalent commands.

## Implementation Notes

- Keep workflow minimal until implementation code exists.
- Do not add remote deployment or secrets to Alpha CI.
- Make failures easy to reproduce locally.

## Done Evidence

- CI workflow file: `.github/workflows/ci.yml`.
- Runs `uv sync`, `uv run ruff check .`, and `uv run pytest` on push/PR to `main`.
- `pyproject.toml` includes `ruff` and `pytest` in `[dependency-groups] dev`.
