# PIANO — «Il Drappo di Tarsilia»: il Palio come modulo autonomo (Golarion · PF1e)

**Stato**: 🟡 in corso — Lotti 1, 2 e 5 chiusi (impianto · profondità AP · apparato d'uso e governance)
**Aperto**: 2026-08-14
**Richiesta-fonte (DM, 2026-08-14)**: *«dato il palio di Channathgate possiamo fare
una variante per sessioni di qualche ora, per 6 persone, per 3 giorni, ambientata a
Golarion per Pathfinder 1e non remastered, con 6 PG massimo con schede pregenerate e
immagini, sulla falsa riga delle avventure Paizo "We Be Goblins"? Si può gestire come
sessioni a sé stanti e svincolate dai Forgotten Realms?»*

**Risposta breve**: sì, e non è un ripiego — è la strada che
[ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) aveva già indicato
(«riambientare fuori da Forgotten Realms») e che
[ADR-0016](adr/ADR-0016-lingua-sorgente-e-edizioni.md) §2 aveva messo in coda come
*«l'unico materiale realmente pubblicabile: il sistema del Palio riambientato fuori
da Faerûn»*. La serie di stemmi Golarion (PR #100–#102) era già il primo pezzo.

---

## 1. Cosa si costruisce, e cosa NON si tocca

| | |
|---|---|
| **Si costruisce** | un modulo **autonomo**: città originale, sei PG pregenerati, tre giorni di gioco, regole PF1e, allegati propri |
| **Si riusa** | il **sistema** del Palio (Sorte, Partiti, Morale/Onore, Stacco, Corsa) — materiale originale dell'autore — e gli **otto stemmi Golarion** già in repo |
| **NON si tocca** | l'arco P2D di Channathgate: resta com'è, in 3.5, dentro la campagna. Nessun file dell'arco 09 viene modificato |
| **NON si eredita** | Faerûn, il Red Hand of Doom, i quattro PG della campagna, il Collezionista, Rethmar, la Cronaca Vivente |

Il vincolo di partenza è quello che rende il lavoro sensato: **due copie non
divergono se una non dipende dall'altra**. Il modulo standalone cita l'arco P2D
nel piano e nelle note di provenienza, e nient'altro.

## 2. Le decisioni prese (e perché)

| Decisione | Scelta | Motivo |
|---|---|---|
| **Ambientazione** | **Tarsilia**, città-stato originale nel **Regno dei Fiumi**, sul Sellen | il Regno dei Fiumi è canone Paizo *fatto apposta* per ospitare staterelli inventati (le Sei Libertà). Città originale = zero canone Paizo da rispettare, aggancio geografico plausibile |
| **Sistema** | **PF1e (non remastered)**, Core Rulebook | è la richiesta; il Core basta e riduce il rischio di regole rese male |
| **Livello / party** | **6 PG di 3°**, 20 punti acquisto | sei uffici della contrada = sei schede; il 3° dà risorse per intrigo *e* combattimento |
| **Durata** | **3 sessioni da 3–4 ore**, una per giornata di corsa | la richiesta; la struttura del Palio è già a giornate |
| **Avanzamento** | **pietre miliari** (4° a fine Giorno 2) | con la traccia media servirebbero ~24.000 px totali: un modulo d'intrigo non li produce e non deve provarci |
| **Nome dell'evento** | «il **Drappo**», non «il Palio di X» | bonifica §7.6 del rapporto IP: *palio* resta nome comune, l'identità senese no |
| **Contrade** | otto, **nomi senesi** (decisione DM 2026-08-15: *«poi bonificheremo anche quelli»*), motti **scritti ex novo**, nessun titolo araldico reale | §7.2 e §7.4 chiuse, **§7.1 sospesa** → Lotto 4 |
| **Immagini** | 8 stemmi SVG (riuso) · 2 mappe tattiche dalla pipeline · **mappa città, il Drappo e 6 ritratti** da `build_tavole.py` · prompt-sheet per l'edizione raster | il repo non genera raster: genera **vettoriale** e *istruzioni* per ComfyUI locale |

## 3. Lotti

> 🔎 **Il CHANGELOG numera da solo, e qui non si rinumera** *(verificato il
> 2026-10-10 su tutta la storia, 248 rami e le PR #105-#108, #115 e #215:
> nessuna sezione è mai stata tolta)*. Tre righe del CHANGELOG portano numeri
> che in questo piano non hanno una sezione:
> - **«Lotto 7»** (`0d2e050c`, PR #105, 2026-08-15: lo spoiler chiuso, il kit
>   anti-improvvisazione, i prompt, la mappa giocatore) sono i lavori [1a], [3]
>   e [6] della lista del Lotto 6, dove compaiono come rimandi *(Lotto 7)*.
> - **I due «Lotto 8»** sono nati su due rami paralleli dallo stesso commit: le
>   venti immagini (`d4183120`, PR #108, ramo `xbyvzt`) e le sei schede vere
>   (`85800574`, PR #107), che sono il Lotto 8 qui sotto. La collisione è
>   raccontata in «Divergenza con xbyvzt».
> - **«Lotto 9 — il dossier delle piste»** (`99cd8757`, PR #115, 2026-08-31,
>   `10-DOSSIER-DELLE-PISTE.md`) non è mai entrato qui; il Lotto 9 di questo piano
>   è «La tavola di fuori» (PR #215). Il dossier è chiuso: ✅ 2026-08-31.
>
> Il CHANGELOG è un registro storico e resta com'è. Il prossimo lotto nuovo
> prende il **10**.

### Lotto 1 — Impianto giocabile ✅ *(chiuso 2026-08-14)*

- [x] `STANDALONE-Il-Drappo-di-Tarsilia/00-HUB-E-QUICKSTART-DM.md`: hub, quickstart,
      contratto del tavolo, cosa stampare, ponte fra le tre sessioni
- [x] `CONTRADE-DI-TARSILIA.md`: le otto contrade: livree, motti nuovi, canti con
      effetti, rivalità, tabella di corrispondenza con gli stemmi SVG
- [x] `REGOLE-DELLA-CORSA-PF1E.md`: il sottosistema: Morale del Rione, Onore del
      Fantino, lo Stacco, la Corsa a nove tratti, lo scudiscio, il cavallo scosso
- [x] `PREGEN-SEI-SCHEDE-PF1E.md`: sei schede complete (statblock, equipaggiamento,
      ufficio, obiettivo personale, come si gioca in un minuto)
- [x] `01-GIORNO-1-LA-SORTE.md` · `02-GIORNO-2-I-PARTITI-E-LA-CENA.md` ·
      `03-GIORNO-3-LO-STACCO-E-LA-CORSA.md` — le tre sessioni
- [x] `STATBLOCCHI-PF1E.md`: PNG, rivali, sicari, cavalli
- [x] `ALLEGATI/mappe/`: 2 mappe dal contratto JSON (piazza, stalle) + render
- [x] `ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`: art direction
- [x] `IP-E-LICENZE.md`: CUP Paizo, OGL, quali bonifiche §7 questa edizione chiude
- [x] tracciatura: questo piano + INDEX + CHANGELOG

**Criterio di accettazione**: un DM che non ha mai letto la campagna RumblingStone
apre l'hub, stampa sei schede e gioca tre serate senza aprire nient'altro.

### Lotto 2 — Profondità da modulo AP ✅ *(chiuso 2026-08-15)*

Nato dall'audit del DM: *«ci sono eventi per i personaggi? come entrano nelle
contrade? ci sono osterie e botteghe? un master ha tutto sotto controllo o ha bisogno
di un'AI? c'è stata una sessione alfa di playtest?»* — sei «no» onesti, e questo lotto
li chiude.

- [x] **Nomi senesi ripristinati** su decisione DM (Oca, Torre, Bruco, Istrice, Drago,
      Civetta, Leocorno, Onda) con gli scudi Golarion; nota IP riscritta **onesta**:
      6 bonifiche su 8 chiuse, 1 sospesa, 1 chiusa altrove
- [x] `04-LUOGHI-E-INTRIGO.md`: quindici luoghi giocabili, il mercato delle
      informazioni della Civetta, le dicerie (1d6), tre luoghi che non servono a niente
- [x] `05-INIZIAZIONE-E-EVENTI-PG.md`: come si entra in una contrada, **il rito
      d'Investitura** come scena d'apertura, **diciotto eventi personali** (3 per PG)
      con griglia di controllo
- [x] `06-VILLAIN-E-AGENDE.md`: agende **ora per ora** di Vesca, Sfregio, Salle e
      Attu; il giro del mondo se i PG stanno fermi; le contromosse; **incontri
      scalabili 4/5/6/7 giocatori** e la variante di 5° livello
- [x] `07-GUIDA-DM-PASSO-PASSO.md`: la regia: 45 minuti di preparazione, le tre
      serate minuto per minuto, otto rilanci, le voci dei PNG, l'elenco di cosa non fare
- [x] `FASCICOLO-SCHEDE-GIOCATORE.md`: sei background in prima persona + **matrice
      dei legami 6×6**
- [x] `ALLEGATI/tavole/build_tavole.py`: mappa della città, il Drappo, sei ritratti,
      tutti vettoriali e rigenerabili
- [x] `PLAYTEST-ALFA.md`: audit meccanico (18 rilievi) + dry-run cronometrato delle
      tre serate + **nove correzioni applicate al modulo**
- [x] `homebrew/`: **tre booklet** (DM, Giocatori, Fascicolo) in HTML pergamena +
      sorgente Homebrewery + **22 PDF A4** esportati

**Criterio di accettazione**: un DM che non ha mai letto il modulo apre
`07-GUIDA-DM-PASSO-PASSO.md`, spende quarantacinque minuti, e gioca tre serate senza
inventare niente di strutturale.

### Lotto 5 — Apparato d'uso, collaudo e governance ✅ *(chiuso 2026-08-15)*

Nato dalla domanda del DM *«cosa manca davvero perché sia memorabile per i giocatori e
bello da masterizzare?»* e dalla ricerca che ne è uscita
([`RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE`](RICERCA-COSA-SERVE-A-UN-MODULO-PUBBLICABILE.md)).
La risposta: non mancava contenuto, mancava **l'apparato d'uso**.

- [x] `08-CASSETTA-DEL-DM.md`: foglio del cast (28 PNG con il tic vocale), guida
      alla **pronuncia**, indice dei **15 read-aloud**, inserto per lo schermo, i
      **suoni**, il **momento da fotografare**, accessibilità
- [x] `ALLEGATI/handout/`: **quattro prop stampabili**: il contratto di Vesca (piegato
      in tre, che i giocatori possono non aprire mai), la pagina del registro dei morti
      con i nove nomi, la ricevuta `C·S·M`, il decreto affisso
- [x] `STATO-DEL-MODULO.md`: la memoria fra le tre serate: contatori, patti scritti,
      sette scelte che cambiano il finale, **Echo Ledger**, conteggio dello spotlight
- [x] `PLAYTEST-SCHEDA-FEEDBACK.md`: scheda giocatore (le domande che misurano
      davvero), debrief del DM con **due metriche numeriche**, ciclo alfa→beta→collaudato
- [x] **skill nuova** `rumblingstone-playtest` — le tre passate, come si legge il
      feedback, come si scrive una correzione. **Vale anche per la campagna**
- [x] **script nuovo** `scripts/validate_standalone.py` — gate CI per i moduli
      `STANDALONE-*`: file obbligatori, riferimenti incrociati, schede, termini 5e,
      read-aloud minimi, contatori. Registrato nel manifest, in CI
- [x] `rumblingstone-module-standard` §15-16 — l'apparato d'uso e i prop entrano
      nella checklist
- [x] **[ADR-0017](adr/ADR-0017-moduli-autoconclusivi-classe-di-artefatto.md)**: i
      moduli autoconclusivi sono una classe a sé: cosa non possono fare, cosa devono avere
- [x] **[ADR-0018](adr/ADR-0018-apparato-uso-obbligatorio.md)**: l'apparato d'uso è
      parte del contenuto, non un extra. Vale per il modulo **e** per la campagna
- [x] `ALLEGATI/mappe/uvtt/`: le due mappe esportate per Foundry/Roll20

**Criterio di accettazione**: il debrief del DM misura **zero improvvisazioni
strutturali** e **meno di cinque ricerche sopra i trenta secondi** a serata. Si verifica
al Lotto 3, non prima.

### Lotto 3 — Collaudo al tavolo ⬜ *(gated: serve una sessione vera)*

⚠️ *(2026-09-27, ADR-0075)* Prima del tavolo il Drappo passa i passi 1-2 e 4-7
del ciclo del master (lotto S3 di PIANO-MASTER-DEF e F5 di PIANO-LETTORE): la
lettura a freddo e il quiz trovano quello che il DM dovrebbe inventare, il
tavolo trova il resto. Il passo 3 (componenti) vale se il contratto è attivo.

- [ ] Giocare il Giorno 1 e annotare durata reale, punti morti, prove mai usate
- [ ] Rispondere alle sei domande aperte di `PLAYTEST-ALFA.md` §5
- [ ] Ritratti raster: il DM passa i prompt a ComfyUI locale
- [ ] Aggiungere il §6 al playtest → il modulo passa da **alfa** a **beta**

### Lotto 4 — Edizione pubblicabile ⬜ *(gated: decisione DM su ADR-0005)*

- [ ] Rinominare le contrade (bonifica §7.1, oggi **sospesa per scelta del DM**)
- [ ] Sostituire almeno quattro figure su otto negli stemmi
- [ ] Rigenerare i cartigli degli scudi coi motti nuovi
- [ ] Audit IP dedicato del solo standalone

### Lotto 6 — Edizione illustrata ⬜ *(pronto a partire: il capitolato è scritto)*

Il modulo è completo come **testo** e come **impaginazione**; non è ancora un **libro
illustrato**. Il divario è misurato e il capitolato d'appalto sta in
`STANDALONE-Il-Drappo-di-Tarsilia/PROMPT-GENERAZIONE-BOOKLET-DEFINITIVO.md`, che
contiene anche il prompt autosufficiente da passare a una sessione nuova.

- [x] Inventario di cosa esiste, e i sei divari verso il livello Paizo/WotC (§1-§2)
- [x] Prompt d'appalto con vincoli IP, strumenti del repo, criteri di accettazione (§3)
- [x] **[1a]** I **venti prompt** scritti e verificati contro la bibbia visiva, con
      look comune, ancora storica fiamminga e patto d'inquadratura *(Lotto 7)*
- [x] **[1b]** La **catena di generazione**: `scripts/comfyui_batch.py` legge i prompt
      annotati dal markdown, compone le leve, fissa i seed, POSTa i workflow e scrive
      `PROVENIENZA.txt`. Manifest + 25 test + smoke in CI (ADR-0012), pesi non
      commerciali **rifiutati** (ADR-0019), procedura in `ALLEGATI/immagini/README.md`
- [ ] **[1c]** I **diciotto raster** — ⚠️ *gated: serve la GPU del DM*. La catena è
      pronta e collaudata a secco; l'esecuzione è ~1,5-2 ore di macchina più il gate
      di rifiuto **il giorno dopo**
- [x] **[1-bis]** Blender come **geometria**, non come illustratore:
      `scripts/render_map_blender.py` risolve la pianta con lo **stesso** `paint()`
      dell'SVG, fonde le celle in solidi e la fa rendere in ortografica;
      `--profondita` produce il passo per ControlNet depth. Manifest + 27 test +
      controllo di determinismo in CI. ⚠️ Il **render** non è mai stato eseguito:
      Blender non c'è in questo ambiente — provato tutto ciò che sta prima di `bpy`
- [x] **[2]** Tipografia OFL embedded — chiusa da **ADR-0020** sul secondo binario
      Typst (EB Garamond + Cinzel), senza toccare `build_booklet_html.py`
- [x] **[3]** `tarsilia-la-ruota-giocatori.json`: la mappa senza token, hazard e note *(Lotto 7)*
- [x] **[4]** PDF unico con segnalibri — `export_booklet_typst.py`, volume da 63 pagine
- [ ] **[5]** Carte da tavolo: otto segnaposto contrada + ordine di corsa, estendendo
      `ALLEGATI/tavole/build_tavole.py`
- [ ] **[6]** Frontespizio vero — il **prompt** della copertina c'è *(Lotto 7)*, manca il raster

**Criterio di accettazione**: i quattro booklet si rigenerano da zero, ogni immagine
ha la sua riga in `PROVENIENZA.txt`, e nessun file della campagna risulta modificato.

### Lotto 8 — Le sei schede come schede vere ✅ *(chiuso 2026-08-16)*

Il modulo aveva le sei pregenerate come **testo**: due master markdown impaginati a
colonne, che è la forma giusta per un manuale e quella sbagliata per un foglio che
sta in mano tre serate. Questo lotto le trasforma in **schede** — una pagina A4 a
testa, sul modello delle pregen dei moduli brevi PF1e.

- [x] `scripts/typst/scheda-pg.typ`: la pagina a due pannelli — fascia alta con
      ritratto e i tre valori sempre consultati, sinistra «chi sei», destra lo
      statblocco, piede «come si gioca in un minuto»
- [x] `scripts/dmcore/schede.py`: legge i **master esistenti** (`PREGEN-*.md` +
      `FASCICOLO-*.md`) e li restituisce strutturati — nessuna seconda copia dei
      numeri, quindi nessuna copia che possa restare vecchia
- [x] `export_booklet_typst.py`: capitolo `"layout": "schede"` e chiave di manifest
      `front_matter: false` (sei fogli, senza copertina né indice da saltare)
- [x] `ALLEGATI/immagini/web/`: le derivate leggere dei sei ritratti — il PDF passa
      da ~40 MB a 0,9 MB
- [x] `homebrew/DRAPPO-SCHEDE-PG.manifest.json` + `scripts/tests/test_schede.py`
      (16 test: regole di taglio su master sintetici, le sei schede vere, `inline`)

**Criterio di accettazione**: `DRAPPO-SCHEDE-PG-STAMPA.pdf` esce di **esattamente sei
pagine**, ogni scheda ha il suo ritratto, e cambiare un numero nel master lo cambia in
stampa senza toccare altro.

**Chiusura del lotto (2026-08-17)** — audit richiesto dal DM, con la flag che ne è uscita:

- [x] `--per-scheda`: un PDF per giocatore, compilato da un **sorgente suo** e non
      ritagliato per numero di pagina (il ritaglio regge finché ogni scheda sta in una
      pagina sola). Serve perché il fascicolo unico brucerebbe i sei segreti insieme
- [x] **Sette smoke CI mancanti**: `build_booklet_html`, `export_booklet_pdf`,
      `export_booklet_typst`, `build_chapter_marks`, `extract_scene_prompts`,
      `import_watabou`, `campaign_branch` dichiaravano `ci_smoke` nel manifest e non
      venivano eseguiti da nessuno — il contratto ADR-0012 prometteva una verifica
      inesistente. Più uno step nuovo che risolve il manifest delle schede senza typst
- [x] **Test anti-drift** fra i parametri emessi dall'esportatore e la firma di
      `#let scheda(...)`: senza typst in CI, un rinomino nel template romperebbe ogni
      build in silenzio
- [x] `scripts/README-automation.md`: la tool map non citava l'esportatore da stampa
- [x] **Audit meccanico delle sei schede** (skill `rumblingstone-playtest`, passata 1)
      → `PLAYTEST-ALFA.md` §6: due correzioni applicate (CMD di Ombra, CD di Tesio)
- [x] `validate_standalone.py`: il gate sui link **esisteva già** e prende le immagini
      rotte; gli è stata aggiunta la **ragione** quando il file manca perché è una
      derivata gitignorata — la trappola in cui sono cadute due sessioni di fila

### Lotto 9 — La tavola di fuori 🟡 *(aperto 2026-10-03: scena scritta, collaudo a freddo gated)*

[engine: Opus, sessione principale · effort: alto · qualità: i gate del modulo verdi, box al metro, e la scena che regge a una lettura a freddo e a un dry-run cronometrato]

**Origine.** Il DM ha chiesto se nei master convenisse innestare qualcosa di
*Alice nel Paese delle Meraviglie*. La valutazione ha proposto tre posti; il DM ha
approvato quello del Drappo (2026-10-03). La scelta di metodo è [ADR-0080](adr/ADR-0080-le-fonti-di-pubblico-dominio-entrano-come-logica.md).

**Cosa ho guardato prima (ADR-0044).** `PIANO-DRAPPO` è 🟡 in corso e il lavoro sta
dentro il suo perimetro, quindi è un lotto suo e non un piano nuovo.
`PIANO-INNESTI-SFIDE` riguarda incontri nel canone giocato, non il Drappo.
`PIANO-LETTORE-E-PLAYTESTER` F5 dà il contratto di lettura sugli stand-alone e resta
il gate del passo 6.

**Cosa NON rifà.** Non tocca i cinque DEF di ARC-07 né i master di ARC-08/09. Non
aggiunge contatori (il modulo ne ha due, e il gate li controlla). Non aggiunge piste né
falsi indizi. Non cambia le regole dei Partiti (`REGOLE-DELLA-CORSA-PF1E.md` §4).

**Dove ho corretto la proposta approvata**, perché leggendo il modulo ho trovato tre
cose che la proposta non sapeva:

| Proposta del 2026-10-03 | Cosa ho trovato | Cosa ho fatto |
|---|---|---|
| Il tè dei matti alla **Cena della vigilia** | La Cena è del rione, ottanta persone dell'Istrice. Il tavolo dove nessuno si siede perché sedersi è prendere posizione è il **mercato del grano** (§2 dei Partiti), e il playtest alfa ha misurato 72 minuti di cinque giocatori fuori scena | La scena è al §2-bis, sotto il portico del mercato, per i cinque che aspettano. La Cena resta com'è |
| Un **indovinello senza risposta** innestato sui quattro quaranta | `10-DOSSIER` §7: un solo falso indizio per modulo, ed è già quello. Un secondo insegna al tavolo che i fatti non contano | Tolto. Il Maestro sbaglia i numeri degli articoli, e il pilastro li corregge: è un Fatto, non si tira. I numeri evitano i quaranta |
| Il **pittore e le rose dipinte** sulla pista C | La pista C è la pista morale, «senza premio meccanico», e il registro di Rasca nasconde nove morti: una gag la guasterebbe | Tolto. Il Drappo non cambia di una riga |

**Cosa è stato scritto** (2026-10-03):

- [x] `02-GIORNO-2` §2-bis, *La tavola di fuori*: box di apertura di 11 righe, il
      regolamento sul pilastro (tre articoli coi numeri veri), il Maestro di Tavola
      (il funzionario di `09-KIT` §3, già previsto alla Cena), il Dormiente (tre
      dicerie della tabella di `04-LUOGHI` §5, nessuna nuova), la porta con il
      foglietto di dodici parole letto a tutti, l'eco alla Cena
- [x] Innesti: indice e puntatore in `02-GIORNO-2` §2, la fascia di `07-GUIDA` §4, la
      riga «non è un mistero» in `10-DOSSIER` §10, il «dove si incontra» in `09-KIT` §3,
      la nota di pubblico dominio in `IP-E-LICENZE` §5-bis, la domanda 0 in `PLAYTEST-ALFA` §5
- [x] Misura: `validate_standalone` verde; `validate_prosa` nessun tic oltre soglia;
      `ciclo_prosa segnala` stesso numero di segnalazioni di prima (2 e 2, entrambe già
      nel file, nessuna nella scena nuova)
- [ ] **Passo 6 del ciclo (ADR-0075): lettore e playtester a freddo** sul §2-bis. ⬜ non
      fatto: servono due agenti che non vedono questo piano, con la rubrica di
      `PIANO-LETTORE` F5
- [ ] **Dry-run cronometrato**: la tavola sta dentro i cinque minuti di un taglio?
      ⬜ non fatto
- [ ] Regenerare i booklet `homebrew/DRAPPO-BOOKLET-DM` dalla fonte aggiornata, e
      controllare con `validate_booklets`. ⬜ non fatto in questo lotto
- [ ] Tavolo vero (L3 di questo piano). La scena resta **alfa** finché non è giocata

<!-- decisioni-dm: DRAPPO-TAVOLA -->

| # | Fase | Domanda |
|---|---|---|
| ~~D1~~ | L9 | ✅ **Decisa il 2026-10-03** (il DM: *«approvo con tutte le premesse e verifiche che vuoi fare»*): l'innesto nel Drappo parte, con la forma proposta |
| ~~D2~~ | L9 | ✅ **Decisa il 2026-10-03** (il DM: *«D2 ok»*): le tre correzioni restano. Era: **Confermi le tre correzioni?** Dedotto da me: la scena sta ai Partiti e non alla Cena; l'enigma senza risposta è tolto; le rose dipinte sono tolte. Sono scelte mie, e il DM approvando non le aveva viste |
| ~~D3~~ | L9 | ✅ **Decisa il 2026-10-03** (il DM: *«d3 ok»*): il foglietto letto a tutti resta nella scena. Era: **Il foglietto letto a tutti è una regola che vuoi?** Dà ai cinque fuori un modo di pesare sulla trattativa di Vanna, ed è l'unica cosa della scena che tocca i Partiti. Alternativa: tavola senza porta |
| ~~D4~~ | futuro | ✅ **Decisa il 2026-10-03** (il DM: *«d4 non adottarlo»*): le altre due proposte **non si adottano**, e il Drappo resta l'unico innesto. Era: **Le altre due proposte della valutazione** (la Torre Invisibile in ARC-09, liv. 2-3; lo Strappo fra le Ere come appendice opzionale di DEF-5) restano non decise. Vanno decise prima di toccare altri file |

<!-- eco: DRAPPO-TAVOLA 2026-10-03 -->
- **Decise**: D1, l'innesto nel Drappo parte (decisa prima, lo stesso giorno); D2, le tre correzioni alla proposta restano; D3, il foglietto di dodici parole letto a tutti resta; D4, le altre proposte non si adottano
- **Aperte**: nessuna decisione. Restano i passi del lotto non fatti: lettura a freddo, dry-run, booklet, tavolo
- **Cambiate**: nessuna rispetto alla proposta; D4 chiude invece di rimandare
- **Dedotto da me**: che *«non adottarlo»*, al singolare, valga per **tutte e due** le proposte di D4 (la Torre Invisibile e lo Strappo fra le Ere). Se il DM voleva escludere solo una, lo dica e riapro l'altra

### ⚠️ Divergenza con `claude/golarion-pathfinder-campaign-xbyvzt`

Le schede sono state fatte su `claude/golarion-pregen-character-sheets-cstheq` mentre
un'altra sessione lavorava allo **stesso modulo** sul branch nominato nel capitolato.
Nessuno dei due è stato mergiato in `main`. **Decisione del DM (2026-08-17): i due rami
restano separati e li unisce lui.** Qui c'è cosa troverà.

| File | Conflitto | Come si scioglie |
|---|---|---|
| `scripts/export_booklet_typst.py` | `md_to_typ(md)` là è diventata `md_to_typ(md, base)`; `inline()` toccata da entrambi (loro: entità HTML — io: enfasi annidata e `~`) | **tenere entrambe**: sono correzioni disgiunte. Le due firme si conciliano passando `base` e lasciando il corpo di `inline()` nella versione ricorsiva |
| `scripts/typst/tema-rumblingstone.typ` | loro `#figura`, io il parametro `apparato:` | additivi: nessuna scelta da fare |
| derivate delle immagini | loro `scripts/build_image_derivatives.py` (1400 px, q88, regole per famiglia) — io sei JPEG a 1000 px/q82 e una ricetta in un README | **vince il loro tool**: rigenerare le derivate con lui e buttare la mia ricetta |
| `.gitignore` | solo mio | **tenere il mio**: senza l'eccezione `!.../web/*.jpg`, il loro ramo ha **dodici link rotti** (verificato eseguendo `validate_standalone.py` su quel branch) |
| `FASCICOLO-SCHEDE-GIOCATORE.md` | loro l'hanno gia' ripuntato alle derivate | **vince il loro**: chiude il debito che avevo dichiarato aperto |
| `plans/CHANGELOG.md`, `docs/tools/*` | righe/artefatti generati da entrambi | append e rigenerazione (`tools_manifest.py --emit-all`) |

## 4. Engine e impegno per fase (regola DM 2026-07-22)

| Fase | Engine | Impegno | Dieta di contesto |
|---|---|---|---|
| Decisioni di ambientazione, IP, struttura d'arco | Opus | alto | ADR-0005/0016, rapporto IP §3/§7 |
| Redazione sessioni, statblock, tabelle | Sonnet | medio | solo il file del giorno + contrade + regole corsa |
| Mappe JSON, render, validazione | script deterministici | basso | `compile_map_json.py`, `render_map_svg.py` |
| Passata di lingua sui read-aloud | Opus | alto | `italiano-nativo.md`, `read-aloud-adulti.md` |

## 5. Rischi noti

| Rischio | Mitigazione |
|---|---|
| **Deriva fra le due edizioni** (Channathgate 3.5 ↔ Tarsilia PF1e) | non c'è dipendenza: l'unico asset condiviso sono gli stemmi, che restano **generati** dalla loro pipeline e citati per percorso relativo, mai copiati |
| **Regole PF1e rese male** su classi fuori Core | il modulo usa **solo il Core Rulebook**. Ogni deroga è marcata `[INFERRED — needs DM confirmation]` |
| **Sei giocatori, tre ore**: si arriva a metà giornata | ogni sessione ha una **linea di taglio** dichiarata («se sono le 23, salta a…») |
| **Il modulo diventa "il Palio ma peggio"** | i sei uffici della contrada sono i sei PG: qui la dirigenza *è* il party, non un ruolo aggiunto |

## 6. Provenienza

Sistema e impianto derivano da `09_Continuazione Arco Narrativo dopo Battaglia di
Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-*.md` (materiale originale dell'autore).
Le bonifiche applicate sono quelle del §7 di
`...P2D-PALIO-VERIFICA-LEGALE-IP.md`; il dettaglio di quali sono chiuse e quali
restano aperte sta in `STANDALONE-Il-Drappo-di-Tarsilia/IP-E-LICENZE.md`.
