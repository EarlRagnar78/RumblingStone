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

### F3 · DEF-4 prima della prossima sessione — ✅

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
- [x] ⚠️ **da decidere (DM)**: TS, DV, RI e incantesimi di Skullcrusher (A.1)
      non ci sono; i nomi e le regole marcati `[INFERRED]` in questo lotto.
      *(2026-10-07: TS, DV e RI chiusi con la D5, drago nero adulto maturo
      dell'SRD. Talenti, abilità e incantesimi conosciuti restano `[INFERRED]`:
      sono la domanda Q37 di F3-quinquies, con le altre marcature)*

⚠️ **Dal 2026-09-26 `DEF-4` non vale più come caso di calibrazione cieca.** La
rubrica del playtester ha preso le domande del developer
(`RICERCA-MANUALE-DEL-MASTER-2026-09`), e due di quelle («e se volano?», «chi
sente il rumore?») sono nate dai suoi difetti. Una calibrazione nuova si fa su
un modulo che la rubrica non ha mai visto.

### F3-bis · DEF-4 prima della prossima serata — ✅ (2026-09-27)

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
- [x] le risposte del DM del 2026-09-28: 3 tacche segnate (sono scesi da Zeth);
      le rune di Zeth in tre famiglie (abiurazione e protezione, annullamento
      come nella miniera di Belkram, spegnimento di un incantesimo solo),
      scritte in fretta e da un uso; i pf non tornarono pieni il 31 luglio; e
      **la Cerimonia delle 100 Asce è solo di Hammerfist nel 1372**: tolti da
      DEF-4 i dieci rimandi che ci mandavano i caduti del 372, che ora il DM
      annota come «caduti del 372», e Thorgrim che riecheggia nell'affresco A3
- [x] le risposte del DM del 2026-09-28, secondo giro: D6 (il Rubino appare
      sull'incudine alla vittoria, e resta nell'incasso), D13 (la custodia col
      glifo incatenata al polso di Grask), D18 (Forza CD 25 cooperativa), D22
      (1 tacca di base al ritorno), D28 (a) la forma della mappa
- [x] le decisioni del DM ancora aperte (D12, D14-D17, D19, D21, D23, D25-D27,
      D28-b; e D7-D10 dalle fasi F3-F5). *(2026-10-07: decise il 2026-09-30 e
      applicate con `f7303df`; la casella era rimasta indietro. Per DEF-4 restano
      aperte D27, D39 e D40, più le marcature di F3-quinquies)*
- [x] **il lotto mappe D28** *(fatto il 2026-10-08: M7-A orientata, M7-B col cortile della Scena 11, M7-C con le altezze, la sezione M7-S e le griglie M7-D, M7-E, M7-F in due stati in `Mappe/ARC07-MAPPE-HAMMERFIST-372-1372.md`; gli stati del 1372 decisi con D48 lo stesso giorno)* — *prioritario per il DM (2026-10-07)*: le stesse
      mappe, con le modifiche del tempo, servono nel **1372** come campo di
      battaglia dell'invasione di Hammerfist (ARC-08): prima per la **ritirata
      progressiva** dei difensori fino al Cuore della Montagna, poi per la
      **riconquista**, quando arrivano i Rumbling Stones (`DEF-5` e ARC-08).
      Quindi ogni griglia ha due stati, 372 e 1372, e segna le vie fra un livello
      e l'altro. La sezione a livelli di Hammerfist 372 (più si
      scende, più le sale sono ampie) e le griglie da 1,5 m di fucina, gallerie,
      alchimista, cappella e armeria, coerenti con le Scene 4-5 già giocate e
      con le varianti del 1372. Si apre con `rumblingstone-mapmaking`.
      *(2026-10-08, D8 di [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md))*:
      si disegna col set di simboli nuovo (porte per tipo, grate, scale che
      salgono e scendono con `@collega`, arredi) e passa da `collaudo_mappe.py`
      e dal collaudatore di mappe prima di dirsi fatto
- [x] la **quarta lettura cieca** di DEF-4 (2026-09-30), sul testo fuso con la
      #183: tabella qui sotto, rapporti `lettura-quarta-*`
- [x] le letture a freddo dopo, e la tabella prima/dopo
- [x] un secondo giro di correzioni sui rilievi delle letture dopo che non
      toccano il canone

**La misura, prima e dopo** (letture cieche, agenti diversi a ogni giro,
stesse rubriche ripulite; rapporti in `esperimenti/def4-seconda-serata/`):

| | Lettore prima | Lettore dopo | Lettore terza | Lettore quarta | Playtester prima | Playtester dopo | Playtester terza | Playtester quarta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rilievi | 36 | 46 | 33 | **45** | 23 | 34 | 26 | **29** |
| 🔴 | 2 | 2 | 1 | **1** | 2 | 1 | 0 | **0** |
| 🟠 | 13 | 18 | 9 | **13** | 7 | 9 | 11 | **10** |
| 🟡 | 21 | 26 | 23 | **31** | 14 | 24 | 15 | **19** |

**La quarta lettura** (2026-09-30). Il playtester resta a zero 🔴. Il lettore ne
trova uno **nuovo**, che nessuna delle tre letture prima aveva visto: le
*Cronache dei Quattro Eroi* che i giocatori hanno in mano dicono già «eroi dal
futuro», mentre il nodo della targa vieta di dirlo e la porta *Sapere* dice che
la profezia è stata cancellata dalle cronache. È canone, e va al DM (D33). Il
totale del lettore risale perché questa lettura è stata la più fine (31 🟡).
Tre dei 🟠 li avevo lasciati io con la D6: il «vecchio che posa la pietra»
rimasto in due punti, e l'Aura «della Corona intera» che arriva prima che la
Corona sia intera. Corretti subito, con altri tre rilievi che non toccano il
canone: il −2 degli aiuti scritto accanto alla CD, la quantità delle bombe di
Kettra (tre, `[INFERRED]`) e il premio di Gunnvor applicato agli acquisti invece
che alle vendite. Gli altri 🟠 sono decisioni già in lista (D12, D16, D17, D19,
D21, D23), il lotto mappe (D28) o materiale fuori dal modulo (la tabella B4, il
piano di battaglia, il Registro delle Perdite).

**La terza lettura** (2026-09-27, sul testo dopo le risposte del DM a D5, D11,
D20, D24): il playtester non trova più un 🔴, il lettore uno solo, e il totale
scende per tutti e due. Il 🔴 rimasto è il ritorno a piedi senza un costo base
in tacche, cioè la D22 ancora aperta. Dei 🟠, la metà sono decisioni già in
lista (il corno, D13; le corde, D18; l'Aura, D17; il Rubino, D6), e una parte
li avevo introdotti io con le risposte del giorno: l'EL della tenda scritto 16 e
17, e i PX di Zog'tar e di Skullcrusher che non tornavano fra loro. Corretti
subito nello stesso giro, con altri sei rilievi che non toccano il canone
(le statistiche di Grask e il modo di avvicinarlo, Ascoltare e Osservare di
Zog'tar, chi legge la pergamena di *silenzio*, quanto copre una pozione da tre
minuti, il sasso di *silenzio* che scade prima del volo, un «qui sotto» che era
sopra, il drago che nel box atterrava).


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

### F3-ter · I banchi di ARC-08 e ARC-09 — ✅ (2026-10-07)

`[engine: Opus, sessione principale · effort: medio · qualità: prezzi ricalcolati a mano sull'SRD, profili PF1e verificati sulla fonte, box al metro di read-aloud-adulti]` — **C**, con due decisioni al DM (D41, D42)

Il DM, il 2026-10-06: *«cerca se ci sono aree nei luoghi dell'AP per il
mercanteggio […] crea questi mercatini, cosa vendono, il valore massimo, in modo
da non doverlo inventare al volo ogni volta»*. La norma del banco (F3-bis) era
arrivata con una sola applicazione, la fucina di Gunnvor in DEF-4. Questo lotto
è la seconda: gli archi che i master DEF non coprono ancora.

Cosa ho guardato prima: `il-banco.md`, la Scena 5 di DEF-4 col conto giocato,
il kit della Valle §2, i due audit del tesoro, le schede di Sal, Varis, il
Collezionista, Sonjak, la cella Zhentarim, il Consiglio di Rethmar, e i file di
luogo dell'arco 09. Nessun piano li copriva: PIANO-MASTER-DEF scriverà i master,
e quando li scriverà ogni banco di qui entra nella scena che gli spetta.

- [x] `08_.../ARC08-17-BANCO-HAMMERFIST-1372.md`: il banco chiuso durante
      l'assedio, socchiuso dopo la Cerimonia (Hammerfist con 90 superstiti è un
      villaggio impoverito), e le promesse della Guida messe contro i tempi di
      fabbricazione dell'SRD. Tre strade per mantenerle, con le reliquie del 372
      come proposta (D41)
