#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/difese.toml`: la resistenza agli incantesimi e la riduzione del danno
che razza e classe danno (ADR-0126, lotto 7).

Uso: python3 estrai_difese.py [<cartella srd-v3.5-md>]            # scrive il file
     python3 estrai_difese.py --check [<cartella srd-v3.5-md>]    # 1 se il file non è aggiornato

Dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL), solo nomi e numeri:
  ri.razze   ogni «spell resistance equal to N + class levels» dei mostri, col nome
             della razza preso dal titolo che la precede
  ri.classi  «Diamond Soul» del monaco: livello + 10, dal livello della tabella
  rd.classi  «Damage reduction N/—» della tabella del barbaro, per livello
  immunita.tipi  le righe «—Immunity to …» (e «Mindless … immunity to all
             mind-affecting effects») di ogni «X Type» dei tipi di creatura
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "dnd35" / "dati" / "difese.toml"
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"
#: i nomi con cui una scheda italiana o inglese chiama la razza (non vengono dall'SRD)
NOMI = {"drow": ["drow"], "svirfneblin": ["svirfneblin", "gnom[oi] delle profondità", "deep gnomes?"],
        "rakshasa": ["rakshasa"], "hound archon": ["hound archons?", "arcont[ei] segugi[oi]?"],
        "azer": ["azer"], "pixie": ["pixie"]}
#: ogni immunità dei tipi: come la scrive l'SRD e come la scrive una scheda (non viene dall'SRD)
IMMUNITA = {
    "influenza mentale": (r"mind-affecting", r"mental|mind-affecting|\bmente\b"),
    "veleno": (r"poison", r"velen|poison"),
    "sonno": (r"sleep", r"sonno|sleep"),
    "paralisi": (r"paralysis", r"paralisi|paraly"),
    "stordimento": (r"stunning", r"stordi|stun"),
    "malattia": (r"disease", r"malatti|disease"),
    "effetti di morte": (r"death effects", r"morte|death"),
    "necromanzia": (r"necromancy", r"necromanzi|necromanc"),
    "metamorfosi": (r"polymorph", r"metamorf|polimorf|polymorph"),
}
TIPI_IT = {"construct": "costrutt[oi]", "dragon": "dragh?[oi]", "elemental": "elemental[ei]", "ooze": "melm[ae]",
           "plant": "vegetal[ei]", "undead": "non[ -]mort[oi]", "vermin": "parassit[ai]"}


