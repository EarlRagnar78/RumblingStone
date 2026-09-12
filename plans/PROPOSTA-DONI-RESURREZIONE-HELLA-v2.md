<!-- Proposta di ridisegno, NON canone. Il master ARC07-DEF-3 non e' stato toccato. -->
# Proposta — I Tre Doni della resurrezione di Hella, **v2**

**Stato**: 🔵 **proposta** — gate: **approvazione del DM dopo il confronto di §5**
**Data**: 2026-09-12 · **Lotto**: 4c (`PIANO-RIPRESA-PR-ABBANDONATE` §4.2)
**Sostituirebbe**: [`ARC07-DEF-3`](../07_il%20Portale%20Della%20Forgia%20Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md) §5 e la sua sintesi in §0-bis
**Non tocca**: §6 (Debito della Radice), §7 (Risveglio), §9 (Contingenze), §11 (budget PX)

> ⚠️ **Il master non è stato modificato.** Questo documento esiste perché il DM
> ha chiesto di *«creare questa nuova modalità e poi confrontarla con quella
> esistente per valutare il bilanciamento prima di approvarlo»*. Il confronto è
> in [§5](#5--il-confronto-v1-contro-v2). Se il DM approva, v2 entra nel master
> in un lotto suo e questo file si chiude.

---

## 0. Cosa mi manca, e cosa sto assumendo

**Cosa mi manca** (dichiarato, non aggirato):

1. 🔴 **Le schede dei PG non esistono come dato nel repo.** `PG/` contiene gli
   artefatti, non i punteggi: non conosco i pf massimi di Thorik, il numero
   esatto di usi giornalieri di Pugno Stordente di Tordek, né i punteggi di
   caratteristica di nessuno dei tre. È lo stesso buco che il lotto **4g** ha
   già a piano (*«oggi le schede PG non esistono come dato da nessuna parte»*).
   Conseguenza pratica: le percentuali di §5 sono **stimate dalla classe e dal
   livello**, non lette. Dove stimo, lo scrivo.
2. 🔵 **La finestra «fino al pieno risveglio» dura quanto dura il P5.** Il
   viaggio a −1.000 anni non ha una durata dichiarata in giorni di gioco. Se
   dura tre sessioni, il registro **Voto** costa il triplo di quanto stimo.
3. 🔵 **Non so se al tuo tavolo il danno alle caratteristiche si gioca davvero.**
   Se lo condonate, metà di questa proposta si sgonfia — vedi §6, è il suo
   singolo modo di fallire.

**Cosa sto assumendo**:

1. **La regola d'oro di §5 resta**: *«la resurrezione non è in ostaggio: col
   Cuore, Hella torna comunque. I sacrifici comprano la qualità del ritorno»*.
   Tutto quel che segue compra doni, mai la vita.
2. **Il meccanismo approvato di §6 è il modello**: nessuna meccanica coercitiva
   adesso, registrazione in `state.md §7` + Echo Ledger, il conto si paga in
   ARC-08/09. Il DM l'ha già accettato il 2026-07-23 per il Debito della Radice;
   v2 lo estende ai Doni invece di inventare un meccanismo nuovo.
3. **Il rifiuto resta una quest, non una punizione**: slot vuoto, si riempie
   retroattivamente in ARC-09 con un atto di sacrificio. Testo di §5 conservato
   alla lettera.
4. **Artemis è un Warlock 13**, non un incantatore a slot. Non è un'assunzione:
   è `state.md` §1 riga «Human Warlock 13». Torna in §1.

---

## 1. Audit — perché v1 non regge, misurato

### 1.1 · I tre prezzi, nella stessa valuta

D&D 3.5, PG di 13° livello. Il 13° comincia a 78.000 PE, il 14° a 91.000:
**13.000 PE** separano i due.

| PG | Costo base v1 | Cosa costa davvero | Quanto serve per tornare come prima |
|---|---|---|---|
| **Thorik** | **−2 COS permanente**, *«NEVER restored»* | a 13 DV: **−13 pf** e **−1 a Tempra**, per sempre | 🔴 **mai.** Il 3.5 distingue *ability damage* (rientra da sé) da *ability drain* (serve *restoration* per ogni punto, e il testo di v1 vieta esplicitamente il ripristino). È l'unico costo della campagna dichiarato irreversibile |
| **Tordek** | **−500 PE** | il **3,8%** dei 13.000 PE che gli servono per il 14° | 🟢 **circa uno scontro.** Il budget di §11 del master ne assegna molti di più al beat stesso |
| **Artemis** | «1 slot invocazione alto per 24 h» | 🔴 **niente, e non per approssimazione: per errore di sistema.** I warlock **non hanno slot**. Le invocazioni sono a volontà (*at will*), è la definizione della classe. La riga usa il vocabolario di un incantatore preparato applicato all'unico PG che non lo è | 🟢 **zero** |

**Il rapporto fra il prezzo più alto e il più basso non è "sbilanciato": è
indefinito**, perché uno dei tre è ∞ e un altro è 0. Il DM ha ragione, e il
margine è più largo di quanto suonasse: *«mi sembra un prezzo troppo alto da far
pagare ad 1 solo pg mentre per gli altri sono quisquiglie»*.

### 1.2 · Il difetto strutturale, che è peggio dello sbilanciamento

Guarda le tre strade di Thorik in v1:

| Strada | Costo | **Hella riceve** |
|---|---|---|
| Il Sangue della Stirpe | −2 COS permanente | Pelle di Adamantio (RD 3/−) |
| La Memoria della Battaglia | −3.000 PE | Pelle di Adamantio (RD 3/−) |
| Il Filo dell'Ascia | Aegis Fang perde *Returning* | Pelle di Adamantio (RD 3/−) |

🔴 **Le tre strade danno lo stesso dono.** Sono tre prezzi per una merce sola —
quindi non sono una scelta: sono un **listino**, e un giocatore che ragiona
prende il più economico. Il *Filo dell'Ascia* costa un incomodo temporaneo e
compra esattamente la stessa RD 3/− del sacrificio permanente.

Ne segue la cosa scomoda: **il −2 COS non viene mai pagato da un giocatore che
ottimizza — viene pagato solo da chi interpreta contro il proprio interesse.**
Il design, così com'è, **mette una tassa sulla buona fede**. Non è un
bilanciamento sbagliato: è un incentivo rovesciato.

Stessa forma per Tordek (tre prezzi → Timeless Body) e per Artemis (due prezzi →
Rinascita Spontanea).

### 1.3 · Cosa v1 fa bene, e che v2 non deve rompere

Non è un documento da buttare. Regge:

- ✅ la **regola d'oro** (la resurrezione non è in ostaggio);
- ✅ **Moradin chiede, non impone** — *«Non è il dono che chiedevo. È il dono che DAI»*;
- ✅ il **rifiuto come quest** (slot vuoti, riempimento retroattivo in ARC-09);
- ✅ **Hella nomina solo chi ha donato**, e per chi ha rifiutato *«lo guarda un
  istante più a lungo del necessario, e non dice nulla»*. Questa riga è il
  meccanismo più efficace di tutto il §5 e **non si tocca**;
- ✅ le **reazioni di Moradin senza giudizio**, tre righe, tutte tenute.

---

## 2. Sviluppo — il ridisegno

### 2.1 · Le due regole che fanno tutto il lavoro

> **Regola 1 — tre strade, tre doni diversi.** Ogni strada dà a Hella una cosa
> **diversa**. Non c'è una strada economica: c'è una **Hella diversa** a seconda
> di come tornano indietro. La scelta smette di essere un acquisto e torna a
> essere una scelta.
>
> **Regola 2 — il prezzo è un debito che il mondo ricorda, non una cifra sulla
> scheda.** È il meccanismo di §6, già approvato dal DM il 2026-07-23:
> registrazione in `state.md §7` + Echo Ledger, **nessuna meccanica coercitiva
> adesso**, il conto arriva in ARC-08/09.

### 2.2 · L'unità di conto

Le nove strade stanno su **tre registri**, e ogni PG ne ha esattamente uno per
registro. Il registro dice quanto costa; il PG dice cosa dona.

| Registro | Cosa paghi | Finestra | Chi lo vede |
|---|---|---|---|
| **A · Carne** | il corpo, adesso | 1 riposo lungo (i pf), 1-2 giorni (il danno a COS) | tutti, subito |
| **B · Voto** | un potere che sospendi | fino al **pieno risveglio** di Hella (inizio ARC-08) | il tavolo, ogni volta che quel potere manca |
| **C · Oggetto** | qualcosa che **cede** | **permanente** — ma passa a Hella | per sempre |

🟢 **La chiave del registro C**: la perdita è permanente **per il PG**, non per
il party — il potere cambia mano, non svanisce. È così che v2 rimette un prezzo
permanente sul tavolo (che v1 aveva, e che dà peso alla scena) **senza** far
pagare a un solo PG un conto che gli altri non pagano.

⚠️ **Un solo registro per PG per rito**: chi paga in Carne non paga anche in
Voto. Non è cumulabile.

### 2.3 · DONO 1 — THORIK: «La Forza»

> *Thorik si inginocchia. Non chiede a nessuno il permesso: l'ha già fatto una
> volta, sotto il Peso, e adesso sa il cambio.*

| | Strada | Costo | **Hella riceve** |
|---|---|---|---|
| **A** | **Il Sangue della Stirpe** — apre la vena sulla fronte di lei | **4d12 pf**, che **non si curano magicamente** fino al risveglio (§7), **e 2 punti di *danno* a Costituzione** | **Pelle di Adamantio** — RD 3/− |
| **B** | **L'Eco dello Smeraldo** — versa nella pietra la carica che la Corona gli aveva dato | lo **Smeraldo** (terremoto 1/settimana) è speso qui e **non ricarica** fino al risveglio; **Stone's Awareness** tace nella stessa finestra | **Lo Scudo del Portatore** — 1/giorno, azione immediata: Hella prende su di sé il danno di un alleato adiacente, **dimezzato** |
| **C** | **Il Filo dell'Ascia** — l'ascia dona il suo richiamo | Aegis Fang cede ***Returning*** **permanentemente**: da qui in poi torna un'ascia che va raccolta | **Il Richiamo** — 1/round, azione gratuita, Hella richiama a sé un'arma lanciata o disarmata entro 9 m |
| **✕** | **Rifiuto** | — | nessun dono da Thorik; lo slot resta vuoto (§2.7) |

⚠️ **Su A, la parola che cambia tutto.** *«2 punti di **danno** a Costituzione»*
non è *«−2 COS»*: in 3.5 il **danno** rientra da sé (1 punto al giorno di riposo,
o una *lesser restoration*), il **risucchio permanente** no. La poesia del prezzo
di sangue resta intera; la permanenza sparisce. È la risposta letterale alla
domanda del DM — *«magari un'alternativa migliore a −2 COS si potrebbe trovare
che abbia senso»* — e conserva anche la sua controproposta (*«perde 4d12 pf ed è
inabile per lo sforzo»*), che è esattamente la riga A.

### 2.4 · DONO 2 — TORDEK: «Il Respiro»

> *Tordek non dice niente. Ha già smesso di parlare tre battiti fa.*

| | Strada | Costo | **Hella riceve** |
|---|---|---|---|
| **A** | **Il Respiro Donato** — soffia il proprio fiato nei polmoni immobili | **2 punti di *danno* a Costituzione** (si svuota, non si ferisce) e **affaticato** fino al riposo lungo successivo | **Timeless Body** — immune a veleni, malattie, invecchiamento |
| **B** | **Il Voto del Silenzio** — non parla finché lei non parla | **Ancoraggio della Montagna** (2/g) e **Salto Infuocato** (3/g) tacciono fino al risveglio; e Tordek **non parla**: niente comando vocale sui Bracieri, e ⚠️ **niente voce nella trattativa con la Custode delle Radici** (§6), che avviene mentre il voto è in corso | **Il Faro** — 1/giorno Hella concede a un alleato entro 9 m di **ritirare** un TS fallito contro paura, charme o costrizione |
| **C** | **L'Ancora Ceduta** — le passa il potere che lo tiene piantato | **Ancoraggio della Montagna** passa a Hella, **permanentemente**: Tordek non ce l'ha più | **Ancoraggio della Montagna** — 2/giorno, il potere trasferito |
| **✕** | **Rifiuto** | — | nessun dono da Tordek; slot vuoto |

⚠️ **B non è gratis, ed è il punto.** In v1 il *Voto del Silenzio del Ki* costava
48 ore di ki e basta. Qui il voto **cade dentro la scena di §6**: il party deve
contrattare con la Custode delle Radici e Tordek — che è il PG con cui il
modulo dice *«da' la scena a Tordek se la vuole»* (§4 Step 5) — **non può
parlare**. È un costo che non si misura in dadi e si sente al tavolo.

### 2.5 · DONO 3 — ARTEMIS: «La Scintilla»

> **Nota di sistema.** Artemis è **Warlock 13**: le invocazioni sono **a
> volontà**, non a slot. Nessuna strada di v2 gli chiede uno slot, perché non ne
> ha. Quel che un warlock **può** spendere sono le cariche giornaliere
> dell'Anello e il proprio corpo.

| | Strada | Costo | **Hella riceve** |
|---|---|---|---|
| **A** | **La Scintilla** — riavvia il ritmo del cuore con caos controllato | **4d6 danni da fuoco che la sua Resistenza al Fuoco 10 non mitiga** (è il suo stesso fuoco che gli torna indietro) e **affaticato** fino al riposo lungo | **Rinascita Spontanea** — 1/giorno auto-stabilizza a 0 pf e le dà 13 pf temporanei |
| **B** | **Il Silenzio dell'Anello** — l'Anello presta la sua armonia | i **quattro poteri 1/giorno** dell'Anello (Luce di Lathander, Ombra di Mask, Dono dell'Unità, Tempesta di Fuoco) tacciono fino al risveglio. 🟢 **Ali d'Ombra e Passo d'Ombra restano**: la mobilità è la sua identità, toglierla è sproporzionato | **Doppia Luce** — 1/giorno, luce d'oro e d'argento insieme, raggio 9 m per 13 round: gli alleati dentro hanno **+1 morale** ai TS contro paura ed effetti di morte, i non-morti subiscono **1d6 ogni 2 livelli** di Hella (Volontà dimezza) |
| **C** | **Il Dono dell'Unità Ceduto** — le dà l'unica cosa dell'Anello che serve a un altro | **Dono dell'Unità** passa a Hella, **permanentemente**: Artemis non lo riavrà | **Il Dono dell'Unità** — 1/giorno, un'azione standard extra a un alleato entro 9 m |
| **✕** | **Rifiuto** | — | nessun dono da Artemis; slot vuoto |

