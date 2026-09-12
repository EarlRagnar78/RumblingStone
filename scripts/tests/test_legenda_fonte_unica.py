"""La legenda ha una casa sola — `legend/single-source` (ADR-0048, 2026-09-12).

Il difetto non era un errore presente: al momento della migrazione i cinque
posti in cui viveva la legenda — `SYMBOLS` nel renderer e i quattro `set` nei
consumatori — **coincidevano tutti**. Era che niente impediva il prossimo.

🔴 **E il prossimo era gia' arrivato due volte.** `⛺` (tenda) non era in
`WALL_SYMS` e non bloccava la vista in Foundry mentre lo faceva nell'SVG:
ADR-0042. `⛰` (montagne) idem su 2.423 celle: ADR-0043. Due ADR, due giri di
test, due mesi — per due sintomi della **stessa** causa, perche' la fonte unica
stava in una PR chiusa dal 26 luglio.

Questo file e' il cancello che quella decisione dichiarava **assente**:

- `TestNessunConsumatoreHaUnSetProprio` e' `legend/single-source`. Analizza
  l'AST dei cinque consumatori e boccia **qualunque** insieme di emoji
  dichiarato a livello di modulo. E' l'unico dei test qui che impedisce il
  difetto *futuro*; tutti gli altri verificano quello passato.
- `TestLaMigrazioneNonHaCambiatoNiente` e' la prova che il refactor e' stato
  a costo zero sugli artefatti — il criterio d'uscita di ADR-0048 §4.

🔎 **E il gate ha morso al primo uso vero**, come gia' `decisioni_dm.py`: ha
trovato in `render_map_blender.py` **tre tabelle** (`ALTEZZE`, `PIATTI`,
`TEXTURE`) che nessuna misura di questo lotto aveva contato — l'ADR ne
dichiarava quattro, erano sette. Una portava un commento fossile, «edificio,
tenda, dais» accanto a ⬛: il significato di **prima** di ADR-0042, sopravvissuto
otto giorni dopo la decisione che lo aveva abolito.

⚠️ **Il limite, dichiarato.** Il gate vede un set **letterale**. Chi costruisse
il proprio insieme a runtime (`{s for s in ... if ...}`) gli sfuggirebbe. E'
la stessa forma di limite di ADR-0043 — un marcatore dimenticato resta
invisibile — e vale la pena saperlo invece di crederlo chiuso.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import legenda  # noqa: E402

CONSUMATORI = ("render_map_svg.py", "export_uvtt.py", "import_ultraclear.py",
               "compile_map_json.py", "render_map_blender.py")


def _e_emoji(testo: str) -> bool:
    """Un simbolo di legenda: un pittogramma, non una parola accentata."""
    return any(ord(c) >= 0x2190 for c in testo) and len(testo) <= 4


def insiemi_di_emoji_cablati(sorgente: str) -> list[str]:
    """I nomi assegnati, a livello di modulo, a un set/dict/lista di emoji."""
    colpevoli = []
    for nodo in ast.parse(sorgente).body:
        if not isinstance(nodo, (ast.Assign, ast.AnnAssign)):
            continue
        valore = nodo.value
        if isinstance(valore, ast.Set):
            elementi = valore.elts
        elif isinstance(valore, ast.Dict):
            elementi = [k for k in valore.keys if k is not None]
        elif isinstance(valore, (ast.List, ast.Tuple)):
            elementi = valore.elts
        else:
            continue
        stringhe = [e.value for e in elementi
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        if stringhe and all(_e_emoji(s) for s in stringhe):
            bersagli = [nodo.target] if isinstance(nodo, ast.AnnAssign) else nodo.targets
            for t in bersagli:
                if isinstance(t, ast.Name):
                    colpevoli.append(t.id)
    return colpevoli


class TestNessunConsumatoreHaUnSetProprio(unittest.TestCase):
    """`legend/single-source` — il criterio d'accettazione del lotto 1.1."""

    def test_i_cinque_consumatori_sono_puliti(self):
        for nome in CONSUMATORI:
            sorgente = (ROOT / "scripts" / nome).read_text(encoding="utf-8")
            colpevoli = insiemi_di_emoji_cablati(sorgente)
            self.assertEqual(
                colpevoli, [],
                f"{nome} dichiara una legenda propria ({colpevoli}). La fonte e' "
                f"scripts/legend.yaml: si legge da dmcore.legenda. Prima di "
                f"ADR-0048 questo e' costato due ADR (0042, 0043) per due "
                f"sintomi della stessa causa.")

    def test_il_gate_morde(self):
        """Provato a rovescio: senza questo, il test sopra non prova niente."""
        ricaduta = 'WALL_SYMS = {"🏰", "⬛", "⛰"}\n'
        self.assertEqual(insiemi_di_emoji_cablati(ricaduta), ["WALL_SYMS"])
        con_valori = 'LIGHT_SYMS = {"🏮": (6.0, "ffd9a0"), "🔥": (5.0, "ffb37a")}\n'
        self.assertEqual(insiemi_di_emoji_cablati(con_valori), ["LIGHT_SYMS"])

    def test_non_boccia_cio_che_non_e_una_legenda(self):
        """L'altra meta': un gate che boccia troppo verrebbe spento al primo giro."""
        for innocente in (
            'TROOP_WORDS = ("nani", "nano", "cantitrice")\n',
            'SEV_ORDER = {"ERROR": 0, "WARN": 1}\n',
            'Z_ORDER = ["t_grass", "t_veg", "t_wall"]\n',
            'HEAVY_PATS = {"t_wall", "t_struct"}\n',
        ):
            self.assertEqual(insiemi_di_emoji_cablati(innocente), [], innocente)


