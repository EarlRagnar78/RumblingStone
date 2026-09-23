"""Il grafo degli import delle creature: la regola di ADR-0066 diventa un test.

`dmcore/caratteristiche.py` e' la **scelta** delle caratteristiche, e il
verificatore non la importa mai, ne' direttamente ne' passando per un altro
modulo. Se una stessa funzione scegliesse e verificasse, un errore di regola
comparirebbe da tutte e due le parti e si confermerebbe da solo: e' successo con
la Tabella 1–1, che la skill e la costante sbagliavano allo stesso modo e un
test confrontava fra loro.

Gli import si leggono con `ast`, **compresi quelli dentro una funzione**: fino
al lotto E3b `genera_attributi.tetti_dai_ts` importava il verificatore cosi', per
non chiudere un ciclo al caricamento, e un controllo sui soli import di modulo
non l'avrebbe visto.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

#: I quattro script del lotto E e i tre moduli di ADR-0066.
SCRIPT_CREATURE = ("genera_attributi", "conformita_statblocchi", "derive_statblocks",
                   "genera_creatura")
MODULI_CREATURE = ("dmcore.progressione", "dmcore.lettura_creatura",
                   "dmcore.caratteristiche")
VERIFICATORE = "conformita_statblocchi"
SCELTA = "dmcore.caratteristiche"


def moduli_noti() -> "dict[str, Path]":
    """{nome importabile: file} per gli script e per `dmcore`."""
    noti = {p.stem: p for p in SCRIPTS.glob("*.py")}
    noti.update({f"dmcore.{p.stem}": p for p in (SCRIPTS / "dmcore").glob("*.py")
                 if p.stem != "__init__"})
    noti["dmcore"] = SCRIPTS / "dmcore" / "__init__.py"
    return noti


def import_di(testo: str, noti) -> "set[str]":
    """I moduli noti che un sorgente importa, in qualunque punto del file."""
    fuori = set()
    for nodo in ast.walk(ast.parse(testo)):
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                if a.name.startswith("dmcore"):
                    fuori.add("dmcore")
                if a.name in noti:
                    fuori.add(a.name)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module and not nodo.level:
            if nodo.module.startswith("dmcore"):
                fuori.add("dmcore")
            if nodo.module in noti:
                fuori.add(nodo.module)
            for a in nodo.names:
                # `from dmcore import tabelle` importa il modulo dmcore.tabelle
                if f"{nodo.module}.{a.name}" in noti:
                    fuori.add(f"{nodo.module}.{a.name}")
    return fuori


def grafo(sorgenti: "dict[str, str]") -> "dict[str, set[str]]":
    """{modulo: moduli che importa}, sui soli moduli di `sorgenti`."""
    return {nome: import_di(testo, sorgenti) - {nome} for nome, testo in sorgenti.items()}


def grafo_del_repo() -> "dict[str, set[str]]":
    return grafo({n: p.read_text(encoding="utf-8") for n, p in moduli_noti().items()})


def raggiungibili(g, da: str) -> "set[str]":
    visti, da_fare = set(), [da]
    while da_fare:
        n = da_fare.pop()
        for m in g.get(n, ()):
            if m not in visti:
                visti.add(m)
                da_fare.append(m)
    return visti


def percorso(g, da: str, a: str) -> "list[str] | None":
    """Il primo percorso di import da `da` ad `a`, per dire *come* ci si arriva."""
    coda, prima = [da], {da: None}
    while coda:
        n = coda.pop(0)
        if n == a:
            fuori = [n]
            while prima[fuori[-1]] is not None:
                fuori.append(prima[fuori[-1]])
            return fuori[::-1]
        for m in sorted(g.get(n, ())):
            if m not in prima:
                prima[m] = n
                coda.append(m)
    return None


def cicli(g, nodi) -> "list[list[str]]":
    """I cicli che passano per almeno uno di `nodi`."""
    fuori = []
    for n in nodi:
        for m in sorted(g.get(n, ())):
            ritorno = percorso(g, m, n)
            if ritorno:
                ciclo = [n] + ritorno
                if sorted(ciclo[:-1]) not in [sorted(c[:-1]) for c in fuori]:
                    fuori.append(ciclo)
    return fuori


class TestIlGrafoDelRepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = grafo_del_repo()

    def test_i_nodi_esistono(self):
        for n in SCRIPT_CREATURE + MODULI_CREATURE:
            self.assertIn(n, self.g)

    def test_nessun_ciclo(self):
        self.assertEqual(cicli(self.g, SCRIPT_CREATURE + MODULI_CREATURE), [])

    def test_il_verificatore_non_arriva_alla_scelta(self):
        via = percorso(self.g, VERIFICATORE, SCELTA)
        self.assertIsNone(via, "conformita_statblocchi arriva a dmcore.caratteristiche: "
                          + " → ".join(via or []))

    def test_nessun_modulo_del_verificatore_arriva_alla_scelta(self):
        for m in sorted(raggiungibili(self.g, VERIFICATORE)):
            with self.subTest(modulo=m):
                self.assertNotIn(SCELTA, raggiungibili(self.g, m) | {m})

    def test_la_libreria_non_importa_gli_script(self):
        """`dmcore` e' la libreria: se importasse uno script, il grafo tornerebbe
        a essere quello di prima, con due script che si reggono a vicenda."""
        for m in MODULI_CREATURE:
            with self.subTest(modulo=m):
                self.assertEqual({n for n in self.g[m] if not n.startswith("dmcore")}, set())

    def test_il_verificatore_non_importa_il_generatore(self):
        self.assertNotIn("genera_attributi", raggiungibili(self.g, VERIFICATORE))


class TestIlControlloMorde(unittest.TestCase):
    """Il controllo, su grafi finti: deve vedere l'import indiretto e quello pigro."""

    def test_import_diretto(self):
        g = grafo({"conformita_statblocchi": "import dmcore.caratteristiche\n",
                   "dmcore.caratteristiche": "", "dmcore": ""})
        self.assertEqual(percorso(g, VERIFICATORE, SCELTA), [VERIFICATORE, SCELTA])

    def test_import_indiretto_e_dentro_una_funzione(self):
        g = grafo({
            "conformita_statblocchi": "from dmcore import lettura_creatura as L\n",
            "dmcore.lettura_creatura": "def f():\n    from dmcore.caratteristiche import genera\n",
            "dmcore.caratteristiche": "", "dmcore": ""})
        self.assertEqual(percorso(g, VERIFICATORE, SCELTA),
                         [VERIFICATORE, "dmcore.lettura_creatura", SCELTA])

    def test_il_ciclo_pigro_di_prima(self):
        """Il grafo com'era fino a E3b: il verificatore importava il generatore,
        e il generatore il verificatore dentro `tetti_dai_ts`."""
        g = grafo({"conformita_statblocchi": "import genera_attributi as GA\n",
                   "genera_attributi": "def tetti_dai_ts():\n    import conformita_statblocchi as C\n"})
        self.assertEqual(len(cicli(g, ("conformita_statblocchi",))), 1)


if __name__ == "__main__":
    unittest.main()
