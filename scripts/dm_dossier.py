#!/usr/bin/env python3
"""
dm_dossier.py — Il DOSSIER DEL DM in veste Homebrewery V3 (Lotto K-B7).

Un solo documento, sempre rigenerabile, con TUTTI i fili della campagna:
cruscotto archi, clock della Marcia e del Rituale, trame dei villain,
conoscenze dei PNG, promesse/debiti, stato artefatti, trame aperte.
Ogni capitolo è incorniciato da un'introduzione d'atmosfera in stile
Red Hand of Doom; il CONTENUTO è estratto ALLA LETTERA da
`campaign/state.md` (la fonte di verità: qui non si inventa una riga).

⚠️ MATERIALE DM — è l'esatto contrario del recap player-safe: contiene
clock, deadline e piani segreti IN CHIARO. Non incollarlo in brew
condivisi coi giocatori.

Uso:
    python3 scripts/dm_dossier.py            # → campaign/DM-DOSSIER.hb.md
    python3 scripts/dm.py dossier            # equivalente

Stdlib only, deterministico, idempotente (design rules del toolkit).
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
STATE = REPO / "campaign" / "state.md"
OUT = REPO / "campaign" / "DM-DOSSIER.hb.md"

sys.path.insert(0, str(SCRIPTS))
from session_recap import harptos_label  # noqa: E402  (ancora Harptos condivisa)

# Capitoli: (titolo sezione in state.md → titolo dossier, intro stile RHoD)
CHAPTERS = [
    ("§0 Campaign Status At-a-Glance", "Il quadro della guerra",
     "La Valle brucia a sud e le Dale trattengono il fiato. Questo è il "
     "punto esatto in cui la storia è arrivata — e ciò che ancora attende, "
     "riga per riga, senza veli."),
    ("2. Active Forces", "Gli eserciti in movimento",
     "Diecimila stendardi rossi marciano al ritmo dei tamburi hobgoblin. "
     "Ogni giorno che passa è un villaggio in meno e una decisione in più. "
     "I due orologi qui sotto non si fermano mai."),
    ("3. Active Villain Threads", "Le mani nell'ombra",
     "Mentre i Custodi guardano avanti, altri guardano loro. Questi sono i "
     "conti alla rovescia dei nemici: quando uno arriva a fondo scala, il "
     "mondo cambia — che i PG se ne accorgano o no."),
    ("4. Open NPC Knowledge State", "Chi sa cosa",
     "In Faerûn i segreti pesano più dell'oro. Questa è la contabilità di "
     "ciò che ogni PNG sa, sospetta o giura di non aver mai sentito."),
    ("5. Open Promises, Debts, Bargains", "Promesse, debiti e patti",
     "Le parole date hanno radici lunghe. Qui sono elencate tutte: quelle "
     "dei PG al mondo, e quelle del mondo ai PG. Nessuna scade in silenzio."),
    ("6. Artifact State", "Il respiro degli artefatti",
     "Corona, martello, anello, collana, bracieri: oggetti che ricordano. "
     "Questo è il loro stato REALE oggi — poteri accesi, non promesse."),
    ("7. Open Narrative Threads", "I fili aperti del racconto",
     "Ogni filo lasciato libero prima o poi si tende. Questa è la tela "
     "completa: trame maggiori, sotto-trame, echi in attesa di riemergere."),
]

HEADER = """<!-- Auto-generated — do not edit by hand.
     Sorgente: campaign/state.md (fonte di verità — il dossier ESTRAE, non riscrive)
     Rigenera con: python3 scripts/dm.py dossier
     ⚠️ MATERIALE DM: clock e piani IN CHIARO. Mai ai giocatori. -->

{{frontCover}}

{{logo ![](/assets/naturalCritLogoRed.svg)}}

# RUMBLING STONE
## Dossier del Dungeon Master
___

### Tutti i fili della campagna, in un colpo d'occhio

{{banner ⚠️ SOLO DM}}

{{footnote
  Generato il %REAL% · %WORLD% · fonte: campaign/state.md · Red Hand of Doom, Faerûn 1372 DR
}}

\\page
"""

FOOTER = ("\n{{descriptive\n##### Come si usa\nRigenera questo dossier dopo "
          "ogni sessione (`dm.py post`, poi `dm.py dossier`): è la fotografia "
          "di `state.md` — se una riga qui è sbagliata, correggi il canone in "
          "state.md, mai questo file. Le prossime scene dell'arco in corso "
          "sono nel QUICKSTART di `ARC07-00-INDICE.md`.\n}}\n")


def split_sections(text: str) -> dict[str, str]:
    """Mappa 'titolo ## esatto' → corpo, per ogni sezione di state.md."""
    out: dict[str, str] = {}
    parts = re.split(r'^##\s+', text, flags=re.M)
    for part in parts[1:]:
        title, _, body = part.partition("\n")
        out[title.strip()] = body.rstrip()
    return out


def find_section(sections: dict[str, str], key: str) -> str | None:
    for title, body in sections.items():
        if key.lower() in title.lower():
            return body
    return None


def current_march_day(text: str) -> int | None:
    m = re.search(r'Current March Day:\*{0,2}\s*\*{0,2}(\d+)', text)
    return int(m.group(1)) if m else None


def main() -> int:
    if not STATE.is_file():
        print("[dossier] ✗ campaign/state.md non trovato", file=sys.stderr)
        return 1
    text = STATE.read_text(encoding="utf-8", errors="ignore")
    sections = split_sections(text)
    day = current_march_day(text)
    world = harptos_label(day) or "data in-mondo da state.md"
    m = re.search(r'\*\*In-world date:\*\*\s*(.+)', text)
    if m:
        world = f"{m.group(1).strip()} · {world}"

    lines = [HEADER.replace("%REAL%", date.today().isoformat())
                   .replace("%WORLD%", world)]
    pagefoot = "{{pageNumber,auto}}\n{{footnote DOSSIER DEL DM · SOLO DM}}\n"

    for key, title, intro in CHAPTERS:
        body = find_section(sections, key.split(" ", 1)[1] if key[0] == "§"
                            else key.split(". ", 1)[1])
        if body is None:
            continue
        lines.append(f"# {title}\n")
        lines.append(f"{{{{descriptive\n*{intro}*\n}}}}\n")
        lines.append(body.strip() + "\n")
        lines.append(pagefoot)
        lines.append("\\page\n")

    # niente \page orfano in coda
    if lines and lines[-1] == "\\page\n":
        lines.pop()
    lines.append(FOOTER)

    OUT.write_text("\n".join(lines), encoding="utf-8")
    rel = OUT.relative_to(REPO)
    print(f"[dossier] ✓ {rel} — incollalo in un brew PRIVATO (mai ai giocatori)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
