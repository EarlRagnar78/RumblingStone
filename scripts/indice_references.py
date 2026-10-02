#!/usr/bin/env python3
"""indice_references.py — l'indice in testa ai references lunghi delle skill.

L12 di PIANO-AGENT-SKILLS-ESTERNE (ADR-0077 §9). La guida di Anthropic sulle
skill (*Skill authoring best practices*, «Structure longer reference files with
table of contents») chiede un indice in testa a ogni file di riferimento oltre
le 100 righe: un agente che ne legge solo l'inizio vede comunque cosa c'è, e
apre la sezione che gli serve invece di caricare tutto o di fermarsi presto.

L'indice si genera dai titoli `##` del file (e dai `###` se i `##` sono meno di
tre), fra due marcatori, subito sotto il titolo `#`. Non si scrive a mano: un
indice scritto a mano invecchia appena qualcuno aggiunge una sezione.

    python3 scripts/indice_references.py --emit    # scrive o aggiorna gli indici
    python3 scripts/indice_references.py --check   # esce 1 se un indice manca o è vecchio

Fuori: `rumblingstone-debugging`, vendorizzata da obra/superpowers (ADR-0010),
che resta com'è arrivata.

Solo stdlib. Deterministico e idempotente.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SOGLIA = 100                     # righe: la soglia della guida di Anthropic
ESCLUSE = ("rumblingstone-debugging",)
APRE = "<!-- indice: generato da scripts/indice_references.py, non scriverlo a mano -->"
CHIUDE = "<!-- /indice -->"
_BLOCCO = re.compile(re.escape(APRE) + r".*?" + re.escape(CHIUDE) + r"\n?", re.S)
_TITOLO = re.compile(r"^(#{2,3})\s+(.+?)\s*#*\s*$")


def references() -> "list[Path]":
    return sorted(p for p in (RADICE / "skills").glob("*/references/*.md")
                  if p.parts[-3] not in ESCLUSE)


def titoli(testo: str) -> "list[tuple[int, str]]":
    """I titoli `##` e `###` fuori dai blocchi di codice e fuori dall'indice."""
    fuori, codice = [], False
    for riga in _BLOCCO.sub("", testo).splitlines():
        if riga.lstrip().startswith(("```", "~~~")):
            codice = not codice
            continue
        m = None if codice else _TITOLO.match(riga)
        if m:
            fuori.append((len(m.group(1)), m.group(2).strip()))
    return fuori


def indice(testo: str) -> "str | None":
    """Il blocco d'indice del testo, o None se il file non ne vuole uno."""
    corpo = _BLOCCO.sub("", testo)
    if len(corpo.splitlines()) <= SOGLIA:
        return None
    t = titoli(corpo)
    livello = 2 if sum(1 for n, _ in t if n == 2) >= 3 else 3
    voci = [(n, s) for n, s in t if n <= livello]
    if len(voci) < 3:
        return None
    righe = [APRE, "**In questo file**", ""]
    righe += [("  " if n == 3 and livello == 3 else "") + f"- {s}" for n, s in voci]
    return "\n".join(righe + [CHIUDE]) + "\n"


def con_indice(testo: str) -> str:
    """Il testo con l'indice al suo posto: subito dopo il titolo `#`."""
    blocco = indice(testo)
    senza = _BLOCCO.sub("", testo)
    if blocco is None:
        return senza
    righe = senza.splitlines(keepends=True)
    i = next((k for k, r in enumerate(righe) if r.startswith("# ")), -1)
    if i < 0:
        return blocco + "\n" + senza
    j = i + 1
    while j < len(righe) and not righe[j].strip():
        j += 1
    return "".join(righe[:i + 1]) + "\n" + blocco + "\n" + "".join(righe[j:])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--emit", action="store_true", help="scrive o aggiorna gli indici")
    g.add_argument("--check", action="store_true", help="esce 1 se un indice manca o è vecchio")
    a = ap.parse_args(argv)

    vecchi, con = [], 0
    for p in references():
        testo = p.read_text(encoding="utf-8")
        nuovo = con_indice(testo)
        con += APRE in nuovo
        if nuovo != testo:
            vecchi.append(p)
            if a.emit:
                p.write_text(nuovo, encoding="utf-8")
    tot = len(references())
    if a.check and vecchi:
        for p in vecchi:
            print(f"  ✗ {p.relative_to(RADICE)}: indice mancante o vecchio")
        print(f"✗ indice_references: {len(vecchi)} file da rigenerare con --emit")
        return 1
    verbo = "aggiornati" if a.emit else "allineati"
    print(f"✓ indice_references: {con} references su {tot} con l'indice, "
          f"{len(vecchi) if a.emit else 0} {verbo if a.emit else 'da aggiornare'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
