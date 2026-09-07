---
name: rumblingstone-plans
description: >
  Plan-archive discipline for the RumblingStone repo — where work plans and
  research docs live and how their completion is tracked. Use WHENEVER
  creating, updating, completing, or merging a piano/lotto/ricerca/iniziativa,
  opening or closing a PR that implements one, or when asked "dov'è il piano",
  "aggiorna il changelog", "traccia le modifiche", "archivio piani",
  "che stato ha il piano X". Trigger on: "piano", "lotto", "PIANO-*",
  "RICERCA-*", "plans/", "INDEX", "CHANGELOG", "ADR", "chiudi/completa il
  piano", "merge della PR". Enforces the repo's golden rule: every closed
  lotto updates plan checklist + plans/INDEX.md + plans/CHANGELOG.md in the
  SAME commit.
---

# RumblingStone — Archivio Piani (disciplina di tracciatura)

Ogni lavoro strutturato del repo (revisioni, infrastruttura, ricerche) è
tracciato in **`plans/`**. Senza questa disciplina le modifiche restano
sparse nelle PR mergiate e la storia si frammenta. Fonte delle regole:
`plans/PIANO-DM-TOOLKIT-HYPE-E-ARCHIVIO-PIANI.md` (Lotto K-A) e l'header di
`plans/INDEX.md`.

## Dove vivono le cose

| Cosa | Dove |
|---|---|
| Piani di lavoro (con lotti/checklist) | `plans/PIANO-<NOME>.md` |
| Ricerche/valutazioni (input di futuri piani) | `plans/RICERCA-<NOME>.md` |
| Decisioni architetturali (il "perché") | `plans/adr/` |
| Vista d'insieme: stato, %, lotti rimanenti, gate | `plans/INDEX.md` |
| Storia: una riga per lotto chiuso | `plans/CHANGELOG.md` |

## ⚖️ Regola d'oro (obbligatoria, non opzionale)

**Chi chiude un lotto/piano/iniziativa aggiorna — NELLO STESSO COMMIT:**

1. la **checklist del piano** (o la nota "STATO ATTUAZIONE" di una ricerca);
2. la **riga del piano in `plans/INDEX.md`** (stato, %, lotti rimanenti,
   gate) e la sua sezione "Prossimi passaggi";
3. **una riga in `plans/CHANGELOG.md`**:
   `| data | piano | lotto | riferimento (PR #N / commit) | esito |`.
4. se il lotto **chiude o apre una decisione del DM**: la riga nella tabella
   marcata `<!-- decisioni-dm: … -->` **dentro il piano**, poi
   `python3 scripts/decisioni_dm.py --emit` per rigenerare l'aggregato di
   `STATO-E-ORDINE` §4 (ADR-0047). Chiusa = identificatore **barrato**:
   `~~D1~~`. Si tocca il piano, mai l'aggregato.

## 🔍 Regola di apertura (obbligatoria — ADR-0044)

**Prima di aprire un piano nuovo, si guardano quelli che ci sono.** Nell'ordine:

1. **Leggi `plans/INDEX.md`.** È l'unico posto dove sta scritto cosa esiste e a
   che punto è. Sono trentaquattro documenti: nessuno se li ricorda a memoria, e
   chi non guarda riscrive.
2. **Cerca per argomento, non per titolo.** Un piano che copre la tua richiesta
   può chiamarsi in un altro modo:
   `grep -ril "<parola chiave>" plans/*.md`.
3. **Guarda anche le PR aperte.** Un piano può esistere e non essere ancora su
   `main` — è successo con la #72, che stava in bozza da sei settimane con
   dentro tre piani commerciali poi riscritti da zero da chi non l'aveva letta.
4. **Poi decidi, e scrivi quale delle tre è**:

| Se… | Allora |
|---|---|
| esiste un piano che copre l'argomento e il lavoro è **dentro il suo perimetro** | **espandi quel piano** con un lotto nuovo. Niente documento nuovo |
| esiste un piano **vicino** ma il tuo lavoro è un difetto suo | **fix nel piano esistente**, e una riga nel CHANGELOG |
| non esiste niente che copra l'argomento | **apri**, e nel documento nuovo scrivi **cosa hai guardato prima** e perché non bastava |

⚠️ **Il §1 di un piano nuovo dice sempre cosa NON rifà.** Un piano che non
dichiara i suoi confini contro i piani vicini si sovrappone entro un mese: è
successo cinque volte, e le cinque sovrapposizioni sono finite in
`PIANO-VENDIBILITA`.

