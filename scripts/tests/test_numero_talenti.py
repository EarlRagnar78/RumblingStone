"""Il numero dei talenti di una scheda (ADR-0126, lotto 4)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verifica_scheda as V  # noqa: E402

RADICE = Path(__file__).resolve().parents[2]

SCHEDA = """# Prova [INFERRED]
**Faction**: none | **Role**: brute | **Environment**: any | **CR**: {gs}

```statblocco
gs: {gs}
tipo: {tipo}
ca: 14
pf: 30
pf-dado: {dv}
ts: Temp +4, Rifl +2, Vol +2
attributi: For 16 Des 12 Cos 14 Int 10 Sag 12 Car 8
velocita: 9 m
iniziativa: +1
attacchi:
  - Mischia spada lunga +{att} (1d8+3/19-20)
voci:
  - Talenti: {talenti}
```
"""


def giudica(tipo: str, dv: str, talenti: str, bab: int = 4, gs: int = 4):
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / f"prova-cr{gs}.md"
        q.write_text(SCHEDA.format(tipo=tipo, dv=dv, talenti=talenti, att=bab + 3, gs=gs), encoding="utf-8")
        if V.VT.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        return V.numero_talenti(q)


class TestConto(unittest.TestCase):
    def test_guerriero_4_ha_due_generali_e_tre_bonus(self):
        cinque = "Attacco Poderoso, Incalzare, Arma Focalizzata (spada lunga), Schivare, Iniziativa Migliorata"
        self.assertEqual(giudica("Medium humanoid (orc), Fighter 4, CE", "4d10+8", cinque), ([], []))
        v, _ = giudica("Medium humanoid (orc), Fighter 4, CE", "4d10+8", cinque + ", Allerta")
        self.assertEqual([(x["regola"], x["ha"], x["atteso"]) for x in v], [("numero.talenti", 6, "5")])
        v, _ = giudica("Medium humanoid (orc), Fighter 4, CE", "4d10+8", "Attacco Poderoso, Incalzare, Schivare, Allerta")
        self.assertEqual([(x["ha"], x["atteso"]) for x in v], [(4, "5")])

    def test_l_umano_ne_ha_uno_in_piu(self):
        sei = "Attacco Poderoso, Incalzare, Arma Focalizzata (spada lunga), Schivare, Iniziativa Migliorata, Allerta"
        self.assertEqual(giudica("Medium humanoid (human), Fighter 4, LN", "4d10+8", sei), ([], []))

    def test_il_mezzelfo_non_ha_il_talento_dell_umano(self):
        # «(elf/human)» è il mezzelfo dell'SRD: sangue umano, niente talento in più
        cinque = "Attacco Poderoso, Incalzare, Arma Focalizzata (spada lunga), Schivare, Iniziativa Migliorata"
        for tipo in ("Medium humanoid (elf/human), Fighter 4, N", "Medium humanoid (half-elf), Fighter 4, N",
                     "Medium humanoid (orc/human), Fighter 4, N"):
            with self.subTest(tipo=tipo):
                self.assertEqual(giudica(tipo, "4d10+8", cinque), ([], []))
                v, _ = giudica(tipo, "4d10+8", cinque + ", Allerta")
                self.assertEqual([(x["ha"], x["atteso"]) for x in v], [(6, "5")])

    def test_il_talento_bonus_del_mostro_non_entra_nel_conto(self):
        # orco di 4 dadi vita: due talenti, il terzo è dichiarato (B)
        self.assertEqual(giudica("Large giant, CE", "4d8+8", "Attacco Poderoso, Robustezza, Seguire Tracce (B)", 3),
                         ([], []))
        v, _ = giudica("Large giant, CE", "4d8+8", "Attacco Poderoso, Robustezza, Seguire Tracce", 3)
        self.assertEqual([(x["ha"], x["atteso"]) for x in v], [(3, "2")])
        self.assertIn("va dichiarato", v[0]["testo"])

    def test_i_talenti_concessi_dalla_classe_non_entrano(self):
        # mago 5: Scrivere Pergamene è della classe; 2 generali e 1 bonus al 5°
        self.assertEqual(giudica("Medium humanoid (elf), Wizard 5, N", "5d4",
                                 "Scrivere Pergamene, Incantare in Combattimento, Iniziativa Migliorata, Incantesimi Estesi", 2),
                         ([], []))

    def test_il_dominio_della_guerra(self):
        tre = "Incantare in Combattimento, Competenza nelle Armi da Guerra (spada lunga), Arma Focalizzata (spada lunga)"
        v, _ = giudica("Medium humanoid (dwarf), Cleric 1, LN", "1d8+2", tre, 0, 1)
        self.assertEqual([(x["ha"], x["atteso"]) for x in v], [(3, "1")])
        self.assertEqual(giudica("Medium humanoid (dwarf), Cleric 1 (domini Guerra/Legge), LN", "1d8+2", tre, 0, 1), ([], []))

    def test_la_classe_senza_talenti_bonus_nel_plugin_lascia_il_dubbio(self):
        v, nv = giudica("Medium humanoid (orc), Barbarian 5 / Frenzied Berserker 2, CE", "7d12+14",
                        "Attacco Poderoso, Incalzare, Allerta, Robustezza, Schivare", 7, 7)
        self.assertEqual(v, [])
        self.assertEqual([x["regola"] for x in nv], ["numero.talenti"])

    def test_il_ladro_del_decimo_puo_avere_un_talento_in_piu(self):
        quattro = "Schivare, Mobilità, Iniziativa Migliorata, Allerta"
        self.assertEqual(giudica("Medium humanoid (elf), Rogue 10, CN", "10d6", quattro, 7, 10), ([], []))
        self.assertEqual(giudica("Medium humanoid (elf), Rogue 10, CN", "10d6", quattro + ", Robustezza", 7, 10), ([], []))
        v, _ = giudica("Medium humanoid (elf), Rogue 10, CN", "10d6", quattro + ", Robustezza, Correre", 7, 10)
        self.assertEqual([(x["ha"], x["atteso"]) for x in v], [(6, "4-5")])


class TestCancello(unittest.TestCase):
    """Le schede del Bestiario fuori conto aspettano il DM: quale talento togliere,
    aggiungere o dichiarare lo sceglie lui. Nessun'altra scheda è fuori conto."""

    IN_ATTESA: "set[str]" = set()

    def test_il_bestiario_non_ha_altre_schede_fuori_conto(self):
        trovate, attese = [], set()
        for p in sorted((RADICE / "Bestiario").rglob("*.md")):
            v = V.numero_talenti(p)[0]
            if p.name in self.IN_ATTESA:
                attese |= {p.name} if v else set()
            else:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in v]
        self.assertEqual(trovate, [])
        self.assertEqual(attese, self.IN_ATTESA, "una scheda in attesa è stata corretta: toglierla dall'elenco")


if __name__ == "__main__":
    unittest.main()
