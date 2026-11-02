#!/usr/bin/env python3
"""migliora_prosa.py — una pipeline che sceglie la riscrittura di un box e misura se è migliore.

Il giudice di «migliore» resta il voto cieco del DM (ADR-0093): nessuna misura
automatica lo prevedeva (`RICERCA-QUALITA-MISURABILE-2026-10` §3). Questo script
mette in fila quattro cose, e la generazione delle candidate **non** è fra queste:
le scrive un agente (o una persona), lo script non chiama modelli linguistici.

| Comando | Cosa fa |
|---|---|
| `dataset` | raccoglie tutte le coppie votate alla cieca dal DM in `pipeline/VOTI.json` |
| `modello` | addestra il modello di preferenza e lo valida in leave-one-out, contro il caso e contro «vince la più lunga» |
| `scegli` | sceglie con un seme i box di ARC-07 e ARC-08 da migliorare, esclusi i congelati e quelli già usati |
| `migliora FILE --box N --candidate C.md` | filtra le candidate (fatti, box impoverito, regole 1-4 di §2-ter), le ordina col modello, dice la migliore |
| `campione` | scheda cieca: la vincitrice della pipeline contro l'originale, con `cieco_versioni.coppie` |
| `esito` | registra i voti in `VOTI.json`, rifà il modello, dice quanto vince la pipeline (Wilson) |
| `languagetool` | facoltativo: rilievi di un server LanguageTool locale, precisione letta a mano, calibrazione, varianti del modello con McNemar (`languagetool/README.md`) |

**Il modello** è una regressione logistica senza intercetta sulle differenze dei
tratti di due versioni (Bradley-Terry), con penalità L2, in libreria standard.
Modello e soglia sono fissati in `pipeline/SOGLIA.txt`, scritto prima di
addestrarlo: se l'accuratezza in leave-one-out non supera il caso (limite
inferiore di Wilson sopra 0,50) e la regola «vince la più lunga», il modello
ordina le candidate solo come suggerimento, e la pipeline vale come filtro di
non regressione e come raccoglitore di voti.

**Il filtro** scarta una candidata che cambia un fatto (`ciclo_prosa.confronta_fatti`),
che `ciclo_prosa.box_impoveriti` segnala, o che viola una delle regole di
`read-aloud-adulti.md` §2-ter misurabili: (1) meno dettagli sensoriali,
(2) monologo spezzato in battute, (3) frase finale tolta, (4) subordinata
spezzata. La regola 5 (guardare a occhio un rilievo di `misura_sintassi` prima
di riscrivere) riguarda chi scrive e non si misura.

Uso:

    python3 scripts/migliora_prosa.py dataset
    python3 scripts/migliora_prosa.py modello [--scrivi]
    python3 scripts/migliora_prosa.py scegli --seme 20261023 --n 6 --uscita BOX.json
    python3 scripts/migliora_prosa.py migliora FILE --box N --candidate C.md [--scelte S.json --id P01]
    python3 scripts/migliora_prosa.py campione --scelte S.json --seme 7 --scheda SCHEDA.md --chiave CHIAVE.json
    python3 scripts/migliora_prosa.py esito --scelte S.json --chiave CHIAVE.json --voti VOTI.txt
    python3 scripts/migliora_prosa.py modello --varianti --tratti-esterni T.json [--tratti-esterni T2.json]
    python3 scripts/migliora_prosa.py languagetool [--url U] [--tratti-esterni T.json] [--scrivi]
    python3 scripts/migliora_prosa.py migliora FILE --box N --candidate C.md --lt

LanguageTool è facoltativo: senza server `languagetool` lo dice ed esce 0, e
`migliora --lt` filtra come senza. La prova del 2026-10-23 non gli ha trovato
gruppi con precisione >= 0,70, quindi il filtro LT oggi non scarta nulla e i
suoi conteggi non entrano nel modello.

spaCy con `it_core_news_md` è facoltativo: senza, il tratto `livelli_max` vale
zero e la subordinata spezzata si stima dal numero di frasi e di subordinanti.
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import random
import re
import statistics as st
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cieco_versioni as cv  # noqa: E402
import ciclo_prosa as cp  # noqa: E402
import misura_craft as mc  # noqa: E402

QUI = ROOT / "plans/esperimenti/qualita-misurabile-2026-10-22"
PIPE = QUI / "pipeline"
VOTI = PIPE / "VOTI.json"
CONGELATI = ROOT / "plans/esperimenti/giro3-arc07-2026-10-19/misure/CONGELATI.json"
CAMPIONE_RISCRITTURA = QUI / "riscrittura/campione/CAMPIONE.json"

ARC07 = [f"07_il Portale Della Forgia Eterna/ARC07-DEF-{i}-{n}.md" for i, n in (
    (1, "PIANO-TERRA-TERROS"), (2, "RITORNO-E-AFFRESCHI"), (3, "RESURREZIONE-HELLA"),
    (4, "VIAGGIO-MILLE-ANNI"), (5, "RITORNO-HAMMERFIST"))]
CARTELLA_ARC08 = "08_La Battaglia Di Hammerfist"

#: Le fonti già votate: le 38 coppie della calibrazione hanno il giro nel campo `set`.
FONTI_38 = {"giro2": "giro2-arc07-2026-10-18", "giro3": "giro3-arc07-2026-10-19",
            "prova": "prova-scrittura-italiana-2026-10-21"}

# ── i parametri fissati in SOGLIA.txt prima di addestrare ────────────────────
LAMBDA = 1.0
TRATTI = ("parole_log", "gulpease", "sensoriali", "gerundi_mente", "possessivi‰",
          "livelli_max", "mattr25", "frase_finale_tolta", "subordinata_spezzata",
          "nomi_tolti", "monologo_spezzato")
#: Il modello decide da solo solo se il limite inferiore di Wilson supera questo.
SOGLIA_WILSON = 0.5

# ── i tratti ─────────────────────────────────────────────────────────────────
_PAROLA = re.compile(r"[A-Za-zÀ-ÿ']+")
_FRASE = re.compile(r"(?<=[.!?…])[»”\"]?\s+")
#: Gli stessi possessivi della calibrazione (calibra_prosa.py, 2026-10-22).
_POSS = re.compile(r"\b(?:il|la|i|le|lo|gli|un|una|del|della|dei|delle|al|alla|nel|nella|sul|sulla)\s+"
                   r"(?:mio|mia|miei|mie|tuo|tua|tuoi|tue|suo|sua|suoi|sue|nostr[oaie]|vostr[oaie]|loro)\b"
                   r"|\b(?:suo|sua|suoi|sue)\b", re.I)
_SUBORDINANTI = re.compile(r"\b(?:che|cui|dove|quando|mentre|perché|finché|poiché|sebbene|benché|"
                           r"affinché|come se|prima che|dopo che)\b", re.I)
_STOP = set("il lo la i gli le un una uno di a da in con su per tra fra e o ma che non si ci vi è sono "
            "era erano ha hanno del della dei delle al alla ai alle dal dalla nel nella nei sul sulla "
            "come più se poi già anche quando dove chi cosa qui lì".split())
_NLP = None


def nlp():
    """Il parser di misura_sintassi, o None se spaCy manca."""
    global _NLP
    if _NLP is None:
        try:
            import misura_sintassi as ms
            _NLP = ms.carica_nlp() or False
        except Exception:
            _NLP = False
    return _NLP or None


def piano(testo: str) -> str:
    """Il testo da leggere: senza marcatura, con i paragrafi."""
    return re.sub(r"[*_`]", "", testo).strip()


def parole(testo: str) -> "list[str]":
    return [w.lower() for w in _PAROLA.findall(testo)]


def frasi(testo: str) -> "list[str]":
    return [f for f in _FRASE.split(piano(testo).replace("\n", " ")) if _PAROLA.search(f)]


def mattr(testo: str, w: int = 25) -> float:
    t = parole(testo)
    if len(t) <= w:
        return len(set(t)) / max(1, len(t))
    return st.mean(len(set(t[i:i + w])) / w for i in range(len(t) - w + 1))


_SINTASSI: dict = {}


def sintassi(testo: str) -> "tuple[int, int] | None":
    """(livelli_max, frasi) di misura_sintassi, o None senza spaCy."""
    if testo not in _SINTASSI:
        n = nlp()
        if n is None:
            _SINTASSI[testo] = None
        else:
            import misura_sintassi as ms
            a = ms.analizza(piano(testo), n)
            _SINTASSI[testo] = (a["livelli_max"], a["frasi"])
    return _SINTASSI[testo]


def _radici(frase: str) -> "set[str]":
    return {w[:5] for w in parole(frase) if w not in _STOP and len(w) > 3}


def frase_finale_tolta(originale: str, testo: str) -> bool:
    """Regola 3 di §2-ter: l'ultima frase dell'originale (almeno tre parole) non
    c'è più: meno della metà delle sue parole piene torna nel testo nuovo."""
    ultime = [f for f in frasi(originale) if len(parole(f)) >= 3]
    if not ultime:
        return False
    chiusa = _radici(ultime[-1])
    if len(chiusa) < 2:
        return False
    return len(chiusa & _radici(testo)) / len(chiusa) < 0.5


