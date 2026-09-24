# PIANO — LEVEL DESIGN DELLE MAPPE E INQUADRATURA SCENICA

> 📦 **Recuperato il 2026-09-24 dalla PR #72** (mai mergiata; file del commit
> `0448956` e seguenti, fino a `960c621`), per la decisione D22 di
> `PIANO-RIPRESA-PR-ABBANDONATE`. ADR-0048 lo nominava come fonte del proprio
> lotto A1, e il file non c'era.
>
> **Stato oggi**: 🔵 **pianificato**, rami C e D. Rimisurati il 2026-09-24:
>
> | Lotto | Oggi | Cosa cambia |
> |---|---|---|
> | Rami 0, A, B | delegati a `PIANO-PRODOTTO-TOOLKIT-VENDIBILE`, che a sua volta è stato assorbito da [PIANO-VENDIBILITA](PIANO-VENDIBILITA.md) (§6). A1, la legenda come dato, è fatto (ADR-0048, 2026-09-12) | niente: restano fuori da qui |
> | §2-bis, le dipendenze Python a livelli | **superato**: ADR-0037 ha deciso la sola libreria standard, e l'ADR-0015 della #72 non è stato recuperato | non si applica |
> | C1 scheda-mappa | non esiste; c'è solo `mappa-tattica-template.md` | valido |
> | C2 le tre mappe peggiori | il Dirupo Mortale e l'Ondata 2 esistono; le metriche M1-M9 chiedono il linter di B1, che non c'è | valido, **dipende dal linter** di PIANO-VENDIBILITA |
> | C3 parity pass | — | valido |
> | D1 scheda-inquadratura | la skill `rumblingstone-art-direction` ha un **brief d'inquadratura** (§5: cosa c'è e perché), ma nessun prompt dichiara focale, altezza di camera o figura di scala | valido, **dentro la skill** e non come template a parte |
> | D2 ordine percettivo nel read-aloud | 0 occorrenze nelle skill | valido; è una norma nuova, quindi va registrata (G3) |
> | D3 modalità 4, blockout 3D | non c'è `scripts/blockout/`; c'è `render_map_blender.py`, che estrude la pianta e la riprende in ortografica (per le mappe, non per le illustrazioni) | valido; la pipeline Blender esistente è la base <!-- validate-docs: ignore --> |
> | D4 igiene IP dei prompt | 10 riferimenti a film e marchi in 7 file di `campaign/ai-media-prompts/` | valido; ricade anche nel gate d'uscita di `rumblingstone-edizione` |
>
> I link agli ADR della #72 portano ai numeri di oggi; quelli a file mai
> arrivati portano all'ultimo commit della PR su GitHub.

