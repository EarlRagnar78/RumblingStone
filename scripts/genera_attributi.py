#!/usr/bin/env python3
"""genera_attributi.py — le caratteristiche dei PNG, VINCOLATE prima che generate.

## Perche' esiste

`RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI` ha misurato il muro: solo **14
statblocchi su 110** dichiarano `attributi`, e senza For/Des/Cos non si ricava
nessuna delle identita' profonde — i pf dai DV e dalla Costituzione, i TS dalla
progressione di classe, l'attacco da BAB + modificatore + taglia. Quelle tre
identita' sono la strada verso il **primo `critico`** del punteggio, che il
κ 0,0 di F3.3 dice mancare.

Il DM, il 2026-09-21: *«generare coerentemente gli statblock nei 96 che non li
hanno usando generatori random che utilizzano le regole di D&D 3.5 e/o PF1e o
gli stat array elite e standard del manuale del DM (usa le regole deterministiche
piu' affidabili con una percentuale di random in modo che non siano tutti
uguali)»*.

## Il principio: prima si copia, poi si legge, poi si sceglie, e il caso per ultimo

Cinque strati, in quest'ordine. Ogni caratteristica scende di strato solo se il
precedente non la determina. Misurato sui 93 file, 2026-09-23 (Karruk e'
uscito dalla marca: le sue caratteristiche ora sono del DM):

| strato | da dove viene | file |
|---|---|---:|
| **0a · copiato** | la sestina che la **scheda stessa** scrive nella prosa, in inglese o in italiano | **41** |
| **0b · trascritto** | la fonte citata in `Bestiario/pregen-pcgen/` (export PCGen, SRD) | **37** |
| **1 · letto** | la Destrezza scritta in `ca-dettaglio` (`+3 Dex`) | } sugli |
| **2 · derivato** | Des dalla CA di contatto e dall'iniziativa; Cos da `pf` e `pf-dado`; For da BAB e lotta | } altri |
| **2-quinquies · tetto** | un TS scritto **sotto** l'atteso abbassa Cos, Des o Sag; l'iniziativa senza talenti ammette due Des | } 15 |
| **3 · scelto** | array del **Manuale del DM 3.5**, per ruolo, con taglia e razza SRD | **15** |

🔴 **Gli strati 0a e 0b la prima stesura non li aveva.** Generava numeri per
42 file che citano la loro fonte, e per 27 che li scrivevano due righe sotto il
blocco. Il conto di ADR-0064 («55 scelti») era sbagliato per questo: i
file davvero scelti sono **18**.

🔴 **Lo strato 3 e' una scelta, non una misura**, e per questo **ogni blocco
scritto porta `[INFERRED — needs DM confirmation]`**, con la sua provenienza e
le divergenze trovate: e' la regola 5 di `AGENTS.md`. Il confine con ADR-0033
lo discutono ADR-0064 e ADR-0065.

## Quanto sbaglia lo strato 3, misurato

Dove la risposta vera c'e', `--taratura` genera **come se non ci fosse** e
confronta, su due banchi separati:

| banco | file | errore medio | entro ±1 di mod |
|---|---:|---:|---:|
| fonti citate — **in campione** (le regole sono state scelte guardandole) | 37 | 1,50 | 85% |
| sestine delle schede — **fuori campione** (trovate dopo) | 41 | **1,54** | 83% |

Prima dello strato 2-quinquies erano 1,63 e 1,84. ⚠️ Il banco fuori campione non e'
piu' del tutto fuori: le tre sestine nuove sono dell'ogre micelio, dell'ogre
frantumapietra e di Zin'thara (Karruk ne e' uscito), e l'ogre frantumapietra
era uno degli otto scarti da cui il tetto e' nato. Sulle altre 38 le regole
non sono state scelte.

Il secondo numero e' quello che conta: dice quanto il generatore vale su un
file che non ha visto. Le mentali (Int e Car sopra i 2 punti) restano le piu'
lontane, perche' il ruolo dice come un PNG combatte e non quanto e'
intelligente.

## Gli array, e quando si usa quale

Manuale del DM 3.5, PNG, tramite `dmcore.tabelle`:

* **elite** — `15 14 13 12 10 8` — per le **creature** e per i ruoli di
  `T.RUOLI_ELITE` (boss, elite, leader, caster…);
* **standard** — `13 12 11 10 9 8` — per gli altri PNG con livelli di classe.

Poi l'**avanzamento**, sul GS come surrogato dei DV (dichiarato: i DV totali
stanno nel `tipo` solo nell'8% dei file); la **taglia** SRD per le creature
(*Improving Monsters*: Large For +8, Des −2, Cos +4) e per i PNG di razza
mostruosa; i **modificatori razziali** SRD per i PNG di razza comune. Non morti:
**Cos —**. Scheletri e zombi: **Int —, Sag 10, Car 1**.

## Il caso: quanto, e perche' a seme fisso

Il DM ha chiesto *«una percentuale di random perche' non siano tutti uguali»*.
La variazione e' **±1 su due caratteristiche secondarie, a somma zero**. Non
tocca mai la caratteristica principale del ruolo, e non tocca lo strato 0.

🔴 **Il seme e' il nome del file**, non l'orologio. Due esecuzioni sullo stesso
repo danno gli **stessi** numeri: un generatore che a ogni giro cambia il
canone non e' uno strumento, e' un dado che scrive sui file.

## Cosa ha trovato strada facendo

🐛 **`pf-dado` in 20 statblocchi su 95 e' il danno di un'arma**, non i dadi
vita: `1d8+7` accanto a «hp 93 (12 HD)». Il controllo e' `pf_dado_sospetto`,
e lo usa anche `validate_bestiario --rules`.

🐛 **Una parentesi dopo il punteggio nascondeva la sestina** (`_NOTA`):
«For 25 (21 base +4 innesto)». Tre schede finivano all'array, e Zin'thara, una
maga con Int 22, ne usciva con Car 21.

🐛 **Il giro circolare con `pf-dado`**: dove la Cos era generata,
`conformita_statblocchi` ricavava il bonus dei dadi vita dai pf supponendo la
media, e `cos_da_pf` ricavava la Cos da quel bonus. Il generatore confermava
se stesso: Khorn scrive «8d10+24, Cos 16» e ne usciva con Cos 18. Ora il bonus
viene prima dalla Tempra, che e' un'identita' esatta.

## Cosa NON fa, dichiarato

* **Non tocca i file con `attributi` scritti a mano**, ne' i `[POINTER]`, che
  per progetto rimandano al file d'arco (ADR-0021). `--rigenera` riscrive
  **solo** i blocchi che portano la sua marca.
* **Non legge il PDF** del death tyrant: la sola stdlib non lo apre, e `--check`
  in CI deve poter rigenerare tutto. Quel file resta generato, e lo dice.
* **Non verifica** che pf, TS e attacco tornino con le caratteristiche: lo fa
  `conformita_statblocchi.py`, che queste caratteristiche rendono possibile.

## Uso

    python3 scripts/genera_attributi.py              # proposta a video, non scrive
    python3 scripts/genera_attributi.py --scrivi     # applica, marcando [INFERRED]
    python3 scripts/genera_attributi.py --rigenera   # riscrive i soli blocchi suoi
    python3 scripts/genera_attributi.py --taratura   # errore dello strato 3 sulle fonti
    python3 scripts/genera_attributi.py --check      # esce 1 se un blocco generato non torna
                                                     # con la regola, o e' duplicato
"""
from __future__ import annotations

import argparse
import html
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

# 🔴 Le tabelle SRD stanno in `dmcore/tabelle.py`, e `genera_creatura` le usa
# gia'. La prima stesura di questo script le aveva **ricopiate**, e ricopiando
# aveva sbagliato due righe: il ranger a d10 (nel 3.5 e' d8) e «minuta» e
# «minuscola» scambiate. Una tabella, un posto.
from dmcore import tabelle as T  # noqa: E402

#: Manuale del DM 3.5 — gli array dei PNG (identici alle *heroic*/*basic* PF1e).
ARRAY_ELITE = T.ELITE
ARRAY_STANDARD = T.BASIC

