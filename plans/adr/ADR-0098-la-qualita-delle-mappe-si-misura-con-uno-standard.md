# ADR-0098 — La qualità delle mappe si misura con uno standard scritto

**Stato**: accettata il 2026-10-22, come regola per le mappe nuove o rifatte
**Data**: 2026-10-22
**Decisione-fonte**: il DM, il 2026-10-22 («rifai tutte le mappe necessarie per essere quanto più plausibili e vicine sia come scale che posizionamento […] misurando coerenza e giocabilità e il rispetto dei parametri usati dalle migliori mappe fantasy per giochi di ruolo. Cerca in rete se ci sono altri metodi o altri parametri per migliorare le mappe e se possibile integrali nel repo in modo che diventino standard»)

## Contesto

Il collaudo (ADR-0082) dice se una mappa si gioca: la porta sta nel muro, la
scala ha la gemella, il nemico arriva ai PG. Non dice se è plausibile né se è
buona. L'audit del 2026-10-21 ha trovato tende a un palo larghe 18 m, fuochi
di 13,5 m sotto i teli, accampamenti fatti di muratura piena, scale scritte solo
fuori dal recinto: niente di questo era un errore per il collaudo. Il 2026-10-21
sono state rifatte 15 mappe a mano, con le misure prese da fonti reali, ma le
regole stavano in due documenti d'esperimento e in nessuno strumento.

In rete non esiste uno standard numerico unico per le battlemap. Esistono
principi di level design con nomi e fonti (Jaquays, Dormans, la Five Room
Dungeon), metriche della ricerca sulla generazione procedurale (Smith e
Whitehead, Liapis e altri, Mawhorter) e le misure dei prodotti che il tavolo
usa (Flip-Mat). Le fonti stanno in `standard-qualita-mappe.md`.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Uno standard scritto con uno strumento nuovo (`qualita_mappe.py`) sopra il collaudo, errori solo per i fatti, avvisi con fonte e deroga, voto da 0 a 100** | le regole stanno in un posto; la classifica dice cosa rifare per primo; il collaudo resta il gate di «si gioca?» | due comandi invece di uno; le soglie senza fonte numerica sono di casa e vanno ricalibrate |
| Aggiungere i controlli a `collaudo_mappe.py` | un comando solo, una sola distanza | il collaudo ha già 25 codici e un gate a tetto (lotto V4); mescolare «si gioca» e «è buona» rende la distanza illeggibile |
| Solo un documento, senza strumento | nessun codice da mantenere | è quello che c'era già (audit e ricerca del 2026-10-21) e non ha impedito i difetti |
| Errori bloccanti in CI per tutte le soglie | le mappe nuove non scendono | la CI diventa rossa sullo storico (81 avvisi sul corpus il 2026-10-22); soglie senza calibrazione non possono bloccare |

## Decisione

**Ogni mappa tattica nuova o rifatta si prepara nell'ordine funzione, flusso,
scala, tattica, ed esce da `qualita_mappe.py` senza errori e con gli avvisi
corretti o derogati per scritto.**

1. Lo standard è `skills/rumblingstone-mapmaking/references/standard-qualita-mappe.md`:
   le fonti, il giro di preparazione, le regole misurabili con soglia e fonte,
   la lista dei controlli a vista.
2. `scripts/qualita_mappe.py` misura il corpus del collaudo. Tre soli errori,
   tutti fatti: l'intestazione che dice una misura diversa dalla griglia
   (`scala/dichiarata`), una direttiva che punta fuori griglia
   (`direttive/fuori-griglia`) e una quota che non è un numero
   (`contesto/quota-illeggibile`). Il resto sono avvisi con `@deroga`.
3. Il voto parte da 100 e somma anche i rilievi del collaudo. Le bande (buona da
   90, da ritoccare da 75, da rivedere da 55) ordinano il lavoro; non sono un
   gate.
4. In CI il rapporto gira non bloccante, accanto a quello del collaudo.
5. Ogni mappa all'aperto, di abitato o strategica dichiara `@quota` e
   `@dislivello` (e `@luogo` se un'altra mappa mostra lo stesso punto). Il DM
   l'ha chiesto lo stesso giorno, per Hammerfist: «una quota e distanze
   realistiche». Lo strumento dà errore solo per un valore che non è un numero;
   la quota mancante e due quote diverse per lo stesso luogo sono avvisi, così
   lo storico non diventa rosso.
6. La classifica del 2026-10-22 sta in
   `plans/esperimenti/mappe-qualita-2026-10-22/CLASSIFICA.md`, le opzioni per il
   fiume fra Channathgate e Rethmar in `OPZIONI-FIUME.md` accanto.

## Conseguenze

- Chi disegna ha un elenco di regole con le misure, invece di due ricerche da
  rileggere; il collaudatore a freddo ha la lista dei controlli a vista.
- Le mappe di ARC-07 e ARC-09 rifatte il 2026-10-21 escono tutte fra 94 e 100,
  e la classifica mette in cima le mappe che l'audit aveva già indicato.
- Si paga: un secondo strumento da mantenere, che dipende dal collaudo (classi
  `Griglia` e `Collaudo`); soglie scelte sul corpus dove le fonti non danno un
  numero (18 simboli, 30% di icone, 150 celle per creatura); un voto che un
  lettore frettoloso può prendere per un giudizio sulla scena.
- Una mappa d'esercito o una vista strategica scritta come tattica perde punti
  finché non dichiara `@tipo strategica`: è voluto.

**Da rivedere se**: il DM boccia una mappa che lo strumento giudica buona, o
promuove una che giudica da rifare (allora le soglie sono sbagliate); oppure,
dopo un arco giocato con mappe nuove, il playtest dice che le soglie sulla
distanza fra le fazioni o sullo spazio per creatura non corrispondono ai round
veri al tavolo.
