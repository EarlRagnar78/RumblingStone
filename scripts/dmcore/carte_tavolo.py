"""carte_tavolo.py — le carte da tavolo di una corsa, lette dai master (voce B3).

La ricerca su cosa serve a un modulo pubblicabile (voce B3 di
`plans/RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md`) chiede carte che
«rendono visibile lo stato della gara senza spiegarlo»: un segnaposto per
contrada, l'ordine alle funi, il tratto in cui si trova la corsa, il posto che
ogni PG ha scelto e i patti scritti. Questo modulo **non scrive contenuto**:
legge le tabelle dei master che il DM già usa e le restituisce come dati, così
una CD cambiata nel master cambia anche sulla carta (ADR-0003).

Le fonti, una per carta:

| carta | master | dove |
|---|---|---|
| contrada | `CONTRADE-DI-TARSILIA.md` | §1 (nome, dèi, livrea, motto) e §7 (stemma) |
| alle funi | `REGOLE-DELLA-CORSA-PF1E.md` | §5: sette cavalli fra le funi, l'ottavo di rincorsa |
| tratto | `REGOLE-DELLA-CORSA-PF1E.md` | §6: tre giri, tabella dei tratti in §6.1 |
| posto | `REGOLE-DELLA-CORSA-PF1E.md` | §6.2, tabella dei posti |

Quello che non viene da una tabella (il numero dei cavalli alle funi, i tre
giri) è contato dal testo del master e controllato: se il master cambia, la
lettura si ferma con un errore invece di stampare carte vecchie.

Solo stdlib.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


class CarteError(ValueError):
    """Il master non ha la forma che le carte si aspettano."""


@dataclass(frozen=True)
class Contrada:
    numero: str
    nome: str
    dei: str
    livrea: str
    motto: str
    mestiere: str
    stemma: Path | None


@dataclass(frozen=True)
class Tratto:
    nome: str
    cd: str
    nota: str


@dataclass(frozen=True)
class Posto:
    nome: str
    chi: str
    azioni: str


_TITOLO = re.compile(r"^(#{2,3})\s+(.*)$")


def sezione(testo: str, inizio: str) -> str:
    """Il corpo della sezione il cui titolo comincia con `inizio` (fino al titolo
    dello stesso livello o superiore)."""
    righe = testo.splitlines()
    for i, r in enumerate(righe):
        m = _TITOLO.match(r)
        if m and m.group(2).strip().startswith(inizio):
            livello = len(m.group(1))
            fuori = []
            for s in righe[i + 1:]:
                n = _TITOLO.match(s)
                if n and len(n.group(1)) <= livello:
                    break
                fuori.append(s)
            return "\n".join(fuori)
    raise CarteError(f"sezione «{inizio}» non trovata")


def tabelle(md: str) -> list[list[list[str]]]:
    """Le tabelle markdown di un testo: ognuna è una lista di righe, intestazione
    compresa, senza la riga dei trattini."""
    fuori, corrente = [], []
    for r in md.splitlines():
        s = r.strip()
        if s.startswith("|") and s.endswith("|"):
            celle = [c.strip() for c in s[1:-1].split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in celle if c):
                continue
            corrente.append(celle)
        elif corrente:
            fuori.append(corrente)
            corrente = []
    if corrente:
        fuori.append(corrente)
    return fuori


def _piano(cella: str) -> str:
    """Toglie il grassetto e le virgolette basse di una cella: sulla carta la
    forma la dà il modello, non il master."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", cella)
    return s.strip()


def _tabella_con(md: str, prima: str, dove: str) -> list[list[str]]:
    for t in tabelle(md):
        if t and t[0] and t[0][0].strip("* ").lower() == prima.lower():
            return t
    raise CarteError(f"{dove}: nessuna tabella con la colonna «{prima}»")


