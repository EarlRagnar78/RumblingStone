# Armate — Composizione Dettagliata (RHoD Army Atlas)

> **🛡️ Canonizzazione 2026-05-05**: il DM ha **accettato** tutte le
> derivazioni precedentemente marcate `[INFERRED]` (unità in
> `Armate-UNITA-NUOVE/`) e tutti i puntatori a `PNG/` come canone di
> campagna. Flag `[INFERRED]` → `[ACCEPTED — DM-canon 2026-05-05]`.
> Le unità restano valide per encounter building e mass combat; i
> numeri §2.x di `Armate-CALCOLI-ESERCITI-DINAMICI.md` sono la verità.

> **Versione**: v1.1 (2026-05-05, canonizzata). Indice maestro di tutte le unità
> potenzialmente in campo nella campagna RumblingStone, organizzate per
> fazione, con link al file statblock canonico (o marcate `[ACCEPTED]`
> quando serve produzione dedicata in `Armate-UNITA-NUOVE/`).
>
> **Regola cardine** (`AGENTS.md`): niente invenzioni. Ogni unit card è
> un puntatore a file esistente o una derivazione marcata
> `[ACCEPTED — DM-canon 2026-05-05]` con base MM/FRCS/AP-RHoD.
>
> **Canonical references**:
>
> - `Armate-CALCOLI-ESERCITI-DINAMICI.md` §2 (totali e composizione orda)
> - `Armate-SINCRONIZZAZIONE-CAMPAGNA.md` (March Clock)
> - `Monsters_Sheets/png_La_mano_rossa_del_destino/` (schede upscalate AP)
> - `08_La Battaglia Di Hammerfist/00_Schede_dei_Personaggi_Unità_…md`
>   (format template + unit cards Hammerfist)
> - `09_Continuazione.../Arco-Post-Hammerfist-P3-*STATBLOCCHI*.md`
>   (boss epici, Ghostlord branch, missioni CR12)

---

## Uso per il DM

1. **Scegli fazione/ambiente** → sezione corrispondente.
2. **Copia l'unit card** (già linkata al file statblock completo).
3. **Mix-and-match per encounter** — usa `scripts/suggest_encounter.py`
   per combinazioni automatiche su EL target.
4. **Unità mancanti**: se serve qualcosa non in atlas, produci una card
   e aggiungi a `Armate-UNITA-NUOVE/`. Lo script cataloga
   automaticamente.

---

## Indice Fazioni

