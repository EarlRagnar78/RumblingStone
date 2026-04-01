# ⚔️ RumblingStone

*A custom D&D 3.5 campaign based on Red Hand of Doom.*  
Setting: Forgotten Realms / The Dalelands • Era: 1372 DR • System: D&D 3.5 SRD

---

## Repo Structure

```
RumblingStone/
├── AGENTS.md                          ← AI agent instructions (universal)
├── campaign/
│   ├── sessions/                      ← Session logs (YYYY-MM-DD_session-N.md)
│   ├── npcs/                          ← NPC cards
│   ├── locations/                     ← Location descriptions
│   ├── encounters/                    ← Custom encounter files
│   └── lore/
│       ├── house-rules.md             ← Active house rules
│       └── rhod-adaptations.md        ← Red Hand of Doom → Dalelands mappings
│
├── skills/dnd-35-rules/               ← CANONICAL skill source
│   ├── SKILL.md
│   └── references/                    ← Per-domain rule references
│
├── .claude/skills/dnd-35-rules/       ← Claude Code (auto-discovered)
├── .agents/skills/dnd-35-rules/       ← OpenAI Codex (auto-discovered)
├── .cursor/skills/dnd-35-rules/       ← Cursor (auto-discovered)
├── .windsurf/skills/dnd-35-rules/     ← Windsurf (auto-discovered)
├── .github/copilot/skills/dnd-35-rules/ ← GitHub Copilot (auto-discovered)
│
└── scripts/
    ├── deploy-skills.sh               ← Install skills to user-level agent paths
    └── sync-skills.sh                 ← Propagate changes from canonical to agent paths
```

---

## Setup for New Collaborators

### 1. Clone the repo
```bash
git clone git@github.com:EarlRagnar78/RumblingStone.git
cd RumblingStone
```

### 2. Deploy skills to your local agent paths (one-time)
```bash
./scripts/deploy-skills.sh
```

This installs the D&D 3.5 skill to:
- `~/.claude/skills/` (Claude Code)
- `~/.codex/skills/` (OpenAI Codex)
- `~/.cursor/skills/` (Cursor)
- `~/.windsurf/skills/` (Windsurf)

### 3. Verify skill is loaded

**Claude Code:**
```
/skills
```

**Codex CLI:**
```bash
codex --list-skills
```

**Cursor / GitHub Copilot:** The skill is auto-discovered from `.claude/skills/` and `.github/copilot/skills/` respectively when you open the repo.

---

## Updating Skills

Edit the canonical source in `skills/dnd-35-rules/`, then sync:
```bash
./scripts/sync-skills.sh
git add . && git commit -m "chore: sync dnd-35-rules skill"
```

---

## ChatGPT / Gemini

These platforms don't auto-read repo files.  
Use the condensed system prompt in `skills/dnd-35-rules/SKILL.md` as the base for:
- A **Custom GPT** (ChatGPT) — paste SKILL.md content into "Instructions"
- A **Gem** (Gemini) — paste into the Gem system prompt
- Any **API-based agent** — inject as system message

---

## License

Campaign content: privately owned (based on *Red Hand of Doom* © Wizards of the Coast).  
D&D 3.5 rules content in `skills/dnd-35-rules/`: Open Game License (OGL 1.0a).  
See `skills/dnd-35-rules/references/resources.md` for OGL details.
