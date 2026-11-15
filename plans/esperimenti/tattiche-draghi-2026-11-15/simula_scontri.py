#!/usr/bin/env python3
"""Tattiche dei draghi (e poi di villain e PNG): simulazione Monte Carlo generica.

Nasce da simula_duello.py di Skullcrusher (15/11/2026) e lo generalizza: un
motore unico, e per ogni creatura un PROFILO (i numeri della sua scheda) e una o
più POLITICHE (la tattica del canone di oggi e quella proposta).

Che cosa è dato e che cosa è stimato:
- Creature: i numeri delle schede del repo, citate nel profilo. Nessun numero
  inventato; quando la scheda non lo dice, il profilo lo segna STIMA.
- PG: CA, pf, TS dalla carta del DM del 05/11
  (plans/esperimenti/p16-inferred-2026-11-04/SCHEDE-PG-CARTA.md). STIMA: i
  bonus d'attacco di Thorik e Tordek (non sono sulla carta), le cure preparate
  da Hella, l'arco di Tordek. --buff alza i bonus di Thorik e Tordek per
  vedere quanto pesa la stima.
- Fuori dal modello, sempre: alleati, evocati, pozioni, terreno a quadretti.
  Aiutano i PG, quindi i morti sono un tetto, non una previsione.

Regole (SRD 3.5): presenza terrificante (scosso, −2), immagine speculare
(le immagini prendono i colpi con probabilità immagini/(immagini+1)),
invisibilità superiore (50% di mancare; *luminescenza* di Hella la toglie se
supera la RI), pelle di pietra (RD 10/adamantio sulle armi, tetto 10 × LI),
danno massiccio, −10 morto.

Uso:
    python3 simula_scontri.py                       # tutti gli scontri
    python3 simula_scontri.py --scontro fauci --prove 5000
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field

R = random.Random()


def d(n: int, f: int) -> int:
    return sum(R.randint(1, f) for _ in range(n))


def tira(bonus: int, ca: int) -> bool:
    t = R.randint(1, 20)
    return t != 1 and (t == 20 or t + bonus >= ca)


def ts(bonus: int, cd: int) -> bool:
    t = R.randint(1, 20)
    return t != 1 and (t == 20 or t + bonus >= cd)


# ===================================================================== PG
@dataclass
class PG:
    nome: str
    pf: int
    ca: int
    temp: int
    rifl: int
    vol: int
    immune_paura: bool = False      # Thorik: vuoto mentale della Corona
    vola: bool = False
    leggero: bool = False           # sollevabile e scagliabile (Artemis)
    pf_ora: int = 0
    morto: bool = False
    scosso: int = 0                 # round rimasti
    nauseato: int = 0
    invisibile: int = 0
    fuori: int = 0                  # round fuori gioco (scagliato, in bocca)
    charmato: bool = False
    resist: int = 0                 # resistere all'energia contro il soffio (T3-preparati)
    danni_fatti: int = 0
    round_persi: int = 0            # metrica del terrore

    def giu(self) -> bool:
        return self.morto or self.pf_ora <= 0

    def subisci(self, n: int) -> int:
        if n <= 0 or self.morto:
            return 0
        self.pf_ora -= n
        if n >= 50 and not ts(self.temp, 15):
            self.morto = True
        if self.pf_ora <= -10:
            self.morto = True
        return n

    def pen(self) -> int:
        return -2 if self.scosso > 0 else 0


def gruppo(buff: int = 0, eb_dadi: int = 7):
    """La carta del 05/11. Thorik con le decisioni del DM (CA 27, 128 pf)."""
    g = {
        "Thorik": PG("Thorik", 128, 27, 13, 5, 11, immune_paura=True),
        "Tordek": PG("Tordek", 106, 22, 14, 11, 12),   # CA 24, −2 in ira
        "Artemis": PG("Artemis", 74, 25, 7, 8, 8, vola=True, leggero=True),
        "Hella": PG("Hella", 80, 25, 11, 7, 13),
    }
    for p in g.values():
        p.pf_ora = p.pf
    stima = {
        # STIMA, come in simula_duello.py
        "Thorik": dict(att=22 + buff, danno=lambda: d(1, 10) + 9, dragondoom=3),
        "Tordek": dict(att=23 + buff, danno=lambda: d(1, 8) + 9 + d(2, 6),
                       arco=20 + buff, danno_arco=lambda: d(1, 8) + 5),
        "Artemis": dict(contatto=13, li=13, eb=eb_dadi),
        "Hella": dict(contatto=11, li=12),
    }
    return g, stima


# =============================================================== creatura
@dataclass
class Creatura:
    nome: str
    pf: int
    ca: int
    contatto: int
    ri: int
    temp: int
    rifl: int
    vol: int
    attacchi: list                 # [(bonus, dadi-callable)], il primo è il morso
    soffio_dadi: tuple             # (n, facce)
    soffio_cd: int
    soffio_forma: str              # "linea" | "cono"
    presenza_cd: int
    li: int = 0                    # livello da incantatore
    immune: tuple = ()             # "fuoco", "freddo", ...
    vulnerabile: tuple = ()
    soglia_fuga: int = 0
    soffio_tipo: str = ""
    rd: int = 0                    # RD che le armi dei PG non superano (es. 3/—)
    note: str = ""


@dataclass
class Stato:
    pf: int
    ca_bonus: int = 0
    immagini: int = 0
    inv_sup: int = 0               # round di invisibilità superiore
    pelle: int = 0                 # pf di pelle di pietra rimasti
    velocita: int = 0              # round di velocità
    soffio_pronto: int = 1
    posizione: str = "alto"        # alto | passata | basso | terra | sotto (scavando)
    luminescenza: bool = False
    risorse: dict = field(default_factory=dict)
    flag: dict = field(default_factory=dict)


@dataclass
class Esito:
    finale: str = ""
    round: int = 0
    pg_morti: int = 0
    pg_giu_fine: int = 0
    danno: int = 0
    terrore: int = 0               # round-PG persi: scossi, nauseati, fuori, charmati
    pf_pg: dict = field(default_factory=dict)   # pf rimasti a ogni PG a fine scontro


# ------------------------------------------------- azioni della creatura
def bersagli_vivi(g):
    return [p for p in g.values() if not p.giu()]


def soffio(c: Creatura, st: Stato, g, rnd: int, sparsi: bool, tutti=False, esclusi=()):
    vivi = [p for p in bersagli_vivi(g) if p.nome not in esclusi and p.fuori == 0]
    if not vivi:
        return
    if tutti:
        k = len(vivi)
    elif c.soffio_forma == "cono":
        k = R.choice((1, 2) if sparsi else (2, 3, 3, 4))
    else:
        k = R.choice((1, 1, 2) if sparsi else (1, 2, 2, 3))
    for p in R.sample(vivi, min(k, len(vivi))):
        n = d(*c.soffio_dadi)
        if ts(p.rifl + p.pen(), c.soffio_cd):
            n //= 2
        p.subisci(max(0, n - p.resist))
    st.soffio_pronto = rnd + R.randint(1, 4)


def attacco_completo(c: Creatura, st: Stato, t: PG, bonus_extra=0, odio=0):
    if R.random() < st.flag.get("alleati_assorbono", 0.0):
        return                        # il round va sugli alleati
    seq = list(c.attacchi)
    if st.velocita > 0:
        seq = [seq[0]] + seq          # un morso in più
    for i, (b, dn) in enumerate(seq):
        extra = (1 if st.velocita > 0 else 0) + bonus_extra + odio
        if t.giu():
            break
        if tira(b + extra, t.ca):
            t.subisci(dn() + (odio if i == 0 else 0))


def morso(c: Creatura, st: Stato, t: PG, extra=0, odio=0) -> bool:
    b, dn = c.attacchi[0]
    if tira(b + extra + odio, t.ca):
        t.subisci(dn() + odio)
        return True
    return False


def presenza(c: Creatura, g):
    for p in g.values():
        if not p.immune_paura and not ts(p.vol, c.presenza_cd):
            p.scosso = d(4, 6)


# ------------------------------------------------- colpi dei PG sul drago
def colpisci_drago(c: Creatura, st: Stato, p: PG, att: int, danno: int,
                   arma: bool, tipo: str = "", area: bool = False) -> int:
    """Applica occultamento, immagini, RD della pelle, immunità. Torna il danno."""
    if st.inv_sup > 0 and not st.luminescenza and not area:
        if R.random() < 0.5:
            return 0
    if st.immagini > 0 and not area:
        if R.random() < st.immagini / (st.immagini + 1):
            if tira(att, 8):           # CA dell'immagine: 10 + taglia + Des
                st.immagini -= 1
            return 0
    if tipo in c.immune:
        return 0
    if tipo in c.vulnerabile:
        danno = danno * 3 // 2
    if arma and c.rd:
        danno = max(0, danno - c.rd)
    if arma and st.pelle > 0:
        assorbe = min(10, danno, st.pelle)
        st.pelle -= assorbe
        danno -= assorbe
    st.pf -= danno
    p.danni_fatti += danno
    return danno


def turno_pg(c: Creatura, st: Stato, g, stima, tattica: str, rnd: int):
    pos = st.posizione
    for p in g.values():
        if p.giu():
            continue
        perso = p.nauseato > 0 or p.fuori > 0 or p.charmato
        if perso:
            p.round_persi += 1
            continue
        if p.scosso > 0:
            p.round_persi += 0  # agisce, ma con −2: contato a parte sotto
        n = p.nome
        if n == "Artemis":
            s = stima[n]
            if tira(s["contatto"] + p.pen(), c.contatto) and ts(s["li"], c.ri):
                base = d(s["eb"], 6)
                colpisci_drago(c, st, p, s["contatto"], base, False, "")
                colpisci_drago(c, st, p, 99, d(1, 6), False, "fuoco")
                colpisci_drago(c, st, p, 99, d(1, 6), False, "freddo")
        elif n == "Hella":
            s = stima[n]
            feriti = [q for q in g.values() if not q.morto and q.pf_ora < q.pf * 0.5]
            if st.inv_sup > 0 and not st.luminescenza and st.risorse.get("lum_hella", 2) > 0:
                st.risorse["lum_hella"] = st.risorse.get("lum_hella", 2) - 1
                if ts(s["li"], c.ri):           # luminescenza: RI sì, nessun TS
                    st.luminescenza = True
            elif feriti and st.risorse.get("cure", 16) > 0:
                st.risorse["cure"] = st.risorse.get("cure", 16) - 1
                f = min(feriti, key=lambda q: q.pf_ora)
                k = st.risorse["cure"]
                f.pf_ora = min(f.pf, f.pf_ora + (d(3, 8) + 12 if k >= 13 else d(2, 8) + 10 if k >= 10 else d(2, 8) + 3))
            elif st.risorse.get("colpo_inf", 3) > 0 and pos != "sotto":
                st.risorse["colpo_inf"] = st.risorse.get("colpo_inf", 3) - 1
                if ts(s["li"], c.ri):
                    fuoco, sacro = d(6, 6), d(6, 6)
                    if ts(c.rifl, 20):
                        fuoco //= 2
                        sacro //= 2
                    colpisci_drago(c, st, p, 99, fuoco, False, "fuoco", area=True)
                    colpisci_drago(c, st, p, 99, sacro, False, "", area=True)
        else:
            s = stima[n]
            mischia = pos in ("basso", "terra") or (p.vola and pos != "sotto")
            if pos == "sotto":
                continue
            if mischia and (pos in ("basso", "terra") or pos == "passata"):
                serie = (0, -5, -10) if pos in ("basso", "terra") else (0,)
                for k in serie:
                    if tira(s["att"] + k + p.pen() + (2 if n == "Tordek" else 0), st_ca(c, st)):
                        x = s["danno"]()
                        if n == "Thorik" and s.get("dragondoom", 0) > 0:
                            s["dragondoom"] -= 1
                            x += d(2, 6)
                        colpisci_drago(c, st, p, s["att"], x, True)
                        if n == "Thorik":
                            st.flag["ascia_ha_cantato"] = True
            elif pos == "passata" and R.random() < 0.5:
                # azione preparata: un colpo quando scende
                if tira(s["att"] + p.pen(), st_ca(c, st)):
                    colpisci_drago(c, st, p, s["att"], s["danno"](), True)
                    if n == "Thorik":
                        st.flag["ascia_ha_cantato"] = True
            elif n == "Tordek":
                for k in (0, -5, -10):
                    if tira(s["arco"] + k + p.pen() - 2, st_ca(c, st)):   # −2 gittata
                        colpisci_drago(c, st, p, s["arco"], s["danno_arco"](), True)
            elif n == "Thorik" and R.random() < 0.3:
                # Aegis Fang scagliata (ritornante): −4 non da lancio, −8 gittata
                if tira(s["att"] - 12 + p.pen(), st_ca(c, st)):
                    colpisci_drago(c, st, p, s["att"], s["danno"](), True)
                    st.flag["ascia_ha_cantato"] = True


def st_ca(c: Creatura, st: Stato) -> int:
    return c.ca + st.ca_bonus + (1 if st.velocita > 0 else 0)


def fine_round(g, st: Stato):
    for p in g.values():
        for a in ("scosso", "nauseato", "invisibile", "fuori"):
            v = getattr(p, a)
            if v > 0:
                setattr(p, a, v - 1)
    for a in ("inv_sup", "velocita"):
        v = getattr(st, a)
        if v > 0:
            setattr(st, a, v - 1)


# ================================================================ motore
def combatti(c: Creatura, politica, tattica: str, buff: int = 0, max_round: int = 20,
             eb_dadi: int = 7, pf_iniziali: int = 0, alleati: tuple = (0, 0.0)) -> Esito:
    """alleati = (danno medio per round sul drago, frazione dei suoi attacchi che
    prendono loro invece dei PG): un'astrazione, STIMA, per le scene di battaglia."""
    g, stima = gruppo(buff, eb_dadi)
    st = Stato(pf=c.pf)
    e = Esito()
    sparsi = "sparsi" in tattica
    if "volo" in tattica:
        for n in ("Thorik", "Tordek", "Hella"):
            g[n].vola = True
    if "preparati" in tattica:
        # Hella sa il colore del drago e prepara resistere all'energia (LI 12°: 30)
        # su tutti e quattro: quattro slot di 2°. Costo: nessuna cura in meno nel modello.
        for p in g.values():
            p.resist = 30
    st.pf = pf_iniziali or c.pf
    politica(c, st, g, 0, sparsi, tattica)      # round 0: preparazione
    for rnd in range(1, max_round + 1):
        e.round = rnd
        if not bersagli_vivi(g):
            e.finale = "vinto"
            break
        giu_prima = sum(1 for p in g.values() if p.giu())
        if st.pf <= c.soglia_fuga:
            e.finale = "fuggito"
            break
        st.flag["alleati_assorbono"] = alleati[1]
        politica(c, st, g, rnd, sparsi, tattica)
        if st.flag.get("fuga"):
            e.finale = "fuggito"
            break
        if st.flag.get("obiettivo"):
            e.finale = "vinto (obiettivo)"
            break
        turno_pg(c, st, g, stima, tattica, rnd)
        if alleati[0] and st.posizione in ("terra", "basso"):
            st.pf -= max(0, int(R.gauss(alleati[0], alleati[0] / 3)))
        if st.pf <= 0:
            e.finale = "ucciso"
            break
        giu = sum(1 for p in g.values() if p.giu())
        if giu >= 2 and giu > giu_prima:
            e.finale = "vinto"
            break
        fine_round(g, st)
    else:
        e.finale = "stallo"
    e.pg_morti = sum(1 for p in g.values() if p.morto)
    e.pg_giu_fine = sum(1 for p in g.values() if p.giu())
    e.danno = (pf_iniziali or c.pf) - max(st.pf, 0)
    e.terrore = sum(p.round_persi for p in g.values())
    e.pf_pg = {p.nome: p.pf_ora for p in g.values()}
    return e


