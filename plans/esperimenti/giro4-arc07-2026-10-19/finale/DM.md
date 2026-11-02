# DM a freddo, lettura finale prima della stampa (giro 4, 2026-10-19)

Ruolo: un DM che non ha scritto niente di ARC-07 e stasera ha **un'ora** per
prepararsi. Rubrica: `skills/rumblingstone-playtest/references/dm-a-freddo.md`.
Letti nell'ordine dei capitoli il generato `ARC07-NOTTE-E-ALBA-BOOKLET.hb.md`
(intro, I regia, II Seme, III cassetta, IV DEF-4 da §0 e da §4 in avanti con le
appendici A, C e D, V la Forgia ricorda, VI Durik) e il volume dei giocatori
`ARC07-NOTTE-E-ALBA-GIOCATORI.hb.md`, poi i due PDF «STAMPA» che stanno nella
stessa cartella. Stato del gruppo da `stato-del-gruppo/` e dalla patch del
2026-10-18; decisioni da `../DECISIONI-DM.md`, «Esito».

Nessun file del repo è stato toccato. `validate_booklets.py` sui due manifest:
ok, con 2 avvisi di parità fra le catene.

## Primo passo · la vista di chi scorre

`python3 scripts/vista_di_chi_scorre.py` su `01-REGIA-SERATA.md` e su
`ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`. Le risposte sono date dalla sola vista.

| Domanda | Regia | DEF-4 |
|---|---|---|
| 1 · la serata in tre frasi | ultime scelte in fortezza, il campo andata e ritorno, l'alba con le mura e il duello; stop sull'esito. Si ricava dalla tabella del §0, perché la regia non ha un riquadro «in tre frasi» | il riquadro «La serata in tre frasi» basta, compresa la ripresa dalla notte con 3 tacche e lo stop prima della Scena 12 |
| 2 · chi si oppone | Zog'tar, Balvar, Skullcrusher, dal grassetto «Chi si oppone» | gli stessi tre, dal riquadro |
| 3 · cosa preparare | la vista non lo dice: le CD non bastano | rimanda alla regia, che è giusto |
| 4 · cosa mi ha fatto rispondere | la tabella del §0 e «Chi si oppone» | il riquadro |

Nessun `D-SERATA`, `D-AVVERSARIO` o `D-PREPARA` nuovo. Il rumore della vista di
DEF-4 (grassetti d'apparato come «Sostituisce e fonde», CD senza contesto nelle
celle delle tabelle) è già noto dai giri precedenti e non lo conto.

## Secondo passo · la preparazione in un'ora

La lista da 60 minuti della regia §1 regge: 10 + 5 + 8 + 20 + 3 + 5 + 9. Alla
fine dell'ora avevo pronto:

- **chi parla per primo**: Durin nel cortile, *«Quando uscite?»*, dopo gli echi;
- **il conto delle tacche**: 3 segnate; col volo 3 + 1 + 1 = 5, Grask sveglio
  all'atterraggio; con una tacca in fortezza (Seme o semi vegliati) Grask dorme;
- **la tenda** su M7-C: coordinate del testo e della mappa coincidono una per
  una (N2, soglia M4–N4, palo M9, seggio M12–N13, guardie K12 L10 O10 P11,
  Balvar P13, telo est S5–S13, glifo L14–N14, Grask N15, sacerdote W11);
- **il duello** su M7-B: gru B10 e W10, mura a 4,5 m, PG sulla riga 16, re a
  L16, Durik U16, wyvern W2 e X2, tutto uguale fra griglia, SVG e Scena 11.

Ho controllato in particolare i numeri toccati dalle correzioni e dalle
decisioni. Sono allineati fra statblocco, tattiche, §0-bis e regia: soffio
14d4 CD 30 (28 + Capacità Focalizzata), Soffio Aderente con ricarica +1, CA 33
e 37 con *armatura magica*, contatto 10 (le corde), CA 41 sulla runa della
Catena, lotta +40 e +20 a una parte sola, 297 pf con fuga a ~100, Presenza
CD 25 a 63 m, *Ghermire* e *Fluttuare* in uso a 15 m (decisione 6), Bane che
non vale (decisione 4), Bracieri che non rifiutano (5), *corrompere l'acqua*
su un PG con Volontà CD 25 (7), Vatore CA 22 contatto 16 (1), 1d4+2 round (2),
Zog'tar 5 minuti nel buco portatile (12), wyvern dal round 2 con EL 14 e 1.625
PX a testa (16), drago in 70 round dal corno, Cintura a 4 cariche, Torque
ancora al collo del re, i quattro tiri del dado dei caduti.

