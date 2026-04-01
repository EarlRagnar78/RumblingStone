# Free & Open Resources for D&D 3.5 — 2026 Reference

---

## SOURCE PRIORITY HIERARCHY

When an AI agent needs to look up rules or lore, follow this order:

| Priority | Source | Best for |
|---|---|---|
| 1 | **d20srd.org** | OGL canonical mechanics; authoritative rules text |
| 2 | **dndtools.one** | Non-SRD books, psionics, ToB, Spell Compendium, cross-refs |
| 3 | **realmshelps.net** | FR lore, NPC stats, regional encounters, weather, history |
| 4 | **forgottenrealms.fandom.com** | FR depth: deity pages, geography, named NPCs |
| 5 | **orbitalflower.github.io → web.archive.org** | Official WotC 3.5 articles: maps, monsters, errata |
| 6 | **imarvintpa.com** | Structured spell lookup, non-SRD spell catalogue |

---

## SOURCE 1 — d20srd.org (System Reference Document 3.5)

**URL**: https://www.d20srd.org
**License**: Open Game License (OGL 1.0a) — freely reproducible

### URL Patterns for AI Agents (web_fetch)

```
https://www.d20srd.org/srd/spells/[spellName].htm
https://www.d20srd.org/srd/classes/[className].htm
https://www.d20srd.org/srd/monsters/[monsterName].htm
https://www.d20srd.org/srd/magicItems/[itemType].htm
https://www.d20srd.org/srd/combat/
https://www.d20srd.org/srd/feats.htm
https://www.d20srd.org/srd/conditionSummary.htm
https://www.d20srd.org/srd/skills/[skillName].htm
https://www.d20srd.org/ogl.htm
```

---

## SOURCE 2 — dndtools.one (The Comprehensive D&D 3.5 Database)

**URL**: https://dndtools.one
**What it is**: Major update/overhaul of dndtools.pw and dndtools.eu. Contains everything from
the old databases plus additional data added by hand during site creation, including all powers
from pretty much every published 3.5 edition material.
**Content**: Classes, Feats (1,600+ general), Feat Categories, Traits, Flaws, Skills, Skill Tricks,
Deities, Languages, Spells (5,000+), Spell Schools, Descriptors, Shadow Casting, Invocations,
Psionics, Auras, Maneuvers (ToB), Domains, Races, Monsters, Templates, Magical Items, Mundane Items
**Why use it**: Covers non-SRD books (Spell Compendium, Tome of Battle, Complete series,
Races of Faerûn, etc.) that d20srd.org does not include.

### URL Patterns for AI Agents

```
# Spells (5,000+ entries including non-SRD)
https://dndtools.one/spells/
https://dndtools.one/spells/[spell-name-hyphenated]/

# Feats by category
https://dndtools.one/feats/categories/general/
https://dndtools.one/feats/categories/fighter/
https://dndtools.one/feats/categories/metamagic/
https://dndtools.one/feats/categories/divine/
https://dndtools.one/feats/categories/domain/
https://dndtools.one/feats/categories/monster/

# Feats by source book (slug--ID format)
https://dndtools.one/feats/[book-slug--ID]/
# e.g. players-handbook-v35--6, monster-manual-v35--5

# Prestige Classes
https://dndtools.one/classes/
https://dndtools.one/classes/[class-name--ID]/

# Monsters
https://dndtools.one/monsters/
https://dndtools.one/monsters/[monster-name--ID]/

# Domains
https://dndtools.one/domains/

# Races
https://dndtools.one/races/

# Psionics (Powers)
https://dndtools.one/powers/

# Maneuvers (Tome of Battle)
https://dndtools.one/maneuvers/

# Magic Items
https://dndtools.one/magical/
```

### When to Use dndtools.one vs d20srd.org

| Situation | Use |
|---|---|
| SRD core spell (Fireball, etc.) | d20srd.org — authoritative text |
| Spell Compendium spell | dndtools.one |
| ToB maneuver (Crusader, Warblade, Swordsage) | dndtools.one |
| Psionic powers or mantles | dndtools.one |
| Feat from Complete Warrior/Adventurer/Divine | dndtools.one |
| Browsing all feats with cross-book filters | dndtools.one |

