#!/usr/bin/env python3
"""
suggest_encounter.py v2 — D&D 3.5 encounter suggester for RumblingStone.

Modes:
  (A) Faction/alliance encounter (canonical):
      --el 13 --alliance red-hand-drow-pact --inject-npc "Drow Priestess of Lolth 9"
      --el 14 --factions red-hand,drow-sonjak --env underdark --narrative
  (B) Wild encounter (faction-less, no structured loot):
      --el 11 --wild --env swamp

Catalogs:
  * scripts/monster_catalog.yaml          (auto)
  * scripts/monster_catalog.custom.yaml   (DM append)
  * scripts/faction_alliances.yaml        (alliances + wild tables)

Output:
  Markdown proposals con tag `loot: structured` (fazioni) o `loot: none` (wild),
  consumabile da scripts/suggest_loot.py (STANDALONE, non integrato qui).

DMG 3.5 EL math:  EL ≈ 2 · log2(Σ 2^(CR/2))
  (Doubling the number of equal-CR creatures increases EL by +2 in 3.5,
   NOT +1 as in 4e/5e. Power scales as 2^(CR/2).)
"""
from __future__ import annotations
import sys, argparse, random, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
CATALOG = HERE / "monster_catalog.yaml"
CUSTOM  = HERE / "monster_catalog.custom.yaml"
ALLIANCES = HERE / "faction_alliances.yaml"


# ───────────────────────── YAML loading ─────────────────────────
def _coerce(v: str):
    v = v.strip()
    if v == "" or v == "~" or v.lower() == "null": return None
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner: return []
        return [_coerce(x) for x in _split_flow(inner)]
    if v.startswith("{") and v.endswith("}"):
        inner = v[1:-1].strip()
        d = {}
        for part in _split_flow(inner):
            if ":" in part:
                k, _, val = part.partition(":")
                d[k.strip()] = _coerce(val)
        return d
    try:
        if "." not in v: return int(v)
        return float(v)
    except ValueError:
        return v

def _split_flow(s: str) -> list[str]:
    """Split a flow-style YAML inner string on top-level commas."""
    out, buf, depth, quote = [], [], 0, None
    for ch in s:
        if quote:
            buf.append(ch)
            if ch == quote: quote = None
            continue
        if ch in '"\'':
            quote = ch; buf.append(ch); continue
        if ch in "[{": depth += 1
        elif ch in "]}": depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(buf).strip()); buf = []
        else:
            buf.append(ch)
    if buf: out.append("".join(buf).strip())
    return out

def load_yaml(path: Path):
    """Tolerant YAML loader: supports nested maps, block lists, flow lists/dicts,
    and multi-line 'folded' scalars where a value continues on subsequent indented
    lines (as produced by the editor auto-formatter)."""
    if not path.exists(): return {}
    raw_text = path.read_text(encoding="utf-8")
    # Pre-pass 1: merge multi-line flow collections ({...} and [...]) into
    # a single logical line. The auto-formatter splits long flow dicts/lists
    # over many lines; we rejoin them before parsing.
    pre_lines = raw_text.splitlines()
    joined: list[str] = []
    buf = None
    depth = 0
    in_string = None
    for ln in pre_lines:
        if buf is None:
            # check if this line opens an unclosed flow collection
            d = 0; s = None
            for ch in ln:
                if s:
                    if ch == s: s = None
                    continue
                if ch in '"\'':
                    s = ch; continue
                if ch == "#" and not s: break
                if ch in "[{": d += 1
                elif ch in "]}": d -= 1
            if d > 0:
                buf = [ln]; depth = d; in_string = s
            else:
                joined.append(ln)
        else:
            buf.append(ln.lstrip())
            d = depth; s = in_string
            for ch in ln:
                if s:
                    if ch == s: s = None
                    continue
                if ch in '"\'':
                    s = ch; continue
                if ch in "[{": d += 1
                elif ch in "]}": d -= 1
            depth = d; in_string = s
            if depth <= 0:
                joined.append(" ".join(buf))
                buf = None; depth = 0; in_string = None
    if buf is not None: joined.append(" ".join(buf))
    lines = joined
    # Pre-pass 2: merge folded continuation lines into their parent value line.
    merged: list[str] = []
    for raw in lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            merged.append(raw); continue
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)
        if merged:
            prev = merged[-1]
            prev_stripped = prev.lstrip()
            prev_indent = len(prev) - len(prev_stripped)
            # folded continuation: deeper indent, previous is a "key: value" or "- key: value"
            # and the current line doesn't start with '-' or 'key:' at its own mapping level.
            is_mapping_like = (":" in prev_stripped) and not prev_stripped.startswith("- ") or \
                              prev_stripped.startswith("- ") and ":" in prev_stripped[2:]
            is_kv_here = re.match(r"[A-Za-z0-9_\-]+:\s", stripped) is not None
            starts_list = stripped.startswith("- ")
            if indent > prev_indent and is_mapping_like and not is_kv_here and not starts_list \
               and not prev_stripped.endswith(":") and not prev_stripped.endswith("|"):
                merged[-1] = prev.rstrip() + " " + stripped
                continue
        merged.append(raw)
    return _parse_block(merged, 0, 0)[0]

