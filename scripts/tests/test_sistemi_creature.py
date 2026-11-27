"""L5 (ADR-0111): le tabelle base delle creature 3.5 lette dal plugin dnd35.

Il difetto che questo test esiste per impedire: un numero che cambia
spostandolo da `dmcore/tabelle.py` a `sistemi/dnd35/dati/creature.toml`. Le
impronte sono quelle delle costanti scritte nel codice fino al 2026-11-07
(main b0a74ae), calcolate su `repr` delle voci ordinate: se un valore cambia
nei dati, l'impronta cambia e il test lo dice. Per cambiare una tabella di
proposito si aggiorna l'impronta qui, nello stesso diff, con il motivo.

Solo `unittest`.
"""
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import sistemi as S  # noqa: E402
from dmcore import caratteristiche as C  # noqa: E402
from dmcore import incantesimi as INC  # noqa: E402
from dmcore import progressione as P  # noqa: E402
from dmcore import tabelle as T  # noqa: E402

#: Cambiate di proposito il 2026-11-09 (audit dei plugin contro l'SRD in cache,
#: plans/esperimenti/plugin-regole-2026-11-09/): ARMATURE (+ pelle, bande,
#: strisce e i nomi italiani del lessico), SCUDI (scudo torre al posto di
#: «torre»), T.ADEPTO (4 righe come la Tabella dell'Adepto), T.INCANTATORI (la
#: griglia dell'adepto), P.PRESTIGIO e P.DADO_DI_CLASSE (le 14 classi di
#: prestigio SRD), LISTE (8 incantesimi al livello giusto della classe) e
#: NOMI_DI_CLASSE. Per la card del DM dello stesso giorno («Tabelle PF1e intere,
#: segnate») anche T.BARDO, T.BARDO_CONOSCIUTI, T.RANGER/T.PALADINO e
#: T.INCANTATORI: griglie del PRD PF1e, non SRD 3.5. Le altre impronte sono
#: quelle di prima. Il 2026-11-10 (regole complete, lotto 1) ARMATURE ancora:
#: «scaglie» diventa «corazza a scaglie», perché le scaglie di un drago non
#: sono un'armatura.
IMPRONTE_PRIMA = {
    "TIPI": "f314442313fc6eb1",
    "CLASSI": "ba993374d9283a09",
    "CLASSI_PNG": "b9acd679e2fa5931",
    "BAB_CLASSE": "e806f841362f1085",
    "TAGLIE": "e0f832356e31615e",
    "ARMATURE": "458da9837e40b7e0",
    "SCUDI": "bdd26a829de31a9a",
    "ELITE": "f3bbb911592fbc0a",
    "BASIC": "09397ca2fbf7a68e",
}

#: L5b (2026-11-07): impronte delle costanti di main c258a3e, prima dello
#: spostamento in `creature.toml`. `NOMI_DI_CLASSE` non c'è: è ordinato per
#: lunghezza partendo da un `set`, quindi a parità di lunghezza l'ordine cambia
#: con PYTHONHASHSEED già prima di L5b (la regex che lo usa non ne dipende).
IMPRONTE_L5B = {
    "T.MAGO": "52ca98ec50a5de88",
    "T.STREGONE": "d81f1e56ec2c06ed",
    "T.STREGONE_CONOSCIUTI": "288be00dadabf4f1",
    "T.CHIERICO": "b830bf626b47fd2e",
    "T.DRUIDO": "b830bf626b47fd2e",
    "T.ADEPTO": "d3240dcbd4580db9",
    "T.BARDO": "e8ac03012a9cddab",
    "T.BARDO_CONOSCIUTI": "2e4799f2efaa6cc6",
    "T.RANGER": "b53e50d7899bb2c0",
    "T.PALADINO": "b53e50d7899bb2c0",
    "T.LIVELLO_INCANTATORE_RIDOTTO": "6a9633f885386bc7",
    "T.INCANTATORI": "b315c798399e47cf",
    "T.INCANTATORI_SENZA_ANCORA": "cbad0fe52ade2682",
    "P.PRESTIGIO": "2cb916e16f7f2afa",
    "P.DADO_DI_CLASSE": "d682e8a39b2f25b8",
    "C.PROFILI": "2abef478722f8731",
    "C.PROFILO_DI_RIPIEGO": "6f6caace7ceb23dc",
    "C.PER_TAGLIA": "08bcc3ca27cf6cb0",
    "C.RAZZE": "7a128d76c0baa3ce",
}

#: L5c (2026-11-07): impronte delle liste di incantesimi di main prima dello
#: spostamento in `sistemi/{dnd35,pf1e}/dati/incantesimi.toml`.
IMPRONTE_L5C = {
    # LISTE riscritta di proposito il 2026-11-10 (lotto 2 delle regole complete): 108 nomi
    # portati al lessico ufficiale, scudo della legge al 8° del chierico, spaventare al 2° del bardo
    "LISTE": "1307c7c7b1998f0a",
    "CANONICA": "2074748d8ae338a2",
    "FUNZIONE_DI_RIPIEGO": "ce42176472ca1491",
    "SENZA_LISTA": "cbad0fe52ade2682",
    "PF1E_SOLO": "495b22c2645cf41b",
}


