#!/usr/bin/env python3
"""
compress_skills.py — Token-Optimized Skill Compressor
RumblingStone / AI Multi-Agent Skill Pipeline

Converts verbose Markdown skill files into three output formats:
  compact.md   → Claude (structured markdown, ~50-70% token reduction)
  structured.yaml → Gemini (YAML key-value, optimal for structured data)
  machine.json → Codex/API (JSON, zero ambiguity, deterministic parsing)

Usage:
  python3 compress_skills.py --input skills/dnd-35-rules/references/ --output build/
  python3 compress_skills.py --input FILE.md --output build/ --measure
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Optional
import yaml

def count_tokens(text: str) -> int:
    """Count tokens using tiktoken if available, else word-based estimate."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        # Fallback: words * 1.3 (empirical avg for English+markdown)
        return int(len(text.split()) * 1.3)


# ─── DSL Compaction Rules ────────────────────────────────────────────────────

# Prose patterns → compact symbols
PROSE_TO_DSL = [
    # Dice / numbers
    (r'\bplus\b', '+'),
    (r'\bminus\b', '-'),
    (r'\btimes\b', '×'),
    (r'\bdivided by\b', '÷'),
    (r'\bgreater than or equal to\b', '≥'),
    (r'\bless than or equal to\b', '≤'),
    (r'\bgreater than\b', '>'),
    (r'\bless than\b', '<'),
    (r'\bnot equal\b', '≠'),

    # Direction / flow
    (r'\btherefore\b', '→'),
    (r'\bresults in\b', '→'),
    (r'\bleads to\b', '→'),
    (r'\bif and only if\b', '⟺'),
    (r'\brequires\b', 'req:'),
    (r'\bmodifier\b', 'mod'),
    (r'\bbonus\b', 'bon'),

    # D&D specific abbreviations
    (r'\bBase Attack Bonus\b', 'BAB'),
    (r'\bArmor Class\b', 'AC'),
    (r'\bHit Points?\b', 'HP'),
    (r'\bDifficulty Class\b', 'DC'),
    (r'\bSaving Throw\b', 'Save'),
    (r'\bSpell Resistance\b', 'SR'),
    (r'\bDamage Reduction\b', 'DR'),
    (r'\bChallenge Rating\b', 'CR'),
    (r'\bAverage Party Level\b', 'APL'),
    (r'\bExperience Points?\b', 'XP'),
    (r'\bSpell Level\b', 'SL'),
    (r'\bCaster Level\b', 'CL'),
    (r'\bFull-Round Action\b', 'FRA'),
    (r'\bStandard Action\b', 'StdA'),
    (r'\bMove Action\b', 'MvA'),
    (r'\bSwift Action\b', 'SwiA'),
    (r'\bImmediate Action\b', 'ImmA'),
    (r'\bFree Action\b', 'FreeA'),
    (r'\bAttack of Opportunity\b', 'AoO'),
    (r'\bForgotten Realms\b', 'FR'),
    (r'\bSystem Reference Document\b', 'SRD'),
    (r'\bper level\b', '/lvl'),
    (r'\bper round\b', '/rnd'),
    (r'\bper day\b', '/day'),
    (r'\bonce per day\b', '1/day'),
    (r'\bonce per round\b', '1/rnd'),
    (r'\bonce per week\b', '1/week'),
    (r'\bStrength\b(?!\s+\d)', 'STR'),
    (r'\bDexterity\b(?!\s+\d)', 'DEX'),
    (r'\bConstitution\b(?!\s+\d)', 'CON'),
    (r'\bIntelligence\b(?!\s+\d)', 'INT'),
    (r'\bWisdom\b(?!\s+\d)', 'WIS'),
    (r'\bCharisma\b(?!\s+\d)', 'CHA'),
    (r'\bFortitude\b', 'Fort'),
    (r'\bReflex\b', 'Ref'),
    (r'\bWill\b(?= save)', 'Will'),
    (r'\bmelee\b', 'mel'),
    (r'\branged\b', 'rng'),
    (r'\bcharacter level\b', 'char_lvl'),
    (r'\bmaximum\b', 'max'),
    (r'\bminimum\b', 'min'),
    (r'\bcontinuous\b', 'cont'),
    (r'\btemporary\b', 'temp'),
    (r'\bpermanent\b', 'perm'),
    (r'\bsupernaturally?\b', 'Su'),
    (r'\bspell-like\b', 'Sp'),
    (r'\bextraordinary\b', 'Ex'),
]

