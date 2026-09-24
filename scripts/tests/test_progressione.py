"""La progressione di classe e di tipo, in un posto solo (ADR-0066, lotto E2).

La base dei TS era calcolata in quattro posti, e il verificatore riscriveva la
formula a mano. Questi casi sono quelli che il verificatore conosceva gia':
l'umanoide col TS buono che varia, il paladino con la Grazia divina, le classi
di prestigio SRD del Bestiario, le abbreviazioni con cui le schede scrivono le
classi.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import progressione as P  # noqa: E402


class TestLaBaseDeiTS(unittest.TestCase):
    def test_un_gruppo(self):
        self.assertEqual(P.ts_base_di(10, ("temp",)), {"temp": 7, "rifl": 3, "vol": 3})
        self.assertEqual(P.ts_base_di(1, ()), {"temp": 0, "rifl": 0, "vol": 0})

    def test_i_gruppi_si_sommano(self):
        # SRD, multiclasse: la base di ogni classe si somma, non si ricalcola sul totale
        g = [P.Gruppo("fighter", 4, 10, ("temp",), 1.0), P.Gruppo("wizard", 4, 4, ("vol",), 0.5)]
        lo, hi = P.ts_base(g)
        self.assertEqual(lo, {"temp": 5, "rifl": 2, "vol": 5})
        self.assertEqual(lo, hi)

    def test_l_umanoide_da_una_fascia(self):
        """Lo gnoll ha buona la Tempra, il bugbear i Riflessi: 2 DV umanoidi
        danno 0 se tutti cattivi e 3 se tutti buoni."""
        g = [P.Gruppo("humanoid", 2, 8, ("rifl",), 0.75), P.Gruppo("warrior", 2, 8, ("temp",), 1.0)]
        lo, hi = P.ts_base(g)
        self.assertEqual(lo, {"temp": 3, "rifl": 0, "vol": 0})
        self.assertEqual(hi, {"temp": 6, "rifl": 3, "vol": 3})

    def test_il_nome_del_tipo_decide_la_fascia_non_i_suoi_buoni(self):
        # un gruppo di tipo diverso da «humanoid» usa i suoi TS buoni
        lo, hi = P.ts_base([P.Gruppo("dragon", 10, 12, ("temp", "rifl", "vol"), 1.0)])
        self.assertEqual(lo, hi)
        self.assertEqual(lo, {"temp": 7, "rifl": 7, "vol": 7})


class TestLeClassi(unittest.TestCase):
    def test_prestigio_srd(self):
        self.assertEqual(P.classe("Blackguard"), (10, ("temp",), 1.0))
        self.assertEqual(P.classe("assassin"), (6, ("rifl",), 0.75))

    def test_abbreviazioni(self):
        self.assertEqual(P.classe("Clr"), P.classe("cleric"))
        self.assertEqual(P.DADO_DI_CLASSE["ranger"], 8)
        self.assertEqual(P.DADO_DI_CLASSE["magi"], 4)

    def test_classe_ignota(self):
        self.assertIsNone(P.classe("diviner"))

    def test_classe_e_livello_nel_testo(self):
        self.assertEqual(P.CLASSE_LIVELLO.findall("Hobgoblin Ftr. 3 / Clr 2"),
                         [("Ftr", "3"), ("Clr", "2")])

    def test_bab(self):
        g = [P.Gruppo("rogue", 2, 6, ("rifl",), 0.75), P.Gruppo("wizard", 1, 4, ("vol",), 0.5)]
        # floor(1,5) + floor(0,5) = 1: ogni gruppo si arrotonda da solo. Il
        # totale arrotondato una volta sola darebbe floor(2,0) = 2
        self.assertEqual(P.bab_atteso(g), 1)


class TestIlVerificatoreLaUsa(unittest.TestCase):
    """La Grazia divina sta nel verificatore, sopra la base: la base non la vede."""

    def test_paladino_con_grazia_divina(self):
        import conformita_statblocchi as C
        from dmcore import lettura_creatura as LC
        s = LC.Scheda(file=Path("paladino-prova-cr4.md"), gs=4.0, tipo="Medium humanoid, Paladin 4",
                     attributi={}, provenienza="a mano",
                     gruppi=[P.Gruppo("paladin", 4, 10, ("temp",), 1.0)], composizione_nota=True)
        self.assertEqual(P.ts_base(s.gruppi)[0], {"temp": 4, "rifl": 1, "vol": 1})
        lo, _ = C.ts_attesi(s, {"Car": 14, "Cos": 12, "Des": 10, "Sag": 10})
        self.assertEqual(lo, (4 + 1 + 2, 1 + 0 + 2, 1 + 0 + 2))


if __name__ == "__main__":
    unittest.main()
