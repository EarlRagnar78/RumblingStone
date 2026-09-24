# 🏗️ PIANO — Chiusura della catena editoriale

**Aperto**: 2026-08-27
**Mandato-fonte (DM)**: dopo il merge della PR #114, *«guarda la seconda
standalone… se ci sono cose nuove non presenti in questo piano aggiungile come
altri punti. Poi vai da P1 a P8 e avanti, e poi anche quelli preesistenti, così
chiudiamo qualcosa, ovviamente con un plan»*.

**Da dove viene.** Tre documenti, in ordine di età:
[`RICERCA-AUDIT-COMPONENTI`](RICERCA-AUDIT-COMPONENTI-E-LIVELLO-EDITORIALE-2026-08.md)
(agosto: cinque difetti chiusi, quattro code aperte) ·
[`RICERCA-RUOLI-EDITORIALI-COLOPHON`](RICERCA-RUOLI-EDITORIALI-COLOPHON-PAIZO-2026-08.md)
(P1-P8, più l'addendum §8 con P9-P19) · la seconda standalone
`10-stand-alone/L'abbazia Della Rotta Sicura/`, che è insieme il modello e il
caso limite.

> **La riga da ricordare**: dei diciannove punti, **dodici non chiedono nessuna
> decisione** — sono lavoro che si può fare oggi. Tre sono decisioni del DM e
> bloccano gli altri quattro. Questo piano mette i dodici davanti.
>
> **Stato al 2026-09-02**: chiusi **A, B, C, D**. Restano **E** e **G** (nessuna
> decisione richiesta), **H1** (le 75 schede: fatica, non decisione) e **F**, che
> sono le quattro domande al DM. Il DM ha aggiunto **P20** (corpo + appendici) e
> confermato **P16** (tavole di supporto): entrambi chiusi dentro C.
>
> **Aggiornamento 2026-09-02 (sera)**: chiuso anche **E**. Aperto **Lotto P** dal
> rilievo del tavolo — prosa tradotta e incoerenze, echi compresi — che fa
> **scattare la condizione di riapertura scritta in ADR-0016**.

---

## §1 · Lo stato in una tabella

Diciannove punti, più le quattro code preesistenti. La colonna «gate» è ciò che
decide l'ordine, non il costo.

| | Punto | Origine | Gate |
|---|---|---|---|
| P1 | Colophon nei volumi (crediti, licenza, edizione, versione, data) | colophon C1 | ✅ **fatto** (lotto B, ADR-0023) |
| P2 | Skill `rumblingstone-edizione` + gate IP d'uscita | colophon C1+C3 | ✅ (E, ADR-0024) |
| P3 | Passate redazionali + `validate_lingua.py` | colophon C2 | ✅ (D + E) |
| P4 | **Vendoring dei pacchetti Typst** | colophon §5 | ✅ **deciso: sì** (F1) |
| P5 | `pdfcpu` per l'imposizione | colophon T1 | ✅ **deciso: sì** (F2) |
| P6 | Server MCP sui 44 tool già descritti | colophon MCP-1 | — |
| P7 | veraPDF + caratteri per riga + daltonismo | colophon T3/T6/T7 | dopo P1 |
| P8 | `dm.py volume` — l'ordine dei mestieri | colophon §3.4 | dopo P1-P3 |
| P9 | Riscalatura a tre assi | Abbazia | ✅ (C) |
| P10 | Avvertenza di contenuto e consenso del tavolo | Abbazia | ✅ (C) |
| P11 | Igiene di licenza per documento | Abbazia | ✅ (E, §2) |
| P12 | ADR di modulo | Abbazia | ✅ (C) |
| P13 | Indirizzamento delle aree fra documenti + gate | Abbazia | ✅ (D) — trova 10 ambiguità vere |
| P14 | Il limite dichiarato del dry-run | Abbazia | ✅ (C) |
| P15 | Cancelli d'uscita a tempo per atto | Abbazia | ✅ (C) |
| P16 | Tavole non zenitali (veduta, profilo, tempi) | Abbazia | ✅ (C) — confermato dal DM |
| P17 | ⚠️ **L'Abbazia è fuori da ogni catena** | Abbazia | 🟡 gate fatto (A); ✅ **deciso: convertire** (F4) |
| P18 | ⚠️ `LICENSE` GPL-3.0 su un'opera testuale | Abbazia | ✅ **deciso: CC BY-NC-SA + MIT** (F3) |
| P19 | Tabelle vive del borgo (dicerie false, reazione) | Abbazia | ✅ (C) |
| **P20** | ⭐ **Corpo + appendici** (punto nuovo del DM, 2026-09-02) | Abbazia | ✅ (C) — verificato che non era persa: **mai esistita** |
| — | E8: 75 schede di bestiario su 157 non migrate | audit ago. | fatica, non decisione |
| — | Capolettera annegato · indice analitico | audit ago. | = P4 |
| — | Imposizione | audit ago. | = P5 |
| — | CMYK / PDF-X | ADR-0020 | rinuncia dichiarata |
| **P21** | ⚠️ **Validatore di prosa** (traduttese + tic dell'IA a densità) | tavolo 2026-09-02 | — |
| **P22** | ⚠️ **Coerenza d'ambientazione** su tutto il contenuto, **echi compresi** | tavolo 2026-09-02 | — |

---

## §2 · I lotti

Ordinati per **quanto si chiude senza chiedere niente a nessuno**.

### ✅ Lotto A — Il gate che manca sull'Abbazia (P17, parte 1) — *chiuso 2026-09-02*

Il difetto più urgente dei nuovi, e la sua metà indolore.

*Il fatto*: `10-stand-alone/` non corrisponde a nessun pattern dei validatori:
la CI conosce `STANDALONE-*` (il Drappo) e basta. Quattro file, ~2.750 righe, e
**nessun controllo di nessun tipo**: un link rotto, un'area rinumerata o un file
rinominato non li vede nessuno finché non si apre al tavolo.

- [x] **A1**: `validate_standalone.py` riconosce `10-stand-alone/*/` come
      **seconda famiglia**: `<title>` non vuoto, almeno un `<h1>`, link relativi
      risolvibili, ancore esistenti **anche verso un altro file del modulo**,
      `id` non duplicati, termini 5e vietati sul testo spogliato dei tag.
- [x] **A2**: step CI rinominato e bloccante; 14 test in `test_standalone_html.py`,
      su cartelle temporanee e **non** sull'Abbazia (un test che dipende dal
      contenuto di un modulo vero diventa rosso il giorno in cui il DM lo riscrive).
- [x] **A3**: riga in `scripts/README-automation.md` + `tools.manifest.json`
      aggiornato e artefatti derivati rigenerati (`docs/tools/*`).

**Esito.** Verde sull'Abbazia com'è. Criterio d'accettazione soddisfatto su sei
casi: ancora rotta, `id` duplicato, `<h1>` tolto, link relativo inesistente,
ancora inesistente nel file di destinazione → **exit 1**; ripristinati → **exit 0**.

🔎 **Trovato guardando, dove il gate non arriva da solo:**

1. **L'«indice navigabile delle 48 aree» non è navigabile**: `indice_maestro.html`
   non contiene **un solo** `href`. I 47 `href` del modulo sono tutti `#bg`/`#bgb`,
   cioè riferimenti interni alle tavole SVG. Non è un errore, non c'è niente di
   rotto, ma la promessa del titolo non è mantenuta. È contenuto del DM: **non
   toccato**. Va con P13 (lotto D), dove l'indirizzamento fra documenti diventa
   una convenzione.
2. Il modulo **non ha master markdown**: il validatore ora lo dice a ogni
   passata come *warning*, così la cosa non sembra normale. Resta la domanda F4.

**Deliverable**: un gate rosso se qualcuno rompe l'Abbazia.
**Criterio d'accettazione**: rompere di proposito un'ancora → CI rossa; ripararla → verde.
**Engine**: Sonnet · **impegno** medio · **dieta**: `scripts/validate_standalone.py`, `.github/workflows/ci.yml`, i 4 file dell'Abbazia.

> ⚠️ **Quello che questo lotto NON fa**: portare l'Abbazia dentro la catena
> (master markdown + manifest, ADR-0003). Quella è una conversione vera, sta nel
> **Lotto F**, e va decisa — non fatta di soppiatto.

### ✅ Lotto B — Il colophon (P1) — *chiuso 2026-09-02* · [ADR-0023](adr/ADR-0023-colophon-di-edizione.md)

*«Se si fa una cosa sola»*, dice la ricerca. Vale ancora, e ora vale di più:
l'Abbazia dimostra che anche il modulo meglio scritto del repo esce **anonimo,
senza licenza e senza versione**.

- [x] **B1**: un **oggetto** `colophon` nello schema, non cinque chiavi piatte
      (`edizione`, `versione`, `data`, `autori`, `basato_su`, `licenza`, `nota`),
      con `additionalProperties: false`. ⚠️ **Scostamento dal piano scritto**, e il
      motivo: cinque chiavi sciolte in cima al manifest sono altrettante cose da
      ricordare; un oggetto è una cosa sola e si valida come tale. Ha richiesto di
      far **ricorrere `validate_booklets.py` negli oggetti annidati**: prima lo
      faceva solo per gli array, quindi un refuso lì dentro sarebbe passato in
      silenzio: esattamente il difetto che lo schema esiste per impedire.
- [x] **B2**, `#colophon()` nel tema: pagina **autonoma e senza testatina**, sul
      verso del frontespizio. La testatina c'era alla prima resa e ripeteva due
      volte lo stesso titolo, visto rendendo la pagina in PNG, non deducendolo.
- [x] **B3**: entrambe le catene la emettono, con **le stesse voci nello stesso
      ordine** (`VOCI_COLOPHON` in tutte e due, e un test che verifica siano
      identiche). Nessun `today()` in nessun punto.
- [x] **B4**, esemplare sul manifest del Palio: edizione, versione, data,
      `basato_su` (SRD 3.5 · OGL 1.0a · adattamento di *Red Hand of Doom*) e la
      riga di licenza che rimanda ad ADR-0005 e alla guida IP.
- [x] **B5**: 11 casi in `test_booklets.py`, fra cui la retrocompatibilità (senza
      la chiave il volume esce identico) e la parità d'ordine fra le catene.

**Esito.** Tutti e **11 i volumi del repo compilano davvero** (`validate_booklets
--stampa`, con typst 0.15.1, la stessa versione fissata in CI), e la pagina è
stata **guardata**, non solo compilata: resa in PNG e ispezionata, prima e dopo
la correzione della testatina.

⚠️ **Una riga che solo il DM può scrivere**: `autori` è deliberatamente **assente**
dal colophon del Palio. Inventare un nome in una pagina di crediti è peggio che
non averla.

**Deliverable**: PDF e HTML che portano il proprio nome, la propria data e la riga di licenza.
**Criterio d'accettazione**: `validate_booklets.py --stampa` verde e il colophon presente nel PDF compilato.
**Engine**: Sonnet · **impegno** medio · **dieta**: tema Typst, i due builder, lo schema, un manifest.

### ✅ Lotto C — Lo standard del modulo (P9, P10, P12, P14, P15, P19, **P20**) — *chiuso 2026-09-02*

Tutti punti di scrittura di skill, **zero decisioni**. È il lotto che trasforma
l'Abbazia da eccezione fortunata in regola.

- [x] **C0**, ⭐ **P20, punto nuovo del DM**: l'architettura **corpo + appendici** in testa a `module-standard`. Verificato che non era «persa» ma **mai esistita**: `grep -ril "appendice" skills/` non trova niente, nessun master `ARC*-DEF-*` la usa, il Drappo nemmeno. Il corpo è ciò che si gioca in ordine; le appendici sono ciò che si consulta a salto (bestiario, gazetteer, cast, incontri), numerate a lettere.
- [x] **C1**, `module-standard`: **riscalatura a tre assi** come sezione
      obbligatoria (livello · numero di PG · durata), con la colonna «cosa si
      perde davvero». Modello: l'indice maestro dell'Abbazia.
- [x] **C2**, `module-standard`: **avvertenza di contenuto e consenso**, con la
      sostituzione alternativa già scritta. Aggancio ad ADR-0018.
- [x] **C3**, `module-standard`: **cancelli d'uscita a tempo** per atto, con il
      rimedio (chi entra in scena e cosa dice se il segnale non è arrivato).
- [x] **C4**, convenzione **ADR di modulo**: quando una decisione è locale e
      quando sale in `plans/adr/`.
- [x] **C5**, `playtest`: la **dichiarazione del limite** del dry-run: cosa non
      ha potuto verificare, e perché solo il tavolo può.
- [x] **C6**, `narrative-style`/`indagine`: **dicerie con falsi deliberati** e
      **tabella di reazione**. Una diceria falsa è un nodo d'indizio a costo zero.
- [x] **C7**: `playtest` §2.6 rimanda a C1 invece di coprire il solo numero di giocatori.
- [x] **C8**: **P16 confermato dal DM** («per le mappe vanno bene le verticali,
      aggiungendo anche le visualizzazioni presenti nella standalone»):
      `mapmaking` guadagna **le tavole di supporto**: veduta, profilo laterale con
      quote e **tempi di percorrenza**, con la regola che si aggiungono *quando
      rispondono a una domanda che la griglia non può*, non per completezza, e la
      numerazione `Tavola I` / `I-a` / `I-b` che le tiene riconoscibili come lo
      stesso luogo visto in un altro modo.

**Deliverable**: sei convenzioni scritte dove un agente le incontra.
**Criterio d'accettazione**: `validate_skills.py` verde; ogni voce cita l'Abbazia come implementazione di riferimento.
**Engine**: Opus (sono decisioni di design) · **impegno** alto · **dieta**: le tre skill toccate + le sezioni citate dell'Abbazia, **non** i quattro file interi.

### ✅ Lotto D — I gate a macchina (P13, P3) — *chiuso 2026-09-02*

- [x] **D1**, **numerazione delle aree**: prefisso di livello obbligatorio, e
      `validate_modules.py` che rifiuta una collisione fra documenti dello stesso
      modulo. È il difetto **D1 del dry-run dell'Abbazia** (16/17/18 usati tre
      volte su tre file): una macchina lo trova gratis, un umano lo trova al tavolo.
