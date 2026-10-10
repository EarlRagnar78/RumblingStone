#!/usr/bin/env python3
"""ciclo_prosa.py — dal segnalare al correggere, con una revisione a due giri.

L12 di PIANO-AGENT-SKILLS-ESTERNE (D15 e D16 del 2026-10-02), decisione in
ADR-0077. Il modello è quello della revisione fra pari: il revisore segnala,
l'autore risponde con una riscrittura, il revisore controlla cosa è cambiato e
cosa è rimasto. Lo script fa il revisore; la riscrittura la fa un agente o una
persona; l'approvazione la dà il DM, modifica per modifica.

    python3 scripts/ciclo_prosa.py segnala FILE
        primo giro: i passaggi da correggere, con la norma e il rimedio

    python3 scripts/ciclo_prosa.py revisione ORIGINALE RISCRITTO [-o REVISIONE.md]
        la risposta dell'autore resa leggibile: ogni modifica in CriticMarkup,
        numerata, con la norma che la motiva e una casella da spuntare; e le
        due garanzie: nessun controllo peggiora, nessun fatto cambia

    python3 scripts/ciclo_prosa.py applica REVISIONE.md
        secondo giro: applica all'ORIGINALE solo le modifiche spuntate, alza la
        revisione del documento e rimisura. Non scrive su `main` (D15).

    python3 scripts/ciclo_prosa.py lotto FILE... -o CARTELLA
        prima del primo giro: per ogni file un pacchetto da riscrivere (i
        passaggi, la norma, il rimedio, cosa non si tocca, i numeri di
        partenza), e la classifica dei file per punteggio MQM

    python3 scripts/ciclo_prosa.py misura ORIGINALE RISCRITTO
        fra un giro di riscrittura e l'altro: di quanto è migliorato, norma per
        norma e in punti MQM. Esce 1 se qualcosa peggiora

    python3 scripts/ciclo_prosa.py rigenera REVISIONE.md
        quando l'originale è cambiato dopo la revisione: le stesse modifiche,
        riportate sul testo di oggi, e il documento riscritto da approvare

    python3 scripts/ciclo_prosa.py registro [--check]
        i miglioramenti applicati, uno per revisione, con il totale; `--check`
        è il cancello: nessuna revisione applicata ha peggiorato il punteggio

Da dove vengono le regole, e con che licenza (ADR-0077):

* i rilevatori del repo, già registrati: `validate_prosa` (calchi, antitesi,
  maiuscole, trattino), `misura_craft` (tetti dei box, P1, metrature),
  `voto_scrittura` («sembra»/«pare», D13);
* la regola **«debole da solo»** di Humanizer (blader/humanizer, MIT) e di
  *Wikipedia: Signs of AI writing* (CC BY-SA 4.0), di cui si adotta l'idea e non
  il testo: un tic minore, preso da solo, è italiano corretto; due tic minori
  diversi nello stesso paragrafo sono un segnale. I tic minori sono quelli che
  `italiano-nativo.md` §9.2-ter e §9.2-quater elenca e lascia, per questa
  ragione, fuori da ogni controllo;
* la sintassi di revisione **CriticMarkup** (Gabe Weatherhead ed Erik Hess,
  Apache 2.0): `{~~vecchio~>nuovo~~}`, `{++aggiunto++}`, `{--tolto--}`,
  `{>>commento<<}`. Implementata qui con `difflib`, senza codice di terzi.

Il **secondo lettore** (ADR-0079) è un passo facoltativo di `segnala`: con
`--languagetool URL` (un server LanguageTool **locale**, avviato da
`scripts/avvia_languagetool.sh`) si aggiungono le tre regole che la misura ha
tenuto. Serve quando si vuole una verifica in più su un master o su un handout,
non come cancello: non è in CI e non entra nel punteggio MQM. LanguageTool è LGPL
e resta un servizio fuori dal repo.

Solo stdlib. Deterministico: lo stesso input dà la stessa uscita.
"""
from __future__ import annotations

import argparse
import json
import statistics
import urllib.parse
import urllib.request
import difflib
import hashlib
import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import misura_craft as mc  # noqa: E402
import validate_prosa as vp  # noqa: E402
import voto_scrittura as vs  # noqa: E402

RADICE = Path(__file__).resolve().parent.parent

# ── I tic minori: italiano-nativo §9.2-ter (copula elusa, importanza dichiarata)
# e §9.2-quater (la watchlist). Ognuno da solo è lecito; il documento lo dice.
DEBOLI: "dict[str, re.Pattern]" = {
    "copula elusa": re.compile(
        r"\b(?:si configura come|funge da|si pone come|rappresenta|costituisce)\b", re.I),
    "importanza dichiarata": re.compile(
        r"\b(?:testimonianza (?:di|vivente)|punto di svolta|simbolo eterno|"
        r"a imperitura memoria)\b", re.I),
    "watchlist": re.compile(
        r"\b(?:un vero e proprio|una vera e propria|nel cuore di|non è un caso che|"
        r"gioca un ruolo fondamentale|un tassello|connubio|risuona di|si staglia contro)\b",
        re.I),
    "sembra/pare": vs.SEMBRA,
    "antitesi": vp.ANTITESI,
    "trattino come respiro": vp.TRATTINO,
}
SOGLIA_DEBOLI = 2   # tic minori DIVERSI nello stesso paragrafo (Humanizer, «weak alone»)

RIMEDI = {
    "calco": "riscrivere all'italiana (italiano-nativo §1)",
    "P1": "il box dice cosa c'è; il gesto o la sensazione a un PNG o al mondo (read-aloud-adulti §1.6)",
    "metratura": "la misura va nei dati per il DM; nel box un paragone (ADR-0014)",
    "box oltre 12 righe": "spezzare in due box o tagliare (read-aloud-adulti §2)",
    "box con parentesi": "togliere la parentesi: all'orale non esiste (read-aloud-adulti §1.3)",
    "box con più nomi propri": "un solo nome nuovo per box (read-aloud-adulti §1.1)",
    "sembra/pare": "dire cosa c'è, o descrivere la cosa che non torna (D13)",
    "tic minori in gruppo": "riscrivere il paragrafo: presi insieme suonano generati (italiano-nativo §9)",
}


@dataclass
class Segnalazione:
    riga: int          # 1-based, la prima riga del passaggio
    fine: int          # 1-based, inclusa
    norma: str
    dettaglio: str

    @property
    def rimedio(self) -> str:
        return RIMEDI.get(self.norma, "")


