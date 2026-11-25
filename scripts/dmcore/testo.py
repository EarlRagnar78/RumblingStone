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
from pathlib import Path, PurePosixPath

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


# ── La storia delle scelte resta nel repo, non va in stampa ──────────────────
#
# Un booklet è per il tavolo. «Allineato il 2026-09-24 su decisione del DM»,
# «il box di prima diceva…», «[CANONE — DM 2026-07-31]» servono a chi lavora
# sul repo e sono rumore per chi gioca: il 2026-09-25 erano 161 righe nei 74
# file che i manifest stampano. Nel sorgente restano, e su GitHub si leggono;
# le due catene di stampa (HTML e Typst) le saltano, con la stessa funzione.
#
# Due forme. Il BLOCCO, scritto da chi scrive il master:
#
#     <!-- storico -->
#     > ✏️ Allineato il 2026-09-24: il box diceva «portatore…»
#     <!-- /storico -->
#
# e l'ATTRIBUZIONE in linea, riconosciuta da sola perché ha una forma fissa:
# `[CANONE — DM 2026-07-31]`, «(decisione DM 2026-09-24)», `[verif. ✓ …]`,
# «(ADR-0014 §1)». Si toglie solo la cornice: «(CANONE DM 2026-07-23: si
# aggancia al Cerchio Sacro)» diventa «(si aggancia al Cerchio Sacro)».

# Il blocco: i due marcatori ciascuno su una riga sua. Se l'apertura avesse
# del testo dopo, la regola arriverebbe fino al primo «/storico» che chiude una
# riga, anche venti righe più in basso: è successo, nel Palio, con l'intestazione.
#
# Lo stesso blocco con `consegna` al posto di `storico` chiude l'istruzione di
# consegna in testa a un foglio ✉ («Si consegna al risveglio…», «Il DM te la
# consegna dopo…»): è del DM, e la dice la regia della serata, non il foglio che
# il giocatore tiene in mano.
#
# E con `apparato` chiude i metadati del repo (ADR-0070, classe A): da quali
# file un master è stato fuso, il suo stato di consolidamento, «MASTER
# DEFINITIVO», i promemoria di sistema («MAI 5e», «CD non DC»), i nomi di file.
# Servono a chi lavora sul repo; la versione a ritroso la tiene git.
_STORICO_RIGHE = re.compile(
    r"^[ \t>]*<!--\s*(storico|consegna|apparato)\s*-->[ \t]*\n.*?^[ \t>]*<!--\s*/\1\s*-->[ \t]*(?:\n|\Z)",
    re.S | re.M)
_STORICO_IN_LINEA = re.compile(r"<!--\s*(storico|apparato)\s*-->.*?<!--\s*/\1\s*-->", re.S)
# Una riga di tabella non si può chiudere fra due marcatori senza spezzare la
# tabella su GitHub: si segna con `<!-- storico: riga -->` dentro una cella, e
# in stampa se ne va la riga intera.
_STORICO_RIGA = re.compile(r"^.*<!--\s*storico:\s*riga\s*-->.*(?:\n|\Z)", re.M)
_DATA = r"2026-\d\d-\d\d"
_ATTRIBUZIONI = (
    # «(canone DM 2026-07-30)» · «*(decisione DM 2026-09-24)*» · «(DM 2026-07-21)»
    # · «(com'è nei ritratti: decisione DM 2026-09-24)» — la parentesi è solo
    # un'attribuzione, e se ne va tutta.
    re.compile(r"[ \t]*\*?\((?:[^()\n]{0,40}?:\s*)?(?:CANONE |canone )?"
               r"(?:decision[ei] (?:del )?DM|DM)[ ,]*" + _DATA + r"(?:,\s*rettifica)?\)\*?"),
    # «*(decisione DM)*» senza data · «(verificato il 2026-09-24)» · `verif. ✓ …` senza parentesi
    re.compile(r"[ \t]*\*?\(decision[ei] (?:del )?DM\)\*?"),
    re.compile(r"[ \t]*\(verificat[oa] il " + _DATA + r"\)"),
    re.compile(r"[ \t]*`verif\. ✓[^`\n]*`"),
    # «(ADR-0057)» · «*(prove grezze, ADR-0022)*» · «`(ADR-0014)`»
    re.compile(r"[ \t]*[`*]?\((?:[^()\n]{0,40}?,\s*)?ADR-\d{4}(?:\s*§[\w.-]+)?\)[`*]?"),
)
# `[CANONE — DM 2026-07-31]` · `[CANONE GIOCATO 2026-07-31]` · `[verif. ✓ …]`
# · `[riscritto 2026-09-25 su richiesta del DM]`: la marca intera, anche quando
# va a capo dentro un paragrafo o sta in uno statblocco preformattato (nelle
# mappe una marca così non compare). Non attraversa una riga vuota.
_MARCA = re.compile(r"[ \t]*`?\[(?:CANONE\b|verif\. ✓|riscritt[oa]\b|ACCEPTED\b)"
                    r"(?:[^\]\n]|\n(?![ \t>]*\n)){0,400}\]`?")
_MARCA_RIGA = re.compile(r"[ \t]*`?\[(?:CANONE\b|verif\. ✓|riscritt[oa]\b|ACCEPTED\b)[^\]\n]{0,400}\]`?")
# «(CANONE DM 2026-07-23: si aggancia…» → «(si aggancia…»: il contenuto resta.
# Anche «(`[CANONE GIOCATO]`: …» → «(…».
_PREFISSO = re.compile(r"\((?:(?:CANONE|canone) DM " + _DATA + r"|`?\[CANONE[^\]\n]*\]`?):\s*")
# «(conseguenza canonica del Marchio, DM 2026-07-23)» → «(conseguenza canonica del Marchio)»
# e «(Varis ↔ Il Collezionista, CANONE DM 2026-07-23)»: dopo la virgola se ne va
# solo la coda, il contenuto resta.
_CODA = re.compile(r",\s*(?:CANONE,?\s*)?DM " + _DATA + r"\)")
# La marca che apre una riga dentro un paragrafo o una voce d'elenco e chiude
# la frase di prima: «…torrione ovest\n  `[CANONE — DM …]`. È una regola…».
# Tolta da sola lascerebbe il punto a colonna 0, e la voce d'elenco si
# spezzerebbe (rilievo di Codex sulla #507): il segno torna in coda alla riga
# di prima e la riga dopo tiene il suo rientro. Se la riga di prima è vuota
# o finisce già con un segno, la marca si toglie come le altre.
_MARCA_A_CAPO = re.compile(r"(?<=[^\s.,;:!?»)])\n([ \t>]*)`?\[(?:CANONE\b|verif\. ✓|riscritt[oa]\b|ACCEPTED\b)"
                           r"[^\]\n]{0,400}\]`?([.,;:])[ \t]*")
