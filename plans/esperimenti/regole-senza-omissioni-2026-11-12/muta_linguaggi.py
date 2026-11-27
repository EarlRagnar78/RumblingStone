#!/usr/bin/env python3
"""Banco del lotto 7, quarta parte (ADR-0126): un linguaggio automatico tolto apposta.

Per ogni scheda del Bestiario con una sola riga dei linguaggi si toglie dalla
riga, uno alla volta, ogni linguaggio che razza o classe danno da soli. La copia
conta come trovata se compare una violazione `tratti.linguaggi`. Le schede di
una razza che la tabella non ha non possono dare violazioni: si contano a parte.

Uso: python3 muta_linguaggi.py  (scrive misure-linguaggi.json accanto)
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
from dmcore import sistemi as S  # noqa: E402


def _giudica(testo: str, nome: str):
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / nome
        q.write_text(testo, encoding="utf-8")
        return V.linguaggi(q)


def main() -> int:
    nomi = S.dati("dnd35", "creature.costruzione")["linguaggi"]["nomi"]
    conto = {"schede con una riga dei linguaggi": 0, "giudicate": 0, "già fuori regola": 0}
    esito, perse = [0, 0], []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        if V.L.leggi(p) is None:
            continue
        righe = p.read_text(encoding="utf-8").split("\n")
        dove = [i for i, r in enumerate(righe) if not V._RIGA_DI_STORIA.match(r) and V._RIGA_LINGUAGGI.search(r)]
        if len(dove) != 1:
            continue
        conto["schede con una riga dei linguaggi"] += 1
        if V.linguaggi(p)[0]:
            conto["già fuori regola"] += 1
            continue
        m = V._RIGA_LINGUAGGI.search(righe[dove[0]])
        giudicata = False
        for rx in nomi.values():
            elenco = re.sub(rf"\b(?:{rx})\b", "…", m.group(1), flags=re.I)
            if elenco == m.group(1):
                continue
            copia = list(righe)
            copia[dove[0]] = righe[dove[0]][:m.start(1)] + elenco + righe[dove[0]][m.end(1):]
            v, _ = _giudica("\n".join(copia), p.name)
            # un linguaggio che la scheda ha ma che la sua razza non dà (il Nanico di un mezzorco) non conta
            if not v and not _giudica("\n".join(copia).replace(m.group(1), "…"), p.name)[0]:
                continue
            atteso = [x for x in (v[0]["atteso"] if v else _giudica(
                "\n".join(copia).replace(elenco, "…"), p.name)[0][0]["atteso"])]
            if not re.search(rx, "|".join(nomi[x] for x in atteso)):
                continue
            giudicata = True
            esito[1] += 1
            if v:
                esito[0] += 1
            else:
                perse.append(f"{p.relative_to(ROOT)}: tolto {rx}")
        conto["giudicate"] += giudicata
    fuori = {"conto": conto, "esito": {"trovate": esito[0], "scritte": esito[1]}, "perse": perse}
    (Path(__file__).parent / "misure-linguaggi.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, n in conto.items():
        print(f"{k:36} {n}")
    print(f"{'linguaggio automatico tolto':36} {esito[0]}/{esito[1]}")
    for x in perse:
        print("  persa:", x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
