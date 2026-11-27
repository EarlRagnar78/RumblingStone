#!/usr/bin/env python3
"""
update_xp.py — Zero-burden XP ledger updater for RumblingStone.

Parses session logs in campaign/sessions/*.md looking for the '## XP awarded'
section (format: see campaign/templates/session-template.md) and produces
campaign/pg/xp-ledger.md with cumulative XP per PC and 3.5 level thresholds.

The DM does NOTHING new: they already fill '## XP awarded' as per template.

Usage:
    python3 scripts/update_xp.py           # update ledger
    python3 scripts/update_xp.py --check   # dry-run, print diff to stdout

Parsing rules (lenient):
  - Inside '## XP awarded' block (until next '## ' heading):
      * Lines like '- Encounter ...: N xp' or 'CR X → total Y / N = Z per PC'
        are informational.
      * The authoritative line is '**Total**: N xp a testa ...' → that N is
        assigned to every PC listed in '**Players present**:' on the file.
      * If a line contains 'PC: NAME → N xp' it overrides per-PC.
  - Session date comes from filename (YYYY-MM-DD_session-M.md) or first
    heading '# Session N — ... (YYYY-MM-DD)'.

No external deps. AGENTS.md: we never invent XP, we only sum what the DM wrote.
"""
from __future__ import annotations
import re, sys, argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
SESS = ROOT / "campaign" / "sessions"
OUT = ROOT / "campaign" / "pg" / "xp-ledger.md"

sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import sistemi as S  # noqa: E402


def soglie_di(sistema: str | None = None, traccia: str | None = None) -> tuple[dict[int, int], str]:
    """(livello → PE, etichetta) dal plugin del sistema (`pe.soglie`, ADR-0111 L4).

    Un sistema con una traccia sola (3.5) la usa; con più tracce (PF1e) vale
    `traccia`, poi l'opzione `traccia_pe` di sistemi.toml, poi «media»."""
    sistema = sistema or S.predefinito()
    if sistema not in S.attivi():
        raise SystemExit(f"[update_xp] sistema «{sistema}» non attivo in sistemi.toml (attivi: {', '.join(S.attivi())})")
    dati = S.dati(sistema, "pe.soglie")
    tracce = dati.get("soglie", {})
    if len(tracce) == 1:  # una traccia sola: --traccia non si applica
        nome, = tracce
        return {int(k): int(v) for k, v in tracce[nome].items()}, dati.get("etichetta", sistema)
    traccia = traccia or S.opzione(sistema, "traccia_pe", "media")
    if traccia not in tracce:
        raise SystemExit(f"[update_xp] {sistema}: traccia «{traccia}» assente (ci sono: {', '.join(tracce)})")
    return {int(k): int(v) for k, v in tracce[traccia].items()}, f"{sistema}, traccia {traccia}"


# Le soglie del sistema predefinito (3.5: PHB Tab. 3-2), dal plugin.
THRESHOLDS = soglie_di()[0]


def level_for_xp(xp: int, soglie: dict[int, int] | None = None) -> int:
    lvl = 1
    for L, th in (soglie or THRESHOLDS).items():
        if xp >= th:
            lvl = L
    return lvl

def next_threshold(xp: int, soglie: dict[int, int] | None = None) -> tuple[int,int]:
    soglie = soglie or THRESHOLDS
    lvl = level_for_xp(xp, soglie)
    nxt = soglie.get(lvl+1, soglie[max(soglie)])
    return lvl, max(0, nxt - xp)

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# Accetta Total/Totale, un ~ opzionale e il separatore migliaia (es. "~1.025 xp")
TOTAL_RE = re.compile(r"\*\*Total[e]?\*\*\s*:\s*~?\s*([\d.]+)\s*xp", re.IGNORECASE)
PER_PC_RE = re.compile(r"^\s*-\s*([A-Za-z][A-Za-z' -]+?)\s*(?:→|->|:)\s*(\d+)\s*xp", re.IGNORECASE | re.MULTILINE)
PLAYERS_RE = re.compile(r"\*\*Players present\*\*\s*:\s*(.+)")

def extract_pcs(line: str) -> list[str]:
    # e.g. "Alice (Hella), Bob (Tordek), ..."
    pcs = []
    for chunk in re.split(r"[,;]", line):
        m = re.search(r"\(([^)]+)\)", chunk)
        if m:
            pcs.append(m.group(1).strip())
        else:
            t = chunk.strip()
            if t and not t.lower().startswith("none"):
                pcs.append(t)
    return pcs

