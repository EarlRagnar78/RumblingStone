#!/usr/bin/env python3
"""Porta le righe leggibili di ADR-0091 nell'ordine delle AP PF1e.

Decisione di Jfs del 2026-11-13: le Tattiche stanno fra Attacco e Statistiche,
come in Burnt Offerings. Lo script sposta le sezioni intere, senza toccare una
parola: l'insieme delle righe di ogni file resta lo stesso.

    python3 riordina_fasce.py            # conta soltanto
    python3 riordina_fasce.py --scrivi   # riscrive i file
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from dmcore import statblock as sb  # noqa: E402

FUORI = ("plans/", "docs/", "node_modules/", ".git/", "skills/", "dist/")


def riordina(testo: str) -> tuple[str, int]:
    righe = testo.split("\n")
    fuori: list[str] = []
    i = spostate = 0
    in_recinto = False
    while i < len(righe):
        r = righe[i]
        if r.lstrip().startswith("```"):
            in_recinto = not in_recinto
        if in_recinto or not sb._SEZIONE.match(r.strip()):
            fuori.append(r)
            i += 1
            continue
        _, fine = sb.sezioni_leggibili(righe, i)
        if fine <= i:
            fuori.append(r)
            i += 1
            continue
        # i pezzi: (etichetta, righe del corpo), e i vuoti che li separano
        pezzi: list[tuple[str, list[str]]] = []
        for k in range(i, fine):
            m = sb._SEZIONE.match(righe[k].strip())
            if m:
                pezzi.append((m.group(1), [righe[k]]))
            else:
                pezzi[-1][1].append(righe[k])
        vuoti = []
        for _, corpo in pezzi:
            n = 0
            while corpo and not corpo[-1].strip():
                corpo.pop()
                n += 1
            vuoti.append(n)
        ordine = sorted(range(len(pezzi)), key=lambda k: (sb.SEZIONI.index(pezzi[k][0]), k))
        if ordine != list(range(len(pezzi))):
            spostate += 1
        for pos, k in enumerate(ordine):
            fuori += pezzi[k][1] + [""] * vuoti[pos]
        i = fine
    return "\n".join(fuori), spostate


def main() -> int:
    scrivi = "--scrivi" in sys.argv
    tot = file_toccati = 0
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(FUORI) or rel.endswith(".hb.md"):
            continue
        testo = p.read_text(encoding="utf-8")
        nuovo, n = riordina(testo)
        if n:
            assert sorted(nuovo.split("\n")) == sorted(testo.split("\n")), rel
            tot += n
            file_toccati += 1
            print(f"{n:3d}  {rel}")
            if scrivi:
                p.write_text(nuovo, encoding="utf-8")
    print(f"schede riordinate: {tot} in {file_toccati} file" + ("" if scrivi else " (prova, niente scritto)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
