"""tabelle.py — le tabelle da cui si costruisce una creatura, con la provenienza.

Sono le stesse tabelle che il DM userebbe sfogliando il manuale. Stavano sparse
fra `derive_statblocks.py` (che le usa per **leggere** una scheda) e le skill
(che le usano per **rispondere a una domanda**); qui stanno una volta sola,
perché il generatore le usa per **scrivere**, ed è l'uso che perdona meno.

La regola del repo vale riga per riga: **nessuna riga inventata in silenzio.**
Ogni tabella dichiara la sua fonte in `PROVENIENZA`, e dove una riga non è
verificata contro un'ancora presente nel repo lo dice `VERIFICATE`. Una riga non
verificata non viene nascosta e non viene tolta: viene **marcata**, e chi la usa
se ne accorge. È la lezione del lotto H — un numero dedotto in silenzio è peggio
di un numero mancante, perché ha l'aria di un conto.

## La gerarchia delle fonti, che è una scelta del DM

    SRD 3.5   →  la norma. Da qui si COSTRUISCE.
    PF1e OGL  →  solo dove il SRD non ha un equivalente, e per una cosa sola:
                 i bersagli per GS, che nel SRD **non esistono**.

E c'è un motivo per cui la seconda non sostituisce la prima: **a parità di GS,
PF1e è più duro del 3.5.** Un mostro costruito sui numeri PF1e e venduto come
«GS 9» al tavolo di questa campagna è più cattivo di quanto il GS prometta. Che
è esattamente perché il DM ha chiesto quei numeri come *variante*: quando servono
più cattivi, si chiedono — non arrivano di straforo.

Solo stdlib.
"""
from __future__ import annotations

import re
from pathlib import Path

PROVENIENZA = {
    "TIPI": "SRD 3.5, «Table: Creature Improvement by Type»",
    "CLASSI": "SRD 3.5, tabelle delle classi (comprese le classi PNG)",
    "TAGLIE": "SRD 3.5, «Table: Creature Size and Scale» + armatura naturale",
    "ARMATURE": "SRD 3.5, «Table: Armor and Shields»",
    "ELITE": "SRD 3.5, matrice elite; PF1e la chiama «heroic» e sono gli stessi numeri",
    "BASIC": "SRD 3.5, matrice standard; PF1e la chiama «basic»",
    "INCANTESIMI": "SRD 3.5, tabelle delle classi incantatrici",
    "CONOSCIUTI": "SRD 3.5, «Table: Sorcerer Spells Known» e «Table: Bard "
                   "Spells Known»",
    "LISTE_INCANTESIMI": "SRD 3.5, le liste di classe — l'ancora in repo è "
                         "`dnd-35-srd/references/spells.md` §Liste di classe",
    "PF1E_SOLO": "PF1e PRD/OGL, incantesimi senza un equivalente 3.5 — l'ancora "
                 "è `pathfinder-1e-srd/references/conversion-guide.md`",
    "PER_GS": "PF1e Bestiary Table 1–1, letta da scripts/pf1e-statistiche-per-gs.yaml "
              "— il SRD 3.5 non ha un equivalente",
    "PASSI_GS": "PF1e Bestiary, appendice «Monster Advancement»",
    "EQUIPAGGIAMENTO": "PF1e, colonna «heroic NPC» — il SRD 3.5 dà la ricchezza "
                       "per livello del PG, non quella del PNG",
}

# ===========================================================================
# SRD 3.5 — le creature
# ===========================================================================

#: Le tabelle base 3.5 stanno nel plugin (ADR-0111, L5a):
#: `sistemi/dnd35/dati/creature.toml`, capacità `creature.costruzione`. Si
#: caricano alla prima richiesta (`di`) e si espongono con i nomi e le forme di sempre.
from functools import cache as _cache  # noqa: E402

from . import formule as _formule  # noqa: E402
from . import sistemi as _S  # noqa: E402

#: Chi merita la matrice elite: chi ha un nome, chi comanda, chi è un boss. Il
#: fondale prende quella standard, ed è il punto — un mook con le caratteristiche
#: di un luogotenente non è un mook, è un secondo luogotenente.
RUOLI_ELITE = ("boss", "elite", "villain", "commander", "captain", "lieutenant",
               "alfa", "leader", "mastermind", "officer", "ally", "caster")


