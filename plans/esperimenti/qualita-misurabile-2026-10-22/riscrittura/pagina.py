"""pagina.py — CONFRONTO.html dai dati di misure/INCROCIATA.json e base/BASE.json.

Una pagina sola, senza script esterni: CSS in linea, tema chiaro e scuro,
leggibile su telefono. Le differenze sono a livello di parola, contro
l'originale. Si chiama da `esegui.py pagina`.
"""
from __future__ import annotations

import difflib
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

E = html.escape
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import misura_craft as mc  # noqa: E402

#: Nei totali queste si mediano, le altre si sommano.
MEDIE = {"Gulpease", "ritmo (CV frasi)", "livelli di subordinate (max)", "profondità dell'albero (max)", "MATTR lemmi"}
#: direzione: -1 = più basso è meglio, +1 = più alto è meglio, 0 = indicatore senza verso
METRICHE = [
    ("rilievi catena V", lambda m: sum(m["cV"].values()), -1),
    ("rilievi catena N", lambda m: sum(m["cN"].values()), -1),
    ("unione V∪N", lambda m: sum(m["unione"].values()), -1),
    ("· famiglia comuni", lambda m: m["famiglie"]["comuni"], -1),
    ("· famiglia solo V", lambda m: m["famiglie"]["solo V"], -1),
    ("· famiglia solo N", lambda m: m["famiglie"]["solo N"], -1),
    ("penalità MQM", lambda m: m["mqm_penalita"], -1),
    ("dettagli sensoriali", lambda m: m["indicatori"]["sensoriali"], +1),
    ("parole", lambda m: m["indicatori"]["parole"], 0),
    ("frasi", lambda m: m["indicatori"]["frasi"], 0),
    ("Gulpease", lambda m: m["indicatori"]["gulpease"], 0),
    ("ritmo (CV frasi)", lambda m: m["indicatori"]["ritmo"], 0),
    ("avverbi -mente", lambda m: m["indicatori"]["-mente"], 0),
    ("nomi propri distinti", lambda m: m["indicatori"]["nomi distinti"], 0),
    ("livelli di subordinate (max)", lambda m: m["sintassi"]["livelli_max"], 0),
    ("profondità dell'albero (max)", lambda m: m["sintassi"]["profondita_max"], 0),
    ("MATTR lemmi", lambda m: m["sintassi"]["mattr_lemmi"], 0),
    ("P1 (indicatore in N)", lambda m: m["N_indicatori"]["P1"], 0),
]

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1b18;--muted:#6b665d;--panel:#ffffff;--line:#e3ded4;
--ins-bg:#d9f2df;--ins-fg:#14532d;--del-bg:#fbdcdc;--del-fg:#7f1d1d;--good:#15803d;--bad:#b91c1c;
--neutral:#6b7280;--accent:#8a5a14;--warn-bg:#fff4d6;--warn-fg:#6b4b00;--chip:#efeae0}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16150f;--fg:#ece8df;
--muted:#a39e92;--panel:#1f1e17;--line:#3a372d;--ins-bg:#16391f;--ins-fg:#b7f0c4;--del-bg:#43191a;
--del-fg:#f6c1c1;--good:#4ade80;--bad:#f87171;--neutral:#9ca3af;--accent:#e0b062;--warn-bg:#3a2f12;
--warn-fg:#f5d98a;--chip:#2a281f}}
:root[data-theme="dark"]{--bg:#16150f;--fg:#ece8df;--muted:#a39e92;--panel:#1f1e17;--line:#3a372d;
--ins-bg:#16391f;--ins-fg:#b7f0c4;--del-bg:#43191a;--del-fg:#f6c1c1;--good:#4ade80;--bad:#f87171;
--neutral:#9ca3af;--accent:#e0b062;--warn-bg:#3a2f12;--warn-fg:#f5d98a;--chip:#2a281f}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,"Iowan Old Style",serif}
main{max-width:1280px;margin:0 auto;padding:16px}
h1,h2,h3{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.25}
h1{font-size:1.6rem;margin:.4em 0}
h2{font-size:1.25rem;margin-top:2em;border-bottom:1px solid var(--line);padding-bottom:.3em}
h3{font-size:1.05rem;margin:0 0 .4em}
.avviso{background:var(--warn-bg);color:var(--warn-fg);border-radius:8px;padding:12px 14px;
font-family:system-ui,sans-serif;font-weight:600}
.nota{color:var(--muted);font-size:.92rem}
.tab{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.6em 0}
table{border-collapse:collapse;font:14px/1.4 system-ui,sans-serif;min-width:100%}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--chip);font-weight:600}
td.n,th.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.box{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin:18px 0}
.meta{font:13px/1.4 system-ui,sans-serif;color:var(--muted);margin-bottom:10px}
.griglia{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
@media (max-width:900px){.griglia{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.griglia{grid-template-columns:1fr}}
.ver{border:1px solid var(--line);border-radius:8px;padding:10px;background:var(--bg)}
.ver h4{margin:0 0 6px;font:600 13px/1.3 system-ui,sans-serif;color:var(--accent)}
.ver p{margin:0;font-size:15px}
.ver .eti{font:12px/1.4 system-ui,sans-serif;color:var(--muted);margin-top:8px}
ins{background:var(--ins-bg);color:var(--ins-fg);text-decoration:none;border-radius:3px}
del{background:var(--del-bg);color:var(--del-fg);border-radius:3px}
.su{color:var(--good)}.giu{color:var(--bad)}.neu{color:var(--neutral)}
.chip{display:inline-block;background:var(--chip);border-radius:999px;padding:1px 8px;margin:2px 4px 2px 0;
font:12px/1.6 system-ui,sans-serif}
details{margin:.5em 0}
summary{cursor:pointer;font:600 14px/1.5 system-ui,sans-serif}
pre{white-space:pre-wrap;word-break:break-word;font:13px/1.45 ui-monospace,Menlo,monospace;
background:var(--chip);padding:10px;border-radius:8px}
.legenda span{margin-right:12px}
.meta,.eti,td,p,code{overflow-wrap:anywhere}
"""


def parole_diff(a: str, b: str) -> str:
    """b rispetto ad a, a livello di parola: <ins> e <del>."""
    ta, tb = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if op == "equal":
            out.append(E(" ".join(ta[i1:i2])))
        if op in ("delete", "replace"):
            out.append(f"<del>{E(' '.join(ta[i1:i2]))}</del>")
        if op in ("insert", "replace"):
            out.append(f"<ins>{E(' '.join(tb[j1:j2]))}</ins>")
    return " ".join(out)


def freccia(v, o, verso) -> str:
    if v == o:
        return f"{v}"
    su = v > o
    if verso == 0:
        cls = "neu"
    else:
        cls = "su" if (su and verso > 0) or (not su and verso < 0) else "giu"
    segno = "↑" if su else "↓"
    d = abs(v - o)
    d = round(d, 3) if isinstance(d, float) else d
    return f'<span class="{cls}">{v} {segno}{d}</span>'


def tabella_catene(base: dict, inc: dict) -> str:
    t = base["tempi_s"]
    tot = Counter()
    for f in base["files"]:
        for b in f["box"]:
            tot["box"] += 1
            tot["V"] += len(b["V"])
            tot["N"] += len(b["N"])
            tot["pulitiV"] += not b["V"]
            tot["pulitiN"] += not b["N"]
        tot["scene"] += f["scene"]["scene"]
        tot["scV"] += len(f["scene"]["V"])
        tot["scN"] += len(f["scene"]["N"])
    righe_codice = {}
    for s in ("ciclo_prosa", "validate_prosa", "punteggio_mqm", "misura_craft", "voto_scrittura",
              "domande_developer", "copertura_scene", "cieco_versioni", "misura_sintassi", "coerenza_campagna"):
        righe_codice[s] = sum(1 for _ in (ROOT / "scripts" / f"{s}.py").open(encoding="utf-8"))
    v_tool = ["ciclo_prosa", "validate_prosa", "punteggio_mqm", "misura_craft", "voto_scrittura",
              "domande_developer", "copertura_scene", "cieco_versioni"]
    n_tool = v_tool + ["misura_sintassi", "coerenza_campagna"]
    rc = lambda xs: sum(righe_codice[x] for x in xs)  # noqa: E731
    righe = [
        ("Skill", "rumblingstone-narrative-style (italiano-nativo.md, read-aloud-adulti.md) · rumblingstone-module-standard",
         "le stesse, senza le norme tolte (possessivo sul corpo, «c'è o dislocazione» della §8, tetto dei nomi distinti) · "
         "più le etichette LAMP/TTCW di cieco_versioni.ETICHETTE come checklist · sviluppo-degli-incontri §18-§21"),
        ("Strumenti", "ciclo_prosa (segnala, box_impoveriti, confronta_fatti) · validate_prosa · punteggio_mqm · "
         "misura_craft --stile e --costrutto-italiano · voto_scrittura · domande_developer D1-D17",
         "quelli di V, senza --costrutto-italiano, senza la watchlist dei tic e con P1 come indicatore · "
         "più misura_sintassi (spaCy, it_core_news_md) · domande_developer D18-D21 · coerenza_campagna fatti"),
        ("Norme dei box (rilievo)", "18: 14 comuni + 4 solo V (nomi distinti, possessivo, c'è/dislocazione, P1)",
         "17: 14 comuni + 3 solo N (soggetto preverbale, aggettivo complesso, oltre due livelli)"),
        ("Domande sulle scene", "D1-D6, D6-5E, D9, D10, D15, D16 (11 regole)",
         "le stesse + D18, D19, D21 (D20 come indicatore) + coerenza dei fatti sull'arco"),
        (f"Tempo (base: {tot['box']} box, {tot['scene']} scene, 2 archi)", f"{t['V']} s",
         f"{t['N']} s, di cui coerenza {t['di cui coerenza (N)']} s, + {t['caricamento spaCy (N, una volta)']} s per caricare spaCy"),
        ("Rilievi sui 229 box (base)", f"{tot['V']} · box puliti {tot['pulitiV']}",
         f"{tot['N']} · box puliti {tot['pulitiN']}"),
        ("Rilievi sulle scene (base)", f"{tot['scV']}", f"{tot['scN']} (+{tot['scN'] - tot['scV']} da D18-D19)"),
        ("Righe di codice degli strumenti", f"{rc(v_tool):,}".replace(",", ".") + " (" + ", ".join(v_tool) + ")",
         f"{rc(n_tool):,}".replace(",", ".") + f" (+{righe_codice['misura_sintassi']} misura_sintassi, "
         f"+{righe_codice['coerenza_campagna']} coerenza_campagna; le norme tolte sono poche righe dentro file che restano)"),
    ]
    h = ['<div class="tab"><table><tr><th></th><th>Catena vecchia (V)</th><th>Catena nuova (N)</th></tr>']
    for a, b, c in righe:
        h.append(f"<tr><th>{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td></tr>")
    h.append("</table></div>")
    return "\n".join(h)


def tabella_totali(inc: dict) -> str:
    h = ['<div class="tab"><table><tr><th>misura (somma sui 16 box, o media dove è scritto)</th>'
         + "".join(f'<th class="n">{a}</th>' for a in "OVNF") + "</tr>"]
    for nome, f, verso in METRICHE:
        vals = {a: sum(f(b["versioni"][a]) for b in inc["box"]) for a in "OVNF"}
        if nome in MEDIE:
            vals = {a: v / len(inc["box"]) for a, v in vals.items()}
        vals = {a: round(v, 2) if isinstance(v, float) else v for a, v in vals.items()}
        h.append(f"<tr><td>{E(nome) + (' (media)' if nome in MEDIE else '')}</td>" + "".join(
            f'<td class="n">{vals[a] if a == "O" else freccia(vals[a], vals["O"], verso)}</td>' for a in "OVNF") + "</tr>")
    h.append("</table></div>")
    return "\n".join(h)


def tabella_norme(inc: dict) -> str:
    tot = {a: Counter() for a in "OVNF"}
    for b in inc["box"]:
        for a in "OVNF":
            tot[a].update(b["versioni"][a]["unione"])
    norme = sorted(set().union(*tot.values()), key=lambda n: -tot["O"][n])
    h = ['<div class="tab"><table><tr><th>norma (misurata con tutte e due le catene)</th>'
         + "".join(f'<th class="n">{a}</th>' for a in "OVNF") + "</tr>"]
    for n in norme:
        h.append(f"<tr><td>{E(n)}</td>" + "".join(
            f'<td class="n">{tot[a][n] if a == "O" else freccia(tot[a][n], tot["O"][n], -1)}</td>' for a in "OVNF") + "</tr>")
    h.append("</table></div>")
    return "\n".join(h)


def scheda_box(b: dict) -> str:
    o = mc.corpo_del_box(b["versioni"]["O"]["righe"])
    cols = []
    nomi = {"O": "Originale", "V": "V · catena vecchia", "N": "N · catena nuova", "F": "F · fusione"}
    for a in "OVNF":
        v = b["versioni"][a]
        testo = mc.corpo_del_box(v["righe"])
        corpo = E(o) if a == "O" else (parole_diff(o, testo) if testo != o else E(testo) + ' <span class="chip">uguale all\'originale</span>')
        eti = ""
        if a != "O":
            eti = f'<div class="eti">versione: {E(v["k"])}</div>'
            note = [re.sub(r"^<!--\s*|\s*--!?>$", "", x) for x in v.get("nota", [])]
            if note:
                eti += "".join(f'<div class="eti">{E(x)}</div>' for x in note)
        rilV = ", ".join(f"{n}×{k}" for n, k in sorted(v["cV"].items())) or "pulito"
        rilN = ", ".join(f"{n}×{k}" for n, k in sorted(v["cN"].items())) or "pulito"
        cols.append(f'<div class="ver"><h4>{nomi[a]}</h4><p>{corpo}</p>'
                    f'<div class="eti">V: {E(rilV)}<br>N: {E(rilN)}</div>{eti}</div>')
    tab = ['<div class="tab"><table><tr><th>misura</th>' + "".join(f'<th class="n">{a}</th>' for a in "OVNF") + "</tr>"]
    for nome, f, verso in METRICHE:
        vals = {a: f(b["versioni"][a]) for a in "OVNF"}
        tab.append(f"<tr><td>{E(nome)}</td>" + "".join(
            f'<td class="n">{vals[a] if a == "O" else freccia(vals[a], vals["O"], verso)}</td>' for a in "OVNF") + "</tr>")
    tab.append("</table></div>")
    its = " · ".join(f"{L}: " + (" → ".join(f"{x['k']} (V{sum(x['cV'].values())}/N{sum(x['cN'].values())})"
                                         for x in b["iterazioni"][L]) or "nessuna iterazione")
                     for L in ("V", "N"))
    fus = b["fusione"]
    fus_t = f"regola: {fus['regola']} — {fus['perche']}" + (f" · {fus['condizioni']}" if fus.get("condizioni") else "")
    return (f'<section class="box" id="{b["id"]}"><h3>{b["id"]} · {E(b["titolo"])}</h3>'
            f'<div class="meta">{E(b["file"])} r.{b["riga"]} · strato: {E(b["strato"])}<br>'
            f'iterazioni (rilievi V/N): {E(its)}<br>fusione: {E(fus_t)}</div>'
            f'<div class="griglia">{"".join(cols)}</div>'
            f'<details><summary>Misure del box</summary>{"".join(tab)}</details></section>')


def scheda_scena(s: dict) -> str:
    p = Counter(r[0] for r in s["rilievi_prima"])
    q = Counter(r[0] for r in s["rilievi_dopo"])
    rr = " · ".join(f"{k}: {freccia(q[k], p[k], -1)} (da {p[k]})" for k in sorted(set(p) | set(q)))
    diff = "\n".join(s["diff_righe"])
    return (f'<section class="box"><h3>{E(s["id"])} · {E(s["titolo"])}</h3>'
            f'<div class="meta">{E(s["file"])} · aggiunte: {E(s["aggiunte"])}</div>'
            f'<p>domande_developer, prima → dopo: {rr}</p>'
            f'<pre>{E(diff)}</pre>'
            + "".join(f'<div class="nota">dopo: {E(r[0])} {E(r[1])} — {E(r[2])}</div>' for r in s["rilievi_dopo"])
            + "</section>")


def scrivi(qui: Path) -> int:
    inc = json.loads((qui / "misure" / "INCROCIATA.json").read_text(encoding="utf-8"))
    base = json.loads((qui / "base" / "BASE.json").read_text(encoding="utf-8"))
    corpo = [
        '<!doctype html><html lang="it"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Confronto delle catene</title>", f"<style>{CSS}</style></head><body><main>",
        '<p class="avviso">Aprire solo dopo aver votato la scheda cieca (cieco/SCHEDA-CIECA.md): '
        "questa pagina dice quale versione è V, quale N e quale F.</p>",
        "<h1>Catena vecchia contro catena nuova: riscrittura di 16 box di ARC-07 e ARC-08</h1>",
        '<p class="nota">Prova del 2026-10-22. Ogni numero viene da uno strumento del repo, chiamato da '
        "<code>riscrittura/esegui.py</code>. Le misure non prevedono il voto del DM (calibrazione su 38 coppie "
        "votate: nessuna misura sotto soglia): dicono dove le versioni differiscono, non quale è migliore. "
        "Il giudice resta il cieco.</p>",
        '<p class="legenda nota"><span><ins>parola aggiunta</ins></span><span><del>parola tolta</del></span>'
        '<span class="su">↑/↓ meglio</span><span class="giu">↑/↓ peggio</span>'
        '<span class="neu">↑/↓ indicatore senza verso</span> (rispetto all\'originale)</p>',
        "<h2>Le due catene</h2>", tabella_catene(base, inc),
        "<h2>Totali sui 16 box del campione</h2>", tabella_totali(inc),
        "<h2>Norma per norma</h2>",
        '<p class="nota">Ogni versione misurata con tutte e due le catene; per ogni norma il numero più alto '
        "fra le due (unione).</p>", tabella_norme(inc),
        "<h2>I box, uno per uno</h2>",
        '<p class="nota">Le differenze sono sempre contro l\'originale. Le note sotto ogni versione sono '
        "le ragioni scritte da chi ha riscritto.</p>",
        *[scheda_box(b) for b in inc["box"]],
        "<h2>Le scene: solo ciò che D18-D21 chiede</h2>",
        '<p class="nota">Copie di lavoro in <code>riscrittura/scene/</code>: il master non è toccato. '
        "Ogni aggiunta porta <code>[INFERRED — needs DM confirmation]</code>.</p>",
        *[scheda_scena(s) for s in inc["scene"]],
        "<h2>Coerenza dei fatti sull'arco</h2>",
        '<div class="tab"><table><tr><th>arm</th><th class="n">ARC-07</th><th class="n">ARC-08</th></tr>'
        + "".join(f'<tr><td>{a}</td><td class="n">{d["ARC-07"]["contraddizioni"]}</td>'
                  f'<td class="n">{d["ARC-08"]["contraddizioni"]}</td></tr>' for a, d in inc["coerenza"].items())
        + "</table></div>",
        '<p class="nota">coerenza_campagna fatti sull\'arco intero, con i box del campione sostituiti dalla '
        "versione dell'arm: numero di contraddizioni.</p>",
        "</main></body></html>",
    ]
    (qui / "CONFRONTO.html").write_text("\n".join(corpo) + "\n", encoding="utf-8")
    print(f"scritto {qui / 'CONFRONTO.html'}")
    return 0
