# Coerenza della storia con un verificatore deterministico: esito della misura

Forma: spiegazione. Data: 2026-11-12. Decisione che ne segue:
[ADR-0125](../../adr/ADR-0125-la-coerenza-della-storia-si-verifica-contro-state-yaml-solo-sui-fatti-strutturati.md).

## La domanda

Il DM, l'11 novembre, nel thread della verifica delle regole (#378): l'idea di
partenza (un verificatore deterministico che rimanda all'LLM la regola violata
o il controesempio perché si corregga) ha senso per la generazione e la
coerenza della **storia**?

## In breve

Sì, ma per una parte piccola: **i fatti che `campaign/state.yaml` ha già come
campi** (giorni della marcia, livello per arco, portatori degli artefatti,
modifiche permanenti dei PG, echi armati). Lì il verificatore ha un'àncora, e
quindi può dire non solo «qui c'è un 40 e là un 42» (lo fa già
`coerenza_campagna`) ma «atteso 42, trovato 40, `file:riga`». Fuori da quei
campi non ha niente da confrontare, e dentro quei campi vede la frase scritta
come la scrive uno script, non come la scrive un autore.

| misura | risultato |
|---|---|
| difetti storici che aggiunge ai cancelli di oggi | **4 su 35** (A5 ARC-07, A2 e A3 ARC-09, le sei righe «−2 COS») |
| replay su commit mai visti (A5, −2 COS) | A5: **0 righe su 4**; −2 COS: **3 righe su 6**, difetto visto |
| mutanti in forma piana (19) | **18** presi; i cancelli di oggi **1** (S5-p3, da `coerenza_campagna`) |
| mutanti in parafrasi d'autore (18) | **1** preso; i cancelli di oggi 0 |
| precisione su main (dopo la taratura) | **7 su 13** (54%; Wilson 95% circa 29%-77%) |
| difetti nuovi trovati su main | 2 righe di `DM-CAMPAIGN-PLAYBOOK.md` §6 (Day 40 e Skull Gorge Day 5), residuo di A2 ARC-09 del 2 luglio; 5 file di ARC-09 tarati per PG di 11°-12° |
| «chi sa cosa» | **non verificabile**: 31 righe di §4 su 31 senza tempo |

## Che cosa esisteva già (e non si rifà)

- `scripts/coerenza_campagna.py fatti`: contraddizioni **prosa contro prosa**
  per entità (GS, pf, CA, CD, classi, titolo, età, vivo/morto, portatore,
  giorno). Cancello in CI su ARC-07 e ARC-08, 0 residui. Precisione 6 su 6
  sul lotto 7c.
- `scripts/validate_state.py`: schema e regole R1-R13 di `state.yaml`; rende
  impossibile scrivere un fatto **senza dire a quale tempo appartiene** (nato
  da A0 di ARC-08).
- Il foglio di stile del glossario §8 (`validate_prosa`) e
  `validate_modules.CANONE_DEPRECATO`: i nomi superati (Regiarax, Hellas,
  Skulldark, Nymeria).
- `fronti` di `coerenza_campagna`: F4 controlla che ogni presagio compaia in un
  master (è la stessa idea di S7, per i fronti).
- NLI (mDeBERTa) per le contraddizioni fra file: già provata e **non adottata**
  (`plans/RICERCA-GUARDRAIL-E-TECNICHE-2026-11.md` §26: 28 delle prime 30 sono
  rumore).

## Il banco

1. **Corpus storico** ([CORPUS.md](CORPUS.md)): 35 incoerenze di storia vere,
   dai tre piani di revisione del 2026-07-02 e da quattro correzioni del DM,
   ognuna classificata per lo strumento che l'avrebbe presa.
2. **Prototipo** ([verifica_storia.py](verifica_storia.py)): sette regole che
   leggono un campo di `state.yaml` e lo cercano in prosa, con le esclusioni
   di `coerenza_campagna` (archivi, errata, righe di storico) e un condizionale
   stretto. Uscita: `regola`, `atteso`, `ha`, `file`, `riga`.
