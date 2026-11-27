---
name: rumblingstone-plans
description: >
  Disciplina dell'archivio dei piani di RumblingStone: dove vivono piani di
  lavoro e ricerche, come si apre un piano, come si taglia un lotto e come se
  ne traccia la chiusura. Da usare OGNI VOLTA che si crea, aggiorna, completa
  o fonde un piano/lotto/ricerca/iniziativa, si apre o si chiude una PR che ne
  realizza uno, o quando si chiede "dov'è il piano", "aggiorna il changelog",
  "traccia le modifiche", "archivio piani", "che stato ha il piano X".
  Trigger: "piano", "lotto", "PIANO-*", "RICERCA-*", "plans/", "INDEX",
  "CHANGELOG", "ADR", "chiudi/completa il piano", "merge della PR". Fa
  rispettare la regola d'oro del repo: ogni lotto chiuso aggiorna checklist
  del piano + plans/INDEX.md + plans/CHANGELOG.md nello STESSO commit.
---

# RumblingStone — Archivio Piani (disciplina di tracciatura)

Ogni lavoro strutturato del repo (revisioni, infrastruttura, ricerche) è
tracciato in **`plans/`**; senza, le modifiche restano sparse nelle PR e la
storia si frammenta.

## Quando no

- La qualità di un lotto che scrive contenuto di gioco la dà
  `rumblingstone-module-standard` (§ Lotto di contenuto, sotto).
- Il contenuto di campagna (`campaign/`, archi `00_`-`09_`, `Bestiario/`,
  `PG/`) non chiede changelog: le sessioni giocate ne sono esenti.

## Fonti

Le regole vengono da `plans/PIANO-DM-TOOLKIT-HYPE-E-ARCHIVIO-PIANI.md` (Lotto
K-A) e dall'header di `plans/INDEX.md`.

| Cosa | Dove |
|---|---|
| Piani di lavoro (con lotti/checklist) | `plans/PIANO-<NOME>.md` |
| Ricerche/valutazioni (input di futuri piani) | `plans/RICERCA-<NOME>.md` |
| Decisioni architetturali (il "perché") | `plans/adr/` |
| Vista d'insieme: stato, %, lotti rimanenti, gate | `plans/INDEX.md` |
| Storia: una riga per lotto chiuso | `plans/CHANGELOG.md` |
| Memoria storica: decisioni, misure, questioni aperte dietro le righe (ADR-0127) | `plans/MEMORIA-STORICA.md`, si cerca con `scripts/memoria_storica.py` |
| Classe prevista e usata di ogni lotto chiuso | [`plans/REGISTRO-LOTTI.md`](../../plans/REGISTRO-LOTTI.md) |

## Procedura

### 1 · 🔍 Regola di apertura (obbligatoria — ADR-0044)

**Prima di aprire un piano nuovo, si guardano quelli che ci sono**, nell'ordine:

1. **Leggi `plans/INDEX.md`**: l'unico posto che dice cosa esiste e a che punto
   è. Sono trentaquattro documenti: chi non guarda riscrive.
2. **Cerca per argomento, non per titolo**: `grep -ril "<parola chiave>" plans/*.md`.
3. **Guarda le PR aperte e chiuse**: un piano può esistere e non essere su
   `main` (storia in ADR-0044). `python3 scripts/contenuti_nei_rami.py --fetch`
   elenca i file di ogni ramo e PR mai arrivati su `main`, ognuno col suo posto
   in `plans/contenuti-nei-rami.json`; `fase1.py` mostra quelli aperti accanto
   al file che stai per toccare.
4. **Decidi, e scrivi quale delle tre è**:

| Se… | Allora |
|---|---|
| esiste un piano che copre l'argomento e il lavoro è **dentro il suo perimetro** | **espandi quel piano** con un lotto nuovo. Niente documento nuovo |
| esiste un piano **vicino** ma il tuo lavoro è un difetto suo | **fix nel piano esistente**, e una riga nel CHANGELOG |
| non esiste niente che copra l'argomento | **apri**, e nel documento nuovo scrivi **cosa hai guardato prima** e perché non bastava |

