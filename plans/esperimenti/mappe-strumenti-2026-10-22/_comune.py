"""
_comune.py — il pezzo condiviso dagli script di prova del 2026-10-22.

Legge le griglie con il parser del renderer e la legenda funzionale, come
fanno collaudo_mappe.py e qualita_mappe.py; non scrive niente nel repo.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = QUI.parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import collaudo_mappe as C  # noqa: E402
import qualita_mappe as Q  # noqa: E402

R, F, MODO, FUORI = C.R, C.F, C.MODO, C.FUORI


def mappe_di(file: Path) -> list[dict]:
    return R.extract_maps(file.read_text(encoding="utf-8"))


def collaudo(file: Path, indice: int, g: dict, corpus: dict | None = None) -> "C.Collaudo":
    corpus = {} if corpus is None else corpus
    return C.Collaudo(file, indice, g, corpus).esegui()


def voto_di(file: Path, indice: int, g: dict, metriche: bool = False):
    """Il voto di qualita_mappe.py su una griglia gia' letta, e i codici dei
    rilievi non derogati (qualita + collaudo); con metriche=True anche q.m."""
    q = Q.Qualita(collaudo(file, indice, g)).esegui()
    codici = sorted(r["codice"] for r in q.rilievi + q.c.rilievi if not r["deroga"])
    return (q.voto(), codici, q.m) if metriche else (q.voto(), codici)


def classe(c) -> str:
    """Le classi di cella su cui si confrontano le mappe (e le versioni).
    M muro · O ostacolo che non ferma la vista · P porta · S scala/botola ·
    H pericolo · K copertura senza blocco · U creatura · . pavimento · V fuori"""
    if c in (None, FUORI):
        return "V"
    f = F.get(c, {})
    if MODO.get(c) == "unit":
        return "U"
    if f.get("door"):
        return "P"
    if f.get("posa") == "fra_livelli":
        return "S"
    if f.get("blocks_movement") and f.get("blocks_sight"):
        return "M"
    if f.get("blocks_movement"):
        return "O"
    if f.get("hazard"):
        return "H"
    if f.get("cover") in ("half", "three_quarters", "total"):
        return "K"
    return "."


def griglia_classi(G: "C.Griglia") -> list[str]:
    return ["".join(classe(G.at(x, y)) for x in range(G.W)) for y in range(G.H)]


def impronta(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def griglia_md(titolo: str, righe: list[list[str]], annotazioni: list[str]) -> str:
    """Una griglia nel formato dei master (intestazione, COLONNE, righe, @direttive)."""
    W = max(len(r) for r in righe)
    col = " ".join(R.col_label(i) for i in range(W))
    corpo = [titolo, f"COLONNE:  {col}"]
    corpo += [f"{i:02d} " + " ".join(r) for i, r in enumerate(righe, 1)]
    corpo += [""] + annotazioni
    return (f"# {titolo}\n\n**Dimensioni**: {W * 1.5:g} m × {len(righe) * 1.5:g} m "
            f"({W} colonne × {len(righe)} righe, scala 1,5 m/quadretto)\n\n"
            "```\n" + "\n".join(corpo) + "\n```\n")
