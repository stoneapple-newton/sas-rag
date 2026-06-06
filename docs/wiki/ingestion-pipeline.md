# Ingestion Pipeline

The ingestion pipeline loads whitelisted SAS sources, parses them through adapters, normalizes text, emits chunks, validates provenance, embeds content, and writes to the local index.

Related stories:
- [PARSE-001](../../safe/enabler/PARSE-001-create-loader-adapter-interface-for-html-pdf-text.md)
- [PARSE-002](../../safe/enabler/PARSE-002-normalize-extracted-text-and-headings.md)
- [PARSE-003](../../safe/enabler/PARSE-003-capture-parser-errors-and-skipped-source-reports.md)
- [ING-004](../../safe/enabler/ING-004-add-checksum-and-re-ingestion-controls.md)

Notes:
- Parser failures should be reported without hiding corpus gaps.
- Re-ingestion must avoid duplicate logical chunks.
- Current implementation is PDF-first extraction plus LangChain/Chroma indexing from emitted chunks.
- Indexing converts chunk records to LangChain `Document` objects, embeds with `langchain-openai`, and persists through `langchain-chroma`.
- Command: `uv run python -m sas_rag.ingestion.cli ingest-pdfs --source-dir docs/sas-documents --whitelist data/source_whitelist.json --out data/ingestion/runs/latest`
- Outputs: normalized Markdown per source, `chunks.jsonl`, and `report.json`.
- Chunk metadata includes `chunk_id`, `source_uri`, `title`, `version`, `section_path`, `source_type`, `content_hash`, `page`, `source_family`, `local_path`, and `priority`.
- First run loaded all 22 local SAS PDFs with 0 failed sources.
- Chroma indexing must keep the same metadata fields on each LangChain document so citations and filters work after retrieval.
- First Chroma run indexed only P0 chunks into a fresh `sas_94_docs` collection.
- Index report: 17,135 total chunks, 8,953 indexed P0 chunks, 8,182 skipped non-P0 chunks.
- Current implementation modules: `pipeline.py` for PDF parse/chunk artifacts and `chroma_index.py` for LangChain/Chroma persistence.
- Test coverage includes whitelist validation, stable chunk IDs, provenance metadata, priority filtering, fake-embedding Chroma indexing, query smoke behavior, and missing API-key failure.
