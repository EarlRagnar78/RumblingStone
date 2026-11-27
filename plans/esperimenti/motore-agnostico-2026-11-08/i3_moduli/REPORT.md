# I3 · Come un plugin porta il suo codice (2026-11-08)

**Domanda.** Alcune regole sono algoritmi e non si riducono a dati. Oggi sono due: il metodo `potenze` del 3.5 e il metodo `somma_px` del PF1e, tutti e due in `METODI` di `suggest_encounter`. Vogliamo che vivano nel plugin del loro sistema e non nel nucleo. Con quale meccanismo li carichiamo, senza `pip`, senza che due plugin si pestino i piedi e senza che una dichiarazione possa puntare fuori da `sistemi/<id>/codice/`?

**Come si rifà.** Si lancia `banco_moduli.py`, che sta in questa cartella. Per il terzo candidato serve `pluggy`, da installare in un ambiente separato. I dati grezzi sono in [RISULTATI.json](RISULTATI.json). Il banco è deterministico: due esecuzioni producono file identici (`cmp`). ⚠️ Dopo F5 (2026-11-08) gli algoritmi non stanno più in `suggest_encounter`, e il banco legge il loro sorgente da lì: si rifà dal commit `aee16d0`. Le stesse misure, sul codice nuovo, le rifà `scripts/tests/test_moduli_plugin.py`.

## Metodo

Il banco crea un repo temporaneo con due plugin, dnd35 e pf1e. Ognuno ha un file `codice/metodi.py`, con **lo stesso nome di modulo** e la stessa funzione `combina`, ma con l'algoritmo del proprio sistema copiato dal nucleo. Su questo repo prova tre caricatori.

| Caricatore | Cosa fa |
|---|---|
| **importlib** | Registro per nome in `sistema.toml` (`[moduli] combina = "metodi:combina"`). Il file si carica con `importlib.util.spec_from_file_location`, che è la ricetta della documentazione di Python per importare un file sorgente. Il modulo prende un nome unico, `rs_plugin.<id>.<modulo>`. Si accettano solo file in `sistemi/<id>/codice/`, dopo aver risolto i symlink |
| **entry point** | Gruppo `rumblingstone.metodi` di `importlib.metadata`. È il meccanismo PyPA per i plugin che si installano come distribuzioni. Il banco scrive a mano il `dist-info`, perché nella skill impacchettata non c'è `pip` |
| **pluggy** 1.7 | Usato da pytest e tox. È un registro di ganci (`hookspec`), ma non sa trovare file, quindi i moduli li trova il caricatore importlib |

Ogni caricatore viene misurato su cinque criteri:

- **(a) Correttezza.** Il metodo caricato dal plugin deve dare lo stesso EL di `METODI` su tutte le liste da 1 a 3 GS, prese fra 28 valori con ripetizione: 4.494 liste per sistema.
- **(b) Isolamento.** I due `metodi.combina` devono restare separati.
- **(c) Dichiarazioni ostili.** Il banco ne prova 12: `../`, un percorso assoluto, `os:system`, `builtins:exec`, un modulo con il punto, un nome dunder, `math.sqrt`, una funzione che non c'è, un oggetto non chiamabile, un modulo che non c'è, un symlink verso `scripts/`, una stringa vuota.
- **(d) Determinismo** dell'ordine del registro.
- **(e) Costo**, cioè righe del caricatore e dipendenze.

## Risultato (Python 3.13)

| Caricatore | Correttezza dnd35 | Correttezza pf1e | Isolamento | Ostili rifiutate | Deterministico | Righe | Da portare nel pacchetto |
|---|---|---|---|---|---|---|---|
| **importlib** (libreria standard) | 4494/4494 | 4494/4494 | sì | **12/12** | sì | 14 | niente |
| entry point (PyPA) | 4494/4494 | **72/4494** | **no** | 8/12: accetta `os:system`, `builtins:exec`, `math.sqrt` e il symlink | sì | 16 | un `dist-info` installato per ogni plugin |
| pluggy sopra importlib | 4494/4494 | 4494/4494 | sì | 12/12 | sì | 19 | pluggy (MIT, puro Python, 2.094 righe) |

## Lettura

- **Gli entry point sono lo standard di fatto, ma per un caso diverso dal nostro**: plugin distribuiti come pacchetti installati, dove ognuno ha un nome di modulo unico. Qui la misura li boccia per tre motivi.
  1. Il riferimento può essere qualunque oggetto importabile. `os:system` e `builtins:exec` passano, e anche il symlink che esce dalla cartella.
  2. Due plugin con un modulo `metodi` si pestano attraverso `sys.modules`. Il PF1e riceve in silenzio l'algoritmo del 3.5, e solo 72 liste su 4.494 risultano giuste, quelle in cui i due metodi coincidono per caso.
  3. Ogni plugin dovrebbe essere installato. Questo va contro il bundle senza `pip` di ADR-0112 e del modello iemod-fetch.
- **pluggy è lo standard di fatto per i ganci** (pytest), e serve quando più plugin rispondono allo stesso gancio. Il nostro caso è più semplice: una funzione per nome, con un solo plugin che la possiede. pluggy dà gli stessi numeri di importlib, perché ci si appoggia sopra, e aggiunge una dipendenza di 2.094 righe. **La misura non lo giustifica oggi.**
- **`importlib.util.spec_from_file_location` è la ricetta standard della libreria standard** per caricare codice da una cartella di dati. Passa tutti i criteri con 14 righe. Le ostili vengono rifiutate prima di caricare qualunque cosa fuori dalla cartella. Il nome unico per ogni sistema evita la collisione.

## Note oneste

- Il codice dentro `sistemi/<id>/codice/` **viene eseguito** al caricamento: è codice Python, non è in una sandbox. Con «funzione che non c'è» e «non chiamabile» il modulo del plugin gira prima che arrivi il rifiuto. Il caricatore protegge da riferimenti che **escono** dalla cartella, non da un plugin scritto male. Il codice di un plugin si rivede in PR come quello del nucleo.
- Le 12 ostili sono una lista scritta a mano, non un'enumerazione completa.

## Proposta per F5

1. `sistema.toml` ha una sezione `[moduli]` nome → `"modulo:funzione"`. La capacità `incontri.livello` nomina il metodo e il nucleo lo cerca nel registro del plugin, risalendo l'eredità. Non lo cerca più in `METODI`.
2. Il caricatore è quello di importlib di questo banco, in `dmcore/sistemi.py`. Il test ostile del banco diventa un test della suite.
3. `potenze` va nella cartella `codice/` del plugin d20 (o di dnd35), `somma_px` in quella del plugin pf1e; F5 crea le cartelle. Criterio di uscita: nessun algoritmo di sistema nel nucleo e EL identici su tutte le 4.494 liste.

**Da rivedere se** più plugin devono rispondere allo stesso punto: per esempio un plugin di ambientazione che aggiunge regole sopra quelle del sistema. È il caso per cui pluggy esiste, e lì va rimisurato.
