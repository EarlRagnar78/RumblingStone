#!/usr/bin/env python3
r"""misura_sintassi.py — i calchi sintattici e la complessità dei box read-aloud,
misurati con un parser a dipendenze (spaCy, facoltativo).

## Perché esiste

`RICERCA-QUALITA-MISURABILE-2026-10` §2-3: le diciassette misure senza parser
non prevedevano il voto cieco del DM, e i calchi sintattici di Cerruti (il
soggetto preverbale con informazione nuova, l'aggettivo complesso anteposto)
non si vedono con una regex. Servivano un'analisi a dipendenze e un lemmatizzatore.
Questo script li porta, **come misura e non come cancello**: la calibrazione sui
voti del DM sta in
`plans/esperimenti/qualita-misurabile-2026-10-22/sintassi/CALIBRAZIONE-SINTASSI.txt`.

## Cosa misura, box per box

| Misura | Cosa conta | Fonte |
|---|---|---|
| `sogg_preverbale` | soggetto indefinito (o nudo) **prima** di un verbo inaccusativo o presentativo: «un campanello suonò» invece di «suonò un campanello» | Cerruti, anglicismi sintattici |
| `agg_complesso` | aggettivo anteposto al nome **con un modificatore** o un coordinato («una molto antica e silenziosa pietra») | Cerruti; `italiano-nativo.md` §1 |
| `stare_gerundio` | «stare + gerundio» in ogni tempo (la regex di `validate_prosa` vede solo il presente) | `italiano-nativo.md` §1 |
| `pron_soggetto` | pronome soggetto espresso dove il verbo basta (pro-drop); esclusi focus («anche lui»), coordinati, posposti, congiuntivo | `italiano-nativo.md` §1 |
| `possessivi_corpo` | **non è una misura nuova**: la regex di `validate_prosa.CALCHI_READ_ALOUD`, riusata e riportata a parte, fuori dal totale dei calchi | `validate_prosa.py` |
| `profondita_max` | il cammino più lungo dalla radice a una foglia, nella frase peggiore | Profiling-UD, READ-IT |
| `livelli_max` | catena più lunga di subordinate incassate (advcl, ccomp, csubj, relative, acl finite) | Profiling-UD |
| `frasi_oltre2%` | quota di frasi con **più di due** livelli di subordinate | `read-aloud-adulti.md` §1.2 |
| `lungh_dip` | distanza media fra una parola e la sua testa | Profiling-UD |
| `mattr_lemmi` | MATTR (finestra 25) sui lemmi | McCarthy e Jarvis 2010 |
| `rip_interna%` | parole di contenuto il cui lemma è già comparso nello stesso box | alla TAACO |
| `rip_fra_box%` | lemmi di contenuto del box che tornano in **un altro** box dello stesso file (ripetizione a distanza); si calcola per file | alla TAACO |

⚠️ **Ogni rilievo è un indizio.** Il parser sbaglia, e un soggetto preverbale
può essere una scelta (tema già noto, enfasi). Precisione letta a mano su 15
rilievi della base ARC-07/ARC-08 (README della cartella `sintassi/`): soggetto
preverbale 5 su 5, stare + gerundio 2 su 2, pronome soggetto **0 su 8**.
Per questo il totale `calchi` somma solo le prime tre righe della tabella;
`pron_soggetto` si riporta a parte e non va usato come difetto.

## Senza spaCy

Lo script parte comunque: dice che la misura è saltata ed esce 0. spaCy è MIT;
il modello `it_core_news_md` è **CC BY-NC-SA 3.0**: va bene per l'uso non
commerciale del repo, e **non entra nel repo** (si installa a parte con
`python -m spacy download it_core_news_md`).

    python3 scripts/misura_sintassi.py                         # ARC-07 DEF e ARC-08 principali
    python3 scripts/misura_sintassi.py --file X.md --per-box   # un file, box per box
    python3 scripts/misura_sintassi.py --json > base.json

Exit: 0 ok (anche senza spaCy), 2 file assente.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import misura_craft as mc  # noqa: E402
from validate_prosa import CALCHI_READ_ALOUD  # noqa: E402

MODELLO = "it_core_news_md"

#: La regex dei possessivi su parti del corpo è quella di validate_prosa:
#: riusata, non riscritta, e riportata fuori dal totale dei calchi.
POSSESSIVI_CORPO = re.compile(CALCHI_READ_ALOUD[0][0], re.I)

#: Verbi inaccusativi e presentativi (comparsa, moto, evento, suono, luce):
#: con questi il soggetto nuovo in italiano va **dopo** il verbo.
INACCUSATIVI = set("""
apparire comparire scomparire sparire arrivare giungere entrare uscire nascere
morire cadere crollare scendere salire sorgere emergere spuntare affiorare
irrompere venire tornare passare partire restare rimanere mancare accadere
succedere capitare iniziare cominciare finire cessare crescere esplodere
scoppiare suonare risuonare echeggiare rimbombare brillare balenare lampeggiare
guizzare scintillare tremare pendere giacere esistere bastare servire seguire
avanzare sbucare piovere colare gocciolare filtrare scorrere soffiare
""".split())

#: Il lemmatizzatore del modello md sbaglia molti passati remoti irregolari
#: («apparve» → «apparve»): le forme si riconoscono anche dalla superficie.
FORME_INACCUSATIVE = set("""
apparve apparvero comparve comparvero scomparve sparve giunse giunsero nacque
nacquero cadde caddero scese scesero salì salirono sorse sorsero emerse emersero
irruppe irruppero venne vennero rimase rimasero accadde successe crebbe
crebbero esplose esplosero uscì uscirono entrò entrarono morì morirono
""".split())

#: Con «si» anticausativo: «una porta si apre» → «si apre una porta».
ANTICAUSATIVI_SI = set("""
aprire chiudere accendere spegnere alzare levare spalancare diffondere
propagare sollevare staccare rompere spezzare formare aprirsi
""".split())

PRON_SOGGETTO = {"io", "tu", "lui", "lei", "egli", "ella", "noi", "voi",
                 "essi", "esse", "esso", "essa", "loro"}
FOCUS = {"anche", "neanche", "nemmeno", "neppure", "solo", "soltanto", "pure",
         "proprio", "persino", "perfino", "almeno"}
MODIF_AMMESSI = {"più", "meno"}   # «la più antica pietra» è italiano
SUBORDINATE = {"advcl", "ccomp", "csubj", "acl:relcl"}
CONTENUTO = {"NOUN", "VERB", "ADJ", "ADV"}
STARE = {"sto", "stai", "sta", "stiamo", "state", "stanno", "stavo", "stavi",
         "stava", "stavamo", "stavate", "stavano", "stetti", "stette", "starò",
         "starà", "starai", "staranno", "stia", "stessi", "stesse"}

#: I rilievi che entrano nel totale `calchi`. `pron_soggetto` resta fuori:
#: letto a mano sulla base ARC-07/ARC-08 ha dato 0 veri su 8 (contrasto,
#: ri-ancoraggio del soggetto, anafora retorica nei discorsi: tutti usi giusti).
CALCHI = ("sogg_preverbale", "agg_complesso", "stare_gerundio")

#: I file della base di partenza (ARC-07 definitivi, ARC-08 con read-aloud,
#: fuori _ARCHIVIO e Mappe).
BASE = [
    "07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md",
    "07_il Portale Della Forgia Eterna/ARC07-DEF-2-RITORNO-E-AFFRESCHI.md",
    "07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md",
    "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md",
    "07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md",
    "08_La Battaglia Di Hammerfist/ARC08-01-GUIDA-DM.md",
    "08_La Battaglia Di Hammerfist/ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md",
    "08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md",
    "08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md",
    "08_La Battaglia Di Hammerfist/ARC08-17-BANCO-HAMMERFIST-1372.md",
    "08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md",
    "08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md",
    "08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md",
]

_NLP = None


def carica_nlp():
    """Il modello spaCy, o None se spaCy o il modello mancano."""
    global _NLP
    if _NLP is None:
        try:
            import spacy
            _NLP = spacy.load(MODELLO, exclude=["ner"])
        except Exception:  # ImportError, OSError (modello assente)
            _NLP = False
    return _NLP or None


# ---------------------------------------------------------------- i calchi

def _definito_ind(nome) -> bool:
    """Il sintagma porta informazione nuova: articolo indeterminativo,
    partitivo, numerale, o nome nudo."""
    if nome.pos_ != "NOUN":
        return False
    det = [c for c in nome.children if c.dep_ == "det"]
    if not det:
        # nome nudo («polvere cade dal soffitto») o con numerale («tre nani arrivano»)
        return not any(c.dep_ in ("nmod:poss", "det:poss") for c in nome.children)
    for d in det:
        if "Ind" in d.morph.get("Definite") or d.lemma_.lower() in ("qualche", "alcuno", "certo"):
            return True
    return False


def _inaccusativo(verbo) -> bool:
    lem, txt = verbo.lemma_.lower(), verbo.text.lower()
    if lem in INACCUSATIVI or txt in FORME_INACCUSATIVE:
        return True
    si = any(c.dep_.startswith("expl") and c.text.lower() in ("si", "s'") for c in verbo.children)
    return si and lem in ANTICAUSATIVI_SI


def sogg_preverbale(doc) -> list:
    out = []
    for t in doc:
        if t.dep_ != "nsubj" or t.i >= t.head.i:
            continue
        v = t.head
        if v.pos_ not in ("VERB",) or "Part" in v.morph.get("VerbForm"):
            continue
        if any(c.dep_ in ("aux:pass", "expl:pass") for c in v.children):
            continue
        if _definito_ind(t) and _inaccusativo(v):
            out.append(doc[t.left_edge.i: v.i + 1].text)
    return out


def agg_complesso(doc) -> list:
    out = []
    for t in doc:
        if t.dep_ != "amod" or t.pos_ != "ADJ" or t.head.pos_ != "NOUN" or t.i >= t.head.i:
            continue
        pesanti = [c for c in t.children
                   if c.dep_ in ("obl", "conj", "nmod", "advcl", "xcomp", "ccomp")
                   or (c.dep_ == "advmod" and c.lemma_.lower() not in MODIF_AMMESSI
                       and c.i < t.i)]
        if pesanti:
            out.append(doc[t.left_edge.i: t.head.i + 1].text)
    return out


def stare_gerundio(doc) -> list:
    out = []
    for t in doc:
        if "Ger" not in t.morph.get("VerbForm"):
            continue
        for c in t.children:
            if c.dep_ == "aux" and (c.lemma_.lower() == "stare" or c.text.lower() in STARE):
                out.append(doc[c.i: t.i + 1].text)
    return out


def pron_soggetto(doc) -> list:
    out = []
    for t in doc:
        if t.dep_ != "nsubj" or t.text.lower() not in PRON_SOGGETTO or t.i > t.head.i:
            continue
        if t.i > 0 and doc[t.i - 1].text.lower() in FOCUS:
            continue
        if any(c.dep_ in ("conj", "cc") for c in t.children) or t.dep_ == "conj":
            continue
        if any(c.dep_ == "conj" and c.head == t for c in t.head.children):
            continue
        if "Sub" in t.head.morph.get("Mood"):
            continue
        # il pronome in coppia contrastiva nella stessa frase («lui ride, lei no»)
        altri = [x for x in t.sent if x.dep_ == "nsubj" and x.text.lower() in PRON_SOGGETTO and x != t]
        if any(x.text.lower() != t.text.lower() for x in altri):
            continue
        out.append(doc[t.i: t.head.i + 1].text)
    return out


# ------------------------------------------------------- tratti sintattici

def _profondita(t) -> int:
    n = 0
    while t.head != t:
        t, n = t.head, n + 1
    return n


def _subordinata(t) -> bool:
    if t.dep_ in SUBORDINATE:
        return True
    return t.dep_ == "acl" and "Fin" in t.morph.get("VerbForm")


def _livelli(t) -> int:
    n = 0
    while True:
        if _subordinata(t):
            n += 1
        if t.head == t:
            return n
        t = t.head


def tratti_frase(sent) -> dict:
    parole = [t for t in sent if not t.is_punct and not t.is_space]
    dist = [abs(t.i - t.head.i) for t in parole if t.head != t and not t.head.is_punct]
    return {
        "profondita": max((_profondita(t) for t in sent), default=0),
        "livelli": max((_livelli(t) for t in sent), default=0),
        "dip": dist,
        "parole": len(parole),
    }


def _mattr(seq: list, w: int = 25) -> float:
    if not seq:
        return 0.0
    if len(seq) <= w:
        return len(set(seq)) / len(seq)
    return st.mean(len(set(seq[i:i + w])) / w for i in range(len(seq) - w + 1))


def lemmi_contenuto(doc) -> list:
    return [t.lemma_.lower() for t in doc
            if t.pos_ in CONTENUTO and not t.is_stop and t.is_alpha and len(t.text) > 2]


def analizza(testo: str, nlp=None) -> dict:
    """Le misure di un testo (un box o una versione votata)."""
    nlp = nlp or carica_nlp()
    doc = nlp(testo)
    frasi = [tratti_frase(s) for s in doc.sents if any(not t.is_punct for t in s)]
    frasi = [f for f in frasi if f["parole"] >= 2] or [{"profondita": 0, "livelli": 0, "dip": [], "parole": 0}]
    parole = sum(f["parole"] for f in frasi)
    rilievi = {k: f(doc) for k, f in (("sogg_preverbale", sogg_preverbale),
                                      ("agg_complesso", agg_complesso),
                                      ("stare_gerundio", stare_gerundio),
                                      ("pron_soggetto", pron_soggetto))}
    poss = [m.group(0) for m in POSSESSIVI_CORPO.finditer(testo)]
    dist = [d for f in frasi for d in f["dip"]]
    lem = lemmi_contenuto(doc)
    visti, rip = set(), 0
    for x in lem:
        rip += x in visti
        visti.add(x)
    tutti = [t.lemma_.lower() for t in doc if t.is_alpha]
    return {
        "parole": parole,
        "frasi": len(frasi),
        **{k: len(v) for k, v in rilievi.items()},
        "calchi": sum(len(rilievi[k]) for k in CALCHI),
        "possessivi_corpo": len(poss),
        "profondita_max": max(f["profondita"] for f in frasi),
        "profondita_media": round(st.mean(f["profondita"] for f in frasi), 2),
        "livelli_max": max(f["livelli"] for f in frasi),
        "frasi_oltre2%": round(100 * sum(f["livelli"] > 2 for f in frasi) / len(frasi), 1),
        "lungh_dip": round(st.mean(dist), 2) if dist else 0.0,
        "mattr_lemmi": round(_mattr(tutti), 3),
        "rip_interna%": round(100 * rip / len(lem), 1) if lem else 0.0,
        "rilievi": {k: v for k, v in rilievi.items() if v},
        "_lemmi": sorted(visti),
    }


# ---------------------------------------------------------------- i file

def box_con_riga(testo: str) -> "list[tuple[int, str]]":
    """I box di misura_craft.box_read_aloud, ognuno con la riga d'inizio (1-based)."""
    righe = testo.splitlines()
    out, da = [], 0
    for box in mc.box_read_aloud(testo):
        for i in range(da, len(righe)):
            if righe[i] == box[0]:
                out.append((i + 1, mc.corpo_del_box(box)))
                da = i + len(box)
                break
    return out


