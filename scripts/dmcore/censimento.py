"""censimento — quali documenti d'arco portano statistiche, e quali contano.

🔴 **Perché questo modulo esiste.** Il 2026-09-17 il lotto 4d-5 ha aggiunto un
cancello che cercava i documenti d'arco con statblocchi in prosa. Cercava
**una forma sola** — quella dell'arco 09, con il trattino:

    - Taglia/Tipo: …
    - CA: 22

Il repo ne usa **tre**. L'arco 08 e l'arco 07 scrivono `**CA:** 22` senza
trattino; il Palio scrive `**CA** 18` senza nemmeno i due punti. Rimisurando
con tutte e tre, i documenti d'arco con statistiche passano da **23 a 38**, e
fra i quindici che il cancello non vedeva c'è un'avventura intera
(`10-stand-alone/L'Abbazia della Rotta Sicura`, 1.419 righe con il proprio
appendice di statblocchi) e la guida del DM dell'arco 08.

⚠️ **La lezione non è «il regex era stretto».** Era che il cancello è nato
tarato su un campione — i file che avevo sotto gli occhi quel giorno — e
dichiarava una copertura che non aveva. Un cancello che guarda una forma su
tre non è un cancello debole: è un cancello che **misura male e lo dice con
sicurezza**, cioè la stessa forma d'errore di ADR-0053.

## La seconda metà: `_ARCHIVIO` non è sinonimo di «copia»

`test_archivi_non_indicizzati.py` stabilisce, e prova a rovescio, che **chi
indicizza deve saltare gli archivi**: archiviare dodici istantanee portò il
catalogo da 305 a 311 record con un doppione. Quella regola resta vera e
questo modulo non la tocca.

Ma il censimento non indicizza: **sorveglia**. E per chi sorveglia la regola
è l'opposta (è la decisione D1, che lasciò gli SVG dentro `_ARCHIVIO/` apposta
«così la cartella resta dentro il raggio di validate_maps»).

La prova che la distinzione serve davvero, e che era già scritta nel repo:
`ARC07-MATRICE-VERSIONI.md` **dichiara MASTER otto file che stanno dentro
`_ARCHIVIO/`** — il P4 narrativo è marcato *«MASTER narrativo (DM 2026-07-03)»*,
`Terros.md` è *«MASTER di combattimento — power-up VOLUTO»*. Di tutti i file
d'archivio con statblocchi, **cinque su cinque** sono master dichiarati:
nessuno è davvero superato. Saltarli in blocco toglieva dal raggio proprio i
documenti che il DM ha eletto.

Quindi: gli archivi **restano fuori dall'indicizzazione**, e i master
dichiarati **rientrano nella sorveglianza**. La differenza la decide un
documento del repo, non un'euristica — ADR-0041, contare quel che è dichiarato.
"""
from __future__ import annotations

import re
from pathlib import Path

#: Le marche meccaniche che distinguono uno statblocco dalla prosa.
_MARCA = r"(?:Taglia/Tipo|Taglia|DV|CA|PF|TS|BAB|GS|CR)"

#: Le **tre** forme in uso nel repo. La terza non ha nemmeno i due punti.
#: Cosa puo' seguire una marca inline. Deliberatamente **stretto**: un numero,
#: un modificatore, o il nome di un tiro salvezza — perche' `**TS** Temp +7
#: Rifl +6` non comincia con una cifra. Allargarlo a «una parola qualunque»
#: farebbe passare la prosa (`**CA** della porta`), e un matcher che riconosce
#: tutto non e' un cancello.
_SEGUE = r"(?:[0-9+]|Temp|Tempra|Rifl|Riflessi|Vol|Volont)"

STATBLOCCO = re.compile(
    # 1) riga con trattino o grassetto:  «- CA: 22»  ·  «**CA:** 22»  ·  «| CA |»
    r"(?:^[ \t]*(?:[-*>|]\s*)*\*{0,2}" + _MARCA + r"\*{0,2}\s*[:|])"
    # 2) inline, senza due punti:  «**CA** 18 (armatura leggera)»  ·  «**TS** Temp +7»
    r"|(?:\*\*" + _MARCA + r"\*\*\s+" + _SEGUE + r")",
    re.M | re.IGNORECASE,
)