def _paragrafi(righe: "list[str]") -> "list[tuple[int, int]]":
    """(inizio, fine) 0-based, inclusi, delle unità di prosa.

    Un'unità finisce a una riga vuota, a un titolo, a una voce d'elenco nuova;
    le tabelle e i blocchi di codice non sono prosa e restano fuori. Un elenco
    di trenta voci sono trenta unità, non un paragrafo.
    """
    out, inizio, codice = [], None, False

    def chiudi(fine):
        nonlocal inizio
        if inizio is not None and fine >= inizio:
            out.append((inizio, fine))
        inizio = None

    for i, r in enumerate(righe):
        t = r.strip().lstrip("> ").strip()
        if r.strip().startswith("```"):
            chiudi(i - 1)
            codice = not codice
            continue
        if codice or not t or t.startswith(("|", "#")):
            chiudi(i - 1)
            continue
        if re.match(r"(?:[-*+]|\d+[.)])\s", t):
            chiudi(i - 1)
        if inizio is None:
            inizio = i
    chiudi(len(righe) - 1)
    return out


def tic_deboli(blocco: str) -> "list[str]":
    """I tic minori DIVERSI di un'unità di prosa, ognuno su un tratto di testo suo.

    Un'antitesi «Non è X: è Y» scritta col trattino è un tic, non due: un tic
    conta solo se ha almeno un'occorrenza che non sta tutta dentro
    un'occorrenza di un altro tic.
    """
    trovate = {n: [m.span() for m in rx.finditer(blocco)] for n, rx in DEBOLI.items()}
    fuori = []
    for n, spans in trovate.items():
        altre = [sp for k, v in trovate.items() if k != n for sp in v]
        if any(not any(a2 <= a and b <= b2 for a2, b2 in altre) for a, b in spans):
            fuori.append(n)
    return sorted(fuori)


def _box_con_righe(testo: str) -> "list[tuple[int, int, list[str]]]":
    """I box di `misura_craft.box_read_aloud`, con la riga d'inizio e di fine (0-based)."""
    righe, out, da = testo.splitlines(), [], 0
    for b in mc.box_read_aloud(testo):
        i0 = next(i for i in range(da, len(righe)) if righe[i:i + len(b)] == b)
        out.append((i0, i0 + len(b) - 1, b))
        da = i0 + len(b)
    return out


def _riga_di(rx: re.Pattern, box: "list[str]", i0: int) -> "int | None":
    """La riga (1-based) del box dove il rilevatore scatta; None se la parola va a capo."""
    for k, r in enumerate(box):
        if rx.search(mc._ETICHETTA.sub("", r)):
            return i0 + k + 1
    return None


def segnala(testo: str) -> "list[Segnalazione]":
    righe = testo.splitlines()
    fuori: "list[Segnalazione]" = []

    spans = _box_con_righe(testo)
    dentro_box = {i for i0, i1, _ in spans for i in range(i0, i1 + 1)}

    # i calchi, riga per riga, con le regex di validate_prosa
    for i, r in enumerate(righe):
        regole = list(vp.CALCHI_SEMPRE) + (list(vp.CALCHI_READ_ALOUD) if i in dentro_box else [])
        for pattern, perche in regole:
            m = re.search(pattern, r, re.I)
            if m:
                fuori.append(Segnalazione(i + 1, i + 1, "calco", f"«{m.group(0)}»: {perche}"))

    # i box, con i rilevatori di misura_craft e voto_scrittura
    for i0, i1, b in spans:
        corpo = mc._ETICHETTA.sub("", " ".join(b))
        if len(b) > mc.TETTO_RIGHE:
            fuori.append(Segnalazione(i0 + 1, i1 + 1, "box oltre 12 righe", f"{len(b)} righe"))
        if "(" in corpo:
            fuori.append(Segnalazione(i0 + 1, i1 + 1, "box con parentesi", ""))
        nomi = mc.nomi_propri(corpo) - set(mc.PG)   # i PG il tavolo li conosce già
        if len(nomi) > 1:
            fuori.append(Segnalazione(i0 + 1, i1 + 1, "box con più nomi propri", ", ".join(sorted(nomi))))
        for norma, rx in (("P1", mc.P1), ("metratura", mc.METRATURA)):
            m = rx.search(corpo)
            if m:
                r = _riga_di(rx, b, i0)
                fuori.append(Segnalazione(r or i0 + 1, r or i1 + 1, norma, f"«{m.group(0).strip()}»"))
        esitanti = vs.sembra_esitanti(corpo)   # D17: il «sembra» smentito resta
        if esitanti:
            m = esitanti[0]
            r = _riga_di(re.compile(r"\b" + re.escape(m.group(0)) + r"\b", re.I), b, i0)
            fuori.append(Segnalazione(r or i0 + 1, r or i1 + 1, "sembra/pare", f"«{m.group(0).strip()}»"))

    # i tic minori in gruppo, paragrafo per paragrafo
    for p0, p1 in _paragrafi(righe):
        blocco = mc._ETICHETTA.sub("", " ".join(righe[p0:p1 + 1]))
        trovati = tic_deboli(blocco)
        if len(trovati) >= SOGLIA_DEBOLI:
            fuori.append(Segnalazione(p0 + 1, p1 + 1, "tic minori in gruppo", ", ".join(trovati)))

    return sorted(fuori, key=lambda s: (s.riga, s.norma))


# ── le garanzie ──────────────────────────────────────────────────────────────
_NOMI: "set[str] | None" = None


def _registro() -> "set[str]":
    """I nomi propri della campagna, letti una volta (misura_craft: Bestiario + state.md)."""
    global _NOMI
    if _NOMI is None:
        _NOMI = mc._registro_dei_nomi()
    return _NOMI


_NUMERO = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?")
_CD = re.compile(r"\bCD\s*\d+")


def fatti(testo: str) -> "dict[str, Counter]":
    """Ciò che una correzione di stile non deve toccare (Humanizer: non inventare)."""
    return {
        "nomi propri": Counter(w for w in re.findall(r"[A-ZÀ-Ù][a-zà-ù']{2,}", testo)
                               if w in _registro()),
        "numeri": Counter(_NUMERO.findall(testo)),
        "CD": Counter(c.replace(" ", "") for c in _CD.findall(testo)),
    }


def misure(testo: str) -> "Counter":
    """Il conto delle segnalazioni per norma: un controllo peggiora se cresce."""
    return Counter(s.norma for s in segnala(testo))


def confronta_fatti(prima: str, dopo: str) -> "list[str]":
    a, b = fatti(prima), fatti(dopo)
    out = []
    for chiave in a:
        tolti, aggiunti = a[chiave] - b[chiave], b[chiave] - a[chiave]
        if tolti or aggiunti:
            out.append(f"{chiave}: tolti {dict(tolti) or '-'}, aggiunti {dict(aggiunti) or '-'}")
    return out


# ── la lettura: misure che non giudicano, ma si confrontano ─────────────────
_FRASE = re.compile(r"[^.!?…]+[.!?…]+[»\"]?|[^.!?…]+$")


