"""schede — legge le schede pregenerate dai master markdown e le restituisce
strutturate, pronte per un layout a pannelli (ADR-0003: il contenuto resta nei
`.md`, il layout è un artefatto).

Un booklet si accontenta di *stampare il testo*: una **scheda** no. Per
impaginare CA e PF in due riquadri, i sei attributi in una griglia e i legami in
una colonna a parte bisogna sapere **quale numero è quale**, e quello un
convertitore markdown→typst generico non lo sa.

Questo modulo legge i due master che il tavolo ha già:

    PREGEN-*.md      i numeri   → difesa, attacco, attributi, talenti, incantesimi
    FASCICOLO-*.md   la persona → background in prima persona, legami, primo gesto

e li fonde per nome in un `Scheda`. **Nessuna riscrittura dei dati**: se un
numero cambia nel master, cambia nella scheda stampata, e non esiste un secondo
posto dove possa restare vecchio.

I campi restano **markdown**: la conversione a Typst la fa chi impagina
(`scripts/export_booklet_typst.py`), che ha già il suo convertitore.

Solo stdlib. Non scrive nulla: legge e restituisce.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Scheda", "Voce", "leggi_schede", "SchedaError"]

# I ritratti si cercano con queste estensioni, in quest'ordine: prima la
# variante «web» leggera (un PNG da 6 MB per scheda fa un PDF da 40, che non si
# manda per posta), poi l'originale.
ESTENSIONI_RITRATTO = (".jpg", ".jpeg", ".png", ".webp", ".svg")


class SchedaError(RuntimeError):
    """Il master non ha la forma che una scheda richiede."""


@dataclass
class Voce:
    """Un blocco «**Etichetta**: corpo» del master, con il corpo in markdown."""

    etichetta: str
    corpo: str


@dataclass
class Scheda:
    numero: str = ""
    nome: str = ""
    ruolo: str = ""            # «il Capitano»
    classe: str = ""           # «Umana guerriera 3 · N · femmina, 38 anni · GS 2»
    occhiello: str = ""        # le due righe in corsivo sotto il nome

    rapide: list[tuple[str, str]] = field(default_factory=list)   # Iniziativa/Percezione/Velocità

    ca: str = ""
    ca_dettaglio: str = ""
    pf: str = ""
    pf_dado: str = ""
    ts: list[tuple[str, str]] = field(default_factory=list)       # (Tempra, +6)
    ts_nota: str = ""

    attributi: list[tuple[str, str, str]] = field(default_factory=list)  # (For, 17, +3)

    attacchi: list[tuple[str, bool]] = field(default_factory=list)  # (riga md, è continuazione)
    manovre: list[tuple[str, str]] = field(default_factory=list)    # (BAB, +3)

    voci: list[Voce] = field(default_factory=list)   # talenti, abilità, incantesimi, equipaggiamento…
    problema: str = ""
    minuto: str = ""

    # dal fascicolo
    ad_alta_voce: str = ""
    voci_retro: list[Voce] = field(default_factory=list)
    legami: list[tuple[str, str]] = field(default_factory=list)

    ritratto: Path | None = None

    def voce(self, prefisso: str) -> Voce | None:
        """La prima voce la cui etichetta comincia per `prefisso` (senza accenti)."""
        p = _piatto(prefisso)
        for v in self.voci:
            if _piatto(v.etichetta).startswith(p):
                return v
        return None


# ── minuzie di testo ─────────────────────────────────────────────────────────

def _piatto(s: str) -> str:
    """Minuscolo e senza accenti: per confrontare etichette e nomi propri."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return s.lower().strip()


def _spoglia(s: str) -> str:
    """Toglie il grassetto/corsivo markdown: serve a leggere le ETICHETTE, non il corpo."""
    return re.sub(r"[*`]", "", s).strip()


_TITOLO = re.compile(r"^##\s+(\d+)\s*·\s*(.+?)\s+—\s+(.+?)\s*$")
_VOCE = re.compile(r"^\*\*([^*]+?)\*\*\s*[:：]?\s*(.*)$")
_NBSP = re.compile(r"^(?:&nbsp;)+")
_PUNTO = re.compile(r"^[-*+]\s")

