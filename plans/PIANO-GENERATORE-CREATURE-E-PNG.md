# PIANO — Un generatore di creature e PNG dalle tabelle

> **Stato**: ✅ **A→I chiusi** (2026-09-03). Le tre domande di §7.6 hanno avuto
> risposta e il lotto I è fatto: 21 celle, 18 liste, `ranger`/`paladino`/`bardo`
> che prima il generatore non sapeva costruire, e la variante PF1e sugli
> incantesimi. **Aperti**: i lotti **J** e **K**, proposti in §9 e §10 su
> richiesta del DM, non ancora autorizzati.
> **Il debito del Bestiario è chiuso: 157 schede su 157 sistemate.** · **Aperto**: 2026-09-02 · **Avviato**: 2026-09-03
> **Decisioni del DM (§5)**: taratura **SRD 3.5 di norma, PF1e come variante
> più cattiva**; il generatore serve per **quello che nel Bestiario non c'è**;
> `suggest_encounter` deve poterne pescare una parte. Ruoli e tabelle del
> carattere: **proposti qui, da confermare**.
> **ADR**: [ADR-0034](adr/ADR-0034-generare-dalle-tabelle.md)
> **Nasce da**: domanda del DM — *«alla fine c'è un generatore di mostri e PNG,
> anche incantatori, fra i tool disponibili al DM, che usa quelle tabelle per
> generare le cose? ha senso creare un nuovo piano o è stato fatto?»*
> **Risposta**: **non è stato fatto.** `suggest_encounter` **pesca** dal catalogo
> (306 record esistenti); non costruisce niente di nuovo.
> **Precedenti da leggere prima**: [ADR-0021](adr/ADR-0021-statblocchi-machine-readable.md)
> · [ADR-0033](adr/ADR-0033-derivare-e-dichiararlo.md) · skill `dnd-35-srd`,
> `pathfinder-1e-srd`, `npc-villain-boosting`

---

## §1 · Perché questo è un problema DIVERSO da quello che è appena fallito

Va detto subito, perché il lotto H si è chiuso con una prova negativa e sarebbe
facile leggerla come un divieto.

Nel lotto H `derive_statblocks.py` ha provato a **ricavare i numeri da schede in
prosa già scritte**, e il collaudo li ha respinti quasi tutti. La causa è
strutturale: una scheda è un documento, non un dato, e un'espressione regolare ci
trova sempre qualcosa di plausibile — *«Esperto 2»* dove la riga diceva *«Esperto
2 / Acolita 6»*, i dadi di un morso scambiati per dadi vita.

**Generare è la direzione opposta, e non ha quel problema.** Non c'è prosa da
interpretare: si parte da **quello che il DM dichiara** — GS, ruolo, tipo,
taglia — e le tabelle producono i numeri. È esattamente l'uso per cui quelle
tabelle esistono. Un generatore non può leggere male una scheda perché **non
legge nessuna scheda**.

Il rischio qui è un altro, ed è il vero criterio di progetto: **produrre creature
generiche che si assomigliano tutte.** Un mostro che rispetta perfettamente la
riga della tabella e non ha niente di suo è peggio di nessun mostro: al tavolo si
gioca come tutti gli altri.

---

## §2 · Cosa esiste già (per non rifarlo)

| Strumento | Cosa fa | Cosa NON fa |
|---|---|---|
| `suggest_encounter.py` | sceglie 3-5 combinazioni per un EL bersaglio dal catalogo, per fazione/ambiente, con seed | non crea creature |
| `build_monster_catalog.py` | indicizza i 306 statblocchi esistenti | non genera |
| `derive_statblocks.py` | deriva CA/pf/TS **da una scheda esistente**; scrive i soli TS | non parte da zero |
| skill `npc-villain-boosting` | il **quadro decisionale** per potenziare | è dottrina, non un tool |
| `scripts/schemas/statblock.schema.json` | il **contratto** del blocco | — |

Il pezzo che manca è uno solo: **da (GS + ruolo + tipo) a un blocco completo.**

---

## §3 · Le tabelle, e quali sono davvero verificate

⚠️ **Prima cosa da fare, prima di scrivere codice.** In `derive_statblocks.py`
la tabella per GS ha venti righe, ma **solo otto sono verificate contro la fonte**
(GS 8 e 10-16); GS 1-7 e 17-20 le ho interpolate io, e il campo
`PER_GS_VERIFICATE` lo dichiara. Un generatore che le usasse come bersaglio
propagherebbe numeri non controllati su ogni creatura che produce.

**Lotto 0 del piano: verificare le dodici righe mancanti** contro la fonte
(`pathfinder-1e-srd/references/monster-advancement.md`, e la sua fonte a monte),
oppure dichiararle non disponibili e rifiutarsi di generare a quei GS.

Serve inoltre quello che oggi **non abbiamo in casa**:

- la **riga per gli incantatori** (livello dell'incantatore e CD primaria per GS)
  — il DM la segnala come esistente, va procurata e verificata;
- le **statistiche per GS dei PNG**, distinte da quelle dei mostri;
- ⚠️ e una **taratura 3.5**: le righe PF1e sono più dure a parità di GS, e questa
  campagna gira su 3.5. Generare sui numeri PF1e produrrebbe mostri
  sistematicamente più cattivi di quanto il GS promette. Va deciso e scritto in
  un ADR: o si tara, o si dichiara che il generatore produce «GS PF1e».

> **⚠️ Correzione, 2026-09-03 (ADR-0034).** L'ultimo punto qui sopra l'avevo
> scritto io e **è sbagliato**. Misurata contro i mostri del SRD 3.5, la riga
> PF1e non è «molto più dura»: Ogre GS 3 ha 29 pf contro i 30 della riga; il
> Gigante delle Colline GS 7 ne ha 102 contro 85. Sui punti ferita le due
> tarature si sovrappongono, e PF1e sta un punto o due sopra su CA e attacco.
> La taratura 3.5 è quindi la riga PF1e con **CA −1 e attacco −1** — non una
> derata al 70%, che avrebbe prodotto mostri di carta. La differenza vera fra i
> due sistemi sta nei **template**, ed è da lì che viene la variante più cattiva.
> *(Lascio il testo originale sopra invece di riscriverlo: la premessa sbagliata
> ha guidato il primo tentativo, e cancellarla nasconderebbe perché.)*

---

## §4 · I lotti

### ✅ Lotto A — Le tabelle, verificate e in un posto solo
Le righe per GS (mostri · PNG · incantatori) diventano un dato del repo, con la
**provenienza per riga** e il segno di quali sono verificate. Nessuna riga
inventata in silenzio. **Accettazione**: ogni riga cita la sua fonte; un test
confronta la tabella con le righe d'ancora della skill.

**✅ Chiuso 2026-09-03.** `scripts/dmcore/tabelle.py` — provenienza riga per riga, `PER_GS_VERIFICATE` conservato, e `derive_statblocks.py` ora **importa** invece di tenere una seconda copia. `test_tabelle.py`: 12 test, 134 sotto-test, che confrontano le griglie con le **ancore scritte nelle skill**, non con una costante accanto.

### ✅ Lotto B — Il generatore, per creature non incantatrici
`scripts/genera_creatura.py`: da `--gs`, `--tipo`, `--taglia`, `--ruolo`
(bruto · schermagliatore · tiratore · comandante) a un blocco completo, con
`--seed` per la riproducibilità (come `suggest_encounter`).
**Accettazione**: il risultato **supera il collaudo sul GS** — cioè la stessa
guardia che nel lotto H respingeva tutto, qui deve passare, e se non passa il
generatore è sbagliato. Test su tutti i GS disponibili e tutti i ruoli.

**✅ Chiuso 2026-09-03.** `scripts/genera_creatura.py`. ⚠️ La **prima versione non passava il collaudo**: un GS 7 con 38 pf e CA 12, −55% sul bersaglio. Costruiva ogni cosa come un PNG con la matrice standard; un mostro non si fa così. Riscritto risolvendo le caratteristiche **verso** il bersaglio, e ora sta nella fascia di Ogre, Troll, Ettin, Chimera, Gigante delle Colline e Osyluth.

### ✅ Lotto C — I PNG con livelli di classe
Razza + classi (comprese le classi PNG del SRD) + matrice elite/standard +
equipaggiamento per livello. **Accettazione**: un PNG generato e uno scritto a
mano dallo stesso profilo stanno nella stessa fascia.

**✅ Chiuso 2026-09-03.** Matrice élite/standard, aumenti ogni 4 livelli (senza, un mago di 9° usciva con Int 15), equipaggiamento per livello, e un collaudo **diverso**: per un PNG con classi il metro non è la riga dei mostri — sono i livelli. Il confronto col mostro resta stampato, ma per un'altra domanda: *regge un incontro da solo?*

### ✅ Lotto D — Gli incantatori
La parte che il DM ha chiesto per nome e che è la più delicata: livello
dell'incantatore, incantesimi al giorno dalle tabelle di classe SRD, CD primaria
dal GS, e **la scelta degli incantesimi** — che è dove un generatore diventa
banale se la fa a caso. Proposta: non estrarre a sorte da tutto il SRD, ma da
**liste per ruolo** (controllore · artigliere · sostegno) scritte a mano una
volta. **Accettazione**: le CD stanno sulla riga del GS; nessun incantesimo fuori
lista di livello.

**✅ Chiuso 2026-09-03.** Griglie SRD complete di mago, stregone, chierico, druido, adepto. ⚠️ Un difetto vero trovato dal test: un **chierico costruito come «controllore» prendeva Int 18 e Sag 13**, e la sua CD restava cinque punti sotto la riga del GS. La caratteristica da incantatore ora batte quella del ruolo. Le CD di mago e chierico cadono **esattamente** sulla riga PF1e a GS 5, 9 e 13.

### ✅ Lotto E — Il carattere, cioè la ragione per cui non è banale
Una creatura generata esce con **una cosa sua**: un talento firma, una tattica in
una riga, una debolezza sfruttabile. Prese da tabelle scritte a mano per ruolo,
non generate. ⚠️ **È questo lotto che decide se il tool serve**: senza, produce
mostri intercambiabili, e un mostro intercambiabile il DM se lo scrive prima da
solo che a leggerlo.

**✅ Chiuso 2026-09-03.** Quattro terne (talento firma · tattica · **debolezza sfruttabile**) per ognuno dei sei ruoli, scritte a mano. ⚠️ **Proposte al DM**, come chiedeva §5.

### ✅ Lotto F — Dove finisce l'output
**Non scrive mai dentro `Bestiario/`.** Stampa il blocco, o scrive in una
cartella di lavoro, e il DM decide se e come farlo entrare — lo stesso confine di
ADR-0033. Con `fonte: generato-SRD — <parametri e conto>`, così fra sei mesi si
sa da dove viene e lo si rifà uguale.

**✅ Chiuso 2026-09-03.** `--in <cartella>`, e un rifiuto esplicito a scrivere sotto `Bestiario/` con la ragione scritta. `fonte:` porta parametri e taratura.

---

### ✅ Lotto G — Il generatore dentro `suggest_encounter`
Aggiunto su richiesta del DM dopo l'apertura del piano: `suggest_encounter`
pesca dal catalogo, e con un'opzione **pesca in parte dal generatore**, così gli
incontri non escono mai due volte uguali. L'opzione «più cattivi» si propaga
alla sola parte generata. **Accettazione**: stesso seed → stesso incontro; il
GS combinato resta quello dichiarato.

**✅ Chiuso 2026-09-03.** `--con-generatore` e `--piu-cattivi`. L'innesto è nel
**pool**, non nel costruttore: aggiungere candidati e lasciar scegliere la logica
di bilanciamento di sempre evita di scriverne una seconda da tenere allineata.
⚠️ Metterli solo nel pool **non bastava**: dodici candidati contro 308 record del
catalogo non uscivano quasi mai, e l'opzione sembrava accesa senza esserlo — che
è il modo peggiore di sbagliare, perché non si vede. Ora una creatura generata
entra per forza in ogni proposta e il resto resta pescato dal Bestiario.
Verificato: stesso seed → output identico; **senza il flag l'output è byte per
byte quello di prima**.

---

## §5 · Le domande da porre al DM prima di cominciare

> **Risposte ricevute il 2026-09-03**, riportate qui perché il piano si legga da solo.

1. **La taratura**: 3.5 o PF1e? (vedi §3 — cambia ogni numero prodotto)
   → **SRD 3.5 di norma; PF1e come variante più cattiva, a richiesta.** Attuato
   in ADR-0034. ⚠️ Nel farlo è emerso che la premessa del piano era sbagliata:
   sulla riga base PF1e **non** è molto più duro del 3.5 (Ogre GS 3: 29 pf
   contro 30). La differenza sta nei *template*, e la variante più cattiva viene
   da lì — Advanced applicato senza alzare il GS.
2. **I ruoli**: quali servono davvero al tuo tavolo? Bruto, schermagliatore,
   tiratore, comandante, controllore, artigliere — o meno?
   → **Non risposta.** Proposti tutti e sei, come dati e non come rami del
   codice: toglierne uno è una riga in `RUOLI`.
3. **Il carattere (lotto E)**: le tabelle di talenti/tattiche firma le scrivi tu
   o le propongo io per la tua conferma?
   → **Proposte io**, in `CARATTERE`: 24 terne, quattro per ruolo. Da confermare.
4. **Dove finisce**: stampa a schermo, o un file in una cartella di lavoro?
   → **Tutt'e due**: stampa di norma, `--in <cartella>` quando serve un file.
   Mai dentro `Bestiario/`, che il tool rifiuta.

---

## §6 · Quando NON usarlo

Va scritto adesso, o il tool diventa la scorciatoia per tutto:

- se nel catalogo c'è già qualcosa di simile → **potenzialo** (`npc-villain-boosting`);
- se la creatura ha un ruolo nella trama → **si scrive a mano**, il generatore dà
  al massimo l'ossatura;
- se serve per **un incontro di passaggio** → è esattamente il suo caso.

### ✅ Lotto H — Le 52 schede che restavano
Punto 2 del DM: *«finisci le schede dei mostri e PNG che mancano»*.

**✅ Chiuso 2026-09-03 — 157 su 157.** Anche qui, come nel lotto H della catena
editoriale, il debito **non era una cosa sola**: erano quattro problemi diversi
contati come uno.

| Quante | Cos'erano | Cosa si è fatto |
|---:|---|---|
| **27** | i numeri stanno **altrove** e duplicarli sarebbe peggio: schede dei pregen in `ARC08-02`, PNG alleati in `ARC08-01`, dossier che puntano al proprio statblocco e viceversa, due schede di **stato finale post-mortem** che dicono a chiare lettere di non essere statblocchi | marcatore `[RIMANDO]`, **verificabile**: la scheda deve dire *dove*, e `--check` va a vedere che quel posto esista |
| **1** | non è una creatura: «Duergar della Scala di Ossa» è un **set d'incontro** di quattro PNG nominati, e il suo «GS 11» è il livello dell'incontro | `[NON-CREATURA]`, la sesta |
| **11** | avevano i numeri del DM in **dialetti che il parser non leggeva** | tre dialetti nuovi insegnati (vedi sotto) |
| **13** | dichiaravano i parametri ma non i numeri | costruite con le tabelle SRD, `fonte:` che dice quali campi sono derivati e quali letti |

**I difetti trovati per strada**, che valgono più delle schede:

- il parser leggeva righe che descrivono **altre creature dello stesso dossier**
  — il Conte Valerius prendeva la CA giusta (13) col dettaglio delle sue guardie
  («armatura completa +2») e i punti ferita esatti marcati «approssimati» per via
  del `~` delle guardie. Un blocco che descriveva due creature diverse;
- una **forbice** lasciata aperta dal DM non è un numero da scegliere: il
  Ghostlord dice «58–90, il DM adatta al livello del party». Il blocco tiene
  l'estremo basso e **scrive la forbice accanto**;
- tre schede dicevano «CA da SRD» citando il file d'origine, che è nel repo:
  lette invece che ricordate, e **tre numeri su quattro erano sbagliati a
  memoria** (Bebilith CA 22 e non 19, Phantom Fungus 14 e non 15, Retriever col
  BAB trascritto +10 dove il SRD dice +7);
- il generatore dava **CA 11 a un arcimago di GS 14**, perché non contava
  l'equipaggiamento: un PNG di quel livello ha 27.000 mo addosso, e la prima cosa
  che compra un incantatore sono bracciali e anello.

⚠️ Le 13 costruite sono **proposte da rileggere al tavolo**, e ognuna lo dichiara
nel proprio `fonte:`. Il confine di ADR-0033 resta: lo strumento propone.

### ✅ Documentazione
Un tool che nessuno sa di avere è un tool che non esiste. Misurato prima di
scrivere: `genera_creatura`, `--piu-cattivi`, `--con-generatore` e `[RIMANDO]`
comparivano in **zero** guide e **zero** skill.

- `GUIDA-BESTIARIO` §0 (la domanda «serve davvero una scheda nuova?»), §6-bis
  (tre strumenti invece di due, più «quando i numeri stanno da un'altra parte»),
  **§6-ter nuova** (costruire una creatura che non c'è, i sei ruoli, il carattere,
  `--piu-cattivi`, gli incontri che non si ripetono, e ⚠️ quando NON usarlo), §8
  (il rimando incrociato: potenziare se qualcosa c'è, generare se non c'è);
- skill `npc-villain-boosting`: una sezione **prima** dell'albero decisionale —
  potenziare presuppone qualcosa da potenziare;
- skill `rumblingstone-automation`: le due opzioni di `suggest_encounter`.

### ✅ Lotto I — Gli incantatori per lista di classe e funzione
La revisione che nasce dal difetto dei due druidi: le liste vanno per **lista di
classe**, non per ruolo né per tradizione. La proposta per esteso, con la matrice
e le domande, è in **§7**; le risposte del DM in **§7.6**.

**✅ Chiuso 2026-09-03.** `scripts/dmcore/incantesimi.py` — **21 celle servite da
18 liste**, perché mago e stregone condividono la lista (nel SRD *è* la stessa, e
due copie divergerebbero al primo ritocco). Il ripiego, quando una cella non
esiste nel gioco, resta **dentro la stessa classe** e lo scrive nel conto: era
esattamente il vecchio `LISTA_DI_RIPIEGO` a mandare un ruolo sulla lista di
un'altra classe.

**Quello che il piano non aveva previsto, e che è costato più delle liste**:

| Cosa | Perché il piano non l'aveva visto |
|---|---|
| **bardo, ranger e paladino non avevano una griglia** in `tabelle.py` | §8 diceva «le griglie ci sono già». Ce n'erano cinque su otto: senza `BARDO`, `BARDO_CONOSCIUTI`, `RANGER` e `PALADINO` il generatore non poteva costruire un bardo — e `lomyn-redtongue-bardo4-cr3` è nel Bestiario da sempre |
| ⚠️ **il paladino lanciava su Carisma** in `dnd-35-srd/references/classes.md` | è la regola di **PF1e**. Nel SRD 3.5 la CD è su **Saggezza**; il Carisma serve a Grazia Divina, Imposizione delle Mani e Punizione. Ogni paladino generato sarebbe uscito con la CD sbagliata *e* la caratteristica sbagliata al primo posto della matrice élite |
| **livello dell'incantatore ≠ livello di classe** per ranger e paladino | `livello − 3`. Un paladino di 12° lancia da 9°: stampare 12 dà due punti di CD di troppo |
| **un incantatore spontaneo non «prepara»** | il blocco diceva «Preparati» anche per bardo e stregone. È una parola, e la legge il DM al tavolo mentre decide cosa quella creatura può lanciare |

**Le tre correzioni al piano stesso**, che vanno scritte perché il piano le
sbagliava e qualcuno le rileggerà:

1. **«17 liste» e «undici» erano tutt'e due sbagliati.** Contando la matrice di
   §7.3: le ✅ sono **16**, le ○ **5** (contando ranger e paladino separati). Il
   DM ha approvato ✅ + ○, cioè **21 celle**.
2. ⚠️ **L'esempio di lista druidica in §7.4 conteneva quattro errori.**
   *Frantumare* non è sulla lista del druido (è da mago, chierico e bardo);
   *muro di spine* è al 5°, non al 4°; *muro di pietra* al 6°, non al 5°;
   *tempesta vendicativa* al 9°, non all'8°. Il testo di §7.4 resta com'era, con
   la nota qui accanto: era la proposta, e cancellarla nasconderebbe che una
   lista scritta a memoria sbaglia comunque.
3. ⚠️ **La diagnosi «*dito della morte* è un incantesimo da mago dato a un
   druido» era falsa.** *Dito della morte* è sulla lista del druido, all'**8°**
   livello (per il mago sta al 7°). Su quella scheda il difetto non era la
   classe: era il **livello** — l'altro modo in cui una lista per ruolo
   sbagliava, meno vistoso e più difficile da vedere al tavolo. L'ha trovato il
   test, non la rilettura.

**L'ancora, che è la parte che rende il test non circolare.** Le liste di classe
del SRD stanno ora in `skills/dnd-35-srd/references/spells.md` §«Liste di
classe», e la divisione del lavoro è netta: la skill dice *cosa quella classe può
lanciare* (un fatto di regole), il modulo dice *cosa un controllore sceglie
davvero* (una scelta di progetto). `test_incantesimi.py` verifica l'inclusione
fra le due — 15 test, ~870 sotto-test.

**Il residuo dichiarato**: l'**adepto**. È fuori dalle 21 celle approvate, e
resta l'unica classe incantatrice per cui il generatore si rifiuta di scegliere.

**Le due schede** (`arci-druido-circolo-cr14`, `druid-bear-ally-cr12`) sono
tornate complete, con `funzione` e `seed` scritti in `fonte:` perché si rifacciano
identiche.

**La variante PF1e sugli incantesimi**, chiesta dal DM in corso d'opera: §8-bis.

---

## §7 · PROPOSTA — gli incantatori per lista di classe e funzione

> ⚠️ **Proposta, non ancora approvata.** Nasce da una domanda del DM
> (*«anche per gli incantatori ci sono arcano e divino e ibridi, e i ruoli
> controllore blaster supporto utilità»*) e da un **difetto vero** trovato mentre
> le rispondevo: due druidi generati avevano incantesimi che un druido non lancia.

### §7.1 · Perché la tradizione non basta

Il primo istinto — separare **arcano** e **divino** — è quello sbagliato, e vale
la pena dire perché prima di scrivere una riga di codice.

Il generatore sceglieva per **ruolo**: «controllore» → lista arcana, «comandante»
→ lista divina. Risultato sulle schede vere:

| Scheda | Classe | Cosa ha ricevuto | Perché è sbagliato |
|---|---|---|---|
| arci-druido GS 14 | druido | *armatura magica*, *sonno*, *dito della morte* | sono da **mago** |
| druido-orso GS 12 | druido | *benedizione*, *santuario*, *scudo della fede* | sono da **chierico** |

Il secondo caso è quello istruttivo: la lista era **divina**, e ancora sbagliata.
Chierico e druido sono tutti e due divini e hanno **liste diverse**. Il bardo è
«ibrido» e ha una lista sua che non coincide con nessuna delle due.

**Quindi la chiave è la lista di CLASSE**, e la tradizione serve solo a
raggrupparle per chi legge.

### §7.2 · Le quattro funzioni

Le parole sono quelle del DM; la colonna «cosa fa al tavolo» è quello che
decide se una funzione serve davvero.

| Funzione | Cosa fa al tavolo | Come si riconosce |
|---|---|---|
| **controllore** | toglie ai PG le opzioni: terreno, movimento, azioni | vince i round che non combatte |
| **blaster** | danno, spesso d'area (oggi il ruolo si chiama «artigliere») | il round in cui apre si vede |
| **supporto** | tiene in piedi i suoi: cure, potenziamenti, rimozione | il suo valore è nei pf che *non* perdono gli altri |
| **utilità** | informazione, mobilità, contromagia, difese | è quello che rende difficile arrivargli |

⚠️ **«artigliere» o «blaster»?** Oggi il codice dice `artigliere`. Rinominarlo in
`blaster` è una riga, ma cambia l'interfaccia (`--ruolo blaster`) e va deciso una
volta sola. **Domanda al DM.**

### §7.3 · La matrice: quali celle valgono la scrittura

Sei liste di classe × quattro funzioni = 24 caselle, ma non tutte esistono nel
gioco. Un paladino blaster non c'è.

| Classe (tradizione) | controllore | blaster | supporto | utilità |
|---|:---:|:---:|:---:|:---:|
| **mago** (arcano, preparato, INT) | ✅ | ✅ | — | ✅ |
| **stregone** (arcano, spontaneo, CAR) | ✅ | ✅ | — | ○ |
| **chierico** (divino, domini, SAG) | ✅ | ✅ | ✅ | ✅ |
| **druido** (divino, natura, SAG) | ✅ | ✅ | ✅ | ✅ |
| **bardo** (ibrido, spontaneo, CAR) | ✅ | — | ✅ | ✅ |
| **ranger · paladino** (divino parziale, LI = liv − 3, max 4°) | — | — | ○ | ○ |

✅ = da scrivere · ○ = utile ma non urgente · — = non esiste nel gioco

**Diciassette liste**, non quattro. È il costo vero della cosa fatta bene, e va
detto prima invece di scoprirlo a metà.

### §7.4 · Come sarebbe una lista (esempio, druido controllore)

Oggi il druido non ha lista e il generatore **si rifiuta di sceglierne una**.
Ecco cosa ci andrebbe — tutto SRD 3.5, lista del druido:

```
1°: intralciare, fuoco fatuo, nebbia oscurante
2°: legame, raffica di vento, frantumare
3°: crescita vegetale, chiamare il fulmine, radicamento
4°: muro di spine, evocare nube, controllare piante
5°: muro di pietra, scacciare i mostri, cambiare forma minore
6°: muro di ferro, viaggio arboreo di massa, respingere legno
7°: cambiare forma, tempesta di fuoco, controllare il clima
8°: tempesta vendicativa, terremoto, forma animale di massa
9°: tempesta di vendetta, mutare forma superiore, prigione di roccia
```

Si vede subito la differenza: **niente** di questo compare nella lista arcana, e
nessuno di questi è un incantesimo da chierico.

### §7.5 · Cosa costa, e cosa si guadagna

**Costa**: 17 liste × 9 livelli ≈ 150 righe di dati scritti a mano, più un test
per lista che verifichi che ogni incantesimo appartenga davvero a quella classe.
Il test è la parte che rende la cosa affidabile: senza, ci si accorge del difetto
al tavolo, com'è appena successo.

**Si guadagna**: un incantatore generato che si può **giocare così com'è**,
invece di una cornice da riempire a mano. È la differenza fra uno strumento e un
promemoria.

### §7.6 · Le tre domande al DM

> **Risposte ricevute il 2026-09-03.**

1. **`artigliere` o `blaster`?**
   → **`blaster`**, con `artigliere` mantenuto come **alias**: il nome nuovo è
   quello canonico e finisce in `fonte:`, così due schede generate coi due nomi
   restano confrontabili, ma nessun comando già scritto negli appunti si rompe.
2. **Le 17 caselle, o meno?**
   → **✅ + ○**, cioè tutte. Sono **21** celle, non 17 né 11 (vedi la correzione
   nel lotto I): ranger e paladino compresi, con le loro liste ridotte a quattro
   livelli.
3. **Le liste le scrivo io e le confermi tu?**
   → **Le propongo io**, come per il carattere, con il test di appartenenza a
   fare da rete. ⚠️ **Da confermare in PR.**

**E le due conferme che il §5 aveva lasciate appese:**

4. **I sei ruoli** → **confermati** tutti e sei.
5. **Le 24 terne di `CARATTERE`** → **confermate.**


---

## §8 · Da dove si comincia, in una chat nuova

```bash
# 1. lo stato reale, non quello che dice questo file
python3 scripts/extract_statblocks.py --check
python3 scripts/genera_creatura.py --gs 9 --ruolo controllore --classe druido:9

#    ↑ il secondo comando mostra il difetto ancora aperto: il druido esce
#      SENZA incantesimi, e lo dichiara. È il lotto I.

# 2. i test che tengono ferma la parte già fatta
python3 -m pytest scripts/tests/test_genera_creatura.py scripts/tests/test_tabelle.py -q
```

**Prima di scrivere una riga**: leggere §7 e ottenere dal DM le risposte alle tre
domande di §7.6. Senza quelle, si scrivono diciassette liste che poi vanno
rifatte.

**I file da toccare**: `scripts/genera_creatura.py` (`INCANTESIMI`,
`CLASSI_SENZA_LISTA`), `scripts/dmcore/tabelle.py` (le griglie ci sono già),
`scripts/tests/test_genera_creatura.py`.

**Le regole del repo che valgono qui**: ADR-0034 (generare e dichiarare),
ADR-0033 (lo strumento propone, il DM scrive), ADR-0021 (il blocco è un dato).
E la regola d'oro dei piani: checklist + `INDEX.md` + `CHANGELOG.md` **nello
stesso commit** (skill `rumblingstone-plans`).


---

## §8-bis · La variante PF1e sugli incantesimi (chiesta in corso d'opera)

> Richiesta del DM: *«se il DM vuole per la generazione la versione più potente
> mantenendo il GS si possano usare gli incantesimi di Pathfinder 1e se più
> potenti»*.

Il meccanismo c'è: `--incantesimi pf1e`, che `--piu-cattivi` accende da sé
(«più cattivo a pari GS» vale per il template e per la lista; due interruttori
per una cosa sola sono due modi di dimenticarne uno). `--incantesimi srd` lo
spegne tenendo il template.

**Ma il perimetro è più stretto della richiesta, e la ragione va detta.** Sugli
incantesimi condivisi **PF1e non è più forte: è pari o più debole**, e lo dice la
tabella di compatibilità che questo repo ha già in
`pathfinder-1e-srd/references/conversion-guide.md` — *grasso*, *polvere
scintillante* e i *tentacoli neri* indeboliti via CMB e tiri salvezza, il «salva o
muori» convertito in danno, il polimorfismo riscritto. Scambiare *palla di fuoco*
con la *palla di fuoco* PF1e non compra niente: è lo stesso incantesimo. Vendere
come «più cattivo» qualcosa di più debole sarebbe il modo peggiore di sbagliare:
invisibile alla generazione, scoperto al tavolo.

Quello che rende davvero più duro un incantatore PF1e a pari GS è, in ordine:

1. gli incantesimi che in 3.5 **non esistono** — 55 righe, la linea della
   *fossa*, *scirocco*, *saette*, *benedizione del fervore*, e per il paladino
   tutta la linea del *fuoco* legata alla Punizione;
2. il **+4 alle caratteristiche mentali** del template Advanced, che alza ogni CD
   di 2. È l'effetto più grosso, e `--piu-cattivi` lo applicava già;
3. le liste di **evocazione** PF1e, che offrono creature migliori per livello.

⚠️ **Il controllo delle righe PF1e ha trovato tre errori**, dello stesso genere
di quello per cui esiste tutto il lotto:

- *ill omen* stava sulla lista di mago e non è un incantesimo da mago (è da
  **strega**, psichico, mesmerista);
- *stone call* stava al 3° ed è **sorcerer/wizard 2**;
- *hungry pit* risultava introvabile a una prima estrazione automatica. C'è, al
  5° da mago: il nome porta il pedice del componente focus e il parser lo
  incollava al nome. **Un'assenza silenziosa dentro un'ancora è peggio di
  un'ancora mancante**, perché il test passa lo stesso.

E un quarto, nell'ancora stessa: i nomi PF1e portano la virgola **dentro**
(*pain strike, mass*), e il separatore era la virgola. Sette voci si erano
spezzate in «mass», «greater», «lesser». Anche questo passava il test, perché
quelle voci fantasma erano *in più* e non *in meno*: nessuno le cercava. Ora il
separatore è ` · ` e c'è una guardia che rifiuta un suffisso nudo.

**Il DM ha risolto il blocco di rete consegnando le due pagine.**
`pathfinder.d20srd.org` resta fuori dal criterio di rete dell'ambiente, ma le
liste — core e Advanced Player's Guide — sono state passate come file, e da lì
è nata l'ancora vera: `pathfinder-1e-srd/references/conversion-guide.md`
§«PF1e spell lists», che tiene le liste **APG** per le sei classi. Sono gli
incantesimi che PF1e *aggiunge*: la lista core di Pathfinder, nome per nome, è
abbastanza vicina al SRD 3.5 che tenerla non servirebbe a niente.

Con l'ancora, le righe sono passate da 21 a **55** e non c'è più nessuna riga
non verificata: `test_incantesimi.py` le controlla tutte contro la sezione, e la
verifica morde (provato iniettando una riga sbagliata a posta). Sono coperti
anche il **paladino**, che prima non aveva nessuna riga, e i livelli che erano
scoperti per mago, druido, bardo e ranger.

⚠️ **Il chierico resta scoperto al 1°, 6° e 7°, ed è voluto**: a quei livelli
l'APG non aggiunge niente che cambi un incontro. Un buco dichiarato batte una
riga messa per far quadrare la tabella — una variante «più cattiva» che non è
più cattiva è il modo peggiore di sbagliare, perché non si vede.

### §8-ter · La conseguenza sulla licenza, che il lotto aveva aperto in silenzio

Domanda del DM mentre il lotto si chiudeva: *«perché lato licenza non si usa
l'Open Game License?»*

**Si usa già** — per la porzione che governa, ed è scritto in `LICENSES.md`
§«Cosa queste due licenze NON coprono». L'OGL non può essere la licenza di tutto
il repo perché licenzia **Open Game Content**, cioè meccanica di gioco: la prosa
delle avventure, il canone della Cannath Vale, le mappe e gli script non sono
OGC, e per quelli servono CC BY-NC-SA e MIT (ADR-0029).

⚠️ **Ma la domanda ha scoperto un buco che questo lotto aveva allargato.**
`LICENSES.md` dichiarava una sola fonte OGC, l'SRD 3.5. Le fonti sono **due**: i
bersagli per GS e i template semplici vengono dal Bestiary PF1e da prima di
questo piano, la ricchezza per livello del PNG dal Core Rulebook, e ora le liste
di incantesimi dall'Advanced Player's Guide. Materiale Paizo porta le **sue**
voci di Sezione 15, e nessuna era dichiarata.

Peggio: nel repo **non c'era il testo dell'OGL**. La Sezione 10 dice che una
copia della licenza va con ogni copia dell'OGC distribuito, e il cancello
d'uscita di `GUIDA-CONDIVISIONE-IP` §7 lo chiedeva senza avere niente da
allegare — una casella che si poteva citare ma non passare.

Chiuso: `OGL.txt` con il testo integrale (verbatim dal PRD, che il DM ha
consegnato) e la Sezione 15 ridotta alle **sei voci** del materiale da cui il
repo deriva davvero. La catena del PRD ne ha 93 perché raccoglie tutta la linea
Paizo più il Tome of Horrors; copiarle tutte dichiarerebbe un uso che qui non
c'è, ed è il modo più rapido di rendere inutile una catena di copyright.

Trovata per strada una citazione larga: `npc-building.md` elencava l'**NPC
Codex** fra le fonti, ma non ne deriva niente — è un suggerimento di consulto al
tavolo. Riscritta, perché una fonte dichiarata e non usata è una voce di Sezione
15 che qualcuno prima o poi aggiunge per scrupolo.

⚠️ **Da decidere al tavolo**: se questa estensione del perimetro OGC meriti un
ADR suo o basti la riga in `LICENSES.md`. ADR-0029 stabilisce già il principio
(«l'OGC resta sotto OGL»); qui si nomina una seconda fonte, e la differenza è
sottile abbastanza da essere una scelta del DM.

---

## §9 · PROPOSTA — Lotto J: i template semplici di PF1e

> ⚠️ **Proposta, non autorizzata.** Nasce da una domanda del DM: *«ha senso
> inserire i template (archetipi) di Pathfinder 1e per versioni potenziate dei
> PNG e mostri della 3.5, quelli sotto licenza aperta e non chiusi da Paizo?»*

**Sì per i template semplici. No per gli archetipi di classe**, e i due non sono
la stessa cosa — è la prima distinzione da fare.

| | Cos'è | Verdetto |
|---|---|---|
| **template semplice** (Advanced, Giant, Young, Celestial, Fiendish, Entropic, Resolute…) | una manciata di modificatori applicati a una creatura finita | **sì**: è aritmetica, si applica a un blocco 3.5 senza attrito, e uno lo usiamo già |
| **archetipo di classe** (Two-Handed Fighter, Urban Ranger…) | scambia i privilegi di classe di una classe PF1e | **no**: importarli significa importare il telaio di classe di PF1e dentro il 3.5, che è la cosa che la guida di conversione dice di non fare |

**Sulla licenza**, che è la parte della domanda a cui va risposto per primo: i
template semplici sono **meccanica**, e la meccanica del PRD è Open Game Content
sotto OGL 1.0a. La Product Identity di Paizo è un'altra cosa — i nomi propri di
Golarion, le divinità, l'ambientazione, l'illustrazione, il marchio «Pathfinder».
«Advanced», «Giant», «Young» sono termini meccanici generici: si importano. Il
gate d'uscita resta quello della skill `rumblingstone-edizione`, e va passato
**prima** di consegnare, non dopo.

**Cosa costa.** Il repo ha già `ADVANCED` in `genera_creatura.py` e la sezione
dei template semplici in `pathfinder-1e-srd/references/monster-advancement.md`.
Il lotto è: generalizzare `--piu-cattivi` in `--template <nome>` (tenendo
`--piu-cattivi` come alias di `--template advanced`, stessa disciplina della
rinomina del lotto I), scrivere i cinque o sei template restanti come dati con la
provenienza per riga, e un test per template che verifichi il conto e che il GS
dichiarato resti quello chiesto.
**Accettazione**: ogni template cita la sua riga d'ancora; applicarne uno e
disfarlo torna al blocco di partenza; `fonte:` dice quale template e quanto vale
in GS reale.

---

## §10 · PROPOSTA — Lotto K: l'incontro tarato sulla composizione del gruppo

> ⚠️ **Proposta, non autorizzata.** Nasce da una domanda del DM: *«il generatore
> ha qualcosa per generare il gruppo di incontro che lavora meglio contro un
> gruppo di incantatori o guerrieri o misti? ha senso?»*

**Oggi non c'è.** `suggest_encounter` sceglie per EL, fazione e ambiente: della
composizione del party non sa niente, e nemmeno `genera_creatura`.

**Ha senso, ma con una guardia, e la guardia è metà del lotto.** Uno strumento
che *contrasta* il gruppo scrive, un incontro alla volta, il contrario di quello
che questa campagna fa: la dottrina dello **Shine Time** dice che ogni PG deve
avere la sua scena, e un incontro costruito per annullare l'incantatore è un
incontro in cui quel giocatore sta fermo. Un generatore che ottimizza contro il
party diventa design anti-giocatore per costruzione, e nessuno se ne accorge
finché non è la terza sessione di fila.

Quindi il criterio di progetto, prima del codice: **pressione, non contromisure.**

| Composizione | Cosa si propone | Cosa NON si propone |
|---|---|---|
| molti incantatori | iniziativa alta, chi chiude la distanza, un TS sulla Volontà decente, terreno che rompe le linee di tiro | *silenzio* su tutta la scena, contromagia sistematica, immunità agli incantesimi |
| molta mischia | portata, volo, terreno difficile, chi costringe a muoversi | nemici irraggiungibili per tutto lo scontro |
| misto | una minaccia per asse, sfalsate nel tempo | tutto insieme al primo round |

E una regola dura: **almeno un bersaglio su cui ogni PG ha una presa evidente**,
verificata dal tool e scritta nella proposta. Se non riesce a produrla, si
rifiuta invece di proporre l'incontro — lo stesso confine dell'adepto senza lista.

**Cosa costa.** Un profilo del gruppo (che il repo ha già in `PG/` e in
`campaign/state.md`), un punteggio di pressione per record del catalogo, e
l'innesto in `suggest_encounter` come un'opzione, non come il comportamento di
norma.
**Accettazione**: a parità di seme l'output resta riproducibile; ogni proposta
dichiara **per ogni PG** su cosa ha presa; il tool si rifiuta quando non ci
riesce.
