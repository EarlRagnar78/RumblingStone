#!/usr/bin/env python3
"""decisioni_dm.py — le decisioni aperte al DM: una fonte, un aggregato generato.

`STATO-E-ORDINE-DEI-PIANI` §4 e' il cruscotto di cosa aspetta il DM. Era scritto
a mano, e per questo si e' sfasato: il 2026-09-06 dava **D1 ancora aperta**
(decisa il giorno prima), **non elencava D6** (decisa due giorni prima), e
soprattutto conteneva **D7-D10 che non esistevano in nessun piano** — quattro
identificatori nati nell'aggregato, senza una fonte da cui derivare.

Da qui la stessa forma che il repo usa per i tool (ADR-0012): la FONTE sono le
tabelle dentro i piani, l'aggregato e' un ARTEFATTO GENERATO, e il drift e'
rosso in CI.

    plans/<PIANO>.md  <!-- decisioni-dm: <etichetta> -->
                     |
                     +--> STATO-E-ORDINE §4, fra i marker auto:begin/auto:end

⚠️ `D<n>` NON e' un identificatore globale: otto piani hanno il loro D1..Dn con
significati incompatibili (in `REVISIONE-ARC07` sono 17 decisioni **gia' prese**,
in `RICERCA-AUDIT` sono **difetti**). Per questo conta solo cio' che e'
**dichiarato** col marker, e l'identita' e' la coppia `<etichetta>#<D<n>>` —
mai il numero da solo. E' la lezione di ADR-0041: non indovinare, contare cio'
che e' instradato.

Stato di una decisione: **chiusa** se l'id e' barrato (`~~D1~~`), aperta
altrimenti. Non si deduce dal testo — si legge da un segno.

Uso:
    python3 scripts/decisioni_dm.py --check    # gate CI (non scrive)
    python3 scripts/decisioni_dm.py --emit     # rigenera l'aggregato

Exit code: 0 = ok · 1 = drift o fonte malformata · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
PIANI = RADICE / "plans"
AGGREGATO = PIANI / "STATO-E-ORDINE-DEI-PIANI.md"
CHIAVE = "decisioni-dm"

# Il marker e' una RIGA, non una menzione: `^…$` sull'intera riga sfrondata.
# Senza l'ancoraggio, citarlo dentro una frase — come fa la riga di CHANGELOG
# che racconta questa ADR — lo trasforma in una tabella fantasma. Trovato al
# primo uso vero del gate, da lui stesso.
MARKER = re.compile(r"^<!--\s*decisioni-dm:\s*(?P<etichetta>[^>]+?)\s*-->$")
# La cella dell'id tollera enfasi e fregi: `**D13** 🆕` e' la stessa decisione
# di `D13`. Prima non lo era, e il modo in cui falliva era il peggiore
# possibile — la riga veniva **saltata in silenzio**, il conto restava
# plausibile, e l'aggregato risultava allineato senza contenerla. Trovato
# scrivendo D13 (lotto 4c): un difetto che il gate di ADR-0047 esiste per
# impedire, nella forma in cui il gate non lo vedeva.
CELLA_ID = r"[*_\s]*(?P<barre>~~)?[*_\s]*(?P<id>D\d+)[*_\s]*(?:~~)?[*_\s]*(?:[^\w|]*)"
RIGA = re.compile(rf"^\|{CELLA_ID}\|(?P<resto>.*)\|\s*$")
INIZIO = f"<!-- auto:begin key={CHIAVE} -->"
FINE = f"<!-- auto:end key={CHIAVE} -->"


class Decisione:
    def __init__(self, piano: str, ident: str, aperta: bool, ambito: str, testo: str):
        self.piano, self.ident, self.aperta = piano, ident, aperta
        self.ambito, self.testo = ambito, testo

    @property
    def chiave(self) -> str:
        """L'identita' vera: il numero da solo collide fra piani diversi."""
        return f"{self.piano}#{self.ident}"


def leggi_fonti(root: Path) -> tuple[list[Decisione], list[str]]:
    """Ogni tabella marcata `<!-- decisioni-dm: <etichetta> -->` in plans/."""
    decisioni: list[Decisione] = []
    errori: list[str] = []
    viste: dict[str, str] = {}

    for md in sorted((root / "plans").glob("*.md")):
        if md.name == AGGREGATO.name:
            continue
        righe = md.read_text(encoding="utf-8").split("\n")
        for i, riga in enumerate(righe):
            m = MARKER.match(riga.strip())
            if not m:
                continue
            etichetta = m.group("etichetta")
            if etichetta in viste:
                errori.append(
                    f"etichetta duplicata «{etichetta}»: {md.name} e {viste[etichetta]}"
                    " — l'identita' e' <etichetta>#<Dn>, quindi due tabelle con la"
                    " stessa etichetta si accavallerebbero"
                )
                continue
            viste[etichetta] = md.name

            trovate = 0
            for successiva in righe[i + 1:]:
                if successiva.strip().startswith("|"):
                    r = RIGA.match(successiva.rstrip())
                    if not r:
                        continue           # intestazione o riga di separazione
                    ident = r.group("id")
                    aperta = r.group("barre") is None
                    celle = [c.strip() for c in r.group("resto").split("|")]
                    ambito = celle[0] if celle else ""
                    testo = celle[1] if len(celle) > 1 else ""
                    decisioni.append(Decisione(etichetta, ident, aperta, ambito, testo))
                    trovate += 1
                elif successiva.strip() and trovate:
                    break                  # la tabella e' finita
                elif successiva.strip():
                    continue               # prosa fra marker e tabella
            if not trovate:
                errori.append(f"{md.name}: marker «{etichetta}» senza nessuna riga D<n> sotto")

    doppioni = {}
    for d in decisioni:
        doppioni.setdefault(d.chiave, []).append(d)
    for chiave, gruppo in sorted(doppioni.items()):
        if len(gruppo) > 1:
            errori.append(f"decisione ripetuta nella stessa tabella: {chiave} ×{len(gruppo)}")

    return decisioni, errori


def rendi(decisioni: list[Decisione]) -> str:
    """L'aggregato: prima le aperte, che sono quelle che aspettano il DM."""
    aperte = [d for d in decisioni if d.aperta]
    chiuse = [d for d in decisioni if not d.aperta]

    out = [INIZIO, "", f"**{len(aperte)} aperte** · {len(chiuse)} chiuse — "
           "generato da `scripts/decisioni_dm.py --emit`, non si scrive a mano.",
           "", "| # | Piano | Ambito | Domanda |", "|---|---|---|---|"]
    for d in aperte:
        out.append(f"| **{d.ident}** | `{d.piano}` | {d.ambito} | {d.testo} |")
    for d in chiuse:
        out.append(f"| ~~{d.ident}~~ | `{d.piano}` | {d.ambito} | {d.testo} |")
    out += ["", FINE]
    return "\n".join(out)