def _griglia(testo: str) -> dict[int, tuple[int, ...]]:
    fuori = {}
    for riga in testo.strip().splitlines():
        liv, _, slot = riga.partition(":")
        fuori[int(liv)] = tuple(int(n) for n in slot.split())
    return fuori


_NOMI = (
    "_DATI", "TIPI", "ALIAS_TIPO", "CLASSI", "CLASSI_PNG", "BAB_CLASSE", "TAGLIE",
    "ARMATURE", "SCUDI", "ELITE", "BASIC", "_GRIGLIE", "MAGO", "STREGONE",
    "STREGONE_CONOSCIUTI", "CHIERICO", "DRUIDO", "ADEPTO", "BARDO", "BARDO_CONOSCIUTI",
    "RANGER", "PALADINO", "LIVELLO_INCANTATORE_RIDOTTO", "INCANTATORI",
    "INCANTATORI_SENZA_ANCORA", "INCANTATORI_ZERO_A_VOLONTA",
    "INCANTATORI_GRIGLIA_PF1E",
)


def di(id_: str = "dnd35") -> dict:
    """Le tabelle di costruzione del sistema `id_` (capacità `creature.costruzione`).

    Si leggono alla prima richiesta, non all'import (F2 di ADR-0112): chi
    vuole un sistema preciso chiama `di(id)`, e i nomi di sempre (`T.TIPI`,
    `T.MAGO`, …) restano e danno quelli del 3.5."""
    return _di(id_)


