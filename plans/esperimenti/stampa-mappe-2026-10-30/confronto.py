"""Confronto per ogni mappa: pergamena attuale (rendered/) contro pianta in stampa (ADR-0106).

Uso, dalla radice del repo: python3 plans/esperimenti/stampa-mappe-2026-10-30/confronto.py esito.json
"""
import re, sys, json, html
from pathlib import Path
sys.path.insert(0, "scripts")
import render_map_svg as R
ROOT = Path(".")
LW, HMAX = 496.0, 595.0

def misure(svg):
    w, h = (float(x) for x in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
    ppx = min(LW / w, HMAX / h)
    corpi = []
    # tiene conto del gruppo scale() se c'è (legenda stampa)
    for blocco, k in _gruppi(svg):
        corpi += [float(c) * k * ppx for c in re.findall(r'font-size="([\d.]+)"', blocco)]
    filtri = len(re.findall(r'filter="url\(', svg))
    return corpi, filtri

def _gruppi(svg):
    k = re.search(r'<g transform="scale\(([\d.]+)\)">', svg)
    if k:
        i = k.end(); kk = float(k.group(1))
        return [(svg[:k.start()], 1.0), (svg[i:], kk)]
    return [(svg, 1.0)]

def testi(svg, lista=False):
    """ogni <text> col suo contenuto (anche tspan), senza emoji iniziale"""
    out = []
    for t in re.findall(r'<text[^>]*>(.*?)</text>', svg, re.S):
        t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
        t = re.sub(r'^\W*\s—\s', '', t.strip())
        t = " ".join(t.split())
        if t: out.append(t)
    return out if lista else set(out)
def piatto(svg):
    return " ".join(" ".join(testi(svg, True)).split())
ETICHETTE_DI_SERVIZIO = re.compile(r'^(\d+×\d+ quadretti.*|INDICAZIONI|LEGENDA|Legenda|metri|\d.*quadrett|\d+(,\d)? m \(.*\)|[A-Z]{1,2}|\d+)$')

righe = []
for p in sorted(ROOT.glob("**/rendered/*_map[0-9][0-9]_*.svg")):
    if "build" in p.parts: continue
    md = p.parent.parent / f"{p.name.split('_map')[0]}.md"
    if not md.exists(): continue
    i = int(re.search(r"_map(\d\d)_", p.name).group(1))
    g = R.extract_maps(md.read_text(encoding="utf-8"))[i - 1]
    perg = p.read_text(encoding="utf-8")
    try:
        sm = R.render_svg(g, md.name, "pianta", "mappa", True)
        sl = R.render_svg(g, md.name, "pianta", "legenda", True)
    except Exception as e:
        righe.append(dict(mappa=str(p), errore=repr(e))); continue
    cp, fp = misure(perg)
    cm, fm = misure(sm); cl, fl = misure(sl)
    tutto = piatto(sm) + " " + piatto(sl)
    persi = sorted(t for t in testi(perg) if not ETICHETTE_DI_SERVIZIO.match(t)
                   and t not in tutto and re.sub(r'^\d+\s*', '', t) not in tutto)
    righe.append(dict(mappa=str(p.relative_to(ROOT)), celle=f"{max(len(c) for c in g['rows'].values())}x{len(g['rows'])}",
        perg_min=round(min(cp), 1), perg_sotto7=sum(c < 7 for c in cp), perg_filtri=fp,
        st_min=round(min(cm + cl), 1), st_sotto7=sum(c < 7 for c in cm + cl), st_filtri=fm + fl,
        testi_persi=persi[:12], n_persi=len(persi)))
json.dump(righe, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
for r in righe:
    if "errore" in r: print("ERR", r["mappa"], r["errore"]); continue
    print(f"{r['mappa'][-70:]:70} {r['celle']:>7} perg {r['perg_min']:>4}pt <7:{r['perg_sotto7']:>3} f:{r['perg_filtri']:>2} | stampa {r['st_min']:>4}pt <7:{r['st_sotto7']:>2} f:{r['st_filtri']} persi:{r['n_persi']}")