#: Il ruolo dichiarato decide **l'ordine di priorita'** delle sei
#: caratteristiche: il valore piu' alto dell'array va alla prima della riga.
#: Si cerca la prima parola chiave che compare nel ruolo, in quest'ordine.
PROFILI = (
    ("psionic",     ("Int", "Cos", "Des", "Sag", "Car", "For")),
    ("psi",         ("Int", "Cos", "Des", "Sag", "Car", "For")),
    ("arcane",      ("Int", "Des", "Cos", "Car", "Sag", "For")),
    ("blaster",     ("Int", "Des", "Cos", "Car", "Sag", "For")),
    ("divine",      ("Sag", "Cos", "For", "Car", "Des", "Int")),
    ("divino",      ("Sag", "Cos", "For", "Car", "Des", "Int")),
    ("warpriest",   ("Sag", "For", "Cos", "Car", "Des", "Int")),
    ("envoy",       ("Car", "Des", "Cos", "Int", "Sag", "For")),
    ("subdolo",     ("Car", "Des", "Cos", "Int", "Sag", "For")),
    ("infiltrator", ("Des", "Car", "Cos", "Int", "Sag", "For")),
    ("stealth",     ("Des", "Car", "Cos", "Int", "Sag", "For")),
    ("caster",      ("Car", "Des", "Cos", "Int", "Sag", "For")),
    ("gish",        ("For", "Int", "Cos", "Des", "Sag", "Car")),
    ("ranged",      ("Des", "For", "Cos", "Sag", "Int", "Car")),
    ("scout",       ("Des", "Sag", "Cos", "For", "Int", "Car")),
    ("skirmisher",  ("Des", "For", "Cos", "Sag", "Int", "Car")),
    ("ambusher",    ("Des", "Sag", "Cos", "For", "Int", "Car")),
    ("flier",       ("Des", "For", "Cos", "Sag", "Car", "Int")),
    ("aerial",      ("Des", "Cos", "For", "Sag", "Car", "Int")),
    ("mount",       ("For", "Cos", "Des", "Sag", "Car", "Int")),
    ("brute",       ("For", "Cos", "Des", "Sag", "Car", "Int")),
    ("defender",    ("Cos", "For", "Des", "Sag", "Car", "Int")),
    ("guard",       ("Cos", "For", "Des", "Sag", "Car", "Int")),
    ("tank",        ("Cos", "For", "Des", "Sag", "Car", "Int")),
    ("guardian",    ("Cos", "For", "Des", "Sag", "Car", "Int")),
    ("commander",   ("Car", "For", "Cos", "Sag", "Des", "Int")),
    ("leader",      ("Car", "For", "Cos", "Sag", "Des", "Int")),
    ("officer",     ("Car", "For", "Cos", "Sag", "Des", "Int")),
    ("shock",       ("For", "Des", "Cos", "Sag", "Car", "Int")),
    ("melee",       ("For", "Cos", "Des", "Sag", "Car", "Int")),
    ("fodder",      ("For", "Cos", "Des", "Sag", "Car", "Int")),
    ("wave",        ("For", "Cos", "Des", "Sag", "Car", "Int")),
    ("hazard",      ("Cos", "For", "Des", "Sag", "Car", "Int")),
)
PROFILO_DI_RIPIEGO = ("For", "Cos", "Des", "Sag", "Car", "Int")
ELITE = T.RUOLI_ELITE

ORDINE = ("For", "Des", "Cos", "Int", "Sag", "Car")

#: I modificatori di taglia alla CA, per ricavare la Destrezza dalla CA di contatto.
TAGLIA = {nome: ca for nome, (_, ca) in T.TAGLIE.items()}

BLOCCO = re.compile(r"```statblocco\n(.*?)```", re.S)
DES_SCRITTA = re.compile(r"([+-]\s*\d+)\s*(?:Des|Dex|destrezza)\b", re.I)
CONTATTO = re.compile(r"(?:touch|contatto)\s*(\d+)", re.I)
#: Le abbreviazioni con cui le schede scrivono le classi, le due classi di
#: prestigio SRD e il dado di ogni classe stanno in `dmcore.progressione`
#: (ADR-0066). `PRESTIGIO` qui resta nella forma di prima: {classe: dado}.
from dmcore.progressione import ABBREVIAZIONI, DADO_DI_CLASSE  # noqa: E402,F401
from dmcore import progressione as _P  # noqa: E402
PRESTIGIO = {n: v[0] for n, v in _P.PRESTIGIO.items()}
#: Se il `tipo` nomina una classe, lo statblocco e' un PNG e gli array del
#: Manuale del DM sono lo strumento giusto. Se no, e' una creatura.
CLASSE_NEL_TIPO = re.compile(
    r"\b(" + "|".join(sorted(map(re.escape, DADO_DI_CLASSE), key=len, reverse=True))
    + r")\w*\s*\d+", re.I)
NON_MORTO = re.compile(r"\b(?:undead|non[ -]?mort[oi])\b", re.I)
MODELLO_SENZA_MENTE = re.compile(r"skelet|schelet|zombi", re.I)


mod = T.mod


def da_modificatore(m: int) -> int:
    """Il punteggio piu' basso che da' quel modificatore: 10 + 2m."""
    return max(1, 10 + 2 * m)


def taglia_di(testo: str) -> int:
    # 🐛 le schede di maggio scrivono la taglia in «**Size/Type**», non in
    # `tipo`: leggendo solo il campo, una creatura Grande pesava come Media, e
    # la Forza ricavata dalla lotta del razorfiend rosso usciva 30 invece di 22
    tipo = (re.search(r"^tipo:\s*(.+)$", testo, re.M)
            or re.search(r"\*\*Size/Type\*\*:?\s*([^|\n]+)", testo))
    if not tipo:
        # se nessuno la scrive, la dice il dettaglio della CA: «(-1 size, …)».
        # 🐛 Non la prosa: il primo «Medium …» del loxo sciamano e' il suo
        # compagno animale, e la creatura e' Grande.
        m = re.search(r"^ca-dettaglio:.*?([+-]\d)\s*(?:size|taglia)\b", testo, re.M | re.I)
        return int(m.group(1)) if m else 0
    basso = tipo.group(1).lower()
    for nome, val in TAGLIA.items():
        if re.search(rf"\b{nome}\b", basso):
            return val
    return 0


def des_vincolata(testo: str, gs: float = 30.0) -> "tuple[int, str] | None":
    """Strato 1 e 2: la Destrezza che il file **gia' dichiara**."""
    d = re.search(r"^ca-dettaglio:\s*(.+)$", testo, re.M)
    if not d:
        return None
    m = DES_SCRITTA.search(d.group(1))
    if m:
        return da_modificatore(int(m.group(1).replace(" ", ""))), "letta da ca-dettaglio"
    ca = re.search(r"^ca:\s*(\d+)", testo, re.M)
    c = CONTATTO.search(d.group(1))
    if c and ca:
        # contatto = 10 + mod Des + taglia  →  mod Des = contatto − 10 − taglia
        m_des = int(c.group(1)) - 10 - taglia_di(testo)
        # la CA di contatto somma anche deviazione e schivata: se il numero
        # che ne esce non e' credibile per il GS, la differenza non e' Destrezza
        if -5 <= m_des and plausibile(m_des, gs):
            return da_modificatore(m_des), "derivata dalla CA di contatto"
    return None


PF_DADO = re.compile(r"^pf-dado:\s*(.+)$", re.M)
DV_DICHIARATI = re.compile(r"\((\d+)\s*(?:HD|DV)\)|^tipo:.*?\b(\d+)\s*(?:HD|DV)\b", re.M)
PEZZO_DADO = re.compile(r"(\d+)d(\d+)")
BONUS_DADO = re.compile(r"([+-]\s*\d+)")
#: Sotto questo il modificatore non e' una Costituzione ma un `pf` scritto male.
MOD_MINIMO = -2


def plausibile(m: int, gs: float) -> bool:
    """Un modificatore **derivato** e' credibile solo se il GS lo regge.

    🐛 **La prima guardia era cieca al GS** (`-2 … +12`) e lasciava passare tre
    Costituzioni da 34: un duergar mago da GS 4, un loxo da GS 4, un ogre da
    GS 8. Tutti e tre per la stessa ragione — `pf-dado` registra solo i DV
    razziali di una creatura che ha anche livelli di classe — e tutti e tre
    con un +12 che nessuna creatura di quella sfida ha. Il tetto `3 + GS/2`
    lascia passare il +8 del bruto da GS 11 (`14d8`, 172 pf: e' vero) e
    respinge i tre.
    """
    return MOD_MINIMO <= m <= 3 + gs / 2


