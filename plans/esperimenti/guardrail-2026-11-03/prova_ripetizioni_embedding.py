import sys, re, json, os
sys.path.insert(0, 'scripts')
os.environ["HF_HUB_DISABLE_XET"] = "1"
import misura_craft as mc
from pathlib import Path
files = sorted(p for p in Path('.').glob('0[0-9]_*/**/*.md')) + sorted(Path('10-stand-alone').glob('**/*.md'))
files = [p for p in files if not any(x in str(p) for x in mc.ESCLUSI) and not any(x in p.name for x in mc.ESCLUSI_NOME)
         and 'Immagini' not in str(p) and ('DEF-' in p.name or p.parts[0].startswith(('08_','09_','10-')))]
box = []
for p in files:
    for b in mc.box_read_aloud(p.read_text(errors='replace')):
        c = mc.corpo_del_box(b)
        if len(c.split()) >= 25:
            box.append((str(p), c))
print("box", len(box), "file", len(files), file=sys.stderr)
def ng(t, n=4):
    w = re.findall(r"\w+", t.lower()); return {tuple(w[i:i+n]) for i in range(len(w)-n+1)}
G = [ng(c) for _, c in box]
from sentence_transformers import SentenceTransformer
m = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
E = m.encode([c for _, c in box], normalize_embeddings=True, batch_size=32)
import numpy as np
S = E @ E.T
pairs = []
for i in range(len(box)):
    for j in range(i+1, len(box)):
        if box[i][1] == box[j][1]: continue
        jac = len(G[i] & G[j]) / (len(G[i] | G[j]) or 1)
        pairs.append((float(S[i, j]), jac, i, j))
out = {"box": len(box),
       "sem_top": [(s, j, box[a][0], box[a][1][:160], box[b][0], box[b][1][:160]) for s, j, a, b in sorted(pairs, reverse=True)[:40]],
       "lex_top": [(s, j, box[a][0], box[a][1][:160], box[b][0], box[b][1][:160]) for s, j, a, b in sorted(pairs, key=lambda x: -x[1])[:40]]}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
