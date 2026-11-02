"""qualita_mappe (ADR-0098): le metriche dello standard di qualita' delle mappe.

Come per il collaudo, ogni controllo ha un caso che morde e uno che tace.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import qualita_mappe as Q  # noqa: E402


def _master(cartella: Path, nome: str, righe: list[str], direttive=(), legenda: str = "",
            intestazione: str = "", banner: str = "") -> Path:
    corpo = ["## MAPPA PROVA", "", "```"]
    if banner:
        corpo.append(banner)
    if intestazione:
        corpo.append(intestazione)
    corpo.append("COL →  " + " ".join(chr(65 + i) for i in range(len(righe[0]))))
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(righe, 1)]
    if legenda:
        corpo.append("LEGENDA · " + legenda)
    corpo += list(direttive) + ["```", ""]
    p = cartella / nome
    p.write_text("\n".join(corpo), encoding="utf-8")
    return p


def _misura(p: Path) -> Q.Qualita:
    return Q.misura(p, {})[0]


def _codici(p: Path) -> list[str]:
    return [r["codice"] for r in _misura(p).rilievi if not r["deroga"]]


STANZA = [
    "🏰🏰🏰🚪🏰🏰",
    "🏰⬜⬜⬜⬜🏰",
    "🏰⬜🔵⬜⬜🏰",
    "🏰⬜⬜🔴⬜🏰",
    "🏰🏰🏰🏰🏰🏰",
]
NORD = ["@north N", "@tipo tattica interni"]


def _sala(lato=20, pilastro=False, porte=1, fra_porte=12):
    """Una sala chiusa da muri, con porte sul lato nord (a ``fra_porte``
    colonne l'una dall'altra) e un blocco al centro."""
    righe = [["⬜"] * lato for _ in range(lato)]
    for i in range(lato):
        righe[0][i] = righe[-1][i] = righe[i][0] = righe[i][-1] = "🏰"
    for k in range(porte):
        righe[0][3 + fra_porte * k] = "🚪"
    if pilastro:
        for y in range(8, 12):
            for x in range(8, 12):
                righe[y][x] = "🏰"
    righe[2][2] = "🔵"
    righe[lato - 3][lato - 3] = "🔴"
    return ["".join(r) for r in righe]


class TestQualita(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_una_stanza_pulita_prende_cento(self):
        q = _misura(_master(self.tmp, "ok.md", STANZA, NORD))
        self.assertEqual(q.rilievi, [])
        self.assertEqual(q.voto(), 100)
        # la porta conta come aperta: 12 di pavimento e 1 di porta su 30
        self.assertEqual(q.m["libere"], round(13 / 30, 3))

    def test_l_intestazione_che_mente_e_un_errore(self):
        p = _master(self.tmp, "d.md", STANZA, NORD, intestazione="STANZA — 8 col × 5 righe · 1,5 m")
        self.assertIn("scala/dichiarata", _codici(p))
        self.assertTrue(_misura(p).voto() <= 88)

    def test_l_intestazione_giusta_tace(self):
        p = _master(self.tmp, "d2.md", STANZA, NORD, intestazione="STANZA — 6 col × 5 righe · 1,5 m")
        self.assertNotIn("scala/dichiarata", _codici(p))

    def test_una_direttiva_fuori_griglia_e_un_errore(self):
        p = _master(self.tmp, "f.md", STANZA, NORD + ["@mark 1 ; Z40 ; nessuno"])
        self.assertIn("direttive/fuori-griglia", _codici(p))

    def test_una_direttiva_dentro_la_griglia_tace(self):
        p = _master(self.tmp, "f2.md", STANZA, NORD + ["@mark 1 ; C03 ; il PG", "@path giro ; B02 E04 loop"])
        self.assertNotIn("direttive/fuori-griglia", _codici(p))

    def test_la_tattica_a_tre_metri_avvisa(self):
        p = _master(self.tmp, "s.md", STANZA, NORD, intestazione="STANZA — 6 col × 5 righe · 3 m")
        self.assertIn("scala/tattica-non-a-1-5", _codici(p))
        p2 = _master(self.tmp, "s2.md", STANZA, ["@north N", "@tipo strategica"],
                     intestazione="STANZA — 6 col × 5 righe · 3 m")
        self.assertNotIn("scala/tattica-non-a-1-5", _codici(p2))

    def test_il_titolo_che_dice_un_altra_misura(self):
        p = _master(self.tmp, "t.md", STANZA, NORD, banner="SALA DI PROVA — 60 m × 40 m (pianta)")
        self.assertIn("scala/titolo", _codici(p))
        p2 = _master(self.tmp, "t2.md", STANZA, NORD, banner="SALA DI PROVA — 9 m × 7,5 m (pianta)")
        self.assertNotIn("scala/titolo", _codici(p2))

    def test_anelli_e_senza_anelli(self):
        """Una sala con un blocco di muro al centro ha un anello; senza, nessuno."""
        piena = _misura(_master(self.tmp, "a.md", _sala(pilastro=False), NORD))
        self.assertEqual(piena.m["anelli_strutturali"], 0)
        self.assertIn("struttura/senza-anelli", [r["codice"] for r in piena.rilievi])
        anello = _misura(_master(self.tmp, "b.md", _sala(pilastro=True), NORD))
        self.assertEqual(anello.m["anelli_strutturali"], 1)
        self.assertNotIn("struttura/senza-anelli", [r["codice"] for r in anello.rilievi])

    def test_un_ingresso_solo_avvisa_due_tacciono(self):
        uno = _codici(_master(self.tmp, "i1.md", _sala(porte=1), NORD))
        self.assertIn("struttura/un-ingresso", uno)
        due = _codici(_master(self.tmp, "i1b.md", _sala(porte=2), NORD))
        self.assertNotIn("struttura/un-ingresso", due)

    def test_due_varchi_vicini_sono_un_ingresso(self):
        """Il caso sfruttato dal riparatore (RICERCA-STRUMENTI-MAPPE.md §5): due
        porte a due quadretti nella stessa stanza non sono due ingressi."""
        q = _misura(_master(self.tmp, "v1.md", _sala(porte=2, fra_porte=2), NORD))
        self.assertEqual(q.m["varchi"], 2)
        self.assertEqual(q.m["ingressi"], 1)
        self.assertIn("struttura/un-ingresso", [r["codice"] for r in q.rilievi])

    def test_due_varchi_lontani_sono_due_ingressi(self):
        q = _misura(_master(self.tmp, "v2.md", _sala(porte=2, fra_porte=12), NORD))
        self.assertEqual((q.m["varchi"], q.m["ingressi"]), (2, 2))
        self.assertNotIn("struttura/un-ingresso", [r["codice"] for r in q.rilievi])

    def test_dieci_passi_si_nove_no(self):
        """Fra due porte nel muro nord a d colonne si fanno 1 + d + 1 passi
        ortogonali (si scende, si cammina, si risale): d = 8 sono 10 passi e due
        ingressi, d = 7 sono 9 passi e uno solo."""
        dieci = _misura(_master(self.tmp, "p10.md", _sala(porte=2, fra_porte=8), NORD))
        self.assertEqual(dieci.m["ingressi"], 2)
        nove = _misura(_master(self.tmp, "p9.md", _sala(porte=2, fra_porte=7), NORD))
        self.assertEqual(nove.m["ingressi"], 1)

    def test_varchi_che_non_si_raggiungono_sono_distinti(self):
        """Due porte vicine su due stanze separate da un muro: a piedi non si
        passa dall'una all'altra, quindi sono due ingressi."""
        righe = [list(r) for r in _sala(porte=2, fra_porte=2)]
        for y in range(1, 19):
            righe[y][4] = "🏰"
        q = _misura(_master(self.tmp, "v3.md", ["".join(r) for r in righe], NORD))
        self.assertEqual(q.m["ingressi"], 2)

    def test_la_deroga_spegne_il_rilievo_e_la_penalita(self):
        d = NORD + ["@deroga struttura/un-ingresso ; la cripta del boss ha una porta sola, di proposito"]
        q = _misura(_master(self.tmp, "i2.md", _sala(porte=1, pilastro=True), d))
        self.assertNotIn("struttura/un-ingresso", [r["codice"] for r in q.rilievi if not r["deroga"]])
        self.assertEqual(q.penalita()["qualita"], 0)

    def test_scale_e_portali_contano_come_ingressi(self):
        righe = _sala(porte=1, pilastro=True)
        righe[10] = righe[10][:2] + "🌀" + righe[10][3:]
        q = _misura(_master(self.tmp, "i3.md", righe, NORD))
        self.assertEqual(q.m["ingressi"], 2)

    def test_distanza_fra_le_fazioni(self):
        q = _misura(_master(self.tmp, "fz.md", _sala(lato=12), NORD))
        # dal PG in C03 al nemico in J10: 7 diagonali = 7 * 1,5 quadretti
        self.assertEqual(q.m["distanza_min_q"], 10.5)
        self.assertEqual(q.m["distanza_min_m"], 15.8)

    def test_fazioni_lontane(self):
        righe = ["🟩" * 50 for _ in range(4)]
        righe[1] = "🔵" + "🟩" * 48 + "🔴"
        p = _master(self.tmp, "fl.md", righe, ["@north N", "@tipo tattica esterno"])
        self.assertIn("fazioni/lontane", _codici(p))

    def test_fazioni_a_contatto(self):
        righe = list(STANZA)
        righe[2] = "🏰⬜🔵🔴⬜🏰"
        righe[3] = "🏰⬜⬜⬜⬜🏰"
        self.assertIn("fazioni/a-contatto", _codici(_master(self.tmp, "ac.md", righe, NORD)))

    def test_vicoli_ciechi_vuoti(self):
        righe = [list("🏰" * 12) for _ in range(9)]
        for x in range(1, 11):
            righe[4][x] = "⬜"          # corridoio est-ovest
        for x in (2, 5, 8):
            righe[2][x] = righe[3][x] = "⬜"   # tre rami ciechi verso nord
        righe[4][1] = "🔵"
        q = _misura(_master(self.tmp, "v.md", ["".join(r) for r in righe], NORD))
        self.assertGreaterEqual(q.m["vicoli_vuoti"], 3)
        self.assertIn("struttura/vicoli-ciechi", [r["codice"] for r in q.rilievi])

    def test_un_vicolo_con_qualcosa_in_fondo_non_e_vuoto(self):
        righe = [list("🏰" * 12) for _ in range(9)]
        for x in range(1, 11):
            righe[4][x] = "⬜"
        for x in (2, 5, 8):
            righe[2][x] = "🏺"
            righe[3][x] = "⬜"
        q = _misura(_master(self.tmp, "v2.md", ["".join(r) for r in righe], NORD))
        self.assertEqual(q.m["vicoli_vuoti"], 0)

    def test_il_telo_enorme_e_le_tende_a_grappolo(self):
        righe = ["🟩" * 16 for _ in range(16)]
        telo = ["🟩" + "🎪" * 14 + "🟩" for _ in range(14)]
        p = _master(self.tmp, "te.md", [righe[0]] + telo + [righe[0]], ["@north N", "@tipo tattica esterno"])
        self.assertIn("oggetti/telo-enorme", _codici(p))
        grappolo = ["🟩⛺⛺🟩🟩", "🟩⛺⛺🟩🟩", "🟩🟩🟩🟩🟩"]
        p2 = _master(self.tmp, "tg.md", grappolo, ["@north N", "@tipo tattica esterno"])
        self.assertIn("oggetti/tende-a-grappolo", _codici(p2))
        sole = ["⛺🟩⛺🟩⛺", "🟩🟩🟩🟩🟩", "⛺🟩⛺🟩⛺"]
        p3 = _master(self.tmp, "ts.md", sole, ["@north N", "@tipo tattica esterno"])
        self.assertNotIn("oggetti/tende-a-grappolo", _codici(p3))

    def test_il_fuoco_sotto_il_telo(self):
        righe = ["🟩🟩🟩🟩🟩", "🟩🎪🔥🟩🟩", "🟩🟩🟩🟩🟩"]
        p = _master(self.tmp, "fu.md", righe, ["@north N", "@tipo tattica esterno"])
        self.assertIn("oggetti/fuoco-sotto-il-telo", _codici(p))
        lontano = ["🟩🟩🟩🟩🟩", "🎪🟩🟩🔥🟩", "🟩🟩🟩🟩🟩"]
        p2 = _master(self.tmp, "fu2.md", lontano, ["@north N", "@tipo tattica esterno"])
        self.assertNotIn("oggetti/fuoco-sotto-il-telo", _codici(p2))

    def test_la_taglia_che_non_entra(self):
        righe = ["🏰🏰🏰🏰🏰", "🏰⬜🔴⬜🏰", "🏰⬜🔵⬜🏰", "🏰🏰🏰🏰🏰"]
        p = _master(self.tmp, "tg.md", ["🏰🏰🏰🏰🏰", "🏰🏰🔴🏰🏰", "🏰⬜🔵⬜🏰", "🏰🏰🏰🏰🏰"],
                    NORD + ["@taglia C02 ; Grande"])
        self.assertIn("taglia/non-entra", _codici(p))
        p2 = _master(self.tmp, "tg2.md", righe, NORD + ["@taglia C02 ; Grande"])
        self.assertNotIn("taglia/non-entra", _codici(p2))

    def test_il_drago_su_un_quadretto_senza_taglia(self):
        righe = ["🟩🟩🟩🟩🟩", "🟩🐉🟩🟩🟩", "🟩🔵🟩🟩🟩"]
        p = _master(self.tmp, "dr.md", righe, ["@north N", "@tipo tattica esterno"], legenda="🐉 drago rosso adulto")
        self.assertIn("taglia/non-dichiarata", _codici(p))
        p2 = _master(self.tmp, "dr2.md", righe, ["@north N", "@tipo tattica esterno", "@taglia B02 ; Enorme"],
                     legenda="🐉 drago rosso adulto")
        self.assertNotIn("taglia/non-dichiarata", _codici(p2))
        p3 = _master(self.tmp, "dr3.md", righe, ["@north N", "@tipo tattica esterno"],
                     legenda="🐉 impronta del drago")
        self.assertNotIn("taglia/non-dichiarata", _codici(p3))

    def test_il_blocco_pieno_di_muratura(self):
        righe = ["🟩" * 12] + ["🟩" + "⬛" * 10 + "🟩" for _ in range(10)] + ["🟩" * 12]
        p = _master(self.tmp, "bp.md", righe, ["@north N", "@tipo tattica esterno"])
        self.assertIn("funzione/blocco-pieno", _codici(p))

    def test_le_mura_sottili_di_una_fortezza(self):
        righe = ["🟩" * 14] + ["🟩" + "🏰" * 12 + "🟩"] + ["🟩🏰" + "⬜" * 10 + "🏰🟩" for _ in range(10)] \
            + ["🟩" + "🏰" * 12 + "🟩"] + ["🟩" * 14]
        p = _master(self.tmp, "mu.md", righe, ["@north N", "@tipo tattica esterno"],
                    banner="LA FORTEZZA DI PROVA (pianta del cortile)")
        self.assertIn("coerenza/mura-sottili", _codici(p))
        p2 = _master(self.tmp, "mu2.md", righe, ["@north N", "@tipo tattica esterno"],
                     banner="IL RECINTO DI PROVA (pianta del cortile)")
        self.assertNotIn("coerenza/mura-sottili", _codici(p2))

    def test_le_metriche_della_strategica_saltano_i_controlli_tattici(self):
        righe = ["🟩" * 50 for _ in range(4)]
        righe[1] = "🔵" + "🟩" * 48 + "🔴"
        p = _master(self.tmp, "st.md", righe, ["@north N", "@tipo strategica"])
        self.assertNotIn("fazioni/lontane", _codici(p))

    def test_la_classifica_unisce_le_copie_e_parte_dal_peggiore(self):
        a = _master(self.tmp, "c1.md", STANZA, NORD)
        b = _master(self.tmp, "c2.md", STANZA, NORD)
        c = _master(self.tmp, "c3.md", STANZA, NORD + ["@mark 1 ; Z40 ; fuori"])
        esiti = [Q.misura(p, {})[0] for p in (a, b, c)]
        tab = Q.classifica(esiti).splitlines()
        self.assertEqual(len(tab), 4)  # intestazione, separatore, due gruppi
        self.assertIn("| 1 | 88 |", tab[2])
        self.assertIn("| 2 |", tab[3])

    def test_il_json_e_lo_strict(self):
        p = _master(self.tmp, "j.md", STANZA, NORD + ["@mark 1 ; Z40 ; fuori"])
        out = self.tmp / "q.json"
        self.assertEqual(Q.main([str(p), "--json", str(out)]), 0)
        dati = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(dati["schema"], "map_quality/1")
        m = dati["mappe"][0]
        self.assertEqual(m["voto"], 88)
        self.assertIn("metriche", m)
        self.assertEqual(Q.main([str(p), "--strict"]), 1)
        pulita = _master(self.tmp, "j2.md", STANZA, NORD)
        self.assertEqual(Q.main([str(pulita), "--strict"]), 0)

    def test_il_file_che_manca(self):
        self.assertEqual(Q.main([str(self.tmp / "non-c-e.md")]), 2)

    # --- rilievo e contesto -------------------------------------------------------
    ESTERNO = ["@north N", "@tipo tattica esterno"]

    def test_all_aperto_senza_quota_avvisa(self):
        cod = _codici(_master(self.tmp, "e.md", STANZA, self.ESTERNO))
        self.assertIn("contesto/quota-mancante", cod)

    def test_al_chiuso_la_quota_non_serve(self):
        self.assertNotIn("contesto/quota-mancante", _codici(_master(self.tmp, "i.md", STANZA, NORD)))

    def test_quota_e_dislivello_dichiarati_tacciono_e_si_leggono(self):
        p = _master(self.tmp, "q.md", STANZA, self.ESTERNO + [
            "@quota 1200 ft ; s.l.m.", "@dislivello +120 m ; sulla piana di Talar"])
        q = _misura(p)
        self.assertNotIn("contesto/quota-mancante", [r["codice"] for r in q.rilievi])
        self.assertAlmostEqual(q.m["quota"]["m"], 365.8, places=1)
        self.assertEqual(q.m["dislivello"], {"m": 120.0, "riferimento": "sulla piana di Talar"})

    def test_la_quota_illeggibile_e_un_errore(self):
        p = _master(self.tmp, "x.md", STANZA, self.ESTERNO + ["@quota alta ; s.l.m.", "@dislivello 0 m"])
        self.assertIn("contesto/quota-illeggibile", _codici(p))

    def test_lo_stesso_luogo_con_due_quote(self):
        a = _master(self.tmp, "a.md", STANZA, NORD + ["@luogo Hammerfist, porta", "@quota 900 m"])
        b = _master(self.tmp, "b.md", STANZA, NORD + ["@luogo hammerfist, porta", "@quota 600 m"])
        c = _master(self.tmp, "c.md", STANZA, NORD + ["@luogo Hammerfist, porta", "@quota 903 m"])
        esiti = Q.misura(a, {}) + Q.misura(b, {}) + Q.misura(c, {})
        Q.confronta_luoghi(esiti)
        self.assertTrue(all("contesto/quote-discordi" in [r["codice"] for r in q.rilievi] for q in esiti))
        concordi = Q.misura(a, {}) + Q.misura(c, {})
        Q.confronta_luoghi(concordi)
        self.assertFalse(any(q.rilievi for q in concordi))


if __name__ == "__main__":
    unittest.main()
