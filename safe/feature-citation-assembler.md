# Citation Assembler

Type: Feature
Capability: Retrieval and grounding
Priority: P0
Sprint target: Beta/Gamma
Owner role: ML/RAG Engineer
Status: Proposed
Dependencies: RET-001, PROV-002

## Intent

Ensure answers are grounded in retrieved SAS documentation and include citations that resolve back to official source chunks.

## Stories

| ID | Type | Title | Points | Sprint | Dependencies |
|---|---|---|---:|---|---|
| CITE-001 | Feature | Return citations from retrieved chunks | 5 | Beta | RET-001, PROV-002 |
| CITE-002 | Feature | Assemble grounded answer context with source links | 5 | Gamma | CITE-001, RET-002 |
| CITE-003 | Enabler | Add unsupported-answer refusal rule | 3 | Gamma | CITE-002, EVAL-001 |

## Story Details

### CITE-001 - Return citations from retrieved chunks

As a SAS RAG user, I want search results to include citations, so that I can verify the official source behind each answer.

Acceptance criteria:
- Retrieval results include source title, source URI, version, section path, and chunk ID.
- Citation fields are generated from provenance rather than prompt-only text.
- Missing citation metadata fails validation before answer assembly.

### CITE-002 - Assemble grounded answer context with source links

As a coding agent, I want answer context assembled with source links, so that generated explanations stay tied to retrieved SAS evidence.

Acceptance criteria:
- Answer composer receives only retrieved evidence and citation metadata needed for the response.
- Final answer includes citations for supported claims.
- Citation format is consistent across MCP tools.

### CITE-003 - Add unsupported-answer refusal rule

As a user, I want the assistant to refuse unsupported SAS answers, so that it does not fabricate behavior when evidence is weak.

Acceptance criteria:
- Composer can return an insufficient-evidence response.
- Refusal response includes the query and any closest available sources when useful.
- Benchmark includes unsupported or weakly supported SAS questions.

## Definition of Done

- Citation metadata resolves to indexed chunks.
- Answers either cite evidence or refuse.
- Citation accuracy is measured in evals once EVAL-002 is available.
