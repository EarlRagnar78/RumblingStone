"""Il registro delle dipendenze è una fonte sola (lotto D di QUALITA-DEL-CODICE).

Il difetto che questi test esistono per impedire non è un crash: è che la stessa
domanda — *«cosa devo avere installato?»* — torni ad avere risposte diverse a
seconda di dove la si fa. Prima del lotto D ne aveva tre che non coincidevano:

* `dm.py doctor` accettava Python 3.8, la guida di setup ne chiedeva 3.11 e la
  CI ne installa 3.11;
* `doctor` teneva una propria lista con `pandoc` e `xelatex`, che `binari.py`
  non conosceva;
* il manifest dei tool dichiarava otto binari esterni, `binari.py` due.

I test che contano qui sono quelli che **confrontano due fonti**: se qualcuno
riscrive un numero in uno dei due posti, cadono.

Solo `unittest`: la CI non installa pytest.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import binari  # noqa: E402


class TestPythonMinimo(unittest.TestCase):
    def test_e_una_coppia_di_interi(self):
        self.assertIsInstance(binari.PYTHON_MINIMO, tuple)
        self.assertTrue(all(isinstance(n, int) for n in binari.PYTHON_MINIMO))

    def test_la_CI_installa_la_versione_che_il_registro_chiede(self):
        """Il confronto fra due fonti: se divergono di nuovo, questo cade."""
        minimo = ".".join(str(n) for n in binari.PYTHON_MINIMO)
        versioni = set()
        for wf in (REPO / ".github" / "workflows").glob("*.yml"):
            versioni |= set(re.findall(r'python-version:\s*"?([\d.]+)"?',
                                       wf.read_text(encoding="utf-8")))
        self.assertTrue(versioni, "nessun workflow dichiara una versione di Python")
        for v in versioni:
            self.assertTrue(
                tuple(int(n) for n in v.split(".")) >= binari.PYTHON_MINIMO,
                f"la CI installa Python {v}, sotto il minimo {minimo} del registro")

    def test_la_guida_di_setup_dichiara_lo_stesso_minimo(self):
        guida = REPO / "docs" / "guides" / "GUIDA-SETUP-MACCHINA.md"
        testo = guida.read_text(encoding="utf-8")
        atteso = ".".join(str(n) for n in binari.PYTHON_MINIMO)
        self.assertIn(atteso, testo,
                      f"la guida non nomina Python {atteso}: le due fonti sono ripartite")

    def test_python_ok_confronta_l_interprete_col_minimo(self):
        with mock.patch.object(binari.sys, "version_info", (3, 8, 0)):
            self.assertFalse(binari.python_ok())
        with mock.patch.object(binari.sys, "version_info", (3, 11, 0)):
            self.assertTrue(binari.python_ok())


class TestRegistroCompleto(unittest.TestCase):
    def test_conosce_i_binari_che_il_manifest_dichiara(self):
        """L'altro confronto fra due fonti: il manifest e il registro."""
        m = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        tools = m["tools"] if isinstance(m, dict) and "tools" in m else m
        dichiarati = set()
        for t in tools:
            for b in t.get("external_bins") or []:
                # alcune voci descrivono come si cerca il binario, non solo il nome
                dichiarati.add(re.split(r"[ |(]", b)[0])
        noti = {b.nome for b in (*binari.TUTTI, *binari.OPZIONALI)}
        noti |= {"python3"}  # l'interprete: ha il suo campo, PYTHON_MINIMO
        mancanti = dichiarati - noti
        self.assertFalse(mancanti,
                         f"il manifest dichiara binari che il registro non conosce: {sorted(mancanti)}")

    def test_conosce_le_librerie_che_il_manifest_dichiara(self):
        m = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        tools = m["tools"] if isinstance(m, dict) and "tools" in m else m
        dichiarate = {d.lower() for t in tools for d in (t.get("external_deps") or [])}
        note = {lib.nome.lower() for lib in binari.LIBRERIE}
        self.assertFalse(dichiarate - note,
                         f"il manifest dichiara librerie che il registro non conosce: "
                         f"{sorted(dichiarate - note)}")

    def test_ogni_voce_dichiara_il_suo_ripiego(self):
        """Un ripiego dichiarato è la differenza fra opzionale e opzionale a parole."""
        for v in (*binari.TUTTI, *binari.OPZIONALI, *binari.LIBRERIE):
            with self.subTest(v.nome):
                self.assertTrue(v.ripiego.strip(), f"{v.nome} non dice cosa resta senza")
                self.assertTrue(v.installa.strip(), f"{v.nome} non dice come si installa")

    def test_i_nomi_non_si_ripetono(self):
        nomi = [v.nome for v in (*binari.TUTTI, *binari.OPZIONALI, *binari.LIBRERIE)]
        self.assertEqual(len(nomi), len(set(nomi)), f"nome duplicato nel registro: {nomi}")

    def test_solo_pyyaml_e_obbligatoria(self):
        """ADR-0037: `Pillow` degrada, `pyyaml` no. Se cambia, l'ADR va riletta."""
        obbligatorie = {lib.nome for lib in binari.LIBRERIE if lib.obbligatoria}
        self.assertEqual(obbligatorie, {"pyyaml"})


