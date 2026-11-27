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



def tabella_costo(titolo, c, politiche, prove, buff, chi="Zog'tar", ultima="Thorik o Tordek giù dal camminamento (round)"):
    """Come m.tabella, più quello che lo scontro costa ai PG prima del drago."""
    print(f"\n### {titolo} · prove {prove} · buff {buff}\n")
    print(f"| Politica | {chi} ucciso | almeno un PG morto | PG morti (media) | round | "
          f"pf dei PG alla fine (% del totale, vivi) | {ultima} |")
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


# =========================================== ZALKATAR NEL SANCTUM (ARC-09, Torre)
# 09_.../Arco-Post-Hammerfist-P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md
# CA 24, 130 pf, 4 tentacoli +13 (1d4+1, afferrare), RI 25, RD 15/magia (le armi
# dei PG sono magiche: non conta), resistenza fuoco e elettricità 20.
# Esplosione mentale: cono 18 m, Volontà CD 24 o 5d6 e stordito 1 round + confuso
# 1d4 (STIMA: i danni solo su chi fallisce; confuso = perde 3 round su 4).
# Thorik: mente sigillata dalla Corona, immune (nel motore immune_paura).
# Ozyrrandion NON è nel modello (EL 16 col drago): la misura è su Zalkatar da solo.
# STIMA comune alle due politiche: i PG salgono sulla piattaforma al round 3
# (tentacoli neri sulle rampe); prima lo colpiscono solo a distanza.
SALITA = 3


def zalkatar() -> Creatura:
    tent = lambda: d(1, 4) + 1  # noqa: E731
    return Creatura("Zalkatar", pf=130, ca=24, contatto=18, ri=25, temp=12, rifl=12, vol=17,
                    attacchi=[(13, tent)] * 4, soffio_dadi=(0, 1), soffio_cd=0,
                    soffio_forma="cono", presenza_cd=0, immune=("fuoco",), soglia_fuga=13)


def _esplosione(g, sparsi, esclusi=("Thorik",)):
    vivi = [p for p in g.values() if not p.giu() and p.fuori == 0 and p.nome not in esclusi]
    k = R.choice((1, 2) if sparsi else (2, 3, 3))
    for p in R.sample(vivi, min(k, len(vivi))):
        if not ts(p.vol + p.pen(), 24):
            p.subisci(d(5, 6))
            p.fuori = 1 + (d(1, 4) * 3) // 4


def politica_zalkatar(variante: str):
    """oggi    le tre fasi della scheda: sopra il 50% esplosione mentale dalla
               piattaforma; sotto il 50% scende in mischia ed estrae il cervello al
               più debole; sotto il 10% fugge (soglia nel motore).
    schema     sa che la Corona chiude la mente di Thorik e non lo mette nel cono
               (anche «oggi» non lo colpisce: è immune; la differenza è che sceglie
               il cono sui tre che può colpire); non scende mai in mischia: con due
               combattenti addosso usa *porta dimensionale* (3/giorno) e torna in
               alto per un round; estrae il cervello solo a chi è già fuori gioco.
    """
    def pol(c, st, g, rnd, sparsi, tattica):
        if rnd == 0:
            st.posizione = "alto"
            st.risorse["porta"] = 3
            st.flag["presa"] = None
            return
        presa = st.flag.get("presa")
        st.flag["presa"] = None
        if presa and not presa[0].giu():
            t, indifeso = presa
            # estrazione automatica (scheda) se la vittima non si è liberata;
            # STIMA: chi era stordito non si libera, Thorik e Tordek (lotta ~+18
            # contro +10) si liberano 7 volte su 10, gli altri 4,5 su 10
            libera = 0 if indifeso else (0.7 if t.nome in ("Thorik", "Tordek") else 0.45)
            if R.random() >= libera:
                t.morto = True
                return
        if st.posizione == "alto" and rnd >= SALITA and st.flag.get("via_fino", 0) < rnd:
            st.posizione = "terra"
        if variante == "oggi":
            if st.pf >= 0.5 * c.pf:
                _esplosione(g, sparsi)
            else:
                st.posizione = "terra"
                bers = [p for p in vivi(g)]
                if bers:
                    t = min(bers, key=lambda p: p.pf_ora)
                    colpi = sum(tira(13, t.ca) for _ in range(4))
                    for _ in range(colpi):
                        t.subisci(d(1, 4) + 1)
                    if colpi == 4:
                        st.flag["presa"] = (t, t.fuori > 0)
            return
        # schema
        addosso = st.posizione == "terra" and len(_davanti(g)) >= 2
        if addosso and st.risorse["porta"] > 0:
            st.risorse["porta"] -= 1
            st.posizione = "alto"
            st.flag["via_fino"] = rnd + 1
        fuori = [p for p in g.values() if not p.giu() and p.fuori > 0 and p.nome != "Thorik"]
        if fuori and st.posizione == "terra" and R.random() < 0.5:
            t = fuori[0]
            if sum(tira(13 + 4, t.ca - 4) for _ in range(4)) == 4:   # stordito/indifeso: STIMA +4/−4
                st.flag["presa"] = (t, True)
            return
        _esplosione(g, sparsi)
    return pol


