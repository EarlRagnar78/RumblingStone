---
name: feedback-standard-di-fatto
description: Regola Jfs 2026-11-08 per TUTTO il progetto (codice, mappe, storia, editoria, booklet): si parte dallo standard de facto e decide la misura
metadata:
  type: feedback
  modified: 2026-11-08T08:22:03.275Z
---

Jfs, 2026-11-08 (thread regolamenti plugin), poi esteso nello stesso giorno: la regola vale per **tutte le parti del progetto**, cioè codice e strumenti, mappe, storia e prosa, editoria e booklet.
- In ogni indagine o scelta il candidato di base è lo standard de facto della comunità di quel campo: per il codice le librerie più adottate, per la stampa le pratiche editoriali consolidate, per le mappe gli strumenti e i formati di riferimento, per la prosa le norme riconosciute.
- Una soluzione fatta in casa entra solo se la misura boccia lo standard, e il motivo va scritto nell'ADR.
- Decide sempre la misura, deterministica e dettagliata, non il gusto.
- Le librerie vanno portate dentro il pacchetto (bundle con tutti i requisiti, modello iemod-fetch), non installate con pip dove la skill gira.

**Why:** Jfs vuole un repo professionale, verificabile e automatizzabile, con meno errori veri.
[riga riservata · sha256:3e6bda34]

2026-11-27 07:22 Jfs (thread «Misurare e migliorare agenti, skill e automatismi»): «Non usare solo la stdlib ma tutte le librerie utilizzate come standard de facto della community». Vale anche per eval e metriche ML: scikit-learn (sklearn.metrics, DummyClassifier, MultinomialNB) e scipy, non reimplementazioni a mano. Entrano comunque per i canali di ADR-0099; l'hook che gira a ogni messaggio le importa solo in --eval/--check.

2026-11-27 (Jfs, thread «Misurare e migliorare agenti, skill e automatismi»): superata la parte «solo stdlib». Si usano le librerie standard di fatto della community senza reinventare la ruota, con il miglioramento misurato contro main. La riga vecchia dell indice è archiviata in coda (thread «Creare l agente custode della memoria»).
