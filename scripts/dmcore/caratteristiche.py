"""dmcore.caratteristiche — la scelta delle sei caratteristiche di una creatura.

ADR-0066, `PIANO-QUALITA-DEL-CODICE` §8 (lotto E).

Gli strati di ADR-0064, in ordine: la sestina che la scheda scrive, quella della
fonte citata, i vincoli ricavati da CA, pf, iniziativa e lotta, il tetto dei TS,
e per ultimo l'array del Manuale del DM per ruolo, con taglia e razza SRD e un
±1 a seme fisso. Qui stanno anche le tabelle della scelta: `PROFILI`,
`PER_TAGLIA`, `RAZZE`.

🔒 **Il verificatore non lo importa mai**, ne' direttamente ne' passando per un
altro modulo: se una stessa funzione scegliesse e verificasse, un errore di
regola comparirebbe da tutte e due le parti e si confermerebbe da solo.
`test_grafo_import_creature.py` lo verifica. Lo importano i generatori:
`genera_attributi`, `derive_statblocks` e il ramo PNG di `genera_creatura`.

Solo stdlib.
"""
from __future__ import annotations

__all__: list[str] = []
