# PIANO — Il ciclo di sessione automatizzato, e il menu che lo guida

> **Stato**: 🔵 **pianificato** (2026-09-24). Nessun lotto eseguito; il primo
> gate è la Fase 0 (ADR e decisioni del DM). **Rev. 2** (stesso giorno): il
> metodo non è più solo TDD, ma contratto prima, nucleo puro e test a strati
> (§5.0), su domanda del DM.
>
> **Origine**: risposta del DM alla D21 di `PIANO-RIPRESA-PR-ABBANDONATE`, punti
> 7 e 8 (2026-09-24): *«non c'è un tool che è chiamato dal DM a fine sessione
> che prende le domande e genera lo state.md e la parte relativa di state.yml in
> maniera automatica?»*, poi il ciclo intero (preparazione, tavolo, chiusura) e
> *«un menu testuale con le varie parti che possono essere richiamate e che in
> background chiamano dm.py con sottocomandi ed opzioni»*, pronto per essere
> avvolto da un'interfaccia grafica.
>
> **Cosa assorbe**: il sotto-lotto **4f-5** di `PIANO-RIPRESA-PR-ABBANDONATE`
> (le proposte di fine sessione che diventano domande) diventa la Fase 1b.

---

## §1 · Cosa ho guardato prima, e cosa questo piano NON rifà

Regola di apertura (ADR-0044). Cercati «menu», «interfaccia grafica», «GUI»,
«ciclo di sessione», «preparazione» in `plans/`, e i file di ogni ramo e PR
mai arrivati su `main` (`contenuti_nei_rami.py`): **nessun piano, nessun ramo
e nessuna PR contiene un menu o un'interfaccia**. Il lavoro sul ciclo di
sessione rimasto fuori da `main` era solo quello della #99, già recuperato nel
lotto 4e.

| Piano vicino | Cosa copre, e qui NON si rifà |
|---|---|
| `PIANO-AUTOMAZIONE-STATO-SESSIONI` (🟢 ~98%) | il wizard di fine sessione, l'applicazione a regioni marcate, la visibilità per PG, il brief e il teaser, i rami per gruppo (ADR-0007). Questo piano li **chiama**, non li riscrive |
| `PIANO-RIPRESA-PR-ABBANDONATE` 4e, 4f | il delta di sessione per `png_id` (4e), il gruppo nuovo da un modulo (4f-4) |
| `PIANO-PIPELINE-IBRIDE` e ADR-0067 | il confine fra codice e modello linguistico, e il ponte (lotto E) se mai servirà. Qui si decide **solo se** usarlo nella preparazione (D3) |
| `SPEC-SERVER-MCP` | i tool esposti a un agente, con allowlist e blocco di chi scrive canone. Il menu è per il DM, non per un agente |
| `PIANO-EDITOR-VISUALE-MAPPE` | l'editor grafico delle mappe. L'interfaccia grafica del menu è un'altra cosa, e un altro piano (§6) |
| `PIANO-DM-TOOLKIT`, ADR-0013 | lo standard dei booklet e `dm.py booklet`/`volume`. Qui si genera il **manifest** di una sessione, il resto è loro |

---

## §2 · Com'è oggi, misurato (2026-09-24)

**La risposta alla domanda del DM è «in parte».** `dm.py session end` esiste
ed è la catena di fine sessione: guardia sul ramo, wizard a domande che scrive
il log, ledger XP, applicazione a `state.yaml` di ciò che è meccanico,
rigenerazione delle tabelle di `state.md`, storico, commit. Quello che **non**
fa:

| Cosa accade al tavolo | Oggi | Dove resta |
|---|---|---|
| March Clock, clock dei villain, morti e fughe | ✅ domanda del wizard → `state.yaml` → `state.md` | — |
| XP | ✅ ledger | — |
| party: stato, PF, livello di un PG | ❌ | proposta stampata, «scrivi in `state.yaml`» |
| chi dei PNG ha saputo cosa (§4) | ❌ | idem |
| alleanze e atteggiamenti | ❌ | **non è un dato**: `state.yaml` non ha una tabella; `state_sync` le riconosce nel testo e le stampa |
| un'eco nuova, o una che matura | ❌ | idem |
| un artefatto che cambia portatore | ❌ | idem |
| la cronaca (`campaign-chronicle.md`) | ❌ | a mano, nessuno strumento la tocca |
| il recap per ciascun PG | 🟡 esiste (`dm.py session recap --pg`), non è nella catena | comando separato |

