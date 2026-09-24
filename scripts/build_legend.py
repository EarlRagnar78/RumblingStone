#!/usr/bin/env python3
"""
build_legend — deriva `scripts/legend.json` da `scripts/legend.yaml` (ADR-0048).

La fonte scritta a mano e' il YAML, perche' porta i commenti: la memoria di
*perche'* una tenda e' un muro sta accanto al dato, non solo in un ADR. Il JSON
e' l'artefatto committato che i consumatori leggono con `json` di stdlib.

⚠️ **Perche' due file e non uno.** `pyyaml` e' un debito dichiarato
(ADR-0037) e non puo' entrare nel percorso di rendering, che e' `stdlib_only`.
Qui sta nel generatore, che gira a mano e in CI; `dmcore/legenda.py` legge solo
JSON. E' la forma che ADR-0048 §2 prescrive — *«un `legend.json` committato e
verificato in CI, come gia' si fa per `docs/tools/`»* — e l'alternativa (un
terzo parser YAML fatto a mano, dopo i due gia' in `suggest_map.py` e
`suggest_encounter.py`) sarebbe la malattia che questa decisione cura.

Uso:
    python3 scripts/build_legend.py            # rigenera legend.json
    python3 scripts/build_legend.py --check    # esce 1 se e' fuori sincronia
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent
SORGENTE = RADICE / "legend.yaml"
DERIVATO = RADICE / "legend.json"

CAMPI_RENDER = ("mode", "pat", "prop", "fill", "heavy",
                "altezza_m", "piatto", "texture")
CAMPI_FUNZIONE = ("blocks_movement", "blocks_sight", "blocks_line_of_effect",
                  "deroga_uvtt", "door", "cover", "obscurement", "move_cost",
                  "climb", "swim", "prone_concealment", "destructible",
                  "nameable", "hazard", "light")


def _carica_yaml() -> dict:
    try:
        import yaml
    except ImportError:
        print("build_legend richiede pyyaml (eccezione dichiarata da ADR-0037):\n"
              "  pip install pyyaml\n"
              "Il percorso di rendering non ne ha bisogno: legge legend.json.",
              file=sys.stderr)
        raise SystemExit(2)
    return yaml.safe_load(SORGENTE.read_text(encoding="utf-8"))


def componi(dati: dict) -> str:
    """Uscita deterministica: ordine del sorgente, chiavi in ordine dichiarato."""
    simboli = {}
    for sim, voce in dati["symbols"].items():
        render = {k: voce["render"][k] for k in CAMPI_RENDER if k in voce["render"]}
        fuori = {"label": voce.get("label", ""), "render": render}
        funzione = voce.get("function") or {}
        if funzione:
            fuori["function"] = {k: funzione[k] for k in CAMPI_FUNZIONE
                                 if k in funzione}
        simboli[sim] = fuori
    testo = json.dumps({"version": dati["version"], "symbols": simboli},
                       ensure_ascii=False, indent=2)
    return testo + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="non scrive: esce 1 se legend.json e' fuori sincronia")
    args = ap.parse_args()

    atteso = componi(_carica_yaml())
    if args.check:
        attuale = DERIVATO.read_text(encoding="utf-8") if DERIVATO.exists() else ""
        if attuale != atteso:
            print(f"✗ {DERIVATO.name} e' fuori sincronia con {SORGENTE.name}: "
                  f"rigenera con `python3 scripts/build_legend.py`", file=sys.stderr)
            return 1
        n = len(json.loads(atteso)["symbols"])
        print(f"✓ build_legend: {n} simboli, legend.json in sincronia")
        return 0

    DERIVATO.write_text(atteso, encoding="utf-8")
    print(f"✓ {DERIVATO.relative_to(RADICE.parent)} — "
          f"{len(json.loads(atteso)['symbols'])} simboli")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
