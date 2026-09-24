"""Il delta di sessione come dato — lotto 4e del piano RIPRESA-PR (§4.9).

Il difetto che questi test chiudono, misurato il 2026-09-24: la regex di
`state_sync` riconosce i villain per nome, coi nomi scritti nel suo sorgente, e
dei tredici di `campaign/state.yaml` vede 3 clock su 9 e 5 morti su 13.
Ghaurush, Zin'thara e Ushgar non li vede affatto.

🔴 **Le prove importanti girano sui FILE VERI** (vincolo di §4.4): la #99 ha
registrato una regressione che la CI non aveva visto perche' i test di
`state_apply` giravano su fixture.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

import render_state  # noqa: E402
import session_recap  # noqa: E402
import state_apply  # noqa: E402
from dmcore import delta_sessione as ds  # noqa: E402

STATE_YAML = ROOT / "campaign" / "state.yaml"


def _dati() -> dict:
    return yaml.safe_load(STATE_YAML.read_text(encoding="utf-8"))


def _numerici(dati: dict) -> "list[tuple[int, str, int, int]]":
    """(indice, png_id, numeratore, fondo) dei villain con un clock numerico."""
    out = []
    for i, r in enumerate(dati["villain"]):
        num, sep, fondo = str(r.get("clock") or "").partition("/")
        if sep and num.strip().isdigit() and fondo.strip().isdigit():
            out.append((i, r["png_id"], int(num), int(fondo)))
    return out


class TestIlFrontMatter(unittest.TestCase):
    def test_un_log_senza_front_matter_non_ha_delta(self):
        self.assertIsNone(ds.estrai("# Session 3 — Test (2026-05-03)\n"))

    def test_un_front_matter_senza_delta_non_ha_delta(self):
        self.assertIsNone(ds.estrai("---\ntitolo: x\n---\n# Session 3\n"))

    def test_un_front_matter_aperto_e_mai_chiuso_e_un_errore(self):
        """Ricadere sulla regex in silenzio e' il difetto che il modulo toglie."""
        with self.assertRaises(ds.DeltaError):
            ds.estrai("---\ndelta:\n  march_clock: {da: 19, a: 20}\n# Session 3\n")

    def test_un_front_matter_illeggibile_e_un_errore(self):
        with self.assertRaises(ds.DeltaError):
            ds.estrai("---\ndelta: [\n---\n# Session 3\n")

    def test_emettere_e_rileggere_torna_uguale(self):
        delta = {"march_clock": {"da": 19, "a": 20},
                 "clock": [{"png_id": "ghaurush", "da": 0, "a": 1}],
                 "stato": [{"png_id": "ushgar", "stato": "morto"}]}
        testo = ds.emetti(delta) + "# Session 4 — Prova (2026-09-24)\n"
        self.assertEqual(ds.estrai(testo), delta)

    def test_un_delta_vuoto_non_emette_niente(self):
        self.assertEqual(ds.emetti({}), "")

    def test_emettere_rifiuta_quello_che_non_rileggerebbe_uguale(self):
        with self.assertRaises(ds.DeltaError):
            ds.emetti({"stato": [{"png_id": "ushgar", "stato": "morto}, x: 1"}]})
        with self.assertRaises(ds.DeltaError):
            ds.emetti({"clock": [{"png_id": "Ghaurush Cenerevento", "da": 0, "a": 1}]})


class TestITrediciSonoRaggiungibili(unittest.TestCase):
    """Sul `state.yaml` vero: ogni villain si nomina per `png_id`."""

    def test_ogni_clock_numerico_si_muove_dal_delta(self):
        dati = _dati()
        numerici = _numerici(dati)
        self.assertGreaterEqual(len(numerici), 9)
        for i, pid, num, fondo in numerici:
            a = num + 1 if num < fondo else num - 1
            with self.subTest(png_id=pid):
                ops = ds.operazioni(
                    {"clock": [{"png_id": pid, "da": num, "a": a}]}, dati)
                self.assertEqual([(o.indice, o.campo, o.valore) for o in ops],
                                 [(i, "clock", f"{a}/{fondo}")])

    def test_ogni_villain_riceve_uno_stato(self):
        dati = _dati()
        for i, r in enumerate(dati["villain"]):
            nuovo = "ignoto" if r.get("stato") != "ignoto" else "attivo"
            with self.subTest(png_id=r["png_id"]):
                ops = ds.operazioni(
                    {"stato": [{"png_id": r["png_id"], "stato": nuovo}]}, dati)
                self.assertEqual([(o.indice, o.valore) for o in ops], [(i, nuovo)])

    def test_i_tre_che_la_regex_non_vede(self):
        """Il caso che la #99 aveva previsto, sui nomi di oggi."""
        from state_sync import TRIGGERS
        rx = dict(TRIGGERS)
        dati = _dati()
        for pid, nome in (("ghaurush", "Ghaurush"), ("zin-thara", "Zin'thara"),
                          ("ushgar", "Ushgar")):
            with self.subTest(png_id=pid):
                self.assertIsNone(rx["npc_killed"].search(f"{nome} killed"))
                ops = ds.operazioni({"stato": [{"png_id": pid, "stato": "morto"}]}, dati)
                self.assertEqual(len(ops), 1)

    def test_il_nome_del_dm_si_risolve_nel_png_id(self):
        dati = _dati()
        self.assertEqual(ds.risolvi_villain(dati, "Ghaurush")[0], "ghaurush")
        self.assertEqual(ds.risolvi_villain(dati, "ghaurush")[0], "ghaurush")
        self.assertEqual(ds.risolvi_villain(dati, "Zin'thara")[0], "zin-thara")

    def test_un_nome_ambiguo_non_sceglie(self):
        """«Zalkatar» sta nell'etichetta di due villain: non se ne sceglie uno."""
        dati = _dati()
        pid, candidati = ds.risolvi_villain(dati, "Zalkatar")
        self.assertEqual(pid, "zalkatar", "il png_id esatto vince sull'etichetta")
        pid, candidati = ds.risolvi_villain(dati, "Illithid")
        self.assertIsNone(pid)
        self.assertGreater(len(candidati), 1)