Delle tre violazioni della decisione D19 («nessun YAML a mano») elencate in
`PIANO-RIPRESA-PR-ABBANDONATE` §4.10.6, due restano scritte: `dmcore/masters.py`
(nota di `DATI`) e la tabella dei tre master nella skill
`rumblingstone-automation` («`state.yaml`: **qui**, poi `render_state`»). A
queste si aggiungono le proposte stesse di `state_apply`. La terza,
`new-campaign-group.sh`, è stata chiusa da 4f-4.

**La preparazione è una lista di file da aprire** (Playbook §2, 15 minuti): lo
stato, l'ultima sessione, il file d'arco, le schede dei PNG. Gli strumenti
esistono ma nessuno li mette in fila:

| Passo di preparazione | Strumento che c'è | Cosa manca |
|---|---|---|
| lo stato è coerente e aggiornato? | `validate_state`, `render_state --check`, `dm.py doctor`, `dm.py session status` | nessuno li chiama insieme |
| cosa succede la prossima volta | `dm.py session next`: brief DM e teaser giocatori dagli hook, dalle finestre di giorni, dai clock | **non legge gli echi** (`state.yaml` §7.E) |
| incontri, mappa, tesoro | `dm.py prep --el --env` | — |
| le mappe delle scene | `render_map_svg`, `export_uvtt`, `validate_maps` | nessuno sa **quali** mappe servono alla prossima sessione |
| le illustrazioni | `dm.py prompts` (i prompt), `comfyui_batch.py` (la generazione, sulla macchina del DM) | idem, e manca il controllo «c'è già?» |
| gli handout che i PG possono trovare | `dm.py handout`, i booklet | nessun indice degli handout di una sessione |
| cosa sa ciascun PG | `dm.py session recap --pg` (con la visibilità degli split) | — |
| il booklet del DM e dei giocatori | `dm.py booklet`, `dm.py volume` | i manifest sono scritti a mano, uno per sessione (quattro in ARC-07) |
| le interazioni dei PNG, il testo degli handout | nessuno | è **prosa di gioco**: oggi la scrive il DM o una sessione di agente con le skill |

`dm.py` ha **15 sottocomandi** e nessun menu. Il repo ha **67 script** in
`scripts/`, **1.307 test**, e un server MCP che espone 71 tool con allowlist.

---

## §3 · L'ordine logico del ciclo, verificato

L'ordine proposto dal DM è quasi giusto. Tre correzioni, e un passo che manca.

```
            ┌──────────────────────────────────────────────────────────┐
            ▼                                                          │
  [A] CONTROLLO ─▶ [B] TURNO DEL MONDO ─▶ [C] SCELTA DELLE SCENE ─▶ [D] MATERIALI
  lo stato è        i villain avanzano      cosa si giocherà          mappe, immagini,
  chiuso e          fuori scena             (brief + scelta DM)       handout, statblock:
  coerente?         (clock, agende)                                   ci sono? si fanno
                                                                           │
  [H] CHIUSURA ◀── [G] TAVOLO ◀── [F] BOOKLET ◀── [E] COSA SANNO I PG ◀───┘
  log a domande,    si gioca        DM e giocatori   recap per PG, echi da
  stato, cronaca,                                    far riemergere, teaser
  recap, commit                                      senza spoiler
```

1. **Prima si sceglie cosa si giocherà, poi si preparano i materiali.** Nella
   proposta del DM la generazione di illustrazioni e mappe viene prima: senza
   sapere quali scene arrivano, si preparano i materiali di tutto l'arco.
2. **Il ciclo comincia dal controllo della chiusura precedente.** Se l'ultima
   sessione non è stata chiusa (log mancante, stato non allineato, commit non
   fatto), tutto ciò che si prepara parte da uno stato falso.
