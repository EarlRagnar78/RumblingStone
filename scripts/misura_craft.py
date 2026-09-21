#!/usr/bin/env python3
r"""misura_craft.py — quanti congegni di mestiere porta un documento, e quali no.

## Perché non misura «la percentuale dei nove pilastri»

🔴 **Sarebbe la metrica sbagliata, e premierebbe il difetto.** La skill dello
stile dichiara una *fusion rule*: «never all nine at once. Every scene has ONE
lead pillar and at most two support». Un documento che portasse tutti e nove i
pilastri in ogni scena **violerebbe** lo standard, non lo supererebbe. Contare
la copertura misurerebbe quanto un testo sbaglia.

E c'è un precedente misurato nel repo: `PIANO-PROSA-CHE-NON-SEMBRI-GENERATA`
provò i tropi esterni sul contenuto di gioco e trovò **64 falsi positivi su
64**. Lo stile come *tessitura* non si misura a macchina, e fingere di sì
produce numeri che sembrano informativi e non lo sono.

## Cosa misura invece

I **congegni di mestiere**: quei dispositivi che le skill e gli ADR dichiarano
per iscritto, che si contano perché **lasciano una traccia nel documento**, e
che un DM userebbe al tavolo. Non «quanto è bello», ma «quali strumenti ci
sono e quali mancano».

⚠️ **Ogni conteggio è un indizio, non un verdetto.** Un documento può fare una
cosa bene senza la marca che questo script cerca, e portarne la marca senza
farla bene. Il numero serve a **dire dove guardare**, e la riga «confronto» lo
dice meglio del valore assoluto — è ADR-0036, *misurare il miglioramento e non
lo stato*: un documento si giudica contro un banco scelto, non contro un ideale.

## I banchi

Il DM ne ha nominati due, e sono i due documenti che il repo ha scritto meglio:
il **Palio di Channathgate** (già benchmark dichiarato in `ARC07-DEF-4`) e
**L'Abbazia della Rotta Sicura**, l'avventura stand-alone.

## 🔴 Cinque rilevatori sbagliati, trovati alla prima esecuzione

Il primo giro ha prodotto una tabella **che invertiva la verità**, e la prova
che la produceva era la tabella stessa: nessuno l'aveva verificata contro il
testo. Il difetto è quello di ADR-0053 — *un matcher largo traveste
l'ignoranza*. Le correzioni, ognuna con la misura che l'ha imposta:

| Rilevatore | Cosa sbagliava | Prova |
|---|---|---|
| **read-aloud** | `^>` prendeva **qualsiasi** citazione, comprese le note editoriali. DEF-1 segnava **183** e sono `> **Sistema: D&D 3.5 SRD**`, `> **Sostituisce e fonde**`; l'Abbazia ne segnava 11 e sono **tutti** prosa in corsivo. Il numero diceva il contrario del vero | stretto (`> *`) → DEF-1 **24**, Abbazia **11 invariati** |
| **spotlight per PG** | pretendeva il **grassetto**. Il Palio nomina tutti e quattro i PG 13 volte, mai in grassetto → segnava 0. Misurava la formattazione, non il beat | tolto `\*\*` |
| **eco** | non conosceva il plurale «**Echi**» — e così il Palio, che ha un **file intero** chiamato `PALIO-CONSEGUENZE-ECHI.md`, segnava **zero echi** | `\bech[io]\b` |
| **voci PNG** | pretendeva `Nome: «…»`: **zero ovunque**, in 12 bersagli | conta le battute `«…»` comunque scritte |
| **grigio politico** | l'alternativa `\bWant\b` (dalla skill, in inglese) non matcha **niente** in tutto il repo | rimossa |

🔴 **E la diagnosi delle «voci PNG» era sbagliata a sua volta**, per lo stesso
motivo per cui lo erano i rilevatori: non avevo letto la fonte. Avevo concluso
«una forma inventata, che nessun documento usa». È il contrario —
`references/editorial-standards.md` §2 la **prescrive**:
`**NOME (registro/tono):** *«battuta»*`. Il fatto vero non è che la forma sia
inventata: è che **esiste sei volte in tutto il repo**.

## Gli standard redazionali scritti e mai messi sotto cancello

Il DM, il 2026-09-18: *«parti da quello che è definito davvero per la parte di
scrittura, stile e linea editoriale, e che c'è davvero nel repo skills»*.
Partendo da lì si trovano quattro congegni **dichiarati, numerici, e non
misurati da nessuno** — sono gli ultimi quattro dell'elenco qui sotto, più le
soglie di `--box`:

| Dove | Cosa prescrive | Chi lo controlla |
|---|---|---|
| `references/read-aloud-adulti.md` §2 | box **≤ 12 righe** (2-4 per un round), **un solo nome proprio nuovo**, niente parentesi | **nessuno** |
| `references/editorial-standards.md` §2 | `**Read-aloud (pilastro lead).**` · `**NOME (registro):** *«…»*` | **nessuno** |
| `ADR-0014` §1-2 | regia di round, chiusura su «Che fate?», occhio da avventuriero | **nessuno** |

⚠️ `validate_modules.py` sembra coprirli e non li copre: conta le occorrenze
della **parola** «read-aloud» e si ferma a cinque, quindi un master con cinque
menzioni e **zero box** passa. E gira **solo** su `ARC*-DEF-*.md`: ARC-08,
ARC-09, il Palio e l'Abbazia non sono mai stati guardati da nessun cancello.

⚠️ **Le virgolette dritte non sono dialogo, qui.** `"[^"]{12,}"` sembrava
l'altra convenzione: nel Palio dà **128 hit**, e sono **titoli di canzoni**
(«L'Aria dei Conti», «Il Lamento del Traghetto»). Un documento che scrivesse i
dialoghi con `"` verrebbe contato sotto: è il **limite dichiarato** di questa
misura, non un difetto nascosto.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: I quattro PG, per il conteggio dello spotlight.
PG = ("Thorik", "Tordek", "Hella", "Artemis")

#: Ogni congegno: (etichetta, regex, dove è dichiarato).
#: Il terzo campo non è decorazione: un congegno che nessun documento del repo
#: dichiara non è un criterio, è un gusto personale — e non entra qui.
CONGEGNI = [
    # 🔴 Contava SOLO i box che cominciano con prosa in corsivo nuda, e
    # saltava quelli scritti nella forma che `editorial-standards` §2
    # PRESCRIVE — `> **Read-aloud (pilastro lead).** *prosa*`. Cioe' i
    # migliori. DEF-4 segnava 5 read-aloud e ne ha **15**: cinque nudi e
    # **dieci etichettati**. Trovato il 2026-09-18 usando lo strumento per
    # riscrivere DEF-4, e ha reso false tre cifre gia' pubblicate.
    ("read-aloud narrativo",
     re.compile(r"^>\s*(?:\*\*Read-aloud[^*\n]*\*\*\s*)?[*_][^*_\s]", re.M | re.I),
     "module-standard §6 — prosa NUOVA per ogni ambiente"),

    ("contingenze «se i PG…»",
     re.compile(r"\bSe (?:i PG|il party|i giocatori|falliscono|il gruppo)\b", re.I),
     "module-standard §9 — e SEMPRE la riga sconfitta"),

    ("scalare lo scontro",
     re.compile(r"scalar\w+ lo scontro|party più (?:forte|debole)|PG abbattuto", re.I),
     "module-standard §8 — sidebar obbligatoria del boss"),

    ("spotlight per PG",
     re.compile(r"\b(?:" + "|".join(PG) + r")\b", re.I),
     "module-standard §5 — ogni PG ha un beat suo"),

    ("tattiche round-per-round",
     re.compile(r"\bRound\s*\d|round-per-round|Round 1[–-]2", re.I),
     "module-standard §7 — dal punto di vista del MOSTRO"),

    ("vie non combattive",
     re.compile(r"vi[ae] non combattiv|senza combattere|Diplomazia\s*C[DA]|"
                r"Intimidire\s*C[DA]|Raggirare\s*C[DA]", re.I),
     "module-standard §7 — sempre ≥2 (Premium Design)"),

    ("eco / conseguenze a distanza",
     re.compile(r"Echo Ledger|carry-over|\bech[io]\b|eco (?:di|del|della)|"
                r"conseguenz\w+ (?:lung|a distanza|durevol)|ritorna cambiat|"
                r"si ricorder|torner[àa] (?:a|nel|nella)", re.I),
     "pilastro 7 (BG3) — una scelta scrive un'eco che torna"),

    ("orologio / countdown",
     re.compile(r"\bOrologio\b|countdown|clock\b|\bgiro\s+\d+/\d+", re.I),
     "module-standard §3 — orologi attivi"),

    ("prove grezze di caratteristica",
     re.compile(r"\b(?:FOR|DES|COS|INT|SAG|CAR|Forza|Destrezza|Costituzione|"
                r"Intelligenza|Saggezza|Carisma)\b[*_\s]*(?:grezz|C[DA]\s*\d)", re.I),
     "skill indagine — le SEI PORTE, per i PG senza gradi"),

    ("nodo d'indizio",
     re.compile(r"\bindizi?o?\b|Fatto/Lettura/Nome|regola dei tre indizi", re.I),
     "skill indagine — Fatto / Lettura / Nome"),

    ("modi di fallimento dichiarati",
     re.compile(r"modi di fall|fallimento a metà|costo, non (?:stop|blocco)|"
                r"vicolo cieco", re.I),
     "Abbazia §«Modi di fallimento al tavolo»"),

    ("ADR interni al documento",
     re.compile(r"^\*{0,2}ADR-\d+\s*[—–-]\s*\S", re.M),
     "🔎 Abbazia — il PERCHÉ di ogni scelta, dentro l'avventura"),

    ("quarta colonna sensoriale",
     re.compile(r"quarta colonna|cosa NON dire|non lo dici mai|"
                r"appartiene a chi (?:tira|fa la domanda)", re.I),
     "ADR-0057 (era ADR-12 dell'Abbazia) — contro «l'atmosfera divora l'indagine»"),

    ("battute di dialogo",
     re.compile(r"«[^»]{4,}»|\"[^\"\n]*?\s\S+\s\S+[^\"\n]*?[.!?…,]\""),
     "pilastro 6 (Mercer) — ogni PNG ha una voce sua"),

    ("esiti etichettati",
     re.compile(r"^[>\s|*-]*\*{0,2}Esit[oi]\b|\btre finali\b|finali progettat|"
                r"esiti possibil|matrice (?:di|degli) esiti|tabella (?:degli )?esiti",
                re.I | re.M),
     "pilastro 8 (BG1–2) + Palio — la matrice delle conseguenze"),

    ("PILASTRO dichiarato (lead/support)",
     re.compile(r"\((?:Casa di Davide|Mercer|Andor|LotR|Tolkien|BG3|BG1|GoT|"
                r"Salvatore|Pillars|PoE)[^)\n]{0,24}(?:lead|support)\)", re.I),
     "fusion rule — UN pilastro guida, al più due di supporto"),

    # ── I quattro qui sotto non vengono dai pilastri: vengono dagli STANDARD
    # REDAZIONALI scritti e mai applicati. Vedi §«Il lavoro annegato» nel piano.
    ("regia etichettata **Read-aloud (X)**",
     re.compile(r"\*\*Read-aloud\s*\([^)\n]{2,30}\)"),
     "editorial-standards §2 — «così il prossimo agente sa quale voce continuare»"),

    ("dialogo nella forma dichiarata",
     re.compile(r"\*\*[A-ZÀ-Ù][^*\n]{1,40}\([^)\n]{2,30}\)\s*:?\*\*\s*\*?«"),
     "editorial-standards §2 — `**NOME (registro/tono):** *«battuta»*`"),

    ("chiusura su decision point",
     re.compile(r"«?\bChe fate\?|\bChe cosa fate\?|\bCosa fate\?", re.I),
     "ADR-0014 §2 — i box di combattimento chiudono su «Che fate?»"),

    # ⚠️ Il vocabolario e' quello che DEF-1 usa davvero — ADR-0014 lo nomina
    # esemplare — non quello dell'ADR, che descrive il congegno a parole sue.
    ("regia di round (una battuta per attore)",
     re.compile(r"regia dei .{0,12}round|giro del round|descrizioni da leggere|"
                r"apertura di round|chiusura di round|micro-box", re.I),
     "ADR-0014 §1 — nessuna sequenza a battute senza regia"),

    # ── Due congegni della skill dello stile che il metro non conosceva, e che
    # erano a ZERO in tutti e nove gli archi. Trovati il 2026-09-18 perche' il
    # DM ha chiesto «soluzioni creative» e la risposta era gia' scritta.
    ("[HDYWTDT] il finisher al giocatore",
     re.compile(r"\[HDYWTDT", re.I),
     "style-pillars §Mercer — «write [HDYWTDT] at boss-death points»"),

    ("assorbi e rilancia (yes-and with teeth)",
     re.compile(r"yes-and|assorbi,? poi rilancia|assorbi e rilancia|"
                r"invenzion\w+ del giocatore|un'idea che non è scritta", re.I),
     "style-pillars §Mercer — l'invenzione entra nel canone E genera una complicazione"),

    ("grigio politico",
     re.compile(r"fazione recuperabil|crede di aver ragione|ha (?:le sue|una sua) ragion|"
                r"\bLeva\b\s*[=:]|ricattabil|vizio\s*/\s*leva|non è (?:un )?(?:cattivo|mostro)\b|"
                # la self-check di narrative-style chiede testualmente un «Want
                # che non riguarda i PG»: se il metro non lo vede, la domanda 5
                # non ha uno strumento.
                r"\bWant\b[^.\n]{0,40}non riguarda",
                re.I),
     "pilastro 5 (GoT) — ogni fazione crede di aver ragione"),
]


def misura(testo: str) -> "dict[str, int]":
    return {nome: len(rx.findall(testo)) for nome, rx, _ in CONGEGNI}


#: Le soglie di `read-aloud-adulti.md` §2, scritte e mai messe sotto cancello.
#: ⚠️ `editorial-standards.md` §2 dice «3-10 righe», `read-aloud-adulti.md` §2
#: dice 8-12 per un'apertura di scena. Il tetto duro comune e' **12**, ed e'
#: quello che si misura: le due fonti non concordano sul minimo e questo
#: script non sceglie per loro.
TETTO_RIGHE = 12


def box_read_aloud(testo: str) -> "list[list[str]]":
    """I box read-aloud veri: citazioni in corsivo, spezzate alla riga vuota."""
    # ⚠️ Lo stesso `[*_][^*_\s]` del rilevatore: `> **Nota**` NON apre un box.
    # Scritto largo, questa funzione contava le note editoriali come read-aloud
    # e dava 51 box «con parentesi» su 67 in DEF-1 — erano note, non letture.
    # ⚠️ Stessa correzione del rilevatore gemello: un box **etichettato**
    # `> **Read-aloud (X).** *prosa*` — la forma PRESCRITTA — apre un box
    # come uno nudo. Senza, `--box` misurava DEF-4 su 2 box invece che 15.
    apre = re.compile(r"^>\s*(?:\*\*Read-aloud[^*\n]*\*\*\s*)?[*_][^*_\s]", re.I)
    box, corrente = [], []
    for riga in testo.splitlines():
        if apre.match(riga) or (corrente and riga.startswith(">")):
            corrente.append(riga)
        else:
            if corrente:
                box.append(corrente)
            corrente = []
    if corrente:
        box.append(corrente)
    return box


#: Un nome proprio: maiuscola interna alla frase, non a inizio riga o dopo punto.
#: L'etichetta di regia: rivolta al DM, non si legge ad alta voce.
_ETICHETTA = re.compile(r"\*\*Read-aloud[^*\n]*\*\*", re.I)

_NOME = re.compile(r"(?<![.!?»\n]\s)(?<!^)\b([A-ZÀ-Ù][a-zà-ù']{2,})")

#: 🔴 Nono difetto della stessa famiglia, trovato il 2026-09-19 misurando la
#: riscrittura di DEF-4. `_NOME` prova a escludere le maiuscole d'inizio frase
#: con due lookbehind, ma nel testo di un box **non ci arriva mai**: il
#: prefisso `> `, l'asterisco del corsivo e l'etichetta si frappongono fra il
#: punto e la maiuscola. Risultato: «Conoscete», «Quando», «Prima», «Dove»,
#: «Che», «Non», «Tra», «Notte» contati come nomi propri — e **nove box su
#: quattordici** di DEF-4 dichiarati fuori norma quando i veri erano **uno**.
#: Lo stesso numero l'avevo pubblicato per DEF-3 (13 su 16) e nel corpo della
#: PR #151. La cura non e' un elenco di eccezioni — sarebbe il metro tarato su
#: un campione, di nuovo — ma **normalizzare prima di cercare**: via i
#: marcatori, poi si guarda solo dentro le frasi, mai la loro prima parola.
_APERTURE = re.compile(r"^>\s*|[*_`]", re.M)
_FINE_FRASE = re.compile(r"(?<=[.!?…»])\s+")


def _registro_dei_nomi() -> "set[str]":
    """I nomi propri della campagna, **presi dai dati del repo**.

    🔴 **Perche' non una regex, e perche' non una lista scritta a mano.** Per
    tre giri ho provato a distinguere un nome proprio da una maiuscola di
    frase con la posizione: escludere la prima parola, poi recuperarla se il
    documento la usa anche a meta' frase. Ogni patch spostava l'errore —
    «Quei», «Nessun», «Silenzio» passavano perche' in italiano una maiuscola
    segue anche un trattino, i due punti e l'apertura di un dialogo.

    Una regex **non puo'** fare questa distinzione, e una lista che scrivo io
    sarebbe il metro tarato sul campione per la decima volta. Ma il repo un
    registro ce l'ha gia': i nomi dei file del **Bestiario** e la prima colonna
    delle tabelle di **`state.md`** — attori, artefatti, luoghi. Si legge da li'.

    ⚠️ **Tre limiti, dichiarati.**

    1. Un nome che non sta ne' nel Bestiario ne' in `state.md` non si vede. E'
       il prezzo giusto: quel nome, al tavolo, non e' ancora canone.
    2. Un nome di **piu' parole** si conta a pezzi — «Mano Rossa» e «Cuore
       della Leggenda» valgono due. Il conteggio e' quindi **prudente al
       rialzo**: segnala piu' di quanto serva, mai meno.
    3. 🔴 **Il piu' importante.** La norma di `read-aloud-adulti.md` §1 dice
       «un solo nome proprio **NUOVO** per box», e *nuovo* dipende da cosa il
       tavolo ha gia' incontrato, cioe' dall'ordine di lettura. Questo metro
       conta i nomi **distinti**, non i nuovi: e' un **indizio**, non il
       verdetto. Un box con tre nomi tutti noti da sei sessioni non viola
       niente, e il giudizio resta di chi scrive.
    """
    nomi: "set[str]" = set()
    bestiario = ROOT / "Bestiario"
    if bestiario.exists():
        for f in bestiario.rglob("*"):
            for parte in re.split(r"[/_\-. ]", f.stem):
                if _PAROLA_MAIUSCOLA.fullmatch(parte):
                    nomi.add(parte)
    stato = ROOT / "campaign" / "state.md"
    if stato.exists():
        for riga in stato.read_text(encoding="utf-8").splitlines():
            if not riga.startswith("|"):
                continue
            prima = riga.strip("|").split("|")[0].strip().strip("*[]`")
            for parte in prima.split():
                if _PAROLA_MAIUSCOLA.fullmatch(parte):
                    nomi.add(parte)
    return nomi


_PAROLA_MAIUSCOLA = re.compile(r"[A-ZÀ-Ù][a-zà-ù']{2,}")
_REGISTRO: "set[str] | None" = None


def nomi_propri(corpo: str) -> "set[str]":
    """I nomi propri di un box: le parole che stanno nel registro del repo."""
    global _REGISTRO
    if _REGISTRO is None:
        _REGISTRO = _registro_dei_nomi()
    piano = _APERTURE.sub("", _ETICHETTA.sub("", corpo))
    return {w.strip("«»\"'()[],;:.!?—-") for w in piano.split()
            if w.strip("«»\"'()[],;:.!?—-") in _REGISTRO}


def difetti_dei_box(testo: str) -> "dict[str, int]":
    """Quante volte i box violano le soglie dichiarate.

    🔴 Nessuna di queste e' controllata da `validate_modules.py`, che conta
    le **occorrenze della parola** «read-aloud» e si ferma a cinque.
    """
    lunghi = parentesi = nomi = 0
    for b in box_read_aloud(testo):
        if len(b) > TETTO_RIGHE:
            lunghi += 1
        # 🔴 Si misura il CORPO, non l'etichetta. `**Read-aloud (LotR lead).**`
        # e' rivolta al DM e non si legge ad alta voce: contarne le parentesi
        # e i nomi dei pilastri faceva risultare *peggiore* ogni box scritto
        # nella forma prescritta. Terza volta che lo stesso difetto — un metro
        # tarato su una forma sola — compare in questo file.
        corpo = _ETICHETTA.sub("", " ".join(b))
        if "(" in corpo:
            parentesi += 1
        if len(nomi_propri(corpo)) > 1:
            nomi += 1
    return {"box": len(box_read_aloud(testo)), "oltre 12 righe": lunghi,
            "con parentesi": parentesi, ">1 nome proprio": nomi}


# ─────────────────────────────────────────────────────────────────────────
# P1 — il read-aloud che presuppone un'azione o un senso del giocatore
#
# La norma viene dalle linee guida di *Dungeon* (Paizo) e dice due cose:
# il box **non fa riferimento a chi guarda**, e si evita **qualunque frase che
# presupponga un'azione del giocatore**. La ragione non e' di gusto: il box che
# dice «entri e senti paura» decide al posto del giocatore due cose che sono
# sue — che sia entrato, e cosa prova.
#
# 🔴 **Il numero pubblicato il 2026-09-19 era falso, e in modo istruttivo.**
# Diceva «229 box su 1.334». Quel conteggio usava un criterio di «box» scritto
# per la ricerca invece di riusare `box_read_aloud`, che sta in questo file da
# settembre. Rimisurato con il rilevatore vero: **104 box su 540**, cioe' il
# denominatore era **piu' del doppio**. Quattordicesimo caso della famiglia
# «un criterio largo si inventa copertura», e la cura e' sempre la stessa:
# riusare il dato invece di riscriverlo. Per questo P1 vive **qui**, accanto a
# `box_read_aloud`, e non in uno script suo.
#
# ⚠️ **Due esclusioni, e una sola e' un'esenzione.**
#
#   * I **file che non sono prosa da tavolo** (prompt d'immagine, archivi
#     dichiarati con `_SNAPSHOT-STORICO.md`, `DEPRECATO`) non si misurano: non
#     e' clemenza, e' che la norma non parla di loro.
#   * Il **dialogo** e la **visione interiore** — un PNG o un artefatto che
#     parla al suo portatore — usano la seconda persona a ragione. La norma
#     riguarda la **narrazione**, non le battute, e questo rilevatore **non sa
#     distinguerle**: il giudizio resta di chi corregge, e il numero e' un
#     indizio.
#
# 🔎 **Un verbo e' uscito dall'elenco, misurando**: `avanz*`. L'unico rilievo
# che produceva era *«Nonna Grasa conta le candele avanzate»* — participio, non
# seconda persona.
_P1_VEDERE = (r"ved(?:i|ete|rai|rete)|noti|notate|scorgi|scorgete|osservi|osservate|"
              r"senti|sentite|odi|udite|percepisci|percepite|ti accorgi|vi accorgete")
_P1_AGIRE = (r"entr(?:i|ate)|arriv(?:i|ate)|ti avvicini|vi avvicinate|apri|aprite|"
             r"vari?chi|varcate|scendi|scendete|sali|salite|attraversi|attraversate|"
             r"ti volti|vi voltate|guardi|guardate|tocchi|toccate|prendi|prendete|"
             r"cammini|camminate")
P1 = re.compile(r"\b(" + _P1_VEDERE + r"|" + _P1_AGIRE + r")\b", re.I)

#: Le cartelle che non portano prosa da leggere al tavolo. `Immagini/` contiene
#: i master di prompt (ADR-0015): sono citazioni in corsivo, non read-aloud.
ESCLUSI_P1 = ("Immagini",)


def cartelle_snapshot() -> "set[Path]":
    """Le cartelle che si dichiarano archivio con un file, non con un nome."""
    return {p.parent for p in ROOT.rglob("_SNAPSHOT-STORICO.md")}


def file_di_gioco_p1() -> "list[Path]":
    """Il contenuto di gioco vivo, con le esclusioni che il repo gia' dichiara."""
    snapshot = cartelle_snapshot()
    fuori = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in (
                "plans", "docs", "skills", "scripts", "converters", "campaign"):
            continue
        for f in d.rglob("*.md"):
            if any(x in f.parts for x in ESCLUSI + ESCLUSI_P1):
                continue
            if any(x in f.name for x in ESCLUSI_NOME) or f.name.endswith(".hb.md"):
                continue
            if any(s in f.parents for s in snapshot):
                continue
            fuori.append(f)
    return fuori


