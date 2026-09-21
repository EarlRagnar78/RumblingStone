"""La sesta regola d'oro, provata all'indietro.

Un cancello che non si e' mai visto bocciare non e' un cancello: e' una
speranza con un exit code. Queste prove lo fanno bocciare apposta, e poi
verificano che i quattro passi non siano vuoti sul repo vero.

⚠️ `unittest`, non funzioni nude: la CI gira `python -m unittest discover`, che
importa il modulo ma **non esegue** una funzione fuori da una TestCase. La
prima stesura era fatta di funzioni nude e in CI girava a vuoto — lo stesso
difetto silenzioso che questa regola esiste per prevenire.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FASE1 = ROOT / "scripts" / "fase1.py"


class TestFase1(unittest.TestCase):

    def corri(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(FASE1), *args],
                              capture_output=True, text=True, cwd=ROOT)

    def test_su_un_file_vivo_esce_zero(self):
        r = self.corri("--check", "plans/INDEX.md")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_su_un_archivio_dichiarato_morde(self):
        """Il difetto vero del 2026-09-20: nove box contati dentro uno snapshot."""
        snap = next(ROOT.rglob("_SNAPSHOT-STORICO.md"), None)
        self.assertIsNotNone(snap, "il repo non ha piu' nessuno snapshot dichiarato")
        bersaglio = next(f for f in sorted(snap.parent.glob("*.md"))
                         if f.name != "_SNAPSHOT-STORICO.md")
        r = self.corri("--check", str(bersaglio.relative_to(ROOT)))
        self.assertEqual(r.returncode, 1, "un archivio dichiarato deve far uscire 1")
        self.assertIn("archivi dichiarati", r.stdout)

    def test_un_modello_che_non_pesca_niente_e_rumoroso(self):
        """La lezione di `misura_craft.espandi`: uno zero muto e' peggio di un errore."""
        r = self.corri("cartella-che-non-esiste/**/*.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("non pesca niente", r.stdout + r.stderr)

    def test_i_quattro_passi_ci_sono_tutti(self):
        r = self.corri("plans/INDEX.md")
        for passo in ("1 · IL REGISTRO DELLE NORME",
                      "2 · L'ALGORITMO A STRATI",
                      "3 · I DATI CHE IL REPO GIA' POSSIEDE",
                      "4 · LE MISURE DI OGGI"):
            self.assertIn(passo, r.stdout, f"passo mancante: {passo}")

    def test_nessun_passo_torna_vuoto_sul_repo_vero(self):
        """Un passo vuoto e' un bersaglio che nessun dato del repo conosce."""
        r = self.corri("07_il Portale Della Forgia Eterna/ARC07-DEF-4-*.md")
        self.assertIn("con un misuratore vero", r.stdout)
        self.assertIn("Nomi propri della campagna: **3", r.stdout,
                      "il registro dei nomi si e' svuotato")
        self.assertIn("box read-aloud", r.stdout)
        self.assertIn("L0 · CANONE", r.stdout)

    def test_le_tre_fonti_della_misura_portano_il_loro_stato(self):
        """Un meccanismo che punta a un file inesistente deve dirlo."""
        r = self.corri("plans/INDEX.md")
        self.assertIn("Le tre fonti della misura", r.stdout)
        self.assertIn("🔵 pianificato, NON esiste", r.stdout,
                      "punteggio_mqm.py esiste ora? allora aggiorna questa prova")

    def test_riconosce_il_registro_di_chi_legge(self):
        """ADR-0035: un bersaglio misto dichiara che sono due lotti, non uno."""
        r = self.corri("plans/INDEX.md",
                       "07_il Portale Della Forgia Eterna/ARC07-DEF-4-*.md")
        self.assertIn("parlano al TAVOLO", r.stdout)
        self.assertIn("parlano al REPO", r.stdout)
        self.assertIn("due lotti", r.stdout)

    def test_la_sesta_regola_nomina_un_comando_che_esiste(self):
        """ADR-0053 applicata ad `AGENTS.md`: un rimando inventato e' un difetto."""
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("scripts/fase1.py", agents,
                      "la sesta regola non nomina il suo comando")
        self.assertTrue(FASE1.exists())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
