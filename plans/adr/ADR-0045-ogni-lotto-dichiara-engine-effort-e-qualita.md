# ADR-0045 — Ogni lotto dichiara engine, effort e qualità attesa

- **Stato**: accettata
- **Data**: 2026-09-04
- **Decisori**: DM (Gianfranco Samuele), agente
- **Origine**: richiesta DM — *«ogni piano fatto o esistente dividilo in lotti
  divisi per engine ed effort e qualità di risultato, in modo da massimizzare il
  throughput dei token e massimizzare il risultato e la qualità finale»*
- **Estende** [ADR-0044](ADR-0044-prima-si-guardano-i-piani-che-ci-sono.md), che
  dice *quando* si apre un piano. Questo dice *come si tagliano i suoi lotti*.

## Contesto

### La richiesta contiene una tensione, e va detta

**Massimizzare il throughput dei token e massimizzare la qualità sono due
obiettivi che tirano in direzioni opposte.** Questa ADR non li ottimizza
entrambi: rende **esplicito il compromesso lotto per lotto**, che è una cosa
diversa e onesta. Un lotto che dichiara *«qui pago, perché se sbaglio il DM se ne
accorge al tavolo»* e uno che dichiara *«qui risparmio, perché un gate mi dice se
è giusto»* sono decisioni consapevoli; oggi non lo erano né l'una né l'altra.

### Come si lavorava prima

Ogni lotto girava allo stesso modo: sessione principale, modello di default,
sforzo massimo, indipendentemente dal fatto che si trattasse di **riscrivere un
eco di canone** o di **rigenerare diciassette SVG**. Nella tornata del
2026-09-04 le due cose sono successe nello stesso commit, con lo stesso
apparato.

### L'avvertenza che ribalta l'ordine delle leve

La documentazione dell'API dice una cosa che cambia il disegno:

> Prima di costruire una cascata multi-modello, misura l'alternativa più
> semplice: **il modello più capace a effort più basso** sugli stessi compiti.
> Le cache sono **legate al modello**, quindi una cascata rinuncia al riuso della
> cache fra i suoi modelli.

E una seconda:

> Giudica il **costo per compito completato**, non per richiesta. Una richiesta
> più economica che ha bisogno di più giri o di ritentativi per finire il lavoro
> non è più economica.

Quindi **l'engine non è la prima leva**. La prima è l'**effort dentro un modello
solo**, che non spezza la cache. La seconda è l'engine, e solo dove la classe di
lavoro è davvero diversa.

## Decisione

Ogni lotto **ancora da fare** dichiara tre cose in intestazione:

```
[engine: <chi lo esegue> · effort: <basso|medio|alto|xhigh|max> · qualità: <come si sa che è finito>]
```

### Le cinque classi di lavoro

Tarate su lotti realmente eseguiti in questo repo, non in astratto.

| Classe | Che cos'è | Esempi veri | Engine | Effort | Qualità |
|---|---|---|---|---|---|
| **M · Meccanico** | Trasformazione verificabile: il risultato è giusto o sbagliato e **un gate lo dice** | rigenerare 17 SVG · rinominare per la slug corretta · propagare una correzione già decisa | inline, oppure `Haiku 4.5` in subagente | **basso** | il gate passa |
| **R · Ricognizione** | Leggere molto, riferire poco. Nessuna decisione | contare 8.216 celle in 24 file · trovare i master senza SVG · misurare i muri prima e dopo | subagente `Explore`, `Sonnet 5` | **basso-medio** | i numeri si **riproducono** rieseguendo il comando |
| **C · Costruzione** | Scrivere codice con un contratto chiaro e dei test | il gate di ADR-0041 · `check_masters_senza_svg` · un validatore nuovo | `Sonnet 5` | **medio-alto** | test che provano il gate **mordere**, non solo passare |
| **G · Giudizio** | Decidere che cosa è vero, che cosa si butta, che cosa si sovrappone | giudicare cinque PR · scrivere un ADR · decidere se un piano è nuovo | **`Opus 5`, sessione principale** | **alto-xhigh** | il DM lo legge e riconosce il proprio problema |
| **K · Canone** | Tocca la verità della campagna | il Peso a Thorik · riscrivere un eco · ridisegnare una griglia giocata | **`Opus 5`, mai delegato** | **xhigh-max** | conferma esplicita del DM |

