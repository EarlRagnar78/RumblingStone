# 📋 Stato dei piani e ordine di chiusura

> **Cos'è**: la fotografia di dove sono i piani **oggi** e in che **ordine** si
> chiudono per non sovrapporsi. Nasce dalla richiesta DM del 2026-09-04 —
> *«documentazione completa su cosa fatto, cosa apre, cosa introduce di nuovo,
> cosa fixa e cosa rimane da fare nel plan, e quale plan chiudere in ordine per
> non sovrapporre i plan»*.
> **Si aggiorna** a ogni lotto chiuso, come `INDEX.md`. Non sostituisce
> `INDEX.md` (che dice *cosa esiste*) né `CHANGELOG.md` (che dice *cosa è
> successo*): questo dice **in che ordine si va avanti, e perché**.

---

## 1 · Cosa è stato fatto in questa tornata

Sette lotti, dal 2026-09-04. Ognuno con la sua riga nel `CHANGELOG`.

| Lotto | Che cos'era | Esito |
|---|---|---|
| **R1** | Il canone su `main` attribuiva a Tordek un pegno permanente di Thorik, per un mese | ✅ corretto in 12 file, con **E-07c riscritta, E-07e annullata, E-07f nuova** |
| **R2** | `AGENTS.md` elencava **13 skill su 18** e diceva il falso su come si caricano | ✅ [ADR-0041](adr/ADR-0041-instradamento-delle-skill-con-un-gate.md): principio → tabella per compito → inventario, **con un gate bidirezionale** |
| **R5** | Cinque PR aperte senza giudizio | ✅ giudicate una per una **sul codice di oggi**: #109 superata e chiusa, le altre quattro **abbandonate, non superate** |
| **R9** *(2026-09-05)* | Il conto di R5 era **incompleto**: la **#67** non aveva giudizio in nessun documento | ✅ **superata** — su `main` gli stessi hint esistono dal 31 luglio come booklet da manifest, e la PR è **contraria alla norma degli handout**. Da chiudere. Zero issue aperte |
| **R6** | `⬛` valeva insieme *tenda, edificio, dais* su 8.216 celle | ✅ [ADR-0042](adr/ADR-0042-tre-glifi-per-tre-cose.md): tre glifi, e `⬛` **non cambia comportamento** |
| **R7** | La DES di Thorik scritta in modo ambiguo; due clausole della Corona mai decise | ✅ tabella punteggio/modificatore; **+4 CAR e non-rimovibilità confermati** dal DM |
| **F0** | `⛰` disegnato solido e non muro nell'export; `validate_maps` con un punto cieco | ✅ [ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md) |
| **D6** | La griglia di `…P1C` mappa 3: dichiarava 40×40, aveva righe da 24 a 26 celle | ✅ ridisegnata **26×29**, nessuna coordinata del testo cambiata |

### Cosa **fixa**, in una riga ciascuno

- Un PG portava il malus permanente di un altro.
- Un agente poteva pubblicare **senza il gate d'uscita IP**, perché la sua skill non era instradata.
- Su Foundry si **attraversava la catena montuosa** e ci si vedeva attraverso.
- Cancellare tutti gli SVG di un master lo faceva **sparire dalla validazione**.
- Un accampamento drow esportava **2.173 quadretti di muro** dove ci sono tende.
- Una scheda diceva a Tordek di sommare un −2 DES **che non è suo**.
- Quattro mappe di ARC-09 non erano mai state renderizzate.

### Cosa **introduce di nuovo**

| | |
|---|---|
| **4 ADR** | 0041 instradamento · 0042 tre glifi · 0043 muri e controllo · 0044 apertura dei piani |
| **3 gate bloccanti** | skill instradate (bidirezionale) · master senza SVG · renderer/export d'accordo sui solidi |
| **1 glifo** | `🔳` dais |
| **21 test** | in tre file nuovi, di cui **sette provano che i gate mordono** |
| **3 documenti** | il piano di ripresa PR · la ricerca sul mestiere · questo |
| **1 regola di disciplina** | ADR-0044, nella skill dei piani |

### Cosa **apre**

- La **ricerca sul mestiere** (cartografia + illustrazione), col suo audit da eseguire.
- La **coda di riclassificazione** delle 8.216 celle `⬛` — lettura, non sostituzione.
- La **coda delle 6 mappe** con l'intestazione discorde dalla griglia.
- Il **piano di ripresa** delle quattro PR abbandonate, con la Fase 0 già chiusa.

