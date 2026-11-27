"""lavoro_in_corso.py: l'istantanea del lavoro in sviluppo, fuori da main.

I test girano in un repository temporaneo con rami finti, PR da fixture JSON
e una cartella condivisa finta: nessuna rete, niente /mnt vero. Il clone vero
conosce rami diversi da una macchina all'altra, e un test che dipende da
quali rami ci sono e' un test che mente.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import lavoro_in_corso as L  # noqa: E402

ORA = "2026-11-27T12:00:00Z"
ORA_DT = datetime(2026, 11, 27, 12, 0, tzinfo=timezone.utc)
THREAD = "cmsg_0123abcDEF"


def _git(radice: Path, *args: str, data: "str | None" = None) -> str:
    env = dict(os.environ)
    if data:
        env.update(GIT_COMMITTER_DATE=data, GIT_AUTHOR_DATE=data)
    return subprocess.run(["git", *args], cwd=radice, capture_output=True, text=True,
                          check=True, env=env).stdout


def _ramo(radice: Path, nome: str, data: str) -> None:
    _git(radice, "commit", "-q", "--allow-empty", "-m", nome, data=data)
    _git(radice, "update-ref", f"refs/remotes/origin/{nome}", "HEAD")


def _repo(radice: Path) -> None:
    _git(radice, "init", "-q", "-b", "main")
    _git(radice, "config", "user.email", "t@t")
    _git(radice, "config", "user.name", "t")
    (radice / "scripts").mkdir()
    (radice / "scripts" / "esiste.py").write_text("x = 1\n", encoding="utf-8")
    _git(radice, "add", ".")
    _git(radice, "commit", "-q", "-m", "base", data="2026-11-01T10:00:00Z")
    _git(radice, "update-ref", "refs/remotes/origin/main", "HEAD")
    _ramo(radice, "claude/del-filone", "2026-11-26T10:00:00Z")
    _ramo(radice, "claude/della-pr-orfana", "2026-11-26T10:00:00Z")
    _ramo(radice, "claude/sciolto", "2026-11-25T10:00:00Z")       # senza filone
    _ramo(radice, "claude/nei-rami", "2026-11-25T10:00:00Z")      # in contenuti-nei-rami
    _ramo(radice, "claude/vecchio", "2026-10-01T10:00:00Z")       # oltre i 14 giorni
    _ramo(radice, "dependabot/pip/x", "2026-11-26T10:00:00Z")     # non claude/*


def _registro(**sopra) -> dict:
    filone = {
        "id": "misure", "titolo": "Misure degli agenti", "stato": "in-corso",
        "thread": "Misurare gli agenti", "thread_id": THREAD,
        "pr": [10, 99], "rami": ["claude/del-filone"], "mnt": ["eval-filone/sotto"],
        "repo": ["scripts/esiste.py"], "aspetta": "", "prossimo": "finire",
        "aggiornato": "2026-11-27",
    }
    filone.update(sopra)
    return {"_cos_e": "prova", "stati": dict(L.STATI), "servizio": [
        {"cartella": "specchio", "perche": "infrastruttura"}], "filoni": [filone]}


def _pr(numero, ramo, aggiornata, corpo="", bozza=True, titolo=None):
    """Una PR nel formato REST di /pulls."""
    return {"number": numero, "title": titolo or f"PR {numero}", "draft": bozza,
            "head": {"ref": ramo}, "updated_at": aggiornata, "body": corpo,
            "html_url": f"https://github.com/o/r/pull/{numero}"}


PRS = [
    _pr(10, "claude/del-filone", "2026-11-27T10:00:00Z"),
    _pr(11, "claude/via-thread", "2026-11-26T10:00:00Z", corpo=f"x thread={THREAD} y"),
    _pr(12, "claude/della-pr-orfana", "2026-11-25T10:00:00Z", bozza=False),
    _pr(13, "dependabot/pip/x", "2026-10-01T10:00:00Z", bozza=False),   # >30 giorni
]


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.radice = self.tmp / "repo"
        self.radice.mkdir()
        _repo(self.radice)
        self.mnt = self.tmp / "mnt"
        self.mnt.mkdir()
        fresco = ORA_DT.timestamp() - 86400
        vecchio = ORA_DT.timestamp() - 40 * 86400
        for nome, quando in (("eval-filone", fresco), ("sciolta", fresco),
                             ("vecchia", vecchio), ("specchio", fresco)):
            d = self.mnt / nome
            d.mkdir()
            (d / "LEGGIMI.md").write_text(f"# Titolo di {nome}\n\ncorpo segreto\n",
                                          encoding="utf-8")
            for p in (d / "LEGGIMI.md", d):
                os.utime(p, (quando, quando))
        self.reg = self.tmp / "lavoro.json"
        self.reg.write_text(json.dumps(_registro()), encoding="utf-8")
        self.contenuti = self.tmp / "contenuti.json"
        self.contenuti.write_text(json.dumps({"rami": [
            {"ref": ["pr/7", "origin/claude/nei-rami"], "stato": "in-volo", "dove": "x"}]}),
            encoding="utf-8")
        self.prjson = self.tmp / "prs.json"
        self.prjson.write_text(json.dumps(PRS), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def rapporto(self, prs=PRS, mnt=None, errore=None):
        return L.rapporto(L.leggi_registro(self.reg), prs, errore,
                          L.rami_remoti(self.radice), L.cartelle(mnt or self.mnt, 14, ORA_DT),
                          L.leggi_contenuti(self.contenuti), ORA_DT, 14)

    def main(self, *argv):
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("rete!")):
            return L.main(["--radice", str(self.radice), "--registro", str(self.reg),
                           "--contenuti", str(self.contenuti), "--ora", ORA, *argv])


class TestPR(Base):
    def test_attacco_via_thread_id(self):
        r = self.rapporto()
        f = r["filoni"][0]
        numeri = {p["numero"]: p for p in f["pr_aperte"]}
        self.assertIn(11, numeri)
        self.assertTrue(numeri[11]["via_thread"])
        self.assertFalse(numeri[10]["via_thread"])

    def test_pr_senza_filone(self):
        r = self.rapporto()
        self.assertEqual([p["numero"] for p in r["senza_filone"]["pr"]], [13, 12])  # dalla più recente

    def test_pr_del_registro_chiusa(self):
        r = self.rapporto()
        self.assertEqual(r["da_aggiornare"]["pr_chiuse"], [{"filone": "misure", "pr": 99}])

    def test_pr_ferma_oltre_trenta_giorni(self):
        r = self.rapporto()
        self.assertEqual([p["numero"] for p in r["da_aggiornare"]["pr_ferme"]], [13])
        self.assertEqual(r["da_aggiornare"]["pr_ferme"][0]["giorni"], 57)

    def test_formato_gh(self):
        gh = [{"number": 11, "title": "t", "headRefName": "claude/x", "isDraft": False,
               "updatedAt": "2026-11-26T10:00:00Z", "url": "u", "body": f"thread={THREAD}"}]
        p = L.normalizza_pr(gh)[0]
        self.assertEqual((p["numero"], p["ramo"], p["bozza"], p["thread_id"]),
                         (11, "claude/x", False, THREAD))

    def test_errore_di_rete_detto_e_niente_chiuse(self):
        r = self.rapporto(prs=None, errore="URLError: niente rete")
        self.assertEqual(r["pr_errore"], "URLError: niente rete")
        self.assertEqual(r["da_aggiornare"]["pr_chiuse"], [])
        md = L.pagina(r)
        self.assertIn("niente rete", md)


class TestRamiECartelle(Base):
    def test_rami_senza_posto(self):
        r = self.rapporto()
        nomi = [x["nome"] for x in r["senza_filone"]["rami"]]
        # del-filone: nel registro; della-pr-orfana: ha una PR aperta; nei-rami:
        # in contenuti-nei-rami; vecchio: fuori finestra; dependabot: non claude/*
        self.assertEqual(nomi, ["claude/sciolto"])

    def test_cartella_senza_filone(self):
        r = self.rapporto()
        self.assertEqual([c["nome"] for c in r["senza_filone"]["cartelle"]], ["sciolta"])
        self.assertEqual(r["senza_filone"]["cartelle"][0]["titolo"], "Titolo di sciolta")

    def test_mai_il_contenuto_dei_file(self):
        md = L.pagina(self.rapporto())
        self.assertNotIn("corpo segreto", md)

    def test_cartella_assente(self):
        r = L.rapporto(L.leggi_registro(self.reg), PRS, None, L.rami_remoti(self.radice),
                       L.cartelle(self.tmp / "non-c-e", 14, ORA_DT),
                       L.leggi_contenuti(self.contenuti), ORA_DT, 14)
        self.assertIsNone(r["cartelle"])
        self.assertIn("non c'è su questa macchina", L.pagina(r))

    def test_filone_vecchio(self):
        self.reg.write_text(json.dumps(_registro(aggiornato="2026-11-01")), encoding="utf-8")
        r = self.rapporto()
        self.assertEqual(r["da_aggiornare"]["filoni_vecchi"],
                         [{"filone": "misure", "aggiornato": "2026-11-01", "giorni": 26}])


class TestCheck(Base):
    def test_registro_buono(self):
        self.assertEqual(L.valida(_registro(), self.radice), [])

    def test_registro_rotto(self):
        rotto = _registro(stato="boh", pr=["12"], aggiornato="27/11/2026",
                          repo=["non/esiste.md"], thread_id="cmsg-no", mnt=["/assoluta"])
        rotto["filoni"].append(dict(rotto["filoni"][0], titolo=""))
        errori = "\n".join(L.valida(rotto, self.radice))
        for atteso in ("stato «boh»", "pr", "aggiornato", "non/esiste.md", "thread_id",
                       "/assoluta", "id ripetuto", "titolo"):
            self.assertIn(atteso, errori)

    def test_stati_allineati_allo_script(self):
        reg = _registro()
        reg["stati"]["nuovo"] = "x"
        self.assertTrue(any("stati" in e for e in L.valida(reg, self.radice)))

    def test_registro_del_repo_valido(self):
        self.assertEqual(L.valida(L.leggi_registro(), ROOT), [])

    def test_niente_email(self):
        errori = L.valida(_registro(aspetta="scrivere a uno@esempio.it"), self.radice)
        self.assertTrue(any("email" in e for e in errori))

    def test_check_esce_1_sul_registro_rotto(self):
        self.reg.write_text(json.dumps(_registro(stato="boh")), encoding="utf-8")
        self.assertEqual(self.main("--check"), 1)
        self.reg.write_text(json.dumps(_registro()), encoding="utf-8")
        self.assertEqual(self.main("--check"), 0)


class TestUscita(Base):
    def test_scrive_la_pagina_senza_rete(self):
        uscita = self.tmp / "LAVORO.md"
        codice = self.main("--pr-json", str(self.prjson), "--mnt", str(self.mnt),
                           "--uscita", str(uscita))
        self.assertEqual(codice, 0)
        md = uscita.read_text(encoding="utf-8")
        self.assertIn("non si scrive a mano", md)
        self.assertIn("2026-11-27 12:00 UTC", md)
        for sezione in ("## Filoni", "## Senza filone", "## Da aggiornare", "## Dove guardare"):
            self.assertIn(sezione, md)
        self.assertIn("#11", md)

    def test_offline_e_json(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            codice = self.main("--offline", "--mnt", str(self.mnt), "--json")
        self.assertEqual(codice, 0)
        dati = json.loads(buf.getvalue())
        self.assertIsNone(dati["pr"])
        self.assertIn("offline", dati["pr_errore"])


class TestRemoto(unittest.TestCase):
    def test_owner_repo(self):
        for url in ("https://github.com/o/r.git", "git@github.com:o/r.git",
                    "http://proxy@127.0.0.1:1234/git/o/r"):
            self.assertEqual(L.owner_repo_da_url(url), ("o", "r"))


PIANO_FINTO = """# Piano

