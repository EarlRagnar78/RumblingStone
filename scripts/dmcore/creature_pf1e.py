"""dmcore/creature_pf1e.py — una creatura costruita in 3.5, portata in PF1e (ADR-0111).

`genera_creatura.py --sistema pf1e` costruisce come sempre sul bersaglio per
GS, poi passa di qui: i numeri che in Pathfinder 1e cambiano si ricalcolano
dai dati del plugin (`sistemi/pf1e/dati/creature.toml`, estratti dal PRD).

Cosa si ricalcola, e con quale regola del PRD (Creature Statistics by Type,
Size Bonuses and Penalties, Combat Maneuvers):

- dado vita del tipo, e la caratteristica dei pf risolta di nuovo sui pf del
  blocco 3.5 (i non morti usano il Carisma, PRD Undead Traits);
- BAB del tipo, quindi gli attacchi spostati della differenza;
- TS buoni del tipo: buono = 2 + DV/2, scarso = DV/3;
- BMC = BAB + For + taglia; DMC = 10 + BAB + For + Des + taglia;
- gradi di abilità = (gradi del tipo + Int) × DV, almeno 1 per DV.

Con i livelli di classe il blocco non si converte: `genera_png` lo costruisce
da zero dalle tabelle PF1e di `classi.toml` e `creature.toml` (tutte le 55
classi, multiclasse e prestigio compresi).

Cosa no, e si dice nel conto: i pf bonus dei costrutti per taglia (la tabella
non c'è nel PRD in cache) e le abilità fuse di PF1e. Gigante ed elementale non sono tipi PF1e: diventano umanoide
(sottotipo gigante) ed esterno (sottotipo elementale).
"""
from __future__ import annotations

import functools
import math
import re
from dataclasses import replace

from . import sistemi as S
from .formule import formula
from . import tabelle as T

#: Tipi 3.5 che in PF1e sono sottotipi di un altro tipo (PRD, Creature Types).
DIVENTA = {"giant": "humanoid", "elemental": "outsider"}
ORDINE_TS = ("temp", "rifl", "vol")
NOMI_TS = {"temp": "Temp", "rifl": "Rifl", "vol": "Vol"}
#: Il tetto della caratteristica dei pf, lo stesso di genera_creatura (COS_MAX).
COS_MAX = 6


def _mod(x: int) -> int:
    """Il modificatore di caratteristica: formula `modificatore` del plugin (F3 di ADR-0112)."""
    return formula("modificatore", "pf1e")(punteggio=x)


def _attributi(testo: str) -> dict[str, int]:
    return {k: int(v) for k, v in re.findall(r"(For|Des|Cos|Int|Sag|Car)\s+(\d+)", testo)}


def taglia_inglese(taglia: str, taglie_pf1e: dict) -> str:
    """La taglia come la scrive il PRD (le alias italiane di tabelle.TAGLIE)."""
    t = taglia.lower()
    if t in taglie_pf1e:
        return t
    valore = T.TAGLIE.get(t)
    for nome in taglie_pf1e:
        if T.TAGLIE.get(nome) == valore:
            return nome
    raise ValueError(f"taglia ignota per PF1e: {taglia}")


def ts_buoni(tipo35: str, voce: dict) -> tuple[str, ...]:
    """I TS buoni PF1e. Per umanoide (uno a scelta) ed esterno (due a scelta) la
    scelta è deterministica: prima i TS buoni che il tipo 3.5 aveva, poi
    nell'ordine Temp, Rifl, Vol."""
    if not voce["ts_a_scelta"]:
        return tuple(voce["ts_buoni"])
    prima = [k for k in T.TIPI[tipo35][2] if k in ORDINE_TS]
    resto = [k for k in ORDINE_TS if k not in prima]
    return tuple((prima + resto)[:voce["ts_a_scelta"]])


