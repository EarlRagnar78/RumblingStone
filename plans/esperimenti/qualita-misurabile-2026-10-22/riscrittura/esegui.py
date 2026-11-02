#!/usr/bin/env python3
"""esegui.py — catena vecchia (V) contro catena nuova (N) su ARC-07 e ARC-08.

Prova del 2026-10-22 (thread q4s7mw, PR #264). Usa gli script di `scripts/` così
come sono in questo albero e **non li modifica**: la catena N è simulata qui,
filtrando i rilievi e, per la watchlist dei tic minori, togliendo per la durata
della chiamata la voce dal dizionario `ciclo_prosa.DEBOLI` (poi la rimette).

Le due catene
-------------
V (vecchia)  ciclo_prosa segnala · box_impoveriti · confronta_fatti ·
             validate_prosa (regole proprie: maiuscole, antitesi, trattino,
             terminologia; i calchi sono gli stessi di segnala) · punteggio_mqm
             (penalità) · misura_craft --stile (gerundio in coda) ·
             misura_craft --costrutto-italiano · voto_scrittura (controlli dei box)
             · domande_developer D1-D17 sulle scene
N (nuova)    V senza: nomi propri distinti >1, possessivo sulle parti del corpo,
             watchlist dei tic minori, --costrutto-italiano; P1 declassato a
             indicatore (INVENTARIO §3 e §5); PIÙ misura_sintassi (soggetto
             preverbale, aggettivo complesso, stare+gerundio, oltre due livelli di
             subordinate), domande_developer D18-D21 (D20 come indicatore,
             INVENTARIO §8), coerenza_campagna fatti sull'arco.

Comandi
-------
    python3 esegui.py base          # tutti i box e le scene, con le due catene, e i tempi
    python3 esegui.py campione      # il campione stratificato (seme dichiarato)
    python3 esegui.py misura [ID…]  # rilievi V e N di ogni iterazione scritta in versioni/BOX.md
    python3 esegui.py incrociata    # O, V, N, F con tutte le misure; scene; coerenza
    python3 esegui.py cieco         # scheda cieca e chiavi, con cieco_versioni
    python3 esegui.py pagina        # CONFRONTO.html

spaCy e `it_core_news_md` servono a N (misura_sintassi); senza, N non si misura.

Nota del lotto 7e (2026-10-22). Questo script misura la catena com'era al
commit 66c50e14. Il lotto 7e ha tolto `voto_scrittura.py` (il suo «sembra» è
ora `validate_prosa.sembra_esitanti`) e la watchlist di `ciclo_prosa.DEBOLI`:
da quel commit in poi `import voto_scrittura` fallisce. Per rifare la prova si
torna a 66c50e14 (`git switch --detach 66c50e14`); i risultati scritti qui
accanto non cambiano.
"""
from __future__ import annotations

import contextlib
import difflib
import html
import io
import json
import random
import re
import statistics
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

QUI = Path(__file__).resolve().parent
ROOT = QUI.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402
import validate_prosa as vp  # noqa: E402
import ciclo_prosa as cp  # noqa: E402
import voto_scrittura as vs  # noqa: E402
import punteggio_mqm as pm  # noqa: E402
import copertura_scene as cs  # noqa: E402
import domande_developer as dd  # noqa: E402
import cieco_versioni as cv  # noqa: E402
import misura_sintassi as ms  # noqa: E402
import coerenza_campagna as cc  # noqa: E402

ARC07 = [f"07_il Portale Della Forgia Eterna/ARC07-DEF-{i}-{n}.md" for i, n in (
    (1, "PIANO-TERRA-TERROS"), (2, "RITORNO-E-AFFRESCHI"), (3, "RESURREZIONE-HELLA"),
    (4, "VIAGGIO-MILLE-ANNI"), (5, "RITORNO-HAMMERFIST"))]
ARC08 = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "08_La Battaglia Di Hammerfist").glob("*.md")
               if not p.name.startswith("ERRATA-"))
FILES = ARC07 + ARC08

#: Le scene di ARC-08 non hanno «### SCENA»: sono «Incontro».
PROFILI_ARC08 = {
    "08_La Battaglia Di Hammerfist/ARC08-01-GUIDA-DM.md":
        {"scena": r"^#{3,4}\s+(?:\S+\s+)?\*\*(?:INCONTRO|Incontro)\b"},
    "08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md":
        {"scena": r"^##\s+\*\*INCONTRO\b"},
}

CONGELATI = ROOT / "plans/esperimenti/giro3-arc07-2026-10-19/misure/CONGELATI.json"
SPEC = pm.carica_specifiche()
_TMP = Path(tempfile.mkdtemp(prefix="riscrittura-"))
SEME = 20261022

# ── le famiglie (CRITERIO-FUSIONE.txt) ──────────────────────────────────────
COMUNI = ("calco", "stare+gerundio", "box con parentesi", "metratura", "sembra/pare",
          "box oltre 12 righe", "tic minori in gruppo", "gerundio in coda", "maiuscole_di_enfasi",
          "trattino_come_respiro", "antitesi_ripetuta", "terminologia_non_canonica",
          "box impoverito", "fatto cambiato")
SOLO_V = ("box con più nomi propri", "possessivo sul corpo", "senza c'è né dislocazione", "P1")
SOLO_N = ("sogg_preverbale", "agg_complesso", "oltre due livelli")
FAMIGLIA = {**{n: "comuni" for n in COMUNI}, **{n: "solo V" for n in SOLO_V},
            **{n: "solo N" for n in SOLO_N}}
