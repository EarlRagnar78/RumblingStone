"""Il confronto cieco fra versioni (ADR-0093): appaiamento, chiave, criterio."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _cv():
    spec = importlib.util.spec_from_file_location(
        "cieco_versioni", ROOT / "scripts" / "cieco_versioni.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CV = _cv()

LUNGO = " ".join(["pietra"] * 30)
MASTER = f"""# Modulo

## SCENA 1 — La soglia

> *La porta si apre su una sala vuota. {LUNGO}.*

## SCENA 2 — Il re

> *Il re alza un braccio verso il soffitto. {LUNGO}.*

## Tattiche

> *Calibrazione rapida: Blast ~28 a colpo, RD 10. {LUNGO}.*
"""


class TestCampione(unittest.TestCase):
    def _file(self, testo):
        d = tempfile.mkdtemp()
        p = Path(d) / "m.md"
        p.write_text(testo, encoding="utf-8")
        return str(p)

    def test_stesso_seme_stesso_campione(self):
        f = self._file(MASTER)
        a = CV.campione("", [f], 2, 1)
        b = CV.campione("", [f], 2, 1)
        self.assertEqual(a["voci"], b["voci"])

    def test_la_nota_di_regola_non_entra(self):
        f = self._file(MASTER)
        titoli = {v["titolo"] for v in CV.campione("", [f], 5, 1)["voci"]}
        self.assertEqual(titoli, {"SCENA 1 — La soglia", "SCENA 2 — Il re"})


class TestAppaia(unittest.TestCase):
    def test_box_quasi_uguale_lungo_si_appaia(self):
        # Con autojunk attivo due box cosi' davano 0,08.
        voce = {"titolo": "S3", "testo": "L'ultimo nemico sparisce. " + LUNGO}
        dopo = [{"titolo": "S1", "testo": "Altro testo del tutto diverso."},
                {"titolo": "S3", "testo": "L'ultima spada cade. " + LUNGO}]
        i, r, _ = CV.appaia(voce, dopo)
        self.assertEqual(i, 1)
        self.assertGreater(r, 0.8)

    def test_box_spezzato_in_battute_si_ricompone(self):
        # Le coppie 3 e 12 del primo voto: il box nuovo era diventato una riga
        # di box e tre battute fuori dai box, che `box_read_aloud` non vede.
        vecchio = ("> *Lei si volta verso Thorik, e c'è qualcosa nei suoi occhi. "
                   "«Ricordi la mano fredda, la luce verde?» Thorik ricorda. "
                   "«Ero io. Siamo pari, tu e io, e non lo eravamo mai stati.»*")
        nuovo = ("## S7\n\n> *Lei si volta verso Thorik. C'è qualcosa nei suoi occhi.*\n\n"
                 "Le battute qui sotto sono l'attacco.\n\n"
                 "Hella: *«Ricordi la mano fredda, la luce verde?»*\n\n"
                 "*Thorik ricorda.*\n\n"
                 "Hella: *«Ero io. Siamo pari, tu e io, e non lo eravamo mai stati.»*\n\n"
                 "## S8\n\n> *Altro box, del tutto diverso, sotto un'altra scena.*\n")
        voce = {"titolo": "S7", "testo": CV.box_con_titolo("## S7\n\n" + vecchio)[0]["testo"]}
        solo_box = CV.box_con_titolo(nuovo)
        con_battute = CV.box_con_titolo(nuovo, battute=True)
        self.assertEqual(len(solo_box), 2)
        _, r_prima, _ = CV.appaia(voce, solo_box)
        i, r, testo = CV.appaia(voce, con_battute)
        self.assertIn("Siamo pari", testo)
        self.assertNotIn("Altro box", testo)
        self.assertNotIn("attacco", testo)
        self.assertGreater(r, r_prima + 0.2)


class TestBattute(unittest.TestCase):
    def test_etichetta_lunga_con_due_punti(self):
        righe = ["**AEGIS FANG (non canta: urla, dentro il cranio):** *«SANGUE ANTICO.»*",
                 "",
                 "**THORGRIM (voce che non trema, occhi che invece sì):** *«Mio nonno.»*"]
        self.assertEqual([i for i, _ in CV._battute(righe)], [0, 2])


class TestVerdettoMisurato(unittest.TestCase):
    def test_meno_dettagli_sensoriali_perde(self):
        vecchio = "Il buio preme contro il vetro, e l'aria sa di fumo e di neve."
        nuovo = "Il buio preme contro la parete."
        self.assertEqual(CV.verdetto_misurato(vecchio, nuovo)[0], "vecchia")
        self.assertEqual(CV.verdetto_misurato(nuovo, vecchio)[0], "nuova")

    def test_tagliare_maiuscole_e_date_non_decide(self):
        vecchio = "Nella prima — Anno −1000 — HAMMERFIST è giovane, e la luce è fredda."
        nuovo = "Nella prima, mille anni fa, Hammerfist è giovane, e la luce è fredda."
        self.assertEqual(CV.verdetto_misurato(vecchio, nuovo)[0], "indecisa")

    def test_monologo_spezzato_perde(self):
        vecchio = "«Bravo. Solo tu potevi vederla. Prendila, e il resto è tuo… vero?»"
        nuovo = "«Bravo. Solo tu potevi vederla.»\n\nLa gemma si scalda.\n\n«Il resto è tuo… vero?»"
        v, perche = CV.verdetto_misurato(vecchio, nuovo)
        self.assertEqual(v, "vecchia")
        self.assertIn("battute", perche)

    def test_due_pezzi_non_bastano(self):
        # Coppie 8 e 18 del primo voto: un box e il suo vicino, non un monologo.
        vecchio = "«Bravo. Solo tu potevi vederla.» E la luce si spegne."
        nuovo = "«Bravo. Solo tu potevi vederla.»\n\nE la luce si spegne."
        self.assertNotIn("battute", CV.verdetto_misurato(vecchio, nuovo)[1])


class TestEsito(unittest.TestCase):
    def _chiave(self, n=20):
        return {"coppie": [{"n": i, "nuova": "A" if i % 2 else "B", "stato": "valida"}
                           for i in range(1, n + 1)]}

    def test_quattordici_su_venti_e_meglio(self):
        chiave = self._chiave()
        voti = []
        for c in chiave["coppie"]:
            vecchia = "B" if c["nuova"] == "A" else "A"
            voti.append(f"{c['n']} {c['nuova'] if c['n'] <= 14 else vecchia}")
        r = CV.esito(chiave, "\n".join(voti))
        self.assertEqual(r["nuova"], 14)
        self.assertTrue(r["verdetto"].startswith("meglio"))
        self.assertGreater(r["wilson_95"][0], 0.48)

    def test_tredici_non_basta_e_il_pari_non_vince(self):
        chiave = self._chiave()
        voti = [f"{c['n']} {c['nuova']}" if c["n"] <= 13 else f"{c['n']} ="
                for c in chiave["coppie"]]
        r = CV.esito(chiave, "\n".join(voti))
        self.assertEqual((r["nuova"], r["pari"]), (13, 7))
        self.assertTrue(r["verdetto"].startswith("non dimostrato"))

    def test_le_coppie_identiche_non_si_contano(self):
        chiave = self._chiave(3)
        chiave["coppie"][0]["stato"] = "identica"
        r = CV.esito(chiave, "1 A\n2 B\n3 A")
        self.assertEqual((r["votate"], r["votabili"]), (2, 2))
        self.assertFalse(r["verdetto"].startswith("incompleto"))

    def test_la_soglia_si_riproporziona(self):
        # Il primo voto: 4 coppie identiche, 16 votabili, soglia 12.
        chiave = self._chiave()
        for c in chiave["coppie"][:4]:
            c["stato"] = "identica"
        self.assertEqual(CV.soglia_per(16), 12)
        voti = [f"{c['n']} {c['nuova']}" if c["n"] <= 16 else
                f"{c['n']} {'B' if c['nuova'] == 'A' else 'A'}" for c in chiave["coppie"][4:]]
        r = CV.esito(chiave, "\n".join(voti))
        self.assertEqual((r["nuova"], r["votabili"], r["soglia"]), (12, 16, 12))
        self.assertTrue(r["verdetto"].startswith("meglio"))

    def test_la_misura_decide_dove_il_dm_non_vota(self):
        chiave = self._chiave(4)
        for c, m in zip(chiave["coppie"], ["nuova", "nuova", "nuova", "indecisa"]):
            c["misura"], c["controllo"] = m, False
        nuova_4 = chiave["coppie"][3]["nuova"]
        r = CV.esito(chiave, f"4 {nuova_4}")
        self.assertEqual((r["misurate"], r["nuova"], r["votate"]), (3, 4, 4))
        self.assertTrue(r["verdetto"].startswith("meglio"))

    def test_due_controlli_smentiti_e_la_misura_cade(self):
        chiave = self._chiave(4)
        for c in chiave["coppie"]:
            c["misura"], c["controllo"] = "nuova", True
        voti = "\n".join(f"{c['n']} {'B' if c['nuova'] == 'A' else 'A'}"
                         for c in chiave["coppie"][:2])
        voti += "\n" + "\n".join(f"{c['n']} {c['nuova']}" for c in chiave["coppie"][2:])
        r = CV.esito(chiave, voti)
        self.assertEqual(r["controlli"], [2, 4])
        self.assertTrue(r["verdetto"].startswith("misura smentita"))

    def test_voti_mancanti_sono_incompleti(self):
        r = CV.esito(self._chiave(), "1 A")
        self.assertTrue(r["verdetto"].startswith("incompleto: 1 coppie decise su 20"))

    def test_le_etichette_contano_la_versione_scartata(self):
        chiave = self._chiave(3)  # nuova: 1 A, 2 B, 3 A
        r = CV.esito(chiave, "1 B goffo, spiega\n2 B\n3 = goffo\n")
        self.assertEqual(r["etichette"]["nuova"], {"goffo": 1, "spiega": 1})
        self.assertEqual(r["etichette"]["vecchia"], {})
        self.assertEqual((r["nuova"], r["vecchia"], r["pari"]), (1, 1, 1))

    def test_etichetta_sconosciuta_non_cambia_il_voto(self):
        chiave = self._chiave(1)
        r = CV.esito(chiave, "1 A bellissima")
        self.assertEqual(r["nuova"], 1)
        self.assertEqual(r["etichette"]["sconosciute"], ["bellissima"])

    def test_wilson_noto(self):
        basso, alto = CV.wilson(14, 20)
        self.assertAlmostEqual(basso, 0.481, places=2)
        self.assertAlmostEqual(alto, 0.855, places=2)


if __name__ == "__main__":
    unittest.main()
