# SAFe File Structure

## Canonical Layout

- `safe/Overall-structure.md` - roadmap and source PI plan.
- `safe/README.md` - PI assumptions, feature/enabler backlog, sprint map, Definition of Done.
- `safe/feature-*.md` - parent feature files.
- `safe/enabler-*.md` - parent enabler files.
- `safe/feature/README.md` - index of individual feature stories.
- `safe/enabler/README.md` - index of individual enabler stories.
- `safe/feature/<ID>-<slug>.md` - individual feature story.
- `safe/enabler/<ID>-<slug>.md` - individual enabler story.

## SAFe Hierarchy

Use this hierarchy consistently:

Epic -> Capability -> Feature/Enabler -> Story

Parent feature/enabler files should identify:
- type
- capability
- priority
- sprint target
- owner role
- status
- dependencies
- intent
- child story table
- story details
- Definition of Done

## Individual Story Schema

Every individual story file must include:

```md
# <ID> - <Title>

Type: Feature Story | Enabler Story
Parent: [Parent Name](../parent-file.md)
Capability: <capability>
Sprint: Alpha | Beta | Gamma | Delta
Points: <number>
Status: Proposed | Ready | In Progress | Done | Blocked
Dependencies: <IDs or None>
Wiki: [Topic](../../docs/wiki/topic.md)

## Story

As a <role>, I want <capability>, so that <outcome>.

## Detail

<implementation-neutral detail>

## Acceptance Criteria

- ...

## Implementation Notes

- ...

## Done Evidence

- ...
```

## Naming

- Preserve story IDs exactly.
- Use filenames shaped as `<ID>-<lowercase-hyphen-slug>.md`.
- Put feature stories in `safe/feature/`.
- Put enabler stories in `safe/enabler/`.

## Maintenance Rules

- Update the parent story table when adding or removing a child story.
- Update `safe/feature/README.md` or `safe/enabler/README.md` when adding or renaming individual story files.
- Update `safe/README.md` when sprint assignment, PI assumptions, or the parent backlog changes.
- Keep wiki links valid.