---

## 2 · L'ordine di chiusura, e perché è questo

Il criterio **non** è l'età né la dimensione. È: *si può chiudere senza aprire
un fronte in un altro piano?*

```
  ①  RIPRESA-PR-ABBANDONATE  F1 → F2 → F3 → F4          ← la coda vera
                                       │
                                       └── F3 è il committente della ─┐
                                                                      ▼
  ②  RICERCA-MESTIERE       F1 audit → F2 gate → F3 norme  ← dà i criteri a F3
                                       │
                                       └── eredita le 6 mappe di §6
  ③  VENDIBILITA            bloccata su D1 e sul cancello di qualità
```

| # | Piano | Quando si chiude | Perché non prima |
|---|---|---|---|
| **①** | [PIANO-RIPRESA-PR-ABBANDONATE](PIANO-RIPRESA-PR-ABBANDONATE.md) | F1 → F2 → F3 → F4, in quest'ordine | Ogni fase svuota una PR aperta. Finché sono aperte, **qualunque piano nuovo rischia di riscriverne il contenuto** — è già successo con la #72 |
| **②** | [RICERCA-MESTIERE-CARTOGRAFO-E-ILLUSTRATORE](RICERCA-MESTIERE-CARTOGRAFO-E-ILLUSTRATORE.md) | la **F1 (audit)** può partire subito e in parallelo; la **F2 (gate)** dopo la F1 | La F2 senza la F1 tara le soglie a occhio, e un gate tarato male si disattiva entro un mese. La **F3 della ripresa** (la catena raster) è il **committente**: se parte prima che l'audit dica i criteri, automatizza senza saperli |
| **③** | [PIANO-VENDIBILITA](PIANO-VENDIBILITA.md) | dopo che ① e ② hanno chiuso il cancello di qualità | Il DM ha già deciso: **prima la qualità, poi il mercato**. E il suo blocco **D1** (le immagini non arrivano al volume da stampa) è nel perimetro della ② |
| **④** | I piani d'arco (`REVISIONE-ARC07/08/09`) | quando l'arco si gioca | Gated sul tavolo, non su di noi |

### Le due sovrapposizioni da non creare

⚠️ **Non aprire un piano sulle mappe.** Ce ne sono già quattro più una ricerca.
Qualunque lavoro sulle mappe entra in **②** (qualità del disegno) o in
`PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI` (fedeltà del renderer). La scelta fra i
due è: *è un problema di cosa si vede, o di cosa si perde?*

⚠️ **Non aprire un piano sulle immagini.** L'automazione è **F3 di ①**, il
mestiere è **②**, la norma è la skill `rumblingstone-art-direction`. Tre posti,
tutti esistenti.

---

## 3 · Cosa resta da fare, per piano

### ① Ripresa PR abbandonate — F0 ✅, restano F1-F4

- **F1 · #63** — le 14 griglie tattiche di Hammerfist che al tavolo mancano,
  **3Y compresa**. Contenuto pronto e verificato byte-identico. ⚠️ Il gate di
  ADR-0043 adesso **forza** la decisione D1 invece di lasciarla al diff.
- **F2 · #52** — l'overlay `@` sui master scritti a mano. Costo: **una
  rinominazione**.
- **F3 · #106** — la catena raster: **cinque requisiti su sei**, e la fase
  aggiunge il sesto (`SCARTI.txt`). ⚠️ L'ultimo passo vuole la **GPU del DM**.
- **F4 · #99** — **a otto lotti**, `validate_docs` per primo.

### ② Ricerca sul mestiere — tutta da eseguire

F1 audit (31 SVG / 17 master + set immagini) · F2 i gate scrivibili · F3 le
norme nelle skill esistenti. **Bloccata su una domanda**: quali mappe pubblicate
sono lo standard.

### Le PR ancora aperte, oggi

| PR | Verdetto | Dove sta scritto | Che si fa |
|---|---|---|---|
| **#63** | abbandonata, **non** superata | ① F1 | si svuota — è la prossima |
| **#52** | abbandonata, **non** superata | ① F2 | si svuota |
| **#106** | abbandonata, **non** superata | ① F3 | si svuota, serve la GPU del DM |
| **#99** | abbandonata, **non** superata | ① F4 | si svuota a otto lotti |
| **#67** | **superata** | `RICONCILIAZIONE-PR` R9 | **si chiude**, niente da recuperare |

