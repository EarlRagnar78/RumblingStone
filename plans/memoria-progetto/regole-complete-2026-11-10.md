---
name: regole-complete-2026-11-10
description: Blocco 1-sexies «regole complete» 3.5/PF1e (Jfs 2026-11-10): lotti 1-5, misure, stato delle PR, cosa resta fuori.
metadata:
  type: project
  modified: 2026-11-10T07:50:27.060Z
---
Richiesta Jfs 2026-11-10: verificare che le regole PF1e (e d20/3.5) siano complete, completarle e misurarle, coordinandosi con gli altri thread. Thread «Completare le regole PF1e», ramo `claude/project-thread-y5dcih`, una PR per lotto, merge dal thread padre col sì di Jfs.
- Misura estesa: plans/esperimenti/regole-complete-2026-11-10/misura_regole_complete.py (+ INVENTARIO.md, MISURA-LOTTOn-PRIMA/DOPO).
- Lotto 1 = PR #369 unita il 2026-11-10 (c185b11) su ordine diretto di Jfs nel thread («mergia le pr che sono pronte e green»): il thread delle regole unisce da sé i suoi lotti a CI verde, uno alla volta (#372 lotto 3, poi 2, 4, 5). Il ramo viene cancellato al merge: si ripubblica col commit del lotto successivo.
- Limite costrutti Fine/Diminutive chiuso (commit dbad5b1d): tabella «Construct Size» dal PRD pubblicato legacy.aonprd.com/bestiary/creatureTypes.html (manca nel PSRD-Data). v1.2.0 aperta solo per le promozioni 22-24/11; poi v1.3.0.
- Tutti su main il 2026-11-10: #369 lotto 1 (c185b11), #372 lotto 3 (3d3e356), #373 lotto 2 (d9a551e), #374 lotto 4 (7820ab3), #375 lotto 5 (0f70d7c). Blocco 1-sexies chiuso; i tre limiti di ADR-0121 chiusi.
  - 3 talenti PNG (`creature.talenti`, dmcore/talenti.py): 3.5 0/11→11/11, PF1e 0/32→32/32.
  - 2 incantesimi 3.5 al lessico (separatore àncora « · »): ADR-0121 3.5 605/606→790/791.
  - 4 requisiti 18 classi di prestigio PF1e 0/18→18/18; orazioni sciamano.
  - 5 tratti dei tipi: Cos — non morti/costrutti, Int — e niente talenti a melma/parassita/costrutto, pf bonus costrutto da SRD; converti(pf_bersaglio=). 3.5 33/45→45/45, PF1e 36/45→45/45, costrutti 0/9→9/9.
- Fuori, detto: immunità/RD dei tipi non scritte dal generatore; non morti 3.5 sotto il bersaglio del GS (regola).
- Suite: in parallelo ha gare (validate_pg ZZZ); in seriale `-p no:randomly` tutta verde.
Collegati: [[audit-plugin-regole-2026-11-09]] [[regole-pf1e-cancello-schede]] [[thread-padre-pr]]
- 2026-11-12: PR #376 unita (1387b7a): genera_creatura dichiara creature.talenti e formule.regole nel manifest (misura 1/3 → 3/3, spia su capacita()). Limite: gli altri strumenti non sono stati spiati.
