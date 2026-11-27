---
paths:
  - "0[0-9]_*/**"
  - "10-stand-alone/**"
  - "campaign/**"
  - "Bestiario/**"
  - "PG/**"
---
<!-- Generato da scripts/regole_claude.py da AGENTS.md (ADR-0141): si corregge AGENTS.md, poi si rigenera. I percorsi sono dalla radice del repo. -->
## Campaign-Specific Conventions

### File naming

- Sessions: `campaign/sessions/YYYY-MM-DD_session-N.md`
- NPCs and villains: `Bestiario/png/` and `Bestiario/villain/` (statblock + catalog entry)
- Encounters: inside the arc module that uses them, next to their tactical map

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

1. **SRD first**: use d20srd.org for all rules lookups
2. **Non-SRD**: flag as `[Private source]`; do not reproduce copyrighted text verbatim
3. **House rules** live in `campaign/lore/house-rules.md`; always check before ruling
4. **RAW vs RAI**: state which you're providing; give both if ambiguous
5. **Red Hand of Doom adaptations**: documented in `skills/rumblingstone-campaign/references/campaign-coherence.md` (canonical) and summarised in `campaign/DM-QUICKSTART-NUOVI-DM.md`
6. **DM Strategy & Player Profiles**: For adult-oriented, non-linear sessions (Shine Time, State Machine design), consult `skills/rumblingstone-campaign/references/campaign-dm-strategy.md` (canonical). The lore folder file `campaign/lore/dm-player-strategy.md` is now a pointer to that canonical source.
7. **Living world state**: Before describing what NPCs know, where parties/villains currently are, or what threads are open, load `campaign/state.md`. It is the single source of truth for *current* world state (changes per session).
8. **Coherence**: Before introducing artifact powers, NPC knowledge, or callbacks to past PG actions, consult `skills/rumblingstone-campaign/references/campaign-coherence.md`.
9. **Boosting PNGs/villains/monsters**: The campaign runs on D&D 3.5; Pathfinder 1e SRD material (simple templates, Monster-Statistics-by-CR benchmarks, NPC recipes) is an approved boost toolkit. Always go through `skills/npc-villain-boosting/`: it enforces the EL cap (≤ APL+4), the benchmark step, and the `Boost log:` requirement on named-NPC files. Never boost silently.
10. **Session lifecycle & canon writes**: Closing a session, updating `state.md`, generating recaps/briefs/teasers, or invoking anything in `scripts/` goes through `skills/rumblingstone-automation/` (single entrypoint `python3 scripts/dm.py`). Scripts may write canon ONLY under the ADR-0007 triple constraint: group branch (never `main`), DM-confirmed diff, and `<!-- auto: -->` marked regions of `state.md`. Everything else stays a printed proposal the DM applies by hand.
11. **Narrative content generation**: ANY request to generate quests, session prose, read-aloud/boxed text, NPC dialogue, hooks, recaps, or handouts MUST load `skills/rumblingstone-narrative-style/` (nine-pillar style engine) automatically; the user should never have to ask for "the style". It enforces the scene mixer (one lead pillar per scene), the PC Protagonism Test, the living-world rules (NPC/villain agency + SRD attitude mechanics, where protagonism is the camera and not gravity), the Echo Ledger (`state.md` §7.E), and the BG1/2 quest-stage patterns. For **mysteries, clues and in-fiction documents** the case skill `skills/rumblingstone-indagine/` carries the operational layer, including the Eco register (`references/documento-ed-errore-fecondo.md`): the document and its omissions, the rule book as a political engine, the table's wrong deduction made productive instead of corrected, and the guard clause (structure and object, never paragraph length), with the read-aloud ceilings winning any conflict. Coherence (rule 8) always beats style.

---