def _testo_da_leggere(testo: str) -> str:
    """I box, se ce ne sono (si leggono ad alta voce); altrimenti la prosa senza tabelle né codice."""
    box = mc.box_read_aloud(testo)
    if box:
        return " ".join(mc._APERTURE.sub("", mc._ETICHETTA.sub("", " ".join(b))) for b in box)
    righe = testo.splitlines()
    return " ".join(mc._APERTURE.sub("", " ".join(righe[a:b + 1])) for a, b in _paragrafi(righe))


def lettura(testo: str) -> "dict[str, float]":
    """Indice Gulpease (GULP, Sapienza 1988: 89 + (300·frasi − 10·lettere)/parole) e ritmo.

    Il **ritmo** è il coefficiente di variazione della lunghezza delle frasi:
    vicino a zero, tutte le frasi sono lunghe uguali (il ritmo piatto che
    Humanizer elenca fra i segni del testo generato); `italiano-nativo` §4 vuole
    l'alternanza. Nessuna delle due misure dice se la prosa è bella: dicono se
    la riscrittura l'ha resa più difficile da seguire a voce o più monotona.
    """
    t = _testo_da_leggere(testo)
    parole = re.findall(r"[A-Za-zÀ-ÿ'’]+", t)
    frasi = [f for f in _FRASE.findall(t) if re.search(r"\w", f)]
    if not parole or not frasi:
        return {"gulpease": 0.0, "ritmo": 0.0, "frasi": 0}
    lettere = sum(len(w.replace("'", "").replace("’", "")) for w in parole)
    lunghe = [len(re.findall(r"[A-Za-zÀ-ÿ'’]+", f)) for f in frasi]
    cv = statistics.pstdev(lunghe) / statistics.mean(lunghe) if len(lunghe) > 1 else 0.0
    g = 89 + (300 * len(frasi) - 10 * lettere) / len(parole)
    return {"gulpease": round(min(100.0, max(0.0, g)), 1),     # la scala è 0-100
            "ritmo": round(cv, 2), "frasi": len(frasi)}


#: Le sole regole di LanguageTool che la misura ha tenuto (ADR-0079): su 94.755
#: rilievi del repo, tutte le altre erano rumore (gergo, inglese degli statblock,
#: nomi). Ognuna ha trovato almeno un difetto vero che le altre vie non vedono.
REGOLE_LANGUAGETOOL = (
    "ARTICOLATA_SOSTANTIVO",        # il genere di un nome proprio che oscilla (*del Mano Rossa*)
    "UNPAIRED_BRACKETS",            # una parentesi senza la sua compagna
    "ITALIAN_WORD_REPEAT_RULE",     # *Solo solo nella Torre*
)
_LOCALI = ("localhost", "127.0.0.1", "::1", "[::1]")


def testo_piano(testo: str) -> str:
    """Il markdown come testo da correggere, **una riga per riga sorgente**.

    Così il numero di riga di LanguageTool è quello del file. Tabelle, codice,
    front matter e HTML diventano righe vuote; il codice in linea diventa `§`, che
    non è una parola: con una lettera, «X X» scatterebbe come parola ripetuta.
    """
    out, codice, fm = [], False, False
    for i, r in enumerate(testo.split("\n")):
        if i == 0 and r.strip() == "---":
            fm = True
            out.append("")
            continue
        if fm:
            fm = r.strip() != "---"
            out.append("")
            continue
        if r.lstrip().startswith("```"):
            codice = not codice
            out.append("")
            continue
        if codice or re.match(r"^\s*(\||<|!--|\[.*\]:|-{3,}|={3,})", r):
            out.append("")
            continue
        r = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", r)
        r = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", r)
        r = re.sub(r"`[^`]*`", "§", r)
        r = re.sub(r"^\s*(#{1,6}\s+|>\s?|[-*+]\s+|\d+\.\s+)+", "", r)
        r = re.sub(r"(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1", r"\2", r).replace("**", "")
        out.append(r)
    return "\n".join(out)


def languagetool(testo: str, url: str) -> "list[Segnalazione]":
    """Il **secondo lettore**: le tre regole tenute di un server LanguageTool (LGPL).

    Si usa quando serve una verifica in più, **non** in CI e non di default
    (ADR-0079): è un servizio, quindi la sua licenza non entra nel repo, e deve
    stare **in locale**. Un indirizzo che non sia `localhost` o `127.0.0.1` è
    rifiutato: il testo della campagna non esce dalla macchina. Senza server,
    avvisa e non segnala niente. Lo avvia `scripts/avvia_languagetool.sh`.
    """
    host = urllib.parse.urlsplit(url).hostname or ""
    if host not in _LOCALI and f"[{host}]" not in _LOCALI:
        print(f"⚠️ LanguageTool rifiutato ({url}): solo un server locale, il testo non esce dalla macchina")
        return []
    piano = testo_piano(testo)
    dati = urllib.parse.urlencode({
        "text": piano, "language": "it", "enabledOnly": "true",
        "enabledRules": ",".join(REGOLE_LANGUAGETOOL)}).encode()
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/v2/check", dati, timeout=60) as r:
            risposta = json.load(r)
    except (OSError, ValueError) as e:
        print(f"⚠️ LanguageTool non raggiungibile ({e}): nessun secondo lettore")
        return []
    u = piano.encode("utf-16-le")        # gli offset di LanguageTool sono unità UTF-16
    fuori = []
    for m in risposta.get("matches", []):
        # un'emoji vale due unità: con `piano.count` la riga scivolerebbe in avanti
        prima = u[:2 * m.get("offset", 0)].decode("utf-16-le", "replace")
        riga = prima.count("\n") + 1
        proposta = ", ".join(x["value"] for x in m.get("replacements", [])[:3])
        regola = m.get("rule", {}).get("id", "")
        fuori.append(Segnalazione(riga, riga, "secondo lettore",
                                  f"{regola}: {m.get('message', '')}"
                                  + (f" → {proposta}" if proposta else "")))
    return fuori


# ── la revisione in CriticMarkup ─────────────────────────────────────────────
_PAROLA = re.compile(r"\s+|[^\s]+")
_PONTE = 3   # parole uguali al massimo fra due modifiche che si leggono come una


def _gruppi(a: "list[str]", b: "list[str]") -> "list[tuple[bool, int, int, int, int]]":
    """Il diff per parole, con le modifiche vicine fuse in una.

    Un revisore approva una frase, non una parola: due cambi separati da tre
    parole o meno, senza una fine di frase o un a capo doppio in mezzo, sono
    una modifica sola. Ogni gruppo è (cambiato?, i1, i2, j1, j2).
    """
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    out: "list[list]" = []
    for k, (op, i1, i2, j1, j2) in enumerate(ops):
        cambiato = op != "equal"
        if not cambiato:
            ponte = "".join(a[i1:i2])
            fra_due = 0 < k < len(ops) - 1 and bool(out) and out[-1][0]
            if fra_due and len(ponte.split()) <= _PONTE and not re.search(r"[.!?…]\s|\n\s*\n", ponte):
                cambiato = True          # il ponte entra nella modifica
        if out and out[-1][0] == cambiato and cambiato:
            out[-1][2], out[-1][4] = i2, j2
        else:
            out.append([cambiato, i1, i2, j1, j2])
    return [tuple(g) for g in out]




