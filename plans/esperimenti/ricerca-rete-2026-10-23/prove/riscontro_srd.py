#!/usr/bin/env python3
"""
riscontro_srd.py — prova della ricerca in rete del 2026-10-23 (non adottata).

Riscontra in locale, senza rete, le regole che il giro della Sessione 2 di
ARC-08 aveva controllato «a memoria». Legge l'SRD 3.5 in Markdown
(olimot/srd-v3.5-md, OGL) e il PRD di Pathfinder 1e in SQLite
(devonjones/PSRD-Data, OGL), scaricati fuori dal repo; i percorsi si passano
come argomenti. Da lanciare con ``python3 -I`` perché legge file scaricati.

Uso:
    python3 -I riscontro_srd.py AFFERMAZIONI.json SRD35_DIR PSRD_DIR REPO
Esce 0; stampa una tabella Markdown. Sola lettura.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path


def testo_srd35(radice: Path, file: str) -> str:
    return (radice / file).read_text(encoding="utf-8")


def testo_pf1(radice: Path, db: str, nome: str) -> str:
    con = sqlite3.connect(f"file:{radice / db}?mode=ro", uri=True)
    righe = []
    for lft, rgt in con.execute("select lft, rgt from sections where name = ?", (nome,)):
        for (corpo,) in con.execute("select body from sections where lft between ? and ? and body is not null",
                                    (lft, rgt)):
            righe.append(re.sub(r"<[^>]+>", "", corpo))
    con.close()
    return "\n".join(righe)


def main() -> int:
    aff = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    srd35, psrd, repo = Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    print("| rilievo | che cosa | nell'SRD (trovato?) | il master dice | esito |")
    print("|---|---|---|---|---|")
    conta = {"concorda": 0, "DISCORDA": 0, "non trovato": 0}
    for a in aff:
        testo = testo_srd35(srd35, a["file"]) if a["srd"] == "35" else testo_pf1(psrd, a["db"], a["nome"])
        m = re.search(a["cerca"], testo)
        trovato = bool(m) and not (a.get("assente") and a["assente"] in m.group(0))
        esito = "non trovato"
        if trovato:
            esito = "concorda"
            if a.get("master"):
                mt = (repo / a["master"]).read_text(encoding="utf-8")
                if a.get("discorda") and re.search(a["master_cerca"], mt):
                    esito = "DISCORDA"
                elif not re.search(a["master_cerca"], mt):
                    esito = "non trovato nel master"
        conta[esito] = conta.get(esito, 0) + 1
        print(f"| {a['id']} | {a['cosa']} | {a['srd_dice']} ({'sì' if trovato else 'no'}) | "
              f"{a['master_dice'] or '—'} | {esito} |")
    print()
    print(" · ".join(f"{k}: {v}" for k, v in conta.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
