"""Profili e politiche dei draghi per simula_scontri.py (15/11/2026).

Ogni scontro ha la tattica del CANONE di oggi, scritta come la scheda la
descrive, e la NUOVA proposta nel thread. Le capacità usate sono solo quelle
della scheda citata. Dove la scheda tace, il commento dice STIMA.
"""
from __future__ import annotations

import simula_scontri as m
from simula_scontri import Creatura, d, ts, tira, R  # noqa: F401

TATTICHE_PG = ["T1-classica", "T1-sparsi", "T2-tutti-in-volo", "T3-preparati-sparsi"]


def vivi(g, esclusi=()):
    return [p for p in g.values() if not p.giu() and p.nome not in esclusi and p.fuori == 0]


def nube_maleodorante(g, cd, sparsi):
    """Nube maleodorante (SRD): nauseati mentre sono dentro e 1d4+1 round dopo.
    Sui PG raggruppati a terra ne prende 2-3, sparsi 1. Tempra CD della scheda."""
    terra = [p for p in vivi(g) if not p.vola]
    if not terra:
        return
    k = R.choice((1, 1, 2)) if sparsi else R.choice((2, 2, 3))
    for p in R.sample(terra, min(k, len(terra))):
        if not ts(p.temp, cd):
            p.nauseato = 1 + d(1, 4) + 1


# ======================================================== FAUCI DI PALUDE
# 08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md §1
FAUCI = Creatura(
    "Fauci di Palude", pf=337, ca=29, contatto=8, ri=21, temp=21, rifl=16, vol=19,
    attacchi=[(34, lambda: d(2, 8) + 10), (31, lambda: d(2, 6) + 5), (31, lambda: d(2, 6) + 5),
              (31, lambda: d(1, 8) + 5), (31, lambda: d(1, 8) + 5), (31, lambda: d(2, 6) + 15)],
    soffio_dadi=(14, 4), soffio_cd=29, soffio_forma="linea", presenza_cd=25, li=7,
    immune=("acido",), soglia_fuga=50, soffio_tipo="acido")
ODIO = 4          # Odio della stirpe contro Thorik
LOTTA_FAUCI = 31  # +27 con la sola bocca, più l'Odio
LOTTA_THORIK = 18


def _presa_di_thorik(c, st, g, rnd, sparsi, nuova: bool):
    """La presa del canone (DM 2026-10-19/20): morso in picchiata, presa, salita,
    soffio con Thorik in bocca, caduta. Fase in st.flag['presa']."""
    th = g["Thorik"]
    fase = st.flag.get("presa", 0)
    if fase == 0:
        if th.giu():
            st.flag["presa"] = 9
            return False
        st.posizione = "passata"
        if m.morso(c, st, th, odio=ODIO):
            if R.randint(1, 20) + LOTTA_FAUCI >= R.randint(1, 20) + LOTTA_THORIK:
                st.flag["presa"] = 1
                th.fuori = 3
                return True
        st.flag["presa"] = 9          # una volta per incontro
        return True
    if fase == 1:                     # la salita: una prova di lotta che morde
        st.posizione = "alto"
        if R.random() < 0.18:         # Thorik si libera: cade dalla quota di ora (~20 m)
            th.subisci(d(6, 6))
            th.fuori = 0
            st.flag["presa"] = 9
            return True
        th.subisci(d(2, 8) + 10 + ODIO)
        st.flag["presa"] = 2
        return True
    if fase == 2:                     # il soffio con lui in bocca, poi lo lascia
        st.posizione = "alto"
        th.subisci(max(0, d(14, 4) - th.resist))   # in bocca non ha il TS
        m.soffio(c, st, g, rnd, sparsi, esclusi=("Thorik",))
        th.subisci(d(11, 6))          # caduta da 30-35 m
        th.fuori = 1
        st.flag["presa"] = 3
        return True
    return False