3. **«Echi per DM e PG» sono due cose in due momenti.** Cosa sa ciascun PG
   viene dal log e si produce alla chiusura (il Playbook §4.6 lo manda ai
   giocatori uno o due giorni prima). Quali echi far riemergere al tavolo è
   preparazione, e legge `state.yaml`.
4. **Manca il turno del mondo.** Fra una sessione e l'altra i villain agiscono:
   è la regola del mondo vivo di `rumblingstone-narrative-style`. La parte
   meccanica (un clock che arriva al suo trigger) si calcola; la parte di
   giudizio (l'agenda che fa un passo) è una domanda al DM, una per villain
   vicino alla soglia.

La chiusura, nell'ordine: log a domande → XP → stato (meccanico e, dopo la
Fase 1, anche il resto) → cronaca → recap per PG → commit e push sul ramo del
gruppo. È l'ordine che `dm.py session end` segue già, allungato.

---

## §4 · PRD

### Attori

| Attore | Cosa fa | Cosa non fa mai |
|---|---|---|
| **DM** | risponde a domande, sceglie da elenchi, approva | aprire un file YAML (D19) |
| **Giocatori** | ricevono teaser, recap per PG, handout, booklet | vedere qualcosa che il loro PG non sa |
| **Menu** | mette in fila i comandi e passa le risposte | contenere logica: ogni voce è una chiamata a `dm.py` |
| **Sessione di agente** (opzionale) | scrive prosa di gioco su richiesta, con le skill | scrivere canone senza la conferma del DM |

### Storie, con il criterio d'accettazione

| # | Dato che… | quando il DM… | allora… |
|---|---|---|---|
| U1 | una sessione è finita | lancia «Chiudi la sessione» dal menu | risponde solo a domande; `state.yaml`, `state.md`, lo storico e la cronaca sono aggiornati e committati; **nessuna proposta dice «scrivi in state.yaml»** |
| U2 | un PG è morto, un PNG ha scoperto un segreto, Dauth è diventata ostile | risponde alle domande della chiusura | le tre cose sono dati validati, con il `png_id` risolto mentre risponde |
| U3 | la sessione precedente è chiusa | lancia «Prepara la prossima» | vede lo stato, i clock, gli echi da far riemergere e le domande del turno del mondo, e sceglie le scene |
| U4 | ha scelto le scene | continua | vede per ogni scena cosa c'è (mappa, UVTT, immagini, handout, statblock) e cosa manca; quello che si genera da solo si genera |
| U5 | mancano interazioni di PNG o il testo di un handout | continua | riceve un **brief di scrittura** con i fatti che il testo deve rispettare; il testo non viene inventato dal codice (D3) |
| U6 | i materiali ci sono | chiede i booklet | escono il booklet del DM e quello dei giocatori per le scene scelte, dal manifest generato |
| U7 | un'interfaccia grafica vuole disegnare il menu | chiama `dm.py menu --json` | riceve le voci, e per ogni modulo le domande in JSON; stdout contiene solo dati |

### Requisiti non funzionali

- **Solo libreria standard** negli script (ADR-0037); pyyaml resta il debito
  dichiarato che è.
- **Offline**, sul portatile del DM, la sera della sessione.
- **Deterministico e idempotente**: rilanciare un passo non duplica niente.
- **Ogni modulo interattivo ha il suo gemello non interattivo**: `--domande`
  stampa il modulo in JSON, `--answers` lo riceve. È il contratto per
  l'interfaccia e per i test.
- **stdout è dei dati, stderr dei messaggi** (dal 4f-4 anche `dm.py`).
- **Tutto o niente** nelle scritture di canone, e il triplo vincolo di ADR-0007
  resta: ramo del gruppo, conferma del DM, regioni marcate.
- **Tempi**: chiusura in 10 minuti, preparazione in 15, cioè i tempi che il
  Playbook già promette e che oggi dipendono dalla disciplina.

### Non-obiettivi

