# Wiki Style

## Goal

Maintain a concise, linked, Karpathy-style Markdown wiki under `docs/wiki/`.

## Page Shape

Use this shape for new pages:

```md
# Page Title

One-sentence purpose or status.

Related:
- [Related Page](related-page.md)
- [Story ID](../../safe/feature/STORY-file.md)

Notes:
- Dense note.
- Dense note.

Open questions:
- Question if useful.
```

## Style Rules

- Keep pages short.
- Prefer bullets over long prose.
- Link aggressively to related wiki pages and SAFe stories.
- Keep one concept per page.
- Put source extracts, copied notes, transcripts, or uncurated research in `docs/raw/`.
- Put conclusions, decisions, and reusable project knowledge in `docs/wiki/`.

## Raw Import Rules

When curating from `docs/raw/`:
- Summarize, do not bulk-copy long raw material.
- Add a source backlink to the raw file.
- Preserve important terms, URLs, and decisions.
- Add related story links when obvious.
- Record the import in `docs/log.md`.

## README Rules

`docs/wiki/README.md` is the topic index.

- Add every new wiki page to the index.
- Keep link text human-readable.
- Do not include raw files in the wiki index unless the page is intentionally about raw-source inventory.
