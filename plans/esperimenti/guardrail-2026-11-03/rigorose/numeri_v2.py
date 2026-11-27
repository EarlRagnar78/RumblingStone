"""Numeri incrociati, configurazione rigorosa: valori dei recinti (CA, pf) di ogni master contro
le citazioni «Nome (… CA N … pf N …)» in TUTTI i file vivi del repo, solo dentro la parentesi
subito dopo il nome; fuori le soglie («metà», «sotto i», «dai»), le varianti («avanzato», «scalat», «DV»)."""
import re, sys
from pathlib import Path
sys.path.insert(0,'scripts')
import conformita_statblocchi as C
from misura_standard_tavolo import chiave, piega
amm={}
for p in C.master_di_default():
    for b in C._recinti_del_master(p.read_text(errors='replace')):
        k=piega((b["sb"].nome or "").split(" ")[0].split(",")[0])
        if not k or len(k)<5: continue
        a=amm.setdefault(k,{"CA":set(),"pf":set()})
        a["CA"]|={int(x) for x in re.findall(r"\d+",b["sb"].ca or "")}
        a["pf"]|={int(x) for x in re.findall(r"\d+",b["sb"].pf or "")}
GENERICI={"guardia","hobgoblin","orco","sacerdote","sentinella","treant","worg","wyvern","xorn"}  # tipi, non persone
amm={k:v for k,v in amm.items() if k not in GENERICI}
print("chiavi proprie",sorted(amm))
tot=0; out=[]
DIRS=["07_il Portale Della Forgia Eterna","08_La Battaglia Di Hammerfist","09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist","Bestiario","campaign"]
for d in DIRS:
    for f in Path(d).rglob("*.md"):
        rel=f.as_posix()
        if "/homebrew/" in rel or "_ARCHIVIO" in rel or "/esperimenti/" in rel: continue
        for i,l in enumerate(f.read_text(errors='replace').split("\n"),1):
            if l.startswith(("pf:","ca:")): continue
            lp=piega(l)
            for k,a in amm.items():
                for m in re.finditer(r"(?<![a-z])"+re.escape(k)+r"[^()\n]{0,40}\(([^()]{0,160})\)",lp):
                    par=m.group(1)
                    if re.search(r"meta|sotto|dai |avanzat|scalat|\bdv\b|ira|forma",par): continue
                    for campo,rx in (("CA",r"\bca (\d+)"),("pf",r"\b(\d+) pf\b|\bpf (\d+)")):
                        for mm in re.finditer(rx,par):
                            v=int(next(g for g in mm.groups() if g)); tot+=1
                            if a[campo] and v not in a[campo]: out.append((rel,i,k,campo,v,sorted(a[campo]),l.strip()[:160]))
print("confronti",tot,"scarti",len(out))
for o in out: print(*o,sep="\t")
