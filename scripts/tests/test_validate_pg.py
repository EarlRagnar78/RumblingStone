"""Test per validate_pg.py e render_pg.py (PR #99 lotto G14, ripresi dal lotto 4g-1).

Il test che vale tutti gli altri è `test_riprodurrebbe_il_difetto_originale`:
toglie dalla scheda di Thorik il −2 DES della Corona e pretende che il gate se
ne accorga. Se un giorno smette di accorgersene, il gate è decorativo, ed è
esattamente il difetto che è rimasto invisibile per tre generazioni di schede.

Nessun test scrive nel repo: le mutazioni si fanno su copie in memoria.
"""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import render_pg as rp  # noqa: E402
import validate_pg as vp  # noqa: E402

PG = ["Thorik", "Tordek", "Hella", "Artemis"]


class TestIlRepoEPulito(unittest.TestCase):
    def test_il_gate_passa(self):
        self.assertEqual(vp.main([]), 0)

    def test_le_viste_sono_allineate(self):
        self.assertEqual(rp.main(["--check"]), 0)

    def test_una_scheda_per_ogni_pg_di_party(self):
        nomi = {d["pg"] for d in vp.schede().values()}
        self.assertEqual(nomi, set(vp.pg_di_party()),
                         "un PG senza scheda è un PG i cui costi possono sparire")


class TestUnPostoSolo(unittest.TestCase):
    """Controllo 5: classe, PF, stato e artefatti sono di state.yaml."""

    def test_una_chiave_di_state_yaml_e_rifiutata(self):
        for chiave in ("classe", "hp", "stato", "artefatti"):
            t = copy.deepcopy(vp.schede()["tordek"])
            t[chiave] = "Dwarf Fighter 4 / Monk 9"
            problemi = vp.valida_schema(t, "tordek")
            self.assertTrue(any(f"`{chiave}`" in p and "state.yaml" in p for p in problemi),
                            f"`{chiave}` copiata sulla scheda e il gate tace: {problemi}")

    def test_una_chiave_sconosciuta_e_rifiutata(self):
        t = copy.deepcopy(vp.schede()["tordek"])
        t["livello_epico"] = 1
        self.assertTrue(vp.valida_schema(t, "tordek"))

    def test_un_pg_senza_scheda_e_visto(self):
        tutte = copy.deepcopy(vp.schede())
        del tutte["hella"]
        self.assertTrue(any("Hella" in p for p in vp.verifica_party(tutte)))

    def test_il_gate_boccia_un_pg_senza_scheda(self):
        """Non basta che la funzione lo veda: il gate deve uscire 1."""
        tutte = copy.deepcopy(vp.schede())
        del tutte["hella"]
        with mock.patch.object(vp, "schede", return_value=tutte):
            self.assertEqual(vp.main([]), 1)

    def test_una_scheda_di_un_pg_che_non_esiste_e_vista(self):
        tutte = copy.deepcopy(vp.schede())
        tutte["regdar"] = dict(tutte["tordek"], pg="Regdar")
        self.assertTrue(any("Regdar" in p for p in vp.verifica_party(tutte)))

    def test_una_caratteristica_inventata_e_vista(self):
        t = copy.deepcopy(vp.schede()["thorik"])
        t["modificatori_permanenti"][0]["caratteristica"] = "FORTUNA"
        self.assertTrue(vp.valida_schema(t, "thorik"))


class TestFontiEAritmetica(unittest.TestCase):
    def test_ogni_modificatore_ha_una_fonte_apribile(self):
        for nome, dati in vp.schede().items():
            for mod in dati.get("modificatori_permanenti") or []:
                self.assertTrue((ROOT / mod["fonte"]).exists(),
                                f"{nome}: fonte inesistente {mod['fonte']}")

    def test_una_fonte_inesistente_e_vista(self):
        t = copy.deepcopy(vp.schede()["thorik"])
        t["modificatori_permanenti"][0]["fonte"] = "07_il Portale Della Forgia Eterna/NON-ESISTE.md"
        self.assertTrue(vp.valida_schema(t, "thorik"))

    def test_la_catena_della_des_di_thorik_torna(self):
        """10 base → 8 (Corona indossata) → 6 (rito dello Smeraldo)."""
        t = vp.schede()["thorik"]
        des = t["caratteristiche"]["des"]
        self.assertEqual((des["base"], des["attuale"]), (10, 6))
        self.assertEqual(vp.valida_aritmetica(t, "thorik"), [])

    def test_il_car_di_thorik_conta_il_quattro_una_volta(self):
        """P1 e DEF-1 scrivono lo stesso +4 CAR: 8 → 12, non 16 (canone giocato)."""
        t = copy.deepcopy(vp.schede()["thorik"])
        car = t["caratteristiche"]["car"]
        self.assertEqual((car["base"], car["attuale"]), (8, 12))
        t["modificatori_permanenti"].append(dict(
            t["modificatori_permanenti"][-1], causa="Corona indossata, P1"))
        self.assertTrue(vp.valida_aritmetica(t, "thorik"),
                        "un secondo +4 CAR e il gate tace: il CAR diventerebbe 16")

    def test_aritmetica_sbagliata_viene_vista(self):
        t = copy.deepcopy(vp.schede()["thorik"])
        t["caratteristiche"]["des"]["attuale"] = 8
        self.assertTrue(vp.valida_aritmetica(t, "x"))

    def test_meta_conto_e_un_errore(self):
        """base senza attuale sembra un dato e non lo è."""
        t = copy.deepcopy(vp.schede()["thorik"])
        t["caratteristiche"]["des"]["attuale"] = None
        self.assertTrue(vp.valida_aritmetica(t, "x"))

    def test_delta_noto_senza_valori_e_lecito(self):
        """«+2 COS permanenti» senza dire da quale COS si parte: resta [INFERRED]."""
        t = vp.schede()["thorik"]
        self.assertIsNone(t["caratteristiche"]["cos"]["base"])
        self.assertNotIn("COS", " ".join(vp.valida_aritmetica(t, "thorik")))

    def test_una_citazione_che_non_ce_piu_e_vista(self):
        tutte = copy.deepcopy(vp.schede())
        tutte["thorik"]["modificatori_permanenti"][0]["cita"] = "una frase che il modulo non dice"
        self.assertTrue(vp.verifica_fonti_primarie(tutte, PG))


