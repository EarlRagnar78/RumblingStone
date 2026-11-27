#!/usr/bin/env python3
"""impronte.py — l'impronta SHA-256 delle uscite degli strumenti di fascia A, B e C.

Il banco d'invarianza di ADR-0111: spostare una tabella dal codice al plugin
`dnd35` non deve cambiare un byte di quello che gli strumenti stampano su un
modulo 3.5. Si lancia prima di un lotto (`--scrivi`) e dopo (`--confronta`);
una riga diversa è una regressione finché il DM non dice il contrario.

    python3 plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py --scrivi
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py --confronta

Ogni comando gira con il seme fisso dove ne ha uno, e in sola lettura.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = Path(__file__).with_name("IMPRONTE.json")
COMANDI = {
    "genera_creatura_gs7": ["scripts/genera_creatura.py", "--gs", "7", "--seed", "42"],
    "genera_creatura_gs14": ["scripts/genera_creatura.py", "--gs", "14", "--seed", "7"],
    "suggest_encounter": ["scripts/suggest_encounter.py", "--seed", "42"],
    "suggest_loot_el13": ["scripts/suggest_loot.py", "--el", "13", "--pcs", "4", "--seed", "42"],
    "suggest_loot_wild": ["scripts/suggest_loot.py", "--el", "11", "--wild", "--seed", "1"],
    "update_xp_check": ["scripts/update_xp.py", "--check"],
    "validate_bestiario": ["scripts/validate_bestiario.py"],
    "conformita_statblocchi": ["scripts/conformita_statblocchi.py"],
    "derive_statblocks": ["scripts/derive_statblocks.py"],
    "validate_modules": ["scripts/validate_modules.py"],
    "validate_standalone": ["scripts/validate_standalone.py"],
    "domande_developer": ["scripts/domande_developer.py", "--json"],
}


#: Le righe che cambiano con l'orologio e non con il codice. Senza questa
#: pulizia `update_xp --check` cambiava impronta a ogni minuto (trovato al
#: primo confronto di L1, 2026-11-07).
OROLOGIO = [re.compile(rb"^_Last update: .*$", re.M)]


def impronta(argv: "list[str]") -> dict:
    r = subprocess.run([sys.executable, *argv], cwd=ROOT, capture_output=True, timeout=600)
    uscita = r.stdout
    for rx in OROLOGIO:
        uscita = rx.sub(b"<orologio>", uscita)
    return {"uscita": r.returncode, "sha256": hashlib.sha256(uscita).hexdigest(),
            "byte": len(uscita)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--scrivi", action="store_true")
    g.add_argument("--confronta", action="store_true")
    a = ap.parse_args(argv)
    ora = {k: impronta(v) for k, v in COMANDI.items()}
    if a.scrivi:
        FILE.write_text(json.dumps(ora, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        for k, v in ora.items():
            print(f"{k:24s} uscita {v['uscita']}  {v['byte']:>7d} byte  {v['sha256'][:12]}")
        return 0
    prima = json.loads(FILE.read_text(encoding="utf-8"))
    diversi = [k for k in COMANDI if prima.get(k) != ora[k]]
    for k in COMANDI:
        print(("🔴 " if k in diversi else "✅ ") + k)
    return 1 if diversi else 0


if __name__ == "__main__":
    sys.exit(main())
