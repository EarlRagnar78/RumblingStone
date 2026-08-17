"""Il lettore delle schede pregenerate (`dmcore.schede`) e la loro impaginazione.

Due livelli, perché i difetti stanno a due livelli diversi:

  * **sintetici** — le regole di taglio dei blocchi. Sono le uniche righe di
    questo modulo dove un errore non si vede: una voce fantasma in mezzo a una
    scheda sembra un dato del personaggio, non un bug del parser.
  * **sul modulo vero** — `Il Drappo di Tarsilia`. Se un master cambia forma e
    il lettore smette di trovare la CA, si scopre qui e non in stampa.

Solo `unittest`: la CI gira `python -m unittest discover -s scripts/tests` e non
installa pytest.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore.schede import SchedaError, leggi_schede  # noqa: E402
from export_booklet_typst import ROOT, inline, schede_di, sorgente  # noqa: E402

DRAPPO = REPO / "STANDALONE-Il-Drappo-di-Tarsilia"
PREGEN = DRAPPO / "PREGEN-SEI-SCHEDE-PF1E.md"
FASCICOLO = DRAPPO / "FASCICOLO-SCHEDE-GIOCATORE.md"
MANIFEST = DRAPPO / "homebrew" / "DRAPPO-SCHEDE-PG.manifest.json"
TEMPLATE = REPO / "scripts" / "typst" / "scheda-pg.typ"


# ── regole di taglio, su un master sintetico ─────────────────────────────────

MINIMA = """\
# prova

## 1 · TIZIA CAIA — il Capitano

**Umana guerriera 3** · N · femmina, 38 anni · **GS 2**
*Due righe di occhiello che
vanno a capo come nei master veri.*

**Iniziativa** +5 · **Percezione** +3 · **Velocità** 6 m

### Difesa
**CA** 18, contatto 11, colto alla sprovvista 17 (+5 armatura)
**pf** 27 (3d10+6)
**TS** Tempra **+6**, Riflessi **+3**, Volontà **+5** *(mantello +1
incluso)*

### Attacco
**Mischia** spada lunga **+8** (1d8+3/19–20)
&nbsp;&nbsp;con **Attacco Poderoso**: **+7** (1d8+5)
**BAB** +3 · **CMB** +6 · **CMD** 17
**Canalizzare**: 2d6 cure, CD 12 — con
**Canalizzazione Selettiva** escludi 1 creatura

### Statistiche
**For** 17 (+3) · **Des** 13 (+1) · **Cos** 14 (+2) · **Int** 10 (+0) · **Sag** 12 (+1) · **Car** 13 (+1)

**Incantesimi preparati** (CD 14 + livello)
- **1°** (3 + 1 dominio): *cura ferite leggere* · *intralciare* ·
  **dominio**: *pietra magica*
**Talenti**: Attacco Poderoso · Volontà di Ferro
**Equipaggiamento**: spada lunga (315) · pugnale (2) · **mantello della
resistenza +1** (1.000) · 2 pozioni (100) ·
**+ ~212 mo**, che sono della contrada

### Il suo problema
Una cosa che ha firmato da sola.

### Come si gioca in un minuto
Decidi, e ad alta voce.