# Redundant prose to strip
STRIP_PATTERNS = [
    r'(?m)^Note:\s*',
    r'(?m)^Note that\s+',
    r'This means that\s+',
    r'It is important to note that\s+',
    r'Please note that\s+',
    r'As mentioned above,?\s+',
    r'As noted above,?\s+',
    r'In other words,?\s+',
    r'That is to say,?\s+',
    r'In summary,?\s+',
    r'To summarize,?\s+',
    r'\bIn this case,?\s+',
    r'\bFor example,?\s+(?=\S)',
    r'\bFor instance,?\s+(?=\S)',
    r'\bSpecifically,?\s+(?=\S)',
    r'\bBasically,?\s+(?=\S)',
    r'\bEssentially,?\s+(?=\S)',
]


def strip_redundant_prose(text: str) -> str:
    for pattern in STRIP_PATTERNS:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text


def apply_dsl_abbreviations(text: str) -> str:
    for pattern, replacement in PROSE_TO_DSL:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def compress_table(text: str) -> str:
    """Compress markdown tables by removing padding spaces."""
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.startswith('|'):
            # Remove excess spaces within cells
            compressed = re.sub(r'\|\s+', '| ', line)
            compressed = re.sub(r'\s+\|', ' |', compressed)
            result.append(compressed)
        else:
            result.append(line)
    return '\n'.join(result)


def compress_whitespace(text: str) -> str:
    """Remove triple+ blank lines, trailing spaces."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    return text.strip()


def strip_yaml_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter if present."""
    match = re.match(r'^---\s*\n(.*?\n)---\s*\n', text, re.DOTALL)
    if match:
        try:
            meta = yaml.safe_load(match.group(1))
            return meta or {}, text[match.end():]
        except Exception:
            pass
    return {}, text


def compress_to_compact_md(content: str) -> str:
    """Claude-optimized: structured markdown with DSL abbreviations."""
    meta, body = strip_yaml_frontmatter(content)
    body = strip_redundant_prose(body)
    body = apply_dsl_abbreviations(body)
    body = compress_table(body)
    body = compress_whitespace(body)

    header = ""
    if meta.get('name'):
        header = f"# SKILL:{meta['name']}\n\n"

    return header + body


def compress_to_yaml(content: str) -> str:
    """Gemini-optimized: structured YAML for clean key-value parsing."""
    meta, body = strip_yaml_frontmatter(content)

    # Extract sections
    sections = {}
    current_section = "overview"
    current_lines = []

    for line in body.split('\n'):
        if line.startswith('## '):
            if current_lines:
                sections[current_section] = '\n'.join(current_lines).strip()
            current_section = line[3:].strip().lower().replace(' ', '_').replace('/', '_')
            current_lines = []
        elif line.startswith('### '):
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_section] = '\n'.join(current_lines).strip()

    output = {
        'skill': meta.get('name', 'unknown'),
        'description': str(meta.get('description', '')).strip(),
        'sections': sections
    }

    return yaml.dump(output, allow_unicode=True, default_flow_style=False, sort_keys=False)


