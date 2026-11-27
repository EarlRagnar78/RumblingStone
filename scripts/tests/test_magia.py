"""Incantesimi al giorno, conosciuti e CD dalle tabelle delle classi (ADR-0126, lotto 3)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dmcore import magia as M  # noqa: E402

RADICE = Path(__file__).resolve().parents[2]


def totali(x):
    return [a + b for a, b in x]


class TestTabelle(unittest.TestCase):
    def test_incantesimi_bonus(self):
        # «Table: Ability Modifiers and Bonus Spells»: 18-19 dà uno fino al 4°, 20-21 due di 1°
        self.assertEqual([M.bonus(4, liv) for liv in range(6)], [0, 1, 1, 1, 1, 0])
        self.assertEqual([M.bonus(5, liv) for liv in range(7)], [0, 2, 1, 1, 1, 1, 0])
        self.assertEqual(M.bonus(17, 1), 5)

    def test_chierico_3_5_con_dominio(self):
        # chierico 11, Sag 18: 6 / 5+1+D / 4+1+D / 4+1+D / 3+1+D / 2+D / 1+D
        self.assertEqual(M.al_giorno("cleric", 11, 18), [(6, 0), (6, 1), (5, 1), (5, 1), (4, 1), (2, 1), (1, 1)])

    def test_la_caratteristica_bassa_chiude_i_livelli_alti(self):
        # mago 9 con Int 13: lancia fino al 3°
        self.assertEqual(totali(M.al_giorno("wizard", 9, 13)), [4, 5, 4, 3])

    def test_lo_zero_della_tabella_vuole_il_bonus(self):
        self.assertEqual(totali(M.al_giorno("ranger", 4, 14)), [0, 1])
        self.assertEqual(M.al_giorno("ranger", 4, 10), [])
        self.assertEqual(totali(M.al_giorno("bard", 4, 18)), [3, 3, 1])

    def test_mago_specialista(self):
        # SRD 3.5: «one additional spell of her specialty school per spell level», 0 compreso
        # (card del DM del 2026-11-19, Ragnhild Mantoferro); PF1e: lo slot di scuola parte dal 1°
        self.assertEqual(M.al_giorno("wizard", 5, 16, specialista=True), [(4, 1), (4, 1), (3, 1), (2, 1)])
        self.assertEqual(M.al_giorno("wizard", 5, 16, "pf1e", specialista=True)[0][1], 0)

    def test_pf1e(self):
        # bardo e stregone: i trucchetti sono a volontà (-1, non si giudicano); il paladino lancia col Carisma
        self.assertEqual(M.al_giorno("bard", 4, 18, "pf1e"), [(-1, 0), (4, 0), (2, 0)])
        self.assertEqual(M.classe("paladin", "pf1e")["caratteristica"], "Car")
        self.assertEqual(M.classe("paladin")["caratteristica"], "Sag")
        # stregone 7: uno di stirpe al 1°, 2° e 3° livello d'incantesimo
        self.assertEqual(M.conosciuti("sorcerer", 7, "pf1e"), [7, 6, 4, 3])
        self.assertEqual(M.conosciuti("sorcerer", 7), [7, 5, 3, 2])

    def test_classe_senza_tabella(self):
        self.assertIsNone(M.al_giorno("favored soul", 7, 18))
        self.assertIsNone(M.conosciuti("cleric", 7))

    def test_il_plugin_e_quello_che_l_estrattore_scrive(self):
        for sis in ("dnd35", "pf1e"):
            classi = M.tabelle(sis)["classi"]
            self.assertEqual(sorted(classi), ["adept", "bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "wizard"])
            for c in classi.values():
                self.assertEqual(len(c["al_giorno"]), 20)


class TestLettura(unittest.TestCase):
    def test_al_giorno_scritto(self):
        self.assertEqual(M.leggi_al_giorno("(LI 8°; 6/5+1/5+1/4+1 al giorno; D = dominio)"), [(6, 0), (5, 1), (5, 1), (4, 1)])
        self.assertEqual(M.leggi_al_giorno("(CL 4°; 2/1 per giorno)"), [(2, 0), (1, 0)])
        self.assertIsNone(M.leggi_al_giorno("(LI 9°, CD 16 + livello)"))

    def test_conta_i_nomi_in_corsivo(self):
        self.assertEqual(M.conta("*aiuto* (D), *blocca persone* (CD 16) ×2, *silenzio*"), 4)
        self.assertEqual(M.conta("*dissolvi magie, preghiera, luce incandescente*; *animare morti* (D)"), 4)
        self.assertEqual(M.conta("*guida*; la perla del potere rende uno di questi, e così i lanci"), 1)
        self.assertEqual(M.conta("*ipotermia* [Private source — supplementi, gli ultimi tre]"), 1)
        self.assertEqual(M.conta("dominio: *ferire* (CD 20)"), 1)


class TestGiudizio(unittest.TestCase):
    def setUp(self):
        self.slot = M.al_giorno("cleric", 11, 18)

    def campi(self, *a, **k):
        return [(x["campo"], x["scritto"], x["atteso"]) for x in M.giudica_riga(*a, **k)]

    def test_riga_giusta(self):
        self.assertEqual(self.campi(3, "5+D", "*a aa*, *bbb*, *ccc*, *ddd*, *eee* (D, CD 17)", self.slot, None, 18), [])

    def test_slot_dichiarati_in_piu(self):
        self.assertEqual(self.campi(2, "6+D", "*aaa*", self.slot, None, 18), [("incantesimi.al_giorno", "6+1", "5+1")])

    def test_piu_incantesimi_degli_slot(self):
        self.assertEqual(self.campi(6, "", "*aaa*, *bbb*, *ccc* (D)", self.slot, None, 18),
                         [("incantesimi.al_giorno", 3, "1+1")])

    def test_meno_incantesimi_non_e_uno_scarto(self):
        self.assertEqual(self.campi(1, "", "*aaa*", self.slot, None, 18), [])

    def test_livello_che_non_lancia(self):
        self.assertEqual(self.campi(7, "", "*aaa*", self.slot, None, 18)[0][0], "incantesimi.livello")
        basso = M.al_giorno("cleric", 11, 13)
        self.assertIn("14", M.giudica_riga(4, "", "*aaa*", basso, None, 13)[0]["nota"])

    def test_cd(self):
        self.assertEqual(self.campi(3, "", "*aaa* (CD 18)", self.slot, None, 18), [("incantesimi.cd", 18, 17)])
        self.assertEqual(self.campi(3, "", "*aaa* (CD 18)", self.slot, None, 18, 1), [])
        self.assertEqual(self.campi(3, "CD 16", "*aaa*", self.slot, None, 18, 1), [("incantesimi.cd", 16, 17)])

    def test_conosciuti(self):
        noti = M.conosciuti("sorcerer", 6)
        slot = M.al_giorno("sorcerer", 6, 16)
        self.assertEqual(self.campi(1, "", "*aaa*, *bbb*, *ccc*, *ddd*", slot, noti, 16), [])
        self.assertEqual(self.campi(1, "", "*aaa*, *bbb*, *ccc*, *ddd*, *eee*", slot, noti, 16),
                         [("incantesimi.conosciuti", 5, 4)])

    def test_dichiarati_in_testa(self):
        s = M.giudica_dichiarati(M.leggi_al_giorno("6/6+1/6+1/5+1/4+1/2+1/1+1 al giorno"), self.slot)
        self.assertEqual([(x["livello"], x["scritto"], x["atteso"]) for x in s], [(2, "6+1", "5+1")])
        ranger = M.al_giorno("ranger", 4, 14)
        s = M.giudica_dichiarati([(2, 0), (1, 0)], ranger, da_zero=False)
        self.assertEqual([(x["livello"], x["atteso"]) for x in s], [(1, "1"), (2, "nessuno")])


SCHEDA = """# Prova

