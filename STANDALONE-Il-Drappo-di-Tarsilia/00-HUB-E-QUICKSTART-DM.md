# Il Drappo di Tarsilia — hub e quickstart del DM

> **Modulo autonomo.** Non serve conoscere la campagna RumblingStone, non serve
> Faerûn, non serve nessun altro file del repo. Si apre qui, si stampa quello che
> dice il §2, si gioca.

| | |
|---|---|
| **Sistema** | **Pathfinder 1e** (non remastered), **solo Core Rulebook** |
| **Ambientazione** | **Tarsilia**, città-stato originale del **Regno dei Fiumi**, sul Sellen — Golarion |
| **Giocatori** | **6**, con **schede pregenerate** (il modulo regge anche a 4–5: vedi §8) |
| **Livello** | **3°**, avanzamento a pietre miliari (4° a fine Giorno 2) |
| **Durata** | **3 sessioni da 3–4 ore**, una per giornata di corsa |
| **Tono** | intrigo cittadino, comico-amaro, adulto. Si muore poco e si perde la faccia molto |
| **Scala mappe** | 1,5 m per quadretto |

## Indice del modulo

| File | Cosa contiene |
|---|---|
| **questo** | premessa, quickstart, cosa stampare, le tre sessioni a colpo d'occhio, tagli, avanzamento |
| `CONTRADE-DI-TARSILIA.md` | le otto contrade: livree, motti, canti con effetti, rivalità, stemmi |
| `REGOLE-DELLA-CORSA-PF1E.md` | il sottosistema: Morale del Rione, Onore del Fantino, lo Stacco, la Corsa |
| `PREGEN-SEI-SCHEDE-PF1E.md` | le sei schede complete, pronte da stampare |
| `01-GIORNO-1-LA-SORTE.md` | Sessione 1 |
| `02-GIORNO-2-I-PARTITI-E-LA-CENA.md` | Sessione 2 |
| `03-GIORNO-3-LO-STACCO-E-LA-CORSA.md` | Sessione 3 |
| `04-LUOGHI-E-INTRIGO.md` | quindici luoghi pronti: osterie, botteghe, il mercato delle informazioni, le dicerie |
| `05-INIZIAZIONE-E-EVENTI-PG.md` | il rito d'apertura + **diciotto eventi personali**, tre per PG |
| `06-VILLAIN-E-AGENDE.md` | le agende dei villain **ora per ora**, il giro del mondo, gli **incontri scalabili** 4/5/6/7 |
| `07-GUIDA-DM-PASSO-PASSO.md` | **la regia**: le tre serate minuto per minuto, i rilanci, le voci dei PNG |
| `FASCICOLO-SCHEDE-GIOCATORE.md` | i sei background da dare in mano + la matrice dei legami |
| `09-KIT-ANTI-IMPROVVISAZIONE.md` | **quando escono dal copione**: 1d20 nomi, prezzi di bottega, tre PNG jolly con statblocco, 1d6 «la città respira» |
| `08-CASSETTA-DEL-DM.md` | **l'apparato d'uso**: foglio del cast, pronuncia, indice dei read-aloud, inserto per lo schermo, i suoni, il momento da fotografare, accessibilità |
| `STATO-DEL-MODULO.md` | la memoria fra le tre serate: contatori, patti, scelte, **Echo Ledger**. Da copiare per gruppo |
| `PLAYTEST-ALFA.md` | audit meccanico, dry-run delle tre serate, le nove correzioni applicate |
| `PLAYTEST-SCHEDA-FEEDBACK.md` | scheda giocatore, debrief del DM, come si passa da alfa a beta |
| `STATBLOCCHI-PF1E.md` | PNG, rivali, sicari, cavalli |
| `ALLEGATI/mappe/` | la Ruota, **la Ruota in versione giocatore** e le stalle: JSON, master emoji-grid, SVG |
| `ALLEGATI/tavole/` | **tavole vettoriali**: mappa della città, il Drappo, sei ritratti (rigenerabili) |
| `ALLEGATI/handout/` | **i quattro prop da stampare**: il contratto di Vesca, la pagina del registro, la ricevuta, il decreto |
| `homebrew/` | **quattro booklet** impaginati (DM · Giocatori · Fascicolo schede · Prop) + i PDF |
| `ALLEGATI/mappe/uvtt/` | le due mappe pronte per **Foundry / Roll20** |
| `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md` | art direction e prompt per l'edizione raster |
| `PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md` | **cosa manca per l'edizione illustrata** e il prompt pronto da passare a una sessione nuova |
| `IP-E-LICENZE.md` | Community Use Policy Paizo, OGL, provenienza |