def contrade(master: Path) -> list[Contrada]:
    """Le contrade del §1, con lo stemma del §7 risolto rispetto al master."""
    testo = master.read_text(encoding="utf-8")
    t = _tabella_con(sezione(testo, "§1"), "#", f"{master.name} §1")
    stemmi: dict[str, Path] = {}
    # §7: «| 1 | Oca | `golarion/01-oca.svg` |» e, più su, il percorso della cartella
    s7 = sezione(testo, "§7")
    cartella = None
    m = re.search(r"`([^`]*stemmi/golarion)/NN-\*\.svg`", sezione(testo, "§1"))
    if m:
        cartella = (master.parent / m.group(1)).resolve()
    for riga in _tabella_con(s7, "#", f"{master.name} §7")[1:]:
        if len(riga) >= 3 and cartella is not None:
            f = re.search(r"`golarion/([^`]+)`", riga[2])
            if f:
                stemmi[riga[0]] = cartella / f.group(1)
    fuori = []
    for riga in t[1:]:
        if len(riga) < 6:
            raise CarteError(f"{master.name} §1: riga con {len(riga)} colonne invece di 6: {riga}")
        n, nome, dei, livrea, motto, mestiere = riga[:6]
        stemma = stemmi.get(n)
        fuori.append(Contrada(
            numero=n, nome=_piano(nome), dei=dei, livrea=livrea,
            motto=motto.strip("*").strip("«»"), mestiere=mestiere,
            stemma=stemma if stemma is not None and stemma.is_file() else None,
        ))
    if not fuori:
        raise CarteError(f"{master.name} §1: tabella delle contrade vuota")
    return fuori


_NUMERI = {"due": 2, "tre": 3, "quattro": 4, "cinque": 5, "sei": 6, "sette": 7,
           "otto": 8, "nove": 9, "dieci": 10}


def cavalli_alle_funi(master: Path) -> int:
    """Quanti cavalli entrano fra le funi (§5: «Sette cavalli entrano fra le funi»)."""
    s5 = sezione(master.read_text(encoding="utf-8"), "§5")
    m = re.search(r"\b(\w+) cavalli entrano fra \*\*le funi\*\*", s5)
    if not m or m.group(1).lower() not in _NUMERI:
        raise CarteError(f"{master.name} §5: non dice quanti cavalli entrano fra le funi")
    return _NUMERI[m.group(1).lower()]


def giri(master: Path) -> int:
    """Quanti giri ha la corsa (§6: «Tre giri della Ruota»)."""
    s6 = sezione(master.read_text(encoding="utf-8"), "§6")
    m = re.search(r"\b(\w+) giri della Ruota", s6)
    if not m or m.group(1).lower() not in _NUMERI:
        raise CarteError(f"{master.name} §6: non dice quanti giri ha la corsa")
    return _NUMERI[m.group(1).lower()]


def tratti(master: Path) -> list[Tratto]:
    """I tratti di un giro, nell'ordine del §6.1."""
    s = sezione(master.read_text(encoding="utf-8"), "6.1")
    t = _tabella_con(s, "Tratto", f"{master.name} §6.1")
    fuori = [Tratto(_piano(r[0]), _piano(r[1]), r[2]) for r in t[1:] if len(r) >= 3]
    if not fuori:
        raise CarteError(f"{master.name} §6.1: tabella dei tratti vuota")
    return fuori


def posti(master: Path) -> list[Posto]:
    """I posti del §6.2 da cui i PG non fantini agiscono, uno per giro."""
    s = sezione(master.read_text(encoding="utf-8"), "6.2")
    t = _tabella_con(s, "Posto", f"{master.name} §6.2")
    fuori = [Posto(_piano(r[0]), r[1], r[2]) for r in t[1:] if len(r) >= 3]
    if not fuori:
        raise CarteError(f"{master.name} §6.2: tabella dei posti vuota")
    return fuori


def frase(master: Path, dove: str, inizio: str) -> str:
    """La frase del master che comincia con `inizio`, fino al punto che la chiude.

    Le carte riportano qualche frase di regola così com'è scritta («In Corsa
    vale così com'è scritto»): presa dal master, non ricopiata, perché una
    regola riscritta sulla carta è una seconda regola.
    """
    corpo = " ".join(sezione(master.read_text(encoding="utf-8"), dove).split())
    i = corpo.find(inizio)
    if i < 0:
        raise CarteError(f"{master.name} {dove}: manca la frase «{inizio}…»")
    m = re.search(r"[.!?](?=\s|$)", corpo[i:])
    return corpo[i:i + m.end()] if m else corpo[i:]


def finte(master: Path) -> list[str]:
    """Le finte del §5 (passo 2): una per voce, in markdown."""
    s5 = sezione(master.read_text(encoding="utf-8"), "§5")
    voci, corrente = [], None
    for r in s5.splitlines():
        m = re.match(r"^\s{2,}-\s+(.*)$", r)
        if m:
            if corrente:
                voci.append(corrente)
            corrente = m.group(1).strip()
        elif corrente is not None and r.startswith("     ") and r.strip():
            corrente += " " + r.strip()
        elif corrente is not None:
            voci.append(corrente)
            corrente = None
    if corrente:
        voci.append(corrente)
    if not voci:
        raise CarteError(f"{master.name} §5: nessuna finta elencata")
    return voci
