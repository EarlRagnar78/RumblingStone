# Bebilith (guardiano delle rovine) [TRANSCRIBED — SRD, L1 2026-07-08]
**Faction**: aberration | **Role**: melee-heavy-boss | **Environment**: dungeon | **CR**: 10 | **Source**: SRD (D&D Wiki, `Bestiario/pregen-pcgen/00_cr10_guardiano_delle_rovine_prima della cattedrale_SRD_Bebilith - D&D Wiki.htm`) | **Status**: transcribed


```statblocco
gs: 10
tipo: Huge outsider (chaotic, evil, extraplanar), 12d8+96
ca: 22
ca-dettaglio: contatto 9, colto alla sprovvista 21 (-2 taglia, +1 Des, +13 naturale)
pf: 150
pf-dado: 12d8+96
ts: Temp +16, Rifl +9, Vol +9
attributi: For 28 Des 12 Cos 26 Int 11 Sag 13 Car 13
velocita: 12 m, scalare 6 m
iniziativa: +5
sensi: scurovisione 18 m, fiuto, telepatia 30 m
attacchi:
  - Mischia morso +19 (2d6+9 più veleno) e 2 artigli +14 (2d4+4)
  - Distanza ragnatela +11 (contatto, 4/giorno)
voci:
  - RD 10/bene
  - Veleno (Temp CD 24, 1d6 Cos / 2d6 Cos), squarciare armatura (4d6+18 all'armatura), ragnatela, spostamento planare
  - Talenti: Fendere, Iniziativa Migliorata, Lottare Migliorato, Attacco Poderoso, Seguire Tracce
fonte: SRD — letto dal file citato dalla scheda (`pregen-pcgen/00_cr10_…_SRD_Bebilith - D&D Wiki.htm`); la scheda diceva «CA da SRD» e il numero è 22, non uno dei valori che si ricordano a memoria
```

> [GENERATO] `attributi` copiati dalla riga delle caratteristiche di questa stessa scheda da `scripts/genera_attributi.py`.

> **Lotta +33**: il SRD stampa +29 (BAB 12 + For 9 + taglia 8), ma il bebilith ha Lottare Migliorato, che dà +4 alle prove di lotta. Si tiene il numero più alto, che il talento della scheda giustifica.

Huge outsider (chaotic, evil, extraplanar), 12d8+96.

**Iniziativa** +5 · **Sensi** scurovisione 18 m, fiuto, telepatia 30 m; Ascoltare +16, Osservare +16

**Difesa** **CA 22** (-2 taglia, +1 Des, +13 naturale), contatto 9, colto alla sprovvista 21 · **pf 150** (12 DV) · TS Temp +16, Rifl +9, Vol +9 · **RD 10/bene**

**Attacco** Vel 12 m, scalare 6 m · Spazio 4,5 m, portata 3 m · **Mischia** morso +19 (2d6+9 più veleno) e 2 artigli +14 (2d4+4) · **Distanza** ragnatela +11 contatto (4/giorno, gittata 9 m) · **Veleno** (Str): ferimento, Temp CD 24, 1d6 Cos iniziale e 2d6 Cos secondario · **Squarciare armatura** (Str): se colpisce con entrambi gli artigli, 4d6+18 danni all'armatura del bersaglio · le sue armi naturali contano come caotiche e malvagie per superare la RD

**Statistiche** For 28, Des 12, Cos 26, Int 11, Sag 13, Car 13 · BAB +12; Lotta +33 · **Talenti** Fendere, Iniziativa Migliorata, Lottare Migliorato, Attacco Poderoso, Seguire Tracce · **Abilità** Scalare +24, Nascondersi +16, Saltare +28, Muoversi Silenziosamente +16, Cercare +15, Percepire Intenzioni +16 · **Linguaggi** capisce l'abissale, non lo parla; telepatia

**Capacità speciali**
- **Ragnatela** (Str): 4 volte al giorno, come una rete, gittata 9 m (incremento 3 m), contro creature fino a Mastodontica. Ancora il bersaglio sul posto. Per uscirne: Artista della Fuga CD 24 o Forza CD 24; la ragnatela ha 14 pf e durezza 0, e ha il 75% di probabilità di non prendere fuoco.
- **Spostamento planare** (Sop): solo su sé stesso, come l'incantesimo, LI 12°.
- **Squarciare armatura** e **veleno**: sopra. Il veleno si guasta all'aria: non si raccoglie.

**Tattiche**
- *Prima del combattimento*: aspetta davanti alla cattedrale, aggrappato in alto fra le rovine (Nascondersi +16 con la livrea a macchie). Sente i PG con la telepatia e il fiuto prima di vederli, e sceglie la preda: la creatura più vicina che porta un'armatura pesante.
- *Durante il combattimento*:
  - **Round 1**: cala dall'alto e lancia la ragnatela sull'incantatore che vede, per tenerlo fuori dallo scontro; poi Attacco Poderoso sulla preda scelta.
  - **Round 2 e seguenti**: attacco completo sempre sulla stessa preda, morso e due artigli. Ogni volta che entrambi gli artigli colpiscono, l'armatura si squarcia: contro Thorik e Tordek è il pericolo vero, perché li spoglia. Fendere sul secondo bersaglio se il primo cade.
  - Usa le ragnatele che restano su chi prova a soccorrere la preda.
- *Morale*: sotto 50 pf morde un'ultima volta chi è più vicino e se ne va con lo spostamento planare, lasciando che il veleno lavori. Il SRD lo dice di tutti i bebilith: quando gli avversari sono troppi, mordono e si ritirano.

**Benchmark** PF T1-1 riga 10 (CA 24, pf 130, att. +18, danno medio 45, CD 19): CA 22 ✗ sotto · pf 150 ✓ sopra · att. +19 ✓ · danno completo ≈ 30 più veleno e armatura ✗ sotto · CD 24 ✓ sopra. Un GS 10 onesto: vale per quello che rompe, non per quello che toglie in pf.

Notes: guardiano evocato posto davanti alla cattedrale (SRD Bebilith). Statblock SRD standard; nel repo non c'è una versione avanzata.

Boost log: nessun potenziamento, correzione sul SRD — GS 10 → 10 — attacco completo (un morso e due artigli, non due morsi), ragnatela, veleno e squarciare armatura scritti coi numeri del SRD; Lotta +33 per Lottare Migliorato.

<!-- storico -->
era: «Mischia 2 morsi + zampe» nella prosa e «2 zampe (squarciare armatura)» nel blocco, senza numeri; il SRD dà un morso e due artigli +14 (2d4+4).
era: «Ferita (morso sanguinante)» fra le capacità: nel SRD è il veleno.
era: Lotta +29, dalla fonte SRD.
<!-- /storico -->
