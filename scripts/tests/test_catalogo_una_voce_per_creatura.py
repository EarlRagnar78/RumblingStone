"""D18 — un documento con dodici creature non e' una voce sola.

🔴 **Il difetto, misurato il 2026-09-17.** `build_monster_catalog.py` produceva
**un record per file** e prendeva il primo GS che trovava. Un documento d'arco
con piu' creature diventava quindi **una voce intitolata al documento**, con un
GS arbitrario: «Parte 2A – Torre Invisibile», GS 10. Erano **19 record** cosi',
e in `suggest_encounter --el 10` comparivano come se fossero mostri.

Non era un buco di copertura — le nove creature della Torre hanno tutte voce
propria — ma rumore che il DM vedeva al tavolo, e che nascondeva creature vere:
gli **otto fantini del Palio**, i **Sicari di Sonjak**, il Gonfaloniere, la
Chierica di Lolth, tutti dentro un record chiamato «Parte 2D — Statblocchi».

**Decisione del DM (D18): spezzarli per intestazione, verificando che non
esistano gia'.** 19 → **8**, e il pool passa da 372 a **397**.

## ⚠️ Perche' la deduplica e' la parte che puo' far danno

Confrontare nomi per somiglianza e' l'errore che **ADR-0053** vieta: un matcher
permissivo non riduce l'ignoranza, la **traveste**. Qui il confronto e'
ammesso perche' e' **ancorato a un fatto dichiarato**: si confronta soltanto
dentro l'insieme delle voci del Bestiario che citano **quel** documento come
`Source`. Il legame documento↔voce l'ha scritto qualcuno; la somiglianza decide
solo *quale* voce corrisponde a *quale* intestazione, dentro un insieme gia'
ristretto a mano.

Fuori da quell'insieme non si confronta niente, e un documento che nessuno cita
non viene mai dedotto: si spezza e basta.

## E il rischio opposto, che questo file presidia

Togliere il record di file per «fare pulizia» **toglierebbe creature dal pool**
quando il documento ne contiene una che nessuna voce nomina. Il record di
documento sparisce solo quando **ogni** creatura che nomina ha gia' la sua voce.
Otto record sopravvivono per questa ragione, e vanno bene cosi'.
"""
from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

CATALOGO = yaml.safe_load(
    (ROOT / "scripts" / "monster_catalog.yaml").read_text(encoding="utf-8"))["monsters"]

#: Come si riconosce un record intitolato al documento invece che alla creatura.
TITOLO_DI_DOCUMENTO = ("Stat blocchi", "Statblocchi", "Stat Blocchi", "Parte ")


