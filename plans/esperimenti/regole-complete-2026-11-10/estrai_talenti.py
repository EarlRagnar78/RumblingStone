#!/usr/bin/env python3
"""estrai_talenti.py — i talenti e i talenti bonus delle classi, dalle fonti in cache.

Lotto 3 delle regole complete (richiesta del DM del 2026-11-10). Il generatore
di PNG dava un solo «talento firma», senza controllare i prerequisiti. Qui si
scrivono i dati che servono per farlo secondo la regola:

    sistemi/pf1e/dati/talenti.toml   dal PRD (devonjones/PSRD-Data@76ea4784)
    sistemi/dnd35/dati/talenti.toml  dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c)

Per ogni talento: nome italiano (lessico), tipi, prerequisiti letti dal testo
(caratteristiche, BAB, livello d'incantatore, livelli di classe, gradi, altri
talenti) e ciò che non si sa leggere in `altro`: un talento con `altro` non
vuoto il generatore non lo sceglie, perché non può dire se il PNG lo ha.
Per ogni classe: a quali livelli prende un talento bonus, da quale lista
(tipi o nomi, anche per livello) e quali talenti la tabella le concede per nome.

    python3 plans/esperimenti/regole-complete-2026-11-10/estrai_talenti.py          # scrive
    python3 plans/esperimenti/regole-complete-2026-11-10/estrai_talenti.py --check  # confronta

Stessa cache, stessi byte. Contenuto aperto OGL 1.0a.
"""
from __future__ import annotations

import argparse
import html
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "plans/esperimenti/sistemi-plugin-2026-11-07"))
import estrai_prd_pf1e as E  # noqa: E402

SRD = "srd-v3.5-md-c7f30a0ce11a"
LIBRI_PF1E = ("cr", "apg", "acg", "uc", "um", "arg", "ma", "ue", "b1", "b2", "b3", "b4",
              "gmg", "tech", "ucampaign", "ogl", "npc", "mc")
CAR = {"str": "For", "dex": "Des", "con": "Cos", "int": "Int", "wis": "Sag", "cha": "Car"}
#: le classi del generatore 3.5, col nome della tabella SRD
CLASSI_35 = {"barbarian": "barbaro", "bard": "bardo", "cleric": "chierico", "druid": "druido",
             "fighter": "guerriero", "monk": "monaco", "paladin": "paladino", "ranger": "ranger",
             "rogue": "ladro", "sorcerer": "stregone", "wizard": "mago"}
TIPI_DAL_TESTO = [("combat", "Combat"), ("metamagic", "Metamagic"), ("item creation", "Item Creation"),
                  ("teamwork", "Teamwork"), ("grit", "Grit"), ("critical", "Critical"), ("style", "Style"),
                  ("performance", "Performance")]


def _testo(x: "str | None") -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", x or "")).replace("\xa0", " ")


