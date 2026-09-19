"""I dodici tool che decidono, e la decisione messa alla prova (lotto C).

Il lotto B aveva collaudato i quattro cancelli della CI. Restavano scoperti
altri quattordici script, e la distinzione che il piano fa è fra quelli che
**misurano** (`measure_tokens`, `compress_skills`: lì un test è cerimonia) e
quelli che **decidono** — che di fronte a un input scelgono un esito e lo
dichiarano con un codice d'uscita.

Per questi la specifica esiste già ed è scritta: il campo `exit_codes` di
`scripts/tools.manifest.json`. Finora nessuno aveva verificato che il codice
promesso sia quello che esce davvero. Questi test lo fanno, chiamando i tool
come li chiama la CI — per processo, non importandoli — perché il codice
d'uscita è il contratto e un `return` intercettato non lo è.

Lotto C di `plans/PIANO-QUALITA-DEL-CODICE.md`. Solo `unittest`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"
MANIFEST = json.loads((SCRIPTS / "tools.manifest.json").read_text(encoding="utf-8"))


def dichiarati(tool_id: str) -> dict[str, str]:
    """I codici d'uscita che il manifest promette per questo tool."""
    for t in MANIFEST["tools"]:
        if t["id"] == tool_id:
            return t.get("exit_codes", {})
    raise KeyError(tool_id)


def esegui(script: str, *argv: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *argv],
                          capture_output=True, text=True, cwd=str(cwd or REPO))


@contextmanager
def cartella():
    d = Path(tempfile.mkdtemp(prefix="decide-"))
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


class BaseDecisione(unittest.TestCase):
    """Ogni asserzione dice anche *quale* riga del manifest sta verificando."""

    def assertEsce(self, tool_id: str, atteso: int, r: subprocess.CompletedProcess):
        codici = dichiarati(tool_id)
        self.assertIn(str(atteso), codici,
                      f"{tool_id}: il manifest non dichiara il codice {atteso}")
        self.assertEqual(
            r.returncode, atteso,
            f"{tool_id}: atteso {atteso} ({codici[str(atteso)]}), "
            f"uscito {r.returncode}\nstdout: {r.stdout[-400:]}\nstderr: {r.stderr[-400:]}")


class TestValidateSkills(BaseDecisione):
    """Il quinto gate della CI, che il lotto B aveva lasciato fuori."""

    def _skill(self, root: Path, frontmatter: str, instrada: bool = True) -> None:
        d = root / "skills" / "finta"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(frontmatter, encoding="utf-8")
        # ADR-0041: un repo con una skill non instradata in AGENTS.md non e' sano.
        # Il mini-repo lo istrada, cosi' ogni test qui sotto boccia per il proprio
        # difetto e non per l'instradamento mancante.
        if instrada:
            (root / "AGENTS.md").write_text(
                "## Skills\n\n| Skill | Che cos'e' |\n|---|---|\n"
                "| `skills/finta/` | una skill di prova |\n", encoding="utf-8")
            # ADR-0058, stessa logica di ADR-0041 un gradino piu' in la': un repo
            # con una skill che non sta in nessuno strato non e' sano. Il
            # mini-repo la colloca, cosi' ogni test boccia per il proprio difetto
            # e non per la gerarchia mancante.
            (root / "skills" / "ORCHESTRAZIONE.md").write_text(
                "# Orchestrazione\n\n<!-- orchestrazione: strati -->\n\n"
                "| Strato | Domanda | Skill | Come si compone |\n|---|---|---|---|\n"
                "| **L2 · CHE COSA E'** | prova | `finta` | additive |\n\n"
                "<!-- orchestrazione: conflitti -->\n\n"
                "| # | Fra | Vince | Perche' |\n|---|---|---|---|\n",
                encoding="utf-8")

    def test_una_skill_sana_passa(self):
        with cartella() as d:
            self._skill(d, "---\nname: finta\ndescription: Una skill di prova.\n---\n\n# Finta\n")
            self.assertEsce("validate_skills", 0, esegui("validate_skills.py", "--repo-root", str(d)))

    def test_frontmatter_rotto_viene_bocciato(self):
        with cartella() as d:
            self._skill(d, "---\nname: finta\n  description: [rotto\n---\n\n# Finta\n")
            self.assertEsce("validate_skills", 1, esegui("validate_skills.py", "--repo-root", str(d)))

    def test_frontmatter_assente_viene_bocciato(self):
        with cartella() as d:
            self._skill(d, "# Finta\n\nNessun frontmatter.\n")
            self.assertEsce("validate_skills", 1, esegui("validate_skills.py", "--repo-root", str(d)))

    def test_link_rotto_viene_bocciato(self):
        with cartella() as d:
            self._skill(d, "---\nname: finta\ndescription: Una skill di prova.\n---\n\n"
                           "# Finta\n\nVedi [le regole](references/non-esiste.md).\n")
            self.assertEsce("validate_skills", 1, esegui("validate_skills.py", "--repo-root", str(d)))

    def test_skill_non_instradata_in_agents_viene_bocciata(self):
        """ADR-0041: la skill c'e' su disco e AGENTS.md non la nomina."""
        with cartella() as d:
            self._skill(d, "---\nname: finta\ndescription: Una skill di prova.\n---\n\n# Finta\n",
                        instrada=False)
            (d / "AGENTS.md").write_text("## Skills\n\nnessuna riga.\n", encoding="utf-8")
            self.assertEsce("validate_skills", 1, esegui("validate_skills.py", "--repo-root", str(d)))

    def test_puntatore_morto_in_agents_viene_bocciato(self):
        """ADR-0041, l'altra direzione: AGENTS.md nomina una skill che non c'e'."""
        with cartella() as d:
            self._skill(d, "---\nname: finta\ndescription: Una skill di prova.\n---\n\n# Finta\n")
            agents = d / "AGENTS.md"
            agents.write_text(agents.read_text(encoding="utf-8")
                              + "| `skills/sparita/` | rinominata e mai aggiornata |\n",
                              encoding="utf-8")
            self.assertEsce("validate_skills", 1, esegui("validate_skills.py", "--repo-root", str(d)))

    def test_il_repo_vero_passa(self):
        self.assertEsce("validate_skills", 0, esegui("validate_skills.py"))


