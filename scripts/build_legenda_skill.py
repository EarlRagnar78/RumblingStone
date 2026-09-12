#!/usr/bin/env python3
"""
build_legenda_skill — genera le tabelle di `legenda-universale.md` (ADR-0048).

La pagina della skill era una **copia a mano** della legenda: il rischio che
ADR-0048 dichiara, e che al momento della migrazione non si era ancora
materializzato — le 63 voci coincidevano tutte. Il difetto non era un errore
presente, era che niente lo impediva.

🐛 **E qualcosa era gia' scivolato, in un modo che nessuno guarda**: un blocco
di nota su ADR-0042 stava **in mezzo alle righe** della tabella «Oggetti», che
ogni lettore markdown rende quindi come **due** tabelle, con le ultime tre voci
(🔮 🪑 🧱) orfane dell'intestazione. Generandola, quella forma non e' piu'
esprimibile.

Solo le tabelle si generano, fra i marcatori `<!-- legenda:auto-begin -->` e
`<!-- legenda:auto-end -->`; la prosa intorno resta scritta a mano, perche' e'
didattica e non dato.

Uso:
    python3 scripts/build_legenda_skill.py            # riscrive le tabelle
    python3 scripts/build_legenda_skill.py --check    # esce 1 se divergono
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent
sys.path.insert(0, str(RADICE))
from dmcore import legenda  # noqa: E402

PAGINA = (RADICE.parent / "skills" / "rumblingstone-mapmaking" /
          "references" / "legenda-universale.md")
APRE = "<!-- legenda:auto-begin -->"
CHIUDE = "<!-- legenda:auto-end -->"

SEZIONI = (
    ("fill", "Terreni (fill — regioni organiche texturizzate)"),
    ("unit", "Unità (token con gradiente e anello)"),
    ("icon", "Oggetti (prop vettoriali illustrati, originali in-house)"),
)


def componi() -> str:
    simboli = legenda.simboli()
    muri, pesanti = legenda.muri(), legenda.pattern_pesanti()
    fuori = [APRE, ""]
    for modo, titolo in SEZIONI:
        fuori += [f"## {titolo}", "", "| Simbolo | Significato | Muro |", "|---|---|---|"]
        for sim, spec in simboli.items():
            if spec["mode"] != modo:
                continue
            muro = "**sì**" if sim in muri else "—"
            fuori.append(f"| {sim} | {spec['it']} | {muro} |")
        fuori.append("")
    solidi = " ".join(s for s, d in simboli.items() if d.get("pat") in pesanti)
    fuori += [
        f"`{solidi}` sono \"solidi\": ombra portata, contorno a inchiostro marcato,",
        "occlusione ambientale sul terreno adiacente, griglia chiara sopra.",
        "",
        CHIUDE,
    ]
    return "\n".join(fuori)


def atteso() -> str:
    testo = PAGINA.read_text(encoding="utf-8")
    a, b = testo.index(APRE), testo.index(CHIUDE) + len(CHIUDE)
    return testo[:a] + componi() + testo[b:]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="non scrive: esce 1 se la pagina e' fuori sincronia")
    args = ap.parse_args()

    nuovo = atteso()
    if args.check:
        if PAGINA.read_text(encoding="utf-8") != nuovo:
            print(f"✗ {PAGINA.name} e' fuori sincronia con legend.yaml: "
                  f"rigenera con `python3 scripts/build_legenda_skill.py`",
                  file=sys.stderr)
            return 1
        print(f"✓ build_legenda_skill: {len(legenda.simboli())} simboli in sincronia")
        return 0

    PAGINA.write_text(nuovo, encoding="utf-8")
    print(f"✓ {PAGINA.name} — {len(legenda.simboli())} simboli")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