Gli handout ✉ non portano marche interne: zero `[CANONE`, `[INFERRED`,
`[Private`, «DEF-», Varis o Collezionista nel volume dei giocatori, sia nel
`.hb.md` sia nell'HTML. Ogni eco sta su una pagina sua, quindi la riga «Solo
per te» resta di chi la riceve, e la regia dice al DM di ricordarlo a voce.

Dove mi sono fermato a cercare sono i rilievi qui sotto.

## I rilievi

| # | Passo | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|
| 1 | 2 | `P-FLUSSO` | il PDF del DM pronto per la stampa è quello di prima delle decisioni | 🔴 | `-STAMPA.pdf` delle 08:36 dice «soffio … CD 28» e «Ghermire e Fluttuare … stasera non li usa» |
| 2 | 2 | `P-HANDOUT` | il ✉ del contratto del Seme non ha un momento di consegna nella regia | 🟠 | intro: «Il volume dei giocatori · gli echi della serata e le dieci boccette» |
| 3 | 2 | `P-STATO` | la benedizione dei chierici (+2/+2) manca da «Cosa hanno in mano» | 🟠 | Scena 4: «fiducia piena: … la benedizione dei chierici di Hammerfist, +2/+2 … 12 ore» |
| 4 | 2 | `P-INTERAZIONI` | la lista da un'ora non apre la tabella dei Treant | 🟠 | regia §2, punto 3, parla solo di «Hella veglia i semi» |
| 5 | 2 | `P-FLUSSO` | punteggiatura orfana dove il generatore toglie le marche | 🟡 | Scena 9: «(qui sotto).» e a capo «: compare dopo il primo box» |
| 6 | 2 | `P-INTERAZIONI` | chi legge le pergamene di cura resta «da verificare» | 🟡 | regia §1: «il mirror SRD del repo non la riporta intera: da verificare» |
| 7 | 2 | `P-HANDOUT` | le pagine «per tutto il tavolo» dicono anche «in privato» | 🟡 | «Pagina da consegnare al giocatore indicato, in privato.» sopra «Per tutto il tavolo» |
| 8 | 2 | `P-INTERAZIONI` | l'ordine fra +50% di Durik e runa d'acido non è dove punta la regia | 🟡 | regia §1: «Il soffio contro Durik è nella Scena 11, riga 4-bis» |
| 9 | 2 | `P-FLUSSO` | rimandi del capitolo II che portano a sezioni inesistenti | 🟡 | «Registra l'esito nell'**Echo Ledger** (§11)» |
| 10 | 2 | `P-DOMANDE` | trattenuta del pesatore sugli acquisti aperti di stasera | 🟡 | Scena 5: «a peso, meno una su dieci» contro «per questo conto il pesatore non ha trattenuto niente» |
| 11 | 2 | `P-FLUSSO` | la regia annuncia quattro cose e ne elenca cinque | 🟡 | regia §4: «Quattro cose da tenere davanti» |

### 🔴 1 · Il PDF «STAMPA» del DM è vecchio

**Dove**: cartella `homebrew/sessione-notte-e-alba/`, file
`ARC07-NOTTE-E-ALBA-BOOKLET-STAMPA.pdf` (08:36), che `.gitignore` tiene fuori
dal repo. Il `.hb.md` e l'HTML sono delle 08:53, dopo il commit delle decisioni.

**Prova**: dal testo del PDF, `§0-bis`: «Soffio acido in linea di 30 m, 14d4,
Riflessi CD 28 ½»; Scena 11: «Ghermire e Fluttuare sono nello statblocco ma
stasera non li usa [INFERRED — needs DM confirmation]». Nel PDF ci sono 12
marche `INFERRED`, nel `.hb.md` una sola. Il Soffio Aderente non c'è. Un DM
che stampa il file che si chiama «STAMPA» gioca il drago con le regole che la
decisione 6 ha rovesciato e con due talenti di meno, e legge marche di lavoro
in mezzo alle tattiche. Il PDF dei giocatori (08:36) invece coincide col
`.hb.md`: ha già il contratto del Seme e gli echi di adesso.

**Correzione**: rigenerare il PDF del DM dal manifest (catena typst) prima di
stampare, oppure cancellarlo e stampare dall'HTML o dal `.hb.md`.

### 🟠 2 · Il ✉ «Il contratto del Seme» non dice quando si consegna

**Dove**: intro del booklet («Come usare questo booklet»), regia §0 colonna «Si
consegna», pagina 5 del volume dei giocatori.

