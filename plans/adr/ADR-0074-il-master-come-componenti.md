# ADR-0074 — Il master come componenti

- **Stato**: accettata
- **Data**: 2026-09-26
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, lo stesso giorno: *«tutti i DEF sono divisibili in
  una serie di oggetti che poi vengono rimessi insieme per creare il modulo […]
  magari così come funzionano gli editor di publishing tipo Scribus»*; poi
  *«sì a tutte e 3»*, cioè il markdown tipizzato **prima** di scrivere i DEF di
  ARC-08
- **Rapporti**: legge i componenti che ADR-0073 ha fissato (contratto «In
  scena», scheda d'entrata, comparse); riusa il blocco statistiche di ADR-0021;
  resta dentro ADR-0003 (il markdown è il master); genera l'apparato che
  `rumblingstone-module-standard` §15 chiede

## Contesto

Scribus e InDesign separano il contenuto dalla pagina: il testo sta in
cornici, e le stesse cornici si ricompongono. Un master DEF non si può scrivere
così: è prosa lunga, e il DM lo legge e lo corregge come prosa.

Ma dentro la prosa ci sono già blocchi con un tipo e una forma fissa, e da
ADR-0073 un gate ne controlla la presenza: la scena con il suo titolo, la riga
`**In scena** — Dove: … — Chi: …`, il box `**Read-aloud (pilastro) — luogo.**`,
la `**Scheda d'entrata — Nome**` con le righe Aspetto, Vuole, Suona e Sa, la
tabella `**Comparse**`, la battuta `**NOME:**`, la prova `<Abilità> CD N`. Il
modulo è già tipizzato. Nessuno strumento però usava quei tipi per **produrre**
qualcosa.

Due cose se ne ricavano, e finora si facevano a mano o non si facevano:

1. **L'apparato d'uso.** module-standard §15 chiede il foglio del cast,
   l'inserto con le CD e l'indice dei read-aloud. Scritti a mano, divergono alla
   prima modifica della scena.
2. **Le copie.** Il DM vuole i numeri di Balvar nel modulo, non solo nel
   Bestiario. PR #180 li ha copiati e ha messo un test che confronta sette
   numeri con delle regex: funziona, ma ogni nuova copia chiede un test nuovo.

## Misure prima di decidere

**Le copie alla lettera fra file vivi.** Paragrafi di almeno 200 caratteri
identici in due file, escluso `build/`: 1.903. Quasi tutti sono archivi,
versioni `DEPRECATO` o vecchie cartelle doppie dello stesso arco, che per
definizione non si sincronizzano. Fra i **master DEF: zero.** DEF-4 coincide
solo con il proprio archivio. L'unica coppia viva utile,
`ARC08-01-GUIDA-DM` ⟷ `hammerfist_encounters-…-final` con 37 paragrafi, si
risolve fondendo i due file nel master di ARC-08, non includendo l'uno
nell'altro.

**La copia di Balvar non è alla lettera.** Il Bestiario scrive «hp 96»,
«Init +2», i Domini e un `[INFERRED]`; DEF-4 A.4 è una riscrittura per il tavolo.
Includere la prosa del Bestiario avrebbe peggiorato il modulo. **Il blocco
```` ```statblocco ```` invece è lo stesso dato** in tutti e due i posti, ed è
già un componente tipizzato (ADR-0021), con il suo riquadro in stampa.

**L'inserto delle CD.** Il primo estrattore prendeva le parole in maiuscolo
prima di «CD N» e su DEF-4 ne perdeva 13 su 43: «FOR o DES grezza», «Conoscenze
storia», «Forza o attacco, CD 18», un nome di prova andato a capo dentro il
grassetto. Il criterio adottato non perde niente (43 su 43), perché ogni `CD N`
entra e l'etichetta è la coda della sua cella o frase. Ha un limite dichiarato:
l'etichetta è testo, non un nome di prova interpretato, e a volte è una
mezza frase («gruppo della Scena 4 scende a»). Un test sorveglia che nessuna CD
di DEF-4 manchi.

## Decisione

**`scripts/componenti.py` legge il master come componenti, e ne fa tre cose.**

1. **L'indice** (`MASTER.md --json`), scena per scena: dove, chi, box, schede,
   comparse, battute, prove. Scene, contratto e schede si leggono con le stesse
   funzioni di `copertura_scene`, i box con quelle di `misura_craft`: una norma,
   un rilevatore.
2. **L'apparato generato** (`--apparato`), per ogni master col contratto «In
   scena». Esce in `APPARATO-<master>.md` accanto al master, con
   un'intestazione che dice di non modificarlo. Il prefisso è una scelta
   obbligata: con il suffisso `…-APPARATO.md` il file combaciava con
   `ARC*-DEF-*.md`, e quattro strumenti lo prendevano per un master. Alla prima
   prova ne è nato un `-APPARATO-APPARATO.md`.
3. **Le copie sincronizzate** (`--includi`). Il file che riceve scrive
   `<!-- include: fonte#nome -->` … `<!-- /include -->`, e lo script ci copia
   il blocco della fonte: `<!-- blocco: nome -->` … `<!-- /blocco -->`, oppure,
   con `#statblocco`, il recinto della scheda del Bestiario, senza toccare la
   scheda. **Il testo copiato resta nel sorgente**, perché il DM, il lettore a
   freddo e `copertura_scene` leggono il markdown grezzo, non la stampa.

`--check` fa tutte e due le verifiche, ed è un passo della CI.

**Primo uso**: DEF-4 A.4 include il blocco statistiche di Balvar dal Bestiario.
La prosa per il tavolo (BAB e Lotta, Leggere il Fuori-Posto, incantesimi, rune)
resta scritta a mano. BAB e Lotta non sono campi del blocco, quindi
`TestLaCopiaDiBalvar` resta per loro.

## Alternative scartate

- **Risolvere le inclusioni alla stampa**, nel caricatore comune
  `dmcore/testo.py:leggi_per_la_stampa`. È come lavorano gli editori, ma il
  sorgente mostrerebbe un marcatore al posto dei numeri, e chi legge il
  markdown è proprio il DM al tavolo.
- **Un formato di componenti separato** (YAML per scena, e il master generato).
  Sarebbe lo Scribus vero, ma rovescia ADR-0003: il DM correggerebbe un file
  generato, oppure dovrebbe imparare un formato nuovo per scrivere prosa.
- **Includere la prosa di Balvar dal Bestiario.** Misurato sopra: è una
  riscrittura, e l'inclusione l'avrebbe peggiorata.

## Conseguenze

- I master nuovi di ARC-08 nascono sotto il contratto e ottengono l'apparato
  gratis: si scrivono i componenti, e il foglio del cast esce da sé.
- Un'errata a un blocco statistiche si fa nel Bestiario, e
  `componenti.py --includi` la porta nei moduli. Se nessuno lo lancia, la CI
  lo segnala.
- Il primo statblocco incluso in un volume ha mostrato un difetto del
  renderer typst, già presente: gli attributi si dividevano sulle virgole, e
  94 schede su 99 li scrivono senza, quindi il riquadro stampava «For» con
  accanto tutto il resto. Corretto in `export_booklet_typst.statblocco_typ`,
  con un test.
- Il file d'apparato è un file in più per ogni master. Viene rigenerato, non
  scritto, quindi non si mantiene a mano.
- **Non** risolve la domanda più grande, cioè se il modulo si capisce: il quiz a
  due agenti del 2026-09-26 (`plans/esperimenti/quiz-def4/`) mostra che la
  missione della serata manca dagli appunti di tutti e due i lettori. Quello è
  lavoro sul contenuto, non sui componenti.