⚠️ **Il §1 di un piano nuovo dice sempre cosa NON rifà**: senza confini contro i
piani vicini si sovrappone entro un mese (storia in ADR-0044).

**PIANO o RICERCA?** Una **RICERCA** misura un divario e propone; un **PIANO**
esegue. Se non sai ancora cosa fare, è una ricerca, che può poi aprire un piano
citandosi.

### 2 · Il numero di un ADR si guarda, non si indovina

Prima di **creare** un ADR:

```bash
python3 scripts/validate_docs.py --prossimo-adr
```

Stampa l'ultimo numero sul disco e il primo libero, contandoli da `plans/adr/` e
non dall'indice. Il numero è l'**identità** dell'ADR (si cita in commit, piani,
codice, changelog): due decisioni con lo stesso numero rendono ambigua ogni
citazione **già scritta** (l'incidente è in ADR-0009). Per un **piano** nuovo
si legge `plans/INDEX.md` prima di aprirlo (ADR-0044): un duplicato divide il
lavoro in due posti che divergono. ⚠️ Il gate in CI
(`validate_docs --sorgenti`) prende la collisione **dopo** che il file esiste: questo comando è
la metà preventiva, e funziona solo se lo esegui.

### 3 · 🧭 Come si tagliano i lotti (obbligatoria — ADR-0045)

Ogni lotto **ancora da fare** dichiara in intestazione:

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

**La classe la decidono queste domande, nell'ordine** (la tabella illustra); la
prima che scatta assegna:

| | Domanda | Se sì |
|---|---|---|
| 1 | **Se sbaglio, se ne accorge il DM al tavolo?** | **K** — nessun gate difende il canone |
| 2 | Devo decidere qualcosa che **una macchina non può contare**? | **G** |
| 3 | Il risultato è definito da un **contratto verificabile**? | **C** se il contratto va scritto, **M** se esiste già |
| 4 | *(nessuna)* Sto solo **leggendo per riferire**? | **R** |

⚠️ **Nessuna chiede quanto è grande il lotto**: la dimensione non entra, ed è
dove l'istinto sbaglia (*«sostituisci Tordek con Thorik in dodici file»* sembra
un `sed` ed è la riscrittura di un eco).

1. **L'effort si abbassa prima dell'engine.** Un modello capace a effort basso
   spesso batte uno inferiore a effort alto, e **non spezza la cache**: le cache
   sono legate al modello, ogni salto di engine la butta.
2. **Un lotto sale di classe, mai scende.** Fra M e C scegli C; fra G e K, K.
   Sovradimensionato costa token; sottodimensionato costa un errore al tavolo.
3. **La colonna «qualità» non è una leva: è il collaudo.** Se non sai
   scriverla, il lotto è **tagliato male**: ritaglialo prima di eseguirlo.

**Si taglia sulla classe**, non sulla dimensione: un lotto che mescola classi si
divide (la parte **G** decide, la parte **M** esegue). ⚠️ **Non si
riclassificano i lotti già chiusi**. ⚠️ **`Haiku 4.5` non è un Opus più
piccolo**: 200K di contesto contro 1M, e **non accetta `effort`**; per lavoro
corto e meccanico, non «per risparmiare».

**A lotto chiuso, una riga in `plans/REGISTRO-LOTTI.md`**: classe prevista,
engine usato, **ha retto?** Così la tabella smette di essere tarata a occhio; se
il lotto è **salito di classe** a metà, la riga vale doppio.

### 4 · 🎭 Lotto di contenuto: segue il ciclo del master (ADR-0075)

Se un lotto **scrive, riscrive o rifinisce nello stile** un master, un modulo o
uno stand-alone, la sua «qualità» sono i sette passi del **ciclo completo** di
[`rumblingstone-module-standard`](../rumblingstone-module-standard/SKILL.md)
(scene riconoscibili, contratto «In scena», componenti, developer, box al metro,
lettore e playtester a freddo, quiz): il lotto li cita per numero e dice quali
salta, e perché. Vale per i piani nuovi e aperti; un lotto che tocca solo dati
(`state.md`, statblocchi, mappe) non ci rientra.

