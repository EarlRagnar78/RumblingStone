"""F1.3 — un congegno che non separa nessuna coppia di documenti e' rumore.

**Perche' questo lotto esisteva.** Il piano lo apriva con una previsione
scritta: *«un congegno che non separa mai due documenti e' rumore e si
toglie»*. Eseguito sul repo, **nessuno dei 23 congegni e' rumore**: il piu'
debole ne separa 11 coppie su 66. La previsione non ha retto, ed e' un esito
utile quanto quello opposto — voleva dire che la tabella di `misura_craft` non
ha righe da buttare.

⚠️ **Il test non congela quel numero.** Congelare «23 congegni, zero rumore»
renderebbe rosso l'aggiunta di un congegno nuovo, che e' una cosa buona. Prova
invece le due **proprieta'** della misura, che valgono per qualunque tabella:
un congegno costante non separa niente, e uno che varia separa.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402


class TestPotereDiscriminante(unittest.TestCase):
    RIGHE = {"a": 1000, "b": 1000, "c": 2000}

    def _pd(self, dati):
        return {r[0]: r for r in mc.potere_discriminante(
            dati, list(next(iter(dati.values()))), self.RIGHE)}

    def test_un_congegno_a_zero_ovunque_non_separa_niente(self):
        dati = {"a": {"x": 0}, "b": {"x": 0}, "c": {"x": 0}}
        _, grezzo, dens, zeri, coppie, _ = self._pd(dati)["x"]
        self.assertEqual((grezzo, dens), (0, 0))
        self.assertEqual(zeri, 3)
        self.assertEqual(coppie, 3)

    def test_un_congegno_costante_non_zero_non_separa_lo_stesso(self):
        """Il caso meno ovvio: presente ovunque nella stessa misura e'
        informativo quanto assente ovunque, cioe' per niente."""
        dati = {"a": {"x": 7}, "b": {"x": 7}, "c": {"x": 14}}
        _, _, dens, _, _, _ = self._pd(dati)["x"]
        self.assertEqual(dens, 0, "7/1000 e 14/2000 sono la stessa densita'")

    def test_la_densita_corregge_la_taglia(self):
        """🔎 Il perche' della colonna: il grezzo separa `c` dagli altri solo
        perche' `c` e' lungo il doppio. La densita' dice che sono uguali."""
        dati = {"a": {"x": 7}, "b": {"x": 7}, "c": {"x": 14}}
        _, grezzo, dens, _, _, _ = self._pd(dati)["x"]
        self.assertEqual(grezzo, 2)
        self.assertEqual(dens, 0)

    def test_un_congegno_che_varia_separa(self):
        dati = {"a": {"x": 1}, "b": {"x": 5}, "c": {"x": 40}}
        _, grezzo, dens, zeri, coppie, _ = self._pd(dati)["x"]
        self.assertEqual(grezzo, coppie)
        self.assertEqual(dens, coppie)
        self.assertEqual(zeri, 0)

    def test_l_ordine_mette_i_piu_deboli_in_cima(self):
        dati = {"a": {"forte": 1, "morto": 0},
                "b": {"forte": 9, "morto": 0},
                "c": {"forte": 90, "morto": 0}}
        ordinati = mc.potere_discriminante(dati, ["forte", "morto"], self.RIGHE)
        self.assertEqual(ordinati[0][0], "morto")


class TestSulRepoVero(unittest.TestCase):
    def test_il_comando_esiste_ed_e_documentato(self):
        """ADR-0053 sui nomi inventati, applicato alle opzioni."""
        sorgente = (ROOT / "scripts" / "misura_craft.py").read_text(encoding="utf-8")
        self.assertIn('"--discriminante"', sorgente)
        self.assertIn("potere_discriminante", sorgente)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
