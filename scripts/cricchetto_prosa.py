#!/usr/bin/env python3
"""cricchetto_prosa.py — sui file di gioco cambiati nessuna norma di prosa peggiora (ADR-0146).

Per ogni file di gioco che la PR cambia rispetto a REV (il punto in cui il ramo
si stacca da REV), conta i difetti di ogni norma che `punteggio_mqm` misura
(box oltre le 12 righe, box con parentesi, calchi e tic di validate_prosa,
read-aloud che presuppongono, metrature, «sembra/pare» nei box, caratteristiche
minuscole) prima e dopo. Se una norma ha piu' difetti dopo, esce 1.

Quali file si controllano: la stessa regola dell'hook `vincolo_skill.py`. La
prosa pura (handout, recap, introduzioni e appendici) sempre; i file misti
(master, schede) solo se il testo aggiunto contiene un box read-aloud. Un
ritocco a uno statblock non si controlla, anche se il file ha difetti vecchi.

Limiti dichiarati: le norme vedono la forma, non la qualita'. Un box corto e
senza tic puo' essere piatto e passa. Il giudizio sulla qualita' resta il voto
alla cieca del DM (ADR-0093); il cricchetto ferma solo il peggioramento che si
conta. Nessuna soglia nuova: le norme e i rilevatori sono quelli del registro.

Uso:
    python3 scripts/cricchetto_prosa.py --rispetto-a origin/main
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import misura_craft as mc  # noqa: E402
import punteggio_mqm as pm  # noqa: E402
import vincolo_skill as vs  # noqa: E402


def _git(*argomenti: str) -> str:
    return subprocess.run(["git", *argomenti], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def conteggi(rel: str, testo: str) -> "dict[str, int]":
    """I difetti di ogni norma MQM in `testo`, come se stesse in `rel`."""
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / Path(rel).name
        f.write_text(testo, encoding="utf-8")
        out: "dict[str, int]" = {}
        for rilevatore in pm.RILEVATORI:
            out.update(rilevatore(testo, f))
    return out


def _aggiunto(prima: "str | None", dopo: str) -> str:
    """Le righe di `dopo` che `prima` non ha, nell'ordine in cui stanno."""
    vecchie = set((prima or "").splitlines())
    return "\n".join(r for r in dopo.splitlines() if r not in vecchie)


def da_controllare(rel: str, prima: "str | None", dopo: str) -> bool:
    c = vs.classe(rel)
    if c == "prosa":
        return True
    if c == "misto":
        return bool(mc.box_read_aloud(_aggiunto(prima, dopo)))
    return False


def confronta(rel: str, prima: "str | None", dopo: str) -> "dict[str, tuple[int, int]]":
    """Le norme che peggiorano: {norma: (difetti prima, difetti dopo)}."""
    a = conteggi(rel, prima or "")
    b = conteggi(rel, dopo)
    return {k: (a.get(k, 0), n) for k, n in b.items() if n > a.get(k, 0)}


def coppie(rev: str) -> "list[tuple[str, str | None, str]]":
    """(file, testo prima, testo dopo) per i file di gioco cambiati da `rev`."""
    base = _git("merge-base", rev, "HEAD").strip()
    out = []
    for rel in vs.cambiati(rev):
        try:
            prima: "str | None" = _git("show", f"{base}:{rel}")
        except subprocess.CalledProcessError:
            prima = None
        dopo = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        out.append((rel, prima, dopo))
    return out


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rispetto-a", default="origin/main", metavar="REV")
    a = ap.parse_args(argv)
    controllati = peggiorati = 0
    for rel, prima, dopo in coppie(a.rispetto_a):
        if not da_controllare(rel, prima, dopo):
            continue
        controllati += 1
        peggio = confronta(rel, prima, dopo)
        if peggio:
            peggiorati += 1
            dettaglio = ", ".join(f"{k} {x}→{y}" for k, (x, y) in sorted(peggio.items()))
            print(f"✗ {rel}: {dettaglio}")
    print(f"cricchetto della prosa: {controllati} file con prosa nuova, "
          f"{peggiorati} peggiorati rispetto a {a.rispetto_a}")
    if peggiorati:
        print("  Correggi i difetti aggiunti (misura: `python3 scripts/punteggio_mqm.py FILE`; "
              "misura_craft non accetta un file, e per homebrew/ vedi lo snippet in "
              "skills/REGISTRO-NORME-EDITORIALI.md). ADR-0146.")
    return 1 if peggiorati else 0


if __name__ == "__main__":
    sys.exit(main())
