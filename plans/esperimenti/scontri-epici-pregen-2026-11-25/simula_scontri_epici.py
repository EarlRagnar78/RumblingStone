#!/usr/bin/env python3
"""Simula i duelli dei pregen di ARC-08 (DEF-1 Scena 8, DEF-2 Scene 2 e 4),
con le schede di oggi e con l'archetipo Avanzato. Sesto giro, 2026-11-25.

Modello semplice, 3.5 (Yrsa PF1e):
- iniziativa tirata, d20 + il bonus della scheda, un turno per creatura;
  nessuno e' colto alla sprovvista, perche' la battaglia e' gia' in corso;
- attacchi con d20 contro CA, minaccia di critico confermata con un secondo
  tiro per colpire, dove l'1 naturale manca e il 20 colpisce (SRD 3.5,
  «Combat I», Attack Roll e Critical Hits), moltiplicatore pieno sui dadi e
  sui bonus fissi (SRD);
- chi si muove per arrivare al nemico fa un attacco solo in quel turno, eroe
  o nemico; dal turno dopo, attacco completo (SRD);
- incantesimi ad area con Riflessi per dimezzare (eludere dove c'e'); l'1
  naturale fallisce sempre e il 20 naturale riesce sempre (SRD);
- la rigenerazione dei troll toglie 5 danni non da fuoco a round;
- il comandante fugge al suo turno, se e' sotto la soglia (libretto §5);
  Gorthak prima fa un round in Furia (A.1), e fugge alla fine di quel round.
  Se gli eroi lo portano a 0 pf o meno prima, non e' una fuga: il duello ha
  tre esiti (fugge, a 0 pf o meno, nessuno dei due) e le tabelle li contano
  in due colonne;
- la guardia (i veterani del sergente, gli orog di Grimjaw) si aggira: chi
  va accanto al comandante passa per un quadretto che una guardia minaccia,
  prende il suo attacco d'opportunita' e in quel turno fa un attacco solo;
  Nala lo evita con Acrobazia +9 contro CD 15. Nella variante «rampa chiusa»
  una guardia va abbattuta prima;
- il comandante (il sergente, Grimjaw) fa l'attacco completo solo a chi gli
  e' adiacente, non a chi sta colpendo una guardia: con la rampa chiusa
  Grimjaw e' dietro gli orog, e finche' nessuno lo raggiunge tira solo su
  chi lancia dalla cinta. Le guardie colpiscono chiunque sia in mischia;
- i veterani del sergente, nella versione piu' dura, al round 1 restano in
  F10-G10 (ARC08-DEF-1, «Sfidare il sergente, round per round»): in quel
  round hanno solo l'attacco d'opportunita', e dal round 2 attaccano in
  pieno;
- il ponte di Gorthak (MAPPA 2A): un eroe esce a round dallo sportello,
  prende l'attacco d'opportunita' di Gorthak (Nala lo evita con Acrobazia) e
  fa un attacco solo; il primo va in BG75, dove arrivano tutti e due i
  troll, il secondo in BG74, dove ne arriva uno; i troll entrano al round 2;
- Gorthak (ettin, SRD: Superior Two-Weapon Fighting): Forza piena su tutti e
  due le armi, 2d6+10 e 2d6+10 (le stelle del mattino Grandi dell'ettin
  SRD; la scheda di ARC08-01 le chiama randelli); la scheda da' 2d6+5 alla
  seconda, e c'e' uno scenario con quella lettura, e uno coi randelli
  Grandi dell'SRD, 1d8+10. La testa sinistra da' +2
  ai danni del primo colpo a segno del round (scheda). Divide i colpi: il
  primo randello su Borin se c'e', l'altro sul piu' ferito degli altri;
- Grimjaw: al round 1 non attacca; dal suo turno del round 2 e' in Furia
  Comandante, con +26 pf; resistenza al fuoco 10 (armatura demoniaca,
  ARC08-01). La soglia di fuga resta 89 pf, meta' dei 178 della scheda: i
  26 pf della Furia non la spostano. Se al suo turno e' gia' sotto 89, fugge
  senza entrare in Furia;
- Yrsa: Concentrazione Furiosa (Furious Focus, PF1e) vale solo con un'arma
  a due mani, e Yrsa porta lo scudo: Attacco Poderoso +19/+14/+9, 1d10+18.
  La scheda di ARC08-01 scrive +23/+14/+9: e' una domanda al DM. La Sfida
  (+18 ai danni, +4 a colpire agli alleati, -2 alla CA del bersaglio contro
  gli altri: Sfida Pressante) vale da quando Yrsa e' accanto al bersaglio;
- Dara: Tiro Rapido +17/+17/+12/+7; il nemico prescelto (+4 contro i
  giganti) e' contato a colpire e ai danni come sulla scheda di campagna;
  l'SRD 3.5 lo da' solo ai danni, e c'e' uno scenario con quella lettura;
- Ragnhild lancia dalla cinta. Se apre, i nani ritardano finche' non ha
  lanciato le due palle di fuoco (ritardata 13d6 CD 26, rapida 10d6 CD 22).
  Poi, coi nani in mischia, due raggi roventi e i dardi incantati (il primo
  massimizzato: cinque dardi al LI 13, 25 danni); senza
  nani in mischia, una palla di fuoco a round (10d6, CD 22);
- chi tira o lancia dalla cinta non e' raggiunto in mischia. Gorthak, se non
  ha un nano accanto, lancia un giavellotto a round su Ragnhild (+10 al
  secondo incremento, 1d8+9); Dara a 48 m e' fuori gittata. Grimjaw, se non
  ha un nano accanto, tira con l'arco dal round 2, e dal round 3 due orog
  arrivano su chi lancia dal camminamento.
Limiti: niente movimento oltre lo sportello e la guardia; tutte le guardie
vive colpiscono l'eroe piu' ferito fra quelli in mischia (il caso peggiore);
la CA di Gorthak in Furia non conta (fugge alla fine di quel round); gli
incantesimi di Harbek e Nala non ci sono; le leve della Sessione 1 (+2 e +4
a colpire contro Gorthak) non ci sono; i giganti e gli archi dei veterani
non tirano su chi sta sulla cinta; Grimjaw dietro gli orog non tira con
l'arco sui nani in mischia.
Quello che manca agli eroi: la Presenza Comandante di Borin, l'Ispirare
Coraggio di Nala, la Postura di Borin. Sono assenze che pendono contro gli
eroi: al tavolo i nani fanno un po' meglio di queste cifre. Manca anche il
+2 della testa sinistra di Gorthak sull'attacco d'opportunita', che pende
dall'altra parte, di poco.

Numeri: ARC08-01, ARC08-02 §3, Appendici A di ARC08-DEF-1 e ARC08-DEF-2,
Bestiario. L'archetipo semplice Avanzato di PF1e: +2 a tutti i tiri e ai
danni, +2 pf per DV; la CA e' quella ricostruita con la regola intera, salvo
l'orog Avanzato (scartato), che tiene le regole rapide della sua scheda, +4.

L'orog della guardia nera e' quello della scheda del Bestiario rifatta il
2026-11-20 (PR #521): CA 21, pf 45, ascia +14/+9 (1d12+12). Fino al
2026-11-26 il simulatore usava la scheda di prima (CA 19, pf 63, +13/+8,
1d12+10; Avanzato CA 23, 75 pf). Una prova lega i numeri alla scheda.

Ogni riga ha il suo seme (--seme, il titolo dello scenario, gli eroi): una
correzione a uno scenario non sposta le cifre degli altri.

Il punto eroe (--punto-eroe, card del DM del 2026-11-25, «gesto da leggenda»):
regola opzionale di PF1e (Advanced Player's Guide, «Hero Points»,
https://www.d20pfsrd.com/gamemastering/other-rules/hero-points/). Ogni eroe
ne ha UNO per i tre giorni d'assedio. L'opzione stampa un confronto sulle
righe principali, con ogni eroe che spende il suo punto in quello scontro:
e' il massimo che quella politica puo' dare su quello scontro, non la media
dei tre giorni, perche' chi lo spende contro il sergente non lo ha piu'
contro Gorthak. Tre politiche, una alla volta:
- «bonus» (Bonus): +8 di fortuna, dichiarato prima, al primo tiro per colpire
  dell'eroe contro il comandante; vale per quel d20 soltanto, e non per il
  tiro di conferma del critico, che e' un altro d20;
- «azione» (Extra Action, azione standard): nel primo turno in cui l'eroe
  attacca, un attacco in piu' al bonus piu' alto, sullo stesso bersaglio;
  Dara una freccia in piu' a +17; Ragnhild, nel suo primo turno, una palla di
  fuoco in piu' (10d6, CD 22) se nessun nano e' in mischia, se no tre raggi
  roventi in piu';
- «movimento» (Extra Action, azione di movimento): nel turno in cui l'eroe
  si muove per arrivare al nemico fa tutti i suoi attacchi invece di uno
  solo (il movimento e' l'azione in piu', e gli resta il round intero); Dara
  e Ragnhild, che non si muovono, non lo spendono.
Senza --punto-eroe l'uscita e' quella di sempre, byte per byte: il punto non
tira dadi e non cambia la sequenza dei tiri.

La rampa chiusa (--rampa-chiusa, lettore a freddo del 2026-11-25): stampa
le otto combinazioni di Grimjaw a rampa chiusa, comprese le tre che
esito_simulazione.md non ha (Yrsa da sola; Harbek e Nala; Ragnhild da sola),
e le ripete con la regola del master: la cima la chiudono i due orog davanti,
i due dietro sono quelli che si staccano. Senza l'opzione l'uscita e' quella
di sempre, byte per byte.

Uso: python3 simula_scontri_epici.py [--n 4000] [--seme 7] [--eroi-primi]
     python3 simula_scontri_epici.py --rampa-chiusa [--n 4000] [--seme 7]
     python3 simula_scontri_epici.py --punto-eroe [--n 4000] [--seme 7] [--eroi-primi]
"""
import argparse
import math
import random
import statistics