def _parse_block(lines: list[str], i: int, indent: int):
    """Parse a block (map or list) starting at line i with the given indent.
    Returns (value, new_i)."""
    # Detect whether block is a list or a map by first non-empty line at indent.
    j = i
    while j < len(lines) and (not lines[j].strip() or lines[j].lstrip().startswith("#")):
        j += 1
    if j >= len(lines): return (None, j)
    first = lines[j]
    first_indent = len(first) - len(first.lstrip())
    if first_indent < indent: return (None, i)
    is_list = first.lstrip().startswith("- ")
    if is_list:
        return _parse_list(lines, i, first_indent)
    return _parse_map(lines, i, first_indent)

def _parse_map(lines, i, indent):
    out = {}
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1; continue
        cur_indent = len(raw) - len(raw.lstrip())
        if cur_indent < indent: break
        if cur_indent > indent: i += 1; continue
        stripped = raw.lstrip()
        if stripped.startswith("- "): break  # not a map at this level
        if ":" not in stripped: i += 1; continue
        key, _, val = stripped.partition(":")
        key = key.strip(); val = val.strip()
        if val == "":
            # nested block: look ahead
            nxt_i = i + 1
            while nxt_i < len(lines) and (not lines[nxt_i].strip() or lines[nxt_i].lstrip().startswith("#")):
                nxt_i += 1
            if nxt_i < len(lines):
                nxt_indent = len(lines[nxt_i]) - len(lines[nxt_i].lstrip())
                if nxt_indent > indent:
                    sub, i = _parse_block(lines, i+1, nxt_indent)
                    out[key] = sub
                    continue
            out[key] = None; i += 1
        elif val == "|":
            # literal block scalar
            i += 1
            buf = []
            while i < len(lines):
                r = lines[i]
                if not r.strip(): buf.append(""); i += 1; continue
                ci = len(r) - len(r.lstrip())
                if ci <= indent: break
                buf.append(r[indent+2:] if len(r) > indent+2 else r.lstrip())
                i += 1
            out[key] = "\n".join(buf).rstrip()
        else:
            out[key] = _coerce(val); i += 1
    return out, i

def _parse_list(lines, i, indent):
    out = []
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1; continue
        cur_indent = len(raw) - len(raw.lstrip())
        if cur_indent < indent: break
        stripped = raw.lstrip()
        if not stripped.startswith("- "): break
        rest = stripped[2:]
        # list item: could be scalar, flow value, or start of nested map
        if rest.startswith("{") or rest.startswith("["):
            out.append(_coerce(rest)); i += 1; continue
        if ":" in rest:
            # map-in-list starting on same line
            key, _, val = rest.partition(":")
            item = {key.strip(): _coerce(val) if val.strip() else None}
            i += 1
            # continue parsing deeper keys (indent == indent+2)
            child_indent = indent + 2
            while i < len(lines):
                r = lines[i]
                if not r.strip() or r.lstrip().startswith("#"): i += 1; continue
                ci = len(r) - len(r.lstrip())
                if ci < child_indent: break
                if ci == child_indent and r.lstrip().startswith("- "): break
                if ci == indent and r.lstrip().startswith("- "): break
                if ci == child_indent:
                    s = r.lstrip()
                    if ":" not in s: i += 1; continue
                    k2, _, v2 = s.partition(":")
                    v2 = v2.strip()
                    if v2 == "":
                        nxt = i+1
                        while nxt < len(lines) and (not lines[nxt].strip() or lines[nxt].lstrip().startswith("#")):
                            nxt += 1
                        if nxt < len(lines):
                            ni = len(lines[nxt]) - len(lines[nxt].lstrip())
                            if ni > child_indent:
                                sub, i = _parse_block(lines, i+1, ni)
                                item[k2.strip()] = sub; continue
                        item[k2.strip()] = None; i += 1
                    elif v2 == "|":
                        i += 1
                        buf = []
                        while i < len(lines):
                            rr = lines[i]
                            if not rr.strip(): buf.append(""); i += 1; continue
                            cii = len(rr) - len(rr.lstrip())
                            if cii <= child_indent: break
                            buf.append(rr[child_indent+2:] if len(rr) > child_indent+2 else rr.lstrip())
                            i += 1
                        item[k2.strip()] = "\n".join(buf).rstrip()
                    else:
                        item[k2.strip()] = _coerce(v2); i += 1
                else:
                    i += 1
            out.append(item)
        else:
            out.append(_coerce(rest)); i += 1
    return out, i


