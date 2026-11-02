# Karkilan, Minotauro Berserk [TRANSCRIBED — PCGen, L1 2026-07-08]
**Faction**: red-hand | **Role**: melee-heavy | **Environment**: dungeon | **CR**: 5 | **Source**: PCGen export `Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/Minotaur karkilan cr5.htm` (+ `Minotaur karkilan.pcg`) | **Status**: transcribed-pcgen


```statblocco
gs: 5
tipo: Large monstrous humanoid, 7 HD (Minotauro 6 / Barbarian 1), CE
ca: 18
ca-dettaglio: contatto 9, colto alla sprovvista 18 (-1 taglia, +5 naturale, +4 giaco di maglia; astuzia naturale: mai colto alla sprovvista)
pf: 67
pf-dado: 6d8+1d12+28
ts: Temp +10, Rifl +5, Vol +7
attributi: For 23 Des 10 Cos 19 Int 7 Sag 10 Car 8
velocita: 12 m
iniziativa: +0
sensi: scurovisione 18 m, fiuto
attacchi:
  - Mischia grande ascia +1 a due mani +13/+8 (3d6+10/x3) e incornata +7 (1d8+3)
  - Mischia incornata +12 (1d8+6) da sola; Carica Devastante incornata +14 (4d6+9)
  - Distanza giavellotto +6/+1 (1d8+6)
voci:
  - Talenti: Tempra Possente, Attacco Poderoso, Volontà di Ferro
  - Ira 1/giorno (7 round)
```

> [GENERATO] `attributi` copiati dalla riga delle caratteristiche di questa stessa scheda da `scripts/genera_attributi.py`.

> **Conti rifatti sul SRD, senza far scendere nessun numero**:
> - **CA 18**: −1 taglia, +5 naturale del minotauro SRD, +4 giaco di maglia, Des 10. L'export dava 16 (contatto 7), cioè la CA in ira.
> - **Vol +7**: col solo Barbaro 1 il conto dà +5 (minotauro +5, Sag 10). L'export scriveva *Powerful Charge* fra i talenti, ma la Carica Devastante è una capacità razziale del minotauro, non un talento: al suo posto **Volontà di Ferro**, che riporta la Volontà a +7 come la scheda la dava.
> - **Incornata**: con la grande ascia è un attacco secondario (−5, metà For): +7 (1d8+3). Il +12 (1d8+6) resta quando incorna da sola, e in carica sale a +14 (4d6+9).
> - **pf 67**: il primo dado (il d12 del barbaro) al massimo, gli altri alla media.

Large monstrous humanoid, 7 HD (Minotauro 6 / Barbarian 1), CE. Tutto SRD.

**Iniziativa** +0 · **Sensi** scurovisione 18 m, fiuto; Ascoltare +8, Osservare +7, Cercare +2

**Difesa** **CA 18**, contatto 9, colto alla sprovvista 18 (astuzia naturale: mai colto alla sprovvista) · **pf 67** (7 DV) · TS Temp +10, Rifl +5, Vol +7

**Attacco** Vel 12 m · Spazio 3 m, portata 3 m · **Mischia** grande ascia +1 a due mani +13/+8 (3d6+10/x3) e incornata +7 (1d8+3); oppure incornata +12 (1d8+6) · **Carica Devastante** (Str): in carica, incornata +14 (4d6+9) · **Distanza** giavellotto +6/+1 (1d8+6) · **Ira** 1/giorno (7 round: For 27, Cos 23, Vol +9, CA 16, +14 pf → 81; grande ascia +15/+10, 3d6+13; incornata +9, 1d8+4)

**Statistiche** For 23, Des 10, Cos 19, Int 7, Sag 10, Car 8 · BAB +7; Lotta +17 · **Talenti** Tempra Possente, Attacco Poderoso, Volontà di Ferro · **Abilità** Intimidire +3, Saltare +8 · **Equipaggiamento** grande ascia +1 (Grande), giaco di maglia (Grande), giavellotti e asce da lancio (Grandi), pozione di *volare*, pozione di *cura ferite gravi*, pozione di *cura ferite leggere*

**Capacità speciali**
- **Astuzia naturale** (Str): immune a *labirinto*, non si perde mai, segue le tracce, non è mai colto alla sprovvista.
- **Movimento veloce** del barbaro (già nella velocità).

**Tattiche**
- *Prima del combattimento*: aspetta nei corridoi stretti della fortezza, dove la sua portata conta e i PG non lo possono circondare. Non si nasconde: si fa sentire, perché vuole che vengano da lui.
- *Durante il combattimento*:
  - **Round 1**: entra in ira e carica il PG con l'armatura più pesante: Carica Devastante, incornata +16 in ira (4d6+12).
  - **Round 2 e seguenti**: attacco completo con la grande ascia e Attacco Poderoso a −4 sullo stesso bersaglio, finché cade; poi il più vicino. In un corridoio usa la portata di 3 m per colpire chi gli si avvicina.
  - Contro chi vola o resta fuori portata: giavellotti; se gli manca il bersaglio per due round beve la pozione di *volare*.
- *Morale*: in ira combatte fino alla morte. Finita l'ira, affaticato e sotto 20 pf, beve *cura ferite gravi* e si ritira verso Koth; se Koth è caduto o fuggito, combatte fino alla fine, nei corridoi che conosce meglio di chiunque.

**Benchmark** PF T1-1 riga 5 (CA 18, pf 55, att. +10, danno medio 20, CD 15): CA 18 ✓ · pf 67 ✓ · att. +13 ✓ · danno completo ≈ 24, ≈ 50 in carica ✓. È un GS 5 pieno; contro APL 13 è un colpo di colore o la guardia del corpo di Koth.

Notes: campione minotauro nominato al servizio della Mano Rossa, il «generale» di Koth alla fortezza di Vraath (RHoD); unico → `villain/`.

Boost log: correzione sul SRD — GS 5 → 5 — CA 18 senza il malus dell'ira, Volontà di Ferro al posto del doppione della Carica Devastante, incornata secondaria contata giusta.

<!-- storico -->
era: CA 16, contatto 7, colto 16, dall'export PCGen (è la CA in ira).
era: talento «Carica Devastante» (Powerful Charge), dall'export PCGen: è la capacità razziale.
era: «grande ascia +13/+8 (3d6+10/x3) e incornata +12 (1d8+6)» insieme, dall'export PCGen.
era: la nota «la CA di contatto suggerisce Des 6, la fonte dice 10»: il contatto 7 era quello in ira.
<!-- /storico -->
