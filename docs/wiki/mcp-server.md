# MCP Server

PI 1 exposes the SAS RAG system through a local `stdio` MCP server.

Related stories:
- [MCP-001](../../safe/feature/MCP-001-implement-local-stdio-mcp-server-shell.md)
- [MCP-002](../../safe/feature/MCP-002-add-search-sas-docs-tool.md)
- [MCP-003](../../safe/feature/MCP-003-add-get-sas-section-tool.md)
- [MCP-004](../../safe/feature/MCP-004-add-explain-sas-code-tool-using-retrieved-evidence.md)
- [MCP-005](../../safe/feature/MCP-005-add-recommend-proc-tool.md)

Notes:
- Keep MCP tools read-only for PI 1.
- Keep retrieval and answer composition behind service boundaries.
- Local server package: `sas_rag.mcp_server`.
- Local stdio command: `uv run sas-rag-mcp`.
- Project-local Codex config: `.codex/config.toml` registers MCP server `sas_rag`.
- Startup validates `OPENAI_API_KEY` and `data/chroma/chroma.sqlite3`.
- Console logs go to stderr so stdout remains reserved for MCP JSON-RPC.
- Current tool: `search_sas_docs`.
- 2026-06-07 stdio smoke listed `search_sas_docs` through an MCP client session.
- 2026-06-07 live stdio tool call for `PROC SQL join syntax` returned cited chunk `d45ef63bda8acda13d278b99` from SAS SQL Procedure User's Guide.
