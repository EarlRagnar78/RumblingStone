#!/usr/bin/env python3
"""Gli effetti dei talenti sulle abilità, dalle fonti (ADR-0126, lotto 4).

Uso: python3 estrai_effetti_talenti.py srd <cartella srd-v3.5-md> > sistemi/dnd35/dati/effetti_talenti.toml
     python3 estrai_effetti_talenti.py prd <cartella PSRD-Data>   > sistemi/pf1e/dati/effetti_talenti.toml

Legge la riga «Benefit» di ogni talento e tiene solo le due forme che spostano
il bonus scritto di un'abilità: «+N bonus on [all] A [checks] and B [skill]
checks» e «+N bonus on all checks involving that/the chosen skill». Nel
repo entrano solo nomi e numeri, mai il testo.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DUE = re.compile(r"\+(\d+) bonus on (?:all )?([A-Z][A-Za-z ()]+?)(?: checks)? and ([A-Z][A-Za-z ()]+?)(?: skill)? checks\.")
SCELTA = re.compile(r"\+(\d+) bonus on all (?:skill )?checks (?:involving|with) (?:that|the chosen) skill")
DIECI = re.compile(r"10 or more ranks.*?increases to \+(\d+)")


def _voce(nome: str, testo: str) -> "dict | None":
    piu = DIECI.search(testo)
    extra = {"con_gradi": 10, "bonus_con_gradi": int(piu.group(1))} if piu else {}
    if (m := SCELTA.search(testo)):
        return {"bonus": int(m.group(1)), "a_scelta": True, **extra}
    if (m := DUE.search(testo)):
        return {"bonus": int(m.group(1)), "abilita": [m.group(2).strip().lower(), m.group(3).strip().lower()], **extra}
    return None


def dall_srd(radice: Path) -> dict:
    out = {}
    for f, fonte in (("basic-rules-and-legal/feats.md", "SRD 3.5, Feats"), ("epic/epic-feats.md", "SRD 3.5, Epic Feats"),
                     ("psionics/psionic-feats.md", "SRD 3.5, Psionic Feats")):
        for blocco in re.split(r"^#{2,4} ", (radice / f).read_text(encoding="utf-8"), flags=re.M)[1:]:
            nome = re.sub(r"\s*<small>.*", "", blocco.splitlines()[0]).strip()
            b = re.search(r"\*\*Benefit:\*\*\s*(.+)", blocco)
            if b and (v := _voce(nome, b.group(1))):
                out[nome.lower()] = {**v, "fonte": fonte}
    return out


def dal_prd(radice: Path) -> dict:
    import sqlite3
    db = sqlite3.connect(radice / "book-cr.db")
    out = {}
    for sid, nome in db.execute("select section_id, name from sections where type='feat'").fetchall():
        for k, corpo in db.execute("select name, body from sections where parent_id=?", (sid,)):
            if k in ("Benefit", "Benefits") and (v := _voce(nome, re.sub(r"<[^>]+>", "", corpo or ""))):
                out[nome.strip().lower()] = {**v, "fonte": "PRD PF1e, Core Rulebook, Feats"}
    return out


def _toml(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_toml(x) for x in v) + "]"
    return '"' + str(v) + '"'


def main() -> int:
    prd = sys.argv[1] == "prd"
    voci = (dal_prd if prd else dall_srd)(Path(sys.argv[2]))
    sis = "pf1e" if prd else "dnd35"
    print(f"# sistemi/{sis}/dati/effetti_talenti.toml — generato, non si corregge a mano")
    print("# Da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_effetti_talenti.py (ADR-0126, lotto 4).")
    print(f"# {len(voci)} talenti che alzano il bonus scritto di un'abilità: solo nomi e numeri.")
    print("# `abilita` = le due abilità che prendono il bonus; `a_scelta` = un'abilità scelta,")
    print("# scritta fra parentesi accanto al talento; `bonus_con_gradi` = il bonus con almeno")
    print("# `con_gradi` gradi nell'abilità (PF1e).")
    print("\n[effetti_talenti]")
    for nome in sorted(voci):
        print(f'"{nome}" = {{ ' + ", ".join(f"{k} = {_toml(x)}" for k, x in voci[nome].items()) + " }")
    return 0


if __name__ == "__main__":
    sys.exit(main())
