"""Lo stato di campagna come dato — lotto 4d-1 (ADR-0050, 2026-09-16).

Le tabelle di `campaign/state.md` sono generate da `campaign/state.yaml`. Il
criterio d'uscita del lotto e' uno solo e non e' negoziabile: **il file
rigenerato deve tornare byte-identico a quello committato**. E' cio' che rende
sicuro un refactor che tocca il canone — senza, resterebbe «fidatevi, ho
trascritto 99 righe giuste».

🔴 **I dati NON vengono dalla PR #99.** Quel ramo e' fermo al 10 agosto ed e'
384 commit indietro: il suo `state.yaml` non conosce D3, D4, D11, D13, i Tre
Doni, la Collana ne' i due tempi di 4c. Portarlo avrebbe annullato cinque
settimane di canone in silenzio. Del ramo si e' recuperata la **macchina**; i
valori sono stati estratti da `state.md` di oggi.

⚠️ **Cosa questo file NON copre, e dove sta.** Lo split dello storico in
`state-changelog.md` e la via di scrittura (`state_apply`, il front-matter dei
log di sessione) sono il lotto **4d-2**. La #99 ha registrato li' una
regressione propria — *«lo split dello storico aveva rotto `state_apply
--migrate`; la CI non l'aveva vista perche' quei test girano su fixture»* — e i
suoi test **sui file veri** si portano insieme a quella modifica, non prima.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

STATE_YAML = ROOT / "campaign" / "state.yaml"
STATE_MD = ROOT / "campaign" / "state.md"

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _dati() -> dict:
    return yaml.safe_load(STATE_YAML.read_text(encoding="utf-8"))


@unittest.skipIf(yaml is None, "pyyaml non installato")
class TestIlFileSiRigeneraIdentico(unittest.TestCase):
    """Il criterio d'uscita. Tutto il resto vale solo se questo passa."""

    def test_render_state_check_e_verde(self):
        esito = subprocess.run([sys.executable, "scripts/render_state.py", "--check"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr + esito.stdout)

    def test_rigenerare_non_scrive_niente(self):
        """Idempotenza: due esecuzioni di fila non muovono un byte."""
        prima = STATE_MD.read_bytes()
        subprocess.run([sys.executable, "scripts/render_state.py"],
                       cwd=ROOT, capture_output=True, check=False)
        self.assertEqual(STATE_MD.read_bytes(), prima)

    def test_il_gate_morde(self):
        """Provato a rovescio: senza questo, i due test sopra non provano nulla.

        Si lavora su una copia: rompere il file vero per provare un test
        sarebbe il modo piu' rapido di perdere canone.
        """
        import render_state as rs
        d = _dati()
        d["archi"][0]["stato"] = "un valore che nessuno ha scritto"
        reso = rs.rendi("archi", d)
        self.assertIn("un valore che nessuno ha scritto", reso)
        self.assertNotIn("un valore che nessuno ha scritto",
                         STATE_MD.read_text(encoding="utf-8"),
                         "il file vero non deve essere stato toccato")


@unittest.skipIf(yaml is None, "pyyaml non installato")
class TestNessunaPerditaDiCanone(unittest.TestCase):
    """Contato nei DUE sensi: nessuna riga sparisce, nessuna compare dal nulla."""

    ATTESI = {"archi": 22, "party": 4, "artefatti": 8, "echi": 7,
              "villain": 13, "conoscenze": 31,
              "difensori_rethmar": 9, "scenari_rethmar": 5}

    def test_ogni_sezione_ha_i_record_che_aveva_la_tabella(self):
        d = _dati()
        for nome, atteso in self.ATTESI.items():
            self.assertEqual(len(d[nome]), atteso, nome)

    def test_ogni_record_diventa_una_riga_e_viceversa(self):
        import render_state as rs
        d = _dati()
        for regione, spec in rs.TABELLE.items():
            righe = [r for r in rs.rendi(regione, d).splitlines()
                     if r.startswith("| ") and not r.startswith("|--")]
            atteso = len(d[spec["chiave"]])
            self.assertEqual(len(righe) - 1, atteso,
                             f"{regione}: {len(righe)-1} righe per {atteso} record")

    def test_le_ancore_del_canone_di_oggi_sopravvivono(self):
        """Frasi che devono restare leggibili nel markdown reso.

        ⚠️ Le ancore della #99 erano **invecchiate**: cercavano «MORTA» in
        maiuscolo, e il canone di oggi scrive «🔴 **morta**». Un'ancora e' una
        citazione del canone, quindi invecchia col canone: queste vengono da
        `state.md` del 2026-09-16 e vanno riviste quando quelle righe cambiano.
        """
        import render_state as rs
        d = _dati()
        ancore = {
            "party": ["morta", "Nessun −2 COS", "Ancoraggio della Montagna",
                      "Rovo Eldritch"],
            "archi": ["Portale della Forgia Eterna", "NON giocato"],
            "artefatti": ["Aegis Fang"],
            "echi": ["E-07c", "E-07e"],
        }
        for regione, frasi in ancore.items():
            reso = rs.rendi(regione, d)
            for frase in frasi:
                self.assertIn(frase, reso, f"«{frase}» persa in {regione}")


@unittest.skipIf(yaml is None, "pyyaml non installato")
class TestIlTempoNonDichiaratoSiConta(unittest.TestCase):
    """R7 — il cuore onesto del lotto.

    ADR-0050 prometteva che «un fatto senza tempo dichiarato non e'
    esprimibile». Misurando si e' scoperto che il canone non lo dichiara
    ovunque: §3, §4 e le due tabelle di Rethmar **non hanno una colonna
    Tempo**, e il generatore della #99 ne aggiungeva una che il lotto 4c ha
    superato cinque settimane dopo.

    Dedurre un tempo riga per riga sarebbe inventare canone in un lotto di
    infrastruttura. Quindi il campo e' opzionale li', e il buco si **conta**:
    un numero che si vede non cresce in silenzio.
    """

    def test_il_conteggio_e_quello_misurato(self):
        import validate_state as vs
        buchi = vs.righe_senza_tempo(_dati())
        self.assertEqual(buchi, {"villain": 13, "conoscenze": 31,
                                 "difensori_rethmar": 9, "scenari_rethmar": 5})
        self.assertEqual(sum(buchi.values()), 58)

    def test_dove_il_canone_il_tempo_lo_dichiara_e_obbligatorio(self):
        """Gli archi ce l'hanno per riga, e li' non si deroga."""
        d = _dati()
        for a in d["archi"]:
            self.assertIn(a["tempo"],
                          ("giocato", "in_corso", "preparato", "fallito", "sospeso"),
                          a["arco"])

    def test_i_due_tempi_di_party_e_artefatti_sono_due_colonne(self):
        """L'altra forma in cui il canone dichiara il tempo, e va riconosciuta."""
        d = _dati()
        for rec in d["party"]:
            self.assertIn("oggi", rec, rec["pg"])
            self.assertIn("preparato", rec, rec["pg"])
        for rec in d["artefatti"]:
            self.assertIn("oggi", rec, rec["artefatto"])

    def test_il_conteggio_reagisce(self):
        import validate_state as vs
        d = _dati()
        d["villain"][0]["tempo"] = "preparato"
        self.assertEqual(vs.righe_senza_tempo(d)["villain"], 12)


@unittest.skipIf(yaml is None, "pyyaml non installato")
class TestEchoLedgerDati(unittest.TestCase):
    """Un'eco registra una SCELTA: l'autore e' un campo, non una stringa."""

    def test_l_autore_e_un_campo_a_se(self):
        """E' la falla del 2026-08-06, chiusa nella forma del dato.

        Con autore, data e scelta in una stringa sola, *rovesciare* un'eco su
        un altro PG era una modifica di testo. Adesso e' una modifica di dato,
        e lo schema puo' pretenderla.
        """
        for e in _dati()["echi"]:
            self.assertTrue(e.get("autore"), e["id"])
            self.assertTrue(e.get("data"), e["id"])

    def test_gli_id_non_si_riusano_e_l_annullata_resta(self):
        echi = _dati()["echi"]
        ids = [e["id"] for e in echi]
        self.assertEqual(len(ids), len(set(ids)), "un ID di eco e' stato riusato")
        annullate = [e for e in echi if e["stato"].startswith("annullat")]
        self.assertTrue(annullate, "E-07e deve restare in tabella, col perche'")
        for e in annullate:
            self.assertIn("nnullata", e["fatto"] + (e.get("payoff") or ""),
                          f"{e['id']}: un'eco annullata deve dire perche'")

    def test_il_genere_incoerente_e_dichiarato_non_normalizzato(self):
        """🔫 armato (maschile) e ✖ annullata (femminile) convivono nel canone.

        E' un'incoerenza vera, di UNA parola, e non si chiude riscrivendo il
        canone dentro un lotto di infrastruttura: lo schema accetta entrambi e
        la questione va al DM. Questo test esiste perche' il giorno in cui
        qualcuno decide, sia lui a toglierlo.
        """
        schema = json.loads(
            (ROOT / "scripts" / "schemas" / "campaign_state.schema.json")
            .read_text(encoding="utf-8"))
        enum = schema["properties"]["echi"]["items"]["properties"]["stato"]["enum"]
        self.assertIn("annullato", enum)
        self.assertIn("annullata", enum)

    def test_il_coautore_si_ricompone_alla_lettera(self):
        """E-07f ha due mani: la vista deve dirlo, e dirlo com'era scritto."""
        import render_state as rs
        d = _dati()
        con_coautore = [e for e in d["echi"] if e.get("coautore")]
        self.assertTrue(con_coautore, "E-07f porta Hella dall'altra parte")
        reso = rs.rendi("echi", d)
        for e in con_coautore:
            self.assertIn(f"*(e **{e['coautore']}**, dall'altra parte)*", reso)


@unittest.skipIf(yaml is None, "pyyaml non installato")
class TestLaVistaNonHaCambiatoForma(unittest.TestCase):
    """Le intestazioni sono quelle che il DM legge oggi, non quelle del ramo.

    🔎 Il generatore della #99 emetteva una forma DIVERSA: colonna `Tempo` in
    §3 e §4, intestazioni italiane in §1 e §6. Era del 10 agosto, mentre il
    lotto 4c ha ridisegnato quelle sezioni il 12 settembre. Adottarla avrebbe
    riportato indietro la presentazione del canone di cinque settimane —
    esattamente come portare i dati del ramo avrebbe riportato indietro i fatti.
    """

    def test_ogni_intestazione_e_quella_del_file_vero(self):
        import render_state as rs
        md = STATE_MD.read_text(encoding="utf-8")
        for regione, spec in rs.TABELLE.items():
            self.assertIn(spec["intestazione"], md,
                          f"{regione}: l'intestazione dichiarata non e' nel file")
            self.assertIn(spec["separatore"], md, regione)

    def test_le_otto_regioni_sono_marcate(self):
        import render_state as rs
        md = STATE_MD.read_text(encoding="utf-8")
        for regione in rs.TABELLE:
            self.assertIn(f"<!-- gen:state:{regione} -->", md)
            self.assertIn(f"<!-- /gen:state:{regione} -->", md)

    def test_la_prosa_resta_fuori(self):
        """§5 e §7 non hanno una regione, ed e' una scelta dichiarata."""
        import render_state as rs
        self.assertNotIn("promesse", rs.TABELLE)
        self.assertNotIn("fili", rs.TABELLE)
        md = STATE_MD.read_text(encoding="utf-8")
        self.assertIn("| Owed by | Owed to | What | Consequence if broken |", md,
                      "§5 deve restare markdown scritto a mano")


@unittest.skipIf(yaml is None, "pyyaml non installato")
class TestLoSchemaMorde(unittest.TestCase):
    def test_il_file_vero_e_valido(self):
        esito = subprocess.run([sys.executable, "scripts/validate_state.py"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_un_arco_senza_tempo_e_invalido(self):
        import validate_state as vs
        schema = json.loads(
            (ROOT / "scripts" / "schemas" / "campaign_state.schema.json")
            .read_text(encoding="utf-8"))
        d = _dati()
        del d["archi"][0]["tempo"]
        errs = vs.validate_schema(d, schema)
        self.assertTrue(any("tempo" in e for e in errs),
                        "un arco senza tempo dichiarato deve essere invalido")


if __name__ == "__main__":
    unittest.main()
