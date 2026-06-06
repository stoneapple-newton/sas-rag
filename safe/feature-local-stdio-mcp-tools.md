# Local Stdio MCP Tools

Type: Feature
Capability: MCP interaction layer
Priority: P0
Sprint target: Gamma/Delta
Owner role: Backend Engineer
Status: Proposed
Dependencies: RET-002, CITE-001

## Intent

Expose the SAS RAG retrieval system through a local `stdio` MCP server for Codex and local coding-agent workflows.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| MCP-001 | Feature | Implement local stdio MCP server shell | 5 | Gamma | RET-002 |
| MCP-002 | Feature | Add `search_sas_docs` tool | 5 | Gamma | MCP-001, RET-002 |
| MCP-003 | Feature | Add `get_sas_section` tool | 5 | Gamma | MCP-001, PROV-002 |
| MCP-004 | Feature | Add `explain_sas_code` tool using retrieved evidence | 8 | Gamma | MCP-002, CITE-002 |
| MCP-005 | Feature | Add `recommend_proc` tool | 5 | Delta | MCP-002, RET-003 |

## Story Details

### MCP-001 - Implement local stdio MCP server shell

As a local coding-agent user, I want a `stdio` MCP server, so that Codex can call SAS retrieval tools without remote infrastructure.

Acceptance criteria:
- Server starts locally over `stdio`.
- Retrieval dependencies are configured through environment variables or config files.
- Server startup fails clearly when required local index or settings are missing.

### MCP-002 - Add `search_sas_docs` tool

As a coding agent, I want to search SAS docs, so that I can retrieve official source snippets for SAS questions.

Acceptance criteria:
- Tool accepts query, top-k, and optional metadata filters.
- Tool returns ranked results with citations and chunk IDs.
- Tool contract is covered by MCP contract tests.

### MCP-003 - Add `get_sas_section` tool

As a coding agent, I want to fetch a known SAS section or chunk, so that I can inspect source context after search.

Acceptance criteria:
- Tool accepts chunk ID or section reference supported by the index.
- Tool returns source text and provenance metadata.
- Tool returns a clear not-found response for unknown IDs.

### MCP-004 - Add `explain_sas_code` tool using retrieved evidence

As a coding agent, I want SAS code explained using official documentation evidence, so that explanations are grounded in SAS behavior.

Acceptance criteria:
- Tool accepts SAS code and optional user question.
- Tool retrieves supporting documentation before composing an explanation.
- Tool cites supporting SAS sources or returns insufficient evidence.

### MCP-005 - Add `recommend_proc` tool

As a SAS user, I want procedure recommendations based on task intent, so that I can find the right SAS procedure with source-backed rationale.

Acceptance criteria:
- Tool accepts task description and optional constraints.
- Tool returns recommended PROC candidates with citations.
- Tool avoids unsupported recommendations when evidence is weak.

## Definition of Done

- Local MCP server works through `stdio`.
- All tools are read-only.
- Tool schemas are documented and contract-tested.
