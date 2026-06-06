# Documentation Log

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

## Open Follow-Ups

- Implement ingestion, retrieval, and MCP server code after planning stories are accepted.
