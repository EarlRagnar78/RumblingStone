#!/usr/bin/env python3
"""
session_recap.py — Genera un recap/preview in italiano (tono R.A. Salvatore)
da dare ai player 1-2 giorni prima della prossima sessione.

Legge:
  - Gli ultimi N file `campaign/sessions/YYYY-MM-DD_session-*.md`
    (estrae SOLO sezioni pubbliche: Summary, Key decisions, XP awarded,
     Loot distributed, World events triggered, Next session hooks).
     ⚠️ La sezione `## DM notes (private — optional)` è TAGLIATA sempre.
  - `campaign/state.md` §0 dashboard + §1 party table (solo dati pubblici).

Scrive:
  - `campaign/recaps/recap-YYYY-MM-DD.md` (markdown italiano A4-friendly)
  - (opzionale) PDF via pandoc, se `--pdf` è passato e pandoc è installato.

Uso:
    python3 scripts/session_recap.py                 # ultima sessione → md
    python3 scripts/session_recap.py --last-n 2      # ultime 2 sessioni
    python3 scripts/session_recap.py --pdf           # markdown + PDF A4
    python3 scripts/session_recap.py --out custom.md

Filosofia:
  - SPOILER-SAFE: mai rivelare clock villain, piani segreti, contenuto Fase X.
  - Tono R.A. Salvatore: sensoriale, riflessivo, con presagi e natura che respira.
  - Nessuna AI/LLM: template italiani curati, output deterministico.
  - Zero dipendenze esterne (solo stdlib).
"""

from __future__ import annotations
import argparse
import re
import sys
import shutil
import subprocess
import random
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = ROOT / "campaign" / "sessions"
STATE_FILE = ROOT / "campaign" / "state.md"
RECAPS_DIR = ROOT / "campaign" / "recaps"

# Sezioni sicure da estrarre dal session log (tutto ciò che viene DOPO
# `## DM notes` viene scartato).
PUBLIC_SECTIONS = [
    "Summary",
    "Key decisions",
    "XP awarded",
    "Loot distributed",
    "World events triggered",
    "Next session hooks",
]
PRIVATE_CUT_MARKER = re.compile(r'^##\s+DM notes', re.MULTILINE | re.IGNORECASE)


# ------------------------------------------------------------------ curated prose
OPENINGS = [
    "Il vento di Mirtul porta ancora il sapore della cenere e del ferro. "
    "Ciò che è stato, resta inciso nella pietra — e nelle memorie di chi "
    "ha camminato fin qui.",
    "La notte cala sul Faerûn come un mantello vecchio, e le stelle, "
    "indifferenti, osservano. Eppure, sotto il loro sguardo, qualcosa "
    "si muove ancora: un respiro di mondo che ricorda.",
    "Dicono i nani che la pietra non dimentica. E se è vero, allora "
    "ogni passo compiuto fin qui è inciso nelle radici delle montagne, "
    "nell'eco dei martelli, nel silenzio che segue la battaglia.",
    "Nel Faerûn del 1372, anche il crepuscolo ha peso. Ogni ombra che "
    "si allunga è un ricordo; ogni respiro di vento, una promessa. "
    "E voi — Custodi Eterni — siete il filo che tiene insieme queste cose.",
]

MID_ATMOSPHERE = [
    "Le ferite non guariscono solo con la carne: guariscono con le scelte "
    "che si sono fatte, e con quelle che ancora attendono.",
    "Un ramo si spezza lontano, e il bosco trattiene il fiato. "
    "Chi ha camminato abbastanza in Faerûn sa che il silenzio, a volte, "
    "è la voce più forte.",
    "C'è un tempo in cui il mondo pare sospeso tra due battiti del cuore. "
    "Questo è quel tempo. Tra ciò che avete compiuto e ciò che verrà.",
    "Le forge degli Hammerfist bruciano ancora, basse, come braci che "
    "non vogliono spegnersi. Ogni scintilla è un nome ricordato.",
]

WORLD_REFLECTIONS = [
    "Il mondo attorno a voi non dorme. Lontano, verso sud, l'orda marcia. "
    "Vicino, qualcuno trama. E sopra tutto, il cielo di Faerûn tiene il "
    "conto dei giorni — come un vecchio scriba che non sbaglia mai.",
    "In qualche luogo, un drago apre un occhio. In un altro, una matrona "
    "drow chiude il suo. Il mondo, come sempre, si muove in due direzioni "
    "al tempo stesso.",
    "C'è chi pianifica alle spalle di mappe di cera, chi affila rituali "
    "in stanze senza finestre, chi invoca nomi che non si dovrebbero mai "
    "pronunciare. Il Faerûn che voi non vedete è grande quanto quello "
    "che camminate.",
]

