"""L'etichetta di provenienza nelle copie da impaginazione (ADR-0132).

Il master generato porta un manifesto C2PA firmato; la copia `web/` che va nei
booklet deve dire la stessa cosa col campo IPTC `DigitalSourceType`, senza che
i suoi pixel cambino. E non deve dirlo quando il master non lo dice.
"""
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import provenienza_immagini as pi  # noqa: E402

try:
    from PIL import Image, PngImagePlugin
    PILLOW = True
except ImportError:                                   # pragma: no cover
    PILLOW = False

#: quello che un manifesto C2PA porta dentro, ridotto all'osso (CBOR: la chiave
#: successiva è attaccata al termine)
MANIFESTO = (b"jumb....c2pa....http://cv.iptc.org/newscodes/digitalsourcetype/"
             b"trainedAlgorithmicMediajparameters")
COMPOSTO = MANIFESTO + b"....http://cv.iptc.org/newscodes/digitalsourcetype/compositejparameters"


def _jpeg(colore=(120, 60, 30)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (40, 30), colore).save(buf, "JPEG", quality=85)
    return buf.getvalue()


def _png(testo: bytes | None = None, esadecimale: bool = False) -> bytes:
    info = PngImagePlugin.PngInfo()
    if testo and esadecimale:
        righe = testo.hex()
        info.add_text("Raw profile type app11",
                      "\napp11\n   %d\n" % len(testo) + "\n".join(
                          righe[i:i + 72] for i in range(0, len(righe), 72)), zip=True)
    elif testo:
        info.add_text("c2pa", testo.decode("latin-1") * 20)
    buf = io.BytesIO()
    Image.new("RGB", (40, 30), (10, 20, 30)).save(buf, "PNG", pnginfo=info)
    dati = buf.getvalue()
    return dati + (testo if testo and not esadecimale else b"")


