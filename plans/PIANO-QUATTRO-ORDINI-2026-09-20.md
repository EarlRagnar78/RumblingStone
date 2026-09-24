# PIANO — Cinque ordini del DM, e una norma che era stata archiviata troppo presto

> **Cos'è**: l'esecuzione delle cinque istruzioni date dal DM il 2026-09-20,
> tre delle quali chiudono altrettante code lasciate aperte dalla PR #151.
>
> **Stato**: 🟡 in corso (2026-09-20) · **Ramo**: `claude/open-prs-plans-review-fu4qcp`
> **Gate**: `misura_craft --p1` · `validate_norme_editoriali` ·
> `validate_prosa` · `pytest scripts/tests`

---

## Gli ordini, come sono arrivati

| | Ordine del DM | Che tipo di lavoro è |
|---|---|---|
| **A** | *«l'INFERRED comanda cosa è scritto nell'artefatto della Corona: se adesso ha già quel potere e il giocatore l'ha letto sulla scheda, non è presente nel Rituale 4; altrimenti è presente»* | una **regola di decisione**, che il DM delega a un dato |
| **B** | *«rendi `ARC07-CONSEGUENZE-ECHI` consapevole del bivio della Senzienza»* | propagazione di canone |
| **C** | *«229 read-aloud da correggere tutti»* | riscrittura di prosa su larga scala |
| **D** | *«se compaiono nello statblock di un PNG sono seguiti da un numero… nel caso di prove non dovrebbe essere nella forma "prova di Forza CD 25"? In questo modo è più facile distinguerli? Puoi verificare se apporta dei miglioramenti misurandoli?»* | una **proposta di misura**, da verificare |
| **E** | *«mettere una golden rule che esegue i passi della Fase 1 di analisi in sola lettura usando le metriche di misurazione introdotte… e si usa preferibilmente il registro delle norme, l'algoritmo a strati e i 322 nomi di Bestiario prima di qualsiasi regex, in modo da eliminare errori di analisi ricorrenti, questo prima di ogni modifica»* | una **regola di processo**, arrivata a metà di questo piano e che questo piano stava già violando a metà |

⚠️ **Assunzioni dichiarate prima di procedere.**