def subordinata_spezzata(originale: str, testo: str) -> bool:
    """Regola 4 di §2-ter: più frasi e meno livelli di subordinate (spaCy), o,
    senza parser, più frasi e meno subordinanti."""
    if len(frasi(testo)) <= len(frasi(originale)):
        return False
    a, b = sintassi(originale), sintassi(testo)
    if a is not None and b is not None:
        return b[0] < a[0]
    return len(_SUBORDINANTI.findall(testo)) < len(_SUBORDINANTI.findall(originale))


def monologo_spezzato(originale: str, testo: str) -> bool:
    """Regola 2 di §2-ter, con lo stesso criterio di cieco_versioni.verdetto_misurato."""
    pezzi = testo.strip().count("\n\n") + 1
    return pezzi >= 3 and "\n\n" not in originale.strip() and "«" in originale


def nomi_tolti(originale: str, testo: str) -> int:
    return len(mc.nomi_propri(piano(originale)) - mc.nomi_propri(piano(testo)))


def tratti(testo: str, originale: "str | None") -> "dict[str, float]":
    """I tratti di una versione. Quelli delle regole si misurano rispetto
    all'originale, e valgono zero se l'originale non c'è o è il testo stesso."""
    p = piano(testo)
    n = max(1, len(parole(p)))
    s = sintassi(testo)
    rel = originale is not None and originale.strip() != testo.strip()
    return {
        "parole_log": math.log(n),
        "gulpease": mc.gulpease(p),
        "sensoriali": float(mc.dettagli_sensoriali(p)),
        "gerundi_mente": float(len(mc.gerundi_in_coda(p)) + len(mc.avverbi_mente(p))),
        "possessivi‰": 1000 * len(_POSS.findall(p)) / n,
        "livelli_max": float(s[0]) if s else 0.0,
        "mattr25": mattr(p),
        "frase_finale_tolta": float(rel and frase_finale_tolta(originale, testo)),
        "subordinata_spezzata": float(rel and subordinata_spezzata(originale, testo)),
        "nomi_tolti": float(nomi_tolti(originale, testo)) if rel else 0.0,
        "monologo_spezzato": float(rel and monologo_spezzato(originale, testo)),
    }


def differenza(a: str, b: str, originale: "str | None") -> "list[float]":
    ta, tb = tratti(a, originale), tratti(b, originale)
    return [ta[k] - tb[k] for k in TRATTI]


