"""
visibility — policy UNICA di visibilità dei session log (Lotto D del piano
AUTOMAZIONE-STATO-SESSIONI; regola d'oro 5 del DM-TOOLKIT: il filtro
spoiler vive in un posto solo).

Livelli, dal template di sessione v2:

  sezioni pubbliche (`## Summary`, `## Key decisions`, …)
      → tutti i giocatori (già gestite da session_recap.PUBLIC_SECTIONS);
  blocchi split  `## Split — <PG[, PG…]> @ <luogo>`
      → SOLO i PG elencati (nell'heading o nella riga `**Visto da**: …`);
        nel recap di gruppo non compaiono MAI (il tavolo può essere misto);
  `## DM notes (private — optional)` e tutto ciò che segue
      → solo DM, mai esportato (regola storica, invariata).

I log senza blocchi Split (tutti quelli esistenti) sono al livello
"pubblico + DM notes": comportamento identico a prima (R5 del piano).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

SPLIT_HEADING_RE = re.compile(
    r"^##\s*Split\s*[—-]\s*(?P<pgs>[^@\n]+?)\s*@\s*(?P<place>.+?)\s*$", re.M)
VISTO_DA_RE = re.compile(r"^\*\*Visto da\*\*\s*:\s*(.+)$", re.M | re.I)
PRIVATE_CUT_RE = re.compile(r"^##\s+DM notes", re.M | re.I)
_NAME_SEP_RE = re.compile(r"\s*(?:,|&| e )\s*", re.I)


@dataclass(frozen=True)
class SplitBlock:
    pgs: tuple[str, ...]      # nomi normalizzati (title-case)
    place: str
    body: str                 # contenuto del blocco, heading escluso
    heading: str = field(default="")

    def visible_to(self, pg: str) -> bool:
        return pg.strip().lower() in (p.lower() for p in self.pgs)


def _parse_names(raw: str) -> tuple[str, ...]:
    return tuple(n.strip().title() for n in _NAME_SEP_RE.split(raw.strip()) if n.strip())


def strip_private(text: str) -> str:
    """Taglia `## DM notes` e tutto ciò che segue (identico a session_recap)."""
    m = PRIVATE_CUT_RE.search(text)
    return (text[:m.start()].rstrip() + "\n") if m else text


def split_blocks(text: str) -> list[SplitBlock]:
    """Estrae i blocchi `## Split — …` (dalla parte NON privata del log)."""
    text = strip_private(text)
    blocks: list[SplitBlock] = []
    matches = list(SPLIT_HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        # il blocco finisce al prossimo heading H2 (Split o no)
        nxt = re.search(r"^##\s", text[start:], re.M)
        end = start + nxt.start() if nxt else len(text)
        body = text[start:end].strip("\n")
        pgs = _parse_names(m.group("pgs"))
        mv = VISTO_DA_RE.search(body)
        if mv:  # la riga esplicita vince sull'heading
            pgs = _parse_names(mv.group(1))
            body = VISTO_DA_RE.sub("", body, count=1).strip("\n")
        blocks.append(SplitBlock(pgs=pgs, place=m.group("place").strip(),
                                 body=body, heading=m.group(0).strip()))
    return blocks


def for_pg(text: str, pg: str) -> list[SplitBlock]:
    """I soli blocchi split visibili al PG indicato."""
    return [b for b in split_blocks(text) if b.visible_to(pg)]


def strip_splits(text: str) -> str:
    """Rimuove TUTTI i blocchi split (per gli artefatti di gruppo)."""
    out = text
    while True:
        m = SPLIT_HEADING_RE.search(out)
        if not m:
            return out
        nxt = re.search(r"^##\s", out[m.end():], re.M)
        end = m.end() + nxt.start() if nxt else len(out)
        out = out[:m.start()] + out[end:]
