#!/usr/bin/env python3
"""eco_decisioni.py — un blocco di decisioni chiuse insieme vuole la sua eco.

L9 di PIANO-AGENT-SKILLS-ESTERNE (D6 del 2026-10-01). Quando il DM chiude piu'
decisioni in un messaggio solo («D1 ok, d2 ok, d4 ok ma dopo…»), l'agente
rimanda l'eco prima di toccare i file: cosa e' deciso, cosa resta aperto, cosa
ha cambiato posizione, e **a parte** cosa ha dedotto lui. Le aggiunte non
chieste sono il punto in cui un «ok» diventa una cosa che il DM non ha detto.

La norma vive in `skills/rumblingstone-plans/SKILL.md` («L'eco prima di
applicare»). Questo script la misura sulle tabelle che `decisioni_dm.py` gia'
legge, senza una regex nuova sulle tabelle: per ogni piano, le decisioni
chiuse con «Decisa il AAAA-MM-GG» si raggruppano per data; due o piu' nella
stessa data, da `DATA_INIZIO` in poi, chiedono nel file del piano:

    <!-- eco: <ETICHETTA> <AAAA-MM-GG> -->
    - **Decise**: …
    - **Aperte**: …
    - **Cambiate**: …
    - **Dedotto da me**: …

Le chiusure di prima della norma si contano e non bloccano: la norma non si
applica all'indietro, e scriverne l'eco oggi sarebbe inventarla.

    python3 scripts/eco_decisioni.py           # il conto
    python3 scripts/eco_decisioni.py --check   # esce 1 se un'eco manca
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decisioni_dm as dd  # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
DATA_INIZIO = "2026-10-01"
SOGLIA = 2
CAMPI = ("Decise", "Aperte", "Cambiate", "Dedotto da me")
RIGHE_DEL_BLOCCO = 20

_DATA = re.compile(r"Decis[ao]\s+il\s+(\d{4}-\d{2}-\d{2})")
_ECO = re.compile(r"^<!--\s*eco:\s*(?P<etichetta>\S+)\s+(?P<data>\d{4}-\d{2}-\d{2})\s*-->$")


def file_delle_etichette(radice: Path) -> "dict[str, Path]":
    out = {}
    for md in sorted((radice / "plans").glob("*.md")):
        for riga in md.read_text(encoding="utf-8").split("\n"):
            m = dd.MARKER.match(riga.strip())
            if m:
                out.setdefault(m.group("etichetta"), md)
    return out


def blocchi(radice: Path) -> "dict[tuple[str, str], list[str]]":
    """(etichetta, data) -> le decisioni chiuse quel giorno."""
    decisioni, _ = dd.leggi_fonti(radice)
    out: "dict[tuple[str, str], list[str]]" = defaultdict(list)
    for d in decisioni:
        if d.aperta:
            continue
        m = _DATA.search(d.testo.replace("*", ""))
        if m:
            out[(d.piano, m.group(1))].append(d.ident)
    return out


_IDENT = re.compile(r"\bD\d+\b")


def eco_presente(testo: str, etichetta: str, data: str) -> "tuple[list[str], set[str]]":
    """(campi mancanti, decisioni nominate nelle righe **Decise**).

    Nello stesso giorno le eco possono essere piu' d'una: il DM puo' chiudere un
    blocco la mattina e un altro la sera. Ognuna deve avere i quattro campi, e
    insieme devono nominare ogni decisione chiusa quel giorno. ['marker'] se non
    ce n'e' nessuna.
    """
    righe = testo.split("\n")
    mancanti: "list[str]" = []
    nominate: "set[str]" = set()
    trovate = 0
    for i, r in enumerate(righe):
        m = _ECO.match(r.strip())
        if not (m and m.group("etichetta") == etichetta and m.group("data") == data):
            continue
        trovate += 1
        blocco = righe[i + 1:i + 1 + RIGHE_DEL_BLOCCO]
        corpo = "\n".join(blocco)
        mancanti += [c for c in CAMPI if f"**{c}**" not in corpo and c not in mancanti]
        for b in blocco:
            if "**Decise**" in b:
                nominate |= set(_IDENT.findall(b.replace("~", "")))
    return (["marker"] if not trovate else mancanti), nominate


def esamina(radice: Path = RADICE) -> "tuple[list[str], list[str], int]":
    """(problemi, eco a posto, chiusure di prima della norma)."""
    files = file_delle_etichette(radice)
    problemi, a_posto, prima = [], [], 0
    for (etichetta, data), idents in sorted(blocchi(radice).items()):
        if len(idents) < SOGLIA:
            continue
        if data < DATA_INIZIO:
            prima += 1
            continue
        f = files.get(etichetta)
        mancano, nominate = eco_presente(f.read_text(encoding="utf-8"), etichetta, data) if f else (["file"], set())
        nome = f.name if f else etichetta
        chi = f"{nome} · {etichetta} {data} ({', '.join(idents)})"
        tacite = [x for x in idents if x not in nominate]
        if mancano == ["marker"]:
            problemi.append(f"{chi}: manca «<!-- eco: {etichetta} {data} -->»")
        elif mancano:
            problemi.append(f"{chi}: l'eco non ha {', '.join('**' + c + '**' for c in mancano)}")
        elif tacite:
            problemi.append(f"{chi}: nessuna eco nomina fra le **Decise** {', '.join(tacite)}")
        else:
            a_posto.append(chi)
    return problemi, a_posto, prima


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--radice", type=Path, default=RADICE)
    a = ap.parse_args(argv)
    problemi, a_posto, prima = esamina(a.radice)
    for p in a_posto:
        print(f"✓ {p}")
    for p in problemi:
        print(f"✗ {p}")
    print(f"{'✗' if problemi else '✓'} eco_decisioni: {len(a_posto)} blocchi con l'eco, "
          f"{len(problemi)} senza; {prima} blocchi chiusi prima del {DATA_INIZIO}, non misurati")
    return 1 if (a.check and problemi) else 0


if __name__ == "__main__":
    sys.exit(main())