# ── il modello: logistica L2 senza intercetta, Newton in libreria standard ──
def _risolvi(A: "list[list[float]]", b: "list[float]") -> "list[float]":
    """Gauss con pivot parziale (le matrici sono 11×11)."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        if abs(M[c][c]) < 1e-12:
            continue
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0 for i in range(n)]


def _sig(x: float) -> float:
    return 1 / (1 + math.exp(-x)) if x >= 0 else math.exp(x) / (1 + math.exp(x))


def scale(Z: "list[list[float]]") -> "list[float]":
    d = len(Z[0]) if Z else len(TRATTI)
    return [math.sqrt(sum(z[j] ** 2 for z in Z) / len(Z)) or 1.0 if Z else 1.0 for j in range(d)]


def addestra(Z: "list[list[float]]", lam: float = LAMBDA,
             nomi: "tuple[str, ...] | list[str]" = TRATTI) -> dict:
    """Z: una differenza (vincente − perdente) per coppia. Ogni coppia entra
    nei due versi, quindi il modello è simmetrico e non ha intercetta."""
    s = scale(Z)
    X = [[v / s[j] for j, v in enumerate(z)] for z in Z]
    righe = [(x, 1.0) for x in X] + [([-v for v in x], 0.0) for x in X]
    d = len(s)
    w = [0.0] * d
    for _ in range(50):
        g = [lam * w[j] for j in range(d)]
        H = [[lam if i == j else 0.0 for j in range(d)] for i in range(d)]
        for x, y in righe:
            p = _sig(sum(a * b for a, b in zip(w, x)))
            for i in range(d):
                g[i] += (p - y) * x[i]
                for j in range(d):
                    H[i][j] += p * (1 - p) * x[i] * x[j]
        passo = _risolvi(H, g)
        w = [a - b for a, b in zip(w, passo)]
        if max(abs(v) for v in passo) < 1e-9:
            break
    return {"pesi": w, "scala": s, "tratti": list(nomi), "lambda": lam}


def probabilita(modello: dict, z: "list[float]") -> float:
    """P(la prima versione batte la seconda)."""
    return _sig(sum(w * v / s for w, v, s in zip(modello["pesi"], z, modello["scala"])))


def binom_p(k: int, n: int) -> float:
    """p a due code del test del segno contro 0,5."""
    if n == 0:
        return 1.0
    hi = max(k, n - k)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(hi, n + 1)) / 2 ** n)


def _diff_esterni(a: str, b: str, extra: "list[str]", esterni: "dict | None") -> "list[float]":
    """Le differenze dei tratti esterni: zero se una delle due versioni non li ha."""
    ta = (esterni or {}).get(chiave_esterni(a), {})
    tb = (esterni or {}).get(chiave_esterni(b), {})
    return [ta[k] - tb[k] if k in ta and k in tb else 0.0 for k in extra]


def valida(voti: "list[dict]", extra: "list[str] | tuple" = (), esterni: "dict | None" = None) -> dict:
    """Leave-one-out sulle coppie decise, più le due regole di confronto.
    `extra` sono tratti in più letti da `esterni` (vedi `carica_esterni`)."""
    decise = [v for v in voti if not v["pari"]]
    extra = list(extra)
    nomi = list(TRATTI) + extra
    Z = [differenza(v["vincente"], v["perdente"], v.get("originale"))
         + _diff_esterni(v["vincente"], v["perdente"], extra, esterni) for v in decise]
    giuste = 0
    esiti = []
    for i in range(len(Z)):
        m = addestra(Z[:i] + Z[i + 1:], nomi=nomi)
        esiti.append(probabilita(m, Z[i]) > 0.5)
        giuste += esiti[-1]
    lunga = sum(len(parole(piano(v["vincente"]))) > len(parole(piano(v["perdente"]))) for v in decise)
    pari_lungh = sum(len(parole(piano(v["vincente"]))) == len(parole(piano(v["perdente"]))) for v in decise)
    n = len(Z)
    basso, alto = cv.wilson(giuste, n)
    lb, la = cv.wilson(lunga, n)
    supera = basso > SOGLIA_WILSON and giuste > lunga
    return {"coppie": n, "pari_esclusi": len(voti) - n, "giuste": giuste,
            "accuratezza": giuste / n if n else 0.0, "wilson_95": [round(basso, 3), round(alto, 3)],
            "p_segno": binom_p(giuste, n), "piu_lunga": lunga, "piu_lunga_pari": pari_lungh,
            "piu_lunga_wilson_95": [round(lb, 3), round(la, 3)],
            "supera_soglia": supera, "spacy": nlp() is not None, "esiti": esiti,
            "n_tratti": len(nomi), "modello": addestra(Z, nomi=nomi) if Z else None}


def carica_voti(percorso: Path = VOTI) -> "list[dict]":
    return json.loads(percorso.read_text(encoding="utf-8"))["coppie"] if percorso.exists() else []


def modello_attuale(voti: "list[dict] | None" = None) -> dict:
    voti = carica_voti() if voti is None else voti
    decise = [v for v in voti if not v["pari"]]
    return addestra([differenza(v["vincente"], v["perdente"], v.get("originale")) for v in decise])


def rapporto(r: dict) -> str:
    righe = ["Modello di preferenza sui voti ciechi del DM (migliora_prosa.py modello)", "",
             f"coppie decise: {r['coppie']} (pari esclusi: {r['pari_esclusi']}) · spaCy: "
             + ("sì" if r["spacy"] else "no, livelli_max = 0"),
             f"leave-one-out: {r['giuste']} su {r['coppie']} = {r['accuratezza']:.3f} · "
             f"Wilson 95% {r['wilson_95']} · test del segno p = {r['p_segno']:.3f}",
             f"caso: 0.500 · «vince la più lunga»: {r['piu_lunga']} su {r['coppie']} = "
             f"{r['piu_lunga'] / max(1, r['coppie']):.3f} (pari di lunghezza {r['piu_lunga_pari']}), "
             f"Wilson 95% {r['piu_lunga_wilson_95']}",
             "", "soglia (SOGLIA.txt): Wilson basso > 0.50 e meglio della più lunga → "
             + ("SUPERATA: il modello è misura automatica" if r["supera_soglia"] else
                "NON superata: il modello ordina solo come suggerimento, il giudice resta il cieco"),
             "", "pesi su tutte le coppie (tratti divisi per lo scarto quadratico; + = la versione con più di questo tende a vincere):"]
    m = r["modello"]
    if m:
        for k, w in sorted(zip(m["tratti"], m["pesi"]), key=lambda x: -abs(x[1])):
            righe.append(f"  {k:22} {w:+.3f}")
    righe += ["", "⚠️ Le regole 1-4 di §2-ter vengono da questi stessi voti (giro 2 e riscrittura):",
              "i loro pesi sono letti sui dati che le hanno suggerite, e il leave-one-out non lo corregge."]
    return "\n".join(righe) + "\n"


# ── il dataset ───────────────────────────────────────────────────────────────
def _voci_scheda(testo: str) -> "dict[int, dict[int, tuple[str, str, str]]]":
    """Parte → coppia → (titolo, A, B) da una scheda cieca a più parti."""
    parti: dict = {}
    parte = 1
    for blocco in re.split(r"(?m)^## ", testo)[1:]:
        intest = blocco.split("\n", 1)[0]
        m = re.match(r"Parte (\d+)", intest)
        if m:
            parte = int(m.group(1))
            continue
        m = re.match(r"Coppia (\d+)", intest)
        if not m:
            continue
        titolo = re.search(r"(?m)^\*(.+)\*$", blocco)
        lati = re.split(r"(?m)^\*\*([AB])\*\*\s*$", blocco)
        testi = {lati[i]: lati[i + 1] for i in range(1, len(lati) - 1, 2)}

        def corpo(t):
            righe = [r[1:].strip() if r.startswith(">") else None for r in t.strip().splitlines()]
            out, par = [], []
            for r in righe:
                if r is None:
                    continue
                if r == "":
                    out.append(" ".join(par))
                    par = []
                else:
                    par.append(r)
            out.append(" ".join(par))
            return "\n\n".join(x for x in out if x)
        parti.setdefault(parte, {})[int(m.group(1))] = (
            titolo.group(1) if titolo else "", corpo(testi.get("A", "")), corpo(testi.get("B", "")))
    return parti


def _leggi_voti(testo: str) -> "dict[int, tuple[str, list[str]]]":
    out = {}
    for r in testo.splitlines():
        m = cv._VOTO.match(r)
        if m:
            out[int(m.group(1))] = (m.group(2).upper(), [w.strip(",;.").lower() for w in m.group(3).split() if w])
    return out


def coppie_da_scheda(scheda: str, chiave: dict, voti: str, fonte: str, parte: int,
                     originali: "dict[str, str]", vecchia: str, nuova: str) -> "list[dict]":
    """Le coppie votate di una parte di scheda, con la chiave di cieco_versioni."""
    testi = _voci_scheda(scheda).get(parte, {})
    vv = _leggi_voti(voti)
    out = []
    for c in chiave["coppie"]:
        if c["stato"] == "identica" or c["n"] not in vv or c["n"] not in testi:
            continue
        titolo, a, b = testi[c["n"]]
        voto, etichette = vv[c["n"]]
        t_nuova, t_vecchia = (a, b) if c["nuova"] == "A" else (b, a)
        if voto == "=":
            vinc, perd, rv, rp = t_nuova, t_vecchia, nuova, vecchia
        elif voto == c["nuova"]:
            vinc, perd, rv, rp = t_nuova, t_vecchia, nuova, vecchia
        else:
            vinc, perd, rv, rp = t_vecchia, t_nuova, vecchia, nuova
        bid = titolo.replace("Box ", "")
        out.append({"id": f"{fonte}-{parte}-{c['n']}", "fonte": fonte, "coppia": c["n"],
                    "titolo": titolo, "pari": voto == "=", "vincente": vinc, "perdente": perd,
                    "ruolo_vincente": rv, "ruolo_perdente": rp,
                    "etichette_sulla_perdente": [] if voto == "=" else etichette,
                    "originale": originali.get(bid)})
    return out


def dataset() -> "list[dict]":
    """Tutte le coppie votate alla cieca dal DM che il repo conserva."""
    coppie = []
    for r in json.loads((QUI / "COPPIE-VOTATE.json").read_text(encoding="utf-8")):
        coppie.append({"id": f"{r['set']}-{r['n']}", "fonte": FONTI_38[r["set"]], "coppia": r["n"],
                       "titolo": "", "pari": False, "vincente": r["win"], "perdente": r["lose"],
                       "ruolo_vincente": "nuova" if r["nuova_vince"] else "vecchia",
                       "ruolo_perdente": "vecchia" if r["nuova_vince"] else "nuova",
                       "etichette_sulla_perdente": [],
                       "originale": r["lose"] if r["nuova_vince"] else r["win"]})
    ris = QUI / "riscrittura"
    incr = json.loads((ris / "misure/INCROCIATA.json").read_text(encoding="utf-8"))
    originali = {b["id"]: mc.corpo_del_box(b["versioni"]["O"]["righe"]) for b in incr["box"]}
    scheda = (ris / "cieco/SCHEDA-CIECA.md").read_text(encoding="utf-8")
    for parte, nome, vecchia, nuova in ((1, "V-N", "V (catena vecchia)", "N (catena nuova)"),
                                        (2, "F-O", "O (originale)", "F (fusione)")):
        chiave = json.loads((ris / f"chiave/CHIAVE-{nome}.json").read_text(encoding="utf-8"))
        voti = (ris / f"cieco/VOTI-{parte}.txt").read_text(encoding="utf-8")
        coppie += coppie_da_scheda(scheda, chiave, voti, "riscrittura-2026-10-22", parte,
                                   originali, vecchia, nuova)
    # i voti della pipeline, se ce ne sono, restano
    coppie += [v for v in carica_voti() if v["fonte"].startswith("pipeline")]
    return coppie


def scrivi_voti(coppie: "list[dict]", percorso: Path = VOTI) -> None:
    percorso.parent.mkdir(parents=True, exist_ok=True)
    dati = {"_nota": "Le coppie votate alla cieca dal DM (ADR-0093). «vincente» e «perdente» "
                     "sono i testi; con «pari» vero sono solo le due versioni. «originale» è il "
                     "testo da cui partivano le riscritture, quando si conosce: le regole di "
                     "§2-ter si misurano rispetto a quello. Rigenera: migliora_prosa.py dataset.",
            "coppie": coppie}
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ── il filtro di non regressione ─────────────────────────────────────────────
def _come_box(testo: str, titolo: str = "Box") -> str:
    righe = [f"## {titolo}", ""]
    for i, par in enumerate(testo.strip().split("\n\n")):
        if i:
            righe.append(">")
        righe.append(f"> *{par.strip()}*")
    return "\n".join(righe) + "\n"


def filtra(originale: str, candidata: str, lt=None) -> "list[str]":
    """Perché la candidata è scartata: vuoto vuol dire che passa. `lt`, se c'è,
    conta i rilievi veri di LanguageTool di un testo per gruppo (`ControlloLT`):
    una candidata con più rilievi dell'originale in un gruppo affidabile si scarta."""
    motivi = [f"fatto cambiato, {x}" for x in cp.confronta_fatti(originale, candidata)]
    motivi += [f"box impoverito, {x}" for x in cp.box_impoveriti(_come_box(originale), _come_box(candidata))]
    d = mc.dettagli_sensoriali(piano(candidata)) - mc.dettagli_sensoriali(piano(originale))
    if d < 0 and not any(m.startswith("box impoverito") for m in motivi):
        motivi.append(f"regola 1, {-d} dettagli sensoriali in meno")
    if monologo_spezzato(originale, candidata):
        motivi.append("regola 2, monologo spezzato in battute")
    if frase_finale_tolta(originale, candidata):
        motivi.append("regola 3, frase finale tolta")
    if subordinata_spezzata(originale, candidata):
        motivi.append("regola 4, subordinata spezzata")
    if lt is not None:
        prima, dopo = lt.conti(originale), lt.conti(candidata)
        for g in sorted(dopo):
            if dopo[g] > prima.get(g, 0):
                motivi.append(f"LanguageTool, {dopo[g] - prima.get(g, 0)} rilievi di {g} in più")
    return motivi


