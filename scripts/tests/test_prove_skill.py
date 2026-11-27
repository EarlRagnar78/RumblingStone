"""prove_skill.py e la scheda della skill in validate_skills.py (ADR-0114).

Le prove con trappola stanno in skills/<nome>/evals/ nella forma di
`claude plugin eval`: qui si controlla che il repo sia in forma, che un caso
rotto venga bocciato, che il piano A/B non sveli la versione e che l'esito dica
quando la versione nuova peggiora.
"""
from __future__ import annotations

import io
import json
import sys
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prove_skill as P  # noqa: E402
import validate_skills as V  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

CASO_BUONO = {
    "prompt.md": "---\ntags: [rumblingstone]\nmax_turns: 5\n---\n\nScrivi la CD.\n",
    "case.yaml": 'schema_version: "1.1"\nname: trappola-uno\nexpected_outcome: |\n  Non inventa.\n',
    "graders/01-non-inventa.md": "---\ntype: llm\nfocus: trace\nweight: 1\n---\n\nNon inventa.\n",
}


def finto(d: Path, skill: str, caso: str, file: "dict[str, str]") -> None:
    (d / "skills" / skill).mkdir(parents=True, exist_ok=True)
    (d / "skills" / skill / "SKILL.md").write_text(
        f"---\nname: {skill}\ndescription: x\n---\n\n# {skill}\n", encoding="utf-8")
    for rel, testo in file.items():
        p = d / "skills" / skill / "evals" / caso / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(testo, encoding="utf-8")


def zitto(f, *a):
    with redirect_stdout(io.StringIO()) as out:
        rc = f(*a)
    return rc, out.getvalue()


class TestRepo(unittest.TestCase):
    def test_i_casi_del_repo_sono_in_forma_e_bastano(self):
        rc, out = zitto(P.main, ["--repo-root", str(ROOT), "controlla"])
        self.assertEqual(rc, 0, out)
        self.assertIn("0 skill sotto il minimo", out)


class TestControlla(unittest.TestCase):
    def test_caso_buono_passa(self):
        with tempfile.TemporaryDirectory() as t:
            finto(Path(t), "s", "trappola-uno", CASO_BUONO)
            caso = Path(t) / "skills/s/evals/trappola-uno"
            self.assertEqual(P.controlla_caso(caso), [])

    def test_caso_rotto_bocciato(self):
        rotto = dict(CASO_BUONO)
        rotto["prompt.md"] = "---\nmodello: x\n---\n\nScrivi.\n"          # chiave sconosciuta
        rotto["case.yaml"] = "schema_version: 1.1\nname: altro\n"           # numero, nome, esito
        rotto["graders/01-non-inventa.md"] = "Non inventa.\n"              # senza blocco
        with tempfile.TemporaryDirectory() as t:
            finto(Path(t), "s", "trappola-uno", rotto)
            err = " ".join(P.controlla_caso(Path(t) / "skills/s/evals/trappola-uno"))
        for atteso in ("chiavi sconosciute", "virgolette", "diverso dalla cartella",
                       "expected_outcome", "type valido"):
            self.assertIn(atteso, err)


