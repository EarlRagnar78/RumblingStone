"""coerenza_campagna.py — fronti e orologi, e fatti in contraddizione (lotto 7c).

I test usano archi finti in una cartella temporanea: i master veri cambiano
ogni settimana, e un test che dipende dal loro testo si rompe per la ragione
sbagliata. Fanno eccezione i due smoke sui dati di prova dell'esperimento, che
devono restare leggibili dallo schema.
"""
from __future__ import annotations

import copy
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import coerenza_campagna as cc  # noqa: E402

ESPERIMENTO = ROOT / "plans" / "esperimenti" / "qualita-misurabile-2026-10-22" / "coerenza"


def _scrivi(cartella: Path, nome: str, testo: str) -> Path:
    p = cartella / nome
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(testo).lstrip(), encoding="utf-8")
    return p


def _fronti_base() -> dict:
    return {
        "schema_version": 1,
        "arco": "ARC-99",
        "master": ["arco/M1.md"],
        "fronti": [{
            "id": "f1", "nome": "Il fronte", "tipo": "avventura",
            "impulso": {"testo": "prendere la rocca", "fonte": "arco/M1.md:1"},
            "pericoli": [
                {"nome": "Il drago", "impulso": "bruciare", "fonte": "arco/M1.md:2"},
                {"nome": "L'orda", "impulso": "assaltare", "fonte": None},
            ],
            "presagi": [{"testo": "il fumo", "chiavi": ["fumo nero"]}],
            "catastrofe": {"testo": "la rocca cade", "fonte": "arco/M1.md:3"},
            "domande": [{"testo": "Reggono?", "fonte": None}],
            "orologi": ["o1"],
        }],
        "orologi": [{
            "id": "o1", "nome": "L'assedio", "segmenti": 6, "riempiti": 2,
            "quando_si_riempie": {"testo": "breccia", "fonte": "arco/M1.md:3"},
            "fonte": "arco/M1.md:1",
        }],
    }


