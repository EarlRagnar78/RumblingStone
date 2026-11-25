#!/usr/bin/env python3
"""Simula i duelli dei pregen di ARC-08 (DEF-1 Scena 8, DEF-2 Scene 2 e 4),
con le schede di oggi e con l'archetipo Avanzato. Quarto giro, 2026-11-25.

Modello semplice, 3.5 (Yrsa PF1e com'e' la sua scheda):
- attacchi con d20 contro CA, minaccia di critico confermata con un secondo
  tiro, moltiplicatore pieno sui dadi e sui bonus fissi (SRD);
- incantesimi ad area con Riflessi per dimezzare (eludere dove c'e');
- la rigenerazione dei troll toglie 5 danni non da fuoco a round;
- il comandante fugge sotto meta' dei pf (libretto §5); Gorthak prima fa un
  round in Furia (A.1);
- la guardia (i veterani del sergente, gli orog di Grimjaw): per arrivare al
  comandante l'eroe passa accanto a una guardia, prende il suo attacco
  d'opportunita' e fa un attacco solo in quel round (SRD); poi attacco completo;
- il ponte di Gorthak (MAPPA 2A): un eroe esce a round dallo sportello, prende
  l'attacco d'opportunita' di Gorthak e fa un attacco solo; il primo va in
  BG75, il secondo resta in BG74, e il troll non ha attacchi d'opportunita';
  Gorthak divide i colpi: il primo randello su Borin se c'e', l'altro su
  chi e' piu' ferito fra gli altri;
- la Sfida di Yrsa vale quando lei minaccia il bersaglio (Ordine del Drago);
- la Presenza intimidatoria di Grimjaw: Volontà CD 19, o -2 a colpire;
- Ragnhild, se apre, lancia prima che esca un nano.
Limiti: gli eroi agiscono sempre per primi; niente movimento oltre lo
sportello e la guardia, niente copertura; la CA di Gorthak in Furia non conta
(fugge alla fine di quel round); gli incantesimi di Harbek e Nala non ci sono.

Numeri: ARC08-01, ARC08-02 §3, Appendici A di ARC08-DEF-1 e ARC08-DEF-2,
Bestiario. L'archetipo semplice Avanzato di PF1e, regole rapide
(+2 a tutti i tiri e ai danni, +4 CA, +2 pf per DV).

Uso: python3 simula_scontri_epici.py [--n 4000] [--seme 7]
"""
import argparse
import random
import statistics

R = random.Random(7)


def d(n, f):
    return sum(R.randint(1, f) for _ in range(n))


def colpo(bonus, ca, dadi, fisso, minaccia=20, molt=2, extra=None):
    """Un attacco. Ritorna i danni (0 se manca). extra: dadi in piu' che non
    si moltiplicano (furtivo, Colpo Devastante)."""
    t = R.randint(1, 20)
    if t == 1 or (t != 20 and t + bonus < ca):
        return 0
    n, f = dadi
    crit = t >= minaccia and (R.randint(1, 20) + bonus >= ca)
    volte = molt if crit else 1
    dmg = sum(d(n, f) + fisso for _ in range(volte))
    if extra:
        dmg += d(*extra)
    return max(1, dmg)


def riflessi(base_dmg, ts, cd, eludere=False):
    ok = R.randint(1, 20) + ts >= cd
    if eludere:
        return 0 if ok else base_dmg
    return base_dmg // 2 if ok else base_dmg


class Nemico:
    def __init__(self, nome, pf, ca, attacchi, rifl, rigen=0, fuga=None,
                 entra=1, primo=None, ruolo="scorta"):
        self.nome, self.pfmax, self.pf, self.ca = nome, pf, pf, ca
        self.attacchi, self.rifl, self.rigen = attacchi, rifl, rigen
        self.fuga, self.entra, self.primo, self.ruolo = fuga, entra, primo, ruolo
        self.giu = False

    def danno(self, n, fuoco=False):
        self.pf -= n
        if self.rigen and not fuoco:
            self.nonfuoco = getattr(self, "nonfuoco", 0) + n
        if self.pf <= 0:
            self.giu = True