def leggi_candidate(testo: str) -> "list[str]":
    """Le candidate di un file: una per sezione `## …`, in box (`> *…*`) o in chiaro."""
    testo = re.sub(r"<!--.*?-->", "", testo, flags=re.S)
    out = []
    for blocco in re.split(r"(?m)^##\s+.*$", testo)[1:]:
        righe = [r for r in blocco.strip().splitlines()]
        if not any(r.strip() for r in righe):
            continue
        if all(r.startswith(">") or not r.strip() for r in righe):
            pars, cur = [], []
            for r in righe:
                r2 = r.lstrip(">").strip()
                if r2:
                    cur.append(r2)
                elif cur:
                    pars.append(cur)
                    cur = []
            if cur:
                pars.append(cur)
            out.append("\n\n".join(mc.corpo_del_box(["> " + x for x in p]) for p in pars))
        else:
            out.append("\n\n".join(re.sub(r"\s+", " ", p).strip()
                                   for p in "\n".join(righe).strip().split("\n\n")))
    return out


def migliora(originale: str, candidate: "list[str]", modello: dict, lt=None) -> dict:
    voci = []
    for i, c in enumerate(candidate, 1):
        motivi = filtra(originale, c, lt)
        z = differenza(c, originale, originale)
        voci.append({"n": i, "testo": c, "scartata": motivi,
                     "punteggio": round(probabilita(modello, z), 3)})
    buone = [v for v in voci if not v["scartata"]]
    migliore = max(buone, key=lambda v: (v["punteggio"], -v["n"])) if buone else None
    # Dal 2026-10-23 il modello supera la soglia di SOGLIA.txt: se anche la
    # migliore perde contro l'originale, resta l'originale. Lo stesso giorno,
    # addestrato sui 55 voti di prima, aveva previsto 5 coppie nuove su 5, fra
    # cui l'unica che il DM ha dato all'originale (P05, 0,94 per l'originale).
    perde = migliore is not None and migliore["punteggio"] < 0.5
    return {"originale": originale, "candidate": voci,
            "vincitrice": None if perde or not migliore else migliore["n"],
            "punteggio": migliore["punteggio"] if migliore else None,
            "resta_originale": "la migliore perde contro l'originale" if perde else
                               ("nessuna candidata passa il filtro" if not migliore else None)}


# ── scegli: i box da migliorare ──────────────────────────────────────────────
def _chiave_testo(t: str) -> str:
    return re.sub(r"\s+", " ", piano(t)).strip()[:120]


def file_arc() -> "list[str]":
    arc08 = sorted(str(p.relative_to(ROOT)) for p in (ROOT / CARTELLA_ARC08).glob("*.md")
                   if not p.name.startswith("ERRATA-"))
    return ARC07 + arc08


def gia_usati() -> "set[str]":
    usati = set()
    if CONGELATI.exists():
        usati |= {_chiave_testo(c["testo"]) for c in json.loads(CONGELATI.read_text(encoding="utf-8"))}
    incr = QUI / "riscrittura/misure/INCROCIATA.json"
    if incr.exists():
        usati |= {_chiave_testo(mc.corpo_del_box(b["versioni"]["O"]["righe"]))
                  for b in json.loads(incr.read_text(encoding="utf-8"))["box"]}
    for v in carica_voti():
        usati |= {_chiave_testo(v["vincente"]), _chiave_testo(v["perdente"])}
    return usati


#: Una nota di regola che `_NOTA_DI_REGOLA` di cieco_versioni non vede: dadi,
#: punti ferita, caratteristiche («25d12+175», «I pf tornano», «For 31»).
_NOTA_DI_REGOLA_IN_PIU = re.compile(r"\d+d\d+|\bpf\b|\b(?:For|Des|Cos|Int|Sag|Car)\s+\d")


def scegli(seme: int, n: int) -> "list[dict]":
    usati = gia_usati()
    cand = []
    for f in file_arc():
        for i, b in enumerate(cv.box_con_titolo((ROOT / f).read_text(encoding="utf-8"))):
            if b["parole"] < cv.PAROLE_MINIME or cv._NOTA_DI_REGOLA.search(b["testo"]) \
                    or _NOTA_DI_REGOLA_IN_PIU.search(b["testo"]):
                continue
            if _chiave_testo(b["testo"]) in usati:
                continue
            cand.append({"file": f, "box": i, "titolo": b["titolo"], "parole": b["parole"],
                         "testo": b["testo"]})
    rng = random.Random(seme)
    return sorted(rng.sample(cand, min(n, len(cand))), key=lambda c: (c["file"], c["box"]))


# ── campione ed esito ────────────────────────────────────────────────────────
TESTA_SCHEDA = [
    "# Scheda cieca — la pipeline migliora_prosa contro l'originale", "",
    "Per ogni coppia leggi ad alta voce **A** e poi **B**, e scrivi una riga nel file dei voti",
    "(`VOTI.txt`): `N A`, `N B` o `N =`. Dopo la lettera, se vuoi, le etichette di ciò che",
    "non andava nella versione scartata (anche più d'una):", ""]


def campione(scelte: dict, seme: int) -> "tuple[str, dict]":
    """La vincitrice di ogni box contro l'originale, con cieco_versioni.coppie.
    Tutte le coppie vanno al DM: la misura non ne decide nessuna."""
    rel = "plans/esperimenti/qualita-misurabile-2026-10-22/pipeline/cieco/_testi-provvisori.md"
    tmp = ROOT / rel
    tmp.parent.mkdir(parents=True, exist_ok=True)
    voci, md = [], ["# testi", ""]
    for s in scelte["box"]:
        if s.get("vincitrice") is None:
            continue
        titolo = f"Box {s['id']}"
        nuovo = next(c["testo"] for c in s["candidate"] if c["n"] == s["vincitrice"])
        voci.append({"file": rel, "indice": len(voci), "titolo": titolo,
                     "testo": s["originale"], "parole": len(s["originale"].split())})
        md += [_come_box(nuovo, titolo)]
    tmp.write_text("\n".join(md) + "\n", encoding="utf-8")
    vecchio = cv.CONTROLLI
    cv.CONTROLLI = 10 ** 6
    try:
        scheda, chiave = cv.coppie({"ref": "", "seme": seme, "per_file": len(voci),
                                    "parole_minime": cv.PAROLE_MINIME, "voci": voci}, "", seme)
    finally:
        cv.CONTROLLI = vecchio
        tmp.unlink()
    chiave["confronto"] = {"vecchia": "originale", "nuova": "vincitrice della pipeline"}
    corpo = [r for r in scheda.splitlines()
             if not r.startswith(("# Confronto cieco", "Leggi ad alta voce", "Se vuoi, dopo la lettera"))]
    corpo = [re.sub(r"^\*_testi-provvisori\.md · (Box \S+)\*$", r"*\1*", r) for r in corpo]
    testa = TESTA_SCHEDA + [f"- `{k}`: {v}" for k, v in cv.ETICHETTE.items()] + [
        "", "Esempio: `3 B goffo ritmo`. Non aprire la cartella `chiave/` prima di aver votato.", ""]
    testo = "\n".join(testa + corpo)
    return re.sub(r"\n{3,}", "\n\n", testo).strip() + "\n", chiave