⚠️ **Nessuna delle cinque si mergia com'è.** Le quattro abbandonate hanno una
base di mesi fa: se ne porta il **contenuto**, non i commit. La #67 non ha
contenuto da portare, e mergiarla rimetterebbe in circolo un handout che detta
tattica al giocatore.

### Code aperte che non sono un piano

| Coda | Quanto | Dove sta scritta |
|---|---|---|
| Celle `⬛` da riclassificare in ⛺/🔳 | **8.216** in 24 file | `LEGENDA-FUNZIONALE-SPEC` §6.2, mappa per mappa |
| Mappe con l'intestazione discorde | **6** | `RICERCA-MESTIERE` §6 |
| `state.md` §1 forward-written | — | lotto **4c** di F4 (era il difetto C1 della #99) |

---

## 3-bis · La classe di ogni lotto rimasto (ADR-0045)

Il taglio segue la **classe di lavoro**, non la dimensione — e serve a rendere
esplicito il compromesso fra costo e qualità, che finora era un default
silenzioso.

| Piano | M meccanico | R ricognizione | C costruzione | G giudizio | K canone |
|---|:---:|:---:|:---:|:---:|:---:|
| ① Ripresa PR — F1 | 2 | — | 1 | 1 | — |
| ① F2 | 2 | — | 1 | — | — |
| ① F3 | 1 | — | 2 | 1 *(il DM)* | — |
| ① F4 | 1 | — | 3 | 1 | **3** |
| ② Ricerca sul mestiere | — | 2 | 1 | 1 | **1** |
| **Totale** | **6** | **2** | **8** | **4** | **4** |

**Come si legge.** Otto lotti su ventiquattro sono **C** — codice con un
contratto chiaro e dei test — e delegabili. Sei sono **M** e non hanno bisogno di
niente più di un gate che dica sì o no. **Otto sono G o K**, cioè giudizio o
canone: quelli restano in sessione principale su `Opus 5` e non si delegano.

⚠️ **Quattro lotti su otto della F4 sono K.** È la misura di quanto la #99 tocchi
il canone, e la ragione per cui non si mergia in blocco.

⚠️ **La tabella è tarata a occhio.** Nessuno ha eseguito lo stesso lotto su due
engine per confrontare: è un'ipotesi dichiarata, da correggere quando i lotti
classificati saranno abbastanza da dire qualcosa.

⚠️ **I 24 non sono tutto il lavoro aperto dell'archivio**, e la mia prima
stesura lo lasciava intendere. Sono i lotti dei **due piani aperti**. Altri
undici documenti contengono in tutto **43 caselle `⬜`** — ma quel numero grezzo
**non è un conteggio di lotti**: separandole sono **29 citate nel testo · 6
celle vuote · 5 lotti veri · 3 glifi di stato** (il «⬜ NON giocato» di un arco
non è un lotto). Contarle bene vuol dire **leggerle una per una**, che è un lotto
**G** e non **R** — e finché non è fatto, «quanto lavoro resta nell'archivio» non
ha una risposta onesta.

⚠️ **Il guadagno vero non è il prezzo per token.** È la colonna «qualità», che
costringe a scrivere il collaudo **prima** di partire — e un lotto la cui
riuscita non si sa descrivere è un lotto tagliato male.

## 4 · Le decisioni ferme al DM

> ⚠️ **Questa tabella è generata**, come `docs/tools/registry.json` lo è dal
> manifest. La fonte sono le tabelle marcate `<!-- decisioni-dm: … -->` dentro i
> piani: si modifica **là**, e qui si rigenera con
> `python3 scripts/decisioni_dm.py --emit`. Il gate `--check` fa rossa la CI se
> le due cose divergono — vedi
> [ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md).
>
> ⚠️ **`D<n>` non è un identificatore globale**: otto piani hanno il loro
> `D1..Dn` con significati diversi (in `REVISIONE-ARC07` sono 17 decisioni *già
> prese*). L'identità è la coppia **piano#Dn**, e la colonna «Piano» serve a
> quello, non all'ordine.

<!-- auto:begin key=decisioni-dm -->

**4 aperte** · 11 chiuse — generato da `scripts/decisioni_dm.py --emit`, non si scrive a mano.

| # | Piano | Ambito | Domanda |
|---|---|---|---|
| **D2** | `RIPRESA-PR` | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM **con Gemini** il 2026-08-15, montati nel modulo, `validate_standalone` verde. `comfyui_batch --lista` dava «6 da fare» per un **disallineamento di nomi**, corretto in questo lotto. La domanda vera è: **l'arte del Drappo è di Gemini, la catena di F3 genera con SDXL in locale — quale delle due è il canone del modulo?** Le differenze che contano (ADR-0019 §2, che questo caso l'aveva previsto): Gemini **non espone il seed**, quindi la serie è irripetibile e il PNG è la sorgente; i suoi termini sono un **contratto che cambia**, verificato per di più su fonti secondarie; SDXL è OpenRAIL++-M, **perpetua**. Di contro la provenienza di Gemini è **firmata C2PA**, e SDXL su queste immagini **nessuno l'ha visto**. 🔵 **Metodo scelto dal DM il 2026-09-11: collaudo prima di scegliere** — la decisione **resta aperta**, si chiude quando il DM ha visto il confronto. Il DM: *«voglio fare prima un collaudo con 2 o 3 immagini e vedere davvero la qualità prima di buttare quelle di Gemini, che sono carine»*. Si generano **due o tre** immagini con SDXL in una cartella a parte, si mettono accanto alle attuali, e A (tenere Gemini) o B (rigenerare tutto) si sceglie **guardando**. Il collaudo chiude anche il buco vero di F3 — la catena mai provata contro un ComfyUI reale — al costo di due immagini invece che diciotto |
| **D11** | `RIPRESA-PR` | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un **AP originale autonomo**, mai un'espansione di RHoD, e porta il **perimetro della v1**. ✅ **I due avvertimenti che bloccavano la domanda sono tolti**: l'audit mancante è stato **rifatto da zero** ([`AUDIT-DERIVAZIONE-IP-CAMPAGNA`](../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md)), e la tesi **regge sul repo di oggi** — archi 07+08 a **0,2** e **0,7** occorrenze RHoD per 1.000 parole contro il **5,6** dell'arco 09. 🔎 **E la misura ha aggiunto due cose che la #72 non sapeva**: il **`Bestiario/` è a 3,0** e **esce col modulo** — un perimetro che tace su di lui lascia fuori il conto una dipendenza vera — e i **moduli autoconclusivi sono già puliti** (`10-stand-alone` e il Drappo a **0,0**), quindi su quest'asse il prodotto della linea 3 di `PIANO-VENDIBILITA` è pronto. 🔴 **Cosa resta da decidere al DM**: (a) si adotta il perimetro così com'è? (b) il **bestiario** sta dentro o fuori? (c) l'ADR resta proposta finché non c'è la **verifica di un avvocato IP**, che l'audit non sostituisce — conta i nomi, non la struttura |
| **D2** | `VENDIBILITA` | **Quanto è alta una tenda, e quanto un dais?** Nella catena Blender `⛺` e `🔳` non hanno un'altezza propria: si estrudono entrambi al default generico di **0,6 m**, mentre un edificio sta a **3,2**. | 🐛 **Terzo sintomo di ADR-0042**, e il primo trovato **da un gate** invece che da un bug al tavolo: `legend/single-source` ha scoperto la tabella `ALTEZZE`, dove il commento accanto a `⬛` diceva ancora *«edificio, tenda, dais»* — il significato di **prima** della decisione che lo aveva abolito. Migrato **com'era**: l'altezza di una tenda è contenuto, non refactoring. Nessun artefatto 3D è committato, quindi il costo di deciderla adesso è **zero** |
| **D12** | `RICERCA-MESTIERE` | §6-bis | 🐛 **`Portale-Forgia-L2` mappa 2 ha una riga `17` duplicata** — una alla riga 290 del sorgente, una alla 297. Quale delle due debba portare un altro numero (19? 24?) lo sa solo chi ha disegnato l'arena circolare: **indovinarlo sposterebbe delle celle**, quindi è rimasto com'è e marcato nel master |
| ~~D1~~ | `RIPRESA-PR` | F1 | ✅ **decisa 2026-09-05: archiviazione.** I tre master e i loro 7 SVG in `_ARCHIVIO/`; gli SVG non cancellati, così la cartella resta dentro il raggio di `validate_maps` |
| ~~D3~~ | `RIPRESA-PR` | F4 · 4c | ✅ **chiusa il 2026-09-12, eseguita nello stesso commit in cui e' stata dichiarata chiusa** (la lezione di D4). Il DM ha risposto il 2026-09-11 e il lotto 4c ha applicato entrambe le risposte: il **Giorno di Marcia 19** e' il punto di sincronia a cui il calendario torna col viaggio nel tempo — non un difetto, un tempo verbale, corretto; il **-2 COS di Thorik** era registrato come versato per una scena mai giocata, tolto dal presente insieme ai **-500 PE di Tordek**, che avevano lo stesso difetto e che nessuno aveva notato. 🔎 **E il lotto ha trovato il resto della stessa crepa**: §1 collocava tutti e quattro i PG dopo Hammerfist e dava **Hella viva**, mentre §6 dello stesso file la dava *«dead — resurrection pending»*. Vedi **§4.2-quater** |
| ~~D13~~ | `RIPRESA-PR` | F4 · 4c | ✅ **DECISA E ATTUATA il 2026-09-12, nello stesso commit.** Il DM ha approvato la **v4-bis**, con l'ultima taratura sua: **−1 CA invece di −2** per Thorik. 🛡️ **Thorik** dona il **+2 di deflessione della Corona** → **Scudo del Custode** (1/g, immediata: Hella prende il danno di un alleato entro 9 m **dimezzato**) + **l'Eco del Custode**, che e' l'idea del DM: quando lei scuda qualcuno **lui e' accelerato 3 round e si muove verso chi e' stato protetto** — l'anello si chiude, la protezione data torna al donatore trasformata in velocita'. ⚒️ **Tordek** dona **Ancoraggio della Montagna** → **Pelle di Adamantio RD 3/adamantino**. 🔮 **Artemis** dona **1d6 di Eldritch Blast** (7d6 → 6d6) → **Rovo Eldritch** a volonta': il DM ha visto che il dono precedente **si sovrapponeva** a quello di Thorik (stessa casella, dare tempo a un altro). ⚒️ **Reazioni degli artefatti al dono e al rifiuto**, tutte reversibili e tutte fondate sulla personalita' gia' in scheda. 🌱 **E il potere #6 della Collana non e' piu' `[da definire col DM]`**: il seme **restituisce** al donatore, una volta sola, e decide Hella. **Attuato in 17 file** + **12 istantanee** in `_ARCHIVIO/doni-v1-2026-09-12/`. Vedi **§4.2-quinquies** |
| ~~D4~~ | `RIPRESA-PR` | F4 | ✅ **chiusa il 2026-09-11: non era una domanda.** Misurato invece di ricordare: il `PALIO-BOOKLET` cita **14 file** — 8 stemmi, 4 mappe, 2 immagini — ed **esistono tutti e 14**. SVG veri da 2,7-5,4 KB, due PNG da ~2 MB, e `CREDITS.md` con l'attribuzione **CC BY 3.0** a game-icons.net già in regola. Niente da produrre, niente da togliere. 🔎 Settimo presupposto invecchiato di questa campagna, e la chiusura era rimasta indietro di un giro: annunciata il 2026-09-11 e non eseguita nello stesso commit |
| ~~D5~~ | `RIPRESA-PR` | ~~fuori piano~~ | ✅ **deciso e fatto il 2026-09-04**: il DM l'ha messo in cima alla coda, ed è chiuso insieme al punto cieco di `validate_maps` (ADR-0043) |
| ~~D6~~ | `RIPRESA-PR` | F1 | ✅ **decisa 2026-09-04: ridisegnata.** `…P1C` mappa 3 dichiarava 40×40 e aveva righe da 24 a 26 celle: rifatta **26×29**, nessuna coordinata del testo cambiata |
| ~~D1~~ | `VENDIBILITA` | ✅ **DECISA il 2026-09-12 — la spec funzionale è ratificata.** Vedi §10 per cosa è entrato e a che prezzo. In sintesi: i campi neutri entrano tutti per i **56 simboli** che ne hanno uno; `📦` diventa muro; `🌲` e `🌳` **no**, con deroga motivata; la luce resta quella del codice, scritta in metri. | ✅ Costo pagato: **+4 polilinee** su ciascuno dei 2 `.uvtt` committati, **zero** SVG. Il resto è additivo. 🔵 Ne è nata [**ADR-0049**](adr/ADR-0049-il-margine-del-bosco-e-un-glifo-a-se.md): `🌲` avrà un glifo per il margine, con una coda di **1.873 celle** da rileggere |
| ~~D7~~ | `RICERCA-MESTIERE` | metro di paragone | ✅ **decisa 2026-09-11: le mappe di *Red Hand of Doom* e quelle di *Rise of the Runelords* (Paizo)** — *«voglio quella qualità e risultato, o il più vicino possibile»*. 🔎 Le prime **sono già nel repo**: **69 immagini** in `00_Red Hand Of Doom/Immagini/`, divise in `MappeIncontri`, `MappeLuoghiTattiche`, `MappeVarie` — il metro si guarda, non si immagina. ⚠️ **Rise of the Runelords non si porta nel repo**: è IP Paizo (ADR-0005). Si nomina come riferimento e si tiene fuori; l'audit cita numeri e criteri, mai i file |
| ~~D8~~ | `RICERCA-MESTIERE` | stampa | ✅ **decisa 2026-09-11: a colori.** A1.6 (daltonismo) e A1.7 (resa in grigi) **restano non bloccanti**: la seconda perde quasi tutto il suo senso, la prima no — il daltonismo non dipende dalla stampante, e va tenuta come avviso |
| ~~D9~~ | `RICERCA-MESTIERE` | doppia versione | ✅ **decisa 2026-09-11: né tutte né solo le hero map — quelle che nascondono qualcosa.** Il DM: *«per le mappe che hanno interazione con i giocatori e che devono nascondere cose ai giocatori o dettagli che devono scoprire»*. Il criterio è **funzionale**, quindi decidibile da chi scrive la mappa e non da una lista: se la griglia contiene una porta segreta, un nemico non ancora visto, una trappola o un indizio da scoprire, serve la versione giocatori. Oggi ce l'ha **una sola** (`tarsilia-la-ruota-giocatori`) |
| ~~D10~~ | `RICERCA-MESTIERE` | §6 | ✅ **decisa e fatta il 2026-09-11.** Il DM: leggile tutte, proponi mappa per mappa, e archivia **solo dove tocchi la griglia** — oggi **nessuna**, quindi nessuna copia in `_ARCHIVIO/` e `git` fa da archivio. 🔎 Rileggendole una per una **la mia stessa proposta si è rivelata sbagliata su due mappe su tre**: solo `L1` era una pura etichetta da correggere; `L2` mappa 1 e mappa 2 sono **estratti**, non griglie mal etichettate. Vedi §6-bis, riscritta sulle celle contate. Fatte: **1 etichetta corretta** (`L1` 20×13 → 20×14, con l'area a 21 m che ne discende), **1 intestazione trasposta corretta** (`L2` mappa 1 → 21 colonne × 53 righe) e **4 marcature di estratto**. `validate_maps` resta a 40 SVG / 18 master, nessuna cella toccata |

<!-- auto:end key=decisioni-dm -->

---

## 5 · Come si tiene aggiornato

Chi chiude un lotto aggiorna **quattro** cose nello stesso commit: la checklist
del piano, `INDEX.md`, `CHANGELOG.md` e — se cambia l'ordine o le dipendenze —
**questo documento**.

Le prime tre le controlla `check_plans_discipline`. La quarta era *«una debolezza
dichiarata»*, e il 2026-09-06 ha ceduto: §4 dava una decisione aperta il giorno
dopo che era stata presa, ne ometteva un'altra, e ne elencava **quattro che non
esistevano in nessun piano**. Adesso **§4 è generata** e il drift è rosso in CI
([ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md)):

```bash
python3 scripts/decisioni_dm.py --check   # gate: l'aggregato combacia coi piani?
python3 scripts/decisioni_dm.py --emit    # rigenera §4 dopo aver toccato un piano
```

⚠️ **Il resto di questo documento resta scritto a mano**, e resta una
fotografia: l'ordine delle fasi, le dipendenze, i costi. Il gate copre la
tabella delle decisioni, non il giudizio che c'è attorno.
