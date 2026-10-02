#!/usr/bin/env python3
"""measure_tokens.py — honest token cost per agent query.

Runs a small set of representative queries against the canonical
`skills/*` source and reports actual token counts for:

  - Loading the entire source (the worst case).
  - Loading only the matching skill's SKILL.md (the routing-only case).
  - Loading SKILL.md + the files the skill itself says to load first + the one
    reference file the routing table sends you to (the realistic case).

Why "the files the skill says to load first" (RIPRESA-PR 4j-3, 2026-09-24,
recovered from a May branch): `rumblingstone-campaign/SKILL.md` mandates
`campaign-coherence.md` and `campaign/state.md` before any reference. Counting
only SKILL.md + one reference under-reported every campaign query and inflated
the savings. The list is read from each SKILL.md's "load order" section, so it
follows the skills when they change instead of living in a second copy here.
A reference that does not exist is reported as missing, never counted as 0.

Token estimate: chars / 4. This is the standard Anthropic / OpenAI
approximation for English+code mixed content. Replace with the official
tokenizer of your model for exact numbers; the ratios stay the same.

Usage:
  python3 scripts/measure_tokens.py
  python3 scripts/measure_tokens.py --tokenizer tiktoken    # if installed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"

# Representative queries — (query_label, target_skill, target_reference_filename)
QUERIES = [
    ("Rules: how does grapple work?",          "dnd-35-srd",           "combat.md"),
    ("Rules: spell DC for fireball?",          "dnd-35-srd",           "spells.md"),
    ("Lore: who is the god of dwarves?",       "forgotten-realms-lore", "fr-deities-complete.md"),
    ("Lore: where is Menzoberranzan?",         "forgotten-realms-lore", "fr-regions-complete.md"),
    ("Campaign: what's Thorik's status?",      "rumblingstone-campaign","campaign-party.md"),
    ("Campaign: current arc state?",           "rumblingstone-campaign","campaign-story-arcs.md"),
    ("Campaign: can artifact X be used again?","rumblingstone-campaign","campaign-coherence.md"),
]


def make_token_counter(name: str):
    if name == "chars/4":
        return lambda text: max(1, len(text) // 4)
    if name == "tiktoken":
        try:
            import tiktoken  # type: ignore
        except ImportError:
            print("tiktoken not installed; falling back to chars/4", file=sys.stderr)
            return lambda text: max(1, len(text) // 4)
        enc = tiktoken.get_encoding("cl100k_base")
        return lambda text: len(enc.encode(text))
    raise ValueError(f"Unknown tokenizer {name}")


def file_tokens(path: Path, count) -> int:
    if not path.is_file():
        return 0
    return count(path.read_text(encoding="utf-8"))


def total_tokens(paths: list[Path], count) -> int:
    return sum(file_tokens(p, count) for p in paths)


def all_md_under(root: Path) -> list[Path]:
    return sorted(root.rglob("*.md"))


LOAD_ORDER = re.compile(r"load(?:ing)? order", re.I)
LIST_ITEM = re.compile(r"^\s*\d+\.\s")
BACKTICK_MD = re.compile(r"`([^`\s]+\.md)`")


def required_preload(skill_dir: Path) -> list[Path]:
    """Files a skill's SKILL.md says to load before the reference.

    Read from the numbered list that follows a "load order" / "loading
    order" line. Paths are tried relative to the skill, to skills/, and to
    the repo root; the skill's own SKILL.md is not a preload.
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return []
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    start = next((i for i, riga in enumerate(lines) if LOAD_ORDER.search(riga)), None)
    if start is None:
        return []
    block: list[str] = []
    seen_item = False
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if LIST_ITEM.match(line):
            seen_item = True
        elif seen_item and line.strip() and not line.startswith((" ", "\t")):
            break
        block.append(line)
    found: list[Path] = []
    for rel in BACKTICK_MD.findall("\n".join(block)):
        for base in (skill_dir, SKILLS_DIR, REPO):
            cand = (base / rel).resolve()
            if cand.is_file():
                if cand != skill_md.resolve() and cand not in found:
                    found.append(cand)
                break
    return found


