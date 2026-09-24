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
| **⑤** | [PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) | Fase 0 appena il DM risponde a D1-D5; la Fase 1 dopo 4f di ① | Aperto il 2026-09-24 dalla D21: assorbe 4f-5. Partire prima di chiudere 4f vorrebbe dire scrivere il delta allargato su un reset che cambia ancora |

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

### ① Ripresa PR abbandonate — F0, F1, F2 ✅; F3 e F4 in corso

- ✅ **F1 · #63** e ✅ **F2 · #52**: chiuse il 2026-09-05, PR chiuse il
  2026-09-11.
- 🟡 **F3 · #106**: 3a-3c chiusi. Resta **3d**, che è la decisione D2 del
  piano: il collaudo SDXL di due immagini accanto alle Gemini, sulla macchina
  del DM.
- 🟡 **F4 · #99**: 4a, 4b, 4c, 4d (4d-1 … 4d-8) e **4e** (una sola via di
  scrittura, 2026-09-24) e **4f** (prodotto e partita, 2026-09-24: la partita
  è un elenco, la cronaca è separata, `dm.py gruppo nuovo`; 4f-5 è passato al
  piano del ciclo di sessione per decisione D21) chiusi. Restano **4g** (schede
  PG a dati), **4h**
  (`groups/<slug>/`, PR dedicata) e **4i**, aggiunto il 2026-09-24 su richiesta
  del DM: il gate vede i percorsi fra backtick in tutti i sorgenti,
  `contenuti_nei_rami.py` dà un posto ai file rimasti nei rami, e la D22 ha
  dato un esito a tutti e quattro. Resta **4i-3**, la protezione di `main`
  (misurato `protected: false`), che il DM ha rinviato. La D24 è chiusa: il
  Collezionista fugge nel Piano del Fuoco, e Varis è il suo informatore.

### ② Ricerca sul mestiere — tutta da eseguire

F1 audit (31 SVG / 17 master + set immagini) · F2 i gate scrivibili · F3 le
norme nelle skill esistenti. **Bloccata su una domanda**: quali mappe pubblicate
sono lo standard.

### Le PR ancora aperte, oggi

*Rimisurato il 2026-09-24 sull'elenco delle PR aperte del repo. La tabella di
prima era ferma al 2026-09-04: dava aperte #63, #52 e #67, chiuse l'11
settembre, e non conosceva la #143.*

| PR | Verdetto | Dove sta scritto | Che si fa |
|---|---|---|---|
| **#143** | contenuto portato su `main` | `PIPELINE-IBRIDE`, riga del CHANGELOG del 2026-09-24 | ✅ **chiusa il 2026-09-24**: il piano è entrato con la #160, l'ADR come **0067** (lo 0050 era occupato) |
| **#106** | abbandonata, **non** superata | ① F3 · 3d | resta aperta finché il DM non ha fatto il collaudo SDXL (D2): serve la sua GPU |
| **#99** | abbandonata, **non** superata | ① F4 · 4f, 4g, 4h | si svuota: restano tre lotti, e 4h vuole una PR sua |

⚠️ **Nessuna delle due si mergia com'è.** Hanno una base di agosto: se ne porta
il **contenuto**, non i commit, come si è fatto con la #143.

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

**15 aperte** · 41 chiuse — generato da `scripts/decisioni_dm.py --emit`, non si scrive a mano.

