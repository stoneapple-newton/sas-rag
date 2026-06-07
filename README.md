# SAS RAG MCP

Early-stage Python project for a SAS retrieval-augmented generation system exposed through a local MCP server for coding agents.

## Current Status

- Project scaffold exists with Python 3.13 and `uv`.
- `main.py` is still a placeholder entry point.
- SAFe PI planning artifacts exist under `safe/`.
- Curated wiki pages exist under `docs/wiki/`.
- PDF-first ingestion and Chroma indexing are implemented for local official SAS 9.4 PDFs.
- Metadata-filtered retrieval and citation formatting are implemented.
- Local stdio MCP server shell exists with the read-only `search_sas_docs` tool.

## PI 1 Defaults

- Corpus: official SAS 9.4 documentation only.
- First MCP target: local `stdio` server for Codex and local coding agents.
- Vector store: Chroma for local persisted development.
- Model provider: configurable OpenAI default, with provider interfaces kept swappable.
- Planning cadence: 8-week PI with Alpha, Beta, Gamma, and Delta sprints.

## Repo Map

- `AGENTS.md` - agent instructions and repo conventions
- `main.py` - placeholder Python entry point
- `pyproject.toml` - Python project metadata
- `safe/` - SAFe PI plan, feature/enabler parent files, and sprint map
- `safe/feature/` - individual feature stories
- `safe/enabler/` - individual enabler stories
- `docs/raw/` - raw notes and source material before curation
- `docs/wiki/` - concise linked wiki pages
- `.agents/skills/` - repo-local Codex skills

## Development

Install dependencies:

```powershell
uv sync
```

Run the current entry point:

```powershell
uv run python main.py
```

Run the local stdio MCP server:

```powershell
uv run sas-rag-mcp
```

Project-local Codex MCP config lives in `.codex/config.toml` and registers the `sas_rag` server for local Codex sessions started from this repository.

Prefer `uv add <package>` for dependencies so `pyproject.toml` and `uv.lock` stay aligned.

## Planning and Docs

- Start with [safe/README.md](safe/README.md) for the PI backlog.
- Use [safe/feature/README.md](safe/feature/README.md) for feature stories.
- Use [safe/enabler/README.md](safe/enabler/README.md) for enabler stories.
- Use [docs/wiki/README.md](docs/wiki/README.md) for curated wiki topics.
- Use [docs/README.md](docs/README.md) and [docs/log.md](docs/log.md) for documentation operations.
