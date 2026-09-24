# ADR-0043 — Le montagne sono muri, e nessun master esce dal controllo

- **Stato**: accettata
- **Data**: 2026-09-04
- **Decisori**: DM (Gianfranco Samuele), agente
- **Origine**: `LEGENDA-FUNZIONALE-SPEC` §6.1 (aperta da luglio) · il punto cieco
  trovato scrivendo la Fase 0 di `PIANO-RIPRESA-PR-ABBANDONATE` · decisione DM
  del 2026-09-04: *«aprilo assolutamente come bug da fixare prima di tutti»*

## Contesto

Due difetti che sembrano lontani e sono la stessa famiglia: **cose che il codice
dava per buone senza che nessuno le contasse**.

### Il primo — `⛰` è disegnato solido e non è un muro

**2.423 celle in 21 file.** Il renderer disegna la montagna come solida: ombra
portata, contorno a inchiostro marcato, riempimento roccioso, e il suo pattern è
dentro `HEAVY_PATS`. L'export UVTT non ci metteva un muro. In Foundry un
personaggio **attraversa la catena montuosa e ci vede attraverso**.

La misura dice quanto era grosso. La mappa `Hammerfist-L1-REVISED-Ultra-Clear`
ha **338 celle di montagna** e produceva **8 segmenti di muro**: tutta la catena
era invisibile al VTT. Dopo il fix ne produce **20**.

| Mappa | celle `⛰` | segmenti prima | dopo |
|---|---:|---:|---:|
| `Hammerfist-L1-REVISED-Ultra-Clear` | 338 | 8 | **20** |
| `Hammerfist-L2-REVISED-Ultra-Clear` | 808 | 44 | **66** |
| `Hammerfist-Lotto-1-Ricognizione` map02 | 179 | 4 | **14** |
| `hammerfist-L2-assedio` | 1.800 | 50 | **54** |

⚠️ L'ultima riga merita una parola: 1.800 celle e **+4** segmenti soli, perché la
montagna lì è un bordo compatto e la fusione greedy la riduce a poche corse
lunghe. Il numero di segmenti misura la **geometria**, non quanta roccia c'è.

La diagnosi era in `LEGENDA-FUNZIONALE-SPEC` **da luglio**, con la riga di codice
da cambiare già scritta. È rimasta lì sei settimane: è esattamente il difetto
trasversale che l'audit della #99 nomina — *la qualità vive nelle regole scritte
e non negli automatismi*.

### Il secondo — un master a cui togli tutti gli SVG esce dalla validazione

`validate_maps.py` rende **solo i markdown che hanno già almeno un SVG
committato**. È una scelta ragionevole (evita di trattare come mappa ogni file di
appunti), e ha un rovescio che nessuno aveva guardato:

> cancella **tutti** gli SVG di un master, e quel master **sparisce dal
> controllo**. La CI resta verde, e nessuno guarda più quelle mappe.

Non è ipotetico: è **quello che fa la PR #63**, che cancella i sette SVG dei tre
master `Hammerfist-Lotto-*` deprecati **tenendo i master**, i quali generano
ancora sette mappe. Il corpo della PR dichiara *«validate_maps verde»* ed è vero.
Vuol dire «nessuno guarda più».

**Il gate ha trovato subito due casi già in `main`**: due master di ARC-09
(`…P1B-Cerchio-Treant-COMPLETO-maps` e `…P1C-Rituale-COMPLETO-SCALE`) che
generano **quattro mappe** in tutto e non avevano un solo SVG. Erano fuori
controllo da sempre.

## Decisione

### 1. `⛰` entra in `WALL_SYMS`

Una cresta rocciosa blocca la vista e il movimento. La regola d'arbitrato della
spec lo diceva già — *«una cella occupata da roccia, edificio, torre o statua è
impenetrabile e opaca»* — e il codice non la seguiva.

`🪨` (rocce/macerie) resta **fuori**, ed è corretto: è copertura **parziale**
(+4 CA, terreno difficile), non totale. La distinzione fra i due è il motivo per
cui questo non è un fix da fare a occhio.

Nessun artefatto versionato cambia: i `.uvtt` non sono committati per
convenzione, e i due che esistono (`tarsilia-*`) non contengono `⛰`.

