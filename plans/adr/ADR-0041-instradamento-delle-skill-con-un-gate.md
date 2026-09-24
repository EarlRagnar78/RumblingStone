# ADR-0041 — L'instradamento delle skill è un principio, e un gate lo verifica

- **Stato**: accettata
- **Data**: 2026-09-04
- **Decisori**: DM (Gianfranco Samuele), agente
- **Sostituisce**: nulla — formalizza una regola che `AGENTS.md` dava per
  implicita e che non reggeva alla prova dei fatti
- **Origine**: PR #109 (analisi), domanda del DM «le modifiche sono valide?»

## Contesto

`AGENTS.md` §Skills apriva con questa frase:

> *AI agents that support SKILL.md will discover them automatically.*

È falsa in due sensi diversi, e vale la pena separarli perché portano a rimedi
diversi.

**Primo senso — tecnico.** Nessuno degli agenti che questo repo serve carica
diciotto `SKILL.md` all'inizio di una conversazione. Alcuni leggono le
descrizioni del frontmatter e decidono; altri caricano solo ciò che il prompt
di sistema elenca; altri ancora non hanno alcun meccanismo di scoperta e
vedono le skill solo se un documento gliele nomina. La frase descriveva un
comportamento che nessun agente ha.

**Secondo senso — misurabile, e più grave.** L'elenco sotto la frase conteneva
**tredici** voci a fronte di **diciotto** directory con un `SKILL.md`. Le cinque
mancanti — `rumblingstone-editoria`, `rumblingstone-edizione`,
`rumblingstone-indagine`, `rumblingstone-module-standard`,
`rumblingstone-prosa-documenti` — sono tutte skill nate *dopo* l'ultima
riscrittura della sezione. Nessuna di loro è mai stata rimossa: semplicemente
non è mai stata aggiunta. Un agente che si fosse fidato di quell'elenco avrebbe
impaginato un booklet senza `editoria`, pubblicato senza il gate d'uscita di
`edizione`, e scritto un ADR con le regole della prosa di gioco.

La causa è strutturale, non di disattenzione: **l'elenco era una lista, e una
lista non ha un invariante**. Aggiungere una skill e dimenticare la riga non
rompe niente, non fallisce nessun test, e il buco si vede solo quando qualcuno
va a contare. Nessuno va a contare.

C'è anche un difetto di forma. L'elenco era organizzato **per artefatto** — una
riga per directory — mentre chi legge non arriva con una directory in mano:
arriva con un compito. «Devo scrivere il read-aloud di una scena» non si mappa
su `rumblingstone-narrative-style` finché non hai già letto la descrizione di
tutte e diciotto.

## Decisione

### 1. Il principio prima, gli esempi dopo

`AGENTS.md` §Skills apre con **la regola di instradamento** enunciata come
principio, e solo dopo mostra la tabella. Il principio è:

> Prima di produrre qualunque cosa, chiediti **chi la leggerà e in che forma
> uscirà**. Quelle due risposte, non l'argomento, scelgono la skill.

La tabella che segue **illustra** il principio su un compito alla volta; non
pretende di esaurirlo. È la differenza pratica fra le due forme: se un compito
nuovo non è in tabella, con una lista sei fermo, con un principio hai comunque
la domanda da farti. Un'omissione diventa un caso non ancora illustrato invece
che un buco.

Alla tabella per compito segue l'**inventario completo** — una riga per skill,
con quello che la skill è. L'inventario risponde a «cosa c'è», la tabella a
«cosa carico adesso». Sono due domande diverse e stavano in un elenco solo.

### 2. Il gate

`scripts/validate_skills.py` acquisisce un quarto controllo, **bloccante**:

> Ogni directory `skills/<nome>/` che contenga un `SKILL.md` deve essere citata
> in `AGENTS.md`, e ogni percorso `skills/<nome>/` citato in `AGENTS.md` deve
> esistere.

Il controllo è bidirezionale di proposito. La direzione *skill → documento*
prende l'omissione (il difetto che si è verificato). La direzione
*documento → skill* prende il residuo: una skill rinominata o rimossa lascia in
`AGENTS.md` un puntatore che manda l'agente su un file inesistente — lo stesso
guasto che il lotto G2 di PR #99 aveva trovato su `campaign/npcs/` e
`rhod-adaptations.md`, cartelle documentate e mai esistite.

Il gate **non giudica il testo**. Non può dire se la riga descrive bene la
skill, se sta nella tabella giusta, o se il principio è stato applicato. Sa
contare, e conta la sola cosa che si è rotta davvero.

### 3. L'obbligo

Il DM ha chiesto esplicitamente che il routing sia **un obbligo, non un
suggerimento**, e che ci sia un gate a verificarlo. L'obbligo vive nella
prosa di `AGENTS.md` («MUST load»); il gate verifica la **completezza
dell'elenco**, che è il presupposto senza cui l'obbligo non è nemmeno
esigibile: non si può pretendere che un agente carichi una skill di cui il
documento non gli ha mai detto l'esistenza.

## Conseguenze

**Positive.**

- Aggiungere una skill senza instradarla **fa fallire la CI**. Il difetto che
  ha prodotto cinque omissioni in sequenza non è più possibile.
- Rimuovere o rinominare una skill senza aggiornare `AGENTS.md` fa fallire la
  CI. Nessun puntatore morto.
- Chi arriva con un compito trova la riga che gli serve senza leggere diciotto
  descrizioni.

**Negative, e vanno dette.**

- Il gate crea **attrito** su ogni nuova skill: un secondo file da toccare
  nello stesso commit. È il prezzo dell'invariante, ed è lo stesso prezzo che
  la regola d'oro dei piani già fa pagare su `INDEX.md` e `CHANGELOG.md`.
- Il gate **non protegge dalla riga sbagliata**. Una skill citata con una
  descrizione errata, o messa nella riga di compito sbagliata, passa. Chi
  legge questo ADR fra sei mesi non deve dedurne che la sezione è verificata:
  è *completa*, che è meno.
- Il principio «chi legge e in che forma esce» è una **euristica**, non un
  algoritmo. Ci sono compiti in cui le due risposte puntano a skill diverse
  (un handout è player-facing *e* impaginato: vuole `narrative-style` **e**
  `editoria`). La tabella lo dice caso per caso; il principio da solo non lo
  risolve.

## Alternative scartate

**Un solo elenco alfabetico, senza tabella per compito.** È lo stato di
partenza. Costa meno da mantenere e non risolve il problema di chi arriva con
un compito.

**Generare la sezione da un template a partire dai frontmatter.** Toglie
l'attrito e toglie anche il giudizio: il frontmatter di una skill è scritto
per l'agente che deve decidere se caricarla, non per il DM che vuole capire
cosa c'è nel repo. Una sezione generata sarebbe stata più lunga, più uniforme
e meno utile. Il gate verifica la copertura senza scrivere il testo al posto
di nessuno — che è la divisione giusta fra ciò che una macchina sa fare e ciò
che no.

**Un warning invece di un errore.** Scartata per la regola già scritta in
PR #99: *nessun gate nuovo nasce non bloccante*. Un warning su un file che
nessuno legge in CI è un modo elaborato di non fare niente.