def _celle(riga: str) -> "list[str]":
    return [re.sub(r"<[^>]+>", " ", c).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", riga, re.S)]


def ri_razze(base: Path) -> "dict[str, int]":
    out = {}
    for f in sorted((base / "monsters").glob("*.md")):
        titolo = ""
        for riga in f.read_text(encoding="utf-8").split("\n"):
            if riga.startswith("#"):
                titolo = riga.lstrip("# ").strip()
            for n in re.findall(r"(?i)spell resistance equal to (\d+) \+ class levels", riga):
                nome = re.sub(r"s? as Characters$", "", titolo).lower()
                out[nome] = int(n)
    return dict(sorted(out.items()))


def _tabella(base: Path, didascalia: str) -> "list[list[str]]":
    t = (base / "basic-rules-and-legal" / "character-classes-i.md").read_text(encoding="utf-8")
    tab = re.search(rf"<table[^>]*><caption>{re.escape(didascalia)}</caption>.*?</table>", t, re.S).group(0)
    return [_celle(r) for r in re.findall(r"<tr>(.*?)</tr>", tab, re.S)]


def monaco(base: Path) -> "tuple[int, int]":
    """(livello da cui, numero da sommare al livello)."""
    t = (base / "basic-rules-and-legal" / "character-classes-i.md").read_text(encoding="utf-8")
    piu = int(re.search(r"a monk gains spell resistance equal to her current monk level \+ (\d+)", t).group(1))
    dal = next(int(re.match(r"\d+", r[0]).group(0)) for r in _tabella(base, "Table: The Monk")
               if r and re.match(r"\d+", r[0]) and any("diamond soul" in c.lower() for c in r))
    return dal, piu


def barbaro(base: Path) -> "list[int]":
    out, ora = [], 0
    for r in _tabella(base, "Table: The Barbarian"):
        if not r or not re.match(r"\d+", r[0]):
            continue
        m = re.search(r"Damage reduction (\d+)/—", " ".join(r))
        ora = int(m.group(1)) if m else ora
        out.append(ora)
    return out


def immunita(base: Path) -> "dict[str, list[str]]":
    t = (base / "basic-rules-and-legal" / "types-subtypes-and-special-abilities.md").read_text(encoding="utf-8")
    out, tipo = {}, None
    for riga in t.split("\n"):
        m = re.match(r"\*\*([A-Z][A-Za-z ]+) (Type|Subtype):\*\*", riga)
        if m:
            tipo = m.group(1).lower() if m.group(2) == "Type" else None
        elif tipo and re.match(r"—(?:Immunity to|Mindless:)", riga):
            for chiave, (srd, _) in IMMUNITA.items():
                if re.search(srd, riga) and chiave not in out.setdefault(tipo, []):
                    out[tipo].append(chiave)
    return out


def genera(base: Path) -> str:
    razze, (dal, piu), rd = ri_razze(base), monaco(base), barbaro(base)
    imm = immunita(base)
    assert set(razze) == set(NOMI) and len(rd) == 20 and rd[-1] == 5, (razze, rd)
    assert set(imm) == set(TIPI_IT), imm
    q = lambda s: '"' + s + '"'  # noqa: E731
    return "\n".join([
        "# sistemi/dnd35/dati/difese.toml — resistenza agli incantesimi e riduzione del danno 3.5",
        "# che razza e classe danno (ADR-0126, lotto 7)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_difese.py",
        "# dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL). Non si corregge a mano.",
        "",
        "[difese.ri.razze]",
        "# SRD, mostri: «spell resistance equal to N + class levels»",
        *[f"{q(n)} = {v}" for n, v in razze.items()],
        "",
        "[difese.ri.nomi]",
        "# come una scheda chiama la razza (espressioni regolari; non vengono dall'SRD)",
        *[f"{q(n)} = [{', '.join(q(x) for x in NOMI[n])}]" for n in razze],
        "",
        "[difese.ri.classi]",
        "# monaco, «Diamond Soul»: livello di monaco + `piu`, dal livello `dal`",
        f"monk = {{ dal = {dal}, piu = {piu} }}",
        "",
        "[difese.rd.classi]",
        "# barbaro, «Damage Reduction»: N/— per livello (dal 1° al 20°)",
        "barbarian = { per_livello = [" + ", ".join(map(str, rd)) + "] }",
        "",
        "[difese.immunita.tipi]",
        "# SRD, tipi di creatura: le righe «Immunity to …» dei tratti di ogni tipo",
        *[f"{q(n)} = [{', '.join(q(x) for x in v)}]" for n, v in sorted(imm.items())],
        "",
        "[difese.immunita.nomi]",
        "# come una scheda chiama il tipo in italiano, per la formula «tratti dei …» (non viene dall'SRD)",
        *[f"{q(n)} = {q(TIPI_IT[n])}" for n in sorted(imm)],
        "",
        "[difese.immunita.parole]",
        "# come una scheda scrive ogni immunità (espressioni regolari; non vengono dall'SRD)",
        *[f"{q(n)} = '{v[1]}'" for n, v in IMMUNITA.items()],
        "",
    ])


def main(argv: "list[str]") -> int:
    check = "--check" in argv
    resto = [a for a in argv if a != "--check"]
    testo = genera(Path(resto[0]) if resto else CACHE)
    if check:
        if not DEST.exists() or DEST.read_text(encoding="utf-8") != testo:
            print("✗ difese.toml non è aggiornato: rilanciare estrai_difese.py", file=sys.stderr)
            return 1
        print("✓ difese.toml aggiornato")
        return 0
    DEST.write_text(testo, encoding="utf-8")
    print(f"scritto {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
