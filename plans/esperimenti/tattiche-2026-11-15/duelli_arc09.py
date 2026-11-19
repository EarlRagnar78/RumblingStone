#!/usr/bin/env python3
"""Duelli di ARC-09 al Torneo di Dauth: Tordek da solo contro Kragar e contro Xal'thor.

Il Torneo è l'arco di Tordek (P2B): lì combatte senza il resto del gruppo, quindi
il motore comune (che mette in campo i quattro PG e chiude a due PG giù) non serve.
Qui c'è un duello piccolo che usa i dadi del motore (`simula_scontri.d/tira/ts`) e
i numeri di Tordek della carta del 05/11 (`simula_scontri.gruppo`).

STIME dichiarate:
- Tordek: For +5 (per lo sbilanciare); attacco +25/+20/+15 come nel motore; CA 22
  in ira. Sono i numeri del 05/11: al Torneo sarà più alto, il confronto fra
  tattiche resta relativo.
- Kragar: scheda d'arco (BATTLE-STATS §1), senza l'Ironclad (niente fiancheggiamento,
  niente attacco furtivo).
- Xal'thor: Bestiario (CA 24, 96 pf, Vol +16), tentacoli +12 (1d6+2) della scheda
  d'arco, esplosione mentale CD 17 (19 dal round 10 dell'arena: qui dal round 3).

Uso: python3 duelli_arc09.py [--prove 20000] [--seme 1372]
"""
from __future__ import annotations

import argparse
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, "..", "tattiche-draghi-2026-11-15"))
sys.path.insert(0, _QUI)
import simula_scontri as m  # noqa: E402
from simula_scontri import d, tira, ts  # noqa: E402

FOR_TORDEK = 5          # STIMA
STABILITA = 4           # nano, SRD


def tordek():
    g, stima = m.gruppo()
    t = g["Tordek"]
    return dict(pf=t.pf, ca=t.ca, temp=t.temp, vol=t.vol, att=stima["Tordek"]["att"] + 2,
                danno=stima["Tordek"]["danno"])


# ================================================================== KRAGAR
def duello_kragar(politica: str, max_round: int = 15):
    """politica:
    oggi     nessuna tattica scritta: il DM gioca la scheda, Sbilanciare Migliorato
             sul primo attacco ogni round (anche contro il nano).
    schema   tattica scritta il 15/11: non sbilancia Tordek (stabilità), prova
             Disarmare Migliorato sul primo attacco.
    pieno    solo attacchi completi, nessuna manovra (riferimento).
    """
    T = tordek()
    tp, kp = T["pf"], 88
    prono = disarmato = False
    intralciato = 0
    pioggia = True
    for rnd in range(1, max_round + 1):
        # --- Kragar (Iniziativa +3; si assume che agisca per primo: entra a sorpresa)
        attacchi = [16, 11] if rnd > 1 else [16]
        if pioggia and rnd == 1:
            pioggia = False
            if tira(16, T["ca"]):
                n = d(2, 4) + 6 + d(2, 6)
                tp -= n
                if not ts(m.gruppo()[0]["Tordek"].rifl, 18):
                    intralciato = 1
            attacchi = []
        for i, b in enumerate(attacchi):
            ca = T["ca"] - (4 if prono else 0)
            if i == 0 and politica == "oggi" and not prono:
                if tira(b, 10):                       # contatto, STIMA CA di contatto 10
                    if d(1, 20) + 4 + 4 > d(1, 20) + FOR_TORDEK + STABILITA:
                        prono = True
                        if tira(b, T["ca"] - 4):      # attacco gratuito di Sbilanciare Migliorato
                            tp -= d(2, 4) + 6
                continue
            if i == 0 and politica == "schema" and not disarmato:
                if d(1, 20) + b + 4 > d(1, 20) + T["att"]:
                    disarmato = True
                continue
            if tira(b, ca):
                tp -= d(2, 4) + 6
        if tp <= 0:
            return "Tordek giù", rnd, tp
        # --- Tordek
        pen = -2 if intralciato else 0
        serie = [0, -5, -10]
        if prono or disarmato:
            # si rialza o raccoglie l'arma: azione di movimento che provoca
            # (Riflessi in Combattimento), poi un attacco solo
            if tira(16, T["ca"] - (4 if prono else 0)):
                tp -= d(2, 4) + 6
            prono = disarmato = False
            serie = [0]
        for k in serie:
            if tira(T["att"] + k + pen, 23):
                kp -= T["danno"]()
        intralciato = max(0, intralciato - 1)
        if tp <= 0:
            return "Tordek giù", rnd, tp
        if kp <= 25:
            return "Kragar si arrende", rnd, tp
    return "stallo", max_round, tp


