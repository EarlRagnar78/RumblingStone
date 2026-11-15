#!/usr/bin/env python3
"""Profili e politiche dei villain per simula_scontri.py (15/11/2026).

Il motore è quello del thread dei draghi (simula_scontri.py), importato e non
copiato. Qui solo i profili dei villain e le loro politiche: la tattica del
CANONE di oggi, scritta come la scheda la descrive, e le varianti proposte.

Uso:
    python3 profili_villain.py                 # tutti gli scontri di questo file
    python3 profili_villain.py --scontro zogtar-breccia --prove 20000
"""
from __future__ import annotations

import argparse
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
# Nel repo il motore sta nella stessa cartella (plans/esperimenti/tattiche-2026-11-15/);
# nella cartella condivisa del progetto sta in quella del thread dei draghi.
sys.path.insert(0, os.path.join(_QUI, "..", "tattiche-draghi-2026-11-15"))
sys.path.insert(0, _QUI)
import simula_scontri as m  # noqa: E402
from simula_scontri import Creatura, d, ts, tira, R  # noqa: E402,F401


def vivi(g, esclusi=()):
    return [p for p in g.values() if not p.giu() and p.nome not in esclusi and p.fuori == 0]


# ============================================== ZOG'TAR SULLA BRECCIA, ALBA
# 07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md
#   Appendice A.2 (scheda), Scena 10 «Come combatte sulla breccia».
# In Ira: ascia +29/+24/+19 (3d6+20), CA 24, pf 283 (+45 di Ira Superiore:
# COS +6 su 15 DV), Rifl +9, Vol +12, RD 3/—, Presenza Minacciosa CD 21.
# Sul camminamento SI STRINGE (SRD): −4 al colpire e −4 alla CA.
# Colpo Terrificante: azione standard, +25 in Ira, 3d6+20; Riflessi con CD pari
# al danno, o vola via di 3 m e cade prono. Sulla breccia vuol dire giù dal
# camminamento, nel cortile, 4,5 m: 1d6 (SRD). STIMA: chi cade torna in linea
# dopo 2 round (si rialza, risale la scala).
STRETTO = 4


def zogtar(pf_alba: int, stretto: bool = True) -> Creatura:
    s = STRETTO if stretto else 0
    asc = lambda: d(3, 6) + 20  # noqa: E731
    return Creatura(
        "Zog'tar", pf=pf_alba + 45, ca=24 - s, contatto=10 - s, ri=0,
        temp=21, rifl=9, vol=12,
        attacchi=[(29 - s, asc), (24 - s, asc), (19 - s, asc)],
        soffio_dadi=(0, 1), soffio_cd=0, soffio_forma="linea", presenza_cd=21,
        soglia_fuga=-10_000, rd=3)




def _presenza(g, cd, gia):
    for p in g.values():
        if p.giu() or p.immune_paura or p.nome in gia:
            continue
        gia.add(p.nome)                 # chi supera il TS è immune 24 ore
        if not ts(p.vol, cd):
            p.scosso = d(1, 4)


def _davanti(g):
    """Chi gli sta davanti sul camminamento: i due nani, se in piedi."""
    return [p for p in vivi(g) if p.nome in ("Thorik", "Tordek")]


def _colpo_terrificante(c, st, t, bonus):
    if t.giu() or not tira(25 - (STRETTO if st.flag["stretto"] else 0) + bonus, t.ca):
        return
    n = d(3, 6) + 20 + st.flag.get("occhio_danni", {}).get(t.nome, 0)
    t.subisci(n)
    if not t.giu() and not ts(t.rifl + t.pen(), n):
        t.subisci(d(1, 6))              # giù nel cortile, 4,5 m
        t.fuori = 2


def _attacco_pieno(c, st, t, pa: int):
    """Attacco completo con Attacco Poderoso −pa/+pa (a due mani: +2×pa? No:
    in 3.5 a due mani il danno è il doppio della penalità)."""
    occ = st.flag.get("occhio_ca", {}).get(t.nome, 0)
    occd = st.flag.get("occhio_danni", {}).get(t.nome, 0)
    for b, dn in c.attacchi:
        if t.giu():
            break
        if tira(b - pa, t.ca - occ):
            t.subisci(dn() + 2 * pa + occd)


def _occhio(st, t):
    st.flag.setdefault("occhio_ca", {})[t.nome] = 2
    st.flag.setdefault("occhio_danni", {})[t.nome] = 2
    st.flag["occhio_fino"] = st.flag.get("rnd", 0) + 5


def _giavellotti(c, st, g):
    volanti = [p for p in vivi(g) if p.vola]
    if not volanti or st.risorse.get("giav", 3) <= 0:
        return False
    st.risorse["giav"] = st.risorse.get("giav", 3) - 1
    t = volanti[0]
    if tira(19, t.ca):
        t.subisci(d(1, 8) + 13)
    return True