# --- i pregen (ARC08-02 §3, ARC08-01) ---------------------------------
EROI = {
    "Borin": dict(vol=8, pf=142, ca=25, melee=[(21, (1, 8), 9, 20, 3), (16, (1, 8), 9, 20, 3), (11, (1, 8), 9, 20, 3)], devastante=3),
    "Yrsa": dict(vol=10, pf=114, ca=32, melee=[(23, (1, 10), 18, 20, 3), (14, (1, 10), 18, 20, 3), (9, (1, 10), 18, 20, 3)], sfida=18),
    "Nala": dict(vol=9, pf=90, ca=20, melee=[(13, (1, 6), 3, 15, 2), (8, (1, 6), 3, 15, 2)]),
    "Harbek": dict(vol=16, pf=114, ca=22, melee=[(13, (1, 8), 5, 20, 3), (8, (1, 8), 5, 20, 3)]),
    # Dara dalla torre: Tiro Rapido +17/+17/+12/+7, +4 contro i giganti, -2 per la distanza
    "Dara": dict(vol=9, pf=102, ca=21, arco=True),
    "Ragnhild": dict(vol=14, pf=84, ca=18, maga=True),
}


def eroe(nome):
    e = dict(EROI[nome])
    e["nome"], e["pfcur"] = nome, e["pf"]
    return e


