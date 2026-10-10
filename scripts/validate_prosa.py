#!/usr/bin/env python3
"""validate_prosa.py — il traduttese e i tic dell'IA, misurati invece che ricordati.

Perché esiste, in tre date.

  * **2026-07-31** — i giocatori al tavolo: *«la prosa sembra tradotta
    dall'inglese»*. Nasce `references/italiano-nativo.md` (274 righe: §1 i dieci
    calchi, §9 i tic dell'IA).
  * **2026-08-01** — [ADR-0016] decide che l'italiano è la lingua sorgente e
    scrive la condizione: *«Banco di prova: i prossimi handout. Se i giocatori
    diranno ancora che sembra tradotto… questa ADR va riaperta»*.
  * **2026-09-02** — i giocatori lo dicono di nuovo, **echi compresi**.

Fra la prima data e la terza c'è un motore di stile da 2047 righe. Quindi il
problema non è che manchi la norma: è che **nessuno misura se il testo la
rispetta**, e una norma che nessuno misura è un'intenzione.

## Le due famiglie di rilievo, che sono problemi diversi

**I calchi** (§1) sono errori: *realizzare* per *to realize* è sbagliato in
italiano, punto. Qui si segnalano solo le forme con **firma inequivocabile** —
`realizzi CHE`, non ogni `realizzare`, perché *realizzare un progetto* è
italiano corretto e un validatore che lo segnala viene spento.

**I tic** (§9) non sono errori: sono **abitudini**. L'antitesi «non X: è Y»
funziona benissimo *una volta*; alla terza il tavolo sente il telaio. Non si
verificano con una regex ma con un **conteggio**, ed è esattamente la cosa che
un revisore umano non fa mai — perché dovrebbe contare — e che una macchina fa
gratis.

I tic si contano **solo nella prosa rivolta ai giocatori** (read-aloud, handout,
echi): in una tabella di CD o in una nota di regia le maiuscole e i trattini
sono legittimi, e contarli lì sarebbe rumore.

## I documenti del repo sono un caso diverso, e peggiore

`--documenti` misura guide, ADR, piani e skill invece del contenuto di gioco. È
un bersaglio diverso perché i tic sono diversi: in una guida non ci sono
read-aloud, e l'antitesi non è il problema principale. Il problema è il
**trattino lungo** e il **conteggio annunciato**.

Misurato sui 177 documenti del repo (32.566 righe), contando la sola prosa —
fuori tabelle, blocchi di codice, titoli e citazioni:

    trattino lungo          2.080 occorrenze · 92 ogni 1.000 righe di prosa
    conteggio annunciato      138 («tre cose», «per due ragioni»)
    antitesi «non X: è Y»      58

⚠️ **Le soglie sono tarate sulla distribuzione reale, non a occhio**: quando
sono state fissate, la mediana dei documenti stava a 82 trattini ogni 1.000
righe di prosa e il quartile alto a 118, e la soglia a 150 segnalava gli otto
file peggiori invece di tingere tutto di rosso: un rilievo che compare ovunque
è un rilievo che nessuno legge.

Dopo la ripulitura del lotto D (2026-09-03) i numeri sono altri: 1.145 trattini
in 157 documenti, densità globale 72/1000, **mediana 73**, quartile alto 108, e
la soglia non segnala più niente. La soglia **resta a 150** ed è voluto. Serve
da guardia contro la ricaduta, non da classifica: a quella densità un documento
nuovo è stato scritto con l'abitudine vecchia, e zero rilievi è il modo in cui
questo controllo dice che va bene.

## Cosa NON si misura, e perché

Provate e scartate, perché il rumore le rendeva inutili:

- **nomi ornati** (arazzo, panorama, ecosistema): 64 occorrenze, **64 falsi
  positivi**. `sinergia` è un termine di regole 3.5, `panorama` sta dentro il
  nome di un PNG, `ecosistema` è ecologia letterale in una prova di Natura.
- **rotazione dei sinonimi**: colpisce le descrizioni delle mappe (`stanza` e
  `camera` nella stessa griglia) e un'iscrizione runica.
- **gerundio d'analisi**: 135 occorrenze, e sono gerundi italiani normali —
  «irradiando un'aura», «innescando la Sfida». Il tic vero («sottolineando la
  sua importanza») nel repo compare **una volta**.
- **anafora**: 291 finestre, e i campioni sono un file di tattiche in inglese e
  un'etichetta `**Costo**` ripetuta in un elenco.
- **intestazioni con parola interrogativa**: è un tell dell'inglese. In italiano
  «Come si usa» è il titolo giusto per una sezione che spiega come si usa.

Restano prescrizioni nella skill `rumblingstone-prosa-documenti`, dove un occhio
umano decide. Un gate che grida al lupo viene spento, e con lui i controlli buoni.

Uso:
    python3 scripts/validate_prosa.py                 # tutto il contenuto
    python3 scripts/validate_prosa.py FILE…           # solo questi
    python3 scripts/validate_prosa.py --documenti     # guide, ADR, piani, skill
    python3 scripts/validate_prosa.py --strict        # i rilievi diventano errori
"""
from __future__ import annotations

import argparse
import re
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENUTO = ("00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_",
             "10-stand-alone", "STANDALONE-", "campaign", "PG")

PARTI_DEL_CORPO = (r"man[oi]|braccia?|test[ae]|occhi?|respiro|cuore|petto|schien[ae]|"
                   r"voce|sguardo|gamb[ae]|piedi?|dita|vis[oi]|volt[oi]|spall[ae]|labbra|ginocchia")

# §1 — i calchi, in DUE famiglie, perché non sono la stessa cosa.
#
# SEMPRE: forme che non hanno nessun uso italiano legittimo. «realizzi che» è
# sbagliato in una nota di regia come in un read-aloud.
CALCHI_SEMPRE: list[tuple[str, str]] = [
    (rf"\brealizz(?:o|i|a|iamo|ate|ano|ato|ata)\s+(?:subito\s+|che\b)",
     "«realizzi che» → capisci / ti rendi conto (realizzare = portare a compimento)"),
    (r"\bassum(?:o|i|e|iamo|ete|ono)\s+che\b",
     "«assumi che» → dai per scontato / immagini (to assume ≠ assumere)"),
    (r"\b(?:la\s+sensazione|un\s+senso|il\s+senso)\s+di\s+\w+",
     "nominalizzazione all'inglese: l'italiano verbalizza («cadi», non «la sensazione di cadere»)"),
    (r"\beventualmente\b",
     "«eventualmente» = casomai, NON eventually → «prima o poi», «alla fine»"),
]

# SOLO NEL READ-ALOUD: calchi che dipendono dal REGISTRO. «Sta piovendo» è
# italiano corretto, e «la sua mano» in terza persona può servire a disambiguare.
# Diventano un difetto nella prosa che si legge ad alta voce al tavolo, che è
# il caso di cui parla `italiano-nativo.md` §1 («stai camminando» → «cammini»).
# Segnalarli ovunque produrrebbe centinaia di rilievi corretti in teoria e
# inutili in pratica — misurato: 256 alla prima passata, per lo più questi.
CALCHI_READ_ALOUD: list[tuple[str, str]] = [
    (rf"\b(?:l[aeoi]|il|gli)\s+(?:su[aoei]|tu[aoei]|mi[aoei]|loro)\s+(?:{PARTI_DEL_CORPO})\b",
     "possessivo su una parte del corpo: in italiano è già implicito («alzò la mano»)"),
    (r"\b(?:sto|stai|sta|stiamo|stat[ei]|stanno)\s+\w+(?:ando|endo)\b",
     "progressivo all'inglese: nel read-aloud basta il presente («cammini nel buio»)"),
]

