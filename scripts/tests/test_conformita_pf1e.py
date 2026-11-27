"""ADR-0119: le regole PF1e del cancello delle schede, dal PRD.

Per ogni conto nuovo, due prove:

1. una scheda giusta (numeri del PRD o rifatti a mano dalla regola) passa;
2. la stessa scheda con **un** numero sbagliato viene bocciata, sul conto
   giusto, e con --severo il cancello esce 1.

L'ultima classe prova lo stesso sulle schede vere del Drappo e del Giardino:
si cambia un numero nel testo del modulo e il conto lo trova.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import conformita_statblocchi as C  # noqa: E402

#: Chierico 13 umano, come Mastro Tariq: BAB 9, TS 12/6/16 con mantello +2,
#: BMC +10, DMC 21 (anello +1 deviazione), incanalare 2/giorno 7d6 CD 15,
#: pf 101 (13d8 + 26 di Cos + 13 di Robustezza), incantesimi CD 16 + livello.
CHIERICO = """## Chierico

```statblocco
nome: Chierico di prova
gs: 12
tipo: Umano chierico 13 · CM Medio
ca: 25
ca-dettaglio: contatto 11, colto alla sprovvista 25 (+11 armatura, +3 scudo, +1 deviazione)
pf: 101
pf-dado: 13d8+39
ts: Tem +12, Rif +6, Vol +16
attributi: For 12 Des 10 Cos 14 Int 13 Sag 22 Car 8
iniziativa: +4
sensi: Percezione +10
```
**Attacco** BAB +9 · BMC +10 · DMC 21 · *incanalare energia negativa* 2/giorno (7d6, CD 15)

**Statistiche** **Talenti** Incanalare Selettivo, Iniziativa Migliorata, Robustezza · **Equipaggiamento** *mantello della resistenza +2*, *anello di protezione +1*

**Capacità speciali**
- **Incantesimi preparati** (LI 13°, CD 16 + livello)
"""

#: Il chuul del Bestiary (book-b1 760) con il template avanzato: Grande,
#: aberrazione 10 DV (BAB 7), BMC +17, DMC 32, TS 9/8/11, scurovisione.
CHUUL = """## Chuul

```statblocco
nome: Chuul avanzato
gs: 8
tipo: Aberrazione Grande (acquatica) · CM
ca: 26
ca-dettaglio: contatto 14, colto alla sprovvista 21 (+5 Des, +12 naturale, −1 taglia)
pf: 105
pf-dado: 10d8+60
ts: Tem +9, Rif +8, Vol +11
attributi: For 29 Des 20 Cos 22 Int 14 Sag 18 Car 9
iniziativa: +9
sensi: scurovisione 18 m, Percezione +21
```
**Attacco** BAB +7 · BMC +17 (+21 lottare) · DMC 32 (36 contro sbilanciare)

**Statistiche** **Talenti** Allerta, Arma Focalizzata (chela), Combattere alla Cieca, Iniziativa Migliorata, Riflessi in Combattimento
"""

#: Il cavallo del Bestiary (book-b1 1849): Grande, animale 2 DV, DMC 17,
#: visione crepuscolare.
CAVALLO = """## Cavallo

```statblocco
nome: Cavallo
gs: 1
tipo: Animale Grande
ca: 11
ca-dettaglio: contatto 11, colto alla sprovvista 9 (+2 Des, −1 taglia)
pf: 15
pf-dado: 2d8+6
ts: Tempra +6, Riflessi +5, Volontà +1
attributi: For 16 Des 14 Cos 17 Int 2 Sag 13 Car 7
iniziativa: +2
sensi: visione crepuscolare, fiuto, Percezione +6
```
**Attacco** BMC +5 · DMC 17 (21 contro sbilanciare)

**Statistiche** **Talenti** Resistenza, Correre
"""

#: Lo skum del Bestiary (book-b1 2584: umanoide mostruoso 2 DV) con 8 livelli da
#: guerriero: BAB 10, TS 11/7/8, pf 115 (2d10+8d10+60: Cos e Robustezza).
SKUM = """## Skum

```statblocco
nome: Skum guerriero 8
gs: 9
tipo: Umanoide mostruoso Medio (acquatico) · LM
ca: 24
ca-dettaglio: contatto 12, colto alla sprovvista 22 (+7 armatura, +3 scudo, +2 Des, +2 naturale)
pf: 115
pf-dado: 2d10+8d10+60
ts: Tem +11, Rif +7, Vol +8 (+2 contro la paura)
attributi: For 21 Des 15 Cos 21 Int 10 Sag 12 Car 4
iniziativa: +6
sensi: scurovisione 18 m, Percezione +7
```
**Attacco** BAB +10 · BMC +15 (+17 spingere) · DMC 27

**Statistiche** **Talenti** Iniziativa Migliorata, Multiattacco, Robustezza, Volontà di Ferro
"""

#: Un ladro con Schivare: la CA lo scrive.
LADRO = """## Ladro

