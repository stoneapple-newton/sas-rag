# Agent Instructions

## Project Overview

Early-stage Python project for a SAS knowledge retrieval system and local MCP server. The PI 1 plan is documentation-first and focuses on:
1. Ingesting official SAS 9.4 documentation into a vector database
2. Building a local `stdio` MCP server for Codex and local coding agents
3. Maintaining a concise Karpathy-style Markdown wiki under `docs/wiki/`
4. Managing SAFe-style planning files under `safe/`

Current status:
- Python project scaffold exists with `main.py` as a placeholder entry point.
- SAFe PI plan exists in `safe/Overall-structure.md`.
- Feature/enabler parent files and individual story files exist under `safe/`, `safe/feature/`, and `safe/enabler/`.
- Wiki stubs exist under `docs/wiki/`.
- Raw source/research landing zone exists under `docs/raw/`.
- Implementation code for ingestion, retrieval, and MCP server is not built yet.

## Tech Stack

- Python: 3.13+ managed via `.python-version`
- Package manager: `uv`
- Project file: `pyproject.toml`
- Entry point: `main.py` placeholder

## Directory Conventions

Create or maintain these directories as the project grows:
- `src/` - application code for ingestion, retrieval, vector DB operations, and MCP server
- `docs/raw/` - raw research notes, copied source notes, and uncurated source material
- `docs/wiki/` - Karpathy-style Markdown wiki for curated research notes and project settings
- `safe/` - SAFe-style parent planning files, PI index, and sprint map
- `safe/feature/` - individual SAFe feature story files
- `safe/enabler/` - individual SAFe enabler story files
- `data/` - ingested SAS docs, white papers, and code samples when implementation begins
- `tests/` - test suite when implementation begins
- `.agents/skills/safe-wiki-manager/` - repo-local skill for maintaining SAFe and wiki files

## Development Workflow

- Always run `uv sync` after pulling changes to `pyproject.toml` or `uv.lock`
- Use `uv run python main.py` to execute the current entry point
- Prefer `uv add` over manual `pyproject.toml` edits to keep the lockfile in sync

## MCP Server Context

The MCP server will eventually expose the vector database to LLMs and coding agents. Design it as a separate module under `src/mcp/` or an equivalent MCP-focused package with clear separation from ingestion and retrieval logic.

PI 1 MCP constraints:
- Local `stdio` transport first
- Read-only tools only
- Official SAS 9.4 corpus first
- Chroma-backed local retrieval by default
- Configurable OpenAI default for embeddings/LLM provider

## Documentation Style

- `docs/wiki/` files: concise, linked Markdown following Karpathy's minimal wiki style
- `safe/` files: structured Markdown using SAFe terminology: Epic -> Capability -> Feature/Enabler -> Story
- `docs/raw/` files: raw inputs only; curate them into `docs/wiki/` before relying on them as project knowledge
- `docs/README.md`: documentation area guide
- `docs/log.md`: documentation changes, raw imports, decisions, and follow-ups
- Keep both human-readable and LLM-parseable

## Planning and Wiki Maintenance

- Use the `safe-wiki-manager` skill when updating SAFe files, wiki pages, raw-to-wiki imports, docs indexes, or docs logs.
- Preserve story IDs and parent links when changing files under `safe/feature/` and `safe/enabler/`.
- Every individual story should include type, parent, capability, sprint, points, status, dependencies, wiki links, story, acceptance criteria, implementation notes, and done evidence.
- Wiki pages should be short, topic-oriented, and linked to related SAFe stories and neighboring wiki pages.
