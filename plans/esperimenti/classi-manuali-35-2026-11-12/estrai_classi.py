#!/usr/bin/env python3
"""estrai_classi.py — le classi 3.5 fuori SRD: dado vita, BAB, tiri salvezza, punti abilità.

Due fonti, lette e messe a confronto (ADR-0124 §8):
  1. le pagine delle classi di srd.dndtools.org (`srd/classes/<sezione>/<classe>.html`):
     «Hit Die», «Skill Points at Each (Additional) Level», la tabella «Level |
     Base Attack Bonus | Fort | Ref | Will», l'elenco «class skills»;
  2. i file `*classes*.lst` di PCGen (BahamutDragon/pcgen): `HD:`, `BONUS:COMBAT|BASEAB`,
     `BONUS:SAVE|BASE.x`, `STARTSKILLPTS`.
Si prendono **solo nome e numeri** (scelta del DM, 2026-11-12): nessun testo.
Dove le due fonti divergono vince la tabella del manuale e la voce porta `diverge`.

Uso:
  python3 estrai_classi.py scarica CARTELLA              # scarica le pagine (elenco dalla sitemap)
  python3 estrai_classi.py PAGINE [--pcgen CLONE]        # scrive sistemi/dnd35/dati/classi_manuali.toml
  python3 estrai_classi.py PAGINE [--pcgen CLONE] --check
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ESCE = ROOT / "sistemi" / "dnd35" / "dati" / "classi_manuali.toml"
SITEMAP = "https://srd.dndtools.org/sitemap.xml"

#: sezione del sito → manuale (le sigle sono del sito)
LIBRI = {"Cad": "Complete Adventurer", "Carc": "Complete Arcane", "Cd": "Complete Divine",
         "Core": "SRD", "Cpsi": "Complete Psionic", "CPsi": "Complete Psionic", "Cwar": "Complete Warrior",
         "Dc": "Dragon Compendium", "Dragonlance": "Dragonlance Campaign Setting", "Drm": "Dragon Magic",
         "Dungeon": "Dungeonscape", "Ds": "Dungeonscape", "Ecs": "Eberron Campaign Setting",
         "Hoh": "Heroes of Horror", "Mh": "Miniatures Handbook", "MH": "Miniatures Handbook",
         "Moi": "Magic of Incarnum", "Oa": "Oriental Adventures", "Other": "web", "Phb2": "Player's Handbook II",
         "Psionic": "SRD (psionici)", "Tob": "Tome of Battle", "Tom": "Tome of Magic",
         "BoED": "Book of Exalted Deeds", "CChamp": "Complete Champion", "CScou": "Complete Scoundrel",
         "City": "Cityscape", "Cmage": "Complete Mage", "Dotu": "Drow of the Underdark",
         "Dramag": "Dragon Magazine", "Dunmag": "Dungeon Magazine", "Epic": "SRD (epici)",
         "Fc2": "Fiendish Codex II", "Sand": "Sandstorm", "Ud": "Underdark"}
TS = ("temp", "rifl", "vol")


class _Testo(HTMLParser):
    """Il testo di una pagina, con «|» al posto di ogni marcatore; script, stili e commenti fuori."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pezzi: "list[str]" = []
        self._muto = 0

    def handle_starttag(self, tag, attrs):
        self._muto += tag in ("script", "style")
        self.pezzi.append("|")

    def handle_startendtag(self, tag, attrs):
        self.pezzi.append("|")

    def handle_endtag(self, tag):
        self._muto = max(0, self._muto - (tag in ("script", "style")))
        self.pezzi.append("|")

    def handle_data(self, data):
        if not self._muto:
            self.pezzi.append(data)


def _testo(pagina: str) -> str:
    lettore = _Testo()
    lettore.feed(pagina)
    lettore.close()
    t = "".join(lettore.pezzi)
    return re.sub(r"\s+", " ", t.replace("�", "'").replace("’", "'"))


def _nome(file: str) -> str:
    s = file.split("__", 1)[1].removesuffix(".html")
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s).lower()


def _celle(riga: str) -> "list[str]":
    return [c.strip() for c in riga.split("|") if c.strip()]