---

## §1 · Quickstart — la sessione zero in una pagina

**Dove siamo.** Tarsilia sta dove il Sellen si allarga e rallenta, tre giorni di
barca a monte di Cassomir. Non ha re. Ha otto contrade, un consiglio che si riunisce
quando conviene, e una corsa di cavalli che si tiene l'ultima settimana d'estate da
prima che qualcuno tenesse i conti.

**Cosa si corre.** Il **Drappo**: un telo dipinto ogni anno da un pittore diverso.
Chi vince se lo porta nell'oratorio della contrada e tiene per un anno il **seggio
girevole** in consiglio — l'unico voto che cambia mano.

**Chi sono i PG.** La dirigenza dell'**Istrice**, la contrada povera: boscaioli,
raccoglitori di resina, l'ospizio dei profughi di guerra. Non vincono da
quarant'anni. Sei uffici, sei giocatori:

| Ufficio | Cosa fa | Scheda |
|---|---|---|
| **Capitano** | comanda nei tre giorni, stringe i patti | Vanna Corsari, guerriera 3 |
| **Fantino** | corre. A pelo, senza sella | Nocca Pettirosso, ranger 3 |
| **Stalliere** | custodisce il cavallo. Veleni, ferri, filtri | Ombra dei Salici, druida 3 |
| **Tenente** | spia, corrompe, fa sparire i problemi | Tesio Marca, mago 3 |
| **Alfiere** | bandiere, tamburi, canti: il morale del rione | Berenice Sallo, barda 3 |
| **Vicario** | l'ospizio, i feriti, la parola data | Fra' Melchio Vanzi, chierico 3 |

**Cosa c'è in ballo, davvero.** Sei giorni fa la Sovrintendente ha letto un decreto:
le contrade che non si piazzano nei primi tre in cinque anni perdono il seggio e
**vengono accorpate** alla contrada confinante. L'Istrice è al quinto anno.
Confina con il **Bruco**, che lo vuole: sotto il bosco di spini c'è la
resina, e la resina la comprano i tintori.

**Come finisce.** Con una corsa di novanta secondi e una scelta che si fa mentre la
corsa è in atto. Chi vince il Drappo lo decidono i giocatori; chi resta in piedi
dopo, anche.

> ⚠️ **Non è un modulo che si vince ammazzando.** Ci sono tre combattimenti in tre
> sere, tutti brevi, tutti evitabili o riducibili. Il resto è gente che parla e
> mente.

---

## §2 · Cosa stampare (prima della sessione 1)

**Per i giocatori** — sei fascicoli:

1. la propria scheda da `PREGEN-SEI-SCHEDE-PF1E.md` (una pagina a testa);
2. il **volantino delle otto contrade** — la tabella §1 di `CONTRADE-DI-TARSILIA.md`,
   con gli stemmi;
3. il **retro della scheda** da `FASCICOLO-SCHEDE-GIOCATORE.md`, con il ritratto da
   `ALLEGATI/tavole/ritratto-<nome>.svg`;
4. la **matrice dei legami** (prima tabella del fascicolo), una copia a testa;
5. la **mappa della Ruota** (`ALLEGATI/mappe/rendered/`) e la **mappa della città**
   (`ALLEGATI/tavole/tarsilia-citta.svg`): una copia ciascuna, al centro del tavolo.

**I quattro prop** (`ALLEGATI/handout/`) si stampano e si consegnano **quando la
fiction li consegna**, mai prima: il decreto al Giorno 1, il contratto quando Vesca lo
posa, il registro a Melchio alla prima serata, la ricevuta se perquisiscono Sfregio.
Una volta dati, **non si ritirano**.

**Per il DM:**

- **`07-GUIDA-DM-PASSO-PASSO.md`** e **`08-CASSETTA-DEL-DM.md`** — sono i due file
  che tieni aperti tutta la sera;