# ================================================================ XAL'THOR
def duello_xalthor(politica: str, max_round: int = 15):
    """politica:
    oggi       ricarica 1d4 dopo ogni esplosione; sugli storditi tentacoli ed
               estrarre il cervello (la scheda: «avanza sui bersagli storditi»).
    volonta    esplosione a volontà (scelta del DM del 15/11), stessa condotta.
    schema     a volontà; ma il suo obiettivo è convincere Tordek ad aprire il
               portale (Bestiario, §L'obiettivo reale): su Tordek stordito non
               estrae il cervello, usa *suggestione* (Vol CD 16, scelta del DM del 19/11) ogni round.
    """
    T = tordek()
    tp, xp = T["pf"], 96
    stordito = 0
    pronto = 0
    afferrato = False
    for rnd in range(1, max_round + 1):
        cd = 17 if rnd < 3 else 19
        # --- Xal'thor
        if stordito > 0:
            if politica == "schema":
                if not ts(T["vol"], 16):
                    return "Tordek convinto", rnd, tp
            elif afferrato:
                if not ts(T["temp"], 20):
                    return "Tordek morto (cervello)", rnd, -99
            else:
                colpi = sum(tira(12, T["ca"] - 2) for _ in range(4))   # stordito: −2 CA, senza Des (STIMA −2)
                tp -= sum(d(1, 6) + 2 for _ in range(colpi))
                afferrato = colpi == 4
        elif pronto <= 0:
            if not ts(T["vol"], cd):
                stordito = d(3, 4)
            if politica == "oggi":
                pronto = d(1, 4)
        else:
            colpi = sum(tira(12, T["ca"]) for _ in range(4))
            tp -= sum(d(1, 6) + 2 for _ in range(colpi))
        pronto -= 1
        if tp <= -10:
            return "Tordek morto", rnd, tp
        # --- Tordek
        if stordito > 0:
            stordito -= 1
        else:
            afferrato = False
            for k in (0, -5, -10):
                if tira(T["att"] + k, 24):
                    xp -= T["danno"]()
        if xp <= 25:
            return "Xal'thor fugge (spostamento planare)", rnd, tp
    return "stallo", max_round, tp



# ================================================================== KARRUK
# Bestiario/villain/Wyrmlord_Karruk/wyrmlord-karruk-cr13.md: duello sui gradini
# della breccia (Carta 13). Fuori ira CA 23, 181 pf, randello +23/+18/+13 (2d8+12);
# in ira (10 round) CA 21, 217 pf, +25/+20/+15 (2d8+15); ira intimidatoria:
# scosso chi lo vede (STIMA: Volontà CD 19). Attacco Poderoso −5 → +10 danni
# (a due mani). Morale: sotto 60 pf ripiega (duello «inconcluso»).
# STIME: campione Thorik (CA 27, 128 pf, ascia +22/+17/+12, 1d10+9, immune alla
# paura) o Tordek (CA 22 in ira, 106 pf, +25/+20/+15, 1d8+9+2d6, Volontà +12).
# Karruk ha iniziativa +0: si assume che il campione agisca per primo.
CAMPIONI = {
    "Thorik": dict(pf=128, ca=27, vol=11, att=(22, 17, 12), danno=lambda: d(1, 10) + 9, immune=True),
    "Tordek": dict(pf=106, ca=22, vol=12, att=(25, 20, 15), danno=lambda: d(1, 8) + 9 + d(2, 6), immune=False),
}


