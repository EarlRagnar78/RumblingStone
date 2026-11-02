# Confronto delle mappe di ARC-08, vecchie e nuove (2026-10-22)

Origine: la richiesta di misurare, senza toccarle, quanto sono cambiate le
mappe di Hammerfist nei due rifacimenti del 2026-10-21 e del 2026-10-22, e se
il voto di `scripts/qualita_mappe.py` è salito per le ragioni giuste.
Strumento: `scripts/confronta_mappe.py`, portato dalla prova di
`plans/esperimenti/mappe-strumenti-2026-10-22/confronta_versioni.py`.
Numeri completi in [`confronto.json`](confronto.json), un SVG affiancato per
mappa in [`svg/`](svg/).

## Le versioni

| | Commit | Cosa contiene |
|---|---|---|
| **A** | `d726e6a2` | le mappe prima di ogni rifacimento |
| **B** | `9359a0af` | una sola geometria della fortezza (tabella MISURE in testa alla L2: fronte sud 102 m, cinta 6 × 12 m, cancello 6 m e 200 pf) |
| **C** | `c6b61123` (HEAD) | quote a gradoni +80/+100/+120 m sulla piana (870 m) e standard ADR-0098 (`3dd46d78`), soffio di Fauci a Riflessi CD 29 (`7362834a`) |

Per le griglie C coincide con `7362834a`: il commit `3bda1038` aveva alzato
di 80 m le quote s.l.m. ed è stato annullato da `49aa52a4`, e `c6b61123`
rigenera solo `MEMORIA.md`. I file confrontati sono i tre master
`Mappe/Hammerfist-L1/L2/L3-REVISED-Ultra-Clear.md` e la copia della MAPPA 1D
nel master `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md`: 13 mappe, 12 nei master e
una copia. L'Atlante e `ARC08-01` non hanno griglie che il parser legga.

**Abbinamento.** Tutte le 13 mappe di C hanno la loro corrispondente in A e
in B, e nessuna mappa di A o B è sparita. Dodici si abbinano per titolo
identico. La 1A-3 ha cambiato titolo («griglia strategica» → «vista
strategica») e si abbina per codice `MAPPA 1A-3`.

## Sintesi

Voti di `qualita_mappe.py` (0-100) e celle cambiate, simboli e classi di
cella, sull'area della griglia più grande delle due:

| Mappa | File | A | B | C | A→C celle (simboli · classi) | B→C celle (simboli · classi) |
|---|---|---|---|---|---|---|
| 1A-2 | L1 #1 | 93 | 93 | 94 | 0 (0,0 %) · 0 (0,0 %) | 0 (0,0 %) · 0 (0,0 %) |
| 1A-1 | L1 #2 | 87 | 87 | 94 | 40 (2,0 %) · 40 (2,0 %) | 0 (0,0 %) · 0 (0,0 %) |
| 1A-3 | L1 #3 | 86 | 83 | 100 | 2369 (65,8 %) · 2098 (58,3 %) | 2369 (65,8 %) · 2098 (58,3 %) |
| 1D | L1 #4 | 97 | 97 | 98 | 0 (0,0 %) · 0 (0,0 %) | 0 (0,0 %) · 0 (0,0 %) |
| 2A | L2 #1 | 92 | 93 | 100 | 4206 (43,8 %) · 1608 (16,8 %) | 198 (2,1 %) · 110 (1,1 %) |
| 1 | L2 #2 | 96 | 96 | 100 | 740 (11,4 %) · 108 (1,7 %) | 668 (10,3 %) · 60 (0,9 %) |
| 2B-CORRETTA | L2 #3 | 78 | 93 | 94 | 1031 (99,1 %) · 248 (23,8 %) | 0 (0,0 %) · 0 (0,0 %) |
| H3-1 | L3 #1 | 91 | 87 | 94 | 2502 (86,9 %) · 1900 (66,0 %) | 170 (6,6 %) · 90 (3,5 %) |
| 3Y | L3 #2 | 78 | 78 | 94 | 604 (67,8 %) · 80 (9,0 %) | 604 (67,8 %) · 80 (9,0 %) |
| 3Z | L3 #3 | 43 | 43 | 98 | 1074 (98,6 %) · 528 (48,5 %) | 1074 (98,6 %) · 528 (48,5 %) |
| 5 | L3 #4 | 81 | 81 | 94 | 52 (1,5 %) · 51 (1,4 %) | 52 (1,5 %) · 51 (1,4 %) |
| 4 | L3 #5 | 85 | 85 | 100 | 722 (17,7 %) · 414 (10,2 %) | 586 (14,4 %) · 366 (9,0 %) |
| 1D | DEF-1 #1 | 97 | 97 | 98 | 0 (0,0 %) · 0 (0,0 %) | 0 (0,0 %) · 0 (0,0 %) |
| **Media** | | **84,9** | **85,6** | **96,8** | | |

Per come sono cambiate, le mappe stanno così.

- **Rifatte da zero** (metà delle classi cambiate o più, Jaccard sul muro
  vicino a 0): 1A-3, 3Z, H3-1 fra A e B, e la 2B fra A e B se si guardano i
  simboli. Per queste il confronto cella per cella dice solo che il disegno è
  un altro.
