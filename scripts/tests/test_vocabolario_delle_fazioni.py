"""Una fazione dice DA CHE PARTE sta, non dove vive e non cosa vuole — lotto 4d-8.

Il DM il 2026-09-17: *«fai il vocabolario delle fazioni e cerchiamo di mergiare
o droppare questi doppioni»*. Misurando, i due problemi si sono rivelati **lo
stesso problema visto da due lati**: il campo `faction` conteneva cose che non
sono schieramenti, e lo stesso soggetto ne portava due valori diversi.

## 1 · Tre valori non erano fazioni

| Valore | Quante | Cos'era davvero |
|---|---:|---|
| `underdark` | 3 | un **ambiente**, e i tre file lo dichiaravano *anche* in `Environment` |
| `rhod-allies` | 1 | un contenitore da un membro |
| `rakshasa-hunter` | 1 | uno **scopo** («caccia il rakshasa»), che sta in `Role` |

🔴 **Perche' un ambiente come fazione fa danno.** L'asse delle alleanze
(`faction_alliances.yaml`) si costruisce **sulle** fazioni: `red-hand-drow-pact`
e' `red-hand` + `drow-sonjak`. Un valore che descrive il posto invece dello
schieramento non puo' entrare in nessuna alleanza, e `--faction underdark`
restituiva tre creature arbitrarie dove `--env underdark` ne restituisce tutte.

I tre file erano trascrizioni PCGen del modulo RHoD **mai collocate in un arco**:
l'alleanza non e' stabilita, e dichiararne una sarebbe inventarla. Adesso
dicono `unknown` e portano scritto il perche'.

## 2 · Tredici soggetti avevano DUE record, che si contraddicevano

Una scheda canonica (`Xal_thor/Xal_thor.md`) e un POINTER `-crN` accanto
(`xal-thor-illithid-commander-cr14.md`), nato quando lo scanner non raggiungeva
i file annidati. Adesso li raggiunge entrambi.

⚠️ **E non erano copie uguali**: in ogni coppia **uno dichiara le intestazioni e
l'altro le fa indovinare**, e in **sei** casi divergevano — Tyrgarun `dragon`
contro `red-hand`, l'Avatar di Tiamat `rethmar-defender` contro `red-hand`,
Therysol `rakshasa-hunter` contro `unknown`. Il **Conte Valerius** aveva due
**GS**: 14 e 6.

La scelta non e' «tengo il canonico»: e' **tengo quello che dichiara**
(ADR-0041). Sei contraddizioni risolte in favore del valore scritto a mano.

## 3 · E due fazioni d'epoca, perche' un incontro non puo' mescolare due ere

🔎 **Trovato dal censimento del vocabolario, ed era un errore mio.** Avevo messo
**Skullcrusher il Nero** e **Zog'tar Deatheye** in `red-hand` — ma il loro
assedio e' del **~372 DR**, mille anni prima della Mano Rossa, ed esisteva
**gia'** `orda-antica-372dr` per **Balvar Fuocospento**, il consigliere della
stessa orda. Senza la correzione, `suggest_encounter --faction red-hand` poteva
proporre un drago di mille anni fa accanto a un hobgoblin del 1372.

Simmetricamente nasce `hammerfist-372dr` per i difensori di quell'assedio (Re
Thorek I, Durin, Thorgrim), distinti da `hammerfist-hero` che sono gli eroi del
**1372**.
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

CATALOGO = yaml.safe_load(
    (ROOT / "scripts" / "monster_catalog.yaml").read_text(encoding="utf-8"))["monsters"]
FAZIONI = Counter(m["faction"] for m in CATALOGO)


def _bmc():
    spec = importlib.util.spec_from_file_location(
        "bmc", ROOT / "scripts" / "build_monster_catalog.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestUnaFazioneNonEUnAmbiente(unittest.TestCase):
    def test_nessuna_fazione_porta_il_nome_di_un_ambiente(self):
        """🔴 La regola, e la prova che morde su tutto il vocabolario.

        Gli ambienti sono le chiavi di `ENV_KEYWORDS`. Se un giorno un valore
        ne riusa il nome, non potra' entrare in nessuna alleanza e questo
        cancello diventa rosso prima che il DM se ne accorga al tavolo.
        """
        ambienti = set(_bmc().ENV_KEYWORDS) | {"any"}
        colpevoli = sorted(set(FAZIONI) & ambienti)
        self.assertEqual(colpevoli, [],
                         f"fazioni che sono in realta' ambienti: {colpevoli}")

    def test_i_tre_dell_underdark_dichiarano_di_non_sapere(self):
        """Non e' una perdita: `unknown` dice il vero, e il fatto vero (vivono
        nel Sottosuolo) resta in `Environment`, dove `--env underdark` lo trova."""
        indice = {m["source_file"]: m for m in CATALOGO}
        for rel in ("Bestiario/mostri/underdark-cleric-ainin-cr5.md",
                    "Bestiario/mostri/underdark-dovil-runecaster-cr7.md",
                    "Bestiario/png/bothor-malvur-cr6.md"):
            with self.subTest(voce=rel.rsplit("/", 1)[-1]):
                m = indice[rel]
                self.assertEqual(m["faction"], "unknown")
                self.assertEqual(m["environment"], "underdark")
                testo = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("ma e' un ambiente", testo,
                              "il perche' non e' scritto nel file: fra un mese "
                              "sembrera' una svista")

    def test_gli_alleati_senza_gruppo_hanno_una_fazione_sola(self):
        """Erano due contenitori da un membro, e uno diceva uno **scopo**."""
        self.assertNotIn("rhod-allies", FAZIONI)
        self.assertNotIn("rakshasa-hunter", FAZIONI)
        nomi = " · ".join(m["name"] for m in CATALOGO
                          if m["faction"] == "alleati-del-vale")
        for atteso in ("Jorr Natherson", "Therysol"):
            with self.subTest(alleato=atteso):
                self.assertIn(atteso, nomi)


class TestLeDueEreNonSiMescolano(unittest.TestCase):
    """🕰️ Un incontro che mette insieme il ~372 DR e il 1372 non puo' esistere."""

    #: ⚠️ **Durin ha cambiato cognome e Thorgrim e' uscito dal pool**, il
    #: 2026-09-18. Il master vivo `ARC07-DEF-4` §4-bis lo chiama **Durin
    #: Rocciadura** (Guerriero 6), l'archivio lo chiamava **Hammerfist**
    #: (Guerriero 8): vince il master, e il cognome e' la decisione D4 aperta
    #: al DM. Thorgrim e' `[NON-CREATURA]`: non ha statblocco da nessuna parte.
    ANTICHI = ("Skullcrusher il Nero", "Zog'tar Deatheye", "Balvar Fuocospento",
               "Re Thorek I", "Durin Rocciadura")

    def test_l_orda_antica_non_e_la_mano_rossa(self):
        indice = {m["name"]: m["faction"] for m in CATALOGO}
        for nome, attesa in (("Skullcrusher il Nero", "orda-antica-372dr"),
                             ("Zog'tar Deatheye", "orda-antica-372dr"),
                             ("Balvar Fuocospento", "orda-antica-372dr"),
                             ("Re Thorek I", "hammerfist-372dr"),
                             ("Durin Rocciadura", "hammerfist-372dr")):
            trovato = next((f for n, f in indice.items() if n.startswith(nome)), None)
            with self.subTest(soggetto=nome):
                self.assertEqual(trovato, attesa)

    def test_nessun_antico_e_rimasto_fra_i_contemporanei(self):
        """La prova all'indietro del caso concreto: `--faction red-hand` non
        deve poter pescare un drago di mille anni fa."""
        moderne = {"red-hand", "dauth-defender", "hammerfist-hero", "rethmar-defender"}
        intrusi = [m["name"] for m in CATALOGO
                   if m["faction"] in moderne
                   and any(m["name"].startswith(a) for a in self.ANTICHI)]
        self.assertEqual(intrusi, [], f"soggetti del ~372 DR in una fazione del 1372: {intrusi}")

    def test_re_thorek_i_non_e_re_thorek_hammerfist(self):
        """Stesso nome, mille anni di distanza — la forma d'errore che il repo
        presidia da 4d-5 (Grom contro l'Ogre Skullcrusher)."""
        uno = next(m for m in CATALOGO if m["name"].startswith("Re Thorek I"))
        mille = next(m for m in CATALOGO if m["name"].startswith("Re Thorek Hammerfist"))
        self.assertNotEqual(uno["faction"], mille["faction"])


