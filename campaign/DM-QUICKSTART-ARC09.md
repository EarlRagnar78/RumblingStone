# DM Quickstart — Arco-09 Post-Hammerfist → Finale Rethmar

> **🎯 Scopo**: punto di ingresso unico per il DM che continua la
> campagna da Day 19 (fine Hammerfist) fino al climax Rethmar (Day 40+).
> Questo file **indicizza** tutti gli strumenti già pronti: workflow,
> script, atlas unità, scheduling, scenari, checklist.

**Stato canonizzato 2026-05-05**: tutte le unità `[INFERRED]` sono
`[ACCEPTED — DM-canon]`. March Clock = Day 19. Ritual Clock = 9/18.
APL = 13.

> **↩ Carry-over dall'ARC-07 — echi del rituale P3B di Hella (T9)**: prima di
> giocare ARC-09 verifica in `campaign/state.md` **come è stato risolto il
> rituale di resurrezione di Hella** (ARC-07 P3B). Se un dono è stato
> **rifiutato**, tre echi si propagano in questo arco e sono già agganciati
> ai file bersaglio:
> - **Tordek rifiuta il respiro** → veleni drow, **Fase 0 Notte dei Drow**
>   (`...FASE0-NOTTE-DEI-DROW-TESTO.md`).
> - **Thorik / Artemis rifiutano** → prima ferita critica / primo 0 pf di
>   Hella (`08_.../ARC08-03-REGISTRO-PERDITE.md`).
> - **Rifiuto totale** → 3 slot-dono vuoti della Collana = 3 quest opzionali
>   (`Arco-Post-Hammerfist-HOOKS-INTEGRATION-MASTER.md` §2).
>
> Tabella completa e default: `07_il Portale Della Forgia
> Eterna/PortaleForgia-P3B-ResurrezioneHella-COMPLETO.md` §2-BIS «Il ramo del
> rifiuto». Se il rituale non è ancora stato giocato, gioca i doni pieni
> (nessun eco attivo).

---

## §1 — Workflow di base (per ogni sessione)

Leggi **una volta sola** il playbook master:

📘 **`campaign/DM-CAMPAIGN-PLAYBOOK.md`** — manuale operativo
(pre/during/post session, 3 livelli di stato, reset per nuovo gruppo).

Poi, ogni sessione:

1. **Pre-session (15 min)**: playbook §2
2. **Live (a tavolo)**: playbook §3 (solo `campaign/state.md` + session log)
3. **Post-session (30 min)**: playbook §4-5
4. **Commit**: git tag per sync.

---

## §2 — Stato vivo della campagna

| File | Cosa contiene |
|---|---|
| `campaign/state.md` | §0 dashboard + §2 March/Ritual clock + party/villains |
| `campaign/sessions/YYYY-MM-DD_session-N.md` | Log di ogni sessione |
| `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md` | Clock ledger, attrition, rifugiati, **§4b Epic Unit Apparition Triggers (CR 10-18)** |
| `00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md` | Numeri orda, distaccamenti, **§2.6 Endgame Elite tier**, §6 scenari finali |

---

## §3 — Atlas delle Unità (cosa metto in campo?)

**File master**: `00_Red Hand Of Doom/Armate-COMPOSIZIONE-DETTAGLIATA.md`
— indice di 16 sezioni (Mano Rossa core, dragoni, Razorfiend, Wyrmlord,
Drow Sonjak, Gnoll, Loxo/Centauri, Githyanki, Teschio Nero, Rakshasa,
Aberrazioni, Alleati Difensori, **§16 Boss Epici CR 10-18**).

**Cartella statblock derivati** (accettati): `00_Red Hand Of Doom/Armate-UNITA-NUOVE/`
(54 file, tutti `[ACCEPTED — DM-canon 2026-05-05]`).

