---
name: feedback-numeri-piu-forti-calcolati
description: Jfs 2026-11-09: ogni numero di scheda è la versione più forte solo se ricostruibile da una scheda legale 3.5 o PF1e; mai inventato
metadata:
  type: feedback
---
Jfs, 2026-11-09 (thread «Scelte dell'8/11»): «i valori sempre i più forti ma calcolati e non inventati; se la versione PF1e è più forte usa PF1e, ma deve essere compliant con le regole». Criterio per ogni numero: la versione più forte, ma solo se si ricostruisce da una scheda legale 3.5 o PF1e. Un numero da una fonte esterna (es. chat Gemini) che non si calcola non entra. Primo caso: Fanteria Hobgoblin AU +10 → +8 (PR #360, 55dcd60).
Jfs vuole che valga per tutti i thread: proposta un ADR breve + cancello CI che rifà il conto di attacchi e AU degli statblock (card nel thread blocco 1).

**Why:** le regole servono solo se i numeri le rispettano; «più forte» non autorizza a inventare.
**How to apply:** prima di accettare un numero più alto, rifai il conto dalla build legale; se non torna, vale quello calcolato. Raffina [[feedback-standard-di-fatto]] e la preferenza «più potente e terrificante» (3.5 → PF1e → SRD).

2026-11-10: PR #364 unita su main (421dbd0), ADR-0118: cancello dei numeri a 0 scarti. Dentro: baliste AU +10 col mastro artigliere Guerriero 8 (scheda nel Bestiario), Doom Hand Chierico 8 GS 8, carta dei giganti = due macigni per settore a d20+9; ARC08-18/19 e DEF-2 toccati, simulazione tre_giorni invariata (nessuna breccia 50→54%).
