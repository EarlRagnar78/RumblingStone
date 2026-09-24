# ADR-0024 — La diciassettesima skill: `rumblingstone-edizione`

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: lotto **E** di
[`PIANO-CHIUSURA-CATENA-EDITORIALE`](../PIANO-CHIUSURA-CATENA-EDITORIALE.md),
autorizzato dal DM il 2026-09-02. Il divario è **C1+C3** della
[ricerca sul colophon](../RICERCA-RUOLI-EDITORIALI-COLOPHON-PAIZO-2026-08.md).

## Contesto

[ADR-0008](ADR-0008-governance-set-skill-focalizzate.md) avvisa esplicitamente sul
costo della frammentazione, e le skill sono sedici. Una diciassettesima va
**motivata**, non aggiunta per simmetria. La motivazione qui non è «manca un
argomento»: è che **una regola scritta che nessun agente carica non è una regola**.

Il fatto misurato: `docs/guides/GUIDA-CONDIVISIONE-IP.md` ha al §7 una *«checklist
prima di far uscire qualcosa dal repo»* — cioè il gate d'uscita, scritto e
completo. `grep -rl "GUIDA-CONDIVISIONE-IP" skills/` restituiva **un solo file**,
e per un'altra ragione (l'art direction, sulle immagini). Un agente che genera un
handout e lo consegna **non incontrava mai quella checklist**.

Lo stesso vale per il resto del mestiere dell'editore: il colophon (ora
esiste come meccanismo, [ADR-0023](ADR-0023-colophon-di-edizione.md), ma nessuna
skill diceva *quando* si compila), le dichiarazioni Product Identity / Open
Content, e il concetto di **edizione** — versione, ristampa, errata — che nel repo
non esisteva affatto.

La verifica IP sull'arco del Palio (`…-VERIFICA-LEGALE-IP.md`, PR #47) dimostra
che il mestiere il repo lo sa fare. L'ha fatto **una volta, a mano, su un arco**:
è un episodio, non un ruolo.

## Decisione

**Nasce `skills/rumblingstone-edizione/`: il mestiere di chi risponde di cosa
esce dal repo — colophon, dichiarazioni, gate d'uscita, versione ed errata.**

### Perché una skill e non un ADR o una guida

Un ADR registra una decisione; una guida la spiega a un umano. Nessuno dei due
viene **caricato al momento giusto** da un agente. La regola 2 di ADR-0008 dice
che «quando un piano introduce un flusso che un agente dovrà usare, la skill che
lo copre nasce o si aggiorna nello stesso piano». Il flusso «sto per far uscire
qualcosa» esiste da sempre e non aveva copertura.

### Confini, perché le sedici esistenti non si sovrappongano

| Se la domanda è… | La skill è |
|---|---|
| come sta sulla pagina (tabella, riquadro, capolettera, tema) | `rumblingstone-editoria` |
| che faccia hanno le immagini | `rumblingstone-art-direction` |
| come si scrive la prosa | `rumblingstone-narrative-style` |
| quanto è profondo un modulo | `rumblingstone-module-standard` |
| **se questo può uscire, con che crediti, che licenza e che versione** | **`rumblingstone-edizione`** |

### Cosa NON entra nella skill nuova

- Le passate redazionali sul testo: restano in `narrative-style`, dove sta già la
  norma (`editorial-standards.md`). Separarle sarebbe la frammentazione che
  ADR-0008 teme.
- Le decisioni di licenza del repo (ADR-0005) e la lingua (ADR-0016): la skill le
  **applica**, non le rifà.

## Conseguenze

- **Più facile**: il gate IP viene incontrato *prima* di consegnare, non dopo.
  Il colophon ha un posto dove è scritto quando si compila e con che valori.
- **Più difficile**: diciassette skill sono diciassette voci di manutenzione.
  Accettato, con la regola di ADR-0008: se un giorno questa si svuota perché il
  contenuto è migrato altrove, si chiude.
- **Da rivisitare**: quando esisterà la prima **ristampa** vera. Allora `versione`
  smetterà di essere una stringa libera e la sezione sull'errata diventerà un
  meccanismo, non una convenzione.
