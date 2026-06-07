# SCHEMA-001 - Define Versioned MCP Tool Schemas

Type: Enabler Story
Parent: [Tool Schema Versioning](../enabler-tool-schema-versioning.md)
Capability: MCP interaction layer
Sprint: Gamma
Points: 3
Status: In Progress
Dependencies: MCP-001
Wiki: [Tool Contracts](../../docs/wiki/tool-contracts.md), [MCP Server](../../docs/wiki/mcp-server.md)

## Story

As a backend engineer, I want versioned MCP tool schemas, so that tool contracts can evolve without surprising clients.

## Detail

Document the PI 1 MCP tool request and response contracts, including schema version and standard error shapes.

## Acceptance Criteria

- Each PI 1 MCP tool has documented input and output fields.
- Schema version is visible in docs or tool metadata.
- Error shapes are consistent for validation, not-found, and insufficient-evidence cases.

## Implementation Notes

- Keep schemas small and stable.
- Align tool output with retrieval and citation result shapes.
- Record compatibility notes in the wiki.

## Done Evidence

- Initial `search_sas_docs` schema implemented with `schema_version: "1.0"`.
- Standard error shape implemented for validation, configuration, insufficient-evidence, not-found, and internal errors.
- Remaining Gamma tool schemas still need to be added as MCP-003 and MCP-004 land.
