# Rumbling Stone

**RumblingStone** is a custom D&D 3.5 campaign set in the Forgotten Realms (Faerûn, 1372 DR). 
It is heavily based on *Red Hand of Doom* (Jacobs & Wyatt, 2006) and adapted from the Elsir Vale to the Dalelands region. 
This repository contains session logs, NPC data, encounters, lore, and custom mechanics tailored for an adult gaming group (emphasizing "Premium Design" and "Shine Time" mechanics).

## Campaign Arcs (Directory Structure)

The campaign is organized into chronological and locational arcs:

- **00_Red Hand Of Doom**: The foundation and initial setup of the Red Hand of Doom adaptation.
- **01_LaMiniera**: Exploration and encounters within the local mining facilities.
- **02_scaladossa-abbattor-funghi**: The treacherous ascent and fungal environments.
- **03_la Cittadella**: Infiltration and battles surrounding the enemy stronghold.
- **04_tomba_di_Belkram**: The ancient dwarven burial grounds and its hidden dangers.
- **05_aa-stanza-runica**: Puzzles and magical confrontations in the arcane chambers.
- **06_Stanza-corona-di-adamantio**: The epic encounter surrounding the mythical adamantine artifact.
- **07_il Portale Della Forgia Eterna**: High-stakes planar and elemental battles to secure the eternal forge.
- **08_La Battaglia Di Hammerfist**: Strategic, large-scale warfare defending the dwarven settlement.
- **09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist**: Narrative continuation and aftermath of the major conflict.

## Characters

### PG (Player Characters)
The core heroes of the campaign (Detailed in `PG/`):
- **Artemis** (Warlock 13): The analytical "Senior Developer," focused on stealth, tactical exploitation, and planar commerce.
- **Thorik** (Guerriero 13): The strategic "Manager," navigating military tactics and political diplomacy.
- **Tordek** (Guerriero 4 / Monaco 9): The out-of-the-box "Engineer," manipulating the battlefield environment and hunting ancient loot.
- **Hella** (Ranger / Druido): The moral compass, bound to a stone-infused rhinoceros companion, anchoring the group's ethics.

### PNG (NPCs & Villains)
Important non-player characters and antagonists (Detailed in `PNG/` and `campaign/npcs/`):
- **Maestro Varis "Seta-Argento"**: Opportunistic planar merchant, urban broker in Rethmar, CR 6.
- **Conte Valerius**: Nobility entangled in funding the enemy, demanding social/political finesse to defeat.
- **Il Collezionista (Rakshasa)**: A deadly collector of rare artifacts and secrets, the shadow mastermind, GS 17–19.
- **Salvatore "Sal" della Luna d'Argento** (`PNG/Salvatore/`): Temporal spy and soul-harvester. Flamboyant desert merchant, secretly "Vatore" who witnessed the PCs at Hammerfist -1000 DR. Bard 8/Sublime Chord 1/Spy 5, GS 14. Supplies living statues to Varis. Introduced Day 28–32, Arc 09 P2C.
- **Azarr Kul** (`PNG/Azarr_Kul/`): High Wyrmlord of Tiamat. Half-Blue-Dragon Hobgoblin, Cleric 10/Fighter 4, GS 15. Commands the Red Hand horde; rides Tyrgarun (Ancient Blue Dragon CR 20). Boss of Rethmar Phase 3.
- **Sonjak / Matrona Sajak** (`PNG/Sonjak/`): Drow Cleric Matrona. Cleric 10/Matrona 3, GS 13. Commands underground Drow forces in Cannath Vale; Sal's employer on the surface. Clock 4/8 — triggers Phase 0 Night of the Drow.
- **Conte Valerius** (`PNG/Conte_Valerius/`): Political villain. Expert 4/Aristocrat 4. Legally finances the Red Hand horde through "patriotic emergency loans." Cannot be defeated in combat — requires political/investigative approach. Clock 2/8.
- **Maestro Varis "Seta-Argento"** (`PNG/Varis_Seta_Argento/`): Urban broker in Rethmar. Rogue 4/Expert 4, CR 6. Knowingly sells petrified living creatures as artwork. Potential ally for Artemis; key link in the statue supply chain. Distinct from Sal (who is the field agent/supplier).
- **Ghostlord / Arcano Zeth il Murato** (`PNG/Ghostlord/`): Druidic Lich of the Thornwaste. Druid 13/Lich, GS 13. Ancient master builder of Hammerfist, tricked into lichdom. Ally or enemy depending on party choices; Hella's key NPC. Holds 20 spectral lions as potential reinforcements at Rethmar.
- **Xal'thor** (`PNG/Xal_thor/`): Illithid Githyanki Commander. Psion 6 (effective GS 14). Targets Tordek's Bracieri as planar keys to the Eternal Forge. Fixed trigger: attacks Dauth Tournament Day 3 regardless of party action. Potential wildcard at Rethmar if not stopped.
- **Therysol** (`PNG/Therysol/`): Tiefling Half-Dragon, former Underdark merchant, hunting Il Collezionista. Ally NPC, GS 9.

## Repository Layout & Agent Support

- **`campaign/`**: Core campaign files.
  - `sessions/`: Chronological session logs.
  - `npcs/` & `locations/`: Key figures and environment descriptions.
  - `encounters/`: Custom encounter design and tactics.
  - `lore/`: House rules, setting details, and DM strategy (e.g., `csmpaign players.md`).
- **`skills/dnd-35-rules/`**: This repo ships a full D&D 3.5 rules skill for AI agents. It ensures rules are sourced from the d20 SRD and accurately adjudicates D&D 3.5 mechanics.

## Design Philosophy (Mastering for Adults)
This campaign uses a **Reactive State Machine Design**. It emphasizes severe consequences for actions, intense political intrigue, destructible environments, and "Shine Time" personalized hooks for each player character to eliminate railroading and maximize player agency.

## Setup Instructions

1. Clone the repository to your local machine.
2. If using AI Agents (Claude Code, Cursor, Windsurf), run `./scripts/build-skills.sh` to build per-agent skill packages and deploy them to your user-level paths. Per-agent mirrors are not committed to git — regenerate them locally.
3. Review `AGENTS.md` to understand campaign conventions and agent instructions.

## Licensing Information
This project contains private lore adaptations based on *Red Hand of Doom*. Mechanical content belongs to the respective owners of the D&D 3.5 OGL/SRD.