def converti(sb, tipo: str, taglia: str, root=None, pf_bersaglio: "int | None" = None):
    """(statblocco PF1e, righe del conto). `sb` è il blocco 3.5 di genera().

    `pf_bersaglio` serve ai non morti: il blocco 3.5 non ha Costituzione e i
    suoi pf non sono sul bersaglio del GS; il PF1e ce li porta col Carisma."""
    dati = S.dati("pf1e", "creature.costruzione", root)
    tipo_pf = DIVENTA.get(tipo, tipo)
    if tipo_pf not in dati["tipi"]:
        raise ValueError(f"tipo {tipo} senza riga PF1e in creature.toml")
    voce = dati["tipi"][tipo_pf]
    tg = taglia_inglese(taglia, dati["taglie"])
    mt = dati["taglie"][tg]["bmc_dmc"]
    car = _attributi(sb.attributi)
    dv = int(sb.pf_dado.split("d")[0])
    conto = [f"PF1e: tipo {tipo_pf}" + (f" (in 3.5 era {tipo}, ora sottotipo)" if tipo_pf != tipo else "")
             + f", d{voce['dv']}, BAB ×{voce['bab']:g}, taglia {tg} (BMC/DMC {mt:+d}) — PRD, "
             "Creature Statistics by Type e Size Bonuses"]

    # pf: dado del tipo, e la caratteristica dei pf risolta di nuovo sui pf del
    # blocco 3.5 (che è già sul bersaglio del GS), come fa genera() con la Cos:
    # cambiare dado senza risolvere spostava il blocco di 70 pf a GS 7.
    # I non morti usano il Carisma, i costrutti non hanno Costituzione.
    media = dv * (voce["dv"] / 2 + 0.5)
    attributi = sb.attributi
    obiettivo = int(sb.pf)
    bonus_costrutto = 0
    if tipo_pf == "construct":
        m_pf, chiave_pf = 0, None
        attributi = re.sub(r"Cos\s+\d+", "Cos —", attributi)
        # PRD, Construct Traits: pf bonus per taglia. La tabella manca nel PSRD-Data
        # in cache: i valori vengono dalle schede dei costrutti del Bestiary,
        # controllati sulla tabella del PRD pubblicato (Fine e Diminutive da lì)
        # ([pf_bonus_costrutti] di creature.toml, generato con le schede che li provano)
        bonus_costrutto = dati.get("pf_bonus_costrutti", {}).get(tg, {})
        bonus_costrutto = bonus_costrutto.get("bonus", 0) if isinstance(bonus_costrutto, dict) else bonus_costrutto
        if bonus_costrutto:
            conto.append(f"pf bonus del costrutto {tg}: +{bonus_costrutto} (PRD, Construct Traits; "
                         "valore ricostruito dalle schede del Bestiary)")
        else:
            conto.append(f"⚠ i pf bonus dei costrutti di taglia {tg} (PRD, Construct Traits) non ci sono: "
                         "la tabella manca nel PRD in cache e nessuna scheda li prova")
    else:
        chiave_pf = "Car" if tipo_pf == "undead" else "Cos"
        if tipo_pf == "undead" and re.search(r"Cos\s+—", sb.attributi):
            # il blocco 3.5 del non morto non ha Costituzione (lotto 5): i suoi pf
            # sono i soli dadi, sotto il bersaglio. Il PF1e glieli ridà col
            # Carisma, quindi il Carisma si risolve sul bersaglio del GS
            # (`pf_bersaglio`, quello di genera_creatura.bersaglio_di), non sul
            # blocco 3.5.
            if pf_bersaglio:
                obiettivo = max(obiettivo, pf_bersaglio)
            else:
                conto.append("⚠ non morto senza Costituzione e senza pf_bersaglio: il Carisma "
                             "si risolve sui pf del blocco 3.5, che sono i soli dadi")
        m_pf = min(COS_MAX, round((obiettivo - media) / dv))
        car[chiave_pf] = 10 + 2 * m_pf
        attributi = re.sub(chiave_pf + r"\s+\d+", f"{chiave_pf} {car[chiave_pf]}", attributi)
        if tipo_pf == "undead":
            attributi = re.sub(r"Cos\s+\d+", "Cos —", attributi)
    pf = max(1, int(media + m_pf * dv)) + bonus_costrutto
    conto.append(f"pf = {dv}d{voce['dv']} ({media:g})"
                 + (f" {m_pf:+d}×{dv} {chiave_pf} {car[chiave_pf]}" if chiave_pf else "")
                 + f" = {pf} (3.5: {sb.pf})"
                 + (f"; {chiave_pf} al tetto +{COS_MAX}, mancano {obiettivo - pf} pf" if chiave_pf and m_pf == COS_MAX and pf < obiettivo else ""))

    # BAB e attacchi.
    bab = int(voce["bab"] * dv)
    bab35 = int(T.TIPI[tipo][1] * dv)
    delta = bab - bab35
    attacchi = list(sb.attacchi)
    if delta:
        attacchi = [re.sub(r"([+-]\d+)", lambda m: f"{int(m.group(1)) + delta:+d}", a, count=1) for a in attacchi]
        conto.append(f"BAB +{bab} (3.5: +{bab35}): attacchi spostati di {delta:+d}"
                     + (" — sopra il bersaglio del GS, è la regola del tipo in PF1e" if delta > 0 else ""))
    else:
        conto.append(f"BAB +{bab}, come in 3.5")

    # TS.
    buoni = ts_buoni(tipo, voce)
    car_ts = {"temp": "Car" if tipo_pf == "undead" else "Cos", "rifl": "Des", "vol": "Sag"}
    ts = {}
    for k in ORDINE_TS:
        base = 2 + dv // 2 if k in buoni else dv // 3
        m = 0 if (k == "temp" and tipo_pf == "construct") else _mod(car.get(car_ts[k], 10))
        ts[k] = base + m
    ts_testo = ", ".join(f"{NOMI_TS[k]} {ts[k]:+d}" for k in ORDINE_TS)
    conto.append(f"TS buoni {', '.join(NOMI_TS[k] for k in buoni) or 'nessuno'} → {ts_testo}")

    # Manovre e abilità.
    m_for, m_des = _mod(car.get("For", 10)), _mod(car.get("Des", 10))
    bmc = bab + m_for + mt
    dmc = 10 + bab + m_for + m_des + mt
    # senza Intelligenza: «mindless creatures do not gain feats or skills» (PRD, Creature Types)
    gradi = 0 if re.search(r"Int\s+—", attributi) else max(1, voce["gradi"] + _mod(car.get("Int", 10))) * dv
    conto.append(f"BMC = {bab} BAB {m_for:+d} For {mt:+d} taglia = {bmc:+d}; "
                 f"DMC = 10 + {bab} {m_for:+d} {m_des:+d} Des {mt:+d} = {dmc}")
    conto.append(f"gradi di abilità = ({voce['gradi']} + Int) × {dv} DV = {gradi}")

    bonus = pf - int(media)
    nuovo = replace(
        sb,
        tipo=re.sub(r"\d+d\d+([+-]\d+)?", f"{dv}d{voce['dv']}" + (f"{bonus:+d}" if bonus else ""), sb.tipo, count=1)
        .replace(tipo, tipo_pf) if tipo_pf != tipo else
        re.sub(r"\d+d\d+([+-]\d+)?", f"{dv}d{voce['dv']}" + (f"{bonus:+d}" if bonus else ""), sb.tipo, count=1),
        pf=str(pf),
        pf_dado=f"{dv}d{voce['dv']}" + (f"{bonus:+d}" if bonus else ""),
        ts=ts_testo,
        attacchi=attacchi,
        attributi=attributi,
        voci=list(sb.voci) + [f"Manovre: BMC {bmc:+d}, DMC {dmc}", f"Gradi di abilità: {gradi}"],
        fonte=sb.fonte.replace("generato-SRD-3.5", "generato-PRD-PF1e (base 3.5)"),
    )
    return nuovo, conto