- [x] **D2**, `scripts/validate_lingua.py`, stdlib: perché/perchè, virgolette
      dritte, doppi spazi, apostrofi, d eufonica. Non bloccante alla prima
      passata, poi bloccante quando il rumore è a zero.
- [x] **D3**: entrambi in CI + `tools.manifest.json` + `README-automation` + test.

**Esito.**

- **D1** trova **dieci ambiguità vere e tuttora aperte** nell'Abbazia: il dry-run
  del modulo aveva corretto la numerazione nelle *chiavi* con i prefissi di
  livello, ma i rimandi **in prosa** sono rimasti nudi: 55 `area N` senza
  prefisso, e dieci numeri (`area 6`, `area 27`…) usati in **file diversi**. Da
  fuori non si distingue se sono la stessa stanza o due. È **warning**, non
  errore: la convenzione nasce oggi.
- **D2** trova **23 refusi** in 494 file di contenuto: spazi prima della
  punteggiatura, doppi spazi, un «ad Damarath». Anche questo **non bloccante in
  CI** (`continue-on-error`), come `validate_bestiario --rules`: diventa `--strict`
  il giorno in cui il rumore è a zero. Un validatore rumoroso viene disattivato
  entro una settimana, e allora non trova più nemmeno i refusi veri.
  ⚠️ **La prima passata produsse 423 rilievi, quasi tutti creati dal validatore
  stesso**: mascherava il codice inline con *uno spazio* e poi segnalava i doppi
  spazi che aveva introdotto. Metà dei 14 test esistono per quel difetto.
  Esentate anche le **guide alla pronuncia** (`*nè-this*`), dove l'accento grave
  dice il suono ed è messo apposta.