```statblocco
nome: Ladro con Schivare
gs: 3
tipo: Umano ladro 4 · NM
ca: 19
ca-dettaglio: contatto 16, colto alla sprovvista 14 (+3 armatura, +4 Des, +1 schivare, +1 anello)
pf: 26
pf-dado: 4d8+4
ts: Tempra +2, Riflessi +8, Volontà +2
attributi: For 12 Des 18 Cos 12 Int 13 Sag 12 Car 10
iniziativa: +4
sensi: Percezione +8
```
**Attacco** **BAB** +3 · **CMB** +4 · **CMD** 20

**Statistiche** **Talenti** Arma Accurata · Schivare · Mobilità
"""


def campi(testo: str) -> "list[tuple[str, str]]":
    # il conto si legge dalla chiave `conto`, che lo scarto porta sempre: `prova`
    # c'è solo finché il conto è in prova (ADR-0119), e un conto promosso la perde
    return [(x["campo"], x.get("conto", "")) for x in C.conti_dei_recinti(testo, "pf1e")]


class LeSchedeGiustePassano(unittest.TestCase):

    def test_chierico(self):
        self.assertEqual(campi(CHIERICO), [])

    def test_chuul(self):
        self.assertEqual(campi(CHUUL), [])

    def test_cavallo(self):
        self.assertEqual(campi(CAVALLO), [])

    def test_ladro_con_schivare(self):
        self.assertEqual(campi(LADRO), [])

    def test_la_classe_scritta_anche_nel_nome_non_conta_due_volte(self):
        # «ladro 4» nel nome e nel tipo: prima erano otto livelli, DV razziali
        # negativi, e BAB e TS non partivano (un numero sbagliato passava)
        doppio = LADRO.replace("nome: Ladro con Schivare", "nome: Umano ladro 4")
        self.assertEqual(campi(doppio), [])
        self.assertIn("BAB", [c for c, _ in campi(doppio.replace("**BAB** +3", "**BAB** +4"))])
        self.assertIn("TS vol", [c for c, _ in campi(doppio.replace("Volontà +2", "Volontà +5"))])

    def test_la_classe_solo_nel_nome_si_legge_ancora(self):
        nel_nome = LADRO.replace("nome: Ladro con Schivare", "nome: Ladro 4 con Schivare").replace(
            "tipo: Umano ladro 4", "tipo: Umano")
        self.assertIn("BAB", [c for c, _ in campi(nel_nome.replace("**BAB** +3", "**BAB** +4"))])

    def test_skum_con_livelli_di_classe(self):
        self.assertEqual(campi(SKUM), [])

    def test_in_3_5_i_conti_nuovi_non_si_fanno(self):
        # il 3.5 non ha le regole di classe nei dati: nessun conto nuovo
        sbagliato = CHIERICO.replace("BMC +10", "BMC +11").replace("Vol +16", "Vol +15")
        self.assertEqual(C.conti_dei_recinti(sbagliato, "dnd35"), [])


class UnNumeroSbagliatoVieneBocciato(unittest.TestCase):

    CASI = [
        # (scheda, da, a, campo, conto)
        (CHIERICO, "BAB +9", "BAB +10", "BAB", "BAB"),
        (CHIERICO, "BMC +10", "BMC +11", "BMC", "BMC"),
        (CHIERICO, "DMC 21", "DMC 20", "DMC", "DMC"),
        (CHIERICO, "Tem +12", "Tem +10", "TS temp", "TS"),
        (CHIERICO, "Rif +6", "Rif +7", "TS rifl", "TS"),
        (CHIERICO, "Vol +16", "Vol +14", "TS vol", "TS"),
        (CHIERICO, "contatto 11", "contatto 12", "CA contatto", "contatto_sprovvista"),
        (CHIERICO, "sprovvista 25", "sprovvista 24", "CA colto alla sprovvista", "contatto_sprovvista"),
        (CHIERICO, "iniziativa: +4", "iniziativa: +0", "iniziativa", "iniziativa_recinto"),
        (CHIERICO, "2/giorno (7d6", "3/giorno (7d6", "incanalare usi", "incanalare"),
        (CHIERICO, "(7d6, CD 15)", "(6d6, CD 15)", "incanalare dadi", "incanalare"),
        (CHIERICO, "(7d6, CD 15)", "(7d6, CD 17)", "incanalare CD", "incanalare"),
        (CHUUL, "BMC +17", "BMC +16", "BMC", "BMC"),            # taglia Grande +1
        (CHUUL, "DMC 32", "DMC 31", "DMC", "DMC"),
        (CHUUL, "BAB +7", "BAB +10", "BAB", "BAB"),             # aberrazione: 3/4
        (CHUUL, "scurovisione 18 m, ", "", "sensi", "scurovisione"),
        (CHUUL, "scurovisione 18 m", "scurovisione 9 m", "sensi", "scurovisione"),
        (CAVALLO, "DMC 17", "DMC 18", "DMC", "DMC"),            # il numero del Drappo
        (CAVALLO, "visione crepuscolare, ", "", "sensi", "visione_crepuscolare"),
        (LADRO, " +1 schivare,", "", "CA", "schivare"),
        (CHIERICO, "13d8+39", "13d8+26", "pf-dado bonus", "pf_bonus"),   # Robustezza dimenticata
        (CHIERICO, "CD 16 + livello", "CD 15 + livello", "CD incantesimi", "cd_incantesimi"),
        (CHIERICO, "(LI 13°", "(LI 12°", "LI", "cd_incantesimi"),
        (SKUM, "pf: 115", "pf: 116", "pf", "pf_misti"),
        (SKUM, "Vol +8", "Vol +6", "TS vol", "TS"),            # il numero del Giardino
        (SKUM, "BAB +10", "BAB +8", "BAB", "BAB"),             # 2 DV razziali + guerriero 8
        (LADRO, "**CMD** 20", "**CMD** 19", "DMC", "DMC"),     # schivare e deviazione nel DMC
    ]

    def test_ogni_numero_sbagliato_e_bocciato_sul_suo_conto(self):
        for scheda, da, a, campo, conto in self.CASI:
            with self.subTest(da=da, a=a):
                self.assertIn(da, scheda)
                trovati = campi(scheda.replace(da, a, 1))
                self.assertIn((campo, conto), trovati)

    def test_la_corrompere_acqua_segue_la_presenza(self):
        drago = CHUUL.replace(
            "**Statistiche**",
            "**Presenza Terrificante** CD 14 · *corrompere l'acqua* CD 15\n\n**Statistiche**")
        # 10 + ½ DV (5) + Car (−1) = 14: la presenza torna, corrompere l'acqua no
        self.assertIn(("CD corrompere l'acqua", "corrompere_acqua"), campi(drago))
        self.assertNotIn(("CD corrompere l'acqua", "corrompere_acqua"),
                         campi(drago.replace("CD 15", "CD 14")))


class IlCancelloDeiModuli(unittest.TestCase):

    def _con(self, sostituzioni):
        vero = C.rapporto_master

        def finto(files):
            fuori = []
            for p in files:
                testo = p.read_text(encoding="utf-8")
                for da, a in sostituzioni.get(p.name, ()):
                    self.assertIn(da, testo)
                    testo = testo.replace(da, a, 1)
                sistema = C.S.sistema_di(p)
                for x in C.conti_dei_recinti(testo, sistema):
                    fuori.append({"file": p.name, **x})
            return fuori
        C.rapporto_master = finto
        try:
            return C.main(["--cancello-moduli"]), C.main(["--cancello-moduli", "--severo"])
        finally:
            C.rapporto_master = vero

    def test_i_moduli_veri_passano_anche_severi(self):
        self.assertEqual(self._con({}), (0, 0))

    def test_un_numero_sbagliato_nel_giardino(self):
        # Karkator: BMC +25 → +26; il BMC è promosso (2026-11-25): blocca anche senza --severo
        self.assertEqual(self._con({"appendice_creature.md": [("BMC +25", "BMC +26")]}), (1, 1))

    def test_un_numero_sbagliato_nel_drappo(self):
        self.assertEqual(self._con({"STATBLOCCHI-PF1E.md": [("**CMB** +3", "**CMB** +2")]}), (1, 1))

    def test_un_conto_in_prova_avvisa_e_severo_blocca(self):
        # il canale resta per i conti che verranno (ADR-0119): un conto che torna
        # in prova avvisa (⚠) e non blocca, con --severo blocca
        regole = C.regole_conformita("pf1e")["conti"]
        fatti, prova = list(regole["fatti"]), list(regole.get("in_prova", []))
        try:
            regole["fatti"].remove("BMC")
            regole["in_prova"] = prova + ["BMC"]
            self.assertEqual(self._con({"appendice_creature.md": [("BMC +25", "BMC +26")]}), (0, 1))
        finally:
            regole["fatti"][:], regole["in_prova"] = fatti, prova


class IQuattordiciContiSonoStable(unittest.TestCase):
    """Promozione del 2026-11-25 (ADR-0099, ADR-0119): i 14 conti in prova dal
    2026-11-10 passano fra i `fatti`, e uno scarto dice ancora quale conto è."""

    PROMOSSI = {"BMC", "DMC", "BAB", "TS", "contatto_sprovvista", "iniziativa_recinto",
                "schivare", "scurovisione", "visione_crepuscolare", "corrompere_acqua",
                "incanalare", "pf_bonus", "pf_misti", "cd_incantesimi"}

    def test_i_quattordici_sono_fatti_e_nessuno_resta_in_prova(self):
        conti = C.regole_conformita("pf1e")["conti"]
        self.assertLessEqual(self.PROMOSSI, set(conti["fatti"]))
        self.assertEqual(list(conti.get("in_prova", [])), [])

    def test_uno_scarto_di_un_conto_fatto_porta_il_conto_e_non_la_prova(self):
        (x,) = [x for x in C.conti_dei_recinti(CHIERICO.replace("BMC +10", "BMC +11"), "pf1e")
                if x["campo"] == "BMC"]
        self.assertEqual(x["conto"], "BMC")
        self.assertNotIn("prova", x)


if __name__ == "__main__":
    unittest.main()
