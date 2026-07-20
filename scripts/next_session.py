#!/usr/bin/env python3
"""
next_session.py — brief DM + teaser player per la prossima sessione
(Lotto E del piano AUTOMAZIONE-STATO-SESSIONI).

AGGREGATORE DETERMINISTICO, non uno sceneggiatore: incrocia ciò che il DM
ha già scritto — niente AI, niente invenzioni (AGENTS.md).

Legge:
  - campaign/state.md: March Day corrente, dashboard §0 (finestre "Day X-Y"),
    party §1 (posizione/thread per PG), clock villain §3 vicini alla soglia;
  - campaign/sessions/: sezione `## Next session hooks` delle ultime N sessioni;
  - i dossier hook per-PG esistenti (`*HOOKS-<PG>-*.md`): linkati, mai riassunti
    (ADR-0003: il canone resta nei master).

Scrive (artefatti generati, mai canone):
  campaign/next/brief-YYYY-MM-DD-DM.md          ⚠️ SOLO DM (clock e finestre in chiaro)
  campaign/next/teaser-YYYY-MM-DD-PLAYERS.md    spoiler-safe, da girare ai giocatori
  campaign/next/homebrew/*.hb.md                vesti Homebrewery V3 (con --hype)

Uso:
    python3 scripts/next_session.py                # ultimo log, output markdown
    python3 scripts/next_session.py --last-n 2 --hype
    python3 scripts/dm.py session next --hype      # equivalente orchestrato

Spoiler-safety del teaser: costruito SOLO dagli hook (sezione pubblica del
template) + party; una guardia finale rifiuta l'output se contiene pattern
DM-only (clock, finestre Day X-Y, CR). Zero dipendenze, deterministico.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402

def _paths(repo: Path) -> "tuple[Path, Path, Path]":
    return (repo / "campaign" / "state.md",
            repo / "campaign" / "sessions",
            repo / "campaign" / "next")

MARCH_DAY_RE = re.compile(r"\*\*Current March Day:\*\*\s*\*\*(\d+)\*\*")
WINDOW_RE = re.compile(r"Day\s*(\d+)\s*[-–]\s*(\d+)")
SINGLE_DAY_RE = re.compile(r"Day\s*(\d+)\b")
CLOCK_RE = re.compile(r"\b(\d+)\s*/\s*(\d+)\b")
HOOKS_SECTION_RE = re.compile(
    r"^##\s*Next session hooks\s*\n(.*?)(?=^##\s|\Z)", re.M | re.S | re.I)

#: Pattern che NON devono mai comparire nel teaser player (cintura finale).
SPOILER_PATTERNS = [re.compile(p, re.I) for p in
                    (r"\bclock\b", r"\b\d+\s*/\s*\d+\b", r"\bDay\s*\d+", r"\bCR\s*\d+",
                     r"DM only", r"SOLO DM")]

GENERATED_NOTE = ("<!-- Auto-generated da scripts/next_session.py — non editare "
                  "a mano, rigenera con `dm.py session next`. -->\n\n")


# ------------------------------------------------------------------ parsing


def _table_rows(text: str, heading_re: str) -> list[list[str]]:
    """Righe (celle) della prima tabella markdown dopo l'heading dato."""
    h = re.search(heading_re, text, re.M)
    if not h:
        return []
    rows: list[list[str]] = []
    in_table = False
    for line in text[h.end():].splitlines():
        if line.startswith("|"):
            in_table = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= {"-", ":", " "} for c in cells):
                continue  # separatore |---|
            rows.append(cells)
        elif in_table:
            break
        elif line.startswith("## "):
            break
    return rows[1:] if rows else []  # scarta l'header


def current_march_day(state_text: str) -> "int | None":
    m = MARCH_DAY_RE.search(state_text)
    return int(m.group(1)) if m else None


def upcoming_windows(state_text: str, today_day: int) -> list[dict]:
    """Righe della dashboard §0 non completate con finestra Day che incombe."""
    out = []
    for cells in _table_rows(state_text, r"^##\s*§0\b.*$"):
        if len(cells) < 6 or cells[1].startswith("✅") or "completato" in cells[2]:
            continue
        arc, _fase, stato, clock_cell = cells[0], cells[1], cells[2], cells[3]
        m = WINDOW_RE.search(clock_cell)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
        else:
            s = SINGLE_DAY_RE.search(clock_cell)
            if not s:
                continue
            lo = hi = int(s.group(1))
        if hi < today_day:
            urgency = "⚫ scaduta"
        elif hi - today_day <= 5:
            urgency = "🔴 urgente"
        elif hi - today_day <= 10:
            urgency = "🟡 vicina"
        else:
            urgency = "🟢 lontana"
        out.append({"arc": arc, "stato": stato, "lo": lo, "hi": hi,
                    "urgency": urgency, "left": hi - today_day})
    return sorted(out, key=lambda w: w["hi"])