### ✅ Lotto E — La skill dell'edizione (P2, P11, P3-prosa) — *chiuso 2026-09-02* · [ADR-0024](adr/ADR-0024-skill-edizione.md)

- [x] **E1**, ADR: perché la diciassettesima skill è giustificata (la
      motivazione è già scritta nella ricerca §3.1; qui diventa decisione).
- [x] **E2**, `skills/rumblingstone-edizione/`: colophon, dichiarazioni Product
      Identity/Open Content, **gate d'uscita** (la checklist §7 di
      `GUIDA-CONDIVISIONE-IP.md`, che oggi nessuna skill carica), versione ed errata.
- [x] **E3**: **igiene di licenza per documento** (P11) come tabella obbligatoria
      in stesura. L'Abbazia è l'implementazione di riferimento: ha separato le
      divinità inventate dai nomi FR non-SRD *prima* del commit, non dopo.
- [x] **E4**: `references/passate-redazionali.md` in `narrative-style`: le tre
      passate, quando un master è chiuso, come si riapre.

**Esito.** `skills/rumblingstone-edizione/` è la **diciassettesima** skill, e
ADR-0024 la motiva invece di darla per scontata: il fatto misurato è che
`grep -rl "GUIDA-CONDIVISIONE-IP" skills/` restituiva **un solo file**, e per
un'altra ragione: un agente che generava un handout **non incontrava mai** il
gate d'uscita. Una regola scritta che nessuno carica non è una regola.

Le sezioni: il gate d'uscita (le cinque domande del §7 della guida, con la
guida dichiarata **fonte** in caso di divergenza) · l'igiene di licenza compilata
**in stesura**, con l'Abbazia come esemplare che ha separato le divinità
inventate dai nomi FR *prima* del commit · quando si compila il colophon e con
che valori (⛔ mai un `autori` inventato) · l'edizione come oggetto:
versione, ristampa, errata, oggi **convenzione e non meccanismo**, dichiarato ·
i confini con le altre cinque skill · e quando **non** serve.

`references/passate-redazionali.md` in `narrative-style`: le tre passate
(struttura → voce → bozze), la 2ª **letta ad alta voce** perché il traduttese si
sente e non si vede, gli **echi trattati come testo** e non come note, quando un
testo è chiuso e i tre soli casi che lo riaprono.

### ✅ Lotto P — La prosa e la coerenza — *chiuso · 2026-09-02* · [ADR-0025](adr/ADR-0025-riapertura-prosa-tradotta.md)

Aperto dal rilievo del tavolo del 2026-09-02: *«incoerenza e prosa inglese
tradotta male, anche negli echi»*. **ADR-0016 aveva scritto la condizione di
riapertura, e la condizione è scattata.**