# La marca a inizio riga seguita da un trattino: «> `[CANONE GIOCATO …]` — registro…»
_MARCA_E_TRATTINO = re.compile(r"^([ \t>]*)`?\[CANONE[^\]\n]*\]`?\s*[—–-]\s*", re.M)


# La riga di metadati di una scheda del Bestiario («**Faction**: … | **Source**:
# creato per `…md` | **Status**: …») la leggono il catalogo e `validate_bestiario`;
# in un volume è apparato di forma fissa (ADR-0070, classe A) e se ne va da sola.
_METADATI_BESTIARIO = re.compile(r"^\*\*Faction\*\*:[^\n]*\*\*Source\*\*:[^\n]*(?:\n|\Z)", re.M)
# Due forme fisse di rimando a un file (classe A): la parentesi che contiene SOLO
# un percorso, con al più un paragrafo o una riga («(`Bracieri.md` §5)»,
# «(`01_Bracieri.md` r.83)»), e la citazione delle fonti in corsivo,
# «*(Fonte: `…md` §Scena C)*». Una parentesi con altro testo resta: dentro
# può esserci un fatto, e lo riscrive chi scrive.
#
# ⚠️ Ogni pezzo dopo il percorso comincia con uno spazio e non ne contiene: così
# la regex ha un solo modo di leggere una stringa. La prima stesura, con
# `\s*` facoltativo e `§[\w.-]+`, poteva spezzare «-r.0» in più modi, e CodeQL
# l'ha segnalata come backtracking esponenziale sulla #175.
_PARENTESI_FILE = re.compile(
    r"[ \t]*\(`[^`\n]+\.(?:md|json|ya?ml)`"
    r"(?:[ \t]+(?:§[\w.]+(?:-[a-z]+)?|r\.[ ]?\d+)){0,3}[ \t]*\)")
_CITAZIONE_FONTI = re.compile(r"[ \t]*\*\(Font[ei]:[^()]*?(?:\([^()]*\)[^()]*?)*\)\*")


def togli_blocchi_storici(md: str) -> str:
    """Solo la prima metà: i blocchi e le righe segnati a mano, non le attribuzioni."""
    md = _METADATI_BESTIARIO.sub("", md)
    md = _STORICO_RIGA.sub("", md)
    md = _STORICO_RIGHE.sub("", md)
    return _STORICO_IN_LINEA.sub("", md)


def togli_storico(md: str) -> str:
    """Il testo come va in stampa: senza blocchi storici né attribuzioni.

    >>> togli_storico("Prima.\\n<!-- storico -->\\n> diceva altro\\n<!-- /storico -->\\nDopo.")
    'Prima.\\nDopo.'
    >>> togli_storico("# Durik\\n\\n<!-- consegna -->\\n> *Si consegna al risveglio.*\\n<!-- /consegna -->\\n\\nEra il tuo cane.")
    '# Durik\\n\\n\\nEra il tuo cane.'
    >>> togli_storico("| 1 | resta |\\n| 7 | coperto <!-- storico: riga --> |\\n")
    '| 1 | resta |\\n'
    >>> togli_storico("> <!-- storico -->v1. <!-- /storico -->Modulo.\\n> Resta.\\n<!-- storico -->\\nvia\\n<!-- /storico -->\\n")
    '> Modulo.\\n> Resta.\\n'
    >>> togli_storico("## §5 — I TRE DONI `[CANONE — DM 2026-09-12]`")
    '## §5 — I TRE DONI'
    >>> togli_storico("Durik c'è *(decisione DM 2026-09-24)*: attraversa")
    "Durik c'è: attraversa"
    >>> togli_storico("(CANONE DM 2026-07-23: si aggancia al Cerchio)")
    '(si aggancia al Cerchio)'
    >>> togli_storico("Gancio muto (conseguenza canonica del Marchio, DM 2026-07-23).")
    'Gancio muto (conseguenza canonica del Marchio).'
    >>> togli_storico("### Le sei porte *(prove grezze, ADR-0022)*")
    '### Le sei porte'
    >>> togli_storico("(Varis ↔ Il Collezionista, CANONE DM 2026-07-23), mille anni")
    '(Varis ↔ Il Collezionista), mille anni'
    >>> togli_storico("~3g 20h** (`[CANONE GIOCATO]`: tre riposi")
    '~3g 20h** (tre riposi'
    >>> togli_storico("> `[CANONE GIOCATO 2026-07-31]` — registro dei riposi")
    '> registro dei riposi'
    >>> togli_storico("- nel torrione ovest\\n  `[CANONE — DM 2026-11-21]`. È una regola")
    '- nel torrione ovest.\\n  È una regola'
    >>> togli_storico("sul ramo del gruppo\\n(ADR-0007).")
    'sul ramo del gruppo.'
    >>> togli_storico("smeraldo) [CANONE — DM 2026-07-31;\\n> ERRATA: vecchie]. Poi")
    'smeraldo). Poi'
    >>> togli_storico("```\\nPUSH `[CANONE — DM,\\n9]`: una volta\\nALTRO `[CANONE]` x\\n```")
    '```\\nPUSH `[CANONE — DM,\\n9]`: una volta\\nALTRO x\\n```'
    >>> togli_storico("PX/PG `[verif. ✓ ERRATA 2026-07-23]` | ~2.400 `verif. ✓ WBL` fine")
    'PX/PG | ~2.400 fine'
    >>> togli_storico("### ✅ GIOCATO (DM 2026-07-31, rettifica) — B · ⏱️ **Quando** *(decisione DM)*: dopo")
    '### ✅ GIOCATO — B · ⏱️ **Quando**: dopo'
    >>> togli_storico("La prova (CD 15) resta.")
    'La prova (CD 15) resta.'
    >>> togli_storico("# Master\\n<!-- apparato -->\\n> **Sostituisce e fonde** `P2.md`.\\n<!-- /apparato -->\\nIl rito.")
    '# Master\\nIl rito.'
    >>> togli_storico("# Balvar\\n**Faction**: orda | **Source**: `X.md` | **Status**: ok\\n\\nNano.")
    '# Balvar\\n\\nNano.'
    >>> togli_storico("il contro esatto (`05_Bracieri.md` §5). Poi (`X.md`, «Limitazioni»: DES 8).")
    'il contro esatto. Poi (`X.md`, «Limitazioni»: DES 8).'
    >>> togli_storico("È il seme. *(Fonte: `Guida.md` §Scena C + `prova.md`.)* Fine.")
    'È il seme. Fine.'
    >>> togli_storico("Coerente con il canone<!-- apparato --> (`Corona-DM.md`, state.md §6)<!-- /apparato -->.")
    'Coerente con il canone.'
    """
    md = togli_blocchi_storici(md)
    md = _CITAZIONE_FONTI.sub("", md)
    md = "\n".join(_PARENTESI_FILE.sub("", r) if "`" in r and ".md" in r else r
                   for r in md.split("\n"))
    # Nella prosa una marca può andare a capo; in un blocco preformattato no,
    # perché togliendola si unirebbero due righe (lo statblocco di Terros
    # passava da 71 a 98 celle e finiva su una pagina A4 sua). Lì si toglie
    # solo la marca che si chiude sulla stessa riga.
    pezzi = re.split(r"(^[ \t]*```.*?^[ \t]*```[^\n]*$)", md, flags=re.S | re.M)
    for k, pezzo in enumerate(pezzi):
        if k % 2:
            pezzi[k] = _MARCA_RIGA.sub("", pezzo)
        else:
            pezzo = _PREFISSO.sub("(", pezzo)
            pezzo = _MARCA_E_TRATTINO.sub(r"\1", pezzo)
            pezzo = _MARCA_A_CAPO.sub(r"\2\n\1", pezzo)
            pezzi[k] = _MARCA.sub("", pezzo)
    md = "".join(pezzi)
    fuori: list[str] = []
    in_codice = False
    for riga in md.split("\n"):
        if riga.lstrip().startswith("```"):
            in_codice = not in_codice
        if not in_codice and ("2026-" in riga or "CANONE" in riga or "ADR-" in riga
                              or "verif." in riga or "ACCEPTED" in riga
                              or "decision" in riga):
            prima = riga
            riga = _MARCA_E_TRATTINO.sub(r"\1", riga)
            riga = _PREFISSO.sub("(", riga)
            riga = _CODA.sub(")", riga)
            for p in _ATTRIBUZIONI:
                riga = p.sub("", riga)
            # «(ADR-0007).» su una riga sua lascerebbe un punto isolato: la
            # punteggiatura torna in coda alla riga di prima.
            if riga != prima and re.fullmatch(r"\s*[.,;:]\s*", riga) and fuori and fuori[-1].strip():
                fuori[-1] = fuori[-1].rstrip() + riga.strip()
                continue
        fuori.append(riga)
    return "\n".join(fuori)


