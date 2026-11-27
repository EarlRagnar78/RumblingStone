import json,subprocess,sys
from pathlib import Path
VP='/tmp/claude-0/vp'
def vp(pdf,fl):
    r=subprocess.run(['java','-Xmx1g','-cp',f'{VP}/greenfield-apps-1.28.2.jar:{VP}','Avvio','--flavour',fl,'--format','json',str(pdf)],capture_output=True,text=True)
    e=json.loads(r.stdout)['report']['jobs'][0]['validationResult'][0]
    return {'conforme':e['compliant'],'falliti':e['details']['failedChecks'],'regole':{f"{x['clause']}-{x['testNumber']}":x['failedChecks'] for x in e['details']['ruleSummaries']}}
out={}
for d in sys.argv[1:]:
    res={}
    for p in sorted(Path(d).glob('*.pdf')):
        res[p.name]={fl:vp(p,fl) for fl in ('ua1','2a','2b')}
        res[p.name]['byte']=p.stat().st_size
        print(d,p.name,{fl:(res[p.name][fl]['conforme'],res[p.name][fl]['falliti']) for fl in ('ua1','2a','2b')},flush=True)
    out[d]=res
json.dump(out,open('/tmp/claude-0/pdfa/misure.json','w'),indent=1,ensure_ascii=False)
