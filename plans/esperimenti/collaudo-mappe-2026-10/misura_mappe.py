#!/usr/bin/env python3
"""Misura in sola lettura del corpus di griglie tattiche (PIANO-COLLAUDO-E-GENERAZIONE-MAPPE §2).

Riproduce i numeri del piano. Non scrive niente nel repo. Solo libreria standard.
Non e' uno strumento: e' la prova della misura. Lo strumento e' il lotto V1.

    python3 -I plans/esperimenti/collaudo-mappe-2026-10/misura_mappe.py [--json OUT]

Corpus: ogni .md con almeno una griglia secondo `render_map_svg.extract_maps`,
esclusi i derivati generati (.hb.md), gli archivi (_ARCHIVIO, _SNAPSHOT), le
fixture e gli esempi di scripts/ (alcune fixture sono rotte apposta), le guide di
docs/ e le cartelle tecniche. Le regole di movimento sono quelle dell'SRD 3.5, uguali in
PF1e: niente diagonale oltre l'angolo di un muro; una creatura Grande occupa 2x2.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
import time
from collections import Counter, deque
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import render_map_svg as R  # noqa: E402

LEG = json.loads((REPO / "scripts/legend.json").read_text(encoding="utf-8"))["symbols"]
F = {k: v.get("function", {}) for k, v in LEG.items()}
MODE = {k: v["render"]["mode"] for k, v in LEG.items()}
ESCLUSI = ("/.git/", "/build/", "/node_modules/", "/.claude/", "/pregen-pcgen/",
           ".hb.md", "_ARCHIVIO", "_SNAPSHOT", "/scripts/", "/docs/")
FUORI = "FUORI"


def n(c):
    return c.replace("️", "") if c else c


def porta(c):
    return c not in (None, FUORI) and bool(F.get(n(c), {}).get("door"))


def blocca(c):
    """Blocca il movimento. Una porta si considera aperta."""
    return c not in (None, FUORI) and bool(F.get(n(c), {}).get("blocks_movement")) and not porta(c)


def muro_o_bordo(c):
    return c == FUORI or blocca(c)


def misura_griglia(g):
    righe = [g["rows"][k] for k in sorted(g["rows"])]
    H, W = len(righe), max(len(r) for r in righe)

    def at(x, y):
        if not (0 <= y < H and 0 <= x < len(righe[y])):
            return FUORI
        return righe[y][x]

    celle = [(x, y) for y in range(H) for x in range(len(righe[y]))]
    ignote = sum(1 for x, y in celle if n(at(x, y)) not in F and n(at(x, y)) not in g["local_legend"])
    perc = {(x, y) for x, y in celle if not blocca(at(x, y))}

    def vicini(x, y):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0 or (x + dx, y + dy) not in perc:
                    continue
                if dx and dy and ((x + dx, y) not in perc or (x, y + dy) not in perc):
                    continue
                yield (x + dx, y + dy)

    comp, taglie = {}, []
    for c in perc:
        if c in comp:
            continue
        i = len(taglie)
        comp[c] = i
        coda, k = deque([c]), 0
        while coda:
            a = coda.popleft()
            k += 1
            for b in vicini(*a):
                if b not in comp:
                    comp[b] = i
                    coda.append(b)
        taglie.append(k)

    porte = Counter()
    for x, y in celle:
        if not porta(at(x, y)):
            continue
        nb = [at(x + a, y + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if not any(v != FUORI and not blocca(v) and not porta(v) for v in nb):
            porte["nessun lato percorribile"] += 1
            continue

        def capo(dx, dy):
            xx, yy = x, y
            while porta(at(xx, yy)):
                xx, yy = xx + dx, yy + dy
            return at(xx, yy)

        if (muro_o_bordo(capo(-1, 0)) and muro_o_bordo(capo(1, 0))) or \
           (muro_o_bordo(capo(0, -1)) and muro_o_bordo(capo(0, 1))):
            porte["a cavallo di un muro o del bordo"] += 1
        elif any(muro_o_bordo(v) for v in nb):
            porte["muro accanto, non a cavallo"] += 1
        else:
            porte["sospesa, nessun muro accanto"] += 1

    unita = [(x, y) for x, y in celle if MODE.get(n(at(x, y))) == "unit"]
    cop = {(x, y) for x, y in celle if F.get(n(at(x, y)), {}).get("cover") in ("half", "three_quarters", "total")}
    vicino_cop = {(x, y) for x, y in perc
                  if any((x + a, y + b) in cop for a in range(-2, 3) for b in range(-2, 3))}
    aperto, visti, vuoto = perc - vicino_cop, set(), 0
    for c in aperto:
        if c in visti:
            continue
        visti.add(c)
        coda, k = deque([c]), 0
        while coda:
            a = coda.popleft()
            k += 1
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                b = (a[0] + d[0], a[1] + d[1])
                if b in aperto and b not in visti:
                    visti.add(b)
                    coda.append(b)
        vuoto = max(vuoto, k)
    grande = set()
    for x, y in perc:
        q = ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))
        if all(c in perc for c in q):
            grande.update(q)
    np_ = len(perc)
    ridef = [(k, v) for k, v in g["local_legend"].items() if n(k) in F]
    contraddizioni = []
    for k, v in ridef:
        fk, low = F[n(k)], v.lower()
        if (fk.get("blocks_movement") and not fk.get("door")
                and re.search(r"paviment|terra|passagg|corridoio|sentiero|strada|impronta", low)) or \
           (not fk.get("blocks_movement") and re.search(r"\bmur|parete|pilastr|colonn", low)):
            contraddizioni.append(f"{k} = {v[:40]}")
    return dict(W=W, H=H, celle=len(celle), ignote=ignote, percorribili=np_,
                componenti=sum(1 for t in taglie if t >= 4), sacche=sum(1 for t in taglie if t < 4),
                porte=dict(porte), unita=len(unita),
                comp_unita=len({comp[u] for u in unita if u in comp}),
                m1=len(vicino_cop) / np_ if np_ else None, m2=vuoto / np_ if np_ else None,
                grande=len(grande) / np_ if np_ else None,
                ridefinizioni=len(ridef), contraddizioni=contraddizioni,
                nord=any(a.startswith("@north") for a in g["annotations"]),
                dichiarata=g["declared_dims"] is not None)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", help="scrive le misure per griglia in questo file")
    args = ap.parse_args()
    t0 = time.time()
    file_md = [p for p in REPO.rglob("*.md") if not any(s in str(p) for s in ESCLUSI)]
    tutte = []
    for p in sorted(file_md):
        try:
            testo = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for g in R.extract_maps(testo):
            m = misura_griglia(g)
            m.update(file=str(p.relative_to(REPO)), titolo=g["title"][:70])
            tutte.append(m)
    dt = time.time() - t0
    grandi = [m for m in tutte if m["W"] >= 12 and m["H"] >= 12]

    def med(k, ms):
        v = [m[k] for m in ms if m[k] is not None]
        return round(st.median(v), 2) if v else None

    porte = Counter()
    for m in tutte:
        porte.update(m["porte"])
    print(f"griglie {len(tutte)} in {len({m['file'] for m in tutte})} file · >=12x12: {len(grandi)} · "
          f"celle {sum(m['celle'] for m in tutte)} · {dt:.1f} s")
    print(f"simboli ignoti: {sum(m['ignote'] for m in tutte)} celle in {sum(1 for m in tutte if m['ignote'])} griglie")
    print(f"legenda locale che ridefinisce un simbolo universale: {sum(m['ridefinizioni'] for m in tutte)} voci "
          f"in {sum(1 for m in tutte if m['ridefinizioni'])} griglie; contraddicono la funzione: "
          f"{sum(len(m['contraddizioni']) for m in tutte)}")
    for m in tutte:
        for c in m["contraddizioni"]:
            print(f"    {m['file']} · {m['titolo'][:40]} · {c}")
    print(f"porte (celle): {sum(porte.values())} · " + " · ".join(f"{k} {v}" for k, v in porte.most_common()))
    print(f"griglie con >1 componente percorribile (>=4 celle): {sum(1 for m in tutte if m['componenti'] > 1)}"
          f" · con sacche <4 celle: {sum(1 for m in tutte if m['sacche'])}")
    print(f"griglie con unita': {sum(1 for m in tutte if m['unita'])} · unita' in componenti separate: "
          f"{sum(1 for m in tutte if m['comp_unita'] > 1)}")
    print(f"header dimensioni dichiarato: {sum(m['dichiarata'] for m in tutte)} · @north: {sum(m['nord'] for m in tutte)}")
    print(f">=12x12: M1 mediana {med('m1', grandi)} (sotto 0,60: "
          f"{sum(1 for m in grandi if m['m1'] is not None and m['m1'] < 0.6)}) · "
          f"M2 mediana {med('m2', grandi)} (sopra 0,20: {sum(1 for m in grandi if m['m2'] is not None and m['m2'] > 0.2)}) · "
          f"Grande 2x2 sotto l'80% del percorribile: {sum(1 for m in grandi if m['grande'] is not None and m['grande'] < 0.8)}")
    # la legenda per porte, chiusure e passaggi fra livelli (D8 del piano)
    concetti = {
        "porta": r"\bport[ae]\b", "porta segreta": r"segret", "saracinesca o grata": r"saracinesc|grat[ae]",
        "sbarre o gabbia": r"sbarr|gabbi", "botola": r"botol", "scala": r"\bscal[ae]\b",
        "salire o scendere": r"\bsal|scend|discesa", "finestra o feritoia": r"finestr|feritoi",
    }
    print("legenda universale, simboli per concetto: " + " · ".join(
        f"{c} {sum(1 for v in LEG.values() if re.search(rx, v.get('label', ''), re.I))}"
        for c, rx in concetti.items()))
    fuori = Counter()
    prosa = Counter()
    rx_prosa = re.compile(r"\b(grat[ae]|sbarr\w*|gabbi[ae]|saracinesc\w*|botol[ae]|prigion\w*|porta segreta|porte segrete)\b", re.I)
    for p in sorted(file_md):
        try:
            testo = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        griglie = R.extract_maps(testo)
        if not griglie:
            continue
        prosa[p.name] += len(rx_prosa.findall(testo))
        for g in griglie:
            for r in g["rows"].values():
                fuori.update(n(c) for c in r if n(c) not in F)
    print(f"nei file con griglie: {sum(prosa.values())} menzioni di grate, gabbie, prigioni, botole o porte segrete "
          f"in {sum(1 for v in prosa.values() if v)} file; simboli fuori legenda nelle griglie: "
          f"{len(fuori)} tipi, {sum(fuori.values())} celle")
    if args.json:
        Path(args.json).write_text(json.dumps(tutte, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
