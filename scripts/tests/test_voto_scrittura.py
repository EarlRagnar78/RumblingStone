"""Test di voto_scrittura.py (L11 di PIANO-AGENT-SKILLS-ESTERNE)."""
from __future__ import annotations

import json
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import voto_scrittura as vs  # noqa: E402

BOX_BUONO = (
    "> **Read-aloud (Salvatore lead).** *C'è odore di ferro bagnato. La pietra\n"
    "> trasuda, e una goccia batte su un elmo rovesciato a terra.*\n"
    ">\n"
    "> *Skullcrusher alza l'ascia. **Che fate?***\n"
)


def _controlli(testo, genere="apertura"):
    return {k: ok for k, (ok, _) in vs.controlli(testo, genere).items()}


class TestIControlliDeiBox(unittest.TestCase):
    def test_un_box_a_norma_passa(self):
        c = _controlli(BOX_BUONO)
        for k in ("box_presente", "box_tetto_righe", "box_senza_parentesi", "box_p1",
                  "box_senza_metrature", "box_etichettato", "chiude_che_fate"):
            assert c[k], k

    def test_oltre_dodici_righe(self):
        lungo = "> *Riga di pietra.*\n" + "".join("> e ancora pietra.\n" for _ in range(12))
        assert not _controlli(lungo)["box_tetto_righe"]

    def test_p1_il_box_che_decide_per_il_giocatore(self):
        assert not _controlli("> *Entrate nella sala e vedete un altare.*\n")["box_p1"]

    def test_la_metratura_resta_al_dm(self):
        assert not _controlli("> *Una sala larga 18 metri, con un altare.*\n")["box_senza_metrature"]

    def test_parentesi(self):
        assert not _controlli("> *Un altare (di basalto) al centro.*\n")["box_senza_parentesi"]

    def test_il_box_nudo_non_e_etichettato(self):
        assert not _controlli("> *Un altare al centro.*\n")["box_etichettato"]

    def test_etichetta_sulla_riga_sopra(self):
        dentro = "> **Read-aloud (LotR lead).**\n> *Un altare al centro.*\n"
        fuori = "**Read-aloud (LotR lead).**\n\n> *Un altare al centro.*\n"
        assert _controlli(dentro)["box_etichettato"]
        assert _controlli(fuori)["box_etichettato"]

    def test_etichetta_che_va_a_capo(self):
        testo = ("**Read-aloud (BG3 lead).** *Da leggere solo se il gruppo\n"
                 "ha scelto la porta.*\n\n> *Un altare al centro.*\n")
        assert _controlli(testo)["box_etichettato"]

    def test_etichetta_lontana_non_vale(self):
        testo = "**Read-aloud (LotR lead).**\n\nPer il DM.\n\n> *Un altare.*\n"
        assert not _controlli(testo)["box_etichettato"]

    def test_senza_box_nessuna_etichetta_vale(self):
        assert not _controlli("Solo prosa per il DM.\n")["box_etichettato"]

    def test_senza_box_nessun_controllo_di_box_passa(self):
        # Prima un testo senza box passava i sei controlli sui box: la
        # spazzatura prendeva 78% in verifica (I1, 2026-10-10).
        c = _controlli("La caverna sembra enorme (circa 30 metri). Fine.\n")
        for k in ("box_tetto_righe", "box_un_nome", "box_senza_parentesi",
                  "box_senza_sembra", "box_p1", "box_senza_metrature"):
            assert not c[k], k


class TestIControlliDeiDocumenti(unittest.TestCase):
    def test_tre_antitesi_sono_troppe(self):
        doc = ("Non è un gate: è una misura. Non è una regola: è un dato. "
               "Non è un voto: è un conto.\n")
        assert not _controlli(doc, "documento")["doc_antitesi"]

    def test_un_trattino_passa_sempre(self):
        assert _controlli("Il voto conta — per ora.\n", "documento")["doc_trattini"]
        assert not _controlli("Il voto — per ora — conta.\n", "documento")["doc_trattini"]

    def test_un_documento_non_ha_box(self):
        assert not _controlli(BOX_BUONO, "documento")["doc_senza_box"]


