# Retrieval Architecture

PI 1 retrieval combines semantic search, metadata filters, and lexical fallback for exact SAS identifiers.

Related stories:
- [RET-001](../../safe/feature/RET-001-create-chroma-backed-vector-index.md)
- [RET-002](../../safe/feature/RET-002-add-semantic-search-with-metadata-filters.md)
- [RET-003](../../safe/feature/RET-003-add-lexical-fallback-for-proc-statement-lookup.md)

Notes:
- Retrieval logic should stay separate from MCP transport.
- Results must include citation-ready provenance.