#: Da quale strumento viene ogni norma (per la sintesi granulare).
STRUMENTO = {
    "calco": "validate_prosa CALCHI_SEMPRE (via ciclo_prosa segnala)",
    "stare+gerundio": "validate_prosa CALCHI_READ_ALOUD (V) · + misura_sintassi (N)",
    "possessivo sul corpo": "validate_prosa CALCHI_READ_ALOUD",
    "box con parentesi": "misura_craft difetti_dei_box", "box oltre 12 righe": "misura_craft difetti_dei_box",
    "box con più nomi propri": "misura_craft nomi_propri (MQM box_piu_di_un_nome_proprio)",
    "metratura": "misura_craft METRATURA", "P1": "misura_craft P1",
    "sembra/pare": "voto_scrittura sembra_esitanti", "tic minori in gruppo": "ciclo_prosa DEBOLI",
    "gerundio in coda": "misura_craft --stile", "senza c'è né dislocazione": "misura_craft --costrutto-italiano",
    "maiuscole_di_enfasi": "validate_prosa", "trattino_come_respiro": "validate_prosa",
    "antitesi_ripetuta": "validate_prosa", "terminologia_non_canonica": "validate_prosa",
    "box impoverito": "ciclo_prosa box_impoveriti (cieco_versioni.verdetto_misurato)",
    "fatto cambiato": "ciclo_prosa confronta_fatti",
    "sogg_preverbale": "misura_sintassi", "agg_complesso": "misura_sintassi",
    "oltre due livelli": "misura_sintassi",
}

_NLP = None


def nlp():
    global _NLP
    if _NLP is None:
        _NLP = ms.carica_nlp()
        if _NLP is None:
            sys.exit("serve spaCy con it_core_news_md per la catena N")
    return _NLP


# ── i box ───────────────────────────────────────────────────────────────────
def box_del_file(rel: str) -> "list[dict]":
    testo = (ROOT / rel).read_text(encoding="utf-8")
    righe = testo.splitlines()
    titoli, corr = {}, ""
    for i, r in enumerate(righe):
        m = cv._TITOLO.match(r)
        if m:
            corr = m.group(1)
        titoli[i] = corr
    out = []
    for k, (i0, i1, b) in enumerate(cp._box_con_righe(testo)):
        corpo = mc.corpo_del_box(b)
        out.append({"id": f"{Path(rel).stem[:22]}#{k:02d}", "file": rel, "indice": k, "riga": i0 + 1,
                    "titolo": re.sub(r"[*_]", "", titoli.get(i0, "")).strip(), "righe": b,
                    "corpo": corpo, "parole": len(corpo.split())})
    return out


def _classifica(s: "cp.Segnalazione") -> str:
    if s.norma == "calco":
        if "possessivo" in s.dettaglio:
            return "possessivo sul corpo"
        if "progressivo" in s.dettaglio:
            return "stare+gerundio"
    return s.norma


def _tmp(testo: str, rel: str) -> Path:
    p = _TMP / Path(rel).name
    p.write_text(testo + "\n", encoding="utf-8")
    return p


@contextlib.contextmanager
def senza_watchlist():
    """N: la watchlist dei tic minori non c'è (INVENTARIO §6). Si toglie per la
    durata della chiamata, e si rimette."""
    tolta = cp.DEBOLI.pop("watchlist")
    try:
        yield
    finally:
        cp.DEBOLI["watchlist"] = tolta


def _comuni(testo: str, corpo: str, rel: str, orig: "str | None") -> "tuple[list, list]":
    """I rilievi che le due catene condividono, e i doppioni di validate_prosa."""
    R, doppioni = [], []
    p = _tmp(testo, rel)
    for k, m in vp.rilievi(p):
        if k in ("maiuscole_di_enfasi", "antitesi_ripetuta", "trattino_come_respiro",
                 "terminologia_non_canonica"):
            R.append(("validate_prosa", k, m.split(": ", 1)[-1][:120]))
        else:
            doppioni.append(("validate_prosa", k))
    for g in mc.gerundi_in_coda(corpo):
        R.append(("misura_craft --stile", "gerundio in coda", g))
    if orig is not None:
        for x in cp.box_impoveriti(orig, testo):
            R.append(("ciclo_prosa box_impoveriti", "box impoverito", x))
        for x in cp.confronta_fatti(orig, testo):
            R.append(("ciclo_prosa confronta_fatti", "fatto cambiato", x))
    return R, doppioni


def rilievi_V(righe: "list[str]", rel: str, orig: "str | None" = None) -> dict:
    testo = "\n".join(righe)
    corpo = mc.corpo_del_box(righe)
    R = [("ciclo_prosa segnala", _classifica(s), s.dettaglio[:120]) for s in cp.segnala(testo)]
    altri, doppioni = _comuni(testo, corpo, rel, orig)
    R += altri
    if mc.box_senza_costrutto_italiano(testo):
        R.append(("misura_craft --costrutto-italiano", "senza c'è né dislocazione", ""))
    # voto_scrittura: i suoi controlli dei box, uno per uno; nessuno è nuovo
    c = vs.controlli(testo, "box")
    for k in ("box_tetto_righe", "box_un_nome", "box_senza_parentesi", "box_senza_sembra",
              "box_p1", "box_senza_metrature", "calchi", "tic_gioco"):
        if not c[k][0]:
            doppioni.append(("voto_scrittura", k))
    e = pm.valuta(_tmp(testo, rel), SPEC)
    return {"rilievi": R, "doppioni": doppioni, "mqm_penalita": e["penalita"],
            "mqm_dettaglio": {d["norma"]: d["conteggio"] for d in e["dettaglio"]}}


