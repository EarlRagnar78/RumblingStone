"""La chiave fra lo stato vivo e il Bestiario — lotto 4d-4, decisione D17.

🔴 **Perche' la chiave e' dichiarata e non dedotta.** Prima di questa sezione,
chi partiva da `state.yaml` per arrivare alla scheda di un PNG doveva
confrontare stringhe. Misurato sul repo: **11 villain su 13** e **23 righe di §4
su 31** si agganciavano; il resto no.

E allentare il confronto **peggiorava** le risposte invece di migliorarle:

| Nome in `state.yaml` | Cosa aggancia un matcher permissivo |
|---|---|
| `Zalkatar (Illithid Warlock)` | `Xal_thor` **o** `Zarim` — due illithid diversi |
| `Wyrmlord Saarvith + Regiarix` | `Wyrmlord_Karruk` — un altro wyrmlord |
| `Zalkatar (via Sethrax)` | `Sethrax_il_Velato` — ma chi *sa* e' Zalkatar |
| `Druid Circle of the Sacred Forest` | `druid-bear-ally-cr12.md` — l'orso alleato |

Trasformare «non lo so» in un errore sicuro di se' e' il modo in cui un LLM
sbaglia, ed e' peggio del silenzio. La chiave dichiarata dice «non c'e'» dove
non c'e'.

I test girano sui **file veri**: `scheda` e' un percorso, e un percorso si prova
solo contro il filesystem.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_state as vs  # noqa: E402

import yaml  # noqa: E402

DATI = yaml.safe_load((ROOT / "campaign" / "state.yaml").read_text(encoding="utf-8"))


class TestLAnagraficaEsisteEdECoerente(unittest.TestCase):
    def test_c_e_una_voce_per_ogni_persona_nominata(self):
        """Nessuna riga di §3 o §4 resta senza una casa dichiarata."""
        noti = {r["id"] for r in DATI["png"]}
        for sez in vs.CON_PNG_ID:
            for i, r in enumerate(DATI[sez]):
                with self.subTest(sezione=sez, riga=i):
                    self.assertIn(r.get("png_id"), noti)

    def test_gli_id_sono_unici(self):
        ids = [r["id"] for r in DATI["png"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_ogni_scheda_dichiarata_esiste_davvero(self):
        """🔴 R11 e' cio' che rende la chiave una chiave.

        Senza questa prova, `scheda` sarebbe una stringa plausibile — la stessa
        cosa di prima, scritta meglio.
        """
        for r in DATI["png"]:
            if r["scheda"]:
                with self.subTest(png=r["id"]):
                    self.assertTrue((ROOT / r["scheda"]).exists(), r["scheda"])

    def test_ogni_buco_dichiara_il_proprio_perche(self):
        for r in DATI["png"]:
            if r["scheda"] is None:
                with self.subTest(png=r["id"]):
                    self.assertTrue(r.get("perche_senza_scheda"),
                                    f"{r['id']}: buco senza motivo scritto")

    def test_solo_le_persone_possono_avere_uno_stato_vivo(self):
        """Il motivo per cui §4 non poteva portare `stato` (ADR-0052).

        Tre righe di §4 non sono persone: il Cerchio Druidico, la coppia
        Lathander + Mask, i Tiri Kitor. L'anagrafica lo dichiara col `tipo`
        invece di lasciarlo capire a chi legge.
        """
        tipi = {r["tipo"] for r in DATI["png"]}
        self.assertEqual(tipi, {"persona", "gruppo", "divinita"})
        non_persone = [r["id"] for r in DATI["png"] if r["tipo"] != "persona"]
        self.assertGreaterEqual(len(non_persone), 3, non_persone)

    def test_resta_un_solo_buco_ed_e_quello_giusto(self):
        """🐛 **Questo test diceva quattro, ed era sbagliato in tre casi su
        quattro.**

        La prima anagrafica cercava le schede **solo dentro `Bestiario/`**, poi
        un `grep` troncato a sei righe mi ha fatto concludere da una lista
        tagliata. Zalkatar e Saarvith+Regiarix hanno **statblocchi completi a
        GS 13** nell'arco 09, e il Cerchio Druidico ne ha uno nel Bestiario
        sotto un nome che la ricerca non copriva.

        Resta `lathander-mask`, e quello e' un buco corretto: due divinita' non
        sono una creatura.
        """
        self.assertEqual(set(vs.png_senza_scheda(DATI)), {"lathander-mask"})

    def test_una_scheda_puo_vivere_fuori_dal_bestiario(self):
        """La lezione, resa una prova: `scheda` e' «dove stanno le statistiche»,
        non «dove nel Bestiario»."""
        fuori = [r for r in DATI["png"]
                 if r["scheda"] and not r["scheda"].startswith("Bestiario/")]
        self.assertGreaterEqual(len(fuori), 2,
                                "le schede d'arco sono sparite dall'anagrafica")
        for r in fuori:
            with self.subTest(png=r["id"]):
                self.assertTrue((ROOT / r["scheda"]).exists())

    def test_un_buco_dichiarato_viene_messo_alla_prova(self):
        """🔴 R13 provata all'indietro **sull'errore vero**.

        Rimettere `zalkatar` a «senza scheda» deve far rosso il cancello: e'
        esattamente lo stato in cui l'anagrafica e' nata, ed e' passato.
        """
        import copy
        finto = copy.deepcopy(DATI)
        i = next(n for n, r in enumerate(finto["png"]) if r["id"] == "zalkatar")
        finto["png"][i]["scheda"] = None
        self.assertTrue(vs.buchi_con_candidati(finto, ROOT))

    def test_un_buco_senza_candidati_passa(self):
        """L'altra meta': due divinita' non hanno un file che ne porti il nome."""
        self.assertEqual(vs.buchi_con_candidati(DATI, ROOT), [])


