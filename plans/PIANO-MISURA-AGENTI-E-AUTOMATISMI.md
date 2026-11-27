# PIANO — Misurare agenti, skill e automatismi su casi veri

> **Stato**: 🟡 in corso (2026-11-27). M1 fatto (PR 1, #531); M2 fatto sul ramo della PR 2 (le buste senza lavoro tacciono, gli omonimi dei trigger non scattano; macro-F1 del test da 41/252 a 58/315, esatti fermi a 4/17); M2-bis fatto sul ramo `lavoro/raccolta-v2` (la raccolta settimanale dei casi, con la consigliata da un annotatore cieco); M3 e M3-bis da fare; M4-M7 solo elencati · **Classe**: G per le etichette e la scelta della tecnica, C per il codice
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

Dopo la conferma delle etichette da parte del DM (27/11, pomeriggio): 28 casi, test 3/17 contro la baseline «piattaforma» 2/17, macro-F1 73/924 ≈ 0,079 contro 0,026. Il tetto è rimesso a questi numeri; D1 è chiusa. Al riallineo con main `77748c5b` il cricchetto è scattato per l'agente nuovo custode-memoria: rietichettato su card il caso della memoria oltre il limite, il test fa 4/17 e la macro-F1 41/252.

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

### M2 · Gli omonimi e i messaggi che non chiedono lavoro ✅ PR 2 (2026-11-27)

Due tecniche, due commit, ognuna con i test scritti prima del codice (8 rossi
per la prima, 13 per la seconda):

1. `testo_di_lavoro()` in `scripts/instradamento_agenti.py` (commit
   `32b48545`): l'hook `--prompt` instrada sul solo testo che chiede lavoro.
   Tace sui tocchi delle card, sugli inoltri del coordinatore (`<relay>`),
   sulle notifiche, sui resoconti dei sottoagenti (due segni della forma su
   cinque) e sui via libera brevi (al più 12 parole, un assenso, nessun verbo
   di lavoro); di una busta `<wake>` legge solo i messaggi `trust="principal"`,
   e il `<session-context>` in testa al primo messaggio si toglie.
2. `OMONIMI` in `scripts/instradamento_skill.py`, usati da `raggiunte()`
   (commit `7cee6d8d`): per «coordinate», «hook», «caso», «png», «master»,
   «corredo», «Canva» e «Canva AI», una regex degli usi che parlano d'altro
   (tolti dal testo) e una del contesto che spegne il trigger nel messaggio;
   l'estensione `.png` di un nome di file non conta come parola.

**La misura.**

| | main `4f713551` | ramo |
|---|---|---|
| test (n=17), esatti | 4/17 | 4/17 |
| test, indulgenti | 4/17 | 4/17 |
| test, macro-F1 | 41/252 ≈ 0,163 | 58/315 ≈ 0,184 |
| dev (n=11), esatti | 4/11 | 4/11 |
| suggerimenti dell'hook sui 103 prompt veri del thread | 57/103 | 1/103 |
| di cui tocchi sulle card | 36/39 | 0/39 |
| di cui messaggi di Jfs | 3/10 | 1/10 |

La macro-F1 sale solo per la seconda tecnica. La prima non muove il set
d'oro, che conserva il testo nudo dei messaggi e non la busta che l'hook
riceve; la sua misura sono i prompt veri del thread, presi dalla trascrizione
della sessione con uno script dello scratchpad che non è nel repo. Il
suggerimento rimasto fra i messaggi di Jfs è una richiesta vera di lavoro.
Tetto del set d'oro alzato a 58/315. `instradamento_skill.py --check`
invariato (17 omissioni su 50, 1 violazione). 116 test verdi su
`test_instradamento_agenti`, `test_instradamento_skill` e `test_eval_metriche`.

**I limiti.**

- Il set d'oro non misura le buste: la prima tecnica non ha un cricchetto.
  Proposta: un set di prompt grezzi, raccolti con la raccolta settimanale.
- Gli errori che restano nel dev sono vocabolario che manca («tattiche» per
  regolista, «immagini» e «pose» per art-director), non omonimi.
- Ogni `<relay>` del coordinatore ora tace, anche quando apre lavoro; la riga
  «Catena:» scritta nell'inoltro la legge ancora il cancello del push.
- Le regex degli omonimi sono euristiche: i falsi positivi possibili sono nei
  commenti accanto a ciascuna.
- «avventura» non è trattata come omonimo.

### M2-bis · La raccolta settimanale dei casi ✅ ramo `lavoro/raccolta-v2` (2026-11-27)

Il limite vero della misura è n: con 17 casi di test nessuna tecnica batte
la regex in modo significativo (banco del 27/11, McNemar p=0,29). Scelta di
Jfs del 27/11, su card: ogni thread nuovo porta un caso, al più dieci per
componente a settimana, e Jfs conferma l'etichetta su card con la
consigliata.

`scripts/raccogli_casi_agenti.py` (commit `df8284cb`, `db757c2d`,
`92255948`, `c66bdf8d`) lavora sui messaggi che la routine esporta in
`/mnt/project-files/instradamento-coda/`, mai nel repo:

- `proponi IN.json --coda DIR` scarta i duplicati (contro il set d'oro, la
  coda e l'ingresso) e i testi con email, segreti o un percorso con nome
  utente (un sottoinsieme delle regole di default di gitleaks), mette a ogni
  caso la predizione dell'hook come «proposta» e scrive la settimana
  `AAAA-Www.json` e `CARD.md`;
- `cieco` scrive `CIECO-AAAA-Www.tsv`, solo id e testo dei casi del DM;
- `annota` prende le etichette dell'annotatore cieco come consigliate e
  stampa l'accordo con l'hook e la kappa di Cohen;
- `applica` porta i casi confermati nel set d'oro, con lo split per sha256
  dell'id (pari dev, dispari test, come gli split stabili di TFDS e Hugging
  Face), rimette il tetto misurando l'hook invariato sul set nuovo e stampa
  la misura prima e dopo; la nota del tetto dice che a mano non si abbassa;
- `--check` controlla la forma del set d'oro.

**Perché la consigliata viene da un annotatore cieco.** Sul set d'oro di
main, 28 casi confermati da Jfs, la predizione dell'hook coincide con
l'etichetta confermata in 8 casi su 28 (Wilson 95% 0,15-0,47, kappa 0,211);
l'annotatore B, che leggeva solo il testo, in 24 su 27 (Wilson 0,72-0,96,
kappa 0,865). Una card con la proposta dell'hook come consigliata
ancorerebbe Jfs sulla cosa che si misura.

