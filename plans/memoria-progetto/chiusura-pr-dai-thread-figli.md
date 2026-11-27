---
name: chiusura-pr-dai-thread-figli
description: Regola di Jfs (2026-10-23): i thread figli testano e avvisano; il merge delle PR lo fa solo il thread padre (coordinatore), che tiene la lista delle PR aperte
metadata:
  type: feedback
  modified: 2026-10-23T12:57:47.592Z
---

Quando la PR di un thread figlio ha la CI verde e i test sono conclusi, il thread:
1. avvisa tutti i thread interessati, con il test fatto e i risultati, così che aggiornino le loro parti;
2. passa la PR al thread padre per il merge, con un riassunto: è il thread «Audit settimanale PR e decisioni» (cmsg_019sykApdKEBBe8D8NJyiFEGUzDsB4hQ7TncCjVE1i2jDW), con message_thread. Il figlio non unisce.

Il thread padre tiene la lista di tutte le PR aperte e incomplete e le aggiorna in un posto solo. I figli fanno test, sviluppo, verifiche e aggiornamenti.

**Why:** Jfs, 2026-10-23, thread «Stanza contro spaCy»: vuole tutto allineato in un solo thread padre, mentre i figli lavorano.

**How to apply:** a CI verde, mandare message_thread ai thread coinvolti e message_coordinator con PR, esito e base del merge. Dire a Jfs in una riga che il merge è passato al padre.

**Aggiornamento 2026-11-12 (Jfs, 10:51 UTC).** Regola permanente: il coordinatore unisce una PR su main senza un nuovo sì di Jfs se valgono tutte e tre: CI verde e mergeable clean; nessun problema o misura omessi (limiti e residui dichiarati nella PR e nel thread); miglioramento misurato rispetto a main. Se una manca non si unisce e si dice quale. Merge uno alla volta, avvisando i thread coinvolti. Il thread figlio manda al coordinatore testa, misura del miglioramento e limiti dichiarati. Le decisioni che tolgono testo restano di Jfs.
