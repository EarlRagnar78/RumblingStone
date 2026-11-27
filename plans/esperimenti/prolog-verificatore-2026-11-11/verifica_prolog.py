#!/usr/bin/env python3
"""verifica_prolog.py — gli stessi fatti di estrai.py, verificati da SWI-Prolog.

Scrive i fatti (dati dei talenti + schede) in un file .pl temporaneo, lancia
`swipl` come processo (argv in lista, niente shell: S-2 di ADR-0030) e legge le
violazioni su stdout, una per riga separata da tab.

Uscita: JSON come verifica_python.py, più `regola` con il nome della regola
Prolog (car(For), bab, talento, catena(Q) ...) e il controesempio `atteso`/`ha`.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
from estrai import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import talenti as T  # noqa: E402

IT_EN = {"barbaro": "barbarian", "bardo": "bard", "chierico": "cleric", "druido": "druid",
         "guerriero": "fighter", "monaco": "monk", "paladino": "paladin", "ranger": "ranger",
         "ladro": "rogue", "stregone": "sorcerer", "mago": "wizard"}


def q(x) -> str:
    """Un atomo Prolog fra apici, con gli apici e le barre protetti."""
    if isinstance(x, int):
        return str(x)
    return "'" + str(x).replace("\\", "\\\\").replace("'", "\\'") + "'"


def fatti_dati(sistemi: set[str]) -> list[str]:
    out = []
    for s in sorted(sistemi):
        d = T.dati(s)
        for en, t in d["talenti"].items():
            for c, v in t.get("car", {}).items():
                out.append(f"req_car({q(s)},{q(en)},{q(c)},{v}).")
            if t.get("bab"):
                out.append(f"req_bab({q(s)},{q(en)},{t['bab']}).")
            if t.get("lic"):
                out.append(f"req_lic({q(s)},{q(en)},{t['lic']}).")
            for c, v in t.get("classe", {}).items():
                out.append(f"req_classe({q(s)},{q(en)},{q(c)},{v}).")
            for p in t.get("talenti", []):
                out.append(f"req_talento({q(s)},{q(en)},{q(p)}).")
            for cap in t.get("capacita", []):
                out.append(f"req_cap({q(s)},{q(en)},{q(cap)}).")
        for cap, classi in d.get("capacita", {}).items():
            for c, lv in classi.items():
                # una sola identità per classe: i dati 3.5 la scrivono in italiano (D1)
                out.append(f"cap_da({q(s)},{q(cap)},{q(IT_EN.get(c, c))},{lv}).")
    return out


def fatti_schede(schede: list[dict]) -> list[str]:
    out = []
    for s in schede:
        f = q(s["file"])
        out.append(f"scheda({f},{q(s['sistema'])}).")
        for c, v in s["car"].items():
            out.append(f"car({f},{q(c)},{v}).")
        if s["bab"] is not None:
            out.append(f"bab({f},{s['bab']}).")
        for c, n in s["livelli"].items():
            out.append(f"livello({f},{q(c)},{n}).")
        if s["dv"]:
            out.append(f"dv({f},{s['dv']}).")
        out.append(f"lic({f},{s['lic']}).")
        for t in s["talenti"]:
            out.append(f"ha({f},{q(t)}).")
    return out


def verifica(schede: list[dict], swipl: str = "swipl") -> list[dict]:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "fatti.pl"
        p.write_text(":- encoding(utf8).\n" + "\n".join(fatti_dati({s["sistema"] for s in schede}) + fatti_schede(schede)) + "\n",
                     encoding="utf-8")
        r = subprocess.run([swipl, "-q", "-g", "main", "-t", "halt",
                            str(QUI / "regole.pl"), str(p)],
                           capture_output=True, text=True, timeout=60, check=False)
    if r.returncode:
        raise RuntimeError(r.stderr)
    out = []
    for riga in r.stdout.splitlines():
        f, t, reg, att, ha = riga.split("\t")
        out.append({"file": f, "talento": t, "regola": reg, "atteso": att, "ha": ha})
    return out


if __name__ == "__main__":
    if not shutil.which("swipl"):
        sys.exit("swipl non trovato: apt install swi-prolog-nox")
    schede = json.load(open(sys.argv[1], encoding="utf-8"))
    t0 = time.perf_counter()
    v = verifica(schede)
    ms = (time.perf_counter() - t0) * 1000
    json.dump({"motore": "swi-prolog", "ms": round(ms, 1), "violazioni": v},
              sys.stdout, ensure_ascii=False, indent=1)