# ─────────────────────────────────────── i rimandi interni (ADR-0070, classe D)
#
# «master #3», «DEF-3 §7», «`ARC07-DEF-2` §0-bis» servono a chi lavora sul repo:
# in un volume stampato il lettore non ha file, ha capitoli. Se il master citato
# sta nello stesso volume il rimando diventa il suo capitolo («cap. IV §7»); se
# non c'è, `DEF-N` diventa il titolo del master, preso dal suo H1 standard
# («ARC-07 · DEFINITIVO #1 — IL PIANO DELLA TERRA & TERROS L'ANTICO» →
# «Il Piano della Terra & Terros l'Antico»): una colonna «Dove» di una tabella
# non resta vuota, e non serve nessuna convenzione nuova. La forma in prosa
# «master #N» fuori dal volume resta com'è: diventerebbe «nel «Il Piano…»», e
# la riscrive chi scrive; la vede il rilevatore dell'apparato.

_SEZIONE = r"(?:[ \t]+§[\w.]+(?:-[\w]+)*)?"
_RIF = (r"(?:master(?:[ \t]*\n[ \t>]*|[ \t]+)#(?P<n1>\d)"
        r"|`?(?:ARC\d\d-)?DEF-(?P<n2>\d)(?![\w-])`?)")
_H1_DEF = re.compile(r"^#\s+[^\n—]*—\s*([^\n(]+)", re.M)
#: Le parole che nel titolo restano minuscole (articoli, preposizioni, «e», «fa»).
_MINUSCOLE = set("il lo la i gli le l un uno una e ed o a ad da di del dello della dei "
                 "degli delle al allo alla ai agli alle dal dallo dalla nel nello nella "
                 "con su per fra tra fa".split())


def titolo_del_master(h1: str) -> str:
    """«IL PIANO DELLA TERRA & TERROS L'ANTICO» → «Il Piano della Terra & Terros l'Antico».

    >>> titolo_del_master("IL VIAGGIO A 1.000 ANNI FA")
    'Il Viaggio a 1.000 Anni fa'
    """
    fuori = []
    for k, parola in enumerate(h1.strip().split()):
        pezzi = parola.lower().split("'")
        pezzi = [q if (q in _MINUSCOLE and (k or j)) else q[:1].upper() + q[1:]
                 for j, q in enumerate(pezzi)]
        fuori.append("'".join(pezzi))
    return " ".join(fuori)
_RIF_PARENTESI = re.compile(r"[ \t]*\(\s*(?:→\s*|vedi\s+)?" + _RIF + r"(?P<sez>" + _SEZIONE + r")\s*\)")
_RIF_NUDO = re.compile(r"(?<![\w/.-])" + _RIF + r"(?P<sez>" + _SEZIONE + r")")
_NUMERO_ROMANO = re.compile(r"^\s*([IVXLC]+)\s*·")


class Volume(dict):
    """File → etichetta del capitolo, e per i master divisi in più capitoli
    (chiave `sezioni`) quali sezioni stanno in quale capitolo (`parti`)."""

    def __init__(self) -> None:
        super().__init__()
        self.parti: "dict[Path, list[tuple[str, list[str]]]]" = {}
        #: righe della guida ai capitoli (titolo, per chi, quando), dai
        #: capitoli del manifest con la chiave `quando`
        self.guida: "list[tuple[str, str, str]]" = []


def capitoli_del_volume(base: "Path", dato: dict) -> "dict[Path, str]":
    """File del volume → come lo si cita in stampa: «cap. IV», o il titolo.

    `base` è la cartella del manifest, a cui i capitoli sono relativi. Un
    master che dà più capitoli si cita col primo, salvo che il rimando dica
    la scena o la sezione: allora con il capitolo che la contiene
    (`capitolo_della_parte`). Un capitolo con `"principale": true` prende i
    rimandi al master che non dicono la parte, anche se non è il primo.

    >>> d = {"chapters": [{"title": "Il riferimento rapido", "file": "m.md", "sezioni": ["§0-bis"]},
    ...                   {"title": "VII · Atto II", "file": "m.md", "sezioni": ["SCENA 6"], "principale": True}]}
    >>> list(capitoli_del_volume(Path("/x"), d).values())
    ['cap. VII']
    """
    fuori = Volume()
    principali = {(base / c["file"]).resolve() for c in dato.get("chapters", [])
                  if isinstance(c, dict) and "file" in c and c.get("principale")}
    for c in dato.get("chapters", []):
        if not isinstance(c, dict) or "file" not in c:
            continue
        titolo = c.get("title", "")
        m = _NUMERO_ROMANO.match(titolo)
        etichetta = f"cap. {m.group(1)}" if m else f"«{titolo.strip()}»"
        f = (base / c["file"]).resolve()
        if f not in principali:
            fuori.setdefault(f, etichetta)
        elif c.get("principale"):
            fuori[f] = etichetta        # chi cita il master senza la parte arriva qui
        if c.get("sezioni"):
            fuori.parti.setdefault(f, []).append((etichetta, list(c["sezioni"])))
        if c.get("quando"):
            chi = "✉" if c.get("tag") == "player" else "⚠ DM"
            fuori.guida.append((titolo.strip(), chi, c["quando"]))
    if fuori.guida:
        fuori.guida += [tuple(r) for r in dato.get("guida_righe_finali", [])]
    return fuori


