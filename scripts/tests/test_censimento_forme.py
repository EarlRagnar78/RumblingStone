"""Le tre forme dello statblocco, e i master che stanno in un archivio.

🔴 **Il difetto misurato il 2026-09-17, un giorno dopo averlo introdotto io.**
Il censimento del lotto 4d-5 cercava i documenti d'arco con statistiche usando
**una forma sola**, quella con il trattino:

    - Taglia/Tipo: Medio umanoide
    - CA: 22

Il repo ne usa tre. L'arco 07 e l'arco 08 scrivono `**CA:** 22`; il Palio e
l'Abbazia scrivono `**CA** 18`, senza nemmeno i due punti. Con tutte e tre i
documenti d'arco con statistiche passano da **23 a 38**, e fra i quindici che
non si vedevano c'erano `ARC08-01-GUIDA-DM.md` (57 marche, la guida del DM
della Battaglia di Hammerfist) e **un'avventura stand-alone intera**.

⚠️ Il punto non e' la larghezza del regex. E' che il cancello era tarato sul
campione che avevo davanti mentre lo scrivevo, e **dichiarava** una copertura
che non aveva misurato. E' la stessa forma d'errore di ADR-0053 — «non lo so»
travestito da risposta sicura — ripetuta dentro il cancello che quella lezione
avrebbe dovuto presidiare.

## La seconda meta': `_ARCHIVIO` non vuol dire «copia»

`test_archivi_non_indicizzati.py` stabilisce che **chi indicizza salta gli
archivi**, e lo prova a rovescio: dodici istantanee archiviate portarono il
catalogo da 305 a 311 record con un doppione. Quella regola resta, e questo
file non la tocca.

Ma il censimento non indicizza: **sorveglia**, e per chi sorveglia vale la
regola opposta (decisione D1, che lascio' gli SVG dentro `_ARCHIVIO/` apposta).
La prova che serviva distinguere era gia' scritta nel repo: la matrice delle
versioni dell'ARC-07 **dichiara MASTER** otto file che stanno in `_ARCHIVIO/`,
fra cui `Terros.md` — lo statblocco di un boss da **GS 15** che nessuno
strumento raggiungeva.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore.censimento import (  # noqa: E402
    SOGLIA, documenti_con_statistiche, marche, master_archiviati,
)


class TestLeTreForme(unittest.TestCase):
    """Ognuna riconosciuta, e ognuna con l'esempio vero da cui e' stata presa."""

    CASI = {
        "trattino (arco 09, il file Zalkatar)":
            "- Taglia/Tipo: Medio costrutto\n- DV: 10d10\n- CA: 24\n- TS: Temp +3\n",
        "grassetto con due punti (archi 07 e 08)":
            "**CA:** 28 (-2 taglia)\n**PF:** 312 (25d12+175)\n"
            "**TS:** Tempra +21\n**Taglia:** Grande\n",
        "inline senza due punti (il Palio, l'Abbazia)":
            "Umano Guerriero 6. **CA** 18 · **PF** 55 · **TS** Temp +7 · **GS** 8\n",
    }

    def test_ogni_forma_supera_la_soglia(self):
        for etichetta, testo in self.CASI.items():
            with self.subTest(forma=etichetta):
                self.assertGreaterEqual(marche(testo), SOGLIA)

    def test_la_prosa_normale_non_conta(self):
        """Il controprova: allargare il matcher non deve spegnere la selettivita'.

        Senza questo, «riconosce tutte le forme» si otterrebbe riconoscendo
        qualunque cosa — e il cancello sarebbe inutile in un modo che passa.
        """
        prosa = (
            "I PG raggiungono il sanctum di Zalkatar, un illithid warlock che ha\n"
            "corrotto la torre. Diplomazia CD 25 o Intimidire CD 28; puo' essere\n"
            "convinto a rivelare informazioni sulla Red Hand in cambio della liberta'.\n"
            "Le CA delle porte non contano; il livello del personaggio nemmeno.\n"
        )
        self.assertLess(marche(prosa), SOGLIA)

    def test_il_matcher_di_ieri_avrebbe_perso_l_abbazia(self):
        """🔴 La prova all'indietro, sul file vero che il difetto ha nascosto.

        Non su un fixture: sul documento dell'Abbazia com'e' scritto oggi. Con
        la forma sola del trattino vale **zero**; con le tre supera la soglia.
        Se qualcuno restringe di nuovo il matcher, questo test diventa rosso
        prima che l'avventura esca di nuovo dal raggio.
        """
        import re
        abbazia = ROOT / "10-stand-alone/L'abbazia Della Rotta Sicura/abbazia_rotta_sicura.md"
        self.assertTrue(abbazia.exists())
        testo = abbazia.read_text(encoding="utf-8", errors="replace")
        solo_trattino = re.compile(r"^\s*[-*]\s*(Taglia/Tipo|DV|CA|TS|BAB)\s*:", re.M | re.I)
        self.assertEqual(len(solo_trattino.findall(testo)), 0,
                         "se l'Abbazia adesso usa anche la forma col trattino, questa "
                         "prova non dimostra piu' niente: cambiare l'esempio")
        self.assertGreaterEqual(marche(testo), SOGLIA)


class TestIMasterCheStannoInUnArchivio(unittest.TestCase):
    def test_la_matrice_li_dichiara_e_noi_li_leggiamo(self):
        eletti = master_archiviati(ROOT)
        self.assertGreaterEqual(len(eletti), 7,
                                "la matrice delle versioni dichiara MASTER almeno sette "
                                "file dentro _ARCHIVIO/; se ne leggiamo meno, il parser "
                                "ha smesso di vedere la tabella")
        for atteso in ("Terros.md",
                       "PortaleForgia-P4-PianoTerra-COMPLETO-alternative.md",
                       "PortaleForgia-P5-DEFINITIVO-PARTE2.md"):
            with self.subTest(file=atteso):
                self.assertTrue(any(e.endswith(atteso) for e in eletti))

    def test_i_master_dichiarati_esistono(self):
        """Stessa disciplina di R11: un percorso dichiarato si prova."""
        for e in sorted(master_archiviati(ROOT)):
            with self.subTest(file=e.rsplit("/", 1)[-1]):
                self.assertTrue((ROOT / e).exists(), e)

    def test_entrano_nel_censimento_e_le_copie_no(self):
        """La distinzione che tutto questo esiste per fare.

        Un master dichiarato dentro `_ARCHIVIO/` **dev'esserci**; un'istantanea
        archiviata **non deve**. Prima del 4d-6 valeva il secondo caso per
        entrambi, e `Terros.md` — un boss da GS 15 — era fuori dal raggio.
        """
        censiti = set(documenti_con_statistiche(ROOT))
        self.assertIn("07_il Portale Della Forgia Eterna/_ARCHIVIO/Terros.md", censiti)
        copie = [c for c in censiti if "doni-v1-2026-09-12" in c]
        self.assertEqual(copie, [], "un'istantanea archiviata e' rientrata nel censimento: "
                                    "e' il difetto che porto' il catalogo da 305 a 311")

    def test_gli_archivi_restano_fuori_dall_indicizzazione(self):
        """L'altra meta' della regola, e non e' negoziabile qui.

        Questo lotto rende i master d'archivio **raggiungibili** (via POINTER),
        non **indicizzati**: il `source_file` di ogni record resta dentro
        `Bestiario/`. Se un giorno qualcuno indicizzasse l'archivio per
        comodita', la copia tornerebbe a fare il record doppio.
        """
        catalogo = (ROOT / "scripts" / "monster_catalog.yaml").read_text(encoding="utf-8")
        colpevoli = [r.strip() for r in catalogo.splitlines()
                     if "source_file:" in r and ("_ARCHIVIO" in r or "/Old/" in r)]
        self.assertEqual(colpevoli, [], f"record generati da un archivio: {colpevoli}")


class TestICancelliDelLottoSulRepoVero(unittest.TestCase):
    def test_nessun_pointer_cita_un_percorso_che_non_si_apre(self):
        """🔴 Undici POINTER puntavano a `08_.../ARC08-01-GUIDA-DM.md`.

        Un umano capisce quei puntini; `Path.exists()` no. Erano voci che
        *sembravano* agganciate e non lo erano — e il censimento le contava
        buone perche' confrontava sottostringhe invece di risolvere percorsi.
        Adesso sono 130 citazioni e **tutte** si aprono.
        """
        import re
        citazione = re.compile(r"`([^`]+\.md)`")
        guasti = []
        risolti = 0
        for b in sorted((ROOT / "Bestiario").rglob("*.md")):
            for n, riga in enumerate(b.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if not riga.startswith(("**Source**", "**Key stats**")):
                    continue
                for citato in citazione.findall(riga):
                    if "..." in citato or "…" in citato:
                        guasti.append(f"{b.relative_to(ROOT)}:{n} abbreviato → {citato}")
                    elif any((base / citato).exists()
                             for base in (ROOT, b.parent, b.parent.parent)):
                        risolti += 1
                    else:
                        guasti.append(f"{b.relative_to(ROOT)}:{n} inesistente → {citato}")
        self.assertEqual(guasti, [], "POINTER che non puntano:\n  " + "\n  ".join(guasti))
        self.assertGreater(risolti, 125, "quasi nessuna voce dichiara una fonte: "
                                         "il test non sta provando quello che dice")


if __name__ == "__main__":
    unittest.main()