- [x] `09_.../Arco-Post-Hammerfist-BANCHI-E-MERCATI.md`: nove banchi (il Cerchio,
      Dauth che cambia col calendario, la Torre di Zalkatar e il campo di Sonjak
      con un terzo della merce maledetta dall'elenco SRD, i recinti di loxo e
      centauri, Rethmar, Channathgate, Sal, il Collezionista con la sua
      clausola), più dove il banco non c'è e gli echi di ogni banco
- [x] «Damarath» letto come Rethmar (D2 di PIANO-REVISIONE-ARC09); il kit della
      Valle §2 rimanda ai banchi e dice perché Channathgate supera il tetto dei
      4.000 mo; i due indici d'arco e il quickstart di ARC-09 citano i file nuovi
- [x] misure: 9 box, nessuno oltre le 12 righe, nessuna parentesi, nessun box con
      più di un nome proprio nuovo (`fase1.py`); `ciclo_prosa segnala` 0 e 0
      dopo una correzione; `validate_prosa --strict` e `validate_lingua --strict`
      verdi; `copertura_scene --check` verde
- [ ] le letture a freddo (lettore e playtester, codice `P-ABITATO`) quando i
      banchi entrano nei master di PIANO-MASTER-DEF

### F3-quater · Le monete antiche e le locande — ✅ (2026-10-07)

`[engine: Opus, sessione principale · effort: medio · qualità: prezzi SRD verificati sulla fonte, box al metro]` — **C**, con una decisione al DM (D43)

Il DM, il 2026-10-07, dopo aver chiuso D41 (B) e D42: *«cosa succede quando i
mercanti dei luoghi si accorgono che vengono pagati con monete antiche, che
informazioni hanno, hanno conseguenze? Verifica anche le locande e simili per
dormire con i prezzi a notte, e creale per i vari quartieri delle città o
luoghi, se hanno senso di esistere»*.

- [x] D41 e D42 applicate: `ARC08-17` §2 con la strada B, i numeri di D42 marcati
      `[CANONE — DM 2026-10-07, D42]` nei banchi e in `ARC08-17`
- [x] banchi §9 · le monete antiche: cinque tipi (Thorek I, pre-imperiali di
      `DEF-1`, elfiche di Rhest, di Talar, segnate dal Collezionista), le regole
      (accorgersene, farle passare, a peso con una su dieci, da collezione a dieci
      volte come in `DEF-1`, fonderle), e luogo per luogo chi se ne accorge, cosa
      sa e cosa succede. Due righe nuove negli echi
- [x] `ARC08-17` §3: le monete di Thorek I davanti al re, e dove si dorme nella rocca
- [x] `09_.../Arco-Post-Hammerfist-LOCANDE.md`: le due locande del canone (il Ponte
      Nuovo, Ai Tre Remi) e quelle nuove, una per quartiere dove ha senso (quattro a
      Dauth, quattro a Rethmar, nove a Channathgate, compresi i balconi sul Campo),
      coi prezzi SRD per il moltiplicatore della condizione, le stanze libere,
      cosa si sente al bancone; dove non si dorme in locanda; le monete antiche al
      bancone
- [x] D43 decisa e applicata: zero monete di Thorek I in proporzione al conto, 6.250 mo di conio elfico nell'hoard di Regiarix, il prezzo da collezione solo sulle prime dieci monete

### F3-quinquies · DEF-4 da chiudere: le marcature `[INFERRED]` — 🟡 (2026-10-07)

`[engine: Opus, sessione principale · effort: alto · qualità: zero marcature senza risposta del DM, poi il giro delle quattro letture]` — **K**: ogni riga tocca il canone

Il DM, il 2026-10-07: *«continua il piano aperto per DEF-4 aggiornandolo con le
cose committate nel frattempo; fammi le domande per le parti inferred, in modo
che anche quella parte si possa sbloccare»*.

**Cosa è arrivato dopo il 30 settembre**, e tocca DEF-4:

- il **registro delle letture a freddo** (`plans/letture-a-freddo.json`, L4 di
  PIANO-AGENT-SKILLS-ESTERNE) e la lettura del **DM a freddo** del 2026-10-01
  (L5). Oggi `registro_letture.py` la dà **scaduta**: il DM ha letto un testo che
  non c'è più. Il master resta in avviso finché non ha una lettura nuova con
  impronta;
- la **revisione a due giri** (ADR-0077, L12): per DEF-4 c'è
  `plans/scrittura/revisioni-D13/REVISIONE-ARC07-DEF-4-VIAGGIO-MILLE-ANNI-r1.md`,
  con **una** modifica da approvare (un «sembra» nel box del russare del campo,
  riga 1260);
- nel testo, un'ultima nota «il box di prima» della Scena 13 era rimasta fuori
  da `<!-- storico -->` e finiva in stampa: avvolta il 2026-10-07.

**La misura di partenza** (`fase1.py`, `misura_craft`, `copertura_scene`,
`domande_developer`, 2026-10-07): 2.930 righe, 13 scene, 32 box (0 oltre 12
righe, 2 con parentesi, 2 con più di un nome proprio), congegni attivi 22 su
23 (manca solo «ADR interni al documento»), `copertura_scene` 0 rilievi,
`domande_developer` 5 rilievi tutti dichiarati, **51 marcature `[INFERRED]`** e
56 `[CANONE]`.

**Le domande.** Ogni marcatura è una domanda, raggruppate per scena. La
proposta è quella che il testo dice oggi, salvo dove scrivo «correzione»: lì il
testo ha un numero che non torna con l'SRD. Si risponde per numero («sì» tiene
la proposta).