### 2.6 · Le combinazioni — quel che emerge se i tre scelgono lo stesso registro

Questa è la parte che risponde a *«tutte le scelte dei 3 pg si devono
ripercuotere in maniera coerente sui doni che vengono dati ad Hella»*: i tre
doni non si sommano soltanto, in tre casi **producono un quarto**.

| Combinazione | Emerge | Perché |
|---|---|---|
| **3 × A** — tutti pagano con la carne | **Il Corpo Prestato** — 1/giorno Hella trasferisce a un donatore adiacente pf temporanei pari al suo livello da druida (12) | *Il sangue torna dove è stato dato.* |
| **3 × B** — tutti fanno un voto | **Il Coro** — finché almeno **due** donatori sono entro 9 m da lei, loro e Hella hanno **+1 morale** ai TS | *Un voto vale poco; tre sono un giuramento.* |
| **3 × C** — tutti cedono qualcosa | **La Collana Piena** — i tre slot-dono della Collana dei Semi Eterni sono pieni **subito**, e il terzo seme (Durik) **non può mai essere perso** | *La Collana nasce già completa.* |
| **misto** (2+1, o uno per registro) | nessun dono emergente | ed è il **caso normale**, non una punizione |

🔴 **Non leggere questa tabella al tavolo, e non anticiparla.** Se i giocatori la
conoscono prima di scegliere, la scena smette di essere una scelta emotiva e
diventa un problema di coordinamento — che è esattamente il difetto di v1
riprodotto un piano più su. Si rivela **dopo**, come una cosa che è successa.