R = random.Random(7)
EROI_PRIMI = False  # --eroi-primi: il limite dei primi quattro giri, per confronto
PUNTO = None  # --punto-eroe: None, "bonus", "azione" o "movimento"


def d(n, f):
    return sum(R.randint(1, f) for _ in range(n))


def colpo(bonus, ca, dadi, fisso, minaccia=20, molt=2, extra=None, fortuna=0):
    """Un attacco. Ritorna i danni (0 se manca). extra: dadi in piu' che non
    si moltiplicano (furtivo, Colpo Devastante). fortuna: il +8 del punto
    eroe, sul tiro per colpire e non sulla conferma del critico."""
    t = R.randint(1, 20)
    if t == 1 or (t != 20 and t + bonus + fortuna < ca):
        return 0
    n, f = dadi
    crit = False
    if t >= minaccia:
        c = R.randint(1, 20)
        crit = c != 1 and (c == 20 or c + bonus >= ca)
    volte = molt if crit else 1
    dmg = sum(d(n, f) + fisso for _ in range(volte))
    if extra:
        dmg += d(*extra)
    return max(1, dmg)


def riflessi(base_dmg, ts, cd, eludere=False):
    """Riflessi per dimezzare. L'1 naturale fallisce sempre e il 20 naturale
    riesce sempre (SRD 3.5, «Saving Throws», Automatic Failures and Successes)."""
    t = R.randint(1, 20)
    ok = t != 1 and (t == 20 or t + ts >= cd)
    if eludere:
        return 0 if ok else base_dmg
    return base_dmg // 2 if ok else base_dmg


class Nemico:
    def __init__(self, nome, pf, ca, attacchi, rifl, iniz, rigen=0, fuga=None,
                 entra=1, primo=None, ruolo="scorta"):
        self.nome, self.pfmax, self.pf, self.ca = nome, pf, pf, ca
        self.attacchi, self.rifl, self.rigen = attacchi, rifl, rigen
        self.iniz = iniz
        self.fuga, self.entra, self.primo, self.ruolo = fuga, entra, primo, ruolo
        self.giu = False
        self.nonfuoco = 0
        self.resfuoco = 0
        self.arrivato = False

    def danno(self, n, fuoco=False):
        if fuoco:
            n = max(0, n - self.resfuoco)
        self.pf -= n
        if self.rigen and not fuoco:
            self.nonfuoco += n
        if self.pf <= 0:
            self.giu = True


# --- i pregen (ARC08-02 §3, ARC08-01) ---------------------------------
EROI = {
    "Borin": dict(iniz=1, vol=8, pf=142, ca=25, melee=[(21, (1, 8), 9, 20, 3), (16, (1, 8), 9, 20, 3), (11, (1, 8), 9, 20, 3)], devastante=3),
    # Attacco Poderoso -4/+8 a una mano, senza Concentrazione Furiosa (lo scudo)
    "Yrsa": dict(iniz=5, vol=10, pf=114, ca=32, melee=[(19, (1, 10), 18, 20, 3), (14, (1, 10), 18, 20, 3), (9, (1, 10), 18, 20, 3)], sfida=18),
    "Nala": dict(iniz=4, vol=9, pf=90, ca=20, melee=[(13, (1, 6), 3, 15, 2), (8, (1, 6), 3, 15, 2)], acrobazia=9),
    "Harbek": dict(iniz=1, vol=16, pf=114, ca=22, melee=[(13, (1, 8), 5, 20, 3), (8, (1, 8), 5, 20, 3)]),
    "Dara": dict(iniz=4, vol=9, pf=102, ca=21, arco=True),
    "Ragnhild": dict(iniz=6, vol=14, pf=84, ca=18, maga=True),
}


