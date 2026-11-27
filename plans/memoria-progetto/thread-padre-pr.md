---
name: thread-padre-pr
description: Il thread «Audit settimanale PR e decisioni» è il thread padre delle PR di RumblingStone: tiene la lista delle PR aperte e fa i merge
metadata:
  type: project
---

Dal 2026-10-23 (richiesta di Jfs, relayed dal coordinatore): un solo thread padre, «Audit settimanale PR e decisioni», tiene la lista di tutte le PR aperte o incomplete e fa i merge (permesso generale scritto di Jfs, 23/10 14:40: «d'ora in poi unisci tu ogni PR che un thread figlio ti passa verde»; la sola card non bastava al classificatore automatico); i thread figli fanno sviluppo, test e verifiche, e quando la CI è verde e le prove sono concluse avvisano il padre (e i thread interessati) con test e risultati.
Lista viva: /mnt/project-files/pr-aperte/LISTA-PR.md (si aggiorna a ogni avviso o merge).
Mappa PR→thread al 23/10: #259 «Chiusura piano LETTORE-PLAYTESTER · F4»; #264 «Avventure della community a confronto»; #270 (base #264) «Stanza contro spaCy»; #234 «LLM locale per la prosa»; #99 «Piano per la PR 99 abbandonata»; #106, #228, #274 senza thread.
Riconfermato da Jfs il 23/10 16:11 («Unisci se sono verdi dai thread figli e notificati»): dopo un riavvio di contesto il classificatore non vede più il permesso, quindi se blocca si chiede di nuovo a Jfs una riga di conferma.
**How to apply:** dal 23/10 c'è il permesso generale; #234 unita così (36d03e6). Dependabot si fonde una alla volta con la sua riga in CHANGELOG. Vedi [[weekly-audit-routine-scope]].

2026-11-09 11:39 Jfs: «unisci le 2 pr e poi coordina il resto del lavoro con gli altri thread lungo la roadmap con il thread padre» → #358 unita (a57b226); #357 riallineata (0199c29). Il classificatore blocca i merge passati dai figli finché Jfs non scrive un sì diretto: chiederlo una volta per lotto, citando i numeri.
2026-11-09 23:57 Jfs: «aspetta che i thread siano completi e mergia nell'ordine concordato e coordinato con gli altri thread» → #364 (ADR-0118), poi #363 (ADR-0119), poi #365 (ADR-0121), ognuna quando il suo thread dice di aver finito e la CI è verde sulla testa.
2026-11-09 23:59 Jfs (thread #363, citato dal coordinatore): «Coordinati con gli altri threads per andare avanti e mergiare quando finito dando sì al thread padre senza deadlock» → il sì copre #364 e #363 a lavoro finito e CI verde nell'ordine concordato; la #365 dopo il via del suo thread (riallinea a main dopo la #363).
2026-11-10: eccezione. Jfs nel thread delle regole (v1.2.0) ha chiesto a quel thread di unire da sé le sue PR pronte e verdi (#369 c185b11, poi #372 e lotti 2, 4, 5). Il padre tiene la lista e non unisce in parallelo PR che toccano CHANGELOG/MEMORIA finché quel thread non avvisa di aver finito. Milestone GitHub: il padre assegna la milestone a ogni PR aperta.
2026-11-12 10:51 Jfs (chat di progetto): regola permanente. Una PR di un thread si unisce senza un nuovo sì se valgono tutte e tre: CI verde e mergeable clean; nessun problema o misura omessi (limiti e residui dichiarati); miglioramento misurato rispetto a main. Merge coordinati dal padre, uno alla volta: prima testa e misura al padre, dopo SHA e file condivisi toccati; avvisare i thread coinvolti.
2026-11-12: **il thread padre non unisce più.** Regola di Jfs del 12/11 (vedi [[chiusura-pr-dai-thread-figli]]): coda unica del coordinatore del progetto, ogni PR la unisce il suo thread al suo via. Il padre tiene LISTA-PR.md, roadmap e milestone GitHub, e riceve SHA a ogni merge. Un sì di Jfs su una card del padre va passato al coordinatore, non eseguito.
