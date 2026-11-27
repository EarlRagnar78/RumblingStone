"""Test di memoria_custode.py (ADR-0151): lo specchio e il custode della memoria del progetto.

Tutto gira in cartelle temporanee fuori dal repo: memoria, specchio, coda e una
radice finta con il suo `plans/MEMORIA-STORICA.md`.
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memoria_coda as mc  # noqa: E402
import memoria_custode as cu  # noqa: E402

STORICA = """# Memoria storica

## Voci

### MS-0001 · 2026-10-19 · Il drago verde vola sopra la palude

- **Data:** 2026-10-19
- **PR:** #257
- **ADR:** —
- **Temi:** arc07 drago
- **Origine:** memoria del progetto
- **Testo:** Il drago verde vola sopra la palude delle lanterne e il guado resta chiuso fino alla terza notte.
"""

MEMORY = """# Progetto
Regole fisse del progetto e puntatori.
- Il drago verde vola sopra la palude delle lanterne, il guado resta chiuso (MS-0001).
- La stampa del volume usa sempre carta pesante e margini larghi nelle tavole.
- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.
"""

NOTA = """---
name: nota-forgia
description: La forgia sommersa e le sue chiavi
---
La forgia sommersa ha tre chiavi d'ottone nascoste nella cisterna.
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        d = Path(self.t.name)
        self.mem = d / "memoria"
        self.spe = d / "specchio"
        self.coda = d / "coda"
        self.rad = d / "radice"
        for c in (self.mem, self.coda, self.rad / "plans"):
            c.mkdir(parents=True)
        (self.rad / "plans" / "MEMORIA-STORICA.md").write_text(STORICA, encoding="utf-8")
        (self.mem / "MEMORY.md").write_text(MEMORY, encoding="utf-8")
        (self.mem / "nota-forgia.md").write_text(NOTA, encoding="utf-8")

    def tearDown(self):
        self.t.cleanup()

    def opz(self) -> "list[str]":
        return ["--memoria", str(self.mem), "--specchio", str(self.spe),
                "--coda", str(self.coda), "--radice", str(self.rad)]

    def gira(self, *argv: str, stdin: str = "") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), mock.patch("sys.stdin", io.StringIO(stdin)):
            codice = cu.main(list(argv) + self.opz())
        return codice, out.getvalue(), err.getvalue()

    def togli(self, testo: str, file: str = "MEMORY.md") -> None:
        f = self.mem / file
        f.write_text(f.read_text(encoding="utf-8").replace(testo + "\n", ""), encoding="utf-8")

    def scrivi_riservati(self, testo: str = "Gianlupo\n") -> None:
        self.spe.mkdir(parents=True, exist_ok=True)
        (self.spe / "RISERVATI.txt").write_text(testo, encoding="utf-8")

    def istantanee(self) -> "list[Path]":
        d = self.spe / "istantanee"
        return sorted(p for p in d.iterdir() if p.is_dir()) if d.is_dir() else []


class TestSpecchia(Base):
    def test_istantanea_idempotente(self):
        self.assertEqual(self.gira("specchia")[0], 0)
        self.assertEqual(self.gira("specchia")[0], 0)
        ist = self.istantanee()
        self.assertEqual(len(ist), 1)
        manifest = json.loads((ist[0] / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["file"]), {"MEMORY.md", "nota-forgia.md"})
        self.assertEqual(len(manifest["file"]["MEMORY.md"]), 64)
        self.assertEqual((self.spe / "ULTIMA.txt").read_text(encoding="utf-8").strip(), ist[0].name)
        self.assertFalse([p for p in (self.spe / "istantanee").iterdir() if p.name.startswith(".")])

    def test_contenuto_nuovo_fa_una_seconda_istantanea(self):
        self.gira("specchia")
        (self.mem / "MEMORY.md").write_text(MEMORY + "- riga nuova\n", encoding="utf-8")
        self.gira("specchia")
        self.assertEqual(len(self.istantanee()), 2)