@_cache
def _di(id_: str) -> dict:
    _DATI = _S.regole(id_).dati("creature.costruzione")

    #: tipo → (faccia del dado dei DV, BAB per DV, tiri salvezza buoni)
    TIPI = {k: (v["dv"], v["bab"], tuple(v["ts_buoni"])) for k, v in _DATI["tipi"].items()}

    #: Come il tipo si scrive nelle schede — italiano, inglese, e le forme miste.
    ALIAS_TIPO = dict(_DATI["alias_tipo"])

    #: classe → (faccia del dado dei DV, tiri salvezza buoni). Le classi PNG del SRD
    #: (warrior, adept, expert, aristocrat, commoner) stanno qui come le altre: sono
    #: SRD a tutti gli effetti, ed è con quelle che si fa il fondale.
    CLASSI = {k: (v["dv"], tuple(v["ts_buoni"])) for k, v in _DATI["classi"].items()}

    #: Le classi PNG del SRD. Contano meno per il GS, ed è il loro scopo.
    CLASSI_PNG = frozenset(k for k, v in _DATI["classi"].items() if v.get("png"))

    #: BAB per livello di classe.
    BAB_CLASSE = {k: v["bab"] for k, v in _DATI["classi"].items()}

    #: taglia → (armatura naturale tipica, modificatore di CA e attacco)
    TAGLIE = {k: (v["armatura_naturale"], v["ca_attacco"]) for k, v in _DATI["taglie"].items()}

    #: armatura → (bonus di CA, massimo di Destrezza)
    ARMATURE = {k: (v["ca"], v["des_max"]) for k, v in _DATI["armature"].items()}
    SCUDI = dict(_DATI["scudi"])

    #: Le due matrici. Identiche fra SRD 3.5 e PF1e — una sola per tutti e due.
    ELITE = tuple(_DATI["matrici"]["elite"])
    BASIC = tuple(_DATI["matrici"]["standard"])



    # ===========================================================================
    # SRD 3.5 — gli incantatori
    # ===========================================================================
    # Il DM ha ragione: le tabelle per GS esistono anche per gli incantatori. Ma la
    # cosa da cui si costruisce **non** è quella: è la tabella della classe, che dà
    # gli incantesimi al giorno per livello. La riga per GS serve dopo, a controllare
    # che la CD primaria sia dove dovrebbe.
    #
    # Griglia: livello di classe → slot per livello d'incantesimo, da 0 a 9.
    # Gli slot di dominio del chierico NON sono contati: sono +1 per livello, e vanno
    # aggiunti quando il dominio è scelto — che è una decisione, non un conto.



    #: Le griglie stanno nel plugin (ADR-0111, L5b): `[griglie]` di
    #: `sistemi/dnd35/dati/creature.toml`, con le stesse fonti e ancore di prima:
    #: «Table: The Wizard», «The Sorcerer», «Sorcerer Spells Known», «The Cleric»
    #: (= «The Druid»), «The Adept», «The Bard», «Bard Spells Known», «The Ranger»
    #: (= «The Paladin»). Ancore verificate in repo ai livelli 1, 5, 10, 15, 20
    #: (`dnd-35-srd/references/classes.md`), tranne l'adepto.
    #:
    #: Per il chierico va aggiunto **+1 slot per livello** quando i domini sono
    #: scelti. Ranger e paladino non hanno incantesimi di livello 0: la prima cifra
    #: di ogni riga è lo **0 finto** che tiene l'indice allineato con le altre
    #: griglie, e sotto il 4° livello di classe la riga è di soli zeri invece che
    #: assente, così nessun chiamante deve gestire un'assenza.
    _GRIGLIE = {nome: {int(liv): tuple(slot) for liv, slot in righe.items()}
                for nome, righe in _DATI["griglie"].items()}
    MAGO = _GRIGLIE["mago"]
    STREGONE = _GRIGLIE["stregone"]
    #: Uno stregone non prepara: la lista è la creatura.
    STREGONE_CONOSCIUTI = _GRIGLIE["stregone_conosciuti"]
    CHIERICO = _GRIGLIE["chierico"]
    DRUIDO = CHIERICO
    #: L'adepto arriva al 5° livello d'incantesimo e non ha un'ancora in repo come
    #: le altre: è dichiarato in `INCANTATORI_SENZA_ANCORA`.
    ADEPTO = _GRIGLIE["adepto"]
    #: ⚠️ Il bardo serve davvero: `Bestiario/png/lomyn-redtongue-bardo8-cr8.md`.
    BARDO = _GRIGLIE["bardo"]
    BARDO_CONOSCIUTI = _GRIGLIE["bardo_conosciuti"]
    RANGER = _GRIGLIE["ranger"]
    PALADINO = RANGER

    #: Le classi il cui livello dell'incantatore **non** coincide col livello di
    #: classe. Nel SRD sono ranger e paladino: `livello − 3`, con un minimo di 1 e
    #: un massimo di 4° livello d'incantesimo.
    LIVELLO_INCANTATORE_RIDOTTO = frozenset(_DATI["incantatori_regole"]["livello_ridotto"])

    #: classe incantatrice → (griglia, caratteristica primaria, spontaneo?)
    #: ⚠️ Ranger e paladino lanciano su **Saggezza**, non su Carisma (quella è la
    #: regola di PF1e): nel SRD 3.5 la CD del paladino è 10 + livello +
    #: modificatore di Saggezza. Il valore sta nei dati e il test delle impronte
    #: (`test_sistemi_creature.py`) dice se cambia.
    INCANTATORI = {c: (_GRIGLIE[v["griglia"]], v["caratteristica"], v["spontaneo"])
                   for c, v in _DATI["incantatori"].items()}

    #: Le griglie che NON hanno una riga d'ancora nel repo. Usarle è lecito; farlo
    #: senza dirlo no.
    INCANTATORI_SENZA_ANCORA = frozenset(_DATI["incantatori_regole"]["senza_ancora"])

    #: Chi lancia i trucchetti a volontà (il bardo con la tabella PF1e, card del
    #: DM del 2026-11-09): la griglia porta uno 0 finto in prima posizione.
    INCANTATORI_ZERO_A_VOLONTA = frozenset(_DATI["incantatori_regole"].get("zero_a_volonta", ()))

    #: Le classi la cui griglia viene dal PRD PF1e e non dall'SRD 3.5 (stessa card).
    INCANTATORI_GRIGLIA_PF1E = frozenset(_DATI["incantatori_regole"].get("griglia_pf1e", ()))
    luogo = locals()
    return {n: luogo[n] for n in _NOMI}


def __getattr__(nome: str):
    if nome in _NOMI:
        return di()[nome]
    raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")


