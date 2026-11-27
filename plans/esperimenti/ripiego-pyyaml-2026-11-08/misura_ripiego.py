"""Misura: un ripiego senza PyYAML in compress_skills darebbe gli stessi dati?"""
import json, re, sys, time
from pathlib import Path
sys.path.insert(0, "scripts")
import yaml, compress_skills as cs

def fm_ripiego(text):
    """Parser minimo: chiave: valore su una riga, e >- / | con righe rientrate."""
    m = re.match(r'^---\s*\n(.*?\n)---\s*\n', text, re.DOTALL)
    if not m: return {}, text
    meta, key, buf, mode = {}, None, [], None
    for line in m.group(1).splitlines():
        if key and (line.startswith(" ") or not line.strip()):
            buf.append(line.strip()); continue
        if key: meta[key] = (" " if mode == ">" else "\n").join(b for b in buf if b) ; key = None
        mm = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if not mm: continue
        k, v = mm.groups()
        if v in (">", ">-", "|", "|-"): key, buf, mode = k, [], v[0]; continue
        meta[k] = v.strip().strip('"').strip("'")
    if key: meta[key] = (" " if mode == ">" else "\n").join(b for b in buf if b)
    return meta, text[m.end():]

skills = sorted(Path("skills").glob("*/SKILL.md"))
ok_fm = ok_dump = 0; diffs = []
t0 = time.perf_counter()
for p in skills:
    t = p.read_text(encoding="utf-8")
    a, _ = cs.strip_yaml_frontmatter(t); b, _ = fm_ripiego(t)
    same = {k: str(a.get(k, "")).strip() for k in ("name", "description")} == {k: str(b.get(k, "")).strip() for k in ("name", "description")}
    ok_fm += same
    if not same: diffs.append(p.parent.name)
    out = cs.compress_to_yaml(t)
    data = yaml.safe_load(out)
    ok_dump += yaml.safe_load(json.dumps(data, ensure_ascii=False)) == data
print(f"skill: {len(skills)}; frontmatter uguale (name+description): {ok_fm}/{len(skills)}; uscita JSON-come-YAML equivalente: {ok_dump}/{len(skills)}")
print("diverse:", diffs)
