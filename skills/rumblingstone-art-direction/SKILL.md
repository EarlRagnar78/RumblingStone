---
name: rumblingstone-art-direction
description: >
  Il mestiere dell'art director applicato alle immagini di RumblingStone: bibbia
  visiva, scheda-personaggio che rende un volto riconoscibile fra un'immagine e
  l'altra, brief d'inquadratura con la funzione narrativa, lock tecnici (seed,
  luce, camera), e soprattutto il **gate di rifiuto** — quando un'immagine si
  butta invece di tenerla perché «è già venuta». Va usata OGNI VOLTA che si
  generano, commissionano, valutano o rigenerano immagini: ritratti, tavole,
  copertine, handout, hero map. Trigger su: "direzione artistica", "art director",
  "coerenza fra le immagini", "le immagini non si somigliano", "ritratti",
  "tavola", "copertina", "che seed", "quale modello", "rigenero o tengo?",
  "l'immagine è brutta ma non so perché", "set di immagini", "bibbia visiva",
  "scheda personaggio", "continuity", "Canva", "Canva AI", "genera le immagini",
  "confronto immagine-scheda", "il ritratto non somiglia alla scheda".
---

# RumblingStone — Direzione artistica

Il repo sa **scrivere** i prompt ([ADR-0015](../../plans/adr/ADR-0015-standard-prompt-immagine.md))
e **eseguirli** ([`GUIDA-IMMAGINI.md`](../../docs/how-to/GUIDA-IMMAGINI.md)).
Questa skill copre il mestiere in mezzo: quello che fa di dieci immagini **un libro**.

> **La riga da ricordare**: un art director non decide come sarà bella
> un'immagine. Decide **cosa hanno in comune tutte le immagini** e **quando una
> si butta**. Il resto lo fa il disegnatore — o il modello.

## Quando no

- Scrivere la scheda-prompt → ADR-0015; eseguirla → `GUIDA-IMMAGINI.md`.
- **Non sostituisce un art director**: intercetta gli errori **frequenti**, non
  il gusto. **Non dà coerenza al 100%**: ancora storica + seed + luce condivisa
  portano un set da «visibilmente scollegato» a «coerente a un'occhiata
  distratta»; il salto al libro illustrato da una persona sola nessuna pipeline
  lo colma.
- **Non decide se un'immagine serve**: lo decide §5, e spesso la risposta è
  **nessuna immagine**. Sei immagini scelte battono venti generate.

## Fonti

1. [ADR-0015](../../plans/adr/ADR-0015-standard-prompt-immagine.md): scheda-prompt, bibbia visiva, confini IP.
2. [ADR-0019](../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md): quale modello si usa, cosa si registra.
3. [`GUIDA-IMMAGINI.md`](../../docs/how-to/GUIDA-IMMAGINI.md): generatori, salvataggio, troubleshooting.
4. [`stile-illustrazione-handout.md`](../rumblingstone-mapmaking/references/stile-illustrazione-handout.md)
   — il vocabolario di stile e l'ancora storica.
5. Schede-personaggio: master d'arco, statblocco del Bestiario, ritratti canone (§7-bis.1).
6. Esemplare: `10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`

## §1 · Le sei leve, in ordine di quanto pesano

| # | Leva | Cosa fissa | Se manca si vede così |
|---|---|---|---|
| 1 | **Bibbia visiva** | palette, resa, materiali, epoca | ogni immagine sembra di un altro progetto |
| 2 | **Ancora storica** | la scuola pittorica in pubblico dominio | il set «oscilla»: una tavola sembra un olio, la successiva un rendering |
| 3 | **Scheda-personaggio** | il volto, i segni, i colori indossati | il PNG non è riconoscibile fra ritratto e tavola di gruppo |
| 4 | **Lock tecnici** | seed, direzione della luce, altezza camera | luci che arrivano da parti diverse nella stessa stanza |
| 5 | **Brief d'inquadratura** | cosa c'è dentro **e perché** | immagini corrette e inutili |
| 6 | **Gate di rifiuto** | quando si butta | il set scende al livello del pezzo peggiore |

Le prime quattro stanno *prima* della generazione, le ultime due *dopo* (quelle che di solito non si fanno).

## §2 · L'ancora storica — la leva più economica

Il divieto di ADR-0005 riguarda **gli artisti viventi e le loro tavole**. **Una
scuola pittorica in pubblico dominio da secoli** è una categoria storica, non
la firma di nessuno.

- ✅ `flemish panel painting`, `venetian cinquecento`, `northern renaissance oil
  glazing`, `egg tempera, gold-leaf ground, flat picture plane`
- ❌ il nome proprio di un pittore quando serve a evocare **le sue opere**
  invece della tecnica del periodo

Batte qualunque elenco di aggettivi perché **fissa insieme** palette, luce,
mani e volti, profondità di campo: un pacchetto storico, non scelte
indipendenti.

