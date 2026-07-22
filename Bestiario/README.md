# BESTIARIO — Libreria standard di Mostri, Villain e PNG

> **Locazione standard della campagna** (decisione DM **T-D12**, 2026-07-04,
> piano trasversale §0). Modello: l'appendice *"Monsters and NPCs"* di **Red
> Hand of Doom** — ogni creatura ha UNA scheda riutilizzabile; gli incontri
> della campagna **puntano** alle schede, non le rigenerano.
> Piano di lavoro: `PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN.md` (repo
> root) · Inventario completo: `CENSIMENTO-MOSTRI-PNG-VILLAIN.md` (repo root).

---

## Regola d'oro (anti-rigenerazione)

**Le stats esistenti NON si rigenerano.** Prima di creare un mostro/PNG per
una quest o un incontro:

1. cerca nel catalogo (`python3 scripts/suggest_encounter.py --list-npcs`, o
   `grep` su `scripts/monster_catalog.yaml`);
2. se esiste → **riusa il file** (puntatore, non copia);
3. se esiste solo come sorgente storica (`pregen-pcgen/`) → **trascrivi** nel
   formato standard (lotto L1 del piano), senza reinventare i numeri;
4. solo se non esiste da nessuna parte → genera ex-novo col template e
   flagga `[INFERRED — needs DM confirmation]` (regola AGENTS.md).

## Struttura

| Cartella | Contenuto | Formato |
|---|---|---|
| `mostri/` | Unità e mostri **generici/ripetibili** (fanteria drow, gnoll, razorfiend…) | 1 file = 1 statblock, filename `nome-crN.md` |
| `villain/` | Antagonisti **unici e nominati** (Azarr Kul, Ghostlord, Sethrax…) | cartella per villain = dossier + statblock; statblock "orfani" di dossier al livello base |
| `png/` | PNG **unici non antagonisti** (alleati/neutrali: Lorana, Maewen, Khorn…) | come `villain/` |
| `pregen-pcgen/` | **Sorgenti storiche**: file PCGen `.pcg`, export HTML/PDF/ODT/TXT (era `Monsters_Sheets/`) | sola lettura — si trascrive nel formato standard, non si modifica |
| `tokens/` | Immagini webp (token/ritratti) per mostri e PNG | `mostri/`, `png/` (per uso), `Dragons/`, `da-catalogare/` |

## Formato statblock standard (ereditato dal catalogo Armate, 2026-05-05)

```markdown
# Nome Creatura (contesto) [ACCEPTED — DM-canon YYYY-MM-DD]   ← o [INFERRED — needs DM confirmation]
**Faction**: … | **Role**: … | **Environment**: … | **CR**: N | **Source**: MM/RHoD/… | **Status**: accepted|inferred

<Taglia> <tipo> HD XdY (NN HP). AC … Fort/Ref/Will … BAB/Grapple …
Attacchi principali, qualità speciali, CD. Str … Dex … (statistiche chiave).
Spell: lista livello+CD, MAI testo verbatim non-SRD (copyright).
Notes: dove/come si usa nella campagna.
```

- **CR nel filename** (`-crN.md`, `05` = ½) DEVE combaciare con l'header.
- **Fonti citate sempre** (MM, RHoD, FRCS…); niente poteri inventati senza flag.
- Il **dossier** dei PNG/villain nominati segue il formato AGENTS.md
  (Role/Status/Location/Motivation/CR/Key stats/Esiti/Notes) — template:
  `campaign/templates/png-dossier-template.md`.
- Le **varianti** (es. war adept fire/ice/acid) sono file distinti solo se i
  numeri cambiano; gli export "spell/no-spell" della stessa build sono UNA
  scheda.

## Automazione e CI

- `scripts/build_monster_catalog.py` → indicizza la libreria in
  `scripts/monster_catalog.yaml` (usato da `suggest_encounter.py`).
  **Rigenerare a ogni modifica di statblock** (la CI lo verifica).
- `scripts/validate_bestiario.py` → gate CI: naming `-crN`, header
  obbligatori, CR filename↔header coerente, catalogo in sync, cartella
  legacy assente.
- Boost di PNG/villain SOLO via `skills/npc-villain-boosting/`
  (EL cap ≤ APL+4, `Boost log:` obbligatorio).

## Provenienza (ristrutturazione 2026-07-08, lotto L0)

- `00_Red Hand Of Doom/Armate-UNITA-NUOVE/` (58 schede) → `mostri/` +
  `villain/` + `png/` (indice storico: `mostri/README-CATALOGO-STORICO.md`).
- `PNG/` (30 dossier) → `villain/` (antagonisti) + `png/` (alleati/neutrali).
- `00_Red Hand Of Doom/Monsters_Sheets/` (125 sorgenti) → `pregen-pcgen/`.
- `00_Red Hand Of Doom/Immagini/{Monster_And_Png,Png_And_Monster_To_Be_added}`
  (182 webp) → `tokens/`.
