# Retrieval Architecture

PI 1 retrieval combines semantic search, metadata filters, and lexical fallback for exact SAS identifiers.

Related stories:
- [RET-001](../../safe/feature/RET-001-create-chroma-backed-vector-index.md)
- [RET-002](../../safe/feature/RET-002-add-semantic-search-with-metadata-filters.md)
- [RET-003](../../safe/feature/RET-003-add-lexical-fallback-for-proc-statement-lookup.md)

Notes:
- Retrieval logic should stay separate from MCP transport.
- Results must include citation-ready provenance.
- PI 1 semantic retrieval uses LangChain retrievers over persistent Chroma.
- Index construction uses `langchain-chroma` and configurable LangChain embeddings, defaulting to OpenAI.
- Metadata filters should use fields emitted by ingestion: `source_family`, `priority`, `version`, `source_type`, `page`, and `section_path`.
- Exact SAS identifiers still need lexical fallback in addition to Chroma similarity search.
- Current semantic index: P0 SAS corpus in Chroma collection `sas_94_docs`.
- Current smoke query `PROC SQL join syntax` returns PROC SQL join examples with citation metadata.
- 2026-06-07 Chroma refresh confirmed collection `sas_94_docs` at `data/chroma`: 17,135 total chunks, 8,953 P0 chunks already indexed, 8,182 non-P0 chunks skipped.
- 2026-06-07 smoke retrieval completed for macro, DATA step, and language-reference topics, closing ING-003.
- Next retrieval work: lexical fallback for exact PROC and statement names in RET-003.
