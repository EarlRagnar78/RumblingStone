# ADR-0126 — Una scheda si verifica senza omissioni, senza tolleranza e col motore di gioco dichiarato

**Stato**: proposta (2026-11-12); D-B, D-B-bis, D-B-ter e D-C scelte dal DM il 2026-11-12
**Data**: 2026-11-12
**Decisione-fonte**: il DM (Jfs), 2026-11-12: completare le regole di SRD d20, D&D 3.5 e PF1e «senza omettere nulla», stringere la tolleranza sui bonus («un +4 è un bonus davvero importante»), aggiungere la variante della campagna (il risultato più forte fra SRD → 3.5 → PF1e) con una logica deterministica, poter vincolare il motore di gioco, accettare le forme ibride solo nella variante.
**Rapporti**: prosegue [ADR-0124](ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md) (verifica via MCP); applica [ADR-0118](ADR-0118-un-numero-entra-solo-se-la-regola-lo-calcola.md) (il numero più forte vale solo se si ricostruisce) e [ADR-0121](ADR-0121-un-plugin-di-regole-si-misura-contro-la-fonte.md) (un plugin si misura contro la fonte). È un ADR di programma: una sezione per lotto, aggiunta quando il lotto arriva.

## Contesto

Dopo la PR #378 `verifica_scheda` giudica talenti, numeri, gradi e
incantesimi, ma con tre limiti misurati:

- una tolleranza larga sui numeri: un tiro salvezza passava fino a +4 sopra
  l'atteso e un attacco fra −1 e +2. Sul banco degli errori messi apposta un
  tiro salvezza gonfiato di +2 si vedeva 1 volta su 362;
- campi della scheda che nessuna regola guarda (CA nel 3.5, danno, abilità
  totali, RI, RD, sensi, velocità, equipaggiamento, GS, conto dei talenti);
- la cascata delle fonti cablata nel codice: una scheda 3.5 accetta un talento
  PF1e senza che nessuno l'abbia chiesto.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Tolleranza zero, bonus dichiarati e sommati per tipo** (scelta) | ogni punto ha una sorgente scritta; la regola del cumulo è quella dell'SRD; sul banco gli errori visti passano dal 55% al 79% | 22 numeri di 20 schede vere diventano violazioni e vanno chiusi uno per uno |
| Stringere la fascia (per esempio +1) | meno violazioni da decidere | resta una soglia arbitraria; un +1 non dichiarato è comunque un bonus che nessuno ha scelto |
| Tenere la fascia e marcare «sospetto» | nessuna scheda cambia stato | è la situazione di prima con un'etichetta: non verifica niente |
| Il più forte regola per regola | massimizza ogni numero | mescola pezzi di sistemi diversi senza controllo; il DM ha scelto «per elemento intero» |

## Decisione

**D-A. Nessuna tolleranza sui numeri.** Tiri salvezza e attacco devono essere
uguali al conto. Ogni punto sopra la base viene da una sorgente che la scheda
dichiara. `--tolleranza` (e `severo=False` nelle funzioni) rimette la fascia
di prima, per confronto. I pf restano nella fascia dei dadi, che è una regola
e non una tolleranza.

**D-B. La variante della campagna sceglie per elemento intero** (card del DM,
2026-11-12). Classe, talento, incantesimo, oggetto, capacità: si prende la
versione più forte fra SRD → 3.5 → PF1e dell'elemento intero, mai un numero
dell'una dentro il testo dell'altra.

**D-B-bis. Il motore di gioco si dichiara e si può vincolare.** Un solo
parametro `motore` per il costruttore e per il verificatore, con quattro
valori: `srd35` (solo SRD), `dnd35` (SRD e manuali 3.5), `pf1e`,
`rumblingstone` (la variante D-B). Con un motore vincolato un elemento di un
altro sistema è una violazione `motore.fuori`. Il valore predefinito resta il
sistema dichiarato dal file.

