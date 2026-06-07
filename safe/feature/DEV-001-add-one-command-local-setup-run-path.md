# DEV-001 - Add One-Command Local Setup/Run Path

Type: Feature Story
Parent: [Dockerized Local Environment](../feature-dockerized-local-environment.md)
Capability: Delivery and operations
Sprint: Alpha
Points: 5
Status: Done
Dependencies: None
Wiki: [Developer Environment](../../docs/wiki/developer-environment.md)

## Story

As a developer, I want one documented local setup and run path, so that I can start the project consistently.

## Detail

Define the first reliable local developer workflow using `uv`, the existing Python 3.13 project setup, and the current entry point or documented successor.

## Acceptance Criteria

- Setup uses `uv sync` for dependencies.
- Entry point can be run with `uv run python main.py` or documented successor command.
- Local configuration requirements are documented.

## Implementation Notes

- Prefer `uv add` for new dependencies.
- Keep setup aligned with `AGENTS.md`.
- Do not require Docker for the Alpha local path.

## Done Evidence

- Local setup instructions in `docs/wiki/developer-environment.md`.
- Official entry point documented: `uv run python -m sas_rag.ingestion.cli` (subcommands: `ingest-pdfs`, `index-chroma`, `query-chroma`).
- `uv sync` installs dependencies; `example.env` documents required variables.
