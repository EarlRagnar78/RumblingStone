"""La pipeline migliora_prosa: modello di preferenza, filtro, scheda cieca, esito."""
from __future__ import annotations

import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _mp():
    spec = importlib.util.spec_from_file_location(
        "migliora_prosa", ROOT / "scripts" / "migliora_prosa.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._NLP = False          # senza spaCy: test veloci e uguali ovunque
    return mod


MP = _mp()

ORIGINALE = ("Il vecchio alza la testa e guarda la luce dietro Thorik. Un fabbro con una "
             "gamba sola si tira su contro il muro, e il muro gli si apre sotto la mano come "
             "argilla. Ottocento nani guardano un nano con una corona, e nel cortile c'è solo "
             "il respiro della forgia.")


class TestModello(unittest.TestCase):
    def test_simmetrico(self):
        Z = [[1.0, 0.2], [0.5, -0.3], [2.0, 0.1], [-0.2, 0.4]]
        m = MP.addestra(Z)
        for z in ([0.7, 0.1], [-1.0, 2.0]):
            self.assertAlmostEqual(MP.probabilita(m, z) + MP.probabilita(m, [-v for v in z]), 1.0)

    def test_impara_il_tratto_che_decide(self):
        # il primo tratto è sempre positivo per chi vince, il secondo è rumore
        Z = [[1.0 + i % 3, (-1) ** i * 0.5] for i in range(20)]
        m = MP.addestra(Z)
        self.assertGreater(m["pesi"][0], 0)
        self.assertGreater(abs(m["pesi"][0]), abs(m["pesi"][1]))
        self.assertGreater(MP.probabilita(m, [1.5, 0.0]), 0.5)

    def test_risolvi(self):
        x = MP._risolvi([[2.0, 1.0], [1.0, 3.0]], [3.0, 5.0])
        self.assertAlmostEqual(x[0], 0.8)
        self.assertAlmostEqual(x[1], 1.4)

    def test_test_del_segno(self):
        self.assertEqual(MP.binom_p(0, 0), 1.0)
        self.assertAlmostEqual(MP.binom_p(5, 10), 1.0)
        self.assertLess(MP.binom_p(10, 10), 0.01)

    def test_valida_su_un_dataset_piccolo(self):
        corto, lungo = "Pietra fredda.", "Pietra fredda, nera e silenziosa sotto la luce del fuoco."
        voti = [{"pari": False, "vincente": lungo, "perdente": corto, "originale": corto}
                for _ in range(6)] + [{"pari": True, "vincente": corto, "perdente": lungo,
                                       "originale": corto}]
        r = MP.valida(voti)
        self.assertEqual(r["coppie"], 6)
        self.assertEqual(r["pari_esclusi"], 1)
        self.assertEqual(r["piu_lunga"], 6)
        self.assertFalse(r["supera_soglia"])   # non batte «vince la più lunga»
        self.assertIn("NON superata", MP.rapporto(r))


class TestFiltro(unittest.TestCase):
    def test_passa_una_riscrittura_leggera(self):
        c = ORIGINALE.replace("Il vecchio alza", "Accanto all'incudine il vecchio alza")
        self.assertEqual(MP.filtra(ORIGINALE, c), [])

    def test_numero_cambiato(self):
        o = ORIGINALE.replace("Ottocento", "800")
        c = o.replace("800", "900")
        self.assertTrue(any(m.startswith("fatto cambiato") for m in MP.filtra(o, c)))

    def test_sensi_tolti(self):
        c = ORIGINALE.replace("guarda la luce dietro Thorik", "guarda Thorik") \
                     .replace(" c'è solo il respiro della forgia", " non si muove nessuno")
        motivi = MP.filtra(ORIGINALE, c)
        self.assertTrue(any("sensoriali" in m or "impoverito" in m for m in motivi), motivi)

    def test_frase_finale_tolta(self):
        c = ORIGINALE.rsplit(" Ottocento", 1)[0]
        self.assertTrue(MP.frase_finale_tolta(ORIGINALE, c))
        self.assertIn("regola 3, frase finale tolta", MP.filtra(ORIGINALE, c))

    def test_monologo_spezzato(self):
        o = "«Prendi la gemma, socio. Incastonala nell'Anello e avrai lo sconto a vita.»"
        c = "«Prendi la gemma, socio.»\n\n*La gemma si scalda.*\n\n«Incastonala nell'Anello: sconto a vita.»"
        self.assertTrue(MP.monologo_spezzato(o, c))

    def test_subordinata_spezzata_senza_parser(self):
        o = "Il fabbro si tira su contro il muro che gli si apre sotto la mano."
        c = "Il fabbro si tira su contro il muro. Il muro gli si apre sotto la mano."
        self.assertTrue(MP.subordinata_spezzata(o, c))
        self.assertFalse(MP.subordinata_spezzata(c, o))


class TestCandidate(unittest.TestCase):
    def test_in_chiaro_e_in_box(self):
        testo = ("# P01\n\n## Candidata 1\n\nUna riga\nche continua.\n\n"
                 "## Candidata 2\n\n> *Un box citato*\n> *che continua.*\n\n<!-- nota -->\n")
        self.assertEqual(MP.leggi_candidate(testo), ["Una riga che continua.",
                                                     "Un box citato che continua."])

    def test_migliora_sceglie_fra_le_buone(self):
        buona = ORIGINALE.replace("Il vecchio alza", "Accanto all'incudine il vecchio alza")
        cattiva = ORIGINALE.rsplit(" Ottocento", 1)[0]
        m = MP.addestra([[0.0] * len(MP.TRATTI)])
        r = MP.migliora(ORIGINALE, [cattiva, buona], m)
        self.assertEqual(r["vincitrice"], 2)
        self.assertTrue(r["candidate"][0]["scartata"])

    def test_se_la_migliore_perde_contro_l_originale_resta_l_originale(self):
        buona = ORIGINALE.replace("Il vecchio alza", "Accanto all'incudine il vecchio alza")
        m = MP.addestra([[0.0] * len(MP.TRATTI)])
        # la candidata ha il Gulpease più basso dell'originale: con questi pesi perde
        m["pesi"] = [5.0] * len(MP.TRATTI)
        m["scala"] = [1.0] * len(MP.TRATTI)
        r = MP.migliora(ORIGINALE, [buona], m)
        self.assertLess(r["punteggio"], 0.5)
        self.assertIsNone(r["vincitrice"])
        self.assertEqual(r["resta_originale"], "la migliore perde contro l'originale")


class TestDataset(unittest.TestCase):
    SCHEDA = ("# Scheda\n\n## Parte 1 — 2 coppie\n\n## Coppia 1\n\n*Box B01*\n\n**A**\n\n> uno A\n>\n> due A\n\n"
              "**B**\n\n> uno B\n\n## Coppia 2\n\n*Box B02*\n\n**A**\n\n> x A\n\n**B**\n\n> x B\n\n"
              "## Parte 2 — 1 coppie\n\n## Coppia 1\n\n*Box B01*\n\n**A**\n\n> p2 A\n\n**B**\n\n> p2 B\n")

    def test_scheda_a_piu_parti(self):
        p = MP._voci_scheda(self.SCHEDA)
        self.assertEqual(p[1][1], ("Box B01", "uno A\n\ndue A", "uno B"))
        self.assertEqual(p[2][1][1], "p2 A")

    def test_coppie_con_chiave_voti_ed_etichette(self):
        chiave = {"coppie": [{"n": 1, "nuova": "A", "stato": "valida"},
                             {"n": 2, "nuova": "B", "stato": "valida"}]}
        out = MP.coppie_da_scheda(self.SCHEDA, chiave, "1 B ritmo goffo\n2 =\n", "prova", 1,
                                  {"B01": "orig"}, "V", "N")
        self.assertEqual(out[0]["vincente"], "uno B")
        self.assertEqual(out[0]["ruolo_vincente"], "V")
        self.assertEqual(out[0]["etichette_sulla_perdente"], ["ritmo", "goffo"])
        self.assertEqual(out[0]["originale"], "orig")
        self.assertTrue(out[1]["pari"])

    def test_dataset_del_repo(self):
        coppie = MP.dataset()
        self.assertGreaterEqual(len(coppie), 55)
        for v in coppie:
            for k in ("id", "fonte", "pari", "vincente", "perdente", "originale"):
                self.assertIn(k, v)
        self.assertEqual(len({v["id"] for v in coppie}), len(coppie))


class TestCampioneEdEsito(unittest.TestCase):
    def test_giro_completo(self):
        scelte = {"box": [{"id": "P01", "file": "x.md", "box": 0, "titolo": "Scena",
                           "originale": ORIGINALE, "vincitrice": 1,
                           "candidate": [{"n": 1, "testo": ORIGINALE.replace(
                               "Il vecchio alza", "Accanto all'incudine il vecchio alza")}]}]}
        scheda, chiave = MP.campione(scelte, 3)
        self.assertIn("## Coppia 1", scheda)
        self.assertIn("*Box P01*", scheda)
        self.assertNotIn("_testi-provvisori", scheda)
        self.assertFalse((MP.PIPE / "cieco" / "_testi-provvisori.md").exists())
        voto = chiave["coppie"][0]["nuova"]
        r, nuove = MP.registra_esito(scelte, chiave, f"1 {voto}\n", "2026-10-22")
        self.assertEqual(r["nuova"], 1)
        self.assertEqual(nuove[0]["ruolo_vincente"], "pipeline")
        self.assertEqual(nuove[0]["perdente"], ORIGINALE)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "VOTI.json"
            MP.scrivi_voti(nuove, p)
            self.assertEqual(MP.carica_voti(p)[0]["fonte"], "pipeline-2026-10-22")


class TestVarianti(unittest.TestCase):
    VOTI = [{"id": f"c{i}", "pari": False, "originale": None,
             "vincente": f"Pietra fredda e nera numero {i}, sotto la luce del fuoco.",
             "perdente": f"Pietra numero {i}."} for i in range(6)]

    def test_esterni_e_tratti_mancanti(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.json"
            p.write_text(json.dumps({"_nota": "x", "c0": {"vincente": {"ppl": math.e, "token": 20},
                                                          "perdente": {"ppl": 1.0, "token": 5}},
                                     "ignoto": {"vincente": {"ppl": 3}}}), encoding="utf-8")
            est = MP.carica_esterni([p], self.VOTI)
        t = est[MP.chiave_esterni(self.VOTI[0]["vincente"])]
        self.assertAlmostEqual(t["nll_token"], 1.0)
        self.assertGreater(t["token_per_parola"], 1)
        # un box senza tratti esterni: la differenza vale zero, il modello funziona lo stesso
        self.assertEqual(MP._diff_esterni("nuovo", "altro", ["nll_token"], est), [0.0])
        r = MP.valida(self.VOTI, ["nll_token"], est)
        self.assertEqual(r["n_tratti"], len(MP.TRATTI) + 1)
        self.assertEqual(len(r["esiti"]), 6)

    def test_mcnemar(self):
        self.assertEqual(MP.mcnemar_p([True, True, False], [True, False, True])[:2], (1, 1))
        self.assertAlmostEqual(MP.mcnemar_p([True] * 3, [True] * 3)[2], 1.0)
        self.assertLess(MP.mcnemar_p([False] * 10, [True] * 10)[2], 0.01)

    def test_varianti_senza_tratti_si_saltano(self):
        righe = MP.confronta_varianti(self.VOTI, {})
        self.assertEqual(righe[0]["variante"], "base")
        self.assertTrue(all("saltata" in r for r in righe[1:]))
        self.assertIn("saltata", MP.rapporto_varianti(righe))


def _rilievo(parola, gruppo="refusi", regola="MORFOLOGIK_RULE_IT_IT"):
    return {"regola": regola, "categoria": "TYPOS", "gruppo": gruppo, "parola": parola,
            "offset": 0, "messaggio": "", "contesto": parola}


class TestLanguageTool(unittest.TestCase):
    """Senza server: le chiamate di rete sono sostituite."""
    DIZ = {"thorik", "nanic", "nanico"}

    def test_gruppi(self):
        self.assertEqual(MP.lt_gruppo("MORFOLOGIK_RULE_IT_IT", "TYPOS"), "refusi")
        self.assertEqual(MP.lt_gruppo("ER_01_001", "CAT12"), "grammatica")
        self.assertEqual(MP.lt_gruppo("ST_03_001", "CAT10"), "stile")
        self.assertEqual(MP.lt_gruppo("ITALIAN_WORD_REPEAT_RULE", "MISC"), "ripetizioni")
        self.assertEqual(MP.lt_gruppo("UNPAIRED_BRACKETS", "PUNCTUATION"), "punteggiatura")

    def test_dizionario_e_flessioni(self):
        self.assertTrue(MP.nome_noto("Thorik", self.DIZ))
        self.assertTrue(MP.nome_noto("naniche", self.DIZ))
        self.assertFalse(MP.nome_noto("avalanga", self.DIZ))
        c = MP.conta_rilievi([_rilievo("Thorik"), _rilievo("avalanga"),
                              _rilievo("ad ogni", "stile", "ST_03_001")], self.DIZ)
        self.assertEqual((c["refusi_grezzi"], c["refusi"], c["stile"]), (2, 1, 1))

    def test_dizionario_del_glossario(self):
        with tempfile.TemporaryDirectory() as d:
            g = Path(d) / "G.md"
            g.write_text("| Italiano | Inglese |\n|---|---|\n| *Barbadiferro* | Ironbeard |\n", encoding="utf-8")
            vecchio = MP._DIZIONARIO
            MP._DIZIONARIO = None
            try:
                diz = MP.dizionario_nomi(g)
            finally:
                MP._DIZIONARIO = vecchio
        self.assertIn("barbadiferro", diz)
        self.assertIn("ironbeard", diz)

    def test_precisione_e_gruppi_affidabili(self):
        letti = ([{"gruppo": "grammatica", "vero": True}] * 5 + [{"gruppo": "grammatica", "vero": False}]
                 + [{"gruppo": "stile", "vero": True}]
                 + [{"gruppo": "refusi", "vero": False, "nome_noto": True}] * 4
                 + [{"gruppo": "refusi", "vero": None}])
        p = MP.precisione(letti)
        self.assertAlmostEqual(p["grammatica"]["precisione"], 5 / 6)
        self.assertNotIn("refusi", p)          # i nomi noti non contano, i non letti nemmeno
        self.assertEqual(MP.gruppi_affidabili(p), {"grammatica"})   # stile: un solo rilievo letto

    def test_campione_con_seme(self):
        ril = [_rilievo(w) for w in ("Thorik", "avalanga", "tump", "lisciva")] + \
              [_rilievo("a morsi", "grammatica", "ER_01_001")]
        a = MP.campione_rilievi(ril, 3, 7, self.DIZ)
        self.assertEqual(a, MP.campione_rilievi(ril, 3, 7, self.DIZ))
        self.assertEqual(a[0]["gruppo"], "grammatica")
        self.assertEqual(len(a), 3)
        self.assertNotIn("Thorik", [r["parola"] for r in a])
        self.assertTrue(all(r["vero"] is None for r in a))

    def test_filtro_scarta_chi_aggiunge_errori(self):
        finto = MP.ControlloLT("http://finto", {"grammatica"})
        vecchio = MP.lt_controlla
        MP.lt_controlla = lambda t, url=None: (
            [_rilievo("e", "grammatica", "X")] if "errore" in t else [])
        try:
            c = ORIGINALE.replace("Il vecchio alza", "Accanto all'incudine il vecchio alza") + " Un errore."
            motivi = MP.filtra(ORIGINALE, c, finto)
            self.assertIn("LanguageTool, 1 rilievi di grammatica in più", motivi)
            self.assertFalse(any("LanguageTool" in m for m in MP.filtra(ORIGINALE, ORIGINALE, finto)))
        finally:
            MP.lt_controlla = vecchio

    def test_senza_server_si_salta_ed_esce_zero(self):
        vecchio = MP.lt_versione
        MP.lt_versione = lambda url=None: None
        try:
            self.assertIsNone(MP.controllo_lt("http://finto"))
            self.assertEqual(MP.main(["languagetool", "--url", "http://finto"]), 0)
        finally:
            MP.lt_versione = vecchio

    def test_calibrazione_segno(self):
        voti = [{"pari": False, "vincente": f"v{i}", "perdente": f"p{i}"} for i in range(3)]
        conti = {}
        for i in range(3):
            conti[MP.chiave_esterni(f"v{i}")] = {**{g: 0 for g in MP.GRUPPI_LT}, "refusi_grezzi": 0}
            conti[MP.chiave_esterni(f"p{i}")] = {**{g: 1 for g in MP.GRUPPI_LT}, "refusi_grezzi": 1}
        s = {r["gruppo"]: r for r in MP.segno_per_gruppo(voti, conti)}
        self.assertEqual(s["grammatica"]["vincente_meno"], 3)
        self.assertEqual(s["grammatica"]["p_bonferroni"], min(1.0, s["grammatica"]["p"] * 6))


if __name__ == "__main__":
    unittest.main()
