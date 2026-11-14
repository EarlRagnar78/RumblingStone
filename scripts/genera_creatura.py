"""genera_creatura.py — da (GS + tipo + ruolo) a un blocco completo.

Il pezzo che mancava. `suggest_encounter` **sceglie** dal catalogo,
`build_monster_catalog` lo **indicizza**, `derive_statblocks` **legge** una
scheda che esiste già. Nessuno dei tre costruisce una creatura che non c'è.

## Perché questo è sicuro dove il lotto H non lo era

Il derivatore leggeva prosa italiana e ne ricavava numeri: sbagliava in silenzio,
e sbagliava producendo cose plausibili — «CA 11 per un mostro di GS 9» ha l'aria
di un conto, non di un errore. Qui l'ingresso non è prosa: sono **parametri
dichiarati** dal DM. Non c'è niente da indovinare, e il conto è mostrato per
esteso in `fonte:`.

## Le due tarature, che il DM ha chiesto distinte

    (di norma)        le tabelle SRD 3.5 danno la FORMA — tipo → dado dei DV,
                      BAB, TS buoni; taglia → modificatori; classe → incantesimi
                      al giorno e CD — e il bersaglio 3.5 dà il LIVELLO.

    --piu-cattivi     la stessa creatura con il template **Advanced** di PF1e
                      applicato SENZA alzare il GS: +4 a tutte le
                      caratteristiche, +2 di armatura naturale. Vale GS +1 e
                      viene venduta come GS: è precisamente «più cattiva di
                      quanto il GS prometta», ed è una riga sola da disfare.

## Una correzione a quello che avevo scritto prima

Nel piano avevo scritto che «PF1e a parità di GS è molto più duro del 3.5», e
sulla riga base **non è vero**. Confrontata con i mostri del SRD 3.5:

    GS 3   Ogre      29 pf, CA 16   ·  riga PF1e:  30 pf, CA 17
    GS 5   Troll     63 pf, CA 16   ·  riga PF1e:  55 pf, CA 19
    GS 7   Chimera   76 pf, CA 19   ·  riga PF1e:  85 pf, CA 20
    GS 7   Ettin     102 pf, CA 20  ·  riga PF1e:  85 pf, CA 20

Sui punti ferita le due tarature si sovrappongono; PF1e sta un punto o due sopra
sulla CA e sull'attacco. Perciò il bersaglio 3.5 qui è la riga PF1e con **CA −1 e
attacco −1**, e non una derata inventata al 70%. La differenza vera fra i due
sistemi non sta nella riga: sta nei *template*, ed è da lì che viene la variante
più cattiva.

## Dove finisce

**Mai dentro `Bestiario/`.** Stampa, o scrive in una cartella di lavoro con
`--in`. Il confine è quello di ADR-0033: lo strumento propone, la mano che
scrive nel canone resta quella del DM. Il generatore serve per **quello che nel
bestiario non c'è**; se c'è già qualcosa di simile, si potenzia (skill
`npc-villain-boosting`), non si genera un doppione.

Uso:

    python3 scripts/genera_creatura.py --gs 7 --tipo umanoide --ruolo bruto
    python3 scripts/genera_creatura.py --gs 7 --ruolo bruto --piu-cattivi
    python3 scripts/genera_creatura.py --gs 9 --ruolo blaster --classe mago:9
    python3 scripts/genera_creatura.py --gs 9 --ruolo bruto --classe chierico:9 \\
        --funzione supporto
    python3 scripts/genera_creatura.py --gs 14 --ruolo controllore \\
        --classe druido:14 --incantesimi pf1e
    python3 scripts/genera_creatura.py --gs 5 --quanti 3 --seed 42 --json

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import caratteristiche as CAR  # noqa: E402
from dmcore import incantesimi as INC  # noqa: E402
from dmcore import modelli as MOD  # noqa: E402
from dmcore import tabelle as T  # noqa: E402
from dmcore import sistemi as S  # noqa: E402
from dmcore.progressione import ts_base_di  # noqa: E402
from dmcore.statblock import Statblocco, rendi  # noqa: E402

# ===========================================================================
# I ruoli
# ===========================================================================
# ⚠️ Sei ruoli, ed è una PROPOSTA: il piano lascia al DM la domanda «quali
# servono davvero al tuo tavolo». Togliere un ruolo qui è una riga; è il motivo
# per cui sono dati e non rami del codice.
#
# Ogni ruolo dice tre cose e nient'altro:
#   * quale profilo di `dmcore.caratteristiche.PROFILI` ordina la matrice
#     élite/standard;
#   * l'arma e il modo di combattere;
#   * se è un incantatore, e con che classe di norma.
#
# ⚖️ **La tabella dei ruoli è una sola** (D2 di `PIANO-QUALITA-DEL-CODICE`,
# decisa dal DM il 2026-09-23: vince `genera_attributi`). Fino al lotto E6 ogni
# ruolo qui aveva un suo ordine delle caratteristiche, e su sei ruoli quattro
# non coincidevano con il profilo omonimo di `genera_attributi`: un tiratore
# generato qui e un tiratore del Bestiario ricevevano la stessa matrice in un
# ordine diverso. Ora il ruolo nomina il profilo, e l'ordine si legge da lì.


@dataclass(frozen=True)
class Ruolo:
    nome: str
    #: La chiave del profilo in `dmcore.caratteristiche.PROFILI`, cercata con
    #: `profilo_esatto` e non per sottostringa come fa `profilo_di`: un profilo
    #: tolto o rinominato là è un `KeyError` al primo PNG, non un ordine di ripiego.
    profilo: str
    arma: str
    dado_arma: str
    #: A distanza usa Destrezza per l'attacco.
    distanza: bool = False
    classe_tipica: str = ""
    #: Bonus all'armatura naturale: il bruto ha la pelle dura, il tiratore no.
    naturale: int = 0
    #: Se il bonus d'attacco va RISOLTO verso il bersaglio (chi campa di colpi)
    #: o preso com'è (un incantatore non deve colpire: deve lanciare). Risolvere
    #: l'attacco di un controllore gli dava Forza 22, che non è un controllore.
    risolve_attacco: bool = True
    descrizione: str = ""


RUOLI = {
    "bruto": Ruolo(
        "bruto", "brute",
        "mazzafrusto pesante", "1d10", naturale=2,
        descrizione="regge la linea e la sfonda; poca finezza, molta stazza"),
    "schermagliatore": Ruolo(
        "schermagliatore", "skirmisher",
        "spada corta", "1d6",
        descrizione="colpisce e si sposta; vive finche' non lo si inchioda"),
    "tiratore": Ruolo(
        "tiratore", "ranged",
        "arco lungo", "1d8", distanza=True,
        descrizione="sta dietro e fa male; il problema e' raggiungerlo"),
    "comandante": Ruolo(
        "comandante", "commander",
        "spada lunga", "1d8", naturale=1,
        descrizione="vale per quello che fa fare agli altri, non per i suoi danni"),
    "controllore": Ruolo(
        "controllore", "arcane",
        "bastone ferrato", "1d6", classe_tipica="mago", risolve_attacco=False,
        descrizione="toglie ai PG le opzioni; il danno viene dopo"),
    "blaster": Ruolo(
        "blaster", "blaster",
        "pugnale", "1d4", classe_tipica="mago", risolve_attacco=False,
        descrizione="danno d'area a distanza; fragile se lo si raggiunge"),
}

#: I nomi vecchi che continuano a funzionare. `artigliere` è come si chiamava
#: `blaster` fino al lotto I; il DM ha scelto il nome nuovo, ma un alias costa
#: una riga e salva ogni comando già scritto negli appunti del tavolo. Il nome
#: **canonico** è quello nuovo, ed è quello che finisce in `fonte:`: due schede
#: generate con i due nomi devono restare confrontabili.
ALIAS_RUOLO = {"artigliere": "blaster"}


def normalizza_ruolo(nome: str) -> str:
    return ALIAS_RUOLO.get(nome.strip().lower(), nome.strip().lower())

#: Il carattere — lotto E del piano, e la ragione per cui il tool non è banale.
#: Senza, escono mostri intercambiabili, e un mostro intercambiabile il DM se lo
#: scrive prima da solo che a leggerlo.
#: ⚠️ Scritte a mano, **proposte al DM**: sono le tabelle che il piano §5 chiede
#: se le scrive lui o le propongo io. Non sono generate, e non devono esserlo.
CARATTERE: dict[str, list[tuple[str, str, str]]] = {
    # (talento firma, tattica in una riga, debolezza sfruttabile)
    "bruto": [
        ("Attacco Poderoso", "carica il bersaglio piu' lontano dai suoi, per spezzare la linea",
         "una volta caricato non si ferma: gli si apre il fianco"),
        ("Sbilanciare Migliorato", "atterra e poi calpesta chi e' a terra",
         "se il bersaglio resta in piedi ha sprecato il turno"),
        ("Colpo Poderoso", "sfonda una porta o un muro per entrare da dove non lo aspettano",
         "sordo a tutto: non nota il secondo gruppo che lo aggira"),
        ("Robustezza", "assorbe il primo scontro mentre gli altri manovrano",
         "lento: chi corre lo semina"),
    ],
    "schermagliatore": [
        ("Schivare Prodigioso", "entra, colpisce il piu' fragile, esce dalla portata",
         "se lo si blocca in mezzo a due, muore in fretta"),
        ("Mobilita'", "usa il terreno rotto per non farsi mai attaccare due volte di fila",
         "in campo aperto perde meta' del suo valore"),
        ("Attacco Furtivo (se accompagnato)", "aspetta che un alleato inchiodi, poi colpisce di lato",
         "da solo non fa male: si toglie l'alleato, non lui"),
        ("Iniziativa Migliorata", "agisce prima e sceglie il bersaglio della giornata",
         "se perde l'iniziativa il suo piano non esiste piu'"),
    ],
    "tiratore": [
        ("Tiro Rapido", "due frecce sul curatore, sempre sul curatore",
         "in mischia e' un bersaglio come un altro"),
        ("Tiro Preciso", "tira anche nella mischia, incurante degli alleati",
         "colpisce i suoi: si puo' provocare l'incidente"),
        ("Mira", "prende posizione alta e non la lascia",
         "la posizione e' nota: si puo' arrivare da sotto"),
        ("Schivare", "arretra sempre di una casella dopo aver tirato",
         "arretrando finisce contro il muro"),
    ],
    "comandante": [
        ("Comandare (azione di round)", "concede un attacco extra a un alleato ogni round",
         "morto lui, gli altri perdono il bonus e spesso il morale"),
        ("Guerra di Squadra", "riorganizza la linea quando un alleato cade",
         "se cadono due alleati nello stesso round non fa in tempo"),
        ("Volonta' di Ferro", "tiene fermi i suoi quando dovrebbero scappare",
         "e' l'unico a saperlo fare: isolarlo scioglie il gruppo"),
        ("Attacco in Movimento", "sta sempre a portata di voce di tre alleati",
         "quel raggio lo rende prevedibile"),
    ],
    "controllore": [
        ("Incantesimi Focalizzati", "chiude il campo prima di fare danno",
         "concentrazione: un colpo mentre lancia gli costa l'incantesimo"),
        ("Incantesimo Rapido", "apre con un controllo e si sposta nello stesso turno",
         "gli slot rapidi sono pochi: dopo due e' scoperto"),
        ("Maestria in Combattimento", "si difende invece di attaccare, e aspetta",
         "se aspetta troppo i PG arrivano"),
        ("Scrutare", "sa dove sono i PG prima che entrino",
         "quello che sa lo dice a nessuno: ucciderlo cieca il gruppo"),
    ],
    "blaster": [
        ("Incantesimi Potenziati", "un'area sola, sul grappolo piu' fitto",
         "colpisce anche i suoi: si puo' costringerlo a scegliere"),
        ("Incantesimo Immobile", "lancia da legato o in spazio stretto",
         "poco resistente: due colpi lo mettono a terra"),
        ("Arcano Fulmineo", "apre col danno prima che i PG chiudano la distanza",
         "speso l'apertura, e' un mago di secondo livello"),
        ("Penetrare Incantesimi", "sceglie il bersaglio con meno resistenza",
         "prevedibile: chi ha la resistenza lo attira"),
    ],
}

#: I tipi che si prestano a un incontro di passaggio, per quando il DM non
#: sceglie. Non è una tabella di regole: è una scorciatoia dichiarata.
TIPI_COMUNI = ("humanoid", "monstrous humanoid", "magical beast", "giant",
               "aberration", "undead", "outsider", "animal")


# ===========================================================================
# Costruire
# ===========================================================================
# Due modi, perché in 3.5 sono due cose diverse e confonderle è il difetto che
# la prima versione di questo file aveva:
#
#   MOSTRO  — non ha classi. I suoi punteggi non escono da una matrice: nel
#             manuale sono scritti uno per uno. Qui si RISOLVONO verso il
#             bersaglio del GS, che è come li sceglie chi scrive un mostro.
#   PNG     — ha livelli di classe. Lì la matrice élite/standard è la fonte
#             giusta, e il GS viene dai livelli, non viceversa.
#
# La prima versione costruiva ogni cosa come un PNG con la matrice standard, e
# produceva un «GS 7» con 38 pf e CA 12. Il collaudo l'ha detto subito (−55%), ed
# è esattamente il lavoro per cui il collaudo esiste.

#: Il bersaglio 3.5 è la riga PF1e con CA e attacco ridotti di uno. Misurato sui
#: mostri del SRD, non deciso a tavolino: vedi il confronto in testa al file.
DERATA_35 = {"ca": -1, "attacco": -1, "cd": -1}

#: Quanto ciascun ruolo si scosta dal bersaglio. Un bruto sta sopra sui pf e
#: sotto sulla CA; un tiratore il contrario. Somma zero: nessun ruolo è
#: gratuitamente migliore di un altro, e questo va tenuto vero se si aggiunge
#: un ruolo.
SCOSTAMENTO = {
    "bruto":           {"pf": +0.20, "ca": -2, "attacco": +1},
    "schermagliatore": {"pf": -0.10, "ca": +1, "attacco": +1},
    "tiratore":        {"pf": -0.20, "ca": +2, "attacco": +1},
    "comandante":      {"pf": +0.00, "ca": +1, "attacco": +0},
    # ⚠️ Gli incantatori stanno SOTTO il bersaglio anche sulla CA, e di parecchio.
    # Il loro GS non lo pagano con la corazza: lo pagano con quello che fanno
    # fare al campo. Un luogotenente illithid di GS 12 costruito sul bersaglio
    # pieno usciva con CA 26 — un mind flayer in armatura da paladino.
    "controllore":     {"pf": -0.20, "ca": -4, "attacco": -2},
    "blaster":         {"pf": -0.25, "ca": -4, "attacco": -2},
}

#: Destrezza tipica per ruolo, che il bersaglio non decide (la CA la si raggiunge
#: con l'armatura naturale, ma un tiratore goffo non è un tiratore).
DESTREZZA = {"bruto": 11, "schermagliatore": 17, "tiratore": 18,
             "comandante": 13, "controllore": 14, "blaster": 13}

#: I punteggi mentali, che nessun bersaglio impone. Un mostro senza carattere ha
#: sempre Int 10: è il modo più veloce per farlo sembrare uguale a tutti gli altri.
MENTALI = {
    "bruto":           {"int": 8,  "sag": 11, "car": 9},
    "schermagliatore": {"int": 11, "sag": 12, "car": 11},
    "tiratore":        {"int": 11, "sag": 14, "car": 10},
    "comandante":      {"int": 13, "sag": 13, "car": 16},
    "controllore":     {"int": 18, "sag": 13, "car": 12},
    "blaster":         {"int": 18, "sag": 11, "car": 12},
}

#: PF1e, template **Advanced** (verificato in
#: `pathfinder-1e-srd/references/monster-advancement.md`): regole di ricostruzione.
#: Vale GS +1. Applicarlo SENZA alzare il GS è la definizione operativa di
#: «più cattivo di quanto il GS prometta» — ed è una riga sola da disfare.
ADVANCED = {"caratteristiche": +4, "naturale": +2, "gs_reale": +1}

#: Il tetto ai modificatori risolti. Oltre questo, la differenza la copre
#: l'equipaggiamento — che è come la copre un DM che costruisce a mano. Senza
#: tetto uscivano Cos 24 e Des 28 a GS 7: numeri giusti per i pf e per l'attacco,
#: e sbagliati per tutto il resto (Tempra, Riflessi, Concentrazione, prove di
#: abilità), dove un mostro con quei punteggi è di un altro livello.
MOD_MAX = 8
#: La Destrezza ha un tetto piu' basso della Forza, e non per gusto: la Forza
#: paga attacco e danno, la Destrezza paga attacco, CA, Riflessi, iniziativa e
#: ogni prova di abilita' basata su di lei. Un +8 di Destrezza sposta sei
#: numeri; un +8 di Forza ne sposta due.
MOD_MAX_DES = 6


@dataclass
class Conto:
    """Il conto per esteso. È metà del valore dello strumento: un numero senza
    il suo conto è un numero di cui al tavolo non ci si fida."""
    righe: list[str] = field(default_factory=list)
    rincari: list[str] = field(default_factory=list)
    #: per i talenti (lotto 3 delle regole complete): BAB, livelli di classe,
    #: livello d'incantatore, DV razziali, scritti da chi costruisce il blocco
    talenti: dict = field(default_factory=dict)

    def __call__(self, riga: str) -> None:
        self.righe.append(riga)

    def rincaro(self, riga: str) -> None:
        self.rincari.append(riga)


def bersaglio_di(gs: int, ruolo: str, piu_cattivi: bool) -> tuple[dict[str, int], bool]:
    """I numeri verso cui si costruisce, e se la riga di partenza è verificata."""
    riga, verificata = T.riga_gs(gs)
    b = dict(riga)
    if not piu_cattivi:
        for campo, delta in DERATA_35.items():
            b[campo] += delta
    s = SCOSTAMENTO[ruolo]
    b["pf"] = max(1, round(b["pf"] * (1 + s["pf"])))
    b["ca"] += s["ca"]
    b["attacco"] += s["attacco"]
    return b, verificata


def _punteggio(modificatore: int) -> int:
    """Dal modificatore al punteggio. SRD: mod = (punteggio − 10) // 2."""
    return max(1, 10 + modificatore * 2)


