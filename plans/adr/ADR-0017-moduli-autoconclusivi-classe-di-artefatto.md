# ADR-0017 — I moduli autoconclusivi sono una classe di artefatto a sé

**Stato**: accettata
**Data**: 2026-08-15
**Decisione-fonte**: costruzione di `STANDALONE-Il-Drappo-di-Tarsilia/` (PR #103) e
audit del DM del 2026-08-15 — *«ci sono eventi per i personaggi? un master ha tutto
sotto controllo o ha bisogno di un'AI? cosa manca davvero?»*

## Contesto

Fino al 2026-08-14 il repo conteneva **una sola forma di contenuto giocabile**: gli
archi della campagna (`00_`–`09_`), che presuppongono tutti quattro PG noti, un
`campaign/state.md`, i Forgotten Realms, le regole 3.5 e la storia pregressa.

Poi è nato un modulo che **non presuppone niente di tutto questo**: sei PG
pregenerati, Golarion, Pathfinder 1e, tre serate, nessuna continuità con la campagna.
Trattarlo come un arco avrebbe prodotto due danni simmetrici:

1. **assorbirlo nella campagna** — e allora avrebbe ereditato `state.md`, ADR-0007,
   il branch di gruppo e il canone dei Reami, cioè esattamente ciò che il modulo
   esiste per non avere;
2. **lasciarlo fuori da ogni regola** — ed è quello che è successo per un giorno:
   `validate_modules.py` copre solo i master `ARC*-DEF-*.md`, quindi il modulo nuovo
   ha vissuto senza **nessun gate**, e un file rinominato non l'avrebbe scoperto
   nessuno fino al tavolo.

Serviva una terza casella.

## Decisione

**Un modulo autoconclusivo è una classe di artefatto distinta**, riconoscibile dal
prefisso di cartella `STANDALONE-`, con un proprio contratto e un proprio gate.

### 1. Il confine — cosa un modulo standalone non può fare

- **Non dipende da `campaign/state.md`**, né dal branch di gruppo (ADR-0007), né dal
  canone della campagna. Se ha bisogno di memoria fra le sessioni, se la tiene da sé
  (`STATO-DEL-MODULO.md`, un modello vuoto da copiare per gruppo).
- **Non entra nel Bestiario** né nel catalogo mostri: i suoi statblocchi sono locali.
  `build_monster_catalog.py` esclude `STANDALONE-*` — altrimenti mescolerebbe sistemi
  diversi nello stesso catalogo.
- **Può riusare gli asset della campagna citandoli per percorso**, mai copiandoli:
  una copia diventa subito una copia vecchia. *(Gli stemmi del Drappo stanno ancora
  nell'arco 09 e sono citati, non duplicati.)*
- **Dichiara il proprio sistema e la propria ambientazione in testa all'hub.** Un
  modulo standalone può girare su regole diverse da quelle della campagna.

### 2. Il contratto — cosa un modulo standalone deve avere

Verificato da `scripts/validate_standalone.py` (gate CI):

| # | Obbligo | Perché |
|---|---|---|
| 1 | un **hub** `00-*.md` | il punto d'ingresso unico |
| 2 | una **guida del DM** `07-GUIDA-DM*.md` | ADR-0018: senza apparato d'uso non è un modulo |
| 3 | **schede pregenerate** `PREGEN-*.md` con Difesa/Attacco/Statistiche/Equipaggiamento per ogni scheda | è quello che si stampa |
| 4 | **statblocchi** `STATBLOCCHI*.md` | |
| 5 | una **nota IP** `IP-E-LICENZE.md` | un modulo staccato dalla campagna è anche staccato dal suo ombrello legale, e deve dire il proprio |
| 6 | almeno un **file-giornata** con ≥3 righe di read-aloud | un modulo senza testo da leggere ad alta voce non si gioca: si riassume |
| 7 | **riferimenti incrociati risolvibili** | è il difetto che si crea da solo rinominando |
| 8 | **contatori dichiarati** col valore di partenza, se il modulo ne usa | |
| 9 | **zero meccaniche 5e** | il repo gira su 3.5/PF1e |

### 3. Il rapporto con gli standard esistenti

- `rumblingstone-module-standard` resta la **misura della profondità** e vale anche
  qui: cambia il formato dei file, non l'asticella.
- `rumblingstone-narrative-style` vale **identica**, senza deroghe.
- `rumblingstone-plans` vale identica: un modulo è un piano come gli altri.
- **Non** valgono: ADR-0007 (scritture canone), il `state.md` di campagna, il
  Bestiario condiviso.

### 4. I generatori locali al modulo — la deroga ad ADR-0012, dichiarata

[ADR-0012](ADR-0012-standard-ingegneria-tool-verificabile.md) impone lo standard di
authoring a *«ogni nuovo tool eseguibile del repo (Python o shell, **sotto `scripts/`
o `converters/`**)»*. Un modulo autoconclusivo produce però i **propri** generatori —
il Drappo ha `ALLEGATI/tavole/build_tavole.py`, che disegna la mappa della città, il
Drappo e i sei ritratti — e quel file è **fuori dal perimetro**: non sta in
`scripts/`, non è nel manifest, e nessun gate lo guardava.

Due strade e una sola sensata:

- ❌ **spostarlo in `scripts/`** — inquinerebbe il toolkit della campagna con codice
  che conosce le otto contrade di Tarsilia e non serve a nient'altro. E contraddice
  il §1 di questo ADR: il modulo possiede i propri asset;
- ✅ **ammettere i generatori locali, con condizioni verificate**.

**Un modulo autoconclusivo può avere generatori propri** sotto la sua cartella, a
quattro condizioni — tutte controllate da `validate_standalone.py`:

1. **stdlib-only**, senza binari esterni: un generatore che richiede installazioni è
   un generatore che fra sei mesi non gira più;
2. **docstring di modulo** che dica cosa produce e con quale comando si rigenera;
3. **citato in un `.md` del modulo**, così esiste anche per chi non fruga nelle
   cartelle;
4. **compila** — smoke minimo, in CI insieme al resto del gate.

Restano invece **fuori discussione** in un generatore locale: scrivere fuori dalla
propria cartella, toccare canone, chiamare la rete. Un tool che fa una di queste cose
non è locale al modulo: va in `scripts/` e segue ADR-0012 per intero.

## Conseguenze

- Più facile: un modulo nuovo nasce con un gate il giorno stesso, e nessuno deve
  decidere caso per caso se «vale come arco».
- Più difficile / rinunce: il modulo **non eredita** gli strumenti di sessione della
  campagna (`dm.py session`, i recap automatici, il diff di `state.md`). Chi vuole
  quel livello di automazione su uno standalone deve costruirselo, oppure accettare
  la versione a matita di `STATO-DEL-MODULO.md`. **Accettato**: tre serate non
  giustificano una pipeline.
- Da rivisitare: **se nascerà un secondo modulo standalone**. Due istanze rendono
  visibile cosa è davvero comune e cosa era specifico del Drappo — e allora il
  contratto del §2 va rivisto sui fatti, non sulle previsioni.

## Copertura

- `scripts/validate_standalone.py` — il gate, in CI a ogni PR (incluse le quattro
  condizioni del §4)
- `scripts/build_monster_catalog.py` — l'esclusione
- `STANDALONE-Il-Drappo-di-Tarsilia/` — l'implementazione di riferimento
- [ADR-0018](ADR-0018-apparato-uso-obbligatorio.md) — cosa deve contenere la guida
  del DM