# Una riga in grassetto apre una voce NUOVA solo se l'etichetta è seguita da due
# punti, o da una parentesi che non sia un prezzo. Senza questa distinzione
# `**+ ~212 mo**, che sono della contrada` e `**mantello della resistenza +1**
# (1.000)` — che nei master vanno a capo in mezzo all'equipaggiamento — si
# staccherebbero come se fossero sezioni della scheda.
_NUOVA_VOCE = re.compile(r"^\*\*([^*]{2,40}?)\*\*\s*(?:[:：]|\((?![\d.,\s]*\)))")


def _sezioni(righe: list[str]) -> dict[str, list[str]]:
    """Spezza il corpo di una scheda sui suoi `### Sottotitoli`.

    La parte prima del primo `###` finisce sotto la chiave vuota: è
    l'intestazione (classe, occhiello, valori rapidi).
    """
    fuori: dict[str, list[str]] = {"": []}
    chiave = ""
    for ln in righe:
        m = re.match(r"^###\s+(.+?)\s*$", ln)
        if m:
            chiave = _piatto(m.group(1))
            fuori[chiave] = []
        else:
            fuori[chiave].append(ln)
    return fuori


def _unisci_continuazioni(righe: list[str]) -> list[str]:
    """Nei master le frasi vanno a capo a 88 colonne: qui si ricuciono.

    Una riga che **non** comincia per `**`, `-`, `&nbsp;` o `>` è la coda della
    precedente — trattarla come riga a sé staccherebbe la fine della frase dal
    suo grassetto, che è il difetto che si vede stampato come `**testo**`.
    """
    fuori: list[str] = []
    for ln in righe:
        nudo = ln.strip()
        if not nudo:
            fuori.append("")
            continue
        attacca = fuori and fuori[-1].strip() and not re.match(r"^(\*\*|[-*+]\s|&nbsp;|>|\|)", nudo)
        if attacca:
            fuori[-1] = fuori[-1].rstrip() + " " + nudo
        else:
            fuori.append(nudo)
    return fuori


def _voci(righe: list[str]) -> list[Voce]:
    """Ogni paragrafo che apre con `**Etichetta**:` diventa una voce.

    Gli elenchi puntati (gli slot degli incantesimi) restano attaccati alla voce
    che li ha introdotti: separarli produrrebbe una lista orfana in mezzo alla
    scheda. E **dentro un elenco il grassetto rientrato non apre niente** — nei
    master gli slot di scuola e dominio vanno a capo come
    `  **scuola**: *invisibilità*`, e presi per etichette diventerebbero voci
    fantasma. A distinguerli è il **rientro**, non la riga vuota: una voce vera
    comincia a colonna zero, sempre, anche quando segue un elenco senza stacco.
    """
    fuori: list[Voce] = []
    in_elenco = False
    for ln in righe:
        nudo = ln.strip()
        if not nudo:
            in_elenco = False
            continue
        if _PUNTO.match(nudo):
            in_elenco = True
            if fuori:
                fuori[-1].corpo = (fuori[-1].corpo + "\n" + nudo).strip()
            continue
        if not (in_elenco and ln[:1].isspace()) and _NUOVA_VOCE.match(nudo):
            in_elenco = False
            m = _VOCE.match(nudo)
            assert m is not None                       # _NUOVA_VOCE è più stretta
            fuori.append(Voce(_spoglia(m.group(1)), m.group(2).strip()))
        elif fuori:
            fuori[-1].corpo = (fuori[-1].corpo + " " + nudo).strip()
    return fuori


_FINE_APERTA = re.compile(r"[a-zà-ÿ]$")


def _righe_attacco(righe: list[str]) -> list[tuple[str, bool]]:
    """Le righe d'attacco, ognuna con il suo flag «è una continuazione».

    Qui il grassetto è posizionale — `**Mischia**`, `**Distanza**` aprono ogni
    volta una riga nuova — quindi la regola è l'opposta di quella delle voci:
    si continua solo quando la riga precedente si è interrotta **a metà frase**,
    cioè finisce con una lettera minuscola (`… CD 12 — con`).
    """
    fuori: list[tuple[str, bool]] = []
    for ln in righe:
        nudo = ln.strip()
        if not nudo:
            continue
        rientro = bool(_NBSP.match(nudo))
        nudo = _NBSP.sub("", nudo).strip()
        # Il rientro `&nbsp;` è una scelta di chi ha scritto il master: quella
        # riga è una variante dell'attacco sopra e va tenuta staccata, anche
        # quando non comincia in grassetto.
        continua = not rientro and (
            not nudo.startswith("**")
            or (bool(fuori) and bool(_FINE_APERTA.search(fuori[-1][0])))
        )
        if continua and fuori:
            fuori[-1] = (fuori[-1][0] + " " + nudo, fuori[-1][1])
        else:
            fuori.append((nudo, rientro))
    return fuori


