import sys,re,statistics as st,importlib
sys.path.insert(0,'scripts'); sys.path.insert(0,sys.argv[1])
import misura_craft as mc
import coppie_a; importlib.reload(coppie_a)
from coppie_a import COPPIE, CONTROLLI
F=mc._FINE_FRASE_BOX
def ppf(t): return [len(f.split()) for f in F.split(t) if len(f.split())>=2]
def ult(t):
    fs=[f for f in F.split(t) if f.strip()!="Che fate?"]; return fs[-1]
allb=[];alll=[]
for k,(b,l) in COPPIE.items():
    pb,pl=ppf(b),ppf(l); allb+=pb; alll+=pl
    wb,wl=len(b.split()),len(l.split())
    sb,sl=mc.dettagli_sensoriali(b),mc.dettagli_sensoriali(l)
    flag=[]
    if abs(wb-wl)/max(wb,wl)>0.10: flag.append("LUNGHEZZA")
    if (sb!=sl)!=(k in CONTROLLI): flag.append(f"SENSI")
    if len(mc.avverbi_mente(b))!=len(mc.avverbi_mente(l)): flag.append("MENTE")
    if ult(b)!=ult(l): flag.append("ULTIMA")
    if re.search(r"\b(sembra|pare|vedete|entrate|ti accorgi)\b",b+l,re.I): flag.append("P1")
    if b.count("«")!=l.count("«") or b.count(";")+l.count(";") or "—" in b+l or "(" in b+l: flag.append("SEGNI")
    print(f"{k:2} parole {wb}/{wl} med {st.median(pb):.0f}/{st.median(pl):.0f} frasi {len(pb)}/{len(pl)} sensi {sb}/{sl}",*flag)
print(f"mediana complessiva breve {st.median(allb)} lunga {st.median(alll)}; oltre 4 frasi: breve {sum(len(ppf(b))>4 for b,_ in COPPIE.values())}, lunga {sum(len(ppf(l))>4 for _,l in COPPIE.values())}")
