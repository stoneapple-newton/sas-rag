# Benchmark Dataset

Type: Enabler
Capability: Retrieval and grounding
Priority: P0
Sprint target: Beta/Delta
Owner role: QA/Automation Engineer
Status: Proposed
Dependencies: ING-001, PROV-001

## Intent

Create a stable benchmark so retrieval, citation, and answer-quality regressions are measurable instead of subjective.

## Stories

| ID       | Type    | Title                                     | Points | Sprint | Dependencies                |
| -------- | ------- | ----------------------------------------- | -----: | ------ | --------------------------- |
| EVAL-001 | Enabler | Create 50-question SAS benchmark dataset  |      8 | Beta   | ING-001, PROV-001           |
| EVAL-002 | Enabler | Add recall@5 and citation accuracy checks |      5 | Gamma  | EVAL-001, RET-002, CITE-001 |
| EVAL-003 | Enabler | Add regression threshold report           |      3 | Delta  | EVAL-002, OBS-002           |

## Story Details

### EVAL-001 - Create 50-question SAS benchmark dataset

As a product and tech lead, I want a curated SAS benchmark dataset, so that demos and quality gates use representative questions.

Acceptance criteria:
- Dataset contains at least 50 SAS questions covering macro, PROC SQL, DATA step, language concepts, and base programming.
- Each question has expected source family or expected supporting chunk labels where available.
- Dataset includes at least five unsupported or weak-evidence questions.

### EVAL-002 - Add recall@5 and citation accuracy checks

As a QA engineer, I want automated retrieval and citation checks, so that quality can be compared across chunking, embedding, and prompt changes.

Acceptance criteria:
- Eval reports recall@5 for labeled questions.
- Eval reports citation accuracy or citation-support pass rate.
- Eval output is usable in CI and LangSmith experiment review.

### EVAL-003 - Add regression threshold report

As a release owner, I want regression thresholds reported, so that quality drops are visible before release.

Acceptance criteria:
- Report compares current results to the chosen baseline.
- Report flags core metric drops above the agreed PI threshold.
- Delta sprint release candidate includes the report as demo evidence.

## Definition of Done

- Benchmark dataset is versioned in the repo or documented data location.
- Eval commands are documented.
- Metrics are used in release readiness discussion.