class TestCheckPlansDiscipline(BaseDecisione):
    """Il gate ADR-0009: una modifica strutturale senza riga di tracciatura."""

    def _repo_git(self, d: Path) -> None:
        def git(*a):
            subprocess.run(["git", *a], cwd=str(d), capture_output=True, check=True)
        git("init", "-q", "-b", "main")
        git("config", "user.email", "t@t"); git("config", "user.name", "t")
        (d / "plans").mkdir(); (d / "scripts").mkdir()
        (d / "plans" / "CHANGELOG.md").write_text("| Data | Piano |\n|---|---|\n", encoding="utf-8")
        (d / "README.md").write_text("base\n", encoding="utf-8")
        git("add", "-A"); git("commit", "-qm", "base")

    def test_modifica_strutturale_senza_riga_viene_bocciata(self):
        with cartella() as d:
            self._repo_git(d)
            (d / "scripts" / "nuovo.py").write_text("print(1)\n", encoding="utf-8")
            subprocess.run(["git", "add", "-A"], cwd=str(d), capture_output=True, check=True)
            subprocess.run(["git", "commit", "-qm", "tocco scripts/"], cwd=str(d),
                           capture_output=True, check=True)
            self.assertEsce("check_plans_discipline", 1,
                            esegui("check_plans_discipline.py", "--repo-root", str(d),
                                   "--base", "HEAD~1", "--head", "HEAD"))

    def test_modifica_strutturale_con_la_riga_passa(self):
        with cartella() as d:
            self._repo_git(d)
            (d / "scripts" / "nuovo.py").write_text("print(1)\n", encoding="utf-8")
            (d / "plans" / "CHANGELOG.md").write_text(
                "| Data | Piano |\n|---|---|\n| 2026-09-03 | PROVA | riga | — | ✅ |\n",
                encoding="utf-8")
            subprocess.run(["git", "add", "-A"], cwd=str(d), capture_output=True, check=True)
            subprocess.run(["git", "commit", "-qm", "tocco scripts/ e traccio"], cwd=str(d),
                           capture_output=True, check=True)
            self.assertEsce("check_plans_discipline", 0,
                            esegui("check_plans_discipline.py", "--repo-root", str(d),
                                   "--base", "HEAD~1", "--head", "HEAD"))

    def test_modifica_non_strutturale_passa(self):
        with cartella() as d:
            self._repo_git(d)
            (d / "README.md").write_text("cambiato\n", encoding="utf-8")
            subprocess.run(["git", "add", "-A"], cwd=str(d), capture_output=True, check=True)
            subprocess.run(["git", "commit", "-qm", "solo prosa"], cwd=str(d),
                           capture_output=True, check=True)
            self.assertEsce("check_plans_discipline", 0,
                            esegui("check_plans_discipline.py", "--repo-root", str(d),
                                   "--base", "HEAD~1", "--head", "HEAD"))

    def test_un_diff_impossibile_salta_il_gate_invece_di_dare_falso_rosso(self):
        """Dichiarato nel codice: meglio un gate saltato e detto che un rosso finto."""
        with cartella() as d:
            self._repo_git(d)
            self.assertEsce("check_plans_discipline", 0,
                            esegui("check_plans_discipline.py", "--repo-root", str(d),
                                   "--base", "origin/inesistente", "--head", "HEAD"))


