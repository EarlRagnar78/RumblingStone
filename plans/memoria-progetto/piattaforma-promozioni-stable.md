---
name: piattaforma-promozioni-stable
description: Promozioni testing→stable di ADR-0099: 2026-11-08 PR #353 ruff/uv/converters stable, xdist resta in testing fino al 2026-11-22; come si misura dai log
metadata:
  type: project
---

Regola ADR-0099: 14 giorni + 10 run su main, zero falsi allarmi, job principale non peggiora >5%, ok del DM.

2026-11-08 (ok di Jfs, thread «Promuovere a stable gli strumenti in prova», PR #353 UNITA il 2026-11-08 (125e535), ramo claude/project-thread-bal1e6): misura su 81 run main dal 23/10 in plans/esperimenti/promozioni-2026-11-08/MISURE.md.
- ruff stable (blocca), compileall tolto: 5 rossi il 7/11 = F841 veri, 0 falsi allarmi.
- uv stable nel job validate (24→6 s, stessi pacchetti 81/81). Gli altri job installano ancora con pip; lock A3 da fare.
- converters/ stable (81/81). Blocca il merge solo se Jfs lo aggiunge ai check richiesti del ruleset (job rinominato «Convertitori (import su 3.13)»).
- pytest-xdist RESTA testing: per 70 run il job non aveva typst e saltava 9 prove; suite uguale solo da #342 (2026-11-08). Riproporre non prima del 2026-11-22 con 10 run a conteggi uguali (job rinominato «pytest-xdist in prova»).
- Audit hook rifatto: test_migliora_prosa e test_misura_stampa aggiunti a SCRIVONO_NEL_REPO.

**How to apply:** un passo con continue-on-error risulta `success` nell'API dei job: leggere i log (`/actions/jobs/{id}/logs`, raggiungibile con curl via proxy). Confrontare anche i conteggi passate/saltate fra job, non solo il verde. Merge al thread «Audit settimanale PR e decisioni».
2026-11-09: anche con il sì di Jfs il PUT su /rulesets risponde 403 «Write access to this GitHub API path is not permitted through this proxy»: è il proxy, non un permesso. Il ruleset (id 23944256) lo modifica solo Jfs dal web.
2026-11-09: Jfs ha aggiunto «Convertitori (import su 3.13)» ai check richiesti del ruleset di main (ora 3: Validate skills & scripts, Build skill packages, Convertitori).

2026-11-09: P8 anticipata da Jfs (card «Accendilo ora»). PR #359 UNITA il 2026-11-09 (f9d3c2d): job «Python 3.14 in prova — non bloccante» (stessa suite pytest, bpy fuori da solo perché solo in requirements-completo). Primo run 3.14.10: 2.562 passate/16 saltate come 3.13, pytest 303 s vs 273. Criterio: un mese di verde, salto legato a Debian 14. Misure in plans/esperimenti/python-314-2026-11-09/. Nella roadmap: blocco 3 «Piattaforma».

2026-11-25 (card di Jfs «Tutti e sei, con il codice», D8; #516 unita e552c899, MS-0222): salgono a stable xdist (passo pytest 1.127→761 s, stima 477 non retta), cancello dei numeri, 14 conti PF1e in `fatti`, d eufonica (opzione --d-eufonica tolta), check_schede come errori, marche ADR-0109. Misure in plans/esperimenti/promozioni-2026-11-25/. Restano P1, P2, P5, P6, P8; il rilascio 1.1.0 può partire.
