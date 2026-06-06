---
name: safe-wiki-manager
description: Maintain the SAS RAG MCP project's SAFe Markdown backlog and Karpathy-style docs wiki. Use when Codex needs to create, update, review, reorganize, or validate files under safe/, safe/feature/, safe/enabler/, docs/raw/, docs/wiki/, docs/README.md, or docs/log.md, including curated imports from docs/raw/ into docs/wiki/.
---

# SAFe Wiki Manager

Use this skill for planning and documentation work in the SAS RAG MCP repo.

## Core Workflow

1. Inspect the relevant `safe/`, `docs/raw/`, `docs/wiki/`, and `docs/log.md` files before editing.
2. Preserve existing story IDs, parent links, sprint assignments, and wiki links unless the user explicitly asks to change planning structure.
3. Keep SAFe planning content under `safe/` and curated knowledge under `docs/wiki/`.
4. Record meaningful documentation changes and raw-to-wiki imports in `docs/log.md`.
5. Validate links and indexes after creating or renaming files.

## Project Structure

- `safe/Overall-structure.md` - source PI plan and roadmap.
- `safe/README.md` - PI backlog index, assumptions, sprint map, and Definition of Done.
- `safe/feature-*.md` - parent feature planning files.
- `safe/enabler-*.md` - parent enabler planning files.
- `safe/feature/*.md` - individual feature story files.
- `safe/enabler/*.md` - individual enabler story files.
- `docs/raw/` - uncurated source notes and research captures.
- `docs/wiki/` - concise, linked, Karpathy-style wiki pages.
- `docs/README.md` - documentation area guide.
- `docs/log.md` - documentation changes, imports, decisions, and follow-ups.

## SAFe Rules

Read `references/safe-file-structure.md` when creating or restructuring SAFe files.

- Preserve hierarchy: Epic -> Capability -> Feature/Enabler -> Story.
- Use parent feature/enabler files for planning summaries and child story tables.
- Use `safe/feature/` and `safe/enabler/` for individual story files.
- Individual story files must include: type, parent, capability, sprint, points, status, dependencies, wiki links, story, acceptance criteria, implementation notes, and done evidence.
- Keep story IDs stable. Do not renumber IDs to make files prettier.

## Wiki Rules

Read `references/wiki-style.md` when creating or rewriting wiki pages.

- Follow a Karpathy-style wiki: short pages, dense notes, strong links.
- Keep raw copied material in `docs/raw/`.
- Put curated project knowledge in `docs/wiki/`.
- Link wiki pages to related SAFe stories when the page supports planning or implementation.
- Prefer one topic per page.

## Raw Import

Use `scripts/import_raw_to_wiki.py` for deterministic Markdown/text imports:

```powershell
python .agents/skills/safe-wiki-manager/scripts/import_raw_to_wiki.py --dry-run
python .agents/skills/safe-wiki-manager/scripts/import_raw_to_wiki.py --write
```

The script:
- Reads `.md` and `.txt` files from `docs/raw/`.
- Creates curated starter pages in `docs/wiki/`.
- Adds source backlinks to raw files.
- Updates `docs/wiki/README.md`.
- Appends import entries to `docs/log.md`.

Default to dry-run before write. For PDF or binary sources, use a document/PDF extraction workflow first, save text or Markdown into `docs/raw/`, then import.
