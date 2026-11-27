---
name: p16-marcature-inferred
description: P16 marcature INFERRED: da 240 a 25 aperte (lotti 1-5, PR #310 #311 #313); le 25 restanti sono righe di regole, al thread skill vincolate
metadata:
  type: project
  modified: 2026-11-04T06:01:34.125Z
---

P16 dell'indice §0 diceva 44 marcature: era un `grep` sul marcatore nudo. Il 2026-11-04 `scripts/inventory_inferred.py` corretto (righe di regola → «meta», note a capo contate) dà **240 aperte su main**, ARC-08 109. Il numero da usare è quello dello strumento (`--check`, baseline in docs/audit/inferred-baseline.json).

Lotto 1 = ARC-08 (PR #310): registro in plans/esperimenti/p16-inferred-2026-11-04/ARC08-DECISIONI.md.

**Why:** Jfs vuole i dubbi in card con la consigliata, parole semplici e senza sigle ([[decisioni-superate-regressione]], [[scelte-inferred-versione-piu-forte]]).
**How to apply:** lotti successivi uno per arco: ARC-07 (~73, quasi tutte ripetute nei tre volumi .hb.md), ARC-09, campaign, PG (caratteristiche di Artemis/Thorik: solo dalle schede del DM). A CI verde si avvisa il thread «Audit settimanale PR e decisioni», che fa il merge.

Regola Jfs 2026-11-04: si chiude solo ciò che è già fatto, risolto o superato, con la prova; mai in blocco. Il resto va in card di decisione per tema.

2026-11-04: PR #310 unita su main (CI verde su ae7ea0d2). Tutte le card ARC-08 applicate. Quota: piana 870 m tenuta, gradoni +80/+100/+120 = 950/970/990 m canone. Condotto della sorgente largo 1,5 m, 5 bugbear dell'ondata 3 lo usano. ARC-08 da 109 a 11 (restano D6, P09, righe di regola); repo 136 aperte.
Avviso: adozioni_in_attesa scatta con 3 file di gioco a 10+ commit in 60 giorni senza blocco storico.
2026-11-04 sera: lotto 2 ARC-07 nella PR #311 (insieme alla quota 520 m), 70 → 1 aperte (resta la riga del 14° livello in DEF-4, servono i PX di partenza), repo 65. CI verde, merge passato al thread audit. Lezione: i volumi .hb.md di ARC-07 si rigenerano coi manifest (build_booklet_html.py --format hb), mai a mano. Prossimi lotti: ARC-09, campaign, PG.
2026-11-05: lotto 3 ARC-09 in PR #313 (con la guida docs/guides/GUIDA-PATCH-RAMO-DI-GRUPPO.md): leva fuori dalle mura di Rethmar e Dauth (combattono solo i difensori degli scenari), guarnigione fissa di Dauth 200 nani, Witchwood 300 m. Repo 58 aperte. Restano campagna, PG (caratteristiche di Artemis/Thorik: servono le schede del DM), Bestiario (orog, bugbear, gufo), Drappo (quote), ARC-08 D6/P09; molte righe di regole/skill/template sono falsi positivi da riclassificare come meta.
2026-11-05 lotto 4 (PR #313): foto della scheda di carta dei 4 PG in /mnt/project-files/schede-pg-2026-11-05/, trascritta in plans/esperimenti/p16-inferred-2026-11-04/SCHEDE-PG-CARTA.md. DM: carta non aggiornata all'ultima serata. Thorik = carta (con −2 Corona già dentro) + rito Smeraldo → 20/10/18/13/12/13, PF 128; Artemis 10/18/14/10/10/18; Hella 16(guanti +2)/13/12/12/20(16+Collana, periapto non si somma)/10, A.1 DEF-3 allineato (CA 21, 80 pf). Aperto: equipaggiamento di Hella carta (dragonhide plate, vanisher cloak) vs modulo (cuoio borchiato, mantello resistenza +2). Repo 49.
2026-11-07 lotto 5 (PR #313 unita su main il 2026-11-07): Bestiario, Drappo, ARC-08, Corona; registro in plans/esperimenti/p16-inferred-2026-11-04/BESTIARIO-DECISIONI.md. Lama mortale al bugbear, orog forte, gufo di Lythiel = scheda Ventolesto, piazza Tarsilia 1,5 m (mappe da JSON + compile_map_json), troll 10 DV GS 6 (EL 13), riserva +3, cavaliere che cade: nessuno lo afferra (15d6), vince copia PG della Corona, schema Tordek ingrandito contro Fauci (lotta impossibile, Sbilanciare solo con Fauci a terra; termine ufficiale «Sbilanciare», mai «sgambetto»). Repo **25** aperte, tutte righe di regole/modelli: le segue il thread «Standardizzare marcatura INFERRED e skill vincolate», che tocca inventory_inferred.py e baseline solo dopo #313 su main. Dopo edit al Bestiario: impronta_creature.py --scrivi.
2026-11-07 sera (PR #314, ancora bozza): le 25 righe di regola passano a meta; **P16 = 0 aperti**, baseline 0. → [[standard-marcature-inferred]]
