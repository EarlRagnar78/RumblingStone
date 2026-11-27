# ADR-0143 — I gate bloccanti e veloci della CI girano prima del push

**Stato**: accettata (2026-11-19)
**Data**: 2026-11-19
**Decisione-fonte**: il DM (Jfs), 2026-11-19: «farle tutte in ordine con PR separate misurando per ognuna il miglioramento» (pratica C, pre-commit) e «fixa tutti i problemi che trovi con le verifiche, usa gli standard TDD e altri standard rigorosi».
**Rapporti**: riprende con configurazione rigorosa una tecnica che [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) aveva scartato; usa `scripts/gate_locale.py`; segue [ADR-0142](ADR-0142-claudeignore-diventa-regole-deny.md). Guida al ritorno indietro: [`docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md`](../../docs/how-to/GUIDA-CONFIGURAZIONE-CLAUDE.md).

## Contesto

Delle 100 corse CI di PR più recenti (15-19/11) 11 sono finite rosse; con la
prima testa della #490 sono 12. Le ho classificate dal log del passo fallito:

| Causa | Corse | Dove si vede in locale |
|---|---|---|
| regola d'oro dei piani o riga del CHANGELOG senza 5 colonne | 4 | `check_plans_discipline.py`, meno di 1 s |
| apparato da rigenerare (`componenti.py`) | 2 | meno di 1 s |
| adozione in attesa diventata attiva | 1 | meno di 1 s |
| booklet che non compila in stampa | 1 | 32 s |
| impronta delle creature cambiata (pytest) | 3 | 86 s |
| un test di pytest (`test_tabelle`, la #490) | 1 | 2 s, ma dentro una suite di 14 minuti |

Un controllo locale esisteva già, `gate_locale.py`, che lancia i passi della
CI. Nei thread nessuno lo installava come hook: il pre-push di
`install-git-hooks.sh` controllava solo la regola d'oro, e nei container non
veniva installato.

ADR-0099 aveva scartato pre-commit perché «scarica dalla rete». Con
`repo: local` e `language: system` non scarica niente: provato il 19/11 con il
proxy puntato su una porta morta, il hook gira lo stesso.

## Alternative considerate

| Opzione | Costo a ogni push | Rossi presi (su 12) | Contro |
|---|---|---|---|
| **`gate_locale --pre-push`: i gate bloccanti, senza pytest né i tre lenti** (scelta) | 45 s | 7 | restano alla CI il booklet in stampa e i test |
| `gate_locale --rapido`, tutti i gate | 3 min 11 s | 8 | su 100 push costa più tempo di quanto ne fa risparmiare |
| `--rapido` più l'impronta delle creature | circa 4 min 40 s | 11 | come sopra, peggio |
| Hook nativo senza pre-commit | 45 s | 7 | non è lo standard di fatto; gli altri strumenti non lo riconoscono |
| Niente hook | 0 | 0 | 12 rossi su 101 corse |

Il conto del tempo, su 100 push: con `--pre-push` circa 75 minuti di hook
contro circa 154 minuti risparmiati (7 rossi evitati, ognuno vale un giro di CI
in più, circa 22 minuti). Con `--rapido` 320 minuti contro 176: non conviene.
Il costo del giro di CI è una stima; il numero di rossi è misurato.

## Decisione

1. **`gate_locale.py --pre-push`** esegue i passi del job `validate` di
   `ci.yml` saltando pytest, i passi non bloccanti (non possono fare rossa la
   CI) e quelli di `LENTI`: resa delle mappe (56 s), edizione da stampa (32 s),
   corredo della serata (17 s). Sotto i 15 secondi un gate resta nel hook.
   `LENTI` ha un test: ogni nome deve esistere ancora in `ci.yml`.
2. **`.pre-commit-config.yaml`** ha un solo hook, locale, sullo stadio
   `pre-push`, che lancia quel comando. `pre-commit` (MIT) entra in
   `requirements-dev.txt`.
3. **`install-git-hooks.sh`** installa il hook di pre-commit; senza
   pre-commit, o con `RS_HOOK_NATIVO=1`, scrive un hook nativo che lancia lo
   stesso comando. Il post-merge delle skill resta com'era.
4. **Nei thread** lo lancia `.claude/hooks/session-start.sh`, solo quando
   `CLAUDE_CODE_REMOTE=true`. Sul computer del DM non si installa da solo: si
   lancia una volta `./scripts/install-git-hooks.sh`.

## Conseguenze

**Misura.** Prova end-to-end il 19/11: un commit con una riga del CHANGELOG a
quattro colonne, spinto verso un remoto di prova, è stato bloccato in 47 s;
il hook ha trovato anche `MEMORIA.md` non rigenerata. Il ramo non è arrivato
sul remoto.

**Quello che si paga.** Ogni push costa circa 45 secondi. Il booklet in stampa
e i test di pytest restano alla CI: 5 dei 12 rossi non li prende. Chi deve
spingere subito usa `git push --no-verify`, e lo fa sapendo di saltare i
cancelli.

**Ritorno indietro.** Revert della PR; oppure, solo su una macchina,
`rm .git/hooks/pre-push`. Per togliere un gate dal hook senza toglierlo dalla
CI, aggiungerlo a `LENTI` con i secondi misurati.