class TestDeriva(unittest.TestCase):
    """Il gate deve trovare i costi affermati nei documenti e assenti dalle schede."""

    def test_riprodurrebbe_il_difetto_originale(self):
        """Tolto il −2 DES della **Corona**, il gate deve accorgersene.

        Thorik ha DUE −2 DES (Corona indossata e rito), e il confronto per
        *tipo* resterebbe soddisfatto dall'altro. Solo la fonte distingue i due.
        """
        tutte = copy.deepcopy(vp.schede())
        tutte["thorik"]["modificatori_permanenti"] = [
            m for m in tutte["thorik"]["modificatori_permanenti"]
            if not (m["caratteristica"] == "DES" and "Corona" in m["causa"])]
        problemi = vp.verifica_fonti_primarie(tutte, PG)
        self.assertTrue(any("Thorik" in x and "DES" in x for x in problemi),
                        f"il −2 DES della Corona sparisce e il gate tace: {problemi}")

    def test_sparizione_totale_vista_dal_controllo_per_tipo(self):
        """Il difetto storico era l'assenza TOTALE: nessuna scheda, nessun DES."""
        trovate = vp.scansiona_deriva(PG)
        self.assertTrue(any(k[0] == "Thorik" and k[2] == "DES" for k in trovate))

    def test_il_totale_e_coperto_dai_singoli(self):
        """«−4 DES permanenti» è la somma dei due −2: non è una deriva."""
        trovate = vp.scansiona_deriva(PG)
        self.assertIn(("Thorik", -4, "DES"), trovate)
        self.assertEqual(vp.main([]), 0)

    def test_una_negazione_non_afferma_il_costo(self):
        """«Nessun −2 COS» dice che il costo NON c'è."""
        self.assertTrue(vp.NEGAZIONE.search("**Nessun "))
        self.assertTrue(vp.NEGAZIONE.search("⚠️ nessun **"))
        self.assertFalse(vp.NEGAZIONE.search("Thorik perde "))
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("- **Thorik**: ⚠️ **Nessun −2 COS** permanente.\n"
                         "- **Thorik**: −2 DES permanenti.\n", encoding="utf-8")
            self.assertEqual(vp.scansiona_file(f, PG), {("Thorik", -2, "DES")})

    def test_le_fonti_primarie_esistono_e_dicono_cosa_stabiliscono(self):
        for voce in vp.fonti_primarie():
            self.assertTrue((ROOT / voce["file"]).exists(), f"inesistente: {voce['file']}")
            self.assertTrue(voce.get("attesta"), f"{voce['file']} non dice cosa stabilisce")
            self.assertTrue(voce.get("cosa"), f"{voce['file']} senza spiegazione")

    def test_ogni_dismissione_porta_una_ragione(self):
        """Dismettere in silenzio sarebbe il difetto originale con un file in più."""
        for chiave, ragione in vp.dismissioni().items():
            self.assertGreater(len(ragione.strip()), 40,
                               f"dismissione {chiave} senza una ragione vera")


class TestVista(unittest.TestCase):
    def test_la_vista_mostra_la_catena(self):
        md = rp.rendi(vp.schede()["thorik"])
        self.assertIn("10 → **8**", md)
        self.assertIn("**6**", md)

    def test_il_check_vede_una_vista_rimasta_indietro(self):
        """Se i dati cambiano e il .md no, `--check` esce 1 (senza scrivere niente)."""
        vero = rp.rendi
        with mock.patch.object(rp, "rendi", lambda d: vero(d) + "riga nuova\n"):
            self.assertEqual(rp.main(["--check"]), 1)

    def test_la_vista_rimanda_a_state_yaml_invece_di_copiare(self):
        md = rp.rendi(vp.schede()["tordek"])
        self.assertIn("campaign/state.yaml", md)
        self.assertNotIn("Monk", md)


if __name__ == "__main__":
    unittest.main()
