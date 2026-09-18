"""Il cancello della regola d'oro della prosa, provato dai due lati.

Il DM il 2026-09-18: *«crea una golden rule che obbliga a leggere davvero tutta
la parte editoriale [...] altrimenti questo problema si ripresentera' come
fatto prima»*.

🔴 **«Come fatto prima» e' un fatto misurato**: `read-aloud-adulti.md`
prescriveva da agosto box <= 12 righe e un solo nome proprio, e **nessuno
strumento lo guardava**; `ADR-0014` era stato applicato a **un documento su
cento**. Nessuno se n'era accorto perche' **una norma non misurata non fa
rumore quando viene ignorata**.

⚠️ E la prima diagnosi era sbagliata: **non** era scopribilita'. Tutti e 56 i
`references/` sono gia' citati dal loro `SKILL.md` — un gate sulla citazione
sarebbe verde e inutile. Il test qui sotto lo prova, perche' e' la ragione per
cui il cancello e' fatto **cosi'** e non nel modo ovvio.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRO = ROOT / "skills" / "REGISTRO-NORME-EDITORIALI.md"


def _gate():
    spec = importlib.util.spec_from_file_location(
        "vne", ROOT / "scripts" / "validate_norme_editoriali.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _gate()


class TestLaDiagnosiOvviaEraSbagliata(unittest.TestCase):
    def test_ogni_reference_e_gia_citato_dal_suo_skill(self):
        """La prova che un gate sulla citazione sarebbe **verde e inutile**.

        Se un giorno questo test diventasse rosso, la diagnosi cambierebbe e il
        cancello andrebbe ripensato: vorrebbe dire che la scopribilita' e'
        tornata a essere un problema vero.
        """
        mancanti = []
        for sk in sorted((ROOT / "skills").glob("*/SKILL.md")):
            testo = sk.read_text(encoding="utf-8")
            for ref in sorted((sk.parent / "references").glob("*.md")):
                if ref.name not in testo:
                    mancanti.append(f"{sk.parent.name}/{ref.name}")
        self.assertEqual(mancanti, [], f"reference non citati: {mancanti}")


class TestIlCancelloSulRepoVero(unittest.TestCase):
    def test_oggi_e_verde(self):
        self.assertEqual(G.controlla(), [])

    def test_le_norme_non_misurate_sono_contate_e_non_zero(self):
        """🔴 Il numero che prima non esisteva e sembrava zero.

        Undici norme su trentacinque non sono guardate da niente. Il valore di
        questo registro non e' che il conto sia basso: e' che **esista**.
        """
        testo = REGISTRO.read_text(encoding="utf-8")
        self.assertGreater(testo.count("🔴"), 5,
                           "il registro non dichiara piu' nessun buco: o sono "
                           "stati chiusi davvero (bene, aggiorna il test) o "
                           "qualcuno li ha nascosti")

    def test_ogni_norma_rossa_porta_la_ragione(self):
        """⚠️ Si guarda l'**ultima** cella, quella dello stato — come fa il
        cancello. La riga di riepilogo «🔴 non misurate | 11» ha il pallino
        nella *prima* cella e un numero nell'ultima: e' un conteggio, non una
        norma, e chiederle una ragione sarebbe chiederla alla tabella."""
        for i, riga in enumerate(REGISTRO.read_text(encoding="utf-8").splitlines(), 1):
            if not riga.startswith("|"):
                continue
            stato = [c.strip() for c in riga.strip("|").split("|")][-1]
            if "🔴" in stato:
                with self.subTest(riga=i):
                    self.assertIn("—", stato,
                                  "«non misurato» nudo non e' una decisione")


class TestIlCancelloMorde(unittest.TestCase):
    """Le tre prove all'indietro. Un cancello che non si e' visto bocciare non
    e' un cancello — e' la regola che questo repo applica dal lotto B di
    PIANO-QUALITA-DEL-CODICE."""

    def _con_registro(self, testo: str):
        originale = REGISTRO.read_text(encoding="utf-8")
        try:
            REGISTRO.write_text(testo, encoding="utf-8")
            return G.controlla()
        finally:
            REGISTRO.write_text(originale, encoding="utf-8")

    def test_una_norma_non_registrata_boccia(self):
        """Il caso che ha creato il problema: un file normativo che nessuno
        nomina, e quindi nessuno misura."""
        testo = REGISTRO.read_text(encoding="utf-8").replace(
            "read-aloud-adulti.md", "qualcosaltro.md")
        errori = self._con_registro(testo)
        self.assertTrue(any("read-aloud-adulti.md" in e for e in errori), errori)

    def test_un_rimando_inventato_boccia(self):
        """ADR-0053 applicato al registro: un rimando che non esiste **sembra
        copertura**, ed e' peggio di un buco dichiarato."""
        testo = REGISTRO.read_text(encoding="utf-8").replace(
            "🟢 congegno `chiusura su decision point`",
            "🟢 congegno `questo non esiste`")
        errori = self._con_registro(testo)
        self.assertTrue(any("questo non esiste" in e for e in errori), errori)

    def test_un_rosso_senza_ragione_boccia(self):
        testo = REGISTRO.read_text(encoding="utf-8") + \
            "\n| `x.md` | norma | 🔴 non misurato |\n"
        errori = self._con_registro(testo)
        self.assertTrue(any("senza una ragione" in e for e in errori), errori)

    def test_un_rosso_PUO_nominare_uno_strumento_inesistente(self):
        """⚠️ Il lato opposto, e serve: la riga di ADR-0022 cita
        `validate_pg.py` **per dire che non esiste**. Un cancello che
        bocciasse anche quello impedirebbe di scrivere il vero."""
        testo = REGISTRO.read_text(encoding="utf-8") + \
            "\n| `y.md` | norma | 🔴 non misurato — `validate_inesistente.py` non c'è |\n"
        errori = self._con_registro(testo)
        self.assertEqual(errori, [], errori)


if __name__ == "__main__":
    unittest.main()
