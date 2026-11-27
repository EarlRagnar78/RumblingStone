"""Razze PF1e: nome italiano da Golarion, nome inglese dal link della pagina a d20pfsrd.

La pagina italiana porta il link alla pagina inglese (API MediaWiki di Golarion, exturlusage
su www.d20pfsrd.com/races/). Dall'ultimo pezzo dell'URL (dwarf, arg-catfolk) si cerca la
sezione «race» del PRD in cache (Core Rulebook e Advanced Race Guide): si tiene la coppia solo
se il pezzo coincide con un titolo del PRD, al singolare o al plurale. Il nome inglese scritto
nella tabella è il titolo del PRD così com'è (Dwarves, Catfolk). Stampa le righe TSV e le scartate.
Uso: python3 -I abbina_razze.py <cartella PSRD-Data>
"""
import json, sqlite3, subprocess, sys, urllib.parse

def golarion(**p):
    u = 'https://golarion.altervista.org/api.php?' + urllib.parse.urlencode({**p, 'format': 'json'})
    return json.loads(subprocess.run(['curl', '-sS', '-m', '60', u], capture_output=True, text=True).stdout)

def chiave(s):
    s = s.lower().replace(' ', '-')
    for fine, sost in (('ves', 'f'), ('es', 'e'), ('s', '')):
        if s.endswith(fine) and s not in ('strix', 'svirfneblin'):
            return s[: -len(fine)] + sost
    return s

prd = {}
for libro in ('cr', 'arg'):
    c = sqlite3.connect(f'{sys.argv[1]}/book-{libro}.db')
    for (nome,) in c.execute("select name from sections where type='race'"):
        prd.setdefault(chiave(nome), nome)

d = golarion(action='query', list='exturlusage', euquery='www.d20pfsrd.com/races/', eulimit=500, euprop='title|url')
righe, scarti, visti = [], [], set()
for x in d['query']['exturlusage']:
    it = x['title'].removeprefix('Razze/')
    pezzo = x['url'].rstrip('/').rsplit('/', 1)[1].removeprefix('arg-')
    en = prd.get(chiave(pezzo)) or prd.get(pezzo)
    if not en:
        scarti.append((it, x['url'], 'non nel PRD in cache')); continue
    if en in visti:
        scarti.append((it, x['url'], f'link già usato da un\'altra pagina per {en}')); continue
    visti.add(en)
    righe.append(f'{it}\t{en}\trazza\tgolarion→d20pfsrd')
print('\n'.join(sorted(righe)))
print(f'# tenute {len(righe)}, PRD {len(set(prd.values()))}, mancanti: {sorted(set(prd.values()) - visti)}', file=sys.stderr)
for s in scarti: print('# scartata', *s, sep='\t', file=sys.stderr)
