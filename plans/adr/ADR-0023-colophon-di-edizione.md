# ADR-0023 — Ogni volume porta il proprio colophon, e la data non si deduce

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: lotto **B** di
[`PIANO-CHIUSURA-CATENA-EDITORIALE`](../PIANO-CHIUSURA-CATENA-EDITORIALE.md),
autorizzato dal DM il 2026-09-02 («parti con A+B»). Il difetto era stato isolato
come **C1** in
[`RICERCA-RUOLI-EDITORIALI-COLOPHON`](../RICERCA-RUOLI-EDITORIALI-COLOPHON-PAIZO-2026-08.md),
nata dalla foto del colophon di *Ascesa dei Signori delle Rune*.

## Contesto

I volumi generati da questo repo uscivano **anonimi**. Lo schema del manifest
aveva sedici chiavi e nessuna era `credits`, `license`, `edition` o `version`; il
tema Typst non stampava nemmeno una data. Conseguenze concrete, non teoriche:

1. **Due PDF dello stesso capitolo, stampati a un mese di distanza, erano
   indistinguibili sul tavolo.** Qualcuno stampa la versione vecchia e nessuno se
   ne accorge finché non gioca.
2. **La riga che dice su cosa il materiale si basa**: SRD 3.5, OGL 1.0a,
   l'avventura originale — viveva solo nelle guide (ADR-0005,
   `GUIDA-CONDIVISIONE-IP.md`), cioè in file che chi riceve il PDF non ha.
3. Il regime d'uso («materiale del DM, non diffondere») era una frase da
   ripetere a voce ogni volta invece che una riga stampata.

Nel frattempo l'unico posto dove qualcosa di simile esisteva era `meta`: una riga
di **prosa** scritta a mano, manifest per manifest, presente in alcuni e assente
in altri. Una riga di prosa non è un dato: non si può ordinare, controllare, né
rendere uguale fra le due catene.

## Decisione

**Ogni volume può dichiarare un `colophon`, e quando lo dichiara la pagina esce
in entrambe le catene, con le stesse voci nello stesso ordine. La data si scrive
nel manifest e non si deduce mai dall'orologio.**

### 1. Il contratto

`colophon` è un oggetto nello schema del manifest, con chiavi dichiarate e
`additionalProperties: false`: `edizione`, `versione`, `data`, `autori`,
`basato_su`, `licenza`, `nota`. Un refuso fra le sue chiavi è un errore di gate,
non un silenzio — per questo `validate_booklets.py` ora **ricorre anche negli
oggetti annidati**, cosa che prima faceva solo per gli array.

### 2. L'ordine è fisso, e uguale nelle due catene

L'ordine delle voci è una costante (`VOCI_COLOPHON`) definita in entrambe le
catene, e **un test verifica che siano identiche**. Due catene che ordinano
diversamente i crediti producono due edizioni diverse dello stesso volume: è
esattamente la divergenza che ADR-0020 aveva promesso di chiudere.

### 3. La data non si deduce ⚠️

`datetime.today()` non compare in nessun punto di questa catena, e non deve
comparire. Un volume che prende la data dall'orologio **cambia a ogni
compilazione**: il PDF smette di essere byte-identico, e il gate di stampa in CI
— che confronta compilazioni — perde significato. La data è un dato editoriale,
si decide e si scrive.

### 4. Chi non lo dichiara non cambia

Senza la chiave, il volume esce esattamente come prima. Non è una migrazione: è
una possibilità. I dieci manifest che non la usano non sono stati toccati, e un
test lo verifica.

### 5. Dove sta la pagina

Sul **verso del frontespizio**, prima dell'introduzione e dell'indice — dov'è in
un manuale stampato. È una pagina autonoma **senza testatina**: è apparato, come
il frontespizio, e la testatina lì ripeteva due volte lo stesso titolo.

## Conseguenze

- **Più facile**: un PDF dice da dove viene, quando è stato fatto e cosa se ne
  può fare, senza che nessuno lo spieghi a voce. La versione sul frontespizio
  rende innocuo impaginare un master vivo — che `rumblingstone-editoria` §6
  sconsigliava proprio perché non c'era modo di distinguere due stampe.
- **Più difficile / rinuncia**: la data va aggiornata **a mano** quando si
  ristampa. È il prezzo del punto 3, ed è voluto: preferiamo una data vecchia e
  visibile a un PDF che cambia da solo.
- **Non fa**: non genera crediti che nessuno ha scritto. Se il manifest non
  dichiara gli autori, la riga non esce — inventare un nome in una pagina di
  crediti è peggio che non averla.
- **Da rivisitare**: quando esisterà una *ristampa* vera, cioè quando il repo
  avrà anche un concetto di errata (**C3** della ricerca, ancora aperto). Allora
  `versione` smetterà di essere una stringa libera e diventerà un contatore con
  una regola.
