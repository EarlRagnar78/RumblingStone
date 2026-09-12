# ADR-0049 — Il margine del bosco è un glifo a sé: `🌲` diventa opaco, la fascia attraversabile no

**Stato**: accettata — decisione DM del 2026-09-12 — **non ancora attuata**

**Data**: 2026-09-12
**Decisione-fonte**: ratifica della specifica funzionale (D1 di
[`PIANO-VENDIBILITA`](../PIANO-VENDIBILITA.md) §8), presa contestualmente
all'attuazione di [ADR-0048](ADR-0048-legenda-funzionale-fonte-unica.md).
**Attuazione**: lotto **1.1-ter** di `PIANO-VENDIBILITA` — ⬜ **da fare**.
**Precedenti diretti**: [ADR-0042](ADR-0042-tre-glifi-per-tre-cose.md) (stesso
schema: un glifo sovraccarico si divide) e
[ADR-0043](ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md)
(stesso difetto: il renderer disegna solido, l'export non ci mette un muro).

## Contesto

Un master si chiama *Foresta In Fiamme*. Il suo export UVTT contiene **zero**
segmenti di linea di vista: in Foundry si vede da un capo all'altro del bosco
in fiamme. Misurato il 2026-09-12 attuando ADR-0048.

Non è un caso isolato. `🌲` occupa **1.873 celle in 5 master**, e in nessuno di
essi ostruisce la vista nel VTT mentre nell'SVG stampato il bosco è chiaramente
denso. È il difetto di `⛰` — che ADR-0043 ha chiuso su 2.423 celle — in una
seconda specie, rimasto in piedi perché nessuno ha ancora giocato quelle mappe
al tavolo virtuale.

| Master | Segmenti di muro oggi | Se `🌲` fosse muro | Celle |
|---|---:|---:|---:|
| `…P1B-Foresta-In-Fiamme-MAPPA` | **0** | **64** | 489 |
| `SUPPLEMENTO-P1C…CAMPI-DROW` mappa 1 | 196 | 272 | 566 |
| `SUPPLEMENTO-P1C…CAMPI-DROW` mappa 2 | 80 | 96 | 849 |
| `…P1C-Rituale-COMPLETO-SCALE` mappe 1-3 | 92 · 0 · 0 | 140 · 24 · 60 | 439 |

## Il problema con la soluzione ovvia

Fare `🌲` un muro come `⛰` chiude il difetto e ne apre un altro **peggiore per
il tavolo**: il muro del VTT è binario, e un bosco no.

La specifica normativa lo dice contro se stessa
([`LEGENDA-FUNZIONALE-SPEC`](../../docs/guides/LEGENDA-FUNZIONALE-SPEC.md) §7):
*«`🌲` è un'approssimazione onesta. Una cella di foresta densa non blocca la
vista dentro di sé ma la blocca attraverso»*. Con `🌲` muro pieno, un PG **in
mezzo agli alberi** non vedrebbe il quadretto adiacente — e l'inseguimento nel
bosco, che è il motivo per cui quelle mappe esistono, diventerebbe ingiocabile
in VTT.

⚠️ **`⛰` aveva lo stesso rovescio e lo si è accettato**, dichiarandolo: *«un
valico è attraversabile nella finzione e adesso è muro; chi disegna un passo
usi un simbolo di terreno»*. Lì il compromesso reggeva perché la cella di
montagna che i PG **attraversano** è rara. Nel bosco è il caso normale.

## Decisione

**`🌲` diventa opaco, e la fascia di bosco che si attraversa prende un glifo
suo.** Due simboli per due cose, come ADR-0042 ha fatto con `⬛`:

| Glifo | Cos'è | Vista | Movimento | Muro UVTT |
|---|---|---|---|---|
| `🌲` | **Interno di bosco denso** — chiome chiuse, non si vede né si passa a vista | blocca | passa | **sì** |
| *(da scegliere)* | **Margine / sottobosco percorribile** — la fascia dove si combatte e si insegue | non blocca | passa | **no** |

Il glifo del margine si sceglie in fase di attuazione con lo stesso vincolo di
`🔳` in ADR-0042: **nessuna collisione**, cioè non deve comparire in nessuna
cella del repo prima di essere introdotto.

⚠️ **`🌿` (vegetazione bassa) non è il candidato ovvio e non va riusato per
comodità**: significa già un'altra cosa — sottobosco leggero fuori dal bosco, e
la spec gli dà `obscurement: light` e `move_cost: 2`. Un margine di bosco è
un'altra affordance.

## Conseguenze

**Cosa diventa più facile**

- *Foresta In Fiamme* e le mappe drow smettono di essere trasparenti in Foundry,
  che è il difetto per cui questa decisione esiste;
- chi disegna un inseguimento nel bosco ha il glifo giusto per la pista, invece
  di dover scegliere fra «tutto muro» e «niente muro»;
- la regola diventa dicibile in una riga sulla pagina della legenda, come per
  `⬛`/`⛺`/`🔳`.

**Cosa diventa più difficile / a cosa si rinuncia**

- 🔴 **Una coda di riclassificazione di 1.873 celle in 5 master.** È la stessa
  forma della coda di ADR-0042 (6.960 celle `⬛`) ed è **lettura, non
  sostituzione**: quali celle sono interno e quali margine lo dice la mappa, non
  un `sed`. Si smaltisce quando quella mappa viene toccata per altri motivi;
- fino ad allora `🌲` resta com'è, con la **deroga dichiarata** in
  `scripts/legend.yaml` — visibile, motivata e sorvegliata da
  `TestLeDerogheSonoDichiarate`, invece che invisibile come era prima;
- un sessantaquattresimo simbolo da imparare.

**Il limite di questa decisione, dichiarato**

⚠️ **Nessun gate distingue un uso corretto da uno pigro**, esattamente come
ADR-0042 §6.2: un agente può continuare a mettere `🌲` ovunque e la CI resta
verde. Il controllo qui è la legenda e chi la legge. Ciò che è misurabile — che
i due glifi restino distinti e che `🌲` non cambi comportamento finché la coda
non è smaltita — quello sì, e va nel test del lotto.

⚠️ **E il difetto resta aperto finché il lotto non parte.** Questa decisione
non chiude *Foresta In Fiamme*: la programma. Chi porta quella mappa al tavolo
virtuale prima di allora deve saperlo, ed è il motivo per cui la deroga in
`legend.yaml` cita questo numero.

## Cosa va rivisitato e quando

- se la coda di riclassificazione non si smaltisce entro l'arco 09, vale la pena
  chiedersi se convenga il compromesso di `⛰` (muro pieno e regola del sentiero)
  su tutto, accettando il costo al tavolo: **una decisione presa e non attuata è
  un difetto che ha smesso di far rumore**, ed è la lezione di ADR-0048, rimasta
  in un cassetto sei settimane;
- se l'editor visuale (`PIANO-EDITOR-VISUALE-MAPPE-TATTICHE`) introduce
  l'occlusione parziale per cella, questa decisione si può semplificare: il
  margine diventerebbe un valore, non un glifo.