### Come si sceglie la classe: tre domande, non cinque esempi

La tabella qui sopra **illustra**; queste tre domande **decidono**. È la lezione
di ADR-0041 applicata qui: con soli esempi, un lotto non previsto è un buco; con
un principio davanti, è un caso non ancora illustrato.

**Si risponde nell'ordine, e la prima che scatta assegna la classe.**

| | Domanda | Se sì |
|---|---|---|
| 1 | **Se sbaglio, se ne accorge il DM al tavolo?** | **K** — canone. Nessun gate difende il canone: solo il DM sa se al tavolo è andata così |
| 2 | **Devo decidere qualcosa che una macchina non può contare?** *(cosa è vero, cosa si butta, cosa si sovrappone)* | **G** — giudizio |
| 3 | **Il risultato è definito da un contratto verificabile?** *(un test che boccia il caso sbagliato)* | **C** se il contratto va **scritto**, **M** se esiste già |
| 4 | *(nessuna delle precedenti)* Sto solo **leggendo per riferire**? | **R** — ricognizione |

La domanda 1 viene prima di tutte di proposito. Un lotto sul canone che sembra
meccanico — *«sostituisci Tordek con Thorik in dodici file»* — **non lo è**: la
correzione del 2026-08-06 sembrava un `sed` ed era la riscrittura di un eco.

⚠️ **Nessuna delle quattro domande chiede quanto è grande il lotto.** La
dimensione non entra nella classificazione, ed è il punto in cui l'istinto
sbaglia più spesso.

### Il registro, che è come la tabella smette di essere tarata a occhio

La debolezza dichiarata di questa ADR è che le cinque classi sono **un'ipotesi**.
Il rimedio non è misurare adesso — non c'è un corpus — ma **accumulare le
prove mentre si lavora**, che è quello che nessuna delle regole precedenti
faceva.

Ogni lotto chiuso aggiunge una riga a **`plans/REGISTRO-LOTTI.md`**:

| Data | Lotto | Classe prevista | Engine usato | Ha retto? | Che cosa ha insegnato |
|---|---|---|---|---|---|

La colonna che conta è **«ha retto?»**: si è dovuto salire di classe a metà
strada, o il lotto è finito con l'engine e l'effort dichiarati? Tre righe non
dicono niente; trenta cominciano a dire se la tabella è tarata bene, e **quali
righe sono tarate male**.

⚠️ **Il registro non è un gate.** Nessuno lo controlla, come per ADR-0044 — è un
quaderno, e un quaderno lo tiene chi vuole tenerlo. Ma senza di lui questa ADR
resta un'ipotesi per sempre, ed è l'unica differenza fra una regola che impara e
una che invecchia.

### Le quattro regole che governano la tabella

1. **L'effort si abbassa prima dell'engine.** Un modello capace a effort basso
   spesso batte un modello inferiore a effort alto, e **non spezza la cache**.
   Cambiare engine dentro un piano è la seconda leva, non la prima.
2. **Un lotto sale di classe, mai scende.** Nel dubbio fra M e C si sceglie C;
   fra G e K si sceglie K. Il costo di un lotto sovradimensionato sono token; il
   costo di uno sottodimensionato è un errore che arriva al tavolo.
3. **La colonna «qualità» non è un lever: è il collaudo.** Dice come si sa che il
   lotto è finito. Se non si riesce a scriverla, il lotto è tagliato male e va
   ritagliato prima di eseguirlo — ed è il vero guadagno di questa ADR, più del
   risparmio di token.
4. **Un lotto che lavora su un insieme dichiara da dove conta l'insieme.**
   Vale per **G** e per **R**: se il lotto è *«giudica le PR aperte»*, *«conta i
   piani»*, *«verifica le skill»*, la colonna «qualità» deve contenere anche il
   **comando che enumera** — l'API, un `ls`, un `grep` — e non «le ho guardate
   tutte». La completezza è l'unica parte di un lotto **G** che una macchina sa
   controllare, e va tolta al giudizio.

