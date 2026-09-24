"""Le derivate da impaginazione: formati accettati, ridimensionamento, uscita JPEG.

Il tool è nato per i PNG generati del Drappo e serve anche ai **WebP** della
campagna (ARC-07), che sono il caso peggiore per la stampa: Typst decodifica e
ricomprime un WebP, mentre incorpora un JPEG così com'è. Questi test tengono
onesta l'estensione (piano TRAVASO, lotto A3).

Pillow non è installato in CI: senza, i test si saltano invece di fallire — il
tool stesso è progettato per uscire pulito quando manca.
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOOL = REPO / "scripts" / "build_image_derivatives.py"

spec = importlib.util.spec_from_file_location("build_image_derivatives", TOOL)
bid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bid)

try:
    from PIL import Image
    PILLOW = True
except ImportError:                                   # pragma: no cover
    PILLOW = False


class TestLatoPerFamiglia(unittest.TestCase):
    """Il lato lungo viene dalla destinazione, non da un numero a caso."""

    def test_tavola_piu_larga_di_un_ritratto(self):
        self.assertEqual(bid.lato_per("tavola-la-ruota", 1400), 1800)

    def test_spot_sta_in_una_colonna(self):
        self.assertEqual(bid.lato_per("spot-la-bilancia", 1400), 900)

    def test_senza_prefisso_vale_il_default(self):
        self.assertEqual(bid.lato_per("png-vesca", 1400), 1400)


@unittest.skipUnless(PILLOW, "Pillow assente: il tool esce pulito, i test si saltano")
class TestDerivate(unittest.TestCase):
    def _cartella(self, nomi):
        d = Path(tempfile.mkdtemp())
        for nome in nomi:
            Image.new("RGB", (2400, 1600), (120, 90, 60)).save(d / nome)
        return d

    def _esegui(self, cartella):
        """Il tool si pilota dalla riga di comando, come in CI."""
        argv = sys.argv
        sys.argv = ["build_image_derivatives.py", str(cartella)]
        try:
            return bid.main()
        finally:
            sys.argv = argv

    def test_png_e_webp_producono_entrambi_un_jpeg(self):
        d = self._cartella(["png-tizio.png", "tavola-caverna.webp"])
        self.assertEqual(self._esegui(d), 0)
        self.assertEqual(sorted(p.name for p in (d / "web").iterdir()),
                         ["png-tizio.jpg", "tavola-caverna.jpg"])

    def test_ridimensiona_al_lato_della_famiglia(self):
        d = self._cartella(["tavola-caverna.webp", "spot-quadro.png"])
        self._esegui(d)
        with Image.open(d / "web" / "tavola-caverna.jpg") as im:
            self.assertEqual(max(im.size), 1800)
        with Image.open(d / "web" / "spot-quadro.jpg") as im:
            self.assertEqual(max(im.size), 900)

    def test_i_master_non_si_toccano(self):
        """ADR-0003: la derivata è un artefatto, il master resta il sorgente."""
        d = self._cartella(["png-tizio.webp"])
        prima = (d / "png-tizio.webp").read_bytes()
        self._esegui(d)
        self.assertEqual((d / "png-tizio.webp").read_bytes(), prima)

    def test_cartella_inesistente_esce_con_2(self):
        self.assertEqual(self._esegui(Path(tempfile.mkdtemp()) / "non-c-e"), 2)


if __name__ == "__main__":
    unittest.main()
