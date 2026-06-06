# MCP-005 - Add `recommend_proc` Tool

Type: Feature Story
Parent: [Local Stdio MCP Tools](../feature-local-stdio-mcp-tools.md)
Capability: MCP interaction layer
Sprint: Delta
Points: 5
Status: Proposed
Dependencies: MCP-002, RET-003
Wiki: [MCP Server](../../docs/wiki/mcp-server.md), [Retrieval Architecture](../../docs/wiki/retrieval-architecture.md)

## Story

As a SAS user, I want procedure recommendations based on task intent, so that I can find the right SAS procedure with source-backed rationale.

## Detail

Recommend likely SAS procedures from official documentation evidence. The tool should cite why each recommendation fits and avoid overconfident guesses.

## Acceptance Criteria

- Tool accepts task description and optional constraints.
- Tool returns recommended PROC candidates with citations.
- Tool avoids unsupported recommendations when evidence is weak.

## Implementation Notes

- Use lexical fallback and semantic retrieval together for PROC names.
- Return multiple candidates when the task is ambiguous.
- Keep output concise for coding-agent use.

## Done Evidence

- Example recommendation response.
- Contract test for weak evidence.
- Benchmark or demo question showing useful recommendation.