MEDIE = ("calchi", "sogg_preverbale", "agg_complesso", "stare_gerundio", "pron_soggetto",
         "possessivi_corpo", "profondita_max", "livelli_max", "frasi_oltre2%", "lungh_dip",
         "mattr_lemmi", "rip_interna%", "rip_fra_box%")


def misura_file(percorso: Path, nlp=None) -> dict:
    nlp = nlp or carica_nlp()
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    box = []
    for riga, corpo in box_con_riga(testo):
        if len(corpo.split()) < 3:
            continue
        m = analizza(corpo, nlp)
        m["riga"] = riga
        m["testo"] = corpo[:90] + ("…" if len(corpo) > 90 else "")
        box.append(m)
    # ripetizione a distanza: lemmi del box che tornano in un altro box del file
    conta: dict = {}
    for b in box:
        for x in b["_lemmi"]:
            conta[x] = conta.get(x, 0) + 1
    for b in box:
        L = b.pop("_lemmi")
        b["rip_fra_box%"] = round(100 * sum(conta[x] > 1 for x in L) / len(L), 1) if L else 0.0
    try:
        rel = str(percorso.resolve().relative_to(ROOT))
    except ValueError:
        rel = str(percorso)
    parole = sum(b["parole"] for b in box)
    medie = {k: round(st.mean(b[k] for b in box), 2) for k in MEDIE} if box else {}
    if box:
        medie["calchi_per_1000_parole"] = round(1000 * sum(b["calchi"] for b in box) / max(1, parole), 2)
        medie["frasi_oltre2%_tot"] = round(
            100 * sum(b["frasi_oltre2%"] * b["frasi"] / 100 for b in box) / sum(b["frasi"] for b in box), 1)
    ricorrenti = sorted(((n, x) for x, n in conta.items() if n >= 4), reverse=True)[:10]
    return {"file": rel, "box": len(box), "parole": parole, "medie": medie,
            "lemmi_ricorrenti": [[x, n] for n, x in ricorrenti], "per_box": box}


