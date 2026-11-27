"""Abbina gli archetipi di classe di Golarion (it) al PRD PF1e (en).
1) pagine «X di Golarion»: il link Fonte dà il nome inglese.
2) pagine «X/Archetipi»: firma = multinsieme dei livelli dei privilegi, unica nella classe da entrambi i lati.
Uso: python3 -I archetipi.py <wikitext.json> <dir PSRD> <lessico_pf1.tsv> <out.json>"""
import json,re,sys,sqlite3,glob,urllib.parse,collections
w=json.load(open(sys.argv[1])); prd=sys.argv[2]; tsv=sys.argv[3]
CL={}
for r in open(tsv,encoding='utf-8'):
    c=r.rstrip('\n').split('\t')
    if len(c)>=3 and c[2]=='classe': CL[c[0]]=c[1]
EN={}
for f in glob.glob(prd+'/*.db'):
    db=sqlite3.connect(f)
    for sid,name,sub,l,rg in db.execute("select section_id,name,subtype,lft,rgt from sections where type='class_archetype'"):
        lv=[]
        for (sid2,b) in db.execute("select section_id,body from sections where lft>? and rgt<? and type='ability' order by lft",(l,rg)):
            tp=[x[0][:2] for x in db.execute("select ability_type from ability_types where section_id=?",(sid2,))]
            if not tp: continue
            m=re.search(r'\b[Aa]t (\d+)(?:st|nd|rd|th) level',b or '')
            lv.append((int(m.group(1)) if m else 0,'/'.join(sorted(tp))))
        EN.setdefault(sub,{})[name]=tuple(sorted(lv))
TIPO=r'\((?:Str|Sop|Mag|Str o Sop|Sop o Mag)\)'
def blocchi_core(t):
    out=[];cur=None
    for riga in t.split('\n'):
        m=re.match(r'^==([^=].*?)==\s*$',riga)
        if m: cur={'nome':m.group(1).strip(),'liv':[]}; out.append(cur); continue
        m=re.match(r'^===+\s*(.*?)\s*===+\s*$',riga)
        if m and cur is not None and re.search(TIPO,m.group(1)):
            tp=re.search(TIPO,m.group(1)).group(0)[1:-1]
            tp='/'.join(sorted({'Str':'Ex','Sop':'Su','Mag':'Sp'}[x] for x in tp.split(' o ')))
            cur['liv'].append([None,tp]); continue
        if cur and cur['liv'] and cur['liv'][-1][0] is None:
            n=re.search(r'\b[Aa]l(?:l\')?\s*(\d+)°\s*livello',riga)
            if n: cur['liv'][-1][0]=int(n.group(1))
    for b in out: b['firma']=tuple(sorted((x[0] or 0,x[1]) for x in b['liv']))
    return [b for b in out if b['liv']]
ris=[];dubbi=[]
for p,t in w.items():
    if p.endswith(' di Golarion'):
        cls=p[:-len(' di Golarion')]
        prima=0
        for m in re.finditer(r'^Fonte:.*$',t,flags=re.M):
            pezzo=t[prima:m.start()]; prima=m.end()
            l=re.match(r'^Fonte:\s*\[(\S+)\s+([^\]]+)\]',m.group(0))
            if not l or 'ArchetypeDisplay' not in l.group(1): continue
            url,label=l.group(1),l.group(2).strip()
            h=[b for a,b in re.findall(r'^(=+)\s*(.*?)\s*=+\s*$',pezzo,flags=re.M)
               if not re.search(TIPO,b) and b not in ('Archetipi',p) and not b.endswith(' di Golarion')]
            h=[re.sub(r'\{\{.*?\}\}','',x).strip() for x in h]
            if not h: continue
            nome=h[0]
            fixed=urllib.parse.unquote(url.split('FixedName=')[1])
            suf=re.sub(r'\s*\(.*?\)','',' '.join(fixed.split()[1:])).strip()
            lab=re.sub(r'\s*\(.*?\)','',label).strip()
            en=lab if suf.endswith(lab) else suf
            ris.append({'it':nome,'en':en,'classe':cls,'via':'golarion→aon','fixed':fixed,'titoli':h[:3]})
    elif p.endswith('/Archetipi'):
        cls=p[:-len('/Archetipi')]; en_cls=CL.get(cls,'').lower()
        sub={'monk (unchained)':'monk'}.get(en_cls,en_cls)
        it=blocchi_core(t); en=EN.get(sub,{})
        fi=collections.Counter(b['firma'] for b in it); fe=collections.Counter(en.values())
        inv={v:k for k,v in en.items()}
        for b in it:
            if fi[b['firma']]==1 and fe.get(b['firma'])==1 and len(b['firma'])>=2:
                ris.append({'it':b['nome'],'en':inv[b['firma']],'classe':cls,'via':'firma','firma':b['firma']})
            else: dubbi.append({'it':b['nome'],'classe':cls,'firma':b['firma'],'fi':fi[b['firma']],'fe':fe.get(b['firma'],0)})
json.dump({'coppie':ris,'dubbi':dubbi},open(sys.argv[4],'w'),ensure_ascii=False,indent=1)
c=collections.Counter(r['via'] for r in ris); print(c, 'dubbi',len(dubbi), 'archetipi PRD',sum(len(v) for v in EN.values()))