class TestVerifica(Base):
    def test_prima_volta_passa_e_fa_l_istantanea(self):
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0)
        self.assertTrue(json.loads(out)["prima_volta"])
        self.assertEqual(len(self.istantanee()), 1)

    def test_riga_tolta_archiviata_in_una_voce_ms_passa(self):
        self.gira("specchia")
        self.togli("- Il drago verde vola sopra la palude delle lanterne, il guado resta chiuso (MS-0001).")
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0, out)
        self.assertEqual(json.loads(out)["non_archiviate"], [])

    def test_riga_tolta_non_archiviata_fallisce(self):
        self.gira("specchia")
        self.togli("- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.")
        codice, out, _ = self.gira("verifica")
        self.assertEqual(codice, 1)
        self.assertIn("MEMORY.md", out)
        self.assertIn("fabbro", out)
        # l'istantanea non avanza: la riga resta da archiviare
        self.assertEqual(len(self.istantanee()), 1)

    def test_hook_merge_esce_2_con_il_rimedio(self):
        self.scrivi_riservati()
        self.gira("specchia")
        self.togli("- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.")
        ev = {"tool_name": "mcp__github__merge_pull_request",
              "tool_input": {"owner": "GSamuele78", "repo": "rumblingstone", "pullNumber": 9}}
        codice, _, err = self.gira("--hook-merge", stdin=json.dumps(ev))
        self.assertEqual(codice, 2)
        self.assertIn("memoria_custode.py archivia", err)
        self.assertIn("ADR-0151", err)

    def test_riga_riscritta_che_perde_un_fatto_fallisce(self):
        self.gira("specchia")
        f = self.mem / "MEMORY.md"
        f.write_text(f.read_text(encoding="utf-8").replace(
            "- La stampa del volume usa sempre carta pesante e margini larghi nelle tavole.",
            "- La stampa del volume usa sempre carta."), encoding="utf-8")
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 1)
        riga = json.loads(out)["non_archiviate"][0]
        self.assertIn("pesante", riga["parole_mancanti"])

    def test_riga_spostata_passa(self):
        self.gira("specchia")
        riga = "- La stampa del volume usa sempre carta pesante e margini larghi nelle tavole."
        self.togli(riga)
        (self.mem / "nota-forgia.md").write_text(NOTA + riga + "\n", encoding="utf-8")
        self.assertEqual(self.gira("verifica")[0], 0)

    def test_riga_riservata_conta_nello_specchio(self):
        self.spe.mkdir()
        (self.spe / "RISERVATI.txt").write_text("fabbro anziano\n", encoding="utf-8")
        self.gira("specchia")
        self.togli("- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.")
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0, out)
        self.assertEqual(len(json.loads(out)["solo_specchio"]), 1)

    def test_file_tolto_intero_fallisce(self):
        self.gira("specchia")
        (self.mem / "nota-forgia.md").unlink()
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 1)
        self.assertTrue(any(r["file"] == "nota-forgia.md" for r in json.loads(out)["non_archiviate"]))


