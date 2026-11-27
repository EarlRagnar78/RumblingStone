#!/usr/bin/env python3
"""Banco del lotto 5, seconda parte (ADR-0126): un grado di sfida sbagliato messo apposta.

Per ogni scheda del Bestiario il cui grado di sfida il controllo giudica in
regola si scrivono due copie, una col grado alzato di 1 e una col grado
abbassato di 1 (sotto 1: il gradino accanto). Una copia conta come trovata se
compare una violazione `numero.gs`. Dove la regola è una forbice (creatura
base con livelli di classe) una copia può restare legale: si conta a parte.

Uso: python3 muta_gs.py  (scrive misure-gs.json accanto)
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import gs as GS  # noqa: E402

RIGA = re.compile(r"^(\s*gs\s*:\s*)(\d+\s*/\s*\d+|\d+(?:[.,]\d+)?)\s*$", re.M | re.I)
SCALA = [Fraction(1, 8), Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)] + [Fraction(n) for n in range(1, 41)]


def _giudica(testo: str, nome: str):
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / nome
        q.write_text(testo, encoding="utf-8")
        return V.grado_di_sfida(q)


def main() -> int:
    conto = {"schede col grado": 0, "giudicate in regola": 0, "dubbie": 0, "già fuori regola": 0}
    esiti = {"più uno": [0, 0], "meno uno": [0, 0]}          # trovate, scritte
    perse = []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        m = RIGA.search(testo)
        if not m or V.L.leggi(p) is None:
            continue
        conto["schede col grado"] += 1
        v, nv = V.grado_di_sfida(p)
        if v:
            conto["già fuori regola"] += 1
            continue
        if nv:
            conto["dubbie"] += 1
            continue
        conto["giudicate in regola"] += 1
        ha = GS.frazione(m.group(2).replace(" ", ""))
        i = SCALA.index(ha) if ha in SCALA else None
        if i is None:
            continue
        for nome, j in (("più uno", i + 1), ("meno uno", i - 1)):
            if not 0 <= j < len(SCALA):
                continue
            copia = testo[:m.start(2)] + GS.scritto(SCALA[j]) + testo[m.end(2):]
            esiti[nome][1] += 1
            if _giudica(copia, p.name)[0]:
                esiti[nome][0] += 1
            else:
                perse.append(f"{p.relative_to(ROOT)}: {nome} ({GS.scritto(ha)} → {GS.scritto(SCALA[j])}) resta legale")
    out = {"conto": conto, "mutazioni": {k: {"trovate": a, "scritte": b} for k, (a, b) in esiti.items()},
           "perse": perse}
    (Path(__file__).with_name("misure-gs.json")).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                                             encoding="utf-8")
    json.dump({k: v for k, v in out.items() if k != "perse"}, sys.stdout, ensure_ascii=False)
    print(f"\nperse: {len(perse)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
