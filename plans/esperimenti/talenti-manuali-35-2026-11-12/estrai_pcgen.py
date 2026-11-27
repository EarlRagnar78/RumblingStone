#!/usr/bin/env python3
"""estrai_pcgen.py — prerequisiti dei talenti 3.5 fuori SRD dai dati PCGen (2026-11-12).

Il repo aveva i **nomi** dei talenti di tutti i manuali 3.5
(`scripts/talenti_manuali_35.tsv`) ma non i prerequisiti: dndtools.net non
risponde. I dati PCGen di BahamutDragon/pcgen (formato LST, campi PRExxx)
li hanno in forma già strutturata per i manuali Wizards of the Coast. Da lì si
prendono **solo il nome, il manuale e i prerequisiti** (regole di gioco, non
testo): DESC, BENEFIT e il resto si scartano, come per i nomi.

Traduzione dei campi PCGen nello schema di `sistemi/dnd35/dati/talenti.toml`:
  PRESTAT:1,STR=13          → car = {For = 13}
  PRETOTALAB:n / PREATT:n   → bab = n
  PREABILITY:k,CATEGORY=FEAT,A,B   → talenti = [A, B] se k = numero dei nomi,
                                     altrimenti altro («uno fra A, B»)
  PRECLASS:1,Fighter=4      → classe = {fighter = 4}
  PRELEVEL:MIN=n            → classe = {character = n}
  PRESKILL:1,Hide=8         → gradi = {hide = 8}
  PREMULT:k,[…],[…]         → se k = numero dei rami, ogni ramo come sopra;
                              altrimenti altro
  tutto il resto (PRECHECKBASE, PRERACE, PRESIZE, PREVARGTEQ, PREALIGN, …)
                            → altro, col testo di PRETEXT quando c'è
`altro` è un prerequisito che la regola non sa leggere: lo strumento lo mette
fra i non verificabili, non lo giudica.

Uso
  python3 estrai_dndtools.py scarica PAGINE             # le pagine dei manuali
  python3 estrai_pcgen.py CLONE_PCGEN --dndtools PAGINE          # scrive il TOML
  python3 estrai_pcgen.py CLONE_PCGEN --dndtools PAGINE --check  # confronta

Clone (solo i file dei talenti WotC 3.5):
  git clone --depth 1 --filter=blob:none --sparse https://github.com/BahamutDragon/pcgen
  git -C pcgen sparse-checkout set --no-cone '/data/35e/wizards_of_the_coast/**/*feat*.lst'
"""
from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "plans" / "esperimenti" / "regole-complete-2026-11-10"))
OUT = ROOT / "sistemi" / "dnd35" / "dati" / "talenti_manuali.toml"
SRD = ROOT / "sistemi" / "dnd35" / "dati" / "talenti.toml"
CAR = {"STR": "For", "DEX": "Des", "CON": "Cos", "INT": "Int", "WIS": "Sag", "CHA": "Car"}
CLASSI = {"barbarian", "bard", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue",
          "sorcerer", "wizard"}


#: capacità di classe che `[capacita]` di talenti.toml sa già giudicare
CAPACITA = {frozenset({"Rage", "Frenzy"}): "rage", frozenset({"Rage"}): "rage",
            frozenset({"Turn Undead", "Rebuke Undead"}): "turn or rebuke creatures",
            frozenset({"Turn Undead"}): "turn or rebuke creatures",
            frozenset({"Wild Shape"}): "wild shape"}
TAGLIE_TAG = ("PRESIZEGTEQ",)
TAGLIE = {"S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan", "C": "Colossal"}


