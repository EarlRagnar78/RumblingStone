"""Le metriche di classificazione del repo: valori fatti a mano, scipy come riscontro (ADR-0154)."""
from __future__ import annotations

import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import eval_metriche as em  # noqa: E402

try:
    from scipy.stats import binomtest  # type: ignore
except ImportError:  # pragma: no cover - scipy è in requirements-dev
    binomtest = None

# Esempio piccolo a tre classi, conti fatti a mano.
#   oro  a a a b b c
#   pred a a b b c c
# matrice (righe oro, colonne pred, ordine a b c): [2 1 0] [0 1 1] [0 0 1]
# a: tp 2, fp 0, fn 1 -> P 1,   R 2/3, F1 4/5
# b: tp 1, fp 1, fn 1 -> P 1/2, R 1/2, F1 1/2
# c: tp 1, fp 1, fn 0 -> P 1/2, R 1,   F1 2/3
# macro-F1 (4/5 + 1/2 + 2/3) / 3 = 59/90; accuracy e micro-F1 4/6 = 2/3
ORO = ["a", "a", "a", "b", "b", "c"]
PRED = ["a", "a", "b", "b", "c", "c"]


class TestMatrice(unittest.TestCase):
    def test_etichette_ordinate_e_unione(self) -> None:
        self.assertEqual(em.etichette(["c", "a"], ["b", "a"]), ["a", "b", "c"])

    def test_matrice_a_mano(self) -> None:
        etich, m = em.matrice_confusione(ORO, PRED)
        self.assertEqual(etich, ["a", "b", "c"])
        self.assertEqual(m, [[2, 1, 0], [0, 1, 1], [0, 0, 1]])

    def test_lunghezze_diverse_rifiutate(self) -> None:
        with self.assertRaises(ValueError):
            em.matrice_confusione(["a"], ["a", "b"])


class TestPerClasse(unittest.TestCase):
    def test_valori_a_mano(self) -> None:
        pc = em.per_classe(ORO, PRED)
        self.assertEqual(pc["a"], {"precision": F(1), "recall": F(2, 3), "f1": F(4, 5),
                                   "supporto": 3})
        self.assertEqual(pc["b"], {"precision": F(1, 2), "recall": F(1, 2), "f1": F(1, 2),
                                   "supporto": 2})
        self.assertEqual(pc["c"], {"precision": F(1, 2), "recall": F(1), "f1": F(2, 3),
                                   "supporto": 1})

    def test_macro_micro_accuracy(self) -> None:
        self.assertEqual(em.macro_f1(ORO, PRED), F(59, 90))
        self.assertEqual(em.micro_f1(ORO, PRED), F(2, 3))
        self.assertEqual(em.accuracy(ORO, PRED), F(2, 3))
        self.assertEqual(em.giusti(ORO, PRED), 4)

    def test_zero_su_zero_e_classe_solo_predetta(self) -> None:
        # «d» c'è solo fra le predizioni, «b» solo nell'oro: entrambe contano nella
        # macro con F1 0 (sklearn: labels=unione, zero_division=0) -> (1 + 0 + 0) / 3
        pc = em.per_classe(["a", "b"], ["a", "d"])
        self.assertEqual(pc["d"], {"precision": F(0), "recall": F(0), "f1": F(0), "supporto": 0})
        self.assertEqual(pc["b"]["precision"], F(0))
        self.assertEqual(em.macro_f1(["a", "b"], ["a", "d"]), F(1, 3))

    def test_insieme_vuoto(self) -> None:
        self.assertEqual(em.accuracy([], []), F(0))
        self.assertEqual(em.macro_f1([], []), F(0))


class TestIndulgente(unittest.TestCase):
    def test_accettabili_contano(self) -> None:
        oro = ["a", "b", "c"]
        pred = ["a", "x", "y"]
        acc = [[], ["x"], ["z"]]
        self.assertEqual(em.giusti_indulgenti(oro, pred, acc), 2)
        self.assertEqual(em.accuracy_indulgente(oro, pred, acc), F(2, 3))


