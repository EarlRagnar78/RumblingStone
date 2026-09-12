# PIANO — Vendibilità: il piano unico

> **Stato**: 🔵 **proposta, non autorizzata** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«fai 1 unico piano per la vendibilità
> […] riconcilia in modo da far avanzare 1 piano»*.

## Cosa sostituisce, e perché esisteva sparso

Cinque documenti dicevano cose sovrapposte, scritti in due momenti diversi da chi
non aveva letto l'altro. Questo li sostituisce **tutti**.

| Sostituito | Dove stava | Cosa se ne salva qui |
|---|---|---|
| `PIANO-PRODOTTO-TOOLKIT-VENDIBILE` (803 righe) | PR #72, 26 lug | i lotti P0-P5, il modello di verifica unico, la matrice dei check — §6 |
| `PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE` | PR #72 | l'AP originale come prodotto — §5 linea 4 |
| `PIANO-AUDIT-PROVENIENZA-E-VENDIBILITA` | main, 4 set | il verdetto sull'AP, i tre metri di qualità — §2, §4 |
| `PIANO-PROPOSTA-COMMERCIALE-E-SFIDE` | main, 4 set | il MIT, la misura degli strumenti, le sfide — §3, §5, §7 |
| `PIANO-ROADMAP-COMMERCIALE` | main, 4 set | la sequenza — §6 |

⚠️ **Come è potuto succedere, perché non si ripeta.** La PR #72 era aperta da
sei settimane come bozza e conteneva già le decisioni del DM del 26 luglio. A
settembre è stato riscritto quasi tutto da capo senza guardarla. La regola che ne
segue è in §8.4.

**Decisioni del DM già prese e non revocate**: rilicenziare il toolkit ·
supportare **3.5 + PF1e + 5e** · distribuire come **wheel + eseguibile
autonomo** · vendere **toolkit + map pack neutri + il metodo** (26 lug) ·
restare su 3.5/PF1e per il *contenuto* e mettere il cancello di qualità prima di
quello di mercato (4 set).

