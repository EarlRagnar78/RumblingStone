---
name: audit-plugin-regole-2026-11-09
description: Audit dei plugin 3.5/PF1e contro SRD/PRD (PR #365, 2026-11-09): misura, correzioni 3.5, card ranger/paladino/bardo, lotto PF1e classi aperto
metadata:
  type: project
  modified: 2026-11-09T23:32:45.204Z
---
PR #365 (bozza, ramo claude/project-thread-y5dcih, thread «Verificare i plugin di regole 3.5 e PF1e»).
- Misura: plans/esperimenti/plugin-regole-2026-11-09/misura_plugin_regole.py (tabelle vere da SRD/PRD in cache vs plugin). `sistemi.py` misura solo la dichiarazione, non la copertura.
- Corretti nel 3.5: griglia adepto (10/14/18/20), 8 incantesimi a livello sbagliato (anche nell'ancora spells.md), 3 armature + nomi ufficiali, 12 prestigio, 7 abilità; derive_statblocks a parola intera e nome più lungo (prima «shield» in Oakenshield e «torre» davano scudo +4 a 11 creature).
- Lezione: le «Verified anchor rows» delle skill (classes.md, spells.md) non sono l'SRD; test verdi confrontavano due copie dello stesso errore. Riscontrare sempre con la fonte in cache.
- Card decisa da Jfs (2026-11-09): «Tabelle PF1e intere, segnate» nel plugin 3.5 per ranger/paladino (in PF1e stessa griglia) e bardo (al giorno con trucchetti a volontà + conosciuti); chiavi incantatori_regole.griglia_pf1e/zero_a_volonta; misura le confronta col PRD. 3.5 a 605/606. ADR-0121. Commit e14397cd.
- Lotto PF1e (patto tra thread, 2026-11-09, su richiesta Jfs): i DATI (classi.toml, armature/scudi, griglie) li genera dal PRD il thread della #363 sul ramo claude/project-thread-8tgb80; questo thread fa costruttore/strumenti/misura partendo da quel ramo dopo il suo hash. Merge: #364, #363, #365, poi lotto PF1e.
- 2026-11-10: dati PF1e del thread #363 (855ac565) misurati 142/142; genera_creatura --sistema pf1e accetta --classe (creature_pf1e.converti_classe: primo dado max come conformita.toml, GS = livelli−1 PRD 3656, tipo «classe N» perché il cancello riconosca il PNG). Solo le 16 classi comuni al 3.5. Lavoro in ramo locale lotto-pf1e, patch in /mnt/project-files/lotto-pf1e-2026-11-10/; PR dopo merge #363. #365 CI verde 12/12, merge al coordinatore.
- 2026-11-10 (Jfs: «completa i limiti»): costruttore nativo genera_creatura.genera_png_pf1e (55 classi, multiclasse «a:5,b:3», prestigio avanza incantatore), liste PF1e e pf bonus costrutti dai dati del thread #363 (757e6e69). Misura PF1e 46/217 → 217/217 (righe «uso»). Ramo locale lotto-pf1e (11523a88), patch in /mnt/project-files/lotto-pf1e-2026-11-10/. Jfs: dare io l'ok al merge se le misure migliorano, ordine #364 (unita 421dbd0) → #363 → #365 → lotto PF1e.
- 2026-11-10: #363 (8598d67), #365 (3064e732) e lotto PF1e #367 (a6223692) unite su main: PF1e 217/217, 55 classi e 20 tipi passano il cancello PF1e. Il merge della #367 ha richiesto il sì di Jfs (il controllo automatico lo negava al thread padre).
- Aperto: 185 nomi incantesimi non del lessico; «scaglie» armatura a rischio.
Collegati: [[sistemi-di-gioco-plugin]] [[regole-pf1e-cancello-schede]] [[feedback-numeri-piu-forti-calcolati]]
- 2026-11-10: **#365 unita su main** (merge 3064e73) dopo #364 (421dbd0) e #363 (8598d67). Il lotto PF1e arriva in una PR nuova da main.