#: La formula dei DV scritta dal DM: «**DV 4d8 + 6d12**», «HD 2d8+2d8+8»,
#: «**HD**: 10d10+80». E' il dato piu' affidabile, perche' e' l'unico che
#: nomina **tutti** i dadi: in parecchi file `pf-dado` registrava i soli DV
#: razziali (`4d8` per un ogre con sei livelli da barbaro).
FORMULA_DV = re.compile(
    r"\b(?:DV|HD)\**:?\**\s*(\d+d\d+(?:\s*\+\s*\d+d\d+)*)(\s*[+-]\s*\d+(?!\s*d))?")


def dadi_vita(testo: str) -> "tuple[list, int | None, str] | None":
    """([(n, faccia)], bonus o None, da dove) — i dadi vita della creatura.

    In quest'ordine: la formula scritta, poi `pf-dado` se non e' sospetto.
    None se nessuno dei due c'e': ricostruirli dalle classi e' un altro
    passo, e chi lo fa lo deve dichiarare.
    """
    m = FORMULA_DV.search(testo)
    if m:
        dadi = [(int(a), int(b)) for a, b in PEZZO_DADO.findall(m.group(1))]
        bonus = int(m.group(2).replace(" ", "")) if m.group(2) else None
        return dadi, bonus, "formula scritta"
    md = PF_DADO.search(testo)
    if md and not pf_dado_sospetto(testo):
        dadi = [(int(a), int(b)) for a, b in PEZZO_DADO.findall(md.group(1))]
        resto = BONUS_DADO.findall(PEZZO_DADO.sub("", md.group(1)))
        return dadi, (sum(int(x.replace(" ", "")) for x in resto) if resto else None), "pf-dado"
    return None


ROBUSTEZZA = re.compile(r"\b(?:Toughness|Robustezza)\b(?!\s+Migliorata)", re.I)
ROBUSTEZZA_MIGLIORATA = re.compile(r"\b(?:Improved Toughness|Robustezza Migliorata)\b", re.I)


def robustezza(testo: str, dv: int) -> int:
    """I pf fissi dei talenti: Robustezza +3, Robustezza Migliorata +1 per DV.

    🐛 Contarle come lo stesso talento dava al duergar guerriero un bonus di 9
    invece di 8, e da quel 9 diviso per 2 DV usciva Cos 18 dove la fonte dice 16.
    """
    migliorata = ROBUSTEZZA_MIGLIORATA.search(testo)
    semplice = ROBUSTEZZA.search(ROBUSTEZZA_MIGLIORATA.sub("", testo))
    return (3 if semplice else 0) + (dv if migliorata else 0)


def pf_dado_sospetto(testo: str, gs: "float | None" = None) -> "str | None":
    """Perche' `pf-dado` **non** registra i dadi vita, o None se sembra farlo.

    🐛 **Il campo non sempre registra i dadi vita.** In 20 statblocchi su 95
    `pf-dado` porta **il danno dell'arma** — `1d8+7` accanto a «hp 93 (12
    HD)» e' il martello di Morlin — e la prima stesura del generatore ne
    ricavava Cos 24. Tre controlli, dal piu' certo al piu' indiziario; lo usa
    anche `validate_bestiario --rules`, perche' una norma ha un rilevatore.
    """
    md = PF_DADO.search(testo)
    if not md:
        return None
    pezzi = PEZZO_DADO.findall(md.group(1))
    dv = sum(int(a) for a, _ in pezzi)
    if not dv:
        return None
    if gs is None:
        # 🐛 chi chiamava senza GS saltava il terzo controllo, e `1d8+2` di un
        # chierico di 3° passava per dadi vita. Il GS sta nel blocco: si legge.
        mg = re.search(r"^gs:\s*([\d.,]+)", testo, re.M)
        gs = float(mg.group(1).replace(",", ".")) if mg else None
    # 0 · la formula scritta nomina altri dadi: il campo e' parziale o e' un'arma
    f = FORMULA_DV.search(testo)
    if f:
        scritti = sorted((int(a), int(b)) for a, b in PEZZO_DADO.findall(f.group(1)))
        if sorted((int(a), int(b)) for a, b in pezzi) != scritti:
            return (f"pf-dado «{md.group(1).strip()}» non ha i dadi della formula scritta "
                    f"«{f.group(1).strip()}»")
    # 1 · il testo dichiara i DV, e non tornano coi dadi
    dichiarati = DV_DICHIARATI.search(testo)
    if dichiarati:
        n = int(next(g for g in dichiarati.groups() if g))
        if n != dv:
            return (f"pf-dado «{md.group(1).strip()}» ha {dv} dad{'o' if dv == 1 else 'i'}, "
                    f"il testo dichiara {n} DV")
    # 2 · l'umanoide senza DV razziali tira solo il dado delle sue classi (SRD)
    tipo = re.search(r"^tipo:\s*(.+)$", testo, re.M)
    if tipo and re.search(r"\bhumanoid|umanoide", tipo.group(1), re.I):
        attesi = {DADO_DI_CLASSE[c.lower()] for c in CLASSE_NEL_TIPO.findall(tipo.group(1))}
        facce = {int(b) for _, b in pezzi}
        if attesi and not (facce & attesi):
            return (f"pf-dado «{md.group(1).strip()}» in d{'/d'.join(map(str, sorted(facce)))}, "
                    f"ma le classi del tipo tirano d{'/d'.join(map(str, sorted(attesi)))}")
    # 3 · un dado solo a GS 2 o piu' e' quasi sempre un'arma (indizio, non prova)
    if gs is not None and dv == 1 and gs >= 2 and not dichiarati:
        return f"pf-dado «{md.group(1).strip()}» ha un dado solo a GS {gs:g}"
    return None


def cos_da_pf(testo: str, gs: float = 30.0) -> "tuple[int, str] | None":
    """Strato 2-bis: la Costituzione **si ricava** da `pf` e `pf-dado`.

    In 3.5 i punti ferita medi sono `DV × (faccia+1)/2 + DV × mod Cos`, quindi
    col totale e i dadi il modificatore e' aritmetica:

        mod Cos = (pf − media dei dadi − bonus scritti) / DV

    🔴 **E serve una guardia, perche' il campo mente in un caso preciso.** In
    molti file `pf-dado` registra i **soli DV razziali** di una creatura che ha
    anche livelli di classe: `4d8` accanto a `pf 80` darebbe Cos +15, cioe' 40.
    Misurato sul repo, l'identita' torna su **30 statblocchi su 95** e sugli
    altri 65 il campo e' sotto-specificato. Fuori dalla fascia plausibile il
    risultato **si butta** e si scende all'array: un numero derivato male e'
    peggio di un numero scelto, perche' sembra misurato.
    """
    mp = re.search(r"^pf:\s*(\d+)", testo, re.M)
    md = PF_DADO.search(testo)
    if not (mp and md):
        return None
    pezzi = PEZZO_DADO.findall(md.group(1))
    if not pezzi:
        return None
    dv = sum(int(a) for a, _ in pezzi)
    if not dv:
        return None
    if pf_dado_sospetto(testo, gs):
        return None
    media = sum(int(a) * (int(b) + 1) / 2 for a, b in pezzi)
    bonus = sum(int(x.replace(" ", "")) for x in BONUS_DADO.findall(PEZZO_DADO.sub("", md.group(1))))
    talenti = robustezza(testo, dv)
    m_cos = round((int(mp.group(1)) - media - talenti) / dv)
    # il bonus scritto (`7d4+7`) e' Cos × DV **piu' i talenti**: tolti quelli,
    # deve dividersi esatto per i DV, o non e' una Costituzione
    if bonus and dv:
        netto = bonus - talenti
        if netto % dv:
            return None
        m_cos = netto // dv
    if not plausibile(m_cos, gs):
        return None
    return da_modificatore(m_cos), f"ricavata da pf {mp.group(1)} su {dv} DV"


