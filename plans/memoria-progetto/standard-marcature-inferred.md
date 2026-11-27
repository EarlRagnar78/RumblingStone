---
name: standard-marcature-inferred
description: Thread 2026-11-07 standard unico marcature INFERRED/CANONE: misura sulla storia git (18% delle ipotesi cambiate dal DM), 8 schede a Jfs
metadata:
  type: project
  modified: 2026-11-07T07:47:24.442Z
---

Thread «Standardizzare marcatura INFERRED e skill vincolate» (2026-11-07). Proposta in /mnt/project-files/marcature-inferred-2026-11-07/PROPOSTA-STANDARD-MARCATURE.md, script misura_transizioni.py accanto.

Misura su git log -p (462 commit): 171 righe uniche INFERRED→CANONE, 141 (82%) confermate identiche, 30 (18%) cambiate, 16 (9%) con un numero cambiato (es. quota piana ARC-07 870→520 m). 61 marche tolte senza marca nella riga: campione 10/10 = volumi .hb.md o commit «scelte del DM» con file DECISIONI (tracciate fuori riga). 86% delle marche (761/883) senza domanda. Forme: 4 di INFERRED, 5 di canone (ACCEPTED di ADR-0091, «decisione DM», CANONE senza data). Regola scritta in 6 posti diversi. Ratchet inventory_inferred in CI è continue-on-error.

Scelte Jfs: scheda 1 = A, scheda 2 = A, scheda 3 = A, scheda 4 = A, scheda 5 = A, scheda 6 = A, scheda 7 = B (prova A/B grande: 30 consegne × 2 versioni, ~60 agenti, autorizzata da Jfs) (2026-11-07). Proposta (★ = A in tutte le 8 card): `[INFERRED — domanda; base: …]`, canone unico `[CANONE — DM data, codice]`, guida unica docs/guides/GUIDA-MARCATURE.md richiamata, cancelli non bloccanti 2 settimane poi bloccanti, blocco vincoli in ~10 skill di contenuto, 25 righe P16 → meta, prova A/B 10×2 agenti, niente grado di fiducia (LLM non calibrati). Partire solo dopo il merge della PR #313 (thread P16 tocca inventory_inferred.py e baseline). ADR da prenotare all'avvio.

[riga riservata · sha256:520f6eb7]

Avanzamento 2026-11-07: PR #314 (bozza, ramo claude/project-thread-ldjnwk, CI verde su 258a9ca) con ADR-0109, GUIDA-MARCATURE, blocco «Vincoli sui fatti» in 10 skill, test_vincoli_delle_skill. Prova A/B lanciata come workflow (consegne in plans/esperimenti/marcature-2026-11-07/consegne.json; worktree scratchpad ab/w7=main, ab/w3=nuova; risposte in ab/out/Cnn-p|q.md, p=vecchia per indici pari). Jfs (via coordinatore) chiede anche vincoli su termini/regole ufficiali 3.5 e PF1e: 4 card aperte (fonti, tabella it→SRD, passata sui moduli, dove). Difetto trovato: riscontro_srd.py `regola "Improved Trip"` non trova la voce 3.5 per il suffisso «<small>[General]</small>» nei titoli di feats.md.

2026-11-07 dopo la #313: sulla #314 anche contatore (meta = skill, templates, README, fixture, AGENTS.md, GUIDA-MARCATURE, schema `<domanda>`; forma nuova/vecchia/nuda), P16 25→0 e baseline 0, migrazione ACCEPTED→CANONE (138 righe, commit a sé, migra_marche.py), `scripts/controlla_marche.py --base` (2 cancelli non bloccanti in CI, testing). Residuo: rethmar.py «needs DM confirmation» nella pianta stampata. Resta la card sugli statblock potenziati.