## §1 · Prima

| Componente | Canale |
|---|---|
| fuori | **testing** |

## §2 · Il censimento

### Strumenti

| Componente | Versione | Canale proposto |
|---|---|---|
| ruff | 0.16.9 | **stable** dal 2026-11-08 (P3) |
| shellcheck | del runner | **testing** (`|| true`); stable con A6 |
| custode (`--hook-merge`) | stdlib | **testing** dal 2026-11-27: il merge si ferma |
| mypy | 2.3.1 | **unstable**, non si adotta |
| `compileall` | stdlib | **uscito** dalla CI il 2026-11-08 |
| pre-commit | — | **non si adotta** |
| `import fitz` | — | da migrare a `import pymupdf` |

### Le pipeline

| Pipeline | Componenti | Stato |
|---|---|---|
| booklet | Chromium | testing in PDF |

## §3 · Lotti

| x | **testing** |
|---|---|
"""


class TestCanali(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.piano = Path(self._tmp.name) / "PIANO.md"
        self.piano.write_text(PIANO_FINTO, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_righe_canali_e_date(self):
        righe = L.canali_piattaforma(self.piano)
        per = {r["componente"]: r for r in righe}
        self.assertEqual([r["componente"] for r in righe],
                         ["ruff", "shellcheck", "custode (`--hook-merge`)", "mypy",
                          "`compileall`", "pre-commit", "`import fitz`", "booklet"])
        self.assertEqual((per["ruff"]["canale"], per["ruff"]["dal"]), ("stable", "2026-11-08"))
        self.assertEqual((per["shellcheck"]["canale"], per["shellcheck"]["dal"]), ("testing", None))
        self.assertIn("|| true", per["shellcheck"]["stato"])       # il codice non spezza la cella
        self.assertEqual(per["custode (`--hook-merge`)"]["dal"], "2026-11-27")
        self.assertEqual(per["mypy"]["canale"], "unstable")
        self.assertEqual(per["`compileall`"]["canale"], "uscito")
        self.assertEqual(per["pre-commit"]["canale"], "non-si-adotta")
        self.assertEqual(per["`import fitz`"]["canale"], "altro")
        self.assertEqual(per["booklet"]["canale"], "testing")
        self.assertEqual(per["booklet"]["sezione"], "Le pipeline")
        self.assertEqual(self.piano.read_text().splitlines()[per["ruff"]["riga"] - 1].split("|")[1].strip(),
                         "ruff")

    def test_piano_assente(self):
        self.assertIsNone(L.canali_piattaforma(Path(self._tmp.name) / "no.md"))

    def test_sezione_nella_pagina_e_nel_json(self):
        canali = L.canali_piattaforma(self.piano)
        r = L.rapporto(_registro(canale="testing"), [], None, [], [], {}, ORA_DT, 14,
                       canali=canali)
        self.assertEqual(r["canali"]["conteggio"], {"stable": 1, "testing": 3, "unstable": 1,
                                                    "uscito": 1, "non-si-adotta": 1, "altro": 1})
        md = L.pagina(r)
        self.assertIn("## Canali della piattaforma (ADR-0099)", md)
        self.assertIn("shellcheck", md)
        self.assertIn("mypy", md)
        self.assertNotIn("| ruff |", md)
        self.assertIn("Gli stable sono 1", md)
        self.assertIn("scritta a mano", md)
        self.assertIn("| `testing` |", md)                       # colonna canale dei filoni

    def test_canale_del_filone_validato(self):
        self.assertEqual(L.valida(_registro(canale="testing", repo=[]), ROOT), [])
        self.assertEqual(L.valida(_registro(canale="", repo=[]), ROOT), [])
        errori = L.valida(_registro(canale="beta", repo=[]), ROOT)
        self.assertTrue(any("canale" in e for e in errori))

    def test_piano_vero_si_legge(self):
        righe = L.canali_piattaforma()
        self.assertTrue(righe and any(r["canale"] == "testing" for r in righe))


if __name__ == "__main__":
    unittest.main()