**PIANO o RICERCA?** Una **RICERCA** misura un divario e propone; un **PIANO**
esegue. Se non sai ancora cosa fare, è una ricerca — e la ricerca può poi
aprire un piano, citandosi.

## 🧭 Come si tagliano i lotti (obbligatoria — ADR-0045)

Ogni lotto **ancora da fare** dichiara tre cose in intestazione:

```
[engine: <chi lo esegue> · effort: <basso|medio|alto|xhigh|max> · qualità: <come si sa che è finito>]
```

| Classe | Che cos'è | Engine | Effort | Qualità |
|---|---|---|---|---|
| **M · Meccanico** | trasformazione verificabile: **un gate dice** se è giusta | inline, o `Haiku 4.5` in subagente | basso | il gate passa |
| **R · Ricognizione** | leggere molto, riferire poco, **non decidere** | subagente `Explore`, `Sonnet 5` | basso-medio | i numeri si **riproducono** |
| **C · Costruzione** | codice con contratto chiaro e test | `Sonnet 5` | medio-alto | test che provano il gate **mordere** |
| **G · Giudizio** | decidere cosa è vero, cosa si butta, cosa si sovrappone | **`Opus 5`, sessione principale** | alto-xhigh | il DM riconosce il proprio problema |
| **K · Canone** | tocca la verità della campagna | **`Opus 5`, mai delegato** | xhigh-max | conferma esplicita del DM |

**Come si sceglie la classe — la tabella illustra, queste domande decidono.**
Si risponde nell'ordine; la prima che scatta assegna la classe.

| | Domanda | Se sì |
|---|---|---|
| 1 | **Se sbaglio, se ne accorge il DM al tavolo?** | **K** — nessun gate difende il canone |
| 2 | Devo decidere qualcosa che **una macchina non può contare**? | **G** |
| 3 | Il risultato è definito da un **contratto verificabile**? | **C** se il contratto va scritto, **M** se esiste già |
| 4 | *(nessuna)* Sto solo **leggendo per riferire**? | **R** |

⚠️ **Nessuna delle quattro chiede quanto è grande il lotto.** La dimensione non
entra nella classificazione, ed è dove l'istinto sbaglia più spesso: *«sostituisci
Tordek con Thorik in dodici file»* sembra un `sed` ed è la riscrittura di un eco.

**A lotto chiuso, una riga in [`plans/REGISTRO-LOTTI.md`](../../plans/REGISTRO-LOTTI.md)**
— classe prevista, engine usato, **ha retto?**. È come la tabella smette di
essere tarata a occhio. Se il lotto è **salito di classe** a metà strada, quella
riga vale doppio.

**Tre regole che governano la tabella:**

1. **L'effort si abbassa prima dell'engine.** Un modello capace a effort basso
   spesso batte un modello inferiore a effort alto, e **non spezza la cache** —
   le cache sono legate al modello, quindi ogni salto di engine la butta.
2. **Un lotto sale di classe, mai scende.** Nel dubbio fra M e C scegli C; fra G
   e K scegli K. Un lotto sovradimensionato costa token; uno sottodimensionato
   costa un errore che arriva al tavolo.
3. **La colonna «qualità» non è una leva: è il collaudo.** Se non riesci a
   scriverla, il lotto è **tagliato male** — ritaglialo prima di eseguirlo.

**Dove si taglia**: sulla **classe**, non sulla dimensione. Un lotto che mescola
classi si divide — la parte **G** decide, la parte **M** esegue.

⚠️ **Non si riclassificano i lotti già chiusi**: instradare un lavoro finito è
spreco puro.

⚠️ **`Haiku 4.5` non è un Opus più piccolo**: 200K di contesto contro 1M, e
**non accetta `effort`**. Per lavoro corto e meccanico, non «per risparmiare».

## ✅ Rituale di chiusura PR (checklist per l'agente)

Prima di aprire (o dichiarare pronta) una PR che completa lavoro pianificato:

- [ ] Il documento del lavoro esiste in `plans/` (PIANO o RICERCA)? Se il
      lavoro è nato "spontaneo" da una richiesta, creare almeno la voce di
      tracciatura (non serve un piano formale per tutto — serve la riga).
- [ ] `plans/INDEX.md`: riga di stato aggiornata + "Prossimi passaggi"
      (anche solo ⬜ opzionali/gated).
- [ ] `plans/CHANGELOG.md`: riga aggiunta con riferimento alla PR.
- [ ] Se la PR introduce tooling/script: `scripts/README-automation.md`
      (tool map) aggiornato.
