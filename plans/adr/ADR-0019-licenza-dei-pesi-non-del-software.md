# ADR-0019 — Per le immagini generate, la licenza sta nei pesi e non nel software

**Stato**: accettata
**Data**: 2026-08-15
**Decisione-fonte**: domanda del DM del 2026-08-15 — *«c'è un tool per la
generazione di immagini open source di qualità professionale che possa essere
automatizzato?»* — e la verifica delle licenze che ne è seguita
(`plans/RICERCA-TOOL-ESTERNI-DM-2026-08.md` §3-ter).

## Contesto

Il repo ha già le regole su **cosa** si può chiedere a un generatore: ADR-0005
(confini IP) e ADR-0015 §5 vietano di nominare illustratori viventi e di usare
tavole altrui come style reference. Quelle regole coprono il **prompt**.

Non coprivano il pezzo che nel 2026 conta di più, ed è controintuitivo: **il
software di generazione e i pesi del modello hanno licenze diverse**, e quella che
decide cosa si può fare delle immagini è la seconda.

ComfyUI è GPL-3.0 e non pone limiti su ciò che produce. Ma i pesi:

- **FLUX.1 [dev]** gira sotto *BFL Non-Commercial License v2.0*, che vieta l'uso
  *«non commerciale»* definito in modo largo: esclude ogni uso «direttamente o
  indirettamente connesso ad attività commerciali». Un modulo che un giorno
  potrebbe finire su una piattaforma di vendita **non può** contenere immagini
  fatte con quei pesi;
- **FLUX.1 [schnell]** è **Apache 2.0**: nessuna restrizione d'uso;
- **SDXL** è *OpenRAIL++-M*: uso commerciale ammesso, con restrizioni d'uso
  (use-based) che non toccano il materiale da gioco.

Il rischio concreto: si generano dieci ritratti col modello più bello, si
impaginano, e **un anno dopo** — quando il DM decide di pubblicare — bisogna
rifare tutto perché nessuno ha annotato con cosa erano stati fatti.

## Decisione

### 1. Il modello si sceglie per licenza, poi per qualità

| Pesi | Licenza | Uso nel repo |
|---|---|---|
| **SDXL** | OpenRAIL++-M — commerciale ammesso | ✅ **default**: ecosistema ControlNet/LoRA maturo, gira su 8 GB |
| **FLUX.1 [schnell]** | **Apache 2.0** | ✅ quando serve testo leggibile in-immagine o la garanzia più solida |
| **FLUX.1 [dev]** | Non-Commercial v2.0 | ❌ **vietato** su qualsiasi asset destinato a un artefatto del repo |

La riga da tenere: **se un asset entra in un artefatto versionato, i suoi pesi
devono permettere l'uso commerciale**, indipendentemente dal fatto che oggi il
repo non venda niente. La decisione sul commerciale non è presa (ADR-0005) — e
proprio per questo non va **preclusa** da una scelta tecnica fatta oggi.

### 2. Ogni immagine generata porta la sua riga di provenienza

In `<cartella>/PROVENIENZA.txt`, una riga per file:

```
<file> · <modello e versione> · <licenza dei pesi> · seed <n> · <data> · <chi>
```

Senza quella riga l'immagine **non si committa**. Non è burocrazia: è l'unica
cosa che rende la scelta reversibile fra un anno.

### 3. Le immagini di terzi restano sotto ADR-0005

Questo ADR aggiunge una regola sui **pesi**; non allenta niente su ciò che si può
chiedere. Il divieto di nominare illustratori viventi e di usare immagini altrui
come reference resta identico.

### 4. Chi genera, degrada pulito

Uno script che pilota un generatore **non deve fallire a metà** se il generatore
non c'è: dice quale binario manca, come si installa, ed esce con codice pulito. I
segnaposto vettoriali esistenti restano validi come artefatto consegnabile.

## Conseguenze

- Più facile: la scelta del modello smette di essere una questione di gusto e
  diventa una riga di tabella. E un asset generato oggi è ancora utilizzabile il
  giorno in cui si decidesse di pubblicare.
- Più difficile / rinunce: **si rinuncia al modello con la resa migliore**
  (FLUX.1 [dev]) per una ragione che oggi è ipotetica. **Accettato**: rifare dieci
  immagini costa più che accettare una resa leggermente inferiore adesso.
- Da rivisitare: **quando esce una licenza nuova**, o se il DM decide
  definitivamente per l'uso non commerciale — nel qual caso il §1 si allarga.

## Copertura

- `skills/rumblingstone-art-direction/SKILL.md` §7 — il ciclo, con la provenienza
  come ultimo passo
- [`docs/guides/GUIDA-IMMAGINI.md`](../../docs/guides/GUIDA-IMMAGINI.md) §1 — la
  tabella dei generatori, con la colonna licenza
- [ADR-0015](ADR-0015-standard-prompt-immagine.md) — cosa si può chiedere
- [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) — il perimetro IP generale
