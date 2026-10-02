#!/usr/bin/env python3
"""quiz_lettura.py — quanto di un modulo resta dopo una lettura sola.

Il punteggio del quiz a due agenti
(`skills/rumblingstone-playtest/references/quiz-a-due-agenti.md`). Un agente
legge il modulo una volta e scrive appunti; un secondo agente risponde al quiz
con i soli appunti, poi a libro aperto. Questo script confronta le due serie di
risposte con la chiave del modulo e divide le domande in tre classi:

  · giusta dagli appunti            — chiaro alla prima lettura
  · giusta solo a libro aperto      — c'è, ma non resta in testa
  · sbagliata anche a libro aperto  — manca, o si contraddice

La chiave (`plans/quiz/<modulo>.json`) dà per ogni domanda una o più
alternative accettate, ciascuna una lista di parole. Una risposta è giusta se
contiene tutte le parole di almeno un'alternativa. Il confronto ignora
maiuscole, accenti e punteggiatura, e ogni parola della chiave vale come
**radice**: «tacch» accetta «tacca» e «tacche»; un numero invece combacia
esatto, «12» non accetta «120». È deterministico, e ha il suo
limite: una risposta giusta scritta con altre parole risulta sbagliata.

Uso:
    python3 scripts/quiz_lettura.py --chiave plans/quiz/ARC07-DEF-4.json \\
        --appunti risposte-appunti.json [--aperto risposte-aperto.json] [--json]
    python3 scripts/quiz_lettura.py --check      # le chiavi del repo sono ben formate

Le risposte sono un JSON `{"q1": "testo", ...}`. Solo libreria standard.
Exit code: 0 = ok · 1 = chiave o risposte malformate.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHIAVI = ROOT / "plans" / "quiz"

GIUSTA_APPUNTI = "giusta dagli appunti"
SOLO_APERTO = "giusta solo a libro aperto"
SBAGLIATA = "sbagliata anche a libro aperto"
NON_MISURATA = "sbagliata dagli appunti (libro aperto non dato)"


def parole(testo: str) -> "list[str]":
    """Minuscolo, senza accenti e senza punteggiatura, diviso in parole."""
    t = unicodedata.normalize("NFKD", testo.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", t)


def giusta(risposta: str, accettate: "list[list[str]]") -> bool:
    """Tutte le radici di almeno un'alternativa compaiono nella risposta."""
    dette = parole(risposta or "")
    for alternativa in accettate:
        radici = [r for p in alternativa for r in parole(p)]
        # Un numero combacia esatto: la radice «12» non deve accettare «120»
        # (lo ha fatto, alla prima prova sulla chiave di DEF-4).
        if radici and all(any((d == r) if r.isdigit() else d.startswith(r) for d in dette)
                          for r in radici):
            return True
    return False


def classifica(chiave: dict, appunti: dict, aperto: "dict | None") -> "list[dict]":
    righe = []
    for d in chiave["domande"]:
        a = giusta(appunti.get(d["id"], ""), d["accettate"])
        if a:
            esito = GIUSTA_APPUNTI
        elif aperto is None:
            esito = NON_MISURATA
        elif giusta(aperto.get(d["id"], ""), d["accettate"]):
            esito = SOLO_APERTO
        else:
            esito = SBAGLIATA
        righe.append({"id": d["id"], "domanda": d["domanda"], "esito": esito})
    return righe


def problemi_della_chiave(chiave: dict) -> "list[str]":
    fuori = []
    if chiave.get("stato") not in ("bozza", "approvata"):
        fuori.append("«stato» deve essere «bozza» o «approvata»")
    domande = chiave.get("domande", [])
    if not 10 <= len(domande) <= 15:
        fuori.append(f"{len(domande)} domande: la chiave ne vuole da 10 a 15")
    visti = set()
    for d in domande:
        if d.get("id") in visti:
            fuori.append(f"id ripetuto: {d.get('id')}")
        visti.add(d.get("id"))
        acc = d.get("accettate")
        if not d.get("domanda") or not acc or not all(isinstance(a, list) and a for a in acc):
            fuori.append(f"{d.get('id')}: servono la domanda e almeno un'alternativa non vuota")
    if chiave.get("modulo") and not (ROOT / chiave["modulo"]).exists():
        fuori.append(f"il modulo {chiave['modulo']} non esiste")
    return fuori


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--chiave", type=Path)
    ap.add_argument("--appunti", type=Path, help="risposte date con i soli appunti")
    ap.add_argument("--aperto", type=Path, help="risposte date a libro aperto")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="controlla le chiavi del repo")
    a = ap.parse_args(argv)

    if a.check:
        errori = 0
        for f in sorted(CHIAVI.glob("*.json")):
            for p in problemi_della_chiave(json.loads(f.read_text(encoding="utf-8"))):
                print(f"✗ {f.relative_to(ROOT)}: {p}")
                errori += 1
        print("✓ quiz_lettura: chiavi ben formate" if not errori else f"✗ {errori} problemi")
        return 1 if errori else 0

    if not a.chiave or not a.appunti:
        ap.error("servono --chiave e --appunti (oppure --check)")
    chiave = json.loads(a.chiave.read_text(encoding="utf-8"))
    guasti = problemi_della_chiave(chiave)
    if guasti:
        for p in guasti:
            print(f"✗ chiave: {p}")
        return 1
    appunti = json.loads(a.appunti.read_text(encoding="utf-8"))
    aperto = json.loads(a.aperto.read_text(encoding="utf-8")) if a.aperto else None
    righe = classifica(chiave, appunti, aperto)
    conta = {e: sum(r["esito"] == e for r in righe)
             for e in (GIUSTA_APPUNTI, SOLO_APERTO, SBAGLIATA, NON_MISURATA)}
    if a.json:
        print(json.dumps({"tool": "quiz_lettura", "chiave": str(a.chiave), "righe": righe,
                          "conta": conta}, ensure_ascii=False, indent=2))
        return 0
    for r in righe:
        print(f"  {r['id']:>4}  {r['esito']:32}  {r['domanda']}")
    print("\n  " + " · ".join(f"{e}: {n}" for e, n in conta.items() if n))
    print(f"  chiaro alla prima lettura: {conta[GIUSTA_APPUNTI]} su {len(righe)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