**Sistema:** D&D 3.5

**Caratteristiche** For 10, Des 10, Cos 10, Int 10, Sag {sag}, Car {car}

**Incantesimi da {classe}** ({testa}):
{righe}
"""


class TestScheda(unittest.TestCase):
    def giudica(self, **k):
        import verifica_scheda as V
        k = {"sag": 18, "car": 18, **k}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prova.md"
            p.write_text(SCHEDA.format(**k), encoding="utf-8")
            v, n = V.incantatori(p)
        return [(x["regola"], x["ha"], x["atteso"]) for x in v], [x["regola"] for x in n]

    def test_chierico_giusto(self):
        v, n = self.giudica(classe="chierico", testa="LI 5°; 5/4+1/3+1/2+1 al giorno",
                            righe="- 3° (CD 17): *preghiera*, *dissolvi magie*, *animare morti* (D)\n- 0: *guida*")
        self.assertEqual((v, n), ([], []))

    def test_chierico_con_uno_slot_in_piu_e_la_cd_sbagliata(self):
        v, _ = self.giudica(classe="chierico", testa="LI 5°; 5/4+1/3+1/3+1 al giorno",
                            righe="- 3° (CD 18): *preghiera*, *dissolvi magie*, *animare morti* (D)")
        self.assertEqual(v, [("numero.incantesimi.al_giorno", "3+1", "2+1"), ("numero.incantesimi.cd", 18, 17)])

    def test_la_caratteristica_dichiarata_in_testa_vince(self):
        v, _ = self.giudica(classe="chierico", testa="LI 5°; 5/5+1/3+1/2+1 al giorno, con Sag 20",
                            righe="- 3° (CD 18): *preghiera*")
        self.assertEqual(v, [])

    def test_bardo_con_la_tabella_scelta_dal_dm(self):
        # 3.5: 3/3/1; la tabella PF1e che il DM ha scelto per il bardo dà 4/2: forma ibrida, non uno scarto
        v, n = self.giudica(classe="bardo", testa="LI 4°; 3/4/2 al giorno", righe="- 1°: *charme su persone*")
        self.assertEqual((v, n), ([], ["numero.incantesimi.variante"]))
        v, n = self.giudica(classe="bardo", testa="LI 4°; 3/5/2 al giorno", righe="- 1°: *charme su persone*")
        self.assertEqual([x[0] for x in v], ["numero.incantesimi.al_giorno"] * 2)

    def test_il_ranger_lancia_col_livello_di_classe_non_col_li(self):
        # ranger 8 con Sag 14: 1+1 di 1° e 0+1 di 2°; la testa dice «CL 4°», metà del livello
        # di classe: prima il verificatore lo prendeva per ranger 4 (ARC08-01, 2026-11-19)
        import verifica_scheda as V
        k = dict(classe="Ranger", testa="CL 4°; 2/1 per giorno", sag=14, car=10,
                 righe="- 2° (CD 14): *pelle coriacea*\n- 1° (CD 13): *passo veloce*, *resistere all'energia*")
        v, n = self.giudica(**k)
        self.assertEqual((v, n), ([], ["numero.incantesimi"]), "senza il livello di classe non si giudica")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prova.md"
            p.write_text(SCHEDA.format(**k).replace("# Prova\n", "# Prova\n\n*Elfo Ranger 8°*\n"), encoding="utf-8")
            v, n = V.incantatori(p)
        self.assertEqual((v, n), ([], []))

    def test_i_segreti_della_maestra_del_sapere_danno_slot(self):
        # mago 13 evocatore con Int 25 e Altro Arcano Ritrovato: 4+1 / 7+1 / 6+1+1 …
        k = dict(classe="Mago", testa="LI 13°; 5/8/8/8 al giorno; scuole proibite Ammaliamento e Illusione",
                 righe="- 2° (CD 21): *raggio rovente* ×2, *sfera infuocata*, *resistere all'energia*, "
                       "*forza del toro*, *frantumare*, *vedere invisibilità*, *individuazione dei pensieri*")
        senza = SCHEDA.format(sag=10, car=10, **k).replace("Int 10", "Int 25")
        con = senza + "\nSegreti: Altro Arcano Ritrovato (uno slot di 2° in più).\n"
        import verifica_scheda as V
        esiti = []
        for testo in (senza, con):
            with tempfile.TemporaryDirectory() as d:
                p = Path(d) / "prova.md"
                p.write_text(testo, encoding="utf-8")
                esiti.append([(x["ha"], x["atteso"]) for x in V.incantatori(p)[0]
                              if "al giorno di 2°" in x["testo"]])
        self.assertEqual(esiti, [[("8", "6+1")], []])

    def test_classe_senza_tabella_non_e_verificabile(self):
        v, n = self.giudica(classe="anima prescelta", testa="LI 7°", righe="- 1°: *benedizione*")
        self.assertEqual(v, [])

    def test_senza_livello_non_e_verificabile(self):
        v, n = self.giudica(classe="chierico", testa="domini Guerra e Terra", righe="- 1°: *benedizione*")
        self.assertEqual((v, n), ([], ["numero.incantesimi"]))


class TestCancello(unittest.TestCase):
    """Gli scarti che il controllo ha trovato nel Bestiario aspettano il DM: togliere
    un incantesimo preparato è una scelta sua. Nessun'altra scheda ne ha."""

    IN_ATTESA: "set[str]" = set()

    def test_il_bestiario_non_ha_altri_scarti(self):
        import verifica_scheda as V
        trovate, attese = [], set()
        for p in sorted((RADICE / "Bestiario").rglob("*.md")):
            v = V.incantatori(p)[0]
            if p.name in self.IN_ATTESA:
                attese |= {p.name} if v else set()
            else:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in v]
        self.assertEqual(trovate, [])
        self.assertEqual(attese, self.IN_ATTESA, "una scheda in attesa è stata corretta: toglierla dall'elenco")


if __name__ == "__main__":
    unittest.main()
