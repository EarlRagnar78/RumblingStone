"""Coppie di frasi quasi uguali in file diversi del repo, che parlano dello stesso nome."""
import difflib, json, re, sys, itertools, random
from pathlib import Path
from collections import defaultdict
R=Path(__file__).resolve().parents[4]
DIRS=["07_il Portale Della Forgia Eterna","08_La Battaglia Di Hammerfist","09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist","10-stand-alone","Bestiario"]
NOME=re.compile(r"\b[A-ZÀ-Ý][a-zà-ÿ'’]{3,}(?:\s[A-ZÀ-Ý][a-zà-ÿ'’]{3,})?")
COMUNI={"Read","Scena","Sessione","Regia","Appendice","Tattica","Mappa","Nota","Fonte","Corona","Sala","Forgia"}
frasi=[]
for d in DIRS:
    for f in (R/d).rglob("*.md"):
        rel=f.relative_to(R).as_posix()
        if "/homebrew/" in rel or "_ARCHIVIO" in rel or rel.endswith(".hb.md") or "/_testi-altrui/" in rel: continue
        for i,r in enumerate(f.read_text(errors="replace").split("\n"),1):
            r=r.strip().lstrip(">*-# ").strip()
            if r.startswith("|") or "🟩" in r or "`" in r: continue
            for s in re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý«*])", r):
                s=re.sub(r"\*+","",s).strip()
                if 50<=len(s)<=300: frasi.append((rel,i,s))
idx=defaultdict(list)
for k,(f,i,s) in enumerate(frasi):
    t=re.sub(r"^\S+","",s)
    for n in set(NOME.findall(t))-COMUNI: idx[n].append(k)
coppie={}
for n,ks in idx.items():
    if len(ks)>600: random.seed(1); ks=random.sample(ks,600)
    for a,b in itertools.combinations(ks,2):
        fa,fb=frasi[a],frasi[b]
        if fa[0]==fb[0] or fa[2]==fb[2]: continue
        sm=difflib.SequenceMatcher(None,fa[2],fb[2])
        if sm.real_quick_ratio()<0.55 or sm.quick_ratio()<0.55: continue
        r=sm.ratio()
        if 0.55<=r<0.95: coppie[(min(a,b),max(a,b))]=r
out=[{"a":frasi[a][0]+":"+str(frasi[a][1]),"b":frasi[b][0]+":"+str(frasi[b][1]),"prima":frasi[a][2],"dopo":frasi[b][2],"sim":round(r,2)} for (a,b),r in coppie.items()]
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False,indent=0)
print(len(frasi),"frasi,",len(out),"coppie")
