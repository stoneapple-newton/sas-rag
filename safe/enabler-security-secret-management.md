# Security and Secret Management

Type: Enabler
Capability: Delivery and operations
Priority: P0
Sprint target: Alpha/Gamma/Delta
Owner role: DevOps/SRE
Status: Proposed
Dependencies: None

## Intent

Keep the PI 1 MCP surface read-only, least-privilege, and safe for local coding-agent workflows while avoiding accidental secret exposure.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| SEC-001 | Enabler | Document secret handling and env var policy | 3 | Alpha | None |
| SEC-002 | Enabler | Threat-model local MCP tool surface | 3 | Gamma | MCP-001, SCHEMA-001 |
| SEC-003 | Enabler | Verify read-only least-privilege tool behavior | 3 | Delta | MCP-002, MCP-003, MCP-004 |

## Story Details

### SEC-001 - Document secret handling and env var policy

As a maintainer, I want clear secret handling rules, so that model keys and tracing keys are not committed or logged.

Acceptance criteria:
- Required environment variables are documented without real values.
- `.env` or local secret files are excluded from source control where applicable.
- Logs and traces must not include raw API keys or credentials.

### SEC-002 - Threat-model local MCP tool surface

As a product and tech lead, I want the local MCP tool surface threat-modeled, so that coding agents cannot accidentally perform out-of-scope actions.

Acceptance criteria:
- Tool list is reviewed for permissions and data access.
- PI 1 tools are read-only by design.
- Risks and mitigations are documented for prompt injection, over-broad retrieval, and local file/index exposure.

### SEC-003 - Verify read-only least-privilege tool behavior

As a release owner, I want read-only MCP behavior verified, so that the release target is safe for local agent use.

Acceptance criteria:
- MCP tools do not write user project files or mutate external services.
- Tests or review checklist verify read-only behavior.
- Any future write-capable tool is explicitly deferred outside PI 1.

## Definition of Done

- Secret policy is documented.
- MCP tool surface has a threat model.
- PI 1 release has no write-capable MCP tools.