**ADR di riferimento**: [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md)
· [ADR-0029](adr/ADR-0029-licenza-doppia-testo-e-script.md)
· [ADR-0039](adr/ADR-0039-profili-regole-multisistema.md) *(era 0016 nella #72)*
· [ADR-0040](adr/ADR-0040-separazione-prodotto-e-toolkit-estraibile.md) *(era 0017)*

> ⚠️ Ingegneria e prodotto, **non parere legale**. Una vendita reale vuole un
> avvocato IP: rilicenziamento, Sezione 15 OGL, attribuzione CC BY, e i marchi
> «D&D» e «Pathfinder» fuori da nome e marketing. Non autocertificabile.

---

## §1 · I due corpi, che hanno vincoli opposti

ADR-0005 dice che il repo non è commercializzabile, e resta vero — **per il
contenuto**. Ma il repo contiene due cose che ADR-0005 trattava come una
(ADR-0040):

| | **A — la campagna** | **B — il toolkit** |
|---|---|---|
| Cosa | archi 00-09, Bestiario, PG, canone | `scripts/`, schemi, legenda, renderer |
| Blocco | RHoD + Forgotten Realms (WotC) | **nessun blocco IP** |
| Vendibile | no, come adattamento | **sì** |

**Il toolkit non ha mai avuto un blocco di IP: ha un blocco strutturale.** Non è
estraibile, e questo si misura.

---

## §2 · Il contenuto: il verdetto, e la rotta che resta

**L'AP adattato da Red Hand of Doom non è vendibile.** RHoD non è mai stato Open
Game Content — WotC ha rilasciato l'SRD, non i moduli — e un adattamento è opera
derivata. Tre cose che si sbagliano spesso: **l'OGL non è l'ostacolo** (permette
il commerciale da venticinque anni); le tavole sono il 5% del problema e la trama
il 95%; e ADR-0005 lo diceva già, ma sull'*uso del repo*, non sul *prodotto*.

**Ma il copyright protegge l'espressione, non le idee.** Un'orda con patronato
draconico che invade una regione di frontiera è genere, non espressione — e nel
racconto del DM (4 set) Hammerfist viene dal Fosso di Helm, Rethmar dalla
battaglia di Gondor, e la quest della Corona, l'Underdark e i poteri miceliali di
Hella sono inventati. Se regge alla verifica, la parentela è sottile.

**La rotta**: la **camera bianca**. Una pagina con la sola premessa in forma di
idea, e da lì si costruisce, senza riaprire né RHoD né i file esistenti. Poi il
**test del lettore**: darlo a chi ha condotto RHoD e sentire se dice «stesso
genere» o «coi nomi cambiati».

⚠️ **La dipendenza vera non è RHoD: è il bestiario non-SRD.** Misurato:

| | File | | | File |
|---|---:|---|---|---:|
| illithid | 86 | | Circolo degli Otto | 31 |
| githyanki | 58 | | mind flayer | 22 |
| beholder | 10 | | maur · yuan-ti · umber hulk | 13 |

Liberi perché SRD: rakshasa, treant, drow, retriever, basilisco, Moradin. La
concentrazione è nell'**arco 09**, cioè quello inventato da zero: l'invenzione è
stata nella trama, il popolamento è stato pescato dal bestiario chiuso. È più
pesante del previsto e **più economico da chiudere**, perché un mostro si
sostituisce e una trama si riscrive.

---

## §3 · La licenza: tre regimi, e la soluzione è architetturale

**Il MIT non blocca.** Una licenza vincola chi la riceve, non chi la concede: si
può vendere, fare doppia licenza, cambiare per il futuro, costruirci sopra un
proprietario. L'unica cosa impossibile è ritirarlo da ciò che è già uscito. Il
MIT **non blocca e non protegge**, e qui non protegge il codice: proteggono il
contenuto, il servizio, l'aggiornamento e il nome. La forma è **open core**.

| Sistema | Regime | Commerciale |
|---|---|---|
| **D&D 5e** — SRD 5.1 / 5.2 | **CC BY 4.0** | ✅ solo attribuzione |
| D&D 3.5 · PF1e | OGL 1.0a | ✅ licenza integrale + Sezione 15 |
| PF2e Remaster | ORC | ✅ |
| RHoD, FR non-SRD | chiuso | ❌ |

⚠️ **E la soluzione al problema di mescolarli non è «un prodotto, un regime»: è
ADR-0039.** Il motore non conosce nessun sistema; i numeri di gioco vivono in
profili sostituibili — `rules/dnd35.yaml` e `rules/pf1e.yaml` sotto OGL,
`rules/dnd5e.yaml` sotto CC BY. **L'OGL tocca due file, non il prodotto.** È una
risposta migliore, ed era già scritta a luglio.

---

## §4 · Il punto di partenza, misurato

**La struttura** (ADR-0040, rimisurata il 4 settembre):

| Fatto | Luglio | **Oggi** |
|---|---:|---:|
| script con `sys.path.insert` | 11 | **24** |
| `pyproject.toml` | assente | **assente** |
| `render_map_svg.py` | 1.530 righe | 1.538, importato da 4 moduli per il *parser* |

⚠️ Il debito è **più che raddoppiato** mentre il piano che lo descriveva restava
in una bozza.

**La qualità** — tre metri, tutti già costruiti, mai letti insieme:

| Asse | Metro | Lettura |
|---|---|---|
| contenuto | `rumblingstone-module-standard` (benchmark RHoD + AP Paizo) | un esemplare lo passa; quanti altri, mai misurato |
| il libro | `RICERCA-AUDIT-...-2026-08` | **cinque difetti verificati**; D1 e D4 alti |
| il gioco | ciclo alfa → beta → collaudato | il Drappo è ad **alfa**; gli archi non hanno marcatore |

⚠️ **D1 da solo impedisce di consegnare qualsiasi volume**: il convertitore
markdown→Typst non gestisce `![alt](path)` e l'immagine diventa il testo dell'alt
— `!Stemma Oca`. Un PDF in vendita che stampa il nome dell'illustrazione.

**Gli strumenti** — accoppiamento al canone misurato sulle 54 voci del manifest:
**12 generici** (di cui 7 la pipeline mappe) · **20 quasi** · **22 legati**. La
misura è testuale e quindi un **limite superiore**: `genera_creatura` risulta
legato solo perché *rifiuta* di scrivere in `Bestiario/`.

---

## §5 · Le linee di prodotto

| # | Prodotto | Stato |
|---|---|---|
| **1** | **Il toolkit** — wheel + eseguibile, tre profili di regole | esiste, non estraibile (§4) |
| **2** | **Map pack neutri** | la pipeline è l'unico asset **system-agnostic** |
| **3** | **Gli standalone** — il Drappo è il prototipo | uno esiste, ad alfa |
| **4** | **Un AP originale** sull'infrastruttura già in piedi | non esiste; è la linea più preziosa |
| **5** | **Il metodo** — lo standard dei moduli, il motore di stile, l'indagine | scritto, mai estratto |

⚠️ **Il software venduto com'è vale essenzialmente zero**: nessuno compra una
CLI. La strada corta a una piccola revenue passa dal **contenuto** — un modulo si
vende a chi già compra moduli. Il vincolo di tutto è che **non c'è un pubblico**,
ed è l'unica sfida che non si chiude con un commit.

---

## §6 · I lotti

Le due catene di lavoro sono **indipendenti**: la provenienza serve prima di
*vendere*, la qualità prima di *migliorare*.

### Fase 0 — Sbloccare (niente esce finché questi non sono chiusi)

- **⬜ 0.1 — D1 e D4**: le immagini nel volume da stampa, e `typst` in CI. Bug già
  specificati. *Accettazione*: un booklet con immagini compila e **le mostra**;
  un manifest con chiave ignota **avvisa** invece di tacere.
- **⬜ 0.2 — `pyproject.toml` e fine dei 24 `sys.path.insert`** (ADR-0040 §1).
  *Accettazione*: package importabile da fuori, entrypoint da console, zero
  `sys.path.insert`.
- **⬜ 0.3 — Si popola dal SRD**, da subito. Non è un lotto, è una regola: ogni
  illithid aggiunto oggi è un file in più da bonificare domani.

### Fase 1 — Il dominio e la legenda unica

- **✅ 1.1 — La legenda come fonte unica** — *fatto il 2026-09-12*, dettaglio in
  **§9**. ([ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md), era
  ADR-0014 della #72.) `scripts/legend.yaml` è la fonte, `legend.json` il
  derivato che i consumatori leggono con stdlib, e `legend/single-source` è il
  cancello che l'ADR dichiarava **assente**. *Accettazione soddisfatta*: il gate
  fallisce se un consumatore usa un set proprio — **provato a rovescio**.
  🔎 **E ha morso al primo uso**: i posti in cui viveva la legenda non erano
  cinque ma **otto**, e le tre tabelle in più (`ALTEZZE`, `PIATTI`, `TEXTURE` in
  `render_map_blender.py`) nessuna misura le aveva contate.
- **⬜ 1.2 — I tre profili di regole**. ⚠️ `move_cost: 4` di PF1e è l'unico valore
  della specifica mai verificato sul PRD: da confermare prima di rilasciare quel
  profilo. *Accettazione*: `rules/profile-incomplete` è **error**;
  `rules/saturation-undeclared` è warn.
- **⬜ 1.3 — Cucitura dominio/presentazione**: legenda, parser e modello escono
  da `render_map_svg.py`. *Accettazione*: `arch/layering` fallisce se il dominio
  importa render, export, CLI o profili.

### Fase 2 — Bonifica e verifica

- **⬜ 2.1 — Bonifica del bestiario non-SRD** (§2). ~220 occorrenze, priorità:
  illithid e githyanki (arco 09), poi il Circolo degli Otto, poi il resto. Le
  statistiche restano SRD: si sostituisce l'**identità**. *Accettazione*: un
  validatore che **fallisce** se una rientra.
- **⬜ 2.2 — La verifica della struttura contro RHoD** (§2): camera bianca + test
  del lettore, un verdetto motivato per arco. ⚠️ **Solo se questo lotto stabilisce
  che è falsa** si corregge la riga *«heavily based on Red Hand of Doom»* del
  README. Mai prima.
- **⬜ 2.3 — Il gate d'uscita eseguibile**: `provenienza:` machine-readable, e il
  test nei **due sensi** — ogni artefatto OGC ha la sua voce in `OGL.txt`, e ogni
  voce è usata da almeno un artefatto. *Accettazione*: `dm.py doctor --ip` in CI;
  il Drappo passa **a secco**; un file dell'arco 00 **fallisce**.
- **⬜ 2.4 — `arch/no-campaign-leak`**: nessuna stringa della campagna dentro il
  package venduto, verificato in CI e non a memoria.

### Fase 3 — I prodotti

- **⬜ 3.1 — Il Drappo a beta**: una serata con un gruppo vero, tempi annotati,
  correzioni applicate ai file. ⚠️ **L'unica voce di tutto il piano che non si
  esegue al computer**, ed è anche l'unico modo di sapere se il metro di qualità
  del repo coincide con quello di chi paga.
- **⬜ 3.2 — Il Drappo esce**. *Dipende da* 0.1, 2.3, 3.1.
- **⬜ 3.3 — La pipeline mappe scorporata**: wheel + eseguibile, unico asset
  system-agnostic. Serve da **vetrina**, cioè attacca la sfida del pubblico prima
  di essere un prodotto.
- **⬜ 3.4 — Decidere la UI**, solo con i numeri di 3.2 e 3.3 sotto gli occhi.

⚠️ **Nota di sequenza dalla #72, che vale più di una stima**: il primo rilascio è
possibile **al passo 4 di 8** — senza il linter, che è ciò di cui si parla, non
ciò che porta il primo utente.

---

## §7 · Le sfide

| # | Sfida | Si chiude con |
|---|---|---|
| C1 | l'AP adattato non è vendibile | un AP originale (§5.4), non una bonifica |
| C2 | niente è stato giocato al metro del repo | 3.1 |
| C3 | **D1** — le immagini non entrano in stampa | 0.1 |
| C4 | il toolkit non è estraibile (debito raddoppiato) | 0.2, 1.3 |
| C5 | le tavole sono di terzi | rigenerazione con bibbia visiva propria |
| C6 | il bestiario non-SRD | 2.1 |
| C7 | **nessun pubblico** | ⚠️ **niente di tutto questo** |
| C8 | provenienza delle tavole raster | ADR-0005; la PR #106 ne ha una parte |
| C9 | il MIT non protegge | il marchio, non la licenza |

---

## §8 · Le decisioni aperte

### Al DM, con il costo misurato

<!-- decisioni-dm: VENDIBILITA -->

| # | Decisione | Perché ora, e cosa costa |
|---|---|---|
| ~~**D1**~~ | ✅ **DECISA il 2026-09-12 — la spec funzionale è ratificata.** Vedi §10 per cosa è entrato e a che prezzo. In sintesi: i campi neutri entrano tutti per i **56 simboli** che ne hanno uno; `📦` diventa muro; `🌲` e `🌳` **no**, con deroga motivata; la luce resta quella del codice, scritta in metri. | ✅ Costo pagato: **+4 polilinee** su ciascuno dei 2 `.uvtt` committati, **zero** SVG. Il resto è additivo. 🔵 Ne è nata [**ADR-0049**](adr/ADR-0049-il-margine-del-bosco-e-un-glifo-a-se.md): `🌲` avrà un glifo per il margine, con una coda di **1.873 celle** da rileggere |
| ~~**D2**~~ | ✅ **DECISA il 2026-09-12 — e allargata: le altezze diventano moduli di griglia.** Il DM: *«i muri normalmente sono 1.5, le tende falle più basse 1m»*. 🔎 **Il «1.5» non erano i muri veri**: nel repo `🏰` sta a 4 m, `⬛` a 3,2, `🗼` a 9 — un muro di pietra a 1,5 m sarebbe più basso di un uomo. Era `🧱` **muretto / copertura bassa**, l'unico simbolo chiamato «muro» che un'altezza non ce l'aveva: si estrudeva al default generico di 0,6 m, cioè un gradino, mentre l'etichetta promette copertura al petto. Poi il DM ha esteso la regola: *«muri piccoli 1.5 metri e poi multipli di 1.5 o approssimazioni più vicine possibili»*. Il quadretto del repo è 1,5 m, quindi **tutte e 31** le altezze sono state portate sul modulo: quadretti interi per ciò che sta in piedi (15), mezzo quadretto per l'ingombro che si scavalca (9), zero per ciò che è piatto (7). Prima erano numeri a occhio — 3.2 · 2.2 · 1.6 · 1.4 · 1.1 · 0.9 · 0.8 · 0.6 · 0.4 — che non volevano dire niente rispetto alla griglia su cui la scena è costruita. | ✅ Costo zero: nessun artefatto 3D è committato. 48 celle `🧱`, 9 `⛺`. 🔵 **Resta il dais** `🔳`, e non è una dimenticanza: **zero celle nel repo** — è nato con ADR-0042 e nessuno l'ha ancora disegnato. Deciderlo adesso sarebbe inventarlo; il giorno che serve costa zero |

### Aperte da prima, senza costo misurato

1. **Licenza del core** — raccomandazione: **lasciarlo MIT**. ADR-0040 chiedeva
   il rilicenziamento quando il repo era GPL-3; oggi MIT permette già di vendere,
   e cambiarla costa l'adozione senza proteggere il passato.
2. **Il marchio** «RumblingStone» — non registrato, tempi lunghi, e difende dove
   la licenza non arriva.
3. **Chi fa il playtest beta** (3.1).
4. ⚠️ **La regola che nasce da questo consolidamento**: *prima di aprire un piano,
   si guardano le PR aperte.* Sei settimane di lavoro sono state riscritte da capo
   perché nessuno ha guardato una bozza. Vale la pena metterla nella skill
   `rumblingstone-plans`.

---

## §9 · Lotto 1.1 in dettaglio — la legenda come fonte unica

> `[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests -q` verde con il
> gate `legend/single-source`; **40 SVG e 2 UVTT byte-identici** prima e dopo]`
>
> 🔎 **Erano «130» quando ho scritto questo piano, e la misura mi ha smentito
> durante l'esecuzione**: `git ls-files '*.svg'` ne conta 130, ma 90 sono prop
> illustrati e non mappe. Sotto `validate_maps` ce ne sono **40**, di 18 master.
>
> **Decisione attuata**: [ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md).
> **Spec normativa**: [`LEGENDA-FUNZIONALE-SPEC`](../docs/guides/LEGENDA-FUNZIONALE-SPEC.md).

### 9.0 · Informazioni mancanti e assunzioni dichiarate

**Cosa mi manca, e come procedo lo stesso**

1. **La spec funzionale non è ratificata.** La sua riga 32 dice *«Stato:
   specifica proposta, **gate DM**»*. I suoi valori di `cover`, `obscurement`,
   `move_cost`, `nameable`, `elevation_m`, `climb` non sono canone: sono una
   proposta di luglio che nessuno ha approvato. → **assunzione**: `legend.yaml`
   v1 porta **solo i fatti che il codice già applica oggi**, e la ratifica della
   spec diventa una decisione DM con il suo costo misurato (§9.1.4).
2. **`radius_m` della spec e `LIGHT_SYMS` del codice non concordano** (§9.1.3).
   → **assunzione**: vince il codice, perché il criterio d'uscita è la
   byte-identità; la divergenza va nella stessa decisione.

**Assunzioni di progetto**

3. **YAML sorgente + JSON derivato committato.** Non è una mia scelta: è la
   forma che ADR-0048 §2 prescrive (*«o da un `legend.json` committato e
   verificato in CI, come già si fa per `docs/tools/`»*). Il motivo è
   [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md): `pyyaml` è un
   **debito dichiarato**, e non può entrare nel percorso di rendering. Il
   generatore lo usa, i consumatori leggono `json` di stdlib.
   ⚠️ **Costo dichiarato**: due file invece di uno, e un gate di sincronia in
   più. L'alternativa — un terzo parser YAML fatto a mano, come i due già in
   `suggest_map.py` e `suggest_encounter.py` — sarebbe **la malattia che questa
   decisione cura**.
4. **`Z_ORDER` resta nel renderer.** È ordine di pittura per *pattern*, nessun
   consumatore lo duplica, e spostarlo allargherebbe il lotto senza chiudere
   niente. Non è una svista.

### 9.1 — FASE 1 · Audit, misurato sul repo di oggi (`563a6a9`)

#### 9.1.1 · Lo stato vero è **migliore** di come lo racconta l'ADR

L'ADR-0048 è stato riverificato il 2026-09-10 e ha già **due giorni di ruggine**.
Rimisurato:

| Cosa dice l'ADR | Cosa c'è davvero |
|---|---|
| «quattro script maturi» da rifattorizzare | ✅ **il render è già a fonte unica**: `compile_map_json`, `import_ultraclear` e `render_map_blender` fanno tutti `rms.SYMBOLS`. Nessuno ridichiara i simboli |
| «`HEAVY_PATS` seconda tabella nel renderer» | ⚠️ **non è una seconda tabella**: è un attributo di *rendering* indicizzato per pattern, non per simbolo. Va nella legenda come `render.heavy`, ma non era una divergenza |
| «`legenda-universale.md` copia manuale» | ✅ **misurata: non è divergente.** Elenca tutti e 63 i simboli e le etichette coincidono; le sole 3 differenze sono grassetti e un trattino al posto di una parentesi |
| «i 62 simboli» (spec §4, riga 10) | ❌ **63**. `🔳` è entrato con ADR-0042 dopo la riverifica |

🔎 **Decimo presupposto invecchiato di questa campagna** — e stavolta in meglio:
il lotto è più piccolo di come è scritto.

#### 9.1.2 · La duplicazione vera: **quattro set in due script**

| Set | Dove | Cardinalità | Tutti dentro `SYMBOLS`? |
|---|---|---:|---|
| `WALL_SYMS` | `export_uvtt.py:63` | 8 | ✅ sì |
| `DOOR_SYMS` | `export_uvtt.py:64` | 1 | ✅ sì |
| `LIGHT_SYMS` | `export_uvtt.py:66` | 7 (con valori) | ✅ sì |
| `HAZARD_SYMS` | `import_ultraclear.py:72` | 7 | ✅ sì |

Nessun orfano: **oggi le due tabelle non divergono in appartenenza**. Il difetto
non è un errore presente, è che **niente impedisce il prossimo** — ed è
esattamente ciò che l'ADR dichiara come limite: *«niente impedisce a un quinto
consumatore di nascere col suo set privato»*, cosa già successa due volte.

E **9 etichette su 63** portano ancora la funzione di gioco in prosa
(`🌲 ⬛ 🔳 🪨 🕸 🌋 🌾 ⛺ 🧱`): «copertura +4 CA», «blocca vista e movimento»,
«NON e' un muro». Prosa che nessuno script può interrogare.

#### 9.1.3 · La spec copre 56 simboli su 63, e i 7 che restano **non sono un buco**

| Categoria | N | Perché |
|---|---:|---|
| con `function` dichiarata nella spec §4 | 56 | — |
| unità (`🔵 🔴 ⚫ 🟡 🟢 🟣`) | 6 | ✅ **per progetto**: la spec §4.5 dice che le unità *non hanno* `function`, hanno `unit: {side, role}` |
| `🔳` dais | 1 | ⚠️ nato dopo la riverifica — ma la sua funzione **è già decisa** da [ADR-0042](adr/ADR-0042-tre-glifi-per-tre-cose.md) §tabella: vista no, movimento no, muro no |

🔴 **Conclusione che cambia il lotto**: non c'è **nessun valore da inventare**.
Ogni dato che serve è già deciso da qualche parte — nel codice, nella spec, o in
un ADR. Questo lotto non prende decisioni di contenuto.

⚠️ **Tranne una divergenza, e va detta**: la spec dà la luce in **metri**
(`🏮 radius_m: 6`, `🕯 1.5`, `✨ 3`, `🔮 3`), il codice in **quadretti**
(`🏮 6.0`, `🕯 3.0`, `✨ 3.0`, `🔮 4.0`). A 1,5 m/quadretto sono **quattro
valori diversi su quattro**. Vince il codice (byte-identità), e la divergenza va
al DM.

#### 9.1.4 · Cosa costerebbe ratificare la spec — il numero che serve al DM

Se `WALL_SYMS` derivasse da `function.blocks_sight` come la spec lo dichiara,
**tre simboli entrerebbero fra i muri** che oggi non ci sono (`🚪` no: le porte
hanno già la loro geometria):

| Simbolo | Occorrenze nei markdown tracciati |
|---|---:|
| `🌲` Foresta densa | **2.073** |
| `🌳` Treant | 18 |
| `📦` Casse | 10 |
| **totale** | **2.101 in 38 file** |

🔴 **`🌲` da solo è grande quanto `⛰`** (2.423 celle), che è costato
[ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md)
e una decisione esplicita del DM. Non si fa di straforo dentro un lotto di
architettura: stessa classe, stesso trattamento. → **decisione D1 di questo
piano** (§8).

#### 9.1.5 · Trovato misurando, fuori scopo, dichiarato

🐛 **La tabella «Oggetti» di `legenda-universale.md` è spezzata in due.** Un
blocco `>` di nota ADR-0042 sta **in mezzo alle righe**, e ogni lettore markdown
la rende come **due tabelle** con le ultime tre voci (`🔮 🪑 🧱`) orfane
dell'intestazione. La generazione di §9.2.6 la ripara di conseguenza — non come
correzione a mano, ma perché un file generato non può avere quella forma.

### 9.2 — FASE 2 · Sviluppo

Un commit, un merge. Ordine di esecuzione, ciascun passo verificabile da solo.

#### 9.2.1 · `scripts/legend.yaml` — generato **dal codice**, non trascritto

⚠️ Trascrivere 63 simboli a mano introdurrebbe errori che la byte-identità
troverebbe ma che costerebbero un giro. Il file nasce da uno **script una-tantum**
che serializza `SYMBOLS` + i quattro set così come sono adesso; i commenti di
ADR-0042 e ADR-0043 — che sono memoria istituzionale, non decorazione — si
riportano a mano **sopra** le voci che spiegano.

#### 9.2.2 · `scripts/build_legend.py` → `scripts/legend.json`

Generatore, `pyyaml` in `external_deps` (l'eccezione già ammessa da ADR-0037).
Uscita deterministica e committata, come `monster_catalog.yaml`.

#### 9.2.3 · `scripts/dmcore/legenda.py` — il lettore, **stdlib**

`json` e basta. Espone `simboli()`, `pattern_pesanti()`, `muri()`, `porte()`,
`luci()`, `pericoli()`. Sta in `dmcore/` per la stessa ragione di `testo.py`:
è la casa dei dati condivisi fra script.

#### 9.2.4 · I consumatori derivano

`render_map_svg.SYMBOLS` e `HEAVY_PATS`; `export_uvtt.WALL_SYMS`/`DOOR_SYMS`/
`LIGHT_SYMS`; `import_ultraclear.HAZARD_SYMS`. **La forma del dict non cambia**
(`mode`/`pat`/`prop`/`fill`/`it`): quattro script e sei test la leggono, e
cambiarla sarebbe un secondo lotto travestito da primo.

#### 9.2.5 · Il cancello che mancava: `legend/single-source`

Il criterio d'accettazione scritto in §6 di questo piano, finalmente eseguibile.
Analisi `ast` dei cinque consumatori: **un set o dict letterale di emoji a
livello di modulo è un errore**. È il presidio che ADR-0048 dichiara assente.

#### 9.2.6 · `legenda-universale.md` si genera

Tabelle fra marcatori `<!-- legenda:auto-begin/end -->`, prosa fuori. Ripara
anche §9.1.5.

#### 9.2.7 · Regola d'oro (ADR-0009) e ADR-0047

ADR-0048 → **attuata**; §6 lotto 1.1 → ✅ con i numeri veri; nota alla spec
(63 non 62); `plans/INDEX.md`; `plans/CHANGELOG.md`; **§8 diventa una tabella
marcata** `<!-- decisioni-dm: VENDIBILITA -->` con la decisione D1 di §9.1.4, e
`decisioni_dm.py --emit` rigenera l'aggregato.

### 9.3 — FASE 3 · Validazione

Il criterio resta quello della campagna: **ogni cancello si prova a rovescio**,
non solo a passare.

| Prova | Come | Atteso |
|---|---|---|
| **Byte-identità SVG** | `validate_maps.py` | 40 SVG identici |
| **Byte-identità UVTT** | rigenerare i 2 `.uvtt` e `diff` | zero righe |
| **YAML↔JSON in sincronia** | rigenerare, `diff` | zero |
| **`legend/single-source` morde** | rimettere `WALL_SYMS = {...}` letterale in `export_uvtt.py` | 🔴 rosso |
| **la legenda-skill morde** | cambiare un'etichetta nel YAML senza rigenerare | 🔴 rosso |
| **i 4 set sopravvivono** | confronto con i valori congelati di oggi | identici |
| **non-regressione** | `pytest scripts/tests -q`, `tools_manifest --check`, `validate_docs --sorgenti`, `check_plans_discipline`, `decisioni_dm --check` | verdi |

### 9.4 · Cosa **non** fa questo lotto, dichiarato

| | Cosa | Perché |
|---|---|---|
| 🔵 | ratificare la spec funzionale (`cover`, `obscurement`, `move_cost`, `nameable`, `elevation_m`, `climb`) | **decisione DM**: 2.101 celle, §9.1.4 |
| 🔵 | luce in metri o in quadretti | stessa decisione, §9.1.3 |
| ⬜ | `rules/<sistema>.yaml`, i tre profili | lotto **1.2** |
| ⬜ | dominio fuori da `render_map_svg.py` | lotto **1.3** |
| ⬜ | riclassificare le 6.960 celle `⬛` | coda di ADR-0042, è lettura non sostituzione |

---

## §10 · Lotto 1.1-bis — la ratifica funzionale (D1 decisa il 2026-09-12)

> `[K canone · Opus 5 · alto · `python3 -m pytest scripts/tests/test_legenda_fonte_unica.py -q`
> verde con 21 test; **40 SVG byte-identici**, i 2 `.uvtt` cambiano di **+4
> polilinee** ciascuno e il delta è misurato prima]`

### 10.1 · Cosa ha deciso il DM, e cosa costa

D1 non era una decisione: erano **tre**, con prezzi molto diversi. Presentate
separate e decise separate.

| | Decisione | Costo pagato |
|---|---|---|
| **a** | ✅ **I campi neutri entrano tutti** — `blocks_movement`, `blocks_sight`, `cover`, `obscurement`, `move_cost`, `nameable`, più `climb`, `swim`, `destructible`, `prone_concealment`, `hazard{kind,severity}` dalle Note | **zero**: nessuno script li legge ancora. Diventano il dato di partenza del lotto **1.2** |
| **b** | ✅ **`📦` diventa muro**; `🌲` e `🌳` **no** | **+4 polilinee** su ciascuno dei 2 `.uvtt` committati |
| **c** | ✅ **La luce resta quella del codice**, scritta in metri | **zero**: la conversione a 1,5 m/quadretto torna esatta |

🔎 **Il conteggio del piano era gonfio, e l'ho corretto misurando meglio.** §9
diceva 2.101 celle in 38 file: era `str.count` su tutto il markdown, quindi
contava le righe di legenda e la prosa. Le **celle vere dentro le griglie sono
1.889 in 8 master**. La conclusione non cambia — `🌲` da solo resta della taglia
di `⛰` — ma il numero sì.

### 10.2 · La scoperta sulla luce

I valori della specifica **sono le regole 3.5 alla lettera**, quelli del codice
sono generosi di casa:

| | Codice | Spec | 3.5 RAW |
|---|---:|---:|---|
| `🏮` braciere | 6,0 quadretti | 4,0 | torcia = 20 ft = 4 quadretti |
| `🕯` candele | 3,0 | **1,0** | candela = 5 ft = 1 quadretto |
| `✨` · `🔮` | 3,0 · 4,0 | 2,0 · 2,0 | — |

Il repo illumina da **1,5 a 3 volte** più del manuale. La decisione è tenere il
codice: le mappe notturne sono state disegnate e giocate con quella luce, e
dimezzarla per aderenza al manuale le spegnerebbe tutte insieme. La divergenza
si chiude **scrivendo in metri i valori del codice**, non cambiandoli.

### 10.3 · Il problema di progetto, e come è stato risolto

🔴 **La tentazione era un secondo booleano.** Dopo la ratifica esistono due
affermazioni diverse: `blocks_sight` (il fatto neutro — un bosco *blocca la
vista attraverso la cella*) e «l'export UVTT ci mette un segmento». Tenerle in
due campi indipendenti avrebbe **ricreato le due fonti** che ADR-0048 aveva
appena finito di unire, e sarebbero divergite in silenzio come `SYMBOLS` e
`WALL_SYMS` prima di ADR-0042.

**Il muro si deriva** da `blocks_sight` meno le **deroghe**, e una deroga deve
scrivere il proprio motivo in `deroga_uvtt`. Sono tre, tutte con una ragione che
non è comodità:

| | Perché deroga |
|---|---|
| `🌲` | il muro del VTT è binario e il bosco no. Muro pieno = un PG **dentro** gli alberi non vede il quadretto adiacente, e l'inseguimento nel bosco — il motivo per cui quelle mappe esistono — diventa ingiocabile. → [ADR-0049](adr/ADR-0049-il-margine-del-bosco-e-un-glifo-a-se.md) |
| `🌳` | è una **creatura**, non terreno: un treant si muove, un muro no. Lo dice la spec stessa (§4.2 → §7) |
| `🚪` | ha già la sua geometria: `door: true` produce un varco. Chiusa è un muro, aperta un passaggio, e lo stato non è una proprietà del simbolo |

### 10.4 · Trovato ratificando, accettato, dichiarato

🐛 **`🌋` non era classificato come pericolo.** La spec gli dà
`hazard: {fire, lethal}`; il codice lo metteva fra le *strutture*, come un tavolo.
Sono **12 celle in un master solo** (`Portale-Forgia-L2`), nessun artefatto
dell'import è committato, e una bocca vulcanica è un pericolo: correzione
accettata dentro la ratifica.

⚠️ **`❄` va nella direzione opposta e non l'ho forzato.** Il codice lo tratta da
pericolo dal primo giorno; la specifica **non lo classifica affatto**. Tengo la
classificazione e scrivo `severity: null`: dire «è un pericolo, la gravità non è
decisa» è vero, inventarne una no.

### 10.5 · Validazione

Tre prove a rovescio sul meccanismo nuovo, tutte rosse quando devono:

| Prova | Esito |
|---|---|
| una deroga con un motivo vuoto (`boh`) | ✅ `test_ogni_deroga_ha_un_motivo_vero` rosso |
| una deroga nuova su `⛰`, con un motivo che *sembra* serio | ✅ **due** test rossi: le deroghe decise e i valori congelati |
| un campo `wall: true` rimesso accanto al fatto neutro | ✅ `test_il_muro_e_derivato_non_dichiarato` rosso |

Più: 40 SVG byte-identici, le luci identiche al quadretto, il delta dei 2 `.uvtt`
misurato **prima** di rigenerarli e coincidente (+4 polilinee ciascuno).

### 10.6 · Cosa resta aperto

| | Cosa | Dove va |
|---|---|---|
| ⬜ | `🌲`: il glifo del margine e la coda di **1.873 celle** | **ADR-0049**, lotto 1.1-ter |
| ✅ | **D2** — `⛺` 1 m e `🧱` 1,5 m, decise il 2026-09-12 (§8) | fatto |
| 🔵 | l'altezza del dais `🔳` | libera: **zero celle** nel repo, si decide quando serve |
| ⬜ | i tre profili di regole; ⚠️ la riga `move_cost: 4` di **PF1e** resta fuori finché non è verificata sul PRD (il valore neutro `4` è 3.5 RAW ed è entrato) | lotto **1.2** |