@dataclass
class Modifica:
    numero: int
    riga: int
    vecchio: str
    nuovo: str
    norme: "list[str]" = field(default_factory=list)

    def critic(self) -> str:
        if not self.vecchio:
            return "{++" + self.nuovo + "++}"
        if not self.nuovo:
            return "{--" + self.vecchio + "--}"
        return "{~~" + self.vecchio + "~>" + self.nuovo + "~~}"


def _modifiche(prima: str, dopo: str, segnalazioni: "list[Segnalazione]") -> "tuple[list[Modifica], str]":
    """Le modifiche, fuse in frasi, e il testo con i segni CriticMarkup.

    La norma di una modifica è quella che **risolve**: il conto che scende
    quando la si applica da sola. Se non ne risolve nessuna, è la norma
    segnalata sulla sua stessa riga; altrimenti la modifica non è motivata.
    Attribuire tutte le norme del box sarebbe rumore: un «sembra» corretto non
    toglie la parentesi tre righe sotto.
    """
    diff = _diff_di(prima, dopo)
    a, b, gruppi = diff
    m0 = misure(prima)
    mods, pezzi, riga = [], [], 1
    for cambiato, i1, i2, j1, j2 in gruppi:
        if not cambiato:
            uguale = "".join(a[i1:i2])
            pezzi.append(uguale)
            riga += uguale.count("\n")
            continue
        vecchio, nuovo = "".join(a[i1:i2]), "".join(b[j1:j2])
        fine = riga + vecchio.count("\n")
        m = Modifica(len(mods) + 1, riga, vecchio, nuovo, [])
        mods.append(m)
        pezzi.append(m.critic() + "{>>#" + str(m.numero) + "<<}")
        riga = fine
    for m in mods:
        m1 = misure(applica_testo(prima, dopo, {m.numero}, diff))
        risolte = sorted(k for k in m0 if m1[k] < m0[k])
        fine = m.riga + m.vecchio.count("\n")
        sulla_riga = sorted({s.norma for s in segnalazioni
                             if s.riga == s.fine and m.riga <= s.riga <= fine})
        m.norme = risolte or sulla_riga
    return mods, "".join(pezzi)


def _rel(p: Path) -> str:
    p = p.resolve()
    try:
        return p.relative_to(RADICE).as_posix()
    except ValueError:
        return p.as_posix()


def _nel_repo(p: Path) -> str:
    """Il riscritto serve solo a fare il documento: fuori dal repo non si nomina."""
    r = _rel(p)
    return r if not Path(r).is_absolute() else "nel documento"


def _assoluto(s: str) -> Path:
    p = Path(s)
    return p if p.is_absolute() else RADICE / p


def _impronta(prima: str, dopo: str) -> str:
    """Le modifiche sono numerate sul diff: se uno dei due testi cambia, i numeri non valgono più."""
    return hashlib.sha256((prima + "\0" + dopo).encode("utf-8")).hexdigest()[:16]


#: Quanto può scendere la lettura per una modifica applicata senza lettore. Un
#: punto Gulpease è una parola lunga in più in un box; 0,05 di ritmo è una
#: frase che si allunga. Oltre, la modifica va guardata da qualcuno.
TOLLERANZA_GULPEASE = 1.0
TOLLERANZA_RITMO = 0.05


def automatiche(prima: str, dopo: str, mods: "list[Modifica]") -> "set[int]":
    """Le modifiche che si possono applicare senza un lettore.

    Quattro condizioni, ognuna sulla modifica **presa da sola**: è motivata da
    una segnalazione; non cambia un fatto (nomi propri, numeri, CD); non fa
    crescere il conto di nessuna norma, e ne fa scendere almeno uno; non rende
    la lettura più dura né più piatta oltre la tolleranza. Le altre restano al DM.
    """
    m0, l0 = misure(prima), lettura(prima)
    diff = _diff_di(prima, dopo)          # una volta: su un master di 2.600 righe costa minuti
    ok = set()
    for m in mods:
        if not m.norme:
            continue
        solo = applica_testo(prima, dopo, {m.numero}, diff)
        if confronta_fatti(prima, solo):
            continue
        m1 = misure(solo)
        l1 = lettura(solo)
        lettura_ok = (l1["gulpease"] >= l0["gulpease"] - TOLLERANZA_GULPEASE
                      and l1["ritmo"] >= l0["ritmo"] - TOLLERANZA_RITMO)
        if all(m1[k] <= m0[k] for k in m1) and sum(m1.values()) < sum(m0.values()) and lettura_ok:
            ok.add(m.numero)
    return ok


_SEGNI = re.compile(r"\{(?:~~|\+\+|--|>>|==)")
_MARCA = re.compile(r"\{~~(?P<v>.*?)~>(?P<n>.*?)~~\}\{>>#\d+<<\}|"
                    r"\{\+\+(?P<a>.*?)\+\+\}\{>>#\d+<<\}|"
                    r"\{--(?P<t>.*?)--\}\{>>#\d+<<\}", re.S)


def dal_markup(marcato: str) -> "tuple[str, str]":
    """Le due versioni, ricostruite dal testo in CriticMarkup del documento.

    Il documento di revisione basta a se stesso: chi lo approva non deve
    tenere accanto una seconda copia del master.
    """
    prima, dopo, da = [], [], 0
    for m in _MARCA.finditer(marcato):
        uguale = marcato[da:m.start()]
        prima.append(uguale)
        dopo.append(uguale)
        if m.group("v") is not None:
            prima.append(m.group("v"))
            dopo.append(m.group("n"))
        elif m.group("a") is not None:
            dopo.append(m.group("a"))
        else:
            prima.append(m.group("t"))
        da = m.end()
    prima.append(marcato[da:])
    dopo.append(marcato[da:])
    return "".join(prima), "".join(dopo)


def _marcato_del_documento(rev: str) -> str:
    i = rev.index("````markdown\n") + len("````markdown\n")
    j = rev.rindex("\n````")
    return rev[i:j]


