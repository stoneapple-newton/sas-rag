# MCP-002 - Add `search_sas_docs` Tool

Type: Feature Story
Parent: [Local Stdio MCP Tools](../feature-local-stdio-mcp-tools.md)
Capability: MCP interaction layer
Sprint: Gamma
Points: 5
Status: Done
Dependencies: MCP-001, RET-002
Wiki: [MCP Server](../../docs/wiki/mcp-server.md), [Tool Contracts](../../docs/wiki/tool-contracts.md)

## Story

As a coding agent, I want to search SAS docs, so that I can retrieve official source snippets for SAS questions.

## Detail

Expose semantic retrieval through a read-only MCP tool. This is the primary tool for local agent discovery of official SAS documentation.

## Acceptance Criteria

- Tool accepts query, top-k, and optional metadata filters.
- Tool returns ranked results with citations and chunk IDs.
- Tool contract is covered by MCP contract tests.

## Implementation Notes

- Keep request and response schema versioned.
- Return clear validation errors for invalid top-k or filters.
- Never mutate files, indexes, or external services from this tool.

## Done Evidence

- Contract tests pass in `tests/test_mcp_contracts.py`.
- Example request: `{"query": "PROC SQL join syntax", "top_k": 1, "filters": {"source_family": "proc-sql"}}`.
- Example response includes `schema_version: "1.0"`, ranked result text, citation metadata, and chunk ID.
- Local stdio MCP smoke call on 2026-06-07 returned cited PROC SQL Procedure User's Guide chunk `d45ef63bda8acda13d278b99`.
