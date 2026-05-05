#!/usr/bin/env python3
"""
suggest_map.py — pick a tactical map template for a D&D 3.5 encounter.

Templates live in scripts/map_templates/*.yaml (human-readable, editable).
Each template contains: name, environment, type, size, legend, grid, notes.

Usage:
    python3 scripts/suggest_map.py --env forest
    python3 scripts/suggest_map.py --env cave --type boss-lair
    python3 scripts/suggest_map.py --list
    python3 scripts/suggest_map.py --name dragon-lair

Output is ready-to-print D&D 3.5 tactical grid (5ft squares, ASCII) with
legend and tactical notes. DM can copy into session prep.
"""
from __future__ import annotations
import sys, argparse
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent / "map_templates"

def parse_yaml_doc(text: str) -> dict:
    """Minimal YAML parser for our template schema. Supports:
       - scalar keys:  key: value
       - nested dict:  legend:\n  X: "..."
       - block scalar: grid: |\n  ...
       - list entries under notes:  - "..."
    """
    out: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1; continue
        if ":" not in line or line.startswith((" ", "\t", "-")):
            i += 1; continue
        key, _, rest = line.partition(":")
        key = key.strip(); rest = rest.strip()
        if rest == "|":
            # block scalar
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i][2:] if lines[i].startswith("  ") else lines[i])
                i += 1
            out[key] = "\n".join(block).rstrip()
            continue
        if rest == "":
            # nested block
            sub = {}
            sub_list = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                sl = lines[i]
                if not sl.strip(): i += 1; continue
                s = sl.strip()
                if s.startswith("- "):
                    sub_list.append(_unquote(s[2:].strip()))
                elif ":" in s:
                    k2, _, v2 = s.partition(":")
                    sub[k2.strip()] = _unquote(v2.strip())
                i += 1
            out[key] = sub_list if sub_list else sub
            continue
        out[key] = _unquote(rest)
        i += 1
    return out

def _unquote(v: str):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        return v[1:-1]
    return v

def load_templates() -> list[dict]:
    if not TEMPLATES_DIR.exists():
        return []
    out = []
    for p in sorted(TEMPLATES_DIR.glob("*.yaml")):
        try:
            d = parse_yaml_doc(p.read_text(encoding="utf-8"))
            d["_file"] = p.name
            d["_id"] = p.stem
            out.append(d)
        except Exception as e:
            print(f"[suggest_map] Failed to parse {p.name}: {e}", file=sys.stderr)
    return out

def match(t: dict, env: str|None, ttype: str|None) -> bool:
    if env and env != "any":
        te = (t.get("environment") or "").lower()
        if te not in ("any", env.lower()) and env.lower() not in te:
            return False
    if ttype:
        tt = (t.get("type") or "").lower()
        if ttype.lower() not in tt and tt not in ttype.lower():
            return False
    return True

def render(t: dict) -> str:
    out = []
    out.append(f"# Map: {t.get('name','?')}  (`{t.get('_id')}`)")
    out.append(f"**Environment**: {t.get('environment','?')}  |  **Type**: {t.get('type','?')}  |  **Size**: {t.get('size','?')}  (5ft squares)")
    out.append("")
    out.append("## Grid\n\n```")
    out.append(t.get("grid","") or "(missing grid)")
    out.append("```\n")
    legend = t.get("legend") or {}
    if isinstance(legend, dict) and legend:
        out.append("## Legend\n")
        for k, v in legend.items():
            out.append(f"- `{k}` — {v}")
        out.append("")
    notes = t.get("notes") or []
    if isinstance(notes, list) and notes:
        out.append("## Tactical notes\n")
        for n in notes:
            out.append(f"- {n}")
        out.append("")
    out.append(f"---\n*Source template: `scripts/map_templates/{t.get('_file')}` — edit or add new YAML files to extend.*")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser(description="Suggest a tactical map template.")
    ap.add_argument("--env", default=None, help="Environment filter: forest, cave, urban, swamp, ruins, dungeon, underdark, any")
    ap.add_argument("--type", dest="ttype", default=None, help="Type filter: ambush, corridor, open, complex, chokepoint, scattered, street, large-room, tower-level, arena, boss-lair")
    ap.add_argument("--name", default=None, help="Exact template id (filename without .yaml)")
    ap.add_argument("--list", action="store_true", help="List available templates")
    args = ap.parse_args()

    templates = load_templates()
    if not templates:
        print(f"[suggest_map] No templates in {TEMPLATES_DIR}.", file=sys.stderr)
        return 2

    if args.list or (not args.env and not args.ttype and not args.name):
        print(f"# Map templates available ({len(templates)})\n")
        print("| ID | Name | Environment | Type | Size |")
        print("|---|---|---|---|---|")
        for t in templates:
            print(f"| `{t['_id']}` | {t.get('name','?')} | {t.get('environment','?')} | {t.get('type','?')} | {t.get('size','?')} |")
        print("\nUsage: `python3 scripts/suggest_map.py --name <id>` or `--env <env>`.")
        return 0

    if args.name:
        hit = next((t for t in templates if t["_id"] == args.name), None)
        if not hit:
            print(f"[suggest_map] No template named '{args.name}'. Use --list.", file=sys.stderr)
            return 3
        print(render(hit)); return 0

    matches = [t for t in templates if match(t, args.env, args.ttype)]
    if not matches:
        print(f"[suggest_map] No templates match env='{args.env}' type='{args.ttype}'.", file=sys.stderr)
        return 4
    for t in matches:
        print(render(t)); print("\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
