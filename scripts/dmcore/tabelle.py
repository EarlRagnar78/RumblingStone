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

#: tipo → (faccia del dado dei DV, BAB per DV, tiri salvezza buoni)
TIPI = {
    "aberration":         (8,  0.75, ("vol",)),
    "animal":             (8,  0.75, ("temp", "rifl")),
    "construct":          (10, 0.75, ()),
    "dragon":             (12, 1.0,  ("temp", "rifl", "vol")),
    "elemental":          (8,  0.75, ("rifl",)),
    "fey":                (6,  0.5,  ("rifl", "vol")),
    "giant":              (8,  0.75, ("temp",)),
    "humanoid":           (8,  0.75, ("temp",)),
    "magical beast":      (10, 1.0,  ("temp", "rifl")),
    "monstrous humanoid": (8,  1.0,  ("rifl", "vol")),
    "ooze":               (10, 0.75, ()),
    "outsider":           (8,  1.0,  ("temp", "rifl", "vol")),
    "plant":              (8,  0.75, ("temp",)),
    "undead":             (12, 0.5,  ("vol",)),
    "vermin":             (8,  0.75, ("temp",)),
}

#: Come il tipo si scrive nelle schede — italiano, inglese, e le forme miste.
ALIAS_TIPO = {
    "aberrazione": "aberration", "animale": "animal", "costrutto": "construct",
    "drago": "dragon", "elementale": "elemental", "folletto": "fey",
    "gigante": "giant", "umanoide": "humanoid", "bestia magica": "magical beast",
    "umanoide mostruoso": "monstrous humanoid", "melma": "ooze",
    "esterno": "outsider", "pianta": "plant", "non-morto": "undead",
    "nonmorto": "undead", "parassita": "vermin", "immondo": "outsider",
    "tiefling": "outsider", "mezzodrago": "dragon",
}

#: classe → (faccia del dado dei DV, tiri salvezza buoni). Le classi PNG del SRD
#: (warrior, adept, expert, aristocrat, commoner) stanno qui come le altre: sono
#: SRD a tutti gli effetti, ed è con quelle che si fa il fondale.
CLASSI = {
    "barbarian": (12, ("temp",)),        "barbaro":    (12, ("temp",)),
    "bard":      (6,  ("rifl", "vol")),  "bardo":      (6,  ("rifl", "vol")),
    "cleric":    (8,  ("temp", "vol")),  "chierico":   (8,  ("temp", "vol")),
    "druid":     (8,  ("temp", "vol")),  "druido":     (8,  ("temp", "vol")),
    "fighter":   (10, ("temp",)),        "guerriero":  (10, ("temp",)),
    "monk":      (8,  ("temp", "rifl", "vol")),
    "monaco":    (8,  ("temp", "rifl", "vol")),
    "paladin":   (10, ("temp",)),        "paladino":   (10, ("temp",)),
    "ranger":    (8,  ("temp", "rifl")),
    "rogue":     (6,  ("rifl",)),        "ladro":      (6,  ("rifl",)),
    "sorcerer":  (4,  ("vol",)),         "stregone":   (4,  ("vol",)),
    "wizard":    (4,  ("vol",)),         "mago":       (4,  ("vol",)),
    "warrior":   (8,  ("temp",)),        "guerriero-png": (8, ("temp",)),
    "adept":     (6,  ("vol",)),         "adepto":     (6,  ("vol",)),
    "expert":    (6,  ("vol",)),         "esperto":    (6,  ("vol",)),
    "aristocrat": (8, ("vol",)),         "aristocratico": (8, ("vol",)),
    "commoner":  (4,  ()),               "popolano":   (4,  ()),
}

#: Le classi PNG del SRD. Contano meno per il GS, ed è il loro scopo.
CLASSI_PNG = frozenset({"warrior", "guerriero-png", "adept", "adepto", "expert",
                        "esperto", "aristocrat", "aristocratico", "commoner",
                        "popolano"})

