#!/usr/bin/env python3
"""
index_skills.py — Semantic Retrieval Index Builder
RumblingStone / AI Multi-Agent Skill Pipeline

Scans compressed skill files and builds a structured index.json that allows
AI agents to load ONLY the relevant chunks instead of entire skill trees.

Output: index.json in each directory level with keyword→file mappings.

Usage:
  python3 index_skills.py --input build/ --output build/index.json
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


# ─── Domain Keyword Taxonomy ─────────────────────────────────────────────────
# Maps retrieval terms → file stems to load

DOMAIN_KEYWORDS = {
    # Core mechanics
    "combat": ["combat", "attack", "initiative", "action", "grapple", "conditions"],
    "spells": ["spells", "spell", "magic", "metamagic", "school", "casting"],
    "classes": ["classes", "fighter", "monk", "druid", "cleric", "ranger", "barbarian",
                 "bard", "rogue", "wizard", "sorcerer", "paladin"],
    "skills_system": ["skills", "skill", "check", "ranks", "trained"],
    "feats": ["feats", "feat", "bonus feat", "regional feat", "divine feat"],
    "items": ["items", "magic items", "weapon", "armor", "wondrous", "ring", "wand", "scroll"],
    "monsters": ["monsters", "monster", "cr", "challenge rating", "template", "creature type"],
    "core_mechanics": ["core", "mechanics", "ability score", "saving throw", "ac", "armor class",
                       "initiative", "xp", "experience", "level"],

    # FR Lore
    "deities": ["deity", "god", "pantheon", "domain", "moradin", "lathander", "lolth",
                 "tymora", "mystra", "tempus", "drow pantheon", "elven pantheon", "dwarven pantheon"],
    "regions": ["region", "waterdeep", "cormyr", "thay", "rashemen", "sword coast",
                 "underdark", "menzoberranzan", "dalelands", "heartlands"],
    "races": ["race", "elf", "dwarf", "halfling", "gnome", "human", "drow", "half-elf",
              "genasi", "tiefling", "aasimar", "svirfneblin"],
    "factions": ["faction", "harpers", "zhentarim", "red wizard", "cult of the dragon",
                 "bregan", "moonstars", "lords alliance"],
    "history": ["history", "timeline", "dale reckoning", "netheril", "time of troubles",
                 "1372 dr", "toril", "faerûn", "ancient empire"],
    "prestige_classes": ["prestige class", "harper scout", "red wizard", "purple dragon",
                         "bladesinger", "shadow adept", "hathran", "archmage"],
    "fr_feats": ["regional feat", "divine feat", "initiate feat", "tattoo focus", "shadow weave"],
    "artifacts_fr": ["artifact", "nether scrolls", "tablets of fate", "moonblade",
                     "crenshinibon", "blackstaff"],

    # Campaign-specific
    "party": ["thorik", "tordek", "hella", "artemis", "party", "rumbling stone"],
    "campaign_artifacts": ["aegis fang", "corona di adamantio", "ring of chaotic illumination",
                            "bracieri gemelli", "collana dei semi eterni", "cuore di moradin"],
    "story_arcs": ["arc", "hammerfist", "eternal forge", "rethmar", "cannath vale",
                   "underdark", "story", "timeline", "current state"],
    "dm_strategy": ["dm", "dungeon master", "shine time", "state machine", "railroading",
                    "player profile", "thorik dm", "artemis dm", "tordek dm", "hella dm",
                    "triangolo di rischio"],
    "map_locations": ["cannath vale", "rethmar", "brindol", "drellin", "skull gorge",
                      "hammerfist holds", "lhesper", "vraath keep", "fane of tiamat",
                      "shaarcah forest", "lhespenbog", "wyrmbones"],
    "npcs": ["therysol", "zalkatar", "sonjak", "il collezionista", "npc"],
    "dm_tools": ["monster art", "token", "vtt", "quest tree", "villain", "faction tracker",
                 "encounter", "branching quest"],
    "resources": ["d20srd", "dndtools", "realmshelps", "wiki", "fandom", "orbitalflower",
                  "free tools", "vtt tools", "imarvintpa"],
}

# File → primary domains mapping (for fast reverse lookup)
FILE_DOMAINS = {
    "SKILL": ["meta", "navigation"],
    "combat": ["combat"],
    "spells": ["spells"],
    "classes": ["classes"],
    "core-mechanics": ["core_mechanics"],
    "items": ["items"],
    "monsters": ["monsters"],
    "forgotten-realms": ["regions", "deities", "history"],
    "fr-deities-complete": ["deities"],
    "fr-regions-complete": ["regions"],
    "fr-races-complete": ["races"],
    "fr-factions": ["factions"],
    "fr-prestige-classes": ["prestige_classes"],
    "fr-feats": ["fr_feats"],
    "fr-history": ["history"],
    "fr-artifacts": ["artifacts_fr"],
    "fr-cannath-vale": ["map_locations", "story_arcs"],
    "campaign-party": ["party", "npcs"],
    "campaign-artifacts": ["campaign_artifacts"],
    "campaign-story-arcs": ["story_arcs"],
    "campaign-dm-strategy": ["dm_strategy"],
    "dm-expansion-toolkit": ["dm_tools"],
    "resources": ["resources"],
}


def extract_headings(content: str) -> list[str]:
    return re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)


def extract_bold_terms(content: str) -> list[str]:
    return re.findall(r'\*\*([^*]{2,40})\*\*', content)


def extract_table_headers(content: str) -> list[str]:
    headers = []
    for line in content.split('\n'):
        if line.startswith('|') and '---' not in line:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            headers.extend(cells[:3])  # Take first 3 cols as domain terms
    return headers


def infer_domains_from_content(filename: str, content: str) -> list[str]:
    """Infer domain tags by scanning content for keyword clusters."""
    stem = Path(filename).stem
    domains = list(FILE_DOMAINS.get(stem, []))

    content_lower = content.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if domain in domains:
            continue
        hits = sum(1 for kw in keywords if kw in content_lower)
        if hits >= 2:  # At least 2 keyword matches = include domain
            domains.append(domain)

    return list(set(domains))


def build_file_entry(md_file: Path, build_dir: Path) -> dict[str, Any]:
    """Build an index entry for a single source file."""
    content = md_file.read_text(encoding='utf-8')
    headings = extract_headings(content)
    bold_terms = extract_bold_terms(content)[:20]  # top 20 terms
    domains = infer_domains_from_content(md_file.name, content)

    # Check which compressed formats exist
    stem = md_file.stem
    available_formats = []
    for fmt_suffix in ["compact.md", "structured.yaml", "machine.json"]:
        candidate = build_dir / f"{stem}.{fmt_suffix}"
        if candidate.exists():
            available_formats.append(fmt_suffix)

    return {
        "file": md_file.name,
        "stem": stem,
        "domains": domains,
        "headings": headings[:10],
        "key_terms": bold_terms,
        "formats": available_formats,
        "chars": len(content),
    }


def build_domain_index(entries: list[dict]) -> dict[str, list[str]]:
    """Build domain → [file stems] reverse index."""
    domain_to_files = defaultdict(list)
    for entry in entries:
        for domain in entry["domains"]:
            domain_to_files[domain].append(entry["stem"])
    return dict(domain_to_files)


def build_keyword_index(entries: list[dict]) -> dict[str, list[str]]:
    """Build keyword → [file stems] for retrieval."""
    kw_to_files = defaultdict(set)
    for entry in entries:
        all_terms = (
            entry["headings"] +
            entry["key_terms"] +
            entry["domains"]
        )
        for term in all_terms:
            key = term.lower().strip()
            if len(key) > 2:
                kw_to_files[key].add(entry["stem"])
    return {k: sorted(v) for k, v in kw_to_files.items()}


def build_agent_routing(entries: list[dict]) -> dict[str, list[str]]:
    """Per-agent optimal format selection."""
    return {
        "claude": {
            "format": "compact.md",
            "load_strategy": "domain_selective",
            "note": "Load only matching domain files, use compact.md",
        },
        "gemini": {
            "format": "structured.yaml",
            "load_strategy": "domain_selective",
            "note": "YAML for structured key-value parsing",
        },
        "codex": {
            "format": "machine.json",
            "load_strategy": "domain_selective",
            "note": "JSON for deterministic parsing",
        },
        "chatgpt": {
            "format": "compact.md",
            "load_strategy": "domain_selective",
            "note": "Mixed NL + structure; compact.md",
        },
        "cursor": {
            "format": "machine.json",
            "load_strategy": "full_load",
            "note": "Code assistant; JSON preferred",
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Build retrieval index for skill files")
    parser.add_argument("--input", "-i", required=True, help="Source skill directory (originals)")
    parser.add_argument("--build", "-b", required=True, help="Build directory (compressed outputs)")
    parser.add_argument("--output", "-o", required=True, help="Output index.json path")
    args = parser.parse_args()

    input_dir = Path(args.input)
    build_dir = Path(args.build)
    output_path = Path(args.output)

    print(f"  Scanning {input_dir}...", flush=True)
    entries = []
    for md_file in sorted(input_dir.rglob("*.md")):
        entry = build_file_entry(md_file, build_dir)
        entries.append(entry)
        print(f"    indexed: {md_file.name} → domains: {entry['domains'][:3]}")

    domain_index = build_domain_index(entries)
    keyword_index = build_keyword_index(entries)
    agent_routing = build_agent_routing(entries)

    index = {
        "_meta": {
            "generated": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
            "total_files": len(entries),
            "total_domains": len(domain_index),
            "usage": (
                "Query 'domain_index' to find files for a topic. "
                "Query 'keyword_index' for term lookup. "
                "Use 'agent_routing' to select format per agent."
            ),
        },
        "files": {e["stem"]: e for e in entries},
        "domain_index": domain_index,
        "keyword_index": keyword_index,
        "agent_routing": agent_routing,
        "decision_tree": {
            "combat_turn": ["check status_conditions", "evaluate threats", "choose action→[melee|ranged|spell|special]"],
            "spell_lookup": ["identify school+level", "load spells.md", "fetch d20srd.org if exact text needed"],
            "fr_lore_lookup": ["identify region|deity|race|faction", "load specific fr-*.md file", "cross-ref wiki if needed"],
            "campaign_query": ["identify topic→[party|artifacts|arcs|dm_strategy|map]", "load campaign-*.md"],
            "rule_adjudication": ["identify domain", "load relevant reference", "RAW first then RAI"],
        }
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n  ✓ Index written → {output_path}")
    print(f"    Files indexed:  {len(entries)}")
    print(f"    Domains:        {len(domain_index)}")
    print(f"    Keywords:       {len(keyword_index)}")


if __name__ == "__main__":
    main()
