"""milestone_pronte.py: quando una milestone della roadmap è pronta (o rilasciata).

Il registro è `plans/milestone.json`. Ogni prova costruisce un repo finto in una
cartella temporanea fuori dal repo vero, con il suo registro, e chiama lo script
per processo, come lo chiama il workflow: il codice d'uscita e le righe di
`--pronte` sono il contratto. L'ultima classe guarda il registro vero, ma solo
la sua integrità (`--solo-integrita`), senza eseguire i comandi dei criteri.

Solo `unittest`, perché la parità dei due corridori lo chiede
(test_i_test_girano_in_ci).
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "milestone_pronte.py"
RILASCIO = ("fatto-changelog", "fatto-versione", "fatto-tag")


def esegui(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, timeout=120)


class RepoFinto:
    """Un repo minimo: due script che escono 0 e 1, un documento, un CHANGELOG."""

    def __init__(self, radice: Path):
        self.radice = radice
        (radice / "scripts").mkdir()
        (radice / "docs").mkdir()
        (radice / "plans").mkdir()
        (radice / "scripts" / "vero.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        (radice / "scripts" / "falso.py").write_text("raise SystemExit(1)\n", encoding="utf-8")
        (radice / "docs" / "GUIDA.md").write_text("# Guida\n\nADR-0001 citata.\n", encoding="utf-8")
        (radice / "CHANGELOG.md").write_text("# Changelog\n\n## [1.0.0]\n", encoding="utf-8")
        self.registro = radice / "plans" / "milestone.json"

    def scrivi(self, milestone: list[dict]) -> None:
        self.registro.write_text(json.dumps({"milestone": milestone}, ensure_ascii=False),
                                 encoding="utf-8")

    def lancia(self, *args: str) -> subprocess.CompletedProcess:
        return esegui("--registro", str(self.registro), "--radice", str(self.radice), *args)


def criteri_di_lavoro(dm_confermato: bool = True, file_vero: bool = True) -> list[dict]:
    return [
        {"id": "guida", "tipo": "file", "testo": "la guida cita l'ADR",
         "file": "docs/GUIDA.md", "regex": ["^# Guida", "ADR-0001" if file_vero else "ADR-9999"],
         "deve": "comparire"},
        {"id": "niente-todo", "tipo": "file", "testo": "nessun TODO",
         "file": ["docs/GUIDA.md"], "regex": "TODO", "deve": "mancare"},
        {"id": "cancello", "tipo": "comando", "testo": "il cancello passa",
         "comando": "python3 scripts/vero.py"},
        {"id": "letto-dm", "tipo": "dm", "testo": "il DM l'ha letto",
         "confermato": {"data": "2026-11-27", "dove": "MEMORIA.md"} if dm_confermato else None},
    ]


def criteri_di_rilascio(rilasciata: bool) -> list[dict]:
    script = "scripts/vero.py" if rilasciata else "scripts/falso.py"
    return [
        {"id": "fatto-changelog", "tipo": "file", "testo": "sezione nel CHANGELOG", "comune": True,
         "file": "CHANGELOG.md", "regex": r"^## \[1\.0\.0\]" if rilasciata else r"^## \[1\.1\.0\]",
         "deve": "comparire"},
        {"id": "fatto-versione", "tipo": "comando", "testo": "versione scritta", "comune": True,
         "comando": f"python3 {script}"},
        {"id": "fatto-tag", "tipo": "comando", "testo": "tag", "comune": True,
         "comando": f"python3 {script}"},
    ]


def milestone(numero: int, versione: str, criteri: list[dict]) -> dict:
    return {"numero": numero, "versione": versione, "titolo": f"v{versione} · prova",
            "criteri": criteri}


class _ConRepo(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="milestone-")
        self.repo = RepoFinto(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()


class TestPronta(_ConRepo):
    def test_tutto_vero_tranne_il_rilascio_compare_in_pronte(self):
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro() + criteri_di_rilascio(False))])
        p = self.repo.lancia("--pronte")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.split(), ["1.1.0"])

    def test_json_dice_pronta_e_l_esito_di_ogni_criterio(self):
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro() + criteri_di_rilascio(False))])
        p = self.repo.lancia("--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        dati = json.loads(p.stdout)
        self.assertTrue(dati["integro"])
        m = dati["milestone"][0]
        self.assertEqual(m["stato"], "pronta")
        esiti = {c["id"]: c["vero"] for c in m["criteri"]}
        self.assertEqual(esiti, {"guida": True, "niente-todo": True, "cancello": True,
                                 "letto-dm": True, "fatto-changelog": False,
                                 "fatto-versione": False, "fatto-tag": False})
        self.assertEqual(m["falsi"], [])
        self.assertEqual(dati["pronte"], ["1.1.0"])

    def test_la_tabella_dice_pronta(self):
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro() + criteri_di_rilascio(False))])
        p = self.repo.lancia()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("pronta", p.stdout)
        self.assertIn("1.1.0", p.stdout)


class TestNonPronta(_ConRepo):
    def test_un_criterio_file_falso(self):
        self.repo.scrivi([milestone(1, "1.1.0",
                                    criteri_di_lavoro(file_vero=False) + criteri_di_rilascio(False))])
        p = self.repo.lancia("--pronte")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "")
        dati = json.loads(self.repo.lancia("--json").stdout)
        self.assertEqual(dati["milestone"][0]["stato"], "non pronta")
        self.assertEqual(dati["milestone"][0]["falsi"], ["guida"])

    def test_un_dm_non_confermato(self):
        self.repo.scrivi([milestone(1, "1.1.0",
                                    criteri_di_lavoro(dm_confermato=False) + criteri_di_rilascio(False))])
        self.assertEqual(self.repo.lancia("--pronte").stdout.strip(), "")
        p = self.repo.lancia()
        self.assertIn("non pronta", p.stdout)
        self.assertIn("letto-dm", p.stdout)

    def test_un_regex_che_deve_mancare_e_trovato(self):
        (self.repo.radice / "docs" / "GUIDA.md").write_text("# Guida\nADR-0001\nTODO\n",
                                                            encoding="utf-8")
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro() + criteri_di_rilascio(False))])
        dati = json.loads(self.repo.lancia("--json").stdout)
        self.assertEqual(dati["milestone"][0]["falsi"], ["niente-todo"])

    def test_un_comando_che_esce_1(self):
        criteri = criteri_di_lavoro()
        criteri[2]["comando"] = "python3 scripts/falso.py"
        self.repo.scrivi([milestone(1, "1.1.0", criteri + criteri_di_rilascio(False))])
        dati = json.loads(self.repo.lancia("--json").stdout)
        self.assertEqual(dati["milestone"][0]["falsi"], ["cancello"])

    def test_un_comando_oltre_il_timeout_e_falso(self):
        (self.repo.radice / "scripts" / "lento.py").write_text("import time\ntime.sleep(30)\n",
                                                               encoding="utf-8")
        criteri = criteri_di_lavoro()
        criteri[2]["comando"] = "python3 scripts/lento.py"
        self.repo.scrivi([milestone(1, "1.1.0", criteri + criteri_di_rilascio(False))])
        p = self.repo.lancia("--json", "--timeout", "1")
        self.assertEqual(p.returncode, 0, p.stderr)
        c = {c["id"]: c for c in json.loads(p.stdout)["milestone"][0]["criteri"]}["cancello"]
        self.assertFalse(c["vero"])
        self.assertIn("timeout", c["dettaglio"])

    def test_il_comando_non_passa_dalla_shell(self):
        """Con shell=True `; touch` creerebbe il file: con shlex è un argomento."""
        criteri = criteri_di_lavoro()
        criteri[2]["comando"] = "python3 scripts/vero.py ; touch BUCATO"
        self.repo.scrivi([milestone(1, "1.1.0", criteri + criteri_di_rilascio(False))])
        self.repo.lancia("--json")
        self.assertFalse((self.repo.radice / "BUCATO").exists())


class TestRilasciata(_ConRepo):
    def test_anche_il_rilascio_vero_non_compare_in_pronte(self):
        self.repo.scrivi([
            milestone(1, "1.0.0", criteri_di_lavoro() + criteri_di_rilascio(True)),
            milestone(2, "1.1.0", criteri_di_lavoro() + criteri_di_rilascio(False)),
        ])
        p = self.repo.lancia("--pronte")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.split(), ["1.1.0"])
        stati = [m["stato"] for m in json.loads(self.repo.lancia("--json").stdout)["milestone"]]
        self.assertEqual(stati, ["rilasciata", "pronta"])


class TestRegistroRotto(_ConRepo):
    def _rotto(self, criterio: dict) -> subprocess.CompletedProcess:
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro() + [criterio])])
        return self.repo.lancia("--check")

    def test_file_citato_che_manca(self):
        p = self._rotto({"id": "x", "tipo": "file", "testo": "t", "file": "docs/NON-CE.md",
                         "regex": "a", "deve": "comparire"})
        self.assertEqual(p.returncode, 2)
        self.assertIn("NON-CE.md", p.stdout + p.stderr)

    def test_regex_che_non_compila(self):
        p = self._rotto({"id": "x", "tipo": "file", "testo": "t", "file": "docs/GUIDA.md",
                         "regex": "([", "deve": "comparire"})
        self.assertEqual(p.returncode, 2)

    def test_deve_sconosciuto(self):
        p = self._rotto({"id": "x", "tipo": "file", "testo": "t", "file": "docs/GUIDA.md",
                         "regex": "a", "deve": "forse"})
        self.assertEqual(p.returncode, 2)

    def test_id_doppio(self):
        p = self._rotto(dict(criteri_di_lavoro()[0]))
        self.assertEqual(p.returncode, 2)
        self.assertIn("guida", p.stdout + p.stderr)

    def test_script_del_comando_che_non_esiste(self):
        p = self._rotto({"id": "x", "tipo": "comando", "testo": "t",
                         "comando": "python3 scripts/non_esiste.py --check"})
        self.assertEqual(p.returncode, 2)
        self.assertIn("non_esiste.py", p.stdout + p.stderr)

    def test_programma_del_comando_che_non_esiste(self):
        p = self._rotto({"id": "x", "tipo": "comando", "testo": "t",
                         "comando": "programma-che-non-esiste-davvero --check"})
        self.assertEqual(p.returncode, 2)

    def test_tipo_sconosciuto(self):
        p = self._rotto({"id": "x", "tipo": "sondaggio", "testo": "t"})
        self.assertEqual(p.returncode, 2)

    def test_dm_confermato_senza_dove(self):
        p = self._rotto({"id": "x", "tipo": "dm", "testo": "t", "confermato": {"data": "2026-11-27"}})
        self.assertEqual(p.returncode, 2)

    def test_numero_doppio(self):
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro()),
                          milestone(1, "1.2.0", criteri_di_lavoro())])
        self.assertEqual(self.repo.lancia("--check").returncode, 2)

    def test_json_non_valido(self):
        self.repo.registro.write_text("{ non è json", encoding="utf-8")
        self.assertEqual(self.repo.lancia("--check").returncode, 2)

    def test_registro_rotto_ferma_anche_pronte(self):
        self._rotto({"id": "x", "tipo": "sondaggio", "testo": "t"})
        p = self.repo.lancia("--pronte")
        self.assertEqual(p.returncode, 2)
        self.assertEqual(p.stdout.strip(), "")

    def test_solo_integrita_non_esegue_i_comandi(self):
        criteri = criteri_di_lavoro()
        (self.repo.radice / "scripts" / "traccia.py").write_text(
            "from pathlib import Path\nPath('ESEGUITO').write_text('x')\n", encoding="utf-8")
        criteri[2]["comando"] = "python3 scripts/traccia.py"
        self.repo.scrivi([milestone(1, "1.1.0", criteri)])
        p = self.repo.lancia("--check", "--solo-integrita")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertFalse((self.repo.radice / "ESEGUITO").exists())


class TestCheckMisura(_ConRepo):
    def test_check_esce_0_anche_se_niente_e_pronto(self):
        """È una misura (canale testing): un criterio falso non è un errore."""
        self.repo.scrivi([milestone(1, "1.1.0",
                                    criteri_di_lavoro(dm_confermato=False) + criteri_di_rilascio(False))])
        self.assertEqual(self.repo.lancia("--check").returncode, 0)


class TestGithub(_ConRepo):
    def test_senza_gh_dice_non_misurato_e_non_fallisce(self):
        import os
        self.repo.scrivi([milestone(1, "1.1.0", criteri_di_lavoro())])
        env = {**os.environ, "PATH": "/nonexistent"}  # niente gh sul PATH
        p = subprocess.run([sys.executable, str(SCRIPT), "--registro", str(self.repo.registro),
                            "--radice", str(self.repo.radice), "--github", "--json"],
                           capture_output=True, text=True, timeout=120, env=env)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["github"]["esito"], "non misurato")


class TestRegistroVero(unittest.TestCase):
    def test_il_registro_del_repo_e_integro(self):
        p = esegui("--check", "--solo-integrita")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_ogni_milestone_ha_i_tre_criteri_di_rilascio(self):
        """Senza uno dei tre, «pronta» e «rilasciata» non si distinguono più."""
        reg = json.loads((REPO / "plans" / "milestone.json").read_text(encoding="utf-8"))
        for m in reg["milestone"]:
            ids = {c["id"] for c in m["criteri"]}
            self.assertTrue(set(RILASCIO) <= ids, f"M{m['numero']}: mancano {set(RILASCIO) - ids}")


if __name__ == "__main__":
    unittest.main()