⚠️ **La quarta regola nasce da un fallimento di questa ADR stessa**, ed è la
prima riga del registro che dice qualcosa sul metodo invece che sulle classi.
Il lotto **R5** — *«giudicare cinque PR»*, l'esempio di **G** che sta nella
tabella qui sopra — è stato eseguito su `Opus 5` in sessione principale, ha
soddisfatto il suo criterio di qualità (*«il DM lo legge e riconosce il proprio
problema»*) **ed era incompleto**: le PR aperte erano sei, e la #67 non ha avuto
nessun verdetto. Il criterio di **G** è soggettivo per costruzione, quindi
**non può accorgersi di un'assenza**: si può leggere una lista di cinque
verdetti, riconoscere il proprio problema in tutti e cinque, e non sapere che
manca il sesto. Un `list_pull_requests --state open` nella colonna «qualità»
l'avrebbe preso in due secondi.

È la stessa lezione di [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md),
dove un elenco scritto a mano diceva 13 skill su 18, e la stessa del quarto
lotto del registro (*un lotto R restituisce un numero, e il numero va ancora
letto*). La forma ricorrente è una sola: **quello che si conta a memoria si
conta male, e la parte contabile di un lavoro di giudizio non è giudizio.**

### Dove si taglia un lotto

Il taglio segue la **classe**, non la dimensione. Un lotto che mescola classi si
divide: la parte **G** decide, la parte **M** esegue. È il taglio che ha reso
possibile la tornata del 2026-09-04 — decidere i tre glifi (G) e rigenerare i 17
SVG (M) sono due lavori diversi che erano uno solo.

### Che cosa **non** si riclassifica

I lotti **già chiusi**. Instradare un lavoro finito è spreco puro: la
classificazione serve a decidere come eseguire, e un lotto chiuso non si esegue
più. I piani d'arco chiusi restano come sono.

## Conseguenze

**Positive.**

- Il compromesso costo/qualità diventa **una decisione scritta** invece di un
  default silenzioso.
- La colonna «qualità» **costringe a definire il collaudo prima di partire**, ed
  è il guadagno maggiore: un lotto la cui riuscita non si sa descrivere è un
  lotto tagliato male.
- Il lavoro **R** e **M** si può delegare a un subagente senza occupare il
  contesto della sessione principale — che è il throughput vero, più del prezzo
  per token.

**Negative, e vanno dette.**

- ⚠️ **La tabella è tarata a occhio, non misurata.** Nessuno ha eseguito lo
  stesso lotto su due engine per confrontare. È un'ipotesi ragionevole, e il
  **registro** è il modo in cui si corregge da sé — ma solo se qualcuno lo
  tiene. Finché il registro è vuoto, questa riga resta il difetto principale.
- ⚠️ **Ogni salto di engine butta la cache** (le cache sono legate al modello).
  Su un piano con molti lotti brevi che si alternano, la cascata può costare
  **più** di un modello solo a effort variabile. È il motivo della regola 1.
- ⚠️ **`Haiku 4.5` non è un Opus più piccolo**: ha **200K** di contesto contro
  1M, e **non accetta il parametro `effort`**. Su un file di canone grosso non
  ci sta. Va usato per lavoro corto e meccanico, non «per risparmiare».
- ⚠️ **Nessun gate verifica la classificazione**, come per ADR-0044: «questo
  lotto è di giudizio o meccanico?» è un giudizio. Un gate potrebbe controllare
  che l'intestazione *esista* — non che sia giusta — e insegnerebbe a metterne
  una a caso.
- **Costa una riga per lotto** e un momento di riflessione. Su un piano da
  quattro lotti sono quattro righe; il beneficio è tutto nella terza colonna.
- **Rischio di burocrazia.** Un lotto di due minuti non ha bisogno
  dell'intestazione. La regola vale per i lotti che stanno in un piano, non per
  ogni correzione.

## Alternative scartate

**Classificare per dimensione (piccolo/medio/grande).** È quello che verrebbe
naturale, e non dice niente su come eseguire: ridisegnare una griglia giocata è
piccola e va trattata come canone; rigenerare 17 SVG è grande e va trattata come
meccanica.

**Una cascata fissa: prima il modello economico, poi quello capace se fallisce.**
Sembra ottimizzare da sé e paga due volte quando il primo giro sbaglia, oltre a
buttare la cache al salto. La documentazione dice di misurare prima
l'alternativa semplice, e questa ADR la segue.

**Misurare prima di scrivere la regola.** Sarebbe più rigoroso e richiede un
corpus di lotti classificati che non esiste ancora. La tabella parte come
ipotesi **dichiarata tale**, ed è meglio di un default silenzioso — che è quello
che c'era.