class TestUnSoggettoUnRecord(unittest.TestCase):
    """🔴 Tredici coppie POINTER↔scheda, e in sei casi si contraddicevano."""

    def test_nessuna_scheda_del_bestiario_e_indicizzata_due_volte(self):
        cop = _bmc()._superate_dal_gemello(ROOT)
        indicizzati = {m["source_file"] for m in CATALOGO}
        self.assertGreaterEqual(len(cop), 13,
                                "la deduplica non trova piu' le coppie: se il "
                                "riconoscimento si rompe, tornano 13 doppioni")
        intrusi = sorted(cop & indicizzati)
        self.assertEqual(intrusi, [], f"file superati ma ancora nel catalogo: {intrusi}")

    def test_vince_chi_dichiara_non_chi_e_canonico(self):
        """ADR-0041 applicato a una coppia, sui sei casi che divergevano."""
        indice = {}
        for m in CATALOGO:
            indice.setdefault(m["name"].split("—")[0].split("(")[0].strip(), m)
        for nome, fazione, cr in (("Tyrgarun", "red-hand", 18.0),
                                  ("Khorn", "dauth-defender", 8.0),
                                  ("Mira Serani", "red-hand", 8.0)):
            with self.subTest(soggetto=nome):
                m = next(v for k, v in indice.items() if k.startswith(nome))
                self.assertEqual(m["faction"], fazione)
                self.assertEqual(m["cr"], cr)

    def test_il_conte_valerius_vale_quattordici_non_sei(self):
        """🐛 Aveva **due GS** nei due file: 14 dichiarato, 6 indovinato."""
        v = [m for m in CATALOGO if "Valerius" in m["name"]]
        self.assertEqual(len(v), 1, f"{[(x['name'], x['cr']) for x in v]}")
        self.assertEqual(v[0]["cr"], 14.0)

    def test_un_pointer_verso_un_ARCO_resta_indicizzato(self):
        """🔵 Il limite della regola, e non e' negoziabile.

        Vale **solo** fra due file del `Bestiario/`. Un POINTER che rimanda a un
        file d'arco e' l'unica cosa che tiene quella creatura nel pool: era
        tutto il senso del lotto 4d-5, e toglierlo disferebbe 47 voci.
        """
        fonti = {m["source_file"] for m in CATALOGO}
        for rel in ("Bestiario/villain/terros-l-antico-cr15.md",
                    "Bestiario/png/madre-ilaria-sonda-cr7.md",
                    "Bestiario/mostri/guardiano-di-luce-cr10.md"):
            with self.subTest(voce=rel.rsplit("/", 1)[-1]):
                self.assertIn(rel, fonti)