def eroe(nome):
    e = dict(EROI[nome])
    e["nome"], e["pfcur"] = nome, e["pf"]
    return e


def duello(nemici_fn, eroi_nomi, giganti=False, round_max=8, ragn_apre=True, dara_srd=False):
    nemici = nemici_fn()
    boss = [n for n in nemici if n.ruolo == "boss"][0]
    eroi = [eroe(n) for n in eroi_nomi]
    mischia = [e for e in eroi if "melee" in e]
    lontani = [e for e in eroi if "melee" not in e]
    for i, e in enumerate(mischia):
        e["_entra"] = i + 1
    yrsa = [e for e in eroi if e["nome"] == "Yrsa"]
    sportello = getattr(boss, "sportello", False)
    dist = getattr(boss, "distanza_arco", 0)

    # --- iniziativa: d20 + bonus; a pari, il bonus, poi la sorte
    for e in eroi:
        e["_t"] = (R.randint(1, 20) + e["iniz"] + (100 if EROI_PRIMI else 0), e["iniz"], R.random())
    for n in nemici:
        n.t = (R.randint(1, 20) + n.iniz, n.iniz, R.random())
    maga = next((e for e in eroi if e.get("maga")), None)
    if maga and ragn_apre:
        # i nani ritardano finche' Ragnhild non ha lanciato (SRD: Delay)
        k = 0
        for e in mischia:
            if e["_t"] > maga["_t"]:
                k += 1
                e["_t"] = (maga["_t"][0], maga["_t"][1], maga["_t"][2] - k * 1e-9)
    turni = sorted([("e", e) for e in eroi] + [("n", n) for n in nemici],
                   key=lambda x: x[1]["_t"] if x[0] == "e" else x[1].t, reverse=True)

    def sfida():
        return bool(yrsa) and yrsa[0]["pfcur"] > 0 and yrsa[0].get("_sul_boss", False)

    def scorte_vive(rnd):
        return [n for n in nemici if n.ruolo == "scorta" and not n.giu and n.entra <= rnd]

    def in_mischia():
        return [e for e in mischia if e["pfcur"] > 0 and e.get("_mischia")]

    def acrobazia(e):
        return "acrobazia" in e and R.randint(1, 20) + e["acrobazia"] >= 15

    # la Presenza intimidatoria (Grimjaw): entro 9 m, Volonta', o -2 a colpire
    for e in eroi:
        cd = getattr(boss, "presenza", 0)
        e["_pres"] = 2 if cd and "melee" in e and R.randint(1, 20) + e["vol"] < cd else 0

    caduti = set()
    # esito: "fugge" (la soglia, al suo turno; per Gorthak dopo il round in
    # Furia) o "abbattuto" (a 0 pf o meno per mano degli eroi)
    stato = dict(min_frac=1.0, esito=None)

    def ferisci(e, x):
        e["pfcur"] -= x
        if e["pfcur"] <= 0:
            caduti.add(e["nome"])

    def spende(e, politica):
        """True una volta sola, se la politica e' quella in prova."""
        if PUNTO != politica or e.get("_punto"):
            return False
        e["_punto"] = True
        return True

    def fortuna(e):
        return 8 if spende(e, "bonus") else 0

    def attacca_eroe(e, b, colpi):
        su_boss = b is boss
        if spende(e, "azione"):
            colpi = list(colpi) + [e["melee"][0]]
        altro = e["nome"] != "Yrsa"
        bonus_sfida = 4 if (sfida() and altro and su_boss) else 0
        ca_b = b.ca - (2 if (sfida() and altro and su_boss) else 0)
        for i, (bon, dadi, fisso, mn, ml) in enumerate(colpi):
            if b.giu:
                break
            extra = None
            if e.get("devastante") and i == 0 and e.get("_dev", 0) < e["devastante"]:
                e["_dev"] = e.get("_dev", 0) + 1
                extra = (4, 6)
            f = fisso + (e["sfida"] if (e.get("sfida") and su_boss) else 0)
            b.danno(colpo(bon + bonus_sfida - e["_pres"], ca_b, dadi, f, mn, ml, extra,
                          fortuna=fortuna(e) if su_boss else 0))

    def turno_eroe(e, rnd):
        vivi = [n for n in nemici if not n.giu and n.entra <= rnd]
        if not vivi:
            return
        guardie = scorte_vive(rnd) if getattr(boss, "guardato", False) else []
        cop = 4 if guardie else 0  # la guardia da' copertura a chi sta dietro
        if e.get("maga"):
            if spende(e, "azione"):
                if not in_mischia():
                    for n in vivi:
                        n.danno(riflessi(d(10, 6), n.rifl, 22, getattr(n, "eludere", False)), fuoco=True)
                else:
                    for _ in range(3):
                        boss.danno(colpo(8, getattr(boss, "contatto", 11) + cop, (4, 6), 0), fuoco=True)
            if ragn_apre and not e.get("_aperto") and not in_mischia():
                e["_aperto"] = True
                for n in vivi:
                    n.danno(riflessi(d(13, 6), n.rifl, 26, getattr(n, "eludere", False)), fuoco=True)
                    n.danno(riflessi(d(10, 6), n.rifl, 22, getattr(n, "eludere", False)), fuoco=True)
            elif not mischia:
                for n in vivi:  # nessun nano in mischia: palla di fuoco, 10d6 CD 22
                    n.danno(riflessi(d(10, 6), n.rifl, 22, getattr(n, "eludere", False)), fuoco=True)
            elif e.get("_raggi", 0) < 2:
                e["_raggi"] = e.get("_raggi", 0) + 1
                for _ in range(3):  # raggio rovente: tre raggi, 4d6, contatto a distanza +8
                    boss.danno(colpo(8, getattr(boss, "contatto", 11) + cop, (4, 6), 0,
                                     fortuna=fortuna(e)), fuoco=True)
            elif e.get("_dardi", 0) < 3:
                e["_dardi"] = e.get("_dardi", 0) + 1
                boss.danno(25 if e["_dardi"] == 1 else d(5, 4) + 5)  # il primo massimizzato, LI 13
            return
        if e.get("arco"):
            gb = 4 if giganti else 0
            gc = 0 if dara_srd else gb  # SRD 3.5: il nemico prescelto solo ai danni
            frecce = (17, 17, 12, 7) + ((17,) if spende(e, "azione") else ())
            for bon in frecce:
                boss.danno(colpo(bon + gc - dist, boss.ca + cop, (1, 8), 6 + gb, 20, 3, fortuna=fortuna(e)))
            return
        colpi = e["melee"]
        if sportello:
            if not e.get("_mischia"):
                if rnd < e["_entra"]:
                    return
                # esce: l'attacco d'opportunita' di Gorthak (uno a round), un attacco solo
                e["_mischia"] = e["_sul_boss"] = True
                e["_quad"] = 75 if not any(x.get("_quad") == 75 and x["pfcur"] > 0 for x in mischia) else 74
                if not acrobazia(e):
                    (bon2, dadi2, f2, mn2, ml2, _t) = boss.attacchi[0]
                    ferisci(e, colpo(bon2, e["ca"], dadi2, f2, mn2, ml2))
                    if e["pfcur"] <= 0:
                        return
                if not spende(e, "movimento"):
                    colpi = colpi[:1]
            attacca_eroe(e, boss, colpi)
            return
        tutte = [n for n in nemici if n.ruolo == "scorta"]
        muro = getattr(boss, "muro", 0)
        fronte = getattr(boss, "fronte", 0)
        if fronte:
            # --rampa-chiusa: la cima la chiudono i soli orog davanti
            davanti = [n for n in guardie if getattr(n, "davanti", False)]
            chiusa, primo = len(davanti) == fronte, davanti[:1]
        else:
            chiusa, primo = muro and guardie and len(guardie) > len(tutte) - muro, guardie[:1]
        if chiusa:
            # la rampa chiusa: prima si abbatte una guardia
            if not e.get("_mischia"):
                e["_mischia"] = True
                if not spende(e, "movimento"):
                    colpi = colpi[:1]
            attacca_eroe(e, primo[0], colpi)
            return
        if not e.get("_sul_boss"):
            if guardie:
                if not acrobazia(e):
                    (bon2, dadi2, f2, mn2, ml2, _t) = guardie[0].attacchi[0]
                    ferisci(e, colpo(bon2, e["ca"], dadi2, f2, mn2, ml2))
                    if e["pfcur"] <= 0:
                        return
                if not spende(e, "movimento"):
                    colpi = colpi[:1]
            elif not (muro and e.get("_mischia")):
                if not spende(e, "movimento"):
                    colpi = colpi[:1]  # si avvicina: un attacco solo
            e["_mischia"] = e["_sul_boss"] = True
        attacca_eroe(e, boss, colpi)

    def serie(n, seq, bersagli, sinistra=False):
        """seq: lista di attacchi; bersagli: lista parallela di eroi."""
        artigli = 0
        primo = sinistra
        for (bon, dadi, fisso, mn, ml, tag), tt in zip(seq, bersagli):
            if tt["pfcur"] <= 0:
                continue
            ca_tt = tt["ca"] - (2 if (tt["nome"] == "Yrsa" and n is not boss and sfida()) else 0)
            x = colpo(bon, ca_tt, dadi, fisso, mn, ml)
            if x and primo:
                x += 2  # la testa sinistra
                primo = False
            if x and tag == "artiglio":
                artigli += 1
            ferisci(tt, x)
        return artigli

    def piu_ferito(lista):
        return min(lista, key=lambda e: e["pfcur"] / e["pf"])

    def turno_nemico(n, rnd):
        if n.giu or n.entra > rnd:
            return
        if n.rigen and n.nonfuoco > 0:
            r = min(n.rigen, n.nonfuoco)
            n.nonfuoco -= r
            n.pf += r
        bers = in_mischia()
        vivi_lontani = [e for e in lontani if e["pfcur"] > 0]
        if n is boss:
            # il comandante colpisce solo chi gli e' adiacente
            bers = [e for e in bers if e.get("_sul_boss")]
            furia = False
            if n.pf < n.fuga:
                if not getattr(n, "furia", None):
                    stato["esito"] = "fugge"
                    return
                furia = True
                stato["furia"] = True
            if getattr(n, "furia_pf", 0) and rnd >= 2 and not getattr(n, "in_furia", False):
                n.in_furia = True
                n.pf += n.furia_pf
            if not bers:
                guardie = scorte_vive(rnd) if getattr(n, "guardato", False) else []
                vivi_m = [e for e in mischia if e["pfcur"] > 0]
                if sportello or guardie or not vivi_m:
                    # resta dov'e': tira su chi lancia dalla cinta
                    tiro = getattr(n, "tiro", None)
                    if tiro and rnd >= getattr(n, "tiro_dal", 1):
                        cand = [e for e in vivi_lontani if e.get("maga") or not sportello]
                        if cand:
                            serie(n, tiro, [cand[0]] * len(tiro))
                    return
                t = vivi_m[0]  # va lui dall'eroe: un attacco solo
                t["_mischia"] = t["_sul_boss"] = True
                serie(n, n.attacchi[:1], [t])
                return
            seq = n.furia if furia else (n.primo if (n.primo is not None and rnd == 1) else n.attacchi)
            if sportello and len(bers) >= 2 and len(seq) == 6:
                primo_b = next((e for e in bers if e["nome"] == "Borin"), piu_ferito(bers))
                secondo_b = piu_ferito([e for e in bers if e is not primo_b])
                serie(n, seq, [primo_b] * 3 + [secondo_b] * 3, sinistra=getattr(n, "sinistra", False))
            else:
                serie(n, seq, [piu_ferito(bers)] * len(seq), sinistra=getattr(n, "sinistra", False))
            return
        if n.ruolo == "ariete":
            if rnd == 1:
                return
            if sportello:
                quad = (74, 75) if n.nome == "troll0" else (75,)
                bers = [e for e in bers if e.get("_quad") in quad]
            if not bers:
                return
            t = piu_ferito(bers)
            if serie(n, n.attacchi, [t] * len(n.attacchi)) == 2 and t["pfcur"] > 0:
                ferisci(t, d(*n.sbranare[0]) + n.sbranare[1])
            return
        # la scorta
        if getattr(n, "avanza", False) and getattr(boss, "guardato", False) and rnd == 1:
            return  # i veterani di guardia restano in F10-G10: solo l'attacco d'opportunita'
        if not bers:
            vivi_m = [e for e in mischia if e["pfcur"] > 0]
            if getattr(n, "avanza", False) and vivi_m:
                t = vivi_m[0]  # sale sull'eroe: un attacco solo
                t["_mischia"] = True
                n.arrivato = True
                serie(n, n.attacchi[:1], [t])
            elif getattr(n, "caccia", False) and not vivi_m and vivi_lontani and rnd >= 3:
                t = vivi_lontani[0]
                seq = n.attacchi if n.arrivato else n.attacchi[:1]
                n.arrivato = True
                serie(n, seq, [t] * len(seq))
            return
        seq = n.primo if (n.primo is not None and rnd == 1) else n.attacchi
        if getattr(n, "avanza", False) and not n.arrivato:
            n.arrivato = True
            if getattr(boss, "guardato", False) is False:
                seq = seq[:1]
        serie(n, seq, [piu_ferito(bers)] * len(seq))

    for rnd in range(1, round_max + 1):
        stato["furia"] = False
        for tipo, a in turni:
            if tipo == "e":
                if a["pfcur"] > 0:
                    turno_eroe(a, rnd)
                    if boss.giu:
                        # a 0 pf o meno prima di poter fuggire: non e' una fuga
                        stato["esito"] = "abbattuto"
            else:
                turno_nemico(a, rnd)
            if stato["esito"]:
                break
        for e in eroi:
            stato["min_frac"] = min(stato["min_frac"], max(0, e["pfcur"]) / e["pf"])
        if stato["furia"] and not stato["esito"]:
            # Gorthak ha finito il suo round in Furia ancora in piedi: lascia il
            # ponte (ARC08-DEF-2, «Sotto i 101 pf»: «È la fuga del libretto»)
            stato["esito"] = "fugge"
        if stato["esito"]:
            return dict(esito=stato["esito"], round=rnd, min_frac=stato["min_frac"], caduti=len(caduti))
        if all(e["pfcur"] <= 0 for e in eroi):
            return dict(esito=None, round=rnd, min_frac=0, caduti=len(eroi))
    return dict(esito=None, round=round_max, min_frac=stato["min_frac"], caduti=len(caduti))


