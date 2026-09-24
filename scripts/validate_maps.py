#!/usr/bin/env python3
"""
validate_maps.py — CI gate for the campaign's generated tactical maps.

The revised maps are authored as emoji-grids inside markdown masters; the
SVGs under every `rendered/` directory are *generated artifacts* produced by
`render_map_svg.py`. Golden Rule §0.6 of the revision plan
(`plans/PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md`) says the markdown grid
is the MASTER and the SVGs must never be hand-edited. This script enforces
that rule in CI.

Checks (hard errors, exit 1):
  1. Well-formedness — every `**/rendered/*.svg` parses as XML with an
     `<svg>` root element.
  2. Provenance — every committed SVG maps back to a markdown master
     (`<stem>.md`) sitting next to its `rendered/` dir. An SVG with no
     source master is an orphan (stale after a master was renamed/removed).
  3. In sync — re-rendering each master in memory reproduces exactly the
     committed SVG bytes. A mismatch means either the master changed without
     regenerating (`python3 scripts/render_map_svg.py <master>`) or the SVG
     was hand-edited. A master that now yields a map with no committed SVG
     is a "missing" error (regenerate + commit).
  4. Determinism — rendering a master twice yields identical bytes.

  5. No master falls out of the check (ADR-0043). Checks 2-3 only look at
     markdown files that ALREADY have a committed SVG, so deleting *every* SVG
     of a master made that master disappear from validation entirely — green,
     and nobody looking at those maps again. A master that generates maps and
     has zero committed SVGs is now an error, unless it opts out in its own
     text with:

         <!-- validate_maps: non-renderizzato — <motivo> -->

     which is how a master intentionally left un-rendered (KO rows of
     `MAPPE-CENSIMENTO.md`) declares itself instead of being guessed at.

Usage:  python3 scripts/validate_maps.py [--repo-root PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.dom import minidom

# Import the renderer as a library (no side effects on import — its CLI lives
# under `if __name__ == "__main__"`).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map_svg as R  # noqa: E402

SVG_NAME_RE = re.compile(r"^(?P<stem>.+)_map\d{2}_.+\.svg$")


# ADR-0043: come un master dichiara di NON voler essere renderizzato. Deve stare
# nel testo del master, non in una lista altrove: una lista in un altro file si
# stacca dalla realta' esattamente come si e' staccato l'elenco delle skill.
OPT_OUT_RE = re.compile(r"<!--\s*validate_maps:\s*non-renderizzato\b", re.IGNORECASE)


def check_masters_senza_svg(root: Path, rendered_dirs: list[Path]) -> list[str]:
    """Un master che genera mappe e non ha NESSUN SVG committato (ADR-0043).

    E' il punto cieco che questo controllo chiude: i controlli 2-3 guardano solo
    i markdown che hanno gia' almeno un SVG, quindi cancellandoli TUTTI il master
    usciva dalla validazione e la CI restava verde. «Verde» li' voleva dire
    «nessuno guarda piu' quelle mappe».
    """
    errors: list[str] = []
    for rdir in rendered_dirs:
        parent = rdir.parent
        con_svg = {m.group("stem") for m in
                   (SVG_NAME_RE.match(p.name) for p in rdir.glob("*.svg")) if m}
        for md in sorted(parent.glob("*.md")):
            if md.stem in con_svg:
                continue
            testo = md.read_text(encoding="utf-8")
            if OPT_OUT_RE.search(testo):
                continue
            try:
                generate = render_master(md)
            except Exception as exc:  # un master illeggibile e' gia' un errore altrove
                errors.append(f"{md.relative_to(root)}: non renderizzabile: {exc}")
                continue
            if generate:
                errors.append(
                    f"master fuori controllo: {md.relative_to(root)} genera "
                    f"{len(generate)} mappe e non ha NESSUN SVG committato — "
                    f"rigenera con render_map_svg.py, oppure dichiaralo con "
                    f"<!-- validate_maps: non-renderizzato — motivo --> nel master stesso"
                )
    return errors


def render_master(md: Path) -> dict[str, str]:
    """Return {expected_svg_filename: svg_text} for every map in a master."""
    maps = R.extract_maps(md.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for i, g in enumerate(maps, 1):
        name = f"{md.stem}_map{i:02d}_{R.nome_mappa(g['title'])}.svg"
        out[name] = R.render_svg(g, md.name)
    return out


def check_wellformed(svg_path: Path, errors: list[str]) -> None:
    try:
        dom = minidom.parseString(svg_path.read_text(encoding="utf-8"))
    except Exception as exc:  # malformed XML
        errors.append(f"XML malformato: {svg_path} — {exc}")
        return
    if dom.documentElement.tagName != "svg":
        errors.append(f"radice non <svg>: {svg_path} (<{dom.documentElement.tagName}>)")


def validate(repo_root: Path, as_json: bool = False) -> int:
    errors: list[str] = []
    total_svg = 0
    total_masters = 0

    rendered_dirs = sorted({p.parent for p in repo_root.glob("**/rendered/*.svg")})
    if not rendered_dirs:
        if as_json:
            print(json.dumps({"tool": "validate_maps", "ok": True,
                              "rendered_dirs": 0, "svg": 0, "errors": []},
                             indent=2, ensure_ascii=False))
        else:
            print("Nessuna directory rendered/ trovata — niente da validare.")
        return 0

    for rdir in rendered_dirs:
        parent = rdir.parent
        committed = {p.name: p for p in sorted(rdir.glob("*.svg"))}
        total_svg += len(committed)

        # 1. well-formedness of every committed SVG
        for name, path in committed.items():
            check_wellformed(path, errors)

        # 2-3. provenance + in-sync, grouped by source master stem
        stems = set()
        for name in committed:
            m = SVG_NAME_RE.match(name)
            if not m:
                errors.append(f"nome SVG fuori standard (atteso <stem>_mapNN_<slug>.svg): {rdir / name}")
                continue
            stems.add(m.group("stem"))

        expected: dict[str, str] = {}
        for stem in sorted(stems):
            md = parent / f"{stem}.md"
            if not md.exists():
                orphans = [n for n in committed if n.startswith(f"{stem}_map")]
                errors.append(
                    f"master mancante per {len(orphans)} SVG orfani: atteso {md} "
                    f"(es. {orphans[0]})"
                )
                continue
            total_masters += 1
            rendered = render_master(md)
            # determinism: render twice
            if render_master(md) != rendered:
                errors.append(f"rendering non deterministico: {md}")
            for fname, text in rendered.items():
                expected[fname] = text

        exp_keys = set(expected)
        com_keys = {n for n in committed if SVG_NAME_RE.match(n)
                    and SVG_NAME_RE.match(n).group("stem") in stems}
        for name in sorted(exp_keys - com_keys):
            errors.append(f"SVG mancante (master lo genera ma non è committato): {rdir / name} "
                          f"— rigenera con render_map_svg.py")
        for name in sorted(com_keys - exp_keys):
            errors.append(f"SVG orfano (nessuna mappa nel master lo genera più): {rdir / name}")
        for name in sorted(exp_keys & com_keys):
            if expected[name] != committed[name].read_text(encoding="utf-8"):
                errors.append(f"SVG NON allineato al master (rigenera o non modificare a mano): "
                              f"{rdir / name}")

    # 5. nessun master esce dal controllo perche' gli hanno tolto tutti gli SVG
    errors.extend(check_masters_senza_svg(repo_root, rendered_dirs))

    if as_json:
        print(json.dumps({
            "tool": "validate_maps", "ok": not errors,
            "rendered_dirs": len(rendered_dirs), "svg": total_svg,
            "masters": total_masters, "errors": errors,
        }, indent=2, ensure_ascii=False))
        return 1 if errors else 0

    if errors:
        print(f"❌ validate_maps: {len(errors)} errore/i\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"✓ validate_maps: {total_svg} SVG in {len(rendered_dirs)} dir rendered/, "
          f"{total_masters} master — tutti ben formati, tracciabili e allineati.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--repo-root", default=".", help="repository root (default: .)")
    ap.add_argument("--json", action="store_true",
                    help="emette il report in JSON (opt-in) invece del testo")
    args = ap.parse_args()
    return validate(Path(args.repo_root).resolve(), as_json=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
