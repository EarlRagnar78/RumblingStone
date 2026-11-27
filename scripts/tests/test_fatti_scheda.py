"""`verifica_scheda --fatti`: i fatti di una scheda in JSON (ADR-0126).

Li legge il controllo di coerenza della storia per incrociare la prosa con la
scheda. Qui si prova che ogni fatto porta la riga giusta e che l'uscita non
giudica nulla."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_scheda as V  # noqa: E402

SCHEDA = """# Sacerdote di prova

**Chierico 5** · GS 5

**Talenti:** Volontà di Ferro, Talento Che Non Esiste

**Incantesimi preparati** (LI 5):
- 1° (4+1): *benedizione* ×2, *scudo della fede* (CD 14), *comando*, *anatema*D
- 0 (5): *luce*, *guida*

- *Aura di paura (Sop)*: 9 m, Volontà CD 15.
- **Scacciare non morti (Sop)** 6/giorno.

#### Soffio di cenere (Mag)

**Tattiche** Apre con *benedizione*.
Poi resta dietro lo scudo.

**Bottino** 30 mo.

### Descrizione
Un vecchio magro.
"""


def _fatti(testo: str = SCHEDA) -> dict:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "prova.md"
        p.write_text(testo, encoding="utf-8")
        return V.fatti(p)


class TestBlocchi(unittest.TestCase):
    """`blocchi`: una voce per scheda del file, e ogni fatto porta l'indice della sua."""

    def test_una_scheda_un_blocco_che_e_tutto_il_file(self):
        f = _fatti()
        self.assertEqual([(b["titolo"], b["inizio"], [t["canonico"] for t in b["talenti"]]) for b in f["blocchi"]],
                         [("Sacerdote di prova", 1, ["Iron Will", None])])
        self.assertEqual(f["blocchi"][0]["fine"], len(SCHEDA.splitlines()))
        self.assertEqual({V.blocco_di(f["blocchi"], x.get("riga") or x["inizio"])
                          for x in f["incantesimi"] + f["capacita_speciali"] + f["tattiche"]}, {0})

    def test_due_schede_due_blocchi_coi_loro_talenti(self):
        f = _fatti(SCHEDA + "\n## Secondo\n\n**Talenti:** Schivare\n\n- 1° (1): *sonno*\n\n**Tattiche** Fugge.\n")
        self.assertEqual([(b["titolo"], [t["nome"] for t in b["talenti"]]) for b in f["blocchi"]],
                         [("Sacerdote di prova", ["Volontà di Ferro", "Talento Che Non Esiste"]),
                          ("Secondo", ["Schivare"])])
        self.assertEqual(f["blocchi"][0]["fine"] + 1, f["blocchi"][1]["inizio"])
        self.assertEqual([V.blocco_di(f["blocchi"], i["riga"]) for i in f["incantesimi"] if i["nome"] == "sonno"], [1])
        self.assertEqual([V.blocco_di(f["blocchi"], t["inizio"]) for t in f["tattiche"]], [0, 1])
        self.assertIsNone(V.blocco_di(f["blocchi"], 9999))
        # la chiave di prima non cambia: i talenti della prima riga del file
        self.assertEqual([t["nome"] for t in f["talenti"]], ["Volontà di Ferro", "Talento Che Non Esiste"])

    def test_nota_citata_e_talenti_ripetuti_sotto_lo_stesso_titolo_non_aprono_un_blocco(self):
        f = _fatti(SCHEDA + "\n> **Talenti**: la scheda ne elencava sei.\n\nTalenti: Volontà di Ferro\n")
        self.assertEqual(len(f["blocchi"]), 1)

    def test_recinto_senza_talenti_e_talenti_in_prosa_sono_una_scheda(self):
        f = _fatti("# Drago\n\n```statblocco\nnome: Drago\n```\n\n## Statistiche\n\n**Talenti:** Schivare\n")
        self.assertEqual([(b["inizio"], [t["nome"] for t in b["talenti"]]) for b in f["blocchi"]], [(1, ["Schivare"])])

    def test_file_senza_schede(self):
        self.assertEqual(_fatti("# Appunti\n\nNiente numeri.\n")["blocchi"], [])


class TestFatti(unittest.TestCase):
    def test_talenti_con_canonico_e_riga(self):
        f = _fatti()
        self.assertEqual([(t["nome"], t["canonico"], t["riga"]) for t in f["talenti"]],
                         [("Volontà di Ferro", "Iron Will", 5), ("Talento Che Non Esiste", None, 5)])

    def test_incantesimi_con_livello_usi_e_riga(self):
        inc = {i["nome"]: i for i in _fatti()["incantesimi"]}
        self.assertEqual(set(inc), {"benedizione", "scudo della fede", "comando", "anatema", "luce", "guida"})
        self.assertEqual(inc["benedizione"], {"nome": "benedizione", "canonico": "Bless", "livello": 1,
                                              "usi": "4+1", "volte": 2, "riga": 8})
        self.assertEqual(inc["scudo della fede"]["canonico"], "Shield of Faith")
        self.assertEqual((inc["luce"]["livello"], inc["luce"]["riga"]), (0, 9))

    def test_capacita_speciali_nelle_tre_grafie(self):
        self.assertEqual([(c["nome"], c["tipo"], c["riga"]) for c in _fatti()["capacita_speciali"]],
                         [("Aura di paura", "Sop", 11), ("Scacciare non morti", "Sop", 12),
                          ("Soffio di cenere", "Mag", 14)])

    def test_sezioni_con_inizio_e_fine(self):
        f = _fatti()
        self.assertEqual(f["tattiche"], [{"inizio": 16, "fine": 17}])
        self.assertEqual(f["descrizione"], [{"inizio": 21, "fine": 22}])

    def test_piu_sezioni_nello_stesso_file(self):
        f = _fatti(SCHEDA + "\n**Tattiche** Seconda creatura: carica.\n")
        self.assertEqual([s["inizio"] for s in f["tattiche"]], [16, 24])

    def test_un_titolo_tiene_i_grassetti_dentro(self):
        f = _fatti("#### Tattiche di prova\n**Round 1** carica.\n**Round 2** fugge.\n\n#### Altro\n")
        self.assertEqual(f["tattiche"], [{"inizio": 1, "fine": 3}])

    def test_elenco_di_prosa_non_e_una_lista_di_incantesimi(self):
        f = _fatti("# Dungeon\n\n- 1° *La Sala dei Riflessi*, *La Cella*\n")
        self.assertEqual(f["incantesimi"], [])

    def test_scheda_senza_nulla(self):
        f = _fatti("# Vuota\n\nSolo prosa.\n")
        self.assertEqual([f[k] for k in ("talenti", "incantesimi", "capacita_speciali", "tattiche", "descrizione")],
                         [[], [], [], [], []])

    def test_cli_stampa_json_e_non_giudica(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prova.md"
            p.write_text(SCHEDA, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(V.main([str(p), "--fatti", "--check"]), 0)
        dati = json.loads(out.getvalue())
        self.assertEqual(len(dati), 1)
        self.assertEqual(set(dati[0]), {"file", "sistema", "talenti", "incantesimi", "capacita_speciali",
                                        "tattiche", "descrizione", "blocchi"})


if __name__ == "__main__":
    unittest.main()
