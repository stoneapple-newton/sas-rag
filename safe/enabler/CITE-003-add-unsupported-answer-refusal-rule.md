# CITE-003 - Add Unsupported-Answer Refusal Rule

Type: Enabler Story
Parent: [Citation Assembler](../feature-citation-assembler.md)
Capability: Retrieval and grounding
Sprint: Gamma
Points: 3
Status: Proposed
Dependencies: CITE-002, EVAL-001
Wiki: [Citation Grounding](../../docs/wiki/citation-grounding.md), [Evaluation Benchmark](../../docs/wiki/evaluation-benchmark.md)

## Story

As a user, I want the assistant to refuse unsupported SAS answers, so that it does not fabricate behavior when evidence is weak.

## Detail

Define and implement the rule for insufficient evidence. The system should prefer a clear refusal over an uncited or weakly grounded explanation.

## Acceptance Criteria

- Composer can return an insufficient-evidence response.
- Refusal response includes the query and any closest available sources when useful.
- Benchmark includes unsupported or weakly supported SAS questions.

## Implementation Notes

- Refusal logic should be testable.
- Keep response style consistent across MCP tools.
- Do not hide useful nearby official sources when they are relevant but insufficient.

## Done Evidence

- Unsupported-answer test.
- Example refusal response.
- Benchmark cases labeled for insufficient evidence.
