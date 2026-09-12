"""Gli archivi non si indicizzano — e non vale per tutti i gate (2026-09-12).

Il difetto vero, trovato dal suo effetto invece che da una revisione: archiviare
dodici istantanee fece passare il catalogo mostri da **305 a 311 record** e rese
rosso `validate_bestiario` con un doppione di «Battaglia Finale - Fase 0».
E' la forma esatta del rischio che la decisione **D10** aveva dichiarato — *«una
copia crea un secondo master»* — comparsa al primo giro di archiviazione vera.

⚠️ **La regola non e' «escludere gli archivi ovunque»**, ed e' il punto di questo
file: dipende da cosa fa il gate.

- **chi INDICIZZA** (costruisce un catalogo) deve **saltarli**: una copia
  diventa un record doppio;
- **chi SORVEGLIA** (nessun master sfugge al controllo) deve **includerli**, ed
  e' esattamente la ragione per cui la decisione **D1** lascio' gli SVG dentro
  `_ARCHIVIO/`, *«cosi' la cartella resta dentro il raggio di validate_maps»*.

Escludere gli archivi da `validate_maps` disferebbe una decisione del DM.

🔴 **E chi fa da rete non e' `validate_bestiario`: e' questo file.** Provato a
rovescio togliendo l'esclusione dal costruttore: il catalogo si inquina di nuovo,
ma il gate resta **verde**, perche' confronta il catalogo committato con una
scansione fatta *dallo stesso costruttore* — se entrambi i lati indicizzano le
copie, «in sync» e' vero e inutile. La prima volta lo prese solo perche' il
catalogo su disco era ancora quello pulito. Rossi, in quella prova, sono andati
i due test qui sotto: `test_il_catalogo_mostri_salta_archivio_e_old` e
`test_il_catalogo_non_contiene_record_da_un_archivio`.

⚠️ Il guardiano in `validate_bestiario` (`in_archivio`) e' **assicurazione**, non
la correzione: oggi sotto `Bestiario/` non c'e' nessun archivio, quindi non
salta niente. Serve il giorno in cui qualcuno ne creera' uno.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _carica(nome: str):
    spec = importlib.util.spec_from_file_location(nome, ROOT / "scripts" / f"{nome}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod


class TestChiIndicizzaSaltaGliArchivi(unittest.TestCase):
    def test_il_catalogo_mostri_salta_archivio_e_old(self):
        bmc = _carica("build_monster_catalog")
        for rel in ("07_arco/_ARCHIVIO/copia.md",
                    "07_arco/_ARCHIVIO/doni-v1-2026-09-12/istantanea.md",
                    "PG/Artefatti/Old/vecchia-scheda.md"):
            self.assertTrue(bmc.should_skip(Path(rel)), f"{rel} andrebbe saltato")

    def test_ma_non_salta_i_file_vivi(self):
        """La correzione non deve spegnere l'indicizzazione: i due test in coppia."""
        bmc = _carica("build_monster_catalog")
        for rel in ("Bestiario/mostri/qualcosa.md",
                    "07_arco/ARC07-DEF-3-RESURREZIONE-HELLA.md",
                    "Bestiario/villain/Salvatore/Salvatore.md"):
            self.assertFalse(bmc.should_skip(Path(rel)), f"{rel} andrebbe indicizzato")

    def test_il_bestiario_riconosce_una_cartella_d_archivio(self):
        vb = _carica("validate_bestiario")
        self.assertTrue(vb.in_archivio(Path("Bestiario/mostri/_ARCHIVIO/x.md")))
        self.assertTrue(vb.in_archivio(Path("Bestiario/png/Old/x.md")))
        self.assertFalse(vb.in_archivio(Path("Bestiario/mostri/x.md")))
        # `_ARCHIVIO` e' un segmento di percorso, non una sottostringa del nome
        self.assertFalse(vb.in_archivio(Path("Bestiario/mostri/note-su-Old-Willow.md")))


class TestChiSorvegliaLiTieneDentro(unittest.TestCase):
    """L'altra meta' della regola, e non e' una svista: e' la decisione D1."""

    def test_validate_maps_non_esclude_archivio(self):
        sorgente = (ROOT / "scripts" / "validate_maps.py").read_text(encoding="utf-8")
        self.assertNotIn(
            "_ARCHIVIO", sorgente,
            "validate_maps deve continuare a guardare dentro _ARCHIVIO: la D1 vi "
            "lascio' apposta gli SVG perche' nessun master sfugga al controllo. "
            "Se qualcuno lo esclude, quella decisione salta in silenzio.",
        )


class TestSulRepoVero(unittest.TestCase):
    def test_il_catalogo_non_contiene_record_da_un_archivio(self):
        """La prova che morde: nessun record puo' venire da una copia."""
        cat = ROOT / "scripts" / "monster_catalog.yaml"
        if not cat.exists():
            self.skipTest("catalogo non generato")
        colpevoli = [r.strip() for r in cat.read_text(encoding="utf-8").splitlines()
                     if "source_file:" in r and ("_ARCHIVIO" in r or "/Old/" in r)]
        self.assertEqual(colpevoli, [], f"record generati da copie archiviate: {colpevoli}")

    def test_il_catalogo_e_riproducibile_e_stabile(self):
        """Rigenerarlo non deve cambiare niente: se cambia, qualcosa lo inquina."""
        cat = ROOT / "scripts" / "monster_catalog.yaml"
        if not cat.exists():
            self.skipTest("catalogo non generato")
        prima = cat.read_text(encoding="utf-8")
        subprocess.run([sys.executable, "scripts/build_monster_catalog.py"],
                       cwd=ROOT, capture_output=True, check=False)
        self.assertEqual(cat.read_text(encoding="utf-8"), prima,
                         "il catalogo rigenerato differisce da quello committato")


if __name__ == "__main__":
    unittest.main()
