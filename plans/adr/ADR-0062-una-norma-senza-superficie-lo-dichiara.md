# ADR-0062 — Una norma senza superficie lo dichiara, e il numero che stampa è la superficie

- **Stato**: 🟢 accettata
- **Data**: 2026-09-21
- **Contesto**: ordine del DM — *«serve un rilevatore per tutte le norme che sia
  deterministico e idempotente»*
- **Sostituisce**: niente. **Estende**: [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md)

---

## Contesto

ADR-0056 ha stabilito che **una norma senza misura non esiste**, e ha portato il
registro delle norme: ogni norma dice chi la guarda, e un «non misurato» deve
portare una ragione scritta. Il cancello lo verifica da settembre.

Il 2026-09-21 il DM ha chiesto il passo successivo: un rilevatore per **tutte**
le norme. Misurando le undici scoperte è venuto fuori un fatto che nessuno
aveva scritto:

> **Per otto su nove non manca il codice.**

Manca il **dato** che la norma presuppone, oppure la **convenzione** con cui
quel dato si marcherebbe, oppure l'**oggetto** di cui la norma parla — o il
fatto non sta nel testo e non ci starà mai.

Scrivere un rilevatore lo stesso produrrebbe un numero finto: `0 violazioni` su
un insieme vuoto è indistinguibile da `0 violazioni` su un insieme conforme, e
la seconda lettura è quella che chi legge farà.

## Il problema con la ragione scritta

ADR-0056 accetta un «non misurato» purché porti il perché. Il perché è
**prosa**, e la prosa invecchia in silenzio: il 2026-09-21 si è scoperto che
*«i 27 ADR mancanti in `docs/INDEX.md`»* erano **zero**, e che 27 non era mai
stato un numero misurato. Il comando che lo diceva era citato accanto alla
riga, girava in CI ed era verde.

Una ragione che nessun comando rimisura è un ricordo con un'icona davanti.

## Decisione

**Ogni norma non misurata dichiara il suo stato di superficie, e lo stato è
derivato da un comando.** Gli stati sono quattro, e il passo successivo è
diverso in ciascuno:

| stato | cosa manca | il passo successivo |
|---|---|---|
| `SUPERFICIE_VUOTA` | la convenzione **esiste** e ha **zero occorrenze** | marcare il contenuto: il rilevatore si accende da solo |
| `CONVENZIONE_ASSENTE` | nessuno ha deciso **come si marca** | una decisione di forma, poi la marcatura |
| `OGGETTO_ASSENTE` | non esiste il **file** di cui la norma parla | produrre l'oggetto, o ammettere che non esiste |
| `FUORI_DOMINIO` | il fatto **non è nel testo** | niente: si dichiara e si chiude |

Lo strumento è `scripts/superficie_norme.py`. `--check` gira in CI e **non
boccia una superficie vuota** — una superficie vuota è un fatto, non un
difetto. Boccia una riga che ha smesso di dire il vero: una norma diventata
misurabile che il registro dichiara ancora 🔴.

## Conseguenze

**Quel che si guadagna.** Il debito delle norme scoperte smette di essere un
elenco omogeneo di «lavoro da fare» e diventa quattro code diverse, ciascuna
con il suo committente. Due sono a **superficie vuota**: il rilevatore c'è già,
manca la marcatura, e il giorno che arriva la norma si accende da sola. Quattro
chiedono una **decisione di forma**, che non è di uno script. Una chiede un
oggetto che non esiste. Due sono chiuse per sempre, e dirlo toglie due righe
dal debito invece di lasciarle a marcire.

**Quel che si paga.** Una tabella in più da tenere aggiornata, e un cancello in
più in CI. Il costo è contenuto perché la tabella è **dato**, non prosa: nove
righe con la forma dichiarata accanto, e il gate confronta il numero di righe
🔴 del registro con il numero di righe descritte — se qualcuno aggiunge una
norma scoperta senza descriverne la superficie, la CI è rossa.

**Quel che NON cambia.** ADR-0056 resta: una norma senza misura non esiste. Qui
si aggiunge che un «non misurato» deve dire **quale dei quattro buchi** è, e
deve farlo con un comando.

⚠️ **Il limite, dichiarato.** `FUORI_DOMINIO` è una classificazione umana:
nessun cancello può stabilire che *«almeno un congegno per campagna deve
scattare davvero»* non stia nel testo. Chi la scrive se ne assume la
responsabilità, come per la ragione di ADR-0056 — ma a differenza di quella,
questa dichiarazione è **rara** (due righe su nove) e sta accanto alle altre
sette che invece un comando rimisura.

## Fonti

- [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) — il registro delle norme
- [ADR-0059](ADR-0059-il-punteggio-di-qualita-e-mqm-adattato.md) — il punteggio pesato
- [ADR-0053](ADR-0053-la-chiave-verso-il-bestiario-si-dichiara.md) — un rimando inventato sembra copertura
- `plans/PIANO-MISURA-EDITORIALE-STANDARD.md` §F2.9
