"""Indice dei nomi inglesi dei talenti PF1e di tutti i manuali, da Archives of Nethys.

Uso: python3 -I indice_talenti_pf1.py <Feats.aspx salvata> > scripts/talenti_manuali_pf1.tsv
Solo i nomi (ADR-0103): la pagina elenco di aonprd.com/Feats.aspx dà nome, prerequisiti e
una riga di descrizione; qui si tiene solo il nome.
"""
import html
import re
import sys

s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
nomi = sorted({html.unescape(m).strip() for m in re.findall(r'FeatDisplay\.aspx\?ItemName=([^"]+)"', s)},
              key=str.casefold)
print("# Nomi inglesi dei talenti Pathfinder 1e di tutti i manuali (solo nomi, niente testo).")
print("# Fonte: Archives of Nethys, https://aonprd.com/Feats.aspx, letto il 2026-11-07.")
print("# Generata da plans/esperimenti/regole-ufficiali-2026-11-07/abbinamenti/indice_talenti_pf1.py")
print("inglese\tfonte")
for n in nomi:
    print(f"{n}\taonprd")
