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

Only markdown files that already have at least one committed SVG are
re-rendered, so map masters that were intentionally left un-rendered (KO rows
of `MAPPE-CENSIMENTO.md`) never trip a false "missing" error.

Usage:  python3 scripts/validate_maps.py [--repo-root PATH]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.dom import minidom

# Import the renderer as a library (no side effects on import — its CLI lives
# under `if __name__ == "__main__"`).
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_map_svg as R  # noqa: E402

SVG_NAME_RE = re.compile(r"^(?P<stem>.+)_map\d{2}_.+\.svg$")


def render_master(md: Path) -> dict[str, str]:
    """Return {expected_svg_filename: svg_text} for every map in a master."""
    maps = R.extract_maps(md.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for i, g in enumerate(maps, 1):
        name = f"{md.stem}_map{i:02d}_{R.slugify(g['title'])}.svg"
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


def validate(repo_root: Path) -> int:
    errors: list[str] = []
    total_svg = 0
    total_masters = 0

    rendered_dirs = sorted({p.parent for p in repo_root.glob("**/rendered/*.svg")})
    if not rendered_dirs:
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
    args = ap.parse_args()
    return validate(Path(args.repo_root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
