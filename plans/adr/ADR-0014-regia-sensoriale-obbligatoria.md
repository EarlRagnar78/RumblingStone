# ADR-0014 — Regia sensoriale obbligatoria: nessuna meccanica senza descrizione, nessuna stanza descritta da un architetto

**Stato**: accettata
**Data**: 2026-07-30
**Decisione-fonte**: review DM del master ARC07-DEF-1 (2026-07-30) —
«queste descrizioni devono essere presenti sempre altrimenti i giocatori si
perderanno sempre qualcosa» + «le descrizioni delle stanze non devono essere
fatte da architetti con misure precise ma da avventurieri con occhio
esperto». Attuazione: lotto K-B12 del piano DM-TOOLKIT.

## Contesto

I master del repo hanno meccaniche eccellenti — round-per-round, CD, soglie,
contingenze — ma in due punti lasciavano il DM (e quindi i giocatori) senza
appigli:

1. **Sequenze a battute senza regia.** Il rituale dello Smeraldo (§9 Fase 2)
   elencava con precisione cosa devono tirare Thorik, Tordek e Artemis, ma
   non diceva **cosa vedono, sentono e percepiscono** mentre lo fanno. Al
   tavolo i tre agiscono *insieme* ma parlano *uno alla volta*: senza una
   descrizione per battuta si tirano dadi al buio, e il pathos di una scena
   costruita per mesi evapora in tre tiri.
2. **Ingressi non descritti.** La camera del boss non diceva *come* ci si
   entra né *cosa si vede appena dentro*: il DM doveva improvvisare il beat
   più importante della serata.
3. **Descrizioni da perizia tecnica.** Dove la descrizione c'era, spesso
   apriva con metrature («camera sferica Ø 60 m, piattaforma 6 m»): dati
   utili al DM, inutili — anzi, dannosi — se letti ai giocatori.

## Decisione

**Ogni sequenza meccanica ha la sua regia, e ogni luogo si descrive con
l'occhio di un avventuriero, non con la squadra di un architetto.**

### 1. Nessuna sequenza a battute senza regia

Dove esiste un giro di round o di fasi — rito corale, scontro a fasi, skill
challenge, hazard ricorrente, inseguimento — il master fornisce, **dopo** le
meccaniche e separata da esse:

- **apertura di round**: cosa è cambiato nel mondo rispetto al round prima;
- **un micro-box per attore**, nell'**ordine di gioco dichiarato** (3-5
  righe: cosa vede/sente/tocca *quel* PG in quei sei secondi);
- **una riga di esito per la riuscita e una per il fallimento** — sensoriale,
  non meccanica: il malus lo applica la tabella, la riga fa *sentire* il costo;
- **chiusura di round**: cosa vedono cambiare (l'avanzamento visibile).

**Corollario — ordine di risoluzione.** Se un PG può modificare la CD o il
tiro di un altro, il master **dichiara l'ordine dei tiri** in modo che il
bonus esista *prima* di servire (non basta l'ordine narrativo). Esemplare:
`ARC07-DEF-1` §9 Fase 2, «il giro del round in quattro battute» — Thorik
dichiara, **Tordek tira**, Thorik tira con la CD risultante, Artemis tira.

### 2. Occhio da avventuriero, non da architetto

Ogni luogo in cui i PG mettono piede ha un read-aloud **«dei sei secondi»**:
ciò che un professionista dell'avventura coglie in un'occhiata.

- **Scala per paragone**, non per misura: «una bolla grande come la piazza di
  un mercato», «una lastra larga quanto la sala di una locanda».
- **Materiali, temperatura, odore, suono** — e soprattutto **cosa è
  sbagliato** in quel posto (dove finisce il «sotto», cosa non proietta
  ombra, cosa è tiepido dove tutto è freddo).
- **Chiusura su decision point** («Che fate?»).
- Le metrature restano: in un blocco **«Dati per il DM (non da leggere)»**
  o sulla mappa. **Mai nella voce narrante.**

### 3. Gli ingressi si scrivono

Per ogni ambiente-chiave (camere di boss in primis) il master dice: **c'è una
porta o no**, chi/cosa la apre, **dove sbucano** i PG, che gravità/terreno
trovano al primo passo, e qual è la **domanda d'apertura** posta dalla
geografia. Il DM non deve improvvisare l'ingresso della scena madre.

## Conseguenze

- Più facile: un DM legge il master e ha in mano **la serata già raccontata**;
  i giocatori percepiscono l'evoluzione invece di subire i dadi; gli agenti
  sanno esattamente cosa produrre (niente «meccanica sì, prosa forse»).
- Più difficile / rinunce: i master si allungano (la regia dei tre round del
  rituale è ~2 pagine); va accettato — è la parte che il DM legge ad alta voce.
- Da rivisitare: se `validate_modules.py` verrà esteso a controllare la
  presenza di blockquote nelle sezioni con marcatori di round, aggiornare qui
  e in `rumblingstone-module-standard`.

## Copertura skill (ADR-0008)

- `rumblingstone-module-standard` — checklist §6 (occhio da avventuriero),
  §8 (ingressi + sei secondi), §10 (regia delle sequenze a battute).
- `rumblingstone-narrative-style/references/editorial-standards.md` §2 — la
  resa sulla pagina delle due regole.

## Esemplari

- `07_.../ARC07-DEF-1-PIANO-TERRA-TERROS.md` §8a («i sei secondi della
  soglia», l'attracco dell'Altare), §8b («il distacco»), §9 Fase 2 («la
  regia dei tre round»).