def box_con_p1(testo: str) -> "list[tuple[str, str]]":
    """I box che violano P1: (verbo trovato, prime parole del box)."""
    fuori = []
    for b in box_read_aloud(testo):
        corpo = _ETICHETTA.sub("", " ".join(b))
        m = P1.search(corpo)
        if m:
            fuori.append((m.group(1), corpo.strip()[:100]))
    return fuori


#: Fuori misura, con la ragione scritta: una versione superata o una errata
#: corrige non dice niente sul mestiere del documento vivo.
ESCLUSI = ("_ARCHIVIO", "homebrew", "build")
ESCLUSI_NOME = ("DEPRECATO", "ERRATA-")


def espandi(modelli: "list[str]") -> "list[Path]":
    """Espande i modelli glob di un bersaglio in file veri, **rumorosamente**.

    🔴 Un modello che non pesca niente alza un'eccezione. Il primo giro di
    questo script misurava **6 file del Palio su 15** e **1 di ARC-08 su 23**,
    e la tabella non lo diceva: gli zeri sembravano assenze di mestiere ed
    erano assenze di misura. E' lo stesso difetto del censimento tarato sul
    campione — qui non puo' piu' restare muto.
    """
    fuori: "list[Path]" = []
    for m in modelli:
        trovati = sorted(ROOT.glob(m))
        if not trovati:
            raise SystemExit(f"modello che non pesca niente: {m!r}")
        fuori.extend(trovati)
    tenuti, visti = [], set()
    for f in fuori:
        if f in visti or not f.is_file():
            continue
        if any(x in f.parts for x in ESCLUSI) or any(x in f.name for x in ESCLUSI_NOME):
            continue
        visti.add(f)
        tenuti.append(f)
    return tenuti


