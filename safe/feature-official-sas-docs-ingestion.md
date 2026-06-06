# Official SAS Docs Ingestion

Type: Feature
Capability: Corpus ingestion and provenance
Priority: P0
Sprint target: Alpha/Beta
Owner role: Data Engineer
Status: In Progress
Dependencies: None

## Intent

Load prioritized official SAS 9.4 documentation into the ingestion pipeline with repeatable source tracking and enough coverage to support the first retrieval benchmark. Indexing will use LangChain `Document` objects, configurable OpenAI embeddings, and persistent local Chroma via `langchain-chroma`.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| ING-001 | Enabler | Define SAS 9.4 source whitelist | 3 | Alpha | None |
| ING-002 | Feature | Ingest one official SAS doc family end to end | 5 | Alpha | ING-001, PARSE-001, PROV-001 |
| ING-003 | Feature | Ingest prioritized SAS 9.4 docs batch | 8 | Beta | ING-002, PARSE-002, PROV-002 |
| ING-004 | Enabler | Add checksum and re-ingestion controls | 5 | Beta | ING-002, PROV-002 |

## Story Details

### ING-001 - Define SAS 9.4 source whitelist

As the product and tech lead, I want a frozen PI source whitelist, so that ingestion scope and benchmark expectations do not drift during the PI.

Acceptance criteria:
- Whitelist includes official SAS 9.4 documentation families needed for macro, SQL procedure, DATA step, language concepts, and base programming coverage.
- Each source entry has title, source URI, source family, SAS version, priority, and ingestion status.
- Non-official and community sources are explicitly out of scope for PI 1.

Current evidence:
- `data/source_whitelist.json` defines the 22 local SAS PDF sources under `docs/sas-documents/`.
- The first PDF ingestion run loaded all 22 sources and emitted 17,135 chunks from 16,698 parsed pages.
- Local PDF paths are used as the source URI for this run; upstream official SAS URLs are a follow-up enrichment.

### ING-002 - Ingest one official SAS doc family end to end

As a data engineer, I want one official SAS documentation family to ingest end to end, so that the pipeline proves source loading, parsing, chunking, embedding, and persistence before scaling out.

Acceptance criteria:
- One whitelisted SAS 9.4 doc family is loaded from local or configured source input.
- Pipeline emits chunks with provenance metadata and stable chunk IDs.
- Chunks are converted to LangChain `Document` records and written to the local Chroma index without duplicate records on a rerun.
- A short demo query retrieves content from the ingested source.

### ING-003 - Ingest prioritized SAS 9.4 docs batch

As a SAS RAG user, I want prioritized SAS 9.4 documentation indexed, so that common SAS questions can be answered from official sources.

Acceptance criteria:
- Prioritized P0 source families from ING-001 are ingested.
- P0 chunks are embedded through LangChain and persisted to local Chroma.
- Parse failure rate is reported and remains below the PI threshold for prioritized sources.
- Ingestion report lists loaded, skipped, failed, and unchanged sources.
- Retrieval smoke test covers at least macro, PROC SQL, DATA step, and language reference topics.

### ING-004 - Add checksum and re-ingestion controls

As a data engineer, I want checksum-based re-ingestion controls, so that unchanged sources are not repeatedly duplicated or needlessly reprocessed.

Acceptance criteria:
- Source checksum or content hash is captured during ingestion.
- Unchanged source reruns are detected and reported.
- Changed sources can be reprocessed while preserving traceability to prior chunk versions.
- Duplicate chunk creation is prevented in local persisted Chroma runs.

## Definition of Done

- Stories pass their acceptance criteria.
- Ingestion command and source whitelist are documented.
- Sample retrieval demonstrates indexed official SAS 9.4 content.
- Ingestion failures are visible in a report or log.