def blocco_attuale(testo: str) -> tuple[int, int] | None:
    try:
        a = testo.index(INIZIO)
        b = testo.index(FINE) + len(FINE)
    except ValueError:
        return None
    return a, b


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="Gate CI: segnala il drift, non scrive.")
    g.add_argument("--emit", action="store_true", help="Rigenera l'aggregato in STATO-E-ORDINE.")
    args = p.parse_args(argv)
    if not (args.check or args.emit):
        p.print_help()
        return 2

    decisioni, errori = leggi_fonti(RADICE)
    if errori:
        for e in errori:
            print(f"✗ {e}", file=sys.stderr)
        return 1
    if not decisioni:
        print("✗ nessuna tabella marcata `<!-- decisioni-dm: … -->` in plans/",
              file=sys.stderr)
        return 1

    testo = AGGREGATO.read_text(encoding="utf-8")
    posizione = blocco_attuale(testo)
    if posizione is None:
        print(f"✗ {AGGREGATO.name}: manca il blocco `{INIZIO}` … `{FINE}`",
              file=sys.stderr)
        return 1

    atteso = rendi(decisioni)
    a, b = posizione
    if testo[a:b] == atteso:
        aperte = sum(1 for d in decisioni if d.aperta)
        print(f"✓ decisioni_dm: {len(decisioni)} decisioni in "
              f"{len({d.piano for d in decisioni})} piani — {aperte} aperte, aggregato allineato")
        return 0

    if args.emit:
        AGGREGATO.write_text(testo[:a] + atteso + testo[b:], encoding="utf-8")
        print(f"✓ aggiornato: {AGGREGATO.relative_to(RADICE)}")
        return 0

    print("✗ decisioni_dm: l'aggregato di STATO-E-ORDINE §4 non combacia con i piani.\n"
          "  E' esattamente lo sfasamento che questo gate esiste per impedire.\n"
          "  Rigeneralo:  python3 scripts/decisioni_dm.py --emit", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
