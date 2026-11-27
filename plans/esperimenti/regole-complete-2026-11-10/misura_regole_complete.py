#!/usr/bin/env python3
"""misura_regole_complete.py — le parti delle regole che misura_plugin_regole non guarda.

Richiesta del DM del 2026-11-10 («verifica che le regole PF1e siano complete e
nel caso completale tutte, così come fatto per d20 SRD e 3.5»). La misura di
ADR-0121 (`plans/esperimenti/plugin-regole-2026-11-09/misura_plugin_regole.py`)
dà 217/217 per il PF1e e 605/606 per il 3.5, ma solo sulle tabelle che misura:
classi, armature, griglie, abilità, liste d'incantesimi del 3.5, soglie PE 3.5.
Questa misura aggiunge, con lo stesso formato e la stessa cache:

- PF1e: soglie PE (tre tracce), PE per GS, tesoro per incontro (tre velocità),
  statistiche dei mostri per GS (Bestiary Table 1–1), modificatore di
  caratteristica (formula d20), liste d'incantesimi 3.5 usate dai moduli PF1e
  (`creature.incantesimi` del plugin pf1e), incantesimi «solo PF1e».
- 3.5: tesoro per livello d'incontro (SRD «Treasure Values per Encounter»).
- Tutti e due: talenti dei PNG generati (numero per ogni classe al 7°, contato
  a mano sul manuale, e prerequisiti dei talenti generali), e nomi italiani nel lessico per talenti, incantesimi e condizioni.
- Tutti e due (lotto 5): tratti dei tipi nei mostri generati (Cos e Int «—», niente
  talenti ai senza mente, pf e Tempra senza Costituzione, pf bonus del costrutto per taglia).

    python3 plans/esperimenti/regole-complete-2026-11-10/misura_regole_complete.py
    … --json FILE   … --md FILE

Solo lettura, nessuna rete, esce 0 sempre: è una misura, non un cancello.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "plans/esperimenti/plugin-regole-2026-11-09"))
sys.path.insert(0, str(ROOT / "scripts"))

import misura_plugin_regole as M  # noqa: E402


def _n(s: str) -> "int | None":
    s = s.replace(",", "").replace("gp", "").strip()
    return M.num(s)


def _tab(base, libro: str, sid: int) -> list:
    body = M._db(base, libro).execute("select body from sections where section_id=?", (sid,)).fetchone()[0]
    return next(iter(M.tabelle(body).values()))


def _riga(nome, fonte, coperte, giuste, sb, mancanti=(), nota="", campi_assenti=(), nv=()):
    out = {"tabella": nome, "fonte": fonte, "coperte": coperte, "giuste": giuste, "sbagliate": sb,
           "mancanti": list(mancanti), "campi_assenti": list(campi_assenti), "non_verificabili": list(nv)}
    if nota:
        out["nota"] = nota
    return out


# ------------------------------------------------------------------ PF1e

def tracce_pf1e(base, nome, sid, file, chiave, col0=0) -> dict:
    righe = _tab(base, "cr", sid)
    dati = M.toml(file)[chiave]
    fonte, sb, cop = 0, [], 0
    for r in righe[2:]:
        lv = M.num(r[col0])
        if lv is None:
            continue
        for i, traccia in enumerate(("lenta", "media", "veloce")):
            v = _n(r[col0 + 1 + i])
            v = 0 if v is None and r[col0 + 1 + i].strip() in ("—", "-") else v
            fonte += 1
            p = dati.get(traccia, {}).get(str(lv))
            if p is None:
                continue
            cop += 1
            if p != v:
                sb.append({"riga": f"{traccia} {lv}", "campo": chiave, "plugin": p, "fonte": v})
    return _riga(nome, fonte, cop, cop - len(sb), sb)


def px_per_gs(base) -> dict:
    dati = M.toml("sistemi/pf1e/dati/incontri.toml")["px_per_gs"]
    sb, mancanti, fonte = [], [], 0
    for r in _tab(base, "cr", 3655)[2:]:
        gs, v = r[0].strip(), _n(r[1])
        if v is None:
            continue
        fonte += 1
        if gs not in dati:
            mancanti.append(gs)
        elif dati[gs] != v:
            sb.append({"riga": gs, "campo": "px", "plugin": dati[gs], "fonte": v})
    cop = fonte - len(mancanti)
    return _riga("PE per GS (Experience Point Awards)", fonte, cop, cop - len(sb), sb, mancanti)


CAMPI_GS = ["pf", "ca", "attacco_alto", "attacco_basso", "danno_alto", "danno_basso",
            "cd_primaria", "cd_secondaria", "ts_buono", "ts_cattivo"]


def statistiche_per_gs(base) -> dict:
    from dmcore import tabelle as T

    plugin = {float(k): r for k, r in T.TABELLA_1_1.items()}
    sb, mancanti, fonte = [], [], 0
    for r in _tab(base, "b1", 93)[2:]:
        g = r[0].strip()
        gs = 0.5 if g == "1/2" else (float(g) if g.replace(".", "").isdigit() else None)
        if gs is None:
            continue
        fonte += 1
        p = plugin.get(gs)
        if p is None:
            mancanti.append(g)
            continue
        for campo, cella in zip(CAMPI_GS, r[1:]):
            v = M.num(cella)
            if v is not None and p.get(campo) != v:
                sb.append({"riga": f"GS {g}", "campo": campo, "plugin": p.get(campo), "fonte": v})
    cop = fonte - len(mancanti)
    return _riga("statistiche dei mostri per GS (Bestiary Table 1–1)", fonte, cop,
                 cop - len({s["riga"] for s in sb}), sb, mancanti)


def formula_modificatore(base) -> dict:
    """La formula d20 del modificatore contro la tabella del PRD (Ability Modifiers)."""
    f = M.toml("sistemi/d20/dati/formule.toml")["formule"]["modificatore"]["espressione"]
    c = M._db(base, "cr")
    body = c.execute("select body from sections where type='table' and name like '%Ability Modifiers%'").fetchone()
    righe = next(iter(M.tabelle(body[0]).values())) if body else []
    sb, fonte = [], 0
    for r in righe:
        m = re.match(r"^(\d+)[–-](\d+)$", r[0].strip()) if r else None
        if not m:
            continue
        for punteggio in (int(m.group(1)), int(m.group(2))):
            fonte += 1
            atteso = M.num(r[1])
            calc = eval(f, {}, {"punteggio": punteggio})  # noqa: S307 — espressione dei dati del repo
            if calc != atteso:
                sb.append({"riga": punteggio, "campo": "modificatore", "plugin": calc, "fonte": atteso})
    return _riga("modificatore di caratteristica (formula d20 contro PRD)", fonte, fonte, fonte - len(sb), sb,
                 nota="" if fonte else "tabella non trovata nel PRD in cache")


CLASSE_EN = {"mago": "Wizard", "chierico": "Cleric", "druido": "Druid", "bardo": "Bard",
             "ranger": "Ranger", "paladino": "Paladin"}


def _k(nome: str) -> str:
    """Chiave di confronto dei nomi inglesi: apostrofi, trattini e barre non contano."""
    return re.sub(r"[^a-z0-9]+", " ", nome.lower().replace("’", "'").replace("'", "")).strip()


def _liste_prd() -> dict:
    li = M.toml("sistemi/pf1e/dati/liste_incantesimi.toml")["liste"]
    return {cl: {int(lv): {_k(n) for n in nomi} for lv, nomi in livelli.items()} for cl, livelli in li.items()}


def liste_35_in_pf1e() -> dict:
    """Le liste classe × funzione del 3.5 che il plugin pf1e riusa: il livello PF1e torna?"""
    lxi = {k: v for k, v in M.lessico("scripts/lessico_it_35.tsv", "srd35").get("incantesimo", {}).items()}
    lxp = {k: v for k, v in M.lessico("scripts/lessico_it_pf1.tsv", "pf1").get("incantesimo", {}).items()}
    prd = _liste_prd()
    inc = M.toml("sistemi/dnd35/dati/incantesimi.toml")["liste"]
    sposta = M.toml("sistemi/pf1e/dati/incantesimi.toml").get("livello_pf1e", {})
    voci, sb, nv, assenti = 0, [], [], 0
    for cl, funzioni in inc.items():
        lista = prd.get(CLASSE_EN.get(cl, "").lower(), {})
        for fn, livelli in funzioni.items():
            for lv, nomi in livelli.items():
                for n in nomi:
                    voci += 1
                    en = _k(lxp.get(n.lower()) or lxi.get(n.lower()) or "")
                    if not en:
                        nv.append(f"{cl}.{fn}.{lv}: {n}")
                        continue
                    dove = sorted(l for l, xs in lista.items() if en in xs)
                    lv_pf1e = sposta.get(cl, {}).get(n, int(lv))   # il plugin pf1e lo sposta o lo toglie
                    if lv_pf1e == -1 and not dove:
                        continue
                    if lv_pf1e not in dove:
                        if not dove:
                            assenti += 1
                        sb.append({"riga": f"{cl}.{fn} {lv}°", "campo": n,
                                   "plugin": f"{en} al {lv_pf1e}°",
                                   "fonte": f"PF1e al {dove[0]}°" if dove else "non nella lista PF1e della classe"})
    return _riga("liste d'incantesimi 3.5 riusate dal plugin pf1e (livello PF1e)", voci, voci,
                 voci - len(sb) - len(nv), sb, nv=nv,
                 nota=f"{assenti} incantesimi non sono nella lista PF1e della classe; gli altri sono a un livello diverso")


def solo_pf1e() -> dict:
    prd = _liste_prd()
    solo = M.toml("sistemi/pf1e/dati/incantesimi.toml")["solo"]
    tutti = {n for lista in prd.values() for xs in lista.values() for n in xs}
    voci, sb, nv = 0, [], []
    for cl, livelli in solo.items():
        lista = prd.get(CLASSE_EN.get(cl, "").lower(), {})
        for lv, coppie in livelli.items():
            for it, en in coppie:
                voci += 1
                if _k(en) not in tutti:
                    nv.append(f"{cl} {lv}°: {it} ({en}, non nel PRD in cache)")
                    continue
                dove = sorted(l for l, xs in lista.items() if _k(en) in xs)
                if int(lv) not in dove:
                    sb.append({"riga": f"{cl} {lv}°", "campo": it, "plugin": f"{en} al {lv}°",
                               "fonte": f"al {dove[0]}°" if dove else "non nella lista della classe"})
    return _riga("incantesimi «solo PF1e» (APG) per classe e livello", voci, voci, voci - len(sb) - len(nv), sb, nv=nv)


# ------------------------------------------------------------------ 3.5

def tesoro_35_letto(base) -> dict:
    testo = (base / M.SRD / "basic-rules-and-legal/treasure.md").read_text(encoding="utf-8")
    tab = M.tabelle(testo)["Table: Treasure Values per Encounter"]
    fonte = {}
    for r in tab[1:]:
        for i in (0, 2):
            if len(r) > i + 1 and M.num(r[i]) is not None:
                fonte[M.num(r[i])] = _n(r[i + 1])
    plugin = {}
    for riga in (ROOT / "scripts/loot_tables.yaml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s+(\d+):\s*\{\s*gp:\s*(\d+)", riga)
        if m:
            plugin[int(m.group(1))] = int(m.group(2))
    sb = [{"riga": f"EL {k}", "campo": "mo", "plugin": plugin.get(k), "fonte": v}
          for k, v in sorted(fonte.items()) if k in plugin and plugin[k] != v]
    mancanti = [k for k in fonte if k not in plugin]
    cop = len(fonte) - len(mancanti)
    return _riga("tesoro per livello d'incontro (SRD Treasure Values per Encounter)", len(fonte), cop,
                 cop - len(sb), sb, mancanti,
                 nota="le colonne coins_pct/goods_pct/items_pct di loot_tables.yaml non sono nella fonte")


# ------------------------------------------------------------------ talenti dei PNG generati

#: Talenti di un PNG al 7° livello di una sola classe, contati a mano sul manuale
#: (non dai dati del plugin, che sono ciò che si misura). Generali: 3.5 1 + 7//3 = 3,
#: PF1e (7+1)//2 = 4. Poi i bonus e i concessi della tabella e del testo della classe.
#: Senza il talento umano: il generatore non sceglie la razza.
ATTESI_7 = {
    "dnd35": {
        "guerriero": (7, "3 + bonus al 1°, 2°, 4°, 6°"),
        "mago": (5, "3 + Scrivere Pergamene + bonus al 5°"),
        "chierico": (3, "3"), "ladro": (3, "3"), "paladino": (3, "3"), "barbaro": (3, "3"),
        "bardo": (3, "3"), "druido": (3, "3"), "stregone": (3, "3"),
        "ranger": (7, "3 + Seguire Tracce + Resistenza Fisica + stile al 2° e al 6°"),
        "monaco": (7, "3 + Colpo Senz'Armi Migliorato + bonus al 1°, 2°, 6°"),
    },
    "pf1e": {
        "fighter": (8, "4 + bonus al 1°, 2°, 4°, 6°"),
        "wizard": (6, "4 + Scribe Scroll + bonus al 5°"),
        "cleric": (4, "4"), "rogue": (4, "4"), "paladin": (4, "4"), "barbarian": (4, "4"), "bard": (4, "4"),
        "druid": (4, "4"), "oracle": (4, "4"), "summoner": (4, "4"), "witch": (4, "4"), "antipaladin": (4, "4"),
        "ninja": (4, "4"), "slayer": (4, "4"), "investigator": (4, "4"), "shaman": (4, "4"), "arcanist": (4, "4"),
        "ranger": (7, "4 + Endurance + combat style al 2° e al 6°"),
        "monk": (9, "4 + Improved Unarmed Strike + Stunning Fist + bonus al 1°, 2°, 6°"),
        "sorcerer": (6, "4 + Eschew Materials + talento di stirpe al 7°"),
        "alchemist": (6, "4 + Brew Potion + Throw Anything"),
        "cavalier": (6, "4 + teamwork del Tactician al 1° + bonus al 6°"),
        "gunslinger": (6, "4 + Gunsmithing + bonus al 4°"),
        "inquisitor": (6, "4 + teamwork al 3° e al 6°"),
        "magus": (5, "4 + bonus al 5°"), "samurai": (5, "4 + bonus al 6°"), "swashbuckler": (5, "4 + bonus al 4°"),
        "skald": (5, "4 + Scribe Scroll"),
        "brawler": (7, "4 + Improved Unarmed Strike + combat al 2° e al 5°"),
        "hunter": (7, "4 + Precise Companion al 2° + teamwork al 3° e al 6°"),
        "warpriest": (7, "4 + Weapon Focus + bonus al 3° e al 6°"),
        "bloodrager": (6, "4 + Eschew Materials al 4° + talento di stirpe al 6°"),
    },
}


def _png(sistema: str, cl: str):
    """(statblocco, conto) di un PNG di 7° livello, come lo fa genera_creatura.main."""
    import genera_creatura as G  # noqa: E402
    from dmcore import sistemi as S
    from dmcore import creature_pf1e as CP
    rng = random.Random(1)
    if sistema == "pf1e":
        classi = CP.leggi_classi(f"{cl}:7", S.dati("pf1e", "creature.costruzione"))
        return G.genera_png_pf1e(7, classi=classi, rng=rng)
    try:
        return G.genera(7, classe=G._classe(f"{cl}:7"), rng=rng, talenti="dnd35")
    except TypeError:   # generatore di prima del lotto 3, per la misura «prima»
        return G.genera(7, classe=G._classe(f"{cl}:7"), rng=random.Random(1))


def _elenco(blocco: str) -> "list[str]":
    m = re.search(r"Talenti:\s*([^\n|]+)", blocco)
    return [re.sub(r"\s*\(.*\)$", "", t).strip() for t in re.split(r",\s*(?![^()]*\))", m.group(1))
            if t.strip()] if m else []


def talenti_generati() -> list:
    """Quanti talenti ha il PNG (contro il manuale) e se ogni talento generale è lecito."""
    import genera_creatura as G  # noqa: E402
    from dmcore import talenti as TL

    out = []
    for sistema, attesi in ATTESI_7.items():
        sb, cop, illeciti, nv, nv_pre, controllati = [], 0, [], [], [], 0
        for cl, (atteso, perche) in attesi.items():
            try:
                blocco, conto = _png(sistema, cl)
            except Exception as e:  # pragma: no cover — la misura dice dove si rompe
                cop += 1
                sb.append({"riga": cl, "campo": "talenti", "plugin": f"errore {type(e).__name__}", "fonte": "—"})
                continue
            nomi = _elenco(G.rendi(blocco))
            cop += 1
            if len(nomi) != atteso:
                sb.append({"riga": f"{cl} 7°", "campo": "talenti", "plugin": len(nomi), "fonte": f"{atteso} ({perche})"})
            st = getattr(conto, "talenti", None)
            if not st:   # generatore di prima del lotto 3: non tiene BAB e livelli per i talenti
                nv_pre.append(f"{cl}: il generatore non dà BAB e livelli, prerequisiti non ricontrollabili")
                continue
            controllati += 1
            car = {k: int(v) for k, v in re.findall(r"\b(For|Des|Cos|Int|Sag|Car)\s+(\d+)", blocco.attributi)}
            origini = dict(re.findall(r"([^;—]+?) \[([^\]]+)\]", next((r for r in conto.righe
                                                                       if r.startswith("talenti:") and "[" in r), "")))
            presi: "list[str]" = []
            for it in nomi:
                en = TL.nome_inglese(sistema, it)
                if en is None:
                    nv.append(f"{cl}: «{it}» non è nei dati dei talenti")
                    continue
                if origini.get(it.strip()) == "generale":
                    m = TL.manca(sistema, en, TL.Stato(car, st.get("bab", 0), st.get("livelli", {}),
                                                       st.get("lic", 0), list(presi)))
                    if m:
                        illeciti.append({"riga": f"{cl} 7°", "campo": it, "plugin": "preso", "fonte": "manca " + ", ".join(m)})
                presi.append(en)
        out.append((sistema, _riga("uso: numero di talenti dei PNG generati (7° livello, ogni classe)", len(attesi), cop,
                                   cop - len(sb), sb, nv=nv,
                                   nota="atteso contato a mano sul manuale (ATTESI_7), non dai dati del plugin")))
        out.append((sistema, _riga("uso: prerequisiti dei talenti generali dei PNG generati", len(attesi), cop,
                                   controllati - len({x["riga"] for x in illeciti}), illeciti, nv=nv_pre,
                                   nota="ogni talento generale ricontrollato coi prerequisiti della fonte, "
                                        "nell'ordine in cui è stato preso")))
    return out


# ------------------------------------------------------------------ classi di prestigio PF1e

#: Una via d'ingresso legale per ogni classe di prestigio, costruita a mano sul
#: manuale (BAB, incantesimi e capacità delle classi messe prima), non dai dati.
INGRESSI_PRESTIGIO = {
    "arcane archer": "fighter:6,wizard:1,arcane archer:1", "arcane trickster": "rogue:3,wizard:3,arcane trickster:1",
    "assassin": "rogue:5,assassin:1", "battle herald": "cavalier:4,battle herald:1",
    "dragon disciple": "sorcerer:5,dragon disciple:1", "duelist": "fighter:6,duelist:1",
    "eldritch knight": "fighter:1,wizard:5,eldritch knight:1", "holy vindicator": "cleric:7,holy vindicator:1",
    "horizon walker": "ranger:5,horizon walker:1", "loremaster": "wizard:7,loremaster:1",
    "master chymist": "alchemist:7,master chymist:1", "master spy": "rogue:5,master spy:1",
    "mystic theurge": "cleric:3,wizard:3,mystic theurge:1", "nature warden": "druid:6,nature warden:1",
    "pathfinder chronicler": "bard:5,pathfinder chronicler:1", "rage prophet": "barbarian:4,oracle:2,rage prophet:1",
    "shadowdancer": "rogue:5,shadowdancer:1", "stalwart defender": "fighter:7,stalwart defender:1",
}


def prestigio_pf1e(base) -> list:
    """Requisiti letti (BAB e talenti contro una seconda lettura del PRD) e usati dal generatore."""
    import genera_creatura as G  # noqa: E402
    from dmcore import sistemi as S
    from dmcore import creature_pf1e as CP
    from dmcore import talenti as TL
    req = M.toml("sistemi/pf1e/dati/talenti.toml").get("requisiti", {})
    classi = {k: v for k, v in M.toml("sistemi/pf1e/dati/classi.toml")["classi"].items() if v["gruppo"] == "prestigio"}
    sb, mancanti = [], [k for k in classi if k not in req]
    for nome, v in classi.items():
        if nome not in req:
            continue
        c = M._db(base, v["libro"])
        sid = c.execute("select section_id from sections where lower(name)=? and type='class'", (nome,)).fetchone()[0]
        voci = {n: re.sub(r"<[^>]+>", " ", b or d or "") for n, b, d in c.execute(
            "select name, body, description from sections where parent_id=(select section_id from sections "
            "where parent_id=? and name like 'Requirement%')", (sid,))}
        bab = int(re.search(r"\+(\d+)", voci["Base Attack Bonus"]).group(1)) if "Base Attack Bonus" in voci else 0
        if bab != req[nome].get("bab", 0):
            sb.append({"riga": nome, "campo": "BAB", "plugin": req[nome].get("bab", 0), "fonte": bab})
        nomi = set(req[nome].get("talenti", [])) | {x for o in req[nome].get("oppure", []) for x in o}
        for n in nomi:
            if n.lower().replace("-", " ") not in voci.get("Feats", "").lower().replace("-", " "):
                sb.append({"riga": nome, "campo": "talento", "plugin": n, "fonte": voci.get("Feats", "—")})
    righe = [_riga("requisiti delle classi di prestigio (BAB e talenti contro il PRD)", len(classi),
                   len(classi) - len(mancanti), len(classi) - len(mancanti) - len({x["riga"] for x in sb}), sb, mancanti,
                   nota="gradi, allineamento, imprese e capacità particolari restano «da verificare dal DM»")]
    sb2, nv = [], []
    cos = S.dati("pf1e", "creature.costruzione")
    for nome, via in INGRESSI_PRESTIGIO.items():
        try:
            sb_, conto = G.genera_png_pf1e(9, classi=CP.leggi_classi(via, cos), rng=random.Random(1),
                                           ruolo="tiratore" if nome == "arcane archer" else "bruto")
        except Exception as e:  # pragma: no cover
            sb2.append({"riga": nome, "campo": via, "plugin": f"errore {type(e).__name__}", "fonte": "—"})
            continue
        testo = "\n".join(conto.righe)
        if nome not in req:
            sb2.append({"riga": nome, "campo": via, "plugin": "requisiti non verificati", "fonte": "PRD Requirements"})
            continue
        if "✗" in testo:
            sb2.append({"riga": nome, "campo": via, "plugin": "requisito mancato", "fonte": "via legale"})
        presi = {TL.nome_inglese("pf1e", t) for t in _elenco(G.rendi(sb_))}
        r = req.get(nome, {})
        dovuti = list(r.get("talenti", [])) + [o[0] for o in r.get("oppure", [])]
        manca = [t for t in dovuti if t not in presi]
        if manca:
            sb2.append({"riga": nome, "campo": via, "plugin": "senza " + ", ".join(manca), "fonte": "talenti richiesti"})
        if r.get("gradi") or r.get("altro"):
            nv.append(f"{nome}: gradi o requisiti non numerici, da verificare dal DM")
    righe.append(_riga("uso: PNG con classe di prestigio, via d'ingresso legale (requisiti ✓, talenti presi)",
                       len(INGRESSI_PRESTIGIO), len(INGRESSI_PRESTIGIO),
                       len(INGRESSI_PRESTIGIO) - len({x["riga"] for x in sb2}), sb2,
                       nota=f"{len(nv)} classi hanno anche requisiti che il generatore non verifica (gradi, allineamento…)"))
    return righe


# ------------------------------------------------------------------ nomi italiani nel lessico

def nomi_nel_lessico(base) -> list:
    out = []
    lxp = M.lessico("scripts/lessico_it_pf1.tsv", "pf1")
    lx3 = M.lessico("scripts/lessico_it_35.tsv", "srd35")
    en_p = {t: {_k(v) for v in d.values()} for t, d in lxp.items()}
    en_3 = {t: {_k(v) for v in d.values()} for t, d in lx3.items()}
    c = M._db(base, "cr")
    cond = [r[0] for r in c.execute("select name from sections where parent_id=5238")]
    talenti = [r[0] for r in c.execute("select name from sections where type='feat'")]
    inc = [r[0] for r in c.execute("select name from sections where type='spell'")]
    for nome, voci, tipo in (("condizioni (PRD)", cond, "condizione"), ("talenti del Core (PRD)", talenti, "talento"),
                             ("incantesimi del Core (PRD)", inc, "incantesimo")):
        manc = sorted(v for v in set(voci) if _k(v) not in en_p.get(tipo, set()))
        n = len(set(voci))
        out.append(("pf1e", _riga(f"nomi italiani: {nome}", n, n - len(manc), n - len(manc), [], manc)))
    srd = base / M.SRD / "basic-rules-and-legal"
    testo = (srd / "special-abilities-and-conditions.md").read_text(encoding="utf-8")
    sez = testo.split("## Conditions", 1)[1]
    cond35 = re.findall(r"^\*\*([A-Z][A-Za-z -]+):\*\*", sez, flags=re.M)
    feat35 = [re.sub(r"\s*<small>.*", "", h).strip()
              for h in re.findall(r"^### (.+\[.+)$", (srd / "feats.md").read_text(encoding="utf-8"), flags=re.M)]
    feat35 = [f for f in feat35 if f != "Feat Name"]
    for nome, voci, tipo in (("condizioni (SRD)", cond35, "condizione"), ("talenti (SRD feats.md)", feat35, "talento")):
        manc = sorted(v for v in set(voci) if _k(v) not in en_3.get(tipo, set()))
        n = len(set(voci))
        out.append(("dnd35", _riga(f"nomi italiani: {nome}", n, n - len(manc), n - len(manc), [], manc)))
    return out


# ------------------------------------------------------------------ lotto 5: tratti dei tipi

#: SRD 3.5 e PRD, «Types»: chi non ha Costituzione e chi non ha Intelligenza.
#: Il costrutto è «di norma senza mente» (le due fonti: «most constructs are
#: mindless»), melma e parassita lo sono per tratto.
SENZA_COS = {"construct", "undead"}
SENZA_INT = {"construct", "ooze", "vermin"}


def _bonus_costrutto_srd(base) -> dict:
    """SRD 3.5, Construct Traits: la tabella dei pf bonus per taglia, letta dalla cache."""
    testo = (base / M.SRD / "basic-rules-and-legal/types-subtypes-and-special-abilities.md").read_text(encoding="utf-8")
    riga = next(r for r in testo.splitlines() if "Construct Size" in r and "<table" in r)
    celle = [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td>(.*?)</td>", riga)]
    coppie = dict(zip(celle[0::2], celle[1::2]))
    return {k.lower(): (0 if v in ("—", "-") else int(v)) for k, v in coppie.items() if k}


BONUS_COSTRUTTO: dict = {}
TIPI_MISURATI = ("aberration", "animal", "construct", "dragon", "elemental", "fey", "giant",
                 "humanoid", "magical beast", "monstrous humanoid", "ooze", "outsider", "plant",
                 "undead", "vermin")


def _mostro(sistema: str, tipo: str, gs: int, taglia: str = "medium"):
    """Il mostro come lo fa genera_creatura.main (ruolo bruto, seme 1)."""
    import genera_creatura as G  # noqa: E402
    from dmcore import sistemi as S
    from dmcore import creature_pf1e as CP
    rng = random.Random(1)
    try:
        sb, conto = G.genera(gs, tipo=tipo, taglia=taglia, ruolo="bruto", rng=rng,
                             talenti=None if sistema == "pf1e" else "dnd35")
    except TypeError:
        sb, conto = G.genera(gs, tipo=tipo, taglia=taglia, ruolo="bruto", rng=rng)
    if sistema == "pf1e":
        try:
            sb, righe = CP.converti(sb, tipo, taglia, pf_bersaglio=G.bersaglio_di(gs, "bruto", False)[0]["pf"])
        except TypeError:   # converti di prima del lotto 5
            sb, righe = CP.converti(sb, tipo, taglia)
        voce = S.dati("pf1e", "creature.costruzione")["tipi"].get(tipo, {})
        if getattr(conto, "talenti", None) and voce:
            conto.talenti["bab"] = int(voce["bab"] * conto.talenti["dv"])
        if hasattr(G, "applica_talenti"):
            G.applica_talenti(sb, conto, "pf1e", "bruto", rng)
    return sb


def _difetti_tipo(sistema: str, tipo: str, sb, taglia: str = "medium") -> "list[str]":
    from dmcore import tabelle as T
    car = dict(re.findall(r"(For|Des|Cos|Int|Sag|Car)\s+(\S+)", sb.attributi))
    dv, dado = (int(x) for x in re.match(r"(\d+)d(\d+)", sb.pf_dado).groups())
    out = []
    if (car.get("Cos") == "—") != (tipo in SENZA_COS):
        out.append(f"Cos {car.get('Cos')}")
    if (car.get("Int") == "—") != (tipo in SENZA_INT):
        out.append(f"Int {car.get('Int')}")
    talenti = next((v.split(":", 1)[1].strip() for v in sb.voci if v.startswith("Talenti:")), "")
    if tipo in SENZA_INT and talenti not in ("", "—"):
        out.append(f"talenti a un senza mente: {talenti}")
    if tipo in SENZA_COS:
        mod = 0
        if sistema == "pf1e" and tipo == "undead":
            mod = (int(car["Car"]) - 10) // 2
        atteso = int(dv * (dado / 2 + 0.5) + mod * dv) + (BONUS_COSTRUTTO[taglia] if tipo == "construct" else 0)
        # Robustezza resta lecita: la si toglie prima del confronto
        robusto = 0
        if "Robustezza" in talenti:
            robusto = max(3, dv) if sistema == "pf1e" else 3
        if int(sb.pf) - robusto != atteso:
            out.append(f"pf {sb.pf} (la regola dà {atteso})")
        temp = int(re.search(r"Temp ([+-]\d+)", sb.ts).group(1))
        t_atteso = dv // 3 + mod
        if "tempra possente" in talenti.lower():
            t_atteso += 2
        if temp != t_atteso:
            out.append(f"Temp {temp:+d} (la regola dà {t_atteso:+d})")
    return out


def tratti_tipo(base) -> list:
    """Cos, Int, talenti, pf e Tempra dei mostri generati contro i tratti del tipo."""
    BONUS_COSTRUTTO.update(_bonus_costrutto_srd(base))
    out = []
    for sistema in ("dnd35", "pf1e"):
        sb_tot, cop = [], 0
        for tipo in TIPI_MISURATI:
            for gs in (3, 7, 12):
                cop += 1
                try:
                    d = _difetti_tipo(sistema, tipo, _mostro(sistema, tipo, gs))
                except Exception as e:  # noqa: BLE001 — un errore è un difetto
                    d = [f"errore {type(e).__name__}: {e}"]
                if d:
                    sb_tot.append({"riga": f"{tipo} GS {gs}", "campo": "tratti", "plugin": "; ".join(d),
                                   "fonte": "tratti del tipo"})
        out.append((sistema, _riga("tratti dei tipi nei mostri generati (Cos, Int, talenti, pf, Tempra)",
                                   cop, cop, cop - len(sb_tot), sb_tot)))
        sb_tot, cop = [], 0
        for taglia in BONUS_COSTRUTTO:
            cop += 1
            try:
                d = _difetti_tipo(sistema, "construct", _mostro(sistema, "construct", 7, taglia), taglia)
            except Exception as e:  # noqa: BLE001
                d = [f"errore {type(e).__name__}: {e}"]
            if d:
                sb_tot.append({"riga": f"costrutto {taglia} GS 7", "campo": "pf", "plugin": "; ".join(d),
                               "fonte": f"bonus +{BONUS_COSTRUTTO[taglia]}"})
        out.append((sistema, _riga("pf bonus dei costrutti per taglia (Construct Traits)",
                                   cop, cop, cop - len(sb_tot), sb_tot)))
    return out


# ------------------------------------------------------------------ insieme

def misura(base: Path) -> dict:
    out = {"dnd35": [], "pf1e": []}
    out["pf1e"].append(tracce_pf1e(base, "soglie PE (tre tracce)", 2743, "sistemi/pf1e/dati/pe.toml", "soglie"))
    out["pf1e"].append(px_per_gs(base))
    out["pf1e"].append(tracce_pf1e(base, "tesoro per incontro (tre velocità)", 3661,
                                   "sistemi/pf1e/dati/tesoro.toml", "mo_per_incontro"))
    out["pf1e"].append(statistiche_per_gs(base))
    out["pf1e"].append(formula_modificatore(base))
    out["pf1e"].append(liste_35_in_pf1e())
    out["pf1e"].append(solo_pf1e())
    out["dnd35"].append(tesoro_35_letto(base))
    for r in prestigio_pf1e(base):
        out["pf1e"].append(r)
    for sis, r in talenti_generati():
        out[sis].append(r)
    for sis, r in nomi_nel_lessico(base):
        out[sis].append(r)
    for sis, r in tratti_tipo(base):
        out[sis].append(r)
    return {"fonti": {"srd35": M.SRD, "prd": M.PRD}, "sistemi": out}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json")
    ap.add_argument("--md")
    a = ap.parse_args(argv)
    random.seed(1)
    m = misura(M.cache())
    testo = "\n".join(M.riepilogo(m))
    print(testo)
    if a.json:
        Path(a.json).write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if a.md:
        Path(a.md).write_text(testo + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