def fauci_canone(c, st, g, rnd, sparsi, tattica):
    if rnd == 0:
        st.ca_bonus = 8               # armatura magica e scudo
        st.risorse["nube"] = 3
        return
    if rnd == 1:
        m.presenza(c, g)
    if st.flag.get("ascia_ha_cantato") and st.flag.get("presa", 0) < 3:
        if _presa_di_thorik(c, st, g, rnd, sparsi, False):
            return
    if st.flag.get("presa") == 3:
        # atterra a finire Thorik, poi il duello
        st.posizione = "terra"
        t = g["Thorik"] if not g["Thorik"].giu() else max(vivi(g) or [g["Thorik"]], key=lambda p: p.danni_fatti)
        if not t.giu():
            m.attacco_completo(c, st, t, odio=ODIO if t.nome == "Thorik" else 0)
        return
    if st.pf < 100:                   # atterra solo se gravemente ferito
        st.posizione = "terra"
        t = max(vivi(g) or list(g.values()), key=lambda p: p.danni_fatti)
        m.attacco_completo(c, st, t, odio=ODIO if t.nome == "Thorik" else 0)
        return
    st.posizione = "alto"
    if rnd >= st.soffio_pronto:
        m.soffio(c, st, g, rnd, sparsi)
    elif st.risorse["nube"] > 0:
        st.risorse["nube"] -= 1
        nube_maleodorante(g, 16, sparsi)


def fauci_nuova(c, st, g, rnd, sparsi, tattica):
    """Le differenze dal canone, tutte con incantesimi della scheda:
    1. immagine speculare prima di farsi vedere, e di nuovo prima della picchiata;
    2. dissolvi magie su chi vola e può prendere Thorik al volo (solo se lo vede);
    3. nube maleodorante sui nani prima di atterrare per il duello;
    4. il soffio cerca la guaritrice;
    5. fugge a un terzo dei pf (112) invece che a 50."""
    if rnd == 0:
        st.ca_bonus = 8
        st.risorse.update(nube=3, specchio=2, dissolvi=2)
        st.immagini = d(1, 4) + 2
        st.risorse["specchio"] -= 1
        return
    if rnd == 1:
        m.presenza(c, g)
    presa = st.flag.get("presa", 0)
    if st.flag.get("ascia_ha_cantato") and presa == 0:
        volanti = [p for p in vivi(g) if p.vola and p.nome in ("Hella", "Tordek")]
        if volanti and st.risorse["dissolvi"] > 0:
            st.risorse["dissolvi"] -= 1
            st.posizione = "alto"
            for p in volanti:
                if R.randint(1, 20) + 7 >= 16:     # pozione di volare, LI 5°: CD 16
                    p.vola = False
            return
        if st.immagini == 0 and st.risorse["specchio"] > 0:
            st.risorse["specchio"] -= 1
            st.immagini = d(1, 4) + 2
            st.posizione = "alto"
            return
    if st.flag.get("ascia_ha_cantato") and presa < 3:
        if _presa_di_thorik(c, st, g, rnd, sparsi, True):
            return
    if presa == 3 and not st.flag.get("nube_prima"):
        st.flag["nube_prima"] = True
        if st.risorse["nube"] > 0:
            st.risorse["nube"] -= 1
            nube_maleodorante(g, 16, sparsi)
            st.posizione = "alto"
            return
    if presa == 3:
        st.posizione = "terra"
        t = g["Thorik"] if not g["Thorik"].giu() else min(vivi(g) or [g["Thorik"]], key=lambda p: p.pf_ora)
        if not t.giu():
            m.attacco_completo(c, st, t, odio=ODIO if t.nome == "Thorik" else 0)
        return
    st.posizione = "alto"
    if rnd >= st.soffio_pronto:
        m.soffio(c, st, g, rnd, sparsi)
    elif st.risorse["nube"] > 1:
        st.risorse["nube"] -= 1
        nube_maleodorante(g, 16, sparsi)


@m.scontro("fauci")
def _fauci(prove, buff):
    m.tabella("Fauci di Palude, canone (fuga a 50 pf)", FAUCI, {"canone": fauci_canone},
              TATTICHE_PG, prove, buff)
    from dataclasses import replace
    m.tabella("Fauci di Palude, nuova (fuga a 112 pf)", replace(FAUCI, soglia_fuga=112),
              {"nuova": fauci_nuova}, TATTICHE_PG, prove, buff)
    m.tabella("Fauci di Palude, nuova ma fuga a 50 pf (per isolare la soglia)", FAUCI,
              {"nuova-50": fauci_nuova}, TATTICHE_PG, prove, buff)


