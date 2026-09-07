# 📒 Registro dei lotti — la classificazione messa alla prova

> **Cos'è**: il quaderno che tiene ADR-0045 onesta. Le cinque classi
> (**M** meccanico · **R** ricognizione · **C** costruzione · **G** giudizio ·
> **K** canone) sono **un'ipotesi tarata a occhio**: nessuno ha mai eseguito lo
> stesso lotto su due engine per confrontare.
>
> Questo file accumula le prove mentre si lavora. La colonna che conta è
> **«ha retto?»**: si è dovuto salire di classe a metà strada, o il lotto è
> finito con l'engine e l'effort dichiarati?

**Tre righe non dicono niente. Trenta cominciano a dire se la tabella è tarata
bene, e quali righe sono tarate male.**

⚠️ **Non è un gate.** Nessuno lo controlla — è un quaderno, e un quaderno lo
tiene chi vuole tenerlo. Ma senza, ADR-0045 resta un'ipotesi per sempre.

---

## Come si scrive una riga

Alla chiusura del lotto, non alla sua apertura. Una riga sola, e la colonna
finale solo se c'è qualcosa da dire — «è andata come previsto» non insegna
niente e si lascia vuota.

Se il lotto è **salito di classe** a metà strada, la riga vale doppio: dice che
una riga della tabella è tarata male, ed è esattamente il caso per cui il
registro esiste.

---

## Registro

| Data | Lotto | Classe prevista | Engine usato | Ha retto? | Che cosa ha insegnato |
|---|---|---|---|---|---|
| 2026-09-04 | **R6** ⬛ si separa in tre glifi | **G** giudizio | Opus 5, sessione principale | ✅ | Il lotto ne conteneva **due**: la decisione (G) e la rigenerazione dei 17 SVG (M). Trattarli come uno solo ha funzionato ma ha speso Opus su lavoro meccanico — è il caso che ha fatto nascere la regola del taglio per classe |
| 2026-09-04 | **F0** `⛰` è un muro | **C** costruzione | Opus 5, sessione principale | ⚠️ **è salito** | Previsto **C** (una riga in `WALL_SYMS` più un test). È diventato **G** quando la misura ha mostrato che il difetto era doppio e che `⛺` era fuori dai muri per sbaglio. **Una riga di codice non fa un lotto meccanico se prima bisogna capire cosa contare** |
| 2026-09-04 | **D6** la griglia di `…P1C` ridisegnata | **K** canone | Opus 5, mai delegato | ✅ | Sembrava **M** (riempire righe mancanti) ed era **K**: la griglia è una scena giocata, e l'interpolazione sbagliata metteva un muro di fuoco dove c'era campo aperto. La domanda 1 di ADR-0045 l'avrebbe presa |
| 2026-09-04 | **Censimento** dei lotti aperti nei piani | **R** ricognizione | subagente `Explore`, Sonnet 5 | ✅ | Primo lotto delegato sotto ADR-0045. Ha **confermato i miei conteggi M/R/C/G/K esattamente** (6·2·8·4·4 = 24) e ha trovato quello che non avevo visto: **43 caselle `⬜` in altri undici piani**, alcuni dei quali marcati ✅ in `INDEX`. 🔎 Ma il numero grezzo **non è un conteggio di lotti**: separandole, sono **29 citate nel testo · 6 celle vuote · 5 lotti veri · 3 glifi di stato** («⬜ NON giocato» di un arco non è un lotto). Il subagente aveva già segnalato da sé un falso positivo. **Lezione: un lotto R restituisce un numero, e il numero va ancora letto** — la ricognizione misura, non interpreta, ed è per questo che è la classe più economica |
| 2026-09-04 | **R5** giudicare le PR aperte | **G** giudizio | Opus 5, sessione principale | ⚠️ **non ha retto** | Ha soddisfatto il suo criterio (*«il DM lo legge e riconosce il proprio problema»*) **ed era incompleto**: le PR aperte erano **sei**, ne ha giudicate cinque. Il criterio di **G** è soggettivo, quindi **non vede un'assenza**. È il caso che ha fatto nascere la **quarta regola** di ADR-0045: un lotto su un insieme dichiara il comando che enumera l'insieme |
| 2026-09-05 | **R9** il censimento rifatto, e la #67 | **G** giudizio | Opus 5, sessione principale | ✅ | Il conteggio è partito da `list_pull_requests --state open`, non dalla memoria né da R5 — ed è così che la #67 è saltata fuori. 🔎 Il verdetto («superata») ha richiesto **G** vero: i motivi della PR andavano cercati uno per uno nel canone di oggi, e la parte che decide non era la data ma **la norma degli handout**, che nel frattempo era cambiata. La parte contabile costa due secondi, la parte di giudizio no: separarle è il punto |
| 2026-09-05 | **F1 1a** archiviare i `Lotto-*` (D1) | **G** giudizio | Opus 5, sessione principale | ✅ | La parte **G** è durata quanto una domanda: misurare l'insieme (3 master, 7 SVG, i riferimenti) ha **cambiato la forma della scelta** — letto il validatore invece di fidarsi del piano, è saltato fuori che archiviare master **e** SVG insieme li tiene sotto il gate, quindi la terza opzione («cancellare gli SVG con l'opt-out») non serviva. 🐛 E il `grep` ha trovato **14 riferimenti** dove il piano ne diceva **1**: la quarta regola di ADR-0045, scritta ieri, ha morso il giorno dopo |
| 2026-09-05 | **F1 1b** portare i tre master + i puntamenti | **M** meccanico | inline, Opus 5 | ⚠️ **è salito** | Previsto **M**: «i link risolvono». Ha fatto rossi **due test**, e capire perché era **G** — bisognava distinguere *«la #63 ha rotto l'importatore»* da *«la #63 ha corretto il file che l'importatore usava come campione»*. Un gate che diventa rosso dice **che** qualcosa è cambiato, mai **chi** ha ragione, e quella lettura non è meccanica |
| 2026-09-05 | **F1 1c** conflitti sui puntamenti | **C** costruzione | inline (merge a tre vie) | ✅ ma **sovradimensionato** | Previsto `Sonnet 5 · medio` per «3 commit di drift». Tre file su quattro si sono fusi **puliti**, il quarto aveva **un conflitto** — e per giunta già identificato e descritto chiudendo 1a. **Chiudere bene il lotto prima ha reso il lotto dopo più piccolo**: un effetto che la tabella dei costi non modella |
| 2026-09-05 | **F1 1d** rigenerare gli SVG | **M** meccanico | inline | ✅ | Il criterio scritto nel piano — «byte-identici» — era **sbagliato**, e il lotto è riuscito lo stesso perché il criterio si è potuto **riformulare mentre girava**: 7 identici, 4 diversi solo dove il repo è migliorato dopo la #63, e zero differenze fuori dal blocco legenda. 🔎 Un collaudo a uguaglianza esatta invecchia con lo strumento che verifica |
| 2026-09-05 | **F2 2a-2b-2c** l'overlay `@` dalla #52 | **M** + **C** | inline | ✅ **sotto stima** | Il lotto **C** (2c, la scena nuova allo standard di modulo) non ha richiesto costruzione: la scena arrivava già conforme e `validate_modules` è passato al primo colpo. E metà del costo di 2b **non esisteva più**: la rinominazione era già su `main`. 🔎 **Due stime del piano smentite in meglio nello stesso lotto** — non perché fossero sciatte, ma perché lavori successivi (lotto A di QUALITA-DEL-CODICE, gate di ADR-0043) ne avevano già chiuso dei pezzi. **Una stima invecchia anche quando nessuno la smentisce**, ed è un argomento per rimisurare all'apertura del lotto, non per stimare meglio all'apertura del piano |
| 2026-09-05 | **F3 3a** portare i due script e i test | **M** meccanico | inline, Opus 5 | ⚠️ **è salito** | Previsto **M** col criterio «i test passano com'erano». Ne sono falliti dieci, e riallinearli era meccanico (una riga: `slugify` → `nome_mappa`). Ma nello stesso lotto c'era una **mina di canone**: il `PROVENIENZA.txt` della PR avrebbe cancellato venti righe di provenienza vera. Riconoscerla è **K**, non M — e nessun gate l'avrebbe fermata, perché per un validatore un file di testo sostituito è un file di testo. 🔎 **Un lotto di trapianto porta sempre dentro anche ciò che il ramo vecchio dava per assente** |
| 2026-09-05 | **F3 3b** `SCARTI.txt` | **C** costruzione | inline, Opus 5 | ✅ | Classificato bene: contratto chiaro, sette test, il gate scritto **prima** dell'implementazione perché il criterio del piano lo nominava (*«un test che prova che un reroll senza motivo non passa»*). 🔎 È il caso che mostra a cosa serve la colonna «qualità» di ADR-0045: il collaudo era già scritto all'apertura, quindi non c'è stato niente da decidere a metà strada |
| 2026-09-05 | **F3 3c** smoke e determinismo in CI | **C** costruzione | inline, Opus 5 | ✅ | I due passi nuovi si scrivono **al contrario** — falliscono se il comando riesce — perché provano un divieto. Eseguiti in locale prima di committarli: un passo di CI scritto e non provato è esattamente il gate che non morde di cui parla ADR-0043 |

