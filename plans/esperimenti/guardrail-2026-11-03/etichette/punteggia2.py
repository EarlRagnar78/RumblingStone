import json, sys, time, random, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
M="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
torch.set_num_threads(4)
tok=AutoTokenizer.from_pretrained(M); m=AutoModelForSequenceClassification.from_pretrained(M).eval()
ic={v.lower():k for k,v in m.config.id2label.items()}["contradiction"]
d=json.load(open(sys.argv[1])); random.seed(7); d=random.sample(d,int(sys.argv[3]))
d.sort(key=lambda x:len(x["prima"])+len(x["dopo"]))
t0=time.time(); out=[]
with torch.no_grad():
    for i in range(0,len(d),16):
        b=d[i:i+16]
        for dirz in (0,1):
            p=[x["prima"] if dirz==0 else x["dopo"] for x in b]; h=[x["dopo"] if dirz==0 else x["prima"] for x in b]
            z=m(**tok(p,h,return_tensors="pt",truncation=True,max_length=128,padding=True)).logits.softmax(-1)[:,ic].tolist()
            for x,v in zip(b,z): x["nli"]=max(x.get("nli",0),round(v,3))
        if i%320==0: print(i,round(time.time()-t0),flush=True)
print("secondi",round(time.time()-t0),"coppie",len(d),flush=True)
json.dump(d,open(sys.argv[2],"w"),ensure_ascii=False,indent=0)
print("sopra 0.5",sum(x["nli"]>0.5 for x in d))
