"""Gli occhi sul giocato: il ramo di gruppo, main e le patch ferme (sincronia_giocato.py).

Tutto su repository git costruiti in una cartella temporanea: un origin nudo,
main, un ramo di gruppo vivo, uno morto, uno non registrato, e le quattro patch
tipiche (applicata, da applicare, in conflitto, fuori canone). Niente /mnt,
niente rete.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sincronia_giocato as sg  # noqa: E402

ORA = "2026-03-01T00:00:00Z"
T_ORA = int(datetime(2026, 3, 1, tzinfo=timezone.utc).timestamp())
GIORNO = 86400


def _git(repo: Path, *args: str, quando: "int | None" = None) -> str:
    env = dict(os.environ)
    if quando is not None:
        data = f"@{quando} +0000"
        env.update(GIT_AUTHOR_DATE=data, GIT_COMMITTER_DATE=data)
    out = subprocess.run(["git", "-C", str(repo), *args], check=True,
                         capture_output=True, text=True, env=env)
    return out.stdout


def _scrivi(repo: Path, rel: str, testo: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(testo, encoding="utf-8")


def _commit(repo: Path, msg: str, quando: int) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", msg, quando=quando)


def _patch(repo: Path, dest: Path, nome: str, eta_ore: float) -> Path:
    """L'ultimo commit di HEAD come mbox di format-patch, con l'età voluta."""
    testo = _git(repo, "format-patch", "-1", "--stdout", "HEAD")
    f = dest / nome
    f.write_text(testo, encoding="utf-8")
    t = T_ORA - int(eta_ore * 3600)
    os.utime(f, (t, t))
    return f


class Mondo:
    """origin nudo + clone completo, con il registro dei rami e le patch."""

    def __init__(self, radice: Path) -> None:
        self.radice = radice
        lavoro = radice / "lavoro"
        lavoro.mkdir()
        _git(lavoro, "init", "-q", "-b", "main")
        _git(lavoro, "config", "user.email", "t@t")
        _git(lavoro, "config", "user.name", "t")
        _scrivi(lavoro, "README.md", "prodotto\n")
        _scrivi(lavoro, "campaign/state.yaml", "a: 1\nb: 1\n")
        _commit(lavoro, "init", T_ORA - 90 * GIORNO)

        _git(lavoro, "checkout", "-qb", "campaign-group-x")
        _scrivi(lavoro, "campaign/sessions/2026-01-10_session-1.md",
                "# Sessione 1\n\nPX: ______\n[INFERRED — needs DM confirmation]\n")
        _scrivi(lavoro, "campaign/state.yaml", "a: 2\nb: 1\nc: da compilare\n")
        _commit(lavoro, "sessione 1", T_ORA - 50 * GIORNO)
        self.patch = radice / "patch"
        self.patch.mkdir()
        self.applicata = _patch(lavoro, self.patch, "0001-sessione-1.patch", 24 * 40)

        # una serata nuova preparata da un thread e mai portata sul ramo
        _git(lavoro, "checkout", "-qb", "thread")
        _scrivi(lavoro, "campaign/sessions/2026-02-20_session-2.md", "# Sessione 2\n")
        _commit(lavoro, "sessione 2", T_ORA - 3 * GIORNO)
        self.da_applicare = _patch(lavoro, self.patch, "0001-sessione-2.patch", 72)

        # una patch scritta contro main: tocca la riga che il ramo ha cambiato
        _git(lavoro, "checkout", "-q", "main")
        _git(lavoro, "checkout", "-qb", "vecchia")
        _scrivi(lavoro, "campaign/state.yaml", "a: 9\nb: 1\n")
        _commit(lavoro, "a 9", T_ORA - 2 * GIORNO)
        sub = self.patch / "thread-vecchio" / "out"
        sub.mkdir(parents=True)
        self.conflitto = _patch(lavoro, sub, "0001-a9.patch", 5)

        # una patch di prodotto: fuori canone, si conta e si ignora
        _git(lavoro, "checkout", "-q", "main")
        _git(lavoro, "checkout", "-qb", "prodotto")
        _scrivi(lavoro, "README.md", "prodotto 2\n")
        _commit(lavoro, "readme", T_ORA - GIORNO)
        self.fuori = _patch(lavoro, self.patch, "0001-readme.patch", 100)

        # una patch già portata sul ramo in un'altra forma: stesso oggetto, testo diverso
        _git(lavoro, "checkout", "-q", "campaign-group-x")
        _scrivi(lavoro, "campaign/state-changelog.md", "storia del ramo\n")
        _commit(lavoro, "Storico: la serata del 10 gennaio", T_ORA - 40 * GIORNO)
        _git(lavoro, "checkout", "-q", "main")
        _git(lavoro, "checkout", "-qb", "riscritta")
        _scrivi(lavoro, "campaign/state-changelog.md", "storia della patch\n")
        _commit(lavoro, "Storico: la serata del 10 gennaio", T_ORA - 45 * GIORNO)
        self.riscritta = _patch(lavoro, self.patch, "0002-storico.patch", 24 * 30)

        # portata sul ramo e poi rinominata (la sessione 5 del 20/11 diventata 7): il file della
        # patch non c'è più, ma è cambiato dopo il commit con lo stesso oggetto → altra forma
        _git(lavoro, "checkout", "-q", "campaign-group-x")
        _scrivi(lavoro, "campaign/recaps/recap.md", "recap del ramo\n")
        _commit(lavoro, "Recap della serata del 10 gennaio", T_ORA - 39 * GIORNO)
        _git(lavoro, "mv", "campaign/recaps/recap.md", "campaign/recaps/recap-rinominato.md")
        _commit(lavoro, "Recap rinominato", T_ORA - 38 * GIORNO)
        _git(lavoro, "checkout", "-q", "main")
        _git(lavoro, "checkout", "-qb", "rinominata")
        _scrivi(lavoro, "campaign/recaps/recap.md", "recap\n")
        _commit(lavoro, "Recap della serata del 10 gennaio", T_ORA - 41 * GIORNO)
        self.rinominata = _patch(lavoro, self.patch, "0003-recap.patch", 24 * 30)

        # stessa modifica (stesso patch-id) e poi il file è andato avanti: applicata
        _git(lavoro, "checkout", "-q", "campaign-group-x")
        _scrivi(lavoro, "campaign/recaps/pg/hella.md", "uno\n")
        _commit(lavoro, "Recap di Hella", T_ORA - 37 * GIORNO)
        _patch(lavoro, self.patch, "0004-hella.patch", 24 * 30)
        _scrivi(lavoro, "campaign/recaps/pg/hella.md", "due\n")
        _commit(lavoro, "Recap di Hella, ritocco", T_ORA - 36 * GIORNO)

        # un thread chiude un campo aperto senza una decisione datata del DM
        _git(lavoro, "checkout", "-qb", "chiude")
        testo = (lavoro / "campaign/sessions/2026-01-10_session-1.md").read_text(encoding="utf-8")
        _scrivi(lavoro, "campaign/sessions/2026-01-10_session-1.md",
                testo.replace("PX: ______", "PX: 500"))
        _commit(lavoro, "Sessione 1: i PX", T_ORA - GIORNO)
        self.chiude = _patch(lavoro, self.patch, "0005-px.patch", 10)

        # main va avanti dopo la nascita del ramo: due commit, il più vecchio di 30 giorni
        _git(lavoro, "checkout", "-q", "main")
        _scrivi(lavoro, "scripts/uno.py", "x = 1\n")
        _commit(lavoro, "uno", T_ORA - 30 * GIORNO)
        _scrivi(lavoro, "scripts/due.py", "x = 2\n")
        _commit(lavoro, "due", T_ORA - 10 * GIORNO)

        _git(lavoro, "branch", "campaign-group-morto", "campaign-group-x")
        _git(lavoro, "branch", "campaign-group-ignoto", "campaign-group-x")

        self.origin = radice / "origin.git"
        _git(radice, "init", "-q", "--bare", str(self.origin))
        _git(lavoro, "push", "-q", str(self.origin), "main", "campaign-group-x",
             "campaign-group-morto", "campaign-group-ignoto")
        self.lavoro = lavoro

        self.clone = radice / "clone"
        _git(radice, "clone", "-q", str(self.origin), str(self.clone))
        _git(self.clone, "config", "user.email", "t@t")
        _git(self.clone, "config", "user.name", "t")

        self.registro = radice / "rami-di-gruppo.json"
        self.registro.write_text(json.dumps({
            "vivi": [{"ramo": "campaign-group-x", "gruppo": "x"}],
            "morti": [{"ramo": "campaign-group-morto", "dal": "2026-01-01",
                       "motivo": "storia non comune con main (ADR-0090)"}],
        }), encoding="utf-8")

    def misura(self, repo: "Path | None" = None, **kw) -> dict:
        kw.setdefault("scansiona", [self.patch])
        return sg.misura(repo or self.clone, registro=self.registro, ora=ORA, **kw)


def _codici(esito: dict) -> "list[tuple[str, str]]":
    return [(r["codice"], r["livello"]) for r in esito["rilievi"]]


class TestSincronia(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.m = Mondo(Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_s1_ramo_non_registrato_giallo_il_morto_si_ignora(self) -> None:
        e = self.m.misura()
        s1 = [r for r in e["rilievi"] if r["codice"] == "S1"]
        self.assertEqual([r["ramo"] for r in s1], ["campaign-group-ignoto"])
        self.assertEqual(s1[0]["livello"], sg.GIALLO)
        self.assertTrue(s1[0]["comando"])
        self.assertFalse([r for r in e["rilievi"] if r["ramo"] == "campaign-group-morto"])

    def test_s2_main_indietro_oltre_soglia_rosso(self) -> None:
        e = self.m.misura()
        s2 = [r for r in e["rilievi"] if r["codice"] == "S2"][0]
        self.assertEqual(s2["livello"], sg.ROSSO)
        self.assertEqual(s2["dati"]["commit"], 2)
        self.assertEqual(s2["dati"]["giorni"], 30)
        self.assertIn("git merge", s2["comando"])

    def test_s2_sotto_soglia_giallo(self) -> None:
        e = self.m.misura(giorni_rosso=60)
        s2 = [r for r in e["rilievi"] if r["codice"] == "S2"][0]
        self.assertEqual(s2["livello"], sg.GIALLO)

    def test_s3_le_quattro_patch(self) -> None:
        e = self.m.misura()
        stati = {Path(p["file"]).name: p["stato"] for p in e["misure"]["patch"]}
        self.assertEqual(stati, {"0001-sessione-1.patch": "applicata",
                                 "0001-sessione-2.patch": "da applicare",
                                 "0001-a9.patch": "in conflitto",
                                 "0002-storico.patch": "da verificare",
                                 "0003-recap.patch": "applicata in altra forma",
                                 "0004-hella.patch": "applicata",
                                 "0005-px.patch": "da applicare"})
        self.assertEqual(e["misure"]["patch_fuori_canone"], 1)
        s3 = {Path(r["dati"]["file"]).name: r["livello"]
              for r in e["rilievi"] if r["codice"] == "S3"}
        # da applicare e più vecchia di 48 ore → rosso; il conflitto e il dubbio sono gialli
        self.assertEqual(s3, {"0001-sessione-2.patch": sg.ROSSO, "0001-a9.patch": sg.GIALLO,
                              "0002-storico.patch": sg.GIALLO, "0005-px.patch": sg.GIALLO})
        dubbio = [r for r in e["rilievi"] if r["codice"] == "S3"
                  and r["dati"]["file"].endswith("0002-storico.patch")][0]
        self.assertEqual(dubbio["dati"]["righe_mancanti"], 1)
        self.assertIn("DM", dubbio["comando"])

    def test_s6_patch_che_chiude_campi_senza_decisione(self) -> None:
        e = self.m.misura()
        s6 = [r for r in e["rilievi"] if r["codice"] == "S6"]
        self.assertEqual([Path(r["dati"]["file"]).name for r in s6], ["0005-px.patch"])
        self.assertEqual(s6[0]["livello"], sg.GIALLO)
        self.assertEqual(s6[0]["dati"]["senza_decisione"], 1)

    def test_s3_patch_giovane_e_gialla(self) -> None:
        e = self.m.misura(ore_patch=1000)
        s3 = {Path(r["dati"]["file"]).name: r["livello"]
              for r in e["rilievi"] if r["codice"] == "S3"}
        self.assertEqual(s3["0001-sessione-2.patch"], sg.GIALLO)

    def test_s3_non_tocca_l_albero_ne_l_indice(self) -> None:
        prima = _git(self.m.clone, "status", "--porcelain")
        self.m.misura()
        self.assertEqual(_git(self.m.clone, "status", "--porcelain"), prima)

    def test_i_percorsi_del_canone_vengono_da_partita(self) -> None:
        self.assertTrue(sg.e_canone("campaign/state.yaml"))
        self.assertTrue(sg.e_canone("campaign/sessions/2026-01-10_session-1.md"))
        self.assertTrue(sg.e_canone("campaign/next/brief-2026-01-01-DM.md"))
        self.assertTrue(sg.e_canone("campaign/group.yaml"))
        self.assertFalse(sg.e_canone("README.md"))
        self.assertFalse(sg.e_canone("campaign/DM-CAMPAIGN-PLAYBOOK.md"))

    def test_s4_campi_aperti_mai_rossi(self) -> None:
        e = self.m.misura()
        s4 = [r for r in e["rilievi"] if r["codice"] == "S4"]
        self.assertEqual(len(s4), 1)
        self.assertEqual(s4[0]["livello"], sg.GIALLO)
        self.assertEqual(s4[0]["dati"]["totale"], 3)

    def test_s5_serata_piu_recente_dell_ultima_registrata(self) -> None:
        e = self.m.misura()
        self.assertEqual(e["misure"]["rami"]["campaign-group-x"]["ultima_sessione"], "2026-01-10")
        s5 = [r for r in e["rilievi"] if r["codice"] == "S5"]
        self.assertEqual(len(s5), 1)
        self.assertEqual(s5[0]["livello"], sg.ROSSO)
        self.assertIn("2026-02-20", s5[0]["messaggio"])

    def test_senza_patch_s5_e_s3_tacciono(self) -> None:
        e = self.m.misura(scansiona=[])
        self.assertFalse([r for r in e["rilievi"] if r["codice"] in ("S3", "S5")])

    def test_check_esce_1_con_un_rosso_e_json(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = sg.main(["--repo", str(self.m.clone), "--registro", str(self.m.registro),
                          "--ora", ORA, "--scansiona", str(self.m.patch), "--check", "--json"])
        self.assertEqual(rc, 1)
        d = json.loads(out.getvalue())
        self.assertEqual(d["esito"], 1)
        self.assertIn("S2", {r["codice"] for r in d["rilievi"]})

    def test_verde_esce_0_e_l_avviso_tace(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            c = Path(t) / "c"
            _git(Path(t), "clone", "-q", str(self.m.origin), str(c))
            _git(c, "config", "user.email", "t@t")
            _git(c, "config", "user.name", "t")
            _git(c, "checkout", "-q", "campaign-group-x")
            _git(c, "merge", "-q", "--no-edit", "origin/main", quando=T_ORA)
            _git(c, "push", "-q", "origin", "campaign-group-x:campaign-group-verde")
            reg = Path(t) / "reg.json"
            reg.write_text(json.dumps({"vivi": [{"ramo": "campaign-group-verde", "gruppo": "x"}],
                                       "morti": [{"ramo": n, "dal": "2026-01-01", "motivo": "test"}
                                                 for n in ("campaign-group-x", "campaign-group-morto",
                                                           "campaign-group-ignoto")]}),
                           encoding="utf-8")
            _git(c, "fetch", "-q", "origin")
            e = sg.misura(c, registro=reg, ora=ORA, scansiona=[], campi_aperti=False)
            self.assertEqual(e["esito"], 0, e["rilievi"])
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = sg.main(["--repo", str(c), "--registro", str(reg), "--ora", ORA,
                              "--avviso", "--senza-campi-aperti"])
            self.assertEqual((rc, out.getvalue()), (0, ""))
            _git(Path(t), "--git-dir", str(self.m.origin), "branch", "-D", "campaign-group-verde")

    def test_avviso_breve_ed_esce_sempre_0(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = sg.main(["--repo", str(self.m.clone), "--registro", str(self.m.registro),
                          "--ora", ORA, "--scansiona", str(self.m.patch), "--avviso"])
        self.assertEqual(rc, 0)
        righe = out.getvalue().strip().splitlines()
        self.assertTrue(righe)
        self.assertLessEqual(len(righe), sg.RIGHE_AVVISO + 1)
        self.assertIn("🔴", out.getvalue())

    def test_avviso_su_un_repo_rotto_esce_0(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(sg.main(["--repo", t, "--avviso"]), 0)

    def test_clone_shallow_non_misurabile(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            c = Path(t) / "s"
            _git(Path(t), "clone", "-q", "--depth", "1", "--no-single-branch",
                 f"file://{self.m.origin}", str(c))
            e = self.m.misura(repo=c, scansiona=[])
            s2 = [r for r in e["rilievi"] if r["codice"] == "S2"][0]
            self.assertEqual(s2["livello"], sg.NON_MISURABILE)
            self.assertIn("git fetch --unshallow", s2["comando"])
            self.assertEqual(e["esito"], 2)

    def test_ramo_vivo_assente_non_misurabile(self) -> None:
        reg = self.m.radice / "reg-assente.json"
        reg.write_text(json.dumps({"vivi": [{"ramo": "campaign-group-nessuno", "gruppo": "n"}],
                                   "morti": []}), encoding="utf-8")
        e = sg.misura(self.m.clone, registro=reg, ora=ORA, scansiona=[])
        self.assertIn(("S2", sg.NON_MISURABILE), _codici(e))
        self.assertEqual(e["esito"], 2)

    def test_ref_locale_che_chiude_campi_senza_decisione_e_rosso(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            c = Path(t) / "c"
            _git(Path(t), "clone", "-q", "-b", "campaign-group-x", str(self.m.origin), str(c))
            _git(c, "config", "user.email", "t@t")
            _git(c, "config", "user.name", "t")
            f = c / "campaign/sessions/2026-01-10_session-1.md"
            f.write_text(f.read_text(encoding="utf-8").replace("PX: ______", "PX: 500"), encoding="utf-8")
            _commit(c, "px", T_ORA)
            e = self.m.misura(repo=c, scansiona=[], ref="HEAD")
            s6 = [r for r in e["rilievi"] if r["codice"] == "S6"]
            self.assertEqual([r["livello"] for r in s6], [sg.ROSSO])
            self.assertEqual(e["misure"]["rami"]["campaign-group-x"]["campi_aperti"], 2)
            f.write_text(f.read_text(encoding="utf-8").replace("PX: 500", "PX: 500 (DM, 2026-03-01)"),
                         encoding="utf-8")
            _commit(c, "px con la decisione", T_ORA)
            e = self.m.misura(repo=c, scansiona=[], ref="HEAD")
            self.assertFalse([r for r in e["rilievi"] if r["codice"] == "S6"])

    def test_dopo_merge_le_righe_di_main_perse_sono_rosse(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            c = Path(t) / "c"
            _git(Path(t), "clone", "-q", "-b", "main", str(self.m.origin), str(c))
            _git(c, "config", "user.email", "t@t")
            _git(c, "config", "user.name", "t")
            # su main una correzione di canone approvata (come Tempestas GS 15)
            _scrivi(c, "campaign/state.yaml", "a: 1\nb: 1\npng:\n  tempestas: GS 15\n")
            _commit(c, "Tempestas GS 15", T_ORA - GIORNO)
            _git(c, "checkout", "-q", "campaign-group-x")
            _git(c, "merge", "-q", "-s", "ours", "--no-edit", "main", quando=T_ORA)
            e = sg.dopo_merge(c, prima="HEAD^1", main="main")
            self.assertEqual(e["esito"], 1)
            persa = [r for r in e["rilievi"] if r["codice"] == "S7"][0]
            self.assertEqual(persa["livello"], sg.ROSSO)
            self.assertIn("tempestas: GS 15", persa["dati"]["righe"])
            _git(c, "reset", "-q", "--hard", "HEAD^1")
            r = subprocess.run(["git", "-C", str(c), "merge", "--no-edit", "main"],
                               capture_output=True, text=True)
            if r.returncode:  # conflitto: blocco per blocco, il giocato del ramo e il png di main
                _scrivi(c, "campaign/state.yaml",
                        "a: 2\nb: 1\nc: da compilare\npng:\n  tempestas: GS 15\n")
                _commit(c, "merge", T_ORA)
            e = sg.dopo_merge(c, prima="HEAD^1", main="main")
            self.assertEqual(e["esito"], 0, e["rilievi"])

    def test_conta_campi_occorrenze_e_intestazioni(self) -> None:
        casi = {
            "PX: ______ e ______": 2,
            "## Da confermare": 0,
            "Da confermare dal DM: chi c'era": 1,
            "i dadi da tirare": 1,
            "i tiri non ancora tirati": 1,
            "da decidere e da compilare": 2,
            "lo schema è `[INFERRED — <domanda al DM>; base: <su cosa poggia>]`": 0,
            "oggetti marcati `[INFERRED]` nel master": 0,
            "[INFERRED — Quanti PF?; base: MM] da confermare": 2,
            "tutto deciso": 0,
        }
        for testo, atteso in casi.items():
            with self.subTest(testo=testo):
                self.assertEqual(sg.conta_campi(testo), atteso)

    def test_chiusure_con_e_senza_decisione(self) -> None:
        def patch(vecchia: str, nuova: str) -> str:
            return ("diff --git a/campaign/sessions/x.md b/campaign/sessions/x.md\n"
                    "--- a/campaign/sessions/x.md\n+++ b/campaign/sessions/x.md\n"
                    f"@@ -1,2 +1,2 @@\n # Sessione\n-{vecchia}\n" + (f"+{nuova}\n" if nuova else ""))
        self.assertEqual(sg.chiusure(patch("PX: ______", "PX: 500"))["senza_decisione"], 1)
        self.assertEqual(sg.chiusure(patch("PX: ______", "PX: 500 (DM, 2026-11-21)"))["senza_decisione"], 0)
        self.assertEqual(sg.chiusure(patch("PX: ______", "PX: 500 (Jfs, 2026-11-21)"))["chiusi"], 1)
        self.assertEqual(sg.chiusure(patch("PX: ______", ""))["senza_decisione"], 1)
        self.assertEqual(sg.chiusure(patch("PX: 400", "PX: 500"))["chiusi"], 0)

    def test_i_rami_morti_dal_registro(self) -> None:
        self.assertEqual(sg.rami_morti(self.m.registro), {"campaign-group-morto"})
        self.assertIn("campaign-group-rumblingstone-dm-gianfranco", sg.rami_morti())

    def test_il_registro_del_repo_e_in_forma(self) -> None:
        d = sg.carica_registro(sg.REGISTRO)
        vivi = {r["ramo"] for r in d["vivi"]}
        morti = {r["ramo"]: r for r in d["morti"]}
        self.assertIn("campaign-group-rumblingstone", vivi)
        self.assertIn("campaign-group-rumblingstone-dm-gianfranco", morti)
        self.assertIn("ADR-0090", morti["campaign-group-rumblingstone-dm-gianfranco"]["motivo"])
        self.assertFalse(vivi & set(morti))


if __name__ == "__main__":
    unittest.main()