class TestCatene(unittest.TestCase):
    def test_ogni_catena_nomina_dipendenze_che_esistono(self):
        for catena, servono in binari.CATENE.items():
            for nome in servono:
                with self.subTest(catena=catena, dipendenza=nome):
                    self.assertIsNotNone(binari.per_nome(nome),
                                         f"la catena «{catena}» chiede {nome!r}, "
                                         f"che il registro non ha")

    def test_disponibile_alza_su_un_nome_inventato(self):
        with self.assertRaises(KeyError):
            binari.disponibile("nonesiste")

    def test_disponibile_risponde_per_binari_e_librerie_con_la_stessa_domanda(self):
        with mock.patch.object(binari.shutil, "which", return_value="/usr/bin/git"):
            self.assertTrue(binari.disponibile("git"))
        with mock.patch.object(binari.shutil, "which", return_value=None):
            self.assertFalse(binari.disponibile("typst"))
        self.assertIsInstance(binari.disponibile("pyyaml"), bool)

    def test_le_catene_senza_dipendenze_sono_sempre_pronte(self):
        """La sessione, i booklet HTML e le mappe SVG girano su Python nudo.

        È l'affermazione che regge tutta la regola stdlib-only (ADR-0037): se un
        giorno la catena della sessione acquistasse una dipendenza, la decisione
        andrebbe riesaminata, e questo test è dove ci si accorge.
        """
        nude = [c for c, s in binari.CATENE.items() if not s]
        self.assertIn("sessione (prep, recap, state)", nude)
        self.assertIn("mappe SVG", nude)


class TestDoctorNonHaListeProprie(unittest.TestCase):
    """Il difetto del lotto D era una lista scritta a mano dentro `doctor`."""

    def test_dm_py_non_nomina_piu_i_binari_uno_per_uno(self):
        dm = (REPO / "scripts" / "dm.py").read_text(encoding="utf-8")
        # `shutil.which("pandoc")` e simili: la lista che è stata tolta
        for nome in ("pandoc", "xelatex", "inkscape", "cwebp"):
            with self.subTest(nome):
                self.assertNotIn(f'"{nome}"', dm,
                                 f"dm.py nomina {nome!r}: la lista è tornata a "
                                 f"vivere lì invece che in binari.py")

    def test_dm_py_non_scrive_a_mano_la_soglia_di_python(self):
        dm = (REPO / "scripts" / "dm.py").read_text(encoding="utf-8")
        self.assertNotIn("(3, 8)", dm)
        self.assertIn("PYTHON_MINIMO", dm)


if __name__ == "__main__":
    unittest.main()
