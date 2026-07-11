# DM Campaign Playbook — RumblingStone Operational Guide

**Scopo**: questo file è il **manuale operativo del DM**. Risponde a tre domande pratiche:

1. Cosa leggo **prima** di ogni sessione?
2. Cosa aggiorno **durante** la sessione?
3. Cosa committo **dopo** la sessione?

Inoltre spiega come **resettare la campagna per un nuovo gruppo** senza perdere il materiale di preparazione (archi 00-09, PNG, skills, mappe).

> Se vuoi solo continuare la campagna attuale → leggi §2, §3, §4, §5.
> Se vuoi far partire un nuovo gruppo senza perdere niente → salta a §7.

---

## §1 — Mental Model: i 3 livelli di stato

Il repo ha tre **livelli** di contenuto. Trattarli allo stesso modo è la fonte n°1 di caos.

| Livello | Cosa c'è | Quando si modifica | Chi lo modifica |
|---|---|---|---|
| **Canonico** (immutabile) | `skills/*`, AP originale RHoD, SRD D&D 3.5, FR 1372 DR lore, `00_Red Hand Of Doom/` (canone di riferimento) | Mai (o raro, con changelog) | Solo DM, in PLAN MODE, mai a tavolo |
| **Scenario** (semi-fisso) | Cartelle arco `01_LaMiniera/ … 09_Continuazione/`, `campaign/lore/`, `Bestiario/{villain,png}/**/*.md` (stat blocks, backstory), encounter files | Tra sessioni, in PLAN MODE | DM in preparazione |
| **Vivo** (per sessione) | `campaign/state.md`, `campaign/sessions/*.md`, status attuale PNG | **Ogni sessione** | DM a fine sessione |

**Regola d'oro**: non modificare MAI contenuto canonico o di scenario durante la sessione live. Tienilo per il post-session in calma.

---

## §2 — Pre-session checklist (15 min prima del tavolo)

Apri i file in questo ordine:

| # | File | Cosa cerchi | Tempo |
|---|---|---|---|
| 1 | `campaign/state.md` §0 | Cruscotto: arco attivo, fase, March Clock, PG Lv | 1 min |
| 2 | `campaign/state.md` §2-§3 | Clock attuali + villain clock | 2 min |
| 3 | `campaign/state.md` §5 | Posizione party + risorse + hook personali | 2 min |
| 4 | `campaign/state.md` §7 | Open narrative threads attivi | 1 min |
| 5 | `campaign/sessions/ultima-sessione.md` | Sezione **Next session hooks** | 2 min |
| 6 | File dell'arco corrente (es. `09_.../Arco-Post-Hammerfist-P1B-...`) | Fase attiva, encounter previsti | 3 min |
| 6b | (opz.) `python3 scripts/dm.py prep --el <N> --env <X>` | Encounter+mappa+loot proposti in un colpo solo (orchestra suggest_encounter/map/loot; `dm.py doctor` se qualcosa non torna) | 3 min |
| 7 | `Bestiario/{villain,png}/<nome>/<nome>.md` (PNG in scena previsti) | Motivazione + segreti + stato | 2 min |
| 8 | `skills/rumblingstone-campaign/references/campaign-coherence.md` | Solo se vuoi rivedere regole coerenza | 2 min |

**Optional ma utile**: apri `campaign/lore/house-rules.md` se prevedi ruling ambigui.

### §2.1 — Regola d'oro anti-rigenerazione (Bestiario)

Prima di **creare** stat per un mostro/PNG/villain di un incontro o di una
quest, **cerca se esistono già** — quasi sempre è così:

1. `python3 scripts/suggest_encounter.py --list-npcs` (elenca i PNG canonici di
   `Bestiario/{villain,png}/` + le voci del catalogo con nome);
2. o cerca nel catalogo: `grep -i "<nome>" scripts/monster_catalog.yaml` →
   la riga `source_file:` ti porta alla scheda;
3. per famiglia/CR sfoglia `Bestiario/mostri/` (unità generiche, `nome-crN.md`),
   `Bestiario/villain/` (antagonisti unici), `Bestiario/png/` (alleati unici);