# §9 — i tic. Non regex ma CONTEGGI: la soglia è il rilievo.
# L'antitesi si riconosce dalla FORMA, non dal verbo: frase che apre con «non»,
# breve, spezzata da due punti o da un trattone. La seconda metà può essere una
# copula («c'è PESO»), un verbo («cataloga») o un sostantivo («niente») — tutti
# e tre gli esempi di `italiano-nativo.md` §9.1, e vanno presi tutti.
ANTITESI = re.compile(
    r"(?:^|[.!?»]\s+|\*\s*)Non\s+[^.;:!?\n]{2,50}?\s*[:—–]\s*\S", re.M)
MAIUSCOLE = re.compile(r"\b[A-ZÀÈÉÌÒÙ]{3,}\b")
# ⚠️ La lineetta enne fra due cifre senza spazi (`3–4 ore`, `GS 17–19`) è
# l'intervallo, e in italiano è la notazione GIUSTA: contarla come tic
# chiede di sbagliare la punteggiatura. Misurate: 79 delle 96 lineette enne
# dei documenti sono di questa forma. Il respiro è sempre la lineetta emme
# fra spazi, e resta contato — anche fra numeri («Chiuso 2026-09-03 — 157
# su 157»), motivo per cui l'esclusione chiede la enne E l'assenza di spazi.
TRATTINO = re.compile(r"—|(?<![0-9])–|–(?![0-9])")
# Sigle e acronimi del repo: maiuscoli per necessità, non per enfasi.
SIGLE = {
    "CD", "GS", "PG", "PGS", "DM", "PNG", "SRD", "OGL", "XP", "PX", "TS", "CA", "BAB",
    "EL", "RD", "RI", "TPK", "ADR", "CI", "PDF", "HTML", "SVG", "JSON", "VTT", "AP",
    "DR", "PF1E", "RHOD", "NPC", "HP", "DV", "MO", "PP", "MA", "CR", "UVTT", "YAML",
    "CSS", "URL", "API", "MIT", "GPL", "IP", "FR", "SW", "NE", "NO", "SE", "II", "III",
    "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "XX",
    # Le sei caratteristiche 3.5 in sigla maiuscola (`−4 DES / +2 COS`, come le
    # scrive `state.md`) e il prefisso degli archi (`ARC-08`). Trovate in L11
    # di PIANO-AGENT-SKILLS-ESTERNE: tre handout su tre che riportavano bene il
    # canone risultavano «con quattro maiuscole di enfasi», e quelli che lo
    # tacevano no. Un controllo che premia chi omette il canone si spegne.
    "FOR", "DES", "COS", "INT", "SAG", "CAR", "ARC",
}
SOGLIE = {"antitesi": 1, "maiuscole": 1}

# ── i documenti del repo ────────────────────────────────────────────────────
DOCUMENTI = ("docs/", "plans/", "skills/")
DOC_RADICE = ("README.md", "AGENTS.md", "CLAUDE.md", "LICENSES.md")

#: Il conteggio annunciato: «tre cose», «per due ragioni». Dire il numero prima
#: di elencare è il tic più frequente dei documenti di questo repo dopo il
#: trattino, e l'elenco che segue rende il numero superfluo.
CONTEGGIO = re.compile(
    r"\b(due|tre|quattro|cinque|sei|sette)\s+"
    r"(cose|ragioni|motivi|punti|modi|problemi|difetti|domande|vincoli|scelte)\b", re.I)

#: ⚠️ «due punti» non è un conteggio annunciato: è il nome italiano del segno
#: `:`, e in un repo che ha una norma sulla punteggiatura ricorre di continuo —
#: *«il segno giusto è due punti»*. Cercato in tutti i documenti: **ogni**
#: occorrenza è il segno o un valore di regole («Resist Freddo nei due punti»),
#: nessuna annuncia un elenco. Il tic vero non ha questa forma, perché nessuno
#: scrive «tre punti» per la punteggiatura. Si esclude la sola coppia.
CONTEGGIO_ESCLUSI = {("due", "punti")}

#: Un documento che **parla** del tic lo cita, e citarlo non è commetterlo. Il
#: caso non è teorico: questo piano, la sua skill e il changelog portano gli
#: esempi fra virgolette basse come prova, e senza questa esclusione il gate
#: segnalava proprio i file che scrivono la norma. Misurate: 6 occorrenze su 77
#: stanno dentro una citazione, e sono citazioni tutte e sei.
CITAZIONE = re.compile(r"«[^«»]{0,120}»|`[^`\n]{0,120}`")


def conteggi_annunciati(prosa: str) -> list[tuple[str, str]]:
    """Le occorrenze del conteggio annunciato, tolte quelle omografe e citate."""
    citazioni = [m.span() for m in CITAZIONE.finditer(prosa)]
    fuori = []
    for m in CONTEGGIO.finditer(prosa):
        coppia = (m.group(1).lower(), m.group(2).lower())
        if coppia in CONTEGGIO_ESCLUSI:
            continue
        if any(a <= m.start() and m.end() <= b for a, b in citazioni):
            continue
        fuori.append((m.group(1), m.group(2)))
    return fuori

#: Soglie per documento. Tarate sulla distribuzione misurata prima del lotto D
#: (mediana 82 trattini/1000 righe, quartile alto 118), quando 150 segnalava gli
#: otto file peggiori. Dopo la ripulitura la mediana è 73 e la soglia non trova
#: più niente: resta dov'è come guardia contro la ricaduta.
SOGLIE_DOC = {"trattino_per_mille": 150, "trattino_minimo": 10,
              "conteggio": 2, "antitesi": 2}

GLOSSARIO = ROOT / "campaign" / "GLOSSARIO-E-LOCALIZZAZIONE.md"


#: Dove finisce il canone e comincia il foglio di stile. Le tabelle prima di
#: questa riga dicono **cosa e' canone**; il §8 dice **quali grafie sono
#: escluse**, e le sue righe non sono nomi: se i due parser sotto le leggessero,
#: una forma esclusa diventerebbe un nome canonico.
FINE_CANONE = "## 8."


def _righe_canone() -> list[str]:
    if not GLOSSARIO.is_file():
        return []
    righe: list[str] = []
    for riga in GLOSSARIO.read_text(encoding="utf-8").splitlines():
        if riga.startswith(FINE_CANONE):
            break
        righe.append(riga)
    return righe


def coppie_glossario() -> list[tuple[str, str]]:
    """(canonico italiano, forma inglese) per le voci che vanno TRADOTTE.

    Le righe marcate `DNT` (do-not-translate) si saltano: *Aegis Fang* e
    *Skullcrusher* sono inglesi per scelta e restano tali. Si saltano anche le
    righe di intestazione di sezione (colonna 1 in grassetto) e i casi in cui la
    forma inglese compare già dentro il nome canonico (`Valle di Channath /
    Cannath Vale`): lì l'inglese è una delle due forme accettate, non un calco.
    """
    fuori: list[tuple[str, str]] = []
    for riga in _righe_canone():
        if not riga.strip().startswith("|"):
            continue
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if len(celle) < 3:
            continue
        it, en, nota = celle[0], celle[1], celle[2]
        if (it.startswith(("Italiano", "---", ":--", "**")) or "DNT" in nota
                or "invariat" in en.lower() or it == en or "·" in en or len(en) < 5
                or en.lower() in it.lower()):
            continue
        fuori.append((it, en))
    return fuori


PG = ("Thorik", "Tordek", "Hella", "Artemis", "Durik")

# Le forme brevi che il canone usa in prosa e che il glossario NON puo' dare,
# perche' li' i nomi stanno per esteso (o in inglese). Si estende a mano quando
# un artefatto prende un soprannome al tavolo: e' l'unico pezzo di questo file
# che sa qualcosa della campagna, ed e' voluto che si veda.
ALIAS = ("Anello", "Ascia", "Corona", "Bracieri", "Guanti", "Collana", "Cuore",
         "Sentinella", "Topazio", "Smeraldo", "Rubino", "Forgia", "Incudine")

