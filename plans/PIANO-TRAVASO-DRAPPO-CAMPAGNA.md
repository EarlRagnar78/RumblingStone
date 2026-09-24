# PIANO — Travaso fra il Drappo e la campagna (nei due sensi)

> **Cos'è.** Il `Drappo di Tarsilia` è nato come modulo autoconclusivo e ha finito
> per essere il **banco di prova** del repo: l'apparato d'uso, la catena di stampa,
> i fregi, il kit anti-improvvisazione, il dossier delle piste sono nati lì. La
> campagna — che è il prodotto principale — non ne ha ereditato quasi niente. E in
> un punto il debito è al contrario.
>
> Questo piano porta **ciò che il Drappo fa meglio dentro la campagna**, e **ciò che
> la campagna fa meglio dentro il Drappo**, senza riscrivere nessuno dei due.
>
> **Decisione-fonte**: domanda del DM del 2026-08-31 — *«ci sono stati miglioramenti
> rispetto all'Arco della Forgia Eterna? e quali si potrebbero portare nella
> campagna?»* — e la verifica dei file che ne è seguita (§1).

**Stato**: 🔵 pianificato · **Data**: 2026-08-31
**Ambito**: apparato, tooling e formati. **Mai** la prosa giocata.

---

## §0 · Il criterio, prima dei lotti

Tre regole che valgono per ogni lotto e che sono il senso di *«senza stravolgere»*:

1. **Si travasa l'apparato e il formato, mai la voce.** Il Drappo è una città in tre
   giorni, la campagna è un'epica in nove archi: le due prose non si toccano. Passano
   gli **attrezzi** (un indice, una tabella, un formato di audit) e non lo stile.
2. **Il testo già giocato non si riscrive.** ARC-07 è al tavolo *adesso*
   (`campaign/state.md`: «Arco 07 in corso»). Ogni lotto **aggiunge un file** o tocca
   un manifest; nessuno riapre un master per rimaneggiarlo. Vale la stessa regola che
   protegge il testo collaudato del Drappo.
3. **Ogni lotto ha un gate a macchina** già esistente. Se un lotto non è verificabile
   da un validatore che c'è già, va ripensato: un lavoro che nessuno può controllare
   fra sei mesi è un lavoro che marcisce.

⚠️ **Debito già dichiarato altrove, e non riaperto qui**: ADR-0018 stabilisce che i
cinque master `ARC*-DEF-*` esistenti **non si riscrivono retroattivamente**. Questo
piano lo rispetta: l'apparato di ARC-07 nasce come **file nuovo accanto** ai master,
non dentro di essi.

---

## §1 · La fotografia — cosa c'è davvero, verificato il 2026-08-31

| Elemento | Drappo | ARC-07 | Come l'ho verificato |
|---|---|---|---|
| Apparato d'uso (ADR-0018, 9 voci) | **9/9** | **1/9** — solo l'inserto per lo schermo, come quick-reference per master | `grep` delle sei voci sui 5 master: gli unici riscontri sono «pronuncia» come verbo nella finzione |
| Indice dei read-aloud | c'è | **no**, e i blocchi sono **260** (130 · 39 · 30 · 43 · 18) | conteggio `^>\s*\*` per master |
| Cue sonori | c'è | **no** su ARC-07; ARC-08 ne ha uno che **dichiara da sé** il debito sulle altre otto voci | `ARC08-16-CUE-SONORI.md` |
| Derivate immagini + provenienza | `web/` a 1400 px + `PROVENIENZA.txt` | **8+ master WebP**, nessuna derivata, **nessuna provenienza in tutto il repo fuori dal modulo** | `find` su `PROVENIENZA.txt` e sulla cartella `Immagini/` |
| Fregi di capitolo | 19, montati | i **10 della campagna esistono** e **nessun file li referenzia** | `docs/assets/fregi/` + `grep -rl "fregi"` su archi e `campaign/` = zero |
| Kit anti-improvvisazione | c'è | nessun equivalente | — |
| Dossier delle piste (indagine) | c'è | nessun equivalente | — |
| Apparato di collaudo (alfa/beta) | c'è | nessuno | `find -iname "*PLAYTEST*"` |
| Edizione da stampa Typst | sì | **sì — già portata** | `validate_booklets --stampa`: 11 manifest, 4 della campagna |
| Regia round per round degli scontri | **sì** (`02-GIORNO-2` §6, Sfregio) | sì | ⚠️ *correzione*: nella prima risposta al DM avevo detto che al Drappo mancava. Non manca |
| **Analisi di bilanciamento (DPR)** | **no** | **sì**, formato riusabile: danno medio/round per PG, round previsti, letalità per bersaglio | `ARC07-DEF-1` §8, «Analisi DPR» |
| **Audit ricchezza / WBL** | **no** | **sì**, con la regola «ricchezza d'uscita = ingresso dell'arco dopo» | `ARC07-TESORO-WBL-AUDIT.md` |

