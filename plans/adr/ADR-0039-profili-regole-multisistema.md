# ADR-0039 — Profili di regole multi-sistema: il motore è neutro, 3.5 / PF1e / 5e sono file sostituibili

**Stato**: accettata — decisione DM del 2026-07-26, **rinumerata** il 2026-09-04

> ⚠️ **Perché il numero è cambiato.** Questa decisione nacque come ADR-0016 nella
> PR #72 (26 luglio 2026), che è rimasta aperta come bozza. Nel frattempo il
> numero 0016 è stato assegnato ad ADR-0016 «lingua sorgente e edizioni», e
> altri quattro numeri della stessa PR (0014, 0015, 0017, 0018) sono finiti
> occupati allo stesso modo. La decisione è valida e non è mai stata revocata:
> cambia solo il numero. La PR #72 è stata chiusa il 2026-09-04 e il suo
> contenuto vive qui e in `PIANO-VENDIBILITA.md`.
**Data**: 2026-07-26
**Decisione-fonte**: risposta DM alla domanda «dove metto i numeri 3.5?» → **«deve supportare 3.5, Pathfinder 1e e D&D 5»**. Specifica completa da recuperare dalla PR #72 (`docs/guides/LEGENDA-FUNZIONALE-SPEC.md`, 283 righe) — è il lotto P1.1 del piano.

## Contesto

Il DM ha deciso che il toolkit va **venduto** (ADR-0040) e che deve supportare
**tre sistemi di regole**. Le due decisioni insieme vincolano l'architettura più
di quanto sembri, per due ragioni indipendenti.

**Ragione tecnica.** I tre sistemi non differiscono solo nei numeri: differiscono
nel *modello*. La copertura in 3.5/PF1e è +4/+8 CA con bonus ai Riflessi; in 5e è
+2/+5 a CA e TS Destrezza. L'occultamento in 3.5/PF1e è una **percentuale di
fallimento**; in 5e non esistono percentuali — c'è l'oscuramento leggero
(svantaggio) e pesante (accecato). Il terreno difficile ×4 esiste in 3.5 e **non
esiste** in 5e. Un'astrazione che copra i tre non può essere «i numeri di uno dei
tre con delle eccezioni»: dev'essere un vocabolario neutro con tre traduzioni.

**Ragione legale.** Le meccaniche dei tre sistemi arrivano con regimi diversi:
SRD 3.5 e PRD Pathfinder 1e sono Open Game Content sotto **OGL 1.0a** (testo
della licenza + catena Section 15 obbligatori nel prodotto); l'SRD 5.1 è stato
rilasciato da WotC sotto **CC BY 4.0**, che chiede solo attribuzione. Mescolare i
tre regimi dentro il motore contaminerebbe l'intero prodotto con l'obbligo più
stringente.

## Decisione

**Il motore non conosce nessun sistema. I numeri di gioco vivono in profili
sostituibili, uno per sistema, isolati anche sotto il profilo della licenza.**

### 1. Tre strati, confini netti

| Strato | Contiene | Cambia col sistema? | Regime |
|---|---|---|---|
| `legend.yaml` | render + **funzione neutra**: `blocks_movement`, `blocks_sight`, `blocks_line_of_effect`, `cover`, `obscurement`, `move_cost`, `elevation_m`, `climb`, `hazard`, `light`, `destructible`, `nameable` | **no** | opera propria |
| `rules/dnd35.yaml` · `rules/pf1e.yaml` | traduzione in meccanica | sì | **OGL 1.0a** |
| `rules/dnd5e.yaml` | traduzione in meccanica | sì | **CC BY 4.0** |

**`legend.yaml` non contiene alcun numero di gioco.** Nessun `+4`, nessun `20%`,
nessuna CD. Una roccia «dà copertura parziale»; quanto valga è del profilo.

### 2. Il vocabolario neutro è dimensionato sul sistema più ricco

- `cover: none | half | three_quarters | total` — **quattro** valori. La bozza
  iniziale di ADR-0014 ne aveva tre (`none|half|full`) e non basta: 3.5 e PF1e
  distinguono copertura da copertura migliorata, 5e metà da tre quarti.
- `obscurement: none | light | heavy` — nome neutro di proposito: `concealment`
  è terminologia 3.5 e avrebbe imposto il modello percentuale a 5e.
- `blocks_sight` e `blocks_line_of_effect` sono **campi distinti**: grate,
  feritoie e siepi separano i due concetti in tutti e tre i sistemi.

### 3. Regola di saturazione: **saturare e dichiarare, mai inventare**

Quando un valore neutro non è esprimibile nel sistema di destinazione, il profilo
lo riduce al valore rappresentabile più vicino **e lo dichiara nel report**. Caso
canonico: `move_cost: 4` non esiste in 5e → il profilo 5e emette ×2 e segnala la
saturazione. Non si inventa una regola casa nel profilo: la deroga è del DM, e
deve restare visibile.

### 4. Il profilo è selezionabile e verificabile

`--rules dnd35|pf1e|dnd5e`, default configurabile per campagna. Ogni profilo ha
una suite di test propria che verifica le traduzioni contro la sua fonte, e
dichiara in testa la licenza, la fonte e la revisione su cui è stato scritto.

### 5. Confini di marchio

«Dungeons & Dragons», «D&D» e «Pathfinder» sono marchi e **non** compaiono nel
nome del prodotto né nel marketing. Il prodotto si descrive per compatibilità,
con la formula ammessa da ciascuna licenza — **formula da verificare testo alla
mano prima del rilascio**, per ciascuno dei tre. Gli *identificatori interni*
(`dnd35`, `pf1e`, `dnd5e`) restano nomi di file, non claim commerciali.

## Conseguenze

**Cosa diventa più facile**

- il mercato indirizzabile passa da «i DM di 3.5» — un pubblico piccolo e in
  calo — a **3.5 + PF1e + 5e**, dove 5e è il grosso;
- l'OGL tocca **due file**, non il prodotto: un acquirente che usa solo il
  profilo 5e non riceve nemmeno contenuto OGL;
- aggiungere un quarto sistema (PF2e, OSR, Shadowdark) diventa **scrivere un
  file**, non toccare il motore. È la scelta che rende il prodotto estendibile
  senza rilasci maggiori;
- il linter di level design resta valido su tutti e tre: le affordance sono
  geometriche, le soglie no.

**Cosa diventa più difficile / a cosa si rinuncia**

- **si rinuncia alla fedeltà completa a un singolo sistema.** Un vocabolario che
  copre tre non esprimerà mai i casi limite di nessuno. È un costo accettato: il
  linter misura affordance, non arbitra regole;
- tre profili significano **tre suite di verifica** e tre fonti da riseguire a
  ogni errata;
- il campo `move_cost: 4` è oggi **non verificato** per PF1e: va confermato sul
  PRD prima del rilascio di quel profilo;
- la conformità OGL (Section 15, dichiarazione di Product Identity e Open Game
  Content) è lavoro reale e ricorrente a ogni release, non una casella iniziale.

**Cosa va rivisitato e quando**

- se un quarto sistema richiedesse un campo neutro nuovo, si estende il
  vocabolario — **mai** si aggiunge un campo specifico di sistema a `legend.yaml`;
- se WotC o Paizo cambiassero i termini di licenza, l'isolamento per file
  permette di ritirare **un profilo** invece del prodotto. È metà del motivo di
  questa decisione;
- la formula di compatibilità nel marketing va rivista a ogni cambio di licenza
  a monte.