### 2.7 · Il rifiuto, e lo Step 5

**Il rifiuto** resta **verbatim da v1** — è già approvato e funziona:

> Il Cuore basta: Hella torna, ma **senza i Doni** mancanti. La Collana nasce
> comunque; gli **slot restano vuoti** e ciascun PG potrà colmarli **in gioco**
> più avanti (quest personali ARC-09 — quando uno slot si riempie con un atto di
> sacrificio, il Dono si attiva **retroattivamente**). *Il rifiuto diventa una
> quest, non una punizione.*

**Lo Step 5 scala coi doni** — questa sostituisce la regola *«3 successi su 3 se
Thorik ha rifiutato»*, che puniva un solo PG per una scelta di tutti:

| Doni versati | Step 5 · Volontà CD 18 |
|---|---|
| **3** | **1 successo su 3** |
| **2** | **2 su 3** — il default scritto in §4 |
| **1** | **3 su 3** |
| **0** | **3 su 3**, e la Custode delle Radici (§6) si presenta **già al ramo B** di default |

⚠️ Anche a 0 doni la regola d'oro tiene: §9 dice che il rito **non fallisce del
tutto** neanche fallendo lo Step 5 — Hella torna con 1 livello negativo (PF1e,
svanisce in 7 giorni) e un risveglio doloroso. **Non esiste un ramo in cui Hella
resta morta perché nessuno ha pagato.**

