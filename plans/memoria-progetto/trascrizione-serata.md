---
name: trascrizione-serata
description: Prova della trascrizione locale della serata con whisper.cpp (ADR-0135, PR #424 in bozza, 14/11): stato, misure del banco, cosa aspetta Jfs
metadata:
  type: project
  modified: 2026-11-14T00:29:04.625Z
---

PR #424 in bozza (ramo claude/project-thread-kcq3f8, 14/11/2026): `scripts/transcribe_session.py`, guida `docs/how-to/GUIDA-TRASCRIZIONE-SERATA.md`, ADR-0135, voce MS-0115 (fuori sequenza finché 0108-0114 non sono su main: test_memoria_storica rosso atteso, si rinumera al riallineo).

Banco non personale nel container (CPU, large-v3-turbo-q5_0): FLEURS italiano 16,6% di parole sbagliate col contesto di whisper, 5,8% con `-mc 0` (ora di serie); copione finto con voce Piper CC0: 6 nomi della campagna giusti su 20, numeri tutti giusti. Il prompt coi nomi con `-mc 0` non fa nulla; col contesto acceso inventa nomi (Tordek → Thorik).

**Why:** Jfs ha scelto «Prova su una serata» (card del 13/11): prova misurata, non adozione.
**How to apply:** la PR resta in bozza finché Jfs non registra una serata e manda M1 (parole/nomi buoni su 3 spezzoni da 5 min), M2 (quota momenti spuntati), M3 (minuti per il log con e senza). Soglia proposta: un terzo di tempo in meno e M2 ≥ 0,5. Audio, trascrizioni e nomi dei giocatori mai nel repo. GPU (Vulkan in distrobox --nvidia) non verificata. whisper.cpp scaricabile da github e modelli da HF nel container. Vedi [[hugging-face-rete]].
