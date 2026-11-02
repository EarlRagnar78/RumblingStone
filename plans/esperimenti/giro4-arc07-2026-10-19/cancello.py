"""Il cancello del giro 4: un file riscritto entra solo se non peggiora niente.

uso (dalla radice del repo):  python3 cancello.py <file del repo> <file riscritto>
Base = main dopo la #252 (8a6b1e1). Esce 1 se qualcosa non passa.
"""
import sys, json, re, subprocess
from pathlib import Path
sys.path.insert(0, "scripts")
import cieco_versioni as cv, ciclo_prosa as cp, misura_craft as mc

QUI = Path(__file__).parent
BASE, PRIMA249 = "8a6b1e1", "d6716f4"
rel, nuovo_p = sys.argv[1], Path(sys.argv[2])
base = cv.testo_a(BASE, rel)
nuovo = nuovo_p.read_text(encoding="utf-8")
errori, note = [], []
norm = lambda t: " ".join(t.replace("*", "").replace(">", " ").split())

# 1. i box votati dal DM restano parola per parola
N = norm(nuovo)
for x in json.load(open(QUI.parent / "giro3-arc07-2026-10-19" / "misure" / "CONGELATI.json")):
    if x["file"] == rel and norm(x["testo"]) not in N:
        errori.append(f"box votato dal DM cambiato: coppia {x['n']} · {x['titolo'][:60]}")

# 2. box per box contro main: la misura del DM non deve preferire il vecchio
nuovi = cv.box_con_titolo(nuovo, battute=True)
cambiati = 0
for b in cv.box_con_titolo(base):
    if b["parole"] < cv.PAROLE_MINIME:
        continue
    _, s, nu = cv.appaia(b, nuovi)
    if nu == b["testo"]:
        continue
    if s < cv.SOMIGLIANZA_DUBBIA:
        errori.append(f"box senza corrispondente (tolto?): {b['titolo'][:60]} · {b['testo'][:50]!r}")
        continue
    cambiati += 1
    v, perche = cv.verdetto_misurato(b["testo"], nu)
    if v == "vecchia":
        errori.append(f"box peggiorato ({perche}): {b['titolo'][:60]} · {b['testo'][:50]!r}")

# 3. contro la versione prima della #249: nessun impoverito nuovo
p249 = cv.testo_a(PRIMA249, rel)
prima_imp = {x.split(":")[0] for x in cp.box_impoveriti(p249, base)}
for x in cp.box_impoveriti(p249, nuovo):
    if x.split(":")[0] not in prima_imp:
        errori.append(f"impoverito rispetto a prima della #249: {x}")

# 4. le norme del ciclo, l'MQM, i fatti
mig = cp.miglioramento(base, nuovo, Path(rel))
errori += [f"peggiora: {x}" for x in cp.peggiora(mig)]
errori += [f"fatto cambiato: {x}" for x in cp.confronta_fatti(base, nuovo)]

# 5. tetti duri dei box: righe e parentesi
def tetti(t):
    out = []
    for b in mc.box_read_aloud(t):
        corpo = mc.corpo_del_box(b)
        if len(b) > 12 and "scelta del DM" not in t[max(0, t.find(b[0]) - 200):t.find(b[0])]:
            out.append(f">12 righe: {corpo[:50]!r}")
    return out
nb, nn = set(tetti(base)), tetti(nuovo)
errori += [x for x in nn if x not in nb]

# le misure, per sapere di quanto
def stile(t):
    bs = [mc.corpo_del_box(b) for b in mc.box_read_aloud(t)]
    testo = "\n".join(bs)
    par = len(testo.split())
    mente = len(re.findall(r"\b\w{3,}mente\b", testo))
    return {"box": len(bs), "parole": par, "sens": mc.dettagli_sensoriali(testo), "-mente": mente,
            "30-70": round(100 * sum(30 <= len(x.split()) <= 70 for x in bs) / max(1, len(bs)))}
sb, sn = stile(base), stile(nuovo)
print(f"== {rel}")
print(f"box cambiati: {cambiati}")
print("misura       " + "  ".join(f"{k} {sb[k]}→{sn[k]}" for k in sb))
print(f"segnalazioni {mig['segnalazioni'][0]}→{mig['segnalazioni'][1]} · MQM {mig['mqm']} · "
      f"Gulpease {mig['gulpease']} · ritmo {mig['ritmo']}")
for e in errori:
    print("✗", e)
print("✓ passa" if not errori else f"✗ {len(errori)} non passano")
sys.exit(1 if errori else 0)
