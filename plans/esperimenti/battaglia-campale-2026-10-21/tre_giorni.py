"""I tre giorni dell'assedio con le regole del libretto (v2).

Quattro schiere in quattro settori, cinque round per giorno, le perdite che
passano da un giorno all'altro. Esperimento per tarare i numeri: non è uno
strumento del repo.

    python3 -I tre_giorni.py [seme] [soglia_pressione] [tacche] [feroce] [modo] [capitano]

feroce = 1 dà +1 ad AU e DU di tutta l'orda (la versione del libretto);
modo = B (eroe e due reparti) o C (il capitano: tre reparti, +2 sempre).
Le carte dei comandanti e la palla di fuoco del libretto non sono simulate.
"""
import random, statistics, sys

SEME = int(sys.argv[1]) if len(sys.argv) > 1 else 1372
SOGLIA = int(sys.argv[2]) if len(sys.argv) > 2 else 2   # PFU minimi per round
TACCHE = int(sys.argv[3]) if len(sys.argv) > 3 else 3
FEROCE = int(sys.argv[4]) if len(sys.argv) > 4 else 0
MODO = sys.argv[5] if len(sys.argv) > 5 else "B"
CAPITANO = int(sys.argv[6]) if len(sys.argv) > 6 else 0   # il bonus del modo C (0 nel libretto)
R = random.Random(SEME)
d = lambda n: R.randint(1, n)
def tab(m): return 0 if m < 0 else 1 if m < 5 else 2 if m < 10 else 3

# AU, DU, PFU col morale di base dentro (ARC08-02 §5-6)
NANI = {"veterani": (10, 21, 11), "elite": (11, 22, 12), "balestrieri": (9, 18, 9)}
ORDA = {"hobgoblin": (10, 20, 10), "orchi": (7, 14, 8), "guerrieri": (6, 18, 11),
        "worg": (7, 17, 10)}
ORDA = {k: (a + FEROCE, b + FEROCE, c) for k, (a, b, c) in ORDA.items()}
EROE = {"Borin": 21, "Dara": 19, "Thorin": 14, "Nala": 13}
ORD = {"tenere": (None, 4), "colpire": (0, 0), "caricare": (2, -2)}
SETTORI = [("Borin", ["elite"] * 2, "Cancello", 3),
           ("Dara", ["balestrieri"] * 2, "Torre Ovest", 2),
           ("Thorin", ["veterani"] * 2, "Mura", 3),
           ("Nala", ["veterani"] * 2, "Torre Est", 2)]
if MODO == "C":
    SETTORI = [(e, rep + rep[:1], n, f) for e, rep, n, f in SETTORI]
REPARTI = sum(len(s[1]) for s in SETTORI)

def ondata():
    m = ["orchi"] * 3 + ["hobgoblin"] * 6 + ["guerrieri"] * 4 + ["worg"]
    R.shuffle(m); return [list(ORDA[x]) for x in m]