---
"""


class TestMasterSintetico(unittest.TestCase):
    """Le regole di taglio, sulle forme che i master usano davvero."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        p = Path(cls._tmp.name) / "PREGEN-PROVA.md"
        p.write_text(MINIMA, encoding="utf-8")
        cls.s = leggi_schede(p)[0]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_intestazione(self):
        s = self.s
        self.assertEqual((s.numero, s.nome, s.ruolo), ("1", "TIZIA CAIA", "il Capitano"))
        self.assertEqual(s.classe, "Umana guerriera 3 · N · femmina, 38 anni · GS 2")
        self.assertTrue(s.occhiello.endswith("nei master veri."))
        self.assertEqual(
            s.rapide, [("Iniziativa", "+5"), ("Percezione", "+3"), ("Velocità", "6 m")]
        )

    def test_difesa(self):
        s = self.s
        self.assertEqual((s.ca, s.pf, s.pf_dado), ("18", "27", "3d10+6"))
        self.assertTrue(s.ca_dettaglio.startswith("contatto 11"))
        self.assertEqual(s.ts, [("Tempra", "+6"), ("Riflessi", "+3"), ("Volontà", "+5")])
        # la nota fra parentesi va a capo nel master: deve arrivare intera
        self.assertEqual(s.ts_nota, "mantello +1 incluso")

    def test_attributi_e_manovre(self):
        self.assertEqual(self.s.attributi[0], ("For", "17", "+3"))
        self.assertEqual(len(self.s.attributi), 6)
        self.assertEqual(self.s.manovre, [("BAB", "+3"), ("CMB", "+6"), ("CMD", "17")])

    def test_attacco_rientro_e_continuazione(self):
        """Il rientro `&nbsp;` resta una riga a sé; la frase spezzata a metà no."""
        righe = self.s.attacchi
        self.assertEqual(righe[0], ("**Mischia** spada lunga **+8** (1d8+3/19–20)", False))
        self.assertEqual(righe[1], ("con **Attacco Poderoso**: **+7** (1d8+5)", True))
        self.assertFalse(righe[2][1])
        self.assertIn("Canalizzazione Selettiva", righe[2][0])   # ricucita, non spezzata
        self.assertEqual(len(righe), 3)

    def test_voci_niente_fantasmi(self):
        """Le tre voci vere, e nessuna delle tre trappole del markdown a capo."""
        self.assertEqual(
            [v.etichetta for v in self.s.voci],
            ["Incantesimi preparati", "Talenti", "Equipaggiamento"],
        )
        equip = self.s.voce("equipaggiamento")
        self.assertIn("mantello della resistenza +1", equip.corpo)  # prezzo a capo
        self.assertIn("+ ~212 mo", equip.corpo)                     # resto in tasca
        self.assertIn("**dominio**: *pietra magica*",
                      self.s.voce("incantesimi").corpo)             # slot di dominio

    def test_filetto_non_finisce_nel_testo(self):
        """`---` fra una scheda e l'altra: Typst lo stamperebbe come lineetta lunga."""
        self.assertEqual(self.s.minuto, "Decidi, e ad alta voce.")
        self.assertFalse(self.s.problema.endswith("—"))

    def test_master_senza_schede(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "PREGEN-VUOTO.md"
            p.write_text("# niente qui\n\ntesto\n", encoding="utf-8")
            with self.assertRaises(SchedaError):
                leggi_schede(p)


# ── il modulo vero ───────────────────────────────────────────────────────────

class TestDrappo(unittest.TestCase):
    """Le sei schede del Drappo, lette dai master che il tavolo usa davvero."""

    @classmethod
    def setUpClass(cls):
        cls.schede = leggi_schede(
            PREGEN, FASCICOLO, [DRAPPO / "ALLEGATI" / "immagini" / "web"]
        )

    def test_sei_schede_complete(self):
        self.assertEqual(len(self.schede), 6)
        for s in self.schede:
            with self.subTest(scheda=s.nome):
                self.assertTrue(s.nome and s.ruolo and s.classe)
                self.assertTrue(s.ca and s.pf)
                self.assertEqual(len(s.attributi), 6)
                self.assertEqual(len(s.ts), 3)
                self.assertTrue(s.attacchi)
                self.assertTrue(s.minuto)               # il piede della scheda
                self.assertIsNotNone(s.voce("equipaggiamento"))
                self.assertIsNotNone(s.voce("abilità"))
                self.assertIsNotNone(s.voce("talenti"))

    def test_ogni_scheda_ha_il_suo_ritratto(self):
        """`FRA' MELCHIO VANZI` → `ritratto-melchio.jpg`: la parola giusta, non la prima."""
        self.assertEqual(
            [s.ritratto.name for s in self.schede],
            ["ritratto-vanna.jpg", "ritratto-nocca.jpg", "ritratto-ombra.jpg",
             "ritratto-tesio.jpg", "ritratto-berenice.jpg", "ritratto-melchio.jpg"],
        )

    def test_meta_sinistra_dal_fascicolo(self):
        for s in self.schede:
            with self.subTest(scheda=s.nome):
                self.assertTrue(s.ad_alta_voce.startswith("«"))
                self.assertEqual(len(s.legami), 5)      # gli altri cinque, mai sé stesso
                self.assertEqual([v.etichetta for v in s.voci_retro][:2],
                                 ["Come parli", "Tre cose che sai"])

    def test_incantatori_hanno_gli_slot(self):
        per_nome = {s.nome.split()[0]: s for s in self.schede}
        for chi in ("OMBRA", "TESIO", "BERENICE"):
            with self.subTest(scheda=chi):
                self.assertIsNotNone(per_nome[chi].voce("incantesimi"))


# ── la traduzione a Typst ────────────────────────────────────────────────────

class TestInline(unittest.TestCase):

    CASI = [
        # enfasi annidata: il caso che stampava mezza riga in corsivo
        ("**bacchetta di *cura ferite leggere*, 25 cariche**",
         "*bacchetta di _cura ferite leggere_, 25 cariche*"),
        # grassetto e corsivo che chiudono sullo stesso asterisco
        ("**2 pozioni di *cura ferite leggere***", "*2 pozioni di _cura ferite leggere_*"),
        ("***tutto insieme***", "*_tutto insieme_*"),
        # `~` in Typst è uno spazio unificatore: non deve sparire dal prezzo
        ("**+ ~212 mo**", "*+ \\~212 mo*"),
        # due grassetti di fila non si fondono in uno
        ("**Cavalcare +10**, **Furtività +19**", "*Cavalcare +10*, *Furtività +19*"),
    ]

    def test_enfasi_e_caratteri_speciali(self):
        for md, atteso in self.CASI:
            with self.subTest(md=md):
                self.assertEqual(inline(md), atteso)


class TestSorgenteTypst(unittest.TestCase):
    """Il ponte fra l'esportatore e il template `.typ`.

    ⚠️ **In CI non c'è typst**, quindi nessuno compila davvero: se qualcuno
    rinomina un parametro dentro `#let scheda(...)`, ogni PDF smette di
    costruirsi e la CI resta verde. Questi test sono l'unico posto dove quella
    rottura si vede senza il binario.
    """

    @classmethod
    def setUpClass(cls):
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        base = MANIFEST.parent
        cls.src = sorgente(man, base, True)
        cls.cap = man["chapters"][0]
        cls.pezzi = schede_di(cls.cap, base, (base / cls.cap["file"]).resolve())

    @staticmethod
    def _firma_template() -> set[str]:
        """I nomi dei parametri di `#let scheda(...)`, letti dal template."""
        testo = TEMPLATE.read_text(encoding="utf-8")
        inizio = testo.index("#let scheda(")
        corpo, livello = [], 0
        for ch in testo[inizio + len("#let scheda") :]:
            if ch == "(":
                livello += 1
                if livello == 1:
                    continue
            elif ch == ")":
                livello -= 1
                if livello == 0:
                    break
            corpo.append(ch)
        return set(re.findall(r"(?:^|,)\s*([a-z][a-z-]*)\s*:", "".join(corpo), re.M))

    @staticmethod
    def _parametri_emessi(src: str) -> set[str]:
        """I nomi che l'esportatore scrive dentro le chiamate `#scheda(...)`."""
        return {
            m.group(1)
            for blocco in re.findall(r"#scheda\(\n(.*?)\n\)", src, re.S)
            for m in re.finditer(r"^  ([a-z][a-z-]*):", blocco, re.M)
        }

    def test_nessun_parametro_inventato(self):
        """Ogni nome emesso esiste nella firma del template — e viceversa."""
        firma = self._firma_template()
        emessi = self._parametri_emessi(self.src)
        self.assertTrue(emessi, "nessuna chiamata #scheda( trovata nel sorgente")
        self.assertEqual(emessi - firma, set(),
                         "l'esportatore passa parametri che il template non ha")
        # I facoltativi non compaiono se il master non li ha: si controlla che
        # ogni parametro della firma sia almeno RAGGIUNGIBILE, non obbligatorio.
        mai_usati = firma - emessi
        self.assertEqual(mai_usati, set(),
                         f"parametri del template che nessuna scheda riempie: {mai_usati}")

    def test_una_chiamata_per_scheda(self):
        self.assertEqual(self.src.count("#scheda("), 6)
        self.assertEqual(len(self.pezzi), 6)
        for etichetta, corpo in self.pezzi:
            with self.subTest(scheda=etichetta):
                self.assertEqual(corpo.count("#scheda("), 1)   # --per-scheda: una sola
                self.assertRegex(etichetta, r"^\d+-[a-z0-9-]+$")

    def test_ritratti_puntano_a_file_veri(self):
        """I percorsi Typst sono relativi alla RADICE: qui si verifica che esistano."""
        percorsi = re.findall(r'ritratto: "([^"]+)"', self.src)
        self.assertEqual(len(percorsi), 6)
        for p in percorsi:
            with self.subTest(ritratto=p):
                self.assertTrue((ROOT / p.lstrip("/")).is_file(), f"ritratto assente: {p}")

    def test_niente_apparato_sul_fascicolo_delle_schede(self):
        """`front_matter: false` nel manifest → nessuna copertina da saltare."""
        self.assertIn("apparato: false", self.src)


if __name__ == "__main__":
    unittest.main()
