# PIANO — Misurare agenti, skill e automatismi su casi veri

> **Stato**: 🟡 in corso (2026-11-27). M1 fatto sul ramo della PR 1 (set d'oro, `eval_metriche.py`, `--eval` e `--check`, cancello in testing); M2 e M3 da fare; M4-M7 solo elencati · **Classe**: G per le etichette e la scelta della tecnica, C per il codice
> **Nasce da**: il thread «Misurare e migliorare agenti, skill e automatismi» del 2026-11-27, aperto da Jfs.
> **Decisione**: [ADR-0154](adr/ADR-0154-l-instradamento-degli-agenti-si-misura-su-messaggi-veri.md), proposta.
> **Audit**: `/mnt/project-files/agenti-eval-2026-11-27/AUDIT.md` (fuori dal repo; i numeri che servono sono qui e nell'ADR).
>
> **In breve**: gli hook e gli agenti di ADR-0146 decidono qualcosa su ogni
> messaggio, e nessuno li aveva misurati su casi veri tenuti fuori dalla
> taratura. Sul primo set d'oro l'hook che suggerisce l'agente fa peggio di
> una costante. Questo piano misura un componente per volta, con
> `eval_metriche.py`, e corregge con una tecnica per PR, misurata sul test
> contro main.

---

## §1 · Cosa c'è già, e cosa questo piano non rifà

| Già nel repo | Cosa copre | Qui |
|---|---|---|
| [ADR-0146](adr/ADR-0146-le-skill-di-prosa-si-caricano-per-vincolo.md) | hook, agenti, cancello del push, `--riepilogo` | non si rifà l'hook: si misura e si corregge il riconoscimento |
| [ADR-0148](adr/ADR-0148-i-fatti-si-verificano-con-script-e-gli-agenti-con-prove-fisse.md) e `.claude/agent-evals/` | prove fisse degli agenti, cricchetto in testing | non si toccano i casi; l'oscillazione fra due esecuzioni (pass^k) resta un lotto di quell'ADR, qui solo elencata (M7) |
| `instradamento_skill.py` e `plans/instradamento/casi.json` (L8 di PIANO-AGENT-SKILLS-ESTERNE) | le skill che una frase raggiunge | il cancello di skill resta suo; qui se ne misura il recall con le metriche nuove (M4) |
| [PIANO-PIATTAFORMA-DI-SVILUPPO](PIANO-PIATTAFORMA-DI-SVILUPPO.md) §2 | il canale di ogni cancello | la promozione del passo «Agent routing» segue quella tabella e le condizioni di ADR-0154 |
| il thread «Garantire che la documentazione si aggiorni da sola» (ADR-0153) | l'hook che non scatta sul primo messaggio | **non si tocca**: qui resta un caso dell'audit |

Guardati prima di aprire: `plans/INDEX.md`, `grep -ril "instradamento" plans/*.md`
(PIANO-AGENT-SKILLS-ESTERNE L8, STATO-E-ORDINE, PIATTAFORMA). Nessuno misura
gli agenti su messaggi veri né ha una libreria di metriche.

## §2 · La misura di partenza

Main `076a74d1`, `python3 scripts/instradamento_agenti.py --eval`, set d'oro di
29 messaggi (dev 11, test 18; kappa fra due etichettature cieche 0,78):

| | Hook | Baseline «sviluppatore» |
|---|---|---|
| test, esatti | 4/18 (Wilson 0,09-0,45) | 6/18 |
| test, macro-F1 | 107/1155 ≈ 0,093 | 0,0625 |
| tutti, esatti | 7/29 | 10/29 |

Cause e dettaglio in ADR-0154.

## §3 · Lotti

### M1 · Il set d'oro, le metriche, il cricchetto in testing ✅ PR 1 (2026-11-27)

`plans/instradamento/agenti-oro.json`, `scripts/eval_metriche.py`,
`instradamento_agenti.py --eval [--json] --check --oro`, il campo `tetto` e il
passo CI con `continue-on-error`. 68 test verdi (`test_eval_metriche`,
`test_instradamento_agenti`, con una regressione iniettata che fa uscire
`--check` con 1).

### M2 · Gli omonimi e i messaggi che non chiedono lavoro ⬜ PR 2

`[engine: Opus 5, sessione principale per la scelta, Sonnet 5 per il codice · effort: alto · qualità: sul test la misura sale sopra main in esatti o macro-F1 senza scendere nell'altra, con le regole tarate solo sul dev, e il tetto si alza]`

Una tecnica sola: disambiguare i trigger omonimi («coordinate», «hook»,
«master», «caso», «corredo», «png», «avventura», «Canva») e riconoscere i
messaggi che non chiedono uno specialista (avvisi del coordinatore, resoconti
dei sottoagenti) perché diano «nessuno».

### M3 · Una baseline statistica contro le regole ⬜ PR 3

`[engine: Sonnet 5 · effort: medio · qualità: Naive Bayes multinomiale stdlib addestrato sul dev, misurato sul test; entra solo se batte M2 sul test, altrimenti il resoconto lo dice e il codice resta in esperimenti]`

### M4-M7 · Gli altri componenti che classificano ⬜

Elencati dall'audit, ognuno con la metrica che il costo dell'errore chiede.
Nessuno è ancora tagliato in lotto.

| Lotto | Componente | Che cosa decide | Metrica | Etichette |
|---|---|---|---|---|
| M4 | instradamento delle skill | skill obbligatorie | recall, con precision a fianco | `casi.json`, solo «verifica» |
| M5 | `vincolo_skill` | blocca la scrittura | precision del blocco, recall a fianco | da costruire dai commit |
| M6 | rilevatori di prosa del cricchetto | difetto sì o no, per norma | precision per norma | box votati e `CONGELATI.json` |
| M6-bis | riconoscimento del push nel cancello | è un push? | recall | i 144 comandi del thread della #510 |
| M7 | prove degli agenti (ADR-0148) | caso passato | pass^k su due esecuzioni | i 36 casi di oggi |

I verificatori `verifica_px` e `verifica_rimandi` sono già misurati con i
mutanti (ADR-0148) e non entrano.

## §4 · Validazione

- `python3 scripts/instradamento_agenti.py --check` verde contro il tetto.
- `python3 -m pytest scripts/tests/test_eval_metriche.py scripts/tests/test_instradamento_agenti.py -q`.
- Promozione del passo: le condizioni di ADR-0154, contate dai log.

## §5 · Decisioni

<!-- decisioni-dm: MISURA-AGENTI -->

| # | Lotto | Domanda |
|---|---|---|
| D1 | M1 | **Le etichette dello split «test» di `plans/instradamento/agenti-oro.json` sono giuste?** Serve alla condizione 4 della promozione (ADR-0154); senza la conferma vale una seconda etichettatura cieca con kappa ≥ 0,6 (oggi 0,78) |

## Checklist di avanzamento

- [x] M1 · set d'oro, `eval_metriche.py`, `--eval` e `--check`, cancello in testing (PR 1)
- [ ] M2 · omonimi e messaggi senza lavoro (PR 2)
- [ ] M3 · Naive Bayes contro le regole (PR 3)
- [ ] M4 · recall dell'instradamento delle skill
- [ ] M5 · precision del blocco di `vincolo_skill`
- [ ] M6 · precision per norma dei rilevatori, recall del riconoscimento del push
- [ ] M7 · pass^k delle prove degli agenti
