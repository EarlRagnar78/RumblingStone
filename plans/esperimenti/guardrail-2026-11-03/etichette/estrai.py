"""Coppie (riga tolta, riga messa) dai commit di correzione e di prosa."""
import difflib, json, random, re, subprocess, sys
REPO = str(__import__("pathlib").Path(__file__).resolve().parents[4])
GRUPPI = {
  "correzione": r"contraddi|non torna|non tornava|riallinea|corrett|sbagliat|errat|discrepanz|incoerenz",
  "prosa": r"prosa|riscrittura|riscritt|giro|box",
}
def git(*a): return subprocess.run(["git","-C",REPO,*a],capture_output=True,text=True,errors="replace").stdout
def pulisci(s): return re.sub(r"\s+"," ",s).strip()
out=[]
random.seed(20261103)
for g,pat in GRUPPI.items():
    shas=git("log","--no-merges","-i","-E",f"--grep={pat}","--format=%H").split()
    for sha in shas:
        msg=git("log","-1","--format=%s",sha).strip()
        diff=git("show","--format=","-U0","--no-color",sha,"--","*.md",":(exclude)plans/**",":(exclude)docs/**",":(exclude)skills/**",":(exclude)*.hb.md",":(exclude)**/README.md",":(exclude)CHANGELOG.md",":(exclude)MEMORIA.md",":(exclude)campaign/**")
        coppie=[]
        for hunk in re.split(r"^@@.*@@.*$",diff,flags=re.M):
            meno=[pulisci(l[1:]) for l in hunk.split("\n") if l.startswith("-") and not l.startswith("---")]
            piu=[pulisci(l[1:]) for l in hunk.split("\n") if l.startswith("+") and not l.startswith("+++")]
            for a in meno:
                if not 40<=len(a)<=400 or re.search(r"[🟩🟫🧱🏰⬛⬜✅═│]|^\|.*\|$|^#|^!\[|`",a): continue
                best=max(piu,key=lambda b:difflib.SequenceMatcher(None,a,b).ratio(),default=None)
                if not best: continue
                r=difflib.SequenceMatcher(None,a,best).ratio()
                if 0.6<=r<0.98 and 40<=len(best)<=400:
                    coppie.append((a,best,round(r,2)))
        random.shuffle(coppie)
        for a,b,r in coppie[:2]:
            out.append({"gruppo":g,"sha":sha[:8],"msg":msg,"prima":a,"dopo":b,"sim":r})
random.shuffle(out)
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False,indent=0)
print(len(out), sum(o["gruppo"]=="correzione" for o in out))
