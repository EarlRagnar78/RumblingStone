"""`validate_corredo.py`: il corredo della serata, e i modi in cui si rompe.

La norma è in `skills/rumblingstone-automation/SKILL.md`, «Il corredo della
serata». Ogni classe qui sotto toglie **un** pezzo a un corredo che passa e
guarda il controllo diventare rosso: un cancello che non si è mai visto
bocciare non conta (PIANO-CICLO-DI-SESSIONE-E-MENU §5.0, mutazioni).

Il corredo vero della serata ARC-07 è il caso d'approvazione: deve passare.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import validate_corredo as vc  # noqa: E402

SERATA = (REPO / "07_il Portale Della Forgia Eterna" / "homebrew" /
          "sessione-resurrezione-mille-anni" / "ARC07-SERATA-RESURREZIONE.corredo.json")

#: Un PNG vero da un pixel: basta a far esistere un'immagine.
PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082")

PROMPT = """# Prompt

<!-- img id=ritratto-tizio size=832x1216 -->
```
old dwarf
```

## §5 · Confronto immagine-scheda

| id | Confrontata con | Cosa non coincideva | Esito |
|---|---|---|---|
| `ritratto-tizio` | scheda | niente | tenuta |
"""


def _corredo(d: Path) -> Path:
    """Un corredo minimo e completo in `d`: due PG, un volume di fogli, un prompt."""
    (d / "ritratti").mkdir()
    (d / "ritratti" / "tizio.png").write_bytes(PNG)
    (d / "PROMPT.md").write_text(PROMPT, encoding="utf-8")
    for nome, testo in {
        "regia.md": "# Regia\n\n> *Un box corto.*\n",
        "eco-a.md": "# Echi A\n\n> *Un'eco.*\n",
        "eco-b.md": "# Echi B\n\n> *Un'altra.*\n",
        "carta.md": "# Carta\n\nUn dono.\n",
    }.items():
        (d / nome).write_text(testo, encoding="utf-8")
    fogli = [{"file": f, "tag": "player"} for f in ("eco-a.md", "eco-b.md", "carta.md")]
    (d / "DM.manifest.json").write_text(json.dumps(
        {"title": "DM", "chapters": [{"file": "regia.md", "tag": "dm"}]}), encoding="utf-8")
    (d / "FOGLI.manifest.json").write_text(json.dumps(
        {"title": "Fogli", "chapters": fogli}), encoding="utf-8")
    c = d / "S.corredo.json"
    c.write_text(json.dumps({
        "versione": 1, "serata": "2026-01-01", "titolo": "Prova", "pg": ["A", "B"],
        "booklet_dm": "DM.manifest.json", "fogli_giocatori": "FOGLI.manifest.json",
        "echi": {"A": "eco-a.md", "B": "eco-b.md"}, "carte_e_handout": ["carta.md"],
        "immagini": {"prompt": ["PROMPT.md"]},
    }), encoding="utf-8")
    return c


class _Base(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.c = _corredo(self.d)

    def tearDown(self):
        shutil.rmtree(self.d)

    def errori(self):
        return vc.controlla_corredo(self.c)[0]

    def dato(self):
        return json.loads(self.c.read_text(encoding="utf-8"))

    def scrivi(self, dato):
        self.c.write_text(json.dumps(dato), encoding="utf-8")


class TestIlCorredoVero(unittest.TestCase):
    def test_la_serata_arc07_e_completa(self):
        errori, _ = vc.controlla_corredo(SERATA)
        self.assertEqual(errori, [])

    def test_il_corredo_minimo_passa(self):
        d = Path(tempfile.mkdtemp())
        try:
            self.assertEqual(vc.controlla_corredo(_corredo(d))[0], [])
        finally:
            shutil.rmtree(d)


class TestUnPezzoMancante(_Base):
    def test_manca_il_file_degli_echi(self):
        (self.d / "eco-b.md").unlink()
        self.assertTrue(any("echi di B" in e or "eco-b.md" in e for e in self.errori()))

    def test_un_pg_senza_echi(self):
        dato = self.dato()
        del dato["echi"]["B"]
        self.scrivi(dato)
        self.assertTrue(any("B non ha i suoi echi" in e for e in self.errori()))

    def test_manca_il_volume_dei_fogli(self):
        (self.d / "FOGLI.manifest.json").unlink()
        self.assertTrue(any("fogli_giocatori" in e for e in self.errori()))

    def test_una_chiave_obbligatoria_assente(self):
        dato = self.dato()
        del dato["carte_e_handout"]
        self.scrivi(dato)
        self.assertTrue(any("carte_e_handout" in e for e in self.errori()))

    def test_una_carta_che_non_esiste(self):
        dato = self.dato()
        dato["carte_e_handout"].append("carta-persa.md")
        self.scrivi(dato)
        self.assertTrue(any("carta-persa.md" in e for e in self.errori()))


class TestIlVolumeDeiFogli(_Base):
    def _fogli(self, capitoli):
        (self.d / "FOGLI.manifest.json").write_text(
            json.dumps({"title": "Fogli", "chapters": capitoli}), encoding="utf-8")

    def test_un_foglio_ristampato_nel_booklet_del_dm(self):
        (self.d / "DM.manifest.json").write_text(json.dumps(
            {"title": "DM", "chapters": [{"file": "regia.md", "tag": "dm"},
                                         {"file": "carta.md", "tag": "player"}]}), encoding="utf-8")
        e = self.errori()
        self.assertTrue(any("carta.md" in x and "solo nel volume dei giocatori" in x for x in e), e)
        self.assertTrue(any("carta.md" in x and "si stampa 2 volte" in x for x in e), e)

    def test_lo_stesso_master_in_due_volumi(self):
        (self.d / "APPROF.manifest.json").write_text(json.dumps(
            {"title": "Secondo libro", "chapters": [{"file": "regia.md", "tag": "dm"}]}),
            encoding="utf-8")
        dato = self.dato()
        dato["approfondimento"] = ["APPROF.manifest.json"]
        self.scrivi(dato)
        self.assertTrue(any("regia.md si stampa 2 volte" in e for e in self.errori()))

    def test_uno_spoiler_nei_fogli(self):
        self._fogli([{"file": f, "tag": "player"} for f in ("eco-a.md", "eco-b.md", "carta.md")]
                    + [{"file": "regia.md", "tag": "dm"}])
        self.assertTrue(any("spoiler" in e for e in self.errori()))


class TestLeImmagini(_Base):
    def test_un_immagine_mai_esportata(self):
        (self.d / "ritratti" / "tizio.png").unlink()
        self.assertTrue(any("non c'è" in e for e in self.errori()))

    def test_un_immagine_senza_confronto(self):
        testo = PROMPT.replace("| `ritratto-tizio` | scheda | niente | tenuta |\n", "")
        (self.d / "PROMPT.md").write_text(testo, encoding="utf-8")
        self.assertTrue(any("riga nel confronto" in e for e in self.errori()))

    def test_senza_la_sezione_del_confronto(self):
        (self.d / "PROMPT.md").write_text(PROMPT.split("## §5")[0], encoding="utf-8")
        self.assertTrue(any("Confronto immagine-scheda" in e for e in self.errori()))


class TestIlTettoDeiBox(_Base):
    def test_un_box_di_tredici_righe(self):
        box = "\n".join(f"> *riga {i}*" if i == 0 else f"> riga {i}" for i in range(13))
        (self.d / "regia.md").write_text(f"# Regia\n\n{box}\n", encoding="utf-8")
        self.assertTrue(any("13 righe" in e for e in self.errori()))

    def test_lo_storico_non_conta(self):
        # Quello che si stampa è il testo senza storico (ADR-0069): un box di
        # dieci righe con sei righe di storia dentro sta sotto il tetto.
        corpo = ["> *apre*"] + [f"> riga {i}" for i in range(9)]
        storico = ["> <!-- storico -->"] + [f"> vecchio {i}" for i in range(4)] + ["> <!-- /storico -->"]
        (self.d / "regia.md").write_text("# Regia\n\n" + "\n".join(corpo + storico) + "\n",
                                         encoding="utf-8")
        self.assertEqual(self.errori(), [])


class TestIlPdf(unittest.TestCase):
    """La misura pura, e poi un PDF vero se ci sono typst e PyMuPDF."""

    def test_due_righe_sovrapposte(self):
        righe = [((50, 100, 200, 110), "prima"), ((60, 102, 210, 112), "seconda")]
        self.assertEqual(len(vc.sovrapposizioni(righe)), 1)

    def test_righe_una_sotto_l_altra_non_si_sovrappongono(self):
        righe = [((50, 100, 200, 110), "prima"), ((50, 111, 200, 121), "seconda")]
        self.assertEqual(vc.sovrapposizioni(righe), [])

    def test_colonne_affiancate_non_si_sovrappongono(self):
        righe = [((50, 100, 250, 110), "sinistra"), ((300, 100, 500, 110), "destra")]
        self.assertEqual(vc.sovrapposizioni(righe), [])

    def test_testo_sul_bordo(self):
        righe = [((10, 100, 200, 110), "fuori"), ((60, 100, 200, 110), "dentro")]
        self.assertEqual(vc.fuori_margine(righe, 595, 842), ["fuori"])

    @unittest.skipUnless(shutil.which("typst"), "typst assente")
    def test_un_pdf_difettoso_viene_bocciato(self):
        try:
            import pymupdf  # noqa: F401
        except ImportError:
            self.skipTest("PyMuPDF assente")
        d = Path(tempfile.mkdtemp())
        try:
            (d / "x.typ").write_text(
                '#set page(paper: "a4", margin: 2cm)\n'
                "#place(top + left, dx: 0cm, dy: 3cm)[Una riga]\n"
                "#place(top + left, dx: 0.3cm, dy: 3.05cm)[Due righe]\n"
                "#place(top + left, dx: -1.8cm, dy: 8cm)[Sul bordo del foglio]\n",
                encoding="utf-8")
            subprocess.run(["typst", "compile", str(d / "x.typ")], check=True)
            difetti, nota = vc.misura_pdf(d / "x.pdf")
            self.assertEqual(nota, "")
            self.assertTrue(any("sovrapposte" in x for x in difetti), difetti)
            self.assertTrue(any("dal bordo" in x for x in difetti), difetti)
        finally:
            shutil.rmtree(d)


class TestUscita(unittest.TestCase):
    def test_un_corredo_inesistente_esce_2(self):
        self.assertEqual(vc.main(["/non/esiste.corredo.json"]), 2)

    def test_un_corredo_rotto_esce_1(self):
        d = Path(tempfile.mkdtemp())
        try:
            c = _corredo(d)
            (d / "carta.md").unlink()
            self.assertEqual(vc.main([str(c)]), 1)
        finally:
            shutil.rmtree(d)


class TestLApparatoInStampa(unittest.TestCase):
    """ADR-0070: le firme delle classi A, B e D nel testo del PDF, e il tetto."""

    PAGINA = ("⭐ MASTER DEFINITIVO — beat HUB. Sostituisce e fonde: P2.md. MAI 5e.\n"
              "Correzione canone (DM). Poi il master #3 §7, e DEF-4.\n"
              "Il nano alza il boccale #1 e si consegna alla guardia.")

    def test_le_tre_classi(self):
        classi = [c for _, c, _, _ in vc.rilievi_apparato([self.PAGINA])]
        self.assertIn("A", classi)
        self.assertIn("B", classi)
        self.assertEqual(classi.count("D"), 2)

    def test_la_finzione_non_e_apparato(self):
        # «#1» senza «master», e «si consegna» dentro la finzione: i due falsi
        # positivi che il prompt del DM prevedeva, e che la firma non prende.
        self.assertEqual(vc.rilievi_apparato(["Il boccale #1. Si consegna alla guardia."]), [])

    def test_la_parola_spezzata_si_riconosce(self):
        self.assertTrue(vc.rilievi_apparato(["FILE-FONTE ASSORBITI DA QUESTO MA\u00ad\nSTER"]))
        self.assertTrue(vc.rilievi_apparato(["in _\u200bARCHIVIO/\u200bP5.md"]))

    def test_oltre_il_tetto_e_rosso(self):
        errori = vc.controlla_apparato(Path("/non/nel/registro.manifest.json"), [self.PAGINA])
        self.assertTrue(errori and "tetto 0" in errori[0], errori)

    def test_un_tetto_piu_alto_del_vero_e_rosso(self):
        palio = (REPO / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
                 / "homebrew" / "PALIO-BOOKLET.manifest.json")
        tetto, perche = vc.tetto_apparato(palio)
        self.assertGreater(tetto, 0)
        self.assertTrue(perche)
        errori = vc.controlla_apparato(palio, ["pagina pulita"])
        self.assertTrue(errori and "abbassalo" in errori[0], errori)

    def test_ogni_residuo_ha_il_suo_perche(self):
        dati = json.loads(vc.RESIDUI_APPARATO.read_text(encoding="utf-8"))["volumi"]
        for manifest, voce in dati.items():
            self.assertTrue((REPO / manifest).is_file(), manifest)
            self.assertGreater(voce["tetto"], 0, manifest)
            self.assertGreater(len(voce["perche"]), 20, manifest)


class TestIRimandiTradotti(unittest.TestCase):
    """ADR-0070, classe D: un rimando diventa il capitolo del volume."""

    def test_gli_esempi_della_funzione(self):
        import doctest  # noqa: PLC0415
        import dmcore.testo as testo  # noqa: PLC0415
        esito = doctest.testmod(testo)
        self.assertEqual(esito.failed, 0)

    def test_un_volume_vero(self):
        d = Path(tempfile.mkdtemp())
        try:
            (d / "ARC07-DEF-1-A.md").write_text("# ARC-07 · DEFINITIVO #1 — IL PIANO DELLA TERRA\n")
            (d / "ARC07-DEF-2-B.md").write_text("# X\nPrima (master #1). Poi `DEF-3` §7 e DEF-1 §9.\n")
            (d / "ARC07-DEF-3-C.md").write_text("# Y\n")
            (d / "V.manifest.json").write_text(json.dumps({"title": "V", "chapters": [
                {"title": "III · Il Ritorno", "file": "ARC07-DEF-2-B.md"},
                {"title": "IV · La Resurrezione", "file": "ARC07-DEF-3-C.md"}]}))
            from dmcore.testo import capitoli_del_volume, leggi_per_la_stampa  # noqa: PLC0415
            dato = json.loads((d / "V.manifest.json").read_text())
            testo = leggi_per_la_stampa(d / "ARC07-DEF-2-B.md", capitoli_del_volume(d, dato))
            self.assertIn("Prima («Il Piano della Terra»).", testo)
            self.assertIn("cap. IV §7", testo)
            self.assertIn("«Il Piano della Terra» §9", testo)
        finally:
            shutil.rmtree(d)


class TestDmCorredo(unittest.TestCase):
    """`dm.py corredo`: un corredo incompleto non si compila."""

    def test_un_corredo_incompleto_non_compila_niente(self):
        import dm  # noqa: PLC0415
        d = Path(tempfile.mkdtemp())
        try:
            c = _corredo(d)
            (d / "eco-a.md").unlink()
            self.assertEqual(dm.main(["corredo", str(c)]), 1)
            self.assertFalse(list(d.glob("*.html")), "ha compilato un corredo incompleto")
        finally:
            shutil.rmtree(d)

    def test_un_corredo_inesistente_esce_2(self):
        import dm  # noqa: PLC0415
        self.assertEqual(dm.main(["corredo", "/non/esiste.corredo.json"]), 2)


if __name__ == "__main__":
    unittest.main()