def party_rows(state_text: str) -> list[list[str]]:
    return _table_rows(state_text, r"^##\s*1\.\s*Party\b.*$")


def hot_villain_clocks(state_text: str, threshold: int = 2) -> list[tuple[str, int, int]]:
    out = []
    for cells in _table_rows(state_text, r"^##\s*3\.\s*Active Villain\b.*$"):
        if len(cells) < 4:
            continue
        m = CLOCK_RE.search(cells[3])
        if m:
            n, tot = int(m.group(1)), int(m.group(2))
            if 0 < tot - n <= threshold:
                out.append((cells[0].split("—")[0].strip(), n, tot))
    return out


def collect_hooks(sessions_dir: Path, last_n: int) -> list[dict]:
    """Hook delle ultime N sessioni: [{'file','date','hooks':[...]}]."""
    files = sorted(sessions_dir.glob("????-??-??_session-*.md"))[-last_n:]
    out = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace")
        m = HOOKS_SECTION_RE.search(text)
        hooks = []
        if m:
            hooks = [ln.lstrip("- ").strip()
                     for ln in m.group(1).splitlines()
                     if ln.strip().startswith("-") and "[x]" not in ln.lower()]
        out.append({"file": p.name, "date": p.name[:10], "hooks": hooks})
    return out


def hook_dossier_link(repo: Path, hook: str, pg_names: list[str]) -> "str | None":
    """Se l'hook riguarda un PG con un dossier HOOKS-<PG> esistente, linka
    il master invece di riassumerlo (ADR-0003)."""
    for name in pg_names:
        if name.lower() in hook.lower():
            hits = sorted(p for p in repo.rglob(f"*HOOKS-{name}*")
                          if ".git" not in p.parts)
            if hits:
                return str(hits[0].relative_to(repo))
    return None


# ------------------------------------------------------------------ output


def render_brief(repo: Path, today_day: "int | None", windows: list[dict],
                 party: list[list[str]], clocks: list[tuple[str, int, int]],
                 sessions: list[dict], pg_names: list[str]) -> str:
    o: list[str] = []
    o.append(GENERATED_NOTE)
    o.append("# Brief prossima sessione — ⚠️ SOLO DM\n")
    o.append("> Clock, finestre e deadline IN CHIARO: non condividere coi player.\n"
             "> Aggregato deterministico da state.md + session log — il canone\n"
             "> resta nei file citati; qui non è stato inventato nulla.\n")
    o.append(f"\n**March Day corrente:** {today_day if today_day is not None else '(?)'} "
             f"· generato il {date.today().isoformat()}\n")

    o.append("\n## Finestre che incombono (dashboard §0)\n")
    if windows:
        o.append("| Urgenza | Arc/quest | Finestra | Giorni residui | Stato |")
        o.append("|---|---|---|---|---|")
        for w in windows:
            win = f"Day {w['lo']}" + (f"-{w['hi']}" if w["hi"] != w["lo"] else "")
            o.append(f"| {w['urgency']} | {w['arc']} | {win} | {w['left']} | {w['stato']} |")
    else:
        o.append("*(nessuna finestra rilevata — controlla §0 a mano)*")

    o.append("\n## Dove sono i PG (party §1)\n")
    if party:
        o.append("| PG | Posizione | Thread personali aperti |")
        o.append("|---|---|---|")
        for cells in party:
            if len(cells) >= 5:
                o.append(f"| {cells[0]} | {cells[2]} | {cells[4]} |")
    else:
        o.append("*(tabella party non trovata in state.md §1)*")

    o.append("\n## Clock villain vicini alla soglia (§3)\n")
    if clocks:
        for who, n, tot in clocks:
            o.append(f"- ⏰ **{who}** — {n}/{tot}: manca{'no' if tot - n > 1 else ''} "
                     f"{tot - n} tick al trigger (rileggi la riga in §3)")
    else:
        o.append("*(nessun clock a ≤2 tick dalla soglia)*")

    o.append("\n## Hook aperti dalle ultime sessioni\n")
    for s in sessions:
        o.append(f"\n### {s['file']}\n")
        if not s["hooks"]:
            o.append("*(nessun hook registrato)*")
        for h in s["hooks"]:
            link = hook_dossier_link(repo, h, pg_names)
            o.append(f"- {h}" + (f"\n  ↳ dossier: `{link}`" if link else ""))
    o.append("\n---\n*Chiudi un hook giocato marcandolo `- [x]` nel session log: "
             "sparirà dai prossimi brief.*\n")
    return "\n".join(o)


