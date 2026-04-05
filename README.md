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
- **Maestro Varis "Seta-Argento"**: Opportunistic planar merchant.
- **Conte Valerius**: Nobility entangled in funding the enemy, demanding social/political finesse to defeat.
- **Il Collezionista (Rakshasa)**: A deadly collector of rare artifacts and secrets.

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
2. If using AI Agents (Claude Code, Cursor, Windsurf), run `./scripts/deploy-skills.sh` to install the `dnd-35-rules` skill to your user-level paths.
3. Review `AGENTS.md` to understand campaign conventions and agent instructions.

## Licensing Information
This project contains private lore adaptations based on *Red Hand of Doom*. Mechanical content belongs to the respective owners of the D&D 3.5 OGL/SRD.
