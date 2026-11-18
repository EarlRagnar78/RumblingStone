# ADR-0138 — La coda della memoria storica ha un cancello

**Stato**: accettata (2026-11-18)
**Data**: 2026-11-18
**Decisione-fonte**: il DM (Jfs), 2026-11-18, chat di progetto, dopo aver scelto la coda per thread di [ADR-0137](ADR-0137-la-memoria-storica-si-scrive-a-ogni-blocco-di-lavoro-non-solo-al-merge.md): «aggiungi anche il cancello di verifica per il punto 3 per superare dall'inizio il limite trovato».
**Rapporti**: completa il punto 3 di ADR-0137, che lasciava la voce a fine blocco come sola regola scritta. Estende il cancello di forma di [ADR-0127](ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md).

## Contesto

ADR-0137 ha misurato che la regola scritta non bastava: in sei giorni 0
voci su 98 erano nate fuori da una PR. La coda per thread
(`/mnt/project-files/memoria-storica-coda/`) sposta il problema, non lo
chiude: un thread che non scrive il suo file non lo bocciava niente. Sui 13
thread risolti dal 2026-11-12 al 2026-11-17 nessuno ha una voce sua.

Il limite è di posto: la CI del repo non vede la cartella condivisa né i
thread. Un cancello vero può stare solo dove quei dati si vedono, cioè nelle
mani di chi risolve un thread e della routine del lunedì.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Script stdlib con tre controlli (forma, thread senza voce, piega numerata) e un controllo in più in CI** (scelta) | stesso stile del repo; esce 1, quindi chi lo lancia non può non vedere; la piega non lascia entrare una voce storta | va lanciato: non parte da solo alla chiusura di un thread |
| Solo la regola nelle istruzioni | nessun codice | è ciò che la misura ha bocciato |
| Portare la coda nel repo e controllarla in CI | cancello automatico | ogni card diventa una PR; numeri in conflitto fra thread (scartata in ADR-0137) |
| Un hook alla chiusura del thread | automatico | la piattaforma dei thread non ne offre uno che il repo possa configurare |

## Decisione

1. **`scripts/memoria_coda.py DIR --check`**: la forma di ogni voce in coda
   (testa `### MS-???? · data · titolo`, campi obbligatori del file storico,
   data valida, Testo di almeno 40 caratteri, nome del file ricavato dal
   titolo del thread). Esce 1 al primo difetto.
2. **`--thread "Titolo"`**: esce 1 se il thread non ha una voce, né in coda né
   già nel repo. Lo lancia il coordinatore prima di risolvere un thread, e
   il thread stesso prima di dichiararsi finito.
3. **`--threads elenco.json`**: dato l'elenco dei thread (la forma di
   `list_threads`), esce 1 se un thread risolto dal 2026-11-18 non ha voce.
   Lo lancia la routine del lunedì e segnala chi manca.
4. **`--piega`**: porta le voci nuove in `plans/MEMORIA-STORICA.md`,
   numerate dopo l'ultima e col campo `Coda`, solo se la coda è in forma e il
   file risultante passa `memoria_storica.py --check`. Una seconda piega non
   ripete nulla, quindi i file di coda non vanno svuotati.
5. **In CI**: `memoria_storica.py --check` boccia una testa `### MS-` che non
   si legge (per esempio `MS-????` copiata a mano dalla coda), che prima
   spariva dentro la voce precedente.

## Conseguenze

- Thread risolti dal 2026-11-12 senza voce: 13 su 13, ora misurabili con un
  comando. La regola vale dal 2026-11-18: per quelli di prima il controllo
  non scatta (non si chiede a thread chiusi di riscrivere la loro storia).
- Voci nate fuori da una PR: da 0 a 5 con la prima piega (MS-0169…MS-0173:
  regola di merge del 12/11, decisioni su card, rilascio 1.1.0, metodo di
  Document AI, questa scelta). Poi a 11 con la seconda piega (MS-0175…MS-0180),
  chiesta dal DM lo stesso giorno: i 13 thread riletti per intero, messaggi,
  card e scelte. Quattro avevano qualcosa che repo e file storico non
  dicevano (immagini in posa, LLM locale, revisione dei bot, bug dei tag di
  typst); negli altri nove ogni scelta su card era già in un ADR, nel
  changelog dei piani o in una voce.
- Alla prima prova vera la piega si è fermata su un file della coda scritto
  da un altro thread senza la testa «### MS-????»: il cancello fa il suo
  lavoro, e finché quel file non è corretto la piega del lunedì non passa.
- **Cosa il cancello non vede.** Non parte da solo: se nessuno lo lancia
  non boccia niente. Non sa di una card chiusa dentro un thread ancora
  aperto. Non giudica se la voce dice tutto: controlla la forma e una
  lunghezza minima. Il titolo del thread deve essere quello dell'elenco: un
  thread rinominato dopo aver scritto la voce risulta senza voce finché il
  file non si rinomina.
- La piega scrive un file di canone: va in una PR di sola storia, come
  dice ADR-0137, e la sua voce porta il campo `Coda` al posto della riga
  del changelog.

## Da rivedere se

- dopo due lunedì `--threads` trova ancora thread risolti senza voce (allora
  il lancio a mano non basta e serve chiedere alla piattaforma un controllo
  alla chiusura);
- le voci in coda passano la forma ma non dicono la decisione (allora si
  misura un controllo sul contenuto, per esempio «card» senza il nome della
  scelta).
