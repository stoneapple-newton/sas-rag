# Security Model

PI 1 assumes local, read-only MCP tools and environment-based secrets.

Related stories:
- [SEC-001](../../safe/enabler/SEC-001-document-secret-handling-and-env-var-policy.md)
- [SEC-002](../../safe/enabler/SEC-002-threat-model-local-mcp-tool-surface.md)
- [SEC-003](../../safe/enabler/SEC-003-verify-read-only-least-privilege-tool-behavior.md)

Notes:
- Do not commit API keys or tracing credentials.
- Use `example.env` for placeholder variable names and `.env` for real local values.
- Do not add write-capable MCP tools in PI 1.
- Review prompt-injection and local index exposure risks before release.
- Current MCP tool surface is read-only: `search_sas_docs`.
- Current local MCP server validates that `OPENAI_API_KEY` and the Chroma index exist before startup.
- Stdio logs go to stderr so log records do not corrupt MCP JSON-RPC on stdout.
- Rotate any local API key that has been pasted into chat or terminal transcripts.
