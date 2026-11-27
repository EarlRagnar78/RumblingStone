#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/movimento.toml`: la velocità a terra che le regole danno (ADR-0126, lotto 7).

Uso: python3 estrai_movimento.py [<cartella srd-v3.5-md>]            # scrive il file
     python3 estrai_movimento.py --check [<cartella srd-v3.5-md>]    # 1 se il file non è aggiornato

Dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL), solo nomi e numeri:
  razze     «Human base land speed is 30 feet», e chi non rallenta in armatura;
            poi nove razze senza dadi vita razziali dal capitolo dei mostri
  armature  la categoria (leggera, media, pesante) di ogni armatura di «Armor and
            Shields», con bonus e Des massima per riconoscerla
  ridotta   «Base Speed / Reduced Speed» di «Carrying Capacity»
  classi    «Fast Movement» del barbaro (+10, non in armatura pesante) e la
            colonna «Unarmored Speed Bonus» del monaco
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "dnd35" / "dati" / "movimento.toml"
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"
RAZZE = {"Human": "human", "Dwarf": "dwarf", "Elf": "elf", "Gnome": "gnome", "Half-elf": "half-elf",
         "Half-orc": "half-orc", "Halfling": "halfling"}
MOSTRI = {"aasimar": ("monsters-o-r.md", "aasimar"), "goblin": ("monsters-g.md", "goblin"),
          "hobgoblin": ("monsters-h-i.md", "hobgoblin"), "kobold": ("monsters-k-l.md", "kobold"),
          "orc": ("monsters-o-r.md", "orc"), "tiefling": ("monsters-o-r.md", "tiefling")}
SOTTORAZZE = {"drow": "elf", "duergar": "dwarf", "svirfneblin": "gnome"}
CATEGORIE = {"Light armor": "leggera", "Medium armor": "media", "Heavy armor": "pesante"}


