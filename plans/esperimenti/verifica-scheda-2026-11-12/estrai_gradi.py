#!/usr/bin/env python3
"""estrai_gradi.py — le regole dei gradi delle abilità 3.5, dall'SRD in cache.

Scrive `sistemi/dnd35/dati/gradi.toml` e `sistemi/pf1e/dati/gradi.toml`:
  [chiave]   abilità → caratteristica chiave («Climb (Str)» → For)
  [classi]   classe → punti abilità per livello («4 + Int modifier» → 4)
  [tipi]     tipo di creatura → punti per dado vita razziale
  [di_classe] classe → abilità di classe («Class Skills»); [fuori_classe] costo e massimo
  [penalita_di_prova] le abilità che la subiscono e la penalità di ogni armatura e scudo
  [regole]   massimo dei gradi, moltiplicatore del primo dado vita, minimo per dado

Fonte: olimot/srd-v3.5-md@c7f30a0c (la stessa di talenti.toml), OGL.

Uso
  python3 scripts/riscontro_srd.py scarica                  # riempie la cache
  python3 plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py [--check]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"
OUT = ROOT / "sistemi" / "dnd35" / "dati" / "gradi.toml"
CAR = {"str": "For", "dex": "Des", "con": "Cos", "int": "Int", "wis": "Sag", "cha": "Car", "none": ""}
FILE_CLASSI = ["basic-rules-and-legal/character-classes-i.md", "basic-rules-and-legal/character-classes-ii.md",
               "basic-rules-and-legal/npc-classes.md", "basic-rules-and-legal/prestige-classes.md",
               "psionics/psionic-classes.md", "epic/epic-prestige-classes.md"]


def _q(s: str) -> str:
    return '"' + s.replace('"', '\\"') + '"'


def chiavi(base: Path) -> "dict[str, str]":
    out = {}
    for f in ("skills-i.md", "skills-ii.md"):
        t = (base / "basic-rules-and-legal" / f).read_text(encoding="utf-8")
        for nome, car in re.findall(r"^#{2,3} ([A-Z][\w' ]+?) (?:<small>)?\((\w+)", t, flags=re.M):
            if car.lower() in CAR:
                out[nome.strip().lower()] = CAR[car.lower()]
    for f in sorted((base / "psionics").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        for nome, car in re.findall(r"^#{2,3} ([A-Z][\w' ]+?) <small>\((Str|Dex|Con|Int|Wis|Cha)\b", t, flags=re.M):
            out.setdefault(nome.strip().lower(), CAR[car.lower()])
    return dict(sorted(out.items()))


def classi(base: Path) -> "dict[str, int]":
    out = {}
    for rel in FILE_CLASSI:
        f = base / rel
        if not f.is_file():
            continue
        t = f.read_text(encoding="utf-8")
        for blocco in re.split(r"^## ", t, flags=re.M)[1:]:
            nome = blocco.split("\n", 1)[0].strip()
            m = re.search(r"\*\*Skill Points at Each (?:Additional )?Level:?\*\*:?\s*(\d+) \+ Int", blocco)
            if m:
                out[re.sub(r"\s*<small>.*", "", nome).lower()] = int(m.group(1))
    return dict(sorted(out.items()))


def di_classe(base: Path, chiave: "dict[str, str]") -> "dict[str, list[str]]":
    """Classe → le sue abilità di classe, dal paragrafo «Class Skills» («The
    barbarian's class skills (and the key ability for each skill) are Climb
    (Str), …»). I nomi sono quelli di `[chiave]`: «Knowledge (arcana)» resta
    con la sua parentesi, «Knowledge (all skills, taken individually)» diventa
    «knowledge», e chi legge prende per buona ogni voce che comincia così.
    Una classe il cui paragrafo non si legge (o dà nomi fuori da `[chiave]`)
    non esce: chi verifica la tratta come classe senza elenco."""
    out = {}
    for rel in FILE_CLASSI:
        f = base / rel
        if not f.is_file():
            continue
        for blocco in re.split(r"^## ", f.read_text(encoding="utf-8"), flags=re.M)[1:]:
            nome = re.sub(r"\s*<small>.*", "", blocco.split("\n", 1)[0].strip()).lower()
            m = re.search(r"class skills \(and the key ability for each skill\) are ([^\n]+)", blocco)
            if not m:
                continue
            testo = re.sub(r"\s*See Chapter 4.*$", "", m.group(1))
            testo = re.sub(r"\((?:Str|Dex|Con|Int|Wis|Cha|None)\)", "", testo)
            testo = re.sub(r"\(all skills,? taken individually\)|\(any\)", "", testo)
            voci, ignote = [], []
            # «Hide (Dex). Listen (Wis)» nell'arciere arcano: il punto in mezzo è un refuso della fonte
            for v in re.split(r"[,.]\s*(?:and\s+)?|\s+and\s+(?![^()]*\))", testo):
                v = re.sub(r"\s+", " ", v.replace("(n/a)", "")).strip(" .").lower()
                if not v:
                    continue
                radice = v.split(" (")[0]
                (voci if radice in chiave else ignote).append(v)
            if voci and not ignote:
                out[nome] = sorted(set(voci))
    return dict(sorted(out.items()))


def di_dominio(base: Path, chiave: "dict[str, str]") -> "dict[str, list[str]]":
    """Dominio → le abilità che aggiunge a quelle di classe del chierico («Add
    Bluff, Disguise, and Hide to your list of cleric class skills»)."""
    t = (base / "spells" / "spell-list-i.md").read_text(encoding="utf-8")
    out = {}
    for blocco in re.split(r"^### ", t, flags=re.M)[1:]:
        nome = blocco.split("\n", 1)[0].strip()
        m = re.search(r"Add (.+?) to your list of cleric class skills", blocco)
        if not nome.endswith(" Domain") or not m:
            continue
        testo = re.sub(r"\ball Knowledge skills\b", "Knowledge", m.group(1))
        voci = [re.sub(r"\s+", " ", v).strip().lower() for v in re.split(r",\s*(?:and\s+)?|\s+and\s+", testo)]
        voci = [v for v in voci if v.split(" (")[0] in chiave]
        if voci:
            out[nome[:-len(" Domain")].lower()] = sorted(voci)
    return dict(sorted(out.items()))


NOMI_RAZZE = {"dwarf": ["dwarf", "nan[oaie]"], "elf": ["elf", "elf[oaie]"], "gnome": ["gnome", "gnom[oaie]"],
              "half-elf": ["half-elf", "mezzelf[oaie]"], "half-orc": ["half-orc", "mezzorc[ohie]+"],
              "halfling": ["halfling"], "human": ["human", "uman[oaie]"]}
#: chi ha un nome di queste non è una delle sette razze, anche se il tipo dice «(elfo)» o «(nano)»
ALTRE_RAZZE = ["drow", "duergar", "svirfneblin", "derro", "aasimar", "tiefling", "githyanki", "githzerai",
               "orog", "tanarukk", "fey'ri", "goblin", "hobgoblin", "bugbear", "kobold", "cobold[oi]",
               "(?<!half-)orc", "orc[ohie]+", "grigi[oa]", "scur[oa]", "profond[oa]", "selvaggi[oa]", "acquatic[oa]"]


def _abilita_in(testo: str, chiave: "dict[str, str]") -> "list[str]":
    """Le abilità di `[chiave]` nominate nel testo, le più lunghe per prime."""
    t = testo.lower()
    return [a for a in sorted(chiave, key=len, reverse=True) if re.search(rf"\b{re.escape(a)}\b", t)]


def salto(base: Path) -> "dict[str, int]":
    """Il modificatore della velocità a Saltare («If your speed is less than 30
    feet, you take a –6 penalty for every 10 feet of speed less than 30 feet…
    you gain a +4 bonus for every 10 feet beyond 30 feet»)."""
    t = (base / "basic-rules-and-legal" / "skills-ii.md").read_text(encoding="utf-8")
    m = re.search(r"If your speed is less than (\d+) feet, you take a [–-](\d+) penalty for every (\d+) feet of speed "
                  r"less than \d+ feet\. If your speed is greater than \d+ feet, you gain a \+(\d+) bonus for every "
                  r"\d+ feet beyond", t)
    return {"velocita": int(m.group(1)), "ogni": int(m.group(3)), "meno": int(m.group(2)), "piu": int(m.group(4))}


def sinergie(base: Path, chiave: "dict[str, str]") -> "dict[str, list[str]]":
    """Abilità → le abilità che con 5 gradi le danno +2 («If you have 5 or more
    ranks in Bluff, Knowledge (nobility and royalty), or Sense Motive, you get
    a +2 bonus on Diplomacy checks»). Le condizioni («…checks related to
    scrolls») non si tengono: il +2 è un tetto, vale quando può valere. Le
    Conoscenze sono una voce sola, come in `[chiave]`."""
    out: "dict[str, set[str]]" = {}
    for f in ("skills-i.md", "skills-ii.md"):
        t = (base / "basic-rules-and-legal" / f).read_text(encoding="utf-8")
        for da, a in re.findall(r"If you have 5 (?:or more )?ranks in (.+?), you (?:get|gain) a \+2 bonus (?:on|to) "
                                r"(.+?) checks", t):
            for bersaglio in _abilita_in(a, chiave):
                out.setdefault(bersaglio, set()).update(x for x in _abilita_in(da, chiave) if x != bersaglio)
    return {a: sorted(v) for a, v in sorted(out.items()) if v}


def penalita_di_prova(base: Path, chiave: "dict[str, str]") -> "tuple[list[str], list[str], dict, dict]":
    """(abilità con la penalità, abilità con la penalità doppia, armature, scudi).

    Le abilità sono quelle col titolo «(Dex; Armor Check Penalty)»; la doppia è
    quella di «subject to double the normal armor check penalty» (Nuotare).
    Armature e scudi vengono dalla tabella «Armor and Shields»: nome → bonus,
    Des massima e penalità (positiva). Chi legge una scheda riconosce l'oggetto
    dal bonus e dalla Des massima, che nella tabella non si ripetono."""
    con, doppia = [], []
    for f in ("skills-i.md", "skills-ii.md"):
        t = (base / "basic-rules-and-legal" / f).read_text(encoding="utf-8")
        for blocco in re.split(r"^#{2,3} ", t, flags=re.M)[1:]:
            titolo = blocco.split("\n", 1)[0]
            nome = re.sub(r"<.*", "", titolo).strip().lower()
            if nome in chiave and "Armor Check Penalty" in titolo:
                con.append(nome)
                if re.search(r"double the normal armor check penalty", blocco):
                    doppia.append(nome)
    t = (base / "basic-rules-and-legal" / "equipment.md").read_text(encoding="utf-8")
    tabella = re.search(r"<table[^>]*><caption>Table: Armor and Shields</caption>.*?</table>", t, re.S).group(0)
    armature, scudi, dove = {}, {}, None
    for riga in re.findall(r"<tr>(.*?)</tr>", tabella, re.S):
        celle = [re.sub(r"<[^>]+>", "", re.sub(r"<sup>.*?</sup>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", riga, re.S)]
        if not celle:
            continue
        if celle[0] in ("Light armor", "Medium armor", "Heavy armor"):
            dove = armature
        elif celle[0] == "Shields":
            dove = scudi
        elif celle[0] == "Extras":
            dove = None
        elif dove is not None and len(celle) > 4 and re.fullmatch(r"\+\d+", celle[2]):
            ca = int(re.match(r"\+(\d+)", celle[2]).group(1))
            pen = abs(int(celle[4].replace("–", "-").replace("−", "-")))
            voce = {"ca": ca, "penalita": pen}
            if dove is armature:
                voce["des_max"] = int(celle[3].replace("+", ""))
            dove[celle[0].lower()] = voce
    return sorted(con), sorted(doppia), armature, scudi


#: le razze senza dadi vita razziali (chiavi di mdl.toml): file dei mostri, titolo del loro
#: capitolo «… as Characters» e la razza di cui sono sottorazza (ne tengono i bonus come tetto)
RAZZE_DEI_MOSTRI = {"aasimar": ("monsters-o-r.md", "Aasimar as Characters", None),
                    "drow": ("monsters-e-f.md", "Drow", "elf"),
                    "duergar": ("monsters-dr-dw.md", "Duergar", "dwarf"),
                    "goblin": ("monsters-g.md", "Goblins as Characters", None),
                    "hobgoblin": ("monsters-h-i.md", "Hobgoblin Characters", None),
                    "kobold": ("monsters-k-l.md", "Kobold Characters", None),
                    "orc": ("monsters-o-r.md", "Orcs as Characters", None),
                    "svirfneblin": ("monsters-g.md", "Svirfneblin", "gnome"),
                    "tiefling": ("monsters-o-r.md", "Tieflings as Characters", None)}


def _bonus_del_blocco(blocco: str, chiave: "dict[str, str]") -> "tuple[dict[str, int], dict[str, int]]":
    """(bonus razziali, bonus di taglia) alle abilità scritti in un blocco di
    tratti. «+4 bonus on Hide checks» nella riga della taglia Piccola è di
    taglia; «which improves to +4 underground» alza il razziale: è un tetto."""
    razziali: "dict[str, int]" = {}
    taglia: "dict[str, int]" = {}
    for n, tipo, resto, coda in re.findall(
            r"\+(\d) (racial |size )?bonus on ([^.+]+?) checks(, which improves to \+\d)?", blocco):
        if not tipo and "hide" not in resto.lower():
            continue  # «+4 bonus on ability checks» dei nani: non è un'abilità
        n = max(int(n), int(coda[-1]) if coda else 0)
        dove = razziali if tipo == "racial " else taglia
        for a in _abilita_in(resto, chiave):
            dove[a] = max(dove.get(a, 0), n)
    return razziali, taglia


def razze(base: Path, chiave: "dict[str, str]") -> "dict[str, dict[str, int]]":
    """Razza dell'SRD → il bonus più alto che razza e taglia danno a ogni
    abilità («+2 racial bonus on Listen, Search, and Spot checks», «+4 size
    bonus on Hide checks»), anche quando vale solo in certi casi (la pietra dei
    nani): è un tetto. Razziale e taglia si sommano, perché sono tipi diversi.
    Una razza senza bonus esce con la tabella vuota, perché «nessun bonus» è un
    fatto anche quello. Dopo le sette razze, le nove senza dadi vita razziali
    del capitolo dei mostri; una sottorazza tiene per tetto anche i bonus della
    razza da cui viene."""
    t = (base / "basic-rules-and-legal" / "races.md").read_text(encoding="utf-8")
    nomi = {"Humans": "human", "Dwarves": "dwarf", "Elves": "elf", "Gnomes": "gnome", "Half-Elves": "half-elf",
            "Half-Orcs": "half-orc", "Halflings": "halfling"}
    grezzi: "dict[str, tuple[dict[str, int], dict[str, int]]]" = {}
    for blocco in re.split(r"^## ", t, flags=re.M)[1:]:
        nome = nomi.get(blocco.split("\n", 1)[0].strip())
        if nome:
            grezzi[nome] = _bonus_del_blocco(blocco, chiave)
    for nome, (file, titolo, madre) in RAZZE_DEI_MOSTRI.items():
        righe, dentro, blocco = (base / "monsters" / file).read_text(encoding="utf-8").split("\n"), False, []
        for riga in righe:
            m = re.match(r"#+ (.+)$", riga)
            if m:
                dentro = m.group(1).strip() == titolo
            elif dentro:
                blocco.append(riga)
        assert blocco, nome
        raz, tag = _bonus_del_blocco("\n".join(blocco), chiave)
        if madre:
            for a, n in grezzi[madre][0].items():
                raz[a] = max(raz.get(a, 0), n)
            for a, n in grezzi[madre][1].items():
                tag[a] = max(tag.get(a, 0), n)
        grezzi[nome] = (raz, tag)
    out = {nome: dict(sorted({a: raz.get(a, 0) + tag.get(a, 0) for a in set(raz) | set(tag)}.items()))
           for nome, (raz, tag) in grezzi.items()}
    return dict(sorted(out.items()))


def tipi(base: Path) -> "dict[str, int]":
    t = (base / "basic-rules-and-legal" / "types-subtypes-and-special-abilities.md").read_text(encoding="utf-8")
    out = {}
    pezzi = re.split(r"^#{2,4} ([A-Z][\w ]+?) Type\s*$|\*\*([A-Z][\w ]+?) Type:\*\*", t, flags=re.M)
    for i in range(1, len(pezzi) - 2, 3):
        nome = (pezzi[i] or pezzi[i + 1] or "").strip().lower()
        m = re.search(r"Skill points equal to \((\d+) \+ Int modifier", pezzi[i + 2])
        if nome and m:
            out[nome] = int(m.group(1))
    return dict(sorted(out.items()))


PRD = Path.home() / ".cache" / "rumblingstone" / "srd" / "PSRD-Data-76ea47846041"
OUT_PF = ROOT / "sistemi" / "pf1e" / "dati" / "gradi.toml"


def genera_pf1e() -> str:
    """PF1e dal PRD (devonjones/PSRD-Data@76ea4784): `skill_attributes` del Core
    e «Skill points equal to» di ogni tipo nel Bestiary. I punti per livello
    delle classi stanno già in `classi.toml` (`gradi`)."""
    import sqlite3
    core = sqlite3.connect(PRD / "book-cr.db")
    k = {n.lower(): CAR[a.lower()] for n, a in core.execute(
        "select s.name, d.attribute from sections s join skill_attributes d on d.section_id = s.section_id")}
    b1 = sqlite3.connect(PRD / "book-b1.db")
    t = {}
    for nome, corpo in b1.execute("select name, body from sections where body like '%Skill points equal to%'"):
        m = re.search(r"Skill points equal to (\d+) \+ Int modifier", re.sub(r"<[^>]+>", " ", corpo or ""))
        if m and nome:
            t.setdefault(nome.lower(), int(m.group(1)))
    righe = [
        "# sistemi/pf1e/dati/gradi.toml — i gradi delle abilità PF1e (ADR-0124)",
        "# Generato da plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py dal PRD",
        "# (devonjones/PSRD-Data@76ea4784): abilità e caratteristica chiave dal Core,",
        "# «Skill points equal to» di ogni tipo dal Bestiary. I punti per livello delle",
        "# classi sono in classi.toml (`gradi`).",
        "",
        "[regole]",
        "# gradi massimi = dadi vita; un'abilità di classe con almeno 1 grado dà +3;",
        "# nessun moltiplicatore al primo dado; almeno 1 grado per dado; umani +1 per livello",
        "massimo_piu = 0",
        "primo_dado = 1",
        "minimo_per_dado = 1",
        "umano_per_livello = 1",
        "bonus_di_classe = 3",
        "",
        "[chiave]",
        *[f"{_q(a)} = {_q(v)}" for a, v in sorted(k.items())],
        "",
        "[tipi]",
        *[f"{_q(a)} = {v}" for a, v in sorted(t.items())],
        "",
    ]
    return "\n".join(righe)


def genera() -> str:
    k, c, t = chiavi(CACHE), classi(CACHE), tipi(CACHE)
    righe = [
        "# sistemi/dnd35/dati/gradi.toml — i gradi delle abilità 3.5 (ADR-0124)",
        "# Generato da plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py dall'SRD 3.5",
        "# (olimot/srd-v3.5-md@c7f30a0c): «Skills Summary», la riga «Skill Points at Each",
        "# Additional Level» di ogni classe, «Skill points equal to» di ogni tipo.",
        "",
        "[regole]",
        "# gradi massimi in un'abilità di classe = dadi vita + 3; il primo dado vita vale 4 volte;",
        "# almeno 1 punto per dado vita; gli umani hanno 1 punto in più per livello",
        "massimo_piu = 3",
        "primo_dado = 4",
        "minimo_per_dado = 1",
        "umano_per_livello = 1",
        "",
        "[chiave]",
        *[f"{_q(a)} = {_q(v)}" for a, v in k.items()],
        "",
        "[classi]",
        *[f"{_q(a)} = {v}" for a, v in c.items()],
        "",
        "[tipi]",
        *[f"{_q(a)} = {v}" for a, v in t.items()],
        "",
        "# le abilità di classe, dal paragrafo «Class Skills» (lotto 6 di ADR-0126). «knowledge»",
        "# senza parentesi vuol dire tutte le Conoscenze. Una classe che qui manca non ha un",
        "# elenco leggibile nella fonte (l'esperto ne sceglie dieci): per lei nessuna abilità si",
        "# giudica fuori classe.",
        "[di_classe]",
        *[f"{_q(a)} = [{', '.join(_q(x) for x in v)}]" for a, v in di_classe(CACHE, k).items()],
        "",
        "# le abilità che un dominio aggiunge a quelle di classe del chierico (SRD, «Cleric Domains»)",
        "[di_dominio]",
        *[f"{_q(a)} = [{', '.join(_q(x) for x in v)}]" for a, v in di_dominio(CACHE, k).items()],
        "",
        "# chi con 5 gradi dà +2 a un'abilità (SRD, «Synergy» di ogni abilità): abilità → fonti",
        "[sinergie]",
        *[f"{_q(a)} = [{', '.join(_q(x) for x in v)}]" for a, v in sinergie(CACHE, k).items()],
        "",
        "# il bonus di razza e di taglia alle abilità (anche se vale solo in certi casi): le sette razze",
        "# dell'SRD e le nove senza dadi vita razziali del capitolo dei mostri (le chiavi di mdl.toml)",
        *[riga for r, v in razze(CACHE, k).items()
          for riga in (f"[razze.{_q(r)}]", *[f"{_q(a)} = {n}" for a, n in v.items()], "")],
        "# come una scheda nomina le sette razze (espressioni regolari, italiano e inglese); una",
        "# sottorazza (drow, duergar…) ha i suoi bonus in un'altra pagina e non è qui",
        "[razze_nomi]",
        *[f"{_q(r)} = [{', '.join(_q(x) for x in v)}]" for r, v in NOMI_RAZZE.items()],
        "altre = [" + ", ".join(_q(x) for x in ALTRE_RAZZE) + "]",
        "",
        "[margine]",
        "# quanto un oggetto può aggiungere senza che la scheda lo dica (attrezzi perfetti: +2 di",
        "# circostanza, SRD «Tools and Skill Kits»); `sinergia` è il +2 di ogni fonte con 5 gradi",
        "oggetto = 2",
        "sinergia = 2",
        "",
        "# SRD, Saltare: la velocità diversa da `velocita` piedi toglie `meno` o dà `piu` ogni `ogni` piedi",
        "[salto]",
        *[f"{a} = {n}" for a, n in salto(CACHE).items()],
        "",
        "[fuori_classe]",
        "# SRD, «Skills Summary»: un grado in un'abilità fuori classe costa 2 punti e il massimo",
        "# è la metà di quello di classe",
        "costo = 2",
        "massimo_diviso = 2",
        "",
    ]
    con, doppia, armature, scudi = penalita_di_prova(CACHE, k)
    righe += [
        "[penalita_di_prova]",
        "# SRD, «Armor Check Penalty»: la penalità dell'armatura e dello scudo si sommano e vanno",
        "# alle abilità di `abilita`; a quelle di `doppia` vanno due volte. `perfetta`: quanto",
        "# un'armatura perfetta (e ogni armatura magica lo è) la riduce; `mithral` e `legnoscuro`:",
        "# quanto la riducono i materiali speciali, perfetta compresa.",
        "abilita = [" + ", ".join(_q(x) for x in con) + "]",
        "doppia = [" + ", ".join(_q(x) for x in doppia) + "]",
        "perfetta = 1",
        "mithral = 3",
        "legnoscuro = 2",
        "",
        "[penalita_di_prova.armature]",
        *[f"{_q(n)} = {{ ca = {v['ca']}, des_max = {v['des_max']}, penalita = {v['penalita']} }}"
          for n, v in armature.items()],
        "",
        "[penalita_di_prova.scudi]",
        *[f"{_q(n)} = {{ ca = {v['ca']}, penalita = {v['penalita']} }}" for n, v in scudi.items()],
        "",
    ]
    return "\n".join(righe)


def main(argv: "list[str]") -> int:
    if not CACHE.is_dir():
        print(f"estrai_gradi: manca la cache {CACHE} (python3 scripts/riscontro_srd.py scarica)", file=sys.stderr)
        return 2
    file = {OUT: genera(), OUT_PF: genera_pf1e()}
    if "--check" in argv:
        vecchi = [f.name for f, t in file.items() if not f.is_file() or f.read_text(encoding="utf-8") != t]
        print("✓ gradi.toml aggiornati" if not vecchi else "✗ da rigenerare: " + ", ".join(vecchi))
        return 1 if vecchi else 0
    for f, t in file.items():
        f.write_text(t, encoding="utf-8")
    print(f"3.5: {len(chiavi(CACHE))} abilità, {len(classi(CACHE))} classi, {len(tipi(CACHE))} tipi; "
          f"PF1e: {OUT_PF.read_text(encoding='utf-8').count(' = ') - 5} voci")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
