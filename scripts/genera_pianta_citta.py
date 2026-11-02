#!/usr/bin/env python3
"""
genera_pianta_citta.py — le piante delle città della valle, dal generatore del
repo (ADR-0102).

Le piante di Rethmar, Dauth e Channathgate non vengono da Watabou: le disegna
il motore `scripts/piante/organica.py` (quartieri di Voronoi, vie, lotti, mura
con le torri), con un programma per città che ne fissa la forma, le taglie
scelte dal DM e la legenda. Ogni programma ha il seme fisso, quindi la pianta
si rifà identica: questo script la rigenera nel suo posto canonico, oppure con
`--check` controlla che quella committata sia ancora quella che il programma
produce.

    python3 scripts/genera_pianta_citta.py rethmar            # riscrive la pianta
    python3 scripts/genera_pianta_citta.py --tutte --check    # nessuna scrittura
    python3 scripts/genera_pianta_citta.py dauth -o prova.svg # altrove, per provare

Serve shapely, numpy e scipy (requirements-dev.txt): la pianta si disegna in
sviluppo, la sera al tavolo si stampa l'SVG committato. Esce con 1 se una
pianta committata non è allineata, con 2 se mancano le librerie.
"""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PIANTE = REPO / "scripts" / "piante"
ARCO9 = "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"

#: città → (programma in scripts/piante/, pianta canonica nel repo)
CITTA = {
    "rethmar": ("rethmar.py", f"{ARCO9}/Mappe/rethmar/rethmar-pianta.svg"),
    "dauth": ("dauth.py", f"{ARCO9}/Mappe/dauth-assedio/dauth-pianta.svg"),
    "channathgate": ("channathgate.py", f"{ARCO9}/P2D-Palio-Allegati/mappe/channathgate-pianta.svg"),
}
LIBRERIE = ("shapely", "numpy", "scipy")


def mancanti() -> list[str]:
    return [m for m in LIBRERIE if importlib.util.find_spec(m) is None]


def genera(citta: str, uscita: Path) -> int:
    """Lancia il programma della città in un processo suo (ha stato a livello
    di modulo e legge l'uscita da argv) e ne lascia passare il riepilogo."""
    programma = PIANTE / CITTA[citta][0]
    r = subprocess.run([sys.executable, str(programma), str(uscita)], cwd=PIANTE,
                       capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr)
    else:
        print(f"[{citta}] {r.stdout.strip()}")
    return r.returncode


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("citta", nargs="?", choices=sorted(CITTA), help="la città da rigenerare")
    ap.add_argument("--tutte", action="store_true", help="tutte e tre le città")
    ap.add_argument("--check", action="store_true",
                    help="non scrive: controlla che le piante committate siano allineate")
    ap.add_argument("-o", "--out", type=Path, help="scrive qui invece che nel posto canonico")
    a = ap.parse_args(argv)
    if bool(a.citta) == a.tutte:
        ap.error("indica una città oppure --tutte")
    if a.out and (a.tutte or a.check):
        ap.error("-o vale per una città sola e senza --check")
    if mm := mancanti():
        print(f"✗ genera_pianta_citta: mancano {', '.join(mm)} — "
              f"pip install -r requirements-dev.txt", file=sys.stderr)
        return 2

    scelte = sorted(CITTA) if a.tutte else [a.citta]
    disallineate = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in scelte:
            canonica = REPO / CITTA[c][1]
            uscita = a.out or (Path(tmp) / f"{c}.svg" if a.check else canonica)
            if genera(c, uscita.resolve()):
                return 1
            if a.check and (not canonica.exists() or canonica.read_bytes() != uscita.read_bytes()):
                disallineate.append(CITTA[c][1])
    if disallineate:
        for p in disallineate:
            print(f"✗ pianta NON allineata al suo programma: {p} — "
                  f"python3 scripts/genera_pianta_citta.py <città>", file=sys.stderr)
        return 1
    if a.check:
        print(f"✓ genera_pianta_citta: {len(scelte)} piante allineate ai loro programmi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
