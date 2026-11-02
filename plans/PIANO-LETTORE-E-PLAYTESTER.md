# PIANO — Il lettore e il playtester: trovare quello che il DM dovrà inventare

> **Cos'è**: uno strumento in due metà che legge un modulo come lo legge un DM
> che non l'ha scritto, e trova i posti in cui dovrà inventare. La metà
> deterministica (`scripts/copertura_scene.py`) sta in CI; l'altra metà sono
> due letture a freddo fatte da un agente con una rubrica fissa
> (`skills/rumblingstone-playtest/references/`).
>
> **Stato**: ✅ **COMPLETO (2026-10-15)**. F1-F4 e F7-F9 chiusi; F4 chiuso il 2026-10-15 con DEF-1, 2, 3 e 5 senza 🔴 e il quiz di DEF-5; F5 e F6 spostate in PIANO-MASTER-DEF (DM 2026-10-12) · **Decisore**: DM ·
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

### F3-quinquies · DEF-4 da chiudere: le marcature `[INFERRED]` — ✅ (2026-10-12)

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
- [x] il giro delle quattro letture a freddo su DEF-4 (passo 6 del ciclo), con la
      lettura del DM a freddo che rientra nel registro con l'impronta. Superato
      dal giro 3 completo e dal giro 4 di conferma, qui sotto.
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
- [x] **subito**: il giro 3 delle letture su DEF-4, un subagente alla volta
      *(2026-10-12, parziale: developer, DM a freddo e playtester sulle parti
      scritte per la serata dopo il 25 settembre, cioè le tattiche nuove delle
      Scene 6, 8 e 10, il torque della Scena 12 e il corredo
      `sessione-notte-e-alba`. Developer 🔴 5, DM 🔴 4, playtester 🔴 3, quasi
      tutti sul conto delle tacche della regia e sulle versioni veloci:
      corretti. Rapporto in `esperimenti/def4-giro3-serata/`. Manca il lettore,
      e il resto del master non è stato riletto: la casella resta aperta)*
      *(2026-10-12, giro 3 completo, PR #239: le quattro letture su tutto il
      master, una alla volta, in `esperimenti/def4-giro3/`. Lettore 🔴 1 · 🟠 5 ·
      🟡 35; playtester 🔴 0 · 🟠 4 · 🟡 20; developer 🔴 0 · 🟠 7 · 🟡 16; DM a
      freddo, a scene e registrato con l'impronta, 🔴 0 · 🟠 9 · 🟡 24. Corretti
      quelli che il testo risolve (fra gli altri: il volo dei nani in armatura a
      12 m, il *comando superiore* di Balvar col TS a ogni turno, i giavellotti
      di Zog'tar, le statistiche di Durik e dei Treant, la C.2 allineata alla
      Scena 6). L'unico 🔴, le pozioni del re in due versioni, e gli 🟠 di
      canone sono D49-D62. Tre falsi allarmi verificati e scartati: la CA 33 di
      Skullcrusher, il GS 16 del drago Vecchio, la pozione di *neutralizza
      veleno*. Resta aperta: dopo le decisioni serve un giro 4 di conferma, e
      la lettura del DM è già scaduta per le correzioni fatte dopo)*
- [x] il passo 7: il ricordo del giorno dopo, e il quiz con la chiave già
      approvata (D1) *(2026-10-12, dal diario del DM a freddo, in
      `esperimenti/def4-giro3/passo7/`: quiz **10 su 14**, il ricordo ha la
      missione, gli avversari e il fallimento. Un rilievo nuovo: il vincolo del
      drago non resta a chi legge)*
- [x] la risposta al rilievo del passo 7, su richiesta del DM: che cosa muove
      Skullcrusher (il patto col runaio, il guinzaglio scoperto dopo, la paura
      di farsi vedere legato) scritto in Scena 7 e ripreso in Scena 11, più
      mezza frase nel box «La serata in tre frasi». È canone nuovo, quindi
      `[INFERRED]` fino a D63 *(2026-10-12)*
- [x] le decisioni del DM del 12 ottobre, D35-D37 e D49-D63, applicate in
      DEF-1, DEF-2, DEF-3, DEF-4, `ARC08-03` e nella scheda di Zog'tar
      *(2026-10-12. Le parti nuove: le due dotazioni del re, i Treant con gli
      indizi e le quattro destinazioni, Balvar in volo, il drago Vecchio e
      Avanzato, il dado dei caduti. I dettagli lasciati `[INFERRED]` sono
      D64-D68)*
- [x] **il giro 4 di conferma su DEF-4**: lettore e playtester a freddo sul
      master corretto, un subagente alla volta, e la lettura del DM rifatta
      *(2026-10-12: il lettore ha trovato 🔴 0 · 🟠 5 · 🟡 16, tutti corretti
      o portati al DM come D69-D71; triage in `esperimenti/def4-giro4/`.
      Il playtester: 🔴 0 · 🟠 6 · 🟡 17, corretti o portati al DM come D74.
      Il DM a freddo: 🔴 0 · 🟠 8 · 🟡 11, corretti o portati al DM come
      D75-D76; tre 🟡 restano residui con la ragione)*

### F4 · Gli altri master di ARC-07 — ✅ (2026-10-15) · allargato il 2026-09-27 (ADR-0075)

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
      Resta il **passo 7** (il quiz, D10): fatto il 2026-10-15
      (`esperimenti/quiz-def5/`), 10 su 12 dagli appunti, nessun buco a libro
      aperto; le marcature `[INFERRED]` sono D90 (decisa) e D91
- [x] **DEF-1, DEF-2, DEF-3 nella forma, passi 1-4 (2026-09-30).** Scene
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
- [x] **DEF-1 chiuso (2026-10-15).** Sei giri del playtester a freddo in
      `esperimenti/f4-giro2/`: l'ultimo senza 🔴 (🟠 6, 🟡 29). I 🟠 sono
      corretti, con D84-D89; i 🟡 restano nei report. Il DM ha chiesto di
      chiuderlo così, senza un settimo giro.
- [x] **DEF-5 chiuso (2026-10-15).** Il quiz (passo 7), D90-D92 decise e
      applicate, nessuna marcatura `[INFERRED]`; il playtester di conferma
      (giro 3) senza 🔴, tre 🟠 chiusi nel testo e tre con D92.
- [x] **Le decisioni del DM del 2026-09-30, applicate.** D7, D12, D14-D17,
      D19, D21, D23, D25, D29-D33 in DEF-4 e DEF-5 (più il registro dell'orologio
      di DEF-2 e l'handout delle Cronache), D34 in DEF-1 Scena 6. Brynja resta
      di 9° livello; la pietra di *silenzio* è incantata all'8° (8 minuti, 160
      mo: la prima stesura diceva 8 round, ed era sbagliato). D8 (il Riflessi del Drappo) entra con F5. D10 e D26 sono metodo: il
      quiz non si fa sulle conversioni di sola forma, il cancello del registro
      delle letture è L4 di [PIANO-AGENT-SKILLS-ESTERNE](PIANO-AGENT-SKILLS-ESTERNE.md), fatto il 2026-10-01: `plans/letture-a-freddo.json` e `registro_letture.py --check` in CI, in avviso finché un master non ha le letture con impronta, poi bloccante. **D9, passo 5**: il DM ha confermato «spezzali»;
      DEF-1 e DEF-2 hanno zero box oltre 12 righe, nessuna parola cambiata
- [x] **Il giro delle quattro letture su DEF-4 e DEF-5, e la procedura (2026-09-30).**
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
- [x] DEF-1 (Varis), DEF-2, DEF-3: i residui dichiarati, prima che un gruppo
      nuovo li riprenda. Sono **già giocati** (`copertura-scene.json`): si
      convertono nella forma (titoli `### SCENA`, contratto, componenti, box al
      metro) e non in cosa succede, che per questo gruppo è già canone
- [x] per ognuno, alla fine: lettore e playtester a freddo senza 🔴, quiz con la
      chiave approvata dal DM, e la riga tolta da `plans/copertura-scene.json`
      *(2026-10-15: DEF-1 al giro 6 del playtester, DEF-2 e DEF-3 al giro 2
      (`esperimenti/f4-giro2/`), DEF-5 al giro 3 (`esperimenti/def5-giro3/`):
      nessun 🔴. Il quiz solo su DEF-5 (D10: DEF-1, 2, 3 sono conversioni di
      sola forma), 10 su 12 dagli appunti (`esperimenti/quiz-def5/`). In
      `copertura-scene.json` i profili restano, perché sono il contratto che il
      cancello controlla; i cinque residui di DEF-1 e DEF-5 sono voci di
      artefatti e di Moradin che parlano, dichiarate con la ragione)*