# --- i nemici ----------------------------------------------------------
A = lambda b, dadi, f, mn=20, ml=2, tag="": (b, dadi, f, mn, ml, tag)


def sergente(avanzato=False, veterani=0, entra=2, guardia=False):
    def fn():
        k = 2 if avanzato else 0
        # A.4: CA 21, Riflessi +7; A.4-bis: CA 23 (contatto 12, sprovvista 22), Riflessi +9;
        # la mano secondaria con la regola intera (1/2 For): 1d8+3 oggi, 1d8+4 Avanzato
        s = Nemico("sergente", 62 if avanzato else 50, 23 if avanzato else 21,
                   [A(9 + k, (1, 8), 6 + k, 19), A(4 + k, (1, 8), 6 + k, 19),
                    A(9 + k, (1, 8), 3 + k // 2, 19), A(4 + k, (1, 8), 3 + k // 2, 19)],
                   rifl=7 + k, iniz=4 + k, fuga=(62 if avanzato else 50) / 2, ruolo="boss")
        s.guardato = guardia
        s.contatto = 12
        out = [s]
        for i in range(veterani):  # hobgoblin veterani, Bestiario, GS 5
            v = Nemico(f"veterano{i}", 43, 19, [A(10, (1, 8), 2, 19), A(5, (1, 8), 2, 19)],
                       rifl=4, iniz=1, entra=entra)
            v.avanza = True
            out.append(v)
        return out
    return fn


def gorthak(avanzato=False, troll_avanzati=False, sportello=True, scheda=False, randelli=False):
    def fn():
        k = 2 if avanzato else 0
        pf = 232 if avanzato else 202
        # SRD, ettin: Forza piena sui due randelli; scheda di ARC08-01: meta' sul secondo
        f2, ff2 = (5, 6) if scheda else (10, 12)
        # scheda: «Randello Enorme» 2d6, il dado della stella del mattino Grande
        # dell'ettin SRD; un randello Grande fa 1d8
        da = (1, 8) if randelli else (2, 6)
        g = Nemico("Gorthak", pf, 28 if avanzato else 25,
                   [A(21 + k, da, 10 + k), A(16 + k, da, 10 + k), A(11 + k, da, 10 + k),
                    A(21 + k, da, f2 + k), A(16 + k, da, f2 + k), A(11 + k, da, f2 + k)],
                   rifl=7 + k, iniz=6 + k, fuga=pf / 2, ruolo="boss")
        g.contatto = 12 if avanzato else 11
        # Furia (+4 For): +2 a colpire, +2 ai danni
        g.furia = [A(23 + k, da, 12 + k), A(18 + k, da, 12 + k), A(13 + k, da, 12 + k),
                   A(23 + k, da, ff2 + k), A(18 + k, da, ff2 + k), A(13 + k, da, ff2 + k)]
        g.sinistra = True
        g.sportello = sportello
        g.distanza_arco = 2  # Dara dalla Torre Ovest, secondo incremento
        g.tiro = [A(10 + k, (1, 8), 9 + k)]  # giavellotto, secondo incremento
        out = [g]
        t = 2 if troll_avanzati else 0
        for i in range(2):
            tr = Nemico(f"troll{i}", 125 if troll_avanzati else 105, 20 if troll_avanzati else 16,
                        [A(13 + t, (1, 6), 7 + t, tag="artiglio"), A(13 + t, (1, 6), 7 + t, tag="artiglio"),
                         A(8 + t, (1, 6), 3 + t)], rifl=5 + t, iniz=2 + t, rigen=5, ruolo="ariete")
            tr.sbranare = ((2, 6), 10 + t)
            out.append(tr)
        return out
    return fn


def grimjaw(orog_avanzati=False, muro=0, fronte=0):
    def fn():
        # round 1: Tattico Superiore e Presenza, nessun attacco; dal round 2 Furia
        # Comandante: +24/+19/+14 (1d10+11, 17-20) e +26 pf
        g = Nemico("Grimjaw", 178, 26, [A(24, (1, 10), 11, 17), A(19, (1, 10), 11, 17), A(14, (1, 10), 11, 17)],
                   rifl=8, iniz=5, fuga=89, ruolo="boss", primo=[])
        g.guardato = True
        g.muro = muro
        g.fronte = fronte
        g.presenza = 19
        g.contatto = 12
        g.resfuoco = 10  # Armatura Completa Demoniaca +2 (ARC08-01)
        g.furia_pf = 26
        g.tiro = [A(15, (1, 8), 7, 20, 3), A(10, (1, 8), 7, 20, 3), A(5, (1, 8), 7, 20, 3)]
        g.tiro_dal = 2
        out = [g]
        o = 2 if orog_avanzati else 0
        for i in range(4):
            # la scheda (Bestiario, dal 2026-11-20): CA 21, pf 45 (6d10+12), Rifl +2,
            # Iniz +4, ascia bipenne +1 +14/+9 (1d12+12, x3). Avanzato, regole rapide
            # PF1e: CA 25, pf 57 (45 + 2 x 6 DV), +2 ai tiri e ai danni.
            # Attacco Poderoso -3 (+6); round 1 Tattico Superiore +2 a colpire; dal 2 anche Furia +2/+2
            og = Nemico(f"orog{i}", 57 if orog_avanzati else 45, 25 if orog_avanzati else 21,
                        [A(15 + o, (1, 12), 20 + o, 20, 3), A(10 + o, (1, 12), 20 + o, 20, 3)],
                        rifl=2 + o, iniz=4 + o,
                        primo=[A(13 + o, (1, 12), 18 + o, 20, 3), A(8 + o, (1, 12), 18 + o, 20, 3)])
            og.caccia = i < 2
            og.davanti = i >= 2  # i due dietro sono quelli che si staccano
            out.append(og)
        return out
    return fn


BY = [["Borin"], ["Yrsa"], ["Nala"], ["Harbek"]]
SCENARI = [
    ("Sergente, oggi (A.4; la scorta non entra)", sergente(), BY, False),
    ("Sergente, versione piu' dura: Avanzato + 2 veterani di guardia, si aggirano, dal round 1",
     sergente(True, 2, 1, True), BY + [["Borin", "Yrsa"], ["Harbek", "Dara"], ["Nala", "Dara"]], False),
    ("Sergente, variante scartata A: Avanzato + 4 veterani dal round 2", sergente(True, 4), BY, False),
    ("Sergente, variante scartata B: Avanzato + 4 veterani di guardia, si aggirano, dal round 1",
     sergente(True, 4, 1, True), BY + [["Borin", "Yrsa"]], False),
    ("Gorthak, oggi, senza lo sportello (riferimento del primo giro)", gorthak(sportello=False),
     [["Borin"], ["Borin", "Yrsa"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"], ["Borin", "Yrsa", "Ragnhild"]], True),
    ("Gorthak, oggi, con lo sportello", gorthak(),
     [["Borin"], ["Yrsa"], ["Borin", "Yrsa"], ["Yrsa", "Borin"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"],
      ["Yrsa", "Borin", "Dara"], ["Borin", "Yrsa", "Ragnhild"], ["Yrsa", "Borin", "Ragnhild"],
      ["Harbek", "Nala"], ["Harbek", "Nala", "Dara"], ["Harbek", "Nala", "Ragnhild"],
      ["Ragnhild", "Dara"], ["Ragnhild"], ["Dara"]], True),
    ("Gorthak, oggi, con lo sportello, il secondo randello come sulla scheda (2d6+5)", gorthak(scheda=True),
     [["Borin"], ["Borin", "Yrsa"], ["Yrsa", "Borin"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"],
      ["Borin", "Yrsa", "Ragnhild"], ["Yrsa", "Borin", "Ragnhild"]], True),
    ("Gorthak, oggi, con lo sportello, randelli Grandi dell'SRD (1d8+10 e 1d8+10)", gorthak(randelli=True),
     [["Borin"], ["Borin", "Yrsa"], ["Yrsa", "Borin"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"],
      ["Borin", "Yrsa", "Ragnhild"], ["Yrsa", "Borin", "Ragnhild"]], True),
    ("Gorthak, oggi, con lo sportello, il nemico prescelto di Dara solo ai danni (SRD 3.5)", gorthak(),
     [["Borin", "Dara"], ["Borin", "Yrsa", "Dara"], ["Yrsa", "Borin", "Dara"], ["Harbek", "Nala", "Dara"],
      ["Ragnhild", "Dara"], ["Dara"]], "dara-srd"),
    ("Gorthak Avanzato (scartato), con lo sportello", gorthak(True),
     [["Borin"], ["Borin", "Yrsa"], ["Yrsa", "Borin"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"],
      ["Borin", "Yrsa", "Ragnhild"], ["Yrsa", "Borin", "Ragnhild"]], True),
    ("Gorthak, oggi, con lo sportello, Ragnhild senza l'apertura", gorthak(),
     [["Borin", "Yrsa", "Ragnhild"], ["Yrsa", "Borin", "Ragnhild"]], "noapre"),
    ("Gorthak e troll tutti Avanzati, con lo sportello (scartato)", gorthak(True, True), [["Borin", "Yrsa"], ["Yrsa", "Borin"]], True),
    ("Grimjaw e quattro orog, oggi: la guardia si aggira", grimjaw(),
     [["Borin"], ["Yrsa"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"],
      ["Harbek", "Nala"], ["Harbek", "Nala", "Ragnhild"], ["Ragnhild"]], False),
    ("Grimjaw e quattro orog, variante: la rampa chiusa, se ne abbatte uno", grimjaw(muro=1),
     [["Borin"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"],
      ["Harbek", "Nala", "Ragnhild"]], False),
    ("Grimjaw, la guardia si aggira, Ragnhild senza l'apertura", grimjaw(), [["Borin", "Yrsa", "Ragnhild"]], "noapre"),
    ("Grimjaw, orog Avanzati (scartato)", grimjaw(True),
     [["Borin"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"]], False),
]


def el(gs):
    """EL della DMG 3.5: 2 log2(somma di 2^(GS/2)), come scripts/suggest_encounter.py."""
    return 2 * math.log2(sum(2 ** (g / 2) for g in gs))


TABELLA_EL = [
    ("pattuglia: 3 cavalcatori GS 5 (+3 worg GS 2)", [5, 5, 5, 2, 2, 2], None),
    ("scout: sergente GS 6 + 9 regolari GS 2", [6] + [2] * 9, [7] + [2] * 9),
    ("duello del sergente: oggi GS 6 solo (la scorta non entra) / Avanzato GS 7 + 2 veterani GS 5", [6], [7, 5, 5]),
    ("pattuglia e scout insieme (col sergente di oggi / Avanzato)", [5, 5, 5, 2, 2, 2, 6] + [2] * 9, [5, 5, 5, 2, 2, 2, 7] + [2] * 9),
    ("Gorthak GS 12 + 2 troll GS 6 / Gorthak Avanzato GS 13 + 2 troll GS 6", [12, 6, 6], [13, 6, 6]),
    ("Grimjaw GS 14 + 4 orog GS 7", [14, 7, 7, 7, 7], None),
    ("il soffio: Fauci GS 15 + cavaliere GS 10", [15, 10], None),
    ("bugbear: 8 x GS 9", [9] * 8, None),
    ("bugbear con la diversione: 8 x GS 9 + 7 x GS 5", [9] * 8 + [5] * 7, None),
    ("bugbear, diversione e 30 orchi GS 2 tutti insieme / con 15 orchi", [9] * 8 + [5] * 7 + [2] * 30, [9] * 8 + [5] * 7 + [2] * 15),
    ("bugbear e 30 orchi, a diversione caduta", [9] * 8 + [2] * 30, None),
]


LIMITI = """## Limiti delle prove

- Le due colonne del comandante sono due esiti diversi, e una prova sta in
  una sola. «Il comandante fugge»: al suo turno e' sotto la soglia e lascia
  lo scontro in piedi; Gorthak fa prima il suo round in Furia e fugge alla
  fine di quel round (ARC08-DEF-2, «Sotto i 101 pf»). «A 0 pf o meno»: gli
  eroi lo portano a 0 pf o sotto prima che possa fuggire, anche durante il
  round in Furia. «Al primo round» conta tutti e due gli esiti. Fino al
  2026-11-25 una colonna sola, «il comandante fugge», li sommava.
- «A 0 pf o meno» non dice che cosa gli succede: il simulatore non distingue
  chi e' a 0 pf (inabile: un'azione sola a round), chi e' fra -1 e -9
  (morente: privo di sensi, perde 1 pf a round, col 10% di stabilizzarsi) e
  chi e' a -10 o meno (morto) (SRD 3.5, «Injury and Death»). Vale anche per
  «un eroe a terra». Il sergente, Gorthak e Grimjaw non rigenerano e nel
  modello non si curano: la pozione che la scheda da' a Grimjaw sotto i 60
  pf non c'e', perche' sotto 89 e' gia' fuggito.
- I troll dell'ariete rigenerano 5 danni non da fuoco a round, ma un troll a
  0 pf o meno resta fuori fino alla fine del duello. Per l'SRD 3.5
  («Regeneration») i danni che non vengono dal fuoco o dall'acido sono per
  lui non letali: perde i sensi, continua a rigenerare e si rialza. E'
  un'assenza che pende a favore degli eroi. I troll non sono il comandante,
  e le due colonne non li contano.
- I tiri salvezza: l'1 naturale fallisce sempre e il 20 naturale riesce
  sempre (SRD 3.5, «Saving Throws»). Nel modello li tirano solo i nemici,
  sui Riflessi contro il fuoco di Ragnhild.
- Quello che manca agli eroi: la Presenza Comandante di Borin, l'Ispirare
  Coraggio di Nala, la Postura di Borin, gli incantesimi di Harbek e Nala, le
  leve della Sessione 1 contro Gorthak. Sono assenze che pendono contro gli
  eroi: al tavolo i nani fanno un po' meglio di queste cifre.
- Quello che manca ai nemici: il +2 della testa sinistra di Gorthak
  sull'attacco d'opportunita'; l'arco di Grimjaw sui nani in mischia, quando
  sta dietro gli orog; i giganti e gli archi dei veterani su chi sta sulla
  cinta.
- Le guardie vive colpiscono tutte l'eroe piu' ferito fra quelli in mischia:
  e' il caso peggiore.
- Yrsa tira +19/+14/+9, senza la Concentrazione Furiosa; Dara conta il nemico
  prescelto anche a colpire, come sulla scheda di campagna; uno scenario lo
  conta solo ai danni, come l'SRD 3.5.
- Ogni riga ha il suo seme, derivato da --seme, dal titolo e dagli eroi: una
  cifra si muove di un punto o due da un seme all'altro."""


# --- il punto eroe (PF1e, APG): le righe principali, oggi e col punto ---
RIGHE_PUNTO = [
    ("Sergente, oggi (A.4; la scorta non entra)", [["Harbek"], ["Nala"], ["Borin"], ["Yrsa"]]),
    ("Sergente, versione piu' dura: Avanzato + 2 veterani di guardia, si aggirano, dal round 1",
     [["Harbek"], ["Nala"], ["Borin"], ["Yrsa"]]),
    ("Gorthak, oggi, con lo sportello", [["Borin", "Yrsa"], ["Yrsa", "Borin"]]),
    ("Grimjaw e quattro orog, oggi: la guardia si aggira", [["Borin", "Yrsa"]]),
    ("Grimjaw e quattro orog, variante: la rampa chiusa, se ne abbatte uno", [["Borin", "Yrsa"]]),
]
POLITICHE = [(None, "oggi, senza punto"), ("bonus", "+8 al primo tiro per colpire sul comandante"),
             ("azione", "un'azione standard in piu'"), ("movimento", "un'azione di movimento in piu'")]

LIMITI_PUNTO = """## Come leggere queste cifre

- Ogni eroe ha UN punto per i tre giorni d'assedio, non uno per scontro. Qui
  ogni eroe della riga lo spende in quello scontro: la differenza e' il
  massimo che quella politica puo' dare su quello scontro, e sui tre giorni
  l'effetto e' piu' piccolo. Chi lo spende contro il sergente non lo ha piu'
  contro Gorthak o Grimjaw.
- Le tre politiche si provano una alla volta: un punto, un uso.
- La riga «oggi, senza punto» ha lo stesso seme di `esito_simulazione.md` (o
  di `esito_eroi_primi.md` con --eroi-primi) e da' le stesse cifre. Le righe
  col punto partono dallo stesso seme, ma i tiri divergono dal primo colpo:
  una differenza di uno o due punti e' rumore.
- Il +8 vale su un d20 solo: il tiro per colpire, non la conferma del
  critico. Speso dopo il tiro varrebbe +4, e non e' provato.
- Non provati: Agire fuori turno, Ripetere il tiro, Richiamare un
  incantesimo o un uso giornaliero, l'uso Speciale. Ingannare la morte costa
  due punti e nessun eroe li ha.
- Valgono tutti i limiti di `esito_simulazione.md`, compreso il senso delle
  due colonne «il comandante fugge» e «a 0 pf o meno»."""


def confronto_punto_eroe(n, seme, eroi_primi):
    global PUNTO
    scenari = {t: (fn, g) for t, fn, _c, g in SCENARI}
    print(f"# Il punto eroe: {n} duelli per riga, seme {seme}"
          + (", gli eroi agiscono per primi" if eroi_primi else "") + "\n")
    print("Regola opzionale di PF1e (Advanced Player's Guide, «Hero Points»): "
          "https://www.d20pfsrd.com/gamemastering/other-rules/hero-points/\n")
    for titolo, combo in RIGHE_PUNTO:
        fn, giganti = scenari[titolo]
        print(f"## {titolo}\n")
        print("| eroi | politica | il comandante fugge | diff. | a 0 pf o meno | diff. "
              "| al primo round | diff. | un eroe a terra | diff. |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for c in combo:
            base = None
            for politica, nome in POLITICHE:
                PUNTO = politica
                R.seed(f"{seme}|{titolo}|{'+'.join(c)}")
                res = [duello(fn, c, giganti=bool(giganti)) for _ in range(n)]
                chiusi = [r for r in res if r["esito"]]
                v = (sum(1 for r in chiusi if r["esito"] == "fugge") / n,
                     sum(1 for r in chiusi if r["esito"] == "abbattuto") / n,
                     sum(1 for r in chiusi if r["round"] == 1) / n,
                     sum(1 for r in res if r["caduti"] > 0) / n)
                if base is None:
                    base = v
                    dd = [""] * len(v)
                else:
                    dd = [f"{round(x * 100) - round(b * 100):+d}" for x, b in zip(v, base)]
                print(f"| {' + '.join(c)} | {nome} | "
                      + " | ".join(f"{x:.0%} | {q}" for x, q in zip(v, dd)) + " |")
        print()
    PUNTO = None
    print(LIMITI_PUNTO)


def stampa_scenario(titolo, fn, combo, giganti, n, seme):
    print(f"## {titolo}\n")
    print("| eroi | il comandante fugge | a 0 pf o meno | al primo round | round medi alla fuga "
          "| round medi a 0 pf | un eroe a terra | l'eroe piu' ferito, pf medi rimasti |")
    print("|---|---|---|---|---|---|---|---|")
    for c in combo:
        # un seme per riga: correggere uno scenario non sposta le cifre degli altri
        R.seed(f"{seme}|{titolo}|{'+'.join(c)}")
        res = [duello(fn, c, giganti=bool(giganti), ragn_apre=(giganti != "noapre"),
                      dara_srd=(giganti == "dara-srd")) for _ in range(n)]
        fuga = [r["round"] for r in res if r["esito"] == "fugge"]
        zero = [r["round"] for r in res if r["esito"] == "abbattuto"]
        p1 = sum(1 for x in fuga + zero if x == 1) / n
        rf = f"{statistics.mean(fuga):.1f}" if fuga else "–"
        rz = f"{statistics.mean(zero):.1f}" if zero else "–"
        terra = sum(1 for r in res if r["caduti"] > 0) / n
        mf = statistics.mean(r["min_frac"] for r in res)
        print(f"| {' + '.join(c)} | {len(fuga) / n:.0%} | {len(zero) / n:.0%} | {p1:.0%} | {rf} | {rz} "
              f"| {terra:.0%} | {mf:.0%} |")
    print()


# --- la rampa chiusa di Grimjaw: le righe che mancavano (--rampa-chiusa) ---
TITOLO_RAMPA = "Grimjaw e quattro orog, variante: la rampa chiusa, se ne abbatte uno"
TITOLO_FRONTE = "Grimjaw e quattro orog, la rampa chiusa: la chiudono i due orog davanti"
RIGHE_RAMPA = [["Borin"], ["Yrsa"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"],
               ["Harbek", "Nala"], ["Harbek", "Nala", "Ragnhild"], ["Ragnhild"]]

LIMITI_RAMPA = """## Come leggere queste cifre

- La prima tabella ha il titolo e il modello della sezione «la rampa chiusa,
  se ne abbatte uno» di `esito_simulazione.md`: le cinque righe che la' ci
  sono hanno lo stesso seme e danno le stesse cifre; Yrsa, Harbek + Nala e
  Ragnhild da sola sono le tre che mancavano. In quel modello la cima si
  apre appena cade un orog qualunque.
- La seconda tabella prova la regola scritta nel master: la cima la chiudono
  i due orog davanti, e i due dietro sono quelli che si staccano. La cima si
  apre solo quando cade uno dei due davanti; un orog dietro che cade, per il
  fuoco di Ragnhild, non la apre. Ha un altro titolo, quindi un altro seme:
  una differenza di uno o due punti dalla prima tabella e' rumore.
- Ragnhild da sola non sale, e la rampa chiusa non la riguarda: il modello e'
  quello della rampa aperta. Dal round 2 Grimjaw le tira con l'arco, e dal
  round 3 i due orog dietro le arrivano addosso sul camminamento.
- Gli orog non si staccano finche' un nano e' in mischia: l'immagine di Nala
  e l'ordine di Grimjaw contro la palla di fuoco non sono provati.
- Valgono tutti i limiti di `esito_simulazione.md`, compreso il senso delle
  due colonne «il comandante fugge» e «a 0 pf o meno»."""


def confronto_rampa_chiusa(n, seme, eroi_primi):
    print(f"# La rampa chiusa di Grimjaw: {n} duelli per riga, seme {seme}"
          + (", gli eroi agiscono per primi" if eroi_primi else "") + "\n")
    stampa_scenario(TITOLO_RAMPA, grimjaw(muro=1), RIGHE_RAMPA, False, n, seme)
    stampa_scenario(TITOLO_FRONTE, grimjaw(muro=1, fronte=2), RIGHE_RAMPA, False, n, seme)
    print(LIMITI_RAMPA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seme", type=int, default=7)
    ap.add_argument("--eroi-primi", action="store_true",
                    help="gli eroi agiscono sempre prima dei nemici (confronto col quarto giro)")
    ap.add_argument("--punto-eroe", action="store_true",
                    help="confronto sulle righe principali: ogni eroe spende in quello scontro "
                         "il suo punto eroe PF1e (tre politiche, una alla volta)")
    ap.add_argument("--rampa-chiusa", action="store_true",
                    help="Grimjaw a rampa chiusa: le otto combinazioni, col modello di "
                         "esito_simulazione.md e con la cima chiusa dai due orog davanti")
    a = ap.parse_args()
    global EROI_PRIMI
    EROI_PRIMI = a.eroi_primi
    if a.punto_eroe:
        confronto_punto_eroe(a.n, a.seme, a.eroi_primi)
        return
    if a.rampa_chiusa:
        confronto_rampa_chiusa(a.n, a.seme, a.eroi_primi)
        return
    print(f"# {a.n} duelli per riga, seme {a.seme}" + (", gli eroi agiscono per primi" if a.eroi_primi else "") + "\n")
    print("## EL (DMG 3.5)\n")
    print("| scontro | EL prima | EL dopo |")
    print("|---|---|---|")
    for nome, prima, dopo in TABELLA_EL:
        print(f"| {nome} | {el(prima):.1f} | {el(dopo):.1f} |" if dopo else f"| {nome} | {el(prima):.1f} | invariato |")
    print()
    for titolo, fn, combo, giganti in SCENARI:
        stampa_scenario(titolo, fn, combo, giganti, a.n, a.seme)
    print(LIMITI)


if __name__ == "__main__":
    main()
