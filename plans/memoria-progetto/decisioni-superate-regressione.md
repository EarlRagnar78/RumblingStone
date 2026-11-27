---
name: decisioni-superate-regressione
description: Regola Jfs 2026-10-31: decisioni nuove che superano le vecchie, si abbandona quella che regredisce; i dubbi vanno a card con consigliata
metadata:
  type: feedback
---

Jfs, 2026-10-31 (thread «Audit settimanale PR e decisioni»): se una decisione nuova supera una presa prima, si abbandona quella che impone una regressione o un peggioramento misurabile. Quelle in dubbio si chiedono a Jfs, una card per ciascuna, con la soluzione consigliata.

**Why:** l'archivio delle decisioni è cresciuto e alcune si contraddicono. Jfs vuole che vinca la misura, non l'ordine in cui sono state prese.

**How to apply:** va scritta nel brief di ogni thread che lavora l'indice §0 di STATO-E-ORDINE. Sempre lo stesso giorno, Jfs ha dato il via libera a lavorare le voci ⬜ dell'indice (P16-P27, P30), un thread alla volta: il successivo parte solo quando la PR del precedente è unita. Primo thread: «Indice: voci piccole e allineamenti» (P17, P18, P26 e la correzione della P05). Vedi [[weekly-audit-routine-scope]] e [[thread-padre-pr]].

2026-10-31, primo thread: PR #300 unita su main il 2026-11-04 (P17, P18 fatte; P26 superata, l'eccezione ruff era già uscita in c6cbf81; P05 → 🙋, 9 caselle 4g-2 al DM). Trovato: l'«ERRATA §2.3» di P17 è di ARC-07, non ARC-08; le skill SRD sono fuori dal registro norme, quindi niente voce G3 per P18.

2026-11-04 Jfs: una voce si chiude **solo** se è già fatta, risolta o superata (con la prova su main), **mai** perché è ferma da tanto o è più semplice. Le card devono spiegare a parole cosa sono le cose, senza sigle. RECUPERO D5 rifatta così: 2 card (fallback pyyaml, migrazione JSON 30 mappe), il resto resta aperto.
2026-11-08: card «migrazione JSON 30 mappe» ritirata perché sbagliata: le mappe del Drappo sono JSON (formato vivo). Lezione: prima di dire «non esiste» cercare in tutto il repo (anche 10-stand-alone), non solo in campaign/. Resta valida la sola card pyyaml.
