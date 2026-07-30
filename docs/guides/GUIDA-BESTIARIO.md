# Guida completa — aggiungere un mostro, un PNG o un villain

> **Cosa copre**: dove va il file, come si chiama, che formato deve avere,
> come si dichiara cosa è canone e cosa no, come si rigenera il catalogo,
> come far passare il gate della CI, e **quando conviene potenziare un
> mostro esistente invece di crearne uno nuovo**.
>
> **Regola d'oro della libreria**: una creatura si scrive **una volta sola**.
> Se ti serve un nemico simile a uno che esiste già, **non rigenerarlo**:
> parti da quello e potenzialo (§8).

---

## 0. TL;DR — il ciclo completo

```bash
# 1. crea il file nella cartella giusta col nome giusto (§1, §2)
#    Bestiario/mostri/nome-crN.md   ·   Bestiario/villain/<Nome>/nome-crN.md

# 2. scrivi lo statblock nel formato standard (§3)

# 3. RIGENERA IL CATALOGO — obbligatorio, altrimenti la CI diventa rossa
python3 scripts/build_monster_catalog.py

# 4. verifica prima di committare
python3 scripts/validate_bestiario.py
python3 scripts/validate_bestiario.py --rules   # avvisi non bloccanti (GS, policy)
```

---

## 1. Dove va cosa

| Cartella | Cosa ci va | Formato |
|---|---|---|
| `Bestiario/mostri/` | unità e mostri **generici e ripetibili** (fanteria drow, gnoll, razorfiend…) | **1 file = 1 statblock**, `nome-crN.md`. Qui **solo statblock** (più i README) |
| `Bestiario/villain/` | antagonisti **unici e nominati** (Azarr Kul, Ghostlord, Mira Serani…) | una **cartella per villain**: dossier + statblock. Statblock senza dossier stanno al livello base |
| `Bestiario/png/` | PNG unici **non antagonisti** (alleati/neutrali: Lorana, Lirien…) | come `villain/` |
| `Bestiario/pregen-pcgen/` | sorgenti storiche PCGen (`.pcg`, export HTML/PDF/TXT) | **sola lettura**: si trascrive nel formato standard, non si modifica |
| `Bestiario/tokens/` | immagini `.webp` (token e ritratti) | sottocartelle `mostri/`, `png/`, `Dragons/`, `da-catalogare/` |

**Come scegliere**: se la creatura può comparire in più scene senza un nome
proprio → `mostri/`. Se ha un nome, una storia e degli obiettivi → `villain/`
(se è ostile) o `png/` (se non lo è).

---

## 2. Come si chiama il file

- **kebab-case minuscolo**, con il CR alla fine: `bone-naga-cr10.md`,
  `razorfiend-blackspawn-alfa-cr13.md`;
- **`05` significa CR ½** (`goblin-scout-cr05.md`);
- il **CR nel nome deve combaciare** con quello dichiarato nell'header —
  se li cambi, cambiali in entrambi i posti;
- **varianti**: file distinti **solo se i numeri cambiano** (war adept
  fuoco/ghiaccio = due file). Gli export «con incantesimi / senza
  incantesimi» della stessa build sono **una sola scheda**.

---

## 3. Il formato dello statblock (obbligatorio)

```markdown
# Nome Creatura (contesto) [ACCEPTED — DM-canon 2026-05-05]
**Faction**: ghostlord-undead | **Role**: caster-melee | **Environment**: any | **CR**: 10 | **Source**: MM II p.146 | **Status**: inferred

Large aberration (undead) HD 13d12 (84 HP). AC 18 (-1 size, +3 Dex, +6 natural).
Fort +4 Ref +7 Will +13. BAB/Grapple +9/+18. Sting +13 (1d4+7 + paralysis Fort
CD 20). Str 20 Dex 17 Con - Int 16 Wis 15 Cha 17. Spells as Sorcerer 8
(CL 8, CD 13+liv): 0-6 1-7 2-7 3-7 4-5. Undead traits.
Notes: guardiana della lair del Ghostlord.
```