**Cartella NPC canonici**: `PNG/` (Azarr Kul, Ghostlord, Lorana, Lythiel,
Maewen, Salvatore, Sethrax, Sonjak, Tempestas, Therysol, Valerius,
Xal'thor, Il Collezionista).

---

## §4 — Script pronti (automazione)

Tutti in `scripts/`, tutti autonomi (zero dipendenze esterne):

| Script | Uso | Quando |
|---|---|---|
| `build_monster_catalog.py` | Scansiona il repo → `monster_catalog.yaml` (216 record) | Dopo aver aggiunto unità nuove a `Armate-UNITA-NUOVE/` |
| `suggest_encounter.py --el N [--alliance X \| --factions a,b] --env Y [--inject-npc N] [--narrative] [--wild]` | Propone 3-5 encounter mix con EL target. Supporta alleanze canoniche (17), PG iniettati, wild (no-loot). | Ogni volta che servono encounter per una scena |
| `suggest_loot.py --from-encounter FILE.md --pcs N [--include-fr-themed]` | **Standalone**: loot SRD-only per l'encounter. Legge `<!-- loot: structured\|none -->`. Skip auto su wild. | Dopo `suggest_encounter.py`, pipe → |
| `suggest_map.py --template forest-ambush` | Genera mappa tattica da template (11 template disponibili) | Prep mappa tattica di una scena |
| `state_sync.py` | Estrae/aggiorna `§0` dashboard di `state.md` | Post-session |
| `update_xp.py` | Calcola XP post-encounter (DMG 3.5) | Post-encounter |
| `session_recap.py --last-n N [--pdf]` | Recap+preview in italiano per i player (tono R.A. Salvatore, spoiler-safe) | Pre-session (1-2 giorni prima) |
| `new-campaign-group.sh` | Reset per nuovo gruppo senza perdere materiale | Playbook §7 |

**Esempio concreto**:

```bash
# Bisogna preparare un encounter Rethmar Fase 1, PG livello 13:
python3 scripts/suggest_encounter.py --el 14 --alliance red-hand-drow-pact --env urban --narrative --seed 42 > /tmp/enc.md
python3 scripts/suggest_loot.py --from-encounter /tmp/enc.md --pcs 5 --include-fr-themed --seed 42
# → encounter + loot SRD-only (con 1 faction signature + opz 1 FR-themed mild)

# Wild encounter (predatori naturali, NO loot strutturato):
python3 scripts/suggest_encounter.py --wild --el 11 --env mountain --seed 3

# Bisogna una mappa per imboscata su Wyrmlord Karruk:
python3 scripts/suggest_map.py --template bridge-chokepoint

# Post-sessione: assegnare XP
python3 scripts/update_xp.py --el 14 --pcs 5 --apl 13

# 1-2 giorni prima della prossima sessione: generare recap per i player
python3 scripts/session_recap.py --last-n 1 --pdf
# → campaign/recaps/recap-YYYY-MM-DD.md (+ .pdf se pandoc installato)
# Spoiler-safe: taglia automaticamente `## DM notes` dai session log
# e le righe ⬜ (archi futuri) dal dashboard §0.
```

---

## §5 — Arco-09: struttura narrativa e files

**Cartella**: `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/`

**File indice**: `INDICE-GENERALE-COMPLETO-CAMPAGNA.md` (indice numerato
di tutte le fasi).

**Fasi principali**:

| Fase | File master | Arco temporale |
|---|---|---|
| P1 Hella | `P1A-Timeline-Quest-Hellas-*` + `P1B-Cerchio-Treant-*` + `P1C-Rituale-*` | Day 20-27 (finestra PG) |
| P2 Rhest | `P2-RHEST-OVERVIEW.md` + `FASE1-4` + `ENCOUNTER-*` | Day 22-26 |
| P2A Torre | `P2A-Torre-PARTE1-4` + `STATBLOCCHI` per livello | Day 24-28 |
| P2B Torneo Dauth | `P2B-Torneo-PARTE1-3` + `OTTO-PORTE` + `BATTLE-STATS` | Day 26-30 (fixed) |
| P2C Mercante | `P2C-Salvatore-Mercante-TESTO.md` | Day 25-35 (subplot) |
| P3 Ghostlord | `P3-Ghostlord-LICH-ALLEANZA-TESTO.md` + `STATBLOCCHI` + `MAPPE` | Day 28-35 |
| P3 Starsong | `P3-Starsong-Hill-ALLEANZA-ELFI-*` | Day 30-38 |
| P3 Sabotaggi | `P3-Sabotaggio-Campi-Drow-*` + `P3-MISSIONI-BREVI-CR12-*` | Day 30-38 |
| **P3 Finale Rethmar** | `P3-BATTAGLIA-FINALE-FASE0..4-*` + `STATBLOCCHI-EPICI.md` + `ARMATE-SYNC.md` | Day 40 (Fase 0) → Day 42 (Fasi 1-4, climax) |

**Hooks integration master**: `Arco-Post-Hammerfist-HOOKS-INTEGRATION-MASTER.md`.

---

## §6 — Scheduling rapido (chi appare quando)

📅 **Cheat sheet** estratto da `Armate-SINCRONIZZAZIONE-CAMPAGNA.md` §4b:

| Day | Epic Event |
|---|---|
| 19 | Hammerfist end — Fauci di Palude: ramo condizionale (D10), non ancora deciso — default fugge ferito, alternativa ucciso |
| 20-22 | Karruk CR 10 pubblico |
| 22-26 | Saarvith/Zalkatar finestre PG (Rhest, Torre) |
| 26-30 | **Dauth fixed**: Zarim CR 12 Day 2, Xal'thor CR 14 Day 3 |
| 28-32 | Emissario Red Hand → Ghostlord parley |
| 30-35 | Il Collezionista CR 18 muove shadow |
| 35-38 | Warpriest élite CR 11 sacrificio → Ritual +1 |
| 38-39 | Hobgoblin Captains CR 8 visibili |
| **40** | **Rethmar Fase 1**: Abithriax CR 15 + Karruk + Ondata Giganti EL 15 |
| 40+1 | Fase 2 — Warpriest ritualisti + Ghostlord non-morti |
| 40+2 | **Fase 3** — Azarr Kul CR 15 + Tyrgarun + Ondata ×2 |
| Ritual 18/18 | **Avatar Tiamat CR 17** evocato (Fase 4 climax) |

---

## §7 — Scenari finali a Rethmar

Dal `Armate-CALCOLI-ESERCITI-DINAMICI.md` §6:

| Scenario | Orda | Difensori | Rapporto | Esito |
|---|---|---|---|---|
| Worst | 12.700 | 2.200 | 5.8:1 | Rethmar cade |
| Baseline | 9.400 | 2.200 | 4.3:1 | Sconfitta |
| Medio | 8.000 | 3.100 | 2.6:1 | Difficile ma vincibile |
| Ottimale | 6.800 | 4.100 | 1.66:1 | Vittoria con perdite |
| Leggendario | 6.400 | 4.700 | 1.36:1 | Vittoria decisiva |

Il DM controlla lo scenario dai **trigger PG** (Rhest, Torre, Ghostlord,
Loxo revolt, Collezionista stop, Starsong/Dauth/Druidi alleanze) —
tutti tracciati in `Armate-CALCOLI-ESERCITI-DINAMICI.md` §4 e §5.2.

---

## §8 — Skills per domande specifiche

Se un player/agent fa una domanda, usa lo skill giusto:

- **Regole D&D 3.5 pure** → `skills/dnd-35-srd/`
- **Lore Faerûn 1372 DR** → `skills/forgotten-realms-lore/`
- **Coerenza campagna / artefatti / PG** → `skills/rumblingstone-campaign/`
- **Meta-router legacy** → `skills/dnd-35-rules/`

Regola AGENTS.md: **mai inventare statblocchi**. Se manca una stat,
flaggala `[ACCEPTED — DM-canon]` e cita fonte (MM/FRCS/AP).

---

## §8.5 — Risorse di resurrezione nel Vale (protocollo morte PG — C3)

> **Lotto C3 (2026-07-02).** Nota unica citata da tutte le sidebar "SE FALLISCONO"
> (P1C, P2A-PARTE4, P2B-PARTE3, RHEST-FASE4, Ghostlord). A APL 13-14 la morte di
> un PG **non deve** chiudere la campagna: deve **costare**.

**Precedente in-fiction (vincolante)**: Hella è **già** stata resuscitata con il
**Cuore di Moradin** — artefatto **single-use, ora speso** (state.md §6). Non è
ripetibile: nessun agente/PG può "riusarlo" (violazione di coerenza da flaggare).

**Chi può riportare indietro un PG nel Vale (Day 20-42):**

| Fonte | Dove | Incantesimo | Costo (SRD/DMG 3.5) | Costo narrativo |
|---|---|---|---|---|
| Tempio maggiore di Rethmar | Rethmar (se non caduta) | *raise dead* / *resurrection* | ~5.450 mo (diamante 5.000) / ~10.910 mo (diamante 10.000) | Debito col Consiglio (favore politico, Consiglio_Rethmar) |
| Confraternita di Ilmater (Sorella Maewen) | Dauth | *raise dead* | ~5.450 mo | Voto di servizio alla Confraternita (hook ARC-10) |
| Circolo degli Otto / arci-druidi | campale, solo a Rethmar | *reincarnate* (nuovo corpo!) | componenti + rischio forma casuale | Cambia razza del PG — costo identitario |
| Chierici alleati al fronte | Rethmar Fase 3-4 | *breath of life*-equivalenti (SRD: *revivify* non esiste in 3.5 → **nessuna** rianimazione istantanea) | — | In battaglia **non** c'è resurrezione: il corpo va portato via |

**Regole d'oro del protocollo:**
1. **In battaglia non si resuscita** (3.5 non ha *revivify*): un PG che cade in
   Fase 0-4 è fuori per la scena; il recupero avviene **dopo**, se il corpo è
   salvato (le sidebar RHEST/Ghostlord notano i casi in cui il corpo è difficile
   da recuperare — fondo del lago, tana del Lich).
2. **Ogni raise lascia un debito**, mai gratis: politico (Consiglio), religioso
   (Ilmater), o identitario (*reincarnate*). È il "costo, non stop".
3. Se il party **non può permettersi** un raise (oro/finestra): il PG morto
   diventa un **hook** (visione, eredità, vendetta) — la storia continua col
   gruppo ridotto, non si ferma.

---

## §9 — TL;DR: il DM ha tutto quello che serve?

✅ **Workflow** → `campaign/DM-CAMPAIGN-PLAYBOOK.md` (§2-§7)
✅ **Stato vivo** → `campaign/state.md` (dashboard + clock)
✅ **Scheduling eventi** → `Armate-SINCRONIZZAZIONE-CAMPAGNA.md` §4b
✅ **Numeri armate** → `Armate-CALCOLI-ESERCITI-DINAMICI.md` §2-§6
✅ **Atlas unità** → `Armate-COMPOSIZIONE-DETTAGLIATA.md` (16 sezioni)
✅ **Statblock derivati** → `Armate-UNITA-NUOVE/` (54 file ACCEPTED)
✅ **NPC canonici** → `PNG/*/`
✅ **Encounter automation** → `scripts/suggest_encounter.py` (alleanze + wild + inject-NPC)
✅ **Loot automation standalone** → `scripts/suggest_loot.py` (DMG 3.5 Tab.3-5, SRD-only + FR-themed mild)
✅ **Mappa automation** → `scripts/suggest_map.py` (11 template)
✅ **XP automation** → `scripts/update_xp.py`
✅ **State sync** → `scripts/state_sync.py`
✅ **Recap player spoiler-safe** → `scripts/session_recap.py` (+ opzionale PDF A4)
✅ **Reset nuovo gruppo** → `scripts/new-campaign-group.sh`
✅ **Narrative files Arc-09** → 70+ file in `09_Continuazione.../`
✅ **Hammerfist guide (rif.)** → `08_.../ARC08-01-GUIDA-DM.md`
✅ **Skills per domande** → `skills/` (4 skills)

**Gaps noti** (documentati):

- ODS `Armate-AGGIORNATO.ods` → rebuild manuale DM (note §8 Calcoli)
- Archi 05-06 ancora da catalogare completamente (TODO atlas §Mapping)

Tutto il resto è pronto per le prossime sessioni.
