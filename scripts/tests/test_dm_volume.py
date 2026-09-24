"""`dm.py volume`: l'ordine dei mestieri, e le due cose che non deve mai fare.

Nasce da §C della ricerca sul colophon Paizo — *«la combinazione mancante»*: le
skill c'erano tutte, e **nessun documento diceva in che ordine si chiamano** per
produrre un volume. Chi ne salta uno se ne accorge in copisteria.

Le due cose che non deve mai fare, e che hanno un test a testa:

1. **proseguire dopo un guasto duro.** Se il manifest non è valido, compilare
   l'HTML produce un artefatto sbagliato con l'aria di essere andato bene.
2. **tacere sul cancello d'uscita.** È il momento in cui un volume sta per
   uscire, ed è esattamente il buco che il lotto E aveva misurato: una regola
   scritta che nessuno carica non è una regola.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import dm  # noqa: E402


def _lancia(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(REPO / "scripts" / "dm.py"), "volume", *args],
                          capture_output=True, text=True, cwd=REPO)


class TestOrdine(unittest.TestCase):
    def test_i_mestieri_sono_in_ordine_e_dichiarati(self):
        # L'ordine è il contenuto di questo comando: se cambia, è una decisione.
        self.assertEqual(dm.PASSI_VOLUME,
                         ("prosa", "lingua", "manifest", "colophon",
                          "schermo", "stampa", "imposizione"))

    def test_senza_stampa_la_catena_si_ferma_allo_schermo(self):
        r = _lancia(str(REPO / "10-stand-alone" / "L'abbazia Della Rotta Sicura" /
                        "homebrew" / "abbazia-rotta-sicura.manifest.json"))
        self.assertIn("passi:", r.stdout)
        riga = next(l for l in r.stdout.splitlines() if l.startswith("[dm] passi:"))
        self.assertNotIn("stampa", riga)
        self.assertIn("schermo", riga)

    def test_solo_seleziona_un_passo_soltanto(self):
        r = _lancia("--solo", "colophon",
                    str(REPO / "10-stand-alone" / "L'abbazia Della Rotta Sicura" /
                        "homebrew" / "abbazia-rotta-sicura.manifest.json"))
        riga = next(l for l in r.stdout.splitlines() if l.startswith("[dm] passi:"))
        self.assertEqual(riga.split(":", 1)[1].strip(), "colophon")


class TestColophon(unittest.TestCase):
    def _scrivi(self, dati: dict) -> Path:
        d = Path(tempfile.mkdtemp())
        p = d / "x.manifest.json"
        p.write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")
        return p

    def test_un_volume_senza_colophon_e_segnalato(self):
        ok, msg = dm._colophon_del_manifest(self._scrivi({"title": "T", "chapters": []}))
        self.assertFalse(ok)
        self.assertIn("anonimo", msg)

    def test_un_colophon_a_meta_dice_cosa_manca(self):
        ok, msg = dm._colophon_del_manifest(self._scrivi(
            {"title": "T", "chapters": [], "colophon": {"versione": "v1"}}))
        self.assertFalse(ok)
        for k in ("data", "autori", "licenza"):
            self.assertIn(k, msg)

    def test_un_colophon_completo_passa_e_si_riassume(self):
        ok, msg = dm._colophon_del_manifest(self._scrivi({"title": "T", "chapters": [],
            "colophon": {"edizione": "Da tavolo", "versione": "v1", "data": "oggi",
                         "autori": "G. Samuele", "licenza": "privato"}}))
        self.assertTrue(ok, msg)
        self.assertIn("G. Samuele", msg)


class TestGuasti(unittest.TestCase):
    def test_un_manifest_inesistente_esce_2_e_non_compila_niente(self):
        r = _lancia("questo-non-esiste.manifest.json")
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("schermo", r.stdout)

    def test_il_cancello_ip_viene_sempre_detto(self):
        # Non è automatizzabile e non si finge che lo sia: si dice.
        r = _lancia("--solo", "colophon",
                    str(REPO / "10-stand-alone" / "L'abbazia Della Rotta Sicura" /
                        "homebrew" / "abbazia-rotta-sicura.manifest.json"))
        self.assertIn("GUIDA-CONDIVISIONE-IP", r.stdout)
        self.assertIn("ADR-0005", r.stdout)

    def test_l_imposizione_degrada_pulito_se_manca_pdfcpu(self):
        # ADR-0027: dichiara e non fallisce. Il volume resta stampabile.
        import binari
        from unittest import mock
        mp = (REPO / "10-stand-alone" / "L'abbazia Della Rotta Sicura" /
              "homebrew" / "abbazia-rotta-sicura.manifest.json")
        with mock.patch.object(binari.shutil, "which", return_value=None):
            nome, segno, dettaglio = dm._imponi(mp)
        self.assertEqual(segno, "○")
        self.assertIn("pdfcpu assente", dettaglio)


class TestRegistrazione(unittest.TestCase):
    def test_volume_e_nel_manifest_dei_tool(self):
        # Un sottocomando che il manifest non conosce è invisibile al server MCP
        # e al registro: esiste solo per chi ha letto il codice.
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        dm_t = next(t for t in d["tools"] if t["id"] == "dm")
        self.assertIn("volume", dm_t["args"][0]["choices"])


if __name__ == "__main__":
    unittest.main()
