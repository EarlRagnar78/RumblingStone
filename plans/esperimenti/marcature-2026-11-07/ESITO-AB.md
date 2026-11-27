# Prova A/B del blocco «Vincoli sui fatti» (ADR-0109) — 2026-11-07

Scheda 7 = B del DM: 30 consegne con fatti che nel repo non ci sono
(`consegne.json`, una trappola ciascuna), ogni consegna eseguita due volte da
un agente con la skill di main (vecchia) e con la skill di questo ramo
(nuova). Le due risposte sono state date a un giudice che non sapeva quale
fosse quale (file `Cnn-p` e `Cnn-q`, lettera assegnata a giro). Giudizi
completi in `giudizi-ab.json`.

| Misura (somma sulle 30 consegne) | Vecchia | Nuova |
|---|---:|---:|
| Fatti inventati senza marca | 127 | 73 |
| Marche in tutto | 188 | 151 |
| Marche con domanda e base (forma ADR-0109) | 42 | 124 |
| Risposte senza nessun fatto inventato non marcato | 17 | 19 |

Per consegna: la nuova inventa meno in 11, di più in 4, pari in 15. Test del
segno sulle 15 non pari: p = 0,059 a una coda, 0,12 a due. Sul totale la
riduzione è del 43%, ma con 30 consegne non è una prova forte per singola
consegna.

Dove la nuova fa peggio:
- **npc-villain-boosting** C10 (0 → 6) e C11 (1 → 7): numeri dello statblock
  (caratteristiche, pf, talenti, GS) scritti senza marca né conto. Nella stessa
  skill C12 migliora molto (15 → 1). Il blocco vincoli non dice che un numero
  di statblock fatto a mano è un fatto da marcare o da derivare dall'SRD.
- **rumblingstone-module-standard** C16 (15 → 22): locanda inventata, la nuova
  marca di più (20) ma lascia anche più dettagli nudi.
- **rumblingstone-playtest** C24 (0 → 1): un dettaglio del cancello.

Lettura: il blocco funziona sulle domande (marche ben formate da 42 a 124) e
riduce gli inventati, ma ha un buco preciso sugli statblock potenziati.
