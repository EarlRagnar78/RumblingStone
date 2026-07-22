"""
regions — regioni marcate ``auto:`` nei file di canone (ADR-0007 vincolo 3).

Gli script possono modificare `campaign/state.md` SOLO dentro blocchi
delimitati da marker HTML-comment (invisibili nel rendering):

    <!-- auto:begin key=march-clock -->
    ...contenuto gestito dagli script...
    <!-- auto:end key=march-clock -->

Tutto ciò che sta fuori dai marker è territorio del DM: `replace_region`
verifica *per costruzione* che i byte esterni restino identici e alza
``RegionError`` in ogni caso ambiguo (marker mancante, duplicato,
disallineato). Meglio nessuna scrittura che una scrittura sbagliata.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

BEGIN_TPL = "<!-- auto:begin key={key} -->"
END_TPL = "<!-- auto:end key={key} -->"

_MARKER_RE = re.compile(
    r"<!--\s*auto:(?P<kind>begin|end)\s+key=(?P<key>[a-z0-9][a-z0-9-]*)\s*-->"
)


class RegionError(RuntimeError):
    """Marker mancanti, duplicati o malformati: nessuna scrittura possibile."""


@dataclass(frozen=True)
class Region:
    key: str
    start: int   # offset del primo byte del contenuto (dopo il newline del begin)
    end: int     # offset dell'ultimo byte del contenuto (prima del marker end)

    def content(self, text: str) -> str:
        return text[self.start:self.end]


def find_regions(text: str) -> dict[str, Region]:
    """Mappa key → Region. Alza RegionError su marker sbilanciati o duplicati."""
    opened: dict[str, int] = {}
    regions: dict[str, Region] = {}
    for m in _MARKER_RE.finditer(text):
        kind, key = m.group("kind"), m.group("key")
        if kind == "begin":
            if key in opened or key in regions:
                raise RegionError(f"marker duplicato: auto:begin key={key}")
            opened[key] = m.end()
        else:
            if key not in opened:
                raise RegionError(f"auto:end key={key} senza begin corrispondente")
            start = opened.pop(key)
            # il contenuto inizia dopo il newline che segue il begin, se c'è
            if start < len(text) and text[start] == "\n":
                start += 1
            regions[key] = Region(key=key, start=start, end=m.start())
    if opened:
        raise RegionError(
            "marker non chiusi: " + ", ".join(f"auto:begin key={k}" for k in opened))
    return regions


def replace_region(text: str, key: str, new_content: str) -> str:
    """Sostituisce il contenuto della regione `key`, garantendo che tutto
    ciò che sta fuori dai marker resti byte-identico (contratto ADR-0007)."""
    regions = find_regions(text)
    if key not in regions:
        raise RegionError(
            f"regione '{key}' assente — lancia `state_apply.py --migrate` "
            f"per inserire i marker (regioni presenti: {sorted(regions) or 'nessuna'})")
    reg = regions[key]
    if new_content and not new_content.endswith("\n"):
        new_content += "\n"
    result = text[:reg.start] + new_content + text[reg.end:]
    # cintura e bretelle: l'esterno DEVE essere rimasto intatto
    if result[:reg.start] != text[:reg.start] or result[len(result) - (len(text) - reg.end):] != text[reg.end:]:
        raise RegionError(f"invariante violata sostituendo la regione '{key}' — nessuna scrittura")
    return result


def wrap(key: str, content: str) -> str:
    """Restituisce `content` avvolto nei marker della regione `key`."""
    if content and not content.endswith("\n"):
        content += "\n"
    return f"{BEGIN_TPL.format(key=key)}\n{content}{END_TPL.format(key=key)}"