class TestIlVocabolarioResaChiuso(unittest.TestCase):
    def test_ogni_fazione_ha_almeno_due_membri_o_una_ragione(self):
        """Un valore da un membro solo e' quasi sempre un ruolo travestito.

        ⚠️ Non e' una legge: una fazione nuova nasce legittimamente a uno. Ma
        deve stare in questo elenco, scritto a mano — cosi' aggiungerne una
        resta **una riga qui e una scelta**, come per le non-creature.
        """
        # nessuna, oggi: il lotto 4d-8 ha consolidato le due che c'erano
        AMMESSE: "set[str]" = set()
        soli = {f for f, n in FAZIONI.items() if n == 1} - AMMESSE
        self.assertEqual(soli, set(),
                         f"fazioni da un membro solo, non dichiarate: {sorted(soli)}")

    def test_il_vocabolario_non_si_gonfia_in_silenzio(self):
        """26 valori (erano 27 prima del consolidamento, con tre sbagliati)."""
        self.assertLessEqual(len(FAZIONI), 27,
                             "il vocabolario sta crescendo: ogni valore nuovo "
                             "dev'essere una fazione vera, non un ambiente ne' "
                             "un ruolo\n  " + "\n  ".join(sorted(FAZIONI)))


if __name__ == "__main__":
    unittest.main()