| # | Dove | Domanda | Proposta |
|---|---|---|---|
| Q1 | Scena 4 | Con il consiglio fallito, cosa vuol dire «aiuti dimezzati»? | 2 pozioni di invisibilità invece di 4, Benedizioni a +1/+1, niente mappa del campo |
| Q2 | Scena 5 | Il dormitorio dei PG erano gli alloggi dei minatori, con la crepa chiusa col piombo? | sì, colore |
| Q3 | Scena 5 | Kettra ha **tre** bombe di fuoco sue, *palla di fuoco* 5d6, Riflessi CD 14, 750 mo l'una? | sì |
| Q4 | Scena 5 | Il chierico incappucciato è la mano del Collezionista e non si incontra in ARC-07? | sì |
| Q5 | Scena 5 | Le rune di Zeth sul modello di *dissolvi magie*: a che livello d'incantatore, e a che prezzo? | Zeth incantatore di **9°** nel 372 (proposta mia: il testo non dà un livello); prezzo da pergamena SRD (*dissolvi magie* 3° × 9° × 25 = **675 mo**, mirato o ad area) |
| Q6 | Scena 5 | Il premio di Gunnvor vale sulle **vendite** dei PG, non sugli acquisti? | sì (corretto il 2026-09-30, resta da confermare) |
| Q7 | Scena 5 | Il forziere del re paga fino a **10.000 mo**, solo con la fiducia piena e solo per cose che servono all'alba? | sì |
| Q8 | Scena 5 | Il pesatore compra il resto **a metà, in gemme, fino a 15.000 mo**; le gemme dei PG a metà prezzo? | sì |
| Q9 | Scena 5 | Le armi e armature naniche d'adamantio il forziere le paga a metà **anche oltre** il limite di 2.500 mo? | sì, è l'unica eccezione |
| Q10 | Scena 5 | Il pesatore trattiene **una moneta su dieci** del 1372, e ha Percepire Intenzioni **+8**? | sì |
| Q11 | Scena 5 | Ogni incantesimo di 4°-5° comprato stanotte toglie qualcosa alle mura: un tiro sul Registro delle Perdite di ARC-08 alla Scena 10? | sì |
| Q12 | Scena 5 | Kettra ha Sapienza Magica **+15** (prende 10, CD 25)? | sì |
| Q13 | Scena 5 | Nel 1372 nessun fabbro sa rifare il disegno di brina dell'ascia del gelo? | sì, eco |
| Q14 | Scena 5, §7 | Gli echi della fucina: le monete del 1372 murate che riemergono in ARC-08 quando si scava, e le cose vendute che tornano come reliquie? | sì |
| Q15 | Scena 6 | La pattuglia dei tre fallimenti: otto hobgoblin guerrieri di 4°, 1d6 a round per il corridore, una tacca in più | sì, con una **correzione**: otto creature di GS 3 fanno **EL 9**, non 10 (SRD, raddoppio = +2) |
| Q16 | Scena 6 | I numeri della sorveglianza del campo (sei squadre su worg fuori, ronde di orchi, squadroni hobgoblin, vedette goblin) | sì: costruiti sulle organizzazioni SRD |
| Q17 | Scena 6, blocco 3 | Se metà del gruppo fallisce Nascondersi davanti agli orchi, il blocco fallisce e conta un fallimento in più verso la pattuglia? | sì |
| Q18 | Scena 6, blocco 4 | Le vedette goblin che strillano portano il blocco dopo a CD +2? | sì |
| Q19 | Scena 6 | Grask veglia nella prima metà della notte e dorme nella seconda? | sì |
| Q20 | Scena 7 | Tagliare la tenda altrove: Ascoltare delle guardie contro Muoversi Silenziosamente di chi taglia | sì |
| Q21 | Scena 7 | Cosa fa Balvar quando comincia lo scontro: recuperato non combatte e indica la runa; in trattativa guarda un round, poi sta con chi vince; minacciato combatte | sì |
| Q22 | Scena 7 | Hald è il figlio della sorella di Balvar; ha diciannove anni ed è di guardia sul camminamento est | sì |
| Q23 | Scena 7 | Perché Balvar è con l'orda: esiliato senza processo, Abbathor, chiede che la fortezza cada in fretta e che chi si arrende sia risparmiato; e le tre ragioni per cui Zog'tar si fida | sì |
| Q24 | Scena 7-8 | La tenda vale **EL 17** con Balvar e **16** senza (conto a mano con la DMG) | sì, sapendo che è al limite: rifatto con le regole DMG (Zog'tar 15 e Balvar 13 fanno circa 16; le quattro guardie di GS 8 insieme fanno 12, e aggiungono mezzo punto) viene **fra 16 e 17**. Scritto 17 tiene il tetto di APL+4 |
| Q25 | Scena 7, 11 | Colpire la runa della Catena sotto la scaglia: regola della casa, attacco contro la CA **piena +4** (33 → 37), non di contatto | sì |
| Q26 | Scena 8 | Il sacerdote della Mano (hobgoblin adepto 7, GS 6) arriva in 1d4+1 round, con *vedere invisibilità* se ha sentito il corno, e lancia *comando* CD 13 | sì |
| Q27 | Scena 8 | Il ritorno a piedi: si rigiocano i cinque blocchi, Nascondersi CD 22 senza invisibilità, +4 se il corno ha suonato | sì |
| Q28 | Scena 8 | Zog'tar catturato sa dove colpiranno all'alba: portarlo alle mura vale un successo in più nella Scena 10 | sì |
| Q29 | Scena 8 | Se va male nella tenda: Zog'tar prende vivi i PG caduti, i nani li riprendono all'alba, il duello comincia con loro in mezzo al campo | sì |
| Q30 | Scena 8, App. A | I gradi di Zog'tar (Ascoltare 8, Intimidire 10, Osservare 0) e delle guardie (nessuno nelle due abilità) | sì |
| Q31 | Scena 9 | Vatore non ha statistiche: al primo colpo a segno il Cronolito lo porta via a fine turno, e *àncora dimensionale* non lo ferma | sì |
| Q32 | Scena 10, 11 | Se l'alba li coglie fuori e falliscono la prova, il soffio va sul PG che ha tirato peggio; e il duello fuori si gioca sulla spianata davanti alla porta | sì |
| Q33 | Scena 11 | Le corde delle gru: il gancio è un attacco di contatto a distanza contro la CA di contatto del drago (8), poi a terra si tira la corda (Forza CD 25 cooperativa, D18) | sì |
| Q34 | Scena 11 | Le balestre pesanti delle mura (1d10, 36 m, un round per ricaricare) non passano la RD 10/magia, ma il drago si gira su chi lo colpisce | sì |
| Q35 | §6 | Se attaccano la pattuglia di Durin: Durin si arrende alla prima ferita grave, la CD del consiglio sale di +4 | sì |
| Q36 | §6 | Il drago attaccato di notte sulle colline: due round per orgoglio, poi via; il danno resta, il duello comincia senza sorpresa, costa 2 tacche | sì |
| Q37 | App. A.1 | I talenti, le abilità e gli incantesimi conosciuti di Skullcrusher (otto talenti, stregone di 5°) | sì: sono quelli dell'SRD per un adulto maturo, scelti fra i suoi |
| Q38 | App. A.5 | Re Thorek I e Thorgrim non combattono; se il tavolo li porta in combattimento decide il DM | sì |
| Q39 | §8 | I PX di Skullcrusher: è la **D40** | vedi D40 |
| Q40 | F3-bis | I cinque punti rimasti senza decisione: quanto dura una tacca nel mondo, il Cronolito, la tabella B4 e le ferite ancestrali, quando Balvar usa il Fuori-Posto, gli oggetti del cortile | proposta da scrivere dopo le risposte qui sopra: dipendono da Q21, Q25 e Q31 |

Le decisioni ancora aperte per DEF-4 restano nella tabella in fondo: **D27**
(il messaggio interrotto), **D39** (l'orologio senza margine), **D40** (i PX).

- [x] le risposte del DM a Q1-Q40, D27, D39, D40, e la revisione D13
      (2026-10-07). Tutte «sì» tranne quelle qui sotto
- [x] le risposte nel testo: 49 marcature su 51 diventano
      `[CANONE — DM 2026-10-07, Qn]`. Le risposte che cambiano qualcosa:
      - **Q26**: nel 372 l'orda **non è la Mano Rossa**, è l'orda di Zog'tar
        Deatheye. Il sacerdote diventa «il sacerdote dell'orda» (e la mano
        dipinta di rosso diventa nera di fuliggine), la tabella delle forze,
        l'intestazione di Zog'tar e i due echi «un generale in più» corretti.
        Restano «Mano Rossa» solo le righe che parlano di oggetti portati dal 1372
        e l'handout delle Cronache, che è canone D33
      - **Q29**: i PG sconfitti nella tenda restano prigionieri fino all'alba, e
        durante l'esecuzione **scompaiono nel nulla**. Dove ricompaiono è Q29-bis
      - **Q37**: Skullcrusher prende il template **Avanzato** di PF1e completo
        senza alzare il GS (297 pf, CA 33, morso +30, soffio CD 28, Presenza CD
        25). `Boost log:` nel master e nella scheda del Bestiario; le cifre
        corrette anche nella Quick-Reference e nella regia della Scena 11
      - **Q15**: la correzione a EL 9 non entra: la pattuglia è di guerrieri di
        4° con due talenti, GS 4 l'uno, e otto GS 4 fanno davvero EL 10. Era un
        mio errore nella domanda (avevo preso il regular di GS 3 del Bestiario)
      - **D13**: la modifica approvata, applicata a mano (`applica` avrebbe
        ricostruito il file dal testo vecchio)
- [x] le misure dopo: `validate_modules`, `copertura_scene`, `componenti`,
      `domande_developer`, `validate_bestiario` verdi; box e congegni invariati
      (32 box, 22 su 23); marcature `[INFERRED]` da 51 a **2**
- [x] le due domande nuove *(applicate il 2026-10-07: l'incappucciato è Vatore)*: **Q4-bis** (l'incappucciato che dà i componenti a
      Zeth è un agente del Collezionista, oppure è **Vatore** stesso, che quella
      notte è nel campo?) e **Q29-bis** (dopo la scomparsa all'esecuzione, dove
      ricompaiono i PG: proposta, nel cortile quando il drago cala, feriti come
      sono, e il duello si gioca su M7-B)
- [~] il giro delle quattro letture a freddo su DEF-4 (passo 6 del ciclo), con la
      lettura del DM a freddo che rientra nel registro con l'impronta.
      *(2026-10-07: rapporti in `esperimenti/def4-giro2/`. Lettore 🔴 1 · 🟠 12 ·
      🟡 48: il 🔴 è il caso di Zog'tar vivo all'alba, che è canone; corretti
      subito i 🟠 che il testo risolve (la CA della scaglia, 41; la soglia di fuga
      allineata a D14; le Cronache del §9; dove sta la tabella B4). Le Cronache
      dicono «quando l'orda calò» su richiesta del DM, e l'handout in uso aveva
      ancora «venuti da un tempo che non era ancora», tolto come vuole D33.
      Playtester e DM a freddo rilanciati a due alla volta dopo il limite di
      richieste; il developer dopo)*. **Il giro 2, i conti**: lettore 🔴 1 · 🟠 12
      · 🟡 48; playtester 🔴 0 · 🟠 7 · 🟡 16; developer 🔴 1 · 🟠 7 · 🟡 13; DM a
      freddo 🔴 1 · 🟠 7 · 🟡 19. Corretti nel testo: CA 41 della scaglia, soglia a
      ⅓ (~100 pf, FERITO GRAVE anche nel gruppo logorato), −2 e aiuti dimezzati
      insieme, i modificatori della notte raccolti nella Scena 10, Vatore
      riconoscibile nella Scena 9. I 🔴 rimasti sono canone o forma, e vanno al DM
      come Q41-Q50. **Risposte del DM, 2026-10-07: sì a tutte**, applicate: Zog'tar
      vivo all'alba (−1 successo, e con 0-1 sale sulla breccia), le corde con le
      azioni preparate sullo stesso innesco, il riquadro «La vostra serata» in
      §0 con le righe da riempire dal registro del 25 settembre, Hammerfist di
      ottant'anni con la cinta rifatta, la posta del consiglio, Thorgrim vecchio
      e vivo, i rinforzi in 1d4+2 e 2d4+2 round, i Treant +1 successo, *ristorare*
      non toglie il −4. Il testo intero della targa l'ho scritto io: resta
      `[INFERRED]` finché il DM non lo legge. Regola nuova del DM: **un subagente
      alla volta**
- [x] i 🟡 del giro 2 (96), corretti senza domande dove il testo li risolve
      (2026-10-07). Q45 approvata dal DM: **zero `[INFERRED]`** nel master.
      Corretti: la Zona 1 e il «non dire» rimandano alla Scena 3; il portale fuori
      dalle mura; i PX in §8; la regia «più sopra»; due pietre accese alla fine
      della Scena 12; il corno si prende solo alla tenda; le pozioni a 1.650 mo
      (incantatore di 11°); il Torque sempre; i tempi al tavolo negli atti II e
      III; Grask sveglio fino alla 4ª tacca; la targa incisa stamattina; la
      CA di Zog'tar da 24 a **22** (l'armatura completa limita la DES a +1,
      anche nel Bestiario); «Volare» e il tiro contrapposto dell'Appendice C. Gli
      altri 🟡 sono mappe (D28: l'orientamento di M7-A, gli oggetti del cortile, le
      posizioni nella tenda) o materiale da aggiungere (statistiche delle comparse
      del campo, diversivi, un gesto per gli altri tre PG nel rito): restano per il
      giro 3
