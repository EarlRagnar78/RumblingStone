"""M4 esatta nel collaudo con tcod, M1 e M2 con scipy (ADR-0084).

La misura che ha deciso: sull'intero corpus (43.423 celle) la visibilita' da
ogni cella costa 75 s in libreria standard e 0,7 s con tcod, con lo stesso
risultato (plans/esperimenti/orientamento-e-dipendenze-2026-10).
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "tests"))
import collaudo_mappe as C  # noqa: E402

from test_collaudo_mappe import _codici, _master  # noqa: E402

APERTA = ["🏰" * 12] + ["🏰" + "⬜" * 10 + "🏰"] * 10 + ["🏰" * 12]
APERTA = [APERTA[0]] + [APERTA[1].replace("⬜", "🔵", 1)] + APERTA[2:]


def _divisa(colonne=(6,), porta=True):
    """Stanze separate da muri nord-sud, con o senza una porta nel primo."""
    righe = [list(r) for r in APERTA]
    for col in colonne:
        for y in range(1, 11):
            righe[y][col] = "🏰"
    if porta:
        righe[5][colonne[0]] = "🚪"
    return ["".join(r) for r in righe]


class TestM4(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def _m4(self, righe):
        p = _master(self.tmp, "m.md", righe, ["@north N"])
        g = C.R.extract_maps(p.read_text(encoding="utf-8"))[0]
        c = C.Collaudo(p, 1, g, {})
        return c._esposizione(c.percorribili()), p

    def test_una_sala_vuota_si_vede_tutta(self):
        m4, p = self._m4(APERTA)
        self.assertAlmostEqual(m4, 1.0)
        self.assertIn("m4/esposizione", _codici(p))

    def test_un_muro_in_mezzo_abbassa_l_esposizione(self):
        aperta, _ = self._m4(APERTA)
        divisa, _ = self._m4(_divisa())
        self.assertLess(divisa, aperta)

    def test_tre_stanze_restano_sotto_la_soglia(self):
        m4, p = self._m4(_divisa((4, 8), porta=False))
        self.assertLess(m4, 0.45)
        self.assertNotIn("m4/esposizione", _codici(p))

    def test_m1_e_m2_come_il_calcolo_a_mano(self):
        """La misura che ha fatto entrare scipy: differenza zero sul corpus.
        Il riferimento e' il calcolo a mano di prima, copiato com'era."""
        from collections import deque

        def a_mano(c, perc):
            cop = {(x, y) for x, y, s in c.G.tutte()
                   if C.F.get(s, {}).get("cover") in ("half", "three_quarters", "total")}
            vicino = {(x, y) for x, y in perc
                      if any((x + a, y + b) in cop for a in range(-2, 3) for b in range(-2, 3))}
            aperto, visti, piu = perc - vicino, set(), 0
            for p0 in aperto:
                if p0 in visti:
                    continue
                visti.add(p0)
                coda, k = deque([p0]), 0
                while coda:
                    a = coda.popleft()
                    k += 1
                    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        b = (a[0] + d[0], a[1] + d[1])
                        if b in aperto and b not in visti:
                            visti.add(b)
                            coda.append(b)
                piu = max(piu, k)
            return len(vicino) / len(perc), piu / len(perc)

        for righe in (APERTA, _divisa(), _divisa((4, 8), porta=False)):
            p = _master(self.tmp, "c.md", righe, ["@north N"])
            g = C.R.extract_maps(p.read_text(encoding="utf-8"))[0]
            c = C.Collaudo(p, 1, g, {})
            perc = c.percorribili()
            for atteso, avuto in zip(a_mano(c, perc), c._copertura_e_vuoto(perc)):
                self.assertAlmostEqual(atteso, avuto)

    def test_e_un_avviso_non_un_errore(self):
        self.assertEqual(C.CLASSE["m4/esposizione"], "A")

    def test_senza_tcod_il_collaudo_si_ferma_e_dice_perche(self):
        with mock.patch.object(C, "_dipendenze", side_effect=ImportError("tcod")), \
                mock.patch("sys.stderr") as err:
            self.assertEqual(C.main([str(self.tmp / "nessuno.md")]), 2)
        self.assertIn("requirements-dev.txt", "".join(a[0][0] for a in err.write.call_args_list))


if __name__ == "__main__":
    unittest.main()