class TestWilson(unittest.TestCase):
    def test_casi_limite(self) -> None:
        self.assertEqual(em.wilson(0, 0), (0.0, 1.0))
        basso, alto = em.wilson(0, 10)
        self.assertEqual(basso, 0.0)
        self.assertGreater(alto, 0.0)

    def test_valore_a_mano(self) -> None:
        # k=7, n=28, z=1,96: denominatore 1 + z²/n = 1,13720, centro 0,28016, semiampiezza 0,15340
        basso, alto = em.wilson(7, 28)
        self.assertAlmostEqual(basso, 0.12676, places=4)
        self.assertAlmostEqual(alto, 0.43356, places=4)

    @unittest.skipUnless(binomtest is not None, "scipy assente")
    def test_contro_scipy(self) -> None:
        for k, n in [(7, 28), (10, 28), (0, 5), (5, 5), (1, 18), (13, 29), (50, 100)]:
            with self.subTest(k=k, n=n):
                ci = binomtest(k, n).proportion_ci(confidence_level=0.95, method="wilson")
                basso, alto = em.wilson(k, n)
                self.assertAlmostEqual(basso, ci.low, places=10)
                self.assertAlmostEqual(alto, ci.high, places=10)


class TestKappa(unittest.TestCase):
    def test_esempio_pubblicato(self) -> None:
        # Esempio della voce «Cohen's kappa» (Wikipedia): 50 casi, sì/sì 20, sì/no 5,
        # no/sì 10, no/no 15 -> p_o 0,7, p_e 0,5, kappa 0,4
        a = ["si"] * 25 + ["no"] * 25
        b = ["si"] * 20 + ["no"] * 5 + ["si"] * 10 + ["no"] * 15
        self.assertEqual(em.kappa_cohen(a, b), F(2, 5))

    def test_accordo_perfetto_e_costante(self) -> None:
        self.assertEqual(em.kappa_cohen(["a", "b"], ["a", "b"]), F(1))
        # p_e = 1: entrambi costanti e d'accordo -> 1 per convenzione
        self.assertEqual(em.kappa_cohen(["a", "a"], ["a", "a"]), F(1))


class TestBootstrap(unittest.TestCase):
    def test_stesso_seme_stesso_risultato(self) -> None:
        r1 = em.bootstrap_macro_f1(ORO, PRED, campioni=200, seme=7)
        r2 = em.bootstrap_macro_f1(ORO, PRED, campioni=200, seme=7)
        self.assertEqual(r1, r2)
        self.assertEqual(r1["stima"], F(59, 90))
        self.assertLessEqual(r1["basso"], r1["alto"])
        self.assertGreaterEqual(r1["basso"], F(0))
        self.assertLessEqual(r1["alto"], F(1))

    def test_indici_dal_random_semplice(self) -> None:
        # gli indici vengono da int(rng.random() * n): stessi numeri fra 3.13 e 3.14
        import random
        rng = random.Random(3)
        attesi = [int(rng.random() * 6) for _ in range(6)]
        self.assertEqual(em._indici(random.Random(3), 6), attesi)


class TestBaseline(unittest.TestCase):
    def test_maggioritaria_e_pareggio(self) -> None:
        self.assertEqual(em.maggioritaria(["b", "a", "b"]), "b")
        # pareggio: vince la prima in ordine alfabetico
        self.assertEqual(em.maggioritaria(["y", "x", "y", "x"]), "x")
        self.assertIsNone(em.maggioritaria([]))

    def test_rapporto_serializzabile(self) -> None:
        import json
        r = em.rapporto(ORO, PRED, [[]] * 6)
        testo = json.dumps(r, ensure_ascii=False)
        self.assertIn('"59/90"', testo)
        self.assertEqual(r["giusti"], 4)
        self.assertEqual(r["n"], 6)


if __name__ == "__main__":
    unittest.main()
