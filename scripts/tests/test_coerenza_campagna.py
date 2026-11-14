"""coerenza_campagna.py — fronti e orologi, e fatti in contraddizione (lotto 7c).

I test usano archi finti in una cartella temporanea: i master veri cambiano
ogni settimana, e un test che dipende dal loro testo si rompe per la ragione
sbagliata. Fanno eccezione i due smoke sui dati di prova dell'esperimento, che
devono restare leggibili dallo schema.
"""
from __future__ import annotations

import copy
import shutil
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


STATE_FINTO = """
schema_version: 1
march_clock:
  giorno_corrente: 1
  giorno_arrivo: 42
party:
  - pg: Thorik
    hp: "−2 DES / +2 COS permanenti dal rito"
  - pg: Tordek
    hp: "nessun malus permanente"
artefatti:
  - artefatto: Aegis Fang (ascia)
    portatore: Thorik
echi:
  - id: E-01a
    stato: armato
    miccia: corta
  - id: E-01b
    stato: armato
    miccia: lunga
  - id: E-01c
    stato: esploso
    miccia: corta
conoscenze:
  - png: Sonjak
    sa_che: qualcosa
    come: spie
"""


class TestStoria(unittest.TestCase):
    """`fatti --state` (ADR-0125): ogni violazione ha regola, atteso, ha e file:riga."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.state = _scrivi(base, "state.yaml", STATE_FINTO)
        self.arco = base / "09_arco"
        self.an = cc.ancore_state(self.state)

    def tearDown(self):
        self.tmp.cleanup()

    def _viol(self, testo: str, regola: str) -> list[dict]:
        p = _scrivi(self.arco, "M.md", "# Modulo\n\n" + textwrap.dedent(testo).lstrip())
        r = cc.verifica_storia([p], self.an, [self.arco])
        return [v for v in r["violazioni"] if v["regola"].startswith(regola)]

    def test_ancore(self):
        self.assertEqual(self.an["giorno_arrivo"], 42)
        self.assertEqual(self.an["portatori"], {"Aegis Fang": "Thorik"})
        self.assertEqual(self.an["modifiche"], {"Thorik": {"DES": -2, "COS": 2}, "Tordek": {}})
        self.assertEqual([e["id"] for e in self.an["echi"]], ["E-01a", "E-01b"])

    def test_s1_arrivo_sbagliato(self):
        v = self._viol("- Day 39: l'orda della Mano Rossa arriva a Rethmar.\n", "S1")
        self.assertEqual(len(v), 1)
        self.assertEqual((v[0]["atteso"], v[0]["ha"], v[0]["riga"]), ("Giorno 42", "Giorno 39", 3))

    def test_s1_non_scatta(self):
        for riga in ("- Day 42: l'orda della Mano Rossa arriva a Rethmar.",
                     "Se la marcia rallenta, l'orda arriva a Rethmar al Giorno 44.",
                     "Giorno 2 dell'assedio: l'orda arriva a Rethmar con le macchine.",
                     "L'orda arriva a Rethmar al Day 40 → corretto in 42.",
                     "Finestra d'arrivo dell'orda a Rethmar: Giorno 38-41."):
            with self.subTest(riga=riga):
                self.assertEqual(self._viol(riga + "\n", "S1"), [])

    def test_s5_portatore(self):
        v = self._viol("Hella impugna Aegis Fang contro il drago.\n", "S5")
        self.assertEqual(len(v), 1)
        self.assertEqual((v[0]["atteso"], v[0]["ha"]), ("Aegis Fang: Thorik", "Hella"))
        self.assertEqual(self._viol("Thorik impugna Aegis Fang contro il drago.\n", "S5"), [])

    def test_s6_modifica_permanente(self):
        v = self._viol("Thorik paga −2 COS permanente.\n", "S6")
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0]["ha"], "COS −2")
        self.assertEqual(self._viol("Tordek ha −2 DES permanenti dal rito.\n", "S6")[0]["atteso"],
                         "Tordek: nessuna")
        for riga in ("Thorik: −2 DES / +2 COS permanenti.",
                     "Thorik e Tordek pagano −2 SAG permanente.",   # due PG: non si sa di chi
                     "Thorik paga −2 COS per un'ora."):             # non è permanente
            with self.subTest(riga=riga):
                self.assertEqual(self._viol(riga + "\n", "S6"), [])

    def test_s7_eco_armato_senza_scena(self):
        v = self._viol("Il seme di E-01a germoglia qui.\n", "S7")
        self.assertEqual([x["atteso"].split()[0] for x in v], ["E-01b"])
        self.assertEqual(v[0]["riga"], 0)

    def test_chi_sa_cosa_dichiarato_non_verificabile(self):
        p = _scrivi(self.arco, "M.md", "# M\n")
        r = cc.verifica_storia([p], self.an, [self.arco])
        self.assertEqual(r["non_verificabili"], {"chi sa cosa (conoscenze senza giorno)": "1 su 1"})

    def test_cli_fatti_state_json(self):
        import contextlib
        import io
        import json
        _scrivi(self.arco, "M.md", "# M\n\nHella impugna Aegis Fang.\n")
        buf = io.StringIO()
        vecchio = cc.STATE
        cc.STATE = self.state
        try:
            with contextlib.redirect_stdout(buf):
                rc = cc.main(["fatti", str(self.arco), "--state", "--json"])
        finally:
            cc.STATE = vecchio
        self.assertEqual(rc, 0)   # misura, non cancello
        storia = json.loads(buf.getvalue())["storia"]
        self.assertEqual(storia["regole"], ["S1", "S5", "S6", "S7", "T2"])
        self.assertTrue(any(v["regola"].startswith("S5") for v in storia["violazioni"]))

    def test_cli_legge_lo_state_indicato(self):
        """La CLI usa cc.STATE al momento della chiamata, non quello dell'import."""
        import contextlib
        import io
        import json
        altro = _scrivi(self.state.parent, "state-37.yaml", STATE_FINTO.replace("giorno_arrivo: 42",
                                                                                "giorno_arrivo: 37"))
        _scrivi(self.arco, "M.md", "# M\n\nL'orda arriva a Rethmar il Giorno 42.\n")
        buf = io.StringIO()
        vecchio = cc.STATE
        cc.STATE = altro
        try:
            with contextlib.redirect_stdout(buf):
                cc.main(["fatti", str(self.arco), "--state", "--json"])
        finally:
            cc.STATE = vecchio
        storia = json.loads(buf.getvalue())["storia"]
        self.assertEqual(storia["ancore"]["giorno_arrivo"], 37)
        self.assertEqual([(v["atteso"], v["ha"]) for v in storia["violazioni"] if v["regola"].startswith("S1")],
                         [("Giorno 37", "Giorno 42")])

    def test_t2_catena_rotta(self):
        def con(*righe):
            return dict(self.an, chi_sa=[dict(zip(("png_id", "dal_giorno", "informato_da", "indice"), r + (i,)))
                                         for i, r in enumerate(righe)])
        def t2(an):
            return [(v["atteso"], v["ha"]) for v in cc.verifica_storia([], an, [])["violazioni"]
                    if v["regola"].startswith("T2")]
        # chi informa lo sa prima: nessuna violazione
        self.assertEqual(t2(con(("capo", 21, None), ("agente", 23, "capo"))), [])
        # chi informa lo sa dopo
        self.assertEqual(t2(con(("capo", 25, None), ("agente", 23, "capo"))),
                         [("capo sa qualcosa entro il Giorno 23", "dal Giorno 25")])
        # chi informa non ha righe con un giorno
        self.assertEqual(t2(con(("capo", None, None), ("agente", 23, "capo"))),
                         [("capo sa qualcosa entro il Giorno 23", "nessuna riga con un giorno")])
        # limite dichiarato: il confronto è fra PNG, non fra fatti (basta una riga in tempo)
        self.assertEqual(t2(con(("capo", 0, None), ("capo", 30, None), ("agente", 23, "capo"))), [])
        # una riga senza giorno non si giudica
        self.assertEqual(t2(con(("capo", 25, None), ("agente", None, "capo"))), [])

    def test_state_vero_ha_i_giorni_e_nessuna_catena_rotta(self):
        an = cc.ancore_state()
        r = cc.verifica_storia([], an, [])
        self.assertEqual([v for v in r["violazioni"] if v["regola"].startswith("T2")], [])
        self.assertEqual(an["conoscenze_senza_tempo"], 6, "le righe di «chi sa cosa» senza giorno sono 6: i Tiri Kitor e le 5 che il DM non ha confermato")

    def test_s1_senza_giorno_arrivo_dichiarato(self):
        an = dict(self.an, giorno_arrivo=None)
        r = cc.verifica_storia([], an, [])
        self.assertIn("S1 arrivo dell'orda", r["non_verificabili"])
        self.assertNotIn("S1 arrivo dell'orda", cc.verifica_storia([], self.an, [])["non_verificabili"])