# Parole che in un nome proprio non identificano niente da sole.
VUOTE = {"della", "delle", "degli", "dello", "dei", "del", "di", "da", "il", "la",
         "lo", "le", "gli", "of", "the", "and", "una", "uno", "in", "e"}


def nomi_canonici() -> list[str]:
    """Nomi del canone, **forme brevi comprese**.

    Un giocatore non scrive «Corona di Adamantio» in un eco: scrive «la Corona».
    Un controllo che pretende il nome per esteso da' il risultato rovesciato — e
    l'ha dato: segnalava l'hint di Artemis, che le ancore ha («l'Anello», «la
    Sentinella»), e lasciava passare quello di Hella, che non ne ha nessuna.
    Da qui: ogni voce del glossario contribuisce anche le sue **parole piene**.
    """
    fuori = set(PG) | set(ALIAS)
    for riga in _righe_canone():
        if not riga.strip().startswith("|"):
            continue
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if len(celle) < 2 or celle[0].startswith(("Italiano", "---", ":--", "**")):
            continue
        for pezzo in re.split(r"\s*[/·(«»]\s*", celle[0]):
            for parola in re.findall(r"[A-Za-zÀ-ÿ'’]{4,}", pezzo):
                if parola.lower() not in VUOTE:
                    fuori.add(parola)
    return sorted(fuori)


_NOMI: list[str] | None = None


def check_ancore(f: Path, righe: list[tuple[int, str]], rel) -> list[str]:
    """Un testo per i giocatori senza un solo nome che loro riconoscano.

    Il caso: gli echi di Hella prima dello scontro con Terros. La giocatrice ha
    detto di **non capirci niente**, e `validate_prosa` sul resto era pulito —
    non era prosa, era progetto. Contate le ancore nella prosa dei quattro testi
    per-PG della stessa sessione: Tordek 8, Thorik 5, Artemis 4, **Hella 0**.
    Riceve «una testa grande, ossuta» (e' Durik) e «spalle larghe, oneste» (e'
    Thorik) senza nominarli mai.

    Quattro immagini non attribuite di fila non sono mistero: sono rumore. Un
    frammento evocativo si regge se chi legge puo' attaccarne **uno** a qualcosa
    che conosce. `module-standard` §5 vuole che un PG assente percepisca «solo
    echi»: li vuole **oscuri**, non **senza appigli**.
    """
    # Il controllo vale dove il glossario E' il canone. I moduli autoconclusivi
    # hanno il loro (il Drappo e' a Tarsilia, su Golarion: Vesca e Salle non
    # stanno in GLOSSARIO-E-LOCALIZZAZIONE.md, e non devono starci). Segnalarli
    # vorrebbe dire chiedere loro di citare un canone che non e' il loro.
    if any(x.startswith(("STANDALONE-", "10-stand-alone")) for x in f.parts):
        return []
    if f.name.upper().startswith("README"):
        return []
    global _NOMI
    if _NOMI is None:
        _NOMI = nomi_canonici()
    prosa = "\n".join(r for _, r in righe if not r.lstrip().startswith("#"))
    prosa = CONGEDO_DM.sub(" ", CAPPELLO_DM.sub(" ", prosa))
    if len(prosa.split()) < 90:
        return []
    # ⚠ Confronto CASE-SENSITIVE, e non e' un dettaglio: meta' delle forme brevi
    # del canone sono anche nomi comuni italiani. «batteva il cuore» non e' il
    # Cuore di Moradin, «voci di cristallo» non e' un artefatto. La maiuscola e'
    # cio' che distingue un nome proprio da una parola — ed e' l'unico segnale
    # affidabile che il testo offre. Senza, il controllo dava Hella per ancorata.
    if any(re.search(rf"\b{re.escape(n)}\b", prosa) for n in _NOMI):
        return []
    return [f"{rel}: testo per i giocatori **senza una sola ancora nominata** — "
            f"niente che chi legge riconosca. Un frammento evocativo si regge su "
            f"almeno un nome noto: senza, non e' mistero, e' rumore"]


_COPPIE: list[tuple[str, str]] | None = None


def check_glossario(f: Path, testo: str, rel) -> list[str]:
    """La forma inglese di un nome che il glossario vuole tradotto.

    È il rilievo che il tavolo ha fatto per primo — «prosa inglese» — nella sua
    forma più letterale e più facile da correggere: *Anvil of the World* dove il
    canone dice *Incudine del Mondo*.
    """
    global _COPPIE
    if _COPPIE is None:
        _COPPIE = coppie_glossario()
    if "GLOSSARIO" in f.name:
        return []
    fuori = []
    for it, en in _COPPIE:
        m = re.search(rf"\b{re.escape(en)}\b", testo)
        if m:
            n = testo[: m.start()].count("\n") + 1
            fuori.append(f"{rel}:{n}: forma inglese «{en}» — il canone è «{it}» (glossario §)")
    return fuori


# La prosa rivolta ai giocatori, in DUE forme.
#
# 1. Il **read-aloud** dentro un file qualunque: blockquote in corsivo.
# 2. Il **file intero**, quando il file *è* per i giocatori — un hint, un teaser,
#    un handout, una lettera, un eco. Lì non c'è un blockquote che marca la
#    prosa: la prosa è tutta la pagina.
#
# ⚠ Senza il secondo caso il controllo copriva **l'8-13%** di un file come
# `02-HINT-THORIK.md` (misurato: 29 parole su 353 dentro `> *…*`), ed è il
# motivo per cui i file che il tavolo aveva segnalato tornavano puliti.
READ_ALOUD = re.compile(r"^>\s*\*[^*].*$", re.M)

PER_I_GIOCATORI = re.compile(
    r"HINT-|TEASER|ECHI-|GIOCATORI|HANDOUT|LETTERA|PROFEZIA|AVVISO|PROP|^pg-",
    re.I)
# Anche dentro un file per i giocatori, questi sono per il DM: non si contano.
# CONSEGUENZE: «ECHI-» nel nome vale per `05-ECHI-HELLA.md`, che si legge al
# giocatore, e non per `…DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md`, che è il
# registro degli esiti per il DM. Gli altri tre file «CONSEGUENZE» erano già
# fuori perché il loro nome non chiude «ECHI» con il trattino.
PER_IL_DM = re.compile(r"REGIA|GUIDA-DM|CASSETTA|DM-MASTER|STATBLOCCHI|CONSEGUENZE", re.I)

# Due cose che SEMBRANO enfasi e non lo sono, e che vanno tolte prima di contare.
#
# 1. L'etichetta di battuta: `**AEGIS FANG**, con quel tono…` — è il formato che
#    `editorial-standards.md` §2 IMPONE per i dialoghi (`**NOME (registro):**`).
#    Contarla come «maiuscola di portento» significa punire la convenzione del
#    repo, e un validatore che punisce la convenzione viene spento.
# 2. Il cappello per il giocatore: *«Per il giocatore di X. Leggi in privato…»* —
#    è un'istruzione del DM, non prosa di gioco.
# I due punti possono stare DENTRO il grassetto (`**I BRACIERI:**`) o fuori
# (`**AEGIS FANG**,`): il repo usa entrambe le forme, e sono la stessa cosa.
ETICHETTA_BATTUTA = re.compile(
    r"^>?\s*\*\*[A-ZÀ-Ù][A-ZÀ-Ù'’ \-]{1,30}[:：]?\*\*\s*[,(:]?", re.M)
# Il cappello sta su PIÙ righe di blockquote: si toglie il blocco intero, non la
# riga che contiene la frase-spia — altrimenti restano dentro le altre.
# Il congedo in coda — `> *(Niente meccanica, stanotte. …)*` — sta su piu' righe
# di blockquote: si toglie il BLOCCO, non la riga che apre la parentesi. Togliendo
# solo la prima restavano dentro le altre, e con loro i nomi che ci sono citati:
# un testo senza appigli risultava ancorato.
CONGEDO_DM = re.compile(r"(?:^>\s*\*?\(.*\n)(?:^>.*\n)*", re.M)
CAPPELLO_DM = re.compile(
    r"(?:^>.*\n)*?^>.*(?:per il giocatore|per la giocatrice|leggi in privato|non ci sono istruzioni"
    r"|affar tuo|ripasso lampo).*\n(?:^>.*\n)*",
    re.I | re.M)


