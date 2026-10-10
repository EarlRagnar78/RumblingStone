"""L'installatore degli asset di 2-Minute Tabletop (R4, D9): estrae solo
immagini e licenze, rifiuta gli zip pericolosi, e il controllo boccia la
tabella che usa un pacchetto premium (la licenza non lo ammette fuori dal
tavolo) o un file che non c'è."""

import io
import json
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import asset_2mtt as A  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"\0" * 32


def _zip(cartella: Path, nome: str, membri: dict, link: str | None = None) -> Path:
    p = cartella / nome
    with zipfile.ZipFile(p, "w") as z:
        for n, dati in membri.items():
            z.writestr(n, dati)
        if link:
            info = zipfile.ZipInfo(link)
            info.external_attr = (0o120777 << 16)
            z.writestr(info, "/etc/passwd")
    return p


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self._vecchi = (A.CARTELLA, A.TABELLA, A.REPO)
        A.REPO = self.tmp
        A.CARTELLA = self.tmp / "asset-esterni" / "2mtt"
        A.TABELLA = self.tmp / "asset-2mtt.json"
        self.tabella({})

    def tearDown(self):
        A.CARTELLA, A.TABELLA, A.REPO = self._vecchi

    def tabella(self, simboli):
        A.TABELLA.write_text(json.dumps({"credito": "c", "licenza": "l", "simboli": simboli}),
                             encoding="utf-8")

    def zitto(self, f, *a):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return f(*a)


class TestInstalla(Base):
    def test_estrae_immagini_e_licenze_e_lascia_fuori_il_resto(self):
        z = _zip(self.tmp, "Dungeon-Map-Tiles.zip",
                 {"tiles/floor.png": PNG, "LICENSE.txt": "CC BY-NC", "pack.dungeondraft_pack": "x"})
        self.assertEqual(self.zitto(A.installa, z, "base", None), 0)
        dest = A.CARTELLA / "dungeon-map-tiles"
        self.assertTrue((dest / "tiles" / "floor.png").exists())
        self.assertFalse((dest / "pack.dungeondraft_pack").exists())
        p = json.loads((dest / "pacchetto.json").read_text(encoding="utf-8"))
        self.assertEqual(p["categoria"], "base")
        self.assertEqual(p["scartati"], ["pack.dungeondraft_pack"])
        self.assertEqual(len(p["file"]), 2)

    def test_rifiuta_un_percorso_che_esce_dalla_cartella(self):
        z = _zip(self.tmp, "cattivo.zip", {"../../fuori.png": PNG})
        self.assertEqual(self.zitto(A.installa, z, "base", None), 1)
        self.assertFalse((self.tmp / "fuori.png").exists())

    def test_rifiuta_un_link_simbolico(self):
        z = _zip(self.tmp, "link.zip", {"a.png": PNG}, link="b.png")
        self.assertEqual(self.zitto(A.installa, z, "base", None), 1)

    def test_rifiuta_uno_zip_senza_immagini(self):
        z = _zip(self.tmp, "testi.zip", {"LEGGIMI.txt": "solo testo"})
        self.assertEqual(self.zitto(A.installa, z, "base", None), 1)

    def test_un_nome_strano_e_un_errore_d_uso(self):
        z = _zip(self.tmp, "a.zip", {"a.png": PNG})
        self.assertEqual(self.zitto(A.installa, z, "base", "Nome Con Spazi"), 2)


class TestControlla(Base):
    def installa(self, categoria, nome="tiles"):
        z = _zip(self.tmp, f"{nome}.zip", {"floor.png": PNG})
        self.assertEqual(self.zitto(A.installa, z, categoria, nome), 0)

    def test_senza_pacchetti_controlla_solo_la_forma(self):
        self.tabella({"⬜": {"pacchetto": "tiles", "file": "floor.png"}})
        self.assertEqual(self.zitto(A.controlla), 0)

    def test_un_pacchetto_base_col_file_giusto_passa(self):
        self.installa("base")
        self.tabella({"⬜": {"pacchetto": "tiles", "file": "floor.png"}})
        self.assertEqual(self.zitto(A.controlla), 0)

    def test_un_pacchetto_premium_e_bocciato(self):
        self.installa("premium")
        self.tabella({"⬜": {"pacchetto": "tiles", "file": "floor.png"}})
        self.assertEqual(self.zitto(A.controlla), 1)

    def test_un_file_che_non_c_e_e_bocciato(self):
        self.installa("base")
        self.tabella({"⬜": {"pacchetto": "tiles", "file": "manca.png"}})
        self.assertEqual(self.zitto(A.controlla), 1)

    def test_una_voce_senza_file_e_bocciata(self):
        self.tabella({"⬜": {"pacchetto": "tiles"}})
        self.assertEqual(self.zitto(A.controlla), 1)


class TestRepo(unittest.TestCase):
    def test_la_tabella_committata_e_valida(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(A.controlla(), 0)

    def test_la_cartella_degli_asset_e_ignorata_da_git(self):
        gi = (SCRIPTS.parent / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("asset-esterni/*", gi)


if __name__ == "__main__":
    unittest.main()