### 5 · Richieste complesse → piano con routing engine & impegno

Per OGNI richiesta comprensibilmente complessa (multi-fase, multi-file, più
sessioni, o canone+meccanica+prosa insieme) l'agente produce PRIMA un piano
(`plans/PIANO-<NOME>.md`, o inline se effimero) in cui **ogni fase dichiara**:

1. **Cosa** produce (deliverable + criterio di accettazione);
2. **Engine consigliato** e **livello di impegno**:

| Tipo di fase | Engine | Impegno |
|---|---|---|
| Find/replace, validazioni, rigenerazione cataloghi, lint | **Haiku** (o script deterministico: sempre preferito se esiste) | basso |
| Redazione standard: statblock, tabelle, mappe ASCII, handout | **Sonnet** | medio |
| Consolidamento narrativo, coerenza cross-arc, decisioni di design, audit | **Opus** | alto |
| Ricognizioni larghe del repo (molti file, serve solo la conclusione) | subagent **Explore** | medio |
| Prosa d'autore su scene cardine (solo su richiesta esplicita del DM) | **Fable/Mythos** | alto |

3. **Dieta di contesto**: all'engine SOLO i file del lotto (mai riletture
   dell'intero arco: regola anti-spreco dei piani ARC).

Non è un gate CI: giudicare complessità ed engine non è deterministico, e un
gate semantico sarebbe cattiva pratica. Il gate resta ADR-0009; la review
meccanica dei contenuti è `validate_modules.py` (token-free). È disciplina che
l'agente applica DA SOLO.

### 6 · 🔁 L'eco prima di applicare un blocco di decisioni (PIANO-AGENT-SKILLS-ESTERNE L9)