def battaglia(politica):
    pfu = {s[2]: [NANI[r][2] for r in s[1]] for s in SETTORI}
    pieno = {k: list(v) for k, v in pfu.items()}
    morale, uccisi, brecce, per_giorno = 1, 0, 0, {}
    for giorno in (1, 2, 3):
        mura = 1 if giorno == 1 else 0
        brecce_g = 0
        for eroe, rep, nome, fr in SETTORI:
            fr += 1 if (giorno == 2 and nome == "Cancello") else 0
            coda, campo, tacche = ondata(), [], 0
            for r in range(4 if giorno == 3 else 5):
                while len(campo) < fr and coda: campo.append(coda.pop(0))
                vivi = [i for i, p in enumerate(pfu[nome]) if p > 0]
                if not vivi: tacche = TACCHE; break
                ordine, gesto = politica(pfu[nome], campo, eroe)
                if MODO == "C": gesto = "comandare"
                dau, ddu = ORD[ordine]
                # la carta dell'orda: i giganti il primo e il secondo giorno,
                # il soffio del drago sulle Mura il terzo
                if giorno < 3 and r == 1:
                    i = R.choice(vivi)
                    pfu[nome][i] = max(0, pfu[nome][i] - tab(d(20) + 14 - (NANI[rep[i]][1] + mura + morale)))  # tiro dell'orda, diretto
                if giorno == 3 and r == 1 and nome == "Mura":
                    for i in vivi: pfu[nome][i] = max(0, pfu[nome][i] - d(4))
                inflitti, com = 0, 0
                if gesto == "comandare": com = CAPITANO if MODO == "C" else 2
                else:
                    b = min(campo, key=lambda x: x[2])
                    p = min(tab(d(20) + EROE[eroe] - b[1]), b[2]); b[2] -= p; inflitti += p
                vivi = [i for i, p in enumerate(pfu[nome]) if p > 0]
                for k, i in enumerate(vivi):
                    vivi_o = [x for x in campo if x[2] > 0]
                    if dau is None or not vivi_o: break
                    e = vivi_o[min(k, len(vivi_o) - 1)]
                    p = min(tab(d(20) + NANI[rep[i]][0] + dau + com + morale - e[1]), e[2])
                    e[2] -= p; inflitti += p
                for k, e in enumerate([x for x in campo if x[2] > 0]):
                    vivi = [i for i, p in enumerate(pfu[nome]) if p > 0]
                    if not vivi: break
                    i = vivi[k % len(vivi)]
                    m = (22 + e[0]) - (d(20) + NANI[rep[i]][1] + ddu + com + mura + morale)
                    # il bianco è il tiro dell'orda rovesciato: mancare di k
                    # vuol dire che l'orda supera di k-1 (fasce 1-5, 6-10, 11+)
                    pfu[nome][i] = max(0, pfu[nome][i] - tab(m - 1))
                    if pfu[nome][i] == 0: morale -= 1
                campo = [x for x in campo if x[2] > 0]
                uccisi += inflitti
                if inflitti < SOGLIA: tacche += 1
                if tacche >= TACCHE: break
            if tacche >= TACCHE:
                brecce_g += 1; morale -= 2
        brecce += brecce_g
        morale = max(-5, min(5, morale + (1 if brecce_g == 0 else 0)))
        for k in pfu:   # la notte: un PFU torna a ogni reparto vivo
            pfu[k] = [min(m, p + 1) if p > 0 else 0 for p, m in zip(pfu[k], pieno[k])]
        per_giorno[giorno] = brecce_g
    return dict(uccisi=uccisi, brecce=brecce, brecce12=per_giorno[1] + per_giorno[2], g1=per_giorno[1], g2=per_giorno[2],
                g3=per_giorno[3], vivi=sum(1 for v in pfu.values() for p in v if p > 0),
                pfu=sum(sum(v) for v in pfu.values()), morale=morale)

def mista(mine, campo, eroe):
    debole = min([p for p in mine if p > 0] or [0]) <= 4
    if debole: return "tenere", "combattere"
    if any(x[1] <= 14 for x in campo): return "caricare", "combattere"
    return "colpire", "combattere"
def comandante(mine, campo, eroe):
    debole = min([p for p in mine if p > 0] or [0]) <= 4
    return ("colpire", "comandare") if debole else ("colpire", "combattere")
POLITICHE = {
    "attento": mista, "col comando": comandante,
    "sempre colpire": lambda m, c, e: ("colpire", "combattere"),
    "sempre tenere": lambda m, c, e: ("tenere", "combattere"),
    "sempre caricare": lambda m, c, e: ("caricare", "combattere"),
}
if __name__ == "__main__":
    print(f"soglia {SOGLIA} PFU a round, {TACCHE} tacche, feroce {FEROCE}, modo {MODO}")
    # le soglie della tabella dei bonus (ARC08-10 §5) lette come nel libretto §12
    pieno_pos, parz_pos = (6, 3) if MODO == "B" else (9, 5)
    for nome, pol in POLITICHE.items():
        rs = [battaglia(pol) for _ in range(3000)]
        m = lambda k: round(statistics.mean(r[k] for r in rs), 2)
        z = round(sum(1 for r in rs if r["brecce"] == 0) / len(rs), 2)
        print(f"  {nome:15s} orda -{m('uccisi'):6} PFU | brecce g1 {m('g1')} g2 {m('g2')} g3 {m('g3')} "
              f"(nessuna: {z}) | reparti vivi {m('vivi')}/{REPARTI} | morale {m('morale')}")
        q = lambda f: round(100 * sum(1 for r in rs if f(r)) / len(rs))
        print(f"  {'':15s} breccia contenuta {q(lambda r: r['brecce12'] == 0)}/"
              f"{q(lambda r: r['brecce12'] == 1)}/{q(lambda r: r['brecce12'] >= 2)}% | "
              f"posizioni tenute {q(lambda r: r['vivi'] >= pieno_pos)}/"
              f"{q(lambda r: parz_pos <= r['vivi'] < pieno_pos)}/{q(lambda r: r['vivi'] < parz_pos)}%")
