"""I cancelli della CI bocciano davvero? Finora non lo sapevamo.

Quattro gate — `validate_bestiario`, `validate_modules`, `validate_maps`,
`build_monster_catalog --check` — girano su ogni push e finora sono sempre
passati. Il che dimostra una cosa sola: che passano.

**Un cancello che non ha mai bocciato niente è indistinguibile da un cancello
rotto.** Un `return 0` messo per sbaglio, una `glob` che non trova più i file
dopo un rinomino, un `re.compile` che non matcha più: in tutti e tre i casi la CI
resta verde e nessuno se ne accorge, perché il segnale «verde» è esattamente
quello che ci si aspetta.

Questi test danno a ogni gate un file **deliberatamente rotto** e verificano che
lo respinga. E danno anche un file **sano**, perché un gate che boccia tutto è
inutile quanto uno che non boccia niente — la coppia è il test, non la metà.

Lotto B di `plans/PIANO-QUALITA-DEL-CODICE.md`. Solo `unittest`: la CI non
installa pytest.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import build_monster_catalog as C  # noqa: E402
import validate_bestiario as B  # noqa: E402
import validate_maps as M  # noqa: E402
import validate_modules as MOD  # noqa: E402


@contextmanager
def repo_finto():
    """Una radice temporanea, così nessun test scrive nel repo vero."""
    d = Path(tempfile.mkdtemp(prefix="gate-"))
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


@contextmanager
def radice(modulo, nuova: Path):
    """`check_statblock` fa `path.relative_to(ROOT)`: la radice va spostata."""
    vecchia = modulo.ROOT
    modulo.ROOT = nuova
    try:
        yield
    finally:
        modulo.ROOT = vecchia


SCHEDA_SANA = """# Orco Predone [ACCEPTED — DM-canon 2026-01-01]
**Faction**: red-hand | **Role**: melee | **Environment**: plain | **CR**: 3
**Source**: SRD | **Status**: transcribed

Medium humanoid (orc), 3d8+6. **hp 19**; **CA 15**. TS Temp +4, Rifl +1, Vol +1.
"""


class BestiarioBoccia(unittest.TestCase):
    """`validate_bestiario` — struttura, naming, coerenza del GS."""

    def setUp(self):
        B.errors.clear()
        B.warnings.clear()

    def _controlla(self, nome: str, testo: str) -> list[str]:
        with repo_finto() as d:
            (d / "Bestiario" / "mostri").mkdir(parents=True)
            f = d / "Bestiario" / "mostri" / nome
            f.write_text(testo, encoding="utf-8")
            with radice(B, d):
                B.check_statblock(f)
        return list(B.errors)

    def test_una_scheda_sana_passa(self):
        """Metà del test: un gate che boccia tutto è inutile quanto uno che
        non boccia niente."""
        self.assertEqual(self._controlla("orco-predone-cr3.md", SCHEDA_SANA), [])

    def test_boccia_il_nome_file_sbagliato(self):
        problemi = self._controlla("Orco_Predone_CR3.md", SCHEDA_SANA)
        self.assertTrue(any("kebab-case" in p for p in problemi), problemi)

    def test_boccia_il_gs_che_non_torna_fra_nome_e_intestazione(self):
        """Il difetto più insidioso: la scheda dice GS 3, il file dice GS 9, e
        `suggest_encounter` bilancia sul numero sbagliato."""
        problemi = self._controlla("orco-predone-cr9.md", SCHEDA_SANA)
        self.assertTrue(any("CR filename" in p for p in problemi), problemi)

    def test_boccia_l_intestazione_mancante(self):
        senza = SCHEDA_SANA.replace("**Faction**: red-hand | ", "")
        problemi = self._controlla("orco-predone-cr3.md", senza)
        self.assertTrue(any("header obbligatorio" in p for p in problemi), problemi)

    def test_boccia_lo_stato_non_dichiarato(self):
        muto = SCHEDA_SANA.replace(" [ACCEPTED — DM-canon 2026-01-01]", "")
        muto = muto.replace(" | **Status**: transcribed", "")
        problemi = self._controlla("orco-predone-cr3.md", muto)
        self.assertTrue(any("stato non dichiarato" in p for p in problemi), problemi)

    def test_boccia_il_gs_illeggibile(self):
        rotta = SCHEDA_SANA.replace("**CR**: 3", "**CR**: boh")
        problemi = self._controlla("orco-predone-cr3.md", rotta)
        self.assertTrue(any("CR non leggibile" in p for p in problemi), problemi)

    def test_il_dossier_senza_titolo_viene_bocciato(self):
        with repo_finto() as d:
            (d / "Bestiario" / "villain").mkdir(parents=True)
            f = d / "Bestiario" / "villain" / "Tizio.md"
            f.write_text("nessun titolo, solo prosa\n", encoding="utf-8")
            with radice(B, d):
                B.check_dossier(f)
        self.assertTrue(any("senza titolo H1" in p for p in B.errors), B.errors)


MASTER_SANO = """<!-- module-type: hub -->
# ARC99-DEF-1 — Prova