| # | Piano | Ambito | Domanda |
|---|---|---|---|
| **D1** | `CICLO-SESSIONE` | F1 · 1c | **La cronaca si aggiorna da sola?** La chiusura aggiungerebbe una voce costruita dal log (Summary e Key decisions) in una regione marcata di `campaign-chronicle.md`. Oggi il vincolo 3 di ADR-0007 ammette scritture automatiche solo nelle regioni `auto:` di `state.md`: dire sì vuol dire estenderlo alla cronaca. Proposta: sì, in una regione marcata in coda |
| **D2** | `CICLO-SESSIONE` | F1 · 1b | **Le alleanze diventano un dato?** Oggi non esistono in `state.yaml`: `state_sync` le riconosce nel testo del log (Dauth, Rethmar, Starsong, i druidi…) e le stampa. Per farne una domanda serve una tabella nuova (fazione, atteggiamento SRD, nota). È canone: i valori di partenza li scegli tu. Proposta: sì, con gli atteggiamenti SRD (ostile … amichevole) |
| **D3** | `CICLO-SESSIONE` | F2 · 2d | **Chi scrive la prosa di gioco che manca** (interazioni dei PNG, testo degli handout, echi)? (a) il DM, o una sessione di agente con le skill, partendo dal brief; (b) una bozza del ponte di ADR-0067, che riapre il lotto E-bis escluso il 2026-07-20. Proposta: (a) adesso, (b) da rivalutare dopo il collaudo |
| **D4** | `CICLO-SESSIONE` | F3 · 3a | **Che menu?** Numerato in testo semplice (libreria standard, funziona ovunque e si avvolge facilmente) oppure a schermo intero con `curses` (che su Windows non c'è). Proposta: numerato |
| **D5** | `CICLO-SESSIONE` | F2 · 2c | **Le immagini mancanti si generano durante la preparazione?** Serve ComfyUI sulla macchina del DM e minuti per immagine. Proposta: la preparazione le **elenca** e lancia `comfyui_batch` solo se il DM lo chiede |
| **D6** | `CICLO-SESSIONE` | F0 · 0c | **BDD con un framework, o solo la sua pratica?** Misurato in [RICERCA-BDD-O-TDD-2026-09](RICERCA-BDD-O-TDD-2026-09.md): `behave` trova gli stessi 16 difetti su 16 del TDD, con +42% di righe, +45% di tempo e 3 MB di dipendenze contro ADR-0037; in cambio il `.feature` si legge senza aprire Python. (a) la pratica senza framework: scenari con identificatore in §4, test che li citano, un gate stdlib che li tiene allineati; (b) `pytest-bdd` con un'eccezione ad ADR-0037; (c) niente, come oggi. Proposta: (a) |
| **D1** | `PIPELINE-IBRIDE` | Lotto A | **Cosa fa il grounding quando trova un difetto in una mappa di canone già giocata?** 🔎 **Non è più una domanda astratta: la misura del 2026-09-16 c'è.** 97 sacche isolate su 40 griglie, di cui **58 con dentro un segnalino di creatura**, 15 porte cieche, 12 griglie che una creatura Grande non attraversa. Una sola sacca è stata verificata a mano fino in fondo, ed **era un difetto vero**: i tre box delle stalle di Tarsilia, chiusi da `🏰` senza `🚪`, con dentro il cavallo che la tattica scritta dice di raggiungere. Le altre 57 **non sono state triangolate**, e il conto grezzo non dice quante siano difetti. Le tre risposte restano: (a) **segnala e basta**, gate non bloccante, canone invariato; (b) **segnala e si correggono le mappe**, cioè toccare griglie approvate; (c) **si esenta il canone esistente**, col rischio dell'esenzione silenziosa che ADR-0032 §1 ha già evitato una volta. 🔵 La proposta resta **(a)**, e adesso con un motivo misurato: 58 segnali non triangolati non possono bloccare una CI. Ma Tarsilia va corretta comunque, perché è un modulo standalone destinato a uscire. ✅ **Tarsilia corretta il 2026-09-24** (variante B: `🧱` e una porta per box); la domanda di D1 resta aperta per le altre 57 |
| **D2** | `PIPELINE-IBRIDE` | Lotto B · B1 | **Dove vive il contratto d'estrazione dalla prosa?** Dentro `skills/rumblingstone-mapmaking/SKILL.md`, dove ogni agente lo vede sempre e paga i token a ogni conversazione, oppure in un file di riferimento caricato solo quando la skill instrada là. `measure_tokens.py` sa dare il costo delle due strade sullo stesso testo: la domanda si può decidere con un numero invece che a occhio |
| **D3** | `PIPELINE-IBRIDE` | Lotto E | **Il ponte `llm_bridge.py` si costruisce, o ADR-0067 resta scritta e il codice aspetta?** La proposta è aspettare: con A e B chiusi il ciclo funziona a mano, e allora si vedrà se il ponte fa risparmiare davvero. Serve una risposta solo quando A e B sono chiusi |
| **D4** | `PIPELINE-IBRIDE` | Lotto D | **Quante scene il DM è disposto ad annotare?** Il banco di misura della prosa esiste solo se qualcuno dice quali testi sono buoni, e l'unico che può dirlo è chi li ha visti funzionare al tavolo. Con zero scene annotate il lotto D copre le prime tre famiglie di §6 e la quarta resta fuori, il che è una risposta legittima e va detta invece che rimandata |
| **D2** | `MESTIERE-BANCHI` | F2 · S4-S6 | **ARC-08 e ARC-09 si rifiniscono nello stile, o si toccano solo dove manca un congegno operativo al tavolo?** Cambia l'ampiezza dei lotti da «aggiungere una sidebar» a «riscrivere prosa». I due archi sono chiusi come *piano* e ⬜ come *gioco*: la Torre non ha **una sola battuta** in 12 file e la Battaglia Finale **zero read-aloud** in 16, ma nessuno dei due è mai stato giocato, quindi nessuno li ha visti mancare |
| **D3** | `MESTIERE-BANCHI` | F2 · S2-S3 | **DEF-1 è 🟡 in corso al tavolo: i lotti su di lui restano additivi?** Il piano assume di sì (si aggiungono sidebar, non si riscrive prosa già letta ai giocatori), ma è un'assunzione mia. DEF-1 ha **0 vie non combattive in 2.277 righe**: colmarlo è additivo, ma toccare i suoi read-aloud non lo sarebbe |
| **D2** | `RIPRESA-PR` | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM **con Gemini** il 2026-08-15, montati nel modulo, `validate_standalone` verde. `comfyui_batch --lista` dava «6 da fare» per un **disallineamento di nomi**, corretto in questo lotto. La domanda vera è: **l'arte del Drappo è di Gemini, la catena di F3 genera con SDXL in locale — quale delle due è il canone del modulo?** Le differenze che contano (ADR-0019 §2, che questo caso l'aveva previsto): Gemini **non espone il seed**, quindi la serie è irripetibile e il PNG è la sorgente; i suoi termini sono un **contratto che cambia**, verificato per di più su fonti secondarie; SDXL è OpenRAIL++-M, **perpetua**. Di contro la provenienza di Gemini è **firmata C2PA**, e SDXL su queste immagini **nessuno l'ha visto**. 🔵 **Metodo scelto dal DM il 2026-09-11: collaudo prima di scegliere** — la decisione **resta aperta**, si chiude quando il DM ha visto il confronto. Il DM: *«voglio fare prima un collaudo con 2 o 3 immagini e vedere davvero la qualità prima di buttare quelle di Gemini, che sono carine»*. Si generano **due o tre** immagini con SDXL in una cartella a parte, si mettono accanto alle attuali, e A (tenere Gemini) o B (rigenerare tutto) si sceglie **guardando**. Il collaudo chiude anche il buco vero di F3 — la catena mai provata contro un ComfyUI reale — al costo di due immagini invece che diciotto |
| **D11** | `RIPRESA-PR` | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un **AP originale autonomo**, mai un'espansione di RHoD, e porta il **perimetro della v1**. ✅ **I due avvertimenti che bloccavano la domanda sono tolti**: l'audit mancante è stato **rifatto da zero** ([`AUDIT-DERIVAZIONE-IP-CAMPAGNA`](../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md)), e la tesi **regge sul repo di oggi** — archi 07+08 a **0,2** e **0,7** occorrenze RHoD per 1.000 parole contro il **5,6** dell'arco 09. 🔎 **E la misura ha aggiunto due cose che la #72 non sapeva**: il **`Bestiario/` è a 3,0** e **esce col modulo** — un perimetro che tace su di lui lascia fuori il conto una dipendenza vera — e i **moduli autoconclusivi sono già puliti** (`10-stand-alone` e il Drappo a **0,0**), quindi su quest'asse il prodotto della linea 3 di `PIANO-VENDIBILITA` è pronto. 🔴 **Cosa resta da decidere al DM**: (a) si adotta il perimetro così com'è? (b) il **bestiario** sta dentro o fuori? (c) l'ADR resta proposta finché non c'è la **verifica di un avvocato IP**, che l'audit non sostituisce — conta i nomi, non la struttura |
| **D12** | `RICERCA-MESTIERE` | §6-bis | 🐛 **`Portale-Forgia-L2` mappa 2 ha una riga `17` duplicata** — una alla riga 290 del sorgente, una alla 297. Quale delle due debba portare un altro numero (19? 24?) lo sa solo chi ha disegnato l'arena circolare: **indovinarlo sposterebbe delle celle**, quindi è rimasto com'è e marcato nel master |
| ~~D1~~ | `MESTIERE-BANCHI` | F2 · S7 | ✅ **DECISA E ATTUATA il 2026-09-18, nello stesso commit.** Il DM ha **separato le due cose**: *«l'unica cosa da prendere è l'ADR quarta colonna, che può essere usata in diversi contesti nei vari archi [...] gli ADR interni li lascerei all'Abbazia [...] ma ovviamente la versione nell'Abbazia rimane così com'è senza estensione»*. → [ADR-0057](adr/ADR-0057-la-quarta-colonna-e-di-tutto-il-repo.md): la quarta colonna entra in `editorial-standards.md` §2 come norma del repo; i dodici ADR interni restano dell'Abbazia; l'Abbazia **non si tocca**. 🔎 **Misurato prima di scrivere la norma, e il numero ha cambiato cosa aspettarsi**: nel repo giocabile esisteva **un solo** blocco sensoriale strutturato (`ARC07-DEF-1` §4) — gli archi il sensoriale lo scrivono dentro la prosa dei read-aloud, non in schede. Come retrofit la norma vale **un posto**; il suo valore è prospettico, sui lotti S4-S6. ⚠️ **La forma è diversa dall'Abbazia, e apposta**: negli archi le schede sono **elenchi**, quindi la norma è sul *blocco* e non sulla colonna — in tabella è la quarta colonna, in elenco l'ultimo punto. Imporre la tabella avrebbe riscritto la forma per portare il contenuto |
| ~~D1~~ | `PRATICHE` | PI-2 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **La soglia delle 400 righe di codice per PR, come avviso in CI?** Oggi 13 merge su 34 la superano, e questa PR la supera di otto volte. Proposta: sì, avviso e non blocco |
| ~~D2~~ | `PRATICHE` | PI-3 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Dependabot, scansione dei segreti con push protection, `pip-audit`?** Le prime due si attivano nelle impostazioni del repository e sono gratuite perché il repo è pubblico. Proposta: sì a tutte e tre, `pip-audit` non bloccante per un mese |
| ~~D3~~ | `PRATICHE` | PI-6 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Le PR che toccano il canone si mergiano solo dopo la tua lettura dell'elenco?** Proposta: sì. Il resto lo verificano i gate |
| ~~D4~~ | `PRATICHE` | PI-1 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Il merge automatico delle PR verdi**, una volta protetto `main`? Proposta: sì, ed è ciò che rende economiche le PR piccole |
| ~~D5~~ | `PRATICHE` | PI-2 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). L'elenco misurato dopo `git fetch --prune` è di **38** rami, ed è nella risposta al DM dello stesso giorno: si cancellano quando il DM lo conferma. **I 39 rami remoti già interamente su `main` si cancellano?** L'elenco lo produce `misura_flusso`; `contenuti-nei-rami.json` conferma che non portano niente di nuovo. Proposta: sì, dopo che hai visto l'elenco |
| ~~D1~~ | `QUALITA-CODICE` | E1 · E3 | ✅ **decisa dal DM il 2026-09-23: sì**, il verificatore condivide il lettore ([ADR-0066](adr/ADR-0066-le-creature-hanno-una-libreria-e-il-verificatore-non-importa-la-scelta.md)). **Il verificatore condivide il lettore?** Oggi lo fa già: importa 23 simboli da `genera_attributi`. **Sì** (consigliato): il lettore va in `dmcore/lettura_creatura.py` e lo usano tutti; l'indipendenza sta nelle regole e nella scelta, che il verificatore non importa mai (E4 lo prova). **No**: il verificatore tiene un lettore suo, copiato, più sicuro contro un errore di lettura condiviso e con una seconda copia da tenere allineata a mano |
| ~~D2~~ | `QUALITA-CODICE` | E6 | ✅ **decisa dal DM il 2026-09-23: (a)**, vince `genera_attributi`; attuata in E6. **Quale tabella dei ruoli vince?** Dei 6 ruoli di `genera_creatura`, 4 ordinano le caratteristiche diversamente dal profilo corrispondente di `genera_attributi` (schermagliatore, tiratore, blaster, controllore). **(a)** vince `genera_attributi`: cambiano i PNG che `genera_creatura` genera d'ora in poi, nessun blocco del Bestiario; **(b)** vince `genera_creatura`: cambiano gli `attributi` di alcuni dei 15 blocchi scelti dall'array, che il DM vede prima; **(c)** si tengono separate e si dichiara perché |
| ~~D3~~ | `QUALITA-CODICE` | E9 | ✅ **decisa dal DM il 2026-09-23: sì, subito**; attuata in E9. **`dm.py bestiario` si fa in questo lotto o dopo?** Costa poco e non dipende dalla libreria; farlo prima di E8 vuol dire toccare `dm.py` due volte se un'interfaccia cambia |
| ~~D1~~ | `RIPRESA-PR` | F1 | ✅ **decisa 2026-09-05: archiviazione.** I tre master e i loro 7 SVG in `_ARCHIVIO/`; gli SVG non cancellati, così la cartella resta dentro il raggio di `validate_maps` |
| ~~D3~~ | `RIPRESA-PR` | F4 · 4c | ✅ **chiusa il 2026-09-12, eseguita nello stesso commit in cui e' stata dichiarata chiusa** (la lezione di D4). Il DM ha risposto il 2026-09-11 e il lotto 4c ha applicato entrambe le risposte: il **Giorno di Marcia 19** e' il punto di sincronia a cui il calendario torna col viaggio nel tempo — non un difetto, un tempo verbale, corretto; il **-2 COS di Thorik** era registrato come versato per una scena mai giocata, tolto dal presente insieme ai **-500 PE di Tordek**, che avevano lo stesso difetto e che nessuno aveva notato. 🔎 **E il lotto ha trovato il resto della stessa crepa**: §1 collocava tutti e quattro i PG dopo Hammerfist e dava **Hella viva**, mentre §6 dello stesso file la dava *«dead — resurrection pending»*. Vedi **§4.2-quater** |
| ~~D13~~ | `RIPRESA-PR` | F4 · 4c | ✅ **DECISA E ATTUATA il 2026-09-12, nello stesso commit.** Il DM ha approvato la **v4-bis**, con l'ultima taratura sua: **−1 CA invece di −2** per Thorik. 🛡️ **Thorik** dona il **+2 di deflessione della Corona** → **Scudo del Custode** (1/g, immediata: Hella prende il danno di un alleato entro 9 m **dimezzato**) + **l'Eco del Custode**, che e' l'idea del DM: quando lei scuda qualcuno **lui e' accelerato 3 round e si muove verso chi e' stato protetto** — l'anello si chiude, la protezione data torna al donatore trasformata in velocita'. ⚒️ **Tordek** dona **Ancoraggio della Montagna** → **Pelle di Adamantio RD 3/adamantino**. 🔮 **Artemis** dona **1d6 di Eldritch Blast** (7d6 → 6d6) → **Rovo Eldritch** a volonta': il DM ha visto che il dono precedente **si sovrapponeva** a quello di Thorik (stessa casella, dare tempo a un altro). ⚒️ **Reazioni degli artefatti al dono e al rifiuto**, tutte reversibili e tutte fondate sulla personalita' gia' in scheda. 🌱 **E il potere #6 della Collana non e' piu' `[da definire col DM]`**: il seme **restituisce** al donatore, una volta sola, e decide Hella. **Attuato in 17 file** + **12 istantanee** in `_ARCHIVIO/doni-v1-2026-09-12/`. Vedi **§4.2-quinquies** |
| ~~D4~~ | `RIPRESA-PR` | F4 | ✅ **chiusa il 2026-09-11: non era una domanda.** Misurato invece di ricordare: il `PALIO-BOOKLET` cita **14 file** — 8 stemmi, 4 mappe, 2 immagini — ed **esistono tutti e 14**. SVG veri da 2,7-5,4 KB, due PNG da ~2 MB, e `CREDITS.md` con l'attribuzione **CC BY 3.0** a game-icons.net già in regola. Niente da produrre, niente da togliere. 🔎 Settimo presupposto invecchiato di questa campagna, e la chiusura era rimasta indietro di un giro: annunciata il 2026-09-11 e non eseguita nello stesso commit |
| ~~D14~~ | `RIPRESA-PR` | F4 · 4d-2 | ✅ **CHIUSA E ATTUATA il 2026-09-16, nello stesso commit.** Il DM: *«la riga va in state.yml e poi riportata in state.md»*. Misurata, la risposta regge: la tabella dei waypoint è **dato puro** (10 righe) e il March Day è **un campo** (`march_clock.giorno_corrente`); il paragrafo di cinque righe che spiega perché il Giorno 19 è un bersaglio e non un passato resta **prosa, sotto e fuori** dalla regione generata. Separati, la macchina riscrive la sua riga a ogni sessione senza mai toccare la nota del DM — che era il nodo. ⚠️ La regione `auto:march-clock` **sparisce**, e marcarla oggi sarebbe *peggio* di prima: una regione dentro una `gen:state:` sono due scrittori sullo stesso testo. Sparisce anche `RETHMAR_DAY = 42`, cablato in `state_apply`: era la seconda fonte di verità più piccola del repo, e sopravviveva perché nessuno aveva mai eseguito il tool. Vedi **§4.8.9** e [ADR-0052](adr/ADR-0052-cosa-e-dato-e-cosa-e-prosa.md) |
| ~~D16~~ | `RIPRESA-PR` | F4 · 4d-2 | ✅ **CHIUSA E ATTUATA il 2026-09-16, nello stesso commit.** Il DM ha scelto l'enumerazione **con il compagno**: `attivo · latitante · neutralizzato · morto · ignoto`, più `reversibile`. ⚒️ `neutralizzato` copre il caso più frequente al tavolo — sconfitto ma non morto — e senza di lui il DM dovrebbe scrivere `morto` per non scrivere `attivo`. 🔴 **E `reversibile` è la metà che conta**: in questa campagna un morto torna (il Ghostlord nasce da un morto, Sal è protetto da un paradosso auto-consistente, Hella è morta in attesa del rito), quindi registrare «morto» senza dire se è definitivo è registrare **meno di quel che il canone sa**. La regola **R9** lo pretende. ⚠️ `state_apply` scrive `stato` ma **non** `reversibile`: il primo è la lettura letterale del log, il secondo è una decisione narrativa, e R9 la chiede al DM alla prima esecuzione — provato sul canone vero. 🔎 **§4 conoscenze è stata esclusa dopo averla misurata**, benché il DM avesse chiesto di includerla: tre righe non sono persone e tre persone compaiono sotto due nomi, quindi `stato` lì vorrebbe dire un valore privo di senso in tre casi e due copie divergenti in altri tre. Va nell'anagrafica del lotto della chiave. Vedi **§4.8.9** |
| ~~D17~~ | `RIPRESA-PR` | F4 · 4d-4 | ✅ **CHIUSA il 2026-09-17 — e la domanda aveva una premessa falsa, trovata dal DM.** Era posta come «i due villain senza scheda: si scrivono, si contano o escono da §3?». 🐛 **Tre delle quattro voci che avevo dichiarato senza scheda ce l'avevano.** Il DM: *«controlla bene negli archi o nel bestiario se c'è qualcosa magari annegato come prosa»*. **Zalkatar** ha uno statblocco a **GS 13** (14d4+70, CA 24) in `09_…/P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md`; **Saarvith + Regiarix** ne hanno uno a **GS 13** in `09_…/P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md`, e il file `FASE4` accanto dichiara esplicitamente *«le statistiche sono lì; questo è la regia dello scontro»*; il **Cerchio Druidico** ne ha uno in `Bestiario/mostri/cerchio-druid7-cr7.md`, marcato [ACCEPTED — DM-canon 2026-05-05]. L'errore non è stato non trovarle: ho cercato **solo dentro `Bestiario/`**, e allargando la ricerca ho **troncato l'output a sei righe** concludendo da una lista tagliata. ✅ Non c'era niente da scrivere né da togliere: c'era da **cercare meglio**. Resta **un** buco su 28 (`lathander-mask`), ed è corretto. ⚠️ **Conseguenza di progetto**: una scheda non vive per forza nel `Bestiario/`, e un cancello tarato lì avrebbe continuato a dare per mancanti due boss da GS 13. Nasce **R13**, che mette alla prova ogni buco dichiarato contro tutto il repo. Vedi **§4.8.10** e [ADR-0053](adr/ADR-0053-la-chiave-verso-il-bestiario-si-dichiara.md) |
| ~~D18~~ | `RIPRESA-PR` | F4 · 4d-6 | ✅ **DECISA E ATTUATA il 2026-09-17, nello stesso commit.** Il DM: *«spezzarli per intestazione verificando che non esistano già»*. Il catalogo portava **19 record intitolati al documento** invece che alla creatura, perché `build_monster_catalog.py` faceva **un record per file** e prendeva il primo GS: «Parte 2A – Torre Invisibile», GS 10. **19 → 8**, pool **372 → 397**. 🔎 Quel che ne è uscito non sono comparse: gli **otto fantini del Palio**, i **Sicari di Sonjak**, il Gonfaloniere Aldemar Vosk, la Drow Chierica di Lolth, gli esempi d'onda di Rethmar — tutti chiusi dentro un record solo. ⚠️ **La deduplica è ancorata a un fatto dichiarato**: si confrontano i nomi **solo** dentro l'insieme delle voci del Bestiario che citano *quel* documento come `Source`. È il modo di rispettare ADR-0053 (un matcher permissivo traveste l'ignoranza) senza rinunciare a dedurre: il legame documento↔voce l'ha scritto qualcuno, la somiglianza sceglie solo *quale* voce sta per *quale* intestazione. 🔴 **E il rischio opposto ha il suo presidio**: il record di file sparisce solo quando **ogni** creatura che il documento nomina ha già la sua voce — gli otto che restano sono quelli dove non è vero, e toglierli significherebbe meno rumore e **meno creature**. 🐛 Due difetti nei nomi generati, trovati misurando: la numerazione del Palio è **multi-livello** (`### 3.2 Drow Chierica`) e lasciava nomi che cominciavano per cifra, e la coda tagliata lasciava parentesi mai chiuse («Aldemar Vosk (LN»). 🔎 **E il cancello nuovo ha trovato un errore mio al primo giro**: contava **due** «Skullcrusher il Nero», perché la voce che avevo appena scritto puntava al file che il drago lo *nomina* soltanto — i numeri stanno in `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md`. Correggendo il puntamento è poi caduto fuori che `P6-INTEGRAZIONE` restava scoperto, e dentro c'erano **Re Thorek I** (Grr 16, il re di mille anni prima che si inginocchia davanti alla Corona) e **Durin Hammerfist**, l'antenato di Othrek: due PNG di canone che non aveva nessuno. Vedi **§4.8.12** e [ADR-0054](adr/ADR-0054-un-archivio-non-e-una-copia.md) |
| ~~D19~~ | `RIPRESA-PR` | F4 · 4f | ✅ **Risposta del DM il 2026-09-24, ed è un principio più largo della domanda**: *«la procedura dovrebbe essere quanto più automatizzata possibile: un DM normalmente non tocca affatto i file yml, al massimo se ha un'interfaccia scrive dei campi o seleziona i valori da un form già impostato»*. Quindi né lo scheletro da compilare né il derivato da rivedere a mano: il template è **derivato in automatico** dal prodotto, e ciò che resta di giudizio passa da un **modulo** a scelte. Procedura in §4.10.6, il via è **D21** |
| ~~D21~~ | `RIPRESA-PR` | F4 · 4f | ✅ **Risposta del DM il 2026-09-24.** Sulla procedura di §4.10.6: sì al comando `dm.py gruppo nuovo`; sì a togliere da sole le conoscenze sul party e a chiedere una riga alla volta solo dove serve un giudizio; **gli artefatti restano nel prodotto**, senza portatore; arco e livello di partenza a scelta; PG con nome, razza, classe, livello e PF, al massimo sei; clock a zero e trigger lasciati. Attuato in **4f-4**, §4.10.7. Sulle proposte di fine sessione (4f-5) il DM ha chiesto di più: *«non c'è un tool chiamato dal DM a fine sessione che prende le domande e genera lo state.md e la parte relativa di state.yaml in maniera automatica?»*, con il ciclo intero preparazione → tavolo → chiusura e un **menu testuale** che chiami `dm.py` e che un'interfaccia grafica possa avvolgere. 4f-5 passa a quel piano, commit successivo |
| ~~D22~~ | `RIPRESA-PR` | F4 · 4i | ✅ **Risposta del DM il 2026-09-24**: per le domande aperte del soggetto, cercare le risposte in tutte le PR, anche chiuse, poi seguire le proposte; piano di level design, `agents.conf` e Giorno 3 di Dauth come proposto. Trovato: **avevi risposto a tutto** (changelog della #72, rev. 5 e 6), e 133 righe su 133 sono in cronaca. Il soggetto è in `plans/`, datato; il basilisco confermato con la tua citazione; restano due conferme, la **D24**. Esiti degli altri tre file in §4.11.5 |
| ~~D23~~ | `RIPRESA-PR` | F4 · 4i | ✅ **Risposta del DM il 2026-09-24: da verificare dopo, e da riproporre come piano.** Diventa il lotto **4i-3** (§4.11.6), con le sue tre fasi. Misurato nel frattempo: `main` risulta `protected: false`, cioè oggi nemmeno una CI rossa impedisce il merge |
| ~~D24~~ | `RIPRESA-PR` | F4 · 4i | ✅ **Risposta del DM il 2026-09-24**: *«la destinazione del Piano del Fuoco è canone, e ha un senso anche per Therysol che vuole vendetta»*; e *«Varis era un informatore del Collezionista, non sono la stessa persona»*. Il GS di Maur (11) aveva già la sua risposta nel foglio XP. Attuato: la fuga nel Piano del Fuoco è canone in cronaca, coerenza, archi, lore di Cannath Vale, dossier del Collezionista e di Therysol. Varis verificato: la sua scheda (`Bestiario/png/Varis_Seta_Argento`) lo dà umano, GS 6, intermediario inconsapevole; la confusione stava solo nel dossier del Collezionista della prima stesura (aprile), nel titolo del suo file-rimando, in un prompt immagine e in due file di dati. Vedi §4.11.5 |
| ~~D20~~ | `RIPRESA-PR` | F4 · 4f-2 | ✅ **DECISA E ATTUATA il 2026-09-24, nello stesso commit.** Il DM: *«D20 ok ma non tralasciare nulla»*. Split per sezione come in §4.10.4: **528 righe su 528** ritrovate nelle due metà (controllate contro git da un test), nessuna duplicata, una sola parola spostata («ESCAPED», che la cronaca racconta già tre volte). Tredici rimandi aggiornati in undici file; restano sul nome vecchio i documenti datati (`plans/`, l'audit IP, la baseline del 21 settembre), come registro di quando sono stati scritti |
| ~~D1~~ | `VENDIBILITA` | ✅ **DECISA il 2026-09-12 — la spec funzionale è ratificata.** Vedi §10 per cosa è entrato e a che prezzo. In sintesi: i campi neutri entrano tutti per i **56 simboli** che ne hanno uno; `📦` diventa muro; `🌲` e `🌳` **no**, con deroga motivata; la luce resta quella del codice, scritta in metri. | ✅ Costo pagato: **+4 polilinee** su ciascuno dei 2 `.uvtt` committati, **zero** SVG. Il resto è additivo. 🔵 Ne è nata [**ADR-0051**](adr/ADR-0051-il-margine-del-bosco-e-un-glifo-a-se.md): `🌲` avrà un glifo per il margine, con una coda di **1.873 celle** da rileggere |
| ~~D2~~ | `VENDIBILITA` | ✅ **DECISA il 2026-09-12 — e allargata: le altezze diventano moduli di griglia.** Il DM: *«i muri normalmente sono 1.5, le tende falle più basse 1m»*. 🔎 **Il «1.5» non erano i muri veri**: nel repo `🏰` sta a 4 m, `⬛` a 3,2, `🗼` a 9 — un muro di pietra a 1,5 m sarebbe più basso di un uomo. Era `🧱` **muretto / copertura bassa**, l'unico simbolo chiamato «muro» che un'altezza non ce l'aveva: si estrudeva al default generico di 0,6 m, cioè un gradino, mentre l'etichetta promette copertura al petto. Poi il DM ha esteso la regola: *«muri piccoli 1.5 metri e poi multipli di 1.5 o approssimazioni più vicine possibili»*. Il quadretto del repo è 1,5 m, quindi **tutte e 31** le altezze sono state portate sul modulo: quadretti interi per ciò che sta in piedi (15), mezzo quadretto per l'ingombro che si scavalca (9), zero per ciò che è piatto (7). Prima erano numeri a occhio — 3.2 · 2.2 · 1.6 · 1.4 · 1.1 · 0.9 · 0.8 · 0.6 · 0.4 — che non volevano dire niente rispetto alla griglia su cui la scena è costruita. | ✅ Costo zero: nessun artefatto 3D è committato. 48 celle `🧱`, 9 `⛺`. 🔵 **Resta il dais** `🔳`, e non è una dimenticanza: **zero celle nel repo** — è nato con ADR-0042 e nessuno l'ha ancora disegnato. Deciderlo adesso sarebbe inventarlo; il giorno che serve costa zero |
| ~~D1~~ | `CONFORMITA-STATBLOCCHI` | `goblin-warrior1-cr05` | ✅ **decisa dal DM il 2026-09-23: For 11**, la Forza del goblin SRD. Cambiano la riga delle caratteristiche e il danno (1d6−1 → 1d6); lotta e attacco la presupponevano già |
| ~~D2~~ | `CONFORMITA-STATBLOCCHI` | `tyrgarun-blue-old-cr18` | ✅ **decisa dal DM il 2026-09-23: lotta +49, For 33 resta.** Tenere +46 voleva dire For 26-27 e abbassare morso, artigli, ali, coda e stritolamento, che tornavano tutti con For 33 |
| ~~D3~~ | `CONFORMITA-STATBLOCCHI` | `drow-assassina-lolth-cr10` | ✅ **decisa dal DM il 2026-09-23: For 12.** Lotta +6 → +7, danno della spada corta 1d6+1 → 1d6+2; l'attacco con Arma Accurata non cambia |
| ~~D4~~ | `CONFORMITA-STATBLOCCHI` | `drow-trickster-arcano-cr11` | ✅ **decisa dal DM il 2026-09-23: BAB +5.** Lotta +3 → +4; stocco e balestra tornavano già |
| ~~D5~~ | `CONFORMITA-STATBLOCCHI` | `ghost-lion-spettrale-cr8` | ✅ **decisa dal DM il 2026-09-23, in due passi.** Prima: trascrivere la fonte d'arco. Poi: *«verifica se è coerente con 3.5 o PF1e e scegli la versione più forte»*. Sulla base della fonte (9 DV, Des 18, Sag 12, Car 24) il **fantasma PF1e** vince: pf 103 contro 58, Tempra +10 contro +3, BAB +6 contro +4, tocco corruttore 8d6 contro 1d6. Il verificatore impara la variante PF1e dei non morti (d8, BAB ¾, Carisma per pf e Tempra), solo dove il `tipo` la dichiara. La fonte d'arco §2 diventa una copia di regia con il rimando alla scheda. ⚠ Regole del template citate a memoria: SRD e PRD bloccati dalla rete |
| ~~D12~~ | `CONFORMITA-STATBLOCCHI` | `ghost-lion-spettrale-cr8` | ✅ **chiusa con D5, il 2026-09-23**: nella versione PF1e scelta dal DM l'iniziativa è **+4** (Des +4, nessun talento) e l'attacco è il tocco corruttore **+9** (BAB +6, Des +4, Grande −1); il morso +10 della fonte non è un potere del fantasma |
| ~~D6~~ | `CONFORMITA-STATBLOCCHI` | `loxo-warrior3-cr4` | ✅ **decisa dal DM il 2026-09-23: umanoide mostruoso.** DV razziali in d8; dalla progressione SRD seguono BAB +6 (con lotta +15 e attacchi +1), Riflessi +4, Volontà +6 (ADR-0065 §2). 🐛 Il primo tentativo scriveva `pf-dado: 6d8+18` e il cancello lo respingeva: il campo deve seguire la formula della scheda, `3d8+3d8+18` |
| ~~D7~~ | `CONFORMITA-STATBLOCCHI` | `druid-bear-ally-cr12` | ✅ **decisa dal DM il 2026-09-23: due gruppi di statistiche, e la composizione della fonte d'arco** (`…STATBLOCCHI-EPICI` §6): Druido 10 / Barbaro 2. Il blocco è la forma d'orso bruno (pf 102, CA 20, artigli +16, TS +14/+4/+11), e tutto torna col SRD; la forma umana sta in una sezione a parte (pf 70, TS +11/+4/+11). `extract_statblocks --check` impara che una sezione «Forma …» o «Variante …» non è la prosa del blocco |
| ~~D10~~ | `CONFORMITA-STATBLOCCHI` | `razorfiend-green-cr9` · `razorfiend-white-cr8` | ✅ **decisa dal DM il 2026-09-23: si applicano.** `pf-dado` trascritto dalla prosa (`10d12+50`, `9d12+36`), la Cos ricavata da lì da `genera_attributi` (20 e 18, erano 18 e 23), i TS ricalcolati dal SRD: verde **+12/+8/+10**, bianco **+10/+6/+7**. Il verde torna con la variante blu del DM su Tempra e Riflessi; la Volontà resta legata a una Sag generata, e la marca lo dice |
| ~~D11~~ | `CONFORMITA-STATBLOCCHI` | `derive_statblocks --apply-ts` | ✅ **decisa dal DM il 2026-09-23: si tiene, e scrive anche le caratteristiche da cui deriva.** Le caratteristiche non le sceglie più la matrice di `derive_statblocks`: vengono da `genera_attributi.genera`, la stessa funzione con gli stessi strati, e i TS si ricalcolano da quelle. Il blocco porta la marca di `genera_attributi`, quindi il suo `--check` lo verifica come uno suo. 🐛 La prima stesura lasciava i TS della matrice nel blocco provvisorio, e il tetto dei TS li leggeva: una prova lo presidia |
| ~~D8~~ | `CONFORMITA-STATBLOCCHI` | `gnoll-cleric-yeenoghu-cr7` | ✅ **decisa dal DM il 2026-09-23: For 18**, anche nella riga delle caratteristiche. Lotta +10 e attacco +12 la presupponevano già; il danno 1d8+5 torna |
| ~~D9~~ | `CONFORMITA-STATBLOCCHI` | `wyrmlord-karruk-cr10` | ✅ **decisa dal DM il 2026-09-23: tre stati, fuori ira, in ira, affaticato.** L'ira era la causa: caratteristiche, Volontà, squartare e roccia erano in ira, pf, CA e `pf-dado` fuori, e lotta, Tempra, attacco e danno non tornavano con nessuno dei due. Lo statblocco ora è fuori ira, con una tabella dei tre stati calcolati dal SRD. In più il BAB scende da +16 a **+14** (gigante 12 DV + Barbaro 5), come dicono i tre attacchi iterativi |
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

### La quinta voce — prima di **creare** un ADR o un piano

⚠️ **Le quattro sopra riguardano chi *chiude* un lotto. Questa riguarda chi
*apre* un documento**, ed è nata da un errore vero.

🐛 **`ADR-0049` è stato assegnato due volte in due giorni**: all'edizione
commerciale (PR #138) e poi al margine del bosco (PR #141), perché chi scriveva
il secondo non aveva guardato la cartella. Nessun controllo poteva vederlo —
nessun link era rotto e nessun ADR mancava dall'indice, che mostrava
semplicemente due righe con lo stesso numero.

**Il numero di un ADR è la sua identità**: si cita nei commit, nei piani, nel
codice e nei changelog. Due decisioni che lo condividono rendono ambigua ogni
citazione **all'indietro**, sui documenti già scritti.

```bash
python3 scripts/validate_docs.py --prossimo-adr   # PRIMA di scrivere l'ADR
```

Stampa l'ultimo numero sul disco e il primo libero, e **esce 1** se una
collisione esiste già. Il numero si conta da `plans/adr/`, non dall'indice:
quarta regola di ADR-0045, e in questo caso l'indice era proprio il documento
che non se n'era accorto.

**Per un piano nuovo** il numero non c'è, ma la regola è la stessa e ha già la
sua decisione: si legge `plans/INDEX.md` **prima** di aprirlo
([ADR-0044](adr/ADR-0044-prima-si-guardano-i-piani-che-ci-sono.md)).
Un piano duplicato non rompe le citazioni, ma divide il lavoro in due posti che
divergono — ed è già costato sei settimane con la PR #72.

⚠️ **Il limite, dichiarato**: `validate_docs --sorgenti` vede la collisione
**dopo** che il file esiste, quindi in CI arriva comunque; `--prossimo-adr` è la
metà preventiva, e funziona solo se la si esegue. È una regola con un cancello
in fondo, non un cancello all'ingresso.

⚠️ **Il resto di questo documento resta scritto a mano**, e resta una
fotografia: l'ordine delle fasi, le dipendenze, i costi. Il gate copre la
tabella delle decisioni, non il giudizio che c'è attorno.

---

## 6 · 🔁 Ripartire da qui — la tornata del 2026-09-20/21

> **A cosa serve questa sezione.** La tornata si chiude con dei lotti aperti, e
> il DM riprende **in un'altra conversazione**. Qui c'è tutto ciò che serve a
> ripartire senza rileggere niente: **ogni cosa da fare ha un comando che la
> rimisura**, perché un elenco che dipende dalla memoria di una chat non è un
> elenco, è un ricordo.

### 6.1 · Il primo comando da dare, sempre

```bash
python3 scripts/fase1.py <i file che stai per toccare>
```

È la **sesta regola d'oro** (`G6`, `AGENTS.md`): quattro passi in sola lettura
prima di qualunque modifica, `--check` esce 1 se stai per toccare un archivio.
L'ordine delle sei regole sta in [`skills/REGOLE-DORO.md`](../skills/REGOLE-DORO.md),
per momento del ciclo.

### 6.2 · Cosa resta, e il comando che lo rimisura

| | Lotto | Dove | Il comando che dice a che punto è |
|---|---|---|---|
| ✅ | **2C** — i box read-aloud che presuppongono un'azione del giocatore | [PIANO-QUATTRO-ORDINI](PIANO-QUATTRO-ORDINI-2026-09-20.md) §2C | *chiuso il 2026-09-21*: `misura_craft --p1` → **22 su 477**, e sono un **elenco nominale** (12 dialoghi · 6 falsi positivi · 2 visioni · 1 canto · 1 condizionale), ancorato file per file da `test_ogni_residuo_e_uno_dei_ventidue_dichiarati`. ⚠️ **Non si porta a zero**: il rilevatore dichiara di non distinguere il dialogo dalla narrazione <!-- attesa: 22 box su 477 --> |
| ⬜ | **M1-M3** — marcare gli incontri | [PIANO-MARCATURA-DEGLI-INCONTRI](PIANO-MARCATURA-DEGLI-INCONTRI.md) | `python3 scripts/validate_modules.py --tetto-el` → oggi **zero incontri marcati** |
| ✅ | **F1.1/F1.2/F1.3** — mappare le norme su severità | [PIANO-MISURA-EDITORIALE](PIANO-MISURA-EDITORIALE-STANDARD.md) | *chiuso il 2026-09-21*: `punteggio_mqm --norme` → **12 norme su 41** (la mattina erano **4 su 39**, e il «~40» era scritto a mano e sbagliato; poi F2.7-F2.9 hanno collegato i rilevatori che esistevano e registrato due norme mai elencate). <!-- attesa: 41 norme; qui ne entrano 12 --> La severità è una colonna del registro — **1 critico · 15 maggiori · 20 minori** — e `misura_craft --discriminante` dice che i congegni-rumore sono **zero su 23** <!-- attesa: 0 congegni su 23 --> |
| 🟡 | **F1.5 + F3.3** — i due campioni e il κ | idem | ✅ F1.5 chiuso; F3.3 **eseguito sul campione B: κ = 0,0** *(misurato 2026-09-21)*. La metrica si dichiara non affidabile e **non entra in CI**. Le manca una norma che morda, e la strada è la verifica aritmetica degli statblocchi, sbloccata dagli `attributi` (riga sotto) |
| ✅ | **Conformità meccanica degli statblocchi** — tutti i lotti chiusi: L1, L2, L2-bis, L3, L4, L5, L6, L6-ter, L7; restano solo **decisioni del DM** (§9) | [RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI](RICERCA-CONFORMITA-MECCANICA-STATBLOCCHI.md) §8-9 | `python3 scripts/conformita_statblocchi.py --check` → **ogni `pf-dado` registra i dadi vita** · `python3 scripts/conformita_statblocchi.py --riepilogo` → **101 tornano, 0 da correggere, 0 scarti del generatore, 0 decisioni aperte al DM** *(misurato 2026-09-23, dopo D1-D12)* <!-- attesa: da correggere 0 --> |
| ✅ | ~~i 27 ADR mancanti in `docs/INDEX.md` §4~~ | *nessun lotto: non c'era niente da fare* | `validate_docs --sorgenti` → **0** *(misurato 2026-09-21)*. 🐛 **I 27 non sono mai esistiti**: il buco più grande che `plans/adr/` abbia mai avuto è stato **uno**, il 2026-09-12, e da `14694c4` (16 settembre) l'indice è completo. Vedi §6.5 |

### 6.2-bis · 🐛 Quello che questa tabella ha sbagliato su se stessa

Delle cinque righe di §6.2, scritte il 20-21 settembre, **una era falsa nel
momento in cui è stata scritta** e una portava un numero già corretto da nove
giorni. Il conto, verificato eseguendo i comandi che le righe stesse citavano:

| Riga | Quel che diceva | Quel che dice il comando |
|---|---|---|
| **2C** | 104 box | ✅ **104** — esatta |
| **M1-M3** | zero incontri marcati | ✅ **zero** — esatta |
| **F1.1-F1.3** | «4 norme su **~40**» | 🟡 4 su **39**: il tilde copriva un numero mai contato |
| **F1.5 + F3.3** | bloccato sul DM | ✅ esatta |
| **i 27 ADR** | 27 mancanti | 🔴 **zero**, e non per poco: il buco più grande mai esistito è stato **uno** |

E la riga gemella in `PIANO-QUATTRO-ORDINI` §310 parlava di *«51 link rotti dei
booklet generati»*: erano **44**, sono stati chiusi il **12 settembre** dal
lotto E1 di `RIPRESA-PR`, che nello stesso documento li registra a **zero**.
Due rami dello stesso archivio dicevano due cose diverse sullo stesso fatto.

⚠️ **E il difetto non è dove sembra.** §6 nasce con un principio dichiarato —
*«ogni cosa da fare ha un comando che la rimisura, perché un elenco che dipende
dalla memoria di una chat non è un elenco, è un ricordo»* — e quel principio è
giusto. Ma **scrivere il comando accanto alla riga non è eseguirlo**: i 27 sono
stati scritti *citando* `validate_docs --sorgenti`, che in quel momento
stampava zero. Il gate esisteva, girava in CI, era verde, e la riga lo
contraddiceva.

**Cosa cambia, quindi.** Ogni riga di §6.2 porta da oggi la **data della
misura** fra parentesi. Non prova che il comando sia stato eseguito — niente lo
prova — ma rende visibile *quando* si dice che sia stato, e una data ferma da
due settimane accanto a un numero è la cosa che fa venire il dubbio. Un
cancello vero su questo è una proposta, non una decisione mia: è in **§6.4**.

---

### 6.3 · Le tre cose decise in questa tornata che NON vanno ridiscusse

1. **Il Rituale 4 è chiuso.** Decide la scheda che il giocatore ha letto: il
   *Manto di Pietra e Spirito* è del Rituale 3, l'*Aura della Forgia Eterna*
   del Rituale 4, e le tre fonti concordano sulla **CD 20**. L'innesco è la
   **vittoria**, non l'arrivo: `§4` non va ribilanciato.
2. **Fondere le skill peggiora.** Misurato: F1 da 0,744 a 0,728, richiamo sotto
   1,000. Non si rifà.
3. **La soglia del punteggio nasce dal repo.** I numeri vengono da
   `punteggio_mqm.py --distribuzione`, e si rimisurano con quel comando prima
   di cambiarli. Mai scriverne uno a memoria: è già successo, il 2026-09-21.

### 6.4 · Le decisioni aperte al DM, in ordine di costo

| | Decisione | Perché non la posso prendere io |
|---|---|---|
| 🔵 | **Aprire il piano di marcatura degli incontri?** | è lavoro su decine di file, e sblocca il primo critico vero del punteggio |
| ~~🔵~~ | ~~**I 104 box P1 si correggono tutti?**~~ | ✅ **eseguito il 2026-09-21**, e la risposta misurata è «82 sì, 22 no»: gli altri 22 sono dialogo, canto, visione, condizionale o falso positivo del rilevatore, e correggerli avrebbe **rotto dodici battute** per far scendere un numero. QUATTRO-ORDINI è **chiuso** |
| 🔵 | **Il campione A per il κ** | costa tempo al DM, e senza non si sa se la metrica concorda con lui |
| ~~🔵~~ | ~~**Un cancello sulle righe di §6.2?**~~ | ✅ **DECISO E ATTUATO dal DM il 2026-09-21, nello stesso giorno in cui è stato proposto.** → [ADR-0063](adr/ADR-0063-i-comandi-citati-si-eseguono.md): `verifica_sezione6.py --check` in CI, in un **job suo** perché esegue i comandi più lenti del repo. 🔒 I tre presidi sul rischio dichiarato — forma rigida (niente pipe, `;`, `&&`, `$()`), allowlist di script, `shell=False` — con **sette prove** che verificano *cosa si rifiuta di eseguire*. 🔎 **E al primo giro ha trovato tre cose**: la riga di F1.1-F1.3 era **già invecchiata di poche ore** (diceva «4 norme su 39», il repo era a 12 su 41), due righe citavano una misura senza dichiarare cosa si aspettassero, e il mio primo criterio dava un **falso positivo** su M1-M3 — `--tetto-el` stampa `✓` perché nessun incontro sfora, ma è verde **a vuoto**: un `⚠` non conta come pulito |
| 🔵 | **Un EL oltre il tetto si ribilancia o si dichiara?** | è una decisione di difficoltà, e oggi non si sa nemmeno quanti siano |
