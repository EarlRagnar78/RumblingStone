"""incantesimi.py — quali incantesimi sceglie un PNG generato, e da quale lista.

Il lotto I del piano `PIANO-GENERATORE-CREATURE-E-PNG.md`, e nasce da un difetto
vero: il generatore sceglieva per **ruolo tattico** e non per **lista di classe**.
A un druido costruito come «controllore» dava *armatura magica*, *sonno* e *dito
della morte* — incantesimi da mago — e come «bruto» *benedizione*, *santuario* e
*scudo della fede*, che sono da chierico. Due schede del Bestiario ci sono
passate e sono dovute essere ripulite a mano.

## Perché separare arcano e divino non bastava

È il primo istinto, ed è quello sbagliato. Chierico e druido sono tutti e due
divini e hanno **liste diverse**: *benedizione* e *scudo della fede* non sono mai
state sulla lista del druido. Il bardo è «ibrido» e ha una lista sua che non
coincide con nessuna delle altre due. La tradizione serve a raggruppare per chi
legge; **la chiave è la lista di classe.**

## I due assi, che sono davvero due

    ruolo tattico     bruto · schermagliatore · tiratore · comandante ·
                      controllore · blaster        (come combatte)

    funzione          controllore · blaster · supporto · utilità
                      (che cosa fa con gli incantesimi)

Non sono la stessa cosa e confonderli era metà del difetto. Un bruto con livelli
da chierico esiste, ed è un chierico da guerra che si potenzia e picchia: ruolo
«bruto», funzione «supporto». `FUNZIONE_DA_RUOLO` dà la corrispondenza di norma,
e `--funzione` la scavalca quando il DM vuole altro.

## Ventuno celle, diciotto liste, e non è pigrizia

La matrice approvata dal DM è di 21 celle. Le liste scritte sono 18, perché
**mago e stregone hanno la stessa lista di incantesimi** — è una regola del SRD,
non una scorciatoia. Tenerne due copie non le renderebbe più giuste: le farebbe
divergere.

## Come si sa che non c'è dentro una bugia

Ogni incantesimo qui dentro deve comparire nell'ancora scritta in
`skills/dnd-35-srd/references/spells.md` §«Liste di classe», per **quella**
classe e **quel** livello. Il test `test_incantesimi.py` verifica l'inclusione
riga per riga. La divisione del lavoro è quella che rende il controllo utile
invece che circolare: la skill dice *cosa quella classe può lanciare* (un fatto
di regole), questo file dice *cosa un controllore sceglie davvero* (una scelta di
progetto). Un test che confrontasse questo file con una costante qui accanto non
troverebbe niente.

Solo stdlib.
"""
from __future__ import annotations

import random

#: Le quattro funzioni da incantatore, con le parole del DM.
#:
#:   controllore  toglie ai PG le opzioni: terreno, movimento, azioni
#:   blaster      danno, spesso d'area
#:   supporto     tiene in piedi i suoi; il suo valore è nei pf che *non*
#:                perdono gli altri
#:   utilità      informazione, mobilità, contromagia, difese
FUNZIONI = ("controllore", "blaster", "supporto", "utilita")

#: Il ruolo tattico dice come combatte; la funzione dice cosa fa con gli
#: incantesimi. Questa è la corrispondenza di norma, e `--funzione` la scavalca.
#: Sostituisce il vecchio `LISTA_DI_RIPIEGO`, che mandava i ruoli non
#: incantatori a pescare dalla lista di un *altro ruolo* — cioè spesso di
#: un'altra classe, che era il difetto.
FUNZIONE_DA_RUOLO = {
    "controllore": "controllore",
    "blaster": "blaster",
    "tiratore": "blaster",
    "comandante": "supporto",
    "bruto": "supporto",
    "schermagliatore": "utilita",
}

#: I nomi di classe come li scrive il DM → la chiave delle liste. `T.CLASSI`
#: accetta italiano e inglese; qui la forma canonica è una sola, o si finisce con
#: «wizard» che non trova la lista di «mago».
from functools import cache as _cache  # noqa: E402