3. **Replay** (`replay/`): il prototipo sui commit **prima** delle
   correzioni, con l'àncora che il canone aveva allora (state.md del commit,
   oppure lo `state.yaml` del commit per le «−2 COS»).
4. **Mutanti** ([muta.py](muta.py), `misure/mutanti.json`): 37 righe false
   inserite una alla volta in file veri, metà in forma piana e metà come le
   scriverebbe un autore; per ognuna si chiede al prototipo, a
   `coerenza_campagna fatti` e a `validate_state`.
5. **Precisione su main** (`misure/main-giro*.json`): ogni rilievo letto
   nel file.

## I numeri, regola per regola

| regola | mutanti piani | parafrasi | main (veri/rilievi) | replay |
|---|---:|---:|---|---|
| S1 arrivo dell'orda | 3/3 | 0/3 | 1/1 (prima della correzione del playbook) | A2: 2/4 al giro 2, 4/4 al giro 3 |
| S2 giorni dei waypoint | 3/3 | 0/3 | 1/4 (più un dubbio, Vraath al Day 1) | — |
| S3 finestre delle quest | 2/3 | 0/3 | 0/3 | A3: 0/3 al giro 2, 3/3 al giro 3 |
| S4 livello del party | 3/3 | 1/3 | 5/5 | A5: 0/4; −2 COS: 2 falsi |
| S5 portatore | 3/3 | 0/3 | nessun rilievo | — |
| S6 modifiche permanenti | 3/3 | 0/3 | nessun rilievo | −2 COS: 3/6, nessun falso |
| S7 eco armata senza scena | 1/1 | — | nessun rilievo | — |

Precisione su main per giro: 7 su 17 al giro 1, 7 su 11 al giro 2, 7 su 13
al giro 3. Il giro 3 aggiunge il titolo di sezione come contesto e legge i
blocchi di cronologia: prende per intero A2 e A3 del replay e porta 2 falsi
nuovi su main (il Palio nominato sotto il titolo del Torneo).

## Onestà sul banco

- **Il giro 3 è tarato sul replay di ARC-09.** I suoi 4/4 e 3/3 non sono una
  prova indipendente; lo sono A5 (0/4) e le «−2 COS» (3/6), che il prototipo
  non aveva visto.
- **I mutanti piani li ho scritti io, sapendo come cerca il prototipo.** Il
  18/19 è un tetto, non una stima del richiamo vero. La stima vera è più
  vicina a quella delle parafrasi (1/18) e del replay mai visto.
- **S7 e `validate_state`**: al primo giro del banco `validate_state` bocciava
  il mutante di S7, ma per un `fatto` di 7 caratteri (minLength 10), non per la
  scena mancante. Rifatto con testi lunghi: `validate_state` lo passa,
  `verifica_storia` lo segnala. Annotato nel JSON.
- **L'àncora può essere sbagliata.** Il pegno del Rituale 3 (corretto il
  2026-08-06) era sbagliato proprio in `state`: un verificatore che si fida
  dell'àncora lo avrebbe difeso.
- **Il ciclo di autocorrezione dell'LLM non è misurato.** Come in ADR-0124 c'è
  solo il fatto meccanico: per S1, S2 e S6 sostituire `ha` con `atteso` sulla
  riga chiude la violazione. Per S4 no: un incontro tarato per l'11° non si
  corregge cambiando il numero nel testo.
- **Il limite dichiarato dal thread della #378 è confermato e misurato**: la
  parte difficile è estrarre il fatto dalla prosa (1 parafrasi su 18), non
  ragionarci sopra. Nessuna delle 35 incoerenze storiche richiedeva una
  regola ricorsiva o temporale: richiedeva di **leggere** il fatto.

## Prolog, clingo, NLI

Non rimisurati. La condizione di ADR-0124 per riaprirli («regole davvero
ricorsive o temporali su fatti già strutturati, per esempio §4 con una colonna
Tempo») non c'è: §4 ha 31 righe su 31 senza tempo, e le regole che servono
sono uguaglianze e intervalli. L'NLI è già stata misurata e scartata sui file
del repo.