# ---------------------------------------------------------------------------
# Strato 0 · la fonte citata
# ---------------------------------------------------------------------------
#: 🔴 **Lo strato che la prima stesura non aveva.** 42 dei 94 statblocchi
#: senza `attributi` citano un export in `Bestiario/pregen-pcgen/`, e 41 di
#: quelle fonti portano le sei caratteristiche in chiaro. Per quei file i
#: numeri **esistono**: generarli era inventare quello che bastava copiare.
CITAZIONE = re.compile(r"pregen-pcgen/[^)`|\]\n]*?\.(?:html?|pcg|txt)")
_V = r"(\d+|—|-(?!\s*\d))"     # un punteggio, o «—»; «-4» e' un modificatore, e si scarta
#: La sestina, in inglese (SRD, PCGen) **e in italiano** (le schede del DM:
#: «For 31, Des 13, Cos 23, Int 10, Sag 12, Car 11»). 🐛 La prima stesura
#: capiva solo l'inglese, e il bruto deforme, che scrive in italiano, finiva
#: all'array con la Forza ricavata da una lotta che dimentica un talento.
_SEP = r"\s*[,;]?\s*"
#: 🐛 **La parentesi dopo il punteggio.** L'ogre micelio scrive «For 25 (21
#: base +4 innesto), Des 8» e Zin'thara «Int 22 (20 + *fascia* +2)»: la regola
#: di prima non ammetteva niente fra il numero e la virgola, e le due schede
#: finivano all'array — Zin'thara, una maga, con Car 21 e Int 11. La
#: parentesi spiega il numero e non lo sostituisce: si salta, e il numero resta.
_NOTA = r"(?:\s*\([^)\n]{0,60}\))?"
SESTINA = re.compile(
    r"\b(?:Str|For)\w*\s*:?\s*" + _V + _NOTA + _SEP + r"(?:Dex|Des)\w*\s*:?\s*" + _V + _NOTA +
    _SEP + r"(?:Con|Cos)\w*\s*:?\s*" + _V + _NOTA + _SEP + r"Int\w*\s*:?\s*" + _V + _NOTA +
    _SEP + r"(?:Wis|Sag)\w*\s*:?\s*" + _V + _NOTA + _SEP + r"(?:Cha|Car)\w*\s*:?\s*" + _V, re.I)
PCG_STAT = re.compile(r"^STAT:(STR|DEX|CON|INT|WIS|CHA)\|SCORE:(\d+)", re.M)
_PCG = ("STR", "DEX", "CON", "INT", "WIS", "CHA")


def _testo_fonte(p: Path) -> str:
    """Il testo della fonte, **con gli a capo**: servono a trovare le intestazioni."""
    t = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix in (".htm", ".html"):
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return t


def _punteggio(v: str):
    return "—" if v in ("—", "-") else int(v)


def _parole(testo: str) -> frozenset:
    """Le parole di un nome, senza numeri e senza plurale inglese."""
    fuori = set()
    for w in re.findall(r"[a-zà-ù]+", testo.lower()):
        if len(w) > 4 and w.endswith("s"):
            w = w[:-1]
        fuori.add(w)
    return frozenset(fuori)


def parole_del_file(nome_file: str) -> frozenset:
    radice = re.sub(r"-cr[\d.]+$", "", Path(nome_file).stem)
    return _parole(" ".join(t for t in radice.split("-") if not re.search(r"\d", t)))


INTESTAZIONE = re.compile(r"^\s*\d+[.)]\s+([A-Za-z][A-Za-z ,'-]{2,60}?)\s*$", re.M)


def sestine_citate(testo: str) -> "list[tuple[str, tuple, bool, frozenset]]":
    """(fonte, sestina in ORDINE, dedicata?, parole dell'intestazione) per fonte.

    *Dedicata* vuol dire che la fonte porta **una** sola sestina: e' la scheda
    di quella creatura, non un file che ne raccoglie parecchie. Per le altre
    conta l'**ultima intestazione numerata** prima della sestina («2. Myconid
    Elite Guards»): e' l'unico modo di sapere di chi e' senza indovinare.
    """
    fuori = []
    for rel in sorted(set(CITAZIONE.findall(testo))):
        p = ROOT / "Bestiario" / rel
        if not p.is_file():
            continue
        if p.suffix == ".pcg":
            s = dict(PCG_STAT.findall(p.read_text(encoding="utf-8", errors="replace")))
            if len(s) == 6:
                fuori.append((rel, tuple(int(s[k]) for k in _PCG), True, frozenset()))
            continue
        t = _testo_fonte(p)
        trovate = []
        for m in SESTINA.finditer(t):
            sestina = tuple(_punteggio(v) for v in m.groups())
            capi = INTESTAZIONE.findall(t, 0, m.start())
            trovate.append((sestina, _parole(capi[-1]) if capi else frozenset()))
        distinte = {x for x, _ in trovate}
        fuori += [(rel, x, len(distinte) == 1, capo) for x, capo in trovate]
    return fuori


def dalla_fonte(nome_file: str, testo: str) -> "tuple[dict, str] | None":
    """Strato 0: una sestina **sola**, scelta con una regola che si puo' dire.

    1. se le fonti *dedicate* concordano su una sestina, e' quella;
    2. altrimenti, quella **sola** la cui intestazione ha le parole del nome
       del file (`myconid-elite-guard` ↔ «Myconid Elite Guards»);
    3. altrimenti niente.

    🐛 **Una terza regola c'era, ed e' stata tolta.** «Fra le candidate, la
    sola che torna con CA e pf del file» ha dato al *myconid worker* la
    sestina del *sovrano*, For 26: la fonte e' una bozza con GS diversi da
    quelli del Bestiario, e un numero che torna per caso non dice di chi e'.
    Una trascrizione sbagliata con scritto «trascritta» e' peggio di un numero
    generato, perche' sembra una misura.
    """
    cand = sestine_citate(testo)
    if not cand:
        return None
    dedicate = {t for _, t, d, _ in cand if d}
    if len(dedicate) == 1:
        t = dedicate.pop()
        fonte = next(f for f, x, d, _ in cand if d and x == t)
        return dict(zip(ORDINE, t)), f"trascritta dalla fonte `{Path(fonte).name}`"
    mie = parole_del_file(nome_file)
    per_nome = {t for _, t, _, capo in cand if capo and capo == mie}
    if len(per_nome) == 1:
        t = per_nome.pop()
        fonte = next(f for f, x, _, capo in cand if x == t and capo == mie)
        return (dict(zip(ORDINE, t)),
                f"trascritta da `{Path(fonte).name}`, sotto l'intestazione che porta il suo nome")
    return None


def dalla_scheda(testo: str) -> "tuple[dict, str] | None":
    """Strato 0a: le caratteristiche **scritte nella scheda stessa**.

    🔴 **Lo strato che mancava anche alla seconda stesura**, trovato il
    2026-09-23 correggendo `pf-dado`: il sergente hobgoblin scrive
    «**Abilities**: Str 14, Dex 12, Con 14, Int 10, Wis 10, Cha 8» nella sua
    prosa, e il generatore gli aveva dato Car 17. **27 dei 55** file che ADR-0064
    contava come «scelti» avevano i numeri del DM scritti due righe sotto il
    blocco. Sono i numeri che si giocano: battono la fonte e battono i vincoli.

    Si legge fuori dal blocco e fuori dalle righe di marca, e solo se la
    scheda porta **una** sestina: due (una variante, un'ira) sono una scelta.
    """
    fuori = BLOCCO.sub("", testo)
    fuori = "\n".join(r for r in fuori.splitlines() if not r.startswith("> [INFERRED"))
    trovate = {tuple(_punteggio(v) for v in m) for m in SESTINA.findall(fuori)}
    if len(trovate) != 1:
        return None
    return dict(zip(ORDINE, trovate.pop())), "letta dalla riga delle caratteristiche della scheda stessa"


BAB_SCRITTO = re.compile(r"(?:\bBAB|Attacco base)(?:/(?:Grapple|Lotta))?\**:?\**\s*([+-]\d+)")
LOTTA_SCRITTA = re.compile(r"(?:\b(?:Lotta|Grapple)\**:?\**\s*([+-]\d+))|"
                           r"(?:BAB/(?:Grapple|Lotta)\**:?\**\s*[+-]\d+/\**([+-]\d+))")
#: SRD 3.5, modificatore speciale di taglia alla lotta.
LOTTA_TAGLIA = {8: -16, 4: -12, 2: -8, 1: -4, 0: 0, -1: 4, -2: 8, -4: 12, -8: 16}
LOTTA_MIGLIORATA = re.compile(r"\b(?:Improved Grapple|Lotta Migliorata|Lottare Migliorato)\b", re.I)


