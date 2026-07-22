#!/usr/bin/env python3
"""
validate_skills.py — CI gate for the RumblingStone skill trees.

Checks (hard errors, exit 1):
  1. Every skills/<name>/SKILL.md has YAML frontmatter with:
     - name  == directory name
     - description (non-empty)
  2. Every markdown link [text](path) in skills/**/*.md that points to a
     relative path resolves to an existing file/dir (repo-relative fallback).
  3. Every data YAML in scripts/ (catalogs, alliances, loot, map templates)
     parses with yaml.safe_load.

Warnings (printed, exit 0):
  - reference files not mentioned anywhere in their skill's SKILL.md
    (orphaned references an agent would never load).

Usage:  python3 scripts/validate_skills.py [--repo-root PATH]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")

DATA_YAML_GLOBS = [
    "scripts/*.yaml",
    "scripts/map_templates/*.yaml",
]


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def check_skills(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skills_dir = root / "skills"
    skill_dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    if not skill_dirs:
        return ["no skill directories found under skills/"], warnings

    for skill in skill_dirs:
        skill_md = skill / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill.relative_to(root)}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        rel = skill_md.relative_to(root)
        if fm is None:
            errors.append(f"{rel}: missing or unparseable YAML frontmatter")
            continue
        if fm.get("name") != skill.name:
            errors.append(
                f"{rel}: frontmatter name {fm.get('name')!r} != directory name {skill.name!r}"
            )
        if not str(fm.get("description") or "").strip():
            errors.append(f"{rel}: frontmatter description missing/empty")

        # Orphaned reference files (warning only)
        refs_dir = skill / "references"
        if refs_dir.is_dir():
            for ref in sorted(refs_dir.glob("*.md")):
                if ref.name not in text:
                    warnings.append(
                        f"{ref.relative_to(root)}: not mentioned in {skill.name}/SKILL.md"
                    )
    return errors, warnings


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    for md in sorted((root / "skills").rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):  # URL scheme
                continue
            # resolve relative to the file, then repo root as fallback
            cands = [md.parent / target, root / target]
            if not any(c.exists() for c in cands):
                errors.append(
                    f"{md.relative_to(root)}: broken relative link -> {target}"
                )
    return errors


def check_yaml_data(root: Path) -> list[str]:
    errors: list[str] = []
    for pattern in DATA_YAML_GLOBS:
        for path in sorted(root.glob(pattern)):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                errors.append(f"{path.relative_to(root)}: YAML parse error: {exc}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    args = ap.parse_args()
    root = args.repo_root.resolve()

    skill_errors, warnings = check_skills(root)
    link_errors = check_links(root)
    yaml_errors = check_yaml_data(root)
    errors = skill_errors + link_errors + yaml_errors

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    n_skills = len(list((root / "skills").glob("*/SKILL.md")))
    print(
        f"\nvalidate_skills: {n_skills} skills checked — "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
