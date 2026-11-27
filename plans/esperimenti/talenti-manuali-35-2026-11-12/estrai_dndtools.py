#!/usr/bin/env python3
"""estrai_dndtools.py — prerequisiti dei talenti 3.5 dalle tabelle di srd.dndtools.org.

Ogni pagina di manuale (`srd/meta/books/<edizione>/<Manuale>.html`) ha le
tabelle riassuntive dei talenti: Feat | Prerequisite | Benefit. Si leggono
**nome e prerequisito** (la colonna del beneficio si scarta) e il prerequisito
passa dallo stesso lettore dell'SRD (`estrai_talenti.prerequisiti`).

Uso (lo chiama estrai_pcgen.py):
  python3 estrai_dndtools.py scarica CARTELLA     # scarica le pagine dei manuali
  python3 estrai_dndtools.py conta CARTELLA       # quanti talenti per manuale
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

BASE = "https://srd.dndtools.org/srd/meta/"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "plans" / "esperimenti" / "regole-complete-2026-11-10"))

#: come le tabelle chiamano capacità che `[capacita]` di talenti.toml sa giudicare
ALIAS = [(r"\s+with (?:the |a )?(?:selected |chosen |same )?weapon\b", ""),
         (r"\b(?:ability to rage|rage or frenzy ability|rage ability|ability to rage or frenzy)\b", "rage"),
         (r"\bability to turn or rebuke undead\b|\bability to turn undead\b|\bability to rebuke undead\b"
          r"|\bturn or rebuke undead\b", "turn or rebuke creatures"),
         (r"\bwild shape ability\b|\bability to wild shape\b", "wild shape"),
         (r"\bability to cast arcane spells\b", "cast arcane spells"),
         (r"\bability to cast divine spells\b", "cast divine spells"),
         (r"\b(arcane|divine) caster level (\d+)", r"cast \1 spells, caster level \2"),
         (r"\b(barbarian|bard|cleric|druid|fighter|monk|paladin|ranger|rogue|sorcerer|wizard) (\d+(?:st|nd|rd|th))\b",
          r"\1 level \2")]


def _pulito(cella: str) -> str:
    cella = re.sub(r"<sup>.*?</sup>", "", cella, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "", cella))
    return re.sub(r"\s+", " ", t.replace("�", "'").replace("’", "'")).strip()


def tabelle(testo: str) -> "list[tuple[str, str]]":
    """(nome, prerequisito) di ogni riga delle tabelle con la colonna «Prerequisite»."""
    out = []
    for tab in re.findall(r"<table[^>]*>(?:(?!<table).)*?</table>", testo, flags=re.S | re.I):
        righe = re.findall(r"<tr[^>]*>(.*?)</tr>", tab, flags=re.S | re.I)
        if not righe:
            continue
        testa = [_pulito(c).lower() for c in re.findall(r"<th[^>]*>(.*?)</th>", righe[0], flags=re.S | re.I)]
        col = next((i for i, c in enumerate(testa) if c.startswith("prerequisite")), None)
        if col is None or not testa or "feat" not in testa[0]:
            continue
        for r in righe[1:]:
            celle = [_pulito(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", r, flags=re.S | re.I)]
            # le righe rientrate (talenti figli) cominciano con un segno; i manuali epici sono in maiuscolo
            nome = re.sub(r"^[^A-Za-z]+", "", celle[0]) if celle else ""
            if nome.isupper():
                nome = re.sub(r"\b(Of|The|And|To|In|A)\b", lambda m: m.group(1).lower(), nome.title())
            if len(celle) > col and nome:
                out.append((nome, celle[col]))
    return out


def manuale(file: Path, testo: str) -> str:
    m = re.search(r"<title>(?:SRD\s*-\s*)?(.*?)</title>", testo, flags=re.S | re.I)
    titolo = _pulito(m.group(1)) if m else ""
    if titolo and titolo != "Book":
        return titolo
    # «CityofSplendorsWaterdeep» → «City of Splendors Waterdeep»
    nome = re.sub(r"(?<=[a-z])(of|the|and|to)(?=[A-Z])", r" \1 ", file.stem.split("__")[-1])
    return re.sub(r"\s+", " ", re.sub(r"(?<=[a-z])(?=[A-Z0-9])", " ", nome)).strip()


def leggi(cartella: Path, noti: "dict[str, str]") -> "dict[str, dict]":
    """Nome → {manuale, prerequisiti…} per ogni talento delle tabelle. `noti` =
    {chiave: nome} dei talenti già conosciuti (SRD): servono a riconoscere i
    talenti dentro i prerequisiti; vi si aggiungono i nomi delle tabelle stesse."""
    import estrai_talenti as E
    grezzi: list[tuple[str, str, str]] = []
    for f in sorted(cartella.glob("*.html")):
        testo = f.read_text(encoding="utf-8", errors="replace")
        libro = manuale(f, testo)
        grezzi += [(n, p, libro) for n, p in tabelle(testo)]
    noti = dict(noti)
    for n, _, _ in grezzi:
        noti.setdefault(E._k(n), n)
    out: dict[str, dict] = {}
    for nome, pre, libro in grezzi:
        if nome in out:
            continue
        t = pre if pre not in ("-", "—", "–", "'", "?") else ""
        for da, a in ALIAS:
            t = re.sub(da, a, t, flags=re.I)
        p = {k: v for k, v in E.prerequisiti(t, noti).items() if v}
        p["talenti"] = [x for x in p.get("talenti", []) if x != nome]
        out[nome] = {"manuale": libro, **{k: v for k, v in p.items() if v}}
    return out


def scarica(cartella: Path) -> int:
    cartella.mkdir(parents=True, exist_ok=True)
    indice = subprocess.run(["curl", "-sS", "-m", "40", BASE + "bookList.html"], capture_output=True,
                            text=True, check=True).stdout
    pagine = sorted(set(re.findall(r'href="(books/[^"]+\.html)"', indice)))
    for x in pagine:
        dest = cartella / x.replace("/", "__")
        if not dest.is_file() or dest.stat().st_size < 500:
            subprocess.run(["curl", "-sS", "-m", "40", "-o", str(dest), BASE + x], check=False)
    print(f"{len(pagine)} pagine in {cartella}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "scarica":
        sys.exit(scarica(Path(sys.argv[2])))
    if len(sys.argv) == 3 and sys.argv[1] == "conta":
        import collections
        d = leggi(Path(sys.argv[2]), {})
        c = collections.Counter(v["manuale"] for v in d.values())
        print(len(d), "talenti;", sum("altro" in v for v in d.values()), "con prerequisiti non leggibili")
        for k, n in c.most_common():
            print(f"{n:4d}  {k}")
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
