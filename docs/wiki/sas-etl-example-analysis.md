# SAS ETL Example Analysis

Analysis target: `sas-test-code/sas-etl-example.sas`

Related:
- [SAS ETL Example Direct Analysis](sas-etl-example-direct-analysis.md)
- [MCP Server](mcp-server.md)
- [Tool Contracts](tool-contracts.md)
- [Citation Grounding](citation-grounding.md)
- [Retrieval Architecture](retrieval-architecture.md)

SAFe:
- [MCP-002](../../safe/feature/MCP-002-add-search-sas-docs-tool.md)
- [MCP-004](../../safe/feature/MCP-004-add-explain-sas-code-tool-using-retrieved-evidence.md)
- [CITE-002](../../safe/feature/CITE-002-assemble-grounded-answer-context-with-source-links.md)

## Summary

The file is a macro-driven SAS ETL program that builds OHDSI CDM v5-style views from CMS VRDC source tables. It defines constants with `%let`, then defines and runs ETL macros for `PERSON`, `DRUG_EXPOSURE`, `DEATH`, and `OBSERVATION_PERIOD`. It also defines `test_etl`, which samples beneficiaries, materializes the views into test tables, reports person counts, and then drops the views through `drop_all_etl_views`.

Compared with the direct no-RAG analysis, this page grounds the SAS-language interpretation in retrieved SAS 9.4 documentation chunks from the project-local MCP server.

## Detected Constructs

- Macros: `etl_person`, `etl_drug_exposure`, `etl_death`, `etl_observation_period`, `test_etl`, `drop_all_etl_views`
- Procedures: `PROC SQL`, `PROC SURVEYSELECT`
- Macro variables: `year_list`, `drug_year_list`, `user_library`, `pde_library`, `pde_file_suffix`, `part_d_enrollment_code`, `part_d_coverage_regex`
- Macro language usage: `%let`, `%macro`, `%mend`, `%do`, `%if`, `%then`, `%scan`, `%sysfunc`, `%eval`
- SAS functions: `countw`, `mdy`, `intnx`, `prxmatch`, `put`, `putn`, `year`, `month`, `day`

## MCP Evidence

The analysis used local static extraction to identify SAS constructs, then called the project-local `sas_rag` MCP server with `search_sas_docs` for official SAS evidence.

Retrieved evidence from the current MCP run:

| Topic | Source | Chunks |
|---|---|---|
| `PROC SQL` create views, unions, joins | SAS SQL Procedure User's Guide | `f4aba1af102ae58216c6eb38`, `fbecfd27182f605fb8d61b4f`, `c6085bc982c226dc02478b87` |
| Macro text generation and `%DO` processing | SAS Macro Language Reference | `e4b7a5819c926bf2835d3ac8`, `0a2b83409579dea5670ea003`, `373c885f4aded6a563496576` |
| `%LET` macro variable behavior | SAS Macro Language Reference | `e71d0a021ddaf7ef578a5df4`, `43303949276f4c7b8b72a9ce` |
| `COUNTW` and scan-style list handling | SAS Functions and CALL Routines Reference; SAS Macro Language Reference | `5a614066e7bf1b1b6ec3aa05`, `0a2b83409579dea5670ea003` |
| `INTNX` interval/date boundary behavior | SAS Formats and Informats Reference; SAS Functions and CALL Routines Reference | `89c45a792af67f0520e1c595`, `3464c2928d9e6740265a1980` |
| `PRXMATCH` regular expression matching | SAS Functions and CALL Routines Reference | `9c579e38566be5b3e0115f52`, `1bbd4b48e0c786d8699bb66f` |

## Interpretation

The program uses SAS macro loops to generate repeated SQL view definitions across multiple claim years. `%scan` and `countw` iterate through year lists, `%sysfunc` bridges DATA step functions into macro logic, and `%if/%then` conditionally emits SQL fragments. The repeated `union` / `union all` patterns combine yearly Medicare source tables into CDM-shaped views.

`PROC SQL` is the main ETL engine. It creates views instead of permanent output tables for the core CDM entities, then the test macro materializes those views into `*_mat` tables for sample validation. `PROC SURVEYSELECT` creates a simple random beneficiary sample for testing.

The observation-period logic uses `mdy` and `intnx` to construct year and month date boundaries. `prxmatch` checks monthly Part D contract identifiers against a macro-configured Perl regular expression.

## MCP-Grounded Table Analysis

| Output | MCP-grounded SAS mechanics | Interpretation |
|---|---|---|
| `PERSON` | `PROC SQL`, joins, macro-generated yearly `UNION` queries | Builds one CDM-shaped demographic view from yearly `MBSF_AB_<year>` tables and local mapping tables. |
| `DRUG_EXPOSURE` | `PROC SQL`, macro `%IF`, `%SCAN`, `UNION ALL` | Builds Part D drug exposure rows from request-specific PDE files and switches naming convention after 2011. |
| `DEATH` | `PROC SQL`, macro-generated yearly `UNION` queries, `WHERE` filtering | Emits death rows for beneficiaries with non-null `BENE_DEATH_DT`. |
| `OBSERVATION_PERIOD` | Macro loops, `MDY`, `INTNX`, `PRXMATCH`, `UNION ALL` | Converts full-year and partial-year Part D enrollment indicators into annual or monthly observation periods. |

## Risks Found

- `observation_period_id` is always `0`; this is acceptable for a view prototype but risky if materialized into a production CDM table requiring unique identifiers.
- `drug_concept_id`, `drug_type_concept_id`, `death_type_concept_id`, and `route_source_value` are hardcoded to `0`, so semantic CDM mapping is incomplete.
- `PERSON` and `DEATH` use `union`, which removes exact duplicates but does not resolve conflicting beneficiary values across years.
- `DRUG_EXPOSURE` assumes `PDE_ID` uniqueness and therefore uses `union all`; this is reasonable only if that source invariant holds.
- Observation periods only reflect Part D enrollment, not Parts A/B.
- The MCP run did not retrieve a clean `PROC SURVEYSELECT` reference from the local index, so the `test_etl` sampling interpretation is based on static code reading rather than a supporting MCP citation in this pass.

## Caveat

The current static analyzer produced one false-positive DATA step detection from prose/comment text. No actual `DATA ... RUN;` block is present in the file. This should be considered when implementing MCP-004 so code parsing filters comments before DATA step detection.