class TestFronti(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        _scrivi(self.root, "arco/M1.md", """
            L'orda vuole la rocca.
            Il drago brucia.
            Si alza un fumo nero dalle colline.
        """)

    def tearDown(self):
        self.tmp.cleanup()

    def regole(self, dati):
        return [v["regola"] for v in cc.controlla_fronti(dati, self.root)["violazioni"]]

    def test_fronte_conforme_passa_e_conta_i_dedotti(self):
        esito = cc.controlla_fronti(_fronti_base(), self.root)
        self.assertEqual(esito["violazioni"], [])
        self.assertEqual(esito["misure"]["campi_dedotti"], 2)       # un pericolo e la domanda
        self.assertEqual(esito["misure"]["presagi_nei_master"], 1)
        self.assertEqual(esito["presagi"][0]["trovato"], "arco/M1.md:3")

    def test_segmenti_fuori_da_4_6_8(self):
        d = _fronti_base()
        d["orologi"][0]["segmenti"] = 5
        self.assertIn("O1", self.regole(d))

    def test_riempiti_oltre_il_totale(self):
        d = _fronti_base()
        d["orologi"][0]["riempiti"] = 7
        self.assertEqual(self.regole(d), ["O2"])

    def test_orologio_in_ore_e_non_in_segmenti(self):
        d = _fronti_base()
        d["orologi"][0].update(segmenti=None, riempiti=None, unita="ore")
        self.assertEqual(sorted(self.regole(d)), ["O1", "O2"])

    def test_orologio_a_tempo_dichiarato_vale_con_qualsiasi_durata(self):
        # il March Clock: 42 giorni, non 4/6/8 tacche (decisione del DM, 2026-10-23)
        d = _fronti_base()
        d["orologi"][0].update(segmenti=42, riempiti=19, unita="giorni")
        self.assertEqual(self.regole(d), [])

    def test_senza_unita_i_segmenti_restano_4_6_8(self):
        d = _fronti_base()
        d["orologi"][0].update(segmenti=18, riempiti=9, unita=None)
        self.assertEqual(self.regole(d), ["O1"])

    def test_quando_si_riempie_e_obbligatorio(self):
        d = _fronti_base()
        del d["orologi"][0]["quando_si_riempie"]
        self.assertEqual(set(self.regole(d)), {"F0"})

    def test_un_pericolo_solo_e_troppo_poco(self):
        d = _fronti_base()
        d["fronti"][0]["pericoli"] = d["fronti"][0]["pericoli"][:1]
        self.assertEqual(self.regole(d), ["F1"])

    def test_presagi_di_campagna_ne_vogliono_tre(self):
        d = _fronti_base()
        d["fronti"][0]["tipo"] = "campagna"
        self.assertEqual(self.regole(d), ["F2"])

    def test_domande_da_una_a_tre(self):
        d = _fronti_base()
        d["fronti"][0]["domande"] = []
        self.assertEqual(self.regole(d), ["F3"])

    def test_presagio_che_nessun_master_scrive(self):
        d = _fronti_base()
        d["fronti"][0]["presagi"][0]["chiavi"] = ["corvi bianchi"]
        self.assertEqual(self.regole(d), ["F4"])

    def test_chiave_trovata_anche_col_grassetto_e_l_apostrofo_tipografico(self):
        _scrivi(self.root, "arco/M1.md", "Il **fumo** nero, e l’ombra.\n")
        self.assertEqual(cc.cerca_chiavi(["fumo nero", "l'ombra"], ["arco/M1.md"], self.root),
                         "arco/M1.md:1")

    def test_fonte_oltre_la_fine_del_file(self):
        d = _fronti_base()
        d["fronti"][0]["impulso"]["fonte"] = "arco/M1.md:99"
        self.assertEqual(self.regole(d), ["F5"])

    def test_orologio_citato_ma_non_dichiarato(self):
        d = _fronti_base()
        d["fronti"][0]["orologi"] = ["o1", "o2"]
        self.assertEqual(self.regole(d), ["F6"])

    def test_schema_rifiuta_un_tipo_sconosciuto(self):
        d = copy.deepcopy(_fronti_base())
        d["fronti"][0]["tipo"] = "dungeon"
        self.assertEqual(set(self.regole(d)), {"F0"})


class TestOrologiState(unittest.TestCase):
    def test_misura_gli_orologi_dei_villain(self):
        with tempfile.TemporaryDirectory() as t:
            p = _scrivi(Path(t), "state.yaml", """
                villain:
                - villain: A
                  png_id: a
                  clock: 3/8
                  trigger: succede
                - villain: B
                  png_id: b
                  clock: 9/18
                  trigger: succede
                - villain: C
                  png_id: c
                  clock: 'Trigger, non clock numerico'
                  trigger: succede
            """)
            esiti = {e["png_id"]: e for e in cc.misura_orologi_state(p)}
        self.assertTrue(esiti["a"]["conforme"])
        self.assertFalse(esiti["b"]["conforme"])
        self.assertIn("O1", esiti["b"]["motivo"])
        self.assertIsNone(esiti["c"]["segmenti"])


class TestEntita(unittest.TestCase):
    def test_chiave_toglie_titolo_numerazione_e_parentesi(self):
        self.assertEqual(cc.chiave_entita("**👑 RE THOREK HAMMERFIST (Nano Guerriero 15°/Nobile 2°, GS 16)**"),
                         ("thorek hammerfist", "re"))
        self.assertEqual(cc.chiave_entita("A.5 · Madre Superiora Dana Forgiapietra (Scene 2-3)"),
                         ("dana forgiapietra", "madre superiora"))

    def test_i_titoli_di_sezione_non_sono_entita(self):
        for t in ("Tattiche di Terros — regia", "SCENA 3 — La foresta", "Round 1-2: la preparazione"):
            self.assertEqual(cc.chiave_entita(t), (None, None), t)

    def test_classi_solo_parole_di_classe(self):
        self.assertEqual(cc.classi_da_paren("Nano Guerriero 15°/Nobile 2°, GS 16"), "guerriero 15/nobile 2")
        self.assertEqual(cc.classi_da_paren("Raffica +12/+12/+7: BAB +10 con monaco 9 e guerriero 4"),
                         "guerriero 4/monaco 9")
        self.assertIsNone(cc.classi_da_paren("APL 13, CA 28, Aegis Fang +21"))


class TestFatti(unittest.TestCase):
    """Un arco finto con contraddizioni piantate, e con trappole che NON lo sono."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.a = base / "arcoA"
        self.b = base / "arcoB"
        _scrivi(self.a, "M1.md", """
            # Modulo

            ### **GORAK IL ROSSO (Orco Barbaro 9°, GS 9)**
            **CA:** 22
            **PF:** 120
            **TS:** Tempra +10, Riflessi +4, Volontà +3
            *   **Ruggito (Str):** cono di 9 m, Volontà CD 17 o scosso.

            ## Note
            Gorak il Rosso è morto nella frana. Brilla l'Aegis Fang di Thorik.
            **Mastro Ulla Pietrafonda** (Nana Esperto 6, GS 5) tiene la fucina.
        """)
        _scrivi(self.b, "M2.md", """
            # Altro modulo

            ### GORAK IL ROSSO
            ```
            ===========================
               GORAK IL ROSSO — capoclan (GS 10)
            ===========================
            PF: 130 (9d12+40) · CA 22
            TS Temp +10, Rifl +4, Vol +3
            ```

            ### Gorak il Rosso, versione ferita
            **PF:** 60

            Prima della correzione Gorak aveva PF 99 → oggi 120.
            Se Gorak il Rosso sopravvive, torna in ARC-10.
            Gorak il Rosso è vivo e regna sulle colline.
            **Capitano Ulla Pietrafonda** guida la ronda.
            La Corona di Adamantio di Thorik brilla; Tordek impugna l'Aegis Fang.
            La Corona di Adamantio sulla fronte di Thorik si scalda.

            | Chi | pf | CA |
            |---|---|---|
            | Gorak il Rosso | 120 | 23 |
        """)

    def tearDown(self):
        self.tmp.cleanup()

    def rileva(self):
        r = cc.rileva_contraddizioni([self.a, self.b])
        return {(c["chiave"], c["attributo"]): {v["valore"] for v in c["valori"]}
                for c in r["contraddizioni"]}, r

    def test_trova_le_contraddizioni_piantate(self):
        c, _ = self.rileva()
        self.assertEqual(c[("gorak il rosso", "GS")], {"9", "10"})
        self.assertEqual(c[("gorak il rosso", "pf")], {"120", "130"})
        self.assertEqual(c[("gorak il rosso", "CA")], {"22", "23"})
        self.assertEqual(c[("gorak il rosso", "vivo/morto")], {"morto", "vivo"})
        self.assertEqual(c[("ulla pietrafonda", "titolo")], {"mastro", "capitano"})
        self.assertEqual(c[("aegis fang", "portatore")], {"Thorik", "Tordek"})

    def test_dice_file_e_riga_di_entrambe(self):
        _, r = self.rileva()
        gs = next(x for x in r["contraddizioni"] if x["chiave"] == "gorak il rosso" and x["attributo"] == "GS")
        dove = {(o["file"].rsplit("/", 1)[-1], o["riga"]) for v in gs["valori"] for o in v["occorrenze"]}
        self.assertIn(("M1.md", 3), dove)
        self.assertIn(("M2.md", 6), dove)

    def test_le_trappole_non_diventano_valori(self):
        c, r = self.rileva()
        pf = c[("gorak il rosso", "pf")]
        self.assertNotIn("60", pf)          # blocco «versione ferita»: variante
        self.assertNotIn("99", pf)          # riga di storico (→, «prima della correzione»)
        self.assertNotIn(("gorak il rosso", "TS"), c)          # stessi TS in due formati
        self.assertNotIn(("corona di adamantio", "portatore"), c)   # Thorik in tutte e due

    def test_un_valore_solo_non_e_una_contraddizione(self):
        _scrivi(self.b, "M2.md", "### GORAK IL ROSSO (GS 9)\n**PF:** 120\n")
        c, _ = self.rileva()
        self.assertNotIn(("gorak il rosso", "GS"), c)
        self.assertNotIn(("gorak il rosso", "pf"), c)

    def test_i_file_fuori_perimetro_si_saltano(self):
        _scrivi(self.b, "ERRATA-ARC99.md", "### GORAK IL ROSSO (GS 3)\n")
        _scrivi(self.b, "_ARCHIVIO/vecchio.md", "### GORAK IL ROSSO (GS 2)\n")
        c, r = self.rileva()
        self.assertEqual(c[("gorak il rosso", "GS")], {"9", "10"})
        self.assertFalse(any("ERRATA" in f or "_ARCHIVIO" in f for f in r["file_letti"]))


class TestAlias(unittest.TestCase):
    def test_alias_breve_solo_se_unico_e_nome_proprio(self):
        chiavi = {"terros l'antico", "fauci di palude", "fauci di diamante", "goblin worg riders"}
        testi = ["Terros 345 pf. Un goblin scappa. Fauci di Diamante."]
        self.assertEqual(cc.alias_brevi(chiavi, testi), {"terros": "terros l'antico"})


class TestDatiDiProva(unittest.TestCase):
    """I dati dell'esperimento restano leggibili dallo schema (niente F0)."""

    def test_fronti_dell_esperimento_rispettano_lo_schema(self):
        import yaml
        for p in sorted(ESPERIMENTO.glob("fronti-*.yaml")):
            esito = cc.controlla_fronti(yaml.safe_load(p.read_text(encoding="utf-8")))
            regole = {v["regola"] for v in esito["violazioni"]}
            self.assertNotIn("F0", regole, p.name)
            self.assertNotIn("F5", regole, p.name)


if __name__ == "__main__":
    unittest.main()


class TestResidui(unittest.TestCase):
    """Il cancello di CI: una contraddizione nuova blocca, un residuo risolto
    va tolto dal file."""

    R = {"contraddizioni": [{"entita": "Orog", "chiave": "orog", "attributo": "GS",
                             "valori": [{"valore": "6"}, {"valore": "7"}]}]}

    def _residui(self, righe):
        d = Path(tempfile.mkdtemp())
        p = d / "residui.json"
        p.write_text(__import__("json").dumps({"residui": righe}), encoding="utf-8")
        return p

    def test_dichiarata_passa(self):
        p = self._residui([{"chiave": "orog", "attributo": "GS", "ragione": "x"}])
        self.assertEqual(cc.controlla_residui(self.R, p), 0)

    def test_nuova_blocca(self):
        self.assertEqual(cc.controlla_residui(self.R, self._residui([])), 1)

    def test_residuo_risolto_blocca(self):
        p = self._residui([{"chiave": "orog", "attributo": "GS", "ragione": "x"},
                           {"chiave": "hobgoblin", "attributo": "CA", "ragione": "y"}])
        self.assertEqual(cc.controlla_residui(self.R, p), 1)