---

## §2 · Direzione A — dal Drappo alla campagna

### A1 · La cassetta del DM per ARC-07 `✅ 2026-08-31`

**Produce**: `07_il Portale Della Forgia Eterna/ARC07-CASSETTA-DEL-DM.md`, un file
solo, consultabile al tavolo, che copre le voci ADR-0018 che mancano:

1. **foglio del cast**: ogni PNG con nome proprio dei cinque master in una riga,
   ruolo, cosa vuole, **il tic vocale**, in quale master compare;
2. **guida alla pronuncia** dei nomi non ovvi (Terros, Dauth, Rethmar, i nomi nanici);
3. **indice dei 260 read-aloud** in ordine di gioco: master · § · prima riga · lunghezza;
4. **cue sonori** sul modello di `ARC08-16-CUE-SONORI.md`: descrizioni, mai titoli;
5. **il momento da fotografare**, uno per master;
6. **nota di accessibilità**.

**Criterio di accettazione**: un DM che non ha scritto l'arco trova un PNG in meno di
trenta secondi; ogni read-aloud dell'arco compare nell'indice con il suo rimando;
`validate_modules.py` verde.
**File toccati**: **solo il file nuovo** + una riga nell'indice `ARC07-00-INDICE.md`.
**Engine**: Opus, impegno **alto** (tocca canone e cinque master).
**Dieta di contesto**: un master alla volta, mai i cinque insieme.
**Anti-stravolgimento**: nessuna riga dei master viene modificata. Se durante la
lettura emergono incoerenze, **si annotano**, non si correggono qui.
**Stima**: mezza giornata. **Priorità: 1**, perché è l'arco che il tavolo sta giocando.

### A2 · I dieci fregi montati nei booklet della campagna `✅ 2026-08-31`

**Produce**: i quattro manifest della campagna (`PALIO-BOOKLET`, i tre di ARC-07)
referenziano il proprio medaglione d'arco come `cover_image`; se il fregio manca per
un arco, lo genera `scripts/build_chapter_marks.py`.
**Criterio**: `validate_booklets.py --stampa` verde e il medaglione visibile nel PDF.
**File toccati**: 4 manifest JSON. Nessun contenuto.
**Engine**: script + Haiku, impegno **basso**.
**Stima**: ~30 minuti. **Priorità: 2**, il rapporto resa/costo più alto del piano.

### A3 · Derivate e provenienza per le immagini di ARC-07 `✅ 2026-08-31`

