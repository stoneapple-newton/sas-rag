# Citation Grounding

The system should cite official SAS sources or refuse when evidence is insufficient.

Related stories:
- [CITE-001](../../safe/feature/CITE-001-return-citations-from-retrieved-chunks.md)
- [CITE-002](../../safe/feature/CITE-002-assemble-grounded-answer-context-with-source-links.md)
- [CITE-003](../../safe/enabler/CITE-003-add-unsupported-answer-refusal-rule.md)

Notes:
- Citations must be generated from provenance metadata.
- Unsupported answers should be explicit and testable.
- Current retrieval citation helper: `sas_rag.retrieval.search.format_citation()`.
- Current MCP `search_sas_docs` response includes citation fields from provenance metadata.
- CITE-001 is Done; CITE-002 and CITE-003 are Ready for Gamma.
- Unsupported question coverage starts in `data/benchmark/sas_questions.json`.