def duello(nemici_fn, eroi_nomi, giganti=False, round_max=8, ragn_apre=True):
    """ragn_apre: Ragnhild apre con le due palle di fuoco prima che un nano sia
    in mischia; se False, usa i raggi roventi."""
    nemici = nemici_fn()
    boss = [n for n in nemici if n.ruolo == "boss"][0]
    eroi = [eroe(n) for n in eroi_nomi]
    mischia = [e for e in eroi if "melee" in e]
    for i, e in enumerate(mischia):
        e["_entra"] = i + 1
    yrsa = [e for e in eroi if e["nome"] == "Yrsa"]
    sportello = getattr(boss, "sportello", False)

    def sfida(rnd):
        # la Sfida chiede che Yrsa minacci il bersaglio: sul ponte vale dal round
        # in cui esce dallo sportello, e dietro una guardia da quando l'ha aggirata
        if not yrsa or yrsa[0]["pfcur"] <= 0:
            return False
        if sportello:
            return rnd >= yrsa[0]["_entra"]
        # dietro la guardia: finche' Yrsa non gli e' arrivata accanto, niente
        if getattr(boss, "guardato", False) and not yrsa[0].get("_passato"):
            return False
        return True
    # la Presenza intimidatoria (Grimjaw): Volontà, o -2 a colpire per il duello
    for e in eroi:
        cd = getattr(boss, "presenza", 0)
        e["_pres"] = 2 if cd and R.randint(1, 20) + e["vol"] < cd else 0
    # Ragnhild, se apre, lancia prima che esca un nano: va per prima
    ordine = sorted(eroi, key=lambda e: 0 if e.get("maga") else 1)
    min_frac = 1.0
    caduti = set()
    for rnd in range(1, round_max + 1):
        # --- gli eroi (si assume che agiscano per primi: iniziativa di gruppo)
        for e in ordine:
            if e["pfcur"] <= 0:
                continue
            vivi = [n for n in nemici if not n.giu and n.entra <= rnd]
            if not vivi:
                break
            if e.get("maga"):
                if rnd == 1 and ragn_apre:
                    for n in vivi:  # ritardata 13d6 CD 26 + rapida 10d6 CD 22
                        n.danno(riflessi(d(13, 6), n.rifl, 26, getattr(n, "eludere", False)), fuoco=True)
                        n.danno(riflessi(d(10, 6), n.rifl, 22, getattr(n, "eludere", False)), fuoco=True)
                else:
                    # tre raggi roventi, 4d6 a raggio, contatto a distanza +8
                    bersaglio = boss if not boss.giu else vivi[0]
                    for _ in range(3):
                        bersaglio.danno(colpo(8, getattr(bersaglio, "contatto", 11), (4, 6), 0), fuoco=True)
                continue
            if e.get("arco"):
                b = boss if not boss.giu and boss.entra <= rnd else vivi[0]
                gb = 4 if giganti else 0
                for bon in (17, 17, 12, 7):
                    b.danno(colpo(bon + gb - 2, b.ca, (1, 8), 6 + gb, 20, 3))
                continue
            # mischia: tutti sul boss se e' entrato, se no sul primo
            b = boss if not boss.giu and boss.entra <= rnd else vivi[0]
            # la guardia: per arrivare al comandante si passa accanto a una
            # guardia viva: il suo attacco d'opportunita', e un attacco solo
            colpi = e["melee"]
            muro = getattr(b, "muro", 0)
            if muro and b is boss:
                # variante: la rampa e' chiusa, e per arrivare al comandante si
                # abbattono prima `muro` guardie
                scorte = [n for n in vivi if n.ruolo == "scorta"]
                if len(scorte) > len([n for n in nemici if n.ruolo == "scorta"]) - muro:
                    b = scorte[0]
            elif getattr(b, "guardato", False) and not e.get("_passato"):
                scorte = [n for n in vivi if n.ruolo == "scorta"]
                if scorte:
                    (bon2, dadi2, f2, mn2, ml2, _t) = scorte[0].attacchi[0]
                    e["pfcur"] -= colpo(bon2, e["ca"], dadi2, f2, mn2, ml2)
                    if e["pfcur"] <= 0:
                        caduti.add(e["nome"])
                        continue
                    colpi = colpi[:1]
                e["_passato"] = True
            bonus_sfida = 4 if (sfida(rnd) and e["nome"] != "Yrsa" and b is boss) else 0
            ca_b = b.ca - (2 if (sfida(rnd) and e["nome"] != "Yrsa" and b is boss) else 0)
            # lo sportello (MAPPA 2A, BG73): gli eroi in mischia escono uno per
            # round e solo due stanno accanto a Gorthak (BG74, BG75); chi esce
            # muove (un attacco solo) e prende l'attacco d'opportunita' di Gorthak
            # (portata 3 m, senza Riflessi in Combattimento: uno a round)
            if getattr(b, "sportello", False):
                if rnd < e["_entra"]:
                    continue
                if rnd == e["_entra"]:
                    colpi = colpi[:1]
                    # il primo va in BG75, il secondo resta in BG74: nessun
                    # artiglio di troll (al round 1 hanno le mani sul tronco)
                    aoo = [boss.attacchi[0]] if not boss.giu else []
                    for (bon2, dadi2, f2, mn2, ml2, _t) in aoo:
                        e["pfcur"] -= colpo(bon2, e["ca"], dadi2, f2, mn2, ml2)
                    if e["pfcur"] <= 0:
                        caduti.add(e["nome"])
                        continue
            for i, (bon, dadi, fisso, mn, ml) in enumerate(colpi):
                if b.giu:
                    break
                extra = None
                if e.get("devastante") and i == 0 and e.get("_dev", 0) < e["devastante"]:
                    e["_dev"] = e.get("_dev", 0) + 1
                    extra = (4, 6)
                f = fisso
                if e.get("sfida") and b is boss:
                    f = fisso + e["sfida"]  # la Sfida (+18) vale solo sul bersaglio sfidato, il boss
                b.danno(colpo(bon + bonus_sfida - e["_pres"], ca_b, dadi, f, mn, ml, extra))
        in_furia = False
        if boss.pf < boss.fuga:
            # Gorthak: sotto meta' un round in Furia, poi fugge (A.1; ARC08-02)
            if boss.giu or not getattr(boss, "furia", None):
                return dict(fuga=True, round=rnd, min_frac=min_frac, caduti=len(caduti))
            in_furia = True
        # --- rigenerazione
        for n in nemici:
            if n.rigen and getattr(n, "nonfuoco", 0) > 0:
                r = min(n.rigen, n.nonfuoco)
                n.nonfuoco -= r
                n.pf += r
                if n.pf > 0:
                    n.giu = False
        # --- i nemici
        bersagli = [e for e in mischia if e["pfcur"] > 0 and e["_entra"] <= rnd]
        if not bersagli:
            bersagli = [e for e in eroi if e["pfcur"] > 0 and not e.get("arco") and not e.get("maga")]
        if not bersagli:
            bersagli = [e for e in eroi if e["pfcur"] > 0]
        if not bersagli:
            return dict(fuga=False, round=rnd, min_frac=0, caduti=len(eroi))
        for n in [x for x in nemici if not x.giu and x.entra <= rnd]:
            if n.ruolo == "ariete" and rnd == 1:
                continue
            vivi_b = [e for e in bersagli if e["pfcur"] > 0]
            if not vivi_b:
                break
            # il piu' ferito, in proporzione (la testa destra; i sicari)
            t = min(vivi_b, key=lambda e: e["pfcur"] / e["pf"])
            seq = n.primo if (n.primo is not None and rnd == n.entra) else n.attacchi
            if n is boss and in_furia:
                seq = boss.furia
            colpi_artiglio = 0
            bersaglio_di = [t] * len(seq)
            if n is boss and sportello and len(vivi_b) >= 2 and len(seq) == 6:
                # sei colpi divisi fra due: il primo randello su Borin se c'e'
                # (la testa sinistra), l'altro sul piu' ferito degli altri
                primo_b = next((e for e in vivi_b if e["nome"] == "Borin"), t)
                altri = [e for e in vivi_b if e is not primo_b]
                secondo_b = min(altri, key=lambda e: e["pfcur"] / e["pf"])
                bersaglio_di = [primo_b] * 3 + [secondo_b] * 3
            for (bon, dadi, fisso, mn, ml, tag), tt in zip(seq, bersaglio_di):
                ca_tt = tt["ca"] - (2 if (tt["nome"] == "Yrsa" and n is not boss and sfida(rnd)) else 0)
                x = colpo(bon, ca_tt, dadi, fisso, mn, ml)
                if x and tag == "artiglio":
                    colpi_artiglio += 1
                tt["pfcur"] -= x
                if tt["pfcur"] <= 0:
                    caduti.add(tt["nome"])
            if colpi_artiglio == 2 and getattr(n, "sbranare", None):
                t["pfcur"] -= d(*n.sbranare[0]) + n.sbranare[1]
            if t["pfcur"] <= 0:
                caduti.add(t["nome"])
        for e in eroi:
            min_frac = min(min_frac, max(0, e["pfcur"]) / e["pf"])
        if in_furia:
            return dict(fuga=True, round=rnd, min_frac=min_frac, caduti=len(caduti))
        if all(e["pfcur"] <= 0 for e in eroi):
            return dict(fuga=False, round=rnd, min_frac=0, caduti=len(eroi))
    return dict(fuga=False, round=round_max, min_frac=min_frac, caduti=len(caduti))