def leggi_pagina(file: Path) -> "dict | None":
    """I numeri di una classe da una pagina del sito, o None se la pagina non è una classe."""
    t = _testo(file.read_text(encoding="utf-8", errors="replace"))
    dv = re.search(r"Hit Di(?:e|ce)\s*\|?\s*:\s*\|?\s*d(\d+)", t)
    if not dv:
        return None
    fuori: dict = {"dv": int(dv.group(1))}
    m = re.search(r"Skill Points at Each (?:Additional )?Level\s*\|?\s*:\s*\|?\s*(\d+)\s*\+\s*Int", t)
    if m:
        fuori["punti"] = int(m.group(1))
    m = re.search(r"class skills[^.]{0,80}? are (.+?)\.\s*\|", t)
    if m:
        ab = [re.sub(r"\s*\((?:Str|Dex|Con|Int|Wis|Cha|None|none)[^)]*\)", "", a).strip(" ,").lower()
              for a in re.split(r"\((?:Str|Dex|Con|Int|Wis|Cha|None|none)[^)]*\)", m.group(1).replace("|", " "))]
        ab = [re.sub(r"^(?:and|,)\s+", "", re.sub(r"\s+", " ", a)).strip(" ,") for a in ab]
        fuori["abilita"] = sorted({a for a in ab if a and len(a) < 40})
    # la tabella: dopo «Base Attack Bonus … Will Save» le righe «1st | +0 | +0 | +0 | +2»
    i = re.search(r"Level\s*\|[\s|]*Base\s*\|?\s*Attack\s*\|?\s*Bonus", t)
    righe = re.findall(r"\b(\d{1,2})(?:st|nd|rd|th)\s*\|[\s|]*([+-]?\d+)(?:/[+\d/]+)?\s*\|[\s|]*\+(\d+)\s*\|[\s|]*\+(\d+)\s*\|[\s|]*\+(\d+)",
                       t[i.start():] if i else "")
    liv = {}
    for n, bab, f, r, w in righe:
        liv.setdefault(int(n), (int(bab), int(f), int(r), int(w)))
    if not liv or 1 not in liv:
        return fuori
    ultimo = max(k for k in liv if all(j in liv for j in range(1, k + 1)))
    bab = liv[ultimo][0]
    fuori["livelli"] = ultimo
    fuori["bab"] = next((p for p in (1.0, 0.75, 0.5) if int(p * ultimo) == bab), None)
    if fuori["bab"] is None:
        del fuori["bab"]
        fuori["bab_irregolare"] = [liv[k][0] for k in range(1, ultimo + 1)]
    # un tiro salvezza è buono se al 1° vale +2 (classi base e di prestigio 3.5)
    fuori["ts_buoni"] = [TS[j] for j in range(3) if liv[1][j + 1] >= 2]
    # la progressione di prestigio «+0/+1/+1» al 1° non è né buona né scarsa del Core
    medi = [TS[j] for j in range(3) if liv[1][j + 1] == 1]
    if medi:
        fuori["ts_medi"] = medi
    return fuori


