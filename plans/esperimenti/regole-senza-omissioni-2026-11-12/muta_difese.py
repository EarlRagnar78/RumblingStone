#!/usr/bin/env python3
"""Banco del lotto 7, seconda parte (ADR-0126): una RI o una RD sbagliata messa apposta.

Per ogni scheda del Bestiario che scrive una resistenza agli incantesimi o una
riduzione del danno N/— fuori dalle righe di storia, si scrivono due copie per
numero: una con un punto in più e una con un punto in meno. Una copia conta
come trovata se compare una violazione `numero.RI` o `numero.RD`. Le schede che
il controllo non giudica (nessuna razza o classe della tabella) non possono
dare violazioni: si contano a parte, è la portata del controllo.

Immunità del tipo: a ogni scheda di un tipo che le dà, e che oggi è in regola,
si toglie la formula «tratti dei …» oppure, se le elenca, la prima immunità
dell'elenco. La copia conta come trovata se compare `tratti.immunita`.

Uso: python3 muta_difese.py  (scrive misure-difese.json accanto)
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

CAMPI = {"RI": V._SCRITTA_RI, "RD": V._SCRITTA_RD}


def _giudica(testo: str, nome: str):
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / nome
        q.write_text(testo, encoding="utf-8")
        return V.difese(q)


def _prima(testo: str, rx):
    """La prima scrittura fuori dalle righe di storia, come (inizio, fine) del numero nel testo."""
    pos = 0
    for riga in testo.split("\n"):
        if not V._RIGA_DI_STORIA.match(riga):
            m = rx.search(riga)
            if m:
                return pos + m.start(1), pos + m.end(1), int(m.group(1))
        pos += len(riga) + 1
    return None


def main() -> int:
    conto = {c: {"schede che la scrivono": 0, "giudicate": 0, "già fuori regola": 0, "dubbie": 0} for c in CAMPI}
    esiti = {f"{c} {v}": [0, 0] for c in CAMPI for v in ("più 1", "meno 1")}      # trovate, scritte
    perse = []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        if V.L.leggi(p) is None:
            continue
        v, nv = V.difese(p)
        for campo, rx in CAMPI.items():
            dove = _prima(testo, rx)
            if dove is None:
                continue
            conto[campo]["schede che la scrivono"] += 1
            regola = f"numero.{campo}"
            if any(x["regola"] == regola for x in v):
                conto[campo]["già fuori regola"] += 1
                continue
            if any(x["regola"] == regola for x in nv):
                conto[campo]["dubbie"] += 1
                continue
            a, b, n = dove
            pv, pn = _giudica(testo[:a] + str(n + 40) + testo[b:], p.name)
            if not any(x["regola"] == regola for x in pv + pn):
                continue                                  # il controllo non la guarda
            conto[campo]["giudicate"] += 1
            for nome, passo in (("più 1", 1), ("meno 1", -1)):
                chiave = f"{campo} {nome}"
                esiti[chiave][1] += 1
                cv, _ = _giudica(testo[:a] + str(n + passo) + testo[b:], p.name)
                if any(x["regola"] == regola for x in cv):
                    esiti[chiave][0] += 1
                else:
                    perse.append(f"{p.relative_to(ROOT)}: {chiave}")
    imm = S.dati("dnd35", "creature.costruzione")["difese"]["immunita"]
    conto["immunità"] = {"schede del tipo": 0, "in regola": 0, "già fuori regola": 0}
    esiti["immunità tolta"] = [0, 0]
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        s = V.L.leggi(p)
        if s is None:
            continue
        prima = re.split(r"[(,/]", s.tipo or "", maxsplit=1)[0]
        tipi = [k for k in imm["tipi"] if re.search(rf"(?<![\w-])(?<!mezzo )(?:{k}|{imm['nomi'][k]})\b", prima, re.I)]
        if len(tipi) != 1:
            continue
        conto["immunità"]["schede del tipo"] += 1
        if any(x["regola"] == "tratti.immunita" for x in V.difese(p)[0]):
            conto["immunità"]["già fuori regola"] += 1
            continue
        conto["immunità"]["in regola"] += 1
        testo = p.read_text(encoding="utf-8")
        formula = rf"tratti\s+(?:(?:de[il]|dei|degli|da|del tipo)\s+)?(?:{imm['nomi'][tipi[0]]})|\b{tipi[0]} traits\b"
        copia = re.sub(formula, "…", testo, flags=re.I)
        if copia == testo:
            copia = re.sub(imm["parole"][imm["tipi"][tipi[0]][-1]], "…", testo, flags=re.I)
        esiti["immunità tolta"][1] += 1
        if any(x["regola"] == "tratti.immunita" for x in _giudica(copia, p.name)[0]):
            esiti["immunità tolta"][0] += 1
        else:
            perse.append(f"{p.relative_to(ROOT)}: immunità tolta")
    fuori = {"conto": conto, "esiti": {k: {"trovate": a, "scritte": b} for k, (a, b) in esiti.items()},
             "perse": perse}
    (Path(__file__).parent / "misure-difese.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for c, d in conto.items():
        for k, n in d.items():
            print(f"{c} {k:30} {n}")
    for k, (a, b) in esiti.items():
        print(f"{k:34} {a}/{b}")
    for x in perse:
        print("  persa:", x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
