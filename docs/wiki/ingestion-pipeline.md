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
