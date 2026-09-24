"""`suggest_encounter --con-generatore`: il catalogo più quello che non c'è.

Il DM: *«generate encounter prende dal bestiario esistente ma con un'opzione
prende anche in parte dal generatore, in modo che gli incontri siano sempre
diversi».*

Due cose vanno tenute vere insieme, e sono in tensione:

  * l'opzione deve **funzionare davvero** — dodici candidati generati messi in un
    pool di 308 record non escono quasi mai, e un'opzione che sembra accesa senza
    esserlo è il modo peggiore di sbagliare, perché non si vede;
  * l'opzione **spenta** non deve cambiare niente — chi non la usa deve ottenere
    esattamente quello che otteneva prima, seed compreso.
"""
from __future__ import annotations

import io
import random
import re
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import suggest_encounter as S  # noqa: E402


def _esegui(*argv: str) -> str:
    fuori = subprocess.run([sys.executable, str(ROOT / "scripts/suggest_encounter.py"),
                            *argv], capture_output=True, text=True, cwd=ROOT)
    return fuori.stdout


class LOpzioneFunzionaDavvero(unittest.TestCase):
    def test_una_creatura_generata_entra_in_ogni_proposta(self):
        """Metterle solo nel pool non bastava: annegavano fra 308 record."""
        testo = _esegui("--el", "9", "--con-generatore", "--count", "3", "--seed", "11")
        proposte = testo.split("### Proposal ")[1:]
        self.assertEqual(len(proposte), 3)
        for i, p in enumerate(proposte, 1):
            with self.subTest(proposta=i):
                self.assertIn("(generato)", p.split("- **Total units**")[0])

    def test_il_resto_viene_dal_bestiario(self):
        """«In parte dal generatore»: in parte, non tutto."""
        testo = _esegui("--el", "9", "--con-generatore", "--count", "2", "--seed", "11")
        prima = testo.split("## Le creature generate")[0]
        righe = [r for r in prima.splitlines() if r.startswith("| ") and "CR" not in r]
        veri = [r for r in righe if "generato — non è nel Bestiario" not in r]
        self.assertTrue(veri, "un incontro tutto generato non è quello che serve")

    def test_i_blocchi_sono_stampati_per_intero(self):
        """Un nome e un GS in tabella non si portano al tavolo."""
        testo = _esegui("--el", "9", "--con-generatore", "--count", "2", "--seed", "11")
        self.assertIn("## Le creature generate", testo)
        self.assertIn("```statblocco", testo)
        self.assertIn("Il conto", testo)

    def test_dice_che_non_stanno_nel_bestiario(self):
        testo = _esegui("--el", "9", "--con-generatore", "--count", "1", "--seed", "3")
        self.assertIn("non è nel Bestiario", testo)
        self.assertIn("ADR-0034", testo)

    def test_piu_cattivi_tocca_solo_i_generati(self):
        testo = _esegui("--el", "9", "--con-generatore", "--piu-cattivi",
                        "--count", "1", "--seed", "4")
        self.assertIn("Advanced", testo)
        self.assertIn("piu' duri" if "piu' duri" in testo else "più duri", testo)
        blocchi = testo.split("## Le creature generate")[1]
        self.assertIn("SENZA alzare il GS", blocchi)


class LOpzioneSpentaNonCambiaNiente(unittest.TestCase):
    def test_senza_il_flag_nessun_generato(self):
        testo = _esegui("--el", "9", "--count", "3", "--seed", "11")
        self.assertNotIn("(generato)", testo)
        self.assertNotIn("Le creature generate", testo)

    def test_lo_stesso_seed_da_lo_stesso_incontro(self):
        a = _esegui("--el", "9", "--con-generatore", "--count", "3", "--seed", "7")
        b = _esegui("--el", "9", "--con-generatore", "--count", "3", "--seed", "7")
        self.assertEqual(a, b)

    def test_seed_diversi_danno_incontri_diversi(self):
        a = _esegui("--el", "9", "--con-generatore", "--count", "3", "--seed", "7")
        b = _esegui("--el", "9", "--con-generatore", "--count", "3", "--seed", "8")
        self.assertNotEqual(a, b)


class IlPoolResta(unittest.TestCase):
    def test_i_generati_hanno_la_forma_dei_record_del_catalogo(self):
        """Se non ce l'hanno, `filter_pool` li scarta e l'opzione non fa nulla."""
        rng = random.Random(1)
        generati = S.candidati_generati(9, rng, False, "cave", ["red-hand"])
        self.assertTrue(generati)
        for m in generati:
            with self.subTest(nome=m["name"]):
                for chiave in ("name", "cr", "faction", "role", "environment",
                               "source_file", "statblocco"):
                    self.assertIn(chiave, m)
                self.assertIsInstance(m["cr"], float)
                self.assertTrue(m["generato"])

    def test_sopravvivono_al_filtro(self):
        """Il difetto che questo previene: la fazione sbagliata e il pool torna
        quello di prima, senza che nessuno se ne accorga."""
        rng = random.Random(1)
        generati = S.candidati_generati(9, rng, False, "cave", ["red-hand"])
        rimasti = S.filter_pool(generati, "cave", ["red-hand"], None)
        self.assertEqual(len(rimasti), len(generati))

    def test_coprono_la_fascia_che_il_costruttore_cerca(self):
        """Le strategie di composizione pescano da EL−5 a EL."""
        rng = random.Random(1)
        gs = {m["cr"] for m in S.candidati_generati(9, rng, False, "any", [])}
        self.assertLessEqual(min(gs), 4.0)
        self.assertGreaterEqual(max(gs), 9.0)

    def test_non_sommergono_il_catalogo(self):
        """Devono affiancare i 306 record veri, non sostituirli."""
        rng = random.Random(1)
        generati = S.candidati_generati(13, rng, False, "any", [])
        self.assertLess(len(generati), 30, "il condimento, non il piatto")


if __name__ == "__main__":
    unittest.main()
