"""La storia delle scelte resta nel sorgente e non va in stampa (2026-09-25).

Il DM: *«per tutti i booklet rimuovere le parti che riguardano le scelte fatte
nel repo, tipo "si è scelto così perché" oppure "prima era così e ora è
cambiato"; vanno in una parte non renderizzata, anche nello stesso file»*.

La funzione è `dmcore.testo.togli_storico`, e la chiamano tutte e due le catene
(HTML e Typst). Ogni caso qui sotto è un difetto trovato scrivendola, sul corpus
vero, prima di consegnarla.
"""
from __future__ import annotations

import doctest
import json
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from build_booklet_html import md_to_html  # noqa: E402
from dmcore import testo  # noqa: E402
from dmcore.testo import togli_blocchi_storici, togli_storico  # noqa: E402
from export_booklet_typst import md_to_typ  # noqa: E402


def fonti_stampate() -> list[Path]:
    """Ogni file che un manifest mette in un volume, introduzioni comprese."""
    fonti: set[Path] = set()
    for m in REPO.glob("**/*.manifest.json"):
        if m.name == "tools.manifest.json" or "/build/" in m.as_posix():
            continue
        d = json.loads(m.read_text(encoding="utf-8"))
        for c in d.get("chapters", []):
            if c.get("file"):
                fonti.add((m.parent / c["file"]).resolve())
        if d.get("intro_md"):
            fonti.add((m.parent / d["intro_md"]).resolve())
    return sorted(f for f in fonti if f.is_file())


# Le formule che dicono la storia di una scelta, e le date di lavoro del repo.
STORIA = re.compile(
    r"\b2026-\d\d-\d\d\b|\bdecision[ei] (?:del )?DM\b|\bstesura (?:di prima|precedente)\b"
    r"|\b(?:il box|la riga|il testo) di prima\b|\bprima (?:diceva|era scritt)"
    r"|\bRiordinat[oa] il\b|\bAllineat[oa] il\b|\bCorrezione del\b|\bsu richiesta del DM\b")

# Quello che resta in stampa il 2026-09-25, file per file, e perché resta.
# Un numero che sale vuol dire storia nuova senza marcatore: si avvolge in
# `<!-- storico -->`, non si alza il numero.
RESIDUI = {
    # una marca `[CANONE …]` spezzata su due righe dentro uno statblocco:
    # toglierla unirebbe le righe (vedi test_il_codice_non_cambia_forma)
    "ARC07-DEF-1-PIANO-TERRA-TERROS.md": 1,
    # la stessa cosa nello statblocco di Zog'tar
    "ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md": 1,
    # data d'edizione nel piede di un handout
    "HANDOUT-1-cronache-quattro-eroi.hb.md": 1,
    # la data della serata per cui il booklet è fatto, e il calendario del volume
    "00-INTRO-DOVE-SIAMO.md": 1,
    "00-INTRO-VOLUME.md": 1,
    # le date in cui un pezzo è stato giocato: è la cronaca, non la storia del repo
    "01-REGIA-SESSIONE.md": 2,
    # da chi viene un'immagine
    "Arco-Post-Hammerfist-P2D-PALIO-MAPPE.md": 2,
    # l'intestazione della scheda è un [INFERRED]: si chiude con la decisione del DM
    "balvar-fuocospento-cr13.md": 1,
    # i capitoli da beta del Drappo (IP e licenze, playtest alfa, stato del
    # modulo, schede di feedback) sono usciti dal volume del DM il 2026-09-25,
    # su decisione del DM: le loro 5 righe non vanno più in stampa
}


