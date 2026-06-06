#!/usr/bin/env python3
"""Curate docs/raw Markdown or text files into docs/wiki starter pages."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".txt"}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "raw-note"


def title_from_path(path: Path) -> str:
    words = re.split(r"[-_\s]+", path.stem)
    return " ".join(word.capitalize() for word in words if word) or path.stem


def first_nonempty_lines(text: str, limit: int = 8) -> list[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            line = line.lstrip("#").strip()
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def make_wiki_content(raw_path: Path, wiki_path: Path, root: Path) -> str:
    text = raw_path.read_text(encoding="utf-8")
    title = title_from_path(raw_path)
    notes = first_nonempty_lines(text)
    raw_link = Path(os.path.relpath(raw_path, wiki_path.parent)).as_posix()

    note_lines = "\n".join(f"- {line}" for line in notes) if notes else "- No non-empty raw lines found yet."
    today = dt.date.today().isoformat()
    root_relative_raw = raw_path.relative_to(root).as_posix()

    return f"""# {title}

Curated starter page imported from [`{root_relative_raw}`]({raw_link}) on {today}.

Related:
- [Wiki Index](README.md)

Notes:
{note_lines}

Open questions:
- What conclusions from the raw source should become durable project knowledge?
- Which SAFe stories should this page support?
"""


def update_wiki_index(index_path: Path, wiki_file: Path) -> bool:
    title = title_from_path(wiki_file)
    entry = f"- [{title}]({wiki_file.name})"
    if index_path.exists():
        content = index_path.read_text(encoding="utf-8")
    else:
        content = "# SAS RAG MCP Wiki\n\n"
    if entry in content:
        return False
    if not content.endswith("\n"):
        content += "\n"
    content += entry + "\n"
    index_path.write_text(content, encoding="utf-8")
    return True


def append_log(log_path: Path, imported: list[tuple[Path, Path]]) -> None:
    if not imported:
        return
    today = dt.date.today().isoformat()
    if log_path.exists():
        content = log_path.read_text(encoding="utf-8")
    else:
        content = "# Documentation Log\n"
    if not content.endswith("\n"):
        content += "\n"
    content += f"\n## {today}\n\n"
    for raw_path, wiki_path in imported:
        content += f"- Imported `{raw_path.as_posix()}` into `{wiki_path.as_posix()}`.\n"
    log_path.write_text(content, encoding="utf-8")


def discover_raw_files(raw_dir: Path) -> list[Path]:
    if not raw_dir.exists():
        return []
    return sorted(
        path
        for path in raw_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--write", action="store_true", help="Write wiki pages, index, and docs log.")
    parser.add_argument("--dry-run", action="store_true", help="Report planned imports without writing.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    raw_dir = root / "docs" / "raw"
    wiki_dir = root / "docs" / "wiki"
    log_path = root / "docs" / "log.md"
    write = args.write and not args.dry_run

    raw_files = discover_raw_files(raw_dir)
    if not raw_files:
        print(f"No supported raw files found in {raw_dir}")
        return 0

    planned: list[tuple[Path, Path]] = []
    for raw_path in raw_files:
        wiki_name = f"{slugify(raw_path.stem)}.md"
        wiki_path = wiki_dir / wiki_name
        if wiki_path.exists():
            print(f"Skip existing wiki page: {wiki_path.relative_to(root)}")
            continue
        planned.append((raw_path, wiki_path))

    if not planned:
        print("No new wiki imports planned.")
        return 0

    for raw_path, wiki_path in planned:
        print(f"Import {raw_path.relative_to(root)} -> {wiki_path.relative_to(root)}")

    if not write:
        print("Dry run only. Re-run with --write to create pages.")
        return 0

    wiki_dir.mkdir(parents=True, exist_ok=True)
    imported: list[tuple[Path, Path]] = []
    for raw_path, wiki_path in planned:
        wiki_path.write_text(make_wiki_content(raw_path, wiki_path, root), encoding="utf-8")
        update_wiki_index(wiki_dir / "README.md", wiki_path)
        imported.append((raw_path.relative_to(root), wiki_path.relative_to(root)))

    append_log(log_path, imported)
    print(f"Imported {len(imported)} raw file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
