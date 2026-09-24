"""Cosa e' PARTITA e si azzera per un gruppo nuovo: l'elenco, come dato.

ADR-0050 §7 fissa la regola: il **prodotto** (archi, Bestiario, mappe, skill,
premessa, house rules) resta; la **partita** (stato, storico, cronaca, sessioni,
recap) si azzera da template. Fino al lotto 4f la regola stava nell'ADR e il
reset in `new-campaign-group.sh`, che azzerava due file su sette: un gruppo
nuovo ereditava 750 righe di `state.yaml` e 1.195 di storico, e la sua CI era
rossa al primo push perche' il template di `state.md` non aveva i marcatori.

Da qui l'elenco sta in un posto solo. Lo legge `azzera_partita.py`, che lo
esegue, e lo legge `test_new_group.py`, che verifica che copra ogni file che
gli script scrivono sotto `campaign/`: uno script nuovo che scrive un file di
partita senza dichiararlo qui fa rossa la CI.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Voce:
    """Un file (o un insieme di file) di partita, e cosa gli succede al reset."""
    percorso: str
    #: `stato` (state.yaml: template + anagrafica PNG del gruppo di prima),
    #: `template` (copia di `sorgente`), `svuota` (cancella i file del modello
    #: `percorso`, la cartella resta), `rimuovi` (un file generato: lo rifa' il
    #: suo comando quando serve)
    azione: str
    sorgente: "str | None" = None
    nota: str = ""


PARTITA: "tuple[Voce, ...]" = (
    Voce("campaign/state.yaml", "stato", "campaign/templates/state-blank.yaml",
         "scheletro + `png`, che e' prodotto (decisione D19 per il template derivato)"),
    Voce("campaign/state.md", "template", "campaign/templates/state-blank.md",
         "poi le regioni `gen:state:` si rigenerano dal nuovo state.yaml"),
    Voce("campaign/state-changelog.md", "template",
         "campaign/templates/state-changelog-blank.md", "storico append-only"),
    Voce("campaign/lore/campaign-chronicle.md", "template",
         "campaign/templates/chronicle-blank.md",
         "la cronaca del tavolo; la premessa (`campaign-premise.md`) e' prodotto e resta"),
    Voce("campaign/sessions/*.md", "svuota", nota="i log del gruppo di prima"),
    Voce("campaign/recaps/*.md", "svuota", nota="recap di gruppo e per PG"),
    Voce("campaign/recaps/pg/*.md", "svuota"),
    Voce("campaign/recaps/homebrew/*.hb.md", "svuota"),
    Voce("campaign/next/*.md", "svuota", nota="brief e teaser"),
    Voce("campaign/pg/xp-ledger.md", "rimuovi", nota="`dm.py post` lo rifa'"),
    Voce("campaign/DM-DOSSIER.hb.md", "rimuovi", nota="`dm.py dossier` lo rifa'"),
    Voce("campaign/group.yaml", "rimuovi",
         nota="porta il nome del gruppo di prima: `dm.py session branch --group` lo rifa'"),
)

#: Partita dichiarata che il reset NON tocca ancora, col lotto che la chiude.
#: Il reset la stampa a ogni esecuzione: una falla nota resta in vista.
#: Vuoto dal lotto 4f-2 (2026-09-24), che ha diviso `campaign-history.md` in
#: premessa e cronaca: era l'unica voce.
PENDENTI: "dict[str, str]" = {}
