"""dmcore.progressione — le regole di classe e di tipo delle creature, senza caratteristiche.

ADR-0066, `PIANO-QUALITA-DEL-CODICE` §8 (lotto E).

Qui stanno le cose che chi genera e chi verifica devono vedere **uguali**,
perche' sono regole del SRD 3.5 e non scelte: i gruppi di dadi vita (una classe,
o i DV razziali del tipo), i nomi con cui le schede scrivono le classi, le due
classi di prestigio SRD che compaiono nel Bestiario, la base dei tiri salvezza
(buono 2 + L/2, cattivo L/3) e il BAB atteso.

Lo importano tutti: `genera_attributi`, `conformita_statblocchi`,
`derive_statblocks`, `genera_creatura` e gli altri due moduli del lotto. Non
importa niente che scelga.

Solo stdlib.
"""
from __future__ import annotations

__all__: list[str] = []