---

## Che cosa dicono le righe finora

Sono **quattordici**, quindi non dicono ancora niente di statistico. Ma due
portano lo stesso insegnamento, e vale la pena guardarlo:

> **La classe non si legge dalla dimensione del diff.** `F0` era una riga in un
> insieme; `D6` era riempire delle righe mancanti. Tutti e due sembravano
> meccanici e non lo erano — uno perché bisognava capire *cosa* contare, l'altro
> perché la griglia era canone giocato.

Se questo si ripete, la conseguenza non è cambiare la tabella: è **dare più peso
alla domanda 1** e accettare che il costo di salire di classe a metà strada è più
basso del costo di accorgersene dopo.

La quarta riga insegna un'altra cosa, sul confine fra **R** e **G**:

> **Un lotto R restituisce un numero, e il numero va ancora letto.** Il
> censimento ha contato 43 caselle `⬜` correttamente; solo cinque erano lotti.
> La ricognizione **misura, non interpreta** — ed è precisamente perché non
> interpreta che può girare su un engine più economico. Chi delega un lotto R e
> prende il numero per una conclusione ha saltato la parte **G**.

La sesta riga — **R5**, l'unica finora che ha mancato il bersaglio senza
accorgersene — dice la cosa più scomoda delle sei:

> **Un lotto G può passare il proprio collaudo ed essere sbagliato.** Le altre
> quattro classi hanno un criterio che una macchina controlla: il gate passa, i
> numeri si riproducono, il test morde. **G** ha *«il DM riconosce il proprio
> problema»*, e un DM riconosce benissimo il proprio problema in una lista
> incompleta. Dove un lotto G lavora su un insieme, la completezza va
> **tolta al giudizio** e affidata a un comando — che è esattamente quello che
> la quarta regola di ADR-0045 adesso impone.