### 2.8 · Cosa ricorda il mondo (il livello §6, applicato ai Doni)

Ogni strada apre un filo nell'**Echo Ledger** (§10) e si registra in
**`state.md §7`**. Come in §6: **nessuna meccanica coercitiva adesso**.

| Registro | L'eco | Quando riemerge |
|---|---|---|
| **A · Carne** | *la carne ricorda* — la prima volta che quel PG scende sotto metà pf in ARC-08, Hella **lo sente**, ovunque sia | ARC-08, 1ª ferita seria |
| **B · Voto** | *il voto si scioglie* — al pieno risveglio la rinuncia finisce in una scena: lei restituisce quel che era sospeso | inizio ARC-08 |
| **C · Oggetto** | *la cosa ha memoria* — quando Hella usa il potere ceduto davanti a chi gliel'ha dato, si descrive **con la voce di chi l'ha dato**. Meccanicamente niente; è il pagamento | sempre |

---

## 3. Cosa cambia nel master, se il DM approva

| File | Sezione | Cosa |
|---|---|---|
| `ARC07-DEF-3` | **§5** | sostituita da §2.3-2.8 di qui |
| `ARC07-DEF-3` | **§0-bis** «I Tre Doni» | la tabella di sintesi si rifà: 9 strade, non 3 |
| `ARC07-DEF-3` | **§9** riga FALLIMENTO | *«meno di 2 successi, o 3/3 mancati se Thorik ha rifiutato»* → la scala di §2.7 |
| `ARC07-DEF-3` | **§10** Echo Ledger | la riga *«Thorik dona il sangue (−2 COS) — costo permanente»* → i tre registri di §2.8 |
| `ARC07-DEF-3` | **§11** budget PX | 🟢 **invariato**: v2 non spende PE, quindi il budget non va rifatto |
| `ARC07-DEF-3` | **§6, §7, §8** | 🟢 **invariati** |
| `campaign/state.md` | §1, §7 | 🟢 **già fatti nel lotto 4c**: i costi non versati sono stati tolti dal presente |

