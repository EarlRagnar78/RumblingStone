# Il corpus: le incoerenze di storia che il progetto ha già trovato

Forma: riferimento. Fonte delle righe: §1 «Lotto A» dei tre piani di
revisione (`plans/PIANO-REVISIONE-ARC07-…`, `…ARC08-…`, `…ARC09-…`, tutti del
2026-07-02) più quattro correzioni del DM registrate dopo. Sono difetti veri,
trovati da letture a mano e corretti. La domanda per ognuno: **quale
strumento deterministico lo avrebbe preso, e che cosa gli serviva?**

Le classi:

| classe | vuol dire |
|---|---|
| **K0** | lo prende già un cancello di oggi (dopo che il DM ha deciso la forma giusta) |
| **K1** | lo prende il prototipo `verifica_storia.py`, con l'àncora in `state.yaml` |
| **K2** | deterministico, ma il fatto non è strutturato: servirebbe un campo nuovo in `state.yaml` e una regola |
| **K3** | serve capire la prosa o giudicare: struttura dei file, intenzione, semantica |
| **F** | non è coerenza della storia (igiene dei file, lingua, nomi di file) |

## ARC-07 (piano del 2026-07-02, §1)

| id | difetto | classe | chi lo prende / che cosa manca |
|---|---|---|---|
| A1 | il drago con tre nomi (Skulldark, Skullcrusher, Infernotooth) | K0 | `validate_modules.CANONE_DEPRECATO`, foglio di stile del glossario §8 |
| A2 | profondità del viaggio: 1.000, 500, 2.372 anni | K2 | nessun campo «anni del viaggio» in `state.yaml` |
| A3 | P6 mette in scena una battaglia del 1372 superata | K3 | è una generazione di file, non un valore |
| A4 | gemme: il Rubino apre il portale contro Topazio+Smeraldo | K3 | una sequenza di eventi scritta in prosa («quando Rubino attiva → portale aperto») |
| A5 | livello del party 12, 13, 14 nei file dell'arco | K1 | regola S4. **Replay: 0 righe su 4** (titolo senza soggetto, «PCs» in inglese, riga con →) |
| A6 | generazioni P3B/P4/P5 mai riconciliate | K3 | scelta del master |
| A7 | file vuoto, temporaneo, coda AI | F | |
| A8 | `DC` inglesi | F | `validate_lingua` |
| A9 | P3B si gioca dopo P4, nessuno lo dice | K3 | ordine di lettura |
| A10 | Devastation Gauntlets contro Cintura, copie divergenti | K0 + K3 | il nome si mette nel foglio di stile; le copie sono struttura |
| A11 | il cane di Hella: Nymeria contro Durik | K0 | `CANONE_DEPRECATO` |

## ARC-08 (piano del 2026-07-02, §1)

| id | difetto | classe | chi lo prende / che cosa manca |
|---|---|---|---|
| A0 | `state.md` scritto in avanti: il futuro come passato | K0 | `validate_state`: il tempo è obbligatorio (ADR-0050, R3-R5) |
| A1 | la sorte di Fauci in quattro versioni, tutte come fatto | K2 | `coerenza_campagna` legge «è morto/sopravvive» solo in frase piana; manca la regola «un arco `preparato` non ha esiti affermati» |
| A2 | perdite dell'orda: −500 contro −900 | K2 | i numeri di §2 di `state.md` sono prosa, non campi |
| A3 | «abbastanza per portare i PG da 13° a 15°» | K3 | una promessa, non una dichiarazione di livello |
| A4 | scala delle mappe 3 m contro 1,5 m | K0 | `qualita_mappe` («scala/dichiarata»), ADR-0106 |
| A5 | terminologia 5e | F | |
| A6 | stub che inventano luoghi (Castle Red, River Styx) | K2 | servirebbe un gazzettino dei luoghi; i nomi propri nuovi sono troppi per un elenco chiuso |
| A7 | code AI | F | |
| A8 | quattro generazioni dell'atlante | K3 | |
| A9 | nomi dei file | F | |
| A10 | Thorin / Thorik / Thorek nello stesso file | K3 | sono tre personaggi veri: un foglio di stile non distingue il refuso dal nome giusto |
| A11 | due comandi elfici (Lunapiena, Lythiel) | K3 | |
| A12 | «la Forgia ricorda le ferite» promesso e mai implementato | K2 | lo prende S7 solo se la promessa è un'eco di §7.E; allora non lo era |