## INDICE
- uno

QUICKSTART: apri così.
QUICK-REFERENCE stampabile.
HIGHLIGHT asimmetrici per PG.
Contingenze «Se i PG fanno X».
Ramo sconfitta: mai punizione gratuita.
Sviluppi: cosa cambia dopo.
ECHI: conseguenze a distanza.
Budget PX sezione-per-sezione.
Tesoro PREGENERATO itemizzato.
HANDOUT & asset.

### MAPPA
scala 1,5 m per quadretto.

Box supporto PF1e dove il 3.5 è vago.
Read-aloud uno. Read-aloud due. Read-aloud tre. Read-aloud quattro.
Read-aloud cinque. [INFERRED — da confermare]
"""


class ModuliBoccia(unittest.TestCase):
    """`validate_modules` — la checklist dello standard di modulo."""

    def _controlla(self, testo: str) -> list[str]:
        with repo_finto() as d:
            f = d / "ARC99-DEF-1-PROVA.md"
            f.write_text(testo, encoding="utf-8")
            errori, _ = MOD.check_file(f, verbose=False)
        return errori

    def test_un_master_sano_passa(self):
        self.assertEqual(self._controlla(MASTER_SANO), [])

    def test_boccia_una_sezione_mancante(self):
        senza = MASTER_SANO.replace("HANDOUT & asset.\n", "")
        problemi = self._controlla(senza)
        self.assertTrue(any("HANDOUT" in p for p in problemi), problemi)

    def test_boccia_la_terminologia_5e(self):
        """«bonus action» e «DC 15» sono i due che scappano più spesso."""
        for veleno, atteso in (("Usa una bonus action per ritirarsi.", "bonus action"),
                               ("Tiro su Riflessi DC 15.", "CD")):
            with self.subTest(riga=veleno):
                problemi = self._controlla(MASTER_SANO + veleno + "\n")
                self.assertTrue(any(atteso in p for p in problemi), problemi)

    def test_boccia_il_canone_deprecato(self):
        problemi = self._controlla(MASTER_SANO + "Nymeria abbaia.\n")
        self.assertTrue(any("DURIK" in p for p in problemi), problemi)

    def test_la_riga_che_VIETA_il_termine_non_viene_bocciata(self):
        """L'esenzione esiste perché la guida che dice «mai bonus action» non
        deve far fallire il gate che vieta «bonus action»."""
        problemi = self._controlla(MASTER_SANO
                                   + "Mai 5e: bonus action → azione veloce.\n")
        self.assertEqual(problemi, [])

    def test_un_beat_di_combattimento_esige_di_piu_di_un_hub(self):
        """`module-type: hub` esenta dalle sezioni tattiche; toglierlo no."""
        dungeon = MASTER_SANO.replace("<!-- module-type: hub -->", "")
        problemi = self._controlla(dungeon)
        self.assertTrue(any("Tattiche" in p for p in problemi), problemi)


SVG_SANO = ('<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" '
            'width="10" height="10"><rect width="10" height="10"/></svg>')


class MappeBoccia(unittest.TestCase):
    """`validate_maps` — gli SVG sono artefatti generati, mai editati a mano."""

    def test_una_cartella_vuota_non_e_un_errore(self):
        with repo_finto() as d:
            self.assertEqual(M.validate(d), 0)

    def test_boccia_uno_svg_malformato(self):
        """Il caso vero: qualcuno apre l'SVG, lo corregge a mano e lo rompe.

        ⚠️ Le prime due versioni di questo test passavano **per la ragione
        sbagliata**, ed è istruttivo. Guardavano il codice d'uscita di
        `validate()`, ma quel file dà DUE errori — l'XML rotto e l'orfano — e
        l'uscita è 1 in entrambi i casi. Disattivando il controllo sulla
        malformazione il test restava verde: non testava niente.

        Non se ne accorgeva nessuno guardando il test. Se n'è accorta la
        **mutazione del validatore**: rompi la riga, e se i test restano verdi
        quella riga non è coperta. Ora si guarda il messaggio, non l'uscita.
        """
        with repo_finto() as d:
            f = d / "rotto.svg"
            f.write_text("<svg><rect></svg>", encoding="utf-8")
            errori: list[str] = []
            M.check_wellformed(f, errori)
            self.assertTrue(any("malformato" in e for e in errori), errori)

    def test_uno_svg_sano_passa_il_controllo_di_forma(self):
        with repo_finto() as d:
            f = d / "sano.svg"
            f.write_text(SVG_SANO, encoding="utf-8")
            errori: list[str] = []
            M.check_wellformed(f, errori)
            self.assertEqual(errori, [])

    def test_boccia_una_radice_che_non_e_svg(self):
        """Un HTML rinominato `.svg` è XML valido e non è una mappa."""
        with repo_finto() as d:
            f = d / "finto.svg"
            f.write_text("<html><body/></html>", encoding="utf-8")
            errori: list[str] = []
            M.check_wellformed(f, errori)
            self.assertTrue(any("radice non" in e for e in errori), errori)

    def test_boccia_lo_svg_orfano(self):
        """Un SVG senza il master markdown da cui dovrebbe nascere: o il master
        è stato cancellato, o l'SVG è stato scritto a mano."""
        with repo_finto() as d:
            r = d / "modulo" / "rendered"
            r.mkdir(parents=True)
            (r / "sparito_map01_prova.svg").write_text(SVG_SANO, encoding="utf-8")
            self.assertNotEqual(M.validate(d), 0)

    def test_boccia_il_nome_fuori_standard(self):
        with repo_finto() as d:
            r = d / "modulo" / "rendered"
            r.mkdir(parents=True)
            (r / "una-mappa-qualsiasi.svg").write_text(SVG_SANO, encoding="utf-8")
            self.assertNotEqual(M.validate(d), 0)


