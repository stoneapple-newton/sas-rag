# Observability and Evals

LangSmith tracing and benchmark evaluation should make retrieval quality visible across the PI.

Related stories:
- [OBS-001](../../safe/feature/OBS-001-configure-langsmith-tracing.md)
- [OBS-002](../../safe/feature/OBS-002-trace-ingestion-retrieval-and-mcp-calls.md)
- [OBS-003](../../safe/feature/OBS-003-publish-baseline-experiment-comparison.md)

Notes:
- Tracing must be optional and config-driven.
- Do not log secrets or unrelated user file contents.
- LangSmith tracing implementation is deferred to Sprint Gamma (OBS-002).
