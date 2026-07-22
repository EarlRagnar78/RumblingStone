#!/usr/bin/env python3
"""
suggest_loot.py — STANDALONE loot generator for RumblingStone (D&D 3.5).

Consumes either:
  (A) A markdown file produced by suggest_encounter.py (contains
      `<!-- loot: structured|none -->` tags + monster table + Combined EL line), OR
  (B) Direct flags: --el N [--factions a,b] [--units "name:cr,name:cr"]

Output: Markdown loot block per DMG 3.5 Table 3-5 (treasure by EL).
  * loot=none (wild encounters) → minimal natural treasure one-liner.
  * loot=structured → coins + gems + art + mundane + 1-3 magic items
    from SRD pool, 0-1 faction signature item (if factions given),
    0-1 FR-themed mild item (if --include-fr-themed).

Examples:
  python3 scripts/suggest_loot.py --from-encounter /tmp/enc.md --pcs 4 --seed 42
  python3 scripts/suggest_loot.py --el 13 --factions red-hand,drow-sonjak --pcs 5
  python3 scripts/suggest_loot.py --el 11 --wild
"""
from __future__ import annotations
import sys, argparse, random, re
from pathlib import Path

# Reuse the tolerant YAML loader from suggest_encounter.py
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from suggest_encounter import load_yaml  # noqa: E402

LOOT_TABLES = HERE / "loot_tables.yaml"
MAGIC_ITEMS = HERE / "magic_items_srd.yaml"


# ───────────────────────── Parsing encounter markdown ─────────────────────────
def parse_encounter_md(path: Path):
    """Extract (loot_tag, combined_el, factions, proposals) from a
    suggest_encounter.py markdown output. Returns dict with keys:
      loot: 'structured'|'none'
      el: float
      factions: list[str]
      proposals: list of per-proposal dicts (el, loot, factions).
    If multiple proposals exist, the caller chooses which to use;
    by default we return the *first* proposal."""
    text = path.read_text(encoding="utf-8")
    # Try to extract factions= from the header line.
    factions: list[str] = []
    m = re.search(r"factions=([a-z0-9,\-_/]+)", text)
    if m:
        raw = m.group(1)
        if raw not in ("any",):
            factions = [f.strip() for f in raw.split(",") if f.strip() and f != "any"]
    # Split by proposal header.
    chunks = re.split(r"^### Proposal \d+", text, flags=re.MULTILINE)
    proposals = []
    for ch in chunks[1:]:
        loot = "structured"
        mt = re.search(r"<!--\s*loot:\s*(\w+)\s*-->", ch)
        if mt:
            loot = mt.group(1).strip()
        me = re.search(r"\*\*Combined EL\*\*:\s*([\d.]+)", ch)
        el = float(me.group(1)) if me else None
        # Extract factions from table column 5 (| faction | role | source |)
        p_factions = set()
        for row in re.finditer(r"^\|\s*\d+\s*\|[^|]+\|[^|]+\|[^|]+\|\s*([^|]+?)\s*\|",
                               ch, flags=re.MULTILINE):
            f = row.group(1).strip()
            if f and f not in ("-", "wild", "unknown"):
                p_factions.add(f)
        proposals.append({"el": el, "loot": loot,
                          "factions": sorted(p_factions) or factions})
    if not proposals:
        # maybe wild single-header doc
        loot = "none" if "loot: none" in text else "structured"
        me = re.search(r"\*\*Combined EL\*\*:\s*([\d.]+)", text)
        el = float(me.group(1)) if me else None
        proposals = [{"el": el, "loot": loot, "factions": factions}]
    return proposals


# ───────────────────────── Treasure math ─────────────────────────
def clamp_el(el: float) -> int:
    e = int(round(el))
    return max(1, min(20, e))

def split_treasure(row: dict, density: float):
    gp_total = row["gp"] * density
    coins = gp_total * row["coins_pct"] / 100.0
    goods = gp_total * row["goods_pct"] / 100.0
    items = gp_total * row["items_pct"] / 100.0
    return gp_total, coins, goods, items

