# RumblingStone — Skill Optimization Pipeline

## What This Does

**Problem:** AI agents load entire skill trees → wasteful token usage (~50K tokens/query).
**Solution:** Build pipeline that produces per-agent optimized formats + retrieval index.

## Token Savings Summary

| Technique | Savings | Where it applies |
|---|---|---|
| Selective loading via index | **60–80%** | All queries (primary lever) |
| Prose stripping | 10–15% | campaign-*.md, dm-strategy.md |
| DSL abbreviations | 5–10% | combat.md, core-mechanics.md |
| Per-agent format (YAML/JSON) | 5–15% | Structured reference files |

**Total effective reduction per query: 70–85%** vs loading all skills raw.

## Pipeline

```
RAW .md → compress_skills.py → compact.md / structured.yaml / machine.json
                             ↓
                       index_skills.py → index.json (domain→file mapping)
                             ↓
                      build-skills.sh → per-agent packages
                             ↓
                      sync-skills.sh → in-repo agent paths + user ~/.agent/skills/
```

## Quickstart

```bash
# Build everything (compress + index + package + deploy)
./build-skills.sh --measure

# Dry run first
./build-skills.sh --dry-run

# Build + sync to repo paths (for git commit)
./scripts/sync-skills.sh

# Build without user-level deploy (CI/CD)
./build-skills.sh --no-deploy
```

## Agent Format Routing

| Agent | Format | Why |
|---|---|---|
| Claude | compact.md | Best at structured markdown, DSL-aware |
| Gemini | structured.yaml | Handles YAML key-value natively |
| Codex / Cursor | machine.json | Deterministic parsing, no ambiguity |
| ChatGPT | compact.md | Mixed NL + structure |
| Windsurf | compact.md | Similar to Claude Code |

## Selective Loading (How the Index Works)

Instead of loading all 15+ reference files (~50K tokens), agent loads index.json first,
identifies the 1-3 relevant domain files, loads only those (~5-10K tokens):

```python
# Agent pseudo-code
index = load("index.json")  # ~500 tokens
relevant_files = index["domain_index"]["combat"]  # → ["combat"]
content = load(f"references/combat.compact.md")  # ~2000 tokens
# Total: ~2500 tokens vs ~50000 = 95% reduction
```

## Scripts

| Script | Purpose |
|---|---|
| `build-skills.sh` | Main pipeline: compress → index → package → deploy |
| `scripts/compress_skills.py` | Multi-format compressor (md/yaml/json) |
| `scripts/index_skills.py` | Builds domain+keyword retrieval index |
| `scripts/sync-skills.sh` | Format-aware repo sync (replaces blind cp -R) |

## Adding a New Skill File

1. Add `skills/dnd-35-rules/references/my-new-file.md`
2. Add entry to `FILE_DOMAINS` dict in `index_skills.py`
3. Add domain keywords to `DOMAIN_KEYWORDS` if needed
4. Run `./build-skills.sh`

## Why compact.md > JSON for Claude

JSON adds structural overhead (+quotes, +braces) that costs tokens for Claude's parser.
Claude reads markdown natively — tables, headers, and bullet structures parse efficiently.
JSON is best for code-oriented agents (Codex, Cursor) that already work in JSON.
