# SEC-001 - Document Secret Handling and Env Var Policy

Type: Enabler Story
Parent: [Security and Secret Management](../enabler-security-secret-management.md)
Capability: Delivery and operations
Sprint: Alpha
Points: 3
Status: Proposed
Dependencies: None
Wiki: [Security Model](../../docs/wiki/security-model.md), [Developer Environment](../../docs/wiki/developer-environment.md)

## Story

As a maintainer, I want clear secret handling rules, so that model keys and tracing keys are not committed or logged.

## Detail

Define how local developers provide model, embedding, and tracing credentials. The policy should be simple enough for local PI 1 use and strict enough to avoid accidental commits.

## Acceptance Criteria

- Required environment variables are documented without real values.
- `.env` or local secret files are excluded from source control where applicable.
- Logs and traces must not include raw API keys or credentials.

## Implementation Notes

- Keep secret names aligned with config code.
- Prefer runtime environment variables.
- Include tracing keys and model provider keys.

## Done Evidence

- Secret policy note.
- `.gitignore` or equivalent review where applicable.
- Local setup documentation references policy.