def numeri_della_fonte(testo: str) -> dict:
    """pf, TS, BAB e lotta come li scrive la prima fonte citata che li porta."""
    out = {}
    for rel in sorted(set(CITAZIONE.findall(testo))):
        p = ROOT / "Bestiario" / rel
        if not p.is_file():
            continue
        f = re.sub(r"\s+", " ", _testo_fonte(p))
        m = re.search(r"Fort\w*\s*:?\s*([+-]\d+),?\s*Ref\w*\s*:?\s*([+-]\d+),?\s*Will\s*:?\s*([+-]\d+)", f)
        if m:
            out.update(zip(("Temp", "Rifl", "Vol"), (int(x) for x in m.groups())))
        m = re.search(r"(?:Base Atk|Base Attack(?:/Grapple)?)\s*:?\s*([+-]\d+)(?:\s*/\s*([+-]\d+))?", f)
        if m:
            out["BAB"] = int(m.group(1))
            if m.group(2):
                out["lotta"] = int(m.group(2))
        m = re.search(r"\bGrp\s*([+-]\d+)", f)
        if m:
            out["lotta"] = int(m.group(1))
        m = re.search(r"\bhp\s*(\d+)", f)
        if m:
            out["pf"] = int(m.group(1))
        m = re.search(r"\bInit(?:iative)?\s*:?\s*([+-]?\d+)", f)
        if m:
            out["iniziativa"] = int(m.group(1))
        # PCGen: «+3 (1d10+3, Sword, bastard, Masterwork)» e' il primo attacco
        m = re.search(r"([+-]\d+)\s*\(\d+d\d+(?:[+-]\d+)?,\s*[A-Z]", f)
        if m:
            out["attacco"] = int(m.group(1))
    return out


INIZIATIVA_SCRITTA = re.compile(r"^iniziativa:\s*([+-]?\d+)", re.M)
INIZIATIVA_MIGLIORATA = re.compile(
    r"\b(?:Improved Initiative|Iniziativa(?:/[\w ]+?)? Migliorat[ao])\b", re.I)


def senza_note(testo: str) -> str:
    """Il testo senza le righe di marca, le errata e le note di fonte.

    🐛 Una marca che scrive «BAB +1 → **+0**» veniva letta come il BAB, e le
    errata del retriever («la prosa diceva BAB +10») pure. I numeri di una
    scheda si leggono solo dove la scheda li dichiara.
    """
    return "\n".join(r for r in testo.splitlines()
                     if not r.lstrip().startswith(("- ⚠", "fonte:", ">")))


def des_da_iniziativa(testo: str, gs: float = 30.0) -> "tuple[int, str] | None":
    """Strato 2-quater: iniziativa = mod Des (+4 con Iniziativa Migliorata).

    E' un'identita' esatta del SRD, e su 66 schede il campo c'e'. Si usa solo
    se la scheda elenca i suoi talenti: senza elenco, un +4 puo' essere il
    talento o la Destrezza, e scegliere sarebbe indovinare.
    """
    pulito = senza_note(testo)
    m = INIZIATIVA_SCRITTA.search(pulito)
    if not m or not re.search(r"\b(?:Talenti|Feats)\b", pulito, re.I):
        return None
    mod_des = int(m.group(1)) - (4 if INIZIATIVA_MIGLIORATA.search(pulito) else 0)
    if not -5 <= mod_des <= 3 + gs:
        return None
    return da_modificatore(mod_des), "ricavata dall'iniziativa"


def for_da_lotta(testo: str, gs: float = 30.0) -> "tuple[int, str] | None":
    """Strato 2-ter: la Forza **si ricava** da BAB e lotta dichiarati.

    lotta = BAB + mod For + taglia (SRD), quindi mod For = lotta − BAB − taglia,
    togliendo 4 se c'e' Lotta Migliorata. Non dipende dai DV, ne' dalla classe:
    solo da due numeri che il DM ha scritto.
    """
    pulito = senza_note(testo)
    b, l = BAB_SCRITTO.search(pulito), LOTTA_SCRITTA.search(pulito)
    if not (b and l):
        return None
    m = (int(next(g for g in l.groups() if g)) - int(b.group(1))
         - LOTTA_TAGLIA.get(taglia_di(testo), 0) - (4 if LOTTA_MIGLIORATA.search(testo) else 0))
    # la guardia di `plausibile` e' tarata sulla Cos ricavata da un `pf-dado`
    # parziale; qui i numeri sono due, scritti dal DM, e la fascia e' piu' larga
    if not (-5 <= m <= 3 + gs):
        return None
    return da_modificatore(m), "ricavata da BAB e lotta"


def iniziativa_ambigua(testo: str) -> "tuple[int, int] | None":
    """(mod Des con Iniziativa Migliorata, mod Des senza) se i talenti non sono elencati.

    `des_da_iniziativa` rifiuta, giustamente, di scegliere fra i due: senza
    elenco un +4 puo' essere il talento o la Destrezza. Ma un valore che non e'
    **nessuno dei due** e' sbagliato comunque, ed e' quel che l'array dava ai
    razorfiend verde e bianco (Des 17 con iniziativa +5).
    """
    pulito = senza_note(testo)
    m = INIZIATIVA_SCRITTA.search(pulito)
    if not m or re.search(r"\b(?:Talenti|Feats)\b", pulito, re.I):
        return None
    i = int(m.group(1))
    return i - 4, i


#: Quale caratteristica porta quale TS (SRD 3.5).
TS_CARATTERISTICA = (("Temp", "Cos"), ("Rifl", "Des"), ("Vol", "Sag"))
TS_SCRITTI = re.compile(r"^ts:\s*Temp\s*([+-]\d+),\s*Rifl\s*([+-]\d+),\s*Vol\s*([+-]\d+)", re.M)


def tetti_dai_ts(nome_file: str, testo: str) -> "dict[str, tuple[int, str]]":
    """Strato 2-quinquies: un TS scritto e' un **tetto** al modificatore.

    TS = base di classe e di tipo + mod della caratteristica + talenti, quindi
    mod ≤ TS scritto − base. E' un tetto e non un'identita': un oggetto, un
    bonus razziale o un incantesimo che la scheda non dichiara alzano il TS, e
    `conformita_statblocchi` per questo accetta un TS **sopra** l'atteso. Un
    TS **sotto** l'atteso, invece, dice che la caratteristica e' troppo alta.

    🔎 Nasce dagli otto scarti che `conformita_statblocchi` dava «del
    generatore» il 2026-09-23: il razorfiend blu aveva Des 17 dall'array e
    Riflessi +8, cioe' drago 10 DV (+7) e Des +1. Per questo e' il vincolo
    **piu' debole** della catena: abbassa solo un valore scelto dall'array,
    e davanti a un numero ricavato da pf, CA, iniziativa o lotta si annota.

    Non si usa dove la base non si sa (composizione ignota) o dove un'altra
    caratteristica entra nei TS (Grazia divina, Benedizione oscura: il Car).
    Restituisce {caratteristica: (modificatore massimo, nota)}.
    """
    import conformita_statblocchi as C       # qui: C importa questo modulo
    ts = TS_SCRITTI.search(testo)
    if not ts:
        return {}
    # 🐛 **Un TS derivato non e' un dato** (2026-09-23, trovato provando il
    # lotto D sui razorfiend). Se la riga `fonte:` dichiara che i `ts` li ha
    # scritti `derive_statblocks`, vengono da una matrice di caratteristiche
    # sua: usarli come tetto abbassava la Sag del razorfiend verde da 16 a 10
    # per far tornare un numero che nessuno ha scelto.
    fonte = re.search(r"^fonte:\s*derivati dalle tabelle:\s*([^(—\n]*)", testo, re.M)
    if fonte and re.search(r"\bts\b", fonte.group(1)):
        return {}
    m_tipo = re.search(r"^tipo:\s*(.+)$", testo, re.M) or \
        re.search(r"\*\*Size/Type\*\*:?\s*([^|\n]+)", testo)
    tipo = m_tipo.group(1).strip() if m_tipo else ""
    gruppi, nota = C.composizione(testo, tipo)
    if not (gruppi and nota):
        return {}
    if any(g.nome.lower() in ("paladin", "paladino", "pal", "blackguard") and g.n >= 2
           for g in gruppi):
        return {}
    s = C.Scheda(file=Path(nome_file), gs=0.0, tipo=tipo, attributi={}, provenienza="",
                 gruppi=gruppi, composizione_nota=True, testo=testo)
    minimi, _ = C.ts_attesi(s, {})       # caratteristiche assenti: mod 0
    fuori = {}
    for (nome, car), scritto, base in zip(TS_CARATTERISTICA, ts.groups(), minimi):
        fuori[car] = (int(scritto) - base,
                      f"ricavata da {nome} {int(scritto):+d} (base {base:+d})")
    return fuori