# ─────────────────────────────────────────────────────────────────────────
# Il foglio di stile eseguibile — `GLOSSARIO-E-LOCALIZZAZIONE.md` §8
#
# 🔎 **Perche' esiste, dal 2026-10-03.** Il glossario dice «fissare **una volta
# sola** come si scrive ogni nome», e il solo controllo che lo applicava cercava
# le forme *inglesi* da tradurre. La **grafia** non la guardava nessuno, e il
# metro era cieco per costruzione: MQM verde su 521 documenti con *Regiarax* nel
# testo, *mithril* in ~25 righe e il PG Hella scritto *Hellas* in 21 file. E'
# la pratica del copyeditor (il foglio di stile) resa eseguibile, come fa Vale
# con le sue regole `substitution`; il codice e' di questo repo.
#
# Due stati. `refuso` e' una decisione presa: ogni occorrenza e' un rilievo.
# `DM?` e' una scelta che il DM non ha fatto: si conta, non si rimprovera.
STATI_FOGLIO = ("refuso", "DM?")


def forme_escluse() -> "list[tuple[str, str, str, str]]":
    """`(forma esclusa, forma canonica, stato, perche')` dal §8 del glossario."""
    if not GLOSSARIO.is_file():
        return []
    righe = GLOSSARIO.read_text(encoding="utf-8").splitlines()
    try:
        inizio = next(i for i, r in enumerate(righe) if r.startswith(FINE_CANONE))
    except StopIteration:
        return []
    voci = []
    for riga in righe[inizio:]:
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if (not riga.strip().startswith("|") or len(celle) < 4
                or not celle[0].startswith("`") or celle[2] not in STATI_FOGLIO):
            continue
        voci.append((celle[0].strip("`"), celle[1], celle[2], celle[3]))
    return voci


def _rx_forma(forma: str) -> "re.Pattern[str]":
    """Una forma tutta minuscola si cerca senza badare alla maiuscola (*Mithril*
    a inizio frase e' la stessa forma); un nome proprio, con la maiuscola."""
    flag = re.I if forma == forma.lower() else 0
    # Il confine non esclude la barra: *Hellas/druidi* e *Witchwood/Hellas* sono
    # prosa. Un percorso («porta/mithril/cartella») ha la barra da entrambi i
    # lati ed e' scartato in `occorrenze_forma`. ADR-0079.
    return re.compile(rf"(?<![\w`.-]){re.escape(forma)}(?![\w`-])", flag)


#: Una riga che cita un file per nome: il nome non si cambia insieme al testo,
#: perche' romperebbe il rimando. Il costo e' dichiarato: una grafia sbagliata in
#: prosa, sulla stessa riga di un percorso, passa.
_PERCORSO = re.compile(r"\.(?:md|webp|png|pdf|json|ya?ml|svg|txt|htm)\b", re.I)


def _freccia_accanto(riga: str, forma: str) -> bool:
    """La freccia che **lega** la forma esclusa a un'altra: «*mithril* →», «→ Hellas».
    Una freccia lontana («… se riesce → COMPLETE!») non spiega niente."""
    f = re.escape(forma)
    return bool(re.search(rf"{f}[\s*_\"«»'`]{{0,6}}→|→[\s*_\"«»'`]{{0,6}}{f}", riga,
                          re.I if forma == forma.lower() else 0))


def _spiega_il_cambio(riga: str, canonica: str, forma: str = "") -> bool:
    """La riga che **dice** il cambio («Regiarax» → «Regiarix») non e' un errore,
    e nemmeno quella che cita un nome di file (`_PERCORSO`)."""
    # ⚠️ Con il confine di parola, non con `in`: «hella» sta dentro «Hellas», e
    # il primo rapporto contava zero *Hellas* proprio per questo.
    # ⚠️ Una freccia lontana non spiega niente: «**Hellas:** Round 40 … → COMPLETE!»
    # la usava come scusa e la grafia sbagliata passava (ADR-0079). Conta la
    # freccia accanto alla forma, o la forma canonica sulla stessa riga.
    return (bool(_rx_forma(canonica).search(riga)) or bool(_PERCORSO.search(riga))
            or (bool(forma) and _freccia_accanto(riga, forma)))


def occorrenze_forma(testo: str, forma: str, canonica: str) -> "list[int]":
    """I numeri di riga in cui la forma esclusa compare davvero."""
    rx = _rx_forma(forma)

    def _fuori_da_un_percorso(riga: str) -> bool:
        return any(not (m.start() > 0 and riga[m.start() - 1] == "/"
                        and m.end() < len(riga) and riga[m.end()] == "/")
                   for m in rx.finditer(riga))

    return [n for n, riga in enumerate(testo.splitlines(), 1)
            if _fuori_da_un_percorso(riga) and not _spiega_il_cambio(riga, canonica, forma)]


_FOGLIO: "list[tuple[str, str, str, str]] | None" = None


def _e_archivio(f: Path) -> bool:
    """Un archivio e' storia: non si riscrive. Le esclusioni sono quelle del repo
    (`misura_craft.ESCLUSI`) e il marcatore `_SNAPSHOT-STORICO.md` delle cartelle,
    non un elenco nuovo. 🔴 Il marcatore mancava, e il primo giro ha riscritto
    uno snapshot: l'ha fermato `fase1.py --check`, dopo."""
    import misura_craft as mc

    return (any(x in f.parts for x in mc.ESCLUSI)
            or any(x in f.name for x in mc.ESCLUSI_NOME)
            or any((d / "_SNAPSHOT-STORICO.md").is_file() for d in f.parents))


def check_forme_escluse(f: Path, testo: str, rel) -> "list[str]":
    """Le grafie che il foglio di stile ha gia' deciso, e il file non rispetta."""
    global _FOGLIO
    if _FOGLIO is None:
        _FOGLIO = forme_escluse()
    if "GLOSSARIO" in f.name or _e_archivio(f):
        return []
    fuori = []
    for forma, canonica, stato, _ in _FOGLIO:
        if stato != "refuso":
            continue
        for n in occorrenze_forma(testo, forma, canonica):
            fuori.append(f"{rel}:{n}: grafia esclusa «{forma}» — il foglio di stile "
                         f"dice «{canonica}» (glossario §8)")
    return fuori


def conta_forme(bersagli: "list[Path]") -> "list[tuple[tuple[str, str, str, str], int, int, int, int]]":
    """Per ogni riga del foglio: occorrenze e file della forma esclusa, e della
    canonica. `(voce, occ. esclusa, file esclusa, occ. canonica, file canonica)`."""
    righe = []
    for voce in forme_escluse():
        forma, canonica, _, _ = voce
        occ = [0, 0]
        file_ = [0, 0]
        for f in bersagli:
            testo = f.read_text(encoding="utf-8", errors="ignore")
            n = len(occorrenze_forma(testo, forma, canonica))
            m = len(_rx_forma(canonica).findall(testo))
            occ[0] += n
            occ[1] += m
            file_[0] += bool(n)
            file_[1] += bool(m)
        righe.append((voce, occ[0], file_[0], occ[1], file_[1]))
    return righe


