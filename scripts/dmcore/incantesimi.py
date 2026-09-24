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
CANONICA = {
    "wizard": "mago", "mago": "mago",
    "sorcerer": "stregone", "stregone": "stregone",
    "cleric": "chierico", "chierico": "chierico",
    "druid": "druido", "druido": "druido",
    "bard": "bardo", "bardo": "bardo",
    "ranger": "ranger",
    "paladin": "paladino", "paladino": "paladino",
    "adept": "adepto", "adepto": "adepto",
}

# ===========================================================================
# Le liste, per lista di classe × funzione
# ===========================================================================
# Ogni voce è presa dall'ancora in `dnd-35-srd/references/spells.md`, per quella
# classe e quel livello. Poche voci per livello, ed è voluto: sono gli
# incantesimi che quella funzione lancerebbe davvero, non tutto il SRD.

#: Lista arcana, condivisa fra mago e stregone (SRD «Sorcerer/Wizard Spells»).
_ARCANO = {
    "controllore": {
        0: ["prestidigitazione", "luce", "lettura del magico", "mano magica"],
        1: ["sonno", "charme su persone", "spruzzo di colori",
            "raggio di indebolimento", "grasso"],
        2: ["immagine speculare", "ragnatela", "polvere scintillante",
            "risata incontenibile di Tasha", "tocco della stupidità"],
        3: ["lentezza", "blocca persone", "nube maleodorante",
            "tempesta di nevischio", "suggestione"],
        4: ["confusione", "muro di fuoco", "terreno illusorio",
            "porta dimensionale", "charme su mostri"],
        5: ["muro di forza", "dominare persone", "blocca mostri",
            "nube mortale", "deficienza"],
        6: ["campo antimagia", "cerchio della morte", "nube acida",
            "muro di ferro", "repulsione"],
        7: ["gabbia di forza", "follia", "spruzzo prismatico",
            "inversione della gravità", "blocca persone di massa"],
        8: ["labirinto", "danza irresistibile di Otto", "muro prismatico",
            "schermo mentale", "parola del potere: stordire"],
        9: ["prigione", "arresto del tempo", "dominare mostri",
            "sfera prismatica", "disgiunzione di Mordenkainen"],
    },
    "blaster": {
        0: ["raggio di gelo", "luce", "mano magica", "bagliore"],
        1: ["dardo incantato", "mani brucianti", "spruzzo di colori"],
        2: ["raggio rovente", "freccia acida di Melf", "frantumare"],
        3: ["palla di fuoco", "fulmine", "tempesta di nevischio"],
        4: ["tempesta di ghiaccio", "muro di fuoco", "prosciugare",
            "scudo di fuoco"],
        5: ["cono di freddo", "nube mortale", "telecinesi", "evocare mostri V"],
        6: ["catena di fulmini", "disintegrazione",
            "sfera congelante di Otiluke", "cerchio della morte"],
        7: ["palla di fuoco ritardata", "dito della morte",
            "spruzzo prismatico", "spada arcana"],
        8: ["avvizzimento orrendo", "nube incendiaria", "raggio polare",
            "esplosione solare", "urlo superiore"],
        9: ["meteore", "parola del potere: uccidere", "urlo della banshee",
            "prosciugamento di energia"],
    },
    "utilita": {
        0: ["prestidigitazione", "individuazione del magico",
            "lettura del magico", "luce"],
        1: ["armatura magica", "scudo", "allarme", "caduta morbida"],
        2: ["invisibilità", "sfocatura", "nube di nebbia",
            "resistere all'energia", "individuazione dei pensieri"],
        3: ["volare", "dissolvi magie", "spostamento", "forma gassosa",
            "velocità"],
        4: ["invisibilità superiore", "pelle di pietra", "occhio arcano",
            "porta dimensionale", "polimorfismo"],
        5: ["teletrasporto", "passapareti", "mano interposta di Bigby",
            "muro di pietra", "metamorfosi funesta"],
        6: ["dissolvi magie superiore", "globo d'invulnerabilità",
            "visione del vero", "carne in pietra", "occhio maligno"],
        7: ["teletrasporto superiore", "deviazione degli incantesimi",
            "esilio", "desiderio limitato"],
        8: ["corpo di ferro", "schermo mentale", "pugno serrato",
            "muro prismatico"],
        9: ["preveggenza", "porta", "desiderio",
            "disgiunzione di Mordenkainen"],
    },
}

