#!/usr/bin/env python3
"""Banco del lotto 2 (ADR-0126): errori messi apposta nel danno delle armi.

Per ogni attacco con un'arma della tabella, in una scheda che `verifica_scheda`
giudica senza violazioni di danno, si scrive una copia con un solo errore:

* `dado`: il dado sale di un passo (1d8 → 1d10, 2d6 → 2d8);
* `bonus +1`, `bonus -2`: il bonus al danno cambia;
* `critico tolto`: via l'intervallo o il moltiplicatore, dove la tabella non dà 20/x2;
* `critico x`: il moltiplicatore sale di uno.

Uso: python3 muta_danno.py  (scrive misure-danno.json accanto)
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
from dmcore import danno as D  # noqa: E402

PASSO = {"1d3": "1d4", "1d4": "1d6", "1d6": "1d8", "1d8": "1d10", "1d10": "1d12", "1d12": "2d8",
         "2d4": "2d6", "2d6": "2d8", "2d8": "3d8", "3d6": "4d6"}
_RIGA = re.compile(r"^  - (?:Mischia|Distanza) .*$", re.M)
_PAR = re.compile(r"\((\d+d\d+)([+−-]\d+)?((?:/|, )[^)]*?)?\)")


def _viol(testo: str, p: Path) -> int:
    with tempfile.TemporaryDirectory(dir=p.parent) as d:
        q = Path(d) / p.name
        q.write_text(testo, encoding="utf-8")
        v, _ = V.danno(q)
    return len(v)


def mutazioni(testo: str):
    for r in _RIGA.finditer(testo):
        for a, m in zip(D.leggi(r.group(0)), _PAR.finditer(r.group(0))):
            if a.nome.startswith("\0") or D.arma_di(a.nome) is None:
                continue
            arma = D.arma_di(a.nome)
            dado, bonus, coda = m.group(1), m.group(2) or "", m.group(3) or ""

            def con(nuova: str):
                i = r.start() + m.start()
                return testo[:i] + nuova + testo[r.start() + m.end():]
            if dado in PASSO:
                yield "dado", con(f"({PASSO[dado]}{bonus}{coda})")
            n = int(bonus.replace("−", "-")) if bonus else 0
            yield "bonus +1", con(f"({dado}{n + 1:+d}{coda})")
            yield "bonus -2", con(f"({dado}{n - 2:+d}{coda})")
            if (arma["minaccia"], arma["moltiplicatore"]) != (20, 2) and re.match(r"/\s*(?:\d+-20|[x×]\d)", coda.replace("–", "-")):
                yield "critico tolto", con(f"({dado}{bonus})")
            if re.search(r"[x×]\d", coda):
                yield "critico x", con("(" + dado + bonus + re.sub(r"([x×])(\d)", lambda k: k.group(1) + str(int(k.group(2)) + 1), coda, count=1) + ")")


def main() -> int:
    conto: dict = {}
    radici = [ROOT / "Bestiario"] + sorted(ROOT.glob("0*"))
    for p in sorted(q for r in radici for q in r.rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        if "attacchi:" not in testo:
            continue
        base = _viol(testo, p)
        for nome, mutato in mutazioni(testo):
            c = conto.setdefault(nome, {"mutanti": 0, "trovati": 0, "persi": []})
            c["mutanti"] += 1
            if _viol(mutato, p) > base:
                c["trovati"] += 1
            else:
                c["persi"].append(p.name)
    for nome, c in sorted(conto.items()):
        print(f"{nome:14} {c['trovati']:3}/{c['mutanti']:3}")
    print("totale", sum(c["trovati"] for c in conto.values()), "/", sum(c["mutanti"] for c in conto.values()))
    (Path(__file__).parent / "misure-danno.json").write_text(
        json.dumps(conto, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