def _bmc():
    spec = importlib.util.spec_from_file_location(
        "bmc", ROOT / "scripts" / "build_monster_catalog.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestLoSpezzamento(unittest.TestCase):
    def test_i_record_intitolati_al_documento_sono_pochi_e_non_crescono(self):
        """Erano 19. Adesso 8, e ognuno degli 8 ha una ragione per esserci.

        ⚠️ La soglia si **abbassa** quando il numero cala: lasciarla sopra il
        valore vero renderebbe il cancello piu' debole di quanto puo' essere.
        """
        doc = [m["name"] for m in CATALOGO if m["name"].startswith(TITOLO_DI_DOCUMENTO)]
        self.assertLessEqual(len(doc), 8,
                             "record intitolati al documento:\n  " + "\n  ".join(doc))

    def test_le_creature_del_palio_hanno_un_nome(self):
        """🔎 Il guadagno concreto: nove soggetti che erano un record solo.

        Prima di D18 tutto il Palio stava dentro «Parte 2D — Statblocchi e
        Comprimari», GS 8. I fantini, i sicari di Sonjak e il Gonfaloniere non
        esistevano per `suggest_encounter`.
        """
        nomi = " · ".join(m["name"] for m in CATALOGO)
        for atteso in ("Fantino Cavaliere", "Fantino Ladro", "Drow Chierica di Lolth",
                       "Gonfaloniere Aldemar Vosk", "I Sicari di Sonjak",
                       "Il Fantino della Nonna"):
            with self.subTest(soggetto=atteso):
                self.assertIn(atteso, nomi)

    def test_nessun_nome_comincia_per_cifra(self):
        """🐛 La numerazione del Palio e' **multi-livello** (`### 3.2 Drow…`).

        Togliendo solo `\\d+[.)]` restava «2 Drow Chierica di Lolth»: un nome
        che comincia per cifra, su otto voci. Il cancello lo fissa.
        """
        # ⚠️ Solo i nomi che vengono da un'INTESTAZIONE. I `.txt` e gli `.htm`
        # non ne hanno una: il loro nome lo ricava `extract_name` dal nome del
        # file (`00_Cubo Gelatinoso powerup.txt`), ed e' rumore che esisteva
        # prima di D18 e che D18 non pretende di risolvere.
        cattivi = [m["name"] for m in CATALOGO
                   if m["source_file"].endswith(".md")
                   and not m["source_file"].startswith(("Bestiario/pregen", "PG/"))
                   and re.match(r"^\d", m["name"])]
        self.assertEqual(cattivi, [], f"nomi che cominciano per cifra: {cattivi}")

    def test_nessun_nome_ha_una_parentesi_che_non_chiude(self):
        """«Gonfaloniere Aldemar Vosk (LN» — la coda tagliata lasciava il moncone."""
        rotti = [m["name"] for m in CATALOGO
                 if m["name"].count("(") > m["name"].count(")")]
        self.assertEqual(rotti, [], f"nomi troncati: {rotti}")


class TestLaDeduplicaNonProduceDoppioni(unittest.TestCase):
    """🔴 Il cancello che conta: spezzare senza dedurre farebbe **due** voci
    per la stessa creatura — quella del Bestiario e quella dell'intestazione."""

    TORRE = ("Elementale del Caos", "Golem Bibliotecario", "Guardiano di Luce",
             "Sciame di Libri Animati", "Spettri di Conoscenza")

    def test_le_creature_della_torre_compaiono_una_volta_sola(self):
        for nome in self.TORRE:
            with self.subTest(creatura=nome):
                quante = [m for m in CATALOGO if m["name"].startswith(nome)]
                self.assertEqual(len(quante), 1,
                                 f"{nome}: {[(q['name'], q['source_file']) for q in quante]}")

    def test_e_vengono_dalla_loro_scheda_non_dall_arco(self):
        """La voce buona e' quella del Bestiario: porta fazione, ruolo e ambiente."""
        for nome in self.TORRE:
            with self.subTest(creatura=nome):
                m = next(m for m in CATALOGO if m["name"].startswith(nome))
                self.assertTrue(m["source_file"].startswith("Bestiario/"), m["source_file"])

    def test_la_copertura_si_legge_dalle_fonti_dichiarate(self):
        """L'ancoraggio che rende lecito il confronto per parole.

        Se `copertura_del_bestiario` smettesse di trovare i legami, la
        deduplica confronterebbe contro l'insieme vuoto e **tutto** verrebbe
        spezzato in doppioni. Questo test prova che l'ancora tiene.
        """
        cop = _bmc().copertura_del_bestiario(ROOT)
        self.assertGreater(len(cop), 30,
                           "quasi nessun documento risulta coperto: l'ancoraggio "
                           "della deduplica non sta leggendo le fonti dichiarate")
        torre = [k for k in cop if "Torre-PARTE1-STATBLOCCHI" in k]
        self.assertTrue(torre, "il file degli statblocchi della Torre non risulta coperto")
        self.assertGreaterEqual(len(cop[torre[0]]), 3)


class TestIlPoolNonSiRestringe(unittest.TestCase):
    def test_il_pool_e_cresciuto_spezzando(self):
        """305 → 352 (4d-5) → 372 (4d-6) → 397 (D18) → 384 (4d-8) → 381 → **380** (L7).

        🔴 **La soglia scende per la seconda volta, e ogni unita' ha un nome.**
        Il primo calo (397 → 384) furono i **13 soggetti con due record** — una
        scheda canonica e un POINTER `-crN` accanto — ridotti a uno.

        Il secondo (384 → 381) e' del 2026-09-18 e sono **tre**, uno per
        ragione diversa:

        | −1 | Chi | Perche' |
        |---|---|---|
        | 1 | **Elementale della Terra Anziano GS 13** | **era Terros**: l'archivio, sotto quel titolo, scrive «TERROS ANZIANO». Un boss con due GS in due record |
        | 2 | **Thorgrim Barbadiferro GS 13** | **non ha uno statblocco in tutto il repo**: nel modulo e' una prova sociale CD 20. Il GS 13 l'avevo inventato io |
        | 3 | **Skullcrusher, secondo record** | riaffiorato per un attimo togliendo l'ERRATA dalle fonti dichiarate della voce, e richiuso rimettendocela |
        | 4 | **Ushgar «Occhio Reso», secondo record** *(2026-09-23)* | il dossier portava un suo blocco con TS diversi dallo statblocco `ushgar-occhio-reso-cr13.md`; ora e' `[RIMANDO]`, e Ushgar resta **una** voce, quella dello statblocco |

        ⚠️ **Zero creature giocabili in meno nel pool.** Una era doppia, una
        non era una creatura, una era un artefatto della deduplica.

        Una soglia che cala va motivata o diventa un tappeto: se domani il
        numero scende ancora senza che nessuno abbia scritto perche', il
        cancello deve tornare rosso.
        """
        self.assertGreaterEqual(len(CATALOGO), 380)

    def test_ogni_record_ha_una_fonte_che_esiste(self):
        for m in CATALOGO:
            with self.subTest(voce=m["name"][:40]):
                self.assertTrue((ROOT / m["source_file"]).exists(), m["source_file"])

    def test_gli_id_restano_unici(self):
        """Spezzare per intestazione conia id nuovi: due sezioni omonime nello
        stesso file collidereb''bero, e un id duplicato rompe ogni consumatore."""
        doppi = [i for i, n in Counter(m["id"] for m in CATALOGO).items() if n > 1]
        self.assertEqual(doppi, [], f"id duplicati: {doppi}")


class TestLeDecisioniDiCanoneDel17Settembre(unittest.TestCase):
    """Due numeri discordi, decisi dal DM e scritti dove si leggono."""

    def test_skullcrusher_il_nero_vale_dodici(self):
        m = [x for x in CATALOGO if "Skullcrusher il Nero" in x["name"]]
        self.assertEqual(len(m), 1)
        self.assertEqual(m[0]["cr"], 12.0)
        archivio = (ROOT / "07_il Portale Della Forgia Eterna" / "_ARCHIVIO"
                    / "PortaleForgia-P6-INTEGRAZIONE-Completa.md").read_text(encoding="utf-8")
        self.assertNotIn("Skullcrusher il Nero** (Adult Black Dragon CR 11)", archivio,
                         "il file d'archivio porta ancora il numero vecchio")
        self.assertIn("GS 12, non CR 11", archivio, "manca l'errata accanto alla riga")
        # 🔎 E la voce non cita piu' l'archivio: i numeri (PF 240, CA 27) sono
        # nel master vivo, e il FASTPLAY che citava non ha **nessuna** marca.
        voce = (ROOT / "Bestiario" / "villain"
                / "skullcrusher-il-nero-cr12.md").read_text(encoding="utf-8")
        self.assertNotIn("_ARCHIVIO", voce.split("## Notes")[0],
                         "la testa della voce torna a puntare a un archivio")
        self.assertIn("ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md", voce)

    def test_il_boss_del_piano_della_terra_giocato_e_terros(self):
        """🔴 **Il 17 settembre questo test si accontentava di un avviso.**

        C'erano **due** voci per lo stesso boss — Terros a GS 15 e «Elementale
        della Terra Anziano» a GS 13 — e il test chiedeva solo che la seconda
        dicesse «al tavolo vale Terros». Un avviso dentro una voce non impedisce
        a `suggest_encounter --cr 13` di proporla.

        Misurando la fonte il 18: l'archivio, sotto il titolo «BOSS FIGHT:
        ELEMENTALE DELLA TERRA ANZIANO (CR 13)», scrive ***«TERROS ANZIANO -
        Elementale della Terra Anziano»***. Non era un altro mostro: era
        Terros prima della ricalibrazione. La voce a GS 13 e' stata rimossa.
        """
        terros = [x for x in CATALOGO if "Terros" in x["name"]]
        self.assertEqual(len(terros), 1)
        self.assertEqual(terros[0]["cr"], 15.0)
        self.assertFalse((ROOT / "Bestiario" / "mostri"
                          / "elementale-terra-anziano-cr13.md").exists(),
                         "il doppione a GS 13 e' tornato")
        doppi = [x for x in CATALOGO
                 if "Elementale della Terra Anziano" in x["name"]]
        self.assertEqual(doppi, [], f"Terros ha di nuovo due record: {doppi}")


class TestIDueConclaviIllithid(unittest.TestCase):
    """🔴 Canone del DM, 2026-09-17: **Zalkatar è «il Padrone delle Menti»**
    del laboratorio di ARC-04.

    Una riga che cuce quattro archi. Il repo dichiarava gia' **due** conclavi
    illithid rivali — Xal'thor chiama Zalkatar «biologo da torre», Zalkatar
    chiama lui «cacciatore di mandria» — ma nessuno dei due era una fazione:
    gli illithid stavano sparsi su **quattro** etichette diverse, e Zarim era
    marcato `red-hand` mentre la sua stessa scheda dice *«legato alla fazione
    di Xal'thor»*.
    """

    def test_le_due_fazioni_esistono_e_non_si_mescolano(self):
        zal = {m["name"] for m in CATALOGO if m["faction"] == "illithid-zalkatar"}
        xal = {m["name"] for m in CATALOGO if m["faction"] == "illithid-xal-thor"}
        self.assertGreaterEqual(len(zal), 11, "la Torre Invisibile ha perso i suoi custodi")
        # 4 e non 6: la deduplica di 4d-8 ha tolto i gemelli di Xal'thor e Zarim,
        # che erano due record ciascuno.
        self.assertGreaterEqual(len(xal), 4, "l'invasione planare ha perso i suoi")
        self.assertEqual(zal & xal, set(), "i due conclavi sono rivali, non si sovrappongono")

    def test_i_custodi_della_torre_sono_di_zalkatar(self):
        indice = {m["name"]: m["faction"] for m in CATALOGO}
        for nome in ("Guardiano di Luce (elementale/costrutto)", "Golem Bibliotecario",
                     "Spettri di Conoscenza", "Sciame di Libri Animati",
                     "Elementale del Caos", "Grell (Torre Invisibile)"):
            with self.subTest(creatura=nome):
                self.assertEqual(indice.get(nome), "illithid-zalkatar")

    def test_zarim_non_e_piu_mano_rossa(self):
        """🐛 La sua scheda diceva «legato alla fazione di Xal'thor» e il
        catalogo lo dava `red-hand`: due valori per lo stesso fatto."""
        zarim = [m for m in CATALOGO if m["name"].startswith("Zarim")]
        self.assertTrue(zarim)
        for m in zarim:
            with self.subTest(voce=m["source_file"]):
                self.assertEqual(m["faction"], "illithid-xal-thor")

    def test_zalkatar_non_e_una_parola_chiave_della_mano_rossa(self):
        """La correzione nel builder, provata sul sorgente.

        `zalkatar` stava nell'elenco di `red-hand`: un illithid warlock
        classificato come comandante della Mano Rossa.
        """
        sorgente = (ROOT / "scripts" / "build_monster_catalog.py").read_text(encoding="utf-8")
        elenco = re.search(r'"red-hand":\s*\[(.*?)\]', sorgente, re.S).group(1)
        self.assertNotIn('"zalkatar"', elenco)

    def test_il_dossier_di_zalkatar_non_finge_di_essere_una_creatura(self):
        """⚠️ Il marcatore e' una stringa esatta, non prosa.

        La prima stesura scriveva `[NON-CREATURA — dossier di fazione]`, e
        `build_monster_catalog` cerca `[NON-CREATURA]` alla lettera: il dossier
        era finito nel pool degli incontri come un mostro da GS 13.
        """
        d = ROOT / "Bestiario" / "villain" / "Zalkatar" / "Zalkatar.md"
        self.assertTrue(d.exists())
        self.assertIn("[NON-CREATURA]", d.read_text(encoding="utf-8").split("\n")[0])
        self.assertNotIn("ZALKATAR — Illithid Warlock",
                         " · ".join(m["name"] for m in CATALOGO))

    def test_il_dossier_registra_il_canone_e_le_sue_prove(self):
        """Un collegamento di canone vale per le prove che cita, non per l'idea."""
        t = (ROOT / "Bestiario" / "villain" / "Zalkatar" / "Zalkatar.md").read_text(encoding="utf-8")
        for prova in ("Padrone delle Menti", "ex-schiavi drow", "Yochlol half-illithid",
                      "Ring of Chaotic Illumination", "biologo da torre"):
            with self.subTest(prova=prova):
                self.assertIn(prova, t)


if __name__ == "__main__":
    unittest.main()
