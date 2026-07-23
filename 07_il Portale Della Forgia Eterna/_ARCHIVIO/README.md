# `_ARCHIVIO/` — ARC-07 (Il Portale della Forgia Eterna)

## Cos'è
Cartella per i **file-fonte assorbiti** dai 5 master DEFINITIVI dell'arco
(`ARC07-DEF-1…5`). Deroga alla regola D10 concordata col DM: i sorgenti
consolidati si spostano qui **dopo** che il loro contenuto è interamente
confluito nei master e **non è più necessario altrove**.

## Stato attuale (2026-07-23): migrazione FISICA ESEGUITA ✅
Il consolidamento **funzionale** è completo (`ARC07-00-INDICE.md` indica per
ogni beat quale master DEF giocare) **e** i 16 sorgenti assorbiti sono stati
**spostati fisicamente** qui, con **riscrittura dei riferimenti**:
- i **link a percorso pieno** nei file *tracciati* (skill-source
  `skills/rumblingstone-campaign/references/`, archi 08/09, `PG/Artefatti/`,
  `campaign/lore/`) ora puntano a `_ARCHIVIO/…`;
- i **riferimenti interni** all'arco (master DEF, MATRICE, ERRATA, fascicoli)
  sono stati prefissati a `_ARCHIVIO/…`;
- i **mirror delle skill** (`.claude/.chatgpt/.github/.windsurf`) e `build/`
  sono **gitignored/generati**: si rigenerano da sorgente con
  `scripts/build-skills.sh` (non si editano a mano);
- i **log append-only** (`campaign/state.md §8`, `plans/CHANGELOG.md`,
  `campaign/sessions/…`) sono **lasciati intatti** come record storici.

### File spostati qui (16)
`PortaleForgia-P4-PianoTerra-COMPLETO-alternative`, `…-RICALIBRATO`, `Terros.md`,
`PortaleForgia-Interludio-Terra`, `PortaleForgia-P3B-ResurrezioneHella-COMPLETO`,
`…-RICALIBRATO-alternative`, i 4 file `…VIAGGIO-NELL'INCUDINE…` (base, v2, 2×
risultati), `PortaleForgia-P5-FASTPLAY`, `…-P5-DEFINITIVO-PARTE1/2`,
`…-P5-RICALIBRATO`, `PortaleForgia-FINAL-P5`, `PortaleForgia-P6-INTEGRAZIONE-Completa`.

### Restano VIVI (NON archiviare)
`La_Piramide_Ricalibrata.md` (master del Fuoco/P3), `P5-B4-CARRYOVER-Forgia-Ricorda.md`
(tabella DM-approved citata anche dall'ARC-08), le schede in `PG/Artefatti/`,
`Bestiario/villain/Salvatore/Salvatore.md`, e i beat **pre-perimetro**
`PortaleForgia-P1/P2/P3-*` (arrivo iniziale + Piano del Fuoco, che precedono
il consolidamento).

> **Decisione al DM**: (a) tenere lo stato attuale (redirect via INDICE, cartella
> vuota) oppure (b) procedere con lo spostamento fisico + una passata di
> riscrittura dei riferimenti (skill-mirror inclusi, con `validate_skills` e
> rebuild dei pacchetti). Finché non si decide (b), questa cartella resta un
> segnaposto documentato.