> **Origine**: guida operativa **«Dall'immagine mentale all'artefatto»**
> (2026-07-25, fornita dal DM) — Parte I §0-§10 (composizione visiva) e
> Parte II §L1-§L9 (level design e codifica nel toolkit).
> **Misura dello scarto**: [`docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md`](../docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md)
> — ogni lotto qui sotto rimedia a un buco misurato lì, mai a un'impressione.
> **Decisioni architetturali portanti**:
> [ADR-0014, oggi ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md) · [ADR-0015, rifiutato](https://github.com/gsamuele78/RumblingStone/blob/960c62185bb24e82da0de251228bbbd027c3d5a9/plans/adr/ADR-0015-dipendenze-a-livelli-e-pacchettizzazione.md)
> · [ADR-0016, oggi ADR-0039](adr/ADR-0039-profili-regole-multisistema.md) · [ADR-0017, oggi ADR-0040](adr/ADR-0040-separazione-prodotto-e-toolkit-estraibile.md)
> — **tutte accettate** (decisioni DM 2026-07-26).
> **Stato**: 🔵 pianificato · **Data**: 2026-07-26 · **% completamento**: 0%
> **Rev. 2** (2026-07-26): aggiunti §0-bis (architettura bersaglio) e §2-bis
> (integrare invece di riscrivere) + **Ramo 0** su richiesta DM.
> **Rev. 3 — CONSOLIDAMENTO** (2026-07-26): i rami **0, A, B sono delegati** a
> [`PIANO-PRODOTTO-TOOLKIT-VENDIBILE`](https://github.com/gsamuele78/RumblingStone/blob/960c62185bb24e82da0de251228bbbd027c3d5a9/plans/PIANO-PRODOTTO-TOOLKIT-VENDIBILE.md)
> (fasi P0/P1/P2) — erano 12 lotti con due proprietari. **Un solo proprietario
> per lotto**: qui resta il contenuto (rami C e D).

---

## 0. Il problema, in una riga

Il toolkit ha una pipeline di **produzione** matura (40 tool a contratto, CI
deterministica, 3 modalità mappa) e **nessuna pipeline di progettazione**: sa
disegnare qualunque cosa gli si dica, e non ha modo di dire se ciò che gli si
è detto di disegnare fosse una buona mappa o una buona inquadratura.

Le due conseguenze misurate:

- **mappe** — su 29 griglie ≥12×12: mediana M1 = 0.30 (soglia ≥0.60),
  M2 = 0.51 (≤0.20), M4 = 0.84 (≤0.45), M8 = 0 (≥3); **15/15** delle mappe con
  token PG+nemico fuori dalla banda 2-4 round. Gli interni passano, **tutti**
  gli esterni falliscono;
- **immagini** — su 48 blocchi prompt: **0** dichiarano focale, altezza camera,
  figura di scala o prospettiva atmosferica.

E un difetto strutturale che vale da solo il primo lotto: **l'SVG e l'export
UVTT della stessa mappa non concordano su cosa sia un muro** (`⛰` occlude
nell'SVG e non blocca la vista in Foundry; `🏛 🗼 🗿` il contrario).

## 0-bis. L'architettura bersaglio: due prodotti, non uno

*(sezione aggiunta nella rev. 2, in risposta alla domanda DM «qual è il percorso
corretto per un prodotto professionale e riusabile?»)*

**La domanda giusta non è «come aggiungo il level design al toolkit», ma «cosa
sta diventando questo repo».** Oggi contiene due prodotti con vincoli opposti,
fusi in un solo albero:

| | **Prodotto A — la campagna** | **Prodotto B — il toolkit** |
|---|---|---|
| Cos'è | archi 00-09, Bestiario, PG, canone, mappe | `scripts/`, schemi, legenda, pipeline |
| Distribuibile? | **no** — IP RHoD/WotC (ADR-0005) | **sì** — nessun asset di terzi, arte procedurale in-house |
| Vive di | sessioni giocate | release e utenti |
| Criterio di qualità | coerenza di canone | contratti stabili, retrocompatibilità |
| Chi lo cambia | il DM | chi manutiene il codice |

**Non sono separati oggi**: 11 script fanno `sys.path.insert(0, …)` per
importarsi a vicenda, e quattro moduli importano `render_map_svg` — un modulo di
**rendering** da 1.530 righe — per ottenere il **parser** e la **legenda**. La
dipendenza punta nella direzione sbagliata: il dominio dipende dalla
presentazione.

**Il percorso a un prodotto professionale e riusabile è rendere B estraibile**,
non riscriverlo. In ordine, e ogni passo ha valore anche se ci si ferma lì:

1. **Il toolkit diventa un package** (`pyproject.toml`, entrypoint da console).
   Fine dei `sys.path` hack. È il prerequisito di qualunque riuso — e di
   `PIANO-EDITOR-VISUALE-MAPPE`, che pianifica già l'editor come progetto separato
   ma oggi non avrebbe nulla da importare.
2. **Il dominio si separa dalla presentazione**: legenda, parser della griglia e
   modello della mappa in un modulo di dominio; renderer, exporter e CLI ne
   **dipendono**, non viceversa. È esattamente la stessa correzione che ADR-0014
   fa per la legenda, generalizzata — e la fa una volta sola.
3. **La campagna diventa un consumatore del toolkit**, non il suo contenitore.
   `campaign/` e gli archi restano dove sono e non cambiano nulla nel modo in cui
   il DM lavora.

Quello che **non** serve: spezzare il repo in due adesso. La decisione «repo unico
con package interno, o due repo» va presa quando B ha una superficie pubblica
stabile — cioè dopo il Ramo 0, non prima.

## 1. Obiettivo e non-obiettivi

**Obiettivo**: portare nel toolkit, come **dato e come gate**, la disciplina di
level design (affordance misurabili, intento dichiarato e verificato) e quella
di inquadratura (blockout geometrico prima della generazione, ordine percettivo
nella prosa).

**Non-obiettivi dichiarati** — per non far crescere il piano oltre il suo scopo:

- ❌ non si riprogettano tutte le mappe del repo (solo le 3 di §C2; il resto è
  gated dal tavolo);
- ❌ il linter **non è bloccante**, mai: apre una domanda, non chiude una porta
  (una mappa può violare ogni soglia ed essere ottima — un ponte stretto sopra
  il vuoto viola M1, M2, M3 e M4 *di proposito*);
- ❌ non si costruisce l'editor visuale (piano separato);
- ❌ non si punta a un prodotto commerciale: i confini restano ADR-0005.

## 2. Principi vincolanti

1. **Il dato prima dello strumento.** Nessuna metrica viene implementata prima
   che la sua informazione esista come dato interrogabile (A prima di B).
2. **Advisory, non bloccante** — come già `validate_bestiario --rules`.
3. **Soglie euristiche finché non calibrate** (§L5.4): prima della
   calibrazione sono un'opinione informata, e vanno dichiarate come tali nei
   messaggi del tool.
4. **Nessuna regressione visiva**: i 17 SVG legacy restano byte-identici
   (`validate_maps.py`) attraverso ogni refactor.
5. **Ogni tool nuovo è ADR-0012-conforme**: manifest, exit code, determinismo
   dichiarato, `--help` senza side-effect, test, smoke in CI.
6. **La calibrazione non usa mappe RHoD** (ADR-0005): solo materiale proprio o
   liberamente licenziato, con corpus dichiarato.

## 2-bis. Integrare invece di riscrivere

*(sezione aggiunta nella rev. 2 — regola DM: «se esiste già ed è usabile, si
integra»)*

La rev. 1 di questo piano proponeva di **scrivere a mano** componenti connesse,
dilatazione binaria, grafi con punti di articolazione e raycast. Sbagliato.
Misurato sulla mappa *Dirupo Mortale* 40×40, con i valori confrontati al bit
contro l'implementazione a mano:

| Serve per | Rev. 1 (a mano) | Rev. 2 (integrato) | Esito misurato |
|---|---|---|---|
| **M1** copertura entro Chebyshev 2 | doppio ciclo su 25 offset | `scipy.ndimage.binary_dilation`, struttura 5×5 | identico (0.0309), **1 riga** |
| **M2** vuoto connesso massimo | BFS + deque, ~15 righe | `ndimage.label` + `bincount` | identico (0.9691), **2 righe** |
| M1+M2 insieme | 18 righe · 11,5 ms | 4 righe · **0,8 ms** | **14×**, ¼ del codice |
| **M3** anelli μ = E−V+C | costruzione grafo + conteggio | `networkx`, 1 riga | — |
| **strozzature** | algoritmo dei punti di articolazione | `nx.articulation_points`, 1 riga | — |
| **M4/M5** visibilità | Bresenham a mano, e la guida **ripiega sul campionamento** perché «in Python puro sono minuti» | `tcod.map.compute_fov`, shadowcasting **simmetrico** | censimento **completo** 1.585 celle in **34 ms** |
| **struttura** dei JSON | validatori a mano (già due nel repo) | `jsonschema` sugli schemi draft-07 **già presenti** | valida 3/4 esempi così com'è ¹ |

¹ il quarto (`esempio-misure-in-metri.json`) fallisce **correttamente**: usa
`units_in: meters`, che lo schema stesso documenta come da validare dopo la
conversione, non prima.

**Tre conseguenze che cambiano il piano, non solo il codice:**

1. **Il campionamento di M4 non serve più.** La mitigazione di §L5.3 della guida
   («campiona, oppure usa numpy») nasce da un vincolo che sparisce integrando: M4
   diventa **esatta**, quindi difendibile. E il campionamento **sottostimava** —
   esatta 0.913 contro 0.88 stimata sulla stessa mappa.
2. **Serve una politica di dipendenze prima del codice** → [ADR-0015, rifiutato](https://github.com/gsamuele78/RumblingStone/blob/960c62185bb24e82da0de251228bbbd027c3d5a9/plans/adr/ADR-0015-dipendenze-a-livelli-e-pacchettizzazione.md):
   il core resta **stdlib puro** (il DM deve poter lanciare `dm.py` su una macchina
   nuda, offline, la sera del gioco); l'analisi va in un **extra opzionale**. Il
   linter è uno strumento di preparazione, non di sessione: è il posto giusto per
   una dipendenza.
3. **Dove invece NON esiste nulla da integrare, e va scritto**: il *linter di
   design per battlemap* non esiste sul mercato (§L8 della guida). Il valore
   originale del progetto è lì — nella **traduzione dominio-specifica** (legenda
   funzionale, intento dichiarato, soglie calibrate), non negli algoritmi sotto.
   Ogni ora spesa a riscrivere `binary_dilation` è un'ora tolta a quella.

**Cosa si integra nel resto del piano**: ComfyUI (già nel repo) invece di una
pipeline di generazione propria; Blender headless invece di un renderer; il
formato **Universal VTT** (già esportato) invece di un formato proprio; Watabou
e l'import ultra-clear (già presenti) invece di nuovi generatori. Su questi il
repo aveva già fatto la scelta giusta.

---

## 3. Lotti

Legenda impegno: **engine consigliato** e **livello** secondo la regola DM
2026-07-22 (piani con routing engine).

### Rami 0, A, B — **DELEGATI** al piano prodotto (consolidamento 2026-07-26)

> ⚠️ **Questi rami non vivono più qui.** Erano duplicati con le fasi P0/P1/P2 di
> [`PIANO-PRODOTTO-TOOLKIT-VENDIBILE`](https://github.com/gsamuele78/RumblingStone/blob/960c62185bb24e82da0de251228bbbd027c3d5a9/plans/PIANO-PRODOTTO-TOOLKIT-VENDIBILE.md): 12
> lotti con due proprietari. Due piani che rivendicano lo stesso lavoro rendono
> impossibile tracciare l'avanzamento — che è esattamente ciò che un piano
> eseguibile a fasi deve garantire.
>
> **Un solo proprietario per lotto.** L'infrastruttura sta nel piano prodotto;
> qui resta il **contenuto**.

| Era qui | Ora è | Cosa fa |
|---|---|---|
| 0.1 · 0.2 · 0.3 · 0.4 | **P0.1 · P0.2 · P0.3 · P0.4** (+ i nuovi **P0.0** rete di sicurezza e **P0.5** fetta verticale) | substrato: package, dipendenze, lint/test, confine dominio/presentazione |
| A1 | **P1.1** | `legend.yaml`, 62 simboli, le 4 correzioni `⛰ 🏛 🗼 🗿` |
| A2 · A3 | **P1.3** | zone, elevazione, `design_intent`, `map_kind` |
| B1 · B2 · B3 · B5 | **P2.1 · P2.2 · P2.3 · P2.4** | il linter (+ il nuovo **P2.0**, contratto unico dei finding) |
| B4 | **P2.0 + P5.1** | integrazione CI, manifest, gate |

**Questo piano resta proprietario di**: i lotti **C** (mappe) e **D**
(inquadratura e prosa) — cioè il contenuto, che il piano prodotto non tocca.
Il lotto **D1** (scheda-inquadratura) alimenta i check `framing/*` di **P2.6**;
il lotto **D4** (igiene IP) alimenta `framing/ip-reference`.

---

### Ramo C — Il debito di contenuto (le mappe)

#### ⬜ C1 — `campaign/templates/scheda-mappa-template.md` <!-- validate-docs: futuro -->

*Realizza*: §L6. **Si compila prima di disegnare**, ed è il gemello della
scheda-inquadratura (D1). Contiene: intento (la domanda che i giocatori devono
porsi · come si vince, mai «uccidere tutti» · come si perde, mai TPK gratuito),
i cinque elementi di Lynch (path/edge/district/node/landmark), i sei parametri
(anelli, copertura, linee di vista, verticalità, strozzature, distanza
d'ingaggio), l'ambiente dinamico, i target del linter e le **deroghe motivate**.

Il template esistente `mappa-tattica-template.md` resta e non si tocca: norma
la **resa** (Ambiente/Tattiche/Evoluzione); la scheda-mappa norma il
**progetto**. Il puntatore reciproco va scritto in entrambi.

**Accettazione**: template committato, referenziato dalla skill mapmaking, e
compilato su **una** mappa reale come esempio vivo.
**Engine**: Opus (è design). **Impegno**: medio. **Stima**: 4-6 h.
**Indipendente da A/B** — candidabile per primo.

#### ⬜ C2 — Riprogettazione delle 3 mappe peggiori

Dalla classifica di audit §3.2, in ordine di urgenza al tavolo:

1. **Dirupo Mortale / Campo Hobgoblin** (ARC-08, 40×40) — M1 0.03 · M2 0.97 ·
   M4 0.88 · M8 0 · M9 1.5. Riprogettazione secondo §L7: 3-4 coperture nel
   terzo centrale, 3 landmark asimmetrici nominabili (l'albero fulminato, il
   carro bruciato, il masso spaccato), 3 bande di elevazione (canalone −2 m ·
   campo 0 · costone +3 m), un secondo accesso che chiuda un anello, una
   linea di vista bloccata che divida il campo, e un **orologio** (il fuoco di
   segnalazione entro il round 6 → sconfitta = incontro successivo +1 GS, non
   TPK);
2. **Ondata 2 Positions** (26×26) — M1 0.00, M2 1.00;
3. **Ground Battle** (30×71) — da valutare: se è una vista strategica va
   marcata `map_kind: strategic` (A3) invece che riprogettata.

**Non aggiungere decorazioni: aggiungere compromessi.** Il criterio non è «più
bella» ma «ogni posizione comporta un guadagno e una perdita».

**Accettazione**: per ciascuna, scheda-mappa compilata **prima**; dopo la
riprogettazione M1 ≥ 0.60, M2 ≤ 0.20, M8 ≥ 3, M9 ∈ [2,4], o deroga scritta e
motivata; SVG rigenerato; companion Ambiente/Tattiche/Evoluzione aggiornati.
**Engine**: Opus (design) → Sonnet (griglia). **Impegno**: alto.
**Stima**: 6-8 h a mappa. **Dipende da**: C1, B1. **Gate**: prova al tavolo.

#### ⬜ C3 — Parity pass sul resto del corpus

Le ~26 griglie restanti, una alla volta, su decisione DM. Le mappe che il
linter promuove già (le caverne: *Cuore della Montagna* M1 1.00 · M2 0.00,
*Stanza della Corona* M1 0.88) **non si toccano**.

**Engine**: Sonnet. **Impegno**: medio. **Gate**: tavolo, a mappa singola.

---

### Ramo D — Inquadratura e prosa (indipendente da A/B/C)

#### ⬜ D1 — Scheda-inquadratura e campo `## Inquadratura`

*Realizza*: §2 e §3.6. Aggiungere a `campaign/ai-media-prompts/` il blocco
strutturato — formato, focale, altezza e inclinazione camera, **momento**
(l'istante esatto, non il luogo), primo piano / piano medio / sfondo, struttura
dei valori, **figura di scala**, elemento vivo, atmosfera, **ancora non
visiva** (che serve al read-aloud, non all'immagine).

Riscrittura dei prompt nella struttura in cinque blocchi
(`soggetto e momento · inquadratura · luce e valore · atmosfera · medium`), a
sostituzione di `[STILE] [SCENA] [CAMERA] [PALETTE]` che ordina per categoria
di metadato invece che per costruzione dell'immagine.

**Retrofit**: non tutti i 48 blocchi. Le **3 scene chiave di ARC-07** come
pilota, poi si valuta.

**Accettazione**: template nel repo; 3 schede compilate; ogni scheda dichiara
focale, altezza camera e figura di scala (oggi: 0/48).
**Engine**: Opus (le schede sono design) → Sonnet (retrofit).
**Impegno**: medio. **Stima**: 6-8 h.

#### ⬜ D2 — Regola d'ordine percettivo nel read-aloud ⭐

*Realizza*: §6. **È l'item a ritorno più alto dell'intero piano**: nessuna GPU,
nessun Blender, nessun codice — e agisce su ciò che il repo produce di più.

In `skills/rumblingstone-narrative-style/references/editorial-standards.md` §2
(che oggi norma texture e tipografia, mai l'ordine di rivelazione — audit §4.3)
aggiungere le tre regole:

1. descrivere nell'**ordine in cui la percezione arriva**:
   non-visivo → primo piano → piano medio → sfondo;
2. dare la scala per **rapporto prima che per numero** («le spalle a metà della
   volta», *poi* «e la volta è a diciotto metri»);
3. inquadrare **un momento**, non un luogo — e chiudere su qualcosa che si
   muove, restituendo il turno ai giocatori.

Con l'esempio prima/dopo della Forgia Adamantina come riferimento canonico.

**Accettazione**: regola nella skill; `build-skills.sh --no-deploy` e
`validate_skills.py` verdi; **un** read-aloud esistente riscritto secondo la
regola e provato al tavolo.
**Engine**: Opus. **Impegno**: medio. **Stima**: 4-5 h. **Gate accettazione
finale**: prova al tavolo.

#### ⬜ D3 — Modalità 4: blockout 3D → depth → illustrazione

*Realizza*: §3, §5. La quarta modalità mancante — l'unica che parte
dall'immagine mentale invece che da un artefatto 2D esistente, e l'unica con
provenienza al 100% originale (rilevante sotto ADR-0005).

```
scripts/blockout/
├─ render_blockout.py     # Blender headless: clay + depth normalizzata
├─ README.md              # contratto I/O secondo ADR-0012
└─ scenes/                # .blend, gitignorati (binari pesanti)
rendered/blockout/        # gitignorata: output non deterministico, non canone
skills/rumblingstone-mapmaking/references/blockout-3d-illustrazione.md
```

Punti critici da non sbagliare: `--near`/`--far` (se sbagliati la depth esce
piatta e il ControlNet non vincola niente — deve essere un **gradiente pieno**,
vicino = bianco); `CompositorNodeOutputFile` aggiunge il numero di frame al
nome (`_depth0001.png`), va gestito a valle; ControlNet **Union** consigliato
sulle 8 GB di VRAM (un file solo invece di tre); `end_percent` **0.80**, non
1.0, altrimenti l'immagine esce plasticosa.

Aggiornare `scripts/comfyui-local/README.md` (oggi cita solo lineart/canny) e
`references/tre-modalita-mappe.md` (oggi dichiara 3 modalità).

**Accettazione**: il test di §4 eseguito end-to-end su una scena
(`--focal 24 --near 2 --far 45`), con il criterio dichiarato dalla guida —
**«le masse principali stanno dove le hai messe nel blockout»**, non «l'immagine
è bella»; depth PNG con gradiente pieno verificato a occhio; `rendered/blockout/`
fuori da `validate_maps.py`; script a manifest se committato.
**Engine**: Sonnet (script) — il collaudo è **al DM, sulla sua macchina**.
**Impegno**: medio. **Stima**: 8-10 h + collaudo.
**Gate**: GPU e Blender sulla macchina del DM. ⚠️ I nomi dei modelli ControlNet
cambiano rapidamente: verificare licenza e nome **al momento del download**.

#### ⬜ D4 — Igiene IP dei prompt versionati

*Rimedia*: audit §4.4. I prompt contengono riferimenti in chiaro a IP protette
(«visual style of Doctor Strange», «Lord of the Rings dwarven aesthetics»,
«Thor: Ragnarok»). Coperto da ADR-0005 per uso privato, ma sono file
**versionati e pubblici**, ed è precisamente ciò che va rimosso da qualunque
edizione distribuita.

Sostituire con linguaggio **descrittivo** (ciò che si vuole vedere, non da
quale film), aggiungere la policy in ADR-0005 e una riga di promemoria nella
testata di `00_INDICE-PROMPT-MEDIA-CAMPAGNA.md`. Documentare che ogni immagine
così prodotta va etichettata `Contains AI-Generated Content` sulle piattaforme
di distribuzione.

**Accettazione**: nessun titolo di film/IP protetta resta nei prompt;
il senso visivo dei prompt bonificati è preservato (verifica a occhio del DM).
**Engine**: Sonnet. **Impegno**: basso. **Stima**: 3-4 h.

---

## 4. Sequenza consigliata

L'ordine **non** è quello dei lotti. La guida stessa avverte: *leggere prima di
aver misurato lo scarto significa studiare a caso.* Lo scarto è misurato
(audit); la sequenza segue il ritorno.

| # | Lotto | Perché qui |
|---|---|---|
| 1 | **D2** — ordine percettivo | ~4 h, zero dipendenze, zero codice; agisce su ciò che il repo produce di più |
| 2 | **C1** — scheda-mappa | indipendente; serve a C2 e insegna la disciplina **prima** di avere il tool |
| — | *(infrastruttura: fasi **P0 → P1 → P2** del piano prodotto)* | delegata, vedi §Rami delegati |
| 3 | **C2** (Dirupo Mortale) | la prima mappa che il linter ripaga — dopo P2.1 |
| 4 | **D1 + D4** | scheda-inquadratura e igiene IP: alimentano i check `framing/*` di P2.6 |
| 5 | **D3** | Modalità 4 — gated dalla macchina del DM |
| 6 | **C3** | parity pass, a mappa singola, sulla lunga |

**Totale stimato di questo piano dopo il consolidamento**: ~50-70 h (soli rami C e D). L'infrastruttura è contabilizzata nel piano prodotto.

*(Nota storica, rev. 2)*: ~110-145 h — il Ramo 0 aggiungeva 25-35 h, l'integrazione ne
toglie ~10 dai rami B. Il saldo è positivo perché il Ramo 0 **si paga una volta e
serve ogni piano successivo**, incluso l'editor visuale.

**Ordine di valore, indipendente dal totale**: i primi due lotti (~10 h, zero
codice nuovo) danno la maggior parte del valore percepito al tavolo; i lotti 3-4
(~25 h) danno tutto il valore *strutturale* — dopo di essi il toolkit è
installabile, il dominio è separato e la divergenza SVG↔UVTT è chiusa, anche se
il linter non venisse mai scritto.

## 5. Rischi dichiarati

| Rischio | Mitigazione |
|---|---|
| A1 rompe i render legacy | `validate_maps.py` esige byte-identità: il gate è già lì, va solo tenuto verde |
| Le 4 decisioni sui simboli divergenti (`⛰ 🏛 🗼 🗿`) sono di **regole**, non di codice | vanno al DM, non risolte dall'agente; documentate nel changelog |
| Il linter genera rumore e viene ignorato | A3 (`map_kind`) **prima** di B1; advisory sempre; messaggi che dichiarano di essere pre-calibrazione |
| Le soglie restano opinione | B5 con corpus dichiarato e licenze verificate, o le soglie restano marcate «euristiche» per sempre — mai spacciate per misura |
| D3 dipende da hardware e da modelli che cambiano nome | collaudo sulla macchina del DM; nomi ControlNet verificati al download; `rendered/blockout/` fuori dal canone |
| Il piano cresce e non chiude mai | i non-obiettivi di §1 sono vincolanti; C3 è esplicitamente a mappa singola e gated |
| **Il Ramo 0 rompe qualcosa che oggi funziona** (11 file di import, un modulo da 1.530 righe) | la rete esiste già ed è forte: 70 test + byte-identità degli SVG + round-trip UVTT in CI. Il layout `scripts/*.py` **resta invocabile identico**: se l'installazione fallisce, il DM non se ne accorge |
| **Le dipendenze del livello 1 non sono disponibili la sera del gioco** | per questo sono **opzionali e fuori dal percorso di sessione** (ADR-0015): il linter è uno strumento di preparazione. Il core resta stdlib puro e offline |
| Il substrato (Ramo 0) rimanda il valore visibile | per questo la sequenza di §4 mette **D2 e C1 prima**: ~10 h a valore immediato e zero codice, e il substrato parte con il beneficio già incassato |

## 6. Cosa questo piano NON risolve

Onestà, in coerenza con §L8 della guida:

- **il linter non misura il divertimento**, misura le affordance. Una mappa può
  passare ogni soglia ed essere noiosa;
- **vale per lo spazio di combattimento**, non per esplorazione, investigazione
  o scene sociali;
- **la scala resta il punto debole dei modelli generativi**: anche con la figura
  di scala, sbagliano spesso. Preventivare più iterazioni sulle scene
  monumentali;
- **coerenza fra immagini diverse: bassa.** Lo stesso luogo in due immagini non
  sarà lo stesso luogo;
- **il ControlNet depth vincola le masse, non il dettaglio.**

---

## Checklist di avanzamento

```
Rami 0, A, B → DELEGATI al PIANO-PRODOTTO (fasi P0/P1/P2)

Ramo C — contenuto mappe
□ C1  scheda-mappa-template.md
□ C2  riprogettazione Dirupo Mortale · Ondata 2 · (Ground Battle → map_kind?)
□ C3  parity pass — a mappa singola, gated dal tavolo

Ramo D — inquadratura e prosa
□ D2  ⭐ ordine percettivo nel read-aloud (narrative-style)
□ D1  scheda-inquadratura + campo ## Inquadratura (pilota: 3 scene ARC-07)
□ D4  igiene IP dei prompt versionati
□ D3  Modalità 4 — blockout 3D → depth → ControlNet (gated: GPU DM)
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna — nello stesso
> commit — questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