def leggi_pcgen(clone: Path) -> "dict[str, dict]":
    """nome → numeri, dalle righe CLASS: dei file *classes*.lst."""
    fuori: dict[str, dict] = {}
    for f in sorted(clone.glob("data/35e/**/*class*.lst")):
        libro = f.parent.name.replace("_", " ").title()
        ultima = None
        for riga in f.read_text(encoding="utf-8", errors="replace").splitlines():
            # «1<TAB>ABILITY:FEAT|VIRTUAL|Diehard»: un talento che la classe concede a quel livello
            m = re.match(r"(\d+)\t", riga)
            if m and ultima in fuori:
                for dono in re.findall(r"ABILITY:FEAT\|(?:VIRTUAL|AUTOMATIC)\|([^\t]+)", riga):
                    nomi = [x.strip() for x in dono.split("|") if x.strip() and not x.startswith("PRE")]
                    nomi = [re.sub(r"\s*\(", " (", x) for x in nomi if "Proficiency" not in x]
                    if nomi:
                        fuori[ultima].setdefault("talenti_concessi", {}).setdefault(m.group(1), []).extend(nomi)
                continue
            if not riga.startswith("CLASS:") or riga.startswith("CLASS:CATEGORY="):
                continue
            ultima = riga.split("\t")[0][6:].split(".MOD")[0].strip().lower()
            campi = riga.split("\t")
            nome = campi[0][6:].split(".MOD")[0].strip().lower()
            v = fuori.setdefault(nome, {"libro": libro})
            for c in campi[1:]:
                if c.startswith("HD:"):
                    v["dv"] = int(c[3:])
                elif c.startswith("STARTSKILLPTS:") and c[14:].isdigit():
                    v["punti"] = int(c[14:])
                elif c.startswith("BONUS:COMBAT|BASEAB|") and "PREVAREQ:UseFractionalBAB,1" not in c:
                    e = c.split("|")[2]
                    v["bab"] = 0.75 if "*3/4" in e else 0.5 if "/2" in e else 1.0
                elif c.startswith("TYPE:"):
                    v["tipi"] = c[5:].split(".")
                elif c.startswith("BONUS:SAVE|"):
                    quali, e = c.split("|")[1].split(","), c.split("|")[2].replace(" ", "")
                    for q in quali:   # «BASE.Fortitude,BASE.Will» su una riga sola
                        chiave = {"BASE.Fortitude": "temp", "BASE.Reflex": "rifl", "BASE.Will": "vol"}.get(q)
                        if chiave is None:
                            continue
                        buoni = v.setdefault("ts_buoni", [])
                        if "/2+2" in e and chiave not in buoni:
                            buoni.append(chiave)
                        elif "/2+2" not in e and "/3" not in e:
                            v["ts_illeggibili"] = True   # progressioni di prestigio scritte in altro modo
    # solo classi da personaggio: via i dadi vita razziali («Humanoid», «Crystal Dragon»),
    # le classi decadute («Ex-…») e quelle con i tiri salvezza scritti in un modo che non si legge
    for v in fuori.values():
        v["prestigio"] = "Prestige" in v.get("tipi", ())
    return {k: {x: y for x, y in v.items() if x not in ("tipi", "ts_illeggibili")} for k, v in fuori.items()
            if "dv" in v and not v.get("ts_illeggibili") and not k.startswith(("ex ", "ex-"))
            and set(v.get("tipi", ())) & {"Base", "PC", "Prestige", "NPC"} and "Monster" not in v.get("tipi", ())}


def raccogli(pagine: Path, clone: "Path | None") -> "tuple[dict, dict]":
    sys.path.insert(0, str(ROOT / "scripts"))
    from dmcore import sistemi as S
    srd = S.dati("dnd35", "creature.costruzione")
    noti = set(srd["classi"]) | set(srd["prestigio"])
    pc = leggi_pcgen(clone) if clone else {}
    classi, conto = {}, {"pagine": 0, "senza_dado": 0, "srd": 0, "senza_tabella": 0, "bab_irregolare": 0,
                         "in_comune": 0, "uguali": 0, "diverse": 0, "solo_pcgen": 0}
    for f in sorted(pagine.glob("*__*.html")):
        conto["pagine"] += 1
        v = leggi_pagina(f)
        if v is None:
            conto["senza_dado"] += 1
            continue
        nome = _nome(f.name)
        if nome in noti:
            conto["srd"] += 1
            continue
        sez = re.sub(r"^(base|prestige)", "", f.name.split("__")[0])
        v["prestigio"] = f.name.startswith("prestige")
        v["libro"] = LIBRI.get(sez, sez)
        v["dati"] = "dndtools"
        if "bab" not in v and "bab_irregolare" not in v:
            conto["senza_tabella"] += 1
        conto["bab_irregolare"] += "bab_irregolare" in v
        p = pc.get(nome)
        if p:
            p = {k: x for k, x in p.items() if k != "prestigio"}
            conto["in_comune"] += 1
            diversi = [k for k in ("dv", "bab", "punti") if k in v and k in p and v[k] != p[k]]
            if "ts_buoni" in v and "ts_buoni" in p and sorted(v["ts_buoni"]) != sorted(p["ts_buoni"]) \
                    and not v.get("ts_medi"):
                diversi.append("ts_buoni")
            if p.get("talenti_concessi"):
                v["talenti_concessi"] = p["talenti_concessi"]
            for k in ("bab", "punti", "ts_buoni"):   # ciò che la pagina non dà e PCGen sì
                if k not in v and k in p and "bab_irregolare" not in v:
                    v[k] = p[k]
            v["dati"] = "dndtools+pcgen"
            if diversi:
                v["diverge"] = diversi
            conto["diverse" if diversi else "uguali"] += 1
        classi[nome] = v
    for nome, p in pc.items():
        if nome not in classi and nome not in noti and {"bab", "ts_buoni"} <= set(p) \
                and not re.search(r"\(|~|substitution|racial|level\b", nome):
            classi[nome] = {**p, "dati": "pcgen"}
            conto["solo_pcgen"] += 1
    for riga in (ROOT / "scripts" / "lessico_it_35.tsv").read_text(encoding="utf-8").splitlines():
        campi = riga.split("\t")   # il nome italiano, dal lessico del repo
        if len(campi) >= 3 and campi[2] in ("classe", "classe di prestigio") and campi[1].lower() in classi:
            classi[campi[1].lower()].setdefault("it", campi[0].lower())
    conto["con_nome_italiano"] = sum("it" in v for v in classi.values())
    return classi, conto


