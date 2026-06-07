# Developer Environment

Local development uses Python 3.13 and `uv`.

Related stories:
- [DEV-001](../../safe/feature/DEV-001-add-one-command-local-setup-run-path.md)
- [DEV-002](../../safe/feature/DEV-002-add-dockerized-local-dev-environment.md)

Notes:
- Install dependencies with `uv sync`.
- Copy `example.env` to `.env` for local secrets and machine-specific paths.
- Keep `.env` untracked; `.gitignore` excludes it.
- Run PDF ingestion with `uv run python -m sas_rag.ingestion.cli ingest-pdfs --source-dir docs/sas-documents --whitelist data/source_whitelist.json --out data/ingestion/runs/latest`.
- Planned LangChain/Chroma indexing dependencies: `langchain-core`, `langchain-openai`, `langchain-chroma`, and Chroma runtime dependencies.
- Keep `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`, `SAS_RAG_CHROMA_PATH`, and `SAS_RAG_CHROMA_COLLECTION` in `.env`.