- Un modello linguistico nel percorso critico. Se la D3 lo introduce, lo fa
  come passo opzionale che produce una bozza, mai canone.
- L'interfaccia grafica: il menu è testuale e pronto a essere avvolto (§6).
- Scrivere canone su `main`.

---

## §5 · Lotti

Ogni lotto dichiara engine, effort e qualità (ADR-0045).

### §5.0 · Il metodo: contratto prima, nucleo puro, test a strati

Rivisto il 2026-09-24 su domanda del DM: *«c'è un modo migliore del TDD per
gestire agilmente aggiunte e modifiche future?»*. Il TDD da solo non basta,
perché decide come si scrive il codice e non come il sistema regge i
cambiamenti. Quello che rende facile aggiungere una domanda al modulo, una voce
al menu o un'interfaccia grafica sono le scelte qui sotto; il TDD resta, nel
posto dove rende.

**1 · Il contratto prima del codice.** Per ogni modulo, per il menu e per ogni
comando nuovo si scrive e si committa prima il contratto: lo schema JSON delle
domande e delle risposte, le voci del menu, gli exit code nel manifest. Il
codice e la futura interfaccia dipendono dal contratto, non l'uno dall'altra. È
la forma che il repo usa già per i tool (ADR-0012) e per `state.yaml`.

**2 · Contratti versionati, e solo additivi.** Ogni JSON porta un campo
`versione`. Una modifica aggiunge campi e non cambia il significato di quelli
che ci sono; chi legge ignora i campi che non conosce. Un cambiamento
incompatibile è una versione nuova, e per un periodo le due convivono. È ciò
che permette di aggiungere una domanda al modulo senza rompere l'interfaccia
grafica che lo disegna.

**3 · Nucleo puro, guscio sottile.** Le decisioni stanno in funzioni pure sotto
`dmcore/` (dati in entrata, dati in uscita); disco, git e terminale stanno negli
script. È la forma minima dell'architettura esagonale, ed è già quella di 4f-4:
`dmcore/gruppo_nuovo.py` decide, `gruppo_nuovo.py` scrive. Il nucleo si prova
senza git e senza tastiera, e un'interfaccia nuova è soltanto un altro guscio.

**4 · Test a strati, ognuno dove rende.**

| Cosa si prova | Tecnica | Perché questa |
|---|---|---|
| la logica del nucleo | **TDD**, il test prima del codice | il contratto è chiaro e il riscontro arriva in secondi |
| un flusso intero (U1-U7) | **test d'accettazione** scritti dalle storie di §4, su una copia del repo sotto git | provano quello che vede il DM, non l'implementazione |
| il JSON fra `dm.py` e un'interfaccia | **test di contratto**: lo schema valida gli esempi nelle due direzioni | `dm.py` e l'interfaccia possono cambiare separati |
| i file generati (`state.md`, manifest, booklet) | **test d'approvazione**: l'uscita si confronta con una già approvata, che si rigenera solo in un commit suo | è già la regola dell'impronta delle creature e degli SVG byte-identici |
| le invarianti (rilanciare non duplica, tutto o niente) | **proprietà** su input generati | trovano i casi che nessuno ha scritto. ⚠️ Senza librerie (ADR-0037): pochi generatori scritti a mano, mirati |
| i test stessi | **mutazioni** | la convenzione del repo: un test che non si è mai visto fallire non conta |

**5 · Le regole dell'architettura diventano controlli.** Ciò che il progetto
deve mantenere nel tempo si controlla in CI a ogni PR: nessuna logica nel menu
(ogni voce è una riga di `dm.py`), stdout solo per i dati, nessuna proposta che
dica «scrivi in `state.yaml`». Nell'architettura evolutiva si chiamano
*funzioni di fitness*; la CI del repo ne esegue già 22 (`validate_docs`,
`check_plans_discipline`, `decisioni_dm --check`…).

**6 · Dove il TDD non serve.** Il menu si prova prima a mano, perché la forma
giusta si scopre usandolo, e poi si fissa con un test d'approvazione. La prosa
di gioco non si progetta con i test: si misura con `misura_craft` e con la
self-check di `rumblingstone-narrative-style`.