def format_coins(gp: float) -> str:
    # split coins: 30% pp, 40% gp, 30% sp roughly
    # Use round() before int() to avoid floating-point truncation errors
    # (e.g. 30.999999999999996 → 30 instead of 31).
    pp = int(round(gp * 0.02))       # pp = 10gp each → small component
    gold = int(round(gp * 0.70))
    sp = int(round((gp - pp * 10 - gold) * 10))
    if sp < 0: sp = 0
    parts = []
    if pp: parts.append(f"{pp} pp")
    if gold: parts.append(f"{gold} gp")
    if sp: parts.append(f"{sp} sp")
    return ", ".join(parts) if parts else f"{int(gp)} gp"

def pick_gems(budget: float, pool: list[dict], rng, limit: int = 6) -> list[tuple[int, dict]]:
    out = []
    remaining = budget
    attempts = 0
    while remaining > 50 and len(out) < limit and attempts < 40:
        attempts += 1
        cands = [g for g in pool if g["price_avg"] <= remaining * 1.1]
        if not cands: break
        g = rng.choice(cands)
        count = 1 if g["price_avg"] > remaining/2 else rng.randint(1, max(1, int(remaining // g["price_avg"])))
        count = min(count, 4)
        out.append((count, g))
        remaining -= g["price_avg"] * count
    return out

def tier_for_el(el: int, tiers: dict) -> list[str]:
    """Return list of tier names appropriate for this EL."""
    out = []
    for name, spec in tiers.items():
        if spec["el_min"] <= el <= spec["el_max"]:
            out.append(name)
    return out or ["medium_lesser"]


# ───────────────────────── Magic item picking ─────────────────────────
def pick_magic_items(budget: float, el: int, magic_data: dict, factions: list[str],
                     rng, include_fr: bool, max_items: int = 3):
    tiers = load_yaml(LOOT_TABLES).get("magic_item_tiers") or {}
    valid_tiers = tier_for_el(el, tiers)
    srd_pool = []
    for t in valid_tiers:
        srd_pool += [{**it, "tier": t} for it in (magic_data.get("srd_items", {}).get(t) or [])]
    picked = []
    remaining = budget
    # 1 faction signature if factions given
    if factions:
        sig_pool = []
        fac_sigs = magic_data.get("faction_signatures", {}) or {}
        for f in factions:
            for it in (fac_sigs.get(f) or []):
                if it.get("price", 99999) <= remaining * 1.2:
                    sig_pool.append({**it, "faction_tag": f, "source": "faction-signature"})
        if sig_pool:
            it = rng.choice(sig_pool)
            picked.append(it)
            remaining -= it.get("price", 0)
    # 0-1 FR-themed mild if opted in
    if include_fr and remaining > 1500:
        fr_pool = [
            {**it, "source": "fr-themed-mild"}
            for it in (magic_data.get("fr_themed_mild") or [])
            if it.get("price", 99999) <= remaining * 1.1
            and (not factions or not it.get("faction_tags")
                 or any(f in (it.get("faction_tags") or []) for f in factions))
        ]
        if fr_pool and rng.random() < 0.7:
            it = rng.choice(fr_pool)
            picked.append(it)
            remaining -= it.get("price", 0)
    # Fill rest with SRD items
    attempts = 0
    while remaining > 500 and len(picked) < max_items and attempts < 30:
        attempts += 1
        cands = [it for it in srd_pool if it.get("price", 99999) <= remaining * 1.1]
        if not cands: break
        it = rng.choice(cands)
        picked.append({**it, "source": "srd"})
        remaining -= it.get("price", 0)
    return picked, remaining


# ───────────────────────── Mundane pick ─────────────────────────
def pick_mundane(budget: float, pool: list[dict], rng, limit: int = 3):
    out = []
    remaining = budget
    attempts = 0
    while remaining > 50 and len(out) < limit and attempts < 20:
        attempts += 1
        cands = [m for m in pool if m["price_avg"] <= remaining * 1.1]
        if not cands: break
        m = rng.choice(cands)
        count = 1 if m["price_avg"] > remaining/2 else rng.randint(1, 3)
        out.append((count, m))
        remaining -= m["price_avg"] * count
    return out


# ───────────────────────── Output formatting ─────────────────────────
def render_loot(el: float, factions: list[str], loot_tag: str, pcs: int,
                density: float, seed_hint: int | None, rng, no_magic: bool,
                include_fr: bool) -> str:
    out = []
    el_int = clamp_el(el if el is not None else 10)
    out.append(f"## Loot — EL {el:.1f} (row {el_int})" if el is not None
               else f"## Loot — EL ? (row {el_int})")
    sub = []
    if factions: sub.append(f"factions: `{', '.join(factions)}`")
    sub.append(f"pcs: {pcs}")
    sub.append(f"density: ×{density:.2f}")
    if seed_hint is not None: sub.append(f"seed: {seed_hint}")
    out.append(f"*{' · '.join(sub)}*\n")

    if loot_tag == "none":
        out.append("> **Wild encounter** — nessun tesoro strutturato.")
        out.append(">")
        out.append("> Solo **tesoro naturale** (discrezione DM): pellame, zanne,"
                   " gemme nello stomaco, 1d4 × 10 gp equivalenti in sottoprodotti"
                   " biologici/commerciali. Nessun magic item.")
        return "\n".join(out)

    loot_yaml = load_yaml(LOOT_TABLES)
    tb_raw = loot_yaml.get("treasure_by_el") or {}
    tbl = tb_raw.get(el_int) or tb_raw.get(str(el_int))
    if not tbl:
        out.append(f"> ⚠ EL {el_int} fuori range tabella (1-20).")
        return "\n".join(out)

    gp_total, coins_gp, goods_gp, items_gp = split_treasure(tbl, density)

    # Coins
    out.append(f"### Monete (~{int(coins_gp)} gp)")
    out.append(f"- {format_coins(coins_gp)}")

    # Gems + art
    gems_pool = loot_yaml.get("gems") or []
    art_pool = loot_yaml.get("art") or []
    out.append(f"\n### Gemme & Arte (~{int(goods_gp)} gp)")
    # split 60/40
    gem_budget = goods_gp * 0.6
    art_budget = goods_gp * 0.4
    for count, g in pick_gems(gem_budget, gems_pool, rng):
        out.append(f"- {count}× **{g['name']}** (~{g['price_avg']} gp cad.)")
    for count, a in pick_gems(art_budget, art_pool, rng, limit=3):
        out.append(f"- {count}× **{a['name']}** (~{a['price_avg']} gp cad.)")

    # Mundane + magic
    mundane_pool = loot_yaml.get("mundane") or []
    out.append(f"\n### Oggetti mondani & masterwork (~{int(items_gp*0.25)} gp)")
    for count, m in pick_mundane(items_gp * 0.25, mundane_pool, rng):
        out.append(f"- {count}× **{m['name']}** (~{m['price_avg']} gp cad.)")

    # Magic
    if not no_magic:
        magic_data = load_yaml(MAGIC_ITEMS)
        magic_budget = items_gp * 0.75
        picked, leftover = pick_magic_items(magic_budget, el_int, magic_data,
                                            factions, rng, include_fr)
        out.append(f"\n### Oggetti magici (budget ~{int(magic_budget)} gp)")
        if not picked:
            out.append("- *(nessun oggetto magico pescato entro budget — DM aggiunga manualmente)*")
        for it in picked:
            src = it.get("source", "srd")
            tag = {"srd": "SRD", "faction-signature": f"Faction: {it.get('faction_tag','?')}",
                   "fr-themed-mild": "FR-themed (mild)"}.get(src, src)
            price = it.get("price", "?")
            line = f"- **{it['name']}** — {price} gp · _[{tag}]_"
            if it.get("desc"):
                line += f"  \n  {it['desc']}"
            if it.get("srd_basis"):
                line += f"  \n  _SRD basis_: {', '.join(it['srd_basis'])}"
            out.append(line)
        if leftover > 500:
            out.append(f"\n*Budget residuo non allocato: ~{int(leftover)} gp "
                       "(convertibile in gemme extra o carryover).*")
    else:
        out.append("\n*Magic items disabilitati (--no-magic).*")

    # Per-PC split
    out.append(f"\n### Divisione per PG ({pcs} PG)")
    out.append(f"- Valore totale atteso: ~{int(gp_total)} gp")
    out.append(f"- Quota a testa (se dividono tutto): ~{int(gp_total/pcs)} gp")

    out.append(f"\n---\n*Generato da `suggest_loot.py` · DMG 3.5 Tab. 3-5 · "
               f"magic items solo meccanica SRD*")
    return "\n".join(out)


# ───────────────────────── Main ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Standalone loot generator (D&D 3.5 SRD).")
    ap.add_argument("--from-encounter", default=None,
                    help="Markdown file from suggest_encounter.py")
    ap.add_argument("--proposal", type=int, default=1,
                    help="Which proposal to use if multiple (1-based, default 1).")
    ap.add_argument("--el", type=float, default=None, help="Target EL (if not using --from-encounter).")
    ap.add_argument("--factions", default=None, help="Comma-separated factions.")
    ap.add_argument("--wild", action="store_true", help="Force wild/no-loot output.")
    ap.add_argument("--pcs", type=int, default=4)
    ap.add_argument("--no-magic", action="store_true")
    ap.add_argument("--dense", action="store_true", help="+25%% treasure.")
    ap.add_argument("--sparse", action="store_true", help="-25%% treasure.")
    ap.add_argument("--include-fr-themed", action="store_true",
                    help="Allow FR-themed mild items in the pool.")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--all-proposals", action="store_true",
                    help="Generate loot for every proposal in the encounter file.")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    density_cfg = load_yaml(LOOT_TABLES).get("density_modifiers") or {
        "dense": 1.25, "sparse": 0.75, "normal": 1.0
    }
    density = density_cfg["normal"]
    if args.dense: density = density_cfg["dense"]
    if args.sparse: density = density_cfg["sparse"]

    proposals = None
    if args.from_encounter:
        p = Path(args.from_encounter)
        if not p.exists():
            print(f"[suggest_loot] file not found: {p}", file=sys.stderr); return 2
        proposals = parse_encounter_md(p)
        if not proposals:
            print("[suggest_loot] no proposals found in file.", file=sys.stderr); return 3

    if args.wild:
        el = args.el if args.el is not None else 10.0
        factions = []
        print(render_loot(el, factions, "none", args.pcs, density, args.seed, rng,
                          args.no_magic, args.include_fr_themed))
        return 0

    if proposals:
        targets = proposals if args.all_proposals else [proposals[min(args.proposal-1, len(proposals)-1)]]
        for i, pr in enumerate(targets, 1):
            el = pr["el"] if pr["el"] is not None else (args.el or 10.0)
            factions = pr["factions"] or (args.factions.split(",") if args.factions else [])
            factions = [f.strip() for f in factions if f.strip()]
            loot_tag = pr["loot"] or "structured"
            if len(targets) > 1:
                print(f"\n\n<!-- Proposal {i} loot -->\n")
            print(render_loot(el, factions, loot_tag, args.pcs, density, args.seed,
                              rng, args.no_magic, args.include_fr_themed))
        return 0

    # direct mode
    if args.el is None:
        print("[suggest_loot] --el required (or --from-encounter).", file=sys.stderr); return 2
    factions = [f.strip() for f in (args.factions or "").split(",") if f.strip()]
    print(render_loot(args.el, factions, "structured", args.pcs, density, args.seed,
                      rng, args.no_magic, args.include_fr_themed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
