"""NLI configurata: solo prosa, solo coppie sulla stessa entità nominata."""
import json, re, sys
NOME=re.compile(r"\b[A-ZÀ-Ý][a-zà-ÿ'’]{3,}(?:\s[A-ZÀ-Ý][a-zà-ÿ'’]{3,})?")
COMUNI={"Read","Scena","Sessione","Regia","Appendice","Tattica","Mappa","Nota","Fonte","Corona","Sala","Forgia","Iniziativa","Sensi","Difesa","Attacco","Statistiche","Faction","Role","Saves","Soffio","Ascoltare","Osservare","Tempra","Riflessi","Volontà","Talenti","Abilità","Mischia","Distanza","Variante","Atto","Echo","Ledger","Dopo","Prima","Quando","Questo","Questa","Nella","Nelle"}
CHIAVE=re.compile(r"^\s*[\w' ]{1,25}:\s")
def prosa(s):
    if CHIAVE.match(s) or "·" in s or "|" in s or "@" in s or "Read-aloud" in s: return False
    if len(re.findall(r"[+−-]?\d+", s))>4: return False
    return len(s.split())>=8
d=json.load(open(sys.argv[1])); out=[]
for x in d:
    if not (prosa(x["prima"]) and prosa(x["dopo"])): continue
    na=set(NOME.findall(re.sub(r"^\S+","",x["prima"])))-COMUNI
    nb=set(NOME.findall(re.sub(r"^\S+","",x["dopo"])))-COMUNI
    comuni=na&nb
    if not comuni: continue
    x["entita"]=sorted(comuni); out.append(x)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False,indent=0)
print(len(d),"->",len(out))
