# Secondo giro sui cinque master di ARC-07, dopo il rifacimento

Il DM, dopo l'unione della PR #245: *«rifacciamo i DEF dell'Arco 07 così
possiamo misurare il miglioramento e finire completando i DEF con i giri di
playtester, DM e developer, con le aggiunte e le mappe, con tutto quello
aggiornato, e lo stile e le strutture»*.

Il lavoro ha avuto due tempi.

1. **Il rifacimento.** I cinque master sono stati riscritti nello stile di
   `rumblingstone-narrative-style` (tetti di `read-aloud-adulti.md`, battute
   brevi, chiusura su «Che fate?») e nella struttura di
   `rumblingstone-module-standard` (§9-§16 della #244), senza toccare il canone
   né gli statblocchi appena verificati sull'SRD. L'Atlante delle mappe è stato
   riallineato ai master. Il punto di partenza è il tag
   `prima-rifacimento-arc07` (`503c9fde`).
2. **Il giro.** Sui master rifatti hanno letto di nuovo un developer, un
   playtester e un DM a freddo per ogni DEF, quindici letture con le stesse
   rubriche del primo giro. Poi un correttore per DEF, un verificatore nuovo e
   una seconda passata del correttore, come nel primo giro. In più i lettori
   avevano i mirror dell'SRD 3.5 per controllare le regole.

## Il giro, a confronto con il primo

In 🔴·🟠·🟡, somma dei tre lettori, prima di togliere i doppi:

| Master | Primo giro (master di partenza) | Secondo giro (master rifatto) | 🔴+🟠 |
|---|---|---|---:|
| DEF-1 | 2·40·54 | 3·18·47 | 42 → 21 |
| DEF-2 | 0·19·46 | 0·15·34 | 19 → 15 |
| DEF-3 | 0·28·54 | 0·19·49 | 28 → 19 |
| DEF-4 | 0·17·55 | 2·18·33 | 17 → 20 |
| DEF-5 | 0·14·39 | 1·13·35 | 14 → 14 |
| **Totale** | **2·118·248** | **6·83·198** | **120 → 104** |

⚠️ **I 🔴 salgono da 2 a 6, e va detto perché.** Sono tre difetti distinti,
contati più volte da lettori diversi. **Tutti e tre c'erano già** nel master
di partenza, e il primo giro non li aveva visti:

- in DEF-1 gli Xorn emergevano, mordevano e si rituffavano nello stesso turno,
  cosa che in 3.5 non si può fare senza Attacco Rapido (tre lettori);
- in DEF-4 il fondo buio della tenda dava occultamento contro guardie con
  scurovisione (due lettori);
- in DEF-5 mancava la CA di Re Thorek, l'unico bersaglio della scena (un
  lettore).

Li hanno trovati perché questa volta avevano l'SRD da consultare. Sono tutti
corretti: gli Xorn seguono l'SRD, la tenda e la sua legenda in M7-C danno
copertura solo dietro il palo, la tavola e il seggio, e la CA del re è presa
dalla Guida DM dell'arco 08, con la scelta fra le due versioni lasciata al DM.

DEF-4 è l'unico master che sale anche nei 🔴+🟠: il rifacimento non ne ha
cambiato la struttura, e i lettori hanno trovato soprattutto regole del duello
col drago. DEF-5 resta pari.

Dopo la correzione e la verifica:

| Master | Corretti | Al DM | Respinti | Verifica: chiusi · parziali · aperti · al DM | Nuovi dalla verifica | Seconda passata |
|---|---:|---:|---:|---|---|---|
| DEF-1 | 30 | 11 | 2 | 11 · 1 · 0 · 9 | 🟠 1 · 🟡 2 | tutti chiusi |
| DEF-2 | 18 | 12 | 4 | 8 · 2 · 0 · 5 | 🟡 4 | 4 corretti, 2 al DM |
| DEF-3 | 16 | 13 | 1 | 7 · 3 · 0 · 9 | 🟠 1 · 🟡 4 | tutti chiusi |
| DEF-4 | 8 | 9 | 0 | 6 · 4 · 0 · 10 | 🟡 4 | chiusi, due in parte |
| DEF-5 | 11 | 9 | 1 | 5 · 1 · 0 · 8 | 🟡 3 | tutti chiusi |

Nessun rilievo è rimasto aperto. Quelli che toccano il canone o il
bilanciamento sono raccolti in [`DECISIONI-DM.md`](DECISIONI-DM.md), senza i
doppioni e controllati contro il canone giocato del ramo di gruppo.

## Le misure, prima e dopo il rifacimento

