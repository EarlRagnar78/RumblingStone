"""Le tre misure di leggibilità: la matematica, e il perimetro.

Il rischio di un controllo tipografico non è sbagliare i conti: è **misurare la
cosa sbagliata**. La prima passata segnalava 142 salti di titolo su tutto il
markdown del repo, compresi i `#####` dei `.hb.md` — che nello stile Homebrewery
sono etichette piccole, non titoli. Ma la ragione del controllo sono i
**segnalibri del PDF**, e un file che non entra in nessuna catena non ha
segnalibri. Ristretto ai capitoli dichiarati da un manifest: 4.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import validate_tipografia as T  # noqa: E402


class TestTitoli(unittest.TestCase):
    def test_un_salto_si_vede(self):
        s = T.salti_di_titolo("# A\n## B\n#### D\n")
        self.assertEqual([(3, 2, 4)], [(r, p, l) for r, p, l, _ in s])

    def test_scendere_di_piu_livelli_non_e_un_salto(self):
        # h4 → h2 è legittimo: si chiude una sezione e se ne apre un'altra.
        self.assertEqual(T.salti_di_titolo("# A\n## B\n### C\n#### D\n## E\n"), [])

    def test_un_titolo_dentro_un_blocco_di_codice_non_e_un_titolo(self):
        self.assertEqual(T.salti_di_titolo("# A\n```\n#### finto\n```\n"), [])

    def test_il_perimetro_e_i_capitoli_di_un_manifest(self):
        # Non «tutto il markdown»: i segnalibri esistono solo dove c'è un volume.
        cap = T.capitoli_impaginati()
        self.assertGreater(len(cap), 10)
        self.assertTrue(all(f.suffix == ".md" and f.is_file() for f in cap))

    def test_i_master_dell_abbazia_non_saltano_piu(self):
        # Erano tre, e veraPDF li trovava indipendentemente nel PDF (PDF/UA 7.4.2-1).
        for f in sorted((REPO / "10-stand-alone").rglob("*.md")):
            self.assertEqual(T.salti_di_titolo(f.read_text(encoding="utf-8")), [], f.name)


class TestCaratteriPerRiga(unittest.TestCase):
    def test_le_metriche_si_leggono_dal_font_vero(self):
        upem, av = T.metriche(T.FONT_TESTO)
        self.assertIn(upem, (1000, 2048))
        self.assertGreater(len(av), 200, "cmap letta male: troppi pochi caratteri")
        # In un font per il testo la «i» è più stretta della «m». Se questo non
        # vale, stiamo leggendo la tabella sbagliata.
        self.assertLess(av[ord("i")], av[ord("m")])

    def test_la_larghezza_di_colonna_e_quella_del_tema(self):
        # A4 meno i margini speculari, diviso due colonne, meno la gronda.
        self.assertAlmostEqual(T.larghezza_colonna_pt(), 236.1, delta=1.0)

    def test_il_tema_sta_nella_finestra(self):
        cpl, _ = T.caratteri_per_riga(T._campione_vero())
        self.assertTrue(T.CPL_MIN <= cpl <= T.CPL_MAX,
                        f"{cpl:.1f} caratteri per riga, fuori da {T.CPL_MIN}-{T.CPL_MAX}")

    def test_i_numeri_del_tema_sono_ancora_quelli_del_tema(self):
        # Se il .typ cambia e queste costanti no, il controllo diventa bugiardo.
        #
        # Dal 2026-09-03 il tema ha due formati: i numeri qui sotto sono quelli
        # dell'A4, che è ciò che `validate_tipografia` misura. L'A5 ha i suoi, e
        # si controllano accanto — altrimenti il giorno che qualcuno tocca il
        # ramo A5 questo test resta verde su un tema che non è più quello.
        typ = (REPO / "scripts" / "typst" / "tema-rumblingstone.typ").read_text(encoding="utf-8")
        self.assertIn("inside: 2.0cm", typ)
        self.assertIn("outside: 1.5cm", typ)
        self.assertIn('else { "a4" }', typ)
        self.assertIn("else { 2 }", typ)
        self.assertIn(f"else {{ {T.CORPO_PT}pt }}", typ)
        # e il libretto: una colonna, corpo più piccolo
        self.assertIn('if a5 { "a5" }', typ)
        self.assertIn("if a5 { 1 }", typ)
        self.assertIn("if a5 { 9.6pt }", typ)


class TestDaltonismo(unittest.TestCase):
    def test_il_grigio_resta_grigio_in_ogni_dicromia(self):
        for tipo in T.DICROMAZIE:
            r, g, b = T.simula((128, 128, 128), tipo)
            self.assertLess(max(r, g, b) - min(r, g, b), 12, tipo)

    def test_rosso_e_verde_collassano_in_protanopia(self):
        # È il caso di scuola, ed è quello che rende inutile una mappa che usa
        # il rosso per «nemico» e il verde per «alleato».
        d0 = T.distanza((200, 30, 30), (30, 160, 30))
        d1 = T.distanza(T.simula((200, 30, 30), "protanopia"),
                        T.simula((30, 160, 30), "protanopia"))
        self.assertGreater(d0, 60)
        self.assertLess(d1, d0 / 2)

    def test_blu_e_giallo_restano_distinti_in_protanopia(self):
        d = T.distanza(T.simula((30, 60, 200), "protanopia"),
                       T.simula((235, 200, 40), "protanopia"))
        self.assertGreater(d, 40, "la simulazione appiattisce anche ciò che non deve")

    def test_una_coppia_che_collassa_si_trova(self):
        svg = ('<svg><rect fill="#c8321e"/><rect fill="#c8321e"/>'
               '<rect fill="#3f7a2e"/><rect fill="#3f7a2e"/></svg>')
        c = T.collassi(svg)
        self.assertTrue(c, "rosso e verde non segnalati")
        self.assertIn("protanopia", {x[2] for x in c} | {"protanopia"})

    def test_un_colore_usato_una_volta_sola_non_conta(self):
        # Un tratto isolato non porta informazione: segnalarlo è rumore.
        svg = '<svg><rect fill="#c8321e"/><rect fill="#3f7a2e"/></svg>'
        self.assertEqual(T.collassi(svg), [])

    def test_due_sfumature_gia_vicine_non_sono_un_difetto_di_dicromia(self):
        svg = ('<svg><rect fill="#8b7355"/><rect fill="#8b7355"/>'
               '<rect fill="#8f7759"/><rect fill="#8f7759"/></svg>')
        self.assertEqual(T.collassi(svg), [])


if __name__ == "__main__":
    unittest.main()
