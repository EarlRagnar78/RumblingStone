"""
testo — normalizzazione di stringhe condivisa (Lotto A del piano
QUALITA-DEL-CODICE; ADR-0037 per il vincolo stdlib-only).

Prima di questo modulo il repo aveva **sette** implementazioni di `slug`, e
una si comportava diversamente dalle altre: `build_monster_catalog.py`
saltava la normalizzazione NFKD, quindi una lettera accentata non veniva
traslitterata, veniva buttata via. Nove record veri del catalogo mostri
avevano un id che nessun altro strumento della catena ricalcolava uguale
(``l-myn-redtongue-…`` contro ``lomyn-redtongue-…``).

Qui ce n'è una sola, parametrica sulle due sole cose su cui i sette
chiamanti divergevano davvero: la lunghezza massima e la stringa di
ripiego quando non resta niente.

    >>> slug("Città")
    'citta'
    >>> slug("Lómyn RedTongue")
    'lomyn-redtongue'
    >>> slug("Razorfiend «Blackspawn Alfa» d'élite")
    'razorfiend-blackspawn-alfa-d-elite'
    >>> slug("12–13")          # trattino lungo, non un trattino ASCII
    '12-13'
    >>> slug("«»", ripiego="mappa")
    'mappa'

Solo stdlib.
"""

from __future__ import annotations

import os
from pathlib import PurePosixPath

import re
import unicodedata

__all__ = ["slug", "piega_ascii"]

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def piega_ascii(s: str) -> str:
    """Riduce `s` ad ASCII, senza far sparire silenziosamente i caratteri.

    Le tre categorie hanno tre destini diversi, e il terzo è il motivo per
    cui questa funzione esiste invece di un ``.encode("ascii", "ignore")``:

    * ASCII: resta com'è;
    * segno combinante (l'accento che NFKD ha staccato dalla lettera): si
      butta, ed è così che ``é`` diventa ``e``;
    * qualsiasi altro carattere non-ASCII: diventa un separatore.

    ``ignore`` metteva tutto e tre nella seconda categoria, e su ``12–13``
    questo produce ``1213``: due numeri diventano uno. Un trattino lungo
    che l'ASCII non sa scrivere separa, non sparisce.
    """
    fuori = []
    for ch in unicodedata.normalize("NFKD", s):
        if ord(ch) < 128:
            fuori.append(ch)
        elif unicodedata.combining(ch):
            continue
        else:
            fuori.append("-")
    return "".join(fuori)


def slug(s: str, *, max_len: int | None = None, ripiego: str = "") -> str:
    """Identificatore stabile derivato da un titolo o da un nome.

    :param max_len: taglia il risultato a questa lunghezza. Il taglio
        avviene prima della ripulitura finale, così un id troncato non
        finisce mai con un trattino penzolante.
    :param ripiego: cosa restituire quando non resta nemmeno un carattere
        utile (un nome fatto di sole virgolette caporali, per dire).
        Vuoto se non specificato.
    """
    s = _NON_ALNUM.sub("-", piega_ascii(s).lower()).strip("-")
    if max_len is not None:
        s = s[:max_len].strip("-")
    return s or ripiego

# ---------------------------------------------------------------- link


# Link e immagini markdown: `[testo](destinazione)` e `![alt](destinazione)`.
# La destinazione si ferma alla prima parentesi chiusa o al primo spazio,
# così un titolo fra virgolette — `[x](y "titolo")` — resta fuori dal gruppo
# e viene riportato tale e quale.
_LINK_MD = re.compile(r'(!?\[[^\]]*\]\()([^)\s]+)([^)]*\))')

# Destinazioni che NON sono percorsi di file e non vanno mai riscritte.
# `URL` e simili sono segnaposto mai compilati: riscriverli significherebbe
# inventare una destinazione, quindi restano rotti e si contano a parte.
_NON_PERCORSO = re.compile(
    r'^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//|#|/|URL$|TODO$|\{)'
)


def link_e_relativo(destinazione: str) -> bool:
    """Vero se la destinazione è un percorso di file da riscalare.

    Fuori restano: URL con schema (``http:``, ``mailto:``), protocol-relative
    (``//host``), àncore (``#sezione``), percorsi assoluti (``/x``) e i
    segnaposto dei template (``URL``, ``TODO``, ``{...}``).
    """
    return bool(destinazione) and not _NON_PERCORSO.match(destinazione)


def riscala_link(testo: str, da_cartella, a_cartella) -> str:
    """Riscrive i link relativi di ``testo`` spostandolo di cartella.

    Un sorgente in ``07_arco/X.md`` che linka ``../plans/adr/Y.md`` punta
    alla radice del repo. Copiato alla lettera in
    ``07_arco/homebrew/sessione/BOOKLET.hb.md`` — due livelli più in basso —
    lo stesso link finisce su ``07_arco/homebrew/plans/adr/Y.md``, che non
    esiste. È il difetto che rendeva rotti **41 link su 44** negli otto
    booklet generati (lotto E1, 2026-09-12): i due generatori concatenavano
    il markdown alla lettera.

    Le àncore attaccate al percorso (``file.md#sezione``) sopravvivono, e la
    destinazione non viene normalizzata oltre il necessario: se il file non
    esiste il link resta rotto: questa funzione **sposta**, non indovina.

        >>> riscala_link("[a](../plans/x.md)", "07_arco", "07_arco/homebrew")
        '[a](../../plans/x.md)'
        >>> riscala_link("[a](https://x.dev)", "07_arco", "07_arco/homebrew")
        '[a](https://x.dev)'
    """
    da, a = PurePosixPath(str(da_cartella)), PurePosixPath(str(a_cartella))
    if da == a:
        return testo

    def _uno(m: "re.Match[str]") -> str:
        apre, dest, chiude = m.group(1), m.group(2), m.group(3)
        if not link_e_relativo(dest):
            return m.group(0)
        percorso, sep, ancora = dest.partition("#")
        if not percorso:                       # solo àncora dopo il partition
            return m.group(0)
        assoluto = os.path.normpath(str(da / percorso))
        nuovo = os.path.relpath(assoluto, str(a))
        return f"{apre}{nuovo}{sep}{ancora}{chiude}"

    return _LINK_MD.sub(_uno, testo)