- [x] Zog'tar Avanzato PF1e completo senza alzare il GS (2026-10-07, il DM: deve
      reggere più di due round contro questi PG e questi artefatti): 283 pf, 328
      in Ira, CA 24, ascia +29 (3d6+22). La tenda resta a EL 17, il tetto.
      `Boost log:` nel master e nel Bestiario. Skullcrusher era già Avanzato (Q37)
- [x] Zog'tar rifatto su richiesta del DM (2026-10-07): Barbaro 14 / Guerriero 1
      (stessi 15 DV e pf), RD 3/—, Volontà Indomita, armatura completa di
      mithral (CA 26), Colpo Devastante al posto di danno in più, per non
      uccidere Artemis in un colpo. La tenda è alta 6 m al palo e 3 m ai lati;
      contro chi vola: giavellotti, il palo abbattuto, *dissolvi magie*,
      *comando*. **Il drago sulla tenda**: il corno è magico (la runa gemella
      della Catena), il drago arriva in circa 70 round, e se trova Zog'tar o le
      guardie in piedi entra nello scontro, EL 18-19, voluto dal DM, con l'avviso
      e l'uscita scritti
- [x] il lotto mappe D28 (2026-10-08; è di F3-bis, vedi sopra)
- [ ] **subito**: il giro 3 delle letture su DEF-4, un subagente alla volta
- [ ] il passo 7: il ricordo del giorno dopo, e il quiz con la chiave già
      approvata (D1)

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

- [x] DEF-5 per primo, passi 1-6 (2026-09-30). Tre scene `### SCENA` col
      contratto «In scena»; schede d'entrata di Re Thorek e Madre Dana (da
      `ARC08-01-GUIDA-DM` e dal Bestiario, niente di inventato); i box riscritti
      al metro; l'accensione del Rubino, che DEF-5 metteva «sulle mura», torna
      su richiesta del DM in DEF-4 Scena 13, in tre battute con la voce di
      Moradin, e DEF-5 parte dal filo; la Tempra (il contraccolpo del salto, `[INFERRED]`);
      l'orco dell'SRD per la pulizia; il gesto a testa nel round di sorpresa.
      Letture a freddo prima di toccare (`esperimenti/def5-ciclo/`): lettore 46
      rilievi (🔴 3), playtester 18 (🔴 1). Due 🔴 su tre del lettore erano la
      stessa contraddizione dell'orologio, che è canone (D31); il terzo, l'ordine
      dei box, è corretto. **Dopo** le correzioni, agenti nuovi: lettore 46 → **35**
      (🔴 3 → **1**), playtester 18 → **17** (🔴 1 → **1**). L'unico 🔴 rimasto,
      in tutte e due, è l'orologio: la D31, che è canone. Quattro 🟠 della
      seconda lettura li avevo introdotti io (il bonus del re che si somma, la
      scala dei re in una caverna con un solo ingresso, l'*Aura di Comando* su
      più bersagli, il capo degli orchi senza statistiche) e sono corretti.
      Resta il **passo 7** (il quiz, D10)
- [~] **DEF-1, DEF-2, DEF-3 nella forma, passi 1-4 (2026-09-30).** Scene
      `### SCENA` (10, 5 e 8), contratto «In scena», Comparse, schede
      d'entrata di Fauci di Diamante, la Madre Cristallo, Varis e Terros
      (solo da testo e Bestiario), apparati generati, i tre profili in
      `copertura-scene.json` a contratto. Nessuna parola dei box letti al
      tavolo è cambiata: quattro box d'ingresso sono spostati nella scena in
      cui si entra nel luogo. Il §2-bis e il §8-bis di DEF-3 e il §7 di DEF-2
      restano fuori dalle scene, con la ragione nel profilo. **Passo 5 fermo
      su D9** (6 box di DEF-1 e 1 di DEF-2 oltre 12 righe). **Passo 6 in
      corso**: letture cieche in `esperimenti/f4-def1-def3/`, DEF-1 lettore
      40 rilievi (🔴 2), DEF-2 lettore 37 (🔴 2), DEF-2 playtester 27 (🔴 2),
      DEF-3 lettore 46 (🔴 1) e playtester 34 (🔴 2), DEF-1 playtester 40
      (🔴 1: Tordek solo contro la Sentinella, D37). I tre 🔴 di DEF-3 sono il rito quando va male: canone, D35. Corretti i 🔴 che il testo risolve (stato al
      tavolo, riposo già giocato, orologio 3g 20h, portale A6 prima del rito,
      canone del DM il 2026-09-30) e sei 🟠 (Radice a Terra, rifugio di Fauci, runa di Varis,
      Volare di PF1e, Therysol donna, il sogno nella Stanza, canone del DM).
      Resta aperto il 🔴 del salto verso il Tempio (DEF-1 Scena 6): D34. I 🟠
      di regole che chiedono canone sono D36
- [x] **Le decisioni del DM del 2026-09-30, applicate.** D7, D12, D14-D17,
      D19, D21, D23, D25, D29-D33 in DEF-4 e DEF-5 (più il registro dell'orologio
      di DEF-2 e l'handout delle Cronache), D34 in DEF-1 Scena 6. Brynja resta
      di 9° livello; la pietra di *silenzio* è incantata all'8° (8 minuti, 160
      mo: la prima stesura diceva 8 round, ed era sbagliato). D8 (il Riflessi del Drappo) entra con F5. D10 e D26 sono metodo: il
      quiz non si fa sulle conversioni di sola forma, il cancello del registro
      delle letture è L4 di [PIANO-AGENT-SKILLS-ESTERNE](PIANO-AGENT-SKILLS-ESTERNE.md), fatto il 2026-10-01: `plans/letture-a-freddo.json` e `registro_letture.py --check` in CI, in avviso finché un master non ha le letture con impronta, poi bloccante. **D9, passo 5**: il DM ha confermato «spezzali»;
      DEF-1 e DEF-2 hanno zero box oltre 12 righe, nessuna parola cambiata