from . import sistemi as _S  # noqa: E402

#: Le liste 3.5 stanno nel plugin (ADR-0111, L5c): `sistemi/dnd35/dati/incantesimi.toml`.
#: Si leggono alla prima richiesta, non all'import (F2 di ADR-0112): `liste(id)`
#: dà il contesto esplicito, e i nomi di sempre (`CANONICA`, `LISTE`,
#: `FUNZIONE_DI_RIPIEGO`, `SENZA_LISTA`, `PF1E_SOLO`) restano per chi li importa.
_NOMI_LISTE = ("CANONICA", "LISTE", "FUNZIONE_DI_RIPIEGO", "SENZA_LISTA")


def liste(id_: str = "dnd35") -> dict:
    """Le liste di classe × funzione del sistema `id_` (capacità `creature.incantesimi`)."""
    return _liste(id_)


@_cache
def _liste(id_: str) -> dict:
    _DATI = _S.regole(id_).dati("creature.incantesimi")
    CANONICA = dict(_DATI["canonica"])

    # ===========================================================================
    # Le liste, per lista di classe × funzione
    # ===========================================================================
    # Ogni voce è presa dall'ancora in `dnd-35-srd/references/spells.md`, per quella
    # classe e quel livello. Poche voci per livello, ed è voluto: sono gli
    # incantesimi che quella funzione lancerebbe davvero, non tutto il SRD.

    #: classe → funzione → livello → incantesimi. Mago e stregone puntano allo
    #: **stesso oggetto** (`[regole] alias` nei dati), e deve restare così: nel SRD
    #: hanno la stessa lista, e due copie divergerebbero al primo ritocco.
    LISTE: dict[str, dict[str, dict[int, list[str]]]] = {
        classe: {f: {int(liv): list(v) for liv, v in per.items()} for f, per in ff.items()}
        for classe, ff in _DATI["liste"].items()}
    for _alias, _di in _DATI["regole"]["alias"].items():
        LISTE[_alias] = LISTE[_di]
    #: L'ordine delle classi resta quello di prima (mago, stregone, chierico, …).
    LISTE = {c: LISTE[c] for c in ["mago", "stregone"] + [c for c in LISTE if c not in ("mago", "stregone")]}

    #: Quando la cella (classe × funzione) non esiste, si ripiega su un'altra
    #: funzione **della stessa classe** — mai sulla lista di un'altra classe, che è
    #: esattamente il difetto da cui nasce questo file. Un mago «supporto» non c'è
    #: nel gioco; diventa un mago «utilità», e il conto lo dice.
    FUNZIONE_DI_RIPIEGO = dict(_DATI["ripiego"])

    #: Le classi incantatrici per cui una lista **non** è stata scritta. Per queste
    #: il generatore preferisce non scegliere invece di scegliere male: un blocco
    #: senza incantesimi si riempie in due minuti, un adepto con la lista del mago
    #: arriva al tavolo e ci resta.
    #: ⚠️ L'adepto è fuori dalla matrice approvata dal DM (le 21 celle sono le sei
    #: classi con lista piena). È l'unico residuo dichiarato del lotto I.
    SENZA_LISTA = frozenset(_DATI["regole"]["senza_lista"])
    return {"CANONICA": CANONICA, "LISTE": LISTE, "FUNZIONE_DI_RIPIEGO": FUNZIONE_DI_RIPIEGO,
            "SENZA_LISTA": SENZA_LISTA}