LISTE: dict[str, dict[str, dict[int, list[str]]]] = {
    # ── arcano ──────────────────────────────────────────────────────────────
    # Mago e stregone puntano allo **stesso oggetto**, e deve restare così: nel
    # SRD hanno la stessa lista, e due copie divergerebbero al primo ritocco.
    "mago": _ARCANO,
    "stregone": _ARCANO,

    # ── divino: chierico ────────────────────────────────────────────────────
    "chierico": {
        "controllore": {
            0: ["guida", "individuazione del magico", "resistenza", "luce"],
            1: ["comando", "santuario", "protezione dal male", "scudo entropico"],
            2: ["blocca persone", "silenzio", "oscurità", "calmare emozioni",
                "zona di verità"],
            3: ["cecità/sordità", "infliggere maledizione", "glifo di interdizione",
                "elusione dell'invisibilità", "muro di vento"],
            4: ["congedo", "ancora dimensionale", "veleno", "divinazione"],
            5: ["comando superiore", "uccidere i viventi", "piaga d'insetti",
                "muro di pietra"],
            6: ["esilio", "barriera di lame", "animare oggetti",
                "parola del richiamo"],
            7: ["distruzione", "repulsione", "bestemmia", "dettame",
                "parola del caos"],
            8: ["blocco dimensionale", "simbolo di morte", "campo antimagia",
                "manto del caos"],
            9: ["implosione", "legare l'anima", "porta", "tempesta di vendetta"],
        },
        "blaster": {
            0: ["individuazione del magico", "guida", "luce", "riparare"],
            1: ["infliggere ferite leggere", "favore divino", "arma magica",
                "benedizione"],
            2: ["arma spirituale", "forza del toro", "aiuto", "oscurità"],
            3: ["luce bruciante", "dissolvi magie", "cura ferite gravi",
                "animare morti"],
            4: ["potere divino", "arma magica superiore", "veleno",
                "cura ferite gravi"],
            5: ["colonna di fuoco", "uccidere i viventi", "potenza virtuosa",
                "scacciare il male"],
            6: ["danno", "barriera di lame", "dissolvi magie superiore", "esilio"],
            7: ["parola sacra", "distruzione", "controllare il clima", "bestemmia"],
            8: ["tempesta di fuoco", "terremoto", "aura sacra", "simbolo di morte"],
            9: ["implosione", "prosciugamento di energia", "tempesta di vendetta",
                "miracolo"],
        },
        "supporto": {
            0: ["cura ferite minime", "guida", "resistenza", "virtù"],
            1: ["benedizione", "scudo della fede", "cura ferite leggere",
                "rimuovi paura", "santuario"],
            2: ["aiuto", "resistere all'energia", "cura ferite moderate",
                "forza del toro", "saggezza del gufo", "ristorare inferiore"],
            3: ["preghiera", "cura ferite gravi", "paramento magico",
                "protezione dall'energia"],
            4: ["libertà di movimento", "immunità agli incantesimi", "ristorare",
                "cura ferite gravi", "protezione dalla morte"],
            5: ["cura ferite leggere di massa", "potenza virtuosa",
                "resistenza agli incantesimi", "spezzare incantesimo",
                "rianimare morti"],
            6: ["guarigione", "cura ferite moderate di massa", "scudo di legge",
                "camminare nel vento"],
            7: ["rigenerazione", "ristorare superiore", "cura ferite gravi di massa",
                "resurrezione"],
            8: ["aura sacra", "cura ferite critiche di massa",
                "immunità agli incantesimi superiore", "manto del caos"],
            9: ["guarigione di massa", "miracolo", "risurrezione pura", "porta"],
        },
        "utilita": {
            0: ["individuazione del magico", "luce", "riparare",
                "individuazione del veleno"],
            1: ["protezione dal male", "arma magica", "scudo entropico", "comando"],
            2: ["consacrare", "zona di verità", "silenzio", "oscurità"],
            3: ["dissolvi magie", "paramento magico", "glifo di interdizione",
                "elusione dell'invisibilità"],
            4: ["divinazione", "ancora dimensionale", "camminare nell'aria",
                "congedo"],
            5: ["visione del vero", "muro di pietra", "resistenza agli incantesimi",
                "spezzare incantesimo"],
            6: ["trovare il sentiero", "camminare nel vento", "parola del richiamo",
                "dissolvi magie superiore"],
            7: ["controllare il clima", "ristorare superiore", "repulsione",
                "resurrezione"],
            8: ["campo antimagia", "blocco dimensionale",
                "immunità agli incantesimi superiore", "aura sacra"],
            9: ["porta", "legare l'anima", "risurrezione pura", "miracolo"],
        },
    },

    # ── divino: druido ──────────────────────────────────────────────────────
    # La lista per cui il lotto esiste. Niente di qui compare nella lista arcana
    # allo stesso livello, e *benedizione*, *santuario* e *scudo della fede* non
    # ci sono affatto: sono da chierico.
    "druido": {
        "controllore": {
            0: ["guida", "luce", "bagliore", "resistenza"],
            1: ["intralciare", "nebbia oscurante", "fuoco fatuo",
                "passo senza tracce"],
            2: ["blocca animali", "raffica di vento", "arroventare il metallo",
                "scalare come un ragno"],
            3: ["crescita vegetale", "crescita di spine", "tempesta di nevischio",
                "muro di vento", "dominare animali"],
            4: ["controllare piante", "spine di pietra", "controllare l'acqua",
                "tempesta di ghiaccio"],
            5: ["muro di spine", "controllare i venti", "metamorfosi funesta",
                "piaga d'insetti"],
            6: ["muro di pietra", "respingere il legno", "spostare la terra",
                "guscio antivita"],
            7: ["controllare il clima", "fato strisciante", "animare piante",
                "camminare nel vento"],
            8: ["terremoto", "turbine", "inversione della gravità",
                "controllare le piante", "respingere metallo o pietra"],
            9: ["tempesta di vendetta", "antipatia", "sciame elementale",
                "mutare forma"],
        },
        "blaster": {
            0: ["bagliore", "luce", "guida", "individuazione del magico"],
            1: ["produrre fiamma", "fuoco fatuo", "zanna magica", "intralciare"],
            2: ["lama di fuoco", "sfera infuocata", "raffica di vento",
                "arroventare il metallo"],
            3: ["chiamare il fulmine", "crescita di spine", "veleno",
                "tempesta di nevischio"],
            4: ["colonna di fuoco", "tempesta di ghiaccio", "avvizzimento",
                "spine di pietra"],
            5: ["tempesta di fulmini", "muro di fuoco", "piaga d'insetti",
                "muro di spine"],
            6: ["semi di fuoco", "spostare la terra", "muro di pietra",
                "dissolvi magie superiore"],
            7: ["tempesta di fuoco", "raggio di sole", "fato strisciante",
                "controllare il clima"],
            8: ["esplosione solare", "terremoto", "dito della morte", "turbine"],
            9: ["sciame elementale", "tempesta di vendetta", "mutare forma",
                "rigenerazione"],
        },
        "supporto": {
            0: ["cura ferite minime", "guida", "resistenza", "creare acqua"],
            1: ["bacca curativa", "cura ferite leggere", "sopportare gli elementi",
                "zanna magica", "randello incantato"],
            2: ["corteccia", "resistenza dell'orso", "forza del toro",
                "saggezza del gufo", "resistere all'energia"],
            3: ["protezione dall'energia", "zanna magica superiore",
                "luce del giorno", "modellare la pietra"],
            4: ["libertà di movimento", "rimuovi malattia", "camminare nell'aria",
                "evoca alleato naturale IV"],
            5: ["pelle di pietra", "crescita animale", "viaggio arboreo",
                "evoca alleato naturale V"],
            6: ["resistenza dell'orso di massa", "legno di ferro",
                "trasporto vegetale", "evoca alleato naturale VI"],
            7: ["guarigione", "camminare nel vento", "visione del vero",
                "evoca alleato naturale VII"],
            8: ["forma animale di massa", "esplosione solare",
                "controllare le piante", "evoca alleato naturale VIII"],
            9: ["guarigione di massa", "rigenerazione", "preveggenza",
                "evoca alleato naturale IX"],
        },
        "utilita": {
            0: ["individuazione del magico", "luce", "riparare", "guida"],
            1: ["passo senza tracce", "nebbia oscurante", "sopportare gli elementi",
                "evoca alleato naturale I"],
            2: ["scalare come un ragno", "resistere all'energia", "corteccia",
                "evoca alleato naturale II"],
            3: ["modellare la pietra", "luce del giorno", "protezione dall'energia",
                "evoca alleato naturale III"],
            4: ["dissolvi magie", "camminare nell'aria", "controllare l'acqua",
                "libertà di movimento"],
            5: ["viaggio arboreo", "trasmutare roccia in fango", "pelle di pietra",
                "evoca alleato naturale V"],
            6: ["trasporto vegetale", "dissolvi magie superiore", "legno di ferro",
                "spostare la terra"],
            7: ["visione del vero", "camminare nel vento", "controllare il clima",
                "evoca alleato naturale VII"],
            8: ["forma animale di massa", "respingere metallo o pietra",
                "inversione della gravità", "evoca alleato naturale VIII"],
            9: ["mutare forma", "preveggenza", "sciame elementale",
                "evoca alleato naturale IX"],
        },
    },

    # ── ibrido: bardo ───────────────────────────────────────────────────────
    # Si ferma al 6°, e non è né arcano né divino: *suggestione* al 2° il mago
    # non ce l'ha, e tutto il ramo del danno d'area qui non esiste — per questo
    # il bardo non ha la cella «blaster».
    "bardo": {
        "controllore": {
            0: ["luci danzanti", "suono fantasma", "prestidigitazione", "messaggio"],
            1: ["charme su persone", "sonno", "ipnotismo", "immagine silenziosa",
                "confusione minore"],
            2: ["risata incontenibile di Tasha", "suggestione", "blocca persone",
                "schema ipnotico", "calmare emozioni"],
            3: ["confusione", "spavento", "disperazione opprimente", "lentezza",
                "charme su mostri"],
            4: ["dominare persone", "blocca mostri", "schema arcobaleno",
                "modificare memoria", "urlo"],
            5: ["suggestione di massa", "canto della discordia", "nebbia mentale",
                "incubo"],
            6: ["danza irresistibile di Otto", "charme su mostri di massa",
                "occhio maligno", "urlo superiore"],
        },
        "supporto": {
            0: ["resistenza", "individuazione del magico", "luce",
                "prestidigitazione"],
            1: ["cura ferite leggere", "rimuovi paura", "ritirata veloce",
                "caduta morbida"],
            2: ["eroismo", "cura ferite moderate", "sfocatura", "calmare emozioni"],
            3: ["velocità", "buona speranza", "cura ferite gravi", "spostamento"],
            4: ["libertà di movimento", "cura ferite critiche",
                "spezzare incantesimo", "invisibilità superiore"],
            5: ["eroismo superiore", "cura ferite leggere di massa",
                "dissolvi magie superiore", "traviare"],
            6: ["cura ferite moderate di massa", "banchetto degli eroi",
                "animare oggetti", "trovare il sentiero"],
        },
        "utilita": {
            0: ["mano magica", "messaggio", "lettura del magico", "luci danzanti"],
            1: ["grasso", "ventriloquio", "immagine silenziosa", "caduta morbida"],
            2: ["invisibilità", "polvere scintillante", "immagine speculare",
                "silenzio", "frantumare"],
            3: ["dissolvi magie", "immagine maggiore", "spostamento",
                "sonno profondo"],
            4: ["porta dimensionale", "evocazione ombrosa", "modificare memoria",
                "spezzare incantesimo"],
            5: ["traviare", "camminare nell'ombra", "immagine persistente",
                "nebbia mentale"],
            6: ["velo", "immagine permanente", "trovare il sentiero",
                "animare oggetti"],
        },
    },

    # ── divino parziale: ranger e paladino ──────────────────────────────────
    # Quattro livelli e non oltre, primo slot al 4° di classe, e il livello
    # dell'incantatore è `livello − 3`. Niente incantesimi di livello 0: la
    # chiave 0 qui non c'è, e chi legge deve accorgersene invece di ricevere una
    # lista vuota in silenzio.
    "ranger": {
        "supporto": {
            1: ["zanna magica", "sopportare gli elementi", "ritardare veleno",
                "resistere all'energia"],
            2: ["cura ferite leggere", "corteccia", "resistenza dell'orso",
                "grazia felina", "protezione dall'energia"],
            3: ["cura ferite moderate", "zanna magica superiore",
                "neutralizzare veleni", "rimuovi malattia"],
            4: ["cura ferite gravi", "libertà di movimento", "crescita animale",
                "evoca alleato naturale IV"],
        },
        "utilita": {
            1: ["passo senza tracce", "falcata prolungata",
                "individuare trappole e fosse", "salto", "intralciare"],
            2: ["laccio", "muro di vento", "crescita di spine", "blocca animali",
                "evoca alleato naturale II"],
            3: ["scurovisione", "camminare sull'acqua", "crescita vegetale",
                "controllare piante", "respingere parassiti"],
            4: ["non individuazione", "viaggio arboreo", "comunione con la natura",
                "libertà di movimento"],
        },
    },
    "paladino": {
        "supporto": {
            1: ["benedizione", "cura ferite leggere", "ristorare inferiore",
                "favore divino", "protezione dal male"],
            2: ["scudo altrui", "forza del toro", "resistere all'energia",
                "rimuovi paralisi", "ritardare veleno"],
            3: ["preghiera", "cura ferite moderate", "arma magica superiore",
                "rimuovi maledizione", "curare cavalcatura"],
            4: ["cura ferite gravi", "ristorare", "protezione dalla morte",
                "spezzare incantesimo", "neutralizzare veleni"],
        },
        "utilita": {
            1: ["benedire arma", "arma magica", "individuazione dei non morti",
                "virtù", "sopportare gli elementi"],
            2: ["zona di verità", "allineamento non individuabile",
                "splendore dell'aquila", "scudo altrui"],
            3: ["dissolvi magie", "cerchio magico contro il male",
                "individuare menzogne", "luce del giorno"],
            4: ["spada sacra", "scacciare il male", "marchio della giustizia",
                "protezione dalla morte"],
        },
    },
}

