import pymupdf,sys,json
from pathlib import Path
out={}
for d in sys.argv[1:]:
    r={}
    for p in sorted(Path(d).glob('*.pdf')):
        doc=pymupdf.open(p); tot=n=0
        for x in range(1,doc.xref_length()):
            if doc.xref_get_key(x,'Subtype')[1]=='/Image' and doc.xref_get_key(x,'Filter')[1]=='/DCTDecode':
                tot+=1; n+= b'digitalsourcetype/' in doc.xref_stream_raw(x)
        r[p.name]={'jpeg':tot,'etichettate':n,'pagine':len(doc)}
    out[d]=r; print(d,'jpeg',sum(v['jpeg'] for v in r.values()),'etichettate',sum(v['etichettate'] for v in r.values()),'booklet con etichette',sum(1 for v in r.values() if v['etichettate']),'pagine',sum(v['pagine'] for v in r.values()))
json.dump(out,open('/tmp/claude-0/pdfa/img.json','w'),indent=1)