def duello_karruk(politica: str, campione: str = "Thorik", max_round: int = 15):
    """politica:
    oggi        la scheda: ira solo quando il campione lo ferisce (dal suo turno
                dopo), Attacco Poderoso −5 solo se la CA del campione è sotto 25.
    ira_subito  entra in ira al primo turno.
    poderoso    come oggi, ma Attacco Poderoso −5 sempre.
    """
    C = CAMPIONI[campione]
    cp, kp = C["pf"], 181
    ira, ferito, scosso, giri_ira = False, False, 0, 0
    for rnd in range(1, max_round + 1):
        # --- campione
        pen = -2 if scosso > 0 else 0
        for b in C["att"]:
            if tira(b + pen, 21 if ira else 23):
                kp -= C["danno"]()
                ferito = True
        scosso = max(0, scosso - 1)
        if kp <= 60:
            return "Karruk ripiega", rnd, cp
        # --- Karruk
        if not ira and giri_ira == 0 and (politica == "ira_subito" or ferito):
            ira, giri_ira = True, 10
            kp += 36
            if not C["immune"] and not ts(C["vol"], 19):
                scosso = 99
        pa = 5 if (politica == "poderoso" or C["ca"] < 25) else 0
        att = (25, 20, 15) if ira else (23, 18, 13)
        bonus = 15 if ira else 12
        for b in att:
            if tira(b - pa, C["ca"]):
                cp -= d(2, 8) + bonus + 2 * pa
        if ira:
            giri_ira -= 1
            if giri_ira == 0:
                ira = False
                kp = max(1, kp - 36)
        if cp <= -10:
            return "campione morto", rnd, cp
        if cp <= 0:
            return "campione a terra", rnd, cp
    return "stallo", max_round, cp


def tabella(titolo, f, politiche, prove, chi="Tordek"):
    print(f"\n### {titolo} · prove {prove}\n")
    esiti_tutti = set()
    righe = {}
    for p in politiche:
        cont, rnd, pf = {}, 0, 0
        for _ in range(prove):
            e, r, t = f(p)
            cont[e] = cont.get(e, 0) + 1
            rnd += r
            pf += max(t, 0)
            esiti_tutti.add(e)
        righe[p] = (cont, rnd / prove, pf / prove)
    esiti = sorted(esiti_tutti)
    print("| Politica | " + " | ".join(esiti) + f" | round | pf di {chi} alla fine |")
    print("|---|" + "---|" * len(esiti) + "---|---|")
    for p, (cont, r, pf) in righe.items():
        print(f"| {p} | " + " | ".join(f"{100 * cont.get(e, 0) / prove:.0f}%" for e in esiti)
              + f" | {r:.1f} | {pf:.0f} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prove", type=int, default=20000)
    ap.add_argument("--seme", type=int, default=1372)
    a = ap.parse_args()
    m.R.seed(a.seme)
    tabella("Kragar contro Tordek (semifinale, senza l'Ironclad)", duello_kragar,
            ["oggi", "schema", "pieno"], a.prove)
    tabella("Xal'thor contro Tordek (Giorno 3, duello senza le ondate)", duello_xalthor,
            ["oggi", "volonta", "schema"], a.prove)
    for camp in ("Thorik", "Tordek"):
        tabella(f"Karruk contro {camp} sui gradini (Carta 13, senza la scorta)",
                lambda p, camp=camp: duello_karruk(p, camp), ["oggi", "ira_subito", "poderoso"], a.prove,
                chi=camp)


if __name__ == "__main__":
    main()