# La guida ai capitoli («Come usare questo booklet»): fra questi due segni la
# tabella la scrive il manifest, se i capitoli hanno la chiave `quando`. Scritta
# a mano si guastava al primo riordino (la serata di ARC-07 stampava la guida
# del booklet lungo, 2026-11-19).
_GUIDA = re.compile(r"<!--\s*guida-capitoli\s*-->\n(.*?)<!--\s*/guida-capitoli\s*-->\n?", re.S)


def guida_capitoli(md: str, capitoli) -> str:
    """La tabella fra i segni `guida-capitoli`, rifatta dal manifest.

    >>> v = Volume(); v.guida = [("I · Regia", "⚠ DM", "prima")]
    >>> guida_capitoli("<!-- guida-capitoli -->\\n| x |\\n<!-- /guida-capitoli -->\\n", v)
    '| Capitolo | Per chi | Quando |\\n|---|---|---|\\n| I · Regia | ⚠ DM | prima |\\n'
    """
    righe = getattr(capitoli, "guida", None)
    if not righe:
        return _GUIDA.sub(lambda m: m.group(1), md)
    tabella = "| Capitolo | Per chi | Quando |\n|---|---|---|\n" + "".join(
        f"| {t} | {chi} | {quando} |\n" for t, chi, quando in righe)
    return _GUIDA.sub(lambda m: tabella, md)


# Il master va a capo dove vuole: «(`DEF-4`\nAppendice C.3)» è lo stesso rimando
# di «(`DEF-4` Appendice C.3)» (la regia della serata stampava «cap. V
# Appendice C.3» invece di «cap. VIII», 2026-11-19).
_PARTE = re.compile(r"\s*,?\s*(?:(?P<scena>[Ss]cen[ae])\s+(?P<num>\d+(?:[ \t]*(?:e|-|–|,)[ \t]*\d+)*)"
                    r"|(?P<sez>§[\w.]+(?:-[\w]+)*)|[Aa]ppendice\s+(?P<app>[A-Z](?:\.\d+)?(?:-bis)?))")
# La parte detta PRIMA del master: «il §7 di `DEF-4`», «nelle Scene 7 e 8 di `DEF-4`».
_PARTE_PRIMA = re.compile(r"(?:(?P<scena>[Ss]cen[ae])\s+(?P<num>\d+(?:[ \t]*(?:e|-|–|,)[ \t]*\d+)*)"
                          r"|(?P<sez>§[\w.]+(?:-[\w]+)*))\s+(?:di|del|nel)\s+\(?$")

#: Il master diviso è citato per una parte che questo volume non stampa.
FUORI_DAL_VOLUME = "fuori"


def capitolo_della_parte(capitoli: "dict[Path, str]", f: "Path", sez: str, dopo: str,
                         prima: str = "") -> "str | None":
    """Il capitolo di un master diviso che contiene la parte citata.

    `sez` è il «§N» già letto dal rimando, `dopo` il testo che lo segue
    («Scena 11», «Scene 10 e 11», «Appendice A.1»). None se il master non è
    diviso o la parte non si riconosce: allora vale l'etichetta del primo
    capitolo. `FUORI_DAL_VOLUME` se la parte si riconosce ma questo volume
    non la stampa: allora il rimando va al master, cioè al volume d'arco.

    >>> v = Volume(); f = Path("/x/DEF-4.md")
    >>> v[f] = "cap. V"; v.parti[f] = [("cap. V", ["SCENA 6", "C.2"]), ("cap. IX", ["SCENA 11", "§6 —", "C.3"])]
    >>> capitolo_della_parte(v, f, "", " Scena 11, la passata"), capitolo_della_parte(v, f, "§6", "")
    ('cap. IX', 'cap. IX')
    >>> capitolo_della_parte(v, f, "", " Appendice C.2"), capitolo_della_parte(v, f, "", " Scena 1)")
    ('cap. V', 'fuori')
    >>> capitolo_della_parte(v, f, "", " Scene 6 e 11"), capitolo_della_parte(v, f, "", " Scene 6-7")
    ('capp. V e IX', 'cap. V')
    >>> capitolo_della_parte(v, f, "", "\\nAppendice C.3)"), capitolo_della_parte(v, f, "", ")", prima="il §6 di ")
    ('cap. IX', 'cap. IX')
    >>> g = Path("/x/barile.md"); v[g] = "cap. V"; v.parti[g] = [("cap. V", ["8."]), ("cap. XIII", ["10."])]
    >>> capitolo_della_parte(v, g, "§10", ""), capitolo_della_parte(v, g, "§8", "")
    ('cap. XIII', 'cap. V')
    >>> v.parti[f].append(("cap. XIV", ["B. Tesoro", "A.1 ·"]))
    >>> capitolo_della_parte(v, f, "", " B. Tesoro)"), capitolo_della_parte(v, f, "", " B. qualcosa)")
    ('cap. XIV', None)
    """
    parti = getattr(capitoli, "parti", {}).get(f)
    if not parti:
        return None
    if sez.strip():
        toks = [sez.strip()]
    else:
        m = _PARTE.match(dopo) or _PARTE_PRIMA.search(prima)
        if not m:
            # Una parte citata col suo titolo («`DEF-4` B. Tesoro»): vale se
            # il testo che segue comincia con una voce di `sezioni` di almeno
            # sei caratteri, perché due lettere qualunque non bastano.
            testo_dopo = _normale(dopo.lstrip(" ,"))
            for etichetta, voci in parti:
                for v in voci:
                    v = _normale(v[len("testa:"):] if v.startswith("testa:") else v)
                    if len(v) >= 6 and testo_dopo.startswith(v):
                        return etichetta
            return None
        if m.group("scena"):
            toks = ["scena " + n for n in re.findall(r"\d+", m.group("num"))]
        else:
            toks = [m.group("sez") or m.group("app")]

    def dove(tok: str) -> "str | None":
        t = _normale(tok)
        # «§10» di un master a paragrafi numerati («## 10. Che cosa cambia»)
        # è la voce «10.» del manifest
        numerato = t[1:] + "." if re.fullmatch(r"§\d+(-bis)?", t) else None
        for etichetta, voci in parti:
            for v in voci:
                v = _normale(v[len("testa:"):] if v.startswith("testa:") else v)
                if v.startswith(t) and (len(v) == len(t) or not (v[len(t)].isalnum() or v[len(t)] in "-.")):
                    return etichetta
                if numerato and v == numerato:
                    return etichetta
        return None

    trovati = [d for d in map(dove, toks) if d]
    if not trovati:
        return FUORI_DAL_VOLUME
    unici = list(dict.fromkeys(trovati))
    if len(unici) == 1:
        return unici[0]
    return "capp. " + " e ".join(u.removeprefix("cap. ") for u in unici)