1. **A si applica alla lettera, e il dato che decide è la scheda giocatore**
   `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md`, non la matrice degli artefatti. È
   quello che il DM ha nominato («la scheda dell'artefatto»), ed è l'unico
   documento che il giocatore ha davvero letto.
2. **C si applica al set vero, non al numero pubblicato.** Il «229» è una
   misura di questa stessa PR e la FASE 1 lo ha trovato falso (§1.2). Correggo
   **tutti** i box del set vero; non ne lascio fuori nessuno per comodità.
3. **D si verifica prima di entrare.** Una proposta di misura si accetta se
   migliora precisione e copertura rispetto a quella che sostituisce, e i
   numeri vanno pubblicati anche se dicono di no.
4. **E vale anche retroattivamente su questo piano.** L'ordine è arrivato
   quando la FASE 1 era già scritta, e la FASE 1 lo aveva **violato due volte**
   (§1.2, §1.3): ho scritto una regex nuova prima di guardare cosa il repo
   avesse già, e le prime due misure erano sbagliate. Le correzioni sono nel
   piano perché la regola nasce da lì.

---

## FASE 1 — Audit (chiusa, riportata qui perché è la prova)

### 1.1 · A — la scheda decide, e decide in due modi opposti

| Potere che la matrice attribuisce al Rituale 4 | Sta sulla scheda del giocatore? | Verdetto per la regola del DM |
|---|---|---|
| **Mantle of Stone and Spirit** (*Manto di Pietra e Spirito*) | **sì** — riga 35, colonna «**Rit. 3**», fra i poteri **attivi** | ⛔ **fuori** dal Rituale 4 |
| **buff forza/coraggio 1/settimana** | **no**, in nessuna forma | ✅ **dentro** il Rituale 4 |

E la scheda dice anche cosa il Rituale 4 consegna, in una riga sola
(riga 144): *«Non ancora sbloccati (Rituale 4, "Assedio della Forgia Eterna"):
**Corona di Protezione +3**, **Senzienza**, **Rubino**»*. Sono esattamente i
tre che `§4-quater` già scrive.

🔎 **Il buff esiste, ma non si chiama così.** Le fonti d'artefatto lo
chiamano ***Aura of the Eternal Forge***, ed è il **potere finale** del
Rituale 4 (`campaign-artifacts.md` §78; `00_corona_di_adamantio_completa_italiano.md`
§114). La sua forma canonica smentisce la riga della matrice in due punti:

| La matrice dice | Le fonti dicono |
|---|---|
| «buff forza/coraggio» | *Possenza Divina* + *Protezione dal Male* ai viaggiatori; *Possenza Divina*, *Protezione dal Male*, *Benedizione* e un uso di *Scolpire Pietra* a **tutti i nani entro 30 m**; **+4 morale** ad attacchi e TS per i nani in vista; nemici **Volontà CD 20** o *scossi* 1 minuto |
| «1/settimana» | **evento unico e irripetibile**, *«automatico all'arrivo nel passato»*, **durata: fino all'alba** |

⚠️ ~~**E qui c'è la conseguenza scomoda.** Se l'Aura è automatica all'arrivo e
dura fino all'alba, allora ha coperto tutto il beat, duello compreso: sono
circa due gradi di EL, e `§4` è tarato senza.~~

> 🔴 **CORREZIONE del 2026-09-21, e il difetto era di nuovo mio.** Quella
> conseguenza **non esiste**, e l'avevo dedotta dalla fonte sbagliata. La
> matrice degli artefatti — che è la fonte viva — dà come innesco del Rituale 4
> *«**vittoria nella battaglia antica (P5)**»*, non l'arrivo. L'«automatica
> all'arrivo» viene da `00_corona_di_adamantio_completa_italiano.md`, che
> descrive un Rituale 4 **di una scena sola**: una struttura superata.
>
> Quindi l'Aura arriva **dopo** il duello, `§4` resta tarato come è scritto, e
> **nessun numero di Skullcrusher va toccato**. È la terza volta in questa
> campagna che leggo una fonte superata come se fosse canone, ed è la terza
> volta che a prendermi è il confronto con la matrice.

🔎 **E scrivendo la scena è saltato fuori che metà del potere si gioca già.**
La **Guarigione del passaggio** di `§3 SCENA 1` — pf pieni, usi ricaricati,
nessun tiro, canone dal 2026-07-31 — **è** la metà curativa dell'*Aura*,
attribuita al portale invece che alla Corona. Resta dov'è e non si somma: al
Rituale 4 arriva solo la metà che potenzia.

### 1.2 · C — il «229» è falso, e lo è per la ragione di sempre

| | Box totali | Box con P1 | % |
|---|---|---|---|
| Pubblicato nella ricerca (2026-09-19) | 1.334 | **229** | 17% |
| Rimisurato col rilevatore vero dei box (`misura_craft.box_read_aloud`) | 626 | **131** | 21% |
| Al netto di archivi dichiarati, prompt d'immagine e file `DEPRECATO` | **540** | **104** | **19%** |

🔴 **Il denominatore pubblicato era più del doppio di quello vero.** La
ricerca aveva contato i box con un criterio proprio invece di riusare
`box_read_aloud`, che è il rilevatore che il repo già possiede per i box. È il
**quattordicesimo** caso della stessa famiglia in questo ramo, e la cura è
sempre la stessa: riusare il dato invece di riscriverlo.

Le tre esclusioni, ognuna con il **dato del repo** che la giustifica:

| Cosa esce | Quanti | Il dato che lo dichiara |
|---|---|---|
| `06_Stanza-corona-di-adamantio/StanzaCoronaDiAdamantio/00-La Corona…/` | 9 | contiene `_SNAPSHOT-STORICO.md`, e i file sono **byte per byte identici** alla copia canonica in `PG/` |
| `07_…/Immagini/PROMPT-IMMAGINI-07ILP.md` | 11 | è un master di prompt d'immagine (ADR-0015), non prosa da leggere al tavolo |
| `ARC08-90/91/92-DEPRECATO-*` | 5 | `misura_craft.ESCLUSI_NOME` esclude già `DEPRECATO` |

E un falso positivo vero, trovato a mano: *«Nonna Grasa conta le candele
**avanzate**»* — participio, non seconda persona. Il verbo `avanz*` esce dal
rilevatore, e con lui l'unico errore del campione.

### 1.3 · D — la proposta del DM misurata, e funziona

La ricerca del 2026-09-19 aveva archiviato la norma WotC sulle maiuscole come
**non misurabile**, con questa ragione: *«in italiano* Forza *è anche un
sostantivo comune, e un rilevatore darebbe più falsi positivi che errori»*.
Era vero del matcher che avevo in mente. **Non era vero della norma.**

Il DM propone di guardare la **forma**, non la parola. Misurato sui 511 file
di gioco:

| | Occorrenze | Fuori norma | Falsi positivi (controllati a mano) |
|---|---|---|---|
| matcher nudo `\b(forza\|destrezza\|…)\b` | **2.014** | — | inutilizzabile |
| **F1** caratteristica + punteggio (`Forza 25`) | 1 | 0 | 0 |
| **F2** abilità + modificatore col segno (`Nuotare +9`) | **213** | **0** | **0** |
| **F3** `prova/tiro/TS di X` con una **CD sulla stessa riga** | 38 | **2** | **0** |
| **F4** `bonus/modificatore di X` | 6 | **1** | **0** |
| **totale delle quattro forme** | **258** | **3** | **0** |

🔎 **Due cose che solo la misura poteva dire.**

- **F1 trova una sola occorrenza** perché questo repo scrive le caratteristiche
  **in sigla**: `For 25`, `Des 14`. Sono **688**, e sono maiuscole per
  costruzione, quindi non c'è niente da misurare lì. L'intuizione del DM è
  giusta e il repo la applica già, in un'altra grafia.
- **F2 ha dovuto stringersi**. Scritta con `\s*[+-]\s*\d`, catturava
  *«40.500 mo in oggetti di artigianato + 1 Sacrificio Personale»*: tre falsi
  positivi su tre. Vietare lo spazio dopo il segno (`Nuotare +9`, mai
  `artigianato + 1`) li azzera tutti e tre senza perdere un solo caso vero.

> **La risposta al DM, in una riga**: sì, la forma rende la norma misurabile —
> **258 occorrenze sotto controllo, 3 violazioni vere, zero falsi positivi** —
> e il cancello nasce quasi verde, a tre correzioni dallo zero.

### 1.4 · B — cosa manca davvero agli echi

`ARC07-CONSEGUENZE-ECHI.md` (73 righe) conosce l'esito del duello e ne fa
tre varianti di tono del Rubino. **Non conosce** il bivio che `DEF-3` §5 apre
e `DEF-4` §4-quater incassa: misurato, il file ha **zero** occorrenze di
*Senzienza*, *deflessione*, *Rituale 4*, *Corona +3*; *Aegis Fang* compare una
volta sola, come nome di Thorgrim.

---

## FASE 2 — Sviluppo

### 2A · Il Rituale 4 dice la verità sulla scheda ✅ *(chiuso 2026-09-21)*

1. `ARC07-DEF-4` §4-quater: il blocco `[INFERRED]` esce e diventa **canone
   scritto**. Il Mantle non compare (è già suo dal Rituale 3); l'*Aura della
   Forgia Eterna* compare nella sua forma vera.
2. Il problema di taratura di §1.1 si risolve **dichiarandolo**, non
   nascondendolo: l'Aura entra come **potere del Rituale 4 che si è già
   manifestato all'arrivo**, con una riga di regia in `§3 SCENA 1` e una
   sidebar di scalatura in `§4`. Il master non viene ribilanciato in questo
   lotto: il DM ha un numero e decide lui se alzare Skullcrusher.
3. `ARTEFATTI-MATRICE-VERSIONI.md` riga 56: il Mantle esce dalla riga del
   Rituale 4, il buff prende il suo nome vero e la sua durata vera.
4. `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` riga 169-172: la riga di PAGINA 2
   che elenca il Manto come «da confermare col DM» contraddice la riga 35
   della stessa scheda, dove è **confermato e attivo**. Si allinea.

### 2B · Gli echi conoscono il bivio ✅ *(chiuso 2026-09-21)*

Due righe nuove nella **TABELLA ECHI** (§1) e una sezione **§2-bis** che porta
il bivio nel formato del file (*evento → eco → quando riemerge → file che lo
gestisce*): Senzienza calda o fredda, la deflessione donata, Corona +3, Aegis
Fang Stage 1. La sezione dice anche **dove si scioglie il ramo freddo**
(ARC-09, la prima volta che Thorik rischia qualcosa di suo), perché un eco
senza il suo punto di riscossione è una nota.

### 2C · I 104 box ✅ *(chiuso 2026-09-21)*

**Esito: 104 → 22, in quattro giri.** Il conto non scende a zero e non
deve: i 22 che restano sono cinque classi di cose che il rilevatore non sa
distinguere dalla narrazione, elencate qui sotto una per una. Il cancello
che le tiene ferme è `test_ogni_residuo_e_uno_dei_ventidue_dichiarati`, che
àncora il conto **file per file** — provato all'indietro reintroducendo un
«lo sentite nello sterno» in `ARC07-DEF-1`: rosso, e ripristinato verde.

| Giro | Bersaglio | Rilevati | Corretti | Restano |
|---|---|---:|---:|---:|
| 1 | i cinque master DEF di ARC-07 + gli handout | 17 | 15 | 2 |
| 2 | i beat non consolidati (P1 · P2 · P3 · Piramide · Boss Fauci) | 58 | 49 | 9 |
| 3 | ARC-08 e ARC-09 | 17 | 8 | 9 |
| 4 | le schede e le fonti d'artefatto in `PG/` | 12 | 10 | 2 |
| | **totale** | **104** | **82** | **22** |

**I 22, per classe** — l'elenco vive anche nel test, perché un elenco che
sta solo in un piano non ferma nessuno:

| Classe | Quanti | Cos'è |
|---|---:|---|
| **dialogo** | 12 | Moradin, Aegis Fang, Mask e Lathander, Re Thorek, Nania, Lythiel, Tempestas, la cellula di Dauth. Parlano in seconda persona a chi hanno davanti, ed è il loro registro: è la prima esenzione scritta in questo lotto |
| **falso positivo del rilevatore** | 6 | tre classi, tutte vere: «chiunque lo *guardi*» e «chiunque *tocchi*» sono **terza persona congiuntiva**; «*VEDI* PARTE 2», «*Vedi* CONTRADE-STEMMI-CANTI» e «*vedi* `ARC07-DEF-1`» sono **rimandi per il DM** finiti dentro un box; «da dove *arrivi* la voce» è una **similitudine al congiuntivo** |
| **visione interiore** | 2 | il sogno di Thorik in DEF-2, il flash della visione di Moradin in P2: la seconda esenzione |
| **canto** | 1 | la ballata del Palio è un testo cantato a qualcuno |
| **condizionale che la scelta la lascia** | 1 | «Non parla finché tu non la *prendi*» dice al DM cosa fa Lythiel **se** il giocatore prende la ghianda. È esattamente la forma che la norma chiede, e viene contata lo stesso |

🔎 **Quel che la correzione ha mostrato, e che l'audit non aveva visto.** In
ARC-07 la clausola d'azione era quasi sempre **ridondante**: la
**Procedura** sopra il box scriveva già *«Quando Thorik tocca la
Corona»*, e il box lo ripeteva in seconda persona. Togliere la ripetizione
non ha tolto un'informazione a nessuno — ha tolto una riga che diceva due
volte la stessa cosa, la seconda delle quali decideva per il giocatore.

⚠️ **Il rapporto fra rilievi e difetti veri cambia per arco, e dice qualcosa
sullo stile.** ARC-07 corregge 64 rilievi su 75 (85%): il sensoriale lo
scrive in narrazione. ARC-08 e ARC-09 ne correggono 8 su 17 (47%): il
sensoriale lo mettono in bocca a un personaggio. Non è che i due archi più
recenti siano più disciplinati — è che hanno un'altra forma, e su quella
forma la norma ha meno presa.

1. **Il rilevatore entra nel repo prima delle correzioni**, come congegno di
   `misura_craft` (`--p1`), riusando `box_read_aloud`: *una norma, un
   rilevatore*. Registrato in `REGISTRO-NORME-EDITORIALI`, provato
   all'indietro dai test.
2. **Le correzioni, in quattro giri** per non fare un commit illeggibile:
   ARC-07 master DEF (17) · ARC-07 beat non consolidati P1/P2/P3 (55) ·
   ARC-08 e ARC-09 (21) · schede e fonti d'artefatto in `PG/` (11).
3. **Il criterio di correzione**, dalla norma *Dungeon* e non dal gusto: il box
   descrive **quello che c'è**, e lascia al giocatore sia l'ingresso sia la
   reazione. *«Entrate e vedete un altare»* diventa *«Al centro della sala, un
   altare»*. ⚠️ **La seconda persona resta legittima in due casi**, e non sono
   un'esenzione ma il perimetro della norma: il **dialogo** (un PNG o un
   artefatto che parla al suo portatore) e la **visione interiore** già
   accaduta al personaggio.

