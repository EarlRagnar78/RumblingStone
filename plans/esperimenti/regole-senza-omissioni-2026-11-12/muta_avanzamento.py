#!/usr/bin/env python3
"""Banco del lotto 3-ter (ADR-0126): l'avanzamento d'incantatore delle classi di prestigio.

Nel Bestiario una sola scheda ha una classe di prestigio che alza gli
incantesimi, quindi il banco le classi di prestigio le mette lui. Per ogni
scheda con una riga `tipo:` che nomina una classe con incantesimi «X n» (n ≥ 3)
e una lista che il controllo giudica, due livelli di X diventano due livelli di
una classe di prestigio, senza toccare la lista:

* `Loremaster` (SRD: +1 a ogni livello, qualsiasi classe): la lista resta
  giusta. È il **controllo**: non deve nascere nessuna violazione.
* `Assassin` (SRD: nessun avanzamento): la lista è di due livelli troppo alta.
* `Eldritch Knight` (SRD: +1 dal 2° livello, solo arcana): la lista è di uno
  (arcana) o due (divina) livelli troppo alta.

«Vista» = `incantatori` dà una violazione che la scheda di partenza non aveva.
Uso: python3 muta_avanzamento.py  (scrive misure-avanzamento.json accanto)
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

VERO = V._prestigio_nel_tipo
CLASSI = {"Loremaster": "controllo", "Assassin": "errore", "Eldritch Knight": "errore"}


def _violazioni(testo: str, p: Path, prima: bool) -> set:
    V._prestigio_nel_tipo = (lambda *a: None) if prima else VERO
    try:
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / p.name
            q.write_text(testo, encoding="utf-8")
            v, _ = V.incantatori(q)
    finally:
        V._prestigio_nel_tipo = VERO
    return {(x["regola"], str(x.get("ha")), str(x.get("atteso"))) for x in v}


def _mutata(testo: str, prestigio: str) -> "str | None":
    righe = testo.split("\n")
    for i, r in enumerate(righe):
        if not r.lstrip().lower().startswith("tipo:"):
            continue
        for m in re.finditer(r"(?<=[,/:])(\s*)([A-Za-zÀ-ú' -]+?)\s+(\d{1,2})\b", r):
            nome, n = m.group(2).strip(), int(m.group(3))
            k = nome.lower()
            lancia = k in V.VT.SPECIALISTI or any(re.match(rx, k) for rx in V.CLASSI_INCANTATRICI)
            if lancia and n >= 3 and not V._prestigio_en(nome, "dnd35"):
                righe[i] = r[:m.start()] + f"{m.group(1)}{nome} {n - 2} / {prestigio} 2" + r[m.end():]
                return "\n".join(righe)
        return None
    return None


def main() -> int:
    conta = {k: {"fatte": 0, "viste_prima": 0, "viste_dopo": 0} for k in CLASSI}
    schede, perse, falsi = 0, [], []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        if V.VT.sistema_di(p, testo) != "dnd35" or len(V.L.BLOCCO.findall(testo)) > 1 or _mutata(testo, "Loremaster") is None:
            continue
        v0, n0 = V.incantatori(p)
        if not (v0 or n0) and not re.search(r"^\s*[-*•]?\s*\**\d(?:°|º)", testo, re.M):
            continue
        base = _violazioni(testo, p, False)
        fatta = False
        for prestigio, tipo in CLASSI.items():
            mutata = _mutata(testo, prestigio)
            prima = _violazioni(mutata, p, True) - base
            dopo = _violazioni(mutata, p, False) - base
            if tipo == "errore" and not prima and not dopo and not any(
                    r[0].startswith("numero.incantesimi") for r in _violazioni(mutata, p, False) | base) and not n0 and not v0:
                continue                      # nessuna lista giudicata: la scheda non entra
            fatta = True
            c = conta[prestigio]
            c["fatte"] += 1
            c["viste_prima"] += bool(prima)
            c["viste_dopo"] += bool(dopo)
            if tipo == "errore" and not dopo:
                perse.append(f"{p.name}: {prestigio}")
            if tipo == "controllo" and dopo:
                falsi.append(f"{p.name}: {sorted(dopo)[:2]}")
        schede += fatta
    errori = [k for k, t in CLASSI.items() if t == "errore"]
    fuori = {"schede": schede, "per_classe": conta,
             "errori_messi": sum(conta[k]["fatte"] for k in errori),
             "errori_visti_prima": sum(conta[k]["viste_prima"] for k in errori),
             "errori_visti_dopo": sum(conta[k]["viste_dopo"] for k in errori),
             "controlli": conta["Loremaster"]["fatte"],
             "controlli_segnati_a_torto_prima": conta["Loremaster"]["viste_prima"],
             "controlli_segnati_a_torto_dopo": conta["Loremaster"]["viste_dopo"],
             "perse": perse, "falsi": falsi}
    (Path(__file__).parent / "misure-avanzamento.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(fuori, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
