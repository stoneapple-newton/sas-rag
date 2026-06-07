# Tool Contracts

MCP tools should have stable request, response, and error shapes.

Related stories:
- [SCHEMA-001](../../safe/enabler/SCHEMA-001-define-versioned-mcp-tool-schemas.md)
- [SCHEMA-002](../../safe/enabler/SCHEMA-002-add-mcp-contract-tests.md)

Notes:
- Include schema versioning in docs or tool metadata.
- Cover validation, not-found, and insufficient-evidence errors.
- Current schema version: `1.0`.
- Standard tool response shape: `schema_version`, `results`, `error`.
- Standard error shape: `code`, `message`, optional `details`.
- Error codes reserved in PI 1: `validation_error`, `not_found`, `insufficient_evidence`, `configuration_error`, `internal_error`.

## `search_sas_docs`

Request:
- `schema_version`: optional, default `1.0`.
- `query`: required non-empty string.
- `top_k`: optional integer, 1 through 20, default 5.
- `filters`: optional metadata filter object with scalar values.

Response:
- `results`: ranked list with `rank`, `score`, `text`, `citation`, and `metadata`.
- `citation`: includes `chunk_id`, `title`, `source_uri`, `version`, `section_path`, `page`, `source_family`, `chunk_type`, and `score`.
- Validation failures return an empty result list plus `error.code = validation_error`.