- [x] **P-0**: **ADR-0016 riaperta** con [ADR-0025](adr/ADR-0025-riapertura-prosa-tradotta.md): la decisione resta (l'italiano è la lingua sorgente), cambia la *misura*. Tre date lette insieme (2026-07-31, 2026-08-01, 2026-09-02) e in mezzo un motore di stile da 2047 righe: l'ipotesi «manca la norma» è falsificata. *Era*: riaprire ADR-0016 con una revisione: non per cambiare la
      decisione (l'italiano resta la lingua sorgente; il rilievo dice che la
      qualità non basta, non che serva l'inglese), ma per registrare che il banco
      di prova ha dato esito negativo e cosa si fa di conseguenza.
- [x] **P-1**, `scripts/validate_prosa.py`: i calchi a firma inequivocabile e i
      **tic a densità** (antitesi «non X: è Y» max 1 per documento, maiuscole di
      portento max 1, trattini lunghi). Non bloccante alla prima passata, come
      `validate_lingua`.
- [x] **P-2**: il controllo del **glossario** è dentro `validate_prosa.py` invece
      che in `validate_modules.py`: è la stessa preoccupazione («la prosa suona
      inglese») e tenerla in un tool solo evita di doverla cercare in due.
      Legge `GLOSSARIO-E-LOCALIZZAZIONE.md`, salta le voci **DNT** (*Aegis Fang*
      e *Skullcrusher* sono inglesi per scelta) e segnala la forma inglese dove
      il canone vuole l'italiano.
      🔎 **Trova 12 casi veri**, fra cui *Anvil of the World* in **15 file** dove
      il canone dice *Incudine del Mondo*, *Necklace of Eternal Seeds* in 4,
      *Crown of Adamantine* in 3. È il rilievo del tavolo nella sua forma più
      letterale e più facile da correggere.
- [x] **P-4**: ⭐ **la correzione che risponde alla domanda del DM** («c'è una
      skill di prosa ma forse va limata?»). La skill non va riscritta: sono 2047
      righe e la norma è esatta. Va spostato **un punto del load order**:
      `italiano-nativo.md` era al **5**, «obbligatorio prima di consegnare»;
      passa al **4**, «prima di scrivere». Il traduttese non è una lista di
      errori da correggere in revisione, è **come la frase è stata costruita**:
      correggere dopo cambia le parole e lascia il respiro. La checklist di 30
      secondi resta come ultima passata, e ora rimanda a `validate_prosa`.
- [x] **P-5**: ⭐ **Il buco che il DM ha trovato con una domanda**: *«il validatore
      va anche negli altri contenuti, o solo gli echi sono corretti?»*. Misurato, ed
      era vero: su `02-HINT-THORIK.md` i controlli sui tic coprivano **29 parole su
      353, l'8%**, perché guardavano solo dentro `> *…*`. Ora un **file per i
      giocatori** (hint, teaser, echi, handout, lettera, prop, `pg-*`) è prosa da
      leggere **per intero**, meno i titoli; un file del DM (regia, guida, cassetta,
      statblocchi) resta fuori. Effetto immediato: i cinque file della sessione
      Terros passano da **0 rilievi a 8**.
      🔎 Due falsi positivi trovati e chiusi nella stessa passata, perché stavano
      **punendo le convenzioni del repo**: l'**etichetta di battuta**
      (`**AEGIS FANG**,` e `**I BRACIERI:**`, il formato che `editorial-standards.md`
      §2 impone) contata come maiuscola di portento, e il **cappello del DM** in
      testa agli hint, che sta su più righe di blockquote e va tolto per blocchi.
- [x] 🟢 **P-3**, **diagnosi fatta, sui file giusti.** Il DM ha indicato quali:
      gli hint di **Artemis e Thorik** prima dello scontro con Terros, non i
      registri `*ECHI*` che avevo scansionato all'inizio (quelli sono ledger di
      conseguenze). Con la copertura di P-5 il validatore ora ci trova:
      **THORIK** due antitesi «non X: è Y» in un documento · **TORDEK** un
      progressivo e due maiuscole d'enfasi · **ARTEMIS** «la tua testa» ·
      **HELLA** «le tue mani», un progressivo, due maiuscole · **TEASER** due
      maiuscole. Sono i tic del §9, non i calchi: la sintassi è giusta e le
      **abitudini** sono sempre le stesse, che è precisamente ciò che il tavolo
      sente quando dice «suona strano».
      ⬜ **Resta la riscrittura**, che è lavoro di voce sul canone e va fatta con
      il DM davanti, non alla cieca.
- [x] **P-6**, ⭐ **Il caso Hella**: la giocatrice ha detto di **non capirci
      niente**. `validate_prosa` su quel file è pulito, quindi non era prosa: era
      **progetto**. Misurate le ancore nominate nella prosa dei quattro testi
      per-PG della stessa sessione: Tordek **8**, Thorik **5**, Artemis **4**,
      **Hella 0** (le due che risultavano stanno nel titolo e nella nota del DM).
      Riceve «una testa grande, ossuta» (è Durik), «spalle larghe, oneste» (è
      Thorik): quattro immagini non attribuite di fila.
      Due regole in `consequence-echoes.md` §3-ter: **almeno un'ancora nominata**,
      e **anche il frammento oscuro porta una riga di lettura**. Il confronto è
      dentro la stessa sessione: Tordek dichiara il frammento incomprensibile *e*
      chiude con «qualcosa di caro sta cercando la strada di casa», il giocatore
      non sa cosa, ma sa verso dove; Hella ha «non capisci le parole, ma il senso
      è inequivocabile», che **afferma** un senso senza consegnarlo.
- [x] **P-7**: ⭐ **Il controllo automatico, dopo l'obiezione del DM** («migliora
      il controllo, altrimenti non si corregge niente»). Aveva ragione: la prima
      stesura dava il risultato **rovesciato** e l'avevo tolta invece di
      ripararla. Due cause, entrambe riparate:
      1. **mancavano le forme brevi**: il canone in prosa scrive «la Corona» e
         «l'Anello», non «Corona di Adamantio»: ora ogni voce del glossario
         contribuisce le sue parole piene, più una lista di alias dichiarata;
      2. **il confronto era case-insensitive**: e metà delle forme brevi sono
         anche nomi comuni: *«batteva il cuore»* non è il **Cuore di Moradin**,
         *«voci di cristallo»* non è un artefatto. La **maiuscola** è l'unico
         segnale affidabile che il testo offre.
      **Esito**: corretto su tutti e quattro i file della sessione, e su tutto il
      repo segnala **un solo file**, quello che la giocatrice aveva segnalato.
      Perimetro dichiarato: vale dove il glossario **è** il canone, quindi i
      moduli autoconclusivi restano fuori (il Drappo è a Tarsilia, su Golarion:
      i suoi nomi non stanno nel glossario di RumblingStone e non devono starci).
      7 test dedicati, fra cui la regressione del «cuore» minuscolo.
- [x] ⭐ **P-8**, **l'eco di Hella riscritto, e il tavolo può giudicarlo.** La
      diagnosi di P-3 diceva *dove*; questo è il *cosa*. Applicate le due regole
      appena scritte in `consequence-echoes.md` §3-ter, sul file che il
      validatore segnalava da solo su 333:
      - **un'ancora nominata per eco**, presa dal canone del DM e non inventata:
        **Durik** (regia §1, «l'Impronta di Durik è caduta nel Sogno della
        Terra») · **Thorik** (regia punto 5: la giocatrice «ha lo stesso momento
        dal suo lato») · **l'Incudine del Mondo** e la risposta a Moradin (il suo
        stesso viaggio, canone giocato). Nessuna è un'anticipazione: sono cose
        che **Hella** sa e gli altri PG no, ed è la direzione in cui gli echi
        viaggiano.
      - **la riga di lettura anche dove resta oscuro**: *«Le parole non le
        capirai: non sono per te. Il tono sì.»* al posto di *«non capisci le
        parole, ma il senso è inequivocabile»*, che affermava un senso senza
        consegnarlo.
      - **il cappello non chiude più la porta**: *«Sono oscuri di proposito, non
        vuoti»*, e la domanda al DM a fine serata è esplicitamente concessa.
      - via anche i tre rilievi meccanici che restavano: *«le tue mani»* →
        *«le mani»*, *«sta aspettando»* → tolto, e l'antitesi *«Non sai se… Non
        sai se…»* sostituita dal pagamento che mancava (*«Lui non sa che sei tu.
        Ma il peso si alleggerisce, e lui lo sente»*).
      **Accettazione**: `validate_prosa.py` sul file → `✓ nessun calco, nessun
      tic oltre soglia`, ancora inclusa. Prima: 3 rilievi, fra cui l'unico
      «senza una sola ancora nominata» del repo. ⚠️ È **canone di tavolo**: il
      DM lo approva o lo revoca in un commit; la versione precedente sta nella
      storia di questo file.

**Esito.** `validate_prosa.py` misura **154 rilievi** in 333 file, e ha richiesto
una taratura vera: la prima passata ne produceva **256** perché segnalava il
progressivo e il possessivo *ovunque*, ma *«sta piovendo»* è italiano corretto.
Separati in due famiglie (**sempre** vs **solo read-aloud**): 110, più 12 del
glossario e i tic a densità. **24 test**, di cui una classe intera (`TestRegistri`)
esiste per quel falso positivo.
⭐ Il pezzo che vale di più sono **i tic a densità**: «massimo uno per documento»
è la regola che un revisore umano non applica mai, perché dovrebbe **contare**.
L'antitesi si riconosce dalla forma, e prende tutti e quattro gli esempi di
`italiano-nativo.md` §9.1 (copula, verbo, sostantivo, trattone).
⚠️ **Quello che NON fa**: trova «realizzi che», non trova una scena che suona
tradotta pur essendo in italiano corretto. Quella è la 2ª passata umana, e la
diagnosi sugli echi (P-3) lo dimostra sul campo.

