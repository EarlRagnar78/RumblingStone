"""Dove vive ogni fatto di campagna: i tre master, e il trigger che li tocca.

🔴 **Questo modulo esiste per una trappola aperta dal lotto 4d-1.** Da quando le
otto tabelle di `campaign/state.md` sono **generate** da `campaign/state.yaml`
(ADR-0050), scriverle a mano in `state.md` non e' «una modifica che poi si
rigenera»: e' una modifica che **sparisce** alla prossima esecuzione di
`render_state.py`, senza un errore e senza un avviso. Il DM la fa, la vede nel
file, la committa, e la ritrova cancellata due giorni dopo.

Fino al 2026-09-16 `state_apply` chiudeva ogni sessione stampando
«proposte NON meccaniche — **applicale a mano in state.md**», che per meta'
delle proposte era l'istruzione per perderle.

I tre master:

    campaign/state.yaml           i FATTI tabellari (§0, §1, §2.4, §3, §4, §6, §7.E)
    campaign/state.md             la PROSA (§2 waypoint e orda, §5, §7, i banner)
    campaign/state-changelog.md   la STORIA, append-only

`state.md` e' insieme master (per la prosa) e vista (per le tabelle): la
distinzione la fanno i marcatori `<!-- gen:state:NOME -->`. Dentro quelli non si
scrive a mano; fuori, si scrive solo a mano.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Master:
    """Un file che e' fonte di verita' per una classe di fatti."""

    file: str
    #: come ci si scrive: `dato` (YAML), `prosa` (markdown a mano), `storia`
    modo: str
    #: perche' e' li', in una riga che il DM legge a fine sessione
    nota: str

    def __str__(self) -> str:  # pragma: no cover - solo presentazione
        return self.file


DATI = Master(
    "campaign/state.yaml", "dato",
    "la tabella corrispondente in state.md e' GENERATA: modificarla li' la "
    "cancella al prossimo `render_state.py`. Dopo la modifica: "
    "`python3 scripts/render_state.py`")

PROSA = Master(
    "campaign/state.md", "prosa",
    "sezione scritta a mano, fuori dai marcatori `gen:state:` — si modifica qui")

STORIA = Master(
    "campaign/state-changelog.md", "storia",
    "storico append-only: si appende in coda, non si riscrive")


#: A quale master appartiene ciascun trigger di `state_sync.TRIGGERS`.
#:
#: ⚠️ La copertura e' un cancello (`test_state_masters`): un trigger nuovo senza
#: la sua riga qui fa rossa la CI, perche' senza destinazione la proposta
#: tornerebbe al messaggio generico che il lotto 4d-2 ha tolto.
DESTINAZIONE: "dict[str, Master]" = {
    # 🔵 Era PROSA fino al 2026-09-16, e la decisione **D14** l'ha spostato.
    # Il banner di §2.1 e la spiegazione del DM erano lo STESSO paragrafo, e per
    # questo la regione non si poteva marcare. Separati, il numero e' un campo
    # (`march_clock.giorno_corrente`) e la nota resta prosa accanto: la macchina
    # riscrive la sua riga senza mai toccare quella del DM.
    "march_clock": DATI,
    # §3 e' la tabella `villain`, generata: il clock e' un campo del record.
    "ritual_clock": DATI,
    "villain_clock": DATI,
    "npc_killed": DATI,
    "npc_escaped": DATI,
    # §2 armate e alleanze: waypoint ledger e condizioni dell'orda sono prosa,
    # e restano tali — modellarle e' un lotto suo, non una riga di questa tabella.
    "alliance": PROSA,
}


def destinazione(trigger: str) -> "Master | None":
    """Il master di un trigger, o None se il trigger non e' dichiarato."""
    return DESTINAZIONE.get(trigger)


def per_master(triggers) -> "dict[Master, list]":
    """Raggruppa `(trigger, testo)` per master, nell'ordine DATI → PROSA → STORIA.

    Le proposte senza destinazione finiscono sotto `None`: si stampano lo
    stesso, con l'avvertenza che nessuno sa dove vadano. Perderle in silenzio
    sarebbe peggio che ammettere il buco.
    """
    gruppi: "dict[Master | None, list]" = {}
    for trigger, testo in triggers:
        gruppi.setdefault(destinazione(trigger), []).append(testo)
    ordine = [DATI, PROSA, STORIA, None]
    return {m: gruppi[m] for m in ordine if m in gruppi}
