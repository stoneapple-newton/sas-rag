# Documentation Log

## 2026-06-07

- Confirmed all completed ingestion/indexing work is represented in SAFe and wiki files.
- Updated parent Hybrid Retrieval Profile with RET-001 completion evidence and current remaining retrieval scope.
- Added wiki implementation inventory for Chroma indexing module, CLI commands, generated artifacts, and test coverage.

## 2026-06-06

- Created SAFe PI backlog index under `safe/README.md`.
- Added parent feature and enabler planning files under `safe/`.
- Split individual feature stories into `safe/feature/`.
- Split individual enabler stories into `safe/enabler/`.
- Created initial Karpathy-style wiki stubs under `docs/wiki/`.
- Added documentation area guide in `docs/README.md`.
- Initialized documentation log in `docs/log.md`.
- Created repo-local `safe-wiki-manager` skill for SAFe and wiki maintenance.
- Imported `docs/raw/sas-rag-docs.md` into `docs/wiki/sas-rag-docs.md`.
- Curated SAS-aware chunking guidance from `docs/raw/sas-rag-docs.md` into `docs/wiki/chunking-strategy.md` and related CHUNK planning files.
- Checked for newly added raw Markdown files; no additional `.md` file was visible under `docs/raw/` at import time.
- Imported `docs/raw/Chunking research.md` into `docs/wiki/chunking-research.md`.
- Curated parent-child chunking, reference-object chunks, three-index retrieval, default chunk sizes, and metadata guidance into `docs/wiki/chunking-strategy.md` and related CHUNK planning files.
- Added `example.env` with placeholder OpenAI, LangSmith, Chroma, and local ingestion settings; `.env` is ignored.
- Added `data/source_whitelist.json` for the 22 local SAS PDFs under `docs/sas-documents/`.
- Implemented the PDF-first ingestion package under `src/sas_rag/ingestion/`.
- Ran PDF ingestion: 22 sources loaded, 16,698 pages parsed, 17,135 chunks emitted, 0 failed sources.
- Updated ING-001 and corpus/ingestion/provenance wiki notes with local PDF source policy and run evidence.
- Updated ingestion and retrieval SAFe/wiki notes to make LangChain `Document` conversion, OpenAI embeddings, and `langchain-chroma` persistence the planned indexing path.
- Added Chroma indexing CLI support using LangChain documents, `langchain-openai`, and `langchain-chroma`.
- Ran first P0 Chroma indexing pass: 8,953 chunks indexed into `sas_94_docs`, 8,182 non-P0 chunks skipped, embedding model `text-embedding-3-small`.
- Ran Chroma smoke query `PROC SQL join syntax`; results returned SAS SQL Procedure User's Guide chunks with citation metadata.

## 2026-06-07 (Alpha Sprint Completion)

- Closed ING-002: added idempotent Chroma indexing with duplicate skip on rerun; `ChromaIndexReport.duplicate_chunks` tracks skips.
- Closed PARSE-001: formalized `SourceAdapter` Protocol in `src/sas_rag/ingestion/pdf_adapter.py`; `PdfAdapter` implements it.
- Closed PARSE-002: normalization functions already implemented in `normalizer.py`; marked complete.
- Closed PROV-001: schema contract enforced via `REQUIRED_PROVENANCE_FIELDS` and validation tests.
- Closed PROV-002: every chunk emitted by `chunk_unit()` carries required provenance and calls `validate_provenance()`.
- Closed DEV-001: documented official entry point `uv run python -m sas_rag.ingestion.cli` in wiki.
- Closed OBS-001: LangSmith tracing deferred to Gamma; config-only in `example.env` and wiki.
- Closed CI-001: created `.github/workflows/ci.yml` with `ruff` and `pytest` via `uv`.
- Closed SEC-001: secret policy covered by `.gitignore`, `example.env`, and `docs/wiki/security-model.md`.
- Added dev dependencies `ruff` and `pytest` to `pyproject.toml` under `[dependency-groups] dev`.
- All 10 Alpha sprint stories now show `Status: Done`.

## Open Follow-Ups

