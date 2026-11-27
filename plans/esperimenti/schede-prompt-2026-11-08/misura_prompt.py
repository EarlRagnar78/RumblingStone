#!/usr/bin/env python3
"""misura_prompt.py — fotografia dei prompt del repo contro la checklist di
Anthropic per le skill (best-practices, 2026) e ADR-0109.
Uso: python3 misura_prompt.py <radice-repo>   (solo lettura)"""
import glob, json, os, re, sys
import yaml
root = sys.argv[1] if len(sys.argv) > 1 else "."
cons = json.load(open(f"{root}/plans/esperimenti/marcature-2026-11-07/consegne.json"))["consegne"]
prove = {}
for c in cons:
    prove[c["skill"]] = prove.get(c["skill"], 0) + 1
print("skill|righe|parole|lingua desc|«quando» in desc|date nel corpo|Vincoli|Formato d'uscita|Prima di consegnare|Cancelli|prove")
for f in sorted(glob.glob(f"{root}/skills/*/SKILL.md")):
    t = open(f, encoding="utf-8").read()
    fm, body = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S).groups()
    d = yaml.safe_load(fm).get("description", "")
    name = os.path.basename(os.path.dirname(f))
    heads = " ".join(re.findall(r"^## (.*)$", body, re.M)).lower()
    print("|".join(map(str, [
        name, body.count("\n"), len(body.split()),
        "it" if re.search(r"\b(della|delle|quando|non|per)\b", d) else "en",
        bool(re.search(r"(?i)\b(use when|when|quando|usala|trigger)", d)),
        len(re.findall(r"20\d\d-\d\d-\d\d", body)),
        "vincoli sui fatti" in heads,
        bool(re.search(r"output|formato|uscita", heads)),
        bool(re.search(r"self-check|prima di consegnare|autocontrollo", heads)),
        "cancelli deterministici" in heads,
        prove.get(name, 0)])))
a = open(f"{root}/AGENTS.md", encoding="utf-8").read()
print(f"\nAGENTS.md: {a.count(chr(10))} righe, {len(a.split())} parole, {len(a.encode())} byte, "
      f"{len(re.findall(r'20[0-9]{2}-[0-9]{2}-[0-9]{2}', a))} date")
briefs = [p for p in glob.glob(f"{root}/plans/esperimenti/**/*", recursive=True)
          if re.search(r"(?i)brief|consegne|prompt", os.path.basename(p))]
print("brief/consegne a mano in plans/esperimenti:", len(briefs))