## ARC-09 (piano del 2026-07-02, §1)

| id | difetto | classe | chi lo prende / che cosa manca |
|---|---|---|---|
| A1 | Regiarix contro Regiarax | K0 | foglio di stile §8 |
| A2 | arrivo dell'orda: Giorno 38, 40, 42 | K1 | regola S1. **Replay: 2 righe su 4 al giro 2, 4 su 4 al giro 3**; e il residuo in `DM-CAMPAIGN-PLAYBOOK.md` §6, mai corretto, c'è ancora su main |
| A3 | finestre delle quest nell'INDICE contro `state.md` §0 | K1 | regola S3. **Replay: 0 su 3 al giro 2, 3 su 3 al giro 3** |
| A4 | nomi di PG usati per PNG («Tordek Tozzefort») | K2 | un registro «nome di PG + cognome che non è il suo»; non scritto |
| A5 | numeri del Ghostlord fuori dal rescale v2 | K2 | i numeri delle armate non sono campi |
| A6 | alleati elfi e nani: numeri diversi | K2 | come A5 |
| A7 | Tyrgarun: colore, età, GS | K0 parziale | `coerenza_campagna` legge GS ed età; il colore no |
| A8 | file citati come fonte che non esistono | K0 | `validate_docs` |
| A9 | file vuoto, file «da integrare» | F | |
| A10 | «costruire un Fane» che esiste già | K3 | |
| A11 | due fazioni fuse nell'INDICE | K3 | |
| A12 | file legacy con canone superato | K3 | |
| A13 | «Rethman» | K0 parziale | non è nel foglio di stile §8; oggi resta solo nello storico |

## Correzioni del DM dopo i piani

| id | difetto | classe | chi lo prende / che cosa manca |
|---|---|---|---|
| X1 | il pegno del Rituale 3 attribuito a Tordek (corretto il 2026-08-06) | K3 | **l'errore era nell'àncora**: un verificatore che si fida di `state` non lo vede |
| X2 | sei righe «Thorik −2 COS» contro `state` (corretto il 2026-09-19, b4f42f37) | K1 | regola S6. **Replay: 3 righe su 6**, il difetto si vede |
| X3 | eco E-07e registrata senza una scelta del PG | K3 | |
| X4 | sergenti hobgoblin e guardie nere con due schede (lotto 7c) | K0 | `coerenza_campagna fatti` |

## Il conto

| classe | righe | quota |
|---|---:|---:|
| K0 (c'è già) | 10 (con i parziali A10 di ARC-07, A7 e A13 di ARC-09) | 29% |
| K1 (il prototipo, con l'àncora) | 4 | 11% |
| K2 (servirebbe strutturare un fatto) | 8 | 23% |
| K3 (serve capire o giudicare) | 13 | 37% |
| F (non è storia) | 6 | — |

Su 35 difetti di storia (senza F), la regola con l'àncora ne aggiunge **4**
a quelli che i cancelli di oggi già prendono: A5, A2, A3, X2. Di questi, al
replay su commit che il prototipo non aveva visto (A5, X2), uno sfugge del
tutto (A5, 0 righe su 4) e uno si vede per metà (X2, 3 su 6). A2 e A3 sono
presi per intero solo dopo aver tarato il prototipo proprio su quel replay
(giro 3), quindi non contano come prova indipendente.
