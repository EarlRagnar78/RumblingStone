# ADR-0063 — I comandi che un elenco cita si eseguono, non si credono

- **Stato**: 🟢 accettata
- **Data**: 2026-09-21
- **Contesto**: ordine del DM — *«fai un cancello che esegua in CI i comandi citati da §6.2»*
- **Estende**: [ADR-0047](ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md) e [ADR-0062](ADR-0062-una-norma-senza-superficie-lo-dichiara.md)

---

## Contesto

`STATO-E-ORDINE-DEI-PIANI` §6 nasce con un principio dichiarato:

> *«ogni cosa da fare ha un comando che la rimisura, perché un elenco che
> dipende dalla memoria di una chat non è un elenco, è un ricordo»*

Il principio è giusto. Il 2026-09-21 si è scoperto che non basta.

La riga *«i 27 ADR mancanti in `docs/INDEX.md` §4»* citava
`validate_docs --sorgenti` — e quel comando, **in quel momento**, stampava
zero, girava in CI ed era verde. I 27 non erano invecchiati: non erano **mai**
stati misurati. La riga gemella parlava di «51 link rotti nei booklet», chiusi
nove giorni prima dal lotto E1 e registrati a zero **nello stesso archivio**.

Scrivere il comando accanto alla riga non è eseguirlo.

## Decisione

**Un elenco di lavoro che cita comandi li fa eseguire in CI, e una riga che il
comando smentisce è rossa.** Lo strumento è `scripts/verifica_sezione6.py`.

### I comandi sono di due specie, e vanno trattate diversamente

| specie | come si riconosce | cosa vuol dire una riga ⬜ |
|---|---|---|
| **cancello** | stampa un verdetto `✓` / `✗` | se stampa `✓` **senza avvisi**, la riga mente |
| **misura** | stampa numeri, nessun verdetto | la riga deve dichiarare il numero atteso in `<!-- attesa: … -->`, e il gate lo cerca nell'output |

⚠️ **Un `⚠` non conta come pulito**, e la distinzione è costata un falso
positivo al primo giro. `validate_modules --tetto-el` stampa
*«✓ nessuno sforamento»* **e** *«⚠ ZERO incontri marcati»*: è verde **a
vuoto**, perché nessun incontro può sforare se nessuno è dichiarato. È il
`SUPERFICIE_VUOTA` di ADR-0062, e la riga ⬜ accanto **dice il vero**.

### Eseguire testo scritto a mano: i tre presidi

🔴 Questo strumento esegue comandi che stanno in un file Markdown. È la ragione
per cui la decisione è stata **proposta al DM e non presa da sola**.

1. **Forma rigida** — si riconosce solo `python3 scripts/<nome>.py [--flag …]`.
   Niente pipe, redirezioni, `;`, `&&`, sostituzioni di comando: un carattere
   fuori dall'alfabeto ammesso e la riga è **rifiutata**, non eseguita.
2. **Allowlist di file** — `<nome>.py` deve stare in `CONSENTITI`. Aggiungerne
   uno è una decisione umana, non la conseguenza di aver scritto un backtick.
3. **Niente shell** — `subprocess.run` con una lista di argomenti,
   `shell=False`, timeout per comando, `cwd` alla radice.

Sette prove verificano **cosa si rifiuta di eseguire**, che è la metà che conta.

## Conseguenze

**Quel che si guadagna.** Una riga di §6.2 non può più invecchiare in silenzio.
Al primo giro il cancello ha trovato che la riga di F1.1-F1.3 era **già
invecchiata di poche ore** — diceva «4 norme su 39» mentre il repo era a 12 su
41 — e che due righe citavano misure senza dichiarare cosa si aspettassero.

**Quel che si paga.** Il passo esegue i comandi più lenti del repo, quindi gira
in un **job suo** e non blocca gli altri. E ogni riga di §6.2 che cita una
misura deve ora portare il suo `<!-- attesa: … -->`: è ceremonia, ed è il
prezzo per cui il numero scritto nella tabella sia verificabile.

**Quel che NON fa.** Non verifica che il lavoro dichiarato sia *sensato*, né
che il piano citato esista: verifica che il **numero** e lo **stato** di una
riga siano d'accordo con ciò che il comando stampa oggi. Una riga ⬜ che cita
un comando bloccato sul DM è esente e dichiarata tale.

## Fonti

- [ADR-0047](ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md) — il dato ha una casa sola, e un gate lo verifica
- [ADR-0062](ADR-0062-una-norma-senza-superficie-lo-dichiara.md) — un rilevatore senza superficie lo dichiara
- `plans/STATO-E-ORDINE-DEI-PIANI.md` §6.2-bis — il conto delle cinque righe
