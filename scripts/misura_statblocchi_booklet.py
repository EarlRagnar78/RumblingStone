#!/usr/bin/env python3
"""misura_statblocchi_booklet.py — in che forma escono le creature dei booklet (ADR-0105).

## Perché esiste

Il DM, il 2026-10-29, sfogliando i booklet: *«i draghi sembrano parti di testo
mentre i PNG e forse boss minori hanno un layout grafico migliore […] possiamo
rendere il layout uniforme per tutti i tipi di creature e PNG, villain e
mostri, […] misurando questo miglioramento anche nei booklet che vengono
stampati?»*. La stampa non decideva nessuna forma: copiava quella del master.
Solo il blocco ```statblocco diventava un riquadro, e i master scrivevano le
statistiche in cinque modi.

Questo script conta, booklet per booklet, ogni scheda di creatura e la forma in
cui esce:

| forma | come la riconosce | in stampa |
|---|---|---|
| `riquadro` | il recinto ```statblocco, con o senza le righe di ADR-0091 | il riquadro a fasce |
| `griglia` | un recinto qualunque con dentro CA, pf e un attacco o i TS | testo a spaziatura fissa |
| `prosa` | un paragrafo con CA, pf e un attacco o i TS | un paragrafo |
| `tabella` | una riga di tabella con CA, pf e un attacco o i TS | una riga di tabella |
| `sciolta` | una riga **Difesa** di ADR-0091 senza il recinto sopra | due paragrafi |

La quota che conta è `riquadro / schede`. Una scheda è «fuori forma» se non sta
nel riquadro.

## Cosa NON misura, dichiarato

La forma, non il contenuto: un riquadro coi numeri sbagliati conta come un
riquadro (i numeri li controllano `conformita_statblocchi` e
`copertura_scene`). Il riconoscimento delle forme libere è per indizi: una riga
della tabella di scala che riassume il boss («337 pf, CA 36, morso +34») non ha
un attacco coi dadi fra parentesi e non conta, ma un paragrafo che cita i
numeri di una creatura per spiegarli può contare, salvo i paragrafi di conto
con un'apertura fissa («**I conti.**», «⚠ Non SRD», «Boost log»), che non contano. Per questo il cancello è un
cricchetto (non si sale), non un obbligo a zero.

## Uso

    python3 scripts/misura_statblocchi_booklet.py               # la tabella
    python3 scripts/misura_statblocchi_booklet.py --dettaglio   # ogni scheda fuori forma, con la riga
    python3 scripts/misura_statblocchi_booklet.py --stampa      # conta anche i riquadri nel sorgente di stampa
    python3 scripts/misura_statblocchi_booklet.py --json
    python3 scripts/misura_statblocchi_booklet.py --check       # la CI: nessun booklet sopra il suo tetto
    python3 scripts/misura_statblocchi_booklet.py --aggiorna    # riscrive i tetti (solo verso il basso)

Exit: 0 ok · 1 un booklet ha più schede fuori forma del suo tetto (--check).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore.statblock import accosta_parte_leggibile, sezioni_leggibili  # noqa: E402
from dmcore.testo import capitoli_del_volume, leggi_per_la_stampa, togli_storico  # noqa: E402

TETTI = ROOT / "docs" / "audit" / "statblocchi-booklet.json"
FORME = ("riquadro", "griglia", "prosa", "tabella", "sciolta")

_CA = re.compile(r"\bCA\b\**\s*:?\s*\**\s*\d")
_PF = re.compile(r"\b\d+\s*\**\s*(?:pf|PF)\b|\b(?:pf|PF|DV)\b\**\s*:?\s*\**\s*\d")
_TS = re.compile(r"\bTS\b|\bTemp(?:ra)?\b\**\s*:?\s*\**\s*[+-]\d")
_ATTACCO = re.compile(r"[+-]\d+(?:/[+-]\d+)*\s*\(\s*\d+d\d+")
# I paragrafi che spiegano i numeri di un riquadro («**I conti.** CA 10 − 1 +
# 15 = 24…», la nota «⚠ Non SRD», il registro del potenziamento) li citano ma
# non sono una scheda: hanno un'apertura fissa e non contano.
_COMMENTO = re.compile(r"^(?:\*\*I conti\b|\*\*Perché GS\b|\*\*Benchmark\b|⚠|Boost log\b)")


def e_scheda(testo: str) -> bool:
    """CA e pf, più i tiri salvezza o un attacco coi dadi: i numeri di una creatura."""
    return bool(_CA.search(testo) and _PF.search(testo)
                and (_TS.search(testo) or _ATTACCO.search(testo)))


def censisci(md: str) -> list[tuple[str, str]]:
    """Le schede di un testo, ognuna con la sua forma e la prima riga che la mostra."""
    md = accosta_parte_leggibile(re.sub(r"<!--.*?-->", "", togli_storico(md), flags=re.S))
    righe = md.split("\n")
    fuori: list[tuple[str, str]] = []
    i = 0
    while i < len(righe):
        s = righe[i].strip()
        if s.startswith("```"):
            recinto = s
            j = i + 1
            while j < len(righe) and not righe[j].strip().startswith("```"):
                j += 1
            corpo = "\n".join(righe[i + 1:j])
            if recinto == "```statblocco":
                nome = re.search(r"^nome:\s*(.+)$", corpo, re.M)
                fuori.append(("riquadro", nome.group(1) if nome else corpo.split("\n", 1)[0]))
                _, i = sezioni_leggibili(righe, j + 1)
                continue
            if e_scheda(corpo):
                prima = next((r.strip() for r in righe[i + 1:j] if r.strip(" =-")), "")
                fuori.append(("griglia", prima))
            i = j + 1
            continue
        if s.startswith("**Difesa**"):
            fuori.append(("sciolta", s))
            _, i = sezioni_leggibili(righe, i)
            continue
        if s.startswith("|"):
            if e_scheda(s):
                fuori.append(("tabella", s))
            i += 1
            continue
        if not s or s.startswith(("#", ">")):
            i += 1
            continue
        j = i
        while j < len(righe) and righe[j].strip() and not righe[j].strip().startswith(("#", "```", "|", ">")):
            j += 1
        paragrafo = " ".join(r.strip() for r in righe[i:j])
        # Una voce d'elenco che cita i numeri è regia («Round di sorpresa: …
        # contro CA 18»), non una scheda: le schede in prosa sono paragrafi.
        if e_scheda(paragrafo) and not re.match(r"^(?:[-*+]|\d+[.)])\s", paragrafo) \
                and not _COMMENTO.match(paragrafo):
            fuori.append(("prosa", paragrafo))
        i = j
    return fuori


def manifesti() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.manifest.json")
                  if "build/" not in p.relative_to(ROOT).as_posix()
                  and "_ARCHIVIO" not in p.as_posix())


def schede_del_booklet(mp: Path) -> list[tuple[str, str, str]]:
    """(forma, capitolo, riga) per ogni scheda dei capitoli che il booklet stampa."""
    man = json.loads(mp.read_text(encoding="utf-8"))
    base = mp.parent
    nel_volume = capitoli_del_volume(base, man)
    voci = ([{"file": man["intro_md"], "title": "introduzione"}] if man.get("intro_md") else [])
    voci += man.get("chapters", [])
    fuori = []
    for cap in voci:
        if cap.get("layout") == "schede":
            continue          # le schede dei PG hanno un'impaginazione loro (dmcore.schede)
        f = (base / cap["file"]).resolve()
        if not f.is_file():
            continue
        for forma, riga in censisci(leggi_per_la_stampa(f, nel_volume)):
            fuori.append((forma, cap.get("title", f.stem), riga))
    return fuori


def nome_booklet(mp: Path) -> str:
    return mp.relative_to(ROOT).as_posix()


def riquadri_in_stampa(mp: Path) -> int:
    """Quanti `#statblocco(` ci sono nel sorgente Typst che va in stampa: la
    prova che il riquadro arriva sulla carta, non solo nel master."""
    import export_booklet_typst as ex
    man = json.loads(mp.read_text(encoding="utf-8"))
    import contextlib
    import io
    with contextlib.redirect_stderr(io.StringIO()):
        typ = ex.sorgente(man, mp.parent, True)
    return typ.count("#statblocco(")


def misura(stampa: bool = False) -> dict[str, dict]:
    risultato = {}
    for mp in manifesti():
        schede = schede_del_booklet(mp)
        if not schede:
            continue
        conto = Counter(forma for forma, _, _ in schede)
        voce = {forma: conto.get(forma, 0) for forma in FORME}
        voce["schede"] = len(schede)
        voce["fuori"] = len(schede) - conto.get("riquadro", 0)
        voce["dettaglio"] = [{"forma": f, "capitolo": c, "riga": r[:140]}
                             for f, c, r in schede if f != "riquadro"]
        if stampa:
            voce["riquadri_in_stampa"] = riquadri_in_stampa(mp)
        risultato[nome_booklet(mp)] = voce
    return risultato


def quota(v: dict) -> str:
    return f"{100 * v['riquadro'] / v['schede']:.0f}%" if v["schede"] else "—"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dettaglio", action="store_true", help="ogni scheda fuori forma")
    ap.add_argument("--stampa", action="store_true", help="conta i riquadri nel sorgente Typst")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="nessun booklet sopra il suo tetto")
    ap.add_argument("--aggiorna", action="store_true", help="riscrive i tetti, solo verso il basso")
    a = ap.parse_args(argv)

    dati = misura(stampa=a.stampa)
    if a.json:
        print(json.dumps(dati, ensure_ascii=False, indent=2))
        return 0

    tetti = json.loads(TETTI.read_text(encoding="utf-8"))["tetti"] if TETTI.is_file() else {}
    if a.aggiorna:
        nuovi = {k: min(v["fuori"], tetti.get(k, v["fuori"])) for k, v in dati.items()}
        TETTI.parent.mkdir(parents=True, exist_ok=True)
        TETTI.write_text(json.dumps({
            "_cos_e": "Per ogni booklet, quante schede di creatura possono uscire fuori dal "
                      "riquadro (ADR-0105). Si scende soltanto: --aggiorna non alza un tetto. "
                      "Lo legge scripts/misura_statblocchi_booklet.py --check.",
            "tetti": dict(sorted(nuovi.items())),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✓ tetti riscritti in {TETTI.relative_to(ROOT)}")
        return 0

    tot = Counter()
    print(f"{'booklet':<62} {'schede':>6} {'riquadro':>8} {'fuori':>5} {'quota':>6}"
          + ("  in stampa" if a.stampa else ""))
    for nome, v in dati.items():
        for k in ("schede", "riquadro", "fuori"):
            tot[k] += v[k]
        print(f"{nome[-62:]:<62} {v['schede']:>6} {v['riquadro']:>8} {v['fuori']:>5} {quota(v):>6}"
              + (f"  {v['riquadri_in_stampa']:>9}" if a.stampa else ""))
        if a.dettaglio:
            for d in v["dettaglio"]:
                print(f"    {d['forma']:<8} {d['capitolo'][:30]:<30} {d['riga'][:90]}")
    if tot["schede"]:
        print(f"{'TOTALE':<62} {tot['schede']:>6} {tot['riquadro']:>8} {tot['fuori']:>5} "
              f"{100 * tot['riquadro'] / tot['schede']:>5.0f}%")

    if a.check:
        sopra = [(k, v["fuori"], tetti.get(k, 0)) for k, v in dati.items()
                 if v["fuori"] > tetti.get(k, 0)]
        for k, n, t in sopra:
            print(f"✗ {k}: {n} schede fuori dal riquadro, il tetto è {t}. "
                  "Una scheda nuova va in un blocco ```statblocco (ADR-0105).", file=sys.stderr)
        if sopra:
            return 1
        print("✓ nessun booklet sopra il suo tetto di schede fuori forma")
    return 0


if __name__ == "__main__":
    sys.exit(main())
