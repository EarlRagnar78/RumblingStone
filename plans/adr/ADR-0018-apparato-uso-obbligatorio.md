# ADR-0018 — L'apparato d'uso è parte del contenuto, non un extra

**Stato**: accettata
**Data**: 2026-08-15
**Decisione-fonte**: audit del DM del 2026-08-15 — *«un master ha tutto sotto
controllo o ha bisogno di un'AI per andare avanti? cosa manca davvero per rendere
questo modulo e la campagna memorabili da giocare e belli da masterizzare?»* —
e la ricerca che ne è nata
([`RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE`](../RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md)).

## Contesto

Il repo sapeva già fare tre cose bene: **scrivere** contenuto
(`rumblingstone-narrative-style`), **strutturarlo in profondità**
(`rumblingstone-module-standard`), **validarlo a macchina** (`validate_*`).

L'audit ha trovato che mancava la quarta, ed era quella che si vede al tavolo. Il
`Drappo di Tarsilia` aveva 3.600 righe di contenuto e un DM che lo apriva avrebbe
comunque dovuto:

- cercare in cinque file chi fosse l'ostessa mentre sei persone aspettavano;
- decidere a occhio come si pronuncia *Iomedae*, e quindi smettere di usare il nome;
- leggere i read-aloud **a freddo davanti al tavolo**, che è il modo per farli
  suonare male;
- improvvisare l'atmosfera sonora, che la `module-standard` chiedeva già («cue
  musicali») e che **nessun file del repo ha mai prodotto**;
- descrivere a voce un contratto, un registro e una ricevuta invece di **darli in
  mano** — mentre i template Homebrewery per farlo esistevano da mesi, inutilizzati.

Il difetto non era di scrittura. Era che **le sei pagine che nessuno legge per
piacere non erano considerate parte del lavoro**.

## Decisione

**L'apparato d'uso è obbligatorio quanto il contenuto.** Un beat, un arco o un modulo
non è finito finché non ha, in un unico file consultabile:

| # | Elemento | Perché è obbligatorio |
|---|---|---|
| 1 | **Foglio del cast** — ogni PNG in una riga: ruolo, cosa vuole, **il tic vocale**, dove si trova | il DM cerca invece di raccontare. Il tic è la parte che rende un PNG riconoscibile senza fare accenti |
| 2 | **Guida alla pronuncia** dei nomi non ovvi | un nome su cui il DM esita è un nome che sparisce dal gioco |
| 3 | **Indice dei read-aloud** in ordine di gioco, con la lunghezza | si leggono **prima, ad alta voce**: è l'unico modo perché funzionino |
| 4 | **Inserto per lo schermo** — una pagina con tutte le CD e le soglie | il §CD sparso nei file non è consultabile a metà di un round |
| 5 | **Cue sonori** — descrizioni, non titoli di brani | il moltiplicatore d'atmosfera più economico che esista. **E si spengono nei momenti importanti, non si alzano** |
| 6 | **Il momento da fotografare** — uno per sessione, dichiarato | un beat che non sa qual è il suo picco lo brucia correndo |
| 7 | **Prop fisici** per ogni documento che la fiction consegna | un foglio che passa di mano vale dieci minuti di descrizione |
| 8 | **Nota di accessibilità** | daltonismo, dislessia, carico cognitivo, sicurezza emotiva. Riguarda più tavoli di quanto sembri |
| 9 | **Memoria fra le sessioni** — contatori, patti, scelte, **Echo Ledger** | senza, gli echi non tornano mai e i patti si dimenticano |

### La regola dei prop

**Ogni documento che la fiction consegna, si consegna davvero.** Se un PNG posa un
contratto sul tavolo, quel contratto esiste come file stampabile. I template stanno
in `campaign/templates/homebrew/` e non erano mai stati usati: da oggi il loro uso
non è un vezzo, è il modo normale di consegnare un documento.

Il prop porta con sé una **nota per il DM che non si stampa**, in coda al file: come
si usa, cosa nessuno nota, cosa succede se lo firmano/stracciano/perdono.

### La regola dei suoni

Descrizioni (*«un tamburo solo, lento, e poi stop netto sul nome»*), mai titoli di
brani: ognuno usa quello che ha, e il file non invecchia con le piattaforme.

## Ambito — vale per il modulo **e** per la campagna

| Elemento | Modulo standalone | Campagna |
|---|---|---|
| 1-6, 8 | **obbligatori** (gate: `validate_standalone.py` per la presenza della guida) | **obbligatori sui nuovi consolidamenti** `ARC*-DEF-*` |
| 7 (prop) | obbligatorio | obbligatorio |
| 9 (memoria) | `STATO-DEL-MODULO.md` | già coperto meglio da `state.md` + ADR-0007: **non si duplica** |

⚠️ **I cinque master `ARC*-DEF-*` esistenti non vengono riscritti retroattivamente.**
L'obbligo vale dal prossimo consolidamento. Un gate a macchina su di essi li farebbe
fallire tutti e cinque, e un gate che fallisce sempre viene disattivato entro una
settimana: `validate_modules.py` resta com'è, e l'asticella vive nella skill.

## Conseguenze

- Più facile: un DM che non ha scritto il modulo può giocarlo dopo
  **quarantacinque minuti** di preparazione, con due file aperti invece di nove.
- Più facile: i giocatori si portano a casa **oggetti**, che è quello che ricordano
  a distanza di un anno.
- Più difficile / rinunce: ogni beat costa **sei-otto pagine in più** che non sono
  narrativa. Chi le scrive non si diverte. Si scrivono lo stesso.
- Debito accettato: i cinque master esistenti restano senza apparato finché non
  passano di mano per altri motivi.
- Da rivisitare: dopo **due tavoli veri**. Se il debrief del DM
  (`rumblingstone-playtest` §5) misura zero improvvisazioni strutturali e meno di
  cinque ricerche sopra i trenta secondi a serata, l'apparato funziona. Se no, la
  lista del §Decisione va cambiata **sui dati**, non a intuito.

## Copertura

- `skills/rumblingstone-module-standard/SKILL.md` §15 — l'obbligo, nella checklist
- `skills/rumblingstone-playtest/SKILL.md` — come si misura se funziona
- `STANDALONE-Il-Drappo-di-Tarsilia/08-CASSETTA-DEL-DM.md` — implementazione di
  riferimento dei punti 1-6 e 8
- `STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/handout/` — i prop (punto 7)
- `STANDALONE-Il-Drappo-di-Tarsilia/STATO-DEL-MODULO.md` — la memoria (punto 9)
- [ADR-0014](ADR-0014-regia-sensoriale-obbligatoria.md) — la regia delle sequenze a
  battute, di cui questo ADR è il completamento fuori dalla scena