def registra_esito(scelte: dict, chiave: dict, voti_testo: str, data: str) -> "tuple[dict, list[dict]]":
    r = cv.esito(chiave, voti_testo)
    vv = _leggi_voti(voti_testo)
    per_titolo = {f"Box {s['id']}": s for s in scelte["box"]}
    nuove = []
    for c in chiave["coppie"]:
        if c["stato"] == "identica" or c["n"] not in vv:
            continue
        s = per_titolo[c["titolo"]]
        voto, etichette = vv[c["n"]]
        nuovo = next(x["testo"] for x in s["candidate"] if x["n"] == s["vincitrice"])
        vince_nuova = voto == c["nuova"]
        vinc, perd = (nuovo, s["originale"]) if voto == "=" or vince_nuova else (s["originale"], nuovo)
        nuove.append({"id": f"pipeline-{data}-{chiave['seme']}-{c['n']}",
                      "fonte": f"pipeline-{data}", "coppia": c["n"], "titolo": f"{s['file']} · {s['titolo']}",
                      "pari": voto == "=", "vincente": vinc, "perdente": perd,
                      "ruolo_vincente": "pipeline" if voto == "=" or vince_nuova else "originale",
                      "ruolo_perdente": "originale" if voto == "=" or vince_nuova else "pipeline",
                      "etichette_sulla_perdente": [] if voto == "=" else etichette,
                      "originale": s["originale"]})
    return r, nuove


# ── i tratti esterni e le varianti del modello ───────────────────────────────
ESTERNI = PIPE / "tratti-esterni.json"
LT_DIR = QUI / "languagetool"
#: Le varianti di languagetool/SOGLIA.txt, scritte prima del leave-one-out.
TRATTI_LT = ("lt_refusi", "lt_altri")
TRATTI_PPL = ("nll_token", "token_per_parola")
TRATTI_STANZA = ("stanza_agg_complesso", "stanza_calchi", "stanza_frasi_oltre2%", "stanza_livelli_max",
                 "stanza_lungh_dip", "stanza_mattr_lemmi", "stanza_possessivi_corpo",
                 "stanza_profondita_max", "stanza_profondita_media", "stanza_pron_soggetto",
                 "stanza_rip_interna%", "stanza_sogg_preverbale", "stanza_stare_gerundio")
VARIANTI = (("base", ()), ("+LT", TRATTI_LT), ("+ppl", TRATTI_PPL), ("+Stanza", TRATTI_STANZA),
            ("+tutto", TRATTI_LT + TRATTI_PPL + TRATTI_STANZA))
#: McNemar contro il base: Bonferroni sulle quattro varianti.
ALFA_VARIANTI = 0.05 / 4


def chiave_esterni(testo: str) -> str:
    return re.sub(r"\s+", " ", piano(testo)).strip()


def carica_esterni(percorsi: "list[Path | str]", voti: "list[dict]") -> dict:
    """Testo → tratti esterni. I file hanno la forma `{id: {vincente: {...},
    perdente: {...}}}` sulle coppie di VOTI.json (tratti-esterni.json dell'altro
    thread, TRATTI-LT.json di `languagetool`). Un id che VOTI.json non ha si
    ignora; da `token` si ricava `token_per_parola`, da `ppl` `nll_token` se manca."""
    out: dict = {}
    for percorso in percorsi:
        _unisci_esterni(json.loads(Path(percorso).read_text(encoding="utf-8")), voti, out)
    return out


def _unisci_esterni(dati: dict, voti: "list[dict]", out: dict) -> dict:
    per_id = {v["id"]: v for v in voti}
    for i, lati in dati.items():
        if i.startswith("_") or i not in per_id:
            continue
        for ruolo in ("vincente", "perdente"):
            if ruolo not in lati:
                continue
            testo = per_id[i][ruolo]
            t = {k: float(v) for k, v in lati[ruolo].items() if isinstance(v, (int, float))}
            if "token" in t:
                t["token_per_parola"] = t["token"] / max(1, len(parole(piano(testo))))
            if "ppl" in t and "nll_token" not in t:
                t["nll_token"] = math.log(t["ppl"])
            out.setdefault(chiave_esterni(testo), {}).update(t)
    return out


def residuo_ppl(voti: "list[dict]", esterni: dict) -> str:
    """La perplessità a lunghezza controllata: retta per l'origine fra le
    differenze di nll_token e di log(token), e test del segno sul residuo."""
    dn, dl = [], []
    for v in voti:
        a, b = esterni.get(chiave_esterni(v["vincente"]), {}), esterni.get(chiave_esterni(v["perdente"]), {})
        if v["pari"] or not all(k in a and k in b for k in ("nll_token", "token")):
            continue
        dn.append(a["nll_token"] - b["nll_token"])
        dl.append(math.log(a["token"]) - math.log(b["token"]))
    if not dn:
        return ""
    pend = sum(x * y for x, y in zip(dl, dn)) / (sum(x * x for x in dl) or 1.0)
    res = [y - pend * x for x, y in zip(dl, dn)]
    meno, piu = sum(r < 0 for r in res), sum(r > 0 for r in res)
    grezzo = sum(y < 0 for y in dn)
    return (f"perplessità e lunghezza: nll_token più bassa nella vincente {grezzo} su {len(dn)} "
            f"(p {binom_p(grezzo, len(dn)):.3f}); tolta la lunghezza (pendenza {pend:+.3f} su log token) "
            f"{meno} contro {piu} (p {binom_p(meno, meno + piu):.3f})\n")


def mcnemar_p(a: "list[bool]", b: "list[bool]") -> "tuple[int, int, float]":
    """McNemar esatto: (solo a giusta, solo b giusta, p a due code)."""
    solo_a = sum(x and not y for x, y in zip(a, b))
    solo_b = sum(y and not x for x, y in zip(a, b))
    return solo_a, solo_b, binom_p(solo_b, solo_a + solo_b)


def confronta_varianti(voti: "list[dict]", esterni: dict) -> "list[dict]":
    """Il leave-one-out di ogni variante sulle stesse coppie, e McNemar contro il base.
    Una variante i cui tratti mancano del tutto si salta."""
    presenti = {k for t in esterni.values() for k in t}
    out, base = [], None
    for nome, extra in VARIANTI:
        mancano = [k for k in extra if k not in presenti]
        if mancano:
            out.append({"variante": nome, "saltata": f"mancano {', '.join(mancano)}"})
            continue
        r = valida(voti, extra, esterni)
        voce = {"variante": nome, "n_tratti": r["n_tratti"], "giuste": r["giuste"], "coppie": r["coppie"],
                "accuratezza": r["accuratezza"], "wilson_95": r["wilson_95"], "esiti": r["esiti"],
                "modello": r["modello"]}
        if base is None:
            base = r["esiti"]
        else:
            sb, sv, pm = mcnemar_p(base, r["esiti"])
            voce.update({"solo_base": sb, "solo_variante": sv, "p_mcnemar": pm,
                         "migliora": pm < ALFA_VARIANTI and sv > sb and r["wilson_95"][0] > SOGLIA_WILSON})
        out.append(voce)
    return out


def rapporto_varianti(righe: "list[dict]") -> str:
    t = ["Varianti del modello (languagetool/SOGLIA.txt): leave-one-out sulle stesse coppie,",
         f"McNemar esatto contro il base, soglia p < {ALFA_VARIANTI:.4f} (Bonferroni su 4) e Wilson basso > 0,50", "",
         f"  {'variante':9} {'tratti':>6} {'giuste':>7} {'acc.':>6}  {'Wilson 95%':15} {'solo base':>9} "
         f"{'solo var.':>9} {'p McNemar':>9}  migliora"]
    for r in righe:
        if "saltata" in r:
            t.append(f"  {r['variante']:9} saltata: {r['saltata']}")
            continue
        w = f"[{r['wilson_95'][0]:.3f}, {r['wilson_95'][1]:.3f}]"
        coda = (f"{r['solo_base']:>9} {r['solo_variante']:>9} {r['p_mcnemar']:>9.3f}  "
                + ("sì" if r["migliora"] else "no")) if "p_mcnemar" in r else f"{'':>9} {'':>9} {'':>9}  (riferimento)"
        t.append(f"  {r['variante']:9} {r['n_tratti']:>6} {r['giuste']:>3}/{r['coppie']:<3} "
                 f"{r['accuratezza']:>6.3f}  {w:15} {coda}")
    for r in righe:
        if "saltata" in r or r["variante"] == "base":
            continue
        pesi = [(k, w) for k, w in zip(r["modello"]["tratti"], r["modello"]["pesi"]) if k not in TRATTI]
        t.append(f"  pesi dei tratti nuovi in {r['variante']}: "
                 + ", ".join(f"{k} {w:+.3f}" for k, w in sorted(pesi, key=lambda x: -abs(x[1]))))
    return "\n".join(t) + "\n"