Stessi comandi sul tag `prima-rifacimento-arc07` e sul ramo dopo il giro. Le
uscite intere sono in `misure/`.

**Box contro i tetti** (`misura_craft --box`), somma dei cinque master:

| | Prima | Dopo |
|---|---:|---:|
| Box | 108 | 142 |
| Oltre 12 righe | 0 | 0 |
| Con parentesi | 7 | 0 |
| Più di un nome proprio | 27 | 1 |
| Più di 4 frasi | 62 | 13 |
| Oltre 500 caratteri | 28 | 0 |

**La prosa dei box** (`box_metri` e `misura_craft --stile` della #246):

| | Prima | Dopo |
|---|---:|---:|
| Parole per box, mediana | 66 | 51 |
| Box oltre 100 parole | 21 | 0 |
| Box fra 30 e 70 parole | 53 su 107 | 125 su 142 |
| Sensi per box, mediana | 1 | 2 |
| Parole ripetute a meno di 20 parole, per box | 1,0 | 0,5 |
| Battute dei PNG oltre 25 parole | 9 | 0 |
| Battute oltre 40 parole | 5 | 0 |

**MQM** (`punteggio_mqm.py`): DEF-1 99,51 → 100 · DEF-2 97,53 → 100 · DEF-3
98,76 → 100 · DEF-4 99,73 → 99,98 · DEF-5 99,87 → 99,91.

**I congegni** (`misura_craft`), somma dei cinque master:

| Congegno | Prima | Dopo |
|---|---:|---:|
| Chiusura su «Che fate?» | 13 | 30 |
| `[HDYWTDT]` ai punti di morte | 12 | 19 |
| *Yes-and with teeth* | 7 | 16 |
| Pilastro dichiarato | 46 | 141 |
| Regia etichettata | 51 | 120 |

Nessun indicatore peggiora. I box sono di più perché quelli lunghi sono stati
spezzati in battute.

## La prova che manca: il cieco

Le misure dicono che il testo rispetta le norme, non che si legge meglio. Per
quello serve il voto del DM alla cieca (ADR-0093, PR #246), sul campione dei
venti box congelato prima del rifacimento.

Due cose da sapere prima di votare:

- **quattro coppie su venti sono identiche**: quei box non sono cambiati, e lo
  strumento non le fa votare. Le coppie da votare sono **sedici**. Il criterio
  dell'ADR, 14 su 20, riportato alla stessa proporzione diventa **12 su 16**;
- **due coppie sono state ricomposte a mano** (la 3 e la 12). Il box vecchio è
  stato spezzato in più battute, e l'appaiamento automatico ne prendeva solo
  un pezzo: nella 3 metteva a confronto la battuta di Varis con la gemma, nella
  12 un box di sei righe con la sua prima riga. Ora il lato nuovo contiene
  tutte le battute che sostituiscono il box vecchio. Il difetto è
  dell'appaiamento di `cieco_versioni.py`, ed è annotato per la #246.

### L'esito: pari, il miglioramento non è dimostrato

Il DM ha votato le sedici coppie la sera stessa, dopo l'unione della PR #249.
La nuova versione ne vince **8**, la vecchia **8**, nessun pari. L'intervallo di
Wilson al 95% sulla quota della nuova è [0,28; 0,72]: contiene la metà, quindi
il voto non distingue le due versioni. La soglia era 12 su 16.

| Vince la vecchia | Vince la nuova |
|---|---|
| 2 · 3 · 4 · 5 · 9 · 12 · 16 · 20 | 6 · 7 · 8 · 10 · 11 · 13 · 17 · 18 |

Le misure del rifacimento restano vere: i box rispettano i tetti. Il cieco dice
che rispettarli non è bastato perché si leggano meglio. Le coppie perse hanno
due difetti in comune.

- **Dove la riscrittura ha tagliato il dettaglio che faceva l'immagine.** Nella
  2 il giardino perde «e dietro ognuna, un pensiero» e i cristalli che tengono
  ciascuno una nota. Nella 5 l'affresco perde Moradin, Frostforge e la Corona
  per nome: il tetto di un nome proprio nuovo per box li ha trasformati in «il
  dio dei nani», «il martello», «una corona». Sono nomi che i giocatori
  conoscono da archi interi, e non sono nuovi.
- **Dove un box è stato spezzato in battute** (3, 12). Lette di fila, le
  battute suonano meno di un box unico.

Vince la nuova dove la vecchia era lunga senza essere precisa: le battute dei
PNG (7, 8), i doni (10, 11), le scene di DEF-5 (17, 18).

La scheda, la chiave, i voti e l'esito sono in `misure/CIECO-*`.

## La varianza delle lunghezze, dal corpus

Dopo il giro, il corpus di 1.762 box scritti da persone (PR #250: Gruppo
Chimera in italiano, Paizo in inglese) ha trovato un difetto che le norme non
misuravano. I box rifatti erano **troppo regolari**: il 90% stava fra 30 e 70
parole, contro il 47% dei box umani, e mancavano quasi del tutto quelli
corti. Il DM ha approvato di adottare le misure del corpus.

Un passaggio per master ha variato le lunghezze secondo la funzione della
scena. Ha accorciato i box d'urto, di reazione e di passaggio. Ha unito in un
box lungo, fino a 100 parole e sempre entro le 12 righe, le battute
consecutive sullo stesso luogo. Il contenuto e i tetti non sono cambiati.

| | Corpus italiano | Prima della varianza | Dopo |
|---|---:|---:|---:|
| Box | 1.644 | 142 | 128 |
| Parole, primo quartile | 26 | 41,5 | 34 |
| Parole, mediana | 41 | 51 | 54 |
| Parole, terzo quartile | 64 | 62 | 69 |
| Box fra 30 e 70 parole | 47% | 88% | 54% |
| Chiusure su una domanda (corpus: il suo rilevatore; ARC-07: `misura_craft`, chiusura su «Che fate?») | 6,5% | 30 su 142 | 27 su 128 |

Le chiusure su domanda restano sopra il corpus, intorno al 21%, perché ADR-0014 le vuole su
ogni box che apre un combattimento o una scelta: i passaggi ne hanno tolte
solo dove il box era pura descrizione. Avverbi in -mente e gerundi in coda
restano molto sotto il corpus, sotto 1‰ contro 5,6‰ e 1,7‰: dove una frase li
voleva sono tornati, ma non se ne sono aggiunti per fare numero. Gli indicatori
`>4 frasi` e `>500 car` risalgono, da 13 a 30 e da 0 a 14, perché i box lunghi
li superano per costruzione; non sono tetti.

### Le scelte del DM, applicate

Il DM ha chiesto di applicare le sue scelte dove le ha fatte, e la stessa
lezione agli altri box.

- **Le otto coppie vinte dalla vecchia** tornano parola per parola. Dove un box
  supera un tetto, un commento lo marca come scelta del DM.
- **Le otto vinte dalla nuova** restano com'erano.
- **Gli altri box rifatti**, uno per uno contro la versione di partenza: sono
  tornati i dettagli sensoriali e i nomi già noti al tavolo (Moradin, Thorik,
  la Corona, Aegis Fang, il Cuore di Moradin, Hammerfist) al posto delle
  perifrasi. I monologhi spezzati in battute con incisi in corsivo sono di
  nuovo un discorso solo. Restano i tagli che funzionavano: niente maiuscole
  di enfasi, niente date, niente parentesi. Sono stati toccati circa settanta
  box su centoventi.

| | Dopo la varianza | Dopo le scelte del DM |
|---|---:|---:|
| Box | 128 | 120 |
| Parole, mediana (IQR) | 54 (34-69) | 61 (45-82) |
| Box oltre 100 parole | 0 | 18 |
| Box oltre 12 righe, con parentesi | 0, 0 | 0, 0 |
| Box con più di un nome (il metro conta anche i nomi noti) | 1 | 23 |
| Tag di canone, `[HDYWTDT]`, `[INFERRED]`, «Che fate?» | 476, 19, 5, 26 | uguali |

La misura dei box impoveriti della PR #246 (`ciclo_prosa.box_impoveriti`,
contro la versione di prima del rifacimento) ne trovava 26 su main; dopo le
scelte del DM ne restano 11, e una correzione mirata li porta a 2. I due sono
falsi positivi: la parola sensoriale c'è ancora, ma sta nella battuta del PNG
che ora è fuori dal box.

Il ritorno dei nomi noti è una lettura della norma (§2-ter della #246: il tetto
di un nome proprio vale per i nomi nuovi), non un voto del DM. Il cieco su
questo è diviso: Moradin in perifrasi perde nella coppia 5, ma il drago senza
nome vince nella 6 e «la druida» al posto di Hella nella 10.

I box sopra le 100 parole tornano perché sono i lunghi che il DM ha preferito,
sempre entro le 12 righe. L'indicatore «più di un nome» sale perché
`misura_craft` conta i nomi distinti, non quelli nuovi: i ventitré sono
quasi tutti nomi che il tavolo conosce. Per sapere se la passata sugli altri box
si legge meglio serve un altro cieco, su un campione nuovo.

