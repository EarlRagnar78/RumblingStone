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
        for norma, rx in (("P1", mc.P1), ("metratura", mc.METRATURA), ("sembra/pare", vs.SEMBRA)):
            m = rx.search(corpo)
            if m:
                r = _riga_di(rx, b, i0)
                fuori.append(Segnalazione(r or i0 + 1, r or i1 + 1, norma, f"«{m.group(0).strip()}»"))

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


def languagetool(testo: str, url: str) -> "list[Segnalazione]":
    """Le segnalazioni grammaticali di un server LanguageTool (LGPL), se ce n'è uno.

    Facoltativo e fuori dalla CI: si usa come servizio, quindi la sua licenza
    non entra nel repo (ADR-0077). Senza rete, o con un server che non
    risponde, avvisa e non segnala niente.
    """
    dati = urllib.parse.urlencode({"text": testo, "language": "it"}).encode()
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/v2/check", dati, timeout=30) as r:
            risposta = json.load(r)
    except (OSError, ValueError) as e:
        print(f"⚠️ LanguageTool non raggiungibile ({e}): nessuna segnalazione grammaticale")
        return []
    fuori = []
    for m in risposta.get("matches", []):
        riga = testo.count("\n", 0, m.get("offset", 0)) + 1
        proposta = ", ".join(x["value"] for x in m.get("replacements", [])[:3])
        fuori.append(Segnalazione(riga, riga, "grammatica",
                                  f"{m.get('message', '')}" + (f" → {proposta}" if proposta else "")))
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
    """Le modifiche, parola per parola, e il testo con i segni CriticMarkup."""
    a, b = _PAROLA.findall(prima), _PAROLA.findall(dopo)
    mods, pezzi = [], []
    for cambiato, i1, i2, j1, j2 in _gruppi(a, b):
        if not cambiato:
            pezzi.append("".join(a[i1:i2]))
            continue
        vecchio, nuovo = "".join(a[i1:i2]), "".join(b[j1:j2])
        riga = "".join(a[:i1]).count("\n") + 1
        fine = riga + vecchio.count("\n")
        norme = sorted({s.norma for s in segnalazioni if s.riga <= fine and riga <= s.fine})
        m = Modifica(len(mods) + 1, riga, vecchio, nuovo, norme)
        mods.append(m)
        pezzi.append(m.critic() + "{>>#" + str(m.numero) + "<<}")
    return mods, "".join(pezzi)


def _rel(p: Path) -> str:
    p = p.resolve()
    try:
        return p.relative_to(RADICE).as_posix()
    except ValueError:
        return p.as_posix()


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
    ok = set()
    for m in mods:
        if not m.norme:
            continue
        solo = applica_testo(prima, dopo, {m.numero})
        if confronta_fatti(prima, solo):
            continue
        m1 = misure(solo)
        l1 = lettura(solo)
        lettura_ok = (l1["gulpease"] >= l0["gulpease"] - TOLLERANZA_GULPEASE
                      and l1["ritmo"] >= l0["ritmo"] - TOLLERANZA_RITMO)
        if all(m1[k] <= m0[k] for k in m1) and sum(m1.values()) < sum(m0.values()) and lettura_ok:
            ok.add(m.numero)
    return ok