class TestArchivia(Base):
    def test_archivia_poi_verifica_passa(self):
        self.scrivi_riservati()
        self.gira("specchia")
        riga = "- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano."
        self.togli(riga)
        codice, out, _ = self.gira("archivia", "--thread", "Prova del custode")
        self.assertEqual(codice, 0, out)
        f = self.coda / (mc.nome_file("Prova del custode") + ".md")
        voci, errori = mc.leggi_coda(f.read_text(encoding="utf-8"))
        self.assertEqual(errori, [])
        self.assertEqual(voci[0]["campi"]["Origine"], "riga tolta dalla memoria del progetto")
        self.assertIn(riga.lstrip("- "), f.read_text(encoding="utf-8"))
        self.assertEqual(self.gira("verifica")[0], 0)

    def test_titolo_predefinito(self):
        self.scrivi_riservati()
        self.gira("specchia")
        self.togli("- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.")
        self.gira("archivia")
        self.assertTrue((self.coda / "memoria-del-progetto-righe-tolte.md").is_file())

    def test_archivia_rifiuta_riga_con_termine_riservato_o_email(self):
        self.spe.mkdir()
        (self.spe / "RISERVATI.txt").write_text("Gianlupo\n", encoding="utf-8")
        (self.mem / "MEMORY.md").write_text(
            MEMORY + "- Il tavolo del giovedi lo ospita Gianlupo in cantina con le lanterne.\n"
            "- Scrivere a qualcuno@esempio.it per le copie stampate della campagna.\n",
            encoding="utf-8")
        self.gira("specchia")
        self.togli("- Il tavolo del giovedi lo ospita Gianlupo in cantina con le lanterne.")
        self.togli("- Scrivere a qualcuno@esempio.it per le copie stampate della campagna.")
        codice, out, _ = self.gira("archivia")
        self.assertEqual(codice, 0)
        self.assertIn("specchio", out)
        coda = "".join(p.read_text(encoding="utf-8") for p in self.coda.glob("*.md"))
        self.assertNotIn("Gianlupo", coda)
        self.assertNotIn("@esempio.it", coda)
        self.assertEqual(self.gira("verifica")[0], 0)


class TestRedigi(Base):
    def test_sostituisce_la_riga_riservata(self):
        self.spe.mkdir()
        (self.spe / "RISERVATI.txt").write_text("fabbro anziano\n", encoding="utf-8")
        uscita = Path(self.t.name) / "redatta"
        codice, _, _ = self.gira("redigi", "--uscita", str(uscita))
        self.assertEqual(codice, 0)
        testo = (uscita / "MEMORY.md").read_text(encoding="utf-8")
        self.assertNotIn("fabbro", testo)
        self.assertRegex(testo, r"\[riga riservata · sha256:[0-9a-f]{8}\]")
        self.assertIn("La stampa del volume", testo)
        self.assertIn("non si modifica a mano", (uscita / "LEGGIMI.md").read_text(encoding="utf-8"))

    def test_rifiuta_senza_riservati(self):
        uscita = Path(self.t.name) / "redatta"
        codice, _, err = self.gira("redigi", "--uscita", str(uscita))
        self.assertEqual(codice, 1)
        self.assertIn("RISERVATI.txt", err)
        self.assertFalse(uscita.exists())


