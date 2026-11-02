#!/usr/bin/env python3
"""coerenza_campagna.py — fronti e orologi, e fatti in contraddizione fra scene e archi.

Scopo
  Il lotto 7c di PIANO-AVVENTURE-COMMUNITY: la coerenza ha i numeri degli
  statblocchi e l'invarianza dei fatti nelle riscritture, non la verità fra
  scene e fra archi, e i fronti e gli orologi non hanno uno schema
  (RICERCA-QUALITA-MISURABILE-2026-10 §1 e §4). Due misure, entrambe
  deterministiche, solo libreria standard più PyYAML.

  fronti   controlla un file di fronti e orologi contro
           `scripts/schemas/fronti_orologi.schema.json` e contro le regole del
           mestiere che lo schema non esprime:
             F1  2-3 pericoli per fronte                   (Dungeon World)
             F2  presagi: 1-3 per l'avventura, 3-5 per la campagna
             F3  1-3 domande sulla posta
             F4  ogni presagio compare, per una delle sue chiavi, in almeno
                 un master dell'arco (dice file:riga del primo)
             F5  ogni `fonte` file:riga esiste davvero
             F6  gli orologi citati da un fronte esistono, gli id sono unici
             O1  segmenti in {4, 6, 8}                     (Blades in the Dark)
                 salvo l'orologio che conta un tempo e lo dichiara in `unita`
                 (giorni, ore): allora basta un intero positivo, perché il
                 March Clock a 42 giorni non si riduce a 8 tacche (DM, 2026-10-23)
             O2  0 <= riempiti <= segmenti
             O3  «quando si riempie» scritto
           e CONTA i campi che il master scrive (fonte) e quelli dedotti
           (fonte null): è la misura di quanto il master già rispetta lo schema.
           Con --state misura anche gli orologi dei villain di campaign/state.yaml
           (solo lettura).

  fatti    il rilevatore di contraddizioni. Per le entità con nome estrae
           attributi fissi (GS, pf, CA, iniziativa, TS, CD delle capacità
           speciali, classi e livelli, titolo, età, anni DR, vivo/morto, chi
           porta quale artefatto, giorno del March Clock) e segnala lo stesso
           attributo della stessa entità con valori diversi, dicendo file:riga
           di ogni valore. È PRUDENTE di proposito: legge i numeri solo nei
           campi di uno statblocco o nella parentesi subito dopo un nome,
           salta le righe di storico (→, «prima della correzione», errata,
           barrato) e le frasi condizionali per vivo/morto. Non decide chi ha
           ragione: dice dove guardare.

Uso
  python3 scripts/coerenza_campagna.py fronti FILE.yaml [FILE.yaml ...] [--state] [--json]
  python3 scripts/coerenza_campagna.py fatti DIR [DIR ...] [--bestiario] [--json]
  python3 scripts/coerenza_campagna.py tutto --fronti F.yaml ... --archi DIR ... --out DIR [--bestiario]

Exit  0 = nessuna violazione (fronti) o misura eseguita (fatti, tutto)
      1 = violazioni nei fronti (solo con `fronti`, o con --rigido)
      2 = errore d'uso o dipendenza mancante
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "scripts" / "schemas" / "fronti_orologi.schema.json"
STATE = ROOT / "campaign" / "state.yaml"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("✗ coerenza_campagna: serve pyyaml (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(ROOT / "scripts"))
from validate_state import validate_schema  # noqa: E402  (stesso sottoinsieme draft-07)

SEGMENTI_AMMESSI = (4, 6, 8)
LIMITI = {
    "pericoli": (2, 3),
    "presagi_avventura": (1, 3),
    "presagi_campagna": (3, 5),
    "domande": (1, 3),
}


# =========================================================================== #
# Utilità comuni
# =========================================================================== #
def _norm(s: str) -> str:
    """Testo confrontabile: minuscolo, apostrofi dritti, senza enfasi markdown."""
    s = unicodedata.normalize("NFC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("`", "")
    s = s.replace("**", "").replace("*", "").replace("_", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def _risolvi_ref(schema: dict) -> dict:
    """Espande i `$ref` locali (#/definitions/x): il validatore di
    validate_state non li conosce, e lo schema li usa per non ripetere `voce`."""
    defs = schema.get("definitions", {})

    def giu(nodo):
        if isinstance(nodo, dict):
            if "$ref" in nodo:
                nome = nodo["$ref"].rsplit("/", 1)[-1]
                return giu(copy.deepcopy(defs[nome]))
            return {k: giu(v) for k, v in nodo.items() if k != "definitions"}
        if isinstance(nodo, list):
            return [giu(x) for x in nodo]
        return nodo

    return giu(schema)


# =========================================================================== #
# 1 · Fronti e orologi
# =========================================================================== #
def _fonte_ok(fonte: str | None, root: Path) -> str | None:
    """None se la fonte esiste, altrimenti il motivo."""
    if fonte is None:
        return None
    file, _, riga = fonte.rpartition(":")
    p = root / file
    if not p.is_file():
        return f"il file «{file}» non esiste"
    n = sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
    if not 1 <= int(riga) <= n:
        return f"la riga {riga} è oltre la fine di «{file}» ({n} righe)"
    return None


def cerca_chiavi(chiavi: list[str], master: list[str], root: Path,
                 cache: dict | None = None) -> str | None:
    """Prima occorrenza (file:riga) di una delle chiavi nei master, o None."""
    cache = {} if cache is None else cache
    for m in master:
        if m not in cache:
            p = root / m
            cache[m] = ([_norm(r) for r in p.read_text(encoding="utf-8").splitlines()]
                        if p.is_file() else [])
        for i, riga in enumerate(cache[m], 1):
            for k in chiavi:
                if _norm(k) in riga:
                    return f"{m}:{i}"
    return None


def controlla_fronti(dati: dict, root: Path = ROOT, schema: dict | None = None) -> dict:
    """Violazioni e misure di un file di fronti. Non lancia: restituisce."""
    if schema is None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    viol: list[dict] = []

    def v(regola, dove, msg):
        viol.append({"regola": regola, "dove": dove, "messaggio": msg})

    for e in validate_schema(dati, _risolvi_ref(schema)):
        v("F0", "schema", e)
    if any(x["regola"] == "F0" for x in viol):
        return {"arco": dati.get("arco") if isinstance(dati, dict) else None,
                "violazioni": viol, "misure": {}, "presagi": [], "orologi": []}

    master = dati["master"]
    for m in master:
        if not (root / m).is_file():
            v("F5", "master", f"il master «{m}» non esiste")

    espliciti = dedotti = 0
    dedotti_dove: list[str] = []

    def conta(fonte, dove):
        nonlocal espliciti, dedotti
        if fonte is None:
            dedotti += 1
            dedotti_dove.append(dove)
        else:
            espliciti += 1
            motivo = _fonte_ok(fonte, root)
            if motivo:
                v("F5", dove, f"fonte {fonte}: {motivo}")

    ids_orologi = [o["id"] for o in dati["orologi"]]
    for d in sorted({i for i in ids_orologi if ids_orologi.count(i) > 1}):
        v("F6", f"orologio {d}", "id duplicato")
    ids_fronti = [f["id"] for f in dati["fronti"]]
    for d in sorted({i for i in ids_fronti if ids_fronti.count(i) > 1}):
        v("F6", f"fronte {d}", "id duplicato")

    cache: dict = {}
    presagi_esito = []
    for f in dati["fronti"]:
        fid = f["id"]
        lo, hi = LIMITI["pericoli"]
        if not lo <= len(f["pericoli"]) <= hi:
            v("F1", fid, f"{len(f['pericoli'])} pericoli: Dungeon World ne vuole {lo}-{hi}")
        lo, hi = LIMITI[f"presagi_{f['tipo']}"]
        if not lo <= len(f["presagi"]) <= hi:
            v("F2", fid, f"{len(f['presagi'])} presagi per un fronte di {f['tipo']}: "
                         f"ne servono {lo}-{hi}")
        lo, hi = LIMITI["domande"]
        if not lo <= len(f["domande"]) <= hi:
            v("F3", fid, f"{len(f['domande'])} domande sulla posta: ne servono {lo}-{hi}")
        conta(f["impulso"]["fonte"], f"{fid}.impulso")
        conta(f["catastrofe"]["fonte"], f"{fid}.catastrofe")
        for i, p in enumerate(f["pericoli"]):
            conta(p["fonte"], f"{fid}.pericoli[{i}] {p['nome']}")
        for i, q in enumerate(f["domande"]):
            conta(q["fonte"], f"{fid}.domande[{i}]")
        for i, p in enumerate(f["presagi"]):
            dove = cerca_chiavi(p["chiavi"], master, root, cache)
            presagi_esito.append({"fronte": fid, "presagio": p["testo"],
                                  "chiavi": p["chiavi"], "trovato": dove})
            if dove is None:
                v("F4", f"{fid}.presagi[{i}]",
                  f"nessuna chiave fra {p['chiavi']} compare nei master dell'arco")
        for oid in f["orologi"]:
            if oid not in ids_orologi:
                v("F6", fid, f"cita l'orologio «{oid}», che non è dichiarato")

    orologi_esito = []
    for o in dati["orologi"]:
        oid = o["id"]
        seg, pieni = o["segmenti"], o["riempiti"]
        ok = True
        a_tempo = bool(o.get("unita")) and isinstance(seg, int) and seg > 0
        if seg not in SEGMENTI_AMMESSI and not a_tempo:
            ok = False
            u = f" ({o.get('unita')})" if o.get("unita") else ""
            v("O1", oid, f"segmenti = {seg}{u}: Blades in the Dark ne vuole 4, 6 o 8, "
                         f"o un intero positivo con `unita` per un orologio a tempo")
        if pieni is None or seg is None or not 0 <= pieni <= seg:
            ok = False
            v("O2", oid, f"riempiti = {pieni} su {seg}: deve stare fra 0 e il totale")
        conta(o["quando_si_riempie"]["fonte"], f"{oid}.quando_si_riempie")
        conta(o["fonte"], f"{oid}.fonte")
        orologi_esito.append({"id": oid, "nome": o["nome"], "segmenti": seg,
                              "riempiti": pieni, "conforme": ok})

    misure = {
        "fronti": len(dati["fronti"]),
        "orologi": len(dati["orologi"]),
        "orologi_conformi": sum(1 for o in orologi_esito if o["conforme"]),
        "presagi": len(presagi_esito),
        "presagi_nei_master": sum(1 for p in presagi_esito if p["trovato"]),
        "campi_espliciti": espliciti,
        "campi_dedotti": dedotti,
        "dedotti": dedotti_dove,
    }
    return {"arco": dati["arco"], "violazioni": viol, "misure": misure,
            "presagi": presagi_esito, "orologi": orologi_esito}


_CLOCK = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")


def misura_orologi_state(path: Path = STATE) -> list[dict]:
    """Gli orologi dei villain di state.yaml sotto O1-O3 (solo lettura)."""
    dati = yaml.safe_load(path.read_text(encoding="utf-8"))
    righe = path.read_text(encoding="utf-8").splitlines()
    out = []
    for vrow in dati.get("villain", []):
        clock = str(vrow.get("clock") or "")
        riga = next((i for i, r in enumerate(righe, 1)
                     if r.strip().startswith("clock:") and clock[:12] in r), None)
        m = _CLOCK.match(clock)
        esito = {"villain": re.sub(r"\*\*|`", "", vrow.get("villain", ""))[:70],
                 "png_id": vrow.get("png_id"), "clock": clock,
                 "riga": f"campaign/state.yaml:{riga}" if riga else None,
                 "quando_si_riempie": bool((vrow.get("trigger") or "").strip())}
        if not m:
            esito.update(segmenti=None, riempiti=None, conforme=False,
                         motivo="non è un orologio a segmenti")
        else:
            pieni, seg = int(m.group(1)), int(m.group(2))
            motivi = []
            if seg not in SEGMENTI_AMMESSI:
                motivi.append(f"{seg} segmenti (O1)")
            if not 0 <= pieni <= seg:
                motivi.append(f"{pieni} riempiti su {seg} (O2)")
            if not esito["quando_si_riempie"]:
                motivi.append("manca il trigger (O3)")
            esito.update(segmenti=seg, riempiti=pieni, conforme=not motivi,
                         motivo="; ".join(motivi) or None)
        out.append(esito)
    return out


# =========================================================================== #
# 2 · Fatti fra scene e fra archi
# =========================================================================== #
ESCLUDI_FILE = re.compile(
    r"(^|/)(_ARCHIVIO|Old|homebrew)(/|$)|ERRATA-|CORREZIONE-|MATRICE-VERSIONI|"
    r"PIANO-REVISIONE|Ricalibrazione|La_Piramide|PortaleForgia-P[123]-", re.I)
"""Fuori dal perimetro, e perché: `_ARCHIVIO` e `Old` sono generazioni superate;
ERRATA e CORREZIONE citano apposta i valori vecchi; la matrice delle versioni
e i piani di revisione parlano DEI file; le ricalibrazioni e le parti P1-P3
precedono il consolidamento e si correggono a vicenda per costruzione
(ARC07-00-INDICE). Con --tutti si leggono lo stesso."""

TITOLI = sorted([
    "alto wyrmlord", "wyrmlord", "re", "regina", "madre superiora", "generale",
    "capitano", "capitana", "maestro", "maestra", "mastro", "signore", "signora",
    "matrona", "conte", "contessa", "lord", "lady", "sergente", "comandante",
    "principe", "principessa", "thane", "sorella", "fratello", "padre", "madre",
], key=len, reverse=True)
ARTICOLI = ("il ", "lo ", "la ", "le ", "i ", "gli ", "l'")
NON_ENTITA = re.compile(
    r"^(tattic|statistic|incontro|mappa|round|fase|scena|sessione|giorno|appendice|"
    r"indice|zona|atto|nota|regia|esito|tabella|schede?|unit|esercito|budget|tesoro|"
    r"handout|immagini|musica|contingenz|echo|avanzamento|ponte|quick|highlight|"
    r"meccanic|condizion|risultat|obiettiv|introduzione|legenda|capitolo|png|pnf|"
    r"analisi|sidebar|come |cosa |chi |se |quando |perch|il giro|le cd|i nemici|"
    r"supporto|armi|regola|riepilogo|struttura|rapporto|composizione|interazione|"
    r"effetti|eventi|opzioni|azioni|errata|a\.|b\.|c\.)")
CLASSI = {
    "guerriero", "guerriera", "chierico", "chierica", "mago", "maga", "stregone", "strega",
    "ladro", "ladra", "ranger", "druido", "druida", "bardo", "barda", "monaco", "monaca",
    "paladino", "barbaro", "warlock", "nobile", "nera", "guerra", "divina", "divino",
    "tempeste", "nanico", "picchi", "rune", "maestra", "maestro", "illusionista", "ombre",
    "esperto", "popolano", "combattente", "adepto", "aristocratico", "warpriest",
    "fighter", "cleric", "wizard", "sorcerer", "rogue", "monk", "druid", "bard",
    "barbarian", "paladin", "blackguard", "assassino", "assassin", "psion", "gish",
    "esploratore", "esploratrice", "difensore", "campione", "sacerdote", "spia",
    "danzatrice", "teurgo", "arcano", "runaio", "fabbro", "berserker", "templare",
}
"""L'ultima parola di una classe o di una classe di prestigio, come la scrivono
gli archi: senza questo filtro «APL 13» e «CA 28» diventavano classi."""
RAZZE = {"nano", "nana", "umano", "umana", "elfo", "elfa", "mezzelfo", "mezzelfa",
         "mezzorco", "orog", "drow", "gnomo", "halfling", "hobgoblin", "goblin",
         "orco", "dwarf", "human", "dream", "mezzo-ogre", "ogre", "dello", "scudo"}

STORICO_RIGA = re.compile(
    r"→|->|~~|prima della correzione|diceva|superat|storico|errata|boost log|"
    r"benchmark|invece di|non più|vecchi[ao] |era stat|correzione|ri-prezz|"
    r"il vecchio|la vecchia|ricalibrat|pre-boost|prima del boost", re.I)
COMMENTO = re.compile(r"<!--.*?-->", re.S)
STORICO_INLINE = re.compile(r"<!--\s*storico\s*-->.*?<!--\s*/storico\s*-->", re.S)
HEADING = re.compile(r"^(#{1,6})\s+(\S.*)$")
VARIANTE = re.compile(
    r"variant|versione|scal[ae]|ferit|\bbis\b|-bis|alternativ|carry|potenziat|"
    r"con [3-5] pg|giovane|vecchio|ridott|\bse\b|forma |evocat|boost|"
    r"senza |dopo |prima ", re.I)
CONDIZIONALE = re.compile(
    r"\bse\b|\bqualora\b|\bquando\b|\bram[oi]\b|alternativ|\bdefault\b|\boppure\b|"
    r"\bpuò\b|\bpotrebbe\b|\bforse\b|\?|\bfinché\b|a meno|nel caso|\bo\b|"
    r"\bipotes|\bsenn[oò]\b|\bcomunque\b|\bmai\b|\bnon\b|\bsembra|\bcrede|"
    r"\bcome se\b|\bfinge|\bpare\b", re.I)

ARTEFATTI = OrderedDict([
    ("Aegis Fang", ["aegis fang"]),
    ("Corona di Adamantio", ["corona di adamantio", "la corona"]),
    ("Ring of Chaotic Illumination", ["ring of chaotic illumination", "l'anello"]),
    ("Bracieri Gemelli", ["bracieri gemelli", "i bracieri"]),
    ("Collana dei Semi Eterni", ["collana dei semi eterni", "la collana"]),
    ("Cintura della Devastazione", ["cintura della devastazione"]),
])
PG = ["Thorik", "Tordek", "Hella", "Artemis"]
EVENTI = {"cerimonia delle 100 asce": "Cerimonia delle 100 Asce",
          "caduta di terrelton": "caduta di Terrelton"}
"""Eventi con una data: senza un nome non c'è entità a cui legare il giorno."""
LUOGHI = ["hammerfist", "rethmar", "terrelton", "rhest", "fane di tiamat", "dauth",
          "sala della forgia", "cuore della montagna", "tempio di mithral",
          "torre invisibile", "skull gorge", "vraath keep", "drellin's ferry"]
"""I luoghi fra cui si misura una distanza. Pochi e certi: una distanza senza
due capi nominati («a 30 m dalla linea») non è un fatto confrontabile."""

# --- campi di statblocco: ancorati all'INIZIO del campo, mai in mezzo alla prosa
F_PF = re.compile(r"(?:^|[·|;]\s*)(?:PF|pf|Punti Ferita|Punti ferita)\s*:?\s*~?\s*(\d{1,4})\b")
F_CA = re.compile(r"(?:^|[·|;]\s*)CA\s*:?\s*(\d{1,2})\b")
F_INIZ = re.compile(r"(?:^|[·|;]\s*)(?:Iniziativa|Iniz\.?)\s*:?\s*([+−-]\s?\d{1,2})\b")
F_PF_DV = re.compile(r"^\s*(?:DV|Dadi Vita)\b[^()\n]*\((\d{2,4})\s*pf\)")
F_TS = re.compile(r"(?:^|[·|;]\s*)TS\s*:?\s*Temp(?:ra)?\.?\s*([+−-]\d{1,2})\D{1,6}Rifl(?:essi)?\.?\s*"
                  r"([+−-]\d{1,2})\D{1,6}Vol(?:ont[àa])?\.?\s*([+−-]\d{1,2})")
F_TITOLO_FENCE = re.compile(r"^\s*([A-ZÀ-Ý][A-ZÀ-Ý'’ ]{3,40}?)\s*(?:—|–|\s-\s|\(|$)")
F_GS = re.compile(r"\b(?:GS|CR|Grado di Sfida)\s*:?\s*(\d{1,2}(?:/\d)?)\b")
F_CAPACITA = re.compile(r"^\s*(?:[-•*]\s*)?([A-Za-zÀ-ÿ' ]{3,40}?)\s*\((?:Sop|Str|Mag|Su|Ex|Sp)\)\s*:?(.*)$")
F_CD = re.compile(r"\bCD\s*(\d{1,2})\b")
INLINE_NOME_PAREN = re.compile(r"\*\*([^*\n]{3,60}?)\*\*\s*\(([^()\n]{2,160})\)")
DAY = re.compile(r"\b(?:March Clock\s+)?Day\s+(\d{1,2}(?:\s*[-–]\s*\d{1,2})?)\b")


def _pulisci(s: str) -> str:
    s = s.replace("**", "").replace("*", "").replace("`", "").replace("_", " ")
    s = "".join(ch for ch in s if unicodedata.category(ch)[0] in "LNPZ" or ch in "'’")
    return re.sub(r"\s+", " ", s).strip()


def chiave_entita(nome: str) -> tuple[str | None, str | None]:
    """(chiave, titolo) di un nome come compare in un titolo o in grassetto.

    «RE THOREK HAMMERFIST (Nano Guerriero 15°…)» → ("thorek hammerfist", "re").
    Restituisce (None, None) per i titoli che non sono entità."""
    s = _pulisci(nome).replace("’", "'")
    s = re.sub(r"^[A-Z]?\.?\d+[a-z]?(?:\.\d+)*(?:-bis)?\s*[·.:-]\s*", "", s)
    s = re.sub(r"^(?:§\s*\d+\S*\s*[—-]\s*)", "", s)
    s = re.sub(r"^(?:BOSS|Boss|Scheda d'entrata)\s*[:—-]\s*", "", s)
    s = re.split(r"\s[(—–]|\(|,|:|\s-\s|«", s)[0]
    s = s.strip(" .;").lower()
    for a in ARTICOLI:
        if s.startswith(a):
            s = s[len(a):]
    titolo = None
    for t in TITOLI:
        if s.startswith(t + " ") and len(s) > len(t) + 2:
            titolo, s = t, s[len(t) + 1:]
            break
    s = s.strip()
    if len(s) < 3 or NON_ENTITA.match(s) or not re.search(r"[a-zà-ÿ]{3}", s):
        return None, None
    if len(s.split()) > 5:
        return None, None
    return s, titolo


def classi_da_paren(paren: str) -> str | None:
    """«Nano Guerriero 15°/Nobile 2°, GS 16» → «guerriero 15/nobile 2».

    Conta solo le parole che chiudono il nome di una classe (CLASSI): «APL 13»,
    «CA 28» e «Aegis Fang +21» non sono classi."""
    parti = set()
    for mm in re.finditer(r"([A-Za-zÀ-ÿ]+)\s+(\d{1,2})°?(?![\d+])(?!/[+-])", _pulisci(paren)):
        parola = mm.group(1).lower()
        if parola in CLASSI:
            parti.add(f"{parola} {int(mm.group(2))}")
    return "/".join(sorted(parti)) if parti else None


class Raccolta:
    """Occorrenze per (entità, attributo, valore), in ordine di lettura."""

    def __init__(self):
        self.occ: dict[tuple[str, str], OrderedDict] = {}
        self.nomi: dict[str, str] = {}

    def add(self, ent, attr, valore, file, riga, sezione, testo):
        if ent is None or valore is None:
            return
        valore = str(valore).replace("−", "-").strip()
        if re.fullmatch(r"[+-]?\s*\d+", valore):
            valore = valore.replace(" ", "")
        d = self.occ.setdefault((ent, attr), OrderedDict())
        lst = d.setdefault(valore, [])
        if all((o["file"], o["riga"]) != (file, riga) for o in lst):
            lst.append({"file": file, "riga": riga, "sezione": sezione,
                        "testo": testo.strip()[:220]})

    def contraddizioni(self) -> list[dict]:
        out = []
        for (ent, attr), valori in sorted(self.occ.items()):
            if attr == "titolo":
                # «Madre» è la forma breve di «Madre Superiora»: non si contraddicono
                valori = OrderedDict((v, o) for v, o in valori.items()
                                     if not any(w != v and w.startswith(v + " ") for w in valori))
            if len(valori) < 2:
                continue
            out.append({
                "entita": self.nomi.get(ent, ent), "chiave": ent, "attributo": attr,
                "valori": [{"valore": v, "n": len(o), "occorrenze": o[:3]}
                           for v, o in valori.items()],
            })
        for i, c in enumerate(out, 1):
            c["id"] = f"C{i:03d}"
        return out


def _righe_pulite(testo: str) -> list[str]:
    """Il testo riga per riga, con commenti e storico inline svuotati ma le
    righe conservate (i numeri di riga restano quelli del file)."""
    def vuota(m):
        return "\n" * m.group(0).count("\n")
    testo = STORICO_INLINE.sub(vuota, testo)
    testo = COMMENTO.sub(vuota, testo)
    return testo.splitlines()


def sezioni(righe: list[str]):
    """Genera (indice_riga, titolo_sezione, livello, in_fence) per ogni riga."""
    fence = False
    titolo, livello = "", 0
    for i, r in enumerate(righe):
        if r.lstrip().startswith("```"):
            fence = not fence
            yield i, titolo, livello, True
            continue
        m = None if fence else HEADING.match(r)
        if m:
            titolo, livello = m.group(2), len(m.group(1))
        yield i, titolo, livello, fence


def estrai_file(path: Path, rac: Raccolta, entita_note: dict) -> None:
    """Statblocchi, parentesi dopo i nomi, campi di prosa: tutto in `rac`."""
    rel = _rel(path)
    righe = _righe_pulite(path.read_text(encoding="utf-8", errors="replace"))
    blocco_ent, blocco_ok, righe_blocco = None, False, 0
    visti_blocco: set[str] = set()
    intestazione: list[str] | None = None
    salvato = None      # il blocco del titolo, mentre si legge uno statblocco in un recinto
    cerca_titolo = 0
    for i, sez, liv, fence in sezioni(righe):
        r = righe[i]
        n = i + 1
        # ---- statblocco in un recinto ``` : l'entità è la riga in MAIUSCOLO in testa
        if r.lstrip().startswith("```"):
            if salvato is None:
                salvato = (blocco_ent, blocco_ok, visti_blocco, righe_blocco)
                cerca_titolo = 4
            else:
                blocco_ent, blocco_ok, visti_blocco, righe_blocco = salvato
                salvato, cerca_titolo = None, 0
            continue
        if fence and cerca_titolo:
            cerca_titolo -= 1
            mt = F_TITOLO_FENCE.match(r)
            if mt and mt.group(1).strip() == mt.group(1).strip().upper() and len(mt.group(1).strip()) > 3:
                ent, _ = chiave_entita(mt.group(1))
                if ent:
                    cerca_titolo = 0
                    ok = salvato[1] if salvato[0] else True
                    blocco_ent, blocco_ok = ent, ok and not VARIANTE.search(r)
                    visti_blocco, righe_blocco = set(), 0
                    entita_note.setdefault(ent, _pulisci(mt.group(1)).title())
                    gs = F_GS.findall(r)
                    if blocco_ok and len(gs) == 1:
                        rac.add(ent, "GS", gs[0], rel, n, sez, r)
                        visti_blocco.add("GS")
                    continue
        # ---- tabelle con una colonna pf / CA / GS: la cella vale solo se è un numero
        if not fence and r.lstrip().startswith("|"):
            celle = [c.strip() for c in r.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in celle if c):
                intestazione = [_pulisci(c).lower() for c in righe[i - 1].strip().strip("|").split("|")] if i else None
                continue
            if intestazione and len(celle) == len(intestazione) and not STORICO_RIGA.search(r):
                ent, _ = chiave_entita(celle[0])
                if ent and not VARIANTE.search(_pulisci(celle[0])):
                    for col, cella in zip(intestazione[1:], celle[1:]):
                        attr = {"pf": "pf", "ca": "CA", "gs": "GS", "iniziativa": "iniziativa"}.get(col)
                        mm = re.fullmatch(r"~?\s*([+−-]?\d{1,4})", _pulisci(cella))
                        if attr and mm:
                            entita_note.setdefault(ent, _pulisci(celle[0]))
                            rac.add(ent, attr, mm.group(1), rel, n, sez, r)
        else:
            intestazione = None
        m = None if fence else HEADING.match(r)
        if m:
            ent, tit = chiave_entita(m.group(2))
            blocco_ent, righe_blocco = ent, 0
            blocco_ok = ent is not None and not VARIANTE.search(_pulisci(m.group(2)))
            visti_blocco = set()
            if ent:
                entita_note.setdefault(ent, _pulisci(m.group(2)).split("(")[0].strip(" ,—-"))
                paren = re.search(r"\(([^()]*)\)", m.group(2))
                if paren and blocco_ok:
                    gs = F_GS.findall(paren.group(1))
                    if len(gs) == 1:
                        rac.add(ent, "GS", gs[0], rel, n, sez, r)
                        visti_blocco.add("GS")
                    rac.add(ent, "classi", classi_da_paren(paren.group(1)), rel, n, sez, r)
                if tit:
                    rac.add(ent, "titolo", tit, rel, n, sez, r)
            continue
        righe_blocco += 1
        piatta = _pulisci(r) if not fence else r.strip()
        if STORICO_RIGA.search(r):
            continue
        # ---- campi di statblocco del blocco corrente
        if blocco_ent and blocco_ok:
            for attr, rx in (("pf", F_PF), ("pf", F_PF_DV), ("CA", F_CA), ("iniziativa", F_INIZ)):
                if attr in visti_blocco:
                    continue
                mm = rx.search(piatta)
                if mm:
                    rac.add(blocco_ent, attr, mm.group(1), rel, n, sez, r)
                    visti_blocco.add(attr)
            if righe_blocco <= 3 or fence:
                # la riga d'apertura in prosa: «Guerriero di 5°, GS 5: 37 pf, CA 21 …»
                if "pf" not in visti_blocco:
                    mm = re.search(r"\b(\d{2,4})\s*pf\b", piatta)
                    if mm and righe_blocco <= 3:
                        rac.add(blocco_ent, "pf", mm.group(1), rel, n, sez, r)
                        visti_blocco.add("pf")
                if "CA" not in visti_blocco:
                    mm = re.search(r"(?:^|[,:;·|]\s*)CA\s*:?\s*(\d{1,2})\b", piatta)
                    if mm:
                        rac.add(blocco_ent, "CA", mm.group(1), rel, n, sez, r)
                        visti_blocco.add("CA")
            if "TS" not in visti_blocco:
                mm = F_TS.search(piatta)
                if mm:
                    rac.add(blocco_ent, "TS", "/".join(mm.groups()), rel, n, sez, r)
                    visti_blocco.add("TS")
            if "GS" not in visti_blocco and righe_blocco <= 3:
                gs = F_GS.findall(piatta)
                if len(gs) == 1:
                    rac.add(blocco_ent, "GS", gs[0], rel, n, sez, r)
                    visti_blocco.add("GS")
            mm = F_CAPACITA.match(piatta)
            if mm:
                cd = F_CD.findall(mm.group(2))
                nome_cap = mm.group(1).strip().lower()
                if len(set(cd)) == 1 and f"CD {nome_cap}" not in visti_blocco:
                    rac.add(blocco_ent, f"CD {nome_cap}", cd[0], rel, n, sez, r)
                    visti_blocco.add(f"CD {nome_cap}")
        if fence:
            continue
        # ---- il nome in grassetto con la parentesi subito dopo
        for mm in INLINE_NOME_PAREN.finditer(r):
            ent, tit = chiave_entita(mm.group(1))
            if not ent or VARIANTE.search(mm.group(2)):
                continue
            entita_note.setdefault(ent, _pulisci(mm.group(1)))
            gs = F_GS.findall(mm.group(2))
            if len(gs) == 1:
                rac.add(ent, "GS", gs[0], rel, n, sez, r)
            rac.add(ent, "classi", classi_da_paren(mm.group(2)), rel, n, sez, r)


def _frasi(riga: str) -> list[str]:
    return [f for f in re.split(r"(?<=[.!?;])\s+", riga) if f.strip()]


def alias_brevi(chiavi: set[str], testi: list[str]) -> dict[str, str]:
    """«terros» → «terros l'antico»: il primo nome, se è di UNA sola entità e se
    nel corpus compare SOLO con la maiuscola (cioè è un nome proprio).

    «fauci» resta fuori (Fauci di Palude e Fauci di Diamante), «goblin» pure
    (compare minuscolo): la prudenza vale più di qualche riga trovata in più."""
    primi: dict[str, list[str]] = {}
    for k in chiavi:
        if " " in k:
            primi.setdefault(k.split()[0], []).append(k)
    out = {}
    corpus = "\n".join(testi)
    for t, ks in primi.items():
        if (len(ks) != 1 or len(t) < 5 or t in chiavi or t in {p.lower() for p in PG}
                or not re.fullmatch(r"[a-zà-ÿ']+", t)):
            continue
        if re.search(r"(?<![\w-])" + re.escape(t) + r"\b", corpus):   # compare minuscolo
            continue
        out[t] = ks[0]
    return out


def estrai_prosa(path: Path, rac: Raccolta, nomi: dict[str, str],
                 alias: dict[str, str] | None = None) -> None:
    """Titolo, età, anni DR, vivo/morto, artefatti, giorno del March Clock."""
    rel = _rel(path)
    righe = _righe_pulite(path.read_text(encoding="utf-8", errors="replace"))
    # le superfici cercate: la chiave intera (due parole, o una lunga) e gli alias brevi
    forme = {}
    for k in nomi:
        if len(k.split()) >= 2 or len(k) >= 6:
            forme[k] = k
    for corta, lunga in (alias or {}).items():
        forme[corta] = lunga
    for i, sez, liv, fence in sezioni(righe):
        if fence:
            continue
        r = righe[i]
        n = i + 1
        if HEADING.match(r) or STORICO_RIGA.search(r):
            continue
        piatta = _pulisci(r).replace("’", "'")
        for corta in (alias or {}):
            # «Ogre Skullcrusher» non è Skullcrusher il Nero: un alias breve
            # preceduto da un'altra parola con la maiuscola fa parte di un altro nome
            piatta = re.sub(r"(\b[A-ZÀ-Ý][a-zà-ÿ']{1,20} )" + re.escape(corta.capitalize()) + r"\b",
                            lambda m: m.group(1) + "·" * len(corta), piatta)
        bassa = piatta.lower()
        for superficie, k in forme.items():
            if superficie not in bassa:
                continue
            nome = re.escape(superficie).replace("\\ ", r"\s+")
            # titolo davanti al nome completo
            for mm in re.finditer(r"\b(" + "|".join(map(re.escape, TITOLI)) + r")\s+" + nome + r"\b",
                                  bassa):
                rac.add(k, "titolo", mm.group(1), rel, n, sez, r)
            # «Terros 345 pf», e il nome seguito dalla sua parentesi
            for mm in re.finditer(r"\b" + nome + r"\s+~?(\d{2,4})\s*pf\b", bassa):
                rac.add(k, "pf", mm.group(1), rel, n, sez, r)
            for mm in re.finditer(r"\b" + nome + r"\s*\(([^()]{2,160})\)", piatta, re.I):
                if VARIANTE.search(mm.group(1)):
                    continue
                gs = F_GS.findall(mm.group(1))
                if len(gs) == 1:
                    rac.add(k, "GS", gs[0], rel, n, sez, r)
                rac.add(k, "classi", classi_da_paren(mm.group(1)), rel, n, sez, r)
            for fr in _frasi(bassa):
                if not re.search(r"\b" + nome + r"\b", fr):
                    continue
                # età
                for mm in re.finditer(r"\b" + nome + r"\b[^.;:]{0,40}?(?:\bha\b|\bdi\b|,|\(|età di|\baveva\b)\s*"
                                      r"(\d{2,4})\s+anni\b(?!\s+(?:fa|prima|dopo|d[ai]|nel))", fr):
                    rac.add(k, "età", mm.group(1), rel, n, sez, r)
                # anni DR con un verbo che dice quale anno è
                for mm in re.finditer(r"\b" + nome + r"\b[^.;]{0,60}?\b(nat[oa]|mort[oa]|fondat[oa]|"
                                      r"erett[oa]|costruit[oa]|cadut[oa]|forgiat[oa]|sepolt[oa])\b"
                                      r"[^.;]{0,30}?\b(?:nel|del|dal)\s+(?:≈|~|circa\s+)?(\d{3,4})\s*dr\b", fr):
                    rac.add(k, f"anno DR ({mm.group(1)[:-1]}o)", mm.group(2), rel, n, sez, r)
                # vivo o morto, solo in frasi affermative e incondizionate
                if not CONDIZIONALE.search(fr):
                    mm = re.search(r"\b" + nome + r"\b[^.;:,]{0,25}?\b(?:(?:è|resta|rimane)\s+(mort|viv)[oa]|"
                                   r"(muore|sopravvive))\b", fr)
                    if mm:
                        stato = "morto" if (mm.group(1) == "mort" or mm.group(2) == "muore") else "vivo"
                        rac.add(k, "vivo/morto", stato, rel, n, sez, r)
                # giorno del March Clock («Giorno 3 dell'assedio» è un conteggio locale: no)
                if "day" in fr or "giorno" in fr:
                    mm = re.search(r"\b" + nome + r"\b[^.;]{0,50}?\b(?:day|giorno)\s+"
                                   r"(\d{1,2}(?:\s*[-–]\s*\d{1,2})?)\b(?!\s*(?:dell'assedio|di battaglia|d'assedio))", fr)
                    if mm and not CONDIZIONALE.search(fr[:mm.start()]):
                        rac.add(k, "giorno March Clock", mm.group(1), rel, n, sez, r)
        # distanza fra due luoghi nominati nella stessa frase
        for fr in _frasi(bassa):
            for mm in re.finditer(r"\b(" + "|".join(map(re.escape, LUOGHI)) + r")\b[^.;]{0,60}?\b(\d+(?:[.,]\d+)?)\s*"
                                  r"(km|chilometri|miglia|giorni di marcia)\b[^.;]{0,15}?\b(?:da|dal|dalla|dall'|dai)\s*"
                                  r"(" + "|".join(map(re.escape, LUOGHI)) + r")\b", fr):
                a, b = sorted((mm.group(1), mm.group(4)))
                if a != b and not CONDIZIONALE.search(fr):
                    rac.add(f"{a} ↔ {b}", f"distanza ({mm.group(3)})", mm.group(2).replace(",", "."),
                            rel, n, sez, r)
        # chi porta quale artefatto
        for art, forme_art in ARTEFATTI.items():
            for a in forme_art:
                if a not in bassa:
                    continue
                pgs = "|".join(p.lower() for p in PG)
                for mm in re.finditer(re.escape(a) + r"\s+(?:di|sulla fronte di|al collo di|al dito di|"
                                      r"ai polsi di|nelle mani di|in mano a)\s+(" + pgs + r")\b", bassa):
                    rac.add(art.lower(), "portatore", mm.group(1).capitalize(), rel, n, sez, r)
                    rac.nomi[art.lower()] = art
                for mm in re.finditer(r"\b(" + pgs + r")\s+(?:impugna|brandisce|indossa|stringe|porta)\s+"
                                      r"(?:la |l'|il |i |lo |gli |le )?" + re.escape(a) + r"\b", bassa):
                    rac.add(art.lower(), "portatore", mm.group(1).capitalize(), rel, n, sez, r)
                    rac.nomi[art.lower()] = art


def file_degli_archi(dirs: list[Path], tutti: bool = False) -> list[Path]:
    out = []
    for d in dirs:
        for p in sorted(d.glob("*.md")):
            if tutti or not ESCLUDI_FILE.search(_rel(p)):
                out.append(p)
    return out


def file_bestiario(chiavi: set[str]) -> list[Path]:
    """Le voci del Bestiario la cui entità compare negli archi."""
    out = []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        if "pregen" in str(p) or "README" in p.name or "INDICE" in p.name:
            continue
        stem = re.sub(r"-cr\d+$", "", p.stem).replace("_", " ").replace("-", " ").lower()
        stem = stem.replace("  ", " ").strip()
        prima = ""
        for r in p.read_text(encoding="utf-8", errors="replace").splitlines()[:5]:
            if r.startswith("#"):
                prima = chiave_entita(r.lstrip("# "))[0] or ""
                break
        if stem in chiavi or prima in chiavi:
            out.append(p)
    return out


def nomi_state(path: Path = STATE) -> dict[str, str]:
    """Le chiavi dei PNG dell'anagrafica di state.yaml, per la prosa."""
    try:
        dati = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except OSError:
        return {}
    out = {}
    for p in dati.get("png", []) or []:
        k, _ = chiave_entita(str(p.get("nome", "")))
        if k:
            out[k] = _pulisci(str(p.get("nome", ""))).split("(")[0].strip()
    return out


def unisci_alias(rac: Raccolta) -> None:
    """«terros» dentro «terros l'antico», ma solo se l'estensione è UNA.

    Prudenza: «thorek» ha due estensioni (Thorek Hammerfist e Thorek I, mille
    anni di distanza) e resta da solo. Fondere per somiglianza è il modo in cui
    validate_state aveva agganciato Zalkatar a Xal'thor (R10)."""
    chiavi = {k for k, _ in rac.occ}
    for corta in sorted({k for k in chiavi if " " not in k}):
        lunghe = [k for k in chiavi if k.startswith(corta + " ")]
        if len(lunghe) != 1:
            continue
        lunga = lunghe[0]
        for (ent, attr) in [x for x in rac.occ if x[0] == corta]:
            for val, occ in rac.occ.pop((ent, attr)).items():
                for o in occ:
                    rac.add(lunga, attr, val, o["file"], o["riga"], o["sezione"], o["testo"])


def rileva_contraddizioni(dirs: list[Path], bestiario: bool = False,
                          tutti: bool = False) -> dict:
    files = file_degli_archi(dirs, tutti)
    rac = Raccolta()
    note: dict[str, str] = {}
    for p in files:
        estrai_file(p, rac, note)
    best = file_bestiario({k for k, _ in rac.occ}) if bestiario else []
    for p in best:
        estrai_file(p, rac, note)
    # In prosa si cercano solo le entità VERE: quelle che hanno già uno
    # statblocco o una parentesi, i PG, e l'anagrafica dei PNG di state.yaml.
    # I titoli di sezione qualunque non sono entità (ed erano il 90% del tempo).
    def leggibile(k):
        d = re.sub(r"^[A-Z]?\.?\d+[a-z]?(?:-bis)?\s*·\s*", "", note.get(k, k)).strip()
        return d.title() if d.isupper() else d
    entita = {k: leggibile(k) for k, _ in rac.occ}
    for pg in PG:
        entita.setdefault(pg.lower(), pg)
    for k, disp in nomi_state().items():
        entita.setdefault(k, disp)
    for k, disp in EVENTI.items():
        entita.setdefault(k, disp)
    testi = [p.read_text(encoding="utf-8", errors="replace") for p in files]
    alias = alias_brevi(set(entita), testi)
    for p in files + best:
        estrai_prosa(p, rac, entita, alias)
    rac.nomi.update({k: v for k, v in entita.items() if k not in rac.nomi})
    unisci_alias(rac)
    contr = rac.contraddizioni()
    # quanti attributi sono stati davvero CONFRONTATI (letti in almeno due
    # posti): senza questo numero «zero contraddizioni» non vuol dire niente
    confronti: dict[str, int] = {}
    occorrenze: dict[str, int] = {}
    for (ent, attr), valori in rac.occ.items():
        a = attr.split(" ")[0]
        tot = sum(len(o) for o in valori.values())
        occorrenze[a] = occorrenze.get(a, 0) + tot
        if tot >= 2:
            confronti[a] = confronti.get(a, 0) + 1
    per_attr: dict[str, int] = {}
    for c in contr:
        per_attr[c["attributo"].split(" ")[0]] = per_attr.get(c["attributo"].split(" ")[0], 0) + 1
    return {
        "file_letti": [_rel(p) for p in files],
        "bestiario_letti": [_rel(p) for p in best],
        "entita": len(entita),
        "attributi_estratti": sum(sum(len(o) for o in v.values()) for v in rac.occ.values()),
        "coppie_entita_attributo": len(rac.occ),
        "contraddizioni": contr,
        "per_attributo": dict(sorted(per_attr.items())),
        "occorrenze_per_attributo": dict(sorted(occorrenze.items())),
        "confrontati_per_attributo": dict(sorted(confronti.items())),
    }


# =========================================================================== #
# Uscita
# =========================================================================== #
def testo_fronti(esiti: list[dict], state: list[dict] | None) -> str:
    out = []
    for e in esiti:
        m = e["misure"]
        out.append(f"== Fronti {e['arco']}")
        if m:
            out.append(f"   fronti {m['fronti']} · orologi {m['orologi']} (conformi a O1-O2: "
                       f"{m['orologi_conformi']}) · presagi nei master {m['presagi_nei_master']}/"
                       f"{m['presagi']} · campi scritti nel master {m['campi_espliciti']}, "
                       f"dedotti {m['campi_dedotti']}")
        for v in e["violazioni"]:
            out.append(f"   ✗ {v['regola']} {v['dove']}: {v['messaggio']}")
        for p in e["presagi"]:
            segno = "✓" if p["trovato"] else "✗"
            out.append(f"   {segno} presagio [{p['fronte']}] {p['presagio'][:60]} → {p['trovato'] or '—'}")
    if state is not None:
        ok = sum(1 for s in state if s["conforme"])
        out.append(f"== Orologi dei villain in campaign/state.yaml: {ok}/{len(state)} conformi")
        for s in state:
            segno = "✓" if s["conforme"] else "✗"
            out.append(f"   {segno} {s['png_id']:<18} {s['clock'][:40]:<40} {s['motivo'] or ''}")
    return "\n".join(out)


def testo_fatti(r: dict) -> str:
    out = [f"== Fatti: {len(r['file_letti'])} file d'arco, {len(r['bestiario_letti'])} del Bestiario, "
           f"{r['entita']} entità, {r['attributi_estratti']} occorrenze, "
           f"{len(r['contraddizioni'])} contraddizioni candidate",
           f"   occorrenze per attributo: {r['occorrenze_per_attributo']}",
           f"   attributi letti in 2+ posti (confrontati): {r['confrontati_per_attributo']}",
           f"   contraddizioni per attributo: {r['per_attributo']}"]
    for c in r["contraddizioni"]:
        out.append(f"-- {c['id']} {c['entita']} · {c['attributo']}")
        for v in c["valori"]:
            o = v["occorrenze"][0]
            out.append(f"     {v['valore']:<22} ×{v['n']:<3} {o['file']}:{o['riga']}")
    return "\n".join(out)


def controlla_residui(r: dict, percorso: Path) -> int:
    """Il cancello di CI: ogni contraddizione trovata è dichiarata in RESIDUI
    (entità e attributo, con la ragione), e ogni residuo esiste ancora. Così una
    contraddizione nuova blocca, e una risolta si toglie dal file."""
    dati = json.loads(percorso.read_text(encoding="utf-8"))
    dichiarati = {(x["chiave"], x["attributo"]) for x in dati.get("residui", [])}
    trovati = {(c["chiave"], c["attributo"]): c for c in r["contraddizioni"]}
    nuove = [trovati[k] for k in trovati if k not in dichiarati]
    sparite = sorted(dichiarati - set(trovati))
    for c in nuove:
        print(f"✗ contraddizione nuova: {c['entita']} · {c['attributo']} "
              f"({', '.join(v['valore'] for v in c['valori'])})")
    for k in sparite:
        print(f"✗ residuo risolto, da togliere da {_rel(percorso)}: {k[0]} · {k[1]}")
    if nuove or sparite:
        return 1
    print(f"✓ coerenza_campagna: {len(trovati)} contraddizioni, tutte residui dichiarati")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("fronti", help="controlla file di fronti e orologi")
    a.add_argument("file", nargs="+", type=Path)
    a.add_argument("--state", action="store_true", help="misura anche gli orologi di state.yaml")
    a.add_argument("--json", action="store_true")
    b = sub.add_parser("fatti", help="contraddizioni fra scene e archi")
    b.add_argument("archi", nargs="+", type=Path)
    b.add_argument("--bestiario", action="store_true")
    b.add_argument("--tutti", action="store_true", help="legge anche i file fuori perimetro")
    b.add_argument("--json", action="store_true")
    b.add_argument("--check", type=Path, metavar="RESIDUI",
                   help="cancello: exit 1 se c'è una contraddizione che RESIDUI non "
                        "dichiara, o un residuo che non c'è più")
    c = sub.add_parser("tutto", help="fronti + fatti, e scrive JSON e riassunto in --out")
    c.add_argument("--fronti", nargs="+", type=Path, required=True)
    c.add_argument("--archi", nargs="+", type=Path, required=True)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--bestiario", action="store_true")
    c.add_argument("--rigido", action="store_true", help="exit 1 se i fronti hanno violazioni")
    args = ap.parse_args(argv)

    def carica(p: Path):
        if not p.is_file():
            print(f"✗ file non trovato: {p}", file=sys.stderr)
            raise SystemExit(2)
        return yaml.safe_load(p.read_text(encoding="utf-8"))

    for p in getattr(args, "archi", []) or []:
        if not p.is_dir():
            print(f"✗ cartella non trovata: {p}", file=sys.stderr)
            return 2

    if args.cmd == "fronti":
        esiti = [controlla_fronti(carica(p)) for p in args.file]
        state = misura_orologi_state() if args.state else None
        if args.json:
            print(json.dumps({"fronti": esiti, "orologi_state": state}, ensure_ascii=False, indent=2))
        else:
            print(testo_fronti(esiti, state))
        return 1 if any(e["violazioni"] for e in esiti) else 0

    if args.cmd == "fatti":
        r = rileva_contraddizioni(args.archi, args.bestiario, args.tutti)
        print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else testo_fatti(r))
        return controlla_residui(r, args.check) if args.check else 0

    esiti = [controlla_fronti(carica(p)) for p in args.fronti]
    state = misura_orologi_state()
    r = rileva_contraddizioni(args.archi, args.bestiario)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "coerenza.json").write_text(json.dumps(
        {"fronti": esiti, "orologi_state": state, "fatti": r},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "coerenza.txt").write_text(
        testo_fronti(esiti, state) + "\n\n" + testo_fatti(r) + "\n", encoding="utf-8")
    print(f"✓ scritti {_rel(args.out / 'coerenza.json')} e {_rel(args.out / 'coerenza.txt')}")
    return 1 if args.rigido and any(e["violazioni"] for e in esiti) else 0


if __name__ == "__main__":
    sys.exit(main())
