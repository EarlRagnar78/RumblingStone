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
└── dnd-35-rules/   # D&D 3.5 Agent Skill — CANONICAL SOURCE
                    # All agent-specific paths symlink here (or copy via deploy.sh)
```

---

## D&D 3.5 Rules Skill

This repo ships a full **D&D 3.5 rules skill** in `skills/dnd-35-rules/`.
AI agents that support the SKILL.md standard will automatically use it.

When any agent answers a D&D 3.5 rules question:
- Load `skills/dnd-35-rules/SKILL.md` first
- Use the domain routing table inside it to load the correct reference file
- Cite sources: SRD section, or `[Private — Red Hand of Doom, p.X]` for non-SRD content
- **Never invent stat blocks or spell effects** — fetch from d20srd.org or flag as uncertain

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

This repo is configured for automatic skill discovery by:
- **Claude Code** → `.claude/skills/dnd-35-rules/`
- **OpenAI Codex** → `.agents/skills/dnd-35-rules/`
- **GitHub Copilot** → `.github/copilot/skills/dnd-35-rules/`
- **Cursor** → `.cursor/skills/dnd-35-rules/`
- **Windsurf** → `.windsurf/skills/dnd-35-rules/`

Run `./scripts/deploy-skills.sh` to install skills to your local user-level paths.
Run `./scripts/sync-skills.sh` to update all agent paths from the canonical `skills/` source.
