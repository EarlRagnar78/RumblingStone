# AGENTS.md — RumblingStone Campaign Repo

**Project**: *RumblingStone* — a custom D&D 3.5 campaign set in the Forgotten Realms,
based on *Red Hand of Doom* (Jacobs & Wyatt, 2006). Content is privately owned.
**System**: D&D 3.5 Edition (d20 SRD / OGL). Non-SRD content is privately held.
**Setting**: Faerûn, 1372 DR. Adapted from the Elsir Vale to the Dalelands region.

---

## What This Repo Contains

```
Bestiario/                   # STANDARD library of monsters, villains & NPCs (T-D12)
├── mostri/                  # generic units/monsters, one statblock per file (-crN.md)
├── villain/                 # unique antagonists (dossier folder + statblock)
├── png/                     # unique allies/neutrals (dossier folder/file + statblock)
├── pregen-pcgen/            # historical sources: PCGen .pcg + HTML/PDF exports (read-only)
└── tokens/                  # webp art/tokens for monsters & NPCs

campaign/
├── DM-CAMPAIGN-PLAYBOOK.md  # DM operational guide (workflow + examples + reset)
├── state.md                 # Living world state (§0 dashboard first)
├── sessions/                # Session logs (YYYY-MM-DD_session-N.md)
├── npcs/                    # NPC cards (name, stat block, motivation, status)
├── locations/               # Location descriptions and maps metadata
├── encounters/              # Custom encounter files (CR, monsters, tactics)
├── templates/               # Blank state + session templates for new groups
└── lore/                    # House rules, world adaptations, timeline

skills/
├── dnd-35-srd/             # D&D 3.5 SRD mechanics (no setting bias)
├── forgotten-realms-lore/  # Faerûn 1372 DR canon
├── rumblingstone-campaign/ # custom campaign + coherence rules
├── pathfinder-1e-srd/      # PF1e rules, templates, 3.5<->PF conversion
├── npc-villain-boosting/   # when/whether/how to boost PNGs, villains, monsters
└── dnd-35-rules/           # legacy meta-router (points to the skills above)

plans/     # work-plan archive: INDEX.md (status + % + gates), CHANGELOG.md, adr/
scripts/   # DM automation — single entrypoint: python3 scripts/dm.py
Script/    # content converters (pdf→md, html→md, img→webp) — NOT the DM automation
```

Per-agent mirrors (`.claude/skills/`, `.cursor/skills/`, etc.) are
generated artifacts of `scripts/build-skills.sh` and are gitignored.
`.hb.md` files are generated Homebrewery layouts (`plans/adr/ADR-0003`):
regenerate via `dm.py recap --hype` / `dm.py handout`, never edit by hand.

> **DMs: start with `campaign/DM-CAMPAIGN-PLAYBOOK.md`.** It contains the
> pre/during/post-session workflow, worked examples for session files and
> `state.md` diffs, the `§0 Campaign Status At-a-Glance` dashboard, and the
> branch-per-group reset procedure (`scripts/new-campaign-group.sh`) for
> running this campaign with a new group.

---

## Skills

This repo ships focused skills plus one legacy meta-router.
AI agents that support SKILL.md will discover them automatically:

- `skills/dnd-35-srd/` — pure d20 SRD mechanics
- `skills/forgotten-realms-lore/` — Faerûn 1372 DR canon
- `skills/rumblingstone-campaign/` — this campaign (PCs, artifacts, arcs, coherence)
- `skills/rumblingstone-narrative-style/` — **mandatory for all content generation**: eight-pillar style engine (Salvatore prose, LotR depth, Casa di Davide destiny, Andor intrigue, GoT politics, Mercer table technique, BG3 echoes, BG1/2 quest design), PC protagonism in good and evil
- `skills/rumblingstone-mapmaking/` — map generation workflow (Watabou, templates, VTT export)
- `skills/rumblingstone-plans/` — work-plan archive conventions (INDEX, gates, ADRs)
- `skills/pathfinder-1e-srd/` — Pathfinder 1e rules, simple templates, CR benchmarks, 3.5↔PF1e conversion
- `skills/npc-villain-boosting/` — decision framework + workflow for boosting PNGs/villains/monsters
- `skills/dnd-35-rules/` — legacy meta-router; points to the skills above

When any agent answers a question:

1. Match the question to the skill (rules / lore / campaign).
2. Load that skill's `SKILL.md` first; follow its routing table.
3. For campaign questions, also load `campaign/state.md` and
   `skills/rumblingstone-campaign/references/campaign-coherence.md`.
4. Cite sources: SRD section, FRCS p.X, or `[Private — Red Hand of Doom, p.X]`.
5. **Never invent** stat blocks, spell effects, NPC stats, or artifact powers.
   Flag as `[INFERRED — needs DM confirmation]` instead.

---

## Campaign-Specific Conventions

### File naming

- Sessions: `campaign/sessions/YYYY-MM-DD_session-N.md`
- NPCs: `campaign/npcs/[name-kebab-case].md`
- Encounters: `campaign/encounters/[location-name]_encounter.md`