**Produce**: `07_.../Immagini/web/` con le derivate da impaginazione, e
`07_.../Immagini/PROVENIENZA.txt` con una riga per file.
⚠️ **Incognita tecnica dichiarata**: i master di ARC-07 sono **WebP**, mentre
`build_image_derivatives.py` è scritto per i PNG. Il lotto **comincia verificando**
se il tool li accetta; se non li accetta, l'estensione è di poche righe **con un test**
(ADR-0012), non un rattoppo.
⚠️ **E una cosa che non si può inventare**: di quelle immagini non si conosce né il
modello né il seme. `PROVENIENZA.txt` registra **quello che è vero**: formato, data,
origine `DA CONFERMARE`, esattamente come si è fatto per i raster di Gemini
(ADR-0019 §2-bis). Meglio una riga onesta che una inventata.
**Criterio**: le derivate esistono, i booklet della campagna non aumentano di peso, i
gate restano verdi.
**Engine**: script + Sonnet, impegno **basso-medio**.
**Stima**: ~1 ora. **Priorità: 3**.

### A4 · Il kit anti-improvvisazione della Valle `✅ 2026-08-31`

**Produce**: `campaign/KIT-ANTI-IMPROVVISAZIONE-VALLE.md`, sul modello di
`09-KIT-ANTI-IMPROVVISAZIONE.md` ma **tarato sulla campagna**: 1d20 nomi della Valle
di Cannath (umani, nani, mezzelfi separati, perché mescolarli suona falso), prezzi
di bottega 3.5 per un party di 13° (cioè: **cosa non si trova** più che cosa si
trova), tre PNG jolly con statblocco al livello giusto, 1d6 «la Valle respira» in cui
nessuna voce è un gancio.
**Criterio**: ogni nome è compatibile con `campaign/GLOSSARIO-E-LOCALIZZAZIONE.md`;
nessuna voce contraddice `state.md`; nessun PNG jolly ha un'agenda (se ce l'ha, non è
un jolly: è canone, e va da un'altra parte).
**Engine**: Sonnet, impegno **medio**. **Dieta**: glossario + `state.md` §PNG, basta.
**Anti-stravolgimento**: il kit **non è canone**. Lo dichiara in testa: quello che il
tavolo trasforma in trama diventa canone *dopo*, via `state.md`.
**Stima**: ~2 ore. **Priorità: 4**, perché vale per tutti gli archi e non per uno.

### A5 · I prop fisici degli handout di ARC-07 `✅ 2026-08-31`

**Produce**: i documenti che la fiction consegna in ARC-07 (`ARC07-HANDOUTS.md`)
diventano **prop stampabili** con i template di `campaign/templates/homebrew/`, che
esistono da mesi e fuori dal Drappo non sono mai stati usati (ADR-0018 «regola dei
prop»). Ognuno con la **nota per il DM che non si stampa** in coda.
**Criterio**: ogni handout citato nei master ha il suo file; `validate_booklets.py`
verde sui manifest che li includono.
**Engine**: Sonnet, impegno **medio**. **Stima**: ~2 ore. **Priorità: 5**.

### A6 · Il dossier delle piste per ARC-09 `⬜ gated`

**Produce**: l'equivalente di `10-DOSSIER-DELLE-PISTE.md` per i misteri che ARC-09 ha
già: la torre invisibile, le due lettere che provano i traffici Sonjak↔Collezionista,
il «dottore», con nodi a tre strati, sei porte e orologio degli indizi
(`rumblingstone-indagine`).
**Gate**: **dopo** che ARC-07 finisce al tavolo. Scrivere le piste di un arco non
ancora giocato mentre il precedente è aperto è lavoro che invecchia.
**Engine**: Opus, impegno **alto**. **Stima**: mezza giornata. **Priorità: 6**.

---

## §3 · Direzione B — dalla campagna al Drappo

Più stretta di quanto sembrasse a occhio, perché il Drappo ha già la regia round per
round e le contingenze. Restano due cose vere.

### B1 · L'analisi di bilanciamento dei tre scontri `✅ 2026-08-31`