4. se esiste solo come sorgente storica in `Bestiario/pregen-pcgen/`, **trascrivila**
   nel formato standard (non reinventarla): vedi `Bestiario/README.md`.

**Genera ex-novo solo se non esiste da nessuna parte**, col
`campaign/templates/png-dossier-template.md`, flag `[INFERRED — needs DM
confirmation]` e — se è un potenziamento — via `skills/npc-villain-boosting/`
con `Boost log:`. Riusare una scheda esistente è sempre preferibile a clonarne
i numeri in un file d'incontro.

---

## §3 — During-session: live tracker leggero

**Non modificare file grossi al tavolo.** Usa un file scratch temporaneo:

📄 `campaign/sessions/_draft-in-corso.md`

Template minimale (6 campi):

```markdown
# Session N — DRAFT in-progress (YYYY-MM-DD)

## Live log
- [HH:MM in-world] evento chiave 1
- [HH:MM] evento chiave 2
- ...

## Clock ticks
- March Clock: Day X → Day Y (+Z)
- Ritual Clock Azarr Kul: n/n → n+1/18 (se triggerato)
- Villain clocks toccati: [Sonjak 4→5, Sal 0→1, ...]

## PG snapshot (fine sessione)
- Thorik: HP 78/120, spell slot 3/5, ...
- Tordek: HP full, bracieri ready, ...
- Hella: HP full, Treant form 1/day used, ...
- Artemis: HP 55/98, spell slot 4/6 + 2/4, ...

## Decisioni chiave
- PG sceglie di X invece di Y (perché...)

## Loot raccolto
- item 1 → PG
- ...

## Nuovi hook emersi
- ...

## XP sessione (calcolo finale)
- encounter 1: CR X → YYY xp / 4 = ZZZ a testa
- ...
```

**Tip**: tienilo aperto in uno split screen accanto al tuo schermo DM. Scrivi a sassolini durante i momenti di pausa (iniziativa, spostamenti, roleplay lungo).

---

## §4 — Post-session: commit workflow (10 min)

Quando il gruppo va a casa, esegui questi 5 passi nell'ordine.
**Scorciatoia**: `python3 scripts/dm.py post` aggiorna il ledger XP,
**propone** il diff di state.md (il 4.2 resta manuale) e stampa la
checklist rimanente.

### 4.1 Rinomina il draft

```bash
cd /home/jfs/00_Antigravity_workspace/RumblingStone
mv campaign/sessions/_draft-in-corso.md "campaign/sessions/$(date +%Y-%m-%d)_session-N.md"
```

Apri il file appena rinominato e **completalo** nel formato canonico (vedi §4.bis worked example).

### 4.2 Aggiorna `campaign/state.md`

Applica cambi **chirurgici** a queste sezioni:

- **§0 Status At-a-Glance** — aggiorna arco attivo / fase / March Clock / PG Lv
- **§2.1 March Clock** — avanza "Current March Day" di N giorni
- **§3 Villain Clocks** — avanza clock dei villain toccati
- **§5 Party Position** — nuova location + risorse attuali
- **§6 World Events Log** — aggiungi nuovo blocco datato
- **§8 Changelog** — entry in fondo con data e one-liner

Vedi §4.ter per diff worked example.

### 4.3 Aggiorna PNG status cambiati

Solo se un PNG è morto / cambiato allineamento / cambiato posizione:

```bash
# esempio: Regiarix ucciso
sed -i 's/Status: alive/Status: dead (killed session 14)/' Bestiario/villain/Regiarix/Regiarix.md
```

### 4.4 Aggiorna encounter files (opzionale)

Se un encounter è stato "consumato" e potrebbe riemergere (es. imboscata replicabile), aggiungi nota in `campaign/encounters/...`.

### 4.5 Commit & push

```bash
git add -A
git commit -m "Session N: <titolo one-line>"
git push origin main   # oppure il tuo branch-gruppo (vedi §7)
```

**Fatto.** Lo stato è consolidato. Alla prossima sessione §2 ti riporta esattamente qui.

