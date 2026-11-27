---
name: usabilita-al-tavolo
description: ADR-0107 e misura_standard_tavolo: chi si incontra sta nel capitolo, appendice schede resta (PR #306, 2026-11-03)
metadata:
  type: project
  modified: 2026-11-03T00:08:53.241Z
---

Dopo la serata del 2026-11-02 (Zog'tar senza descrizione nel capitolo del barile, numeri in appendice, mappe M7-C/M7-H assenti) Jfs ha fissato lo «standard sindacale»: in ogni capitolo, accanto alla scheda, ci vanno descrizione, immagine, chi è e cosa vuole. Il booklet si legge da DM prima della consegna.

- PR #306 (bozza, 2026-11-03): ricerca `plans/RICERCA-USABILITA-AL-TAVOLO-2026-11.md` (14 criteri dalla rete), `scripts/misura_standard_tavolo.py` (indicatore) e ADR-0107 **proposta**, che emenda ADR-0105 §7.
- Jfs 2026-11-03: «voglio anche l'appendice con le schede perché erano fatte bene». Va scheda nel capitolo E appendice, modo manifest `"schede": "entrambe"`.
- Misura su main (7de45df): 6 complete su 145 coppie capitolo × persona, 0 con numeri nel capitolo, «chi è» al 6%, mappa nel capitolo in 7 scontri su 41.
- Da fare: riga «Chi è» nelle schede d'entrata (ARC-07 prima), skill module-standard/playtest aggiornate, cricchetto CI.
- Nessun plugin serve.
- Prova 2026-11-03 (Jfs: «facciamo la prova…», commit 30fa09e su #306): dmcore/chi_si_incontra.py + manifest `"chi_si_incontra": true` con `"schede": "entrambe"` (nome e tema presi dalla #305, a867d35). Misura più severa: complete vere 3 (non 6); numeri nel capitolo 0→25/151, mappe vicine 4→8/41, solo ARC-07. Cieco DM e playtester: entrambi scelgono la nuova. «Chi è» dal titolo bocciato e tolto. Aperti: fascia TATTICHE sopra il piede dopo tabella float (parametro nel tema dopo merge #305), errori di contenuto DEF-4 (M7-C vs testo, CD del Vecchio 22/26, scurovisione Zog'tar). PDF prima/dopo in /mnt/project-files/usabilita-al-tavolo/.

Legato a [[booklet-letto-da-dm]] e [[riquadro-creature-booklet]].

2026-11-03 (Jfs: guardrail a tutte le skill, transformer/document AI solo se misurano un guadagno), commit ed0bb35 su #306, ADR-0108 proposta: `conformita_statblocchi --master` legge i recinti ADR-0091 (6 conti veri: corrompere l'acqua Vecchio 25/26, scurovisione Zog'tar/Durin/wyvern, pf Balvar 101/97, pf Treant DEF-3 90/95); note di lavoro in stampa 60 (Notte e Alba 19); cricchetti nei test; `misura_distanza_pagine.py` sul PDF (Zog'tar 23,5→5); sezione «Cancelli deterministici» in tutte le 18 skill con test. Provati e scartati con misura: embedding MiniLM per box ripetuti (+1 parafrasi su 362), regex box «telecomando» (2/15). NLI rimandato a 30 contraddizioni etichettate. Venv con torch/sentence-transformers solo nello scratchpad. Pagina prima/dopo: https://claude.ai/artifact/7EpzTvPF6UPuWU1VAC664P
Jfs 2026-11-03 06:17: dopo l'ultimo merge di questo thread (#306, che va dopo la #305) la documentazione, il README e l'architettura si aggiornano in un thread separato: lo avvia il coordinatore quando glielo scrivo. Nel frattempo: tecniche di text AI avanzate assenti dal repo, adottate solo con prima/dopo misurato.
2026-11-03 Jfs 07:37: «metti insieme tutto e mergia», standard solo ciò che migliora. #305 fusa dentro #306 (f01b9f9), ADR-0107 e ADR-0108 **accettate** (ce5db49). chi_si_incontra+entrambe in 6 booklet (Terros escluso: si allunga). Tema: tabella «Chi si incontra» sempre `top`, riquadro misurato dove cade. NLI (mDeBERTa xnli) provata fino in fondo: F1 0,86 su coppie etichettate, 0 contraddizioni nuove nelle prime 30 sul repo (non sa di quale creatura parla una riga): non adottata, ricerca §7. Card a Jfs: correggere all'SRD i 4 conti rimasti (Treant 90→95, Balvar 101→97, scurovisione Durin e wyvern). Dopo il merge: thread documentazione/README/architettura dal coordinatore con cmsg_019sykApdKEBBe8D8NJyiFEG4jqobHWut7p4gVrzXMBJat.
PR #306 unita su main il 2026-11-03 (47489fb), #305 segnata unita con lei. Coordinatore avvisato per il thread doc/README/architettura.
[riga riservata · sha256:ac72912f]
