# LangSmith Observability

Type: Feature
Capability: Delivery and operations
Priority: P0
Sprint target: Alpha/Gamma/Delta
Owner role: ML/RAG Engineer
Status: In Progress
Dependencies: None

## Intent

Trace ingestion, retrieval, and MCP behavior so experiments and regressions are visible throughout the PI.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| OBS-001 | Feature | Configure LangSmith tracing | 3 | Alpha | None |
| OBS-002 | Feature | Trace ingestion, retrieval, and MCP calls | 5 | Gamma | OBS-001, MCP-001, RET-002 |
| OBS-003 | Feature | Publish baseline experiment comparison | 3 | Delta | OBS-002, EVAL-002 |

## Story Details

### OBS-001 - Configure LangSmith tracing

As a project lead, I want LangSmith configured early, so that retrieval experiments and demos have trace evidence from the start.

Acceptance criteria:
- Required environment variables and setup steps are documented.
- Local runs can enable or disable tracing by configuration.
- A smoke trace is visible from a local retrieval or placeholder workflow.

### OBS-002 - Trace ingestion, retrieval, and MCP calls

As a debugging engineer, I want traces across core workflows, so that failures can be diagnosed from source load through MCP response.

Acceptance criteria:
- Retrieval calls include query, selected retriever profile, result count, and citation metadata in trace context where appropriate.
- MCP tool calls are traceable without logging secrets.
- Trace IDs or run links are available in local debug output when configured.

### OBS-003 - Publish baseline experiment comparison

As a release owner, I want a baseline experiment comparison, so that Delta release decisions include measured retrieval and citation quality.

Acceptance criteria:
- Baseline experiment is identified.
- Current eval results are compared against baseline.
- Regression summary is linked or included in release readiness notes.

## Definition of Done

- Tracing setup is documented.
- Sensitive values are not logged.
- Evaluation results can be compared to baseline.

Current status:
- OBS-001 is Done as config/documentation.
- OBS-002 is Ready for Gamma.
- Current MCP/retrieval logging is structured JSON and avoids stdout for stdio safety.