- [ ] Se la PR introduce/tocca una skill: `./scripts/build-skills.sh
      --no-deploy` e `python3 scripts/validate_skills.py` verdi.
- [ ] Nuova convenzione o scelta strutturale? → ADR in `plans/adr/`.

## 🤖 Enforcement automatico (ADR-0009)

La regola d'oro non è più solo disciplina — `scripts/check_plans_discipline.py`
gira in CI su ogni PR e come hook `pre-push` locale
(`./scripts/install-git-hooks.sh`):

- **Blocca** (rosso in CI, push rifiutato) modifiche a file strutturali
  (`scripts/`, `skills/`, `converters/`, `.github/`, `plans/adr/`) senza una
  riga in `plans/CHANGELOG.md` nello stesso range di commit.
- **Blocca** l'aggregato di `STATO-E-ORDINE` §4 che non combacia con le tabelle
  dei piani (`scripts/decisioni_dm.py --check`, ADR-0047). Era la quarta cosa
  della regola d'oro, l'unica non controllata: il 2026-09-06 dava una decisione
  aperta il giorno dopo che era stata presa, ne ometteva un'altra e ne elencava
  quattro **inesistenti in ogni piano**.
  ⚠️ `D<n>` **non è globale**: otto piani hanno il loro `D1..Dn` con significati
  diversi, quindi conta solo ciò che porta il marker, e l'identità è `piano#Dn`.
- **Promemoria ADR** (warning non bloccante): nuova skill, nuovo script
  top-level o modifica ai workflow CI senza alcun tocco a `plans/adr/` →
  invito esplicito a valutare un ADR. Non bloccante di proposito: «serve
  un ADR?» resta una decisione umana, non di uno script.
- Il contenuto di campagna (`campaign/`, archi `00_`-`09_`, `Bestiario/`,
  `PG/`) è esente: le sessioni giocate non richiedono changelog.
- Bypass locale consapevole: `git push --no-verify` (la CI resta il gate
  finale).

Se una PR è già stata mergiata senza tracciatura (com'è successo alla
PR #40 prima di questa skill): recuperare subito con un commit dedicato
`docs(plans): tracciatura PR #N` — mai lasciare buchi nella storia.

## Note

- Le voci di INDEX/CHANGELOG citano **fatti verificabili** (PR, commit,
  file), mai intenzioni. Gli esiti parziali si dichiarano (🟡 + cosa manca
  + gate), non si arrotondano a ✅.
- I "Prossimi passaggi" di INDEX si lasciano ⬜ finché il tavolo/DM non
  decide: il vuoto dichiarato è informazione, il vuoto implicito no.


## Richieste complesse → piano con routing engine & impegno (regola DM 2026-07-22)

Per OGNI richiesta comprensibilmente complessa (multi-fase, multi-file, più
sessioni di lavoro, o che tocca canone+meccanica+prosa insieme) l'agente
produce PRIMA un piano dettagliato — nel formato `plans/PIANO-<NOME>.md` o
inline se effimero — in cui **ogni fase dichiara**:

1. **Cosa** produce (deliverable + criterio di accettazione);
2. **Engine consigliato** e **livello di impegno**, per ottimizzare il flusso
   e il consumo di token:

| Tipo di fase | Engine | Impegno |
|---|---|---|
| Find/replace, validazioni, rigenerazione cataloghi, lint | **Haiku** (o script deterministico: sempre preferito se esiste) | basso |
| Redazione standard: statblock, tabelle, mappe ASCII, handout | **Sonnet** | medio |
| Consolidamento narrativo, coerenza cross-arc, decisioni di design, audit | **Opus** | alto |
| Ricognizioni larghe del repo (molti file, serve solo la conclusione) | subagent **Explore** | medio |
| Prosa d'autore su scene cardine (solo su richiesta esplicita del DM) | **Fable/Mythos** | alto |

3. **Dieta di contesto** per fase: passare all'engine SOLO i file del lotto
   (mai riletture dell'intero arco — regola anti-spreco dei piani ARC).

**CI/CD**: questa regola NON è un gate bloccante — giudicare la complessità
di una richiesta o la scelta d'engine non è deterministico, e un gate
semantico in CI sarebbe cattiva pratica. Il gate resta ADR-0009 (tracciatura
nel CHANGELOG); la review meccanica dei contenuti è `validate_modules.py`
(token-free). Questa sezione è la disciplina che l'agente applica DA SOLO
quando riceve la richiesta.
