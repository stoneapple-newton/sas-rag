# CI Quality Gates

CI should protect unit tests, MCP contracts, and retrieval evaluation smoke checks.

Related stories:
- [CI-001](../../safe/feature/CI-001-add-lint-unit-test-workflow.md)
- [CI-002](../../safe/feature/CI-002-add-integration-and-eval-workflow.md)
- [EVAL-003](../../safe/enabler/EVAL-003-add-regression-threshold-report.md)

Notes:
- Keep checks locally reproducible where practical.
- Avoid remote deployment requirements for PI 1 CI.
- Current local gate: `uv run ruff check` and `uv run pytest -q`.
- MCP contract tests live in `tests/test_mcp_contracts.py`.
- Contract tests use fake embeddings and temporary Chroma collections so they do not require OpenAI.
- Live MCP smoke remains manual for now because it uses the local OpenAI-backed index.
