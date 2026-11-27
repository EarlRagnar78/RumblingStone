"""Aggiunge all'indice dei talenti 3.5 i nomi che ci sono su dndtools.net e mancano (solo nomi e manuale).

Le pagine si scaricano a parte (curl, un elenco di 181 pagine, https://dndtools.net/feats/?page=N) in una
cartella di dati; questo script legge solo i link «/feats/<manuale>--<id>/<talento>--<id>/» e non esegue
nulla dei file scaricati. I manuali 3.0 sostituiti in 3.5 (Psionics Handbook, Player's Handbook 3.0 e le
cinque guide di classe) non entrano nell'indice 3.5: vanno in talenti_manuali_30.tsv, come riferimento.

    python3 -I indice_dndtools.py <cartella-pagine> <talenti_manuali_35.tsv> <talenti_manuali_30.tsv>
"""
from __future__ import annotations

import html
import re
import sys
import unicodedata
from pathlib import Path

LINK = re.compile(r'href="/feats/([^"/]*)--\d+/[^"/]*--\d+/">([^<]*)')
SOSTITUITI_30 = re.compile(r"-30$|guidebook-to")


def norma(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def manuale(slug: str) -> str:
    return " ".join(w.capitalize() if w not in {"of", "the", "and", "a", "to"} else w for w in slug.split("-"))


def main(cartella: str, tsv35: str, tsv30: str) -> int:
    trovati: dict[tuple[str, str], None] = {}
    for p in sorted(Path(cartella).glob("p*.html")):
        for slug, nome in LINK.findall(p.read_text(encoding="utf-8", errors="replace")):
            trovati[(slug, html.unescape(nome).strip())] = None
    righe = Path(tsv35).read_text(encoding="utf-8").splitlines()
    noti = {norma(r.split("\t")[0]) for r in righe if r and not r.startswith("#")}
    nuovi35, nuovi30 = [], []
    for slug, nome in trovati:
        if norma(nome) in noti:
            continue
        (nuovi30 if SOSTITUITI_30.search(slug) else nuovi35).append(f"{nome}\t{manuale(slug)}\tdndtools")
        noti.add(norma(nome))
    testa = [r for r in righe if r.startswith("#")]
    corpo = [r for r in righe if r and not r.startswith("#")]
    nota = "# Aggiunti da dndtools.net (2026-11-07, solo nomi e manuale): abbinamenti/indice_dndtools.py."
    if nota not in testa:
        testa.append(nota)
    corpo = [corpo[0]] + sorted(set(corpo[1:] + nuovi35))
    Path(tsv35).write_text("\n".join(testa + corpo) + "\n", encoding="utf-8")
    Path(tsv30).write_text(
        "# Talenti dei manuali 3.0 sostituiti in 3.5 (Psionics Handbook, Player's Handbook 3.0, guide di classe),\n"
        "# da dndtools.net (2026-11-07), solo nomi: non valgono come fonte in un modulo 3.5, servono a riconoscere\n"
        "# un nome 3.0 e a cercare il sostituto 3.5. abbinamenti/indice_dndtools.py.\n"
        "inglese\tmanuale\tfonte\n" + "\n".join(sorted(nuovi30, key=norma)) + "\n", encoding="utf-8")
    print(f"dndtools: {len(trovati)} talenti letti · {len(nuovi35)} nuovi nell'indice 3.5 · {len(nuovi30)} solo 3.0")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