- [x] **DEF-5 è la prova cieca di `P-ABITATO`** (ADR-0075, «La prova contro il
      tavolo»), **riuscita** il 2026-09-30: il playtester, senza la tabella, ha
      trovato da solo il buco (#13): dopo la pulizia i PG sono in una fortezza
      abitata, e il modulo dà solo chi comanda e chi cura; mancano rimedi,
      armi, messaggi, guardia, chi compra il bottino e chi identifica. La
      domanda resta com'è. La tabella in DEF-5 però **non** l'ho aggiunta: la
      fortezza del 1372 è quella dell'ARC-08, e cosa c'è a Hammerfist lo decide
      la Fase 0 (D31)

### F5 · Gli stand-alone — ➡️ spostata in PIANO-MASTER-DEF (DM 2026-10-12)

> Le tre voci qui sotto le fanno S3 (il Drappo) e S4 (l'Abbazia) di
> [PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE](PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md),
> che le ha già nel lotto. Restano qui come storia; questo piano si chiude con ARC-07.


- ➡️ Drappo: sette sezioni senza box, fra cui la rivelazione del Drappo di
      Lino Rasca (Giorno 3 §8)
- ➡️ Abbazia: l'Atto II e le stanze in stile *keyed*: decidere col DM se
      ogni stanza vuole un box
- ➡️ il contratto sugli stand-alone, col foglio del cast come fonte delle schede

### F6 · I master nuovi di ARC-08 e ARC-09 — ➡️ spostata in PIANO-MASTER-DEF (DM 2026-10-12)

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
- ➡️ i master nuovi di ARC-08 (F6) nascono con l'apparato generato

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
- [x] F4: la Tempra di DEF-5. Il DM ha scelto la Volontà (D90); il residuo
      «nessun TS su Tempra» è dichiarato con la ragione
- [ ] F5: l'invisibilità al corpo di guardia dell'Abbazia, Riflessi e Volontà
      nell'Abbazia e nel Drappo ➡️ con F5, in PIANO-MASTER-DEF

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
| ~~D35~~ | F4 | ✅ **Decisa il 2026-10-12**: (A) tre tentativi per step, poi lo step passa col suo ❌ come prezzo; senza gradi la caratteristica a −4; a 0 successi allo Step 5 si occupa il Sud e si ritira una volta. Applicata in DEF-3 (Quick-Reference, regia, §9); i dettagli rimasti sono D67. Era: **DEF-3, il rito quando va male** (i due 🔴 del playtester a freddo). **(a)** Gli Step 1-3 falliti dicono solo «riprova» (−2 cumulativo, 2d6 non letali, −10 min), senza tetto né uscita, e Conoscenze e Utilizzare Oggetti Magici senza gradi non si tirano oltre CD 10. Proposta: ogni step si ritenta al massimo tre volte, ognuna costa 10 minuti; al terzo fallimento lo step riesce lo stesso e il suo esito ❌ della regia resta come prezzo. Chi non ha gradi può usare la prova grezza della caratteristica (SAG per l'Invocazione, CAR per la Stabilizzazione) con −4. **(b)** Con 0 successi allo Step 5 il modulo apre «un'indagine di un'ora» ma non dice cosa fanno i PG trovata la risposta. Proposta: la risposta è occupare il Sud vuoto (un PG, o Therysol); fatto questo lo Step 5 si ritira una volta, con 2 successi su 3 |
| ~~D36~~ | F4 | ✅ **Decisa il 2026-10-12**: (a) vale la tabella; (b) solo eventi del d6 più la prova per zona; (c) CD 18 come la via C; (d) lo Smeraldo si incastona comunque; (e) il +1 sacro viene dal **toccare l'incisione**; (f) vale il §5. Applicata in DEF-1, DEF-2, DEF-3; un effetto collaterale di (e) è in D68. Era: **I 🟠 di regole di DEF-1, DEF-2 e DEF-3 che chiedono canone**, raccolti dalle letture a freddo del 2026-09-30 (`esperimenti/f4-def1-def3/`). **(a)** DEF-1: la Benedizione «ignora le penalità» ma la tabella della gravità le applica ridotte (−25%, −5): vale la tabella? **(b)** DEF-1: polvere ogni 10 minuti e stalattiti ogni 15 per tutto il viaggio, o solo come evento del d6? Proposta: solo come evento del d6, più la prova di gruppo per zona. **(c)** DEF-1: la via B contro gli Xorn non ha CD. Proposta: Intimidire o Diplomazia CD 18, come la via C; fallita, gli Xorn non sono accerchiati e si combatte senza il bonus. **(d)** DEF-1: al terzo fallimento di Thorik nel rito lo Smeraldo si incastona comunque? Proposta: sì, e il prezzo sono i malus già scritti. **(e)** DEF-2: il +1 sacro al rito viene dal toccare l'incisione o dal dormire nella Stanza? **(f)** DEF-3: la soglia dei 3 su 3 è «se Thorik rifiuta» nella Quick-Reference e «uno o nessun dono» nel §5: vale il §5? |
| ~~D37~~ | F4 | ✅ **Decisa il 2026-10-12**: (A) la Sentinella è una prova: Tordek a terra, la Magnetite si spegne, si ritenta dopo un riposo (−12 h); Thorik si libera con l'aiuto di Artemis, Artemis parla e lancia senza componenti somatiche. Applicata in DEF-1 Scena 7; i dettagli in D68. Era: **DEF-1 Scena 7: Tordek da solo contro la Sentinella, e se cade?** (🔴 del playtester a freddo). L'anticamera immobilizza Thorik (Forza CD 28, che lui al massimo fa 27) e lascia Artemis prono e indifeso: se Tordek va a 0 pf il modulo non dice cosa succede, e gli altri due passano la scena senza agire. Proposta: la Sentinella è una prova, come Terros è un voto: quando Tordek cade la Magnetite si spegne, la Sentinella torna immobile, e si può ritentare dopo un riposo (−12 h). E per gli altri due un'azione possibile: Thorik può liberarsi con la CD 28 grazie all'aiuto di Artemis (+2), Artemis può parlare, e un suo incantesimo senza componenti somatiche passa |
| ~~D49~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: tutte e due: il re chiede «come pensate di entrare?» e dà la dotazione **dal basso** (4 *invisibilità* al 12°) o **dall'alto** (5 *volare*), oltre alle quattro *cura ferite gravi* dell'antica fucina. Il 25 settembre il tavolo ha avuto la seconda. Applicata in DEF-4 Scene 4, 5, 6, C.1 e §8 B. Era: **Le pozioni del re per i gruppi futuri** (🔴 del lettore, giro 3). La Scena 4 e C.1 danno 4 pozioni d'*invisibilità* CL 12, le Benedizioni e la mappa; il banco e §8 B danno 5 *volare* e 4 *cura ferite gravi*, che è il canone del primo tavolo (2026-10-06). Tutta la Scena 6 è costruita sulla prima versione. Proposta: il master tiene la versione della Scena 4 per i gruppi futuri; §8 B e la riga del banco diventano la variante «al tavolo del 25 settembre», marcata come tale, e il riquadro della Scena 6 lo dice in una riga |
| ~~D50~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) sveglio finché l'ultima tacca segnata è la 4ª. Applicata in DEF-4 Scena 7. Era: **Grask a 4 tacche esatte** (🟠 del lettore). «Sveglio fino alla 4ª tacca, addormentato dalla 5ª»: chi arriva alla tenda con 4 tacche segnate lo trova sveglio o addormentato? Proposta: **sveglio** finché la 4ª tacca è l'ultima segnata; dorme da quando se ne segna la 5ª |
| ~~D51~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) il criterio proposto. Applicata in DEF-4 Scena 8. Era: **Ucciso «in silenzio» o «spettacolare»** (🟠 del lettore). Decide se all'alba i PG perdono la prima azione. Proposta: è **spettacolare** se almeno una guardia o Grask, vivi e coscienti, vedono la morte di Zog'tar **e** il colpo è un incantesimo ad area, una decapitazione o un colpo che il giocatore descrive come esibito (il `[HDYWTDT]`); è **in silenzio** se nessuno esce dalla tenda a gridare e Grask non suona; tutto il resto è «ucciso», senza picchiata e senza il successo in meno |
| ~~D52~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) una riga da leggere: tre rune spezzate, un nome e una freccia; il senso in ARC-09. Applicata in DEF-4 Scena 7, il nome e la direzione sono in D64. Era: **La lastra di Balvar** (🟠 del lettore). Il master lascia al DM cosa c'è inciso («gancio bianco per ARC-09»). Proposta: resta un gancio bianco, ma il master dà una riga da leggere se il tavolo la legge subito (tre rune nane spezzate, un nome e una direzione) e scrive che il senso si decide in ARC-09 |
| ~~D53~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) 900 mo. Applicata in DEF-4 Scena 5. Era: **Il prezzo delle rune d'annullamento di Zeth** (🟡 del playtester, giro 3). Q5 le prezza come una pergamena di *dissolvi magie* all'incantatore di 9°, 675 mo: è il prezzo del 3° livello (chierico, mago). Ma Zeth è un druido, e per il druido *dissolvi magie* è di 4°: 4 × 9 × 25 = **900 mo**. Proposta: 900 mo. Il tavolo, per quanto dice il conto, ne ha comprate solo di *resistere all'energia*, e non cambia niente di giocato |
| ~~D54~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: il tavolo del 25 settembre non ha avuto indizi (il re parlava solo al portatore della Corona). Per i gruppi futuri due indizi (un capitano al tavolo di guerra, i semi che si girano verso est); per questo gruppo i Treant vanno dove li vuole la giocatrice: fuori dalla tenda contro i rinforzi, dentro contro Zog'tar, sul fianco all'alba o nel duello col drago, uno o due, con quello che cambia. Applicata in DEF-4 Scena 5; i numeri nuovi sono in D65. Era: **I Treant di Hella entrano nel duello?** (🟠 del playtester). Durano 1 ora (`DEF-3` A.2) e caricano il fianco dell'orda all'alba; il master non dice se sono ancora lì quando cala il drago. Proposta: no. Restano sul fianco dell'orda, che è il successo in più di Q49; un Treant può essere richiamato nel cortile solo se il duello comincia entro l'ora, e allora la carica sul fianco non c'è |
| ~~D55~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) Balvar esce da solo e arriva al round 1d4+2; scritto anche cosa cambia se i PG lo portano in volo (peso, postierla, notte nelle mura, duello, campo). Applicata in DEF-4 Scena 8; i dettagli in D66. Era: **Balvar recuperato e il ritorno in volo** (🟠 del playtester). Il master porta Balvar al cortile solo a piedi; il gruppo che torna in volo lo lascia al campo. Proposta: Balvar non vola; esce dal campo da solo nella confusione dell'alba, con le sue rune (non ha bisogno di prove: nessuno lo sorveglia, Scena 5), e arriva nel cortile al round **1d4+2** del duello |
| ~~D56~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A). Applicata in DEF-4 Scena 8. Era: **Zog'tar catturato: come si porta via?** (🟠 del playtester). Il successo in più sulle mura c'è, il trasporto no. Proposta: solo legato e privo di sensi; in volo non si porta (Grande, in mithral, oltre il carico di chiunque nel gruppo); a piedi lo portano due PG, il blocco dello skill challenge costa −4, e se si sveglia e grida è l'allarme |
| ~~D57~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) CD 21 e quarta riga del `Boost log:`, nel master e nel Bestiario. Era: **La Presenza Minacciosa di Zog'tar** (🟠 del developer, giro 3). Non è SRD, non è nei tre `Boost log:` e ha CD 22. Proposta: resta, presa sul modello della presenza terrificante dei draghi (10 + ½ DV + mod. CAR = 10 + 7 + 4 = **21**), e entra come quarta riga del `Boost log:` nel master e nel Bestiario |
| ~~D58~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) le Scene 6-8 alla tabella: ≈ 3.650 a testa (≈ 2.700 con Balvar recuperato), pattuglia ≈ 350, lupi ≈ 250, la breccia con le guardie ≈ 2.600; il beat sale a ≈ 7.610. Applicata in DEF-4 §8 A e Scene 8 e 10. Era: **I PX delle Scene 6-8** (🟠 del developer). Il master dà 2.400 a testa; il developer, a tabella DMG, stima ≈ 3.650 a testa per la tenda intera (≈ 2.700 con Balvar recuperato) e trova pattuglia e lupi senza voce. D40 ha già messo il duello alla tabella SRD. Proposta: anche le Scene 6-8 alla tabella, con le voci di pattuglia e lupi; i numeri si rifanno a mano prima di scriverli |
| ~~D59~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A), legato all'allarme: con l'allarme si prende solo quello che si stacca con un'azione (le armature si tolgono in 1d4+1 minuti); senza allarme spogliare la tenda costa una tacca. ≈ 49.750 mo di listino, ≈ 24.500 senza Balvar. Applicata in DEF-4 §8 B e §4. Era: **Il bottino della tenda** (🟠 del developer). §8 B elenca ≈ 10.400 mo più il Sigillo; l'equipaggiamento di Zog'tar, delle guardie e (se muore) di Balvar vale, a stima del developer, ≈ 40.000-45.000 mo, cioè il tesoro di un EL 17, e il master non dice se si può prendere. Proposta: si può, ed entra in §8 B con i valori SRD rifatti a mano; il mithral Grande di Zog'tar si vende, non si indossa |
| ~~D60~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (B) la riga si tiene ma diventa davvero più dura: drago **Vecchio e Avanzato**, GS 17, 337 pf, solo per un gruppo di 14° (EL = APL+3); per uno di 13° restano le wyvern. Applicata in DEF-4 Scena 11 e Appendice A.1-bis. Era: **Il drago Vecchio del «party straripante»** (🟠 del DM a freddo, giro 3). La riga dovrebbe rendere il duello più duro, e invece dà meno pf e CD più basse del drago di base, che ha già il template Avanzato (297 pf, CD 28/25 contro 287 pf, CD 27/24). Il Vecchio dell'SRD è GS 16; col template Avanzato supera il tetto di APL+4. Proposta: la riga si toglie, e il «party straripante» usa il drago di base con le campane già suonate e i rinforzi dell'orda |
| ~~D61~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) funziona. Applicata in DEF-4 Scena 11. Era: ***Dragondoom* di Aegis Fang contro Skullcrusher** (🟠 del DM a freddo). Per la Cintura di Tordek il master dice che rifiuta; per Aegis Fang non dice niente, e il giocatore lo chiederà. Proposta: funziona, come contro ogni drago Grande o più (3 volte al giorno, da `state.md`); la Catena non lo blocca |
| ~~D62~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A), ma solo nel 372: il tiro diventa il **dado dei caduti** (1d4 difensori del 372 per ogni incantesimo comprato) e nel 1372 torna solo come eco. Il Registro di ARC-08 toglie 1d4 PFU ai Veterani solo per gli acquisti del banco del 1372 (`ARC08-17`). Applicata in DEF-4 Scene 5, 10 e §7, e in `ARC08-03`. Era: **Cosa vuol dire «un tiro sul *Registro delle Perdite*»** (🟠 di lettore e DM a freddo). Q11 lo vuole, DEF-4 e `ARC08-17` lo citano, ma `ARC08-03-REGISTRO-PERDITE.md` è un foglio di caselle per unità e **non ha una tabella su cui tirare**: il tiro non esiste in nessun file. Proposta: ogni tiro è 1d4 caselle PFU tolte, prima della battaglia di ARC-08, a un'unità di Guerrieri Nanici Veterani (il DM sceglie quale); la regola si scrive nel Registro e DEF-4 la cita |
| ~~D63~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A) confermato. Tolti gli `[INFERRED]` in DEF-4. Era: **Che cosa muove Skullcrusher** (risposta al passo 7, scritta su richiesta del DM, `[INFERRED]` in DEF-4 Scena 7 e 11). Il drago non ha mai perso; ha accettato il patto di Balvar per il tesoro del re, e ha scoperto dopo che la runa è un guinzaglio. Teme che l'orda lo veda legato: chi dice la Catena ad alta voce se lo tira addosso, chi gli offre di spezzarla davanti all'orda viene rifiutato e diventa il bersaglio. Proposta: confermare, e togliere i tre `[INFERRED]` |
| ~~D64~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (a), (b), (d), (e) come proposte; (c) **no**: chi porta armature fuori dalla tenda ha la penalità, oltre al carico SRD; il buco portatile la evita per quello che ci entra, e il master ne dà la capienza. Applicata in DEF-4 Scene 7, 8, 5, §7, §8 B e A.1-bis; i numeri della penalità e dei volumi sono D72. Era: **DEF-4, i dettagli lasciati `[INFERRED]` dalle decisioni del 12 ottobre.** (a) Sulla lastra di Balvar il nome è **Hald**, il nipote, e la freccia punta a **nord** (D52). (b) La polvere di diamante di Balvar vale **400 mo**, i glifi di una sera (D59). (c) Chi torna carico di armature: nessuna penalità oltre il carico dell'SRD (D59). (d) Nel 1372 i nomi del dado dei caduti si leggono fra i caduti dell'assedio antico, ma il master non dice dove (D62). (e) I due incantesimi di 3° del drago Vecchio: *dissolvi magie* e *lentezza* (D60). Proposta: sì ad (a), (b), (c), (e); per (d) i nomi entrano nel pannello in più della Sala degli affreschi, lo stesso di Balvar (Scena 7) |
| ~~D65~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (a) e (b) sì; (c) valgono **tutte e due**: la regola del mese e la carica per Durik parlano di cose diverse, ma attingono alle stesse tre cariche; la scheda della Collana lo conferma, con l'unica eccezione dei due Treant all'alba della notte a −1000. Applicata in DEF-4 Scena 5. Era: **I Treant, i numeri nuovi** (D54). (a) Con un Treant fuori dalla tenda le ronde arrivano in 2d4+2 round e gli squadroni in 3d4+2; con due non entra nessuno. (b) Un seme speso di notte torna all'alba, come dice `DEF-3` §7. (c) **C'è una contraddizione che c'era già**: `DEF-3` §7 dice che chiamare i due Treant insieme spegne l'Evocazione per un mese e che Durik distrutto torna solo all'alba; `DEF-4` Scena 5 dice che i due Treant dell'alba costano «due delle tre cariche» e che ne resta una per Durik. Proposta: sì ad (a) e (b); per (c) vale `DEF-3`, perché la Collana è sua, e `DEF-4` si allinea |
| ~~D66~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: sì così. Applicata in DEF-4 Scena 8. Era: **Balvar portato in volo** (D55). Il peso (circa 85 kg, carico medio per chi ha FOR 18), la postierla (Durin lo fa entrare se un PG garantisce, Diplomazia CD 20), la notte in catene nel cortile per ordine del re, e Hald che lo vede dal camminamento. Proposta: sì così |
| ~~D67~~ | F4 | ✅ **Decisa il 2026-10-12**: (a), (b), (c) sì (Therysol al rito c'è: non viene a −1000, resta nella Forgia a chiedere alla sua divinità un modo per uscire). Applicata in DEF-3 regia e §9. (d) **riformulata come D73**: il DM ha letto «il Custode» come Thorik; è la Custode delle Radici della Scena 5 di DEF-3. Era: **DEF-3, i dettagli di D35.** (a) La riga ❌ dello Step 5 nella regia dice ancora «si può ritentare, ma ogni tentativo la porta più lontano»: si allinea al §9 (un ritiro solo, a 0 successi, dopo aver occupato il Sud). (b) Se il Sud lo occupa Therysol, il ritiro lo fanno i tre PG agli altri punti. (c) Se il ritiro dà di nuovo 0, il rito riesce col prezzo del suo ❌, come i tre tentativi degli Step 1-3. (d) Il Custode compare in questo ramo? Proposta: sì ad (a), (b), (c); (d) la decide il DM |
| ~~D68~~ | F4 | ✅ **Decisa il 2026-10-12**: (a) sì; (b) adiacente come l'SRD, salvo un potere degli artefatti, che nelle schede non c'è; (c) sì. Applicata in DEF-1 §7b e Quick-Reference, DEF-2 §6 (tolto anche un «riposo lungo», termine 5e). Era: **DEF-1 e DEF-2, i dettagli di D36 e D37.** (a) La Forza CD 28 di Thorik nell'anticamera adesso lo **libera del tutto**, non più un braccio per un round? (b) L'aiuto di Artemis (+2): basta la voce, o deve essere adiacente? (c) Con il +1 sacro che viene dall'incisione (D36 e), la tabella del sonno di DEF-2 §6 dà alla Stanza solo «la scena giusta», e il testo la chiama ancora «un vero scambio». Proposta: (a) sì, del tutto; (b) adiacente, come l'aiuto dell'SRD; (c) si toglie «un vero scambio» |
| ~~D69~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: sì. Applicata in DEF-4 Scena 8 e §7. Era: **Zog'tar catturato, il dopo** (🟠 del lettore, giro 4). Il master lo portava fino alla porta e si fermava. Scritto `[INFERRED]` in DEF-4 Scena 8: (a) il re lo fa incatenare nella cella sotto la torre nord e lo fa giustiziare all'alba del giorno dopo, se il duello va bene, quando i PG sono già nel 1372; (b) nel 1372 è solo un nome nelle cronache dell'assedio antico (riga nuova in §7); (c) quando si sveglia: la regola SRD (10% l'ora se stabilizzato, 15 pf non letali l'ora), e imbavagliato il blocco in cui si sveglia si tira a −8. Proposta: sì ad (a), (b), (c) |
| ~~D70~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (B) restano, come eccezione dichiarata: le ultime della cappella. Applicata in DEF-4 Scena 5. Era: **Le cinque pozioni di *neutralizza veleno*** (🟡 del lettore, giro 4). Sono nel conto della serata del 25 settembre, ma *neutralizza veleno* è di 4° e l'SRD non fa pozioni oltre il 3°, come dice lo stesso master. Proposta: **(A)** diventano pozioni di *ritarda veleno* (2°, 300 mo l'una) e la differenza, 2.250 mo, torna al gruppo; **(B)** restano, come eccezione dichiarata del forziere del re; **(C)** diventano 5 pergamene di *neutralizza veleno*, stesso prezzo |
| ~~D71~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (a)-(d), (f)-(h) sì. (e) cambiata: il drago colpisce solo chi ha un nome, lo dice forte prima di colpire, e se non lo sa lo chiede; a parità di richiami decide l'arroganza, e sceglie la caduta che fa più orrore agli altri PG. Applicata in DEF-4 Scene 4, 6, 7, 8, 11 e A.1-bis. Era: **DEF-4, i dettagli `[INFERRED]` del giro 4.** (a) La dotazione dimezzata è 2 pozioni d'*invisibilità* o 2 di *volare*. (b) Le pozioni del re sono un dono e non toccano i 10.000 mo del forziere. (c) Balvar da solo all'alba entra dalla postierla, che Durin tiene aperta per gli esploratori; con i PG, a piedi o in volo, vale la garanzia (Diplomazia CD 20) e le catene. (d) Balvar tira Nascondersi e Muoversi Silenziosamente a −1. (e) Il drago sceglie, nell'ordine: chi ha detto la Catena, chi tiene la corda dell'ala, chi lo ha ferito di più. (f) Il drago Vecchio ha i talenti di A.1 più Allerta, e fugge a circa 112 pf. (g) Delle dodici ore della notte, le prime quattro se ne vanno prima del consiglio. (h) Finire la lastra costa a Balvar l'ultima azione di round pieno. Proposta: sì a tutto |
| ~~D72~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (a), (b), (d) sì; per (c) si calcola l'ingombro e il DM chiede l'elenco al giocatore; se sfora va detto ai PG. Il buco è lo stesso in 3.5 e in PF1e. Applicata in DEF-4 §8 B e DEF-3 §9; il foglio di calcolo è in `/mnt/project-files/lettore-playtester/INGOMBRO-BUCO-PORTATILE.md`. Era: **I numeri dietro D64 (c).** (a) La penalità del ferro che sbatte: **−2** a Muoversi Silenziosamente e Nascondersi per ogni armatura portata e non indossata, sul ritorno. (b) Il buco portatile: 1,8 m per 3 m (SRD), circa 7,5 m³; a occhio una completa Media 0,15 m³, una Grande 0,5, uno scudo o un'arma a due mani 0,05; la tenda intera circa 1,5 m³. (c) Il contenuto del buco di Artemis non è scritto da nessuna parte: per sapere se la tenda ci entra serve l'elenco, o almeno quante armature e armi ci sono già. (d) Il prezzo di un secondo 0 allo Step 5 di DEF-3 (D67 c) è quello della riga «1 su 3» del §9: un livello negativo e i nomi dimenticati per 1d4 minuti. Proposta: sì ad (a), (b), (d); per (c) l'elenco lo dà il DM o il giocatore di Artemis |
| ~~D73~~ | F4 | ✅ **Decisa il 2026-10-12**: (A): entra lo stesso, una volta sola, dopo il ritiro riuscito. Applicata in DEF-3 §9. Era: **DEF-3: la Custode delle Radici compare anche nel rito che va male?** Non è Thorik: è la psicopompa della Scena 5 di DEF-3, quella che al tavolo del 25 settembre ha chiesto chi paga il debito, e Thorik ha detto «io». Entra dal Sud al momento del richiamo. La domanda è cosa fa se il richiamo dà 0 e qualcuno deve occupare il Sud. Proposta: **(A)** entra lo stesso, una volta sola, dopo il ritiro riuscito, come nel rito che va bene; **(B)** è lei che si mette al Sud se nessuno lo occupa entro l'ora, e il debito si fa più pesante; **(C)** in questo ramo non compare |
| ~~D74~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: sì a tutto, (a), (c), (d), (o) prima e le altre dodici poi. Applicata in DEF-4. Era: **DEF-4, i dettagli `[INFERRED]` dal playtester del giro 4.** (a) Il Treant di Adamantio ha FOR 28 (dai suoi schianti, +9) e TS Temp +11, Rifl +2, Vol +7. (b) Un Treant alla tenda non costa tacche; uno che compare nella tenda rende la morte di Zog'tar spettacolare. (c) Il campo non ha alberi vivi per *trasporto vegetale* entro 500 m dalla tenda. (d) Una bolla di *silenzio* su Grask prende anche la tenda: è un allarme senza corno, con il successo in meno e senza drago. (e) La ronda che arriva dopo la pattuglia o i lupi grida: campo pre-allertato e CD +2, salvo abbatterla in 2 round. (f) Il blocco fallito col fiuto dei lupi costa una tacca sola. (g) Durik richiamato alla tenda resta con Hella. (h) All'atterraggio si tira solo se Grask è sveglio. (i) Chi torna in volo subito dopo il corno è dentro le mura prima del drago (42 round contro 70). (j) Zog'tar pesa circa 300 kg; una bestia Grande di Hella lo porta da sola. (k) Balvar al ritorno conta per la metà del gruppo. (l) Tenere la breccia: Forza CD 18 o un attacco contro CA 28. (m) Le wyvern vanno su chi tiene la corda e su chi vola, e fuggono col drago. (n) Alla corda al massimo tre aiutanti, nani compresi. (o) Il bottino della tenda stanotte non lo compra nessuno: si vende nel 1372; l'armatura di Zog'tar Re Thorek la riprende in cambio della sua parola. (p) Una tacca non è un'ora. Proposta: sì a tutto |
| ~~D75~~ | F3-quinquies | ✅ **Decisa il 2026-10-12**: (A), la tacca si paga anche per questo gruppo. Già scritto così in DEF-4 Scena 5 e in §0. Era: **La veglia dei semi per il gruppo del 25 settembre** (🟠 del DM a freddo, giro 4). Il master dice che vegliare i semi costa una tacca, e anche che per questo gruppo i Treant stanno dove la giocatrice li vuole (D54): non dice se la tacca si paga. Con 3 tacche e il volo Grask è sveglio all'atterraggio; con la veglia il volo diventa la 5ª e Grask dorme. Proposta: **(A)** la tacca si paga anche per questo gruppo, prima di partire, come scritto nella Scena 5; (B) i Treant arrivano senza tacca, perché la veglia è già stata decisa al tavolo |
| ~~D76~~ | F3-quinquies | ✅ **Decisa il 2026-10-12** (il DM: le decisioni sono sul ramo del gruppo, ma chi prende cosa non è ancora assegnato perché non è ancora giocato). Dal log del ramo: (c) la n. 4 l'ha fermata Kettra, nessuno l'ha bevuta; (b) le richieste rimaste aperte non sono ancora scelte; (a) il Nome serviva solo al consiglio, giocato con fiducia piena. In DEF-4 §0: chi porta cosa si chiede al tavolo prima della Scena 6. (d) la correzione del log è un diff pronto per il DM, da applicare sul ramo. Era: **Tre fatti del gruppo e il log del 25 settembre** (🟠 del DM a freddo, giro 4). Il log non dice: (a) se hanno preso il Nome della targa; (b) se hanno comprato la pietra del silenzio; (c) chi ha bevuto la pozione n. 4 dalla cera nera. E (d) il log manda il dado dei caduti al Registro delle Perdite di ARC-08, mentre il master dice che non lo tocca. Le risposte (a)-(c) le sa solo il DM; per (d) la proposta è correggere il log sul ramo del gruppo con un diff che il DM conferma (ADR-0007) |
| ~~D77~~ | F4 | ✅ **Decisa il 2026-10-12**: sì a tutti. In DEF-5 i marcatori diventano `[CANONE — DM 2026-10-12, D77]`. Era: **DEF-5, i dettagli `[INFERRED]` del giro 2.** Già scritti nel master, marcati, da confermare o cambiare uno per uno. (a) Dei 20 hobgoblin i nani ne tengono 15 e 5 passano l'anello; i nani finiscono i loro entro il round 4, i cinque si arrendono quando ne restano due. (b) Gli hobgoblin puntano il re, è l'ordine che hanno; contro chi vola usano l'arco. (c) Re Thorek resta a 8 pf ed esausto: parla e comanda, non combatte; *ristorare* lo toglie, e Dana lo tiene giù. (d) Le due *guarigioni* di Dana di stamattina sono spese sulle mura. (e) Il varco ha i cardini strappati: si chiude solo con la magia. (f) Fermarsi a curarsi costa una torre della Porta Ovest ogni 10 minuti. (g) Dana e le Cantitrici danno una *cura ferite gravi* a testa, nel minuto del portale. (h) Il primo ordine di Thorik ai novanta, dall'altare. (i) Il ramo «meno luminoso»: aura a CD 20, cinque orchi scossi più il capo, gli hobgoblin entrano subito. (j) Il portale di Dana: un arco di luce, un round. (k) Gli orchi scossi si stringono al capo e si arrendono se cade. (l) Il gesto di Artemis: alla porta solo con 36 m in un movimento. (m) La colonna d'orchi scende dalle gallerie di Zeth. (n) Le radici di Hella e il re: copertura per un round. (o) Il torque: il re lo vede prima del viso. Proposta: **sì a tutti** |
| ~~D78~~ | F4 | ✅ **Decisa il 2026-10-12**: (A), la scheda corretta al conto SRD, e DEF-5 la segue. Era: **Lo statblocco dell'hobgoblin sergente nel Bestiario** (🟡 del developer, giro 2 di DEF-5). La scheda è marcata accettata dal DM il 2026-05-05, ma col conto SRD non torna: le classi sostituiscono il DV razziale, quindi guerriero 5 e basta. Ne viene CA 21 (la completa dà +8), attacco +9/+4, danno 1d8+4 (Specializzazione), 5d10+10 pf. Scritto ora: CA 20, +10/+5, 1d8+3, 46 pf. DEF-5 copia il Bestiario, e gli stessi sergenti tornano nell'ARC-08. Proposta: **(A)** si corregge la scheda al conto SRD, e DEF-5 la segue; **(B)** resta com'è, come scelta del DM, e si scrive perché |
| ~~D79~~ | F4 | ✅ **Decisa il 2026-10-12**: (a)-(g) come proposte; (h) resta com'era, con Volare CD 20 (il DM, dopo un primo «correggi»: «lascia h, Volare CD 20 andava benissimo»). Applicata in DEF-1 §0-bis, §3, §5, §6, §7a, §7b, §8. Era: **DEF-1, otto buchi di regola dal lettore di conferma** (un 🔴, sette 🟠). Il modulo è già giocato: valgono per i gruppi futuri, e nessuna proposta cambia cosa è successo al tavolo. (a) 🔴 **L'Onda Gravitazionale nella sfera a gravità zero**: «tutti cadono 9 m», ma dall'Altare la parete è a ~25 m, e il box mette Tordek «sul muro». Proposta: chi trova una superficie entro 9 m la colpisce (Riflessi CD 22 o 4d6 e prono); chi non la trova resta sospeso a 9 m e rientra come chiunque nello zero-G (spinta o Volare); Tordek, con l'Ancoraggio dei Bracieri, resta sull'Altare, e nel box i piedi trovano l'Altare, non il muro. (b) **La Forza CD 28 di Thorik con la Sentinella è irraggiungibile**: FOR 20 dà +5, con l'aiuto di Artemis fa al massimo 27. L'errore era nella mia proposta di D37. Proposta: **CD 25**. (c) **Le due piattaforme laterali con le scale** non stanno in una sfera a gravità zero, e la mappa T-6 non le ha. Proposta: si tolgono, e Artemis tira in volo. (d) **L'abisso di lava fredda** che il pilastro degli Xorn fa da ponte non c'è nella zona né sulla mappa. Proposta: si toglie il ponte, e il pilastro che cade travolge e basta. (e) **Il «Successo Critico» dei Cristalli**, che dà il Diapason, non è definito. Proposta: 6 successi senza nessun fallimento. (f) **Il Diapason nella salita al Tempio**: è monouso, ed è stato speso sulla Sentinella. Proposta: suonarlo per la scala non lo consuma, perché il suo uso unico è lo stordimento; servono 4 prove riuscite, e una fallita fa ricadere l'ultimo blocco. (g) **I danni sonici di Tordek contro Terros**: il Frantumare dei Bracieri scatta dopo un critico confermato, e Terros è immune ai critici, quindi non scatta mai. Proposta: quando il gruppo canta la Frequenza, i colpi dei Bracieri sono sonici per quel round, come la modalità sonica di Artemis. (h) **Il volo di Artemis** dipende da Volare CD 20, un'abilità di PF1e. Proposta: il modificatore di Volare lo chiedi al giocatore; vale anche nello zero-G |
| ~~D80~~ | F4 | ✅ **Decisa il 2026-10-12**: sì a tutte e due. Applicata in DEF-2 A3 e §7. Era: **DEF-2, due punti dal lettore di conferma** (🟠; nessun 🔴). (a) **Quale visione mostra l'affresco A3.** Il box dice che Thorik, toccata la Corona, si è trovato su un campo di battaglia accanto agli eroi del passato, con Thorgrim. La guida della Corona e DEF-1 §1 dicono che la visione del risveglio era il futuro: Fauci di Palude e le Cantitrici, in forma spirituale. Proposta: l'affresco dipinge solo il passato, cioè il tocco, il lampo e Thorgrim che gli passa l'ascia; la visione di Fauci resta di Thorik, e la Sala non la mostra. Una riga per il DM sotto il box, che non cambia. (b) **Le Benedizioni chiedono Conoscenze (religioni) CD 12 e dicono «Moradin risponde sempre»**, senza dire cosa succede se la prova fallisce; senza gradi la CD 12 non si può nemmeno tentare (SRD). Proposta: la prova non c'è, la preghiera di 10 minuti basta |
| ~~D81~~ | F4 | ✅ **Decisa il 2026-10-12**: sì a tutte. Applicata in DEF-3 §0, §6, §9, §8-ter e Appendice A.1. Era: **DEF-3, cinque punti dal lettore di conferma** (🟠; nessun 🔴). (a) **La soglia dello Step 5 con uno o nessun Dono** è 3 su 3 (D36), ma la tabella dei fallimenti conta i successi grezzi: con un Dono e 2 successi non si sa quale riga vale. Proposta: si conta quanto manca alla soglia; con 2 successi su una soglia di 3 vale la riga «1 su 3» (Hella torna con un livello negativo), con 1 la riga «0 su 3». (b) **L'ora del Cuore**: se scade, Therysol parla, ma non è detto se il rito è perso. Proposta: no, il Cuore regge finché il tavolo lavora sul Sud; l'ora segna solo quando parla Therysol. (c) **Quanto dura il rito, e se c'è un riposo prima della soglia** (il testo dice «riposato» e anche «respira da tre ore»). Proposta: il rito dura circa un'ora; nessun riposo prima della soglia; l'orologio di Hammerfist scende di un'ora. (d) **Cosa compra la risposta C (offrire Durik)**, visto che il terzo seme rigermoglia già di base. Proposta: compra che il Debito è saldato subito, senza quest in ARC-09; Durik risponde al Sogno una volta per sessione. (e) **Lo statblocco di Hella in Appendice A.1** non torna con l'SRD: ha uno slot di 7° livello (una druida di 12° arriva al 6°), *cura ferite gravi* e *pietre aguzze* stanno al 4°, *cura ferite critiche* al 5°, *cura ferite moderate di massa* al 7°, e il BAB di ranger 1 e druida 12 è +10, non +9. È la scheda di una PG: la proposta è correggerla all'SRD, e farla vedere alla giocatrice |
| ~~D82~~ | F4 | ✅ **Decisa il 2026-10-15**: sì a tutte. Applicate in DEF-2 (A7, il riquadro PF1e sui bonus sacri, il sogno nella Stanza della Corona). La (a) vale per i gruppi futuri: il gruppo di oggi tiene il premio di A7 che ha avuto al tavolo, e se l'ha avuto lo dice `campaign-artifacts.md` (+3d6, ×4). Era: **DEF-2, tre punti dal playtester di conferma** (🟠; nessun 🔴). (a) **Il Bane draconico di A7 contro la scheda di Aegis Fang.** A7 dà «+3d6 (invece di +2d6 vs draghi), critico ×4, +2 competenza»; la scheda dell'ascia dice *Dragondoom* (MIC) e 20/×3, senza +2d6 contro i draghi, e «competenza» non è un tipo di bonus 3.5. Proposta: A7 dà, solo contro Fauci di Palude, +1d6 ai danni oltre il *Dragondoom* e lo *Scosso* 1/incontro come scritto; niente critico ×4 né «competenza». (b) **Thorik ha già +2 sacro a tutti i TS** dalla Risonanza della Corona con Aegis Fang: con la regola «vale il più alto», i premi di A1, A3 e A8 per lui valgono zero. Proposta: per Thorik quei premi diventano bonus **morale** dello stesso valore, che si sommano al sacro. (c) **Se il gruppo dorme nella Stanza della Corona** il sogno non c'è, e la giocatrice di Hella, morta, passa il beat senza niente. Proposta: il sogno di Hella resta anche lì, perché è lei a sognare, non la Sala |
| ~~D83~~ | F4 | ✅ **Decisa il 2026-10-12**: sì a tutte. Applicata in DEF-3 §0 e §9. Era: **DEF-3, cinque punti dal playtester di conferma** (🟠; nessun 🔴). Il primo nasce dalla mia applicazione di D81 (a). (a) **L'inversione dello Step 5.** Senza Doni la soglia è 3: chi fa 1 successo va all'indagine del Sud e col ritiro può riavere Hella intera, chi fa 2 prende subito il livello negativo. Proposta: il ritiro riuscito paga sempre il prezzo della riga «1 su 3», così l'indagine salva Hella ma non la fa tornare meglio di chi ha tirato 2. (b) **Sotto soglia, la Custode e lo Step 6.** La Custode entra «se il richiamo riesce»: con le righe «2 su 3» e «1 su 3» Hella torna, ma il testo non dice se si gioca il §6 e lo Step 6. Proposta: se Hella torna, in qualunque riga, si giocano la Custode e lo Step 6; col richiamo a zero, dopo il ritiro (come D73). (c) **Il Sud occupato prima del primo Step 5** (basta chiedere a Therysol). Proposta: conta come la risposta trovata in anticipo; se lo Step 5 va a zero, il ritiro parte subito, senza l'ora d'indagine. (d) **Il livello negativo della riga «1 su 3»**: né natura né durata. Proposta: un livello negativo dell'SRD che non diventa perdita di livello e si toglie con *ristorare*; il gruppo ne ha le pergamene. Il riquadro PF1e citava regole sbagliate, e l'ho già corretto. (e) **L'orologio**: D81 fa scendere l'orologio di un'ora, ma i tentativi da 10 minuti e l'ora d'indagine non sono contati. Proposta: un'ora per il rito, più un'ora se c'è l'indagine del Sud |
| ~~D84~~ | F4 | ✅ **Decisa il 2026-10-12**: sì a tutte. Applicata in DEF-1 (quick-reference, §7a, §8, §9, §11-bis). Era: **DEF-1, sei punti dal playtester di conferma** (un 🔴, quattro 🟠, due 🟡 di canone). Il 🔴 nasce da D79 (a). (a) 🔴 **Come rientra chi resta sospeso dopo l'Onda**, senza una superficie a portata (l'Onda verso il soffitto è la tattica del round 1). Proposta: l'Onda dura un round; finita, la gravità dell'Altare riprende chi è entro 9 m, che ricade sull'Altare alla fine del suo turno successivo e perde l'azione di movimento (Riflessi CD 15 o prono, senza danni); chi è più lontano deriva di 3 m a round nella direzione dell'Onda finché non tocca la parete, e da lì si spinge. (b) **Cantare la Frequenza durante lo scontro**: chi canta, con che azione, per quanto. Proposta: un PG, azione standard, Intrattenere (Canto) CD 18 (+4 con l'Anello); vale fino all'inizio del suo turno successivo. All'apertura le tre prove le tirano i tre PG, una a testa. (c) **Se l'Ancora di Thorik fallisce** (FOR CD 20) o la Scalare sulla corda, «perdersi nel piano» non ha esito. Proposta: chi cade finisce nell'oceano di roccia (affonda in 3 round, Nuotare CD 20, §4), e Artemis può ripescarlo col cavo. (d) **La DES di Thorik al rituale** può arrivare a 0 (esausto più i fallimenti di Artemis), che nell'SRD vuol dire paralizzato. Proposta: durante il rito non scende sotto 1, perché il Peso del Mondo lo tiene in piedi. (e) **I PX** non tornano con la tabella della DMG che il modulo cita (Terros, GS 15, per tre PG di 13°: circa 2.600 a testa, non 5.400). Proposta: per il gruppo di oggi i PX restano quelli dati; per i gruppi futuri si ricalcolano al conto SRD, come D40 per DEF-4. (f) **Il prezzo del rito di Thorik**: `state.md` gli dà anche +4 CAR dal rito dello Smeraldo, il modulo solo −2 DES e +2 COS. Proposta: il modulo si allinea a `state.md` |
| ~~D85~~ | F4 | ✅ **Decisa il 2026-10-12**: sì a tutte. Applicata in DEF-1 (§7a, §7b, §8). Era: **DEF-1, sei punti dal playtester del giro 3** (un 🔴, cinque 🟠). Valgono per i gruppi futuri: il gruppo di oggi ha già giocato la Sentinella. (a) 🔴 **La Sentinella non si batte coi numeri del modulo**: la Raffica di Tordek (+12) contro CA 30 colpisce col 18, la crepa chiede di superare la CA di 5 (35), e la sconfitta rigioca lo stesso duello. Proposta: ogni colpo dei Bracieri che va a segno è una crepa (la Risonanza), e al secondo tentativo la Sentinella riparte dai pf a cui era rimasta. (b) **La Spinta fuori dal bordo**: vale la regola dell'Onda (D84 a); si tolgono i «2d6 contro il muro» dalla regia dell'apertura. (c) **La caduta attorno al Tempio**, dove la gravità è zero: niente danno, si deriva lentamente verso l'oceano; Artemis ripesca con un'azione di round intero, FOR CD 15, prima dei 3 round dell'affondamento; anche Tordek è legato al cavo. (d) **La Sentinella ferma dopo che Tordek è caduto**: chi la tocca la risveglia e la Magnetite si riaccende; la porta verso Terros resta chiusa finché non la batte Tordek. (e) **Terros addormentato alla soglia**: si sveglia appena qualcuno mette piede sull'Altare; chi agisce prima ha un round di sorpresa, senza l'indifeso. (f) **La tabella DPR**: Thorik allo stadio 0 di Aegis Fang (1d10, niente sacro, ~3 a colpo dopo la RD) e la rigenerazione sottratta, quindi Terros dura circa 10 round invece di 5. Proposta: si corregge la stima e non si toccano le statistiche |
| ~~D86~~ | F4 | ✅ **Decisa il 2026-10-14**: «Sentinella + tutto». La Sentinella è applicata in DEF-1 §7b e nella quick-reference; gli undici 🟠 sono D87. Era: **DEF-1, come si chiude** (giro 4 del playtester: un 🔴, undici 🟠, tutti per i gruppi futuri). (a) 🔴 **La Sentinella resta imbattibile** dopo D85 (a): con +12 contro CA 30 Tordek mette a segno 0,4 colpi a round e cade in 3-4 round. Proposta: i colpi dei Bracieri sono attacchi di contatto (la Risonanza, CA di contatto 11), al massimo una crepa a round, e **3 crepe sono la vittoria** (il petto si apre e si estrae il Geode, come dice già la MAPPA T-5); l'Overdrive parte alla prima crepa. (b) **Gli undici 🟠**: proposta, restano residui dichiarati per i gruppi futuri, e si fa un ultimo giro solo sul 🔴. In alternativa li correggo tutti con un'altra scheda e un altro giro intero |
| ~~D87~~ | F4 | ✅ **Decisa il 2026-10-14**: «Sì a tutte», l'Overdrive resta alla prima crepa. Applicate in DEF-1 (§4 salita, §6 Cristalli, §7b, soglia e distacco, Onda, 8c-4, *Scalare lo scontro*, MAPPA T-5); il giro 5 del playtester le misura. Era: **DEF-1, i dieci 🟠 del giro 4** (il #2, le crepe con tre significati, è già chiuso da D86). Tutti per i gruppi futuri. (3) **Il ritentativo contro la Sentinella**: Tordek ritenta coi pf del riposo più le cariche di Vigore della Forgia, che nel Piano tornano a ogni riposo; le Benedizioni durano finché il gruppo resta nel Piano. (4) **I riposi**: ogni riposo, anche quello dopo la Sentinella, costa −12 h; il ramo «hanno dormito» di Terros scatta una volta sola; caduto Tordek, la porta dell'anticamera si riapre. (5) **Artemis nel duello**: è prona, non indifesa; sulla MAPPA T-5 sta accanto a Thorik; con un'azione standard Aiuta Thorik (+2 alla FOR) o incoraggia Tordek (+2 al prossimo attacco). (6) **Thorik libero**: può solo Aiutare Tordek (+2 alla CA o all'attacco); se attacca la Sentinella, lei lo ignora. (7) **L'affondamento**: dopo i 3 round l'oceano risputa il sommerso sulla riva in 1d4 round, a 0 pf e stabile, e costa −12 h; Thorik sale per ultimo, e gli fa da Ancora Tordek dal Tempio. (8) **La soglia**: i tre box si leggono dalla soglia («davanti agli stivali»); chi attacca o mette piede per primo ha il round di sorpresa; l'Altare si stacca all'inizio del round 1. (9) **L'Ancoraggio contro l'Onda** non consuma un uso: si paga solo contro la Spinta. (10) **La durata contro Terros**: 8c-4 diventa «~12 round invece di ~10»; un PG a −1 o meno sull'Altare è espulso subito sulla riva, stabile. (11) **Il round 1**: Thorik resta sull'Altare con Riflessi CD 22 conficcando Aegis Fang, il box resta; Terros non è spostato dalla propria Onda. (12) **I Cristalli**: ogni abilità vale una volta per PG a giro, e ognuno tira almeno una volta per giro |
| ~~D88~~ | F4 | ✅ **Decisa il 2026-10-15**: «Sì, tranne alcune». Applicate in DEF-1 la (1), (2), (3), (4), (6) e (7). La (8) cambiata dal DM: lo stadio Terra dei Bracieri si sveglia col rito dopo la Sentinella, prima di Terros, quindi la scheda completa si stampa; a un gruppo futuro si copre solo *Diventare una Collina*, che si sblocca abbattendo Terros. Della (2) ho scritto la regia senza i numeri di Tordek, che il playtester ha stimato e io non ho verificato. Era: **DEF-1, il giro 5 del playtester** (un 🔴, sette 🟠, tutti per i gruppi futuri; il #5, la T-5 dell'Atlante, l'ho allineata io al modulo). (1) 🔴 **Tordek che muore nel duello**: proposta, a −1 pf o meno la Magnetite si spegne e Tordek resta stabile, come l'espulsione davanti a Terros. (2) **Il primo tentativo quasi perso** (12-25% col gioco diretto, 70-85% entrando curati e in difesa con Maestria): proposta, una riga di regia coi numeri di Tordek e il consiglio di entrare curati; l'Overdrive resta alla prima crepa. (3) **Le tattiche della Sentinella**: proposta, Attrazione Fatale strappa l'arma o lo scudo più vicino, mai l'Anello; se Tordek si allontana lo insegue; ignora Thorik e Artemis. (4) **Le invocazioni di Artemis**: proposta, dentro la Magnetite passano solo le invocazioni su sé stessa o sui compagni; *Chilling Tentacles* e *Flee the Scene* non funzionano lì, perché la gravità 10× schiaccia anche loro. (6) **Il pilastro sugli Xorn**: proposta, chi è nella pietra prende metà danni ed esce stordito 1 round, e lo scontro si fa comunque. (7) **Il +4 dell'Anello al canto**: proposta, vale per tutti quelli che cantano con Artemis. (8) **La scheda dei Bracieri da stampare**: proposta, si stampa solo lo stadio Fuoco, e *Diventare una Collina* si sblocca dopo Terros |
| ~~D89~~ | F4 | ✅ **Decisa il 2026-10-15**: «applica tutte le soluzioni consigliate e chiudi». Applicate in DEF-1 la (2), la (8) e la (18). Della (18) ho cambiato una parte per coerenza col canone giocato: il Diapason contro la Sentinella non è «senza effetto», fa il *grido superiore* che ha fatto al tavolo il 2026-07-24, ma non la stordisce. DEF-1 è chiuso. Era: **DEF-1, il giro 6 del playtester** (nessun 🔴, sei 🟠, tutti per i gruppi futuri). Tre li ho chiusi io senza decisione: la T-3 e la T-6 dell'Atlante allineate al modulo, e il *Manto di Pietra e Spirito* aggiunto al §9 e alla carta della Corona, perché è già canone in `state.md`. Restano tre. (2) **L'affaticamento del viaggio si somma fino a esausto**: proposta, ognuno tira per sé; chi fallisce è affaticato fino al prossimo scontro, non si somma, e una carica di *Vigore della Forgia* lo toglie. (8) **I nani ai Cristalli non hanno una prova che possano vincere**: proposta, chi non ha un'abilità utile può Aiutare un compagno (+2) o passare il giro senza fallimento, più una prova per i nani: Conoscenze (architettura e ingegneria) o Cercare sulla pietra, CD 18, +1. (18) **Lo stordimento di Terros**: proposta, nello statblock «immune allo stordimento, tranne il Diapason»; *Move Earth* lo blocca 1 round senza stordirlo; il Diapason non ha effetto sulla Sentinella, che è un costrutto |
| ~~D90~~ | F4 | ✅ **Decisa il 2026-10-15**: «solo la 1 da cambiare, TS sulla Volontà; le restanti vanno bene, adottale». Applicata in DEF-5: all'arrivo **Volontà CD 15** o frastornati 1 round; le altre sette sono canone, e la chiave del quiz accetta la q4 (10 su 12 dagli appunti). Era: **DEF-5, le marcature `[INFERRED]` prima di giocarlo** (il quiz è fatto, 0 buchi). Sei regole scritte da me, da confermare o cambiare: (1) **la Tempra all'arrivo**: Tempra CD 15 o frastornati 1 round (era Volontà); (2) **l'aura sugli orchi**: chi fa 20 resta scosso, e l'effetto dura tutta la scena, chi fugge non torna; (3) **l'ordine**: l'aura scatta con l'apparizione e i TS si risolvono subito, poi il round di sorpresa dei PG, poi l'iniziativa; (4) **i novanta nani** non si tirano: tre blocchi, e un blocco travolge ciò che ha davanti; (5) **il ramo «meno luminoso»** scatta se il duello di DEF-4 è finito FUGGITO o VINTO SPORCO, e la Catena spezzata non conta; (6) **il 14° livello** si prende al primo riposo, dopo la battaglia di Hammerfist. Più due cose del quiz: (7) la riga D77 del §6 letta come «si rialza quando non è più esausto, anche a 8 pf»; (8) la chiave del quiz che accetta anche «Volontà… fuggono» per la q4 |
| ~~D91~~ | F4 | ✅ **Decisa il 2026-10-15**: sì a tutte. Applicata in DEF-5: nessuna marcatura `[INFERRED]` resta nel modulo. Era: **DEF-5, le sei marcature `[INFERRED]` che la scheda di D90 non elencava** (le avevo saltate io). (1) **l'Aura della Forgia**: l'alba è quella del 1372, il salto non ne consuma la durata; (2) **«Fuggi!» sul capo degli orchi**: se il capo è uno dei rimasti lo manda via, e l'altro scosso scappa con lui; (3) **il capo degli orchi**: orco dell'SRD con un elmo nanico, 8 pf invece di 5; (4) **Artemis sopra la porta**: se ci arriva nel round di sorpresa vede gli hobgoblin un round prima, e i nani avvisati vincono il primo scambio del muro di scudi; (5) **le Cantitrici della Pietra**: se Dana cade apre il portale una di loro, chierica di 5°, più lenta e con la voce che trema; (6) **la porta murata**: con *muro di pietra* regge, e chi insegue trova il corridoio vuoto fino alla prima svolta |
| ~~D92~~ | F4 | ✅ **Decisa il 2026-10-15**: sì a tutte. Applicate in DEF-5 Scena 2, Scena 3 e §6. F4 è chiuso. Era: **DEF-5, giro 3 del playtester** (nessun 🔴, sei 🟠). Tre li ho chiusi io nel testo: la durata dello scontro (4-5 round), il tempo di lancio di *ristorare* e chi lo legge, la Cintura di Tordek (il suo scontro è Fauci). Restano tre. (a) **l'ordine di Thorik e il preavviso di Artemis sul muro di scudi**: proposta, con l'ordine nel round di sorpresa passano tre hobgoblin invece di cinque; con anche il preavviso di Artemis, due; (b) **Dana e le Cantitrici, cosa hanno ancora**: proposta, hanno speso tutto sulle mura tranne il *muro di pietra* di Dana, che lancia se un PG le chiede di chiudere il varco; niente *ristorare*; (c) **gli hobgoblin all'altare, e se il re muore**: proposta, l'altare si scala con Scalare CD 15 (un round); il re non muore in DEF-5: il colpo che lo porterebbe sotto 0 lo prende Dana, che gli si getta sopra |
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

<!-- eco: LETTORE-PLAYTESTER 2026-10-15 -->
- **Decise**: D88 sì tranne la (8), cambiata dal DM (DEF-1) · D89 tutte, e DEF-1 chiuso (DEF-1) · D82 sì a tutte (DEF-2) · la chiave del quiz di DEF-5 approvata · D90 sì tranne la (1), cambiata dal DM (DEF-5) · D91 sì a tutte (DEF-5) · D92 sì a tutte, e DEF-5 e F4 chiusi (DEF-5)
- **Aperte**: nessuna
- **Cambiate**: D88 (8) da «si stampa solo lo stadio Fuoco» a «la scheda completa si stampa, si copre solo *Diventare una Collina*»: lo stadio Terra si sveglia col rito dopo la Sentinella. D90 (1) da «Tempra CD 15» a «Volontà CD 15» all'arrivo. D89 (18) da «il Diapason non ha effetto sulla Sentinella» a «fa il *grido superiore*, non la stordisce», per il canone giocato il 2026-07-24
- **Dedotto da me**: per D82, che la (a) valga solo per i gruppi futuri, perché il gruppo di oggi ha già giocato DEF-2; per D88 e D89, la regia del duello senza i numeri di Tordek, che il playtester ha stimato su una scheda al 12°; la prova dei nani ai Cristalli vale +1, come le altre prove da CD 18

<!-- eco: LETTORE-PLAYTESTER 2026-10-14 -->
- **Decise**: D86 «Sentinella + tutto» (DEF-1) · D87 sì a tutte (DEF-1)
- **Aperte**: nessuna dopo il 2026-10-15
- **Cambiate**: D87 dalla mia raccomandazione («Sì, e Overdrive dopo», l'Overdrive alla seconda crepa) a «Sì a tutte»: l'Overdrive resta alla prima crepa, e il giro 5 del playtester dirà se il duello regge
- **Dedotto da me (D87)**: i 13 pf del riposo (uno per livello, SRD, senza guaritore); la riga prima del box del primo scambio (se Thorik fallisce i Riflessi CD 22, la frase di Aegis Fang si salta); «a giri» per i Cristalli; Utilizzare Oggetti Magici solo con i gradi, come nell'SRD; l'aiuto di Artemis a Thorik scritto come +2 alla prova di FOR, quello di prima

<!-- eco: LETTORE-PLAYTESTER 2026-10-12 -->
- **Decise**: D35 A · D36 a-d e f come proposte, (e) il +1 sacro dal toccare l'incisione · D37 A · D49 tutte e due le versioni · D50, D51, D52, D53 A · D54 indizi per i gruppi futuri e destinazioni a scelta per questo gruppo · D55 A, più il caso del volo · D56, D57, D58, D59 A, D59 legata all'allarme e al drago · D60 B · D61 A · D62 A, solo nel 372 · D63 A · F5 e F6 spostate in MASTER-DEF · seconda risposta: D64 a, b, d, e, e (c) con la penalità · D65 a, b, c (valgono tutte e due) · D66 sì · D67 a, b, c · D68 a, b (adiacente), c · terza risposta: D69 sì · D70 B · D71 sì, con (e) cambiata: il nome detto prima di colpire, e a parità la caduta che fa più orrore · quarta risposta: D72 a, b, d, e (c) col calcolo dell'ingombro · D73 A · quinta risposta: D74 a, c, d, o, poi sì a tutte le altre · D75 A · D76 come dal log del ramo · D81 sì a tutte (DEF-3) · D77 sì a tutti (DEF-5) · D78 A (la scheda dell'hobgoblin sergente) · D80 sì a tutte e due (DEF-2) · D79 (a)-(g); (h) resta com'era (DEF-1) · D83 sì a tutte (DEF-3) · D84 sì a tutte (DEF-1) · D85 sì a tutte (DEF-1)
- **Aperte**: nessuna. D75 (A) e D76 decise lo stesso giorno: la veglia costa la tacca; i fatti del gruppo non sono ancora giocati, e il master lo dice. Aperte dopo: nessuna; le decisioni del 2026-10-14 e del 2026-10-15 sono nei blocchi sopra
- **Cambiate**: D49 dalla proposta «la Scena 4 per i gruppi futuri» a «due dotazioni, sceglie il tavolo»; D54 da «no» a «dove li vuole la giocatrice»; D60 da «si toglie» a «si rifà più dura»; D62 da «1d4 PFU nel Registro di ARC-08» a «dado dei caduti nel 372, solo eco nel 1372» · D79 (h) da «il modificatore lo chiedi al giocatore» a «volo del 3.5», e poi di nuovo a «resta com'era, Volare CD 20»
- **Dedotto da me (D79)**: niente: il volo del 3.5 che avevo scritto per la (h) è tolto, e il testo è tornato quello di prima
- **Dedotto da me (D78)**: la proposta diceva «+9/+4», ed era sbagliata: con BAB +5 il secondo attacco non c'è, quindi +9 e basta. *Leadership* chiede il 6° livello: l'ho sostituita con *Riflessi in Combattimento*, che non cambia nessun numero, e il +1 morale l'ho tenuto come comando del sergente. Pf 37, la media di 5d10+10; Tempra +6, Volontà +1
- **Dedotto da me (D77)**: quali marcatori erano di D77 l'ho deciso io, riga per riga contro main; due `[INFERRED]` nuovi del giro restano tali perché D77 non li nominava (il panico per tutta la scena, il capo degli orchi a 8 pf)
- **Dedotto da me (D81)**: gli slot e i livelli della scheda di Hella presi dalle tabelle del druido dell'SRD (6/5+2/5+1/4+1/4+1/3+1/2, con i bonus di SAG 20), la Lotta +11 da FOR 12; l'orologio alla soglia scritto 3g 15h; il box «respira da tre ore» lasciato com'è, perché le tre ore contano dal risveglio e non dal registro
- **Dedotto da me (seconda risposta)**: −2 per armatura portata e i volumi del buco (D72); il prezzo di un secondo 0 allo Step 5 dalla riga «1 su 3» (D72 d). ⚠️ Anche qui ho applicato prima di mandare l'eco
- **Dedotto da me**: che «entrambe le opzioni» di D49 si faccia con una domanda del re al consiglio, invece di due master; che i Treant tengano i rinforzi con la loro RD, e i tempi 2d4+2 / 3d4+2; che il drago Vecchio vada bene perché la riga è per un gruppo di 14° (EL = APL+3), mentre per uno di 13° supera il tetto; che la regola di D62 (1d4 PFU ai Veterani) resti valida in `ARC08-03` per gli acquisti del banco del 1372, che sono perdite vere di quella battaglia; i numeri del bottino di D59 dai prezzi SRD (taglia Grande al doppio, mithral pesante +9.000). ⚠️ L'eco andava mandata al DM prima di toccare i file: l'ho scritta dopo averle applicate

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