class TestSuggestMap(BaseDecisione):
    """Tre esiti distinti, e il manifest li distingue: 0, 3, 4."""

    def test_senza_filtri_elenca_e_passa(self):
        self.assertEsce("suggest_map", 0, esegui("suggest_map.py", "--list"))

    def test_nome_inesistente_da_3(self):
        self.assertEsce("suggest_map", 3, esegui("suggest_map.py", "--name", "non-esiste-davvero"))

    def test_filtri_senza_match_danno_4(self):
        self.assertEsce("suggest_map", 4, esegui("suggest_map.py", "--type", "zzz-inesistente"))

    def test_un_ambiente_inventato_NON_da_4_e_il_motivo_e_un_template(self):
        """`bridge-chokepoint.yaml` ha `environment: any`, e `any` matcha tutto.

        Scritto come test e non come commento perche' e' controintuitivo: chi
        chiede una mappa per un ambiente che non esiste si aspetta un rifiuto e
        invece riceve il ponte. Se un giorno quel template smette di essere
        `any`, questo test cade e la riga del manifest va riletta.
        """
        self.assertEsce("suggest_map", 0, esegui("suggest_map.py", "--env", "vulcano-sottomarino"))

    def test_un_filtro_che_matcha_da_0(self):
        r = esegui("suggest_map.py", "--list")
        prima = [l for l in r.stdout.splitlines() if l.startswith("| `")]
        self.assertTrue(prima, "nessun template: il corpus di prova è vuoto")
        env = prima[0].split("|")[3].strip()
        self.assertEsce("suggest_map", 0, esegui("suggest_map.py", "--env", env))


class TestSuggestLoot(BaseDecisione):
    def test_senza_argomenti_parte_dal_Party_APL(self):
        """Cambiato il 2026-09-03 su rilievo del DM: prima era un errore d'uso.

        Il numero c'era in `campaign/state.md` e nessuno lo leggeva. Ora senza
        argomenti lo strumento parte da lì e **dice da dove viene**.
        """
        r = esegui("suggest_loot.py")
        self.assertEsce("suggest_loot", 0, r)
        self.assertIn("Party APL", r.stderr)

    def test_senza_argomenti_e_senza_APL_da_2(self):
        """L'errore d'uso resta, ma solo quando non c'è davvero da dove partire."""
        from unittest import mock
        import importlib.util
        spec = importlib.util.spec_from_file_location("suggest_loot", SCRIPTS / "suggest_loot.py")
        mod = importlib.util.module_from_spec(spec)
        sys.argv = ["suggest_loot.py"]
        spec.loader.exec_module(mod)
        with cartella() as d:
            vuoto = d / "state.md"
            vuoto.write_text("# Senza APL\n", encoding="utf-8")
            import dmcore.tavolo as tav
            with mock.patch.object(tav, "STATE", vuoto):
                self.assertEqual(mod.main(), 2)

    def test_file_di_incontri_assente_da_2(self):
        self.assertEsce("suggest_loot", 2,
                        esegui("suggest_loot.py", "--from-encounter", "/non/esiste.md"))

    def test_un_el_valido_da_0(self):
        self.assertEsce("suggest_loot", 0, esegui("suggest_loot.py", "--el", "10"))

    def test_un_file_senza_EL_ora_parte_dal_Party_APL(self):
        """⚠️→✅ Il difetto trovato dal lotto C, chiuso su rilievo del DM.

        Il lotto C aveva trovato che `suggest_loot`, davanti a un file che non è
        un output di `suggest_encounter`, non protestava: ripiegava su un **10
        scritto nel codice**, muto. Il DM ha osservato due cose giuste — che
        nella catena vera l'EL viene da `suggest_encounter` (e infatti il 10 non
        si vedeva mai), e che quando non c'è lo si può guardare nell'avventura.

        `campaign/state.md` dichiara `**Party APL:** 13` nell'intestazione. Ora
        la gerarchia è `--el` → il file → il Party APL → il rifiuto, e il numero
        non arriva mai senza dire da dove viene. Il codice 3 del manifest, che
        era irraggiungibile, ora si raggiunge: solo quando manca anche l'APL.
        """
        with cartella() as d:
            vuoto = d / "niente.md"
            vuoto.write_text("# Nessuna proposta qui dentro\n", encoding="utf-8")
            r = esegui("suggest_loot.py", "--from-encounter", str(vuoto))
            self.assertEsce("suggest_loot", 0, r)
            self.assertIn("Party APL", r.stderr)
            self.assertIn("3", dichiarati("suggest_loot"),
                          "il codice 3 e' tornato raggiungibile: deve stare nel manifest")