# ── LanguageTool, facoltativo (server HTTP locale) ───────────────────────────
#: Avvio: `scripts/avvia_languagetool.sh` (lo stesso server del secondo lettore
#: di `ciclo_prosa`, ADR-0079, sulla porta 8081). La variabile LANGUAGETOOL_URL
#: cambia l'indirizzo.
LT_URL = os.environ.get("LANGUAGETOOL_URL", "http://localhost:8081")
GLOSSARIO = ROOT / "campaign/GLOSSARIO-E-LOCALIZZAZIONE.md"
GRUPPI_LT = ("refusi", "grammatica", "stile", "ripetizioni", "punteggiatura")
#: Le categorie di LanguageTool (generali e di grammar.xml italiano) nei cinque gruppi.
_CATEGORIE_LT = {
    "TYPOS": "refusi", "CASING": "grammatica", "GRAMMAR": "grammatica", "CONFUSED_WORDS": "grammatica",
    "SEMANTICS": "grammatica", "CAT1": "grammatica", "CAT2": "grammatica", "CAT3": "grammatica",
    "CAT4": "grammatica", "CAT5": "grammatica", "CAT7": "grammatica", "CAT12": "grammatica",
    "CAT13": "refusi", "PUNCTUATION": "punteggiatura", "TYPOGRAPHY": "punteggiatura",
    "CAT6": "punteggiatura", "STYLE": "stile", "REDUNDANCY": "stile", "CAT8": "stile", "CAT9": "stile",
    "CAT10": "stile", "CAT11": "stile", "REPETITIONS": "ripetizioni", "REPETITIONS_STYLE": "ripetizioni"}
#: La sonda di richiamo: frasi con un errore voluto (scritte qui, nessun testo di terzi).
SONDA_LT = (("Le ragazza sono andate a casa.", "accordo"), ("Io ho andato al mare ieri.", "ausiliare"),
            ("Perchè non vieni con noi?", "accento"), ("Lui disse che e bello.", "e/è"),
            ("Una amico mio è arrivato.", "articolo"), ("Se lo sapevo, venivo.", "periodo ipotetico"),
            ("Gli ho detto a lei di venire.", "pronome doppio"), ("Un'albero alto cresce lì.", "apostrofo"),
            ("Qual'è la strada giusta?", "apostrofo"), ("Il nano prende la ascia.", "elisione"),
            ("Sono andato a casa a casa.", "ripetizione"), ("C'è ne sono tre.", "ce/c'è"),
            ("Ci sono stati molte battaglie.", "accordo"), ("I nani è arrivati.", "accordo"),
            ("La spada di il re.", "preposizione"), ("Si è rotto la spada.", "accordo"),
            ("Fa freddo,, molto freddo.", "punteggiatura"), ("Va bene ,disse il nano.", "spazio"),
            ("Dopo di chè partirono.", "accento"), ("Il re ha detto che verrà domani, domani.", "ripetizione"))
#: Una soglia di precisione per gruppo, e i rilievi letti che servono per fidarsene.
PRECISIONE_MINIMA = 0.7
LETTI_MINIMI = 5


def lt_gruppo(regola: str, categoria: str) -> str:
    if "REPEAT" in regola or "REPETITION" in regola:
        return "ripetizioni"
    return _CATEGORIE_LT.get(categoria, "stile")


def _apri(url: str, dati: "bytes | None" = None, timeout: float = 60):
    senza_proxy = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return senza_proxy.open(urllib.request.Request(url, data=dati), timeout=timeout)


def lt_versione(url: str = LT_URL) -> "str | None":
    """La versione del server, o None se non risponde."""
    try:
        dati = urllib.parse.urlencode({"text": "Prova.", "language": "it"}).encode()
        return json.load(_apri(url.rstrip("/") + "/v2/check", dati, timeout=5))["software"]["version"]
    except Exception:
        return None


def lt_controlla(testo: str, url: str = LT_URL) -> "list[dict]":
    """I rilievi grezzi del server, semplificati."""
    dati = urllib.parse.urlencode({"text": testo, "language": "it"}).encode()
    out = []
    for m in json.load(_apri(url.rstrip("/") + "/v2/check", dati))["matches"]:
        regola, cat = m["rule"]["id"], m["rule"]["category"]["id"]
        out.append({"regola": regola, "categoria": cat, "gruppo": lt_gruppo(regola, cat),
                    "parola": testo[m["offset"]:m["offset"] + m["length"]], "offset": m["offset"],
                    "messaggio": m["message"],
                    "contesto": testo[max(0, m["offset"] - 50):m["offset"] + m["length"] + 50]})
    return out


_DIZIONARIO: "set[str] | None" = None


def _radice(parola: str) -> str:
    """nanico, nanica, nanici, naniche → nanic: il dizionario copre le flessioni."""
    w = parola.lower().strip("'’")
    return re.sub(r"h?[aeiou]$", "", w) if len(w) > 4 else w


def dizionario_nomi(glossario: Path = GLOSSARIO) -> "set[str]":
    """Le parole che non sono refusi: il registro dei nomi di misura_craft
    (Bestiario e state.md) più le prime due colonne delle tabelle del glossario."""
    global _DIZIONARIO
    if _DIZIONARIO is None:
        voci = {w.lower() for w in mc._registro_dei_nomi()}
        if glossario.exists():
            for r in glossario.read_text(encoding="utf-8").splitlines():
                if r.startswith("|") and not re.match(r"^\|[-\s|:]+\|?$", r):
                    for cella in r.strip().strip("|").split("|")[:2]:
                        voci |= {w.lower() for w in re.findall(r"[A-Za-zÀ-ÿ'-]+", re.sub(r"[*_`]", "", cella))
                                 if len(w) > 2}
        _DIZIONARIO = voci | {_radice(w) for w in voci}
    return _DIZIONARIO


def nome_noto(parola: str, diz: "set[str] | None" = None) -> bool:
    diz = dizionario_nomi() if diz is None else diz
    pezzi = [p for p in re.split(r"[-\s]", parola) if p]
    return bool(pezzi) and all(p.lower() in diz or _radice(p) in diz for p in pezzi)


def conta_rilievi(rilievi: "list[dict]", diz: "set[str] | None" = None) -> "dict[str, int]":
    """Rilievi per gruppo; `refusi` senza le parole del dizionario, `refusi_grezzi` con."""
    c = {g: 0 for g in GRUPPI_LT}
    c["refusi_grezzi"] = 0
    for r in rilievi:
        if r["gruppo"] == "refusi":
            c["refusi_grezzi"] += 1
            if nome_noto(r["parola"], diz):
                continue
        c[r["gruppo"]] += 1
    return c


def precisione(letti: "list[dict]") -> "dict[str, dict]":
    """Precisione per gruppo dai rilievi letti a mano (campo `vero`). Per i
    refusi conta solo quelli che il dizionario dei nomi non spiega: sono quelli
    che il filtro userebbe."""
    out: dict = {}
    for r in letti:
        if r.get("vero") is None or (r["gruppo"] == "refusi" and r.get("nome_noto")):
            continue
        d = out.setdefault(r["gruppo"], {"veri": 0, "letti": 0})
        d["letti"] += 1
        d["veri"] += bool(r["vero"])
    for d in out.values():
        d["precisione"] = d["veri"] / d["letti"]
    return out


def gruppi_affidabili(prec: "dict[str, dict]") -> "set[str]":
    return {g for g, d in prec.items() if g in GRUPPI_LT and d["letti"] >= LETTI_MINIMI
            and d["precisione"] >= PRECISIONE_MINIMA}


class ControlloLT:
    """Il filtro: conta solo i gruppi affidabili, con una cache per testo."""

    def __init__(self, url: str, gruppi: "set[str]"):
        self.url, self.gruppi, self._cache = url, set(gruppi), {}

    def conti(self, testo: str) -> "dict[str, int]":
        if testo not in self._cache:
            self._cache[testo] = conta_rilievi(lt_controlla(piano(testo), self.url))
        return {g: n for g, n in self._cache[testo].items() if g in self.gruppi}