- Implement lexical fallback for exact SAS identifiers in RET-003.
- Add schemas and contract tests for `get_sas_section` and `explain_sas_code`.
- Continue MCP server implementation with MCP-003 and MCP-004.

## 2026-06-07 (Sprint Beta Preparation)

- Carried ING-003 into Sprint Beta; remaining smoke retrieval evidence for macro, DATA step, and language reference topics scheduled for Beta completion.
- Transitioned 9 Beta stories from `Proposed` to `Ready`:
  - ING-004 (checksum/re-ingestion controls)
  - PROV-003 (provenance validation gate)
  - PARSE-003 (parser error and skip reporting)
  - CHUNK-001 (heading-aware documentation chunking)
  - CHUNK-002 (SAS-aware code boundary detection)
  - CHUNK-003 (persist chunk IDs and section paths)
  - RET-002 (semantic search with metadata filters)
  - CITE-001 (citations from retrieved chunks)
  - EVAL-001 (50-question benchmark dataset)
- Sprint Beta focus: ingestion scale-out, chunking, vector index, first citations, benchmark v1.
- Dependency note: CHUNK-003 depends on CHUNK-001; recommend completing CHUNK-001 early or establishing interface contract before parallel work.

## 2026-06-07 (Sprint Beta Implementation)

### CHUNK-001: Heading-Aware Documentation Chunking
- Enhanced `chunker.py` with `split_on_headings()` function that detects heading-like boundaries
- Added heading detection heuristics for "Chapter N / Title", "PART N", "Overview", "Syntax", "Examples" patterns
- Falls back to paragraph splitting for sections without detected headings
- Preserves section context through heading metadata

### CHUNK-002: SAS-Aware Code Boundary Detection
- Added `extract_sas_blocks()` function to detect PROC, DATA step, and MACRO boundaries
- Detects `PROC ... RUN;`, `DATA ... RUN;`, `%MACRO ... %MEND;` patterns
- Emits chunk metadata with `sas_block_types` and `sas_block_count`
- Distinguishes between syntax definitions and example code blocks

### CHUNK-003: Persist Chunk IDs and Section Paths
- Chunk IDs remain stable via `stable_chunk_id()` using source_id, section_path, ordinal, and content hash
- Enhanced metadata includes `chunk_type` (concept, syntax, example, option_table, troubleshooting)
- Section paths preserve heading context when heading-aware splitting is active
- Re-indexing unchanged sources does not create duplicate logical chunks (duplicate skip already in Chroma indexer)

### PROV-003: Provenance Validation Gate
- Added `validate_chunks()` function in `pipeline.py` that validates every chunk before indexing
- Tracks rejected chunks with source_id, chunk_id, reason, and metadata keys
- Writes `rejections.json` report when chunks fail validation
- Updated `SourceReport` to include `chunks_rejected` count
- Updated `IngestionReport.summary()` to include total rejected count

### PARSE-003: Parser Error and Skip Reporting
- Pipeline already catches exceptions per-source without crashing batch
- Distinguishes skipped (status not ready), unchanged (checksum match), failed (exception), and loaded sources
- Error reporting includes exception type and message
- No additional implementation needed; acceptance criteria satisfied by existing pipeline

### ING-004: Checksum and Re-Ingestion Controls
- Created `ChecksumRegistry` class in `src/sas_rag/ingestion/checksum.py`
- Persists source checksums across runs in `checksum_registry.json`
- Classifies sources as new, unchanged, or changed
- Supports `skip_unchanged` parameter to skip unchanged sources on rerun
- Registry updated after successful source processing

### RET-002: Semantic Search with Metadata Filters
- Created `src/sas_rag/retrieval/search.py` with `search_with_filters()` function
- Supports Chroma-compatible metadata filters (equality filters on any metadata field)
- Added convenience functions: `search_by_source_family()`, `search_by_chunk_type()`
- Results include score, text, and full metadata
- Added `search` CLI subcommand with `--source-family`, `--chunk-type`, `--priority` filters
- Empty filters dict returns unfiltered semantic search