def _toml(v) -> str:
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{json.dumps(k)} = {_toml(x)}" for k, x in sorted(v.items(), key=lambda t: int(t[0]))) + " }"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_toml(x) for x in v) + "]"
    return json.dumps(v, ensure_ascii=False)


ORDINE = ("it", "dv", "bab", "bab_irregolare", "ts_buoni", "ts_medi", "punti", "livelli", "prestigio",
          "libro", "dati", "diverge", "talenti_concessi", "abilita")


def scrivi(classi: dict, conto: dict) -> str:
    righe = ["# sistemi/dnd35/dati/classi_manuali.toml — le classi 3.5 fuori SRD (ADR-0124 §8)",
             "# Generato da plans/esperimenti/classi-manuali-35-2026-11-12/estrai_classi.py dalle pagine",
             "# delle classi di srd.dndtools.org e dai file *classes*.lst di PCGen (BahamutDragon/pcgen).",
             "# Solo nome e numeri: dado vita, BAB per livello, tiri salvezza buoni, punti abilità per",
             "# livello, abilità di classe. Nessun testo dei manuali. Un nome dell'SRD vince sempre.",
             f"# {len(classi)} classi; {conto['in_comune']} in tutte e due le fonti, {conto['diverse']} con numeri diversi",
             "# (campo `diverge`: vince la tabella del manuale, la voce va riletta sul libro).",
             "", "[classi_manuali]"]
    for nome in sorted(classi):
        v = classi[nome]
        righe.append(f"{json.dumps(nome, ensure_ascii=False)} = {{ "
                     + ", ".join(f"{k} = {_toml(v[k])}" for k in ORDINE if k in v) + " }")
    return "\n".join(righe) + "\n"


def scarica(cartella: Path) -> None:
    cartella.mkdir(parents=True, exist_ok=True)
    mappa = subprocess.run(["curl", "-sS", "-m", "60", SITEMAP], capture_output=True, text=True, check=True).stdout
    for u in re.findall(r"<loc>([^<]*/classes/[^<]*)", mappa):
        dest = cartella / u.split("/classes/")[1].replace("/", "__")
        if not dest.exists() or not dest.stat().st_size:
            subprocess.run(["curl", "-sS", "-m", "40", "-o", str(dest), u.replace("http://", "https://")], check=False)


def main(argv: "list[str]") -> int:
    if argv and argv[0] == "scarica":
        scarica(Path(argv[1]))
        return 0
    pagine = Path(argv[0])
    clone = Path(argv[argv.index("--pcgen") + 1]) if "--pcgen" in argv else None
    classi, conto = raccogli(pagine, clone)
    testo = scrivi(classi, conto)
    if "--check" in argv:
        ok = ESCE.exists() and ESCE.read_text(encoding="utf-8") == testo
        print("classi_manuali.toml", "aggiornato" if ok else "DA RIGENERARE")
        return 0 if ok else 1
    ESCE.write_text(testo, encoding="utf-8")
    print(json.dumps(conto, ensure_ascii=False))
    print(f"{len(classi)} classi → {ESCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
