# ADR-0021 — I numeri delle schede sono un dato, non una frase

**Stato**: accettata *(mandato del DM del 2026-08-22: «E8 ok, risolvi tutti i bug
e inserisci tutti gli enhancement rilevati dall'audit»)*
**Data**: 2026-08-22
**Decisione-fonte**: `plans/RICERCA-AUDIT-COMPONENTI-E-LIVELLO-EDITORIALE-2026-08.md`
§3 («il pezzo grosso: gli statblocchi come dato») e §6 lotto E8.

## Contesto

`Bestiario/` contiene **157 schede**. I numeri — CA, pf, TS, attacchi, GS — vivono
dentro frasi italiane:

> `Small plant, 4d8+16. **hp 34**; **AC 15** (+1 taglia, +4 naturale), touch 11 … TS Temp +6, Rifl +1, Vol +2.`

Si legge benissimo al tavolo. Non si può usare per nient'altro, e le conseguenze
erano tutte già visibili:

- `scripts/monster_catalog.yaml` ha **312 record** che contengono solo
  `id/nome/gs/fazione/ruolo/ambiente/file`: è un **indice**, non una scheda;
- in stampa un mostro non può diventare un riquadro, perché nessuno sa quale
  numero è quale — il divario **R2** dell'audit era bloccato qui;
- `suggest_encounter.py` bilancia sul GS **dichiarato** e non può verificarlo
  contro i numeri reali;
- l'export UVTT porta a Foundry muri e luci, e **non i mostri**;
- un errore di trascrizione (un `+7` diventato `+1`) non è rilevabile da nessun
  gate: sopravvive fino al tavolo.

## Decisione

**Un blocco recintato in testa alla scheda, coi soli campi meccanici. La prosa
resta dov'era.**

````markdown
# Myconid Worker (operaio) [TRANSCRIBED — …]
**Faction**: aberration | **Role**: fodder | **CR**: 2 | …

```statblocco
gs: 2
tipo: Small plant, 4d8+16
ca: 15
ca-dettaglio: contatto 11, colto alla sprovvista 15 (+1 taglia, +4 naturale)
pf: 34
pf-dado: 4d8+16
ts: Temp +6, Rifl +1, Vol +2
velocita: 6 m
attacchi:
  - Mischia schianto +5 (1d4+1)
voci:
  - Talenti: Allerta, Resistenza Fisica
```

Small plant, 4d8+16. **hp 34**; **AC 15** …
````

### 1. Perché dentro il master e non in un file a parte

Vale [ADR-0003](ADR-0003-markdown-master-layout-generati.md): il markdown è la
verità. Un `Bestiario/dati/*.yaml` parallelo sarebbe **una seconda copia degli
stessi numeri**, e due copie divergono sempre — è la lezione che il repo ha già
pagato con le schede pregenerate del Drappo, dove i dati stanno nei master del
tavolo e il layout li legge di lì.

### 2. Perché un YAML minuscolo e non JSON

`chiave: valore` più liste con `- `, e nient'altro. Sta in venti righe di parser
stdlib (`scripts/dmcore/statblock.py`), si legge a occhio dentro il file, e non
costringe chi scrive una scheda a contare le graffe. Il contratto è dichiarato
una volta sola in `scripts/schemas/statblock.schema.json`.

### 3. La migrazione non inventa

`scripts/extract_statblocks.py` ricava il blocco dalla prosa e lo scrive **solo
dove l'estrazione è completa**: 82 schede su 157 alla prima passata. Le altre 75
finiscono in un rapporto con scritto quale campo manca.

È la stessa disciplina di `import_ultraclear.py` per le mappe — bozza più
rapporto dei conflitti — e per la stessa ragione: **una scheda migrata a metà,
con un numero dedotto, è peggio di una scheda non migrata**. Al tavolo ci si fida
di quello che c'è scritto.

### 4. Il gate

`extract_statblocks.py --check` gira in CI e verifica tre cose:

1. ogni blocco presente **si legge** (campo sconosciuto = errore, non silenzio);
2. ci sono i campi obbligatori (`gs`, `ca`, `pf`, `ts`);
3. il **GS del blocco coincide con quello del nome del file** (`-crN.md`) — che è
   il modo tipico in cui una scheda potenziata resta indietro. Alla prima
   esecuzione ha trovato subito due casi.

## Conseguenze

- Più facile: il riquadro-mostro in stampa (`#statblocco()` nel tema), la verifica
  del GS, l'arricchimento del catalogo, e domani i mostri nell'export UVTT.
- Più difficile / rinunce: **due posti dove vive lo stesso numero dentro la stessa
  scheda** — il blocco e la prosa. È il prezzo di non riscrivere 157 schede in una
  volta. Mitigazione dichiarata: il blocco è la fonte per gli script, la prosa è la
  fonte per l'occhio, e se un giorno divergono vince il blocco, perché è quello che
  un gate può controllare.
- **Non** si è imposto il blocco a tutte le schede: 75 restano senza, e la libreria
  funziona lo stesso. Un formato obbligatorio su file che nessuno ha tempo di
  convertire diventa un gate spento.
- Da rivisitare: quando le schede migrate superano il 90%, si può valutare di
  **generare** la riga di prosa dal blocco invece di tenerne due — a quel punto la
  rinuncia qui sopra si chiude da sola.

## Copertura

- `scripts/dmcore/statblock.py`: lettura, estrazione dalla prosa, forma canonica
- `scripts/extract_statblocks.py`: migrazione semi-automatica e gate `--check`
- `scripts/schemas/statblock.schema.json`: il contratto dei campi
- `scripts/typst/tema-rumblingstone.typ`: `#statblocco()`, il riquadro in stampa
- `scripts/export_booklet_typst.py`: il blocco diventa riquadro, non codice
- `scripts/tests/test_statblock.py`: 12 test, fra cui i dadi vita che non sono i
  dadi di danno e il mezzo grado di sfida
- `.github/workflows/ci.yml`: il gate
