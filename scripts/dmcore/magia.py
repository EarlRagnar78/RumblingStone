"""dmcore.magia — incantesimi al giorno, conosciuti e CD ricostruiti dalle tabelle
delle classi (ADR-0126, lotto 3).

SRD 3.5, tabelle delle classi e «Table: Ability Modifiers and Bonus Spells»:

* gli **incantesimi al giorno** di un livello sono la cella della tabella della
  classe al livello d'incantatore, più gli incantesimi bonus della
  caratteristica (dal 1° livello in su), più lo slot di dominio del chierico
  (dal 1° in su) e lo slot di scuola del mago specialista (nel 3.5 anche al 0);
* una cella «—» vuol dire che la classe a quel livello non lancia; uno 0 che
  lancia solo gli incantesimi bonus;
* per lanciare un incantesimo di livello L serve la caratteristica a 10 + L;
* la **CD** è 10 + livello dell'incantesimo + modificatore della
  caratteristica (+1 con Incantesimi Focalizzati sulla scuola, +2 con il
  Superiore);
* gli **incantesimi conosciuti** di bardo e stregone sono fissi, la
  caratteristica non li cambia.

Qui stanno i conti. Trovare la classe, il livello e la caratteristica in una
scheda è lavoro di `verifica_scheda.incantatori`.
"""
from __future__ import annotations

import functools
import re

from dmcore import formule as _F
from dmcore import sistemi as S

__all__ = ["tabelle", "classe", "bonus", "al_giorno", "conosciuti", "cd", "leggi_al_giorno",
           "conta", "RIGA", "giudica_dichiarati", "giudica_riga"]

#: una riga della lista: livello, parentesi subito dopo il livello, resto
RIGA = re.compile(r"^\s*(?:[-*•]\s*)?\**(?:Level\s+|Livello\s+)?(?P<liv>\d)(?:°|º|st|nd|rd|th)?\**\s*"
                  r"(?:\((?P<par>[^)]*)\))?\s*\**\s*[:—–-]\s*(?P<resto>\S.*)$", re.I)
#: «6/7+1/7+1/6+1 al giorno», «3/4/2 per giorno»
_AL_GIORNO = re.compile(r"((?:\d+(?:\s*\+\s*(?:\d+|D))?\s*/\s*)+\d+(?:\s*\+\s*(?:\d+|D))?)\s*"
                        r"(?:al giorno|per giorno|/giorno|per day)", re.I)
_VOLTE = re.compile(r"[×x]\s*(\d+)\b|\((\d+)\)")
_CD = re.compile(r"\b(?:CD|DC)\s*(\d+)")


@functools.cache
def tabelle(sistema: str = "dnd35") -> dict:
    """Le tabelle degli incantatori del `sistema` (capacità `creature.incantatori`)."""
    return S.dati(sistema, "creature.incantatori")


def classe(nome: str, sistema: str = "dnd35") -> "dict | None":
    return tabelle(sistema)["classi"].get(nome)


def _f(nome: str, **valori: int) -> int:
    """Le formule stanno nel plugin d20 (`sistemi/d20/dati/formule.toml`, F3 di ADR-0112)."""
    return _F.formula(nome)(**valori)


def mod(punteggio: int) -> int:
    return _f("modificatore", punteggio=punteggio)


def bonus(modificatore: int, livello: int) -> int:
    """Incantesimi bonus al giorno per modificatore e livello d'incantesimo."""
    return _f("incantesimi_bonus", livello=livello, modificatore=modificatore)


def serve(livello: int) -> int:
    """Il punteggio che serve per lanciare un incantesimo di quel livello."""
    return _f("punteggio_per_lanciare", livello=livello)


