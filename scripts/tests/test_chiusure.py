"""L'asse delle chiusure (ADR-0083): una risposta, tre lettori.

Ogni regola ha un caso che deve mordere e uno che deve tacere. Le proprieta'
(ruotare la griglia scambia gli assi, specchiarla no) girano su griglie a caso
con un seme fisso: la misura di plans/esperimenti/orientamento-e-dipendenze-2026-10
ha trovato che coglie gli stessi mutanti di hypothesis, senza la dipendenza.
"""

import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "tests"))
import collaudo_mappe as C  # noqa: E402
import export_uvtt as U  # noqa: E402
import render_map_svg as R  # noqa: E402
from dmcore import chiusure as K  # noqa: E402

from test_collaudo_mappe import _codici, _master  # noqa: E402


def _at(righe):
    g = [list(r) for r in righe]

    def at(x, y):
        if 0 <= y < len(g) and 0 <= x < len(g[y]):
            return g[y][x]
        return None
    return at


# una porta in un muro est-ovest (si passa da nord a sud) e la sua ruotata
EST_OVEST = ["⬜⬜⬜", "🏰🚪🏰", "⬜⬜⬜"]
NORD_SUD = ["⬜🏰⬜", "⬜🚪⬜", "⬜🏰⬜"]


class TestAsse(unittest.TestCase):
    def test_muro_est_ovest(self):
        self.assertEqual(K.asse(_at(EST_OVEST), 1, 1), K.EO)

    def test_muro_nord_sud(self):
        self.assertEqual(K.asse(_at(NORD_SUD), 1, 1), K.NS)

    def test_il_bordo_vale_come_muro(self):
        self.assertEqual(K.asse(_at(["🚪🏰", "⬜⬜"]), 0, 0), K.EO)

    def test_una_fila_di_porte_continua_il_muro(self):
        at = _at(["⬜⬜⬜⬜", "🏰🚪🚪🏰", "⬜⬜⬜⬜"])
        self.assertEqual((K.asse(at, 1, 1), K.asse(at, 2, 1)), (K.EO, K.EO))

    def test_le_sbarre_hanno_un_asse(self):
        self.assertEqual(K.asse(_at(["⬜🏰⬜", "⬜⛓⬜", "⬜🏰⬜"]), 1, 1), K.NS)

    def test_senza_muro_non_c_e_asse(self):
        self.assertIsNone(K.asse(_at(["⬜⬜⬜", "⬜🚪⬜", "⬜⬜⬜"]), 1, 1))

    def test_l_incrocio_e_ambiguo(self):
        """Muri in diagonale soltanto: tutti e quattro i lati si attraversano."""
        at = _at(["🏰🚪🏰", "🚪🚪🚪", "🏰🚪🏰"])
        self.assertEqual(K.asse(at, 1, 1), K.AMBIGUO)

    def test_il_passaggio_decide_fra_due_letture(self):
        """Muro a ovest e a est, muro a nord: si passa solo verso sud."""
        self.assertEqual(K.asse(_at(["🏰🏰🏰", "🏰🚪🏰", "⬜⬜⬜"]), 1, 1), K.EO)

    def test_il_selettore_di_variante_non_conta(self):
        self.assertEqual(K.asse(_at([["⬜"] * 3, ["🏰", "🚪️", "🏰"], ["⬜"] * 3]), 1, 1), K.EO)


ROT = {K.EO: K.NS, K.NS: K.EO, K.AMBIGUO: K.AMBIGUO, None: None}
SIMBOLI = ["🏰", "⬜", "🚪", "🟫"]


class TestProprieta(unittest.TestCase):
    """Su 2.000 griglie a caso: la regola non sa dov'e' il nord."""

    def _griglie(self):
        rng = random.Random(20261008)
        for _ in range(2000):
            n = rng.randint(3, 7)
            yield [[rng.choice(SIMBOLI) for _ in range(n)] for _ in range(n)]

    def test_ruotare_scambia_gli_assi(self):
        for g in self._griglie():
            n = len(g)
            r = [[g[n - 1 - x][y] for x in range(n)] for y in range(n)]
            for y in range(n):
                for x in range(n):
                    if g[y][x] == "🚪":
                        self.assertEqual(ROT[K.asse(_at(g), x, y)], K.asse(_at(r), n - 1 - y, x))

    def test_specchiare_conserva_gli_assi(self):
        for g in self._griglie():
            n = len(g)
            m = [riga[::-1] for riga in g]
            for y in range(n):
                for x in range(n):
                    if g[y][x] == "🚪":
                        self.assertEqual(K.asse(_at(g), x, y), K.asse(_at(m), n - 1 - x, y))


