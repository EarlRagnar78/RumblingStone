"""dmcore.caratteristiche — la scelta delle sei caratteristiche di una creatura.

ADR-0066, `PIANO-QUALITA-DEL-CODICE` §8 (lotto E).

Gli strati di ADR-0064, in ordine: la sestina che la scheda scrive, quella della
fonte citata, i vincoli ricavati da CA, pf, iniziativa e lotta, il tetto dei TS,
e per ultimo l'array del Manuale del DM per ruolo, con taglia e razza SRD e un
±1 a seme fisso. Qui stanno anche le tabelle della scelta: `PROFILI`,
`PER_TAGLIA`, `RAZZE`.

🔒 **Il verificatore non lo importa mai**, ne' direttamente ne' passando per un
altro modulo: se una stessa funzione scegliesse e verificasse, un errore di
regola comparirebbe da tutte e due le parti e si confermerebbe da solo.
`test_grafo_import_creature.py` lo verifica. Lo importano i generatori:
`genera_attributi`, `derive_statblocks` e il ramo PNG di `genera_creatura`.

Solo stdlib.
"""
from __future__ import annotations

import random
import re
from pathlib import Path

from dmcore import tabelle as T
from dmcore.lettura_creatura import (
    BAB_SCRITTO, BONUS_DADO, CLASSE_NEL_TIPO, INIZIATIVA_MIGLIORATA, INIZIATIVA_SCRITTA,
    LOTTA_MIGLIORATA, LOTTA_SCRITTA, LOTTA_TAGLIA, ORDINE, PEZZO_DADO, PF_DADO,
    dalla_scheda, numeri_della_fonte, parole_del_file, pf_dado_sospetto, plausibile,
    robustezza, senza_note, sestine_citate, taglia_di, tetti_dai_ts,
)

__all__ = [
    "ARRAY_ELITE", "ARRAY_STANDARD", "PROFILI", "PROFILO_DI_RIPIEGO", "ELITE",
    "DES_SCRITTA", "CONTATTO", "NON_MORTO", "MODELLO_SENZA_MENTE", "mod",
    "da_modificatore", "des_vincolata", "cos_da_pf", "dalla_fonte", "des_da_iniziativa",
    "for_da_lotta", "iniziativa_ambigua", "profilo_di", "PER_TAGLIA", "RAZZE",
    "razza_di", "genera", "riga_attributi"
]


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
DES_SCRITTA = re.compile(r"([+-]\s*\d+)\s*(?:Des|Dex|destrezza)\b", re.I)
CONTATTO = re.compile(r"(?:touch|contatto)\s*(\d+)", re.I)
NON_MORTO = re.compile(r"\b(?:undead|non[ -]?mort[oi])\b", re.I)
MODELLO_SENZA_MENTE = re.compile(r"skelet|schelet|zombi", re.I)
mod = T.mod


def da_modificatore(m: int) -> int:
    """Il punteggio piu' basso che da' quel modificatore: 10 + 2m."""
    return max(1, 10 + 2 * m)


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
