# ADR-0016 — Lingua sorgente italiana, l'inglese è un'edizione derivata

**Stato**: accettata
**Data**: 2026-08-01
**Decisione-fonte**: domanda DM 2026-08-01 — *«se un domani volessi pubblicare
qualcosa, renderlo davvero in inglese e non tradurlo sarebbe un vantaggio?»*,
nata dal rilievo dei giocatori: gli handout erano scritti *«così male in
italiano che per loro era quasi meglio averlo in inglese»*.

## Contesto

Era stata proposta una pipeline editoriale a più ruoli in cui un «narratore»
scrive la prima stesura **in inglese** e un «adattatore» la porta in italiano,
sul modello di come un libro esce in più lingue.

Tre fatti hanno deciso la questione:

1. **Il tavolo gioca in italiano.** Il testo che viene letto ad alta voce a
   quattro persone è testo collaudato dalla realtà — vale più di qualsiasi
   passata editoriale, e lo si ottiene solo se la sorgente è la lingua del
   tavolo.
2. **L'adattamento non sposta le ossa.** La struttura si sceglie in stesura:
   ritmo, ordine delle informazioni, scelta dei tempi. Un adattatore cambia le
   parole; il respiro resta quello della lingua di partenza. È esattamente il
   difetto che i giocatori hanno segnalato
   (`references/italiano-nativo.md`).
3. **Gli strumenti italiani non sono traduzioni di niente.** Dislocazione a
   sinistra, congiuntivo, passato remoto per la leggenda, alterati: si
   scelgono componendo, non retroattivamente.

Nel modello editoriale reale, del resto, un libro in dieci lingue ha **una
sola lingua sorgente — quella in cui l'autore pensa** — e poi edizioni affidate
a traduttori letterari madrelingua con licenza di ri-creare. Nessun editore fa
scrivere l'autore in una seconda lingua per poi riportarlo nella sua.

## Decisione

**L'italiano è la lingua sorgente di tutto il contenuto narrativo. L'inglese,
se e quando servirà, è un'edizione derivata prodotta per transcreation
dall'italiano finito — mai il contrario.**

### 1. Cosa è sorgente e cosa no

| Livello | Lingua | Nota |
|---|---|---|
| **Prosa**: read-aloud, handout, dialoghi, descrizioni | **italiano, sempre** | è qui che si crea la qualità |
| **Scaletta / beat sheet**: cosa succede, chi è protagonista, forma emotiva | indifferente | la lingua non incide sulla struttura degli eventi |
| **Documentazione tecnica**, skill agent-facing, commenti di codice | inglese ammesso | è già la prassi del repo |
| **Edizione inglese** | derivata | prodotta a valle, su richiesta |

### 2. Se e quando si farà l'edizione inglese

**Transcreation, non traduzione**: chi la produce ha licenza di riscrivere per
ottenere lo stesso *effetto*, non le stesse parole. Servirà un
`references/inglese-nativo.md` speculare a quello italiano, con le regole
rovesciate (cosa fa suonare *tradotto-dall'italiano* un testo inglese: periodi
lunghi, subordinate accumulate, nominalizzazioni, connettivi ridondanti).

**Non si costruisce adesso**, per due ragioni:
- la sorgente **cambia a ogni sessione**: mantenere due edizioni allineate su
  un testo vivo è il modo più rapido per averne una sbagliata;
- ⚠️ **c'è un tetto di IP che nessuna lingua alza.** La campagna è Red Hand of
  Doom adattato ai Forgotten Realms: pubblicazione gratuita 🟡 con condizioni,
  **vendita ❌** (`docs/guides/GUIDA-CONDIVISIONE-IP.md`). L'unico materiale
  realmente pubblicabile è quello **originale** (Terros, i Bracieri, la Cronaca
  Vivente, Balvar, il sistema del Palio) **riambientato fuori da Faerûn** — e
  quello sì, un giorno, in inglese nativo.

### 3. Cosa si costruisce invece adesso: il loc kit

È la parte del modello editoriale che vale **a prescindere dalla lingua** e che
costa caro a rifarla dopo: **glossario bloccato** e **lista non-tradurre**, in
`campaign/GLOSSARIO-E-LOCALIZZAZIONE.md`. Oggi il repo mescola già nomi inglesi
(*Aegis Fang*, *Skullcrusher*, *Hammerfist*) e italiani (*Barbadiferro*,
*Fuocospento*, *Corona di Adamantio*): al tavolo funziona, in due edizioni
parallele diventa un problema se non è deciso una volta sola.

## Conseguenze

- Più facile: la qualità si concentra dove viene collaudata; una sola
  sorgente da mantenere; il glossario esiste prima di servire.
- Più difficile / rinunce: **niente uscita inglese immediata**. Se domani
  servisse un estratto in inglese, va prodotto a mano dall'italiano — accettato.
- Da rivisitare: **quando esisterà una cosa concreta e IP-pulita da
  pubblicare**. Allora si scrive `inglese-nativo.md` e si apre l'edizione.

## Il vero rimedio al rilievo dei giocatori

Non era la lingua: era la qualità. La risposta sta in tre riferimenti della
skill di stile — `italiano-nativo.md` (§1-8 traduttese, §9 tic dell'IA),
`read-aloud-adulti.md` (il pubblico: adulti che il fantasy lo conoscono) e le
passate editoriali. **Banco di prova**: i prossimi handout. Se i giocatori
diranno ancora che sembra tradotto, il problema non è la lingua e non è la
pipeline — e questa ADR va riaperta.

## Copertura skill / docs

- `skills/rumblingstone-narrative-style/SKILL.md` — load order.
- `references/italiano-nativo.md` · `references/read-aloud-adulti.md`.
- `campaign/GLOSSARIO-E-LOCALIZZAZIONE.md` — glossario e DNT.
- [`docs/guides/GUIDA-CONDIVISIONE-IP.md`](../../docs/guides/GUIDA-CONDIVISIONE-IP.md) — il tetto di pubblicazione.