#: Sotto questa soglia è una menzione di passaggio, non una creatura giocabile.
SOGLIA = 4

#: Dove la provenienza dei file d'arco 07 è dichiarata riga per riga.
MATRICE = "07_il Portale Della Forgia Eterna/ARC07-MATRICE-VERSIONI.md"

#: 🔴 `**MASTER` da solo NON basta: la tabella storica della matrice lo usa al
#: passato («era la versione viva *prima* del consolidamento»), e leggerlo al
#: presente ha eletto otto archivi come master vivi. Serve la marca esplicita.
_RIGA_MASTER_VIVO = re.compile(r"\*{0,2}MASTER VIVO\*{0,2}", re.IGNORECASE)
_CITAZIONE = re.compile(r"`([^`]+\.md)`")


def marche(testo: str) -> int:
    """Quante marche di statblocco porta il testo, in una qualunque delle tre forme."""
    return len(STATBLOCCO.findall(testo))


def master_archiviati(root: Path) -> "set[str]":
    """I file dentro `_ARCHIVIO/` che la matrice dichiara master **al presente**.

    🔴 **Oggi restituisce l'insieme vuoto, ed è il punto.** Questa funzione
    nacque il 2026-09-17 (ADR-0054) leggendo ``**MASTER`` ovunque nella
    matrice — e la matrice usa quella parola nella sua **tabella storica**,
    dove significa «era la versione viva *prima* del consolidamento». Il
    risultato: otto file d'archivio eletti master vivi, e otto voci del
    Bestiario che puntavano a **generazioni superate** invece che al master
    DEF che si apre al tavolo.

    Misurando il 2026-09-18 si è visto che **nessuna delle otto creature
    esisteva solo lì**: Skullcrusher, Zog'tar, Durin e Re Thorek I hanno lo
    statblocco in `ARC07-DEF-4`, Terros e lo Xorn in `ARC07-DEF-1`, l'
    «Elementale della Terra Anziano GS 13» *era Terros* prima della
    ricalibrazione, e Thorgrim non ha numeri da nessuna parte. Le voci sono
    state ripuntate ai master vivi e la matrice adesso scrive *(fino al
    consolidamento)* **nella cella**, non solo nella legenda.

    ⚠️ **Non si cancella, si svuota.** La regola resta vera — se un giorno la
    matrice dichiarasse un master *vivo* dentro `_ARCHIVIO/`, il censimento
    deve raggiungerlo — ma adesso pretende la marca esplicita
    ``MASTER VIVO``, che nessuna riga porta. Una funzione che torna vuota e
    dice perché è più onesta di una che non c'è: `test_censimento_forme.py`
    prova entrambi i lati.
    """
    matrice = root / MATRICE
    if not matrice.exists():
        return set()
    base = matrice.parent.relative_to(root)
    fuori = set()
    for riga in matrice.read_text(encoding="utf-8", errors="replace").splitlines():
        if not _RIGA_MASTER_VIVO.search(riga):
            continue
        for citato in _CITAZIONE.findall(riga):
            if "_ARCHIVIO" not in citato:
                continue
            # la matrice cita relativamente alla cartella dell'arco
            candidato = base / citato
            if (root / candidato).exists():
                fuori.add(str(candidato))
    return fuori


def _in_archivio(rel: str) -> bool:
    return "_ARCHIVIO" in Path(rel).parts or "Old" in Path(rel).parts


def documenti_con_statistiche(root: Path) -> "list[str]":
    """I documenti d'arco che il censimento deve poter raggiungere.

    Include i master dichiarati dentro `_ARCHIVIO/`; esclude le copie
    archiviate e i booklet generati (`homebrew/`, che sono artefatti: la
    sorgente è altrove e si corregge lì).
    """
    archi = sorted([p for p in root.glob("0*") if p.is_dir()]
                   + [p for p in root.glob("1*") if p.is_dir()])
    eletti = master_archiviati(root)
    fuori = []
    for base in archi:
        for p in sorted(base.rglob("*.md")):
            rel = str(p.relative_to(root))
            if "homebrew" in Path(rel).parts:
                continue
            if _in_archivio(rel) and rel not in eletti:
                continue
            if marche(p.read_text(encoding="utf-8", errors="replace")) >= SOGLIA:
                fuori.append(rel)
    return fuori
