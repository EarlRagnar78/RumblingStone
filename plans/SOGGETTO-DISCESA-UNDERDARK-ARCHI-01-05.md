# SOGGETTO — LA DISCESA NELL'UNDERDARK (archi 01-05, + i due pre-archi)

> 📦 **Documento datato, recuperato il 2026-09-24 dalla PR #72** (mai mergiata;
> revisione 6, commit `f5972c4`, 2026-07-26), per la decisione D22 di
> `PIANO-RIPRESA-PR-ABBANDONATE`. Nessun documento su `main` lo nominava.
>
> **Stato oggi.** Ogni domanda di §3, §7 e §9.4 ha una risposta del DM (§9 e
> §10, revisioni 3-6). Il canone che ne esce è già in
> `campaign/lore/campaign-chronicle.md`: 133 righe su 133, integrate dal commit
> `960c621` della stessa PR e divise dallo storico nel lotto 4f-2. Restano due
> conferme, che sono la D24 di quel piano: la **destinazione della fuga del
> Collezionista** (§10.3: il DM aveva delegato la scelta, e nella cronaca è
> ancora `[INFERRED]`) e il **GS di Maur** (11 qui e nel registro XP, ~10 nella
> cronaca).
>
> **Rimandi aggiornati**: `campaign-history.md` è diventato
> `campaign-chronicle.md`; l'ADR-0018 della #72 è l'ADR-0049; l'audit di
> derivazione IP è quello rifatto il 2026-09-11. Gli archi 01, 02, 03 e 05 hanno
> ancora zero file markdown (misurato il 2026-09-24): la raccomandazione di §11,
> scrivere per primo il mercato drow di Sonjak, resta valida e non ha un piano.

> **Cos'è**: il consolidamento in un solo posto della catena narrativa che va dai
> portali/nodi terrestri fino alla Stanza della Corona di Adamantio. Oggi quella
> catena **esiste in tre posti diversi e in nessuno per intero**: nella memoria
> del DM, in `campaign/lore/campaign-chronicle.md` (scheletro), e come materiale
> grezzo non consolidato nelle cartelle degli archi.
>
> **Perché adesso**: gli archi 01, 02, 03, 05 **non hanno un solo file markdown**
> — solo `.txt`, `.pdf`, `.webp`. È la parte più a rischio del repo: se si perde,
> si perde dalla testa del DM, non da un file.
>
> **Cosa NON è**: non è un master DEF. È il **soggetto** da cui i master si
> scrivono, secondo `skills/rumblingstone-module-standard`. La prosa segue in un
> secondo momento, con `rumblingstone-narrative-style`.
>
> **Fonte primaria**: racconto del DM del 2026-07-26, incrociato con
> `campaign/lore/campaign-chronicle.md`, con l'inventario del materiale grezzo e —
> **rev. 2** — con il **registro XP incontro-per-incontro** estratto da
> `00_Red Hand Of Doom/CalcoloPuntiEperienza-current.ods` (§6).
> **Data**: 2026-07-26 · **Stato**: 🟡 bozza da validare dal DM
>
> **Rev. 2**: il registro XP ha **sciolto 4 delle 6 domande** di §3 e ne ha
> aperte 2 nuove. Ha anche isolato il problema vero: §7.
> **Rev. 3** (risposte DM, 2026-07-26 sera): il Giardino ha un nome e una fonte,
> la fusione di Hella ha una meccanica, i tre mostri sono confermati. §9 elenca
> ciò che resta aperto.
> **Rev. 4**: il mercato drow di Sonjak è documentato (§1.4) — merci, luogo,
> la scala sorvegliata da invisibili. Apre una contraddizione di ordine.
> **Rev. 5** (risposte DM): **la catena è chiusa**. Ordine risolto, costo di
> Hella risolto, Zuggtmoy canone, viaggio iniziale, fuga del Collezionista,
> Sonjak, portale. Vedi §10 — resta **un solo** punto aperto.

---

## 0. Come leggere questo documento

- ✅ = attestato in `campaign-history.md` o nel materiale grezzo
- 🗣 = raccontato dal DM il 2026-07-26, **non ancora scritto in nessun file**
- ⚠️ = **da chiarire**: contraddizione o ambiguità che serve sciogliere prima di
  scrivere. **Non l'ho risolta al posto tuo** — sono scelte di canone.

---

## 1. La catena, nell'ordine raccontato dal DM

### 1.0 — Il viaggio 🗣

Attraverso **portali e nodi terrestri**, il gruppo arriva nell'Underdark.

> ⚠️ **Da chiarire**: «nodo terrestre» compare in **20 file** del repo, ma sempre
> come riferimento a valle. Il viaggio in sé non è descritto da nessuna parte:
> quanti salti, chi apre i portali, cosa costa. È il primo pezzo mancante.

### 1.1 — La Tana dei Minotauri *(Pre-Arco 01)* ✅🗣

Una tribù di **minotauri** tiene i **miconidi in schiavitù**.

- **Maur** — creatura nativa dell'Underdark, CR ~10, sconfitta ✅
  *(fonte dichiarata: `Underdark` p.95)*
- **IL COLLEZIONISTA — prima apparizione** ✅ — un **rakshasa** che usa un
  **basilisco vincolato** per pietrificare i nemici e ne **vende le statue** a
  clienti malvagi come trofei. **FUGGE.** Diventa il villain ricorrente
- Più tardi si allea con la fazione drow, fornendo artefatti malvagi ✅

> ⚠️ **Da chiarire**: hai detto *«il loro capo è un mostro score + basilico e il
> rakshasa che vende le statue»*. La storia di campagna attribuisce il basilisco
> **al Collezionista** (rakshasa + basilisco vincolato). Quindi «score» è:
> (a) Maur? (b) un capo minotauro distinto, ancora senza nome? (c) un refuso?
> **Sono tre soggetti diversi in scena e va deciso quanti sono.**

