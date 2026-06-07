# Observability and Evals

LangSmith tracing and benchmark evaluation should make retrieval quality visible across the PI.

Related stories:
- [OBS-001](../../safe/feature/OBS-001-configure-langsmith-tracing.md)
- [OBS-002](../../safe/feature/OBS-002-trace-ingestion-retrieval-and-mcp-calls.md)
- [OBS-003](../../safe/feature/OBS-003-publish-baseline-experiment-comparison.md)

Notes:
- Tracing must be optional and config-driven.
- Do not log secrets or unrelated user file contents.
- LangSmith tracing implementation is Sprint Gamma work in OBS-002.
- Current logging is structured JSON via `sas_rag.logging_config.JSONFormatter`.
- MCP and retrieval calls log start/end and result counts; secrets are not intentionally logged.
- Current local quality gate is `uv run ruff check` plus `uv run pytest -q`.
- Benchmark dataset v1 exists at `data/benchmark/sas_questions.json`; automated recall@5/citation checks are EVAL-002.
