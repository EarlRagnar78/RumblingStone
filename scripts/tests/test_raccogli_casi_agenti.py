"""Ogni thread nuovo porta un caso al set d'oro, e Jfs ne conferma l'etichetta (ADR-0154)."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import instradamento_agenti as ia  # noqa: E402
import raccogli_casi_agenti as rc  # noqa: E402


def _caso(testo: str, atteso: str, split: str, **altro) -> dict:
    c = {"data": "2026-11-20", "fonte": "thread «prova»", "tipo": "dm", "testo": testo,
         "atteso": atteso, "accettabili": [], "annotatore_b": atteso, "split": split}
    c.update(altro)
    return c


class _Base(unittest.TestCase):
    # «scegli» finta: le parole chiave decidono, così i test non dipendono dai trigger veri
    RISPOSTE = {"ci": ["sviluppatore", "autore-documenti"], "mappa": ["cartografo"],
                "box": ["autore-prosa-gioco"]}

    def _scegli(self, testo: str) -> "list[str]":
        for chiave, agenti in self.RISPOSTE.items():
            if chiave in testo.lower().split():
                return list(agenti)
        return []

    def _voti(self, testo: str) -> "dict[str, int]":
        agenti = self._scegli(testo)
        return {a: len(agenti) - i for i, a in enumerate(agenti)}

    def setUp(self) -> None:
        self.dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.dir)
        self.coda = self.dir / "coda"
        self.oro = self.dir / "oro.json"
        casi = [_caso("sistema la ci rossa", "sviluppatore", "dev"),
                _caso("disegna la mappa della cripta", "cartografo", "test"),
                _caso("riscrivi il box", "autore-prosa-gioco", "test"),
                _caso("grazie, chiudo", "nessuno", "test")]
        self.oro.write_text(json.dumps({"nota": "prova.", "tetto": {
            "nota": "Cricchetto di prova.", "giusti": 3, "giusti_indulgenti": 3,
            "macro_f1": "1"}, "casi": casi}, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        self.kw = {"scegli_": self._scegli, "voti_": self._voti}

    def _in(self, messaggi: "list[dict]") -> Path:
        p = self.dir / "IN.json"
        p.write_text(json.dumps(messaggi, ensure_ascii=False), encoding="utf-8")
        return p

    @staticmethod
    def _msg(id_: str, testo: str, tipo: str = "dm") -> dict:
        return {"data": "2026-11-24", "fonte": f"thread «{id_}»", "tipo": tipo,
                "testo": testo, "id_messaggio": id_}


class TestNormalizzaESegreti(unittest.TestCase):
    def test_normalizza(self) -> None:
        self.assertEqual(rc.normalizza("  Sistema   la CI\n rossa! "),
                         rc.normalizza("sistema la ci rossa"))
        self.assertNotEqual(rc.normalizza("sistema la ci"), rc.normalizza("sistema la cia"))

    def test_segreti_ed_email(self) -> None:
        sporchi = ["scrivimi a mario.rossi@example.com",
                   "il token è ghp_" + "a" * 36,
                   "usa github_pat_" + "A1b2" * 10,
                   "chiave sk-ant-api03-" + "x" * 40,
                   "AKIA" + "ABCDEFGHIJKLMNOP",
                   "-----BEGIN OPENSSH PRIVATE KEY-----",
                   "password=hunter22",
                   "xoxb-123456789012-abcdefghijkl",
                   "il file è in " + "/home" + "/mario/repo"]
        for t in sporchi:
            with self.subTest(t=t):
                self.assertTrue(rc.motivo_scarto(t), t)
        puliti = ["sistema la CI rossa sul test di validate_pg",
                  "la password del forziere è un enigma della cripta",
                  "il file è in " + "/home" + "/user/repo",
                  "chiedi a @autore-documenti"]
        for t in puliti:
            with self.subTest(t=t):
                self.assertIsNone(rc.motivo_scarto(t), t)


class TestSplit(unittest.TestCase):
    def test_split_per_hash_deterministico(self) -> None:
        for id_ in ("cmsg_a", "cmsg_b", "cmsg_01KdRg4J"):
            atteso = "dev" if int(hashlib.sha256(id_.encode()).hexdigest(), 16) % 2 == 0 \
                else "test"
            self.assertEqual(rc.split_di(id_), atteso)
            self.assertEqual(rc.split_di(id_), rc.split_di(id_))

    def test_split_circa_meta(self) -> None:
        n = sum(rc.split_di(f"cmsg_{i}") == "test" for i in range(1000))
        self.assertTrue(430 < n < 570, n)


class TestProponi(_Base):
    def test_scarta_duplicati_segreti_e_scrive_settimana(self) -> None:
        msg = [self._msg("m1", "Sistema la CI rossa"),          # già nel set (testo)
               self._msg("m2", "disegna la mappa del forte"),
               self._msg("m2", "un altro testo con lo stesso id"),  # stesso id in ingresso
               self._msg("m3", "Disegna la mappa   del forte"),  # stesso testo in ingresso
               self._msg("m4", "scrivimi a a.b@example.org"),
               self._msg("m5", "   "),
               self._msg("m6", "Avviso: la catena non è stata chiamata", "coordinatore")]
        with contextlib.redirect_stdout(io.StringIO()):
            esito = rc.proponi(self._in(msg), self.coda, oro=self.oro, oggi="2026-11-30",
                               **self.kw)
        self.assertEqual([c["id_messaggio"] for c in esito["proposti"]], ["m2", "m6"])
        motivi = {s["id_messaggio"]: s["motivo"] for s in esito["scartati"]}
        self.assertEqual(set(motivi), {"m1", "m2", "m3", "m4", "m5"})
        self.assertIn("ingresso", motivi["m2"])
        self.assertIn("set d'oro", motivi["m1"])
        self.assertIn("email", motivi["m4"])
        # la seconda m2 è scartata per id
        self.assertEqual(sum(1 for s in esito["scartati"] if s["id_messaggio"] == "m2"), 1)
        settimana = self.coda / "2026-W49.json"
        d = json.loads(settimana.read_text(encoding="utf-8"))
        c2 = next(c for c in d["casi"] if c["id_messaggio"] == "m2")
        self.assertEqual(c2["proposta"], "cartografo")
        # la consigliata non è la predizione dell'hook (ancoraggio): aspetta l'annotatore cieco
        self.assertIsNone(c2["consigliata"])
        self.assertEqual(c2["stato"], "da confermare")
        self.assertIn("nessuno", c2["alternative"])
        self.assertEqual(c2["catene"]["cartografo"], list(ia.CATENE["cartografo"]))
        # un avviso del coordinatore non chiede lavoro: la consigliata è «nessuno»
        c6 = next(c for c in d["casi"] if c["id_messaggio"] == "m6")
        self.assertEqual(c6["consigliata"], "nessuno")
        card = (self.coda / "CARD.md").read_text(encoding="utf-8")
        self.assertIn("m2", card)
        self.assertIn("da annotare", card)
        self.assertIn("→", card)
        self.assertNotIn("a.b@example.org", card)

    def test_seconda_scelta_dei_voti_fra_le_alternative(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            esito = rc.proponi(self._in([self._msg("m9", "la ci e la doc")]), self.coda,
                               oro=self.oro, oggi="2026-11-30", **self.kw)
        c = esito["proposti"][0]
        self.assertEqual(c["proposta"], "sviluppatore")
        # senza consigliata nessuna opzione è messa avanti: la proposta è fra le alternative
        self.assertEqual(c["alternative"], ["sviluppatore", "autore-documenti", "nessuno"])
        self.assertEqual(set(c["catene"]), {"sviluppatore", "autore-documenti", "nessuno"})

    def test_coda_esistente_non_ripete(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            rc.proponi(self._in([self._msg("m2", "disegna la mappa del forte")]), self.coda,
                       oro=self.oro, oggi="2026-11-30", **self.kw)
            esito = rc.proponi(self._in([self._msg("m2", "disegna la mappa del forte"),
                                         self._msg("m7", "riscrivi il box del ponte")]),
                               self.coda, oro=self.oro, oggi="2026-12-01", **self.kw)
        self.assertEqual([c["id_messaggio"] for c in esito["proposti"]], ["m7"])
        self.assertIn("coda", esito["scartati"][0]["motivo"])
        d = json.loads((self.coda / "2026-W49.json").read_text(encoding="utf-8"))
        self.assertEqual([c["id_messaggio"] for c in d["casi"]], ["m2", "m7"])

    def test_ingresso_malformato_esce_2(self) -> None:
        p = self._in([{"testo": "manca tutto"}])
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(rc.main(["proponi", str(p), "--coda", str(self.coda),
                                      "--oro", str(self.oro)]), 2)


class TestCieco(_Base):
    """La consigliata viene da un annotatore che non vede la predizione dell'hook."""

    def _proponi(self, msg: "list[dict]") -> Path:
        with contextlib.redirect_stdout(io.StringIO()):
            rc.proponi(self._in(msg), self.coda, oro=self.oro, oggi="2026-11-30", **self.kw)
        return self.coda / "2026-W49.json"

    def _tsv(self, righe: "list[str]") -> Path:
        p = self.dir / "ANNOTAZIONI.tsv"
        p.write_text("id_messaggio\tetichetta\n" + "\n".join(righe) + "\n", encoding="utf-8")
        return p

    def test_cieco_non_mostra_la_proposta(self) -> None:
        sett = self._proponi([self._msg("m2", "disegna la mappa del forte"),
                              self._msg("m6", "Avviso: fatto", "coordinatore")])
        with contextlib.redirect_stdout(io.StringIO()):
            uscita = rc.cieco(sett)
        testo = uscita.read_text(encoding="utf-8")
        self.assertIn("m2", testo)
        self.assertIn("disegna la mappa del forte", testo)
        self.assertNotIn("cartografo", testo)
        self.assertNotIn("m6", testo)   # «nessuno» per regola: non serve annotarlo

    def test_annota_mette_la_consigliata_e_misura_l_accordo(self) -> None:
        sett = self._proponi([self._msg("m2", "disegna la mappa del forte"),
                              self._msg("m7", "riscrivi il box del ponte"),
                              self._msg("m8", "sistema la ci del ramo")])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            esito = rc.annota(sett, self._tsv(["m2\tcartografo", "m7\tautore-master",
                                               "m8\tsviluppatore"]))
        self.assertEqual(esito, 0)
        d = json.loads(sett.read_text(encoding="utf-8"))
        per_id = {c["id_messaggio"]: c for c in d["casi"]}
        self.assertEqual(per_id["m7"]["consigliata"], "autore-master")
        self.assertEqual(per_id["m7"]["annotatore"], "cieco")
        self.assertIn("autore-prosa-gioco", per_id["m7"]["alternative"])
        self.assertIn("autore-master", per_id["m7"]["catene"])
        self.assertIn("accordo hook-cieco 2/3", out.getvalue())
        self.assertIn("kappa", out.getvalue())
        card = (self.coda / "CARD.md").read_text(encoding="utf-8")
        self.assertIn("Consigliata: autore-master", card)
        self.assertIn("m7\tautore-master", card)

    def test_annota_rifiuta_etichetta_o_id_sconosciuti(self) -> None:
        sett = self._proponi([self._msg("m2", "disegna la mappa del forte")])
        prima = sett.read_text(encoding="utf-8")
        for righe in (["m2\tmago"], ["m99\tcartografo"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(rc.annota(sett, self._tsv(righe)), 1)
            self.assertEqual(sett.read_text(encoding="utf-8"), prima)

    def test_riga_di_comando(self) -> None:
        sett = self._proponi([self._msg("m2", "disegna la mappa del forte")])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(rc.main(["cieco", str(sett)]), 0)
            self.assertEqual(rc.main(["annota", str(sett),
                                      str(self._tsv(["m2\tcartografo"]))]), 0)


class TestApplica(_Base):
    def _settimana(self) -> Path:
        msg = [self._msg("m2", "disegna la mappa del forte"),
               self._msg("m7", "riscrivi il box del ponte"),
               self._msg("m8", "sistema la ci del renderer")]
        with contextlib.redirect_stdout(io.StringIO()):
            rc.proponi(self._in(msg), self.coda, oro=self.oro, oggi="2026-11-30", **self.kw)
        return self.coda / "2026-W49.json"

    def _scelte(self, righe: "list[str]") -> Path:
        p = self.dir / "SCELTE.tsv"
        p.write_text("id_messaggio\tatteso\taccettabili\tazione\n" + "\n".join(righe) + "\n",
                     encoding="utf-8")
        return p

    def test_applica_aggiunge_e_rimette_il_tetto(self) -> None:
        sett = self._settimana()
        scelte = self._scelte(["m2\tcartografo\t\ttieni",
                               "m7\tautore-master\tautore-prosa-gioco\ttieni",
                               "m8\t\t\ttogli"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            codice = rc.applica(sett, scelte, oro=self.oro, oggi="2026-12-01",
                                scegli_=self._scegli)
        self.assertEqual(codice, 0)
        d = json.loads(self.oro.read_text(encoding="utf-8"))
        nuovi = [c for c in d["casi"] if c.get("id_messaggio")]
        self.assertEqual([c["id_messaggio"] for c in nuovi], ["m2", "m7"])
        m7 = nuovi[1]
        self.assertEqual((m7["atteso"], m7["accettabili"]), ("autore-master",
                                                              ["autore-prosa-gioco"]))
        self.assertEqual(m7["split"], rc.split_di("m7"))
        self.assertNotIn("proposta", m7)
        # il tetto è quello che l'hook invariato misura sul set nuovo
        v = ia.valuta(self.oro, scegli_=self._scegli, campioni=0)["test"]
        t = d["tetto"]
        self.assertEqual((t["giusti"], t["giusti_indulgenti"], t["macro_f1"]),
                         (v["giusti"], v["giusti_indulgenti"], v["macro_f1"]["frazione"]))
        self.assertIn("2026-12-01", t["nota"])
        self.assertIn("non l'hook", t["nota"])
        self.assertIn("a mano non si abbassa", t["nota"])
        self.assertEqual(ia.controlla(self.oro, scegli_=self._scegli)[0], 0)
        out = buf.getvalue()
        self.assertIn("prima", out)
        self.assertIn("dopo", out)
        # la settimana ricorda cosa è stato fatto
        s = {c["id_messaggio"]: c["stato"] for c in
             json.loads(sett.read_text(encoding="utf-8"))["casi"]}
        self.assertEqual(s, {"m2": "applicato", "m7": "applicato", "m8": "tolto"})
        self.assertEqual(rc.controlla_forma(self.oro), [])

    def test_applica_due_volte_non_duplica(self) -> None:
        sett = self._settimana()
        scelte = self._scelte(["m2\tcartografo\t\ttieni"])
        with contextlib.redirect_stdout(io.StringIO()):
            rc.applica(sett, scelte, oro=self.oro, oggi="2026-12-01", scegli_=self._scegli)
            rc.applica(sett, scelte, oro=self.oro, oggi="2026-12-01", scegli_=self._scegli)
        d = json.loads(self.oro.read_text(encoding="utf-8"))
        self.assertEqual(sum(1 for c in d["casi"] if c.get("id_messaggio") == "m2"), 1)

    def test_scelta_sbagliata_non_scrive(self) -> None:
        sett = self._settimana()
        prima = self.oro.read_text(encoding="utf-8")
        for righe in (["m2\tagente-che-non-esiste\t\ttieni"],
                      ["m2\tcartografo\t\tforse"],
                      ["m99\tcartografo\t\ttieni"],
                      ["m2\tcartografo\tcartografo\ttieni"]):
            with self.subTest(righe=righe), contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(rc.applica(sett, self._scelte(righe), oro=self.oro,
                                            oggi="2026-12-01", scegli_=self._scegli), 1)
                self.assertEqual(self.oro.read_text(encoding="utf-8"), prima)


class TestForma(_Base):
    def _scrivi(self, casi: "list[dict]", **altro) -> Path:
        d = {"nota": "x", "tetto": {"giusti": 1, "giusti_indulgenti": 1, "macro_f1": "1"},
             "casi": casi}
        d.update(altro)
        self.oro.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        return self.oro

    def test_forma_buona(self) -> None:
        self.assertEqual(rc.controlla_forma(self.oro), [])

    def test_difetti(self) -> None:
        buono = _caso("uno", "sviluppatore", "dev")
        difetti = {
            "campo": [{k: v for k, v in buono.items() if k != "fonte"}],
            "split": [dict(buono, split="tutto")],
            "duplicat": [buono, dict(buono, data="2026-11-21", testo="  UNO ")],
            "vuoto": [dict(buono, testo="  ")],
            "atteso": [dict(buono, atteso="chi-sa-chi")],
            "accettabil": [dict(buono, accettabili=["sviluppatore"])],
            "tipo": [dict(buono, tipo="giocatore")],
            "data": [dict(buono, data="27/11/2026")],
            "id_messaggio": [dict(buono, id_messaggio="m1"),
                             dict(buono, testo="due", id_messaggio="m1")],
        }
        for parola, casi in difetti.items():
            with self.subTest(parola=parola):
                errori = rc.controlla_forma(self._scrivi(casi))
                self.assertTrue(errori)
                self.assertIn(parola, " ".join(errori).lower())
        errori = rc.controlla_forma(self._scrivi([buono], tetto={}))
        self.assertIn("tetto", " ".join(errori))

    def test_check_da_riga_di_comando(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(rc.main(["--check", "--oro", str(self.oro)]), 0)
            self._scrivi([_caso("", "sviluppatore", "dev")])
            self.assertEqual(rc.main(["--check", "--oro", str(self.oro)]), 1)

    def test_oro_del_repo_in_forma(self) -> None:
        self.assertEqual(rc.controlla_forma(ia.ORO), [])


if __name__ == "__main__":
    unittest.main()