### Fase 0 · Le decisioni prima del codice

#### ⬜ 0a · ADR-0068, il menu è un guscio e ogni modulo ha un gemello in JSON
`[engine: Opus 5.5, sessione principale · effort: alto · qualità: il DM la legge e riconosce il proprio problema]`

Estratta dalla bozza di §7. Classe **G**.

#### ⬜ 0c · I contratti, prima del codice
`[engine: Sonnet 5 · effort: medio · qualità: gli esempi del modulo di 4f-4 e del wizard passano lo schema; un esempio con un campo in più passa, uno con un campo cambiato no]`

Classe **C**. Tre schemi JSON versionati in `scripts/schemas/`: il modulo (le
domande), le risposte, il menu. Il modulo di `dm.py gruppo nuovo` è il primo
esempio vero, perché esiste già (§5.0, punti 1 e 2).

#### ⬜ 0b · Le risposte del DM a D1-D5
`[engine: DM · effort: — · qualità: le cinque righe barrate in §8]`

### Fase 1 · La chiusura che non lascia niente a mano

#### ⬜ 1a · Un motore di moduli, uno solo
`[engine: Sonnet 5 · effort: medio · qualità: il wizard e dm.py gruppo nuovo passano i loro test invariati sopra il motore nuovo]`

Classe **C**. `dmcore/modulo.py`: un modulo è un dato (campi di tipo testo,
scelta, intero, elenco, riga da decidere); il motore lo presenta in terminale e
restituisce il JSON delle risposte. Oggi il wizard e `gruppo_nuovo.py` hanno due
presentazioni scritte a mano: si portano sopra il motore, e i loro test sono il
collaudo del refactoring.

#### ⬜ 1b · Le proposte diventano domande (ex 4f-5)
`[engine: Sonnet 5 · effort: alto · qualità: nessuna riga di state_apply stampa più «scrivi in state.yaml»; mutazioni sul delta rosse]`

Classe **C**, dopo D2. Il delta di sessione (`dmcore/delta_sessione.py`) si
allarga a party (stato, PF, livello), conoscenze (`png_id`, che cosa, come),
echi (nuovi e maturati), portatore degli artefatti e, se la D2 dice sì,
alleanze. Ogni domanda offre i valori possibili presi dallo stato; tutto si
applica tutto o niente, come il delta di 4e. Chiude ciò che di D19 resta
violato (§2).

#### ⬜ 1c · La cronaca si aggiorna da sola
`[engine: Sonnet 5 · effort: medio · qualità: rilanciare la chiusura non duplica la voce; la regione è l'unica parte toccata]`

Classe **C**, dopo D1. Dal log (Summary e Key decisions) una voce nella
cronaca, dentro una regione marcata come quelle di `state.md`.

#### ⬜ 1d · La catena di chiusura completa
`[engine: Sonnet 5 · effort: medio · qualità: test d'accettazione U1 e U2 su una copia del repo]`

Classe **C**. `dm.py session end` aggiunge alla catena la cronaca e i recap per
PG. Il Playbook §4 si riscrive attorno a un comando.

### Fase 2 · La preparazione in fila

#### ⬜ 2a · Il controllo e il turno del mondo
`[engine: Sonnet 5 · effort: medio · qualità: una sessione non chiusa blocca la preparazione con il motivo; test U3]`

Classe **C**. `dm.py session prep`: controlla che la chiusura precedente sia
completa, mostra lo stato in breve, gli echi da far riemergere (il brief oggi
non li legge) e fa le domande del turno del mondo, una per villain vicino alla
soglia del clock.

#### ⬜ 2b · Da una scena ai suoi materiali: ricognizione
`[engine: subagente Explore · effort: medio · qualità: i numeri si riproducono con un comando]`

Classe **R**. Prima di scrivere lo strumento di 2c si misura se il legame fra
una scena e i suoi materiali **è già scritto** nei master d'arco (link alle
mappe, ai prompt, alle schede, agli handout) e in che forma. Se non lo è, 2c
cambia natura: non si cerca, si dichiara.

