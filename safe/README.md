# SAS RAG MCP PI Backlog

This folder contains the SAFe-style planning artifacts for the first 8-week Program Increment for the SAS RAG MCP project. The source roadmap is [Overall-structure.md](Overall-structure.md).

## PI assumptions

- Corpus scope: official SAS 9.4 documentation only.
- First release target: local `stdio` MCP server for Codex and local coding agents.
- Model provider: configurable OpenAI default, with provider interfaces kept swappable.
- Vector store default: Chroma for local persisted development.
- Sprint cadence: four 2-week sprints named Alpha, Beta, Gamma, and Delta.
- PI status legend: `Proposed`, `Ready`, `In Progress`, `Done`, `Blocked`.

## Feature and enabler backlog

Individual story files live in [feature/](feature/README.md) and [enabler/](enabler/README.md). Wiki context for the backlog lives in [../docs/wiki/](../docs/wiki/README.md).

| Item | Type | Capability | Priority | Sprint target |
|---|---|---|---|---|
| [Official SAS Docs Ingestion](feature-official-sas-docs-ingestion.md) | Feature | Corpus ingestion and provenance | P0 | Alpha/Beta |
| [Provenance Schema](feature-provenance-schema.md) | Feature | Corpus ingestion and provenance | P0 | Alpha/Beta |
| [Parser Adapter Layer](enabler-parser-adapter-layer.md) | Enabler | Corpus ingestion and provenance | P0 | Alpha/Beta |
| [Structure-Aware Chunking](feature-structure-aware-chunking.md) | Feature | Retrieval and grounding | P0 | Beta |
| [Hybrid Retrieval Profile](feature-hybrid-retrieval-profile.md) | Feature | Retrieval and grounding | P0 | Beta/Gamma |
| [Citation Assembler](feature-citation-assembler.md) | Feature | Retrieval and grounding | P0 | Beta/Gamma |
| [Benchmark Dataset](enabler-benchmark-dataset.md) | Enabler | Retrieval and grounding | P0 | Beta/Delta |
| [Local Stdio MCP Tools](feature-local-stdio-mcp-tools.md) | Feature | MCP interaction layer | P0 | Gamma/Delta |
| [Tool Schema Versioning](enabler-tool-schema-versioning.md) | Enabler | MCP interaction layer | P1 | Gamma |
| [LangSmith Observability](feature-langsmith-observability.md) | Feature | Delivery and operations | P0 | Alpha/Gamma/Delta |
| [Dockerized Local Environment](feature-dockerized-local-environment.md) | Feature | Delivery and operations | P0 | Alpha/Delta |
| [GitHub Actions CI](feature-github-actions-ci.md) | Feature | Delivery and operations | P0 | Alpha/Delta |
| [Security and Secret Management](enabler-security-secret-management.md) | Enabler | Delivery and operations | P0 | Alpha/Gamma/Delta |

## Sprint map

| Sprint | Focus | Story IDs |
|---|---|---|
| Alpha | Foundation, source policy, metadata, parser spike, local run path | ING-001, ING-002, PROV-001, PROV-002, PARSE-001, PARSE-002, OBS-001, DEV-001, CI-001, SEC-001 |
| Beta | Ingestion scale-out, chunking, vector index, first citations, benchmark v1 | ING-003, ING-004, PROV-003, PARSE-003, CHUNK-001, CHUNK-002, CHUNK-003, RET-001, RET-002, CITE-001, EVAL-001 |
| Gamma | MCP server, tool contracts, retrieval hardening, traces, threat model | RET-003, CITE-002, CITE-003, EVAL-002, MCP-001, MCP-002, MCP-003, MCP-004, SCHEMA-001, SCHEMA-002, OBS-002, SEC-002 |
| Delta | Final MCP tool, regression gate, Docker, CI evals, least privilege | EVAL-003, MCP-005, OBS-003, DEV-002, CI-002, SEC-003 |

## Definition of Done

- Acceptance criteria are met.
- Tests and relevant evals pass.
- Documentation or runbooks are updated when behavior changes.
- Security impact is reviewed for auth, secrets, tool scope, or external calls.
- Demo evidence is available for the sprint system demo.
