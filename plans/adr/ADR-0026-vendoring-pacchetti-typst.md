# ADR-0026 — I pacchetti Typst si vendorizzano, la build non scarica niente

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: DM, lotto F1 di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md) —
*«Sì, vendorizzare»*
**Precedente**: [ADR-0010](ADR-0010-vendoring-skill-terzi.md) (vendoring per
cherry-pick, mai collezioni) · **Sblocca**: H2 (capolettera annegato, indice analitico)

## Contesto

La catena di stampa (ADR-0020) è deliberatamente un secondo binario: un solo
eseguibile `typst`, nessun toolchain. Due mancanze restavano aperte verso il
modello Paizo — il **capolettera annegato** e l'**indice analitico** — e per
entrambe esiste un pacchetto Typst maturo. Ma un pacchetto Typst si importa così:

```typst
#import "@preview/droplet:0.3.1": dropcap
```

e quella riga, la prima volta, **scarica** da `packages.typst.org` in una cache
utente fuori dal repo. Il che introduce tre cose che questo repo ha già deciso
di non volere:

1. **la rete dentro la build.** ADR-0020 promette un PDF byte-identico a parità
   di sorgenti; una dipendenza scaricata a runtime è un ingresso non versionato.
   La build di oggi e quella dell'anno prossimo possono divergere senza che
   nessuno abbia toccato il repo;
2. **una build che offline non parte.** In questo ambiente `packages.typst.org`
   è già irraggiungibile: `typst compile` senza il percorso locale muore con
   *«failed to download package»*. Non è un caso di scuola;
3. **codice di terzi che non passa da nessun cancello.** ADR-0010 aveva già
   deciso il contrario per le skill: si vendorizza, con la licenza, e si
   aggiorna a mano.

## Decisione

**I pacchetti Typst di terzi vivono nel repo**, in
`scripts/typst/packages/<namespace>/<nome>/<versione>/`, ed è quel percorso che
`typst` riceve con `--package-path`. La cache utente non viene mai popolata.

### 1. Cosa entra

Le stesse condizioni di ADR-0010 §2, tradotte:

- **licenza compatibile** (MIT/Apache/BSD) e **il file `LICENSE` resta integro**
  dentro il pacchetto — è la condizione per cui abbiamo il diritto di tenerlo;
- **attribuzione completa** nella tabella di `scripts/typst/packages/README.md`:
  pacchetto, versione, licenza e titolare, upstream, **e a cosa serve qui**.
  Un pacchetto vendorizzato senza un uso dichiarato è peso morto;
- **provenienza tracciabile**: repo di origine e **commit** da cui è stato
  copiato, con la data;
- si tolgono i file che il `typst.toml` del pacchetto stesso dichiara in
  `exclude` (asset, test, gallery, PDF campione): non servono a compilare.

Prima applicazione: **`droplet` 0.3.1** (MIT, © Eric Biedert) e **`in-dexter`
0.7.2** (Apache-2.0, JKRB / in-dexter Contributors), copiati da
`typst/packages` al commit `359500f2`. 112 KB in tutto.

### 2. Come si aggiornano

**Mai automaticamente** (ADR-0010 §3). La versione nuova si copia *accanto* alla
vecchia — il percorso le tiene separate — si sposta l'import, **si ricompilano i
volumi e si guardano le pagine**, e solo dopo si toglie la vecchia. Un pacchetto
di impaginazione cambia come appare la pagina: la sola CI verde non basta a dire
che è andata bene.

### 3. Il controllo

`scripts/tests/test_pacchetti_typst.py` (7 test) verifica che ogni pacchetto
dichiarato esista con entrypoint e `LICENSE`, che **la versione nel `typst.toml`
sia quella della cartella** (copiare il nuovo dentro la cartella vecchia è
l'errore facile: l'import continua a dire `0.3.1` e il codice è un altro), che
il README lo dichiari, che l'exporter passi davvero `--package-path`, e — se
`typst` è installato — che un documento che importa entrambi **compili con
l'ambiente ripulito**, senza proxy e senza `HOME`.

## Conseguenze

**Buone.**
- La build è offline e riproducibile davvero, non per convenzione.
- H2 è sbloccato: capolettera e indice analitico sono **la stessa decisione**, e
  ora è presa.
- Il diff di un aggiornamento è leggibile nel repo, come per le skill.

**Il prezzo, dichiarato.**
- **112 KB di codice di terzi nel repo**, e la responsabilità di guardarli: sono
  contenuto nostro adesso, non una dipendenza di qualcun altro.
- **Gli aggiornamenti di sicurezza non arrivano da soli.** Per un pacchetto di
  impaginazione senza I/O il rischio è basso, ed è il motivo per cui la
  decisione è accettabile qui e non lo sarebbe per una libreria di rete.
- **Una versione in più da ricordare**: quella nella cartella, quella nel
  `typst.toml` e quella nell'import devono coincidere. È esattamente ciò che il
  terzo test controlla, perché a ricordarlo a mano non funziona.

**Cosa NON decide.** Non apre ai pacchetti in generale: ogni pacchetto nuovo è
una riga nuova in quella tabella e una decisione a sé, come per le skill.