def rilievi_N(righe: "list[str]", rel: str, orig: "str | None" = None) -> dict:
    testo = "\n".join(righe)
    corpo = mc.corpo_del_box(righe)
    with senza_watchlist():
        seg = cp.segnala(testo)
    R, indicatori = [], {"P1": 0, "nomi distinti": len(mc.nomi_propri(corpo) - set(mc.PG))}
    for s in seg:
        n = _classifica(s)
        if n in ("box con più nomi propri", "possessivo sul corpo"):
            continue
        if n == "P1":
            indicatori["P1"] += 1
            continue
        R.append(("ciclo_prosa segnala", n, s.dettaglio[:120]))
    altri, _ = _comuni(testo, corpo, rel, orig)
    R += altri
    a = ms.analizza(corpo, nlp())
    prog_regex = sum(1 for r in R if r[1] == "stare+gerundio")
    for k in ("sogg_preverbale", "agg_complesso", "stare_gerundio"):
        voci = a["rilievi"].get(k, [])
        if k == "stare_gerundio":
            voci = voci[prog_regex:]          # lo stesso calco non si conta due volte
            k = "stare+gerundio"
        R += [("misura_sintassi", k, str(v)[:120]) for v in voci]
    if a["livelli_max"] > 2:
        R.append(("misura_sintassi", "oltre due livelli", f"{a['livelli_max']} livelli"))
    indicatori["pron_soggetto"] = a["pron_soggetto"]
    return {"rilievi": R, "indicatori": indicatori,
            "sintassi": {k: a[k] for k in ("profondita_max", "livelli_max", "lungh_dip",
                                           "mattr_lemmi", "rip_interna%", "frasi")}}


def indicatori(righe: "list[str]") -> dict:
    corpo = mc.corpo_del_box(righe)
    testo = "\n".join(righe)
    let = cp.lettura(testo)
    par = mc._parole(corpo)
    return {"parole": par, "frasi": mc.frasi_del_box(corpo), "righe": len(righe),
            "caratteri": len(corpo), "sensoriali": mc.dettagli_sensoriali(corpo),
            "-mente": len(mc.avverbi_mente(corpo)), "gulpease": round(mc.gulpease(corpo), 1),
            "ritmo": let["ritmo"], "in 30-70": int(mc.LUNGHEZZA_TIPICA[0] <= par <= mc.LUNGHEZZA_TIPICA[1]),
            "nomi distinti": len(mc.nomi_propri(corpo) - set(mc.PG))}


def conta(R: list) -> "dict[str, int]":
    return dict(Counter(r[1] for r in R))


def unione(cV: dict, cN: dict) -> "dict[str, int]":
    return {n: max(cV.get(n, 0), cN.get(n, 0)) for n in set(cV) | set(cN)}


def per_famiglia(c: dict) -> "dict[str, int]":
    out = {"comuni": 0, "solo V": 0, "solo N": 0}
    for n, k in c.items():
        out[FAMIGLIA.get(n, "comuni")] += k
    return out


# ── le scene ────────────────────────────────────────────────────────────────
def profili() -> "dict[str, dict]":
    cfg = dd.carica_config()
    out = {}
    for mod in cs.moduli(cs.carica_config()):
        out[mod["file"]] = {**mod, **cfg.get("profili", {}).get(mod["file"], {})}
    out.update(PROFILI_ARC08)
    return out


V_D = {f"D{i}" for i in range(1, 18)} | {"D6-5E"}


def rilievi_scene(rel: str, testo: "str | None" = None) -> dict:
    prof = profili().get(rel, {})
    testo = testo if testo is not None else (ROOT / rel).read_text(encoding="utf-8")
    scene = cs.scene(cs.pulisci(testo), prof.get("scena", cs.SCENA_DEF), prof.get("escludi"))
    if not scene:
        # un file senza scene non è un modulo: la D3 sull'intero modulo qui è rumore
        return {"scene": 0, "V": [], "N": [], "N_indicatori": []}
    tutti = dd.analizza(testo, prof)
    return {"scene": len(scene),
            "V": [list(r) for r in tutti if r[0] in V_D],
            "N": [list(r) for r in tutti if r[0] not in ("D20",)],
            "N_indicatori": [list(r) for r in tutti if r[0] == "D20"]}


# ── base ────────────────────────────────────────────────────────────────────
def base() -> int:
    t0 = time.perf_counter()
    nlp()
    t_spacy = time.perf_counter() - t0
    t_v = t_n = 0.0
    dati = {"files": [], "seme": SEME}
    for rel in FILES:
        voce = {"file": rel, "box": []}
        for b in box_del_file(rel):
            t0 = time.perf_counter()
            v = rilievi_V(b["righe"], rel)
            t1 = time.perf_counter()
            n = rilievi_N(b["righe"], rel)
            t2 = time.perf_counter()
            t_v += t1 - t0
            t_n += t2 - t1
            voce["box"].append({k: b[k] for k in ("id", "riga", "titolo", "parole", "indice")} | {
                "V": v["rilievi"], "N": n["rilievi"], "doppioni_V": v["doppioni"],
                "mqm_penalita": v["mqm_penalita"], "N_indicatori": n["indicatori"],
                "sintassi": n["sintassi"], "indicatori": indicatori(b["righe"])})
        t0 = time.perf_counter()
        sc = rilievi_scene(rel)
        dt = time.perf_counter() - t0
        t_v += dt          # domande_developer gira una volta e si filtra: lo stesso tempo
        t_n += dt
        voce["scene"] = sc
        dati["files"].append(voce)
        print(f"{rel}: {len(voce['box'])} box, {sc['scene']} scene", file=sys.stderr)
    # coerenza fatti sull'arco: solo N
    t0 = time.perf_counter()
    coer = {}
    for arco, d in (("ARC-07", "07_il Portale Della Forgia Eterna"), ("ARC-08", "08_La Battaglia Di Hammerfist")):
        r = cc.rileva_contraddizioni([ROOT / d])
        coer[arco] = {"file_letti": len(r["file_letti"]), "contraddizioni": len(r["contraddizioni"]),
                      "attributi_estratti": r["attributi_estratti"],
                      "per_attributo": r["per_attributo"]}
    t_coer = time.perf_counter() - t0
    t_n += t_coer
    dati["coerenza"] = coer
    dati["tempi_s"] = {"V": round(t_v, 2), "N": round(t_n, 2), "di cui coerenza (N)": round(t_coer, 2),
                       "caricamento spaCy (N, una volta)": round(t_spacy, 2),
                       "nota": "una corsa, 4 core locali; il caricamento di spaCy è a parte"}
    (QUI / "base").mkdir(exist_ok=True)
    (QUI / "base" / "BASE.json").write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n",
                                            encoding="utf-8")
    (QUI / "base" / "BASE.txt").write_text(testo_base(dati), encoding="utf-8")
    print(testo_base(dati).split("\n\nPER BOX")[0])
    return 0