def dv_di_partenza(gs: int, tipo: str) -> int:
    """Quanti DV ha un mostro di questo GS.

    ⚠️ **Regola pratica dichiarata, non una tabella del SRD**: il SRD non ha un
    «DV per GS». È tarata sui mostri del SRD (Ogre GS 3 → 4 DV; Troll GS 5 → 6;
    Chimera GS 7 → 9; Ettin GS 6 → 10; Osyluth GS 9 → 10) e sta scritta qui,
    invece che sepolta nel codice, perché è esattamente il genere di numero che
    fra sei mesi sembra una fonte se nessuno dice che non lo è.
    """
    dado, bab, buoni = T.TIPI[tipo]
    fattore = 1.3
    if bab >= 1.0 and len(buoni) >= 3:
        fattore = 1.1          # esterni e draghi: BAB pieno, tre TS buoni
    elif bab <= 0.5:
        fattore = 1.5          # non-morti e costrutti: BAB e TS bassi
    return max(1, round(gs * fattore))


def genera(gs: int, *, tipo: str = "humanoid", taglia: str = "medium",
           ruolo: str = "bruto", dv: int | None = None, elite: bool | None = None,
           classe: tuple[str, int] | None = None, piu_cattivi: bool = False,
           rng: random.Random | None = None, funzione: str | None = None,
           incantesimi_pf1e: bool | None = None,
           talenti: str | None = "dnd35",
           modello: str | None = None) -> tuple[Statblocco, Conto]:
    """Un blocco completo, e il conto che l'ha prodotto.

    `funzione` è la funzione da incantatore (controllore · blaster · supporto ·
    utilità) e vale solo con `classe`: il ruolo tattico dice **come combatte**,
    la funzione **cosa fa con gli incantesimi**, e sono due assi diversi — un
    bruto con livelli da chierico è un chierico da guerra, ruolo «bruto» e
    funzione «supporto». Se non la si passa, `FUNZIONE_DA_RUOLO` la deduce.

    `incantesimi_pf1e` lasciato a None segue `piu_cattivi`, che è la lettura
    naturale: «più cattivo a pari GS» vale per il template e per la lista. Passarlo
    esplicitamente separa le due metà.

    `talenti` è il sistema di cui si applicano i talenti (`applica_talenti`);
    None li lascia a chi converte il blocco in un altro sistema dopo.

    `modello` è un modello semplice di PF1e (`dmcore/modelli.py`, lotto J):
    advanced, giant, young, celestial, fiendish, entropic, resolute. Si applica
    al blocco finito senza cambiare il GS scritto. `piu_cattivi` è il modello
    «advanced» coi bersagli e gli incantesimi di PF1e: i due nomi dicono la
    stessa cosa e chiederli insieme con un modello diverso è un errore.
    """
    if modello:
        modello = MOD.modello(modello)["chiave"]
        if modello == "advanced":
            piu_cattivi = True
        elif piu_cattivi:
            raise ValueError("«più cattivi» è il modello advanced: non si somma a "
                             f"«{modello}»")
    rng = rng or random.Random()
    ruolo = normalizza_ruolo(ruolo)
    if ruolo not in RUOLI:
        raise ValueError(f"ruolo ignoto: {ruolo}")
    if incantesimi_pf1e is None:
        incantesimi_pf1e = piu_cattivi
    R = RUOLI[ruolo]
    conto = Conto()
    conto(f"GS {gs} · {tipo} · {taglia} · ruolo {ruolo} — {R.descrizione}")

    if classe:
        sb, conto = _genera_png(gs, tipo, taglia, R, classe, elite, conto,
                                rng, funzione, incantesimi_pf1e)
    else:
        sb, conto = _genera_mostro(gs, tipo, taglia, R, dv, piu_cattivi, conto, rng)

    traccia = None
    if piu_cattivi or modello:
        traccia = MOD.applica(sb, modello or "advanced")
        for riga in traccia.righe:
            conto.rincaro(riga)
    if talenti:
        applica_talenti(sb, conto, talenti, ruolo, rng)
    sb.fonte = _fonte(gs, tipo, taglia, ruolo, classe, piu_cattivi, conto,
                      funzione, incantesimi_pf1e)
    if traccia:
        sb.fonte += f" template={traccia.modello}-PF1e-gs-reale={traccia.gs_reale}"
    return sb, conto


