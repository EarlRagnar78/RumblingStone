---
name: scelte-inferred-versione-piu-forte
description: Regola di Jfs per statblocchi e INFERRED: sempre la versione più forte, ma calcolata e legale (3.5 → PF1e → SRD), mai inventata; il non SRD segnato
metadata:
  type: feedback
  modified: 2026-10-18T09:06:30.500Z
---

Quando un INFERRED, uno statblocco o una scheda ammette più versioni, la proposta ★ è sempre quella **più potente e terrificante**. Le fonti si guardano in quest'ordine: D&D 3.5 completo (anche i manuali non SRD, marcati `[Private source — …]`), poi Pathfinder 1e, poi l'SRD. Tutto quello che esce dall'SRD si segna nel file (`⚠ **Non SRD**`, «oltre la ricchezza SRD», «non verificato»), insieme alla riga «PF1e:» quando PF1e lo legalizza o lo cambia. È un'estensione di ADR-0091 §4-bis.

**Why:** il 2026-10-18 Jfs ha fatto rifare i lotti 3 e 4 (commit 99776b1c, PR #241), perché alcune ★ avevano scelto la versione SRD più debole: Tiro in Corsa tolto ai ranger, RI di Maewen tolta, scurovisione del fungo tolta, 12 usi di Tempestas invece di 14, Fauci che si ritirava prima. Vuole la versione forte, e vuole che resti traccia di dove esce dalle regole.

**How to apply:** non proporre mai come ★ un'opzione che abbassa un numero solo per rientrare nell'SRD. Se la versione forte rompe un prerequisito, aggiungi il prerequisito invece di togliere il talento, e segnalo. Vale per tutti i lotti successivi di [[ramo-di-gruppo-campagna]] e ADR-0091.

2026-11-09 Jfs (thread «Scelte dell'8/11»): «valori sempre i più forti ma calcolati e non inventati; se PF1e è più forte usa PF1e, ma deve essere compliant con le regole, altrimenti a cosa servono?». Un numero più alto preso da una fonte (es. chat Gemini) entra solo se si ricostruisce da una scheda legale 3.5/PF1e; altrimenti si scarta col conto scritto (Fanteria Hobgoblin AU +10 della chat → resta +8).