**Produce**: in `06-VILLAIN-E-AGENDE.md` un **§7-bis** che applica il formato DPR di
ARC-07 ai tre momenti duri del modulo: la rissa alla fontana, l'assalto alle stalle,
la curva nord: danno medio per round delle sei pregenerate, round previsti per
chiudere, e **chi rischia davvero di cadere**.
**Criterio**: **nessun numero nuovo**, tutti derivati dagli statblocchi e dalle
schede già scritte; la conclusione dichiara se lo scontro dura 3 round o 8, perché è
la cosa che il DM vuole sapere prima di sedersi.
**Engine**: Sonnet, impegno **medio** (è aritmetica su dati esistenti).
**Dieta**: `STATBLOCCHI-PF1E.md` + `PREGEN-SEI-SCHEDE-PF1E.md` + `06-VILLAIN` §7.
**Stima**: ~2 ore. **Priorità: 7**.

### B2 · L'audit della ricchezza del Drappo `✅ 2026-08-31`

**Produce**: un `§7-ter` (o un file breve) con l'audit in stile
`ARC07-TESORO-WBL-AUDIT.md`: quanto entra in mano al gruppo nei tre giorni (il Peso da
140 mo, la cassa da 220 mo dell'oratorio, i premi), quanto ne esce, e **con quanto un
gruppo esce dal modulo** se poi continua a giocare quei personaggi.
**Criterio**: i numeri tornano con quelli già scritti nel modulo; i valori non
attestati sono marcati `[INFERRED]`.
**Engine**: Sonnet, impegno **medio**. **Stima**: ~1 ora. **Priorità: 8**.

---

## §4 · Ordine di esecuzione, e perché questo

```
A2 fregi ──► A3 immagini ──► A1 cassetta ARC-07 ──► A4 kit Valle ──► A5 prop
   (30')        (1 h)            (mezza giornata)       (2 h)         (2 h)

                          B1 bilanciamento ──► B2 ricchezza
                               (2 h)              (1 h)

A6 dossier ARC-09  ⟵ gated: dopo che ARC-07 finisce al tavolo
```

Il criterio dell'ordine è uno solo: **prima ciò che serve alla serata che il tavolo
giocherà davvero** (ARC-07), poi ciò che vale per tutti gli archi, infine ciò che
riguarda un arco non ancora aperto. I due lotti B stanno in mezzo perché sono
indipendenti da tutto e si possono fare mentre A1 è in corso.

**Dipendenze reali**: solo A3 → A1 (la cassetta cita le immagini se ci sono).
Tutto il resto è parallelizzabile.

---

## §5 · Cosa NON si travasa, e perché — dichiarato

| Non si porta | Dove starebbe | Perché no |
|---|---|---|
| `STATO-DEL-MODULO.md` | campagna | lo fa meglio `state.md` + ADR-0007. ADR-0018 §9 lo esclude esplicitamente: **non si duplica la memoria** |
| Le schede pregenerate | campagna | i PG sono veri e vivi da nove archi |
| Il fascicolo giocatori | campagna | i recap per-PG di `dm.py` fanno già quel lavoro, meglio |
| La riscrittura dei read-aloud al metro nuovo | ARC-07/08 | **non autorizzata** (già a INDEX per ARC-08). Indicizzarli sì, riscriverli no |
| Il quick-reference d'incontro | Drappo | ce l'ha già, in forma di quickstart di serata + inserto per lo schermo |
| La regia round per round | Drappo | ce l'ha già (`02-GIORNO-2` §6) |

---

## §6 · Gate e tracciatura

| Lotto | Gate a macchina |
|---|---|
| A1 | `validate_modules.py` · `check_plans_discipline.py` |
| A2 | `validate_booklets.py --stampa` (compila davvero, con typst) |
| A3 | `validate_booklets.py` · i test di `build_image_derivatives` se il tool va esteso |
| A4 | `validate_modules.py` (termini vietati, igiene) |
| A5 | `validate_booklets.py` |
| A6 | `validate_modules.py` · rilettura con `rumblingstone-indagine` |
| B1, B2 | `validate_standalone.py` |

**Tracciatura** (regola d'oro, ADR-0009): ogni lotto chiuso aggiorna **nello stesso
commit** la checklist qui sotto, la riga di questo piano in `plans/INDEX.md` e una
riga in `plans/CHANGELOG.md`.

---

## §7 · I rischi, e cosa li tiene a bada

1. **Che il travaso diventi una riscrittura.** È il rischio grosso, ed è il motivo del
   §0.2: ogni lotto aggiunge file, non rimaneggia master. Se un lotto si trova a voler
   cambiare una riga di testo giocato, **si ferma e lo chiede**.
2. **Che l'apparato invecchi rispetto al contenuto.** Un indice dei read-aloud è vero
   il giorno che lo scrivi. Mitigazione: l'indice cita **file e §**, non i numeri di
   riga, che cambiano a ogni modifica.
3. **Che il kit della Valle diventi canone per sbaglio.** Mitigazione: lo dichiara in
   testa, e i tre PNG jolly non hanno agenda.
4. **Che si faccia tutto e non si giochi niente.** Il piano è ordinato per **utilità
   alla prossima serata**, non per completezza. A6 è dichiaratamente gated.

---

## §8 · Checklist di stato

- ✅ **A1**: cassetta del DM per ARC-07 *(`ARC07-CASSETTA-DEL-DM.md`: 12 PNG col tic, 9 pronunce con le due collisioni Thorek/Thorik e Durik/Durin, indice dei 260 read-aloud per § con il comando che lo rigenera, 12 cue sonori, 5 momenti da fotografare, accessibilità; §7 dichiara che i prop restano scoperti = lotto A5)*
- ✅ **A2**: i dieci fregi montati nei manifest della campagna *(chiave `fregio` nel manifest: nel modulo il medaglione si trova dal nome del capitolo, nella campagna è dell'arco)*
- ✅ **A3**: derivate e provenienza per le immagini di ARC-07 *(booklet di Terros: 11,7 MB → 1,7 MB; cinque coppie di duplicati trovate e dichiarate, non cancellate)*
- ✅ **A4**: kit anti-improvvisazione della Valle *(`campaign/KIT-ANTI-IMPROVVISAZIONE-VALLE.md`: 3×1d20 nomi separati per popolo, i prezzi che dicono **cosa non si trova** a 13°, tre jolly senza agenda, 1d6 «la Valle respira»)*
- ✅ **A5**: prop fisici per gli handout di ARC-07 *(tre prop nuovi + il difetto trovato: la nota anti-spoiler finiva stampata nella carta dei giocatori)*
- ⬜ **A6**: dossier delle piste per ARC-09 *(gated: ARC-07 finito al tavolo)*
- ✅ **B1**: analisi di bilanciamento dei tre scontri del Drappo *(`06-VILLAIN` §7-bis: ~17-18 danni/round di gruppo, l'assalto dura 5-6 round, e Tesio cade in due colpi di Sfregio)*
- ✅ **B2**: audit della ricchezza del Drappo *(`06-VILLAIN` §7-ter: si esce con quasi gli stessi soldi con cui si entra, ed è il punto del modulo)*

---

## Materiale collegato

- [ADR-0018](adr/ADR-0018-apparato-uso-obbligatorio.md): l'apparato d'uso è parte del contenuto (e il debito dei cinque master)
- [ADR-0019](adr/ADR-0019-licenza-dei-pesi-non-del-software.md) §2-bis: provenienza quando il seme non c'è
- [ADR-0020](adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md): la catena di stampa, già condivisa
- `skills/rumblingstone-indagine`: il vocabolario per A6
- `skills/rumblingstone-playtest`: cosa misura se l'apparato funziona (ADR-0018: due tavoli veri)
- `STANDALONE-Il-Drappo-di-Tarsilia/08-CASSETTA-DEL-DM.md`: il modello di A1
- `08_La Battaglia Di Hammerfist/ARC08-16-CUE-SONORI.md`: il modello dei suoni, e l'esempio di come si dichiara il debito
