"""confronta_mappe: due versioni della stessa mappa, misurate cella per cella.

Il confronto deve essere ripetibile al byte, nullo su una mappa contro se
stessa e capace di vedere una cella sola.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import confronta_mappe as M  # noqa: E402

STANZA = [
    "🏰🏰🏰🚪🏰🏰🏰🏰",
    "🏰⬜⬜⬜⬜⬜⬜🏰",
    "🏰⬜🔵⬜⬜⬜⬜🏰",
    "🏰⬜⬜⬜⬜⬜⬜🏰",
    "🏰⬜⬜⬜⬜🔴⬜🏰",
    "🏰🏰🏰🏰🏰🏰🏰🏰",
]


def _master(cartella: Path, nome: str, righe: list[str], titolo: str = "MAPPA 9Z: Stanza di prova") -> Path:
    corpo = [f"## {titolo}", "", "```", titolo,
             "COL →  " + " ".join(chr(65 + i) for i in range(len(righe[0])))]
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(righe, 1)]
    corpo += ["@north N", "@tipo tattica interni", "```", ""]
    p = cartella / nome
    p.write_text("\n".join(corpo), encoding="utf-8")
    return p


def _esegui(*argv) -> int:
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        return M.main(list(argv))


class TestConfrontaMappe(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_due_esecuzioni_identiche_al_byte(self):
        a = _master(self.d, "a.md", STANZA)
        righe = list(STANZA)
        righe[3] = "🏰⬜⬜🏰⬜⬜⬜🏰"
        b = _master(self.d, "b.md", righe)
        uscite = []
        for k in (1, 2):
            j, s = self.d / f"c{k}.json", self.d / f"c{k}.svg"
            self.assertEqual(_esegui(str(a), str(b), "--json", str(j), "--svg", str(s)), 0)
            uscite.append((j.read_bytes(), s.read_bytes()))
        self.assertEqual(uscite[0], uscite[1])
        dato = json.loads(uscite[0][0])
        self.assertEqual(list(dato), sorted(dato))

    def test_versioni_git_identiche_al_byte(self):
        master = "08_La Battaglia Di Hammerfist/ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md"
        if not (M.REPO / master).exists():
            self.skipTest("master di ARC-08 assente")
        uscite = []
        for k in (1, 2):
            out = self.d / f"out{k}"
            self.assertEqual(_esegui("--versioni", "A=HEAD", "C=HEAD", "--base", "C",
                                     "--estrai", str(self.d / f"estr{k}"), "--out", str(out), master), 0)
            uscite.append(sorted((p.relative_to(out).as_posix(), p.read_bytes())
                                 for p in out.rglob("*") if p.is_file()))
        self.assertEqual(uscite[0], uscite[1])
        dato = json.loads(dict(uscite[0])["confronto.json"])
        for voce in dato["mappe"]:
            self.assertEqual(voce["confronti"]["A→C"]["celle_cambiate"]["simboli"], 0)

    def test_mappa_contro_se_stessa(self):
        a = _master(self.d, "a.md", STANZA)
        q = M.misura_file([a])[(a, 1)]
        esito = M.confronta(q, q)
        self.assertEqual(esito["celle_cambiate"]["simboli"], 0)
        self.assertEqual(esito["celle_cambiate"]["classi"], 0)
        self.assertEqual(esito["transizioni"], [])
        self.assertEqual(esito["voto"]["delta"], 0)
        self.assertEqual(esito["rilievi_spariti"], [])
        self.assertEqual(esito["rilievi_comparsi"], [])
        presenti = {k: v for k, v in esito["jaccard_classi"].items() if v is not None}
        self.assertTrue(presenti)
        self.assertTrue(all(v == 1.0 for v in presenti.values()))
        self.assertEqual(esito["jaccard_gruppi"], {"blocco": 1.0, "percorribile": 1.0})

    def test_una_cella_cambiata(self):
        a = _master(self.d, "a.md", STANZA)
        righe = list(STANZA)
        righe[3] = "🏰⬜⬜🏰⬜⬜⬜🏰"  # un muro in D04, dove c'era pavimento
        b = _master(self.d, "b.md", righe)
        qa, qb = M.misura_file([a])[(a, 1)], M.misura_file([b])[(b, 1)]
        esito = M.confronta(qa, qb)
        self.assertEqual(esito["celle_cambiate"]["simboli"], 1)
        self.assertEqual(esito["celle_cambiate"]["classi"], 1)
        self.assertEqual(esito["celle_cambiate"]["quota_simboli"], round(1 / 48, 4))
        self.assertEqual(esito["transizioni"], [[".→M", 1]])
        self.assertEqual(esito["_cambi"], [(3, 3, ".", "M")])
        self.assertLess(esito["jaccard_classi"]["M"], 1.0)
        self.assertEqual(esito["jaccard_classi"]["U"], 1.0)
        svg = M.svg_affiancato([("prima", qa, esito["_cambi"]), ("dopo", qb, esito["_cambi"])], "prova")
        self.assertEqual(svg.count(f'stroke="{M.ROSSO}"'), 2)

    def test_abbinamento_per_titolo_codice_e_ordine(self):
        vecchie = ["MAPPA 1A-2: Torrione", "MAPPA 1A-3: Campo (griglia strategica)", "Senza codice"]
        nuove = ["MAPPA 1A-3: Campo (vista strategica)", "MAPPA 1A-2: Torrione", "Altro titolo", "MAPPA 7: nuova"]
        coppie, sole_n, sole_v = M.abbina(vecchie, nuove)
        self.assertEqual(coppie[2], (1, "titolo"))
        self.assertEqual(coppie[1], (2, "codice"))
        self.assertEqual(coppie[3], (3, "ordine"))
        self.assertEqual(sole_n, [4])
        self.assertEqual(sole_v, [])

    def test_errore_d_uso(self):
        import contextlib
        import io
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(_esegui(str(self.d / "manca.md"), str(self.d / "manca.md")), 2)
            self.assertEqual(_esegui("solo-uno.md"), 2)


if __name__ == "__main__":
    unittest.main()
