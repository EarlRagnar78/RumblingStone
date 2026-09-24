# ADR-0025 — Il banco di prova di ADR-0016 ha dato esito negativo: la norma si misura

**Stato**: accettata · **riapre e integra**
[ADR-0016](ADR-0016-lingua-sorgente-e-edizioni.md), che resta valida nella decisione
**Data**: 2026-09-02
**Decisione-fonte**: rilievo del tavolo riportato dal DM — *«incoerenza e prosa
inglese tradotta male, anche negli echi»*. Lotto **P** di
[`PIANO-CHIUSURA-CATENA-EDITORIALE`](../PIANO-CHIUSURA-CATENA-EDITORIALE.md).

## Contesto

ADR-0016 si chiudeva con una condizione, e la condizione era scritta bene:

> **Banco di prova**: i prossimi handout. Se i giocatori diranno ancora che
> sembra tradotto, il problema non è la lingua e non è la pipeline — e questa
> ADR va riaperta.

**I giocatori l'hanno detto di nuovo.** Tre date, e vanno lette insieme:

| Data | Cosa è successo |
|---|---|
| **2026-07-31** | I giocatori: *«la prosa sembra tradotta dall'inglese»*. Nasce `italiano-nativo.md` — 274 righe, §1 i dieci calchi, §9 i tic dell'IA |
| **2026-08-01** | ADR-0016: l'italiano è la lingua sorgente; il rimedio è la qualità, non la lingua; il banco di prova sono i prossimi handout |
| **2026-09-02** | I giocatori lo dicono **ancora**, e aggiungono *«anche negli echi»* |

Fra la prima data e la terza c'è un motore di stile da **2047 righe**. Quindi
l'ipotesi «manca la norma» è falsificata: la norma c'è, è dettagliata, ed è
esatta. Quello che mancava è **la misura** — e una norma che nessuno misura è
un'intenzione.

Verificato prima di scrivere questo: `grep -ril "traduttese\|calco" scripts/` non
trovava niente. Nessuno strumento del repo guardava la prosa.

## Decisione

**La decisione di ADR-0016 resta**: l'italiano è la lingua sorgente, l'inglese
è un'edizione derivata, e non si costruisce adesso. Il rilievo dice che la
qualità non basta, **non** che serva l'inglese.

Cambiano tre cose.

### 1. La norma si legge PRIMA di scrivere, non prima di consegnare

`italiano-nativo.md` era al punto **5** del load order, «obbligatorio prima di
consegnare». Passa al punto **4**, «prima di scrivere», e la checklist di 30
secondi resta come ultima passata.

Il motivo non è formale. **Il traduttese non è una lista di errori da correggere
in revisione: è il modo in cui la frase è stata costruita.** Se si scrive con la
testa in inglese e poi si correggono i dieci calchi che la lista nomina, restano
la sintassi, il ritmo e l'ordine delle informazioni — che sono esattamente ciò
che un lettore sente. Correggere dopo cambia le parole e lascia il respiro.

### 2. Nasce `scripts/validate_prosa.py`

Non per sostituire la lettura umana: per **togliere il rumore** perché la
lettura veda il resto. Misura tre cose che una macchina misura meglio di un
revisore stanco:

- **i calchi a firma inequivocabile** (`realizzi che`, `assumi che`,
  `eventualmente`, la nominalizzazione) — sempre;
- **il possessivo sulle parti del corpo e il progressivo**: **solo nel
  read-aloud**, perché dipendono dal registro: *«sta piovendo»* è italiano
  corretto, e segnalarlo ovunque produceva **256 rilievi** alla prima passata,
  quasi tutti legittimi. Con lo split: 110;
- **i tic a densità**, l'antitesi «non X: è Y» massimo una per documento, le
  maiuscole di portento massimo una, i trattini lunghi. ⭐ È il pezzo che vale
  di più: *«massimo uno per documento»* è la regola che un revisore umano non
  applica mai, perché dovrebbe **contare**;
- **la forma inglese di un nome che il glossario vuole tradotto**: *Anvil of
  the World* dove il canone dice *Incudine del Mondo*: trovata in **15 file**,
  ed è il rilievo del tavolo nella sua forma più letterale.

⚠️ **Non bloccante alla prima passata** (`continue-on-error`), come
`validate_bestiario --rules` e `validate_lingua`. Un validatore rumoroso viene
disattivato entro una settimana, e allora non trova più nemmeno i rilievi veri.

### 3. Gli echi sono testo, non note

Il tavolo li ha nominati. `passate-redazionali.md` lo scrive esplicitamente: gli
echi si saltano nella revisione perché sembrano appunti, e invece i giocatori li
**leggono**.

## Conseguenze

- **Più facile**: il rumore meccanico esce da solo, e la 2ª passata umana — la
  lettura ad alta voce — vede il ritmo invece dei refusi.
- **Più difficile / rinuncia**: un validatore trova *«realizzi che»*; **non**
  trova una scena che suona tradotta pur essendo in italiano corretto. Quella
  resta lavoro umano, e questo ADR non finge il contrario.
- **Il nuovo banco di prova**: i prossimi handout, di nuovo — ma stavolta con un
  numero. Se `validate_prosa` scende e i giocatori dicono ancora che sembra
  tradotto, allora il problema non è nei calchi né nei tic, ed è **la voce**:
  a quel punto si guarda `style-pillars.md`, non `italiano-nativo.md`.