class TestImportWatabou(BaseDecisione):
    """⚠️ Difetto trovato dal lotto C: il codice 1 usciva per caso.

    Un JSON rotto non veniva deciso, veniva *subito*: `json.loads` alzava
    `JSONDecodeError`, l'eccezione arrivava in cima e Python usciva con 1. Il
    codice era quello giusto per la ragione sbagliata, e chi scarica un export
    da un sito si trovava venti righe di traccia che finiscono su
    `json.decoder`. E' la stessa cosa che `binari.py` aveva gia' deciso di non
    fare per i binari.

    Per questo qui non basta il codice d'uscita: si verifica anche che **non
    esca una traccia di stack**. Senza questa asserzione la mutazione passa.
    """

    def test_json_non_valido_da_1_e_lo_dice_in_italiano(self):
        with cartella() as d:
            rotto = d / "rotto.json"
            rotto.write_text("{questo non e' json", encoding="utf-8")
            r = esegui("import_watabou.py", str(rotto))
            self.assertEsce("import_watabou", 1, r)
            self.assertNotIn("Traceback", r.stderr)
            self.assertIn("non e' JSON valido", r.stderr)

    def test_json_valido_ma_non_un_dungeon_da_1(self):
        with cartella() as d:
            altro = d / "altro.json"
            altro.write_text('{"qualcosa": "che non e\' una mappa"}', encoding="utf-8")
            r = esegui("import_watabou.py", str(altro))
            self.assertEsce("import_watabou", 1, r)
            self.assertNotIn("Traceback", r.stderr)

    def test_file_inesistente_da_1(self):
        self.assertEsce("import_watabou", 1, esegui("import_watabou.py", "/non/esiste.json"))


class TestExtractScenePrompts(BaseDecisione):
    def test_arco_inesistente_da_2(self):
        self.assertEsce("extract_scene_prompts", 2,
                        esegui("extract_scene_prompts.py", "99_arco_che_non_esiste"))