def revisione(originale: Path, riscritto: Path) -> "tuple[str, bool]":
    prima = originale.read_text(encoding="utf-8")
    dopo = riscritto.read_text(encoding="utf-8")
    if _SEGNI.search(prima) or _SEGNI.search(dopo):
        raise ValueError("il testo contiene già segni CriticMarkup: la revisione non sarebbe reversibile")
    seg = segnala(prima)
    mods, marcato = _modifiche(prima, dopo, seg)
    m0, m1 = misure(prima), misure(dopo)
    peggiorate = sorted(k for k in m1 if m1[k] > m0[k])
    fatti_cambiati = confronta_fatti(prima, dopo)
    non_motivate = [m.numero for m in mods if not m.norme]
    auto = automatiche(prima, dopo, mods)
    l0, l1 = lettura(prima), lettura(dopo)
    mig = miglioramento(prima, dopo, originale)
    mqm_scende = bool(mig["mqm"]) and mig["mqm"][1] < mig["mqm"][0]
    ok = not peggiorate and not fatti_cambiati and not mqm_scende

    r = [f"# Revisione · {originale.name}", "",
         f'<!-- revisione: originale="{_rel(originale)}" riscritto="{_nel_repo(riscritto)}" '
         f'impronta="{_impronta(prima, dopo)}" -->', "",
         "Si approva modifica per modifica: spuntare `[x]` nella colonna «ok», poi",
         f"`python3 scripts/ciclo_prosa.py applica {{questo file}}`. Le modifiche non spuntate",
         "restano come nell'originale. Con `--auto` si applicano anche quelle che la",
         "colonna «auto» segna: motivate, e che da sole non cambiano un fatto né",
         "peggiorano un controllo.", "",
         "## Le garanzie", "",
         f"- **Nessun controllo peggiora**: {'sì' if not peggiorate else 'NO, peggiorano ' + ', '.join(peggiorate)}",
         f"- **Nessun fatto cambia** (nomi propri, numeri, CD): {'sì' if not fatti_cambiati else 'NO'}"]
    r += [f"  - {x}" for x in fatti_cambiati]
    if mig["mqm"]:
        r.append(f"- **Il punteggio MQM non scende**: {'sì' if not mqm_scende else 'NO'} "
                 f"({mig['mqm'][0]} → {mig['mqm'][1]})")
    r += [f"- **Segnalazioni**: {sum(m0.values())} prima, {sum(m1.values())} dopo",
          f"- **Modifiche non motivate da una segnalazione**: {len(non_motivate)}"
          + (f" (#{', #'.join(map(str, non_motivate))}): vanno guardate per prime" if non_motivate else ""),
          f"- **Applicabili senza lettore**: {len(auto)} su {len(mods)}",
          "", "## Di quanto migliora", "",
          "Con tutte le modifiche applicate. Il punteggio MQM pesa le norme registrate",
          "per severità (ADR-0059); le segnalazioni le contano norma per norma. Un",
          "numero che sale vuol dire più norme rispettate, non una prosa più bella.", ""]
    r += tabella_miglioramento(mig)
    r += ["", "## La lettura, prima e dopo", "",
          "Non dicono se la prosa è bella: dicono se la riscrittura l'ha resa più dura",
          "da seguire a voce o più monotona. Il giudizio resta di chi legge ad alta voce.", "",
          "| misura | prima | dopo | si vuole |", "|---|---:|---:|---|",
          f"| Gulpease (0-100) | {l0['gulpease']} | {l1['gulpease']} | non scendere: un box si capisce al primo ascolto |",
          f"| ritmo (variazione delle frasi) | {l0['ritmo']} | {l1['ritmo']} | non scendere: frasi tutte uguali sono un ritmo piatto |",
          f"| frasi | {l0['frasi']} | {l1['frasi']} | |",
          "", "## Le modifiche", "",
          "| ok | # | riga | prima | dopo | norma | auto |", "|---|---:|---:|---|---|---|:---:|"]

    def cella(s: str) -> str:
        if s and not s.strip(" >\n"):          # solo a capo: si mostra com'è
            return s.replace(" ", "").replace("\n", "⏎")
        s = " ".join(s.split())
        return (s[:70] + "…" if len(s) > 70 else s).replace("|", "\\|") or "∅"

    for m in mods:
        r.append(f"| [ ] | {m.numero} | {m.riga} | {cella(m.vecchio)} | {cella(m.nuovo)} | "
                 f"{', '.join(m.norme) or '⚠️ non motivata'} | {'✓' if m.numero in auto else '—'} |")
    r += ["", "## Il testo con le modifiche (CriticMarkup)", "",
          "Il testo intero, con le due versioni dentro: `applica` le ricostruisce da qui.", "",
          "<details><summary>apri il testo marcato</summary>", "",
          "````markdown", marcato, "````", "", "</details>", ""]
    return "\n".join(r), ok


# ── il miglioramento: di quanto, non solo «non peggiora» (ADR-0077, estensione) ──
#: Il registro dei miglioramenti applicati: una riga per revisione applicata.
REGISTRO = RADICE / "plans" / "scrittura" / "miglioramenti.json"

#: I master già letti al tavolo: lì una revisione spezza i box e non cambia una
#: parola (D9 di PIANO-LETTORE-E-PLAYTESTER, 2026-09-30). Il pacchetto lo dice.
GIA_GIOCATI = ("ARC07-DEF-1-", "ARC07-DEF-2-", "ARC07-DEF-3-")

#: Quando ci si ferma: dopo un giro che non abbassa le segnalazioni, o al terzo.
#: Senza un tetto «il più possibile» diventa riscrivere per il gusto di farlo.
GIRI_MASSIMI = 3


def mqm(testo: str, percorso: Path) -> "dict | None":
    """Il punteggio MQM di `testo` come se fosse `percorso` (ADR-0059).

    `punteggio_mqm` legge un file: il testo riscritto si scrive in una cartella
    temporanea con lo stesso nome, e la classe si prende dal percorso vero.
    None se le specifiche non ci sono (il ciclo funziona anche senza).
    """
    try:
        import punteggio_mqm as pm
        spec = pm.carica_specifiche()
    except (ImportError, SystemExit):  # pragma: no cover — senza pyyaml o specifiche
        return None
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / percorso.name
        tmp.write_text(testo, encoding="utf-8")
        e = pm.valuta(tmp, spec)
    e["file"] = _rel(percorso)
    e["classe"] = pm.classe_di(_assoluto(str(percorso)), spec)
    return e


def miglioramento(prima: str, dopo: str, percorso: Path) -> dict:
    """Di quanto la riscrittura ha migliorato il testo, misurato.

    Tre misure, e nessuna dice se la prosa è bella: le segnalazioni norma per
    norma (quante norme registrate il testo rispetta in più), il punteggio MQM
    (le stesse norme pesate per severità, ISO 5060), e la lettura (che non sia
    diventata più dura o più piatta). Il giudizio resta di chi legge a voce.
    """
    m0, m1 = misure(prima), misure(dopo)
    q0, q1 = mqm(prima, percorso), mqm(dopo, percorso)
    l0, l1 = lettura(prima), lettura(dopo)
    norme = sorted(set(m0) | set(m1))
    return {
        "norme": {n: [m0[n], m1[n]] for n in norme},
        "segnalazioni": [sum(m0.values()), sum(m1.values())],
        "mqm": [q0["punteggio"], q1["punteggio"]] if q0 and q1 else None,
        "penalita": [q0["penalita"], q1["penalita"]] if q0 and q1 else None,
        "gulpease": [l0["gulpease"], l1["gulpease"]],
        "ritmo": [l0["ritmo"], l1["ritmo"]],
    }


