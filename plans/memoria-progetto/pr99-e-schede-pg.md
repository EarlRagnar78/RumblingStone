---
name: pr99-e-schede-pg
description: PR #99 chiusa il 2026-10-24 (scelta A di Jfs, ADR-0088 accettata); #278 (4g-1 schede PG) su main; PR #289 (ripresa di inventory_inferred, echi §1-bis, nota Golarion) unita il 2026-10-24; resta 4g-2
metadata:
  type: project
---

- PR #278 unita su main il 2026-10-23 (8c29508a): `PG/schede/<pg>.yaml` + vista `.md`, `validate_pg.py` e `render_pg.py --check` in CI, reset del gruppo nuovo rifà le schede (azione `schede` in dmcore/partita.py).
- Canone (Jfs 2026-10-23: «il canone è quello giocato nel gruppo» + artefatti rivisti): CAR di Thorik 8 → 12, un solo +4 (P1 lo dà alla Corona, DEF-1/D84 al rito). DES 10 → 6. 22 caselle su 24 ancora [INFERRED] → lotto 4g-2 (valori dalle schede del DM via modulo, D19).
- #99 chiusa dal thread padre il 2026-10-24 (Jfs 00:07: opzione A). PR #289 unita su main il 2026-10-24 (d8b2985c; ramo claude/recupero-pr99, thread «Piano per la PR 99 abbandonata») riprende da main: `inventory_inferred.py` canale testing (ratchet non bloccante, baseline 260 in docs/audit/inferred-baseline.json), consequence-echoes.md §1-bis, nota Golarion in P2D-PALIO §4. ADR-0088 accettata, piano §4.14. Il ramo pr/99 resta per 4g-2.
- 4g-2 prima parte: PR #291 unita su main il 2026-10-26 (ramo claude/4g-2-caratteristiche-pg): Tordek 6/6 da PCGen (`Tordek Durinheart 12 lvl modificato.pdf`, base 18/14/16/14/16/8, +2 guanti/stivali/fascia → attuale 20/16/16/14/18/8), Hella 6/6 da DEF-3 App. A.1 (SAG 16+4 Collana), Thorik FOR 20 da P1. Mancano COS/INT/SAG di Thorik e le 6 di Artemis (seconda PR da main quando Jfs risponde): modulo writing_draft a Jfs del 24/10, con conferme (oggetti nell'attuale = default; correggere FOR 14 di Tordek in P1/P2/DEF-1 lotta). Baseline ratchet 247.
- Il ratchet conta anche le citazioni del marcatore nella prosa: quando se ne parla scrivere «marcatori INFERRED» senza parentesi.

**Why:** evitare di rifare l'inventario e di ricontare il CAR a 16.
**How to apply:** 4g-2 parte da main; vedi [[thread-padre-pr]].
