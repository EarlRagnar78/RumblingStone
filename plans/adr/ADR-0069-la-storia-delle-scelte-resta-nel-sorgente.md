# ADR-0069 — La storia delle scelte resta nel sorgente e non va in stampa

- **Stato**: accettata
- **Data**: 2026-09-25
- **Numero**: 0069 e non 0068, che `PIANO-CICLO-DI-SESSIONE-E-MENU` ha già
  riservato per il menu
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: richiesta del DM del 2026-09-25, dopo la #169:
  *«per tutti i booklet e gli echi rimuovere tutte le parti che riguardano le
  scelte fatte nel repo, tipo "si è scelto così perché" oppure "prima era così
  e ora è cambiato"; vanno in un file storico che non viene renderizzato, anche
  nello stesso file se si riesce, vedendo se dopo il risultato è più pulito»*
- **Rapporti**: si aggiunge alle regole d'impaginazione di
  [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) e le applica a tutte e due
  le catene di [ADR-0013](ADR-0013-standard-generazione-booklet-sessioni.md)

## Contesto

I master e i booklet del repo si scrivono in molte passate, e ogni passata
lasciava una traccia: «✏️ Allineato il 2026-09-24 su decisione del DM», «il box
di prima diceva…», `[CANONE — DM 2026-07-31]`, un §9 intero intitolato «Cosa è
cambiato nel riordino». Nel repo servono: dicono perché una riga è così, e chi
la cambia sa cosa sta toccando. Al tavolo sono rumore, e in un volume stampato
dicono al lettore che sta leggendo una bozza.

Misurato il 2026-09-25 sui file che i manifest stampano: 181 righe portavano un
segnale di storia, e a mano 161 erano storia vera e 20 falsi positivi (frasi
dentro la finzione, come «la Sala non è cambiata», o regole come «a scelta del
DM»). Nei quindici PDF le righe con un segnale erano 257.

Togliere quelle righe dai sorgenti avrebbe perso l'informazione. Spostarle in
un file storico a parte l'avrebbe separata dalla riga che spiega, e i due file
avrebbero divergito alla prima modifica.

## La decisione

**La storia resta nel sorgente, accanto alla riga che spiega, e le catene di
stampa non la stampano.** Una funzione sola, `dmcore.testo.togli_storico`, la
chiamano la catena HTML e quella Typst, così le due non possono divergere.

Le forme sono tre, scritte a mano da chi scrive il master:

| Forma | Si usa per | In stampa |
|---|---|---|
| `<!-- storico -->` e `<!-- /storico -->`, ciascuno su una riga sua | un paragrafo o un riquadro di storia | sparisce il blocco |
| gli stessi marcatori dentro una riga | una frase o un inciso | sparisce il pezzo |
| `<!-- storico: riga -->` dentro una cella | una riga di tabella | sparisce la riga |

Su GitHub i marcatori sono commenti e non si vedono, e il testo in mezzo si
legge come prima.

Le attribuzioni che hanno una forma fissa se ne vanno da sole, senza
marcatori: `[CANONE — DM 2026-07-31]`, «(decisione DM 2026-09-24)», `[verif. ✓
…]`, «(ADR-0014 §1)», «(verificato il 2026-09-24)». Si toglie la cornice, il
contenuto resta: «(CANONE DM 2026-07-23: si aggancia al Cerchio Sacro)»
diventa «(si aggancia al Cerchio Sacro)».

Quando la storia e il fatto stanno nella stessa frase, la frase vecchia va nel
blocco storico e sotto si scrive quella nuova, che dice solo il fatto.

## Le conseguenze

Il risultato, sui quindici volumi del repo:

| | Prima | Dopo |
|---|---:|---:|
| righe dei PDF con un segnale di storia (falsi positivi compresi) | 257 | 67 |
| righe di storia vera arrivate in stampa, contate dal test | 161 | 15, tutte dichiarate |
| pagine: volume del −1000 · serata della resurrezione · Terros | 42 · 104 · 48 | 40 · 101 · 47 |
| sovrapposizioni, pagine quasi vuote nuove | 0 · 0 | 0 · 0 |

Le 15 righe rimaste sono elencate in `scripts/tests/test_storico.py`, file per
file, con il motivo: date d'edizione, date in cui un pezzo è stato giocato, la
provenienza di un'immagine, due capitoli da beta del Drappo che il DM deve
decidere se tenere nel volume.

Il test è un tetto: una riga di storia nuova senza marcatore lo fa diventare
rosso, e la correzione è il marcatore, non il numero.

Quello che si paga:

- **I marcatori si scrivono a mano.** Le attribuzioni di forma fissa le prende
  la funzione; una frase come «la stesura di prima metteva Balvar nella tenda»
  no, perché una regola che la riconoscesse prenderebbe anche la finzione.
- **Dentro un blocco preformattato** (uno statblocco) la funzione toglie solo
  la marca che si chiude sulla stessa riga. Una marca che va a capo resta:
  toglierla unirebbe due righe, ed è successo scrivendo la funzione (lo
  statblocco di Terros passava da 71 a 98 celle e finiva su una pagina sua).
- **Due errori della funzione sono stati presi prima del merge** e sono ora
  casi del test: un marcatore in linea a inizio riga preso per un blocco, che
  nel Palio si portava via l'intera intestazione, e una virgola che faceva
  perdere il contenuto di una parentesi. Una regola che toglie testo sbaglia
  in silenzio: il test sul corpus vero è la ragione per cui questa si può usare.

## Estensione: l'istruzione di consegna sui fogli ✉

Lo stesso giorno, rileggendo il volume dei giocatori della serata, il DM ha
trovato in testa a undici fogli l'istruzione di consegna scritta per lui: «Si
consegna al risveglio, quando Durik appoggia la testa sul petto di Hella»,
«Il DM te la consegna dopo che hai scelto di donare». Il giocatore che riceve
il foglio non ne ha bisogno, e in due casi gli anticipa la scena.

La stessa funzione chiude anche il blocco `<!-- consegna -->` …
`<!-- /consegna -->`. Quello che diceva il blocco resta nel master, nella riga
**✉ Si consegna qui**, o nella regia della serata: tre informazioni che non
c'erano (come si legge la preghiera, le caselle dei Doni che segna il DM, la
seconda metà dell'eco di Hella) sono state aggiunte lì prima di chiudere i
blocchi. Il test `TestIFogliDeiGiocatori` boccia un capitolo `player` che
stampa ancora un'istruzione di consegna.