#: BAB per livello di classe.
BAB_CLASSE = {
    "barbarian": 1.0, "barbaro": 1.0, "fighter": 1.0, "guerriero": 1.0,
    "paladin": 1.0, "paladino": 1.0, "ranger": 1.0, "warrior": 1.0,
    "guerriero-png": 1.0,
    "bard": 0.75, "bardo": 0.75, "cleric": 0.75, "chierico": 0.75,
    "druid": 0.75, "druido": 0.75, "monk": 0.75, "monaco": 0.75,
    "rogue": 0.75, "ladro": 0.75, "expert": 0.75, "esperto": 0.75,
    "aristocrat": 0.75, "aristocratico": 0.75,
    "sorcerer": 0.5, "stregone": 0.5, "wizard": 0.5, "mago": 0.5,
    "adept": 0.5, "adepto": 0.5, "commoner": 0.5, "popolano": 0.5,
}

#: taglia → (armatura naturale tipica, modificatore di CA e attacco)
TAGLIE = {
    "fine": (0, +8), "diminutive": (0, +4), "minuta": (0, +4),
    "tiny": (0, +2), "minuscola": (0, +2),
    "small": (0, +1), "piccola": (0, +1),
    "medium": (0, 0), "media": (0, 0),
    "large": (2, -1), "grande": (2, -1),
    "huge": (5, -2), "enorme": (5, -2),
    "gargantuan": (9, -4), "mastodontica": (9, -4),
    "colossal": (14, -8), "colossale": (14, -8),
}

#: armatura → (bonus di CA, massimo di Destrezza)
ARMATURE = {
    "full plate": (8, 1), "piastre": (8, 1), "fullplate": (8, 1),
    "half-plate": (7, 0), "mezza piastra": (7, 0),
    "breastplate": (5, 3), "corazza": (5, 3),
    "chainmail": (5, 2), "cotta di maglia": (5, 2),
    "chain shirt": (4, 4), "camicia di maglia": (4, 4), "maglia": (4, 4),
    "scale mail": (4, 3), "scaglie": (4, 3),
    "studded leather": (3, 5), "cuoio borchiato": (3, 5),
    "leather": (2, 6), "cuoio": (2, 6),
    "padded": (1, 8), "imbottita": (1, 8),
}
SCUDI = {"heavy shield": 2, "scudo pesante": 2, "tower": 4, "torre": 4,
         "light shield": 1, "scudo leggero": 1, "buckler": 1, "brocchiere": 1,
         "shield": 2, "scudo": 2}

#: Le due matrici. Identiche fra SRD 3.5 e PF1e — una sola per tutti e due.
ELITE = (15, 14, 13, 12, 10, 8)
BASIC = (13, 12, 11, 10, 9, 8)

#: Chi merita la matrice elite: chi ha un nome, chi comanda, chi è un boss. Il
#: fondale prende quella standard, ed è il punto — un mook con le caratteristiche
#: di un luogotenente non è un mook, è un secondo luogotenente.
RUOLI_ELITE = ("boss", "elite", "villain", "commander", "captain", "lieutenant",
               "alfa", "leader", "mastermind", "officer", "ally", "caster")


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

def _griglia(testo: str) -> dict[int, tuple[int, ...]]:
    fuori = {}
    for riga in testo.strip().splitlines():
        liv, _, slot = riga.partition(":")
        fuori[int(liv)] = tuple(int(n) for n in slot.split())
    return fuori


#: SRD «Table: The Wizard». Ancore verificate in repo: livelli 1, 5, 10, 15, 20
#: (`dnd-35-srd/references/classes.md` §Wizard).
MAGO = _griglia("""
1: 3 1
2: 4 2
3: 4 2 1
4: 4 3 2
5: 4 3 2 1
6: 4 3 3 2
7: 4 4 3 2 1
8: 4 4 3 3 2
9: 4 4 4 3 2 1
10: 4 4 4 3 3 2
11: 4 4 4 4 3 2 1
12: 4 4 4 4 3 3 2
13: 4 4 4 4 4 3 2 1
14: 4 4 4 4 4 3 3 2
15: 4 4 4 4 4 4 3 2 1
16: 4 4 4 4 4 4 3 3 2
17: 4 4 4 4 4 4 4 3 2 1
18: 4 4 4 4 4 4 4 3 3 2
19: 4 4 4 4 4 4 4 4 3 3
20: 4 4 4 4 4 4 4 4 4 4
""")

