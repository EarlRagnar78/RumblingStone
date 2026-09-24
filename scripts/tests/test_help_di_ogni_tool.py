"""Ogni tool dichiarato risponde a `--help`, e l'elenco non si tiene a mano.

🔴 **Lo stesso difetto e' capitato due volte, e la seconda l'ho fatto io.**

`.github/workflows/ci.yml` tiene un elenco **scritto a mano** di smoke test
`--help`. Un lotto precedente ci aveva gia' trovato **sette** tool che
dichiaravano `ci_smoke` nel manifest e che nessuno eseguiva — il commento nel
workflow lo dice ancora: *«il contratto prometteva una verifica che non
esisteva»*.

Il 2026-09-18 e' ricapitato con `misura_craft.py` e
`validate_norme_editoriali.py`: dichiaravano `ci_smoke: --help` e non erano
nell'elenco. E `misura_craft --help` **andava in crash** — argparse fa
`%`-formatting sulle stringhe di aiuto e il testo di `--spotlight` conteneva
`«no PC >40%»`. Un `--help` rotto per un giorno intero, con il contratto che
prometteva di provarlo.

⚠️ **Aggiungere due righe all'elenco non era la correzione**: l'elenco a mano
e' *la causa*, e scivola ogni volta che nasce un tool. Questo test lo deriva
dal manifest, che e' gia' la fonte di verita' (ADR-0012).
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

#: Chi **non** deve rispondere a `--help`, e perche'. Una riga qui e' una
#: scelta, come per le non-creature del Bestiario: si aggiunge di proposito.
ESENTI = {
    "blender/costruisci_mappa":
        "gira DENTRO Blender e rifiuta di partire a mano: il driver e' "
        "render_map_blender.py, dove sta la logica provabile senza GPU",
}


def _tool_python() -> "list[dict]":
    d = json.loads((ROOT / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
    return [t for t in d["tools"]
            if t.get("language") == "python" and str(t.get("path", "")).endswith(".py")]


class TestOgniToolRispondeAHelp(unittest.TestCase):
    def test_help_esce_zero(self):
        """Il cancello. Un tool nuovo che rompe `--help` diventa rosso **qui**,
        senza che nessuno debba ricordarsi di aggiungerlo a una lista."""
        for t in _tool_python():
            if t["id"] in ESENTI:
                continue
            p = ROOT / t["path"]
            if not p.exists():
                continue
            with self.subTest(tool=t["id"]):
                r = subprocess.run([sys.executable, str(p), "--help"],
                                   capture_output=True, timeout=120, cwd=ROOT)
                self.assertEqual(
                    r.returncode, 0,
                    f"{t['id']} --help esce {r.returncode}:\n"
                    + r.stderr.decode(errors="replace")[-400:])

    def test_le_esenzioni_esistono_ancora(self):
        """Un'esenzione per un tool sparito e' una riga che mente: si toglie."""
        noti = {t["id"] for t in _tool_python()}
        fantasmi = sorted(set(ESENTI) - noti)
        self.assertEqual(fantasmi, [],
                         f"esenzioni per tool che non esistono piu': {fantasmi}")

    def test_ogni_esenzione_porta_la_ragione(self):
        for nome, ragione in ESENTI.items():
            with self.subTest(tool=nome):
                self.assertGreater(len(ragione), 30,
                                   "un'esenzione senza una ragione scritta e' "
                                   "una dimenticanza con un nome")


class TestIlContrattoNonPromettePiuDiQuelCheProva(unittest.TestCase):
    """⚠️ La forma d'errore che ha reso possibile il crash: il manifest
    dichiarava `ci_smoke` e **nessuno lo eseguiva**."""

    def test_chi_dichiara_uno_smoke_help_e_coperto_da_questo_test(self):
        scoperti = []
        for t in _tool_python():
            smoke = (t.get("ci_smoke") or "")
            if "--help" in smoke and t["id"] in ESENTI:
                scoperti.append(t["id"])
        self.assertEqual(scoperti, [],
                         "un tool dichiara uno smoke `--help` ed e' esente dal "
                         f"test che lo prova: {scoperti}")


if __name__ == "__main__":
    unittest.main()
