# Migrazione delle forme vecchie e righe di regola — 2026-11-07

ADR-0109, schede 2, 4 e 6 = A, fatte dopo la #313 su main.

## Il contatore (scheda 6)

`scripts/inventory_inferred.py` conta come «meta» skill, modelli (`templates/`),
README, fixture dei test e GUIDA-MARCATURE, e lo schema da copiare
`[INFERRED — <domanda>; base: <…>]` dovunque compaia. Ogni marcatore ha anche
una forma: nuova (domanda e base), vecchia, nuda.

| | Prima | Dopo |
|---|---:|---:|
| INFERRED aperti (P16) | 25 | **0** |
| baseline del ratchet | 25 | 0 |

Le 25 erano tutte righe che spiegano come si marca: 14 diventano meta per
cartella, 4 (GUIDA-BESTIARIO) per schema, le altre si riscrivono nella forma
nuova (modelli, guide, ARCHITETTURA, INDEX).

## La migrazione (scheda 2)

`migra_marche.py --scrivi`, fuori da `plans/`, archivi, changelog, script e
volumi generati, righe dentro `<!-- storico -->` escluse. Rapporto riga per
riga in `migrazione.json`.

| Forma vecchia | Prima | Dopo |
|---|---:|---:|
| `[ACCEPTED…]` | 137 | 4 |
| `(decisione DM data)` | 7 | 2 |
| «needs DM confirmation» | 16 | 16 (a mano: 0 fuori dai residui sotto) |

138 righe in 89 file. Da dove viene la data delle marche
che non l'avevano: 84 l'avevano già, 47 dalla data che lo stesso file dà alla
scelta, 4 dal dossier nella stessa cartella («Approvato dal DM il …»),
3 dal primo commit che ha messo `ACCEPTED` nel file (tre schede del Bestiario,
2026-10-06: è la data della marca, non per forza quella della scelta).

Dopo lo script, a mano: Bestiario/README, i due modelli di `campaign/templates/`,
GUIDA-BESTIARIO, ARCHITETTURA, INDEX, README-automation, quattro riferimenti
delle skill, il default di `compile_map_json.py`. `validate_bestiario.py`
accetta `[CANONE` nel titolo (resta letto `[ACCEPTED`, per le prove);
`monster_catalog.yaml` e l'impronta delle creature rigenerati (cambia solo la
lunghezza dei titoli, 40 voci).

**Residui voluti**: le 4 `[ACCEPTED` rimaste sono righe che nominano la forma
vecchia (GUIDA-MARCATURE, i test). `scripts/piante/rethmar.py` scrive ancora
«needs DM confirmation» nella pianta stampata di Rethmar: cambiarlo vuol dire
rigenerare la pianta, e la leva è materia del lotto 3; resta per il thread
delle città. I volumi HTML di ARC-07 e gli archivi non si toccano.

## I cancelli (scheda 4)

`scripts/controlla_marche.py --base origin/<base>` sulle righe cambiate di una
PR: marca INFERRED senza domanda e base, INFERRED tolto senza CANONE, GENERATO
o storico nello stesso file. Passo CI non bloccante (canale testing); dopo due
settimane l'audit settimanale propone se renderlo bloccante.