# ───────────────────────── EL / CR math ─────────────────────────
def combine_el(crs: list[float]) -> float:
    """Combine CRs into an Encounter Level per D&D 3.5 DMG.

    In 3.5 doubling the number of equal-CR creatures raises EL by +2
    (not +1 as in 4e/5e). Power therefore scales as 2^(CR/2) and the
    combined EL is:

        EL = 2 · log2( Σ 2^(CR/2) )

    Example: two CR 10 creatures → 2·log2(2·2^5) = 2·log2(64) = 12 ✓
    """
    if not crs: return 0.0
    return 2.0 * math.log2(sum(2 ** (c / 2.0) for c in crs))

def _cr_num(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    s = str(v).strip().replace("CR", "").strip()
    if "/" in s:
        try:
            a, b = s.split("/")
            num, den = float(a), float(b)
            if den == 0:
                return None
            return num / den
        except Exception:
            return None
    try: return float(s)
    except: return None



# ───────────────────────── Catalog ─────────────────────────
def load_catalog() -> list[dict]:
    data = load_yaml(CATALOG)
    cat = list(data.get("monsters") or []) if isinstance(data, dict) else []
    cdata = load_yaml(CUSTOM)
    if isinstance(cdata, dict):
        cat += list(cdata.get("monsters") or [])
    for m in cat:
        m["cr"] = _cr_num(m.get("cr"))
        m["faction"] = (m.get("faction") or "unknown").lower()
        m["role"] = (m.get("role") or "").lower()
        m["environment"] = (m.get("environment") or "").lower()
        m["name"] = m.get("name") or m.get("id") or "?"
    return [m for m in cat if m["cr"] is not None]

def load_alliances() -> dict:
    return load_yaml(ALLIANCES) or {}


# ───────────────────────── Canonical PNG/ directory scan ─────────────────────────
def scan_canonical_npcs() -> list[dict]:
    """Scan PNG/ directory for canonical named NPCs (one folder or .md per NPC)."""
    png_dir = ROOT / "PNG"
    out = []
    if not png_dir.exists(): return out
    for entry in sorted(png_dir.iterdir()):
        if entry.name.startswith("."): continue
        nm = entry.stem.replace("_", " ")
        out.append({"name": nm, "path": str(entry.relative_to(ROOT))})
    return out


def _dump_npcs(cat: list[dict]):
    """Print all injectable NPCs: canonical PNG/ + named catalog entries
    (those having a distinctive non-'unknown' faction AND a proper name)."""
    print("# Injectable NPCs\n")
    print("## Canonical PNG (from PNG/ directory)\n")
    for n in scan_canonical_npcs():
        print(f"- **{n['name']}**  \n  `{n['path']}`")
    print("\n## Named catalog entries (usable with --inject-npc \"<substring>\")\n")
    # Heuristic: include monsters whose name starts with a capital letter and
    # whose CR >= 5 and whose source is not a generic atlas doc.
    seen = set()
    for m in sorted(cat, key=lambda x: (-(x.get("cr") or 0), x.get("name",""))):
        nm = m.get("name","")
        if not nm or nm == "?": continue
        key = nm.lower()
        if key in seen: continue
        seen.add(key)
        if (m.get("cr") or 0) < 5: continue
        src = m.get("source_file","") or ""
        if "Armate-COMPOSIZIONE" in src or "atlas" in src.lower(): continue
        print(f"- **{nm}** (CR {m['cr']:g}, faction `{m.get('faction','-')}`)  \n  `{src}`")


# ───────────────────────── Filtering ─────────────────────────
def filter_pool(cat, env, factions: list[str], role):
    env = (env or "any").lower()
    role = (role or "").lower()
    pool = []
    for m in cat:
        if factions:
            if not any(f in m["faction"] for f in factions):
                continue
        if env and env != "any":
            if env not in m["environment"] and m["environment"] not in ("any", ""):
                continue
        if role and role not in m["role"]: continue
        pool.append(m)
    return pool

def find_npc(cat, query: str):
    q = query.lower().strip()
    cands = [m for m in cat if q in m["name"].lower()]
    if not cands: return None
    return sorted(cands, key=lambda m: -m["cr"])[0]


# ───────────────────────── Encounter builder ─────────────────────────
def build_encounter(pool, target_el, size, rng, forced: list[dict] | None = None):
    if not pool and not forced: return None
    forced = forced or []
    strategies = [
        [(target_el,   1), (max(1, target_el-4), max(0, size-1))],
        [(max(1,target_el-2), 2), (max(1, target_el-5), max(0, size-2))],
        [(max(1,target_el-4), min(size,4))],
        [(max(1,target_el-1), 1), (max(1, target_el-3), 2), (max(1, target_el-5), max(0,size-3))],
    ]
    best: dict | None = None
    for strat in strategies:
        mix, crs, ok = [], [], True
        # include forced NPCs first
        for fm in forced:
            mix.append({"monster": fm, "count": 1})
            crs.append(fm["cr"])
        remaining_slots = max(0, size - sum(e["count"] for e in mix))
        for (cr_wanted, count) in strat:
            if count <= 0 or remaining_slots <= 0: continue
            count = min(count, remaining_slots)
            cands = [m for m in pool if abs(m["cr"] - cr_wanted) <= 1.0]
            if not cands and pool:
                cands = sorted(pool, key=lambda x: abs(x["cr"]-cr_wanted))[:3]
            if not cands: ok = False; break
            pick = rng.choice(cands)
            mix.append({"monster": pick, "count": count})
            crs.extend([pick["cr"]] * count)
            remaining_slots -= count
        if not ok or not mix: continue
        el = combine_el(crs)
        score = -abs(el - target_el)
        if best is None or score > best["score"]:  # type: ignore[index]
            best = {"mix": mix, "el": el, "score": score}
    return best

def format_encounter(enc, idx, loot_tag, narrative=None):
    out = []
    el = enc["el"]
    out.append(f"### Proposal {idx} — EL {el:.1f} (rounded {round(el)})\n")
    out.append(f"<!-- loot: {loot_tag} -->")
    out.append("| # | Monster | CR | Count | Faction | Role | Source |")
    out.append("|---|---|---:|---:|---|---|---|")
    for i, e in enumerate(enc["mix"], 1):
        m = e["monster"]
        src = m.get("source_file") or "-"
        out.append(f"| {i} | {m['name']} | {m['cr']:g} | {e['count']} | "
                   f"{m.get('faction','-')} | {m.get('role','-')} | `{src}` |")
    total = sum(e["count"] for e in enc["mix"])
    crs = [e["monster"]["cr"] for e in enc["mix"] for _ in range(e["count"])]
    out.append(f"\n- **Total units**: {total}  |  **CR sum**: {sum(crs):.1f}  "
               f"|  **Combined EL**: {el:.2f}  |  **Loot**: `{loot_tag}`")
    if narrative:
        out.append(f"\n> *{narrative}*")
    return "\n".join(out)


# ───────────────────────── Alliance helpers ─────────────────────────
def resolve_alliance(alliances_data, alliance_id):
    for a in (alliances_data.get("alliances") or []):
        if a.get("id") == alliance_id:
            return a
    return None

def check_incompatibility(alliances_data, factions):
    pairs = alliances_data.get("incompatible_pairs") or []
    bad = []
    fs = set(factions)
    for p in pairs:
        if isinstance(p, list) and len(p) >= 2 and p[0] in fs and p[1] in fs:
            bad.append((p[0], p[1]))
    return bad


# ───────────────────────── Wild mode ─────────────────────────
def build_wild_encounter(wild_table, target_el, size, rng):
    monsters = wild_table.get("monsters") or []
    if not monsters: return None
    # synth pool items
    pool = []
    for m in monsters:
        if isinstance(m, dict) and m.get("cr") is not None:
            pool.append({
                "name": m.get("name","?"), "cr": float(m["cr"]),
                "faction":"wild", "role":"wild",
                "environment":"any",
                "source_file": f"SRD: {m.get('srd_ref','-')}",
            })
    if not pool: return None
    return build_encounter(pool, target_el, size, rng)


# ───────────────────────── Main ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Suggest 3.5 encounters for RumblingStone (v2).")
    ap.add_argument("--el", type=int, help="Target encounter level.")
    ap.add_argument("--env", default="any")
    ap.add_argument("--faction", default=None, help="Single faction (legacy; use --factions for multi).")
    ap.add_argument("--factions", default=None, help="Comma-separated faction list.")
    ap.add_argument("--alliance", default=None, help="Canonical alliance id.")
    ap.add_argument("--alliance-list", action="store_true")
    ap.add_argument("--inject-npc", default=None, help="Comma-separated NPC names (substring match).")
    ap.add_argument("--narrative", action="store_true", help="Include alliance narrative in output.")
    ap.add_argument("--wild", action="store_true", help="Wild (faction-less) encounter; no structured loot.")
    ap.add_argument("--role", default=None)
    ap.add_argument("--size", type=int, default=5)
    ap.add_argument("--count", type=int, default=4)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--list-factions", action="store_true")
    ap.add_argument("--list-environments", action="store_true")
    ap.add_argument("--list-npcs", action="store_true",
                    help="List all injectable NPCs (canonical PNG/ + named catalog entries).")
    ap.add_argument("--list-all", action="store_true",
                    help="Dump factions + alliances + environments + NPCs + wild envs.")
    args = ap.parse_args()

    cat = load_catalog()
    all_data = load_alliances()

    if args.list_factions:
        facs = sorted({m["faction"] for m in cat})
        print("\n".join(facs)); return 0
    if args.list_environments:
        envs = sorted({e for m in cat for e in (m["environment"] or "").split(",") if e.strip()})
        print("\n".join(envs) or "(no environments tagged)"); return 0
    if args.alliance_list:
        print("# Alliances (from faction_alliances.yaml)\n")
        for a in (all_data.get("alliances") or []):
            facs = a.get("factions") or []
            print(f"- **{a.get('id')}** — {a.get('label','')}")
            print(f"  factions: {', '.join(facs)}")
            if a.get("narrative"):
                print(f"  narrative: {a['narrative']}")
        return 0
    if args.list_npcs or args.list_all:
        _dump_npcs(cat)
        if not args.list_all: return 0
    if args.list_all:
        print("\n# Factions (14 canonical)\n")
        for f in (all_data.get("factions") or []):
            envs = ",".join(f.get("baseline_env") or [])
            print(f"- **{f.get('id')}** — {f.get('label','')} "
                  f"(env: {envs}; leader: {f.get('leader','?')})")
        print("\n# Alliances (17 canonical)\n")
        for a in (all_data.get("alliances") or []):
            print(f"- **{a.get('id')}** — {a.get('label','')}")
            print(f"  factions: {', '.join(a.get('factions') or [])}")
        print("\n# Incompatible pairs (cannot co-belligerate)\n")
        for p in (all_data.get("incompatible_pairs") or []):
            print(f"- {p[0]} ✗ {p[1]}")
        print("\n# Wild encounter environments\n")
        for env in sorted((all_data.get("wild_encounter_tables") or {}).keys()):
            tbl = (all_data.get("wild_encounter_tables") or {})[env]
            ms = tbl.get("monsters") or []
            print(f"- **{env}** — {len(ms)} monsters: "
                  + ", ".join(f"{m.get('name','?')}(CR {m.get('cr','?')})" for m in ms[:5])
                  + (" …" if len(ms) > 5 else ""))
        return 0

    if args.el is None:
        print("[suggest_encounter] --el required (e.g. --el 13).", file=sys.stderr); return 2

    rng = random.Random(args.seed)

    # ─── Wild mode ───
    if args.wild:
        tables = all_data.get("wild_encounter_tables") or {}
        env_key = args.env if args.env and args.env != "any" else None
        if not env_key or env_key not in tables:
            print(f"[suggest_encounter] --wild requires --env in: {', '.join(sorted(tables.keys()))}",
                  file=sys.stderr); return 2
        table = tables[env_key]
        narr = table.get("narrative","")
        print(f"# Wild Encounter proposals — EL {args.el}, env={env_key} (faction=wild, loot=none)")
        print(f"*{narr}*\n")
        seen, printed = set(), 0
        for _ in range(args.count * 6):
            enc = build_wild_encounter(table, args.el, args.size, rng)
            if not enc: continue
            key = tuple(sorted((e["monster"]["name"], e["count"]) for e in enc["mix"]))
            if key in seen: continue
            seen.add(key); printed += 1
            print(format_encounter(enc, printed, loot_tag="none",
                                   narrative=narr if args.narrative else None))
            print()
            if printed >= args.count: break
        if printed == 0:
            print("[suggest_encounter] Could not assemble wild encounter.", file=sys.stderr); return 4
        print("---\n*Wild encounter: no structured loot. "
              "Only natural treasure (pelts, gems in gizzards) — ignore suggest_loot.py.*")
        return 0

    # ─── Faction/alliance mode ───
    factions: list[str] = []
    alliance_info = None
    if args.alliance:
        alliance_info = resolve_alliance(all_data, args.alliance)
        if not alliance_info:
            print(f"[suggest_encounter] Unknown alliance '{args.alliance}'. "
                  f"Try --alliance-list.", file=sys.stderr); return 2
        factions = list(alliance_info.get("factions") or [])
    if args.factions:
        factions += [f.strip() for f in args.factions.split(",") if f.strip()]
    if args.faction and args.faction.lower() != "any":
        factions.append(args.faction.strip())
    factions = list(dict.fromkeys(factions))  # dedup preserving order

    # Incompatibility check
    if len(factions) >= 2:
        bad = check_incompatibility(all_data, factions)
        if bad:
            print(f"[suggest_encounter] Incompatible factions:", file=sys.stderr)
            for a,b in bad: print(f"  - {a} ✗ {b}", file=sys.stderr)
            return 3

    # Forced NPCs
    forced = []
    if args.inject_npc:
        for q in args.inject_npc.split(","):
            q = q.strip()
            if not q: continue
            npc = find_npc(cat, q)
            if npc:
                forced.append(npc)
            else:
                print(f"[suggest_encounter] NPC not found: '{q}' (skipped)", file=sys.stderr)

    pool = filter_pool(cat, args.env, factions, args.role)
    if not pool and not forced:
        print(f"[suggest_encounter] Empty pool. factions={factions or 'any'} env={args.env}",
              file=sys.stderr); return 3

    fac_label = ",".join(factions) if factions else "any"
    header = f"# Encounter proposals — EL {args.el}, env={args.env}, factions={fac_label}"
    if args.alliance: header += f", alliance={args.alliance}"
    if forced: header += f", injected={[m['name'] for m in forced]}"
    print(header)
    print(f"*Pool: {len(pool)} monsters matching filters (catalog total: {len(cat)}).*\n")
    if args.narrative and alliance_info:
        print(f"> **{alliance_info.get('label','')}** — {alliance_info.get('narrative','')}\n")

    seen, printed = set(), 0
    for _ in range(args.count * 6):
        enc = build_encounter(pool, args.el, args.size, rng, forced=forced)
        if not enc: continue
        key = tuple(sorted((e["monster"]["name"], e["count"]) for e in enc["mix"]))
        if key in seen: continue
        seen.add(key); printed += 1
        narr = alliance_info.get("narrative") if (args.narrative and alliance_info) else None
        print(format_encounter(enc, printed, loot_tag="structured", narrative=narr))
        print()
        if printed >= args.count: break
    if printed == 0:
        print("[suggest_encounter] Could not assemble any encounter.", file=sys.stderr); return 4
    print("---\n*Pipe to suggest_loot.py: `suggest_encounter ... > /tmp/enc.md && "
          "scripts/suggest_loot.py --from-encounter /tmp/enc.md --pcs 4`*")
    return 0


if __name__ == "__main__":
    sys.exit(main())
