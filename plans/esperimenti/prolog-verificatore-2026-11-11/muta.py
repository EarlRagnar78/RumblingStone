#!/usr/bin/env python3
"""muta.py — difetti iniettati nelle schede vere: chi li trova, e con quale messaggio.

Per ogni talento senza violazioni di una scheda vera si costruisce un mutante per
ogni prerequisito che il talento ha:
  car      la caratteristica richiesta portata a soglia − 1
  bab      il BAB portato a soglia − 1
  talento  il talento prerequisito tolto dalla scheda
  classe   i livelli della classe richiesta portati a soglia − 1
Un mutante è TROVATO se il verificatore dà, per quel talento, una violazione
della regola mutata. Stessi mutanti a Python, SWI-Prolog e clingo.

Uscita: tabella su stdout e misure.json accanto.
"""
from __future__ import annotations

import copy
import json
import sys
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import verifica_clingo as VC  # noqa: E402
import verifica_prolog as VP  # noqa: E402
import verifica_python as VY  # noqa: E402
from estrai import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import talenti as T  # noqa: E402


def mutanti(schede: list[dict], sporchi: set) -> list[tuple[dict, str, str]]:
    out = []
    for s in schede:
        for en in s["talenti"]:
            if (s["file"], en) in sporchi:
                continue
            t = T.dati(s["sistema"])["talenti"].get(en, {})
            for c, v in t.get("car", {}).items():
                m = copy.deepcopy(s)
                m["car"][c] = v - 1
                out.append((m, en, "car"))
            if t.get("bab") and s["bab"] is not None:
                m = copy.deepcopy(s)
                m["bab"] = t["bab"] - 1
                out.append((m, en, "bab"))
            for p in t.get("talenti", []):
                if p in s["talenti"]:
                    m = copy.deepcopy(s)
                    m["talenti"].remove(p)
                    out.append((m, en, "talento"))
            for c, v in t.get("classe", {}).items():
                m = copy.deepcopy(s)
                if c == "character":
                    m["dv"] = v - 1
                else:
                    m["livelli"][c] = v - 1
                out.append((m, en, "classe"))
    for i, (m, _, _) in enumerate(out):
        m["file"] = f"mutante-{i:04d}"
    return out


def main() -> None:
    schede = json.load(open(sys.argv[1], encoding="utf-8"))
    base, _ = VY.verifica(schede)
    sporchi = {(v["file"], v["talento"]) for v in base}
    mm = mutanti(schede, sporchi)
    lotto = [m for m, _, _ in mm]
    ris, tempi = {}, {}
    for nome, f in (("python", lambda x: VY.verifica(x)[0]), ("swi-prolog", VP.verifica),
                    ("clingo", VC.verifica)):
        t0 = time.perf_counter()
        v = f(lotto)
        tempi[nome] = round((time.perf_counter() - t0) * 1000, 1)
        ris[nome] = {(x["file"], x["talento"], x["regola"].split("(")[0]) for x in v}
    righe = {}
    for m, en, cat in mm:
        r = righe.setdefault(cat, {"mutanti": 0, **{k: 0 for k in ris}})
        r["mutanti"] += 1
        for k, s in ris.items():
            r[k] += (m["file"], en, cat) in s
    tot = {"mutanti": sum(r["mutanti"] for r in righe.values()),
           **{k: sum(r[k] for r in righe.values()) for k in ris}}
    print(f"{'regola':10} {'mutanti':>8} " + " ".join(f"{k:>11}" for k in ris))
    for cat, r in sorted(righe.items()) + [("TOTALE", tot)]:
        print(f"{cat:10} {r['mutanti']:>8} " + " ".join(f"{r[k]:>11}" for k in ris))
    print("ms:", tempi)
    (QUI / "misure-mutanti.json").write_text(json.dumps({"per_regola": righe, "totale": tot, "ms": tempi},
                                                        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