# --- i nemici ----------------------------------------------------------
A = lambda b, dadi, f, mn=20, ml=2, tag="": (b, dadi, f, mn, ml, tag)


def sergente(avanzato=False, veterani=0, entra=2, guardia=0):
    def fn():
        k = 2 if avanzato else 0
        s = Nemico("sergente", 62 if avanzato else 50, 25 if avanzato else 21,
                   [A(9 + k, (1, 8), 6 + k, 19), A(4 + k, (1, 8), 6 + k, 19),
                    A(9 + k, (1, 8), 3 + k, 19), A(4 + k, (1, 8), 3 + k, 19)],
                   rifl=6 + k, fuga=(62 if avanzato else 50) / 2, ruolo="boss")
        s.guardato = bool(guardia)
        out = [s]
        for i in range(veterani):  # hobgoblin veterani, Bestiario, GS 5
            out.append(Nemico(f"veterano{i}", 43, 19, [A(10, (1, 8), 2, 19), A(5, (1, 8), 2, 19)],
                              rifl=4, entra=entra))
        return out
    return fn


def gorthak(avanzato=False, troll_avanzati=False, sportello=True):
    def fn():
        k = 2 if avanzato else 0
        pf = 232 if avanzato else 202
        g = Nemico("Gorthak", pf, 29 if avanzato else 25,
                   [A(21 + k, (2, 6), 10 + k), A(16 + k, (2, 6), 10 + k), A(11 + k, (2, 6), 10 + k),
                    A(21 + k, (2, 6), 5 + k), A(16 + k, (2, 6), 5 + k), A(11 + k, (2, 6), 5 + k)],
                   rifl=7 + k, fuga=pf / 2, ruolo="boss")
        # niente carica al round 1: e' gia' adiacente a chi esce in BG74, e la
        # carica vuole almeno 3 m di movimento; agisce dopo l'eroe, attacco completo
        g.contatto = 15 if avanzato else 11
        # Furia (+4 For): +2 a colpire, +2 ai danni del braccio forte, +1 dell'altro
        g.furia = [A(23 + k, (2, 6), 12 + k), A(18 + k, (2, 6), 12 + k), A(13 + k, (2, 6), 12 + k),
                   A(23 + k, (2, 6), 6 + k), A(18 + k, (2, 6), 6 + k), A(13 + k, (2, 6), 6 + k)]
        g.sportello = sportello
        out = [g]
        t = 2 if troll_avanzati else 0
        for i in range(2):
            tr = Nemico(f"troll{i}", 125 if troll_avanzati else 105, 20 if troll_avanzati else 16,
                        [A(13 + t, (1, 6), 7 + t, tag="artiglio"), A(13 + t, (1, 6), 7 + t, tag="artiglio"),
                         A(8 + t, (1, 6), 3 + t)], rifl=5 + t, rigen=5, ruolo="ariete")
            tr.sbranare = ((2, 6), 10 + t)
            out.append(tr)
        return out
    return fn