#: SRD «Table: The Sorcerer». Ancore verificate in repo: 1, 5, 10, 15, 20.
STREGONE = _griglia("""
1: 5 3
2: 6 4
3: 6 5
4: 6 6 3
5: 6 6 4
6: 6 6 5 3
7: 6 6 6 4
8: 6 6 6 5 3
9: 6 6 6 6 4
10: 6 6 6 6 5 3
11: 6 6 6 6 6 4
12: 6 6 6 6 6 5 3
13: 6 6 6 6 6 6 4
14: 6 6 6 6 6 6 5 3
15: 6 6 6 6 6 6 6 4
16: 6 6 6 6 6 6 6 5 3
17: 6 6 6 6 6 6 6 6 4
18: 6 6 6 6 6 6 6 6 5 3
19: 6 6 6 6 6 6 6 6 6 4
20: 6 6 6 6 6 6 6 6 6 6
""")

#: SRD «Table: Sorcerer Spells Known». Ancore verificate: 1, 5, 10, 15, 20.
#: Serve perché uno stregone non prepara: la lista è la creatura.
STREGONE_CONOSCIUTI = _griglia("""
1: 4 2
2: 5 2
3: 5 3
4: 6 3 1
5: 6 4 2
6: 7 4 2 1
7: 7 5 3 2
8: 8 5 3 2 1
9: 8 5 4 3 2
10: 9 5 4 3 2 1
11: 9 5 5 4 3 2
12: 9 5 5 4 3 2 1
13: 9 5 5 4 4 3 2
14: 9 5 5 4 4 3 2 1
15: 9 5 5 4 4 4 3 2
16: 9 5 5 4 4 4 3 2 1
17: 9 5 5 4 4 4 3 3 2
18: 9 5 5 4 4 4 3 3 2 1
19: 9 5 5 4 4 4 3 3 3 2
20: 9 5 5 4 4 4 3 3 3 3
""")

#: SRD «Table: The Cleric» e «Table: The Druid» — la griglia è la stessa. Per il
#: chierico va aggiunto **+1 slot per livello** quando i domini sono scelti.
CHIERICO = _griglia("""
1: 3 1
2: 4 2
3: 4 2 1
4: 5 3 2
5: 5 3 2 1
6: 5 3 3 2
7: 6 4 3 2 1
8: 6 4 3 3 2
9: 6 4 4 3 2 1
10: 6 4 4 3 3 2
11: 6 5 4 4 3 2 1
12: 6 5 4 4 3 3 2
13: 6 5 5 4 4 3 2 1
14: 6 5 5 4 4 3 3 2
15: 6 5 5 5 4 4 3 2 1
16: 6 5 5 5 4 4 3 3 2
17: 6 5 5 5 5 4 4 3 2 1
18: 6 5 5 5 5 4 4 3 3 2
19: 6 5 5 5 5 5 4 4 3 3
20: 6 5 5 5 5 5 4 4 4 4
""")
DRUIDO = CHIERICO

#: SRD «Table: The Adept» — la classe PNG incantatrice, che arriva al 5° livello
#: d'incantesimo e non oltre. ⚠️ Non ha un'ancora in repo come le altre: è
#: dichiarata in `INCANTATORI_SENZA_ANCORA` e chi la usa lo sa.
ADEPTO = _griglia("""
1: 3 1
2: 3 1
3: 3 2
4: 3 2 0
5: 3 2 1
6: 3 2 1
7: 3 3 2
8: 3 3 2 0
9: 3 3 2 1
10: 3 3 3 1
11: 3 3 3 2
12: 3 3 3 2 0
13: 3 3 3 2 1
14: 3 3 3 3 1
15: 3 3 3 3 2
16: 3 3 3 3 2 0
17: 3 3 3 3 2 1
18: 3 3 3 3 3 1
19: 3 3 3 3 3 2
20: 3 3 3 3 3 3
""")

