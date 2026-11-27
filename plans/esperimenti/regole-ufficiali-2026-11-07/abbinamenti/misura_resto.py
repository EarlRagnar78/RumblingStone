import json,re,collections,urllib.parse,html,sys
res=json.load(open('tutti-link.json'))
tsv=[l.rstrip('\n').split('\t') for l in open(sys.argv[1],encoding='utf-8') if l.count('\t')>=2 and not l.startswith('#')]
tab=collections.defaultdict(dict)
for r in tsv: tab[r[0]][r[1].lower()]=r[2]
A=lambda s:''.join(sorted(re.sub(r'[^a-z]','',re.sub(r'\s*\([A-Z0-9]{1,5}\)$','',s).lower())))
KIND={'FeatDisplay':'talento','SpellDisplay':'incantesimo','MonsterDisplay':'mostro'}
for k in ['MagicArmorDisplay','MagicArtifactsDisplay','MagicCursedDisplay','MagicRingsDisplay','MagicRodsDisplay','MagicStavesDisplay','MagicWeaponsDisplay','MagicWondrousDisplay']: KIND[k]='oggetto magico'
aon=collections.defaultdict(dict)
for l in open('../aon/liste/tutti.txt'):
    d,n=l.strip().split('?',1); d=d[:-5]; n=html.unescape(urllib.parse.unquote(n.split('=',1)[1])).strip()
    if d in KIND: aon[KIND[d]].setdefault(A(n),set()).add(n)
D20=[('magic/all-spells','incantesimo'),('bestiary/monster-listings','mostro'),('magic-items/','oggetto magico'),('feats/','talento')]
def abbina(v):
    for u in v:
        m=re.search(r'^https?://(?:www\.|legacy\.)?aonprd\.com/(\w+)\.aspx\?(?:ItemName|FinalName)=([^&#]+)',u)
        if m and m.group(1) in KIND:
            return re.sub(r'\s*\([A-Z0-9]{1,5}\)$','',urllib.parse.unquote(m.group(2)).strip()),KIND[m.group(1)],'aon'
        pu=urllib.parse.urlparse(u)
        if pu.hostname in ('d20pfsrd.com','www.d20pfsrd.com') and 'mythic' not in pu.path:
            path=pu.path.lstrip('/').lower(); kind=next((k for p,k in D20 if path.startswith(p)),None)
            if not kind: continue
            s=[x for x in path.rstrip('/').split('/') if x][-1]; s=re.sub(r'-cr-[\w-]*$','',s); s=re.sub(r'-\d+$','',s)
            c=aon[kind].get(A(s),set())
            return (next(iter(c)),kind,'d20') if len(c)==1 else None
    return None
ok=collections.Counter(); ko=collections.defaultdict(list); nuove=[]
for t,v in res.items():
    it=t.split('/',1)[1] if t.startswith(('Incantesimi/','Talenti/','Mostri/')) else t
    if '/' in it: continue
    r=abbina(v)
    if not r: continue
    en,kind,via=r
    if it in tab:
        if any(A(e)==A(en) for e in tab[it]): ok[via]+=1
        else: ko[via].append((it,en,list(tab[it])))
    else: nuove.append((it,en,kind,via))
print('verità nota: giuste',dict(ok),'diverse',{k:len(v) for k,v in ko.items()})
for k in ko: print(k,ko[k][:30])
json.dump({'nuove':nuove,'ko':ko,'ok':ok},open('resto.json','w'),ensure_ascii=False,indent=0)
print('nuove',len(nuove),collections.Counter(x[2] for x in nuove))
# filtro: un inglese da d20 vale solo se nessun altro titolo di Golarion punta allo stesso inglese
quanti=collections.Counter()
tutte=[]
for t,v in res.items():
    it=t.split('/',1)[1] if t.startswith(('Incantesimi/','Talenti/','Mostri/')) else t
    if '/' in it: continue
    r=abbina(v)
    if r: quanti[(r[1],A(r[0]))]+=1; tutte.append((it,)+r)
ok2=collections.Counter();ko2=collections.Counter()
for it,en,kind,via in tutte:
    if it in tab and quanti[(kind,A(en))]==1:
        (ok2 if any(A(e)==A(en) for e in tab[it]) else ko2)[via]+=1
print('con filtro unicità: giuste',dict(ok2),'diverse',dict(ko2))
nuove2=[(it,en,kind,via) for it,en,kind,via in tutte if it not in tab and (via=='aon' or quanti[(kind,A(en))]==1)]
print('nuove col filtro',len(nuove2),collections.Counter((x[2],x[3]) for x in nuove2))
json.dump(nuove2,open('resto-filtrato.json','w'),ensure_ascii=False,indent=0)
# righe della tabella che puntano a un inglese diverso da un link unico: sospette
sosp=[(it,en,list(tab[it])) for it,en,kind,via in tutte if it in tab and quanti[(kind,A(en))]==1 and not any(A(e)==A(en) for e in tab[it])]
json.dump(sosp,open('sospette.json','w'),ensure_ascii=False,indent=0); print('sospette',len(sosp),sosp[:20])