def grimjaw(orog_avanzati=False, muro=0):
    def fn():
        # dal round 2 in Furia Comandante: +24/+19/+14 (1d10+11, 17-20); round 1 non attacca
        g = Nemico("Grimjaw", 178, 26, [A(24, (1, 10), 11, 17), A(19, (1, 10), 11, 17), A(14, (1, 10), 11, 17)],
                   rifl=8, fuga=89, ruolo="boss", entra=1,
                   primo=[])  # round 1: Tattico Superiore e Presenza, nessun attacco
        g.guardato = True  # la guardia: per arrivare a lui si passa accanto a un orog
        g.muro = muro
        g.presenza = 19
        out = [g]
        o = 2 if orog_avanzati else 0
        for i in range(4):
            # Attacco Poderoso -3, Furia Comandante +2/+2, Tattico Superiore +2 a colpire
            out.append(Nemico(f"orog{i}", 75 if orog_avanzati else 63, 23 if orog_avanzati else 19,
                              [A(14 + o, (1, 12), 18 + o, 20, 3), A(9 + o, (1, 12), 18 + o, 20, 3)],
                              rifl=2 + o, primo=[A(12 + o, (1, 12), 16 + o, 20, 3), A(7 + o, (1, 12), 16 + o, 20, 3)]))
        return out
    return fn