#: Quando la cella (classe × funzione) non esiste, si ripiega su un'altra
#: funzione **della stessa classe** — mai sulla lista di un'altra classe, che è
#: esattamente il difetto da cui nasce questo file. Un mago «supporto» non c'è
#: nel gioco; diventa un mago «utilità», e il conto lo dice.
FUNZIONE_DI_RIPIEGO = {
    "mago": "utilita", "stregone": "utilita",
    "chierico": "supporto", "druido": "controllore",
    "bardo": "supporto", "ranger": "utilita", "paladino": "supporto",
}

#: Le classi incantatrici per cui una lista **non** è stata scritta. Per queste
#: il generatore preferisce non scegliere invece di scegliere male: un blocco
#: senza incantesimi si riempie in due minuti, un adepto con la lista del mago
#: arriva al tavolo e ci resta.
#: ⚠️ L'adepto è fuori dalla matrice approvata dal DM (le 21 celle sono le sei
#: classi con lista piena). È l'unico residuo dichiarato del lotto I.
SENZA_LISTA = frozenset({"adepto", "adept"})

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
PF1E_SOLO: dict[str, dict[int, list[tuple[str, str]]]] = {
    "mago": {
        1: [
            ("fossa d'inciampo", 'stumble gap'),
            ('spinta idraulica', 'hydraulic push'),
        ],
        2: [
            ('fossa', 'create pit'),
            ('pioggia di pietre', 'stone call'),
        ],
        3: [
            ('fossa irta', 'spiked pit'),
            ("sfera d'acqua", 'aqueous orb'),
        ],
        4: [
            ('fulmini globulari', 'ball lightning'),
            ('fossa acida', 'acid pit'),
        ],
        5: [
            ('fossa vorace', 'hungry pit'),
            ('serpente di fuoco', 'fire snake'),
        ],
        6: [
            ('scirocco', 'sirocco'),
        ],
        7: [
            ('tizzone ardente', 'firebrand'),
            ('deviazione', 'deflection'),
        ],
        8: [
            ('saette', 'stormbolts'),
        ],
        9: [
            ('rocce cozzanti', 'clashing rocks'),
        ],
    },
    "chierico": {
        2: [
            ('arma del timore', 'weapon of awe'),
        ],
        3: [
            ('manto irato', 'wrathful mantle'),
        ],
        4: [
            ('benedizione del fervore', 'blessing of fervor'),
        ],
        5: [
            ('colonna di vita', 'pillar of life'),
            ('mondare', 'cleanse'),
        ],
        8: [
            ('saette', 'stormbolts'),
        ],
        9: [
            ('venti della vendetta', 'winds of vengeance'),
        ],
    },
    "druido": {
        1: [
            ('aculei', 'bristle'),
            ('spinta idraulica', 'hydraulic push'),
        ],
        2: [
            ('pioggia di pietre', 'stone call'),
        ],
        3: [
            ("sfera d'acqua", 'aqueous orb'),
        ],
        4: [
            ('fulmini globulari', 'ball lightning'),
        ],
        5: [
            ('serpente di fuoco', 'fire snake'),
            ('aspetto del lupo', 'aspect of the wolf'),
        ],
        6: [
            ('scirocco', 'sirocco'),
        ],
        7: [
            ('terrapieno', 'rampart'),
        ],
        8: [
            ('saette', 'stormbolts'),
        ],
        9: [
            ('rocce cozzanti', 'clashing rocks'),
        ],
    },
    "bardo": {
        1: [
            ('finale salvifico', 'saving finale'),
        ],
        2: [
            ('ispirazione galante', 'gallant inspiration'),
        ],
        3: [
            ('tamburi tonanti', 'thunderous drums'),
        ],
        4: [
            ('esplosione discorde', 'discordant blast'),
        ],
        5: [
            ('dardo assordante', 'deafening song bolt'),
            ('manto dei sogni', 'cloak of dreams'),
        ],
        6: [
            ('finale letale', 'deadly finale'),
            ('interdizione dello stolto', "fool's forbiddance"),
        ],
    },
    "ranger": {
        1: [
            ('arco gravitazionale', 'gravity bow'),
            ('lame pesanti', 'lead blades'),
        ],
        2: [
            ("aspetto dell'orso", 'aspect of the bear'),
            ('eruzione di frecce', 'arrow eruption'),
        ],
        3: [
            ('nemico istantaneo', 'instant enemy'),
        ],
        4: [
            ('aspetto del lupo', 'aspect of the wolf'),
            ("spirito dell'arco", 'bow spirit'),
        ],
    },
    "paladino": {
        1: [
            ('richiamo del cavaliere', "knight's calling"),
        ],
        2: [
            ('vigore virtuoso', 'righteous vigor'),
            ('fuoco che avvince', 'fire of entanglement'),
        ],
        3: [
            ('fuoco del giudizio', 'fire of judgment'),
            ("santificare l'armatura", 'sanctify armor'),
        ],
        4: [
            ('fuoco della vendetta', 'fire of vengeance'),
            ('colpo risonante', 'resounding blow'),
        ],
    },
}
PF1E_SOLO["stregone"] = PF1E_SOLO["mago"]


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
    per_classe = LISTE[CANONICA.get(classe.lower(), classe.lower())]
    if funzione in per_classe:
        return per_classe[funzione], funzione
    ripiego = FUNZIONE_DI_RIPIEGO[CANONICA.get(classe.lower(), classe.lower())]
    return per_classe[ripiego], ripiego


