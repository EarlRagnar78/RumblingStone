"""
Test di `dmcore.testo` (Lotto A del piano QUALITA-DEL-CODICE).

I casi non sono inventati: sono i nomi veri che il repo aveva sbagliato.
Prima dell'unificazione c'erano sette `slug` diverse, e i difetti erano due,
non uno.

1. `build_monster_catalog.py` saltava la normalizzazione NFKD, quindi le
   accentate sparivano invece di traslitterare: 3 record del catalogo con un
   id che nessun altro strumento della catena ricalcolava uguale.
2. **Tutte e sette** buttavano via i caratteri non-ASCII che NFKD non riduce a
   una lettera base. Il trattino lungo è il caso che si vede: `CR 12–13`
   diventava `cr-1213`, e due numeri diventavano uno.

Metodo del lotto B, applicato qui: scritto il test, mutare la funzione e
verificare che il test cada.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore.testo import piega_ascii, slug  # noqa: E402


class TestAccentate(unittest.TestCase):
    """Il difetto n. 1: le accentate traslitterate, non buttate."""

    def test_citta(self):
        self.assertEqual(slug("Città"), "citta")

    def test_lomyn_e_il_record_del_catalogo(self):
        # id vecchio: l-myn-redtongue-bardo-mezzelfo
        self.assertEqual(slug("Lómyn RedTongue, bardo mezzelfo", max_len=80),
                         "lomyn-redtongue-bardo-mezzelfo")

    def test_d_elite(self):
        # id vecchio: …-spawn-draconico-d-lite
        self.assertEqual(
            slug("Razorfiend «Blackspawn Alfa» — spawn draconico d'élite", max_len=80),
            "razorfiend-blackspawn-alfa-spawn-draconico-d-elite")

    def test_accento_grave_dentro_una_parola(self):
        # id vecchio: …-il-preventivo-scaduto (spariva la "è")
        self.assertEqual(slug("il preventivo è scaduto"), "il-preventivo-e-scaduto")


class TestSegniCheLAsciiNonHa(unittest.TestCase):
    """Il difetto n. 2: separare invece di far sparire."""

    def test_trattino_lungo_fra_due_numeri(self):
        self.assertEqual(slug("12–13"), "12-13")

    def test_intervallo_di_gs(self):
        self.assertEqual(slug("Rhest – Nido dei Greenspawn (CR 12–13)"),
                         "rhest-nido-dei-greenspawn-cr-12-13")

    def test_freccia(self):
        self.assertEqual(slug("Cutaway Sud→Nord"), "cutaway-sud-nord")

    def test_caporali_non_incollano_le_parole(self):
        self.assertEqual(slug("Ghaurush «Cenerevento» Secondo"),
                         "ghaurush-cenerevento-secondo")


class TestTroncamento(unittest.TestCase):
    def test_taglia_alla_lunghezza(self):
        self.assertEqual(len(slug("a" * 200, max_len=48)), 48)

    def test_senza_max_len_non_taglia(self):
        self.assertEqual(len(slug("a" * 200)), 200)

    def test_il_taglio_non_lascia_un_trattino_penzolante(self):
        # "abc-defgh" tagliato a 4 darebbe "abc-"; deve dare "abc"
        self.assertEqual(slug("abc defgh", max_len=4), "abc")

    def test_taglio_esatto_sul_confine(self):
        self.assertEqual(slug("abc defgh", max_len=3), "abc")


class TestRipiego(unittest.TestCase):
    def test_niente_di_utile_e_c_e_un_ripiego(self):
        self.assertEqual(slug("«»", ripiego="mappa"), "mappa")

    def test_niente_di_utile_e_non_c_e_ripiego(self):
        self.assertEqual(slug("«»"), "")

    def test_stringa_vuota(self):
        self.assertEqual(slug("", ripiego="scheda"), "scheda")

    def test_il_ripiego_non_scatta_se_resta_qualcosa(self):
        self.assertEqual(slug("7", ripiego="mappa"), "7")


class TestFormaDellId(unittest.TestCase):
    def test_niente_trattini_ai_bordi(self):
        s = slug("  — Titolo —  ")
        self.assertFalse(s.startswith("-") or s.endswith("-"), s)

    def test_trattini_ripetuti_collassati(self):
        self.assertEqual(slug("a — b «c» d"), "a-b-c-d")

    def test_solo_minuscole_cifre_e_trattino(self):
        s = slug("MAPPA 2C: Fortezza (Cutaway Sud→Nord) — élite 12–13")
        self.assertRegex(s, r"^[a-z0-9-]+$")

    def test_idempotente(self):
        s = slug("Lómyn «RedTongue» — CR 12–13")
        self.assertEqual(slug(s), s)


class TestPiegaAscii(unittest.TestCase):
    """I tre destini dei caratteri, verificati uno per uno."""

    def test_ascii_resta(self):
        self.assertEqual(piega_ascii("abc-123"), "abc-123")

    def test_il_combinante_si_butta(self):
        self.assertEqual(piega_ascii("é"), "e")

    def test_il_non_ascii_non_combinante_separa(self):
        self.assertEqual(piega_ascii("12–13"), "12-13")

    def test_e_la_differenza_con_encode_ignore(self):
        # come faceva il codice vecchio, per fissare cosa è cambiato
        import unicodedata
        vecchio = unicodedata.normalize("NFKD", "12–13").encode("ascii", "ignore").decode()
        self.assertEqual(vecchio, "1213")
        self.assertNotEqual(piega_ascii("12–13"), vecchio)


class TestParitaConIChiamanti(unittest.TestCase):
    """I sette chiamanti divergevano solo su lunghezza e ripiego.

    Se qualcuno riaggiunge un parametro, questo test dice quali combinazioni
    sono in uso davvero.
    """

    def test_le_combinazioni_in_uso(self):
        atteso = {
            ("catalogo", slug("Nome Mostro", max_len=80)): "nome-mostro",
            ("mappe", slug("Nome Mappa", max_len=48, ripiego="mappa")): "nome-mappa",
            ("scheda", slug("Nome Scheda", ripiego="scheda")): "nome-scheda",
            ("capitolo", slug("Nome Capitolo", ripiego="capitolo")): "nome-capitolo",
            ("scena", slug("Nome Scena", max_len=60, ripiego="scena")): "nome-scena",
            ("html", slug("Nome Modulo")): "nome-modulo",
        }
        for (_, ottenuto), voluto in atteso.items():
            self.assertEqual(ottenuto, voluto)


if __name__ == "__main__":
    unittest.main()