def controllo_lt(url: str, percorso: Path = LT_DIR / "PRECISIONE.json") -> "ControlloLT | None":
    """Il filtro LT se il server risponde e qualche gruppo è affidabile; se no None e un messaggio."""
    if lt_versione(url) is None:
        print(f"LanguageTool non risponde su {url}: il filtro LT si salta.", file=sys.stderr)
        return None
    letti = json.loads(percorso.read_text(encoding="utf-8"))["rilievi"] if percorso.exists() else []
    gruppi = gruppi_affidabili(precisione(letti))
    if not gruppi:
        print("LanguageTool: nessun gruppo ha precisione letta >= 0,70, il filtro LT non scarta nulla.",
              file=sys.stderr)
    return ControlloLT(url, gruppi)


def testi_dei_box() -> "list[dict]":
    """I box read-aloud di ARC-07 e ARC-08, con misura_craft.box_read_aloud."""
    out = []
    for f in file_arc():
        for i, b in enumerate(mc.box_read_aloud((ROOT / f).read_text(encoding="utf-8"))):
            out.append({"file": f, "box": i, "testo": mc.corpo_del_box(b)})
    return out


def campione_rilievi(rilievi_box: "list[dict]", n: int, seme: int, diz=None) -> "list[dict]":
    """Il campione da leggere a mano: tutti i rilievi che non sono refusi, e il
    resto fino a `n` fra i refusi che il dizionario non spiega (quelli che il
    filtro userebbe), estratti con il seme."""
    altri = [r for r in rilievi_box if r["gruppo"] != "refusi"]
    refusi = [r for r in rilievi_box if r["gruppo"] == "refusi" and not nome_noto(r["parola"], diz)]
    scelti = altri[:n] + random.Random(seme).sample(refusi, max(0, min(len(refusi), n - len(altri))))
    return [{**r, "nome_noto": r["gruppo"] == "refusi" and nome_noto(r["parola"], diz),
             "vero": None, "nota": ""} for r in scelti]


def segno_per_gruppo(voti: "list[dict]", conti: "dict[str, dict]") -> "list[dict]":
    """Calibrazione: per ogni gruppo, la vincente ha meno rilievi della perdente?
    Test del segno sulle coppie non pari nel conto, Bonferroni sui gruppi."""
    gruppi = list(GRUPPI_LT) + ["refusi_grezzi"]
    out = []
    for g in gruppi:
        meno = piu = 0
        for v in voti:
            if v["pari"]:
                continue
            a, b = conti[chiave_esterni(v["vincente"])][g], conti[chiave_esterni(v["perdente"])][g]
            meno += a < b
            piu += a > b
        p = binom_p(meno, meno + piu)
        out.append({"gruppo": g, "vincente_meno": meno, "vincente_piu": piu,
                    "p": p, "p_bonferroni": min(1.0, p * len(gruppi))})
    return out


def misura_lt(url: str, voti: "list[dict]", letti: "list[dict]", esterni_altri: dict) -> "tuple[str, dict]":
    """Tutto il giro: rilievi su VOTI.json e sui box, precisione, calibrazione,
    varianti del modello. Restituisce il testo di MISURE.txt e TRATTI-LT.json."""
    versione = lt_versione(url)
    diz = dizionario_nomi()
    t0 = time.time()
    conti, rilievi_voti = {}, []
    for v in voti:
        for ruolo in ("vincente", "perdente"):
            k = chiave_esterni(v[ruolo])
            if k not in conti:
                ril = lt_controlla(piano(v[ruolo]), url)
                rilievi_voti += ril
                conti[k] = conta_rilievi(ril, diz)
    t_voti = time.time() - t0
    t0 = time.time()
    box = testi_dei_box()
    rilievi_box = []
    for b in box:
        for r in lt_controlla(b["testo"], url):
            rilievi_box.append({"file": b["file"], "box": b["box"], **r})
    t_box = time.time() - t0
    tratti_lt = {"_nota": f"Rilievi di LanguageTool {versione} sulle coppie di VOTI.json "
                          "(migliora_prosa.py languagetool). lt_refusi: TYPOS senza le parole del "
                          "dizionario dei nomi; lt_altri: tutti gli altri gruppi."}
    for v in voti:
        tratti_lt[v["id"]] = {r: {"lt_refusi": conti[chiave_esterni(v[r])]["refusi"],
                                  "lt_altri": sum(conti[chiave_esterni(v[r])][g] for g in GRUPPI_LT
                                                  if g != "refusi")}
                              for r in ("vincente", "perdente")}
    esterni = {k: dict(t) for k, t in esterni_altri.items()}
    _unisci_esterni(tratti_lt, voti, esterni)

    def per_gruppo(rilievi):
        c = {g: 0 for g in GRUPPI_LT}
        c["refusi_grezzi"] = 0
        regole: dict = {}
        for r in rilievi:
            regole[(r["gruppo"], r["regola"])] = regole.get((r["gruppo"], r["regola"]), 0) + 1
            if r["gruppo"] == "refusi":
                c["refusi_grezzi"] += 1
                if nome_noto(r["parola"], diz):
                    continue
            c[r["gruppo"]] += 1
        return c, regole

    righe = [f"Misure di LanguageTool {versione} (migliora_prosa.py languagetool --scrivi)", "",
             f"testi: {len(conti)} versioni distinte delle {len(voti)} coppie di VOTI.json in {t_voti:.1f} s; "
             f"{len(box)} box di ARC-07 e ARC-08 in {t_box:.1f} s",
             f"dizionario dei nomi (registro di misura_craft + glossario): {len(diz)} voci con le radici", ""]
    for nome, ril in (("sulle coppie di VOTI.json", rilievi_voti), ("sui box di ARC-07 e ARC-08", rilievi_box)):
        c, regole = per_gruppo(ril)
        righe.append(f"rilievi {nome}: " + ", ".join(f"{g} {c[g]}" for g in ("refusi_grezzi",) + GRUPPI_LT)
                     + "  (refusi = grezzi meno le parole del dizionario)")
        for (g, r), n in sorted(regole.items(), key=lambda x: -x[1]):
            righe.append(f"  {g:13} {r:32} {n}")
        righe.append("")
    prec = precisione(letti)
    righe.append(f"precisione letta a mano (PRECISIONE.json, {sum(r.get('vero') is not None for r in letti)} rilievi "
                 f"sui box; soglia {PRECISIONE_MINIMA} su almeno {LETTI_MINIMI}):")
    for g, d in sorted(prec.items()):
        righe.append(f"  {g:14} {d['veri']} veri su {d['letti']} = {d['precisione']:.2f}")
    aff = gruppi_affidabili(prec)
    righe += [f"gruppi nel filtro: {', '.join(sorted(aff)) if aff else 'nessuno'}", "",
              "calibrazione sulle coppie decise (la vincente ha meno rilievi?), test del segno, Bonferroni su "
              f"{len(GRUPPI_LT) + 1}:"]
    for s in segno_per_gruppo(voti, conti):
        righe.append(f"  {s['gruppo']:14} vincente con meno {s['vincente_meno']:2}, con più {s['vincente_piu']:2} · "
                     f"p {s['p']:.3f} · corretto {s['p_bonferroni']:.3f}")
    trovate = [(f, t) for f, t in SONDA_LT if lt_controlla(f, url)]
    righe += ["", f"sonda di richiamo: {len(trovate)} su {len(SONDA_LT)} frasi con un errore voluto hanno almeno "
              "un rilievo; mancate:"]
    righe += [f"  {t:14} {f}" for f, t in SONDA_LT if (f, t) not in trovate]
    righe += ["", rapporto_varianti(confronta_varianti(voti, esterni)) + residuo_ppl(voti, esterni)]
    return "\n".join(righe), tratti_lt