def peggiora(mig: dict) -> "list[str]":
    """Le misure che la riscrittura ha peggiorato: vuoto vuol dire promossa."""
    fuori = [f"{n} {a} → {b}" for n, (a, b) in mig["norme"].items() if b > a]
    if mig["mqm"] and mig["mqm"][1] < mig["mqm"][0]:
        fuori.append(f"MQM {mig['mqm'][0]} → {mig['mqm'][1]}")
    return fuori


def tabella_miglioramento(mig: dict) -> "list[str]":
    r = ["| misura | prima | dopo | Δ |", "|---|---:|---:|---:|"]
    if mig["mqm"]:
        a, b = mig["mqm"]
        r.append(f"| **punteggio MQM** (0-100, ISO 5060) | {a} | {b} | {b - a:+.2f} |")
        pa, pb = mig["penalita"]
        r.append(f"| penalità MQM (minore 1, maggiore 5) | {pa} | {pb} | {pb - pa:+d} |")
    a, b = mig["segnalazioni"]
    r.append(f"| **segnalazioni** | {a} | {b} | {b - a:+d} |")
    for n, (a, b) in mig["norme"].items():
        r.append(f"| · {n} | {a} | {b} | {b - a:+d} |")
    return r


def misura_cmd(originale: Path, riscritto: Path) -> int:
    prima = originale.read_text(encoding="utf-8")
    dopo = riscritto.read_text(encoding="utf-8")
    mig = miglioramento(prima, dopo, originale)
    print("\n".join(tabella_miglioramento(mig)))
    fatti_cambiati = confronta_fatti(prima, dopo)
    for x in fatti_cambiati:
        print(f"✗ fatto cambiato: {x}")
    male = peggiora(mig)
    for x in male:
        print(f"✗ peggiora: {x}")
    rimaste = segnala(dopo)
    print(f"{'✓' if not male and not fatti_cambiati else '✗'} restano {len(rimaste)} segnalazioni")
    if mig["segnalazioni"][1] >= mig["segnalazioni"][0]:
        print("  questo giro non ha abbassato le segnalazioni: ci si ferma qui (GIRI_MASSIMI, ADR-0077)")
    return 1 if male or fatti_cambiati else 0


def _estratto(righe: "list[str]", s: Segnalazione) -> str:
    testo = " ".join(r.strip() for r in righe[s.riga - 1:s.fine])
    testo = " ".join(testo.split())
    return (testo[:220] + "…") if len(testo) > 220 else testo


def pacchetto(percorso: Path) -> "tuple[str, dict]":
    """Il pacchetto di un file: quello che serve a chi riscrive, e niente altro."""
    testo = percorso.read_text(encoding="utf-8")
    righe = testo.splitlines()
    seg = segnala(testo)
    q = mqm(testo, percorso)
    lt = lettura(testo)
    f = fatti(testo)
    giocato = any(percorso.name.startswith(g) for g in GIA_GIOCATI)
    rel = _rel(percorso)
    r = [f"# Pacchetto di riscrittura · {percorso.name}", "",
         f"<!-- pacchetto: originale=\"{rel}\" -->", "",
         "Si riscrivono **solo** i passaggi qui sotto, e solo quanto basta a",
         "togliere la segnalazione. Prima di scrivere si leggono i `references/` di",
         "`rumblingstone-narrative-style` (AGENTS.md G1): `italiano-nativo.md`,",
         "`read-aloud-adulti.md`, `editorial-standards.md`, `style-pillars.md`.", ""]
    if giocato:
        r += ["⚠️ **Master già letto al tavolo (D9).** I box si spezzano e basta: nessuna",
              "parola cambia. Le segnalazioni che chiedono di riscrivere restano al DM.", ""]
    r += ["## Da che numero si parte", "",
          "| misura | valore |", "|---|---:|"]
    if q:
        r += [f"| punteggio MQM | {q['punteggio']} |", f"| penalità MQM | {q['penalita']} |"]
    r += [f"| segnalazioni | {len(seg)} |", f"| Gulpease | {lt['gulpease']} |",
          f"| ritmo | {lt['ritmo']} |", "",
          "## Cosa non si tocca", "",
          f"Nomi propri ({len(f['nomi propri'])} diversi), numeri ({len(f['numeri'])}) e CD",
          f"({len(f['CD'])}): `revisione` confronta i tre insiemi e blocca la modifica",
          "che ne cambia uno. Una frase senza segnalazione resta com'è.", "",
          "## I passaggi", "",
          "| # | righe | norma | rimedio | il testo |", "|---:|---|---|---|---|"]
    for i, s in enumerate(seg, 1):
        estratto = _estratto(righe, s).replace("|", "\\|")
        r.append(f"| {i} | {s.riga}-{s.fine} | {s.norma} {s.dettaglio} | {s.rimedio} | {estratto} |")
    r += ["", "## Il giro", "",
          "```bash",
          f"cp '{rel}' /tmp/riscritto.md         # si riscrive la copia, mai l'originale",
          f"python3 scripts/ciclo_prosa.py misura '{rel}' /tmp/riscritto.md",
          "# … si ritocca quello che resta, e si rimisura",
          f"python3 scripts/ciclo_prosa.py revisione '{rel}' /tmp/riscritto.md -o REVISIONE.md",
          "```", "",
          f"Ci si ferma quando un giro non abbassa le segnalazioni, o al giro {GIRI_MASSIMI}.",
          "Il documento di revisione va al DM, che approva modifica per modifica (D15).", ""]
    riassunto = {"file": rel, "segnalazioni": len(seg), "giocato": giocato,
                 "mqm": q["punteggio"] if q else None, "penalita": q["penalita"] if q else None}
    return "\n".join(r), riassunto


def lotto(files: "list[Path]", uscita: Path) -> int:
    uscita.mkdir(parents=True, exist_ok=True)
    righe = []
    for f in files:
        testo, rias = pacchetto(f)
        if rias["segnalazioni"]:         # un file pulito sta nella classifica, non ha pacchetto
            (uscita / f"PACCHETTO-{f.stem}.md").write_text(testo, encoding="utf-8")
        righe.append(rias)
    righe.sort(key=lambda x: (x["mqm"] if x["mqm"] is not None else 100, -x["segnalazioni"]))
    indice = ["# Lotto di riscrittura", "",
              "I file in ordine di punteggio MQM, dal peggiore. I master già letti al",
              "tavolo (D9) si spezzano e non si riscrivono.", "",
              "| file | MQM | penalità | segnalazioni | al tavolo |", "|---|---:|---:|---:|:---:|"]
    for x in righe:
        indice.append(f"| `{x['file']}` | {x['mqm']} | {x['penalita']} | {x['segnalazioni']} | "
                      f"{'sì' if x['giocato'] else ''} |")
    (uscita / "LOTTO.md").write_text("\n".join(indice) + "\n", encoding="utf-8")
    print("\n".join(indice))
    print(f"\n✓ {sum(1 for x in righe if x['segnalazioni'])} pacchetti in {_rel(uscita)}, "
          f"{sum(1 for x in righe if not x['segnalazioni'])} file già puliti")
    return 0