HOOKS_PREFACES = [
    "Sussurri nel vento — frammenti di ciò che si sta profilando all'orizzonte:",
    "La prossima alba porta con sé le sue domande. Queste sono quelle che "
    "già si fanno sentire:",
    "Il filo del racconto non è mai spezzato. Queste sono le linee che "
    "ancora tremano, in attesa di essere tirate:",
]

CLOSINGS = [
    "Riposate, Custodi. Perché la prossima alba verrà — e con lei, "
    "il peso delle scelte che ancora vi aspettano.",
    "Il cammino non è finito. Mai lo è, per chi porta un nome che la "
    "pietra riconosce. A presto, viandanti.",
    "In Faerûn, anche il silenzio è una forma di preghiera. "
    "Portate con voi ciò che avete imparato — e siate pronti.",
    "Che Moradin vegli sulle vostre incudini, e Mielikki sui vostri "
    "sentieri. La storia che state scrivendo non è ancora finita.",
]


# ------------------------------------------------------------------ parsing
SESSION_HEADER_RE = re.compile(
    r'^#\s+Session\s+(\d+)\s+[—-]\s+(.+?)\s*\((\d{4}-\d{2}-\d{2})\)',
    re.MULTILINE | re.IGNORECASE,
)


def find_session_files(last_n: int) -> list[Path]:
    if not SESSIONS_DIR.is_dir():
        return []
    files = sorted(SESSIONS_DIR.glob("*.md"))
    # Sort by filename (should start with YYYY-MM-DD) descending, then take N.
    files = sorted(files, key=lambda p: p.name, reverse=True)[:last_n]
    return list(reversed(files))  # chronological order in output


def strip_private(content: str) -> str:
    """Rimuove tutto da `## DM notes` in poi."""
    m = PRIVATE_CUT_MARKER.search(content)
    if m:
        return content[:m.start()].rstrip() + "\n"
    return content


def parse_sections(content: str) -> dict[str, str]:
    """Estrae le sezioni pubbliche. Ritorna dict {section_name: body_md}."""
    content = strip_private(content)
    # Split by H2
    parts = re.split(r'^##\s+(.+?)\s*$', content, flags=re.MULTILINE)
    # parts[0] = header preamble; then [title, body, title, body, ...]
    sections: dict[str, str] = {}
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        # Normalize known titles
        for wanted in PUBLIC_SECTIONS:
            if title.lower().startswith(wanted.lower()):
                sections[wanted] = body
                break
    return sections


def parse_session_meta(content: str, path: Path) -> dict:
    m = SESSION_HEADER_RE.search(content)
    meta = {
        "number": None,
        "title": path.stem,
        "date": None,
        "file": path.name,
    }
    if m:
        meta["number"] = int(m.group(1))
        meta["title"] = m.group(2).strip()
        meta["date"] = m.group(3)
    # Try inline fields
    for key, label in [
        ("players", "Players present"),
        ("location", "Location"),
        ("in_world", "In-world dates"),
    ]:
        rm = re.search(rf'\*\*{re.escape(label)}\*\*[:\s]*(.+)', content)
        if rm:
            meta[key] = rm.group(1).strip()
    return meta


# ------------------------------------------------------------------ state.md (public bits only)
def extract_state_public() -> dict:
    """Estrae §0 dashboard + APL + in-world date + party table. NO villain clocks."""
    out = {
        "last_updated": None,
        "in_world_date": None,
        "apl": None,
        "dashboard_rows": [],
        "party_rows": [],
    }
    if not STATE_FILE.is_file():
        return out
    text = STATE_FILE.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'\*\*Last updated:\*\*\s*([^\n(]+)', text)
    if m:
        out["last_updated"] = m.group(1).strip()
    m = re.search(r'\*\*In-world date:\*\*\s*(.+)', text)
    if m:
        out["in_world_date"] = m.group(1).strip()
    m = re.search(r'\*\*Party APL:\*\*\s*(\d+)', text)
    if m:
        out["apl"] = m.group(1).strip()

    # Dashboard: §0 table rows
    sec = re.search(r'##\s*§?0[^\n]*At-a-Glance(.+?)(?=\n##\s)', text, re.DOTALL)
    if sec:
        for line in sec.group(1).splitlines():
            line = line.strip()
            if line.startswith("|") and not re.match(r'^\|\s*[-:| ]+\|', line):
                cells = [c.strip() for c in line.strip("|").split("|")]
                # Skip header row
                if cells and cells[0].lower() in ("arc", ""):
                    continue
                if len(cells) >= 3:
                    out["dashboard_rows"].append(cells)

    # Party table: §1
    sec = re.search(r'##\s*1\.\s*Party[^\n]*\n(.+?)(?=\n##\s)', text, re.DOTALL)
    if sec:
        for line in sec.group(1).splitlines():
            line = line.strip()
            if line.startswith("|") and not re.match(r'^\|\s*[-:| ]+\|', line):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[0].lower() in ("pc", ""):
                    continue
                if len(cells) >= 3:
                    out["party_rows"].append(cells)
    return out