⚠️ **La scuola si sceglie per la resa, non per il luogo.** Ancorare un modulo
alla pittura di una città reale da cui si allontana per ragioni di diritto
rimette dalla finestra ciò che si è tolto dalla porta (il Drappo di Tarsilia
usa l'ancora **fiamminga**, non la senese, per questo).

Vocabolario: `stile-illustrazione-handout.md` (mapmaking), §«L'ancora che invece si può usare».

## §3 · La scheda-personaggio

La bibbia visiva dell'arco (ADR-0015 §3) tiene insieme *il mondo*, non *le
persone*, e un modello generativo non si ricorda un volto. Per ogni personaggio
che compare **più di una volta**, cinque righe, non di più:

```
NOME — età apparente · corporatura
VOLTO      tre tratti al massimo, quelli che si vedono da lontano
           (naso rotto, sopracciglia folte, cicatrice sullo zigomo sinistro)
CAPELLI    colore, lunghezza, come sono tenuti
INDOSSA    un capo riconoscibile + un colore che è SUO e di nessun altro
SEGNO      l'oggetto che porta sempre (un mazzo di chiavi, un cane, una benda)
```

1. **Tre tratti, non dieci.** Un elenco lungo il modello lo media e non lo rende.
2. **Un colore per persona, e non si ripete**: funziona anche quando le facce
   vengono male.
3. **Il segno vale più del volto.** Se il tavolo riconosce il personaggio dal
   cane e dalle chiavi, il ritratto ha fatto il suo lavoro anche se la
   faccia cambia un po'.
4. Va copiata **verbatim** in ogni prompt in cui il personaggio compare. Non
   riassunta: copiata.

## §4 · I lock tecnici

Quattro numeri, scritti una volta e riusati per tutto il set:

| Lock | Perché | Nota |
|---|---|---|
| **Seed** | rende la generazione **ripetibile**: senza, un'immagine persa è persa | si annota accanto al file, non si tiene a mente |
| **Direzione della luce** | è la prima cosa che l'occhio nota quando non torna | a parole: *«luce da sinistra, alta, unica sorgente»* |
| **Altezza camera** | tiene insieme i ritratti come **serie** | ritratti all'altezza degli occhi; tavole leggermente sopra |
| **Formato** | non si cambia a metà set | ritratti verticali, tavole orizzontali |

⚠️ Il seed è la differenza fra una serie **riproducibile** e una irripetibile.
Se lo strumento **non lo espone** (i servizi come Gemini), **il file generato
diventa il sorgente**: si versiona e non si butta mai (ADR-0019 §2-bis).

## §5 · Il brief d'inquadratura

Prima del prompt, una riga sola:
> **Cosa dice questa immagine che il testo non può dire?**

*«Mostra la locanda descritta a pagina 12»*: ridondante. *«Fa capire in un
colpo che quella gente ha fame»*: sta lavorando. Un'immagine di modulo fa
**una** di queste cose:

- **dice un tono** che la prosa costruirebbe in un paragrafo;
- **rende riconoscibile** una persona o un luogo che tornerà;
- **mostra una relazione**: chi sta davanti a chi, chi guarda chi;
- **dà al DM un appiglio da descrivere** invece di leggere.

**Non** illustra un momento che i giocatori devono ancora vivere: mostrare il
colpo di scena lo brucia (ADR-0013 §3 sugli spoiler vale anche per le figure).

## §6 · Il gate di rifiuto

**Si butta e si rigenera** quando anche solo una è vera:

1. **le mani** sono sbagliate in modo che si nota a grandezza di stampa;
2. la **luce** non viene da dove dice il lock;
3. il personaggio **non è riconoscibile** rispetto alla sua scheda-personaggio;
4. c'è **testo** dentro l'immagine (scritte, insegne, rune inventate): in un
   libro stampato tradisce per primo la generazione automatica;
5. **la simmetria è troppo perfetta**: firma del modello, non composizione;
6. l'immagine è **corretta e non dice niente** (§5).

> **Il set vale quanto il suo pezzo peggiore.** Nove buone e una mediocre non
> fanno «nove su dieci»: fanno un libro in cui il lettore si accorge che le
> immagini sono generate. **Meglio otto e due segnaposto vettoriali**, che
> almeno dichiarano cosa sono.

🔢 **Tessere delle mappe** (ADR-0086): una tessera, generata o resa da un
modello, sostituisce un glifo solo se `misura_resa.py` non la boccia
(contrasto del contorno, confusione col simbolo vicino, distanza dalla
tavolozza) **e** il DM la preferisce nel confronto alla cieca. La misura dice
se si legge; se è più bella lo dice solo il DM.

⚠️ Dopo quaranta generazioni si tiene tutto ciò che è «abbastanza», per
stanchezza: il gate si applica **il giorno dopo**, non alla fine della sessione
di generazione.

## Procedura

### §7 · Il ciclo completo, in ordine

```
1. bibbia visiva d'arco          ADR-0015 §3
2. ancora storica                §2  ← si sceglie UNA volta per progetto
3. schede-personaggio            §3  ← solo per chi compare più di una volta
4. lock tecnici                  §4  ← seed, luce, camera, formato
5. brief d'inquadratura          §5  ← una riga per immagine
6. scrittura dei prompt          ADR-0015 §2 (anatomia della scheda)
7. generazione                   GUIDA-IMMAGINI.md
8. confronto immagine-scheda     §7-bis passo 4 ← una riga per id
9. gate di rifiuto               §6  ← IL GIORNO DOPO
10. provenienza                  ADR-0019: modello, licenza, seed, data
```

I passi 1-5 costano **mezza giornata per progetto**, una volta sola: il
miglior rapporto valore/costo della produzione. Senza, il passo 7 si ripete
all'infinito.

### §7-bis · La procedura con un servizio (Canva AI), come per ARC-07

È quella da ripetere finché la pipeline locale di ComfyUI non è collaudata.
Quando il DM dice «genera le immagini» o «genera i prompt» si fa questa, in
quest'ordine; è la parte immagini del corredo della serata
(`rumblingstone-automation`, «Il corredo della serata»). Dove resta scritto
ogni passo: `## Formato d'uscita`.

1. **La scheda-personaggio si prende dal master**, non si inventa: ruolo,
   abiti, armi e segno dal master d'arco e dallo statblocco del Bestiario; per
   i volti già canone vale il ritratto che c'è. Cinque righe per PNG (§3).
2. **Il prompt** si scrive dalla scheda copiata parola per parola, col look
   comune, l'ancora storica e i negativi del set (ADR-0015): un blocco
   `<!-- img id=… -->` per immagine.
3. **Canva AI**: un testo solo, nell'ordine look + ancora + soggetto +
   negativi in coda come «no text, no watermark…», perché il servizio non ha il
   campo. Rapporto 2:3 per i ritratti, 16:9 per le tavole. Un riferimento 3D
   (un ritratto di PG) si chiede «reso a olio», o lo stile del riferimento
   vince sul set. Il file esportato prende il nome dell'`id`.
4. **Confronto PNG per PNG con la scheda**, a piena risoluzione e **mai sulla
   miniatura**. **Sui tratti del volto vince il ritratto**, e la scheda si
   allinea; **l'arma resta quella dello statblocco** anche quando il ritratto
   la disegna diversa (Durin: ascia doppia nel master, a una lama nel
   ritratto). Una riga per `id`.
5. **Il gate di rifiuto** (§6), il giorno dopo: si butta anche quando «è già
   venuta». Con un servizio non c'è seme da cambiare: si corregge **il
   prompt**, perché la correzione vale per qualunque modello. Esce l'immagine
   rigenerata, o tenuta con la riserva scritta.

I termini di Canva si rileggono prima di pubblicare, non una volta per sempre
(ADR-0019 §2-bis), e il modello del servizio non è dichiarato. Il caso da cui
vengono i passi 4 e 5 (scarti sulla miniatura che erano buoni a piena vista) è
scritto in `PROMPT-RITRATTI-E-TAVOLE-ARC07.md`.

## Formato d'uscita

| Passo | Cosa si produce | Dove resta scritto |
|---|---|---|
| 1 | cinque righe per PNG, nel modello di §3 | il file delle schede-scena dell'arco (per ARC-07 `PROMPT-IMMAGINI-07ILP.md`) |
| 2 | un blocco `<!-- img id=… -->` per immagine | il file dei prompt eseguibili (per ARC-07 `PROMPT-RITRATTI-E-TAVOLE-ARC07.md`) |
| 3 | il file esportato col nome dell'`id` | la tabella dell'esecuzione nel file dei prompt, con l'identificativo del media Canva; la riga in `PROVENIENZA.txt` con seme «—» (ADR-0019 §2-bis: il file è il sorgente e non si butta) |
| 4 | una riga per `id` | la sezione «Confronto immagine-scheda» del file dei prompt: id, con che cosa si è confrontata, cosa non coincideva, esito |
| 5 | l'immagine rigenerata, o tenuta con la riserva | il motivo in `SCARTI.txt`, la correzione nel blocco `img` |

Con pesi locali: seed accanto al file (§4), provenienza per ADR-0019.

## Prima di consegnare

- Ogni immagine risponde alla domanda di §5, e nessuna brucia un colpo di scena?
- Il gate di §6 è passato **il giorno dopo**, a piena risoluzione?
- Ogni blocco `img` ha il suo file e la sua riga nel confronto? Lo dice
  `python3 scripts/validate_corredo.py`; se il confronto è giusto lo decide
  il passo 4, cioè chi guarda l'immagine accanto alla scheda, con il DM per i
  volti.
- Seed o riga in `PROVENIENZA.txt` ci sono per ogni file, e i termini del
  servizio sono stati riletti?

## Cancelli deterministici

I controlli che non chiedono un giudizio, da far girare prima di consegnare.
Quello che qui non c'è resta giudizio di chi legge (registro delle norme).

- `python3 scripts/validate_booklets.py`: le immagini citate esistono e le mappe entrano in pianta (ADR-0106).
