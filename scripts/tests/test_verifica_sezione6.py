"""Il cancello che esegue i comandi citati da §6.2 — provato dai due lati.

🔴 **Questo strumento esegue comandi che stanno in un file Markdown**, quindi
meta' di queste prove non riguarda gli esiti: riguarda **cosa si rifiuta di
eseguire**. Un cancello del genere sbagliato e' peggio di nessun cancello.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import verifica_sezione6 as v6  # noqa: E402


class TestNonEsegueQualunqueCosa(unittest.TestCase):
    """La meta' che conta: l'allowlist e la forma rigida."""

    def test_rifiuta_i_metacaratteri_di_shell(self):
        for veleno in (
            "`python3 scripts/misura_craft.py --p1; rm -rf /`",
            "`python3 scripts/misura_craft.py --p1 && curl http://x`",
            "`python3 scripts/misura_craft.py --p1 | sh`",
            "`python3 scripts/misura_craft.py $(whoami)`",
            "`python3 scripts/misura_craft.py --p1 > /etc/passwd`",
            "`bash -c 'echo pwned'`",
            "`rm -rf /`",
        ):
            with self.subTest(veleno=veleno):
                for argv in v6._comandi(veleno):
                    self.assertNotIn(";", " ".join(argv))
                    self.assertNotIn("|", " ".join(argv))
                    self.assertNotIn("&", " ".join(argv))
                    self.assertNotIn("$", " ".join(argv))
                    self.assertNotIn(">", " ".join(argv))
                    for pezzo in argv[2:]:
                        self.assertTrue(pezzo.startswith("--"), pezzo)

    def test_rifiuta_uno_script_fuori_allowlist(self):
        self.assertEqual(v6._comandi("`python3 scripts/dm.py session`"), [])
        self.assertEqual(v6._comandi("`python3 scripts/inesistente.py`"), [])

    def test_accetta_la_forma_buona(self):
        argv = v6._comandi("`python3 scripts/misura_craft.py --p1`")
        self.assertEqual(len(argv), 1)
        self.assertEqual(argv[0][1:], ["scripts/misura_craft.py", "--p1"])

    def test_ogni_script_dell_allowlist_esiste(self):
        """ADR-0053: un nome nell'allowlist che non e' un file sembra un
        presidio e non lo e'."""
        for nome in v6.CONSENTITI:
            self.assertTrue((ROOT / "scripts" / nome).exists(), nome)

    def test_non_usa_la_shell(self):
        sorgente = (ROOT / "scripts" / "verifica_sezione6.py").read_text(encoding="utf-8")
        self.assertIn("shell=False", sorgente)
        self.assertNotIn("shell=True", sorgente)
        self.assertIn("timeout=", sorgente)


class TestLeggeLaTabella(unittest.TestCase):
    def test_trova_le_righe_di_62(self):
        righe = v6.righe_di_62()
        self.assertGreaterEqual(len(righe), 4)
        for r in righe:
            self.assertIn(r["stato"], ("aperto", "chiuso", "altro"))

    def test_si_ferma_alla_sezione_successiva(self):
        """§6.2-bis e §6.3 non sono §6.2: se il parser le inghiottisse,
        eseguirebbe comandi citati in un discorso, non in un elenco."""
        for r in v6.righe_di_62():
            self.assertNotIn("Rituale 4", r["lotto"])


class TestIlCancelloMorde(unittest.TestCase):
    def test_oggi_e_verde(self):
        errori, _ = v6.verifica()
        self.assertEqual(errori, [], errori)

    def test_un_aperto_con_il_cancello_verde_boccia(self):
        """🐛 Il difetto dei «27 ADR mancanti»: una riga ⬜ accanto a un
        comando che dice zero."""
        vere = v6.righe_di_62
        finte = [dict(r, stato="aperto") for r in vere()
                 if "27 ADR" in r["lotto"] or "ADR mancanti" in r["cella"]]
        self.assertTrue(finte, "la riga dei 27 ADR non e' piu' in §6.2")
        try:
            v6.righe_di_62 = lambda: finte
            errori, _ = v6.verifica()
        finally:
            v6.righe_di_62 = vere
        self.assertTrue(any("verde" in e for e in errori), errori)

    def test_una_misura_senza_attesa_boccia(self):
        vere = v6.righe_di_62
        finte = [{"stato": "chiuso", "lotto": "finto", "cella": "",
                  "attese": [], "comandi": [[sys.executable,
                                             "scripts/misura_craft.py", "--p1"]]}]
        try:
            v6.righe_di_62 = lambda: finte
            errori, _ = v6.verifica()
        finally:
            v6.righe_di_62 = vere
        self.assertTrue(any("senza dichiarare" in e for e in errori), errori)

    def test_un_numero_invecchiato_boccia(self):
        vere = v6.righe_di_62
        finte = [{"stato": "chiuso", "lotto": "finto", "cella": "",
                  "attese": ["9999 box su 477"],
                  "comandi": [[sys.executable, "scripts/misura_craft.py", "--p1"]]}]
        try:
            v6.righe_di_62 = lambda: finte
            errori, _ = v6.verifica()
        finally:
            v6.righe_di_62 = vere
        self.assertTrue(any("invecchiato" in e for e in errori), errori)

    def test_un_avviso_non_conta_come_pulito(self):
        """🐛 Il falso positivo del primo giro: `--tetto-el` stampa `✓ nessuno
        sforamento` **e** `⚠ ZERO incontri marcati`. E' verde **a vuoto**, e la
        riga ⬜ accanto dice il vero."""
        self.assertEqual(v6._specie("✓ tutto ok"), "cancello")
        righe = [r for r in v6.righe_di_62() if r["stato"] == "aperto"
                 and any("validate_modules" in " ".join(c) for c in r["comandi"])]
        if righe:
            errori, _ = v6.verifica()
            self.assertFalse([e for e in errori if "M1-M3" in e], errori)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
