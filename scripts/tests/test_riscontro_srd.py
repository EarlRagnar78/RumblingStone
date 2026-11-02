"""riscontro_srd: le regole dei master riscontrate sull'SRD 3.5 e sul PRD PF1e.

Nessun test usa la rete. Le fonti sono fixture piccole scritte in una cache
temporanea, con lo sha256 fissato al volo al posto di quello vero; lo scarico
si prova sostituendo ``scarica_url``.
"""

import hashlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import riscontro_srd as R  # noqa: E402

FRECCIA = ("**Slaying Arrow:** This _+1 arrow_ is keyed to a particular type. If it "
           "strikes such a creature, the target must make a DC 20 Fortitude save or die.\n")
FIUTO = ("### Scent\n\nA creature with the scent ability can detect opponents, generally "
         "within 30 feet. If the opponent is upwind, the range is 60 feet.\n")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _db(percorso: Path) -> None:
    con = sqlite3.connect(percorso)
    con.execute("create table sections (section_id integer primary key, type text, "
                "subtype text, lft integer, rgt integer, parent_id integer, name text, "
                "abbrev text, source text, description text, body text, image text, "
                "alt text, url text, create_index boolean)")
    con.execute("insert into sections (type, lft, rgt, name, source, body) values "
                "('item', 1, 2, 'Slaying Arrow', 'Ultimate Equipment', "
                "'<p>the target must succeed at a DC 20 Fortitude save or take 50 points of damage.</p>')")
    con.commit()
    con.close()