**La misura.** Su main non c'è nessuna raccolta, e il set d'oro cresce solo
a mano. Da qui può crescere ogni settimana, e il guadagno di n è la leva per
distinguere una tecnica dall'altra. Test: 19 passati su
`test_raccogli_casi_agenti` (5 rossi prima del codice dell'annotatore
cieco), 92 su `test_raccogli_casi_agenti` e `test_instradamento_agenti`;
`raccogli_casi_agenti.py --check` verde sui 28 casi, `instradamento_agenti.py
--check` invariato (test 4/17, macro-F1 58/315).

**I limiti.**

- 24 su 27 sopravvaluta l'accordo: B ha etichettato prima della conferma di
  Jfs, e in parte le consigliate delle card di Jfs venivano da B.
- L'annotatore cieco è un agente Claude a cui si passano solo il file
  `CIECO-*.tsv` e la guida delle cascate
  (`/mnt/project-files/agenti-eval-2026-11-27/GUIDA-AGENTI-E-CASCATE.md`):
  la cecità dipende dalla disciplina di chi lo lancia, nessun controllo la
  garantisce.
- Lo split per hash è deterministico, ma con n piccolo dev e test possono
  sbilanciarsi.
- Il tetto di dieci casi per componente a settimana non è nel codice: lo
  tiene la routine che esporta.
- La routine del lunedì non chiama ancora lo script; lo chiederà il thread
  al coordinatore dopo il merge.
- Dopo `applica` i numeri di `test_oro_del_repo_numeri_di_oggi` si
  aggiornano a mano: lo script lo ricorda e basta.
- Il set conserva ancora il testo nudo e non la busta: la tecnica 1 di M2
  resta senza cricchetto.

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
- [x] M2 · omonimi e messaggi senza lavoro (PR 2): macro-F1 del test 41/252 → 58/315, suggerimenti sui prompt veri 57/103 → 1/103
- [x] M2-bis · raccolta settimanale dei casi, con la consigliata da un annotatore cieco (`raccogli_casi_agenti.py`): accordo con l'etichetta di Jfs 8/28 per l'hook contro 24/27 per l'annotatore B
- [ ] M3 · TF-IDF con MultinomialNB o LogisticRegression di scikit-learn contro le regole (PR 3)
- [ ] M3-bis · rete con sentence-transformers, solo con ≥ 200 casi e M3 che non basta (PR 4)
- [ ] M4 · recall dell'instradamento delle skill
- [ ] M5 · precision del blocco di `vincolo_skill`
- [ ] M6 · precision per norma dei rilevatori, recall del riconoscimento del push
- [ ] M7 · pass^k delle prove degli agenti
