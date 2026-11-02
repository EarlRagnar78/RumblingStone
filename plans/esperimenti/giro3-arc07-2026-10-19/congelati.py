"""I 16 box votati dal DM nel cieco del 2026-10-18: il testo di oggi (main) di ciascuno.
Scrive congelati.json: [{file, titolo, testo}]."""
import sys, json, re, difflib
sys.path.insert(0, "scripts")
import cieco_versioni as cv
M = "plans/esperimenti/giro2-arc07-2026-10-18/misure"
chiave = json.load(open(f"{M}/CIECO-CHIAVE.json"))
voti = dict(l.split() for l in open(f"{M}/CIECO-VOTI.txt") if l.strip())
scheda = open(f"{M}/CIECO-SCHEDA.md", encoding="utf-8").read()
blocchi = re.split(r"^## Coppia (\d+)\s*$", scheda, flags=re.M)
testi = {}
for i in range(1, len(blocchi), 2):
    n, corpo = blocchi[i], blocchi[i + 1]
    a = re.search(r"\*\*A\*\*\n\n(.*?)\n\n\*\*B\*\*", corpo, re.S).group(1)
    b = re.search(r"\*\*B\*\*\n\n(.*?)\s*$", corpo, re.S).group(1)
    pulisci = lambda t: "\n".join(l[2:] if l.startswith("> ") else l.lstrip(">") for l in t.splitlines())
    testi[n] = {"A": pulisci(a), "B": pulisci(b)}
out = []
for c in chiave["coppie"]:
    n = str(c["n"])
    if n not in voti: continue
    vincitore = testi[n][voti[n]]
    oggi = cv.box_con_titolo(cv.testo_a("e0ce0e6", c["file"]))
    best = max(oggi, key=lambda b: difflib.SequenceMatcher(None, vincitore, b["testo"], autojunk=False).ratio())
    r = difflib.SequenceMatcher(None, vincitore, best["testo"], autojunk=False).ratio()
    out.append({"n": int(n), "file": c["file"], "titolo": best["titolo"], "testo": best["testo"], "somiglianza": round(r, 3)})
    print(n, voti[n], round(r, 3), best["titolo"][:60], "|", best["testo"][:60].replace("\n", " "))
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
