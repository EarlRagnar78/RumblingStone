"""L'avanguardia (Sessione 1): quattro squadre di guastatori sul pendio, un
eroe e un reparto ciascuna, scavano trappole mentre arrivano i lupi con i
goblin, poi la pattuglia hobgoblin col sergente, poi il corno di Grimjaw.
Quante trappole si posano e quanto costa restare un round in più: una squadra
travolta perde le sue trappole. I guastatori non sono i reparti delle mura.

La ritirata è di tutto il gruppo, a un round fisso (decisione del DM del
2026-10-21): una squadra sola non si ritira, smette di scavare alla seconda
tacca e combatte (Colpire). Le trappole si contano sul gruppo: ogni round di
scavo vale mezza trappola, e il totale si tronca alla fine.

    python3 -I avanguardia.py [ferocia] [round_prima_della_ritirata]
"""
import random, statistics, sys

FEROCIA = int(sys.argv[1]) if len(sys.argv) > 1 else 2
ROUND = int(sys.argv[2]) if len(sys.argv) > 2 else 5
R = random.Random(1372)
d = lambda n: R.randint(1, n)
def tab(m): return 0 if m < 0 else 1 if m < 5 else 2 if m < 10 else 3

SQUADRE = [("Borin", 21, (11, 22, 12)), ("Dara", 19, (9, 18, 9)),
           ("Thorin", 14, (10, 21, 11)), ("Nala", 13, (10, 21, 11))]
LUPI, HOB = (7, 17, 10), (10, 20, 10)

def squadra(eroe, att, rep):
    au, du, pfu = rep
    nem, trappole, tacche, travolta = [], 0, 0, False
    for r in range(1, ROUND + 1):
        fronte, tipo, extra = (1, LUPI, 0) if r <= 2 else (2, HOB, 1 if r >= 3 else 0)
        if r >= 5: extra += 1                       # il corno di Grimjaw
        while len([e for e in nem if e[2] > 0]) < fronte:
            nem.append([tipo[0], tipo[1], tipo[2]])
        nem = [e for e in nem if e[2] > 0]
        scava = pfu > 5 and tacche < 2
        inflitti = 0
        e = min(nem, key=lambda x: x[2])
        p = min(tab(d(20) + att - (e[1] + FEROCIA + extra)), e[2]); e[2] -= p; inflitti += p
        if scava: trappole += 0.5                     # una trappola ogni due round di scavo
        else:
            e = [x for x in nem if x[2] > 0]
            if e:
                p = min(tab(d(20) + au + 1 - (e[0][1] + FEROCIA + extra)), e[0][2]); e[0][2] -= p; inflitti += p
        for x in [x for x in nem if x[2] > 0]:
            sb = 2 if x[0] == LUPI[0] else 0              # i lupi sbilanciano
            m = (22 + x[0] + FEROCIA + extra) - (d(20) + du + 1 - (2 if scava else 0) - sb)
            pfu = max(0, pfu - tab(m - 1))
        if inflitti < 2: tacche += 1
        if tacche >= 3 or pfu == 0:
            # travolta: l'orda trova le sue trappole e le disfa
            travolta = True; trappole = 0; break
    return trappole, pfu, travolta, rep[2]

if __name__ == "__main__":
    tot, persi, travolte, pfu_res = [], [], [], []
    for _ in range(3000):
        rs = [squadra(*s) for s in SQUADRE]
        tot.append(sum(r[0] for r in rs)); travolte.append(sum(r[2] for r in rs))
        persi.append(sum(r[1] == 0 for r in rs)); pfu_res.append(sum(r[1] for r in rs))
    m = lambda xs: round(statistics.mean(xs), 2)
    q = lambda f: round(100 * sum(1 for t in tot if f(int(t))) / len(tot))
    print(f"ferocia {FEROCIA}, ritirata dopo il round {ROUND}: trappole {m([int(t) for t in tot])} "
          f"(6+ {q(lambda t: t >= 6)}%, 3-5 {q(lambda t: 3 <= t < 6)}%, <3 {q(lambda t: t < 3)}%) | "
          f"squadre travolte {m(travolte)} | reparti persi {m(persi)} | PFU rimasti {m(pfu_res)}/43")