# ── il mostro: si risolve verso il bersaglio ────────────────────────────────

def tratti_del_tipo(tipo: str, taglia: str = "medium") -> dict:
    """I tratti del tipo che cambiano il blocco: senza Costituzione, senza mente,
    pf bonus del costrutto (sistemi/dnd35/dati/creature.toml, [tratti_tipo] e
    [pf_bonus_costrutti], dall'SRD «Types»)."""
    dati = S.dati("dnd35", "creature.costruzione")
    chiave = T.ALIAS_TIPO.get(tipo, tipo)
    t = dati.get("tratti_tipo", {}).get(chiave, {})
    tg = taglia.lower()
    if tg not in dati.get("pf_bonus_costrutti", {}):
        tg = next((k for k in T.TAGLIE if T.TAGLIE[k] == T.TAGLIE.get(tg)
                   and k in dati.get("pf_bonus_costrutti", {})), tg)
    bonus = dati.get("pf_bonus_costrutti", {}).get(tg, 0) if chiave == "construct" else 0
    return {"senza_cos": bool(t.get("senza_cos")), "senza_int": bool(t.get("senza_int")),
            "pf_bonus": bonus}


def _genera_mostro(gs, tipo, taglia, R, dv, piu_cattivi, conto, rng):
    dado, bab_per_dv, ts_buoni = T.TIPI[tipo]
    dv_tot = dv if dv is not None else dv_di_partenza(gs, tipo)
    dv_iniziali = dv_tot

    # Il bersaglio si calcola SEMPRE sulla taratura 3.5: il template Advanced
    # arriva dopo, come strato dichiarato, e non deve essere contato due volte.
    bersaglio, verificata = bersaglio_di(gs, R.nome, piu_cattivi=False)
    conto("bersaglio 3.5 (riga PF1e con CA/attacco −1, più lo scostamento del "
          f"ruolo): pf {bersaglio['pf']}, CA {bersaglio['ca']}, "
          f"attacco {bersaglio['attacco']:+d}"
          + ("" if verificata else "  ⚠ riga PF1e NON verificata per questo GS"))

    nat_taglia, mod_taglia = T.TAGLIE[taglia]
    des = DESTREZZA[R.nome]
    m_des = T.mod(des)

    # Costituzione: quella che porta i pf sul bersaglio — ma dentro una banda.
    #
    # Risolvendo la sola Costituzione, un GS 7 usciva con Cos 24 su 9 DV. È il
    # numero giusto e la creatura sbagliata: nel SRD un mostro con quei pf ha più
    # DV e una Costituzione normale (Ettin GS 6: 10 DV, Cos 15; Gigante delle
    # Colline GS 7: 12 DV, Cos 19). Una Cos 24 a GS 7 non si nota nei pf — si
    # nota nei tiri salvezza su Tempra e nelle prove di Concentrazione, e lì è
    # un mostro di un altro livello. Quindi: prima si aggiungono DV, e solo
    # quando i DV finiscono si alza la Costituzione.
    COS_MAX = 6          # +6 → Cos 22, il tetto di un mostro non eccezionale
    DV_MAX = max(2 * gs, dv_tot)
    tratti = tratti_del_tipo(tipo, taglia)
    if tratti["senza_cos"]:
        # SRD 3.5, Construct e Undead: «No Constitution score». I pf sono i soli
        # dadi (più il bonus di taglia del costrutto): il bersaglio si insegue
        # con i DV, e quello che i DV non coprono resta scoperto e si dice.
        m_cos = 0
        while True:
            media = T.media_dado(dado) * dv_tot
            if (media + tratti["pf_bonus"] >= bersaglio["pf"] or dv_tot >= DV_MAX
                    or dv is not None):
                break
            dv_tot += 1
        cos = "—"
        pf = max(1, int(media) + tratti["pf_bonus"])
    else:
        while True:
            media = T.media_dado(dado) * dv_tot
            m_cos = round((bersaglio["pf"] - media) / dv_tot)
            if m_cos <= COS_MAX or dv_tot >= DV_MAX or dv is not None:
                break
            dv_tot += 1
        cos = _punteggio(m_cos)
        pf = max(1, int(media + m_cos * dv_tot))
    conto(f"DV {dv_tot}d{dado}" + ("" if dv is not None else
          f" (regola pratica DV≈GS×1,{'1' if dv_iniziali < gs else '3'}, tarata sui "
          f"mostri del SRD"
          + (f"; saliti da {dv_iniziali} per " + ("inseguire i pf senza Costituzione"
             if tratti["senza_cos"] else "non sfondare la banda della Costituzione")
             if dv_tot != dv_iniziali else "") + ")"))
    if tratti["senza_cos"]:
        conto(f"Cos — ({tipo}: nessun punteggio di Costituzione, SRD «Types»): pf = "
              f"{media:.1f} dei dadi"
              + (f" +{tratti['pf_bonus']} bonus del costrutto {taglia} (Construct Traits)"
                 if tratti["pf_bonus"] else "") + f" = {pf}"
              + (f"; mancano {bersaglio['pf'] - pf} pf al bersaglio con {dv_tot} DV, "
                 "il tetto di 2×GS: è il prezzo del tipo, che le immunità ripagano"
                 if pf < bersaglio["pf"] else ""))
    else:
        conto(f"Cos {cos} ({m_cos:+d}) risolta sui pf: {media:.1f} + {m_cos:+d}×{dv_tot} DV = {pf}")

    # Armatura naturale: quella che porta la CA sul bersaglio, mai sotto quella
    # della taglia (un mostro enorme ha comunque la sua corazza).

    # Forza: quella che porta l'attacco sul bersaglio.
    bab = int(bab_per_dv * dv_tot)
    m_att = bersaglio["attacco"] - bab - mod_taglia
    if not R.risolve_attacco:
        # Un incantatore non campa di colpi: la Forza resta quella di un
        # incantatore e l'attacco è quello che viene. Risolverlo verso il
        # bersaglio gli dava Forza 22, e un controllore con Forza 22 non è un
        # controllore: è un bruto che conosce due incantesimi.
        forza, m_for = 12, 1
        attacco = bab + m_for + mod_taglia
        conto(f"For {forza}: l'attacco non si risolve per un {R.nome} — "
              f"{attacco:+d} contro un bersaglio di {bersaglio['attacco']:+d}, "
              "e va bene così: il suo danno passa dagli incantesimi")
    elif R.distanza:
        # A distanza il bersaglio si raggiunge con la Destrezza — ma dentro una
        # banda, come per la Costituzione: risolvendola senza tetto un GS 7
        # usciva con Des 28. Un arciere vero non ha Des 28: ha Des 18 e un arco
        # magico. Il resto lo copre l'equipaggiamento, e viene detto.
        m_des = min(max(m_des, m_att), MOD_MAX_DES)
        des = _punteggio(m_des)
        arma_magica = max(0, m_att - m_des)
        forza, m_for = 14, 2
        attacco = bab + m_des + mod_taglia + arma_magica
        conto(f"Des {des} ({m_des:+d}) sull'attacco a distanza: BAB {bab:+d} "
              f"{m_des:+d} Des" + (f" {mod_taglia:+d} taglia" if mod_taglia else "")
              + (f" +{arma_magica} arco magico" if arma_magica else "")
              + f" = {attacco:+d}; arco composito (For {forza}) perché il danno sia suo")
    else:
        m_for = min(m_att, MOD_MAX)
        forza = _punteggio(m_for)
        arma_magica = max(0, m_att - m_for)
        attacco = bab + m_for + mod_taglia + arma_magica
        conto(f"For {forza} ({m_for:+d}) sull'attacco: BAB {bab:+d} {m_for:+d} For"
              + (f" {mod_taglia:+d} taglia" if mod_taglia else "")
              + (f" +{arma_magica} arma magica" if arma_magica else "")
              + f" = {attacco:+d}")

    # L'armatura naturale si calcola DOPO l'attacco: per un tiratore la
    # Destrezza è appena salita, e con essa la CA. Calcolarla prima le dava
    # due punti di troppo.
    naturale = max(nat_taglia + R.naturale,
                   bersaglio["ca"] - 10 - m_des - mod_taglia)
    ca = 10 + m_des + naturale + mod_taglia
    pezzi_ca = [f"{m_des:+d} Des", f"+{naturale} naturale"]
    if mod_taglia:
        pezzi_ca.append(f"{mod_taglia:+d} taglia")
    conto(f"CA = 10 {' '.join(pezzi_ca)} = {ca}")

    men = dict(MENTALI[R.nome])
    if tratti["senza_int"]:
        men["int"] = "—"
    attr = {"for": forza, "des": des, "cos": cos, **men}
    # una caratteristica che non c'è non dà modificatore (SRD, «Nonabilities»)
    m = {k: (T.mod(v) if isinstance(v, int) else 0) for k, v in attr.items()}

    ts = _tiri_salvezza(dv_tot, ts_buoni, m, conto)
    talento, tattica, debolezza = rng.choice(CARATTERE[R.nome])
    conto.talenti = {"bab": bab, "livelli": {}, "lic": 0, "dv_razziali": dv_tot, "dv": dv_tot}
    if tratti["senza_int"]:
        # SRD: «Mindless creatures do not gain feats or skills»
        conto.talenti = None
        talento = "—"
        conto(f"Int — ({tipo} senza mente, SRD «Types»): niente talenti né abilità")
    mod_danno = m["for"]   # arco composito: anche a distanza il danno è suo

    return Statblocco(
        nome=f"{R.nome} {tipo} GS {gs}",
        gs=str(gs),
        tipo=f"{taglia.capitalize()} {tipo}, {dv_tot}d{dado}"
             + (f"+{m_cos * dv_tot}" if m_cos > 0 else "")
             + (f"+{tratti['pf_bonus']}" if tratti["pf_bonus"] else ""),
        ca=str(ca), ca_dettaglio="(" + ", ".join(pezzi_ca) + ")",
        pf=str(pf), pf_dado=f"{dv_tot}d{dado}" + (f"+{tratti['pf_bonus']}" if tratti["pf_bonus"] else ""),
        ts=_ts_testo(ts), velocita="9 m", iniziativa=f"{m['des']:+d}",
        attributi=" ".join(f"{k.capitalize()} {v}" for k, v in attr.items()),
        attacchi=[_riga_attacco(R, attacco, mod_danno)],
        voci=[f"Talenti: {talento}", f"Debolezza: {debolezza}"],
        tattica=tattica,
    ), conto


