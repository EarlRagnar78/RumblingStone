"""Le caratteristiche contro il salvataggio PCGen citato (ADR-0126, lotto delle razze;
scelta del DM sulla card del 2026-11-20: «Contro la fonte citata (.pcg)»).

Il .pcg scrive il punteggio dopo l'acquisto a punti e gli aumenti di livello, ma prima
della razza. Si chiede che una scheda legale passi: acquisto a punti più razza, con o
senza l'oggetto che dà la caratteristica, e l'ira scritta a parte; e che la razza
dimenticata o l'ira dentro la riga `attributi` si vedano."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

# orc_regular.pcg: STR 14 DEX 13 CON 14 INT 12 WIS 11 CHA 10, Warrior 4, nessun oggetto
# di caratteristica; l'orco dà For +4, Int −2, Sag −2, Car −2 (SRD)
ORCO = """# Orco di prova [INFERRED]
**Faction**: none | **Role**: brute | **Environment**: any | **CR**: 3 | **Source**: PCGen save `{pcg}`

```statblocco
gs: 3
tipo: Medium humanoid (orc), Warrior 4, CE
ca: 15
pf: 26
pf-dado: 4d8+8
ts: Temp +6, Rifl +2, Vol +0
attributi: {attributi}
```
{coda}"""
GIUSTE = "For 18 Des 13 Cos 14 Int 10 Sag 9 Car 8"


def _prova(attributi: str, coda: str = "", pcg: str = "orc_regular.pcg") -> "tuple[list, list]":
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "orco-prova-cr3.md"
        p.write_text(ORCO.format(attributi=attributi, coda=coda, pcg=pcg), encoding="utf-8")
        return V.caratteristiche_dalla_fonte(p)


class TestDallaFonte(unittest.TestCase):
    def test_acquisto_a_punti_piu_razza_passa(self):
        self.assertEqual(_prova(GIUSTE), ([], []))

    def test_la_razza_dimenticata_si_vede(self):
        viol, _ = _prova("For 14 Des 13 Cos 14 Int 12 Sag 11 Car 10")
        self.assertEqual(len(viol), 1)
        self.assertEqual(viol[0]["atteso"], {"For": 18, "Int": 10, "Sag": 9, "Car": 8})

    def test_l_ira_scritta_a_parte_passa(self):
        coda = "\nIra (1/giorno): For 22, Cos 18, pf 34, Temp +8, Vol +2, CA 13.\n"
        self.assertEqual(_prova(GIUSTE, coda), ([], []))

    def test_l_ira_dentro_la_riga_attributi_si_vede(self):
        viol, _ = _prova("For 22 Des 13 Cos 18 Int 10 Sag 9 Car 8")
        self.assertEqual(viol[0]["ha"], {"For": 22, "Cos": 18})

    def test_oggetto_di_caratteristica_con_o_senza(self):
        # Bothor: STR 16, guanti della potenza dell'orco (+2 di potenziamento), Guerriero 6, nano
        pcg = "00-underdark-grr6-Bothor-Malvur.pcg"
        nano = "Des 13 Cos 16 Int 10 Sag 12 Car 6"
        for forza, ok in ((16, True), (18, True), (20, False)):
            testo = ORCO.replace("Warrior 4", "Fighter 6").replace("4d8+8", "6d10+18").replace("(orc)", "(dwarf)")
            with tempfile.TemporaryDirectory() as d:
                p = Path(d) / "nano-prova-cr6.md"
                p.write_text(testo.format(attributi=f"For {forza} {nano}", coda="", pcg=pcg), encoding="utf-8")
                viol, _ = V.caratteristiche_dalla_fonte(p)
            self.assertEqual(viol == [], ok, (forza, viol))

    def test_oggetto_nello_zaino_non_conta(self):
        # gli stessi guanti, ma l'insieme d'equipaggiamento del .pcg li tiene «Carried»: For 18 non torna più
        from unittest import mock
        nome = "00-underdark-grr6-Bothor-Malvur.pcg"
        vero = V._salvataggi_pcg()[nome].read_text(encoding="utf-8", errors="replace")
        self.assertIn("EQUIPSET:Hands|ID:0.1.04|VALUE:Gauntlets of Ogre Power", vero)
        nano = "Des 13 Cos 16 Int 10 Sag 12 Car 6"
        testo = ORCO.replace("Warrior 4", "Fighter 6").replace("4d8+8", "6d10+18").replace("(orc)", "(dwarf)")
        with tempfile.TemporaryDirectory() as d:
            q = Path(d) / nome
            q.write_text(vero.replace("EQUIPSET:Hands|ID:0.1.04|VALUE:Gauntlets", "EQUIPSET:Carried|ID:0.1.04|VALUE:Gauntlets"),
                         encoding="utf-8")
            with mock.patch.object(V, "_salvataggi_pcg", return_value={nome: q}):
                for forza, ok in ((16, True), (18, False)):
                    p = Path(d) / "nano-prova-cr6.md"
                    p.write_text(testo.format(attributi=f"For {forza} {nano}", coda="", pcg=nome), encoding="utf-8")
                    viol, _ = V.caratteristiche_dalla_fonte(p)
                    self.assertEqual(viol == [], ok, (forza, viol))

    def test_un_export_citato_non_si_giudica(self):
        self.assertEqual(_prova("For 14 Des 13 Cos 14 Int 12 Sag 11 Car 10",
                                pcg="orc_regular.pcg` (export `orco.htm`)"), ([], []))

    def test_scheda_avanzata_oltre_il_salvataggio_non_si_giudica(self):
        testo = GIUSTE.replace("For 18", "For 19")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "orco-prova-cr5.md"
            p.write_text(ORCO.format(attributi=testo, coda="", pcg="orc_regular.pcg").replace("4d8+8", "8d8+16"),
                         encoding="utf-8")
            viol, nv = V.caratteristiche_dalla_fonte(p)
        self.assertEqual(viol, [])
        self.assertIn("avanzata", nv[0]["testo"])


if __name__ == "__main__":
    unittest.main()