def compress_to_json(content: str) -> str:
    """Codex/API-optimized: machine-readable JSON for deterministic parsing."""
    meta, body = strip_yaml_frontmatter(content)

    # Extract tables as structured data
    tables = []
    current_table = []
    headers = []
    in_table = False

    for line in body.split('\n'):
        if line.startswith('|') and '|' in line[1:]:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if not in_table:
                headers = cells
                in_table = True
            elif re.match(r'^[\|\s\-:]+$', line):
                continue  # separator row
            else:
                if headers:
                    tables.append(dict(zip(headers, cells)))
        else:
            if in_table and current_table:
                pass
            in_table = False

    # Extract rules as key→value pairs
    rules = {}
    for match in re.finditer(r'\*\*([^*]+)\*\*:\s*([^\n]+)', body):
        key = match.group(1).strip()
        val = match.group(2).strip()
        rules[key] = val

    # Compact body: apply DSL, strip prose
    compact_body = apply_dsl_abbreviations(strip_redundant_prose(body))
    compact_body = compress_whitespace(compact_body)

    output = {
        "skill": meta.get("name", "unknown"),
        "desc": str(meta.get("description", "")).strip()[:200],
        "rules": rules,
        "tables": tables,
        "body": compact_body
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


# ─── Token Measurement ───────────────────────────────────────────────────────

def measure_compression(original: str, compressed: str, label: str) -> dict:
    orig_tokens = count_tokens(original)
    comp_tokens = count_tokens(compressed)
    reduction = (1 - comp_tokens / orig_tokens) * 100 if orig_tokens > 0 else 0
    return {
        "label": label,
        "original_tokens": orig_tokens,
        "compressed_tokens": comp_tokens,
        "reduction_pct": round(reduction, 1),
        "original_chars": len(original),
        "compressed_chars": len(compressed),
    }


# ─── Main Processing ─────────────────────────────────────────────────────────

def process_file(input_path: Path, output_dir: Path, measure: bool = False) -> dict:
    content = input_path.read_text(encoding='utf-8')
    stem = input_path.stem
    results = {"file": str(input_path), "formats": {}}

    formats = {
        "compact.md": compress_to_compact_md(content),
        "structured.yaml": compress_to_yaml(content),
        "machine.json": compress_to_json(content),
    }

    for fmt_suffix, compressed in formats.items():
        out_path = output_dir / f"{stem}.{fmt_suffix}"
        out_path.write_text(compressed, encoding='utf-8')

        if measure:
            stats = measure_compression(content, compressed, fmt_suffix)
            results["formats"][fmt_suffix] = stats

    return results


def process_directory(input_dir: Path, output_dir: Path, measure: bool = False) -> list:
    output_dir.mkdir(parents=True, exist_ok=True)
    all_results = []

    for md_file in sorted(input_dir.rglob("*.md")):
        relative = md_file.relative_to(input_dir)
        file_output_dir = output_dir / relative.parent
        file_output_dir.mkdir(parents=True, exist_ok=True)
        result = process_file(md_file, file_output_dir, measure)
        all_results.append(result)
        print(f"  ✓ {relative}", file=sys.stderr)

    return all_results


def print_report(results: list):
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║           COMPRESSION REPORT (token delta)              ║")
    print("╠══════════════════════════════════════════════════════════╣")

    totals = {}
    for result in results:
        fname = Path(result["file"]).name
        for fmt, stats in result.get("formats", {}).items():
            if fmt not in totals:
                totals[fmt] = {"orig": 0, "comp": 0}
            totals[fmt]["orig"] += stats["original_tokens"]
            totals[fmt]["comp"] += stats["compressed_tokens"]
            print(f"║ {fname[:35]:<35} [{fmt[:15]:<15}] "
                  f"-{stats['reduction_pct']:4.1f}%  ║")

    print("╠══════════════════════════════════════════════════════════╣")
    print("║ TOTALS                                                   ║")
    for fmt, t in totals.items():
        reduction = (1 - t["comp"] / t["orig"]) * 100 if t["orig"] > 0 else 0
        print(f"║  {fmt:<20} {t['orig']:>6} → {t['comp']:>6} tokens  "
              f"(-{reduction:.1f}%)  ║")
    print("╚══════════════════════════════════════════════════════════╝\n")


def main():
    parser = argparse.ArgumentParser(description="Skill compressor for AI agents")
    parser.add_argument("--input", "-i", required=True, help="Input .md file or directory")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--measure", "-m", action="store_true", help="Measure token savings")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if input_path.is_file():
        output_dir.mkdir(parents=True, exist_ok=True)
        result = process_file(input_path, output_dir, args.measure)
        results = [result]
        print(f"  ✓ {input_path.name}", file=sys.stderr)
    elif input_path.is_dir():
        results = process_directory(input_path, output_dir, args.measure)
    else:
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    if args.measure:
        print_report(results)

    # Write summary JSON
    summary_path = output_dir / "_compression_summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding='utf-8')


if __name__ == "__main__":
    main()
