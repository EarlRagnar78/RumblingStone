"""La griglia campione del corredo V2-bis (#226), recuperata il 2026-10-09.

Due usi: il renderer disegna i venti simboli nuovi nei due temi senza perderne
uno, e il collaudo trova sempre gli stessi difetti messi apposta (tre scale
senza gemella). Se un domani il collaudo ne trova di più o di meno, il cambio
si vede qui.
"""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402

PROVA = SCRIPTS / "tests" / "fixtures" / "prova-simboli.md"
NUOVI = "🔒❔🗄📚⚒🥅🧪🪟🧰🛐🔼⛓🔽🟤🪵🔻💧🫧⛲🏗"


class TestRender(unittest.TestCase):
    def test_i_venti_simboli_nuovi_sono_nella_griglia_e_nella_legenda(self):
        g = R.extract_maps(PROVA.read_text(encoding="utf-8"))[0]
        testo = PROVA.read_text(encoding="utf-8")
        legenda = json.loads((SCRIPTS / "legend.json").read_text(encoding="utf-8"))
        chiavi = json.dumps(legenda, ensure_ascii=False)
        for s in NUOVI:
            self.assertIn(s, testo, s)
            self.assertIn(s, chiavi, f"{s} fuori dalla legenda")
        self.assertEqual(len(g["rows"]), 8)

    def test_si_rende_nei_due_temi(self):
        g = R.extract_maps(PROVA.read_text(encoding="utf-8"))[0]
        for tema in ("pergamena", "texture"):
            svg = R.render_svg(g, PROVA.name, tema)
            self.assertTrue(svg.lstrip().startswith("<svg"), tema)


try:
    import collaudo_mappe as C
    C._dipendenze()
    COLLAUDO = True
except (ImportError, SystemExit):  # pragma: no cover
    COLLAUDO = False


@unittest.skipUnless(COLLAUDO, "il collaudo vuole tcod, scipy e numpy")
class TestCollaudo(unittest.TestCase):
    def test_trova_le_tre_scale_senza_gemella_e_niente_altro_di_grave(self):
        out = Path(tempfile.mkdtemp()) / "r.json"
        with redirect_stdout(io.StringIO()):
            C.main([str(PROVA), "--json", str(out)])
        rilievi = json.loads(out.read_text(encoding="utf-8"))["mappe"][0]["rilievi"]
        errori = sorted((r["codice"], r["cella"]) for r in rilievi if r["classe"] == "E")
        self.assertEqual(errori, [("posa/fra-livelli", "B05"), ("posa/fra-livelli", "K05"),
                                  ("posa/fra-livelli", "K06")])

if __name__ == "__main__":
    unittest.main()