def rapporto_foglio(bersagli: "list[Path]") -> "tuple[list[str], int]":
    """Il foglio di stile contro il repo: `(righe stampabili, refusi aperti)`."""
    conti = conta_forme(bersagli)
    out = []
    refusi = 0
    for (forma, canonica, stato, _), n, nf, m, mf in conti:
        if stato == "refuso":
            refusi += n
            segno = "✗" if n else "✓"
        else:
            segno = "?"
        out.append(f"  {segno} {stato:6} «{forma}» {n:4} occ. in {nf:3} file"
                   f"   ·   «{canonica}» {m:4} occ. in {mf:3} file")
    return out, refusi


#: Le forme che hanno **un solo** uso legittimo e che il generatore di
#: proposte non deve rimproverare: due PNG diversi, due parole inglesi. Sono i
#: quattro falsi positivi contati a mano il 2026-10-03 su nove candidati.
OMONIMI_VOLUTI = frozenset({
    frozenset({"garruk", "karruk"}),      # il pugile del torneo e il Wyrmlord
    frozenset({"thorek", "thorik"}),      # il Re nanico e il PG
    frozenset({"headed", "healed"}),      # due parole inglesi
    frozenset({"hell's", "hellas"}),      # «hell's» e' inglese
    frozenset({"hella's", "hellas"}),     # il possessivo di Hella
})


def _a_distanza_uno(a: str, b: str) -> bool:
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(a == b[:i] + b[i + 1:] for i in range(len(b)))


def proponi_grafie(bersagli: "list[Path]") -> "list[tuple[str, int, str, int]]":
    """Coppie di nomi a **una sola lettera** di distanza, da portare al foglio.

    ⚠️ E' un generatore di **proposte**, non un rilevatore: decide un umano, e
    cio' che propone non e' un rilievo. Cinque filtri, ognuno nato da un falso
    positivo contato a mano il 2026-10-03:

    1. almeno **sei** lettere e almeno un nome del registro dei 322;
    2. nessuna parola italiana comune: se la forma compare **in minuscolo** in
       due punti del repo e' una parola, non un nome (*campagna/campana*,
       *portale/mortale*);
    3. niente flessioni: la differenza sull'ultima lettera e' genere o numero
       (*Cerchio/Cerchi*), non grafia;
    4. niente maiuscole di enfasi: *ABBATHOR* e' *Abbathor* gridato;
    5. niente omonimi voluti (`OMONIMI_VOLUTI`).

    ⚠️ **Limite noto, il filtro 3 ha un costo**: *Hella/Hellas* differisce
    sull'ultima lettera e **non esce**. Lo ha trovato il confronto di *Hellas*
    con *Hella's*, per caso. Una grafia che si distingue solo per l'ultima
    lettera la trova chi guarda il foglio, non questo generatore.
    """
    import misura_craft as mc

    registro = mc._registro_dei_nomi()
    cap: Counter = Counter()
    low: Counter = Counter()
    for f in bersagli:
        t = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8", errors="ignore"),
                   flags=re.S).replace("’", "'")
        for w in re.findall(r"[A-Za-zÀ-ù'\-]{4,}", t):
            w = w.strip("'-")
            (cap if w[:1].isupper() else low)[w] += 1
    nomi = [w for w in cap if len(w) >= 6 and not w.isupper() and low[w.lower()] < 2]
    out = []
    for i, a in enumerate(nomi):
        for b in nomi[i + 1:]:
            la, lb = a.lower(), b.lower()
            if not _a_distanza_uno(la, lb):
                continue
            if la[:-1] == lb[:-1] or la == lb[:-1] or lb == la[:-1]:
                continue
            if a not in registro and b not in registro:
                continue
            if frozenset({la, lb}) in OMONIMI_VOLUTI:
                continue
            out.append((a, cap[a], b, cap[b]))
    return sorted(out)


def e_per_i_giocatori(f: Path) -> bool:
    """Vero se il file, per intero, è testo che i giocatori leggono."""
    if PER_IL_DM.search(f.name):
        return False
    return bool(PER_I_GIOCATORI.search(f.name)
                or "handout" in str(f).lower()
                or "templates/homebrew" in str(f).replace("\\", "/").lower())
CODE_FENCE = re.compile(r"^\s*```")
INLINE = re.compile(r"`[^`]*`|https?://\S+|\[[^\]]*\]\([^)]*\)|[\w./-]+\.(?:md|py|json|svg|html|typ)")


def prosa_e_readaloud(testo: str) -> tuple[list[tuple[int, str]], str]:
    """(righe di prosa numerate, testo dei soli read-aloud).

    Le tabelle si saltano: una riga `| CD 22 | ... |` non è prosa, e i tic
    contati lì sarebbero rumore.
    """
    righe: list[tuple[int, str]] = []
    fence = False
    for n, riga in enumerate(testo.splitlines(), 1):
        if CODE_FENCE.match(riga):
            fence = not fence
            continue
        if fence or riga.lstrip().startswith("|") or riga.startswith(("    ", "\t")):
            continue
        righe.append((n, INLINE.sub(lambda m: "x" * len(m.group(0)), riga)))
    # 🔴 Fino al 2026-10-01 il read-aloud era `READ_ALOUD.findall`: la sola PRIMA
    # riga dei soli box NUDI. I box nella forma che `editorial-standards` §2
    # prescrive (`> **Read-aloud (X).** *…*`) e le righe di continuazione non
    # si leggevano: 32.765 parole su 55.680 (59%), misurato in L11 di
    # PIANO-AGENT-SKILLS-ESTERNE. Lo stesso difetto `misura_craft` l'aveva
    # corretto per se' a settembre; qui si riusa il suo rilevatore, una norma
    # un rilevatore. L'etichetta di regia resta fuori: e' rivolta al DM.
    from misura_craft import _ETICHETTA, box_read_aloud
    return righe, "\n".join(_ETICHETTA.sub("", "\n".join(b)) for b in box_read_aloud(testo))


# ===========================================================================
# Confrontare due versioni dello stesso testo (ADR-0036)
# ===========================================================================
# La cosa che mancava: una misura del **miglioramento**, non dello stato.
#
# Tutte le misure assolute provate su questo corpus hanno fallito, e il
# fallimento è istruttivo:
#
#   * la **burstiness** — varianza della lunghezza delle frasi, la misura più
#     citata nella letteratura sui rilevatori — sulla riscrittura che il DM ha
#     approvato **peggiora**: CV 0,55 → 0,47. La riscrittura aveva tolto i
#     frammenti brevi, e togliere frammenti riduce la varianza. La metrica
#     premia il tic che §9 vieta;
#   * la **densità di frasi corte** come soglia di repo: il file peggiore (75%)
#     è fatto di grida («PORTATORE MALEDETTO!») e note telegrafiche di regia
#     («Treant lo lancia»), non di frammenti narrativi;
#   * le **aperture ripetute**: tre occorrenze in tutto il corpus.
#
# Le stesse misure **dentro un solo testo, fra due versioni**, funzionano: grida
# e note di regia ci sono prima e dopo, quindi si annullano nella differenza.
# Resta quello che la riscrittura ha cambiato.

FRASE = re.compile(r"(?<=[.!?…])\s+")


def _frasi(testo: str) -> list[str]:
    return [f.strip() for f in FRASE.split((testo or "").strip())
            if len(f.split()) >= 2]


def burstiness(testo: str) -> float | None:
    """Il coefficiente di variazione della lunghezza delle frasi.

    ⚠️ **Misurabile, ma non un obiettivo.** Sta qui perché è la misura che
    l'analisi esterna proponeva e perché il confronto con la riscrittura
    approvata dal DM la contraddice: serve a poterlo rifare, non a puntarci.
    Fuori da `conta_tic()` di proposito.
    """
    lunghezze = [len(f.split()) for f in _frasi(testo)]
    if len(lunghezze) < 5:
        return None
    media = statistics.mean(lunghezze)
    return statistics.pstdev(lunghezze) / media if media else None


#: Quanti numeri del profilo si stampano prima di troncare. Un file di 215
#: frasi ne stamperebbe 215, e un profilo che non si legge non serve a niente.
PROFILO_MAX = 40


