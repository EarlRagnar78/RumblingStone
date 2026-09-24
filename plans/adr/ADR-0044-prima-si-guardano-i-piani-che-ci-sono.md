# ADR-0044 — Prima di aprire un piano, si guardano quelli che ci sono

- **Stato**: accettata
- **Data**: 2026-09-04
- **Decisori**: DM (Gianfranco Samuele), agente
- **Origine**: richiesta DM del 2026-09-04 — *«aggiungi una regola che prima
  visiona i plan esistenti, verifica se è qualcosa di nuovo e solo allora apre
  un plan, altrimenti fix o espande i plan esistenti»*
- **Formalizza** una regola già scritta a mano in `PIANO-VENDIBILITA` §8.4 dopo
  l'incidente della PR #72, e mai applicata perché stava dentro un piano invece
  che nella disciplina.

## Contesto

`plans/` contiene **trentaquattro** documenti. Nessuno se li ricorda a memoria,
e chi non li guarda riscrive.

Il costo è misurato, non temuto. Il 4 settembre sono stati aperti **tre piani
commerciali** senza guardare le PR aperte. La **#72**, in bozza dal 26 luglio,
conteneva già `PIANO-PRODOTTO-TOOLKIT-VENDIBILE`,
`PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE`, `AUDIT-DERIVAZIONE-IP-CAMPAGNA` e le
decisioni del DM di quel giorno — le stesse ri-poste a settembre. Il danno vero
non è stato il lavoro doppio: **due dei suoi ADR erano migliori** di quelli
riscritti al posto loro, e si sono recuperati solo perché il DM ha chiesto
*«ma hai mergiato i piani aperti?»*.

Il rimedio fu scritto in `PIANO-VENDIBILITA` §8.4 — *prima di aprire un piano,
si guardano le PR aperte* — e non è mai stato applicato, perché **una regola
scritta dentro un piano la legge solo chi apre quel piano**. È lo stesso difetto
che ADR-0041 ha trovato in `AGENTS.md` §Skills e ADR-0043 in `validate_maps`:
la regola c'è, il posto è sbagliato, e nessuno la incontra al momento giusto.

## Decisione

La regola sta in **`skills/rumblingstone-plans/`**, che è la skill che chiunque
apra, aggiorni o chiuda un piano deve caricare — e a cui `AGENTS.md` instrada
per compito dopo ADR-0041.

### La procedura, in quattro passi

1. **Leggere `plans/INDEX.md`**: è l'unico posto dove sta scritto cosa esiste e
   a che punto è.
2. **Cercare per argomento, non per titolo**: `grep -ril "<chiave>" plans/*.md`.
   Un piano che copre la richiesta può chiamarsi diversamente — la ricerca sulle
   mappe si chiama `RICERCA-GENERATORI-MAPPE-QUALITA-RHOD` e nessuno la trova
   cercando «cartografia».
3. **Guardare anche le PR aperte**: un piano può esistere e non essere su
   `main`. È esattamente il caso #72.
4. **Dichiarare quale delle tre**: espandere un piano esistente con un lotto
   nuovo · correggere un piano vicino · aprire, **scrivendo nel documento nuovo
   cosa si è guardato prima e perché non bastava**.

### Il §1 obbligatorio

Un piano nuovo apre dichiarando **cosa non rifà**. Senza quel paragrafo la
sovrapposizione arriva entro un mese: è successo cinque volte, e le cinque
sovrapposizioni sono finite consolidate in `PIANO-VENDIBILITA`.

### PIANO o RICERCA

Una **RICERCA** misura un divario e propone; un **PIANO** esegue. Se non si sa
ancora cosa fare, è una ricerca — e la ricerca può poi aprire un piano,
citandosi. La distinzione esisteva già nei fatti (`plans/` ha undici `RICERCA-`)
e non era mai stata scritta.

## Conseguenze

**Positive.**

- Il caso #72 non è più possibile per distrazione: chi apre un piano ha davanti
  la procedura nel documento che deve caricare comunque.
- I piani nuovi portano i confini scritti, quindi la sovrapposizione si vede al
  momento della revisione e non un mese dopo.
- La distinzione RICERCA/PIANO smette di essere folklore.

**Negative, e vanno dette.**

- ⚠️ **Nessun gate la verifica**, e a differenza di ADR-0041 non se ne può
  scrivere uno onesto: «questo piano si sovrappone a quello» è un giudizio, non
  un conteggio. Un gate meccanico — «il §1 esiste?» — verificherebbe la
  presenza del paragrafo, non che dica il vero, e insegnerebbe a scrivere un
  paragrafo vuoto. Qui il controllo è chi legge.
- **Costa una lettura** all'inizio di ogni lavoro pianificato. Con trentaquattro
  documenti è la lettura di `INDEX.md`, non di tutto: qualche minuto.
- **Può irrigidire.** C'è il rischio opposto — infilare un lavoro davvero nuovo
  dentro un piano vicino solo per non aprirne uno. La regola dice di
  **dichiarare** la scelta, non di preferire sempre l'espansione.

## La prima applicazione, come esempio

Il DM ha proposto due piani: *«la generazione delle mappe usa le best practice
dei cartografi?»* e *«le illustrazioni usano quelle degli illustratori di AP?»*.
Applicando la regola:

- `RICERCA-GENERATORI-MAPPE-QUALITA-RHOD` esiste, ma è un **censimento di
  strumenti**, non un audit del mestiere: tocca la tecnica solo di sfuggita
  (texture, bordi inchiostrati). La domanda è **nuova**.
- `PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI`, `PIANO-INTEGRAZIONE-PIPELINE-MAPPE` e
  `PIANO-EDITOR-VISUALE-MAPPE-TATTICHE` coprono la **catena**, non la
  **qualità del disegno**.
- Sul lato illustrazione esiste la skill `rumblingstone-art-direction`
  (ADR-0019), che è il **mestiere applicato**, non l'audit di quanto ci si
  attenga; e l'**automazione** è già la Fase 3 di
  `PIANO-RIPRESA-PR-ABBANDONATE` (la #106).

**Esito**: **una** ricerca sui due assi invece di due piani, che dichiara di non
rifare né il censimento degli strumenti né la pipeline della #106.
