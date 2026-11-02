"""L'assedio con l'ambiente (v3): tre giorni, quattro settori, le regole del
libretto più il terreno, le capacità dei reparti, le baliste e le trappole
posate nell'avanguardia. Esperimento per tarare i numeri, non uno strumento.

    python3 -I assedio_v3.py [ferocia] [trappole] [ambiente] [seme] [persi] [morale] [lim] [politica]

ferocia: si somma ad AU e DU dell'orda base (1 = normale del libretto, 2 = feroce,
3 = terrificante); trappole 0-8 dall'avanguardia, ognuna annulla una tacca del
giorno 1 o del giorno 2, dove serve (decisione del DM del 2026-10-21);
ambiente 0 = regole della v2, 1 = con terreno, capacità e baliste;
politica: attento (default), tenere, colpire, caricare (lo stesso ordine sempre).

I giganti tirano un macigno per settore al round 2 dei giorni 1 e 2: è la carta
del libretto. Il macigno conta il +1 del primo giorno e il morale, non le
merlature delle Mura.
"""
import random, statistics, sys

FEROCIA = int(sys.argv[1]) if len(sys.argv) > 1 else 2
TRAPPOLE = int(sys.argv[2]) if len(sys.argv) > 2 else 4
AMBIENTE = int(sys.argv[3]) if len(sys.argv) > 3 else 1
R = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1372)
PERSI = int(sys.argv[5]) if len(sys.argv) > 5 else 0   # reparti delle mura persi prima
MORALE0 = int(sys.argv[6]) if len(sys.argv) > 6 else 1  # il morale all'alba del primo giorno
LIM = int(sys.argv[7]) if len(sys.argv) > 7 else 2      # il morale pesa sui dadi al massimo ±LIM
POLITICA = sys.argv[8] if len(sys.argv) > 8 else "attento"
def mo(m): return max(-LIM, min(LIM, m))
d = lambda n: R.randint(1, n)
def tab(m): return 0 if m < 0 else 1 if m < 5 else 2 if m < 10 else 3

NANI = {"guardia": (11, 22, 12), "veterani": (10, 21, 11), "balestrieri": (9, 18, 9)}
BASE = {"hobgoblin": (10, 20, 10), "orchi": (7, 14, 8), "guerrieri": (6, 18, 11),
        "lupi": (7, 17, 10)}
EROE = {"Borin": 21, "Dara": 19, "Thorin": 14, "Nala": 13}
ORD = {"tenere": (None, 4), "colpire": (0, 0), "caricare": (2, -2)}
SETTORI = [("Borin", ["guardia"] * 2, "Cancello", 3),
           ("Dara", ["balestrieri"] * 2, "Torre Ovest", 2),
           ("Thorin", ["veterani"] * 2, "Mura", 3),
           ("Nala", ["veterani"] * 2, "Torre Est", 2)]
TORRI = ("Torre Ovest", "Torre Est")

def nemico(t):
    au, du, pfu = BASE[t]
    return {"t": t, "au": au + FEROCIA, "du": du + FEROCIA, "pfu": pfu, "nuovo": True}

def mazzo():
    m = ["orchi"] * 3 + ["hobgoblin"] * 6 + ["guerrieri"] * 4 + ["lupi"]
    R.shuffle(m); return [nemico(x) for x in m]

def au_nemico(e, campo):
    au = e["au"]
    if AMBIENTE and e["t"] == "orchi":
        if e["nuovo"]: au += 1          # Carica selvaggia, il round in cui arrivano
        if e["pfu"] <= 4: au += 1       # Furia
    return au

def du_nemico(e, campo):
    du = e["du"]
    if AMBIENTE:
        if e["t"] == "orchi" and e["nuovo"]: du -= 2
        if e["t"] == "hobgoblin" and sum(x["t"] == "hobgoblin" for x in campo) >= 2: du += 1
    return du

def politica(mie, rep, campo, eroe):
    ordini = []
    for p, tipo in zip(mie, rep):
        if p <= 0: ordini.append(None)
        elif POLITICA != "attento": ordini.append(POLITICA)
        elif p <= 4: ordini.append("tenere")
        elif any(x["t"] == "orchi" for x in campo): ordini.append("caricare")
        else: ordini.append("colpire")
    return ordini, "combattere"