class TestVerso(unittest.TestCase):
    def test_la_direttiva_si_legge(self):
        self.assertEqual(K.versi_dichiarati(["@verso B05 ; NS", "@verso c3;eo"]),
                         {("B", 5): K.NS, ("C", 3): K.EO})

    def test_una_direttiva_storta_e_scartata_e_detta(self):
        righe = ["@verso B05 ; diagonale", "@verso ; NS"]
        self.assertEqual(K.versi_dichiarati(righe), {})
        self.assertEqual(len(K.verso_illeggibile(righe)), 2)

    def test_la_direttiva_vince_sui_muri(self):
        at = _at(EST_OVEST)
        self.assertEqual(K.asse_da_disegnare(at, 1, 1, "B", 2, {("B", 2): K.NS}), K.NS)
        self.assertEqual(K.asse_da_disegnare(at, 1, 1, "B", 2, {}), K.EO)


STANZA_NS = [
    "🏰🏰🏰🏰🏰🏰",
    "🏰⬜⬜⬜⬜🏰",
    "🚪⬜🔵⬜🔴🏰",
    "🏰⬜⬜⬜⬜🏰",
    "🏰🏰🏰🏰🏰🏰",
]


class TestTreLettori(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def _mappa(self, righe, direttive=("@north N",)):
        p = _master(self.tmp, "m.md", righe, list(direttive))
        return p, R.extract_maps(p.read_text(encoding="utf-8"))[0]

    def test_il_renderer_ruota_la_porta_in_un_muro_nord_sud(self):
        _, g = self._mappa(STANZA_NS)
        self.assertIn('href="#pr_door"', R.render_svg(g, "m.md"))
        self.assertIn("rotate(90", R.render_svg(g, "m.md"))

    def test_il_renderer_non_ruota_la_porta_in_un_muro_est_ovest(self):
        _, g = self._mappa(["🏰🏰🚪🏰🏰", "🏰⬜🔵⬜🏰", "🏰⬜🔴⬜🏰", "🏰🏰🏰🏰🏰"])
        self.assertNotIn("rotate(90", R.render_svg(g, "m.md"))

    def test_l_export_uvtt_mette_il_portale_lungo_il_muro(self):
        _, g = self._mappa(STANZA_NS)
        (portale,) = U.build_uvtt(g, 70)["portals"]
        a, b = portale["bounds"]
        self.assertEqual(a["x"], b["x"], "in un muro nord-sud il portale e' verticale")

    def test_l_export_uvtt_obbedisce_a_verso(self):
        _, g = self._mappa(STANZA_NS, ["@north N", "@verso A03 ; EO"])
        (portale,) = U.build_uvtt(g, 70)["portals"]
        a, b = portale["bounds"]
        self.assertEqual(a["y"], b["y"])

    def test_il_collaudo_conta_gli_assi(self):
        p, g = self._mappa(STANZA_NS)
        dato = C.Collaudo(p, 1, g, {}).esegui().come_dato()
        self.assertEqual(dato["chiusure"]["NS"], 1)
        self.assertEqual(dato["chiusure"]["EO"], 0)

    def test_asse_ambiguo_e_un_avviso(self):
        p = _master(self.tmp, "a.md", [
            "🏰🏰🏰🏰🏰🏰",
            "🏰⬜⬜⬜⬜🏰",
            "🏰🏰🚪🏰⬜🏰",
            "🏰🚪🚪🚪⬜🏰",
            "🏰🔵🚪🔴⬜🏰",
            "🏰🏰🏰🏰🏰🏰",
        ], ["@north N"])
        self.assertIn("posa/asse-ambiguo", _codici(p))
        self.assertEqual(C.CLASSE["posa/asse-ambiguo"], "A")

    def test_verso_contro_i_muri(self):
        p = _master(self.tmp, "c.md", STANZA_NS, ["@north N", "@verso A03 ; EO"])
        self.assertIn("posa/verso-contro-muri", _codici(p))

    def test_verso_d_accordo_coi_muri_tace(self):
        p = _master(self.tmp, "d.md", STANZA_NS, ["@north N", "@verso A03 ; NS"])
        self.assertNotIn("posa/verso-contro-muri", _codici(p))

    def test_verso_su_una_cella_senza_chiusura(self):
        p = _master(self.tmp, "v.md", STANZA_NS, ["@north N", "@verso B02 ; NS"])
        self.assertIn("posa/verso-illeggibile", _codici(p))

    def test_il_rapporto_resta_nello_schema(self):
        schema = json.loads((SCRIPTS / "schemas/map_findings.schema.json").read_text(encoding="utf-8"))
        voce = schema["properties"]["mappe"]["items"]["properties"]["chiusure"]["properties"]
        self.assertEqual(set(voce), {"EO", "NS", "ambigue", "senza_muro", "dichiarate"})


if __name__ == "__main__":
    unittest.main()