def al_giorno(nome: str, livello_classe: int, punteggio: int, sistema: str = "dnd35",
              specialista: bool = False) -> "list[tuple[int, int]] | None":
    """Per ogni livello d'incantesimo, (slot di base con i bonus, slot in più di
    dominio o di scuola). Un livello che la classe non lancia, o che la
    caratteristica non regge, non c'è. None se la classe non ha tabella."""
    c = classe(nome, sistema)
    if c is None:
        return None
    riga = c["al_giorno"].get(str(max(1, min(20, livello_classe))), [])
    m = mod(punteggio)
    fuori = []
    for liv, base in enumerate(riga):
        if base < 0 and liv == 0 and "conosciuti" in c:
            fuori.append((-1, 0))          # trucchetti a volontà (PF1e): il numero al giorno non si giudica
            continue
        if base < 0 or punteggio < serve(liv):
            fuori.append((0, 0))
            continue
        # lo slot di scuola: nell'SRD 3.5 «per spell level», anche lo 0 (card del DM del
        # 2026-11-19); nel PRD «from 1st on up». Lo slot di dominio parte dal 1°.
        extra = 1 if ((liv >= 1 and c.get("slot_di_dominio"))
                      or (specialista and (liv >= 1 or sistema == "dnd35"))) else 0
        fuori.append((base + bonus(m, liv), extra))
    while fuori and sum(fuori[-1]) <= 0:
        fuori.pop()
    return fuori


def conosciuti(nome: str, livello_classe: int, sistema: str = "dnd35") -> "list[int] | None":
    c = classe(nome, sistema)
    if c is None or "conosciuti" not in c:
        return None
    riga = [max(0, n) for n in c["conosciuti"].get(str(max(1, min(20, livello_classe))), [])]
    if c.get("conosciuti_di_stirpe"):      # PF1e: un incantesimo di stirpe di livello L dal livello di classe 2L+1
        riga = [n + (1 if liv >= 1 and livello_classe >= 2 * liv + 1 else 0) for liv, n in enumerate(riga)]
    return riga


def cd(livello: int, punteggio: int) -> int:
    return _f("cd_incantesimo", livello=livello, modificatore=mod(punteggio))


def leggi_al_giorno(testo: str) -> "list[tuple[int, int]] | None":
    """«6/7+1/7+1» → [(6, 0), (7, 1), (7, 1)]. None se la riga non lo scrive."""
    m = _AL_GIORNO.search(testo)
    if not m:
        return None
    fuori = []
    for pezzo in m.group(1).split("/"):
        a, _, b = pezzo.partition("+")
        fuori.append((int(a), 0 if not b.strip() else 1 if b.strip().upper() == "D" else int(b)))
    return fuori


def conta(resto: str) -> int:
    """Quanti incantesimi scrive il resto di una riga della lista. Un
    incantesimo è un nome in corsivo; più nomi nello stesso corsivo si separano
    con la virgola. «×2» e «(2)» subito dopo il nome contano due. Il testo fuori
    dal corsivo (note, parentesi, quadre) non è un incantesimo."""
    resto = re.sub(r"\[[^\]]*\]", "", resto).replace("**", "")
    n = 0
    for m in re.finditer(r"\*([^*]+)\*", resto):
        nomi = [x for x in re.split(r"[,;]", m.group(1)) if re.search(r"[A-Za-zÀ-ÿ]{3}", x)]
        if not nomi:
            continue
        n += len(nomi)
        dentro = _VOLTE.search(nomi[-1])
        coda = re.match(r"(?:\s*\((?:CD|DC)[^)]*\))?\s*(?:[×x]\s*(\d+)\b|\([×x]?\s*(\d+)\))", resto[m.end():])
        if dentro or coda:
            n += int(next(g for g in (dentro or coda).groups() if g)) - 1
    return n


