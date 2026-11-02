"""Simulazione delle regole del libretto della battaglia campale (v1).

Esperimento, non strumento: serve a tarare i numeri del libretto prima di
darlo al tavolo. Un settore, una schiera (eroe + reparti) contro la coda
dell'ondata; si misura cosa succede in un giorno di battaglia.
"""
import random, statistics, sys
from dataclasses import dataclass, field

R = random.Random(1372)
d = lambda n: R.randint(1, n)

def esito(tiro, bersaglio):
    """La tabella unica: si colpisce se tiro >= bersaglio; +5 = 2, +10 = 3."""
    m = tiro - bersaglio
    return 0 if m < 0 else 1 if m < 5 else 2 if m < 10 else 3

@dataclass
class Reparto:
    nome: str; au: int; du: int; pfu: int; distanza: bool = False
    def vivo(self): return self.pfu > 0

# AU e DU dei reparti col morale di base già dentro (canone ARC08-02 §5-6)
NANI = {
    "veterani":   dict(au=10, du=21, pfu=11),
    "elite":      dict(au=11, du=22, pfu=12),
    "balestrieri": dict(au=9, du=18, pfu=9, distanza=True),
}
ORDA = {
    "hobgoblin": dict(au=10, du=20, pfu=10),
    "orchi":     dict(au=7, du=14, pfu=8),
    "guerrieri": dict(au=6, du=18, pfu=11),
    "worg":      dict(au=7, du=17, pfu=10),
    "orog":      dict(au=15, du=22, pfu=13),
}
EROI = {  # bonus d'attacco della scheda corretta (Bestiario, 2026-10-16)
    "Borin": 21, "Dara": 19, "Thorin": 14, "Nala": 13,
}
ORDINI = {"tenere": (-2, +3), "colpire": (0, 0), "caricare": (+2, -2)}

def giorno(eroe, schiera, coda, round_=5, modo="B", ordine="colpire",
           fronte=2, gesto="combattere", incantesimi=2, morale_n=0,
           morale_o=0):
    """modo A: solo l'eroe (reparti fuori, esito da copione); B: eroe e
    reparti; C: solo i reparti."""
    nostri = [Reparto(n, **NANI[n]) for n in schiera] if modo != "A" else []
    coda = [Reparto(n, **ORDA[n]) for n in coda]
    in_campo = []
    uccisi = persi = dell_eroe = tiri = 0
    tiri_per_round = []
    for r in range(round_):
        t0 = tiri
        while len(in_campo) < fronte and coda:
            in_campo.append(coda.pop(0))
        if not in_campo: break
        dau, ddu = ORDINI[ordine]
        com = 0
        # gesto dell'eroe
        if modo in "AB" and eroe:
            if gesto == "comandare" and modo == "B":
                com = 2
            elif gesto == "incantesimo" and incantesimi > 0:
                incantesimi -= 1
                b = in_campo[0]; tiri += 2
                p = d(4)
                if d(20) + 4 >= 18: p //= 2   # TS dell'unità
                p = min(p, b.pfu); b.pfu -= p; uccisi += p; dell_eroe += p
            else:
                b = min(in_campo, key=lambda x: x.pfu)
                tiri += 1
                p = min(esito(d(20) + EROI[eroe], b.du + morale_o), b.pfu)
                b.pfu -= p; uccisi += p; dell_eroe += p
        in_campo = [x for x in in_campo if x.vivo()]
        # scontri: ogni reparto nostro contro uno dell'orda, il giocatore
        # tira attacco e difesa
        for i, n in enumerate([x for x in nostri if x.vivo()]):
            if not in_campo: break
            e = in_campo[min(i, len(in_campo) - 1)]
            tiri += 1
            p = min(esito(d(20) + n.au + dau + com + morale_n,
                          e.du + morale_o), e.pfu)
            e.pfu -= p; uccisi += p
        vivi = [x for x in nostri if x.vivo()]
        for i, e in enumerate(in_campo):
            if not e.vivo() or not vivi: continue
            n = vivi[i % len(vivi)]
            tiri += 1
            # difesa del giocatore: d20 + DU contro 22 + AU nemico
            # equivalente a «d20 + AU nemico contro DU»
            m = (22 + e.au + morale_o) - (d(20) + n.du + ddu + morale_n)
            p = 0 if m <= 0 else 1 if m < 5 else 2 if m < 10 else 3
            p = min(p, n.pfu); n.pfu -= p; persi += p
        in_campo = [x for x in in_campo if x.vivo()]
        tiri_per_round.append(tiri - t0)
    tiene = modo == "A" or any(x.vivo() for x in nostri)
    return dict(uccisi=uccisi, persi=persi, eroe=dell_eroe, tiene=tiene,
                tiri=statistics.mean(tiri_per_round) if tiri_per_round else 0)

def prova(n=4000, **kw):
    rs = [giorno(**kw) for _ in range(n)]
    m = lambda k: statistics.mean(r[k] for r in rs)
    return dict(uccisi=round(m("uccisi"), 1), persi=round(m("persi"), 1),
                quota_eroe=round(m("eroe") / max(m("uccisi"), .01), 2),
                tiene=round(sum(r["tiene"] for r in rs) / n, 2),
                tiri=round(m("tiri"), 1))

if __name__ == "__main__":
    ONDATA = ["orchi", "orchi", "hobgoblin", "hobgoblin", "guerrieri",
              "hobgoblin", "guerrieri", "hobgoblin"]
    casi = [
      ("Borin, 2 élite, colpire",   dict(eroe="Borin", schiera=["elite"]*2)),
      ("Borin, 2 élite, tenere",    dict(eroe="Borin", schiera=["elite"]*2, ordine="tenere")),
      ("Borin, 2 élite, caricare",  dict(eroe="Borin", schiera=["elite"]*2, ordine="caricare")),
      ("Borin comanda",             dict(eroe="Borin", schiera=["elite"]*2, gesto="comandare")),
      ("Nala, 2 veterani",          dict(eroe="Nala", schiera=["veterani"]*2)),
      ("Thorin, 2 veterani, incant.", dict(eroe="Thorin", schiera=["veterani"]*2, gesto="incantesimo")),
      ("Dara, 2 balestrieri",       dict(eroe="Dara", schiera=["balestrieri"]*2)),
      ("modo C: 2 veterani, nessun eroe", dict(eroe=None, schiera=["veterani"]*2, modo="C")),
      ("modo A: solo Borin",        dict(eroe="Borin", schiera=[], modo="A")),
    ]
    for nome, kw in casi:
        print(f"{nome:34s}", prova(coda=list(ONDATA), **kw))