def peggiori(dati: dict, chiave: str, n: int = 3) -> list:
    return sorted((b for b in dati["per_box"] if b[chiave]), key=lambda b: -b[chiave])[:n]


def stampa(dati: dict, per_box: bool) -> None:
    m = dati["medie"]
    print(f"\n{dati['file']}  —  {dati['box']} box, {dati['parole']} parole")
    if not m:
        print("   nessun box read-aloud")
        return
    print(f"   calchi/box {m['calchi']:.2f} ({m['calchi_per_1000_parole']:.1f}‰ parole): "
          f"sogg.prev {m['sogg_preverbale']:.2f} · agg.compl {m['agg_complesso']:.2f} · "
          f"stare+ger {m['stare_gerundio']:.2f}  "
          f"[fuori totale: pron.sogg {m['pron_soggetto']:.2f}, possessivi corpo "
          f"{m['possessivi_corpo']:.2f} da validate_prosa]")
    print(f"   profondità max {m['profondita_max']:.1f} · livelli max {m['livelli_max']:.2f} · "
          f"frasi >2 livelli {m['frasi_oltre2%_tot']:.1f}% · lungh.dip {m['lungh_dip']:.2f}")
    print(f"   MATTR lemmi {m['mattr_lemmi']:.3f} · ripetizione interna {m['rip_interna%']:.1f}% · "
          f"fra box {m['rip_fra_box%']:.1f}%")
    if dati["lemmi_ricorrenti"]:
        print("   lemmi in ≥4 box: " + ", ".join(f"{x} {n}" for x, n in dati["lemmi_ricorrenti"]))
    righe = per_box and dati["per_box"] or peggiori(dati, "calchi")
    titolo = "box" if per_box else "box con più calchi"
    if righe:
        print(f"   {titolo}:")
    for b in righe:
        print(f"     r.{b['riga']:<5} calchi {b['calchi']} liv {b['livelli_max']} prof {b['profondita_max']}  {b['testo']}")
        for k, v in b["rilievi"].items():
            print(f"            {k}: " + " | ".join(v[:3]))
    if not per_box:
        for b in peggiori(dati, "livelli_max"):
            if b["livelli_max"] > 2:
                print(f"     r.{b['riga']:<5} {b['livelli_max']} livelli di subordinate  {b['testo']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", action="append", help="un master (ripetibile); senza, la base ARC-07/ARC-08")
    ap.add_argument("--json", action="store_true", help="uscita JSON")
    ap.add_argument("--per-box", action="store_true", help="tutti i box, non solo i peggiori")
    a = ap.parse_args(argv)
    files = [Path(f) for f in a.file] if a.file else [ROOT / f for f in BASE]
    for f in files:
        if not f.exists():
            print(f"file assente: {f}", file=sys.stderr)
            return 2
    nlp = carica_nlp()
    if nlp is None:
        print(f"misura_sintassi: spaCy o il modello {MODELLO} non sono installati, "
              "misura saltata (pip install spacy; python -m spacy download it_core_news_md)")
        return 0
    risultati = [misura_file(f, nlp) for f in files]
    if a.json:
        if not a.per_box:
            for r in risultati:
                r["peggiori"] = [{k: b[k] for k in ("riga", "calchi", "livelli_max", "testo", "rilievi")}
                                 for b in peggiori(r, "calchi", 5)]
        print(json.dumps({"modello": MODELLO, "file": risultati}, ensure_ascii=False, indent=1))
        return 0
    for r in risultati:
        stampa(r, a.per_box)
    return 0


if __name__ == "__main__":
    sys.exit(main())
