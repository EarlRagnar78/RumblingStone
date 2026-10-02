#!/usr/bin/env python3
"""adozioni_in_attesa.py — le adozioni rimandate, e quando smettono di aspettare.

Il DM, il 2026-10-01, su `commit-archaeologist`: *«inseriscilo in una possibile
revisione di inserimento con gli url corretti, in modo che quando la condizione
di inserimento diventa attiva si procede all'inserimento»*.

Una skill o uno script esterno valutato e rimandato non sparisce: entra in
`plans/adozioni-in-attesa.json` con la fonte, il commit, la licenza e una
**condizione misurabile**. Questo script la misura. Con `--check` esce 1
quando una condizione e' attiva e la voce dice ancora «in attesa»: e' la riga
che ha smesso di dire il vero, come nei cancelli di ADR-0062.

Le misure sono funzioni con un nome; la voce del registro dice quale usare e
con che parametri. Una misura che qui non puo' girare (un clone senza storia)
lo dice, e non risponde «spenta».

Uso:
    python3 scripts/adozioni_in_attesa.py            # la tabella
    python3 scripts/adozioni_in_attesa.py --check    # esce 1 se una condizione e' attiva

Solo libreria standard. Decisione: ADR-0076.
Exit code: 0 = ok · 1 = condizione attiva su una voce ancora in attesa · 2 = registro malformato.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRO = ROOT / "plans" / "adozioni-in-attesa.json"

#: I file di gioco che contano per la misura sulla storia: master, stand-alone,
#: Drappo. Fuori i prompt delle immagini, gli apparati generati e gli archivi.
FILE_DI_GIOCO = re.compile(r"^(0\d_[^/]+/[^/]+\.md|10-stand-alone/.+\.md|STANDALONE-[^/]+/[^/]+\.md)$")
ESCLUSI = ("_ARCHIVIO", "homebrew", "Immagini/", "APPARATO-")
#: Le forme con cui il repo scrive la storia di una scelta nel sorgente (ADR-0069).
STORIA = re.compile(r"<!-- storico|correzione del playtest", re.I)

NON_MISURABILE = "non misurabile"


def _git(*argomenti: str) -> str:
    return subprocess.run(["git", *argomenti], cwd=ROOT, capture_output=True,
                          text=True, check=False).stdout


def file_rimaneggiati_senza_storia(giorni: int, commit_minimi: int, soglia_file: int,
                                   **_ignorati) -> "tuple[object, str]":
    """Quanti file di gioco cambiano spesso e non portano la loro storia scritta."""
    if _git("rev-parse", "--is-shallow-repository").strip() == "true":
        return NON_MISURABILE, "clone senza storia completa: serve `git fetch --unshallow` (in CI c'e')"
    conti: "dict[str, int]" = {}
    for riga in _git("log", f"--since={giorni} days ago", "--name-only", "--format=").splitlines():
        if FILE_DI_GIOCO.match(riga) and not any(x in riga for x in ESCLUSI):
            conti[riga] = conti.get(riga, 0) + 1
    colpiti = sorted(f for f, n in conti.items() if n >= commit_minimi
                     and (ROOT / f).exists()
                     and not STORIA.search((ROOT / f).read_text(encoding="utf-8", errors="replace")))
    attiva = len(colpiti) >= soglia_file
    return attiva, f"{len(colpiti)} file su una soglia di {soglia_file}" + (f": {', '.join(colpiti)}" if colpiti else "")


MISURE = {"file_rimaneggiati_senza_storia": file_rimaneggiati_senza_storia}
CAMPI = ("id", "fonte", "commit_upstream", "licenza", "autore", "stato", "condizione", "quando_scatta")


def carica() -> "list[dict]":
    dati = json.loads(REGISTRO.read_text(encoding="utf-8"))
    voci = dati.get("adozioni", [])
    for v in voci:
        mancanti = [c for c in CAMPI if c not in v]
        if mancanti:
            raise ValueError(f"{v.get('id', '?')}: mancano {mancanti}")
        if v["condizione"].get("misura") not in MISURE:
            raise ValueError(f"{v['id']}: misura sconosciuta {v['condizione'].get('misura')!r}")
    return voci


def valuta(voce: dict) -> "tuple[object, str]":
    cond = dict(voce["condizione"])
    return MISURE[cond.pop("misura")](**cond)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="esce 1 se una condizione e' attiva su una voce ancora in attesa")
    args = ap.parse_args(argv)
    try:
        voci = carica()
    except (ValueError, json.JSONDecodeError) as errore:
        print(f"✗ adozioni_in_attesa: registro malformato — {errore}")
        return 2
    da_fare = []
    for v in voci:
        attiva, dettaglio = valuta(v)
        segno = "⚪" if attiva == NON_MISURABILE else ("🔴 ATTIVA" if attiva else "🟢 spenta")
        print(f"{v['id']:24} {v['stato']:12} {segno:10} {dettaglio}")
        if attiva is True and v["stato"] == "in attesa":
            da_fare.append(v)
    for v in da_fare:
        print(f"  → {v['id']}: la condizione e' attiva. {v['quando_scatta']}")
    if args.check and da_fare:
        print(f"✗ adozioni_in_attesa: {len(da_fare)} adozione/i da avviare")
        return 1
    print(f"✓ adozioni_in_attesa: {len(voci)} voce/i, nessuna condizione attiva su una voce in attesa"
          if not da_fare else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
