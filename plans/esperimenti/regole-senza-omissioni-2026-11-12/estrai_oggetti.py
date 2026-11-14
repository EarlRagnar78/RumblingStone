#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/oggetti.toml`: i prezzi degli oggetti magici e il valore
dell'equipaggiamento di un PNG per livello (ADR-0126, lotto 8).

Uso: python3 estrai_oggetti.py [<cartella srd-v3.5-md>]            # scrive il file
     python3 estrai_oggetti.py --check [<cartella srd-v3.5-md>]    # 1 se il file non è aggiornato

Dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL), solo nomi e numeri:
  potenziamento  «Table: Weapons» e «Table: Armor and Shields»: il prezzo base del bonus +N
  prezzi         ogni riga con un «Market Price» delle tabelle di armature, scudi e armi
                 specifiche, pozioni, anelli, verghe, bastoni, bacchette e oggetti meravigliosi
  capacita       le tabelle delle capacità speciali di armi, armature e scudi
  pergamene      le tabelle delle pergamene arcane e divine
  materiali      «Special Materials»: quanto costano in più adamantio e mithral
  comuni         «Equipment»: il prezzo di armi, armature e scudi non magici e della
                 fattura perfetta

Non dall'SRD (che non l'ha), solo numeri:
  png            Dungeon Master's Guide 3.5, Tabella 4-23 «NPC Gear Value», riscontrata il
                 2026-11-13 su realmshelps.net/charbuild/classes/npc
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "dnd35" / "dati" / "oggetti.toml"
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"

#: tabella dell'SRD → prefisso che fa del nome della riga il nome dell'oggetto
TABELLE = {
    "Specific Armors": "", "Specific Shields": "", "Specific Weapons": "",
    "Potions and Oils": "potion of ", "Rings": "ring of ", "Rods": "rod of ", "Staffs": "staff of ",
    "Wands": "wand of ", "Minor Wondrous Items": "", "Medium Wondrous Items": "", "Major Wondrous Items": "",
}
#: DMG 3.5, Tabella 4-23: il valore dell'equipaggiamento di un PNG dal 1° al 20° livello
PNG = [900, 2000, 2500, 3300, 4300, 5600, 7200, 9400, 12000, 16000,
       21000, 27000, 35000, 45000, 59000, 77000, 100000, 130000, 170000, 220000]
#: come una scheda italiana o inglese scrive un oggetto (non viene dall'SRD). «N» nel nome è il
#: bonus letto dal primo gruppo dello schema.
NOMI = [
    ("ring of protection +N", r"(?:anello|ring)\s+(?:di|della|of)\s+(?:protezione|deviazione|protection)\s*\+(\d)"),
    ("cloak of resistance +N", r"(?:mantello|cloak)\s+(?:della|di|of)\s+(?:resistenza|resistance)\s*\+(\d)"),
    ("cloak of charisma +N", r"(?:mantello|cloak)\s+(?:del|di|of)\s+(?:carisma|charisma)\s*\+(\d)"),
    ("amulet of health +N", r"(?:amuleto|amulet)\s+(?:della|di|of)\s+(?:salute|health)\s*\+(\d)"),
    ("amulet of natural armor +N",
     r"(?:amuleto|amulet)\s+(?:(?:dell['’]|di|of)\s*)?(?:armatura naturale|natural armor)\s*\+(\d)"),
    ("gauntlets of ogre power", r"guanti\s+della\s+forza\s+dell['’]\s*ogre|gauntlets\s+of\s+ogre\s+power"),
    ("gloves of dexterity +N", r"(?:guanti|gloves)\s+(?:della|di|of)\s+(?:destrezza|dexterity)\s*\+(\d)"),
    ("belt of giant strength +N",
     r"(?:cintura\s+della\s+forza\s+(?:del|dei)\s+gigant[ei]|belt\s+of\s+giant\s+strength)\s*\+(\d)"),
    ("headband of intellect +N", r"(?:fascia\s+dell['’]\s*intelletto|headband\s+of\s+intellect)\s*\+(\d)"),
    ("periapt of wisdom +N",
     r"(?:(?:periapto|pendente)\s+(?:della|di)\s+saggezza|periapt\s+of\s+wisdom)\s*\+(\d)"),
    ("bracers of armor +N", r"(?:bracciali\s+(?:dell['’]|di)\s*armatura|bracers\s+of\s+armor)\s*\+(\d)"),
    ("boots of speed", r"stivali\s+(?:di|della)\s+velocit[àa]|boots\s+of\s+speed"),
    ("ring of mind shielding", r"(?:anello|ring)\s+(?:di|dello|of)\s+(?:mind shielding|schermo mentale)"),
]


