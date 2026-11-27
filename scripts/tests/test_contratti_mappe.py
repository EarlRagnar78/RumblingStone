"""Ogni mappa di campagna ha il suo contratto JSON, e i due dicono la stessa cosa.

Regola del DM (2026-11-09): «per le mappe fai sempre il json». Il contratto
(`scripts/schemas/tactical_map.schema.json`) è la fonte da cui
`compile_map_json.py` dipinge la griglia; la griglia a emoji nel master è quella
che si legge, si rende e si stampa. Se le due divergono, una delle due mente.

Il test:

1. compila ogni contratto JSON del repo e raccoglie le griglie che produce;
2. legge ogni griglia dei file markdown (con lo stesso parser del renderer) e
   pretende che sia identica, cella per cella, a quella di un contratto;
3. pretende che nessuna intestazione dichiari dimensioni diverse da quelle
   disegnate (`render_map_svg --strict`, che fino al 2026-11-09 era solo a mano).

Fuori dal controllo: le fixture dei test, gli esperimenti, gli esempi della guida
e le cartelle `_ARCHIVIO/` (mappe deprecate e assorbite dalle REVISED, tenute per
la storia; vedi `ARCHIVIATE_SENZA_CONTRATTO` qui sotto).
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import compile_map_json as C  # noqa: E402
import render_map_svg as R  # noqa: E402

# le guide e il riferimento delle mappe mostrano griglie d'esempio (ADR-0123: docs/ in Diátaxis)
ESCLUSI = ("scripts/tests/", "plans/esperimenti/", "docs/how-to/", "docs/reference/")
# Le mappe d'archivio sono schizzi con righe di lunghezza diversa: un contratto
# dipinge sempre un rettangolo, quindi non può ridarle uguali senza toccare la
# storia. Il DM li ha lasciati fuori (card del 2026-11-09, «Fuori, sono archivio»).
ARCHIVIO = "/_ARCHIVIO/"


def _tracciati() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout
    return out.splitlines()


def _chiave(rows: dict) -> str:
    return json.dumps(rows, sort_keys=True, ensure_ascii=False)


def _contratti(files: list[str]) -> dict[str, str]:
    """{griglia: contratto} per ogni JSON del repo che è un contratto di mappa."""
    griglie: dict[str, str] = {}
    for f in files:
        if not f.endswith(".json") or "schema" in f:
            continue
        try:
            spec = json.loads((ROOT / f).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not (isinstance(spec, dict) and "map_size" in spec and "title" in spec):
            continue
        spec = C.normalize_units(spec)
        cols, rows = C.validate(spec)
        master = C.emit_master(spec, C.paint(spec, cols, rows))
        for m in R.extract_maps(master):
            griglie[_chiave(m["rows"])] = f
    return griglie


class TestContrattiMappe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = _tracciati()
        cls.griglie = _contratti(cls.files)

    def test_ogni_mappa_ha_il_suo_contratto(self):
        mancanti = []
        for f in self.files:
            if not f.endswith(".md") or f.startswith(ESCLUSI) or ARCHIVIO in f:
                continue
            testo = (ROOT / f).read_text(encoding="utf-8")
            if "```" not in testo:
                continue
            for i, m in enumerate(R.extract_maps(testo), 1):
                if _chiave(m["rows"]) not in self.griglie:
                    mancanti.append(f"{f} mappa {i}: «{m['title'][:60]}»")
        self.assertEqual(
            mancanti, [],
            "griglie senza un contratto JSON che le ridia uguali. Per una mappa "
            "nuova: scrivi il JSON e genera la griglia con compile_map_json.py; per "
            "una vecchia: import_ultraclear.py FILE --map N -o CONTRATTO.json")

    def test_le_intestazioni_dicono_le_dimensioni_disegnate(self):
        r = subprocess.run([sys.executable, "scripts/render_map_svg.py", "--strict",
                            "--tutti-i-master", "--list"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
