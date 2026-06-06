# Dockerized Local Environment

Type: Feature
Capability: Delivery and operations
Priority: P0
Sprint target: Alpha/Delta
Owner role: DevOps/SRE
Status: Proposed
Dependencies: None

## Intent

Make the project reproducible for local development, demos, and evaluations without requiring each developer to manually recreate the runtime environment.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| DEV-001 | Feature | Add one-command local setup/run path | 5 | Alpha | None |
| DEV-002 | Feature | Add Dockerized local dev environment | 5 | Delta | DEV-001, MCP-001 |

## Story Details

### DEV-001 - Add one-command local setup/run path

As a developer, I want one documented local setup and run path, so that I can start the project consistently.

Acceptance criteria:
- Setup uses `uv sync` for dependencies.
- Entry point can be run with `uv run python main.py` or documented successor command.
- Local configuration requirements are documented.

### DEV-002 - Add Dockerized local dev environment

As a developer, I want a Dockerized local environment, so that demos and evals run in a reproducible container.

Acceptance criteria:
- Docker image builds locally.
- Container can run the local MCP server or project smoke command.
- Secrets are passed at runtime and are not baked into the image.

## Definition of Done

- Local setup path is documented.
- Docker build and smoke run are documented.
- Environment does not require committed secrets.