def giudica_dichiarati(scritti: "list[tuple[int, int]]", attesi: "list[tuple[int, int]]",
                       da_zero: bool = True) -> "list[dict]":
    """Gli scarti di una riga «N/N+1/…» contro gli slot attesi. `da_zero` False
    se la riga parte dal 1° livello (ranger, paladino)."""
    scarti = []
    att = attesi if da_zero else attesi[1:]
    for i in range(max(len(scritti), len(att))):
        liv = i if da_zero else i + 1
        s = scritti[i] if i < len(scritti) else None
        a = att[i] if i < len(att) else None
        if a is not None and a[0] < 0:
            continue
        if s is None:
            if sum(a) > 0:
                scarti.append({"livello": liv, "scritto": "manca", "atteso": _slot(a)})
        elif a is None:
            if sum(s) > 0:
                scarti.append({"livello": liv, "scritto": _slot(s), "atteso": "nessuno"})
        elif sum(s) != sum(a):
            scarti.append({"livello": liv, "scritto": _slot(s), "atteso": _slot(a)})
    return scarti


def _slot(x: "tuple[int, int]") -> str:
    return f"{x[0]}+{x[1]}" if x[1] else str(x[0])


def giudica_riga(livello: int, par: str, resto: str, attesi: "list[tuple[int, int]] | None",
                 noti: "list[int] | None", punteggio: int, focalizzato: int = 0,
                 lista_intera: bool = True) -> "list[dict]":
    """Gli scarti di una riga della lista: campo `incantesimi.livello`,
    `incantesimi.al_giorno` (la parentesi «5+1», o più incantesimi preparati
    degli slot), `incantesimi.conosciuti`, `incantesimi.cd`.

    `attesi` sono gli slot (None se non si giudicano), `noti` i conosciuti di
    una classe che non prepara; `focalizzato` è quanto la CD può salire per i
    talenti che la scheda dichiara (0, 1 o 2). Meno incantesimi degli slot non è
    uno scarto: la scheda può scrivere una scelta («incantesimi chiave»)."""
    scarti = []
    if attesi is not None:
        if livello >= len(attesi) or (sum(attesi[livello]) == 0 and livello > 0):
            motivo = (f"serve la caratteristica a {serve(livello)}" if punteggio < serve(livello)
                      else "la classe a questo livello non lo lancia")
            return [{"campo": "incantesimi.livello", "scritto": f"{livello}°", "atteso": "nessuno", "nota": motivo}]
        a = attesi[livello]
        if a[0] < 0:
            a = (99, 0)
        m = re.fullmatch(r"\s*(\d+)\s*(?:\+\s*(\d+|D|S))?\s*(?:conosciut[oi]|al giorno|slot)?\s*", par or "", re.I)
        if noti is not None:
            quanti = noti[livello] if livello < len(noti) else 0
            n = conta(resto)
            if m and int(m.group(1)) != quanti and "giorno" not in (par or ""):
                scarti.append({"campo": "incantesimi.conosciuti", "scritto": m.group(1), "atteso": quanti,
                               "nota": f"conosciuti di {livello}° dalla tabella"})
            elif n > quanti:
                scarti.append({"campo": "incantesimi.conosciuti", "scritto": n, "atteso": quanti,
                               "nota": f"la riga ne scrive {n}, la tabella ne dà {quanti}"})
        else:
            if m:
                s = (int(m.group(1)), 0 if not m.group(2) else 1 if not m.group(2).isdigit() else int(m.group(2)))
                if sum(s) != sum(a) and a[0] != 99:
                    scarti.append({"campo": "incantesimi.al_giorno", "scritto": _slot(s), "atteso": _slot(a),
                                   "nota": f"slot di {livello}°: tabella più incantesimi bonus"})
            n = conta(resto)
            if lista_intera and n > sum(a):
                scarti.append({"campo": "incantesimi.al_giorno", "scritto": n, "atteso": _slot(a),
                               "nota": f"la riga prepara {n} incantesimi, gli slot sono {sum(a)}"})
    giusta = cd(livello, punteggio)
    for v in sorted({int(x) for x in _CD.findall((par or "") + " " + resto)}):
        if not giusta <= v <= giusta + focalizzato:
            scarti.append({"campo": "incantesimi.cd", "scritto": v, "atteso": giusta,
                           "nota": f"10 + {livello} + modificatore {mod(punteggio):+d}"
                                   + (f", fino a +{focalizzato} con gli Incantesimi Focalizzati" if focalizzato else "")})
    return scarti
