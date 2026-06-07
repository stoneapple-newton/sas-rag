# Chroma Index

Chroma is the PI 1 default vector store for local persisted development.

Related stories:
- [RET-001](../../safe/feature/RET-001-create-chroma-backed-vector-index.md)
- [ING-004](../../safe/enabler/ING-004-add-checksum-and-re-ingestion-controls.md)

Notes:
- Collection name and storage path should be configurable.
- Metadata must support filters and citation assembly.
- Chroma integration should use the dedicated LangChain package `langchain-chroma`.
- Embeddings should use LangChain provider integrations, with `langchain-openai` and `OPENAI_EMBEDDING_MODEL` as the default path.
- Default local settings: `SAS_RAG_CHROMA_PATH=data/chroma`, `SAS_RAG_CHROMA_COLLECTION=sas_94_docs`.
- Do not mix embedding models between indexing and querying for the same Chroma collection.
- Build from ingestion chunk records by mapping `text` to LangChain document content and chunk metadata to document metadata.
- First run command: `uv run python -m sas_rag.ingestion.cli index-chroma --chunks data/ingestion/runs/latest/chunks.jsonl --priority P0 --reset`.
- First run result: 8,953 P0 chunks indexed into `sas_94_docs`; 8,182 non-P0 chunks skipped.
- 2026-06-07 refresh result: 0 new indexed, 8,953 duplicates skipped, collection already current.
- Report path: `data/ingestion/runs/latest/chroma_report.json`.
- Smoke query: `uv run python -m sas_rag.ingestion.cli query-chroma "PROC SQL join syntax" --k 3`.
- Smoke result returned SQL join chunks from `docs/sas-documents/sqlproc.pdf` with citation-ready metadata.
- Implementation module: `src/sas_rag/ingestion/chroma_index.py`.
- CLI entrypoint: `src/sas_rag/ingestion/cli.py`.
- Tests: `tests/test_chroma_index.py` uses fake embeddings and a temporary Chroma directory, so indexing behavior is covered without OpenAI calls.
- MCP depends on this collection at startup and fails clearly if `data/chroma/chroma.sqlite3` is missing.