#: SRD «Table: The Bard» — l'incantatore ibrido, spontaneo, che si ferma al 6°
#: livello d'incantesimo. Ancore verificate in repo: 1, 5, 10, 15, 20
#: (`dnd-35-srd/references/classes.md` §Bard).
#: ⚠️ Il bardo serve davvero: `Bestiario/png/lomyn-redtongue-bardo4-cr3.md` è un
#: bardo, e fino al lotto I il generatore non sapeva costruirlo.
BARDO = _griglia("""
1: 2
2: 3 0
3: 3 1
4: 3 2 0
5: 3 3 1
6: 3 3 2
7: 3 3 2 0
8: 3 3 3 1
9: 3 3 3 2
10: 3 3 3 2 0
11: 3 3 3 3 1
12: 3 3 3 3 2
13: 3 3 3 3 2 0
14: 4 3 3 3 3 1
15: 4 4 3 3 3 2
16: 4 4 4 3 3 2 0
17: 4 4 4 4 3 3 1
18: 4 4 4 4 4 3 2
19: 4 4 4 4 4 4 3
20: 4 4 4 4 4 4 4
""")

#: SRD «Table: Bard Spells Known». Come per lo stregone: un bardo non prepara,
#: e la lista **è** la creatura.
BARDO_CONOSCIUTI = _griglia("""
1: 4 2
2: 5 3
3: 6 4
4: 6 4 2
5: 6 4 3
6: 6 4 4
7: 6 5 4 2
8: 6 5 4 3
9: 6 5 4 4
10: 6 5 5 4 2
11: 6 6 5 4 3
12: 6 6 5 4 4
13: 6 6 5 5 4 2
14: 6 6 6 5 4 3
15: 6 6 6 5 4 4
16: 6 6 6 5 5 4 2
17: 6 6 6 6 5 4 3
18: 6 6 6 6 5 4 4
19: 6 6 6 6 5 5 4
20: 6 6 6 6 6 5 4
""")

#: SRD «Table: The Ranger» e «Table: The Paladin» — la griglia è **la stessa**,
#: come lo è quella di chierico e druido. Due cose la rendono diversa da tutte le
#: altre di questo file, e chi la legge deve saperle:
#:
#:   * non c'è la colonna degli incantesimi di livello 0 (ranger e paladino non
#:     ne hanno), e la prima cifra di ogni riga è quindi lo **0 finto** che tiene
#:     l'indice allineato con le altre griglie;
#:   * il **livello dell'incantatore non è il livello di classe**: è
#:     `livello − 3` (`LIVELLO_INCANTATORE_RIDOTTO`). Un paladino di 12° lancia
#:     da incantatore di 9°, e la sua CD si calcola su quello.
#:
#: Sotto il 4° livello di classe non lanciano nulla, e la riga lo dice con una
#: griglia di soli zeri invece che con un'assenza: un'assenza andrebbe gestita da
#: chi chiama, e prima o poi qualcuno se ne dimenticherebbe.
RANGER = _griglia("""
1: 0
2: 0
3: 0
4: 0 0
5: 0 1
6: 0 1
7: 0 1 0
8: 0 1 1
9: 0 2 1
10: 0 2 1 0
11: 0 2 1 1
12: 0 2 2 1
13: 0 3 2 1 0
14: 0 3 2 1 1
15: 0 3 2 2 1
16: 0 3 3 2 1
17: 0 4 3 2 1
18: 0 4 3 2 2
19: 0 4 3 3 2
20: 0 4 3 3 3
""")
PALADINO = RANGER

