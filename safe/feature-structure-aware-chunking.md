# Structure-Aware Chunking

Type: Feature
Capability: Retrieval and grounding
Priority: P0
Sprint target: Beta
Owner role: ML/RAG Engineer
Status: Proposed
Dependencies: PARSE-002, PROV-002

## Intent

Chunk SAS documentation and examples around meaningful boundaries so retrieval preserves definitions, procedure guidance, DATA step logic, macros, and nearby explanatory comments.

Curated guidance:
- Use parent-child hierarchical chunking as the default for official docs.
- Chunk semantically before applying token-size fallback.
- Maintain a chunk taxonomy for `concept`, `syntax`, `argument`, `option_table`, `example`, `proc`, `data_step`, `macro`, `ds2`, `troubleshooting`, `migration`, and `reference_object`.
- Keep SAS reference, concept/tutorial, and code/example chunks separable in retrieval so exact syntax, explanations, and examples can rank differently.
- Add atomic reference-object chunks for procedures, statements, functions, macro elements, options, formats, and informats.
- Preserve product/version/source-priority metadata on every emitted chunk.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| CHUNK-001 | Enabler | Implement heading-aware documentation chunking | 5 | Beta | PARSE-002, PROV-002 |
| CHUNK-002 | Enabler | Implement SAS-aware code boundary detection | 8 | Beta | PARSE-002 |
| CHUNK-003 | Feature | Persist chunk IDs and source section paths | 3 | Beta | CHUNK-001, PROV-001 |

## Story Details

### CHUNK-001 - Implement heading-aware documentation chunking

As a SAS RAG user, I want documentation chunks aligned to headings, so that retrieved passages contain coherent source context.

Acceptance criteria:
- Chunker splits documentation on heading hierarchy before size fallback.
- Chunk size limits are configurable.
- Section path from parser output is preserved in chunk metadata.
- Oversized heading sections are split only after preserving syntax blocks, tables, examples, and citation context.
- Parent/child chunk sizes support documented defaults for syntax/reference, concept docs, white papers, code examples, and option tables.

### CHUNK-002 - Implement SAS-aware code boundary detection

As a coding agent, I want SAS examples chunked by SAS-native boundaries, so that explanations do not mix unrelated procedures, DATA steps, or macros.

Acceptance criteria:
- Boundary detection recognizes `PROC ... RUN;`, `PROC ... QUIT;`, `DATA ... RUN;`, and `%MACRO ... %MEND;`.
- Boundary detection recognizes DS2 package, method, and class bodies well enough to avoid splitting obvious DS2 examples.
- Nearby comments stay with the code block they explain.
- Unit cases cover PROC, DATA step, macro, and mixed prose/code examples.
- Setup statements such as `LIBNAME`, `FILENAME`, `OPTIONS`, and `ODS` are attached to the following code chunk as dependency metadata when applicable.

### CHUNK-003 - Persist chunk IDs and source section paths

As a retrieval engineer, I want stable chunk IDs and section paths, so that citations and benchmark labels survive repeated indexing.

Acceptance criteria:
- Chunk IDs remain stable for unchanged source content and section context.
- Section paths are stored in vector metadata.
- Chunk metadata stores chunk type and product/version/source-priority fields.
- Chunk metadata stores section type, SAS object type/name, keywords, valid context, and parent chunk reference when available.
- Re-indexing the same source does not create duplicate logical chunks.

## Definition of Done

- Documentation and SAS-aware chunking tests pass.
- Representative SAS examples are manually inspected.
- Benchmark smoke retrieval does not regress after chunking changes.