#### ⬜ 2c · L'inventario dei materiali delle scene scelte
`[engine: Sonnet 5 · effort: alto · qualità: su ARC-07 l'inventario coincide con i quattro manifest scritti a mano]`

Classe **C**. Il DM sceglie le scene dal brief; lo strumento elenca per ognuna
mappa, UVTT, immagini, handout e statblock, dice cosa c'è e cosa manca, e
lancia ciò che si genera da solo (render delle mappe, export UVTT, build dei
booklet; le immagini solo sulla macchina del DM con ComfyUI). Il collaudo usa
i manifest di ARC-07 come verità nota.

#### ⬜ 2d · Il brief di scrittura per ciò che è prosa
`[engine: Opus 5.5 · effort: alto · qualità: il DM usa il brief senza riaprire i file che cita]`

Classe **G**, dopo D3. Per le interazioni dei PNG e il testo degli handout che
mancano, un brief con i fatti da rispettare (chi sa cosa, cosa è successo, i
nomi, le soglie del read-aloud). Il testo lo scrive il DM, o una sessione di
agente con `rumblingstone-narrative-style`; se la D3 dice sì, il ponte di
ADR-0067 ne fa una bozza.

#### ⬜ 2e · Il manifest della sessione
`[engine: Sonnet 5 · effort: medio · qualità: validate_booklets verde; il booklet dei giocatori non contiene niente di marcato DM]`

Classe **C**. Il manifest del booklet del DM e di quello dei giocatori si
genera dalle scene scelte; poi `dm.py booklet` o `dm.py volume`.

### Fase 3 · Il menu

#### ⬜ 3a · `dm.py menu`, testuale
`[engine: Sonnet 5 · effort: medio · qualità: ogni voce produce la stessa riga di comando del manuale; test con risposte su stdin]`

Classe **C**, dopo 0a e D4. Un menu a numeri, per fase: *Prepara*, *Chiudi*,
*Gruppo*, *Stampa*, *Strumenti*. Le voci sono un dato (`dmcore/menu.py`): per
ognuna la riga di `dm.py` e, se serve, il modulo da riempire. Il menu non ha
logica sua; chiama `dm.py` e mostra l'uscita.

#### ⬜ 3b · `dm.py menu --json`
`[engine: Sonnet 5 · effort: basso · qualità: un test disegna il menu dal JSON e lo confronta con quello testuale]`

Classe **C**. Le voci, i moduli e i comandi in JSON, per un'interfaccia.

### Fase 4 · Collaudo al tavolo

#### ⬜ 4a · Un ciclo intero con una sessione vera
`[engine: DM al tavolo, poi Opus 5.5 per le correzioni · effort: alto · qualità: tempi misurati contro i 10 e 15 minuti del Playbook; scheda di feedback]`

Classe **G**, con `rumblingstone-playtest`. Il ramo del gruppo, una sessione,
il menu dall'inizio alla fine; si cronometra ogni fase.

---

## §6 · L'interfaccia grafica, dopo

Fuori da questo piano. Quando arriverà, le due forme candidate sono una
**pagina locale** servita da `http.server` della libreria standard, che legge
`dm.py menu --json` e i moduli in JSON, e un'interfaccia desktop. Tutte e due
funzionano solo se la Fase 3 rispetta il contratto: nessuna logica nel menu, i
moduli come dati, stdout pulito. Per questo il contratto si scrive adesso.

---

## §7 · Bozza di ADR-0068 (da estrarre in 0a)

**Contesto.** Il DM non scrive YAML (D19) e vuole un menu che un'interfaccia
grafica possa avvolgere. Oggi ogni modulo interattivo presenta le sue domande
a modo suo, e `dm.py` scriveva i suoi messaggi su stdout.

**Decisione.**

1. `dm.py` resta l'unico ingresso (ADR-0002). Il menu è un guscio: ogni voce è
   una riga di comando di `dm.py`, e il menu non decide niente.
2. Ogni modulo interattivo ha un gemello non interattivo: `--domande` stampa il
   modulo in JSON, `--answers` riceve le risposte in JSON. La presentazione in
   terminale è una delle presentazioni possibili dello stesso dato.
