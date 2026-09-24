# ADR-0031 — `dm.py volume`: l'ordine dei mestieri, e il cancello detto a voce

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: lotto **G3** di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md), che
nasce da §C di
[RICERCA-RUOLI-EDITORIALI-COLOPHON](../RICERCA-RUOLI-EDITORIALI-COLOPHON-PAIZO-2026-08.md)
— *«la combinazione mancante»* · **Assorbe**: il `dm.py stampa` promesso
dall'audit di agosto e mai fatto

## Contesto

La ricerca sul colophon Paizo aveva ribaltato la domanda del DM. Non mancava un
mestiere: **mancava l'ordine in cui si chiamano**. Le skill c'erano tutte —
redazione, coerenza, impaginazione, edizione — e nessun documento diceva la
sequenza per produrre un volume. Chi ne saltava uno se ne accorgeva in
copisteria, o non se ne accorgeva affatto.

E c'era un secondo buco, misurato nel lotto E: `grep -rl "GUIDA-CONDIVISIONE-IP"
skills/` restituiva **un solo file**, e per un'altra ragione. Il cancello
d'uscita di ADR-0005 esisteva scritto e non lo incontrava nessuno.

## Decisione

**`dm.py volume MANIFEST.json`** esegue la catena in ordine, dichiarato:

    prosa → lingua → manifest → colophon → schermo → stampa → imposizione

`--stampa` aggiunge l'edizione Typst (è il `dm.py stampa` mai fatto, assorbito
qui invece di essere un comando a parte); `--imposto` il libretto da piegare;
`--solo` e `--salta` per rifare un passo solo.

### 1. Non tutti i passi hanno lo stesso peso

- **`prosa` e `lingua` misurano e non bloccano.** La norma è
  `italiano-nativo.md`; questi la contano (ADR-0025). Un gate rumoroso che
  blocca viene disattivato entro una settimana, e allora non trova più nemmeno i
  refusi veri.
- **`manifest` e `schermo` sono guasti duri e fermano la catena.** Compilare
  l'HTML da un manifest non valido produce un artefatto sbagliato **con l'aria
  di essere andato bene**, ed è il modo peggiore di fallire.
- **`stampa` e `imposizione` degradano pulito** (ADR-0027): se `typst` o
  `pdfcpu` mancano, lo dicono e la catena prosegue. Il volume resta stampabile
  pagina per pagina.

### 2. `colophon` non è un controllo di schema

Quello lo fa già `validate_booklets`. Questo è **la domanda dell'editore**:
*questo volume dice di chi è, che versione è e cosa se ne può fare?* Un volume
anonimo si stampa lo stesso — è precisamente il difetto che ADR-0023 ha chiuso, e
qui si verifica che non torni.

### 3. Il cancello d'uscita si **dice**, sempre

In coda, comunque sia andata, il comando ricorda il §7 di
`GUIDA-CONDIVISIONE-IP.md`: *«uso privato al tavolo: nessun cancello; fuori di lì
quelle cinque domande vengono prima, e se c'è di mezzo del denaro ci si ferma»*.

**Non è automatizzabile e non si finge che lo sia.** Ma questo è il momento in cui
un volume sta per uscire, ed è l'unico punto della catena in cui metterlo davanti
a una persona ha senso. Una regola scritta che nessuno carica non è una regola: è
la stessa constatazione che ha motivato la skill `rumblingstone-edizione`.

## Conseguenze

**Buone.** L'ordine dei mestieri esiste in un posto solo ed è eseguibile. Il
`dm.py stampa` promesso non resta un debito. Il cancello IP smette di essere una
pagina che nessuno apre.

**Il prezzo, dichiarato.**
- **L'ordine è ora una decisione**, non un'abitudine: cambiarlo è modificare
  questo ADR e la costante `PASSI_VOLUME`, che un test confronta pezzo per pezzo.
- **Un volume alla volta.** Niente ricompilazione di massa: quella resta un
  ciclo di shell, e va bene così.
- **Il promemoria in coda si può ignorare.** È un promemoria. L'alternativa —
  bloccare la compilazione finché qualcuno non risponde a cinque domande — renderebbe
  il comando inusabile per l'uso privato, che è il 99% dei casi.
