# PIANO — Le pratiche d'ingegneria del 2026, misurate sul repo

> **Stato**: 🔵 pianificato (2026-09-24), **D1-D5 decise dal DM lo stesso giorno: sì a tutte** · **Classe**: G per la scelta, C per i lotti
> **Nasce da**: domanda del DM del 2026-09-24, dopo la
> [RICERCA-BDD-O-TDD](RICERCA-BDD-O-TDD-2026-09.md): *«non ha senso invece
> integrare gli aspetti positivi di entrambi e limitare quelli negativi? Cioè,
> dato questo, confrontandolo e valutando i miglioramenti oggettivi che
> potrebbero dare, sarebbe il caso di modificarlo o adottare le parti rilevanti
> che creano davvero miglioramenti»*, con in allegato un elenco delle pratiche
> più apprezzate nel 2026 (CI/CD, lotti piccoli, revisione, test a strati,
> trunk-based, osservabilità, DevSecOps, platform engineering, scoperta del
> prodotto, IA con verifica, debito tecnico, apprendimento continuo) e i
> risultati DORA 2025.
>
> **Risposta breve**: sì. L'elenco dice di combinare le pratiche, ed è quello
> che il repo fa già per sette su dodici. Il confronto trova **cinque buchi
> misurati**, e per ognuno c'è un intervento piccolo. Tre pratiche non si
> applicano a uno strumento che gira offline sul portatile del DM, e il piano
> dice perché.

---

## §1 · Cosa ho guardato prima, e cosa questo piano NON rifà