---

## 4. Validazione — come si prova che v2 regge

### 4.1 · Le prove di coerenza (si fanno a tavolino, prima del tavolo)

| # | Prova | Criterio di successo |
|---|---|---|
| V1 | **Nessuna strada dominante** | per ogni PG, le tre strade danno **tre doni diversi** — non esiste «la stessa merce più economica» |
| V2 | **Nessun costo permanente asimmetrico** | il registro **C** è permanente per **tutti e tre**, o per nessuno |
| V3 | **Nessun costo in PE** | v2 non tocca il budget PX di §11 |
| V4 | **Vocabolario di sistema corretto** | nessuna strada chiede a un warlock uno **slot**; nessuna confonde *danno* e *risucchio* di caratteristica |
| V5 | **La regola d'oro tiene** | esiste un cammino, per ogni combinazione (0-3 doni), in cui Hella torna |
| V6 | **Il rifiuto resta una quest** | il testo del rifiuto totale di v1 è conservato alla lettera |
| V7 | **Niente meccaniche coercitive adesso** | come §6: si registra, non si impone |

### 4.2 · La prova che conta, e che solo il tavolo può dare

🔴 **Nessuna di queste prove dice se la scena è *bella*.** Dicono che è coerente.
La domanda vera — *un giocatore, messo davanti a queste tre strade, esita?* — si
risponde giocandola. Se v2 viene approvato, la verifica è: al rito, **quanto
tempo passa fra la domanda di Moradin e la prima risposta**. Se rispondono
subito, il ridisegno ha fallito lo stesso, in un modo diverso.