class TestTattiche(unittest.TestCase):
    """S8: un incantesimo o un talento che le «Tattiche» nominano e la scheda non ha."""

    SCHEDA = ("# Mago di prova\n\n**Talenti**: Attacco Poderoso, Incantare in Combattimento\n\n"
              "**Incantesimi preparati** (mago 5):\n- 3° — *palla di fuoco*, *velocità*\n"
              "- 1° — *dardo incantato*\n\n**Equipaggiamento** pozione di *invisibilità*\n\n"
              "**Tattiche**: {}\n\n**Morale**: fugge sotto 10 pf.\n")

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _viol(self, tattica, scheda=None):
        p = _scrivi(self.tmp, "mago.md", (scheda or self.SCHEDA).format(tattica))
        return cc.verifica_tattiche([p])

    def test_tattica_coerente(self):
        r = self._viol("apre con *palla di fuoco*, beve *invisibilità* e usa Attacco Poderoso.")
        self.assertEqual(r["violazioni"], [])
        self.assertEqual(r["letti"], {"schede": 1, "menzioni": 3})

    def test_incantesimo_che_la_scheda_non_ha(self):
        r = self._viol("apre con *fermare il tempo*, poi *palla di fuoco*.")
        self.assertEqual([(v["regola"], v["ha"], v["riga"]) for v in r["violazioni"]],
                         [("S8 tattica senza riscontro in scheda", "assente", 11)])
        self.assertIn("Time Stop", r["violazioni"][0]["atteso"])

    def test_talento_che_la_scheda_non_ha_anche_in_minuscolo(self):
        for forma in ("Tiro Multiplo", "tiro multiplo"):
            with self.subTest(forma=forma):
                r = self._viol(f"da lontano usa {forma}.")
                self.assertEqual(len(r["violazioni"]), 1)
                self.assertIn("Manyshot", r["violazioni"][0]["atteso"])

    def test_incantesimo_altrui_e_nota_del_dm_non_contano(self):
        r = self._viol("contro *fermare il tempo* si arrende.\n> era scritto *desiderio*.")
        self.assertEqual(r["violazioni"], [])

    def test_limiti_dichiarati(self):
        # senza corsivo l'incantesimo non si legge; un talento di una parola in minuscolo nemmeno
        self.assertEqual(self._viol("apre con fermare il tempo e poi usa mobilità.")["violazioni"], [])

    def test_file_con_due_schede_si_giudica_scheda_per_scheda(self):
        # il secondo blocco ha *fermare il tempo* e Schivare: non valgono per le tattiche del primo
        due = (self.SCHEDA + "\n# Secondo\n\n**Talenti**: Schivare\n\n"
               "**Incantesimi preparati** (mago 17):\n- 9° — *fermare il tempo*\n\n"
               "**Tattiche**: apre con *fermare il tempo* e resta in Schivare.\n")
        r = self._viol("apre con *fermare il tempo* e poi usa Schivare.", due)
        self.assertEqual([(v["riga"], v["atteso"].split(" (")[0]) for v in r["violazioni"]],
                         [(11, "fermare il tempo"), (11, "Schivare")])
        self.assertEqual(r["letti"]["schede"], 2)
        self.assertEqual(r["non_verificabili"], {})

    def test_blocco_senza_talenti_e_tattiche_fuori_blocco_restano_contati(self):
        testo = ("# Scena\n\n**Tattiche**: il gruppo usa Attacco Poderoso.\n\n" + self.SCHEDA.replace("# ", "## ")
                 + "\n## Gregario\n\n```statblocco\nnome: Gregario\n```\n\n"
                   "**Tattiche**: colpisce con Attacco Poderoso.\n")
        r = self._viol("usa Attacco Poderoso.", testo)
        self.assertEqual(r["violazioni"], [])
        self.assertEqual(r["non_verificabili"],
                         {"tattiche fuori da una scheda": 1, "blocchi senza riga Talenti": 1})

    def test_cli_tattiche_sul_bestiario_vero(self):
        import contextlib
        import io
        import json
        buf = io.StringIO()
        arco = _scrivi(self.tmp / "arco", "A.md", "# A\n").parent
        with contextlib.redirect_stdout(buf):
            self.assertEqual(cc.main(["fatti", str(arco), "--tattiche", "--json"]), 0)
        t = json.loads(buf.getvalue())["tattiche"]
        self.assertEqual(t["regole"], ["S8"])
        self.assertGreaterEqual(t["letti"]["schede"], 50)
        self.assertEqual(t["violazioni"], [], "una tattica del Bestiario nomina ciò che la scheda non ha")


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


if __name__ == "__main__":
    unittest.main()