@m.scontro("zalkatar-sanctum")
def scontro_zalkatar(prove: int, buff: int):
    c = zalkatar()
    pols = {v: politica_zalkatar(v) for v in ("oggi", "schema")}
    tabella_costo("Zalkatar nel sanctum, senza Ozyrrandion", c, pols, prove, buff,
                  chi="Zalkatar", ultima="round-PG persi (storditi, confusi)")



# ===================================== XILTHRA NELLA SALA DELLA CORTE (ARC-09, P3)
# Bestiario/villain/xilthra-velssin-cr13.md (scheda legale del 15/11) contro
# l'abbozzo di main (STATBLOCCHI §4 e Upscale: «pf ~90-100, CA 24-26», nessuna
# tattica: il DM gioca gli incantesimi della lista dal trono).
# STIME comuni: CD 15 + livello in tutte e due (l'abbozzo non la dava); la scorta
# (due guerrieri drow 9, arcieri sulle terrazze) NON è nel modello, in nessuna
# delle due; Thorik è immune a comando e blocca persone (Volontà Adamantina
# della Corona: immune a charme e compulsioni). Gli altri tre sono umanoidi.
# *Comando superiore* e *blocca persone*: un TS nuovo ogni round, quindi chi
# fallisce perde 1 round più uno per ogni TS fallito di fila.
def xilthra(versione: str) -> Creatura:
    mazza = lambda: d(1, 8) + 2  # noqa: E731
    if versione == "abbozzo":
        return Creatura("Xilthra", pf=95, ca=25, contatto=13, ri=22, temp=10, rifl=7, vol=14,
                        attacchi=[(10, mazza), (5, mazza)], soffio_dadi=(0, 1), soffio_cd=0,
                        soffio_forma="cono", presenza_cd=0, soglia_fuga=-10_000)
    return Creatura("Xilthra", pf=69, ca=30, contatto=17, ri=23, temp=9, rifl=6, vol=15,
                    attacchi=[(11, mazza), (6, mazza)], soffio_dadi=(0, 1), soffio_cd=0,
                    soffio_forma="cono", presenza_cd=0, soglia_fuga=20)


def _compulsione(t, cd):
    """Comando superiore o blocca persone su t: round persi."""
    if t.nome == "Thorik" or t.giu() or t.fuori > 0:
        return
    k = 0
    while k < 12 and not ts(t.vol + t.pen(), cd):
        k += 1
    if k:
        t.fuori = max(t.fuori, k)