**Prova**: la tabella delle pagine ✉ dell'intro ha due righe, «Echi della
notte» e «Le dieci boccette»; la colonna «Si consegna» del §0 ha gli echi e le
boccette all'Atto 0 e «—» all'Atto I. L'unico posto che dice «dopo il box» è
la testa del capitolo II. La pagina stampata, sopra, porta la nota «Pagina da
consegnare al giocatore indicato, in privato», e subito sotto «Per tutto il
tavolo». Un DM che sfoglia il volume all'Atto 0 trova tre pagine «del tavolo»
e la regia gli ha appena detto di dare le boccette a tutti: il contratto esce
con loro, e il tavolo legge le otto clausole senza pergamena, senza ora e
senza tacca. È un errore introdotto stamattina: la pagina è entrata nel
manifest alle 08:34 e l'intro e il §0 non sono stati riallineati.

**Correzione**: una riga nella tabella ✉ dell'intro e nella colonna «Si
consegna» dell'Atto I: «✉ Il contratto del Seme, solo dopo l'ora della
pergamena (cap. II); se il Seme si rinvia, resta nel volume».

### 🟠 3 · La benedizione dei chierici manca da «Cosa hanno in mano»

**Dove**: regia §1, tabella «Cosa hanno in mano»; master Scena 4, Scena 6
(«Prima di uscire») e Scena 8 (Via A).

**Prova**: Scena 4, con la fiducia piena: «la benedizione dei chierici di
Hammerfist, +2/+2 (morale, al colpire e ai danni, 12 ore …)». Il gruppo ha
avuto la fiducia piena, dal consiglio all'alba passano meno di 12 ore, quindi
vale in tutti i tiri di stasera. La Via A la usa: Sapienza Magica «**gratis**
se hanno addosso la benedizione dei chierici di Hammerfist». La tabella della
regia elenca Benedizioni della Sala, Doni, pozioni e pergamene, ma questa no,
e la Scena 4 non è nella lista di lettura. Quando un giocatore chiede «ce
l'abbiamo ancora?», il DM la cerca in un atto già giocato.

**Correzione**: una riga nella tabella: «Benedizione dei chierici · +2 morale
al colpire e ai danni, 12 ore dal consiglio · tutta la notte e il duello; rende
gratis la Sapienza Magica della Via A (Scena 8)».

### 🟠 4 · I Treant alla tenda: la lista di lettura non li apre

