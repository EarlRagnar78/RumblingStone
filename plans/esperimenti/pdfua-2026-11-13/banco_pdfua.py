"""banco_pdfua.py — i booklet contro PDF/UA-1 (ISO 14289-1) con veraPDF (ADR-0129).

Fuori dalla CI: serve Java e il jar di veraPDF (GPLv3+/MPL-2.0), che non entra
nel repo. Ricetta, la stessa di ADR-0032:

    mkdir -p /tmp/vp && cd /tmp/vp
    curl -O https://repo.maven.apache.org/maven2/org/verapdf/apps/greenfield-apps/1.28.2/greenfield-apps-1.28.2.jar
    cp <repo>/plans/esperimenti/pdfua-2026-11-13/Avvio.java . && javac -cp greenfield-apps-1.28.2.jar Avvio.java

(`repo1.maven.org` può rispondere 429 alle macchine condivise: lo specchio
`repo.maven.apache.org` è lo stesso archivio.) Il fat jar non registra da sé il
proprio provider, e `Avvio` lo fa prima di chiamare la CLI.

Uso, dalla radice del repo, dopo `export_booklet_typst.py MANIFEST --all --keep-typ`
su ogni booklet:

    python3 plans/esperimenti/pdfua-2026-11-13/banco_pdfua.py --vp /tmp/vp [--ua] > esito.json

Compila ogni `.typ` tenuto (con `--ua` chiede PDF/UA-1 a typst, come fa ora
l'esportatore) e passa il PDF a veraPDF col profilo `ua1`. Stampa per booklet
se compila, se è conforme e i controlli falliti per regola.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import typst  # noqa: E402

import typst_motore as tm  # noqa: E402
from export_booklet_typst import FONTS, PACCHETTI  # noqa: E402


def verapdf(vp: Path, pdf: Path) -> dict:
    jar = next(vp.glob("greenfield-apps-*.jar"))
    r = subprocess.run(["java", "-cp", f"{jar}:{vp}", "Avvio", "--flavour", "ua1", "--format", "json", str(pdf)],
                       capture_output=True, text=True)
    esito = json.loads(r.stdout)["report"]["jobs"][0]["validationResult"][0]
    det = esito["details"]
    return {"conforme": esito["compliant"], "regole_fallite": det["failedRules"],
            "controlli_falliti": det["failedChecks"],
            "per_regola": {f'{x["clause"]}-{x["testNumber"]}': x["failedChecks"] for x in det["ruleSummaries"]}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vp", type=Path, required=True, help="cartella con il jar di veraPDF e Avvio.class")
    ap.add_argument("--ua", action="store_true", help="chiede PDF/UA-1 a typst")
    a = ap.parse_args()
    opz = tm._opzioni_py(ROOT, FONTS, PACCHETTI, False, None)
    if a.ua:
        opz["pdf_standards"] = ["ua-1"]
    out = {}
    manifest = sorted(p for p in ROOT.rglob("*.manifest.json") if "scripts" not in p.parts)
    with tempfile.TemporaryDirectory() as d:
        for m in manifest:
            typ = m.with_name(m.name.replace(".manifest.json", ".typ"))
            if not typ.exists():
                continue
            pdf = Path(d) / (typ.stem + ".pdf")
            try:
                typst.compile(str(typ.relative_to(ROOT)), output=str(pdf), **opz)
            except typst.TypstError as e:
                out[typ.stem] = {"compila": False, "errore": str(e)[:300]}
                continue
            out[typ.stem] = {"compila": True, **verapdf(a.vp, pdf)}
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