### 2D · Le caratteristiche entrano fra le cose misurate ✅ *(chiuso 2026-09-20)*

1. Nuovo controllo in `validate_prosa.py` sulle quattro forme di §1.3
   (l'unico posto del repo dove vivono i controlli di norma editoriale sul
   testo di gioco), con la soglia a **zero** perché il repo è a tre.
2. Le **tre violazioni vere** corrette.
3. `RICERCA-STANDARD-PROSA-WOTC-PAIZO` §3: la voce *«non misurabile»* si
   **ritira**, con la misura accanto. Una ricerca che sbaglia una previsione e
   non la corregge vale meno di una che non l'aveva fatta.
4. `ADR-0060` — *la forma rende misurabile ciò che la parola non distingue*.
   Numero verificato libero: l'ultimo scritto è 0058, il 0059 è **prenotato**
   da `PIANO-MISURA-EDITORIALE` §F2.5.

### 2E · La sesta regola d'oro — la FASE 1 si esegue, non si ricorda ✅ *(chiuso 2026-09-20)*

> **6. Prima di modificare qualunque cosa, esegui la FASE 1 in sola lettura, e
> in quest'ordine: il registro delle norme, l'algoritmo a strati, i dati che il
> repo già possiede. Una regex nuova è l'ultima risorsa, e va provata
> all'indietro.**

