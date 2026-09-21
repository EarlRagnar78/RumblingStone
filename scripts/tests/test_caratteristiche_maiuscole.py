"""La norma WotC sulle maiuscole, provata all'indietro.

Il punto di queste prove non e' che il controllo passi: e' che **distingua**.
La ragione per cui la norma era stata archiviata come non misurabile e' che
*forza* e' anche un sostantivo comune, e un rilevatore che lo ignora segnala
piu' rumore che errori. Quindi meta' delle prove verifica che il controllo
**taccia** dove deve tacere.

⚠️ `unittest`, non pytest: la CI gira `python -m unittest discover` e pytest
non e' installato (ADR-0037).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_prosa.py"


class TestCaratteristicheMaiuscole(unittest.TestCase):

    def corri(self, testo: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "prova.md"
            f.write_text(testo, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), "--caratteristiche", str(f)],
                capture_output=True, text=True, cwd=ROOT)

    def assertSegnala(self, testo: str, atteso: str = "") -> None:
        r = self.corri(testo)
        self.assertEqual(r.returncode, 1, f"doveva segnalare:\n{r.stdout}")
        if atteso:
            self.assertIn(atteso, r.stdout)

    def assertTace(self, testo: str) -> None:
        r = self.corri(testo)
        self.assertEqual(r.returncode, 0, f"doveva tacere:\n{r.stdout}")

    # ── quello che DEVE segnalare ────────────────────────────────────────

    def test_prova_minuscola_con_una_cd(self):
        self.assertSegnala("Il nano tenta una prova di forza, CD 18, per sollevarlo.\n",
                           "prova di forza")

    def test_abilita_col_modificatore_minuscola(self):
        self.assertSegnala("**Abilita**: nuotare +9, Scalare +6\n", "nuotare +9")

    def test_punteggio_di_caratteristica_minuscolo(self):
        self.assertSegnala("| forza 25 | Des 14 |\n")

    def test_bonus_di_caratteristica_minuscolo(self):
        self.assertSegnala("- CA 15 (bonus di destrezza +2)\n")

    # ── quello che deve TACERE, ed e' il motivo per cui la norma esiste ──

    def test_il_sostantivo_comune_non_conta(self):
        """2.014 occorrenze nude nel repo: se queste passano, il controllo e' morto."""
        self.assertTace("La forza dell'orda era nella sua destrezza di manovra,\n"
                        "e il carisma del capitano teneva insieme la saggezza dei vecchi.\n")

    def test_prova_senza_una_cd_non_conta(self):
        """«prove di saggezza e spiritualita'» e' una descrizione, non un tiro."""
        self.assertTace("Ambientazione: antica foresta sacra, prove di saggezza "
                        "e spiritualita'.\n")

    def test_lo_spazio_dopo_il_segno_non_conta(self):
        """Il falso positivo vero: «40.500 mo in oggetti di artigianato + 1 Sacrificio»."""
        self.assertTace("**Costo:** 40.500 mo in oggetti di artigianato + 1 "
                        "Sacrificio Personale.\n")

    def test_il_bonus_di_intuizione_non_e_un_abilita(self):
        """In 3.5 «intuizione» e' un TIPO di bonus; l'abilita' e' Percepire Intenzioni."""
        self.assertTace("Concede un bonus di intuizione +4 alle prove di Artigianato.\n")

    def test_la_forma_corretta_passa(self):
        self.assertTace("Prova di Forza CD 25; **Nuotare** +9; bonus di Destrezza +3; "
                        "For 25.\n")

    # ── il repo vero ─────────────────────────────────────────────────────

    def test_il_repo_e_a_zero(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--caratteristiche"],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_gli_archivi_sono_fuori(self):
        """Il passo 3 della sesta regola: `_SNAPSHOT-STORICO.md` esclude la cartella."""
        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_prosa as vp

        snapshot = {p.parent for p in ROOT.rglob("_SNAPSHOT-STORICO.md")}
        self.assertTrue(snapshot, "il repo non ha piu' nessuno snapshot dichiarato")
        for f in vp.file_di_gioco():
            self.assertFalse(any(s in f.parents for s in snapshot), f)
            self.assertNotIn("_ARCHIVIO", f.parts, f)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