def testo_base(dati: dict) -> str:
    out = ["BASE ARC-07 (5 DEF) e ARC-08 — rilievi della catena V e della catena N",
           f"tempi: V {dati['tempi_s']['V']} s · N {dati['tempi_s']['N']} s "
           f"(coerenza {dati['tempi_s']['di cui coerenza (N)']} s) + caricamento spaCy "
           f"{dati['tempi_s']['caricamento spaCy (N, una volta)']} s — {dati['tempi_s']['nota']}", "",
           f"{'file':58} {'box':>4} {'V':>5} {'N':>5} {'solo V':>7} {'solo N':>7} {'entr.':>6} {'puliti V':>9} {'puliti N':>9}"]
    tot = Counter()
    per_norma = {"V": Counter(), "N": Counter()}
    for f in dati["files"]:
        c = Counter()
        for b in f["box"]:
            cv_, cn = Counter(r[1] for r in b["V"]), Counter(r[1] for r in b["N"])
            per_norma["V"].update(cv_)
            per_norma["N"].update(cn)
            entrambe = sum((cv_ & cn).values())
            c.update({"box": 1, "V": sum(cv_.values()), "N": sum(cn.values()),
                      "soloV": sum((cv_ - cn).values()), "soloN": sum((cn - cv_).values()),
                      "entrambe": entrambe, "pulitiV": int(not cv_), "pulitiN": int(not cn)})
        tot.update(c)
        out.append(f"{f['file'][-58:]:58} {c['box']:>4} {c['V']:>5} {c['N']:>5} {c['soloV']:>7} {c['soloN']:>7} "
                   f"{c['entrambe']:>6} {c['pulitiV']:>9} {c['pulitiN']:>9}")
    out.append(f"{'TOTALE':58} {tot['box']:>4} {tot['V']:>5} {tot['N']:>5} {tot['soloV']:>7} {tot['soloN']:>7} "
               f"{tot['entrambe']:>6} {tot['pulitiV']:>9} {tot['pulitiN']:>9}")
    out += ["", "rilievi per norma (box):", f"{'norma':32} {'V':>5} {'N':>5}  famiglia · strumento"]
    for n in sorted(set(per_norma["V"]) | set(per_norma["N"]), key=lambda n: -(per_norma["V"][n] + per_norma["N"][n])):
        out.append(f"{n:32} {per_norma['V'][n]:>5} {per_norma['N'][n]:>5}  {FAMIGLIA.get(n, '?')} · {STRUMENTO.get(n, '')}")
    out += ["", "scene (domande_developer): V = D1-D17, N = D1-D21 (D20 indicatore)",
            f"{'file':58} {'scene':>5} {'V':>4} {'N':>4}  regole solo N"]
    for f in dati["files"]:
        s = f["scene"]
        nuove = Counter(r[0] for r in s["N"] if r[0] not in V_D)
        out.append(f"{f['file'][-58:]:58} {s['scene']:>5} {len(s['V']):>4} {len(s['N']):>4}  "
                   + " ".join(f"{k} {v}" for k, v in sorted(nuove.items())))
    out += ["", "coerenza_campagna fatti (solo N): " + " · ".join(
        f"{a}: {d['contraddizioni']} contraddizioni su {d['attributi_estratti']} attributi, {d['file_letti']} file"
        for a, d in dati["coerenza"].items())]
    out += ["", "PER BOX (V: rilievi catena vecchia · N: catena nuova · = in entrambe)"]
    for f in dati["files"]:
        if not f["box"]:
            continue
        out.append(f"\n{f['file']}")
        for b in f["box"]:
            cv_, cn = Counter(r[1] for r in b["V"]), Counter(r[1] for r in b["N"])
            parti = [f"={n}×{k}" for n, k in sorted((cv_ & cn).items())]
            parti += [f"V:{n}×{k}" for n, k in sorted((cv_ - cn).items())]
            parti += [f"N:{n}×{k}" for n, k in sorted((cn - cv_).items())]
            out.append(f"  r.{b['riga']:<5} {b['parole']:>4}p  V{sum(cv_.values()):>2} N{sum(cn.values()):>2}  "
                       f"{b['titolo'][:40]:40}  " + (", ".join(parti) or "pulito"))
    return "\n".join(out) + "\n"


# ── campione ────────────────────────────────────────────────────────────────
def congelati() -> "set[tuple[str, str]]":
    return {(c["file"], re.sub(r"\s+", " ", c["testo"]).strip()[:120])
            for c in json.loads(CONGELATI.read_text(encoding="utf-8"))}


