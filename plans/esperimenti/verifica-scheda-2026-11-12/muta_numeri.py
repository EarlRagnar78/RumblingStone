#!/usr/bin/env python3
"""muta_numeri.py — verifica_scheda trova un numero sbagliato messo apposta?

Per ogni scheda `*-cr*.md` del Bestiario senza violazioni di numeri si fa una
copia con **un** numero cambiato (BAB +1, lotta +3, ogni tiro salvezza +2, −2
e +5) e si chiede a `verifica_scheda` se lo vede. Un mutante conta solo
se la scheda scrive quel campo in una forma che il mutatore riconosce.

Uso:  python3 muta_numeri.py            # stampa il conto e scrive misure-numeri.json
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

_TS = {"Temp": r"(\b(?:Temp(?:ra)?|Fort)\W{0,4}\+)(\d+)", "Rifl": r"(\b(?:Rifl(?:essi)?|Ref)\W{0,4}\+)(\d+)",
       "Vol": r"(\b(?:Vol(?:ontà)?|Will)\W{0,4}\+)(\d+)"}
#: mutazione → (campo che la regola deve segnalare, espressione, scarto messo)
MUTAZIONI = {
    "BAB +1": ("BAB", r"(\bBAB\W{0,6}\+)(\d+)|(Base Atk\W{0,6}\+)(\d+)", 1),
    "lotta +3": ("lotta", r"(\b(?:Lotta|Grapple|Grp)\W{0,4}\+)(\d+)", 3),
    **{f"{k} +2": (k, rx, 2) for k, rx in _TS.items()},
    **{f"{k} -2": (k, rx, -2) for k, rx in _TS.items()},
    **{f"{k} +5": (k, rx, 5) for k, rx in _TS.items()},
}


def muta(testo: str, campo: str) -> "str | None":
    """Cambia il campo **dovunque** la scheda lo scrive con lo stesso valore
    (intestazione e corpo): un numero cambiato in un posto solo misurerebbe
    quale dei due posti legge lo strumento, non la regola."""
    _, rx, delta = MUTAZIONI[campo]
    m = re.search(rx, testo)
    if not m:
        return None
    valore = next(x for x in reversed(m.groups()) if x is not None)

    def sost(k: "re.Match") -> str:
        g = [x for x in k.groups() if x is not None]
        return g[0] + str(max(0, int(g[1]) + delta)) if g[1] == valore else k.group(0)
    return re.sub(rx, sost, testo)


def main() -> int:
    conto = {c: {"mutanti": 0, "trovati": 0, "persi": []} for c in MUTAZIONI}
    with tempfile.TemporaryDirectory() as tmp:
        for p in sorted((ROOT / "Bestiario").rglob("*-cr*.md")):
            # si salta il campo che ha già una violazione, non tutta la scheda:
            # a tolleranza zero 28 schede ne hanno una, e sparirebbero dal banco
            gia = {x["regola"] for x in V.numeri(p)[0]}
            testo = p.read_text(encoding="utf-8")
            for campo in MUTAZIONI:
                nuovo = muta(testo, campo)
                if nuovo is None or f"numero.{MUTAZIONI[campo][0]}" in gia:
                    continue
                q = Path(tmp) / p.name
                q.write_text(nuovo, encoding="utf-8")
                viol, nv = V.numeri(q)
                visto = any(x["regola"] == f"numero.{MUTAZIONI[campo][0]}" for x in viol + nv)
                conto[campo]["mutanti"] += 1
                conto[campo]["trovati"] += visto
                if not visto:
                    conto[campo]["persi"].append(p.name)
    tot = sum(c["mutanti"] for c in conto.values())
    trovati = sum(c["trovati"] for c in conto.values())
    for campo, c in conto.items():
        print(f"{campo:9s} {c['trovati']:3d}/{c['mutanti']:3d}")
    print(f"totale {trovati}/{tot}")
    (Path(__file__).parent / "misure-numeri.json").write_text(
        json.dumps(conto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