#: Quanti caratteri di testo uguale, prima di una modifica, la ritrovano
#: nell'originale cambiato. Pochi pescano due posti, troppi non pescano niente
#: se l'originale è cambiato proprio lì vicino.
CONTESTO = 25


def rigenera_testo(rev_md: str, oggi: str) -> "tuple[str | None, str]":
    """Le modifiche di una revisione, riportate su `oggi` (l'originale cambiato).

    Ogni modifica si ritrova dal testo che la precede (CONTESTO caratteri, già
    nella versione riscritta) più il testo che toglie: se quella stringa non
    compare una volta sola nell'originale di oggi, non si indovina. Restituisce
    (riscritto, "") oppure (None, il motivo).
    Nato dal lotto D13 del 2026-10-03: DEF-4 e ARC08-01 erano cambiati dopo la
    revisione, e `applica` giustamente rifiutava.
    """
    marcato = _marcato_del_documento(rev_md)
    fatto, da, cur = [], 0, oggi
    for m in _MARCA.finditer(marcato):
        uguale = marcato[da:m.start()]
        fatto.append(uguale)
        if m.group("v") is not None:
            vecchio, nuovo = m.group("v"), m.group("n")
        elif m.group("a") is not None:
            vecchio, nuovo = "", m.group("a")
        else:
            vecchio, nuovo = m.group("t"), ""
        sinistra = "".join(fatto)[-CONTESTO:]
        chiave = sinistra + vecchio
        n = cur.count(chiave)
        if n != 1:
            return None, (f"la modifica «{vecchio[:40]}» → «{nuovo[:40]}» compare {n} volte "
                          "nel testo di oggi: non si riporta da sola")
        cur = cur.replace(chiave, sinistra + nuovo)
        fatto.append(nuovo)
        da = m.end()
    return cur, ""


def rigenera(percorso_rev: Path) -> int:
    rev = percorso_rev.read_text(encoding="utf-8")
    m = _TESTA.search(rev)
    if not m:
        print("✗ non è un file di revisione: manca la riga di testa")
        return 2
    originale = _assoluto(m.group("o"))
    oggi = originale.read_text(encoding="utf-8")
    vecchio, _ = dal_markup(_marcato_del_documento(rev))
    if vecchio == oggi:
        print("✓ l'originale non è cambiato: non c'è niente da rigenerare")
        return 0
    riscritto, motivo = rigenera_testo(rev, oggi)
    if riscritto is None:
        print(f"✗ {motivo}. La revisione va rifatta a mano")
        return 1
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / originale.name
        tmp.write_text(riscritto, encoding="utf-8")
        testo, ok = revisione(originale, tmp)
    testo = testo.replace(f'riscritto="{_nel_repo(tmp)}"', 'riscritto="nel documento"')
    percorso_rev.write_text(testo, encoding="utf-8")
    print(f"{'✓' if ok else '✗'} rigenerata {_rel(percorso_rev)} sul testo di oggi: "
          "le spunte ripartono da zero, perché i numeri delle modifiche possono cambiare")
    return 0 if ok else 1


def _leggi_registro() -> "list[dict]":
    if not REGISTRO.exists():
        return []
    return json.loads(REGISTRO.read_text(encoding="utf-8"))


def registra(voce: dict) -> None:
    voci = _leggi_registro()
    voci.append(voce)
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    REGISTRO.write_text(json.dumps(voci, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def registro_cmd(check: bool) -> int:
    voci = _leggi_registro()
    if not voci:
        print("registro vuoto: nessuna revisione applicata dal 2026-10-03")
        return 0
    print("| data | file | modifiche | segnalazioni | MQM |")
    print("|---|---|---:|---|---|")
    male, ds, dq = [], 0, 0.0
    for v in voci:
        s0, s1 = v["segnalazioni"]
        q = v.get("mqm")
        ds += s1 - s0
        if q:
            dq += q[1] - q[0]
        print(f"| {v['data']} | `{v['file']}` | {v['modifiche']} | {s0} → {s1} | "
              f"{f'{q[0]} → {q[1]}' if q else '—'} |")
        if s1 > s0 or (q and q[1] < q[0]):
            male.append(v)
    print(f"\n{len(voci)} revisioni applicate: segnalazioni {ds:+d}, MQM {dq:+.2f} punti in tutto")
    if check and male:
        for v in male:
            print(f"✗ {v['file']} ({v['data']}): una revisione applicata ha peggiorato la misura")
        return 1
    if check:
        print("✓ registro dei miglioramenti: nessuna revisione applicata ha peggiorato la misura")
    return 0


# ── l'applicazione ───────────────────────────────────────────────────────────
_TESTA = re.compile(r'<!-- revisione: originale="(?P<o>[^"]+)" riscritto="(?P<r>[^"]+)" '
                    r'impronta="(?P<h>[0-9a-f]+)" -->')
_SPUNTA = re.compile(r"^\|\s*\[(?P<x>[ xX])\](?: auto)?\s*\|\s*(?P<n>\d+)\s*\|")
_REV = re.compile(r"<!-- revisione-testo: r(?P<n>\d+) · (?P<data>\d{4}-\d{2}-\d{2}) -->")


def accettate(revisione_md: str) -> "set[int]":
    return {int(m.group("n")) for r in revisione_md.splitlines()
            if (m := _SPUNTA.match(r)) and m.group("x").lower() == "x"}


def applica_testo(prima: str, dopo: str, numeri: "set[int]", _diff=None) -> str:
    """L'originale con le sole modifiche `numeri`. `_diff` riusa un diff già fatto."""
    a, b, gruppi = _diff or _diff_di(prima, dopo)
    out, n = [], 0
    for cambiato, i1, i2, j1, j2 in gruppi:
        if not cambiato:
            out.append("".join(a[i1:i2]))
            continue
        n += 1
        out.append("".join(b[j1:j2]) if n in numeri else "".join(a[i1:i2]))
    return "".join(out)


def _diff_di(prima: str, dopo: str):
    """Il diff a due livelli: per righe, poi per parole dentro i blocchi cambiati.

    Un diff per parole su un master intero (40.000 parole) costa minuti; per
    righe costa un attimo, e le parole si confrontano solo dove serve.
    Restituisce (parole di prima, parole di dopo, gruppi di `_gruppi`).
    """
    la, lb = prima.splitlines(keepends=True), dopo.splitlines(keepends=True)
    a: "list[str]" = []
    b: "list[str]" = []
    gruppi: "list[tuple[bool, int, int, int, int]]" = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, la, lb, autojunk=False).get_opcodes():
        ta = [t for r in la[i1:i2] for t in _PAROLA.findall(r)]
        tb = [t for r in lb[j1:j2] for t in _PAROLA.findall(r)]
        da, db = len(a), len(b)
        a += ta
        b += tb
        if op == "equal":
            gruppi.append((False, da, da + len(ta), db, db + len(tb)))
        else:
            gruppi += [(c, da + x1, da + x2, db + y1, db + y2) for c, x1, x2, y1, y2 in _gruppi(ta, tb)]
    return a, b, gruppi


def alza_revisione(testo: str, data: str) -> str:
    """La riga di revisione del testo (ADR-0077, sulla scia di ADR-0071)."""
    m = _REV.search(testo)
    if m:
        nuova = f"<!-- revisione-testo: r{int(m.group('n')) + 1} · {data} -->"
        return testo[:m.start()] + nuova + testo[m.end():]
    riga = f"<!-- revisione-testo: r1 · {data} -->\n"
    fm = re.match(r"---\n.*?\n---\n", testo, re.S)   # dopo il frontmatter, se c'è
    return testo[:fm.end()] + riga + testo[fm.end():] if fm else riga + testo


def _ramo() -> str:
    r = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=RADICE,
                       capture_output=True, text=True)
    return r.stdout.strip()


