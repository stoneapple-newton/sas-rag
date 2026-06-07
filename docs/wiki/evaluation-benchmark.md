# SAS 9.4 Benchmark Dataset

Curated benchmark questions for evaluating SAS RAG retrieval and grounding quality.

## Dataset Overview

- **Total questions**: 53
- **Supported questions**: 48
- **Unsupported questions**: 5
- **Coverage**: macro, proc-sql, data-step, language-reference, procedures, language-concepts, base-programming

## Topic Distribution

| Topic | Count |
|---|---|
| macro | 9 |
| proc-sql | 9 |
| data-step | 8 |
| language-reference | 10 |
| procedures | 7 |
| language-concepts | 5 |
| unsupported | 5 |

## Difficulty Distribution

| Difficulty | Count |
|---|---|
| beginner | 16 |
| intermediate | 25 |
| advanced | 12 |

## Unsupported Questions

Five intentionally unsupported questions test refusal behavior:
- Quantum computing in SAS
- Blockchain verification in BASE SAS
- PROC TELEPATHY
- Time reversal PROC
- Lottery prediction PROC

## File Location

`data/benchmark/sas_questions.json`

## Current Status

- EVAL-001 is Done.
- EVAL-002 is Ready for Gamma and should add recall@5 plus citation accuracy checks.
- Contract/unit tests currently avoid OpenAI by using fake embeddings; live smoke tests remain manual.

## Schema

Each question entry includes:
- `id`: Unique identifier
- `question`: Query text
- `topic`: Category/topic
- `difficulty`: beginner, intermediate, advanced
- `expected_source_family`: Expected primary source family
- `expected_evidence`: Description of expected supporting evidence
- `unsupported`: Boolean flag for weak-evidence questions
- `notes`: Optional context
