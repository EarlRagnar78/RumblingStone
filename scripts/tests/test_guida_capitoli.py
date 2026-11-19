"""La guida ai capitoli nasce dal manifest (2026-11-19).

Il booklet della serata di ARC-07 stampava, nell'introduzione condivisa con il
booklet lungo, la tabella «Come usare questo booklet» del booklet lungo:
«V · La cassetta del DM», «VIII · Durik», mentre nella serata il V era l'Atto
II e Durik il XII. Una tabella scritta a mano si guasta al primo riordino;
quella che il manifest genera no.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from dmcore import testo  # noqa: E402

INTRO = """Prima.

<!-- guida-capitoli -->
| Capitolo | Per chi | Quando |
|---|---|---|
| V · La cassetta del DM | ⚠ DM | vecchia |
<!-- /guida-capitoli -->

Dopo.
"""


class TestGuida(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.base = Path(self.dir.name)
        (self.base / "intro.md").write_text(INTRO, encoding="utf-8")
        for f in ("a.md", "b.md"):
            (self.base / f).write_text("# x\n", encoding="utf-8")

    def tearDown(self):
        self.dir.cleanup()

    def leggi(self, manifest):
        cap = testo.capitoli_del_volume(self.base, manifest)
        return testo.leggi_per_la_stampa(self.base / "intro.md", cap)

    def test_il_manifest_scrive_la_guida(self):
        md = self.leggi({"chapters": [
            {"title": "I · Regia", "file": "a.md", "tag": "dm", "quando": "prima di tutto"},
            {"title": "II · Durik", "file": "b.md", "tag": "player", "quando": "accanto a Hella"},
        ], "guida_righe_finali": [["Il volume dei giocatori", "✉", "gli echi"]]})
        self.assertIn("| I · Regia | ⚠ DM | prima di tutto |", md)
        self.assertIn("| II · Durik | ✉ | accanto a Hella |", md)
        self.assertIn("| Il volume dei giocatori | ✉ | gli echi |", md)
        self.assertNotIn("La cassetta", md)
        self.assertNotIn("guida-capitoli", md)
        self.assertTrue(md.startswith("Prima.") and md.rstrip().endswith("Dopo."))

    def test_senza_quando_resta_la_tabella_scritta(self):
        md = self.leggi({"chapters": [{"title": "I · Regia", "file": "a.md"}]})
        self.assertIn("| V · La cassetta del DM | ⚠ DM | vecchia |", md)
        self.assertNotIn("guida-capitoli", md)


if __name__ == "__main__":
    unittest.main()


class TestProfonditaDellIndice(unittest.TestCase):
    """L'indice del volume d'arco di ARC-07 era di otto pagine (pp. 3-10): un
    AP Paizo lo stampa in una. `indice_profondita` sceglie quanti livelli."""

    def test_la_chiave_arriva_al_tema(self):
        import export_booklet_typst as ebt
        testa = "\n".join(ebt.intestazione({"title": "x", "chapters": [], "indice_profondita": 1}))
        self.assertIn("indice-profondita: 1", testa)

    def test_senza_chiave_resta_il_tema(self):
        import export_booklet_typst as ebt
        self.assertNotIn("indice-profondita", "\n".join(ebt.intestazione({"title": "x", "chapters": []})))

    def test_il_tema_la_usa(self):
        tema = (Path(__file__).resolve().parents[2] / "scripts/typst/tema-rumblingstone.typ").read_text(encoding="utf-8")
        self.assertIn("depth: indice-profondita", tema)
