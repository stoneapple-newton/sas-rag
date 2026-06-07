# MCP-004 - Add `explain_sas_code` Tool Using Retrieved Evidence

Type: Feature Story
Parent: [Local Stdio MCP Tools](../feature-local-stdio-mcp-tools.md)
Capability: MCP interaction layer
Sprint: Gamma
Points: 8
Status: Ready
Dependencies: MCP-002, CITE-002
Wiki: [MCP Server](../../docs/wiki/mcp-server.md), [Citation Grounding](../../docs/wiki/citation-grounding.md), [Chunking Strategy](../../docs/wiki/chunking-strategy.md)

## Story

As a coding agent, I want SAS code explained using official documentation evidence, so that explanations are grounded in SAS behavior.

## Detail

The tool accepts SAS code and an optional question, retrieves relevant official documentation, and composes an explanation with citations. It should not claim unsupported behavior.

## Acceptance Criteria

- Tool accepts SAS code and optional user question.
- Tool retrieves supporting documentation before composing an explanation.
- Tool cites supporting SAS sources or returns insufficient evidence.

## Implementation Notes

- Use retrieval before generation.
- Preserve code snippets in the request without logging secrets or local file content beyond the user-provided snippet.
- Keep final answer focused on observed code and retrieved SAS docs.

## Done Evidence

- Contract test for supported explanation.
- Contract test for insufficient evidence.
- Example answer with citations.
