# OBS-001 - Configure LangSmith Tracing

Type: Feature Story
Parent: [LangSmith Observability](../feature-langsmith-observability.md)
Capability: Delivery and operations
Sprint: Alpha
Points: 3
Status: Done
Dependencies: None
Wiki: [Observability and Evals](../../docs/wiki/observability-and-evals.md)

## Story

As a project lead, I want LangSmith configured early, so that retrieval experiments and demos have trace evidence from the start.

## Detail

Document and wire optional LangSmith tracing for local workflows without making it mandatory for basic development.

## Acceptance Criteria

- Required environment variables and setup steps are documented.
- Local runs can enable or disable tracing by configuration.
- A smoke trace is visible from a local retrieval or placeholder workflow.

## Implementation Notes

- Do not hardcode API keys.
- Ensure tracing can be disabled for offline development.
- Keep trace naming consistent with ingestion, retrieval, and MCP workflows.

## Done Evidence

- LangSmith tracing deferred to Sprint Gamma (OBS-002) per team decision.
- Configuration variables documented in `example.env`: `LANGSMITH_API_KEY`, `LANGSMITH_TRACING`, `LANGSMITH_PROJECT`.
- `docs/wiki/observability-and-evals.md` notes the deferral and current config-only approach.