**D-B-ter. Le forme ibride sono lecite solo nella variante, e solo se
registrate.** Una scheda che mescola regole di sistemi diversi passa col
motore `rumblingstone` se l'ibrida è nel registro delle regole custom del DM
(elemento, sistema d'origine, sistema della scheda, fonte, data). Il
verificatore controlla che l'elemento sia legale nel suo sistema e coerente
col resto della scheda. Non registrata è `ibrida.non_dichiarata`.

**D-C. Ogni campo scritto ha un esito** (card del DM: «tutto ciò che una
scheda può scrivere»). Per ogni campo del recinto e della prosa meccanica
l'uscita dice verificato, violazione o non verificabile col motivo.
Descrizione e tattiche restano al verificatore della storia (ADR-0125), che
riceve da qui talenti, incantesimi e capacità per controllarne la coerenza.

**D-D. Due fonti per ogni dato fuori SRD.** Dove due fonti divergono la voce
resta non verificabile finché un libro non la decide. Dalle fonti non OGL
entrano solo nomi e numeri.

## Lotti

### Lotto 1 — cumulo dei bonus per tipo (2026-11-12)

- `sistemi/d20/dati/bonus.toml`, capacità `bonus.cumulo` della famiglia d20:
  i tipi di bonus, quali si sommano (schivare, circostanza, razziale, senza
  tipo: SRD 3.5, «Bonus Types»), le parole che fanno di un bonus un bonus a
  condizione, e 16 sorgenti con la loro fonte (mantello e veste della
  resistenza, veste dell'arcimago, pietra della buona fortuna, veste delle
  stelle, prisma verde pallido, i sei talenti dei tiri salvezza, Fortuna degli
  Eroi, Anima Forte, il bonus razziale dell'halfling).
- `dmcore.bonus`: `somma` (per tipo), `dichiarati` (sorgenti note più le
  dichiarazioni esplicite nella riga dei tiri salvezza, «+1 fortuna a tutti»),
  `totali`. `lettura_creatura.talenti` lo usa: il lettore resta uno.
- `conformita_statblocchi.verifica(severo=True)` e `verifica_scheda` senza
  tolleranza; i tiri salvezza condivisi col padrone (cavalcatura, famiglio) non
  si giudicano verso l'alto.
- Ogni violazione di tiro salvezza o attacco elenca i bonus contati.

Misura (banco `muta_numeri.py`, stessi errori messi apposta):

| | Prima (#378) | Lotto 1 |
|---|---|---|
| Errori visti | 701 su 1.279 (55%) | 1.007 su 1.279 (79%) |
| Tiri salvezza gonfiati di +2 visti | 1 su 362 | 286 su 362 |
| Violazioni di numero sulle schede vere | 0 (nascoste dalla fascia) | 22 trovate, 0 rimaste |

Le 22 trovate, chiuse nello stesso lotto:

- 6 erano difetti del verificatore sull'attacco (potenziamento in mezzo al
  nome dell'arma, Arma Focalizzata contata anche su un'altra arma, Arma
  Focalizzata Superiore non contata): senza tolleranza si usa il conto fine
  di `attacco_atteso`;
- 2 (Avarthel) erano il talento Anima Forte, ora fra le sorgenti;
- 16 numeri in 14 schede erano tiri salvezza senza sorgente. Scelta del DM
  (card del 2026-11-12): «tenere il numero, dichiarare la sorgente». Undici
  PNG e umanoidi ricevono un *mantello della resistenza* (+1 o +2, SRD), che
  alza anche gli altri tiri salvezza; tre creature fatte in casa (due
  razorfiend, la guardia d'élite dei miconidi) dichiarano un bonus razziale
  alla Volontà, segnato «Non SRD». Ogni scheda porta la nota in fondo.

Restano fuori dal lotto 1, detti: la CA del 3.5, i bonus all'attacco diversi
da potenziamento, perfetta, Arma Focalizzata e prisma; gli oggetti col prezzo;
BAB e lotta delle schede senza composizione leggibile.

### Lotto 1-bis — CA del 3.5, sensi e CD (2026-11-12)

`verifica_scheda` sul 3.5 non guardava la classe armatura: il cancello dei
moduli la controlla solo per il PF1e. Ora `dmcore.classe_armatura` legge la
parentesi di `ca-dettaglio` e ricostruisce la CA dalle sue voci:

- armature e scudi dalla tabella della capacità `creature.costruzione` (bonus
  base più potenziamento, Destrezza massima, mithral +2 alla Destrezza massima);
- gli altri bonus per tipo, con la stessa regola del cumulo del lotto 1
  (deviazione, naturale, potenziamento dell'armatura naturale, cognitivo, sacro,
  profano, fortuna, morale: vale il più alto; schivare e senza tipo si sommano);
- contatto (senza armatura, scudo e naturale) e sprovvista (senza Destrezza e
  schivare; con schivare prodigioso la Destrezza resta);
- una clausola a condizione («+1 contro i giganti») non entra nel numero.

Nella stessa passata entrano i conti che il cancello dei moduli faceva solo
sui recinti dei master: i sensi dati dalla razza e la CD delle capacità
speciali (10 + metà DV + caratteristica).

| | Prima (main) | Lotto 1-bis |
|---|---|---|
| Errori di CA messi apposta, visti da `verifica_scheda` | 0 su 379 | 377 su 379 |
| Scurovisione tolta a chi la ha, vista | 0 su 25 | 10 su 25 |
| Scarti veri trovati nel Bestiario | non misurati | 21 di CA in 18 schede, 10 di sensi, 0 di CD |
| Scarti rimasti dopo le correzioni | | 0 |

Banco: `plans/esperimenti/regole-senza-omissioni-2026-11-12/muta_ca.py`
(CA +1, CA −2, voce +1 con la somma che torna, contatto +1, sprovvista +1,
scurovisione tolta), misure in `misure-ca.json` accanto.

Cosa è stato corretto, con la regola del DM «il numero più forte, se si
ricostruisce da una scheda legale» (ADR-0118):

- 18 schede: la CA scritta non era la somma delle voci, oppure una voce non
  era quella della tabella. Dove due letture erano legali è rimasta la più
  alta: in 8 schede la CA sale di 1 (tra queste difensore nanico di Dauth,
  sacerdotessa drow, capitano githyanki, comandante del Teschio Nero), nelle
  altre cambia solo il dettaglio. Ogni scheda porta la nota in fondo;
- 10 schede: duergar, nani, gnoll, flind e orchi senza la scurovisione della
  razza nella riga `sensi:`;
- 1 difetto del verificatore: i dadi vita di più classi («12d8+4d10») si
  contavano solo dal primo gruppo, e la CD del soffio di Azarr Kul risultava
  sbagliata. Ora si sommano.

Limiti, detti:

- 28 schede su 145 restano **non verificabili** per la CA: 23 non elencano le
  voci, 4 nominano gli oggetti senza i bonus, 1 ha una voce che il lettore non
  riconosce. Stanno in `non_verificabili`, non fra le violazioni; il generatore
  dovrà scrivere le voci (lotti 2-5);
- 2 errori di sprovvista su 60 non si vedono (bruto deforme, alleato orso del
  druido): la Destrezza è negativa o la scheda non la scrive fra le voci;
- la scurovisione si vede solo per le razze che la tabella conosce (10 su 25):
  i mostri che la hanno per tipo arrivano col lotto dei tipi di creatura;
- gli **oggetti dell'SRD col prezzo** erano previsti qui e non ci sono: vanno
  nel lotto 8 insieme alla ricchezza per livello, perché senza quel tetto il
  prezzo da solo non giudica niente. Le armature salite a +1 e i mantelli del
  lotto 1 vanno ricontati lì;
- il PF1e non cambia: contatto, sprovvista e DMC stanno già nel cancello dei
  moduli.

### Lotto 2 — armi e danno (2026-11-12)

`verifica_scheda` non guardava il danno: né il dado, né il bonus, né il
critico. Ora la capacità `creature.armi` porta la tabella delle armi dell'SRD
(`sistemi/dnd35/dati/armi.toml`, 72 armi, scritto da `estrai_armi.py` da
«Table: Weapons» e dai nomi italiani del lessico) e `dmcore.danno` ricostruisce
il danno di ogni attacco con un'arma della tabella:

- **dado** della tabella portato alla taglia di chi impugna (SRD, «Weapon
  Size»); la taglia viene dalla riga `tipo:` o dalla voce di taglia della CA;
- **bonus**: Forza (una volta e mezza a due mani, metà con la mano secondaria,
  niente per archi e balestre, fino alla Forza per gli archi compositi), più il
  potenziamento dell'arma, più i talenti dichiarati (Arma Specializzata e
  Superiore sull'arma nominata; specialista del martello del chierico nano);
- **critico** della tabella; l'intervallo raddoppia con Critico Migliorato
  sull'arma o con un'arma affilata. Il 20/x2 si può tacere, gli altri no.

Una clausola a condizione («in Ira», «con Attacco Poderoso», «entro 9 m») non
si giudica. Il manuale base del PF1e ha le stesse 72 armi con lo stesso dado e
lo stesso critico (riscontro su PSRD-Data, 72 su 72): il plugin `pf1e` eredita
la capacità, ma la verifica resta sul 3.5 fino al lotto 10.

| | Prima (main) | Lotto 2 |
|---|---|---|
| Errori di danno messi apposta, visti da `verifica_scheda` | 0 su 364 | 336 su 364 (92%) |
| per campo: dado, critico tolto, critico sbagliato | 0 | 95/96, 54/54, 20/20 |
| per campo: bonus +1, bonus −2 | 0 | 80/97, 87/97 |
| Scarti veri trovati (Bestiario e moduli) | non misurati | 17: 15 critici non scritti, 2 bonus |
| Scarti rimasti dopo le correzioni | | 4, tutti di ARC-07, in attesa del DM |

Banco: `plans/esperimenti/regole-senza-omissioni-2026-11-12/muta_danno.py`,
misure in `misure-danno.json` accanto.

Cosa è stato corretto, in 11 schede del Bestiario:

- 12 critici non scritti (stocco 18-20, spada lunga e spadone 19-20, spada
  bastarda, balestre, pugnale): è il numero della tabella;
- il cavaliere githyanki d'élite: mazzafrusto pesante a due mani 1d10+3 →
  1d10+4 (Forza +3 per una volta e mezza), regola del DM «il numero più forte,
  se si ricostruisce» (ADR-0118).

Cosa **non** è stato corretto, e perché. Quattro scarti stanno nel master di
ARC-07 (`ARC07-DEF-4`) e nelle sue copie: toccarlo cambia le impronte dei
booklet della serata e la copia di Balvar che un test tiene uguale al
Bestiario. Restano violazioni nell'uscita di `verifica_scheda` e vanno al DM:

- Zog'tar, giavellotti Grandi 1d8+13: con Forza 30 la regola dà +10; +13 è il
  danno in Ira Superiore (Forza 36) e la riga non lo dice;
- guardie di Zog'tar, spadone 2d6+6 senza critico (19-20);
- Balvar, martello da guerra runico +1 senza critico (x3), nel master e nella
  scheda del Bestiario.

Difetti del verificatore trovati e chiusi lungo la strada: i talenti scritti
nella prosa sotto il recinto, la condizione scritta dopo la parentesi, la
stessa arma ripetuta senza nome, il potenziamento dello scudo che non va al
danno, il dado del colpo senz'armi del monaco.

Limiti, detti:

- **attacchi naturali** (78 righe) e **armi fuori tabella** (19: balista, nerbo,
  raffica, righe senza nome) restano non verificabili: il dado di un morso viene
  dalla creatura (lotto 5), le armi dei manuali arrivano con gli oggetti;
- 28 errori messi apposta su 364 non si vedono: un'arma a una mano senza scudo
  ammette due letture (una mano o due), l'arco composito ammette ogni bonus fino
  alla Forza, il monaco e le schede senza Forza leggibile non si giudicano;
- il danno aggiuntivo (furtivo, elementale, «più veleno») non si giudica;
- Arma Specializzata scritta senza l'arma fra parentesi vale come «forse»: sono
  ammessi il numero con e quello senza;
- i talenti di una scheda con più recinti si cercano dal recinto al successivo:
  una nota di un'altra creatura in quel tratto può ammettere un numero in più.

### Lotto 3 — incantatori: slot, conosciuti, livello e CD (2026-11-12)

`verifica_scheda` controllava che un incantesimo stesse nella lista della
classe, non quanti se ne possono lanciare. Ora la capacità
`creature.incantatori` porta le tabelle delle classi che lanciano (bardo,
chierico, druido, paladino, ranger, stregone, mago, adepto) e `dmcore.magia`
ricostruisce, per ogni lista di cui si leggono classe, livello e
caratteristica:

- **incantesimi al giorno**: la cella della tabella al livello di classe, più
  gli incantesimi bonus della caratteristica (la tabella dei bonus è una
  formula, riscontrata riga per riga dall'estrattore), più lo slot di dominio
  del chierico e quello di scuola del mago specialista. Si giudicano la riga
  «N/N+1/… al giorno» dell'intestazione, la parentesi «(5+1)» di una riga e il
  numero di incantesimi preparati: più degli slot è uno scarto, meno no (una
  scheda può scrivere solo gli incantesimi chiave);
- **incantesimi conosciuti** di bardo e stregone, fissi;
- **livello**: una riga a un livello che la classe non lancia ancora, o che la
  caratteristica non regge (serve 10 + livello);
- **CD**: 10 + livello + modificatore, +1 o +2 se la scheda dichiara
  Incantesimi Focalizzati.

I dati sono due file scritti da `estrai_incantatori.py`, solo numeri:
`sistemi/dnd35/dati/incantatori.toml` dall'SRD 3.5 e
`sistemi/pf1e/dati/incantatori.toml` dal PRD (PSRD-Data, book-cr). Il PF1e non
eredita: bardo e stregone non hanno slot di livello 0 (trucchetti a volontà),
il paladino lancia col Carisma, lo stregone ha i conosciuti di stirpe.

**Forma ibrida dichiarata.** Per il bardo il DM ha scelto la tabella del PF1e
(card del 2026-11-09, `[griglie.bardo]` di `creature.toml`). Una lista di bardo
3.5 che torna con la tabella PF1e non è una violazione: esce fra i non
verificabili con la regola `numero.incantesimi.variante`, perché il lotto 11
la scriva nel registro delle regole custom (D-B-ter). Una lista che non torna
con nessuna delle due tabelle è una violazione.

| | Prima (main 942899b5) | Lotto 3 |
|---|---|---|
| Errori messi apposta negli incantesimi, visti da `verifica_scheda` | 0 su 616 | 376 su 616 (61%) |
| di cui in liste che si leggono (classe, livello, caratteristica) | 0 su 449 | 376 su 449 (84%) |
| per campo: CD +1, CD −1 | 0 | 84/126, 80/126 |
| per campo: slot +1, slot −1, livello | 0 | 58/85, 48/85, 20/29 |
| per campo: un incantesimo in più | 0 | 86/165 |
| Scarti veri trovati (Bestiario e moduli) | non misurati | 40 righe in 9 file |
| `verifica_scheda Bestiario 0*/` | 14 violazioni in 9 schede | 54 in 17 |

Banco: `muta_magia.py`, misure in `misure-magia.json`.

Cosa ha trovato, e **non è corretto**: togliere un incantesimo preparato o
cambiare gli slot di un personaggio è una scelta del DM, e i moduli toccano i
booklet. Quattro schede del Bestiario stanno in un elenco «in attesa» esplicito
nel test del cancello:

- `ur-vrax-voce-del-drago-cr10` (chierico 9, Sag 23): ogni livello dal 1° al 5°
  ha uno slot in più della tabella (7+1 contro 6+1 al 1°);
- `morlin-coalhewer-cr12` (chierico 12, Sag 19): 3° e 4° livello, uno in più;
- `abbathor-cleric11-cr11` (chierico 11, Sag 18): 2° livello, 6+D contro 5+D;
- `lomyn-redtongue-bardo8-cr8`: slot da bardo 3.5 e conosciuti di 1° da bardo
  PF1e (5 contro 4), cioè nessuna delle due tabelle per intero;
- nei moduli: ARC-08 guida del DM (chierico 8, chierico 12, ranger 4 con
  incantesimi di 2°, druido 14) e schede (drago nero «come stregone 7»,
  6/8/8/6 contro 6/7/7/5), ARC-05 stanza runica, l'errata dell'arco
  post-Hammerfist (CD più alte di uno), `villans.md` della Corona (CD da
  Carisma 20 con Carisma 24 scritto).

Limiti, detti:

- 167 errori messi apposta su 616 cadono in liste che **non si leggono**: manca
  la caratteristica o il livello nel blocco (schede a prosa dei moduli), o la
  classe non ha tabella nel plugin (anima prescelta, accordo sublime: manuali,
  lotto 9). Stanno fra i non verificabili, una riga per lista;
- 73 errori in liste lette non si vedono: una CD dentro il margine degli
  Incantesimi Focalizzati (la scuola dell'incantesimo non si guarda ancora), un
  incantesimo in più in una riga che non riempiva gli slot, uno slot in meno
  che porta al numero giusto una riga già sbagliata;
- la verifica dei conosciuti guarda solo l'eccesso;
- oggetti che danno slot (perla del potere, anello della stregoneria) non si
  leggono: una scheda che li conta negli slot esce come violazione, e va
  dichiarata come per i bonus del lotto 1;
- il lotto 3 del piano aveva anche i requisiti delle classi di prestigio e il
  rigiudizio delle 7 violazioni vecchie: vanno in un **lotto 3-bis**, come è
  stato per la CA nel lotto 1.

### Lotto 3-bis — i requisiti delle classi di prestigio (2026-11-12)

Una scheda poteva scrivere «Blackguard 10» senza nessun'altra classe e
`verifica_scheda` non diceva nulla: dei requisiti d'ingresso delle classi di
prestigio non c'era un dato. Ora la capacità `creature.prestigio` li porta e
`dmcore.prestigio` li giudica contro il personaggio **prima** del primo livello
della classe, che è quando i requisiti servono. La scheda scrive il personaggio
com'è adesso, quindi ogni giudizio è una condizione necessaria:

- **bonus di attacco base**: quello che danno le altre classi (dalla
  composizione dei dadi vita, quando la scheda la scrive tutta);
- **gradi**: il requisito non supera il massimo che i dadi vita prima
  dell'ingresso permettono (3.5: dadi vita + 3; PF1e: dadi vita), e l'abilità è
  scritta nella scheda con un bonus che quei gradi li regge. Un'abilità di
  Forza o Destrezza scritta con un bonus basso resta un dubbio (la penalità di
  armatura può nascondere i gradi); una non scritta è una violazione;
- **talenti**: per nome. La parentesi («Arma Focalizzata (martello da guerra)»)
  non si giudica. Se la scheda ha un talento che la lettura non conosce, il
  talento mancante è un dubbio e non una violazione;
- **razza** e **allineamento**: quelli scritti nel tipo;
- **livello d'incantesimo**: una delle altre classi lancia incantesimi arcani o
  divini di quel livello, contando lo slot che viene solo dagli incantesimi
  bonus (paladino 8 con Saggezza 14).

**I dati, e quello che non c'è.** `estrai_prestigio.py` scrive due file, solo
nomi e numeri. `sistemi/dnd35/dati/prestigio.toml`: 15 classi dalle sezioni
«Requirements» dell'SRD 3.5 e 478 dai tag `PRE…` di PCGen per i manuali (un
nome dell'SRD vince). `sistemi/pf1e/dati/prestigio.toml`: le 10 classi del Core
dal PRD, con i loro gradi (assassino: Camuffare 2 e Furtività 5, non 4 e 8).
Un requisito che non si riduce a un numero (speciale, divinità, lingua,
regione, «due scuole a scelta») **non si copia**: se ne tiene il conto in
`non_verificati` e la scheda lo porta fra i non verificabili.

| | 3.5 (493 classi) | PF1e (10 classi) |
|---|---|---|
| Requisiti ridotti a un numero | 1.301 (60%) | 26 (70%) |
| Requisiti solo contati (`non_verificati`) | 877 (40%) | 11 (30%) |
| Classi con soli requisiti speciali | 39 | 0 |
| Classi di cui i dati non hanno nessun requisito | 17 | 0 |
| Classi in più manuali con requisiti diversi (`diverge`) | 6 | 0 |

Le 17 classi senza requisiti e le 6 che divergono non danno mai una
violazione: la scheda esce con un dubbio che dice di leggere il manuale.

| | Prima (main f33282c0) | Lotto 3-bis |
|---|---|---|
| Requisiti tolti apposta dalle schede vere, visti da `verifica_scheda` | 0 su 30 | 30 su 30 |
| Requisiti tolti a ogni classe dei dati, visti da `dmcore.prestigio` | non c'era | tutti (test su 503 classi) |
| Violazioni vere trovate nel Bestiario | non misurate | 3 in 2 schede |
| `verifica_scheda Bestiario 0*/` | 54 violazioni in 17 schede, 308 dubbi | 57 in 19, 315 dubbi |

Il banco (`muta_prestigio.py`, `misure-prestigio.json`) è piccolo e va letto
per quello che è: le schede con una classe di prestigio sono 8, tutte nel
Bestiario, e le mutazioni sono 30 (allineamento 5, razza 1, talento 10, abilità
8, livelli 6). Due mutazioni perse al primo giro erano difetti del banco, una
era un difetto vero del controllo (un'abilità di Destrezza non scritta passava
per dubbio) ed è corretta. Il 30 su 30 dice che la lettura di queste 8 schede
regge, non che reggerà su una scheda scritta in un altro modo. Nessun modulo
(`0*/`) ha una classe di prestigio che la lettura riconosca.

Cosa ha trovato, e **non è corretto** (i livelli di un PNG sono del DM): due
schede in un elenco «in attesa» esplicito nel test del cancello.

- `abbathor-blackguard-cr10`: «Blackguard 10» senza altre classi. La guardia
  nera chiede bonus di attacco base +6 e Nascondersi 5 gradi prima del primo
  livello: con zero livelli d'altro non si entra.
- `drow-assassina-lolth-cr10`: Ladro 4 / Assassino 5. Nascondersi e Muoversi
  Silenziosamente a 8 gradi chiedono 5 dadi vita prima dell'ingresso (massimo
  dei gradi 7 al 4° livello).

**Un buco del lotto 1, chiuso.** L'estrattore dei gradi non leggeva
«Spellcraft» (nell'SRD è l'unica abilità col titolo senza `<small>`):
`creature.gradi` aveva 37 abilità su 38 e Sapienza Magica non entrava né nel
massimo né nella somma dei punti. Corretto l'estrattore e rigenerato
`gradi.toml`: nessuna violazione nuova nelle 150 schede.

Limiti dichiarati: i requisiti si giudicano contro tutte le altre classi, non
contro l'ordine vero dei livelli (che la scheda non scrive), quindi un
personaggio con due classi di prestigio può passare anche se la prima è
servita a entrare nella seconda fuori ordine; oltre i 20 dadi vita il bonus di
attacco base non si ricostruisce; le razze si riconoscono in inglese e, in
italiano, solo per le cinque del lessico (elfo, gnomo, halfling, mezzelfo,
nano): le altre restano un dubbio; i 3.5 dei manuali vengono dai tag di PCGen
e non sono riscontrati sul libro. Il rigiudizio delle 7 violazioni di talenti
rimaste dalla #378 resta fuori: aspetta la risposta del DM alla card.

### Lotto 3-ter — l'avanzamento d'incantatore delle classi di prestigio (2026-11-12)

**Contesto.** Il controllo degli incantatori (lotto 3) giudicava una lista dal
livello scritto in testa, o da quello della classe nella riga `tipo:`. Una
classe di prestigio non entrava nel conto: «Chierico 3 / Assassino 2» con una
lista da chierico di 5° passava, e «Chierico 3 / Loremaster 2» senza livello
scritto si giudicava da chierico di 3°, con violazioni false sugli slot.

**Decisione.** I livelli della classe di prestigio che danno «+1 livello di
una classe che si aveva già» stanno nel plugin, in `prestigio.toml`, voce
`avanza` (`tipo`: arcane, divine, both, any o il nome della classe; `livelli`).
Li scrive `estrai_prestigio.py`: dall'SRD 3.5 e dal PRD PF1e la colonna
«Spells per Day» della tabella della classe, dai manuali 3.5 il tag
`ADD:SPELLCASTER` di PCGen, solo nomi e numeri. 201 classi 3.5 su 493 e 6 PF1e
su 10 hanno un avanzamento. `dmcore.prestigio.avanzamento` fa il conto;
`verifica_scheda`, regola nuova `numero.incantesimi.livello_incantatore`:
livello scritto in testa alla lista ≠ livelli della classe + avanzamento è una
violazione; se il livello non è scritto, la lista si giudica da quello che le
classi danno. È un dubbio, non una violazione, quando la classe viene da un
manuale e il plugin non ne ha l'avanzamento, quando due libri divergono, o
quando un'altra classe del personaggio potrebbe prendere quei livelli.

**Misura** (`muta_avanzamento.py`, `misure-avanzamento.json`). Nel Bestiario
una sola scheda ha una classe di prestigio che alza gli incantesimi, quindi il
banco le mette lui: in 6 schede con una lista giudicata, due livelli della
classe diventano due livelli di Loremaster (la lista resta giusta: controllo),
di Assassino o di Cavaliere Mistico (la lista è troppo alta: errore).

| | Prima (main d6c3740e) | Dopo |
|---|---|---|
| Liste troppo alte messe apposta, viste | 0 su 12 | 12 su 12 |
| Liste giuste (controllo) segnate a torto | 0 su 6 | 0 su 6 |
| `verifica_scheda Bestiario 0*/` | 72 violazioni, 321 dubbi | 72 violazioni, 321 dubbi |

**Conseguenze e limiti dichiarati.** Nessuna scheda vera cambia giudizio.
Balvar (chierico 9 / Runecaster 4, lista da chierico di 13°) torna. Il banco è
piccolo (6 schede) e sintetico. Il controllo parte solo se la scheda ha una
riga `tipo:` con la classe e il suo numero e una lista con gli incantesimi fra
asterischi: `underdark-dovil-runecaster-cr7` scrive in prosa «Incantesimi da
Diviner 5» mentre Diviner 5 / Deep Diviner 1 dà 6, e il controllo non lo vede
(trovato a mano, non corretto: lo decide il DM). Per i manuali 3.5 l'assenza
del tag in PCGen non prova che la classe non avanzi: per questo è un dubbio.
Le classi di prestigio con una lista propria (Assassino, Guardia Nera) non
hanno una tabella degli incantesimi nel plugin. Il livello d'incantatore di
paladino e ranger scritto come «LI» (metà del livello) non si confronta.

### Lotto 4 — il numero dei talenti (2026-11-12)

Il generatore sapeva quanti talenti spettano a un personaggio
(`dmcore.talenti.quanti`, dal lotto 3 delle regole complete); il verificatore
no: controllava i prerequisiti di ogni talento, non quanti fossero. Una scheda
con due talenti di troppo passava. Ora `verifica_scheda.numero_talenti` conta:

- **quanti ne spettano**: i generali per dadi vita (3.5: 1 + 1 ogni 3; PF1e: uno
  ai livelli dispari; i dadi vita razziali contano), i talenti bonus delle
  classi (capacità `creature.talenti`), il talento dell'umano. Per il ladro il
  conto è una forbice: una capacità speciale (3.5, dal 10°) o un talento da
  ladro (PF1e) può essere un talento oppure no;
- **quanti ne scrive la scheda**: le voci della riga, tolte quelle che la classe
  concede per nome (Seguire Tracce del ranger, Scrivere Pergamene del mago, i
  due del dominio della Guerra 3.5 se la scheda nomina il dominio) e quelle che
  la scheda **dichiara** fuori dal conto accanto al nome: «(B)» del mostro,
  «(razziale)», «(dominio)», «(difetto)», «(tratto)». Un nome che la lettura non
  conosce è comunque un talento scritto e si conta.

Regola `numero.talenti`: di più è una violazione, di meno pure (uno slot non
speso è un'omissione). Resta un dubbio, mai una violazione, quando il conto non
si può fare: una classe di cui il plugin non ha i talenti bonus (classi di
prestigio e dei manuali 3.5), la composizione dei dadi vita non letta, un
umanoide con più di tre dadi «razziali» e nessuna classe (sono livelli non
letti), prosa finita nella riga dei talenti.

I tre dati nuovi stanno in `talenti_in_piu.toml` dei due plugin (capacità
`creature.costruzione`), scritti a mano
con la fonte: umano +1 (SRD e PRD, «Humans»), dominio della Guerra 3.5,
livelli a cui il ladro può scegliere un talento.

| | Prima (main 74a6cf80) | Lotto 4 |
|---|---|---|
| Un talento in più o in meno messo apposta, visto da `verifica_scheda` | 0 su 127 | 101 su 127 (80%) |
| di cui nelle schede di cui il conto si può fare | 0 su 101 | 101 su 101 |
| nelle schede dove il conto è un dubbio (13 schede) | 0 su 26 | 0 su 26 |
| Schede del Bestiario fuori conto | non misurate | 15 su 73 |
| `verifica_scheda Bestiario 0*/` | 57 violazioni in 19 schede, 315 dubbi | 72 in 33, 321 dubbi |

Banco: `muta_numero_talenti.py`, misure in `misure-numero-talenti.json`. Dieci
mutazioni non entrano nel conto: cadono su una scheda già fuori conto e la
rimettono in regola, non sono un errore messo apposta. Le violazioni salgono da
57 a 72 perché il controllo vede di più: nessuna scheda è stata modificata.

Cosa ha trovato, e **non è corretto**: quale talento togliere, aggiungere o
dichiarare lo sceglie il DM. Quindici schede in un elenco «in attesa» nel test
del cancello:

- **di troppo** (11): `duergar-chierico3-cr4` (4 contro 2), `underdark-cleric-ainin-cr5`
  (4 contro 2: ha i due talenti del dominio della Guerra ma la scheda non nomina
  il dominio), `gnoll-hyenodon-rider-cr4` (3 contro 1), `ogre-skullcrusher-cr5`
  (5 contro 3), `drow-wizard7-cr8`, `duergar-ladro1-cr1`, `duergar-mago3-cr4`,
  `hell-hound-mezzoimmondo-cr4` (Seguire Tracce è il bonus del segugio: va
  scritto «(B)»), `myconid-sovereign-cr7`, `warpriest-tiamat-cr7`,
  `koth-signore-dei-dragoni-cr8` (uno di troppo ciascuna);
- **in meno** (4): `bruto-deforme-sottosuolo-cr11` (4 contro 6),
  `ogre-micelio-sporeborn-cr8`, `lomyn-redtongue-bardo8-cr8` e
  `avarthel-druido-cr9` (uno in meno; gli ultimi due sono umani).

**Le capacità dichiarate.** `verifica_scheda` leggeva 13 capacità dei plugin e
nel manifest ne dichiarava una (`creature.talenti`): lo stesso buco che la #376
ha chiuso per `genera_creatura`, trovato dal thread della documentazione. Ora le
dichiara tutte e 13 (misura: `misura_capacita_verifica_scheda.py`, da 1 su 13 a
13 su 13) e un test boccia una capacità letta e non dichiarata. I due plugin di
prova dichiarano le quattro che mancavano (`bonus.cumulo`, `creature.armi`,
`creature.incantatori`, `creature.prestigio`); nel censimento del plugin non
d20 lo strumento passa da «nessuna» a «in parte».

Limiti dichiarati: i difetti (Arcani Rivelati) e i tratti si accettano solo se
dichiarati, non si verifica che il personaggio li abbia; i talenti bonus dei
mostri del manuale non sono nei dati, si riconoscono solo dal «(B)»; i talenti
epici oltre il 20° non si contano a parte; gli «effetti dei talenti sui
numeri» del piano non sono in questo lotto (`dmcore.talenti.effetti` li calcola
per il generatore, il cancello ne riconosce una parte): restano da misurare.

### Lotto 4, seconda parte — gli effetti dei talenti sulle abilità (2026-11-12)

**Contesto.** Degli effetti dei talenti sui numeri, i conti di scheda
coprivano già pf (Robustezza), tiri salvezza (Tempra Possente, Riflessi
Fulminei, Volontà di Ferro), iniziativa (Iniziativa Migliorata), attacco (Arma
Focalizzata e Superiore, Arma Accurata) e danno (Arma Specializzata, lotto 2).
Restavano le abilità. Il conto dei gradi dava 3 punti di margine a **tutte** le
abilità di una scheda che nominasse, in qualsiasi punto del testo, un talento
d'abilità: «Allerta» alzava il tetto anche di Scalare, e bastava la parola
«agile» o «furtivo» in una frase («attacco furtivo») per avere il margine.

**Decisione.** Il bonus va solo alle abilità che il talento nomina, col suo
numero, e i numeri stanno nel plugin: `sistemi/dnd35/dati/effetti_talenti.toml`
(19 talenti: i quindici da +2 a due abilità e Abilità Focalizzata dell'SRD,
Abilità Focalizzata Epica, i due psionici) e `sistemi/pf1e/dati/effetti_talenti.toml`
(11 talenti del manuale base, col bonus che raddoppia a 10 gradi), generati da
`estrai_effetti_talenti.py` dalla riga «Benefit» delle fonti, solo nomi e
numeri, e letti dalla capacità `creature.gradi`. L'abilità scelta di Abilità
Focalizzata si legge fra parentesi; se manca, il bonus vale per tutte. Un
talento nominato fuori dalla riga dei talenti («Allerta dal famiglio», o una
riga dei talenti che la lettura non trova) vale lo stesso, ma solo sulle sue
abilità. In PF1e si prende il bonus alto quando i dadi vita permettono 10 gradi.

**Misura** (`muta_effetti_talenti.py`, `misure-effetti-talenti.json`): nelle 10
schede del Bestiario che nominano un talento d'abilità, il bonus di ogni abilità
alzato al valore più alto che il conto di prima accettava.

| | Prima (main 813213e4) | Dopo |
|---|---|---|
| Abilità fuori regola messe apposta, viste | 0 su 44 | 44 su 44 |
| Abilità in regola (talento da +3 proprio su quella) segnate a torto | 0 su 2 | 0 su 2 |
| `verifica_scheda Bestiario 0*/` | 72 violazioni, 321 dubbi | 72 violazioni, 321 dubbi |

**Conseguenze e limiti dichiarati.** Nessuna scheda vera cambia giudizio: il
conto dei gradi resta una condizione necessaria con un margine di 4 o più punti
(sinergia, razza), e vede gli errori grossi. Il banco tocca solo 10 schede,
perché solo quelle nominano un talento d'abilità. Il bonus PF1e a 10 gradi si
concede a chi ha 10 dadi vita, senza sapere se i gradi ci sono davvero.
«Furtivo» in «attacco furtivo» conta ancora come il talento Furtivo quando la
riga dei talenti non ne ha (ora solo su Nascondersi e Muoversi Silenziosamente,
prima su tutte). I talenti dei manuali che alzano un'abilità non sono nei dati.
Autoipnosi manca dalle abilità 3.5 del plugin (`gradi.toml`): il bonus di
«Autonomous» su quella non si applica. Gli effetti condizionali (Schivare,
Incantare in Combattimento, Resistenza Fisica) non spostano un numero scritto e
restano fuori. Con questo il lotto 4 del piano è chiuso.

### Lotto 3, coda — i fatti di una scheda in JSON (2026-11-12)

**Contesto.** Il controllo di coerenza della storia (regola S8) deve incrociare
«Tattiche» e «Descrizione» con la scheda: se la prosa fa lanciare un
incantesimo, la scheda deve averlo. Per farlo gli servono i fatti della scheda
con la riga, e li rileggeva per conto suo con espressioni sue.

**Decisione.** `verifica_scheda --fatti` (funzione `fatti`) stampa in JSON, per
file: i talenti (nome scritto, nome canonico, riga), gli incantesimi (nome,
canonico, livello, usi o slot, volte, riga), le capacità speciali (nome, tipo
Str/Sop/Mag, riga) e le righe di inizio e fine di ogni «Tattiche» e
«Descrizione». Non giudica nulla ed esce sempre 0. Usa le capacità che lo
strumento dichiara già (talenti e liste d'incantesimi): il manifest dei plugin
non cambia.

**Misura** (`misure-fatti-scheda.json`, `Bestiario 0*/`): 186 file con almeno
un fatto; 486 talenti canonici su 508; 626 incantesimi canonici su 688; 214
capacità speciali; 265 sezioni «Tattiche» in 111 file; 120 «Descrizione».

**Limiti dichiarati.** I talenti sono quelli della prima riga «Talenti» del
file: in un booklet con più blocchi gli altri non escono (dal 2026-11-13
escono in `blocchi`, vedi «Lotto 5, terza parte»). Un incantesimo
scritto in italiano che il dizionario dell'SRD non ha esce con `canonico`
nullo (62 su 688). Fuori da una scheda riconosciuta una riga «1° …» conta solo
se almeno un nome è un incantesimo noto, per non prendere gli elenchi di prosa.
Le capacità speciali senza la sigla fra parentesi non escono.

### Lotto 5, prima parte — la creatura base (2026-11-13)

**Contesto.** Un «Ogre + Barbaro 6» porta con sé i numeri dell'ogre: dadi vita
razziali, armatura naturale, dado degli attacchi naturali. Il motore non li
aveva: 85 attacchi naturali del Bestiario finivano fra i non verificabili con
«il dado viene dalla creatura», e l'armatura naturale scritta non si
confrontava con niente.

**Decisione.** Capacità nuova `creature.base` (`sistemi/dnd35/dati/creature_base.toml`,
scritto da `estrai_creature_base.py` sui blocchi di statistiche dell'SRD 3.5, e
`sistemi/pf1e/dati/creature_base.toml` dai Bestiary 1-4 di PSRD-Data, 1138
creature): per il 3.5 409 creature con taglia, tipo, dadi vita razziali, armatura naturale,
caratteristiche, attacchi naturali col dado, modificatore di livello e grado di
sfida; più la tabella dei draghi veri, dove il dado viene dalla taglia.
`dmcore/creature_base.py` trova la base **solo dove la scheda la dichiara**
nella riga della fonte («SRD *Ogre* + …», «MM p.33 Centaur + …»), in un file
con un blocco solo, e solo se il tipo del blocco è quello della base. Un
archetipo dichiarato (scheletro, immondo, avanzato…) ferma il confronto. Un
drago vero si riconosce dal colore scritto accanto alla parola «drago».
`verifica_scheda` ha la verifica `creatura_base` con due regole,
`numero.dv.razziali` e `numero.CA.naturale`, e il conto del danno giudica il
dado degli attacchi naturali della base quando la taglia è la stessa (con
Attacco Naturale Migliorato vale anche un passo in più).

**Scartato.** Dedurre la base dal sottotipo del `tipo` («umanoide (gnoll)»):
provato e tolto, perché un flind è un umanoide (gnoll) e non è uno gnoll, e
dava due violazioni false. Dedurla dal nome della scheda: «ghost lion» non è
un leone.

**Misura** (`misure-creature-base.json`, `Bestiario 0*/`, contro main 3cc11aee):
non verificabili 321 → 297; attacchi naturali senza dado 85 → 61 (i 24 chiusi
sono cinque draghi veri, tutti coi dadi della tabella); violazioni 72 → 73: la
nuova è vera, `gnoll-warrior2-cr2` scrive armatura naturale +2 e lo gnoll
dell'SRD ha +1.

**Limiti dichiarati.** Solo 8 schede del Bestiario dichiarano una base
dell'SRD nella fonte: la copertura è piccola finché le schede non la
dichiarano. I mostri dei manuali (abishai, flind, naga d'ossa) non sono nei
dati. Con taglia diversa dalla base il confronto resta un dubbio: l'avanzamento
per dadi vita non è nel motore. Il bonus di Forza degli attacchi naturali
(primario, secondario, unico) non si giudica. Modificatori razziali di
caratteristica, modificatore di livello e archetipi sono nei dati o nominati,
ma nessuna regola li usa ancora: restano della seconda parte del lotto.
In PF1e della base si usano dadi vita razziali e armatura naturale; il dado
degli attacchi naturali no, perché il conto del danno PF1e arriva col lotto 10,
e nessuna scheda PF1e del repo dichiara oggi una base: i dati PF1e sono
riscontrati solo sulle prove.

## Conseguenze

- Una scheda nuova deve dichiarare da dove viene ogni punto: il generatore
  dovrà scriverlo (lotti 2-5).
- Le violazioni salgono a ogni lotto prima di scendere: è la misura che si
  stringe, non le schede che peggiorano. L'elenco va al DM dopo ogni lotto.
- `verifica_scheda` resta nel canale testing: misura, non cancello.
- Il programma è di dodici lotti (piano in
  `plans/esperimenti/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md`);
  i parametri MCP nuovi (`motore`) arrivano coi lotti 11 e 12.

## Da rivedere se

- il registro delle ibride supera qualche decina di voci (serve una regola
  generale);
- una sorgente di bonus dei manuali diverge fra due fonti (D-D);
- il DM vuole un quinto motore (3.0, PF1e solo manuale base).

### Lotto 5, seconda parte — il grado di sfida (2026-11-13)

**Contesto.** Il grado di sfida è il numero che il DM usa per comporre un
incontro e per i punti esperienza, e nessuna verifica lo confrontava con la
scheda. Nel Bestiario 126 schede lo scrivono nel blocco.

**Decisione.** Verifica `grado_di_sfida` in `verifica_scheda`, regola
`numero.gs`, col conto puro in `scripts/dmcore/gs.py` e i numeri nella tabella
`[gs]` della capacità `creature.costruzione` (nessuna capacità nuova):

- chi è fatto di soli livelli di classe: 3.5, classe da PG = livello, classe da
  PNG = livello −1 (`[Private source — Dungeon Master's Guide 3.5]`, solo i
  numeri; l'SRD lo mostra nei blocchi: hobgoblin combattente di 1° GS 1/2);
  PF1e, livello −1 e livello −2 (PRD). Sotto 1 si scende per gradini;
- le razze che nell'SRD hanno la loro riga «Challenge Rating»: drow, duergar e
  svirfneblin +1 con classi da PG e pari al livello con classi da PNG; goblin −2
  e coboldo −3 con classi da PNG;
- creatura base più livelli (SRD, *Improving Monsters*): livello associato +1,
  non associato +½ finché i livelli non pareggiano i dadi vita d'origine. Quali
  livelli sono associati lo decide chi costruisce: il grado è legale dentro la
  forbice fra tutti non associati e tutti associati;
- creatura base senza livelli: il grado della base.

Non si giudica, e lo si dice fra i non verificabili: un modello o un innesto,
l'avanzamento per dadi vita, una cavalcatura nel blocco, classi da PG e da PNG
insieme, una razza fuori dalla fonte (githyanki, orog…) o non riconosciuta, una
scheda che non scrive la composizione dei dadi vita.

**Conseguenze.** Misura sul Bestiario e sugli archi: violazioni 30 → 33,
non verificabili 293 → 371. Delle 126 schede col grado, 49 sono in regola, 3
fuori (`duergar-ladro1-cr1`, `duergar-mago-ladro8-cr7`, `goblin-warrior1-cr05`:
decisione del DM, le schede non si toccano qui) e 74 dubbie con la ragione
scritta. Banco `muta_gs.py`: 92 gradi sbagliati messi apposta trovati su 98; i
6 che restano sono dentro la forbice legale di una creatura base con livelli.
Limiti: il conto per il livello di chi ha classi miste, i modelli e
l'avanzamento per dadi vita restano da fare; la base si riconosce dal nome
inglese (il «gigante delle colline» resta un dubbio).

### Lotto 5, terza parte — i fatti scheda per scheda (2026-11-13)

**Contesto.** `--fatti` dava i talenti della prima riga «Talenti» del file. In
un file con più schede (i master degli archi, i booklet) i talenti delle altre
non uscivano, e la regola S8 (le «Tattiche» contro la scheda, ADR-0125) saltava
ogni file con più di una riga «Talenti». Nel Bestiario i file saltati erano
cinque, e in tutti e cinque la seconda riga non era una seconda scheda: era una
nota citata con «>» o la stessa scheda riscritta più sotto.

**Decisione.** `fatti()` aggiunge la chiave `blocchi`: una voce per scheda del
file con titolo, righe di inizio e fine e talenti (nome, canonico, riga). Un
blocco comincia a ogni recinto `statblocco` e, fuori dai recinti, a ogni riga
«Talenti» non citata che ha un titolo fra sé e la scheda prima e nomina talenti
diversi. Un recinto senza talenti seguito dai talenti in prosa è una scheda
sola. Le altre chiavi non cambiano; `blocco_di(blocchi, riga)` dice di quale
scheda è una riga. S8 giudica un file con più schede scheda per scheda: le
«Tattiche» di un blocco contro i talenti, gli incantesimi e il testo di quel
blocco.

**Conseguenze.** Misura su `Bestiario 0*/` (595 file): talenti che `--fatti` dà
500 → 748 (720 col nome canonico), in 148 schede; 16 file hanno più di una
scheda. S8 sul Bestiario: schede lette 60 → 65, menzioni 220 → 246, violazioni
0 → 0, file non giudicati per «più schede» 5 → 0. Limiti: in un file con più
schede un blocco senza riga «Talenti» non giudica i talenti, e le «Tattiche»
scritte fuori da ogni scheda non si giudicano: tutti e due restano contati fra
i non verificabili. Il confine del blocco è il titolo che lo precede: una
«Tattiche» scritta sotto il titolo della scheda dopo passa a quella. S8 resta
sul Bestiario: sugli archi dà 33 segnalazioni non ancora lette una per una
(negazioni come «senza Estrazione Rapida», booklet generati che ripetono il
master), quindi lì non è né cancello né misura.

### Lotto 6, prima parte — le abilità di classe e il margine dei gradi (2026-11-13)

**Contesto.** La verifica delle abilità (ADR-0124) contava ogni grado come se
l'abilità fosse di classe e lasciava a tutti lo stesso margine fisso per
razza, sinergie e oggetti. Chi mette troppi gradi in un'abilità che la sua
classe non ha passava, e il margine largo copriva gli errori di due o quattro
punti. Il plugin non sapeva quali abilità sono di quale classe.

**Decisione.** `estrai_gradi.py` legge dall'SRD e scrive in `gradi.toml` del
plugin 3.5: `[di_classe]` (le abilità di classe di 38 classi; l'esperto, il
maestro del sapere, il discepolo dei draghi e le classi psioniche ed epiche non
hanno un elenco e restano fuori), `[di_dominio]` (le abilità che cinque domini
aggiungono al chierico), `[sinergie]` (per ogni abilità, quelle che con 5 gradi
le danno +2), `[razze]` (i bonus alle abilità delle sette razze dell'SRD),
`[margine]` e `[fuori_classe]` (costo 2, massimo diviso 2). `verifica_scheda`
ha la regola nuova `gradi.massimo.fuori_classe`: chi ha soltanto livelli di
classe, tutti con l'elenco, non supera la metà del massimo in un'abilità che
nessuna delle sue classi ha, e quei gradi contano doppio nella somma dei punti.
Il chierico riceve le abilità di tutti e cinque i domini, perché la scheda non
sempre li scrive: si sbaglia a favore della scheda. Per chi è di una delle
sette razze dell'SRD e non scrive «razziale» nel testo, il margine fisso lascia
il posto a un conto: 2 per l'oggetto, il bonus della razza, 2 per ogni
abilità che dà sinergia ed è scritta nella riga delle abilità.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 33 → 33, non
verificabili 371 → 371; nessuna scheda toccata e nessuna violazione nuova.
Banco `muta_abilita.py` (32 schede, main → qui): un'abilità +4 3 → 4, +8
19 → 19, +12 24 → 26; tutte +3 6 → 9, tutte +6 18 → 18; ogni abilità della riga
alzata da sola, casi nuovi: +2 1 → 2 su 162, +4 10 → 16 su 162. Il guadagno è
piccolo e si dice: su 130 schede lette 37 scrivono una riga di abilità coi
numeri, 18 hanno soltanto classi con l'elenco e 6 hanno il margine contato
(le altre sono goblinoidi, drow, duergar, cioè razze che l'SRD descrive fra i
mostri); le abilità fuori classe giudicate sono 8 in 4 schede. Limiti: la
penalità di armatura alla prova non si conta ancora; i gradi dichiarati fra
parentesi («8 gradi») non si leggono; i gradi comprati a un livello di una
classe che aveva l'abilità si contano di classe per tutte le classi della
scheda (l'SRD lo vuole livello per livello, e la scheda non lo dice); le razze
dei mostri non hanno i bonus alle abilità nel plugin; PF1e non ha queste
tabelle e resta com'era.

### Lotto 6, seconda parte — la penalità di armatura alla prova (2026-11-13)

**Contesto.** Il bonus che la scheda scrive per Scalare o Nascondersi ha già
dentro la penalità dell'armatura e dello scudo. Il conto dei gradi non la
conosceva: a un guerriero in armatura completa lasciava sei punti di margine in
più di quelli che ha, e a Nuotare dodici.

**Decisione.** `estrai_gradi.py` legge dall'SRD e scrive in `gradi.toml` del
3.5 la tabella `[penalita_di_prova]`: le nove abilità che la subiscono (dal
titolo «Armor Check Penalty» di ogni abilità), quella a cui vale doppia
(Nuotare), e la penalità di dodici armature e sei scudi con bonus e Des massima
(tabella «Armor and Shields»). `verifica_scheda` legge la riga della CA con lo
stesso lettore del conto della CA, riconosce armatura e scudo dal bonus e dalla
Des massima e aggiunge la penalità ai gradi minimi di quelle abilità. La
penalità è la più bassa possibile: ogni oggetto si conta perfetto (−1), il
mithral toglie 3 e il legnoscuro 2. Il carico, che la può solo alzare, non si
conta. Se il file ha più di una riga della CA con un'armatura, la penalità non
si conta: non si sa di chi è la riga delle abilità.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 33 → 33, non
verificabili 371 → 371; nessuna scheda toccata. Le schede del Bestiario con
un'armatura o uno scudo riconosciuti sono 62. Banco `muta_abilita.py` (32
schede, main → qui): un'abilità +4 4 → 4, +8 19 → 20, +12 26 → 26; tutte +3
9 → 10, tutte +6 18 → 20; ogni abilità da sola +2 2 → 3 su 162, +4 16 → 16 su
162. Il guadagno è di pochi casi. Limiti: PF1e non ha la tabella e resta
com'era; il carico non si conta; chi porta un'armatura fuori dalla tabella
dell'SRD non ha penalità. I gradi dichiarati fra parentesi non si leggono: nel
Bestiario li scrive abilità per abilità una scheda sola (la capitana Lorana),
altre tre li scrivono in prosa, e una regola per quattro schede non si fa.

### Lotto 7, prima parte — la velocità a terra (2026-11-13)

**Contesto.** Nessun controllo guardava la riga della velocità. Un umano in
armatura completa scritto a 9 metri, o un barbaro senza i suoi 3 metri in più,
passavano.

**Decisione.** `estrai_movimento.py` legge dall'SRD e scrive
`sistemi/dnd35/dati/movimento.toml`, dentro la capacità `creature.costruzione`:
la velocità a terra delle sette razze e chi non rallenta in armatura (il nano),
la categoria di ogni armatura, la tabella della velocità ridotta, il movimento
veloce del barbaro (+10 piedi, non in armatura pesante) e del monaco (per
livello, senza armatura né scudo). `verifica_scheda` ha la verifica nuova
`velocita`, regola `numero.velocita`: per chi ha soltanto livelli di classe ed
è di una delle sette razze, la velocità scritta deve essere quella della razza,
più il movimento veloce, ridotta dall'armatura media o pesante. Il mithral conta
una categoria più leggera. Se la scheda nomina stivali della velocità o
dell'andatura, *velocità*, *passo veloce* o *ritirata rapida*, o scrive una nota
nella riga stessa, uno scarto è un non verificabile e non una violazione.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 33 → 33, non
verificabili 371 → 371: le velocità giudicate sono tutte in regola. Portata:
100 schede del Bestiario hanno una riga di velocità, il controllo ne giudica 18
(le altre hanno dadi vita razziali o una razza che non è fra le sette). Banco
`muta_velocita.py` → `misure-velocita.json`: con 3 metri in più 15 su 18, con 3
metri in meno 15 su 18; su main 0 su 18. Le tre che sfuggono hanno una classe
che il plugin non conosce o un incantesimo che cambia la velocità. Limiti: il
carico non si conta; le velocità di volo, nuoto e scavo non si guardano; le
razze dei mostri e le creature base non hanno la velocità nel plugin; PF1e non
ha la tabella. Restano del lotto 7: resistenza agli incantesimi, riduzione del
danno, immunità dei tipi, sensi delle razze, linguaggi.

### Lotto 7, seconda parte — resistenza agli incantesimi e riduzione del danno (2026-11-13)

**Contesto.** Nessun controllo guardava la resistenza agli incantesimi e la
riduzione del danno. Un drow con la RI di un livello fa, o un barbaro di 10°
con la RD del 7°, passavano; e passava un rakshasa con livelli di classe che
tiene la RI del rakshasa senza livelli.

**Decisione.** `estrai_difese.py` legge dall'SRD e scrive
`sistemi/dnd35/dati/difese.toml`, dentro la capacità `creature.costruzione`:
le sei razze che l'SRD scrive con «spell resistance equal to N + class levels»
(azer 13, drow 11, arconte segugio 16, pixie 15, rakshasa 27, svirfneblin 11),
il monaco (livello + 10 dal 13°) e la riduzione del danno N/— del barbaro per
livello. `verifica_scheda` ha la verifica nuova `difese`, regole `numero.RI` e
`numero.RD`. I livelli di classe sono i dadi vita oltre quelli della razza
(presi dalla capacità `creature.base`; il drow e lo svirfneblin non ne hanno).
La razza conta solo se il tipo della scheda è quello della razza: il «cultista
rakshasa» umanoide non è un rakshasa. Chi dovrebbe avere la RI o la RD e non la
scrive è una violazione. Una nota fra parentesi accanto al numero, o un oggetto
o un incantesimo che dà la RI, fanno di uno scarto un non verificabile. Più
numeri diversi nella stessa scheda: non verificabile. Le righe di storia
(citazioni, «era:», registri delle correzioni) non si leggono.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 33 → 34, non
verificabili 371 → 372. La violazione nuova è il Collezionista (rakshasa con 11
livelli da stregone, RI 27 scritta contro 38 dell'SRD): la scheda non si tocca,
decide il DM, e intanto sta in `IN_ATTESA` di `test_difese.py`. Il dubbio nuovo
è la guardia nobile drow (RI 16 con la nota «drow noble +4», la regola dà 15).
Portata: 26 schede del Bestiario scrivono una RI e il controllo ne giudica 8 (6
in regola, una fuori, una dubbia); 4 scrivono una RD N/— e ne giudica 3. Banco
`muta_difese.py` → `misure-difese.json`: un punto in più o in meno alla RI 6 su
6 per verso, alla RD 3 su 3 per verso; su main 0. Limiti: la RI delle creature
senza livelli di classe e quella dei modelli non si guardano; la RD che non è
N/— (magia, adamantio, allineamento) non si guarda; PF1e non ha la tabella.
I sensi non entrano in questo lotto perché un controllo c'è già
(`conformita_statblocchi`, scurovisione dal tipo nel 3.5 e dalla razza in
PF1e). Restano del lotto 7: immunità dei tipi, linguaggi.

### Lotto 7, terza parte — le immunità del tipo (2026-11-13)

**Contesto.** Un non morto, un costrutto o un vegetale hanno dal tipo una lista
di immunità (SRD, tratti dei tipi). Una scheda che non le scrive lascia il DM a
ricordarsele al tavolo: è un'omissione, e nessun controllo la vedeva.

**Decisione.** `estrai_difese.py` legge dall'SRD anche le righe «Immunity to …»
(e «Mindless … immunity to all mind-affecting effects») dei sette tipi che ne
hanno: costrutto, drago, elementale, melma, vegetale, non morto, parassita.
Stanno in `[difese.immunita]` di `difese.toml`, con i nomi italiani del tipo e
le parole con cui una scheda scrive ogni immunità (scritti a mano, non vengono
dall'SRD). La verifica `difese` ha la regola nuova `tratti.immunita`: la scheda
di uno di quei tipi deve avere la formula («tratti dei non morti», «tratti
vegetali», «undead traits») oppure nominare ogni immunità in una riga che dice
«immune». Il tipo si legge prima della prima parentesi o virgola della riga del
tipo: un «aberration (undead)» o un mezzo-drago non si giudicano. Chi ha un
punteggio di Intelligenza non è senza mente: a costrutti, melme e parassiti
l'immunità all'influenza mentale si chiede solo se non lo hanno.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 34 → 37, non
verificabili 372 → 372. Le tre violazioni nuove sono tre non morti che non
scrivono i tratti del tipo (deathlock, leone spettrale, leone crudele
scheletrico, che scrive solo «Immune cold»): le schede non si toccano, decide
il DM, e intanto stanno in `IN_ATTESA` di `test_difese.py`. Portata: 21 schede
del Bestiario sono di uno dei sette tipi, 18 in regola. Banco `muta_difese.py`:
tolta la formula o un'immunità dell'elenco, 16 su 18; su main 0. Le due che
sfuggono (fungo fantasma, retriever) scrivono le immunità due volte, con la
formula e per esteso: tolta una resta l'altra. Limiti: non si guardano i
sottotipi (freddo, fuoco, arconte), né le immunità oltre la lista del tipo, né
«non soggetto a colpi critici»; PF1e non ha la tabella. Resta del lotto 7: i
linguaggi.

### Lotto 7, quarta parte — i linguaggi automatici (2026-11-13)

**Contesto.** Una scheda che scrive la riga dei linguaggi può dimenticare
quello che la razza dà da sé (il Nanico di un nano) o il Druidico di un druido.
Nessun controllo guardava quella riga.

**Decisione.** `estrai_linguaggi.py` legge dall'SRD i linguaggi automatici
delle sette razze e il Druidico del druido, e scrive
`sistemi/dnd35/dati/linguaggi.toml` dentro la capacità `creature.costruzione`.
`verifica_scheda` ha la verifica nuova `linguaggi`, regola `tratti.linguaggi`:
chi scrive una sola riga dei linguaggi, fuori dalle righe di storia, deve
averci quelli della sua razza e, se è druido, il Druidico. Due cose non si
giudicano, e sono scelte dichiarate. Chi non scrive la riga non è una
violazione: nel 3.5 il blocco delle statistiche non ha una riga dei linguaggi,
e nel Bestiario la scrivono 24 schede. Quanti linguaggi in più si possono avere
non si conta: dipende dalla regione (i linguaggi regionali della campagna) e
dai gradi di Parlare Linguaggi, che le schede non scrivono.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 37 → 37, non
verificabili 372 → 372: le righe giudicate sono tutte in regola. Portata: 24
schede con la riga, 7 giudicate (le altre sono di razze che la tabella non ha:
goblinoidi, orchi, draghi, immondi). Banco `muta_linguaggi.py` →
`misure-linguaggi.json`: tolto un linguaggio automatico, 13 su 13; su main 0.
Limiti: le razze dei mostri non hanno i linguaggi nel plugin; PF1e non ha la
tabella. Il lotto 7 è chiuso con questa parte; di tutto il lotto restano fuori
il carico, i sensi oltre quelli che `conformita_statblocchi` già guarda, la RD
che non è N/— e i sottotipi.

### Lotto 8, prima parte — il valore dell'equipaggiamento (2026-11-13)

**Contesto.** Nessun controllo guardava quanto vale l'equipaggiamento di una
scheda. Il plugin non aveva i prezzi degli oggetti magici, e l'SRD 3.5 non ha
la tabella del valore dell'equipaggiamento di un PNG per livello.

**Decisione.** `estrai_oggetti.py` legge dall'SRD i prezzi delle tabelle degli
oggetti magici (623 voci: armature, scudi e armi specifiche, pozioni, anelli,
verghe, bastoni, bacchette, oggetti meravigliosi) e il prezzo base del bonus di
potenziamento di armi e armature, e scrive `sistemi/dnd35/dati/oggetti.toml`
dentro la capacità `creature.costruzione`. La tabella dei PNG viene dal Dungeon
Master's Guide 3.5 (Tabella 4-23), che non è nell'SRD: nel repo entrano solo i
venti numeri, con la fonte e il riscontro in rete scritti nel file.
`verifica_scheda` ha la verifica nuova `ricchezza`, regola
`equipaggiamento.valore`. Somma solo gli oggetti dal prezzo certo: tredici
famiglie di nomi (anello di protezione, mantello della resistenza e del
carisma, amuleti, guanti, cintura, fascia, periapto, bracciali, stivali della
velocità, anello dello schermo mentale) e armature, scudi e armi «+N» per il
solo potenziamento. La somma è quindi un minimo, e il giudizio va in un verso
solo: se il minimo supera il valore della tabella per il livello effettivo
(dadi vita più modificatore di livello della creatura base, come dice l'SRD in
«Improving Monsters») è una violazione; sotto la tabella non si dice niente.
Se la razza non è una delle sette dell'SRD e la creatura base non è dichiarata,
lo scarto è un non verificabile.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 37 → 37, non
verificabili 372 → 374 (Therysol: 20.000 mo riconosciuti a 2 dadi vita, razza
senza modificatore di livello noto; Ghaurush al secondo incontro: livello
effettivo 22, oltre la tabella). Portata: 7 schede del Bestiario hanno oggetti
dal prezzo certo, 5 stanno sotto la tabella. Banco `muta_ricchezza.py` →
`misure-ricchezza.json`: aggiunti 75.000 mo a 125 schede, 24 violazioni, 88 non
verificabili, 0 perse, 13 fuori portata (oltre il 15° livello); su main 0.
Limiti dichiarati. Il guadagno è piccolo: poche schede scrivono
l'equipaggiamento, e 88 schede su 112 non si giudicano finché il plugin non ha
il modificatore di livello delle razze dei mostri (resto del lotto 5). Non si
contano pozioni, pergamene, bacchette, bastoni, capacità speciali di armi e
armature, materiali e oggetti comuni. Una violazione non dice che la scheda è
illegale: il DMG lascia dare a un PNG più equipaggiamento, ma allora conta nel
GS, e la scheda deve dirlo. PF1e non ha la tabella nel plugin.

### Lotto 5, quarta parte — il modificatore di livello delle razze senza dadi vita (2026-11-13)

**Contesto.** La verifica `ricchezza` (lotto 8) vuole il livello effettivo. Il
plugin aveva il modificatore di livello solo delle creature con dadi vita
razziali (`creature_base.toml`): hobgoblin, goblin, orchi, drow e duergar, che
l'SRD presenta come combattenti di 1° livello, restavano non verificabili.

**Decisione.** `estrai_mdl.py` legge dall'SRD ogni blocco «X, 1st-Level
Warrior» con la sua riga «Level Adjustment» e scrive
`sistemi/dnd35/dati/mdl.toml` dentro la capacità `creature.costruzione`: dieci
razze (aasimar +1, drow +2, duergar +1, goblin +0, hobgoblin +1, coboldo +0,
marinide +1, orco +0, svirfneblin +3, tiefling +1). `ricchezza` le usa quando
la scheda nomina una sola di queste razze, il tipo è quello della razza e non
c'è un modello (mezzo-drago, vampiro, immondo…): con un modello il
modificatore cambia e lo scarto resta non verificabile.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 37 → 37, non
verificabili 374 → 374. Banco `muta_ricchezza.py` (75.000 mo aggiunti a 112
schede): violazioni 24 → 57, non verificabili 88 → 55, perse 0. Limiti: i 55
rimasti sono creature con dadi vita razziali che non dichiarano la base nella
riga della fonte, draghi, modelli. La tabella serve oggi solo a `ricchezza`:
`grado_di_sfida` ha già le sue eccezioni di razza in `gs.toml` e non è stato
toccato. Del lotto 5 restano i modificatori razziali alle caratteristiche, i
modelli, l'avanzamento per dadi vita e i mostri dei manuali.

### Lotto 8, seconda parte — capacità speciali, pozioni, pergamene, bacchette (2026-11-13)

**Contesto.** La prima parte contava di un'arma il solo potenziamento e
riconosceva tredici famiglie di nomi scritte a mano. Uno «spadone sacrilego +2»
valeva 8.000 mo invece di 32.000, e pozioni, pergamene e bacchette non
contavano.

**Decisione.** `estrai_oggetti.py` aggiunge a `oggetti.toml` le tabelle delle
capacità speciali di armi (30) e di armature e scudi (43), col bonus
equivalente o il prezzo in mo, e i prezzi delle pergamene (586 incantesimi, il
più basso fra arcana e divina). `verifica_scheda` legge i nomi italiani dal
lessico (`scripts/lessico_it_35.tsv`): gli oggetti magici che hanno un prezzo
nel plugin, le capacità speciali, gli incantesimi di pozioni, pergamene e
bacchette. Quattro regole tengono la somma un minimo sicuro. Una capacità
speciale conta solo se sta attaccata al nome o al bonus («spadone sacrilego
+2», «spada lunga +1 infuocata e affilata»): «Arco +1 di tasso del Cerchio
Sacro» resta un +1. Se potenziamento e capacità passano il +10 resta il solo
potenziamento. Una bacchetta conta solo con le cariche scritte, in
proporzione. Fra più voci dello stesso incantesimo vale la meno cara.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 37 → 37, non
verificabili 374 → 374. Valore riconosciuto nelle righe dell'equipaggiamento
del Bestiario: 224.000 → 267.830 mo (30 → 34 oggetti). Banco
`muta_ricchezza.py`, seconda prova (uno spadone +3 sacrilego e sei pozioni
aggiunti a 125 schede): violazioni 41 → 57; la prima prova non cambia (57
violazioni, 55 non verificabili). Limiti: la capacità scritta prima del nome
all'inglese («+1 flaming longsword») non si legge; i bastoni non si contano
(le cariche cambiano il prezzo); materiali speciali e oggetti comuni restano
fuori; PF1e non ha le tabelle. Del lotto 8 restano i bastoni, i materiali e la
tabella PF1e.

### Addendum 2026-11-13: le due card delle difese hanno risposta

Il DM ha risposto alle due card rimaste dal lotto 7. La RI del Collezionista
è 38, come dà l'SRD (27 del rakshasa + 11 livelli di classe). Deathlock,
leone spettrale e leone crudele scheletrico scrivono «Tratti dei non morti».
Le quattro schede sono corrette e `IN_ATTESA` di `test_difese.py` è vuoto.
Misura su `Bestiario 0*/`: violazioni 37 → 33, non verificabili 374 → 374.

### Lotto 8, terza parte — adamantio, mithral, bastoni con le cariche (2026-11-13)

**Contesto.** Dopo la seconda parte restavano fuori dalla somma i materiali
speciali e i bastoni. Una «armatura completa +1 di mithral» valeva 1.000 mo
invece di 10.000.

**Decisione.** `estrai_oggetti.py` aggiunge a `oggetti.toml` la tabella
`[oggetti.materiali]` dalle due tabelle di «Special Materials» dell'SRD:
adamantio (armatura leggera, media, pesante, arma) e mithral (armatura
leggera, media, pesante, scudo). `verifica_scheda` somma il costo del
materiale al potenziamento, e conta anche l'oggetto senza «+N» («mithral
chainmail», «ascia di adamantio»). La categoria dell'armatura viene da
`[movimento.armature]`. Un bastone conta solo con le cariche scritte, in
proporzione alle 50 di un bastone nuovo, come le bacchette. Il materiale conta
solo attaccato al nome o al bonus; un'arma di mithral e uno scudo di adamantio
non si contano, perché la tabella non li prezza.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 33 → 33, non
verificabili 374 → 375. Il non verificabile nuovo è Ghaurush Cenerevento
(GS 16): col bastone del fuoco da 10 cariche (3.550 mo) l'equipaggiamento
arriva a 36.300 mo contro i 35.000 di un PNG di 13 dadi vita, ma il
modificatore di livello della razza non si conosce. Banco `muta_ricchezza.py`,
terza prova (armatura completa +1 di adamantio, ascia bipenne di adamantio,
bastone del fuoco con 40 cariche, aggiunti a 125 schede): violazioni 1 → 52.
Limiti: il materiale scritto dopo una capacità speciale («pugnale +1 infuocato
di adamantio») non si legge; ferro freddo, argento alchemico, legnoscuro e
pelle di drago restano fuori (dipendono dal prezzo o dal peso dell'oggetto);
il prezzo base degli oggetti comuni non si conta; PF1e non ha le tabelle. Del
lotto 8 restano il prezzo base degli oggetti comuni e la tabella PF1e.

### Addendum 2026-11-13: cinque decisioni del DM sulle card

Il DM ha risposto sulle card del 13/11 (thread dell'audit). (1) I due duergar
con classi da PG hanno il grado di sfida della regola: `duergar-ladro1-cr2.md`
GS 2 e `duergar-mago-ladro8-cr8.md` GS 8, con i file rinominati. (2) Il goblin
combattente di 1° è GS 1/3 come nell'SRD; il file resta
`goblin-warrior1-cr05.md`. `IN_ATTESA` di `test_grado_di_sfida.py` è vuoto.
(3) Le tre righe accorciate di Balvar in `ARC07-DEF-4` tornano intere: il DM
non ha scelto la consigliata, e la scheda di Balvar si spezza su due pagine
nel booklet della notte (tetto `schede_spezzate` da 0 a 1 per i due booklet
in `docs/audit/stampa-booklet.json`). (4) Terros ha 348 pf (30d8+210, +3 di
Robustezza); le soglie 260 e 172 restano. (5) Il talento *Wingover* si chiama
«Virare», come nelle due fonti italiane, e non più «Virata»: scheda di
Skullcrusher, `ARC07-DEF-4`, booklet e le altre schede che lo nominano; il
testo del talento è riscontrato sull'SRD («Monster Feats»). Misura su
`Bestiario 0*/`: violazioni 33 → 30, non verificabili 375 → 372. Il nome
`goblin-warrior1-cr05.md` resta per scelta del DM: `extract_statblocks.py`
lo sa da `GS_COL_NOME_VECCHIO`. Il `pf-dado` di Terros è `30d8+213`.

### Lotto 8, quarta parte — prezzo base, dove sta scritto l'equipaggiamento, dati di ADR-0134 (2026-11-14)

`oggetti.toml` del 3.5 ha `[oggetti.comuni]` (66 armi, 12 armature, scudi
per bonus alla CA, dalle tabelle «Weapons» e «Armor and Shields» dell'SRD) e
`[oggetti.perfetta]` (300 mo l'arma, 150 l'armatura). La verifica `ricchezza`
somma il prezzo base e la fattura a ogni arma o armatura magica e conta gli
oggetti comuni; legge l'equipaggiamento anche dentro la riga delle Statistiche
(la forma di ADR-0091) e nelle voci «Equipaggiamento da combattimento» e
«Altro equipaggiamento», e lo conta una volta sola se sta sia nel recinto sia
nella prosa. Regola nuova `equipaggiamento.da_png`: una creatura base che non
avanza per classe e non ha livelli di classe ha un tesoro, e la Tabella 4-23
non la giudica (`avanza = "classe"` su 52 creature di `creature_base.toml`).
Una riga «Equipaggiamento sopra la tabella: … DM …» dichiara lo scarto come
scelta del DM. I dati di PF1e (Tabella 14-9 e 454 PNG dei Codex) e la regola
ibrida stanno in [ADR-0134](ADR-0134-l-equipaggiamento-standard-viene-dai-codex-pf1e-entro-il-valore-del-3-5.md).

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 30 → 30, non
verificabili 372 → 374. Sette schede vere superano la tabella dei PNG ora che
l'equipaggiamento si legge dov'è scritto: Avarthel, Bothor e Malvur, il
comandante dei mercenari di Dauth, il blackguard e il chierico di Abbathor,
Krusk, Ur-Vrax. Il DM ha risposto alle sette card il 2026-11-14 («Tieni e
dichiara»): ogni scheda porta la riga «Equipaggiamento sopra la tabella:
scelta del DM» col valore, il tetto e il GS, nessun numero cambia e
`IN_ATTESA` di `test_ricchezza.py` è vuoto. Senza le sette dichiarazioni la
misura sarebbe 37. Banco `muta_ricchezza.py`,
quarta prova (gli oggetti della prima scritti nella riga delle Statistiche):
0 → 50 su 118. Limiti: una scheda PF1e non si giudica (mancano i prezzi
PF1e); ferro freddo, argento alchemico e gli altri materiali restano fuori;
uno scudo si prezza dal bonus alla CA, quindi «d'acciaio» vale come «di
legno» (7 mo invece di 20); la ricerca nei Codex lascia «?» sugli oggetti che
`ricchezza` non riconosce. Il lotto 8 è chiuso per il 3.5; restano i prezzi
degli oggetti PF1e.

### Lotto 7, quinta parte — i linguaggi delle razze senza dadi vita razziali (2026-11-14)

**Contesto.** La verifica `linguaggi` conosceva solo le sette razze del
capitolo delle razze. Una scheda di hobgoblin, orco, drow o duergar con la riga
dei linguaggi non si giudicava. L'ha chiesto il thread del volume, che scrive
le righe dei linguaggi nelle schede.

**Decisione.** `estrai_linguaggi.py` legge anche la riga «Automatic Languages»
che l'SRD scrive nel capitolo dei mostri per nove razze di `mdl.toml`: aasimar,
drow, duergar, goblin, hobgoblin, coboldo, orco, svirfneblin, tiefling. Il
marinide non ha la riga e resta fuori. La razza si riconosce come in
`ricchezza`: un solo nome di `[mdl.nomi]`, col suo tipo, e nessun modello nel
titolo. Restano fuori le razze coi dadi vita razziali (bugbear, gnoll, ogre,
troll, lucertoloide e le altre): per loro la riga dell'SRD vale per il
personaggio giocante, e il mostro del manuale può parlare meno.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni di `linguaggi` 0 → 0.
Banco `muta_linguaggi.py`: schede giudicate 7 → 14 su 24 con la riga, linguaggi
tolti e trovati 13 su 13 → 27 su 27. Nessuna scheda toccata.

### Lotto 6, terza parte — razze dei mostri, taglia e velocità nelle abilità (2026-11-14)

**Contesto.** Il margine contato voce per voce valeva solo per le sette razze
del capitolo delle razze. Un hobgoblin o un orco fatti di soli livelli di classe
tenevano il margine fisso di 4. Due regole dell'SRD mancavano del tutto: il +4
di taglia a Nascondersi dei Piccoli e il modificatore della velocità a Saltare.

**Decisione.** `estrai_gradi.py` legge i bonus alle abilità anche dal capitolo
dei mostri, per le nove razze senza dadi vita razziali che hanno la sezione dei
personaggi (le stesse dei linguaggi). Una sottorazza tiene per tetto anche i
bonus della razza da cui viene: il drow quelli dell'elfo, il duergar quelli del
nano, lo svirfneblin quelli dello gnomo. Razziale e taglia si sommano, perché
sono bonus di tipo diverso. `[salto]` porta la regola di Saltare: +4 ogni 10
piedi di velocità sopra i 30, −6 ogni 10 sotto. La velocità è quella scritta
nella scheda, e conta solo dove il margine è contato.

**Conseguenze.** Misura su `Bestiario 0*/`, verifica `abilita`: violazioni
0 → 1, non verificabili 2 → 2. La violazione nuova è Bothor e Malvur, nani a 6
metri con Saltare +6: con 9 gradi, +5 di Forza, −6 di armatura e scudo e −6 di
velocità la regola dà +2. La scheda non si tocca: decide il DM sulla card.
Banco `muta_abilita.py`: una abilità +4, 4 → 6 su 31; tutte +3, 10 → 12;
ciascuna +4, 16 su 162 → 24 su 160. Il guadagno è piccolo perché poche schede
di queste razze scrivono la riga delle abilità coi numeri.

**Limiti dichiarati.** La velocità scritta si prende per buona: se è sbagliata,
anche il conto di Saltare lo è. La verifica `velocita` conosce ancora solo le
sette razze. I bonus razziali delle razze coi dadi vita razziali restano nel
margine fisso.

### Lotto 7, sesta parte — la velocità delle razze senza dadi vita razziali (2026-11-14)

**Contesto.** La verifica `velocita` giudicava solo le sette razze. La terza
parte del lotto 6 prende per buona la velocità scritta per il conto di Saltare:
serviva giudicare quella velocità anche per hobgoblin, orchi e drow.

**Decisione.** `estrai_movimento.py` legge «base land speed» dal capitolo dei
mostri per aasimar, goblin, hobgoblin, coboldo, orco e tiefling; drow, duergar
e svirfneblin tengono la velocità di elfo, nano e gnomo, e il duergar come il
nano non rallenta in armatura. Regola nuova di prudenza, che vale per tutte le
razze: se la velocità scritta è quella ridotta da un'armatura media o pesante e
la scheda non scompone la CA, l'esito è un dubbio e non una violazione.

**Conseguenze.** Misura su `Bestiario 0*/`, verifica `velocita`: violazioni
0 → 2, schede giudicate 18 → 34 su 100. Le due violazioni sono vere e aspettano
il DM su due card: la Furia della Mano va a 12 m con una corazza di piastre,
che è media (la regola dà 9 m); il bladebearer hobgoblin scrive «corazza di
piastre +1» dove l'esportazione PCGen citata dice «Chain Shirt +1». Stanno in
`IN_ATTESA` di `test_velocita.py`. Banco `muta_velocita.py`: più 3 m da 15 su 18
a 27 su 34, meno 3 m da 15 su 18 a 26 su 34.

### Addendum 2026-11-14: tre decisioni del DM sulle card dei lotti 6 e 7

Il DM ha risposto alle tre card lo stesso giorno, e le schede sono scritte:

- Bothor e Malvur: «Correggi a +2». Saltare +6 → +2 in `Bestiario/png/bothor-malvur-cr6.md`.
- Furia della Mano: «Corazza di mithral, resta 12 m». La corazza di piastre +2
  è di mithral, conta leggera e i 12 m sono legali. La ricchezza dichiarata
  sopra il tetto sale da circa 32.700 a circa 36.700 mo contro 16.000.
- Bladebearer hobgoblin: «Scrivi giaco di maglia +1», come nella fonte PCGen.

Misura dopo le risposte: `abilita` 0 violazioni, `velocita` 0 violazioni,
`IN_ATTESA` di `test_velocita.py` vuoto.

### Lotto 8, quinta parte — la ricchezza di un file con più schede (2026-11-14)

**Contesto.** `ricchezza` usciva senza dire niente quando il file aveva più di
un recinto `statblocco`. Le dodici schede di ARC07-DEF-4 non erano giudicate
contro la Tabella 4-23, e una misura «senza violazioni nuove» lì voleva dire
«non controllate». L'ha trovato il thread del volume leggendo il codice.

**Decisione.** Un file con più schede si taglia coi blocchi di `--fatti`
(`_blocchi_dei_fatti`): ogni scheda va dal suo titolo alla scheda dopo e si
giudica da sola, con la riga contata nel file e il titolo nella chiave
`scheda`. La dichiarazione «Equipaggiamento sopra la tabella» vale solo per la
scheda che la porta. In un master il nome del file non aiuta a riconoscere la
razza: conta solo il titolo della scheda.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni di `ricchezza` negli
archi 0 → 1. È Durin Rocciadura (ARC07-DEF-4, riga 4428): armatura completa +1,
scudo pesante +1 e ascia da guerra nanica +1 valgono 6.137 mo contro i 5.600 di
un PNG di 6°. La scheda non si tocca: card al DM, titolo in `IN_ATTESA` del
cancello nuovo `Archi` di `test_ricchezza.py`.
Il DM ha scelto sulla card del 2026-11-14 lo scudo pesante perfetto al posto
dello scudo pesante +1: CA 22 → 21, `IN_ATTESA` vuoto, violazioni 1 → 0.

**Limiti dichiarati.** Le altre verifiche che leggono una scheda sola
(`velocita`, `linguaggi`, `abilita`) non sono ancora portate ai file con più
schede.

### Lotti 6 e 7 — velocità, linguaggi e abilità di un file con più schede (2026-11-14)

**Contesto.** Il limite dichiarato qui sopra: in un master d'arco `velocita` e
`linguaggi` uscivano mute (chiedono una sola riga in tutto il file) e `abilita`
giudicava soltanto la prima scheda.

**Decisione.** Il taglio fatto per `ricchezza` diventa una funzione sola,
`_scheda_per_scheda(p, giudica)`, e le quattro verifiche la usano. `VT.leggi`
ha la gemella `VT.leggi_testo` per leggere i livelli di classe del pezzo e non
del file.

**Conseguenze.** Misura su `Bestiario 0*/`: violazioni 30 → 30, non
verificabili 383 → 384 (un dubbio di `abilita` che prima usciva una volta ora
esce per due schede). I file con più recinti sono 5, con 30 schede, 17
leggibili: `velocita` ne legge 11 (prima 0), `linguaggi` 3 (prima 0), `abilita`
11 (prima le 5 in testa ai file). Nessuna violazione nuova e nessuna scheda
toccata.

**Limiti dichiarati.** 13 schede su 30 dei master non si leggono (senza riga
degli attributi o del GS nel recinto). Le altre verifiche di `verifica_scheda`
(talenti, incantatori, prestigio, difese, grado di sfida) hanno ciascuna il suo
modo di trattare i master e non passano da questa funzione.

### Lotto 8, sesta parte — merci, proiettili, pezzi doppi e arco composito (2026-11-14)

**Contesto.** Il thread del volume riempie le schede con l'equipaggiamento dei Codex e ha mandato l'elenco di 96 voci che `ricchezza` non sapeva prezzare: nessuna aveva un prezzo su main. Una voce senza prezzo non entra nel totale, quindi la verifica dà «almeno N mo» più basso del vero e una scheda troppo ricca passa.

**Decisione.** I prezzi che l'SRD 3.5 ha si leggono dall'SRD, col generatore e non a mano:

- `estrai_oggetti.py` scrive in `oggetti.toml` le merci di «Table: Goods and Services» (`[oggetti.comuni.merci]`; sotto 1 mo valgono 0), i proiettili col numero di pezzi del prezzo (`ammo`), lo scudo d'acciaio (`scudi_acciaio`), le armi che costano 0, le perle del potere e le collane delle palle di fuoco per tipo, il costo per punto di Forza dell'arco composito (`arco_forza`: 100 mo il lungo, 75 il corto) e i 6 mo di fattura perfetta di un proiettile.
- `_oggetti_col_prezzo` conta: le merci in inglese e in italiano (i nomi italiani vengono dal lessico, tipo `equipaggiamento`); le armi a più pezzi («2 pugnali +1», «giavellotti (4)») e al plurale; i proiettili comuni e magici (potenziamento diviso 50 per pezzo, più fattura e prezzo base); lo scudo «d'acciaio» scritto prima o dopo il bonus; «mezza armatura»; le pozioni con la forza nel nome e il numero di dosi; l'arco composito con la Forza scritta fra parentesi («(For +1)», «(+2 Str)»).
- «Pozione di scudo della fede +2» non è più letta come uno scudo +2.

**Cosa non entra.** L'arco composito conta la Forza solo se sta scritta accanto al nome: dal bonus ai danni non si deduce. Gli oggetti che ha solo PF1e (terbutje, dogslicer, o-yoroi, headband…) non hanno prezzo nell'SRD 3.5 e restano fuori: 33 voci su 96, che vanno a card e le porta il thread del volume. Ferro freddo, argento alchemico, veleni e «worth N gp» sono un secondo giro.

**Misura** (worktree pulito su 7193c7b7 contro il ramo). Elenco dei Codex: 0 → 63 voci col prezzo su 96. Nelle righe di equipaggiamento di `Bestiario` e degli archi: 472 → 489 voci col prezzo, 2.218.392 → 2.271.561 mo contati. `verifica_scheda.py Bestiario 0*/`: violazioni 30 → 30, non verificabili 384 → 384; cambiano due testi di «non verificabile» perché il totale sale (Therysol 20.335 → 20.435 mo per la lente; Vreek 22.100 → 26.704 mo per i due pugnali +1, prima contati zero). Il guadagno nel repo di oggi è piccolo (17 voci): serve alle schede che il thread del volume sta riempiendo.

**Conseguenze.** Lo scudo pesante «d'acciaio» +2 vale 4.170 mo e non 4.157: il test che lo fissava è aggiornato. Un totale che sale può far scattare una violazione di ricchezza su una scheda che prima passava per difetto: è il comportamento voluto, e una scheda non si corregge senza la risposta del DM.

### Lotto 5, quinta parte — i draghi veri per colore e categoria d'età (2026-11-14)

**Contesto.** Dei draghi veri `creature.base` aveva solo il dado degli attacchi per taglia. Dadi vita, armatura naturale e grado di sfida di un drago stanno nelle tabelle per età dell'SRD, e senza quelle i tre draghi del Bestiario uscivano «dadi vita razziali senza una creatura base riconosciuta».

**Decisione.** `estrai_creature_base.py` genera `[draghi_eta.<colore>]` in `creature_base.toml`: dieci colori per dodici età (120 voci) con taglia, dadi vita, armatura naturale, caratteristiche e grado di sfida, dalle tabelle «Dragons by Age» e «Dragon Abilities by Age» e dalla riga «Challenge Ratings». `creature_base.drago` porta questi numeri solo se il testo dice colore **ed** età («Drago Rosso (Young Adult)», «drago nero adulto maturo») e la taglia della scheda è quella dell'età. Poi:

- l'armatura naturale diversa da quella dell'età è una violazione (`numero.CA.naturale`);
- il grado di sfida si giudica dalla base, come per le altre creature;
- dadi vita diversi da quelli dell'età non sono una violazione: un drago cresce di dadi vita dentro la sua età (riga «Advancement»), e la scheda può essere di un'altra età. Esce «non verificabile»;
- un modello scritto nel tipo («Avanzato») cambia l'armatura naturale: «non verificabile», non violazione.

**Cosa non entra.** L'età non si deduce dai dadi vita o dalla taglia: va scritta. Caratteristiche, tiri salvezza, soffio e resistenza agli incantesimi per età non si giudicano ancora. I draghi di PF1e restano alla loro tabella dei Bestiary.

**Misura** (contro main bff08716). `verifica_scheda.py Bestiario 0*/`: violazioni 30 → 33, non verificabili 376 → 380. Le tre violazioni nuove sono vere e stanno su card al DM del 14/11: Arbitrax (GS 15 contro 13 e armatura naturale +24 contro +18 del giovane adulto rosso) e Tyrgarun (armatura naturale +29 contro +26: il titolo dice «Old», il corpo è del molto vecchio). Ozyrrandion torna: +19 è l'adulto verde, e i 22 dadi vita sono un avanzamento dichiarato. Skullcrusher (tre blocchi, «Avanzato» nel tipo) esce «non verificabile». I tre «senza una creatura base riconosciuta» dei draghi spariscono.

**Conseguenze.** Arbitrax entra in `IN_ATTESA` del cancello del grado di sfida finché il DM non risponde. Le schede non si toccano senza la sua risposta.

### Lotto 5, sesta parte — il grado di sfida di chi avanza per dadi vita (2026-11-14)

**Contesto.** Una creatura con più dadi vita razziali della sua base usciva sempre «avanzata per dadi vita»: non verificabile. L'SRD ha la regola («Table: Improved Monster CR Increase», `improving-monsters.md`).

**Decisione.** `gs.toml` ha `[gs.avanzamento]`: quanti dadi vita aggiunti danno +1 al grado di sfida, per tipo d'origine (4 per aberrazioni, costrutti, elementali, folletti, giganti, umanoidi, melme, vegetali, non morti, parassiti; 3 per animali, bestie magiche, umanoidi mostruosi; 2 per draghi ed esterni). `gs.atteso` la applica solo se:

- la scheda **dichiara** la base (riga della fonte, o colore ed età di un drago). Una base trovata solo per nome non basta: un flind non è uno gnoll avanzato, l'ogre Skullcrusher non è un ogre con più dadi vita;
- non ci sono livelli di classe («Do not stack this CR increase with any increase from class levels»);
- i dadi vita sono di più, non di meno.

Se la taglia non è quella della base il grado atteso è un intervallo: +1 se è cresciuta di taglia.

**Cosa non entra.** Le capacità speciali aggiunte (+1 o +2 a giudizio) non stanno nei dati: una scheda sopra il conto deve dichiarare lo scarto. Il PF1e ha un'altra regola e non è toccato.

**Misura** (contro main 676f296f). `verifica_scheda.py Bestiario 0*/`: violazioni 33 → 34, non verificabili 380 → 378. Ozyrrandion ora è giudicato e torna: adulto verde GS 13, due dadi vita in più, GS 14. Tyrgarun passa da «non verificabile» a violazione: «Old» GS 18 con 30 dadi vita, tre più del vecchio blu, dà GS 19. È la stessa scheda già su card al DM (età e grado di sfida): la violazione non è una scoperta nuova, è il conto che la card chiedeva. Flind e ogre Skullcrusher restano «non verificabili», come devono.

**Conseguenze.** Tyrgarun entra in `IN_ATTESA` del cancello del grado di sfida insieme ad Arbitrax, fino alla risposta del DM.

### Le tre risposte del DM del 2026-11-14: monaco, Arbitrax, Tyrgarun

**Contesto.** Tre scarti stavano su card al DM: la velocità del monaco «Pugno del Destino», armatura naturale e grado di sfida di Arbitrax, età e grado di sfida di Tyrgarun. Il DM ha risposto il 2026-11-14.

**Decisione.**

- Monaco «Pugno del Destino»: velocità 24 m → 15 m (hobgoblin 9 m, più 6 m del monaco di 7°); «Hobgoblin» torna nel titolo.
- Arbitrax: variante del DM, i numeri restano (armatura naturale +24, GS 15). È la voce RC-002 di `campaign/REGOLE-CUSTOM.md`.
- Tyrgarun: molto vecchio, GS 19, come l'SRD per 30 DV e +29 di armatura naturale. Le citazioni vive negli archi e in `state.md` seguono.

**Come si dichiara una variante.** Una riga «Armatura naturale diversa dalla base: N …» o «Grado di sfida diverso dalla regola: N …» con «DM», una voce RC o un ADR. Il primo numero dopo i due punti deve essere quello della scheda: se la scheda cambia e la riga no, lo scarto torna. È la stessa forma di «Equipaggiamento sopra la tabella» (lotto 8).

**Misura** (contro main 99c09bb6). `verifica_scheda.py Bestiario 0*/`: violazioni 34 → 30, non verificabili 378 → 375.

**Conseguenze.** `IN_ATTESA` del cancello del grado di sfida è vuoto. Il file di Tyrgarun diventa `tyrgarun-blue-very-old-cr19.md`: `extract_statblocks.py --check` vuole nel nome il GS del blocco. Il GS «16–17» di Tyrgarun a terra (Fase 4) non è stato ricalcolato: resta al DM.

### Lotto 5, settima parte — il grado di sfida dei modelli dell'SRD (2026-11-14)

**Contesto.** Una scheda con un modello nel tipo o nel titolo usciva sempre non verificabile. Dieci modelli dell'SRD 3.5 hanno il conto scritto nella riga «Challenge Rating» del loro «Creating a …».

**Decisione.** `gs.toml` ha `[gs.modelli_gs]`:

- aumento per soglie di dadi vita: celestiale e immondo (0, +1, +2 a 3, 7 e oltre), mezzo-celestiale (+1, +2, +3 a 5, 10 e oltre), mezzo-immondo (+1, +2, +3 a 4, 10 e oltre);
- aumento fisso: mezzo-drago +2 e mai sotto 3; lich, vampiro e fantasma +2;
- grado dai dadi vita: scheletro e zombi. La base non serve, i livelli di classe si perdono.

`gs.modello_noto` riconosce un solo modello e toglie le parole che lo accompagnano («template», «archetipo», «augmented»). Se resta un avanzamento, una cavalcatura o un secondo modello il grado resta non verificabile. Per i modelli ad aumento il conto è quello della scheda senza modello, più l'aumento; i dadi vita per le soglie sono quelli razziali più i livelli.

**Cosa non entra.** Il licantropo conta i dadi vita dell'animale, che la scheda non separa. Il mezzo dado vita dello scheletro (GS 1/6) e dello zombi (GS 1/8) non si legge. I modelli dei manuali non OGL non sono nei dati. L'armatura naturale e le caratteristiche che il modello cambia non si riscontrano ancora.

**Misura** (contro main ce805024). `verifica_scheda.py Bestiario 0*/`: violazioni 30 → 31, non verificabili 375 → 372. Draxoksus ora è giudicato e torna (hobgoblin di 6° mezzo-immondo, 6 + 2), e così l'hell hound mezzo-immondo (3 + 1): `[gs.nomi_base]` dice che «hell hound» nel titolo è «hellhound» nei dati. Skeletal Dire Lion da non verificabile a violazione: 16 dadi vita da scheletro danno 7, la scheda scrive 6. Il gufo gigante celestiale ora trova la base ma resta non verificabile: ha 8 dadi vita contro 4 e la fonte, che nomina un modello, non vale come base dichiarata. L'ariete celestiale non ha una base nell'SRD.

**Conseguenze.** Skeletal Dire Lion entra in `IN_ATTESA` fino alla risposta del DM (card del 2026-11-14). Nella stessa PR: `conformita_statblocchi._attacco_di_scheda` non legge più come attacco una voce di equipaggiamento, talenti o abilità («doppia ascia orchesca +1 (…)» in una scheda senza `attacchi:`); lo stato dei numeri sul repo non cambia.


### Lotto 5, ottava parte — la base dichiarata con un modello che non ne cambia i numeri (2026-11-14)

**Contesto.** Una fonte che nomina un modello non dichiarava mai la base: il gufo gigante celestiale («SRD 3.5 (gufo gigante, avanzamento a 8 DV, modello celestiale)») restava senza riscontro su dadi vita, armatura naturale, dadi degli attacchi e grado di sfida.

**Decisione.** Tre regole, tutte in `creature_base.dichiarata` e in `verifica_scheda.creatura_base`:

- celestiale e immondo (SRD, celestial-creature e fiendish-creature) lasciano alla base dadi vita, armatura naturale e attacchi: la fonte che nomina solo loro dichiara la base. I «mezzi» (mezzo-celestiale, mezzo-immondo, mezzo-drago) no, perché cambiano armatura naturale e caratteristiche;
- la base può stare fra parentesi dopo «SRD 3.5» e avere il nome di `[gs.nomi_base]` («gufo gigante», «hell hound»);
- se la fonte dichiara l'avanzamento («avanzamento a 8 DV», «advanced to 8 HD») e i dadi scritti sono quelli, con il dado della base, i dadi vita in più non sono una violazione. Il grado di sfida li conta già (tabella «Improved Monster CR Increase»).

**Cosa non entra.** Il massimo della riga «Advancement» di ogni creatura non è nei dati: un avanzamento dichiarato oltre quel massimo passa. Le caratteristiche che crescono con la taglia non si riscontrano. L'armatura naturale dei «mezzi» e dello scheletro resta da fare.

**Misura** (contro main 2ade1d5c). `verifica_scheda.py Bestiario 0*/`: violazioni 31 = 31, non verificabili 372 → 369. Le tre voci tolte sono del gufo gigante celestiale, ora giudicato per intero e in regola (3 della base, +1 per quattro dadi vita in più, +2 da celestiale con 8 dadi vita = 6). Nessun'altra scheda cambia giudizio.

**Scartato in corsa.** Far dichiarare la base a qualsiasi fonte che ne contenga il nome accanto a un modello: l'Ogre Skullcrusher (Races of Faerûn, col nome «Ogre» nel percorso del file) diventava un ogre dell'SRD avanzato e prendeva una violazione falsa sul grado di sfida.

### Lotto 5 — risposta del DM sullo Skeletal Dire Lion (2026-11-14)

**Decisione del DM** (card del thread delle regole, 2026-11-14): i 16 dadi vita restano e il grado di sfida è 7, il valore che l'SRD dà a uno scheletro da 16 dadi vita. La scheda toglie «2x HD» (il modello scheletro non raddoppia i dadi vita) e scrive che il leone crudele ha 16 dadi vita di suo.

**Conseguenze.** Il file diventa `Bestiario/mostri/skeletal-dire-lion-cr7.md`, perché `extract_statblocks --check` vuole il grado nel nome; aggiornati i rimandi vivi (composizione delle armate, incontri del viaggio verso Cannath Vale, catalogo storico, baseline dei punteggi), rigenerati catalogo e impronta. `IN_ATTESA` di `test_grado_di_sfida.py` torna vuoto. Misura contro main e88959fd: violazioni 31 → 30, non verificabili 368 = 368.

**Non toccato, resta al DM.** Il livello d'incontro delle due righe della tabella del viaggio che usano questi leoni (10 e 12) e i PX. L'armatura naturale +4 della scheda: lo scheletro Grande dell'SRD ha +2, e il controllo dell'armatura naturale dei modelli non c'è ancora.

### Lotto 5, nona parte — l'armatura naturale dei modelli dell'SRD (2026-11-14)

**Contesto.** Il controllo dell'armatura naturale guardava solo la creatura base dichiarata. Chi porta un modello (mezzo-immondo, mezzo-drago, lich, vampiro, scheletro, zombi) restava fuori, e lo Skeletal Dire Lion scriveva +4 senza che nessuno lo vedesse.

**Decisione.** Ogni voce di `[gs.modelli_gs]` in `sistemi/dnd35/dati/gs.toml` prende una chiave `naturale` con la riga «Armor Class» del suo «Creating a …» dell'SRD: mezzo-celestiale e mezzo-immondo +1 sopra la base, mezzo-drago +4, vampiro +6, lich +5 o la base se è più alta, scheletro il numero della taglia al posto della base, zombi un numero per taglia sopra la base. `gs.naturale_col_modello` fa il conto; `verifica_scheda._naturale_col_modello` lo applica alle schede con un blocco solo e un solo modello riconosciuto (lo stesso riconoscimento del grado di sfida), dentro la verifica `creatura_base` e con la regola `numero.CA.naturale`.

**Dove la base si conosce.** Lo scheletro non ne ha bisogno. Per gli altri la base è nota solo se il tipo nomina una razza di `razze_fonte`, cioè una razza fatta di soli livelli di classe: 0, il coboldo +1 (`naturale_razze`). Negli altri casi si giudica solo il minimo che il modello dà da solo, e sopra il minimo la scheda resta non verificabile. La variante del DM si dichiara con la stessa riga «Armatura naturale diversa dalla base: N …».

**Cosa ha trovato, e la risposta del DM.** `skeletal-dire-lion-cr7.md` scriveva +4, l'armatura del leone crudele vivo; lo scheletro Grande ha +2. Il DM ha scelto sulla card del 2026-11-15 «+2 come l'SRD, CA 13»: la scheda è corretta in questa stessa PR (CA 15 → 13). Draxoksus (hobgoblin mezzo-immondo, +1) ora è giudicato e torna. `hell-hound-mezzoimmondo-cr4.md` scrive la CA senza addendi e resta non verificabile.

**Misura** contro main fc5c1a8e con `verifica_scheda.py Bestiario 0*/`: violazioni 30 = 30, non verificabili 368 → 369 (il cane infernale mezzo-immondo); schede con modello giudicate sull'armatura naturale 0 → 2.

**Limiti dichiarati.** Azarr Kul (versione finale) e Therysol sono mezzi-draghi ma il tipo scrive solo «dragon (augmented …)»: il modello non si riconosce e il loro +4 non è giudicato. Il Ghostlord non ha la riga del tipo nel blocco: il +5 da lich non è giudicato. Il fantasma (bonus di deviazione dal Carisma) e il licantropo (+2, forme diverse) non hanno la chiave. Le caratteristiche che i modelli cambiano non sono in questo pezzo. PF1e non ha `[gs.modelli_gs]`: lì il controllo tace.

### Lotto 5, decima parte — le caratteristiche che i modelli dell'SRD cambiano (2026-11-15)

**Contesto.** I modelli cambiano le caratteristiche: i «mezzi» le alzano, i non morti perdono la Costituzione, scheletro e zombi perdono anche l'Intelligenza e hanno Saggezza 10 e Carisma 1. Nessun controllo lo guardava.

**Decisione.** Ogni voce di `[gs.modelli_gs]` prende una chiave `caratteristiche` con la riga «Abilities» del suo «Creating a …» dell'SRD: `piu` (aumenti sopra la base), `senza` (punteggi tolti), `fisse` (punteggi fissati), `almeno` (celestiale e immondo: Intelligenza 3). `gs.caratteristiche_col_modello` fa il conto; `verifica_scheda._caratteristiche_col_modello` lo applica dentro la verifica `creatura_base`, alle schede con un blocco solo e un solo modello riconosciuto, con la regola `numero.caratteristiche.modello`. Una violazione sola per scheda, con tutti i punteggi che non tornano.

**Dove la base si conosce.** I punteggi tolti e fissati si giudicano sempre. Gli aumenti si giudicano solo sopra la creatura base che la fonte dichiara («MM Dire Lion + Skeleton template»): `creature_base.dichiarata` prende `col_modello=True` e rende la base anche quando la fonte nomina il modello. Servono la stessa taglia e nessun livello di classe. Il punteggio scritto non può stare sotto base più aumento; sopra può starci (un punto ogni quattro dadi vita, gli oggetti) e non si giudica. Negli altri casi il controllo dice che gli aumenti non si riscontrano. La variante del DM si dichiara con la riga «Caratteristiche diverse dal modello: …» con DM, RC o ADR.

**Cosa ha trovato.** `skeletal-dire-lion-cr7.md` scrive Des 15 e Car 10, i punteggi del leone crudele vivo: lo scheletro ha Des 17 e Car 1. Con Des 17 la CA passa da 13 a 14 e i Riflessi da +7 a +8. Il DM ha scelto sulla card del 2026-11-15 «Des 17 e Car 1 come l'SRD»: la scheda è corretta in questa stessa PR (CA 13 → 14, Riflessi +7 → +8). Letta a mano, fuori dal controllo: `hell-hound-mezzoimmondo-cr4.md` ha nel titolo «mezzo-immondo» ma i punteggi (For 15, Cos 15, Car 8 contro 13, 13, 6 del segugio dell'SRD) e il sottotipo «dragonblood» sono del modello draconico di un manuale fuori dall'SRD; sulla card il DM ha scelto «Rifarlo mezzo-immondo dall'SRD», e la scheda si rifà in una PR sua.

**Misura** contro main 53d48bfe con `verifica_scheda.py Bestiario 0*/`: violazioni 30 → 31 prima della risposta del DM (lo Skeletal Dire Lion) e 30 = 30 dopo la correzione, non verificabili 369 → 371 (segugio infernale e Draxoksus: la fonte non dichiara una base dell'SRD). Schede con modello giudicate sulle caratteristiche 0 → 5.

**Limiti dichiarati.** Le schede con più blocchi restano fuori, come per l'armatura naturale. Sopra il minimo non si giudica: un punteggio troppo alto passa. Con livelli di classe i punteggi di partenza non sono quelli dell'SRD e gli aumenti non si riscontrano. Il licantropo non ha la chiave. PF1e non ha `[gs.modelli_gs]`.

### Lotto 7, settima parte — la velocità delle creature coi dadi vita razziali (2026-11-15)

**Contesto.** La verifica `velocita` giudicava solo chi è fatto di soli livelli di classe. Un ogre barbaro o un bugbear ladro uscivano senza giudizio: «la velocità è della creatura».

**Decisione.** `estrai_creature_base.py` legge dalla riga «Speed» dell'SRD la velocità a terra senza armatura («base speed 40 ft.» dove la riga parte da quella in armatura) e la scrive come `vel` in `creature_base.toml`: 378 creature su 409, le altre non camminano. `verifica_scheda._creatura_per_la_velocita` prende la creatura base che la fonte dichiara, con la stessa regola del lotto 5 (un blocco solo, stesso tipo), e il conto prosegue come per le razze: movimento veloce del barbaro e del monaco, armatura media o pesante che riduce, mithral. Taglia diversa dalla base: dubbio.

**Cosa ha trovato.** `ogre-frantumapietra-barbaro6-cr9.md` scrive 12 m con la nota «12 m anche in armatura: andatura veloce da Barbaro». L'SRD dà 40 piedi all'ogre, +10 al barbaro, e la cotta di maglia media riduce 50 a 35: 10,5 m. La nota nella riga fa dello scarto un dubbio e non una violazione; la scheda non si tocca e la scelta è del DM, su card. Il DM sceglie sulla card del 2026-11-15 «10,5 m come l'SRD»: la riga e la prosa ora scrivono 10,5 m in cotta di maglia e 15 m senza armatura.

**Ricchezza coi dadi vita dichiarati.** La verifica `ricchezza` prendeva il livello dalla somma delle classi lette; una classe che il parser non riconosce («Diviner 5») abbassava il livello e faceva sembrare troppo ricco un corredo giusto (Dovil Runecaster, patch del thread del volume). Ora il livello è il massimo fra quella somma e i dadi vita dichiarati nella scheda (`L.dv_totali`). Test `TestDadiVitaDichiarati`.

**Misura** sopra il pezzo precedente con `verifica_scheda.py Bestiario 0*/`: violazioni invariate, non verificabili 371 → 372 (l'ogre). Schede coi dadi vita razziali che arrivano al giudizio della velocità 0 → 5 (bugbear assassino, gnoll in sella, gufo gigante celestiale, ogre barbaro, Ghaurush). Banco `muta_velocita.py`: giudicate 34 → 42 su 100, più 3 m trovate 33 su 42, meno 3 m 31 su 41; il file delle misure era fermo a prima di due correzioni del DM, quindi non tutto il guadagno è di questo pezzo.

**Limiti dichiarati.** Solo la velocità a terra: volo, nuoto, scavare e scalare non sono nei dati. Solo il 3.5: `creature_base.toml` del PF1e non è rigenerato. Le schede con più blocchi e quelle che non dichiarano la base dopo «SRD» o «MM» restano fuori. Lo gnoll in sella e Ghaurush scrivono una nota nella riga: uno scarto lì sarebbe un dubbio, e il banco li conta fra i persi.


### Lotto 5, undicesima parte — il segugio infernale rifatto mezzo-immondo e l'armatura naturale sopra la base dichiarata (2026-11-17)

**Contesto.** Il DM ha scelto sulla card del 2026-11-15 «Rifarlo mezzo-immondo dall'SRD» per `hell-hound-mezzoimmondo-cr4.md`: la scheda portava i numeri del modello draconico di Races of the Dragon (For 15, Cos 15, Car 8, sottotipo dragonblood, Clinging Breath) sotto il nome «mezzo-immondo». Il controllo dell'armatura naturale dei modelli (nona parte) conosceva la base solo per chi è fatto di livelli di classe con una razza della fonte nel tipo: per tutti gli altri giudicava il minimo del modello.

**Decisione.** La scheda si rifà dal segugio infernale dell'SRD più il mezzo-immondo dell'SRD, con la fonte scritta come «SRD 3.5 Hell Hound + modello Half-Fiend (SRD)», così la base è dichiarata. La versione di prima resta nel blocco storico della scheda. La verifica `creatura_base` usa per l'armatura naturale anche la base che la fonte dichiara, se ha la stessa taglia del blocco: l'armatura naturale cambia con la taglia, non coi dadi vita né coi livelli di classe. Il conto diventa esatto (base più modello) e un bonus in più si dichiara con la riga di variante del DM, come per gli altri modelli.

**Conti della scheda.** For 17, Des 17, Cos 15, Int 10, Sag 10, Car 8 (13/13/13/6/10/6 più 4/4/2/4/0/2). CA 19 (+3 Des, +6 naturale: +5 del segugio, +1 del modello). Iniziativa +7. Tiri salvezza +6/+7/+4. Lotta +7. Artigli 1d4+3 primari, morso 1d8+1 secondario (−5, metà Forza; l'1d8 del segugio batte l'1d6 della tabella del modello) più 1d6 di fuoco. Soffio CD 14. Punire il bene +4, *oscurità* 3/giorno e *dissacrare* 1/giorno (Int 10). RD 5/magia, RI 14, immunità al veleno, resistenze 10. Grado di sfida 3 + 1 = 4. Abilità: (8 + Int 0) × (4 + 3) = 56 punti; le sei del segugio al massimo ne prendono 42, gli altri 14 vanno fuori classe come ha scelto il DM sulla card del 2026-11-17 (Acrobazia 3, Intimidire 3, Scalare 1; Acrobazia +8 con la sinergia di Saltare). Talenti dell'SRD (Iniziativa Migliorata, Correre, Seguire Tracce B): Enlarge Breath del .pcg viene da un manuale fuori dall'SRD.

**Misura** contro main ec5fca70 con `verifica_scheda.py Bestiario 0*/`: violazioni 34 = 34, non verificabili 388 → 387. Il segugio si giudica ora su CA, armatura naturale e caratteristiche, e passa; restano non verificabili i dadi dei suoi attacchi naturali, perché la verifica del danno non applica ancora la tabella dei modelli.

**Limiti dichiarati.** La base dichiarata vale solo con la stessa taglia. Il dado degli attacchi naturali coi modelli non si giudica ancora. Draxoksus resta non verificabile sulle caratteristiche: ha livelli di classe.
### Il generatore: Incantesimi focalizzati con la scuola (2026-11-17)

**Contesto.** Il generatore scriveva «Incantesimi focalizzati (bene, caos, legge o male)»: il lessico aveva preso per Spell Focus il nome del talento del *Libro delle Imprese Eroiche* che lo estende agli allineamenti (che il lessico ha già a parte, «Incantesimi Focalizzati (Bene)»). La scuola mancava sempre, e il talento finiva anche su mostri senza incantesimi, dove non fa niente. Il difetto l'ha trovato il thread Document AI.

**Decisione.**
- Il nome italiano di Spell Focus è «Incantesimi focalizzati» (`scripts/lessico_it_35.tsv`, `talenti.toml` rigenerato).
- `estrai_liste.py` legge dall'SRD 3.5 anche la scuola di ogni incantesimo (la riga sotto il titolo) e la scrive in `[scuole]` di `liste_incantesimi.toml`: 600 incantesimi, fuori «Universal» e «Any». Per i 45 incantesimi dell'APG che il generatore usa, la scuola viene dal PRD (`[scuole]` di `sistemi/pf1e/dati/incantesimi.toml`).
- `genera_creatura.py` dà a Incantesimi focalizzati e a Incantesimi focalizzati superiore la scuola con più incantesimi sul blocco; a parità vince la scuola dell'incantesimo di livello più alto, poi l'ordine alfabetico. Il conto lo scrive.
- Un blocco senza incantesimi non prende Incantesimi focalizzati: prende il talento seguente del suo ruolo, anche quando il carattere tirato era «Incantesimi Focalizzati». Lo ha scelto il DM sulla card del 2026-11-17 (la consigliata).
- Lo stesso vale per un blocco i cui incantesimi non hanno nessuno una scuola nelle tabelle (gli estratti dell'alchimista PF1e, come *spezzalinee*): il talento si scriverebbe senza scuola. L'ha notato la revisione di Codex; sui PNG PF1e a classi (945 generati, 21 classi) erano 44 talenti senza scuola su 665.

- Ricontrollo del 2026-11-18. Le liste di classe PF1e non avevano la scuola: 912 voci su 8548, e sui PNG a classi un incantesimo su sette restava fuori dal conto della scuola. Ora `estrai_prd_pf1e.py` scrive `[scuole]` anche in `sistemi/pf1e/dati/liste_incantesimi.toml`, per tutti i 1536 incantesimi delle liste (`spell_details.school` del PRD). Il generatore li riconosce col nome del PRD e col nome italiano. Sui 598 nomi che sono anche dell'SRD 3.5 la scuola è la stessa. I 5 incantesimi «universal» restano senza scuola da focalizzare. La nota «niente Incantesimi focalizzati» esce nel conto solo se l'esclusione ha cambiato la scelta (#470).

**Misura** sull'impronta delle creature (720 blocchi generati), contro main: nome sbagliato 234 → 0; Incantesimi focalizzati senza scuola 312 → 0, con la scuola 0 → 102; su blocchi senza incantesimi 210 → 0.

**Limiti dichiarati.** La scuola è quella degli incantesimi scelti, non una scelta di personaggio: il DM la cambia se vuole un mago specialista. La CD scritta nel blocco non aggiunge il +1 (o +2) sulla scuola. Gli altri talenti da incantatore (Incantare in combattimento, metamagia, Incantesimo Rapido) restano possibili su un mostro senza incantesimi: la card chiedeva solo di Incantesimi focalizzati. Nel PRD «thunderous drums» si chiama «Thundering Drums»: la scuola è presa da lì, il nome nei dati non è corretto in questa PR.

### Addendum 2026-11-19: le scelte storiche ricontrollate con una seconda fonte

**Contesto.** Il DM ha aperto all'ambiente dnd.arkalseif.info (D&D Tools: classi, talenti, incantesimi, domini e divinità dei manuali 3.5) e ha chiesto di ricontrollare con essa le scelte già fatte sulle schede, comprese quelle decise su card nelle settimane prima. È una fonte non OGL: nel repo entrano solo nomi, numeri e pagine, e nessun test di CI la legge.

**Decisione.** Una correzione che il sito decide da solo (una pagina citata sbagliata, una nota «non verificato» che ora ha risposta) si applica con la fonte accanto. Una correzione che lascia una scelta va su card, una alla volta, con la consigliata e le fonti per verificarla. Un dominio di chierico è legale se è nella lista del dio del Deities and Demigods o del FRCS; l'allineamento sta a un passo da quello del dio (SRD).

**Conseguenze.** Venti card risolte il 19/11 (elenco nella voce MS e nel registro della revisione). Due errori di conto trovati rifacendo gli slot sulla tabella SRD sono corretti con le card che li contenevano. `magia.py` conta lo slot di scuola dello specialista anche allo 0 nel 3.5 (SRD «per spell level»; nel PRD dal 1°), e `verifica_scheda.py` conta gli incantesimi bonus del Maestro del Sapere e legge il livello di classe, non il LI, per ranger e paladino. Misura contro main 517a3e79: violazioni 34 → 2.

**Limiti dichiarati.** Il sito copre poco il Monster Manual e il Magic Item Compendium, e per gli dei del Deities and Demigods non dà la lista dei Reami: quello che non copre resta non verificato, con il nome nella voce MS.

### Addendum 2026-11-25: le caratteristiche dentro una regola misurabile

**Contesto.** Il lotto «razze coi dadi vita razziali» ha misurato le caratteristiche di 64 schede contro le serie della DMG 3.5 (p. 110): 49 non combaciano. Le serie sono una scelta e non una regola, quindi lo scarto da solo non è una violazione.

**Decisione del DM (2026-11-20).** Una scheda passa se le sue caratteristiche, tolti razza, un aumento ogni 4 livelli o dadi vita, età, oggetti e ira, sono una di queste: il .pcg che la scheda cita, un acquisto a punti fino a 32, la serie normale, la serie d'élite. Chi non rientra va su card, scheda per scheda. Una scheda può restare fuori solo con una riga che lo dichiara come scelta del DM.

**Conseguenze.** Le bocciate scendono da 21 a 3, e nessuna delle tre è un difetto della scheda: lo script legge l'Orog Guardia Nera come orco e Zin'thara come elfa invece che drow, e Tempestas dichiara il suo acquisto a 60 punti. Grimjaw non è nella misura, perché la sua scheda sta in ARC08-02 e non nel Bestiario: entra dopo la #517. Il bonus razziale alle abilità delle creature coi dadi vita razziali entra nel conto voce per voce (`[razze_dv]` in `gradi.toml`). La scheda che cita un .pcg si confronta col .pcg più la razza.

**Limiti dichiarati.** La regola non è un cancello: la misura sta in `/mnt/project-files/regole-razze-dv-2026-11-20/misura_regola_jfs.py`, fuori dal repo. Il verificatore non conosce l'orog e lo tratta come orco. Gli oggetti di caratteristica si leggono dal testo della scheda.

**Dopo la verifica (2026-11-26).** La PR #521 era stata dichiarata pronta con la sola CI. Regolista e custode del canone, in sola lettura, hanno trovato errori che `verifica_scheda.py` non vede: sulle 13 schede dava 0 violazioni. Cambiate le caratteristiche, i derivati non erano stati ricalcolati tutti (Tempra e frusta della sacerdotessa drow, Saltare di Dauth, la CD del Pugno Stordente di Maewen), e le copie in prosa di ARC-08 e dell'arco 09 portavano ancora i numeri vecchi dell'Orog Guardia Nera e del comandante di Dauth. Altri errori c'erano già su main, nel trickster arcano, nella guardia nobile e in Bothor. Il DM ha scelto su card di correggerli tutti nella stessa PR; l'elenco sta in MS-0227.

Il verificatore è cieco su tiri salvezza, attacchi, CD, abilità con penalità di armatura e di velocità, e su ogni copia in prosa di una scheda. Per questo una PR di schede si dichiara pronta solo dopo il passaggio di regolista e custode del canone: la CI verde dice che le voci contate tornano, e niente sulle altre. I rilievi di Codex hanno poi corretto il verificatore stesso: la taglia entra nel conto di Nascondersi delle creature coi dadi vita razziali, e un oggetto che il .pcg tiene solo «Carried» non dà il suo bonus. Resta aperto, e chiede una card perché è canone, il tesoro della tenda di Balvar in ARC07-DEF-4, che non conta i suoi cinque oggetti +2.
