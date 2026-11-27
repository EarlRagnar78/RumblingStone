#!/usr/bin/env python3
"""Secondo passo di riordina_fasce.py: le Tattiche staccate dalla scheda.

In alcune schede del Bestiario fra le Capacità speciali e le Tattiche ci sono
note (righe «> ⚠ …») o un altro paragrafo: le Tattiche formano un gruppo a sé e
riordina_fasce.py non le vede. Qui salgono, intere, subito prima della prima
«Statistiche» o «Capacità speciali» della stessa scheda. Si ferma a un titolo
o a un altro recinto ```statblocco.

    python3 riordina_staccate.py [--scrivi]
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import statblock as sb  # noqa: E402

FUORI = ("plans/", "docs/", "skills/")


def gruppi(righe):
    """(inizio, fine, [(etichetta, riga)]) per ogni gruppo di sezioni leggibili."""
    out, i, recinto = [], 0, False
    while i < len(righe):
        if righe[i].lstrip().startswith("```"):
            recinto = not recinto
        if not recinto and sb._SEZIONE.match(righe[i].strip()):
            _, fine = sb.sezioni_leggibili(righe, i)
            if fine > i:
                et = [(sb._SEZIONE.match(righe[k].strip()).group(1), k)
                      for k in range(i, fine) if sb._SEZIONE.match(righe[k].strip())]
                out.append((i, fine, et))
                i = fine
                continue
        i += 1
    return out


def sposta(testo: str) -> tuple[str, int]:
    """Ogni «Tattiche» che viene dopo una «Statistiche» o una «Capacità
    speciali» della stessa scheda sale subito prima della prima delle due."""
    n = 0
    while True:
        righe = testo.split("\n")
        gg = gruppi(righe)
        fatto = False
        for x, (ini, fine, et) in enumerate(gg):
            if et[0][0] != "Tattiche" or x == 0:
                continue
            # il pezzo delle Tattiche: dalla sua etichetta alla prossima, o alla fine del gruppo
            t_ini = et[0][1]
            t_fine = et[1][1] if len(et) > 1 else fine
            # indietro, fino al recinto della scheda: la prima Statistiche/Capacità dopo l'Attacco
            bersaglio = None
            for y in range(x - 1, -1, -1):
                y_ini, y_fine, y_et = gg[y]
                if any(r.strip().startswith(("```statblocco", "## ", "# ")) for r in righe[y_fine:gg[y + 1][0]]):
                    break
                nomi = [e for e, _ in y_et]
                if "Tattiche" in nomi:
                    bersaglio = None
                    break
                for e, k in y_et:
                    if e in ("Statistiche", "Capacità speciali"):
                        bersaglio = k
                        break
                if "Attacco" in nomi or "Difesa" in nomi:
                    break
            if bersaglio is None:
                continue
            blocco = righe[t_ini:t_fine]
            while blocco and not blocco[-1].strip():
                blocco.pop()
            resto = righe[:t_ini] + righe[t_fine:]
            while 0 < t_ini < len(resto) and not resto[t_ini].strip() and not resto[t_ini - 1].strip():
                del resto[t_ini]
            testo = "\n".join(resto[:bersaglio] + blocco + [""] + resto[bersaglio:])
            n += 1
            fatto = True
            break
        if not fatto:
            return testo, n


def main() -> int:
    scrivi = "--scrivi" in sys.argv
    tot = 0
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(FUORI) or rel.endswith(".hb.md"):
            continue
        testo = p.read_text(encoding="utf-8")
        nuovo, n = sposta(testo)
        if n:
            a = sorted(r for r in testo.split("\n") if r.strip())
            b = sorted(r for r in nuovo.split("\n") if r.strip())
            assert a == b, rel
            tot += n
            print(f"{n:3d}  {rel}")
            if scrivi:
                p.write_text(nuovo, encoding="utf-8")
    print(f"Tattiche staccate portate dopo l'Attacco: {tot}" + ("" if scrivi else " (prova)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
