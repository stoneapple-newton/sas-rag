# Chunking Strategy

Chunking should preserve SAS-native structure before falling back to generic size-based splitting.

Source:
- [SAS RAG Docs](sas-rag-docs.md)
- [Chunking Research](chunking-research.md)

Related stories:
- [CHUNK-001](../../safe/enabler/CHUNK-001-implement-heading-aware-documentation-chunking.md)
- [CHUNK-002](../../safe/enabler/CHUNK-002-implement-sas-aware-code-boundary-detection.md)
- [CHUNK-003](../../safe/feature/CHUNK-003-persist-chunk-ids-and-source-section-paths.md)

Notes:
- Use parent-child hierarchical chunking as the default: parent chunks are logical pages or major sections; child chunks are smaller retrievable units.
- Use semantic boundaries before token limits. Token fallback is only for oversized sections after structure has been preserved.
- Documentation chunks should follow heading hierarchy and retain `section_path` for citations.
- Keep code fences, syntax blocks, tables, and nearby explanatory prose with the section or example they explain.
- SAS examples should preserve primary code blocks: `PROC ... RUN;`, `PROC ... QUIT;`, `DATA ... RUN;`, `%MACRO ... %MEND;`, and DS2 package/method/class bodies.
- Model chunk types explicitly: `concept`, `syntax`, `argument`, `option_table`, `example`, `proc`, `data_step`, `macro`, `ds2`, `troubleshooting`, `migration`, and `reference_object`.
- Build three retrieval indexes or collections: SAS reference, SAS concept/tutorial, and SAS code/example.
- Add atomic reference-object chunks for SAS language elements such as procedures, statements, functions, call routines, macro statements, macro functions, formats, informats, and options.
- Use hybrid dense + keyword retrieval with reranking and parent-context expansion because SAS queries are often exact-name-heavy.
- Tag every chunk with product/version/source priority metadata; version-sensitive answers should not mix SAS 9.4, Viya 3.5, and current Viya material silently.
- For PDFs, normalize to Markdown before chunking so headings, lists, tables, links, and code examples survive extraction.

Default sizes:
- Syntax/reference: 250-600 token child chunks; full page or major heading as parent; 0-80 overlap.
- Concept docs: 500-900 token child chunks; 1,500-2,500 token parent chunks; 80-150 overlap.
- White papers: 700-1,200 token child chunks; section or page-group parent chunks; 100-200 overlap.
- Code examples: one complete example; no arbitrary token split.
- SAS codebase: one DATA/PROC/macro block; dependency-based expansion for setup statements.
- Option tables: one option or 5-10 rows; never split a row.

Boundary rules:
- `concept`: split at heading/subheading boundaries.
- `syntax`: keep exact syntax section together for statements, functions, formats, macros, and procedures.
- `argument`: keep each required or optional argument definition whole; group only when entries are small.
- `option_table`: chunk by option or by row group; never split a row.
- `example`: keep intro prose, full code example, comments, and result notes together.
- `proc`: keep `PROC <name>` through matching `RUN;` or `QUIT;`.
- `data_step`: keep `DATA` through terminating `RUN;`.
- `macro`: keep `%MACRO` through `%MEND`.
- `ds2`: keep package, method, and class boundaries intact.
- `troubleshooting`: keep one symptom, fix, and context together.
- `migration`: keep one versioned issue or migration path per chunk.
- `reference_object`: structured object for exact lookup, including object type, name, aliases, syntax, arguments/options, valid context, version, section path, and source URL.

Open questions:
- Should the first implementation use separate Chroma collections or one collection with index/category metadata?
- Which reference-object types need dedicated benchmark labels in the first evaluation set?
