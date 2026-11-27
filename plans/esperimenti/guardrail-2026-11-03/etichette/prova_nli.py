"""Le contraddizioni etichettate: NLI contro il confronto deterministico.

Uso: prova_nli.py coppie-etichettate.json [--modello NOME]
"""
import json, re, sys, argparse

NEG = re.compile(r"\b(non|niente|nessun[oa]?|mai|senza|not|no|never)\b", re.I)
NUM = re.compile(r"[+−-]?\d+(?:[.,]\d+)?")
NOME = re.compile(r"\b[A-ZÀ-Ý][\w'’À-ÿ]{2,}")

def numeri(s): return sorted(n.replace("−","-") for n in NUM.findall(s))
def negazioni(s): return len(NEG.findall(s))
def nomi(s):
    t = re.sub(r"(^|[.!?:»«*>\-]\s*)\S+", " ", s)   # la parola a inizio frase non è un nome
    return set(NOME.findall(t))

def deterministico(a, b):
    """1 se cambia un numero, una negazione o un nome proprio; 0 altrimenti."""
    return int(numeri(a) != numeri(b) or negazioni(a) != negazioni(b) or bool(nomi(a) ^ nomi(b)))

def solo_numeri(a, b):
    return int(numeri(a) != numeri(b))

def auc(y, s):
    pos=[x for x,t in zip(s,y) if t]; neg=[x for x,t in zip(s,y) if not t]
    return sum((p>n)+0.5*(p==n) for p in pos for n in neg)/(len(pos)*len(neg))

def prf(y, p):
    tp=sum(a and b for a,b in zip(y,p)); fp=sum((not a) and b for a,b in zip(y,p)); fn=sum(a and not b for a,b in zip(y,p))
    pr=tp/(tp+fp) if tp+fp else 0; rc=tp/(tp+fn) if tp+fn else 0
    return round(pr,3), round(rc,3), round(2*pr*rc/(pr+rc),3) if pr+rc else 0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("coppie"); ap.add_argument("--modello", default="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7")
    a=ap.parse_args()
    d=json.load(open(a.coppie)); y=[x["etichetta"]=="C" for x in d]
    out={"coppie":len(d),"contraddizioni":sum(y)}
    for nome,f in (("solo numeri",solo_numeri),("numeri+negazioni+nomi",deterministico)):
        p=[bool(f(x["prima"],x["dopo"])) for x in d]
        out[nome]=dict(zip(("precisione","richiamo","F1"),prf(y,p)))
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tok=AutoTokenizer.from_pretrained(a.modello); m=AutoModelForSequenceClassification.from_pretrained(a.modello).eval()
    lab={v.lower():k for k,v in m.config.id2label.items()}
    ic=lab["contradiction"]
    s=[]
    with torch.no_grad():
        for x in d:
            # simmetrico: la contraddizione vale nei due sensi, si prende il massimo
            pr=[]
            for p,h in ((x["prima"],x["dopo"]),(x["dopo"],x["prima"])):
                z=m(**tok(p,h,return_tensors="pt",truncation=True,max_length=256)).logits.softmax(-1)[0]
                pr.append(float(z[ic]))
            s.append(max(pr))
    out["NLI AUC"]=round(auc(y,s),3)
    out["NLI argmax(>0,5)"]=dict(zip(("precisione","richiamo","F1"),prf(y,[v>0.5 for v in s])))
    best=max(((t,prf(y,[v>t for v in s])[2]) for t in sorted(set(s))), key=lambda z:z[1])
    out["NLI soglia migliore (ottimista: scelta sugli stessi dati)"]={"soglia":round(best[0],3),"F1":best[1]}
    # combinazione: il deterministico propone, l'NLI conferma
    det=[bool(deterministico(x["prima"],x["dopo"])) for x in d]
    out["deterministico E NLI>0,5"]=dict(zip(("precisione","richiamo","F1"),prf(y,[a and v>0.5 for a,v in zip(det,s)])))
    out["deterministico O NLI>0,5"]=dict(zip(("precisione","richiamo","F1"),prf(y,[a or v>0.5 for a,v in zip(det,s)])))
    for x,v in zip(d,s): x["nli"]=round(v,3); x["det"]=deterministico(x["prima"],x["dopo"])
    json.dump(d,open(a.coppie.replace(".json","-punteggi.json"),"w"),ensure_ascii=False,indent=1)
    print(json.dumps(out,ensure_ascii=False,indent=1))
main()
