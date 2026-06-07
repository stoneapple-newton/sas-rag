# SCHEMA-002 - Add MCP Contract Tests

Type: Enabler Story
Parent: [Tool Schema Versioning](../enabler-tool-schema-versioning.md)
Capability: MCP interaction layer
Sprint: Gamma
Points: 5
Status: Proposed
Dependencies: SCHEMA-001, MCP-002
Wiki: [Tool Contracts](../../docs/wiki/tool-contracts.md), [CI Quality Gates](../../docs/wiki/ci-quality-gates.md)

## Story

As a QA engineer, I want contract tests for MCP tools, so that schema regressions are caught before release.

## Detail

Add tests that verify tool request validation, response structure, and error behavior for local `stdio` MCP tools.

## Acceptance Criteria

- Contract tests cover successful and error responses for core tools.
- Tests can run locally without remote HTTP deployment.
- CI can execute contract tests after MCP implementation exists.

## Implementation Notes

- Start with `search_sas_docs` and expand as tools land.
- Use fixtures or sample indexes to keep tests repeatable.
- Treat schema changes as intentional test updates.

## Done Evidence

- Contract test output.
- CI integration note.
- Example failing schema regression if practical.