def applica(percorso_rev: Path, data: str, forza_ramo: bool = False, auto: bool = False,
            registro: bool = True) -> int:
    rev = percorso_rev.read_text(encoding="utf-8")
    m = _TESTA.search(rev)
    if not m:
        print("✗ non è un file di revisione: manca la riga di testa")
        return 2
    if _ramo() in ("main", "master") and not forza_ramo:
        print("✗ sul ramo principale non si applica (D15): passare su un ramo di lavoro")
        return 1
    originale = _assoluto(m.group("o"))
    prima = originale.read_text(encoding="utf-8")
    vecchio, dopo = dal_markup(_marcato_del_documento(rev))
    if vecchio != prima or _impronta(prima, dopo) != m.group("h"):
        print("✗ l'originale è cambiato dopo la revisione, o il documento è stato toccato: rigenerarla")
        return 1
    sì = accettate(rev)
    if auto:
        mods, _ = _modifiche(prima, dopo, segnala(prima))
        nuove = automatiche(prima, dopo, mods) - sì
        sì |= nuove
        # Il documento dice chi ha spuntato cosa: il lettore vede le automatiche.
        rev = "\n".join(re.sub(r"^\|\s*\[ \]\s*\|", "| [x] auto |", r)
                        if (m2 := _SPUNTA.match(r)) and int(m2.group("n")) in nuove else r
                        for r in rev.splitlines()) + "\n"
        percorso_rev.write_text(rev, encoding="utf-8")
    corretto = applica_testo(prima, dopo, sì)
    cambiati = confronta_fatti(prima, corretto)     # prima della riga di revisione, che ha una data
    if cambiati:
        print("✗ le modifiche accettate cambiano dei fatti: non si applica")
        for x in cambiati:
            print(f"  - {x}")
        return 1
    nuovo = alza_revisione(corretto, data)
    originale.write_text(nuovo, encoding="utf-8")
    mig = miglioramento(prima, nuovo, originale)
    print(f"✓ applicate {len(sì)} modifiche a {_rel(originale)}")
    print(f"  secondo giro: segnalazioni {mig['segnalazioni'][0]} → {mig['segnalazioni'][1]}")
    if mig["mqm"]:
        print(f"  punteggio MQM: {mig['mqm'][0]} → {mig['mqm'][1]}")
    if registro:
        registra({"data": data, "file": _rel(originale), "revisione": _rel(percorso_rev),
                  "modifiche": len(sì), "segnalazioni": mig["segnalazioni"], "mqm": mig["mqm"],
                  "penalita": mig["penalita"], "gulpease": mig["gulpease"], "norme": mig["norme"]})
    for s in segnala(nuovo):
        print(f"  · resta r.{s.riga}: {s.norma} {s.dettaglio}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("segnala", help="primo giro: i passaggi da correggere")
    s1.add_argument("file", type=Path)
    s1.add_argument("--languagetool", metavar="URL",
                    help="il secondo lettore: un server LanguageTool LOCALE, avviato da "
                         "scripts/avvia_languagetool.sh (facoltativo, ADR-0079)")
    s2 = sub.add_parser("revisione", help="il documento da approvare")
    s2.add_argument("originale", type=Path)
    s2.add_argument("riscritto", type=Path)
    s2.add_argument("-o", "--uscita", type=Path)
    s3 = sub.add_parser("applica", help="secondo giro: applica le modifiche spuntate")
    s3.add_argument("revisione", type=Path)
    s3.add_argument("--data", required=True, help="AAAA-MM-GG: la data non si deduce (ADR-0023)")
    s3.add_argument("--auto", action="store_true",
                    help="applica anche le modifiche segnate «auto», e lo scrive nel documento")
    s4 = sub.add_parser("lotto", help="i pacchetti da riscrivere, e la classifica MQM")
    s4.add_argument("file", type=Path, nargs="+")
    s4.add_argument("-o", "--uscita", type=Path, required=True)
    s5 = sub.add_parser("misura", help="di quanto il riscritto migliora l'originale")
    s5.add_argument("originale", type=Path)
    s5.add_argument("riscritto", type=Path)
    s6 = sub.add_parser("registro", help="i miglioramenti applicati; --check è il cancello")
    s6.add_argument("--check", action="store_true")
    s7 = sub.add_parser("rigenera", help="la revisione riportata sull'originale cambiato")
    s7.add_argument("revisione", type=Path)
    a = ap.parse_args(argv)

    if a.cmd == "lotto":
        return lotto(a.file, a.uscita)
    if a.cmd == "misura":
        return misura_cmd(a.originale, a.riscritto)
    if a.cmd == "registro":
        return registro_cmd(a.check)
    if a.cmd == "rigenera":
        return rigenera(a.revisione)

    if a.cmd == "segnala":
        testo = a.file.read_text(encoding="utf-8")
        seg = segnala(testo) + (languagetool(testo, a.languagetool) if a.languagetool else [])
        for s in seg:
            print(f"r.{s.riga}-{s.fine} · {s.norma} · {s.dettaglio}\n    → {s.rimedio}")
        print(f"{len(seg)} segnalazioni in {a.file}")
        return 0
    if a.cmd == "revisione":
        testo, ok = revisione(a.originale, a.riscritto)
        if a.uscita:
            a.uscita.write_text(testo, encoding="utf-8")
            print(f"{'✓' if ok else '✗'} revisione scritta in {a.uscita}")
        else:
            print(testo)
        return 0 if ok else 1
    return applica(a.revisione, a.data, auto=a.auto)


if __name__ == "__main__":
    sys.exit(main())
