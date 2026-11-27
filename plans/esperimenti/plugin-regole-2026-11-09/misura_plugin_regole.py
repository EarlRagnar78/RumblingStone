#!/usr/bin/env python3
"""misura_plugin_regole.py — quanto i plugin 3.5 e PF1e coprono le fonti, e se i numeri tornano.

Audit del 2026-11-09 (thread «Verificare i plugin di regole 3.5 e PF1e»).
`scripts/sistemi.py` dice quali capacità un plugin *dichiara*; questa misura
dice quanto di ogni tabella *c'è davvero* e se coincide con la fonte:

    SRD 3.5   olimot/srd-v3.5-md@c7f30a0c   (cache di riscontro_srd.py)
    PRD PF1e  devonjones/PSRD-Data@76ea4784 (cache di riscontro_srd.py)

Per ogni tabella: righe nella fonte, righe coperte dal plugin, righe giuste,
righe sbagliate (con il campo e i due valori) e campi che il plugin non ha.

    python3 plans/esperimenti/plugin-regole-2026-11-09/misura_plugin_regole.py
    … --json FILE      scrive la misura completa
    … --md FILE        scrive il rapporto in Markdown

Solo lettura, nessuna rete (la cache si riempie con
`python3 scripts/riscontro_srd.py scarica`). Stesso albero e stessa cache,
stesso risultato. Esce 0 sempre: è una misura, non un cancello.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sqlite3
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRD = "srd-v3.5-md-c7f30a0ce11a"
PRD = "PSRD-Data-76ea47846041"


def cache() -> Path:
    for c in (os.environ.get("RUMBLINGSTONE_SRD_CACHE"),
              os.path.join(os.environ["XDG_CACHE_HOME"], "rumblingstone", "srd")
              if os.environ.get("XDG_CACHE_HOME") else None,
              str(Path.home() / ".cache" / "rumblingstone" / "srd")):
        if c and (Path(c) / SRD).is_dir() and (Path(c) / PRD).is_dir():
            return Path(c)
    sys.exit("mancano le fonti in cache: python3 scripts/riscontro_srd.py scarica")


# ------------------------------------------------------------ tabelle HTML

class Tabelle(HTMLParser):
    """Tutte le <table> di un testo: {didascalia: [righe…]} (colspan espanso)."""

    def __init__(self):
        super().__init__()
        self.tab: dict[str, list] = {}
        self._cap = self._righe = self._r = self._c = None
        self._in_cap = False
        self._span = 1
        self._sup = 0

    def handle_starttag(self, t, a):
        if t == "table":
            self._righe, self._cap = [], ""
        elif t == "caption":
            self._in_cap = True
        elif t == "tr":
            self._r = []
        elif t in ("td", "th") and self._r is not None:
            self._c, self._span = [], int(dict(a).get("colspan") or 1)
        elif t == "br" and self._c is not None:
            self._c.append(" ")
        elif t == "sup":
            self._sup += 1   # i rimandi alle note («2<sup>1</sup>») non sono numeri della tabella

    def handle_endtag(self, t):
        if t == "sup":
            self._sup -= 1
        elif t == "caption":
            self._in_cap = False
        elif t in ("td", "th") and self._c is not None:
            v = re.sub(r"\s+", " ", "".join(self._c)).strip()
            self._r += [v] * self._span
            self._c = None
        elif t == "tr" and self._r is not None:
            if self._r:
                self._righe.append(self._r)
            self._r = None
        elif t == "table" and self._righe is not None:
            self.tab.setdefault(self._cap.strip(), self._righe)
            self._righe = None

    def handle_data(self, d):
        if self._sup:
            return
        if self._in_cap:
            self._cap += d
        elif self._c is not None:
            self._c.append(d)


def tabelle(testo: str) -> dict:
    p = Tabelle()
    p.feed(html.unescape(testo))
    return p.tab


def num(s: str) -> "int | None":
    m = re.match(r"^[+]?(-?\d+)", s.replace("–", "-").replace("−", "-").strip())
    return int(m.group(1)) if m else None


# ------------------------------------------------------------ righe di classe

ORDINALI = re.compile(r"^(\d+)(st|nd|rd|th)$")
COL_INC = {"0": 0, "1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5,
           "6th": 6, "7th": 7, "8th": 8, "9th": 9}


def classe_da_tabella(righe: list) -> dict:
    """BAB per livello, TS buoni, griglia degli incantesimi al giorno."""
    i_testa = next((i for i, r in enumerate(righe) if r and r[0] in ("Level", "NPC Level")), None)
    if i_testa is None:
        return {}
    testa = list(righe[i_testa])
    # Swashbuckler (ACG): la riga sopra con «Base Attack», «Fort», «Ref», «Will»
    # manca nel PRD, restano «Bonus», «Save», «Save», «Save»
    if testa[1:5] == ["Bonus", "Save", "Save", "Save"]:
        testa[1:5] = ["Base Attack Bonus", "Fort Save", "Ref Save", "Will Save"]
    # PRD: intestazione su due righe (rowspan), la seconda ha solo i livelli d'incantesimo
    dopo = righe[i_testa + 1] if i_testa + 1 < len(righe) else []
    # alchimista e investigatore: «Extracts per Day» al posto di «Spells per Day»
    testa = [c.replace("Extracts per Day", "Spells per Day") for c in testa]
    if dopo and all(c in COL_INC or c.startswith(("Spells", "Extracts")) for c in dopo):
        sotto = iter(c for c in dopo if c in COL_INC)
        testa = [next(sotto, c) if c.startswith("Spells per Day") else c for c in testa]
    i_bab = next(i for i, c in enumerate(testa) if c.startswith("Base Attack"))
    i_ts = {k: next(i for i, c in enumerate(testa) if c.startswith(n))
            for k, n in (("temp", "Fort"), ("rifl", "Ref"), ("vol", "Will"))}
    spazio = [r for r in righe if r[:1] and r[0] == "" and any("Spells per Day" in c for c in r)]
    i_inc = {}
    if spazio or any(c in COL_INC for c in testa):
        for i, c in enumerate(testa):
            if c in COL_INC and (not spazio or "Spells per Day" in spazio[0][i] if i < len(spazio[0] if spazio else []) else True):
                i_inc[COL_INC[c]] = i
    liv = {}
    for r in righe:
        m = ORDINALI.match(r[0]) if r else None
        if not m:
            continue
        n = int(m.group(1))
        if len(r) <= max(i_ts.values()):
            continue
        # PRD: una riga senza capacità speciali a volte omette la cella «Special»
        # (Hunter 16°), e le colonne degli incantesimi scivolano di uno
        i_sp = next((i for i, c in enumerate(testa) if c == "Special"), None)
        if (i_sp is not None and len(r) == len(testa) - 1 and i_sp < len(r)
                and re.fullmatch(r"\d+|—", r[i_sp].strip())):
            r = r[:i_sp] + [""] + r[i_sp:]
        bab = num(r[i_bab])
        ts = {k: num(r[i]) for k, i in i_ts.items()}
        griglia = {}
        for lv, i in i_inc.items():
            if i < len(r):
                v = r[i].split("+")[0].strip()
                if v.isdigit():
                    griglia[lv] = int(v)
        liv[n] = {"bab": bab, "ts": ts, "griglia": griglia}
    if not liv:
        return {}
    top = max(liv)
    bab = liv[top]["bab"] / top
    bab = 1.0 if bab >= 0.95 else 0.75 if bab >= 0.7 else 0.5
    # TS buono = progressione che all'ultimo livello supera quella scarsa (liv // 3)
    # (base 20°: +12 contro +6; prestigio 10°: +7 nel 3.5, +5 nel PF1e, contro +3). Il vecchio criterio
    # «≥ +2 al 1°» sbagliava le prestigio PF1e, che partono da +1 (segnalato dal
    # thread della #363).
    buoni = sorted(k for k, v in liv[top]["ts"].items() if v is not None and v > top // 3)
    return {"livelli": top, "bab": bab, "ts_buoni": buoni,
            "griglia": {n: liv[n]["griglia"] for n in sorted(liv) if liv[n]["griglia"]}}


def griglia_lista(g: dict) -> list:
    """{livello d'incantesimo: n} → lista come nel plugin (indice = livello, 0 finto se manca lo 0)."""
    if not g:
        return []
    alto = max(g)
    return [g.get(i, 0) for i in range(alto + 1)]


# ------------------------------------------------------------ fonti 3.5

def srd35(base: Path) -> dict:
    d = base / SRD
    classi, prestigio = {}, {}
    file_classi = {
        "base": ["basic-rules-and-legal/character-classes-i.md", "basic-rules-and-legal/character-classes-ii.md"],
        "png": ["basic-rules-and-legal/npc-classes.md"],
        "prestigio": ["basic-rules-and-legal/prestige-classes.md"],
    }
    for gruppo, files in file_classi.items():
        for f in files:
            testo = (d / f).read_text(encoding="utf-8")
            # ogni sezione «## Nome» con il suo Hit Die, punti abilità e tabella
            for sez in re.split(r"\n## ", testo)[1:]:
                nome = sez.split("\n", 1)[0].strip()
                dv = re.search(r"\*\*Hit Die:\*\*\s*d(\d+)", sez)
                pa = re.search(r"Skill Points at Each Additional Level:\*\*\s*(\d+)", sez)
                tab = {k: v for k, v in tabelle(sez).items() if k.startswith("Table: The ")}
                if not dv or not tab:
                    continue
                riga = classe_da_tabella(next(iter(tab.values())))
                riga.update(dv=int(dv.group(1)), gradi=int(pa.group(1)) if pa else None)
                conosciuti = tabelle(sez).get(f"Table: {nome} Spells Known")
                if conosciuti:
                    riga["conosciuti"] = classe_conosciuti(conosciuti)
                (prestigio if gruppo == "prestigio" else classi)[nome.lower()] = riga | {"gruppo": gruppo}
    # tipi
    t = tabelle((d / "monsters/improving-monsters.md").read_text(encoding="utf-8"))["Table: Creature Improvement by Type"]
    tipi = {}
    for r in t:
        if len(r) < 5 or not r[1].startswith("d"):
            continue
        bab = 1.0 if "fighter" in r[2] else 0.75 if "3/4" in r[2] else 0.5
        buoni = sorted({"Fort": "temp", "Ref": "rifl", "Will": "vol"}[x]
                       for x in re.findall(r"Fort|Ref|Will", r[3].split("(")[0]))
        tipi[r[0].lower()] = {"dv": int(r[1][1:]), "bab": bab, "ts_buoni": buoni,
                              "gradi": num(r[4]), "nota_ts": r[3]}
    # armature e scudi
    arm, scu = {}, {}
    gruppo = None
    for r in tabelle((d / "basic-rules-and-legal/equipment.md").read_text(encoding="utf-8"))["Table: Armor and Shields"]:
        if r[0] in ("Light armor", "Medium armor", "Heavy armor", "Shields", "Extras"):
            gruppo = r[0]
            continue
        if gruppo is None or len(r) < 4 or num(r[2]) is None:
            continue
        nome = re.sub(r"\d+$", "", r[0]).strip().lower()
        if gruppo == "Shields":
            scu[nome] = num(r[2])
        elif gruppo != "Extras":
            arm[nome] = {"ca": num(r[2]), "des_max": num(r[3])}
    # abilità: i titoli con la caratteristica chiave tra parentesi
    abil = set()
    for f in ("skills-i.md", "skills-ii.md"):
        abil |= set(re.findall(r"^#{2,3} (.+?)\s*(?:<small>)?\((?:Str|Dex|Con|Int|Wis|Cha|None)\b",
                               (d / "basic-rules-and-legal" / f).read_text(encoding="utf-8"), re.M))
    # liste di classe: {classe: {livello: {nome inglese minuscolo}}}
    liste: dict = {}
    for f in ("spell-list-i.md", "spell-list-ii.md"):
        classe = None
        liv = None
        for riga in (d / "spells" / f).read_text(encoding="utf-8").splitlines():
            m = re.match(r"^## (\w[\w/]*) Spells\s*$", riga)
            if m:
                classe, liv = m.group(1).lower(), None
                continue
            if riga.startswith("## "):
                classe = None
            m = re.match(r"^### (\d)(?:st|nd|rd|th)?-Level ", riga)
            if m and classe:
                liv = int(m.group(1))
                continue
            m = re.match(r"^\*\*(.+?):?\*\*", riga)
            if m and classe and liv is not None:
                liste.setdefault(classe, {}).setdefault(liv, set()).update(_varianti(m.group(1)))
            # incantesimi di dominio del chierico (tabelle per livello)
            for lv, nome in re.findall(r"<td>(\d)</td><td><strong>(.+?):?</strong>", riga):
                liste.setdefault("dominio", {}).setdefault(int(lv), set()).update(_varianti(nome))
    return {"classi": classi, "prestigio": prestigio, "tipi": tipi, "armature": arm, "scudi": scu,
            "abilita": sorted(abil), "liste": liste}


def _varianti(nome: str) -> set:
    """«Protection from Chaos/Evil» → le due voci; «Blindness/Deafness» resta anche intera."""
    n = _norm(nome)
    out = {n}
    m = re.match(r"^(.* )(\w+)/(\w+)$", n)
    if m:
        out |= {m.group(1) + m.group(2), m.group(1) + m.group(3)}
    return out


def _norm(nome: str) -> str:
    """Nome d'incantesimo confrontabile: minuscolo, apostrofi dritti, senza «, Mass» spostato."""
    n = re.sub(r"<sup>.*?</sup>", "", nome).replace("*", "")
    n = n.lower().replace("’", "'").replace("-", "/").strip().rstrip(":").strip()
    m = re.match(r"^(.+), (mass|greater|lesser|communal)$", n)
    return f"{m.group(2)} {m.group(1)}" if m else n


def classe_conosciuti(righe: list) -> dict:
    i = next(i for i, r in enumerate(righe) if r and r[0] in ("Level", "NPC Level"))
    testa = list(righe[i])
    # PRD: la seconda riga d'intestazione ha solo i livelli d'incantesimo
    if i + 1 < len(righe) and all(c in COL_INC for c in righe[i + 1]):
        testa = [testa[0]] + list(righe[i + 1])
    out = {}
    for r in righe:
        m = ORDINALI.match(r[0]) if r else None
        if m:
            out[int(m.group(1))] = {COL_INC[c]: int(r[i]) for i, c in enumerate(testa)
                                    if c in COL_INC and i < len(r) and r[i].isdigit()}
    return out


# ------------------------------------------------------------ fonti PF1e

def _db(base: Path, libro: str) -> sqlite3.Connection:
    return sqlite3.connect(base / PRD / f"book-{libro}.db")


def prd_pf1e(base: Path) -> dict:
    classi, prestigio = {}, {}
    for libro in ("cr", "apg", "acg", "uc", "um", "npc"):
        p = base / PRD / f"book-{libro}.db"
        if not p.exists():
            continue
        c = _db(base, libro)
        for sid, nome, sub, lft, rgt in c.execute(
                "select section_id, name, subtype, lft, rgt from sections where type='class'"):
            if sub not in ("core", "base", "hybrid", "npc", "prestige") or not nome:
                continue
            dv = c.execute("select hit_die from class_details where section_id=?", (sid,)).fetchone()
            corpo = c.execute("select body from sections where lft between ? and ? and type='table' "
                              "and (name like 'Table: %' or name = ? or name = '') and body like '%Base Attack%'",
                              (lft, rgt, nome)).fetchone()
            if not corpo:  # Swashbuckler: l'intestazione PRD non dice «Base Attack»
                corpo = c.execute("select body from sections where lft between ? and ? and type='table' "
                                  "and name = ?", (lft, rgt, nome)).fetchone()
            if not dv or not dv[0]:
                # antipaladino: class_details.hit_die è vuoto, il PRD lo scrive
                # nella sezione figlia «Hit Die» (book-apg 2731, «d10.»)
                hd = c.execute("select body from sections where lft between ? and ? and name='Hit Die'",
                               (lft, rgt)).fetchone()
                m_hd = re.search(r"d(\d+)", re.sub("<[^>]+>", "", hd[0])) if hd and hd[0] else None
                dv = (f"d{m_hd.group(1)}",) if m_hd else dv
            pa = c.execute("select body from sections where lft between ? and ? and name in "
                           "('Skill Ranks per Level', 'Skill Ranks at Each Level')",
                           (lft, rgt)).fetchone()
            if not dv or not dv[0] or not corpo:
                continue
            riga = classe_da_tabella(next(iter(tabelle(corpo[0]).values())))
            if not riga:
                continue
            sk = c.execute("select body from sections where lft between ? and ? and type='table' "
                           "and name like '%Spells Known%'", (lft, rgt)).fetchone()
            if sk:
                riga["conosciuti"] = classe_conosciuti(next(iter(tabelle(sk[0]).values())))
            riga.update(dv=int(dv[0].strip().lstrip("d")), gradi=num(re.sub("<[^>]+>", "", pa[0])) if pa else None,
                        gruppo={"core": "base", "base": "base", "hybrid": "base", "npc": "png"}.get(sub, "prestigio"),
                        libro=libro)
            (prestigio if sub == "prestige" else classi).setdefault(nome.lower(), riga)
    c = _db(base, "cr")
    arm, scu, gruppo = {}, {}, None
    for r in next(iter(tabelle(c.execute("select body from sections where section_id=2955").fetchone()[0]).values())):
        if r[0] in ("Light armor", "Medium armor", "Heavy armor", "Shields", "Extras"):
            gruppo = r[0]
            continue
        if gruppo is None or len(r) < 4 or num(r[2]) is None:
            continue
        nome = re.sub(r"\d+$", "", r[0]).strip().lower()
        if gruppo == "Shields":
            scu[nome] = num(r[2])
        elif gruppo != "Extras":
            arm[nome] = {"ca": num(r[2]), "des_max": num(r[3])}
    abil = sorted({n for (n,) in c.execute("select name from sections where type='skill'") if n})
    con = {}
    for nome, sid in (("bard", 1773), ("sorcerer", 2444)):
        con[nome] = classe_conosciuti(next(iter(tabelle(c.execute(
            "select body from sections where section_id=?", (sid,)).fetchone()[0]).values())))
    for k, v in con.items():
        if k in classi:
            classi[k]["conosciuti"] = v
    return {"classi": classi, "prestigio": prestigio, "armature": arm, "scudi": scu, "abilita": abil}


# ------------------------------------------------------------ il plugin

def toml(rel: str) -> dict:
    return tomllib.loads((ROOT / rel).read_text(encoding="utf-8"))


def lessico(rel: str, col: str) -> dict:
    """{italiano minuscolo: inglese} delle righe di tipo abilità/classe di un lessico."""
    out = {}
    righe = [r.split("\t") for r in (ROOT / rel).read_text(encoding="utf-8").splitlines()
             if r and not r.startswith("#")]
    testa = righe[0]
    i_it, i_en, i_t = testa.index("italiano"), testa.index(col), testa.index("tipo")
    for r in righe[1:]:
        if len(r) > i_t:
            out.setdefault(r[i_t], {})[r[i_it].lower()] = r[i_en]
    return out


EN = {"barbaro": "barbarian", "bardo": "bard", "chierico": "cleric", "druido": "druid",
      "guerriero": "fighter", "monaco": "monk", "paladino": "paladin", "ladro": "rogue",
      "stregone": "sorcerer", "mago": "wizard", "guerriero-png": "warrior", "adepto": "adept",
      "esperto": "expert", "aristocratico": "aristocrat", "popolano": "commoner"}
GRIGLIA_CLASSE = {"mago": "wizard", "stregone": "sorcerer", "chierico": "cleric", "adepto": "adept",
                  "bardo": "bard", "ranger": "ranger"}


# ------------------------------------------------------------ confronti

def confronta(nome: str, fonte: dict, plugin: dict, campi: list, mancanti_campi=()) -> dict:
    righe = sorted(fonte)
    coperte = [k for k in righe if k in plugin]
    sbagliate = []
    for k in coperte:
        for c in campi:
            a, b = plugin[k].get(c), fonte[k].get(c)
            if c == "ts_buoni":
                a, b = sorted(a or []), sorted(b or [])
            if b is not None and a != b:
                sbagliate.append({"riga": k, "campo": c, "plugin": a, "fonte": b})
    giuste = len({k for k in coperte} - {s["riga"] for s in sbagliate})
    return {"tabella": nome, "fonte": len(righe), "coperte": len(coperte), "giuste": giuste,
            "mancanti": [k for k in righe if k not in plugin], "sbagliate": sbagliate,
            "campi_assenti": list(mancanti_campi)}


def uso_pf1e(p1: dict) -> dict:
    """Le classi del PRD che `genera_creatura --sistema pf1e` costruisce (5° livello;
    le prestigio sopra un mago, un chierico o un guerriero di 5°) e se il blocco
    passa i conti PF1e del cancello dei moduli."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import random
    try:
        import genera_creatura as G
        from dmcore import sistemi as S
        import conformita_statblocchi as CS
        S.dati("pf1e", "creature.costruzione")  # il plugin si carica: se manca, lo dice
    except Exception as e:  # noqa: BLE001 — la misura dice cosa manca, non cade
        return {"tabella": "uso: classi generate da genera_creatura", "fonte": 0, "coperte": 0,
                "giuste": 0, "mancanti": [], "sbagliate": [], "campi_assenti": [f"non si importa: {e}"]}
    if not hasattr(G, "genera_png_pf1e"):
        tutte = sorted(p1["classi"]) + sorted(p1["prestigio"])
        return {"tabella": "uso: classi generate da genera_creatura", "fonte": len(tutte), "coperte": 0,
                "giuste": 0, "mancanti": tutte, "sbagliate": [],
                "campi_assenti": ["genera_creatura --sistema pf1e rifiuta i livelli di classe"]}
    sb_err, coperte, mancanti = [], [], []
    for en in sorted(p1["classi"]) + sorted(p1["prestigio"]):
        if en in p1["prestigio"]:
            base = {"arcane": "wizard", "divine": "cleric"}.get(
                "arcane" if en in ("arcane archer", "arcane trickster", "dragon disciple", "eldritch knight",
                                   "loremaster", "master chymist") else
                "divine" if en in ("holy vindicator", "nature warden", "rage prophet", "mystic theurge") else "",
                "fighter")
            classi = [(base, 5), (en, 3)] if en != "mystic theurge" else [("cleric", 3), ("wizard", 3), (en, 3)]
        else:
            classi = [(en, 5)]
        try:
            sb, _ = G.genera_png_pf1e(5, classi=classi, rng=random.Random(1))
        except Exception as e:  # noqa: BLE001
            mancanti.append(en)
            sb_err.append({"riga": en, "campo": "genera", "plugin": None, "fonte": str(e)[:80]})
            continue
        coperte.append(en)
        scarti = CS.conti_del_recinto({"sb": sb, "prosa": "", "riga": 1}, sistema="pf1e")
        for s in scarti:
            sb_err.append({"riga": en, "campo": s["campo"], "plugin": s["scritto"], "fonte": s["atteso"]})
        if not sb.completo:
            sb_err.append({"riga": en, "campo": "completo", "plugin": sb.mancanti(), "fonte": []})
        for v in sb.voci:
            if v.startswith("Incantatore") and not any(x.startswith(("Preparati", "Conosciuti")) for x in sb.voci):
                sb_err.append({"riga": en, "campo": "incantesimi scelti", "plugin": "nessuno",
                               "fonte": "lista PF1e della classe"})
                break
    return {"tabella": "uso: classi generate da genera_creatura (5°, cancello PF1e, incantesimi scelti)",
            "fonte": len(coperte) + len(mancanti), "coperte": len(coperte),
            "giuste": len(coperte) - len({s["riga"] for s in sb_err if s["riga"] in coperte}),
            "mancanti": mancanti, "sbagliate": sb_err, "campi_assenti": []}


def uso_tipi_pf1e() -> dict:
    """Ogni tipo di creatura portato in PF1e da `genera_creatura --sistema pf1e`
    (GS 9, taglia media e, per i costrutti, tutte le taglie con pf bonus)
    passa i conti PF1e del cancello dei moduli?"""
    sys.path.insert(0, str(ROOT / "scripts"))
    import random
    import genera_creatura as G
    from dmcore import creature_pf1e as CP
    import conformita_statblocchi as CS
    casi = [(t, "medium") for t in G.T.TIPI if t not in ("humanoid",)]
    casi += [("construct", tg) for tg in ("tiny", "small", "large", "huge", "gargantuan", "colossal")]
    sb_err, righe = [], []
    for tipo, taglia in casi:
        riga = f"{tipo} {taglia}"
        righe.append(riga)
        try:
            sb, _ = G.genera(9, tipo=tipo, taglia=taglia, rng=random.Random(1))
            try:
                pf, _ = CP.converti(sb, tipo, taglia, pf_bersaglio=G.bersaglio_di(9, "bruto", False)[0]["pf"])
            except TypeError:   # converti di prima del lotto 5 delle regole complete
                pf, _ = CP.converti(sb, tipo, taglia)
        except Exception as e:  # noqa: BLE001
            sb_err.append({"riga": riga, "campo": "converti", "plugin": None, "fonte": str(e)[:80]})
            continue
        for s in CS.conti_del_recinto({"sb": pf, "prosa": "", "riga": 1}, sistema="pf1e"):
            sb_err.append({"riga": riga, "campo": s["campo"], "plugin": s["scritto"], "fonte": s["atteso"]})
    return {"tabella": "uso: tipi di creatura portati in PF1e (GS 9, cancello PF1e)", "fonte": len(righe),
            "coperte": len(righe), "giuste": len(righe) - len({s["riga"] for s in sb_err}),
            "mancanti": [], "sbagliate": sb_err, "campi_assenti": []}


def misura(base: Path) -> dict:
    s35, p1 = srd35(base), prd_pf1e(base)
    c35 = toml("sistemi/dnd35/dati/creature.toml")
    cp1 = toml("sistemi/pf1e/dati/creature.toml")
    out = {"dnd35": [], "pf1e": []}

    # --- tipi
    t35 = {k: v for k, v in c35["tipi"].items()}
    out["dnd35"].append(confronta("tipi (Creature Improvement by Type)", s35["tipi"], t35,
                                  ["dv", "bab", "ts_buoni"], ["gradi (punti abilità per DV)"]))
    # il tipo umanoide 3.5 ha «Varies (any one)»: un TS buono a scelta, non uno fisso
    for r in out["dnd35"][-1]["sbagliate"]:
        if r["riga"] in ("humanoid", "elemental"):
            r["nota"] = s35["tipi"][r["riga"]]["nota_ts"]

    # --- classi base e PNG
    cl35 = {}
    for k, v in c35["classi"].items():
        en = EN.get(k, k)
        if en in s35["classi"] and en not in cl35:
            cl35[en] = v | {"bab": v["bab"]}
    out["dnd35"].append(confronta("classi base e PNG", s35["classi"], cl35, ["dv", "bab", "ts_buoni"],
                                  ["gradi (punti abilità per livello)"]))
    out["dnd35"].append(confronta("classi di prestigio", s35["prestigio"], c35.get("prestigio", {}),
                                  ["dv", "bab", "ts_buoni"]))
    k1 = toml("sistemi/pf1e/dati/classi.toml") if (ROOT / "sistemi/pf1e/dati/classi.toml").exists() else {}
    kc = k1.get("classi", {})
    cl1 = {k: v for k, v in kc.items() if v["gruppo"] != "prestigio"}
    pr1 = {k: v for k, v in kc.items() if v["gruppo"] == "prestigio"}
    out["pf1e"].append(confronta("classi base, ibride e PNG", p1["classi"], cl1,
                                 ["dv", "bab", "ts_buoni", "gradi"],
                                 [] if cl1 else ["il plugin PF1e non ha la tabella"]))
    out["pf1e"].append(confronta("classi di prestigio", p1["prestigio"], pr1,
                                 ["dv", "bab", "ts_buoni", "gradi"]))

    # --- armature e scudi
    a35 = {k: v for k, v in c35["armature"].items()}
    out["dnd35"].append(confronta("armature", s35["armature"], a35, ["ca", "des_max"]))
    sc35 = {k: {"ca": v} for k, v in c35["scudi"].items()}
    sc_fonte = {}
    for k, v in s35["scudi"].items():
        chiave = {"buckler": "buckler", "shield, light wooden": "light shield", "shield, light steel": "light shield",
                  "shield, heavy wooden": "heavy shield", "shield, heavy steel": "heavy shield",
                  "shield, tower": "tower shield"}.get(k, k)
        sc_fonte[chiave] = {"ca": v}
    out["dnd35"].append(confronta("scudi", sc_fonte, sc35, ["ca"]))
    a1 = cp1.get("armature", {})
    out["pf1e"].append(confronta("armature", p1["armature"], a1, ["ca", "des_max"],
                                 [] if a1 else ["il plugin PF1e non ha la tabella"]))
    out["pf1e"].append(confronta("scudi", {k: {"ca": v} for k, v in p1["scudi"].items()},
                                 cp1.get("scudi", {}), ["ca"]))

    # --- griglie degli incantesimi (3.5)
    g35 = {}
    for nome, en in GRIGLIA_CLASSE.items():
        g = c35["griglie"].get(nome)
        if g:
            g35[en] = {"griglia": {int(k): v for k, v in g.items()}}
    # divergenza voluta (card del DM del 2026-11-09, «Tabelle PF1e intere,
    # segnate»): le classi in incantatori_regole.griglia_pf1e si misurano
    # contro il PRD PF1e, non contro l'SRD, e il rapporto lo dice
    pf1e_voluta = {EN.get(k, k) for k in c35["incantatori_regole"].get("griglia_pf1e", ())}
    gf = {}
    for en in ("wizard", "sorcerer", "cleric", "druid", "bard", "ranger", "paladin", "adept"):
        src = (p1 if en in pf1e_voluta else s35)["classi"].get(en, {}).get("griglia")
        if src:
            gf[en] = {"griglia": {n: griglia_lista(x) for n, x in src.items()}}
    plugin_g = {}
    for en, v in gf.items():
        nome = next((k for k, x in c35["incantatori"].items() if EN.get(k, k) == en or k == en), None)
        if nome is None:
            continue
        g = c35["griglie"].get(c35["incantatori"][nome]["griglia"])
        plugin_g[en] = {"griglia": {int(k): list(x) for k, x in g.items()}}
    ris = confronta("incantesimi al giorno (griglie)", gf, plugin_g, [])
    sb = []
    for en in sorted(set(gf) & set(plugin_g)):
        for n in sorted(gf[en]["griglia"]):
            a, b = plugin_g[en]["griglia"].get(n), gf[en]["griglia"][n]
            # il plugin scrive lo «0 finto» per ranger e paladino; si confronta dal 1° livello
            if en in ("ranger", "paladin"):
                a, b = (a or [])[1:], b[1:]
            if a != b:
                sb.append({"riga": f"{en} {n}°", "campo": "slot", "plugin": a, "fonte": b})
    ris["sbagliate"] = sb
    ris["giuste"] = sum(1 for en in set(gf) & set(plugin_g)) - len({s["riga"].split()[0] for s in sb})
    if pf1e_voluta:
        ris["tabella"] += f" — {', '.join(sorted(pf1e_voluta))} contro il PRD PF1e (scelta del DM)"
    out["dnd35"].append(ris)
    for chiave, campo, nome in (("griglie", "griglia", "incantesimi al giorno (griglie)"),
                                ("conosciuti", "conosciuti", "incantesimi conosciuti")):
        fonte = {k: v[campo] for k, v in (p1["classi"] | p1["prestigio"]).items() if v.get(campo)}
        plug = {k: {int(n): list(x) for n, x in g.items()} for k, g in k1.get(chiave, {}).items()}
        sb = []
        for k in sorted(set(fonte) & set(plug)):
            for n in sorted(fonte[k]):
                a, b = plug[k].get(n), griglia_lista(fonte[k][n])
                if not b and not a:  # livello senza incantesimi (bloodrager 1°-3°)
                    continue
                # lo 0 d'allineamento (classi senza livello 0) non è nella fonte
                if a and b and len(a) == len(b) + 1 and a[0] == 0:
                    b = [0] + b
                if a != b and not (a and b and a[1:] == b[1:] and b[0] == 0):
                    sb.append({"riga": f"{k} {n}°", "campo": campo, "plugin": a, "fonte": b})
        cop = sorted(set(fonte) & set(plug))
        out["pf1e"].append({"tabella": nome, "fonte": len(fonte), "coperte": len(cop),
                            "giuste": len(cop) - len({s["riga"].rsplit(" ", 1)[0] for s in sb}),
                            "mancanti": sorted(set(fonte) - set(plug)), "sbagliate": sb,
                            "campi_assenti": [] if plug else ["il plugin PF1e non ha la tabella"]})

    # --- conosciuti
    for en, chiave in (("sorcerer", "stregone_conosciuti"), ("bard", "bardo_conosciuti")):
        voluta = en in pf1e_voluta
        src = (p1 if voluta else s35)["classi"][en].get("conosciuti", {})
        g = {int(k): v for k, v in c35["griglie"][chiave].items()}
        sb = [{"riga": f"{en} {n}°", "campo": "conosciuti", "plugin": g.get(n), "fonte": griglia_lista(src[n])}
              for n in sorted(src) if g.get(n) != griglia_lista(src[n])]
        out["dnd35"].append({"tabella": f"incantesimi conosciuti ({en})"
                             + (" contro il PRD PF1e (scelta del DM)" if voluta else ""), "fonte": len(src),
                             "coperte": len(set(src) & set(g)), "giuste": len(src) - len(sb),
                             "mancanti": [], "sbagliate": sb, "campi_assenti": []})

    # --- uso: ogni classe PF1e del PRD si genera e passa il cancello PF1e?
    out["pf1e"].append(uso_pf1e(p1))
    out["pf1e"].append(uso_tipi_pf1e())

    # --- abilità
    lx35 = lessico("scripts/lessico_it_35.tsv", "srd35").get("abilità", {})
    nomi = toml("sistemi/dnd35/dati/abilita.toml")["nomi"]
    en = {}
    ignoti = []
    for n in nomi:
        e = lx35.get(n.lower())
        if e:
            en[e] = {"nome": n}
        else:
            ignoti.append(n)
    r = confronta("abilità (nomi)", {a: {} for a in s35["abilita"]}, en, [])
    r["sbagliate"] = [{"riga": n, "campo": "nome", "plugin": n, "fonte": "non è un'abilità SRD 3.5 nel lessico"}
                      for n in ignoti]
    r["giuste"] = r["coperte"]
    out["dnd35"].append(r)
    lx1 = lessico("scripts/lessico_it_pf1.tsv", "pf1").get("abilità", {})
    en1 = {v: {} for v in lx1.values()}
    out["pf1e"].append(confronta("abilità (nomi, dal lessico PF1e)", {a: {} for a in p1["abilita"]}, en1, []))

    # --- liste d'incantesimi per classe × funzione, contro le liste SRD 3.5
    lxi = {k: _norm(v) for k, v in lessico("scripts/lessico_it_35.tsv", "srd35").get("incantesimo", {}).items()}
    inc = toml("sistemi/dnd35/dati/incantesimi.toml")
    classe_srd = {"mago": "sorcerer/wizard", "chierico": "cleric", "druido": "druid", "bardo": "bard",
                  "ranger": "ranger", "paladino": "paladin"}
    voci, sb, ignote, dominio = 0, [], [], 0
    for cl, funzioni in inc["liste"].items():
        srd = s35["liste"].get(classe_srd.get(cl, ""), {})
        for fn, livelli in funzioni.items():
            for lv, nomi in livelli.items():
                for n in nomi:
                    voci += 1
                    en = lxi.get(n.lower())
                    if en is None:
                        ignote.append(f"{cl}.{fn}.{lv}: {n}")
                        continue
                    if en not in srd.get(int(lv), set()):
                        if cl == "chierico" and en in s35["liste"].get("dominio", {}).get(int(lv), set()):
                            dominio += 1
                            continue
                        dove = sorted(l for l, xs in srd.items() if en in xs)
                        sb.append({"riga": f"{cl}.{fn} {lv}°", "campo": n, "plugin": f"{en} al {lv}°",
                                   "fonte": f"al {dove[0]}°" if dove else "non nella lista SRD della classe"})
    out["dnd35"].append({"tabella": "liste d'incantesimi (classe × funzione)", "fonte": voci, "coperte": voci,
                         "giuste": voci - len(sb) - len(ignote), "mancanti": [],
                         "sbagliate": sb, "non_verificabili": ignote,
                         "campi_assenti": [], "nota": f"{dominio} voci del chierico sono incantesimi di dominio, contati giusti"})

    # --- PE 3.5: la formula del PHB (non nell'SRD) n(n−1)/2 × 1000
    pe = toml("sistemi/dnd35/dati/pe.toml")["soglie"]["unica"]
    sb = [{"riga": k, "campo": "pe", "plugin": v, "fonte": int(k) * (int(k) - 1) // 2 * 1000}
          for k, v in pe.items() if v != int(k) * (int(k) - 1) // 2 * 1000]
    out["dnd35"].append({"tabella": "soglie PE (PHB Tab. 3-2)", "fonte": 20, "coperte": len(pe),
                         "giuste": len(pe) - len(sb), "mancanti": [], "sbagliate": sb, "campi_assenti": []})

    # --- tipi e taglie PF1e (generati)
    tp1 = {k: v for k, v in cp1["tipi"].items()}
    out["pf1e"].append({"tabella": "tipi e taglie", "fonte": len(tp1), "coperte": len(tp1), "giuste": len(tp1),
                        "mancanti": [], "sbagliate": [], "campi_assenti": [],
                        "nota": "generati da estrai_prd_pf1e.py --check (cancello in CI)"})
    return {"fonti": {"srd35": SRD, "prd": PRD}, "sistemi": out,
            "fonte_classi": {"dnd35": {k: {x: v.get(x) for x in ("dv", "bab", "ts_buoni", "gradi", "gruppo")}
                                       for k, v in (s35["classi"] | s35["prestigio"]).items()},
                             "pf1e": {k: {x: v.get(x) for x in ("dv", "bab", "ts_buoni", "gradi", "gruppo", "libro")}
                                      for k, v in (p1["classi"] | p1["prestigio"]).items()}},
            "fonte_armature": {"dnd35": s35["armature"], "pf1e": p1["armature"]},
            "fonte_griglie_pf1e": {k: {n: griglia_lista(x) for n, x in v["griglia"].items()}
                                   for k, v in p1["classi"].items() if v.get("griglia")}}


def riepilogo(m: dict) -> "list[str]":
    righe = []
    for sis, tab in m["sistemi"].items():
        tf = sum(t["fonte"] for t in tab)
        tc = sum(t["coperte"] for t in tab)
        tg = sum(t["giuste"] for t in tab)
        tv = tc - sum(len(t.get("non_verificabili", [])) for t in tab)
        righe.append(f"## {sis}: {tc}/{tf} righe coperte ({100 * tc / max(tf, 1):.0f}%), "
                     f"{tg}/{tv} giuste tra le verificabili ({100 * tg / max(tv, 1):.0f}%)")
        righe.append("")
        righe.append("| Tabella | Fonte | Coperte | Giuste | Sbagliate | Non verificabili | Campi assenti |")
        righe.append("|---|---:|---:|---:|---:|---:|---|")
        for t in tab:
            righe.append(f"| {t['tabella']} | {t['fonte']} | {t['coperte']} | {t['giuste']} | "
                         f"{len(t['sbagliate'])} | {len(t.get('non_verificabili', []))} | "
                         f"{'; '.join(t['campi_assenti']) or '—'} |")
        righe.append("")
        for t in tab:
            if t["sbagliate"]:
                righe.append(f"**{t['tabella']}**, voci che non tornano:")
                for s in t["sbagliate"]:
                    righe.append(f"- {s['riga']} · {s['campo']}: plugin {s['plugin']} ≠ fonte {s['fonte']}"
                                 + (f" ({s['nota']})" if s.get("nota") else ""))
                righe.append("")
            if t.get("non_verificabili"):
                righe.append(f"**{t['tabella']}**, non verificabili (nome italiano assente dal lessico): "
                             + ", ".join(t["non_verificabili"]))
                righe.append("")
            if t["mancanti"] and t["coperte"]:
                righe.append(f"**{t['tabella']}**, mancano: {', '.join(t['mancanti'])}")
                righe.append("")
    return righe


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json")
    ap.add_argument("--md")
    a = ap.parse_args(argv)
    m = misura(cache())
    testo = "\n".join(riepilogo(m))
    print(testo)
    if a.json:
        Path(a.json).write_text(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if a.md:
        Path(a.md).write_text(testo + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