class TestHook(Base):
    def test_merge_su_altro_repo_esce_0(self):
        self.gira("specchia")
        self.togli("- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.")
        ev = {"tool_name": "mcp__github__merge_pull_request",
              "tool_input": {"owner": "altri", "repo": "RumblingStone", "pullNumber": 1}}
        self.assertEqual(self.gira("--hook-merge", stdin=json.dumps(ev))[0], 0)

    def test_merge_senza_memoria_esce_0(self):
        ev = {"tool_input": {"owner": "gsamuele78", "repo": "RumblingStone"}}
        (self.mem / "MEMORY.md").unlink()
        (self.mem / "nota-forgia.md").unlink()
        self.mem.rmdir()
        codice, _, err = self.gira("--hook-merge", stdin=json.dumps(ev))
        self.assertEqual(codice, 0)
        self.assertIn("assente", err)

    def test_scrittura_fuori_memoria_esce_0_senza_leggere(self):
        ev = {"tool_name": "Write", "tool_input": {"file_path": str(self.rad / "x.md"), "content": ""}}
        with mock.patch.object(cu, "leggi_memoria", side_effect=AssertionError("letta")), \
                mock.patch.object(cu, "ultima_istantanea", side_effect=AssertionError("letta")):
            codice, out, _ = self.gira("--hook-scrittura", stdin=json.dumps(ev))
        self.assertEqual((codice, out), (0, ""))

    def test_scrittura_dentro_avvisa_senza_bloccare(self):
        f = self.mem / "MEMORY.md"
        nuovo = f.read_text(encoding="utf-8").replace(
            "- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.\n", "")
        ev = {"tool_name": "Write", "tool_input": {"file_path": str(f), "content": nuovo}}
        codice, out, _ = self.gira("--hook-scrittura", stdin=json.dumps(ev))
        self.assertEqual(codice, 0)
        ctx = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(ctx["hookEventName"], "PreToolUse")
        self.assertIn("fabbro", ctx["additionalContext"])
        self.assertIn("memoria_custode.py archivia", ctx["additionalContext"])
        registro = self.rad / ".claude" / ".custode-memoria.jsonl"
        riga = json.loads(registro.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(riga["esito"], "avvisa")
        self.assertIn("durata_ms", riga)

    def test_edit_e_multiedit_calcolano_il_contenuto_nuovo(self):
        f = self.mem / "nota-forgia.md"
        vecchia = "La forgia sommersa ha tre chiavi d'ottone nascoste nella cisterna."
        ev = {"tool_name": "Edit", "tool_input": {"file_path": str(f), "old_string": vecchia,
                                                 "new_string": "La forgia sommersa."}}
        out = self.gira("--hook-scrittura", stdin=json.dumps(ev))[1]
        self.assertIn("cisterna", out)
        ev = {"tool_name": "MultiEdit", "tool_input": {"file_path": str(f), "edits": [
            {"old_string": "tre chiavi", "new_string": "TRE CHIAVI"},
            {"old_string": "TRE CHIAVI d'ottone nascoste nella cisterna", "new_string": "tre chiavi d'ottone nascoste nella cisterna"}]}}
        self.assertEqual(self.gira("--hook-scrittura", stdin=json.dumps(ev))[1], "")

    def test_edit_con_replace_all(self):
        self.assertEqual(cu.applica_edit("a b a", "a", "c", True), "c b c")
        self.assertEqual(cu.applica_edit("a b a", "a", "c", False), "c b a")

    def test_riepilogo(self):
        self.gira("specchia")
        self.togli("- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano.")
        ev = {"tool_input": {"owner": "gsamuele78", "repo": "RumblingStone"}}
        self.gira("--hook-merge", stdin=json.dumps(ev))
        codice, out, _ = self.gira("--riepilogo", "--json")
        r = json.loads(out)
        self.assertEqual((r["merge_visti"], r["blocchi"]), (1, 1))
        self.assertIn("p95_ms", r)


class TestTetto(Base):
    def test_sopra_12_kb_solo_avviso(self):
        (self.mem / "MEMORY.md").write_text(MEMORY + ("x" * 100 + "\n") * 130, encoding="utf-8")
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0)
        self.assertTrue(any("tetto" in a for a in json.loads(out)["avvisi"]))

    def test_sopra_16_kb_fallisce(self):
        (self.mem / "MEMORY.md").write_text(MEMORY + ("x" * 100 + "\n") * 170, encoding="utf-8")
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 1)
        self.assertTrue(json.loads(out)["sopra_limite"])

    def test_coda_storta_solo_avviso(self):
        (self.coda / "storta.md").write_text("### MS-???? · ieri · senza campi\n", encoding="utf-8")
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0)
        self.assertTrue(any("coda" in a for a in json.loads(out)["avvisi"]))


class TestCerca(Base):
    def test_tre_fonti(self):
        (self.coda / "un-thread.md").write_text(
            "### MS-???? · 2026-11-20 · Il drago e il guado\n\n- **Data:** 2026-11-20\n- **PR:** —\n"
            "- **ADR:** —\n- **Temi:** drago\n- **Origine:** card\n"
            "- **Testo:** Il drago verde non attraversa il guado prima della terza notte di luna.\n",
            encoding="utf-8")
        codice, out, _ = self.gira("cerca", "drago", "--json")
        self.assertEqual(codice, 0)
        fonti = {r["fonte"] for r in json.loads(out)["risultati"]}
        self.assertEqual(fonti, {"memoria", "storica", "coda"})
        mem = [r for r in json.loads(out)["risultati"] if r["fonte"] == "memoria"][0]
        self.assertEqual((mem["file"], mem["riga"]), ("MEMORY.md", 3))

    def test_dice_dove_non_ha_trovato(self):
        codice, out, _ = self.gira("cerca", "cisterna")
        self.assertEqual(codice, 0)
        self.assertIn("nessun risultato", out)


