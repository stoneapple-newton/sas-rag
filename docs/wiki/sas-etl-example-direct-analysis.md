# SAS ETL Example Direct Analysis

Direct, no-RAG analysis of `sas-test-code/sas-etl-example.sas` for side-by-side comparison.

Related:
- [SAS ETL Example Analysis](sas-etl-example-analysis.md)
- [MCP Server](mcp-server.md)
- [Tool Contracts](tool-contracts.md)
- [Retrieval Architecture](retrieval-architecture.md)

SAFe:
- [MCP-004](../../safe/feature/MCP-004-add-explain-sas-code-tool-using-retrieved-evidence.md)
- [CITE-002](../../safe/feature/CITE-002-assemble-grounded-answer-context-with-source-links.md)

## Summary

The program is a SAS macro-based ETL that builds OHDSI CDM v5-style views from CMS VRDC source tables. It targets four CDM-style outputs:

| Output | Source data | Purpose |
|---|---|---|
| `PERSON` | `BENE_CC.MBSF_AB_<year>` | Beneficiary demographics |
| `DRUG_EXPOSURE` | `PDE` / `PDESAF` Part D files | Prescription drug events |
| `DEATH` | `MBSF_AB_<year>` | Death records |
| `OBSERVATION_PERIOD` | `MBSF_D_<year>` | Part D enrollment-derived coverage periods |

## Flow

- Defines macro constants for years, libraries, PDE suffixes, and Part D enrollment rules.
- Defines ETL macros for each target CDM table.
- Executes the ETL macros to create SAS SQL views.
- Defines and runs `%test_etl(42, 10000000)` to sample beneficiaries, materialize views into tables, and count unique people.
- Drops the ETL views afterward as a safety measure.

## Key Macros

- `%etl_person`: creates `PERSON` by unioning annual beneficiary summary files, joining to gender, race, ethnicity, and beneficiary inclusion maps.
- `%etl_drug_exposure`: creates `DRUG_EXPOSURE` from Part D Event files, using `PDE_ID` as the exposure id and preserving `PROD_SRVC_ID` as the source drug value.
- `%etl_death`: creates `DEATH` from non-null `BENE_DEATH_DT` records across annual beneficiary files.
- `%etl_observation_period`: creates Part D-only observation periods, with annual rows for full-year coverage and monthly rows for partial-year coverage.
- `%test_etl`: builds a beneficiary sample, materializes views, and reports person counts across output tables.
- `%drop_all_etl_views`: removes the generated ETL views after testing.

## Data Lineage

| Target field | Derived from |
|---|---|
| `person.person_id` | `BENE_ID` |
| `person.gender_concept_id` | `vc5_gender_map` |
| `person.year_of_birth`, `month_of_birth`, `day_of_birth` | `BENE_BIRTH_DT` |
| `person.race_concept_id` | `vc5_race_map` |
| `person.ethnicity_concept_id` | `vc5_ethnicity_map` |
| `drug_exposure.drug_exposure_id` | `PDE_ID` |
| `drug_exposure.drug_exposure_start_date` | `SRVC_DT` |
| `drug_exposure.days_supply` | `DAYS_SUPLY_NUM` |
| `drug_exposure.drug_source_value` | `PROD_SRVC_ID` |
| `death.death_date` | `BENE_DEATH_DT` |
| `observation_period` dates | Part D enrollment year/month logic |

## Risks and Gaps

- Many CDM concept fields are hardcoded to `0`, especially drug and death type concepts.
- `OBSERVATION_PERIOD` only uses Part D enrollment; Parts A and B are explicitly excluded.
- `observation_period_id` is always `0`, which is unsuitable for a finalized materialized CDM table requiring unique ids.
- `DRUG_EXPOSURE` does not map `PROD_SRVC_ID` to standard drug concepts such as RxNorm.
- `PERSON` uses `union` across years; exact duplicates collapse, but conflicting demographic rows for the same person can survive.
- `DEATH` also unions across years; conflicting death dates would survive.
- The program depends on external SAS libraries: `BENE_CC`, `FKU838SL`, and `IN026250`.
- SQL views defer computation; opening a view can trigger large ETL execution.
- The test macro validates rough row/person presence, but not CDM uniqueness, date constraints, concept mapping, or referential integrity.

## Assessment

This is a readable macro-driven prototype for converting selected CMS VRDC data into partial OHDSI CDM v5 structures. It is useful as an ETL example because it shows macro iteration, multi-year source unioning, PROC SQL view creation, sampling, and materialization.

It is not production-complete CDM ETL. The main gaps are incomplete concept mapping, placeholder ids, limited observation-period logic, hardcoded library configuration, and weak validation.
