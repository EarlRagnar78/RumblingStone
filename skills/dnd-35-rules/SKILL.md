---
name: dnd-35-rules
description: >
  Meta-router legacy (D&D 3.5 Rules), tenuto per compatibilità: documenti e
  vecchie configurazioni degli agenti puntano ancora qui. Non ha contenuto
  proprio: instrada verso le skill focalizzate in cui è stato diviso —
  dnd-35-srd (meccanica), forgotten-realms-lore (ambientazione, 1372 DR),
  rumblingstone-campaign (questa campagna), pathfinder-1e-srd (regole PF1e e
  conversione), npc-villain-boosting (potenziare e avanzare PNG, villain,
  mostri), rumblingstone-narrative-style (motore di stile per i contenuti
  generati), rumblingstone-mapmaking (pipeline delle mappe di battaglia),
  rumblingstone-automation (CLI dm.py e pipeline dello stato di sessione),
  rumblingstone-plans (disciplina dell'archivio dei piani). Si usa con le
  stesse parole d'innesco di quelle skill messe insieme (ADR-0008).
---

# D&D 3.5 Rules — meta-router (legacy)

## Quando no

Mai in un documento nuovo: lì si citano le skill focalizzate. Lo shim si
toglie quando niente nel repo (né una config agent supportata) punta più a
`dnd-35-rules` (ADR-0008).

## Fonti

Nessun reference proprio: il materiale sta nelle skill focalizzate, così si
carica solo quello che serve.

| If the question is about... | Load skill |
|---|---|
| Pure 3.5 mechanics, SRD rules, generic d20 | `dnd-35-srd` |
| Forgotten Realms canon (1372 DR), deities, regions, factions | `forgotten-realms-lore` |
| RumblingStone campaign, the four PCs, custom artifacts, current arc | `rumblingstone-campaign` |
| Pathfinder 1e rules, PF↔3.5 conversion, simple templates, CR benchmarks | `pathfinder-1e-srd` |
| Boosting/advancing a PNG, villain, or monster ("too easy", "upscale", "potenziare") | `npc-villain-boosting` |
| Generating narrative content — quests, prose, read-aloud, dialogue, hooks, recaps ("genera", "scrivi") | `rumblingstone-narrative-style` |
| Battle maps — creating, rendering, JSON contract, UVTT export ("mappa", "griglia") | `rumblingstone-mapmaking` |
| Session lifecycle & scripts — `dm.py`, "fine sessione", recap, brief, `state.md`, Homebrewery | `rumblingstone-automation` |
| Work plans, lotti, INDEX/CHANGELOG, ADRs ("piano", "traccia le modifiche") | `rumblingstone-plans` |

## Procedura

1. Carica la skill della riga giusta.
2. Preparazione della campagna, in quest'ordine:
   1. `rumblingstone-campaign/SKILL.md` (più `references/campaign-coherence.md`
      e `campaign/state.md`): ciò che oggi è vero;
   2. `forgotten-realms-lore/SKILL.md`: la cornice dell'ambientazione;
   3. `dnd-35-srd/SKILL.md`: la cornice delle regole.
3. Ogni *generazione* carica anche `rumblingstone-narrative-style` (motore
   di stile obbligatorio, regola 11 di AGENTS.md).
4. Più alberi toccati: caricali tutti, la divisione non costa nulla in più
   (domanda stretta ~4–12K token invece di ~60K; ADR-0008).

## Formato d'uscita

Nessuno proprio: lo fissa la skill caricata.

## Prima di consegnare

- Risposta dalla skill focalizzata, non da qui?
- Generazione: caricata anche `rumblingstone-narrative-style`?

## Cancelli deterministici

I controlli che non chiedono un giudizio, da far girare prima di consegnare.
Quello che qui non c'è resta giudizio di chi legge (registro delle norme).

- `python3 scripts/conformita_statblocchi.py --master`: pf, CA, lotta, CD di soffio/schiacciare/presenza e sensi degli statblocchi nei master; cricchetto in test_conformita_statblocchi.
- `python3 scripts/riscontro_srd.py`: la regola citata contro l'SRD in cache (ADR-0103).
