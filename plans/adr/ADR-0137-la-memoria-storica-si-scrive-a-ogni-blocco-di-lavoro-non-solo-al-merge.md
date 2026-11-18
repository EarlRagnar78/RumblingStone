# ADR-0137 — La memoria storica si scrive a ogni blocco di lavoro, non solo al merge

**Stato**: accettata (2026-11-18): punti 1-2 in questa PR; punto 3 scelto dal DM sulla card del 2026-11-18 (coda per thread + routine del lunedì, la consigliata); punto 4 lo scrive il coordinatore nelle istruzioni del progetto
**Data**: 2026-11-18
**Decisione-fonte**: il DM (Jfs), 2026-11-18, thread «Rendere obbligatoria la memoria storica»: «controlla se la memoria storica obbligatoria su tutte le chat è attiva, quale è lo stato attuale implementato e cosa fare per migliorarla ed utilizzarla per tutti i threads aperti e quelli nuovi così non si perdono dati». Termine di confronto: le regole «MEMORIA STORICA DEL PROGETTO (obbligatoria)» del suo progetto di dottorato, incollate nel thread.
**Rapporti**: estende [ADR-0127](ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md) (file storico, addendum in CI). Non cambia il formato delle voci né il cancello di [ADR-0009](ADR-0009-gate-tracciatura-changelog-adr.md).

## Contesto

Misure sul main c9159831 (2026-11-18), dal 2026-11-12 (nascita di ADR-0127):

| Che cosa | Misura | Imposto da |
|---|---|---|
| PR unite con riga nel changelog dei piani e voce MS | 88 su 90 (le 2 senza, #387 e #389, toccano solo `docs/`, che non è strutturale) | CI, `check_plans_discipline.py` |
| Voci MS con numeri consecutivi e campi completi | 165 su 165 | CI, `memoria_storica.py --check` |
| Voci dal 2026-11-12 col campo PR «—» | 82 su 98: la voce si scrive prima che la PR abbia un numero | nessuno |
| PR unite che `--pr N` ritrovava | **37 su 90** (contando anche le voci che le citano soltanto nel testo) | nessuno |
| Voci dal 2026-11-12 nate da altro che una riga del changelog (riga tolta dalla memoria, scelta su card, esito di un thread senza PR) | **0 su 98** | solo una regola scritta |
| Note della memoria delle sessioni citate nel file storico | 41 su 77 | nessuno |
| Righe della memoria delle sessioni con PR, ADR, SHA o percorsi che il repo non ha | 84 su 408 controllabili (311 righe sono prosa e non si controllano così); 21 di queste rimandano solo a `/mnt/project-files/` | nessuno |

Esempi di fatti decisi su card e oggi solo nella memoria delle sessioni:
il rilascio 1.1.0 dopo le promozioni del 22-24/11 con card prima del tag,
Lychee «solo se il DM la chiede». Nessuna stringa nel repo li contiene.

Quindi l'obbligo vale davvero solo dove passa una PR col changelog. Ciò che
nasce in un thread e non diventa PR (decisioni su card, file solo nella
cartella condivisa, righe tolte dalla memoria, thread risolti) dipende dalla
disciplina della singola sessione, e la misura dice che quella disciplina,
in sei giorni, non ha prodotto nessuna voce.

### Confronto con le regole del progetto di dottorato

| Regola del phd | Qui | Esito |
|---|---|---|
| 1. Leggere la memoria a inizio conversazione | l'indice della memoria entra da solo in ogni sessione; `AGENTS.md` manda a `MEMORIA.md` | coperto (dall'ambiente, non da un cancello) |
| 2. Cercare prima di chiedere: memoria, documenti, chat passate | non scritto | **manca** |
| 3. Prima di usare un documento, controllare che una decisione più recente non lo superi | regola «decisioni superate» nella memoria; stato degli ADR | **parziale**: nessun ordine di ricerca |
| 4. A fine di ogni blocco di lavoro, una riga nel diario | solo al merge di una PR col changelog (CI) | **manca** fuori dalle PR |
| 4b. Rileggere prima di riscrivere, non togliere righe altrui | file storico solo in coda; `--check` sui numeri | coperto meglio: da un cancello |
| 5. Righe brevi con rimando; decisioni una volta sola nel loro registro | memoria corta con puntatori; ADR; card | coperto |
| 6. Segnalare le discordanze fra memoria e documenti | `memoria.py --check` per `MEMORIA.md`; niente fra memoria delle sessioni e repo | **parziale**, chiuso in parte da questa PR |
| 7. Moodle, password | non pertinente | — |