def measure_queries(queries, count) -> tuple[list[dict], int]:
    """One row per query; a missing SKILL.md or reference marks the row."""
    all_load = total_tokens(all_md_under(SKILLS_DIR), count)
    rows = []
    for label, skill, ref in queries:
        skill_dir = SKILLS_DIR / skill
        skill_md = skill_dir / "SKILL.md"
        ref_md = skill_dir / "references" / ref
        missing = [str(p.relative_to(REPO)) for p in (skill_md, ref_md) if not p.is_file()]
        preload = required_preload(skill_dir)
        load_set = sorted({skill_md, ref_md, *preload})
        targeted = total_tokens(load_set, count)
        rows.append({
            "query": label,
            "skill": skill,
            "ref": ref,
            "missing": missing,
            "preload": [str(p.relative_to(REPO)) for p in preload],
            "tokens_preload": total_tokens(preload, count),
            "tokens_targeted": targeted,
            "tokens_skill_full": total_tokens(all_md_under(skill_dir), count),
            "tokens_all_skills": all_load,
            "savings_vs_all_pct": round(100 * (1 - targeted / all_load), 1) if all_load else 0,
        })
    return rows, all_load


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tokenizer", default="chars/4",
                    choices=["chars/4", "tiktoken"],
                    help="Tokenization method. chars/4 is approximate, tiktoken is exact for OpenAI/Anthropic-like.")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a human table.")
    args = ap.parse_args()

    count = make_token_counter(args.tokenizer)

    # Per-skill SKILL.md only.
    skill_md_only = {
        skill_dir.name: file_tokens(skill_dir / "SKILL.md", count)
        for skill_dir in sorted(SKILLS_DIR.iterdir())
        if (skill_dir / "SKILL.md").is_file()
    }

    # Worst case (every md) and the representative queries.
    rows, all_load = measure_queries(QUERIES, count)

    if args.json:
        json.dump({
            "tokenizer": args.tokenizer,
            "all_skills_load_tokens": all_load,
            "per_skill_md_tokens": skill_md_only,
            "queries": rows,
        }, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    # Human table
    print(f"\nTokenizer: {args.tokenizer}")
    print(f"Worst case (load every skill md):  {all_load:>7,} tokens")
    print(f"\nPer-skill SKILL.md (routing only):")
    for k, v in skill_md_only.items():
        print(f"  {k:<28} {v:>5,} tokens")
    print(f"\nRepresentative queries (SKILL.md + required preload + matching reference):\n")
    print(f"{'Query':<42} {'Targeted':>10} {'Preload':>9} {'Skill Full':>11} {'vs All %':>10}")
    print("-" * 88)
    for r in rows:
        if r["missing"]:
            print(f"{r['query']:<42} {'MISSING':>10} {'-':>9} {'-':>11} {'-':>10}")
            continue
        print(f"{r['query']:<42} {r['tokens_targeted']:>10,} {r['tokens_preload']:>9,} "
              f"{r['tokens_skill_full']:>11,} {r['savings_vs_all_pct']:>9}%")
    missing = [r for r in rows if r["missing"]]
    if missing:
        print("\nWARNING: queries pointing at missing files (not counted as 0):", file=sys.stderr)
        for r in missing:
            print(f"  - {r['query']}: {', '.join(r['missing'])}", file=sys.stderr)
    print()
    print("Read this honestly:")
    print("  - 'Targeted' = what an agent loads when it follows the routing table,")
    print("    including the files the skill's SKILL.md says to load first ('Preload').")
    print("  - 'Skill Full' = what an agent loads if it grabs the whole matching skill.")
    print("  - 'vs All %' = savings vs loading every md file in skills/ (the dumb case).")
    print("  These numbers are the actual lever. The README's old 70-85% figure")
    print("  was theoretical; this is measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
