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


def capitoli_del_volume(base: "Path", dato: dict) -> "dict[Path, str]":
    """File del volume → come lo si cita in stampa: «cap. IV», o il titolo.

    `base` è la cartella del manifest, a cui i capitoli sono relativi.
    """
    fuori: "dict[Path, str]" = {}
    for c in dato.get("chapters", []):
        if not isinstance(c, dict) or "file" not in c:
            continue
        titolo = c.get("title", "")
        m = _NUMERO_ROMANO.match(titolo)
        fuori[(base / c["file"]).resolve()] = (
            f"cap. {m.group(1)}" if m else f"«{titolo.strip()}»")
    return fuori


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
    """
    def sostituisci(m: "re.Match") -> str:
        coda = m.group("tok").replace("\\", "/").rsplit("/", 1)[-1].lstrip(".…")
        trovati = [f for f in capitoli if f.name == coda or f.name.endswith(coda)]
        if len(trovati) != 1:
            return m.group(0)
        sez = (m.group("sez") or "").strip()
        if trovati[0] == io:
            return sez or "questo capitolo"
        return capitoli[trovati[0]] + (" " + sez if sez else "")

    pezzi = re.split(r"(^[ \t]*```.*?^[ \t]*```[^\n]*$)", md, flags=re.S | re.M)
    for k in range(0, len(pezzi), 2):
        pezzi[k] = _NOME_DI_FILE.sub(sostituisci, pezzi[k])
    return "".join(pezzi)


def leggi_per_la_stampa(f: "Path", capitoli: "dict[Path, str]") -> str:
    """Il sorgente di un capitolo con i rimandi già tradotti per questo volume."""
    return traduci_rimandi(f.read_text(encoding="utf-8"), f, capitoli)


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
        etichetta = capitoli.get(dove) or titolo(dove)
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
        etichetta = capitoli.get(dove) or (None if m.group("n1") else titolo(dove))
        if etichetta:
            return etichetta + (" " + sez if sez else "")
        return m.group(0)

    pezzi = re.split(r"(^[ \t]*```.*?^[ \t]*```[^\n]*$)", md, flags=re.S | re.M)
    for k, pezzo in enumerate(pezzi):
        if k % 2 == 0:
            pezzi[k] = _RIF_NUDO.sub(nudo, _RIF_PARENTESI.sub(in_parentesi, pezzo))
    return "".join(pezzi)