#: Il livello dell'incantatore per una classe e un livello di classe. Per quasi
#: tutti è lo stesso numero; per ranger e paladino è `livello − 3`, e chiamare
#: questa funzione invece di usare il livello di classe è ciò che evita di
#: stampare «incantatore di livello 12» per un paladino che lancia da 9°.
#: ⚠️ `livello − 3` è la regola PF1e: nell'SRD 3.5 è metà del livello di classe
#: dal 4°. La divergenza è scritta in `sistemi/d20/dati/formule.toml` e la
#: decide il DM; F3 ha spostato la formula senza cambiare le uscite.
def livello_incantatore(classe: str, livello_classe: int) -> int:
    if classe.lower() in di()["LIVELLO_INCANTATORE_RIDOTTO"]:
        return _formula("livello_incantatore_ridotto")(livello=livello_classe)
    return livello_classe

#: I livelli che il test confronta con le ancore delle skill.
ANCORE = (1, 5, 10, 15, 20)


def livello_massimo(griglia: dict[int, tuple[int, ...]], livello: int) -> int:
    """Il livello d'incantesimo più alto che questo incantatore lancia."""
    slot = griglia[max(1, min(20, livello))]
    alti = [i for i, n in enumerate(slot) if n > 0]
    return max(alti) if alti else 0


def cd_incantesimo(livello_incantesimo: int, modificatore: int) -> int:
    """SRD: CD = 10 + livello dell'incantesimo + modificatore di caratteristica.

    La formula sta nei dati del plugin (`formule.regole`, F3 di ADR-0112)."""
    return _formula("cd_incantesimo")(livello=livello_incantesimo, modificatore=modificatore)


# ===========================================================================
# PF1e — i bersagli per GS. La variante «più cattivi».
# ===========================================================================
# Qui il SRD 3.5 **non ha un equivalente**: una tabella «statistiche per GS» non
# esiste nel SRD, e questa è contenuto libero OGL. Il DM l'ha chiesta per due
# usi distinti, e vanno tenuti distinti:
#
#   1. **collaudo** (sempre attivo): dice se un mostro costruito dal SRD è fuori
#      bersaglio. Non fornisce numeri.
#   2. **bersaglio** (solo con `--piu-cattivi`): fornisce i numeri, e allora la
#      creatura esce dichiaratamente più dura di quanto il GS 3.5 prometta.
#
#: 🔴 **La tabella non sta piu' qui: sta in `scripts/pf1e-statistiche-per-gs.yaml`.**
#: Fino al 2026-09-23 c'era una costante scritta a mano, con otto righe
#: dichiarate «verificate» contro la skill. Rilette contro la fonte OGL
#: (Bestiary, Table 1–1) sbagliavano **danno, CD primaria e TS cattivo**, e il
#: GS 12 aveva l'attacco del GS 11: la skill e la costante erano state scritte
#: dalla stessa mano, e il test che le confrontava confrontava due copie dello
#: stesso errore. Ora il dato e' uno, e sta dove il DM lo legge.
FILE_PER_GS = Path(__file__).resolve().parent.parent / "pf1e-statistiche-per-gs.yaml"
_RIGA_YAML = re.compile(r"^\s*-\s*\{(.*)\}\s*$")


def _leggi_per_gs(percorso: Path = FILE_PER_GS) -> "tuple[dict, dict]":
    """Le righe della Tabella 1–1 e la tolleranza, senza pyyaml.

    Il file ha una forma sola — una mappa in linea per riga sotto `righe:` —
    e il lettore accetta **solo** quella: un file scritto diversamente fallisce
    qui, rumorosamente, invece di dare una tabella vuota.
    """
    righe, tolleranza, sezione = {}, {}, None
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        if not riga.startswith(" "):
            sezione = riga.split(":")[0].strip()
            continue
        if sezione == "righe":
            m = _RIGA_YAML.match(riga)
            if not m:
                raise ValueError(f"{percorso.name}: riga illeggibile: {riga!r}")
            campi = dict(c.split(":") for c in m.group(1).split(","))
            campi = {k.strip(): float(v) for k, v in campi.items()}
            gs = campi.pop("gs")
            righe[int(gs) if gs >= 1 else gs] = {k: int(v) for k, v in campi.items()}
        elif sezione == "tolleranza":
            k, v = riga.split(":")
            tolleranza[k.strip()] = float(v)
    if len(righe) < 30:
        raise ValueError(f"{percorso.name}: {len(righe)} righe, la Tabella 1–1 ne ha 31")
    return righe, tolleranza


