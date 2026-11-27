#!/usr/bin/env python3
"""riscontra_modelli.py — i numeri di `sistemi/pf1e/dati/modelli.toml` contro il PRD.

`modelli.toml` è scritto a mano (sette righe di regola). Questo script rilegge
le sezioni «Simple Templates» del Bestiary nel PRD in cache e controlla che
ogni numero del file ci sia davvero. Non scrive niente.

    python3 plans/esperimenti/regole-senza-omissioni-2026-11-12/riscontra_modelli.py

Esce con 1 se un numero non torna, con 2 se la cache del PRD non c'è.
"""
from __future__ import annotations

import html
import re
import sqlite3
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = Path.home() / ".cache/rumblingstone/srd/PSRD-Data-76ea47846041"
INGLESE = {"advanced": "Advanced Creature", "giant": "Giant Creature", "young": "Young Creature",
           "celestial": "Celestial Creature", "fiendish": "Fiendish Creature",
           "entropic": "Entropic Creature", "resolute": "Resolute Creature"}
CAR = {"For": "Str", "Des": "Dex", "Cos": "Con"}
ENERGIA = {"acido": "acid", "freddo": "cold", "fuoco": "fire", "elettricità": "electricity"}
ALLINEAMENTO = {"male": "evil", "bene": "good", "legale": "lawful", "caotico": "chaotic"}
PUNIRE = {"il male": "smite evil", "il bene": "smite good", "la legge": "smite law",
          "il caos": "smite chaos"}


def _testo(c: sqlite3.Connection, section_id: int) -> str:
    """La sezione e tutte le sue figlie, in testo semplice."""
    pezzi, coda = [], [section_id]
    while coda:
        sid = coda.pop(0)
        for nome, corpo in c.execute("select name, body from sections where section_id=?", (sid,)):
            pezzi.append(f"{nome} {corpo or ''}")
        coda.extend(r[0] for r in c.execute(
            "select section_id from sections where parent_id=? order by section_id", (sid,)))
    t = re.sub(r"<[^>]+>", " ", html.unescape(" ".join(pezzi)))
    return re.sub(r"\s+", " ", t).replace("–", "-").replace("—", "-")


def riscontra() -> list[str]:
    dati = tomllib.loads((ROOT / "sistemi/pf1e/dati/modelli.toml").read_text(encoding="utf-8"))
    c = sqlite3.connect(CACHE / "book-b1.db")
    errori = []
    for chiave, m in dati["modelli"].items():
        riga = c.execute("select section_id from sections where name=?", (INGLESE[chiave],)).fetchone()
        if not riga:
            errori.append(f"{chiave}: sezione «{INGLESE[chiave]}» assente nel PRD")
            continue
        t = _testo(c, riga[0])

        def serve(cosa: str, schema: str) -> None:
            if not re.search(schema, t, re.I):
                errori.append(f"{chiave}: {cosa} non riscontrato ({schema})")

        if "gs_da_dv" in m:
            serve("GS +1 da 5 DV", rf"CR increases by \+{m['gs']} only if the base creature has "
                                   rf"{m['gs_da_dv']} or more HD")
        else:
            serve("GS", r"As base creature ?" + re.escape(f"{m['gs']:+d}"))
        for car, delta in m.get("caratteristiche", {}).items():
            if chiave == "advanced":
                serve("caratteristiche", rf"\+{delta} to all ability scores")
            else:
                serve(car, re.escape(f"{delta:+d}") + rf"( size bonus to)? [\w ,+-]*{CAR[car]}")
        if "int_minima" in m:
            serve("Intelligenza minima", rf"except Int scores of {m['int_minima'] - 1} or less")
        if "naturale" in m:
            serve("armatura naturale", "natural armor by " + re.escape(f"{m['naturale']:+d}"))
        if m.get("taglia"):
            serve("taglia", "Size increase by one category" if m["taglia"] > 0
                  else "Size decrease by one category")
        if m.get("dadi"):
            serve("dadi", "increase dice rolled by 1 step" if m["dadi"] > 0
                  else "decrease damage dice by 1 step")
        if "resistenze" in m:
            serve("scurovisione", r"darkvision 60 ft")
            for r in m["resistenze"]:
                serve(f"resistenza {r}", rf"Resist [\w ,]*{ENERGIA[r]}")
            serve("RD", rf"5/{ALLINEAMENTO[m['rd']]} 11\+ 15 10/{ALLINEAMENTO[m['rd']]}")
            serve("fasce", r"1-4 5 - 5-10 10 5/")
            serve("RI", rf"SR equal to new CR \+{dati['modelli_regole']['ri_oltre_il_gs']}")
            serve("punire", rf"{PUNIRE[m['punire']]} {dati['modelli_regole']['punire_al_giorno']}/day")
    return errori


def main() -> int:
    if not (CACHE / "book-b1.db").is_file():
        print(f"✗ riscontra_modelli: manca la cache del PRD in {CACHE}", file=sys.stderr)
        return 2
    errori = riscontra()
    for e in errori:
        print(f"✗ {e}")
    if not errori:
        print("✓ riscontra_modelli: i sette modelli tornano col PRD (Bestiary, Simple Templates)")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