| Documento | Cosa copre | Qui |
|---|---|---|
| [PIANO-QUALITA-DEL-CODICE](PIANO-QUALITA-DEL-CODICE.md) (✅ chiuso) | librerie, riuso, TDD, OOP, gate che non bocciano | non si rifà: il suo «TDD sì, OOP no» resta |
| [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md) | solo libreria standard, pytest come dipendenza di sviluppo | vincolo: ogni lotto qui lo rispetta |
| [ADR-0045](adr/ADR-0045-ogni-lotto-dichiara-engine-effort-e-qualita.md) | classi dei lotti M/R/C/G/K | la usa PI-6 |
| [ADR-0056](adr/ADR-0056-una-norma-senza-misura-non-esiste.md) | ogni norma ha la sua misura | ogni lotto qui porta il suo rilevatore |
| [PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5.0 e D6 | il metodo di quel piano, e il BDD | PI-4 esegue la D6 se il DM sceglie (a); non la decide |
| [PIANO-RIPRESA-PR-ABBANDONATE](PIANO-RIPRESA-PR-ABBANDONATE.md) lotto 4i-3 | la protezione di `main` | non si rifà: PI-1 rimanda lì |
| `plans/contenuti-nei-rami.json` | cosa dei rami non è mai arrivato su `main` | PI-2 lo usa per i rami da togliere |

Ho cercato in `plans/` e in `plans/adr/` Dependabot, scansione dei segreti,
catena di fornitura, trunk-based, dimensione delle PR e rami vecchi: **nessun
documento ne parla**. DORA compare solo nel CHANGELOG e in due piani di
contenuto, come parola.

## §2 · Il confronto, pratica per pratica (misurato il 2026-09-24)

| Pratica | Com'è il repo oggi | Verdetto |
|---|---|---|
| **CI/CD** | un workflow, due job, 22 cancelli e due corridori di test; su `main` **40 esecuzioni su 40 verdi** dal 3 al 23 settembre, **0** revert in 30 giorni | ✅ tieni |
| **Lotti piccoli** | 34 merge in 30 giorni. Righe di codice (`scripts/` e `.github/`) per merge: **mediana 267**, **13 su 34 sopra 400**. Questa PR, la #160: **3.357 righe di codice**, 9.811 in tutto, 26 commit | ⚠️ **buco 1** |
| **Revisione del codice** | un solo manutentore umano; i gate fanno la revisione meccanica. Nessuna regola dice quali PR il DM deve leggere. L'errore Varis/Collezionista stava nel dossier dall'aprile 2026 ed è passato da tutti i gate: l'ha trovato il DM | ⚠️ **buco 2** |
| **Test automatici** | 1.310 test, mutazioni come convenzione (citate in 20 commit in 30 giorni), test d'approvazione (impronta delle creature), test su copia del repo sotto git. Input generati: **3 file su 87** | ⚠️ **buco 3**, sulle proprietà |
| **Trunk-based** | `main` è `protected: false`. **57 rami remoti**, 33 anteriori ad agosto, **39 già interamente su `main`** | ⚠️ **buco 4** (la protezione è già il lotto 4i-3) |
| **Osservabilità e SRE** | non c'è un servizio in esercizio: gli strumenti girano offline e finiscono. L'equivalente utile c'è già: stdout per i dati e stderr per i messaggi, exit code nel manifest, `dm.py doctor` | ➖ non si applica |
| **DevSecOps** | nessun Dependabot, nessuna scansione dei segreti, nessun controllo delle vulnerabilità sulle dipendenze (quattro pacchetti, versioni con `>=`) | ⚠️ **buco 5** |
| **Platform engineering** | `dm.py` come ingresso unico, `build-skills.sh`, il Playbook come percorso guidato, il manifest dei tool | ✅ tieni |
| **Scoperta del prodotto** | il DM è il prodotto e l'utente: le D nei piani, le storie Dato/Quando/Allora, `rumblingstone-playtest`. Le metriche d'esito ci sono nel PRD del ciclo di sessione (chiusura in 10 minuti, preparazione in 15) e nessuno le misura ancora | ✅ tieni; le misura la Fase 4 di CICLO-SESSIONE |
| **IA con verifica** | è il punto più forte del repo: G1-G6 in `AGENTS.md`, «misura prima di affermare», mutazioni, ADR-0067 sul confine fra codice e LLM | ✅ tieni |
| **Debito tecnico** | dichiarato dove nasce (pyyaml in ADR-0037, `[INFERRED]` nel canone), senza un registro unico | ✅ basta così: un registro in più sarebbe un terzo posto da tenere allineato |
| **Apprendimento continuo** | 68 ADR; le regole di `AGENTS.md` nascono ognuna da un fallimento misurato e datato, cioè postmortem senza colpe | ✅ tieni |

Sui test l'elenco del DM propone una distribuzione, e il repo la segue già
quasi tutta: TDD sulle regole, integrazione sui flussi, pochi end-to-end. Manca
la parte **proprietà e fuzz sui parser**, e il repo di parser ne ha molti. Per il
BDD vale la misura della ricerca: la parte utile è la specifica condivisa col
DM, e si prende senza il framework.

⚠️ **Sulle metriche DORA**, lo stesso avvertimento dell'elenco: servono a
trovare dove il sistema rallenta, non a dare voti. Qui non c'è una squadra da
confrontare, c'è un flusso da tenere piccolo.

## §3 · La decisione proposta (forma ADR)

**Contesto.** Un manutentore umano, un agente che scrive codice e prosa, uno
strumento offline e un canone che nessun gate può verificare del tutto. La CI è
solida e i test anche. I difetti che arrivano su `main` sono di due tipi: PR
troppo grandi per essere lette, e canone sbagliato che passa i gate.

**Decisione.** Si adottano le pratiche che chiudono i cinque buchi, ognuna con
il suo rilevatore (ADR-0056) e senza dipendenze nel percorso del DM
(ADR-0037). Si dichiarano non applicabili osservabilità, SRE e feature flag
finché non esiste un servizio in esercizio.

**Conseguenze.**

- Più PR, più piccole. Con `main` protetto e il merge automatico sul verde
  costano poco; senza, costano al DM un clic in più per lotto.
- Dependabot apre PR da solo: con quattro dipendenze e un controllo
  settimanale, poche al mese.
- Le PR che toccano il canone chiedono al DM una lettura mirata in più. È il
  costo che l'errore di Varis ha dimostrato necessario.
- Si paga una volta: sei script o file di configurazione, ognuno con test e
  mutazioni.

## §4 · Fase 1 · Audit *(fatto: §2)*

Le misure di §2 si rifanno così:

```bash
git log origin/main --merges --since=<data> --format=%h          # merge
git diff --numstat <m>^1 <m> -- scripts .github                  # righe di codice
git for-each-ref refs/remotes/origin --format='%(committerdate:short) %(refname:short)'
git merge-base --is-ancestor <ramo> origin/main                  # ramo gia' su main
```

PI-2 le trasforma in un comando, perché una misura che si rifà a mano non si
rifà.

## §5 · Fase 2 · Lotti

#### ⬜ PI-1 · `main` protetto
`[engine: DM · effort: basso · qualità: l'API dei rami dà protected: true e un push diretto su main viene rifiutato]`

È il lotto **4i-3** di RIPRESA-PR, con le regole già elencate lì. Qui si
aggiunge una cosa sola: con la protezione attiva conviene accendere il **merge
automatico** delle PR verdi, che è ciò che rende economiche le PR piccole di
PI-2.

#### ⬜ PI-2 · Lotti piccoli, e la misura del flusso
`[engine: Sonnet 5 · effort: medio · qualità: misura_flusso ridà i numeri di §2 su origin/main; test con mutazioni]`

Classe **C**.

- `scripts/misura_flusso.py`, solo libreria standard, da git: per ogni merge <!-- validate-docs: futuro -->
  le righe di codice e di contenuto, la durata del ramo, la frequenza; i rami
  remoti già interamente su `main`; i rami più vecchi di 30 giorni.
- **La norma**: una PR porta un lotto, e le righe di codice restano sotto
  **400**. File generati e contenuti di gioco non contano: un booklet
  rigenerato non è una PR grande. Registrata in
  `skills/REGISTRO-NORME-EDITORIALI.md` con `misura_flusso` come rilevatore.
- **In CI è un avviso, non un blocco**: un lotto di codice che serve davvero
  grande resta possibile, e l'avviso lo fa dire nel corpo della PR.
- **I rami**: l'elenco dei 39 già su `main` va al DM. Si cancellano solo con il
  suo sì (D5), perché un ramo cancellato si recupera solo conoscendo lo SHA.

#### 🟡 PI-3 · La catena di fornitura
`[engine: Sonnet 5 per i file, DM per le impostazioni · effort: basso · qualità: un segreto finto in un commit di prova viene bloccato; Dependabot apre la prima PR]`

Classe **C**, con una parte nelle impostazioni.

- `.github/dependabot.yml` per `pip` (i due `requirements*.txt`) e per
  `github-actions`, settimanale.
- **Scansione dei segreti e push protection**: per un repo pubblico sono
  gratuite e si attivano dalle impostazioni, senza codice. Le accende il DM.
- **`pip-audit`** (Apache-2.0) nel job della CI, come `pytest`: dipendenza di
  sviluppo, mai nel percorso del DM. Non bloccante per il primo mese, poi
  bloccante sulle vulnerabilità alte.
- **SBOM**: rinviato a [PIANO-VENDIBILITA](PIANO-VENDIBILITA.md). Serve quando
  qualcuno riceve il toolkit, non prima.

✅ **Fatto nel ramo `claude/focused-meitner-pgyb20` (2026-09-24).**
- `.github/dependabot.yml`: `pip` e `github-actions` sulla radice, settimanale,
  al massimo tre PR aperte per ecosistema. Nessuna etichetta personalizzata:
  se l'etichetta non esiste nel repo, Dependabot lo scrive in ogni PR.
- `pip-audit>=2.10` in `requirements-dev.txt` e un passo non bloccante in CI,
  `pip-audit -r requirements-dev.txt`, subito dopo l'installazione. Provato qui:
  risolve anche il `-r requirements.txt` annidato (13 pacchetti, nessuna
  vulnerabilità nota) e su un file con `pyyaml==5.3` esce 1 con
  `PYSEC-2020-96` e `PYSEC-2021-142`. Il cancello morde.
- `runs-on: ubuntu-24.04` nei due job, al posto di `ubuntu-latest`. Oggi è la
  stessa immagine, quindi non cambia niente; dal 19 ottobre non si sposta da
  sola. È la regola che il workflow applica già a typst («versione FISSATA,
  mai latest»). Si passa a 26.04 con una PR che la prova.

⚠️ **Una cosa che il piano prometteva e che lo strumento non fa.** «Bloccante
sulle vulnerabilità alte» presuppone un filtro per gravità, e `pip-audit` non
ce l'ha: esce 1 su qualunque avviso noto. Dopo il primo mese (2026-10-24) le
strade sono due: bloccante su tutto, con le eccezioni accettate dichiarate una
per una in `--ignore-vuln`, oppure resta un avviso. Si decide guardando cosa
avrà segnalato nel mese.

⬜ **Resta**, e non si fa da un ramo:
- la **prima PR di Dependabot**, che è il criterio di qualità del lotto: arriva
  dopo il merge, e la prima attesa è l'aggiornamento delle tre azioni su
  Node.js 20;
- la **prova del blocco dei segreti** (un segreto finto in un commit di prova):
  la fa il DM, perché un agente che tenta di spingere un segreto è esattamente
  ciò che la protezione deve fermare, e il risultato non si distinguerebbe da un
  rifiuto dei permessi della sessione;
- la **revisione con l'IA di GitHub** che fallisce per il modello, e l'esito di
  `Analyze (javascript-typescript)`: si leggono sui controlli di questa PR.

🔎 **Cosa è successo attivando le impostazioni (2026-09-24).** Insieme alla
sicurezza si sono accesi due controlli nuovi sulle PR:
- **CodeQL** (configurazione predefinita): `Analyze (python)` e
  `Analyze (actions)` verdi al primo giro sulla #160;
  `Analyze (javascript-typescript)` da guardare alla prossima PR;
- **`github-advanced-security`**, la revisione di sicurezza con l'IA di GitHub:
  **fallisce prima di leggere un file**, con `400 The requested model is not
  supported`. Il modello lo sceglie il servizio, non il repo; il rilancio da
  una sessione di agente è rifiutato (403). Va sistemato nelle impostazioni
  (cambiare modello o spegnerla) e **non va messo fra i controlli
  obbligatori** della regola di `main` finché non è verde.

🔎 **Due scadenze viste nelle annotazioni della CI il 2026-09-24**, che
appartengono a questo lotto:
- **Node.js 20 è deprecato**: `actions/checkout@v4`, `actions/setup-python@v5`
  e `actions/upload-artifact@v4` girano già forzate su Node.js 24. È il primo
  lavoro che Dependabot per `github-actions` proporrà;
- **`ubuntu-latest` diventa Ubuntu 26 dal 19 ottobre 2026.** Prima di quella
  data si decide se fissare `ubuntu-24.04` o provare la CI su 26.

#### ⬜ PI-4 · Gli scenari del piano, tracciati fino ai test
`[engine: Sonnet 5 · effort: medio · qualità: uno scenario senza test fa rosso, un test che cita uno scenario inesistente fa rosso; 2 mutazioni su 2]`

Classe **C**. **Parte solo se la D6 di CICLO-SESSIONE è (a).** È la parte del
BDD che la ricerca ha misurato utile, senza il framework:

- ogni scenario nelle tabelle Dato/Quando/Allora di un piano ha un
  identificatore (`U1`…);
- ogni test d'accettazione lo cita nel nome o nella docstring;
- `scripts/tracciabilita_scenari.py` controlla le due direzioni. Si applica ai <!-- validate-docs: futuro -->
  piani che dichiarano le storie con un marcatore, a partire da CICLO-SESSIONE.

#### ⬜ PI-5 · Proprietà sui parser
`[engine: Sonnet 5 · effort: medio · qualità: ogni generatore trova almeno un mutante che i test d'esempio non trovano, o si toglie]`

Classe **C**. I lettori da cui dipende la chiusura della sessione: il
front-matter `delta:` di `state_apply`, `validate_state`, il riconoscimento del
log in `state_sync`. Generatori scritti a mano con `random.Random(seme)`, seme
fisso e stampato quando fallisce, come chiede §5.0 di CICLO-SESSIONE. Le
invarianti sono quelle del PRD: rilanciare non duplica, tutto o niente, un
testo mai visto non fa crashare.

⚠️ Il criterio di qualità è severo di proposito. Un test di proprietà che non
trova niente in più dei test d'esempio è cerimonia, e l'elenco del DM lo
consiglia per i parser, non ovunque.

#### ⬜ PI-6 · Il canone toccato, detto nella PR
`[engine: Sonnet 5 · effort: basso · qualità: su questa PR elenca i file del Collezionista e di Therysol; su una PR di soli script non elenca niente]`

Classe **C** per lo strumento, **K** per la lettura del DM.

- `.github/pull_request_template.md`: le sezioni che i corpi delle PR di questo
  repo hanno già (lotti, verifica, resta al DM), più **«Canone toccato»**.
- Uno script elenca i file di canone cambiati rispetto alla base: cronaca e
  premessa, `Bestiario/`, `skills/rumblingstone-campaign/references/`,
  `campaign/state.*`, i master d'arco. Il corpo della PR riporta l'elenco, e il
  DM legge **quelli**, non 119 file.

## §6 · Fase 3 · Validazione

| Lotto | Come si sa che funziona | Rimisura dopo 30 giorni |
|---|---|---|
| PI-1 | push diretto su `main` rifiutato; una PR rossa non si mergia | — |
| PI-2 | `misura_flusso` ridà 267 / 13 su 34 su `origin/main` del 2026-09-24; il suo test fa rosso se una mutazione conta i file generati come codice | mediana delle righe di codice, quota sopra 400, rami anteriori a 30 giorni |
| PI-3 | un segreto finto viene bloccato in push; `pip-audit` gira in CI | avvisi di Dependabot aperti e chiusi |
| PI-4 | due mutazioni del gate, una per direzione | scenari di CICLO-SESSIONE con test: da 0 su 7 |
| PI-5 | almeno un mutante per parser ucciso solo dalle proprietà | difetti trovati dai generatori |
| PI-6 | l'elenco su questa PR contiene i sei file del Collezionista | PR con canone toccato e letto dal DM |

Un criterio vale per tutto il piano: **la CI di `main` resta 40 su 40**. Una
pratica nuova che la fa diventare rossa si corregge o si toglie.

## §7 · Decisioni aperte

<!-- decisioni-dm: PRATICHE -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | PI-2 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **La soglia delle 400 righe di codice per PR, come avviso in CI?** Oggi 13 merge su 34 la superano, e questa PR la supera di otto volte. Proposta: sì, avviso e non blocco |
| ~~D2~~ | PI-3 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Dependabot, scansione dei segreti con push protection, `pip-audit`?** Le prime due si attivano nelle impostazioni del repository e sono gratuite perché il repo è pubblico. Proposta: sì a tutte e tre, `pip-audit` non bloccante per un mese |
| ~~D3~~ | PI-6 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Le PR che toccano il canone si mergiano solo dopo la tua lettura dell'elenco?** Proposta: sì. Il resto lo verificano i gate |
| ~~D4~~ | PI-1 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). **Il merge automatico delle PR verdi**, una volta protetto `main`? Proposta: sì, ed è ciò che rende economiche le PR piccole |
| ~~D5~~ | PI-2 | ✅ **Risposta del DM il 2026-09-24: sì** (*«d1-d5 del piano pratiche di ingegneria sì»*). L'elenco misurato dopo `git fetch --prune` è di **38** rami, ed è nella risposta al DM dello stesso giorno: si cancellano quando il DM lo conferma. **I 39 rami remoti già interamente su `main` si cancellano?** L'elenco lo produce `misura_flusso`; `contenuti-nei-rami.json` conferma che non portano niente di nuovo. Proposta: sì, dopo che hai visto l'elenco |

