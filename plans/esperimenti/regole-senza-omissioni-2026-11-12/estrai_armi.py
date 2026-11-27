#!/usr/bin/env python3
"""Lotto 2 di ADR-0126: la tabella delle armi dell'SRD 3.5 in `sistemi/dnd35/dati/armi.toml`.

Legge «Table: Weapons» di `basic-rules-and-legal/equipment.md` (SRD in cache,
OGL) e i nomi italiani di `scripts/lessico_it_35.tsv` (categoria
«equipaggiamento»). Scrive solo nomi e numeri: dado per taglia Media, critico,
impugnatura, gittata. Deterministico: stesso ingresso, stessi byte.

Uso: python3 estrai_armi.py CARTELLA_SRD > sistemi/dnd35/dati/armi.toml
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# nomi con cui le schede del repo chiamano un'arma e che il lessico non ha
ALTRI_NOMI = {
    "Greatclub": ["randello pesante", "randello enorme", "grande randello"],
    "Greataxe": ["grande ascia", "ascia a due mani"],
    "Morningstar": ["morning star", "stella del mattino"],
    "Quarterstaff": ["bastone da viaggio"],
    "Lance": ["lancia da carica", "lancia da cavaliere"],
    "Longspear": ["picca lunga", "picca"],
    "Flail": ["flagello"],
    "Shield, heavy": ["colpo di scudo pesante", "scudo pesante"],
    "Shield, light": ["colpo di scudo leggero", "scudo leggero"],
    "Unarmed strike": ["colpo senz'armi", "pugno"],
    "Battleaxe": ["ascia da battaglia"],
    "Falchion": ["falchion"],
    "Club": ["randello"],
    "Waraxe, dwarven": ["ascia nanica"],
    "Dart": ["dardo", "dardi"],
    "Javelin": ["giavellotti"],
    "Shuriken (5)": ["shuriken"],
}

CODA = """# Il dado al cambiare della taglia di chi impugna (SRD 3.5, Equipment, «Weapon
# Size», Table: Tiny and Large Weapon Damage). `su` = una taglia in più, `giu` =
# una in meno, a partire dal dado della taglia Media.
[scala.su]
"1d2" = "1d3"
"1d3" = "1d4"
"1d4" = "1d6"
"1d6" = "1d8"
"1d8" = "2d6"
"1d10" = "2d8"
"1d12" = "3d6"
"2d4" = "2d6"
"2d6" = "3d6"
"2d8" = "3d8"
"3d6" = "4d6"
"3d8" = "4d8"
"4d6" = "6d6"
"4d8" = "6d8"

[scala.giu]
"1d2" = "1"
"1d3" = "1d2"
"1d4" = "1d3"
"1d6" = "1d4"
"1d8" = "1d6"
"1d10" = "1d8"
"1d12" = "1d10"
"2d4" = "1d6"
"2d6" = "1d10"
"2d8" = "2d6"

# Passi di taglia rispetto alla Media, coi nomi che le schede scrivono in `tipo:`.
[taglie]
"fine" = -4
"piccolissima" = -4
"piccolissimo" = -4
"diminutive" = -3
"minuta" = -3
"minuto" = -3
"tiny" = -2
"minuscola" = -2
"minuscolo" = -2
"small" = -1
"piccola" = -1
"piccolo" = -1
"medium" = 0
"media" = 0
"medio" = 0
"large" = 1
"grande" = 1
"huge" = 2
"enorme" = 2
"gargantuan" = 3
"mastodontica" = 3
"mastodontico" = 3
"colossal" = 4
"colossale" = 4

# Bonus al danno che una scheda può dichiarare con un talento (SRD 3.5, Feats).
[[sorgenti]]
nome = "Arma Specializzata"
schema = '(?:weapon specialization|arma specializzata)(?! superiore)'
valore = 2
fonte = "SRD 3.5, Feats, «Weapon Specialization»"

[[sorgenti]]
nome = "Arma Specializzata Superiore"
schema = '(?:greater weapon specialization|arma specializzata superiore)'
valore = 2
fonte = "SRD 3.5, Feats, «Greater Weapon Specialization»"