## Decisione

1. **Lettura per PR senza scrivere il numero** (in questa PR): `--pr N`
   ricava da git le voci che il merge «Merge pull request #N» ha portato su
   main. Nessun campo da compilare a mano, nessuna rinumerazione.
2. **Confronto con la memoria delle sessioni** (in questa PR):
   `memoria_storica.py --confronta-memoria DIR` elenca le righe della
   memoria con PR, ADR, SHA o percorsi che il repo non ha, e le note che il
   file storico non cita. È un rapporto, non un cancello: la memoria sta
   fuori dal repo e la CI non la vede.
3. **Voce a fine blocco anche senza PR** (scelta del DM sulla card del 2026-11-18):
   ogni thread, a fine di un blocco di lavoro che non finisce in una PR
   (scelta su card, dato verificato, file solo nella cartella condivisa,
   thread che si risolve), scrive la voce in un file suo nella coda
   `/mnt/project-files/memoria-storica-coda/` (un file per thread: nessuna
   sovrascrittura). La routine del lunedì la porta nel repo con una PR che
   tocca solo il file storico (non strutturale: il cancello non chiede la
   riga del changelog), numerando le voci in quel momento.
4. **Righe nelle istruzioni del progetto** (le scrive il coordinatore,
   dopo il sì del DM al punto 3): ordine di ricerca prima di chiedere,
   controllo delle decisioni superate, voce a fine blocco, discordanze da
   segnalare.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Coda per thread nella cartella condivisa, piegata nel repo dalla routine (scelta) | nessun conflitto di numeri; nessuna PR minuscola per ogni card; la cartella sopravvive ai thread | fino al lunedì la voce sta fuori dal repo; la cartella non ha storia |
| Una PR di sola storia per ogni blocco | la voce entra subito | numeri MS in conflitto fra thread, decine di PR al giorno da riallineare |
| Cancello in CI sulla memoria delle sessioni | sarebbe un obbligo vero | la memoria non è nel repo; la CI non la vede |
| Campo PR obbligatorio e controllato in CI | numero nella voce | il numero nasce dopo il commit; git lo sa già (punto 1) |
| Indice semantico | cerca anche con altre parole | nessuna misura lo giustifica (ADR-0127, «Da rivedere se») |

## Conseguenze

- `--pr N` ritrova 90 PR su 90 (prima 37): 88 con la voce propria, #387 e
  #389 solo perché MS-0082 le cita (toccano solo `docs/` e non hanno voce).
  Il numero dal merge vale solo per le voci nate da una riga del changelog e
  senza numero scritto: le 67 righe portate in blocco dalla #381 non
  diventano «della» #381.
- Il confronto rende misurabile ciò che prima era solo regola: oggi 84 righe
  e 36 note. Dà falsi positivi su nomi di codice fra apici inversi e non vede
  le righe in prosa: dice dove guardare, non decide.
- La parte 3 resta una regola: un thread che non scrive la voce non è
  bocciato da niente. La routine del lunedì e `--confronta-memoria` la
  rendono visibile entro una settimana, non la impongono.
- Il confronto legge tutti i file di testo tracciati: circa 10 s.

## Da rivedere se

- la memoria del progetto entra nel repo (allora il punto 2 diventa un cancello);
- la coda resta vuota per due settimane mentre le card si chiudono (allora la regola non basta e serve un controllo alla chiusura del thread).
