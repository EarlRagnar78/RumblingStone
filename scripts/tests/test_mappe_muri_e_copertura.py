"""ADR-0043: le montagne bloccano la vista, e nessun master esce dal controllo.

Due difetti diversi, tenuti insieme perche' sono la stessa famiglia — cose che
il codice dava per buone senza che nessuno le contasse:

  1. `⛰` era disegnato solido dal renderer e NON era un muro nell'export UVTT:
     in Foundry si attraversava la catena montuosa e ci si vedeva attraverso.
  2. `validate_maps` rendeva solo i master con almeno un SVG committato, quindi
     togliendoli TUTTI il master usciva dalla validazione: verde, e nessuno
     guardava piu' quelle mappe.
"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import export_uvtt as U  # noqa: E402
import render_map_svg as R  # noqa: E402
import validate_maps as V  # noqa: E402

MONTAGNA, MACERIE = "⛰", "🪨"


def _griglia(simbolo: str) -> list[list[str]]:
    """Una colonna del simbolo in mezzo al pavimento: se e' muro, fa segmenti."""
    return [["⬜", simbolo, "⬜", "⬜", "⬜", "⬜"] for _ in range(4)]


class TestMontagneSonoMuri(unittest.TestCase):
    def test_la_montagna_blocca_la_vista(self):
        self.assertIn(MONTAGNA, U.WALL_SYMS,
                      "il renderer la disegna solida: l'export deve metterci un muro")

    def test_le_macerie_no_e_va_bene_cosi(self):
        """🪨 e' copertura PARZIALE (+4 CA, terreno difficile), non totale."""
        self.assertNotIn(MACERIE, U.WALL_SYMS)

    def test_la_montagna_produce_davvero_segmenti_di_muro(self):
        """Stare nell'insieme non basta: si conta l'effetto sull'export."""
        self.assertTrue(U.extract_walls(_griglia(MONTAGNA)),
                        "una colonna di ⛰ non genera nessun segmento")
        self.assertFalse(U.extract_walls(_griglia(MACERIE)),
                         "🪨 non deve generare muri")

    def test_il_renderer_e_l_export_sono_d_accordo_sui_solidi(self):
        """Il difetto nasceva dal disaccordo fra chi disegna e chi esporta.

        Ogni simbolo che il renderer tratta come riempimento PESANTE deve essere
        un muro nell'export. Se qualcuno aggiunge un pattern pesante e si scorda
        WALL_SYMS, questo test lo prende.
        """
        pesanti = {sym for sym, spec in R.SYMBOLS.items()
                   if spec.get("pat") in R.HEAVY_PATS}
        mancanti = sorted(pesanti - U.WALL_SYMS)
        self.assertEqual(mancanti, [],
                         f"disegnati solidi ma non muri nell'export: {mancanti}")


class TestNessunMasterEsceDalControllo(unittest.TestCase):
    def test_il_repo_reale_non_ha_master_fuori_controllo(self):
        rendered = sorted({p.parent for p in ROOT.glob("**/rendered/*.svg")})
        self.assertEqual(V.check_masters_senza_svg(ROOT, rendered), [])

    def test_togliere_tutti_gli_svg_non_fa_sparire_il_master(self):
        """Lo scenario esatto della #63: cancella gli SVG, tieni il master."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Mappe" / "rendered").mkdir(parents=True)
            (root / "Mappe" / "sparito.md").write_text(_MASTER, encoding="utf-8")
            # un SVG di un ALTRO master, cosi' la cartella rendered/ esiste
            (root / "Mappe" / "rendered" / "altro_map01_x.svg").write_text(
                "<svg/>", encoding="utf-8")
            (root / "Mappe" / "altro.md").write_text(
                "<!-- validate_maps: non-renderizzato — fixture -->\n", encoding="utf-8")
            errori = V.check_masters_senza_svg(root, [root / "Mappe" / "rendered"])
            self.assertTrue(any("sparito.md" in e for e in errori), errori)

    def test_l_opt_out_dichiarato_e_rispettato(self):
        """Chi non vuole essere renderizzato lo dice nel master, non altrove."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Mappe" / "rendered").mkdir(parents=True)
            (root / "Mappe" / "rendered" / "altro_map01_x.svg").write_text(
                "<svg/>", encoding="utf-8")
            (root / "Mappe" / "scelto.md").write_text(
                "<!-- validate_maps: non-renderizzato — riga KO del censimento -->\n"
                + _MASTER, encoding="utf-8")
            self.assertEqual(
                V.check_masters_senza_svg(root, [root / "Mappe" / "rendered"]), [])

    def test_validate_chiama_davvero_il_gate(self):
        """Un gate scritto e non agganciato e' un gate che non c'e'.

        I test qui sopra chiamano `check_masters_senza_svg` di persona, quindi
        resterebbero verdi anche se `validate()` smettesse di usarla. Questo va
        per la porta principale.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Mappe" / "rendered").mkdir(parents=True)
            (root / "Mappe" / "rendered" / "altro_map01_x.svg").write_text(
                "<svg xmlns='http://www.w3.org/2000/svg'/>", encoding="utf-8")
            (root / "Mappe" / "altro.md").write_text(
                "<!-- validate_maps: non-renderizzato — fixture -->\n", encoding="utf-8")
            (root / "Mappe" / "sparito.md").write_text(_MASTER, encoding="utf-8")
            # Sul contenuto, non sul codice d'uscita: quel mini-repo produce
            # anche un «SVG orfano» dal segnaposto, quindi un exit != 0 direbbe
            # solo che qualcosa e' andato storto — non che sia stato QUESTO
            # controllo a parlare.
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                V.validate(root, as_json=True)
            errori = json.loads(buf.getvalue())["errors"]
            self.assertTrue(any("master fuori controllo" in e for e in errori),
                            f"validate() non sta agganciando il controllo: {errori}")

    def test_un_markdown_che_non_e_una_mappa_non_da_falsi_positivi(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Mappe" / "rendered").mkdir(parents=True)
            (root / "Mappe" / "rendered" / "altro_map01_x.svg").write_text(
                "<svg/>", encoding="utf-8")
            (root / "Mappe" / "note.md").write_text(
                "# Note del DM\n\nNessuna griglia qui dentro.\n", encoding="utf-8")
            self.assertEqual(
                V.check_masters_senza_svg(root, [root / "Mappe" / "rendered"]), [])


_MASTER = (
    "## MAPPA X-1: prova (griglia 6×3, scala 1,5 m/q)\n\n"
    "```\n"
    "     A  B  C  D  E  F\n"
    " 1 | ⬜ ⬛ ⬛ ⬜ ⛰ ⬜ |\n"
    " 2 | ⬜ ⬛ ⬛ ⬜ ⛰ ⬜ |\n"
    " 3 | ⬜ ⬜ ⬜ ⬜ ⛰ ⬜ |\n"
    "```\n"
)


if __name__ == "__main__":
    unittest.main()
