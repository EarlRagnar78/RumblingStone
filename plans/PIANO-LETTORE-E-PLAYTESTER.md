# PIANO — Il lettore e il playtester: trovare quello che il DM dovrà inventare

> **Cos'è**: uno strumento in due metà che legge un modulo come lo legge un DM
> che non l'ha scritto, e trova i posti in cui dovrà inventare. La metà
> deterministica (`scripts/copertura_scene.py`) sta in CI; l'altra metà sono
> due letture a freddo fatte da un agente con una rubrica fissa
> (`skills/rumblingstone-playtest/references/`).
>
> **Stato**: 🟡 F1-F3 chiusi; restano al DM le statistiche di Skullcrusher e l'origine del Rubino · **Decisore**: DM ·
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

### F4 · Gli altri master di ARC-07 — ⬜

- [ ] DEF-5 per primo, perché si gioca subito dopo DEF-4: Madre Dana, Re Thorek,
      §5 senza box, contratto
- [ ] DEF-1 (Varis), DEF-2, DEF-3: i residui dichiarati, prima che un gruppo
      nuovo li riprenda

### F5 · Gli stand-alone — ⬜

- [ ] Drappo: sette sezioni senza box, fra cui la rivelazione del Drappo di
      Lino Rasca (Giorno 3 §8)
- [ ] Abbazia: l'Atto II e le stanze in stile *keyed*: decidere col DM se
      ogni stanza vuole un box
- [ ] il contratto sugli stand-alone, col foglio del cast come fonte delle schede

### F6 · I master nuovi di ARC-08 e ARC-09

Nascono sotto il cancello: un `ARC*-DEF-*` che `copertura-scene.json` non
elenca prende il profilo severo, contratto compreso. Si pianificano a parte.

## 5 · Validazione

- `python3 scripts/copertura_scene.py --check` verde in CI.
- Ogni residuo ha la ragione, e un residuo che smette di verificarsi fa fallire
  il cancello finché non lo si toglie.
- Un tipo di rilievo che le letture trovano in **due moduli diversi** diventa una
  regola nuova, con i falsi positivi contati a mano prima di entrare.
