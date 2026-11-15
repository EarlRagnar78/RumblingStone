#!/usr/bin/env python3
"""Il duello con Skullcrusher (ARC-07 DEF-4, Scena 11): simulazione Monte Carlo.

Domanda di Jfs (15/11/2026): la tattica del drago regge contro le tattiche dei
PG, dalla più probabile alla meno probabile? Il drago è quello di stasera, il
Vecchio dell'Appendice A.1-bis, con le due wyvern dell'Appendice A.6.

Che cosa è dato e che cosa è stimato (vedi LEGGIMI.md):
- Drago e wyvern: numeri delle schede del master, nessuno inventato.
- PG: CA, pf e Riflessi dalla carta del DM del 05/11
  (plans/esperimenti/p16-inferred-2026-11-04/SCHEDE-PG-CARTA.md). I bonus di
  attacco NON sono sulla carta: sono stimati da BAB, caratteristica, bonus
  dell'arma e un talento di Arma Focalizzata, e marcati STIMA. La seconda
  passata (--buff) li alza di 4 per vedere quanto conta la stima.
- Regole: SRD 3.5 e le regole della casa del master (danno massiccio, soffio
  impregnante, corde, Catena a CA 44, soglie di fuga D14).

Uso:
    python3 simula_duello.py                  # tutte le tattiche, 20.000 prove
    python3 simula_duello.py --prove 2000 --seme 7 --buff 4
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field

R = random.Random()
VARIANTI = {"esita": False, "strappa": False}


def d(n: int, f: int) -> int:
    return sum(R.randint(1, f) for _ in range(n))


def colpisce(bonus: int, ca: int) -> bool:
    t = R.randint(1, 20)
    if t == 1:
        return False
    if t == 20:
        return True
    return t + bonus >= ca


# ------------------------------------------------------------------ il drago
DRAGO_PF = 337            # A.1-bis
DRAGO_CA = 40             # 36 + armatura magica, già addosso
DRAGO_CONTATTO = 10
DRAGO_RI = 22
DRAGO_RIFL = 18
DRAGO_VOL = 20
SOGLIA_FUGA = 112         # un terzo dei pf
CATENA_CA = 44            # Q25: CA con armatura magica + 4
SOFFIO_CD = 31            # 16d4, linea 30 m
MORSO = 34                # +20 di colpo accurato quando ha nominato
DISSOLVI = 7              # incantatore di 7°: d20+7

WYVERN_PF = 59            # A.6
WYVERN_CA = 18


@dataclass
class PG:
    nome: str
    pf: int
    ca: int
    rifl: int
    temp: int
    cos: int
    livello: int
    vola: bool = False
    runa_acido: bool = False   # runa di Zeth, resistere all'energia 20
    pf_ora: int = 0
    morto: bool = False
    danni_fatti: int = 0
    acido_dopo: int = 0        # soffio impregnante: metà al round dopo

    def a_terra(self) -> bool:
        return self.pf_ora <= 0

    def subisci(self, danno: int, acido: bool = False) -> int:
        if acido and self.runa_acido:
            danno = max(0, danno - 20)
        if danno <= 0:
            return 0
        self.pf_ora -= danno
        if danno >= 50 and not self.morto:        # danno massiccio, SRD
            if R.randint(1, 20) + self.temp < 15:
                self.morto = True
        if self.pf_ora <= -10:
            self.morto = True
        return danno

    def veleno_wyvern(self) -> None:
        # Tempra CD 17, 2d6 COS: i pf calano col modificatore
        if R.randint(1, 20) + self.temp >= 17:
            return
        prima = (self.cos - 10) // 2
        self.cos -= d(2, 6)
        dopo = (self.cos - 10) // 2
        self.pf_ora -= (prima - dopo) * self.livello
        if self.pf_ora <= -10 or self.cos <= 0:
            self.morto = True


def gruppo(buff: int):
    # STIMA dei bonus d'attacco (BAB + car + arma + 1 di Arma Focalizzata)
    pg = {
        "Thorik": PG("Thorik", 128, 27, 5, 13, 18, 13, runa_acido=True),
        "Tordek": PG("Tordek", 106, 22, 11, 14, 16, 13, runa_acido=True),  # CA 24, −2 in ira
        "Artemis": PG("Artemis", 74, 25, 8, 7, 14, 13, vola=True),
        "Hella": PG("Hella", 80, 25, 7, 11, 12, 13),
    }
    for p in pg.values():
        p.pf_ora = p.pf
    att = {
        # Aegis Fang +2: 13 BAB + 5 FOR + 2 + 1; danno 1d10+2+5+2 (spec.)
        "Thorik": (22 + buff, lambda: d(1, 10) + 9),
        # Bracieri contro i draghi: 13 + 7 (FOR 24 in ira) + 2 + 1; 1d8+9+2d6
        "Tordek": (23 + buff, lambda: d(1, 8) + 9 + d(2, 6)),
    }
    return pg, att


@dataclass
class Esito:
    finale: str = ""
    round: int = 0
    pg_morti: int = 0
    danno_drago: int = 0
    inchiodato: int = 0


def simula(tattica: str, drago_dinamico: bool, buff: int) -> Esito:
    pg, att = gruppo(buff)
    e = Esito()
    drago = DRAGO_PF
    wyv = [WYVERN_PF, WYVERN_PF]
    soffio_pronto = 1            # round in cui il soffio è di nuovo pronto
    nominato = None
    fermo_in_aria = False
    round_extra = False
    fire_seeds, flame_strike = 1, 3
    # le cure di un druido di 12° con SAG 20 (slot di 4° e 3°, STIMA del
    # prepararne metà): 3 cure ferite gravi, 3 moderate, poi la bacchetta (2d8+3)
    cure = ([lambda: d(3, 8) + 12] * 3 + [lambda: d(2, 8) + 10] * 3
            + [lambda: d(2, 8) + 3] * 10)
    dragondoom = 3
    catena_rotta = False
    colpi_round_prima = 0

    # chi vola nelle varie tattiche dei PG
    if tattica in ("T2-tutti-in-volo",):
        for n in ("Thorik", "Tordek", "Hella"):
            pg[n].vola = True
    if tattica == "T3-barile-sul-drago":
        pg["Thorik"].vola = True

    for rnd in range(1, 31):
        e.round = rnd
        colpi = 0
        inchiodato = False
        # acido impregnante del round prima
        for p in pg.values():
            if p.acido_dopo:
                p.subisci(p.acido_dopo, acido=True)
                p.acido_dopo = 0
        vivi = [p for p in pg.values() if not p.a_terra() and not p.morto]
        if not vivi:
            e.finale = "vinto sporco"
            break

        caduti_prima = sum(1 for p in pg.values() if p.a_terra())

        # ---------------------------------------------------- turno del drago
        if drago <= SOGLIA_FUGA:
            if not fermo_in_aria:
                fermo_in_aria = True          # Fluttuare: la prima paura
            elif round_extra or colpi_round_prima < 2:
                e.finale = "ferito grave"
                break
            else:
                round_extra = True
        bersagli = vivi
        if fermo_in_aria:
            # attacco completo da fermo in aria su chi lo ha ferito di più
            t = max(bersagli, key=lambda p: p.danni_fatti)
            seq = ((MORSO, lambda: d(2, 8) + 11), (29, lambda: d(2, 6) + 5),
                   (29, lambda: d(2, 6) + 5), (29, lambda: d(2, 6) + 16))
            if VARIANTI["esita"]:
                seq = ()            # la prima paura: esita, non attacca
            for b, dn in seq:
                if colpisce(b, t.ca):
                    t.subisci(dn())
        elif rnd == 1 or (rnd >= soffio_pronto and R.random() < 0.6):
            # soffio in linea: 1-3 PG a terra (sfalsati su due righe), i volanti
            # solo se allineati; dal round 1 impregnante
            terra = [p for p in bersagli if not p.vola]
            aria = [p for p in bersagli if p.vola]
            pool = terra if len(terra) >= 2 else bersagli
            k = min(len(pool), R.choice((1, 2, 2, 3)))
            presi = R.sample(pool, k)
            impregnante = rnd == 1
            for p in presi:
                dn = d(16, 4)
                if R.randint(1, 20) + p.rifl >= SOFFIO_CD:
                    dn //= 2
                preso = p.subisci(dn, acido=True)
                if impregnante and preso:
                    p.acido_dopo = (dn // 2)
            soffio_pronto = rnd + R.randint(1, 4) + (1 if impregnante else 0)
            del aria
        elif drago_dinamico and sum(1 for p in bersagli if p.vola) >= 2 and R.random() < 0.5:
            # dissolvi magie ad area sui volanti raggruppati (raggio 6 m)
            for p in bersagli:
                if p.vola and p.nome != "Artemis":    # pozione di volare, CD 16
                    if R.randint(1, 20) + DISSOLVI >= 16:
                        p.vola = False                # scende, SRD: di solito illeso
        elif nominato is not None and nominato in bersagli:
            t = nominato
            if colpisce(MORSO + 20, t.ca):
                t.subisci(d(2, 8) + 11)
            nominato = None
            # la picchiata per mordere: occasione delle corde
            if tattica in ("T1-classica", "T3-barile-sul-drago", "T4-la-Catena") and R.random() < 0.5:
                tiratori = [pg[n] for n in ("Tordek", "Thorik") if not pg[n].a_terra() and not pg[n].vola]
                if tiratori and colpisce(13 - 4, DRAGO_CONTATTO):   # gancio, ~2 incrementi
                    forza = 7 if tiratori[0].nome == "Tordek" else 5
                    aiuto = 2 * (len(tiratori) - 1) + 2              # un nano aiuta sempre
                    if R.randint(1, 20) + forza + aiuto >= 25:
                        inchiodato = True
                        e.inchiodato += 1
        else:
            # grida un nome: chi lo ha ferito di più (o un epiteto)
            nominato = max(bersagli, key=lambda p: (p.danni_fatti, R.random()))

        # --------------------------------------------- le wyvern, dal round 2
        if rnd >= 2:
            for i in range(2):
                if wyv[i] <= 0:
                    continue
                aria = [p for p in pg.values() if p.vola and not p.a_terra()]
                terra = [p for p in pg.values() if not p.vola and not p.a_terra()
                         and p.nome in ("Tordek", "Thorik")]
                if i == 0 and aria:
                    t = R.choice(aria)
                    if colpisce(10, t.ca):            # pungiglione in passata
                        t.subisci(d(1, 6) + 4)
                        t.veleno_wyvern()
                elif terra:
                    t = terra[0]
                    if colpisce(10, t.ca):
                        t.subisci(d(1, 6) + 4)
                        t.veleno_wyvern()
                    if colpisce(8, t.ca):
                        t.subisci(d(2, 8) + 4)
                    for _ in range(2):
                        if colpisce(8, t.ca):
                            t.subisci(d(1, 8) + 2)
                        if colpisce(8, t.ca):
                            t.subisci(d(2, 6) + 2)

        legati = [pg[n] for n in ("Tordek", "Thorik") if not pg[n].a_terra()]
        if inchiodato and legati and not VARIANTI["strappa"]:
            # a terra un round: attacco completo su chi tiene la corda
            t = legati[0]
            for b, dn in ((MORSO, lambda: d(2, 8) + 11), (29, lambda: d(2, 6) + 5),
                          (29, lambda: d(2, 6) + 5), (29, lambda: d(1, 8) + 5),
                          (29, lambda: d(1, 8) + 5), (29, lambda: d(2, 6) + 16)):
                if colpisce(b, t.ca):
                    t.subisci(dn())

        # ---------------------------------------------------- turno dei PG
        def danno(p: PG, n: int) -> None:
            nonlocal drago, colpi
            if n > 0:
                drago -= n
                p.danni_fatti += n
                colpi += 1

        art = pg["Artemis"]
        if not art.a_terra() and wyv[0] > 0 and rnd >= 2:
            # la wyvern che la punge le sta addosso: prima quella (niente RI)
            if colpisce(13, 10):
                wyv[0] -= d(9, 6)
        elif not art.a_terra():
            # deflagrazione occulta 7d6 + 1d6 fuoco + 1d6 freddo, contatto a distanza
            if colpisce(13, DRAGO_CONTATTO) and R.randint(1, 20) + 13 >= DRAGO_RI:
                danno(art, d(9, 6))

        hel = pg["Hella"]
        if not hel.a_terra():
            feriti = [p for p in pg.values() if not p.morto and p.pf_ora < p.pf * 0.5]
            if feriti and cure:
                f = min(feriti, key=lambda p: p.pf_ora)
                f.pf_ora = min(f.pf, f.pf_ora + cure.pop(0)())
            elif fire_seeds:
                fire_seeds -= 1                               # semi di fuoco: RI no
                if colpisce(11, DRAGO_CONTATTO):
                    danno(hel, d(12, 6))
            elif flame_strike:
                flame_strike -= 1                             # colpo infuocato 12d6
                if R.randint(1, 20) + 12 >= DRAGO_RI:
                    n = d(12, 6)
                    if R.randint(1, 20) + DRAGO_RIFL >= 20:
                        n //= 2
                    danno(hel, n)

        for n in ("Thorik", "Tordek"):
            p = pg[n]
            if p.a_terra():
                continue
            b, dn = att[n]
            if inchiodato:
                n_att = (b, b - 5, b - 10)
                for i, bb in enumerate(n_att):
                    if tattica == "T4-la-Catena" and i == 0:
                        if colpisce(bb, CATENA_CA):
                            catena_rotta = True
                        continue
                    if colpisce(bb, DRAGO_CA):
                        x = dn()
                        if n == "Thorik" and dragondoom:
                            dragondoom -= 1
                            x += d(2, 6)
                        danno(p, x)
            elif wyv[1] > 0 and rnd >= 2 and not p.vola:
                # la wyvern è addosso: la si abbatte
                for bb in (b, b - 5, b - 10):
                    if colpisce(bb, WYVERN_CA):
                        wyv[1] -= dn()
            elif wyv[0] > 0 and rnd >= 2 and p.vola:
                for bb in (b, b - 5, b - 10):
                    if colpisce(bb, WYVERN_CA):
                        wyv[0] -= dn()
            elif n == "Thorik" and not p.vola and R.random() < 0.3:
                # Aegis Fang scagliata a 15 m: −4 e quattro incrementi interi
                if colpisce(b - 4 - 8, DRAGO_CA):
                    danno(p, dn())
            # altrimenti prepara la corda per il round dopo

        if tattica == "T3-barile-sul-drago" and inchiodato and not pg["Thorik"].a_terra():
            # Thorik, in volo sopra la verticale, lascia cadere la botte: 15d6
            # (oggetto in caduta, SRD) e le due palle di fuoco da 6d6 (Riflessi CD 14)
            n = d(15, 6)
            for _ in range(2):
                f = d(6, 6)
                if R.randint(1, 20) + DRAGO_RIFL >= 14:
                    f //= 2
                n += f
            danno(pg["Thorik"], n)

        colpi_round_prima = colpi
        if catena_rotta:
            e.finale = "Catena spezzata: ferito grave" if drago <= DRAGO_PF - 112 else "Catena spezzata: fuggito"
            break
        if drago <= 0:
            e.finale = "ucciso"
            break
        caduti = sum(1 for p in pg.values() if p.a_terra())
        if caduti - caduti_prima >= 2:
            e.finale = "vinto sporco"
            break
    else:
        e.finale = "senza esito (30 round)"
    e.pg_morti = sum(1 for p in pg.values() if p.morto)
    e.danno_drago = DRAGO_PF - max(drago, 0)
    return e


TATTICHE = [
    ("T1-classica", "nel cortile: Artemis vola e deflagra, Hella lancia e cura, Thorik e Tordek alle corde"),
    ("T4-la-Catena", "come T1, ma nei round a terra il primo colpo va sulla runa (CA 44)"),
    ("T2-tutti-in-volo", "pozioni di volare per Thorik, Tordek e Hella"),
    ("T3-barile-sul-drago", "come T1, e Thorik in volo con la botte sopra il drago inchiodato"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prove", type=int, default=20000)
    ap.add_argument("--seme", type=int, default=1372)
    ap.add_argument("--esita", action="store_true", help="alla prima paura non fa l'attacco completo")
    ap.add_argument("--strappa", action="store_true", help="inchiodato, passa il round a liberare l'ala")
    ap.add_argument("--buff", type=int, default=0, help="bonus d'attacco in più a Thorik e Tordek")
    a = ap.parse_args()
    R.seed(a.seme)
    VARIANTI["esita"], VARIANTI["strappa"] = a.esita, a.strappa
    for drago_din in (False, True):
        print(f"\n### Drago {'con la tabella dinamica (dissolvi sui volanti)' if drago_din else 'del canone di oggi'}"
              f" · prove {a.prove} · buff {a.buff}\n")
        print("| Tattica dei PG | ucciso | ferito grave | Catena | vinto sporco | almeno un PG morto | round | danno al drago | round inchiodato |")
        print("|---|---|---|---|---|---|---|---|---|")
        for t, _ in TATTICHE:
            es = [simula(t, drago_din, a.buff) for _ in range(a.prove)]
            n = len(es)
            def pc(f):
                return f"{100 * sum(1 for x in es if f(x)) / n:.0f}%"
            print(f"| {t} | {pc(lambda x: x.finale == 'ucciso')} | {pc(lambda x: x.finale == 'ferito grave')} | "
                  f"{pc(lambda x: x.finale.startswith('Catena'))} | {pc(lambda x: x.finale == 'vinto sporco')} | "
                  f"{pc(lambda x: x.pg_morti > 0)} | {sum(x.round for x in es) / n:.1f} | "
                  f"{sum(x.danno_drago for x in es) / n:.0f} | {sum(x.inchiodato for x in es) / n:.2f} |")


if __name__ == "__main__":
    main()
