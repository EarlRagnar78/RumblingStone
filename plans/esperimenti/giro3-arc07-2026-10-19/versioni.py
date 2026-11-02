"""Le cinque versioni di ARC-07 a confronto. uso: versioni.py [cartella dei nuovi]"""
import sys, re, glob, statistics
from pathlib import Path
sys.path.insert(0, "scripts")
import cieco_versioni as cv, ciclo_prosa as cp, misura_craft as mc
FILES = sorted(glob.glob("07_il Portale Della Forgia Eterna/ARC07-DEF-*.md"))
VERS = [("prima del rifacimento", "prima-rifacimento-arc07"), ("#249", "2ee82472"), ("#251 (main)", "e0ce0e6")]
nuovi = sys.argv[1] if len(sys.argv) > 1 else None
if nuovi: VERS.append(("giro 3", None))
def testo(ref, f):
    if ref is None:
        p = Path(nuovi) / Path(f).name
        return p.read_text(encoding="utf-8") if p.exists() else cv.testo_a("e0ce0e6", f)
    return cv.testo_a(ref, f)
righe = []
for nome, ref in VERS:
    bs, seg, mqm, imp = [], 0, [], 0
    for f in FILES:
        t = testo(ref, f)
        bs += [mc.corpo_del_box(b) for b in mc.box_read_aloud(t)]
        seg += len(cp.segnala(t))
        q = cp.mqm(t, Path(f)); mqm.append(q["punteggio"] if q else 0)
        if ref != "d6716f4":
            imp += len(cp.box_impoveriti(cv.testo_a("d6716f4", f), t))
    tutto = "\n".join(bs); par = len(tutto.split())
    lun = [len(b.split()) for b in bs]
    mente = len(re.findall(r"\b\w{3,}mente\b", tutto))
    righe.append((nome, len(bs), par, statistics.median(lun), mc.dettagli_sensoriali(tutto),
                  round(1000 * mc.dettagli_sensoriali(tutto) / par, 1), mente, round(1000 * mente / par, 1),
                  round(100 * sum(30 <= l <= 70 for l in lun) / len(lun)), seg,
                  round(statistics.mean(mqm), 2), imp))
print("| versione | box | parole | mediana | sens. | sens. ‰ | -mente | -mente ‰ | 30-70 % | segnalazioni | MQM medio | impoveriti vs prima della #249 |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for r in righe: print("| " + " | ".join(map(str, r)) + " |")