class TestRiservatiFallisceChiuso(Base):
    """Senza un RISERVATI.txt leggibile e non vuoto, archivia non copia niente in coda."""

    RIGA = "- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano."

    def prepara(self):
        self.gira("specchia")
        self.togli(self.RIGA)

    def coda_intatta(self):
        self.assertEqual(sorted(p.name for p in self.coda.iterdir()), [])

    def test_archivia_senza_riservati_esce_1_e_non_tocca_la_coda(self):
        self.prepara()
        codice, out, err = self.gira("archivia")
        self.assertEqual(codice, 1, out + err)
        self.assertIn("RISERVATI.txt", err)
        self.coda_intatta()

    def test_archivia_con_riservati_vuoto_o_solo_commenti_esce_1(self):
        self.scrivi_riservati("# solo un commento\n\n   \n")
        self.prepara()
        codice, _, err = self.gira("archivia")
        self.assertEqual(codice, 1)
        self.assertIn("vuoto", err)
        self.coda_intatta()

    def test_archivia_con_riservati_illeggibile_esce_1(self):
        (self.spe / "RISERVATI.txt").mkdir(parents=True)     # una cartella: read_text fallisce
        self.prepara()
        codice, _, err = self.gira("archivia", "--json")
        self.assertEqual(codice, 1)
        self.assertIn("non si legge", err)
        self.coda_intatta()

    def test_verifica_senza_riservati_avvisa_senza_cambiare_l_uscita(self):
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0)
        self.assertTrue(any("RISERVATI.txt" in a for a in json.loads(out)["avvisi"]))
        self.scrivi_riservati()
        codice, out, _ = self.gira("verifica", "--json")
        self.assertFalse(any("RISERVATI.txt" in a for a in json.loads(out)["avvisi"]))

    def test_hook_merge_senza_riservati_dice_di_crearlo_e_non_suggerisce_archivia(self):
        self.prepara()
        ev = {"tool_name": "mcp__github__merge_pull_request",
              "tool_input": {"owner": "gsamuele78", "repo": "RumblingStone", "pullNumber": 9}}
        codice, _, err = self.gira("--hook-merge", stdin=json.dumps(ev))
        self.assertEqual(codice, 2)
        self.assertIn("RISERVATI.txt", err)
        self.assertIn("crea", err.lower())
        self.assertNotIn("memoria_custode.py archivia", err)


