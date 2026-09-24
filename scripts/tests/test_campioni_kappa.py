"""F1.5 e F3.3 — i due campioni, e il κ che dice di no.

⚠️ **Meta' di queste prove verifica che il κ sappia dire zero.** Una metrica
d'accordo che non puo' bocciare non valida niente: il caso del 2026-09-21 —
Po 0,95, Pe 0,95, **κ 0,0** — e' il caso che conta, ed e' quello che la
percentuale grezza avrebbe nascosto dietro un «95% d'accordo».
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import campioni_kappa as ck  # noqa: E402


class TestIlKappaEQuelloDiCohen(unittest.TestCase):
    def test_accordo_totale_con_giudizi_vari(self):
        c = [("promosso", "promosso")] * 10 + [("bocciato", "bocciato")] * 10
        self.assertEqual(ck.kappa(c)["kappa"], 1.0)

    def test_disaccordo_totale_e_negativo(self):
        c = [("promosso", "bocciato")] * 10 + [("bocciato", "promosso")] * 10
        self.assertLess(ck.kappa(c)["kappa"], 0)

    def test_accordo_alto_ma_per_caso_vale_zero(self):
        """🔴 Il caso vero del repo, e la ragione per cui si usa il κ e non la
        percentuale: 19 accordi su 20 sembrano un ottimo risultato, e non
        valgono niente se entrambi i giudici dicono «promosso» a tutto."""
        c = [("promosso", "promosso")] * 19 + [("bocciato", "promosso")]
        r = ck.kappa(c)
        self.assertEqual(r["accordo_osservato"], 0.95)
        self.assertEqual(r["accordo_atteso_per_caso"], 0.95)
        self.assertEqual(r["kappa"], 0.0)
        self.assertFalse(r["supera_la_soglia"])

    def test_la_soglia_e_quella_del_piano(self):
        self.assertTrue(ck.kappa([("p", "p")] * 9 + [("b", "b")] * 11)["supera_la_soglia"])
        self.assertFalse(ck.kappa([("p", "p")] * 19 + [("b", "p")])["supera_la_soglia"])

    def test_la_lettura_e_landis_e_koch(self):
        for k, atteso in ((-0.1, "peggio del caso"), (0.1, "lieve"),
                          (0.3, "discreto"), (0.5, "moderato"),
                          (0.7, "sostanziale"), (0.9, "quasi perfetto")):
            self.assertEqual(ck._lettura(k), atteso, k)

    def test_nessun_voto_non_e_un_kappa_zero(self):
        """Un campione non votato e' **assenza di misura**, non accordo nullo:
        confonderli direbbe «la metrica e' inaffidabile» dove il vero e' «non
        e' stata ancora provata»."""
        self.assertIsNone(ck.kappa([]))


class TestICampioniSonoOnesti(unittest.TestCase):
    def setUp(self):
        self.dati = json.loads(ck.CAMPIONI.read_text(encoding="utf-8"))

    def test_sono_disgiunti(self):
        a, b = set(self.dati["A"]["file"]), set(self.dati["B"]["file"])
        self.assertEqual(a & b, set(), "i due campioni si sovrappongono")

    def test_il_seme_e_fisso_e_l_estrazione_riproducibile(self):
        """Senza seme fisso il campione cambierebbe a ogni esecuzione e il κ
        non sarebbe confrontabile con se stesso."""
        self.assertEqual(ck.estrai()["A"]["file"], ck.estrai()["A"]["file"])
        self.assertEqual(self.dati["seme"], ck.SEME)

    def test_ogni_file_del_campione_esiste(self):
        for quale in ("A", "B"):
            for f in self.dati[quale]["file"]:
                self.assertTrue((ROOT / f).exists(), f)

    def test_il_bias_del_giudice_B_e_dichiarato(self):
        """🔴 Il giudice B ha scritto meta' dei rilevatori. Tacerlo renderebbe
        il suo κ una certificazione invece che un limite superiore."""
        self.assertIn("bias", self.dati["B"]["giudice"].lower())


class TestIlVerdettoSulRepoEScrittoDovunque(unittest.TestCase):
    def test_il_piano_dichiara_la_metrica_non_validata(self):
        piano = (ROOT / "plans" / "PIANO-MISURA-EDITORIALE-STANDARD.md").read_text(
            encoding="utf-8")
        self.assertIn("κ = 0,0", piano)
        # ⚠️ Si cerca la **frase della regola**, non una formulazione: il piano
        # scrive «NON è validata» in maiuscolo dentro il grassetto, e la prima
        # stesura di questa prova cercava la minuscola. Un test che dipende da
        # come e' scritta una frase invecchia alla prima riscrittura.
        self.assertIn("non affidabile", piano)

    def test_i_voti_di_B_ci_sono_e_quelli_di_A_no(self):
        voti = json.loads(ck.VOTI.read_text(encoding="utf-8"))
        self.assertEqual(len(voti["B"]), 20)
        self.assertEqual(voti["A"], {},
                         "i voti di A li scrive il DM: non si inventano")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()


class TestLaBaselineMisuraIlMiglioramento(unittest.TestCase):
    """ADR-0036 dice *«si misura il miglioramento, non lo stato»*, e fino al
    2026-09-21 mancava la linea di base: il miglioramento si confrontava a
    occhio fra due esecuzioni. Un confronto a memoria non e' una misura."""

    def setUp(self):
        import punteggio_mqm as pm  # noqa: PLC0415
        self.pm = pm
        self.b = json.loads(pm.BASELINE.read_text(encoding="utf-8"))

    def test_la_baseline_e_per_documento_non_solo_aggregata(self):
        """L'aggregato dice CHE qualcosa e' peggiorato, non QUALE."""
        self.assertGreater(len(self.b["documenti"]), 400)

    def test_dichiara_con_quante_norme_e_stata_presa(self):
        """🔴 Il confronto vale solo a metro costante: un metro con piu' denti
        da' numeri piu' bassi sugli **stessi** documenti, e senza questo campo
        il calo sembrerebbe un peggioramento del repo."""
        self.assertIn("norme_pesate", self.b)
        self.assertEqual(self.b["norme_pesate"],
                         len(self.pm.carica_specifiche()["norme"]))

    def test_ogni_documento_della_baseline_esiste(self):
        for f in list(self.b["documenti"])[:60]:
            self.assertTrue((ROOT / f).exists(), f)

    def test_il_confronto_con_se_stessa_non_trova_differenze(self):
        esiti = [{"file": f, "punteggio": p}
                 for f, p in self.b["documenti"].items()]
        import io, contextlib  # noqa: PLC0415
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.pm.confronta_baseline(esiti)
        uscita = buf.getvalue()
        self.assertIn("migliorati: 0", uscita)
        self.assertIn("peggiorati: 0", uscita)

    def test_un_peggioramento_si_vede(self):
        esiti = [{"file": f, "punteggio": p - 3}
                 for f, p in list(self.b["documenti"].items())[:5]]
        import io, contextlib  # noqa: PLC0415
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.pm.confronta_baseline(esiti)
        self.assertIn("peggiorati: 5", buf.getvalue())
