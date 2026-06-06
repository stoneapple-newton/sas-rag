# SAS Corpus

PI 1 focuses on official SAS 9.4 documentation only.

Related stories:
- [ING-001](../../safe/enabler/ING-001-define-sas-94-source-whitelist.md)
- [ING-002](../../safe/feature/ING-002-ingest-one-official-sas-doc-family-end-to-end.md)
- [ING-003](../../safe/feature/ING-003-ingest-prioritized-sas-94-docs-batch.md)
- [EVAL-001](../../safe/enabler/EVAL-001-create-50-question-sas-benchmark-dataset.md)

Notes:
- Prioritize macro, PROC SQL, DATA step, language concepts, and base programming coverage.
- Defer community and third-party code sources outside PI 1.
- Current local corpus lives in `docs/sas-documents/` and contains 22 PDF files.
- `data/source_whitelist.json` is the machine-readable whitelist for ING-001.
- Local PDF paths are the source URI for the first run; verified upstream SAS URLs can be added later without changing chunk provenance keys.
- First ingestion run: 22 loaded sources, 16,698 parsed pages, 17,135 emitted chunks, 0 failed sources.

P0 families:
- macro: `mcrolref.pdf`
- proc-sql: `sqlproc.pdf`
- data-step/language reference: `lestmtsref.pdf`, `lestmtsglobal.pdf`, `lefunctionsref.pdf`, `leforinforref.pdf`, `lesysoptsref.pdf`, `ledsoptsref.pdf`
- language concepts: `lepg.pdf`
- Base procedures/utilities: `proc.pdf`, `lebaseutilref.pdf`
