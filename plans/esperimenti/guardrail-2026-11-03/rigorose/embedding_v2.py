"""Ripetizioni fra box, configurazione rigorosa: a livello di FRASE (non di box intero), solo fra box di
scene diverse, escluse le copie volute (4-grammi in comune >= 0,5 = copia, la trova già il confronto
lessicale) e le frasi sotto le 8 parole. Soglia 0,85 sul coseno."""
import sys, re, json, os
sys.path.insert(0, 'scripts'); os.environ["HF_HUB_DISABLE_XET"] = "1"
import torch; torch.set_num_threads(2)
import misura_craft as mc
from pathlib import Path
files = sorted(p for p in Path('.').glob('0[0-9]_*/**/*.md')) + sorted(Path('10-stand-alone').glob('**/*.md'))
files = [p for p in files if not any(x in str(p) for x in mc.ESCLUSI) and not any(x in p.name for x in mc.ESCLUSI_NOME)
         and 'Immagini' not in str(p) and ('DEF-' in p.name or p.parts[0].startswith(('08_','09_','10-')))]
fr = []
for p in files:
    for k, b in enumerate(mc.box_read_aloud(p.read_text(errors='replace'))):
        for s in re.split(r"(?<=[.!?»])\s+", mc.corpo_del_box(b)):
            s = s.strip()
            if len(s.split()) >= 8: fr.append((str(p), k, s))
def ng(t, n=4):
    w = re.findall(r"\w+", t.lower()); return {tuple(w[i:i+n]) for i in range(len(w)-n+1)}
G = [ng(s) for *_, s in fr]
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
E = m.encode([s for *_, s in fr], normalize_embeddings=True, batch_size=64)
S = E @ E.T
import numpy as np
iu = np.argwhere(np.triu(S, 1) >= float(sys.argv[2]))
out = []
for i, j in iu:
    a, b = fr[i], fr[j]
    if (a[0], a[1]) == (b[0], b[1]) or a[2] == b[2]: continue
    jac = len(G[i] & G[j]) / (len(G[i] | G[j]) or 1)
    if jac >= 0.5: continue
    out.append({"cos": round(float(S[i, j]), 3), "jac": round(jac, 2), "a": a[0], "b": b[0], "fa": a[2], "fb": b[2]})
out.sort(key=lambda x: -x["cos"])
json.dump({"frasi": len(fr), "coppie": out}, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print("frasi", len(fr), "coppie sopra soglia", len(out))
