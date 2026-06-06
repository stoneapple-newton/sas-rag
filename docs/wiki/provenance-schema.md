# Provenance Schema

Every indexed chunk must be traceable to its official SAS source.

Required fields:
- `chunk_id`
- `source_uri`
- `title`
- `version`
- `section_path`
- `source_type`
- content hash

Related stories:
- [PROV-001](../../safe/enabler/PROV-001-define-chunk-provenance-metadata-schema.md)
- [PROV-002](../../safe/feature/PROV-002-attach-provenance-to-every-emitted-chunk.md)
- [PROV-003](../../safe/feature/PROV-003-validate-provenance-completeness-during-ingestion.md)

Notes:
- Provenance powers filtering, citations, benchmark labels, and MCP outputs.
- The PDF ingestion run uses SHA-256 source file hashes as `content_hash`.
- `source_uri` currently stores the repo-relative local PDF path, matching the ING-001 whitelist policy.
- Page-level chunks set `section_path` to `<title> > Page <n>` until richer PDF heading extraction is added.
