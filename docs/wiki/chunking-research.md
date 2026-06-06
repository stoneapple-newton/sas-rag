# Chunking Research

Curated from [`docs/raw/Chunking research.md`](../raw/Chunking%20research.md) on 2026-06-06.

Related:
- [Chunking Strategy](chunking-strategy.md)
- [Retrieval Architecture](retrieval-architecture.md)
- [CHUNK-001](../../safe/enabler/CHUNK-001-implement-heading-aware-documentation-chunking.md)
- [CHUNK-002](../../safe/enabler/CHUNK-002-implement-sas-aware-code-boundary-detection.md)
- [CHUNK-003](../../safe/feature/CHUNK-003-persist-chunk-ids-and-source-section-paths.md)

Notes:
- Project standard: parent-child hierarchical chunks + SAS reference-object chunks + code-aware chunks + strong metadata.
- Do not use fixed-size chunking as the primary method for SAS docs; token splitting is only a fallback after structural parsing.
- SAS reference docs commonly contain `Syntax`, `Required Arguments`, `Optional Arguments`, `Details`, `Examples`, PROC/task tables, and reference entries; chunking should use these section types.
- Parent chunks should represent a logical page or major section, roughly 1,200-2,500 tokens.
- Child chunks should be precise retrievable units, roughly 300-700 tokens with 50-100 token overlap.
- Atomic reference chunks should capture exact SAS objects such as `PROC SQL`, `WHERE`, `%MACRO`, `PRXCHANGE`, options, formats, and informats.
- Use three retrieval indexes: SAS reference index, SAS concept/tutorial index, and SAS code/example index.
- Prefer hybrid dense + keyword search, reranking, and parent-context expansion because SAS questions are symbol-heavy and exact-name-heavy.
- Never split syntax blocks, code examples, option table rows, or macro definitions in the middle.
- Attach metadata aggressively: source type, product, version, document title, section path, page title, section type, SAS object type, SAS object name, keywords, valid context, URL, and last-updated date.

Default sizes:
- Syntax/reference pages: 250-600 token child chunks, full page or major heading as parent, 0-80 overlap.
- Concept docs: 500-900 token child chunks, 1,500-2,500 token parent chunks, 80-150 overlap.
- White papers: 700-1,200 token child chunks, section/page-group parent chunks, 100-200 overlap.
- Code examples: one complete example as child, containing doc section as parent, no arbitrary split.
- Local SAS codebase: one DATA/PROC/macro block as child, file/module/job flow as parent, dependency-based expansion.
- Option tables: one option or 5-10 rows as child, full table/section as parent, no row split.

Open questions:
- Should the first implementation use one physical vector store with index metadata, or separate Chroma collections for reference, concept, and code/example indexes?
- Which reference-object types belong in the MVP: procedures, statements, functions, macro statements, macro functions, options, formats, and informats?