class CatalogoBoccia(unittest.TestCase):
    """`build_monster_catalog --check` — il catalogo deve restare in sincronia."""

    def test_trova_una_scheda_e_ne_legge_il_gs(self):
        with repo_finto() as d:
            (d / "Bestiario" / "mostri").mkdir(parents=True)
            (d / "Bestiario" / "mostri" / "orco-predone-cr3.md").write_text(
                SCHEDA_SANA, encoding="utf-8")
            with radice(C, d):
                record = C.scan_directory(d)
        self.assertTrue(record, "non ha trovato la scheda")
        self.assertEqual(float(record[0]["cr"]), 3.0)

    def test_un_catalogo_vecchio_di_una_scheda_viene_bocciato(self):
        """È il caso che capita davvero: si aggiunge un mostro e ci si dimentica
        di rigenerare. Il gate deve accorgersene."""
        with repo_finto() as d:
            (d / "Bestiario" / "mostri").mkdir(parents=True)
            (d / "Bestiario" / "mostri" / "orco-predone-cr3.md").write_text(
                SCHEDA_SANA, encoding="utf-8")
            with radice(C, d):
                prima = C.to_yaml(C.scan_directory(d))
                (d / "Bestiario" / "mostri" / "gnoll-cr2.md").write_text(
                    SCHEDA_SANA.replace("**CR**: 3", "**CR**: 2")
                               .replace("Orco Predone", "Gnoll"), encoding="utf-8")
                dopo = C.to_yaml(C.scan_directory(d))
        self.assertNotEqual(prima, dopo,
                            "aggiungere una scheda deve cambiare il catalogo, "
                            "altrimenti --check non potrebbe accorgersene")

    def test_lo_stesso_albero_da_lo_stesso_catalogo(self):
        """`--check` confronta byte per byte: senza determinismo boccerebbe
        sempre, e verrebbe spento entro una settimana."""
        with repo_finto() as d:
            (d / "Bestiario" / "mostri").mkdir(parents=True)
            for nome, cr in (("orco-predone-cr3.md", 3), ("gnoll-cr2.md", 2)):
                (d / "Bestiario" / "mostri" / nome).write_text(
                    SCHEDA_SANA.replace("**CR**: 3", f"**CR**: {cr}"),
                    encoding="utf-8")
            with radice(C, d):
                self.assertEqual(C.to_yaml(C.scan_directory(d)),
                                 C.to_yaml(C.scan_directory(d)))


if __name__ == "__main__":
    unittest.main()