@unittest.skipUnless(PILLOW, "Pillow assente")
class TestEtichettaJpeg(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.master = self.d / "ritratto.png"
        self.master.write_bytes(_png(MANIFESTO))

    def test_si_scrive_e_si_rilegge(self):
        nuovo = pi.etichetta_jpeg(_jpeg(), pi.pacchetto_xmp(pi.GENERATA, self.master))
        self.assertEqual(pi.leggi_etichetta(nuovo), pi.GENERATA)
        self.assertEqual(pi.leggi_etichetta(_jpeg()), "")

    def test_i_pixel_non_cambiano(self):
        prima = _jpeg()
        dopo = pi.etichetta_jpeg(prima, pi.pacchetto_xmp(pi.GENERATA, self.master))
        self.assertEqual(Image.open(io.BytesIO(prima)).tobytes(),
                         Image.open(io.BytesIO(dopo)).tobytes())

    def test_pillow_la_legge_come_xmp(self):
        dopo = pi.etichetta_jpeg(_jpeg(), pi.pacchetto_xmp(pi.GENERATA, self.master))
        xmp = Image.open(io.BytesIO(dopo)).info.get("xmp", b"")
        self.assertIn(b"Iptc4xmpExt:DigitalSourceType", xmp)
        self.assertIn(b"ritratto.png sha256:", xmp)

    def test_riscrivere_non_raddoppia(self):
        una = pi.etichetta_jpeg(_jpeg(), pi.pacchetto_xmp(pi.GENERATA, self.master))
        due = pi.etichetta_jpeg(una, pi.pacchetto_xmp(pi.COMPOSTA, self.master))
        self.assertEqual(due.count(b"http://ns.adobe.com/xap/1.0/\x00"), 1)
        self.assertEqual(pi.leggi_etichetta(due), pi.COMPOSTA)

    def test_un_file_che_non_e_jpeg_si_rifiuta(self):
        with self.assertRaises(ValueError):
            pi.etichetta_jpeg(b"\x89PNG....", b"<x/>")


@unittest.skipUnless(PILLOW, "Pillow assente")
class TestSorgenteDelMaster(unittest.TestCase):
    def _master(self, dati: bytes, nome="m.png") -> Path:
        p = Path(tempfile.mkdtemp()) / nome
        p.write_bytes(dati)
        return p

    def test_manifesto_nei_byte(self):
        self.assertEqual(pi.sorgente_del_master(self._master(_png(MANIFESTO))), (True, pi.GENERATA))

    def test_manifesto_in_esadecimale_dentro_il_png(self):
        """Il modo di Gemini: «Raw profile type app11», con un'intestazione che ha cifre sue."""
        m = self._master(_png(MANIFESTO, esadecimale=True))
        self.assertNotIn(b"c2pa", m.read_bytes())
        self.assertEqual(pi.sorgente_del_master(m), (True, pi.GENERATA))

    def test_generata_e_composta(self):
        self.assertEqual(pi.sorgente_del_master(self._master(_png(COMPOSTO))), (True, pi.COMPOSTA))

    def test_senza_manifesto_niente_etichetta(self):
        self.assertEqual(pi.sorgente_del_master(self._master(_png())), (False, ""))

    def test_il_termine_senza_firma_non_basta(self):
        """Il termine IPTC scritto da chiunque, senza manifesto C2PA, non si copia."""
        m = self._master(_png() + b"digitalsourcetype/trainedAlgorithmicMedia")
        self.assertEqual(pi.sorgente_del_master(m), (False, ""))


@unittest.skipUnless(PILLOW, "Pillow assente")
class TestCartella(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "web").mkdir()
        (self.d / "firmata.png").write_bytes(_png(MANIFESTO))
        (self.d / "ignota.png").write_bytes(_png())
        for n in ("firmata", "ignota", "orfana"):
            (self.d / "web" / f"{n}.jpg").write_bytes(_jpeg())

    def test_scrive_solo_dove_il_master_e_firmato(self):
        prima = {v.copia.split("/")[-1]: v for v in pi.esamina(self.d)}
        self.assertFalse(prima["firmata.jpg"].a_posto)
        self.assertTrue(prima["ignota.jpg"].a_posto and prima["orfana.jpg"].a_posto)
        self.assertEqual(pi.scrivi(self.d), 1)
        dopo = {v.copia.split("/")[-1]: v for v in pi.esamina(self.d)}
        self.assertEqual(dopo["firmata.jpg"].scritta, pi.GENERATA)
        self.assertEqual((dopo["ignota.jpg"].scritta, dopo["orfana.jpg"].scritta), ("", ""))
        self.assertEqual(pi.scrivi(self.d), 0)

    def test_check_esce_1_finche_manca(self):
        self.assertEqual(pi.main([str(self.d), "--check"]), 1)
        self.assertEqual(pi.main([str(self.d), "--scrivi", "--check"]), 0)

    def test_un_etichetta_che_il_master_non_giustifica_e_un_errore(self):
        copia = self.d / "web" / "ignota.jpg"
        copia.write_bytes(pi.etichetta_jpeg(copia.read_bytes(),
                                            pi.pacchetto_xmp(pi.GENERATA, self.d / "ignota.png")))
        self.assertEqual(pi.main([str(self.d), "--check"]), 1)

    def test_il_generatore_delle_copie_la_mette_da_se(self):
        import build_image_derivatives as bid
        vecchio = sys.argv
        sys.argv = ["build_image_derivatives.py", str(self.d)]
        try:
            self.assertEqual(bid.main(), 0)
        finally:
            sys.argv = vecchio
        self.assertEqual(pi.leggi_etichetta((self.d / "web" / "firmata.jpg").read_bytes()), pi.GENERATA)
        self.assertEqual(pi.leggi_etichetta((self.d / "web" / "ignota.jpg").read_bytes()), "")


@unittest.skipUnless(PILLOW, "Pillow assente")
class TestIlRepo(unittest.TestCase):
    """Il cancello: nel repo ogni copia dice quello che il suo master firma."""

    def test_ogni_copia_tiene_l_etichetta_del_master(self):
        storte = [v for c in pi.cartelle_web() for v in pi.esamina(c) if not v.a_posto]
        self.assertEqual(storte, [], "rilanciare: python3 scripts/provenienza_immagini.py --scrivi")

    def test_ci_sono_copie_etichettate(self):
        firmate = [v for c in pi.cartelle_web() for v in pi.esamina(c) if v.attesa]
        self.assertGreaterEqual(len(firmate), 28)


if __name__ == "__main__":
    unittest.main()
