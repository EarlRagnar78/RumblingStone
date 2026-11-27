"""Nomi inglesi dei talenti 3.5 di tutti i manuali, con manuale e pagina (solo nomi, ADR-0103).

Fonte: «Dungeons & Dragons 3.5 Edition Index – Feats» di Chet Erez e Outlands (crystalkeep.com,
28 febbraio 2007), PDF letto con Firecrawl e salvato in markdown. Di ogni riga «| Nome [Tipi] |
(Sigla pNN) | …» si tengono il nome e il riferimento: prerequisiti e testo restano fuori.
Seconda fonte, solo nomi: l'elenco «All Feats From All sources» di Forgotten Realms Helps
(realmshelps.net/cgi-bin/feat-form.pl, letto con Firecrawl il 2026-11-07), 3.481 nomi senza manuale.
Uso: python3 -I indice_talenti_35.py <crystalkeep.md> <realmshelps.md> > scripts/talenti_manuali_35.tsv
"""
import re, sys
# riga di tabella: «| Nome [Tipi] | (Sigla pNN) |» oppure «| Nome [Tipi] (Sigla pNN) |  |»
RIGA = re.compile(r"^\|\s*(?P<n>[A-Z][^|\[(]{1,60}?)\s*(?:\[[^\]]*\])?\s*(?P<f1>(?:\([^)|]{2,40}\)\+?\s*)*)\|\s*(?P<f2>(?:\([^)|]{2,40}\)\+?\s*)*)\|")
# riga dell'indice iniziale: «Goad .............. 22, 172»
INDICE = re.compile(r"^(?P<n>[A-Z][A-Za-z'’,\- ()]{1,60}?)\s*\.{2,}\s*[\d, ]+\s*$")
voci = {}
fine_indice = False
for riga in open(sys.argv[1], encoding="utf-8"):
    riga = riga.rstrip("\n")
    if riga.startswith("General Feats") and voci:
        fine_indice = True
    m = RIGA.match(riga)
    if m and m.group("n").strip() != "Name":
        n = re.sub(r"\s+", " ", m.group("n")).strip(" *")
        rif = re.findall(r"\(([^)]+)\)", (m.group("f1") or "") + (m.group("f2") or ""))
        voci.setdefault(n, set()).update(r.strip() for r in rif if re.search(r"\bp\d", r))
        continue
    m = INDICE.match(riga.strip())
    if m and not fine_indice:
        voci.setdefault(re.sub(r"\s+", " ", m.group("n")).strip(), set())
fonti = {n: "crystalkeep" for n in voci}
if len(sys.argv) > 2:
    for m in re.finditer(r"^\| \[(?P<n>[^\]]+)\]\(https://www\.realmshelps\.net/charbuild/feat/", open(sys.argv[2], encoding="utf-8").read(), re.M):
        n = m.group("n").strip()
        if not n.startswith("[") and "realmshelps" not in fonti.get(n, ""):
            fonti[n] = fonti.get(n, "") + ("+" if n in voci else "") + "realmshelps"
            voci.setdefault(n, set())
print("# Nomi inglesi dei talenti D&D 3.5 di tutti i manuali, con sigla e pagina (solo nomi, niente testo).")
print("# Fonti: D&D 3.5 Edition Index – Feats, Chet Erez e Outlands (crystalkeep.com), 2007-02-28, con sigla e pagina;")
print("# «All Feats From All sources», Forgotten Realms Helps (realmshelps.net), letto il 2026-11-07, solo nomi.")
print("# Generato da plans/esperimenti/regole-ufficiali-2026-11-07/abbinamenti/indice_talenti_35.py.")
print("inglese\tmanuale\tfonte")
for n in sorted(voci):
    print(f"{n}\t{'; '.join(sorted(voci[n]))}\t{fonti[n]}")
print(f"# {len(voci)} nomi, {sum(1 for v in voci.values() if v)} con manuale", file=sys.stderr)