### 1.2 — Il Giardino dei Miceni e la Madre dei Funghi 🗣

I miconidi accolgono il gruppo. Nel **Giardino**, **Hella si fonde con i poteri
fungini**, e la **Madre dei Funghi** teletrasporta la compagnia.

> ⚠️ **Da chiarire (due cose, entrambe pesanti)**
> 1. Hai scritto «l'amore dei funghi»; poco prima «la madre dei funghi». Assumo
>    **la Madre dei Funghi** (attestata in 6 file). Confermare.
> 2. **La fusione di Hella è un beat maggiore e non è scritta da nessuna parte.**
>    È il precedente diretto della sua morte all'arco 06 e della sua
>    resurrezione all'arco 07: cosa cede, cosa ottiene, e se il legame resta.

> ⚠️ **IP**: `campaign-history.md` dichiara la torre fungina «**Adapted from
> *Out of the Abyss* (D&D 5e) Neverlight Grove**». Vedi §4.

### 1.3 — Dopo il teletrasporto 🗣

Il gruppo si ritrova **vicino alla destinazione**. Esplorando, incontra **mostri
che attraversano la pietra come se ci nuotassero**.

> ⚠️ **Da chiarire**: sono **xorn** (materiale in `04_tomba_di_Belkram/`: `xorn
> talent.txt`, `xorn.webp`, `Xcorn.webp`) o i **Cristal Warriors** (`Underdark`
> p.93, che la storia colloca nell'**arco 01**)? Sono due creature diverse e
> cambiano il tono della scena.

### 1.4 — Il bivio, la scala sorvegliata e il mercato drow 🗣 *(rev. 4)*

**Il luogo.** Un **bivio** nell'Underdark, **lungo la strada per la Tana dei
Minotauri**. Da lì si scende.

**La scala.** Ripida, lunga, scavata nella roccia — il DM la immagina come *la
scala che i nani salgono per trovare la porta segreta della Montagna Solitaria*.
⚠️ **Immagine di regia, non testo**: il riferimento serve a te per trovare il
tono, **non va scritto nel modulo** (vedi §4-bis).

**La scala non è sguarnita.** Ed è qui che la scena funziona:

- **drow invisibili** la sorvegliano lungo tutta la discesa;
- **ragni invisibili** stanno **sopra**, appesi alla volta;
- **solo Artemis li vede**, usando i suoi poteri — e li usa per **frenare la
  spavalderia del gruppo**.

> **Questo è il cuore della scena e va progettato, non raccontato.** Il gruppo
> scende disarmato di conoscenza; un solo PG sa che sono osservati da decine di
> occhi, e deve convincere gli altri a comportarsi. Il pericolo non è il
> combattimento: è il **passo falso**. Chi sguaina, muore — e nessuno lo sa
> tranne uno.

**Il mercato.** In fondo la scala si apre in una **grotta ampia con tre tende**.
Si vende:

| Merce | Nota del DM |
|---|---|
| **Pozioni** | a prezzo da strozzino |
| **Armi** | «prezzi proibitivi» |
| **Schiavi** | ovviamente |

È un gruppo sotto la matrona **Sonjak**. Non attaccano: **commerciano**.

**Perché è la scena migliore del materiale**: un incontro drow che non è un
combattimento, in cui la tensione viene dal *prezzo* e dall'essere sorvegliati.
E offre ai PG la scelta che nessun combattimento offre — **comprare schiavi, o
no**, sapendo che il denaro finisce a Sonjak.

> ⚠️ **CONTRADDIZIONE DI ORDINE — da sciogliere.**
> Nel primo racconto (2026-07-26) l'accampamento drow veniva **dopo** il
> teletrasporto della Madre dei Funghi, in una zona esplorata più tardi.
> In questa risposta l'accampamento è **a un bivio lungo la strada PER la Tana
> dei Minotauri** — cioè **prima**.
> Le possibilità sono tre: (a) l'ordine corretto è questo e il primo racconto
> comprimeva due momenti; (b) i campi drow sono **due**, uno prima e uno dopo;
> (c) il gruppo ci è passato **due volte**, all'andata e al ritorno — che sarebbe
> la versione migliore, perché la seconda visita cambia di segno dopo la torre.
> **Serve la tua parola.**

### 1.5 — L'accampamento dei funghi e le aberrazioni fungine 🗣✅

Esplorando, il gruppo trova **drow modificati dai funghi** in una sorta di
**aberrazione fungina**. ✅ *(la storia parla di «drow-modified creatures» e di
un «drow-modified myconid research lab»)*

### 1.6 — La torre fungina 🗣✅

Il gruppo entra nella **torre fungina** per parlare con la Madre dei Funghi. Ma
la torre è stata **modificata dai drow di Sonjak nella struttura *e nello
spazio***. Il gruppo **distrugge la compagnia drow**.

> **Il dettaglio da non perdere**: *Sonjak è un'architetto*. Non modifica solo
> gli edifici: modifica **lo spazio**. È il tratto che la distingue da qualunque
> altra matrona drow, ed è già canone (`campaign-history.md` la chiama «drow
> architect»). La torre è la sua prima dimostrazione — e va **giocata**, non
> raccontata: corridoi che non tornano, distanze che non corrispondono.

### 1.7 — Il portale a senso unico 🗣

Inseguendo pattuglie drow, il gruppo attraversa un **portale a senso unico** e
si ritrova **vicino alla miniera**.

> ⚠️ **Da chiarire — ordine degli archi.** Il tuo racconto mette **la miniera
> DOPO** la torre fungina. La numerazione delle cartelle e `campaign-history.md`
> mettono **01 = La Miniera** *prima* di 02 (scala d'ossa/funghi). La storia
> modella già due «pre-archi» non numerati (Tana dei Minotauri = Pre-Arco 01,
> Neverlight Grove = Pre-Arco 02), ma **non nell'ordine che hai raccontato**.
> **Va deciso**: la numerazione delle cartelle riflette l'ordine di gioco reale,
> oppure no?

### 1.8 — La Miniera ✅

Antica miniera nanica. **Tana del Grell Necromante**, **Grell Patriarca**
(aberrazione, sconfitto). **Cristal Warriors** nelle prime sale dopo l'arrivo
dal portale. ✅
*Materiale grezzo*: `grell necromante.txt`, `grellPatriarca.txt`, `Miniera.txt`,
`Miniera-ita.txt`.

### 1.9 — Scala d'Ossa ✅

Nani malvagi di **Abaddor**, un necromante. Sconfitto il necromante, il gruppo
trova l'**Anello dell'Illuminazione Caotica**, che si lega ad **Artemis**. ✅
*Materiale grezzo*: `00_nani_dwergar_abaddor_scala_di_ossa.txt`,
`Epic_fight_dwarf_duergar.txt`, `Fight_fungi_colony.txt`.

> ⚠️ **Da chiarire**: «Abaddor» è il nome del necromante, del clan, o del luogo?
> Compare solo in un nome di file.

### 1.10 — La Cittadella nanica ✅🗣

In fondo alla miniera, una **Cittadella nanica devastata da nani grigi
(duergar) e drow**. 🗣

- **Affreschi runici** con indizi sulla Corona di Adamantio ✅
- Lore dell'antico regno nanico ✅
- **Drow schiavisti** e il loro capo, uno stregone drow, anch'essi in cerca
  della Corona, che comandano un **retriever** (sconfitto) ✅

### 1.11 — Il Tempio ✅

**Tempio di Moradin**, con un **beholder non-morto** (Death Tyrant, CR ~13,
sconfitto). ✅
*Materiale grezzo*: `Il Tempio di Moradin.webp`, `Tempio Nanico.txt`,
`temple-map-revised.svg` *(esiste già una mappa!)*, `Il Guardiano Beholder.html`,
`Beholder-zombie-hal-illithid-cr13.odt`.

### 1.12 — La Tomba di Belkram ✅

Xorn, cubi gelatinosi, torrette di gargoyle. **Incontro con il verme illithid** →
Artemis subisce la **crisi di cerebromorfosi**. Prima grande attivazione
dell'Anello — *Sfida dell'Alba* salva Artemis. **Artemis RIFIUTA la classe di
prestigio Signore del Sole e dell'Ombra** offerta da Lathander e Mask, scegliendo
di restare warlock e forgiare la propria via caotica. ✅

### 1.13 — La Stanza Runica ✅

Sala enigma runica nanica. *Materiale grezzo*: `stanzaRunica.pdf`, `La Gemma
dell'Antico Portatore — riferimento rapido.pdf`.
**È la sezione più povera di tutte**: solo due PDF, nessuna nota.

### 1.14 — La Stanza della Corona di Adamantio ✅

Boss battle. **Thorik supera la prova e indossa la Corona.**
**Hella Oakenshield MUORE.** ✅

---

## 2. Cosa esiste, cosa manca

| Arco | File markdown | Materiale grezzo | Stato |
|---|---:|---|---|
| 01 La Miniera | **0** | 4 `.txt` | 🔴 da scrivere |
| 02 Scala d'Ossa / Funghi | **0** | 4 `.txt` + 4 `.webp` | 🔴 da scrivere |
| 03 La Cittadella + Tempio | **0** | 29 file (`.txt`, `.pdf`, `.webp`, `.html`, **1 `.svg`**) | 🔴 da scrivere — **il più ricco di materiale** |
| 04 Tomba di Belkram | 2 (solo cerebromorfosi) | 19 file | 🟡 parziale |
| 05 Stanza Runica | **0** | 2 `.pdf` | 🔴 **il più povero** |
| Pre-archi (Minotauri, Torre fungina) | 0 | — | 🔴 solo scheletro nella storia |

**Nessuno di questi archi ha una mappa tattica renderizzata**, con l'eccezione
del `temple-map-revised.svg` dell'arco 03 — che è però un artefatto sciolto,
fuori dalla pipeline.

---

## 3. Le sei domande da sciogliere prima di scrivere

Raccolte da §1. Sono decisioni di canone, non di forma:

1. **Ordine reale**: la miniera viene prima o dopo la torre fungina?
2. **Il capo dei minotauri**: «score» è Maur, un terzo soggetto, o un refuso?
3. **La Madre dei Funghi**: confermare il nome.
4. **La fusione di Hella**: cosa cede, cosa ottiene, il legame resta?
5. **I nuotatori nella pietra**: xorn o Cristal Warriors?
6. **Abaddor**: persona, clan o luogo?

---

## 4. ⚠️ Nota IP — e perché queste pagine bianche sono un'occasione

`campaign/lore/campaign-chronicle.md` dichiara che questa catena adatta **tre
manuali di terzi**, con numero di pagina:

| Sezione | Fonte dichiarata |
|---|---|
| Tana dei Minotauri | *Expedition to Undermountain* p.165 · *Underdark* |
| Torre fungina / Giardino | ***Out of the Abyss*** (5e) — Neverlight Grove |
| Scala d'Ossa (02) | *Expedition to Undermountain* p.123 |
| Cittadella + Tempio (03) | *Expedition to Undermountain* p.122 e p.140 |
| Tomba di Belkram (04) | *Expedition to Undermountain* p.117 |

Il nome stesso — **Belkram** — è una località di Undermountain (*Belkram's
Fall*), e compare **232 volte in 49 file**.

**Ma questi archi non sono scritti.** Non c'è un testo da bonificare: c'è un
testo da **scrivere**. E scrivere una sala runica nanica originale costa
esattamente quanto scriverne una derivata.

> **È il punto in cui diventare originali è gratis** — l'unico del repo. Vale la
> pena spenderlo bene: vedi [ADR-0049](adr/ADR-0049-edizione-commerciale-ap-originale.md) (era l'ADR-0018 della #72)
> e [`docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md`](../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md) (§6-bis dell'audit originale della #72, mai arrivato; quello rifatto misura la derivazione per arco in §2).

Il materiale genuinamente tuo in questa catena è già molto: **Il Collezionista**
e il suo commercio di statue, **Sonjak architetto che piega lo spazio**, la
**fusione di Hella coi funghi**, il **rifiuto della classe di prestigio da parte
di Artemis**, la **Corona** e la **morte di Hella**. Nessuna di queste cose viene
da un manuale.

---

## 4-bis. Riferimenti di regia — utili a te, vietati sulla pagina

Alcune immagini che il DM usa per fissare il tono vengono da opere protette.
**Servono in fase di scrittura, non vanno nel testo.**

| Immagine di regia | Dove | Regola |
|---|---|---|
| «la scala per l'entrata della Montagna Solitaria» (*Lo Hobbit*) | §1.4, la discesa al mercato drow | usare la **sensazione** — scala lunga, esposta, che porta a una porta che non si vede finché non sei arrivato. Mai il nome |

Vale la stessa regola dei prompt immagine (lotto D4 del piano level design): il
riferimento aiuta a **dirigere**, e sparisce dal prodotto.

---

## 5. Prossimo passo proposto

Scrivere **un arco solo, per intero**, come implementazione di riferimento —
proposta: **arco 03 (Cittadella + Tempio di Moradin)**, perché ha 29 file di
materiale grezzo e già una mappa. Da lì si tara il ritmo e si scrivono gli altri
quattro allo stesso standard (`rumblingstone-module-standard`).

**Prima però servono le sei risposte di §3.**


---

## 6. Il registro XP — la spina dorsale che mancava

`00_Red Hand Of Doom/CalcoloPuntiEperienza-current.ods`, foglio **«Calcolo PX»**,
**98 righe**: un incontro per riga, in ordine cronologico, con i PX assegnati a
ciascun PG. *(La versione precedente, `CalcoloPuntiEperiennza.ods`, ne ha 78: è
un sottoinsieme. Usare la `-current`.)*

**È il documento più prezioso del repo per questi archi**, e non è mai stato letto
da nessuno strumento: è un foglio di calcolo, non markdown.

### 6.1 Dati di inquadramento

| | |
|---|---|
| PX iniziali | **28.000** = **8° livello** — conferma la riscalatura |
| Livelli attuali | 13° (Thorik 81.130 · Tordek 82.946 · Artemis 78.495 · Hella 78.217) |
| **Jorr** | **5° personaggio, 8° livello, 30.685 PX** — presente in tutta la prima metà |
| Copertura del registro | dalla superficie RHoD fino a **«Duergar Ambush sul ponte»**. **Non arriva alla Corona.** |

### 6.2 La sequenza reale, dalla riga dell'Underdark in poi

```
Underdark 20 scarafaggi giganti          ← ingresso nell'Underdark
2 orrori uncinati cr6 + 4 gnoll
trappole (caduta massi cr5, veleno cr7)
protoplasma nero cr6
Minotauri 5 cr5 4 cr4 AL PORTO
Minotauri 5 cr5 1 cr6 ALLA MINIERA
★ Il capo dei minotauri MAUR cr11 + una GORGONE cr8 + un RAKASA (il Collezionista)
topi che parlano (creature demoniache torturate dai drow) cr10
★ il ciambellano miconide DEMONIACO cr7 + 2 protoplasmi neri cr7
trappola gas e acido con i cadaveri con la MALEDIZIONE DI YUGGTMOY
5 grick + 1 grell filosofo
15 trappole acido gr2 PER SALIRE AL 2° E AL 3° PIANO   ← la torre fungina
1 sporebat
10 trappole spore e ragnatele gr3 PER SALIRE AL 4° PIANO
cubo gelatinoso cr5 → Artemis TS Tempra CD 14 o torna a metà fra 8° e 9°
1 chwidencha · 2 guardie drow · pattuglia drow · sacerdotessa drow cr6 …
thiefling stregone accolito della pelle cr8 · statue barbute con risucchio
★ vrock MINERAL WARRIOR cr10
★ «trovano la frase per chiudere le porte della MINIERA DI BELKAM»
golem di cristallo cr11 · una decina di trappole
4 knight di ABBATHOR e non-morti evocati
★ incontro con MICONIDI: 2 guardie élite, 2 guardie, 6 worker
★ chierico di ABBATHOR duergar cr12 + cavalieri duergar     ← i nani grigi
direguard · defacer · vansoud · Ettin a tre teste (contro Thorik nel sonno)
★ RETRIEVER contro gli altri mentre Thorik dormiva
★ orrore della palude + ragno fase + guardie casato drow    ← shadow marsh
3 round di ragni e phase spider
★ warlock cr9 + 3 wraith + BEHOLDER ZOMBIE TYRANT cr13      ← il Tempio
2 drow cr9 + 2 carnevus demons · stanza torrette goblin
★ 1 mostro a 3 gambe — un ELDER XORN
★ STANZA DELLA RINASCITA + 4 grimlock CELEBROMORFI cr5 + drow
cubo gelatinoso cr8
★ LA QUEST DELLA GEMMA DELL'ANTICO PORTATORE — piano spirituale (5.800 PX!)
★ Belkram, worg e le tre yoch
★ Duergar Ambush sul ponte                                   ← il registro finisce qui
```

### 6.3 Cosa combacia col tuo racconto

**Quasi tutto, e nell'ordine che hai detto.** Minotauri → miconidi/torre →
drow → miniera → duergar → tempio → xorn → rinascita → gemma → Belkram.

Un solo scarto strutturale: la miniera è **«la miniera di Belkam»** — miniera e
tomba di Belkram sono **lo stesso complesso**, non due luoghi. Il tuo racconto le
teneva separate.

---

## 6-bis. Le quattro domande che il registro ha sciolto

| # | Domanda | Risposta dal registro |
|---|---|---|
| **2** | «un mostro score + basilico» | **`Il capo dei minotauri maur cr 11 una GORGONE cr 8 un RAKASA (il Collezionista)`** — sono **tre** creature: Maur è il capo minotauro, la **gorgone** è il mostro pietrificante, il rakshasa è il Collezionista. «score» = **gorgone** |
| **5** | i nuotatori nella pietra | **`1 mostro 3 gambe — un ELDER XORN`**. (E c'è anche un **vrock mineral warrior**) |
| **6** | «Abaddor» | **ABBATHOR** — la divinità nanica dell'avidità. Non una persona, non un clan: un **dio**. Già in 17 file `.md` del repo |
| **1** | ordine miniera / torre fungina | **il tuo racconto è giusto**: minotauri → torre fungina → drow → miniera. La numerazione delle cartelle **non** riflette l'ordine di gioco |

### ⚠️ Due contraddizioni nuove, da sciogliere

1. **Gorgone o basilisco?** Il registro (il *giocato*) dice **gorgone cr 8**.
   `campaign-history.md` dice che il Collezionista usa un **basilisco vincolato**.
   In 3.5 sono due mostri diversi — entrambi pietrificano, quindi entrambi
   reggono il commercio di statue, ma **non sono la stessa creatura**.
   Quale vale come canone?
2. **Zuggtmoy.** Il registro cita la *«maledizione di **yuggtmoy**»* sui cadaveri
   nella torre. **Zuggtmoy compare in ZERO file markdown del repo**: esiste solo
   in questo foglio di calcolo. È la regina demoniaca dei funghi — e spiega
   *perché* i miconidi sono «crazed» e il ciambellano è «demoniaco». **È il
   tassello che tiene insieme tutta la sezione fungina, e non è scritto da
   nessuna parte.** ⚠️ È anche Product Identity WotC (vedi §4).

---

## 7. Il problema vero: cosa NON ha lasciato traccia

Il registro assegna PX per **combattimenti e trappole**. Tutto il resto non
compare — e «tutto il resto» è esattamente ciò che ricordi come **la storia**:

| Beat del tuo racconto | Nel registro | Altrove |
|---|---|---|
| Viaggio per portali e **nodi terrestri** | ❌ | ❌ |
| **Giardino dei Miceni** | ❌ | ❌ |
| **Hella si fonde coi poteri fungini** | ❌ | ❌ |
| **La Madre dei Funghi li teletrasporta** | ❌ | ❌ |
| **Accampamento drow che commercia** invece di attaccare | ❌ | ❌ |
| Drow **modificati dai funghi** | ❌ | parziale in `campaign-history` |
| Torre modificata **nello spazio** da Sonjak | ❌ | ❌ |
| **Sonjak** in persona | ❌ | citata a valle, mai in scena qui |
| **Portale a senso unico** | ❌ | ❌ |

> **Il registro conserva ciò che ha dato PX. La storia non dà PX.**

Ecco perché «mancano le parti descrittive»: non è che siano andate perse — **non
sono mai state scritte**, perché il sistema di tracciamento che avevi (il foglio
XP) non aveva un posto dove metterle. La spina dei combattimenti è documentata al
100%; il tessuto connettivo esiste solo nella tua memoria.

**Le due domande che restano aperte, ed è dove serve la tua testa:**

- **la fusione di Hella** — cosa cede, cosa ottiene, il legame resta? È il
  precedente diretto della sua morte all'arco 06 e della resurrezione all'arco 07;
- **cosa vendono i drow di Sonjak, e a che prezzo** — è la scena migliore di
  tutto il materiale, ed è quella di cui non resta una riga.

---

## 8. Conseguenza operativa

Il registro XP va **promosso da foglio di calcolo a dato**: 98 incontri con GS,
composizione e PX sono già la metà di ogni master d'arco (la sezione «Incontri»
si compila da lì, non a memoria). Oggi nessuno strumento del repo lo legge.

Ordine di scrittura rivisto rispetto a §5:

1. **estrarre il registro in markdown** — è meccanico e sblocca tutto il resto;
2. rispondere alle **due** domande di §7 (Hella, i drow) e alle **due**
   contraddizioni di §6-bis (gorgone/basilisco, Zuggtmoy);
3. scrivere l'**arco 03** per intero come riferimento — ha 29 file di materiale,
   una mappa SVG, e nel registro il beholder zombie tyrant cr13, i duergar di
   Abbathor, il retriever e l'ettin.


---

## 9. Risposte del DM (rev. 3) e cosa resta aperto

### 9.1 Il Giardino ha un nome — ed è una **quinta fonte WotC**

> *«dopo il lair dei minotauri i giocatori hanno scoperto grazie ad Hella e ai
> funghi il **Gardens of Resplendent Hues** (Drow of the Underdark p.189)»*

**Nuovo dato, e nuovo problema.** ⚠️ *Drow of the Underdark* (WotC 2007) è la
**quinta** fonte di terzi dichiarata per questa catena, dopo *Expedition to
Undermountain*, *Underdark*, *Out of the Abyss* e la lore FR.

Verificato: **«Gardens of Resplendent Hues» compare in ZERO file markdown** del
repo. Come Zuggtmoy, esisteva solo nella memoria del DM.

### 9.2 La fusione di Hella — **meccanica confermata**

> *«Hella ha superato le prove e ha acquisito la possibilità di viaggiare il
> micelio portando con sé gli altri PG, che hanno dovuto superare un TS sulla
> Tempra CD 17 per non restare nauseati (Artemis l'ha fallito)»*

| | |
|---|---|
| Cosa ottiene Hella | **viaggio attraverso il micelio**, con la compagnia al seguito |
| Costo per gli altri | **TS Tempra CD 17** o **nauseati** |
| Esito reale al tavolo | **Artemis fallisce** |
| Attestazione | ⚠️ **«micelio» e «mycelium»: 0 file markdown.** Nulla di tutto questo è scritto |

⚠️ **Da non confondere**: il registro XP ha un *altro* TS di Artemis — `Cubo
gelatinoso cr5 → Artemis se non supera il TS Tempra **CD 14** torna a metà fra 8°
e 9° livello`. Sono **due tiri diversi in due scene diverse**: CD 17 nausea al
Giardino, CD 14 perdita di livello al cubo. Nel master vanno tenuti separati.

### 9.3 I tre mostri della Tana — confermati

> *«poi i mostri sono **maur**, **basilisk** e **rachasa**»*

Confermato l'assetto a tre. **Ma resta una discrepanza da dirimere**: il registro
XP — cioè il *giocato* — scrive `Il capo dei minotauri maur cr 11 una **GORGONE**
cr 8 un rakasa (il Collezionista)`. Il DM dice **basilisco**, coerente con
`campaign-history.md` («bonded basilisk»).

**Due fonti su tre dicono basilisco, il foglio dice gorgone.** Il DM è l'arbitro,
ma la scelta va scritta una volta e propagata: 2 contro 1 → **basilisco**, salvo
smentita.

---

### 9.4 ⚠️ COSA RESTA APERTO

Sciolte: il nome del Giardino, la meccanica di Hella, i tre mostri, l'ordine,
Abbathor, lo xorn. **Restano nove cose**, in ordine di quanto pesano:

| # | Aperto | Perché pesa |
|---|---|---|
| ~~1~~ | ~~Cosa vendono i drow di Sonjak~~ | ✅ **RISPOSTO (rev. 4)**: pozioni, armi a prezzi proibitivi, schiavi; a un bivio sulla strada per la Tana; scala ripida sorvegliata da drow e ragni **invisibili**, visti dal solo Artemis; grotta finale con **tre tende**. Vedi §1.4 |
| **1-bis** | ⚠️ **L'accampamento drow viene PRIMA o DOPO la Tana dei Minotauri?** | Nuova contraddizione fra i due racconti. Tre ipotesi in §1.4 — la migliore è che ci siano passati **due volte** |
| **2** | **Cosa è costato a Hella** | Ha *ottenuto* il micelio. Non sappiamo cosa ha **ceduto**. È il precedente diretto della sua morte (arco 06) e della resurrezione (arco 07): senza il costo, quei due beat perdono la radice |
| **3** | **Il viaggio del micelio è permanente?** | Se Hella lo conserva, cambia la logistica di tutti gli archi successivi. Se lo perde, quando e come |
| **4** | **Chi somministra «le prove»** | La Madre dei Funghi? Il ciambellano miconide (che il registro dice **demoniaco**)? Sono due scene molto diverse |
| **5** | **Zuggtmoy è canone?** | Il registro cita la «maledizione di yuggtmoy». Spiega perché i miconidi sono impazziti e il ciambellano è demoniaco — cioè tiene insieme tutta la sezione fungina. **0 file markdown** |
| **6** | **Il viaggio iniziale** per portali e nodi terrestri | Precede tutto e non esiste da nessuna parte: quanti salti, chi apre, cosa costa |
| **7** | **Come fugge il Collezionista** | Fugge — ma come, e porta via qualcosa? È la prima apparizione del villain ricorrente: la sua uscita di scena è la sua presentazione |
| **8** | **Sonjak entra mai in scena qui?** | O si vede solo la sua *opera* (la torre piegata)? Un villain che non si mostra mai è una scelta forte, ma va decisa |
| **9** | **Il portale a senso unico** | Dove sbuca esattamente, ed è ancora lì? |

E una conseguenza pratica del punto 9.2: **Artemis fallisce due tiri in questa
catena** (nausea CD 17, livello CD 14). Se al tavolo la nausea ha avuto effetti
giocati — round persi, una scena mancata — vale la pena scriverli: è il tipo di
dettaglio che rende un master credibile invece che generico.


---

## 10. La catena completa (rev. 5) — canone dichiarato dal DM

Con queste risposte **la spina narrativa è chiusa**. Ordine definitivo:

```
① HAMMERFIST — stanza privata
     chierici e druidi di Moradin aprono la connessione
     attraverso un NODO DELLA TERRA
                    ↓
② ZONA DEI FUNGHI — sotto attacco dei minotauri
     l'attacco in corso È l'aggancio: fa scattare la quest
                    ↓
③ IL BIVIO E IL MERCATO DROW  (§1.4)
     scala ripida · drow e ragni INVISIBILI · 3 tende
     pozioni, armi, schiavi — a prezzo da strozzino
                    ↓
④ TANA DEI MINOTAURI
     Maur (capo, cr11) · basilisco · rakshasa = IL COLLEZIONISTA
     → il Collezionista FUGGE (vedi §10.3)
                    ↓
⑤ GARDENS OF RESPLENDENT HUES — le prove
     Hella le supera → VIAGGIO NEL MICELIO, compagnia al seguito
     TS Tempra CD 17 o nauseati — ARTEMIS FALLISCE
     ⚠️ le prove NON sono un premio: sono il MEZZO. Senza,
        il gruppo non saprebbe come raggiungere la torre
                    ↓
⑥ TORRE FUNGINA — il regno di ZUGGTMOY (canone)
     Sonjak l'ha modificata nella struttura E NELLO SPAZIO,
     per ACCORDO CON ZUGGTMOY, a beneficio dei suoi
     esperimenti di aberrazione
     Zuggtmoy sa dove si trova l'antica miniera nanica
                    ↓
⑦ PORTALE A SENSO UNICO (dentro la torre)
     ci sbucano i drow in fuga E i PG
                    ↓
⑧ ZONA DELLA MINIERA — il MOSTRO CRISTALLINO
                    ↓
⑨ … miniera → Scala d'Ossa → Cittadella → Tempio → Belkram
                    ↓
⑩ STANZA RUNICA
     i PG BRUCIANO I FUNGHI → IRA FUNGINA
     → Hella PERDE il potere del micelio
                    ↓
⑪ CORONA DI ADAMANTIO — Thorik la indossa · Hella muore
```

### 10.1 Il costo di Hella: **non l'ha pagato lei, l'ha pagato il gruppo**

> *«non ha ceduto nulla, ma nella stanza runica ha perso il potere concesso
> perché i PG hanno bruciato i funghi presenti provocando l'ira fungina»*

**Questa è la risposta migliore che potevi darmi, ed è meglio di qualunque prezzo
pattuito.** Il dono non aveva un costo: aveva una **condizione**, e il gruppo l'ha
violata senza sapere che esistesse.

Conseguenze da scrivere:

- si apre all'arco 02 (le prove) e si chiude all'arco 05 (i funghi bruciati):
  **è un arco lungo tre sessioni**, non una scena;
- il colpevole è **il gruppo**, non un nemico. Hella paga per una decisione
  altrui, e questo la lega e la isola insieme;
- il precedente per la sua morte all'arco 06 è **narrativo, non meccanico**:
  arriva alla Corona **già spogliata** di ciò che l'aveva resa la guida della
  discesa;
- ⚠️ **da decidere**: i PG hanno mai saputo perché il potere è sparito? Se non
  l'hanno collegato, è ancora un debito aperto al tavolo.

### 10.2 Sonjak non appare mai — ed è la scelta giusta

> *«si vedono solo le sue opere, non l'hanno mai incontrata. Il bello è quello.»*

Confermato come **scelta di regia deliberata**. E il patto con Zuggtmoy le dà una
motivazione che non è la solita malvagità drow: ha **modificato la torre in
cambio del permesso di sperimentare**. La torre piegata nello spazio non è
un dungeon: è il **laboratorio pagato con un accordo**.

Regola per chi scriverà: di Sonjak si mostrano **l'opera, la firma e il
prezzo** — mai il volto. La prima volta che comparirà di persona varrà il doppio.

### 10.3 La fuga del Collezionista — **raccomandazione motivata**

Il DM ha chiesto di scegliere la soluzione più coerente. I fatti: diventa
invisibile; l'unico non messo KO era **il monaco**, che non ha potuto vedere dove
si rifugiasse; porta con sé forse un **monile di ossidiana** o altro oggetto
magico, verso un'altra località di Faerûn **o un altro piano, temporaneamente**.

**Raccomandazione: il monile di ossidiana, e la destinazione è il PIANO DEL
FUOCO — la forgia dei salamandri dove la sua gilda commercia.**

Perché questa e non «un'altra località di Faerûn»:

| Motivo | Fondamento nel canone esistente |
|---|---|
| La sua gilda **ha già una rotta planare** | Therysol «fu venduta da mercanti drow affiliati alla gilda del Collezionista **ai salamandri nel Piano del Fuoco Elementale**, costretta a servire alla forgia» |
| L'ossidiana **è già legata al Piano del Fuoco** | canone del repo: *«giganti del fuoco che usano arieti fatti di ossidiana — forse forgiati proprio nel piano che avete appena lasciato»* |
| **Pianta l'arco 07 con tre archi d'anticipo** | quando i PG arrivano alla Forgia Eterna e al Piano del Fuoco, il Collezionista è già di casa lì **da tutta la campagna**. Payoff gratuito |
| Dà un **bersaglio** alla vendetta di Therysol | lei «scende in profondità cercando l'origine del suo destino — la gilda drow del Collezionista». Se lui è fuggito **lungo la stessa rotta su cui lei fu venduta**, la caccia di lei e la fuga di lui sono la **stessa strada** |
| Meccanicamente pulito | un rakshasa è un esterno nativo: il passo planare non richiede spiegazioni |

«Un'altra località di Faerûn» invece è un vicolo cieco: non spiega niente e non
si collega a niente.

> ⚠️ **Collisione da evitare**: nel repo esiste già il **Sigillo di Ossidiana**,
> artefatto allineato a **Shar** (`[CANONE — DM 2026-07-23]`), più una *Piramide*
> e un *Occhio* di Ossidiana. Il **monile** dev'essere un oggetto **distinto e
> minore** — non un pezzo del Sigillo. Se vuoi un filo fra i due, la formula
> sicura è «stessa pietra, stessa scuola, altra mano»: suggerisce una tradizione
> senza creare una dipendenza fra artefatti.

**E il dettaglio del monaco è il gancio, non un contorno**: c'è un testimone che
sa che è svanito, e **non sa dove**. Tordek porta quella domanda per tutta la
campagna. Quando i PG metteranno piede sul Piano del Fuoco, è lui che deve
riconoscere qualcosa.

### 10.4 Il mostro cristallino chiude anche la domanda sui «nuotatori nella pietra»

Il portale a senso unico li fa sbucare vicino alla miniera, dove incontrano il
**mostro cristallino** — e `campaign-history.md` mette i **Cristal Warriors**
(*Underdark* p.93) proprio «nelle prime sale dopo l'arrivo dal portale».

**Combacia.** Quindi le creature della pietra sono **due specie in due momenti**:

| Dove | Cosa |
|---|---|
| Subito dopo il portale, zona miniera | **Cristal Warriors** — il «mostro cristallino» |
| Molto più avanti, verso la Tomba | **elder xorn** (registro XP: «1 mostro a 3 gambe — un elder xorn») |

Non sono la stessa cosa e non vanno fuse.

---

### 10.5 ✅ CHIUSO — Hella ha *sentito* la perdita e ha fatto supposizioni

> *«Hella ha sentito questa perdita e ha fatto supposizioni»*

**È il caso migliore dei tre, e va scritto esattamente così.**

| Chi | Cosa sa |
|---|---|
| **Il DM** | la verità: i funghi bruciati, l'ira fungina |
| **Hella** | che il potere **se n'è andato**. Ha una **supposizione**, non una conferma |
| **Il gruppo** | ⚠️ **potrebbe non sapere di essere la causa** |

Regole di scrittura che ne discendono:

- nella Stanza Runica **non si annuncia niente**: la perdita è un **beat
  sensoriale**. Il micelio smette di rispondere. Non c'è un tiro, non c'è un
  messaggio: c'è un silenzio dove prima c'era una voce;
- Hella **ipotizza ad alta voce** — ed è il DM a sapere se ha ragione. Una
  supposizione detta al tavolo è più forte di una spiegazione corretta;
- **il filo resta vivo**: Hella muore all'arco 06 e torna all'arco 07. Se è morta
  senza sapere, la conferma può arrivare **dopo** la resurrezione — ed è una
  delle scene più forti disponibili in tutta la campagna;
- **il gruppo porta una colpa che non sa di avere.** Non serve fargliela
  scoprire: serve che il DM sappia che c'è.

**La catena è chiusa. Si può scrivere.**

### 10.6 La porta non aperta: **Zuggtmoy non viene mai incontrata**

> *«Hella avrebbe voluto incontrare Zuggtmoy senza davvero sapere cosa la
> aspettava — la follia come minimo. Ma il gruppo ha deciso di inseguire i drow
> attraverso un portale senza sapere nemmeno dove li avrebbe portati. Per loro
> fortuna, nella direzione giusta.»*

**È il beat che tiene insieme tutto l'arco fungino, ed è una scelta dei
giocatori, non una scena del DM.**

| | |
|---|---|
| **Hella voleva** | l'udienza con la Regina — senza sapere che il minimo prezzo era la follia |
| **Il gruppo ha scelto** | inseguire i drow in un portale di cui ignoravano la destinazione |
| **Esito** | direzione giusta **per fortuna**, non per bravura |

**Conseguenze per la scrittura:**

- **Zuggtmoy resta fuori scena, come Sonjak.** Due potenze, nessun volto: di
  entrambe si vedono solo le opere. È già un principio di regia della catena
  (§10.2) — ora è **doppio e voluto**, non un caso;
- il bivio va **giocato come bivio**: l'udienza è una **porta aperta e non
  attraversata**, non un'occasione mancata dal DM. I giocatori hanno scelto la
  fretta e la caccia. Il modulo deve rendere la porta **visibile** — altrimenti
  non è una scelta, è un corridoio;
- **il desiderio di Hella resta insoddisfatto** — e lei muore all'arco 06 senza
  averlo esaudito. Poi torna all'arco 07. È un filo che il DM può riaprire in
  qualunque momento, ed è già carico;
- ⚠️ **e c'è una scala di offesa**: il gruppo prima **rifiuta l'udienza** della
  Regina, poi **brucia i suoi funghi** nella Stanza Runica. L'ira fungina che
  toglie il dono a Hella non è un capriccio: è il **secondo** sgarbo. Scritta
  così, la punizione ha una progressione invece di essere arbitraria;
- il fatto che il portale porti **nella direzione giusta per caso** va scritto
  come tale: nella tabella delle contingenze, «e se sbagliassero portale?» è una
  domanda legittima che il modulo deve saper gestire.

---

## 11. ⚠️ Quale arco scrivere per primo — RACCOMANDAZIONE CORRETTA

Nella rev. 1 avevo proposto **l'arco 03** perché è il più ricco di materiale
(29 file, una mappa SVG già pronta). **Avendo letto le fonti, ritiro quella
proposta.**

Il file `il Tempio di Moradin - in fondo guardiano da sx.txt` **è testo tradotto
di *Expedition to Undermountain***, non appunti originali. Lo si riconosce da
tre segni nel testo stesso:

- rimanda a **«pagina 121»** e alla **«sezione Chiavi della Tomba»** — cioè alla
  paginazione del manuale d'origine;
- nomina i **nani del clan Melairkyn** — il clan di Undermountain, IP WotC;
- descrive gli otto pilastri, le otto chiavi e l'ascensore verso la Tomba con la
  struttura dell'originale.

E `Scontro_davanti_tempio di moradin.txt` contiene il blocco **Darklight Ore**
riportato **testualmente in inglese** da un manuale.

> **L'arco 03 è il più ricco di materiale proprio perché il materiale è di
> qualcun altro.** Scriverlo per primo significherebbe consolidare la parte più
> derivata della catena — l'opposto dell'obiettivo di ADR-0018.

### La scelta giusta: **il mercato drow di Sonjak** (§1.4)

| Criterio | Perché vince |
|---|---|
| **Provenienza** | **nessuna fonte dichiarata.** Viene per intero dal racconto del DM: è materiale suo al 100% |
| **Qualità** | è la scena migliore del corpus: un incontro drow che non è un combattimento, con un solo PG che sa il pericolo |
| **Autosufficienza** | un luogo, una discesa, tre tende. Si gioca in una sessione e non dipende da nient'altro |
| **Copertura dello standard** | ha già tutto ciò che il `module-standard` chiede: scelta grigia (comprare schiavi o no), sconfitta gestita (il passo falso, non il TPK), eco a lungo termine (il denaro finisce a Sonjak), momento per un PG specifico (Artemis che vede gli invisibili) |
| **Serve due prodotti** | è il primo tassello dell'AP vendibile **e** una scena giocabile per il tavolo |

**Ordine proposto rivisto**: mercato drow → Tana dei Minotauri → Gardens/prove →
torre fungina. Gli archi 03 e 04 si scrivono **dopo**, e si scrivono
**riprogettandoli**, non consolidandoli.