### 4.6 — Recap per i player (1-2 giorni prima della prossima sessione)

Genera un preludio/recap in italiano, **spoiler-safe**, con tono R.A. Salvatore,
da mandare ai giocatori via chat prima della prossima sessione per tenere
viva l'epica della campagna.

```bash
# Solo markdown (campaign/recaps/recap-YYYY-MM-DD.md)
python3 scripts/dm.py recap

# In più la versione HYPE in stile Manuale del Giocatore — pronta da
# incollare su homebrewery.naturalcrit.com (recaps/homebrew/*.hb.md)
python3 scripts/dm.py recap --hype

# Con PDF A4 (richiede pandoc + xelatex installati)
python3 scripts/dm.py recap --pdf

# Ultime 2 sessioni se il gruppo ha saltato una settimana
python3 scripts/dm.py recap --last-n 2
```

*(equivalenti diretti: `python3 scripts/session_recap.py …` — dm.py
orchestra e basta. Per gli handout in-game: `dm.py handout --tipo
lettera|profezia|avviso-torneo|scheda-artefatto --da <file canone>`.)*

**Cosa fa**:

- Legge gli ultimi N file `campaign/sessions/*.md` + `campaign/state.md`.
- Estrae **solo** `Summary`, `Key decisions`, `XP awarded`, `Loot distributed`,
  `World events triggered`, `Next session hooks`.
- **Taglia automaticamente** tutto ciò che segue `## DM notes (private — optional)`.
- Dal dashboard `§0` di `state.md` include solo righe ✅ (completato) e
  🟡 (in corso); le righe ⬜ (archi futuri non rivelati) sono filtrate.
- Produce 6 sezioni in prosa evocativa italiana: *Il Respiro del Mondo*,
  *Dove siete in questo istante*, *Negli episodi precedenti*, *Il mondo
  attorno a voi*, *Sussurri nel vento*, *La prossima alba*.
- Output deterministico (nessun LLM): template curati. Usa `--seed N` per
  rigenerare output identico, oppure nessun seed per variare la prosa.

**Regola d'oro prima di inviare**: dai uno sguardo al `.md` prodotto.
Se vedi qualcosa che i player non dovrebbero sapere ancora, è perché
l'hai scritto **sopra** la linea `## DM notes` nel session log — spostalo
sotto e rigenera.

---

## §4.bis — Worked Example: file di sessione

Ecco un esempio completo. Immagina che nella sessione 14 il party completi la Quest Hellas (Arc-09 P1A), uccida un razorfiend di ricognizione, e avanzi March Clock di 2 giorni.

📄 `campaign/sessions/2026-05-12_session-14.md`

```markdown
# Session 14 — Il Cerchio Sacro di Hellas (2026-05-12)

**Players present**: Artemis (Tordek PG1), Luca (Hella PG3), Marco (Thorik PG2), Giulia (Maewen PG4)
**Location**: Shaarcah Forest, radura del Cerchio Treant
**In-world dates**: dal Day 27 al Day 29 del March Clock
**Session XP budget**: CR 13 target (party avg level 13)

## Summary

I PG raggiungono il Cerchio Sacro dopo l'imboscata dei worg rider. Hellas completa il rituale di
comunione con Silvanus (CD 22 Knowledge Nature — riuscito al 3° tentativo, 2 ore in-game),
ottenendo l'alleanza dei **druidi-orsi mutaforma** (vedi
`Arco-Post-Hammerfist-P1B-Cerchio-Treant-COMPLETO.md` §3).

Scontro imprevisto: un razorfiend di ricognizione intercetta il party mentre lasciano il Cerchio.
Tordek lo finisce con un critico di +3 greataxe di Moradin. Nessun PG giù.

## Key decisions

- Hellas ACCETTA il patto con Silvanus → ora è Druid 12 / Hierophant 1 (trigger livello 13 ritardato)
- Party decide di NON tornare a Rethmar subito → prosegue verso Lhesper (P2 Rhest) invece
- Maewen rivela backstory sul padre elfico → potenziale hook Tiri-Kitor per P3

## XP awarded

- Razorfiend ricognitore CR 10 → 3.000 xp / 4 = 750 xp a testa
- Cerchio Treant (ritualistic challenge CR 12) → 4.500 xp / 4 = 1.125 xp a testa
- **Total**: 1.875 xp a testa (nessun level up questa sessione)

## Loot distributed

- Anello di Resistenza Elementale +2 (fuoco) → Hella
- 2× pozione Cure Serious Wounds → Tordek, Thorik
- 340 gp in moneta druidica convertibile a Rethmar

## World events triggered

- **March Clock**: Day 27 → Day 29 (+2)
- **Ritual Clock Azarr Kul**: nessun avanzamento (PG non hanno interagito)
- **Hellas alleanza druidi-orsi**: CONFERMATA → +150 druidi-orsi alla difesa Fase 1-2 di Rethmar
- **Regiarix**: ancora vivo (P2 non completato)
- **Ghostlord**: status immutato (ancora nemico)

## Next session hooks

- Approccio a Lhesper dalla Shaarcah Forest occidentale (1 giorno di marcia)
- Saarvith + Regiarix boss fight incombente
- Corriere in arrivo da Rethmar con messaggio del Consiglio (timing Day 31)
```