### ✅ Lotto F — Le decisioni del DM — **prese E ESEGUITE tutte e quattro il 2026-09-02**

Qui non si eseguiva: si chiedeva. **Le risposte ci sono**, e sbloccano H2, H3 e la
conversione dell'Abbazia. L'esecuzione di ognuna porta con sé il suo ADR, che si
scrive **con** l'implementazione, perché la sezione «conseguenze» di un ADR
compilata prima di aver eseguito è metà ADR.

- [x] ✅ **F1, ESEGUITO** (2026-09-02) · [ADR-0026](adr/ADR-0026-vendoring-pacchetti-typst.md)
      **`droplet` 0.3.1** (MIT, © Eric Biedert) e **`in-dexter` 0.7.2** (Apache-2.0,
      JKRB) vendorizzati in `scripts/typst/packages/preview/<nome>/<versione>/`,
      copiati da `typst/packages` al commit `359500f2`, 112 KB in tutto, tolti i
      file che il loro stesso `typst.toml` dichiara in `exclude`, **`LICENSE`
      integri**. `export_booklet_typst.py` passa ora `--package-path`.
      **Accettazione, misurata e non asserita**: lo stesso documento che importa
      entrambi **compila** col percorso vendorizzato e **fallisce** senza
      (*«failed to download package»*: qui `packages.typst.org` è davvero
      irraggiungibile, quindi la prova è vera e non simulata); la cache utente
      di typst resta **inesistente** dopo la compilazione.
      `scripts/tests/test_pacchetti_typst.py`: **7 test**, fra cui la versione
      del `typst.toml` confrontata con quella della cartella; copiare il nuovo
      dentro la cartella vecchia è l'errore facile, e l'import continuerebbe a
      dire `0.3.1` mentre il codice è un altro, e una compilazione con
      **l'ambiente ripulito** (niente proxy, niente `HOME`).
      **Sblocca H2**: capolettera annegato e indice analitico erano la stessa
      decisione, ed è presa.
- [x] ✅ **F2, ESEGUITO** (2026-09-02) · [ADR-0027](adr/ADR-0027-imposizione-con-pdfcpu.md)
      `pdfcpu` accettato come seconda dipendenza binaria (Apache-2.0, eseguibile
      Go statico, `booklet` nativo), e la **regola di degradazione pulita scritta
      in codice** invece che in un piano: `scripts/binari.py`. `esigi()`
      restituisce il percorso **oppure esce con 2** (`MANCA`, distinto da 1 =
      «ho provato e fallito») **prima** di aprire qualunque file di destinazione
      Il difetto da evitare non è un crash, è un PDF di 40 pagine su 96
      indistinguibile da uno buono. Ogni binario dichiara il suo **ripiego**.
      La regola ha **due utenti**: `typst` è stato portato sopra lo stesso helper
      nello stesso commit, perché una regola con un utente solo è un caso
      particolare. `dm.py doctor` ora li elenca.
      **Verificato sul campo, non supposto**: `pdfcpu v0.11.0` su
      `ARC07-TEASER-GIOCATORI-STAMPA.pdf`: 3 pagine A4 → **2 fogli**, exit 0.
      ⚠️ E una scoperta che l'ADR registra invece di nascondere: **l'output non è
      byte-identico fra due esecuzioni**. Misurata la causa: è la seconda metà
      dell'array `/ID`, che `pdfcpu` rigenera a ogni scrittura; `CreationDate` e
      `ModDate` sono identici e **i flussi di contenuto delle pagine hanno lo
      stesso md5**. Quindi *il documento è deterministico, il file no*, e ne
      segue la regola: un PDF imposto **non si versiona e non si confronta a
      byte**. Invocazione sempre con `-c disable` (altrimenti `pdfcpu` scrive
      `~/.config/pdfcpu/` e installa un font sulla macchina di chi lo esegue) e
      `-o` (niente rete, come ADR-0026).
      **Sblocca H3**: l'imposizione, cioè un libretto invece di una risma.
      `scripts/tests/test_binari.py`: **8 test**, fra cui *«ogni binario cita un
      ADR che esiste davvero»*: una dipendenza binaria senza ADR è una
      dipendenza entrata di nascosto.
- [x] ✅ **F3, ESEGUITO** (2026-09-02) · [ADR-0029](adr/ADR-0029-licenza-doppia-testo-e-script.md)
      `LICENSE` **CC BY-NC-SA 4.0** sul testo, `scripts/LICENSE` **MIT** sugli
      strumenti, e `LICENSES.md` in radice che spiega il taglio. La regola per i
      casi di confine sta scritta: *se lo legge un essere umano al tavolo è testo,
      se lo esegue una macchina è strumento*.
      Il difetto che chiude (P19): **il file di licenza e la postura del progetto
      si contraddicevano.** ADR-0005 dice «uso non commerciale»; la GPL
      *garantisce espressamente* il diritto di vendere copie. In un contenzioso
      conta il file.
      I due testi sono presi **verbatim** da `spdx/license-list-data` al commit
      `a522a89`, non riscritti a memoria, che su un testo legale è il modo di
      introdurre una differenza che nessuno rileggerà mai.
      ⚠️ **Quello che una licenza doppia rischia di far dimenticare**, e che
      ora stanno scritte dove si guarda:
      1. **il contenuto SRD resta Open Game Content sotto OGL 1.0a**: non va
         sotto CC, e chi lo ridistribuisce si porta dietro la **Sezione 15**. È
         entrato nel cancello d'uscita §7;
      2. **i marchi altrui non si licenziano perché si nominano**: *Forgotten
         Realms* non diventa nostro da dare;
      3. **MIT su `scripts/` non copre `scripts/typst/packages/`**: quello è
         codice di terzi con la sua licenza (ADR-0026).
      ⚠️ E **ADR-0005 non viene allargato, prevale**: una licenza dice cosa
      possono fare gli altri con ciò che pubblichiamo; ADR-0005 dice **se e cosa**
      pubblichiamo. Sono due domande diverse e la seconda viene prima. Per il caso
      limite («non commerciale» non è definito con precisione in CC 4.0: un
      Patreon, un tavolo a pagamento) la risposta non sta nella licenza:
      **fermarsi e chiedere**.