def profilo_lunghezze(testo: str) -> dict | None:
    """Le lunghezze delle frasi **in ordine di lettura**, con media e scarto.

    È quello che resta della burstiness dopo la verifica, ed è deliberatamente
    la sua forma **non compressa**. Il coefficiente di variazione schiaccia in un
    numero solo due cose opposte — il ritmo vero (periodi ampi chiusi da una
    frase secca) e il tic dell'IA (una raffica di stoccate da due parole) — e su
    questo corpus quel numero punta dalla parte sbagliata: vedi ADR-0036.

    La sequenza non schiaccia niente. Sull'eco di Hella si legge in due righe
    cosa ha fatto la riscrittura approvata::

        prima   14 24 14  3  6 12 22  8 26 …   media 17,1 · scarto  8,9
        dopo    14 24 14 19 12 28 23 21 23 …   media 21,4 · scarto 10,1

    Le frasi da 3, 6 e 8 parole sono sparite dentro periodi. Il CV scende (0,52
    → 0,47) perché la media sale più in fretta dello scarto, e direbbe
    «peggiorata» su una versione che il tavolo ha approvato.

    ⚠️ **Informazione, non punteggio.** Non entra in `conta_tic()` e non vota nel
    verdetto di `confronta()`; un test lo tiene fermo.
    """
    lunghezze = [len(f.split()) for f in _frasi(testo)]
    if not lunghezze:
        return None
    return {"lunghezze": lunghezze,
            "media": statistics.mean(lunghezze),
            "scarto": statistics.pstdev(lunghezze)}


def righe_profilo(etichetta: str, testo: str) -> list[str]:
    """Le due righe da stampare: la sequenza e, sotto, media e scarto."""
    p = profilo_lunghezze(testo)
    if p is None:
        return [f"    {etichetta:<9} (nessuna frase)"]
    mostrati = p["lunghezze"][:PROFILO_MAX]
    avanzo = len(p["lunghezze"]) - len(mostrati)
    coda = f"  …+{avanzo}" if avanzo else ""
    return [f"    {etichetta:<9} " + " ".join(f"{n:>3d}" for n in mostrati) + coda,
            f"    {'':<9} media {p['media']:.1f} · scarto {p['scarto']:.1f}"]


def conta_tic(testo: str) -> dict[str, int]:
    """I tic contabili di un testo. Meno è meglio, per tutti.

    Nessuno di questi vale come soglia assoluta — vedi il commento sopra. Valgono
    come **differenza** fra due versioni della stessa cosa.
    """
    frasi = _frasi(testo)
    aperture = [" ".join(f.split()[:2]).lower().strip("*«»>_-# ") for f in frasi]
    return {
        "frammenti": sum(1 for f in frasi if len(f.split()) <= 6),
        "aperture_ripetute": sum(1 for i in range(len(aperture) - 1)
                                 if aperture[i] and aperture[i] == aperture[i + 1]),
        "antitesi": len(ANTITESI.findall(testo or "")),
        "trattini": len(TRATTINO.findall(testo or "")),
        "maiuscole": sum(1 for m in MAIUSCOLE.findall(testo or "") if m not in SIGLE),
    }


def confronta(prima: str, dopo: str) -> dict:
    """Quanti tic sono calati e quanti saliti, fra due versioni."""
    a, b = conta_tic(prima), conta_tic(dopo)
    delta = {k: b[k] - a[k] for k in a}
    return {
        "delta": delta,
        "migliorati": sum(1 for v in delta.values() if v < 0),
        "peggiorati": sum(1 for v in delta.values() if v > 0),
        "prima": a, "dopo": b,
    }


def versione_git(percorso: Path, revisione: str) -> str | None:
    """Il file com'era a quella revisione, o `None` se lì non c'era."""
    try:
        rel = percorso.resolve().relative_to(ROOT)
    except ValueError:
        return None
    fuori = subprocess.run(["git", "show", f"{revisione}:{rel.as_posix()}"],
                           cwd=ROOT, capture_output=True, text=True)
    return fuori.stdout if fuori.returncode == 0 else None


def rapporto_confronto(f: Path, revisione: str, profilo: bool = False) -> list[str]:
    """Il verdetto su una riscrittura, e — se richiesto — il profilo sotto.

    `profilo` si accende solo sui file nominati sulla riga di comando. Una
    scansione senza argomenti confronta tutto il contenuto, e 255 file per tre
    righe l'uno non sono un rapporto: sono un muro.
    """
    prima = versione_git(f, revisione)
    if prima is None:
        return [f"{f.name}: non esiste a {revisione} — niente da confrontare"]
    if not f.is_file():
        return [f"{f.name}: non esiste adesso"]
    dopo = f.read_text(encoding="utf-8", errors="ignore")
    v = confronta(prima, dopo)
    if not v["migliorati"] and not v["peggiorati"]:
        testa = f"{f.name}: nessun tic cambiato rispetto a {revisione}"
    else:
        segni = ", ".join(f"{k} {d:+d}" for k, d in v["delta"].items() if d)
        verso = ("migliorata" if v["migliorati"] > v["peggiorati"]
                 else "peggiorata" if v["peggiorati"] > v["migliorati"] else "pari")
        testa = f"{f.name}: {verso} rispetto a {revisione} — {segni}"
    if not profilo:
        return [testa]
    return [testa] + righe_profilo("prima", prima) + righe_profilo("dopo", dopo)


def prosa_documento(testo: str) -> list[str]:
    """Le righe di un documento che sono davvero prosa.

    Fuori: blocchi di codice, tabelle, titoli, citazioni e separatori. In una
    tabella il trattino lungo vuol dire «niente» ed è la notazione giusta;
    contarlo lì faceva risultare il CHANGELOG il file peggiore del repo con
    2.819 trattini ogni mille righe, che era un artefatto della misura.
    """
    fuori, dentro_codice = [], False
    for riga in testo.splitlines():
        if riga.lstrip().startswith("```"):
            dentro_codice = not dentro_codice
            continue
        if dentro_codice:
            continue
        nudo = riga.strip()
        if not nudo or nudo[0] in "|#>" or re.fullmatch(r"[-:| ]+", nudo):
            continue
        fuori.append(riga)
    return fuori


def controlla_documento(f: Path) -> list[str]:
    """I tic di una guida, di un ADR, di un piano o di una skill.

    Bersaglio diverso dal contenuto di gioco, quindi tic diversi: qui non ci
    sono read-aloud, e quello che tradisce la macchina è il trattino lungo usato
    come respiro e il numero annunciato prima dell'elenco.
    """
    testo = f.read_text(encoding="utf-8", errors="ignore")
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    righe = prosa_documento(testo)
    if len(righe) < 40:          # sotto quaranta righe la densità non dice niente
        return []
    prosa = "\n".join(righe)
    fuori: list[str] = []

    trattini = len(TRATTINO.findall(prosa))
    per_mille = trattini * 1000 // len(righe)
    if trattini >= SOGLIE_DOC["trattino_minimo"] and per_mille > SOGLIE_DOC["trattino_per_mille"]:
        fuori.append(
            f"{rel}: {trattini} trattini lunghi in {len(righe)} righe di prosa "
            f"({per_mille}/1000, mediana del repo 73): in italiano il trattone "
            "non è un respiro — punto e virgola, due punti, o niente")

    conteggi = conteggi_annunciati(prosa)
    n_cont = len(conteggi)
    if n_cont > SOGLIE_DOC["conteggio"]:
        esempi = ", ".join(f"«{a} {b}»" for a, b in conteggi[:3])
        fuori.append(
            f"{rel}: il numero annunciato prima dell'elenco compare {n_cont} volte "
            f"({esempi}): l'elenco che segue rende il conteggio superfluo")

    n_ant = len(ANTITESI.findall(prosa))
    if n_ant > SOGLIE_DOC["antitesi"]:
        fuori.append(
            f"{rel}: l'antitesi «non X: è Y» compare {n_ant} volte "
            f"(massimo {SOGLIE_DOC['antitesi']} per documento)")
    return fuori