# Un nome di file fra backtick, anche abbreviato con «...» o «…» davanti
# («`...P2D-PALIO-DM-MASTER-REFERENCE.md` §3»): se è un capitolo del volume
# diventa il suo capitolo, come «DEF-3».
# Il token si prende intero e la coda si calcola dopo: una regex che separa
# prefisso e nome in due gruppi adiacenti può farlo in troppi modi (CodeQL, #175).
_NOME_DI_FILE = re.compile(r"`(?P<tok>[^`\s]+\.md)`(?P<sez>" + _SEZIONE + r")")


def _traduci_nomi_di_file(md: str, io: "Path", capitoli: "dict[Path, str]") -> str:
    """`X.md` → «cap. IV» quando X è un capitolo di questo volume. Pura.

    >>> import pathlib
    >>> a, b = pathlib.Path("/v/A-MASTER.md"), pathlib.Path("/v/B-ALLEGATO.md")
    >>> _traduci_nomi_di_file("Allegato di `...A-MASTER.md` §3, e `Z.md`.", b, {a: "cap. I", b: "cap. II"})
    'Allegato di cap. I §3, e `Z.md`.'
    >>> _traduci_nomi_di_file("Vedi `B-ALLEGATO.md`.", b, {a: "cap. I", b: "cap. II"})
    'Vedi questo capitolo.'

    Un master diviso in più capitoli (`sezioni`) manda il §N al capitolo che
    stampa quella parte (2026-11-19: il §10 del barile andava al cap. V):

    >>> v = Volume(); v[a] = "cap. V"; v.parti[a] = [("cap. V", ["8."]), ("cap. XIII", ["10."])]
    >>> _traduci_nomi_di_file("(`A-MASTER.md` §10) e (`A-MASTER.md` §8)", b, v)
    '(cap. XIII §10) e (cap. V §8)'
    """
    def sostituisci(m: "re.Match") -> str:
        coda = m.group("tok").replace("\\", "/").rsplit("/", 1)[-1].lstrip(".…")
        trovati = [f for f in capitoli if f.name == coda or f.name.endswith(coda)]
        if len(trovati) != 1:
            return m.group(0)
        sez = (m.group("sez") or "").strip()
        if trovati[0] == io:
            return sez or "questo capitolo"
        parte = capitolo_della_parte(capitoli, trovati[0], sez, m.string[m.end():m.end() + 40],
                                     m.string[max(0, m.start() - 40):m.start()])
        if parte == FUORI_DAL_VOLUME:
            parte = None
        return (parte or capitoli[trovati[0]]) + (" " + sez if sez else "")

    pezzi = re.split(r"(^[ \t]*```.*?^[ \t]*```[^\n]*$)", md, flags=re.S | re.M)
    for k in range(0, len(pezzi), 2):
        pezzi[k] = _NOME_DI_FILE.sub(sostituisci, pezzi[k])
    return "".join(pezzi)


_TITOLO_MD = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
_RECINTO = re.compile(r"^[ \t]*(```|~~~)")
_MARCHE_DI_BLOCCO = ("storico", "apparato", "consegna")


def _normale(t: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t)).strip().casefold()


def _blocchi_aperti(md: str) -> "list[str]":
    """I blocchi `storico`/`apparato`/`consegna` aperti alla fine di `md`.

    >>> _blocchi_aperti("<!-- storico -->\\nx\\n<!-- /storico -->\\n<!-- apparato -->\\n")
    ['apparato']
    """
    aperti: "list[str]" = []
    for m in re.finditer(r"^[ \t]*<!--\s*(/?)(" + "|".join(_MARCHE_DI_BLOCCO) + r")\s*-->[ \t]*$", md, re.M):
        if m.group(1):
            if m.group(2) in aperti:
                aperti.remove(m.group(2))
        else:
            aperti.append(m.group(2))
    return aperti


def _bilancia_marche(md: str) -> str:
    """Toglie le marche `<!-- x -->` / `<!-- /x -->` rimaste spaiate da un taglio.

    >>> _bilancia_marche("Testo.\\n<!-- storico -->\\n")
    'Testo.\\n'
    >>> _bilancia_marche("<!-- /apparato -->\\nResta.\\n<!-- apparato -->via<!-- /apparato -->")
    'Resta.\\n<!-- apparato -->via<!-- /apparato -->'
    """
    for nome in _MARCHE_DI_BLOCCO:
        tok = re.compile(r"<!--\s*(/?)" + nome + r"\s*-->\n?")
        aperte: list = []
        via: list = []
        for m in tok.finditer(md):
            if m.group(1):
                (aperte.pop() if aperte else via.append(m))
            else:
                aperte.append(m)
        for m in sorted(via + aperte, key=lambda m: m.start(), reverse=True):
            md = md[:m.start()] + md[m.end():]
    return md


_PAGINA_APRE = re.compile(r"^\s*<!--\s*pagina:[^>]*-->\s*$")
_PAGINA_CHIUDE = re.compile(r"^\s*<!--\s*/pagina\s*-->\s*$")


