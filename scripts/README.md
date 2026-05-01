# RumblingStone — Skill Build & Sync Pipeline

## What This Does

Compresses, indexes, and packages the `skills/*` source trees into per-agent
formats and (optionally) deploys to user-level skill directories.

## Skills

The repo ships **three skills** as canonical sources, plus one legacy
meta-router for backwards compatibility:

| Skill | Scope |
|---|---|
| `skills/dnd-35-srd/` | Pure d20 SRD mechanics (no setting bias) |
| `skills/forgotten-realms-lore/` | Faerûn 1372 DR canon |
| `skills/rumblingstone-campaign/` | Custom campaign — PCs, artifacts, arcs, coherence |
| `skills/dnd-35-rules/` | Meta-router that points to the three above (legacy compat) |

The build pipeline auto-discovers anything under `skills/` that has a
`SKILL.md` file.

## Pipeline

```
RAW .md → compress_skills.py → compact.md / structured.yaml / machine.json
                             ↓
                      index_skills.py → build/<skill>/index.json
                             ↓
                      build-skills.sh → packages/<agent>/
                             ↓
              user-level deploy OR sync-skills.sh (in-repo mirrors)
```

## Quickstart

```bash
./scripts/build-skills.sh                     # build all skills + deploy to ~/.<agent>/skills/
./scripts/build-skills.sh --no-deploy         # build only (CI)
./scripts/build-skills.sh --skill=dnd-35-srd  # build a single skill
./scripts/build-skills.sh --measure           # report compression numbers
./scripts/build-skills.sh --dry-run           # see what would happen
./scripts/sync-skills.sh                      # populate in-repo mirrors (gitignored)
```

## What is NOT committed

Per-agent mirrors (`.claude/skills/`, `.agents/skills/`, `.cursor/skills/`,
`.windsurf/skills/`, `.chatgpt/skills/`, `.gemini/skills/`,
`.github/copilot/skills/`) and `build/` are all gitignored. They are
deterministic outputs of the canonical `skills/*` source. Each developer
runs the pipeline locally.

This was changed because committing the mirrors caused ~3MB of duplication
and silent drift between agents.

## Per-Agent Format Routing

| Agent | Format | Why |
|---|---|---|
| Claude | compact.md | Reads markdown natively |
| Windsurf | compact.md | Same loader family as Claude |
| ChatGPT | compact.md | Mixed NL + structure |
| Copilot | compact.md | Conservative default |
| Gemini | structured.yaml | Native YAML parsing |
| Codex | machine.json | Deterministic |
| Cursor | machine.json | Deterministic |

## index.json — Honest Note

`index.json` is generated under `build/<skill>/index.json` and is intended
for selective loading. **No mainstream agent loader currently consumes it
automatically.** It is therefore *not* copied into per-agent packages —
shipping it would only inflate token cost.

It remains useful for:

- Custom scripts that want to do their own retrieval.
- Developers writing prompts that want to point at specific files.
- Future agents whose loaders gain index.json support (add their name to
  `AGENT_INDEX_AWARE` in `build-skills.sh`).

## Adding a New Skill

1. Create `skills/<new-skill>/SKILL.md` (must contain a YAML frontmatter
   block with `name:` and `description:`).
2. Add reference files under `skills/<new-skill>/references/`.
3. (Optional) Add domain keywords to `DOMAIN_KEYWORDS` in `index_skills.py`
   for richer index coverage.
4. Run `./scripts/build-skills.sh` — auto-discovers and builds it.

## Why compact.md > JSON for Claude

JSON adds structural overhead (quotes, braces, commas) that costs tokens for
text-native models. Claude reads markdown tables and headers efficiently.
JSON is best for code-oriented agents (Codex, Cursor) that already parse JSON.