class TestHookMergeDaBash(Base):
    RIGA = "- Lavoro aperto: correggere la forgia sommersa entro venerdi con il fabbro anziano."

    def setUp(self):
        super().setUp()
        self.scrivi_riservati()
        self.gira("specchia")
        self.togli(self.RIGA)
        self.fuori = Path(self.t.name) / "altrove"
        self.fuori.mkdir()

    def bash(self, comando: str, cwd: "Path | None" = None) -> "tuple[int, str]":
        ev = {"tool_name": "Bash", "tool_input": {"command": comando},
              "cwd": str(cwd if cwd is not None else self.rad)}
        codice, _, err = self.gira("--hook-merge", stdin=json.dumps(ev))
        return codice, err

    def test_gh_pr_merge_nella_cartella_del_repo_verifica(self):
        codice, err = self.bash("gh pr merge 12 --squash")
        self.assertEqual(codice, 2, err)
        self.assertIn("ADR-0151", err)
        registro = self.rad / ".claude" / ".custode-memoria.jsonl"
        riga = json.loads(registro.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual((riga["esito"], riga["pr"], riga["via"]), ("blocca", "12", "bash"))

    def test_gh_pr_merge_senza_numero_nel_repo(self):
        self.assertEqual(self.bash("gh pr merge --merge --delete-branch")[0], 2)

    def test_gh_pr_merge_con_repo_esplicito_da_fuori(self):
        for c in ("gh pr merge 3 -R gsamuele78/RumblingStone",
                  "gh pr merge 3 --repo=GSamuele78/rumblingstone",
                  "gh pr merge 3 --repo github.com/gsamuele78/RumblingStone",
                  "GH_REPO=gsamuele78/RumblingStone gh pr merge 3",
                  "gh pr merge https://github.com/gsamuele78/RumblingStone/pull/3",
                  f"cd {self.rad} && gh pr merge 3",
                  "bash -c 'gh pr merge 3 -R gsamuele78/RumblingStone'"):
            with self.subTest(c=c):
                self.assertEqual(self.bash(c, cwd=self.fuori)[0], 2)

    def test_gh_api_merge_con_put(self):
        for c in ("gh api -X PUT repos/gsamuele78/RumblingStone/pulls/7/merge",
                  "gh api --method put /repos/gsamuele78/rumblingstone/pulls/7/merge -f merge_method=squash"):
            with self.subTest(c=c):
                self.assertEqual(self.bash(c, cwd=self.fuori)[0], 2)

    def test_gh_api_in_lettura_non_e_un_merge(self):
        # GET su /merge dice solo se la PR è unita (204/404).
        self.assertEqual(self.bash("gh api repos/gsamuele78/RumblingStone/pulls/7/merge")[0], 0)

    def test_altri_repo_escono_0(self):
        for c in ("gh pr merge 5 -R altri/RumblingStone",
                  "gh pr merge https://github.com/altri/RumblingStone/pull/5",
                  "gh api -X PUT repos/altri/RumblingStone/pulls/5/merge"):
            with self.subTest(c=c):
                self.assertEqual(self.bash(c)[0], 0)

    def test_senza_repo_fuori_dal_repo_esce_0(self):
        self.assertEqual(self.bash("gh pr merge 5", cwd=self.fuori)[0], 0)

    def test_senza_repo_in_un_clone_del_repo_verifica(self):
        import subprocess
        clone = Path(self.t.name) / "clone"
        clone.mkdir()
        subprocess.run(["git", "init", "-q", str(clone)], check=True)
        subprocess.run(["git", "-C", str(clone), "remote", "add", "origin",
                        "https://github.com/gsamuele78/RumblingStone.git"], check=True)
        self.assertEqual(self.bash("gh pr merge 5", cwd=clone)[0], 2)

    def test_comandi_che_non_uniscono_escono_0_senza_leggere_la_memoria(self):
        for c in ("git status", "gh pr view 12", "gh pr list", "echo 'gh pr merge 3'",
                  "grep -r 'gh pr merge' scripts", "ls"):
            with self.subTest(c=c), \
                    mock.patch.object(cu, "cartella_memoria", side_effect=AssertionError("letta")), \
                    mock.patch.object(cu, "verifica", side_effect=AssertionError("letta")):
                self.assertEqual(self.bash(c)[0], 0)
        self.assertFalse((self.rad / ".claude" / ".custode-memoria.jsonl").exists())

    def test_riconosce_merge_puro(self):
        self.assertEqual(cu.merge_da_bash("git status", None, self.rad), None)
        self.assertEqual(cu.merge_da_bash("gh pr merge 12", str(self.rad), self.rad), "12")
        self.assertEqual(cu.merge_da_bash("gh pr merge", str(self.rad), self.rad), "")


NOTA_LINK = """---
name: nota-forgia
description: La forgia sommersa e le sue chiavi
---
La forgia sommersa ha tre chiavi d'ottone nascoste nella cisterna.
Vedi [[nota-chiavi]] e [[da-scrivere]]; il simbolo `[[link]]` in codice non conta.
"""


def _nota(nome: str, descr: str, corpo: str) -> str:
    return f"---\nname: {nome}\ndescription: {descr}\n---\n{corpo}\n"


class TestLink(Base):
    def setUp(self):
        super().setUp()
        (self.mem / "nota-forgia.md").write_text(NOTA_LINK, encoding="utf-8")
        (self.mem / "nota-chiavi.md").write_text(
            _nota("nota-chiavi", "Le chiavi d'ottone", "Le chiavi aprono la porta. Vedi [[nota-porta]]."),
            encoding="utf-8")
        (self.mem / "nota-porta.md").write_text(
            _nota("nota-porta", "La porta del molo", "La porta del molo resta chiusa."), encoding="utf-8")
        (self.mem / "nota-molo.md").write_text(
            _nota("nota-molo", "Il molo vecchio", "Dal molo si scende alla [[nota-forgia]]."),
            encoding="utf-8")
        (self.mem / "MEMORY.md").write_text(MEMORY + "- Forgia sommersa: [[nota-forgia]]\n",
                                             encoding="utf-8")

    def link(self, out: str) -> "list[dict]":
        return [r for r in json.loads(out)["risultati"] if r["fonte"] == "memoria-link"]

    def test_cerca_aggiunge_le_note_a_un_passo_in_uscita_e_in_entrata(self):
        codice, out, _ = self.gira("cerca", "cisterna", "--json")
        self.assertEqual(codice, 0)
        visti = {(r["file"], r["verso"], r["da"]) for r in self.link(out)}
        self.assertEqual(visti, {("nota-chiavi.md", "uscita", "nota-forgia.md"),
                                 ("nota-molo.md", "entrata", "nota-forgia.md")})
        chiavi = [r for r in self.link(out) if r["file"] == "nota-chiavi.md"][0]
        self.assertEqual(chiavi["testo"], "Le chiavi d'ottone")

    def test_senza_link(self):
        out = self.gira("cerca", "cisterna", "--senza-link", "--json")[1]
        self.assertEqual(self.link(out), [])

    def test_riga_dell_indice_porta_solo_i_suoi_link(self):
        out = self.gira("cerca", "Forgia sommersa:", "--json")[1]
        self.assertEqual([(r["file"], r["da"]) for r in self.link(out)],
                         [("nota-forgia.md", "MEMORY.md")])

    def test_nota_gia_trovata_non_si_ripete(self):
        out = self.gira("cerca", "chiavi", "--json")[1]
        trovati = {r["file"] for r in json.loads(out)["risultati"] if r["fonte"] == "memoria"}
        self.assertFalse(trovati & {r["file"] for r in self.link(out)})

    def test_stampa_testuale(self):
        out = self.gira("cerca", "cisterna")[1]
        self.assertIn("[memoria-link]", out)

    def test_verifica_avvisa_dei_link_rotti_senza_cambiare_l_uscita(self):
        codice, out, _ = self.gira("verifica", "--json")
        self.assertEqual(codice, 0)
        v = json.loads(out)
        self.assertEqual(v["link"]["totali"], 5)
        self.assertEqual(v["link"]["rotti"], [{"file": "nota-forgia.md", "nome": "da-scrivere"}])
        self.assertTrue(any("1 link" in a and "da-scrivere" in a for a in v["avvisi"]))

    def test_nome_dal_frontmatter(self):
        (self.mem / "altro-file.md").write_text(_nota("nome-vero", "x", "corpo"), encoding="utf-8")
        (self.mem / "cita.md").write_text(_nota("cita", "y", "[[nome-vero]] [[altro-file]]"),
                                          encoding="utf-8")
        rotti = cu.link_memoria(cu.leggi_memoria(self.mem))["rotti"]
        self.assertNotIn({"file": "cita.md", "nome": "nome-vero"}, rotti)
        self.assertIn({"file": "cita.md", "nome": "altro-file"}, rotti)


if __name__ == "__main__":
    unittest.main()
