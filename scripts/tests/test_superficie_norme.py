"""ADR-0062 — «manca il codice, o manca il dato?», provato dai due lati.

🔴 **Il difetto che questo cancello presidia.** ADR-0056 accetta un «non
misurato» purche' porti una ragione scritta. La ragione e' **prosa**, e la
prosa invecchia in silenzio: il 2026-09-21 si e' scoperto che «i 27 ADR
mancanti» erano **zero**, e che 27 non era mai stato un numero misurato — col
comando che lo smentiva citato accanto alla riga, verde in CI.

Meta' delle prove qui sotto verifica che il cancello **taccia**: una superficie
vuota e' un fatto, non un difetto, e un gate che la bocciasse renderebbe rossa
la CI per una cosa che nessuno puo' chiudere oggi.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import superficie_norme as sn  # noqa: E402
import validate_norme_editoriali as vne  # noqa: E402


class TestOgniNormaScopertaHaUnoStato(unittest.TestCase):
    def test_ogni_riga_porta_uno_dei_quattro_stati(self):
        validi = {sn.SUPERFICIE_VUOTA, sn.CONVENZIONE_ASSENTE,
                  sn.OGGETTO_ASSENTE, sn.FUORI_DOMINIO, "MISURABILE"}
        for r in sn.misura():
            self.assertIn(r["stato"], validi, r["chiave"])

    def test_ogni_riga_dice_dove_guardare(self):
        """Una riga senza «dove» e' la ragione in prosa di ADR-0056, da capo."""
        for r in sn.misura():
            self.assertTrue(r["dove"].strip(), r["chiave"])

    def test_chi_ha_una_forma_ha_un_conteggio_e_viceversa(self):
        for r in sn.misura():
            if r["forma"] is not None:
                self.assertIsInstance(r["occorrenze"], int, r["chiave"])
            elif not r.get("oggetto"):
                self.assertIsNone(r["occorrenze"], r["chiave"])

    def test_fuori_dominio_non_promette_un_seguito(self):
        """⚪ non e' debito: se avesse un «lo sblocca», sarebbe una riga che
        qualcuno un giorno proverebbe a chiudere, e non si chiude."""
        for r in sn.misura():
            if r["stato"] == sn.FUORI_DOMINIO:
                self.assertIsNone(r.get("sblocca"), r["chiave"])
                self.assertIsNone(r["prerequisito"], r["chiave"])


class TestEDeterministicoEIdempotente(unittest.TestCase):
    def test_due_esecuzioni_danno_lo_stesso_risultato(self):
        self.assertEqual(sn.misura(), sn.misura())

    def test_l_insieme_dei_file_e_quello_che_il_repo_dichiara(self):
        """🐛 La prima stesura ne teneva uno suo e si e' dimenticata `build/`:
        `COLORE DOMINANTE` risultava presente **5 volte** — le copie generate
        della skill che quella forma la *prescrive* — e la norma sulla tinta
        veniva dichiarata «misurabile ora». Ventesimo caso della famiglia."""
        for f in sn._file_di_gioco():
            self.assertNotIn("build", f.parts, f)
            self.assertNotIn("_ARCHIVIO", f.parts, f)
            self.assertFalse(any(p.name.startswith(".") for p in f.parents
                                 if p != ROOT), f)


class TestIlCancelloTaceDoveDeve(unittest.TestCase):
    def test_oggi_e_verde(self):
        self.assertEqual(sn.problemi(), [])

    def test_una_superficie_vuota_NON_boccia(self):
        """La meta' che conta. `el_oltre_il_tetto` ha zero occorrenze da
        sempre: se questo bocciasse, la CI sarebbe rossa per una cosa che si
        chiude solo marcando 150 incontri."""
        vuote = [r for r in sn.misura() if r["stato"] == sn.SUPERFICIE_VUOTA]
        self.assertTrue(vuote, "nessuna superficie vuota: il caso non e' piu' coperto")
        self.assertEqual(sn.problemi(), [])


class TestIlCancelloMorde(unittest.TestCase):
    def test_una_norma_diventata_misurabile_boccia(self):
        """Il caso che il gate esiste per prendere: la superficie si riempie e
        il registro continua a dire 🔴."""
        vera = sn.NORME_SCOPERTE
        finta = tuple(dict(r, forma=r"\bil\b") if r["chiave"] == "el_oltre_il_tetto"
                      else r for r in vera)
        try:
            sn.NORME_SCOPERTE = finta
            errori = sn.problemi()
        finally:
            sn.NORME_SCOPERTE = vera
        self.assertTrue(any("misurabile" in e for e in errori), errori)

    def test_il_registro_e_la_tabella_non_divergono(self):
        """Ogni 🔴 del registro ha la sua riga qui, e viceversa."""
        testo = (ROOT / "skills" / "REGISTRO-NORME-EDITORIALI.md").read_text(
            encoding="utf-8")
        self.assertEqual(vne.conto_vero(testo)["🔴"], len(sn.misura()))

    def test_il_gate_del_registro_richiama_questo(self):
        """L'ordine del DM era «inseriscilo nella catena in modo che possa
        essere richiamato in automatico»: la prova che il collegamento c'e'."""
        sorgente = (ROOT / "scripts" / "validate_norme_editoriali.py").read_text(
            encoding="utf-8")
        self.assertIn("superficie_norme", sorgente)
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("superficie_norme.py --check", ci)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