class TestAB(unittest.TestCase):
    def test_piano_alla_cieca_ed_esito(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            finto(d, "s", "trappola-uno", CASO_BUONO)
            uscita = d / "ab"
            rc, _ = zitto(P.main, ["--repo-root", str(d), "prepara", "--uscita", str(uscita)])
            self.assertEqual(rc, 0)
            piano = json.loads((uscita / "piano.json").read_text(encoding="utf-8"))
            self.assertEqual(len(piano), 2)
            self.assertNotIn("vecchia", json.dumps(piano))      # il piano non svela la versione
            chiave = json.loads((uscita / "chiave.json").read_text(encoding="utf-8"))
            inv = {v: k.split("|")[1] for k, v in chiave.items()}
            giudizi = [
                {"caso": "s/trappola-uno", "lettera": inv["vecchia"], "inventati_senza_marca": 1},
                {"caso": "s/trappola-uno", "lettera": inv["nuova"], "inventati_senza_marca": 4},
            ]
            (uscita / "giudizi.json").write_text(json.dumps(giudizi), encoding="utf-8")
            rc, out = zitto(P.main, ["--repo-root", str(d), "esito", "--piano", str(uscita)])
            self.assertEqual(rc, 1)
            self.assertIn("PEGGIORA", out)

    def test_segno(self):
        self.assertAlmostEqual(P.segno(11, 4), 0.0592, places=3)   # la A/B di ADR-0109
        self.assertEqual(P.segno(0, 0), 1.0)


class TestScheda(unittest.TestCase):
    def test_scheda_completa_senza_rilievi_e_fuori_ordine_segnalata(self):
        sezioni = ["Quando no", "Fonti", "Procedura", "Formato d'uscita",
                   "Prima di consegnare", "Cancelli deterministici"]
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            for i in range(3):
                finto(d, "s", f"trappola-{i}", CASO_BUONO)
            corpo = "".join(f"## {s}\n\nx\n\n" for s in sezioni)
            f = d / "skills/s/SKILL.md"
            f.write_text("---\nname: s\ndescription: x\n---\n\n" + corpo, encoding="utf-8")
            self.assertEqual(V.check_schede(d), [])
            f.write_text("---\nname: s\ndescription: x\n---\n\n"
                         + "".join(f"## {s}\n\nnel 2026-11-08\n\n" for s in reversed(sezioni)),
                         encoding="utf-8")
            rilievi = " ".join(V.check_schede(d))
            self.assertIn("fuori ordine", rilievi)
            self.assertIn("date nel corpo", rilievi)

    def _main(self, rilievi, *argv):
        vero, argv_vero = V.check_schede, sys.argv
        V.check_schede = lambda root: list(rilievi)
        sys.argv = ["validate_skills.py", *argv]
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                return V.main(), out.getvalue()
        finally:
            V.check_schede, sys.argv = vero, argv_vero

    def test_un_rilievo_della_scheda_e_un_errore(self):
        # ADR-0114 promossa a stable il 2026-11-25 (ADR-0099): la scheda non avvisa, blocca
        esito, out = self._main(["skills/s: scheda senza Fonti (ADR-0114)"])
        self.assertEqual(esito, 1)
        self.assertIn("ERROR skills/s: scheda senza Fonti", out)
        self.assertNotIn("WARN  skills/s", out)
        esito, out = self._main(["skills/s: scheda senza Fonti (ADR-0114)"], "--json")
        self.assertEqual(esito, 1)
        self.assertIn("skills/s: scheda senza Fonti (ADR-0114)", json.loads(out)["errors"])

    def test_senza_rilievi_le_skill_del_repo_passano(self):
        self.assertEqual(self._main([])[0], 0)




# ------------------------------------------------------------ agenti (ADR-0148)

def _ese(d: Path, risposta: str = "", trace: str = "", file: "dict[str, str] | None" = None) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    (d / "risposta.md").write_text(risposta, encoding="utf-8")
    if trace:
        (d / "trace.jsonl").write_text(trace, encoding="utf-8")
    for rel, testo in (file or {}).items():
        p = d / "files" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(testo, encoding="utf-8")
    return d


def _uso(nome: str, inp: dict) -> str:
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": nome, "input": inp}]}}) + "\n"


class TestAgentiNelRepo(unittest.TestCase):
    def test_ogni_agente_ha_tre_casi_in_forma(self):
        rc, out = zitto(P.main, ["--repo-root", str(ROOT), "controlla", "--agenti"])
        self.assertEqual(rc, 0, out)
        self.assertIn("0 agenti sotto il minimo", out)

    def test_i_giudici_promuovono_la_buona_e_bocciano_la_cattiva(self):
        rc, out = zitto(P.main, ["--repo-root", str(ROOT), "esempi"])
        self.assertEqual(rc, 0, out)

    def test_ogni_caso_ha_un_giudice_deterministico(self):
        for caso in P.casi_agenti(ROOT):
            tipi = {(P._blocco(f.read_text(encoding="utf-8"))[0] or {}).get("type")
                    for f in (caso / "graders").glob("*.md")}
            self.assertTrue(tipi & P.DETERMINISTICI, caso)

    def test_l_impronta_non_dipende_dai_fine_riga_ne_dai_file_di_cache(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            (d / ".claude" / "agents").mkdir(parents=True)
            md = d / ".claude" / "agents" / "a.md"
            md.write_bytes(b"---\nname: a\nskills:\n  - s\n---\ncorpo\n")
            (d / "skills" / "s").mkdir(parents=True)
            prima = P.impronta(d, "a")
            md.write_bytes(b"---\r\nname: a\r\nskills:\r\n  - s\r\n---\r\ncorpo\r\n")
            (d / "skills" / "s" / "__pycache__").mkdir()
            (d / "skills" / "s" / "__pycache__" / "x.pyc").write_bytes(b"\0")
            self.assertEqual(P.impronta(d, "a"), prima)


class TestGiudici(unittest.TestCase):
    def test_regex_contains_not_contains_count(self):
        with tempfile.TemporaryDirectory() as t:
            e = _ese(Path(t) / "e", "CD 17, poi ancora 17")
            self.assertTrue(P.giudica({"type": "regex", "pattern": r"\b17\b"}, e))
            self.assertFalse(P.giudica({"type": "regex", "pattern": r"\b17\b", "match": "not_contains"}, e))
            self.assertTrue(P.giudica({"type": "regex", "pattern": r"\b17\b", "match": "count:2"}, e))
            self.assertFalse(P.giudica({"type": "regex", "pattern": "cd", "flags": ""}, e))
            self.assertTrue(P.giudica({"type": "regex", "pattern": "cd", "flags": "i"}, e))

    def test_regex_su_trace_e_file(self):
        with tempfile.TemporaryDirectory() as t:
            e = _ese(Path(t) / "e", "", _uso("Read", {"file_path": "campaign/REGISTRO-PX.md"}),
                     {"out/nota.md": "Hella 86.354"})
            self.assertTrue(P.giudica({"type": "regex", "pattern": "REGISTRO-PX", "target": "trace"}, e))
            self.assertTrue(P.giudica({"type": "regex", "pattern": "nota", "target": "files"}, e))
            self.assertTrue(P.giudica({"type": "regex", "pattern": "86.354",
                                       "target": {"source": "file", "path": "out/*.md"}}, e))
            self.assertTrue(P.giudica({"type": "file_exists", "path": "out/*.md"}, e))
            self.assertFalse(P.giudica({"type": "file_exists", "path": "altro/*.md"}, e))

    def test_tool_used_e_tool_order(self):
        with tempfile.TemporaryDirectory() as t:
            e = _ese(Path(t) / "e", "", _uso("Read", {"file_path": "a.py"}) + _uso("Edit", {"file_path": "a.py"}))
            self.assertTrue(P.giudica({"type": "tool_used", "tool": "Edit", "input_match": "a\\.py"}, e))
            self.assertFalse(P.giudica({"type": "tool_used", "tool": "Edit", "input_match": "",
                                        "min": 0, "max": 0}, e))
            self.assertTrue(P.giudica({"type": "tool_order", "before": "Read", "after": "Edit"}, e))
            self.assertFalse(P.giudica({"type": "tool_order", "before": "Edit", "after": "Read"}, e))
            self.assertIsNone(P.giudica({"type": "llm"}, e))

    def test_un_caso_d_agente_senza_giudice_deterministico_e_bocciato(self):
        with tempfile.TemporaryDirectory() as t:
            caso = Path(t) / ".claude" / "agent-evals" / "regolista" / "trappola-uno"
            for rel, testo in CASO_BUONO.items():
                (caso / rel).parent.mkdir(parents=True, exist_ok=True)
                (caso / rel).write_text(testo, encoding="utf-8")
            err = P.controlla_caso(caso)
            self.assertTrue(any("deterministico" in e for e in err), err)
            self.assertTrue(any("esempi/buona" in e for e in err), err)


class TestCricchetto(unittest.TestCase):
    def _repo(self, d: Path) -> Path:
        (d / ".claude" / "agents").mkdir(parents=True)
        (d / ".claude" / "agents" / "a.md").write_text("---\nname: a\nskills:\n  - s\n---\n", encoding="utf-8")
        (d / "skills" / "s").mkdir(parents=True)
        (d / "skills" / "s" / "SKILL.md").write_text("uno", encoding="utf-8")
        return d

    def _registra(self, d: Path, impronta: str, punteggio: float) -> None:
        f = d / P.ESITI
        f.parent.mkdir(parents=True, exist_ok=True)
        with f.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"agente": "a", "impronta": impronta, "punteggio": punteggio}) + "\n")

    def test_senza_esito_peggiore_e_buono(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._repo(Path(t))
            self.assertIn("nessun esito", P.cricchetto(d, ["a"])[0])
            vecchia = P.impronta(d, "a")
            self._registra(d, vecchia, 0.9)
            self.assertEqual(P.cricchetto(d, ["a"]), [])
            (d / "skills" / "s" / "SKILL.md").write_text("due", encoding="utf-8")
            nuova = P.impronta(d, "a")
            self.assertNotEqual(vecchia, nuova, "la skill cambiata cambia l'impronta dell'agente")
            self._registra(d, nuova, 0.8)
            self.assertIn("sotto il precedente", P.cricchetto(d, ["a"])[0])
            self._registra(d, nuova, 0.95)
            self.assertEqual(P.cricchetto(d, ["a"]), [])


class TestEseguiERegistra(unittest.TestCase):
    """Le parti di `esegui` e `registra` che non chiamano un modello."""

    def _git(self, d: Path, *a: str) -> None:
        subprocess.run(["git", *a], cwd=d, check=True, capture_output=True)

    def test_file_toccati_anche_in_cartelle_nuove_e_con_accenti(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            self._git(d, "init", "-q")
            (d / "vecchio.md").write_text("a", encoding="utf-8")
            self._git(d, "add", ".")
            self._git(d, "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "x")
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d, capture_output=True,
                                 text=True).stdout.strip()
            (d / "07_il Portale" / "città").mkdir(parents=True)
            (d / "07_il Portale" / "città" / "nuovo.md").write_text("b", encoding="utf-8")
            (d / "vecchio.md").write_text("c", encoding="utf-8")
            self.assertEqual(P._file_toccati(d, sha),
                             ["07_il Portale/città/nuovo.md", "vecchio.md"])

    def _caso(self, root: Path, nome: str) -> None:
        caso = root / P.DIR_PROVE_AGENTI / "a" / nome
        (caso / "graders").mkdir(parents=True)
        (caso / "graders" / "01.md").write_text("---\ntype: regex\npattern: sì\n---\nDice sì.\n",
                                                encoding="utf-8")

    def test_un_caso_fallito_vale_zero_e_le_impronte_devono_coincidere(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for n in ("uno", "due"):
                self._caso(root, n)
            ese = root / "ese"
            for n in ("uno", "due"):
                _ese(ese / n, "sì")
                (ese / n / "impronta.txt").write_text("abc\n", encoding="utf-8")
            (ese / "due" / "ERRORE.txt").write_text("oltre 900 s", encoding="utf-8")
            rc, out = zitto(P.main, ["--repo-root", str(root), "registra", "--agente", "a",
                                     "--esecuzioni", str(ese), "--data", "2026-11-20"])
            self.assertEqual(rc, 0, out)
            voce = json.loads((root / P.ESITI).read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual((voce["punteggio"], voce["saltati"], voce["impronta"]), (0.5, ["due"], "abc"))
            (ese / "due" / "impronta.txt").write_text("def\n", encoding="utf-8")
            rc, _ = zitto(P.main, ["--repo-root", str(root), "registra", "--agente", "a",
                                   "--esecuzioni", str(ese), "--data", "2026-11-20"])
            self.assertEqual(rc, 1, "impronte diverse fra le esecuzioni: non si registra")

    def test_esempi_boccia_un_giudice_che_non_distingue(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            self._caso(root, "uno")
            caso = root / P.DIR_PROVE_AGENTI / "a" / "uno"
            _ese(caso / "esempi" / "buona", "sì")
            _ese(caso / "esempi" / "cattiva", "sì, anche questa")
            rc, out = zitto(P.main, ["--repo-root", str(root), "esempi"])
            self.assertEqual(rc, 1, out)
            self.assertIn("non discriminano", out)

    def test_agenti_cambiati_esclude_le_prove_delle_skill(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t)
            self._git(d, "init", "-q")
            (d / ".claude" / "agents").mkdir(parents=True)
            (d / ".claude" / "agents" / "a.md").write_text("---\nname: a\nskills:\n  - s\n---\n",
                                                           encoding="utf-8")
            (d / "skills" / "s" / "evals").mkdir(parents=True)
            (d / "skills" / "s" / "SKILL.md").write_text("uno", encoding="utf-8")
            self._git(d, "add", ".")
            self._git(d, "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "base")
            self._git(d, "tag", "base")
            (d / "skills" / "s" / "evals" / "caso.md").write_text("x", encoding="utf-8")
            self._git(d, "add", ".")
            self._git(d, "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qm", "evals")
            self.assertEqual(P.agenti_cambiati(d, "base"), [])
            (d / "skills" / "s" / "SKILL.md").write_text("due", encoding="utf-8")
            self._git(d, "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qam", "skill")
            self.assertEqual(P.agenti_cambiati(d, "base"), ["a"])

    def test_un_match_sconosciuto_e_bocciato(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            self._caso(root, "uno")
            f = root / P.DIR_PROVE_AGENTI / "a" / "uno" / "graders" / "01.md"
            f.write_text("---\ntype: regex\npattern: sì\nmatch: contiene\n---\nDice sì.\n", encoding="utf-8")
            self.assertTrue(any("match" in e for e in P.controlla_caso(f.parents[1])))


if __name__ == "__main__":
    unittest.main()
