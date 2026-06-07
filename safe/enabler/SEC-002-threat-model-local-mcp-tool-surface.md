# SEC-002 - Threat-Model Local MCP Tool Surface

Type: Enabler Story
Parent: [Security and Secret Management](../enabler-security-secret-management.md)
Capability: Delivery and operations
Sprint: Gamma
Points: 3
Status: Ready
Dependencies: MCP-001, SCHEMA-001
Wiki: [Security Model](../../docs/wiki/security-model.md), [MCP Server](../../docs/wiki/mcp-server.md)

## Story

As a product and tech lead, I want the local MCP tool surface threat-modeled, so that coding agents cannot accidentally perform out-of-scope actions.

## Detail

Review each PI 1 MCP tool for permissions, data access, prompt-injection exposure, and accidental mutation risk.

## Acceptance Criteria

- Tool list is reviewed for permissions and data access.
- PI 1 tools are read-only by design.
- Risks and mitigations are documented for prompt injection, over-broad retrieval, and local file/index exposure.

## Implementation Notes

- Keep the analysis practical and tied to actual tool contracts.
- Explicitly defer write-capable tools outside PI 1.
- Link mitigations to tests or review checks where possible.

## Done Evidence

- Threat model note.
- Tool permission review table.
- Accepted mitigations for PI 1 release.
