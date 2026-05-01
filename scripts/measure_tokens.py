#!/usr/bin/env python3
"""measure_tokens.py — honest token cost per agent query.

Runs a small set of representative queries against the canonical
`skills/*` source and reports actual token counts for:

  - Loading the entire source (the worst case).
  - Loading only the matching skill's SKILL.md (the routing-only case).
  - Loading SKILL.md + the one reference file the routing table sends you to
    (the realistic case).

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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tokenizer", default="chars/4",
                    choices=["chars/4", "tiktoken"],
                    help="Tokenization method. chars/4 is approximate, tiktoken is exact for OpenAI/Anthropic-like.")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a human table.")
    args = ap.parse_args()

    count = make_token_counter(args.tokenizer)

    # Worst case: load everything everywhere (the pre-split monolith behavior).
    all_paths = all_md_under(SKILLS_DIR)
    all_load = total_tokens(all_paths, count)

    # Per-skill SKILL.md only.
    skill_md_only = {
        skill_dir.name: file_tokens(skill_dir / "SKILL.md", count)
        for skill_dir in sorted(SKILLS_DIR.iterdir())
        if (skill_dir / "SKILL.md").is_file()
    }

    rows = []
    for label, skill, ref in QUERIES:
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        ref_md = SKILLS_DIR / skill / "references" / ref
        targeted = total_tokens([skill_md, ref_md], count)
        skill_full = total_tokens(all_md_under(SKILLS_DIR / skill), count)
        rows.append({
            "query": label,
            "skill": skill,
            "ref": ref,
            "tokens_targeted": targeted,
            "tokens_skill_full": skill_full,
            "tokens_all_skills": all_load,
            "savings_vs_all_pct": round(100 * (1 - targeted / all_load), 1) if all_load else 0,
        })

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
    print(f"\nRepresentative queries (load SKILL.md + matching reference):\n")
    print(f"{'Query':<42} {'Targeted':>10} {'Skill Full':>11} {'vs All %':>10}")
    print("-" * 80)
    for r in rows:
        print(f"{r['query']:<42} {r['tokens_targeted']:>10,} "
              f"{r['tokens_skill_full']:>11,} {r['savings_vs_all_pct']:>9}%")
    print()
    print("Read this honestly:")
    print("  - 'Targeted' = what an agent loads when it follows the routing table.")
    print("  - 'Skill Full' = what an agent loads if it grabs the whole matching skill.")
    print("  - 'vs All %' = savings vs loading every md file in skills/ (the dumb case).")
    print("  These numbers are the actual lever. The README's old 70-85% figure")
    print("  was theoretical; this is measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