#: Le classi 3.5 il cui nome italiano non è nel lessico PF1e (`[alias]` di
#: classi.toml): il guerriero PNG della 3.5 è il «warrior» del PRD.
ALIAS_35 = {"guerriero-png": "warrior"}


def classe_pf1e(nome: str, dati: dict) -> str:
    """Il nome PRD (inglese minuscolo) di una classe 3.5 o italiana."""
    n = nome.lower()
    if n in dati["classi"]:
        return n
    n = ALIAS_35.get(n) or dati.get("alias", {}).get(n)
    if n not in dati["classi"]:
        raise ValueError(f"classe {nome} senza riga PF1e in classi.toml")
    return n


def ts_di_classe(livelli: int, buoni, gruppo: str) -> dict[str, int]:
    """TS base PF1e di una classe. Base e PNG: buono 2 + L/2, scarso L/3, come
    nel 3.5. Prestigio PF1e: buono (L+1)/2, scarso (L+1)/3 (al 10° +5 e +3,
    PRD, tabelle delle classi di prestigio)."""
    if gruppo == "prestigio":
        return {k: (livelli + 1) // 2 if k in buoni else (livelli + 1) // 3 for k in ORDINE_TS}
    return {k: 2 + livelli // 2 if k in buoni else livelli // 3 for k in ORDINE_TS}


def _riga_slot(griglia: list, livello_zero: bool) -> str:
    """La riga «Incantesimi al giorno» del blocco con una griglia PF1e."""
    if livello_zero:
        return ("Incantesimi al giorno (dal 1° livello): " + "/".join(map(str, griglia[1:]))
                + " · trucchetti a volontà")
    return "Incantesimi al giorno (dal 1° livello): " + "/".join(map(str, griglia[1:]))


# ── PNG costruiti in PF1e (tutte le classi di classi.toml) ──────────────────
#
# Un PNG con livelli di classe non si porta dal 3.5 (varrebbe solo per le 16
# classi in comune): `genera_png` lo costruisce da zero con i dati del plugin
# PF1e, quindi per tutte le 55 classi del PRD, anche in multiclasse con le
# classi di prestigio.

#: Armature del ruolo, con i nomi del PRD (`[armature]`/`[scudi]` di creature.toml).
ARMATURA_DEL_RUOLO = {"tiratore": ("studded leather", None),
                      "schermagliatore": ("chain shirt", None)}
SCUDO_PESANTE = "shield, heavy steel"
#: Le funzioni da incantatore delle liste curate 3.5 (dmcore/incantesimi.py).
FUNZIONI_CURATE = ("controllore", "blaster", "supporto", "utilita")


def leggi_classi(testo: str, dati: dict) -> list[tuple[str, int]]:
    """«mago:7» o «mago:5,mistificatore arcano:3» → [(nome PRD, livelli), ...]."""
    fuori = []
    for pezzo in testo.split(","):
        nome, _, liv = pezzo.strip().rpartition(":")
        if not nome or not liv.isdigit():
            raise ValueError(f"serve «classe:livello», non «{pezzo.strip()}»")
        fuori.append((classe_pf1e(nome.strip(), dati), int(liv)))
    return fuori


def livello_incantatore_pf1e(en: str, livelli: int, dati: dict) -> int:
    """LI: le classi la cui griglia comincia al 4° livello (ranger, paladino,
    antipaladino, iracondo di stirpe) lanciano da livello − 3 (PRD, descrizione
    di ogni classe); le altre dal livello di classe."""
    g = dati["griglie"][dati["incantatori"][en]["griglia"]]
    return livelli - 3 if min(map(int, g)) == 4 else livelli


def avanzamento(classi: list[tuple[str, int]], dati: dict) -> dict[str, int]:
    """Livelli d'incantatore aggiunti dalle classi di prestigio. Vanno alla prima
    classe incantatrice della lista; il teurgo mistico li dà alla prima arcana e
    alla prima divina (PRD, «+1 level of existing spellcasting class»)."""
    incantatrici = [en for en, _ in classi if en in dati.get("incantatori", {})]
    piu = {en: 0 for en in incantatrici}
    car = S.dati("pf1e", "creature.conformita").get("incantesimi", {}).get("caratteristica", {})
    for en, liv in classi:
        livelli_che_avanzano = dati.get("avanza_incantatore", {}).get(en)
        if not livelli_che_avanzano or not incantatrici:
            continue
        n = sum(1 for x in livelli_che_avanzano if x <= liv)
        if en == "mystic theurge":
            arcane = next((c for c in incantatrici if car.get(c) == "Int" or c in ("sorcerer", "bard")), None)
            divine = next((c for c in incantatrici if car.get(c) == "Sag"), None)
            for c in {arcane, divine} - {None}:
                piu[c] += n
        else:
            piu[incantatrici[0]] += n
    return piu


@functools.lru_cache(maxsize=None)
def _mappa_funzioni(root=None) -> dict[str, set[str]]:
    """nome PRD dell'incantesimo → funzioni in cui le liste curate 3.5 lo mettono
    (via lessico italiano 3.5 → PRD). Serve a scegliere per funzione dentro la
    lista PF1e della classe, che è la fonte di cosa la classe può lanciare."""
    from . import incantesimi as INC
    import lessico_regole as LR
    it_en = {}
    for v in LR.tabella_35():
        if v["tipo"] == "incantesimo":
            for it in [v["it"]] + [x for x in v.get("varianti", "").split("|") if x]:
                it_en[it.lower()] = v["srd35"].lower()
    fuori: dict[str, set[str]] = {}
    for per_classe in INC.liste()["LISTE"].values():
        for funzione, livelli in per_classe.items():
            for nomi in livelli.values():
                for it in nomi:
                    en = it_en.get(it.lower())
                    if en:
                        fuori.setdefault(en, set()).add(funzione)
    return fuori


def scegli_pf1e(en: str, slot: list[int], funzione: str, rng, dati: dict,
                root=None) -> tuple[list[str], list[str]]:
    """Un incantesimo per slot dalla lista PF1e della classe (PRD). Dentro la
    lista si preferiscono quelli che le liste curate mettono nella funzione
    chiesta; se non bastano si completa dal resto della lista, e il conto lo
    dice. Torna (righe, note)."""
    liste = dati.get("liste", {}).get(en)
    if not liste:
        return [], [f"⚠ nessuna lista PF1e di {en} nei dati del plugin: incantesimi da scegliere a mano"]
    # i nomi PRD si confrontano senza maiuscole («Breath Of Life» nel PRD)
    nomi_it = {k.lower(): v for k, v in dati.get("nomi_it", {}).items()}
    funzioni = _mappa_funzioni(root)
    righe, note, fuori_funzione = [], [], 0
    for livello, quanti in enumerate(slot):
        pool = liste.get(str(livello), [])
        if not quanti or livello == 0 or not pool:
            continue
        adatti = sorted(n for n in pool if funzione in funzioni.get(n.lower(), ()))
        altri = sorted(n for n in pool if n not in adatti)
        scelti = rng.sample(adatti, min(quanti, len(adatti)))
        if len(scelti) < quanti:
            extra = rng.sample(altri, min(quanti - len(scelti), len(altri)))
            fuori_funzione += len(extra)
            scelti += extra
        righe.append(f"{livello}°: " + ", ".join(sorted(nomi_it.get(n.lower(), n) for n in scelti)))
    if fuori_funzione:
        note.append(f"{fuori_funzione} incantesimi presi dalla lista PF1e di {en} fuori dalla funzione "
                    f"«{funzione}», perché quelli della funzione non bastavano")
    senza_it = sorted(n for r in righe for n in liste_nomi(r)
                      if n in set().union(*liste.values()) and n.lower() not in nomi_it)
    if senza_it:
        note.append(f"{len(senza_it)} nomi restano inglesi: non sono nel lessico italiano PF1e")
    return righe, note


def liste_nomi(riga: str) -> list[str]:
    return [x.strip() for x in riga.split(":", 1)[1].split(",")]