class TestICancelliMordono(unittest.TestCase):
    def setUp(self):
        self.dati = _dati()
        self.giorno = self.dati["march_clock"]["giorno_corrente"]
        _, self.pid, self.num, self.fondo = _numerici(self.dati)[0]

    def _rosso(self, delta, frammento):
        with self.assertRaises(ds.DeltaError) as cm:
            ds.operazioni(delta, self.dati)
        self.assertIn(frammento, str(cm.exception))

    def test_un_delta_scritto_su_un_altro_stato(self):
        self._rosso({"march_clock": {"da": self.giorno - 3, "a": self.giorno - 2}},
                    "parte dal Day")
        altro = (self.num + 2) % self.fondo
        self._rosso({"clock": [{"png_id": self.pid, "da": altro, "a": altro + 1}]},
                    "state.yaml dice")

    def test_un_png_id_che_non_esiste(self):
        self._rosso({"stato": [{"png_id": "nessuno-cosi", "stato": "morto"}]},
                    "nessun villain")

    def test_uno_stato_fuori_enumerazione(self):
        self._rosso({"stato": [{"png_id": self.pid, "stato": "defunto"}]},
                    "fuori enumerazione")

    def test_una_chiave_sconosciuta(self):
        """Un refuso ignorato in silenzio e' la regex di prima con un altro nome."""
        self._rosso({"clok": []}, "chiave sconosciuta")

    def test_un_clock_non_numerico(self):
        xal = next(r["png_id"] for r in self.dati["villain"]
                   if "/" not in str(r.get("clock") or ""))
        self._rosso({"clock": [{"png_id": xal, "da": 0, "a": 1}]}, "non e' numerico")

    def test_un_clock_oltre_il_fondo(self):
        self._rosso({"clock": [{"png_id": self.pid, "da": self.num,
                                "a": self.fondo + 1}]}, "esce dal clock")

    def test_lo_stesso_villain_due_volte(self):
        self._rosso({"stato": [{"png_id": self.pid, "stato": "morto"},
                               {"png_id": self.pid, "stato": "latitante"}]},
                    "compare due volte")

    def test_tutto_o_niente(self):
        """Una voce buona accanto a una cattiva non passa da sola."""
        self._rosso({"march_clock": {"da": self.giorno, "a": self.giorno + 1},
                     "stato": [{"png_id": "nessuno-cosi", "stato": "morto"}]},
                    "nessun villain")

    def test_un_log_gia_applicato_non_scrive_e_non_e_un_errore(self):
        delta = {"march_clock": {"da": self.giorno - 1, "a": self.giorno},
                 "clock": [{"png_id": self.pid, "da": self.num - 1 if self.num else 1,
                            "a": self.num}]}
        self.assertEqual(ds.operazioni(delta, self.dati), [])


class TestIlRecapNonLoVede(unittest.TestCase):
    """Il front-matter porta numeri di clock: e' materia del DM, non dei PG."""

    LOG = (ds.emetti({"clock": [{"png_id": "ghaurush", "da": 0, "a": 1}]})
           + "# Session 4 — Prova (2026-09-24)\n\n"
           "**Players present**: A (Thorik)\n\n## Summary\n\nTesto.\n\n"
           "## XP awarded\n\n- **Total**: 1200 xp a testa\n")

    def test_nessuna_sezione_pubblica_contiene_il_delta(self):
        sezioni = session_recap.parse_sections(self.LOG)
        self.assertIn("Summary", sezioni)
        for testo in sezioni.values():
            self.assertNotIn("png_id", testo)
            self.assertNotIn("ghaurush", testo)

    def test_l_intestazione_si_legge_ancora(self):
        meta = session_recap.parse_session_meta(self.LOG, Path("x.md"))
        self.assertEqual(meta["number"], 4)


