# Repo Organization Analysis — RumblingStone Campaign

**Goal**: Improve repository organization to help the dungeon master continue a live campaign with AI agent support (Claude Code, Cursor, etc.).

---

## Findings

### 🔴 Critical Issues

| # | Issue | Impact on DM |
|---|-------|-------------|
| 1 | `campaign/{sessions,npcs,locations,encounters}/` is a **literal directory** with braces in its name (empty) | Breaks the documented convention. DM looks for `campaign/npcs/` and finds nothing. |
| 2 | `campaign/npcs/`, `campaign/locations/`, `campaign/encounters/` **do not exist** as real directories | All NPC data lives in `PNG/` instead, creating a structural mismatch with `AGENTS.md`, `README.md`, and session-log templates. |
| 3 | Only **1 session log** exists (`2026-05-03_session-3.md`) but campaign state shows "post-Hammerfist" content | The actual campaign history is in `state.md` and `00_Red Hand Of Doom/` notes, not in session logs. Future sessions lack continuity. |

### 🟡 Medium Issues

| # | Issue | Impact |
|---|-------|--------|
| 4 | Duplicate spreadsheets: `00_Red Hand Of Doom/Armate.ods` vs `Armate-AGGIORNATO.ods` | DM may edit stale version; army balance may reference wrong numbers. |
| 5 | Duplicate XP spreadsheets with typo: `CalcoloPuntiEperiennza.ods` vs `CalcoloPuntiEperienza-current.ods` | Same risk — which one is current? |
| 6 | Multiple near-identical Tordek HTML files in `PG/Artefatti/Artefatti-Pg/Tordek/` (3 copies) | Confusion about which is the authoritative artifact reference. |
| 7 | `DM-QUICKSTART-ARC09.md` claims all references resolve, but reads like a "done" checklist with live content elsewhere | DM may think Arc-09 is fully prepared when encounter details, loot, and maps still need per-session assembly. |
| 8 | `README.md` references `campaign/npcs/` (non-existent) and has a typo `csmpaign players.md` | New users / AI agents get confused about NPC location. |

### 🟢 Low / Cosmetic

| # | Issue | Impact |
|---|-------|--------|
| 9 | `Script/` (capital S) contains utility tools not documented anywhere | Dead weight; nobody knows they exist. |
| 10 | `scripts/Old/` contains legacy scripts (`deploy-skills.sh`, `sync-skills.sh`) | Could confuse DM about which version to run. |
| 11 | `00_Red Hand Of Doom/00_shaar/` has raw web scrapes not referenced | Not harmful, but unused clutter. |
| 12 | `08_La Battaglia Di Hammerfist/` has atlas files with both `-complete` and bare suffixes | Likely intentional versioning, but should be clarified. |
| 13 | TODOs in `DM-QUICKSTART-ARC09.md` ("Archi 05-06 ancora da catalogare") | Cataloging gaps are documented but not flagged prominently. |

---

## Recommended Improvements

### Priority 1 — Fix Structural Mismatches (do first)

**A. Remove the literal-brace directory and create real directories**

Delete `campaign/{sessions,npcs,locations,encounters}/` (the directory with literal curly braces in its name). Then create:

```
campaign/
├── npcs/          # symlinks or copies of PNG/ files, or move PNG/ contents here
├── locations/     # populate from 00_Red Hand Of Doom/ and arc-specific maps
├── encounters/    # populate from arc-specific encounter files
```

**Decision needed**: Should `campaign/npcs/` contain the NPC cards directly, or should `PNG/` be renamed/merged into `campaign/npcs/`?

**Recommended**: Symlink `campaign/npcs/` → `../PNG/` (or vice versa) to avoid duplicating files, since AI agents and DM workflows reference both paths.

**B. Archive the duplicate spreadsheets**

