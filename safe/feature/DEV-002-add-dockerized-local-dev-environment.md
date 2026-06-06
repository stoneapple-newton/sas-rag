# DEV-002 - Add Dockerized Local Dev Environment

Type: Feature Story
Parent: [Dockerized Local Environment](../feature-dockerized-local-environment.md)
Capability: Delivery and operations
Sprint: Delta
Points: 5
Status: Proposed
Dependencies: DEV-001, MCP-001
Wiki: [Developer Environment](../../docs/wiki/developer-environment.md), [Security Model](../../docs/wiki/security-model.md)

## Story

As a developer, I want a Dockerized local environment, so that demos and evals run in a reproducible container.

## Detail

Create a local container path for running the MCP server or smoke workflow without embedding credentials into the image.

## Acceptance Criteria

- Docker image builds locally.
- Container can run the local MCP server or project smoke command.
- Secrets are passed at runtime and are not baked into the image.

## Implementation Notes

- Use multi-stage builds if they reduce runtime image size or risk.
- Keep local persisted indexes mounted or configured explicitly.
- Document runtime environment variables.

## Done Evidence

- Docker build output.
- Container smoke run output.
- Secret handling review note.