### 2. Un master che genera mappe e non ha SVG è un errore

Quinto controllo in `validate_maps.py`, **bloccante**. Con una via d'uscita
dichiarata:

```
<!-- validate_maps: non-renderizzato — <motivo> -->
```

Il marcatore sta **nel testo del master**, non in una lista altrove. È la
lezione di ADR-0041: una lista in un altro file si stacca dalla realtà
esattamente come si era staccato l'elenco delle skill in `AGENTS.md`. Chi
cancella il master porta via anche la sua dichiarazione.

### 3. Il renderer e l'export devono restare d'accordo

Un test lega le due parti: **ogni simbolo che il renderer tratta come
riempimento pesante (`HEAVY_PATS`) dev'essere un muro nell'export**. È la
condizione che era violata, e adesso se qualcuno aggiunge un pattern pesante e
si scorda `WALL_SYMS`, la CI lo prende.

### 4. Le quattro mappe trovate si renderizzano

I due master di ARC-09 hanno ora i loro SVG (**31 SVG / 17 master**, erano 27 e
15). Non sono stati dichiarati KO: sono mappe tattiche vere di un arco vero, e
la ragione per cui non erano renderizzate è che **nessuno se n'era accorto**.

## Conseguenze

**Positive.**

- Le montagne bloccano la vista in Foundry. Un assedio giocato su mappa
  importata smette di avere arcieri che sparano attraverso una cresta.
- Nessun master può più uscire dalla validazione in silenzio: **la PR #63 non
  può più cancellare quei sette SVG senza dichiararlo**, che è il prerequisito
  che la Fase 0 di `PIANO-RIPRESA-PR-ABBANDONATE` chiedeva.
- Quattro mappe che nessuno aveva mai renderizzato adesso esistono come
  artefatto.

**Negative, e vanno dette.**

- **Il muro delle montagne è binario, e la montagna non lo è.** Un valico, una
  sella, un sentiero fra due creste sono attraversabili nella finzione e adesso
  sono muro nell'export. Chi disegna una mappa con un passo deve usare un
  simbolo di terreno per il passo, non `⛰`. Prima il difetto era «si passa
  ovunque»; adesso è «non si passa da nessuna parte», ed è il meno sbagliato
  dei due, non il giusto.
- **`extract_walls` è più lenta** su mappe con molta montagna, e la
  `hammerfist-L2-assedio` ne ha 1.800 celle. Misurato: resta sotto il secondo,
  ma non è gratis.
- **Il gate nuovo non dice se la mappa è buona**, solo se esiste. Renderizzando
  i quattro SVG di ARC-09 è emerso un difetto di contenuto in uno dei master
  (`…P1C` mappa 3 dichiara 40×40 e ha 26×29 celle): il renderer lo **avvisa** e
  disegna lo stesso. Non l'ho corretto — la griglia è contenuto, e ridisegnarla
  è una decisione del DM, non una conseguenza di questo ADR.
- **La via d'uscita si può usare per zittire il gate.** Un
  `<!-- validate_maps: non-renderizzato -->` senza motivo passa. Il motivo è
  obbligatorio nella forma scritta qui, ma nessuno lo verifica: è una
  convenzione, non un vincolo.

## Alternative scartate

**Trattare `⛰` come copertura parziale, come `🪨`.** Sarebbe coerente con
l'idea che una montagna si aggira — ma il renderer la disegna solida, e il
disaccordo fra quello che si vede e quello che si esporta è **il difetto
originale**, non la sua soluzione. Se un giorno serve la montagna aggirabile,
serve un simbolo per il valico, non un'ambiguità in più su `⛰`.

**Una lista di master esentati dentro `validate_maps.py`.** È come ci si è
arrivati la prima volta: la nota nel docstring parlava delle «righe KO di
`MAPPE-CENSIMENTO.md`», e nessuno l'aveva mai messa in codice. Una lista fuori
dal file che governa **è** il modo in cui i documenti si staccano dalla realtà.

**Rendere il controllo non bloccante per la prima passata.** Contro la regola
già scritta: *nessun gate nuovo nasce non bloccante*. E qui i due casi trovati
erano due, non duecento: il costo del blocco è stato renderizzare quattro SVG.