- **`STATO-DEL-MODULO.md`**, copiato e stampato: si compila a matita a fine serata;
- questo file e il file della giornata che si gioca;
- `06-VILLAIN-E-AGENDE.md` §1 (l'agenda di Vesca) e `05-INIZIAZIONE` §5 (la griglia
  degli eventi personali, da spuntare);
- `REGOLE-DELLA-CORSA-PF1E.md` §2 e §4 (una pagina in tutto: i due contatori e la
  Corsa);
- il segnapunti dei contatori — due righe su un foglio, si aggiornano a vista.

**Sul tavolo, se ci sono:** otto segnalini colorati per le contrade (i colori delle
livree stanno in `CONTRADE-DI-TARSILIA.md` §1) e un mazzo di carte da usare come
ordine di corsa.

---

## §3 · Tarsilia in dieci righe

**Siamo nel 4712 AR**, ultima settimana d'estate. Le due date che compaiono nel
modulo — il 4692 e il 4705 — stanno vent'anni e sette anni indietro.

Città di legno e mattone crudo su palafitte di ontano, quattromila anime, cinque
ponti di cui due che dondolano. Vive di tre cose: il pedaggio sul fiume, la resina
dell'Istrice e i tintori del Bruco, che comprano la resina e la
rivendono lavorata a valle. Non ha mura verso il fiume e ne ha di ottime verso terra,
il che dice quello che c'è da sapere su chi la assale di solito.

Il consiglio ha otto seggi fissi e uno girevole. La **Sovrintendente al Drappo**,
Vidalia Roncetti, è l'unico ufficio che nessuna contrada può occupare: si sceglie fra
i forestieri residenti da almeno dieci anni, e serve a decidere ciò che le contrade
non riuscirebbero mai a decidere fra loro. Roncetti è al terzo mandato ed è onesta
nel modo peggiore possibile — non si lascia comprare e non si lascia nemmeno
convincere.

La **Ruota** è la piazza: un anello di terra battuta largo quanto una strada
maestra, intorno al vecchio mercato coperto del grano. Ci si corre tre giri. Le
curve sono due, una a nord davanti al Ponte Storto e una a sud sotto le finestre
dell'Oca, e sono lì che si cade.

---

## §4 · Le tre sessioni a colpo d'occhio

```
 GIORNO 1 ─────────── GIORNO 2 ──────────────── GIORNO 3
 La Sorte              I Partiti e la Cena       Lo Stacco e la Corsa
   │                     │                          │
 il cavallo che        i patti col nemico,        tre giri, novanta
 ti tocca, e se        il duello dei canti,       secondi, e una scelta
 provi a cambiarlo     le stalle di notte         che non si può rimandare
```

### Le pietre miliari — accadono comunque, all'ora scritta

| Quando | Cosa accade | Dove agiscono i PG |
|---|---|---|
| G1, mattina | La Sovrintendente legge i cavalli e le contrade | truccare la Sorte (o no) |
| G1, sera | La Bruco manda la prima offerta | comprare, rifiutare, mentire |
| G2, pomeriggio | I Capitani si chiudono nel mercato del grano: i **Partiti** | contrattare o restare soli |
| G2, sera | La **Cena della vigilia**, tutta la contrada nei vicoli | il duello dei canti |
| G2, notte | Qualcuno entra nelle stalle | difendere cavallo e fantino |
| G3, alba | Benedizione del cavallo all'oratorio | l'ultimo morale |
| G3, mezzogiorno | Lo **Stacco** alle funi | finte, scudisciate, iniziativa |
| G3, pomeriggio | La **Corsa** | tre giri — e ciò che succede alla curva nord |
| G3, sera | Il decreto della Sovrintendente | l'esito, e il prezzo |

---

## §5 · Le linee di taglio (perché tre ore passano prima di quanto credi)

Ogni sessione ha un punto oltre il quale si taglia e si chiude. Non è un ripiego:
è la differenza fra finire la serata su un colpo e finirla su un dado a caso.

