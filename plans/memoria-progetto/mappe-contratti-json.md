---
name: mappe-contratti-json
description: Regola Jfs 2026-11-09: ogni mappa di campagna ha il suo contratto JSON identico alla griglia (ADR-0117, cancello in CI)
metadata:
  type: project
---

Jfs 2026-11-09: «per le mappe fai sempre il json». ADR-0117 (PR #362 unita il 2026-11-09, 04dbf0b): ogni griglia a emoji tracciata ha un contratto JSON che, ricompilato con compile_map_json.py, la ridà identica cella per cella. Cancello: scripts/tests/test_contratti_mappe.py, che lancia anche render_map_svg --strict --tutti-i-master.
Campo `simboli_locali` del contratto per simboli fuori dalla legenda universale. Per migrare una vecchia griglia: import_ultraclear.py FILE --map N -o CONTRATTO.json.
Fuori dal cancello: `_ARCHIVIO/`, scripts/tests/, plans/esperimenti/, docs/guides/. Archivio fuori per scelta del DM (card 2026-11-09).
**How to apply:** quando tocchi una griglia, tocca il JSON e rigenera; una mappa nuova nasce dal JSON. Vedi [[mappe-scala-reale]].
