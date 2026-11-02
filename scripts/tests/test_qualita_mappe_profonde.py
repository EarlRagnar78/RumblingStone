"""qualita_mappe_profonde: le metriche profonde di qualita_mappe.py --profonde.

Griglie e grafi piccoli, con i valori fatti a mano dove si puo'. Le metriche
non hanno soglia: si verifica che il numero sia quello della formula, che non
tocchi il voto e che due esecuzioni diano lo stesso file.
"""

import json
import math
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import collaudo_mappe as C  # noqa: E402
import qualita_mappe as Q  # noqa: E402
import qualita_mappe_profonde as P  # noqa: E402
from test_qualita_mappe import NORD, _master, _sala  # noqa: E402


def _grafo(n: int, archi) -> list[int]:
    adj = [0] * n
    for a, b in archi:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj


CAMMINO_4 = _grafo(4, [(0, 1), (1, 2), (2, 3)])


class TestSintassi(unittest.TestCase):
    def test_d_k_di_hillier_e_hanson(self):
        # D_4 = 2(4(log2 2 - 1) + 1) / (3 * 2) = 1/3; D_7 = 0,34 in Ostwald 2011
        self.assertAlmostEqual(P.d_k(4), 1 / 3)
        self.assertAlmostEqual(P.d_k(7), 0.34, places=2)
        self.assertIsNone(P.d_k(3))

    def test_cammino_di_quattro_nodi(self):
        """0-1-2-3. MD dei capi (1+2+3)/3 = 2, dei due in mezzo (1+1+2)/3 = 4/3.
        RA = 2(MD-1)/(k-2): 1 e 1/3; integrazione D_4/RA: 1/3 e 1."""
        grado, md, integ = P.per_nodo(CAMMINO_4)
        self.assertEqual(grado, [1, 2, 2, 1])
        for got, att in zip(md, [2, 4 / 3, 4 / 3, 2]):
            self.assertAlmostEqual(got, att)
        for got, att in zip(integ, [1 / 3, 1, 1, 1 / 3]):
            self.assertAlmostEqual(got, att)

    def test_riassunto_e_intelligibilita(self):
        s, _ = P.sintassi(CAMMINO_4)
        self.assertEqual(s["nodi"], 4)
        self.assertEqual(s["connettivita_media"], 1.5)
        self.assertEqual(s["profondita_media"], round(5 / 3, 4))
        self.assertEqual(s["integrazione_media"], round(2 / 3, 4))
        self.assertEqual(s["integrazione_min"], round(1 / 3, 4))
        self.assertEqual(s["integrazione_max"], 1.0)
        # grado [1,2,2,1] e integrazione [1/3,1,1,1/3] crescono insieme: r^2 = 1
        self.assertEqual(s["intelligibilita_r2"], 1.0)

    def test_grafo_completo_profondita_uno_e_integrazione_assente(self):
        """In K4 ogni nodo vede tutti a un passo: MD = 1, RA = 0, e
        l'integrazione HH (D_k / RA) non e' definita."""
        k4 = _grafo(4, [(a, b) for a in range(4) for b in range(a + 1, 4)])
        s, integ = P.sintassi(k4)
        self.assertEqual(s["profondita_media"], 1.0)
        self.assertIsNone(s["integrazione_media"])
        self.assertEqual(integ, [None] * 4)

    def test_componenti_sotto_quattro_nodi_si_saltano(self):
        """Due componenti: un cammino di 4 e una coppia. La coppia ha k = 2."""
        g = _grafo(6, [(0, 1), (1, 2), (2, 3), (4, 5)])
        _, md, integ = P.per_nodo(g)
        self.assertIsNone(md[4])
        self.assertIsNone(integ[5])
        self.assertAlmostEqual(md[0], 2)

    def test_pearson(self):
        self.assertAlmostEqual(P.pearson([1, 2, 3], [2, 4, 6]), 1.0)
        self.assertAlmostEqual(P.pearson([1, 2, 3], [3, 2, 1]), -1.0)
        self.assertIsNone(P.pearson([1, 1, 1], [1, 2, 3]))
        self.assertIsNone(P.pearson([1, 2], [1, 2]))
        self.assertAlmostEqual(P.pearson([1, None, 2, 3], [2, 9, 4, 6]), 1.0)