class TestLaFonteEUnaSola(unittest.TestCase):
    def test_yaml_e_json_sono_in_sincronia(self):
        esito = subprocess.run([sys.executable, "scripts/build_legend.py", "--check"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_la_pagina_della_skill_e_generata(self):
        esito = subprocess.run(
            [sys.executable, "scripts/build_legenda_skill.py", "--check"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_ogni_simbolo_dichiarato_ha_un_rendering(self):
        for sim, spec in legenda.simboli().items():
            self.assertIn(spec["mode"], ("fill", "unit", "icon"), sim)
            self.assertTrue(spec["fill"].startswith("#"), sim)

    def test_i_set_di_funzione_sono_sottoinsiemi_dei_simboli(self):
        """Un orfano vorrebbe dire che la fonte unica non e' unica."""
        simboli = set(legenda.simboli())
        for nome, insieme in (("muri", legenda.muri()), ("porte", legenda.porte()),
                              ("pericoli", legenda.pericoli()),
                              ("luci", set(legenda.luci()))):
            self.assertEqual(set(insieme) - simboli, set(), nome)

    def test_niente_numeri_di_gioco_nella_legenda(self):
        """ADR-0048 §5: «+4 CA», «20%» e «x2» vivono nei profili, non qui.

        E' cio' che permette di supportare 3.5, PF1e e 5e senza tre legende:
        `half` diventa +4 CA in 3.5 e +2 in 5e, e la legenda non lo sa.
        """
        dati = json.loads((ROOT / "scripts" / "legend.json").read_text(encoding="utf-8"))
        ammessi = {"blocks_movement", "blocks_sight", "blocks_line_of_effect",
                   "deroga_uvtt", "door", "cover", "obscurement", "move_cost",
                   "climb", "swim", "prone_concealment", "destructible",
                   "nameable", "hazard", "light"}
        vocabolario = {
            "cover": {"none", "half", "three_quarters", "total"},
            "obscurement": {"none", "light", "heavy"},
            "climb": {"none", "easy", "moderate", "hard", "sheer"},
            "move_cost": {1, 2, 4},
        }
        for sim, voce in dati["symbols"].items():
            f = voce.get("function", {})
            self.assertEqual(set(f) - ammessi, set(), sim)
            for campo, valori in vocabolario.items():
                if campo in f:
                    self.assertIn(f[campo], valori, f"{sim}.{campo}")

    def test_la_spec_funzionale_e_ratificata_per_intero(self):
        """56 simboli su 56 che una funzione ce l'hanno (DM, 2026-09-12).

        I 7 restanti non sono un buco: 6 sono token di creatura, e la spec
        §4.5 dice che le unita' `function` non ce l'hanno — hanno `unit`.
        Il settimo e' 🔳, nato con ADR-0042 dopo la riverifica della spec, e
        quella decisione la sua funzione la dichiara per esteso.
        """
        con = [s for s, v in legenda.simboli().items()
               if json.loads((ROOT / "scripts" / "legend.json")
                             .read_text(encoding="utf-8"))["symbols"][s].get("function")]
        self.assertEqual(len(con), 56)
        unita = [s for s, v in legenda.simboli().items() if v["mode"] == "unit"]
        self.assertEqual(len(unita), 6)
        for u in unita:
            self.assertNotIn(u, con, f"{u} e' un token: non ha function")


class TestLeDerogheSonoDichiarate(unittest.TestCase):
    """Il muro UVTT deriva dal fatto neutro, meno le deroghe — e ognuna motiva.

    🔴 **La tentazione era un secondo booleano.** `blocks_sight` dice cosa fa
    la cella nella finzione; l'export UVTT ci mette un segmento o no. Sono
    due affermazioni diverse, e metterle in due campi indipendenti avrebbe
    ricreato le due fonti che ADR-0048 ha appena finito di unire: diverrebbero
    in silenzio, come `SYMBOLS` e `WALL_SYMS` prima di ADR-0042.

    Quindi il muro **si deriva**, e chi diverge deve scrivere perche'. Questo
    test e' il prezzo della deroga: senza motivo, e' rossa.
    """

    ATTESE = {"🌲", "🌳", "🚪"}

    def test_ogni_deroga_ha_un_motivo_vero(self):
        for sim, motivo in legenda.deroghe().items():
            self.assertGreater(len(motivo), 60,
                               f"{sim}: una deroga senza motivo e' una svista "
                               f"travestita da decisione")

    def test_le_deroghe_sono_solo_quelle_decise(self):
        """Una deroga nuova non deve poter comparire senza che qualcuno la veda."""
        self.assertEqual(set(legenda.deroghe()), self.ATTESE)

    def test_una_deroga_esiste_solo_dove_c_e_qualcosa_da_derogare(self):
        dati = json.loads((ROOT / "scripts" / "legend.json").read_text(encoding="utf-8"))
        for sim in legenda.deroghe():
            self.assertTrue(dati["symbols"][sim]["function"]["blocks_sight"],
                            f"{sim} deroga da un muro che non ci sarebbe comunque")

    def test_il_muro_e_derivato_non_dichiarato(self):
        """Se qualcuno rimettesse un campo `wall`, sarebbero due fonti di nuovo."""
        sorgente = (ROOT / "scripts" / "legend.yaml").read_text(encoding="utf-8")
        self.assertNotIn("wall: true", sorgente,
                         "il muro si deriva da blocks_sight meno le deroghe")

    def test_la_foresta_e_una_decisione_non_una_dimenticanza(self):
        """🌲 non e' muro per scelta del DM: il glifo del margine e' ADR-0049."""
        self.assertNotIn("🌲", legenda.muri())
        self.assertIn("ADR-0049", legenda.deroghe()["🌲"])


class TestLeAltezzeSonoModuliDiGriglia(unittest.TestCase):
    """Un'altezza non e' un numero libero: e' un multiplo del quadretto.

    Decisione DM del 2026-09-12 — *«muri piccoli 1.5 metri e poi multipli di
    1.5 o approssimazioni piu' vicine possibili»*. Il quadretto del repo e'
    1,5 m per tutti e tre i sistemi (`LEGENDA-FUNZIONALE-SPEC` §3.5), quindi
    cio' che sta in piedi occupa quadretti interi e l'ingombro che si scavalca
    mezzo quadretto.

    Prima erano numeri a occhio — 3.2, 2.2, 1.6, 1.4, 1.1, 0.9, 0.8, 0.6, 0.4,
    -0.3, -0.6 — e nessuno di essi voleva dire niente rispetto alla griglia su
    cui la scena e' costruita.
    """

    PASSO = 0.75  # mezzo quadretto

    def _e_modulo(self, v):
        return abs(v / self.PASSO - round(v / self.PASSO)) < 1e-9

    def test_ogni_altezza_e_un_modulo(self):
        for sim, v in legenda.altezze().items():
            self.assertTrue(self._e_modulo(v),
                            f"{sim} = {v} m non e' un multiplo di mezzo quadretto")

    def test_cio_che_sta_in_piedi_occupa_quadretti_interi(self):
        for sim in ("🗼", "⛰", "🏛", "🌳", "🌲", "🟪", "🏰", "⬛", "🧱", "📦"):
            v = legenda.altezze()[sim]
            self.assertAlmostEqual(v / 1.5, round(v / 1.5), places=9,
                                   msg=f"{sim} = {v} m non e' un quadretto intero")

    def test_il_muro_piccolo_e_un_quadretto(self):
        """La riga che il DM ha dettato: «muri piccoli 1.5 metri»."""
        self.assertEqual(legenda.altezze()["🧱"], 1.5)

    def test_l_acqua_profonda_resta_piu_profonda_di_quella_bassa(self):
        """L'unico posto dove la semantica ha battuto l'arrotondamento.

        `🟦` stava a -0,6: il modulo piu' vicino sarebbe -0,75, lo stesso a cui
        finisce `🌊` (-0,3). Due glifi che esistono per distinguere l'acqua
        alta dalla bassa sarebbero diventati la stessa profondita'. `🟦` prende
        un quadretto pieno, che e' anche quello che «profonda» vuol dire.
        """
        a = legenda.altezze()
        self.assertLess(a["🟦"], a["🌊"])
        self.assertEqual(a["🟦"], -1.5)

    def test_la_scala_resta_leggibile_dal_basso_verso_l_alto(self):
        a = legenda.altezze()
        for basso, alto in (("🌊", "🌿"), ("⛺", "🧱"), ("🧱", "⬛"),
                            ("⬛", "🏰"), ("🏰", "🏛"), ("🏛", "⛰"), ("⛰", "🗼")):
            self.assertLess(a[basso], a[alto], f"{basso} deve stare sotto {alto}")


class TestLaMigrazioneNonHaCambiatoNiente(unittest.TestCase):
    """Il criterio d'uscita di ADR-0048 §4: nessuna regressione visiva."""

    CONGELATI = {
        "muri": {"🏰", "⬛", "⛺", "⛰", "🟪", "🗼", "🏛", "🗿", "📦"},
        "porte": {"🚪"},
        "pericoli": {"🔥", "💥", "💀", "🕳", "⚡", "❄", "🕸", "🌋", "🟧", "🟥"},
        "pesanti": {"t_wall", "t_struct", "t_pillar", "t_mountain"},
        "piatti": {"🚪", "⬇", "🎯", "⭐", "✨", "⚔", "🖼"},
    }

    def test_i_set_valgono_esattamente_quel_che_valevano(self):
        self.assertEqual(set(legenda.muri()), self.CONGELATI["muri"])
        self.assertEqual(set(legenda.porte()), self.CONGELATI["porte"])
        self.assertEqual(set(legenda.pericoli()), self.CONGELATI["pericoli"])
        self.assertEqual(set(legenda.pattern_pesanti()), self.CONGELATI["pesanti"])

    def test_le_tre_tabelle_del_blender_le_ha_trovate_il_gate(self):
        """Non erano in nessuna misura: le ha scoperte `legend/single-source`.

        ⚠️ **I valori delle altezze non sono piu' quelli di allora, e non e'
        una regressione**: il 2026-09-12 il DM le ha portate tutte sul modulo
        di griglia (`TestLeAltezzeSonoModuliDiGriglia`). Qui restano fissate la
        **cardinalita'** delle tre tabelle e i due insiemi che quella decisione
        non tocca, perche' sono la prova che la migrazione le ha prese tutte.
        """
        self.assertEqual(set(legenda.piatti()), self.CONGELATI["piatti"])
        self.assertEqual(len(legenda.altezze()), 31)
        self.assertEqual(len(legenda.texture()), 15)
        self.assertEqual(legenda.altezze()["🗼"], 9.0, "la torre: 6 quadretti")
        self.assertLess(legenda.altezze()["🕳"], 0, "la voragine resta uno scavo")

    def test_il_buco_di_adr_0042_nel_blender_e_chiuso_a_meta(self):
        """⛺ ha la sua altezza; 🔳 no, e la differenza e' voluta.

        🐛 Era il terzo sintomo della causa che ADR-0048 chiude, e il primo
        trovato **da un gate** invece che da un bug al tavolo: tenda e dais si
        estrudevano al default generico di 0,6 m mentre un edificio sta a 3,2.

        Il DM ha deciso la tenda il 2026-09-12 (1 m, *«falle piu' basse»*) e
        insieme il muretto, che era l'unico simbolo chiamato «muro» senza
        altezza. **Il dais no**, e non e' una dimenticanza: `🔳` non compare in
        **nessuna cella** del repo — e' nato con ADR-0042 e non e' ancora stato
        usato. Decidere adesso l'altezza di una pedana che nessuno ha disegnato
        vorrebbe dire inventarla; il giorno che serve, costa zero.
        """
        self.assertEqual(legenda.altezze()["⛺"], 0.75)
        self.assertEqual(legenda.altezze()["🧱"], 1.5)
        self.assertNotIn("🔳", legenda.altezze(),
                         "il dais resta al default finche' qualcuno non lo usa")

    def test_la_tenda_e_piu_bassa_del_muretto_e_il_muretto_del_muro(self):
        """L'ordine che il DM ha dato, come invariante invece che come numeri."""
        a = legenda.altezze()
        self.assertLess(a["⛺"], a["🧱"], "la tenda e' piu' bassa del muretto")
        self.assertLess(a["🧱"], a["🏰"], "il muretto e' piu' basso del muro")
        self.assertLess(a["🏰"], a["🗼"], "e la torre svetta su tutto")

    def test_i_63_simboli_ci_sono_tutti(self):
        """62 era il numero della spec di luglio; 🔳 e' entrato con ADR-0042."""
        self.assertEqual(len(legenda.simboli()), 63)

    def test_i_consumatori_vedono_gli_stessi_valori(self):
        import export_uvtt as eu
        import import_ultraclear as iu
        import render_map_svg as rms
        self.assertEqual(rms.SYMBOLS, legenda.simboli())
        self.assertEqual(rms.HEAVY_PATS, set(legenda.pattern_pesanti()))
        self.assertEqual(eu.WALL_SYMS, set(legenda.muri()))
        self.assertEqual(iu.HAZARD_SYMS, set(legenda.pericoli()))
        import render_map_blender as rmb
        self.assertEqual(rmb.ALTEZZE, legenda.altezze())
        self.assertEqual(rmb.PIATTI, set(legenda.piatti()))
        self.assertEqual(rmb.TEXTURE, legenda.texture())

    def test_le_luci_valgono_ancora_i_quadretti_di_prima(self):
        """La legenda le dichiara in metri; l'uscita non e' cambiata di un byte.

        Decisione DM del 2026-09-12: la spec dava i raggi RAW di 3.5 (torcia
        20 ft, candela 5 ft) e il repo illumina 1,5-3 volte di piu'. Ha vinto
        il codice, perche' le mappe notturne sono state disegnate con questa
        luce. La divergenza si e' chiusa scrivendo in metri i valori del
        codice, non cambiandoli.
        """
        atteso = {"🔥": 5.0, "🏮": 6.0, "⚡": 4.0, "✨": 3.0, "🕯": 3.0, "🔮": 4.0}
        self.assertEqual({s: q for s, (q, _) in legenda.luci().items()}, atteso)

    def test_la_voragine_non_e_una_sorgente_di_luce(self):
        """🕳 stava fra le luci con raggio 0.0, e l'export lo scartava.

        Toglierlo dalla fonte non cambia un byte d'uscita, e la guardia
        `if rng <= 0` resta al suo posto per chi dichiarasse una luce spenta.
        """
        self.assertNotIn("🕳", legenda.luci())
        self.assertIn("if rng <= 0", (ROOT / "scripts" / "export_uvtt.py")
                      .read_text(encoding="utf-8"))
        self.assertIn("🕳", legenda.pericoli(), "resta un pericolo, ed e' quel che e'")


if __name__ == "__main__":
    unittest.main()
