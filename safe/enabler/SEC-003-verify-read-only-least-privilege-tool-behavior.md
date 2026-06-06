# SEC-003 - Verify Read-Only Least-Privilege Tool Behavior

Type: Enabler Story
Parent: [Security and Secret Management](../enabler-security-secret-management.md)
Capability: Delivery and operations
Sprint: Delta
Points: 3
Status: Proposed
Dependencies: MCP-002, MCP-003, MCP-004
Wiki: [Security Model](../../docs/wiki/security-model.md), [Tool Contracts](../../docs/wiki/tool-contracts.md)

## Story

As a release owner, I want read-only MCP behavior verified, so that the release target is safe for local agent use.

## Detail

Confirm the implemented PI 1 MCP tools do not mutate files, indexes, or external systems. Capture the verification as part of release readiness.

## Acceptance Criteria

- MCP tools do not write user project files or mutate external services.
- Tests or review checklist verify read-only behavior.
- Any future write-capable tool is explicitly deferred outside PI 1.

## Implementation Notes

- Review code paths for tool handlers and dependencies.
- Include local index writes only in ingestion workflows, not MCP query tools.
- Make exceptions explicit if discovered.

## Done Evidence

- Read-only verification checklist.
- Test or review result.
- Release note confirming no write-capable MCP tools.
