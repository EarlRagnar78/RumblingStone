#!/usr/bin/env python3
r"""misura_box_telecomando.py — i box che decidono per il gruppo cosa capisce, sa o prova.

## Perché esiste

Un box read-aloud descrive; non dice ai giocatori cosa pensano («capite che
qualunque cosa facciate, lui ne guadagnerà»). Il 2026-11-03 (RICERCA-GUARDRAIL)
due configurazioni a confronto sui 569 box del repo:

* prima: 40 verbi di pensiero e sentimento in seconda persona, singolare e
  plurale: 15 colpi fuori dalle battute, **2 veri** (13%). Il singolare era
  quasi sempre un'eco personale voluta per un PG («la ricordi»), un sogno o un
  effetto magico;
* **rigorosa**: solo la seconda persona **plurale**, cioè il gruppo intero,
  fuori dalle battute, e non quando il verbo è seguito da «voi» («quello che
  decidete voi» dà la scelta, non la toglie): 4 colpi, **2 veri** (50%).

Si adotta la seconda. Il 2026-11-03 i 2 veri sono stati corretti nel testo
(PALIO «capite che…», P1-REVISED «sapete che…»: 4 colpi → 2) e, su richiesta
del DM, lo strumento è diventato un **cancello**: `--check` esce con 1 se
compare un colpo che non è in `ACCETTATI`, i due falsi positivi letti a mano.
`test_misure_rigorose` lo esegue in CI. Deterministico, nessuna dipendenza.

## Uso

    python3 scripts/misura_box_telecomando.py [FILE.md ...]   # default: i file vivi
    python3 scripts/misura_box_telecomando.py --check         # il cancello
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

#: Seconda persona plurale di capire, sapere, ricordare, decidere, credere,
#: pensare, temere, rendersi conto, accorgersi, sentirsi: il gruppo intero.
VERBI = re.compile(
    r"\b(capite|sapete|ricordate|decidete|credete|pensate|temete|"
    r"vi rendete conto|vi accorgete|vi sentite)\b(?!\s+voi\b(?!\s+che))", re.I)
#: I colpi letti e lasciati come sono (2026-11-03): (file, parole del box).
#: Il primo è un ricordo vero dei PG (la fortezza la conoscono davvero), il
#: secondo l'estratto dello stesso box copiato nel file dei prompt d'immagine.
#: Fino al 2026-11-08 il secondo era «Vi sentite allungare», un estratto di
#: P5 (ora in `_ARCHIVIO/`) che la rigenerazione di `extract_scene_prompts`
#: ha tolto dal file dei prompt.
ACCETTATI = (
    ("ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md", "una fortezza che conoscete"),
    ("PROMPT-IMMAGINI-07ILP.md", "una fortezza che conoscete"),
)


def accettato(p: Path, estratto: str) -> bool:
    """>>> accettato(Path("x/PROMPT-IMMAGINI-07ILP.md"), "… una fortezza che conoscete, più basse …")
    True
    """
    return any(p.name == f and pezzo in estratto for f, pezzo in ACCETTATI)


BATTUTA = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”")


def colpi(testo: str) -> list[str]:
    """Le frasi dei box col verbo, tolte le battute dei PNG.

    >>> colpi("> *Sorride, e capite che qualunque cosa facciate, lui ne guadagnerà.*")
    ['capite']
    >>> colpi("> *Le loro mani fanno quello che decidete voi.*")
    []
    >>> colpi("> *Capite anche voi che è finita.*")
    ['capite']
    >>> colpi('> *«Lo sapete anche voi» dice il re.*')
    []
    """
    import misura_craft as mc
    out = []
    for b in mc.box_read_aloud(testo):
        corpo = BATTUTA.sub(" ", mc.corpo_del_box(b))
        out += [m.group(1).lower() for m in VERBI.finditer(corpo)]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="*", type=Path, help="file markdown (default: i file vivi)")
    ap.add_argument("--check", action="store_true",
                    help="cancello: esce con 1 se c'è un colpo fuori da ACCETTATI")
    a = ap.parse_args(argv)
    import misura_craft as mc
    if a.file:
        fs = a.file
    else:
        import misura_craft as mc
        fs = [p for p in sorted(ROOT.glob("0[0-9]_*/**/*.md")) + sorted((ROOT / "10-stand-alone").glob("**/*.md"))
              if not any(x in str(p) for x in mc.ESCLUSI) and not any(x in p.name for x in mc.ESCLUSI_NOME)]
    import misura_craft as mc
    tot, trovati = 0, []
    for p in fs:
        t = p.read_text(errors="replace")
        tot += len(mc.box_read_aloud(t))
        for b in mc.box_read_aloud(t):
            corpo = BATTUTA.sub(" ", mc.corpo_del_box(b))
            for m in VERBI.finditer(corpo):
                trovati.append((p, corpo[max(0, m.start() - 90):m.end() + 70].strip()))
    nuovi = [(p, f) for p, f in trovati if not accettato(p, f)]
    print(f"BOX TELECOMANDO — {tot} box, {len(trovati)} colpi, {len(nuovi)} da correggere")
    for p, f in trovati:
        rel = p.resolve().relative_to(ROOT) if p.resolve().is_relative_to(ROOT) else p
        print(f"  {'✓ accettato' if (p, f) not in nuovi else '✗'} {rel}: …{f}…")
    if nuovi:
        print("  il box descrive quello che si vede o si sente; cosa capisce il gruppo lo decidono i giocatori")
    return 1 if a.check and nuovi else 0


if __name__ == "__main__":
    sys.exit(main())