---

## SOURCE 3 — Forgotten Realms Helps (realmshelps.net)

**URL**: https://www.realmshelps.net
**Scope**: All information pertains to the Realms prior to 1374 DR. No novel-only info, no 4e changes.
**Why use it**: The best FR-specific DM tool for weather, NPC banks, regional encounters, timeline lookup.

### URL Patterns for AI Agents

```
# Character building
https://www.realmshelps.net/charbuild/index.shtml
https://www.realmshelps.net/charbuild/feats.shtml
https://www.realmshelps.net/charbuild/skills.shtml
https://www.realmshelps.net/charbuild/birthday.shtml   ← character birthday/age tool

# Magic
https://www.realmshelps.net/magic/index.shtml
https://www.realmshelps.net/magic/spells.shtml
https://www.realmshelps.net/magic/items.shtml

# FR Lore — Places
https://www.realmshelps.net/faerun/index.shtml
https://www.realmshelps.net/faerun/[region-name].shtml

# FR History timeline (lookup by year + region)
https://www.realmshelps.net/faerun/history.shtml

# Deities database
https://www.realmshelps.net/deities/index.shtml
https://www.realmshelps.net/deities/[deity-name].shtml

# DM Tools
https://www.realmshelps.net/monsters/index.shtml
https://www.realmshelps.net/monsters/by-cr/[cr-number].shtml
https://www.realmshelps.net/npc/index.shtml                   ← Named FR NPC stat blocks
https://www.realmshelps.net/adventuring/faerun_encounters.shtml ← Regional encounter tables
https://www.realmshelps.net/stores/index.shtml                 ← Shop/treasure generator

# Faerûn Weather Generator (Dandello's Almanac)
# Real-time weather by location + in-game date — extremely useful
https://www.realmshelps.net/faerun/weather.shtml
```

### Best Uses for realmshelps.net

- **Session weather**: Generate weather for party's current location and Harptos calendar date
- **NPC lookup**: Stat blocks for named Faerûn personalities
- **Regional encounters**: Monsters by terrain/region in the Dalelands, Thunder Peaks, etc.
- **History**: "What happened in 1342 DR in Cormyr?" — year/region timeline lookup
- **Shopping**: Generate a realistic shop inventory and pricing

---

## SOURCE 4 — Forgotten Realms Wiki (fandom)

**URL**: https://forgottenrealms.fandom.com/wiki/[Article_Name]
(use underscores for spaces; percent-encode special chars)

```
# Key patterns
https://forgottenrealms.fandom.com/wiki/[Deity_Name]
https://forgottenrealms.fandom.com/wiki/[City_Name]
https://forgottenrealms.fandom.com/wiki/[Historical_Event]
https://forgottenrealms.fandom.com/wiki/[NPC_Name]
https://forgottenrealms.fandom.com/wiki/[Year]_DR    ← e.g. 1372_DR
```

**Caution**: Contains ALL edition lore — always filter for 3.5 / pre-1385 DR context.

---

## SOURCE 5 — orbitalflower + web.archive.org (WotC D&D 3.5 Archive)

**Index**: https://orbitalflower.github.io/rpg/wizards-3e-archive.html

During the run of Dungeons & Dragons third edition (2000–2007), Wizards of the Coast's D&D
website posted thousands of free articles including new spells, monster stats, maps, advice
articles, news and errata. This index provides a searchable list of that archived content.

### Archive Categories

Feature articles: Rules of the Game, Elite Opponents, Design & Development, Villain Builder,
Adventure Builder, Vicious Venues, Tactics and Tips, Save My Game, Steal This Hook

Downloads: Original Adventures, Map-A-Week, Web enhancement archive, Art gallery archive,
D&D character sheets, Map gallery archive, D&D 3.5 accessory update booklets

Forgotten Realms Archives: Elminster Speaks, Realmslore, Perilous Gateways, Rand's Travelogue,
Wyrms of the North, Realms Personalities, Magic Books of Faerûn, Class Chronicles, Border
Kingdoms, Return to Undermountain, Waterdeep News, Adventure Locales

### How to Use with web_fetch