**Dove**: regia §1 (lista da un'ora) e §2, punto 3; master Scena 5, «I Treant:
come lo viene a sapere Hella, e dove possono andare»; Appendice A.6.

**Prova**: la regia tratta i semi solo come scelta da una tacca («Hella veglia
i semi della Collana: all'alba i due Treant caricano il fianco»). La Scena 5
dice invece che per questo gruppo «i Treant restano dove la giocatrice li
vuole», con quattro posti, tenda compresa, e regole che cambiano lo scontro:
RD contro le ronde, niente Colpo Devastante su un Treant, la regola del mese
se ne chiama due di notte, la carica che manca a Durik. La lista da un'ora
legge Scene 6-11, A.1, A.2, A.4 e A.6 per le wyvern, non la tabella dei
Treant. Se la giocatrice di Hella dice «ne chiamo uno nella tenda», il DM
cerca a metà della Scena 5.

**Correzione**: aggiungere alla lista «3 · cap. IV Scena 5, la tabella "I
Treant … dove possono andare", e la riga Treant di A.6», togliendo i tre
minuti dalla Scena 6.

### 🟡 5 · Punteggiatura orfana dove si tolgono le marche

**Dove**: 24 righe del `.hb.md` del DM che cominciano con «.», «:» o «;», più
un paio di frasi monche. Due vengono dalle correzioni di oggi: Scena 7, «sta
con chi sta vincendo.: vince chi ha tolto…» (giro 4 n. 8), e Scena 9,
«come se il tavolo avesse fretta (qui sotto).» seguito a capo da «: compare
dopo il primo box della Scena 10» (giro 4 n. 11). In A.5 la frase finisce in
«va segnata come.».

**Causa**: `togli_storico` in `scripts/dmcore/testo.py` toglie la marca quando
apre una riga, ma lascia la punteggiatura che la seguiva sulla riga nuova:
`togli_storico("vale la soglia a colpi\n`[CANONE — DM]`;\nThorgrim")` dà
`'vale la soglia a colpi\n;\nThorgrim'`.

**Correzione**: in `togli_storico`, quando la marca è a inizio riga, attaccare
la punteggiatura che la segue alla fine della riga prima (con un doctest), e
rigenerare. Nelle due frasi di oggi basta spostare la marca in fondo alla
frase.

### 🟡 6 · Chi legge le pergamene di cura

**Dove**: regia §1 (riga «Pergamene») e Scena 5, «Chi legge le pergamene».

**Prova**: «Le cure e *neutralizza veleno* le legge Hella se sono sulla lista
del druido (il mirror SRD del repo non la riporta intera: da verificare)».
Confermo: in `skills/dnd-35-srd/references/spells.md` la lista del druido non
ha *cura ferite moderate*, *gravi* e *critiche* né *neutralizza veleno*. È da
verificare. Se resta aperta, il DM decide a metà duello chi legge una
pergamena da CD 25-27.

**Correzione**: controllare «Druid Spells» su d20srd.org prima della serata e
scrivere l'esito al posto di «da verificare», nei due punti.

### 🟡 7 · Le pagine «per tutto il tavolo» dicono anche «in privato»

**Dove**: volume dei giocatori, pagine «Il contratto del Seme» e «Le dieci
boccette».

**Prova**: il riquadro generato dal tag `player` dice «Pagina da consegnare al
giocatore indicato, in privato.»; il testo, due righe sotto: «**Per tutto il
tavolo.** Questa pagina non è privata».

**Correzione**: un tag diverso per le pagine del tavolo nel manifest dei
giocatori, o un testo del riquadro che non dica «in privato» quando la pagina
apre con «Per tutto il tavolo».

### 🟡 8 · Durik e la runa d'acido: la regola dell'ordine è altrove

**Dove**: regia §1, «Le schede che contano», riga Durik; master §1, Hella.

**Prova**: la regia rimanda a «Scena 11, riga 4-bis», che dice solo «l'acido
gli fa il 50% in più». L'ordine deciso (decisione 23: «prima il +50% e poi la
resistenza») sta in cap. IV §1, nel paragrafo di Hella, che non è nella lista.

**Correzione**: nella riga Durik della regia, «con la runa: prima +50%, poi
−20 (cap. IV §1, Hella)».

### 🟡 9 · Rimandi del capitolo II che portano fuori dal booklet

**Dove**: capitolo II, testo incluso da DEF-1 §6-bis.

**Prova**: «Registra l'esito nell'**Echo Ledger** (§11)», «→ **Echo Ledger
(§11)**», «Aggiorna così la nota su Vatore al #4». In questo booklet l'Echo
Ledger è cap. IV §7, e «il #4» è cap. IV.

**Correzione**: tradurre i tre rimandi in «cap. IV §7» e «cap. IV, Scena 9»,
come il generatore fa già per «DEF-n».

### 🟡 10 · La trattenuta del pesatore stasera

**Dove**: regia §2, passo 0; master Scena 5.

**Prova**: la tabella «Cosa compra» dice «Monete del 1372 · a peso, meno una
su dieci»; il conto giocato dice «per questo conto il pesatore non ha
trattenuto niente» (D43). Per le richieste aperte che si pagano stasera il
testo non dice quale delle due vale, e Artemis lo chiederà.

**Correzione**: al passo 0 della regia, «senza trattenuta, come il conto del
25 (D43)», oppure il contrario, ma scritto.

### 🟡 11 · «Quattro cose», e sono cinque

**Dove**: regia §4, Scena 11.

**Prova**: «Quattro cose da tenere davanti:» e sotto cinque punti (Cintura,
soffio e Durik, wyvern, *Ghermire* e *Fluttuare*, Aegis Fang). Il punto su
*Ghermire* è entrato con la decisione 6.

**Correzione**: «Cinque cose da tenere davanti».

## Struttura e ordine dei capitoli

Regge. L'ordine I regia, II Seme, III cassetta, IV DEF-4, V la Forgia, VI
Durik segue la serata: il Seme è la prima cosa che il tavolo chiede, la
Forgia si apre durante il duello. Il capitolo IV si stampa intero, Atto I
compreso, e l'intro e il colophon dicono di aprirlo dalla Scena 5. Le mappe che
servono stasera sono due, M7-C e M7-B, a pagina intera in Appendice D; M7-A non
è in scala e la regia lo dice, e per la breccia di Zog'tar e per la spianata
dice cosa disegnare. Le immagini citate esistono tutte ai percorsi del booklet,
tranne il logo di Homebrewery, che è un asset del sito.

🔴 1 · 🟠 3 · 🟡 7
