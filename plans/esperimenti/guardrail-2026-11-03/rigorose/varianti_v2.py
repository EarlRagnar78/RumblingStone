"""Varianti dei nomi, configurazione rigorosa.
- nomi propri: parole maiuscole del repo che NON compaiono mai in minuscolo (quindi non sono parole italiane) e compaiono >=10 volte
- variante: parola maiuscola rara (<=3), mai in minuscolo, non genitivo inglese ('s), stessa iniziale,
  distanza di modifica <=2 dal nome e lunghezza >=5
"""
import re, sys, collections
from pathlib import Path
R=Path(sys.argv[1])
DIRS=["07_il Portale Della Forgia Eterna","08_La Battaglia Di Hammerfist","09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist","10-stand-alone","Bestiario","campaign","PG"]
cap=collections.Counter(); low=set(); dove={}
for d in DIRS:
    for f in (R/d).rglob("*.md"):
        rel=f.relative_to(R).as_posix()
        if "/homebrew/" in rel or rel.endswith(".hb.md") or "/_testi-altrui/" in rel: continue
        t=f.read_text(errors="replace")
        t=re.sub(r"\]\([^)]*\)|`[^`]*`|https?://\S+","",t)
        for m in re.finditer(r"\b[\wÀ-ÿ']+\b",t):
            w=m.group(0)
            if w[0].islower(): low.add(w.lower())
            elif w[0].isupper() and w[1:].islower():
                cap[w]+=1; dove.setdefault(w,rel)
def lev(a,b):
    p=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        c=[i]
        for j,cb in enumerate(b,1): c.append(min(p[j]+1,c[j-1]+1,p[j-1]+(ca!=cb)))
        p=c
    return p[-1]
nomi=[w for w,n in cap.items() if n>=10 and w.lower() not in low and len(w)>=5]
rari=[w for w,n in cap.items() if n<=3 and w.lower() not in low and len(w)>=5 and not w.endswith("'s") and "'" not in w]
out=[]
for r in rari:
    for n in nomi:
        if r[0]==n[0] and abs(len(r)-len(n))<=2 and r!=n and lev(r.lower(),n.lower())<=2:
            out.append((lev(r.lower(),n.lower()),r,cap[r],n,cap[n],dove[r]))
out.sort()
print(f"# nomi propri {len(nomi)}, parole rare candidate {len(rari)}, varianti {len(out)}")
for o in out: print(*o,sep="\t")
