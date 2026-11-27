---
paths:
  - "skills/**"
  - "scripts/build-skills.sh"
  - "scripts/sync-skills.sh"
  - "scripts/validate_skills.py"
  - ".claude/**"
  - "0[0-9]_*/**"
  - "10-stand-alone/**"
  - "campaign/**"
  - "Bestiario/**"
  - "PG/**"
---
<!-- Generato da scripts/regole_claude.py da AGENTS.md (ADR-0141): si corregge AGENTS.md, poi si rigenera. I percorsi sono dalla radice del repo. -->
## Supported Agents

The canonical skill source is the whole `skills/` tree (every directory with
a `SKILL.md`; `build-skills.sh` auto-discovers them). The one exception is the
game-system skills (ADR-0111, L6): a skill listed by a plugin in
`sistemi/<id>/sistema.toml` is built and synced only when that system is
`attivi` or `rinforzo` in `sistemi.toml`; `python3 scripts/sistemi.py
--skill-escluse` prints the skills that are skipped; skills no plugin lists
are always built. Per-agent mirrors are **generated artifacts**, not committed
to git (see `.gitignore`); each developer/CI builds them locally:

- **Claude Code** → `.claude/skills/<skill>/` (compact.md format). Claude Code also gets THIS file
  split into `.claude/rules/rs-*.md` by `python3 scripts/regole_claude.py`
  (ADR-0141): each section loads only with the files it is for. Edit AGENTS.md,
  then regenerate; `--check` fails when the two drift apart.
- **OpenAI Codex** → `.agents/skills/<skill>/` (machine.json)
- **GitHub Copilot** → `.github/copilot/skills/<skill>/` (compact.md)
- **Cursor** → `.cursor/skills/<skill>/` (machine.json)
- **Windsurf** → `.windsurf/skills/<skill>/` (compact.md)
- **Gemini** → `.gemini/skills/<skill>/` (structured.yaml)
- **ChatGPT** → `.chatgpt/skills/<skill>/` (compact.md)

Build commands:

```
./scripts/build-skills.sh           # build + deploy to ~/.<agent>/skills/
./scripts/build-skills.sh --no-deploy  # build only (CI)
./scripts/sync-skills.sh            # build + populate in-repo mirrors locally
```

**Automatic sync (no manual step needed):**

- **Claude Code** (web + CLI): `.claude/hooks/session-start.sh` (registered
  in `.claude/settings.json`) rebuilds and deploys ALL skill mirrors at the
  start of every session, **asynchronously**, in background.
- **Stale-mirror protocol (async race guard)**: the hook writes
  `.claude/.skills-sync-status` (`syncing…` → `ok <sha> <ts>` | `failed`).
  Before the FIRST campaign-content generation of a session, the agent must
  check that file: if it is missing or not `ok`, **tell the user** the skill
  mirrors may be stale and ask whether to update now; on yes run
  `./scripts/build-skills.sh && ./scripts/sync-skills.sh --no-build`, then
  continue the conversation normally. If the user declines, proceed reading
  the canonical `skills/` tree directly (always current in git).
- **Claude Code started OUTSIDE the repo** (the project threads on claude.ai
  start in the folder that contains the clone): `scripts/claude-progetto.sh`,
  run by the cloud environment's setup script, writes there a short
  `CLAUDE.md`, the repo's `.claude/settings.json` with absolute paths and the
  `.mcp.json`, so the hook, the skills and `rumblingstone-tools` apply
  ([ADR-0140](plans/adr/ADR-0140-la-configurazione-claude-del-repo-arriva-anche-nei-thread.md)).
- **Other agents / plain git users**: run `./scripts/install-git-hooks.sh`
  once; it installs a `post-merge` git hook that resyncs the mirrors after
  every `git pull` that touches `skills/`, and a `pre-push` hook that runs the
  blocking, fast CI gates (`python3 scripts/gate_locale.py --pre-push`, about
  45 s, via pre-commit when installed;
  [ADR-0143](plans/adr/ADR-0143-i-gate-veloci-girano-prima-del-push.md)). In
  Claude Code cloud sessions the SessionStart hook installs both.

Treat `skills/` as the only thing humans edit; mirrors regenerate
deterministically from it.