- [x] ✅ **F4, ESEGUITO** (2026-09-02) · [ADR-0028](adr/ADR-0028-abbazia-master-markdown.md)
      Quattro master markdown, un manifest col **colophon**, **sette tavole**
      estratte in `tavole/*.svg`, e le due catene che compilano: HTML 615 KB,
      **PDF di 34 pagine** con frontespizio, colophon e segnalibri.
      Il travaso l'ha fatto uno strumento, `scripts/import_html_module.py`, che
      conosce il vocabolario di questa famiglia (`p.ra` → blockquote,
      `div.warn/.mech/.sb/.meta` → `{{note}}`, `div.entry` → chiave d'area,
      `figure > svg` → file separato) e **davanti a un tag che non conosce lo
      dichiara** invece di inventare una traduzione. È **una volta sola** e lo
      impone: se i master esistono già si ferma, perché da lì in poi il markdown
      è il master e rilanciare butterebbe via le correzioni in silenzio.
      **Accettazione, perdita di contenuto: zero parole su ~20.000.** È il
      confronto che ha trovato tutto il resto, e che nessuna compilazione verde
      avrebbe trovato:
      - `megereGrinza`: una mia ripulitura di «`** **`» cancellava lo **spazio**
        fra due neretti adiacenti, dentro un nome proprio;
      - i nomi dei PNG **sparati fuori da una tabella** da un `<br>` dentro una
        cella (`<td><b>Dama Orsola Rive</b><br>guerriero 5</td>`);
      - la barra `.meta` che stavo **buttando via**, e che invece dice
        *«Sostituisce: Tavola I e il blocco Il conto che non torna»*: il
        rapporto fra un'appendice e il documento principale, non impaginazione;
      - **11 read-aloud su 11**: stavano su `<p class="ra">`, non su un `div`, e
        la prima versione li appiattiva tutti in prosa normale. Tre stanno dentro
        un riquadro d'avviso, dove l'etichetta `⚠` finiva davanti al `>` e
        scioglieva la citazione.
      ⚠️ **E due difetti che si vedevano solo guardando la pagina**, non
      compilandola: i `<defs>` condivisi lasciati indietro (ogni tavola citava
      `url(#rock)` da un file che non c'era più) e, peggio, `html.parser`
      **minuscola tutto mentre XML è case-sensitive**: `viewBox` → `viewbox`
      spariva, `patternUnits` → `patternunits` faceva tornare il riempimento del
      mare al default e lo riduceva a **un quadratino azzurro nell'angolo**. Il
      file restava XML valido. Per questo le pagine sono state **renderizzate e
      guardate**, non solo compilate.
      🔑 Le chiavi d'area prendono il codice: `#### 22 Le Celle` → `#### C22`.
      Nella conversione la collisione era finalmente a occhio nudo, nello
      **stesso file** c'erano `#### 3 Corpo di Guardia` (borgo) e `#### 3 Navata`.
      `scripts/tests/test_import_html_module.py`: **15 test**, uno per difetto
      vero.
      ✅ **Prerequisito chiuso** (2026-09-02): i rimandi `area N` senza prefisso
      sono **da 55 (10 ambigui fra file) a 0**. Lo schema non l'ho inventato: era
      già scritto nell'**indice maestro del modulo**, che aveva diagnosticato il
      difetto (*«16, 17, 18 usati tre volte su tre documenti»*) e prescritto la
      correzione minima: *i numeri restano, si aggiunge un prefisso di livello*,
      senza però propagarla negli altri tre file. Le 48 aree hanno un codice
      autoritativo: **B** borgo · **A** abbazia livello 0 · **T** campanile ·
      **C** cripta −1 · **G** grotta −2 · **X** contado. Applicato a tutti e 54 i
      rimandi, uno per uno.
      ⚠️ Due numeri significavano **due posti diversi nello stesso file**, e sono
      la prova che l'ambiguità non era teorica: `area 6` era la **sacrestia (A6)**
      in una riga e il **registro dei defunti della cappella del borgo (B6)** in
      un'altra; `area 8` era la **loggia (A8)** e il **punto del ritrovamento
      (B8)**. Quelli sono stati risolti per contesto, mai in blocco.
      🔧 E la sostituzione meccanica ha rotto cinque articoli elisi: *«Con l'area
      4 profanata»* → *«Con l'A4»*, che non è italiano. Corretti a mano: un
      codice d'area l'articolo non lo vuole. È il motivo per cui un rename di
      massa si rilegge invece di fidarsene.
      🔎 **Resta aperto, e va detto**: 63 rimandi in forma **parentetica nuda**,
      *«la chiave è in sacrestia (6)»*, *«la botola in cappella (9)»*. Stessa
      classe di ambiguità, ma il gate non li vede e **non si sistemano alla
      cieca**: un `(8)` può essere un'area, un risultato di dado o una CD.
      Diventa **P-23**, non un colpo di `sed` dentro questo lotto.

**Deliverable**: ✅ quattro risposte, prese. Gli ADR si scrivono con l'esecuzione.
**Ordine consigliato d'esecuzione**: F1 (sblocca due code a costo basso) → F2 →
F4 (il più grosso, e va dopo il lotto D sulla numerazione) → F3 (tocca ADR-0005).

### ✅ Lotto G — Infrastruttura (P6, P7, P8, P16)

- [x] ✅ **G1, ESEGUITO** (2026-09-02) · [ADR-0030](adr/ADR-0030-server-mcp-sui-tool.md)
      · progetto per esteso in [SPEC-SERVER-MCP.md](SPEC-SERVER-MCP.md)
      `scripts/mcp_server.py`: JSON-RPC 2.0 su stdio, stdlib, catalogo derivato
      dal manifest. `initialize` · `tools/list` · `tools/call` · `ping`.
      ⭐ **La fonte di verità ha finalmente un lettore, e ha subito trovato tre
      difetti che nessuno vedeva perché nessuno la leggeva:**
      1. **tre delle 48 voci erano cartelle**, non programmi: `converters/`
         html-to-markdown, pdf-to-md-engine e image-to-webp hanno per invocazione
         *«(vedi …/README)»*. Il descrittore prometteva tre tool che non partono;
      2. **`invocation` non è un comando**: è una riga d'esempio per umani, e
         mescola l'eseguibile con segnaposto e flag di comodo (`MANIFEST.json`,
         `<cartella>`, `--all`, `--check`). **Nove tool su quarantasei** ne hanno
         uno: un server che la usasse verbatim lancerebbe `--all` che nessuno ha
         chiesto. Il comando si deriva da `path` + `language`;
      3. **nessuna voce portava gli effetti collaterali**: un client non
         distingueva `validate_prosa` da `state_apply`. Ora ci sono le
         annotazioni MCP (`readOnlyHint`, `destructiveHint`, `idempotentHint`).
      `mcp-tools.json` scende da 48 a **46** voci: è una correzione, non una
      perdita.
      🔒 **Sei difese, un test a testa**, perché un processo che lancia 46
      programmi per conto di un agente è una superficie d'esecuzione: **S-1** solo
      allowlist · **S-2** niente shell (argv come lista) · **S-3** schema validato
      prima di partire · **S-4** percorsi confinati sotto la radice · **S-5**
      read-only per difetto · **S-6** timeout e tetto all'output.
      ⚠️ **S-5 non nasce da un manuale di sicurezza, nasce da qui**: i cinque tool
      che scrivono contenuto (quattro dei quali fanno commit) sono **elencati ma
      non partono** senza `--allow-write`. ADR-0007 vuole il canone su un branch
      di gruppo con l'occhio del DM sopra; un agente che li lanciasse perché
      «sembrava il passo successivo» non violerebbe una regola di sicurezza,
      violerebbe **il flusso di lavoro del DM**, che è peggio, perché lì per lì
      non se ne accorge nessuno. Elencati e non nascosti di proposito: un tool
      invisibile diventa una richiesta fatta a mano.
      📋 **Un'uscita ≠ 0 è un risultato, non un guasto**: `validate_lingua` esce
      1 per progetto, e porta con sé **il significato del codice preso dal
      manifest**. È la differenza fra un agente che ritenta a caso e uno che
      cambia parametri.
      **Accettazione**: 24 test (guidano il server *attraverso stdio*, non
      chiamandone le funzioni) + un gate CI che lo fa **parlare davvero**,
      `initialize`, `tools/list` con le annotazioni, e `state_apply` che deve
      essere **rifiutato** in sola lettura.