class TestIlVoto(unittest.TestCase):
    def test_un_testo_che_manca_fallisce_tutto(self):
        caso = {"id": "X", "genere": "apertura", "controlli": ["box_presente", "calchi"]}
        assert vs.vota(None, caso) == {"box_presente": False, "calchi": False}

    def test_un_insieme_non_chiesto_non_vale_zero(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            corsa = Path(d) / "C-con-1"
            corsa.mkdir()
            (corsa / "S06.md").write_text("> *x*\n", encoding="utf-8")
            casi = [{"id": "S01", "insieme": "taratura", "genere": "apertura", "controlli": ["box_presente"]},
                    {"id": "S06", "insieme": "verifica", "genere": "apertura", "controlli": ["box_presente"]}]
            voti = vs.voti_delle_corse(Path(d), casi)
            assert set(voti["C-con-1"]) == {"S06"}

    def test_le_ripetizioni_si_sommano(self):
        assert vs.condizione("A-con-2") == "A-con"
        assert vs.condizione("B-con-10") == "B-con"

    def test_sembra_nel_box_fallisce(self):
        # D13: da indizio a controllo.
        assert not _controlli("> **Read-aloud (LotR lead).** *La sala sembra vuota.*\n")["box_senza_sembra"]

    def test_come_se_non_e_sembra(self):
        assert _controlli("> *Batte come se fosse vivo.*\n")["box_senza_sembra"]

    def test_sembra_smentito_col_trattino_resta(self):
        # D17: «sembra» seguito dalla smentita prepara il colpo, non esita
        assert _controlli("> *Quella che sembrava una parete — è una palpebra.*\n")["box_senza_sembra"]

    def test_sembra_smentito_nella_frase_dopo_resta(self):
        assert _controlli("> *Sembra un luogo sicuro. E non lo è.*\n")["box_senza_sembra"]
        assert _controlli("> *Sembrava una macchia scura, e si rivela un'ala.*\n")["box_senza_sembra"]

    def test_smentita_troppo_lontana_non_salva(self):
        # oltre la frase dopo la smentita non vale: il narratore ha già esitato
        testo = "> *La sala sembra vuota. Il vento soffia. Il fuoco arde. Invece c'è qualcuno.*\n"
        assert not _controlli(testo)["box_senza_sembra"]

    def test_un_e_da_solo_non_smentisce(self):
        assert not _controlli("> *La sala sembra vuota. È fredda.*\n")["box_senza_sembra"]

    def test_sembra_fuori_dal_box_non_conta(self):
        assert _controlli("Al DM sembra lungo.\n> *Una sala vuota.*\n")["box_senza_sembra"]


class TestICasi(unittest.TestCase):
    def setUp(self):
        self.casi = vs.leggi_casi()

    def test_ogni_controllo_esiste(self):
        noti = set(vs.controlli("x", "apertura"))
        for c in self.casi:
            assert set(c["controlli"]) <= noti, c["id"]

    def test_meta_stratificate_per_genere(self):
        per_genere = Counter((c["genere"], c["insieme"]) for c in self.casi)
        generi = {c["genere"] for c in self.casi}
        for g in generi:
            assert per_genere[(g, "taratura")] == per_genere[(g, "verifica")], g

    def test_i_prompt_non_insegnano_la_norma(self):
        # Se il prompt nomina la norma, la corsa senza skill la impara dal prompt.
        spie = ("read-aloud", "che fate", "etichett", "p1", "parentesi", "hdywtdt",
                "trattino", "antitesi", "righe")
        for c in self.casi:
            p = c["prompt"].lower()
            assert not [s for s in spie if s in p], c["id"]

    def test_id_unici(self):
        ids = [c["id"] for c in self.casi]
        assert len(ids) == len(set(ids))


class TestIlRepo(unittest.TestCase):
    def test_voti_allineati_alle_corse(self):
        """voti.json e' l'uscita di --emit sulle corse: i numeri di
        RISULTATI.md non possono andare per conto loro."""
        if not vs.VOTI.is_file():
            self.skipTest("voti.json non ancora emesso")
        self.assertEqual(json.loads(vs.VOTI.read_text(encoding="utf-8")),
                         vs.voti_delle_corse())