L'ordine non è burocrazia: è la classifica dei difetti veri. Quattordici
misure sbagliate in questo ramo, e **nessuna** veniva da una regex scritta
male. Venivano tutte dall'aver scritto una regex **prima di guardare se il
dato c'era già**.

| Passo, in ordine | Che domanda risponde | Il file che lo risponde |
|---|---|---|
| **1 · il registro** | «questa cosa la misura già qualcuno?» | [`skills/REGISTRO-NORME-EDITORIALI.md`](../skills/REGISTRO-NORME-EDITORIALI.md) — se sì, **si riusa**: *una norma, un rilevatore* |
| **2 · l'algoritmo a strati** | «quali skill devo avere aperte per non sbagliare registro?» | [`skills/ORCHESTRAZIONE.md`](../skills/ORCHESTRAZIONE.md), le cinque domande |
| **3 · i dati del repo** | «chi sono i nomi propri? cosa è archivio? cosa è superato?» | i **322 nomi** di `Bestiario/` + `state.md`; `_SNAPSHOT-STORICO.md`; `ESCLUSI_NOME`; `ARC07-MATRICE-VERSIONI.md` |
| **4 · solo ora, una regex** | «cosa resta da misurare che nessuno misura?» | e si pubblica **con i suoi falsi positivi contati a mano** |

