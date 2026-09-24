# ADR-0056 — Una norma senza misura non esiste, e introdurla non è averla applicata

- **Stato**: accettata (2026-09-18), **attuata** (`validate_norme_editoriali.py`,
  `skills/REGISTRO-NORME-EDITORIALI.md`, regola d'oro in `AGENTS.md`)
- **Decisore**: DM — *«crea una golden rule che obbliga a leggere davvero tutta
  la parte editoriale per la prosa, lo stile, e le mod specifiche del repo, le
  skill, le metriche, altrimenti questo problema si ripresenterà come fatto
  prima»*
- **Rapporti**: nasce dall'addendum di
  [ADR-0055](ADR-0055-il-mestiere-si-misura-per-congegni.md) · applica
  [ADR-0053](ADR-0053-la-chiave-verso-il-bestiario-si-dichiara.md) al registro
  stesso · dà finalmente un presidio ad
  [ADR-0014](ADR-0014-regia-sensoriale-obbligatoria.md)

---

## Contesto: due norme ottime, ferme per settimane

| Norma | Introdotta | Applicata a |
|---|---|---|
| `references/read-aloud-adulti.md` — box ≤ 12 righe, **un solo nome proprio nuovo**, niente parentesi, «l'ultima cosa detta è quella che resta» (171 righe) | commit `10795aa`, PR #89 | 🔴 **nessun file d'arco**: il commit tocca 7 file, tutti skill, piani e glossario |
| `ADR-0014` — *regia sensoriale obbligatoria*: nessuna sequenza a battute senza regia, occhio da avventuriero, **chiusura su «Che fate?»** | commit `d9c357b` | 🔴 **ARC07-DEF-1 e basta** (309 righe) |

Misurato il 2026-09-18 su 100 file: la **regia di round** esiste solo in DEF-1;
la **chiusura su «Che fate?»**, dovuta a *ogni* box di combattimento, esiste
**una volta in tutto il repo**; la forma di dialogo prescritta, **sei volte**.

E un agente — io — ha costruito un metro dello stile senza aprire un solo
`references/`, concludendo che alcune di quelle norme «non esistevano».

## Le due diagnosi sbagliate, prima di quella giusta

1. ❌ **«È un problema di scopribilità: le reference sono nascoste.»** Misurato:
   **tutti e 56** i file `references/` del repo sono già citati dal loro
   `SKILL.md`. Un gate sulla citazione sarebbe **verde e inutile**.
2. ❌ **«È un problema di disciplina: basta scriverlo in AGENTS.md.»** È già
   pieno di regole scritte bene. `read-aloud-adulti.md` *è* una regola scritta
   bene, ed è stata ignorata per tre settimane senza che nulla diventasse rosso.

✅ **La diagnosi vera**: **una norma che nessuno misura non fa rumore quando
viene ignorata.** Non c'è il momento in cui qualcuno se ne accorge. Il testo
sta lì, verde, e la violazione è indistinguibile dal rispetto.

## Decisione

**Ogni norma editoriale deve avere un nome, un posto e uno stato di misura.**
Tre pezzi, e il terzo è l'unico che non si può aggirare:

1. **La regola d'oro** (`AGENTS.md` §Skills): prima di scrivere prosa di gioco,
   o di misurarla, o di dire che uno standard manca, si aprono i `references/`
   e **si leggono**. Il `SKILL.md` è l'indice, non la norma.
2. **Il registro** (`skills/REGISTRO-NORME-EDITORIALI.md`): ogni file normativo,
   ogni norma verificabile che contiene, e **chi la misura** — oppure **perché
   nessuno la misura**.
3. **Il cancello** (`scripts/validate_norme_editoriali.py`), che boccia:
   - un file normativo **non registrato** (è così che una norma torna a
     nascondersi);
   - un rimando a un congegno o a uno script **che non esiste** — ADR-0053
     applicato al registro stesso: un rimando inventato è **peggio** di un buco
     dichiarato, perché sembra copertura;
   - un 🔴 **senza la ragione scritta**: «non misurato» nudo non è una
     decisione, è una dimenticanza con un'icona.

### Il corollario, che è metà del valore

> **Introdurre uno standard non è aver fatto il lavoro.** Una norma nuova
> arriva con il suo **lotto di applicazione** e la sua **misura**, o non è
> arrivata.

## Conseguenze

**Buone.**
- Il conto è pubblico: **35 norme registrate**, di cui **11 🔴 non misurate**,
  ognuna con il perché. Prima quel numero non esisteva e sembrava zero.
- Nove delle undici hanno **la stessa causa**, che il registro rende visibile:
  la norma presuppone un dato che il testo non porta (i nodi d'indagine non
  sono marcati, gli archi non dichiarano la tinta, le scene di spotlight non
  sono marcate). Non è un buco di codice: è un **prerequisito di dato**.

**Costi, dichiarati.**
- ⚠️ **Il registro è scritto a mano e mente come tutto ciò che è scritto a
  mano.** Lo si è visto al primo giro: avevo registrato il tetto dei gradi di
  ADR-0022 come presidiato da `validate_pg.py`, **che non esiste**. Il cancello
  l'ha trovato subito — ed è per questo che i rimandi si verificano contro il
  filesystem invece di essere creduti.
- ⚠️ **Il cancello non controlla che le norme siano rispettate**, solo che
  qualcuno le guardi. È una distinzione che va ripetuta o il verde illude.
- ⚠️ Una riga 🔴 può nominare uno strumento inesistente **apposta** (per dire
  che non esiste): il controllo dei rimandi gira **solo** sulle righe che
  affermano una misura. Un cancello più zelante impedirebbe di scrivere il vero.

## Alternative scartate

1. **Gate sulla citazione dei `references/` nel `SKILL.md`.** Scartata perché
   **già verde**: 56 su 56. Avrebbe dato l'illusione di un presidio.
2. **Rendere bloccanti subito tutte le soglie numeriche.** Scartata: accendere
   il lint su 96 file mai controllati produce centinaia di rilievi in un colpo.
   Il `PIANO-PORTARE-IL-MESTIERE-DEI-BANCHI` lo fa in due tempi (S0a misura,
   S0b blocca), che è come il repo ha già gestito `validate_docs --sorgenti`.
3. **Un LLM che legge le reference e giudica la conformità.** Scartata per
   ADR-0012 (tool verificabili, zero token nei gate) e per il precedente dei
   64/64 falsi positivi: un giudizio non riproducibile non è un cancello.
