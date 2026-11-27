#!/usr/bin/env python3
"""estrai.py — i fatti dei talenti delle schede del Bestiario, uguali per tutti i verificatori.

Esperimento del 2026-11-11 (thread «Valutare la verifica delle regole con Prolog»).
L'estrazione è LA STESSA per Python, Prolog e clingo: il confronto misura solo lo
strato che ragiona, non il lettore delle schede.

Per ogni scheda leggibile da `dmcore.lettura_creatura.leggi` (gs, tipo, caratteristiche)
prende la riga «Talenti/Feats», la spezza alle virgole, toglie markup e parentesi,
e risolve ogni nome con `dmcore.talenti.nome_inglese`. Le classi si normalizzano
all'inglese minuscolo (`fighter`), che è la chiave dei prerequisiti `classe`.

Uscita: JSON su stdout, una voce per scheda:
  {file, sistema, car{For..Car}, bab, livelli{classe:n}, dv, lic, talenti[en], ignoti[str]}

Solo lettura del repo.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import lettura_creatura as L  # noqa: E402
from dmcore import progressione as P  # noqa: E402
from dmcore import talenti as T  # noqa: E402

RIGA = re.compile(r"^\W*(?:Talenti|Feats)\W*(?:[:：]|\*\*)\s*(.+)$", re.I | re.M)
IT_EN = {"barbaro": "barbarian", "bardo": "bard", "chierico": "cleric", "druido": "druid",
         "guerriero": "fighter", "monaco": "monk", "paladino": "paladin", "ranger": "ranger",
         "ladro": "rogue", "stregone": "sorcerer", "mago": "wizard"}
INCANTATORI = {"wizard": 1, "sorcerer": 1, "cleric": 1, "druid": 1, "bard": 1,
               "paladin": 0.5, "ranger": 0.5}


def _pezzi(riga: str) -> list[str]:
    riga = re.sub(r"`[^`]*`|\*|_", "", riga)
    riga = re.split(r"\s—\s|\.\s+[A-Z]", riga)[0]          # la prosa dopo l'elenco
    out, prof, buf = [], 0, ""
    for ch in riga:                                           # virgole fuori parentesi
        prof += (ch == "(") - (ch == ")")
        if ch == "," and prof == 0:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return [re.sub(r"\s*\(.*?\)\s*", " ", x).strip(" .;") for x in out if x.strip()]


def sistema_di(p: Path, testo: str) -> str:
    return "pf1e" if ("PF1e" in testo[:2000] or "pf1e" in p.as_posix().lower()) else "dnd35"


def scheda(p: Path) -> "dict | None":
    s = L.leggi(p)
    if s is None:
        return None
    m = RIGA.search(L.senza_note(s.testo)) or RIGA.search(s.testo)
    if not m:
        return None
    sistema = sistema_di(p, s.testo)
    livelli: dict[str, int] = {}
    dv = 0
    for g in s.gruppi:
        dv += g.n
        n = g.nome.lower()
        n = P.ABBREVIAZIONI.get(n, n)
        n = IT_EN.get(n, n)
        if P.classe(n) or n in INCANTATORI:
            livelli[n] = livelli.get(n, 0) + g.n
    lic = int(max([livelli.get(c, 0) * f if livelli.get(c, 0) >= (4 if f < 1 else 1) else 0
                   for c, f in INCANTATORI.items()] or [0]))
    talenti, ignoti = [], []
    for nome in _pezzi(m.group(1)):
        en = T.nome_inglese(sistema, nome)
        (talenti if en else ignoti).append(en or nome)
    car = {k: v for k, v in s.attributi.items() if isinstance(v, int)}
    return {"file": p.relative_to(ROOT).as_posix(), "sistema": sistema, "car": car,
            "bab": s.bab, "livelli": livelli, "dv": dv or None, "lic": lic,
            "talenti": sorted(set(talenti)), "ignoti": ignoti}


def tutte(radice: Path = ROOT / "Bestiario") -> list[dict]:
    return [d for p in sorted(radice.rglob("*.md")) if (d := scheda(p))]


if __name__ == "__main__":
    json.dump(tutte(), sys.stdout, ensure_ascii=False, indent=1)
