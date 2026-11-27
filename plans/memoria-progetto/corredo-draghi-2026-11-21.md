---
name: corredo-draghi-2026-11-21
description: Thread «Equipaggiare tutti i draghi della campagna» (21/11): inventario del corredo dei draghi vs tesoro, 5 card aperte, report in /mnt
metadata:
  type: project
  modified: 2026-11-21T01:23:24.539Z
---

Richiesta di Jfs del 21/11: Fauci e gli altri draghi non devono sembrare marionette accanto a Skullcrusher Vecchio (pacchetto «Signore del terrore», 53.000 mo su 108.000, non ancora nel repo: lo porta la PR del thread booklet ARC-07).

Report: /mnt/project-files/draghi-corredo-2026-11-21/INVENTARIO-E-PROPOSTE.md (+ misura_fauci.py, misura_tyr.py, girano sul simulatore di plans/esperimenti/tattiche-draghi-2026-11-15/).
Fatti: Fauci 0 oggetti (tesoro triplo 66k), Tyrgarun 0 (141k), Ozyrrandion 27%, Regiarix e drago di Vaereth senza oggetti e con incantesimi conosciuti mai scelti, Arbitrax 79% (ok). Misura: bonus solo difensivi a Fauci spostano gli esiti di 1-3 punti; servono gesti in scena. Tyrgarun con anello e mantello +3: Fase 4 −3/−5 punti alla sua morte.
Incoerenze: state.md r.220 «flees under 50 hp» (canone 112); ARC08-13 r.69 tesoro di Fauci da rifare se porta oggetti.
Card aperte 21/11 01:30 UTC (consigliata prima): Fauci A «Signore dell'assedio»; Tyrgarun B solo consumabili; Ozyrrandion A tentatore; Regiarix A; Vaereth A. Dopo le scelte: PR con catena regolista → custode-canone → autore-master → lettore-a-freddo → autore-documenti (agenti solo sul ramo della #510), voce MS.

**Why:** non rifare l'inventario. **How to apply:** vedi [[tattiche-draghi-2026-11-15]] e [[skullcrusher-tattica-dinamica]].

21/11 01:27: card scelte da Jfs: Fauci A (Signore dell'assedio), Tyrgarun A (Tempesta e ferro, contro la consigliata B), Ozyrrandion B (tentatore armato, contro la consigliata A), Regiarix A, Vaereth A. Lavoro sul ramo claude/project-thread-qhcgvh, una PR unica; agenti dalle definizioni del ramo della #510 (coordinatore: nessuna deroga, aspettare il suo via per unire).

21/11: PR #513 in bozza (testa ea0e8b37, MS-0214, gate 49/49, suite verde dopo impronta rigenerata). Non unire senza il via del coordinatore. Card ancora aperte (a)-(g), INFERRED con la consigliata: alla scelta, commit sullo stesso ramo.
21/11 06:05: Jfs ha chiuso (f) e (g) sulla consigliata; marche a CANONE nel commit 4beb5c42 sulla #513. Aperte (a)-(e).
21/11 06:20: tutte e sette le card chiuse sulla consigliata; testa #513 = 1fa6633d (Vaereth: raggio di indebolimento). Coda di merge: #513 per ultima dopo #506, #509, #511; al turno unire main, rinumerare MS, rigenerare MEMORIA.md, mandare la testa.
21/11 07:10: #513 dirty contro main ffb64bea (#505, #509): conflitti CHANGELOG, MEMORIA-STORICA, impronta, spells.md (#505 ha già corretto dominare persone; Tordek Monaco con mantello +1). CI non parte finché non si unisce main; si fa al turno di merge.
21/11 07:45: main 28422f87 unito nella #513, testa 3a1f0efd, voce MS-0218 (PR #513). Impronte plugin riscritte (derive_statblocks non propone più i TS di Fauci: legge 4.000 caratteri). In attesa che il thread della coda tolga la bozza e unisca.
21/11 07:55: testa #513 = 2b36a06b (thread coda: rimessa Confusion della #509, persa nella mia unione per un checkout --ours sull'intero spells.md). Lezione: in un conflitto si risolve il blocco, mai il file intero.
CHIUSO: #513 unita su main il 21/11 08:16 UTC (testa 2b36a06b, MS-0218), coordinata dalla coda di merge. Restano fuori: state.md r.220 (fuga 112, ramo di gruppo), GS 18/19 di Tyrgarun, simulatore coi numeri vecchi, derive_statblocks tronca a 4.000 caratteri.
