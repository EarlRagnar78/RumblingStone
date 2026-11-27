"""L8 (ADR-0111): la prova del nove dei plugin.

Il difetto che questo test esiste per impedire: un sistema di gioco nuovo
che per entrare nel repo chiede di toccare il codice. Si prende un repo
temporaneo con `sistemi/`, `sistemi.toml`, il manifest degli strumenti e i
file di dati che i plugin elencano; ci si aggiunge il plugin finto
`scripts/tests/dati/prova-d20/` (solo dati: un `sistema.toml` e due `.toml`)
e una riga in `sistemi.toml`. Poi si chiede agli strumenti veri, senza
cambiarne una riga, di usarlo: il cancello deve restare verde e le due
regole che il plugin cambia (soglie dei PE e raddoppio dell'EL) devono
arrivare negli strumenti.

È M4 del censimento: i file di codice da toccare per un sistema nuovo. Qui
sono zero per costruzione, perché il test non ne scrive nessuno.

Solo `unittest`.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import sistemi as S  # noqa: E402
import sistemi as CLI  # noqa: E402
import suggest_encounter as SE  # noqa: E402
import update_xp as UX  # noqa: E402

FINTO = REPO / "scripts" / "tests" / "dati" / "prova-d20"


def _file_dei_plugin() -> set[str]:
    """I file che i plugin veri elencano, in `dati` o in `codice` («file:NOME»)."""
    fuori = set()
    for f in (REPO / "sistemi").glob("*/sistema.toml"):
        for c in tomllib.loads(f.read_text(encoding="utf-8")).get("capacita", {}).values():
            fuori.update(c.get("dati", []))
            fuori.update(v.split(":", 1)[0] for v in c.get("codice", []))
    return fuori


class ProvaDelNove(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        r = cls.root = Path(cls._tmp.name)
        shutil.copytree(REPO / "sistemi", r / "sistemi")
        for rel in _file_dei_plugin() | {"scripts/tools.manifest.json"}:
            (r / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, r / rel)
        for d in (REPO / "skills").iterdir():
            if (d / "SKILL.md").is_file():
                (r / "skills" / d.name).mkdir(parents=True)
                (r / "skills" / d.name / "SKILL.md").write_text("", encoding="utf-8")
        # il plugin finto: solo dati
        shutil.copytree(FINTO, r / "sistemi" / "prova-d20")
        cfg = (REPO / "sistemi.toml").read_text(encoding="utf-8")
        letto = tomllib.loads(cfg)
        for cartella in {**letto.get("moduli", {}), **letto.get("ambientazioni", {}).get("moduli", {})}:
            (r / cartella).mkdir(parents=True)
        (r / "moduli-di-prova").mkdir()
        cfg = cfg.replace('attivi = ["dnd35", "pf1e"]', 'attivi = ["dnd35", "pf1e", "prova-d20"]')
        cfg = cfg.replace("[moduli]\n", '[moduli]\n"moduli-di-prova" = "prova-d20"\n')
        (r / "sistemi.toml").write_text(cfg, encoding="utf-8")
        cls._root_vero = S.ROOT
        S.ROOT = r
        S._carica.cache_clear()

    @classmethod
    def tearDownClass(cls):
        S.ROOT = cls._root_vero
        S._carica.cache_clear()
        cls._tmp.cleanup()

    def test_la_configurazione_e_cambiata_davvero(self):
        self.assertIn("prova-d20", S.attivi())

    def test_il_cancello_resta_verde(self):
        self.assertEqual(S.problemi(self.root, CLI.strumenti(self.root)), [])

    def test_ogni_capacita_del_catalogo_e_coperta(self):
        cat = tomllib.loads((self.root / "sistemi" / "catalogo.toml").read_text(encoding="utf-8"))
        for nome in cat["capacita"]:
            self.assertNotEqual(S.capacita("prova-d20", nome).modo, "mancante", nome)

    def test_un_modulo_dichiarato_prende_il_sistema_nuovo(self):
        self.assertEqual(S.sistema_di("moduli-di-prova/capitolo.md"), "prova-d20")
        self.assertEqual(S.sistema_di("07_altro/capitolo.md"), "dnd35")

    def test_le_soglie_dei_pe_arrivano_in_update_xp(self):
        soglie, etichetta = UX.soglie_di("prova-d20")
        self.assertEqual(etichetta, "prova")
        self.assertEqual(soglie[3], 6000)
        self.assertNotEqual(soglie, UX.soglie_di("dnd35")[0])

    def test_il_raddoppio_arriva_in_suggest_encounter(self):
        crs = [10.0, 10.0]
        el_35 = SE.combinatore("dnd35")(crs)
        el_prova = SE.combinatore("prova-d20")(crs)
        self.assertAlmostEqual(el_35, 12.0, places=6)    # due GS 10 = EL 12 in 3.5
        self.assertAlmostEqual(el_prova, 13.0, places=6)  # raddoppio 3: 10 + 3

    def test_quello_che_eredita_e_lo_stesso_del_3_5(self):
        for nome in ("creature.costruzione", "creature.incantesimi", "lessico.abilita"):
            self.assertEqual(S.dati("prova-d20", nome), S.dati("dnd35", nome), nome)
        self.assertEqual(S.etichette("prova-d20"), S.etichette("dnd35"))
        self.assertEqual(S.termini_vietati("prova-d20"), S.termini_vietati("dnd35"))

    def test_nessuna_skill_in_piu_ne_in_meno(self):
        self.assertEqual(S.skill_escluse(self.root), [])

    def test_il_plugin_finto_e_solo_dati(self):
        estensioni = {p.suffix for p in FINTO.rglob("*") if p.is_file()}
        self.assertEqual(estensioni, {".toml"})


if __name__ == "__main__":
    unittest.main()