Quando il DM chiude **due o più decisioni in un messaggio solo** («D1 ok, d2 ok,
d4 ok ma dopo…»), prima di toccare i file si rimanda l'eco e la si scrive nel
piano accanto alla tabella (§ Formato d'uscita). L'ultima riga, «Dedotto da
me», è il motivo della norma: in un «ok» con un «ma» l'agente aggiunge del suo,
e se l'aggiunta non sta **a parte** il DM non può vederla né smentirla.
`python3 scripts/eco_decisioni.py --check`, in CI, legge le tabelle che
`decisioni_dm.py` già legge e boccia un piano con due o più decisioni chiuse
nella stessa data senza l'eco di quella data, o con un campo mancante. Le
chiusure di prima di `DATA_INIZIO` nello script (1 ottobre 2026) si contano
e non bloccano.

### 7 · ⚖️ Regola d'oro (obbligatoria, non opzionale)

**Chi chiude un lotto/piano/iniziativa aggiorna, NELLO STESSO COMMIT:**

1. la **checklist del piano** (o la nota "STATO ATTUAZIONE" di una ricerca);
2. la **riga del piano in `plans/INDEX.md`** (stato, %, lotti rimanenti, gate)
   e la sua sezione "Prossimi passaggi";
3. **una riga in `plans/CHANGELOG.md`** (§ Formato d'uscita) e, con essa,
   **una voce `MS-NNNN` in coda a `plans/MEMORIA-STORICA.md`** (addendum,
   ADR-0127): le decisioni, le misure, le questioni aperte e i rimandi che la
   riga non tiene. Modello nel file; `python3 scripts/memoria_storica.py --check`;
4. se il lotto **chiude o apre una decisione del DM**: la riga nella tabella
   marcata `<!-- decisioni-dm: … -->` **dentro il piano**, poi
   `python3 scripts/decisioni_dm.py --emit` per rigenerare l'aggregato di
   `STATO-E-ORDINE` §4 (ADR-0047). Chiusa = identificatore **barrato**:
   `~~D1~~`. Si tocca il piano, mai l'aggregato.

## 🤖 Enforcement automatico (ADR-0009)

`scripts/check_plans_discipline.py` gira in CI su ogni PR e come hook
`pre-push` locale (`./scripts/install-git-hooks.sh`):

- **Blocca** (rosso in CI, push rifiutato) modifiche a file strutturali
  (`scripts/`, `skills/`, `converters/`, `.github/`, `plans/adr/`) senza una
  riga in `plans/CHANGELOG.md` nello stesso range di commit.
- **Blocca** una PR che aggiunge righe a `plans/CHANGELOG.md` senza almeno
  una voce nuova in `plans/MEMORIA-STORICA.md` (addendum, ADR-0127).
- **Blocca** l'aggregato di `STATO-E-ORDINE` §4 che non combacia con le tabelle
  dei piani (`scripts/decisioni_dm.py --check`, ADR-0047; l'incidente che l'ha
  fatto nascere è nell'ADR). ⚠️ `D<n>` **non è globale**: otto piani hanno il
  loro `D1..Dn` con significati diversi, quindi conta solo ciò che porta il
  marker, e l'identità è `piano#Dn`.
- **Promemoria ADR** (warning non bloccante): nuova skill, nuovo script
  top-level o modifica ai workflow CI senza tocchi a `plans/adr/` → invito a
  valutare un ADR. Non bloccante di proposito: «serve un ADR?» resta una
  decisione umana.
- Il contenuto di campagna è esente (§ Quando no).
- Bypass locale consapevole: `git push --no-verify` (la CI resta il gate
  finale).

Una PR già mergiata senza tracciatura (caso in ADR-0009) si recupera subito
con un commit dedicato `docs(plans): tracciatura PR #N`: mai buchi nella storia.

## Formato d'uscita

- Riga di `plans/CHANGELOG.md`:
  `| data | piano | lotto | riferimento (PR #N / commit) | esito |`.
- Intestazione di un lotto da fare: `[engine: … · effort: … · qualità: …]`.
- L'eco di un blocco di decisioni:

```
<!-- eco: <ETICHETTA> <AAAA-MM-GG> -->
- **Decise**: cosa, in una riga per decisione
- **Aperte**: cosa resta, comprese quelle nate dal messaggio
- **Cambiate**: dove la decisione si è spostata dalla proposta
- **Dedotto da me**: quello che il DM non ha scritto e io ho letto fra le righe
```

- Le voci di INDEX/CHANGELOG citano **fatti verificabili** (PR, commit, file),
  mai intenzioni. Gli esiti parziali si dichiarano (🟡 + cosa manca + gate), non
  si arrotondano a ✅.
- I "Prossimi passaggi" di INDEX restano ⬜ finché tavolo/DM non decide: il
  vuoto dichiarato è informazione, quello implicito no.

## Prima di consegnare

Prima di aprire (o dichiarare pronta) una PR che completa lavoro pianificato:

- [ ] Il documento del lavoro esiste in `plans/` (PIANO o RICERCA)? Un lavoro
      nato "spontaneo" da una richiesta prende almeno la voce di tracciatura
      (non serve un piano formale per tutto: serve la riga).
- [ ] `plans/INDEX.md`: riga di stato + "Prossimi passaggi" (anche solo ⬜
      opzionali/gated).
- [ ] `plans/CHANGELOG.md`: riga con riferimento alla PR, e la voce
      `MS-NNNN` in `plans/MEMORIA-STORICA.md` (addendum, ADR-0127).
- [ ] Tooling/script nuovi: `scripts/README-automation.md` (tool map)
      aggiornato.
- [ ] Skill nuova o toccata: `./scripts/build-skills.sh --no-deploy` e
      `python3 scripts/validate_skills.py` verdi.
- [ ] Nuova convenzione o scelta strutturale? → ADR in `plans/adr/`.
- [ ] La PR si chiude **senza merge**, o sul ramo restano commit dopo il merge?
      I file che non arrivano su `main` prendono una riga in
      `plans/contenuti-nei-rami.json`, con stato e responsabile
      (`contenuti_nei_rami.py --check` verde; storia in
      `plans/PIANO-RIPRESA-PR-ABBANDONATE.md`).

## Cancelli deterministici

I controlli che non chiedono un giudizio, da far girare prima di consegnare.
Quello che qui non c'è resta giudizio di chi legge (registro delle norme).

- `python3 scripts/check_plans_discipline.py`: intestazioni dei piani, INDEX e CHANGELOG.
