---
name: rumblingstone-art-direction
description: >
  Il mestiere dell'art director applicato alle immagini di RumblingStone: bibbia
  visiva, scheda-personaggio che rende un volto riconoscibile fra un'immagine e
  l'altra, brief d'inquadratura con la funzione narrativa, lock tecnici (seed,
  luce, camera), e soprattutto il **gate di rifiuto** — quando un'immagine si
  butta invece di tenerla perché «è già venuta». Use WHENEVER si generano,
  commissionano, valutano o rigenerano immagini: ritratti, tavole, copertine,
  handout, hero map. Trigger su: "direzione artistica", "art director",
  "coerenza fra le immagini", "le immagini non si somigliano", "ritratti",
  "tavola", "copertina", "che seed", "quale modello", "rigenero o tengo?",
  "l'immagine è brutta ma non so perché", "set di immagini", "bibbia visiva",
  "scheda personaggio", "continuity".
---

# RumblingStone — Direzione artistica

Il repo sa **scrivere** i prompt ([ADR-0015](../../plans/adr/ADR-0015-standard-prompt-immagine.md))
e sa **eseguirli** ([`GUIDA-IMMAGINI.md`](../../docs/guides/GUIDA-IMMAGINI.md)).
Questa skill copre il mestiere che sta in mezzo, e che è il motivo per cui dieci
immagini generate bene restano dieci immagini invece di diventare **un libro**.

> **La riga da ricordare**: un art director non decide come sarà bella
> un'immagine. Decide **cosa hanno in comune tutte le immagini** e **quando una
> si butta**. Il resto lo fa il disegnatore — o il modello.

---

## §1 · Le sei leve, in ordine di quanto pesano

| # | Leva | Cosa fissa | Se manca si vede così |
|---|---|---|---|
| 1 | **Bibbia visiva** | palette, resa, materiali, epoca | ogni immagine sembra di un altro progetto |
| 2 | **Ancora storica** | la scuola pittorica in pubblico dominio | il set «oscilla»: una tavola sembra un olio, la successiva un rendering |
| 3 | **Scheda-personaggio** | il volto, i segni, i colori indossati | il PNG non è riconoscibile fra ritratto e tavola di gruppo |
| 4 | **Lock tecnici** | seed, direzione della luce, altezza camera | luci che arrivano da parti diverse nella stessa stanza |
| 5 | **Brief d'inquadratura** | cosa c'è dentro **e perché** | immagini corrette e inutili |
| 6 | **Gate di rifiuto** | quando si butta | il set scende al livello del pezzo peggiore |

Le prime quattro sono *prima* della generazione. Le ultime due sono *dopo*, e
sono quelle che di solito non si fanno.

---

## §2 · L'ancora storica — la leva più economica che esista

Il divieto di ADR-0005 riguarda **gli artisti viventi e le loro tavole**. Lascia
aperta la cosa che serve davvero: **una scuola pittorica in pubblico dominio da
secoli** è una categoria storica, non la firma di nessuno.

- ✅ `flemish panel painting`, `venetian cinquecento`, `northern renaissance oil
  glazing`, `egg tempera, gold-leaf ground, flat picture plane`
- ❌ il nome proprio di un pittore quando serve a evocare **le sue opere**
  invece della tecnica del periodo

Funziona meglio di qualunque elenco di aggettivi perché **fissa insieme** palette,
resa della luce, trattamento di mani e volti e profondità di campo: sono un
pacchetto storico, non scelte indipendenti.

⚠️ **La scuola si sceglie per la resa, non per il luogo.** Ancorare un modulo alla
pittura di una città reale da cui il modulo si sta allontanando per ragioni di
diritto rimette dalla finestra ciò che si è tolto dalla porta. *(Caso concreto: il
Drappo di Tarsilia usa l'ancora **fiamminga**, non quella senese, per questo
motivo esatto.)*

Il vocabolario completo sta in
[`stile-illustrazione-handout.md`](../rumblingstone-mapmaking/references/stile-illustrazione-handout.md)
della skill mapmaking, §«L'ancora che invece si può usare».

---

## §3 · La scheda-personaggio — quella che nessuno scrive

ADR-0015 §3 chiede la bibbia visiva **dell'arco**. Non basta: la bibbia tiene
insieme *il mondo*, non *le persone*. Un PNG che compare in tre immagini deve
essere la stessa persona in tutte e tre, e un modello generativo non se lo ricorda.

Per ogni personaggio che compare **più di una volta**, cinque righe, non di più:

```
NOME — età apparente · corporatura
VOLTO      tre tratti al massimo, quelli che si vedono da lontano
           (naso rotto, sopracciglia folte, cicatrice sullo zigomo sinistro)
CAPELLI    colore, lunghezza, come sono tenuti
INDOSSA    un capo riconoscibile + un colore che è SUO e di nessun altro
SEGNO      l'oggetto che porta sempre (un mazzo di chiavi, un cane, una benda)
```

Le regole che la rendono utile invece che decorativa:

1. **Tre tratti, non dieci.** Un elenco lungo il modello lo media e non lo rende.
2. **Un colore per persona, e non si ripete.** È il trucco più antico del
   fumetto e funziona anche quando le facce vengono male.
3. **Il segno vale più del volto.** Se il tavolo riconosce il personaggio dal
   cane e dalle chiavi, il ritratto ha fatto il suo lavoro anche se la faccia
   cambia un po'.
4. Va copiata **verbatim** in ogni prompt in cui il personaggio compare. Non
   riassunta: copiata.

---

## §4 · I lock tecnici