def politica_zogtar(variante: str, stretto: bool):
    """variante:
    canone      R1 Ira + Occhio su chi porta la Corona (Thorik) + un colpo;
                R2+ Colpo Terrificante su chi gli sta davanti; sotto il 30%
                attacco pieno −15/+30 (canone: «cerca di portarsi via qualcuno»).
    pieno       come canone, ma dal R2 attacco completo −5/+10 invece del Colpo.
    divide      Occhio su Tordek (non immune alla paura, CA 22 in ira); Colpo
                Terrificante su Thorik per toglierlo dalla linea, poi attacco
                completo −5/+10 su chi resta davanti.
    """
    def pol(c, st, g, rnd, sparsi, tattica):
        st.flag["rnd"] = rnd
        st.flag["stretto"] = stretto
        st.posizione = "terra"
        if rnd == 0:
            st.flag["presenza_gia"] = set()
            return
        if st.flag.get("occhio_fino", 0) < rnd:
            st.flag["occhio_ca"], st.flag["occhio_danni"] = {}, {}
        fronte = _davanti(g)
        if not fronte:
            # nessuno davanti: giavellotti su chi vola, poi avanza sul camminamento
            if not _giavellotti(c, st, g):
                bers = vivi(g)
                if bers:
                    _attacco_pieno(c, st, min(bers, key=lambda p: p.ca), 5)
            return
        _presenza(g, c.presenza_cd, st.flag["presenza_gia"])
        basso = st.pf < 0.3 * c.pf
        if rnd == 1:
            mark = g["Tordek"] if variante == "divide" else g["Thorik"]
            if mark.giu():
                mark = fronte[0]
            _occhio(st, mark)
            t = mark if mark in fronte else fronte[0]
            b, dn = c.attacchi[0]           # Occhio = movimento, resta un colpo
            if tira(b, t.ca - st.flag["occhio_ca"].get(t.nome, 0)):
                t.subisci(dn() + st.flag["occhio_danni"].get(t.nome, 0))
            return
        if basso:
            _attacco_pieno(c, st, min(fronte, key=lambda p: p.pf_ora), 15)
            return
        if variante == "canone":
            _colpo_terrificante(c, st, fronte[0], 0)
        elif variante == "pieno":
            marcati = [p for p in fronte if p.nome in st.flag.get("occhio_ca", {})]
            _attacco_pieno(c, st, (marcati or fronte)[0], 5)
        elif variante == "divide":
            th = g["Thorik"]
            if th in fronte and len(fronte) == 2:
                _colpo_terrificante(c, st, th, 0)
            else:
                t = g["Tordek"] if g["Tordek"] in fronte else fronte[0]
                _attacco_pieno(c, st, t, 5)
    return pol


TATTICHE_PG_BRECCIA = ["T1-classica"]
PF_PIENI = {n: p.pf for n, p in m.gruppo()[0].items()}



def tabella_costo(titolo, c, politiche, prove, buff):
    """Come m.tabella, più quello che lo scontro costa ai PG prima del drago."""
    print(f"\n### {titolo} · prove {prove} · buff {buff}\n")
    print("| Politica | Zog'tar ucciso | almeno un PG morto | PG morti (media) | round | "
          "pf dei PG alla fine (% del totale, vivi) | Thorik o Tordek giù dal camminamento (round) |")
    print("|---|---|---|---|---|---|---|")
    for np_, pol in politiche.items():
        es, pfp, fuori = [], 0.0, 0
        for _ in range(prove):
            e = m.combatti(c, pol, "T1-classica", buff)
            tot = sum(PF_PIENI.values())
            pfp += sum(max(v, 0) for v in e.pf_pg.values()) / tot
            fuori += e.terrore
            es.append(e)
        n = len(es)
        print(f"| {np_} | {100 * sum(e.finale == 'ucciso' for e in es) / n:.0f}% | "
              f"{100 * sum(e.pg_morti > 0 for e in es) / n:.0f}% | {sum(e.pg_morti for e in es) / n:.2f} | "
              f"{sum(e.round for e in es) / n:.1f} | {100 * pfp / n:.0f}% | {fuori / n:.1f} |")


@m.scontro("zogtar-costo")
def scontro_zogtar_costo(prove: int, buff: int):
    for stretto in (True, False):
        c = zogtar(264, stretto)
        pols = {v: politica_zogtar(v, stretto) for v in ("canone", "pieno", "divide")}
        tabella_costo(f"Che cosa costa la breccia ai PG · dopo il barile · "
                      f"{'si stringe' if stretto else 'senza stringersi'}", c, pols, prove, buff)


@m.scontro("zogtar-breccia")
def scontro_zogtar(prove: int, buff: int):
    for pf_alba, etichetta in ((283, "pf pieni (Scena 8 saltata, o curato)"),
                               (264, "dopo il barile e la notte: 249 + 15 di riposo (SRD)")):
        for stretto in (True, False):
            c = zogtar(pf_alba, stretto)
            pols = {v: politica_zogtar(v, stretto) for v in ("canone", "pieno", "divide")}
            m.tabella(f"Zog'tar sulla breccia · {etichetta} · "
                      f"{'si stringe (−4/−4)' if stretto else 'senza stringersi'}",
                      c, pols, TATTICHE_PG_BRECCIA, prove, buff)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prove", type=int, default=10000)
    ap.add_argument("--seme", type=int, default=1372)
    ap.add_argument("--buff", type=int, default=0)
    ap.add_argument("--scontro", default="tutti")
    a = ap.parse_args()
    m.R.seed(a.seme)
    for nome, f in m.SCONTRI.items():
        if a.scontro in ("tutti", nome):
            f(a.prove, a.buff)


if __name__ == "__main__":
    main()
