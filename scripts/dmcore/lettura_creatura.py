"""dmcore.lettura_creatura — che cosa dice una scheda del Bestiario, letto una volta sola.

ADR-0066, `PIANO-QUALITA-DEL-CODICE` §8 (lotto E).

Il lettore degli statblocchi e della loro prosa: le espressioni regolari del
blocco, i dadi vita e il sospetto su `pf-dado`, le sestine delle caratteristiche
scritte nella scheda o nella fonte citata, i numeri della fonte, la composizione
dei DV, i talenti, la provenienza delle caratteristiche, e i **tetti** che un TS
scritto mette ai modificatori.

🔴 **Lo usa anche il verificatore** (D1, deciso dal DM il 2026-09-23): una
scheda si legge con lo stesso codice da chi genera e da chi verifica. Per questo
questo modulo non importa mai `dmcore.caratteristiche`, e
`test_grafo_import_creature.py` lo verifica. Quello che qui si ricava da un
numero scritto e' un limite, non una scelta: chi usa il limite per scegliere e'
`dmcore.caratteristiche`.

Solo stdlib.
"""
from __future__ import annotations

__all__: list[str] = []