**I sei header sono obbligatori** — senza uno solo, la CI fallisce:

| Header | Cosa ci scrivi |
|---|---|
| `Faction` | a chi appartiene (`mano-rossa`, `ghostlord-undead`, `drow`, `neutrale`…) |
| `Role` | funzione tattica (`melee`, `caster`, `skirmisher`, `boss`, `caster-melee`…) |
| `Environment` | dove compare (`any`, `underground`, `forest`, `urban`…) |
| `CR` | numero, coerente col filename |
| `Source` | **sempre citata**: `MM p.NNN`, `RHoD p.NN`, `FRCS`, `SRD`, o `[INFERRED]` se costruita |
| `Status` | `accepted` (canone confermato dal DM) o `inferred` (proposta) |

**Regole di contenuto:**
- niente **testo verbatim non-SRD** (copyright): degli incantesimi si citano
  nome, livello e CD, non la descrizione;
- niente **poteri inventati senza flag**: se non è attestato, marcalo
  `[INFERRED — needs DM confirmation]`;
- `Notes:` finale = **come si usa nella campagna** (dove compare, con chi,
  perché) — è la parte che ti serve davvero al tavolo.

### Titolo e stato di canone

Nel titolo H1 ci va il flag:

- `[ACCEPTED — DM-canon YYYY-MM-DD]` → il DM l'ha confermato: è canone;
- `[INFERRED — needs DM confirmation]` → ricostruito o proposto, in attesa.

Lo stesso stato va ripetuto in `**Status**`. Quando il DM approva: cambi il
flag, aggiorni `Status`, e se tocca il canone di campagna aggiorni
`campaign/state.md` (§8 changelog).

---

## 4. I dossier (solo `villain/` e `png/`)

Un antagonista nominato ha **due file**: lo statblock (i numeri) e il
**dossier** (chi è). Template: `campaign/templates/png-dossier-template.md`.

Struttura del dossier: **Role · Status · Location · Motivation · CR · Key
stats · Esiti · Notes**. Deve avere un **titolo H1** (lo verifica la CI).

Il dossier è dove vivono le cose che i numeri non dicono: cosa vuole, di chi
si fida, cosa succede se muore, cosa succede se scappa, e i **rami aperti**
lasciati alle decisioni del DM.

---

## 5. Rigenerare il catalogo (passaggio che tutti dimenticano)

`scripts/monster_catalog.yaml` è l'indice di tutta la libreria, usato da
`suggest_encounter` e dagli agenti. **Va rigenerato ogni volta che tocchi
uno statblock**:

```bash
python3 scripts/build_monster_catalog.py            # rigenera
python3 scripts/build_monster_catalog.py --check    # dry-run: dice solo se è disallineato
```

Se lo dimentichi, `validate_bestiario` fallisce in CI con «catalogo non in
sync». Non è un capriccio: senza rigenerare, il tuo mostro **non esiste**
per gli strumenti di preparazione.

---

## 6. Validare prima di committare

```bash
python3 scripts/validate_bestiario.py          # GATE: errori bloccanti
python3 scripts/validate_bestiario.py --rules  # avvisi (GS vs benchmark, policy flag)
python3 scripts/validate_bestiario.py --json   # report JSON, se ti serve automatizzare
```

Cosa controlla il gate:

1. la **struttura standard** esiste e le vecchie cartelle legacy no;
2. ogni statblock rispetta **naming, header obbligatori, coerenza CR** e ha
   uno **stato dichiarato**;
3. ogni dossier ha un **titolo H1**;
4. `mostri/` contiene **solo** statblock;
5. il **catalogo è in sync**.

`--rules` non blocca: segnala scostamenti dai benchmark di GS e dalle policy
dei flag — utile per capire se il CR che hai messo è realistico.

---

## 7. Aggiungere un mostro: la procedura completa

1. **Cerca prima**: `grep -ril "<nome>" Bestiario/` — c'è già qualcosa di simile?
   Se sì → §8 (potenzia, non duplicare).
