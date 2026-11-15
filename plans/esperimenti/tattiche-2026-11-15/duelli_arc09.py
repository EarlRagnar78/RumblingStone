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
               estrae il cervello, usa *suggestione* (Vol CD 20) ogni round.
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
                if not ts(T["vol"], 20):
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


def tabella(titolo, f, politiche, prove):
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
    print("| Politica | " + " | ".join(esiti) + " | round | pf di Tordek alla fine |")
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


if __name__ == "__main__":
    main()
