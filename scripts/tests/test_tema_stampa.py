"""Il modo stampa delle mappe (ADR-0105, M7-H, 2026-10-30).

Una mappa larga 44 colonne, messa nel booklet A4, scendeva a scala 0,3: le
scritte uscivano a 3-3,8 pt e i filtri della pergamena (grana, ombre sfumate)
diventavano strati raster a 288 dpi. Il tema stampa scrive ogni corpo in
punti per una mappa larga quanto la gabbia (17,5 cm), sposta indicazioni e
legenda in un secondo SVG e non usa filtri. Vale per ogni tema; nel booklet
va la pianta (lo stile di Dauth), scelta di Jfs al cieco. Il test fissa queste
cose sulla mappa vera che l'ha fatto nascere, in tutti e tre i temi.
"""

import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402

M7H = SCRIPTS.parent / "07_il Portale Della Forgia Eterna" / "Mappe" / \
    "ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.md"
ALTEZZA_MAX_PT = 595  # il tetto delle figure su pagina dedicata (21 cm)


def _misure(svg: str) -> tuple[float, float, float]:
    """(larghezza, altezza, scala del gruppo) dell'SVG."""
    w, h = (float(x) for x in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
    k = re.search(r'<g transform="scale\(([\d.]+)\)">', svg)
    return w, h, float(k.group(1)) if k else 1.0


def _corpi_pt(svg: str) -> list[float]:
    """I corpi delle scritte una volta stampato l'SVG nella gabbia."""
    w, h, k = _misure(svg)
    pt_per_px = min(R.LARGHEZZA_STAMPA_PT / w, ALTEZZA_MAX_PT / h)
    return [float(c) * k * pt_per_px for c in re.findall(r'font-size="([\d.]+)"', svg)]


class TestTemaStampa(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        g = R.extract_maps(M7H.read_text(encoding="utf-8"))[0]
        cls.temi = {t: (R.render_svg(g, M7H.name, t, "mappa", True),
                        R.render_svg(g, M7H.name, t, "legenda", True)) for t in R.TEMI}
        cls.mappa, cls.legenda = cls.temi["pianta"]
        cls.pergamena = R.render_svg(g, M7H.name)

    def test_nessuna_scritta_sotto_i_7_pt(self):
        for tema, (mappa, legenda) in self.temi.items():
            for nome, svg in (("mappa", mappa), ("legenda", legenda)):
                # le emoji della griglia sono disegni, non scritte: qui non ce ne sono
                self.assertGreaterEqual(min(_corpi_pt(svg)), 7.0, f"{tema} {nome}")

    def test_la_pergamena_invece_scende_a_3_pt(self):
        self.assertLess(min(_corpi_pt(self.pergamena)), 4.0)

    def test_niente_filtri_ne_vignettatura(self):
        for svg in (x for coppia in self.temi.values() for x in coppia):
            self.assertNotIn('filter="url(', svg)
            self.assertNotIn("url(#vign)", svg)

    def test_la_mappa_non_porta_la_legenda_e_viceversa(self):
        self.assertNotIn("Legenda", self.mappa)
        self.assertIn("Legenda", self.legenda)
        self.assertIn("Luoghi, zone e percorsi", self.legenda)
        self.assertNotIn("quadretto di", self.legenda)
        perg_mappa, perg_legenda = self.temi["pergamena"]
        self.assertNotIn("INDICAZIONI", perg_mappa)
        self.assertIn("INDICAZIONI", perg_legenda)

    def test_le_zone_sono_lettere_spiegate_in_legenda(self):
        self.assertNotIn("Telo del glifo", self.mappa)
        self.assertIn("Telo del glifo", self.legenda)
        self.assertRegex(self.mappa, r'font-style="italic">b</text>')

    def test_la_legenda_dice_la_regola_intera(self):
        # in stampa la parentesi della voce non si taglia: porta la regola
        piatto = " ".join(re.sub(r"<[^>]+>", " ", self.legenda).split())
        self.assertIn("blocca la vista, si taglia)", piatto)

    def test_a_capo_tiene_le_parole(self):
        righe = R._a_capo("uno due tre quattro cinque", 9)
        self.assertEqual(righe, ["uno due", "tre", "quattro", "cinque"])
        self.assertEqual(" ".join(righe), "uno due tre quattro cinque")


class TestStandardDiRepo(unittest.TestCase):
    """ADR-0106: la pianta in stampa vale per ogni mappa del repo."""

    RADICE = SCRIPTS.parent

    def _mappa(self, rel: str, i: int = 0):
        md = self.RADICE / rel
        return md, R.extract_maps(md.read_text(encoding="utf-8"))[i]

    def test_mappa_alta_resta_sopra_i_7_pt(self):
        # 21×53: stretta nella pagina per altezza, scendeva a 4,3 pt
        md, g = self._mappa("07_il Portale Della Forgia Eterna/Mappe/Portale-Forgia-L2-REVISED-UltraClear.md")
        self.assertGreaterEqual(min(_corpi_pt(R.render_svg(g, md.name, "pianta", "mappa", True))), 7.0)

    def test_legenda_lunga_va_su_due_colonne(self):
        # 17 luoghi e 15 zone: su una colonna la legenda superava i 21 cm
        md, g = self._mappa("08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md")
        self.assertGreaterEqual(min(_corpi_pt(R.render_svg(g, md.name, "pianta", "legenda", True))), 7.0)

    def test_simboli_della_legenda_del_master(self):
        # 🛡️ e 🥋 non sono nel glossario: il nome viene dalla legenda del master
        md, g = self._mappa("07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-DEFINITIVO.md")
        legenda = R.render_svg(g, md.name, "pianta", "legenda", True)
        self.assertIn("Thorik (F04)", legenda)
        self.assertIn("base corrosa del pilastro", legenda)

    def test_stesso_svg_con_ogni_seme_di_hash(self):
        # le acque si disegnavano nell'ordine di un set: l'SVG cambiava da
        # un processo all'altro e validate_maps falliva a caso
        codice = ("import sys; sys.path.insert(0, sys.argv[1]); import render_map_svg as R; "
                  "from pathlib import Path; md = Path(sys.argv[2]); "
                  "g = R.extract_maps(md.read_text(encoding='utf-8'))[2]; "
                  "import hashlib; print(hashlib.md5(R.render_svg(g, md.name, 'pianta').encode()).hexdigest())")
        md = self.RADICE / "08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md"
        uscite = {subprocess.run([sys.executable, "-c", codice, str(SCRIPTS), str(md)], capture_output=True,
                                 text=True, env={**os.environ, "PYTHONHASHSEED": str(seme)}).stdout
                  for seme in (1, 5)}
        self.assertEqual(len(uscite), 1, uscite)

    def test_la_foresta_si_disegna(self):
        md, g = self._mappa("09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/"
                            "Arco-Post-Hammerfist-P1B-Foresta-In-Fiamme-MAPPA.md")
        self.assertIn("<svg", R.render_svg(g, md.name, "pianta", "mappa", True))


if __name__ == "__main__":
    unittest.main()


class TestSchemi(unittest.TestCase):
    def test_schemi_allineati_e_leggibili(self):
        """Gli schemi di ARC-07 (ADR-0106 §5) sono quelli dello script, con il corpo minimo di stampa."""
        import render_schemi as S

        self.assertEqual(S.main(["--check"]), 0)
        for fn in S.SCHEMI.values():
            svg = fn()
            self.assertIn('width="496"', svg)
            corpi = [float(x) for x in re.findall(r'font-size="([\d.]+)"', svg)]
            self.assertTrue(corpi)
            self.assertGreaterEqual(min(corpi), 7.4)
            self.assertNotIn("<filter", svg)
