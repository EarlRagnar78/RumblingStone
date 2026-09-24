"""Un gruppo nuovo non eredita la partita del primo — lotto 4f, ADR-0050 §7.

ADR-0050 §7 nominava questo test come il presidio della regola prodotto/partita
fin da quando e' stata recuperata (lotto 4d-1), e il test non esisteva. Nel
frattempo `new-campaign-group.sh` azzerava due file su sette: il gruppo nuovo
ereditava 750 righe di `state.yaml` e 1.195 di storico, e la sua CI era rossa al
primo push perche' il template di `state.md` non aveva i marcatori.

🔴 **Il reset gira su una copia dei FILE VERI** di `campaign/`, col resto del
repo collegato: un fixture costruito per passare proverebbe il fixture.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

import azzera_partita  # noqa: E402
import render_state  # noqa: E402
import state_apply  # noqa: E402
import validate_state  # noqa: E402
from dmcore import delta_sessione  # noqa: E402
from dmcore.partita import PARTITA, PENDENTI  # noqa: E402

STATO_VERO = yaml.safe_load((ROOT / "campaign" / "state.yaml").read_text(encoding="utf-8"))
#: I nomi del primo tavolo: i PG e i villain che il template non dichiara.
PG_DEL_PRIMO = [p["pg"] for p in STATO_VERO["party"]]


def _copia(dest: Path) -> None:
    """`campaign/` e `scripts/` copiati, tutto il resto del repo collegato."""
    for nome in ("campaign", "scripts"):
        shutil.copytree(ROOT / nome, dest / nome,
                        ignore=shutil.ignore_patterns("__pycache__"))
    for voce in ROOT.iterdir():
        if not (dest / voce.name).exists() and voce.name != ".git":
            (dest / voce.name).symlink_to(voce)


def _corrisponde(percorso: str, modello: str) -> bool:
    """Un glob dove `*` NON attraversa le cartelle, come in `Path.glob`.

    🐛 `fnmatch` lo lascia attraversare: con `fnmatch`, `campaign/recaps/*.md`
    copriva anche `campaign/recaps/homebrew/*.hb.md`, e togliere quella voce
    dall'elenco lasciava questo test verde. Il reset invece usa `Path.glob`,
    che non attraversa: il test deve misurare con lo stesso metro.
    """
    rx = "".join("[^/]*" if c == "*" else re.escape(c) for c in modello)
    return re.fullmatch(rx, percorso) is not None


class TestLElencoCopreOgniFileDiPartita(unittest.TestCase):
    """Uno script che scrive sotto `campaign/` senza dichiararlo fa rossa la CI."""

    def test_ogni_uscita_degli_script_sotto_campaign_e_dichiarata(self):
        manifest = json.loads((ROOT / "scripts" / "tools.manifest.json").read_text(encoding="utf-8"))
        modelli = [v.percorso for v in PARTITA] + list(PENDENTI)
        scoperti = []
        for tool in manifest["tools"]:
            for uscita in tool.get("outputs", []):
                p = uscita["path"]
                if not p.startswith("campaign/"):
                    continue
                # `YYYY-MM-DD_session-N.md` e `brief-*-DM.md` sono modelli
                # del manifest: si confrontano come glob.
                g = re.sub(r"YYYY-MM-DD|N(?=\.md)", "*", p)
                if not any(_corrisponde(g, m) or _corrisponde(p, m) for m in modelli):
                    scoperti.append(f"{tool['id']} → {p}")
        self.assertEqual(scoperti, [], "file di partita non dichiarati in dmcore/partita.py")

    def test_lo_script_bash_non_ha_un_suo_elenco(self):
        """Una lista scritta due volte diverge: lo script delega e basta."""
        sh = (ROOT / "scripts" / "new-campaign-group.sh").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/azzera_partita.py", sh)
        self.assertNotRegex(sh, r"\ncp campaign/templates/")
        self.assertNotRegex(sh, r"\nrm -f campaign/")

    def test_i_template_non_portano_il_primo_tavolo(self):
        for v in PARTITA:
            if not v.sorgente:
                continue
            testo = (ROOT / v.sorgente).read_text(encoding="utf-8")
            for nome in PG_DEL_PRIMO:
                self.assertNotIn(nome, testo, f"{v.sorgente} nomina {nome}")


class TestIlResetSuiFileVeri(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.radice = Path(self._tmp.name)
        _copia(self.radice)
        (self.radice / "campaign" / "group.yaml").write_text("group: vecchio\n", encoding="utf-8")
        self.resoconto = azzera_partita.azzera(self.radice)

    def tearDown(self):
        self._tmp.cleanup()

    def _testo(self, rel: str) -> str:
        return (self.radice / rel).read_text(encoding="utf-8")

    def test_la_ci_del_gruppo_nuovo_e_verde(self):
        dati = yaml.safe_load(self._testo("campaign/state.yaml"))
        self.assertEqual(validate_state.errori(dati, self.radice), [])
        md = self._testo("campaign/state.md")
        nuovo, mancanti = render_state.apply_regions(md, dati)
        self.assertEqual(mancanti, [])
        self.assertEqual(nuovo, md)

    def test_non_eredita_niente_della_partita(self):
        for rel in ("campaign/state.yaml", "campaign/state.md", "campaign/state-changelog.md",
                    "campaign/lore/campaign-chronicle.md"):
            testo = self._testo(rel)
            for nome in PG_DEL_PRIMO:
                with self.subTest(file=rel, pg=nome):
                    self.assertNotIn(nome, testo)
        dati = yaml.safe_load(self._testo("campaign/state.yaml"))
        self.assertEqual(dati["echi"], [])
        self.assertEqual(dati["march_clock"]["giorno_corrente"], 1)
        self.assertLess(len(self._testo("campaign/state-changelog.md").splitlines()), 30)
        for v in PARTITA:
            if v.azione in ("svuota", "rimuovi"):
                with self.subTest(percorso=v.percorso):
                    self.assertEqual(list(self.radice.glob(v.percorso)), [])
        self.assertTrue((self.radice / "campaign" / "sessions" / ".gitkeep").exists())
        # Contati direttamente, non attraverso l'elenco: se una voce sparisse
        # dall'elenco, il ciclo qui sopra smetterebbe di guardarla.
        self.assertEqual(list((self.radice / "campaign" / "recaps").rglob("*.md")), [])
        self.assertEqual(list((self.radice / "campaign" / "sessions").rglob("*.md")), [])

    def test_il_prodotto_resta(self):
        dati = yaml.safe_load(self._testo("campaign/state.yaml"))
        self.assertEqual(dati["png"], STATO_VERO["png"], "l'anagrafica e' prodotto")
        for rel in ("campaign/lore/house-rules.md", "campaign/lore/campaign-premise.md"):
            self.assertEqual(self._testo(rel), (ROOT / rel).read_text(encoding="utf-8"), rel)

    def test_la_via_di_scrittura_funziona_sul_gruppo_nuovo(self):
        """Il primo `session end` del gruppo nuovo scrive, e la vista segue."""
        import subprocess
        repo = self.radice
        log = repo / "campaign" / "sessions" / "2026-10-01_session-1.md"
        log.write_text(delta_sessione.emetti({
            "march_clock": {"da": 1, "a": 2},
            "clock": [{"png_id": "azarr-kul", "da": 0, "a": 1}]})
            + "# Session 1 — Prima (2026-10-01)\n", encoding="utf-8")
        for cmd in (["init", "-q", "-b", "campaign-group-nuovo"], ["config", "user.email", "t@t"],
                    ["config", "user.name", "t"], ["add", "-A", "campaign"],
                    ["commit", "-qm", "reset"]):
            subprocess.run(["git", "-C", str(repo), *cmd], check=True)
        self.assertEqual(state_apply.main(["--session", log.name, "--yes", "--no-guard",
                                           "--repo-root", str(repo)]), 0)
        dati = yaml.safe_load(self._testo("campaign/state.yaml"))
        self.assertEqual(dati["march_clock"]["giorno_corrente"], 2)
        self.assertEqual(dati["villain"][0]["clock"], "1/18")
        self.assertIn("March Clock Day 1 → Day 2", self._testo("campaign/state-changelog.md"))

    def test_rifarlo_da_lo_stesso_risultato(self):
        prima = {v.percorso: self._testo(v.percorso) for v in PARTITA
                 if v.azione in ("stato", "template")}
        azzera_partita.azzera(self.radice)
        for rel, testo in prima.items():
            self.assertEqual(self._testo(rel), testo, rel)


LORE = ROOT / "campaign" / "lore"
PREMESSA = LORE / "campaign-premise.md"
CRONACA = LORE / "campaign-chronicle.md"
#: Eventi di questo tavolo, presi dal test della #99 (`c825d6d`) e dal file di
#: oggi: la cronaca li racconta, la premessa non deve dirli.
EVENTI = ("Hella Oakenshield DIES", "Thorik passes trial", "Artemis REJECTS",
          "Hella returns as Treant", "ESCAPED", "Current Level")


class TestLaPremessaELaCronaca(unittest.TestCase):
    """Lotto 4f-2, decisione D20: `campaign-history.md` diviso in due."""

    def test_i_due_file_esistono_e_il_vecchio_non_c_e_piu(self):
        self.assertTrue(PREMESSA.exists())
        self.assertTrue(CRONACA.exists())
        self.assertFalse((LORE / "campaign-history.md").exists(),
                         "andava diviso, non duplicato")

    def test_la_premessa_non_racconta_eventi_del_tavolo(self):
        """L'invariante della #99: non «la premessa non nomina mai un PG»,
        troppo stretto dove gli artefatti portano il nome del portatore, ma
        «la premessa non afferma cosa e' successo»."""
        testo = PREMESSA.read_text(encoding="utf-8")
        corpo = testo.split("\n---\n", 1)[1]  # l'intestazione cita «ESCAPED» per spiegarlo
        self.assertEqual([e for e in EVENTI if e in corpo], [])
        self.assertNotIn("| PC | Race |", testo, "la tabella del party e' cronaca")

    def test_gli_eventi_sono_nella_cronaca(self):
        """Senza questo, il test di sopra passerebbe anche con gli eventi persi."""
        testo = CRONACA.read_text(encoding="utf-8")
        self.assertEqual([e for e in EVENTI if e not in testo], [])
        for nome in PG_DEL_PRIMO:
            self.assertIn(nome, testo)

    def test_nessuna_riga_persa_nello_split(self):
        """Contro git, non contro una copia fatta al momento: l'ultimo commit in
        cui `campaign-history.md` esisteva, trovato per contenuto."""
        import subprocess
        log = subprocess.run(["git", "log", "--format=%H", "--", "campaign/lore/campaign-history.md"],
                             cwd=ROOT, capture_output=True, text=True).stdout.split()
        prima = None
        for sha in log:
            r = subprocess.run(["git", "show", f"{sha}:campaign/lore/campaign-history.md"],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 0:
                prima = r.stdout
                break
        if prima is None:
            self.skipTest("campaign-history.md non e' nella storia (clone shallow?)")
        banale = lambda r: r.strip() in ("", "---")  # noqa: E731
        from collections import Counter
        attese = Counter(r for r in prima.splitlines() if not banale(r))
        spostata = "        │   ├── Il Collezionista (Rakshasa, ESCAPED)"
        attese[spostata] -= 1
        attese[spostata.replace(", ESCAPED", "")] += 1
        oggi = Counter(r for f in (PREMESSA, CRONACA)
                       for r in f.read_text(encoding="utf-8").splitlines() if not banale(r))
        self.assertEqual(sum((attese - oggi).values()), 0, list((attese - oggi))[:5])


class TestIlResetSiFermaPrimaDiScrivere(unittest.TestCase):
    def test_uno_stato_invalido_non_scrive_niente(self):
        with tempfile.TemporaryDirectory() as tmp:
            radice = Path(tmp)
            _copia(radice)
            tpl = radice / "campaign" / "templates" / "state-blank.yaml"
            tpl.write_text(tpl.read_text(encoding="utf-8").replace(
                "png_id: azarr-kul", "png_id: nessuno-cosi", 1), encoding="utf-8")
            prima = (radice / "campaign" / "state.yaml").read_text(encoding="utf-8")
            with self.assertRaises(azzera_partita.ResetError):
                azzera_partita.azzera(radice)
            self.assertEqual((radice / "campaign" / "state.yaml").read_text(encoding="utf-8"), prima)
            self.assertTrue(any((radice / "campaign" / "sessions").glob("*.md")),
                            "le sessioni non si toccano se lo stato non e' valido")

    def test_senza_anagrafica_non_parte(self):
        with self.assertRaises(azzera_partita.ResetError):
            azzera_partita.stato_nuovo("schema_version: 1\n", "schema_version: 1\n")


if __name__ == "__main__":
    unittest.main()
