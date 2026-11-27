#!/usr/bin/env python3
"""Banco del lotto 4 (ADR-0126): un talento in più o in meno messo apposta.

Per ogni scheda del Bestiario con una riga dei talenti si scrivono due copie:

* `uno in più`: la riga prende un talento che la scheda non ha;
* `uno in meno`: la riga perde l'ultimo talento che entra nel conto.

Una copia conta come trovata se compare una violazione `numero.talenti` che
prima non c'era (o cambia il numero contato). Le schede di cui il conto è un
dubbio (classe non letta, classe senza talenti bonus nel plugin) restano nel
totale, in una colonna a parte. Una mutazione che rimette in regola una scheda
già fuori conto non è un errore messo apposta: si conta a parte e non entra.

Uso: python3 muta_numero_talenti.py  (scrive misure-numero-talenti.json accanto)
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

IN_PIU = ["Allerta", "Correre", "Tempra Possente", "Alertness", "Run"]


def _esito(testo: str, p: Path) -> "tuple[set, bool]":
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / p.name
        q.write_text(testo, encoding="utf-8")
        v, n = V.numero_talenti(q)
    return {(x["regola"], str(x["ha"])) for x in v}, bool(n)


def mutazioni(testo: str, p: Path):
    f = V.VT.leggi(p)
    righe = testo.split("\n")
    i = f["riga"] - 1
    nuovo = next(t for t in IN_PIU if t.lower() not in testo.lower())
    ultimo = next((n for n in reversed(f["nomi"]) if not V._FUORI_CONTO.search(n) and V.VT.risolvi(f["sistema"], n)), None)
    if ultimo and ultimo in righe[i]:
        yield "uno in più", "\n".join(righe[:i] + [righe[i].replace(ultimo, f"{ultimo}, {nuovo}", 1)] + righe[i + 1:])
        tolta = righe[i].replace(f", {ultimo}", "", 1) if f", {ultimo}" in righe[i] else righe[i].replace(f"{ultimo}, ", "", 1)
        if tolta != righe[i]:
            yield "uno in meno", "\n".join(righe[:i] + [tolta] + righe[i + 1:])


def main() -> int:
    esiti = {"uno in più": [0, 0, 0], "uno in meno": [0, 0, 0]}      # trovate, in schede giudicate, in schede dubbie
    schede, perse, annullate = 0, [], 0
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        if V.VT.leggi(p) is None or V.L.leggi(p) is None:
            continue
        testo = p.read_text(encoding="utf-8")
        prima, dubbia = _esito(testo, p)
        schede += 1
        fatte = [(nome, *_esito(mutata, p)) for nome, mutata in mutazioni(testo, p)]
        # una classe senza talenti bonus nel plugin rende dubbia tutta la scheda, anche quando un conto torna
        dubbia = dubbia or any(d for _, _, d in fatte)
        for nome, dopo, _ in fatte:
            if prima and not dopo and not dubbia:
                annullate += 1          # la scheda era già fuori conto e la mutazione la rimette in regola
                continue
            e = esiti[nome]
            e[2 if dubbia else 1] += 1
            if dopo - prima:
                e[0] += 1
            elif not dubbia:
                perse.append(f"{p.name}: {nome}")
    tot = [sum(e[0] for e in esiti.values()), sum(e[1] + e[2] for e in esiti.values()), sum(e[1] for e in esiti.values())]
    fuori = {"schede_con_talenti": schede,
             "per_mutazione": {k: {"trovate": a, "in_schede_giudicate": b, "in_schede_dubbie": c} for k, (a, b, c) in esiti.items()},
             "annullate_da_una_violazione_gia_presente": annullate,
             "trovate": f"{tot[0]}/{tot[1]}", "nelle_schede_giudicate": f"{tot[0]}/{tot[2]}", "perse": perse}
    (Path(__file__).parent / "misure-numero-talenti.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(fuori, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