def _coppie_puntate(riga: str) -> list[tuple[str, str]]:
    """`**Iniziativa** +5 · **Percezione** +3` → [(Iniziativa, +5), (Percezione, +3)]."""
    fuori: list[tuple[str, str]] = []
    for pezzo in re.split(r"\s+·\s+", riga.strip()):
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", pezzo.strip())
        if m:
            fuori.append((_spoglia(m.group(1)), _spoglia(m.group(2))))
    return fuori


def _prosa(righe: list[str]) -> str:
    return " ".join(x.strip() for x in righe if x.strip())


# ── il master dei numeri ─────────────────────────────────────────────────────

_ATTRIBUTO = re.compile(r"\*\*(For|Des|Cos|Int|Sag|Car)\*\*\s*(\d+)\s*\(\s*([+−-]?\d+)\s*\)")
_TS = re.compile(r"(Tempra|Riflessi|Volont\w*)\s*\*{0,2}\s*([+−-]?\d+)")


def _numeri(blocco: list[str], s: Scheda) -> None:
    sez = _sezioni(blocco)

    # intestazione: classe, occhiello in corsivo, valori rapidi
    testa = [x for x in sez.get("", []) if x.strip()]
    corsivo: list[str] = []
    for ln in testa:
        nudo = ln.strip()
        if not s.classe and nudo.startswith("**"):
            s.classe = _spoglia(nudo)
        elif nudo.startswith("*") and not nudo.startswith("**"):
            corsivo.append(nudo)
        elif corsivo and not nudo.startswith("**"):
            corsivo.append(nudo)
        elif nudo.startswith("**Iniziativa"):
            s.rapide = _coppie_puntate(nudo)
    s.occhiello = _prosa(corsivo).strip("*").strip()

    for ln in _unisci_continuazioni(sez.get("difesa", [])):
        m = re.match(r"^\*\*CA\*\*\s*(\d+)\s*,?\s*(.*)$", ln)
        if m:
            s.ca, s.ca_dettaglio = m.group(1), m.group(2).strip()
            continue
        m = re.match(r"^\*\*pf\*\*\s*(\d+)\s*(?:\(([^)]*)\))?", ln, re.I)
        if m:
            s.pf, s.pf_dado = m.group(1), (m.group(2) or "").strip()
            continue
        if ln.startswith("**TS**"):
            s.ts = [(_spoglia(a), _spoglia(b)) for a, b in _TS.findall(ln)]
            nota = re.search(r"\*\(([^)]*)\)\*\s*$", ln)
            s.ts_nota = nota.group(1).strip() if nota else ""

    for riga, rientro in _righe_attacco(sez.get("attacco", [])):
        if riga.startswith("**BAB**"):
            s.manovre = _coppie_puntate(riga)
        else:
            s.attacchi.append((riga, rientro))

    resto: list[str] = []
    for ln in sez.get("statistiche", []):
        trovati = _ATTRIBUTO.findall(ln)
        if len(trovati) >= 3 and not s.attributi:
            s.attributi = [(a, b, c.replace("−", "−")) for a, b, c in trovati]
        else:
            resto.append(ln)
    s.voci = _voci(resto)

    for chiave, righe in sez.items():
        if chiave.startswith("il suo problema") or chiave.startswith("il problema"):
            s.problema = _prosa(righe)
        elif chiave.startswith("come si gioca"):
            s.minuto = _prosa(righe)


# ── il master della persona ──────────────────────────────────────────────────

def _retro(blocco: list[str], s: Scheda) -> None:
    corpo, citazione = [], []
    for ln in blocco:
        nudo = ln.strip()
        if nudo.startswith(">"):
            citazione.append(nudo.lstrip(">").strip())
        elif nudo.startswith("!["):          # il ritratto lo risolve il chiamante
            continue
        elif nudo.startswith("*Ritratto:"):
            continue
        else:
            corpo.append(ln)
    testo = _prosa(citazione)
    testo = re.sub(r"^\*\*[^*]*\*\*\s*", "", testo)       # via l'etichetta «Da leggere ad alta voce.»
    s.ad_alta_voce = testo.strip().strip("*").strip()
    s.voci_retro = _voci(corpo)