class TestVista(unittest.TestCase):
    def test_tutto_aperto_si_vede_tutto(self):
        t = [[True] * 3 for _ in range(3)]
        self.assertEqual(P.campo_visivo(t, (0, 0)), {(x, y) for x in range(3) for y in range(3)})

    def test_il_muro_ferma_la_vista_e_si_vede(self):
        t = [[True, True, False, True, True]]
        self.assertEqual(P.campo_visivo(t, (0, 0)), {(0, 0), (1, 0), (2, 0)})

    def test_l_ombra_di_un_pilastro(self):
        """Pilastro in C3 di una 5 x 5, occhio in C1: l'ombra sono C4 e C5
        (pendenze -1/4 e +1/4 dal muro, fatte a mano con l'algoritmo di Ford)."""
        t = [[True] * 5 for _ in range(5)]
        t[2][2] = False
        tutte = {(x, y) for x in range(5) for y in range(5)}
        self.assertEqual(tutte - P.campo_visivo(t, (2, 0)), {(2, 3), (2, 4)})

    def test_la_vista_e_simmetrica(self):
        """Lo shadowcasting di Ford e' simmetrico fra celle trasparenti: se A
        vede B, B vede A. Una griglia a caso a seme fisso, ogni coppia."""
        rnd = random.Random(7)
        W, H = 14, 11
        t = [[rnd.random() > 0.3 for _ in range(W)] for _ in range(H)]
        libere = [(x, y) for y in range(H) for x in range(W) if t[y][x]]
        campi = {c: P.campo_visivo(t, c) for c in libere}
        for a in libere:
            for b in libere:
                self.assertEqual(b in campi[a], a in campi[b], (a, b))


class TestClassi(unittest.TestCase):
    def _c(self, s):
        return P.classe(s, C.F, C.MODO, C.FUORI)

    def test_le_classi_dalla_legenda(self):
        self.assertEqual(self._c("🏰"), "M")
        self.assertEqual(self._c("🚪"), "P")
        self.assertEqual(self._c("⬜"), ".")
        self.assertEqual(self._c("🔵"), "U")
        self.assertEqual(self._c("🪨"), "K")
        self.assertEqual(self._c("🔥"), "H")
        self.assertEqual(self._c(C.FUORI), "V")

    def test_simmetria(self):
        # «M.M» sopra «...»: speculare sinistra-destra; alto-basso uguali solo
        # le celle di mezzo (2 su 6); la rotazione come l'alto-basso
        s = P.simmetria(["M.M", "..."])
        self.assertEqual(s, {"orizzontale": 1.0, "verticale": round(2 / 6, 4), "rotazione": round(2 / 6, 4)})
        # la diagonale: nessuno specchio, ma ruotata di 180 gradi e' se stessa
        self.assertEqual(P.simmetria(["M.", ".M"]), {"orizzontale": 0.0, "verticale": 0.0, "rotazione": 1.0})

    def test_le_righe_corte_si_completano_con_fuori(self):
        self.assertEqual(P.simmetria(["M", "MM"])["verticale"], 0.5)

    def test_pattern_2x2(self):
        self.assertEqual(P.pattern_2x2(["..", ".."]), {"finestre": 1, "distinti": 1, "entropia_bit": 0.0})
        # due finestre diverse, una volta ciascuna: un bit
        self.assertEqual(P.pattern_2x2(["...", ".M."]), {"finestre": 2, "distinti": 2, "entropia_bit": 1.0})
        # tre finestre uguali e una diversa: -(3/4 log2 3/4 + 1/4 log2 1/4) = 0,8113
        p = P.pattern_2x2(["....", "....", "...M"])
        self.assertEqual((p["finestre"], p["distinti"]), (6, 2))
        h = -(5 / 6 * math.log2(5 / 6) + 1 / 6 * math.log2(1 / 6))
        self.assertEqual(p["entropia_bit"], round(h, 4))
        q = P.pattern_2x2(["...", "...", "..M"])
        self.assertEqual(q["entropia_bit"], round(-(0.75 * math.log2(0.75) + 0.25 * math.log2(0.25)), 4))