[[sorgenti]]
nome = "specialista del martello (livello di sostituzione del chierico nano)"
schema = '(?:hammer specialist|specialista del martello)'
valore = 2
armi = ["Warhammer"]
fonte = "D&D 3.5, Races of Stone (solo nome e numero)"
"""


def _pulito(s: str) -> str:
    s = re.sub(r"<sup>.*?</sup>", "", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


def righe(srd: Path):
    testo = (srd / "basic-rules-and-legal" / "equipment.md").read_text(encoding="utf-8")
    tabella = re.search(r"<caption>Table: Weapons</caption>(.*?)</table>", testo, re.S).group(1)
    competenza = impugnatura = ""
    for tr in re.findall(r"<tr>(.*?)</tr>", tabella, re.S):
        th = re.findall(r"<th[^>]*>(.*?)</th>", tr, re.S)
        if th:
            competenza = {"Simple": "semplice", "Martial": "da guerra", "Exotic": "esotica"}[th[0].split()[0]]
            continue
        celle = [(_pulito(c), "sup>5<" in c, "sup>4<" in c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if len(celle) == 1:
            t = celle[0][0]
            impugnatura = ("leggera" if t.startswith("Light") else "una mano" if t.startswith("One")
                           else "due mani" if t.startswith("Two") else "distanza" if t.startswith("Ranged")
                           else "leggera" if t.startswith("Unarmed") else impugnatura)
            continue
        nome, _costo, _piccola, media, critico, gittata = [c[0] for c in celle[:6]]
        if not re.match(r"\d", media):
            continue
        yield {"nome": nome, "competenza": competenza, "impugnatura": impugnatura,
               "dado": media.split("/")[0], "critico": critico.replace("–", "-"),
               "gittata": gittata if re.match(r"\d", gittata) else "",
               "doppia": celle[0][1], "portata": celle[0][2]}


def nomi_italiani() -> dict:
    fuori: dict = {}
    for riga in (ROOT / "scripts" / "lessico_it_35.tsv").read_text(encoding="utf-8").splitlines():
        p = riga.split("\t")
        if len(p) >= 3 and p[2] == "equipaggiamento":
            fuori.setdefault(p[1].lower(), []).append(p[0].lower())
    return fuori


def main() -> int:
    srd = Path(sys.argv[1])
    it = nomi_italiani()
    print("# sistemi/dnd35/dati/armi.toml — le armi dell'SRD 3.5 (ADR-0126, lotto 2)\n#\n"
          "# Scritto da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_armi.py\n"
          "# da «Table: Weapons» (SRD 3.5, Equipment) e dai nomi italiani di\n"
          "# scripts/lessico_it_35.tsv. Solo nomi e numeri. Non si modifica a mano.\n#\n"
          "# dado = danno per taglia Media; critico = «19-20/x2», oppure il solo\n"
          "# moltiplicatore («3») quando la minaccia è il 20.\n")
    for r in righe(srd):
        crit = r["critico"]
        m = re.fullmatch(r"(\d+)-20/x(\d)", crit)
        minaccia, molt = (int(m.group(1)), int(m.group(2))) if m else (20, int(re.search(r"\d", crit).group(0)))
        virgola = r["nome"].split(", ")
        inglese = [r["nome"].lower()] + ([f"{virgola[1]} {virgola[0]}".lower()] if len(virgola) == 2 else [])
        nomi = sorted(set(inglese + it.get(r["nome"].lower(), []) + ALTRI_NOMI.get(r["nome"], [])))
        print("[[armi]]")
        print(f'nome = "{r["nome"]}"')
        print("nomi = [" + ", ".join(f'"{n}"' for n in nomi) + "]")
        print(f'dado = "{r["dado"]}"')
        print(f"minaccia = {minaccia}")
        print(f"moltiplicatore = {molt}")
        print(f'impugnatura = "{r["impugnatura"]}"')
        print(f'competenza = "{r["competenza"]}"')
        if r["gittata"]:
            print(f'gittata = "{r["gittata"]}"')
        if r["doppia"]:
            print("doppia = true")
        if r["portata"]:
            print("portata = true")
        print()
    print(CODA, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