# ------------------------------------------------------------------ narrative assembly
def narrative_summary_wrap(raw_summary: str) -> str:
    """Riscrive il Summary grezzo in prosa atmosferica (leggera — prefisso tonale)."""
    if not raw_summary.strip():
        return ""
    opener = random.choice([
        "Negli ultimi passi del cammino, questo è ciò che è accaduto — "
        "e che ora vive come pietra nella memoria:",
        "Il racconto recente, quello che ancora brucia come brace sotto "
        "la cenere:",
        "Ciò che le ombre hanno visto, e che le pietre di Faerûn hanno "
        "inciso a modo loro:",
    ])
    return f"{opener}\n\n{raw_summary.strip()}"


def format_hooks(raw_hooks: str) -> str:
    if not raw_hooks.strip():
        return ""
    preface = random.choice(HOOKS_PREFACES)
    return f"{preface}\n\n{raw_hooks.strip()}"


def build_recap(sessions_data: list[dict], state: dict, seed: int | None) -> str:
    if seed is not None:
        random.seed(seed)

    today = date.today().isoformat()
    lines: list[str] = []

    # Frontmatter-ish title
    lines.append(f"# Cronache dei Custodi Eterni — Recap & Preludio")
    lines.append("")
    lines.append(f"*Generato {today} · solo per i giocatori · spoiler-safe*")
    lines.append("")
    if state.get("in_world_date") or state.get("apl"):
        meta_bits = []
        if state.get("in_world_date"):
            meta_bits.append(f"**Data in-mondo**: {state['in_world_date']}")
        if state.get("apl"):
            meta_bits.append(f"**APL**: {state['apl']}")
        lines.append(" · ".join(meta_bits))
        lines.append("")

    lines.append("---")
    lines.append("")

    # Opening atmospheric
    lines.append("## I. Il Respiro del Mondo")
    lines.append("")
    lines.append(random.choice(OPENINGS))
    lines.append("")

    # Party snapshot (from state.md, public)
    if state.get("party_rows"):
        lines.append("## II. Dove siete, in questo istante")
        lines.append("")
        lines.append("| PG | Classe | Luogo | Condizione |")
        lines.append("|---|---|---|---|")
        for row in state["party_rows"]:
            # row = [PC, Class, Location, HP/status, threads...]
            pc = row[0] if len(row) > 0 else "?"
            klass = row[1] if len(row) > 1 else "?"
            loc = row[2] if len(row) > 2 else "?"
            status = row[3] if len(row) > 3 else "?"
            lines.append(f"| {pc} | {klass} | {loc} | {status} |")
        lines.append("")
        lines.append(f"*{random.choice(MID_ATMOSPHERE)}*")
        lines.append("")

    # Previously on — session logs
    if sessions_data:
        lines.append("## III. Negli episodi precedenti…")
        lines.append("")
        for sd in sessions_data:
            meta = sd["meta"]
            sec = sd["sections"]
            hdr = f"### Sessione {meta.get('number') or '?'} — {meta.get('title','')}"
            if meta.get("date"):
                hdr += f"  *(reale: {meta['date']})*"
            lines.append(hdr)
            lines.append("")
            if meta.get("location"):
                lines.append(f"*Luogo*: {meta['location']}  ")
            if meta.get("in_world"):
                lines.append(f"*Giorni in-mondo*: {meta['in_world']}")
            lines.append("")
            if sec.get("Summary"):
                lines.append(narrative_summary_wrap(sec["Summary"]))
                lines.append("")
            if sec.get("Key decisions"):
                lines.append("**Le scelte che pesano:**")
                lines.append("")
                lines.append(sec["Key decisions"])
                lines.append("")
            if sec.get("XP awarded"):
                lines.append("**Il prezzo e la ricompensa (XP):**")
                lines.append("")
                lines.append(sec["XP awarded"])
                lines.append("")
            if sec.get("Loot distributed"):
                lines.append("**Ciò che resta nelle bisacce:**")
                lines.append("")
                lines.append(sec["Loot distributed"])
                lines.append("")
            if sec.get("World events triggered"):
                lines.append("**Il mondo ha risposto così:**")
                lines.append("")
                lines.append(sec["World events triggered"])
                lines.append("")

    # Atmospheric middle
    lines.append("## IV. Il mondo attorno a voi")
    lines.append("")
    lines.append(random.choice(WORLD_REFLECTIONS))
    lines.append("")

    # Dashboard arc progress (public)
    if state.get("dashboard_rows"):
        lines.append("### Lo stato delle cose (in breve)")
        lines.append("")
        lines.append("| Arco | Fase | Stato | Note |")
        lines.append("|---|---|---|---|")
        # Show only completed + current — skip rows marked ⬜ for spoiler safety
        # (those are future arcs the DM hasn't revealed yet).
        for row in state["dashboard_rows"]:
            # Dashboard cols: [Arc, Fase-icon, Stato-text, March, PG Lv, Note]
            icon = row[1] if len(row) > 1 else ""
            status = row[2] if len(row) > 2 else ""
            # Skip future/unstarted arcs for spoiler safety
            if ("⬜" in icon or "⬜" in status
                    or "non iniziato" in status.lower()
                    or "target" in status.lower()):
                continue
            arc = row[0] if len(row) > 0 else ""
            note = row[5] if len(row) > 5 else (row[-1] if row else "")
            lines.append(f"| {arc} | {icon} | {status} | {note} |")
        lines.append("")

    # Preview hooks from LAST session only
    if sessions_data:
        last_hooks = sessions_data[-1]["sections"].get("Next session hooks", "")
        if last_hooks.strip():
            lines.append("## V. Sussurri nel vento — ciò che si profila")
            lines.append("")
            lines.append(format_hooks(last_hooks))
            lines.append("")

    # Closing
    lines.append("## VI. La prossima alba")
    lines.append("")
    lines.append(random.choice(CLOSINGS))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "*Questo documento contiene solo ciò che è già accaduto al tavolo "
        "o che è già stato mostrato in-fiction. Nessun piano del DM, "
        "nessun dettaglio ancora da scoprire. Buon viaggio, Custodi.*"
    )
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ pdf
def maybe_pdf(md_path: Path) -> Path | None:
    if not shutil.which("pandoc"):
        print("[recap] pandoc non installato: salto generazione PDF.", file=sys.stderr)
        print("        (Installa con: sudo apt install pandoc texlive-xetex "
              "fonts-dejavu)", file=sys.stderr)
        return None
    pdf_path = md_path.with_suffix(".pdf")
    cmd = [
        "pandoc", str(md_path), "-o", str(pdf_path),
        "-V", "geometry:a4paper,margin=2cm",
        "-V", "mainfont=DejaVu Serif",
        "-V", "lang=it",
        "--pdf-engine=xelatex",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[recap] PDF: {pdf_path}", file=sys.stderr)
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"[recap] pandoc error: {e.stderr[:500]}", file=sys.stderr)
        print("        Fallback: usa il markdown direttamente.", file=sys.stderr)
        return None


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(
        description="Genera un recap/preludio spoiler-safe per i player (tono R.A. Salvatore).")
    ap.add_argument("--last-n", type=int, default=1,
                    help="Numero di ultime sessioni da includere (default 1).")
    ap.add_argument("--out", type=Path, default=None,
                    help="File markdown di output. Default: campaign/recaps/recap-YYYY-MM-DD.md")
    ap.add_argument("--pdf", action="store_true",
                    help="Genera anche PDF A4 via pandoc (se installato).")
    ap.add_argument("--seed", type=int, default=None,
                    help="Seed RNG per output riproducibile (default: random).")
    args = ap.parse_args()

    RECAPS_DIR.mkdir(parents=True, exist_ok=True)

    session_files = find_session_files(args.last_n)
    sessions_data = []
    for sf in session_files:
        text = sf.read_text(encoding="utf-8", errors="ignore")
        sessions_data.append({
            "path": sf,
            "meta": parse_session_meta(text, sf),
            "sections": parse_sections(text),
        })

    if not sessions_data:
        print(f"[recap] ⚠ Nessun session log in {SESSIONS_DIR}. "
              "Creo comunque un preludio basato su state.md.", file=sys.stderr)

    state = extract_state_public()
    md = build_recap(sessions_data, state, args.seed)

    out = args.out or (RECAPS_DIR / f"recap-{date.today().isoformat()}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"[recap] Markdown: {out}", file=sys.stderr)

    if args.pdf:
        maybe_pdf(out)

    print(f"[recap] ✓ Recap generato ({len(sessions_data)} sessioni incluse).",
          file=sys.stderr)


if __name__ == "__main__":
    main()