def scegli(classe: str, funzione: str, slot: tuple[int, ...],
           rng: random.Random, pf1e: bool = False) -> tuple[list[str], list[str]]:
    """Un incantesimo per slot, dalla lista di quella classe e di quel livello.

    Torna (le righe da stampare, le note sui rincari PF1e). Gli incantesimi di
    livello 0 non si scelgono: sono a volontà e non descrivono la creatura.
    """
    canonica = CANONICA.get(classe.lower(), classe.lower())
    if canonica in SENZA_LISTA:
        return [], []
    lista, _ = cella(canonica, funzione)
    righe, note = [], []
    for livello, quanti in enumerate(slot):
        if not quanti or livello == 0 or livello not in lista:
            continue
        scelti = rng.sample(lista[livello], min(quanti, len(lista[livello])))
        if pf1e:
            aggiunte = PF1E_SOLO.get(canonica, {}).get(livello)
            if aggiunte:
                it, prd = rng.choice(aggiunte)
                # Uno solo per livello, e **sostituisce** invece di aggiungere:
                # il numero di slot è quello della tabella SRD e non si tocca.
                scelti[-1] = f"{it} (PF1e: {prd})"
                note.append(f"{livello}°: {it} ({prd}) — PF1e, senza equivalente 3.5")
        righe.append(f"{livello}°: " + ", ".join(sorted(scelti)))
    return righe, note