# ===========================================================================
# La variante PF1e — la richiesta del DM, tarata su cosa PF1e dà davvero
# ===========================================================================
# Richiesta: *«per la versione più potente mantenendo il GS si possano usare gli
# incantesimi di Pathfinder 1e se più potenti»*. Il meccanismo c'è; il perimetro
# è più stretto della richiesta, e la ragione va scritta qui perché è la parte
# che sorprende.
#
# **Sugli incantesimi condivisi PF1e non è più forte: è pari o più debole.** Lo
# dice la tabella di compatibilità in `pathfinder-1e-srd/references/conversion-
# guide.md`: *grasso*, *polvere scintillante* e i *tentacoli neri* sono stati
# indeboliti via CMB e tiri salvezza; la linea del «salva o muori» (*dito della
# morte* e parenti) è stata convertita in danno; la linea del polimorfismo è
# riscritta, e la regola del repo è di lanciarla dal testo 3.5. Scambiare *palla
# di fuoco* con la *palla di fuoco* PF1e non compra niente: è lo stesso
# incantesimo.
#
# Quello che rende davvero più duro un incantatore PF1e a pari GS è, in ordine:
#   1. gli incantesimi che in 3.5 **non esistono** — la tabella qui sotto;
#   2. il +4 alle caratteristiche mentali del template Advanced, che alza ogni
#      CD di 2. È l'effetto più grosso, e `--piu-cattivi` lo applica già;
#   3. le liste di evocazione PF1e, che offrono creature migliori per livello.
#
#: classe → livello → [(nome italiano, nome PRD)]. **55 righe.**
#:
#: L'ancora sta in `pathfinder-1e-srd/references/conversion-guide.md` §«PF1e
#: spell lists»: sono le liste dell'**Advanced Player's Guide**, cioè gli
#: incantesimi che PF1e *aggiunge*. La lista core di Pathfinder, nome per nome,
#: è abbastanza vicina al SRD 3.5 che scambiarla non compra niente — la parte
#: che un incantatore PF1e ha in più è questa, ed è quella che vale tenere.
#: `test_incantesimi.py` verifica ogni riga contro quella sezione, con la stessa
#: disciplina delle liste 3.5.
#:
#: ⚠️ **Il controllo contro la pagina ha trovato tre errori**, e sono lo stesso
#: genere di difetto per cui esiste tutto questo file:
#:
#:   * *ill omen* stava sulla lista di mago al 1°. Non è un incantesimo da mago:
#:     è da **strega**, psichico e mesmerista. Tolto.
#:   * *stone call* stava al 3° per il mago. È **sorcerer/wizard 2**. Spostato.
#:   * *hungry pit* risultava introvabile a una prima estrazione automatica —
#:     ma c'è, al 5° da mago. Il nome porta il pedice del componente focus
#:     (`Hungry Pit<sup>F</sup>`) e il parser lo incollava al nome. Un'assenza
#:     silenziosa dentro un'ancora è peggio di un'ancora mancante, perché il
#:     test passa lo stesso.
#:
#: ⚠️ **Il chierico resta scoperto al 1°, 6° e 7°**, e non è una dimenticanza:
#: a quei livelli l'APG non aggiunge niente che cambi un incontro (al 1° *ant
#: haul* e *dancing lantern*, al 6° la sola *planar adaptation, mass*, al 7°
#: nulla). Meglio un buco dichiarato che una riga messa per far quadrare la
#: tabella.
#:
#: Il commento accanto a ogni riga è la descrizione **della pagina**, non una
#: parafrasi: la scelta di quali importare è mia e va confermata, ma cosa fanno
#: non è affidato alla memoria di nessuno.
#: Stanno nel plugin pf1e (ADR-0111, L5c): `[solo]` di
#: `sistemi/pf1e/dati/incantesimi.toml`; lo stregone è un alias del mago.
def solo_pf1e(id_: str = "pf1e") -> "dict[str, dict[int, list[tuple[str, str]]]]":
    """Gli incantesimi PF1e senza equivalente 3.5 (`[solo]` dei dati di `id_`)."""
    return _solo_pf1e(id_)


@_cache
def _solo_pf1e(id_: str) -> "dict[str, dict[int, list[tuple[str, str]]]]":
    _SOLO = _S.regole(id_).dati("creature.incantesimi")
    PF1E_SOLO: dict[str, dict[int, list[tuple[str, str]]]] = {
        classe: {int(liv): [tuple(v) for v in voci] for liv, voci in per.items()}
        for classe, per in _SOLO["solo"].items()}
    for _alias, _di in _SOLO["solo_alias"].items():
        PF1E_SOLO[_alias] = PF1E_SOLO[_di]
    return PF1E_SOLO