- [~] **Il giro delle quattro letture su DEF-4 e DEF-5, e la procedura (2026-09-30).**
      Su richiesta del DM: lettore, playtester, developer e un **DM a freddo**
      (rubrica nuova, `rumblingstone-playtest/references/dm-a-freddo.md`: legge
      scena per scena senza guardare avanti, e il giorno dopo scrive cosa
      ricorda, un'idea presa da *first-reader*, Apache 2.0). Il giro diventa il
      passo 6 del ciclo in `module-standard`, «Il giro»: triage in testo,
      prosa con `narrative-style`, canone al DM, e di nuovo il giro finché non
      restano 🔴. Primo giro in `esperimenti/giro-def4-def5/`: DEF-5 lettore 0
      🔴, playtester 1, developer 1, DM 0; DEF-4 lettore 2, DM 1 (playtester e
      developer rilanciati dopo il limite di sessione). Corretto quello che il
      testo risolve; scritta la prosa che mancava (l'handout «Lo Stato dei
      Custodi», il chierico incappucciato, Hald); l'assedio di DEF-5 è D38.
      Dai report di DEF-4 arrivati dopo: il 🔴 del developer era vero (il morso
      ha portata 4,5 m, e l'azione preparata «quando scende» non scatta mai per
      un nano) e ora l'azione si prepara sul round in cui le corde lo
      inchiodano. Il 🔴 del playtester sull'orologio è D39, i PX sopra la
      tabella SRD sono D40, le mappe M7-B e M7-C sono il lotto D28. **Resta da
      fare il giro 2**, dopo D39 e il lotto mappe: finché quelli sono aperti, i
      due 🔴 tornerebbero identici
- [ ] DEF-1 (Varis), DEF-2, DEF-3: i residui dichiarati, prima che un gruppo
      nuovo li riprenda. Sono **già giocati** (`copertura-scene.json`): si
      convertono nella forma (titoli `### SCENA`, contratto, componenti, box al
      metro) e non in cosa succede, che per questo gruppo è già canone
- [ ] per ognuno, alla fine: lettore e playtester a freddo senza 🔴, quiz con la
      chiave approvata dal DM, e la riga tolta da `plans/copertura-scene.json`
- [x] **DEF-5 è la prova cieca di `P-ABITATO`** (ADR-0075, «La prova contro il
      tavolo»), **riuscita** il 2026-09-30: il playtester, senza la tabella, ha
      trovato da solo il buco (#13): dopo la pulizia i PG sono in una fortezza
      abitata, e il modulo dà solo chi comanda e chi cura; mancano rimedi,
      armi, messaggi, guardia, chi compra il bottino e chi identifica. La
      domanda resta com'è. La tabella in DEF-5 però **non** l'ho aggiunta: la
      fortezza del 1372 è quella dell'ARC-08, e cosa c'è a Hammerfist lo decide
      la Fase 0 (D31)

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
| ~~D6~~ | F3 | ✅ **Decisa il 2026-09-28** (il DM: *«il Rubino appare alla vittoria»*): nessuno lo porta, si forma sull'incudine nel momento della vittoria, e nessun nano del 372 sa spiegarlo. Riscritti il box dell'incudine e le note della Scena 12. Il Rubino **si usa una volta sola**, per il ritorno, e **la Corona si completa dopo l'uso** (precisazione del DM lo stesso giorno): all'incudine la Corona resta a +2 e muta, il +3 e la Senzienza arrivano all'arrivo nel 1372 (`DEF-5` §3, dove sono passati il Momento 2 e il box della corona intera). Allineati `campaign-artifacts.md`, la scheda del giocatore e le pagine S3 della Corona (r7) |
| ~~D7~~ | F3 | ✅ **Decisa il 2026-09-30**: Balvar era già runaio, ma di altre fortezze: è arrivato a Hammerfist, giovane, perché era un mastro runaio. La fortezza resta giovane. Era: **La fortezza «giovane, appena eretta» e Balvar che ne è stato il runaio** prima dei bisnonni dei nani di oggi: una delle due cose va cambiata. È aperta anche in `PIANO-CHIUSURA-DEI-MILLE-ANNI` M7 |
| ~~D8~~ | F5 | ✅ **Decisa il 2026-09-30**: sì al Riflessi (la caduta nella curva); la Volontà solo se il DM la vuole. Era: **Il Drappo vuole un Riflessi e una Volontà?** `domande_developer` non ne trova nessuno sull'intero modulo. Proposta: il Riflessi sì (la caduta nella curva), la Volontà solo se il DM la vuole in un modulo d'intrigo |
| ~~D9~~ | F4 | ✅ **Decisa il 2026-09-30**: si spezzano, senza cambiare una parola. Fatto: sei box di DEF-1 e uno di DEF-2, oggi zero box oltre 12 righe (due erano note per il DM in corsivo e righe `storico` dentro la citazione, uscite dal box). Era: **Nei master già giocati (DEF-1, DEF-2, DEF-3) i box oltre 12 righe si spezzano?** Il passo 5 del ciclo li vuole ≤ 12; DEF-1 ne ha 6, DEF-2 uno. Spezzarli in battute non cambia una parola, ma tocca prosa già letta ai giocatori, ed è la D3 ancora aperta di MESTIERE-BANCHI. Proposta: sì, solo spezzare, come il box di Balvar in DEF-4; mai riscrivere cosa dicono |
| ~~D10~~ | F4 | ✅ **Decisa il 2026-09-30**: sì alla proposta: niente quiz sulle conversioni di sola forma di DEF-1, 2, 3; il quiz sui master nuovi e su quelli riscritti nella prosa (ADR-0075). Era: **Il quiz a due agenti (passo 7) va fatto su ogni master?** Ogni quiz chiede una chiave approvata dal DM: con ARC-07, ARC-08, ARC-09 e gli stand-alone sono una ventina di chiavi. Proposta: sì sui master nuovi e su quelli riscritti nella prosa; no sulle conversioni di sola forma dei master già giocati (DEF-1, 2, 3), dove bastano lettore e playtester. Saltarlo lì è una decisione del DM, e va scritta (ADR-0075) |
| ~~D11~~ | F3-bis | **I numeri del campo, delle guardie e di Zog'tar.** *(2026-09-27, risposta del DM)*: fuori girano i lupi, dentro le ronde di hobgoblin, orchi e goblin senza lupi; gli sciamani gli esploratori non li hanno visti, ma possono esserci. Scritto in DEF-4 Scena 6: sei squadre di cavalieri su worg sull'anello esterno, ronde di orchi, squadroni hobgoblin e vedette goblin dentro, con i numeri SRD (worg, orco, goblin, hobgoblin); circa quindici sciamani (adepti orchi di 5°) che dopo il corno lanciano *vedere invisibilità*; un sacerdote della Mano (hobgoblin adepto 7, GS 6) nella tenda accanto a Zog'tar, EL della tenda sempre 16. La pattuglia dei tre fallimenti ha i suoi numeri (guerriero 4 SRD). Tutto `[INFERRED]` fino al tuo OK. ✅ **Zog'tar, decisa lo stesso giorno** (il DM: *«lo voglio con l'Ira Superiore, e tosto: deve reggere più di un round»*): Barbaro 11 / Guerriero 4, GS 15, 253 pf (298 in Ira), numeri ricalcolati sull'SRD, `Boost log:` nel Bestiario; la tenda arriva a EL 17, il tetto. E **Balvar**, stessa data (il DM: *«sì, certo»*): abilità nel suo statblocco del Bestiario, ricopiato in DEF-4; Percepire Intenzioni +13 (8 gradi fuori classe + SAG), gli 80 punti spiegati, `[INFERRED]` perché il ritmo del Runecaster è del FRCS |
| ~~D12~~ | F3-bis | ✅ **Decisa il 2026-09-30**: la pietra la incanta Sorella Brynja, chierica di 9° livello, ma all'8°: *silenzio* dell'SRD, 1 minuto per livello, cioè 8 minuti, e 160 mo (servizio SRD: livello dell'incantesimo × livello dell'incantatore × 10 mo). Brynja resta di 9°. Copre il volo di andata e la tenda. *Corretto il 2026-09-30 su segnalazione del DM: la prima stesura diceva 8 round*. Era: **La pietra del silenzio della variante dall'alto: chi la dà, e quanto dura?** Nessuno la vende. Proposta: Brynja, alla cappella, lancia *silenzio* su un sasso; dura un round per il suo livello, quindi basta per l'atterraggio e la tenda, non per il volo intero. Serve il livello di Brynja |
| ~~D13~~ | F3-bis | ✅ **Decisa il 2026-09-28**: il corno sta nella **custodia col glifo**, e la custodia è **incatenata al polso di Grask**: chi la tocca lo sveglia anche se dorme. Le ore di veglia e di sonno (prima metà della notte sveglio, seconda a −10) sono una proposta `[INFERRED]`. Resta aperta la seconda metà della domanda: dopo un allarme di notte, il drago va sulle colline o sul campo? |
| ~~D14~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì alla proposta: fuga a metà pf = FERITO GRAVE; la Catena spezzata vale FERITO GRAVE se il drago aveva già perso un terzo dei pf; a ⅓ dei pf fugge al suo turno, salvo due colpi subiti nel round prima. Era: **Due esiti del duello senza casella.** Se Balvar è morto il drago fugge a metà pf: conta come FERITO GRAVE o FUGGITO? E la Catena spezzata dà «FUGGITO garantito», che per il carry-over B4 è l'esito più debole: è voluto? Proposta: fuga a metà pf = FERITO GRAVE; la Catena spezzata vale FERITO GRAVE se il drago aveva già perso almeno un terzo dei pf. E la fuga a ⅓ dipende da «se i PG premono o allentano», che non è una regola. Proposta: a ⅓ dei pf fugge al suo turno, a meno che nel round prima abbia subito almeno due colpi |
| ~~D15~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: il duello crolla con due PG a terra nello stesso round, o con il gruppo che si ritira dal cortile. Era: **Quando il duello «crolla» e intervengono gli avi (§6)?** Non c'è una soglia. Proposta: due PG a terra nello stesso round, oppure il gruppo che si ritira dal cortile |
| ~~D16~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: vince l'esito del duello, gli altri tre colorano la prima frase della Corona. Era: **Il tono del Rubino è deciso in quattro posti** (la targa nella Scena 3, come muore Zog'tar nella Scena 8, l'esito del duello in §7, il «vinto sporco» in §6). Quale vince? Proposta: vince l'esito del duello; gli altri tre colorano la prima frase della Corona |
| ~~D17~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: l'Aura dura fino all'alba del giorno dopo, quindi arriva a DEF-5. Era: **L'Aura della Forgia «dura fino all'alba», ma il rito si fa già all'alba.** Proposta: fino all'alba del giorno dopo, e quindi i PG arrivano a DEF-5 con *Possenza Divina* e *Protezione dal Male* ancora addosso, oppure fino al ritorno col Rubino |
| ~~D18~~ | F3-bis | ✅ **Decisa il 2026-09-28**: prova di **Forza CD 25**, con gli aiuti SRD di chi tira insieme (+2 a testa), l'ala inchiodata per un round. Le corde sono quelle delle **gru sulle mura** `[INFERRED]`; fuori dalle mura restano quelle degli arieti rovesciati |
| ~~D19~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: i nani capiscono il nanico antico a fatica (il senso, non le sfumature), Thorik lo legge. Era: **Chi del gruppo capisce il nanico antico?** Balvar parla solo quello, e la trattativa della Scena 7 si regge su chi lo capisce. Oggi il modulo nomina solo Thorik come lettore. Proposta: i nani lo capiscono a fatica (tutto il senso, non le sfumature), Thorik lo legge |
| ~~D20~~ | F3-bis | ✅ **Decisa il 2026-09-27**: al tavolo hanno fatto il consiglio e il giro della fortezza (fucina, alchimista, cappella, rune di Zeth): **3 tacche** segnate: sono scesi da Zeth nelle gallerie (DM, 2026-09-28). Non hanno dormito. Il «campo di corsa» resta senza regola, ma con 6 tacche per il sonno la scelta non si pone più |
| ~~D24~~ | F3-bis | ✅ **Decisa il 2026-09-27** (il DM: *«forse 6 tacche»*): dormire otto ore vale **6 tacche**. Con il consiglio segnato, chi dorme non fa in tempo a fare il campo prima dell'alba. (b) chiusa il 2026-09-28: al tavolo del 31 luglio i pf **non** sono tornati pieni, quindi vale l'SRD già scritto in DEF-2 |
| ~~D25~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì a tutti e tre: (a) −2 ad attacchi e prove, senza la parola «confusi»; (b) il banchetto dà +1 ai TS; (c) con le campane suonate il drago perde il round di sorpresa della picchiata (Ascoltare CD 20). Era: **Tre rilievi di regole della prima lettura a freddo (2026-09-25) mai chiusi**, trovati rileggendo i rapporti vecchi. Il riposo breve era il quarto, e il playtester l'aveva già visto (#13). **(a)** Scena 1: «confusi 1d4 round (−2…)» è la condizione *confuso* dell'SRD o un −2? Proposta: *frastornato* non basta, quindi un −2 a attacchi e prove, scritto senza la parola «confusi». **(b)** Il +1 morale del banchetto e il +2 morale delle Benedizioni **non si sommano** in 3.5 (stesso tipo): proposta, il banchetto dà il +1 ai TS, dove le Benedizioni non arrivano. **(c)** Scena 11: «togliere al drago il vantaggio del suono in picchiata» non ha un numero. Proposta: con le campane suonate il drago perde il round di sorpresa della picchiata (ascoltare CD 20 per sentirlo arrivare) |
| ~~D26~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì alla proposta: il registro delle letture a freddo in JSON e il cancello in CI che chiede una lettura nuova quando il master cambia. È un lotto da aprire. Era: **Il giro lettore, playtester e developer in automatico.** Oggi è obbligatorio (ADR-0075) ma lo ricorda solo il piano, e il riposo breve dimostra che un rilievo 🟡 può restare nel testo per giorni. Proposta: un registro in `plans/`, le letture a freddo in JSON, con per ogni master DEF, l'impronta del testo letto e i rilievi con il loro stato (corretto, residuo con ragione, domanda al DM); un cancello in CI che fallisce se il master è cambiato dopo l'ultima lettura, o se un rilievo 🔴 o 🟠 non ha uno stato. La lettura la fa un agente, non la CI: il cancello dice solo *quando* va rifatta. Costo: ogni modifica a un DEF, anche un refuso, chiede una lettura prima del merge, salvo una dichiarazione «modifica di sola forma» |
| ~~D27~~ | — | ✅ **Decisa il 2026-10-07**: non c'era niente da considerare: il DM chiude la domanda. Era: **Il messaggio del 2026-09-27 si interrompe a «considera che i…».** Cosa andava considerato? |
| ~~D28~~ | F3-bis | **La mappa di Hammerfist nel 372, dall'alto in basso.** Il DM, 2026-09-27: *«in ogni regno nanico, più si scende e più le stanze sono ampie, soprattutto le fucine grandi, come Erebor sotto la Montagna. Magari una mappa, anche con i camminamenti e le gallerie che le rune di Zeth riempiono come difesa contro un assalto interno, e il contorno delle mura esterne»*. Tre cose da decidere prima di disegnare: **(a)** che tipo di mappa (una sezione verticale a livelli, da consultare, o una griglia tattica da 1,5 m per giocarci sopra); **(b)** le rune di Zeth nelle gallerie sono già in gioco la prossima serata, con un effetto meccanico (per esempio un *glifo di interdizione* per corridoio), o solo colore; **(c)** la Scena 5 già giocata descrive tre forge e gallerie strette puntellate da poco: la fucina grande sta **sotto** quella giocata, oppure si riscrive il box. Proposta: (a) una sezione a livelli per il DM, più la griglia del solo cortile e delle mura, che c'è già (M7-B); (b) colore fino al 1372, dove Zeth è il Ghostlord; (c) la fucina grande sta sotto, e la si vede scendendo da Zeth  *(2026-09-28, il DM)*: la mappa è della **fucina, delle gallerie sotterranee, dell'alchimista, del chierico e dell'armeria**, e deve combaciare con il modulo, con le modifiche che il tempo porta (372 e 1372). ✅ **(a) decisa il 2026-09-28**: una **sezione a livelli** per il DM e le **griglie tattiche da 1,5 m** di fucina, gallerie, alchimista, cappella e armeria, con le varianti 372 e 1372. Il disegno è un lotto a sé (checklist F3-bis, con `rumblingstone-mapmaking`); resta aperta la (b), le rune di Zeth sui camminamenti con un effetto meccanico o solo colore |
| ~~D21~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: con 8 tacche o più la Scena 10 non si gioca, le mura valgono «a stento»; Muoversi Silenziosamente CD 20 fallito fa partire il duello col bersaglio già scelto dal drago. Era: **Con 8 tacche o più, la Scena 10 si gioca?** Il modulo fa cominciare il duello fuori dalle mura, ma non dice se la prova delle mura salta né quale esito vale. Proposta: la Scena 10 non si gioca, le mura valgono «a stento» (2-3 successi), e un fallimento della prova di Muoversi Silenziosamente CD 20 fa partire il duello con il drago che ha già scelto il suo bersaglio |
| ~~D22~~ | F3-bis | ✅ **Decisa il 2026-09-28**: il ritorno a piedi costa **1 tacca** di base, più una per blocco fallito. Chiude l'unico 🔴 della terza lettura |
| ~~D23~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: Balvar recuperato può sciogliere la Catena, ma solo toccando la scaglia, nel cortile durante il duello, e lo sa. Era: **Un Balvar recuperato può sciogliere lui la Catena?** È la prima cosa che un tavolo gli chiede. Oggi il modulo dice solo che spiega dove sta la runa e come si spezza. Proposta: può, ma solo toccando la scaglia, cioè nel cortile durante il duello, e lo sa |
| ~~D29~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: dopo un allarme il drago va sulle colline e torna solo al corno successivo. Era: **Dopo un allarme di notte, il drago dove va?** È la metà di D13 rimasta aperta: il testo dice «se ne va», senza scegliere fra le colline e il campo. Proposta: sulle colline, come ogni notte, e torna solo al corno successivo; così un allarme brucia il corno e non porta il drago sopra la tenda |
| ~~D30~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: colore nel 372, difese del Ghostlord nel 1372. Era: **Le rune di Zeth sui camminamenti e nelle gallerie hanno un effetto meccanico la prossima serata, o sono colore?** È la (b) di D28, che la forma della mappa non chiude. Proposta: colore nel 372 (Zeth scrive in fretta e da un uso, e quelle le ha date ai PG), e nel 1372 sono le difese del Ghostlord |
| ~~D31~~ | F4 | ✅ **Decisa il 2026-09-30**: l'arrivo nel Cuore della Montagna è fisso; l'orologio decide cosa succede sopra, e cioè la prima ondata già passata. Si toglie «all'istante di partenza». Era: **L'orologio di DEF-5 si contraddice** (🔴 del lettore e del playtester a freddo). Il modulo dice che il Rubino riporta i PG «all'istante di partenza» e che il viaggio non consuma orologio; dice anche che li deposita nell'istante in cui le porte del Cuore della Montagna cedono e la fortezza sta per cadere; e la tabella dei rami dice che con 3g 15h le mura sono intatte e c'è tempo per la Fase 0. Tre cose che non stanno insieme. Proposta: il **Cuore della Montagna è fisso** (è il «punto più nero» che il Rubino sceglie, e la cucitura con ARC08-11), e il ramo dell'orologio decide **cosa c'è sopra**: le mura intatte e la Fase 0 piena, o la prima ondata già passata. Si toglie «all'istante di partenza» |
| ~~D32~~ | F4 | ✅ **Decisa il 2026-09-30**: sì: il Cuore di Moradin fa parte della Forgia e non entra nella meccanica del ritorno; l'ancora è la Forgia. Era: **Il Cuore di Moradin è speso o fa da ancora?** DEF-5 lo dà SPESO per la resurrezione di Hella, e nello stesso §3 lo fa agganciare gli spiriti dei PG «nella Forgia del 1372». Proposta: l'ancora è la **Forgia** (il luogo), non l'artefatto speso; si toglie il Cuore dalla meccanica del ritorno |
| ~~D33~~ | F3-bis | ✅ **Decisa il 2026-09-30**: sì: la targa dice «quattro eroi dal fuoco e dalla pietra» in tutti e tre i punti; le Cronache dicono «quattro eroi» senza «dal futuro», e il «dal futuro» lo capisce il tavolo. Era: **La profezia: le Cronache in mano ai giocatori dicono già «eroi dal futuro»** (🔴 della quarta lettura di DEF-4). Il nodo della targa vieta di dire che la profezia parla di loro, la porta *Sapere* dice che è stata cancellata dalle cronache del 1372, e il testo della targa ha tre versioni («dal futuro», «dal fuoco e dalla pietra», e quella lunga del re). Proposta: la targa dice **«quattro eroi dal fuoco e dalla pietra»** in tutti e tre i punti; le Cronache che i giocatori hanno parlano di «quattro eroi» senza «dal futuro», e il «dal futuro» lo capisce il tavolo |
| ~~D34~~ | F4 | ✅ **Decisa il 2026-09-30**: Tordek salta da un detrito sopra l'oceano, a metà strada; il Tempio è a 40 m; la strada si crea suonando il Diapason e tenendo la musica, con prove che sollevano blocchi dall'oceano. Quante prove e cosa costa un fallimento restano `[INFERRED]` nel master. Era: **DEF-1 Scena 6: da dove parte il salto verso il Tempio, e quanto è lontano?** (🔴 del lettore a freddo). Il modulo dice il portale a 50 m sopra l'oceano e i detriti fluttuanti, ma non la distanza dalla riva né da dove salta Tordek; la mappa T-4 lo fa partire dal pelo dell'oceano. Proposta: una catena di detriti parte dalla riva e sale fino al portale; ogni balzo è Saltare CD 25 (circa 7,5 m in 3.5), a ~20 m dal portale la gravità del Tempio cattura chi salta; il Tempio ruota sopra l'oceano a circa 40 m dalla riva, cioè sei-sette balzi |
| D35 | F4 | **DEF-3, il rito quando va male** (i due 🔴 del playtester a freddo). **(a)** Gli Step 1-3 falliti dicono solo «riprova» (−2 cumulativo, 2d6 non letali, −10 min), senza tetto né uscita, e Conoscenze e Utilizzare Oggetti Magici senza gradi non si tirano oltre CD 10. Proposta: ogni step si ritenta al massimo tre volte, ognuna costa 10 minuti; al terzo fallimento lo step riesce lo stesso e il suo esito ❌ della regia resta come prezzo. Chi non ha gradi può usare la prova grezza della caratteristica (SAG per l'Invocazione, CAR per la Stabilizzazione) con −4. **(b)** Con 0 successi allo Step 5 il modulo apre «un'indagine di un'ora» ma non dice cosa fanno i PG trovata la risposta. Proposta: la risposta è occupare il Sud vuoto (un PG, o Therysol); fatto questo lo Step 5 si ritira una volta, con 2 successi su 3 |
| D36 | F4 | **I 🟠 di regole di DEF-1, DEF-2 e DEF-3 che chiedono canone**, raccolti dalle letture a freddo del 2026-09-30 (`esperimenti/f4-def1-def3/`). **(a)** DEF-1: la Benedizione «ignora le penalità» ma la tabella della gravità le applica ridotte (−25%, −5): vale la tabella? **(b)** DEF-1: polvere ogni 10 minuti e stalattiti ogni 15 per tutto il viaggio, o solo come evento del d6? Proposta: solo come evento del d6, più la prova di gruppo per zona. **(c)** DEF-1: la via B contro gli Xorn non ha CD. Proposta: Intimidire o Diplomazia CD 18, come la via C; fallita, gli Xorn non sono accerchiati e si combatte senza il bonus. **(d)** DEF-1: al terzo fallimento di Thorik nel rito lo Smeraldo si incastona comunque? Proposta: sì, e il prezzo sono i malus già scritti. **(e)** DEF-2: il +1 sacro al rito viene dal toccare l'incisione o dal dormire nella Stanza? **(f)** DEF-3: la soglia dei 3 su 3 è «se Thorik rifiuta» nella Quick-Reference e «uno o nessun dono» nel §5: vale il §5? |
| D37 | F4 | **DEF-1 Scena 7: Tordek da solo contro la Sentinella, e se cade?** (🔴 del playtester a freddo). L'anticamera immobilizza Thorik (Forza CD 28, che lui al massimo fa 27) e lascia Artemis prono e indifeso: se Tordek va a 0 pf il modulo non dice cosa succede, e gli altri due passano la scena senza agire. Proposta: la Sentinella è una prova, come Terros è un voto: quando Tordek cade la Magnetite si spegne, la Sentinella torna immobile, e si può ritentare dopo un riposo (−12 h). E per gli altri due un'azione possibile: Thorik può liberarsi con la CD 28 grazie all'aiuto di Artemis (+2), Artemis può parlare, e un suo incantesimo senza componenti somatiche passa |
| ~~D38~~ | F4 | ✅ **Decisa il 2026-10-03**: la proposta. La Fase 0 dell'ARC-08 si gioca dopo il drago ai bastioni (prima il Cuore, poi Fauci, poi il consiglio di guerra), e l'aura dell'Apparizione è la presenza terrificante dell'SRD: ogni orco tira, chi fallisce è in panico, chi fa 20 è scosso. Applicata a `DEF-5` §0-bis, Scena 2, Scena 3 e CM-1. Era: **DEF-5: quando si gioca la Fase 0 dell'ARC-08?** (🔴 del playtester e del developer a freddo, 30 settembre). DEF-5 fa arrivare i PG nel Cuore della Montagna nell'ultima resistenza, col drago sulle mura e il riposo impossibile; la tabella dei rami prometteva una Fase 0 (consiglio di guerra, preparativi) prima della battaglia. Dopo D31 «sopra la prima ondata è già passata» le due cose non stanno insieme. Proposta: la Fase 0 si gioca **dopo** il drago ai bastioni: prima il Cuore, poi Fauci, poi il consiglio di guerra per le ondate che restano. E l'aura dell'Apparizione segue l'SRD della presenza terrificante: ogni orco tira, chi fallisce (quasi tutti, con Volontà −2 contro CD 25) è in panico, chi fa 20 è scosso; la Scena 3 si gioca con i pochi che restano e con i nemici che arrivano dopo (CM-1) |
| ~~D39~~ | F4 | ✅ **Decisa il 2026-10-07**: (b): parlare con Balvar **durante** lo scontro nella tenda non costa tacche; prima di colpire costa ancora 1. Applicata nell'orologio della notte di DEF-4. Era: **L'orologio di DEF-4 non ha margine.** Con le 3 tacche già spese dal gruppo di oggi, parlare con Balvar (1) o fallire un solo blocco del campo porta a 8 tacche: l'alba fuori dalle mura, e la Scena 10 non si gioca. Lo dicono sia il playtester sia il developer del giro 1. Proposta: **(a)** la soglia 🔴 passa a 9 tacche; **(b)** parlare con Balvar costa 0 se lo si fa durante lo scontro nella tenda; **(c)** si lascia così: l'alba fuori è l'esito più probabile, ed è voluto |
| ~~D40~~ | F4 | ✅ **Decisa il 2026-10-07**: (b): il duello al conto SRD, 1.460 PX a testa; il totale del beat scende a ~6.360, e il 14° arriva dopo DEF-5. Applicata in DEF-4 §8; DEF-5 §8 va rifatto con questa cifra. Era: **I PX del beat sono circa tre volte la tabella SRD** (Skullcrusher: 5.400 a testa scritti, ~1.460 da tabella). Il 14° livello di DEF-5 poggia su quella cifra. Proposta: **(a)** si tiene la cifra come premio di storia, detto apertamente; **(b)** si scende al conto SRD, e il 14° arriva dopo DEF-5 |
| ~~D41~~ | F3-ter | ✅ **Decisa il 2026-10-07**: strada **B**. Il re dà il Giorno 21 le reliquie vendute a Gunnvor nel 372 e copre la differenza in gemme, fino a 10.000 mo per PG; vale anche la tacca nel legno del conto. Applicata in `ARC08-17` §2-§3 |
| ~~D42~~ | F3-ter | ✅ **Decisa il 2026-10-07**: sì a tutto. Profili PF1e di Rethmar, Dauth e Channathgate, le casse, i loxo, la Cintura del monaco come premio del Torneo, il Tempio di Rethmar con un chierico di 13° e un diamante. Marcati `[CANONE — DM 2026-10-07, D42]` nei banchi e in `ARC08-17` |
| ~~D43~~ | F3-quater | ✅ **Decisa il 2026-10-07** (il DM: *«1 calcola in proporzione, 2 ok»*). **(a)** In proporzione al conto della fucina le monete di Thorek I in tasca ai PG sono **zero**: la borsa al momento di pagare (10.000 in monete del 372, 6.314 in gemme, 19.603 in monete del 1372) è uguale ai conti (35.917), quindi tutto torna ai nani. **(b)** Sì: un quarto delle monete dell'hoard di Regiarix è conio elfico, **6.250 mo**, nella stessa proporzione delle reliquie di Rhest sul tesoro non magico. Applicata nei banchi §9 e in `ARC08-17` §3 |
| ~~D44~~ | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie la proposta). **Da dove escono i PG di notte?** La **postierla** è nel muro sud, all'angolo sud-est, sotto la torre est: esce verso il fianco est del campo, col bosco come riparo. Corregge M7-A, che la dava a nord |
| ~~D45~~ | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM: *«ci sono più fucine»*, poi lo schema proposto). **Le fucine di Hammerfist nel 372**: tre, una per livello. La **fucina originale** (la prima forgia) apre sul cortile: è quella che i Bracieri di Tordek riconoscono, dove si spinge il drago (Scena 11) e da cui viene l'incudine del rito (Scena 12); la **fucina di Gunnvor**, tre forge, dentro la montagna sul corridoio di cappella, alchimista e quartieri (Scena 5); la **fucina grande**, sotto le gallerie di Zeth, la più ampia. Chiude la (c) di D28 |
| ~~D46~~ | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie la proposta). **La fortezza del 372 rispetto a quella del 1372**: è il **nucleo**. Esistono già il cortile (M7-B, che nel 1372 diventa il cortile interno), mura più basse (+4,5 m) e le sale nella montagna; fossato, cortile esterno, torri da 20 m e bastioni vengono nei secoli dopo |
| ~~D47~~ | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie la proposta). **Dove sta l'armeria?** Accanto alla fucina di Gunnvor: la stanza del «mucchio buono» e delle armi per le mura. Nel 1372 è l'armeria nanica del banco di ARC-08 B4 |
| ~~D48~~ | F3-bis, D28 | ✅ **Decisa il 2026-10-08** (il DM sceglie le proposte, una per una). **(a)** Il percorso e le misure come nelle griglie; **(b)** le rune di Zeth nel 1372 sono glifi di interdizione dell'SRD legati alla razza: un'esplosione per runa su chi non è nano, 4d8, Riflessi CD 14 dimezza (incantatore di 9°, come una pergamena, Q5), Cercare e Disattivare Congegni CD 28; **(c)** i leoni di pietra sono statue vuote, un'eco dei leoni spettrali del Ghostlord in ARC-09. Era: **Gli stati del 1372 delle sale sotto la montagna vanno bene?** Nessun master li descriveva, e le griglie M7-D, M7-E e M7-F del 1372 li propongono: la ritirata del Giorno 3 dal tunnel della statua alle gallerie di Zeth, poi alla fucina grande e al Cuore; gli orchi che saccheggiano il livello −1 dal corridoio principale; la riconquista al contrario; le rune di Zeth accese (D30) e due leoni di pietra nelle gallerie; le misure delle stanze. Resta da fissare l'effetto meccanico delle rune nel 1372. Proposta: approvare le griglie come sono e decidere le rune quando ARC-08 gioca la ritirata |