def render_teaser(sessions: list[dict]) -> str:
    hooks = [h for s in sessions for h in s["hooks"]]
    seed = sum(ord(c) for c in (sessions[-1]["date"] if sessions else "x"))
    opening = OPENINGS[seed % len(OPENINGS)]
    o = [GENERATED_NOTE]
    o.append("# Sussurri per la prossima sessione\n")
    o.append(f"*{opening}*\n")
    if hooks:
        o.append("\nQuesto giunge alle vostre orecchie, tra fuochi da campo "
                 "e strade polverose:\n")
        for h in hooks:
            o.append(f"- {h}")
    o.append("\n*Dove porterà il prossimo passo, lo decidete voi.*\n")
    return "\n".join(o)


# frasi d'apertura riusate dal tono di session_recap (curate, deterministiche)
OPENINGS = [
    "Il vento d'estate della Valle porta ancora il sapore della cenere e del ferro.",
    "La notte cala sul Faerûn come un mantello vecchio, e le stelle osservano.",
    "Dicono i nani che la pietra non dimentica: ogni passo è inciso nelle montagne.",
    "Anche il crepuscolo ha peso, nel 1372: ogni ombra che si allunga è un ricordo.",
]


def guard_teaser(text: str) -> None:
    for rx in SPOILER_PATTERNS:
        if rx.search(text):
            print(f"[next] ✗ teaser bloccato: contiene materiale DM-only "
                  f"(pattern {rx.pattern!r})", file=sys.stderr)
            raise SystemExit(1)


def hb_wrap(body: str, title: str, dm_only: bool) -> str:
    head = ("<!-- Auto-generated — do not edit by hand. "
            "Rigenera con `dm.py session next --hype`. -->\n\n")
    cover = f"{{{{wide\n# {title}\n}}}}\n\n"
    warn = ("{{note\n⚠️ **MATERIALE DM** — non incollare in brew condivisi "
            "coi giocatori.\n}}\n\n" if dm_only else "")
    foot = "\n{{pageNumber,auto}}\n{{footnote RUMBLINGSTONE · PROSSIMA SESSIONE}}\n"
    body = re.sub(r"^<!--.*?-->\n\n", "", body, flags=re.S)  # niente doppio header
    return head + cover + warn + body + foot


# ------------------------------------------------------------------ main


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(
        description="Brief DM + teaser player per la prossima sessione "
                    "(aggregatore deterministico).")
    ap.add_argument("--last-n", type=int, default=1,
                    help="quante sessioni recenti scandire per gli hook (default 1)")
    ap.add_argument("--hype", action="store_true",
                    help="genera anche le vesti Homebrewery V3 in campaign/next/homebrew/")
    ap.add_argument("--out-dir", type=Path, default=None, help=argparse.SUPPRESS)
    ap.add_argument("--repo-root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    repo = args.repo_root.resolve()
    state, sessions_dir, out_default = _paths(repo)
    if not state.exists():
        print(f"[next] ✗ {state} non trovato", file=sys.stderr)
        return 1
    state_text = state.read_text(encoding="utf-8", errors="replace")
    today_day = current_march_day(state_text)
    sessions = collect_hooks(sessions_dir, args.last_n)
    if not sessions:
        print(f"[next] ✗ nessun log in {sessions_dir}", file=sys.stderr)
        return 1
    party = party_rows(state_text)
    pg_names = [c[0].split()[0] for c in party if c]
    windows = upcoming_windows(state_text, today_day) if today_day is not None else []
    clocks = hot_villain_clocks(state_text)

    brief = render_brief(repo, today_day, windows, party, clocks, sessions, pg_names)
    teaser = render_teaser(sessions)
    guard_teaser(teaser)

    out = args.out_dir or out_default
    out.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    brief_path = out / f"brief-{stamp}-DM.md"
    teaser_path = out / f"teaser-{stamp}-PLAYERS.md"
    brief_path.write_text(brief, encoding="utf-8")
    teaser_path.write_text(teaser, encoding="utf-8")
    print(f"[next] ✓ brief DM:      {brief_path}")
    print(f"[next] ✓ teaser player: {teaser_path}")

    if args.hype:
        hb = out / "homebrew"
        hb.mkdir(parents=True, exist_ok=True)
        (hb / f"brief-{stamp}-DM.hb.md").write_text(
            hb_wrap(brief, "Dossier della Prossima Sessione", dm_only=True),
            encoding="utf-8")
        (hb / f"teaser-{stamp}.hb.md").write_text(
            hb_wrap(teaser, "Sussurri dalla Valle", dm_only=False),
            encoding="utf-8")
        print(f"[next] ✓ vesti Homebrewery in {hb}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