class TestSuiFileVeri(unittest.TestCase):
    """`state_apply` sui tre master del repo, copiati in un repo temporaneo."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "campaign" / "sessions").mkdir(parents=True)
        for nome in ("state.md", "state.yaml", "state-changelog.md"):
            shutil.copy(ROOT / "campaign" / nome, self.repo / "campaign" / nome)
        dati = _dati()
        self.giorno = dati["march_clock"]["giorno_corrente"]
        self.gha = next(r for r in dati["villain"] if r["png_id"] == "ghaurush")
        self.sonjak = next(r for r in dati["villain"] if r["png_id"] == "sonjak")
        num = int(str(self.gha["clock"]).partition("/")[0])
        self.delta = {"march_clock": {"da": self.giorno, "a": self.giorno + 1},
                      "clock": [{"png_id": "ghaurush", "da": num, "a": num + 1}],
                      "stato": [{"png_id": "ushgar", "stato": "morto"}]}
        self.clock_atteso = f"{num + 1}/{str(self.gha['clock']).partition('/')[2]}"
        sonjak = str(self.sonjak["clock"]).partition("/")
        # La stessa sessione scritta ANCHE in prosa, con in piu' un clock di
        # Sonjak che il delta non ha: la regex, da sola, lo scriverebbe.
        self.log = self.repo / "campaign" / "sessions" / "2026-09-24_session-4.md"
        self.log.write_text(
            ds.emetti(self.delta)
            + "# Session 4 — Prova (2026-09-24)\n\n## World events triggered\n\n"
            f"- **March Clock**: Day {self.giorno} → Day {self.giorno + 1}\n"
            f"- **Villain clocks**: Sonjak {sonjak[0]} → {int(sonjak[0]) + 1}\n",
            encoding="utf-8")
        for cmd in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"],
                    ["config", "user.name", "t"], ["add", "-A"],
                    ["commit", "-qm", "init"], ["checkout", "-qb", "campaign-group-test"]):
            subprocess.run(["git", "-C", str(self.repo), *cmd], check=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _run(self, *argv):
        return state_apply.main(["--session", self.log.name, "--no-guard",
                                 "--repo-root", str(self.repo), *argv])

    def _villain(self, pid):
        dati = yaml.safe_load((self.repo / "campaign" / "state.yaml").read_text(encoding="utf-8"))
        return next(r for r in dati["villain"] if r["png_id"] == pid), dati

    def test_il_delta_scrive_il_master_e_la_vista_segue(self):
        self.assertEqual(self._run("--yes"), 0)
        gha, dati = self._villain("ghaurush")
        self.assertEqual(gha["clock"], self.clock_atteso)
        self.assertEqual(self._villain("ushgar")[0]["stato"], "morto")
        self.assertEqual(dati["march_clock"]["giorno_corrente"], self.giorno + 1)
        md = (self.repo / "campaign" / "state.md").read_text(encoding="utf-8")
        rigenerato, mancanti = render_state.apply_regions(md, dati)
        self.assertEqual(mancanti, [])
        self.assertEqual(rigenerato, md, "dopo l'apply la vista e' gia' allineata")
        self.assertIn(f"clock ghaurush", (self.repo / "campaign" /
                      "state-changelog.md").read_text(encoding="utf-8"))

    def test_una_via_sola(self):
        """La riga di prosa su Sonjak non passa: con un delta scrive solo lui."""
        self.assertEqual(self._run("--yes"), 0)
        self.assertEqual(self._villain("sonjak")[0]["clock"], self.sonjak["clock"])

    def test_il_secondo_giro_non_scrive_niente(self):
        self.assertEqual(self._run("--yes"), 0)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "apply"], check=True)
        prima = (self.repo / "campaign" / "state-changelog.md").read_text(encoding="utf-8")
        self.assertEqual(self._run("--yes"), 0)
        self.assertEqual(prima, (self.repo / "campaign" /
                                 "state-changelog.md").read_text(encoding="utf-8"))

    def test_un_delta_sbagliato_non_tocca_niente(self):
        testo = self.log.read_text(encoding="utf-8").replace(
            "png_id: ushgar", "png_id: nessuno-cosi")
        self.log.write_text(testo, encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "commit", "-aqm", "rotto"], check=True)
        prima = {n: (self.repo / "campaign" / n).read_text(encoding="utf-8")
                 for n in ("state.md", "state.yaml", "state-changelog.md")}
        self.assertEqual(self._run("--yes"), 1)
        for n, testo in prima.items():
            self.assertEqual(testo, (self.repo / "campaign" / n).read_text(encoding="utf-8"), n)


if __name__ == "__main__":
    unittest.main()
