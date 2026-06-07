# MCP-001 - Implement Local Stdio MCP Server Shell

Type: Feature Story
Parent: [Local Stdio MCP Tools](../feature-local-stdio-mcp-tools.md)
Capability: MCP interaction layer
Sprint: Gamma
Points: 5
Status: Proposed
Dependencies: RET-002
Wiki: [MCP Server](../../docs/wiki/mcp-server.md), [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md)

## Story

As a local coding-agent user, I want a `stdio` MCP server, so that Codex can call SAS retrieval tools without remote infrastructure.

## Detail

Create the local MCP server process and dependency wiring. This story establishes server startup, configuration loading, and basic health behavior before adding individual tools.

## Acceptance Criteria

- Server starts locally over `stdio`.
- Retrieval dependencies are configured through environment variables or config files.
- Server startup fails clearly when required local index or settings are missing.

## Implementation Notes

- Keep transport logic thin.
- Retrieval and answer composition should remain behind internal services.
- PI 1 server is local-first and does not include remote HTTP transport.

## Done Evidence

- Local server startup command.
- Successful MCP client smoke connection.
- Failure example for missing required configuration.