class TestLaFunzione(unittest.TestCase):
    def test_gli_esempi_della_funzione(self):
        esito = doctest.testmod(testo)
        self.assertEqual(esito.failed, 0)
        self.assertGreater(esito.attempted, 10)

    def test_le_due_catene_saltano_il_blocco(self):
        md = "Prima.\n\n<!-- storico -->\n> ✏️ Il box diceva altro.\n<!-- /storico -->\n\nDopo."
        self.assertNotIn("diceva altro", md_to_typ(md))
        self.assertNotIn("diceva altro", md_to_html(md, REPO))
        self.assertIn("Dopo.", md_to_typ(md))
        self.assertIn("Dopo.", md_to_html(md, REPO))

    def test_un_marcatore_in_linea_non_si_porta_via_il_resto(self):
        """Nel Palio, «> <!-- storico -->v1. <!-- /storico -->Modulo…» a inizio
        riga veniva preso per un blocco, e la regola arrivava al primo
        «/storico» che chiudeva una riga: via tutta l'intestazione."""
        md = ("> <!-- storico -->**Versione**: v1. <!-- /storico -->Modulo doppio-uso.\n"
              "> Resta anche questa.\n\n<!-- storico -->\n> via\n<!-- /storico -->\n\nE questa.")
        fuori = togli_storico(md)
        self.assertIn("Modulo doppio-uso.", fuori)
        self.assertIn("Resta anche questa.", fuori)
        self.assertIn("E questa.", fuori)
        self.assertNotIn("via", fuori.replace("Resta", ""))

    def test_l_attribuzione_se_ne_va_il_contenuto_resta(self):
        self.assertEqual(togli_storico("(Varis ↔ Il Collezionista, CANONE DM 2026-07-23), mille"),
                         "(Varis ↔ Il Collezionista), mille")
        self.assertEqual(togli_storico("della Terra (CANONE DM 2026-07-23: si aggancia al Cerchio"),
                         "della Terra (si aggancia al Cerchio")


class TestSulCorpusVero(unittest.TestCase):
    def setUp(self):
        self.fonti = fonti_stampate()
        self.assertGreater(len(self.fonti), 70, "i manifest non si leggono più")

    def test_nessun_marcatore_arriva_in_stampa(self):
        for f in self.fonti:
            fuori = togli_storico(f.read_text(encoding="utf-8"))
            self.assertNotRegex(fuori, r"<!--\s*/?storico", f"{f.name}: marcatore non chiuso")

    def test_il_codice_non_cambia_forma(self):
        """Una marca che va a capo, tolta in un blocco preformattato, univa due
        righe: lo statblocco di Terros passava da 71 a 98 celle e finiva su una
        pagina A4 sua, con due righe sole sulla pagina prima."""
        blocco = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.S | re.M)
        for f in self.fonti:
            md = f.read_text(encoding="utf-8")
            # un blocco dentro «storico» sparisce, ed è voluto: si confronta
            # quello che resta dopo i blocchi segnati a mano
            prima = [b.count("\n") for b in blocco.findall(togli_blocchi_storici(md))]
            dopo = [b.count("\n") for b in blocco.findall(togli_storico(md))]
            self.assertEqual(prima, dopo, f"{f.name}: un blocco preformattato ha cambiato righe")

    def test_la_storia_rimasta_e_quella_dichiarata(self):
        trovati: dict[str, int] = {}
        for f in self.fonti:
            n = sum(1 for r in togli_storico(f.read_text(encoding="utf-8")).split("\n")
                    if STORIA.search(r))
            if n:
                trovati[f.name] = trovati.get(f.name, 0) + n
        for nome, n in trovati.items():
            self.assertLessEqual(
                n, RESIDUI.get(nome, 0),
                f"{nome}: {n} righe di storia arrivano in stampa. Si avvolgono in "
                f"<!-- storico --> … <!-- /storico --> (rumblingstone-editoria §4.6)")



class TestIFogliDeiGiocatori(unittest.TestCase):
    """Un foglio ✉ va in mano al giocatore: l'istruzione di consegna («Si consegna
    al risveglio…», «Il DM te la consegna dopo…») è del DM e sta nella regia.
    Il 2026-09-25 undici fogli della serata la stampavano in testa."""

    # «si consegna il Peso di contrada», minuscolo e dentro una frase, è il Palio:
    # finzione, non un'istruzione al DM
    CONSEGNA = re.compile(r"\bSi consegna|te l[ao] consegna|Da mostrare al tavolo")

    def test_nessuna_istruzione_di_consegna_sui_fogli(self):
        for m in REPO.glob("**/*.manifest.json"):
            if m.name == "tools.manifest.json" or "/build/" in m.as_posix():
                continue
            for c in json.loads(m.read_text(encoding="utf-8")).get("chapters", []):
                f = (m.parent / c.get("file", "")).resolve()
                if c.get("tag") != "player" or not f.is_file():
                    continue
                for riga in togli_storico(f.read_text(encoding="utf-8")).split("\n"):
                    self.assertNotRegex(riga, self.CONSEGNA, f"{m.name} → {f.name}")

if __name__ == "__main__":
    unittest.main()
