"""Le metriche di classificazione del repo: valori fatti a mano contro sklearn e scipy (ADR-0154).

I conti a mano restano: dicono che usiamo bene la libreria (le etichette, la
media, il caso 0/0), non che la libreria sappia contare.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import eval_metriche as em  # noqa: E402

LIBRERIE = all(importlib.util.find_spec(m) is not None for m in ("sklearn", "scipy"))
SENZA = "scikit-learn o scipy assenti: pip install -r requirements-dev.txt"

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


class TestImport(unittest.TestCase):
    def test_il_modulo_non_carica_le_librerie_all_import(self) -> None:
        # instradamento_agenti importa questo modulo nel percorso degli hook:
        # sklearn e scipy si caricano solo quando una metrica si calcola
        codice = ("import sys; sys.path.insert(0, sys.argv[1]); import eval_metriche; "
                  "print(sorted(m for m in ('sklearn', 'scipy', 'numpy') if m in sys.modules))")
        r = subprocess.run([sys.executable, "-c", codice, str(SCRIPTS)],
                           capture_output=True, text=True, check=True)
        self.assertEqual(r.stdout.strip(), "[]")


@unittest.skipUnless(LIBRERIE, SENZA)
class TestMatrice(unittest.TestCase):
    def test_etichette_ordinate_e_unione(self) -> None:
        self.assertEqual(em.etichette(["c", "a"], ["b", "a"]), ["a", "b", "c"])

    def test_matrice_a_mano(self) -> None:
        etich, m = em.matrice_confusione(ORO, PRED)
        self.assertEqual(etich, ["a", "b", "c"])
        self.assertEqual(m, [[2, 1, 0], [0, 1, 1], [0, 0, 1]])
        self.assertIs(type(m[0][0]), int)  # niente numpy.int64 nel JSON

    def test_lunghezze_diverse_rifiutate(self) -> None:
        with self.assertRaises(ValueError):
            em.matrice_confusione(["a"], ["a", "b"])


@unittest.skipUnless(LIBRERIE, SENZA)
class TestPerClasse(unittest.TestCase):
    def _uguale(self, got: dict, atteso: dict) -> None:
        self.assertEqual(got["supporto"], atteso["supporto"])
        for k in ("precision", "recall", "f1"):
            self.assertAlmostEqual(got[k], float(atteso[k]), places=12, msg=k)

    def test_valori_a_mano(self) -> None:
        pc = em.per_classe(ORO, PRED)
        self._uguale(pc["a"], {"precision": F(1), "recall": F(2, 3), "f1": F(4, 5), "supporto": 3})
        self._uguale(pc["b"], {"precision": F(1, 2), "recall": F(1, 2), "f1": F(1, 2),
                               "supporto": 2})
        self._uguale(pc["c"], {"precision": F(1, 2), "recall": F(1), "f1": F(2, 3), "supporto": 1})

    def test_macro_micro_accuracy(self) -> None:
        self.assertIsInstance(em.macro_f1(ORO, PRED), float)  # il valore di sklearn, non nostro
        self.assertAlmostEqual(em.macro_f1(ORO, PRED), 59 / 90, places=12)
        self.assertAlmostEqual(em.micro_f1(ORO, PRED), 2 / 3, places=12)
        self.assertAlmostEqual(em.accuracy(ORO, PRED), 2 / 3, places=12)
        self.assertEqual(em.giusti(ORO, PRED), 4)
        self.assertIs(type(em.giusti(ORO, PRED)), int)

    def test_uguale_a_sklearn_chiamato_a_mano(self) -> None:
        from sklearn.metrics import f1_score
        self.assertEqual(em.macro_f1(ORO, PRED),
                         f1_score(ORO, PRED, labels=["a", "b", "c"], average="macro",
                                  zero_division=0))

    def test_macro_esatta_dai_conteggi_uguale_a_sklearn(self) -> None:
        self.assertEqual(em.macro_f1_esatta(ORO, PRED), F(59, 90))
        self.assertEqual(em.macro_f1_esatta(["a", "b"], ["a", "d"]), F(1, 3))
        self.assertEqual(em.macro_f1_esatta([], []), F(0))
        casi = [(ORO, PRED), (["a", "b"], ["a", "d"]), (list("aabbccdd"), list("abcdabcd")),
                (list("xxxxxy"), list("xxxxxx"))]
        for oro, pred in casi:
            with self.subTest(oro=oro):
                self.assertAlmostEqual(float(em.macro_f1_esatta(oro, pred)),
                                       em.macro_f1(oro, pred), places=12)

    def test_zero_su_zero_e_classe_solo_predetta(self) -> None:
        # «d» c'è solo fra le predizioni, «b» solo nell'oro: entrambe contano nella
        # macro con F1 0 (sklearn: labels=unione, zero_division=0) -> (1 + 0 + 0) / 3
        pc = em.per_classe(["a", "b"], ["a", "d"])
        self.assertEqual(pc["d"], {"precision": 0.0, "recall": 0.0, "f1": 0.0, "supporto": 0})
        self.assertEqual(pc["b"]["precision"], 0.0)
        self.assertAlmostEqual(em.macro_f1(["a", "b"], ["a", "d"]), 1 / 3, places=12)

    def test_insieme_vuoto(self) -> None:
        self.assertEqual(em.accuracy([], []), 0.0)
        self.assertEqual(em.macro_f1([], []), 0.0)
        self.assertEqual(em.matrice_confusione([], []), ([], []))

    def test_rapporto_di_testo_di_sklearn(self) -> None:
        testo = em.rapporto_testo(ORO, PRED)
        self.assertIn("macro avg", testo)
        self.assertIn("0.6556", testo)  # 59/90 a quattro cifre


class TestIndulgente(unittest.TestCase):
    """Le «accettabili» sono nostre: nessuna libreria le conosce."""

    def test_accettabili_contano(self) -> None:
        oro = ["a", "b", "c"]
        pred = ["a", "x", "y"]
        acc = [[], ["x"], ["z"]]
        self.assertEqual(em.giusti_indulgenti(oro, pred, acc), 2)
        self.assertEqual(em.accuracy_indulgente(oro, pred, acc), F(2, 3))


@unittest.skipUnless(LIBRERIE, SENZA)
class TestWilson(unittest.TestCase):
    def test_casi_limite(self) -> None:
        self.assertEqual(em.wilson(0, 0), (0.0, 1.0))
        basso, alto = em.wilson(0, 10)
        self.assertEqual(basso, 0.0)
        self.assertGreater(alto, 0.0)
        self.assertEqual(em.wilson(5, 5)[1], 1.0)

    def test_valore_a_mano(self) -> None:
        # k=7, n=28, z=1,96: denominatore 1 + z²/n = 1,13720, centro 0,28016, semiampiezza 0,15340
        basso, alto = em.wilson(7, 28)
        self.assertAlmostEqual(basso, 0.12676, places=4)
        self.assertAlmostEqual(alto, 0.43356, places=4)

    def test_e_scipy(self) -> None:
        from scipy.stats import binomtest
        for k, n in [(7, 28), (10, 28), (0, 5), (5, 5), (1, 18), (13, 29), (50, 100)]:
            with self.subTest(k=k, n=n):
                ci = binomtest(k, n).proportion_ci(confidence_level=0.95, method="wilson")
                self.assertEqual(em.wilson(k, n), (float(ci.low), float(ci.high)))


@unittest.skipUnless(LIBRERIE, SENZA)
class TestKappa(unittest.TestCase):
    def test_esempio_pubblicato(self) -> None:
        # Esempio della voce «Cohen's kappa» (Wikipedia): 50 casi, sì/sì 20, sì/no 5,
        # no/sì 10, no/no 15 -> p_o 0,7, p_e 0,5, kappa 0,4
        a = ["si"] * 25 + ["no"] * 25
        b = ["si"] * 20 + ["no"] * 5 + ["si"] * 10 + ["no"] * 15
        self.assertAlmostEqual(em.kappa_cohen(a, b), 0.4, places=12)

    def test_accordo_perfetto_e_costante(self) -> None:
        self.assertAlmostEqual(em.kappa_cohen(["a", "b"], ["a", "b"]), 1.0, places=12)
        # p_e = 1: entrambi costanti e d'accordo. sklearn lo dichiara indefinito
        # (nan); noi gli diamo 1 con replace_undefined_by, la convenzione di prima
        self.assertEqual(em.kappa_cohen(["a", "a"], ["a", "a"]), 1.0)


@unittest.skipUnless(LIBRERIE, SENZA)
class TestBootstrap(unittest.TestCase):
    def test_stesso_seme_stesso_risultato(self) -> None:
        r1 = em.bootstrap_macro_f1(ORO, PRED, campioni=200, seme=7)
        r2 = em.bootstrap_macro_f1(ORO, PRED, campioni=200, seme=7)
        self.assertEqual(r1, r2)
        self.assertAlmostEqual(r1["stima"], 59 / 90, places=12)
        self.assertLessEqual(r1["basso"], r1["alto"])
        self.assertGreaterEqual(r1["basso"], 0.0)
        self.assertLessEqual(r1["alto"], 1.0)

    def test_e_scipy_bootstrap_percentile(self) -> None:
        import numpy as np
        from scipy.stats import bootstrap
        from sklearn.metrics import f1_score

        def stat(idx):
            o = [ORO[i] for i in np.asarray(idx, dtype=int)]
            p = [PRED[i] for i in np.asarray(idx, dtype=int)]
            return f1_score(o, p, labels=sorted(set(o) | set(p)), average="macro",
                            zero_division=0)

        ci = bootstrap((np.arange(len(ORO)),), stat, n_resamples=200, method="percentile",
                       confidence_level=0.95, rng=np.random.default_rng(7),
                       vectorized=False).confidence_interval
        r = em.bootstrap_macro_f1(ORO, PRED, campioni=200, seme=7)
        self.assertEqual((r["basso"], r["alto"]), (float(ci.low), float(ci.high)))

    def test_senza_campioni_o_con_un_caso(self) -> None:
        r = em.bootstrap_macro_f1(["a"], ["a"], campioni=200)
        self.assertEqual((r["basso"], r["alto"], r["campioni"]), (1.0, 1.0, 0))
        r = em.bootstrap_macro_f1(ORO, PRED, campioni=0)
        self.assertEqual(r["campioni"], 0)


@unittest.skipUnless(LIBRERIE, SENZA)
class TestBaseline(unittest.TestCase):
    def test_maggioritaria_e_pareggio(self) -> None:
        self.assertEqual(em.maggioritaria(["b", "a", "b"]), "b")
        # pareggio: DummyClassifier prende la prima di classes_, che è np.unique,
        # cioè l'ordine dei code point: la stessa regola alfabetica di sorted()
        self.assertEqual(em.maggioritaria(["y", "x", "y", "x"]), "x")
        self.assertEqual(em.maggioritaria(["b", "B", "b", "B"]), "B")
        self.assertIsNone(em.maggioritaria([]))

    def test_baseline_addestrata_su_uno_e_applicata_a_un_altro(self) -> None:
        self.assertEqual(em.baseline_maggioritaria(["b", "a", "b"], 4), ["b"] * 4)
        self.assertEqual(em.baseline_maggioritaria([], 2), [])

    def test_rapporto_serializzabile_e_identico(self) -> None:
        r = em.rapporto(ORO, PRED, [[]] * 6, campioni=100)
        testo = json.dumps(r, ensure_ascii=False, sort_keys=True)
        self.assertEqual(testo, json.dumps(em.rapporto(ORO, PRED, [[]] * 6, campioni=100),
                                           ensure_ascii=False, sort_keys=True))
        self.assertEqual(r["giusti"], 4)
        self.assertEqual(r["n"], 6)
        self.assertEqual(r["accuracy"]["frazione"], "2/3")
        self.assertEqual(r["macro_f1"], {"frazione": "59/90", "valore": 0.6556})
        # senza campioni il bootstrap non entra nel rapporto (dipende da numpy)
        self.assertNotIn("macro_f1_bootstrap95", em.rapporto(ORO, PRED, campioni=0))
        # ogni float esce a quattro cifre: nessun 0.65555555555 nel JSON
        for v in (r["wilson95"] + r["wilson95_indulgente"]
                  + [r["macro_f1_bootstrap95"]["basso"], r["macro_f1_bootstrap95"]["alto"]]
                  + [x for c in r["per_classe"].values() for x in
                     (c["precision"], c["recall"], c["f1"])]):
            self.assertEqual(v, round(v, 4))
            self.assertIs(type(v), float)


class TestEsecuzioneDaSola(unittest.TestCase):
    """Il manifest dichiara stdout JSON: senza opzioni l'uscita si legge con json.loads (Codex, #531)."""

    def _esegui(self, *argomenti: str) -> str:
        return subprocess.run([sys.executable, str(Path(em.__file__)), *argomenti],
                              capture_output=True, text=True, check=True).stdout

    def test_senza_opzioni_esce_solo_json(self) -> None:
        dati = json.loads(self._esegui())
        self.assertIn("macro_f1", dati)

    def test_il_testo_si_chiede_a_parte(self) -> None:
        uscita = self._esegui("--testo")
        self.assertRaises(ValueError, json.loads, uscita)
        self.assertIn("precision", uscita)


if __name__ == "__main__":
    unittest.main()
