import pymupdf,sys,hashlib
from pathlib import Path
tp=td=0; diff={}
for p in sorted(Path('main').glob('*.pdf')):
    a=pymupdf.open(p); b=pymupdf.open(Path('ramo')/p.name)
    tp+=len(a); assert len(a)==len(b),p.name
    n=0
    for i in range(len(a)):
        ha=hashlib.md5(a[i].get_pixmap(dpi=40).samples).hexdigest(); hb=hashlib.md5(b[i].get_pixmap(dpi=40).samples).hexdigest()
        if ha!=hb: n+=1
    if n: diff[p.name]=n
    td+=n
print('pagine',tp,'diverse',td,diff)
a=pymupdf.open('main/DRAPPO-PROP-STAMPA.pdf'); b=pymupdf.open('ramo/DRAPPO-PROP-STAMPA.pdf')
print(a.metadata); print(b.metadata)