def campione() -> int:
    dati = json.loads((QUI / "base" / "BASE.json").read_text(encoding="utf-8"))
    gelo = congelati()
    rng = random.Random(SEME)
    scelti = []
    for arco, files in (("ARC-07", ARC07), ("ARC-08", ARC08)):
        cand = []
        for f in dati["files"]:
            if f["file"] not in files:
                continue
            corpi = {b["indice"]: b for b in box_del_file(f["file"])}
            for b in f["box"]:
                corpo = corpi[b["indice"]]["corpo"]
                if b["parole"] < cv.PAROLE_MINIME or cv._NOTA_DI_REGOLA.search(corpo):
                    continue
                if (f["file"], corpo[:120]) in gelo:
                    continue
                cand.append({"file": f["file"], **b, "nV": len(b["V"]), "nN": len(b["N"]),
                             "caso": rng.random()})
        presi: "list[dict]" = []

        def prendi(lista, k, strato):
            for c in lista:
                if k == 0:
                    break
                if any(c["id"] == p["id"] for p in presi):
                    continue
                presi.append({**c, "strato": strato})
                k -= 1
        prendi(sorted(cand, key=lambda c: (-c["nN"], c["caso"])), 3, "più rilievi N")
        prendi(sorted(cand, key=lambda c: (-c["nV"], c["caso"])), 3, "più rilievi V")
        prendi(sorted([c for c in cand if c["nV"] == 0 and c["nN"] == 0], key=lambda c: c["caso"]), 1,
               "pulito per entrambe")
        prendi(sorted([c for c in cand if c["nV"] == 0 and c["nN"] > 0], key=lambda c: c["caso"]), 1,
               "pulito per V, non per N")
        prendi(sorted([c for c in cand if c["nN"] == 0 and c["nV"] > 0], key=lambda c: c["caso"]),
               8 - len(presi), "pulito per N, non per V")
        prendi(sorted(cand, key=lambda c: c["caso"]), 8 - len(presi), "a caso")
        print(f"{arco}: {len(cand)} candidati (≥{cv.PAROLE_MINIME} parole, non congelati, non note di regola)")
        scelti += presi
    out = []
    for i, c in enumerate(scelti, 1):
        out.append({"id": f"B{i:02d}", "box": c["id"], "file": c["file"], "riga": c["riga"],
                    "indice": c["indice"], "titolo": c["titolo"], "strato": c["strato"],
                    "nV": c["nV"], "nN": c["nN"], "parole": c["parole"]})
        print(f"B{i:02d} {c['strato']:26} V{c['nV']} N{c['nN']} {c['parole']:>3}p {c['file'][-40:]} r.{c['riga']} {c['titolo'][:40]}")
    (QUI / "campione").mkdir(exist_ok=True)
    (QUI / "campione" / "CAMPIONE.json").write_text(
        json.dumps({"seme": SEME, "criterio": "per arco: 3 con più rilievi N, 3 con più rilievi V, "
                    "1 pulito per entrambe, 1 pulito per V e non per N; esclusi i 25 CONGELATI, i box "
                    f"sotto {cv.PAROLE_MINIME} parole e le note di regola", "box": out},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # lo scheletro delle versioni, con l'originale
    vers = QUI / "versioni" / "BOX.md"
    if not vers.exists():
        vers.parent.mkdir(exist_ok=True)
        r = ["# Versioni dei box del campione", "",
             "O = originale (non toccare). V1..V3 = iterazioni della catena vecchia, N1..N3 della nuova,",
             "F = fusione (CRITERIO-FUSIONE.txt). L'ultima iterazione presente è la versione dell'arm.", ""]
        for c in out:
            b = box_del_file(c["file"])[c["indice"]]
            r += [f"## {c['id']} · {Path(c['file']).stem} r.{c['riga']} · {c['titolo']}",
                  f"<!-- file: {c['file']} · indice {c['indice']} · strato: {c['strato']} -->", "",
                  "### O", "", *b["righe"], ""]
        vers.write_text("\n".join(r) + "\n", encoding="utf-8")
    return 0


# ── le versioni ─────────────────────────────────────────────────────────────
def leggi_versioni() -> "dict[str, dict]":
    testo = (QUI / "versioni" / "BOX.md").read_text(encoding="utf-8")
    out = {}
    for blocco in re.split(r"(?m)^## ", testo)[1:]:
        bid = blocco.split()[0]
        meta = re.search(r"<!-- file: (.*?) · indice (\d+)", blocco)
        arms = {}
        for m in re.finditer(r"(?ms)^### ([A-Z]\d?)\s*$\n(.*?)(?=^### |\Z)", blocco):
            righe = [r for r in m.group(2).strip("\n").splitlines()]
            while righe and not righe[-1].strip():
                righe.pop()
            while righe and not righe[0].strip():
                righe.pop(0)
            nota = [r for r in righe if r.startswith("<!--")]
            arms[m.group(1)] = {"righe": [r for r in righe if not r.startswith("<!--")], "nota": nota}
        out[bid] = {"file": meta.group(1), "indice": int(meta.group(2)), "arms": arms}
    return out


def finale(arms: dict, lettera: str) -> "tuple[str, list[str]] | None":
    chiavi = sorted((k for k in arms if k.startswith(lettera) and k[1:].isdigit()), key=lambda k: int(k[1:]))
    if lettera == "F" and "F" in arms:
        return "F", arms["F"]["righe"]
    if chiavi:
        return chiavi[-1], arms[chiavi[-1]]["righe"]
    return "O", arms["O"]["righe"]       # l'arm non ha trovato niente da correggere


def misura_tutto(righe: "list[str]", rel: str, orig: "list[str] | None") -> dict:
    o = "\n".join(orig) if orig is not None else None
    v = rilievi_V(righe, rel, o)
    n = rilievi_N(righe, rel, o)
    cV, cN = conta(v["rilievi"]), conta(n["rilievi"])
    u = unione(cV, cN)
    return {"V": v["rilievi"], "N": n["rilievi"], "cV": cV, "cN": cN, "unione": u,
            "famiglie": per_famiglia(u), "mqm_penalita": v["mqm_penalita"],
            "mqm_dettaglio": v["mqm_dettaglio"], "doppioni_V": v["doppioni"],
            "N_indicatori": n["indicatori"], "sintassi": n["sintassi"], "indicatori": indicatori(righe)}


def misura(ids: "list[str]") -> int:
    vers = leggi_versioni()
    for bid, d in vers.items():
        if ids and bid not in ids:
            continue
        orig = d["arms"]["O"]["righe"]
        print(f"\n{bid}  {d['file'][-45:]}")
        for k in sorted(d["arms"], key=lambda k: (k[0] != "O", k)):
            m = misura_tutto(d["arms"][k]["righe"], d["file"], None if k == "O" else orig)
            def fmt(c):
                return ", ".join(f"{n}×{x}" for n, x in sorted(c.items())) or "pulito"
            print(f"  {k:3} V[{sum(m['cV'].values())}] {fmt(m['cV'])}")
            print(f"      N[{sum(m['cN'].values())}] {fmt(m['cN'])}")
            ind = m["indicatori"]
            print(f"      parole {ind['parole']} sens {ind['sensoriali']} gulp {ind['gulpease']} "
                  f"liv {m['sintassi']['livelli_max']} P1 {m['N_indicatori']['P1']} nomi {ind['nomi distinti']}")
            if k != "O":
                det = [r for r in m["V"] + m["N"] if r[1] in ("fatto cambiato", "box impoverito")]
                for r in dict.fromkeys(tuple(x) for x in det):
                    print(f"      ✗ {r[1]}: {r[2]}")
                for r in m["N"]:
                    if r[0] == "misura_sintassi":
                        print(f"      · {r[1]}: {r[2]}")
    return 0


# ── la fusione: la regola, applicata ai numeri ─────────────────────────────
def esclusa(m: dict) -> bool:
    return bool(m["unione"].get("fatto cambiato") or m["unione"].get("box impoverito"))


def decidi_fusione(mV: dict, mN: dict) -> "tuple[str, str]":
    """Regole 1-3 di CRITERIO-FUSIONE.txt: ('V'|'N'|'fondere', perché)."""
    eV, eN = esclusa(mV), esclusa(mN)
    if eV and not eN:
        return "N", "V esclusa (fatti o impoverimento)"
    if eN and not eV:
        return "V", "N esclusa (fatti o impoverimento)"
    fV, fN = mV["famiglie"], mN["famiglie"]
    fam = ("comuni", "solo V", "solo N")
    if all(fV[f] <= fN[f] for f in fam) and any(fV[f] < fN[f] for f in fam):
        return "V", "V domina: " + " · ".join(f"{f} {fV[f]}/{fN[f]}" for f in fam)
    if all(fN[f] <= fV[f] for f in fam) and any(fN[f] < fV[f] for f in fam):
        return "N", "N domina: " + " · ".join(f"{f} {fV[f]}/{fN[f]}" for f in fam)
    if all(fV[f] == fN[f] for f in fam):
        sV, sN = mV["indicatori"]["sensoriali"], mN["indicatori"]["sensoriali"]
        return ("V" if sV > sN else "N"), f"pari; sensoriali V {sV}, N {sN}"
    return "fondere", "vittorie incrociate: " + " · ".join(f"{f} {fV[f]}/{fN[f]}" for f in fam)


def accetta_fusione(mF: dict, mV: dict, mN: dict) -> "tuple[bool, str]":
    tot = lambda m: sum(m["famiglie"].values())  # noqa: E731
    ok_a = tot(mF) <= min(tot(mV), tot(mN))
    ok_b = mF["indicatori"]["sensoriali"] >= min(mV["indicatori"]["sensoriali"], mN["indicatori"]["sensoriali"])
    ok_c = not mF["unione"].get("fatto cambiato")
    return ok_a and ok_b and ok_c, (f"a) totale F {tot(mF)} ≤ min(V {tot(mV)}, N {tot(mN)}): {ok_a} · "
                                    f"b) sensoriali: {ok_b} · c) fatti invariati: {ok_c}")


# ── incrociata ──────────────────────────────────────────────────────────────
def incrociata() -> int:
    vers = leggi_versioni()
    camp = {c["id"]: c for c in json.loads((QUI / "campione" / "CAMPIONE.json").read_text(encoding="utf-8"))["box"]}
    out = {"box": [], "scene": []}
    tV = tN = 0.0
    for bid, d in vers.items():
        rel, orig = d["file"], d["arms"]["O"]["righe"]
        voce = {"id": bid, "file": rel, "titolo": camp[bid]["titolo"], "riga": camp[bid]["riga"],
                "strato": camp[bid]["strato"], "versioni": {}, "iterazioni": {}}
        for lettera in ("V", "N"):
            its = sorted((k for k in d["arms"] if k.startswith(lettera) and k[1:].isdigit()), key=lambda k: int(k[1:]))
            voce["iterazioni"][lettera] = []
            for k in its:
                t0 = time.perf_counter()
                m = misura_tutto(d["arms"][k]["righe"], rel, orig)
                dt = time.perf_counter() - t0
                if lettera == "V":
                    tV += dt
                else:
                    tN += dt
                voce["iterazioni"][lettera].append({"k": k, "cV": m["cV"], "cN": m["cN"]})
        mO = misura_tutto(orig, rel, None)
        voce["versioni"]["O"] = {"righe": orig, **mO}
        for lettera in ("V", "N"):
            k, righe = finale(d["arms"], lettera)
            voce["versioni"][lettera] = {"righe": righe, "k": k, "nota": d["arms"][k]["nota"] if k != "O" else [],
                                         **misura_tutto(righe, rel, orig)}
        mV, mN = voce["versioni"]["V"], voce["versioni"]["N"]
        regola, perche = decidi_fusione(mV, mN)
        voce["fusione"] = {"regola": regola, "perche": perche}
        if regola == "fondere" and "F" in d["arms"]:
            mF = misura_tutto(d["arms"]["F"]["righe"], rel, orig)
            ok, det = accetta_fusione(mF, mV, mN)
            voce["fusione"]["accettata"] = ok
            voce["fusione"]["condizioni"] = det
            if ok:
                voce["versioni"]["F"] = {"righe": d["arms"]["F"]["righe"], "k": "F", **mF}
            else:
                tot = lambda m: sum(m["famiglie"].values())  # noqa: E731
                ripiego = "V" if (tot(mV), -mV["indicatori"]["sensoriali"]) < (tot(mN), -mN["indicatori"]["sensoriali"]) else "N"
                voce["fusione"]["ripiego"] = ripiego
                voce["versioni"]["F"] = {**voce["versioni"][ripiego], "k": f"F={ripiego}"}
        elif regola == "fondere":
            voce["fusione"]["accettata"] = None
            voce["versioni"]["F"] = {**voce["versioni"]["N"], "k": "F=N (fusione non scritta)"}
        else:
            voce["versioni"]["F"] = {**voce["versioni"][regola], "k": f"F={regola}"}
        out["box"].append(voce)
        print(f"{bid}: fusione → {regola} ({perche})", file=sys.stderr)
    # le scene
    sc = QUI / "scene"
    for f in sorted(sc.glob("S*.md")) if sc.exists() else []:
        testo = f.read_text(encoding="utf-8")
        meta = re.search(r"<!-- scena: file=(.*?) · titolo=(.*?) · aggiunte=(.*?) -->", testo)
        prima, dopo = re.split(r"(?m)^<!-- DOPO -->\s*$", testo.split("<!-- PRIMA -->", 1)[1])
        rel = meta.group(1)
        prof = profili().get(rel, {})
        def d_(t):
            return [list(r) for r in dd.analizza(t, {**prof, "escludi": None}, con_ts=False)]
        out["scene"].append({"id": f.stem, "file": rel, "titolo": meta.group(2), "aggiunte": meta.group(3),
                             "prima": prima.strip("\n"), "dopo": dopo.strip("\n"),
                             "rilievi_prima": d_(prima), "rilievi_dopo": d_(dopo),
                             "diff_righe": [r for r in difflib.unified_diff(prima.strip().splitlines(),
                                                                             dopo.strip().splitlines(), lineterm="", n=0)
                                            if r[:1] in "+-" and not r.startswith(("+++", "---"))]})
    # coerenza sull'arco con i box riscritti, per arm
    out["coerenza"] = coerenza_arm(out["box"])
    (QUI / "misure").mkdir(exist_ok=True)
    (QUI / "misure" / "INCROCIATA.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8")
    print(riassunto(out))
    (QUI / "misure" / "RIASSUNTO.txt").write_text(riassunto(out), encoding="utf-8")
    return 0


def coerenza_arm(box: list) -> dict:
    """coerenza_campagna fatti sull'arco intero, con i box del campione sostituiti
    dalla versione di ogni arm: il numero di contraddizioni cambia?"""
    import shutil
    risultati = {}
    for arm in ("O", "V", "N", "F"):
        risultati[arm] = {}
        for arco, cartella in (("ARC-07", "07_il Portale Della Forgia Eterna"), ("ARC-08", "08_La Battaglia Di Hammerfist")):
            dest = _TMP / f"coer-{arm}" / cartella
            if dest.exists():
                shutil.rmtree(dest)
            dest.mkdir(parents=True)
            for p in (ROOT / cartella).glob("*.md"):
                testo = p.read_text(encoding="utf-8")
                for b in box:
                    if b["file"] == str(p.relative_to(ROOT)) and arm != "O":
                        vecchio = "\n".join(b["versioni"]["O"]["righe"])
                        nuovo = "\n".join(b["versioni"][arm]["righe"])
                        testo = testo.replace(vecchio, nuovo, 1)
                (dest / p.name).write_text(testo, encoding="utf-8")
            r = cc.rileva_contraddizioni([dest])
            risultati[arm][arco] = {"contraddizioni": len(r["contraddizioni"]),
                                    "attributi_estratti": r["attributi_estratti"]}
    return risultati


def riassunto(out: dict) -> str:
    righe = ["MISURA INCROCIATA — O, V, N, F con tutte le misure", ""]
    tot = {a: Counter() for a in "OVNF"}
    for b in out["box"]:
        for a in "OVNF":
            m = b["versioni"][a]
            tot[a].update({"rilievi V": sum(m["cV"].values()), "rilievi N": sum(m["cN"].values()),
                           "unione": sum(m["unione"].values()), "sensoriali": m["indicatori"]["sensoriali"],
                           "parole": m["indicatori"]["parole"], "mqm": m["mqm_penalita"],
                           **{f"fam {k}": v for k, v in m["famiglie"].items()}})
    chiavi = ["rilievi V", "rilievi N", "unione", "fam comuni", "fam solo V", "fam solo N", "mqm",
              "sensoriali", "parole"]
    righe.append(f"{'totali su ' + str(len(out['box'])) + ' box':26}" + "".join(f"{a:>8}" for a in "OVNF"))
    for k in chiavi:
        righe.append(f"{k:26}" + "".join(f"{tot[a][k]:>8}" for a in "OVNF"))
    righe += ["", "fusione per box:"]
    for b in out["box"]:
        f = b["fusione"]
        righe.append(f"  {b['id']} {f['regola']:8} {f['perche']}" + (f" · {f.get('condizioni', '')}" if f.get("condizioni") else ""))
    righe += ["", "coerenza_campagna fatti, contraddizioni sull'arco con i box sostituiti:"]
    for a, d in out["coerenza"].items():
        righe.append(f"  {a}: " + " · ".join(f"{k} {v['contraddizioni']}" for k, v in d.items()))
    righe += ["", "scene (domande_developer, prima → dopo):"]
    for s in out["scene"]:
        p = Counter(r[0] for r in s["rilievi_prima"])
        q = Counter(r[0] for r in s["rilievi_dopo"])
        righe.append(f"  {s['id']} {s['titolo'][:40]:40} " + " · ".join(
            f"{k} {p[k]}→{q[k]}" for k in sorted(set(p) | set(q))) + f"  (+{sum(1 for r in s['diff_righe'] if r[0] == '+')} righe)")
    return "\n".join(righe) + "\n"


# ── cieco ───────────────────────────────────────────────────────────────────
def cieco() -> int:
    """Due schede con cieco_versioni.coppie: V contro N, e F contro O dove F è
    una fusione vera. Tutte le coppie vanno al DM (CONTROLLI alzato: qui la
    misura non decide nessuna coppia, perché la calibrazione dice che non
    prevede il DM)."""
    dati = json.loads((QUI / "misure" / "INCROCIATA.json").read_text(encoding="utf-8"))
    cart = QUI / "cieco"
    chiavi = QUI / "chiave"
    cart.mkdir(exist_ok=True)
    chiavi.mkdir(exist_ok=True)
    cv.CONTROLLI = 10 ** 6
    schede = []
    for nome, vecchia, nuova, filtro in (
            ("V-N", "V", "N", lambda b: True),
            ("F-O", "O", "F", lambda b: b["versioni"]["F"]["k"] == "F")):
        voci, nuovo_md = [], ["# testi", ""]
        for b in dati["box"]:
            if not filtro(b):
                continue
            titolo = f"Box {b['id']}"
            vecchio = mc.corpo_del_box(b["versioni"][vecchia]["righe"])
            voci.append({"file": f"plans/esperimenti/qualita-misurabile-2026-10-22/riscrittura/cieco/testi-{nome.lower()}.md",
                         "indice": len(voci), "titolo": titolo, "testo": vecchio, "parole": len(vecchio.split())})
            nuovo_md += [f"## {titolo}", "", *b["versioni"][nuova]["righe"], ""]
        if not voci:
            continue
        (cart / f"testi-{nome.lower()}.md").write_text("\n".join(nuovo_md) + "\n", encoding="utf-8")
        camp = {"ref": "", "seme": SEME, "per_file": len(voci), "parole_minime": cv.PAROLE_MINIME, "voci": voci}
        scheda, chiave = cv.coppie(camp, "", SEME + len(nome))
        chiave["confronto"] = {"vecchia": vecchia, "nuova": nuova,
                               "nota": "«nuova» nella chiave = la seconda versione del confronto"}
        (chiavi / f"CHIAVE-{nome}.json").write_text(json.dumps(chiave, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8")
        schede.append((nome, scheda, chiave))
        (cart / f"testi-{nome.lower()}.md").unlink()   # serviva solo a coppie(): i testi sono nella scheda
    testa = ["# Scheda cieca — riscrittura automatica di ARC-07 e ARC-08", "",
             "Due prove, in due parti. Per ogni coppia leggi ad alta voce **A** e poi **B**, e scrivi",
             "una riga nel file dei voti: `N A`, `N B` o `N =`. Dopo la lettera, se vuoi, le",
             "etichette di ciò che non andava nella versione scartata (anche più d'una):",
             "", *[f"- `{k}`: {v}" for k, v in cv.ETICHETTE.items()], "",
             "Esempio: `7 B goffo spiega`. Le due parti hanno numerazioni proprie: scrivi i voti",
             "in due file, `VOTI-1.txt` e `VOTI-2.txt`. Non aprire `CONFRONTO.html` prima di aver votato.", ""]
    for i, (nome, scheda, chiave) in enumerate(schede, 1):
        corpo = scheda.split("\n", 6)[-1] if False else "\n".join(
            r for r in scheda.splitlines() if not r.startswith("# Confronto cieco")
            and not r.startswith("Leggi ad alta voce") and not r.startswith("Se vuoi, dopo la lettera"))
        corpo = re.sub(r"\*testi-[a-z-]+\.md · (Box B\d+)\*", r"*\1*", corpo)
        n_cop = sum(1 for c in chiave["coppie"] if c["stato"] != "identica")
        ident = [c["titolo"] for c in chiave["coppie"] if c["stato"] == "identica"]
        testa += [f"## Parte {i} — {n_cop} coppie", "",
                  ("Due riscritture dello stesso box, fatte con due catene di strumenti diverse."
                   if nome == "V-N" else
                   "L'originale contro una fusione delle due riscritture, dove la fusione è un testo nuovo."),
                  (f"Box con le due versioni identiche, non si votano: {', '.join(ident)}." if ident else ""),
                  "", corpo.strip(), ""]
    (cart / "SCHEDA-CIECA.md").write_text("\n".join(testa) + "\n", encoding="utf-8")
    print(f"scheda: {cart / 'SCHEDA-CIECA.md'} · chiavi in {chiavi}")
    return 0


# ── pagina ──────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    cmd = argv[0] if argv else "base"
    if cmd == "base":
        return base()
    if cmd == "campione":
        return campione()
    if cmd == "misura":
        return misura(argv[1:])
    if cmd == "incrociata":
        return incrociata()
    if cmd == "cieco":
        return cieco()
    if cmd == "pagina":
        import pagina
        return pagina.scrivi(QUI)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