def impronta(x) -> str:
    if isinstance(x, dict):
        x = sorted(x.items())
    elif isinstance(x, frozenset):
        x = sorted(x)
    return hashlib.sha256(repr(x).encode()).hexdigest()[:16]


class TabelleDalPlugin(unittest.TestCase):
    def test_stessi_valori_di_prima(self):
        for nome, attesa in IMPRONTE_PRIMA.items():
            self.assertEqual(impronta(getattr(T, nome)), attesa, nome)

    def test_la_fonte_e_il_plugin(self):
        self.assertEqual(S.capacita("dnd35", "creature.costruzione").modo, "dati")
        dati = S.dati("dnd35", "creature.costruzione")
        self.assertEqual(set(dati["tipi"]), set(T.TIPI))
        self.assertEqual(T.TIPI["undead"], (12, 0.5, ("vol",)))

    def test_ogni_classe_ha_dado_ts_e_bab(self):
        self.assertEqual(set(T.BAB_CLASSE), set(T.CLASSI))
        self.assertTrue(T.CLASSI_PNG <= set(T.CLASSI))



class IncantatoriEProfiliDalPlugin(unittest.TestCase):
    """L5b: incantatori, prestigio, profili, taglie e razze dal plugin."""

    MODULI = {"T": T, "P": P, "C": C}

    def test_stessi_valori_di_prima(self):
        # Le classi dei manuali fuori SRD (classi_manuali.toml, ADR-0124 §8) si
        # aggiungono: la parte SRD deve restare quella di prima.
        for chiave, attesa in IMPRONTE_L5B.items():
            modulo, nome = chiave.split(".")
            valore = getattr(self.MODULI[modulo], nome)
            if chiave in ("P.PRESTIGIO", "P.DADO_DI_CLASSE"):
                valore = {k: v for k, v in valore.items() if k not in P.MANUALI}
            self.assertEqual(impronta(valore), attesa, chiave)

    def test_nomi_di_classe_stesso_insieme(self):
        self.assertEqual(impronta(frozenset(P.NOMI_DI_CLASSE) - P.MANUALI), "692243b47b976b91")
        self.assertGreater(len(P.MANUALI), 500)

    def test_alias_restano_la_stessa_griglia(self):
        self.assertIs(T.DRUIDO, T.CHIERICO)
        self.assertIs(T.PALADINO, T.RANGER)
        self.assertIs(T.INCANTATORI["paladino"][0], T.RANGER)

    def test_ogni_incantatore_ha_venti_livelli(self):
        for classe, (griglia, car, _) in T.INCANTATORI.items():
            self.assertEqual(sorted(griglia), list(range(1, 21)), classe)
            self.assertIn(car, {"int", "sag", "car"}, classe)

    def test_ordine_delle_razze_conta(self):
        nomi = [n for n, _ in C.RAZZE]
        self.assertLess(nomi.index("hobgoblin"), nomi.index("goblin"))
        self.assertLess(nomi.index("duergar"), nomi.index("nano"))



class ListeIncantesimiDalPlugin(unittest.TestCase):
    """L5c: liste 3.5 dal plugin dnd35, aggiunte APG dal plugin pf1e."""

    def test_stessi_valori_di_prima(self):
        for nome, attesa in IMPRONTE_L5C.items():
            self.assertEqual(impronta(getattr(INC, nome)), attesa, nome)

    def test_alias_arcano_e_un_oggetto_solo(self):
        self.assertIs(INC.LISTE["mago"], INC.LISTE["stregone"])
        self.assertIs(INC.PF1E_SOLO["mago"], INC.PF1E_SOLO["stregone"])

    def test_pf1e_eredita_le_liste_core_e_aggiunge_le_sue(self):
        self.assertEqual(S.capacita("pf1e", "creature.incantesimi").modo, "dati")
        pf = S.dati("pf1e", "creature.incantesimi")
        self.assertEqual(set(pf["liste"]), set(S.dati("dnd35", "creature.incantesimi")["liste"]))
        self.assertIn("solo", pf)



class RegoleDiTipoECampiDalPlugin(unittest.TestCase):
    """L5d: alias dei tipi (dnd35), non morto PF1e (pf1e), campi dello statblocco (d20)."""

    IMPRONTE = {
        "ALIAS_TIPO": "ee9d0a3a4dd5bd38",
        "OBBLIGATORI": "76269d2a7d4a1fc5",
        "AMMESSI": "4cc38d37ad840269",
        "LISTE": "95c5850902a37d41",
        "NON_MORTO_PF1E": "b1097a871dea2f15",
    }

    def test_stessi_valori_di_prima(self):
        from dmcore import lettura_creatura as LC
        from dmcore import statblock as SB
        dove = {"ALIAS_TIPO": T, "OBBLIGATORI": SB, "AMMESSI": SB, "LISTE": SB, "NON_MORTO_PF1E": LC}
        for nome, attesa in self.IMPRONTE.items():
            self.assertEqual(impronta(getattr(dove[nome], nome)), attesa, nome)

    def test_nessuna_capacita_l5_resta_nel_codice(self):
        for id_ in ("d20", "dnd35", "pf1e"):
            for nome in ("statblocco.campi", "creature.regole_di_tipo", "creature.incantesimi",
                         "creature.costruzione"):
                c = S.capacita(id_, nome)
                self.assertNotEqual(c.modo, "codice", f"{id_} {nome}")


if __name__ == "__main__":
    unittest.main()
