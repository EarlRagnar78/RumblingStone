"""I prompt media della campagna non citano opere protette (piano LEVEL-DESIGN, lotto D4).

`campaign/ai-media-prompts/` è versionato e pubblico. Fino al 2026-11-27 i
prompt chiedevano «visual style of Doctor Strange», «in the style of Alan Lee»,
la colonna sonora di un film: 57 righe in 12 file. ADR-0015 §5 vieta di
nominare artisti viventi e opere altrui; il lotto D4 le ha riscritte come
descrizioni di stile (luce, palette, scala, strumenti), e questo test impedisce
che tornino.

L'elenco è chiuso e scritto a mano: titoli, franchise, compositori e artisti
trovati nei file il 2026-11-27, più i più probabili a tornare. Le parole comuni
che somigliano a un titolo («alien biology», il «warhammer» arma, «gladiatorial
combat», l'«Avatar of Tiamat») non sono nell'elenco, e la prova
`test_parole_comuni_non_scattano` lo tiene vero.

Il secondo gruppo di prove tiene in piedi ciò che cita la cartella: l'indice
elenca i file che esistono, e la copertina di `hype_homebrew.py` rimanda alla
cartella giusta.
"""
import importlib.util
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CARTELLA = REPO / "campaign" / "ai-media-prompts"
INDICE = CARTELLA / "00_INDICE-PROMPT-MEDIA-CAMPAGNA.md"
TOOL = REPO / "scripts" / "hype_homebrew.py"

# Sensibile alle maiuscole: i titoli si scrivono con l'iniziale grande, le
# parole comuni no («gladiator» nome comune resta ammesso, «Gladiator» no).
OPERE_PROTETTE = re.compile(
    r"Doctor Strange|Endgame|Avengers|Marvel|\bMCU\b|Ragnarok"
    r"|Lord of the Rings|\bLOTR\b|Signore degli Anelli|Tolkien|Peter Jackson"
    r"|Helm's Deep|\bMoria\b|Rivendell|Boromir|Pelennor|Due Torri|Two Towers"
    r"|Ritorno del Re|Return of the King|Hobbit|Cinque Eserciti|Dead Marshes"
    r"|Fellowship|Uruk-hai"
    r"|Ridley Scott|\bGladiator(e)?\b|\"Aliens?\"|Alien \(|Alien,|Cronenberg"
    r"|del Toro|Pan's Labyrinth|James Cameron|Avatar \(|Avatar-inspired"
    r"|Annihilation|Interstellar|Jurassic Park|Indiana Jones|Harry Potter"
    r"|Game of Thrones|House of the Dragon|Witcher|\bAndor\b"
    r"|Warhammer Fantasy|Warhammer-style|Warcraft|Marcia Imperiale"
    r"|Howard Shore|\bShore\b|Zimmer|Horner|Goldsmith|Salisbury|Silvestri"
    r"|Navarrete|O Fortuna|Orff"
    r"|Giger|Frazetta|Alan Lee|John Howe|Salvatore|Escher|Weta"
    r"|Khazad-d\u00fbm|Misty Mountains|Carmina Burana|Lovecraft|Sistine"
    r"|Delacroix|Moriarty|Night Watch|Dante's Inferno|Bram Stoker|Stravinsk"
)


def righe_con_opere(testo: str) -> list[tuple[int, str]]:
    return [(n, riga) for n, riga in enumerate(testo.splitlines(), 1)
            if OPERE_PROTETTE.search(riga)]


class TestNessunaOperaProtetta(unittest.TestCase):
    def test_la_cartella_ha_i_suoi_dodici_file(self):
        self.assertEqual(len(sorted(CARTELLA.glob("*.md"))), 12)

    def test_nessun_prompt_cita_opere_protette(self):
        trovate = []
        for file in sorted(CARTELLA.glob("*.md")):
            for n, riga in righe_con_opere(file.read_text(encoding="utf-8")):
                trovate.append(f"{file.name}:{n}: {riga.strip()[:100]}")
        self.assertEqual(trovate, [], "riferimenti a opere protette:\n" + "\n".join(trovate))

    def test_l_elenco_scatta_sui_casi_veri(self):
        for caso in ("visual style of Doctor Strange (portal magic)",
                     "in the style of Alan Lee and John Howe",
                     "Lord of the Rings: The Two Towers",
                     "Riferimento: \"Alien\" (Jerry Goldsmith)",
                     "Gladiator arena atmosphere",
                     "R.A. Salvatore dark elf aesthetic"):
            self.assertTrue(righe_con_opere(caso), caso)

    def test_parole_comuni_non_scattano(self):
        for caso in ("violation of dwarven sacred spaces by alien biology",
                     "swinging a glowing magical warhammer",
                     "gladiatorial combat intensity",
                     "a half-orc gladiator",
                     "The horrifying Avatar of Tiamat",
                     "violet arcane energy",
                     "Byzantine icon painting"):
            self.assertFalse(righe_con_opere(caso), caso)


class TestChiCitaLaCartella(unittest.TestCase):
    def test_l_indice_elenca_file_che_esistono(self):
        citati = set(re.findall(r"`(\d\d_[^`]+\.md)`", INDICE.read_text(encoding="utf-8")))
        self.assertGreaterEqual(len(citati), 11)
        for nome in citati:
            self.assertTrue((CARTELLA / nome).is_file(), nome)

    def test_la_copertina_di_hype_rimanda_alla_cartella(self):
        spec = importlib.util.spec_from_file_location("hype_homebrew", TOOL)
        hh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hh)
        copertina = hh.build_cover("Titolo", "Sottotitolo", "meta")
        self.assertIn("campaign/ai-media-prompts/", copertina)
        self.assertTrue(CARTELLA.is_dir())


if __name__ == "__main__":
    unittest.main()
