"""L'ordine delle sezioni di un booklet di serata (scripts/misura_ordine.py).

Un booklet finto di dieci pagine con un difetto per regola, poi lo stesso
corretto: ogni regola deve vedere il suo difetto e tacere sul libro giusto.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import misura_ordine as mo  # noqa: E402


def s(t, da, a, ruolo, livello=1, **kw):
    return {"livello": livello, "titolo": t, "da": da, "a": a, "ruolo": ruolo, **kw}


DIFETTOSO = [
    s("Regia", 1, 1, "avvio"),
    s("Scena 2", 2, 3, "gioco", scena=2),
    s("Scena 1", 4, 4, "gioco", scena=1),           # R3: la scena 1 dopo la 2
    s("Le prossime volte", 5, 5, "fuori-serata"),   # R6: fra due scene
    s("Scena 3", 6, 6, "gioco", scena=3),
    s("Scena 3 in tre righe", 7, 7, "sintesi", riassume="^Scena 3$"),  # R4: dopo
    s("Il cast", 8, 8, "preparazione"),             # R2: dopo il gioco
    s("Schede", 9, 9, "riferimento"),
    s("Schede, di nuovo", 10, 10, "riferimento", doppione_di="Schede"),  # R7
]

GIUSTO = [
    s("Regia", 1, 1, "avvio"),
    s("Il cast", 2, 2, "preparazione"),
    s("Scena 3 in tre righe", 3, 3, "sintesi", riassume="^Scena 3$"),
    s("Scena 1", 4, 4, "gioco", scena=1),
    s("Scena 2", 5, 6, "gioco", scena=2),
    s("Scena 3", 7, 7, "gioco", scena=3),
    s("Le prossime volte", 8, 8, "fuori-serata"),
    s("Schede", 9, 10, "riferimento"),
]


class TestRegole(unittest.TestCase):

    def test_ogni_difetto_e_visto(self):
        m = mo.misura(DIFETTOSO)
        self.assertEqual(m["R2_preparazione_prima"], "0/1")
        self.assertEqual(m["R3_scene_fuori_ordine"], [("Scena 1", "Scena 2")])
        self.assertEqual(m["R4_sintesi_dopo_il_dettaglio"], "1/1")
        self.assertEqual(m["R6_pagine_fuori_serata_fra_le_scene"], 1)
        self.assertEqual(len(m["R7_doppioni"]), 1)
        self.assertEqual(mo.difetti(m), 5)

    def test_il_libro_giusto_passa(self):
        m = mo.misura(GIUSTO)
        self.assertEqual(m["R1_avvio_in_testa"], "1/1")
        self.assertEqual(m["R2_preparazione_prima"], "1/1")
        self.assertEqual(mo.difetti(m), 0)

    def test_etichetta_eredita_dal_capitolo(self):
        sez = [{"livello": 1, "titolo": "X · Appendice", "da": 1, "a": 2},
               {"livello": 2, "titolo": "§0-bis — QUICK-REFERENCE", "da": 1, "a": 1},
               {"livello": 2, "titolo": "Tesoro", "da": 2, "a": 2}]
        regole = [{"titolo": "QUICK-REFERENCE", "ruolo": "preparazione"},
                  {"titolo": "Appendice", "ruolo": "riferimento", "capitolo": True}]
        self.assertEqual([x["ruolo"] for x in mo.etichetta(sez, regole)],
                         ["riferimento", "preparazione", "riferimento"])


class TestEreditaDallaSezione(unittest.TestCase):

    def test_la_sottosezione_eredita_dalla_sezione_sopra(self):
        """«La parte in trenta secondi» sta sotto «§0 — QUICKSTART» (avvio),
        non è gioco perché il capitolo è gioco (volume d'arco, 2026-11-19)."""
        sez = [{"livello": 1, "titolo": "I · Terra", "da": 1, "a": 1},
               {"livello": 1, "titolo": "§0 — QUICKSTART", "da": 2, "a": 2},
               {"livello": 2, "titolo": "La parte in trenta secondi", "da": 2, "a": 2},
               {"livello": 1, "titolo": "§2 — INGRESSO", "da": 3, "a": 3},
               {"livello": 2, "titolo": "SCENA 1", "da": 3, "a": 3}]
        regole = [{"titolo": "QUICKSTART", "ruolo": "avvio"},
                  {"titolo": "^I · ", "ruolo": "gioco", "capitolo": True}]
        self.assertEqual([x["ruolo"] for x in mo.etichetta(sez, regole)],
                         ["gioco", "avvio", "avvio", "gioco", "gioco"])


class TestGuida(unittest.TestCase):
    """R8: la guida ai capitoli stampata dice il vero (la serata di ARC-07
    stampava la guida del booklet lungo)."""

    TITOLI = ["I · Regia della serata", "V · Atto II · Dopo il barile", "XII · Durik, il compagno"]

    def test_la_guida_sbagliata_si_vede(self):
        righe = ["I · Regia della serata", "V · La cassetta del DM", "VIII · Durik"]
        self.assertEqual(mo.guida_sbagliata(righe, self.TITOLI),
                         ["V · La cassetta del DM", "VIII · Durik"])

    def test_la_guida_giusta_passa(self):
        self.assertEqual(mo.guida_sbagliata(["V · Atto II · Dopo il barile", "XII · Durik"],
                                            self.TITOLI), [])


class TestVolume(unittest.TestCase):
    """Il volume d'arco (richiesta di Jfs del 2026-11-19, «lo stesso lavoro
    per l'avventura completa»): lo schema degli AP chiede il quadro del
    volume prima della Parte I, un indice che si legge in una pagina, e in
    ogni parte le stesse regole della serata."""

    def test_quadro_assente_e_difetto_di_una_parte(self):
        sez = [
            s("I · Parte prima", 1, 3, "gioco", parte=True),
            s("§0 Quickstart", 1, 1, "avvio", livello=2),
            s("Scena 1", 2, 3, "gioco", livello=2),
            s("II · Parte seconda", 4, 7, "gioco", parte=True),
            s("§0 Quickstart", 4, 4, "avvio", livello=2),
            s("Scena 2", 5, 5, "gioco", livello=2),
            s("Le versioni veloci", 6, 6, "sintesi", livello=2, riassume="^Scena 2$"),
            s("Le prossime volte", 7, 7, "fuori-serata", livello=2),
        ]
        m = mo.misura_volume(sez, pagine_indice=1)
        self.assertEqual(m["V1_quadro_del_volume"], 0)
        self.assertEqual(m["V2_pagine_di_indice_oltre_due"], 0)
        self.assertEqual(m["parti"]["II · Parte seconda"]["R4_sintesi_dopo_il_dettaglio"], "1/1")
        self.assertEqual(mo.difetti_volume(m), 2)   # niente quadro + una sintesi dopo

    def test_volume_giusto(self):
        sez = [
            s("Il quadro dell'arco", 1, 1, "avvio"),
            s("I · Parte prima", 2, 3, "gioco", parte=True),
            s("§0 Quickstart", 2, 2, "avvio", livello=2),
            s("Scena 1", 3, 3, "gioco", livello=2),
        ]
        m = mo.misura_volume(sez, pagine_indice=2)
        self.assertEqual(m["V1_quadro_del_volume"], 1)
        self.assertEqual(mo.difetti_volume(m), 0)

    def test_segnalibri_piatti(self):
        """Nei nostri PDF il titolo della parte è un segnalibro di una pagina
        allo stesso livello delle sezioni: non è gioco, e una parte senza
        gioco (un ponte, gli echi) non ha preparazione «dopo»."""
        sez = [
            s("I · Parte", 1, 1, "gioco", parte=True),
            s("§1 Highlight", 2, 2, "preparazione"),
            s("Scena 1", 3, 3, "gioco"),
            s("II · Ponte", 4, 4, "fuori-serata", parte=True),
            s("Chi si incontra", 4, 4, "preparazione"),
        ]
        m = mo.misura_volume(sez, pagine_indice=1)
        self.assertEqual(m["parti"]["I · Parte"]["R2_dopo"], [])
        self.assertEqual(m["parti"]["II · Ponte"]["R2_dopo"], [])

    def test_parte_senza_gioco_fra_due_parti(self):
        """V3: il ponte verso l'arco dopo (VII nel volume di ARC-07) stampato
        fra il duello e il ritorno spezza la lettura; negli AP la conclusione
        sta dopo l'ultima parte giocata."""
        sez = [
            s("I · Gioco", 1, 1, "gioco", parte=True), s("Scena 1", 2, 2, "gioco"),
            s("II · Ponte", 3, 3, "fuori-serata", parte=True), s("Esiti", 4, 4, "fuori-serata"),
            s("III · Gioco", 5, 5, "gioco", parte=True), s("Scena 2", 6, 6, "gioco"),
            s("IV · Echi", 7, 7, "fuori-serata", parte=True), s("Echi", 8, 8, "fuori-serata"),
        ]
        m = mo.misura_volume(sez, pagine_indice=1)
        self.assertEqual(m["V3_parti_senza_gioco_fra_le_parti"], ["II · Ponte"])

    def test_indice_lungo(self):
        m = mo.misura_volume([s("I · X", 1, 1, "gioco", parte=True)], pagine_indice=8)
        self.assertEqual(m["V2_pagine_di_indice_oltre_due"], 6)

    def test_pagine_di_indice_dai_puntini(self):
        testi = ["Colophon", "Indice\nI · Terra . . . . . . 11", "Scena 9 . . . . . 40", "Testo"]
        self.assertEqual(mo.pagine_di_indice(testi), 2)


class TestRuoliNelManifest(unittest.TestCase):
    """ADR-0145, 2026-11-19: i ruoli stanno nel manifest, accanto ai capitoli.
    L'introduzione e le appendici generate non sono capitoli del manifest:
    valgono avvio (prima) e riferimento (dopo), come in CMOS 1.4."""

    MAN = {"chapters": [
        {"title": "I · Regia", "ruolo": "avvio"},
        {"title": "II · Atto I", "ruolo": "gioco", "scena": 1, "parte": True},
        {"title": "III · Dopo", "ruolo": "fuori-serata"},
    ], "ruoli_sezioni": [{"titolo": "^Tesoro", "ruolo": "riferimento"}]}
    TITOLI = ["Dove siamo", "I · Regia", "II · Atto I", "III · Dopo", "Appendice: le creature"]

    def test_regole_dai_capitoli_e_dalle_sezioni(self):
        r = mo.regole_dal_manifest(self.MAN, self.TITOLI)
        self.assertEqual([x["ruolo"] for x in r],
                         ["avvio", "avvio", "gioco", "fuori-serata", "riferimento", "riferimento"])
        self.assertEqual((r[2]["scena"], r[2]["parte"]), (1, True))
        self.assertTrue(all(x["capitolo"] for x in r[:5]))
        self.assertNotIn("capitolo", r[5])

    def test_il_titolo_combacia_intero(self):
        # «I · Regia» non deve prendere «I · Regia bis»: il titolo è esatto.
        r = mo.regole_dal_manifest(self.MAN, self.TITOLI)
        self.assertIsNone(__import__("re").search(r[1]["titolo"], "I · Regia bis"))

    def test_capitolo_senza_ruolo_e_un_difetto(self):
        man = {"chapters": [{"title": "I · Regia", "ruolo": "avvio"}, {"title": "II · Atto I"}]}
        r = mo.regole_dal_manifest(man, ["I · Regia", "II · Atto I"])
        sez = mo.etichetta([s("I · Regia", 1, 1, None), s("II · Atto I", 2, 3, None),
                            s("Scena 1", 2, 2, None, livello=2)], r)
        self.assertEqual([x["ruolo"] for x in sez], ["avvio", "?", "?"])

    def test_violazioni_dicono_la_regola(self):
        v = dict(mo.violazioni(mo.misura(DIFETTOSO)))
        self.assertIn("R3_scene_fuori_ordine", v)
        self.assertIn("R7_doppioni", v)
        self.assertEqual(mo.violazioni(mo.misura(GIUSTO)), [])


class TestManifestDelRepo(unittest.TestCase):
    """Il cancello statico, senza PDF: un manifest che dichiara i ruoli li
    dichiara per ogni capitolo, con un valore ammesso. Quello con il PDF è
    `difetti_ordine` di misura_stampa.py."""

    def test_ruoli_completi(self):
        import json
        radice = Path(__file__).resolve().parents[2]
        visti = 0
        for mp in radice.rglob("*.manifest.json"):
            if ".git" in mp.parts or "build" in mp.parts:
                continue
            man = json.loads(mp.read_text(encoding="utf-8"))
            if not mo.ha_ruoli(man):
                continue
            visti += 1
            for c in man["chapters"]:
                self.assertIn(c.get("ruolo"), mo.RUOLI, f"{mp.name}: {c.get('title')}")
            for r in man.get("ruoli_sezioni", []):
                self.assertIn(r["ruolo"], mo.RUOLI, f"{mp.name}: {r['titolo']}")
        self.assertGreaterEqual(visti, 2, "la serata e il volume d'arco di ARC-07 dichiarano i ruoli")


if __name__ == "__main__":
    unittest.main()
