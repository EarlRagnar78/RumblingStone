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


if __name__ == "__main__":
    unittest.main()
