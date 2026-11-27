#!/usr/bin/env python3
"""Banco del lotto 7, prima parte (ADR-0126): una velocità sbagliata messa apposta.

Per ogni scheda del Bestiario con una sola riga `velocita:` si scrivono due
copie, una con 3 metri (10 piedi) in più e una con 3 metri in meno. Una copia
conta come trovata se compare una violazione `numero.velocita`. Le schede che
il controllo non giudica (dadi vita razziali, razza fuori dalle sette dell'SRD)
non possono dare violazioni: si contano a parte, è la portata del controllo.

Uso: python3 muta_velocita.py  (scrive misure-velocita.json accanto)
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402


def _giudica(testo: str, nome: str):
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / nome
        q.write_text(testo, encoding="utf-8")
        return V.velocita(q)


def _cambia(testo: str, m, passo: float) -> "str | None":
    numero = float(m.group(1).replace(",", "."))
    nuovo = numero + (passo if m.group(2).lower() == "m" else passo / 3 * 10)
    if nuovo <= 0:
        return None
    return testo[:m.start(1)] + f"{nuovo:g}" + testo[m.end(1):]


def main() -> int:
    conto = {"schede con una riga di velocità": 0, "giudicate": 0, "già fuori regola": 0, "dubbie": 0}
    esiti = {"più 3 m": [0, 0], "meno 3 m": [0, 0]}          # trovate, scritte
    perse = []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        righe = list(V._RIGA_VELOCITA.finditer(testo))
        if len(righe) != 1 or V.L.leggi(p) is None:
            continue
        conto["schede con una riga di velocità"] += 1
        v, nv = V.velocita(p)
        if v:
            conto["già fuori regola"] += 1
            continue
        if nv:
            conto["dubbie"] += 1
            continue
        # giudicata: una velocità impossibile deve dare una violazione o un dubbio
        prova = _cambia(testo, righe[0], 30)
        pv, pn = _giudica(prova, p.name)
        if not pv and not pn:
            continue
        conto["giudicate"] += 1
        for nome, passo in (("più 3 m", 3), ("meno 3 m", -3)):
            copia = _cambia(testo, righe[0], passo)
            if copia is None:
                continue
            esiti[nome][1] += 1
            cv, _ = _giudica(copia, p.name)
            if any(x["regola"] == "numero.velocita" for x in cv):
                esiti[nome][0] += 1
            else:
                perse.append(f"{p.relative_to(ROOT)}: {nome}")
    fuori = {"conto": conto, "esiti": {k: {"trovate": a, "scritte": b} for k, (a, b) in esiti.items()},
             "perse": perse}
    (Path(__file__).parent / "misure-velocita.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, n in conto.items():
        print(f"{k:34} {n}")
    for k, (a, b) in esiti.items():
        print(f"{k:34} {a}/{b}")
    for x in perse:
        print("  persa:", x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
