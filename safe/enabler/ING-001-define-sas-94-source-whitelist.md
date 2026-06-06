# ING-001 - Define SAS 9.4 Source Whitelist

Type: Enabler Story
Parent: [Official SAS Docs Ingestion](../feature-official-sas-docs-ingestion.md)
Capability: Corpus ingestion and provenance
Sprint: Alpha
Points: 3
Status: Done
Dependencies: None
Wiki: [SAS Corpus](../../docs/wiki/sas-corpus.md)

## Story

As the product and tech lead, I want a frozen PI source whitelist, so that ingestion scope and benchmark expectations do not drift during the PI.

## Detail

Define the authoritative SAS 9.4 source set for PI 1. This enabler keeps ingestion focused on official SAS documentation and prevents community or third-party sources from entering the first benchmark.

The current whitelist is the local PDF corpus under `docs/sas-documents/`. Local paths are the authoritative source URI for this ingestion run; upstream SAS URLs remain a follow-up enrichment.

Machine-readable source inventory: `data/source_whitelist.json`.

## Whitelist Summary

| Source ID | Local PDF | Family | Priority | Status |
|---|---|---|---|---|
| acpcref | `docs/sas-documents/acpcref.pdf` | access | P1 | Loaded |
| acreldb | `docs/sas-documents/acreldb.pdf` | access | P1 | Loaded |
| ds2pg | `docs/sas-documents/ds2pg.pdf` | ds2 | P1 | Loaded |
| ds2ref | `docs/sas-documents/ds2ref.pdf` | ds2 | P1 | Loaded |
| graphref | `docs/sas-documents/graphref.pdf` | graph | P1 | Loaded |
| gridref | `docs/sas-documents/gridref.pdf` | grid | P1 | Loaded |
| lebaseutilref | `docs/sas-documents/lebaseutilref.pdf` | base-utilities | P0 | Loaded |
| lecompobjref | `docs/sas-documents/lecompobjref.pdf` | language-reference | P1 | Loaded |
| ledsoptsref | `docs/sas-documents/ledsoptsref.pdf` | language-reference | P0 | Loaded |
| leforinforref | `docs/sas-documents/leforinforref.pdf` | language-reference | P0 | Loaded |
| lefunctionsref | `docs/sas-documents/lefunctionsref.pdf` | language-reference | P0 | Loaded |
| lepg | `docs/sas-documents/lepg.pdf` | language-concepts | P0 | Loaded |
| lestmtsglobal | `docs/sas-documents/lestmtsglobal.pdf` | language-reference | P0 | Loaded |
| lestmtsref | `docs/sas-documents/lestmtsref.pdf` | data-step | P0 | Loaded |
| lesysoptsref | `docs/sas-documents/lesysoptsref.pdf` | language-reference | P0 | Loaded |
| logug | `docs/sas-documents/logug.pdf` | base-programming | P1 | Loaded |
| mcrolref | `docs/sas-documents/mcrolref.pdf` | macro | P0 | Loaded |
| movefile | `docs/sas-documents/movefile.pdf` | base-programming | P1 | Loaded |
| odsgs | `docs/sas-documents/odsgs.pdf` | ods | P1 | Loaded |
| proc | `docs/sas-documents/proc.pdf` | procedures | P0 | Loaded |
| procstat | `docs/sas-documents/procstat.pdf` | stat-procedures | P1 | Loaded |
| sqlproc | `docs/sas-documents/sqlproc.pdf` | proc-sql | P0 | Loaded |

## Acceptance Criteria

- Whitelist includes official SAS 9.4 documentation families for macro, SQL procedure, DATA step, language concepts, and base programming coverage.
- Each source entry has title, source URI, source family, SAS version, priority, and ingestion status.
- Non-official and community sources are explicitly out of scope for PI 1.

## Implementation Notes

- Favor stable official documentation over broad coverage.
- Include enough source metadata to support provenance and re-ingestion stories.
- Keep rights and source policy notes in the wiki.
- The first run used local PDFs as `source_uri` values because verified upstream SAS URLs were not yet captured.
- P0 sources cover macro, PROC SQL, DATA step, language concepts, statements, functions, formats/informats, system options, data set options, and Base procedures.

## Done Evidence

- Source whitelist dataset: `data/source_whitelist.json`.
- Wiki note explaining PI 1 corpus policy: [SAS Corpus](../../docs/wiki/sas-corpus.md).
- Ingestion report: `data/ingestion/runs/latest/report.json`.
- Run result: 22 PDFs loaded, 16,698 pages parsed, 17,135 chunks emitted, 0 failed sources.
- Scope review: PI 1 remains official SAS 9.4 PDFs only; community and third-party sources are excluded.
