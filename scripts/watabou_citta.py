#!/usr/bin/env python3
"""
watabou_citta.py — l'URL di una città di Watabou, da una scheda committata
(R5 di PIANO-RESA-E-ASSET-DELLE-MAPPE, D10).

Il Medieval Fantasy City Generator di Watabou è un'applicazione web: non ha
un'interfaccia di programmazione, ma legge i parametri dall'URL (seme,
dimensione, mura, porte, tempio...) e, con `export=svg|png|json`, esporta la
città appena generata. Questo script tiene il seme e i parametri in una scheda
JSON accanto alle mappe dell'arco, e ne ricava sempre lo stesso URL: la pianta
si rifà identica su qualunque macchina, e il repo sa da dove viene.

Le mappe che il generatore produce si possono usare liberamente, anche a scopo
commerciale (pagina itch del generatore). La pianta è un'immagine per il DM o
per i giocatori, non una griglia tattica: non passa dal collaudo.

    python3 scripts/watabou_citta.py <scheda>.watabou.json           # l'URL da aprire
    python3 scripts/watabou_citta.py <scheda>.watabou.json --export svg

Lo script non usa la rete. Esce con 1 se la scheda ha un parametro che il
generatore non conosce o un valore fuori elenco.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlencode

BASE = "https://watabou.github.io/city-generator/"

#: i parametri che il generatore legge dall'URL (devlog 0.7.3 e successivi);
#: gli interruttori valgono 0 o 1; random=0 fa usare i parametri dati
#: invece di sceglierli a caso
INTERRUTTORI = ("random", "citadel", "plaza", "temple", "walls", "shantytown", "river", "coast")
INTERI = ("seed", "size", "gates")
EXPORT = ("svg", "png", "json")


def leggi(percorso: Path) -> dict:
    dati = json.loads(percorso.read_text(encoding="utf-8"))
    if dati.get("generatore") != "city":
        raise ValueError("«generatore» deve essere «city» (il Medieval Fantasy City Generator)")
    return dati


def parametri(scheda: dict) -> dict:
    """I parametri dell'URL, in un ordine fisso: lo stesso URL per la stessa scheda."""
    p = scheda.get("parametri", {})
    ignoti = sorted(set(p) - set(INTERRUTTORI) - set(INTERI))
    if ignoti:
        raise ValueError(f"parametri che il generatore non conosce: {', '.join(ignoti)}")
    if not isinstance(p.get("seed"), int):
        raise ValueError("«seed» è obbligatorio e intero: senza, la città cambia a ogni apertura")
    fuori = {}
    for k in INTERI:
        if k in p:
            if not isinstance(p[k], int) or p[k] < 0:
                raise ValueError(f"«{k}» deve essere un intero ≥ 0")
            fuori[k] = p[k]
    for k in INTERRUTTORI:
        if k in p:
            if p[k] not in (0, 1):
                raise ValueError(f"«{k}» vale 0 o 1")
            fuori[k] = p[k]
    return fuori


def url(scheda: dict, export: str | None = None) -> str:
    p = parametri(scheda)
    if export:
        if export not in EXPORT:
            raise ValueError(f"export: uno di {', '.join(EXPORT)}")
        p["export"] = export
    return f"{BASE}?{urlencode(p)}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("scheda", type=Path, help="la scheda *.watabou.json")
    ap.add_argument("--export", choices=EXPORT, help="aggiunge export=…: il generatore esporta appena ha finito")
    args = ap.parse_args(argv)
    try:
        scheda = leggi(args.scheda)
        print(url(scheda, args.export))
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"✗ watabou_citta: {e}", file=sys.stderr)
        return 1
    if scheda.get("salva_in"):
        print(f"  salva l'esportazione in: {scheda['salva_in']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
