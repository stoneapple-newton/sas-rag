# Agent Instructions

## Project Overview

Early-stage Python project for a SAS knowledge retrieval system. The roadmap is:
1. Ingest SAS documentation, white papers, and commented SAS code into a vector database
2. Build an MCP server to expose the vector DB to LLMs and CLI coding tools
3. Maintain a Karpathy-style Markdown wiki for research and project settings
4. Use SAFe-style Markdown files for feature planning and project management

## Tech Stack

- **Python**: 3.13+ (managed via `.python-version`)
- **Package Manager**: `uv` — use `uv add <pkg>`, `uv run <script>`, `uv pip install`
- **Project File**: `pyproject.toml` — dependencies and scripts live here
- **Entry Point**: `main.py` (placeholder)

## Directory Conventions

Create these top-level directories as the project grows:
- `src/` — application code (vector DB ingestion, MCP server)
- `wiki/` — Karpathy-style Markdown wiki for research notes and project settings
- `safe/` — SAFe-style Markdown files for epics, features, and backlog items
- `data/` — ingested SAS docs, white papers, and code samples
- `tests/` — test suite

## Development Workflow

- Always run `uv sync` after pulling changes to `pyproject.toml` or `uv.lock`
- Use `uv run python main.py` to execute the entry point
- Prefer `uv add` over manual `pyproject.toml` edits to keep the lockfile in sync

## MCP Server Context

The MCP server will eventually expose the vector database to LLMs. Design it as a separate module under `src/mcp/` with clear separation from ingestion logic.

## Documentation Style

- `wiki/` files: concise, linked Markdown following Karpathy's minimal wiki style
- `safe/` files: structured Markdown using SAFe terminology (Epic → Feature → Story)
- Keep both human-readable and LLM-parseable
