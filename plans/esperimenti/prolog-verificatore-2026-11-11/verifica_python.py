#!/usr/bin/env python3
"""verifica_python.py — il verificatore che il repo ha già: `dmcore.talenti.manca`.

Base del confronto. Si usa la funzione così com'è; l'unico aiuto sono le chiavi
delle classi date in tutte e due le lingue e il livello del personaggio, perché i
dati del 3.5 le mescolano (vedi ESITO.md, difetti D1 e D2): senza, il confronto
misurerebbe quei due difetti e non il ragionamento.

Uscita: JSON, una violazione per riga: {file, talento, regola, dettaglio}.
`gradi` e `altro` sono prerequisiti che i dati non sanno leggere: vanno in
`non_verificabili`, non fra le violazioni.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
from estrai import IT_EN, ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import talenti as T  # noqa: E402

EN_IT = {v: k for k, v in IT_EN.items()}


def regola_di(msg: str, en: str, sistema: str) -> str:
    t = T.dati(sistema)["talenti"][en]
    if msg.startswith("BAB"):
        return "bab"
    if msg.startswith("livello d'incantatore"):
        return "lic"
    if msg.split(" ")[0] in ("For", "Des", "Cos", "Int", "Sag", "Car"):
        return "car"
    if msg.startswith("gradi") or msg in t.get("altro", []):
        return "non_verificabile"
    if msg in t.get("talenti", []):
        return "talento"
    if msg in t.get("capacita", []):
        return "capacita"
    return "classe"


def verifica(schede: list[dict]) -> tuple[list[dict], list[dict]]:
    viol, nv = [], []
    for s in schede:
        livelli = dict(s["livelli"])
        livelli.update({EN_IT[c]: n for c, n in s["livelli"].items() if c in EN_IT})
        livelli["character"] = s["dv"] or 0
        st = T.Stato(car=s["car"], bab=s["bab"] if s["bab"] is not None else 99,
                     livelli=livelli, lic=s["lic"], talenti=s["talenti"])
        for en in s["talenti"]:
            for msg in T.manca(s["sistema"], en, st):
                r = regola_di(msg, en, s["sistema"])
                voce = {"file": s["file"], "talento": en, "regola": r, "dettaglio": msg}
                (nv if r == "non_verificabile" else viol).append(voce)
    return viol, nv


if __name__ == "__main__":
    schede = json.load(open(sys.argv[1], encoding="utf-8"))
    t0 = time.perf_counter()
    v, nv = verifica(schede)
    ms = (time.perf_counter() - t0) * 1000
    json.dump({"motore": "python", "ms": round(ms, 1), "violazioni": v, "non_verificabili": nv},
              sys.stdout, ensure_ascii=False, indent=1)
