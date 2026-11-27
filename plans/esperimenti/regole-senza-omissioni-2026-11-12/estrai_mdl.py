#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/mdl.toml`: il modificatore di livello delle razze che l'SRD
presenta come personaggi di 1° livello, senza dadi vita razziali (ADR-0126, lotto 5).

Uso: python3 estrai_mdl.py [<cartella srd-v3.5-md>]            # scrive il file
     python3 estrai_mdl.py --check [<cartella srd-v3.5-md>]    # 1 se il file non è aggiornato

Dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL), solo nomi e numeri: ogni blocco di
statistiche di monsters/*.md intitolato «X, 1st-Level Warrior», con la sua riga «Level
Adjustment» e il suo tipo. Le creature con dadi vita razziali hanno il loro `mdl` in
`creature_base.toml`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "dnd35" / "dati" / "mdl.toml"
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"
#: come una scheda italiana o inglese chiama la razza (non viene dall'SRD)
NOMI = {
    "aasimar": "aasimar", "drow": "drow", "duergar": "duergar", "goblin": "goblin", "hobgoblin": "hobgoblin",
    "kobold": "kobold[oi]?|cobold[oi]", "merfolk": "merfolk|marinid[ei]", "orc": "(?<!half-)(?<!mezz)orc(?:[oa]|hi|he|s)?",
    "svirfneblin": "svirfneblin|gnom[oi] delle profondità|deep gnomes?", "tiefling": "tiefling",
}


def _celle(riga: str) -> "list[str]":
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", riga, re.S)]


def razze(base: Path) -> "dict[str, dict]":
    out = {}
    for f in sorted((base / "monsters").glob("*.md")):
        for tab in re.findall(r"<table[^>]*>(.*?)</table>", f.read_text(encoding="utf-8"), re.S):
            righe = [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", tab, re.S)]
            mdl = next((r for r in righe if r and r[0].startswith("Level Adjustment")), None)
            if mdl is None or len(righe) < 2:
                continue
            for i, nome in enumerate(righe[0][1:], 1):
                m = re.fullmatch(r"(.+?), 1st-Level Warrior", nome)
                n = re.fullmatch(r"\+(\d+)", mdl[i]) if m and i < len(mdl) else None
                tipo = re.match(r"\w+ ([\w ]+?)\s*(?:\(|$)", righe[1][i]) if n and i < len(righe[1]) else None
                if tipo:
                    out[m.group(1).lower()] = {"mdl": int(n.group(1)), "tipo": tipo.group(1).lower(), "fonte": f.name}
    return dict(sorted(out.items()))


def testo(base: Path) -> str:
    r = razze(base)
    mancano = sorted(set(r) - set(NOMI) - {"dwarf", "elf", "gnome", "halfling"})
    if mancano:
        raise SystemExit(f"estrai_mdl: razze senza un nome in NOMI: {mancano}")
    righe = [
        "# sistemi/dnd35/dati/mdl.toml — il modificatore di livello delle razze senza dadi vita razziali",
        "# (ADR-0126, lotto 5)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_mdl.py",
        "# dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL). Non si corregge a mano.",
        "",
        "[mdl.razze]",
        "# SRD, blocchi «X, 1st-Level Warrior»: riga «Level Adjustment» e tipo della creatura",
    ]
    righe += [f'"{k}" = {{ mdl = {v["mdl"]}, tipo = "{v["tipo"]}", fonte = "{v["fonte"]}" }}'
              for k, v in r.items() if k in NOMI]
    righe += ["", "[mdl.nomi]", "# come una scheda scrive la razza (espressioni regolari; non vengono dall'SRD)"]
    righe += [f"\"{k}\" = '''{v}'''" for k, v in NOMI.items() if k in r]
    return "\n".join(righe) + "\n"


def main(argv: "list[str]") -> int:
    check = "--check" in argv
    resto = [a for a in argv if a != "--check"]
    base = Path(resto[0]) if resto else CACHE
    if not base.is_dir():
        print(f"estrai_mdl: manca {base}", file=sys.stderr)
        return 2
    nuovo = testo(base)
    if check:
        if not DEST.is_file() or DEST.read_text(encoding="utf-8") != nuovo:
            print(f"estrai_mdl: {DEST.relative_to(ROOT)} non è aggiornato", file=sys.stderr)
            return 1
        return 0
    DEST.write_text(nuovo, encoding="utf-8")
    print(f"estrai_mdl: scritto {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
