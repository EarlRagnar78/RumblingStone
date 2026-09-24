# ADR-0040 — Separazione dei due prodotti e rilicenziamento del toolkit

**Stato**: accettata — decisione DM del 2026-07-26, **rinumerata e annotata** il 2026-09-04

> ⚠️ **Il numero è cambiato** per la stessa ragione di ADR-0039: nacque come
> ADR-0017 nella PR #72, rimasta bozza, e 0017 è stato poi assegnato ad
> «moduli autoconclusivi».
>
> ⚠️ **Una premessa di questa ADR è invecchiata, la conclusione no.** Il testo
> dice «il repo è GPL-3»: non lo è più. [ADR-0029](ADR-0029-licenza-doppia-testo-e-script.md)
> (settembre 2026) ha diviso il repo in **CC BY-NC-SA 4.0** per il testo e
> **MIT** per `scripts/`. Il rilicenziamento del toolkit quindi **non serve più
> per poter vendere** — MIT lo permette già, e una licenza vincola chi la riceve,
> non chi la concede. Resta invece intatta, e verificata di nuovo il 2026-09-04,
> la diagnosi che conta: **il blocco non è di IP, è strutturale.**
>
> ⚠️ **E il debito è cresciuto.** Luglio misurava 11 `sys.path.insert`; oggi sono
> **24**. `render_map_svg.py` era 1.530 righe, oggi 1.538, ed è ancora importato
> da quattro moduli per il parser e la legenda. `pyproject.toml` continua a non
> esistere.
**Data**: 2026-07-26
**Decisione-fonte**: risposte DM del 2026-07-26 — *«rilicenziare il toolkit»*, *«wheel + eseguibile autonomo»*, *«vendo il toolkit, i map pack neutri e il metodo»*. Presupposti misurati in `docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md` §6.4. Non modifica [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md), lo **delimita**.

## Contesto

ADR-0005 ha stabilito che il repo non è commercializzabile: il blocco
WotC/Forgotten Realms da solo basta. Quella conclusione resta vera — **per il
contenuto**. Ma il repo contiene due corpi con vincoli opposti, e ADR-0005 li
trattava come uno:

| | **A — la campagna** | **B — il toolkit** |
|---|---|---|
| Cosa | archi 00-09, Bestiario, PG, canone | `scripts/`, schemi, legenda, renderer |
| Blocco IP | RHoD + Forgotten Realms (WotC) | **nessuno**: codice originale, arte procedurale in-house, nessun asset di terzi |
| Vendibile | **no** | **sì** |

Il toolkit non ha mai avuto un blocco IP. Aveva un blocco **strutturale**: non è
estraibile. 11 script fanno `sys.path.insert(0, …)`; quattro moduli importano
`render_map_svg.py` — 1.530 righe di *rendering* — per ottenerne il **parser** e
la **legenda**. Non esiste `pyproject.toml`. Nulla è installabile o importabile
da fuori.

C'è poi la licenza: il repo è **GPL-3**. Vendere sotto GPL-3 è legittimo, ma chi
acquista può ridistribuire il sorgente liberamente. La cronologia dei contributi
è pulita — le uniche identità sono il DM (tre email) e Claude, i cui output
appartengono al DM — quindi il rilicenziamento è possibile senza raccogliere
consensi di terzi.

## Decisione

**Il toolkit diventa un prodotto separato, estraibile e rilicenziabile. La
campagna resta dov'è, con i vincoli di ADR-0005 intatti.**

### 1. Separazione strutturale prima di quella legale

Nessun cambio di licenza prima che il confine tecnico esista. In ordine:

1. `pyproject.toml`, package importabile, entrypoint da console, **fine degli 11
   `sys.path.insert`**;
2. cucitura **dominio / presentazione**: legenda, parser della griglia e modello
   della mappa escono da `render_map_svg.py`; renderer, exporter, importer e
   linter **dipendono** dal dominio, non viceversa;
3. la campagna diventa un **consumatore** del toolkit. `campaign/` e gli archi
   non cambiano, e il modo in cui il DM lavora non cambia.

**Il layout attuale resta invocabile identico** (`python3 scripts/dm.py …`):
l'installazione è un'aggiunta, non una sostituzione.