3. stdout è dei dati, stderr dei messaggi. Gli exit code sono dichiarati nel
   manifest dei tool.
4. Il codice mette in fila, controlla e scrive dati. La prosa di gioco la
   scrivono il DM o un agente con le skill; il codice prepara il brief (D3).
5. I contratti JSON portano una versione e cambiano solo aggiungendo; chi li
   legge ignora ciò che non conosce.
6. Le decisioni stanno in funzioni pure sotto `dmcore/`; gli script sono il
   guscio che legge, scrive e parla col DM.

**Le conseguenze.** Si paga un refactoring (1a) e la disciplina di non mettere
logica nel menu. Si guadagna un'interfaccia grafica che non riscrive niente, e
test che non hanno bisogno di una tastiera.

---

## §8 · Decisioni aperte

<!-- decisioni-dm: CICLO-SESSIONE -->

| # | Fase | Domanda |
|---|---|---|
| D1 | F1 · 1c | **La cronaca si aggiorna da sola?** La chiusura aggiungerebbe una voce costruita dal log (Summary e Key decisions) in una regione marcata di `campaign-chronicle.md`. Oggi il vincolo 3 di ADR-0007 ammette scritture automatiche solo nelle regioni `auto:` di `state.md`: dire sì vuol dire estenderlo alla cronaca. Proposta: sì, in una regione marcata in coda |
| D2 | F1 · 1b | **Le alleanze diventano un dato?** Oggi non esistono in `state.yaml`: `state_sync` le riconosce nel testo del log (Dauth, Rethmar, Starsong, i druidi…) e le stampa. Per farne una domanda serve una tabella nuova (fazione, atteggiamento SRD, nota). È canone: i valori di partenza li scegli tu. Proposta: sì, con gli atteggiamenti SRD (ostile … amichevole) |
| D3 | F2 · 2d | **Chi scrive la prosa di gioco che manca** (interazioni dei PNG, testo degli handout, echi)? (a) il DM, o una sessione di agente con le skill, partendo dal brief; (b) una bozza del ponte di ADR-0067, che riapre il lotto E-bis escluso il 2026-07-20. Proposta: (a) adesso, (b) da rivalutare dopo il collaudo |
| D4 | F3 · 3a | **Che menu?** Numerato in testo semplice (libreria standard, funziona ovunque e si avvolge facilmente) oppure a schermo intero con `curses` (che su Windows non c'è). Proposta: numerato |
| D5 | F2 · 2c | **Le immagini mancanti si generano durante la preparazione?** Serve ComfyUI sulla macchina del DM e minuti per immagine. Proposta: la preparazione le **elenca** e lancia `comfyui_batch` solo se il DM lo chiede |

---

## §9 · Rischi

| Rischio | Probabilità | Mitigazione |
|---|---|---|
| Il delta allargato scrive canone sbagliato | media | tutto o niente, validazione mentre il DM risponde (come 4e), mutazioni |
| Il legame scena → materiali non esiste nei master (2b) | alta | 2b è una ricognizione proprio per saperlo prima; se manca, 2c chiede al DM di dichiararlo una volta per scena |
| Il menu accumula logica «per comodità» | media | ADR-0068 punto 1, e un test che confronta ogni voce con la riga di comando del manuale |
| La preparazione dura più di 15 minuti | media | si misura in 4a; ciò che è lento (immagini) è opzionale (D5) |

## Checklist di avanzamento

- ⬜ Fase 0 · 0a ADR-0068 · 0c i contratti versionati · 0b risposte a D1-D5
- ⬜ Fase 1 · 1a motore dei moduli · 1b proposte → domande (ex 4f-5) · 1c cronaca · 1d catena di chiusura
- ⬜ Fase 2 · 2a controllo e turno del mondo · 2b ricognizione · 2c inventario · 2d brief di scrittura · 2e manifest
- ⬜ Fase 3 · 3a menu testuale · 3b menu in JSON
- ⬜ Fase 4 · 4a collaudo al tavolo
