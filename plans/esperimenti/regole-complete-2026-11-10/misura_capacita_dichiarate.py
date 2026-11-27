"""Capacità che genera_creatura legge davvero contro quelle che il manifest dichiara."""
import json, random, sys, subprocess
from pathlib import Path
R = Path.cwd(); sys.path.insert(0, str(R / "scripts"))
from dmcore import sistemi as S
lette = set()
orig = S.capacita
def spia(id_, nome, root=None):
    lette.add(nome); return orig(id_, nome, root)
S.capacita = spia
import genera_creatura as G
from dmcore import creature_pf1e as CP
tipi = ["humanoid", "undead", "construct", "ooze", "dragon", "outsider", "giant", "aberration"]
ruoli = None
n = 0
for gs in (1, 3, 7, 12, 17, 20):
    for t in tipi:
        for r in (ruoli or list(G.RUOLI)):
            try:
                G.genera(gs, tipo=t, taglia="medium", ruolo=r, rng=random.Random(gs)); n += 1
            except Exception as e:
                print("ERR", gs, t, r, e); break
def dichiarate(ref):
    m = json.loads(subprocess.check_output(["git", "show", f"{ref}:scripts/tools.manifest.json"]))
    return set(next(t for t in m["tools"] if t["id"] == "genera_creatura")["sistema"]["capacita"])
print("mostri generati:", n)
print("lette:", sorted(lette))
for ref in sys.argv[1:]:
    d = dichiarate(ref)
    print(ref, "dichiarate:", len(d), "lette ma non dichiarate:", sorted(lette - d), "coperte:", f"{len(lette & d)}/{len(lette)}")