### 4.3 · Il gate che non esiste

⚠️ Non c'è un controllo automatico che possa accorgersi che v2 si è sfasato dal
master. `validate_docs` vede i link rotti, non le regole divergenti. Finché
questo file e §5 di `ARC07-DEF-3` coesistono, **coesistono due versioni della
stessa scena** — ed è per questo che questa proposta ha una scadenza: o entra
nel master, o si archivia. Non deve restare qui a marcire, o al primo giro
qualcuno leggerà quella sbagliata.

---

## 5. Il confronto — v1 contro v2

### 5.1 · I prezzi, affiancati

| | **v1** | **v2 · A Carne** | **v2 · B Voto** | **v2 · C Oggetto** |
|---|---|---|---|---|
| **Thorik** | −2 COS **permanente**, mai ripristinata | 4d12 pf + 2 **danno** a COS → ~1 riposo lungo + 2 giorni | Smeraldo + Stone's Awareness → 1 arco | *Returning* di Aegis Fang → **permanente, ceduto** |
| **Tordek** | −500 PE → **~1 scontro** | 2 **danno** a COS + affaticato → ~1 riposo + 2 giorni | Ancoraggio + Salto + la voce → 1 arco | Ancoraggio della Montagna → **permanente, ceduto** |
| **Artemis** | 1 «slot» inesistente → **0** | 4d6 fuoco non mitigato + affaticato → 1 riposo | i quattro 1/giorno dell'Anello → 1 arco | Dono dell'Unità → **permanente, ceduto** |
| **Rapporto max/min** | 🔴 **indefinito** (∞ contro 0) | 🟢 **~1:1** | 🟢 **~1:1** | 🟢 **1:1 per costruzione** |

### 5.2 · Il confronto che conta di più

