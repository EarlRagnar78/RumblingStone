# Prova di ADR-0107 — chi si incontra sta nel capitolo (2026-11-03)

Il DM (Jfs, 2026-11-03): *«facciamo la prova di cosa misura e cosa dice di
migliorare, e misurare il miglioramento globale se c'è, e poi una verifica del
DM e una del playtester se verifica o un miglioramento»*.

## Cosa si è provato

`"schede": "entrambe"` (il valore e il tema della PR #305) più
`"chi_si_incontra": true` (questa PR, `scripts/dmcore/chi_si_incontra.py`).
Prima di stampare, il generatore:

- sposta il riquadro della persona, con la tattica, subito dopo la sua scheda
  d'entrata e il ritratto. Se il riquadro sta in un altro master, lo copia;
- porta la scheda nella scena dove la riga **In scena … Chi:** nomina la
  persona. Se il capitolo non ha quelle righe e cita la persona almeno 10
  volte, la porta in testa al capitolo;
- copia la pianta e la legenda della mappa dopo il paragrafo «**Mappa …**»
  della scena, quando la mappa è stampata lontano (l'Appendice D, a 40 pagine
  di distanza) o non è stampata affatto;
- lascia intatte regia e cassetta. L'appendice in fondo al volume resta.

Il master non cambia: cambia solo quello che va in stampa.

## La misura, prima e dopo (`misura.json`)

`python3 scripts/misura_standard_tavolo.py` contro lo stesso comando con
`--prova`, su tutti e dieci i booklet del DM.

| | prima | dopo |
|---|---|---|
| coppie capitolo × persona | 145 | 151 |
| complete (tutte e sei le voci) | 3 | 3 |
| con almeno 5 voci su 6 | 15 | 17 |
| riquadro stampato nel capitolo | 0 | 25 |
| «Chi è» | 4% | 4% |
| «Vuole» | 33% | 40% |
| mappa vicina alla scena (scontri) | 4 su 41 | 8 su 41 |
| mappa nel capitolo ma lontana | 3 | 0 |

Il miglioramento sta tutto in ARC-07. Palio, Giardino, Drappo e Abbazia non
cambiano di un punto: lì le persone sono descritte in prosa, non hanno una
scheda d'entrata, e le mappe non hanno un codice da cui ritrovarle. Il
generatore sposta solo ciò che esiste già.

Le «complete» restano 3 perché la riga **Chi è** non esiste quasi da nessuna
parte. La prima versione della prova la ricavava dal titolo («il generale»):
la lettura del DM l'ha bocciata perché ripeteva il titolo, ed è stata tolta.
Una riga vera va scritta a mano nel master.

### Quanto si fida la misura

In questa prova la misura è stata corretta tre volte, e ogni correzione l'ha
resa più severa:

1. una riga in grassetto che nomina soltanto la persona («**Vuole** … Balvar»)
   non apre più il suo blocco;
2. il blocco di una persona finisce alla scheda d'entrata della persona dopo.
   Prima la sezione «Chi è» di Balvar veniva contata anche per Zog'tar;
3. una mappa stampata nel capitolo ma 40 pagine dopo la scena conta come
   `lontana`, non come `qui`.

Per questo la tabella dice «complete 3» dove la PR #306 diceva 6: le altre 3
erano falsi positivi. La misura resta un indicatore, e il giudizio sta alle
letture qui sotto.

## Lettura alla cieca: DM e playtester

Il booklet della serata del 2026-09-25 è stato stampato in due versioni:
quella di oggi (157 pagine) e quella con la prova (174 pagine nella versione
letta). Le due versioni, convertite in testo con i numeri di pagina, sono
andate a due lettori senza dire quale fosse la nuova: un DM e un playtester.
Non è un cieco vero, perché la versione nuova si riconosce dalla forma; i due
lettori però non sapevano quale delle due fosse.

**Il DM sceglie la nuova.** Per la tenda di Zog'tar:

| | nuova | vecchia |
|---|---|---|
| numeri (CA, pf, attacchi) | +1 pagina | +31 (CA e pf), +56 (attacchi) |
| mappa M7-C | +3 | +37 |

**Il playtester sceglie la nuova.** Con la nuova versione i round di Zog'tar
e di Skullcrusher si giocano senza sfogliare; con la vecchia nessuno dei due
round parte, perché i numeri stanno in appendice dietro due rimandi.

I difetti che hanno trovato nella versione nuova, e cosa ne è stato:

| difetto | stato |
|---|---|
| righe «Chi è» che ripetono il titolo | tolte: il generatore non inventa più la riga |
| la copia di M7-B messa nell'introduzione e non nella Scena 11 | corretto: il rimando «> **Mappa M7-B.**» dentro una citazione ora vale come punto della scena |
| M7-H copiata due volte nella stessa appendice | corretto: se la pianta sta già prima del punto, non si copia |
| «contro Zog'tar in DEF-4» nella scheda di Durik portata da un altro master | corretto: i rimandi si traducono anche nel testo portato |
| «immagine mancante: ../plans/…» | corretto: entrano solo piante che esistono, e non dai piani |
| la fascia TATTICHE di Zog'tar stampata sopra il piede di pagina (p. 108) | **aperto**: il tema di «entrambe» (PR #305) sbaglia lo spazio che resta quando sopra c'è una tabella larga in float. Va fatto un parametro nel tema dopo il merge della #305, per non litigare sullo stesso file |
| 13-17 pagine in più (157 → 172) | è il costo dichiarato dall'ADR |
| doppioni dove una persona compare in più capitoli (Durik tre volte) | voluto dall'ADR, ma al DM pesa: da decidere |

Hanno trovato anche cose che c'erano già, in tutte e due le versioni, e che
riguardano il contenuto:

- la Scena 8 (il combattimento nella tenda) sta 6-11 pagine dopo la scheda di
  Zog'tar della Scena 7;
- le mini-schede di guardie e sacerdote e un ordine d'iniziativa della tenda
  non ci sono vicino;
- la M7-C non torna con il testo: Zog'tar Grande a P14 si sovrappone alla
  guardia, il testo nomina tre pali e la mappa ne mostra uno, e in Appendice D
  c'è un'altra M7-C con il seggio a X22;
- nella scheda di Zog'tar mancano la scurovisione e la frequenza di Presenza
  Minacciosa;
- per Skullcrusher Vecchio, Concentrazione CD 21 e corrompere l'acqua CD 25
  sono i valori dell'Adulto (per il Vecchio sono 22 e 26). Inoltre entra a
  45 m di quota con un soffio a linea di 30 m;
- nel testo stampato restano note di lavoro: «[INFERRED…]» e «va riscontrato
  su d20srd.org».

Queste correzioni non si fanno con il generatore: vanno riportate nel master
ARC-07 DEF-4, con le decisioni del DM.

## Cosa dice di migliorare

1. **Il generatore va acceso** sui booklet di ARC-07 della serata
   (`"schede": "entrambe", "chi_si_incontra": true`), dopo il merge della
   #305 e la correzione del tema.
2. **«Chi è» va scritto nel master**, una riga col ruolo nella storia, nelle
   25 schede d'entrata che esistono.
3. **Fuori da ARC-07 servono le schede d'entrata.** Palio, Giardino, Drappo e
   Abbazia hanno 51 coppie capitolo × persona senza nessuna scheda e 24 scontri
   senza mappa codificata. È lavoro di scrittura, un modulo alla volta.
4. **Le correzioni di contenuto** della lista qui sopra vanno al master DEF-4.
