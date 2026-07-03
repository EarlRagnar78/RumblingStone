# Rules Verification Ledger

Every hard number in `skills/` and in the scripts' rules data traces to an
official source. This file records what was verified, against what, and what
remains structurally unverifiable. Update it whenever rules content changes.

**Verification sources** (provided by the DM, 2026-07-03; not committed —
kept outside the repo):

- **3.5**: official WotC D&D 3.5 SRD, RTF distribution (OGL) — files cited
  below by SRD section name. Online mirror: https://www.d20srd.org
- **PF1e**: official Paizo PRD epubs (Core Rulebook, Bestiary, GameMastery
  Guide, APG, UM, UC, ARG — OGL/Community Use). Online mirror:
  https://aonprd.com

## Method

1. Convert source (striprtf / epub-xhtml strip) to plain text.
2. Locate the authoritative table/paragraph by name.
3. Compare each cell/claim in the skill reference; fix mismatches in place.
4. Where a table is absent from the sources (see "Not verifiable"), state
   the formula, mark provenance, or cross-check indirectly.

## Verified — by file

| File | Verified against | Errors found & fixed |
|---|---|---|
| `dnd-35-srd/references/monsters.md` | SRD *ImprovingMonsters*, monster files (templates) | Type table BAB: Construct ¾, Elemental ¾, Fey ½, Undead ½; template ability lines; size/CR RAW modifiers |
| `dnd-35-srd/references/combat.md` | SRD *Combat I/II*, *Abilities and Conditions* | Crit multiplication (flat bonuses multiply; extra dice don't); Dying (10%/round, no save); Grappled; Run (no −2 AC); massive damage is core |
| `dnd-35-srd/references/core-mechanics.md` | SRD *Basics*, *Carrying and Exploration*, *Skills I/II* | XP slow/fast columns labeled house-rule (3.5 has no official tracks; table itself is PHB, non-SRD — formula noted) |
| `dnd-35-srd/references/classes.md` | SRD *Classes I/II* | Druid wild-shape progression (full table replaced); paladin turning (level −3, from 4th); monk speed (per 3 levels); rogue special abilities (every 3 from 10th); sorcerer slots/known rows; wizard prohibited-school rule (no fixed pairs) |
| `dnd-35-srd/references/spells.md` | SRD spell files (S, F–G) | Sleep = 4 HD; finger of death save logic; magic missile SR note |
| `dnd-35-srd/references/items.md` | SRD *Magic Items I–VI* | Pricing table (potion 50, wand 750, continuous 2,000 — no ×4,000 row); weapon min CL = 3×bonus; keen (no stacking); vorpal (no save); disruption (Will, bludgeoning); gauntlets of ogre power (+2 Str); haversack (move action); robe of the archmagi |
| `npc-villain-boosting/references/boost-methods-35.md` | SRD *ImprovingMonsters* | Nonassociated threshold wording; RAW CR modifiers (size/elite array/special abilities); no HD+class-level stacking |
| `npc-villain-boosting/references/boost-workflow.md` | SRD troll entry + size tables | Worked-example damage dice (bite 1d8+5, rend 3d6+15) |
| `pathfinder-1e-srd/references/monster-advancement.md` | PF Bestiary (simple templates, Monster Advancement appendix) | Giant/Young quick+rebuild rules; Advanced rebuild; Entropic/Resolute resistances; non-key threshold = original CR; per-step advancement deltas added |
| `pathfinder-1e-srd/references/npc-building.md` | PF Core (NPC creation, Table: NPC Gear, encounter design) | NPC gear values; CR-from-level incl. sub-1 progression; arrays |
| `pathfinder-1e-srd/references/core-differences.md` | PF Core / Bestiary size table | CMB size modifiers (G +4, C +8) |
| `scripts/magic_items_srd.yaml` | SRD pricing formulas + item entries | Wand of magic missile (CL 1 at 750 gp); +2 flaming burst battleaxe 32,310; +3 keen rapier 32,320; +4 holy greatsword 72,350; staff of fire 17,750 |
| `scripts/update_xp.py` | XP formula 500·N·(N−1) | none — thresholds correct |
| `scripts/suggest_encounter.py` | DMG ch.3 EL doubling rule (see below) | none — 2·log₂ Σ2^(CR/2) reproduces "double creatures = EL +2" |

## Not directly verifiable (and how each is handled)

| Item | Why | Handling |
|---|---|---|
| 3.5 XP-to-level table | PHB material, excluded from the OGL SRD | Standard formula stated; slow/fast columns explicitly labeled house rule |
| 3.5 XP awards per CR (DMG Table 2–6) | DMG, non-OGL | Scripts never compute awards; DM supplies XP in session logs (`update_xp.py` only sums) |
| 3.5 EL/encounter math (DMG ch.3) | DMG, non-OGL | Documented as DMG-derived; formula validated against the published doubling rule |
| 3.5 NPC gear (DMG Table 4–23) | DMG, non-OGL | Flagged "verify in your copy"; verified PF Core Table: NPC Gear offered as substitute |
| PF Bestiary Table 1–1 absolute rows | Table absent from the PRD epub text (prose references it) | Anchor rows cross-checked by integrating the verified per-step Monster Advancement deltas (CR 8→13 reproduces the row values exactly); flag kept out, provenance noted in file |
| Non-SRD splat content (Tome of Battle, Complete series, MM III/IV…) | Copyrighted, never reproduced | Always flagged `[Non-SRD: <book>]` per `AGENTS.md` policy |

## Re-verification checklist (for future edits)

- Adding a number to any `skills/**` reference? Cite the source section in
  the same paragraph, verify against the sources above (or the online
  mirrors), and add a row here.
- CI (`scripts/validate_skills.py`) guards structure (frontmatter, links,
  data-YAML parse) — it cannot check rules facts. Rules facts are guarded
  by this ledger and the cited sources only.
