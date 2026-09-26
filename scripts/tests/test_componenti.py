"""componenti: l'indice, l'apparato generato e le copie sincronizzate (ADR-0074).

I casi vengono dalla prima esecuzione su DEF-4: 13 CD su 43 perse dalla regex
sulle maiuscole, un nome di prova andato a capo dentro il grassetto, e il file
d'apparato che combaciava con `ARC*-DEF-*.md` e veniva preso per un master.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import componenti as comp  # noqa: E402


class TestLeProve(unittest.TestCase):

    def prove(self, testo):
        return [(p["prova"], p["cd"]) for p in comp._prove(testo)]

    def test_etichetta_in_minuscolo(self):
        self.assertEqual(self.prove("| ✋ Toccare | **FOR o DES grezza CD 12** |"),
                         [("FOR o DES grezza", 12)])

    def test_virgola_prima_della_cd(self):
        self.assertEqual(self.prove("| Tenere la breccia | Forza o attacco, **CD 18** |"),
                         [("Forza o attacco", 18)])

    def test_nome_che_va_a_capo_nel_grassetto(self):
        self.assertEqual(self.prove("Finché dura, **Muoversi Silenziosamente\n  CD 20**: bene."),
                         [("Finché dura, Muoversi Silenziosamente", 20)])

    def test_la_cd_precedente_non_entra_nell_etichetta(self):
        out = self.prove("Sapienza Magica **CD 24**, o Conoscenze storia CD 22")
        self.assertEqual(out, [("Sapienza Magica", 24), ("Conoscenze storia", 22)])

    def test_alternativa_fra_parentesi(self):
        out = self.prove("Diplomazia/Intimidire **CD 20** (**CD 16** col Nome)")
        self.assertEqual(out[1], ("Diplomazia/Intimidire, alternativa", 16))

    def test_nessuna_cd_persa_su_def4(self):
        import re
        import copertura_scene as cs
        master = ROOT / "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"
        idx = comp.indice(master)
        testo = cs.pulisci(master.read_text(encoding="utf-8"))
        attese = set()
        for titolo, corpo in cs.scene(testo, cs.SCENA_DEF, None):
            for m in comp._CD.finditer(corpo):
                attese.add((cs.chiave_scena(titolo), int(m.group(1))))
        trovate = {(s["scena"], p["cd"]) for s in idx["scene"] for p in s["prove"]}
        self.assertEqual(attese - trovate, set())


class TestLeInclusioni(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory(dir=ROOT / "build") if (ROOT / "build").exists() \
            else tempfile.TemporaryDirectory(dir=ROOT)
        self.d = Path(self.dir.name)
        self.rel = self.d.relative_to(ROOT).as_posix()

    def tearDown(self):
        self.dir.cleanup()

    def test_blocco_nominato(self):
        (self.d / "f.md").write_text("a\n<!-- blocco: n -->\nuno\ndue\n<!-- /blocco -->\nb\n", encoding="utf-8")
        testo = f"<!-- include: {self.rel}/f.md#n -->\nvecchio\n<!-- /include -->\n"
        self.assertEqual(comp.riallinea(testo),
                         f"<!-- include: {self.rel}/f.md#n -->\nuno\ndue\n<!-- /include -->\n")

    def test_statblocco_senza_marcatori(self):
        (self.d / "s.md").write_text("# X\n\n```statblocco\ngs: 1\npf: 5\n```\n\nprosa\n", encoding="utf-8")
        testo = f"<!-- include: {self.rel}/s.md#statblocco -->\n<!-- /include -->"
        self.assertIn("```statblocco\ngs: 1\npf: 5\n```\n<!-- /include -->", comp.riallinea(testo))

    def test_blocco_mancante_e_un_errore(self):
        (self.d / "f.md").write_text("niente\n", encoding="utf-8")
        with self.assertRaises(KeyError):
            comp.riallinea(f"<!-- include: {self.rel}/f.md#n -->\n<!-- /include -->")

    def test_riallineare_due_volte_non_cambia_niente(self):
        (self.d / "f.md").write_text("<!-- blocco: n -->\nuno\n<!-- /blocco -->\n", encoding="utf-8")
        una = comp.riallinea(f"<!-- include: {self.rel}/f.md#n -->\n<!-- /include -->")
        self.assertEqual(comp.riallinea(una), una)


class TestIlRepo(unittest.TestCase):

    def test_il_file_d_apparato_non_sembra_un_master(self):
        import fnmatch
        import copertura_scene as cs
        f = comp.file_apparato(Path("x/ARC07-DEF-4-VIAGGIO.md"))
        self.assertFalse(fnmatch.fnmatch(f.name, cs.GLOB_MASTER))

    def test_il_cancello_e_verde(self):
        self.assertEqual(comp.main(["--check"]), 0)

    def test_def4_include_balvar_dal_bestiario(self):
        modulo = (ROOT / "07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md").read_text(encoding="utf-8")
        self.assertIn("<!-- include: Bestiario/villain/balvar-fuocospento-cr13.md#statblocco -->", modulo)


if __name__ == "__main__":
    unittest.main()