def _con_la_pagina(righe: "list[str]", inizio: int, fine: int) -> str:
    """Il pezzo `righe[inizio:fine]` con la sua impaginazione: se cade dentro
    un `<!-- pagina: … -->` del master lo riapre e lo richiude, e un'apertura
    rimasta in coda (è della sezione dopo) la toglie.

    >>> r = ["a\\n", "<!-- pagina: una-colonna -->\\n", "## B\\n", "tab\\n", "## C\\n", "<!-- /pagina -->\\n"]
    >>> _con_la_pagina(r, 0, 2), _con_la_pagina(r, 2, 4)
    ('a\\n', '<!-- pagina: una-colonna -->\\n## B\\ntab\\n<!-- /pagina -->\\n')
    """
    aperta = None
    for r in righe[:inizio]:
        if _PAGINA_APRE.match(r):
            aperta = r
        elif _PAGINA_CHIUDE.match(r):
            aperta = None
    pezzo = list(righe[inizio:fine])
    if aperta:
        pezzo.insert(0, aperta)
    stato, ultima = None, -1
    tenute = []
    for r in pezzo:
        if _PAGINA_APRE.match(r):
            stato, ultima = r, len(tenute)
        elif _PAGINA_CHIUDE.match(r):
            if stato is None:
                continue                      # chiusura senza apertura: via
            stato = None
        tenute.append(r)
    if stato is not None:
        coda = "".join(tenute[ultima + 1:]).strip()
        if not coda or set(coda) <= set("-\n "):
            del tenute[ultima]                # l'apertura è della sezione dopo
        else:
            tenute.append("<!-- /pagina -->\n")
    return "".join(tenute).rstrip("\n") + "\n"


def estrai_sezioni(md: str, voci: "list[str]") -> str:
    """Solo le sezioni del master che il volume chiede, nell'ordine chiesto.

    Ogni voce è l'inizio del testo di un titolo markdown (senza i `#`, senza
    distinguere maiuscole); la sezione va dal titolo al titolo seguente di
    livello uguale o più alto. I `#` dentro i recinti di codice non sono
    titoli. Una voce che non trova il suo titolo, o ne trova due, ferma la
    stampa: un capitolo con un pezzo mancante non deve uscire in silenzio.
    `testa:§2` prende solo il testo del titolo fino al primo sottotitolo.

    >>> md = "# M\\n## §1 — A\\nuno\\n### Dett\\nd\\n## §2 — B\\n```\\n# non è un titolo\\n```\\n## §3 — C\\ntre\\n"
    >>> print(estrai_sezioni(md, ["§3", "§1"]), end="")
    ## §3 — C
    tre
    <BLANKLINE>
    ## §1 — A
    uno
    ### Dett
    d
    >>> print(estrai_sezioni(md, ["testa:§1"]), end="")
    ## §1 — A
    uno
    >>> estrai_sezioni(md, ["§9"])
    Traceback (most recent call last):
    ...
    ValueError: sezione non trovata: '§9'

    Una sezione dentro un blocco `storico` o `apparato` resta dentro il suo
    blocco (2026-11-19: il §12 «Domande al DM» del barile, avvolto in
    `storico`, usciva nel volume d'arco quando lo si chiedeva per nome):

    >>> md2 = "## 11. A\\nuno\\n<!-- storico -->\\n## 12. B\\ndue\\n<!-- /storico -->\\n## 13. C\\n"
    >>> print(estrai_sezioni(md2, ["12."]), end="")
    <!-- storico -->
    ## 12. B
    due
    <!-- /storico -->
    """
    righe = md.splitlines(keepends=True)
    titoli: "list[tuple[int, int, str]]" = []   # (riga, livello, testo)
    nel_recinto = False
    for i, r in enumerate(righe):
        if _RECINTO.match(r):
            nel_recinto = not nel_recinto
            continue
        m = None if nel_recinto else _TITOLO_MD.match(r.rstrip("\n"))
        if m:
            titoli.append((i, len(m.group(1)), _normale(m.group(2))))
    pezzi = []
    for voce in voci:
        solo_testa = voce.startswith("testa:")
        v = _normale(voce[len("testa:"):] if solo_testa else voce)
        trovati = [k for k, t in enumerate(titoli) if t[2].startswith(v)]
        if not trovati:
            raise ValueError(f"sezione non trovata: {voce!r}")
        if len(trovati) > 1:
            raise ValueError(f"sezione ambigua: {voce!r} ({len(trovati)} titoli)")
        k = trovati[0]
        inizio, livello, _ = titoli[k]
        fine = next((t[0] for t in titoli[k + 1:]
                     if solo_testa or t[1] <= livello), len(righe))
        pezzo = _con_la_pagina(righe, inizio, fine)
        aperti = _blocchi_aperti("".join(righe[:inizio]))
        if aperti:
            pezzo = "".join(f"<!-- {n} -->\n" for n in aperti) + pezzo
        pezzi.append(_bilancia_marche(pezzo))
    return "\n".join(pezzi)


def leggi_per_la_stampa(f: "Path", capitoli: "dict[Path, str]",
                        sezioni: "list[str] | None" = None) -> str:
    """Il sorgente di un capitolo con i rimandi già tradotti per questo volume.

    `sezioni` (chiave `sezioni` del capitolo nel manifest): solo quei pezzi
    del master, per il booklet di serata (ADR-0122).
    """
    md = f.read_text(encoding="utf-8")
    if sezioni:
        md = estrai_sezioni(md, sezioni)
        md = _SENZA_SCHEDA.sub("", md)
        # non in testa al capitolo, che comincia già a pagina nuova
        md = _SCENA_CON_SCHEDA.sub(
            lambda m: m.group(1) if not md[:m.start()].strip() else "<!-- nuova-pagina -->\n\n" + m.group(1), md)
    else:
        md = togli_schede_da_tavolo(_SEGNO_SENZA_SCHEDA.sub("", md))
    return togli_etichette_pilastri(traduci_rimandi(guida_capitoli(md, capitoli), f, capitoli))


# Le etichette dei pilastri di stile («Read-aloud (Andor lead)», «(pilastro
# GoT)») servono a chi scrive e a `misura_craft`: al tavolo sono rumore. Scelta
# di Jfs del 2026-11-19 (card del thread della prosa): restano nel sorgente e
# non si stampano, né nella serata né nel volume d'arco.
_PILASTRO = (r"(?:Salvatore|LotR|Tolkien|Casa di Davide|Andor|GoT|Game of Thrones|Mercer"
             r"|BG3|BG ?1 ?[-–/] ?2|BG1|BG2)")
_VOCE_PILASTRO = re.compile(rf"^(?:{_PILASTRO}\s+(?:lead|support)(?:\s+qui)?|pilastro\s+{_PILASTRO})$", re.I)
_PARENTESI = re.compile(r"[ \t]?(?P<e>)\((?P<d>[^()\n]*)\)")
#: la stessa parentesi in corsivo o in grassetto: si toglie con i suoi asterischi
_PARENTESI_ENFASI = re.compile(r"[ \t]?(?P<e>[*_]{1,2})\((?P<d>[^()\n]*)\)(?P=e)")