---

## §4.ter — Worked Example: diff `campaign/state.md`

Sempre sessione 14. Il DM apre `state.md` e applica questi cambi (mostrato come `diff`):

```diff
 ## §0 Campaign Status At-a-Glance

 | Arc | Fase | Stato | March Clock | PG Lv |
 |---|---|---|---|---|
-| 09 P1A Hellas | 🟡 in corso | Day 27 | 13 |
+| 09 P1A Hellas | ✅ completato | Day 29 | 13 |
-| 09 P2 Rhest | ⬜ non iniziato | — | — |
+| 09 P2 Rhest | 🟡 approccio | Day 29 | 13 |

 ## §2.1 March Clock

-**Current March Day:** 27
+**Current March Day:** 29
-**Last session end:** 2026-04-28 (Session 13)
+**Last session end:** 2026-05-12 (Session 14)

 ## §3 Villain Clocks

-| Saarvith + Regiarix | 3/8 | Day 27 |
+| Saarvith + Regiarix | 4/8 | Day 29 (Regiarix ancora vivo, sposta in campo) |

 ## §5 Party Position

-**Location**: Shaarcah Forest (margini ovest, verso Cerchio)
+**Location**: Shaarcah Forest occidentale, in marcia verso Lhesper
-**Last rest**: Day 26 extended rest
+**Last rest**: Day 28 extended rest (post-ritual)
 **Resources**: spell slot 70%, HP avg 85%

 ## §6 World Events Log

+### Day 29 — Cerchio Sacro completato (Session 14)
+- Hellas patto Silvanus → Hierophant 1
+- Alleanza druidi-orsi mutaforma confermata (+150 unità Fase 1-2 Rethmar)
+- Razorfiend ricognitore eliminato in Shaarcah Forest
+
 ### Day 19 — Battaglia di Hammerfist (locked sync)

 ## §8 Changelog

+2026-05-12  Session 14: Cerchio Sacro Hellas completato. Day 27→29. Alleanza
+            druidi-orsi confermata (+150 Rethmar difese). Regiarix ancora vivo.
+            Next: approccio a Lhesper per P2.
```

E poi:

```bash
git add -A
git commit -m "Session 14: Cerchio Sacro Hellas completato, Day 27->29, druidi-orsi alleati"
git push
```

Questo è il **pattern ripetibile** per ogni sessione. Una volta fatto 2-3 volte diventa muscolo memoria (~10 minuti totali).

---

## §5 — Campaign Status At-a-Glance (dashboard)

Apri `campaign/state.md` §0 per vedere il cruscotto in tempo reale. Template:

| Arc | Fase | Stato | March Clock | PG Lv | Note |
|---|---|---|---|---|---|
| 00 Setup RHoD | ✅ | completato | Day 0 | 5 | — |
| 01 Miniera | ✅ | completato | — | 6 | — |
| 02 Scaladossa | ✅ | completato | — | 7 | — |
| ... | ... | ... | ... | ... | ... |
| 08 Hammerfist | ✅ | completato | Day 19 | 12 | Sync point ✓ |
| 09 P1A Hellas | 🟡 | in corso | Day 27 | 13 | Deadline Day 30 |
| 09 P2 Rhest | ⬜ | non iniziato | — | — | Regiarix vivo |
| 09 P3 Rethmar | ⬜ | non iniziato | Target Day 40 | — | Battaglia finale |

**Legenda**: ✅ completato · 🟡 in corso · ⬜ non iniziato · ❌ fallito · ⏸ sospeso

---

## §6 — Dual Clock — Quick Reference

Riassunto operativo di `campaign-coherence.md` §5.2/§5.2.bis:

### March Clock (deterministico)

- **Tick +1** per ogni giorno in-world che passa (anche se i PG non fanno nulla / sessione off-screen)
- Gira **Day 1 → Day 40**
- Eventi **locked** (non toccare mai):
  - Day 5: PG non interferiscono a Skull Gorge ✓
  - **Day 19**: Terrelton cade = fine Battaglia di Hammerfist (sync)
  - Day 40: Orda arriva a Rethmar

### Ritual Clock Azarr Kul (indipendente)

- Gira `/18`
- **Tick +1 SOLO** se: (a) PG causano ritardo rituale, (b) Azarr Kul esegue uno step rituale, (c) evento Rethmar-specifico
- NON avanza coi giorni di marcia dell'Orda

### Villain Clocks individuali (`/N`)

- Ogni villain in `state.md §3` ha il proprio clock
- Avanzano per azione del villain, non per tempo che passa
- Quando si riempie → trigger della conseguenza elencata

---

## §7 — Reset per nuovo gruppo (mantenendo tutto il resto)

Il materiale di preparazione (archi, PNG, skills, stat block, mappe) è **riutilizzabile all'infinito**. Solo lo stato vivo va resettato. Strategia: **un branch git per gruppo**.

### 7.1 Backup del gruppo attuale

```bash
cd /home/jfs/00_Antigravity_workspace/RumblingStone
git checkout main

# crea un branch dedicato al gruppo corrente (snapshot eterno)
git checkout -b campaign-group-<nome-gruppo>
git push -u origin campaign-group-<nome-gruppo>
```

**Da ora in poi** il branch `campaign-group-<nome-gruppo>` conserva per sempre la storia di quella campagna.

### 7.2 Reset lo stato vivo su main (o crea nuovo branch)

Opzione A — **Reset su main** (raccomandato se vuoi che main ospiti il "prossimo" gruppo):

```bash
git checkout main

# resetta solo i file di stato vivo
rm -f campaign/sessions/*.md
cp campaign/templates/state-blank.md campaign/state.md

# facoltativo: resetta status nei PNG (se li hai modificati)
# (lo script new-campaign-group.sh lo fa automaticamente)

git add -A
git commit -m "Reset: pronti per nuovo gruppo"
git push origin main
```

Opzione B — **Nuovo branch per nuovo gruppo** (raccomandato se vuoi main come "template pulito"):

```bash
git checkout main
git checkout -b campaign-group-beta
cp campaign/templates/state-blank.md campaign/state.md
rm -f campaign/sessions/*.md
git add -A
git commit -m "Campaign group beta: session 0"
git push -u origin campaign-group-beta
```

Poi per switchare tra gruppi: `git checkout campaign-group-alpha` ↔ `git checkout campaign-group-beta`.

### 7.3 Prima sessione del nuovo gruppo

1. Apri `campaign/state.md` (ora vuoto)
2. Compila §1 Party con nuovi PG (nomi, classi, livello 5 partenza)
3. Imposta §2.1 March Clock a Day 0
4. Imposta §3 Villain Clocks a 0/N su tutti
5. Gioca la prima sessione
6. Applica workflow §4

### 7.4 Helper script

Esiste (o va creato): `scripts/new-campaign-group.sh` che automatizza 7.1 e 7.2 in un comando solo. Vedi `scripts/README.md`.

---

## §8 — Red Flags — cosa NON fare

