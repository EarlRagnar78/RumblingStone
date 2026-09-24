"""I due rilevatori nuovi del 2026-09-21, e perche' uno pesa e l'altro no.

**ADR-0014 §2 — la metratura nella voce narrante.** Si cerca la **forma**
numero + unita' di *spazio*, non il numero: e' la lezione di ADR-0060, che ha
portato 2.014 occorrenze inutilizzabili a 258 con zero falsi positivi. Meta'
delle prove qui sotto verifica che il rilevatore **taccia** sui numeri che la
voce narrante usa a ragione.

**`italiano-nativo.md` §8 — la norma positiva.** Rilevata a meta' e dichiarata
tale: il «c'e'» presentativo si riconosce, la dislocazione a sinistra no. Per
questo **misura e non pesa**, e c'e' una prova che lo impone.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402
import punteggio_mqm as pm  # noqa: E402


def _box(corpo: str) -> str:
    return f"> *{corpo}*\n"


class TestLaMetraturaSiRiconosce(unittest.TestCase):
    def test_metri_nella_voce_narrante(self):
        for forma in ("diametro 9 metri", "sospeso 2 metri sopra", "largo 15 m",
                      "cerchio 2,5m", "camera di 30 centimetri", "Ø 60 m",
                      "6 quadretti", "~120°F", "49 °C", "a 3 km"):
            with self.subTest(forma=forma):
                self.assertTrue(mc.metrature_nei_box(_box(f"Davanti a voi, {forma}.")),
                                forma)

    def test_tace_sui_numeri_che_la_voce_usa_a_ragione(self):
        """La meta' che conta: un rilevatore che segnala ogni numero viene
        spento dopo una settimana."""
        for forma in ("per tre round", "sessanta battiti al minuto",
                      "l'anno -5000", "tre nani in fila", "otto secoli fa",
                      "quattro civette", "1 tonnellata di roccia",
                      "alta come tre nani", "grande come la piazza di un mercato"):
            with self.subTest(forma=forma):
                self.assertEqual(mc.metrature_nei_box(_box(f"Vedi {forma}.")), [],
                                 forma)

    def test_il_paragone_e_la_forma_che_la_norma_VUOLE(self):
        """ADR-0014 §2 non vieta la scala: vieta la misura. «Grande come la
        piazza di un mercato» e' l'esempio che l'ADR porta come corretto."""
        self.assertEqual(
            mc.metrature_nei_box(_box("una bolla grande come la piazza di un mercato")), [])

    def test_guarda_solo_dentro_i_box(self):
        fuori = "La sala e' larga 30 metri.\n\n**Dati per il DM:** 12 quadretti.\n"
        self.assertEqual(mc.metrature_nei_box(fuori), [],
                         "il blocco dati e' il posto GIUSTO per una metratura")

    def test_e_idempotente(self):
        t = _box("piattaforma di 9 metri") + _box("alta 3 m")
        self.assertEqual(mc.metrature_nei_box(t), mc.metrature_nei_box(t))

    def test_il_conteggio_sul_repo_e_quello_pubblicato(self):
        tot = sum(len(mc.metrature_nei_box(f.read_text(encoding="utf-8", errors="replace")))
                  for f in mc.file_di_gioco_p1())
        self.assertGreater(tot, 0, "il rilevatore non pesca piu' niente")
        self.assertLess(tot, 60, f"{tot} rilievi: il rilevatore si e' allargato")


class TestLaNormaPositiva(unittest.TestCase):
    def test_il_ce_presentativo_si_riconosce(self):
        """⚠️ Con l'accento vero: il repo scrive `c’è`, non `c’e’`.
        La prima stesura di questa prova usava la traslitterazione ASCII ed e'
        diventata rossa — il rilevatore aveva ragione, il fixture no."""
        self.assertEqual(
            mc.box_senza_costrutto_italiano(_box(
                "C'è una porta sul fondo, e nessuno sa dove porti. " * 4)), [])

    def test_anche_ci_sono_e_presentativo(self):
        self.assertEqual(
            mc.box_senza_costrutto_italiano(_box(
                "Ci sono tre porte sul fondo, e nessuna delle tre porta fuori "
                "da questa sala senza pagare un prezzo. " * 2)), [])

    def test_la_dislocazione_col_clitico_si_riconosce(self):
        self.assertEqual(
            mc.box_senza_costrutto_italiano(_box(
                "La porta sul fondo, la conoscono tutti quelli che hanno passato "
                "una notte qui dentro senza dormire mai fino all'alba. " * 2)), [])

    def test_un_box_corto_non_deve_portare_un_costrutto(self):
        """Una norma positiva su due righe sarebbe una tassa, non una norma."""
        self.assertEqual(mc.box_senza_costrutto_italiano(_box("Buio. Poi la fiamma.")), [])

    def test_un_box_lungo_senza_costrutto_si_segnala(self):
        self.assertEqual(len(mc.box_senza_costrutto_italiano(_box(
            "Le pareti salgono dritte verso un soffitto che nessuna torcia "
            "raggiunge, e il rumore dei vostri passi torna indietro tre volte "
            "prima di spegnersi del tutto nel fondo della sala."))), 1)


class TestChiPesaEChiNo(unittest.TestCase):
    def test_la_metratura_pesa(self):
        self.assertIn("metratura_nella_voce_narrante", pm.carica_specifiche()["norme"])

    def test_la_norma_positiva_NON_pesa_ed_e_una_scelta(self):
        """🔴 La prova che impone la decisione, non che la registra.

        La dislocazione a sinistra e' rilevata a meta': pesarla metterebbe
        **penalita' false** su box che la norma la rispettano in un modo che
        il pattern non vede — 281 rilievi su 477 sul repo, il 59%, che e' il
        numero di una sovrastima e non di un difetto. Se un giorno qualcuno la
        mette nel punteggio, questo test glielo dice in faccia: prima serve il
        rilevatore della meta' mancante.
        """
        spec = pm.carica_specifiche()
        for chiave in spec["norme"]:
            self.assertNotIn("costrutto", chiave,
                             "la norma positiva non si pesa finche' e' rilevata a meta'")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
