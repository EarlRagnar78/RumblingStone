import re, sys
from pathlib import Path
sys.path.insert(0,'scripts')
import conformita_statblocchi as C
from misura_standard_tavolo import chiave, piega
tot=0; out=[]
for p in C.master_di_default():
    t=p.read_text(errors='replace'); righe=t.split("\n")
    bl=list(C._recinti_del_master(t))
    ammessi={}
    dentro=set()
    for b in bl:
        k=chiave(b["sb"].nome)
        if not k: continue
        a=ammessi.setdefault(k,{"CA":set(),"pf":set()})
        testo=" ".join([b["sb"].ca,b["sb"].ca_dettaglio,b["prosa"].split("\n")[0] if b["prosa"] else ""])
        a["CA"]|={int(x) for x in re.findall(r"\b(\d{2})\b",b["sb"].ca+" "+(b["sb"].ca_dettaglio or ""))}
        a["CA"]|={int(x) for x in re.findall(r"\*\*CA (\d+)",b["prosa"])}|{int(x) for x in re.findall(r"\*\*(\d+) con",b["prosa"])}
        a["pf"]|={int(x) for x in re.findall(r"\d+",b["sb"].pf or "")}|{int(x) for x in re.findall(r"(\d+) in Ira",b["sb"].pf_dado or "")}
        n0=b["riga"]; n1=b["riga_prosa"]+b["prosa"].count("\n")
        dentro|=set(range(n0,n1+1))
    for i,l in enumerate(righe,1):
        if i in dentro: continue
        lp=piega(l)
        for k,a in ammessi.items():
            for m in re.finditer(r"(?<![a-z])"+re.escape(k),lp):
                fin=l[m.end():m.end()+120]
                fin=re.split(r"[.;|]\s|\(.*?(adulto|vecchio)",fin)[0]
                for campo,rx in (("CA",r"\bCA (\d+)"),("pf",r"\b(\d+) pf\b|\bpf (\d+)")):
                    for mm in re.finditer(rx,fin):
                        v=int(next(g for g in mm.groups() if g)); tot+=1
                        if a[campo] and v not in a[campo]:
                            out.append((p.name,i,k,campo,v,sorted(a[campo]),l.strip()[:150]))
print("confronti",tot,"scarti",len(out))
for o in out: print(o)
