# Tool Schema Versioning

Type: Enabler
Capability: MCP interaction layer
Priority: P1
Sprint target: Gamma
Owner role: Backend Engineer
Status: In Progress
Dependencies: MCP-001

## Intent

Keep MCP tool inputs and outputs stable enough for coding agents, tests, and future clients to rely on.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| SCHEMA-001 | Enabler | Define versioned MCP tool schemas | 3 | Gamma | MCP-001 |
| SCHEMA-002 | Enabler | Add MCP contract tests | 5 | Gamma | SCHEMA-001, MCP-002 |

## Story Details

### SCHEMA-001 - Define versioned MCP tool schemas

As a backend engineer, I want versioned MCP tool schemas, so that tool contracts can evolve without surprising clients.

Acceptance criteria:
- Each PI 1 MCP tool has documented input and output fields.
- Schema version is visible in docs or tool metadata.
- Error shapes are consistent for validation, not-found, and insufficient-evidence cases.

### SCHEMA-002 - Add MCP contract tests

As a QA engineer, I want contract tests for MCP tools, so that schema regressions are caught before release.

Acceptance criteria:
- Contract tests cover successful and error responses for core tools.
- Tests can run locally without remote HTTP deployment.
- CI can execute contract tests after MCP implementation exists.

## Definition of Done

- Tool schemas are documented.
- Contract tests protect the published schema.
- Schema changes require intentional test updates.

## Current Evidence

- `search_sas_docs` uses schema version `1.0`.
- Contract tests cover successful and validation-error responses for `search_sas_docs`.
- Remaining Gamma tools still need schemas and tests as they are implemented.