# ── il PNG: le tabelle decidono, il collaudo riferisce ──────────────────────

def _genera_png(gs, tipo, taglia, R, classe, elite, conto, rng,
                funzione=None, incantesimi_pf1e=False):
    """Con i livelli di classe il GS non è un bersaglio: è una conseguenza.

    SRD 3.5: un PNG con livelli di classe da PG vale GS = livelli; con le classi
    PNG (warrior, adept, expert, aristocrat, commoner) vale GS = livelli − 1. Se
    il GS chiesto non torna, lo si dice — non si truccano i livelli per farlo
    tornare.
    """
    nome_classe, livelli = classe
    dado_classe, ts_classe = T.CLASSI[nome_classe]
    e_png = nome_classe in T.CLASSI_PNG
    gs_atteso = max(1, livelli - 1 if e_png else livelli)
    conto(f"classe {nome_classe} {livelli} (d{dado_classe}, "
          + ("classe PNG" if e_png else "classe da PG") + f") → GS atteso {gs_atteso}")
    if gs_atteso != gs:
        conto(f"⚠ il GS chiesto ({gs}) non è quello che i livelli producono "
              f"({gs_atteso}). Non tocco i livelli: decide il DM.")

    if elite is None:
        elite = not e_png
    matrice = CAR.ARRAY_ELITE if elite else CAR.ARRAY_STANDARD
    # La scelta sta in `dmcore.caratteristiche.matrice_png`, con i due difetti
    # che l'hanno fatta com'è; qui resta il conto che la racconta.
    lancia_su = T.INCANTATORI[nome_classe][1] if nome_classe in T.INCANTATORI else ""
    attr = {k.lower(): v for k, v in
            CAR.matrice_png(R.profilo, livelli, elite, lancia_su.capitalize()).items()}
    primaria = next(iter(attr))
    del_ruolo = CAR.profilo_esatto(R.profilo)[0].lower()
    if primaria != del_ruolo:
        conto(f"la caratteristica da incantatore ({primaria.upper()}) passa "
              f"davanti a quella del ruolo ({del_ruolo.upper()}): "
              f"{nome_classe} lancia su quella")
    aumenti = attr[primaria] - matrice[0]
    conto(("matrice élite " if elite else "matrice standard ") + str(matrice)
          + (f", +{aumenti} a {primaria.upper()} (SRD: uno ogni 4 livelli)"
             if aumenti else "")
          + " → " + ", ".join(f"{k.upper()} {v}" for k, v in attr.items()))
    m = {k: T.mod(v) for k, v in attr.items()}

    media = T.media_dado(dado_classe) * livelli
    pf = max(1, int(media + m["cos"] * livelli))
    conto(f"pf = {media:.1f} + {m['cos']:+d}×{livelli} = {pf}")

    nat_taglia, mod_taglia = T.TAGLIE[taglia]
    armatura, max_des = _armatura_del_ruolo(R, livelli)
    m_des_usato = min(m["des"], max_des)
    ca = 10 + m_des_usato + nat_taglia + mod_taglia + armatura
    pezzi_ca = [f"{m_des_usato:+d} Des", f"+{armatura} armatura"]
    if nat_taglia:
        pezzi_ca.append(f"+{nat_taglia} naturale")
    if mod_taglia:
        pezzi_ca.append(f"{mod_taglia:+d} taglia")
    conto(f"CA = 10 {' '.join(pezzi_ca)} = {ca}")

    bab = int(T.BAB_CLASSE[nome_classe] * livelli)
    car_attacco = "des" if R.distanza else "for"
    attacco = bab + m[car_attacco] + mod_taglia
    conto(f"attacco = BAB {bab:+d} {m[car_attacco]:+d} {car_attacco.capitalize()}"
          + (f" {mod_taglia:+d} taglia" if mod_taglia else "") + f" = {attacco:+d}")

    ts = _tiri_salvezza(livelli, ts_classe, m, conto)
    voci = []
    if nome_classe in T.INCANTATORI:
        voci += _voci_incantatore(nome_classe, livelli, m, conto, R.nome, rng,
                                  funzione, incantesimi_pf1e)
    if livelli in T.EQUIPAGGIAMENTO_PNG:
        voci.append(f"Equipaggiamento: {T.EQUIPAGGIAMENTO_PNG[livelli]:,} mo "
                    "(colonna «heroic NPC» PF1e)".replace(",", "."))

    _collaudo_png(pf, ca, gs, gs_atteso, R.nome, conto)
    talento, tattica, debolezza = rng.choice(CARATTERE[R.nome])
    ridotto = nome_classe in T.LIVELLO_INCANTATORE_RIDOTTO
    conto.talenti = {"bab": bab, "livelli": {_CLASSE_35_IT.get(nome_classe, nome_classe): livelli},
                     "lic": (max(0, livelli - 3) if ridotto else livelli) if nome_classe in T.INCANTATORI else 0,
                     "dv_razziali": 0, "dv": livelli}
    return Statblocco(
        nome=f"{R.nome} {tipo} {nome_classe} {livelli}",
        gs=str(gs),
        tipo=f"{taglia.capitalize()} {tipo}, {livelli}d{dado_classe}",
        ca=str(ca), ca_dettaglio="(" + ", ".join(pezzi_ca) + ")",
        pf=str(pf), pf_dado=f"{livelli}d{dado_classe}",
        ts=_ts_testo(ts), velocita="9 m", iniziativa=f"{m['des']:+d}",
        attributi=" ".join(f"{k.capitalize()} {v}" for k, v in attr.items()),
        attacchi=[_riga_attacco(R, attacco, 0 if R.distanza else m["for"])],
        voci=voci + [f"Talenti: {talento}", f"Debolezza: {debolezza}"],
        tattica=tattica,
    ), conto


