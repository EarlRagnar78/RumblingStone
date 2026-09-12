# `doni-v1-2026-09-12/` — le istantanee di prima del ridisegno dei Tre Doni

## Cos'è

Le **dodici copie congelate** dei file com'erano **prima** del lotto che ha
sostituito i Tre Doni della resurrezione di Hella (`ARC07-DEF-3` §5) con la
versione **v4-bis**, approvata dal DM il **2026-09-12**.

Ogni file porta nel nome il suo percorso originale, con `~` al posto delle
barre: `PG~Artefatti~…~01_Collana_dei_Semi_Eterni.md` stava in
`PG/Artefatti/Artefatti-Pg/Hella/01_Collana_dei_Semi_Eterni.md`.

## 🧊 Non si gioca da qui

Ogni istantanea si apre con un cartello che lo dice, e porta la direttiva
`validate-docs: ignore` perché i suoi link relativi sono **storici**: puntano a
dove stava il file prima e da qui non risolvono. **Non si aggiornano mai**: se
serve correggere qualcosa, si corregge il file vivo.

## Perché esistono, e la cosa scomoda

Le ha chieste il DM (*«tutti i file originali cambiati vanno in archivio»*), e
per il canone narrativo la ragione è buona: al tavolo si vuole poter rileggere
la versione di prima senza passare da `git`.

⚠️ **Ma il repo ha un precedente contrario, e va detto.** Alla decisione **D10**
(2026-09-11) si scelse di **non** copiare i master modificati proprio perché una
copia crea **un secondo master**, e qualcuno prima o poi legge quello sbagliato.
Il rimedio adottato qui è il cartello in testa a ogni file più questo README —
un presidio **umano**, non un cancello: `validate_modules` esclude `_ARCHIVIO`
per costruzione, quindi **nessuno strumento verificherà mai** che queste copie
restino coerenti. È voluto: sono istantanee, devono restare ferme.

## Cosa è cambiato, in una riga per file

| Istantanea | Cosa è cambiato nel file vivo |
|---|---|
| `ARC07-DEF-3-RESURREZIONE-HELLA` | **§5 riscritta** (i Tre Doni), più §0-bis, §7-bis, §9 e §10 allineate |
| `01_Collana_dei_Semi_Eterni` | il potere **#6** non è più `[da definire col DM]`: la restituzione ha una meccanica |
| `00_Collana-SCHEDA-GIOCATORE-STATO-ATTUALE` | i tre doni ricevuti |
| `00_Aegis_Fang-SCHEDA-GIOCATORE-STATO-ATTUALE` | tolta la riga del **«Filo dell'Ascia»**: quella strada non esiste più |
| `00_Aegis_Fang-MASTER-DM` | idem, più la reazione dell'arma alla scelta di Thorik |
| `01_Bracieri_Gemelli_di_Moradin` | **Ancoraggio della Montagna** trapiantato, e la reazione dei Bracieri |
| `00_Ring-SCHEDA-GIOCATORE-STATO-ATTUALE` | **−1d6 di Eldritch Blast**, e la reazione dell'Anello |
| `00_SCHEDA-GIOCATORE-STATO-ATTUALE` (Corona) | **−1 di deflessione**, e l'Eco del Custode |
| `ARTEFATTI-MATRICE-VERSIONI` | l'eco del «Filo dell'Ascia» sostituito |
| `campaign-artifacts` · `campaign-party` | i doni di Hella, che erano ancora quelli di v1 |
| `…FASE0-NOTTE-DEI-DROW-TESTO` | l'eco condizionato non poggia più su *Timeless Body*, che nessuno dona più |

## Cosa **non** è archiviato qui, e perché

- **`campaign/state.md`** — ha già il suo archivio dentro di sé (§8, append-only)
  e la regola del file è di non duplicarlo. La modifica è registrata lì.
- **I mirror per-agente** (`.claude/`, `.chatgpt/`, `.github/copilot/`,
  `.windsurf/`) e **`build/`** — sono **generati** da `skills/`, si rifanno con
  `scripts/build-skills.sh` e non si archiviano (regola già scritta nel README
  del `_ARCHIVIO` padre).
- **I log append-only** (`plans/CHANGELOG.md`) — sono record storici e restano
  intatti dove sono.