```
# Step 1: Load the index to find the article URL
web_fetch: https://orbitalflower.github.io/rpg/wizards-3e-archive.html

# Step 2: Identify the original Wizards URL from the index, e.g.:
# http://www.wizards.com/dnd/article.asp?x=fr/rp/20030428a

# Step 3: Fetch via Wayback Machine (original URLs are dead)
# Format: https://web.archive.org/web/[YYYYMMDD000000]/[original-url]
web_fetch: https://web.archive.org/web/20060501000000*/http://www.wizards.com/dnd/article.asp?x=fr/rp/20030428a

# Step 4: Use the most recent snapshot that returns content (not a redirect)
```

### Most Useful FR Archive Series for RumblingStone

| Series | Content | Use for |
|---|---|---|
| **Elminster Speaks** | In-character FR commentary | NPC voice, obscure lore |
| **Realmslore** | FR setting articles by WotC designers | Deep setting canon |
| **Wyrms of the North** | Dragon stat blocks + individual lore | Dragon encounters |
| **Realms Personalities** | Full stat blocks for named FR NPCs | Ready-to-use NPCs |
| **Map-A-Week** | Downloadable dungeon/regional maps (GIF/JPG) | Session maps |
| **Elite Opponents** | High-CR stat blocks and tactics | Boss encounters |
| **Rules of the Game** | Rules clarifications + edge cases | RAW adjudication |
| **Villain Builder** | Step-by-step villain construction articles | AP villain design |
| **Vicious Venues** | Encounter locations with maps | Ready encounter sites |
| **Perilous Gateways** | FR portal network lore | Travel/planar hooks |
| **Magic Books of Faerûn** | Unique spellbooks as treasure | Wizard loot |
| **Art gallery archive** | Official 3.5 D&D art (monsters, environments) | Visual references |

---

## SOURCE 6 — IMarvinTPA Spell Database

**URL**: https://www.imarvintpa.com/dndLive/spells.php
**Content**: ALL 3.5 spells (SRD and non-SRD; non-SRD shows book reference only)
**Pattern**: `https://www.imarvintpa.com/dndLive/spells.php?ID=[spell_id]`
**Use**: Browse spells by class, level, school across ALL sourcebooks at once

---

## LOCAL AI RAG SETUP (Self-Hosted, Free)

For DMs with legally-obtained PDFs of non-SRD books (FRCS, Red Hand of Doom, etc.):

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen2.5:14b    # 8GB VRAM — good reasoning
# or: ollama pull mistral:7b  # 4GB VRAM — lighter

# Run Open WebUI
docker run -d -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://localhost:11434 \
  ghcr.io/open-webui/open-webui:main

# AnythingLLM for PDF RAG (https://useanything.com)
# Upload: FRCS.pdf, RHoD.pdf, PHB.pdf → connect to Ollama

# System prompt for 3.5 rules agent:
"You are a strict D&D 3.5 Edition rules referee for the Forgotten Realms.
Cite every rule as [Book, page]. Distinguish RAW from RAI explicitly.
Flag non-SRD content. Do not invent mechanics."
```

---

## FREE VIRTUAL TABLETOP TOOLS

| Tool | Type | URL |
|---|---|---|
| Improved Initiative | Combat tracker | improved-initiative.com |
| Owlbear Rodeo | VTT (no account) | owlbear.rodeo |
| Roll20 (free tier) | Full VTT | roll20.net |
| Kenku.fm | Ambient audio | kenku.fm |
| Homebrewery | PDF homebrew creation | homebrewery.naturalcrit.com |
| GM Binder | PDF homebrew creation | gmbinder.com |
| Dungeondraft | Map creation (one-time) | dungeondraft.net |
| Inkarnate (free tier) | Regional maps | inkarnate.com |

---

## LEGAL NOTES

- **d20srd.org content**: OGL 1.0a — freely reproducible
- **Non-SRD books**: Must be legally owned. PDFs at DMs Guild (dmsguild.com) or DriveThruRPG
- **Archived WotC articles**: Free to read; do not reproduce in bulk
- **realmshelps.net, forgottenrealms.fandom.com**: Fan sites; for personal/educational use
- OGL full text: https://www.d20srd.org/ogl.htm
