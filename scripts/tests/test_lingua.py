"""`validate_lingua.py`: i refusi che una macchina trova, e i falsi positivi che deve tacere.

Metà di questi test esistono per la seconda ragione. La prima passata sul repo
produsse **423 rilievi**, quasi tutti creati dal validatore stesso: mascherava il
codice inline con **uno spazio**, e poi segnalava come «doppio spazio» quello che
aveva appena introdotto. Un validatore rumoroso viene disattivato entro una
settimana, e allora non trova più nemmeno i refusi veri.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from validate_lingua import controlla  # noqa: E402


def _testo(s: str) -> tuple[list[str], list[str]]:
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "prova.md"
        f.write_text(s, encoding="utf-8")
        return controlla(f)


class TestRefusiVeri(unittest.TestCase):

    def test_accento_grave_al_posto_dellacuto(self):
        for sbagliato in ("perchè", "poichè", "finchè", "nè"):
            with self.subTest(parola=sbagliato):
                errori, _ = _testo(f"Una riga con {sbagliato} dentro.")
                self.assertTrue(errori, sbagliato)

    def test_po_con_laccento(self):
        errori, _ = _testo("Aspetta un pò.")
        self.assertTrue(errori)

    def test_qual_e_con_lapostrofo(self):
        errori, _ = _testo("Non si sa qual'è la porta.")
        self.assertTrue(errori)

    def test_d_eufonica_davanti_a_consonante(self):
        errori, _ = _testo("# Gran Finale ad Damarath")
        self.assertTrue(errori)

    def test_spazio_prima_della_punteggiatura(self):
        errori, _ = _testo("Il totale e' 5.8 : la soglia.")
        self.assertTrue(errori)

    def test_spazio_prima_dei_due_punti_dopo_una_parola(self):
        # Il refuso vero del box di Tordek (#167): le eccezioni per la cella
        # «?» e per il rapporto «5.8 : 1» non devono spegnerlo.
        errori, _ = _testo("Il gatto familiare : è sparito.")
        self.assertTrue(errori)

    def test_due_punti_fra_un_numero_e_una_parola(self):
        errori, _ = _testo("Il totale è 5 : poi si vede.")
        self.assertTrue(errori)

    def test_doppio_spazio_fra_parole(self):
        errori, _ = _testo("Due  spazi fra le parole.")
        self.assertTrue(errori)


class TestFalsiPositivi(unittest.TestCase):
    """Ogni caso qui sotto è una riga corretta che NON deve produrre un rilievo."""

    def test_una_riga_pulita(self):
        errori, avvisi = _testo("Perché la porta è chiusa, né si apre.")
        self.assertEqual(errori, [])
        self.assertEqual(avvisi, [])

    def test_il_codice_inline_non_crea_doppi_spazi(self):
        # Il difetto della prima passata: mascherare con uno spazio.
        errori, _ = _testo("Vedi `render_map_svg.py` e poi prosegui.")
        self.assertEqual(errori, [])

    def test_i_blocchi_di_codice_si_saltano(self):
        errori, _ = _testo("Testo.\n\n```\nx = {'a' : 1}   # due  spazi\n```\n\nAltro testo.")
        self.assertEqual(errori, [])

    def test_il_front_matter_yaml_si_salta(self):
        errori, _ = _testo("---\nname: x\ndesc:  due spazi\n---\n\nTesto pulito.")
        self.assertEqual(errori, [])

    def test_la_guida_alla_pronuncia_usa_lacento_apposta(self):
        # `module-standard` §15 chiede la guida alla pronuncia: lì l'accento
        # grave dice il SUONO, e segnalarlo sarebbe corretto e inutile.
        errori, _ = _testo("| **Nethys** | *nè-this* | la magia |")
        self.assertEqual(errori, [])

    def test_gli_url_non_si_analizzano(self):
        errori, _ = _testo("Vedi https://esempio.invalid/a?x=1&y=2 per il resto.")
        self.assertEqual(errori, [])

    def test_un_link_markdown_non_e_prosa(self):
        errori, _ = _testo("Vedi [la guida](docs/guides/GUIDA-MAPPE.md) e prosegui.")
        self.assertEqual(errori, [])

    def test_i_due_spazi_prima_di_unancora_non_sono_un_refuso(self):
        # PROMPT-IMMAGINI-07ILP.md, 7 titoli: mascherato con la «x», il codice
        # diventava una parola e i due spazi un «doppio spazio fra parole».
        errori, _ = _testo("### 10 · L'ARRIVO — i primi sei secondi  `[8a-l-arrivo]`")
        self.assertEqual(errori, [])

    def test_un_segno_solo_in_una_cella_di_tabella(self):
        # ARC07-TESORO-WBL-AUDIT.md:44 — la cella dice «non lo sappiamo».
        errori, _ = _testo("| P3 Piano Fuoco | bottino | ? | `P3` |")
        self.assertEqual(errori, [])

    def test_il_rapporto_fra_due_numeri(self):
        # ARMATE-SYNC.md, 5 righe: «5.8 : 1» è un rapporto, non un refuso.
        for rapporto in ("**5.8 : 1**", "1.46 : 1", "3 : 2"):
            with self.subTest(rapporto=rapporto):
                errori, _ = _testo(f"| A | rapporto {rapporto} | CR |")
                self.assertEqual(errori, [])

    def test_ad_davanti_a_vocale_e_corretto(self):
        errori, _ = _testo("Va ad Anfiteatro ed entra.")
        self.assertEqual(errori, [])


class TestApostrofoAlPostoDellAccento(unittest.TestCase):
    """ADR-0079: una regex sola, ed è un avviso, mai un errore."""

    def _avvisi(self, riga: str) -> list[str]:
        e, a = _testo(riga + "\n")
        self.assertEqual(e, [])
        return [x for x in a if "apostrofo al posto" in x]

    def test_le_forme_sbagliate_sono_un_avviso(self):
        for riga in ("Il drago e' ferito.", "Non lo so perche' e partito.",
                     "Era gia' tardi.", "Ne vale di piu' la pena.", "Cosi' fu.",
                     "Si, ma Perche' proprio lui?"):
            self.assertEqual(len(self._avvisi(riga)), 1, riga)

    def test_le_forme_corrette_tacciono(self):
        for riga in ("Dammi un po' di tempo.",        # po' è corretto
                     "Da' la scena alla giocatrice.",  # da' imperativo di dare
                     "L'ascia è scritta in `e'` nel codice.",  # solo il codice
                     "Disse: 'Sara' la fine'.",        # apostrofo di citazione
                     "Il re d'e'ra", ):                # lettera attaccata
            self.assertEqual(self._avvisi(riga), [], riga)

    def test_il_maiuscolo_a_inizio_frase_ha_la_sua_regola(self):
        _, a = _testo("E' Terros prima della ricalibrazione.\n")
        self.assertEqual(len([x for x in a if "apostrofo al posto" in x]), 0)
        self.assertEqual(len([x for x in a if "maiuscola accentata" in x]), 1)


if __name__ == "__main__":
    unittest.main()