- [x] ✅ **G2, ESEGUITO** (2026-09-02) · [ADR-0032](adr/ADR-0032-misurare-la-leggibilita.md)
      `scripts/validate_tipografia.py`: tre misure sulla **leggibilità**, che
      nessun exit code vede. Non bloccante alla prima passata.
      1. **Gerarchia dei titoli**: un `h4` sotto un `h2` salta l'`h3`, e nei
         segnalibri del PDF (la ragione per cui ADR-0020 esiste) diventa un ramo
         che non c'è. ⚠️ **Il perimetro è la decisione**: la prima passata dava
         **142** salti su tutto il markdown, inclusi i `#####` dei `.hb.md`, che
         in Homebrewery sono **etichette, non titoli**. Punirli sarebbe stato
         punire una convenzione, il difetto in cui questo repo è già inciampato
         due volte. Ristretto ai **capitoli dichiarati da un manifest**: da 142 a
         **4**. Tre sono handout-oggetto (`PROP-*`) dove il `######` imita il
         documento vero: **segnalati e non esentati**, perché è una chiamata del
         DM e un'esenzione silenziosa è come un gate smette di trovare i difetti.
      2. **Caratteri per riga**, non stimati, **calcolati**: larghezza di colonna
         dal tema e **avanzate reali dei glifi** lette con `struct` da `head`,
         `cmap` e `hmtx` del font che incorporiamo, su un campione di prosa
         italiana del repo (non un pangramma: le frequenze contano).
         **Esito: 62,1**, dentro la finestra 45-75. Il tema era giusto; adesso è
         *misurato*, e un font cambiato lo sposta sotto gli occhi di qualcuno
         invece che in copisteria.
      3. **Daltonismo**: le tre dicromazie simulate (Viénot/Brettel via LMS), e
         le coppie **distinte in visione normale** che sotto una dicromia
         collassano. Raggruppate per coppia e non per file: le tavole condividono
         la palette. **Esito: 21 coppie**, e una che si ripete: l'alizarina
         `#c0392b`, il rosso dei marcatori di pericolo, collassa sui **bruni del
         terreno** in protanopia (Δ62 → Δ18) su cinque tavole da battaglia, dove i
         marcatori rossi sono la cosa più densa d'informazione che ci sia.
      🔎 **veraPDF: procurato, fatto funzionare davvero, e lasciato fuori dalla CI**
      con il referto scritto nell'ADR invece che una rinuncia a scatola chiusa.
      Maven Central, `greenfield-apps` 1.28.2 più una classe Java di avvio (il fat
      jar **non registra il proprio provider** e la CLI muore da sola). Sul volume
      dell'Abbazia PDF/UA-1 **FAIL**, tre rilievi: *«heading level 3 is skipped»*
      ×3, **gli stessi tre** che il controllo §1 trova nel markdown, due misure
      indipendenti allo stesso numero, più due che sono **di Typst** (manca lo
      schema XMP di identificazione PDF/UA, mancano le `ViewerPreferences`).
      Fuori dalla CI perché l'unico rilievo azionabile lo troviamo **prima e
      meglio**, nel master dove si corregge; gli altri due resterebbero rossi per
      sempre; e il costo non è quello di un binario statico: JVM, 9,5 MB di jar e
      una classe scritta da noi, che è la ragione per cui ADR-0020 e ADR-0027
      avevano detto sì a `typst` e `pdfcpu`. La ricetta per rifarlo sta nell'ADR.
- [x] ✅ **G3, ESEGUITO** (2026-09-02) · [ADR-0031](adr/ADR-0031-dm-volume-ordine-dei-mestieri.md)
      `dm.py volume MANIFEST.json` esegue la catena in ordine, **dichiarato**:
      `prosa → lingua → manifest → colophon → schermo → stampa → imposizione`.
      `--stampa` è il `dm.py stampa` mai fatto, **assorbito** invece che aggiunto;
      `--imposto` il libretto da piegare; `--solo`/`--salta` per rifare un passo.
      Nasce da §C della ricerca sul colophon: non mancava un mestiere, **mancava
      l'ordine in cui si chiamano**, e chi ne saltava uno se ne accorgeva in
      copisteria.
      I passi non hanno lo stesso peso, e la differenza è la decisione: `prosa` e
      `lingua` **misurano e non bloccano**; `manifest` e `schermo` sono **guasti
      duri che fermano la catena**: compilare da un manifest non valido produce
      un artefatto sbagliato *con l'aria di essere andato bene*; `stampa` e
      `imposizione` **degradano pulito** (ADR-0027).
      ⭐ E in coda, **comunque sia andata**, il cancello d'uscita §7 detto a voce.
      Non è automatizzabile e non si finge che lo sia, ma è il momento in cui un
      volume sta per uscire, ed è il buco che il lotto E aveva misurato: `grep -rl
      "GUIDA-CONDIVISIONE-IP" skills/` dava **un solo file**, e per un'altra
      ragione.
      **Accettazione**: provato sull'Abbazia dall'inizio alla fine: sette passi,
      HTML 615 KB, PDF 34 pagine, **libretto imposto**, e 10 test, fra cui
      «un manifest inesistente esce 2 e non compila niente» e «il cancello IP
      viene sempre detto».
- [x] ✅ **G4, già chiuso in C8** (2026-09-02). Era la stessa cosa di P16, che il
      DM aveva confermato nella stessa domanda: `mapmaking` §«tavole di supporto»
      ha veduta, profilo laterale con quote e **tempi di percorrenza**, con la
      regola che si aggiungono **quando rispondono a una domanda che la griglia
      non può**, non per completezza, e la convenzione di numerazione
      (`Tavola I` zenitale · `I-a` veduta · `I-b` profilo). Resta segnato qui
      perché il piano lo elencava due volte.

**Engine**: Sonnet (G1-G3), Opus (G4: è una convenzione) · **impegno** medio-alto.

### 🟢 Lotto H — Le code preesistenti — *H2, H3, H4 chiusi · H1 misurato bene e ridotto · 2026-09-02*