## Che cosa ho corretto

Il residuo di A2 ARC-09 trovato su main, perché allinea il testo a una
decisione già presa (Day 42, `state.yaml` `march_clock`) e non tocca canone:

- `campaign/DM-CAMPAIGN-PLAYBOOK.md` §5 e §6: «Target Day 40», «Day 1 → Day
  40», «Day 5 Skull Gorge», «Day 40 Orda arriva» → Day 42 e Day 8-9;
- `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md` r.5: «Day 1→40»
  → «Day 1→42» (riga che il prototipo **non** vedeva: l'ho trovata leggendo
  il file).

## Che cosa va al DM

1. **I cinque file di ARC-09 tarati per PG di 11°-12°** (P1A r.52, P1B r.10,
   Torre P1 r.15, Torneo STATBLOCCHI r.8, Sabotaggio Upscale r.7) contro il
   13° di `state.yaml`. Non li ho toccati: cambiare il numero senza riscalare
   l'incontro scriverebbe una falsità. Da decidere: riscalare, oppure
   dichiarare «progettato per l'11°-12°, da riscalare».
2. **Vraath al Day 1** in ARMATE-SYNC r.11 («Baseline Orda al Day 1 (Vraath
   Keep)») contro `state.yaml` (Day 1 il Fane, Day 6 Vraath): può essere il
   raduno di RHoD, può essere un errore.
3. ~~Se promuovere il prototipo~~ **Deciso il 2026-11-12** (card «Solo le
   regole precise, in testing»): S1, S5, S6 e S7 sono in
   `scripts/coerenza_campagna.py fatti --state` e via MCP. Sui 9 mutanti piani
   di S1, S5 e S6 il codice promosso prende gli stessi 9 del prototipo, sulle 9
   parafrasi nessuno; sul replay delle «−2 COS» le stesse 3 righe su 6; su main
   0 violazioni. S2, S3 e S4 restano qui.

## Aggiunta del 2026-11-13: S8, le tattiche contro la scheda

Regola in `scripts/coerenza_campagna.py fatti --tattiche`, banco in
`muta_tattiche.py`, esiti in `misure/mutanti-tattiche.json`. L'àncora è la
scheda (`verifica_scheda --fatti`, PR #393), non `state.yaml`.

| Famiglia di mutanti | Mutanti | Visti |
|---|---|---|
| La scheda perde l'incantesimo o il talento che la tattica usa | 206 | 204 |
| La tattica usa un incantesimo (corsivo) o un talento (maiuscole) che la scheda non ha | 195 | 193 |
| Parafrasi: talento di più parole in minuscolo | 65 | 65 |
| Parafrasi: incantesimo senza corsivo | 65 | 0 |
| Parafrasi: talento di una parola in minuscolo | 65 | 0 |
| Controllo: scambio fra due incantesimi della scheda (non va segnalato) | 29 | 0 |

Dal lotto 5, terza parte, di ADR-0126 (2026-11-13, su 9f019c18): 0 violazioni
su 246 menzioni in 65 schede; 178 file senza «Tattiche» non si giudicano. Prima
(3cc11aee) erano 220 menzioni in 60 schede, con 5 file saltati per «più
schede»: non ne avevano due, la seconda riga «Talenti» era una nota o la stessa
scheda riscritta, e ora `--fatti` li dà come un blocco solo. I numeri del banco
di prima: 181 su 183, 178 su 180, 60 su 60, 0 su 60, 0 su 60, 0 su 26. Il banco gira in circa
tre minuti. I quattro mutanti non visti hanno un nome che la scheda scrive
anche per altro («velocita: 9 m» nel frontmatter, «fendere»).

I mutanti usano il dizionario della regola: dicono che la regola fa ciò che
dichiara, non quanto spesso un autore sbaglia così. Su main non c'è nessun
errore vero di questo tipo, quindi il valore oggi è di guardia sulle schede
che cambiano (i lotti di ADR-0126 tolgono e aggiungono talenti e incantesimi).
