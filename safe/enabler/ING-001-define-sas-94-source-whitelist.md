# ING-001 - Define SAS 9.4 Source Whitelist

Type: Enabler Story
Parent: [Official SAS Docs Ingestion](../feature-official-sas-docs-ingestion.md)
Capability: Corpus ingestion and provenance
Sprint: Alpha
Points: 3
Status: Proposed
Dependencies: None
Wiki: [SAS Corpus](../../docs/wiki/sas-corpus.md)

## Story

As the product and tech lead, I want a frozen PI source whitelist, so that ingestion scope and benchmark expectations do not drift during the PI.

## Detail

Define the authoritative SAS 9.4 source set for PI 1. This enabler keeps ingestion focused on official SAS documentation and prevents community or third-party sources from entering the first benchmark.

## Acceptance Criteria

- Whitelist includes official SAS 9.4 documentation families for macro, SQL procedure, DATA step, language concepts, and base programming coverage.
- Each source entry has title, source URI, source family, SAS version, priority, and ingestion status.
- Non-official and community sources are explicitly out of scope for PI 1.

## Implementation Notes

- Favor stable official documentation over broad coverage.
- Include enough source metadata to support provenance and re-ingestion stories.
- Keep rights and source policy notes in the wiki.

## Done Evidence

- Source whitelist document or dataset.
- Wiki note explaining PI 1 corpus policy.
- Review note confirming SAS 9.4-only scope.