| ~~D6~~ | tutti | ✅ **Risposta del DM il 2026-09-24: (a).** **Come si esegue la regola di D1 dopo la #160?** (a) un ramo e una PR per lotto, (b) si aspetta il merge della #160 e si riparte sullo stesso ramo un lotto alla volta. Da qui ogni lotto di questo piano ha un ramo suo e una PR sua in bozza |
| ~~D7~~ | PI-2 | ✅ **Risposta del DM il 2026-09-24: no.** Gli 11 rami del gruppo B restano. La misura riga per riga (`plans/esperimenti/misura-rami/misura_rami.py`) dà otto rami con tutto su `main` e tre (#42, #109, #67) con contenuto giudicato ma non su `main`; il DM: *«ci sono delle varianti che si possono estrarre e integrare nel main»*. Le varianti dei tre sono il lotto [RIPRESA-PR 4j-4](PIANO-RIPRESA-PR-ABBANDONATE.md) |
| ~~D8~~ | PI-2 | ✅ **Risposta del DM il 2026-09-24: no, e il recupero previsto davvero** (*«no solo se è previsto davvero il recupero, altrimenti mantieni»*). I due rami senza PR restano finché il loro recupero non è chiuso: il Torneo di Dauth di maggio è [RIPRESA-PR 4j-1](PIANO-RIPRESA-PR-ABBANDONATE.md), `measure_tokens.py` è 4j-3 |
| ~~D9~~ | PI-3 | ✅ **Risposta del DM il 2026-09-24: sì agli avvisi, no alle PR settimanali** (*«d9 ok, non le PR di aggiornamenti settimanali»*). **Dependabot anche per `converters/`?** Gli avvisi di sicurezza vengono dal grafo delle dipendenze, che legge già `converters/Html_to_markdown` e `converters/pdf-to-md-engine`; `dependabot.yml` resta sulla radice, e un commento in testa dice perché |

PI-4 non ha una decisione qui: dipende dalla D6 di CICLO-SESSIONE.

⚠️ **Da non confondere**: queste sono `PRATICHE#D1`-`D5`. Le D1-D6 di
[PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §8 sono
altre decisioni (cronaca automatica, alleanze, prosa, menu, immagini, BDD), e
restano **aperte**.

### §7.1 · I rami della D5, misurati il 2026-09-24

Dopo `git fetch --prune`: **38** rami remoti interamente contenuti in
`origin/main`. Nessuno è un ramo di gruppo `campaign-group-*`, nessuno è la testa
di una PR aperta (#99, #106). Il DM ha detto sì alla D5 e ha chiesto che la
pulizia si faccia nella conversazione successiva: prima di cancellare si
**rimisura**, perché nel frattempo un ramo può aver ricevuto commit.

```bash
git fetch --prune origin
git fetch --unshallow origin 2>/dev/null   # vedi l'avvertenza qui sotto
for b in $(git for-each-ref refs/remotes/origin --format='%(refname:short)' | grep -v -E 'HEAD|origin/main$'); do
  git merge-base --is-ancestor "$b" origin/main && echo "${b#origin/}"
done
```

🐛 **Rimisura del 2026-09-24, seconda conversazione: su un clone shallow il
comando sbaglia in silenzio.** Il clone di una sessione d'agente scarica gli
ultimi commit e basta, e `merge-base --is-ancestor` risponde «no» per ogni
ramo la cui testa sta sotto il taglio. Il primo giro ha dato **13** rami su
`main` invece di 38, e 25 rami vecchi di luglio sembravano portare lavoro mai
arrivato. Con `git fetch --unshallow` il conto torna a **38, gli stessi 38** del
primo elenco. `contenuti_nei_rami.py` lo avvisa già («clone shallow? usare
--fetch»); il ciclo qui sopra no, per questo ora ha la riga in più.

Rimisurati i 38, nessuno è la testa della #99 o della #106, e
`claude/festive-tesla-tgsauj` non c'è più: GitHub l'ha tolto al merge della
#160. **La cancellazione non è partita dalla sessione d'agente**: i permessi
della sessione rifiutano `git push --delete` come azione distruttiva. La
esegue il DM, con il comando in STATO-E-ORDINE §7.2. Lo SHA di ogni testa è
nella tabella: con quello un ramo cancellato si ricrea
(`git push origin <sha>:refs/heads/<ramo>`).

| Ultimo commit | SHA della testa | Ramo |
|---|---|---|
| 2026-07-01 | `331ce0732b33dfea9a584bc0fe60635abe589d87` | `claude/rhod-army-calculations-9TO1B` |
| 2026-07-02 | `3598c7b38f457af247cecabb0ec7628cdaa64327` | `claude/hammerfist-adventure-review-lqmdfu` |
| 2026-07-02 | `68f2091851007999cbcb8cbcb0bb1ff0bd8f29d7` | `claude/lotto-orphan-subquests-xwyb27` |
| 2026-07-02 | `ee04017bcfc15fefac08dd3f269aa3261117f879` | `claude/lotto-plan-token-availability-ahoco4` |
| 2026-07-02 | `03df20aca8993225eb9d06ccf7164d7a9e42f49d` | `claude/lucid-bell-yv0vg0` |
| 2026-07-02 | `0f728d0d2580d8bfb47bf6999964408ee0469255` | `claude/palio-channathgate-expansion` |
| 2026-07-02 | `266217163bafd411b4a64c2eca21a8c53d19fec9` | `claude/piano-revisione-arco-09-dh32ad` |
| 2026-07-03 | `1551c6615080f30d47641b098f5b23f1d07f75e6` | `claude/arc-07-09-review-fyxrc0` |
| 2026-07-03 | `2d1d582dce8a77433b40c539015acdea72564cd5` | `claude/arc-07-09-review-q3p3pp` |
| 2026-07-03 | `6ae17edc01b69d1d4ea45decdadc76077b0a134c` | `claude/dnd-pathfinder-agent-skills-jjyp6u` |
| 2026-07-03 | `12ea2a8bb9d9f396193568a2a9a993874f823b54` | `claude/piano-revisione-arc07-exec-cafnw4` |
| 2026-07-03 | `d149e7a388596933b615669c952022b49379c99b` | `claude/piano-revisione-arc08-rumbling-stone-ha5zk2` |
| 2026-07-10 | `29105852574815c481f965567142da7fc70e10fa` | `claude/piano-revisione-completion-ujdv60` |
| 2026-07-12 | `e824ca1e6d9ca0a37eec65315189c2fae7d36c40` | `claude/campaign-assets-library-restructure-cx2uti` |
| 2026-07-19 | `b22925850cfc73b9411cd48f67a7939d1f5f1ef1` | `claude/analisi-pr-commit-plan-q94cud` |
| 2026-07-19 | `651f98ff37a25e3d9f67273914f0313142595e30` | `claude/palio-compliance-check-enlu8j` |
| 2026-07-20 | `597c83f130ee87852ef70a7b05d1d751793320fa` | `claude/rumblingstone-campaign-state-management-pgkyc5` |
| 2026-07-20 | `62b9516cb7e942c4ec80921f49ccc8a7deb75df9` | `claude/rumblingstone-content-audit-n000d8` |
| 2026-07-20 | `e2cab058fdb6e9b35c50f4f629939dc54b15663e` | `claude/rumblingstone-png-assets-ykunrc` |
| 2026-07-20 | `3d848a126779f99b524830eb3a1eaa03a747d7e0` | `claude/rumblingstone-skills-update-j7ke6y` |
| 2026-07-23 | `f09573aefe3190fe7d1ab24157a4c531b8f05e86` | `claude/bugbear-assassin-section-recovery-1pyw3r` |
| 2026-07-23 | `5d815de48ee42af259679f15ba0d12f7d38b2acc` | `claude/rumblingstone-forgia-audit-vgzav8` |
| 2026-07-24 | `7f9b660a0ad9b81f5217adc9ec230e3f74cfe9e8` | `claude/freecad-map-generation-qfaow8` |
| 2026-07-24 | `5b8a5eeb81174f38ad762ed7738c164120d54e92` | `claude/piani-completare-5b85qg` |
| 2026-08-23 | `0a2b2fc2973a955c07f0b6b1a979eeb8adb404bb` | `claude/rumblingstone-section-check-ustn8s` |
| 2026-08-26 | `4cc505a06710d046ffaf72bbfed88ec19fe99f39` | `claude/adventure-game-generation-skills-cevaqt` |
| 2026-09-01 | `d3c214003b8efb19372f99e64cd84bfb25cad01d` | `claude/golarion-pathfinder-campaign-xbyvzt` |
| 2026-09-01 | `e3987b0b132b33a266a20fb314777d199168ad1c` | `claude/rumblingstone-campaign-tools-40pt1b` |
| 2026-09-03 | `f4f9028758335f801756453e6ed9dc7ed1963a38` | `claude/lotto-d-piano-prosa-kj9bbm` |
| 2026-09-03 | `8fdfd1b25956cdfeaf3514adadab35949de353e5` | `claude/rumblingstone-analysis-kh4yfa` |
| 2026-09-03 | `97423d94c58a319dae623bcb9fbf151580e78022` | `claude/rumblinstone-overdue-plans-nvjy9m` |
| 2026-09-04 | `8ce2ebedf1c8d599318a37846056f9fb4f86b3fc` | `claude/monster-png-generation-questions-8c36yp` |
| 2026-09-04 | `2f55fc0b32ba47435a6f127cb043320b16b5b7b1` | `claude/rumblingstione-analysis-enhancement-p44wk5` |
| 2026-09-21 | `dd2687517344ce239322fd798fb9992dad397998` | `claude/open-prs-plans-review-fu4qcp` |
| 2026-09-23 | `e17c6fecb632f256255b02feefd749130518aec6` | `claude/busy-planck-gkzrur` |
| 2026-09-23 | `2151b185efb08859f265abdf8575ffddb93ad834` | `claude/funny-newton-l813cs` |
| 2026-09-23 | `b36ce256dcff7a3bb7f53c916eaaf22a5b6f54e6` | `claude/gallant-sagan-to3cr6` |
| 2026-09-23 | `2a9700f197cec83a1ae0724c1ed2ee54aa9dc41d` | `claude/youthful-thompson-o1kktp` |

✅ **Cancellati dal DM il 2026-09-24**: 38 su 38, verificato con
`git ls-remote` subito dopo. Sono spariti anche `claude/festive-tesla-tgsauj`
e `claude/focused-meitner-pgyb20`, i rami delle #160 e #162, tolti al merge.

### §7.2 · I 17 rami rimasti, misurati il 2026-09-24 dopo la pulizia

Nessuno è interamente contenuto in `main`, quindi il ciclo di §7.1 non li
vede. Ma non vuol dire che portino lavoro nuovo: una PR mergiata con squash
lascia il ramo «fuori» da `main` anche se il suo contenuto c'è tutto. Il
metodo: la testa del ramo confrontata con le teste delle PR
(`git ls-remote origin 'refs/pull/*/head'`), `git cherry`, il registro dei
rami, e per i casi dubbi il diff contro `main`.

🔎 **Il fatto che rende sicura la cancellazione**: quando un ramo con una PR
viene cancellato, GitHub tiene il suo contenuto in `refs/pull/<N>/head`.
Lo si è visto sulle PR dei 38: le loro teste sono ancora tutte lì, 162
riferimenti.

**A · da tenere**

| SHA della testa | Ramo | Perché |
|---|---|---|
| `d100709a4271cd88403093d27d3a4a84bdd03930` | `campaign-group-rumblingstone-dm-gianfranco` | ramo di partita del gruppo (ADR-0007) |
| `fce049071d6156d76321b5fb2c7ac733071d5930` | `claude/stone-audit-best-practices-yver7k` | PR #99 aperta |
| `80a91a220763f58d184a8f1947b29942c260e848` | `claude/pr-105-raster-generation-bq0efs` | PR #106 aperta |
| `64df2ebc8f87992e951b212e59996866ad4bf326` | `claude/salvatore-character-art-wSjuH` | **porta tre correzioni che su `main` non ci sono**: vedi sotto |

**B · misurati riga per riga (D7)**

Il DM, sulla classificazione qui sopra: *«prima misura davvero se non c'è
niente, non ti fidare»*. Aveva ragione a chiederlo: la prima stesura di
questa tabella dava #52 e #63 per «riportati» senza averlo contato, e la
misura ha trovato due rami su tredici che non vanno cancellati (gruppo C).

Lo strumento è `plans/esperimenti/misura-rami/misura_rami.py`: per ogni riga
che il ramo aggiunge, cerca la stessa riga su `main`, poi una quasi uguale
(somiglianza ≥ 0,9) nello stesso file o in un file con lo stesso nome. SVG e
immagini non contano. Il controllo positivo è il ramo Salvatore: 3 righe
mancanti su 3. Le righe mancanti degli altri rami sono state lette.

| SHA della testa | Ramo | Righe aggiunte | Mancanti su `main` | Cosa sono le mancanti |
|---|---|---:|---:|---|
| `006338e384399923eae4405dfd62f07745b09122` | `claude/documento-stemmi-alternativi-ehgi9m` (#102) | 31 | 0 | — |
| `aab266cc89fde924998f02b3227f0c564b7ad96f` | `claude/campaign-session-tools-j2dzx1` (#92) | 808 | 5 | l'avvertenza sul «−2 DES» di Tordek, tolta apposta perché era il malus di un altro PG (STATO-E-ORDINE §1, R1) |
| `3e4315336db109940d53783e59be5f71d0606b18` | `claude/rumbling-stone-casters-oxzi2w` (#98) | 104 | 2 | la voce di Ushgar in `monster_catalog.yaml`, rigenerata con un nome nuovo |
| `219a5eb031dd24256959c0f762281ead4685aa91` | `claude/paizo-editorial-components-qky8nv` (#120) | 1.115 | 20 | numeri della misura della prosa del 2026-09-03, poi rimisurati |
| `7293e923a6739a00c8641a21f9c65585249fc4e3` | `claude/scripts-audit-documentation-u48g28` (#66) | 17.856 | 166 | descrizioni nei manifest e nei registri degli strumenti, file generati e rigenerati da allora |
| `571c209c4076264159dca04a60ca1f3b41b52dbf` | `claude/hammerfist-maps-ultra-clear-9pczfe` (#63) | 1.422 | 28 | avvisi sui master `Lotto-*` e righe di piano del ramo; RIPRESA-PR F1 ha riportato le griglie tenendo i sette SVG che la #63 toglieva |
| `e5cf517799550a81fedf0767313be7c892c992f5` | `claude/map-generation-pipeline-7ka5a7` (#52) | 147 | 1 | la riga di CHANGELOG del ramo |
| `974e9260193453e4c0b385a7d08001f838d9194e` | `claude/document-audit-prd-cleanup-j5ipln` (#143) | 572 | 5 | le stesse righe con un marcatore `validate-docs` aggiunto, e il titolo dell'ADR rinumerato 0067 |
| `4986ce87cb7826c804df3be3c34a1f3e3614b30b` | `claude/dnd-map-generation-research-55pzry` (#42) | 264 | 245 | **contenuto vero** (un master del Portale, 11 righe di `render_map_svg.py`): PR rifiutata dal DM il 2026-09-03, resta in `refs/pull/42/head` |
| `c45c9cc43d64cb6723682a96f56b58f364267cfe` | `claude/golarion-pregen-character-sheets-cstheq` (#109) | 134 | 130 | **contenuto vero** (ADR-0021 e il caricamento esplicito delle skill): superato da ADR-0041, resta in `refs/pull/109/head` |
| `23f14b607be177699b915c33dbaa7f9e022dee6a` | `claude/terros-battle-hints-booklet-hfvbef` (#67) | 364 | 308 | **contenuto vero** (un booklet HTML): superato dal booklet da manifest, resta in `refs/pull/67/head` |

**C · da tenere: portano lavoro che su `main` non c'è (D8 = no)**

| SHA della testa | Ramo | Righe aggiunte | Mancanti | Cosa porta |
|---|---|---:|---:|---|
| `895863241eaff57d135ed1b2527bd9f55009c2c1` | `claude/review-tournament-integration-yYlwv` | 834 | 813 | il Torneo di Dauth di maggio: master del DM, echi a lungo periodo, sotto-quest di Artemis, Hella e Thorik, il Giorno 3 |
| `b5e04d2d78799a56bcfa8257c09bc0d817d61e28` | `claude/optimize-skills-agent-folders-dwJC4` | 281 | 182 | per lo più infrastruttura di maggio rifatta dopo (`agents.conf`, `build-skills.sh`, `validate_skill_paths.py`); **ma** la correzione di `measure_tokens.py` che conta i file di caricamento obbligatorio non c'è su `main` |

🔴 **Il Torneo di Dauth è stato scritto due volte.** Il 2026-07-02 il lotto A
di [PIANO-REVISIONE-ARC09](PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA.md) (voce
A8) ha trovato «inesistenti» i file del Torneo citati come fonte e li ha
creati consolidando il materiale sparso, dichiarando le sotto-quest di Artemis
e Hella e il Giorno 3 «mai scritte». Erano scritte dal 2026-05-03, in questo
ramo, mai mergiato. Le versioni di `main` sono più corte per il master (166
righe contro 290) e per gli echi (93 contro 229), più lunghe per Artemis e
Hella, riscritte a settembre. Il Giorno 3 di maggio contraddice il canone di
oggi su Karruk (registro dei rami, D22). È lo schema della #72: un lavoro
riscritto da chi non sapeva che esisteva.

🔴 **Il ramo Salvatore, e il punto cieco che ha mostrato.** Un commit del
2026-05-02, tre righe su due file, e nessuna delle tre è su `main`:

- `Bestiario/villain/Salvatore/Salvatore.md` scrive «Matrona Sajak»; il ramo
  aggiunge che è Sonjak. **Non è un errore**: `state.md` dice
  «Sonjak (= Matrona Sajak)», quindi Sajak è un alias ammesso e la riga del
  ramo è un chiarimento;
- lo stesso file dà i PF come «79 (14 DV: 13d6+28)», e il ramo li scrive
  «79 (14d6+28)»;
- il testo P2C fa de-pietrificare le statue con *Rimuovere Maledizione*; il
  ramo lo sostituisce con *Pietra in Carne* o *Sciogliere Incantesimo*.
  **Verificato sulle schede PCGen del repo**
  (`Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/Duergar_figther_ponte/cleric_11_abbathr_spell.htm`):
  *Break Enchantment* (PHB p. 207) «frees subjects from enchantments,
  alterations, curses, and petrification», ed è di 5° livello (CD 19 contro
  la CD 17 di *Remove Curse*, 3°, per lo stesso chierico); *Remove Curse*
  (p. 270) toglie le maledizioni e non nomina la pietrificazione. Il livello di
  *Stone to Flesh* non è in nessun file del repo.

Il ramo sembrava cancellabile perché il registro dei rami **conta i file
nuovi e non vede le modifiche a file esistenti**. Il porting è un lotto K, il
punto cieco un lotto C: STATO-E-ORDINE §8.2. `misura_rami.py` è il prototipo
del secondo.

## §8 · Ordine

PI-1 e PI-3 prima, perché sono impostazioni e costano minuti. Poi PI-6, che
avrebbe fermato Varis. Poi PI-2, PI-5 e, se la D6 lo dice, PI-4, ognuno in una
PR sua: il primo esercizio della norma di PI-2 è questo piano stesso.

## Checklist di avanzamento

- ✅ Fase 1 · audit (§2, 2026-09-24)
- ⬜ PI-1 · `main` protetto e merge automatico (DM, con 4i-3). 2026-09-24: `main` risulta `protected: true` via API; il dettaglio delle regole, il merge automatico e la sicurezza non si leggono da qui e si verificano alla prima PR indietro rispetto a `main`
- 🟡 PI-3 · Dependabot, segreti, `pip-audit`. D9 decisa: `converters/` solo con gli avvisi del grafo. 2026-09-24: `dependabot.yml`, `pip-audit` in CI (non bloccante), runner fissato a `ubuntu-24.04`; restano la prima PR di Dependabot, la prova del segreto (DM) e la revisione con l'IA (impostazioni)
- ⬜ PI-6 · canone toccato nella PR
- ⬜ PI-2 · `misura_flusso` e la norma delle 400 righe. 2026-09-24: cancellati i 38 rami già su `main` (D5); 17 rimasti misurati riga per riga in §7.2: D7 = no e D8 = no, i rami restano; il recupero è RIPRESA-PR 4j
- ⬜ PI-5 · proprietà sui parser
- ⬜ PI-4 · scenari tracciati (se CICLO-SESSIONE D6 = a)
- ⬜ Fase 3 · rimisura a 30 giorni