⚠️ **Perché una regola in più non basta, e cosa la rende diversa.** Le cinque
esistenti si eseguono a memoria, e la quarta è stata aggiunta il 2026-09-18
proprio perché *«leggi» e «misura» non dicono «eseguila»*. Quindi la sesta
arriva con **un comando**: `python3 scripts/fase1.py <bersagli>`, che stampa i
quattro passi già risolti sul bersaglio — quali norme lo coprono, quali skill
apre l'algoritmo, quali dati del repo lo riguardano, e le misure di oggi. La
regola è eseguita quando quel comando è girato, e l'output è la prova.

🔎 **Provata all'indietro sul difetto di oggi.** Lanciata su questo stesso
lotto, `fase1.py` avrebbe detto al passo 3 che
`06_Stanza-corona-di-adamantio/…/00-La Corona…` porta un `_SNAPSHOT-STORICO.md`,
e i nove box falsi non sarebbero mai entrati nel conteggio.

---

## FASE 3 — Validazione

| Prova | Criterio |
|---|---|
| `misura_craft --p1` sul repo | il conteggio **scende a 0** sui file corretti, e il rilevatore **non** si è ristretto per farlo |
| tre sabotaggi | un box con *«vedete»* reintrodotto a mano → il cancello **morde**; una `prova di forza CD 15` reintrodotta → morde; un `Nuotare +9` reso minuscolo → morde |
| `validate_norme_editoriali.py` | le due norme nuove registrate, con il loro misuratore vero |
| `misura_craft --box` su ogni file toccato | le correzioni **non** hanno fatto crescere nessun box oltre le 12 righe |
| `pytest scripts/tests -q` | verde, coi test nuovi |
| coerenza | `state.md` e `campaign-artifacts.md` concordano con §4-quater sul Rituale 4 |
| `fase1.py` gira sui bersagli di ogni lotto | e i suoi quattro passi tornano **non vuoti**: un passo vuoto è un bersaglio che nessun dato del repo conosce, e va detto |
| un test sulla sesta regola | `AGENTS.md` nomina un comando che **esiste**, con la stessa verifica di ADR-0053 sui nomi inventati |

