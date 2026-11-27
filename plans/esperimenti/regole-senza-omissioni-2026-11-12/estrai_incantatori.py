#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/incantatori.toml` dalle tabelle dell'SRD 3.5.

Uso: python3 estrai_incantatori.py <cartella srd-v3.5-md> > sistemi/dnd35/dati/incantatori.toml
     python3 estrai_incantatori.py <PSRD-Data/book-cr.db> > sistemi/pf1e/dati/incantatori.toml

Legge «Table: The Bard / Cleric / Druid / Paladin / Ranger / Sorcerer /
Wizard», «Table: The Adept», «Bard Spells Known», «Sorcerer Spells Known» e
«Table: Ability Modifiers and Bonus Spells». Solo numeri: nessun testo
dell'SRD entra nel file. Una cella «—» diventa -1 (la classe non lancia a quel
livello d'incantesimo), uno 0 resta 0 (solo incantesimi bonus). La tabella dei
bonus si riduce a una formula, che lo script riscontra riga per riga.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

CLASSI = {  # didascalia → (chiave, caratteristica, modo, dominio, nomi italiani)
    "The Bard": ("bard", "Car", "spontaneo", False, ["bardo"]),
    "The Cleric": ("cleric", "Sag", "preparato", True, ["chierico", "chierica"]),
    "The Druid": ("druid", "Sag", "preparato", False, ["druido", "druida"]),
    "The Paladin": ("paladin", "Sag", "preparato", False, ["paladino", "paladina"]),
    "The Ranger": ("ranger", "Sag", "preparato", False, ["ranger"]),
    "The Sorcerer": ("sorcerer", "Car", "spontaneo", False, ["stregone", "stregona"]),
    "The Wizard": ("wizard", "Int", "preparato", False, ["mago", "maga"]),
    "The Adept": ("adept", "Sag", "preparato", False, ["adepto", "adepta"]),
}
CONOSCIUTI = {"Bard Spells Known": "bard", "Sorcerer Spells Known": "sorcerer"}