1. [Mano Rossa — Core Hobgoblin](#1-mano-rossa--core-hobgoblin)
2. [Mano Rossa — Ausiliari (goblin/orco/worg)](#2-mano-rossa--ausiliari)
3. [Mano Rossa — Giganti / Mostri grandi](#3-giganti-e-mostri-grandi)
4. [Mano Rossa — Casters & Supporto](#4-casters-e-supporto)
5. [Dragoni (5 AP canon + Fauci)](#5-dragoni)
6. [Razorfiend — Draconic Spawn](#6-razorfiend)
7. [Wyrmlord (comandanti)](#7-wyrmlord)
8. [Drow — Casata Sonjak / Sajak](#8-drow--casata-sonjak)
9. [Gnoll — 3 Tribù mercenarie](#9-gnoll--tribù-mercenarie)
10. [Loxo & Centauri corrotti (Shaar)](#10-loxo--centauri-corrotti)
11. [Githyanki di Vaereth](#11-githyanki-di-vaereth)
12. [Compagnia del Teschio Nero (Thay)](#12-compagnia-del-teschio-nero-thay)
13. [Rakshasa — Il Collezionista](#13-rakshasa--il-collezionista)
14. [Aberrazioni — Ghostlord / Underdark](#14-aberrazioni)
15. [Alleati Difensori (Rethmar & Alleanze)](#15-alleati-difensori)
16. [Endgame — Boss Epici & Élite CR 10-18](#16-endgame--boss-epici--élite-cr-10-18)

---

## 1. Mano Rossa — Core Hobgoblin

| Unità | CR | Statblock file | Note |
|---|---|---|---|
| Hobgoblin Regular (Warrior 1/Fighter 1) | 1 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin regular 3 liv.htm` | Fanteria base orda (~3.600) |
| Hobgoblin Regular 4° liv | 2 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin regular 4 liv.pcg` | Upgrade pre-Hammerfist |
| Hobgoblin Veterans 6° liv | 4 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin veterans 6 liv.htm` | 900 unità |
| Hobgoblin Bladebearer 6° | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin bladebearer 6 liv.htm` | Greatsword specialists |
| Hobgoblin Bladebearer (longsword) | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin bladebearer 6 liv longsword.htm` | Variante |
| Hobgoblin Doom Hand Cleric 5° | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin doom hand cleric 5 liv.htm` | Warpriest di Tiamat + spells |
| Hobgoblin Shamano Draconico cr8 | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/hobgoblin shamano draconico cr8 .htm` | Caster cluster leader |
| Hobgoblin Sergente (Fighter 5) | 5 | [ACCEPTED] `Armate-UNITA-NUOVE/hobgoblin-sergente-cr5.md` | 240 unità, capo compagnia |
| Bugbear Draconico Koth | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/bugbear_draconic_koth.pcg` | NPC nominato |

---

## 2. Mano Rossa — Ausiliari

| Unità | CR | Statblock file | Note |
|---|---|---|---|
| Goblin Warrior 1 | 1/2 | [ACCEPTED] `Armate-UNITA-NUOVE/goblin-warrior1.md` | MM Goblin |
| Goblin Worg Rider | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/goblin worg raider cr5.htm` | 300 unità |
| Worg (cavalcatura) | 2 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Worg.htm` | MM |
| Orc Regular | 1/2 | `Monsters_Sheets/png_La_mano_rossa_del_destino/orc_regular.pcg` | MM Orc |
| Orc Berserk Warrior 2 | 2 | `Monsters_Sheets/png_La_mano_rossa_del_destino/orc_berserk 2 liv.pcg` | 700 unità |

---

## 3. Giganti e Mostri Grandi

| Unità | CR | Statblock file | Note |
|---|---|---|---|
| Hill Giant (MM) | 7 | [REF MM p.123] | 80 unità |
| Ogre | 3 | [REF MM p.199] | 70 unità |
| Ogre Skullcrusher | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Ogre, Skullcrusher cr5.html` | Variante RHoD |
| Ettin standard | 6 | [REF MM p.106] | 30 coppie |
| Ettin Barbaro a 3 teste (Gorthak) | 10 | `Monsters_Sheets/Triple-Headed Ettin Barbarian (3.5e).pdf` | NPC unico |
| Manticore | 5 | [REF MM p.179] | 40 unità |
| Wyvern selvatico addestrato | 6 | [REF MM p.259] | 50 unità |
| Hell Hound standard | 3 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Hell Hound.htm` | 30 unità |
| Hell Hound Draconico cr4 | 4 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Hell Hound 4cr .htm` | Variante mezzo-immondo |
| Hell Hound Mezzo-immondo cr4 | 4 | `Monsters_Sheets/png_La_mano_rossa_del_destino/00_Hell Hound-mezzoimmondi-cr4.pcg` | Élite |
| Chimera | 7 | [REF MM p.34] | 20 unità |
| Minotauro Karkilan cr5 | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Minotaur karkilan cr5.htm` | NPC/unità élite |
| Monaco Pugno del Destino cr7 | 7 | `Monsters_Sheets/png_La_mano_rossa_del_destino/monaco pugno del destino cr7.htm` | Sicario di Azarr Kul |

---

## 4. Casters e Supporto

| Unità | CR | Statblock file | Note |
|---|---|---|---|
| KulkorZhul War Adept cr8 | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/KulkorZhul war Adept cr8_spell.htm` | Base, 25 unità totali |
| KulkorZhul War Adept cr9 — Fire | 9 | `Monsters_Sheets/png_La_mano_rossa_del_destino/KulkorZhul war Adept cr9 fire.htm` | Specializzato |
| KulkorZhul War Adept cr9 — Acid | 9 | `Monsters_Sheets/png_La_mano_rossa_del_destino/KulkorZhul war Adept cr9 acid.htm` | Variante |
| KulkorZhul War Adept cr9 — Ice | 9 | `Monsters_Sheets/png_La_mano_rossa_del_destino/KulkorZhul war Adept cr9 ice.htm` | Variante |
| KulkorZhul War Adept cr9 — Lightning | 9 | `Monsters_Sheets/png_La_mano_rossa_del_destino/KulkorZhul war Adept cr9 lightining.htm` | Variante |
| Draxoksus (shamano draconico mezzo-immondo) | 7 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Draxoksus.htm` | NPC cluster leader |
| Blue (psionic goblinoid) | 1 | [ACCEPTED] `Armate-UNITA-NUOVE/blue-psion-cr1.md` | MM II p.38; 10 unità |
| Warpriest di Tiamat (Cleric 7) | 7 | [ACCEPTED] `Armate-UNITA-NUOVE/warpriest-tiamat-cr7.md` | 20 unità; PHB Cleric |
| Lómyn RedTongue (Bard 8) | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Lómyn redTongue bard 8.pcg` | NPC bardo |

---

## 5. Dragoni

| Drago | Tipo / Età | CR | File | Stato campagna |
|---|---|---|---|---|
| **Abithriax** | Red Adult | 15 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Arbitrax Drago Rosso.htm` | Vivo, Rethmar Fase 1 |
| **Regiarix** | Black Young Adult | 10 | `09_.../Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` | A rischio (P2 Rhest) |
| **Ozyrrandion** | Blue Adult (AP) / green cr8 variant | 8-14 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Ozyrrandion drago Verde cr8.pcg` + `green dragon.htm` | A rischio (P2A Torre) |
| **Tyrgarun** | **Blue Old (terrore dei cieli, D11 v2)** | **18** | [ACCEPTED] `Armate-UNITA-NUOVE/tyrgarun-blue-old-cr18.md` | Vivo; hazard aereo Fasi 1-3, inchiodato dal Mythal in Fase 4 (CR eff. ~16-17) — NON cavalcatura di Azarr Kul |
| **Fauci di Palude** | Black Adult avanzato | 15 | `08_…/00_Schede_dei_Personaggi_Unità_…md` §1 | Ramo condizionale D10, non deciso (default: fugge <50 PF, assente da Rethmar; alternativa: ucciso ad Hammerfist) |
| Draon-hamann (cr8) | Red Young (escort) | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Draon-hamann-cr8.pcg` | Gith mount |
| Green dragon (generic) | — | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/green dragon.htm` | Swap pool |

---

## 6. Razorfiend (Draconic Spawn)

Varianti colore Tiamat. Base template + delta per colore.

| Variante | CR | File | Assegnazione |
|---|---|---|---|
| Razorfiend base (Black) | 8 | `09_…/Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-RAZORFIEND-NIDO.md` | Saarvith/Rhest |
| Razorfiend Black (alt statblock) | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Incontro-RedHandof-doom/` | — |
| Razorfiend Red | 9 | [ACCEPTED] `Armate-UNITA-NUOVE/razorfiend-red-cr9.md` | Wyrmlord Karruk |
| Razorfiend Blue | 9 | [ACCEPTED] `Armate-UNITA-NUOVE/razorfiend-blue-cr9.md` | Ozyrrandion/Tower |
| Razorfiend White | 8 | [ACCEPTED] `Armate-UNITA-NUOVE/razorfiend-white-cr8.md` | Azarr Kul guard |
| Razorfiend Green | 9 | [ACCEPTED] `Armate-UNITA-NUOVE/razorfiend-green-cr9.md` | Azarr Kul support |

---

## 7. Wyrmlord (comandanti)

| Wyrmlord | CR | File | Ruolo |
|---|---|---|---|
| Azarr Kul (Gran Signore) | 17 | `09_…/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md` | Boss finale Fase 3 |
| Koth (Signore dei Dragoni) | 9 | `Monsters_Sheets/png_La_mano_rossa_del_destino/signore dei Dragoni Koth.htm` | Vraath Keep / field commander |
| Saarvith | 11 | `09_…/Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` | Rhest boss |
| Zalkatar | 13 | `09_…/Arco-Post-Hammerfist-P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` | Torre Invisibile boss |
| Karruk | 10 | [ACCEPTED] `Armate-UNITA-NUOVE/wyrmlord-karruk-cr10.md` | Rethmar Fase 1 assault leader |
| Ulwai Stormcaller (Bard) | 8 | Base: `Lómyn redTongue bard 8.pcg` | Variante nominata |

---

## 8. Drow — Casata Sonjak

Matrona Sajak, Sonjak (enforcer). ~305 unità + élite.

| Unità | CR | File | Note |
|---|---|---|---|
| Underdark Cleric 5° (Ainin) | 5 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Underdark cleric cr5 Ainin.htm` | Sacerdotessa minore |
| Underdark Cleric 6° (Ainin) | 6 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Underdark cleric cr6 Ainin.htm` | Upgrade |
| Underdark Deep Warden Brieyn | 7 | `Monsters_Sheets/png_La_mano_rossa_del_destino/underdark deep warden brieyn.htm` | Ranger-type |
| Underdark Dovil Runecaster (Deep Diviner) | 7 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Underdark dovil runecaster deep diviner cr7.htm` | Wizard |
| Drow Warrior (base) | 1 | [ACCEPTED] `Armate-UNITA-NUOVE/drow-warrior-cr1.md` | FRCS; fanteria drow |
| Drow Fighter 3 | 4 | [ACCEPTED] `Armate-UNITA-NUOVE/drow-fighter3-cr4.md` | Guardia casata |
| Drow Priestess 9 of Lolth | 11 | [ACCEPTED] `Armate-UNITA-NUOVE/drow-priestess9-cr11.md` | Sajak rituali Fase 0 |
| Drow Wizard 7 | 8 | [ACCEPTED] `Armate-UNITA-NUOVE/drow-wizard7-cr8.md` | Supporto mago |
| Drow Noble House Guard | 5 | [ACCEPTED] `Armate-UNITA-NUOVE/drow-noble-guard-cr5.md` | Élite Sajak |
| Sonjak (enforcer) | 12 | `PNG/Sonjak/` (link dir) | NPC nominato |

Statblocchi già presenti per drow in P3 Fase 0:

- `09_…/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE0-NOTTE-DEI-DROW-TESTO.md`
- `09_…/Arco-Post-Hammerfist-P3-MISSIONI-BREVI-CR12-STATBLOCCHI-FUNGHI-GITH-DROW.md`
- `09_…/Arco-Post-Hammerfist-P3-Sabotaggio-Campi-Drow-STATBLOCCHI.md`

---

## 9. Gnoll — Tribù Mercenarie

3 tribù: **Flinderoso** (500), **Abbattitori** (350), **Artigli Neri** (250). Totale 1.100.

| Unità | CR | File | Note |
|---|---|---|---|
| Gnoll base (MM) | 1 | [REF MM p.130] | Warrior tier 0 |
| Gnoll Warrior 2 | 2 | [ACCEPTED] `Armate-UNITA-NUOVE/gnoll-warrior2-cr2.md` | Fanteria tribale |
| Gnoll Ranger 4 | 5 | [ACCEPTED] `Armate-UNITA-NUOVE/gnoll-ranger4-cr5.md` | Scout Artigli Neri |
| Gnoll Cleric 6 of Yeenoghu | 7 | [ACCEPTED] `Armate-UNITA-NUOVE/gnoll-cleric-yeenoghu-cr7.md` | Shaman tribale |
| Flind (MM II) | 3 | [ACCEPTED] `Armate-UNITA-NUOVE/flind-cr3.md` | MM II p.104; Flinderoso élite |
| Gnoll Hyenodon Rider | 4 | [ACCEPTED] `Armate-UNITA-NUOVE/gnoll-hyenodon-rider-cr4.md` | Cavalry Abbattitori |
| Gnoll Chieftain (Barbarian 8) | 10 | [ACCEPTED] `Armate-UNITA-NUOVE/gnoll-chieftain-cr10.md` | Comandante tribù |
| Hyenodon (mount) | 3 | [REF MM p.153 Dire Hyena adattato] | Cavalcatura |

---

## 10. Loxo & Centauri Corrotti

Contingente Shaar, ~480 unità. Revolt trigger se PG diplomazia.

| Unità | CR | File | Note |
|---|---|---|---|
| Loxo Warrior 3 | 4 | [ACCEPTED] `Armate-UNITA-NUOVE/loxo-warrior3-cr4.md` | MM II Loxo + Warrior 3 |
| Loxo Shaman 6 | 7 | [ACCEPTED] `Armate-UNITA-NUOVE/loxo-shaman6-cr7.md` | Druid variant |
| Centaur Ranger 4 (corrotto) | 5 | [ACCEPTED] `Armate-UNITA-NUOVE/centaur-ranger4-corrupted-cr5.md` | MM Centaur + Ranger 4 |
| Centaur Chieftain (Fighter 6) | 7 | [ACCEPTED] `Armate-UNITA-NUOVE/centaur-chieftain-cr7.md` | Leader band |

---

## 11. Githyanki di Vaereth

Dragonrider corps, ~375 unità (cavaliere + 1 red young dragon + reclute).

| Unità | CR | File | Note |
|---|---|---|---|
| Githyanki Warrior 3 | 4 | [ACCEPTED] `Armate-UNITA-NUOVE/githyanki-warrior3-cr4.md` | MM p.128 + Fighter 3 |
| Githyanki Captain (Gish, Ftr8/Wiz3) | 12 | [ACCEPTED] `Armate-UNITA-NUOVE/githyanki-captain-gish-cr12.md` | Élite |
| Githyanki Knight | 10 | `09_…/Arco-Post-Hammerfist-P3-MISSIONI-BREVI-CR12-STATBLOCCHI-FUNGHI-GITH-DROW.md` | File esistente |
| Red Young Dragon (mount) | 8 | `Draon-hamann-cr8.pcg` | Cavalcatura |
| Vaereth (leader gith) | 14 | `09_…/Arco-Post-Hammerfist-P3-MISSIONI-BREVI-CR12-STATBLOCCHI-FUNGHI-GITH-DROW.md` | NPC nominato |

---

## 12. Compagnia del Teschio Nero (Thay)

650 unità; heavy infantry + 6 Red Wizard + comandante. Si unisce Day 27-32.

| Unità | CR | File | Note |
|---|---|---|---|
| Thayan Heavy Infantry (Fighter 3) | 3 | [ACCEPTED] `Armate-UNITA-NUOVE/thayan-heavy-infantry-cr3.md` | Human Fighter 3 |
| Thayan Red Wizard 7 (Evoker) | 9 | [ACCEPTED] `Armate-UNITA-NUOVE/thayan-red-wizard7-cr9.md` | FRCS Red Wizard PrC |
| Teschio Nero Commander (Ftr 8/Bbn 2) | 10 | [ACCEPTED] `Armate-UNITA-NUOVE/teschio-nero-commander-cr10.md` | CR 10 boss |
| Thayan Knight (PrC) | 8 | [ACCEPTED] `Armate-UNITA-NUOVE/thayan-knight-cr8.md` | Complete Warrior |

---

## 13. Rakshasa — Il Collezionista

Incursione condizionale (+300 cultisti Rakshasa se trigger).

| Unità | CR | File | Note |
|---|---|---|---|
| Il Collezionista (Rakshasa) | 13+ | `PNG/Il_Collezionista_Rakshasa.md` | NPC nominato |
| Cultista Rakshasa (human Rog 3) | 3 | [ACCEPTED] `Armate-UNITA-NUOVE/cultista-rakshasa-cr3.md` | Minion |
| Tiger guardian | 4 | [REF MM p.281] | Compagno |

---

## 14. Aberrazioni

Fonte principale: file Arc-04/05/06/07 + `Monsters_Sheets/` vari.

| Unità | CR | File | Origine arc |
|---|---|---|---|
| Myconid Sovereign | 7 | `Monsters_Sheets/Myconid Sovereign.html` | Fughi colony |
| Phantom Fungus | 3 | `Monsters_Sheets/Phantom Fungus d20srd.org.html` | Fughi |
| Bebilith (Guardiano Rovine) | 10 | `Monsters_Sheets/00_cr10_guardiano_delle_rovine_prima della cattedrale_SRD_Bebilith - D&D Wiki.htm` | Cattedrale |
| Retriever | 11 | `Monsters_Sheets/00_Cr11_ordinato_dai_chierici_di_abbathor_di_riportare_Eagis_fang_al_loro_re_SRD_Retriever - D&D Wiki.htm` | Eagis Fang |
| Beholder, Death Tyrant | 13 | `Monsters_Sheets/00_difensoreDelTempio_Beholder,Death Tyrant-cr13.pdf` | Difensore Tempio |
| Antenato Nanico (Belkram) | 13 | `04_tomba_di_Belkram/Antenato_Nanico_cr13.html` | Tomba |
| Xorn | 6 | `04_tomba_di_Belkram/xorn talent.txt` | Tomba |
| Black Pudding | 7 | `04_tomba_di_Belkram/Black Pudding Black Pudding.txt` | Tomba |
| Cubo Gelatinoso (power-up) | 3+ | `04_tomba_di_Belkram/00_Cubo Gelatinoso powerup.txt` | Tomba |
| Celebromorfosi (brain-transformed) | vari | `04_tomba_di_Belkram/00_Celebromorfosi/` | Arc-04 |
| Grell Necromante / Patriarca | 7/9 | `01_LaMiniera/grell necromante.txt` / `grellPatriarca.txt` | Miniera |
| Bone Naga (Ghostlord) | 10 | [ACCEPTED] `Armate-UNITA-NUOVE/bone-naga-cr10.md` | MM II |
| Deathlock | 8 | [ACCEPTED] `Armate-UNITA-NUOVE/deathlock-cr8.md` | MM III |
| Skeletal Dire Lion | 6 | [ACCEPTED] `Armate-UNITA-NUOVE/skeletal-dire-lion-cr6.md` | Pride Ghostlord |
| Spectre | 7 | [REF MM p.232] | Ghostlord pride |
| Allip | 3 | [REF MM p.11] | Minion non-morto |

Ghostlord branch completo:

- `09_…/Arco-Post-Hammerfist-P3-Ghostlord-LICH-ALLEANZA-STATBLOCCHI.md`

---

## 15. Alleati Difensori

Per l'uso in Rethmar Fase 1-4 (difensori) o encounter di supporto.

| Unità | CR | File | Contingente |
|---|---|---|---|
| Rethmar Militia (Warrior 1) | 1/2 | [ACCEPTED] `Armate-UNITA-NUOVE/rethmar-militia-cr05.md` | 1.200 guarnigione |
| Rethmar City Guard (Fighter 2) | 2 | [ACCEPTED] `Armate-UNITA-NUOVE/rethmar-city-guard-cr2.md` | Guardia |
| Conte Valerius (Captain Ftr 10) | 10 | `PNG/Conte_Valerius/` | NPC nominato |
| Starsong Elf Ranger 6 | 7 | `09_…/Arco-Post-Hammerfist-P3-Starsong-Hill-ALLEANZA-ELFI-STATBLOCCHI.md` | +500 alleanza |
| Starsong Owl Cavalry (celestial) | — | Idem | Aerial |
| Maewen (Ranger/Scout) | 9 | `PNG/Maewen/` | NPC |
| Lythiel | — | `PNG/Lythiel/` | NPC |
| Dauth Dwarf Defender (Ftr 6) | 6 | [ACCEPTED] `Armate-UNITA-NUOVE/dauth-dwarf-defender-cr6.md` | +400 Dauth |
| Morlin Coalhewer (dwarf cr12) | 12 | `Monsters_Sheets/png_La_mano_rossa_del_destino/nano Morlin Coalhewer cr12.htm` | NPC |
| Rurik Gorunn (Martello di Moradin 10) | 10 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Rurik Gorunn martello di moradin 10 liv.htm` | NPC |
| Jorr Natherson (Ranger 8) | 8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/Jorr Natherson 8liv.htm` | NPC |
| Capitan Loranna Anitah | ~8 | `Monsters_Sheets/png_La_mano_rossa_del_destino/capitan loranna anitah.htm` | NPC |
| Druido Avarthel cr9 | 9 | `Monsters_Sheets/png_La_mano_rossa_del_destino/druido Avarthel cr9.htm` | Cerchio Sacro support |
| Cerchio Sacro Druid 7 (Hella ally) | 7 | [ACCEPTED] `Armate-UNITA-NUOVE/cerchio-druid7-cr7.md` | +150 |
| Treant (ally) | 8 | [REF MM p.244] | +Cerchio Treant |
| Tempestas (Bardo/Arcimago) | 15 | `PNG/Tempestas/` + `08_…/00_Schede_dei_Personaggi…md` §2 | NPC |
| Signore Ventolesto (Gufo Celestiale Alpha) | 8 | `08_…/00_Schede_dei_Personaggi…md` §2 | NPC |
| Orion Pelleorsa (Druido umano) | 9 | `08_…/00_Schede_dei_Personaggi…md` §2 | NPC |
| Capitano Lunapiena (Ranger elfico) | 10 | `08_…/00_Schede_dei_Personaggi…md` §2 | NPC |
| Dana Forgiapietra (Madre Superiora) | 12 | `08_…/00_Schede_dei_Personaggi…md` §2 | NPC |
| Re Thorek Hammerfist | 13 | `08_…/00_Schede_dei_Personaggi…md` §2 | NPC |
| Borin Ferropugno (Ftr/Champion) | 8 | `08_…/00_Schede_dei_Personaggi…md` §3 | NPC giocabile |
| Dara Occhiolesto (Ranger) | 8 | `08_…/00_Schede_dei_Personaggi…md` §3 | NPC giocabile |
| Thorin Runaforte (Cleric) | 8 | `08_…/00_Schede_dei_Personaggi…md` §3 | NPC giocabile |
| Nala Cantapietre (Bard) | 8 | `08_…/00_Schede_dei_Personaggi…md` §3 | NPC giocabile |

---

## 16. Endgame — Boss Epici & Élite CR 10-18

Unità **alto-CR** (10-18) aggiunte per il tier finale della campagna
(PG livello 13 in ingresso; Arc 09 Fase 2-3 + finale Rethmar).
Tutti marcati `[ACCEPTED — DM-canon 2026-05-05]`; fonte AP RHoD + SRD/MM/FRCS.

### 16a. Mano Rossa — Epic Tier

| Unità | CR | File | Arc |
|---|---|---|---|
| Hobgoblin Captain | 8 | `Armate-UNITA-NUOVE/hobgoblin-captain-cr8.md` | 08/09 Fase 1 |
| Warpriest di Tiamat (upscale) | 11 | `Armate-UNITA-NUOVE/tiamat-warpriest-elite-cr11.md` | 09 Fase 2+ |
| Emissario Red Hand | 12 | `Armate-UNITA-NUOVE/emissario-red-hand-cr12.md` | 09 P3 Ghostlord |
| Zarim (Illithid luogotenente) | 12 | `Armate-UNITA-NUOVE/zarim-illithid-luogotenente-cr12.md` | 09 P2B Torneo |
| Xal'thor (Illithid Commander) | 14 | `Armate-UNITA-NUOVE/xal-thor-illithid-commander-cr14.md` | 09 P2B Day 3 |
| Ondata Giganti — mass wave | 15 | `Armate-UNITA-NUOVE/ondata-giganti-fanteria-cr15.md` | 09 Fase 1-3 |
| Azarr Kul (finale) | 15 | `Armate-UNITA-NUOVE/azarr-kul-final-cr15.md` | 09 Fase 3 |
| Avatar di Tiamat | 17 | `Armate-UNITA-NUOVE/avatar-tiamat-cr17.md` | 09 Fase 3 climax |

### 16b. Ghostlord Branch (Undead Aberration)

| Unità | CR | File | Arc |
|---|---|---|---|
| Ghost Lion Spettrale | 8 | `Armate-UNITA-NUOVE/ghost-lion-spettrale-cr8.md` | 09 P3 Ghostlord |

### 16c. Alleati Epici & Arcani

| Unità | CR | File | Ruolo |
|---|---|---|---|
| Capitana Lorana | 7 | `Armate-UNITA-NUOVE/capitana-lorana-cr7.md` | Rethmar ally, milizia |
| Therysol (tiefling mezzo-drago) | 9 | `Armate-UNITA-NUOVE/therysol-tiefling-mezzodrago-cr9.md` | Rakshasa hunter ally |
| Githyanki Knight Elite | 10 | `Armate-UNITA-NUOVE/githyanki-knight-elite-cr10.md` | Rethmar wave |
| Dauth Commander (mercenari nani) | 11 | `Armate-UNITA-NUOVE/dauth-commander-mercenari-nani-cr11.md` | Rethmar ally |
| Druid-Bear Ally (wildshape tank) | 12 | `Armate-UNITA-NUOVE/druid-bear-ally-cr12.md` | Cerchio Sacro |
| Arci-Druido Circolo | 14 | `Armate-UNITA-NUOVE/arci-druido-circolo-cr14.md` | Cerchio Sacro boss |
| Arcimago Circolo degli Otto | 14 | `Armate-UNITA-NUOVE/arcimago-circolo-otto-cr14.md` | Starsong/Circle ally |

### 16d. Villain Politici / Shadow Masters

| Unità | CR | File | Ruolo |
|---|---|---|---|
| Conte Valerius (political) | 14 | `Armate-UNITA-NUOVE/conte-valerius-cr14-political.md` | NON risolvere in combat — social DC 30 |
| Il Collezionista (Rakshasa) | 18 | `Armate-UNITA-NUOVE/il-collezionista-rakshasa-cr18.md` | Shadow mastermind Phase 3 |

> **Nota design**: in Arc 09 Fase 2-3 i PG sono livello 13-15. Gli
> encounter EL 13-15 vanno assemblati preferendo un boss CR 13-15 +
> supporto CR 10-12 (vedere §16a/c), oppure wave dinamiche come
> `ondata-giganti-fanteria-cr15.md` per risoluzione via mass-combat.
> Avatar di Tiamat e Il Collezionista sono **eventi di climax**, non
> encounter ordinari.

---

## Mapping Arc → Atlas (quick reference)

| Arc | Fazioni principali in campo |
|---|---|
| 01 Miniera | Aberrazioni (Grell), Mano Rossa minore |
| 02 Scaladossa | Duergar, Fungi (Aberrazioni §14) |
| 03 Cittadella | Aberrazioni (Bebilith, Beholder, Shadow Marsh) |
| 04 Tomba Belkram | Aberrazioni (Xorn, Black Pudding, Antenato, Celebromorfosi) |
| 05 Stanza Runica | (TBD — catalogare in Step 2) |
| 06 Corona Adamantio | Aberrazioni, guardiani |
| 07 Portale Forgia | Aberrazioni, Fauci (pre-ritorno), Terros |
| 08 Hammerfist | Mano Rossa §1-4, Fauci §5, Ogre/Ettin §3, Difensori §15 |
| 09 P1 Hella | Druidi §15, Mano Rossa skirmish §1-2 |
| 09 P2 Rhest | Drow §8 (Saarvith subset), Razorfiend §6, Regiarix §5 |
| 09 P2A Torre | Ozyrrandion §5, Zalkatar §7, Aberrazioni (Illithid) |
| 09 P2B Dauth | Difensori nani §15, Villain torneo (vedi file P2B-VILLAIN) |
| 09 P3 Fase 0 | Drow Sonjak §8 full |
| 09 P3 Fase 1 | Mano Rossa assault §1-4, Abithriax §5, Razorfiend §6 |
| 09 P3 Fase 2 | Ghostlord §14, Ritualisti (warpriest §4) |
| 09 P3 Fase 3 | Azarr Kul §7, Razorfiend §6 (green/white) |
| 09 P3 Fase 4 | Boss epici + Mythal + §16a-d (Azarr Kul CR15, Tiamat CR17, Rakshasa CR18) |

---

## TODO (da espandere)

- [ ] Finalizzare tutti gli [ACCEPTED] in `Armate-UNITA-NUOVE/` (file separati).
- [ ] Catalogare anche `04_tomba_di_Belkram/00_Celebromorfosi/` e `02_Celebromorfosi/` (script Step 2 lo fa automaticamente).
- [ ] Integrare `05_aa-stanza-runica/` e `06_Stanza-corona-di-adamantio/` (inspection).
- [ ] Collegamento ODS `Armate-AGGIORNATO.ods` → atlas (rebuild manuale DM).
