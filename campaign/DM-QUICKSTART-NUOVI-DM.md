# 🚀 Quick Guide — Nuovo DM su RumblingStone

> **Per chi è**: un DM che parte da zero con questa campagna (D&D 3.5,
> Forgotten Realms 1372 DR, adattamento di *Red Hand of Doom*) e vuole
> usare tutti gli strumenti del repo senza leggersi prima tutto.
> Tempo per essere operativi: **~15 minuti**.
>
> Approfondimenti: [`DM-CAMPAIGN-PLAYBOOK.md`](DM-CAMPAIGN-PLAYBOOK.md)
> (manuale operativo completo) · [`DM-QUICKSTART-ARC09.md`](DM-QUICKSTART-ARC09.md)
> (ingresso all'arco corrente) · `scripts/README-automation.md` (tool map
> di tutti gli script) · `plans/INDEX.md` (roadmap) · `plans/adr/` (le
> decisioni architetturali e i loro perché).

---

## 1. I 3 concetti da capire subito

1. **`main` è la libreria, il tuo branch è la partita.** Archi (cartelle
   `00_`-`09_`), Bestiario, mappe e script vivono su `main` e servono a
   qualsiasi gruppo. Il *tuo* canone vivo (stato del mondo, log delle
   sessioni) vive su un branch dedicato `campaign-group-<tuo-nome>` che
   **non si mergia mai** in `main` (ADR-0007).
2. **`campaign/state.md` è la verità.** Se un file di lore dice una cosa
   e `state.md` un'altra, vince `state.md`. Si aggiorna a fine sessione —
   in parte in automatico (vedi §4), in parte a mano.
3. **Il markdown è il master, il "bello" si genera.** Recap eleganti,
   booklet e handout in stile Manuale del Giocatore sono `.hb.md`
   generati (Homebrewery V3): si rigenerano con gli script, mai editati a
   mano (ADR-0003).

## 2. Setup una-tantum (5 min)

```bash
git clone <repo> && cd RumblingStone
python3 scripts/dm.py doctor          # diagnosi: ti dice cosa manca
python3 scripts/dm.py session branch --group mario-rossi
#   → crea il branch campaign-group-mario-rossi + campaign/group.yaml
python3 scripts/state_apply.py --migrate --commit
#   → inserisce i marker `auto:` in state.md (una volta sola)
```

Poi apri `campaign/state.md` §1 e metti i TUOI PG (o parti dallo stato
del gruppo di esempio per continuare la campagna dal punto attuale).
Per un reset completo da template c'è `scripts/new-campaign-group.sh`
(Playbook §7).

## 3. Prima della sessione (15 min)

```bash
python3 scripts/dm.py session next --hype   # brief DM + teaser player
python3 scripts/dm.py prep --el 13 --env forest   # incontri + mappa + loot proposti
python3 scripts/dm.py maps render <file.md>       # SVG "pergamena" delle griglie
```

- Il **brief DM** (`campaign/next/brief-*-DM.md`) ti dice: finestre di
  quest che scadono, dove sono i PG, clock villain a un passo dalla
  soglia, hook aperti. ⚠️ Solo per te.
- Il **teaser player** (`teaser-*-PLAYERS.md`) è spoiler-safe: giralo al
  gruppo così arrivano carichi.
- Le proposte di `prep` NON scrivono niente: scegli tu cosa usare.

## 4. Dopo la sessione (10 min)

1. Compila il log da template:
   `cp campaign/templates/session-template.md campaign/sessions/$(date +%F)_session-N.md`
   — le sezioni sono guidate (XP, loot, `## World events triggered`,
   hook). La sezione `## DM notes (private)` non finirà MAI nei recap.
2. ```bash
   python3 scripts/dm.py session end --session $(date +%F)_session-N.md
   ```
   Fa da solo, sul tuo branch (mai su `main`): ledger XP → diff dei
   cambi meccanici di `state.md` (March Clock, changelog §8) → **te li
   mostra e applica solo se confermi** → commit. I cambi non meccanici
   (prosa, PNG morti, alleanze) restano stampati come proposte: applicali
   a mano (Playbook §4.2-4.3).
3. `git push -u origin campaign-group-<tuo-nome>` — il tuo canone è al sicuro.

## 5. Tra una sessione e l'altra

```bash
python3 scripts/dm.py recap --hype    # recap R.A. Salvatore + veste Homebrewery
python3 scripts/dm.py dossier         # ⚠️ SOLO DM: tutte le trame in un fascicolo
python3 scripts/dm.py handout --tipo lettera --da bozza.md   # handout ai PG
python3 scripts/dm.py hype docker     # Homebrewery locale su localhost:8000
```

Gli `.hb.md` si incollano su Homebrewery (locale o naturalcrit.com) e
vengono fuori pagine da manuale. L'indice cronologico degli handout è
`campaign/recaps/homebrew/00-CRONOLOGIA.hb.md`.

## 6. Igiene del branch (1 min a settimana)

```bash
python3 scripts/dm.py session status   # dove sono? sono indietro rispetto a main?
git merge main                         # porta nel tuo branch i nuovi materiali di prep
```

Se `session status` avvisa che sei indietro di molti commit, fai il merge:
`main` evolve (statblock, mappe, fix agli script) e il tuo branch li
eredita così. Mai il contrario: niente merge del tuo branch in `main`.

## 7. Dove sono le cose (mappa mentale)

| Cosa cerchi | Dove |
|---|---|
| Stato del mondo (verità corrente) | `campaign/state.md` |
| Log sessioni / template | `campaign/sessions/` · `campaign/templates/` |
| Brief/teaser prossima sessione | `campaign/next/` |
| Recap + handout generati | `campaign/recaps/` (+ `homebrew/`) |
| Avventure per arco | cartelle `00_…` → `09_…` (con `homebrew/` per i booklet) |
| Mostri / villain / PNG | `Bestiario/` (validato da `validate_bestiario.py`) |
| Schede e artefatti dei PG | `PG/` |
| Regole della casa / lore | `campaign/lore/` |
| Tutti gli script (tool map) | `scripts/README-automation.md` |
| Roadmap e decisioni | `plans/INDEX.md` · `plans/adr/` |

## 8. Regole d'oro (non negoziabili)

1. **Mai scrivere canone su `main`** — gli script te lo impediscono
   (guardia ADR-0007), non aggirarli.
2. **Mai editare gli `.hb.md` a mano** — si rigenerano (ADR-0003).
3. **Mai inventare numeri** — XP/statblock/loot vengono solo da ciò che
   è scritto nei file o marcato `[INFERRED]` (AGENTS.md).
4. **In dubbio**: `python3 scripts/dm.py doctor` prima, poi il Playbook.