def _matrice(testo: str) -> dict[str, list[tuple[str, str]]]:
    """La tabella dei legami → per ogni personaggio, cosa pensa degli altri cinque."""
    righe = [x.strip() for x in testo.split("\n")]
    for i, ln in enumerate(righe):
        if not (ln.startswith("|") and "pensa di" in _piatto(ln)):
            continue
        intestazione = [_spoglia(c) for c in ln.strip("|").split("|")][1:]
        fuori: dict[str, list[tuple[str, str]]] = {}
        for r in righe[i + 2:]:
            if not r.startswith("|"):
                break
            celle = [c.strip() for c in r.strip("|").split("|")]
            chi = _spoglia(celle[0])
            fuori[chi] = [
                (intestazione[j], _spoglia(c))
                for j, c in enumerate(celle[1:])
                if j < len(intestazione) and _spoglia(c) not in ("", "—", "-")
            ]
        return fuori
    return {}


# ── ritratti ─────────────────────────────────────────────────────────────────

def _ritratto(nome: str, cartelle: list[Path]) -> Path | None:
    """`FRA' MELCHIO VANZI` → `ritratto-melchio.jpg`.

    Si prova **ogni parola** del nome invece di indovinare quale sia: i sei nomi
    hanno articoli, soprannomi fra virgolette e un «Fra'», e una regola sul
    primo token darebbe `ritratto-fra.jpg`.
    """
    parole = [_piatto(re.sub(r"[^\wÀ-ÿ']+", "", p)).strip("'") for p in nome.split()]
    for cartella in cartelle:
        if not cartella.is_dir():
            continue
        for parola in parole:
            if len(parola) < 3:
                continue
            for est in ESTENSIONI_RITRATTO:
                p = cartella / f"ritratto-{parola}{est}"
                if p.is_file():
                    return p
    return None


# ── ingresso ─────────────────────────────────────────────────────────────────

_FILETTO = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")


def _blocchi(testo: str) -> list[tuple[str, str, str, list[str]]]:
    """Spezza un master sui suoi `## N · NOME — ruolo`.

    Il filetto `---` che separa una scheda dall'altra viene buttato qui: in una
    scheda non c'è niente da separare, e lasciandolo passare finirebbe in coda
    all'ultimo paragrafo — dove Typst lo stampa come lineetta lunga («… sei tu.
    —»), che sembra un errore di battitura del DM.
    """
    fuori: list[tuple[str, str, str, list[str]]] = []
    corrente: list[str] | None = None
    for ln in testo.split("\n"):
        m = _TITOLO.match(ln)
        if m:
            corrente = []
            fuori.append((m.group(1), m.group(2).strip(), m.group(3).strip(), corrente))
        elif corrente is not None:
            if re.match(r"^##\s", ln):        # un `##` che non è una scheda chiude l'ultima
                corrente = None
            elif not _FILETTO.match(ln):
                corrente.append(ln)
    return fuori


def leggi_schede(
    pregen: Path,
    fascicolo: Path | None = None,
    ritratti: list[Path] | None = None,
) -> list[Scheda]:
    """Le schede del modulo, nell'ordine del master dei numeri.

    `fascicolo` e `ritratti` sono facoltativi: senza fascicolo si ottiene la sola
    metà destra (i numeri), che è comunque una scheda — solo muta.
    """
    testo = pregen.read_text(encoding="utf-8")
    blocchi = _blocchi(testo)
    if not blocchi:
        raise SchedaError(
            f"{pregen.name}: nessuna scheda trovata. Attese intestazioni «## N · NOME — ruolo»."
        )

    schede: list[Scheda] = []
    for numero, nome, ruolo, righe in blocchi:
        s = Scheda(numero=numero, nome=nome, ruolo=ruolo)
        _numeri(righe, s)
        s.ritratto = _ritratto(nome, ritratti or [])
        schede.append(s)

    if fascicolo and fascicolo.is_file():
        testo_retro = fascicolo.read_text(encoding="utf-8")
        per_nome = {_piatto(n): righe for _, n, _, righe in _blocchi(testo_retro)}
        matrice = _matrice(testo_retro)
        for s in schede:
            righe = per_nome.get(_piatto(s.nome))
            if righe:
                _retro(righe, s)
            parole = {_piatto(p) for p in s.nome.split()}
            for chi, legami in matrice.items():
                if _piatto(chi) in parole:
                    s.legami = legami
                    break
    return schede