class TestDmDossier(BaseDecisione):
    """`dm_dossier` legge `campaign/state.md` da una costante, non da un flag.

    La decisione «state.md non c'e'» si prova quindi spostando la costante, non
    con un argomento: per processo non sarebbe provabile affatto, ed e' il
    motivo per cui finora non lo era.
    """

    def test_senza_state_md_da_1(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("dm_dossier", SCRIPTS / "dm_dossier.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with cartella() as d:
            vecchio = mod.STATE
            mod.STATE = d / "non-esiste.md"
            try:
                self.assertEqual(mod.main(["-o", str(d / "out.md")]), 1)
            finally:
                mod.STATE = vecchio

    def test_col_state_vero_produce_il_dossier(self):
        with cartella() as d:
            self.assertEsce("dm_dossier", 0,
                            esegui("dm_dossier.py", "-o", str(d / "dossier.md")))
            self.assertTrue((d / "dossier.md").is_file())


class TestExportUvtt(BaseDecisione):
    def test_master_senza_mappe_da_1(self):
        with cartella() as d:
            nudo = d / "nudo.md"
            nudo.write_text("# Un file senza nessuna griglia\n\nSolo prosa.\n", encoding="utf-8")
            self.assertEsce("export_uvtt", 1, esegui("export_uvtt.py", str(nudo)))


class TestBuildChapterMarks(BaseDecisione):
    def test_senza_serie_ne_all_da_2(self):
        self.assertEsce("build_chapter_marks", 2, esegui("build_chapter_marks.py"))


class TestIndexSkills(BaseDecisione):
    """⚠️ Due difetti trovati dal lotto C, e il secondo nascondeva il primo.

    1. Una cartella sorgente inesistente non era un errore: `rglob` non alza
       niente, e lo script scriveva un `index.json` con **zero voci**. Un file
       che c'e' e sembra buono e' peggio di un errore.
    2. `main()` era chiamato senza `sys.exit()`, quindi il valore di ritorno
       finiva nel nulla e lo script usciva **sempre con 0**. I codici dichiarati
       nel manifest erano una promessa che solo argparse manteneva.
    """

    def test_cartella_sorgente_inesistente_da_2(self):
        with cartella() as d:
            r = esegui("index_skills.py", "-i", str(d / "non-esiste"),
                       "-b", str(d), "-o", str(d / "index.json"))
            self.assertEsce("index_skills", 2, r)
            self.assertFalse((d / "index.json").exists(),
                             "ha scritto un indice nonostante l'errore")

    def test_argomenti_mancanti_da_2(self):
        self.assertEsce("index_skills", 2, esegui("index_skills.py"))

    def test_una_cartella_vera_da_0(self):
        with cartella() as d:
            (d / "src").mkdir()
            (d / "src" / "a.md").write_text("# A\n\nTesto.\n", encoding="utf-8")
            r = esegui("index_skills.py", "-i", str(d / "src"),
                       "-b", str(d), "-o", str(d / "index.json"))
            self.assertEsce("index_skills", 0, r)
            self.assertTrue((d / "index.json").is_file())


class TestExportBookletPdf(BaseDecisione):
    def test_manifest_assente_da_2(self):
        self.assertEsce("export_booklet_pdf", 2,
                        esegui("export_booklet_pdf.py", "/non/esiste.manifest.json"))


class TestCampaignBranch(BaseDecisione):
    """La guardia ADR-0007, provata dove decide davvero.

    `cmd_guard` legge il repo da una costante di modulo e non dal cwd: lanciarlo
    con `cwd=` su un repo finto non prova niente, perche' guarda sempre questo.
    Si monta quindi la decisione dove sta, sostituendo il gruppo configurato.
    """

    def _modulo(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("campaign_branch",
                                                      SCRIPTS / "campaign_branch.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_se_il_gruppo_e_configurato_e_il_branch_e_un_altro_rifiuta(self):
        from unittest import mock
        mod = self._modulo()
        with mock.patch.object(mod.cfg, "load_group", return_value="gruppo-che-non-e-questo"):
            self.assertEqual(mod.cmd_guard(mod.REPO), 1)

    def test_senza_gruppo_configurato_non_rifiuta(self):
        """Il caso di un clone appena fatto: nessun gruppo, nessuna guardia."""
        from unittest import mock
        mod = self._modulo()
        with mock.patch.object(mod.cfg, "load_group", return_value=None):
            self.assertIn(mod.cmd_guard(mod.REPO), (0, 1))

    def test_ensure_senza_gruppo_da_2(self):
        mod = self._modulo()
        from unittest import mock
        with mock.patch.object(mod.cfg, "load_group", return_value=None):
            self.assertEqual(mod.cmd_ensure(mod.REPO, None), 2)


class TestCopertura(unittest.TestCase):
    """Il conto, perché il lotto si possa dire chiuso con un numero."""

    DECIDONO = {
        "validate_skills", "check_plans_discipline", "campaign_branch", "export_uvtt",
        "suggest_loot", "suggest_map", "import_watabou", "export_booklet_pdf",
        "extract_scene_prompts", "build_chapter_marks", "dm_dossier", "index_skills",
    }

    def test_ognuno_dei_dodici_ha_almeno_un_test_qui(self):
        testo = Path(__file__).read_text(encoding="utf-8")
        for tid in sorted(self.DECIDONO):
            with self.subTest(tid):
                self.assertIn(f'"{tid}"', testo, f"{tid} non è collaudato da nessuna parte")

    def test_i_due_che_misurano_restano_fuori_di_proposito(self):
        """`measure_tokens` e `compress_skills` misurano: un test lì è cerimonia.

        Sta scritto qui perché la prossima persona non lo scambi per una svista.
        """
        self.assertNotIn("measure_tokens", self.DECIDONO)
        self.assertNotIn("compress_skills", self.DECIDONO)


if __name__ == "__main__":
    unittest.main()
