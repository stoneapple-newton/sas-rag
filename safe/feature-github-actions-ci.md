# GitHub Actions CI

Type: Feature
Capability: Delivery and operations
Priority: P0
Sprint target: Alpha/Delta
Owner role: DevOps/SRE
Status: In Progress
Dependencies: None

## Intent

Add automated checks that protect the SAS RAG MCP codebase from test, contract, and retrieval-quality regressions.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| CI-001 | Feature | Add lint/unit test workflow | 3 | Alpha | DEV-001 |
| CI-002 | Feature | Add integration and eval workflow | 5 | Delta | EVAL-002, SCHEMA-002 |

## Story Details

### CI-001 - Add lint/unit test workflow

As a maintainer, I want basic CI checks, so that obvious failures are caught before merge.

Acceptance criteria:
- Workflow installs dependencies with `uv`.
- Workflow runs unit tests and any configured lint/type checks.
- Workflow documentation states required local equivalent commands.

### CI-002 - Add integration and eval workflow

As a release owner, I want integration and eval checks in CI, so that MCP and retrieval regressions are visible before release.

Acceptance criteria:
- Workflow runs MCP contract tests once tools exist.
- Workflow runs the eval smoke suite or documented subset.
- Eval output is published in logs or artifacts for review.

## Definition of Done

- CI workflows are documented.
- Local commands match CI behavior where practical.
- Eval checks do not require remote MCP deployment.

Current status:
- CI-001 is Done with local equivalents `uv run ruff check` and `uv run pytest -q`.
- CI-002 remains Delta scope for integration and eval workflow expansion.