<!-- eco: LETTORE-PLAYTESTER 2026-10-07 -->
- **Decise**: D27 (niente da considerare, la domanda si chiude); D39 (b), Balvar a 0 tacche se gli si parla durante lo scontro; D40 (b), il duello ai PX della tabella SRD; D41, strada B (le reliquie del 372 date dal re il Giorno 21); D42, tutti e cinque i punti (profili delle città, casse, loxo, Cintura del monaco, Tempio di Rethmar); D43, in un secondo messaggio: le monete del 372 calcolate in proporzione (zero) e il conio elfico di Rhest (sì, 6.250 mo)
- **Aperte**: nessuna. D43, aperta e chiusa lo stesso giorno: zero monete del 372 in proporzione, 6.250 mo di conio elfico nell'hoard di Regiarix
- **Cambiate**: nessuna rispetto alle proposte
- **Dedotto da me**: che «calcola in proporzione» voglia dire pagare ogni conto con la borsa in proporzione a quello che c'era dentro, banco per banco, e che il risultato zero vada scritto anche se toglie la scena più forte (la scena resta per una moneta trovata dopo); che il prezzo da collezione valga per le prime dieci monete per collezionista, altrimenti 6.250 monete elfiche varrebbero 62.500 mo; che con la B valga anche la parte della proposta sulle gemme a copertura della differenza, fino a 10.000 mo per PG, e la tacca nel legno del conto; che «D42 ok» copra tutti e cinque i punti; che le «monete antiche» siano tutte quelle che il gruppo può avere (Thorek I, le pre-imperiali di `DEF-1`, quelle di Rhest e di Talar, quelle del Collezionista) e non solo quelle del 372

