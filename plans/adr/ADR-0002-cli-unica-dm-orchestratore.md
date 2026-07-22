# ADR-0002 — `scripts/dm.py`: CLI unica come orchestratore, mai come logica

**Stato**: accettata
**Data**: 2026-07-10
**Decisione-fonte**: K-D1 (DM 2026-07-10, domanda 1)

## Contesto

La prep di sessione richiede 8+ comandi in ordine (catalogo → incontri →
mappe → loot; poi XP → state-sync → recap), documentati solo come prosa
nel Playbook. Due famiglie di script con nomi in collisione (`scripts/`
automazione DM, `Script/` convertitori) confondono umani e agenti. Fondere
le cartelle toccherebbe decine di path interni per un beneficio estetico.

## Decisione

Un solo entrypoint `scripts/dm.py` (stdlib only: argparse + subprocess)
con sottocomandi mappati sulle fasi del Playbook (`prep`, `maps`, `post`,
`recap`, `handout`, `skills`, `doctor`). **Solo orchestrazione**: dm.py
invoca gli script esistenti e non duplica una riga della loro logica.
Gli script restano dove sono e restano invocabili singolarmente.
`Script/` (convertitori) non si sposta: nota di disambiguazione nei README.

## Conseguenze

- Un DM nuovo impara un solo comando; `dm.py doctor` diagnostica l'ambiente.
- Zero rotture: ogni flusso esistente continua a funzionare identico.
- Costo: dm.py va tenuto allineato quando si aggiunge uno script nuovo
  (checklist: aggiungere il sottocomando o documentare perché no).
- L'eventuale fusione `Script/`+`scripts/` resta possibile in futuro con
  un ADR dedicato — non è preclusa, solo rinviata.
