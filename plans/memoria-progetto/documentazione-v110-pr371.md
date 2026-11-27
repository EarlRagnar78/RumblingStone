---
name: documentazione-v110-pr371
description: Recupero documentazione della milestone v1.1.0 (PR #371, 2026-11-10): cosa contiene, card aperte, problemi trovati e girati
metadata:
  type: project
  modified: 2026-11-10T06:53:08.565Z
---
PR #371 (bozza, milestone 1, ramo claude/project-thread-i5v4kc, 2026-11-10): ARCHITETTURA §19 motore/plugin e §20 fatti-termini-numeri (29 diagrammi), docs/how-to/GUIDA-SISTEMI-DI-GIOCO.md (guida pratica) e docs/reference/RIFERIMENTO-PLUGIN-DI-SISTEMA.md (riferimento), `dm.py sistemi` (passa i flag a sistemi.py), README/INDEX a 119 ADR, misura Diátaxis in plans/esperimenti/documentazione-2026-11-10/ (5 guide su 14 in una forma sola).
Card a Jfs chiuse il 2026-11-10: Diátaxis scelta B (riorganizzare subito, ADR-0123), ADR-0117 accettata.
Trovati e girati al thread regole: schema JSON per capacità di ADR-0112 §3 non implementato; Sezione 15 di OGL.txt senza ACG/UC/UM/Bestiari 2-4 da cui derivano i dati PF1e, LICENSES.md §1 punta ancora a dmcore/tabelle.py.
Rilascio: nessuna rottura della superficie pubblica dopo v1.0.0 → 1.1.0, non 2.0.0.
test_fase1::test_mostra_solo_cio_che_e_ancora_aperto fallisce nel container anche su main (clone shallow). Vedi [[milestone-roadmap]] [[documentazione-a-ogni-milestone]].
Aggiornamento 2026-11-10: il lotto 3 del thread regole (dopo la #369) porta la capacità `creature.talenti` e OGL.txt da 6 a 25 voci; da documentare (RIFERIMENTO §5, ARCHITETTURA §19, conteggio 16→17 capacità) solo quando è su main. ADR-0123 confermato dal thread padre per la struttura doc (Diátaxis).
2026-11-10 09:00: il thread regole unisce #372 e i lotti 2,4,5 uno alla volta; niente merge paralleli su genera_creatura, dmcore/talenti, sistemi/*/dati, CHANGELOG, MEMORIA finché non avvisa. La #371 tocca CHANGELOG e MEMORIA: si unisce dopo. Poi citare creature.talenti, [tratti_tipo], [pf_bonus_costrutti].
2026-11-10 10:14: PR #376 (thread regole, milestone v1.2.0) dichiara creature.talenti in genera_creatura; quando entra su main, nel RIFERIMENTO-PLUGIN §5 sostituire «— (nessuno la dichiara)» con genera_creatura. Avvisa il thread regole al merge. CI #371 verde su 0cd33e88, merge passato al thread padre.
2026-11-10 10:32 card Jfs: Diátaxis = B «Riorganizzare docs/ subito» (ADR-0123 accettata, commit 0ba48c7): docs/tutorials|how-to|reference|explanation; sezioni spostate tengono il numero e lasciano un rimando; docs/tools e docs/audit restano; docs/guides/README.md redirect da togliere alla v1.2.0. ADR-0117 accettata (card stessa ora). test_validate_docs e test_validate_pg instabili sotto xdist, verdi in seriale.
2026-11-12: coda verso main #378 (ADR-0124 verifica schede MCP), #379 (ADR-0125), poi 12 lotti «regole senza omissioni» che toccano tools.manifest/CHANGELOG/MEMORIA: la #371 va riallineata dopo ogni merge (INDEX, plans/CHANGELOG, MEMORIA rigenerata); doc MCP e plugin regole cambieranno.
2026-11-12 coordinatore: ADR-0123 conteso col thread volume (taglia/portata): lo tiene chi arriva prima su main, l'altro rinumera (nel caso: rinominare file ADR, rimandi in docs/*, INDEX, CHANGELOG, guides/README). PR #381: ogni PR con righe nuove in plans/CHANGELOG.md deve aggiungere «### MS-NNNN» in plans/MEMORIA-STORICA.md. Regola merge Jfs 12/11: verde+clean, problemi e misure dichiarati, miglioramento misurato vs main, un merge alla volta, testa e misura al coordinatore prima.