<!-- eco: LETTORE-PLAYTESTER 2026-10-08 -->
- **Decise**: D44 la postierla nel muro sud sotto la torre est · D45 tre fucine su tre livelli · D46 il 372 è il nucleo della fortezza del 1372 · D47 l'armeria accanto alla fucina di Gunnvor · D48 il percorso del 1372 e le misure, le rune di Zeth glifi contro chi non è nano, i leoni vuoti
- **Aperte**: nessuna. D48 è nata e si è chiusa lo stesso giorno
- **Cambiate**: D45 dalla proposta «la fucina di Gunnvor e quella del cortile sono la stessa sala» a «tre fucine»
- **Dedotto da me**: che la fucina originale del cortile sia la «prima forgia» da cui viene l'incudine della cappella e del rito; che la statua di un re nel cortile del 372 (Scena 3) sia la statua del Re Antenato del 1372 (H3-1), col tunnel scavato dopo; che le gallerie di Zeth siano i «passaggi antichi» della ritirata del 1372 verso il Cuore della Montagna; per D48, che la CD delle rune venga dalla regola delle pergamene (Q5, incantatore di 9°) e non da una Saggezza di Zeth nel 372 che nessuna scheda dà

### L'eco del 2026-10-03

<!-- eco: LETTORE-PLAYTESTER 2026-10-03 -->
- **Decise**: D38, la proposta: la Fase 0 dell'ARC-08 dopo il drago ai bastioni, e l'aura dell'Apparizione come presenza terrificante SRD
- **Aperte**: D27, D35, D36, D37, D39, D40 (D39 e D40 decise poi il 2026-10-07, eco qui sopra)
- **Cambiate**: D39. Il 2026-10-03 avevo letto *«a ok, b ok»* come le opzioni (a) e (b) di D39 e portato la notte a 9 tacche; il 2026-10-07 il DM ha deciso **(b) sola**, e nel merge di `main` del 2026-10-10 l'orologio è tornato a 8 tacche, come vuole la decisione più recente
- **Dedotto da me**: D38 è stata applicata su un *«d38»* del DM nello stesso messaggio delle altre approvazioni. Su `main`, nella sessione del 2026-10-07, D38 risultava ancora aperta perché quella sessione non vedeva questo ramo: se la lettura è sbagliata, si riapre. In D38 la proposta diceva *«chi fa 20 è scosso»*; l'SRD della presenza terrificante non prevede uno scosso per chi supera il tiro, e la proposta è scritta com'era

## 5 · Validazione

- `python3 scripts/copertura_scene.py --check` verde in CI.
- `python3 scripts/componenti.py --check` e `python3 scripts/quiz_lettura.py --check`
  verdi in CI (F7, F8).
- `python3 scripts/domande_developer.py --check` verde in CI (F9).
- Ogni residuo ha la ragione, e un residuo che smette di verificarsi fa fallire
  il cancello finché non lo si toglie.
- Un tipo di rilievo che le letture trovano in **due moduli diversi** diventa una
  regola nuova, con i falsi positivi contati a mano prima di entrare.
