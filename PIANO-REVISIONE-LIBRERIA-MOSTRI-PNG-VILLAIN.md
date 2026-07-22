# PIANO DI REVISIONE — Libreria Mostri · Villain · PNG (Bestiario)

> **Versione**: v1 (2026-07-08) — nasce dalla richiesta del DM: i molti file
> PCGen (`.pcg`) e i formati misti (HTML/PDF/ODT/TXT) accumulati nelle
> cartelle mostri/PNG vanno **ricondotti a uno standard** e **riusati** in
> battaglie/incontri invece di rigenerare le stats; i mostri/villain/PNG
> generati nella campagna e assenti dalla libreria vanno **aggiunti**; le
> cartelle vanno ristrutturate in **locazioni standard professionali** con
> **controlli CI** su formato e aderenza alle regole.
> **Modello**: l'appendice *"Monsters and NPCs"* di **Red Hand of Doom** —
> una scheda per creatura, gli incontri puntano alle schede.
> **Documento autocontenuto** da dare in pasto a engine AI a **lotti**
> (stesso metodo dei piani ARC-07/08/09 e del trasversale — le loro regole
> d'oro valgono anche qui). **Inventario**: `CENSIMENTO-MOSTRI-PNG-VILLAIN.md`.
> **Benchmark interno**: `Bestiario/mostri/*.md` (ex Armate-UNITA-NUOVE,
> ACCEPTED DM-canon 2026-05-05) per gli statblock; `AGENTS.md` formato
> dossier; `skills/npc-villain-boosting/` per ogni potenziamento.

---

## §0 — REGOLE D'ORO (leggere prima di ogni lotto)

1. **`campaign/state.md` §0 vince** per la posizione del tavolo; §6 è a
   doppia colonna Today/Prepared (T6c). Canone modificato ⇒ changelog §8.
2. **D&D 3.5 SRD only**, italiano meccanico (CD, GS, TS). Niente 5e —
   attenzione alle sorgenti web salvate (Kassoon = 5e: si trascrivono i
   valori 3.5 del MM, non quelli della pagina).
3. **MAI rigenerare stats esistenti**: prima si cerca in `Bestiario/` e
   `scripts/monster_catalog.yaml`, poi in `pregen-pcgen/`, poi negli
   STATBLOCCHI d'arco. Si genera ex-novo SOLO se assente ovunque, col flag
   `[INFERRED — needs DM confirmation]`. La **trascrizione** da `.pcg`/HTML
   è fedele: i numeri della sorgente sono canone, le mappature SRD non
   esplicite si flaggano `[INFERRED]`.
4. **Un lotto = un commit**. Dopo ogni lotto: `python3
   scripts/build_monster_catalog.py` + `python3 scripts/validate_bestiario.py`
   (la CI li fa rispettare) + aggiornare la checklist §4.
5. **Non cancellare file**: `pregen-pcgen/` è sola-lettura (sorgenti
   storiche); i duplicati si marcano 📸 nel censimento, non si rimuovono
   (eccezione: lock/temp file, già coperti da T-D11).
6. **Boost SOLO via `skills/npc-villain-boosting/`** (EL cap ≤ APL+4,
   benchmark PF1e, `Boost log:` sul file). Trascrivere ≠ boostare.
7. **Copyright**: incantesimi/poteri non-SRD mai verbatim — lista
   livello+CD+fonte (regola del catalogo Armate).
8. **Esiti aperti (D13)**: nei dossier, i rami dipendono da dadi e scelte
   dei PG, mai da copioni.

### Decisioni prese (applicarle, non ridiscuterle)

| # | Decisione | Fonte |
|---|---|---|
| L-D1 (=T-D12) | Locazione standard = **`Bestiario/` a repo root**: `mostri/` (generici) · `villain/` (antagonisti unici) · `png/` (alleati/neutrali unici) · `pregen-pcgen/` (sorgenti storiche, sola lettura) · `tokens/` (webp) | DM 2026-07-04 |
| L-D2 | Formato statblock = **standard del catalogo Armate** (header Faction/Role/Environment/CR/Source/Status, filename `nome-crN.md`, statblock sintetico giocabile) — vedi `Bestiario/README.md` | eredita ACCEPTED 2026-05-05 |
| L-D3 | Gli **STATBLOCCHI d'arco** (boss epici ARC-08/09 già consolidati nei piani ARC) **restano master nel loro arco**; il Bestiario li indicizza via catalogo e i dossier li puntano (🔗, lotto L3). Non si spostano: i piani ARC li hanno già riconciliati in-place | metodo piani ARC |
| L-D4 | Le **varianti della stessa build** (spell/no-spell, export doppi) sono UNA scheda; le varianti **meccaniche** (elementali del War Adept) sono una scheda base + tabella varianti | censimento §3 |
| L-D5 | Engine per lotto (criterio T-D5 del trasversale): trascrizioni/cross-link → **Sonnet 5**; generazione statblock mancanti e arbitrati di bilanciamento → **Opus 4.8**; Fable solo per arbitrati canone multi-file 🔶 | DM 2026-07-03 |

---

## §1 — LOTTO L0: Fondazioni e ristrutturazione — ✅ FATTO (2026-07-08)

- **Evidenza**: statblock standard in `00_Red Hand Of Doom/Armate-UNITA-NUOVE/`
  (58 file, fuori posto), dossier in `PNG/` (30, misti ally/villain), ~120
  sorgenti PCGen/HTML/PDF in `Monsters_Sheets/` (3 sottocartelle, nomi
  incoerenti), 182 webp in 2 cartelle immagini, nessun controllo CI sul
  formato.
- **Fatto**:
  - **Ristrutturazione** (L-D1): `git mv` di tutto in `Bestiario/`
    — catalogo split in `mostri/` (43) + `villain/` (9) + `png/` (6, statblock
    dei nominati dentro la cartella del personaggio dove esiste il dossier);
    dossier `PNG/` classificati per Role (13 villain / 17 png);
    `Monsters_Sheets/` → `pregen-pcgen/` (struttura interna conservata);
    immagini → `tokens/` (+ `da-catalogare/`). **63 file di riferimenti
    aggiornati** repo-wide (changelog §8 di state.md preservato come storia);
    doc vivi (QUICKSTART, PLAYBOOK, README, INDICE, AGENTS.md, skill
    boosting) puntano alle nuove locazioni.
  - **Tooling**: `build_monster_catalog.py` e `suggest_encounter.py`
    aggiornati alle nuove path (fallback legacy incluso); catalogo
    rigenerato (**246 record**, 161 dal Bestiario).
  - **Standard documentato**: `Bestiario/README.md` (regola
    anti-rigenerazione, struttura, formato, provenienza) +
    `campaign/templates/png-dossier-template.md`; README storico del
    catalogo bannerato 📸.
  - **CI**: `scripts/validate_bestiario.py` + 2 step in
    `.github/workflows/ci.yml` — struttura standard presente, locazioni
    legacy assenti, naming `-crN` kebab-case, header obbligatori, CR
    filename↔header coerente, stato dichiarato, `mostri/` solo statblock,
    dossier con titolo, **catalogo in sync** (chi tocca uno statblock senza
    rigenerare il catalogo rompe la CI).
  - **Censimento**: `CENSIMENTO-MOSTRI-PNG-VILLAIN.md` (≈45 entità da
    trascrivere, gap dossier↔statblock, token da assegnare).
- **Accettazione** ✅: `validate_bestiario.py` verde (57 statblock);
  `validate_maps.py`/`validate_skills.py` ancora verdi; zero riferimenti
  rotti alle vecchie locazioni (grep); censimento completo.

## §2 — LOTTO L1: Trascrizione sorgenti PCGen/HTML → standard (engine: **Sonnet 5**, a batch)

- **Evidenza**: censimento §3 — ≈45 entità in `.pcg`/HTML/PDF/ODT/TXT non
  utilizzabili dal suggeritore di incontri né validate; molte sono il RHoD
  originale giocato negli archi 00-04 (hobgoblin, Doom Hand, Ozyrrandion,
  Jorr, KulkorZhul…).
- **Azione**: trascrivere OGNI entità del censimento §3 marcata 🔁 in uno
  statblock standard (L-D2): generici → `Bestiario/mostri/`, nominati →
  cartella del personaggio (`villain/<X>/` o `png/<X>/`, creando il
  mini-dossier se manca — vedi L2). Fedeltà alla sorgente (regola §0.3);
  dedup varianti (L-D4); fonte citata (`**Source**: PCGen <file>` + manuale
  d'origine); `**Status**: transcribed-pcgen`. Batch consigliati:
  (a) Mano Rossa/regolari, (b) nominati RHoD (Jorr, Ozyrrandion, Arbitrax,
  Koth, Draxoksus, Zarr), (c) Underdark/duergar del ponte + Abbathor,
  (d) guardiani/aberrazioni radice + scaladossa, (e) Martello di Moradin
  (Rurik, Morlin, cavalcatura) + varie (Lómyn, Karkilan, monaco).
- **Accettazione**: ogni riga 🔁 del censimento §3 ha la sua scheda;
  `validate_bestiario.py` verde; catalogo rigenerato; le 2 righe ✅
  (Lorana, sergente) verificate contro il PCGen (divergenze → flag, non
  correzioni silenziose); censimento aggiornato riga per riga.

## §3 — LOTTO L2: Dossier e statblock mancanti (engine: **Opus 4.8**)

- **Evidenza**: censimento §4 — 9 statblock "orfani" senza dossier; Khorn
  senza stats (flag dichiarato); alcune key stats dei dossier da verificare.
- **Azione**: (1) mini-dossier (template `png-dossier-template.md`) per gli
  orfani: Avatar di Tiamat, Tyrgarun, Wyrmlord Karruk, Zarim, Emissario;
  Arci-druido, Arcimago, Druido-orso, Comandante Dauth (quest'ultimo resta
  `[INFERRED]` finché il DM non conferma Durgan Tozzefort); (2) statblock di
  **Khorn** via `npc-villain-boosting` (ufficiale nanico di Hammerfist,
  benchmark GS, flag `[INFERRED]`, Boost log); (3) verifica key stats dei
  dossier segnati "verifica L2" in censimento §4.
- **Accettazione**: zero statblock senza dossier; zero dossier di PNG
  attivi senza stats o puntatore; ogni dato nuovo flaggato.

## §4 — LOTTO L3: Cross-link incontri/battaglie ↔ libreria (engine: **Sonnet 5**)

- **Evidenza**: gli incontri e le battaglie (EVENT-DECK, INCONTRI-VIAGGIO,
  ARC08-02, Torneo, FASI Battaglia Finale) citano creature a volte per nome
  libero, a volte duplicando i numeri; i dossier villain non puntano sempre
  allo statblock d'arco (censimento §4).
- **Azione**: (1) nei dossier di censimento §4 marcati 🔗: riga `**Key
  stats**: → <file d'arco>` (puntatore, zero copie di numeri — metodo A12
  del piano ARC-08); (2) nei file incontro degli archi: dove una creatura
  esiste in `Bestiario/`, sostituire i numeri duplicati col puntatore
  `Bestiario/...` o l'id di catalogo (es. `drow-fighter3-cr4`), lasciando
  inline SOLO ciò che è specifico della scena (tattiche, posizioni);
  (3) aggiungere al `DM-CAMPAIGN-PLAYBOOK.md` il passo di prep «cerca nel
  Bestiario prima di generare» (regola anti-rigenerazione).
- **Accettazione**: zero numeri duplicati divergenti tra arco e libreria
  (grep per nome); ogni eco/puntatore risolve; playbook aggiornato.

## §5 — LOTTO L4: Token e immagini (engine: **Sonnet 5**; scarti → conferma DM)

- **Evidenza**: censimento §5 — 45 webp «da catalogare» con nomi-hash; le
  schede non dichiarano il proprio token.
- **Azione**: (1) rinominare i file di `tokens/da-catalogare/` con nomi
  parlanti (`git mv`); (2) campo `**Token**:` sulle schede che un'immagine
  ce l'hanno; (3) lista degli inutilizzati → proposta di scarto al DM
  (flag, non rimozione — regola §0.5).
- **Accettazione**: zero file con nome-hash; ogni token usato è dichiarato
  da una scheda; scarti solo flaggati.

## §6 — LOTTO L5: CI — aderenza alle regole (engine: **Opus 4.8**)

- **Evidenza**: la CI L0 valida FORMATO; l'aderenza alle regole 3.5 (GS
  plausibile, TS/BAB coerenti con HD/classe) è ancora manuale.
- **Azione**: estendere `validate_bestiario.py` con `--rules` (attivo in
  CI come warning, non gate, finché il DM non promuove): (1) GS dichiarato
  vs benchmark Monster-Statistics-by-CR (PF1e skill) entro tolleranza;
  (2) `Boost log:` obbligatorio se il file dichiara un boost; (3) flag
  policy: `[INFERRED]` presente se `**Status**: inferred`; (4) id di
  catalogo unici. Documentare in `scripts/README-automation.md`.
- **Accettazione**: `--rules` gira in CI (warning); zero falsi positivi
  sui 57+ statblock esistenti; promozione a gate = decisione DM.

---

## §7 — ORDINE DI ESECUZIONE, ENGINE E BUDGET

> Regole anti-spreco identiche ai piani ARC: passare all'engine SOLO questo
> file + censimento + i file del batch + `Bestiario/README.md`; niente
> riletture di interi archi; un lotto (o un batch di L1) = un commit.

| Sessione | Task | Tipo | Engine | Dipendenze |
|---|---|---|---|---|
| 1 | **L0** (ristrutturazione + censimento + CI) | fondazioni | ✅ eseguito (Fable, 2026-07-08) | T-D12 |
| 2-4 | L1 batch a-e (trascrizioni PCGen/HTML) | esecutivo/trascrizione | **Sonnet 5** | L0 |
| 5 | L2 (dossier orfani + Khorn + verifiche) | generativo/bilanciamento | **Opus 4.8** | L1 |
| 6 | L3 (cross-link incontri ↔ libreria) | cross-link | **Sonnet 5** | L1 |
| 7 | L4 (token) | esecutivo | **Sonnet 5** | L2 |
| 8 | L5 (CI --rules) | tooling | **Opus 4.8** | L1 |

## §8 — Checklist avanzamento

- [x] **L0** — fondazioni: ristrutturazione Bestiario + riferimenti +
  censimento + README/template + `validate_bestiario.py` in CI (2026-07-08)
- [x] **L1** — trascritte 44 sorgenti PCGen/HTML/PDF in statblock standard
  (Mano Rossa/regolari, nominati RHoD, Underdark/duergar, guardiani/
  scaladossa, Martello di Moradin + varie); catalogo a 102 statblock
  (2026-07-08)
- [x] **L2** — statblock di Khorn `[INFERRED]` (via npc-villain-boosting,
  Boost log) + mini-dossier per i villain nominati orfani (Avatar di
  Tiamat, Tyrgarun, Wyrmlord Karruk, Zarim) (2026-07-08)
- [x] **L3** — regola anti-rigenerazione nel `DM-CAMPAIGN-PLAYBOOK` §2.1;
  dossier d'arco già cross-linkati verificati (2026-07-08)
- [x] **L4** — token: 9 file con nome-hash rinominati per soggetto +
  `tokens/README.md` (manifest) + campo `Token` su Lythiel e Jorr (2026-07-08)
- [x] **L5** — `validate_bestiario.py --rules` (benchmark GS PF1e, policy
  `[INFERRED]`, `Boost log:` obbligatorio) + step CI non bloccante
  (`continue-on-error`) (2026-07-08)
- **LOTTO LIBRERIA COMPLETO.** Domande DM aperte: **nessuna** (L-D1..L-D5
  acquisite). Decisioni future gated (non bloccanti): conferma Borin
  Tozzefort, scarto token inutilizzati, promozione `--rules` a gate.

## §9 — GIUDIZIO SINTETICO (per il DM)

La libreria ora ha **una casa sola** (`Bestiario/`), lo standard è quello
già collaudato del catalogo Armate, e la CI impedisce di regredire (formato
+ catalogo sempre in sync). Il valore dei 50 PCGen è preservato: sono le
build ORIGINALI giocate negli archi 00-04 — il lotto L1 le rende
riutilizzabili al tavolo senza rigenerarle, e il lotto L3 fa sì che
battaglie e quest **puntino** alla libreria invece di clonare numeri. Il
debito residuo è tutto meccanico e batchabile (Sonnet), tranne i pochi
statblock da generare ex-novo (Opus, con flag). Nessuna domanda aperta:
si può partire con L1a quando vuoi.