def revisione(originale: Path, riscritto: Path) -> "tuple[str, bool]":
    prima = originale.read_text(encoding="utf-8")
    dopo = riscritto.read_text(encoding="utf-8")
    seg = segnala(prima)
    mods, marcato = _modifiche(prima, dopo, seg)
    m0, m1 = misure(prima), misure(dopo)
    peggiorate = sorted(k for k in m1 if m1[k] > m0[k])
    fatti_cambiati = confronta_fatti(prima, dopo)
    non_motivate = [m.numero for m in mods if not m.norme]
    auto = automatiche(prima, dopo, mods)
    l0, l1 = lettura(prima), lettura(dopo)
    ok = not peggiorate and not fatti_cambiati

    r = [f"# Revisione · {originale.name}", "",
         f'<!-- revisione: originale="{_rel(originale)}" riscritto="{_rel(riscritto)}" '
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
    r += [f"- **Segnalazioni**: {sum(m0.values())} prima, {sum(m1.values())} dopo",
          f"- **Modifiche non motivate da una segnalazione**: {len(non_motivate)}"
          + (f" (#{', #'.join(map(str, non_motivate))}): vanno guardate per prime" if non_motivate else ""),
          f"- **Applicabili senza lettore**: {len(auto)} su {len(mods)}",
          "", "## La lettura, prima e dopo", "",
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
    r += ["", "## Il testo con le modifiche (CriticMarkup)", "", "````markdown", marcato, "````", ""]
    return "\n".join(r), ok


# ── l'applicazione ───────────────────────────────────────────────────────────
_TESTA = re.compile(r'<!-- revisione: originale="(?P<o>[^"]+)" riscritto="(?P<r>[^"]+)" '
                    r'impronta="(?P<h>[0-9a-f]+)" -->')
_SPUNTA = re.compile(r"^\|\s*\[(?P<x>[ xX])\](?: auto)?\s*\|\s*(?P<n>\d+)\s*\|")
_REV = re.compile(r"<!-- revisione-testo: r(?P<n>\d+) · (?P<data>\d{4}-\d{2}-\d{2}) -->")


def accettate(revisione_md: str) -> "set[int]":
    return {int(m.group("n")) for r in revisione_md.splitlines()
            if (m := _SPUNTA.match(r)) and m.group("x").lower() == "x"}


def applica_testo(prima: str, dopo: str, numeri: "set[int]") -> str:
    a, b = _PAROLA.findall(prima), _PAROLA.findall(dopo)
    out, n = [], 0
    for cambiato, i1, i2, j1, j2 in _gruppi(a, b):
        if not cambiato:
            out.append("".join(a[i1:i2]))
            continue
        n += 1
        out.append("".join(b[j1:j2]) if n in numeri else "".join(a[i1:i2]))
    return "".join(out)


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


def applica(percorso_rev: Path, data: str, forza_ramo: bool = False, auto: bool = False) -> int:
    rev = percorso_rev.read_text(encoding="utf-8")
    m = _TESTA.search(rev)
    if not m:
        print("✗ non è un file di revisione: manca la riga di testa")
        return 2
    if _ramo() in ("main", "master") and not forza_ramo:
        print("✗ sul ramo principale non si applica (D15): passare su un ramo di lavoro")
        return 1
    originale, riscritto = _assoluto(m.group("o")), _assoluto(m.group("r"))
    prima = originale.read_text(encoding="utf-8")
    dopo = riscritto.read_text(encoding="utf-8")
    if _impronta(prima, dopo) != m.group("h"):
        print("✗ l'originale o il riscritto sono cambiati dopo la revisione: rigenerarla")
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
    m0, m1 = misure(prima), misure(nuovo)
    print(f"✓ applicate {len(sì)} modifiche a {_rel(originale)}")
    print(f"  secondo giro: segnalazioni {sum(m0.values())} → {sum(m1.values())}")
    for s in segnala(nuovo):
        print(f"  · resta r.{s.riga}: {s.norma} {s.dettaglio}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("segnala", help="primo giro: i passaggi da correggere")
    s1.add_argument("file", type=Path)
    s1.add_argument("--languagetool", metavar="URL", help="un server LanguageTool (facoltativo)")
    s2 = sub.add_parser("revisione", help="il documento da approvare")
    s2.add_argument("originale", type=Path)
    s2.add_argument("riscritto", type=Path)
    s2.add_argument("-o", "--uscita", type=Path)
    s3 = sub.add_parser("applica", help="secondo giro: applica le modifiche spuntate")
    s3.add_argument("revisione", type=Path)
    s3.add_argument("--data", required=True, help="AAAA-MM-GG: la data non si deduce (ADR-0023)")
    s3.add_argument("--auto", action="store_true",
                    help="applica anche le modifiche segnate «auto», e lo scrive nel documento")
    a = ap.parse_args(argv)

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