Quattro numeri, scritti una volta e riusati per tutto il set:

| Lock | Perché | Nota |
|---|---|---|
| **Seed** | rende la generazione **ripetibile**: senza, un'immagine persa è persa | si annota accanto al file, non si tiene a mente |
| **Direzione della luce** | è la prima cosa che l'occhio nota quando non torna | dichiarala a parole: *«luce da sinistra, alta, unica sorgente»* |
| **Altezza camera** | tiene insieme i ritratti come **serie** invece che come raccolta | ritratti all'altezza degli occhi; tavole leggermente sopra |
| **Formato** | non si cambia a metà set | ritratti verticali, tavole orizzontali |

⚠️ **Il seed non è un dettaglio da nerd**: è la differenza fra una serie
**riproducibile** e una irripetibile. Un modulo che si ristampa fra un anno con
due immagini rifatte a occhio si vede subito.

---

## §5 · Il brief d'inquadratura — la domanda che cambia tutto

Prima di scrivere il prompt, una riga sola:

> **Cosa dice questa immagine che il testo non può dire?**

Se la risposta è *«mostra la locanda descritta a pagina 12»*, l'immagine è
ridondante: il testo l'ha già fatto meglio. Se la risposta è *«fa capire in un
colpo che quella gente ha fame»*, l'immagine sta lavorando.

Le immagini che funzionano in un modulo fanno **una** di queste cose:

- **dicono un tono** che la prosa impiegherebbe un paragrafo a costruire;
- **rendono riconoscibile** una persona o un luogo che tornerà;
- **mostrano una relazione** — chi sta davanti a chi, chi guarda chi;
- **danno al DM un appiglio da descrivere** invece di leggere.

Quello che **non** devono fare: illustrare un momento che i giocatori devono
ancora vivere. Un'immagine che mostra il colpo di scena lo brucia (ADR-0013 §3
sugli spoiler vale anche per le figure, non solo per il testo).

---

## §6 · Il gate di rifiuto — dove si perde la qualità

È il pezzo che distingue un set diretto da un set raccolto. **Si butta e si
rigenera** quando anche solo una di queste è vera:

1. **le mani** sono sbagliate in modo che si nota a grandezza di stampa;
2. la **luce** non viene da dove dice il lock;
3. il personaggio **non è riconoscibile** rispetto alla sua scheda-personaggio;
4. c'è **testo** dentro l'immagine (scritte, insegne, rune inventate): in un
   libro stampato è la cosa che tradisce prima la generazione automatica;
5. **la simmetria è troppo perfetta** — è la firma tipica del modello, non una
   scelta di composizione;
6. l'immagine è **corretta e non dice niente** (§5).

La regola che rende il gate reale invece che teorico:

> **Il set vale quanto il suo pezzo peggiore.** Nove immagini buone e una
> mediocre non fanno «nove su dieci»: fanno un libro in cui il lettore si accorge
> che le immagini sono generate. **Meglio otto e due segnaposto vettoriali**, che
> almeno dichiarano cosa sono.

⚠️ E il bias da conoscere: dopo quaranta generazioni si tiene tutto quello che è
«abbastanza», perché si è stanchi. Il gate va applicato **il giorno dopo**, non
alla fine della sessione di generazione.

---

## §7 · Il ciclo completo, in ordine

```
1. bibbia visiva d'arco          ADR-0015 §3
2. ancora storica                §2  ← si sceglie UNA volta per progetto
3. schede-personaggio            §3  ← solo per chi compare più di una volta
4. lock tecnici                  §4  ← seed, luce, camera, formato
5. brief d'inquadratura          §5  ← una riga per immagine
6. scrittura dei prompt          ADR-0015 §2 (anatomia della scheda)
7. generazione                   GUIDA-IMMAGINI.md
8. gate di rifiuto               §6  ← IL GIORNO DOPO
9. provenienza                   ADR-0019: modello, licenza, seed, data
```

I passi 1-5 costano **mezza giornata per progetto** e si fanno una volta sola. È
il rapporto valore/costo più alto di tutta la produzione delle immagini: senza,
il passo 7 si ripete all'infinito.

---

## §8 · Quello che questa skill non può fare

Detto perché non ci si illuda:

- **non sostituisce un art director.** Un art director *guarda* le immagini e sa
  dire perché una non funziona. Qui c'è una lista di controlli che intercetta gli
  errori **frequenti**, non il gusto;
- **non risolve la coerenza al 100%.** Ancora storica + seed + luce condivisa
  portano un set generato da «visibilmente scollegato» a «coerente a un'occhiata
  distratta». Da lì al livello di un libro illustrato da una persona sola resta
  un salto che nessuna pipeline colma;
- **non decide se un'immagine serve.** Quello lo decide il §5, e la risposta
  giusta è spesso **nessuna immagine**. Un modulo con sei immagini scelte batte
  un modulo con venti generate.

---

## Materiale collegato

- [ADR-0015](../../plans/adr/ADR-0015-standard-prompt-immagine.md) — anatomia della
  scheda-prompt, bibbia visiva, confini IP
- [ADR-0019](../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md) — quale
  modello si può usare e cosa si registra
- [`GUIDA-IMMAGINI.md`](../../docs/guides/GUIDA-IMMAGINI.md) — la procedura
  operativa: generatori, salvataggio, troubleshooting
- [`stile-illustrazione-handout.md`](../rumblingstone-mapmaking/references/stile-illustrazione-handout.md)
  — il vocabolario di stile e l'ancora storica
- Esemplare: `STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`
