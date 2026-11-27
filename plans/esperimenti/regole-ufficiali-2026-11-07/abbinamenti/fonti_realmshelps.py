"""Aggiunge il manuale ai talenti 3.5 che nell'indice non hanno sigla.

Uso: python3 -I fonti_realmshelps.py <cartella con le pagine charbuild/feat di realmshelps> scripts/talenti_manuali_35.tsv
Le pagine si scaricano dai link di https://www.realmshelps.net/cgi-bin/feat-form.pl. Si legge solo
il nome (<h1>) e il campo «Source»: niente testo delle regole (ADR-0103).
"""
import glob
import html
import os
import re
import sys
import unicodedata


def norma(t: str) -> str:
    t = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>|\[[^\]]*\]", "", t)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


fonti = {}
for p in glob.glob(os.path.join(sys.argv[1], "*.html")):
    s = open(p, encoding="utf-8", errors="replace").read()
    n = re.search(r"<h1>(.*?)</h1>", s, re.S)
    f = re.search(r"<strong>Source:?</strong>:?\s*(.*?)<br", s, re.S)
    if n and f:
        fonti[norma(html.unescape(n.group(1)))] = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", f.group(1)))).strip()
righe = open(sys.argv[2], encoding="utf-8").read().split("\n")
for i, r in enumerate(righe):
    if r.startswith(("#", "inglese\t")) or "\t" not in r:
        continue
    c = r.split("\t")
    if not c[1] and norma(c[0]) in fonti:
        c[1] = fonti[norma(c[0])]
        righe[i] = "\t".join(c)
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(righe))
