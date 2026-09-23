"""`dm.py bestiario`: i cinque script delle creature da un solo ingresso.

`PIANO-QUALITA-DEL-CODICE` §8, sotto-lotto E9 (D3 decisa dal DM: si fa).

Il sottocomando non ha logica: passa gli argomenti allo script. Quindi la cosa
da provare è che non si metta in mezzo. Per ogni azione `--help` deve dare
l'aiuto dello script, non quello di `dm.py`, e il codice d'uscita dello script
deve arrivare a chi ha chiamato `dm.py`.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import dm  # noqa: E402


def _esegui(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=REPO)


def _senza_freccia(testo: str) -> str:
    """`dm.py` stampa una riga «[dm] → script …» prima di lanciare: il resto è dello script."""
    return "\n".join(r for r in testo.splitlines() if not r.startswith("[dm] → "))


#: Il contratto di E9, scritto qui e non letto da `dm.BESTIARIO`: se il test
#: leggesse la mappa dal modulo, un'azione mandata allo script sbagliato
#: cambierebbe tutte e due le parti del confronto e passerebbe.
CONTRATTO = {
    "estrai": "extract_statblocks.py",
    "deriva": "derive_statblocks.py",
    "attributi": "genera_attributi.py",
    "creatura": "genera_creatura.py",
    "conformita": "conformita_statblocchi.py",
}


class TestLAiutoEQuelloDelloScript(unittest.TestCase):
    def test_le_azioni_sono_quelle_del_piano(self):
        self.assertEqual(dm.BESTIARIO, CONTRATTO)

    def test_ogni_azione_da_l_aiuto_del_suo_script(self):
        for azione, script in CONTRATTO.items():
            with self.subTest(azione=azione):
                diretto = _esegui(f"scripts/{script}", "--help")
                via_dm = _esegui("scripts/dm.py", "bestiario", azione, "--help")
                self.assertEqual(via_dm.returncode, diretto.returncode)
                self.assertEqual(_senza_freccia(via_dm.stdout), diretto.stdout.rstrip("\n"))
                self.assertIn(f"usage: {script}", via_dm.stdout)

    def test_anche_la_forma_corta(self):
        via_dm = _esegui("scripts/dm.py", "bestiario", "creatura", "-h")
        self.assertIn("usage: genera_creatura.py", via_dm.stdout)


class TestIlCodiceDUscitaPassa(unittest.TestCase):
    def test_un_errore_dello_script_arriva_a_chi_chiama(self):
        # un ruolo che non esiste: genera_creatura esce 2, e dm.py con lui
        diretto = _esegui("scripts/genera_creatura.py", "--gs", "3", "--ruolo", "nessuno")
        via_dm = _esegui("scripts/dm.py", "bestiario", "creatura", "--gs", "3", "--ruolo", "nessuno")
        self.assertNotEqual(diretto.returncode, 0)
        self.assertEqual(via_dm.returncode, diretto.returncode)

    def test_i_flag_e_i_file_passano(self):
        via_dm = _esegui("scripts/dm.py", "bestiario", "creatura",
                         "--gs", "3", "--ruolo", "bruto", "--seed", "1")
        diretto = _esegui("scripts/genera_creatura.py", "--gs", "3", "--ruolo", "bruto", "--seed", "1")
        self.assertEqual(via_dm.returncode, 0)
        self.assertEqual(_senza_freccia(via_dm.stdout), diretto.stdout.rstrip("\n"))

    def test_senza_azione_elenca_le_azioni_ed_esce_2(self):
        r = _esegui("scripts/dm.py", "bestiario")
        self.assertEqual(r.returncode, 2)
        for azione, script in dm.BESTIARIO.items():
            self.assertIn(azione, r.stdout)
            self.assertIn(script, r.stdout)


class TestRegistrazione(unittest.TestCase):
    def test_ogni_script_esiste_ed_e_nel_manifest(self):
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        percorsi = {t["path"] for t in d["tools"]}
        for script in dm.BESTIARIO.values():
            with self.subTest(script=script):
                self.assertTrue((REPO / "scripts" / script).exists())
                self.assertIn(f"scripts/{script}", percorsi)

    def test_bestiario_e_nel_manifest_dei_tool(self):
        # come `volume`: un sottocomando che il manifest non conosce è invisibile
        # al server MCP e al registro
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        dm_t = next(t for t in d["tools"] if t["id"] == "dm")
        self.assertIn("bestiario", dm_t["args"][0]["choices"])


if __name__ == "__main__":
    unittest.main()
