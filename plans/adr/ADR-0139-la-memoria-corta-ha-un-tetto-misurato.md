# ADR-0139 — La memoria corta ha un tetto misurato

**Stato**: accettata (2026-11-19)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19, thread «Riportare la memoria sotto il limite»: «controlla perché la memoria del progetto è oltre il limite, non avevamo implementato la memoria storica per risolvere questi problemi? […] fixare questi problemi». Sulla card dello stesso giorno il DM ha scelto «Script + routine + coordinatore».
**Rapporti**: completa [ADR-0127](ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md), [ADR-0137](ADR-0137-la-memoria-storica-si-scrive-a-ogni-blocco-di-lavoro-non-solo-al-merge.md) e [ADR-0138](ADR-0138-la-coda-della-memoria-storica-ha-un-cancello.md), che dicono dove va la storia ma non quando la memoria corta deve scendere.

## Contesto

Il 2026-11-19 l'indice della memoria delle sessioni (`MEMORY.md`) era a
16.878 byte, oltre il limite di 16.384 oltre cui la piattaforma lo taglia.
Il 2026-11-12 era stato ridotto a circa 8 KB: +8,8 KB in sette giorni.

Perché la memoria storica non l'ha evitato: ADR-0127 e ADR-0137 obbligano ad
**archiviare prima di togliere** una riga, ma nessuna regola obbliga a
toglierla e nessun controllo misura i byte. `--confronta-memoria` guarda i
riferimenti (PR, ADR, SHA, percorsi), non la dimensione; la piega del lunedì
porta la coda nel repo ma non accorcia la memoria. In pratica ogni thread
chiudeva aggiungendo «#N unita il …, merge SHA, MS-N» invece di togliere la
riga del suo stato aperto. Al 19/11 la sezione «PR aperte e ordine» datata
13/11 elencava solo PR già unite, e su GitHub ne restavano aperte due.

Misura prima del taglio: 18 PR citate nella memoria hanno tutte una voce in
`plans/MEMORIA-STORICA.md`; `--confronta-memoria` segnalava una sola riga
dell'indice (Kaggle, percorsi in `/mnt`). La memoria è stata riscritta a
11.255 byte senza perdere fatti; ciò che non aveva un posto è nella coda.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **`memoria_storica.py --tetto-memoria DIR`, lanciato dalla routine del lunedì e dal coordinatore dopo ogni modifica dell'indice** (proposta) | esce 1, mostra le cinque righe più lunghe; stdlib, stesso script | va lanciato: la memoria non è nel repo e la CI non la vede |
| Solo la regola «chi chiude toglie la sua riga» in testa all'indice | nessun codice | è la forma di ADR-0127 che non ha retto |
| Solo nella routine del lunedì | un solo punto | a +1,2 KB al giorno, sei giorni bastano a passare il limite |

## Decisione

- Tetto di `MEMORY.md`: **12 KB** (12.288 byte), 4 KB di margine al limite.
- `python3 scripts/memoria_storica.py --tetto-memoria DIR [--tetto N] [--json]`:
  esce 1 sopra il tetto, dice se è oltre il limite e mostra le righe più
  lunghe; esce 0 sotto; 2 se manca `MEMORY.md`.
- Lo lanciano la routine del lunedì (con `--confronta-memoria`) e il
  coordinatore dopo ogni modifica dell'indice. Sopra il tetto si tolgono
  prima le righe di cronologia (PR unite, lavori chiusi), dopo averle
  archiviate come dice ADR-0127.
- In testa all'indice la regola: chi chiude un lavoro toglie la sua riga di
  stato, non ne aggiunge una «unita il …».

## Conseguenze

- Si vede il problema prima del taglio, non dopo.
- **Cosa non vede.** Non parte da solo: se nessuno lo lancia non boccia
  niente. Misura solo l'indice, non le note (che hanno il loro limite di
  4 KB ciascuna, non controllato qui). Non sa se una riga è cronologia o
  stato aperto: lo decide chi accorcia.

## Da rivedere se

- l'indice supera il tetto due volte fra un lunedì e l'altro (allora il
  lancio del coordinatore non basta e serve un controllo della piattaforma
  alla scrittura della memoria);
- il limite della piattaforma cambia.
