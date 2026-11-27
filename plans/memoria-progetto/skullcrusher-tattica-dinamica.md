---
name: skullcrusher-tattica-dinamica
description: Audit del 15/11 sulla tattica di Skullcrusher (ARC-07 DEF-4 Scena 11): cortile, PG in volo e invisibili, motivo dell'attacco; quattro card aperte a Jfs
metadata:
  type: project
  modified: 2026-11-15T08:04:34.283Z
---

Thread «Rendere dinamica la tattica di Skullcrusher» (15/11/2026, main 5fb61280). Audit su `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`, Scena 11 e schede A.1/A.1-bis.

Cosa è emerso:
- «Chi sceglie» (r.3302, r.3556) è già dinamico sul chi; il dove è fisso sul cortile M7-B, e l'unica alternativa scritta è «fuori dalle mura».
- r.2403 «cala sul cortile dove sta il re» regge poco: alla fine della Scena 10 i PG e il re sono sulle mura, e dalla piana (100 m più in basso) l'orda non vede il cortile, contro il «davanti all'orda» di r.2400. Appiglio non usato: la porta principale si apre sul cortile (M7-B, riga 18).
- La scheda del Vecchio ha già *vedere invisibilità*, *dissolvi magie* e *lentezza* (D64), volo a 45 m: la tattica contro i PG in volo si fa senza numeri nuovi.
- r.4212 dice 50 minuti per *vedere invisibilità*: è il numero dell'Adulto (incantatore di 5°); col Vecchio (7°) sono 70.
- B13 (BARILE r.634): la caduta secca da 48 m per 15d6 non è SRD. Per l'SRD chi perde il *volare* scende di 18 m a round per 1d6 round; e da 48 m sarebbero comunque 16d6.

Quattro card aperte nel thread, tutte con la prima opzione consigliata: (1) il cortile come porta principale più il re; (2) la tabella «Dove sono i PG all'alba»; (3) *vedere invisibilità* lanciata al corno; (4) B13 secondo l'SRD. La card 4 pesa già sulla serata, nello sgancio.

**Why:** nella scheda si scrive solo dopo le scelte di Jfs (vedi [[feedback-numeri-piu-forti-calcolati]] e [[card-solo-se-risolte]]).
**How to apply:** dopo le scelte, una PR sul ramo del thread con voce MS, `coerenza_campagna.py fatti DIR --tattiche` e i test del Bestiario.

Aggiornamento 15/11, 08:55 UTC: tutte e otto le card scelte da Jfs sulla consigliata (cortile per la porta principale e il re, tabella, vedere invisibilità al corno, B13 secondo l'SRD, chi colpisce l'orda dall'alto subito dopo la Catena, alla prima paura esita, inchiodato attacca chi tiene la corda, dissolvi solo su chi in aria lo minaccia). PR #448 in bozza su main 78b3dfb2. Misura: duelli T1 con un PG morto dal 79% al 42%; il drago muore nello 0-5%. Pendenze note: test_fase1 rosso per il clone shallow; impronte conformita_statblocchi rosso anche su main.

Unita il 15/11: #448 merge c0c5206a sopra 78b3dfb2, MS-0142. In CI la stampa del booklet della serata falliva per un bug dei tag PDF/UA di typst 0.15.1 legato all'impaginazione (internal error: tags weren't properly closed, riportato dal motore come «binario typst non nel PATH»); aggirato dividendo il capoverso di B13. Si trova applicando i pezzi del diff uno alla volta al .typ di main.