- [x] 🟢 **H1, il debito non era dove sembrava** (2026-09-02) · [ADR-0033](adr/ADR-0033-derivare-e-dichiararlo.md)
      Il piano diceva «non è una decisione, è fatica». Eseguendo la decisione del
      DM, *«usa le tabelle SRD, e il contenuto libero Pathfinder dove il SRD non
      ha un equivalente»*: il debito si è rivelato **tre cose diverse**.
      1. ⭐ **Cinque schede non sono creature**, e non lo saranno mai: un organo
         collegiale di sette seggi, una popolazione di ~1.500 profughi (che
         dichiara già di non portare statistiche, **per ragioni di IP**), un
         aggregato di combattimento di massa il cui «GS 15» è un **EL**, e due
         dossier che puntano agli statblocchi che vivono altrove. Forzarci sopra
         un blocco vorrebbe dire **inventare un mostro che non esiste**. Marcate
         `[NON-CREATURA]` **con la ragione scritta nel file**: non un'esenzione
         silenziosa. Prima risultavano «da migrare» per sempre, debito che
         nessuno poteva estinguere.
      2. ⭐ **Dieci schede i numeri li avevano già**, in dialetti che il lettore
         non sapeva leggere: la tilde d'approssimazione (`hp ~30`), l'italiano
         esteso (`**Punti Ferita:** 60`, `**Classe Armatura:** 19`, `**Tiri
         Salvezza:** Tempra +7…`), il GS fra parentesi (`**Grado di Sfida
         (GS):** 9`), la forma a barre (`TS +2/+9/+1`), la parentesi con testo
         dentro (`(104 HP with skeleton template)`). Sono **numeri del DM**, e
         derivarli da capo li avrebbe sostituiti con numeri calcolati: per
         `skeletal-dire-lion` la derivazione dava **136 pf**, la scheda ne
         diceva **104**. E quando il numero era una stima, il blocco lo dice:
         trascrivere `hp ~30` come `pf: 30` promuove un'approssimazione a fatto.
      3. **La derivazione vera: fatta, provata, e non abilitata a scrivere.**
         `derive_statblocks.py` implementa le tabelle SRD (tipi, TS per classe,
         matrici elite/standard, taglie, armature) e usa la Tabella 1–1 di PF1e
         **come guardia, non come fonte**: il SRD 3.5 non ha una tabella
         «statistiche per GS», e i valori PF1e sono più duri a parità di GS.
         ⚠️ **Il collaudo respinge tutte e 60**: CA 11 per un GS 9, pf 22 per un
         GS 14. Il motivo è strutturale: le schede sono **prosa, non dati**, e
         una regex ci trova sempre qualcosa di plausibile («Esperto 2» dove la
         riga diceva «Esperto 2 / Acolita 6»). Un numero sbagliato con l'aria di
         un conto entra nel canone e ci resta fino al tavolo. Perciò lo strumento
         **propone**. ⚠️ La prima versione **sopprimeva** invece di annotare, e
         produceva **zero** proposte, cioè non correggeva niente. Rilievo del
         DM, e giusto. Corretto: la guardia **annota** (una proposta con scritto
         sopra *«FUORI BERSAGLIO»* si giudica; una soppressa non esiste), e si
         scrive **un campo solo, i TS,** e solo dove GS, CA e pf li ha scritti
         il DM. I tiri salvezza sono la cosa più meccanica del sistema: la base
         è **esatta** dalle tabelle SRD, e l'unica incertezza è il modificatore
         di caratteristica, che viene dalla matrice dichiarata. **CA e pf non si
         scrivono mai**: dipendono da equipaggiamento e Costituzione, che da una
         scheda in prosa non si leggono.
      **Esito misurato: 100 schede su 157 col blocco** (erano 82): 10 per sola
      lettura dei dialetti, 8 derivando i TS, **e il debito da 75 a 52**, di cui
      nessuno più falso. Le 52 restano aperte e si chiudono a mano: è la sessione
      a sé che il piano prevedeva, ma ora su un numero vero.
      🔎 Due difetti trovati nel farlo: la **stessa classe letta due volte con
      livelli diversi** (*«Chierico 10 / Prestige …»* e più avanti *«Chierico
      13»*) dava Tempra +17 per un GS 13; ora si rifiuta invece di sommare; e
      `argparse` accettava `--apply` come abbreviazione di `--apply-ts`, quindi
      chi scrivesse il primo aspettandosi la scrittura larga otteneva comunque
      una scrittura.
- [x] ✅ **H2, ESEGUITO** (2026-09-02). Il tema aveva un commento che diceva
      *«se un giorno si vuole l'annegato, si apre un ADR sul vendoring dei
      pacchetti Typst»*: quell'ADR è [ADR-0026](adr/ADR-0026-vendoring-pacchetti-typst.md)
      e il ripiego è scaduto.
      **Capolettera annegato** con `droplet`: la maiuscola scende tre righe dentro
      il paragrafo e il testo le scorre attorno. Il versale resta come
      `capolettera-versale`, **e non per nostalgia**: l'annegato ha bisogno di
      almeno tre righe sotto di sé, e il ripiego va scritto invece che implicito.
      **Indice analitico** con `in-dexter`, chiave `indice_analitico` del manifest.
      ⭐ Le voci **non si annotano a mano**: le marca l'esportatore prendendo i
      nomi canonici dal glossario, alla prima occorrenza per volume; chiedere a
      chi scrive di marcare ogni ricorrenza è il modo in cui un indice analitico
      resta vuoto per sempre. Verificato sul booklet della sessione Terros: **13
      voci**, raggruppate per lettera, con le pagine (*Portale della Forgia
      Eterna 3, 14*). E se in un volume non compare **nessun** nome del glossario
      Il caso dei moduli autoconclusivi, che hanno un'ambientazione loro, la
      pagina **non si aggiunge**: un «INDICE ANALITICO» vuoto è peggio di niente.
      Le pagine sono state **guardate**, non solo compilate.
- [x] ✅ **H3, già chiuso in G3** (verificato 2026-09-02): `dm.py volume --imposto`
      impone il libretto con `pdfcpu` ([ADR-0031](adr/ADR-0031-dm-volume-ordine-dei-mestieri.md),
      funzione `_imponi`), e degrada pulito se il binario manca. Riprovato
      sull'Abbazia: il libretto esce. Non è stato rifatto: è stato verificato.
- [x] ✅ **H4, rinuncia confermata**, e resta tale: ADR-0020 la dichiara, e si
      riapre solo il giorno di una tiratura vera. Non toccata di proposito.

---

## §3 · L'ordine consigliato

```
  A ──► B ──► D ──► G2  (nessuna decisione: si può partire oggi)
        │
  C ────┤     (parallelo ad A/B: tocca skill, non codice)
        │
  E ────┘     (dopo B, perché il colophon è il suo primo oggetto)

  F ──► H2, H3, G3   (tutto ciò che aspetta il DM)
```

**Se si fa un lotto solo**: **A**. Non perché sia il più prezioso (lo è B) ma
perché è l'unico dove oggi il repo è *cieco*: 2.750 righe senza nessun controllo
sono il posto dove il prossimo difetto arriverà al tavolo invece che alla CI.

---

## §4 · Cosa questo piano NON fa

Scritto qui perché non si riapra a ogni lotto.

1. **Non riapre le rinunce già decise**: niente edizione inglese (ADR-0016),
   niente CMYK/PDF-X (ADR-0020), niente skill di traduzione o di vendite
   (ADR-0005). Restano no.
2. **Non converte l'Abbazia di nascosto.** Il Lotto A le dà un gate; la
   conversione è F4, ed è una domanda.
3. **Non aggiunge skill per simmetria.** Una sola nuova (`rumblingstone-edizione`,
   Lotto E), e con l'ADR-0008 davanti. Tutto il resto sono estensioni.
4. **Non tocca il contenuto giocato.** Nessun lotto qui riscrive una scena, un
   read-aloud o un canone: è tutto apparato, gate e supporto.