def _k(nome: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", nome.lower().replace("’", "'").replace("'", "")).strip()


def _lessico(file: str, col: str) -> dict:
    out = {}
    righe = [r.split("\t") for r in (ROOT / file).read_text(encoding="utf-8").splitlines()
             if r and not r.startswith("#")]
    t = righe[0]
    i_it, i_en, i_t = t.index("italiano"), t.index(col), t.index("tipo")
    for r in righe[1:]:
        if len(r) > i_t and r[i_t] == "talento":
            out.setdefault(_k(r[i_en]), r[i_it])
    return out


#: capacità di classe che i talenti chiedono come prerequisito; quali classi le
#: hanno, e da che livello, si legge dalle tabelle delle classi (`capacita_di_classe`)
CAPACITA_NOTE = {"channel energy", "channel positive energy", "channel negative energy", "ki pool",
                 "lay on hands", "mercy", "bardic performance", "rage", "wild shape",
                 "turn or rebuke creatures", "cast arcane spells", "cast divine spells", "cast spells"}


def prerequisiti(testo: str, noti: "dict[str, str]") -> dict:
    """«Str 13, Power Attack, base attack bonus +1.» → dict dei prerequisiti.
    `noti` = {chiave normalizzata: nome} dei talenti, per riconoscerli."""
    p = {"car": {}, "bab": 0, "lic": 0, "talenti": [], "classe": {}, "gradi": {}, "capacita": [], "altro": []}
    t = _testo(testo).strip().rstrip(".").strip()
    if not t or t.lower() in ("none", "—"):
        return p
    # «Light Armor Proficiency» è il talento «Armor Proficiency, Light» (PF1e)
    t = re.sub(r"\b(Light|Medium|Heavy) Armor Proficiency\b", lambda m: f"Armor Proficiency, {m.group(1)}", t)
    # i nomi con la virgola («Armor Proficiency, Light») non vanno spezzati
    segnaposto = {}
    for k, nome in sorted(noti.items(), key=lambda kv: -len(kv[1])):
        if "," in nome and nome in t:
            s = f"§{len(segnaposto)}§"
            segnaposto[s] = nome
            t = t.replace(nome, s)
    for pezzo in re.split(r",\s*|;\s*|\band\b\s+", t):
        pezzo = pezzo.strip().strip(".").strip()
        if not pezzo:
            continue
        for s, nome in segnaposto.items():
            pezzo = pezzo.replace(s, nome)
        if re.match(r"(weapon )?proficien(cy|t)\b", pezzo, re.I):
            continue  # il PNG usa le armi che conosce
        pezzo = re.sub(r"\s+with (?:the )?selected weapon$", "", pezzo, flags=re.I)
        low = pezzo.lower()
        cap = re.sub(r"^(?:the )?ability to |\s+(?:class feature|ability)$", "", low).strip()
        if cap in CAPACITA_NOTE:
            p["capacita"].append(cap)
            continue
        m = re.fullmatch(r"(str|dex|con|int|wis|cha)\s+(\d+)", low)
        if m:
            p["car"][CAR[m.group(1)]] = int(m.group(2))
            continue
        m = re.search(r"base attack bonus\s*\+?(\d+)", low)
        if m:
            p["bab"] = max(p["bab"], int(m.group(1)))
            continue
        m = re.search(r"caster level (\d+)", low)
        if m:
            p["lic"] = max(p["lic"], int(m.group(1)))
            continue
        m = re.fullmatch(r"(\d+)(?:st|nd|rd|th)[- ]level ([a-z ]+?)", low) or \
            re.fullmatch(r"([a-z ]+?) level (\d+)(?:st|nd|rd|th)", low)
        if m:
            a, b = m.groups()
            livello, classe = (int(a), b) if a.isdigit() else (int(b), a)
            p["classe"][classe.strip()] = livello
            continue
        m = re.fullmatch(r"([a-z ()\[\]]+?) (\d+) ranks?", low)
        if m:
            p["gradi"][m.group(1).strip()] = int(m.group(2))
            continue
        if low.startswith("proficiency with") or low.startswith("proficient with"):
            continue  # il PNG usa le armi che conosce
        base = _k(pezzo) if _k(pezzo) in noti else _k(re.sub(r"\s*\(.*\)$", "", pezzo))
        if base in noti:
            p["talenti"].append(noti[base])
            continue
        p["altro"].append(pezzo)
    return p


# ------------------------------------------------------------------ PF1e

def talenti_pf1e(base: Path) -> "dict[str, dict]":
    grezzi = {}
    for libro in LIBRI_PF1E:
        f = base / f"book-{libro}.db"
        if not f.exists():
            continue
        c = sqlite3.connect(f)
        for sid, nome in c.execute("select section_id, name from sections where type='feat' order by section_id"):
            if not nome or nome in grezzi:
                continue
            tipi = sorted({r[0] for r in c.execute("select feat_type from feat_types where section_id=?", (sid,))})
            pre = c.execute("select description from sections where parent_id=? and name like 'Prerequisite%'",
                            (sid,)).fetchone()
            grezzi[nome] = {"libro": libro, "sid": sid, "tipi": tipi, "pre": pre[0] if pre else ""}
    noti = {_k(n): n for n in grezzi}
    it = _lessico("scripts/lessico_it_pf1.tsv", "pf1")
    out = {}
    for nome, g in grezzi.items():
        p = prerequisiti(g["pre"], noti)
        if "Mythic" in g["tipi"]:   # solo per chi ha un grado mitico: un PNG del generatore non lo ha
            p["altro"].append("grado mitico (Mythic Adventures)")
        out[nome] = {"it": it.get(_k(nome), ""), "tipi": g["tipi"], "libro": g["libro"], **p}
    return out


def _nomi_nel_testo(testo: str, noti: "dict[str, str]") -> "list[str]":
    """I nomi di talento che compaiono nel testo, nell'ordine, il più lungo per primo."""
    nomi = sorted(set(noti.values()), key=len, reverse=True)
    rx = re.compile(r"\b(" + "|".join(re.escape(n).replace(r"\-", "[- ]").replace(r"\ ", "[- ]")
                                      for n in nomi) + r")\b", re.I)
    trovati = []
    for m in rx.finditer(testo):
        n = noti.get(_k(m.group(1)))
        if n is None:
            continue
        if n not in trovati:
            trovati.append(n)
    return trovati


def _livelli_da_testo(t: str) -> "list[int]":
    return [int(x) for x in re.findall(r"(\d+)(?:st|nd|rd|th)", t)]


#: «gains Improved Unarmed Strike as a bonus feat», «receives a teamwork feat as a bonus feat»,
#: «chooses either Precise Shot or Outflank as a bonus feat», «is treated as having the Rapid Shot feat»
_CONCESSO = re.compile(r"(?:gains?|receives?|gets?|is treated as having) (?:the )?([A-Z][\w'’ -]+?)(?: feat)?"
                       r"(?: as a bonus feat|, even if| even if)")
_TIPO_A_LIVELLO = re.compile(r"receives? (?:a|an|one|an additional) (teamwork|combat|metamagic|item creation|style) "
                             r"feat as a bonus feat", re.I)
_SCELTA = re.compile(r"chooses? either ([A-Z][\w'’ -]+?) or ([A-Z][\w'’ -]+?) as a bonus feat")
_STILE_35 = re.compile(r"(?:selects?|selected) (archery|two-weapon combat)[^.]*?treated as having the "
                       r"([A-Z][\w' -]+?) feat", re.I)


def _dal_testo(paragrafi: "list[tuple[str, str]]", livello_di: "dict[str, int]", noti: "dict[str, str]") -> dict:
    """Talenti dati dalle capacità di classe col loro testo, non dalla tabella.

    Si leggono solo le capacità che la colonna «Special» nomina (`livello_di`):
    domini, misteri, talenti del ladro e trucchi del ninja sono scelte, non
    talenti che ogni membro della classe ha. Il livello è quello della frase
    («At 1st level, …») o, se la frase non lo dice, quello della tabella.
    """
    out = {"concessi": {}, "tipi_livello": {}, "scelte": {}, "stili": {}}
    for intest, testo in paragrafi:
        base = livello_di.get(re.sub(r"\s*\(.*\)$", "", intest.strip().lower()))
        if base is None:
            continue
        for frase in re.split(r"(?<=[.!?])\s+", testo):
            lv = re.search(r"\bat (\d+)(?:st|nd|rd|th) level\b", frase, re.I)
            m = _STILE_35.search(frase)
            if m:   # 3.5: «If the ranger selects archery, he is treated as having the Rapid Shot feat»
                stile = "Archery" if m.group(1).lower() == "archery" else "Two-Weapon"
                n = noti.get(_k(m.group(2)))
                if n:
                    out["stili"].setdefault(stile, {}).setdefault(str(base), []).append(n)
                continue
            livello = str(int(lv.group(1)) if lv and "selected" not in frase else base)
            m = _TIPO_A_LIVELLO.search(frase)
            if m:
                out["tipi_livello"][livello] = [m.group(1).title()]
                continue
            m = _SCELTA.search(frase)
            if m:
                out["scelte"][livello] = [noti[_k(x)] for x in m.groups() if _k(x) in noti]
                continue
            m = _CONCESSO.search(frase)
            if m and noti.get(_k(m.group(1))) and not re.search(r"\b(?:if|who selects|that selects)\b", frase[:m.start()], re.I):
                n = noti[_k(m.group(1))]
                if n not in out["concessi"].setdefault(livello, []):
                    out["concessi"][livello].append(n)
    return out



def _unisci(livelli: list, concessi: dict, dt: dict) -> dict:
    """Aggiunge a livelli e concessi della tabella ciò che il testo delle capacità dà."""
    for lv, nomi in dt["concessi"].items():
        for n in nomi:
            if n not in concessi.setdefault(lv, []):
                concessi[lv].append(n)
    for lv in sorted({int(x) for x in list(dt["tipi_livello"]) + list(dt["scelte"])} - set(livelli)):
        livelli.append(lv)
    livelli.sort()
    return dt


def bonus_pf1e(base: Path, talenti: dict) -> "dict[str, dict]":
    noti = {_k(n): n for n in talenti}
    prog, _ = E._classi(base)
    out = {}
    for nome, _bab, _ts, _tipo, libro, tid in prog:
        c = sqlite3.connect(base / f"book-{libro}.db")
        sid, lft, rgt = c.execute("select section_id, lft, rgt from sections where lower(name)=? "
                                  "and type='class' order by section_id", (nome,)).fetchone()
        righe = E._righe(c.execute("select body from sections where section_id=?", (tid,)).fetchone()[0])
        testa = next(r for r in righe if r[0] == "Level")
        if "Special" not in testa:
            continue
        i = testa.index("Special")
        livelli, concessi = [], {}
        for r in righe:
            n = E._ordinale(r[0])
            if not n or len(r) <= i:
                continue
            for pezzo in re.split(r",\s*", r[i]):
                low = pezzo.lower().strip()
                if re.search(r"\b(bonus|combat style|teamwork|bloodline)( combat)? feats?\b", low):
                    livelli.append(n)
                elif _k(re.sub(r"\s*\(.*\)$", "", pezzo)) in noti:
                    concessi.setdefault(str(n), []).append(noti[_k(re.sub(r"\s*\(.*\)$", "", pezzo))])
        livello_di: "dict[str, int]" = {}
        for r in righe:
            n = E._ordinale(r[0])
            if n and len(r) > i:
                for pezzo in re.split(r",\s*", r[i]):
                    livello_di.setdefault(re.sub(r"\s*\(.*\)$", "", pezzo.strip().lower()), n)
        # solo le capacità della classe (figlie della classe o di «Class Features»), non quelle
        # di uno spirito, di un dominio o del compagno animale che stanno più in basso
        cf = [sid] + [x for (x,) in c.execute("select section_id from sections where parent_id=? "
                                              "and name='Class Features'", (sid,))]
        paragrafi = [(nm or "", _testo(b or d)) for nm, b, d in c.execute(
            f"select name, body, description from sections where parent_id in ({','.join('?' * len(cf))}) "
            "order by lft", cf)]
        dt = _unisci(livelli, concessi, _dal_testo(paragrafi, livello_di, noti))
        if not livelli and not concessi:
            continue
        voce = {"livelli": livelli, "tipi": [], "nomi": {}, "senza_prerequisiti": False, "concessi": concessi,
                "stili": {}, "tipi_livello": dt["tipi_livello"], "scelte": dt["scelte"],
                "fonte": f"book-{libro} {tid} (tabella della classe)"}
        corpi = c.execute("select section_id, parent_id, name, body, description from sections where lft>? and rgt<? "
                          "and (name like '%Bonus Feat%' or name like 'Combat Style%' or name like 'Teamwork Feat%' "
                          "or name like 'Bloodline Feat%') order by lft", (lft, rgt)).fetchall()
        figli = []
        for csid, _p, _n, _b, _d in corpi:
            figli += c.execute("select section_id, parent_id, name, body, description from sections "
                               "where parent_id=? and body is not null order by lft", (csid,)).fetchall()
        nomi_usati = []
        for csid, pid, cname, body, desc in list(corpi) + figli:
            testo = _testo(body or desc)
            if not testo.strip():
                continue
            nomi_usati.append(cname or "")
            padre = c.execute("select name from sections where section_id=?", (pid,)).fetchone()[0]
            # un elenco sotto una scelta (stile del ranger, stirpe dello stregone) è uno «stile»
            stile = None
            if pid != sid and padre and not re.search(r"feat", padre, re.I):
                stile = padre                          # stirpe: la sezione «Bonus Feats» sta sotto «Arcane»
            elif cname and not re.search(r"feat", cname, re.I):
                stile = cname                          # stile: «Archery» sta sotto «Combat Style Feat»
            low = testo.lower()
            dest = voce["stili"].setdefault(stile, {}) if stile else voce["nomi"]
            frase = re.search(r"(must be (?:selected|taken|chosen) from|must be|can choose|may choose|"
                              r"from (?:those listed as|the following list))(.{0,200})", low)
            zona = frase.group(2) if frase else ""
            if not stile and "following list" not in zona:
                voce["tipi"] = sorted(set(voce["tipi"]) | {t for chiave, t in TIPI_DAL_TESTO
                                                           if re.search(rf"\b{chiave}\b", zona)})
                if "spell mastery" in zona:
                    dest.setdefault("1", []).append("Spell Mastery")
            for blocco in re.split(r"(?=\bat \d+(?:st|nd|rd|th) level\b)", testo, flags=re.I):
                nomi = _nomi_nel_testo(blocco, noti)
                if len(nomi) >= 2 or (stile and nomi):
                    lv = re.match(r"\s*at (\d+)(?:st|nd|rd|th) level", blocco, re.I)
                    chiave = lv.group(1) if lv else "1"
                    dest.setdefault(chiave, [])
                    dest[chiave] += [x for x in nomi if x not in dest[chiave]]
            if "even if he does not have the normal prerequisites" in low or \
                    "without meeting the prerequisites" in low or "even if she does not meet" in low or \
                    "need not have any of the prerequisites" in low:
                voce["senza_prerequisiti"] = True
        if voce["stili"]:
            voce["tipi"] = []  # la lista è quella dello stile scelto
        if not voce["tipi"] and not voce["nomi"] and not voce["stili"] and any(
                "bonus combat feat" in x.lower() for r in righe if len(r) > i for x in [r[i]]):
            voce["tipi"] = ["Combat"]  # «Bonus combat feat» nella tabella (brawler)
        if nomi_usati:
            voce["fonte"] += f"; testo: {', '.join(sorted(set(x for x in nomi_usati if x)))}"
        out[nome] = voce
    return out


#: la capacità come la scrive la colonna «Special» delle tabelle; i canalizzatori
#: positivi o negativi accettano anche chi ha «channel energy» senza aggettivo
SPECIAL = {"channel energy": ("channel energy",), "channel positive energy": ("channel positive energy", "channel energy"),
           "channel negative energy": ("channel negative energy", "channel energy"), "ki pool": ("ki pool",),
           "lay on hands": ("lay on hands",), "mercy": ("mercy",), "bardic performance": ("bardic performance",),
           "rage": ("rage",), "wild shape": ("wild shape",),
           "turn or rebuke creatures": ("turn or rebuke undead", "turn undead", "rebuke undead")}


def _capacita(speciali: "dict[str, dict[int, list[str]]]", incantatori: "dict[str, dict[str, int]]") -> dict:
    """{capacità: {classe: primo livello}} dalle colonne «Special» e dalle griglie."""
    out = {}
    for cap, frasi in SPECIAL.items():
        for cl, livelli in speciali.items():
            for lv in sorted(livelli):
                if any(x.lower().strip().startswith(f) for x in livelli[lv] for f in frasi):
                    out.setdefault(cap, {})[cl] = lv
                    break
    for tipo in ("arcane", "divine"):
        out[f"cast {tipo} spells"] = dict(sorted(incantatori.get(tipo, {}).items()))
    out["cast spells"] = dict(sorted({**incantatori.get("arcane", {}), **incantatori.get("divine", {})}.items()))
    return out


def speciali_pf1e(base: Path) -> "dict[str, dict[int, list[str]]]":
    out = {}
    for nome, _bab, _ts, _tipo, libro, tid in E._classi(base)[0]:
        c = sqlite3.connect(base / f"book-{libro}.db")
        righe = E._righe(c.execute("select body from sections where section_id=?", (tid,)).fetchone()[0])
        testa = next(r for r in righe if r[0] == "Level")
        if "Special" in testa:
            i = testa.index("Special")
            out[nome] = {E._ordinale(r[0]): re.split(r",\s*", r[i]) for r in righe
                         if E._ordinale(r[0]) and len(r) > i}
    return out


def incantatori_pf1e(base: Path) -> "dict[str, dict[str, int]]":
    """{arcane|divine: {classe: primo livello con incantesimi}}: tipo dal testo «Spells» della classe nel PRD
    (la colonna magic_type di spell_lists dà «arcane» anche al chierico… degli ibridi), livello da classi.toml."""
    import tomllib
    dati = tomllib.loads((ROOT / "sistemi/pf1e/dati/classi.toml").read_text(encoding="utf-8"))
    tipo = {}
    for nome, _bab, _ts, _t, libro, _tid in E._classi(base)[0]:
        c = sqlite3.connect(base / f"book-{libro}.db")
        lft, rgt = c.execute("select lft, rgt from sections where lower(name)=? and type='class' "
                             "order by section_id", (nome,)).fetchone()
        corpo = c.execute("select body from sections where lft>? and rgt<? and name like 'Spell%' "
                          "and body is not null order by lft", (lft, rgt)).fetchone()
        m = re.search(r"\b(arcane|divine)\b", _testo(corpo[0]).lower()) if corpo else None
        if m:
            tipo[nome] = m.group(1)  # il PRD lo dice nel testo «Spells» della classe
    out = {}
    for cl, v in dati["incantatori"].items():
        g = dati["griglie"].get(v["griglia"], {})
        primo = min((int(k) for k, r in g.items() if any(r)), default=None)
        if primo and tipo.get(cl) in ("arcane", "divine"):
            out.setdefault(tipo[cl], {})[cl] = primo
    return out


# ------------------------------------------------------------------ 3.5

#: I file dei talenti dell'SRD 3.5 e il `libro` che ognuno scrive nei dati.
#: Fino al 2026-11-11 si leggeva solo feats.md: i talenti dei mostri (Multiattacco,
#: Attacco in Volo, Armatura Naturale Migliorata), epici, divini e psionici
#: dell'SRD restavano «ignoti» al controllo delle schede (ADR-0124).
FILE_TALENTI_35 = (("basic-rules-and-legal/feats.md", "srd"),
                   ("monsters/monster-feats.md", "srd-mostri"),
                   ("epic/epic-feats.md", "srd-epici"),
                   ("divine/divine-abilities-and-feats.md", "srd-divini"),
                   ("psionics/psionic-feats.md", "srd-psionici"))


def _blocchi_35(base: Path):
    """(libro, blocco) di ogni talento dei file dell'SRD, il primo file vince."""
    for rel, libro in FILE_TALENTI_35:
        f = base / SRD / rel
        if not f.exists():
            continue
        for b in re.split(r"\n#{2,3} ", f.read_text(encoding="utf-8"))[1:]:
            yield libro, b


def talenti_35(base: Path) -> "tuple[dict, set]":
    grezzi, guerriero = {}, set()
    for libro, b in _blocchi_35(base):
        testa = b.split("\n", 1)[0]
        m = re.match(r"(.+?)\s*<small>\[(.+?)\]</small>", testa)
        if not m or m.group(1) == "Feat Name":
            continue
        nome, tipi = m.group(1).strip(), [x.strip() for x in m.group(2).split(",")]
        if nome in grezzi:
            continue
        pre = re.search(r"\*\*Prerequisites?:\*\*\s*(.+)", b)
        grezzi[nome] = {"tipi": tipi, "pre": pre.group(1) if pre else "", "libro": libro}
        if re.search(r"fighter may select .+? as one of his fighter bonus feats", b, re.I):
            guerriero.add(nome)
    noti = {_k(n): n for n in grezzi}
    it = _lessico("scripts/lessico_it_35.tsv", "srd35")
    out = {}
    for nome, g in grezzi.items():
        tipi = g["tipi"] + (["Fighter"] if nome in guerriero else [])
        out[nome] = {"it": it.get(_k(nome), ""), "tipi": sorted(set(tipi)), "libro": g["libro"],
                     **prerequisiti(g["pre"], noti)}
    return out, guerriero


def speciali_35(base: Path) -> "dict[str, dict[int, list[str]]]":
    out = {}
    for f in ("character-classes-i.md", "character-classes-ii.md"):
        testo = (base / SRD / "basic-rules-and-legal" / f).read_text(encoding="utf-8")
        for sez in re.split(r"\n## ", testo)[1:]:
            nome = sez.split("\n", 1)[0].strip().lower()
            if nome not in CLASSI_35:
                continue
            tab = E._righe(next((t for t in re.findall(r"<table.*?</table>", sez, flags=re.S)
                                 if "Base Attack" in t), ""))
            testa = next((r for r in tab if r and r[0] == "Level"), None)
            if testa and "Special" in testa:
                i = testa.index("Special")
                out[CLASSI_35[nome]] = {E._ordinale(r[0]): re.split(r",\s*", r[i]) for r in tab
                                        if r and E._ordinale(r[0]) and len(r) > i}
    return out


def incantatori_35() -> "dict[str, dict[str, int]]":
    """Dal plugin 3.5 (griglie già misurate contro l'SRD, ADR-0121): primo livello con incantesimi."""
    import tomllib
    c = tomllib.loads((ROOT / "sistemi/dnd35/dati/creature.toml").read_text(encoding="utf-8"))
    arcani = {"mago", "stregone", "bardo"}
    out = {}
    for cl, v in c.get("incantatori", {}).items():
        if cl not in set(CLASSI_35.values()):
            continue
        g = c.get("griglie", {}).get(v["griglia"], {})
        primo = min((int(k) for k, r in g.items() if any(r[1:]) or (r and r[0] and cl not in ("bardo",))),
                    default=None)
        if primo:
            out.setdefault("arcane" if cl in arcani else "divine", {})[cl] = primo
    return out


def bonus_35(base: Path, talenti: dict) -> "dict[str, dict]":
    noti = {_k(n): n for n in talenti}
    out = {}
    for f in ("character-classes-i.md", "character-classes-ii.md"):
        testo = (base / SRD / "basic-rules-and-legal" / f).read_text(encoding="utf-8")
        for sez in re.split(r"\n## ", testo)[1:]:
            nome = sez.split("\n", 1)[0].strip().lower()
            if nome not in CLASSI_35:
                continue
            tab = E._righe(next((t for t in re.findall(r"<table.*?</table>", sez, flags=re.S)
                                 if "Base Attack" in t), ""))
            testa = next((r for r in tab if r and r[0] == "Level"), None)
            if not testa or "Special" not in testa:
                continue
            i = testa.index("Special")
            livelli, concessi = [], {}
            for r in tab:
                n = E._ordinale(r[0]) if r else None
                if not n or len(r) <= i:
                    continue
                for pezzo in re.split(r",\s*", r[i]):
                    low = pezzo.lower().strip()
                    if re.search(r"\bbonus feat\b", low):
                        livelli.append(n)
                    elif _k(re.sub(r"\s*\(.*\)$", "", pezzo)) in noti:
                        concessi.setdefault(str(n), []).append(noti[_k(re.sub(r"\s*\(.*\)$", "", pezzo))])
            livello_di: "dict[str, int]" = {}
            for r in tab:
                n = E._ordinale(r[0]) if r else None
                if n and len(r) > i:
                    for pezzo in re.split(r",\s*", r[i]):
                        livello_di.setdefault(re.sub(r"\s*\(.*\)$", "", pezzo.strip().lower()), n)
            paragrafi = [(m.group(1), m.group(2)) for m in
                         re.finditer(r"\*\*([^*]+?):\*\*(.+?)(?=\n\*\*|\n#|\Z)", sez, flags=re.S)]
            dt = _dal_testo(paragrafi, livello_di, noti)
            for st, per_lv in dt["stili"].items():   # ranger 3.5: lo stile dà un talento a quei livelli
                for lv in per_lv:
                    if int(lv) not in livelli:
                        livelli.append(int(lv))
            livelli.sort()
            _unisci(livelli, concessi, dt)
            if not livelli and not concessi:
                continue
            voce = {"livelli": livelli, "tipi": [], "nomi": {}, "senza_prerequisiti": False,
                    "concessi": concessi, "stili": dt["stili"], "tipi_livello": dt["tipi_livello"],
                    "scelte": dt["scelte"], "fonte": f"SRD 3.5 {f}, tabella e testo «{nome}»"}
            if dt["stili"]:
                voce["senza_prerequisiti"] = True   # «even if he does not have the normal prerequisites»
                voce["cumulativa"] = False          # a ogni livello lo stile dà quel talento, non una lista
            m = re.search(r"\*\*Bonus Feats?:\*\*(.+?)(?:\n\*\*|\n#)", sez, flags=re.S)
            t = (m.group(1) if m else "").lower()
            if nome == "fighter":
                voce["tipi"] = ["Fighter"]
            elif "metamagic" in t or "item creation" in t:
                voce["tipi"] = sorted({x for k, x in (("metamagic", "Metamagic"), ("item creation", "Item Creation"))
                                       if k in t})
                if "spell mastery" in t:
                    voce["nomi"]["1"] = ["Spell Mastery"]
            elif nome == "monk":
                # «At 1st level, a monk may choose either Improved Grapple or Stunning Fist…»
                for lv, a, b in re.findall(r"at (\d+)(?:st|nd|rd|th) level,? (?:he|she|a monk) may select either "
                                           r"([a-z' -]+?) or ([a-z' -]+?) as a bonus feat", t):
                    voce["nomi"][lv] = [noti[_k(x)] for x in (a, b) if _k(x) in noti]
                voce["senza_prerequisiti"] = "need not have any of the prerequisites" in t
                voce["cumulativa"] = False  # 3.5: a ogni livello si sceglie tra i due di quel livello
            out[CLASSI_35[nome]] = voce
    return out


# ------------------------------------------------------------------ requisiti delle classi di prestigio

def requisiti_pf1e(base: Path, talenti: dict) -> "dict[str, dict]":
    """I requisiti d'accesso delle classi di prestigio PF1e, dalla sezione «Requirements» del PRD.

    Letti: BAB, talenti per nome (anche «A or B»), gradi per abilità, livello
    d'incantesimo arcano o divino, «channel energy». Il resto (allineamento,
    razza, lingue, imprese, poteri d'ira, «any three metamagic feats»…) va in
    `altro`: il generatore lo scrive nel conto come cosa che decide il DM.
    """
    noti = {_k(n): n for n in talenti}
    classi = {k: v for k, v in _toml_classi().items() if v.get("gruppo") == "prestigio"}
    out = {}
    for nome, v in sorted(classi.items()):
        c = sqlite3.connect(base / f"book-{v['libro']}.db")
        sid = c.execute("select section_id from sections where lower(name)=? and type='class'", (nome,)).fetchone()[0]
        r = c.execute("select section_id from sections where parent_id=? and name like 'Requirement%'",
                      (sid,)).fetchone()
        req = {"bab": 0, "talenti": [], "oppure": [], "gradi": {}, "incantesimi": {}, "capacita": [], "altro": [],
               "armi": {}, "fonte": f"book-{v['libro']} {r[0]}"}
        for voce, body, desc in c.execute("select name, body, description from sections where parent_id=? "
                                          "order by lft", (r[0],)):
            t = re.sub(r"\s+", " ", _testo(body or desc)).strip().rstrip(".")
            if voce == "Base Attack Bonus":
                req["bab"] = int(re.search(r"\+(\d+)", t).group(1))
            elif voce == "Feats":
                for pezzo in re.split(r",\s*(?![^()]*\))", t):
                    intero = pezzo.strip()
                    arma = re.search(r"\((.*)\)$", intero)
                    pezzo = re.sub(r"\s*\(.*\)$", "", pezzo.strip())
                    if arma and noti.get(_k(pezzo)):
                        req["armi"][noti[_k(pezzo)]] = arma.group(1)
                    alternative = [noti.get(_k(x)) for x in re.split(r"\s+or\s+", pezzo)]
                    if all(alternative) and len(alternative) > 1:
                        req["oppure"].append(alternative)
                    elif all(alternative):
                        req["talenti"].append(alternative[0])
                    else:
                        req["altro"].append(f"talenti: {intero}")
            elif voce == "Skills":
                for pezzo in re.split(r",\s*(?![^()]*\))", t):
                    m = re.match(r"^(.+?) (\d+) ranks?$", pezzo.strip())
                    if m and "any" not in m.group(1).lower():
                        req["gradi"][m.group(1)] = int(m.group(2))
                    else:
                        req["altro"].append(f"gradi: {pezzo.strip()}")
            elif voce in ("Spells", "Spellcasting"):
                trovati = re.findall(r"(\d)(?:st|nd|rd|th)-level (arcane|divine) spells", t)
                for lv, tipo in trovati:
                    req["incantesimi"]["arcani" if tipo == "arcane" else "divini"] = int(lv)
                if not trovati or re.search(r"without preparation|mage hand|divination|draconic", t, re.I):
                    req["altro"].append(f"incantesimi: {t}")
            elif voce == "Special" and re.fullmatch(r"channel energy class feature", t, re.I):
                req["capacita"].append("channel energy")
            else:
                req["altro"].append(f"{voce.lower()}: {t}")
        out[nome] = req
    return out


def _toml_classi() -> dict:
    import tomllib
    with open(ROOT / "sistemi/pf1e/dati/classi.toml", "rb") as fh:
        return tomllib.load(fh)["classi"]


# ------------------------------------------------------------------ scrittura

def _q(x: str) -> str:
    return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _lista(xs) -> str:
    return "[" + ", ".join(_q(x) if isinstance(x, str) else str(x) for x in xs) + "]"


def _tabella(d: dict) -> str:
    return "{ " + ", ".join(f"{_q(k)} = {v if isinstance(v, int) else _q(v)}" for k, v in d.items()) + " }"


def scrivi(intestazione: str, talenti: dict, bonus: dict, capacita: dict, requisiti: "dict | None" = None) -> str:
    righe = [intestazione, ""]
    righe.append("# [capacita]: classi che hanno la capacità chiesta da un talento, e da quale livello")
    righe.append("# (colonna «Special» delle tabelle; per «cast … spells» la prima riga della griglia).")
    righe.append("[capacita]")
    for cap in sorted(capacita):
        righe.append(f"{_q(cap)} = {_tabella(capacita[cap])}")
    righe.append("")
    righe.append("# [talenti.\"Nome inglese\"]: it, tipi, prerequisiti (car, bab, lic, talenti, classe, gradi).")
    righe.append("# `altro` = prerequisiti che il testo dice e la regola non sa leggere: il generatore salta il talento.")
    righe.append("# [bonus.\"classe\"]: livelli dei talenti bonus, lista (tipi e nomi; nomi per livello d'ingresso),")
    righe.append("# senza_prerequisiti se la classe li ignora, concessi = talenti dati per nome dalla tabella o dal")
    righe.append("# testo delle capacità; tipi_livello e scelte = la lista di quel solo livello (tattico del cavaliere,")
    righe.append("# compagno preciso del cacciatore); stili = liste per stile di combattimento o stirpe.")
    righe.append("")
    for cl in sorted(bonus):
        v = bonus[cl]
        righe.append(f"[bonus.{_q(cl)}]")
        righe.append(f"livelli = {_lista(v['livelli'])}")
        righe.append(f"tipi = {_lista(v['tipi'])}")
        righe.append("nomi = { " + ", ".join(f"{_q(k)} = {_lista(x)}" for k, x in sorted(v["nomi"].items(), key=lambda kv: int(kv[0]))) + " }")
        righe.append(f"senza_prerequisiti = {'true' if v['senza_prerequisiti'] else 'false'}")
        righe.append(f"cumulativa = {'true' if v.get('cumulativa', True) else 'false'}")
        righe.append("concessi = { " + ", ".join(f"{_q(k)} = {_lista(x)}" for k, x in sorted(v["concessi"].items(), key=lambda kv: int(kv[0]))) + " }")
        for chiave in ("tipi_livello", "scelte"):
            if v.get(chiave):
                righe.append(f"{chiave} = {{ " + ", ".join(f"{_q(k)} = {_lista(x)}" for k, x in sorted(v[chiave].items(), key=lambda kv: int(kv[0]))) + " }")
        for st, nomi in sorted(v.get("stili", {}).items()):
            righe.append(f"stili.{_q(st)} = {{ " + ", ".join(f"{_q(k)} = {_lista(x)}" for k, x in sorted(nomi.items(), key=lambda kv: int(kv[0]))) + " }")
        righe.append(f"fonte = {_q(v['fonte'])}")
        righe.append("")
    if requisiti:
        righe.append("# [requisiti.\"classe di prestigio\"]: BAB, talenti (oppure = uno a scelta), gradi, livello")
        righe.append("# d'incantesimo arcano/divino, capacità; `altro` = ciò che decide il DM (allineamento, imprese…).")
        righe.append("")
        for cl in sorted(requisiti):
            r = requisiti[cl]
            righe.append(f"[requisiti.{_q(cl)}]")
            if r["bab"]:
                righe.append(f"bab = {r['bab']}")
            for k in ("talenti", "capacita", "altro"):
                if r[k]:
                    righe.append(f"{k} = {_lista(r[k])}")
            if r["oppure"]:
                righe.append("oppure = [" + ", ".join(_lista(x) for x in r["oppure"]) + "]")
            for k in ("gradi", "incantesimi", "armi"):
                if r[k]:
                    righe.append(f"{k} = {_tabella(r[k])}")
            righe.append(f"fonte = {_q(r['fonte'])}")
            righe.append("")
    for nome in sorted(talenti):
        t = talenti[nome]
        righe.append(f"[talenti.{_q(nome)}]")
        righe.append(f"it = {_q(t['it'])}")
        righe.append(f"tipi = {_lista(t['tipi'])}")
        righe.append(f"libro = {_q(t['libro'])}")
        for k in ("car", "classe", "gradi"):
            if t[k]:
                righe.append(f"{k} = {_tabella(t[k])}")
        for k in ("bab", "lic"):
            if t[k]:
                righe.append(f"{k} = {t[k]}")
        for k in ("talenti", "capacita", "altro"):
            if t.get(k):
                righe.append(f"{k} = {_lista(t[k])}")
        righe.append("")
    return "\n".join(righe)


def genera() -> "dict[Path, str]":
    prd = E.cache()
    srd = prd.parent / SRD
    t1 = talenti_pf1e(prd)
    b1 = bonus_pf1e(prd, t1)
    t3, _ = talenti_35(srd.parent)
    b3 = bonus_35(srd.parent, t3)
    return {
        ROOT / "sistemi/pf1e/dati/talenti.toml": scrivi(
            "# sistemi/pf1e/dati/talenti.toml — talenti PF1e e talenti bonus delle classi, dal PRD.\n"
            "# Generato da plans/esperimenti/regole-complete-2026-11-10/estrai_talenti.py (non a mano).\n"
            "# Fonte: devonjones/PSRD-Data@76ea4784, sezioni di tipo «feat» e tabelle delle classi. OGL 1.0a.",
            t1, b1, _capacita(speciali_pf1e(prd), incantatori_pf1e(prd)), requisiti_pf1e(prd, t1)),
        ROOT / "sistemi/dnd35/dati/talenti.toml": scrivi(
            "# sistemi/dnd35/dati/talenti.toml — talenti SRD 3.5 e talenti bonus delle classi.\n"
            "# Generato da plans/esperimenti/regole-complete-2026-11-10/estrai_talenti.py (non a mano).\n"
            "# Fonte: olimot/srd-v3.5-md@c7f30a0c, feats.md e character-classes-i/ii.md. OGL 1.0a.",
            t3, b3, _capacita(speciali_35(srd.parent), incantatori_35())),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    diversi = 0
    for f, testo in genera().items():
        if a.check:
            if not f.exists() or f.read_text(encoding="utf-8") != testo:
                print(f"✗ {f.relative_to(ROOT)} diverso da quello che il PRD/SRD in cache dà")
                diversi += 1
        else:
            f.write_text(testo, encoding="utf-8")
            print(f"✓ scritto {f.relative_to(ROOT)}")
    return 1 if diversi else 0


if __name__ == "__main__":
    sys.exit(main())
