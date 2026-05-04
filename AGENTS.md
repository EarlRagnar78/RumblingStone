# AGENTS.md — RumblingStone Campaign Repo

**Project**: *RumblingStone* — a custom D&D 3.5 campaign set in the Forgotten Realms,
based on *Red Hand of Doom* (Jacobs & Wyatt, 2006). Content is privately owned.
**System**: D&D 3.5 Edition (d20 SRD / OGL). Non-SRD content is privately held.
**Setting**: Faerûn, 1372 DR. Adapted from the Elsir Vale to the Dalelands region.

---

## What This Repo Contains

```
campaign/
├── sessions/       # Session logs (YYYY-MM-DD.md format)
├── npcs/           # NPC cards (name, stat block, motivation, status)
├── locations/      # Location descriptions and maps metadata
├── encounters/     # Custom encounter files (CR, monsters, tactics)
└── lore/           # House rules, world adaptations, timeline

skills/
├── dnd-35-srd/             # D&D 3.5 SRD mechanics (no setting bias)
├── forgotten-realms-lore/  # Faerûn 1372 DR canon
├── rumblingstone-campaign/ # custom campaign + coherence rules
└── dnd-35-rules/           # legacy meta-router (points to the three above)
```

Per-agent mirrors (`.claude/skills/`, `.cursor/skills/`, etc.) are
generated artifacts of `scripts/build-skills.sh` and are gitignored.

---

## Skills (three of them)

This repo ships **three** focused D&D 3.5 skills plus one legacy meta-router.
AI agents that support SKILL.md will discover them automatically:

- `skills/dnd-35-srd/` — pure d20 SRD mechanics
- `skills/forgotten-realms-lore/` — Faerûn 1372 DR canon
- `skills/rumblingstone-campaign/` — this campaign (PCs, artifacts, arcs, coherence)
- `skills/dnd-35-rules/` — legacy meta-router; points to the three above

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
