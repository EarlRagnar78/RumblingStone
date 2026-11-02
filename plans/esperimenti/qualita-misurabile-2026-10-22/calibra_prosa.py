import json,re,sys,statistics as st,math
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parents[3]/'scripts'))
import misura_craft as mc
W=re.compile(r"[A-Za-zÀ-ÿ']+")
def tok(t): return [w.lower() for w in W.findall(t)]
def frasi(t): return [f for f in re.split(r'(?<=[.!?…])\s+',t.replace('\n',' ')) if W.search(f)]
POSS=re.compile(r"\b(?:il|la|i|le|lo|gli|un|una|del|della|dei|delle|al|alla|nel|nella|sul|sulla)\s+(?:mio|mia|miei|mie|tuo|tua|tuoi|tue|suo|sua|suoi|sue|nostr[oaie]|vostr[oaie]|loro)\b|\b(?:suo|sua|suoi|sue)\b",re.I)
PRON=re.compile(r"(?:^|[.!?;:»«,]\s*)(?:io|tu|lui|lei|egli|ella|noi|voi|essi|esse|loro)\s+[a-zàèéìòù]+",re.I|re.M)
DIM=re.compile(r"\b(?:quest[oaie]|quell[oaie]|quel|quei|quegli)\b",re.I)
NONMA=re.compile(r"\bnon\b[^.!?;]{1,60}?[,:;]\s*(?:ma|è|sono)\b",re.I)
FILTRO=re.compile(r"\b(?:vedete|vedi|vide|senti|sentite|sentì|notate|noti|notò|vi accorgete|ti accorgi|si accorse|sembra|sembrava|pare|pareva)\b(?:\s+che)?",re.I)
EMO=re.compile(r"\b(?:paur[ae]|terror[ei]|rabbi[ae]|furi[ae]|gioi[ae]|tristezz[ae]|orror[ei]|disperazion[ei]|angosci[ae]|ansi[ae]|speranz[ae]|odi[oa]|vergogn[ae]|sollievo|stupore|spavent[oai])\b",re.I)
CONN=re.compile(r"(?:^|[.!?]\s+)(?:Inoltre|Tuttavia|Pertanto|Quindi|Infatti|Dunque|Eppure|Così)\b")
STOP=set("il lo la i gli le un una uno di a da in con su per tra fra e o ma che non si ci vi è sono era erano ha hanno del della dei delle al alla ai alle dal dalla nel nella nei sul sulla come più se poi già anche quando dove chi cosa qui lì".split())
def contenuto(f): return {w[:5] for w in tok(f) if w not in STOP and len(w)>3}
def sovrapp(t):
    F=frasi(t); v=[]
    for a,b in zip(F,F[1:]):
        A,B=contenuto(a),contenuto(b)
        if A|B: v.append(len(A&B)/len(A|B))
    return st.mean(v) if v else 0
def mattr(t,w=25):
    T=tok(t)
    if len(T)<=w: return len(set(T))/max(1,len(T))
    return st.mean(len(set(T[i:i+w]))/w for i in range(len(T)-w+1))
def m(t):
    T=tok(t); n=max(1,len(T)); F=frasi(t); L=[len(tok(f)) for f in F] or [0]
    return {'parole':len(T),'gulpease':mc.gulpease(t),'frasi_sd':st.pstdev(L),'frase_media':st.mean(L),
     'frasi_brevi%':sum(1 for x in L if x<=7)/len(L),'possessivi‰':1000*len(POSS.findall(t))/n,
     'pron_sogg‰':1000*len(PRON.findall(t))/n,'dimostrativi‰':1000*len(DIM.findall(t))/n,
     'non_X_ma':len(NONMA.findall(t)),'filtro‰':1000*len(FILTRO.findall(t))/n,'emozioni_nominate‰':1000*len(EMO.findall(t))/n,
     'connettivi_apertura':len(CONN.findall(t)),'sovrapp_adiacenti':sovrapp(t),'mattr25':mattr(t),
     'sensoriali‰':1000*mc.dettagli_sensoriali(t)/n,'mente‰':1000*len(mc.avverbi_mente(t))/n,'gerundi_coda':len(mc.gerundi_in_coda(t))}
if __name__=='__main__':
    rows=json.load(open(sys.argv[1]))
    keys=list(m('a b.').keys())
    print(f"{'metrica':22} vinc>perd vinc<perd pari  accordo  p(binom)")
    for k in keys:
        up=dn=eq=0
        for r in rows:
            a,b=m(r['win'])[k],m(r['lose'])[k]
            if abs(a-b)<1e-9: eq+=1
            elif a>b: up+=1
            else: dn+=1
        nn=up+dn; hi=max(up,dn)
        p=sum(math.comb(nn,i) for i in range(hi,nn+1))/2**nn*2 if nn else 1
        print(f"{k:22} {up:9} {dn:9} {eq:5}  {hi/nn if nn else 0:6.2f}  {min(1,p):.3f}")