2. **Scegli la cartella** (§1) e il **nome file** col CR (§2).
3. **Scrivi lo statblock** nel formato standard (§3), citando la fonte.
4. Se è un villain/PNG nominato: **scrivi anche il dossier** (§4).
5. **Rigenera il catalogo**: `python3 scripts/build_monster_catalog.py`.
6. **Valida**: `python3 scripts/validate_bestiario.py`.
7. Se cambia il canone di campagna (nuovo villain attivo, morte, alleanza):
   aggiorna `campaign/state.md` — e ricordati che le scritture di canone
   passano da `dm.py session` (ADR-0007), non a mano sulle regioni `auto:`.
8. **Traccia**: riga in `plans/CHANGELOG.md` se è un lotto di lavoro.

---

## 8. Potenziare invece di creare (quasi sempre la scelta giusta)

Se il party è di livello 13 e hai uno statblock CR 9 che ti piace, **non
scrivere un mostro nuovo**: potenzialo. Il repo ha una skill dedicata,
`npc-villain-boosting`, con tre metodi:

| Metodo | Quando |
|---|---|
| **Dadi Vita aggiuntivi** (advancement 3.5) | vuoi lo stesso mostro «più grosso», stessa identità |
| **Livelli di classe** | vuoi dargli un mestiere (il capitano gnoll che è anche chierico) |
| **Template** (3.5) o **simple template PF1e** (avanzato, elementale…) | vuoi cambiargli natura in fretta, con numeri già tarati |

Chiedi pure a un agente: *«potenzia razorfiend CR 9 per un party APL 13»* —
la skill si attiva da sola e applica i benchmark di GS. L'esemplare in repo
è `Bestiario/mostri/razorfiend-blackspawn-alfa-cr13.md` (Huge 16 DV,
ottenuto avanzando il razorfiend CR 9).

Il file nuovo, se lo crei, segue comunque §2-§3 — e il vecchio **resta**:
la truppa d'ondata e l'élite convivono.

---

## 9. Se la CI diventa rossa

| Messaggio | Causa e rimedio |
|---|---|
| **catalogo non in sync** | hai toccato uno statblock senza rigenerare → `python3 scripts/build_monster_catalog.py` e committa lo YAML |
| **header mancante** | manca uno dei sei (`Faction/Role/Environment/CR/Source/Status`) → aggiungilo, sulla riga singola separata da ` | ` |
| **CR filename ≠ CR header** | allinea i due (ricorda `05` = ½) |
| **stato non dichiarato** | metti `[ACCEPTED — DM-canon …]` o `[INFERRED — …]` nel titolo **e** `Status:` nell'header |
| **filename non conforme** | kebab-case minuscolo + `-crN.md`, niente spazi o maiuscole |
| **`mostri/` contiene non-statblock** | spostalo: i dossier vanno in `villain/` o `png/` |
| **dossier senza titolo** | aggiungi un `# Titolo` in cima |
| **struttura legacy rilevata** | esistono ancora `Armate-UNITA-NUOVE/`, `Monsters_Sheets/` o `PNG/` a root → vanno migrate in `Bestiario/` |

---

## 10. Dove sta il resto

| Cosa | Dove |
|---|---|
| Indice e regole della libreria | [`Bestiario/README.md`](../../Bestiario/README.md) |
| Template dossier PNG/villain | `campaign/templates/png-dossier-template.md` |
| Potenziamento: decisione, metodi, workflow | skill `npc-villain-boosting` (`references/boost-decision.md`, `boost-methods-35.md`, `boost-workflow.md`) |
| Regole 3.5 / PF1e per costruire | skill `dnd-35-srd` · `pathfinder-1e-srd` |
| Censimento di ciò che manca (cosa dell'AP non è ancora in repo) | [`CENSIMENTO-MOSTRI-PNG-VILLAIN.md`](../../CENSIMENTO-MOSTRI-PNG-VILLAIN.md) (radice del repo) |
| Parametri esatti degli script | [`scripts/README-automation.md`](../../scripts/README-automation.md) · [`docs/tools/README.md`](../tools/README.md) |
| Proporre incontri col catalogo | `python3 scripts/dm.py prep --el 13 --env underground` |
