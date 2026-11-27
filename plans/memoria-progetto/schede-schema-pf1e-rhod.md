---
name: schede-schema-pf1e-rhod
description: Standard delle schede contro Burnt Offerings e Red Hand of Doom (Jfs 13/11): ordine PF1e e voci mancanti su main, due colonne in prova fino al 28/11, corredo RC-001: dieci schede su main al 16/11
metadata:
  type: project
---
Jfs 2026-11-13 20:21: le schede hanno perso voci rispetto a PF1e e Red Hand of Doom («manca ad esempio l'equipaggiamento»). Rapporto: /mnt/project-files/schede-schema-2026-11-13/CONFRONTO-SCHEDE.md. Deciso sulla card (13/11 21:57): «Voci mancanti, ordine PF1e»: Difesa · Attacco · Tattiche · Statistiche · Capacità speciali, equipaggiamento in due voci (da combattimento, altro).

**How to apply:** riempire solo da testo già nel repo o dall'SRD; ciò che non è scritto va a Jfs su card, scheda per scheda. Ogni riga di equipaggiamento aggiunta passa per `verifica_scheda.py Bestiario 0*/ --json` (verifica `ricchezza`, Tabella 4-23 al livello effettivo) e, se tocca DEF-4, per `misura_stampa --tutti --check`. Coordinarsi col thread delle regole ([[regole-senza-omissioni]]); l'ordine dei merge lo dà il coordinatore.

**Stato al 14/11:** #415 (ordine PF1e, MS-0107) e #420 (voci mancanti in sei schede di DEF-4, merge 91a34b37, MS-0113) sono su main. Serata Notte e Alba a 126 pagine (accettate da Jfs sulla card), totale 991.

**Due colonne nel riquadro (Jfs 13/11 23:30 sulla card: «Sì, due colonne nel riquadro», in prova 14 giorni):** terza PR, ADR-0133, MS-0114, cancello `scripts/tests/test_scheda_due_colonne.py`. Nel tema (`intero` in scripts/typst/tema-rumblingstone.typ) il corpo va in `columns(2)` quando `page.columns == 1` e il corpo a mezza larghezza è alto almeno 6 cm. Misura contro main 91a34b37 nei 36 riquadri larghi: righe oltre 100 caratteri 174 → 11, mediana 99 → 64, pagine 991 → 990; veraPDF ua1 e 2a conformi. Restano tre schede sotto soglia con righe fino a 126 caratteri (guardie di Zog'tar, Treant di Adamantio e copia giocatori): abbassare la soglia è scelta di Jfs. **Il 28/11 chiedere a Jfs su card se le due colonne restano** (scade la prova). Script di misura delle righe (non nel repo): riquadri col fondo #efe6d2 larghi oltre il 55% della pagina che contengono «DIFESA».

**Corredo RC-001 (ADR-0134), stato al 16/11 01:15 UTC:** su main dieci schede, ognuna decisa da Jfs su card nel thread del volume. #445 (5fb61280, MS-0140): Fantino Ladro, Drow Chierica, Collezionista. #458 (91a4f1be, MS-0154): Dovil, Drow Assassina, Duergar mago/ladro, Maewen, Varis, Tempestas, Therysol. Dettagli e conti in plans/MEMORIA-STORICA.md (MS-0140, MS-0154). Nessuna card aperta. Varis e Tempestas hanno oggetti che la CA o l'attacco già contavano e la card non nominava (detto a Jfs; se li vuole fuori si tolgono).

**Come si fa:** prima fonte ciò che i numeri della scheda già usano, poi l'export PCGen o la prosa; sopra la Tabella 4-23 serve la riga «Equipaggiamento sopra la tabella: scelta del DM (card del …)»; nota «> RC-001 (data, ADR-0134) `[CANONE — DM …, RC-001]`» in fondo; poi `impronta_creature.py --scrivi`. `verifica_scheda` non legge Acolita né i modelli draconici (Therysol non verificabile).
Da verificare se ancora dovute (erano nella versione lunga di questa nota): card sui linguaggi bonus di Zog'tar (Int 16) e del sacerdote (Int 14).

**#478 unita il 19/11 (merge 2ebb687c sopra d8f9f6b6, MS-0188):** ricontrollo delle dieci schede chiesto da Jfs. Corrette quattro note (contatto di Dovil, tetto di Drow Assassina e Drow Chierica al livello effettivo 11 = 21.000), 10 quadrelli alle due balestre, e per scelta di Jfs sulla card la Drow Assassina ha la balestra a mano perfetta: +12, +13 entro 9 m con Tiro Ravvicinato (10.811 mo). Lasciato: il +1 ai danni entro 9 m non è nella riga; tabella in prosa di Varis senza giaco +1 e pugnale +1. Lezione: prima di dire che un attacco non torna, contare i talenti (Tiro Ravvicinato).

**#494 unita il 19/11 (0f9c36da, MS-0202):** scelte di Jfs sulle card del 19/11: Drow Assassina entro 9 m +13 (1d4+1 + veleno); tabella in prosa di Varis con giaco +1 e pugnale +1. Jfs tiene gli oggetti aggiunti senza card (Varis, anello di Tempestas, quadrelli). Nulla resta aperto sul corredo RC-001 delle dieci schede.
