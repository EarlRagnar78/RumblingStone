# Giro del 2026-10-19 su ARC-08, dal 3B alla Cerimonia

Il primo giro fatto con lo standard di ADR-0095 (A4 di
[MASTER-DEF](../../PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md)): quattro letture a
freddo una alla volta (D8), correzione con quattro esiti, verifica di un agente
nuovo, seconda passata.

**Cosa è stato letto.** La parte che i PG giocano in ogni caso, qualunque sia
la scelta sul flashback dei pregen (D4): l'Incontro 3B, la Sessione 4,
l'epilogo e la Cerimonia, con la mappa L3. Le copie a freddo stavano in
`/mnt/project-files/giro-arc08-2026-10-19/fonti/`:

| Copia | File del repo |
|---|---|
| A | `ARC08-01-GUIDA-DM.md`, righe 147-622 (PNG chiave) e 2504-3208 (3B e Sessione 4) |
| B | `hammerfist_encounters-…-final.md`, righe 821-1357 (3B, 4A, 4B) |
| C · D · E | `ARC08-10-ESITI-E-CONTINGENZE.md` · `ARC08-11-PONTE-ARRIVO.md` · `Cerimonia-delle-100-Asce.md` |
| F | `Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`, coi PNG resi e il rapporto di `collaudo_mappe.py` |
| G | `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`, senza il blocco `storico` |

I numeri si sono verificati sulla copia locale dell'SRD 3.5 (D8) e sul canone
giocato del ramo `campaign-group-rumblingstone`.

## Le letture

| Lettore | 🔴 | 🟠 | 🟡 |
|---|---:|---:|---:|
| Developer | 3 | 24 | 17 |
| Playtester | 5 | 14 | 12 |
| DM a freddo | 3 | 14 | 13 |
| Collaudatore delle mappe | 2 | 9 | 13 |
| **Totale** | **13** | **61** | **55** |

Il difetto che tutti e quattro hanno visto è lo stesso. Lo scontro con Fauci di
Palude esiste in versioni incompatibili: in A e B il drago fugge al round 5 e
lo combattono i PNG, mentre i PG guardano; in F si schianta ai round 18-20 e
duella coi PG. I pf di partenza erano 180, 220 o 232 su 312, contro i 337 della
scheda. La Mappa 5 aveva la riga dei rinforzi tutta muro e l'altare in
muratura piena, quindi le ondate non entravano e i PG apparivano chiusi.

## Correzione, verifica, seconda passata

| | |
|---|---|
| 🔴 e 🟠 dopo aver unito i doppi | 74 |
| Correzione | 37 corretti · 35 al DM · 1 respinto · 1 residuo |
| Verifica (agente nuovo) | 20 chiusi · 15 parziali · 0 aperti · 39 in attesa del DM · nuovi 🟠 2, 🟡 10 |
| Seconda passata | parziali: 12 chiusi, 1 al DM, 2 residui · nuovi: 11 corretti, 1 al DM |

Nei casi al DM la parte vera in ogni versione è già corretta: il denominatore
337, la tempesta secondo l'SRD, *invocare il fulmine*, i rimandi al Bestiario.
L'Atlante delle mappe di ARC-08 è stato allineato nella seconda passata, perché
il verificatore l'aveva trovato ancora vecchio. È il difetto che ADR-0095 mette
nel passo 4. La scala della Mappa 4 negli SVG è passata a 3 m per quadretto con
la riga di dimensioni della griglia, senza toccare il renderer.

Le dodici decisioni sono nel piano, D9-D20. Restano due residui: il tempo di
lettura al tavolo, che si misura solo con un dry-run, e la tattica degli
«ultimi fedeli», che dipende dalla versione di Fauci.

## Cancelli dopo la seconda passata

`validate_maps` ✓ (53 SVG) · `validate_modules` ✓ · `conformita_statblocchi
--master` su A, B, G: 0 conti sbagliati · `misura_craft --box`: 0 box oltre le
12 righe in ARC-08 · `collaudo_mappe` sulla L3 da 8 errori e 15 avvisi a 7 e 13.
I sette errori sono porte fuori perimetro nelle mappe H3-1, 3Y e 3Z, che questo
giro non ha letto.
