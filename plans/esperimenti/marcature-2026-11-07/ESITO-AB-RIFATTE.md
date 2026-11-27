# Prova A/B: le 3 consegne peggiorate, rifatte con la skill di main (2026-11-07)

Seguito di [ESITO-AB.md](ESITO-AB.md). Con il blocco «Vincoli sui fatti» (ADR-0109) tre consegne
erano andate peggio: C10 e C11 (npc-villain-boosting) e C16 (rumblingstone-module-standard).
Dopo la card del DM «Adotta e correggi gli statblock», la skill di main dice che uno statblock
potenziato si costruisce dall'SRD con il conto, e che un numero senza conto è INFERRED.

Le tre consegne sono state rifatte da un agente con la skill di main. Un giudice cieco ha letto
nove risposte, tre per consegna: la rifatta e le due della prima prova (`p` e `q`). Le lettere
x/y/z sono state assegnate a mano, diverse per ogni consegna. Lo stesso giudice ha contato anche
le risposte vecchie, così la deriva di un giudice nuovo vale per tutte e tre. I conti sono in
`giudizi-ab-rifatte.json`, con la chiave delle lettere.

| Consegna | Inventati senza marca: rifatta | vecchia p | vecchia q | Marche con domanda e base: rifatta | p | q |
|---|---:|---:|---:|---:|---:|---:|
| C10 | 0 | 5 | 4 | 7 | 3 | 0 |
| C11 | 0 | 0 | 2 | 10 | 0 | 3 |
| C16 | 2 | 10 | 6 | 27 | 20 | 0 |
| **Totale** | **2** | **15** | **12** | **44** | **23** | **3** |

Tutte e nove le risposte dicono che il soggetto della consegna non esiste nel repo.

Lettura:
- Sulle tre consegne peggiorate la rifatta inventa meno di tutte e due le versioni precedenti,
  e quasi tutte le sue marche hanno la domanda e la base.
- Rifatto con la stessa misura, il giudice dà numeri diversi dalla prima prova: per C10, 6
  inventati della «nuova» diventano 5 o 4. La differenza fra i giudici è di qualche unità per
  consegna, molto meno del salto fra la rifatta e le vecchie.
- Sono 3 consegne, scelte proprio perché erano peggiorate: non è una prova sul totale delle 30.
  Il buco degli statblock potenziati risulta chiuso su questi casi, non dimostrato in generale.