def profilo_di(ruolo: str) -> "tuple[str, ...]":
    basso = ruolo.lower()
    for chiave, ordine in PROFILI:
        if chiave in basso:
            return ordine
    return PROFILO_DI_RIPIEGO


#: SRD 3.5, *Improving Monsters*, «Changes to Statistics by Size», sommati a
#: partire da Media. Si applicano solo alle **creature**: un PNG con livelli
#: di classe ha gia' la taglia nella razza.
PER_TAGLIA = {
    8: (-10, 8, -2), 4: (-10, 6, -2), 2: (-8, 4, -2), 1: (-4, 2, -2), 0: (0, 0, 0),
    -1: (8, -2, 4), -2: (16, -4, 8), -4: (24, -4, 12), -8: (32, -4, 16),
}

#: SRD 3.5, modificatori razziali, per i PNG con livelli di classe. L'ordine
#: conta: `hobgoblin` prima di `goblin`, `duergar` prima di `nano`.
RAZZE = (
    ("hobgoblin",   {"Des": 2, "Cos": 2}),
    ("bugbear",     {"For": 4, "Des": 2, "Cos": 2, "Car": -2}),
    ("goblin",      {"For": -2, "Des": 2, "Car": -2}),
    ("half-orc",    {"For": 2, "Int": -2, "Car": -2}),
    ("mezzorc",     {"For": 2, "Int": -2, "Car": -2}),
    ("orc",         {"For": 4, "Int": -2, "Sag": -2, "Car": -2}),
    ("orco",        {"For": 4, "Int": -2, "Sag": -2, "Car": -2}),
    ("duergar",     {"Cos": 2, "Car": -4}),
    ("dwarf",       {"Cos": 2, "Car": -2}),
    ("nano",        {"Cos": 2, "Car": -2}),
    ("drow",        {"Des": 2, "Cos": -2, "Int": 2, "Car": 2}),
    ("elf",         {"Des": 2, "Cos": -2}),
    ("elfo",        {"Des": 2, "Cos": -2}),
    ("svirfneblin", {"For": -2, "Des": 2, "Sag": 2, "Car": -4}),
    ("gnome",       {"For": -2, "Cos": 2}),
    ("gnomo",       {"For": -2, "Cos": 2}),
    ("halfling",    {"For": -2, "Des": 2}),
    ("kobold",      {"For": -4, "Des": 2, "Cos": -2}),
    ("gnoll",       {"For": 4, "Cos": 2, "Int": -2, "Car": -2}),
    ("lizardfolk",  {"For": 2, "Cos": 2, "Int": -2}),
)


def razza_di(nome_file: str, tipo: str) -> "tuple[str, dict] | None":
    dove = (nome_file + " " + tipo).lower()
    for nome, mods in RAZZE:
        if re.search(rf"(?<![a-z]){re.escape(nome)}", dove):
            return nome, mods
    return None


def _dall_array(nome_file: str, ruolo: str, gs: float, testo: str, png: bool) -> "tuple[dict, list[str]]":
    """Strato 3: array del Manuale del DM per ruolo, piu' taglia, razza e caso."""
    note = []
    elite = any(k in ruolo.lower() for k in ELITE)
    # 🔴 **Due regimi, e la prima stesura ne aveva uno solo.** Gli array del
    # Manuale del DM sono tarati sui **PNG con livelli di classe**; applicati a
    # un mostro da GS 11 davano Forza 15, cioe' meno di un guerriero di 3°.
    # La distinzione la porta il campo `tipo`: se nomina una classe, e' un PNG.
    # 🐛 **La prima stesura cercava in tutto il file** e classificava come PNG
    # un gigante e una naga, perche' la loro prosa nomina «Barbaro 2» e
    # «Sorcerer 8» — varianti e note, non il loro tipo. Si guarda **solo** il
    # campo `tipo`, che e' quello che lo dichiara.
    array = list(ARRAY_ELITE if (elite or not png) else ARRAY_STANDARD)
    note.append(f"array {'elite' if (elite or not png) else 'standard'} del "
                f"Manuale del DM ({'PNG con classe' if png else 'creatura'})")
    priorita = list(profilo_di(ruolo))

    rng = random.Random(nome_file)     # 🔴 il seme e' il NOME, non l'orologio
    # il caso: ±1 a somma zero su due secondarie (mai la principale)
    valori = dict(zip(priorita, array))
    secondarie = priorita[2:]
    if len(secondarie) >= 2:
        su, giu = rng.sample(secondarie, 2)
        valori[su] += 1
        valori[giu] -= 1
        note.append(f"variazione a seme fisso: {su} +1, {giu} −1")

    # avanzamento: +1 ogni 4 DV (PHB). I DV totali ci sono nell'8% dei file,
    # quindi si usa il GS come surrogato — dichiarato, non nascosto.
    if png:
        # PHB: +1 a una caratteristica ogni 4 livelli.
        passo, dove = 4, priorita[:1]
        nota = f"un avanzamento ogni 4 livelli, contati sul GS {gs:g}"
    else:
        # Una creatura da GS alto non e' un PNG con molti livelli: nel Manuale
        # dei Mostri le sue caratteristiche crescono **con i DV**, e molto piu'
        # in fretta. Il passo e' tarato perche' a GS 11 la principale stia
        # intorno a 20-21, che e' la fascia del MM per quella sfida.
        passo, dove = 2, priorita[:3]
        nota = f"creatura: la principale sale ogni 2 GS, le due dopo ogni 4 (GS {gs:g})"
    for i, c in enumerate(dove):
        quanto = int(gs) // (passo if i == 0 else 4)
        if quanto:
            valori[c] += quanto
    if int(gs) >= passo:
        note.append(nota + " — surrogato dichiarato: i DV totali stanno nel campo "
                    "`tipo` solo nell'8% dei file")

    # SRD: la taglia per le creature, la razza per i PNG. La prima stesura non
    # aveva ne' l'una ne' l'altra, e `--taratura` l'ha fatto vedere: sulla
    # Forza sbagliava di quasi 4 punti, e il drago rosso usciva con For 17.
    m_tipo = re.search(r"^tipo:\s*(.+)$", testo, re.M)
    tipo = m_tipo.group(1) if m_tipo else ""
    r = razza_di(nome_file, tipo) if png else None
    if r:
        for c, d in r[1].items():
            valori[c] += d
        note.append(f"modificatori razziali SRD: {r[0]} "
                    + " ".join(f"{c} {d:+d}" for c, d in r[1].items()))
    else:
        # una creatura, o un PNG con livelli di classe ma di razza mostruosa
        # (minotauro, ogre): la taglia gli spetta comunque
        f, d, c = PER_TAGLIA.get(taglia_di(testo), (0, 0, 0))
        if (f, d, c) != (0, 0, 0):
            valori["For"] += f
            valori["Des"] += d
            valori["Cos"] += c
            note.append(f"taglia (SRD, Improving Monsters): For {f:+d}, Des {d:+d}, Cos {c:+d}")
    for k in valori:
        valori[k] = max(1, valori[k])
    return valori, note


