#!/usr/bin/env python3
"""grafo.py — punti chiave, grafo degli eventi e regole temporali e ricorsive di «chi sa cosa».

Misura del 2026-11-12, chiesta dal DM: con un giorno su ogni fatto e un grafo di
chi informa chi, Prolog o clingo migliorano la verifica della storia? E un
estrattore con recupero (RAG) supera il collo di bottiglia misurato da ADR-0125
(leggere il fatto nella prosa)?

Il grafo è in `eventi.yaml` (non è canone). Le regole sono le stesse in tre
motori, sugli stessi fatti:

  conosce(P, F, G)   P sa F dal giorno G: direttamente (`sa` con giorno) oppure
                     perché lo sa un informatore Y dal giorno G' e G = G' + ritardo
                     (RICORSIVA: la catena può essere lunga quanto si vuole)
  T0 origine         una scena del giorno ≤ D afferma F, ma F nasce dopo D
  T1 temporale       P mostra di sapere F in una scena che finisce prima di G
  T2 catena rotta    P sa F «da Y», ma nel grafo Y non sa F (difetto del grafo stesso)
  T3 negazione       P mostra di sapere F, e state.yaml dice che non lo sa

Ogni violazione esce con regola, atteso, ha, file, riga (pattern di ADR-0124).

Uso
  python3 grafo.py chiusura                      # chi sa cosa da quando, e T2
  python3 grafo.py regex [--radice DIR] [--json] # estrattore deterministico + regole (Python)
  python3 grafo.py motori CITAZIONI.json         # le stesse regole in Python, SWI-Prolog, clingo
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

QUI = Path(__file__).resolve().parent
REPO = QUI.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import coerenza_campagna as cc  # noqa: E402  (stesse esclusioni di file e righe di storico)

INF = 999
ARCHI = ["07_il Portale Della Forgia Eterna", "08_La Battaglia Di Hammerfist",
         "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"]
# Il PNG «mostra di sapere»: verbi di conoscenza, non una semplice menzione
CUE = re.compile(
    r"\b(sa|sapeva|sanno|saprà|sapere|conosce|conosceva|scopr\w*|ha saputo|è al corrente|"
    r"informat\w*|riferit\w*|rivel\w*|racconta\w*|sospett\w*|sussurr\w*|annunci\w*|"
    r"dice|disse|dichiar\w*|chiama|cita|nomina|knows?|knew|aware|learns?|reveals?|tells?)\b", re.I)
FUTURO = re.compile(r"\bse\b|\bquando\b|\bdopo\b|\bpoi\b|diventer|sarann|saprà|scoprirà|"
                    r"\bwill\b|\bafter\b|\bif\b|\bfinché\b|\bnon sa\b|\bnon conosce\b|\bignora\b|"
                    r"does not know|doesn't know|\bnon\b[^.]{0,20}\bsa\b", re.I)


def carica(p: Path = QUI / "eventi.yaml") -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Chiusura (Python): punto fisso della regola ricorsiva
# --------------------------------------------------------------------------- #
def chiusura(g: dict) -> tuple[dict, list[dict]]:
    """{(png, fatto): giorno} e le catene rotte (T2)."""
    orig = {f: v["origine"] for f, v in g["fatti"].items()}
    da: dict[tuple[str, str], int] = {}
    for s in g["sa"]:
        if "giorno" in s:
            k = (s["png"], s["fatto"])
            da[k] = min(da.get(k, INF), max(s["giorno"], orig[s["fatto"]]))
    cambiato = True
    while cambiato:
        cambiato = False
        for s in g["sa"]:
            y = s.get("informato_da")
            if not y or (y, s["fatto"]) not in da:
                continue
            k = (s["png"], s["fatto"])
            gg = da[(y, s["fatto"])] + s.get("ritardo", 0)
            if gg < da.get(k, INF):
                da[k] = gg
                cambiato = True
    rotte = [{"regola": "T2 catena rotta", "atteso": f"{s['informato_da']} sa {s['fatto']}",
              "ha": f"{s['informato_da']} non lo sa nel grafo", "file": "eventi.yaml",
              "riga": 0, "png": s["png"], "fatto": s["fatto"]}
             for s in g["sa"] if s.get("informato_da") and (s["png"], s["fatto"]) not in da]
    return da, rotte


def regole_python(g: dict, cit: list[dict]) -> list[dict]:
    da, rotte = chiusura(g)
    orig = {f: v["origine"] for f, v in g["fatti"].items()}
    neg = {(n["png"], n["fatto"]): n.get("fino_a", INF) for n in g["non_sa"]}
    out = list(rotte)
    for c in cit:
        lo, hi, f, p = c["giorno_da"], c["giorno_a"], c["fatto"], c.get("png")
        base = {"file": c["file"], "riga": c["riga"], "png": p, "fatto": f}
        if hi < orig[f]:
            out.append({"regola": "T0 origine", "atteso": f"{f} dal Day {orig[f]}",
                        "ha": f"scena Day {lo}-{hi}", **base})
        if not p:
            continue
        if (p, f) in neg and lo < neg[(p, f)]:
            out.append({"regola": "T3 negazione", "atteso": f"{p} non sa {f}",
                        "ha": "lo mostra di sapere", **base})
        elif (p, f) in da and hi < da[(p, f)]:
            out.append({"regola": "T1 temporale", "atteso": f"{p} sa {f} dal Day {da[(p, f)]}",
                        "ha": f"scena Day {lo}-{hi}", **base})
    return out


# --------------------------------------------------------------------------- #
# Gli stessi fatti e le stesse regole in Prolog e in clingo
# --------------------------------------------------------------------------- #
def _q(x) -> str:
    return str(x) if isinstance(x, int) else "'" + str(x).replace("\\", "\\\\").replace("'", "\\'") + "'"


def fatti_logici(g: dict, cit: list[dict]) -> list[str]:
    out = []
    for f, v in g["fatti"].items():
        out.append(f"origine({_q(f)},{v['origine']}).")
    for s in g["sa"]:
        if "giorno" in s:
            out.append(f"sa_diretto({_q(s['png'])},{_q(s['fatto'])},{s['giorno']}).")
        else:
            out.append(f"informa({_q(s['informato_da'])},{_q(s['png'])},{_q(s['fatto'])},{s.get('ritardo', 0)}).")
    for n in g["non_sa"]:
        out.append(f"non_sa({_q(n['png'])},{_q(n['fatto'])},{n.get('fino_a', INF)}).")
    for i, c in enumerate(cit):
        out.append(f"cita({i},{_q(c.get('png') or 'nessuno')},{_q(c['fatto'])},{c['giorno_da']},{c['giorno_a']}).")
    return out


PROLOG = r"""
:- discontiguous sa_diretto/3, informa/4, non_sa/3, cita/5, origine/2.
:- table conosce(_,_,min).
conosce(P,F,G) :- sa_diretto(P,F,G0), origine(F,O), G is max(G0,O).
conosce(P,F,G) :- informa(Y,P,F,R), conosce(Y,F,G1), G is G1+R.
viol(t0,I,P,F,O)  :- cita(I,P,F,_,Hi), origine(F,O), Hi < O.
viol(t3,I,P,F,0)  :- cita(I,P,F,Lo,_), non_sa(P,F,Fino), Lo < Fino.
viol(t1,I,P,F,G)  :- cita(I,P,F,Lo,Hi), \+ (non_sa(P,F,Fino), Lo < Fino), conosce(P,F,G), Hi < G.
viol(t2,-1,P,F,0) :- informa(Y,P,F,_), \+ conosce(Y,F,_).
main :- forall(viol(R,I,P,F,X), format("~w\t~w\t~w\t~w\t~w~n",[R,I,P,F,X])).
"""

CLINGO = r"""
#const inf=999.
conosce(P,F,G0) :- sa_diretto(P,F,G0), origine(F,O), G0 >= O.
conosce(P,F,O) :- sa_diretto(P,F,G0), origine(F,O), G0 < O.
conosce(P,F,G) :- informa(Y,P,F,R), conosce(Y,F,G1), G = G1+R, G <= inf.
primo(P,F,G) :- conosce(P,F,_), G = #min{ H : conosce(P,F,H) }.
negato(I) :- cita(I,P,F,Lo,_), non_sa(P,F,Fino), Lo < Fino.
viol(t0,I,P,F,O) :- cita(I,P,F,_,Hi), origine(F,O), Hi < O.
viol(t3,I,P,F,0) :- cita(I,P,F,Lo,_), non_sa(P,F,Fino), Lo < Fino.
viol(t1,I,P,F,G) :- cita(I,P,F,Lo,Hi), not negato(I), primo(P,F,G), Hi < G.
sa_qualcosa(Y,F) :- conosce(Y,F,_).
viol(t2,-1,P,F,0) :- informa(Y,P,F,_), not sa_qualcosa(Y,F).
#show viol/5.
"""


def _norm_viol(regola, i, p, f, cit):
    if i < 0:
        return ("T2", "eventi.yaml", 0, p, f)
    c = cit[i]
    return (regola.upper(), c["file"], c["riga"], None if p == "nessuno" else p, f)


def regole_prolog(g: dict, cit: list[dict]) -> list[tuple]:
    with tempfile.NamedTemporaryFile("w", suffix=".pl", delete=False, encoding="utf-8") as t:
        t.write("\n".join(fatti_logici(g, cit)) + "\n" + PROLOG)
        nome = t.name
    r = subprocess.run([shutil.which("swipl"), "-q", "-g", "main", "-t", "halt", nome],
                       capture_output=True, text=True, timeout=300)
    Path(nome).unlink()
    if r.returncode:
        raise RuntimeError(r.stderr)
    out = set()
    for riga in r.stdout.splitlines():
        reg, i, p, f, _x = riga.split("\t")
        out.add(_norm_viol(reg, int(i), p, f, cit))
    return sorted(out, key=str)


def regole_clingo(g: dict, cit: list[dict]) -> list[tuple]:
    import clingo
    ctl = clingo.Control(["0"])
    prog = "\n".join(fatti_logici(g, cit)).replace("'", '"') + "\n" + CLINGO
    ctl.add("base", [], prog)
    ctl.ground([("base", [])])
    out = set()
    with ctl.solve(yield_=True) as h:
        for m in h:
            for s in m.symbols(shown=True):
                a = s.arguments
                out.add(_norm_viol(a[0].name, a[1].number, a[2].string, a[3].string, cit))
    return sorted(out, key=str)


def chiavi_viol(v: list[dict]) -> list[tuple]:
    return sorted({(x["regola"][:2], x["file"], x["riga"], x.get("png"), x["fatto"]) for x in v}, key=str)


# --------------------------------------------------------------------------- #
# L'estrattore deterministico (il «collo di bottiglia» di ADR-0125)
# --------------------------------------------------------------------------- #
def finestra(rel: str, g: dict) -> tuple[int, int] | None:
    nome = Path(rel).name
    for w in g["finestre_file"]:
        if re.search(w["rx"], nome if not w["rx"].startswith("^") else rel):
            return tuple(w["giorni"])
    return None


def file_corpus(radice: Path) -> list[Path]:
    out = []
    for a in ARCHI:
        for p in sorted((radice / a).glob("*.md")):
            if not cc.ESCLUDI_FILE.search(str(p.relative_to(radice))):
                out.append(p)
    return out


def _rx_alias(a: str) -> re.Pattern:
    return re.compile(r"(?<![\w'’])" + re.escape(a) + r"(?![\w'’])", re.I)


def estrai_regex(radice: Path, g: dict) -> list[dict]:
    alias = {p: [_rx_alias(a) for a in v] for p, v in g["alias"].items()}
    chiavi = {f: [re.compile(re.escape(k), re.I) for k in v["chiavi"]] for f, v in g["fatti"].items()}
    cit = []
    for p in file_corpus(radice):
        rel = str(p.relative_to(radice))
        w = finestra(rel, g)
        if not w:
            continue
        fence = False
        for n, riga in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if riga.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence or cc.STORICO_RIGA.search(riga) or cc.HEADING.match(riga):
                continue
            for fr in re.split(r"(?<=[.;!?])\s+", riga):
                if FUTURO.search(fr):
                    continue
                fatti = [f for f, rx in chiavi.items() if any(r.search(fr) for r in rx)]
                if not fatti:
                    continue
                pngs = [q for q, rx in alias.items() if any(r.search(fr) for r in rx)]
                sapere = bool(CUE.search(fr))
                for f in fatti:
                    # T0 vale anche senza PNG: la scena afferma il fatto
                    cit.append({"png": None, "fatto": f, "giorno_da": w[0], "giorno_a": w[1],
                                "file": rel, "riga": n, "testo": fr.strip()[:240], "estrattore": "regex"})
                    if sapere and len(pngs) == 1:
                        cit.append({"png": pngs[0], "fatto": f, "giorno_da": w[0], "giorno_a": w[1],
                                    "file": rel, "riga": n, "testo": fr.strip()[:240], "estrattore": "regex"})
    return cit


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("chiusura")
    r = sub.add_parser("regex")
    r.add_argument("--radice", type=Path, default=REPO)
    r.add_argument("--json", action="store_true")
    m = sub.add_parser("motori")
    m.add_argument("citazioni", type=Path)
    a = ap.parse_args(argv)
    g = carica()
    if a.cmd == "chiusura":
        da, rotte = chiusura(g)
        for (p, f), d in sorted(da.items()):
            print(f"  {p:<18} {f:<20} dal Day {d}")
        for x in rotte:
            print(f"✗ {x['regola']} · {x['png']} · {x['fatto']} · atteso {x['atteso']} · ha {x['ha']}")
        return 0
    if a.cmd == "regex":
        cit = estrai_regex(a.radice, g)
        v = regole_python(g, cit)
        if a.json:
            print(json.dumps({"citazioni": cit, "violazioni": v}, ensure_ascii=False, indent=1))
        else:
            for x in v:
                print(f"✗ {x['regola']} · atteso {x['atteso']} · ha {x['ha']} · {x['file']}:{x['riga']}")
            print(f"== {len(cit)} citazioni, {len(v)} violazioni")
        return 0
    cit = json.loads(a.citazioni.read_text(encoding="utf-8"))["citazioni"]
    tempi = {}
    t = time.perf_counter(); py = chiavi_viol(regole_python(g, cit)); tempi["python"] = time.perf_counter() - t
    t = time.perf_counter(); pl = regole_prolog(g, cit); tempi["prolog"] = time.perf_counter() - t
    t = time.perf_counter(); cl = regole_clingo(g, cit); tempi["clingo"] = time.perf_counter() - t
    print(json.dumps({"citazioni": len(cit), "python": len(py), "prolog": len(pl), "clingo": len(cl),
                      "uguali": py == pl == cl, "solo_python": [x for x in py if x not in pl],
                      "solo_prolog": [x for x in pl if x not in py],
                      "solo_clingo": [x for x in cl if x not in py],
                      "secondi": {k: round(v, 3) for k, v in tempi.items()}}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