def documenti() -> list[Path]:
    fuori = [p for p in ROOT.rglob("*.md")
             if any(str(p.relative_to(ROOT)).startswith(d) for d in DOCUMENTI)]
    fuori += [ROOT / n for n in DOC_RADICE if (ROOT / n).is_file()]
    return sorted(set(fuori))


#: La chiave con cui ogni rilievo dichiara **quale norma** ha violato.
#:
#: 🔎 **Perche' esiste, dal 2026-09-21.** `controlla()` restituiva una lista di
#: stringhe gia' formattate, e `punteggio_mqm` non poteva usarne nessuna: per
#: contare «quanti calchi» avrebbe dovuto riconoscere la frase italiana con cui
#: il messaggio e' scritto. Cosi' quattro norme entravano nel punteggio e sei,
#: **gia' misurate da questo file**, restavano fuori — non per mancanza di
#: rilevatore, ma perche' il rilevatore non diceva il proprio nome.
#:
#: La forma e' quella di sempre per un misuratore: **una sola computazione, due
#: viste**. `rilievi()` produce i record tipati; `controlla()` ne stampa i
#: messaggi ed e' identica a prima per chi la chiama.
NORME = (
    "terminologia_non_canonica",
    "testo_giocatori_senza_ancore",
    "calco_dall_inglese",
    "antitesi_ripetuta",
    "maiuscole_di_enfasi",
    "trattino_come_respiro",
    "caratteristica_minuscola",
)


def rilievi(f: Path) -> "list[tuple[str, str]]":
    """`(chiave della norma, messaggio)` — la computazione vera.

    Deterministica e idempotente: dipende solo dal contenuto del file e dai
    dati del repo (glossario, nomi canonici), mai dall'ordine delle chiamate
    ne' da uno stato accumulato. Due esecuzioni sullo stesso commit danno la
    stessa lista, nello stesso ordine.
    """
    testo = f.read_text(encoding="utf-8", errors="ignore")
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    righe, readaloud = prosa_e_readaloud(testo)
    if e_per_i_giocatori(f):
        # Il file è per i giocatori: la prosa è tutta la pagina, non solo i box.
        # Restano fuori i titoli, che non sono prosa letta.
        readaloud = "\n".join(r for _, r in righe if not r.lstrip().startswith("#"))
    fuori: "list[tuple[str, str]]" = [
        ("terminologia_non_canonica", m)
        for m in check_glossario(f, testo, rel) + check_forme_escluse(f, testo, rel)]
    if e_per_i_giocatori(f):
        fuori += [("testo_giocatori_senza_ancore", m)
                  for m in check_ancore(f, righe, rel)]

    for n, riga in righe:
        for pattern, perche in CALCHI_SEMPRE:
            m = re.search(pattern, riga, re.I)
            if m:
                fuori.append(("calco_dall_inglese",
                              f"{rel}:{n}: calco — {perche}  «…{m.group(0)}…»"))

    if not readaloud.strip():
        return fuori

    for pattern, perche in CALCHI_READ_ALOUD:
        for m in re.finditer(pattern, readaloud, re.I):
            fuori.append(("calco_dall_inglese",
                          f"{rel}: read-aloud — {perche}  «…{m.group(0)}…»"))

    n_ant = len(ANTITESI.findall(readaloud))
    if n_ant > SOGLIE["antitesi"]:
        fuori.append((
            "antitesi_ripetuta",
            f"{rel}: l'antitesi «non X: è Y» compare {n_ant} volte nei read-aloud "
            f"(massimo {SOGLIE['antitesi']} per documento): alla terza il tavolo sente il telaio"
        ))
    ripulito = ETICHETTA_BATTUTA.sub(" ", CAPPELLO_DM.sub(" ", readaloud))
    portento = Counter(w for w in MAIUSCOLE.findall(ripulito) if w.upper() not in SIGLE)
    if len(portento) > SOGLIE["maiuscole"]:
        elenco = ", ".join(sorted(portento)[:6])
        fuori.append((
            "maiuscole_di_enfasi",
            f"{rel}: {len(portento)} parole in maiuscolo di enfasi nei read-aloud "
            f"({elenco}) — massimo {SOGLIE['maiuscole']}: se sono due, non funzionano più"
        ))
    parole = len(readaloud.split())
    if parole >= 80:
        densita = TRATTINO.findall(readaloud)
        if len(densita) / parole > 0.03:
            fuori.append((
                "trattino_come_respiro",
                f"{rel}: {len(densita)} trattini lunghi in {parole} parole di read-aloud "
                f"— il trattino come respiro è un tic: punto e virgola, due punti, o niente"
            ))
    return fuori


def controlla(f: Path) -> list[str]:
    """I soli messaggi, per chi stampa. Identica a prima del 2026-09-21."""
    return [m for _, m in rilievi(f)]


def file_di_contenuto() -> list[Path]:
    out: list[Path] = []
    for d in ROOT.iterdir():
        if d.is_dir() and d.name.startswith(CONTENUTO):
            out.extend(p for p in d.rglob("*.md") if not p.name.endswith(".hb.md"))
    return sorted(out)


# ─────────────────────────────────────────────────────────────────────────
# §1.2 — caratteristiche e abilità maiuscole (norma WotC/Paizo)
#
# 🔴 **Questa norma era stata archiviata come non misurabile**, il 2026-09-19,
# con questa ragione scritta: *«in italiano* Forza *è anche un sostantivo
# comune, e un rilevatore darebbe più falsi positivi che errori»*. Era vero del
# matcher che avevo in mente — `\bforza\b` pesca **2.014** occorrenze nei 511
# file di gioco, quasi tutte sostantivi comuni — e **falso della norma**.
#
# Il DM, il 2026-09-20: *«se compaiono nello statblock di un PNG sono seguiti da
# un numero… nel caso di prove non dovrebbe essere nella forma "prova di Forza
# CD 25"? In questo modo è più facile distinguerli?»*. Sì: non si cerca la
# **parola**, si cerca la **forma meccanica**, che un sostantivo comune non ha.
#
# Misurato sui 511 file di gioco: **258 occorrenze sotto le quattro forme, 3
# fuori norma, zero falsi positivi** (controllati a mano, uno per uno).
#
# ⚠️ Due tarature che solo la misura poteva dare:
#
#  * **F1 trova quasi nulla** perché questo repo scrive le caratteristiche in
#    **sigla** — `For 25`, `Des 14`, 688 volte — e le sigle sono maiuscole per
#    costruzione. La forma nominata dal DM esiste, è giusta, e qui è rara.
#  * **F2 ha dovuto vietare lo spazio dopo il segno.** Scritta `\s*[+-]\s*\d`
#    catturava *«40.500 mo in oggetti di artigianato + 1 Sacrificio Personale»*:
#    tre falsi positivi su tre. `Nuotare +9` sì, `artigianato + 1` no.
CARATTERISTICHE = ("forza", "destrezza", "costituzione", "intelligenza",
                   "saggezza", "carisma")
