"""Firme dei privilegi degli archetipi dalle pagine aon scaricate.
Uso: python3 -I firme_aon.py <dir aon> <out.json>"""
import re,html,glob,json,sys,os
D=sys.argv[1]; out={}
cls_di={}
for f in glob.glob(D+'/lista-*.html'):
    c=os.path.basename(f)[6:-5]
    for u in re.findall(r'ArchetypeDisplay.aspx\?FixedName=([^"]*)',open(f,encoding='utf-8',errors='ignore').read()):
        cls_di.setdefault(html.unescape(u),c)
for fixed,c in cls_di.items():
    f=D+'/pag/'+re.sub(r'[^A-Za-z0-9-]','_',fixed)+'.html'
    if not os.path.exists(f) or os.path.getsize(f)<1000: continue
    t=open(f,encoding='utf-8',errors='ignore').read()
    t=html.unescape(re.sub(r'<[^>]+>','\n',t))
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    i=t.find('\nSource\n'); 
    nome=t[:i].strip().split('\n')[-1].strip() if i>0 else None
    firma=[]
    for m in re.finditer(r'\n([^\n]{1,80}?) \(((?:Ex|Su|Sp)(?:(?:,| or|/) ?(?:Ex|Su|Sp))*)\)\n:?\s*([^\n]*)',t[i:]):
        tp='/'.join(sorted(set(re.findall(r'Ex|Su|Sp',m.group(2)))))
        lv=re.search(r'\b[Aa]t (\d+)(?:st|nd|rd|th) level',m.group(3))
        firma.append((int(lv.group(1)) if lv else 0,tp))
    out[fixed]={'classe':c,'nome':nome,'firma':sorted(firma)}
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(out)); 
for k in list(out)[:3]: print(k,out[k])
