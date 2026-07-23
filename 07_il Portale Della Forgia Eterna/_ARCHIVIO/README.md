# `_ARCHIVIO/` — ARC-07 (Il Portale della Forgia Eterna)

## Cos'è
Cartella per i **file-fonte assorbiti** dai 5 master DEFINITIVI dell'arco
(`ARC07-DEF-1…5`). Deroga alla regola D10 concordata col DM: i sorgenti
consolidati si spostano qui **dopo** che il loro contenuto è interamente
confluito nei master e **non è più necessario altrove**.

## Stato attuale (2026-07-23): migrazione FISICA rimandata
Il consolidamento **funzionale** è completo: `ARC07-00-INDICE.md` indica per
ogni beat **quale master DEF giocare** e marca i sorgenti come «assorbiti», e
ogni master porta in fondo la propria lista `FILE-FONTE ASSORBITI`. Quindi al
tavolo non serve più saltare fra generazioni.

Lo **spostamento fisico** dei sorgenti in questa cartella è però **sospeso**,
perché un audit dei riferimenti ha trovato un *blast radius* ampio: p.es.
`PortaleForgia-P3B-ResurrezioneHella-COMPLETO.md` è citato da **29 file** —
non solo dentro l'arco, ma anche nei **mirror delle skill**
(`.claude/.chatgpt/.github/.windsurf` + `build/`), negli **archi 08 e 09**,
in `PG/Artefatti/`, `campaign/lore/` e in `plans/`. Molti sono **record di
canone/log** dove il percorso è una traccia storica, non un puntatore da
riscrivere. Spostare i file senza riscrivere tutti i riferimenti lascerebbe
link penzolanti; riscriverli tutti è un'operazione trasversale ad alto rischio.

### Candidati alla migrazione (quando si deciderà di procedere)
Interamente assorbiti dai DEF (da spostare **con** riscrittura dei riferimenti):
`P4-PianoTerra-COMPLETO-alternative`, `P4-PianoTerra-RICALIBRATO`, `Terros.md`,
`Interludio-Terra`, `P3B-ResurrezioneHella-COMPLETO`,
`P3B-ResurrezioneHella-RICALIBRATO-alternative`, i file `…VIAGGIO-NELL'INCUDINE…`,
`P5-FASTPLAY`, `P5-DEFINITIVO-PARTE1/2`, `P5-RICALIBRATO`, `PortaleForgia-FINAL-P5`,
`P6-INTEGRAZIONE-Completa` (sez. «battaglia antica/1372»).

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
