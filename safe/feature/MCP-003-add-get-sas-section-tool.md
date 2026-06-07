# MCP-003 - Add `get_sas_section` Tool

Type: Feature Story
Parent: [Local Stdio MCP Tools](../feature-local-stdio-mcp-tools.md)
Capability: MCP interaction layer
Sprint: Gamma
Points: 5
Status: Ready
Dependencies: MCP-001, PROV-002
Wiki: [MCP Server](../../docs/wiki/mcp-server.md), [Tool Contracts](../../docs/wiki/tool-contracts.md)

## Story

As a coding agent, I want to fetch a known SAS section or chunk, so that I can inspect source context after search.

## Detail

Expose direct source lookup for a chunk ID or section reference returned by search. This makes citations explorable by coding agents.

## Acceptance Criteria

- Tool accepts chunk ID or section reference supported by the index.
- Tool returns source text and provenance metadata.
- Tool returns a clear not-found response for unknown IDs.

## Implementation Notes

- Prefer exact chunk ID behavior for PI 1.
- Keep response text bounded to avoid oversized MCP messages.
- Include source title, URI, version, and section path.

## Done Evidence

- Contract tests for found and not-found cases.
- Example lookup response.
- Trace or log showing direct retrieval path.