def parse_session(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    # date
    m = DATE_RE.search(path.name) or DATE_RE.search(text[:400])
    date = m.group(1) if m else "0000-00-00"
    # players
    pm = PLAYERS_RE.search(text)
    pcs = extract_pcs(pm.group(1)) if pm else []
    # XP block
    xp_block = ""
    m2 = re.search(r"##\s*XP awarded\s*\n(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    if m2:
        xp_block = m2.group(1)
    # total
    total = 0
    mt = TOTAL_RE.search(xp_block)
    if mt:
        total = int(mt.group(1).replace(".", ""))  # "1.025" → 1025
    # per-PC overrides
    overrides = {}
    for mm in PER_PC_RE.finditer(xp_block):
        name = mm.group(1).strip()
        if name.lower() in ("encounter", "total", "note", "boss"):
            continue
        overrides[name] = int(mm.group(2))
    if total == 0 and not overrides:
        return None
    return {"file": path.name, "date": date, "pcs": pcs, "total": total, "overrides": overrides}

def build_ledger(sessions: list[dict], soglie: dict[int, int] | None = None,
                 etichetta: str = "3.5") -> str:
    # accumulate per PC chronologically
    sessions.sort(key=lambda s: (s["date"], s["file"]))
    pc_rows: dict[str, list[tuple]] = {}
    for s in sessions:
        # union of pcs + overrides keys
        names = set(s["pcs"]) | set(s["overrides"].keys())
        for name in sorted(names):
            gained = s["overrides"].get(name, s["total"])
            if gained <= 0: continue
            prev = pc_rows.get(name, [])
            cum = (prev[-1][3] if prev else 0) + gained
            prev.append((s["date"], s["file"], gained, cum))
            pc_rows[name] = prev

    lines = []
    lines.append("# XP Ledger — RumblingStone\n")
    lines.append("*Auto-generated by `scripts/update_xp.py` from `campaign/sessions/*.md`.*  ")
    lines.append("*Do not edit by hand — edit the session log's `## XP awarded` block instead.*\n")
    lines.append(f"_Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    if etichetta != "3.5":
        lines.append(f"_Soglie di livello: {etichetta} (sistemi.toml, ADR-0111)._\n")
    if not pc_rows:
        lines.append("\n*(No session logs with XP found yet.)*\n")
        return "\n".join(lines)
    # summary
    lines.append("## Current status\n")
    lines.append("| PC | Cumulative XP | Level | To next level |")
    lines.append("|---|---:|---:|---:|")
    for name, rows in sorted(pc_rows.items()):
        cum = rows[-1][3]
        lvl, togo = next_threshold(cum, soglie)
        lines.append(f"| {name} | {cum:,} | {lvl} | {togo:,} |")
    lines.append("")
    # per-PC history
    for name, rows in sorted(pc_rows.items()):
        lines.append(f"\n### {name}\n")
        lines.append("| Date | Session | XP gained | Cumulative | Level |")
        lines.append("|---|---|---:|---:|---:|")
        for (d, f, g, c) in rows:
            lines.append(f"| {d} | `{f}` | {g:,} | {c:,} | {level_for_xp(c, soglie)} |")
    lines.append("")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="print diff, don't write")
    ap.add_argument("--sistema", default=None,
                    help="sistema di gioco delle soglie (sistemi.toml; predefinito dnd35)")
    ap.add_argument("--traccia", choices=("lenta", "media", "veloce"), default=None,
                    help="traccia PE PF1e (predefinita: opzioni.pf1e.traccia_pe)")
    args = ap.parse_args()
    soglie, etichetta = soglie_di(args.sistema, args.traccia)
    if not SESS.exists():
        print(f"[update_xp] No {SESS} directory — nothing to do.")
        return 0
    sessions = []
    for p in sorted(SESS.glob("*.md")):
        r = parse_session(p)
        if r: sessions.append(r)
    content = build_ledger(sessions, soglie, etichetta)
    if args.check:
        sys.stdout.write(content)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if old == content:
        print(f"[update_xp] No changes. {len(sessions)} session(s) processed.")
        return 0
    OUT.write_text(content, encoding="utf-8")
    print(f"[update_xp] Wrote {OUT.relative_to(ROOT)} ({len(sessions)} sessions).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
