#!/usr/bin/env python3
"""estrai_liste.py — le liste di classe e di dominio degli incantesimi 3.5, dall'SRD.

Ogni incantesimo dell'SRD 3.5 (`spells/spells-*.md`) ha la riga «Level: Clr 2,
Sor/Wiz 2, Luck 2»: da lì escono le liste per classe e per dominio, nella
stessa forma di `sistemi/pf1e/dati/liste_incantesimi.toml`. Solo nomi e livelli.
La riga sotto il titolo («Conjuration (Creation) [Acid]») dà la scuola: la tabella
`[scuole]` serve al generatore per la scuola di Incantesimi focalizzati.

Uso:
  python3 estrai_liste.py            # scrive sistemi/dnd35/dati/liste_incantesimi.toml
  python3 estrai_liste.py --check    # esce 1 se il file non è aggiornato
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ESCE = ROOT / "sistemi" / "dnd35" / "dati" / "liste_incantesimi.toml"
SIGLE = {"Brd": ["bard"], "Clr": ["cleric"], "Drd": ["druid"], "Pal": ["paladin"], "Rgr": ["ranger"],
         "Sor/Wiz": ["sorcerer", "wizard"], "Wiz": ["wizard"], "Sor": ["sorcerer"]}


#: le scuole a cui si applica Incantesimi focalizzati («Any» e «Universal» no)
SCUOLE = ("Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy",
          "Transmutation")


def leggi(cartella: Path) -> "tuple[dict, dict, dict]":
    liste: dict = {}
    domini: dict = {}
    scuole: dict = {}
    for f in sorted(cartella.glob("spells-*.md")):
        nome = None
        attesa = None   # il titolo di cui si aspetta la riga della scuola
        for riga in f.read_text(encoding="utf-8").splitlines():
            if riga.startswith("## "):
                nome = attesa = riga[3:].strip()
                continue
            if attesa and riga.strip():
                prima = riga.split()[0]
                if prima in SCUOLE:
                    scuole[attesa] = prima.lower()
                attesa = None
            m = re.match(r"\*\*Level:\*\*\s*(.+)", riga)
            if not (m and nome):
                continue
            for voce in m.group(1).split(","):
                k = re.fullmatch(r"\s*([A-Za-z/]+)\s+(\d)\s*", voce)
                if not k:
                    continue
                sigla, liv = k.group(1), k.group(2)
                if sigla in SIGLE:
                    for classe in SIGLE[sigla]:
                        liste.setdefault(classe, {}).setdefault(liv, []).append(nome)
                else:
                    domini.setdefault(sigla.lower(), {}).setdefault(liv, []).append(nome)
            nome = None
    return liste, domini, scuole


def scrivi(liste: dict, domini: dict, scuole: dict) -> str:
    n = len({x for c in liste.values() for v in c.values() for x in v})
    righe = ["# sistemi/dnd35/dati/liste_incantesimi.toml — le liste di classe e di dominio 3.5 (ADR-0124 §10)",
             "# Generato da plans/esperimenti/incantesimi-35-2026-11-12/estrai_liste.py dalla riga «Level:»",
             "# di ogni incantesimo dell'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c). Non si scrive a mano.",
             f"# {n} incantesimi, {len(liste)} classi, {len(domini)} domini. Stregone e mago hanno la stessa lista.",
             "# Mancano le liste di adepto, assassino e guardia nera: nell'SRD stanno nel testo della classe."]
    for titolo, gruppo in (("liste", liste), ("domini", domini)):
        for classe in sorted(gruppo):
            righe += ["", f'[{titolo}."{classe}"]']
            for liv in sorted(gruppo[classe]):
                righe.append(f'"{liv}" = ' + json.dumps(sorted(gruppo[classe][liv]), ensure_ascii=False))
    righe += ["", "# la scuola di ogni incantesimo, dalla riga sotto il titolo (solo le otto scuole di",
              "# Incantesimi focalizzati: «Universal» e «Any» restano fuori)", "[scuole]"]
    righe += [f"{json.dumps(n, ensure_ascii=False)} = {json.dumps(scuole[n])}" for n in sorted(scuole)]
    return "\n".join(righe) + "\n"


def main(argv: "list[str]") -> int:
    cartella = next(Path.home().glob(".cache/rumblingstone/srd/srd-v3.5-md-*/spells"))
    testo = scrivi(*leggi(cartella))
    if "--check" in argv:
        ok = ESCE.exists() and ESCE.read_text(encoding="utf-8") == testo
        print("liste_incantesimi.toml", "aggiornato" if ok else "DA RIGENERARE")
        return 0 if ok else 1
    ESCE.write_text(testo, encoding="utf-8")
    print(testo.splitlines()[3])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