def politica_xilthra(variante: str):
    """abbozzo  main: dal trono, a terra; round 1 *influenza sacrilega* (5d8,
                Volontà CD 19 dimezza), poi *blocca persone* (CD 17) su un
                combattente, *comando superiore* (CD 20) su tutti, *scagliare
                maledizione* (CD 18: −4, qui come scosso per 12 round); nessuna fuga.
    schema    la tattica scritta il 15/11: sul balcone; round 1 *barriera di lame*
              (12d6, Riflessi CD 21 dimezza) che i due nani attraversano al round 2
              per arrivarle addosso, e *comando* rapido (CD 16) su Tordek; poi
              *comando superiore* e *blocca persone*; con due combattenti addosso
              *fuorviare* (invisibilità superiore 12 round) e torna lontana; sotto
              20 pf fugge col Patto (soglia nel motore).
    """
    def pol(c, st, g, rnd, sparsi, tattica):
        if rnd == 0:
            st.posizione = "terra" if variante == "abbozzo" else "alto"
            st.risorse.update(blocca=2, comando_sup=1, maled=2, fuorv=1, influenza=1)
            if variante == "schema":
                st.ca_bonus = 0          # scudo della fede già nella CA 30
            return
        vivi_ = [p for p in g.values() if not p.giu() and p.fuori == 0]
        if not vivi_:
            return
        combattenti = [p for p in vivi_ if p.nome in ("Thorik", "Tordek")]
        if variante == "abbozzo":
            if st.risorse["influenza"]:
                st.risorse["influenza"] -= 1
                for p in vivi_:
                    n = d(5, 8)
                    p.subisci(n // 2 if ts(p.vol + p.pen(), 19) else n)
            elif st.risorse["blocca"] and combattenti:
                st.risorse["blocca"] -= 1
                _compulsione(R.choice(combattenti), 17)
            elif st.risorse["comando_sup"]:
                st.risorse["comando_sup"] -= 1
                for p in vivi_:
                    _compulsione(p, 20)
            elif st.risorse["maled"]:
                st.risorse["maled"] -= 1
                t = R.choice(vivi_)
                if not ts(t.vol + t.pen(), 18):
                    t.scosso = 12
            else:
                t = min(vivi_, key=lambda p: p.pf_ora)
                for b, dn in c.attacchi:
                    if tira(b, t.ca):
                        t.subisci(dn())
            return
        # schema
        if rnd == 1:                     # schema e schema+influenza
            st.flag["barriera"] = True
            t = g.get("Tordek")
            if t in vivi_ and not ts(t.vol + t.pen(), 16):
                t.fuori = max(t.fuori, 1)        # *comando*: dura 1 round
            return
        if rnd == 2 and st.flag.get("barriera"):
            for p in combattenti:
                n = d(12, 6)
                p.subisci(n // 2 if ts(p.rifl + p.pen(), 21) else n)
            st.posizione = "terra"
        addosso = st.posizione == "terra" and len([p for p in combattenti if not p.giu() and p.fuori == 0]) >= 2
        if addosso and st.risorse["fuorv"]:
            st.risorse["fuorv"] -= 1
            st.inv_sup = 12
            st.posizione = "alto"
            st.flag["torna"] = rnd + 2
            return
        if st.posizione == "alto" and st.flag.get("torna", 99) <= rnd:
            st.posizione = "terra"
        if variante == "schema+influenza" and st.risorse["influenza"]:
            st.risorse["influenza"] -= 1
            for p in vivi_:
                n = d(5, 8)
                p.subisci(n // 2 if ts(p.vol + p.pen(), 19) else n)
        elif st.risorse["comando_sup"]:
            st.risorse["comando_sup"] -= 1
            for p in vivi_:
                _compulsione(p, 20)
        elif st.risorse["blocca"] and combattenti:
            st.risorse["blocca"] -= 1
            _compulsione(R.choice(combattenti), 17)
        elif st.risorse["maled"]:
            st.risorse["maled"] -= 1
            t = R.choice(vivi_)
            if not ts(t.vol + t.pen(), 18):
                t.scosso = 12
        else:
            t = min(vivi_, key=lambda p: p.pf_ora)
            for b, dn in c.attacchi:
                if tira(b, t.ca):
                    t.subisci(dn())
    return pol


@m.scontro("xilthra-corte")
def scontro_xilthra(prove: int, buff: int):
    for v in ("abbozzo", "schema", "schema+influenza"):
        tabella_costo(f"Xilthra nella Sala della Corte, senza scorta · {v}",
                      xilthra("abbozzo" if v == "abbozzo" else "legale"),
                      {v: politica_xilthra(v)}, prove, buff, chi="Xilthra",
                      ultima="round-PG persi (comandati, bloccati)")



# ============================================ ZARIM AL TORNEO (ARC-09, Giorno 3)
# Bestiario/villain/Zarim/zarim-illithid-luogotenente-cr12.md: CA 23, 73 pf, RI 25,
# 4 tentacoli +10 (1d4+1), esplosione mentale a volontà (cono 18 m, Volontà CD 19
# o stordito 3d4 round), charme sui mostri CD 17, Archivio delle Anime (1/scontro,
# cura 3d8+8 quando un nemico cade), morale sotto 25 pf.
# STIME: in levitazione fino al round 3 (lo colpiscono solo a distanza); il PG
# ammaliato perde lo scontro (nel modello non attacca i compagni); estrarre il
# cervello come per Zalkatar: chi è stordito non si libera, Tempra CD 19 il round
# dopo. Thorik immune all'esplosione e al charme (Corona). Senza le ondate.
def zarim() -> Creatura:
    tent = lambda: d(1, 4) + 1  # noqa: E731
    return Creatura("Zarim", pf=73, ca=23, contatto=12, ri=25, temp=9, rifl=7, vol=15,
                    attacchi=[(10, tent)] * 4, soffio_dadi=(0, 1), soffio_cd=0,
                    soffio_forma="cono", presenza_cd=0, soglia_fuga=25)


def politica_zarim(variante: str):
    """oggi         la tattica della scheda: round 1 esplosione, round 2 charme sul
                    combattente più pericoloso non protetto (Tordek), dal round 3
                    scende sugli storditi ed estrae il cervello, Tordek compreso.
    tordek_vivo  la stessa, ma Tordek non si tocca: Xal'thor lo vuole vivo per il
                 portale (canone del 15/11, Bestiario Xal_thor.md §L'obiettivo
                 reale); su Tordek stordito niente tentacoli, e il charme va su
                 Hella."""
    def pol(c, st, g, rnd, sparsi, tattica):
        if rnd == 0:
            st.posizione = "alto"
            st.flag.update(presa=None, archivio=True, giu_prima=0)
            return
        giu = sum(1 for p in g.values() if p.giu())
        if giu > st.flag["giu_prima"] and st.flag["archivio"]:
            st.flag["archivio"] = False
            st.pf = min(c.pf, st.pf + d(3, 8) + 8)
        st.flag["giu_prima"] = giu
        presa = st.flag.get("presa")
        st.flag["presa"] = None
        if presa and not presa.giu():
            if not ts(presa.temp, 19):
                presa.morto = True
                return
        protetti = {"Thorik"} | ({"Tordek"} if variante == "tordek_vivo" else set())
        if rnd == 2:
            bers = [p for p in vivi(g) if p.nome != "Thorik"]
            scelto = "Hella" if variante == "tordek_vivo" else "Tordek"
            t = g.get(scelto)
            if t in bers and not ts(t.vol + t.pen(), 17):
                t.charmato = True
            return
        if rnd >= 3:
            st.posizione = "terra"
            storditi = [p for p in g.values() if not p.giu() and p.fuori > 0 and p.nome not in protetti]
            if storditi:
                t = storditi[0]
                if sum(tira(14, t.ca - 4) for _ in range(4)) == 4:
                    st.flag["presa"] = t
                return
        for p in [q for q in g.values() if not q.giu() and q.fuori == 0 and q.nome != "Thorik"
                  and not q.charmato]:
            if R.random() < (0.5 if sparsi else 0.8):          # chi sta nel cono
                if not ts(p.vol + p.pen(), 19):
                    p.fuori = d(3, 4)
    return pol


@m.scontro("zarim-torneo")
def scontro_zarim(prove: int, buff: int):
    c = zarim()
    pols = {v: politica_zarim(v) for v in ("oggi", "tordek_vivo")}
    tabella_costo("Zarim al Torneo, Giorno 3, senza le ondate", c, pols, prove, buff,
                  chi="Zarim", ultima="round-PG persi (storditi, ammaliati)")


# ============================================== AZARR KUL A RETHMAR (ARC-09, Fase 3)
# Bestiario/villain/Azarr_Kul/azarr-kul-final-cr17.md: pre-buff completo (taglia
# Grande) CA 36, pf 186, spadone +28/+23/+18/+13 (3d6+19, +2d6 sacrilego contro i
# buoni), RD 6/bene, Temp +20 Rifl +8 Vol +17; soffio in linea 6d8 CD 23 con
# ricarica 1d4 (canone del DM); ferire LI 14 (140 pf, Volontà CD 22 dimezza, mai
# sotto 1 pf); blocca persone CD 18 (Thorik immune: mente vuota della Corona);
# contingenza: guarigione sotto 40 pf (una volta), parola del ritorno sotto 15.
# Senza l'Avatar, le erinni e i luogotenenti (STIMA dichiarata).
# STIMA: CA di contatto dei PG 11 (Thorik, Tordek), 18 (Artemis), 12 (Hella);
# i PG sono buoni (+2d6 dello spadone); Aegis Fang non supera la RD 6/bene.
CONTATTO = {"Thorik": 11, "Tordek": 11, "Artemis": 18, "Hella": 12}


def azarr_kul() -> Creatura:
    sp = lambda: d(3, 6) + 19 + d(2, 6)  # noqa: E731
    return Creatura("Azarr Kul", pf=186, ca=36, contatto=14, ri=0, temp=20, rifl=8, vol=17,
                    attacchi=[(28, sp), (23, sp), (18, sp), (13, sp)],
                    soffio_dadi=(6, 8), soffio_cd=23, soffio_forma="linea", presenza_cd=0,
                    immune=("elettricita",), soglia_fuga=15, rd=6)


def _spadone(t, poderoso):
    k, extra = (4, 8) if poderoso else (0, 0)
    for b in (28, 23, 18, 13):
        if t.giu():
            return
        if tira(b - k, t.ca):
            t.subisci(d(3, 6) + 19 + d(2, 6) + extra)


def _ferire(t):
    if not tira(25, CONTATTO[t.nome]):
        return
    n = 140 if not ts(t.vol + t.pen(), 22) else 70
    t.pf_ora = max(min(t.pf_ora, d(1, 4)), t.pf_ora - n) if t.pf_ora > 0 else t.pf_ora


def politica_azarr(variante: str):
    """oggi    la tattica della scheda: round 1 soffio sul gruppo; round 2 carica il
               guaritore (Hella) e attacco completo, Attacco Poderoso a −4 se la CA
               è bassa (sotto 30); dal round 3 *ferire* sul più corazzato (Thorik),
               *blocca persone* su chi non è immune (Tordek), poi attacco completo
               sul più debole; soffio ogni volta che è carico.
    schema     sa che Thorik regge la linea e ha la mente chiusa, e che Hella cura:
               round 1 *ferire* su Thorik (lo lascia a 1d4 pf), round 2 attacco
               completo su Thorik per finirlo; poi *blocca persone* su Tordek e
               attacco completo su chi è tenuto o più debole; soffio quando è carico
               e ci sono almeno due PG in piedi. Incantare in Combattimento (scheda)
               gli lascia lanciare in mischia.
    guaritore  come oggi, ma il round 2 è *ferire* su Hella e il round 3 l'attacco
               completo su di lei: toglie la cura prima di tutto il resto.
    """
    def pol(c, st, g, rnd, sparsi, tattica):
        if rnd == 0:
            st.posizione = "terra"
            st.flag.update(guarigione=True)
            return
        if st.pf < 40 and st.flag["guarigione"]:
            st.flag["guarigione"] = False
            st.pf = min(c.pf, st.pf + 140)
        bersagli = vivi(g)
        if not bersagli:
            return
        tenuti = [p for p in g.values() if not p.giu() and getattr(p, "tenuto", False)]
        for p in tenuti:
            if ts(p.vol, 18):
                p.tenuto = False
                p.fuori = 0
        pronto = rnd >= st.soffio_pronto
        if variante in ("oggi", "guaritore"):
            if rnd == 1:
                m.soffio(c, st, g, rnd, sparsi)
                return
            if rnd == 2 and variante == "guaritore" and not g["Hella"].giu():
                _ferire(g["Hella"])
                return
            if rnd == 2 or (rnd == 3 and variante == "guaritore"):
                t = g["Hella"] if not g["Hella"].giu() else min(bersagli, key=lambda p: p.ca)
                _spadone(t, t.ca < 30)
                return
            if pronto:
                m.soffio(c, st, g, rnd, sparsi)
                return
            if rnd == 3 and not g["Thorik"].giu():
                _ferire(g["Thorik"])
                return
            tordek = g["Tordek"]
            if rnd == 4 and not tordek.giu() and not getattr(tordek, "tenuto", False):
                if not ts(tordek.vol + tordek.pen(), 18):
                    tordek.tenuto, tordek.fuori = True, 14
                return
        else:
            thorik = g["Thorik"]
            if rnd == 1 and not thorik.giu():
                _ferire(thorik)
                return
            if rnd == 2 and not thorik.giu():
                _spadone(thorik, False)
                return
            if pronto and len(bersagli) >= 2 and rnd >= 3:
                m.soffio(c, st, g, rnd, sparsi)
                return
            tordek = g["Tordek"]
            if not tordek.giu() and not getattr(tordek, "tenuto", False) and not st.flag.get("blocca"):
                st.flag["blocca"] = True
                if not ts(tordek.vol + tordek.pen(), 18):
                    tordek.tenuto, tordek.fuori = True, 14
                return
        tenuti = [p for p in g.values() if not p.giu() and getattr(p, "tenuto", False)]
        if tenuti:                    # colpo di grazia sul paralizzato (SRD)
            t = tenuti[0]
            n = 2 * (d(3, 6) + 19) + d(2, 6)
            t.subisci(n)
            if not t.giu() and not ts(t.temp, 10 + n):
                t.morto = True
            return
        bersagli = vivi(g)
        if bersagli:
            t = min(bersagli, key=lambda p: p.pf_ora)
            _spadone(t, t.ca < 30)
    return pol


@m.scontro("azarr-kul-rethmar")
def scontro_azarr(prove: int, buff: int):
    c = azarr_kul()
    pols = {v: politica_azarr(v) for v in ("oggi", "guaritore", "schema")}
    tabella_costo("Azarr Kul a Rethmar, Fase 3, pre-buff completo, senza Avatar né erinni",
                  c, pols, prove, buff, chi="Azarr Kul",
                  ultima="round-PG persi (tenuti, fuori)")


# ============================================ USHGAR «OCCHIO RESO» (ARC-09, innesti)
# Bestiario/villain/Ushgar_Occhio_Reso/ushgar-occhio-reso-cr13.md, in ira:
# pf 179, CA 19, ascia +23/+18/+13 (1d12+14, ×3), Attacco Poderoso a −5 (+10 a due
# mani), RD 3/—, Temp +17 Rifl +8 Vol +11; carica di 30 m al round 1; due pozioni di
# *cura ferite critiche* sotto ~40 pf; non fugge. Da solo, senza chierico né bruto.
# STIMA: Artemis in volo non si raggiunge in mischia la metà dei round; i critici
# (×3) non sono nel modello.
def ushgar() -> Creatura:
    return Creatura("Ushgar", pf=179, ca=19, contatto=12, ri=0, temp=17, rifl=8, vol=11,
                    attacchi=[(23, lambda: d(1, 12) + 14)], soffio_dadi=(0, 1), soffio_cd=0,
                    soffio_forma="linea", presenza_cd=0, soglia_fuga=-10_000, rd=3)


def politica_ushgar(variante: str):
    """oggi       la scheda: punta l'incantatore e non cambia bersaglio, Attacco
                  Poderoso a −5 sempre; l'incantatore è Hella (Artemis vola).
    artemis    come oggi, ma l'incantatore che punta è Artemis: in volo la metà dei
                  round non la raggiunge e perde il round.
    misurato   punta Hella, ma usa l'Attacco Poderoso solo contro CA 22 o meno; caduto
                  il bersaglio passa al PG a terra con meno pf.
    """
    def pol(c, st, g, rnd, sparsi, tattica):
        if rnd == 0:
            st.posizione = "terra"
            st.risorse["pozioni"] = 2
            st.flag["bersaglio"] = "Artemis" if variante == "artemis" else "Hella"
            return
        if st.pf < 40 and st.risorse["pozioni"] > 0:
            st.risorse["pozioni"] -= 1
            st.pf = min(c.pf, st.pf + d(4, 8) + 13)
            return
        t = g.get(st.flag["bersaglio"])
        if t is None or t.giu():
            a_terra = [p for p in vivi(g) if p.nome != "Artemis"] or vivi(g)
            if not a_terra:
                return
            t = min(a_terra, key=lambda p: p.pf_ora)
            st.flag["bersaglio"] = t.nome
        if t.nome == "Artemis" and R.random() < 0.5:
            return
        poderoso = variante != "misurato" or t.ca <= 22
        k, extra = (5, 10) if poderoso else (0, 0)
        serie = (23,) if rnd == 1 else (23, 18, 13)      # round 1: carica, un colpo (+2)
        for b in serie:
            if t.giu():
                break
            if tira(b - k + (2 if rnd == 1 else 0), t.ca):
                t.subisci(d(1, 12) + 14 + extra)
    return pol


@m.scontro("ushgar-carica")
def scontro_ushgar(prove: int, buff: int):
    c = ushgar()
    pols = {v: politica_ushgar(v) for v in ("oggi", "artemis", "misurato")}
    tabella_costo("Ushgar da solo, in ira, carica al round 1", c, pols, prove, buff,
                  chi="Ushgar", ultima="round-PG persi")


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