- Keep `Armate-AGGIORNATO.ods` (the updated one), remove or move `Armate.ods` to `00_Red Hand Of Doom/Archivio/`
- Keep `CalcoloPuntiEperienza-current.ods`, fix the typo filename, archive the old one

### Priority 2 — Clean Up Duplicate Artifacts

**C. Deduplicate `PG/Artefatti/`**

- Keep one authoritative file per artifact (the most complete one)
- Move duplicates to `PG/Artefatti/Archivio/`
- Add a `README.md` in `PG/Artefatti/` documenting which files are canonical

**D. Archive legacy `scripts/Old/`**

- Move `deploy-skills.sh` and `sync-skills.sh` to `scripts/Old/` and add a note that they are superseded by the root-level versions
- Or remove if confirmed unused

### Priority 3 — Improve DM Workflow Discoverability

**E. Create a `campaign/README.md` for the DM**

A short file (30-40 lines) that says:
- "Start here: `DM-CAMPAIGN-PLAYBOOK.md`"
- "Live state: `state.md`"
- "NPCs are in `PNG/` (also accessible via `campaign/npcs/` symlink)"
- "Skills in `skills/` auto-load for AI agents"
- "Arc-09 quick access: `DM-QUICKSTART-ARC09.md`"

**F. Fix `README.md` typos and references**

- Replace `csmpaign players.md` with correct reference
- Add a note that `campaign/npcs/` is a symlink to `PNG/` (or update to point to `PNG/`)

### Priority 4 — Document Existing Power-User Tools

**G. Add a `Script/README.md`**

Briefly document what the three tool subdirectories do and when a DM might use them (HTML extraction, image conversion, PDF parsing — mostly for content migration, not live play).

### Priority 5 — Long-Term Archival Hygiene

**H. Create `00_Red Hand Of Doom/Archivio/`**

Move stale/duplicate files here:
- `Armate.ods` (old)
- `CalcoloPuntiEperiennza.ods` (typo version)
- Any other superseded files

**I. Audit Arc-05 and Arc-06** per existing TODO

- `DM-QUICKSTART-ARC09.md` flags "Archi 05-06 ancora da catalogare completamente"
- Assign an indexing task or mark as "prepared but not cataloged" in the atlas

---

## Implementation Order

```
1. Remove literal-brace dir               ← 1 command
2. Create real campaign/ subdirs          ← 1 command each
3. Symlink campaign/npcs/ → PNG/         ← 1 command
4. Archive duplicate spreadsheets         ← mv commands
5. Archive duplicate PG/Artefatti files   ← mv + README edit
6. Archive scripts/Old/                   ← mv or rm
7. Fix README.md typos/references         ← edit
8. Create campaign/README.md              ← new file
9. Create Script/README.md                ← new file
10. Create 00_Red Hand Of Doom/Archivio/  ← 1 command + mv
11. Update DM-QUICKSTART-ARC09.md TODOs   ← edit
```

All changes are **additive or archival** — nothing is deleted permanently. The DM can roll back any step with git.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| AI agents reference `campaign/npcs/` and break when directory is reorganized | Use a **symlink** so both paths resolve to the same content |
| DM has unsaved notes in `campaign/{sessions,npcs,...}/` (the brace dir) | It's empty per inventory; no data loss risk |
| Removing `scripts/Old/` breaks someone's workflow | Move to `scripts/Old/` (lowercase, matching convention) instead of deleting |
| Renaming `PNG/` to `campaign/npcs/` breaks absolute references | Prefer symlink approach; only rename after all refs are updated |

---

## Validation Steps

After changes:
1. Run `find campaign/ -type d` to confirm real directories exist where expected
2. Run `ls -la campaign/npcs/` to confirm symlink resolves
3. Run AI agent test: "Where is the NPC Tempestas?" — should resolve to `campaign/npcs/Tempestas/` **and** `PNG/Tempestas/`
4. Confirm `git status` shows only expected moves/creates, no content changes
5. Confirm `.gitignore` still covers `build/` and draft files
