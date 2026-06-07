# Project Codex Config

This folder contains project-local Codex configuration for the SAS RAG MCP server.

The `sas_rag` MCP server is local-only and uses stdio:

```powershell
uv run sas-rag-mcp
```

Requirements:
- Run Codex from the repository root.
- `.env` must contain `OPENAI_API_KEY`.
- `data/chroma/chroma.sqlite3` must exist.