def genera(nome_file: str, ruolo: str, gs: float, testo: str,
           usa_fonte: bool = True) -> "tuple[dict, list[str]]":
    """Le sei caratteristiche, con la nota di **come** ciascuna e' stata ottenuta.

    `usa_fonte=False` salta lo strato 0: serve a misurare quanto sbaglia lo
    strato 3 sui file dove la risposta vera c'e' (`--taratura`).
    """
    # 🔴 **Due regimi, e la prima stesura ne aveva uno solo.** Gli array del
    # Manuale del DM sono tarati sui **PNG con livelli di classe**; applicati a
    # un mostro da GS 11 davano Forza 15, cioe' meno di un guerriero di 3°.
    # La distinzione la porta il campo `tipo`: se nomina una classe, e' un PNG.
    # 🐛 **La prima stesura cercava in tutto il file** e classificava come PNG
    # un gigante e una naga, perche' la loro prosa nomina «Barbaro 2» e
    # «Sorcerer 8» — varianti e note, non il loro tipo. Si guarda **solo** il
    # campo `tipo`, che e' quello che lo dichiara.
    m_tipo = re.search(r"^tipo:\s*(.+)$", testo, re.M)
    tipo = m_tipo.group(1) if m_tipo else ""
    png = bool(CLASSE_NEL_TIPO.search(tipo))
    scheda = dalla_scheda(testo) if usa_fonte else None
    fonte = scheda or (dalla_fonte(nome_file, testo) if usa_fonte else None)
    if fonte:
        valori, come = fonte
        note = [come]
    else:
        valori, note = _dall_array(nome_file, ruolo, gs, testo, png)

    # il vincolo vince sempre, anche sulla fonte: la fonte e' l'origine, lo
    # statblocco e' quello che si gioca, e dove divergono la scheda e' stata
    # adattata. La divergenza si scrive, perche' e' un'informazione per il DM.
    nonmorto = bool(NON_MORTO.search(tipo))
    fonte_numeri = numeri_della_fonte(testo) if fonte and not scheda else {}
    lotta_scritta = LOTTA_SCRITTA.search(senza_note(testo))
    iniz_scritta = INIZIATIVA_SCRITTA.search(senza_note(testo))
    ricavate = set()
    for campo, trova in (("Des", des_vincolata), ("Des", des_da_iniziativa),
                         ("Cos", cos_da_pf), ("For", for_da_lotta)):
        if campo == "Cos" and nonmorto:
            continue
        vincolo = trova(testo, gs)
        if not vincolo:
            continue
        valore, come = vincolo
        prima = valori[campo]
        if (trova is des_da_iniziativa and fonte and not scheda and iniz_scritta
                and fonte_numeri.get("iniziativa") == int(iniz_scritta.group(1))):
            continue                  # stessa iniziativa della fonte: non adattata
        if (campo == "For" and fonte and not scheda and lotta_scritta
                and fonte_numeri.get("lotta") == int(next(g for g in lotta_scritta.groups() if g))):
            # lo statblocco ha la stessa lotta della fonte: non e' stato
            # adattato, e uno scarto di 1 e' della fonte (un oggetto, un
            # talento che PCGen conta). Si tiene la Forza della fonte.
            continue
        if fonte and isinstance(prima, int) and mod(prima) == mod(valore):
            continue                              # la fonte torna: si tiene la fonte
        if scheda:
            # i numeri scritti dal DM non si toccano: la divergenza si annota
            note.append(f"⚠ {campo} {valore} {come}, ma la scheda scrive {prima}: "
                        "si tiene la scheda, da verificare.")
            continue
        if fonte and campo == "Cos" and " su 1 DV" in come:
            # con un DV solo non si sa se il pf e' la media o il massimo del
            # dado (PCGen da' il massimo al 1° livello): il conto e' ambiguo
            note.append(f"⚠ i pf suggeriscono {campo} {valore}, la fonte dice {prima}: "
                        "con 1 DV il conto dipende da media o massimo, si tiene la fonte.")
            continue
        if fonte and come.startswith("derivata"):
            # la CA di contatto somma anche deviazione e schivata: e' un
            # indizio piu' debole di una fonte trascritta, e non la batte
            note.append(f"⚠ la CA di contatto suggerisce {campo} {valore}, la fonte "
                        f"dice {prima}: si tiene la fonte, la differenza può essere "
                        "deviazione o schivata, da verificare.")
            continue
        valori[campo] = valore
        if fonte:
            note.append(f"⚠ {campo} {valore} {come}: la fonte dice {prima}, "
                        "lo statblocco è stato adattato e vince lo statblocco")
        else:
            note.append(f"{campo} {valore} **{come}** — il vincolo batte l'array")
        ricavate.add(campo)

    # l'iniziativa senza elenco dei talenti: due candidati, l'array sceglie
    iniz = iniziativa_ambigua(testo)
    if iniz and not fonte and "Des" not in ricavate and isinstance(valori["Des"], int) \
            and mod(valori["Des"]) not in iniz:
        prima = valori["Des"]
        # il piu' vicino all'array; a pari distanza il piu' basso, cioe' il
        # talento: e' il piu' comune dei talenti dei mostri, e l'array non
        # gonfia una caratteristica per spiegare un numero
        scelto = min(iniz, key=lambda m: (abs(m - mod(prima)), m))
        valori["Des"] = da_modificatore(scelto) + (prima % 2)
        ricavate.add("Des")
        note.append(f"Des {valori['Des']} **ricavata dall'iniziativa {iniz[1]:+d}**, "
                    f"con Iniziativa Migliorata {'supposta' if scelto == iniz[0] else 'esclusa'}: "
                    "la scheda non elenca i talenti, e dei due valori possibili si tiene "
                    "il più vicino all'array")

    # il tetto dei TS: ultimo e piu' debole, tocca solo un valore dell'array
    for campo, (tetto, come) in tetti_dai_ts(nome_file, testo).items():
        prima = valori[campo]
        if not isinstance(prima, int) or mod(prima) <= tetto:
            continue
        if campo == "Cos" and nonmorto:
            continue
        if fonte or campo in ricavate or tetto < -5:
            note.append(f"⚠ {campo} al più {da_modificatore(tetto) + 1} {come}, "
                        f"ma {prima} viene da un dato più forte: si tiene, da verificare.")
            continue
        valori[campo] = da_modificatore(tetto) + (prima % 2)
        note.append(f"{campo} {valori[campo]} **{come}** — il tetto del TS batte l'array")

    # SRD 3.5, tipo non morto: **nessun punteggio di Costituzione**. I suoi pf
    # vengono da d12 senza modificatore, e un Cos 10 scritto accanto sarebbe
    # un errore di regole, non una scelta.
    if nonmorto and valori["Cos"] != "—" and not scheda:
        valori["Cos"] = "—"
        note.append("Cos — : non morto, nessun punteggio di Costituzione (SRD, tipo Undead)")
    # SRD 3.5, modelli scheletro e zombi: Int —, Sag 10, Car 1. Sono i soli due
    # casi in cui la regola scrive le mentali da se', e si applica quella.
    if not fonte and MODELLO_SENZA_MENTE.search(tipo + " " + nome_file):
        valori.update({"Int": "—", "Sag": 10, "Car": 1})
        note.append("Int —, Sag 10, Car 1: modello scheletro/zombi (SRD)")
    return valori, note


def riga_attributi(v: dict) -> str:
    return "attributi: " + " ".join(f"{k} {v[k]}" for k in ORDINE)


#: La riga che marca un blocco **scritto da questo script**. E' specifica: un
#: `[INFERRED` generico gia' presente nel file non basta, perche' parla
#: d'altro, e `--check` e `--rigenera` devono ritrovare esattamente i blocchi
#: suoi. La coda dice **da dove** vengono i numeri, file per file.
MARCA = "> [INFERRED — needs DM confirmation] `attributi` "
CODA_FONTE = ("trascritti dalla fonte citata in `Bestiario/pregen-pcgen/` da "
              "`scripts/genera_attributi.py`. Confermali o correggili.")
CODA_SCHEDA = ("copiati dalla riga delle caratteristiche di questa stessa scheda "
               "da `scripts/genera_attributi.py`.")
CODA_ARRAY = ("generati da `scripts/genera_attributi.py`: array del Manuale del DM "
              "con taglia e razza SRD, vincolati da CA e pf dove il file li "
              "dichiara. Confermali o correggili.")
RIGA_MARCA = re.compile("^" + re.escape(MARCA) + ".*$", re.M)


def statblocchi(rigenera: bool = False) -> "list[Path]":
    """I file da generare; con `rigenera`, anche quelli gia' generati da qui."""
    fuori = []
    for p in sorted(ROOT.glob("Bestiario/*/*-cr*.md")) + sorted(ROOT.glob("Bestiario/*/*/*-cr*.md")):
        t = p.read_text(encoding="utf-8", errors="replace")
        if "[POINTER" in t or "[RIMANDO]" in t:
            continue
        if not BLOCCO.search(t):
            continue
        if re.search(r"^attributi:", t, re.M) and not (rigenera and MARCA in t):
            continue
        fuori.append(p)
    return fuori


