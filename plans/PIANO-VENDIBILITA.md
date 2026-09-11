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

- **⬜ 1.1 — La legenda come fonte unica**
  ([ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md), era ADR-0014
  della #72). La spec è **già in repo** dal 2026-09-04
  (`docs/guides/LEGENDA-FUNZIONALE-SPEC.md`, 62 simboli): resta da fare
  l'attuazione, cioè `scripts/legend.yaml` e i consumatori che ne derivano.
  ⚠️ Chiude un difetto **ancora aperto**: `SYMBOLS` del renderer e `WALL_SYMS`
  dell'export UVTT sono due tabelle separate, e l'SVG stampato e la scena
  Foundry non concordano su cosa sia un muro. 🔴 **Il costo del ritardo è
  misurato**: ADR-0042 e ADR-0043 hanno rattoppato due sintomi di questa stessa
  causa, uno per volta, con due ADR separati. *Accettazione*:
  `legend/single-source` fallisce se un consumatore usa un set proprio.
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