CORRIDOIO = [
    "🏰🏰🏰🏰🏰🏰",
    "🏰⬜⬜⬜⬜🏰",
    "🏰🏰🏰🏰🏰🏰",
]


class TestNelloStrumento(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_un_corridoio_fatto_a_mano(self):
        """Quattro celle in fila. A piedi e' il cammino di quattro nodi; alla
        vista si vedono tutte (K4): profondita' 1, integrazione assente."""
        q = Q.misura(_master(self.tmp, "c.md", CORRIDOIO, NORD), {})[0]
        p = q.profonde()
        self.assertEqual(p["accesso"]["profondita_media"], round(5 / 3, 4))
        self.assertEqual(p["accesso"]["integrazione_media"], round(2 / 3, 4))
        self.assertEqual(p["accesso"]["intelligibilita_r2"], 1.0)
        self.assertEqual(p["vista"]["connettivita_media"], 3.0)
        self.assertEqual(p["vista"]["profondita_media"], 1.0)
        self.assertIsNone(p["vista"]["integrazione_media"])
        self.assertIsNone(p["vista_accesso_r"])
        self.assertEqual(p["simmetria"], {"orizzontale": 1.0, "verticale": 1.0, "rotazione": 1.0})
        # 6 colonne per 3 righe: (6-1) x (3-1) = 10 finestre 2x2
        self.assertEqual(p["pattern_2x2"]["finestre"], 10)

    def test_la_vista_dietro_un_pilastro_e_piu_profonda(self):
        aperta = Q.misura(_master(self.tmp, "a.md", _sala(pilastro=False), NORD), {})[0].profonde()
        pilastro = Q.misura(_master(self.tmp, "b.md", _sala(pilastro=True), NORD), {})[0].profonde()
        self.assertGreater(pilastro["vista"]["profondita_media"], aperta["vista"]["profondita_media"])
        self.assertGreater(pilastro["accesso"]["profondita_media"], aperta["accesso"]["profondita_media"])

    def test_solo_nel_json_e_niente_sul_voto(self):
        p = _master(self.tmp, "j.md", _sala(pilastro=True), NORD)
        senza, con = self.tmp / "senza.json", self.tmp / "con.json"
        self.assertEqual(Q.main([str(p), "--json", str(senza)]), 0)
        self.assertEqual(Q.main([str(p), "--json", str(con), "--profonde"]), 0)
        a = json.loads(senza.read_text(encoding="utf-8"))["mappe"][0]
        b = json.loads(con.read_text(encoding="utf-8"))["mappe"][0]
        self.assertNotIn("profonde", a)
        self.assertIn("profonde", b)
        self.assertEqual(json.loads(con.read_text(encoding="utf-8"))["schema"], "map_quality/1")
        b.pop("profonde")
        self.assertEqual(a, b)  # voto, penalita', metriche e rilievi identici

    def test_senza_json_e_un_errore_d_uso(self):
        p = _master(self.tmp, "u.md", CORRIDOIO, NORD)
        with self.assertRaises(SystemExit) as e:
            Q.main([str(p), "--profonde"])
        self.assertEqual(e.exception.code, 2)

    def test_la_strategica_si_salta(self):
        q = Q.misura(_master(self.tmp, "s.md", CORRIDOIO, ["@north N", "@tipo strategica"]), {})[0]
        self.assertIn("saltata", q.profonde())

    def test_due_esecuzioni_danno_lo_stesso_file(self):
        """Stesso file al byte, in due processi con il seme degli hash diverso."""
        p = _master(self.tmp, "d.md", _sala(pilastro=True), NORD)
        uscite = []
        for seme in ("1", "2"):
            out = self.tmp / f"d{seme}.json"
            env = dict(os.environ, PYTHONHASHSEED=seme)
            subprocess.run([sys.executable, str(SCRIPTS / "qualita_mappe.py"), str(p), "--json", str(out),
                            "--profonde"], check=True, capture_output=True, env=env)
            uscite.append(out.read_bytes())
        self.assertEqual(uscite[0], uscite[1])


if __name__ == "__main__":
    unittest.main()