def proponi(rigenera: bool = False) -> "list[dict]":
    fuori = []
    for p in statblocchi(rigenera):
        t = p.read_text(encoding="utf-8", errors="replace")
        ruolo = re.search(r"\*\*Role\*\*:\s*([^\|\n]+)", t, re.I)
        gs = re.search(r"^gs:\s*([\d.,]+)", t, re.M)
        if not (ruolo and gs):
            continue
        v, note = genera(p.name, ruolo.group(1).strip(),
                         float(gs.group(1).replace(",", ".")), t)
        scritta = re.search(r"^attributi:.*$", t, re.M)
        fuori.append({"file": p, "ruolo": ruolo.group(1).strip(),
                      "attributi": v, "riga": riga_attributi(v), "note": note,
                      "marca": MARCA + (CODA_SCHEDA if note[0].startswith("letta dalla riga")
                                        else CODA_FONTE if note[0].startswith("trascritt")
                                        else CODA_ARRAY)
                               + "".join(" " + n for n in note if n.startswith("⚠")),
                      "scritta": scritta.group(0) if scritta else None})
    return fuori


def applica(prop: "list[dict]", rigenera: bool = False) -> int:
    """Scrive i blocchi. Idempotente: un secondo giro non cambia un byte.

    Senza `rigenera` salta i file che hanno gia' `attributi`; con `rigenera`
    riscrive **solo** quelli che portano la marca di questo script, mai un
    blocco scritto a mano.
    """
    scritti = 0
    for r in prop:
        t = r["file"].read_text(encoding="utf-8", errors="replace")
        if r["scritta"]:
            if not (rigenera and MARCA in t):
                continue
            nuovo_t = re.sub(r"^attributi:.*$", lambda _: r["riga"], t, count=1, flags=re.M)
            nuovo_t = RIGA_MARCA.sub(lambda _: r["marca"], nuovo_t, count=1)
            if nuovo_t != t:
                r["file"].write_text(nuovo_t, encoding="utf-8")
                scritti += 1
            continue
        m = BLOCCO.search(t)
        corpo = m.group(1)
        # dopo `ts:` se c'e', altrimenti in coda al blocco: e' il posto in cui
        # i 14 file che gia' l'hanno lo scrivono.
        if re.search(r"^ts:.*$", corpo, re.M):
            nuovo = re.sub(r"^(ts:.*)$", lambda x: x.group(1) + "\n" + r["riga"],
                           corpo, count=1, flags=re.M)
        else:
            nuovo = corpo.rstrip("\n") + "\n" + r["riga"] + "\n"
        t = t[:m.start(1)] + nuovo + t[m.end(1):]
        # la marca va subito sotto il blocco chiuso: sempre, e sempre li'
        fine = t.index("```", m.start(1) + len(nuovo)) + 3
        t = t[:fine] + "\n\n" + r["marca"] + t[fine:]
        r["file"].write_text(t, encoding="utf-8")
        scritti += 1
    print(f"✓ scritti {scritti} blocchi `attributi`, tutti marcati [INFERRED]")
    return 0


VALORE = re.compile(r"(For|Des|Cos|Int|Sag|Car) (\d+|—)")


def controlla() -> "list[str]":
    """Tre promesse, e il cancello le verifica tutte e tre sui file veri."""
    problemi = []
    for r in proponi(rigenera=True):
        nome = r["file"].name
        if r["scritta"] and r["scritta"] != r["riga"]:
            problemi.append(f"{nome}: scritto «{r['scritta']}», la regola da' «{r['riga']}»")
        if r["scritta"] and r["marca"] not in r["file"].read_text(encoding="utf-8"):
            problemi.append(f"{nome}: la marca non dice piu' da dove vengono i numeri")
        for c, v in VALORE.findall(r["riga"]):
            if v != "—" and not 1 <= int(v) <= 45:
                problemi.append(f"{nome}: {c} {v} fuori da 1–45")
    for p in ROOT.glob("Bestiario/**/*-cr*.md"):
        t = p.read_text(encoding="utf-8", errors="replace")
        if len(RIGA_MARCA.findall(t)) > 1 or len(re.findall(r"^attributi:", t, re.M)) > 1:
            problemi.append(f"{p.name}: blocco o marca duplicati — la scrittura non e' idempotente")
    return problemi


def taratura(insieme: str = "fonti") -> dict:
    """Quanto sbaglia lo strato 3 dove la risposta vera c'e'.

    Si genera **come se la risposta non ci fosse** e si confronta. Due banchi:

    * ``fonti`` — le 39 sestine trascritte da `pregen-pcgen/`. **In-campione**:
      e' su questi file che si e' visto che taglia e razza servivano;
    * ``schede`` — le 27 sestine che le schede scrivono nella loro prosa,
      trovate **dopo** aver fissato le regole. **Fuori campione**: e' il
      numero che dice quanto il generatore vale su un file che non ha visto.
    """
    coppie = []
    for r in proponi(rigenera=True):
        t = r["file"].read_text(encoding="utf-8", errors="replace")
        vera = dalla_scheda(t) if insieme == "schede" else (
            None if dalla_scheda(t) else dalla_fonte(r["file"].name, t))
        if not vera:
            continue
        gs = float(re.search(r"^gs:\s*([\d.,]+)", t, re.M).group(1).replace(",", "."))
        gen, _ = genera(r["file"].name, r["ruolo"], gs, t, usa_fonte=False)
        coppie.append((r["file"].name, vera[0], gen))
    per_car, tutti, mods = {}, [], []
    for _, v, g in coppie:
        for c in ORDINE:
            if isinstance(v[c], int) and isinstance(g[c], int):
                e = abs(v[c] - g[c])
                per_car.setdefault(c, []).append(e)
                tutti.append(e)
                mods.append(abs(mod(v[c]) - mod(g[c])))
    media = lambda xs: round(sum(xs) / len(xs), 2) if xs else 0.0  # noqa: E731
    return {"insieme": insieme, "file": len(coppie), "mae": media(tutti), "mae_mod": media(mods),
            "entro_1_mod": round(sum(e <= 1 for e in mods) / len(mods), 2) if mods else 0.0,
            "per_caratteristica": {c: media(per_car.get(c, [])) for c in ORDINE},
            "coppie": coppie}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--scrivi", action="store_true", help="applica ai file")
    ap.add_argument("--rigenera", action="store_true",
                    help="riscrive i soli blocchi marcati da questo script")
    ap.add_argument("--check", action="store_true",
                    help="esce 1 se un blocco generato non e' riproducibile")
    ap.add_argument("--taratura", action="store_true",
                    help="errore dello strato 3 contro le fonti trascrivibili")
    args = ap.parse_args(argv)
    if args.taratura:
        for insieme, etichetta in (("fonti", "fonti citate, IN-CAMPIONE"),
                                   ("schede", "sestine scritte nelle schede, FUORI CAMPIONE")):
            m = taratura(insieme)
            print(f"TARATURA dello strato 3 su {m['file']} file — {etichetta}")
            print(f"  errore medio: {m['mae']} sul punteggio, {m['mae_mod']} sul modificatore; "
                  f"entro ±1 di modificatore: {m['entro_1_mod']:.0%}")
            print("  per caratteristica: " + "  ".join(
                f"{c} {e}" for c, e in m["per_caratteristica"].items()))
        return 0
    if args.check:
        problemi = controlla()
        for x in problemi:
            print(f"✗ {x}")
        if problemi:
            return 1
        gen = sum(1 for r in proponi(rigenera=True) if r["scritta"])
        print(f"✓ genera_attributi: {gen} blocchi generati, tutti riproducibili "
              f"e nei limiti; {len(proponi())} ancora da generare")
        return 0
    if args.rigenera:
        return applica(proponi(rigenera=True), rigenera=True)
    prop = proponi()
    if args.scrivi:
        return applica(prop)
    print(f"\nPROPOSTA — {len(prop)} statblocchi senza `attributi`\n" + "=" * 70)
    for r in prop[:12]:
        print(f"\n  {r['file'].name}  [{r['ruolo']}]")
        print(f"    {r['riga']}")
        for n in r["note"]:
            print(f"      · {n}")
    if len(prop) > 12:
        print(f"\n  … e altri {len(prop) - 12}. `--scrivi` li applica.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