#: Le abilità 3.5 nella grafia italiana del repo. Elenco esplicito e non una
#: classe di parole: un'abilità in più che manca è un falso negativo (si
#: aggiunge), una parola comune di troppo sarebbe un falso positivo (non si
#: recupera più).
#:
#: 🔴 **`intuizione` è uscita da qui, e l'ha trovata il cancello stesso.** Al
#: primo giro l'elenco la conteneva e il conto saliva da 3 a 25: ventidue erano
#: *«bonus di intuizione +4»*, che in 3.5 è un **tipo di bonus** (*insight
#: bonus*) e va minuscolo. L'abilità 3.5 è *Percepire Intenzioni*; *Intuizione*
#: è il nome 5e/PF, e questa campagna è 3.5. Quindicesimo caso della stessa
#: famiglia — un criterio largo che si inventa copertura — e il primo in cui a
#: trovarlo è stato il controllo nuovo prima del commit, non una PR dopo.
ABILITA = ("acrobazia", "addestrare animali", "artigianato", "artista della fuga",
           "ascoltare", "camuffare", "cavalcare", "cercare", "concentrazione",
           "decifrare scritture", "diplomazia", "disattivare congegni",
           "equilibrio", "falsificare", "guarire", "intimidire",
           "nascondersi", "nuotare", "osservare", "percepire intenzioni",
           "professione", "raccogliere informazioni", "rapidità di mano",
           "saltare", "sapienza magica", "scalare", "scassinare serrature",
           "seguire tracce", "sopravvivenza", "utilizzare congegni magici",
           "valutare")
_TUTTE = "|".join(re.escape(x) for x in CARATTERISTICHE + ABILITA)
_CAR = "|".join(re.escape(x) for x in CARATTERISTICHE)
_ABI = "|".join(re.escape(x) for x in ABILITA)

FORME_CARATTERISTICA = (
    ("F1 punteggio nello statblock", re.compile(rf"\b({_CAR})\s+(\d{{1,2}})\b", re.I), None),
    ("F2 abilità col modificatore", re.compile(rf"\b({_ABI})\s*[+-]\d{{1,2}}\b", re.I), None),
    ("F3 prova con una CD", re.compile(
        rf"\b(?:prov[ae]|tiri?|TS|test|verifich?[ae])\s+(?:di|su|sulla|sul|della|del)\s+({_TUTTE})\b", re.I),
     re.compile(r"\b(?:CD|DC)\s*\d+", re.I)),
    ("F4 modificatore o bonus", re.compile(
        rf"\b(?:mod\.?|modificatore|bonus|malus|penalità)\s+(?:di|a|alla|al)\s+({_TUTTE})\b", re.I), None),
)


def controlla_caratteristiche(f: Path) -> list[str]:
    """Caratteristiche e abilità maiuscole, cercate per forma e non per parola."""
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    fuori: list[str] = []
    for n, riga in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        for nome, rx, condizione in FORME_CARATTERISTICA:
            if condizione is not None and not condizione.search(riga):
                continue
            for m in rx.finditer(riga):
                if m.group(1)[0].islower():
                    fuori.append(
                        f"{rel}:{n}: «{m.group(0).strip()}» — {nome}: caratteristiche "
                        f"e abilità vanno maiuscole (norma WotC/Paizo)")
    return fuori


def file_di_gioco() -> list[Path]:
    """Il contenuto di gioco, **archivi esclusi come il repo li dichiara**.

    Non si riscrive un elenco di esclusioni: si riusa `ESCLUSI`/`ESCLUSI_NOME`
    di `misura_craft` e il marcatore `_SNAPSHOT-STORICO.md` che le cartelle
    d'archivio si mettono da sole. È il passo 3 della sesta regola d'oro.
    """
    import misura_craft as mc

    snapshot = {p.parent for p in ROOT.rglob("_SNAPSHOT-STORICO.md")}
    out = file_di_contenuto()
    bestiario = ROOT / "Bestiario"
    if bestiario.is_dir():
        out += [p for p in bestiario.rglob("*.md") if not p.name.endswith(".hb.md")]
    return sorted(
        p for p in out
        if not any(x in p.parts for x in mc.ESCLUSI)
        and not any(x in p.name for x in mc.ESCLUSI_NOME)
        and not any(s in p.parents for s in snapshot)
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--strict", action="store_true",
                    help="i rilievi diventano errori (exit 1)")
    ap.add_argument("--documenti", action="store_true",
                    help="misura guide, ADR, piani e skill invece del contenuto")
    ap.add_argument("--caratteristiche", action="store_true",
                    help="caratteristiche e abilità maiuscole (norma WotC/Paizo), "
                         "cercate per forma meccanica e non per parola")
    ap.add_argument("--foglio", action="store_true",
                    help="il foglio di stile (glossario §8) contro il repo: quanti "
                         "refusi aperti, quante scelte del DM in sospeso")
    ap.add_argument("--proponi-grafie", action="store_true",
                    help="coppie di nomi a una lettera di distanza da portare "
                         "al foglio (proposte, non rilievi)")
    ap.add_argument("--prima-dopo", action="store_true",
                    help="confronta i file con una revisione git: dice se una "
                         "riscrittura ha tolto tic o ne ha aggiunti")
    ap.add_argument("--rispetto-a", default="HEAD", metavar="REV",
                    help="la revisione con cui confrontare (default: HEAD)")
    args = ap.parse_args(argv)

    if args.prima_dopo:
        nominati = bool(args.files)
        bersagli = [Path(f).resolve() for f in args.files] or file_di_contenuto()
        righe = [r for f in bersagli
                 for r in rapporto_confronto(f, args.rispetto_a, profilo=nominati)]
        for r in righe:
            # le righe del profilo arrivano gia' rientrate: niente pallino
            print(r if r.startswith("    ") else f"  · {r}")
        print(f"  ({len(bersagli)} file confrontati con {args.rispetto_a})")
        return 0

    if args.foglio or args.proponi_grafie:
        bersagli = ([Path(f).resolve() for f in args.files] if args.files
                    else file_di_gioco())
        if args.proponi_grafie:
            coppie = proponi_grafie(bersagli)
            for a, na, b, nb in coppie:
                print(f"  ? «{a}» {na:4}  ↔  «{b}» {nb:4}")
            print(f"  ({len(coppie)} coppie proposte in {len(bersagli)} file di gioco: "
                  f"decide un umano, e si guarda il contesto prima di scrivere la riga)")
            return 0
        righe, refusi = rapporto_foglio(bersagli)
        print(f"validate_prosa --foglio: {len(bersagli)} file di gioco, archivi esclusi")
        print("\n".join(righe))
        aperte = sum(1 for v in forme_escluse() if v[2] == "DM?")
        print(f"  → {refusi} refusi aperti · {aperte} scelte del DM in sospeso")
        return 1 if refusi and args.strict else 0

    if args.caratteristiche:
        bersagli = [Path(f).resolve() for f in args.files] if args.files else file_di_gioco()
        rilievi = [r for f in bersagli if f.is_file()
                   for r in controlla_caratteristiche(f)]
        if not rilievi:
            print(f"✓ validate_prosa --caratteristiche: {len(bersagli)} file di gioco "
                  f"— ogni caratteristica e abilità in forma meccanica è maiuscola")
            return 0
        print(f"✗ validate_prosa --caratteristiche: {len(rilievi)} rilievi "
              f"in {len(bersagli)} file di gioco")
        for r in rilievi:
            print(f"  - {r}")
        return 1

    if args.documenti:
        bersagli = [Path(f).resolve() for f in args.files] if args.files else documenti()
        esamina = controlla_documento
    else:
        bersagli = [Path(f).resolve() for f in args.files] if args.files else file_di_contenuto()
        esamina = controlla
    rilievi: list[str] = []
    for f in bersagli:
        if f.is_file():
            rilievi += esamina(f)

    che = "documenti" if args.documenti else "file"
    if not rilievi:
        print(f"✓ validate_prosa: {len(bersagli)} {che} — nessun tic oltre soglia")
        return 0
    testa = "✗" if args.strict else "  ⚠"
    print(f"{testa} validate_prosa: {len(rilievi)} rilievi in {len(bersagli)} {che}")
    for r in rilievi[:60]:
        print(f"  - {r}")
    if len(rilievi) > 60:
        print(f"  … e altri {len(rilievi) - 60}")
    if not args.strict:
        norma = ("`rumblingstone-prosa-documenti`" if args.documenti
                 else "`italiano-nativo.md`")
        print(f"  (non bloccante: la norma è {norma}, questo la misura)")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
