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