| Sessione | Se mancano 40 minuti… | Se mancano 15 minuti… |
|---|---|---|
| **G1** | salta le altre offerte degli emissari: arrivano tutte insieme, i PG ne ascoltano due | vai dritto alla Sorte, e chiudi sull'annuncio del cavallo |
| **G2** | il duello dei canti si risolve con **una** prova contrapposta invece di tre | l'assalto alle stalle diventa la scena d'apertura della sessione 3 |
| **G3** | taglia il corteo e la sbandierata: si arriva allo Stacco con il Morale com'è | la Corsa non si taglia mai. Semmai si taglia l'epilogo e lo si manda scritto |

---

## §6 · Contratto del tavolo

Prima di distribuire le schede, due minuti in piedi:

- **Cosa c'è dentro**: corruzione, animali in pericolo (i cavalli), veleno, una
  folla che può fare male, debiti e ricatti familiari. Un ferimento grave di un
  personaggio non giocante che i PG conoscono.
- **Cosa non c'è**: violenza sessuale, tortura in scena, bambini in pericolo.
- **Strumento**: chiunque, in qualunque momento, può battere due dita sul tavolo. Si
  taglia e si riprende dieci secondi prima, senza spiegazioni e senza discussione.
- **Il cavallo può morire.** Ditelo prima. Al tavolo pesa più di quanto sembri.

---

## §7 · Avanzamento, tesoro, ricchezza

**Avanzamento: pietre miliari.** I PG salgono al **4° livello** alla fine del Giorno
2, dopo le stalle, che vincano o perdano. Con la traccia media di PF1e servirebbero
circa 24.000 px complessivi per sei personaggi: un modulo d'intrigo non li produce e
non deve provarci.

> Se il tavolo vuole comunque i px: sono segnati sezione per sezione nei tre file
> giornata, incluse le prove non combattive e i premi narrativi.

**Ricchezza.** Le sei schede partono a 3.000 mo di equipaggiamento (ricchezza da 3°
livello PF1e) — **quel tetto vale per il tesoro che il modulo distribuisce, non per
l'equipaggiamento iniziale**, che segue la tabella standard. Il modulo distribuisce **circa 1.900 mo** in tre giorni, quasi tutta
in oggetti consumabili e in denaro della contrada, che è denaro *vincolato*: serve a
comprare fieno, silenzio e ferri. Nessun oggetto magico permanente sopra le 500 mo.
È voluto — è un modulo in cui il problema non si risolve comprando.

---

## §8 · Se i giocatori non sono sei

| Giocatori | Cosa fare |
|---|---|
| **5** | togli il **Tenente** (Tesio). Diventa un PNG che esegue quello che i PG gli ordinano, e che di suo non decide mai niente |
| **4** | togli anche il **Vicario** (Melchio). Il chierico dell'ospizio resta fuori scena, e le cure si comprano: metti 4 pozioni di *cura ferite leggere* nella cassa della contrada |
| **7** | il settimo prende l'ufficio di **Duce** (capo del corteo): usa la scheda del Capitano, cambia la spada in un'alabarda da parata e scambia Intimidire con Intrattenere |

Con quattro o cinque giocatori, riduci di un grado ogni scontro (§ nei file
giornata: c'è la riga «a cinque / a quattro» in ogni incontro).

---

## §9 · Dopo il Drappo

Il modulo si chiude e sta in piedi da solo. Se il tavolo ne vuole ancora, i tre
semi già piantati sono questi — e sono semi, non capitoli scritti:

1. **La resina.** Chiunque abbia vinto, a valle qualcuno ha già firmato contratti
   sulla resina dell'Istrice per l'anno prossimo. Firmati a Cassomir, non a
   Tarsilia.
2. **Chi ha dipinto il Drappo.** Il pittore di quest'anno ha lasciato la città la
   notte prima della corsa e non ha ritirato il compenso.
3. **Il quinto ponte.** Quello che dondola di più. Il consiglio ha stanziato i soldi
   per rifarlo tre volte in dieci anni.

---

## §10 · Provenienza

Il sottosistema della corsa (contatori di morale, patti, Stacco, inseguimento a tre
giri) è materiale originale dell'autore, sviluppato per l'arco *Il Palio di
Channathgate* della campagna RumblingStone e qui **riscritto per PF1e e per una città
che non sta nei Forgotten Realms**. Nomi, contrade, motti, PNG e trama di questo
modulo sono nuovi. Il dettaglio legale sta in `IP-E-LICENZE.md`.