#: Le classi il cui livello dell'incantatore **non** coincide col livello di
#: classe. Nel SRD sono queste due, e la regola è la stessa: `livello − 3`, con
#: un minimo di 1 e un massimo di 4° livello d'incantesimo.
LIVELLO_INCANTATORE_RIDOTTO = frozenset({"ranger", "paladin", "paladino"})

#: classe incantatrice → (griglia, caratteristica primaria, spontaneo?)
INCANTATORI = {
    "wizard":   (MAGO, "int", False),   "mago":      (MAGO, "int", False),
    "sorcerer": (STREGONE, "car", True), "stregone": (STREGONE, "car", True),
    "cleric":   (CHIERICO, "sag", False), "chierico": (CHIERICO, "sag", False),
    "druid":    (DRUIDO, "sag", False),  "druido":   (DRUIDO, "sag", False),
    "adept":    (ADEPTO, "sag", False),  "adepto":   (ADEPTO, "sag", False),
    "bard":     (BARDO, "car", True),   "bardo":     (BARDO, "car", True),
    # ⚠️ Ranger e paladino lanciano su **Saggezza**, non su Carisma. È la
    # differenza che il repo aveva sbagliata: `classes.md` diceva «CHA-based»
    # per il paladino, che è la regola di **PF1e**. Nel SRD 3.5 il Carisma del
    # paladino gli serve per Grazia Divina, Imposizione delle Mani e Punizione;
    # la CD dei suoi incantesimi è 10 + livello + modificatore di Saggezza.
    # Prenderla per Carisma avrebbe prodotto paladini con la CD sbagliata e la
    # caratteristica sbagliata al primo posto della matrice élite.
    "ranger":   (RANGER, "sag", False),
    "paladin":  (PALADINO, "sag", False), "paladino": (PALADINO, "sag", False),
}

#: Le griglie che NON hanno una riga d'ancora nel repo. Usarle è lecito; farlo
#: senza dirlo no.
INCANTATORI_SENZA_ANCORA = frozenset({"adept", "adepto"})

#: Il livello dell'incantatore per una classe e un livello di classe. Per quasi
#: tutti è lo stesso numero; per ranger e paladino è `livello − 3`, e chiamare
#: questa funzione invece di usare il livello di classe è ciò che evita di
#: stampare «incantatore di livello 12» per un paladino che lancia da 9°.
def livello_incantatore(classe: str, livello_classe: int) -> int:
    if classe.lower() in LIVELLO_INCANTATORE_RIDOTTO:
        return max(0, livello_classe - 3)
    return livello_classe

#: I livelli che il test confronta con le ancore delle skill.
ANCORE = (1, 5, 10, 15, 20)


def livello_massimo(griglia: dict[int, tuple[int, ...]], livello: int) -> int:
    """Il livello d'incantesimo più alto che questo incantatore lancia."""
    slot = griglia[max(1, min(20, livello))]
    alti = [i for i, n in enumerate(slot) if n > 0]
    return max(alti) if alti else 0


def cd_incantesimo(livello_incantesimo: int, modificatore: int) -> int:
    """SRD: CD = 10 + livello dell'incantesimo + modificatore di caratteristica."""
    return 10 + livello_incantesimo + modificatore


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

def mod(punteggio: int) -> int:
    return (punteggio - 10) // 2


def ts_buono(dv: int) -> int:
    return 2 + dv // 2


def ts_cattivo(dv: int) -> int:
    return dv // 3


def media_dado(faccia: int) -> float:
    """La media di un dado come la conta il SRD per i PNG: (faccia / 2) + 0,5."""
    return faccia / 2 + 0.5


def normalizza_tipo(testo: str) -> str | None:
    """Il tipo di creatura, comunque sia scritto nella scheda."""
    t = (testo or "").strip().lower()
    if t in TIPI:
        return t
    if t in ALIAS_TIPO:
        return ALIAS_TIPO[t]
    for chiave in sorted(TIPI, key=len, reverse=True):
        if chiave in t:
            return chiave
    for alias in sorted(ALIAS_TIPO, key=len, reverse=True):
        if alias in t:
            return ALIAS_TIPO[alias]
    return None
