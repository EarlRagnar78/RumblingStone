# PIANO — Misurare agenti, skill e automatismi su casi veri

> **Stato**: 🟡 in corso (2026-11-27). M1 fatto sul ramo della PR 1 (set d'oro, `eval_metriche.py` su scikit-learn e scipy, `--eval` e `--check`, cancello in testing); M2, M3 e M3-bis da fare; M4-M7 solo elencati · **Classe**: G per le etichette e la scelta della tecnica, C per il codice
> **Nasce da**: il thread «Misurare e migliorare agenti, skill e automatismi» del 2026-11-27, aperto da Jfs.
> **Decisione**: [ADR-0154](adr/ADR-0154-l-instradamento-degli-agenti-si-misura-su-messaggi-veri.md), proposta, con l'emendamento del 2026-11-27 (Jfs: le librerie standard di fatto della comunità al posto della sola stdlib).
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

Dopo la conferma delle etichette da parte del DM (27/11, pomeriggio): 28 casi, test 3/17 contro la baseline «piattaforma» 2/17, macro-F1 73/924 ≈ 0,079 contro 0,026. Il tetto è rimesso a questi numeri; D1 è chiusa.

Cause e dettaglio in ADR-0154.

## §3 · Lotti

### M1 · Il set d'oro, le metriche, il cricchetto in testing ✅ PR 1 (2026-11-27)

`plans/instradamento/agenti-oro.json`, `scripts/eval_metriche.py`,
`instradamento_agenti.py --eval [--json] --check --oro`, il campo `tetto` e il
passo CI con `continue-on-error`. 68 test verdi (`test_eval_metriche`,
`test_instradamento_agenti`, con una regressione iniettata che fa uscire
`--check` con 1).

Riscritto lo stesso giorno, su richiesta di Jfs, sopra le librerie che la
comunità usa (emendamento di ADR-0154): `sklearn.metrics` per matrice, P/R/F1,
accuracy e kappa, `DummyClassifier(strategy="most_frequent")` per la baseline,
`scipy.stats` per Wilson e bootstrap; scikit-learn `==1.9.1` in
`requirements-dev.txt`, canale testing. Del repo restano l'accuracy
indulgente, l'insieme vuoto, il formato e `macro_f1_esatta`, che il cancello
usa. Numeri del cancello invariati (4/18, baseline 6/18, macro-F1 107/1155);
il bootstrap esce dal JSON. `--check` da 0,19 a 1,28 s, l'hook `--prompt`
resta a 0,06 s. 92 test verdi.

### M2 · Gli omonimi e i messaggi che non chiedono lavoro ⬜ PR 2

`[engine: Opus 5, sessione principale per la scelta, Sonnet 5 per il codice · effort: alto · qualità: sul test la misura sale sopra main in esatti o macro-F1 senza scendere nell'altra, con le regole tarate solo sul dev, e il tetto si alza]`

Una tecnica sola: disambiguare i trigger omonimi («coordinate», «hook»,
«master», «caso», «corredo», «png», «avventura», «Canva») e riconoscere i
messaggi che non chiedono uno specialista (avvisi del coordinatore, resoconti
dei sottoagenti) perché diano «nessuno».

### M3 · Un modello classico di scikit-learn contro le regole ⬜ PR 3

`[engine: Sonnet 5 · effort: medio · qualità: TF-IDF con MultinomialNB o LogisticRegression di scikit-learn, scelto con la validazione incrociata sul solo dev e misurato una volta sul test; entra solo se batte M2 sul test, altrimenti il resoconto lo dice e il codice resta in esperimenti]`

Con 11 casi di dev la validazione incrociata ha pieghe minuscole: il
resoconto dice quante e con che varianza. Il modello gira solo in `--eval` e
`--check`, mai nell'hook, che resta senza dipendenze.

### M3-bis · Una rete, solo se il classico non basta ⬜ PR 4, con condizione

`[engine: Opus 5 per decidere se aprirlo, Sonnet 5 per il codice · effort: alto · qualità: con almeno 200 casi etichettati e M3 che non basta, un modello di embedding piccolo e multilingue (PyTorch e sentence-transformers) batte M3 sul test; gira nei 6 GB della RTX 4050 e fuori dalla CI]`

Non si apre prima che valgano tutte e due le condizioni: con 29 casi una rete
impara a memoria. Keras e TensorFlow, nominati da Jfs, sono scartati dal
thread il 27/11 a favore di PyTorch e sentence-transformers, lo standard di
fatto per il testo; Jfs può ribaltare la scelta. Sulla 4050 non è ancora stato
provato niente di questo lotto.

### M4-M7 · Gli altri componenti che classificano ⬜

Elencati dall'audit, ognuno con la metrica che il costo dell'errore chiede.
Nessuno è ancora tagliato in lotto. Jfs ha chiesto il 27/11 di allargare
l'audit e i fix a tutte le parti del progetto: ogni componente segue la
strada di M1 e M2, cioè un set etichettato con split dev e test, la misura
con `eval_metriche.py`, un cricchetto in testing e poi un fix per PR, tarato
sul dev e misurato sul test contro main.

| Lotto | Componente | Che cosa decide | Metrica (da `sklearn.metrics`) | Set etichettato | Fix |
|---|---|---|---|---|---|
| M4 | instradamento delle skill | skill obbligatorie | recall, con precision a fianco | `casi.json`, solo «verifica»; da rifare con split dev e test, perché quei casi tarano anche i trigger | gli omonimi dei trigger sono gli stessi di M2: il fix di M2 si rimisura qui prima di scriverne un altro |
| M5 | `vincolo_skill` | blocca la scrittura | precision del blocco, recall a fianco | da costruire dai commit | da scegliere dopo la misura |
| M6 | rilevatori di prosa del cricchetto | difetto sì o no, per norma | precision per norma | box votati e `CONGELATI.json` | da scegliere dopo la misura, norma per norma |
| M6-bis | riconoscimento del push nel cancello | è un push? | recall | i 144 comandi del thread della #510 | da scegliere dopo la misura |
| M7 | prove degli agenti (ADR-0148) | caso passato | pass^k su due esecuzioni (non è di sklearn) | i 36 casi di oggi | prima due esecuzioni per caso, come già scritto in ADR-0148 |

I verificatori `verifica_px` e `verifica_rimandi` sono già misurati con i
mutanti (ADR-0148) e non entrano.

## §4 · Validazione

- `python3 scripts/instradamento_agenti.py --check` verde contro il tetto.
- `python3 -m pytest scripts/tests/test_eval_metriche.py scripts/tests/test_instradamento_agenti.py -q`,
  con `requirements-dev.txt` installato (scikit-learn 1.9.1, scipy).
- Promozione del passo: le condizioni di ADR-0154, contate dai log.

## §5 · Decisioni

<!-- decisioni-dm: MISURA-AGENTI -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | M1 | **Le etichette dello split «test» di `plans/instradamento/agenti-oro.json` sono giuste?** Serve alla condizione 4 della promozione (ADR-0154); senza la conferma vale una seconda etichettatura cieca con kappa ≥ 0,6 (oggi 0,78). **Chiusa il 2026-11-27**: Jfs ha confermato i casi uno per uno su card, cinque etichette cambiate e «Sì grazie» tolto (emendamento di ADR-0154) |

## Checklist di avanzamento

- [x] M1 · set d'oro, `eval_metriche.py`, `--eval` e `--check`, cancello in testing (PR 1)
- [ ] M2 · omonimi e messaggi senza lavoro (PR 2)
- [ ] M3 · TF-IDF con MultinomialNB o LogisticRegression di scikit-learn contro le regole (PR 3)
- [ ] M3-bis · rete con sentence-transformers, solo con ≥ 200 casi e M3 che non basta (PR 4)
- [ ] M4 · recall dell'instradamento delle skill
- [ ] M5 · precision del blocco di `vincolo_skill`
- [ ] M6 · precision per norma dei rilevatori, recall del riconoscimento del push
- [ ] M7 · pass^k delle prove degli agenti
