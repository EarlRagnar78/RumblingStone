#!/usr/bin/env python3
"""render_pg.py — dalle schede PG in dati alla scheda leggibile (ADR-0050, ADR-0088).

Scritto nella PR #99 e riportato dal lotto 4g-1 di PIANO-RIPRESA-PR-ABBANDONATE.
I fatti stanno in `PG/schede/<pg>.yaml`, validati da `validate_pg.py`; questa è
la vista. Classe, PF, stato e artefatti non ci sono: sono di
`campaign/state.yaml`, e la vista rimanda lì invece di copiarli (una copia nel
markdown diventerebbe rossa a ogni sessione).
Stessa divisione di `state.yaml` → `state.md`: i dati si modificano nel YAML, il
markdown si **rigenera**. `--check` è il gate che verifica che non abbiano preso
strade diverse.

Quello che la vista fa e i dati da soli non fanno: mostrare **la catena**. Una
riga «DES 6» non dice niente; «10 → 8 (Corona indossata) → 6 (rito dello
Smeraldo)» dice tutto, e rende visibile a colpo d'occhio se manca un anello.

Uso
  python3 scripts/render_pg.py            # rigenera PG/schede/<pg>.md
  python3 scripts/render_pg.py --check    # gate CI

Exit  0 = ok/in sync · 1 = fuori sync · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEDE = ROOT / "PG" / "schede"

ORDINE = [("for", "FOR"), ("des", "DES"), ("cos", "COS"),
          ("int", "INT"), ("sag", "SAG"), ("car", "CAR")]


def slug(pg: str) -> str:
    """Il nome del file di un PG: «Thorik» → `thorik`, «(PG 1)» → `pg-1`."""
    return re.sub(r"[^a-z0-9]+", "-", pg.lower()).strip("-") or "pg"


def scheda_vuota(pg: str) -> str:
    """La scheda di un PG di cui il repo non sa ancora niente: tutto [INFERRED]."""
    righe = [
        f"# Scheda di {pg} come dato (ADR-0088). Creata vuota dal reset per un gruppo",
        "# nuovo: classe, PF e stato sono in campaign/state.yaml (`party`); qui vanno",
        "# solo caratteristiche e modificatori permanenti, ognuno con la sua fonte.",
        "schema_version: 1",
        f"pg: {pg!r}" if not re.fullmatch(r"[\w' -]+", pg) else f"pg: {pg}",
        "",
        "caratteristiche:",
    ]
    righe += [f"  {c}: {{base: null, attuale: null, attestato_da: null}}" for c, _ in ORDINE]
    righe += ["", "modificatori_permanenti: []", ""]
    return "\n".join(righe)


def crea_schede(radice: Path, pgs: "list[str]") -> "list[str]":
    """Rifà `PG/schede/` per i PG dati: una scheda vuota e la sua vista per ognuno.

    La chiama `azzera_partita.py` dopo aver scritto il `party` del gruppo nuovo:
    le schede del gruppo di prima sono partita, e i PG nuovi devono avere la
    loro, o `validate_pg` sarebbe rosso al primo push del ramo.
    """
    cartella = radice / "PG" / "schede"
    cartella.mkdir(parents=True, exist_ok=True)
    for vecchio in [*cartella.glob("*.yaml"), *cartella.glob("*.md")]:
        vecchio.unlink()
    scritti: list[str] = []
    for pg in pgs:
        testo = scheda_vuota(pg)
        y = cartella / f"{slug(pg)}.yaml"
        y.write_text(testo, encoding="utf-8")
        import yaml
        y.with_suffix(".md").write_text(rendi(yaml.safe_load(testo)), encoding="utf-8")
        scritti.append(y.name)
    return scritti


def carica(p: Path) -> dict:
    import yaml
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def catena(dati: dict, sigla: str) -> str:
    """«10 → 8 (Corona indossata) → 6 (rito dello Smeraldo)» — o «—»."""
    car = (dati.get("caratteristiche") or {}).get(sigla.lower()) or {}
    mods = [m for m in (dati.get("modificatori_permanenti") or [])
            if str(m.get("caratteristica", "")).upper() == sigla]
    if car.get("base") is None and car.get("attuale") is None:
        if not mods:
            return "`[INFERRED]` — non attestato"
        passi = ", ".join(f"{int(m['delta']):+d} ({str(m.get('quando') or m['causa'])[:34]})"
                          for m in mods)
        return f"`[INFERRED]` valore ignoto, ma con {passi}"
    valore = car.get("base")
    pezzi = [str(valore)]
    for m in mods:
        valore = (valore or 0) + int(m["delta"])
        eti = str(m.get("quando") or m["causa"])[:34]
        pezzi.append(f"**{valore}** *({eti})*")
    return " → ".join(pezzi)


def rendi(dati: dict) -> str:
    out: list[str] = []
    w = out.append
    pg = dati.get("pg", "?")
    w(f"<!-- GENERATO da scripts/render_pg.py dal file `{slug(pg)}.yaml` — non modificare a mano. -->")
    w("")
    w(f"# {dati.get('nome_completo') or pg} — scheda dei fatti")
    w("")
    w(f"**Razza** {dati.get('razza') or '—'} · "
      f"**Allineamento** {dati.get('allineamento') or '—'}")
    w("")
    w("Classe, PF e stato di oggi: `campaign/state.yaml`, blocco `party` "
      "(e [`state.md`](../../campaign/state.md) §1). Gli artefatti: blocco `artefatti`.")
    w("")
    w("> Non è la scheda del giocatore: è l'insieme dei fatti che il repo deve tenere onesti, "
      "e sopra ogni altra cosa i **modificatori permanenti con la loro fonte**. "
      "I dati stanno in `" + f"PG/schede/{slug(pg)}.yaml" + "`; questo file si rigenera.")
    w("")
    w("## Caratteristiche — la catena, non solo il numero")
    w("")
    w("| | Catena | Oggi |")
    w("|---|---|---:|")
    for chiave, sigla in ORDINE:
        car = (dati.get("caratteristiche") or {}).get(chiave) or {}
        oggi = car.get("attuale")
        w(f"| **{sigla}** | {catena(dati, sigla)} | {oggi if oggi is not None else '—'} |")
    w("")
    mods = dati.get("modificatori_permanenti") or []
    w(f"## Modificatori permanenti — {len(mods)}")
    w("")
    if not mods:
        w("**Nessuno.** *(Un elenco vuoto è un fatto, non un vuoto: `validate_pg.py` "
          "verifica che nessun documento affermi il contrario senza che sia stato dismesso "
          "con una ragione scritta.)*")
    else:
        w("| Car. | Δ | Causa | Quando | Fonte |")
        w("|---|---:|---|---|---|")
        for m in mods:
            causa = " ".join(str(m["causa"]).split())
            w(f"| **{m['caratteristica']}** | {int(m['delta']):+d} | {causa} | "
              f"{m.get('quando') or '—'} | `{m['fonte']}` |")
    w("")
    if dati.get("vincoli"):
        w("## Vincoli permanenti non numerici")
        w("")
        for v in dati["vincoli"]:
            w(f"- **{' '.join(str(v['vincolo']).split())}**")
            if v.get("conseguenze"):
                w(f"  - *Conseguenze*: {' '.join(str(v['conseguenze']).split())}")
            w(f"  - *Fonte*: `{v['fonte']}`")
        w("")
    if dati.get("note"):
        w("## Note")
        w("")
        w(" ".join(str(dati["note"]).split()))
        w("")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="Gate CI: verifica che siano in sync.")
    args = ap.parse_args(argv)

    if not SCHEDE.is_dir():
        print(f"ERRORE: manca {SCHEDE.relative_to(ROOT)}", file=sys.stderr)
        return 2

    fuori: list[str] = []
    n = 0
    for y in sorted(SCHEDE.glob("*.yaml")):
        atteso = rendi(carica(y))
        md = y.with_suffix(".md")
        n += 1
        if args.check:
            if not md.exists() or md.read_text(encoding="utf-8") != atteso:
                fuori.append(str(md.relative_to(ROOT)))
        else:
            md.write_text(atteso, encoding="utf-8")

    if args.check:
        if fuori:
            print("✗ render_pg: schede fuori sync — rigenerare con `python3 scripts/render_pg.py`:")
            for f in fuori:
                print(f"  · {f}")
            return 1
        print(f"✓ render_pg: {n} schede allineate ai dati")
        return 0

    print(f"✓ render_pg: rigenerate {n} schede da PG/schede/*.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
