# OBS-002 - Trace Ingestion, Retrieval, and MCP Calls

Type: Feature Story
Parent: [LangSmith Observability](../feature-langsmith-observability.md)
Capability: Delivery and operations
Sprint: Gamma
Points: 5
Status: Proposed
Dependencies: OBS-001, MCP-001, RET-002
Wiki: [Observability and Evals](../../docs/wiki/observability-and-evals.md), [MCP Server](../../docs/wiki/mcp-server.md)

## Story

As a debugging engineer, I want traces across core workflows, so that failures can be diagnosed from source load through MCP response.

## Detail

Add trace metadata at ingestion, retrieval, and MCP boundaries while avoiding sensitive values.

## Acceptance Criteria

- Retrieval calls include query, selected retriever profile, result count, and citation metadata in trace context where appropriate.
- MCP tool calls are traceable without logging secrets.
- Trace IDs or run links are available in local debug output when configured.

## Implementation Notes

- Avoid logging API keys, local secrets, or unrelated user file contents.
- Trace identifiers should help connect tool calls to retrieval calls.
- Keep observability optional and config-driven.

## Done Evidence

- Trace sample covering MCP to retrieval.
- Redaction or no-secret review.
- Debug output showing trace ID or run link.