# ============================================== TYRGARUN, FASE 4 (a terra)
# Bestiario/villain/Tyrgarun/tyrgarun-blue-very-old-cr19.md: Mythal −2 a tiri e TS
TYR = Creatura(
    "Tyrgarun (Fase 4)", pf=405, ca=37, contatto=8, ri=25, temp=22, rifl=17, vol=21,
    attacchi=[(37, lambda: d(2, 8) + 11), (35, lambda: d(2, 6) + 5), (35, lambda: d(2, 6) + 5),
              (35, lambda: d(1, 8) + 5), (35, lambda: d(1, 8) + 5), (35, lambda: d(2, 6) + 16)],
    soffio_dadi=(20, 8), soffio_cd=30, soffio_forma="linea", presenza_cd=29, li=11,
    immune=("elettricità",), soglia_fuga=0, soffio_tipo="elettricità")   # col Mythal attivo non fugge
FOCUS = "Artemis"   # STIMA: il PG che tiene il cerchio del Mythal; se cade, Tyrgarun rivola


def _contro_focus(c, st, g, schermo: float):
    f = g[FOCUS]
    if not f.giu() and R.random() > schermo:
        m.attacco_completo(c, st, f)
    else:
        bl = vivi(g, esclusi=(FOCUS,)) or vivi(g)
        if bl:
            m.attacco_completo(c, st, R.choice(bl))
    if f.giu():
        st.flag["obiettivo"] = True


def tyr_canone(c, st, g, rnd, sparsi, tattica):
    """Scheda: «costretto alla mischia, usa stritolamento, coda e morso; cerca di
    sfondare verso il cerchio del Mythal». Nessun incantesimo nella tattica."""
    if rnd == 0:
        st.posizione = "terra"
        return
    if rnd == 1:
        m.presenza(c, g)
        m.soffio(c, st, g, rnd, sparsi)
        return
    _contro_focus(c, st, g, schermo=0.5)     # i nani gli sbarrano la strada metà delle volte


def tyr_nuova(c, st, g, rnd, sparsi, tattica):
    """Stregone di 11° che sa del Mythal (vedi la proposta):
    - pelle di pietra lanciata all'alba (110 min, dura tutta la battaglia: 110 pf di RD 10);
    - immagine speculare quando il cerchio comincia a chiudersi (11 min);
    - round 1 velocità, round 2 scava sotto la mischia (scavare 6 m: il Mythal nega il
      volo, non lo scavare), round 3 esce sotto il cerchio: niente schermo;
    - soffio in linea sul focus e su chi gli sta dietro appena è pronto."""
    if rnd == 0:
        st.posizione = "terra"
        st.pelle = 110
        st.immagini = d(1, 4) + 3
        return
    if rnd == 1:
        m.presenza(c, g)
        st.velocita = 11
        st.soffio_pronto = 1
        st.posizione = "terra"
        m.soffio(c, st, g, rnd, sparsi)    # rapidità: velocità come azione veloce? no: STIMA, vedi nota
        return
    if rnd == 2:
        st.posizione = "sotto"
        return
    st.posizione = "terra"
    if rnd >= st.soffio_pronto and not g[FOCUS].giu():
        f = g[FOCUS]
        n = d(20, 8)
        if ts(f.rifl + f.pen(), c.soffio_cd):
            n //= 2
        f.subisci(n)
        altri = vivi(g, esclusi=(FOCUS,))
        if altri:
            p = R.choice(altri)
            n = d(20, 8)
            if ts(p.rifl + p.pen(), c.soffio_cd):
                n //= 2
            p.subisci(n)
        st.soffio_pronto = rnd + R.randint(1, 4)
        if f.giu():
            st.flag["obiettivo"] = True
        return
    _contro_focus(c, st, g, schermo=0.5 if rnd > 4 else 0.0)


@m.scontro("tyrgarun")
def _tyr(prove, buff):
    pol = {"canone": tyr_canone, "nuova": tyr_nuova}
    tt = ["T1-classica", "T1-sparsi", "T3-preparati-sparsi"]
    m.tabella("Tyrgarun inchiodato dal Mythal (Fase 4), intatto e senza alleati", TYR, pol, tt, prove, buff,
              max_round=25)
    m.tabella("Tyrgarun inchiodato, già ferito (250 pf) e con alleati (statue: 40 a round, metà dei suoi round)",
              TYR, pol, tt, prove, buff, max_round=25, pf_iniziali=250, alleati=(40, 0.5))


