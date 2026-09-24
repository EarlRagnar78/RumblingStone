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

#### ⬜ PI-3 · La catena di fornitura
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

PI-4 non ha una decisione qui: dipende dalla D6 di CICLO-SESSIONE.

⚠️ **Da non confondere**: queste sono `PRATICHE#D1`-`D5`. Le D1-D6 di
[PIANO-CICLO-DI-SESSIONE-E-MENU](PIANO-CICLO-DI-SESSIONE-E-MENU.md) §8 sono
altre decisioni (cronaca automatica, alleanze, prosa, menu, immagini, BDD), e
restano **aperte**.

## §8 · Ordine

PI-1 e PI-3 prima, perché sono impostazioni e costano minuti. Poi PI-6, che
avrebbe fermato Varis. Poi PI-2, PI-5 e, se la D6 lo dice, PI-4, ognuno in una
PR sua: il primo esercizio della norma di PI-2 è questo piano stesso.

## Checklist di avanzamento

- ✅ Fase 1 · audit (§2, 2026-09-24)
- ⬜ PI-1 · `main` protetto e merge automatico (DM, con 4i-3; le istruzioni passo passo sono state date al DM il 2026-09-24)
- ⬜ PI-3 · Dependabot, segreti, `pip-audit`
- ⬜ PI-6 · canone toccato nella PR
- ⬜ PI-2 · `misura_flusso` e la norma delle 400 righe
- ⬜ PI-5 · proprietà sui parser
- ⬜ PI-4 · scenari tracciati (se CICLO-SESSIONE D6 = a)
- ⬜ Fase 3 · rimisura a 30 giorni