def tabella(titolo: str, c: Creatura, politiche: dict, tattiche: list, prove: int, buff: int, **kw):
    print(f"\n### {titolo} · prove {prove} · buff {buff}\n")
    print("| Politica | Tattica dei PG | ucciso | fuggito | vinto | stallo | almeno un PG morto | PG morti (media) | round | danno al drago | round-PG persi |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for np_, pol in politiche.items():
        for t in tattiche:
            es = [combatti(c, pol, t, buff, **kw) for _ in range(prove)]
            n = len(es)

            def pc(f):
                return f"{100 * sum(1 for x in es if f(x)) / n:.0f}%"
            print(f"| {np_} | {t} | {pc(lambda x: x.finale == 'ucciso')} | {pc(lambda x: x.finale == 'fuggito')} | "
                  f"{pc(lambda x: x.finale.startswith('vinto'))} | {pc(lambda x: x.finale == 'stallo')} | "
                  f"{pc(lambda x: x.pg_morti > 0)} | {sum(x.pg_morti for x in es) / n:.2f} | "
                  f"{sum(x.round for x in es) / n:.1f} | {sum(x.danno for x in es) / n:.0f} | "
                  f"{sum(x.terrore for x in es) / n:.1f} |")


SCONTRI = {}


def scontro(nome):
    def reg(f):
        SCONTRI[nome] = f
        return f
    return reg


def main() -> None:
    import simula_scontri as m        # lo stesso modulo che importano i profili
    import profili_draghi  # noqa: F401  registra gli scontri
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