def togli_etichette_pilastri(md: str) -> str:
    """Toglie dal testo da stampare le etichette dei pilastri, e solo quelle.

    >>> togli_etichette_pilastri("**Read-aloud (Andor lead)** — la tenda.")
    '**Read-aloud** — la tenda.'
    >>> togli_etichette_pilastri("Read-aloud (Salvatore lead, solo per Artemis) — il corridoio")
    'Read-aloud (solo per Artemis) — il corridoio'
    >>> togli_etichette_pilastri("### ⚖️ Il grigio — perché crede di aver ragione (pilastro GoT)")
    '### ⚖️ Il grigio — perché crede di aver ragione'
    >>> togli_etichette_pilastri("### Il grigio — perché **crede di aver ragione** *(pilastro GoT)*")
    '### Il grigio — perché **crede di aver ragione**'
    >>> togli_etichette_pilastri("HELLA — la seconda vita (BG3 lead — il ritorno che conta)")
    'HELLA — la seconda vita (il ritorno che conta)'
    >>> togli_etichette_pilastri("(LotR lead + liturgia) e (support/buff), il pilastro di mithral")
    '(liturgia) e (support/buff), il pilastro di mithral'
    """
    def pulisci(m: "re.Match") -> str:
        enfasi = m.group("e") or ""
        dentro = m.group("d")
        if not re.search(_PILASTRO, dentro, re.I):
            return m.group(0)
        voci = [v.strip() for v in re.split(r"\s*(?:,|—|\+)\s*", dentro)]
        resto = [v for v in voci if v and not _VOCE_PILASTRO.match(v)]
        if len(resto) == len([v for v in voci if v]):
            return m.group(0)
        spazio = m.group(0)[0] if m.group(0)[0] in " \t" else ""
        return f"{spazio}{enfasi}({', '.join(resto)}){enfasi}" if resto else ""
    md = _PARENTESI_ENFASI.sub(pulisci, md)
    return _PARENTESI.sub(pulisci, md)


# La scheda da tavolo che apre una scena (prova del 2026-11-12, ADR-0122): una
# tabella larga con quello che serve per condurla. Si stampa nel booklet di
# serata, cioè nei capitoli presi per `sezioni`; nei volumi che stampano il
# master intero resta fuori finché il giro dei lettori non la promuove.
_SCHEDA_DA_TAVOLO = re.compile(r"\n<!--\s*scheda-da-tavolo\s*-->.*?<!--\s*/scheda-da-tavolo\s*-->\n", re.S)


# La scena che ha la scheda comincia a pagina nuova: titolo e scheda stanno
# nella stessa pagina (giro del 2026-11-12: il float finiva una o due pagine
# dopo il titolo, o sopra la coda della scena prima).
_SCENA_CON_SCHEDA = re.compile(r"^(#{2,4} [^\n]+\n(?:(?!#{1,4} )[^\n]*\n){0,12}?<!--\s*scheda-da-tavolo\s*-->)", re.M)


# Quel che la scheda da tavolo sostituisce (il riassunto «In tre righe») sta
# nel master fra `<!-- senza-scheda -->` e `<!-- /senza-scheda -->`: si stampa
# nei volumi che la scheda non la stampano, e sparisce dove la scheda c'è
# (fusione dei tre strati, Jfs 2026-11-12).
_SENZA_SCHEDA = re.compile(r"<!--\s*senza-scheda\s*-->\n.*?<!--\s*/senza-scheda\s*-->\n\n?", re.S)
_SEGNO_SENZA_SCHEDA = re.compile(r"<!--\s*/?senza-scheda\s*-->\n")
_CONTRATTO_IN_SCENA = re.compile(r"^\*\*In scena\*\*\s*—\s*Dove:\s*(?P<dove>.*?)\s*—\s*Chi:.*$")
_APRE_SCHEDA = re.compile(r"^<!--\s*scheda-da-tavolo\s*-->$")


def fondi_contratto_e_scheda(md: str) -> str:
    """La riga «In scena» di una scena con la scheda da tavolo entra nella
    scheda: il «Dove» diventa la sua prima riga, il «Chi» lo dice già «Chi c'è».
    Si chiama dopo `chi_si_incontra.arricchisci`, che quella riga la legge.

    >>> print(fondi_contratto_e_scheda("### S\\n\\n**In scena** — Dove: la tenda — Chi: Zog'tar\\n\\n"
    ...     "<!-- scheda-da-tavolo -->\\n| Scena | x |\\n|---|---|\\n| **Chi c'è** | Zog'tar |\\n"))
    ### S
    <BLANKLINE>
    <!-- scheda-da-tavolo -->
    | Scena | x |
    |---|---|
    | **Dove** | La tenda |
    | **Chi c'è** | Zog'tar |
    <BLANKLINE>

    Senza scheda prima del titolo dopo, la riga resta:

    >>> fondi_contratto_e_scheda("**In scena** — Dove: a — Chi: b\\n\\n### T\\n")
    '**In scena** — Dove: a — Chi: b\\n\\n### T\\n'
    """
    righe = md.split("\n")
    fuori: list[str] = []
    i = 0
    while i < len(righe):
        m = _CONTRATTO_IN_SCENA.match(righe[i])
        if m:
            j = i + 1
            while j < len(righe) and not re.match(r"#{1,4} ", righe[j]) and not _APRE_SCHEDA.match(righe[j]):
                j += 1
            k = next((n for n in range(j, min(j + 6, len(righe))) if re.match(r"\|\s*-{3,}", righe[n])), None) \
                if j < len(righe) and _APRE_SCHEDA.match(righe[j]) else None
            if k is not None:
                dove = m.group("dove")
                fine = next((n for n in range(k, len(righe))
                             if re.match(r"<!--\s*/scheda-da-tavolo\s*-->$", righe[n])), len(righe) - 1)
                # «Succede» apre la scheda, «Dove» la segue
                if k + 1 < len(righe) and righe[k + 1].startswith("| **Succede**"):
                    k += 1
                # la scheda subito sotto il titolo: quel che `arricchisci` ha
                # portato fra la riga «In scena» e la scheda viene dopo
                fuori += righe[j:k + 1]
                fuori.append(f"| **Dove** | {dove[:1].upper()}{dove[1:]} |")
                fuori += righe[k + 1:fine + 1]
                in_mezzo = righe[i + 1:j]
                while in_mezzo and in_mezzo[0] == "":
                    in_mezzo.pop(0)
                while in_mezzo and in_mezzo[-1] == "":
                    in_mezzo.pop()
                if in_mezzo:
                    fuori += [""] + in_mezzo
                i = fine + 1
                continue
        fuori.append(righe[i])
        i += 1
    return "\n".join(fuori)