| ❌ | ✅ |
|---|---|
| Modificare file di arco (`09_.../*.md`) durante la sessione | Solo appunti nel draft; modifiche scenario in PLAN MODE tra sessioni |
| Committare senza aggiornare `state.md` | `state.md` **deve** riflettere l'ultimo stato prima del commit |
| Modificare `00_Red Hand Of Doom/` originale (AP canon) | Se serve una variante, crea file adattamento in `campaign/lore/rhod-adaptations.md` |
| Tenere lo stato di campagna "nella testa" | Tutto deve stare in `state.md` — alla 20ª sessione non ricordi dettagli del Day 14 |
| Dimenticare il changelog in §8 | Un one-liner sempre, anche per cambi piccoli |
| Far "rivelare" a un PNG qualcosa che non ha mai imparato in-fiction | Controlla `state.md §4 Open NPC Knowledge State` prima |
| Usare artefatti one-shot già spesi (es. Ruby Gem, Cuore di Moradin) | Controlla `state.md §6 Artifact State` — one-shot marked 🔥 |
| Modificare regole RAW senza mettere in `house-rules.md` | House rules sempre documentate |
| Lasciare più di 1 sessione senza commit | Rischio di dimenticare cosa è successo — sempre commit entro 24h dalla sessione |

---

## §9 — Riferimenti veloci

- **Coerenza canoniche**: `skills/rumblingstone-campaign/references/campaign-coherence.md`
- **Regole d'adattamento RHoD**: `campaign/lore/rhod-adaptations.md` (se esiste) + `campaign/lore/house-rules.md`
- **DM strategy meta**: `skills/rumblingstone-campaign/references/campaign-dm-strategy.md`
- **Toolkit espansione**: `skills/rumblingstone-campaign/references/dm-expansion-toolkit.md`
- **Fazioni FR**: `skills/forgotten-realms-lore/references/fr-factions.md`
- **Cannath Vale mappa**: `skills/forgotten-realms-lore/references/fr-cannath-vale.md`
- **AP originale**: `00_Red Hand Of Doom/` (read-only canon)
- **DM Quickstart Arc-09**: `campaign/DM-QUICKSTART-ARC09.md` (indice di tutti gli script + scheduling Arc-09)

### Script di automazione (cartella `scripts/`)

| Script | Quando usarlo | Dove in questo playbook |
|---|---|---|
| `scripts/build_monster_catalog.py` | Dopo aver aggiunto statblock nuovi | — (indicizzato in DM-QUICKSTART §4) |
| `scripts/suggest_encounter.py --el N --alliance X --env Y [--inject-npc N] [--narrative] [--wild]` | Pre-session §2 (preparare encounter fazioni/alleanze o wild) | §2 |
| `scripts/suggest_loot.py --from-encounter FILE.md --pcs N [--include-fr-themed]` | Pre-session §2 (loot standalone SRD-only; rispetta `loot: none` per wild) | §2 |
| `scripts/suggest_map.py --template NAME` | Pre-session §2 (mappa tattica) | §2 |
| `scripts/update_xp.py --el N --pcs N --apl N` | Post-session §4 (assegnare XP) | §4 |
| `scripts/state_sync.py` | Post-session §4 (aggiornare dashboard §0) | §4.2 |
| `scripts/session_recap.py --last-n N [--pdf]` | **1-2 giorni prima** della prossima sessione (recap player spoiler-safe, tono R.A. Salvatore) | **§4.6** |
| `scripts/new-campaign-group.sh` | Reset per nuovo gruppo mantenendo tutto il resto | §7.4 |

---

## §10 — Changelog (questo playbook)

- **2026-05-05** — Creato file v1: workflow pre/during/post-session, worked examples per file sessione e diff state.md, reset procedure per nuovo gruppo (branch-per-gruppo), dual clock quick reference, red flags.
- **2026-05-05** — Aggiunto §4.6 "Recap per i player" con integrazione di `scripts/session_recap.py` (generatore markdown/PDF A4 italiano spoiler-safe, tono R.A. Salvatore). Aggiunta tabella script in §9.
