# PIANO — Il lettore e il playtester: trovare quello che il DM dovrà inventare

> **Cos'è**: uno strumento in due metà che legge un modulo come lo legge un DM
> che non l'ha scritto, e trova i posti in cui dovrà inventare. La metà
> deterministica (`scripts/copertura_scene.py`) sta in CI; l'altra metà sono
> due letture a freddo fatte da un agente con una rubrica fissa
> (`skills/rumblingstone-playtest/references/`).
>
> **Stato**: 🟡 F1-F3 e F7-F9 chiusi; restano F4 (allargato al ciclo del master, ADR-0075), F5, F6-a e le decisioni D5-D8 qui sotto · **Decisore**: DM ·
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

- [ ] 🐛 **F6-a · il cancello che non vede un master senza scene**
      `[engine: Sonnet · effort: medio · qualità: un test in cui un ARC*-DEF-* senza «### SCENA» fa uscire 1 --check]` — **C**.
      Trovato il 2026-09-27: `copertura_scene` e la parte per scene di
      `domande_developer` riconoscono una scena solo dal titolo `### SCENA`. Un
      master di prova senza quel titolo, con un PNG che parla senza scheda e
      nessun box, ha avuto **zero rilievi**. «I master nuovi nascono sotto il
      cancello» era vero solo per chi usava il titolo giusto. Rimedio: una
      regola `C0 · nessuna scena` per ogni file col profilo severo. **Va prima
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
| D5 | F3 | **TS, DV, RI e incantesimi di Skullcrusher** (DEF-4 A.1) non ci sono. Proposta: ricavarli dal drago nero adulto dell'SRD, avanzato a Enorme, e marcarli come derivati |
| D6 | F3 | **Da dove viene il Rubino, e chi lo custodisce nel 372?** (lettore a freddo, seconda lettura, L #34 🔴). Il modulo lo fa comparire sull'incudine senza dire da dove |
| D7 | F3 | **La fortezza «giovane, appena eretta» e Balvar che ne è stato il runaio** prima dei bisnonni dei nani di oggi: una delle due cose va cambiata. È aperta anche in `PIANO-CHIUSURA-DEI-MILLE-ANNI` M7 |
| D8 | F5 | **Il Drappo vuole un Riflessi e una Volontà?** `domande_developer` non ne trova nessuno sull'intero modulo. Proposta: il Riflessi sì (la caduta nella curva), la Volontà solo se il DM la vuole in un modulo d'intrigo |

## 5 · Validazione

- `python3 scripts/copertura_scene.py --check` verde in CI.
- `python3 scripts/componenti.py --check` e `python3 scripts/quiz_lettura.py --check`
  verdi in CI (F7, F8).
- `python3 scripts/domande_developer.py --check` verde in CI (F9).
- Ogni residuo ha la ragione, e un residuo che smette di verificarsi fa fallire
  il cancello finché non lo si toglie.
- Un tipo di rilievo che le letture trovano in **due moduli diversi** diventa una
  regola nuova, con i falsi positivi contati a mano prima di entrare.