def togli_schede_da_tavolo(md: str) -> str:
    """Il master senza le schede da tavolo delle scene.

    >>> togli_schede_da_tavolo("a\\n\\n<!-- scheda-da-tavolo -->\\n| x |\\n<!-- /scheda-da-tavolo -->\\nb")
    'a\\nb'
    """
    return _SCHEDA_DA_TAVOLO.sub("", md)


def _radice_dell_arco(sorgente: Path) -> "Path | None":
    for d in (sorgente.parent, *sorgente.parents):
        if any(d.glob("ARC*-DEF-*.md")):
            return d
    return None


def traduci_rimandi(md: str, sorgente: Path, capitoli: "dict[Path, str]") -> str:
    """I rimandi ai master tradotti nel capitolo del volume, o tolti.

    >>> import tempfile, pathlib
    >>> d = pathlib.Path(tempfile.mkdtemp())
    >>> for n in (1, 2, 3): _ = (d / f"ARC07-DEF-{n}-X.md").write_text("x")
    >>> vol = {(d / "ARC07-DEF-2-X.md").resolve(): "cap. III", (d / "ARC07-DEF-3-X.md").resolve(): "cap. IV"}
    >>> io = d / "ARC07-DEF-2-X.md"
    >>> traduci_rimandi("prima della resurrezione (master #3). Poi il master #3 §7.", io, vol)
    'prima della resurrezione (cap. IV). Poi il cap. IV §7.'
    >>> traduci_rimandi("dopo la Terra (master #1), e `ARC07-DEF-2` §0-bis.", io, vol)
    'dopo la Terra, e §0-bis.'
    >>> traduci_rimandi("progettato nel master #1 §10.", io, vol)
    'progettato nel master #1 §10.'
    >>> traduci_rimandi("```\\nDEF-3\\n```", io, vol)
    '```\\nDEF-3\\n```'
    >>> _ = (d / "ARC07-DEF-1-X.md").write_text("# ARC-07 · DEFINITIVO #1 — IL PIANO DELLA TERRA (x)")
    >>> traduci_rimandi("| Terros | `DEF-1` §8 |, e DEF-3 §7, come nel master #1.", io, vol)
    '| Terros | «Il Piano della Terra» §8 |, e cap. IV §7, come nel master #1.'

    Un capitolo che sta fuori dall'arco, come la pagina di un artefatto,
    trova i master nella cartella dei capitoli del volume:

    >>> fuori = pathlib.Path(tempfile.mkdtemp()) / "Collana.md"
    >>> traduci_rimandi("statblocco in `DEF-3`, Appendice A.2", fuori, vol)
    'statblocco in cap. IV, Appendice A.2'
    """
    io = sorgente.resolve()
    md = _traduci_nomi_di_file(md, io, capitoli)
    radice = _radice_dell_arco(sorgente)
    if radice is None:
        radice = next(filter(None, map(_radice_dell_arco, sorted(capitoli))), None)
    if radice is None:
        return md

    def bersaglio(m: "re.Match") -> "tuple[Path | None, str]":
        n = m.group("n1") or m.group("n2")
        trovati = sorted(radice.glob(f"ARC*-DEF-{n}-*.md"))
        return (trovati[0].resolve() if trovati else None), (m.group("sez") or "").strip()

    def titolo(dove: "Path") -> "str | None":
        m = _H1_DEF.search(dove.read_text(encoding="utf-8")[:2000])
        return f"«{titolo_del_master(m.group(1))}»" if m else None

    def in_parentesi(m: "re.Match") -> str:
        dove, sez = bersaglio(m)
        if dove is None:
            return m.group(0)
        if dove == io:
            return f" ({sez})" if sez else ""
        parte = capitolo_della_parte(capitoli, dove, sez, m.string[m.end():m.end() + 40],
                                     m.string[max(0, m.start() - 40):m.start()])
        if parte == FUORI_DAL_VOLUME:
            parte = titolo(dove)
        etichetta = parte or capitoli.get(dove) or titolo(dove)
        if etichetta:
            return f" ({etichetta}{' ' + sez if sez else ''})"
        return ""

    def nudo(m: "re.Match") -> str:
        dove, sez = bersaglio(m)
        if dove is None:
            return m.group(0)
        if dove == io:
            return sez or "questo capitolo"
        # «nel master #1» con un titolo diventerebbe «nel «Il Piano della
        # Terra»»: dentro una frase, fuori dal volume, lo riscrive chi scrive.
        parte = capitolo_della_parte(capitoli, dove, sez, m.string[m.end():m.end() + 40],
                                     m.string[max(0, m.start() - 40):m.start()])
        if parte == FUORI_DAL_VOLUME:
            parte = titolo(dove)
        etichetta = parte or capitoli.get(dove) or (None if m.group("n1") else titolo(dove))
        if etichetta:
            return etichetta + (" " + sez if sez else "")
        return m.group(0)

    pezzi = re.split(r"(^[ \t]*```.*?^[ \t]*```[^\n]*$)", md, flags=re.S | re.M)
    for k, pezzo in enumerate(pezzi):
        if k % 2 == 0:
            pezzi[k] = _RIF_NUDO.sub(nudo, _RIF_PARENTESI.sub(in_parentesi, pezzo))
    return "".join(pezzi)


_SIGLA_APPENDICE_A = re.compile(r"\b[Aa]ppendice\s+A(?:\.\d+(?:-(?:bis|ter))?)?(?![\w-])(?!\.\d)")
_SIGLA_APPENDICE_D = re.compile(r"\b[Aa]ppendice\s+D(?![\w-])(?!\.\d)")


def sigle_d_appendice(md: str) -> str:
    """Nel booklet di serata (manifest «prima-volta», ADR-0122) le appendici
    del master non si stampano con le loro sigle: «Appendice A.2» è
    l'appendice delle creature del volume, «Appendice D» quella delle mappe.
    Un capitolo che stampa lui la sua «APPENDICE A» resta com'è.

    >>> sigle_d_appendice("(Appendice A.2; EL 16) e la mappa M7-C (Appendice D).")
    '(appendice delle creature, in fondo; EL 16) e la mappa M7-C (appendice delle mappe, in fondo).'
    >>> sigle_d_appendice("Numeri in Appendice A.4. Poi")
    'Numeri in appendice delle creature, in fondo. Poi'
    >>> sigle_d_appendice("## APPENDICE A — STATISTICHE\\n\\nvedi Appendice A.2").endswith("vedi Appendice A.2")
    True
    """
    if re.search(r"^#{1,4}\s+APPENDICE [AD]\b", md, re.M):
        return md
    md = _SIGLA_APPENDICE_A.sub("appendice delle creature, in fondo", md)
    return _SIGLA_APPENDICE_D.sub("appendice delle mappe, in fondo", md)