- **Corrette** (dall'1 al 20 % delle classi): 2A, MAPPA 1, MAPPA 4, MAPPA 5,
  3Y, 1A-1. Qui transizioni e Jaccard dicono cosa è cambiato e dove.
- **Ferme**: 1A-2 e 1D (nelle due copie) hanno la stessa griglia in tutte e
  tre le versioni, e la 2B fra B e C. Il punto in più viene dalle righe
  `@quota` e `@dislivello` (sparisce `contesto/quota-mancante`, peso 1).

Nessun rilievo è comparso, in nessun confronto. Dieci rilievi sono spariti
per deroga e non per correzione: due nella 1A-1, tre nella 2A, tre nella
H3-1, due nella MAPPA 5 (la tabella di ogni mappa dà i derogati di C).

## Mappa per mappa

Classi di cella: M muro, O ostacolo che non ferma la vista, P porta, S scala
fra livelli, H pericolo, K copertura, U creatura, `.` pavimento, V fuori
griglia. Jaccard = celle della classe in tutte e due le versioni, diviso le
celle della classe in almeno una; «—» vuol dire classe assente in entrambe.
Il voto è quello di `qualita_mappe.py` sui quattro file della stessa
versione misurate insieme, come lo calcola lo script sul corpus. I rilievi
sono `codice@cella`, `-` quando il rilievo vale per tutta la mappa. Negli SVG
i pannelli A e B cerchiano le celle diverse da C, il pannello C quelle
diverse da B: rosso dove compare un blocco, verde dove sparisce, ambra ogni
altro cambio di simbolo.

### MAPPA 1A-2 REVISED: Il Torrione di Vedetta (griglia densa)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`, mappa 1 · SVG: [`svg/Hammerfist-L1-REVISED-Ultra-Clear-01-1a-2.svg`](svg/Hammerfist-L1-REVISED-Ultra-Clear-01-1a-2.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 40 × 40 | 40 × 40 | 40 × 40 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (no) |
| `@quota` · `@dislivello` | — | — | 930 · +60 m |
| voto | 93 | 93 | 94 |
| rilievi non derogati · derogati | 4 · 0 | 4 · 0 | 3 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 0 (0,0 %) | 0 (0,0 %) |
| celle cambiate, classi | 0 (0,0 %) | 0 (0,0 %) |
| Jaccard muro M · pavimento . · creature U | 1,00 · 1,00 · 1,00 | 1,00 · 1,00 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 1,00 · — · 1,00 | 1,00 · — · 1,00 |
| Jaccard blocco · percorribile | 1,00 · 1,00 | 1,00 · 1,00 |
| transizioni principali | nessuna | nessuna |
| voto | 93 → 94 (+1) | 93 → 94 (+1) |
| rilievi spariti | `contesto/quota-mancante@-` | `contesto/quota-mancante@-` |
| rilievi comparsi | nessuno | nessuno |

La griglia è la stessa in tutte e tre le versioni. Il punto in più viene dalle righe `@luogo`, `@quota 930 m` e `@dislivello +60 m` aggiunte con le quote a gradoni (piana a 870 m): sparisce `contesto/quota-mancante`. Restano i 6 punti degli avvisi del collaudo, gli stessi di prima.

### MAPPA 1A-1 REVISED: Il Sentiero Nascosto (canyon completo)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`, mappa 2 · SVG: [`svg/Hammerfist-L1-REVISED-Ultra-Clear-02-1a-1.svg`](svg/Hammerfist-L1-REVISED-Ultra-Clear-02-1a-1.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 20 × 100 | 20 × 100 | 20 × 100 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (no) |
| `@quota` · `@dislivello` | — | — | 900 · +30 m |
| voto | 87 | 87 | 94 |
| rilievi non derogati · derogati | 6 · 0 | 6 · 0 | 3 · 2 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 40 (2,0 %) | 0 (0,0 %) |
| celle cambiate, classi | 40 (2,0 %) | 0 (0,0 %) |
| Jaccard muro M · pavimento . · creature U | 0,92 · 0,97 · 1,00 | 1,00 · 1,00 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 1,00 · — · — | 1,00 · — · — |
| Jaccard blocco · percorribile | 0,92 · 0,97 | 1,00 · 1,00 |
| transizioni principali | `.→M` 40 | nessuna |
| voto | 87 → 94 (+7) | 87 → 94 (+7) |
| rilievi spariti | `contesto/quota-mancante@-`, `fazioni/lontane@-`, `spazio/disperso@-` | `contesto/quota-mancante@-`, `fazioni/lontane@-`, `spazio/disperso@-` |
| rilievi comparsi | nessuno | nessuno |

Fra A e B la geometria unica ha chiuso la strozzatura a 9 m: 40 celle di pavimento diventate roccia (`.→M`) alle righe 10-14, colonne H-M. Fra B e C la griglia non cambia; il voto sale di 7 perché arrivano le quote (900 m, +30 m) e due deroghe motivate, `fazioni/lontane` e `spazio/disperso` (la scena è la risalita furtiva). Due dei tre rilievi spariti sono quindi deroghe, e non correzioni.

### MAPPA 1A-3 REVISED: Campo della Mano Rossa (vista strategica)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`, mappa 3 · SVG: [`svg/Hammerfist-L1-REVISED-Ultra-Clear-03-1a-3.svg`](svg/Hammerfist-L1-REVISED-Ultra-Clear-03-1a-3.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | codice | codice | — |
| quadretti | 40 × 50 | 40 × 50 | 60 × 60 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 6 m (sì) | 3 m (sì) |
| `@quota` · `@dislivello` | — | — | 870 · +0 m |
| voto | 86 | 83 | 100 |
| rilievi non derogati · derogati | 6 · 0 | 7 · 0 | 0 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 2369 (65,8 %) | 2369 (65,8 %) |
| celle cambiate, classi | 2098 (58,3 %) | 2098 (58,3 %) |
| Jaccard muro M · pavimento . · creature U | 0,00 · 0,42 · 0,03 | 0,00 · 0,42 · 0,03 |
| Jaccard copertura K · porte P · pericolo H | 0,00 · — · 0,00 | 0,00 · — · 0,00 |
| Jaccard blocco · percorribile | 0,00 · 0,54 | 0,00 · 0,54 |
| transizioni principali | `V→.` 1528, `U→.` 311, `.→M` 83, `.→K` 67 | `V→.` 1528, `U→.` 311, `.→M` 83, `.→K` 67 |
| voto | 86 → 100 (+14) | 83 → 100 (+17) |
| rilievi spariti | `contesto/quota-mancante@-`, `m1/copertura@-`, `m2/vuoto@-`, `m4/esposizione@-`, `oggetti/tende-a-grappolo@R29`, `scala/titolo@-` | `contesto/quota-mancante@-`, `m1/copertura@-`, `m2/vuoto@-`, `m4/esposizione@-`, `oggetti/tende-a-grappolo@R29`, `scala/tattica-non-a-1-5@-`, `scala/titolo@-` |
| rilievi comparsi | nessuno | nessuno |

A e B hanno la stessa griglia; B aggiunge solo la riga DIMENSIONI a 6 m nella recinzione, e il voto scende di 3 perché `qualita_mappe.py` ora legge una tattica a 6 m (`scala/tattica-non-a-1-5`). C è rifatta da contratto JSON (`HF-1A3-campo-mano-rossa.json`) sul modello della M7-C di ARC-07: 60 × 60 a 3 m, centurie di tende in file, piazza del comando, clan degli orchi, recinto dei worg. Il titolo cambia («griglia strategica» → «vista strategica»), e l'abbinamento si fa per codice. Il confronto cella per cella qui misura poco: la scala passa da 6 a 3 m e la griglia da 40 × 50 a 60 × 60, quindi la cella G10 di A e la G10 di C non sono lo stesso pezzo di piana. Le 1528 transizioni `V→.` sono celle che in A non esistevano; le 311 `U→.` sono le creature-segnaposto di A che in C sono diventate tende e corsie. Jaccard 0 su muri e coperture vuol dire «nessun muro nello stesso posto», cosa ovvia con un disegno nuovo.

### MAPPA 1D: Il pendio sotto le mura

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`, mappa 4 · SVG: [`svg/Hammerfist-L1-REVISED-Ultra-Clear-04-1d.svg`](svg/Hammerfist-L1-REVISED-Ultra-Clear-04-1d.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 12 × 12 | 12 × 12 | 12 × 12 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (no) |
| `@quota` · `@dislivello` | — | — | 945 · +75 m |
| voto | 97 | 97 | 98 |
| rilievi non derogati · derogati | 2 · 0 | 2 · 0 | 1 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 0 (0,0 %) | 0 (0,0 %) |
| celle cambiate, classi | 0 (0,0 %) | 0 (0,0 %) |
| Jaccard muro M · pavimento . · creature U | 1,00 · 1,00 · 1,00 | 1,00 · 1,00 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 1,00 · — · 1,00 | 1,00 · — · 1,00 |
| Jaccard blocco · percorribile | 1,00 · 1,00 | 1,00 · 1,00 |
| transizioni principali | nessuna | nessuna |
| voto | 97 → 98 (+1) | 97 → 98 (+1) |
| rilievi spariti | `contesto/quota-mancante@-` | `contesto/quota-mancante@-` |
| rilievi comparsi | nessuno | nessuno |

Griglia identica nelle tre versioni; il punto in più è `@quota 945 m` e `@dislivello +75 m`. La copia nel master DEF-1 dà gli stessi numeri (vedi sotto).

### MAPPA 2A REVISED: Fortezza Hammerfist top-down (scala piena)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md`, mappa 1 · SVG: [`svg/Hammerfist-L2-REVISED-Ultra-Clear-01-2a.svg`](svg/Hammerfist-L2-REVISED-Ultra-Clear-01-2a.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 120 × 80 | 120 × 80 | 120 × 80 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (sì) | 1,5 m (sì) |
| `@quota` · `@dislivello` | — | — | 950 · +80 m |
| voto | 92 | 93 | 100 |
| rilievi non derogati · derogati | 4 · 0 | 4 · 0 | 0 · 3 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 4206 (43,8 %) | 198 (2,1 %) |
| celle cambiate, classi | 1608 (16,8 %) | 110 (1,1 %) |
| Jaccard muro M · pavimento . · creature U | 0,63 · 0,80 · 0,15 | 0,99 · 0,98 · 0,77 |
| Jaccard copertura K · porte P · pericolo H | 0,00 · 0,41 · — | 1,00 · 1,00 · — |
| Jaccard blocco · percorribile | 0,63 · 0,85 | 0,99 · 0,99 |
| transizioni principali | `.→M` 933, `.→U` 185, `M→.` 134, `U→.` 130 | `U→.` 48, `.→M` 42, `.→U` 20 |
| voto | 92 → 100 (+8) | 93 → 100 (+7) |
| rilievi spariti | `coerenza/mura-sottili@-`, `contesto/quota-mancante@-`, `oggetti/porta-enorme@BE41`, `oggetti/porta-enorme@BE72` | `contesto/quota-mancante@-`, `oggetti/porta-enorme@BG20`, `oggetti/porta-enorme@BG41`, `oggetti/porta-enorme@BG73` |
| rilievi comparsi | nessuno | nessuno |

Qui si vedono i due rifacimenti separati. Fra A e B (geometria unica) la griglia è rigenerata da `HF-2A-fortezza.json` sulla tabella MISURE: 933 celle di pavimento diventano muro (`.→M`), perché la cinta passa da 1,5 a 6 m di spessore e i bastioni G1-G2 da 6 × 4,5 a 15 × 12 m; sparisce `coerenza/mura-sottili`. Fra B e C (quote) cambiano 198 celle: 80 di pavimento diventano scale (🪜), cioè la scarpa di 20 m fra il ripiano a +80 e quello a +100 con le sue due scale; 42 diventano muro; 48 nani lasciano il cortile interno e 20 compaiono nel cortile esterno, che è la riserva di 30 nani decisa dal DM al posto dei 50 «di riserva» nel cortile interno (le unità sono gettoni, non un nano per cella). Il Re sul cancello il Giorno 3 non si vede nella griglia: sta nella tabella POSIZIONI. Il voto sale da 93 a 100 anche per tre deroghe `oggetti/porta-enorme` (cancello, Porta Interna, porta della cittadella da 6 m).

### MAPPA 1 REVISED: Disposizione Generale Giorno 1 (0-300 m)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md`, mappa 2 · SVG: [`svg/Hammerfist-L2-REVISED-Ultra-Clear-02-1.svg`](svg/Hammerfist-L2-REVISED-Ultra-Clear-02-1.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 60 × 108 | 60 × 108 | 60 × 108 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 3 m (sì) | 3 m (sì) |
| `@quota` · `@dislivello` | — | — | 950 · +80 m |
| voto | 96 | 96 | 100 |
| rilievi non derogati · derogati | 2 · 0 | 2 · 0 | 0 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 740 (11,4 %) | 668 (10,3 %) |
| celle cambiate, classi | 108 (1,7 %) | 60 (0,9 %) |
| Jaccard muro M · pavimento . · creature U | 0,50 · 0,98 · 1,00 | 0,92 · 0,99 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 0,00 · 1,00 · — | 0,00 · 1,00 · — |
| Jaccard blocco · percorribile | 0,50 · 0,99 | 0,92 · 1,00 |
| transizioni principali | `.→K` 55, `M→.` 53 | `.→K` 55, `M→.` 5 |
| voto | 96 → 100 (+4) | 96 → 100 (+4) |
| rilievi spariti | `contesto/quota-mancante@-`, `oggetti/tende-a-grappolo@AA62` | `contesto/quota-mancante@-`, `oggetti/tende-a-grappolo@AA62` |
| rilievi comparsi | nessuno | nessuno |

Fra B e C cambiano 668 simboli ma solo 60 classi: 339 celle di prato diventano terra battuta e 195 il contrario, cioè la strada a tornanti coi cinque gomiti ridisegnata sul pendio che scende da 950 a 870 m. Le 55 celle `.→K` sono cespugli e alberi (🌿, 🌲, 🪨) del pendio; i 5 ⛺ tolti sono le tende di Grimjaw che stavano sul pendio (`oggetti/tende-a-grappolo` sparito). Fra A e B cambiano solo 72 simboli (48 di classe): il fronte allineato alla tabella MISURE e la riga DIMENSIONI a 3 m dentro la griglia, che porta la scala letta da 1,5 a 3 m senza toccare il voto. Su A→C la quota di classi cambiate resta all'1,7 % perché il grosso della mappa è pendio, e il pendio resta pendio.

### MAPPA 2B-CORRETTA REVISED: Attacco del Drago sui Bastioni

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md`, mappa 3 · SVG: [`svg/Hammerfist-L2-REVISED-Ultra-Clear-03-2b-corretta.svg`](svg/Hammerfist-L2-REVISED-Ultra-Clear-03-2b-corretta.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 40 × 26 | 40 × 26 | 40 × 26 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (sì) | 1,5 m (sì) |
| `@quota` · `@dislivello` | — | — | 965 · +15 m |
| voto | 78 | 93 | 94 |
| rilievi non derogati · derogati | 6 · 0 | 4 · 0 | 3 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 1031 (99,1 %) | 0 (0,0 %) |
| celle cambiate, classi | 248 (23,8 %) | 0 (0,0 %) |
| Jaccard muro M · pavimento . · creature U | 0,00 · 0,76 · 0,02 | — · 1,00 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 0,00 · 0,00 · 0,00 | 1,00 · — · 1,00 |
| Jaccard blocco · percorribile | 0,00 · 0,98 | — · 1,00 |
| transizioni principali | `.→U` 50, `H→.` 46, `.→H` 43, `.→K` 30 | nessuna |
| voto | 78 → 94 (+16) | 93 → 94 (+1) |
| rilievi spariti | `coerenza/mura-sottili@-`, `contesto/quota-mancante@-`, `posa/nel-muro@W15` | `contesto/quota-mancante@-` |
| rilievi comparsi | nessuno | nessuno |

Il rifacimento vero è fra A e B: la 2B diventa il tratto G1-cancello-G2 della 2A, rigenerata da contratto, col sud in alto, il drago che arriva dal fossato, Fauci Enorme su 3 × 3 e nessun tunnel sul bastione (sparisce `posa/nel-muro@W15`, che valeva 12 punti). Il 99,1 % dei simboli cambia, ma le classi solo per il 23,8 %: il disegno nuovo usa altri simboli di pavimento (🟫, 🟦, 🔳) dove prima c'era 🟨. Fra B e C la griglia non cambia; il punto in più è la quota (965 m, +15 m sul cortile esterno). Il Re sul cancello il Giorno 3 e il soffio a Riflessi CD 29 (7362834a, come nella scheda del Bestiario) stanno nel testo della 2B: questo strumento non li vede.

### MAPPA H3-1 REVISED: Cortile sfondato, ultima difesa ed evacuazione

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`, mappa 1 · SVG: [`svg/Hammerfist-L3-REVISED-Ultra-Clear-01-h3-1.svg`](svg/Hammerfist-L3-REVISED-Ultra-Clear-01-h3-1.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 40 × 40 | 72 × 36 | 72 × 36 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (sì) | 1,5 m (sì) |
| `@quota` · `@dislivello` | — | — | 970 · +20 m |
| voto | 91 | 87 | 94 |
| rilievi non derogati · derogati | 5 · 0 | 7 · 0 | 3 · 3 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 2502 (86,9 %) | 170 (6,6 %) |
| celle cambiate, classi | 1900 (66,0 %) | 90 (3,5 %) |
| Jaccard muro M · pavimento . · creature U | 0,06 · 0,36 · 0,01 | 0,91 · 0,96 · 0,71 |
| Jaccard copertura K · porte P · pericolo H | 0,02 · 0,00 · 0,00 | 1,00 · 1,00 · 1,00 |
| Jaccard blocco · percorribile | 0,06 · 0,46 | 0,91 · 0,98 |
| transizioni principali | `V→.` 839, `V→M` 222, `.→M` 201, `.→U` 118 | `.→M` 34, `.→U` 32, `U→.` 16, `U→M` 8 |
| voto | 91 → 94 (+3) | 87 → 94 (+7) |
| rilievi spariti | `contesto/quota-mancante@-`, `oggetti/fuoco-enorme@R34` | `contesto/quota-mancante@-`, `oggetti/fuoco-enorme@AE21`, `oggetti/fuoco-enorme@AM21`, `oggetti/porta-enorme@AI03` |
| rilievi comparsi | nessuno | nessuno |

Fra A e B la H3-1 diventa il cortile interno della 2A (colonne Y-CR, righe 18-53), da 40 × 40 a 72 × 36, rigenerata da contratto: per questo 839 celle `V→.` e 222 `V→M` sono celle che in A non c'erano, e il confronto A→C dice soprattutto che è un'altra inquadratura. B scende a 87 perché il cortile più grande porta nuovi avvisi (fuochi e porta grandi). Fra B e C cambiano 170 celle: la scarpa di 20 m con due scale e pianerottolo (76 🪜), l'orda che sale dalla scala ovest (32 `.→U`), B1/B2 a +120. Tre dei quattro rilievi spariti sono deroghe (`oggetti/fuoco-enorme` ×2, `oggetti/porta-enorme`).

### MAPPA 3Y REVISED: Il Ponte Sospeso (retroguardia)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`, mappa 2 · SVG: [`svg/Hammerfist-L3-REVISED-Ultra-Clear-02-3y.svg`](svg/Hammerfist-L3-REVISED-Ultra-Clear-02-3y.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 33 × 27 | 33 × 27 | 33 × 27 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (sì) |
| `@quota` · `@dislivello` | — | — | — |
| voto | 78 | 78 | 94 |
| rilievi non derogati · derogati | 6 · 0 | 6 · 0 | 3 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 604 (67,8 %) | 604 (67,8 %) |
| celle cambiate, classi | 80 (9,0 %) | 80 (9,0 %) |
| Jaccard muro M · pavimento . · creature U | 0,87 · 0,78 · 0,47 | 0,87 · 0,78 · 0,47 |
| Jaccard copertura K · porte P · pericolo H | 1,00 · 0,00 · 1,00 | 1,00 · 0,00 · 1,00 |
| Jaccard blocco · percorribile | 0,87 · 0,94 | 0,87 · 0,94 |
| transizioni principali | `.→M` 38, `U→.` 26, `.→U` 15, `P→.` 1 | `.→M` 38, `U→.` 26, `.→U` 15, `P→.` 1 |
| voto | 78 → 94 (+16) | 78 → 94 (+16) |
| rilievi spariti | `fazioni/a-contatto@-`, `posa/nel-muro@Q01`, `struttura/senza-anelli@-` | `fazioni/a-contatto@-`, `posa/nel-muro@Q01`, `struttura/senza-anelli@-` |
| rilievi comparsi | nessuno | nessuno |

A e B coincidono: la geometria unica non tocca il ponte. C è rifatta da contratto: quattro colonne di roccia sulle due sponde (gli anelli che mancavano, sparisce `struttura/senza-anelli`), uscita nord senza porta (sparisce `posa/nel-muro@Q01`, 12 punti), ponte di 15 m. Il 67,8 % dei simboli cambia ma le classi solo per il 9 %: 253 celle passano da 🏰 a ⛰, muro in tutti e due i casi.

### MAPPA 3Z REVISED: L'Incrocio Silenzioso (imboscata)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`, mappa 3 · SVG: [`svg/Hammerfist-L3-REVISED-Ultra-Clear-03-3z.svg`](svg/Hammerfist-L3-REVISED-Ultra-Clear-03-3z.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 33 × 33 | 33 × 33 | 33 × 33 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (sì) |
| `@quota` · `@dislivello` | — | — | — |
| voto | 43 | 43 | 98 |
| rilievi non derogati · derogati | 10 · 0 | 10 · 0 | 1 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 1074 (98,6 %) | 1074 (98,6 %) |
| celle cambiate, classi | 528 (48,5 %) | 528 (48,5 %) |
| Jaccard muro M · pavimento . · creature U | 0,49 · 0,28 · 0,11 | 0,49 · 0,28 · 0,11 |
| Jaccard copertura K · porte P · pericolo H | 0,00 · 0,00 · 0,00 | 0,00 · 0,00 · 0,00 |
| Jaccard blocco · percorribile | 0,50 · 0,52 | 0,50 · 0,52 |
| transizioni principali | `M→.` 298, `U→.` 94, `.→U` 57, `.→M` 23 | `M→.` 298, `U→.` 94, `.→U` 57, `.→M` 23 |
| voto | 43 → 98 (+55) | 43 → 98 (+55) |
| rilievi spariti | `fazioni/a-contatto@-`, `posa/nel-muro@A18`, `posa/nel-muro@AG18`, `posa/nel-muro@H06`, `posa/nel-muro@P01`, `posa/nel-muro@P33`, `posa/nel-muro@Z06`, `spazio/affollato@-`, `struttura/senza-anelli@-` | `fazioni/a-contatto@-`, `posa/nel-muro@A18`, `posa/nel-muro@AG18`, `posa/nel-muro@H06`, `posa/nel-muro@P01`, `posa/nel-muro@P33`, `posa/nel-muro@Z06`, `spazio/affollato@-`, `struttura/senza-anelli@-` |
| rilievi comparsi | nessuno | nessuno |

La mappa peggiore dell'arco, 43 in A e in B, rifatta da contratto in C (`HF-3Z-incrocio-silenzioso.json`): caverna ottagonale di ~40 m, sei tunnel senza porte, un pilastro di roccia al centro che fa l'anello, 60 veterani e 20 balestrieri ad anello, bugbear alle bocche est e ovest. Spariscono sei `posa/nel-muro` (le porte nei tunnel, 48 punti di errori del collaudo), `spazio/affollato`, `fazioni/a-contatto` e `struttura/senza-anelli`. Le 298 transizioni `M→.` sono roccia diventata caverna. Il confronto cella per cella dice che la mappa è un'altra (Jaccard sul pavimento 0,28).

### MAPPA 5 REVISED: Il Cuore della Montagna (ultima resistenza)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`, mappa 4 · SVG: [`svg/Hammerfist-L3-REVISED-Ultra-Clear-04-5.svg`](svg/Hammerfist-L3-REVISED-Ultra-Clear-04-5.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 67 × 53 | 67 × 53 | 67 × 53 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (no) |
| `@quota` · `@dislivello` | — | — | — |
| voto | 81 | 81 | 94 |
| rilievi non derogati · derogati | 8 · 0 | 8 · 0 | 3 · 2 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 52 (1,5 %) | 52 (1,5 %) |
| celle cambiate, classi | 51 (1,4 %) | 51 (1,4 %) |
| Jaccard muro M · pavimento . · creature U | 0,97 · 0,97 · 1,00 | 0,97 · 0,97 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 1,00 · 0,67 · 1,00 | 1,00 · 0,67 · 1,00 |
| Jaccard blocco · percorribile | 0,97 · 0,97 | 0,97 · 0,97 |
| transizioni principali | `.→M` 44, `M→.` 5, `P→M` 2 | `.→M` 44, `M→.` 5, `P→M` 2 |
| voto | 81 → 94 (+13) | 81 → 94 (+13) |
| rilievi spariti | `dimensioni/oltre-tavolo@-`, `fazioni/a-contatto@-`, `oggetti/porta-enorme@AE05`, `struttura/senza-anelli@-`, `struttura/un-ingresso@-` | `dimensioni/oltre-tavolo@-`, `fazioni/a-contatto@-`, `oggetti/porta-enorme@AE05`, `struttura/senza-anelli@-`, `struttura/un-ingresso@-` |
| rilievi comparsi | nessuno | nessuno |

A e B coincidono. In C cambiano 52 celle: 36 di pavimento diventano i quattro pilastri (🟪), 8 diventano muro, 5 il canale della sorgente (💧), 2 porte diventano muro. Il voto sale di 13: spariscono `struttura/senza-anelli` (i pilastri) e `fazioni/a-contatto`, e due rilievi spariscono per deroga (`dimensioni/oltre-tavolo` per la cattedrale, `oggetti/porta-enorme` per la porta di mithral da 6 m). `struttura/un-ingresso` sparisce perché la griglia di C ha due ingressi, la porta e il canale della sorgente; un secondo accesso per le creature resta una domanda aperta per il DM.

### MAPPA 4 REVISED: Battaglia Finale Terrestre (carica in discesa)

`08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`, mappa 5 · SVG: [`svg/Hammerfist-L3-REVISED-Ultra-Clear-05-4.svg`](svg/Hammerfist-L3-REVISED-Ultra-Clear-05-4.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 60 × 68 | 60 × 68 | 60 × 68 |
| scala (DIMENSIONI nella griglia) | 3 m (sì) | 3 m (sì) | 3 m (sì) |
| `@quota` · `@dislivello` | — | — | 920 · +50 m |
| voto | 85 | 85 | 100 |
| rilievi non derogati · derogati | 7 · 0 | 7 · 0 | 0 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 722 (17,7 %) | 586 (14,4 %) |
| celle cambiate, classi | 414 (10,2 %) | 366 (9,0 %) |
| Jaccard muro M · pavimento . · creature U | 0,12 · 0,89 · 1,00 | 0,13 · 0,90 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 0,00 · 1,00 · 1,00 | 0,00 · 1,00 · 1,00 |
| Jaccard blocco · percorribile | 0,12 · 0,90 | 0,13 · 0,91 |
| transizioni principali | `M→.` 406, `.→K` 6, `M→K` 2 | `M→.` 358, `.→K` 6, `M→K` 2 |
| voto | 85 → 100 (+15) | 85 → 100 (+15) |
| rilievi spariti | `contesto/quota-mancante@-`, `dimensioni/oltre-tavolo@-`, `fazioni/a-contatto@-`, `m1/copertura@-`, `m2/vuoto@-`, `m4/esposizione@-`, `scala/tattica-non-a-1-5@-` | `contesto/quota-mancante@-`, `dimensioni/oltre-tavolo@-`, `fazioni/a-contatto@-`, `m1/copertura@-`, `m2/vuoto@-`, `m4/esposizione@-`, `scala/tattica-non-a-1-5@-` |
| rilievi comparsi | nessuno | nessuno |

Fra A e B cambiano 136 simboli (il fronte allineato a 102 m e il fossato col ponte). Fra B e C il pendio sotto le mura, prima roccia, diventa prato e terra battuta: 358 `M→.`, e la strada a tornanti da 950 a ~890 m. Il voto sale da 85 a 100 senza deroghe, ma in buona parte per una riga: C dichiara `@tipo strategica`, e una vista d'insieme non riceve i controlli tattici. Così spariscono `dimensioni/oltre-tavolo`, `fazioni/a-contatto`, `scala/tattica-non-a-1-5` e gli avvisi M1/M2/M4 del collaudo (6 punti). La dichiarazione è giusta per una mappa a 3 m del campo di battaglia, ma il voto non distingue fra una mappa corretta e una mappa riclassificata.

### MAPPA 1D: Il pendio sotto le mura

`08_La Battaglia Di Hammerfist/ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md`, mappa 1 · SVG: [`svg/ARC08-DEF-1-OMBRA-SULLA-MONTAGNA-01-1d.svg`](svg/ARC08-DEF-1-OMBRA-SULLA-MONTAGNA-01-1d.svg)

| | A (d726e6a2) | B (9359a0af) | C (c6b61123) |
|---|---|---|---|
| abbinata per | titolo | titolo | — |
| quadretti | 12 × 12 | 12 × 12 | 12 × 12 |
| scala (DIMENSIONI nella griglia) | 1,5 m (no) | 1,5 m (no) | 1,5 m (no) |
| `@quota` · `@dislivello` | — | — | 945 · +75 m |
| voto | 97 | 97 | 98 |
| rilievi non derogati · derogati | 2 · 0 | 2 · 0 | 1 · 0 |

| | A→C | B→C |
|---|---|---|
| celle cambiate, simboli | 0 (0,0 %) | 0 (0,0 %) |
| celle cambiate, classi | 0 (0,0 %) | 0 (0,0 %) |
| Jaccard muro M · pavimento . · creature U | 1,00 · 1,00 · 1,00 | 1,00 · 1,00 · 1,00 |
| Jaccard copertura K · porte P · pericolo H | 1,00 · — · 1,00 | 1,00 · — · 1,00 |
| Jaccard blocco · percorribile | 1,00 · 1,00 | 1,00 · 1,00 |
| transizioni principali | nessuna | nessuna |
| voto | 97 → 98 (+1) | 97 → 98 (+1) |
| rilievi spariti | `contesto/quota-mancante@-` | `contesto/quota-mancante@-` |
| rilievi comparsi | nessuno | nessuno |

La copia della 1D nel master DEF-1 è identica a quella della L1 in tutte e tre le versioni (stessa griglia, stessi numeri). Fra B e C il master DEF-1 ha ricevuto le tre righe `@luogo`, `@quota`, `@dislivello` e la scala della 1A-3 nel testo (da 6 a 3 m).

## Cosa i numeri non dicono

- **Se la mappa gioca meglio.** Il voto misura la distanza dallo standard
  ADR-0098: spazio libero, anelli, ingressi, distanze, scala dichiarata. Non
  sa se lo scontro della 3Z è più teso, se il DM trova le cose sulla 2A più
  in fretta, se i giocatori capiscono il pendio della MAPPA 4. Lo dice solo il
  tavolo (skill `rumblingstone-playtest`), e nessuna di queste mappe è stata
  giocata dopo il rifacimento.
- **La coerenza col canone.** Le decisioni del DM stanno quasi tutte nel
  testo: il Re sul cancello il Giorno 3 è una riga della tabella POSIZIONI
  della 2A e della 2B, il soffio a Riflessi CD 29 è nel testo della 2B, i 300
  nani con 30 di riserva sono in `ARC08-01`, `ARC08-18` e `ARC08-19`. Nella
  griglia la riserva si vede (nani spostati dal cortile interno a quello
  esterno nella 2A), ma il numero di gettoni non è il numero di nani. Che la
  2A e la 2B siano lo stesso tratto di mura, che la H3-1 sia il cortile della
  2A, che le quote 870/950/970/990 tornino fra le mappe: questo strumento non
  lo controlla. Il controllo `contesto/quote-discordi` di `qualita_mappe.py`
  guarda solo le mappe con lo stesso `@luogo`.
- **Le deroghe pesano come correzioni.** Un rilievo derogato esce dal voto
  come uno corretto. Dieci dei rilievi spariti sono deroghe motivate; la
  MAPPA 4 guadagna una parte dei suoi 15 punti dichiarandosi `@tipo
  strategica`, che spegne i controlli tattici. Le deroghe sono legittime e
  hanno il loro motivo scritto nella griglia, ma il voto alto di quelle mappe
  vuol dire «conforme o dichiarata eccezione», e la tabella lo tiene separato.
- **Le celle cambiate non sono lavoro né qualità.** Il 99 % dei simboli della
  2B cambia fra A e B, ma le classi cambiano per il 24 %: il disegno nuovo usa
  altri simboli di pavimento. Il 67,8 % dei simboli della 3Y cambia, e 253 di
  quelle celle sono muro diventato roccia, sempre classe M. Le classi sono la
  misura che conta per il gioco; i simboli dicono quanto è cambiata la resa.
- **Quando cambia la scala, le celle non si corrispondono.** La 1A-3 passa da
  6 a 3 m per quadretto e da 40 × 50 a 60 × 60; la H3-1 da 40 × 40 a 72 × 36
  con un'altra inquadratura. Il confronto allinea le celle per indice, dall'angolo
  in alto a sinistra: per queste due mappe percentuali e Jaccard
  misurano un disegno contro un altro, non la stessa piana prima e dopo.
- **L'NCD** (nel JSON, distanza di compressione con lzma) non scende a 0 per
  due griglie identiche: sulla 1A-2 vale 0,18 a griglia invariata, per il
  costo fisso del compressore su testi corti. Va letta solo per confrontare
  mappe della stessa taglia, e dipende dalla versione di liblzma.
- **I `@collega` verso altri file** si risolvono sul file del repo di oggi,
  non sulla sua versione storica. Nessuna mappa di ARC-08 ne ha uno verso un
  altro file, quindi qui non cambia niente.

## Come si rifà

```bash
python3 scripts/confronta_mappe.py --versioni A=d726e6a2 B=9359a0af C=c6b61123 --base C \
    --estrai /tmp/confronto-estratti --out plans/esperimenti/confronto-mappe-arc08-2026-10-22 \
    "08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md" \
    "08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md" \
    "08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md" \
    "08_La Battaglia Di Hammerfist/ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md"
```

Due esecuzioni danno gli stessi byte, in `confronto.json` e negli SVG
(provato qui, e coperto da `scripts/tests/test_confronta_mappe.py`). Le
versioni nel JSON si riconoscono dal blob git di ogni file, che non dipende
da dove si estrae né da quando. Nessuna mappa e nessun master sono stati
toccati.

