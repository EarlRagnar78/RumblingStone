"""`dm.py prosa`: la catena della prosa da un solo ingresso (ADR-0101).

Come `dm.py bestiario`, il sottocomando non ha logica: passa gli argomenti allo
script. Si prova che non si metta in mezzo (l'aiuto è quello dello script, il
codice d'uscita arriva a chi chiama) e che ogni script della catena sia nel
manifest, così il server MCP e il registro lo vedono.
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
    return "\n".join(r for r in testo.splitlines() if not r.startswith("[dm] → "))


#: Il contratto di ADR-0101, scritto qui e non letto da `dm.PROSA`: l'ordine
#: conta, perché `dm.py prosa` senza azione è il promemoria della catena.
CONTRATTO = {
    "misura": "misura_craft.py",
    "ciclo": "ciclo_prosa.py",
    "mqm": "punteggio_mqm.py",
    "sintassi": "misura_sintassi.py",
    "coerenza": "coerenza_campagna.py",
    "domande": "domande_developer.py",
    "migliora": "migliora_prosa.py",
    "cieco": "cieco_versioni.py",
    "banco": "banco_prosa_locale.py",
    "voto": "voto_scrittura.py",
}


class TestLaCatena(unittest.TestCase):
    def test_le_azioni_e_il_loro_ordine_sono_quelli_dell_adr(self):
        self.assertEqual(list(dm.PROSA.items()), list(CONTRATTO.items()))

    def test_ogni_azione_da_l_aiuto_del_suo_script(self):
        for azione, script in CONTRATTO.items():
            with self.subTest(azione=azione):
                diretto = _esegui(f"scripts/{script}", "--help")
                via_dm = _esegui("scripts/dm.py", "prosa", azione, "--help")
                self.assertEqual(via_dm.returncode, diretto.returncode)
                self.assertEqual(_senza_freccia(via_dm.stdout), diretto.stdout.rstrip("\n"))

    def test_senza_azione_elenca_la_catena_ed_esce_2(self):
        r = _esegui("scripts/dm.py", "prosa")
        self.assertEqual(r.returncode, 2)
        posizioni = [r.stdout.index(f"{a} ") for a in CONTRATTO]
        self.assertEqual(posizioni, sorted(posizioni))

    def test_il_codice_d_uscita_passa(self):
        # un file che non esiste: lo script esce diverso da 0, e dm.py con lui
        diretto = _esegui("scripts/misura_craft.py", "non-esiste.md")
        via_dm = _esegui("scripts/dm.py", "prosa", "misura", "non-esiste.md")
        self.assertNotEqual(diretto.returncode, 0)
        self.assertEqual(via_dm.returncode, diretto.returncode)


class TestRegistrazione(unittest.TestCase):
    def test_ogni_script_esiste_ed_e_nel_manifest(self):
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        percorsi = {t["path"] for t in d["tools"]}
        for script in dm.PROSA.values():
            with self.subTest(script=script):
                self.assertTrue((REPO / "scripts" / script).exists())
                self.assertIn(f"scripts/{script}", percorsi)

    def test_prosa_e_nel_manifest_dei_tool(self):
        d = json.loads((REPO / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        dm_t = next(t for t in d["tools"] if t["id"] == "dm")
        self.assertIn("prosa", dm_t["args"][0]["choices"])


if __name__ == "__main__":
    unittest.main()