def carica(modelli: "list[str]") -> "tuple[str, int, int]":
    """Concatena i file di un bersaglio e restituisce (testo, righe, n_file)."""
    files = espandi(modelli)
    testo = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in files)
    return testo, max(1, testo.count("\n")), len(files)


#: I bersagli: i banchi del DM, poi i master da confrontare.
A9 = "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
A7 = "07_il Portale Della Forgia Eterna"

A8 = "08_La Battaglia Di Hammerfist"

BERSAGLI = {
    "★ Abbazia (stand-alone)": ["10-stand-alone/L'abbazia Della Rotta Sicura/*.md"],
    "★ Palio di Channathgate": [f"{A9}/Arco-Post-Hammerfist-P2D-PALIO-*.md"],
    "DEF-1 Piano della Terra": [f"{A7}/ARC07-DEF-1-PIANO-TERRA-TERROS.md"],
    "DEF-2 Ritorno e affreschi": [f"{A7}/ARC07-DEF-2-RITORNO-E-AFFRESCHI.md"],
    "DEF-3 Resurrezione Hella": [f"{A7}/ARC07-DEF-3-RESURREZIONE-HELLA.md"],
    "DEF-4 Viaggio 1.000 anni": [f"{A7}/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"],
    "DEF-5 Ritorno Hammerfist": [f"{A7}/ARC07-DEF-5-RITORNO-HAMMERFIST.md"],
    "ARC-09 Torre di Zalkatar": [f"{A9}/Arco-Post-Hammerfist-P2A-Torre-*.md"],
    "ARC-09 Torneo di Dauth": [f"{A9}/Arco-Post-Hammerfist-P2B-Torneo-*.md"],
    "ARC-09 Rhest": [f"{A9}/Arco-Post-Hammerfist-P2-RHEST-*.md"],
    "ARC-09 Battaglia Finale": [f"{A9}/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-*.md"],
    "ARC-08 Hammerfist": [f"{A8}/ARC08-*.md", f"{A8}/Cerimonia-delle-100-Asce.md"],
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--densita", action="store_true",
                    help="normalizza ogni conteggio su 1.000 righe (confronto fra documenti di taglia diversa)")
    ap.add_argument("--spotlight", action="store_true",
                    help="equilibrio dei quattro PG contro la norma «no PC oltre il 40%%» di pc-protagonism.md")
    ap.add_argument("--box", action="store_true",
                    help="i box read-aloud contro le soglie di read-aloud-adulti.md")
    ap.add_argument("--copertura", action="store_true",
                    help="quanti congegni su N, e quali hanno i banchi che qui mancano")
    ap.add_argument("--mancanti", action="store_true",
                    help="elenca, per ogni bersaglio, i congegni a ZERO")
    ap.add_argument("--p1", action="store_true",
                    help="i read-aloud che presuppongono un'azione o un senso "
                         "del giocatore (norma Dungeon/Paizo), file per file")
    args = ap.parse_args()

    if args.p1:
        files = file_di_gioco_p1()
        per_file, tot_box, tot_p1 = {}, 0, 0
        for f in files:
            testo = f.read_text(encoding="utf-8", errors="replace")
            tot_box += len(box_read_aloud(testo))
            colpiti = box_con_p1(testo)
            if colpiti:
                per_file[f.relative_to(ROOT)] = colpiti
                tot_p1 += len(colpiti)
        pct = (100 * tot_p1 / tot_box) if tot_box else 0
        print(f"\nP1 — read-aloud che presuppongono un'azione del giocatore")
        print(f"    norma: linee guida *Dungeon* (Paizo) · rilevatore: box_read_aloud\n")
        print(f"    {tot_p1} box su {tot_box} = {pct:.0f}%   in {len(per_file)} file "
              f"su {len(files)} misurati\n")
        for rel, colpiti in sorted(per_file.items(), key=lambda kv: -len(kv[1])):
            print(f"  {len(colpiti):3}  {rel}")
            for verbo, inizio in colpiti[:3]:
                print(f"       [{verbo}] {inizio}")
        print("\n⚠️  Il dialogo e la visione interiore usano la seconda persona a")
        print("    ragione: la norma riguarda la narrazione. Questo conteggio e' un")
        print("    indizio, e il giudizio resta di chi corregge.\n")
        return 0

    dati, righe, nfile = {}, {}, {}
    for nome, modelli in BERSAGLI.items():
        testo, n, k = carica(modelli)
        if not testo.strip():
            continue
        dati[nome] = misura(testo)
        righe[nome] = n
        nfile[nome] = k

    etichette = [c[0] for c in CONGEGNI]
    largh = max(len(n) for n in dati) + 1

    print(f"\n{'':{largh}} file  righe | " + " | ".join(f"{e[:11]:>11}" for e in etichette))
    for nome, conta in dati.items():
        cella = []
        for e in etichette:
            v = conta[e]
            if args.densita:
                cella.append(f"{v * 1000 / righe[nome]:>11.1f}")
            else:
                cella.append(f"{v:>11d}")
        print(f"{nome:{largh}}{nfile[nome]:>4} {righe[nome]:>6} | " + " | ".join(cella))

    if args.spotlight:
        print("\n\nEQUILIBRIO DELLO SPOTLIGHT (`pc-protagonism.md`: «no PC >40%»)\n")
        print("⚠️  **Indicatore, non la norma.** La norma conta le *scene marcate*;")
        print("    qui si contano le menzioni del nome, che e' cio' che si puo'")
        print("    misurare senza una marcatura che il repo non ha. Uno squilibrio")
        print("    puo' essere voluto (il Torneo *di Tordek*), un PG a ZERO no.\n")
        print(f"{'bersaglio':30}" + "".join(f"{p:>9}" for p in PG) + f"{'max':>7}  norma")
        for nome, modelli in BERSAGLI.items():
            testo, _, _ = carica(modelli)
            c = {p: len(re.findall(rf"\b{p}\b", testo, re.I)) for p in PG}
            tot = sum(c.values())
            if tot < 8:
                continue
            top = 100 * max(c.values()) / tot
            assenti = [p for p, v in c.items() if v == 0]
            nota = "🔴 " + ", ".join(assenti) + " MAI nominati" if assenti else (
                   "🟡 sbilanciato" if top > 40 else "✓")
            print(f"{nome:30}" + "".join(f"{c[p]:>9}" for p in PG)
                  + f"{top:>6.0f}%  {nota}")
        print()

    if args.box:
        print("\n\nI BOX READ-ALOUD CONTRO LE SOGLIE DICHIARATE "
              "(`read-aloud-adulti.md` §2)\n")
        print("🔴 Nessuna di queste soglie e' sotto cancello: `validate_modules`")
        print("   conta le occorrenze della PAROLA «read-aloud» e si ferma a 5.\n")
        print(f"{'bersaglio':30} {'box':>5} {'>12 righe':>10} "
              f"{'parentesi':>10} {'>1 nome':>8}")
        for nome, modelli in BERSAGLI.items():
            testo, _, _ = carica(modelli)
            d = difetti_dei_box(testo)
            print(f"{nome:30} {d['box']:>5} {d['oltre 12 righe']:>10} "
                  f"{d['con parentesi']:>10} {d['>1 nome proprio']:>8}")
        print()

    if args.copertura:
        banchi = [n for n in dati if n.startswith("★")]
        hanno_i_banchi = {e for e in etichette
                          if any(dati[b][e] for b in banchi)}
        print("\n\nCOPERTURA — quanti congegni su "
              f"{len(etichette)}, e cosa manca RISPETTO AI BANCHI\n")
        print("⚠️  La percentuale NON e' un voto: un documento puo' legittimamente")
        print("    non avere orologi. La colonna che conta e' l'ultima.\n")
        for nome, conta in dati.items():
            presenti = {e for e in etichette if conta[e]}
            debito = sorted(hanno_i_banchi - presenti)
            marca = "★ " if nome.startswith("★") else "  "
            print(f"{marca}{nome:28} {len(presenti):2d}/{len(etichette)} "
                  f"({100 * len(presenti) / len(etichette):4.0f}%)   "
                  f"debito verso i banchi: {len(debito)}")
            for e in debito:
                print(f"       ✗ {e}")
            print()

    if args.mancanti:
        print("\n\nCONGEGNI ASSENTI (conteggio zero) — dove guardare\n")
        for nome, conta in dati.items():
            zero = [e for e in etichette if conta[e] == 0]
            if zero:
                print(f"  {nome}")
                for e in zero:
                    dove = next(c[2] for c in CONGEGNI if c[0] == e)
                    print(f"      ✗ {e:32s} {dove}")
                print()
    print("\n⚠️  Ogni conteggio e' un indizio, non un verdetto: dice dove guardare.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