def tabelle(testo: str):
    for m in re.finditer(r"<table[^>]*><caption>Table: ([^<]+)</caption>(.*?)</table>", testo, re.S):
        righe = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(2), re.S):
            celle = [html.unescape(re.sub(r"<sup>.*?</sup>|<[^>]+>", "", c)).strip()
                     for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
            righe.append(celle)
        yield m.group(1).strip(), righe


def numero(c: str) -> int:
    c = c.replace("+1", "").strip()          # «1+1» del chierico: il +1 è lo slot di dominio
    return -1 if c in ("—", "-", "–", "") else int(c)


def griglia(righe) -> dict[int, list[int]]:
    """Livello di classe → celle per livello d'incantesimo, dall'indice 0. Le
    colonne si riconoscono dall'intestazione («0», «1st», …): una tabella senza
    la colonna dello 0 ha -1 in quella posizione."""
    colonne: dict[int, int] = {}
    fuori = {}
    for r in righe:
        liv_col = {i: (0 if c == "0" else int(c[:-2])) for i, c in enumerate(r)
                   if re.fullmatch(r"0|[1-9](?:st|nd|rd|th)", c)}
        if len(liv_col) >= 4 and not colonne:
            # l'intestazione può stare su una riga più corta (rowspan): si allinea a destra
            colonne = {i - len(r): l for i, l in liv_col.items()}
            continue
        m = re.match(r"(\d+)(?:st|nd|rd|th)$", r[0]) if r else None
        if not m or not colonne:
            continue
        riga = [-1] * (max(colonne.values()) + 1)
        for i, l in colonne.items():
            riga[l] = numero(r[i])
        while riga and riga[-1] == -1:
            riga.pop()
        fuori[int(m.group(1))] = riga
    return fuori


def bonus(mod: int, livello: int) -> int:
    """Incantesimi bonus al giorno per modificatore e livello d'incantesimo."""
    return 0 if livello < 1 or mod < livello else 1 + (mod - livello) // 4


def sorgenti(dove: Path) -> "tuple[str, str]":
    """(sistema, html delle tabelle) da una cartella dell'SRD 3.5 o dal book-cr.db del PRD PF1e."""
    if dove.is_dir():
        return "dnd35", "\n".join((dove / "basic-rules-and-legal" / f).read_text(encoding="utf-8") for f in
                                  ("character-classes-i.md", "character-classes-ii.md", "npc-classes.md",
                                   "basics-and-ability-scores.md"))
    import sqlite3
    con = sqlite3.connect(dove)
    return "pf1e", "\n".join(corpo for (corpo,) in con.execute(
        "select body from sections where type='table' and name like 'Table: %' order by section_id"))


def main() -> int:
    sistema, testo = sorgenti(Path(sys.argv[1]))
    if sistema == "pf1e":
        # PRD: «Table: Bard», il paladino lancia col Carisma
        for k in list(CLASSI):
            v = CLASSI.pop(k)
            CLASSI[k.replace("The ", "")] = (v[0], "Car" if v[0] == "paladin" else v[1], *v[2:])
    al_giorno, noti = {}, {}
    for titolo, righe in tabelle(testo):
        if titolo in CLASSI:
            g = griglia(righe)
            assert len(g) == 20, (titolo, len(g))
            al_giorno[CLASSI[titolo][0]] = g
        elif titolo in CONOSCIUTI:
            g = griglia(righe)
            assert len(g) == 20, (titolo, len(g))
            noti[CONOSCIUTI[titolo]] = g
        elif titolo == "Ability Modifiers and Bonus Spells":
            visti = 0
            for r in righe:
                m = re.match(r"[+]?(\d+)$", r[1]) if len(r) == 12 else None
                if not m:
                    continue
                for liv in range(1, 10):
                    assert bonus(int(m.group(1)), liv) == max(0, numero(r[2 + liv])), (r, liv)
                visti += 1
            assert visti >= 17, visti
    assert set(al_giorno) == {v[0] for v in CLASSI.values()}, sorted(al_giorno)
    assert set(noti) == set(CONOSCIUTI.values())
    out = ["# Scritto da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_incantatori.py:",
           "# non si modifica a mano. Fonte: " + ("SRD 3.5" if sistema == "dnd35" else "PRD PF1e (PSRD-Data, book-cr)") + ", tabelle delle classi (solo numeri).",
           "# -1 = la classe non lancia a quel livello; 0 = solo incantesimi bonus.",
           "", "[bonus]",
           '# «Table: Ability Modifiers and Bonus Spells», riscontrata riga per riga dallo script',
           'formula = "0 se mod < livello o livello < 1, altrimenti 1 + (mod - livello) // 4"',
           'minimo_per_lanciare = "10 + livello dell\'incantesimo"', ""]
    for titolo, (k, car, modo, dominio, nomi) in CLASSI.items():
        out += [f"[classi.{k}]", f'fonte = "{"SRD 3.5" if sistema == "dnd35" else "PRD PF1e"}, Table: {titolo}"', f'caratteristica = "{car}"',
                f'modo = "{modo}"', f"slot_di_dominio = {'true' if dominio else 'false'}",
                "nomi = [" + ", ".join(f'"{n}"' for n in nomi) + "]"]
        if sistema == "dnd35" and k == "bard":
            # creature.toml, [griglie.bardo]: card del DM del 2026-11-09, «Tabelle PF1e intere, segnate»
            out.append('variante_del_dm = "pf1e"')
        if sistema == "pf1e" and k == "sorcerer":
            # PRD, Sorcerer, «Bloodline Spells»: uno in più al 3°, 5°, … 19° livello di classe
            out.append("conosciuti_di_stirpe = true")
        out += ["", f"[classi.{k}.al_giorno]"]
        out += [f'"{liv}" = {al_giorno[k][liv]}' for liv in range(1, 21)]
        out.append("")
        if k in noti:
            out.append(f"[classi.{k}.conosciuti]")
            out += [f'"{liv}" = {noti[k][liv]}' for liv in range(1, 21)]
            out.append("")
    print("\n".join(out).rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