class TestLaChiaveEMiglioreDelConfrontoDiStringhe(unittest.TestCase):
    """🔴 Il test che giustifica il lotto: la chiave **corregge** il matcher.

    Non basta che la chiave esista: deve dare risposte diverse *e giuste* dove
    il confronto di stringhe ne dava di sbagliate. Qui si riproduce il matcher
    permissivo e si verifica che l'anagrafica non lo segua.
    """

    #: (riga, cosa aggancerebbe il matcher, cosa dice l'anagrafica)
    CASI = [
        ("villain", 3, "Xal_thor", "zalkatar"),
        ("villain", 4, "Wyrmlord_Karruk", "saarvith-regiarix"),
        ("conoscenze", 9, "Sethrax", "zalkatar"),
        ("conoscenze", 18, "druid-bear-ally", "cerchio-sacro"),
    ]

    def test_dove_il_matcher_sbagliava_l_anagrafica_non_lo_segue(self):
        for sez, i, sbagliato, atteso in self.CASI:
            with self.subTest(sezione=sez, riga=i):
                rec = DATI[sez][i]
                self.assertEqual(rec["png_id"], atteso)
                voce = next(r for r in DATI["png"] if r["id"] == atteso)
                if voce["scheda"]:
                    self.assertNotIn(sbagliato, voce["scheda"],
                                     "l'anagrafica punta dove puntava l'errore")

    def test_chi_sa_e_zalkatar_non_sethrax(self):
        """«Zalkatar (via Sethrax)»: il tramite non e' il soggetto.

        Un confronto di stringhe legge «Sethrax» e attribuisce a lui la
        conoscenza. E' l'errore piu' insidioso dei quattro, perche' il
        risultato e' un PNG che esiste davvero.
        """
        riga = DATI["conoscenze"][9]
        self.assertIn("Zalkatar", riga["png"])
        self.assertEqual(riga["png_id"], "zalkatar")


class TestICancelliMordonoDavvero(unittest.TestCase):
    """Provati all'indietro in memoria: un cancello che non boccia non e' un
    cancello."""

    def test_un_png_id_inventato_e_bocciato(self):
        finto = {"png": [{"id": "vero"}], "villain": [{"png_id": "inventato"}],
                 "conoscenze": []}
        self.assertTrue(vs.riferimenti_rotti(finto))

    def test_un_png_id_buono_passa(self):
        buono = {"png": [{"id": "vero"}], "villain": [{"png_id": "vero"}],
                 "conoscenze": []}
        self.assertEqual(vs.riferimenti_rotti(buono), [])

    def test_una_scheda_inesistente_e_bocciata(self):
        finto = {"png": [{"id": "x", "scheda": "Bestiario/non-esiste.md"}]}
        self.assertTrue(vs.schede_inesistenti(finto, ROOT))

    def test_una_scheda_che_esiste_passa(self):
        vero = {"png": [{"id": "x", "scheda": "Bestiario/README.md"}]}
        self.assertEqual(vs.schede_inesistenti(vero, ROOT), [])

    def test_un_id_duplicato_e_bocciato(self):
        finto = {"png": [{"id": "x", "scheda": "a"}, {"id": "x", "scheda": "b"}]}
        self.assertTrue(vs.anagrafica_incoerente(finto))

    def test_un_buco_senza_motivo_e_bocciato(self):
        finto = {"png": [{"id": "x", "scheda": None}]}
        self.assertTrue(vs.anagrafica_incoerente(finto))
        finto["png"][0]["perche_senza_scheda"] = "non esiste, e il perche' e' scritto"
        self.assertEqual(vs.anagrafica_incoerente(finto), [])


class TestLaVistaNonCambia(unittest.TestCase):
    """L'anagrafica e' strato MACCHINA: il DM non deve vedere niente di nuovo.

    E' il criterio di ADR-0052 applicato a se stesso — un `png_id` non spiega
    niente a chi legge, quindi non ha motivo di comparire in `state.md`.
    """

    def test_png_id_non_finisce_nel_markdown(self):
        md = (ROOT / "campaign" / "state.md").read_text(encoding="utf-8")
        self.assertNotIn("png_id", md)

    def test_le_tabelle_generate_non_portano_la_chiave(self):
        import render_state as rs
        for nome in ("villain", "conoscenze"):
            with self.subTest(tabella=nome):
                campi = {k for k, _ in rs.TABELLE[nome]["campi"]}
                self.assertNotIn("png_id", campi)


if __name__ == "__main__":
    unittest.main()