### CITE-001: Citations from Retrieved Chunks
- Implemented `format_citation()` in `src/sas_rag/retrieval/search.py`
- Extracts citation-ready fields: chunk_id, title, source_uri, version, section_path, page, source_family, chunk_type, score
- Added `--citations` flag to `search` CLI command for citation-formatted output
- Citation fields are generated from provenance metadata, not prompt-only text

### EVAL-001: 50-Question Benchmark Dataset
- Created `data/benchmark/sas_questions.json` with 53 curated questions (48 supported + 5 unsupported)
- Coverage: macro (9), proc-sql (9), data-step (8), language-reference (10), procedures (7), language-concepts (5)
- Difficulty distribution: beginner (16), intermediate (25), advanced (12)
- 5 unsupported questions test refusal behavior (quantum computing, blockchain, telepathy, time reversal, lottery)
- Updated `docs/wiki/evaluation-benchmark.md` with dataset overview and schema

### ING-003: Smoke Evidence Carryover
- Original Beta implementation lacked live OpenAI smoke evidence for macro, DATA step, and language-reference topics
- Resolved during Gamma Sprint Start on 2026-06-07 with live OpenAI-backed Chroma searches
- ING-003 is now closed

### Files Changed
- `src/sas_rag/ingestion/chunker.py` - heading-aware and SAS-aware chunking
- `src/sas_rag/ingestion/pipeline.py` - validation gate, checksum integration
- `src/sas_rag/ingestion/models/records.py` - chunks_rejected field
- `src/sas_rag/ingestion/checksum.py` - new checksum registry module
- `src/sas_rag/ingestion/cli.py` - search command with filters and citations
- `src/sas_rag/retrieval/search.py` - new retrieval module
- `src/sas_rag/retrieval/__init__.py` - retrieval package
- `data/benchmark/sas_questions.json` - benchmark dataset
- `docs/wiki/evaluation-benchmark.md` - benchmark documentation

## 2026-06-07 (Gamma Sprint Start)

- Refreshed Chroma collection `sas_94_docs` at `data/chroma`; 8,953 P0 chunks already present, 0 new indexed, 8,953 duplicates skipped.
- Completed live OpenAI-backed smoke retrieval for macro, DATA step, and language-reference topics; closed ING-003.
- Added `mcp` dependency and `sas-rag-mcp` console script for the local stdio MCP server.
- Implemented `sas_rag.mcp_server` with startup validation, clean stderr logging, versioned schemas, and read-only `search_sas_docs`.
- Fixed OpenAI embedding construction to pass the configured API key from Pydantic settings into `OpenAIEmbeddings`.
- Added MCP contract tests for `search_sas_docs` success, validation error, server registration, and missing-index startup validation.
- Verified live stdio MCP client can call `search_sas_docs`; PROC SQL smoke returned cited chunk `d45ef63bda8acda13d278b99`.
- Marked MCP-001 and MCP-002 Done; moved remaining Gamma stories to Ready where implementation has not started.

## 2026-06-07 (SAFe and Wiki Reconciliation)

- Updated `safe/README.md` with the current Alpha/Beta/Gamma status, current Chroma collection, and MCP command.
- Updated parent SAFe pages so ingestion is Done and Gamma parent items reflect In Progress/Ready state.
- Updated `docs/wiki/chroma-index.md` with the 2026-06-07 refresh result and MCP startup dependency.
- Updated feature/enabler story indexes with status columns.
- Updated security, observability/evals, citation grounding, and benchmark wiki pages with current Gamma-start state.
- Added project-local Codex MCP configuration in `.codex/config.toml` for server `sas_rag`.
- Added `docs/wiki/sas-etl-example-analysis.md` with MCP-backed analysis of `sas-test-code/sas-etl-example.sas`.
- Added `docs/wiki/sas-etl-example-direct-analysis.md` with direct no-RAG analysis of `sas-test-code/sas-etl-example.sas` and cross-linked it with the MCP-backed analysis page.
- Refreshed `docs/wiki/sas-etl-example-analysis.md` with a current MCP-backed SAS construct analysis and explicit citation coverage limitations.