# ================================================ ARBITRAX / ABITHRIAX
# Bestiario/villain/arbitrax-drago-rosso-cr15.md
ARB = Creatura(
    "Arbitrax", pf=237, ca=32, contatto=8, ri=19, temp=17, rifl=11, vol=13,
    attacchi=[(27, lambda: d(2, 8) + 10), (22, lambda: d(2, 6) + 5), (22, lambda: d(2, 6) + 5),
              (22, lambda: d(1, 8) + 5), (22, lambda: d(1, 8) + 5), (22, lambda: d(2, 6) + 15)],
    soffio_dadi=(10, 10), soffio_cd=25, soffio_forma="cono", presenza_cd=24, li=5,
    immune=("fuoco",), vulnerabile=("freddo",), soglia_fuga=80, soffio_tipo="fuoco")


def _colpo_terrificante(c, st, g, t):
    """Awesome Blow (SRD): azione standard, un attacco; se colpisce, danno e
    scagliato 3 m prono: qui perde il round dopo per rientrare nel cerchio."""
    b, dn = c.attacchi[0]
    if tira(b - 4, t.ca):            # −4 di Attacco Poderoso: STIMA della scelta
        t.subisci(dn() + 8)
        if not ts(t.rifl, 10 + 27):   # TS Riflessi CD = danno inflitto: qui sempre fallito
            t.fuori = 1


def arb_canone(c, st, g, rnd, sparsi, tattica):
    if rnd == 0:
        st.ca_bonus = 4 + 2           # scudo, grazia del gatto
        st.posizione = "alto"
        return
    if rnd == 1:
        m.presenza(c, g)
        m.soffio(c, st, g, rnd, sparsi)
        return
    v = vivi(g)
    if not v:
        return
    if rnd >= st.soffio_pronto:
        st.posizione = "alto"
        m.soffio(c, st, g, rnd, sparsi)
    elif rnd == 2 or R.random() < 0.5:
        st.posizione = "passata"
        m.morso(c, st, R.choice(v))
    else:
        st.posizione = "basso"
        mischia = [p for p in v if p.nome in ("Thorik", "Tordek")] or v
        _colpo_terrificante(c, st, g, R.choice(mischia))


def arb_nuova(c, st, g, rnd, sparsi, tattica):
    """Il bullo giovane, con un difetto leggibile:
    - sa del freddo: chi lo ferisce col freddo (Artemis) è il primo bersaglio, di
      soffio e di morso in passata; dardo incantato non serve (RI dei PG: nessuna);
    - cura ferite moderate su di sé sotto 150 pf (2 slot di 2°);
    - DIFETTO: il primo nano che lo ferisce in mischia lo offende, e il drago
      atterra a schiacciarlo per due round (attacco completo e Colpo Terrificante):
      è l'apertura che i PG possono leggere."""
    if rnd == 0:
        st.ca_bonus = 6
        st.risorse["cure"] = 2
        st.posizione = "alto"
        return
    if rnd == 1:
        m.presenza(c, g)
        m.soffio(c, st, g, rnd, sparsi)
        return
    v = vivi(g)
    if not v:
        return
    if st.pf < 150 and st.risorse["cure"] > 0:
        st.risorse["cure"] -= 1
        st.pf = min(c.pf, st.pf + d(2, 8) + 5)
        st.posizione = "alto"
        return
    offeso = st.flag.get("offeso", 0)
    if offeso == 0 and (g["Thorik"].danni_fatti > 0 or g["Tordek"].danni_fatti > 0):
        st.flag["offeso"] = 1
        offeso = 1
    if offeso in (1, 2):
        st.flag["offeso"] = offeso + 1
        st.posizione = "terra"
        t = max((g["Thorik"], g["Tordek"]), key=lambda p: p.danni_fatti)
        if t.giu():
            t = v[0]
        if offeso == 1:
            m.attacco_completo(c, st, t)
        else:
            _colpo_terrificante(c, st, g, t)
        return
    art = g["Artemis"]
    if rnd >= st.soffio_pronto:
        st.posizione = "alto"
        m.soffio(c, st, g, rnd, sparsi)
    else:
        st.posizione = "passata"
        m.morso(c, st, art if not art.giu() else R.choice(v))


@m.scontro("arbitrax")
def _arb(prove, buff):
    m.tabella("Arbitrax all'altare (duello, senza ritualisti né alleati)", ARB,
              {"canone": arb_canone, "nuova": arb_nuova}, TATTICHE_PG, prove, buff)