def _celle(riga: str) -> "list[str]":
    return [re.sub(r"<[^>]+>", "", re.sub(r"<sup>.*?</sup>", "", c)).strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", riga, re.S)]


def razze(base: Path) -> "tuple[dict[str, int], list[str]]":
    t = (base / "basic-rules-and-legal" / "races.md").read_text(encoding="utf-8")
    velocita, non_rallenta = {}, []
    for nome, piedi, resto in re.findall(r"^- ([A-Z][a-z-]+) base land speed is (\d+) feet\.(.*)$", t, re.M):
        if nome in RAZZE:
            velocita[RAZZE[nome]] = int(piedi)
            if re.search(r"even when wearing medium or heavy armor", resto):
                non_rallenta.append(RAZZE[nome])
    # le razze senza dadi vita razziali (chiavi di mdl.toml): «—A hobgoblin’s base land speed is 30 feet»
    # nel capitolo dei mostri; una sottorazza tiene la velocità della razza da cui viene
    for razza, (file, nome) in MOSTRI.items():
        m = re.search(rf"^— ?An? {nome} ?’s base land speed is (\d+) feet\.",
                      (base / "monsters" / file).read_text(encoding="utf-8"), re.M)
        velocita[razza] = int(m.group(1))
    for razza, madre in SOTTORAZZE.items():
        velocita[razza] = velocita[madre]
        if madre in non_rallenta:
            non_rallenta.append(razza)
    return velocita, non_rallenta


def armature(base: Path) -> "dict[str, dict]":
    t = (base / "basic-rules-and-legal" / "equipment.md").read_text(encoding="utf-8")
    tabella = re.search(r"<table[^>]*><caption>Table: Armor and Shields</caption>.*?</table>", t, re.S).group(0)
    out, categoria = {}, None
    for riga in re.findall(r"<tr>(.*?)</tr>", tabella, re.S):
        c = _celle(riga)
        if not c:
            continue
        if c[0] in CATEGORIE:
            categoria = CATEGORIE[c[0]]
        elif c[0] in ("Shields", "Extras"):
            categoria = None
        elif categoria and len(c) > 7 and re.fullmatch(r"\+\d+", c[2]):
            out[c[0].lower()] = {"ca": int(c[2]), "des_max": int(c[3].replace("+", "")), "categoria": categoria}
    return out


def ridotta(base: Path) -> "dict[int, int]":
    t = (base / "basic-rules-and-legal" / "carrying-movement-and-exploration.md").read_text(encoding="utf-8")
    tabella = next(x for x in re.findall(r"<table.*?</table>", t, re.S) if "Reduced Speed" in x)
    out = {}
    for riga in re.findall(r"<tr>(.*?)</tr>", tabella, re.S):
        n = [int(m.group(1)) for c in _celle(riga) if (m := re.fullmatch(r"(\d+) ft\.", c))]
        out.update(zip(n[::2], n[1::2]))
    return dict(sorted(out.items()))


def classi(base: Path) -> "tuple[int, bool, list[int]]":
    """(bonus del barbaro, il barbaro lo perde in armatura pesante, bonus del monaco per livello da 1 a 20)."""
    t = (base / "basic-rules-and-legal" / "character-classes-i.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Fast Movement \(Ex\):\*\* A barbarian’s land speed is faster than the norm for his race by "
                  r"\+(\d+) feet\. This benefit applies only when he is wearing (no armor, light armor, or medium armor)", t)
    tabella = re.search(r"<table[^>]*><caption>Table: The Monk</caption>.*?</table>", t, re.S).group(0)
    righe = [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", tabella, re.S)]
    colonna = righe[0].index("Unarmored Speed Bonus")
    monaco = [int(re.match(r"\+(\d+)", r[colonna]).group(1)) for r in righe[1:] if re.match(r"\d+", r[0])]
    return int(m.group(1)), "heavy" not in m.group(2), monaco


def genera(base: Path) -> str:
    v, non = razze(base)
    arm, rid = armature(base), ridotta(base)
    barbaro, non_pesante, monaco = classi(base)
    assert len(v) == 16 and len(arm) == 12 and len(monaco) == 20, (v, len(arm), len(monaco))
    q = lambda s: '"' + s + '"'  # noqa: E731
    return "\n".join([
        "# sistemi/dnd35/dati/movimento.toml — la velocità a terra 3.5 (ADR-0126, lotto 7)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_movimento.py",
        "# dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL). Non si corregge a mano. Velocità in piedi.",
        "",
        "[movimento]",
        "# SRD, «Armor and Shields»: l'armatura media o pesante riduce la velocità a quella di",
        "# `[movimento.ridotta]`; `non_rallenta`: le razze che in armatura non rallentano.",
        "# SRD, «Special Materials»: un'armatura di mithral conta una categoria più leggera.",
        "non_rallenta = [" + ", ".join(q(x) for x in non) + "]",
        "rallentano = [\"media\", \"pesante\"]",
        "piedi_per_metro_e_mezzo = 5",
        "",
        "[movimento.razze]",
        *[f"{q(n)} = {p}" for n, p in v.items()],
        "",
        "[movimento.armature]",
        *[f"{q(n)} = {{ ca = {a['ca']}, des_max = {a['des_max']}, categoria = {q(a['categoria'])} }}"
          for n, a in arm.items()],
        "",
        "[movimento.ridotta]",
        *[f"{q(str(k))} = {r}" for k, r in rid.items()],
        "",
        "[movimento.classi]",
        "# barbaro: «Fast Movement», non in armatura pesante; monaco: «Unarmored Speed Bonus» per",
        "# livello (dal 1° al 20°), solo senza armatura e senza scudo",
        f"barbarian = {{ piu = {barbaro}, non_in = [{q('pesante') if non_pesante else ''}] }}",
        "monk = { per_livello = [" + ", ".join(map(str, monaco)) + "] }",
        "",
    ])


def main(argv: "list[str]") -> int:
    check = "--check" in argv
    resto = [a for a in argv if a != "--check"]
    testo = genera(Path(resto[0]) if resto else CACHE)
    if check:
        if not DEST.exists() or DEST.read_text(encoding="utf-8") != testo:
            print("✗ movimento.toml non è aggiornato: rilanciare estrai_movimento.py", file=sys.stderr)
            return 1
        print("✓ movimento.toml aggiornato")
        return 0
    DEST.write_text(testo, encoding="utf-8")
    print(f"scritto {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