---

## Cosa questo piano NON fa, e perché dirlo

| | Cosa | Perché |
|---|---|---|
| 🔵 | **Ribilanciare `§4` per l'Aura** | è una decisione di difficoltà, e il DM ha ora il numero per prenderla. Farla d'iniziativa vorrebbe dire alzare un boss che il DM ha già tarato |
| 🔵 | Fondere le due copie della cartella Corona (`PG/` e lo snapshot ARC-06) | l'`[INFERRED]` di `_SNAPSHOT-STORICO.md` è del 2026-07-02 e aspetta ancora il DM |
| ✅ | ~~I 51 link rotti dei booklet generati, i 27 ADR mancanti in `docs/INDEX.md`~~ | 🐛 **Nessuna delle due esisteva quando questa riga è stata scritta.** I link erano **44**, non 51, e li ha chiusi il lotto **E1 di `RIPRESA-PR`** il **12 settembre**, che nello stesso archivio li registra a zero. Gli ADR mancanti erano **zero**: il buco più grande mai avuto è stato **uno**, il 12 settembre, e dal 16 l'indice è completo. Misurato il 2026-09-21 con `validate_booklets` e `validate_docs --sorgenti`, i due comandi che la riga stessa citava. Vedi `STATO-E-ORDINE` §6.2-bis |