| | v1 | v2 |
|---|---|---|
| Strade per PG | 3 (+ rifiuto) | 3 (+ rifiuto) |
| Doni distinti offerti | **3** | **9** |
| Doni per strada | **lo stesso per tutte e 3** 🔴 | **uno diverso per strada** 🟢 |
| Esiste una strada dominante? | 🔴 **sì** — la più economica, a parità di dono | 🟢 **no** — non c'è parità di dono |
| Chi paga il prezzo permanente | 🔴 **solo Thorik**, e solo se interpreta | 🟢 **chiunque scelga C**, e il party non perde il potere |
| Il costo in PE | −500 e −3.000 PE, che il DM deve scontare dal budget di §11 | 🟢 **nessuno** |
| Errori di sistema | 🔴 uno (slot a un warlock) | — |
| Le combinazioni contano? | no: 3 doni fissi | 🟢 sì — tre sinergie emergenti (§2.6) |
| Lo Step 5 | 3/3 **solo se rifiuta Thorik** — un PG punito per la scelta di tutti | 🟢 scala **coi doni versati**, chiunque li abbia dati |
| Cose da tenere a mente per il DM | 3 doni, 8 strade | 🔴 **9 doni, 9 strade, 3 sinergie** |

### 5.3 · Cosa v2 peggiora — onestamente

1. 🔴 **È tre volte più roba da ricordare.** 9 doni contro 3. Mitigazione: la
   tabella di §0-bis diventa una pagina intera, e al tavolo servono comunque
   solo le tre righe del PG che sta parlando. Ma è un costo vero per il DM.
2. 🔴 **Il registro C sposta poteri fra schede, per sempre.** Se non ti piace che
   Aegis Fang perda *Returning* in via definitiva, il registro C va rifatto —
   ed è la gamba su cui poggia tutta la simmetria del prezzo permanente.
3. 🔴 **Se al tavolo il danno alle caratteristiche si condona, il registro A
   diventa di nuovo il più economico** e v2 ricade nel difetto di v1. È il suo
   **singolo modo di fallire**, e va deciso prima: se non giocate il danno a
   COS, sostituisci A con «4d12 pf + affaticato» per tutti e tre e accetta che A
   sia il registro leggero, dichiarandolo.
4. 🟡 **Le sinergie di §2.6 possono trasformare la scena in un coordinamento.**
   Mitigazione in §2.6: non si leggono ad alta voce. Ma un tavolo di veterani le
   indovina.
5. 🟡 **Hella diventa più complicata.** In v1 aveva 3 doni fissi; in v2 la sua
   scheda dipende da 3 scelte fatte da altri. `ARC07-DEF-3` §7-bis (la sua
   scheda giocabile) va rigenerata **dopo** il rito, non prima.

### 5.4 · La raccomandazione

**Adotterei v2, con la §5.3 punto 3 decisa prima.** Non perché v1 sia
sbilanciato — quello si aggiustava cambiando tre numeri — ma perché v1 ha
un **incentivo rovesciato**: paga di più chi interpreta meglio. Cambiare i numeri
non lo toglie; cambiare la struttura sì.

La singola modifica che porta più valore, se il DM volesse il **minimo**
indispensabile invece di tutto v2, è **una sola**:

> 🎯 **Rendere diversi i tre doni delle tre strade di Thorik**, e sostituire
> *«−2 COS permanente»* con *«2 punti di danno a Costituzione»*. Due righe. Da
> sole tolgono sia il prezzo indefinito sia la strada dominante del PG che il DM
> ha segnalato.

Il resto di v2 — Tordek, Artemis, i registri, le sinergie — è quel che serve
perché la stessa correzione valga per tutti e tre invece che per uno solo, come
il DM ha chiesto.

---

## 6. La decisione che resta al DM

| Domanda | Opzioni |
|---|---|
| **1. Si adotta v2?** | **A** tutto v2 · **B** solo la correzione minima di §5.4 · **C** si resta a v1 e si cambiano solo i numeri |
| **2. Al tuo tavolo si gioca il danno alle caratteristiche?** | se **no**, va rifatto il registro A (§5.3 punto 3) **prima** di approvare |
| **3. Il registro C (cessione permanente) ti va?** | è la gamba della simmetria: se cade, cade il prezzo permanente per tutti |

Registrata come **D13** in [`PIANO-RIPRESA-PR-ABBANDONATE`](PIANO-RIPRESA-PR-ABBANDONATE.md#le-decisioni-che-restano-al-dm).
