"""Archetipi di classe: firma italiana (Golarion) contro firma aon, unica nella classe.
Misura la precisione sulle 95 coppie con link (verità nota), poi abbina i dubbi.
Uso: python3 -I abbina_aon.py <arch.json> <wikitext.json> <firme.json> <lessico_pf1.tsv> <out.json>"""
import json,re,sys,collections
arch=json.load(open(sys.argv[1])); w=json.load(open(sys.argv[2])); aon=json.load(open(sys.argv[3]))
CL={}
for r in open(sys.argv[4],encoding='utf-8'):
    c=r.rstrip('\n').split('\t')
    if len(c)>=3 and c[2]=='classe': CL[c[0]]=c[1]
TIPO=r'\((Str|Sop|Mag)(?:(?:,| o|/) ?(Str|Sop|Mag))*\)'
M={'Str':'Ex','Sop':'Su','Mag':'Sp'}
def firma(testo):
    out=[];att=None
    for riga in testo.split('\n'):
        m=re.match(r'^(=+)\s*(.*?)\s*=+\s*$',riga)
        if m:
            t=re.search(TIPO,m.group(2))
            if t:
                tp='/'.join(sorted({M[x] for x in re.findall(r'Str|Sop|Mag',t.group(0))}))
                att=[0,tp]; out.append(att)
            else: att=None
            continue
        if att and att[0]==0:
            n=re.search(r'\b[Aa]l(?:l\')?\s*(\d+)°\s*livello',riga)
            if n: att[0]=int(n.group(1))
            elif riga.strip(): att[0]=-1  # primo paragrafo senza livello
    return tuple(sorted((max(a,0),b) for a,b in out))
def blocchi(p,t):
    """(nome, testo) per archetipo: pagine core a ==X==, pagine Golarion fino a 'Fonte:'."""
    if p.endswith('/Archetipi'):
        parti=re.split(r'^==([^=].*?)==\s*$',t,flags=re.M)
        return [(parti[i].strip(),parti[i+1]) for i in range(1,len(parti),2)]
    out=[];prima=0
    for m in re.finditer(r'^Fonte:.*$',t,flags=re.M):
        out.append((None,t[prima:m.start()],m.group(0))); prima=m.end()
    return out
# indice aon per classe
per_cl=collections.defaultdict(dict)
for fixed,v in aon.items():
    if v['firma']: per_cl[v['classe']][v['nome']]=tuple(tuple(x) for x in v['firma'])
def unico(cls_it,f,altre_it):
    en=CL.get(cls_it); 
    if not en: return None
    en=en.split(' (')[0] if en.endswith('(Unchained)') and en.split(' (')[0] not in per_cl else en
    tab=per_cl.get(en.split(' (')[0],{}) 
    cand=[n for n,g in tab.items() if g==f]
    return cand[0] if len(cand)==1 and altre_it[f]==1 and len(f)>=2 else None
# 1) verità nota: coppie Golarion con link
firme_it=collections.defaultdict(collections.Counter); voci=[]
for p,t in w.items():
    cls=p.split('/')[0] if '/' in p else p[:-len(' di Golarion')]
    if p.endswith('/Archetipi'):
        for nome,testo in blocchi(p,t):
            f=firma(testo); voci.append((cls,nome,f,None)); firme_it[cls][f]+=1
noti={(r['classe'],r['it']):r['en'] for r in arch['coppie'] if r['via']=='golarion→aon'}
# firme dei noti dalle pagine Golarion
for p,t in w.items():
    if not p.endswith(' di Golarion'): continue
    cls=p[:-len(' di Golarion')]
    for _,testo,fonte in blocchi(p,t):
        h=[b for a,b in re.findall(r'^(=+)\s*(.*?)\s*=+\s*$',testo,flags=re.M) if not re.search(TIPO,b) and b!='Archetipi' and not b.endswith(' di Golarion')]
        if not h: continue
        nome=re.sub(r'\{\{.*?\}\}','',h[0]).strip()
        if (cls,nome) in noti:
            f=firma(testo); voci.append((cls,nome,f,noti[(cls,nome)])); firme_it[cls][f]+=1
giusti=sbagliati=astenuti=0; errori=[]
for cls,nome,f,vero in voci:
    if vero is None: continue
    g=unico(cls,f,firme_it[cls])
    if g is None: astenuti+=1
    elif g==vero: giusti+=1
    else: sbagliati+=1; errori.append((cls,nome,vero,g))
print(f'verità nota {giusti+sbagliati+astenuti}: giusti {giusti}, sbagliati {sbagliati}, astenuti {astenuti}'); print(errori[:10])
# 2) controllo sulle 141 coppie per firma PRD
prd={(r['classe'],r['it']):r['en'] for r in arch['coppie'] if r['via']=='firma'}
acc=dis=0; disac=[]
for cls,nome,f,vero in voci:
    if vero is None and (cls,nome) in prd:
        g=unico(cls,f,firme_it[cls])
        if g is None: continue
        if g==prd[(cls,nome)]: acc+=1
        else: dis+=1; disac.append((cls,nome,prd[(cls,nome)],g))
print(f'PRD contro aon: d\'accordo {acc}, in disaccordo {dis}'); print(disac[:20])
# 3) dubbi
nuovi=[]
gia={(r['classe'],r['it']) for r in arch['coppie']}
for cls,nome,f,vero in voci:
    if vero is None and (cls,nome) not in gia:
        g=unico(cls,f,firme_it[cls])
        if g: nuovi.append({'classe':cls,'it':nome,'en':g,'via':'firma aon'})
print('nuovi da aon',len(nuovi),'su',sum(1 for v in voci if v[3] is None and (v[0],v[1]) not in gia))
json.dump({'nuovi':nuovi,'errori':errori,'disaccordi':disac},open(sys.argv[5],'w'),ensure_ascii=False,indent=1)