# ── la riga di comando ───────────────────────────────────────────────────────
def _scrivi_json(percorso: str, dati) -> None:
    p = Path(percorso)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("dataset", help="raccoglie le coppie votate in pipeline/VOTI.json")
    m = sub.add_parser("modello", help="leave-one-out, caso e «vince la più lunga»")
    m.add_argument("--scrivi", action="store_true", help="scrive anche pipeline/MODELLO.txt")
    m.add_argument("--varianti", action="store_true",
                   help="confronta base, +LT, +ppl, +Stanza, +tutto (languagetool/SOGLIA.txt) con McNemar")
    m.add_argument("--tratti-esterni", action="append", default=[], metavar="FILE",
                   help="tratti per le coppie di VOTI.json ({id: {vincente, perdente}}); ripetibile")
    s = sub.add_parser("scegli", help="sceglie con un seme i box da migliorare")
    s.add_argument("--seme", type=int, required=True)
    s.add_argument("--n", type=int, default=6)
    s.add_argument("--uscita", required=True)
    g = sub.add_parser("migliora", help="filtra e ordina le candidate di un box")
    g.add_argument("file")
    g.add_argument("--box", type=int, help="l'indice del box (senza: li elenca)")
    g.add_argument("--candidate", help="file con una candidata per sezione `## …`")
    g.add_argument("--scelte", help="registra il risultato in questo JSON")
    g.add_argument("--id", help="l'identificativo del box nelle scelte (P01…)")
    g.add_argument("--lt", nargs="?", const=LT_URL, metavar="URL",
                   help="aggiunge al filtro i rilievi affidabili di LanguageTool (se il server non c'è, si salta)")
    lt = sub.add_parser("languagetool", help="rilievi di LanguageTool: conti, precisione, calibrazione, varianti")
    lt.add_argument("--url", default=LT_URL)
    lt.add_argument("--tratti-esterni", action="append", default=[], metavar="FILE",
                    help="altri tratti per le varianti (tratti-esterni.json)")
    lt.add_argument("--precisione", default=str(LT_DIR / "PRECISIONE.json"),
                    help="i rilievi letti a mano (campo vero)")
    lt.add_argument("--campione", type=int, metavar="N", help="scrive N rilievi dei box da leggere a mano")
    lt.add_argument("--seme", type=int, default=20261023)
    lt.add_argument("--uscita", help="con --campione: il file JSON del campione")
    lt.add_argument("--scrivi", action="store_true", help="scrive languagetool/MISURE.txt e TRATTI-LT.json")
    c = sub.add_parser("campione", help="scheda cieca: vincitrice contro originale")
    c.add_argument("--scelte", required=True)
    c.add_argument("--seme", type=int, required=True)
    c.add_argument("--scheda", required=True)
    c.add_argument("--chiave", required=True)
    e = sub.add_parser("esito", help="registra i voti, rifà il modello, dice quanto vince la pipeline")
    e.add_argument("--scelte", required=True)
    e.add_argument("--chiave", required=True)
    e.add_argument("--voti", required=True)
    e.add_argument("--data", default=datetime.date.today().isoformat())
    a = ap.parse_args(argv)

    if a.cmd == "dataset":
        coppie = dataset()
        scrivi_voti(coppie)
        per_fonte: dict = {}
        for v in coppie:
            per_fonte[v["fonte"]] = per_fonte.get(v["fonte"], 0) + 1
        print(f"{len(coppie)} coppie in {VOTI.relative_to(ROOT)} "
              f"({sum(v['pari'] for v in coppie)} pari): "
              + ", ".join(f"{k} {n}" for k, n in per_fonte.items()))
    elif a.cmd == "modello":
        voti = carica_voti()
        if a.varianti:
            esterni = carica_esterni(a.tratti_esterni, voti)
            print(rapporto_varianti(confronta_varianti(voti, esterni)) + residuo_ppl(voti, esterni), end="")
            return 0
        testo = rapporto(valida(voti))
        print(testo, end="")
        if a.scrivi:
            (PIPE / "MODELLO.txt").write_text(testo, encoding="utf-8")
    elif a.cmd == "languagetool":
        versione = lt_versione(a.url)
        if versione is None:
            print(f"LanguageTool non risponde su {a.url}: niente da misurare (languagetool/README.md dice "
                  "come avviarlo).")
            return 0
        voti = carica_voti()
        if a.campione:
            if not a.uscita:
                ap.error("--campione vuole --uscita")
            ril = [{"file": b["file"], "box": b["box"], **r} for b in testi_dei_box()
                   for r in lt_controlla(b["testo"], a.url)]
            c = campione_rilievi(ril, a.campione, a.seme)
            _scrivi_json(a.uscita, {"_nota": f"Campione di rilievi di LanguageTool {versione} sui box di "
                                    f"ARC-07 e ARC-08, seme {a.seme}: «vero» si scrive a mano.",
                                    "seme": a.seme, "rilievi": c})
            print(f"{len(c)} rilievi in {a.uscita}")
            return 0
        pp = Path(a.precisione)
        letti = json.loads(pp.read_text(encoding="utf-8"))["rilievi"] if pp.exists() else []
        testo, tratti_lt = misura_lt(a.url, voti, letti, carica_esterni(a.tratti_esterni, voti))
        print(testo, end="")
        if a.scrivi:
            LT_DIR.mkdir(parents=True, exist_ok=True)
            (LT_DIR / "MISURE.txt").write_text(testo, encoding="utf-8")
            _scrivi_json(str(LT_DIR / "TRATTI-LT.json"), tratti_lt)
    elif a.cmd == "scegli":
        scelti = scegli(a.seme, a.n)
        _scrivi_json(a.uscita, {"seme": a.seme, "criterio": "box di ARC-07 e ARC-08 con almeno "
                                f"{cv.PAROLE_MINIME} parole, non note di regola (né dadi, pf, caratteristiche), non congelati, non nel "
                                "campione della riscrittura, non già votati", "box": [
                                    {"id": f"P{i:02d}", **b} for i, b in enumerate(scelti, 1)]})
        for i, b in enumerate(scelti, 1):
            print(f"P{i:02d} {b['file']} box {b['box']} ({b['parole']} parole) · {b['titolo'][:50]}")
    elif a.cmd == "migliora":
        testo = Path(a.file).read_text(encoding="utf-8")
        boxes = cv.box_con_titolo(testo)
        if a.box is None:
            for i, b in enumerate(boxes):
                print(f"{i:3} {b['parole']:4} parole · {b['titolo'][:60]}")
            return 0
        if not a.candidate:
            ap.error("migliora --box vuole --candidate")
        originale = boxes[a.box]["testo"]
        candidate = leggi_candidate(Path(a.candidate).read_text(encoding="utf-8"))
        r = migliora(originale, candidate, modello_attuale(), controllo_lt(a.lt) if a.lt else None)
        for v in r["candidate"]:
            stato = "scartata: " + "; ".join(v["scartata"]) if v["scartata"] else "passa"
            print(f"candidata {v['n']} · P(batte l'originale) {v['punteggio']:.3f} · {stato}")
        if r["vincitrice"] is None:
            print(f"{r['resta_originale']}: resta l'originale")
        else:
            print(f"migliore: candidata {r['vincitrice']} (punteggio {r['punteggio']:.3f})")
            print(next(v["testo"] for v in r["candidate"] if v["n"] == r["vincitrice"]))
        if a.scelte:
            p = Path(a.scelte)
            dati = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"box": []}
            voce = {"id": a.id or f"P{len(dati['box']) + 1:02d}", "file": str(Path(a.file).resolve().relative_to(ROOT))
                    if Path(a.file).resolve().is_relative_to(ROOT) else a.file,
                    "box": a.box, "titolo": boxes[a.box]["titolo"], **r}
            dati["box"] = [b for b in dati["box"] if b["id"] != voce["id"]] + [voce]
            dati["box"].sort(key=lambda b: b["id"])
            _scrivi_json(a.scelte, dati)
    elif a.cmd == "campione":
        scelte = json.loads(Path(a.scelte).read_text(encoding="utf-8"))
        scheda, chiave = campione(scelte, a.seme)
        Path(a.scheda).parent.mkdir(parents=True, exist_ok=True)
        Path(a.scheda).write_text(scheda, encoding="utf-8")
        _scrivi_json(a.chiave, chiave)
        print(f"{len(chiave['coppie'])} coppie in {a.scheda}; chiave in {a.chiave} (fuori dal repo fino al voto)")
    else:
        scelte = json.loads(Path(a.scelte).read_text(encoding="utf-8"))
        chiave = json.loads(Path(a.chiave).read_text(encoding="utf-8"))
        r, nuove = registra_esito(scelte, chiave, Path(a.voti).read_text(encoding="utf-8"), a.data)
        ids = {v["id"] for v in nuove}
        tutte = [v for v in carica_voti() if v["id"] not in ids] + nuove
        scrivi_voti(tutte)
        print(f"{len(nuove)} coppie aggiunte a {VOTI.relative_to(ROOT)} ({len(tutte)} in tutto)")
        print(f"la pipeline vince {r['nuova']} · l'originale {r['vecchia']} · pari {r['pari']} "
              f"su {r['votate']} · Wilson 95% {r['wilson_95']} · soglia di cieco_versioni "
              f"{r['soglia']} su {r['votabili']}")
        print(r["verdetto"].replace("la nuova versione", "la pipeline"))
        print(rapporto(valida(tutte)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