TABELLA_1_1, TOLLERANZA_PER_GS = _leggi_per_gs()

#: GS → (CA, pf, attacco alto, danno medio alto, CD primaria, TS buono, TS cattivo),
#: la forma che i chiamanti usavano gia'. Solo i GS interi da 1 a 20.
PER_GS = {gs: (r["ca"], r["pf"], r["attacco_alto"], r["danno_alto"],
               r["cd_primaria"], r["ts_buono"], r["ts_cattivo"])
          for gs, r in TABELLA_1_1.items() if isinstance(gs, int) and 1 <= gs <= 20}
CAMPI_PER_GS = ("ca", "pf", "attacco", "danno", "cd", "ts_buono", "ts_cattivo")

#: Tutte le righe vengono dalla fonte, quindi sono tutte verificate. Il nome
#: resta perche' i chiamanti lo usano per ammorbidire un giudizio: adesso non
#: devono ammorbidire niente.
PER_GS_VERIFICATE = frozenset(PER_GS)

#: PF1e Bestiary, appendice «Monster Advancement» — quanto compra un passo di
#: GS. Questa tabella è verificata su tutto l'arco, ed è la ragione per cui le
#: righe non verificate qui sopra sono *estrapolate* e non *inventate*.
PASSI_GS = {
    "<1→1": (5, 1, 1, 2.5), "1→3": (7.5, 1.5, 1.5, 2.5), "3→4": (10, 2, 2, 2.5),
    "4→12": (15, 1.5, 1.5, 4), "12→16": (20, 1, 1.5, 6.5),
    "16→19": (30, 1, 1, 8.5), "19→": (40, 2, 1, 9),
}

#: PF1e, colonna «heroic NPC» — il valore totale dell'equipaggiamento. Il SRD 3.5
#: dà la ricchezza per livello del **PG**, che è un'altra cosa: un PNG non ha
#: vent'anni di avventure alle spalle.
EQUIPAGGIAMENTO_PNG = {7: 6000, 9: 10050, 11: 16350, 13: 27000, 15: 45000,
                       17: 75000}


def riga_gs(gs: int) -> tuple[dict[str, int], bool]:
    """I bersagli per un GS, e se quella riga è verificata.

    Restituisce sempre una riga — rifiutarsi non aiuta nessuno — ma il secondo
    valore dice se fidarsene ciecamente. Chi la usa per **giudicare** deve
    ammorbidire il giudizio su una riga non verificata; chi la usa per
    **generare** deve stamparlo nel `fonte:` della creatura.
    """
    gs = max(1, min(20, int(gs)))
    return dict(zip(CAMPI_PER_GS, PER_GS[gs])), gs in PER_GS_VERIFICATE


# ===========================================================================
# I conti che si ripetono
# ===========================================================================

#: Le formule stanno nei dati del plugin d20 (`sistemi/d20/dati/formule.toml`,
#: F3 di ADR-0112) e si valutano con `dmcore.formule`; qui restano i nomi.
def _formula(nome: str):
    return _formule.formula(nome, "dnd35")


def mod(punteggio: int) -> int:
    return _formula("modificatore")(punteggio=punteggio)


def ts_buono(dv: int) -> int:
    return _formula("ts_buono")(dv=dv)


def ts_cattivo(dv: int) -> int:
    return _formula("ts_cattivo")(dv=dv)


def media_dado(faccia: int) -> float:
    """La media di un dado come la conta il SRD per i PNG: (faccia / 2) + 0,5."""
    return faccia / 2 + 0.5


def normalizza_tipo(testo: str) -> str | None:
    """Il tipo di creatura, comunque sia scritto nella scheda."""
    t = (testo or "").strip().lower()
    if t in di()["TIPI"]:
        return t
    if t in di()["ALIAS_TIPO"]:
        return di()["ALIAS_TIPO"][t]
    for chiave in sorted(di()["TIPI"], key=len, reverse=True):
        if chiave in t:
            return chiave
    for alias in sorted(di()["ALIAS_TIPO"], key=len, reverse=True):
        if alias in t:
            return di()["ALIAS_TIPO"][alias]
    return None
