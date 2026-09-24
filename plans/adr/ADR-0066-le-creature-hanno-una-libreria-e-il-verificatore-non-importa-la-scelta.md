# ADR-0066 — Le creature hanno una libreria, e il verificatore non ne importa la scelta

- **Stato**: 🟢 accettata
- **Data**: 2026-09-23
- **Contesto**: domanda del DM, 2026-09-23 — *«se i tre script usano le stesse funzioni, si possono unire in una libreria unica, lasciando nei tre script solo le funzioni diverse che chiamano la libreria comune? così è meglio o più facile da unire in `dm.py`?»*; risposta a D1 di `PIANO-QUALITA-DEL-CODICE` §8.6: *«D1 = sì (il verificatore condivide il lettore)»*
- **Estende**: [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md), con cui `dmcore/` è nata come libreria condivisa del toolkit; [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (sola stdlib); [ADR-0064](ADR-0064-gli-attributi-si-scrivono-nel-bestiario.md) e [ADR-0065](ADR-0065-la-conformita-si-corregge-dove-il-dato-non-e-una-scelta.md), di cui sposta il codice senza cambiarne una regola
- **Piano**: [`PIANO-QUALITA-DEL-CODICE`](../PIANO-QUALITA-DEL-CODICE.md) §8, lotto E

---

## Contesto

Quattro script lavorano sulle creature del Bestiario, e ognuno è nato per conto
suo:

| Script | Che cosa fa |
|---|---|
| `genera_attributi.py` | sceglie le sei caratteristiche di uno statblocco, a strati (ADR-0064) |
| `conformita_statblocchi.py` | verifica che pf, TS, BAB, lotta e attacco tornino con quelle caratteristiche (ADR-0065) |
| `derive_statblocks.py` | deriva dalle tabelle SRD i numeri che una scheda in prosa non scrive (ADR-0033) |
| `genera_creatura.py` | costruisce una creatura che non c'è, da GS, tipo e ruolo |

La misura del 2026-09-23 (§8.2 del piano), presa prima di scrivere una riga:

- la base dei tiri salvezza (buono 2 + L/2, cattivo L/3) è calcolata in **quattro**
  posti, e uno di questi, `conformita_statblocchi.ts_attesi`, riscrive la formula
  invece di chiamare `dmcore.tabelle.ts_buono`;
- classi e DV si leggono dal testo in **tre** posti;
- l'ordine delle caratteristiche per ruolo sta in **due** tabelle, che su sei
  ruoli coincidono in due;
- il verificatore **importa già 23 simboli** dal generatore (`PF_DADO`,
  `dadi_vita`, `pf_dado_sospetto`, `numeri_della_fonte`, `tetti_dai_ts`…), e il
  generatore importa il verificatore dentro una funzione, per non chiudere un
  ciclo al caricamento.

L'ultimo fatto è quello che decide. La risposta al DM dava l'indipendenza fra chi
genera e chi verifica per un principio da difendere; nel codice è parziale da
settimane, e **nessuno l'ha deciso**. Due script che si importano a vicenda non
dicono quale parte è condivisa di proposito e quale per comodità.

Il lotto non ripara un difetto di oggi. La classe di errori che l'ha fatto
nascere (un lettore corretto in un posto e non negli altri) la prende già il
cancello di `extract_statblocks --check`. Serve perché la prossima correzione di
un lettore si faccia in un posto solo.

## Decisione

### 1. Tre moduli in `dmcore/`, separati per chi li può importare

| Modulo | Contiene | Chi lo importa |
|---|---|---|
| `dmcore/progressione.py` | le regole di classe e di tipo: `Gruppo`, i nomi delle classi e le loro abbreviazioni, le due classi di prestigio SRD del Bestiario, la base dei TS, il BAB atteso | tutti |
| `dmcore/lettura_creatura.py` | **il lettore**: le espressioni regolari del blocco e della prosa, dadi vita, `pf-dado` sospetto, sestine della scheda e della fonte, numeri della fonte, composizione dei DV, talenti, provenienza delle caratteristiche, `leggi`/`Scheda`, e i **tetti** che un TS scritto mette ai modificatori | tutti, verificatore compreso |
| `dmcore/caratteristiche.py` | **la scelta**: gli strati di `genera`, gli array per ruolo con taglia e razza, i vincoli che sostituiscono un valore scelto, `PROFILI`, `PER_TAGLIA`, `RAZZE` | i generatori, **mai** il verificatore |

Il criterio non è l'argomento ma **la direzione della fiducia**. Una regola SRD e
una lettura del testo sono fatti che chi genera e chi verifica devono vedere
uguali. Una scelta no: se il verificatore la importasse, un errore nella scelta
comparirebbe da tutte e due le parti e si confermerebbe da solo. È già successo
con la Tabella 1–1, che la skill e la costante sbagliavano allo stesso modo e un
test confrontava fra loro.

### 2. Il verificatore condivide il lettore (D1)

Il DM ha scelto **sì**. Il verificatore legge le schede con lo stesso codice del
generatore; l'indipendenza sta nelle **regole** di conformità, che restano sue
(`ts_attesi` con le caratteristiche, `pf_attesi`, `verifica`, `giudica`), e nella
**scelta**, che non importa mai.

L'alternativa scartata era un lettore copiato nel verificatore: più sicuro contro
un errore di lettura condiviso, con una seconda copia da tenere allineata a mano.
Il repo ha già visto come finiscono le due copie (le tabelle SRD ricopiate in
`genera_attributi`, con il ranger a d10 e due taglie scambiate).

### 3. La regola diventa un test

`test_grafo_import_creature.py` legge gli import dei quattro script e dei tre
moduli con `ast`, compresi quelli dentro una funzione, e verifica che non ci
siano cicli e che `conformita_statblocchi` non arrivi mai a
`dmcore.caratteristiche`, nemmeno passando per un altro modulo.

### 4. Gli script restano dove sono

Stesso nome, stessa riga di comando, stesso output: la CI,
`tools.manifest.json`, le skill e i test li chiamano per nome. Dentro resta ciò
che è solo loro: `proponi`/`applica`/`--check`/`--taratura` di
`genera_attributi`; `verifica`, `giudica` e la correzione di `pf-dado` del
verificatore; `deriva` e il collaudo PF1e di `derive_statblocks`; il ramo mostri
e gli incantesimi di `genera_creatura`. I nomi vecchi restano importabili dagli
script come alias finché il sotto-lotto E8 non li toglie.

### 5. Il collaudo è un'impronta

`scripts/impronta_creature.py` scrive tutto quello che i quattro script calcolano
sul Bestiario vero, letture intermedie comprese, e un test la confronta con
quella committata dopo ogni spostamento. Un sotto-lotto che la cambia ha
cambiato un comportamento, e si ferma. L'impronta non si rigenera per far
passare il test.

### 6. Due cose che il disegno del piano metteva altrove

- **`tetti_dai_ts` e `plausibile` stanno nel lettore, non nella scelta.** Il
  piano li elencava fra gli strati di `genera`, ma il verificatore li usa quando
  ricostruisce il bonus di `pf-dado` (`pf_dado_corretto`), e metterli nella scelta
  avrebbe violato la regola del punto 3 al primo import. Nessuno dei due sceglie:
  `tetti_dai_ts` ricava un limite da un TS scritto e dalla progressione,
  `plausibile` rifiuta un modificatore ricavato che il GS non regge. Chi usa quel
  limite per abbassare un valore dell'array è `genera`, e resta nella scelta.
- **`derive_statblocks.leggi_scheda` non entra nel lettore.** Legge schede in
  prosa per derivarle, con la sua struttura `Lettura`, e unificarlo con il lettore
  degli statblocchi cambierebbe le proposte sulle 95 schede che legge oggi. Resta dov'è.

## Conseguenze

**Buone.**

- Una lettura si corregge in un posto, e il verificatore la vede subito.
- La base dei TS ha un solo punto di calcolo; la formula riscritta a mano nel
  verificatore sparisce.
- La dipendenza fra generatore e verificatore, che oggi è un import circolare
  dentro una funzione, diventa un grafo dichiarato e verificato.
- `genera_creatura` può usare la stessa scelta delle caratteristiche per i PNG
  (sotto-lotto E7), invece di una tabella dei ruoli sua.

**Quello che si paga.**

- **Un errore di lettura condiviso non lo vede più nessuno dei due.** Con due
  lettori, una scheda letta male dal generatore poteva risultare scartata dal
  verificatore; con uno, il numero sbagliato torna da tutte e due le parti. È il
  prezzo di D1, e il DM l'ha scelto sapendolo. La difesa sono i test del lettore
  sulle schede vere (`test_genera_attributi`, `test_conformita_statblocchi`) e
  l'impronta, che però protegge dallo **spostamento**, non da un errore già
  presente il giorno in cui è stata scritta.
- **Per un lotto intero esistono due nomi per ogni simbolo spostato**, il nuovo
  in `dmcore` e l'alias nello script. Fino a E8, chi cerca una funzione la trova
  in due posti.
- **`dmcore/` cresce di tre moduli** che nessun altro script usa ancora. Se il
  lotto si fermasse dopo E5, la libreria resterebbe un posto dove quattro script
  tengono il loro codice, senza un quinto che ne approfitti.
- **Per `dm.py` non cambia quasi niente.** `dm.py` chiama i suoi strumenti con
  `subprocess`, e un sottocomando `bestiario` costa una ventina di righe con o
  senza libreria (sotto-lotto E9, D3).

## Alternative considerate

- **Lasciare le cose come stanno.** Il costo era la manutenzione, non un difetto;
  ma l'import circolare e i 23 simboli presi dal generatore erano già una
  libreria, solo non dichiarata.
- **Una classe `Creatura` con i suoi metodi.** È la domanda OOP che §3 del piano
  ha già risposto: il vantaggio sta nei test e nei confini, non nella forma.
  Funzioni pure su un testo si provano scheda per scheda, e l'impronta le
  confronta una per una.
- **Un pacchetto nuovo fuori da `dmcore/`.** `dmcore` è già la libreria
  condivisa del toolkit e contiene le tabelle SRD e il blocco
  statistiche da cui questi moduli dipendono. Un secondo pacchetto dividerebbe
  in due la risposta a «dove sta questa funzione».

## Emendamento — 2026-09-23: la tabella dei ruoli è una (D2)

Il contesto contava due tabelle «ruolo → ordine delle caratteristiche»:
`PROFILI`, che sceglie gli `attributi` dei blocchi del Bestiario, e i sei
`Ruolo.priorita` di `genera_creatura`, che ordinavano la matrice dei PNG
generati. Su sei ruoli ne coincidevano due. Il DM ha scelto la prima (D2 = a).

**Cosa si decide.** Un ruolo di `genera_creatura` nomina un profilo di
`dmcore.caratteristiche.PROFILI` e ne legge l'ordine per chiave esatta. Il ramo
PNG di `genera_creatura` diventa così un generatore che importa la scelta, come
il punto 1 già prevedeva; il ramo mostri non la usa.

**Quello che si paga.** Cambiano i PNG che `genera_creatura` produce da qui in
avanti, in quattro ruoli su sei: il tiratore e il blaster perdono un punto
ferita per livello, il controllore e il blaster uno di Volontà. Nessun blocco
già scritto nel Bestiario cambia, perché nessuno di loro è uscito da
`genera_creatura`. Aggiungere un ruolo al generatore ora vuol dire scegliere un
profilo esistente o aggiungerne uno a `PROFILI`, e un profilo nuovo là vale
anche per le schede del Bestiario che ne contengono la parola.