def _armatura_del_ruolo(R: Ruolo, livelli: int) -> tuple[int, int]:
    """Cosa indossa. SRD «Table: Armor and Shields»; lo scudo dove ha senso."""
    if R.nome in ("controllore", "blaster"):
        # ⚠️ Un mago in armatura non lancia — ma non per questo va in giro con
        # CA 11. Difetto trovato costruendo le schede del Bestiario: l'arcimago
        # del Cerchio degli Otto, GS 14, usciva con CA 11, cioè colpito da
        # chiunque con un tiro di 2. Un PNG di quel livello ha **27.000 mo** di
        # equipaggiamento addosso (la tabella EQUIPAGGIAMENTO_PNG lo dice), e la
        # prima cosa che compra un incantatore sono bracciali dell'armatura e un
        # anello di protezione. Non è una concessione: è come si costruisce.
        bracciali = min(8, 1 + livelli // 3)
        anello = min(5, 1 + livelli // 6)
        return bracciali + anello, 99
    if R.nome == "tiratore":
        return T.ARMATURE["studded leather"]
    if R.nome == "schermagliatore":
        return T.ARMATURE["chain shirt"]
    corpo, max_des = T.ARMATURE["breastplate" if livelli < 6 else "full plate"]
    return corpo + T.SCUDI["scudo pesante"], max_des


# ── i pezzi condivisi ───────────────────────────────────────────────────────

def _tiri_salvezza(dv, buoni, m, conto) -> dict[str, int]:
    base = ts_base_di(dv, buoni)
    ts = {}
    for k in ("temp", "rifl", "vol"):
        car = {"temp": "cos", "rifl": "des", "vol": "sag"}[k]
        ts[k] = base[k] + m[car]
    conto("TS = base per DV + modificatore → " + _ts_testo(ts))
    return ts


def _ts_testo(ts: dict[str, int]) -> str:
    return ", ".join(f"{n} {ts[k]:+d}" for k, n in
                     (("temp", "Temp"), ("rifl", "Rifl"), ("vol", "Vol")))


def _riga_attacco(R: Ruolo, attacco: int, mod_danno: int) -> str:
    forma = "Distanza" if R.distanza else "Mischia"
    danno = R.dado_arma + (f"{mod_danno:+d}" if mod_danno else "")
    return f"{forma} {R.arma} {attacco:+d} ({danno})"


def _collaudo(pf: int, ca: int, gs: int, ruolo: str, conto: Conto) -> None:
    bersaglio, verificata = bersaglio_di(gs, ruolo, piu_cattivi=False)
    scarto = (pf - bersaglio["pf"]) / bersaglio["pf"] * 100
    conto(f"collaudo GS {gs}: pf {pf} vs {bersaglio['pf']} ({scarto:+.0f}%), "
          f"CA {ca} vs {bersaglio['ca']} ({ca - bersaglio['ca']:+d})"
          + ("" if verificata else "  ⚠ riga PF1e non verificata"))


def _collaudo_png(pf: int, ca: int, gs: int, gs_atteso: int, ruolo: str,
                  conto: Conto) -> None:
    """Per un PNG con livelli di classe la riga dei mostri NON è il metro giusto.

    Un mago di 9° livello ha davvero una quarantina di punti ferita e CA 11
    senza armatura: è il SRD, non un difetto. Confrontarlo con gli 86 pf di un
    mostro di GS 9 dà −53% e sembra un fallimento, mentre il metro giusto per un
    PNG con classi è uno solo: **i livelli tornano col GS?** Il resto lo fa la
    tabella della classe, che è la fonte.

    La riga dei mostri resta stampata, perché serve a un'altra domanda: *questo
    PNG regge un incontro da solo?* La risposta è quasi sempre no, ed è giusto
    che si veda prima del tavolo invece che durante.
    """
    if gs_atteso == gs:
        conto(f"collaudo PNG: livelli e GS tornano (GS {gs}). "
              "La tabella della classe è la fonte; il resto sono conseguenze.")
    else:
        conto(f"⚠ collaudo PNG: i livelli danno GS {gs_atteso}, non {gs}")
    bersaglio, _ = bersaglio_di(gs, ruolo, piu_cattivi=False)
    conto(f"per confronto, un MOSTRO di GS {gs} avrebbe {bersaglio['pf']} pf e "
          f"CA {bersaglio['ca']}: questo PNG ({pf} pf, CA {ca}) non regge un "
          "incontro da solo, e va accompagnato o protetto")


# ── gli incantesimi scelti ──────────────────────────────────────────────────
# ⚠️ **Qui c'era il difetto che il lotto I chiude.** Le liste stavano in questo
# file, erano tre, ed erano indicizzate per **ruolo tattico**: «controllore» →
# lista arcana, «comandante» → lista divina. Un druido costruito come controllore
# riceveva *armatura magica*, *sonno* e *dito della morte*, che sono da mago; come
# bruto riceveva *benedizione* e *santuario*, che sono da chierico. Separare
# arcano e divino non bastava: chierico e druido sono tutti e due divini e hanno
# liste diverse.
#
# Ora la chiave è **(lista di classe × funzione)** e le liste stanno in
# `dmcore/incantesimi.py`, con l'ancora in `dnd-35-srd/references/spells.md` e un
# test che verifica riga per riga che ogni scelta appartenga a quella classe.
# Sono 400 righe di dati: tenerle qui avrebbe raddoppiato questo file, e il posto
# dei dati in questo repo è `dmcore/`.


def _voci_incantatore(nome_classe: str, livello: int, m: dict[str, int],
                      conto: Conto, ruolo: str = "comandante",
                      rng: random.Random | None = None,
                      funzione: str | None = None,
                      pf1e: bool = False) -> list[str]:
    """Gli incantesimi al giorno, la CD e la scelta, dalle tabelle di classe SRD.

    Il livello dell'incantatore e la CD **non** vengono dalla riga per GS:
    vengono dalla tabella della classe, che è SRD. La riga per GS serve dopo, a
    dire se la CD è dove dovrebbe stare.
    """
    griglia, caratteristica, spontaneo = T.INCANTATORI[nome_classe]
    livello = max(1, min(20, livello))
    slot = griglia[livello]
    # ⚠️ Per ranger e paladino il livello dell'incantatore **non** è il livello
    # di classe: è `livello − 3`. Stampare il livello di classe darebbe un
    # paladino di 12° che «lancia da 12°», e una CD di due punti sbagliata.
    cl = T.livello_incantatore(nome_classe, livello)
    massimo = T.livello_massimo(griglia, livello)
    mod_car = m[caratteristica]

    if cl < 1 or massimo == 0:
        conto(f"{nome_classe} di {livello}° livello: nessun incantesimo — "
              "nel SRD i primi slot arrivano al 4° livello di classe")
        return [f"Nessun incantesimo: un {nome_classe} comincia a lanciare "
                "dal 4° livello di classe"]

    fuori = [f"Incantatore di livello {cl} ({nome_classe}, "
             f"{caratteristica.upper()} {mod_car:+d})"]
    if cl != livello:
        fuori[0] += f" — livello di classe {livello}, meno 3"
    # Ranger e paladino non hanno incantesimi di livello 0, e la loro griglia
    # porta uno zero finto in prima posizione per tenere l'indice allineato: va
    # tolto dalla riga stampata, o il blocco annuncia orisons che non esistono.
    # Il bardo con la tabella PF1e (card del DM del 2026-11-09) ha lo stesso zero
    # finto, perché i suoi trucchetti sono a volontà.
    a_volonta = nome_classe.lower() in T.INCANTATORI_ZERO_A_VOLONTA
    senza_zero = nome_classe.lower() in T.LIVELLO_INCANTATORE_RIDOTTO or a_volonta
    mostrati = slot[1:] if senza_zero else slot
    fuori.append(("Incantesimi al giorno (dal 1° livello): " if senza_zero
                  else "Incantesimi al giorno: ")
                 + "/".join(str(n) for n in mostrati)
                 + (" · trucchetti a volontà" if a_volonta else ""))
    if nome_classe in ("cleric", "chierico"):
        fuori.append("+1 slot per livello dai due domini, una volta scelti")
    if spontaneo:
        conosciuti = (T.BARDO_CONOSCIUTI if nome_classe in ("bard", "bardo")
                      else T.STREGONE_CONOSCIUTI)
        fuori.append("Incantesimi conosciuti: "
                     + "/".join(str(n) for n in conosciuti[livello]))
    cd_max = T.cd_incantesimo(massimo, mod_car)
    fuori.append(f"CD degli incantesimi: 10 + livello + {mod_car:+d} "
                 f"(massimo: {massimo}° livello, CD {cd_max})")
    if spontaneo:
        # SRD: un incantatore spontaneo prende ogni livello d'incantesimo due
        # livelli dopo (2° al 4°, 9° al 18°). A pari livello di classe la sua CD
        # sta un punto o due sotto quella di un preparato, e non è un difetto da
        # correggere: è la classe. Ma se il DM lo mette a fare il blaster di un
        # GS alto e non lo sa, al tavolo scopre un mago che non fa passare nulla.
        fuori.append("⚠ incantatore spontaneo: prende ogni livello d'incantesimo "
                     "due livelli dopo un preparato — per stare sulla stessa CD "
                     "servono ~2 livelli in più")
    fonte_griglia = ("tabella PF1e (scelta del DM, non SRD 3.5)"
                     if nome_classe.lower() in T.INCANTATORI_GRIGLIA_PF1E else "tabella SRD")
    conto(f"incantesimi: {fonte_griglia} di {nome_classe}, livello di classe "
          f"{livello} → incantatore di {cl}°, "
          f"{'/'.join(str(n) for n in mostrati)}; CD massima {cd_max}")
    if nome_classe in T.INCANTATORI_SENZA_ANCORA:
        conto(f"⚠ la griglia di {nome_classe} non ha una riga d'ancora nel repo")

    f_chiesta = INC.funzione_di(ruolo, funzione)
    canonica = INC.CANONICA.get(nome_classe.lower(), nome_classe.lower())
    if canonica in INC.SENZA_LISTA:
        fuori.append(f"⚠ Incantesimi da scegliere a mano: la lista di "
                     f"{nome_classe} non è coperta, e prenderla da un'altra "
                     "classe darebbe incantesimi che questa classe non lancia")
        conto(f"⚠ nessun incantesimo scelto per {nome_classe}: meglio un vuoto "
              "che una lista di un'altra classe")
        return fuori

    _, f_usata = INC.cella(canonica, f_chiesta)
    if f_usata != f_chiesta:
        conto(f"⚠ la cella «{canonica} × {f_chiesta}» non esiste nel gioco: "
              f"ripiegato su «{canonica} × {f_usata}», che è una funzione della "
              "STESSA classe — mai la lista di un'altra")
    scelti, note_pf1e = INC.scegli(canonica, f_usata, slot,
                                   rng or random.Random(), pf1e=pf1e)
    if scelti:
        # Un bardo e uno stregone **non preparano**: conoscono. È una parola, e
        # sul blocco la legge il DM al tavolo mentre decide cosa può lanciare.
        fuori.append(("Conosciuti — " if spontaneo else "Preparati — ")
                     + " · ".join(scelti))
        conto(f"incantesimi dalla lista di **{canonica}**, funzione «{f_usata}» "
              f"(ruolo tattico: {ruolo}) — mai a sorte da tutto il SRD, e mai "
              "dalla lista di un'altra classe")
    for nota in note_pf1e:
        conto.rincaro(f"incantesimo PF1e senza equivalente 3.5 — {nota}; "
                      "va letto sul PRD, non c'è un paragrafo 3.5 su cui "
                      "ripiegare")
    return fuori


def _fonte(gs, tipo, taglia, ruolo, classe, piu_cattivi, conto: Conto,
           funzione=None, incantesimi_pf1e=False) -> str:
    """Da dove viene questa creatura, in una riga che si rilegge fra sei mesi."""
    pezzi = ["generato-SRD-3.5", f"gs={gs}", f"tipo={tipo}", f"taglia={taglia}",
             f"ruolo={ruolo}"]
    if classe:
        pezzi.append(f"classe={classe[0]}:{classe[1]}")
        pezzi.append(f"funzione={INC.funzione_di(ruolo, funzione)}")
        if incantesimi_pf1e:
            pezzi.append("incantesimi=PF1e-senza-equivalente-3.5")
    if piu_cattivi:
        pezzi.append("piu-cattivi=Advanced-PF1e-senza-alzare-il-gs")
    return " ".join(pezzi)


# ===========================================================================
# La riga di comando
# ── PNG PF1e costruiti dalle tabelle del PRD (audit dei plugin, ADR-0121) ──

def genera_png_pf1e(gs: int, *, tipo: str = "humanoid", taglia: str = "medium", ruolo: str = "bruto",
               classi: list[tuple[str, int]], elite: bool | None = None, rng=None,
               funzione: str | None = None, root=None):
    """(statblocco, Conto) di un PNG PF1e costruito dalle tabelle del PRD.

    Tutte le 55 classi di `sistemi/pf1e/dati/classi.toml`, anche in multiclasse
    con le classi di prestigio; i dati e le regole stanno in dmcore/creature_pf1e.py
    (qui, e non lì, per non chiudere un ciclo di import: test_grafo_import_creature)."""
    from dmcore import creature_pf1e as CP
    from dmcore import sistemi as S

    rng = rng or random.Random()
    dati = S.dati("pf1e", "creature.costruzione", root)
    regole = S.dati("pf1e", "creature.conformita", root)
    car_inc = regole.get("incantesimi", {}).get("caratteristica", {})
    R = RUOLI[normalizza_ruolo(ruolo)]
    conto = Conto()
    voci_cl = [(en, liv, dati["classi"][en]) for en, liv in classi]
    totale = sum(liv for _, liv, _ in voci_cl)
    descr = ", ".join(f"{en} {liv}" for en, liv, _ in voci_cl)
    conto(f"PF1e · {descr} · {taglia} · ruolo {R.nome} — classi da sistemi/pf1e/dati/classi.toml (PRD)")

    # GS: PRD, Encounters (sezione 3656): classi senza DV razziali → livelli − 1.
    gs_pf = "1/2" if totale == 1 else str(totale - 1)
    conto(f"GS {gs_pf} = livelli di classe − 1 (PRD, Encounters)"
          + (f"; chiesto GS {gs}, non tocco i livelli: decide il DM" if str(gs) != gs_pf else ""))
    # requisiti d'accesso delle classi di prestigio (lotto 4 delle regole complete):
    # BAB, incantesimi e capacità dalle classi messe prima, talenti presi per primi
    from dmcore import talenti as TL
    obbligati, righe_req = TL.prestigio("pf1e", list(classi), dati)
    for riga in righe_req:
        conto(riga)

    # caratteristiche: matrice eroica se c'è una classe da PG (PRD, Creating NPCs)
    if elite is None:
        elite = any(v["gruppo"] != "png" for _, _, v in voci_cl)
    incantatrici = [en for en, _, _ in voci_cl if en in dati.get("incantatori", {})]
    lancia_su = car_inc.get(incantatrici[0], "") if incantatrici else ""
    attr = {k.lower(): v for k, v in CAR.matrice_png(R.profilo, totale, elite, lancia_su).items()}
    m = {k: CP._mod(v) for k, v in attr.items()}
    conto(("matrice eroica " if elite else "matrice di base ") + "→ "
          + ", ".join(f"{k.upper()} {v}" for k, v in attr.items()))

    # pf: primo dado della prima classe al massimo, gli altri a mezza in su
    rp = regole["punti_ferita"]
    arrot = math.ceil if rp["mezzi_dopo_il_primo"] == "su" else math.floor
    dadi = [(liv, v["dv"]) for _, liv, v in voci_cl]
    primo = dadi[0][1] if rp["primo_dado_di_classe"] == "massimo" else (dadi[0][1] + 1) / 2
    resto = arrot(sum((liv - (1 if i == 0 else 0)) * (f + 1) / 2 for i, (liv, f) in enumerate(dadi)))
    pf = max(1, int(primo + resto + m["cos"] * totale))
    pf_dado = "+".join(f"{liv}d{f}" for liv, f in dadi) + (f"{m['cos'] * totale:+d}" if m["cos"] else "")
    conto(f"pf = {pf_dado}: primo dado {primo:g} + {resto} {m['cos']:+d}×{totale} Cos = {pf} — conformita.toml")

    # BAB e TS: somma per classe (PRD, Multiclassing)
    bab = sum(int(v["bab"] * liv) for _, liv, v in voci_cl)
    base = {k: 0 for k in CP.ORDINE_TS}
    for _, liv, v in voci_cl:
        for k, x in CP.ts_di_classe(liv, v["ts_buoni"], v["gruppo"]).items():
            base[k] += x
    ts = {"temp": base["temp"] + m["cos"], "rifl": base["rifl"] + m["des"], "vol": base["vol"] + m["sag"]}
    ts_testo = ", ".join(f"{CP.NOMI_TS[k]} {ts[k]:+d}" for k in CP.ORDINE_TS)
    conto(f"BAB +{bab}; TS base {base['temp']}/{base['rifl']}/{base['vol']} + caratteristiche → {ts_testo}")

    # CA: armature e scudi PF1e del plugin
    tg = CP.taglia_inglese(taglia, dati["taglie"])
    mod_taglia, mt = dati["taglie"][tg]["ca_attacco"], dati["taglie"][tg]["bmc_dmc"]
    if R.nome in ("controllore", "blaster"):
        armatura, max_des = min(8, 1 + totale // 3) + min(5, 1 + totale // 6), 99
        pezzi = [f"+{armatura} bracciali e anello"]
    else:
        nome_arm = CP.ARMATURA_DEL_RUOLO.get(R.nome, ("breastplate" if totale < 6 else "full plate", None))[0]
        a = dati["armature"][nome_arm]
        armatura, max_des = a["ca"], a["des_max"]
        pezzi = [f"+{a['ca']} {a.get('it', nome_arm)}"]
        if R.nome not in CP.ARMATURA_DEL_RUOLO:
            s = dati["scudi"][CP.SCUDO_PESANTE]
            armatura += s["ca"]
            pezzi.append(f"+{s['ca']} {s.get('it', CP.SCUDO_PESANTE)}")
    arcane = [en for en in incantatrici if car_inc.get(en) in ("Int", "Car")
              and en not in ("paladin", "antipaladin", "oracle")]
    if arcane and R.nome not in ("controllore", "blaster"):
        fall = sum(dati["armature"].get(n, {}).get("fallimento", 0) for n in
                   [CP.ARMATURA_DEL_RUOLO.get(R.nome, ("breastplate" if totale < 6 else "full plate", None))[0]])
        fall += 0 if R.nome in CP.ARMATURA_DEL_RUOLO else dati["scudi"][CP.SCUDO_PESANTE]["fallimento"]
        conto(f"⚠ {', '.join(arcane)} in armatura del ruolo {R.nome}: fallimento degli incantesimi "
              f"arcani {fall}% (PRD), salvo le capacità della classe che lo tolgono")
    m_des = min(m["des"], max_des)
    ca = 10 + m_des + mod_taglia + armatura
    pezzi = [f"{m_des:+d} Des"] + pezzi + ([f"{mod_taglia:+d} taglia"] if mod_taglia else [])
    conto(f"CA = 10 {' '.join(pezzi)} = {ca} — armature del PRD (creature.toml)")

    car_att = "des" if R.distanza else "for"
    attacco = bab + m[car_att] + mod_taglia
    bmc = bab + m["for"] + mt
    dmc = 10 + bab + m["for"] + m["des"] + mt
    gradi = sum(max(1, v["gradi"] + m["int"]) * liv for _, liv, v in voci_cl)
    conto(f"attacco = BAB {bab:+d} {m[car_att]:+d} {car_att.capitalize()} = {attacco:+d}; "
          f"BMC {bmc:+d}, DMC {dmc}; gradi = Σ (gradi + Int) × livelli = {gradi}")

    voci = []
    piu = CP.avanzamento(classi, dati)
    for en in incantatrici:
        liv = dict(classi)[en] + piu.get(en, 0)
        inc = dati["incantatori"][en]
        griglia = dati["griglie"][inc["griglia"]].get(str(min(20, liv)))
        caratt = car_inc.get(en, "Int")
        mod_c = m[caratt.lower()]
        li = CP.livello_incantatore_pf1e(en, liv, dati)
        nome_it = next((k for k, v in dati.get("alias", {}).items() if v == en), en)
        if not griglia or li < 1 or not any(griglia[1:]):
            voci.append(f"Nessun incantesimo da {nome_it} a questo livello")
            continue
        massimo = max(i for i, n in enumerate(griglia) if n)
        voci.append(f"Incantatore di livello {li} ({nome_it}, {caratt.upper()} {mod_c:+d})"
                    + (f" — {piu[en]} livelli dalle classi di prestigio" if piu.get(en) else ""))
        voci.append(CP._riga_slot(griglia, inc["livello_zero"]).replace("Incantesimi", "Estratti")
                    if inc.get("estratti") else CP._riga_slot(griglia, inc["livello_zero"]))
        if inc.get("slot_di_dominio"):
            voci.append("+1 slot per livello (1° in su) dal dominio, una volta scelto")
        slot = griglia
        if inc.get("conosciuti"):
            cono = dati["conosciuti"][inc["conosciuti"]].get(str(min(20, liv)))
            if cono:
                voci.append("Incantesimi conosciuti: " + "/".join(map(str, cono)))
                slot = cono
        voci.append(f"CD degli incantesimi: 10 + livello {mod_c:+d} (massimo: {massimo}° livello, "
                    f"CD {10 + massimo + mod_c})")
        f = INC.funzione_di(R.nome, funzione)
        righe, note = CP.scegli_pf1e(en, list(slot), f, rng, dati, root)
        if righe:
            voci.append(("Conosciuti — " if inc.get("conosciuti") else "Preparati — ") + " · ".join(righe))
        for n in note:
            conto(n)
        conto(f"incantesimi di {en}: griglia PF1e al {min(20, liv)}° = {'/'.join(map(str, griglia))}, "
              f"LI {li}, caratteristica {caratt} — PRD")
    if totale in T.EQUIPAGGIAMENTO_PNG:
        voci.append(f"Equipaggiamento: {T.EQUIPAGGIAMENTO_PNG[totale]:,} mo "
                    "(colonna «heroic NPC» PF1e)".replace(",", "."))
    talento, tattica, debolezza = rng.choice(CARATTERE[R.nome])
    voci += [f"Manovre: BMC {bmc:+d}, DMC {dmc}", f"Gradi di abilità: {gradi}",
             f"Talenti: {talento}", f"Debolezza: {debolezza}"]
    nomi = ", ".join(f"{next((k for k, v in dati.get('alias', {}).items() if v == en), en)} {liv}"
                     for en, liv, _ in voci_cl)
    sb = Statblocco(
        # i livelli stanno nel tipo, non nel nome: il cancello li legge da tutti
        # e due, e scritti due volte li conterebbe due volte
        nome=f"{R.nome} {tipo} " + " / ".join(n.rsplit(" ", 1)[0] for n in nomi.split(", ")),
        gs=gs_pf,
        # «classe N» nel tipo: così il cancello riconosce il PNG con classi
        tipo=f"{taglia.capitalize()} {tipo}, {nomi}",
        ca=str(ca), ca_dettaglio="(" + ", ".join(pezzi) + ")",
        pf=str(pf), pf_dado=pf_dado,
        ts=ts_testo, velocita="9 m", iniziativa=f"{m['des']:+d}",
        attributi=" ".join(f"{k.capitalize()} {v}" for k, v in attr.items()),
        attacchi=[_riga_attacco(R, attacco, 0 if R.distanza else m["for"])],
        voci=voci, tattica=tattica,
        fonte=f"generato-PRD-PF1e gs={gs_pf} tipo={tipo} taglia={taglia} ruolo={R.nome} "
              f"classi={','.join(f'{en}:{liv}' for en, liv in classi)}",
    )
    lic = max([CP.livello_incantatore_pf1e(en, dict(classi)[en] + piu.get(en, 0), dati)
               for en in incantatrici] or [0])
    conto.talenti = {"bab": bab, "livelli": dict(classi), "lic": max(0, lic), "dv_razziali": 0, "dv": totale,
                     "obbligati": obbligati}
    applica_talenti(sb, conto, "pf1e", R.nome, rng)
    return sb, conto


# ===========================================================================

def _classe(testo: str) -> tuple[str, int]:
    nome, _, liv = testo.partition(":")
    nome = nome.strip().lower()
    if nome not in T.CLASSI:
        raise argparse.ArgumentTypeError(
            f"classe ignota: {nome}. Note: {', '.join(sorted(T.CLASSI))}")
    if not liv.strip().isdigit():
        raise argparse.ArgumentTypeError(f"serve «classe:livello», non «{testo}»")
    return nome, int(liv)


def _ruolo(testo: str) -> str:
    nome = normalizza_ruolo(testo)
    if nome not in RUOLI:
        raise argparse.ArgumentTypeError(
            f"ruolo ignoto: {testo}. Noti: {', '.join(sorted(RUOLI))}"
            f" (alias: {', '.join(sorted(ALIAS_RUOLO))})")
    return nome


def _tipo(testo: str) -> str:
    t = T.normalizza_tipo(testo)
    if t is None:
        raise argparse.ArgumentTypeError(
            f"tipo ignoto: {testo}. Noti: {', '.join(sorted(T.TIPI))}")
    return t


def costruisci_parser() -> argparse.ArgumentParser:
    # allow_abbrev=False: nel lotto H `--apply` passava come abbreviazione di
    # `--apply-ts`. Qui `--piu-cattivi` non deve poter essere invocato per sbaglio.
    p = argparse.ArgumentParser(
        description=__doc__.split("\n")[0], allow_abbrev=False,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--gs", type=int, required=True, help="grado di sfida (1-20)")
    p.add_argument("--tipo", type=_tipo, default="humanoid")
    p.add_argument("--taglia", default="medium", choices=sorted(T.TAGLIE))
    p.add_argument("--ruolo", default="bruto", type=_ruolo,
                   help="ruolo tattico: " + ", ".join(sorted(RUOLI))
                        + f" (alias: {', '.join(sorted(ALIAS_RUOLO))})")
    p.add_argument("--funzione", default=None, choices=INC.FUNZIONI,
                   help="funzione da incantatore, se la creatura ha livelli da "
                        "incantatore. Il ruolo dice COME combatte, la funzione "
                        "COSA fa con gli incantesimi: un bruto con livelli da "
                        "chierico è ruolo «bruto» e funzione «supporto». "
                        "Se omessa si deduce dal ruolo")
    p.add_argument("--incantesimi", choices=("srd", "pf1e"), default=None,
                   help="quale lista per gli incantesimi. Di norma SRD 3.5; "
                        "«pf1e» innesta gli incantesimi PF1e che in 3.5 NON "
                        "esistono (uno per livello, elencato nei rincari). "
                        "--piu-cattivi lo accende da sé; questa opzione lo "
                        "separa dal template")
    p.add_argument("--dv", type=int, default=None,
                   help="dadi vita; se omesso, DV ≈ GS con lo scarto del tipo")
    p.add_argument("--classe", default=None,
                   help="livelli di classe, es. «mago:9» o «guerriero:5»; con --sistema pf1e "
                        "tutte le classi del PRD e la multiclasse, es. «mago:5,mistificatore arcano:3»")
    p.add_argument("--elite", action="store_true", default=None,
                   help="forza la matrice élite (15,14,13,12,10,8)")
    p.add_argument("--standard", dest="elite", action="store_false",
                   help="forza la matrice standard (13,12,11,10,9,8)")
    p.add_argument("--piu-cattivi", action="store_true",
                   help="sale ai bersagli PF1e, più duri a pari GS. Ogni rincaro "
                        "è elencato in fonte:. È «--template advanced»")
    p.add_argument("--template", default=None, metavar="NOME", choices=MOD.nomi(),
                   help="un modello semplice di PF1e applicato al blocco finito senza "
                        "cambiare il GS scritto: " + ", ".join(MOD.nomi()) + ". Il blocco "
                        "dice in una voce quanto vale davvero")
    p.add_argument("--sistema", default=None,
                   help="sistema di gioco del blocco (sistemi.toml): pf1e ricalcola dado, BAB, "
                        "TS, BMC/DMC e gradi dal PRD (dmcore/creature_pf1e.py). Se omesso, "
                        "quello della cartella di --in (sistema_di), altrimenti dnd35")
    p.add_argument("--quanti", type=int, default=1)
    p.add_argument("--seed", type=int, default=None,
                   help="per riprodurre la stessa creatura")
    p.add_argument("--json", action="store_true")
    p.add_argument("--in", dest="cartella", type=Path, default=None,
                   help="scrive i blocchi in questa cartella di lavoro. "
                        "Mai dentro Bestiario/: quello lo fa il DM")
    return p


def _rifiuta_bestiario(cartella: Path) -> None:
    """ADR-0033: lo strumento propone, il canone lo scrive il DM.

    Non è una precauzione teorica. Una scheda generata che finisce nel Bestiario
    senza che nessuno l'abbia letta è indistinguibile da una scritta a mano — e
    da quel momento `suggest_encounter` bilancia su di lei.
    """
    bestiario = (ROOT / "Bestiario").resolve()
    dove = cartella.resolve()
    if dove == bestiario or bestiario in dove.parents:
        raise SystemExit(
            "genera_creatura: mi rifiuto di scrivere dentro Bestiario/.\n"
            "  Lo strumento propone; nel canone scrive il DM (ADR-0033).\n"
            "  Usa una cartella di lavoro e ricopia quello che ti convince.")


#: le classi 3.5 del generatore col nome dei dati dei talenti (SRD → italiano)
_CLASSE_35_IT = {"barbarian": "barbaro", "bard": "bardo", "cleric": "chierico", "druid": "druido",
                 "fighter": "guerriero", "monk": "monaco", "paladin": "paladino", "ranger": "ranger",
                 "rogue": "ladro", "sorcerer": "stregone", "wizard": "mago"}


def applica_talenti(sb: Statblocco, conto: Conto, sistema: str, ruolo: str, rng: random.Random) -> None:
    """Sostituisce il «talento firma» con i talenti della regola, e ne applica gli effetti.

    Quanti e quali: `dmcore.talenti` (lotto 3 delle regole complete). Il talento
    firma del carattere resta il primo da provare, ma solo se il PNG lo può prendere.
    """
    from dmcore import talenti as TL

    st = conto.talenti
    if not st:
        return
    attr = {k: int(v) for k, v in re.findall(r"\b(For|Des|Cos|Int|Sag|Car)\s+(\d+)", sb.attributi)}
    firma = next((v.split(":", 1)[1].strip() for v in sb.voci if v.startswith("Talenti:")), None)
    stile = None
    if "ranger" in st["livelli"]:
        stile = "Archery" if ruolo == "tiratore" else "Two-Weapon"
    if "sorcerer" in st["livelli"]:
        stile = "Arcane"
    s = TL.Stato(car=attr, bab=st["bab"], livelli=st["livelli"], lic=st["lic"], dv=st.get("dv", 0))
    if firma and TL.nome_inglese(sistema, firma) and TL.manca(sistema, TL.nome_inglese(sistema, firma), s):
        # il carattere tira un talento che il PNG non può avere: si prende un altro
        # carattere dello stesso ruolo il cui talento è lecito (o non è un talento)
        leciti = [c for c in CARATTERE.get(ruolo, [])
                  if not TL.nome_inglese(sistema, c[0]) or not TL.manca(sistema, TL.nome_inglese(sistema, c[0]), s)]
        if leciti:
            vecchio = firma
            firma, sb.tattica, debolezza = rng.choice(leciti)
            sb.voci = [f"Debolezza: {debolezza}" if v.startswith("Debolezza:") else v for v in sb.voci]
            conto(f"carattere: «{vecchio}» non è lecito per questo PNG, il carattere diventa «{firma}»")
    scelta = TL.scegli(sistema, ruolo, s, dv_razziali=st["dv_razziali"], firma=firma, stile=stile, rng=rng,
                       obbligati=st.get("obbligati"))
    en = [n for n, _ in scelta.talenti]
    m = re.match(r"^(?:Mischia|Distanza)\s+(.+?)\s+[+-]\d+", sb.attacchi[0]) if sb.attacchi else None
    arma = m.group(1) if m else ""
    nomi = []
    for n in en:
        it = TL.italiano(sistema, n)
        if n in ("Weapon Focus", "Weapon Specialization", "Improved Critical", "Greater Weapon Focus") and arma:
            it += f" ({arma})"
        nomi.append(it)
    sb.voci = [v for v in sb.voci if not v.startswith("Talenti:")]
    i = next((k for k, v in enumerate(sb.voci) if v.startswith("Debolezza:")), len(sb.voci))
    sb.voci.insert(i, "Talenti: " + ", ".join(nomi))
    totale = TL.quanti(sistema, st["livelli"], st["dv_razziali"])
    conto(f"talenti: {len(en)} su {totale} della regola ("
          + ("3.5: 1 + 1 ogni 3 livelli" if sistema == "dnd35" else "PF1e: uno ogni livello dispari")
          + ", più bonus e concessi delle classi) — " + "; ".join(f"{TL.italiano(sistema, n)} [{o}]"
                                                                 for n, o in scelta.talenti))
    for nota in scelta.note:
        conto(f"talenti: {nota}")
    senza_it = [n for n in en if TL.italiano(sistema, n) == n]
    if senza_it:
        conto(f"talenti senza nome italiano nel lessico, lasciati in inglese: {', '.join(senza_it)}")
    e = TL.effetti(sistema, en, st["dv"])
    if e["iniziativa"]:
        sb.iniziativa = f"{int(sb.iniziativa) + e['iniziativa']:+d}"
    if e["pf"]:
        sb.pf = str(int(sb.pf) + e["pf"])
        sb.pf_dado = (sb.pf_dado + f"+{e['pf']}") if "+" not in sb.pf_dado else re.sub(
            r"\+(\d+)$", lambda x: f"+{int(x.group(1)) + e['pf']}", sb.pf_dado)
    for chiave, sigla in (("temp", "Temp"), ("rifl", "Rifl"), ("vol", "Vol")):
        if e[chiave]:
            sb.ts = re.sub(rf"{sigla} ([+-]\d+)", lambda x: f"{sigla} {int(x.group(1)) + e[chiave]:+d}", sb.ts)
    if e["attacco"] and sb.attacchi:
        sb.attacchi[0] = re.sub(r"(\s)([+-]\d+)(\s*\()", lambda x: f"{x.group(1)}{int(x.group(2)) + e['attacco']:+d}{x.group(3)}",
                                sb.attacchi[0], count=1)
    if e["ca"]:
        sb.ca = str(int(sb.ca) + e["ca"])
        sb.ca_dettaglio = sb.ca_dettaglio.rstrip(")") + f", +{e['ca']} schivare)"
    if any(e.values()):
        conto("effetti dei talenti sui numeri: " + ", ".join(f"{k} {v:+d}" for k, v in e.items() if v))


def main(argv: list[str] | None = None) -> int:
    args = costruisci_parser().parse_args(argv)
    if not 1 <= args.gs <= 20:
        raise SystemExit("genera_creatura: il GS sta fra 1 e 20")
    if args.cartella:
        _rifiuta_bestiario(args.cartella)
        args.cartella.mkdir(parents=True, exist_ok=True)

    if args.sistema is None:
        # F4 di ADR-0112: il blocco si scrive nel sistema della cartella in cui va
        from dmcore import sistemi as S
        args.sistema = S.sistema_di(args.cartella) if args.cartella else "dnd35"
    if args.sistema != "dnd35":
        from dmcore import sistemi as S
        if args.sistema not in S.attivi():
            raise SystemExit(f"genera_creatura: sistema «{args.sistema}» non attivo in sistemi.toml")
        if args.sistema != "pf1e":
            raise SystemExit(f"genera_creatura: nessuna conversione per «{args.sistema}»")
        from dmcore import creature_pf1e as CP
        if args.classe and args.template:
            raise SystemExit("genera_creatura: --template su un PNG PF1e con classe non è "
                             "ancora gestito (BMC e DMC non si ricalcolano); funziona sui "
                             "mostri e sui blocchi 3.5")
        if args.classe:
            # PF1e: costruito dalle tabelle del PRD (classi.toml), per tutte le
            # classi e in multiclasse, non portato dal 3.5
            try:
                classi_pf1e = CP.leggi_classi(args.classe, S.dati("pf1e", "creature.costruzione"))
            except ValueError as e:
                raise SystemExit(f"genera_creatura: {e}")
            rng = random.Random(args.seed)
            fuori = [genera_png_pf1e(args.gs, tipo=args.tipo, taglia=args.taglia, ruolo=args.ruolo,
                                   classi=classi_pf1e, elite=args.elite, rng=rng,
                                   funzione=args.funzione) for _ in range(args.quanti)]
            return _stampa(fuori, args)
    if args.sistema == "dnd35" and args.classe:
        try:
            args.classe = _classe(args.classe)
        except argparse.ArgumentTypeError as e:
            raise SystemExit(f"genera_creatura: {e}")

    rng = random.Random(args.seed)
    fuori = []
    if args.template and args.piu_cattivi and args.template != "advanced":
        raise SystemExit("genera_creatura: --piu-cattivi è --template advanced, non si "
                         f"somma a --template {args.template}")
    for i in range(args.quanti):
        try:
            sb, conto = genera(args.gs, tipo=args.tipo, taglia=args.taglia,
                               ruolo=args.ruolo, dv=args.dv, elite=args.elite,
                               classe=args.classe, piu_cattivi=args.piu_cattivi,
                               modello=args.template,
                               rng=rng, funzione=args.funzione,
                               incantesimi_pf1e=(None if args.incantesimi is None
                                                 else args.incantesimi == "pf1e"),
                               talenti=None if args.sistema == "pf1e" else "dnd35")
        except MOD.ModelloVietato as e:
            raise SystemExit(f"genera_creatura: {e}")
        if args.sistema == "pf1e":
            # un modello può aver cambiato la taglia: si converte quella del blocco
            sb, righe = CP.converti(sb, args.tipo, MOD.taglia_di(sb) if args.template
                                    else args.taglia, pf_bersaglio=bersaglio_di(
                args.gs, normalizza_ruolo(args.ruolo), piu_cattivi=False)[0]["pf"])
            conto.righe.extend(righe)
            if conto.talenti and not conto.talenti.get("livelli"):
                # BAB PF1e del tipo, non quello 3.5
                voce = S.dati("pf1e", "creature.costruzione")["tipi"].get(args.tipo, {})
                if voce:
                    conto.talenti["bab"] = int(voce["bab"] * conto.talenti["dv"])
            applica_talenti(sb, conto, "pf1e", normalizza_ruolo(args.ruolo), rng)
        fuori.append((sb, conto))
    return _stampa(fuori, args)


def _stampa(fuori, args) -> int:
    if args.json:
        print(json.dumps([{"blocco": rendi(sb), "conto": c.righe,
                           "rincari": c.rincari} for sb, c in fuori],
                         ensure_ascii=False, indent=2))
        return 0

    for i, (sb, conto) in enumerate(fuori, 1):
        if args.quanti > 1:
            print(f"\n─── {i} di {args.quanti} " + "─" * 40)
        print(rendi(sb))
        print("\nIl conto:")
        for riga in conto.righe:
            print(f"  · {riga}")
        if conto.rincari:
            print("\nI rincari (variante più cattiva):")
            for riga in conto.rincari:
                print(f"  → {riga}")
        if args.cartella:
            f = args.cartella / f"gs{args.gs}-{args.ruolo}-{i}.md"
            f.write_text(f"# {sb.nome}\n\n{rendi(sb)}\n", encoding="utf-8")
            print(f"\nscritto: {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