def battaglia():
    pfu = {s[2]: [NANI[r][2] for r in s[1]] for s in SETTORI}
    pieno = {k: list(v) for k, v in pfu.items()}
    for nome in R.sample([s[2] for s in SETTORI], PERSI): pfu[nome][0] = 0
    morale, brecce, per_giorno, tr = MORALE0, 0, {}, TRAPPOLE
    mura_rotte = False
    for giorno in (1, 2, 3):
        brecce_g = 0
        for eroe, rep, nome, fr in SETTORI:
            fr += 1 if (giorno == 2 and nome == "Cancello") else 0
            coda, campo, tacche, spezza = mazzo(), [], 0, True
            for r in range(4 if giorno == 3 else 5):
                while len(campo) < fr and coda: campo.append(coda.pop(0))
                vivi = [i for i, p in enumerate(pfu[nome]) if p > 0]
                if not vivi: tacche = TACCHE; break
                # le difese: +1 il primo giorno ovunque, e sulle Mura le merlature
                # finché non hanno ceduto una volta
                muro = 1 if giorno == 1 else 0
                if AMBIENTE and nome == "Mura" and not mura_rotte: muro = 1
                ordini, gesto = politica(pfu[nome], rep, campo, eroe)
                if giorno < 3 and r == 1:
                    # i giganti: un macigno per settore; le merlature non contano
                    i = R.choice(vivi)
                    primo = 1 if giorno == 1 else 0
                    pfu[nome][i] = max(0, pfu[nome][i] - tab(d(20) + 14 - (NANI[rep[i]][1] + primo + mo(morale))))
                if giorno == 3 and r == 1 and nome == "Mura":
                    for i in vivi: pfu[nome][i] = max(0, pfu[nome][i] - d(4))
                inflitti = 0
                # la balista della torre, una volta per round
                if AMBIENTE and nome in TORRI:
                    e = min([x for x in campo if x["pfu"] > 0] or [None], key=lambda x: x["pfu"] if x else 0)
                    if e:
                        p = min(tab(d(20) + 10 - du_nemico(e, campo)), e["pfu"]); e["pfu"] -= p; inflitti += p
                # Spezzare la carica: la Guardia, una volta al giorno
                if AMBIENTE and rep[0] == "guardia" and spezza:
                    bers = [x for x in campo if x["t"] == "orchi" and x["pfu"] > 0]
                    if bers:
                        p = min(d(4), bers[0]["pfu"]); bers[0]["pfu"] -= p; inflitti += p; spezza = False
                b = [x for x in campo if x["pfu"] > 0]
                if b and gesto == "combattere":
                    e = min(b, key=lambda x: x["pfu"])
                    bonus = 6 if (eroe == "Dara" and e["t"] == "orchi") else 0
                    p = min(tab(d(20) + EROE[eroe] + bonus - du_nemico(e, campo)), e["pfu"])
                    e["pfu"] -= p; inflitti += p
                vivi = [i for i, p in enumerate(pfu[nome]) if p > 0]
                alto = 1 if (AMBIENTE and nome in TORRI) else 0   # balestrieri sulle torri
                for k, i in enumerate(vivi):
                    b = [x for x in campo if x["pfu"] > 0]
                    dau = ORD[ordini[i]][0]
                    if dau is None or not b: continue
                    e = b[min(k, len(b) - 1)]
                    a = alto if rep[i] == "balestrieri" else 0
                    p = min(tab(d(20) + NANI[rep[i]][0] + dau + a + mo(morale) - du_nemico(e, campo)), e["pfu"])
                    e["pfu"] -= p; inflitti += p
                for k, e in enumerate([x for x in campo if x["pfu"] > 0]):
                    vivi = [i for i, p in enumerate(pfu[nome]) if p > 0]
                    if not vivi: break
                    i = vivi[k % len(vivi)]
                    ddu = ORD[ordini[i]][1]
                    if AMBIENTE and rep[i] == "veterani" and ordini[i] == "tenere": ddu = 6   # Muro di scudi
                    a = alto if rep[i] == "balestrieri" else 0
                    sb = 2 if (AMBIENTE and e["t"] == "lupi") else 0                       # Sbilanciare
                    m = (22 + au_nemico(e, campo)) - (d(20) + NANI[rep[i]][1] + ddu + a + muro + mo(morale) - sb)
                    pfu[nome][i] = max(0, pfu[nome][i] - tab(m - 1))
                    if pfu[nome][i] == 0: morale = max(-5, morale - 1)
                for e in campo: e["nuovo"] = False
                campo = [x for x in campo if x["pfu"] > 0]
                if inflitti < 2:
                    # una trappola posata nell'avanguardia annulla una tacca del
                    # giorno 1 o del giorno 2, dove serve
                    if giorno <= 2 and tr > 0: tr -= 1
                    else: tacche += 1
                if tacche >= TACCHE: break
            if tacche >= TACCHE:
                brecce_g += 1; morale = max(-5, morale - 2)
                if nome == "Mura": mura_rotte = True
        brecce += brecce_g
        morale = max(-5, min(5, morale + (1 if brecce_g == 0 else 0)))
        for k in pfu:
            pfu[k] = [min(m, p + 1) if p > 0 else 0 for p, m in zip(pfu[k], pieno[k])]
        per_giorno[giorno] = brecce_g
    return dict(b12=per_giorno[1] + per_giorno[2], vivi=sum(1 for v in pfu.values() for p in v if p > 0))

TACCHE = 3
if __name__ == "__main__":
    rs = [battaglia() for _ in range(3000)]
    q = lambda f: round(100 * sum(1 for r in rs if f(r)) / len(rs))
    print(f"ferocia {FEROCIA} trappole {TRAPPOLE} ambiente {AMBIENTE} politica {POLITICA}: "
          f"breccia {q(lambda r: r['b12'] == 0)}/{q(lambda r: r['b12'] == 1)}/{q(lambda r: r['b12'] >= 2)}% "
          f"posizioni {q(lambda r: r['vivi'] >= 6)}/{q(lambda r: 3 <= r['vivi'] < 6)}/{q(lambda r: r['vivi'] < 3)}% "
          f"reparti {round(statistics.mean(r['vivi'] for r in rs), 2)}/8")