def _livelli_pf1e(classe: str, lista: "dict[int, list[str]]", livello: int) -> "list[str]":
    """Le voci della cella 3.5 al livello PF1e: tolte quelle che il PRD sposta o non ha.

    `[livello_pf1e]` dei dati pf1e (lotto 2 delle regole complete): *metamorfosi*
    è 4° per il mago 3.5 e 5° in PF1e; *cura ferite minori* in PF1e non c'è.
    """
    d = _S.regole("pf1e").dati("creature.incantesimi").get("livello_pf1e", {})
    sposta = d.get(liste()["CANONICA"].get(classe, classe), d.get("mago", {}) if classe == "stregone" else {})
    fuori = [v for v in lista.get(livello, []) if v not in sposta]
    dentro = [v for lv, voci in lista.items() for v in voci if sposta.get(v) == livello and v not in fuori]
    return fuori + dentro


def __getattr__(nome: str):
    if nome in _NOMI_LISTE:
        return liste()[nome]
    if nome == "PF1E_SOLO":
        return solo_pf1e()
    raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")


# ===========================================================================
# La scelta
# ===========================================================================

def funzione_di(ruolo: str, funzione: str | None = None) -> str:
    """La funzione da incantatore: quella chiesta, o quella di norma del ruolo."""
    if funzione:
        if funzione not in FUNZIONI:
            raise ValueError(f"funzione ignota: {funzione}. Note: {', '.join(FUNZIONI)}")
        return funzione
    return FUNZIONE_DA_RUOLO.get(ruolo, "supporto")


def cella(classe: str, funzione: str) -> tuple[dict[int, list[str]], str]:
    """La lista per (classe × funzione), e la funzione **davvero** usata.

    Il secondo valore non è una formalità: quando la cella chiesta non esiste nel
    gioco — un mago «supporto», un bardo «blaster» — si ripiega su un'altra
    funzione della stessa classe, e chi chiama deve poterlo scrivere nel conto
    invece di far sparire la differenza.
    """
    per_classe = liste()["LISTE"][liste()["CANONICA"].get(classe.lower(), classe.lower())]
    if funzione in per_classe:
        return per_classe[funzione], funzione
    ripiego = liste()["FUNZIONE_DI_RIPIEGO"][liste()["CANONICA"].get(classe.lower(), classe.lower())]
    return per_classe[ripiego], ripiego


def scegli(classe: str, funzione: str, slot: tuple[int, ...],
           rng: random.Random, pf1e: bool = False) -> tuple[list[str], list[str]]:
    """Un incantesimo per slot, dalla lista di quella classe e di quel livello.

    Torna (le righe da stampare, le note sui rincari PF1e). Gli incantesimi di
    livello 0 non si scelgono: sono a volontà e non descrivono la creatura.
    """
    canonica = liste()["CANONICA"].get(classe.lower(), classe.lower())
    if canonica in liste()["SENZA_LISTA"]:
        return [], []
    lista, _ = cella(canonica, funzione)
    righe, note = [], []
    for livello, quanti in enumerate(slot):
        if not quanti or livello == 0 or livello not in lista:
            continue
        voci = lista[livello]
        if pf1e:
            voci = _livelli_pf1e(canonica, lista, livello)
            if not voci:
                continue
        scelti = rng.sample(voci, min(quanti, len(voci)))
        if pf1e:
            aggiunte = solo_pf1e().get(canonica, {}).get(livello)
            if aggiunte:
                it, prd = rng.choice(aggiunte)
                # Uno solo per livello, e **sostituisce** invece di aggiungere:
                # il numero di slot è quello della tabella SRD e non si tocca.
                scelti[-1] = f"{it} (PF1e: {prd})"
                note.append(f"{livello}°: {it} ({prd}) — PF1e, senza equivalente 3.5")
        righe.append(f"{livello}°: " + ", ".join(sorted(scelti)))
    return righe, note
