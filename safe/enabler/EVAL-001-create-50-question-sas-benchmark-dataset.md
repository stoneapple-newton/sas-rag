# EVAL-001 - Create 50-Question SAS Benchmark Dataset

Type: Enabler Story
Parent: [Benchmark Dataset](../enabler-benchmark-dataset.md)
Capability: Retrieval and grounding
Sprint: Beta
Points: 8
Status: Done
Dependencies: ING-001, PROV-001
Wiki: [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md), [SAS Corpus](../../docs/wiki/sas-corpus.md)

## Story

As a product and tech lead, I want a curated SAS benchmark dataset, so that demos and quality gates use representative questions.

## Detail

Create the first benchmark question set for SAS 9.4 retrieval and grounding. The dataset should reflect the P0 corpus and include positive and insufficient-evidence cases.

## Acceptance Criteria

- Dataset contains at least 50 SAS questions covering macro, PROC SQL, DATA step, language concepts, and base programming.
- Each question has expected source family or expected supporting chunk labels where available.
- Dataset includes at least five unsupported or weak-evidence questions.

## Implementation Notes

- Keep questions stable after baseline selection.
- Prefer questions with clear official source support.
- Include metadata for topic, difficulty, and expected evidence when available.

## Done Evidence

- Dataset file or documented location.
- Topic coverage summary.
- Review notes for unsupported questions.
