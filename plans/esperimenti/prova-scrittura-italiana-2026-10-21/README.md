# Prova: scrittura-italiana come eccezione su ARC-07 DEF-4 e DEF-5

Prova del 2026-10-21 per [ADR-0097](../../adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md).

- `CAMPIONE.json`: i 35 box di DEF-4 (32) e DEF-5 (3) sopra le 25 parole,
  congelati su `origin/main` (1553869) prima di riscrivere, seme 20261021. Gli
  8 box già votati al giro 3 (`giro3-arc07-2026-10-19/misure/CONGELATI.json`)
  restano fuori.
- `RISCRITTURE.json`: per ogni box il vecchio, il nuovo, il verdetto della
  misura e la nota di chi l'ha riscritto. Due agenti, stesse norme, con
  `references/scrittura-italiana-eccezione.md`.
- `SCHEDA-CIECO.md`: le coppie per il DM.
- `ESITO.md`: i voti del DM, la chiave sciolta e l'esito.

## Le misure

| | prima | dopo |
|---|---|---|
| box cambiati | | 13 su 35 (22 identici) |
| `verdetto_misurato` | | 13 «indecisa»: stessi dettagli sensoriali, nessun monologo spezzato |
| `ciclo_prosa confronta --rif origin/main` | | ✓ su DEF-4 e DEF-5, nessun peggioramento |
| Gulpease dei box di DEF-4 (`misura_craft --stile`) | 69,8 | 70,8 |
| Gulpease dei box di DEF-5 | 69,8 | 69,8 |

Le riscritture sono ritocchi da revisione: frasi lunghe spezzate in due,
soggetti ripetuti, pronomi ambigui sciolti. La misura non decide nessuna
coppia, quindi le 13 vanno tutte al cieco. Soglia riproporzionata di ADR-0093:
**10 su 13**.

## Due difetti trovati, corretti dopo il cieco

Il 2026-10-21 il DM ha lasciato la scelta: il box 24 dice «Dove il drago
passa basso» (il nome resta al momento in cui il DM lo rivela), il box 26
dice «corrono righe di rune», così «L'ultima riga» ha le sue sorelle.
I due difetti com'erano:

- DEF-4, box 24 del campione: «gli cola dalle fauci» e «dove passa basso» non
  hanno un nome maschile a cui riferirsi. Si corregge nominando il drago nel
  box, ed è il DM a decidere quando rivelarlo.
- DEF-4, box 26: «una riga di rune» e poi «L'ultima riga» si contraddicono. La
  correzione cambia un dettaglio della Catena.
