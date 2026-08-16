"""Il lettore delle schede pregenerate (`dmcore.schede`) e la loro impaginazione.

Due livelli, perché i difetti stanno a due livelli diversi:

  * **sintetici** — le regole di taglio dei blocchi. Sono le uniche righe di
    questo modulo dove un errore non si vede: una voce fantasma in mezzo a una
    scheda sembra un dato del personaggio, non un bug del parser.
  * **sul modulo vero** — `Il Drappo di Tarsilia`. Se un master cambia forma e
    il lettore smette di trovare la CA, si scopre qui e non in stampa.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore.schede import SchedaError, leggi_schede  # noqa: E402
from export_booklet_typst import inline  # noqa: E402

DRAPPO = REPO / "STANDALONE-Il-Drappo-di-Tarsilia"
PREGEN = DRAPPO / "PREGEN-SEI-SCHEDE-PF1E.md"
FASCICOLO = DRAPPO / "FASCICOLO-SCHEDE-GIOCATORE.md"


# ── regole di taglio, su master sintetici ────────────────────────────────────

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


@pytest.fixture(scope="module")
def minima(tmp_path_factory):
    p = tmp_path_factory.mktemp("schede") / "PREGEN-PROVA.md"
    p.write_text(MINIMA, encoding="utf-8")
    return leggi_schede(p)[0]


def test_intestazione(minima):
    assert (minima.numero, minima.nome, minima.ruolo) == ("1", "TIZIA CAIA", "il Capitano")
    assert minima.classe == "Umana guerriera 3 · N · femmina, 38 anni · GS 2"
    assert minima.occhiello.endswith("nei master veri.")
    assert minima.rapide == [("Iniziativa", "+5"), ("Percezione", "+3"), ("Velocità", "6 m")]


def test_difesa(minima):
    assert (minima.ca, minima.pf, minima.pf_dado) == ("18", "27", "3d10+6")
    assert minima.ca_dettaglio.startswith("contatto 11")
    assert minima.ts == [("Tempra", "+6"), ("Riflessi", "+3"), ("Volontà", "+5")]
    # la nota fra parentesi va a capo nel master: deve arrivare intera
    assert minima.ts_nota == "mantello +1 incluso"


def test_attributi_e_manovre(minima):
    assert minima.attributi[0] == ("For", "17", "+3")
    assert len(minima.attributi) == 6
    assert minima.manovre == [("BAB", "+3"), ("CMB", "+6"), ("CMD", "17")]


def test_attacco_rientro_e_continuazione(minima):
    """Il rientro `&nbsp;` resta una riga a sé; la frase spezzata a metà no."""
    righe = minima.attacchi
    assert righe[0] == ("**Mischia** spada lunga **+8** (1d8+3/19–20)", False)
    assert righe[1] == ("con **Attacco Poderoso**: **+7** (1d8+5)", True)
    assert righe[2][1] is False
    assert "Canalizzazione Selettiva" in righe[2][0]        # ricucita, non spezzata
    assert len(righe) == 3


def test_voci_niente_fantasmi(minima):
    """Le tre voci vere, e nessuna delle tre trappole del markdown a capo."""
    assert [v.etichetta for v in minima.voci] == [
        "Incantesimi preparati", "Talenti", "Equipaggiamento",
    ]
    equip = minima.voce("equipaggiamento")
    assert "mantello della resistenza +1" in equip.corpo    # prezzo a capo: non è una voce
    assert "+ ~212 mo" in equip.corpo                       # né lo è il resto in tasca
    incantesimi = minima.voce("incantesimi")
    assert "**dominio**: *pietra magica*" in incantesimi.corpo  # né lo slot di dominio


def test_filetto_non_finisce_nel_testo(minima):
    """`---` fra una scheda e l'altra: Typst lo stamperebbe come lineetta lunga."""
    assert minima.minuto == "Decidi, e ad alta voce."
    assert not minima.problema.endswith("—")


def test_master_senza_schede(tmp_path):
    p = tmp_path / "PREGEN-VUOTO.md"
    p.write_text("# niente qui\n\ntesto\n", encoding="utf-8")
    with pytest.raises(SchedaError):
        leggi_schede(p)


# ── il modulo vero ───────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def drappo():
    return leggi_schede(PREGEN, FASCICOLO, [DRAPPO / "ALLEGATI" / "immagini" / "web"])


def test_sei_schede_complete(drappo):
    assert len(drappo) == 6
    for s in drappo:
        assert s.nome and s.ruolo and s.classe, s.nome
        assert s.ca and s.pf, s.nome
        assert len(s.attributi) == 6, s.nome
        assert len(s.ts) == 3, s.nome
        assert s.attacchi, s.nome
        assert s.minuto, s.nome                     # il piede della scheda
        assert s.voce("equipaggiamento"), s.nome
        assert s.voce("abilità"), s.nome
        assert s.voce("talenti"), s.nome


def test_ogni_scheda_ha_il_suo_ritratto(drappo):
    """`FRA' MELCHIO VANZI` → `ritratto-melchio.jpg`: la parola giusta, non la prima."""
    assert [s.ritratto.name for s in drappo] == [
        "ritratto-vanna.jpg", "ritratto-nocca.jpg", "ritratto-ombra.jpg",
        "ritratto-tesio.jpg", "ritratto-berenice.jpg", "ritratto-melchio.jpg",
    ]


def test_meta_sinistra_dal_fascicolo(drappo):
    for s in drappo:
        assert s.ad_alta_voce.startswith("«"), s.nome
        assert len(s.legami) == 5, s.nome           # gli altri cinque, mai sé stesso
        assert [v.etichetta for v in s.voci_retro][:2] == ["Come parli", "Tre cose che sai"]


def test_incantatori_hanno_gli_slot(drappo):
    per_nome = {s.nome.split()[0]: s for s in drappo}
    for chi in ("OMBRA", "TESIO", "BERENICE"):
        assert per_nome[chi].voce("incantesimi"), chi


# ── la traduzione a Typst ────────────────────────────────────────────────────

@pytest.mark.parametrize("md, atteso", [
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
])
def test_inline(md, atteso):
    assert inline(md) == atteso
