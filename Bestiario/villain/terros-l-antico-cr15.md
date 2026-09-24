# Terros l'Antico — l'Incudine del Mondo [POINTER — statblocco nell'arco] [RIMANDO]
**Key stats**: → `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md` §7 (i numeri stanno li'; duplicarli qui creerebbe una seconda copia che diverge alla prima errata — ADR-0021).

**Faction**: elemental-earth | **Role**: boss | **Environment**: elemental-earth | **CR**: 15
**Source**: `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md` §7 (statblocco nel master DEFINITIVO — CR 15: PF 345 (30d8+210), Elementale della Terra Avanzato 30 DV, Enorme)
**Status**: POINTER — NON duplicare lo statblock qui. Usare sempre il file d'arco.

## Summary

**Boss del Piano Elementale della Terra**, ARC-07 Parte 4. Il file di fonte e' un'analisi di ricalibrazione: dichiara il target GS, il BAB, i TS e le CD, e porta gia' la correzione D8+D15 (party di **13°**, **3 PG senza Therysol** — non 14° con supporto, come diceva la prima stesura).


Questa voce esiste perche' `build_monster_catalog.py` e `suggest_encounter.py` scansionano `Bestiario/` per popolare il pool degli incontri: senza, una creatura con statistiche scritte non e' raggiungibile da nessuno strumento. Ogni modifica va fatta nel file d'arco.

## Notes

✅ **GS 15 e' il boss giocato — confermato dal DM il 2026-09-17**, contro la cornice narrativa che lo dava a GS 13. Il power-up e' voluto (D8: artefatti unici → scontri duri).

La cornice narrativa dello stesso scontro sta in `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P4-PianoTerra-COMPLETO-alternative.md`; lo statblocco operativo in `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P4-PianoTerra-RICALIBRATO.md` §7. Tre file, un solo scontro: i numeri si correggono in `Terros.md`.

🔎 **Ripuntato al master vivo il 2026-09-18.** Questa voce citava `_ARCHIVIO/`, e la misura ha mostrato che non serviva: **lo statblocco e' nel master DEFINITIVO**, con gli stessi numeri. `ARC07-MATRICE-VERSIONI.md` dichiara quelle righe **MASTER** al passato — «era la versione viva *prima* del consolidamento» — e leggerle al presente faceva puntare il Bestiario a una generazione superata invece che al file che si apre al tavolo.

🔴 **Era due voci, ed era la stessa creatura.** Fino al 2026-09-18 il Bestiario
portava anche `mostri/elementale-terra-anziano-cr13.md`, un secondo record a
**GS 13** con l'avviso «al tavolo vale Terros». Misurando la fonte si e' visto
che non e' un altro mostro nemmeno un po': l'archivio, sotto il titolo
«BOSS FIGHT: ELEMENTALE DELLA TERRA ANZIANO (CR 13)», scrive
***«TERROS ANZIANO - Elementale della Terra Anziano»***. E' Terros prima della
ricalibrazione.

Un avviso dentro una voce non impedisce a `suggest_encounter --cr 13` di
proporla: la regola del repo e' **un soggetto, un record**
(`test_catalogo_una_voce_per_creatura.py`), e il DM ha dichiarato **GS 15**
il 2026-09-17. La voce a GS 13 e' stata quindi rimossa, non deprecata.

⚠️ **Cosa si perde, dichiarato**: la *cornice narrativa* di
`_ARCHIVIO/PortaleForgia-P4-PianoTerra-COMPLETO-alternative.md` §8 — le scene
attorno allo scontro, non i numeri — resta nell'archivio e non e' piu' citata
da nessuna voce del Bestiario. Non e' una perdita di canone: e' una
generazione confluita in `ARC07-DEF-1`, ed e' la matrice delle versioni a
dirlo.
