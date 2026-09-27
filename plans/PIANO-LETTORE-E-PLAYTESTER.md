# PIANO — Il lettore e il playtester: trovare quello che il DM dovrà inventare

> **Cos'è**: uno strumento in due metà che legge un modulo come lo legge un DM
> che non l'ha scritto, e trova i posti in cui dovrà inventare. La metà
> deterministica (`scripts/copertura_scene.py`) sta in CI; l'altra metà sono
> due letture a freddo fatte da un agente con una rubrica fissa
> (`skills/rumblingstone-playtest/references/`).
>
> **Stato**: 🟡 F1-F3 e F7-F9 chiusi; restano F4 (allargato al ciclo del master, ADR-0075), F5 e le decisioni qui sotto · **Decisore**: DM ·
> **Decisione**: [ADR-0073](adr/ADR-0073-chi-e-dove-sta-scritto-nella-scena.md)
> **Gate**: `copertura_scene.py --check` verde; su `ARC07-DEF-4` la lettura a
> freddo ripetuta dopo F3 non trova più rilievi 🔴 nelle Scene 5-9

---

## 0 · Perché

Il DM, il 2026-09-26, dopo la sessione del giorno prima: *«nell'avventura così
come è scritta mancano davvero le descrizioni delle stanze e dei png che
incontrano, li ho dovuti inventare sul momento»*. E poi: *«vedi se si può
implementare un ruolo lettore e playtester che cercano di capire l'avventura
solo leggendola e giocando […] da utilizzare come verifica per ogni canone»*.

Sette cose inventate al tavolo: i quartieri, la cappella e la sua chierica,
l'alchimista, le gallerie, il capitano delle mura, l'araldo, le guardie della
tenda. Il giorno della sessione tutti i cancelli del repo erano verdi. La norma
che le avrebbe coperte c'era: `rumblingstone-module-standard` scrive da luglio
che *la scheda d'entrata del PNG sta nella scena in cui i PG lo incontrano*.
Nessuno la misurava.

## 1 · Cosa fanno gli editori, e cosa si prende

Solo fatti generali e verificabili, senza pretendere di conoscere i processi
interni:

- Nei colophon Paizo e WotC il lavoro sul testo è diviso fra **sviluppo**
  (*developer*: la cosa si gioca? i numeri tornano?) ed **editing** (*editor*:
  la cosa si capisce?). `RICERCA-RUOLI-EDITORIALI-COLOPHON-PAIZO-2026-08` ha
  già mappato quei ruoli sulle skill del repo.
- Tutte e due le case hanno fatto **playtest pubblici** su larga scala: *D&D
  Next* (2012-2014) e le *Unearthed Arcana* con sondaggi per WotC, il
  *Pathfinder Playtest* del 2018 per Paizo. Il playtest pubblico misura le
  regole con migliaia di tavoli; un gruppo solo non può farlo.

Da qui la divisione: il **lettore** fa il lavoro dell'editor, il
**playtester** quello del developer. Il playtest pubblico non si può imitare, e
la sua funzione la tiene il tavolo vero (`rumblingstone-playtest` §6). Quello
che un editore non ha, e il repo sì, è una CI: un difetto trovato una volta si
trasforma in una regola che impedisce che si ripeta.

## 2 · La calibrazione — su cosa il DM aveva al tavolo

Bersaglio: `ARC07-DEF-4` al commit `ddd683c`. Rapporti completi in
`esperimenti/lettore-playtester-def4/`. La rubrica è stata ripulita **prima**
della misura: la prima stesura citava tre delle sette lacune come esempi, e
quelle due letture sono state fermate prima che dessero un numero.

| Lacuna inventata al tavolo | Script (C1) | Lettore | Playtester |
|---|:-:|:-:|:-:|
| i quartieri | ✅ Scena 5 senza box | — | — |
| la cappella e la chierica | — | — | ✅ #14 mancano prezzi e venditori |
| l'alchimista | — | — | ◐ #14, generico |
| le gallerie | — | ✅ #18 | — |
| il capitano delle mura | — | ✅ #40 | — |
| l'araldo | — | ◐ #33 | — |
| le guardie della tenda | — | ◐ #33, #55 | — |

**4 trovate, 3 in parte, nessuna mancata del tutto**, e nessuna delle tre metà
da sola ne trova più di due. Tre controprove che le letture misurano cose vere:

- il lettore (#20) e il playtester (#8) trovano l'invisibilità a 120 minuti,
  che era stata corretta a 12 in M6 per conto suo;
- il lettore (#25) trova l'incoerenza sull'età di Balvar, aperta in
  `PIANO-CHIUSURA-DEI-MILLE-ANNI`;
- il playtester (#19) prevede il sorvolo del campo, che il tavolo ha fatto
  davvero, e (#24) le rune di Balvar senza CD, che il DM ha chiesto il giorno
  dopo.

⚠️ **Cosa questa calibrazione non dice.** È un caso solo, con un agente solo
per ruolo. Non misura quanto le due letture siano stabili: ripetute, daranno
elenchi diversi. Le letture trovano, e il cancello tiene fermo quello che è
stato trovato.

## 3 · Le regole deterministiche, e quelle scartate

Misurate su DEF-4 prima e dopo, controllando a mano ogni segnalazione (G2, G6):

| Regola | Esito | Perché |
|---|---|---|
| **C1** scena senza box | ✅ tenuta | sui 9 moduli, 16 segnalazioni, controllate a mano una per una: in nessuna delle 16 sezioni c'è un box, quindi il rilevatore non sbaglia mai. In 3 casi è discutibile che serva (DEF-4 Scena 8, che continua la tenda della 7; DEF-2 §7, che è una sezione di regole; DEF-3 §8-bis, un momento lasciato all'improvvisazione) |
| **C2** chi parla senza scheda | ✅ tenuta | 8 segnalazioni: 2 lacune vere (Varis, Madre Dana), 1 da decidere (Re Thorek in DEF-5), 5 voci che non sono persone (un dio, artefatti, un'entità) dichiarate come residui |
| **C3/C4** contratto «In scena» | ✅ nuova norma | non si misura un'assenza con una regex; si chiede a chi scrive di fare l'elenco, e si misura l'elenco |
| luogo annunciato in grassetto senza box | ❌ scartata | 1 vera su 6 in DEF-4 (circa 17%) |
| CD senza chi la tira | ❌ scartata | 5 segnalazioni, quasi tutte falsi positivi; resta alla passata 2 dell'audit meccanico |

## 4 · I lotti

### F1 · Lo strumento ✅ (2026-09-26)

- [x] `scripts/copertura_scene.py`, `plans/copertura-scene.json` (profili e
      residui con la ragione), `scripts/tests/test_copertura_scene.py`
      (ogni regola ha un caso che la fa scattare), voce nel manifest, passo in CI
- [x] rubriche fisse: `lettore-a-freddo.md`, `playtester-a-freddo.md`
- [x] ADR-0073, norma nel registro, rimando in `rumblingstone-playtest` e in
      `rumblingstone-module-standard`

### F2 · La calibrazione ✅ (2026-09-26)

- [x] le due letture cieche sul DEF-4 del tavolo, e la tabella §2

### F3 · DEF-4 prima della prossima sessione — 🟡 in corso

La sessione si è fermata prima dell'infiltrazione. Si parte dalle Scene 6-9.

- [x] i rilievi 🔴 e 🟠 dei due rapporti, ricontrollati **sul testo di oggi**:
      diversi erano già chiusi da M5-M7 (invisibilità a 12 minuti, sorvolo,
      guardie, araldo, capitano). Chiusi qui, nelle Scene 6-9: lo skill
      challenge (prova di gruppo per blocco, cinque blocchi, quanto copre
      l'invisibilità), la pattuglia dei tre fallimenti, «+2 nemici» diventato
      «un successo in meno» sulle mura, cosa fa Balvar quando comincia lo
      scontro e l'EL combinato, le sue tre rune nella tenda allineate alla
      scheda del Bestiario (la quarta è la Catena), quando si vede la runa e
      come si colpisce, la Corona «sentita» se sono invisibili, da dove si
      entra nella tenda, il round di sorpresa SRD, Zog'tar catturato e la
      sconfitta nella tenda, Vatore senza statistiche e il Cronolito, le
      abilità non 3.5. Fuori dalle 6-9: la riga di §6 per chi attacca la
      pattuglia di Durin, il soffio del drago in linea
- [x] i numeri di Balvar copiati in Appendice A.4, come ha chiesto il DM, e
      `TestLaCopiaDiBalvar` che confronta le due copie
- [x] il contratto «In scena» su tutte le tredici scene, `contratto: true`.
      Ha trovato da solo **la bottega di Kettra senza box**, e ha costretto a
      scrivere le comparse: i sei veterani, le guardie della porta, il
      pesatore, Grask, le creature del campo, le quattro guardie, Hrodgar
- [x] C1 delle Scene 2 e 8: un box per la pattuglia di Durin e uno per Zog'tar
      che si alza dal seggio. I due residui temporanei sono scaduti, e il
      cancello ha chiesto di toglierli
- [x] una seconda lettura a freddo sul testo corretto: il lettore non trova
      🔴 nelle Scene 5-9, il playtester due (il corno durante lo scontro, il
      ritorno a piedi). Chiusi subito dopo, con il 🔴 del drago attaccato di
      notte e otto 🟠. Resoconto: `esperimenti/lettore-playtester-def4/SECONDA-LETTURA.md`
- [ ] ⚠️ **da decidere (DM)**: TS, DV, RI e incantesimi di Skullcrusher (A.1)
      non ci sono; i nomi e le regole marcati `[INFERRED]` in questo lotto

⚠️ **Dal 2026-09-26 `DEF-4` non vale più come caso di calibrazione cieca.** La
rubrica del playtester ha preso le domande del developer
(`RICERCA-MANUALE-DEL-MASTER-2026-09`), e due di quelle («e se volano?», «chi
sente il rumore?») sono nate dai suoi difetti. Una calibrazione nuova si fa su
un modulo che la rubrica non ha mai visto.

### F3-bis · DEF-4 prima della prossima serata — 🟡 (2026-09-27)

`[engine: Opus, sessione principale; letture a freddo in subagenti ciechi · effort: xhigh · qualità: ciclo del master passi 1-6 sulle Scene 6-13, misura prima e dopo]` — **K** dove tocca il canone, **C** per il resto

Il DM, il 2026-09-27: *«prima di DEF-5 andiamo bene con DEF-4»*. Al tavolo si
riprende dall'infiltrazione nel campo nemico (Scena 6). Richieste esplicite:
Skullcrusher che secondo gli esploratori va via al tramonto; cosa cambia se i
PG volano, sono invisibili e silenziosi; scene, PNG e villain descritti quando
i PG li incontrano, con i controlli automatici dove vale la pena; un giro del
developer e del playtester; la misura del miglioramento.

- [x] misura di partenza e due letture a freddo cieche sul testo di prima
      (`esperimenti/def4-seconda-serata/`)
- [x] giro del developer sulle Scene 6-13
- [x] correzioni che non toccano il canone, nel modulo
- [x] due controlli nuovi: `copertura_scene` C5 (la scheda sta nella scena del
      primo incontro) e C0 (un modulo senza scene), `domande_developer` D2 col
      silenzio
- [x] niente riposo breve o lungo (il DM, 2026-09-27: *«non esistono riposi
      lunghi e corti in D&D 3.5 e PF1e»*): sei righe corrette in DEF-1, DEF-2 e
      DEF-4, il controllo in `validate_modules` e `validate_standalone` con la
      stessa regex, la tabella del riposo SRD in `dnd-35-srd` (dove la
      guarigione a letto diceva ×1,5 invece di ×2). Il playtester della prima
      lettura l'aveva già visto (#13 🟡) e il testo era andato al tavolo lo
      stesso: rileggendo quei rapporti, altri tre rilievi di regole erano
      rimasti aperti (D25)
- [x] le risposte del DM del 2026-09-27 (D5, D20, D24): Skullcrusher adulto
      maturo dell'SRD, il sonno a 6 tacche, le tacche segnate. Nello stesso
      giro, la notte già giocata messa in conto: le pergamene chieste
      (*silenzio*, *identificare*, *rimuovi maledizione*, *rimuovi paralisi*)
      con prezzi e quantità SRD, l'identificazione delle pozioni in 35 minuti
      (Sapienza Magica CD 25, un minuto l'una), e il tetto di quello che i nani
      comprano, con le armi e armature naniche d'adamantio vendute al tavolo
- [x] **il banco**, perché i prossimi moduli non siano carenti (il DM:
      *«organizza il tutto in modo che i prossimi moduli non siano carenti,
      mettendo un po' di diffidenza e preferenze dei mercanti […] come un
      pizzico di spezie»*). Le decisioni prese al volo nelle serate del 25-27
      settembre stavano già in DEF-4 come `[CANONE — DM …]` (22 punti); da lì
      la norma `module-standard/references/il-banco.md` (cosa vende e quante,
      servizi, chi identifica e in quanto tempo, cosa compra e fino a quale
      tetto; la spezia facoltativa). Misure: `copertura_scene` C6 (chi vende
      senza un prezzo) e C7 (Chi si trova qui senza le sei righe), con i test;
      `P-ABITATO` chiede quantità, tetti e identificazione. La rete al tavolo:
      §2-bis del kit anti-improvvisazione, una spezia a d8 per luogo. Prima
      applicazione: la tabella **Chi si trova qui** della Scena 5 di DEF-4, che
      ADR-0075 chiedeva e il master non aveva ancora
- [ ] le decisioni del DM ancora aperte (D11-D19, D21-D23, D24-b, D25-D28)
- [x] le letture a freddo dopo, e la tabella prima/dopo
- [x] un secondo giro di correzioni sui rilievi delle letture dopo che non
      toccano il canone

**La misura, prima e dopo** (letture cieche, agenti diversi a ogni giro,
stesse rubriche ripulite; rapporti in `esperimenti/def4-seconda-serata/`):

| | Lettore prima | Lettore dopo | Playtester prima | Playtester dopo |
|---|---:|---:|---:|---:|
| rilievi | 36 | 46 | 23 | 34 |
| 🔴 | 2 | 2 | 2 | **1** |
| 🟠 | 13 | 18 | 7 | 9 |
| 🟡 | 21 | 26 | 14 | 24 |

**Il numero è salito, e va letto così.** Due letture non danno mai lo stesso
elenco (lo dice la rubrica), e le seconde sono state più lunghe e più fini: molti
🟡 nuovi sono cose che c'erano anche prima e nessuno aveva segnato (i PX di
Skullcrusher, la mappa del campo senza effetto). Quello che si confronta è la
classe grave e dove cade:

- **il 🔴 comune alle due letture di prima**, i PG visibili alla tenda, **non
  compare più in nessuna delle due**;
- **il 🔴 rimasto al playtester** sono le statistiche di Skullcrusher (D5), che
  solo il DM può chiudere;
- **il nuovo 🔴 del lettore** è la provenienza del Rubino, che è la D6 aperta da
  settimane: la seconda lettura di luglio l'aveva già segnato;
- **una parte dei 🟠 nuovi li ho introdotti io**: regole che citavano numeri che
  il modulo non ha (l'Osservare del drago, il Percepire Intenzioni di Balvar,
  l'Ascoltare di Vatore) e il rapporto degli esploratori messo dopo lo skill
  challenge. Il secondo giro li ha corretti.

**Il secondo giro, dopo le letture**, ha chiuso senza toccare il canone sette
rilievi 🟠 (l'ordine della Scena 6, il blocco fallito, la caccia notturna del
drago, Vatore che sente i PG e le prove fallite con lui, le complicazioni 3 e 4,
il Registro delle Perdite ancora citato nella Scena 5). Questi non sono stati
rimisurati alla cieca: la terza lettura si fa dopo le risposte del DM, sul testo
che andrà al tavolo.

Restano aperti senza una decisione: la durata di una tacca nel mondo, il
Cronolito, la tabella B4 e le ferite ancestrali, il momento in cui Balvar usa il
Fuori-Posto, e gli oggetti del cortile che la mappa M7-B non ha (è un lotto di
mappe, non di testo).

### F4 · Gli altri master di ARC-07 — ⬜ · allargato il 2026-09-27 (ADR-0075)

`[engine: Opus, sessione principale · effort: xhigh · qualità: i sette passi del ciclo del master, per ogni DEF]` — **K** per DEF-5 (si gioca subito), **C** per gli altri

Il DM, il 2026-09-27: *«l'arco 07 è davvero completo anche con le nuove
regole? ci hai fatto una passata anche con developer e playtester?»*. No.
Le quattro regole nuove (contratto, componenti, developer, lettura a freddo)
sono state applicate a **DEF-4 soltanto**. Misura dello stesso giorno:

| Master | Righe | Scene `### SCENA` | Contratto | Apparato | Box > 12 | Developer | Lettura a freddo |
|---|---:|---:|---|---|---:|---:|---|
| DEF-1 | 2.293 | 0 | no | no | 6 | 0 (non vede scene) | no |
| DEF-2 | 939 | 0 | no | no | 1 | 2 | no |
| DEF-3 | 1.306 | 0 | no | no | 0 | 2 | no |
| DEF-5 | 516 | 0 | no | no | 1 | 1 | no |

Il lotto è quindi il **ciclo completo** di `rumblingstone-module-standard`
(sette passi) su ognuno dei quattro, non il solo contratto. **Va prima di A3 di
PIANO-MASTER-DEF**, perché ARC-08 comincia dove finisce DEF-5.

- [ ] DEF-5 per primo, perché si gioca subito dopo DEF-4: Madre Dana, Re Thorek,
      §5 senza box, la Tempra; qui confluiscono anche i read-aloud di S4 di
      MESTIERE-BANCHI (DEF-5 ne ha quattro in 516 righe). ⚠️ Una scena già
      letta al tavolo non si riscrive (D3 di MESTIERE-BANCHI)
- [ ] DEF-1 (Varis), DEF-2, DEF-3: i residui dichiarati, prima che un gruppo
      nuovo li riprenda. Sono **già giocati** (`copertura-scene.json`): si
      convertono nella forma (titoli `### SCENA`, contratto, componenti, box al
      metro) e non in cosa succede, che per questo gruppo è già canone
- [ ] per ognuno, alla fine: lettore e playtester a freddo senza 🔴, quiz con la
      chiave approvata dal DM, e la riga tolta da `plans/copertura-scene.json`
- [ ] **DEF-5 è la prova cieca di `P-ABITATO`** (ADR-0075, «La prova contro il
      tavolo»): il playtester legge DEF-5 **prima** che gli si aggiunga la
      tabella *Chi si trova qui*, e si conta se trova da solo i ruoli che
      mancano. Se non li trova, la domanda va riscritta

### F5 · Gli stand-alone — ⬜

- [ ] Drappo: sette sezioni senza box, fra cui la rivelazione del Drappo di
      Lino Rasca (Giorno 3 §8)
- [ ] Abbazia: l'Atto II e le stanze in stile *keyed*: decidere col DM se
      ogni stanza vuole un box
- [ ] il contratto sugli stand-alone, col foglio del cast come fonte delle schede

### F6 · I master nuovi di ARC-08 e ARC-09

Nascono sotto il cancello: un `ARC*-DEF-*` che `copertura-scene.json` non
elenca prende il profilo severo, contratto compreso. Si pianificano in
[PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE](PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md),
aperto il 2026-09-27.

- [x] 🐛 **F6-a · il cancello che non vede un master senza scene** ✅ (2026-09-27, con F3-bis: `copertura_scene` C0 e il suo test)
      `[engine: Sonnet · effort: medio · qualità: un test in cui un ARC*-DEF-* senza «### SCENA» fa uscire 1 --check]` — **C**.
      Trovato il 2026-09-27: `copertura_scene` e la parte per scene di
      `domande_developer` riconoscono una scena solo dal titolo `### SCENA`. Un
      master di prova senza quel titolo, con un PNG che parla senza scheda e
      nessun box, ha avuto **zero rilievi**. «I master nuovi nascono sotto il
      cancello» era vero solo per chi usava il titolo giusto. Rimedio: una
      regola `C0 · nessuna scena` per ogni file sotto cancello, che usa il titolo di scena del suo profilo (`### SCENA` per i master, `## §N` per DEF-5 e gli stand-alone). **Va prima
      di S1 di PIANO-MASTER-DEF** (ADR-0075)

### F7 · Il quiz a due agenti ✅ (2026-09-26)

Il DM: *«capisco qualcosa se leggo, o devo rileggere il modulo più volte?»*.
Le letture a freddo trovano i buchi; il quiz misura quanto resta dopo una
lettura sola.

- [x] la rubrica del lettore prende **le domande, sempre le stesse**: sette per
      scena, ognuna col suo codice, e tre di modulo
- [x] procedura in `rumblingstone-playtest/references/quiz-a-due-agenti.md`,
      punteggio in `scripts/quiz_lettura.py` (`--check` in CI sulle chiavi)
- [x] chiave di DEF-4, 14 domande, **stato bozza**
- [x] prima esecuzione, DEF-4 prima e dopo F3 (`esperimenti/quiz-def4/`): a libro
      aperto i buchi scendono **da 4 a 0**, dagli appunti la quota sale solo
      **da 5 a 6**, e la missione della serata (q4) manca negli appunti di
      tutti e due i lettori
- [x] il DM approva la chiave (2026-09-27), e la q8 accetta tutti e due i
      desideri di Balvar
- [x] il riquadro *La serata in tre frasi* in testa a DEF-4 (sì del DM), e un
      terzo quiz: 6 su 14 dagli appunti come prima, e la missione ancora fuori
      dagli appunti. Il limite è del lettore-agente, che prende appunti
      procedurali: scritto nel protocollo, «Il limite osservato»

### F8 · Il master come componenti ✅ (2026-09-26)

Il DM: *«i DEF sono divisibili in oggetti che vengono rimessi insieme […] come
gli editor di publishing tipo Scribus»*, e *«sì»* a farlo prima dei DEF di
ARC-08. Decisione in [ADR-0074](adr/ADR-0074-il-master-come-componenti.md).

- [x] `scripts/componenti.py`: indice dei componenti, apparato generato
      (`APPARATO-<master>.md`: cast, CD, read-aloud), copie sincronizzate
      (`<!-- include: fonte#blocco -->`, e `#statblocco` per il Bestiario);
      `--check` in CI
- [x] misurato prima di decidere: nessuna copia alla lettera fra master vivi, e
      la copia di Balvar era una riscrittura. Si include il **blocco
      statistiche**, non la prosa
- [x] primo uso: DEF-4 A.4 include lo statblocco di Balvar dal Bestiario
- [x] l'inserto delle CD prende 43 CD su 43 in DEF-4 (il primo estrattore ne
      perdeva 13); l'apparato è escluso da `misura_craft` e marcato in `fase1`
- [ ] i master nuovi di ARC-08 (F6) nascono con l'apparato generato

### F9 · Le domande del developer, misurate ✅ (2026-09-26)

Il DM: *«fai anche lo strumento di analisi scaturito dalle cose decenti dei due
manuali, così può misurare e segnare il problema, se esiste nell'avventura»*.

- [x] `scripts/domande_developer.py`: sei delle sette domande di
      `sviluppo-degli-incontri.md` (D1 nemico in volo, D2 volo e invisibilità,
      D3 i tre TS, D4 chi sente il rumore, D5 la soglia del boss, D6 lo skill
      challenge per intero, D6-5E abilità estranee al sistema); la §7 resta un
      giudizio del playtester
- [x] calibrato sul DEF-4 del tavolo (`esperimenti/domande-developer-def4/`):
      **5 difetti noti su 5**, precisione 5 su 9; due forme corrette dalla
      calibrazione (la risposta per chi non vola, il sistema PF1e del Drappo)
- [x] 12 rilievi sui 9 moduli, ognuno dichiarato con la ragione in
      `plans/domande-developer.json`; `--check` in CI
- [x] DEF-4 Scena 11, cosa fa chi non vola nei round in quota (playtester
      #42): chiuso il 2026-09-27 col sì del DM, tre vie SRD e le balestre delle
      mura `[INFERRED]`
- [ ] F4: la Tempra di DEF-5 · F5: l'invisibilità al corpo di guardia
      dell'Abbazia, Riflessi e Volontà nell'Abbazia e nel Drappo

## Decisioni aperte al DM

<!-- decisioni-dm: LETTORE-PLAYTESTER -->

| # | Fase | Domanda |
|---|---|---|
| ~~D1~~ | F7 | ✅ **Decisa il 2026-09-27**: la chiave del quiz di DEF-4 è approvata |
| ~~D2~~ | F7 | ✅ **Decisa il 2026-09-27**: alla q8 valgono tutti e due i desideri di Balvar (Hammerfist che cade in fretta, e qualcuno che dica che c'era) |
| ~~D3~~ | F7 | ✅ **Decisa il 2026-09-27**: il riquadro *La serata in tre frasi* entra in testa a DEF-4 |
| ~~D4~~ | F9 | ✅ **Decisa il 2026-09-27**: DEF-4 Scena 11 dice cosa fa chi non vola (preparare un'azione, le corde, le balestre delle mura `[INFERRED]`) |
| ~~D5~~ | F3 · F3-bis | ✅ **Decisa il 2026-09-27**: Skullcrusher è un **drago nero adulto maturo** dell'SRD (il DM: *«anziano adulto, con resistenza agli incantesimi e lista degli incantesimi»*). Numeri dalla tabella SRD, raggiunta via Firecrawl: 22 DV, 253 pf, CA 29, RI 21, RD 10/magia, soffio 14d4 CD 26, Presenza CD 23, incantatore di 5°. GS 14 = APL+1. Talenti, abilità e incantesimi conosciuti sono una proposta `[INFERRED]`. Aggiornati il giro del boss, la regia dei round, la scalatura (Vecchio SRD) e i PX (5.400, `[INFERRED]`) |
| D6 | F3 | **Da dove viene il Rubino, e chi lo custodisce nel 372?** (lettore a freddo, seconda lettura, L #34 🔴). Il modulo lo fa comparire sull'incudine senza dire da dove |
| D7 | F3 | **La fortezza «giovane, appena eretta» e Balvar che ne è stato il runaio** prima dei bisnonni dei nani di oggi: una delle due cose va cambiata. È aperta anche in `PIANO-CHIUSURA-DEI-MILLE-ANNI` M7 |
| D8 | F5 | **Il Drappo vuole un Riflessi e una Volontà?** `domande_developer` non ne trova nessuno sull'intero modulo. Proposta: il Riflessi sì (la caduta nella curva), la Volontà solo se il DM la vuole in un modulo d'intrigo |
| D9 | F4 | **Nei master già giocati (DEF-1, DEF-2, DEF-3) i box oltre 12 righe si spezzano?** Il passo 5 del ciclo li vuole ≤ 12; DEF-1 ne ha 6, DEF-2 uno. Spezzarli in battute non cambia una parola, ma tocca prosa già letta ai giocatori, ed è la D3 ancora aperta di MESTIERE-BANCHI. Proposta: sì, solo spezzare, come il box di Balvar in DEF-4; mai riscrivere cosa dicono |
| D10 | F4 | **Il quiz a due agenti (passo 7) va fatto su ogni master?** Ogni quiz chiede una chiave approvata dal DM: con ARC-07, ARC-08, ARC-09 e gli stand-alone sono una ventina di chiavi. Proposta: sì sui master nuovi e su quelli riscritti nella prosa; no sulle conversioni di sola forma dei master già giocati (DEF-1, 2, 3), dove bastano lettore e playtester. Saltarlo lì è una decisione del DM, e va scritta (ADR-0075) |
| ~~D11~~ | F3-bis | **I numeri del campo, delle guardie e di Zog'tar.** *(2026-09-27, risposta del DM)*: fuori girano i lupi, dentro le ronde di hobgoblin, orchi e goblin senza lupi; gli sciamani gli esploratori non li hanno visti, ma possono esserci. Scritto in DEF-4 Scena 6: sei squadre di cavalieri su worg sull'anello esterno, ronde di orchi, squadroni hobgoblin e vedette goblin dentro, con i numeri SRD (worg, orco, goblin, hobgoblin); circa quindici sciamani (adepti orchi di 5°) che dopo il corno lanciano *vedere invisibilità*; un sacerdote della Mano (hobgoblin adepto 7, GS 6) nella tenda accanto a Zog'tar, EL della tenda sempre 16. La pattuglia dei tre fallimenti ha i suoi numeri (guerriero 4 SRD). Tutto `[INFERRED]` fino al tuo OK. ✅ **Zog'tar, decisa lo stesso giorno** (il DM: *«lo voglio con l'Ira Superiore, e tosto: deve reggere più di un round»*): Barbaro 11 / Guerriero 4, GS 15, 253 pf (298 in Ira), numeri ricalcolati sull'SRD, `Boost log:` nel Bestiario; la tenda arriva a EL 17, il tetto. **Resta aperto**: Balvar non ha abilità nello statblocco, mentre la Scena 7 usa il suo Percepire Intenzioni |
| D12 | F3-bis | **La pietra del silenzio della variante dall'alto: chi la dà, e quanto dura?** Nessuno la vende. Proposta: Brynja, alla cappella, lancia *silenzio* su un sasso; dura un round per il suo livello, quindi basta per l'atterraggio e la tenda, non per il volo intero. Serve il livello di Brynja |
| D13 | F3-bis | **Il corno di Grask: al polso o nella custodia col glifo?** Il modulo dice tutte e due le cose. E dopo un allarme di notte il drago dove va? Il testo ora dice «se ne va», senza scegliere fra le colline e il campo |
| D14 | F3-bis | **Due esiti del duello senza casella.** Se Balvar è morto il drago fugge a metà pf: conta come FERITO GRAVE o FUGGITO? E la Catena spezzata dà «FUGGITO garantito», che per il carry-over B4 è l'esito più debole: è voluto? Proposta: fuga a metà pf = FERITO GRAVE; la Catena spezzata vale FERITO GRAVE se il drago aveva già perso almeno un terzo dei pf. E la fuga a ⅓ dipende da «se i PG premono o allentano», che non è una regola. Proposta: a ⅓ dei pf fugge al suo turno, a meno che nel round prima abbia subito almeno due colpi |
| D15 | F3-bis | **Quando il duello «crolla» e intervengono gli avi (§6)?** Non c'è una soglia. Proposta: due PG a terra nello stesso round, oppure il gruppo che si ritira dal cortile |
| D16 | F3-bis | **Il tono del Rubino è deciso in quattro posti** (la targa nella Scena 3, come muore Zog'tar nella Scena 8, l'esito del duello in §7, il «vinto sporco» in §6). Quale vince? Proposta: vince l'esito del duello; gli altri tre colorano la prima frase della Corona |
| D17 | F3-bis | **L'Aura della Forgia «dura fino all'alba», ma il rito si fa già all'alba.** Proposta: fino all'alba del giorno dopo, e quindi i PG arrivano a DEF-5 con *Possenza Divina* e *Protezione dal Male* ancora addosso, oppure fino al ritorno col Rubino |
| D18 | F3-bis | **Le corde degli arieti non funzionano coi numeri**: una Lotta con +4 contro il +39 del drago non riesce quasi mai. Proposta: non è una Lotta ma una prova di Forza cooperativa, CD 25, con gli aiuti SRD di chi tira insieme; l'effetto resta l'ala inchiodata per un round. E le corde stanno nel cortile interno, mentre gli arieti sono fuori dalle mura: sono corde di un altro attrezzo (le gru delle mura?) o si tolgono |
| D19 | F3-bis | **Chi del gruppo capisce il nanico antico?** Balvar parla solo quello, e la trattativa della Scena 7 si regge su chi lo capisce. Oggi il modulo nomina solo Thorik come lettore. Proposta: i nani lo capiscono a fatica (tutto il senso, non le sfumature), Thorik lo legge |
| ~~D20~~ | F3-bis | ✅ **Decisa il 2026-09-27**: al tavolo hanno fatto il consiglio e il giro della fortezza (fucina, alchimista, cappella, rune di Zeth): **2 tacche** segnate, **3** se sono scesi da Zeth nelle gallerie. Non hanno dormito. Il «campo di corsa» resta senza regola, ma con 6 tacche per il sonno la scelta non si pone più |
| ~~D24~~ | F3-bis | ✅ **Decisa il 2026-09-27** (il DM: *«forse 6 tacche»*): dormire otto ore vale **6 tacche**. Con il consiglio segnato, chi dorme non fa in tempo a fare il campo prima dell'alba. Resta aperta la parte (b): i pf pieni di DEF-2 al tavolo del 31 luglio |
| D25 | F3-bis | **Tre rilievi di regole della prima lettura a freddo (2026-09-25) mai chiusi**, trovati rileggendo i rapporti vecchi. Il riposo breve era il quarto, e il playtester l'aveva già visto (#13). **(a)** Scena 1: «confusi 1d4 round (−2…)» è la condizione *confuso* dell'SRD o un −2? Proposta: *frastornato* non basta, quindi un −2 a attacchi e prove, scritto senza la parola «confusi». **(b)** Il +1 morale del banchetto e il +2 morale delle Benedizioni **non si sommano** in 3.5 (stesso tipo): proposta, il banchetto dà il +1 ai TS, dove le Benedizioni non arrivano. **(c)** Scena 11: «togliere al drago il vantaggio del suono in picchiata» non ha un numero. Proposta: con le campane suonate il drago perde il round di sorpresa della picchiata (ascoltare CD 20 per sentirlo arrivare) |
| D26 | F3-bis | **Il giro lettore, playtester e developer in automatico.** Oggi è obbligatorio (ADR-0075) ma lo ricorda solo il piano, e il riposo breve dimostra che un rilievo 🟡 può restare nel testo per giorni. Proposta: un registro in `plans/`, le letture a freddo in JSON, con per ogni master DEF, l'impronta del testo letto e i rilievi con il loro stato (corretto, residuo con ragione, domanda al DM); un cancello in CI che fallisce se il master è cambiato dopo l'ultima lettura, o se un rilievo 🔴 o 🟠 non ha uno stato. La lettura la fa un agente, non la CI: il cancello dice solo *quando* va rifatta. Costo: ogni modifica a un DEF, anche un refuso, chiede una lettura prima del merge, salvo una dichiarazione «modifica di sola forma» |
| D27 | — | **Il messaggio del 2026-09-27 si interrompe a «considera che i…».** Cosa andava considerato? |
| D28 | F3-bis | **La mappa di Hammerfist nel 372, dall'alto in basso.** Il DM, 2026-09-27: *«in ogni regno nanico, più si scende e più le stanze sono ampie, soprattutto le fucine grandi, come Erebor sotto la Montagna. Magari una mappa, anche con i camminamenti e le gallerie che le rune di Zeth riempiono come difesa contro un assalto interno, e il contorno delle mura esterne»*. Tre cose da decidere prima di disegnare: **(a)** che tipo di mappa (una sezione verticale a livelli, da consultare, o una griglia tattica da 1,5 m per giocarci sopra); **(b)** le rune di Zeth nelle gallerie sono già in gioco la prossima serata, con un effetto meccanico (per esempio un *glifo di interdizione* per corridoio), o solo colore; **(c)** la Scena 5 già giocata descrive tre forge e gallerie strette puntellate da poco: la fucina grande sta **sotto** quella giocata, oppure si riscrive il box. Proposta: (a) una sezione a livelli per il DM, più la griglia del solo cortile e delle mura, che c'è già (M7-B); (b) colore fino al 1372, dove Zeth è il Ghostlord; (c) la fucina grande sta sotto, e la si vede scendendo da Zeth |

| D21 | F3-bis | **Con 8 tacche o più, la Scena 10 si gioca?** Il modulo fa cominciare il duello fuori dalle mura, ma non dice se la prova delle mura salta né quale esito vale. Proposta: la Scena 10 non si gioca, le mura valgono «a stento» (2-3 successi), e un fallimento della prova di Muoversi Silenziosamente CD 20 fa partire il duello con il drago che ha già scelto il suo bersaglio |
| D22 | F3-bis | **Il ritorno a piedi non ha un costo di base in tacche**: l'andata ne costa 2, il ritorno 0 più una per blocco fallito. È voluto (al ritorno si sa la strada)? Proposta: 1 tacca di base |
| D23 | F3-bis | **Un Balvar recuperato può sciogliere lui la Catena?** È la prima cosa che un tavolo gli chiede. Oggi il modulo dice solo che spiega dove sta la runa e come si spezza. Proposta: può, ma solo toccando la scaglia, cioè nel cortile durante il duello, e lo sa |

## 5 · Validazione

- `python3 scripts/copertura_scene.py --check` verde in CI.
- `python3 scripts/componenti.py --check` e `python3 scripts/quiz_lettura.py --check`
  verdi in CI (F7, F8).
- `python3 scripts/domande_developer.py --check` verde in CI (F9).
- Ogni residuo ha la ragione, e un residuo che smette di verificarsi fa fallire
  il cancello finché non lo si toglie.
- Un tipo di rilievo che le letture trovano in **due moduli diversi** diventa una
  regola nuova, con i falsi positivi contati a mano prima di entrare.
