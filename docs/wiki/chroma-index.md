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