def _q(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _rami(v: str) -> "list[str]":
    """I rami di PREMULT: «2,[PREA:…],[PREB:…]» → ['PREA:…', 'PREB:…']."""
    out, prof, buf = [], 0, ""
    for ch in v.split(",", 1)[1]:
        if ch == "[":
            prof += 1
            if prof == 1:
                buf = ""
                continue
        if ch == "]":
            prof -= 1
            if prof == 0:
                out.append(buf)
                continue
        if prof >= 1:
            buf += ch
    return out


def traduci(tag: str, v: str, p: dict) -> None:
    """Aggiunge a `p` il prerequisito di un campo PRExxx."""
    neg = tag.startswith("!")
    tag = tag.lstrip("!")
    if neg:
        p.setdefault("altro", []).append(f"non {tag}:{v}")
        return
    if tag == "PREABILITY" and "CATEGORY=Special Ability" in v:
        tipi = {x.replace("TYPE.", "") for x in v.split(",")[2:]}
        for nomi, cap in CAPACITA.items():
            if tipi and tipi <= nomi:
                p.setdefault("capacita", []).append(cap)
                return
    if tag == "PRESTAT":
        k, *coppie = v.split(",")
        coppie = [c.split("=") for c in coppie if "=" in c]
        if k == str(len(coppie)) and all(c[0] in CAR for c in coppie):
            for c, n in coppie:
                p.setdefault("car", {})[CAR[c]] = int(n)
            return
    elif tag in ("PRETOTALAB", "PREATT") and v.strip().isdigit():
        p["bab"] = max(p.get("bab", 0), int(v))
        return
    elif tag == "PREABILITY":
        k, *resto = v.split(",")
        if resto and resto[0].upper() == "CATEGORY=FEAT":
            nomi = [x for x in resto[1:] if not x.startswith("TYPE")]
            if nomi and k == str(len(nomi)) and len(nomi) == len(resto) - 1:
                p.setdefault("talenti", []).extend(nomi)
                return
            if nomi and len(nomi) == len(resto) - 1:
                p.setdefault("altro", []).append(f"{k} fra i talenti " + ", ".join(nomi))
                return
    elif tag == "PRECHECKBASE":
        ts, _, n = v.split(",", 1)[1].partition("=")
        p.setdefault("altro", []).append(f"base {ts} save +{n}")
        return
    elif tag in TAGLIE_TAG and v in TAGLIE:
        p.setdefault("altro", []).append(f"size {TAGLIE[v]} or larger")
        return
    elif tag == "PRECLASS" and re.fullmatch(r"1,SPELLCASTER(\.Arcane|\.Divine)?=\d+", v):
        tipo, n = re.fullmatch(r"1,SPELLCASTER(?:\.(\w+))?=(\d+)", v).groups()
        p.setdefault("capacita", []).append(f"cast {tipo.lower()} spells" if tipo else "cast spells")
        if int(n) > 1:
            p["lic"] = max(p.get("lic", 0), int(n))
        return
    elif tag == "PRECLASS":
        k, *coppie = v.split(",")
        coppie = [c.split("=") for c in coppie if "=" in c]
        if k == "1" and len(coppie) == 1 and coppie[0][0].rstrip("%").lower() in CLASSI:
            p.setdefault("classe", {})[coppie[0][0].rstrip("%").lower()] = int(coppie[0][1])
            return
    elif tag == "PRELEVEL" and v.startswith("MIN="):
        p.setdefault("classe", {})["character"] = int(v[4:])
        return
    elif tag == "PRESKILL":
        k, *coppie = v.split(",")
        coppie = [c.rsplit("=", 1) for c in coppie if "=" in c]
        if k == str(len(coppie)) and not any(c[0].startswith("TYPE") for c in coppie):
            for s, n in coppie:
                p.setdefault("gradi", {})[s.lower()] = int(n)
            return
    elif tag == "PREMULT":
        k = v.split(",")[0]
        rami = _rami(v)
        if rami and k == str(len(rami)):
            for r in rami:
                t, _, rv = r.partition(":")
                traduci(t, rv, p)
            return
    elif tag == "PRETEXT":
        p["_testo"] = v
        return
    p.setdefault("altro", []).append(f"{tag}:{v}")


def manuale(rel: str) -> str:
    """Il manuale dal percorso: «…/supplement/complete_warrior/cw_feats.lst» → «Complete Warrior»."""
    parti = rel.split("/")
    cartella = parti[-2] if parti[-2] not in ("campaign", "core") else parti[-3]
    return " ".join(w.capitalize() for w in cartella.split("_"))


def leggi(clone: Path) -> "dict[str, dict]":
    srd = tomllib.loads(SRD.read_text(encoding="utf-8"))["talenti"]
    base = clone / "data" / "35e" / "wizards_of_the_coast"
    out: dict[str, dict] = {}
    for f in sorted(base.rglob("*.lst")):
        if "feat" not in f.name.lower():
            continue
        rel = f.relative_to(clone).as_posix()
        for riga in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not riga.strip() or riga.startswith("#"):
                continue
            campi = [c for c in riga.split("\t") if c]
            nome = campi[0].strip()
            if "CATEGORY:FEAT" not in campi or "." in nome or "|" in nome or nome in srd or nome in out:
                continue
            p: dict = {"manuale": manuale(rel)}
            for c in campi[1:]:
                tag, _, v = c.partition(":")
                if tag.lstrip("!").startswith("PRE"):
                    traduci(tag, v, p)
                elif tag == "TYPE":
                    p["tipi"] = sorted(set(v.split(".")))
            testo = p.pop("_testo", None)
            if "altro" in p and testo and not (set(p) - {"manuale", "tipi", "altro"}):
                p["altro"] = [testo]
            out[nome] = p
    return out


CHIAVI = ("car", "bab", "lic", "classe", "gradi", "talenti", "capacita")


def fondi(pcgen: "dict[str, dict]", cartella: Path) -> "tuple[dict[str, dict], str]":
    """Le tabelle di srd.dndtools.org sopra i dati PCGen. Dove un talento sta in
    tutte e due le fonti vince la tabella del manuale (è il testo del libro; i
    campi PCGen sono codice di un programma e a volte saltano un requisito, per
    esempio il BAB +6 di Two-Weapon Pounce), ma un prerequisito **leggibile**
    che solo PCGen ha si aggiunge. Restituisce anche il conto del confronto."""
    import estrai_dndtools as D
    import estrai_talenti as E
    srd = tomllib.loads(SRD.read_text(encoding="utf-8"))["talenti"]
    noti = {E._k(n): n for n in list(srd) + list(pcgen)}
    tab = D.leggi(cartella, noti)
    out, uguali, diversi, solo_tab = dict(pcgen), 0, 0, 0
    chiavi_srd = {E._k(n) for n in srd}
    per_chiave = {E._k(n): n for n in pcgen}
    for nome, t in tab.items():
        if E._k(nome) in chiavi_srd:
            continue
        t = {**t, "dati": "dndtools"}
        nome = per_chiave.get(E._k(nome), nome)
        p = pcgen.get(nome)
        if p is None:
            solo_tab += 1
            out[nome] = t
            continue
        stesso = all(sorted(p.get(k) or []) == sorted(t.get(k) or []) if k in ("talenti", "capacita")
                     else (p.get(k) or 0) == (t.get(k) or 0) for k in CHIAVI)
        uguali += stesso
        diversi += not stesso
        t["manuale"], t["tipi"], t["dati"] = p["manuale"], p.get("tipi"), "dndtools+pcgen"
        if not stesso:
            t["diverge"] = True   # le due fonti non danno gli stessi prerequisiti: si rilegge sul libro
        for k in ("car", "classe", "gradi"):
            if p.get(k):
                t[k] = {**p[k], **t.get(k, {})}
        for k in ("bab", "lic"):
            if p.get(k) or t.get(k):
                t[k] = max(p.get(k, 0), t.get(k, 0))
        for k in ("talenti", "capacita"):
            if p.get(k) or t.get(k):
                t[k] = list(dict.fromkeys((t.get(k) or []) + (p.get(k) or [])))
        out[nome] = t
    conto = (f"tabelle srd.dndtools.org: {len(tab)} talenti; in comune con PCGen {uguali + diversi} "
             f"({uguali} con gli stessi prerequisiti leggibili, {diversi} diversi); solo nelle tabelle {solo_tab}")
    return out, conto


def scrivi(d: "dict[str, dict]", commit: str) -> str:
    righe = [
        "# Talenti 3.5 dei manuali Wizards of the Coast fuori dall'SRD: nome, manuale, prerequisiti.",
        "# Generato da plans/esperimenti/talenti-manuali-35-2026-11-12/estrai_pcgen.py dai dati PCGen",
        f"# di BahamutDragon/pcgen@{commit[:12]} (data/35e/wizards_of_the_coast/**/*feat*.lst) e dalle",
        "# tabelle Feat/Prerequisite dei manuali su srd.dndtools.org (estrai_dndtools.py). `dati` dice",
        "# da quale fonte viene la voce; dove ci sono tutte e due vince la tabella del manuale.",
        "# Solo i prerequisiti, che sono regole di gioco: niente testo dei manuali.",
        "# `altro` = prerequisito che la regola non sa leggere (non verificabile).",
        "# Si fonde in dmcore/talenti.py sotto i talenti dell'SRD: un nome dell'SRD vince sempre.",
        "",
    ]
    for nome in sorted(d):
        p = d[nome]
        righe.append(f"[talenti_manuali.{_q(nome)}]")
        righe.append(f"libro = {_q('3.5 ' + p['manuale'])}")
        righe.append(f"dati = {_q(p.get('dati', 'pcgen'))}")
        if p.get("diverge"):
            righe.append("diverge = true")
        if p.get("tipi"):
            righe.append("tipi = [" + ", ".join(_q(t) for t in p["tipi"]) + "]")
        for k in ("car", "classe", "gradi"):
            if p.get(k):
                righe.append(f"{k} = {{ " + ", ".join(f"{_q(a)} = {b}" for a, b in sorted(p[k].items())) + " }")
        if p.get("bab"):
            righe.append(f"bab = {p['bab']}")
        if p.get("lic"):
            righe.append(f"lic = {p['lic']}")
        for k in ("talenti", "capacita", "altro"):
            if p.get(k):
                righe.append(f"{k} = [" + ", ".join(_q(x) for x in dict.fromkeys(p[k])) + "]")
        righe.append("")
    return "\n".join(righe)


def main(argv: "list[str]") -> int:
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    clone = Path(argv[0])
    commit = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True,
                            text=True, check=True).stdout.strip()
    d = leggi(clone)
    for v in d.values():
        v["dati"] = "pcgen"
    if "--dndtools" in argv:
        d, conto = fondi(d, Path(argv[argv.index("--dndtools") + 1]))
        print(conto)
    testo = scrivi(d, commit)
    if "--check" in argv:
        ok = OUT.is_file() and OUT.read_text(encoding="utf-8") == testo
        print("✓ talenti_manuali.toml aggiornato" if ok else "✗ talenti_manuali.toml da rigenerare")
        return 0 if ok else 1
    OUT.write_text(testo, encoding="utf-8")
    d = tomllib.loads(testo)["talenti_manuali"]
    print(f"{len(d)} talenti, {sum('altro' in v for v in d.values())} con prerequisiti non leggibili")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
