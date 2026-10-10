#!/usr/bin/env python3
"""
build_emoji_noto.py — il ripiego per le emoji locali delle mappe (ADR-0085).

Gli 86 simboli della legenda universale sono disegnati in casa. Una mappa che
dichiara un simbolo suo nella riga `LEGENDA` (`💠 base corrosa del pilastro`)
lo vedeva disegnato con l'emoji del font di sistema: 177 celle in 7 SVG il
2026-10-08, ognuna con una faccia diversa su ogni macchina. Questo script
prende dal progetto Noto Emoji (immagini Apache-2.0, `2D/svg/LICENSE`) l'SVG di
ogni emoji locale che il corpus usa, rinomina gli id interni perche' due emoji
nella stessa mappa non si pestino i gradienti, e lo scrive in
`scripts/emoji-noto/`. Il renderer lo incorpora; un'emoji senza file resta al
font di sistema, come prima.

    python3 scripts/build_emoji_noto.py           # scarica quelle che mancano
    python3 scripts/build_emoji_noto.py --check   # esce 1 se un'emoji locale non ha il suo file

Solo libreria standard. Lo scaricamento chiede la rete (raw.githubusercontent.com),
il controllo no. Il commit di Noto e' fissato: lo stesso file ogni volta.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent
REPO = RADICE.parent
sys.path.insert(0, str(RADICE))
import render_map_svg as R  # noqa: E402

CARTELLA = RADICE / "emoji-noto"
INDICE = CARTELLA / "indice.json"
COMMIT = "e20cbc2"  # googlefonts/noto-emoji, 2026-09-24
URL = "https://raw.githubusercontent.com/googlefonts/noto-emoji/{commit}/2D/svg/emoji_u{codice}.svg"
ESCLUSI = ("/.git/", "/node_modules/", "/.claude/", ".hb.md")


def codice(emoji: str) -> str:
    return "_".join(f"{ord(c):x}" for c in emoji if ord(c) != 0xFE0F)


def file_di(emoji: str) -> Path:
    return CARTELLA / f"emoji_u{codice(emoji)}.svg"


def locali_del_corpus() -> dict[str, int]:
    """Le emoji delle griglie che la legenda universale non conosce, con quante celle."""
    conto: dict[str, int] = {}
    for p in sorted(REPO.rglob("*.md")):
        if any(s in str(p) for s in ESCLUSI):
            continue
        try:
            testo = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "```" not in testo:
            continue
        for g in R.extract_maps(testo):
            for riga in g["rows"].values():
                for c in riga:
                    e = (c or "").replace("️", "")
                    if e and e not in R.SYMBOLS and any(ord(ch) > 0x2000 for ch in e):
                        conto[e] = conto.get(e, 0) + 1
    return conto


def prepara(svg: str, emoji: str) -> str:
    """Prefissa gli id interni con il codice dell'emoji (modifica dichiarata in CREDITS.md)."""
    pre = f"nt{codice(emoji)}_"
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = re.sub(rf'\bid="{re.escape(i)}"', f'id="{pre}{i}"', svg)
        svg = re.sub(rf'url\(#{re.escape(i)}\)', f"url(#{pre}{i})", svg)
        svg = re.sub(rf'href="#{re.escape(i)}"', f'href="#{pre}{i}"', svg)
    return svg


def scarica(locali: dict[str, int]) -> int:
    CARTELLA.mkdir(exist_ok=True)
    nuove = 0
    for e in sorted(locali):
        dest = file_di(e)
        if dest.exists():
            continue
        try:
            with urllib.request.urlopen(URL.format(commit=COMMIT, codice=codice(e)), timeout=30) as r:
                svg = r.read().decode("utf-8")
        except OSError as err:
            print(f"✗ {e} (emoji_u{codice(e)}.svg): {err}", file=sys.stderr)
            continue
        dest.write_text(prepara(svg, e), encoding="utf-8")
        nuove += 1
        print(f"✓ {e} → {dest.relative_to(REPO)}")
    indice = {e: {"file": file_di(e).name, "celle": n} for e, n in sorted(locali.items())
              if file_di(e).exists()}
    INDICE.write_text(json.dumps({"noto_commit": COMMIT, "emoji": indice}, ensure_ascii=False,
                                 indent=1) + "\n", encoding="utf-8")
    print(f"build_emoji_noto: {nuove} nuove, {len(indice)} in tutto")
    return 0


def controlla(locali: dict[str, int]) -> int:
    mancanti = [e for e in sorted(locali) if not file_di(e).exists()]
    for e in mancanti:
        print(f"✗ l'emoji locale {e} ({locali[e]} celle) non ha il suo SVG: "
              "python3 scripts/build_emoji_noto.py")
    if not mancanti:
        print(f"✓ build_emoji_noto: {len(locali)} emoji locali, tutte con il loro SVG Noto")
    return 1 if mancanti else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--check", action="store_true", help="verifica senza scaricare")
    args = ap.parse_args(argv)
    locali = locali_del_corpus()
    return controlla(locali) if args.check else scarica(locali)


if __name__ == "__main__":
    sys.exit(main())
