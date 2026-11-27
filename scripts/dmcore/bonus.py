"""dmcore.bonus — il cumulo dei bonus per tipo (ADR-0126, lotto 1).

La regola è una sola per tutta la famiglia d20 (SRD 3.5 «Bonus Types», PRD
PF1e uguale): due bonus dello stesso tipo non si sommano, vale il più alto;
schivare, circostanza, razziale e i bonus senza tipo si sommano.

Qui stanno tre cose, tutte deterministiche:

* `somma(voci)`: il totale di una lista di bonus, col tipo che decide;
* `dichiarati(testo)`: i bonus che una scheda **dichiara**, per campo. Vengono
  da due posti: le sorgenti note di `sistemi/d20/dati/bonus.toml` (un oggetto,
  un talento, una razza scritti nella scheda) e le dichiarazioni esplicite
  nella riga dei tiri salvezza («+1 fortuna a tutti», «+2 sacro alla Volontà»);
* `totali(testo)`: {campo: totale}, quello che i conti usano.

Un bonus a condizione («+2 razziale contro gli incantesimi») non entra: il
numero scritto nella scheda è quello di base.
"""
from __future__ import annotations

import functools
import re
from dataclasses import dataclass

from dmcore import sistemi as S

__all__ = ["Voce", "CAMPI_TS", "regole", "somma", "dichiarati", "totali"]

CAMPI_TS = ("Temp", "Rifl", "Vol")
_NOME_CAMPO = (("Temp", r"temp(?:ra)?|fort(?:itude)?"), ("Rifl", r"rifl(?:essi)?|ref(?:lex)?"),
               ("Vol", r"vol(?:ont[aà])?|will"))
_RIGA_TS = re.compile(
    r"^(?:ts:|.*\bTS\b|.*\bTiri Salvezza\b|.*\bSaves\b|.*\bFort\s*[+-]\d).*$", re.M | re.I)
_RIGA_TIPO = re.compile(r"^tipo:.*$", re.M | re.I)
_PARENTESI = re.compile(r"\(([^()]*)\)")


@dataclass(frozen=True)
class Voce:
    valore: int
    tipo: str
    sorgente: str
    fonte: str = ""


@functools.lru_cache(maxsize=None)
def regole(sistema: str = "d20") -> dict:
    d = S.dati(sistema, "bonus.cumulo")
    sorgenti = [dict(s, _re=re.compile(s["schema"], re.I)) for s in d.get("sorgenti", [])]
    tipi = {alias.lower(): tipo for tipo, nomi in d["tipi"].items() for alias in nomi}
    alternative = "|".join(sorted((re.escape(a) for a in tipi), key=len, reverse=True))
    campo = "|".join(f"(?P<{c}>{r})" for c, r in _NOME_CAMPO)
    esplicita = re.compile(
        rf"\+(?P<n>\d+)\s+(?:bonus\s+)?(?:di\s+)?(?P<tipo>{alternative})\b"
        rf"(?:\s+(?:a|ai|al|alla|alle|su|sui|sulla|on|to)\s+(?:(?P<tutti>tutti|all)|{campo})\b)?", re.I)
    condizione = re.compile(
        r"(?<!\w)(?:" + "|".join(re.escape(p) for p in d["condizioni"]["parole"]) + r")(?!\w)", re.I)
    return {"si_sommano": frozenset(d["cumulo"]["si_sommano"]), "sorgenti": sorgenti,
            "tipi": tipi, "esplicita": esplicita, "condizione": condizione}


def somma(voci: "list[Voce]", sistema: str = "d20") -> "tuple[int, list[Voce], list[Voce]]":
    """(totale, voci contate, voci scartate perché dello stesso tipo di una più alta)."""
    libere = regole(sistema)["si_sommano"]
    contate, scartate, migliore = [], [], {}
    for v in voci:
        if v.tipo in libere:
            contate.append(v)
        elif v.tipo not in migliore or v.valore > migliore[v.tipo].valore:
            if v.tipo in migliore:
                scartate.append(migliore[v.tipo])
            migliore[v.tipo] = v
        else:
            scartate.append(v)
    contate += [migliore[t] for t in sorted(migliore)]
    return sum(v.valore for v in contate), contate, scartate


def _esplicite(testo: str, r: dict) -> "dict[str, list[Voce]]":
    fuori: dict = {}
    for riga in _RIGA_TS.findall(testo):
        for dentro in _PARENTESI.findall(riga):
            for clausola in re.split(r"[;,]", dentro):
                m = r["esplicita"].search(clausola)
                if not m or r["condizione"].search(clausola):
                    continue
                campi = [c for c in CAMPI_TS if m.group(c)] or list(CAMPI_TS)
                v = Voce(int(m.group("n")), r["tipi"][m.group("tipo").lower()],
                         "dichiarato nella riga dei tiri salvezza: " + clausola.strip())
                for c in campi:
                    fuori.setdefault(c, []).append(v)
    return fuori


def dichiarati(testo: str, sistema: str = "d20") -> "dict[str, list[Voce]]":
    """{campo: [Voce]} dei bonus che il testo dichiara. `testo` va dato senza note."""
    r = regole(sistema)
    fuori: dict = {}
    riga_tipo = "\n".join(_RIGA_TIPO.findall(testo))
    for s in r["sorgenti"]:
        m = s["_re"].search(riga_tipo if s.get("dove") == "tipo" else testo)
        if not m:
            continue
        n = int(m.group(1)) if s["valore"] == "N" else int(s["valore"])
        v = Voce(n, s["tipo"], s["nome"], s.get("fonte", ""))
        for c in s["campi"]:
            fuori.setdefault(c, []).append(v)
    for c, voci in _esplicite(testo, r).items():
        fuori.setdefault(c, []).extend(voci)
    return fuori


def totali(testo: str, sistema: str = "d20") -> "dict[str, int]":
    return {c: somma(voci, sistema)[0] for c, voci in dichiarati(testo, sistema).items()}