class Base(unittest.TestCase):
    """Una cache con due file dell'SRD e un libro del PRD, e un repo con un master."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        t = Path(self._tmp.name)
        self.cache = t / "cache"
        self.repo = t / "repo"
        self.repo.mkdir()
        self.srd_file = {"magic-items/frecce.md": FRECCIA.encode(), "rules/scent.md": FIUTO.encode()}
        srd_base = R.SRD35.cartella(self.cache)
        for rel, dati in self.srd_file.items():
            (srd_base / rel).parent.mkdir(parents=True, exist_ok=True)
            (srd_base / rel).write_bytes(dati)
        pf1_base = R.PF1.cartella(self.cache)
        pf1_base.mkdir(parents=True)
        _db(pf1_base / "book-ue.db")
        self.patch = [
            mock.patch.object(R.SRD35, "file", {k: _sha(v) for k, v in self.srd_file.items()}),
            mock.patch.object(R.PF1, "file", {"book-ue.db": _sha((pf1_base / "book-ue.db").read_bytes())}),
        ]
        for p in self.patch:
            p.start()
        (self.repo / "master.md").write_text(
            "Il worg sente entro **9 m**; col vento **18 m**.\n"
            "Freccia: Tempra **CD 20** o subisce **50 danni**.\n", encoding="utf-8")

    def tearDown(self):
        for p in self.patch:
            p.stop()
        self._tmp.cleanup()

    def basi(self):
        return {"srd35": R.SRD35.cartella(self.cache), "pf1": R.PF1.cartella(self.cache)}

    def voce(self, **k):
        v = {"id": "x", "cosa": "prova", "fonte": "srd35", "master": "master.md"}
        v.update(k)
        return R.riscontra_voce(v, self.basi(), self.repo)

    def esegui(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            codice = R.main(["--cache", str(self.cache), *argv])
        return codice, out.getvalue(), err.getvalue()


class Confronti(Base):
    def test_numero_con_scala_dai_piedi_ai_metri(self):
        e = self.voce(file="rules/scent.md", regola=r"within (?P<v>\d+) feet",
                      affermazione=r"entro \*\*(?P<v>[\d,]+) m\*\*", confronto="numero", scala=0.3)
        self.assertEqual(e.esito, "concorda")
        self.assertIn("rules/scent.md:3", e.fonte)
        self.assertIn("master.md:1", e.master)

    def test_numero_sbagliato_discorda_e_lo_dice(self):
        e = self.voce(file="rules/scent.md", regola=r"upwind, the range is (?P<v>\d+) feet",
                      affermazione=r"entro \*\*(?P<v>[\d,]+) m\*\*", confronto="numero", scala=0.3)
        self.assertEqual(e.esito, "discorda")
        self.assertIn("«9» contro «60»", e.master_dice)

    def test_termine_con_equivalenze(self):
        e = self.voce(file="magic-items/frecce.md", regola=r"save or (?P<v>die)",
                      affermazione=r"o (?P<v>subisce \*\*50 danni\*\*|muore)",
                      confronto="termine", equivale={"die": ["muore"]})
        self.assertEqual(e.esito, "discorda")
        (self.repo / "master.md").write_text("Tempra **CD 20** o muore.\n", encoding="utf-8")
        e = self.voce(file="magic-items/frecce.md", regola=r"save or (?P<v>die)",
                      affermazione=r"o (?P<v>subisce \*\*50 danni\*\*|muore)",
                      confronto="termine", equivale={"die": ["muore"]})
        self.assertEqual(e.esito, "concorda")

    def test_regola_del_prd_dal_database(self):
        e = self.voce(fonte="pf1", libro="book-ue.db", sezione="Slaying Arrow",
                      regola=r"save or take (?P<v>\d+) points of damage",
                      affermazione=r"subisce \*\*(?P<v>\d+) danni\*\*", confronto="numero")
        self.assertEqual(e.esito, "concorda")
        self.assertIn("Ultimate Equipment › Slaying Arrow (book-ue.db)", e.fonte)

    def test_senza_libro_cerca_in_tutti(self):
        e = self.voce(fonte="pf1", sezione="slaying arrow", master=None,
                      regola=r"save or take 50")
        self.assertEqual(e.esito, "concorda")

    def test_non_trovata_nella_fonte_e_nel_master(self):
        e = self.voce(regola="questa frase non c'è", affermazione="x")
        self.assertEqual((e.esito, e.dove), ("non trovata", "nella fonte"))
        e = self.voce(regola="Slaying Arrow", affermazione="nemmeno questa")
        self.assertEqual((e.esito, e.dove), ("non trovata", "nel master"))

    def test_regola_non(self):
        e = self.voce(master=None, file="magic-items/frecce.md",
                      regola=r"\*\*Slaying Arrow:\*\*", regola_non="3d6")
        self.assertEqual(e.esito, "concorda")
        e = self.voce(master=None, file="magic-items/frecce.md",
                      regola=r"\*\*Slaying Arrow:\*\*", regola_non="Fortitude")
        self.assertEqual(e.esito, "discorda")

    def test_ogni_occorrenza_del_master_conta(self):
        (self.repo / "master.md").write_text("entro **9 m**\npoi entro **12 m**\n", encoding="utf-8")
        e = self.voce(file="rules/scent.md", regola=r"within (?P<v>\d+) feet",
                      affermazione=r"entro \*\*(?P<v>[\d,]+) m\*\*", confronto="numero", scala=0.3)
        self.assertEqual(e.esito, "discorda")
        self.assertIn("master.md:2", e.master)

    def test_numeri_italiani_e_inglesi(self):
        self.assertEqual(R.numero("4,5"), 4.5)
        self.assertEqual(R.numero("2.282"), 2282)
        self.assertEqual(R.numero("2,282", inglese=True), 2282)
        self.assertEqual(R.numero("1.5", inglese=True), 1.5)

    def test_confronto_senza_valore_e_un_errore_d_uso(self):
        with self.assertRaises(R.ErroreUso):
            self.voce(file="rules/scent.md", regola="within", affermazione="entro",
                      confronto="numero")


class Comandi(Base):
    def _file(self, voci, nome="r.json"):
        p = self.repo / nome
        p.write_text(json.dumps({"riscontri": voci}), encoding="utf-8")
        return str(p)

    def test_riscontra_scrive_md_e_json_e_strict_esce_1(self):
        f = self._file([
            {"id": "a", "fonte": "srd35", "file": "rules/scent.md", "regola": r"within (?P<v>\d+) feet",
             "master": "master.md", "affermazione": r"entro \*\*(?P<v>[\d,]+) m\*\*",
             "confronto": "numero", "scala": 0.3},
            {"id": "b", "fonte": "srd35", "file": "magic-items/frecce.md", "regola": r"save or (?P<v>die)",
             "master": "master.md", "affermazione": r"o (?P<v>subisce \*\*50 danni\*\*)",
             "confronto": "termine"},
        ])
        md, js = self.repo / "o.md", self.repo / "o.json"
        codice, out, _ = self.esegui("--offline", "riscontra", f, "--repo", str(self.repo),
                                     "--md", str(md), "--json", str(js))
        self.assertEqual(codice, 0)
        self.assertIn("concorda: 1 · discorda: 1 · non trovata: 0", out)
        self.assertIn("Open Game License 1.0a", out)
        self.assertEqual(md.read_text(encoding="utf-8"), out)
        self.assertEqual([e["esito"] for e in json.loads(js.read_text())["esiti"]],
                         ["concorda", "discorda"])
        codice, _, _ = self.esegui("--offline", "riscontra", f, "--repo", str(self.repo), "--strict")
        self.assertEqual(codice, 1)

    def test_due_esecuzioni_danno_lo_stesso_json(self):
        f = self._file([{"id": "a", "fonte": "srd35", "regola": "Slaying"}])
        uscite = []
        for n in range(2):
            js = self.repo / f"o{n}.json"
            self.esegui("--offline", "riscontra", f, "--repo", str(self.repo), "--json", str(js))
            uscite.append(js.read_bytes())
        self.assertEqual(uscite[0], uscite[1])

    def test_file_dei_riscontri_sbagliato_esce_2(self):
        p = self.repo / "r.yaml"
        p.write_text("riscontri: [\n  - id: : x", encoding="utf-8")
        self.assertEqual(self.esegui("--offline", "riscontra", str(p))[0], 2)
        f = self._file([{"id": "a", "fonte": "srd35", "regola": "(non chiusa"}])
        codice, _, err = self.esegui("--offline", "riscontra", f)
        self.assertEqual(codice, 2)
        self.assertIn("regex", err)

    def test_regola_per_nome(self):
        codice, out, _ = self.esegui("--offline", "regola", "Scent")
        self.assertEqual(codice, 0)
        self.assertIn("SRD 3.5, rules/scent.md:1", out)
        codice, out, _ = self.esegui("--offline", "regola", "Slaying Arrow")
        self.assertIn("magic-items/frecce.md:1", out)
        self.assertIn("Ultimate Equipment › Slaying Arrow", out)
        self.assertEqual(self.esegui("--offline", "regola", "Nessuna Regola")[0], 1)


class Scarico(unittest.TestCase):
    """Lo scarico, la cache e la rete che manca."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cache = Path(self._tmp.name) / "cache"
        self.dati = b"## Commune\n**Casting Time:** 10 minutes\n"
        self.p = mock.patch.object(R.SRD35, "file", {"spells/c.md": _sha(self.dati)})
        self.p.start()

    def tearDown(self):
        self.p.stop()
        self._tmp.cleanup()

    def esegui(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            codice = R.main(["--cache", str(self.cache), *argv])
        return codice, out.getvalue(), err.getvalue()

    def test_scarica_e_controlla_lo_sha256(self):
        def finto(url, dest, timeout=60):
            self.assertIn(R.SRD35.commit, url)
            Path(dest).write_bytes(self.dati)
        with mock.patch.object(R, "scarica_url", finto):
            codice, out, _ = self.esegui("scarica", "--fonte", "srd35")
        self.assertEqual(codice, 0)
        self.assertEqual((R.SRD35.cartella(self.cache) / "spells/c.md").read_bytes(), self.dati)
        self.assertEqual(self.esegui("scarica", "--verifica")[0], 0)

    def test_sha256_sbagliato_esce_1_e_non_lascia_il_file(self):
        with mock.patch.object(R, "scarica_url", lambda u, d, timeout=60: Path(d).write_bytes(b"altro")):
            codice, _, err = self.esegui("scarica", "--fonte", "srd35")
        self.assertEqual(codice, 1)
        self.assertIn("sha256", err)
        cartella = R.SRD35.cartella(self.cache)
        self.assertEqual([p.name for p in cartella.rglob("*") if p.is_file()], [])

    def test_senza_rete_esce_3_e_lo_dice(self):
        def giu(url, dest, timeout=60):
            raise urllib.error.URLError("Tunnel connection failed: 403 Forbidden")
        with mock.patch.object(R, "scarica_url", giu):
            codice, _, err = self.esegui("scarica", "--fonte", "srd35")
        self.assertEqual(codice, R.ESITO_RETE)
        self.assertIn("la rete non risponde", err)
        self.assertIn("--da-cartella", err)

    def test_offline_con_cache_vuota_esce_3(self):
        codice, _, err = self.esegui("--offline", "regola", "Commune", "--fonte", "srd35")
        self.assertEqual(codice, 3)
        self.assertIn("--offline", err)

    def test_da_cartella_copia_un_clone_locale(self):
        clone = Path(self._tmp.name) / "clone"
        (clone / "spells").mkdir(parents=True)
        (clone / "spells/c.md").write_bytes(self.dati)
        codice, out, _ = self.esegui("scarica", "--fonte", "srd35", "--da-cartella", f"srd35={clone}")
        self.assertEqual(codice, 0)
        self.assertIn("1 file copiati", out)
        self.assertEqual(self.esegui("--offline", "regola", "Commune", "--fonte", "srd35")[0], 0)

    def test_verifica_trova_un_file_alterato(self):
        f = R.SRD35.cartella(self.cache) / "spells/c.md"
        f.parent.mkdir(parents=True)
        f.write_bytes(b"manomesso")
        codice, out, _ = self.esegui("scarica", "--verifica")
        self.assertEqual(codice, 1)
        self.assertIn("sha256 diverso", out)

    def test_la_cache_si_sceglie_con_la_variabile(self):
        with mock.patch.dict("os.environ", {"RUMBLINGSTONE_SRD_CACHE": "/tmp/x-srd"}):
            self.assertEqual(R.cartella_cache(None), Path("/tmp/x-srd"))
        self.assertEqual(R.cartella_cache("/a/b"), Path("/a/b"))


class FileDelRepo(unittest.TestCase):
    """Il file dei riscontri di ARC-08 e le fonti fissate stanno in piedi senza rete."""

    def test_riscontri_arc08_ben_formati(self):
        f = REPO / "plans/esperimenti/ricerca-rete-2026-10-23/riscontri-arc08.yaml"
        voci = R.leggi_riscontri(f)
        self.assertGreaterEqual(len(voci), 9)
        ids = [v["id"] for v in voci]
        self.assertEqual(len(ids), len(set(ids)), "id ripetuti")
        for v in voci:
            self.assertIn(v["fonte"], R.FONTI)
            for chiave in ("regola", "affermazione", "regola_non"):
                R.compila(v, chiave)
            if v.get("file"):
                self.assertIn(v["file"], R.SRD35.file, v["id"])
            if v.get("master"):
                self.assertTrue((REPO / v["master"]).is_file(), v["master"])

    def test_fonti_fissate(self):
        for f in R.FONTI.values():
            self.assertRegex(f.commit, r"^[0-9a-f]{40}$")
            self.assertIn(f.file_licenza, f.file)
            for rel, h in f.file.items():
                self.assertRegex(h, r"^[0-9a-f]{64}$", rel)
            self.assertIn("Open Game License 1.0a", f.licenza)


if __name__ == "__main__":
    unittest.main()