SCENARI = [
    ("Sergente, oggi (solo: la scorta non entra)", sergente(), [["Borin"], ["Yrsa"], ["Nala"], ["Harbek"]], False),
    ("Sergente, versione piu' dura: Avanzato + 2 veterani in muro dal round 1", sergente(True, 2, 1, 2), [["Borin"], ["Yrsa"], ["Nala"], ["Harbek"], ["Borin", "Yrsa"]], False),
    ("Sergente, variante scartata A: Avanzato + 4 veterani dal round 2", sergente(True, 4), [["Borin"], ["Yrsa"], ["Nala"], ["Harbek"]], False),
    ("Sergente, variante scartata B: Avanzato + 4 veterani in muro dal round 1", sergente(True, 4, 1, 3), [["Borin"], ["Yrsa"], ["Nala"], ["Harbek"], ["Borin", "Yrsa"]], False),
    ("Gorthak, oggi, senza lo sportello (riferimento del primo giro)", gorthak(sportello=False), [["Borin"], ["Borin", "Yrsa"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"], ["Borin", "Yrsa", "Ragnhild"]], True),
    ("Gorthak, oggi, con lo sportello", gorthak(), [["Borin"], ["Borin", "Yrsa"], ["Yrsa", "Borin"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"], ["Borin", "Yrsa", "Ragnhild"], ["Harbek", "Nala"], ["Harbek", "Nala", "Dara"]], True),
    ("Gorthak, versione piu' dura (Avanzato), con lo sportello", gorthak(True), [["Borin"], ["Borin", "Yrsa"], ["Yrsa", "Borin"], ["Borin", "Dara"], ["Borin", "Yrsa", "Dara"], ["Borin", "Yrsa", "Ragnhild"]], True),
    ("Gorthak Avanzato con lo sportello, Ragnhild senza l'apertura", gorthak(True), [["Borin", "Yrsa", "Ragnhild"]], "noapre"),
    ("Gorthak e troll tutti Avanzati, con lo sportello (scartato)", gorthak(True, True), [["Borin", "Yrsa"], ["Borin", "Dara"]], True),
    ("Grimjaw e quattro orog, oggi", grimjaw(), [["Borin"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"]], False),
    ("Grimjaw e quattro orog, variante: la rampa chiusa, se ne abbatte uno", grimjaw(muro=1), [["Borin"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"]], False),
    ("Grimjaw, orog Avanzati (scartato)", grimjaw(True), [["Borin"], ["Borin", "Yrsa"], ["Borin", "Yrsa", "Harbek"], ["Borin", "Yrsa", "Ragnhild"]], False),
]


def el(gs):
    """EL della DMG 3.5: 2 log2(somma di 2^(GS/2)), come scripts/suggest_encounter.py."""
    import math
    return 2 * math.log2(sum(2 ** (g / 2) for g in gs))


TABELLA_EL = [
    ("pattuglia: 3 cavalcatori GS 5 (+3 worg GS 2)", [5, 5, 5, 2, 2, 2], None),
    ("scout: sergente GS 6 + 9 regolari GS 2", [6] + [2] * 9, [7] + [2] * 9),
    ("duello del sergente: oggi GS 6 solo (la scorta non entra) / Avanzato GS 7 + 2 veterani GS 5", [6], [7, 5, 5]),
    ("pattuglia e scout insieme (col sergente di oggi / Avanzato)", [5, 5, 5, 2, 2, 2, 6] + [2] * 9, [5, 5, 5, 2, 2, 2, 7] + [2] * 9),
    ("Gorthak GS 12 + 2 troll GS 6 / Gorthak Avanzato GS 13 + 2 troll GS 6", [12, 6, 6], [13, 6, 6]),
    ("Grimjaw GS 14 + 4 orog GS 7", [14, 7, 7, 7, 7], None),
    ("il soffio: Fauci GS 15 + cavaliere GS 10", [15, 10], None),
    ("bugbear: 8 x GS 9 (+ 7 hobgoblin GS 5)", [9] * 8, None),
    ("bugbear con la diversione: 8 x GS 9 + 7 x GS 5", [9] * 8 + [5] * 7, None),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4000)
    ap.add_argument("--seme", type=int, default=7)
    a = ap.parse_args()
    R.seed(a.seme)
    print(f"# {a.n} duelli per riga, seme {a.seme}\n")
    print("## EL (DMG 3.5)\n")
    print("| scontro | EL prima | EL dopo |")
    print("|---|---|---|")
    for nome, prima, dopo in TABELLA_EL:
        print(f"| {nome} | {el(prima):.1f} | {el(dopo):.1f} |" if dopo else f"| {nome} | {el(prima):.1f} | invariato |")
    print()
    for titolo, fn, combo, giganti in SCENARI:
        print(f"## {titolo}\n")
        print("| eroi | il comandante fugge | round medi alla fuga | un eroe a terra | l'eroe piu' ferito, pf medi rimasti |")
        print("|---|---|---|---|---|")
        for c in combo:
            res = [duello(fn, c, giganti=bool(giganti), ragn_apre=(giganti != "noapre")) for _ in range(a.n)]
            fuga = [r for r in res if r["fuga"]]
            pf = sum(1 for r in res if r["fuga"]) / a.n
            rmed = statistics.mean(r["round"] for r in fuga) if fuga else float("nan")
            terra = sum(1 for r in res if r["caduti"] > 0) / a.n
            mf = statistics.mean(r["min_frac"] for r in res)
            print(f"| {' + '.join(c)} | {pf:.0%} | {rmed:.1f} | {terra:.0%} | {mf:.0%} |")
        print()


if __name__ == "__main__":
    main()