### NPC file format

```markdown
# [NPC Name]
**Role**: [villain / ally / neutral]
**Status**: [alive / dead / unknown]
**Location**: [current known location]
**Motivation**: [one sentence]
**CR**: [N] | **Race/Class**: [race, class N]
**Key stats**: HP X, AC Y, Attack +Z
**Notes**: [adaptation from RHoD original]
```

### Session log format

```markdown
# Session N — [Title] (YYYY-MM-DD)
**Players present**: [list]
**Location**: [in-world location]
## Summary
## Key decisions
## XP awarded
## Loot distributed
## Next session hooks
```

### Encounter file format

```markdown
# Encounter: [Name]
**Location**: [room/area]
**EL**: [N] | **CR breakdown**: [list monsters + CR]
**Terrain**: [description]
## Tactics
## Adaptations from RHoD original
## Read-aloud text (custom)
```

---

## Rules Adjudication Policy

1. **SRD first** — use d20srd.org for all rules lookups
2. **Non-SRD**: flag as `[Private source]`; do not reproduce copyrighted text verbatim
3. **House rules** live in `campaign/lore/house-rules.md` — always check before ruling
4. **RAW vs RAI**: state which you're providing; give both if ambiguous
5. **Red Hand of Doom adaptations**: documented in `campaign/lore/rhod-adaptations.md`
6. **DM Strategy & Player Profiles**: For adult-oriented, non-linear sessions (Shine Time, State Machine design), consult `skills/dnd-35-rules/references/campaign-dm-strategy.md` (canonical). The lore folder file `campaign/lore/dm-player-strategy.md` is now a pointer to that canonical source.
7. **Living world state**: Before describing what NPCs know, where parties/villains currently are, or what threads are open, load `campaign/state.md`. It is the single source of truth for *current* world state (changes per session).
8. **Coherence**: Before introducing artifact powers, NPC knowledge, or callbacks to past PG actions, consult `skills/dnd-35-rules/references/campaign-coherence.md`.
9. **Boosting PNGs/villains/monsters**: The campaign runs on D&D 3.5; Pathfinder 1e SRD material (simple templates, Monster-Statistics-by-CR benchmarks, NPC recipes) is an approved boost toolkit. Always go through `skills/npc-villain-boosting/` — it enforces the EL cap (≤ APL+4), the benchmark step, and the `Boost log:` requirement on named-NPC files. Never boost silently.
10. **Narrative content generation**: ANY request to generate quests, session prose, read-aloud/boxed text, NPC dialogue, hooks, recaps, or handouts MUST load `skills/rumblingstone-narrative-style/` (eight-pillar style engine) automatically — the user should never have to ask for "the style". It enforces the scene mixer (one lead pillar per scene), the PC Protagonism Test, the living-world rules (NPC/villain agency + SRD attitude mechanics — protagonism is the camera, not gravity), the Echo Ledger (`state.md` §7.E), and the BG1/2 quest-stage patterns. Coherence (rule 8) always beats style.

---

## For AI Agents: Key DO / DON'T

| DO | DON'T |
|---|---|
| Read session logs before generating continuations | Invent events that contradict session logs |
| Check `campaign/npcs/` before describing NPCs | Invent NPC stats not in files |
| Use 3.5 SRD for all mechanics | Use 5e rules (different system) |
| Load the dnd-35-rules skill for rules questions | Quote non-SRD books verbatim |
| Flag 4e/5e Forgotten Realms lore as post-1372 DR | Present Spellplague as canon for this campaign |
| Preserve 3.5-era Faerûn canon (1372 DR) | Mix in FR lore from after 1385 DR |

---

## Supported Agents

The canonical skill source is `skills/dnd-35-rules/`. Per-agent mirrors are
**generated artifacts**, not committed to git (see `.gitignore`). Each
developer/CI runs the build pipeline locally:

- **Claude Code** → `.claude/skills/dnd-35-rules/` (compact.md format)
- **OpenAI Codex** → `.agents/skills/dnd-35-rules/` (machine.json)
- **GitHub Copilot** → `.github/copilot/skills/dnd-35-rules/` (compact.md)
- **Cursor** → `.cursor/skills/dnd-35-rules/` (machine.json)
- **Windsurf** → `.windsurf/skills/dnd-35-rules/` (compact.md)
- **Gemini** → `.gemini/skills/dnd-35-rules/` (structured.yaml)
- **ChatGPT** → `.chatgpt/skills/dnd-35-rules/` (compact.md)

Build commands:

```
./scripts/build-skills.sh           # build + deploy to ~/.<agent>/skills/
./scripts/build-skills.sh --no-deploy  # build only (CI)
./scripts/sync-skills.sh            # build + populate in-repo mirrors locally
```

Why mirrors aren't committed: they are 6× the source size (~3MB), drift over
time, and any agent that needs them can regenerate deterministically from
`skills/`. Treat `skills/` as the only thing humans edit.