### 2. Rilicenziamento

Alla fine del punto 1, il toolkit esce da GPL-3 e la licenza è scelta dall'autore
(proprietaria o duale). Vincoli:

- il rilicenziamento copre **solo** il codice originale del toolkit. Le
  dipendenze di terzi restano sotto le loro licenze — tutte permissive e
  compatibili con la ridistribuzione (BSD-3 / MIT / BSD-2, ADR-0015);
- i **profili di regole** hanno un regime proprio e non seguono la licenza del
  motore: OGL 1.0a per 3.5 e PF1e, CC BY 4.0 per 5e ([ADR-0039](ADR-0039-profili-regole-multisistema.md));
- la campagna **non** viene rilicenziata e **non** viene venduta. ADR-0005 resta
  in vigore su di essa senza modifiche.

### 3. Cosa si vende (decisione DM)

| Prodotto | Contenuto | Vincolo |
|---|---|---|
| **Il toolkit** | renderer, contratto JSON, export UVTT/Foundry/Roll20, import Watabou e ultra-clear, linter di level design | il titolo che vende resta *«scrivi la mappa come testo, ottieni una scena Foundry con muri e luci»*; il linter è la funzione che fa dire «l'ha scritta qualcuno che sa cosa fa», non è ciò che porta il primo utente |
| **Map pack neutri** | mappe originali **world-neutral**, fuori Forgotten Realms, in SVG/PNG/UVTT | zero contenuto WotC; etichetta `Contains AI-Generated Content` dove pertinente; **nessuna mappa RHoD**, nemmeno riprogettata |
| **Il metodo** | schede-mappa, le 9 metriche, il corpus di calibrazione, la disciplina di progettazione | è la parte senza concorrenti; vendibile come guida, e utile anche a chi non compra il software |

### 4. Confezionamento

Doppia via, decisa dal DM: **wheel** per chi è tecnico **ed eseguibile autonomo**
(PyInstaller) con tutte le dipendenze incluse per il DM medio, che non deve
sapere cosa sia `pip`. Conseguenza vincolante su ADR-0015: **ogni dipendenza deve
essere ridistribuibile in forma binaria dentro un bundle** — il gate di licenza
permissiva smette di essere igiene e diventa un requisito di prodotto.

## Conseguenze

**Cosa diventa più facile**

- il toolkit diventa vendibile **senza toccare la campagna** e senza riaprire la
  bonifica §7 del rapporto Palio, che resta gated e non necessaria;
- diventa possibile accettare contributi esterni con una CLA, e pubblicare
  release versionate;
- l'editor visuale (`PIANO-EDITOR-VISUALE-MAPPE`) ha finalmente qualcosa da
  importare: oggi pianifica un progetto separato che non avrebbe un package a cui
  agganciarsi;
- la separazione dei due prodotti chiarisce anche **cosa non va mai messo dove**:
  nessun nome, luogo o statblocco della campagna entra nel toolkit.

**Cosa diventa più difficile / a cosa si rinuncia**

- vendere significa **obblighi ricorrenti**: conformità OGL a ogni release,
  attribuzione CC BY per il profilo 5e, avvisi di licenza delle dipendenze
  bundled, supporto agli acquirenti, matrice di build su tre sistemi operativi;
- il rilicenziamento va fatto **una volta e bene**: serve una verifica della
  provenienza di ogni file che entra nel package (nessun frammento di terzi, che
  è già la regola del repo, ma va **dimostrata**, non assunta);
- si rinuncia al contributo GPL della community sul toolkit, se si sceglie la
  via proprietaria pura;
- **questa non è consulenza legale.** Prima di vendere serve un avvocato IP: la
  conformità OGL, il testo di compatibilità e i marchi non sono
  autocertificabili.

**Cosa va rivisitato e quando**

- **repo unico con package interno, o due repo separati**: si decide quando il
  toolkit ha una superficie pubblica stabile — cioè dopo la separazione
  strutturale, non prima. Deciderlo adesso sarebbe indovinare;
- se arrivassero contributor esterni, serve una CLA **prima** del primo merge,
  non dopo;
- ADR-0005 va riletto se e solo se si decidesse di vendere anche contenuto di
  campagna: oggi la decisione è esplicitamente il contrario.
