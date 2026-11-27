---
name: regole-lotto-caratteristiche-2026-11-25
description: Thread delle regole al 26/11: #521 (caratteristiche, regola di Jfs del 20/11) verificata, corretta e pronta, in attesa del via del coordinatore; Grimjaw fuori; cosa resta dei plugin
metadata:
  type: project
  modified: 2026-11-26T12:52:53.407Z
---

Thread «Completare le regole senza omissioni», stato al 2026-11-26 12:50 UTC. Continua [[regole-stato-2026-11-14]].

- #521 UNITA su main il 26/11 12:50 UTC: 912a8a2d, voce MS-0227 (campo PR «—», alla piega mettere #521). Ramo claude/project-thread-fv2zai riallineato su 912a8a2d.
- Cosa c'è dentro oltre al lotto: verifica di regolista e custode-canone del 25/11 (elenco in /mnt/project-files/regole-razze-dv-2026-11-20/VERIFICA-AGENTI-521-2026-11-25.md), card di Jfs del 26/11 «Tutto, anche quelli già su main» (15 numeri in 8 schede, 3 copie) e «Sì, entrano nel tesoro» (cinque oggetti +2 di Balvar nel tesoro della tenda, 49.750 → 69.750 mo), estrattore di `[razze_dv]`, due rilievi di Codex sul verificatore.
- 26/11: tredici card scelte (sette + sei dopo il ricalcolo del regolista), applicate nella PR #523 (unita a3cff99e) (testa ccd5f87d, MS-0228; sacerdotessa rinominata -cr10). Il 26/11 18:25 Jfs ha chiuso anche le ultime due (Zin'thara «Via Focalizzati Superiore», stalla «Sangue nero e Attacco Mortale»): testa 4d1cc503. #517 unita (55d1698b) e fusa nella #523 (1325747b): voce ora MS-0230. Grimjaw in corso. Poi Grimjaw dopo #517. Scelte e file: /mnt/project-files/regole-razze-dv-2026-11-20/SCELTE-CARD-2026-11-26.md, RICALCOLO-REGOLISTA-2026-11-26.md, PATCH-STATE-MAEWEN-GS11.md.
- Domande aperte al DM (MS-0227 «Solo qui»): tempo per sfilare a Balvar morto gli oggetti indossati; Lythiel elfa dei boschi di 220 anni; sicari del Palio coi numeri vecchi; RI e scudo della guardia nobile; talenti della sacerdotessa; Zin'thara senza riga del corredo; grimlock, stone giant, sahuagin in `[razze_dv]`.
- Grimjaw: card del 26/11 «A: Guerriero 11 + Robustezza» (122 pf, CA 27 con anello +1 e Volontà di Ferro, spada +24/+19/+14, CD 19, GS 15, ripiega sotto 61 e poi beve, ritirata sotto 30). Con le quattro card del Palio (due dosi, −4 ai tiri di Zona, fantino in mappa e Poste, sangue nero homebrew fuori corredo) nella PR #526, unita il 26/11 (0963e72f), voce MS-0233. Aperta a Jfs la card «Dove dorme il fantino la notte dell'assalto» (segnalino nella stalla, consigliata «nella stalla, accanto al box»): va in una PR piccola. Proposta e simulatore: /mnt/project-files/regole-razze-dv-2026-11-20/grimjaw-boost/.
- Regola di Jfs (20/11): passa chi, tolti razza, aumenti, età, oggetti e ira, è il .pcg citato, acquisto fino a 32, serie normale o d'élite. Misura fuori dal repo: `python3 -I /mnt/project-files/regole-razze-dv-2026-11-20/misura_regola_jfs.py . Bestiario`, 21 → 3.
- Aperto dal 21/11 (MS-0216): arco 09 Torneo P2B Tordek «Monk 13»; ARC07-DEF-4 «in ira»; 77% di Karruk; porte dell'Orbe Monaco 10/12.
- Promesso a Jfs dopo la #521: lotti 9-12 di ADR-0126, prezzi, mostri dei manuali, dadi degli attacchi naturali, 912 incantesimi PF1e senza scuola, verificatore cieco a razza, ira, derivati e copie.

**How to apply:**
- Prima di mettere su card «quale talento tolgo», verificare gli slot vincolati (bonus di classe: Mago 5° = metamagia/creazione/Padronanza).
- Una PR di schede si dichiara pronta solo dopo regolista e custode-canone: `verifica_scheda.py` non vede derivati sbagliati né copie in prosa.
- Il classificatore della modalità auto nega le modifiche a schede e copie senza il sì di Jfs su card: non aggirare, chiedere.
- Mai una marca INFERRED né una data in chiaro in un master stampato (`test_misura_standard_tavolo`, `test_storico`): la dichiarazione si scrive «scelta del DM `[CANONE — DM data, card «…»]`:», la domanda aperta va nella voce MS.
- Prima di spingere contenuto di gioco, suite intera (`pytest -n 4`, 7 minuti): i test mirati non bastano.
- File di gioco a 10 commit in 60 giorni senza `<!-- storico -->` fa scattare adozioni_in_attesa.
