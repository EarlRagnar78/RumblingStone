"""I pacchetti Typst vendorizzati esistono, sono coerenti, e compilano offline.

Il vendoring (ADR-0026) serve a una cosa sola: **la build non scarica niente**.
Il modo in cui si rompe non è un errore rumoroso — è che qualcuno cancella una
cartella «di roba generata», e la catena di stampa torna silenziosamente a
dipendere da `packages.typst.org` finché non c'è una macchina offline o il
pacchetto non cambia sotto i piedi. Questi test sono lì per quel giorno.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import typst_motore  # noqa: E402  (ADR-0116)
PACCHETTI = REPO / "scripts" / "typst" / "packages"

# Quelli che la catena importa davvero. La lista sta qui e non si deduce dal
# disco: un test che si adatta a ciò che trova non è un test.
ATTESI = (("preview", "droplet", "0.3.1"), ("preview", "in-dexter", "0.7.2"))


class TestPresenza(unittest.TestCase):
    def test_ogni_pacchetto_atteso_c_e(self):
        for ns, nome, ver in ATTESI:
            d = PACCHETTI / ns / nome / ver
            self.assertTrue(d.is_dir(), f"pacchetto vendorizzato mancante: {d}")

    def test_ogni_pacchetto_ha_typst_toml_ed_entrypoint(self):
        for ns, nome, ver in ATTESI:
            d = PACCHETTI / ns / nome / ver
            toml = d / "typst.toml"
            self.assertTrue(toml.is_file(), f"{nome}: manca typst.toml")
            testo = toml.read_text(encoding="utf-8")
            m = re.search(r'^entrypoint\s*=\s*"([^"]+)"', testo, re.M)
            self.assertIsNotNone(m, f"{nome}: typst.toml senza entrypoint")
            self.assertTrue((d / m.group(1)).is_file(),
                            f"{nome}: entrypoint {m.group(1)} non esiste")

    def test_la_versione_dichiarata_e_quella_della_cartella(self):
        # Copiare una versione nuova nella cartella vecchia è l'errore facile:
        # l'import continua a dire 0.3.1 e il codice è un altro.
        for ns, nome, ver in ATTESI:
            toml = (PACCHETTI / ns / nome / ver / "typst.toml").read_text(encoding="utf-8")
            m = re.search(r'^version\s*=\s*"([^"]+)"', toml, re.M)
            self.assertEqual(m.group(1), ver, f"{nome}: cartella {ver}, typst.toml {m.group(1)}")

    def test_la_licenza_e_ancora_li(self):
        # È la condizione per cui abbiamo il diritto di tenerli nel repo.
        for ns, nome, ver in ATTESI:
            lic = PACCHETTI / ns / nome / ver / "LICENSE"
            self.assertTrue(lic.is_file(), f"{nome}: LICENSE rimosso dal pacchetto vendorizzato")
            self.assertGreater(len(lic.read_text(encoding="utf-8")), 200, f"{nome}: LICENSE svuotato")

    def test_il_readme_dichiara_ogni_pacchetto(self):
        testo = (PACCHETTI / "README.md").read_text(encoding="utf-8")
        for _, nome, ver in ATTESI:
            self.assertIn(f"`{nome}`", testo, f"{nome} non è nella tabella del README")
            self.assertIn(ver, testo, f"la versione {ver} di {nome} non è nel README")


class TestCatena(unittest.TestCase):
    def test_l_exporter_passa_il_percorso_dei_pacchetti(self):
        # Senza questo, `typst` va in rete e il vendoring è decorazione.
        src = (REPO / "scripts" / "export_booklet_typst.py").read_text(encoding="utf-8")
        self.assertIn("pacchetti=PACCHETTI", src)
        # ADR-0116: il motore lo passa a entrambe le vie, il modulo e la CLI.
        motore = (REPO / "scripts" / "typst_motore.py").read_text(encoding="utf-8")
        self.assertIn("--package-path", motore)
        self.assertIn("package_path=", motore)
        self.assertIn('PACCHETTI = ROOT / "scripts" / "typst" / "packages"', src)


@unittest.skipIf(not typst_motore.disponibile(), "typst non installato")
class TestCompilazione(unittest.TestCase):
    def test_compila_senza_rete(self):
        doc = (
            '#import "@preview/droplet:0.3.1": dropcap\n'
            '#import "@preview/in-dexter:0.7.2": index, make-index\n'
            "#set page(width: 12cm, height: 8cm)\n"
            "#dropcap(height: 2, gap: 4pt)[Pietra che si assesta attorno a ossa "
            "care #index[Forgia], come una mano che si chiude piano per "
            "proteggere, non per stringere, nel buio verde.]\n"
            "#make-index()\n"
        )
        with tempfile.TemporaryDirectory() as d:
            typ, pdf = Path(d) / "p.typ", Path(d) / "p.pdf"
            typ.write_text(doc, encoding="utf-8")
            # Con il motore della catena (ADR-0116), in un processo senza proxy
            # e senza rete: se typst prova a scaricare un pacchetto, fallisce.
            codice = ("import sys; sys.path.insert(0, sys.argv[1]); import typst_motore as t; "
                      "from pathlib import Path as P; "
                      "e = t.compila(P(sys.argv[2]), P(sys.argv[3]), root=P(sys.argv[4]), "
                      "font=P(sys.argv[1]) / 'fonts', pacchetti=P(sys.argv[5])); "
                      "print(e.errore, file=sys.stderr); sys.exit(0 if e.ok else 1)")
            ambiente = {"PATH": "/usr/bin:/bin:/usr/local/bin:/root/.local/bin", "HOME": d}
            if "RUMBLINGSTONE_TYPST" in os.environ:
                ambiente["RUMBLINGSTONE_TYPST"] = os.environ["RUMBLINGSTONE_TYPST"]
            esito = subprocess.run(
                [sys.executable, "-c", codice, str(REPO / "scripts"), str(typ), str(pdf), d, str(PACCHETTI)],
                capture_output=True, text=True, env=ambiente,
            )
            self.assertEqual(esito.returncode, 0, esito.stderr)
            self.assertTrue(pdf.is_file())
            self.assertGreater(pdf.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
