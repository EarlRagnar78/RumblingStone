#!/usr/bin/env python3
"""muta_abilita.py — verifica_scheda vede i gradi di abilità gonfiati apposta?

Per ogni scheda del Bestiario con una riga di abilità e senza violazioni si
fanno copie con (a) **una** abilità alzata di 4, 8, 12 e (b) **tutte** le
abilità alzate di 3 e di 6, e (c) **ciascuna** abilità della riga, una alla
volta, alzata di 2 e di 4; si conta quante lo strumento ne segnala.

Uso:  python3 muta_abilita.py     # stampa il conto e scrive misure-abilita.json
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402

NUM = re.compile(r"([+−-])(\d+)")


def alza(riga: str, quanto: int, tutte: bool) -> str:
    fatto = [False]

    def sost(m: "re.Match") -> str:
        if fatto[0] and not tutte:
            return m.group(0)
        fatto[0] = True
        v = int(m.group(0).replace("−", "-")) + quanto
        return f"{v:+d}"
    return NUM.sub(sost, riga)


def main() -> int:
    casi = {"una +4": (4, False), "una +8": (8, False), "una +12": (12, False),
            "tutte +3": (3, True), "tutte +6": (6, True)}
    conto = {k: {"mutanti": 0, "trovati": 0} for k in casi}
    schede = 0
    with tempfile.TemporaryDirectory() as tmp:
        for p in sorted((ROOT / "Bestiario").rglob("*.md")):
            s = L.leggi(p)
            if s is None:
                continue
            righe = s.testo.splitlines()
            i = next((k for k, r in enumerate(righe)
                      if (m := V.RIGA_ABILITA.search(r)) and NUM.search(m.group(1))), None)
            if i is None:
                continue
            v, nv = V.abilita(p)
            if v or nv:
                continue
            schede += 1
            m = V.RIGA_ABILITA.search(righe[i])
            for nome, (quanto, tutte) in casi.items():
                nuova = righe[i][:m.start(1)] + alza(m.group(1), quanto, tutte) + righe[i][m.end(1):]
                q = Path(tmp) / p.name
                q.write_text("\n".join(righe[:i] + [nuova] + righe[i + 1:]), encoding="utf-8")
                conto[nome]["mutanti"] += 1
                conto[nome]["trovati"] += bool(V.abilita(q)[0])
            # ogni abilità della riga, una alla volta (lotto 6 di ADR-0126): la prima sola
            # non dice nulla delle abilità fuori classe, che stanno dove capita
            numeri = list(NUM.finditer(m.group(1)))
            for quanto in (2, 4):
                for n in numeri:
                    v = int(n.group(0).replace("−", "-")) + quanto
                    testo = m.group(1)[:n.start()] + f"{v:+d}" + m.group(1)[n.end():]
                    nuova = righe[i][:m.start(1)] + testo + righe[i][m.end(1):]
                    q = Path(tmp) / p.name
                    q.write_text("\n".join(righe[:i] + [nuova] + righe[i + 1:]), encoding="utf-8")
                    c = conto.setdefault(f"ciascuna +{quanto}", {"mutanti": 0, "trovati": 0})
                    c["mutanti"] += 1
                    c["trovati"] += bool(V.abilita(q)[0])
    print(f"{schede} schede con abilità, pulite e calcolabili")
    for k, c in conto.items():
        print(f"{k:12s} {c['trovati']:3d}/{c['mutanti']:3d}")
    (Path(__file__).parent / "misure-abilita.json").write_text(
        json.dumps({"schede": schede, **conto}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