def _celle(riga: str) -> "list[str]":
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", riga, re.S)]


def _tabelle(base: Path):
    for f in sorted((base / "magic-items").glob("*.md")):
        for m in re.finditer(r"<table[^>]*><caption>Table: (.*?)</caption>(.*?)</table>",
                             f.read_text(encoding="utf-8"), re.S):
            yield m.group(1), [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", m.group(2), re.S)]


def _mo(cella: str) -> "int | None":
    m = re.fullmatch(r"\+?([\d,]+) gp", cella.strip())
    return int(m.group(1).replace(",", "")) if m else None


def potenziamento(base: Path) -> "dict[str, list[int]]":
    out: dict[str, dict[int, int]] = {"arma": {}, "armatura": {}}
    for nome, righe in _tabelle(base):
        if nome not in ("Weapons", "Armor and Shields"):
            continue
        for r in righe[1:]:
            if len(r) < 2:
                continue
            m = re.fullmatch(r"\+(\d+)(?: (?:armor|shield))?\d?", r[-2])
            mo = _mo(r[-1])
            if m and mo is not None:
                out["arma" if nome == "Weapons" else "armatura"].setdefault(int(m.group(1)), mo)
    return {k: [v[i] for i in sorted(v)] for k, v in out.items()}


def prezzi(base: Path) -> "dict[str, int]":
    out: dict[str, int] = {}
    for nome, righe in _tabelle(base):
        if nome not in TABELLE:
            continue
        for r in righe[1:]:
            if len(r) < 2 or _mo(r[-1]) is None:
                continue
            voce = re.sub(r"\d$", "", r[-2]).strip() if not re.search(r"[+ ]\d$", r[-2]) else r[-2]
            chiave = (TABELLE[nome] + voce).lower().replace("’", "'")
            out.setdefault(chiave, _mo(r[-1]))
    return dict(sorted(out.items()))


def capacita(base: Path) -> "dict[str, dict[str, dict]]":
    """Le capacità speciali di armi, armature e scudi: bonus equivalente («+1 bonus») o prezzo in mo."""
    out: dict[str, dict[str, dict]] = {"arma": {}, "armatura": {}}
    for nome, righe in _tabelle(base):
        if not nome.endswith("Special Abilities"):
            continue
        dove = out["arma" if "Weapon" in nome else "armatura"]
        for r in righe[1:]:
            if len(r) < 2:
                continue
            voce = re.sub(r"\d$", "", r[-2]).strip().lower()
            m = re.fullmatch(r"\+(\d+) bonus\d?", r[-1])
            mo = _mo(re.sub(r"(?<=gp)\d$", "", r[-1]))
            if m:
                dove.setdefault(voce, {"bonus": int(m.group(1))})
            elif mo is not None:
                dove.setdefault(voce, {"mo": mo})
    return {k: dict(sorted(v.items())) for k, v in out.items()}


def pergamene(base: Path) -> "dict[str, int]":
    """Il prezzo più basso di una pergamena per incantesimo (arcana o divina), in mo intere."""
    out: dict[str, int] = {}
    for nome, righe in _tabelle(base):
        if not nome.endswith("Spell Scrolls"):
            continue
        for r in righe:
            m = re.fullmatch(r"([\d,]+) gp(?: 5 sp)?\d?", r[-1]) if len(r) == 3 else None
            if m:
                voce = r[1].lower().replace("’", "'")
                mo = int(m.group(1).replace(",", ""))
                out[voce] = min(out.get(voce, mo), mo)
    return dict(sorted(out.items()))


#: riga delle tabelle di «Special Materials» → chiave del plugin
MATERIALI = {"Light armor": "leggera", "Medium armor": "media", "Heavy armor": "pesante",
             "Weapon": "arma", "Shield": "scudo"}


def materiali(base: Path) -> "dict[str, dict[str, int]]":
    """Quanto costa in più un oggetto di adamantio o di mithral (mo), per categoria."""
    out: dict[str, dict[str, int]] = {}
    f = base / "basic-rules-and-legal" / "special-materials.md"
    for m in re.finditer(r"<table[^>]*>(.*?)</table>", f.read_text(encoding="utf-8"), re.S):
        righe = [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", m.group(1), re.S)]
        t = re.fullmatch(r"Type of (Adamantine|Mithral) Item", righe[0][0]) if righe and righe[0] else None
        if not t:
            continue
        for r in righe[1:]:
            if len(r) == 2 and r[0] in MATERIALI and _mo(r[1]) is not None:
                out.setdefault(t.group(1).lower(), {})[MATERIALI[r[0]]] = _mo(r[1])
    return out


def comuni(base: Path) -> "dict[str, dict]":
    """Il prezzo in mo intere di armi, armature e scudi comuni («Table: Weapons», «Table: Armor and
    Shields») e della fattura perfetta. Gli scudi vanno per bonus di CA, col prezzo più basso: una
    scheda dice «scudo pesante» e non se è di legno o d'acciaio. Chi costa meno di 1 mo resta fuori."""
    f = (base / "basic-rules-and-legal" / "equipment.md").read_text(encoding="utf-8")
    out: dict[str, dict] = {"armi": {}, "armature": {}, "scudi": {}}
    for m in re.finditer(r"<table[^>]*><caption>Table: (Weapons|Armor and Shields)</caption>(.*?)</table>", f, re.S):
        dove = ""
        for r in (_celle(x) for x in re.findall(r"<tr>(.*?)</tr>", m.group(2), re.S)):
            if len(r) < 3:
                continue
            nome = re.sub(r"\s+", " ", re.sub(r"\d$", "", r[0].replace("&nbsp;", " "))).strip().lower()
            dove = {"shields": "scudi", "extras": "", "light armor": "armature"}.get(nome, dove)
            mo = _mo(r[1])
            if mo is None or mo < 1:
                continue
            if m.group(1) == "Weapons":
                out["armi"].setdefault(re.sub(r"\s*\(\d+\)$", "", nome), mo)
            elif dove == "armature":
                out["armature"][nome] = mo
            elif dove == "scudi" and (b := re.fullmatch(r"\+(\d)\d?", r[2])):
                out["scudi"][b.group(1)] = min(out["scudi"].get(b.group(1), mo), mo)
    arma = re.search(r"The masterwork quality adds (\d+) gp to the cost of a normal weapon", f)
    armatura = re.search(r"A masterwork suit of armor or shield costs an extra (\d+) gp", f)
    out["perfetta"] = {"arma": int(arma.group(1)), "armatura": int(armatura.group(1))}
    return out


def testo(base: Path) -> str:
    pot, pr = potenziamento(base), prezzi(base)
    cap, perg, mat, com = capacita(base), pergamene(base), materiali(base), comuni(base)
    righe = [
        "# sistemi/dnd35/dati/oggetti.toml — prezzi degli oggetti magici e valore dell'equipaggiamento",
        "# di un PNG per livello (ADR-0126, lotto 8)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_oggetti.py",
        "# dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL). Non si corregge a mano.",
        "",
        "[oggetti.png]",
        "# NON dall'SRD, che non l'ha: Dungeon Master's Guide 3.5, Tabella 4-23 «NPC Gear Value»,",
        "# solo i numeri (mo dal 1° al 20° livello), riscontrati il 2026-11-13 su",
        "# realmshelps.net/charbuild/classes/npc",
        f"per_livello = {PNG}",
        "",
        "[oggetti.potenziamento]",
        "# SRD, «Table: Weapons» e «Table: Armor and Shields»: prezzo base del bonus da +1 in su (mo)",
        f"arma = {pot['arma']}",
        f"armatura = {pot['armatura']}",
        "",
        "[oggetti.prezzi]",
        "# SRD, tabelle degli oggetti magici: «Market Price» (mo). Anelli, verghe, bastoni, bacchette",
        "# e pozioni hanno davanti il nome della loro tabella.",
    ]
    righe += [f'"{k}" = {v}' for k, v in pr.items()]
    for che, titolo in (("arma", "Melee/Ranged Weapon Special Abilities"),
                        ("armatura", "Armor/Shield Special Abilities")):
        righe += ["", f"[oggetti.capacita.{che}]",
                  f"# SRD, «Table: {titolo}»: bonus equivalente da sommare al potenziamento, o prezzo in mo"]
        righe += [f'"{k}" = {{ {next(iter(v))} = {next(iter(v.values()))} }}' for k, v in cap[che].items()]
    righe += ["", "[oggetti.pergamene]",
              "# SRD, «Table: Arcane Spell Scrolls» e «Table: Divine Spell Scrolls»: il prezzo più basso (mo intere)"]
    righe += [f'"{k}" = {v}' for k, v in perg.items()]
    for nome, voci in sorted(mat.items()):
        righe += ["", f"[oggetti.materiali.{nome}]",
                  "# SRD, «Special Materials»: costo in più dell'oggetto (mo), per categoria"]
        righe += [f"{k} = {v}" for k, v in voci.items()]
    righe += ["", "[oggetti.perfetta]",
              "# SRD, «Masterwork Weapons» e «Masterwork Armor»: quanto costa in più la fattura perfetta (mo)"]
    righe += [f"{k} = {v}" for k, v in com["perfetta"].items()]
    for che, nota in (("armi", "«Table: Weapons»: prezzo dell'arma di taglia Media (mo intere)"),
                      ("armature", "«Table: Armor and Shields»: prezzo dell'armatura (mo)"),
                      ("scudi", "«Table: Armor and Shields»: per bonus di CA, lo scudo che costa meno (mo)")):
        righe += ["", f"[oggetti.comuni.{che}]", f"# SRD, {nota}"]
        righe += [f'"{k}" = {v}' for k, v in sorted(com[che].items())]
    righe += ["", "# come una scheda scrive un oggetto (espressioni regolari; non vengono dall'SRD). «N» è il bonus letto."]
    for nome, schema in NOMI:
        righe += ["[[oggetti.nomi]]", f'nome = "{nome}"', f"schema = '''{schema}'''", ""]
    return "\n".join(righe).rstrip("\n") + "\n"


def main(argv: "list[str]") -> int:
    check = "--check" in argv
    resto = [a for a in argv if a != "--check"]
    base = Path(resto[0]) if resto else CACHE
    if not base.is_dir():
        print(f"estrai_oggetti: manca {base}", file=sys.stderr)
        return 2
    nuovo = testo(base)
    if check:
        if not DEST.is_file() or DEST.read_text(encoding="utf-8") != nuovo:
            print(f"estrai_oggetti: {DEST.relative_to(ROOT)} non è aggiornato", file=sys.stderr)
            return 1
        return 0
    DEST.write_text(nuovo, encoding="utf-8")
    print(f"estrai_oggetti: scritto {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
