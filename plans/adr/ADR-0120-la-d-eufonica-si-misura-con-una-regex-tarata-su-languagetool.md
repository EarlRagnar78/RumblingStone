# ADR-0120 — La *d* eufonica si misura con una regex tarata su LanguageTool

**Stato**: proposta (2026-11-09)
**Data**: 2026-11-09
**Canale (ADR-0099)**: stable dal 2026-11-25, scelta del DM sulla card del 2026-11-25 (*«Tutti e sei, con il codice»*, D8 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md)). 141 run su `main` e 369 run di PR senza rossi; la forma fuori norma è un errore di `validate_lingua.py`, e l'opzione `--d-eufonica` e il suo passo separato escono ([misura](../esperimenti/promozioni-2026-11-25/MISURE.md)).
**Decisione-fonte**: il DM (Jfs), 2026-11-08, card D3 di PIANO-CODA-DEL-SECONDO-LETTORE: *ad* solo davanti alla stessa vocale, scritta in `editorial-standards.md` e misurata. Il 2026-11-09, Blocco 1 della roadmap: «fai tutte e 3 in ordine di importanza».
**Rapporti**: applica la regola del DM «si parte dallo standard di fatto, decide la misura». Segue [ADR-0079](ADR-0079-un-secondo-rilevatore-per-la-prosa.md) (LanguageTool come secondo lettore, l'apostrofo come regex del repo) e [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) (una norma senza misura non esiste). Resta dentro [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md): nessuna dipendenza nuova.

## Contesto

Il repo scriveva *legato a Aegis Fang* accanto a *ad esempio* e *ad ogni*, senza
una norma. Il DM ha deciso la norma il 2026-11-08. Serve un rilevatore, e la
regola del progetto vuole lo standard di fatto prima di uno fatto in casa.

## Alternative considerate

1. **LanguageTool nel cancello di CI** (lo standard di fatto, regola ST_03_001).
   Scartata: vuole Java e un server locale di circa 200 MB in ogni giro di CI, e
   propone *od*, che la norma non vuole. Resta il riferimento contro cui si tara.
2. **Una regex del repo, tarata su LanguageTool** (scelta).
3. **Nessun rilevatore, solo la norma scritta**. Scartata da ADR-0056.

## Decisione

`validate_lingua.d_eufonica_righe` segnala (in che canale, sotto):
- *a* davanti ad *a*, *e* davanti ad *e* (anche accentate, anche con corsivo o
  grassetto in mezzo, anche quando la congiunzione chiude la riga);
- *ad* davanti a vocale diversa da *a*, *ed* davanti a vocale diversa da *e*,
  tranne *ad esempio* e *ad es.*, come in LanguageTool.

Fuori norma: *o/od* (arcaico) e le lettere-etichetta (*Unità A*, *§7.E*).

## Canale (ADR-0099)

Il controllo è nuovo, quindi nasce nel canale **testing**, come il cancello dei
numeri di ADR-0118: nel passo bloccante `validate_lingua.py` la forma fuori norma
è un **avviso**; un secondo passo di CI, `validate_lingua.py --d-eufonica`, la
legge come errore ma **non blocca** (`continue-on-error`). Promozione a stable
proposta dal **2026-11-24**, alle condizioni di ADR-0099: 14 giorni e 10 corse
della CI su `main`, nessun falso allarme non spiegato. Quel giorno si toglie
`continue-on-error` e `--d-eufonica` diventa il comportamento di sempre.

Fatto il 2026-11-25, con la scelta del DM D8 di PIANO-PIATTAFORMA-DI-SVILUPPO: l'opzione è uscita insieme al passo.

Il corpus a zero e la misura qui sotto non bastano a saltare il canale: dicono
che la regex non sbaglia sui testi di oggi, non su quelli che si scriveranno.

## Misura

`plans/esperimenti/d-eufonica-2026-11-09/RISULTATO.md`: sui 686 file di contenuto
la regex concorda con LanguageTool su 53 righe; le 28 solo di LanguageTool sono
*o o…* e lettere-etichetta (più due righe rientrate, corrette a mano); le 2 solo
della regex sono errori veri che LanguageTool perde. Dopo la correzione: 0
segnalazioni della regex, 26 di LanguageTool, tutte delle due classi escluse.

**Falsi positivi misurati** (2026-11-10): sui 692 file di contenuto la regex ha
segnalato 55 righe prima della correzione, tutte lette e tutte errori veri (53
confermate da LanguageTool, 2 che LanguageTool perde): **0 su 55**. Le forme
fisse *ad esempio* e *ad es.* sono escluse per costruzione; *ad hoc* è in norma
perché la *h* non è una vocale. Le lettere-etichetta e i nomi propri con la
maiuscola (*Unità A attacca*, *Appendice A*) non scattano: 9 casi che
LanguageTool segnala e la regex no. I 16 file di `_testi-altrui/` non si
controllano; a provarla lì la regex segnala 5 righe, tutte fuori norma davvero
(sono della fonte e restano come sono). Le citazioni non hanno un filtro: una
citazione con *ad ogni* verrebbe segnalata, e nel corpus non ce n'è nessuna.

## Conseguenze

- Il conto è a zero: fino alla promozione una forma nuova fuori norma si vede nel
  passo in testing e nel conto degli avvisi, ma **non ferma una PR**.
- 58 righe corrette in 42 file, archivi compresi.
- ~~Le righe rientrate come codice non si controllano.~~ Superato con
  l'emendamento del 2026-11-11, qui sotto.

**Da rivedere se**: LanguageTool trova sul repo una classe di forme che la regex
non vede (si rifà `misura.py` dopo un lotto grande di prosa nuova); il DM decide
di accettare *od*; la CI accetta un servizio Java, e allora il cancello passa a
LanguageTool.

---

## Emendamento del 2026-11-11 — i limiti si misurano seminando, e due si chiudono

**Stato**: accettato dal DM il 2026-11-12 per la scelta del parser (card «parser CommonMark» contro «regola del repo, solo stdlib»); il resto proposta · **Chiesto dal DM** il 2026-11-11: «c'è un modo deterministico e affidabile, misurando il miglioramento?»

### Contesto

Col corpus a zero il conto dei rilievi non dice più niente: 0 vuol dire «pulito»
o «cieco». I limiti dichiarati erano tre: le righe rientrate saltate come codice,
le citazioni senza filtro, la *a* minuscola usata come etichetta.

### Alternative considerate

1. **Contare i rilievi sul corpus vero**. Scartata: prima e dopo fa 0.
2. **Un banco di semina** (scelta): errori noti messi in modo deterministico in
   una copia in memoria di ogni file, e si conta quanti ne trova il rilevatore,
   posto per posto. È il test di mutazione applicato alla prosa.
3. Per distinguere il codice dalla prosa rientrata: **il parser CommonMark di
   riferimento, markdown-it-py** (scelta, lo standard di fatto), oppure una
   regola del repo solo stdlib (resta come ripiego).
4. Per le citazioni: **un marchio esplicito sulla riga** (scelta), oppure
   indovinare la citazione dalle virgolette. Scartata la seconda: nei testi di
   gioco le virgolette aprono quasi sempre un dialogo scritto da noi, che la
   norma la deve rispettare.

### Decisione

- `plans/esperimenti/d-eufonica-limiti-2026-11-11/semina.py` è la misura del
  rilevatore. Si rifà a ogni modifica della regex o di `righe_da_controllare`.
- `validate_lingua.righe_di_codice` chiede a markdown-it-py quali righe sono
  codice. Una riga rientrata che è il seguito di un elenco o di un paragrafo è
  prosa e si legge, per **tutti** i controlli del validatore. markdown-it-py
  (MIT, puro Python) entra in `requirements.txt` come libreria opzionale con
  ripiego dichiarato (famiglia di Pillow in ADR-0037): senza, vale la regola
  stdlib `_codice_senza_parser`, e il validatore lo stampa.
- `<!-- sic -->` su una riga dice che è una citazione alla lettera: lì la *d*
  eufonica non si segnala, gli altri refusi sì. Il conto delle righe marcate si
  stampa a ogni giro. Vale anche per una *a* minuscola usata come etichetta.

### Misura (692 file, 3.944 righe di prosa seminate, 106 nel codice)

| Rilevatore | Richiamo sulla prosa | Righe rientrate di prosa | Rilievi nel codice | Rilievi su righe non seminate |
|---|---:|---:|---:|---:|
| Regex, prima | 3.880 (98,38%) | 0 su 64 | 1 su 106 | 0 |
| Regex, regola stdlib | 3.944 (100%) | 64 su 64 | 1 su 106 | 0 |
| **Regex, markdown-it-py** | **3.944 (100%)** | **64 su 64** | **0 su 106** | **0** |
| LanguageTool ST_03_001 | 3.323 (84,25%) | 64 su 64 | 1 su 106 | 23 |

Le righe lette dal validatore passano da 116.470 a 117.589: 1.309 righe rientrate
di prosa che prima nessun controllo leggeva. Sul corpus vero: 0 errori prima e
dopo, 48 avvisi di virgolette dritte in più. LanguageTool perde le 619 righe di
tabella, che svuota prima di leggere; i suoi 23 rilievi su righe non seminate
sono le classi già note (*o o…*, lettere-etichetta).

La regola stdlib e markdown-it-py classificano in altro modo 184 righe, quasi
tutte in `ARC08-92-DEPRECATO-atlante-visivo-v3-complete.md`, che ha i recinti
rotti (la chiusura in coda a una riga di testo): CommonMark li legge come
codice fino in fondo, la regola stdlib no.

### Conseguenze e limiti onesti

- I semi nascono da quattro schemi vicini a quelli della regex: il banco misura
  **dove** il rilevatore legge, e lo fa bene; non dimostra che gli schemi siano
  tutta la lingua. Lì il riscontro indipendente resta LanguageTool, che sui semi
  in riga normale ne conferma 2.502 su 2.503.
- I semi sono solo minuscoli e sulla stessa riga: maiuscole, corsivo in mezzo e
  congiunzione a fine riga restano coperti dai test, non dal banco.
- Il marchio `sic` è a mano: una citazione non marcata viene segnalata. Oggi nel
  corpus non ce n'è nessuna.
- Il canale non cambia: testing fino al 2026-11-24. Salito a stable il 2026-11-25 (intestazione).

**Da rivedere se**: il banco scende sotto il 100% dopo una modifica; markdown-it-py
cambia la lettura dei blocchi rientrati in una versione nuova (si vede dal banco).
