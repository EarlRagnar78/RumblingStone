#!/usr/bin/env python3
"""vista_di_chi_scorre.py — il master come lo vede un DM che lo sfoglia.

Adattato da `agent_skills/first-reader/scripts/skim.py` di awesome-llm-apps
(Shubham Saboo, Apache 2.0, commit 4bf51ab704fb2c5b3803cd5191b30d7dcdb51dc2).
**Modificato** per il repo (ADR-0076): il lettore non e' chi decide se aprire
un articolo, e' il DM che conduce stasera e sfoglia il master prima di
prepararlo (L5 di PIANO-AGENT-SKILLS-ESTERNE, D2). Quindi la vista non tiene
i link e la velocita' di lettura su telefono; tiene il riquadro *La serata in
tre frasi*, i titoli, la riga «In scena» e la prima frase di ogni scena, i grassetti e le CD, cioe'
quello su cui l'occhio si ferma in un master.

Lo studio da cui parte skim.py (Nielsen Norman Group, eyetracking): chi scorre
guarda titoli, inizio delle righe, grassetti e numeri, e salta il resto. La
vista stampa solo quello, e di proposito tronca: dare il testo intero a chi
deve rispondere guasterebbe la prova.

La domanda per chi riceve la vista e' una sola: *so cosa succede stasera?*
(`skills/rumblingstone-playtest/references/dm-a-freddo.md`, primo passo).

    python3 scripts/vista_di_chi_scorre.py <master>
    python3 scripts/vista_di_chi_scorre.py <master> --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lettura_a_scene as las  # noqa: E402
from ricordo_lettura import intenzione  # noqa: E402

RADICE = Path(__file__).resolve().parent.parent

PAROLE_AL_MINUTO = 200  # indicativo: skim.py usa 238 per l'inglese, l'italiano di un master e' piu' lento
GRASSETTI_MASSIMI = 15
CD_MASSIME = 20
PAROLE_DI_TESTA = 12

_TITOLO = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.M)
_GRASSETTO = re.compile(r"\*\*(.+?)\*\*")
_CD = re.compile(r"((?:\S+\s+){0,4})CD\s*(\d{1,2})\b")
_FINE_FRASE = re.compile(r".+?[.!?…](?=\s|$)", re.S)

DOMANDA = (
    "Da questa vista soltanto: (1) cosa succede stasera, in tre frasi; "
    "(2) chi si oppone ai PG e cosa vuole; (3) cosa devi preparare prima di "
    "sederti al tavolo; (4) l'elemento della vista che ti ha fatto rispondere. "
    "«Non lo so» e' una risposta lecita, e vale un rilievo sul master."
)


_IN_SCENA = re.compile(r"^\*\*In scena\*\*.*$", re.M)


def _in_scena(corpo: str) -> str:
    """La riga del contratto «In scena» (ADR-0073): dove e chi, se la scena la porta."""
    m = _IN_SCENA.search(corpo)
    return " ".join(m.group(0).replace("**", "").split()) if m else ""


def _prima_frase(corpo: str) -> str:
    """La prima frase di prosa: salta titoli, citazioni, tabelle, la riga «In scena»."""
    for blocco in re.split(r"\n\s*\n", corpo):
        blocco = blocco.strip()
        if not blocco or blocco.startswith(("#", "|", ">", "```", "---", "<!--", "**In scena**")):
            continue
        piatto = " ".join(blocco.split())
        m = _FINE_FRASE.match(piatto)
        frase = m.group(0) if m else piatto
        parole = frase.split()
        if len(parole) > PAROLE_DI_TESTA * 3:
            frase = " ".join(parole[:PAROLE_DI_TESTA * 3]) + " …"
        return frase
    return ""


def vista(master: Path) -> dict:
    testo = master.read_text(encoding="utf-8")
    try:
        relativo = master.resolve().relative_to(RADICE).as_posix()
    except ValueError:
        relativo = master.name
    fonte, serata = intenzione(master)
    scene = [
        {"titolo": t, "in_scena": _in_scena(c), "prima_frase": _prima_frase(c)}
        for t, c in las.passaggi(testo, las.profilo_di(relativo))
        if t not in ("premessa", "fra le scene", "coda", "intero")
    ]
    grassetti = []
    for g in _GRASSETTO.findall(testo):
        g = " ".join(g.split())
        if g and g not in grassetti:
            grassetti.append(g)
    parole = len(testo.split())
    return {
        "master": relativo,
        "parole": parole,
        "minuti": max(1, round(parole / PAROLE_AL_MINUTO)),
        "serata": {"fonte": fonte, "testo": serata},
        "titoli": [("  " * (len(h) - 1)) + t for h, t in _TITOLO.findall(testo) if len(h) <= 3],
        "scene": scene,
        "grassetti": [g[:60] for g in grassetti[:GRASSETTI_MASSIMI]],
        "grassetti_in_tutto": len(grassetti),
        "cd": [
            {"cd": int(n), "prima": " ".join(p.replace("*", "").split())}
            for p, n in _CD.findall(testo)
        ][:CD_MASSIME],
    }


def in_chiaro(v: dict) -> str:
    righe = [
        "VISTA DI CHI SCORRE — il testo intero non c'è, di proposito",
        f"{v['master']} · {v['parole']} parole · circa {v['minuti']} minuti per leggerlo tutto",
        "-" * 60,
    ]
    if v["serata"]["testo"]:
        righe += [f"LA SERATA ({v['serata']['fonte']}):", "  " + v["serata"]["testo"], ""]
    else:
        righe += ["LA SERATA: il master non la dichiara", ""]
    righe.append("TITOLI:")
    righe += ["  " + t for t in v["titoli"]]
    righe += ["", "LE SCENE, la prima frase:"]
    for s in v["scene"]:
        righe.append(f"  {s['titolo']}")
        if s["in_scena"]:
            righe.append(f"      {s['in_scena']}")
        if s["prima_frase"]:
            righe.append(f"      {s['prima_frase']}")
    righe += ["", f"GRASSETTI ({len(v['grassetti'])} su {v['grassetti_in_tutto']}): " + " · ".join(v["grassetti"])]
    righe.append("CD:" + ("" if v["cd"] else " nessuna"))
    righe += [f"  CD {c['cd']} ← …{c['prima']}" for c in v["cd"]]
    righe += ["-" * 60, "DOMANDA: " + DOMANDA]
    return "\n".join(righe)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("master", type=Path)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not a.master.is_file():
        print(f"✗ non trovo {a.master}", file=sys.stderr)
        return 2
    v = vista(a.master)
    print(json.dumps(v, ensure_ascii=False, indent=2) if a.json else in_chiaro(v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
