# Il DM a freddo — Sessione 1 dell'assedio di Hammerfist

**Chi legge**: un DM che non ha scritto il modulo e deve condurlo stasera con
quattro pregen. **Rubrica**: `freddo/dm-a-freddo.md`. **Materiale letto**,
e solo questo: `freddo/SESSIONE-1.md` (234 righe), `freddo/LIBRETTO.md` (397),
`freddo/HANDOUT-PREGEN.md` (227), `freddo/SEGRETI-DM.md` (66). Non ho letto
PLAYTESTER, LETTORE, DEVELOPER né nessun file che i quattro citano.

**Tempo di preparazione dichiarato**: un'ora. I quattro file insieme sono
circa 920 righe; la lettura completa prende 35-40 minuti, il resto va in
appunti. Ci sto dentro, ma solo perché ho rinunciato a ricostruire le cose che
mancano (statblocchi, mappe, abilità dei pregen): quelle restano rilievi.

**Scostamento dalla rubrica, dichiarato.** La rubrica chiede la lettura a scene
con `lettura_a_scene.py` e il terzo passo con un agente nuovo. Il primo passo
l'ho fatto con lo script; i quattro file li ho letti per intero (sono quattro
documenti, non un master solo, e lo script ne serve uno). Il terzo passo lo
faccio io rispondendo alle tre domande dopo aver chiuso gli appunti: non è
indipendente, e lo segno.

Riferimenti: `S1` = `freddo/SESSIONE-1.md`, `LIB` = `freddo/LIBRETTO.md`,
`HO` = `freddo/HANDOUT-PREGEN.md`, `SEG` = `freddo/SEGRETI-DM.md`, col numero
di riga.

---

## Primo passo · la vista di chi scorre

`python3 scripts/vista_di_chi_scorre.py freddo/SESSIONE-1.md`:

- **LA SERATA: il master non la dichiara.** Nessun riquadro «La serata in tre
  frasi», nessun Quickstart.
- Le scene, la prima frase: **vuota**. Lo script non trova righe «In scena».
- I primi grassetti sono il titolo del capitolo di un altro documento
  (`4. CAPITOLO 2: LA CAMPAGNA - SCONTRO PER SCONTRO`), `📎 Regia (A5)`,
  `Griglia ultra-clear:`.
- Le CD sono tutte prove d'abilità (Intimidire 18, Osservare 20,
  Sopravvivenza 22, Nascondersi 22, Diplomazia 18/16, Artigianato 20,
  Sapienza Magica 22…).

Le quattro risposte, dalla sola vista:

1. **Cosa succede stasera.** «Tre giorni prima di un assedio: una ricognizione
   del campo nemico, un consiglio di guerra, i preparativi alle difese.» La
   vista **non mostra** la scaramuccia dell'avanguardia del libretto (§13),
   che secondo il libretto è il cuore meccanico della serata. → `D-SERATA`.
2. **Chi si oppone.** «La Mano Rossa.» Chi la comanda e cosa vuole: non lo so.
   → `D-AVVERSARIO`.
3. **Cosa preparo.** «Le mappe di Hammerfist (file esterno), un elenco di CD.»
   La vista non dice: le schede pregen, il libretto, i dadi rossi e bianchi, i
   fogli dei PFU, il mazzo dell'orda. → `D-PREPARA`.
4. **Cosa mi ha fatto rispondere.** I titoli FASE 1/2/3 e la lista di CD. Il
   primo grassetto è il titolo di un capitolo che non esiste in questo file.
   → `D-RUMORE`.

---

## Secondo passo · la preparazione, scena per scena

Per ogni rilievo: dove, gravità, cosa manca, cosa farei al tavolo
(`P-RILIEVI`: il problema risolto, non solo elencato) e cosa avrei voluto
trovare.

### A. Dove sta la serata: due sessioni 1 diverse

**R1 · 🔴 · `S1` 27-229 contro `LIB` 359-363 · `D-SERATA`, `P-FLUSSO`.**
`SESSIONE-1` è la sessione dell'avvistamento: 1A ricognizione, 1B consiglio,
1C rafforzare le difese, 1E presagi, 1F il drago. Il libretto dice che nella
Sessione 1, «dopo l'avvistamento, il giorno prima che l'orda arrivi alle
mura», si gioca la scaramuccia dell'avanguardia (§13) ed «è la prima volta che
si tira». In `SESSIONE-1` la scaramuccia **non c'è**: nessun titolo, nessun
box, nessun rimando a `LIB` §13. Non so dove metterla e non so se sostituisce
1C (che fa la stessa cosa, preparare le difese, con un altro sistema).
- *Al tavolo*: la metto fra 1F (alba dell'ultimo giorno di pace) e 1E (la
  notte prima), cioè «prima di sera» del giorno prima, e **tolgo 1C**: le
  trappole di §13 sono le difese preparate.
- *Avrei voluto*: in `S1`, dopo 1F, un «Incontro 1G: l'avanguardia → giocala
  con `LIB` §13 e `SEG` §2», con una riga che dice che 1C è sostituito.

**R2 · 🔴 · `S1` 182-195 e 231-234 contro `LIB` 151-158, 387-390, `SEG`
64-66 · `P-CONGEGNI`.** Due sistemi di esito che non si parlano. 1C dà «+2 CA
alle mura», «+2 danni alle unità nemiche», «+1 morale», «−1 al primo
assalto»; i Risultati chiedono «morale iniziale da −2 a +4» e «CA delle
fortificazioni da 23 a 27». Il libretto invece fa partire il morale da **+1**
(`LIB` 154), non ha CA delle mura (`SEG` 64-66: «la breccia si misura con le
tacche»), e misura le difese preparate col numero di trappole. A fine serata
non so cosa scrivere sul foglio per la Sessione 2.
- *Al tavolo*: scrivo solo il numero di trappole, le squadre travolte e il
  morale. Traduco il morale di `S1` così: parte da +1, il consiglio (1B) o
  l'eloquenza di Nala possono portarlo a +2, una figuraccia col drago (1F) a
  0. È un'invenzione mia.
- *Avrei voluto*: i Risultati di `S1` riscritti nei termini del libretto:
  *trappole N · morale della rocca M · bonus dell'avvistamento (quali) ·
  sergente fuggito sì/no*.

**R3 · 🔴 · `LIB` 238 contro `LIB` 361-363.** Il libretto si contraddice:
in §9 «Nella Sessione 1, dove la battaglia campale non c'è», in §13 «nella
Sessione 1 … questa è la prima volta che si tira». Per chi non vuole il
pregen cambia tutto (vedi R18).
- *Al tavolo*: vale §13, la battaglia c'è.
- *Avrei voluto*: §9 corretto: «nella Sessione 1 la battaglia campale è
  solo l'avanguardia (§13)».

**R4 · 🟠 · `S1` 199-212 · `P-FLUSSO`.** La cronologia della Fase 3 è
rovesciata: 1E è «la notte prima dell'assalto», 1F «l'alba dell'ultimo giorno
di pace», che viene prima di quella notte. Letti in ordine di pagina, il drago
arriva dopo la notte dei presagi.
- *Al tavolo*: 1F → avanguardia → 1E, e la sessione chiude sulla notte dei
  fuochi.
- *Avrei voluto*: l'ordine giusto, e una riga di chiusura (la scena su cui si
  spegne la serata).

**R5 · 🟡 · `S1` 27, 41, 75, 115, 180, 199.** Tre «FASE 1», due «FASE 2»,
due «FASE 3»: le fasi della sessione e le fasi dell'incontro 1A hanno gli
stessi nomi. L'incontro 1D non c'è (da 1C a 1E). Al tavolo «torno alla Fase 2»
non mi dice dove tornare.

**R6 · 🟡 · `S1` 5, 16-20, 47, 82, 122, 214-224.** Il file è un estratto: il
primo titolo è «4. CAPITOLO 2», e ci sono sette rimandi a file che non ho
(`ARC08-16-CUE-SONORI`, `ERRATA-ARC08-…`, `Mappe/Hammerfist-L1-…`,
`PortaleForgia-P5-…`, `ARC08-10`). Anche gli altri file chiamano i compagni
con altri nomi: il libretto è `ARC08-18`, i segreti `ARC08-19-SEGRETI-DELL-
ORDA.md` (`LIB` 6, `SEG` 3). Un DM a freddo cerca file che non esistono.

### B. L'avvistamento e il consiglio (`S1` 9-178)

**R7 · 🔴 · `S1` 69, 144-158, 177-195 contro `HO` 67-114 · `D-PREPARA`.**
Tutta la prima metà della serata si regge su prove d'abilità (Nascondersi,
Muoversi Silenziosamente, Osservare CD 20, Sopravvivenza CD 22, Intimidire
CD 18, Conoscenze Religione CD 18, Nascondersi CD 22, Diplomazia CD 18,
Artigianato Pietra CD 20, Sapienza Magica CD 22), e **le schede dei pregen non
hanno abilità**. Niente gradi, niente modificatori, e mancano anche
caratteristiche (Borin non ha Int, Sag, Car; Dara non ha Int e Car; Thorin non
ha Des e Int sulla riga; Nala non ha For, Int, Sag). Niente lingue: «Linguaggi
(parlare Orco/Goblin)» (`S1` 158) in 3.5 non è una prova, è sapere o no la
lingua, e la scheda di Nala non lo dice. Niente penalità d'armatura per Borin
in armatura completa che deve muoversi in silenzio.
- *Al tavolo*: invento i modificatori dal livello. Classe d'abilità con gradi
  pieni = livello + 3 + caratteristica: Dara Osservare/Sopravvivenza/Nascondersi
  circa +17/+17/+19, Nala Nascondersi/Ascoltare/Raggirare circa +19/+15/+19,
  Thorin Conoscenze Religione circa +17, Borin Intimidire +10 (con Car 10
  ipotetico) e Muoversi Silenziosamente −6. Dico che Nala parla l'orco e il
  goblin perché è la spia. Tutto inventato, e lo dico ai giocatori come
  «numeri provvisori».
- *Avrei voluto*: su ogni scheda una riga **Abilità** con le 6-8 che la
  serata usa, già calcolate, più lingue e le tre caratteristiche mancanti.

**R8 · 🔴 · `S1` 60-69, 103-105, 144-146 · `D-PREPARA`.** Nessun avversario
dell'avvistamento ha statistiche: la pattuglia «3 Orchi su Worg», gli scout
hobgoblin «1 Sergente, 9 guerrieri». L'azione primaria di Borin è «eliminare
silenziosamente la pattuglia» (`S1` 145): è un combattimento previsto, non un
incidente. Le mappe tattiche sono nel file `Mappe/…` che non ho; le ASCII hanno
scale diverse da quelle citate (`S1` 49 «5 metri» contro 47 «1,5 m»). Il LS
«da 5 a 12» (`S1` 38) contro pregen di GS 12-13 dice che lo scontro è facile,
ma non quanto.
- *Al tavolo*: orchi = orco guerriero 3° dell'SRD sui worg dell'SRD; scout
  hobgoblin = hobgoblin guerriero 2°, il sergente come in `SEG` 43-45
  (guerriero 6°, armatura completa: CA 21 circa, 55 pf circa, +11 a colpire).
  Lo scontro con la pattuglia lo risolvo in due round a tiri liberi, senza
  mappa.
- *Avrei voluto*: tre righe di statblocco in fondo a 1A (orco su worg, scout,
  sergente), e cosa succede se scappa un orco.

**R9 · 🟠 · `S1` 69, 109, 142-163 · `P-CONGEGNI`.** La ricognizione ha i
successi (`S1` 160-163) ma non i fallimenti. Se la pattuglia li vede, se Nala
è scoperta, se Dara sbaglia l'Osservare: cosa succede? Allarme? Inseguimento?
Si perde «Eliminazione silenziosa» e basta? «Livello di Sfida variabile»
promette una scala che il testo non dà.
- *Al tavolo*: scoperti = la pattuglia suona il corno, i pregen devono
  ritirarsi; il bonus «Intelligence completa» si dimezza (+1) e l'orda «adotta
  contromisure» (per me: l'avanguardia di §13 arriva un round prima).
- *Avrei voluto*: una scala a tre gradini (pulito · visti ma via · scontro) con
  l'effetto di ognuno sulla scaramuccia e sull'assedio.

**R10 · 🟠 · `S1` 115-140 · `P-CONGEGNI`, `D-AVVERSARIO`.** Il momento più
bello dell'avvistamento (Dara col cannocchiale sul campo nemico) non ha
read-aloud. La mappa nomina Grimjaw, Gorthak, l'Ettin, i giganti, il Dragone,
chierici e sciamani, «migliaia di orchi e hobgoblin»: chi siano Grimjaw e
Gorthak e cosa vogliano non è scritto in nessuno dei quattro file. `SEG` 42 dà
solo «Grimjaw è sulla cresta e non scende»; `S1` 206 dice che ha «magia
demoniaca». Non so cosa vede Dara a CD 20, cosa a CD 25, cosa se fallisce.
- *Al tavolo*: tre gradini inventati. Fallito: «sono più di quanti sappiate
  contare». CD 20: i numeri (sette a uno, come dirà la Madre Superiora) e i
  giganti. CD 25: la tenda di Grimjaw, Gorthak il bruto davanti alle
  catapulte, un'ombra nera sopra la palude (il drago). Gorthak lo descrivo come
  il comandante dell'assalto al cancello perché il libretto lo mette lì
  (`LIB` 331).
- *Avrei voluto*: un box «Cosa vede Dara» a gradini, e due righe per Grimjaw e
  Gorthak: aspetto, cosa vogliono, come parlano.

**R11 · 🟠 · `S1` 167-178 · `P-STATO`, `P-INTERAZIONI`.** Il Consiglio di
Guerra ha quattro «decisioni strategiche» senza opzioni né effetti, due CD
senza conseguenza scritta, e due PNG (Re Thorek, Madre Superiora Dana) senza
una riga di carattere. Nessuno dei due ha una prima battuta oltre al box. Il
box poi parla ai PG della campagna, non ai pregen: «voi, gli eroi leggendari
tornati in tempo per questa ora buia» (`S1` 169). I pregen non sono mai
partiti: Borin è il nipote del re (`HO` 69), Thorin il consigliere spirituale
(`HO` 96).
- *Al tavolo*: riscrivo la frase («…e voi quattro, gli eroi di Hammerfist»).
  Uso il consiglio per la cosa che il libretto chiede e nessuno dice: **chi
  tiene quale settore** (`LIB` 38-45) e quante squadre di guastatori escono
  domani. È il ponte naturale fra la scena di ruolo e le regole.
- *Avrei voluto*: una riga per PNG (cosa vuole, cosa teme, come parla) e
  l'indicazione che le «decisioni» del consiglio sono la tabella «chi tiene
  cosa» del libretto.

**R12 · 🟠 · `S1` 27-32.** «Il Rapporto delle Sentinelle», primo evento
chiave, non ha testo. Nemmeno l'aggancio di 1A: chi manda i quattro in
ricognizione, e perché proprio loro?
- *Al tavolo*: è il re, al termine del rapporto; li manda perché Dara conosce
  il crinale.

**R13 · 🟡 · `S1` 205-208.** «Se presente un Warlock / un Druido / un
Monaco»: nessuno dei quattro pregen lo è (guerriero, ranger, chierico, bardo),
e il warlock non è una classe del manuale base 3.5. Il testo è stato scritto
per un altro gruppo. Al tavolo lo giro: Thorin sente lo zolfo (Grimjaw), Dara
vede gli animali fuggire.

**R14 · 🟠 · `S1` 210-229 · `P-CONGEGNI`.** 1F offre tre opzioni, la prima
è «attaccare il drago», e Borin ha scritto in scheda «gettati per primo nella
mischia» (`HO` 70). Fauci di Palude non ha statistiche, l'opzione non ha
conseguenze, nessuna delle tre ha un effetto. La nota del carry-over (`S1`
214-224) parla di Thorik, del P5 e di Aegis Fang: a un DM a freddo dice solo
che c'è qualcosa che non ha letto.
- *Al tavolo*: il drago è a 150 m d'altezza, fuori tiro anche per l'arco
  lungo di Dara (120 m d'incremento, tiro a −2 ma possibile: lo lascio
  tentare, colpisce, il drago non se ne cura). Magia: Thorin con *Colpo
  infuocato* arriva a 66 m, non lo raggiunge, ma la colonna di fuoco vista dai
  nani dà +1 morale. Ignorare: nessun effetto. Attacco sconsiderato: −1 morale
  se qualcuno si fa male.
- *Avrei voluto*: per ognuna delle tre opzioni un effetto sul morale della
  rocca del libretto.

### C. La scaramuccia dell'avanguardia (`LIB` §13, `SEG` §2)

**R15 · 🟠 · `LIB` 365-385 e `SEG` 37-41 · `P-CONGEGNI`.** Il mazzo
dell'avanguardia non c'è. Il libretto ha un mazzo per l'assedio (`LIB` 308-310,
quattordici reparti per settore), i segreti hanno tre carte per i round 1-2, 3
e 5. Restano aperti: se i lupi del round 1 vengono distrutti, ne arriva un
altro al round 2? Cosa riempie il fronte di due dal round 3 in poi, quando gli
hobgoblin muoiono? Cosa arriva ai round 4 e 6? Quale ferocia (§12 la chiede
«prima della battaglia»; §13 dice che le prove usano la feroce)?
- *Al tavolo*: ferocia feroce. Per squadra: round 1-2 un reparto di lupi, che
  si rimpiazza se muore; dal round 3 il fronte si riempie pescando da un
  mazzo piccolo per squadra (2 hobgoblin, 1 guerrieri, 1 orchi). Il sergente
  vale per tutta l'avanguardia.
- *Avrei voluto*: in `SEG` §2 il mazzo dell'avanguardia scritto come quello
  dell'assedio, quattro righe.

**R16 · 🟠 · `LIB` 76-77, 151-170, 373-382 · `P-CONGEGNI`.** Le regole
dell'assedio valgono «con un ordine in più», ma tre di esse non si sa se
valgono fuori dalle mura: il **+1 al bianco del primo giorno** (le squadre sono
«sul pendio, senza merlature», e non è ancora il primo giorno); il **morale
della rocca** (parte da +1 qui? una squadra travolta fa −1?); l'**eroe ferito**
con 3d6 (sì, credo). E il conto delle tacche è per squadra, mentre nell'assedio
è per settore.
- *Al tavolo*: niente +1 del primo giorno; il morale vale ed è +1 (o quello
  uscito dal consiglio); una squadra travolta fa −1; tacche per squadra.
- *Avrei voluto*: tre righe in §13: «vale · non vale».

**R17 · 🔴 · `LIB` 383-385, `SEG` 43-46 · `D-PREPARA`.** La retroguardia è
l'unico combattimento «sulla mappa» che la serata promette, ed è contro il
sergente hobgoblin. Il sergente ha mezza riga («guerriero di 6° livello con
l'armatura completa»), niente pf, CA, attacco, talenti; la mappa del pendio
non c'è; «poi scappa (o no)» non dice cosa succede se l'eroe resta, né se il
sergente fugge sotto metà pf come i comandanti (`LIB` 141-143). E cosa succede
se un pregen muore: `HO` 30-32 dice «quello che i quattro perdono, lo trovano
perso», ma le Sessioni 2-3 con quale scheda le gioca quel giocatore?
- *Al tavolo*: sergente hobgoblin guerriero 6°: CA 21, 55 pf, spadone +11
  (2d6+6), Attacco Poderoso. Contro Borin (+21, 142 pf) dura due round: lo
  faccio fuggire a metà pf come un comandante, e il sergente esce dalla carta
  del round 3. Un pregen morto: il giocatore passa al capitano (modo C).
  Tutto inventato.
- *Avrei voluto*: lo statblocco del sergente in `SEG` §2, un rettangolo di
  pendio 12×12 quadretti, e una riga sulla morte di un pregen.

**R18 · 🟡 · `LIB` 373-375 e `SEG` 23.** Scavare dà −2 al bianco, i lupi
Sbilanciare un altro −2: una squadra di veterani che scava contro i lupi tira
d20+17 contro 31 e non perde PFU solo con 14 o più. È dentro le prove («il
round in più è una scommessa»), ma il DM deve saperlo per non sembrare
crudele: lo dico ai giocatori prima del primo round.

**R19 · 🟡 · `LIB` 1-36, 258-261.** Il libretto dice «i dadi li tirate voi»
(`LIB` 29-31), poi nell'esempio il macigno dei giganti «è un tiro diretto del
DM» (`LIB` 259). Non è sbagliato, ma lo noto quando lo spiego.

**R20 · 🟡 · `SEG` 15-16 contro `LIB` 66-72.** «Il DM le applica senza
annunciarle»: ma i giocatori tirano il bianco contro «22 + AU del nemico», e
l'AU la sanno dal libretto (§11). Se gli orchi caricano a +1 devo dire il
numero, quindi lo annuncio. Lo risolvo dicendo sempre il bersaglio («stavolta
contro 32») e raccontando il perché solo la prima volta (`SEG` 26-33).

### D. I pregen e chi non li vuole (`HO`, `LIB` §9)

**R21 · 🟠 · `LIB` 231-240, `HO` 49-51 · chi non vuole il pregen.** Le due
strade ci sono e sono buone (capitano, orda). Per stasera però:
- il **capitano** nella Sessione 1 «guida la pattuglia di nani che accompagna
  gli eroi (prove di gruppo, nessuna scheda)»: la pattuglia non ha numeri e
  le prove di gruppo non sono scritte. In §13 il capitano (modo C) ha tre
  reparti: per la scaramuccia, una squadra o tre?
- se a rifiutare è chi dovrebbe giocare **Dara**, l'avvistamento perde il suo
  perno (Osservare dal torrione, `S1` 109, 117, 140) e il suo pregen «lo muove
  il DM, senza tiri».
- chi sceglie **l'orda** gioca «gli esploratori della Mano Rossa»: senza
  scheda. Nella scaramuccia pesca le carte e dà voce a Gorthak e Grimjaw: deve
  leggere `SEG`? Se sì, sa cose che gli amici non sanno; se no, non sa cosa
  fanno le carte.
- il ripiego per il tavolo che non vuole i pregen sta in `ARC08-10` §5.5, che
  non ho.
- *Al tavolo*: il capitano ha una squadra in più nella scaramuccia (di
  veterani) e nell'avvistamento tira le prove di gruppo a +8 piatto. Se rifiuta
  chi deve fare Dara, do Dara a un altro e chi rifiuta fa il capitano. A chi
  gioca l'orda do solo `SEG` §2 (le carte), non §1 né §3.
- *Avrei voluto*: un riquadro «chi non vuole il pregen, stasera» con le
  prove di gruppo della pattuglia e quale parte di `SEG` dare al giocatore
  dell'orda.

**R22 · 🟡 · `HO` 46-48 e 23-28.** La proposta «chi gioca chi» è per il
gruppo dei Rumbling Stones (Thorik, Hella, Tordek, Artemis). Va bene per il
tavolo della campagna; per un tavolo nuovo l'handout 0 intero (la visione
della Corona, «i vostri personaggi non rischiano niente») non ha senso, e non
c'è una presentazione alternativa per una serata con soli pregen.

**R23 · 🟡 · `HO` 61-62, 159-200.** «Una pagina l'una»: la carta di Thorin ha
34 righe di incantesimi e da sola fa due pagine. Va bene, ma per la stampa
conta.

**R24 · 🟡 · `HO` 151, 182 contro `LIB` 126-136.** Non è chiaro se lanciare
*Grazia del Gatto* o *Potere Divino* consuma il gesto del round (il gesto
Incantesimo vale solo dal 3° livello). La carta dice «Combattere +21 per un
round», che suggerisce lancio e colpo nello stesso round di battaglia (un
minuto ne contiene dieci). Al tavolo dico di sì: lancio gratis, poi Combattere.
Anche *Guarigione* (`HO` 169) cura un bersaglio solo ma vale «+1d4 PFU a un
reparto», come una cura di massa: lo accetto.

**R25 · 🟡 · `HO` 79-89, `S1` 117.** Dara usa «il suo cannocchiale» (`S1`
117) che sulla scheda non c'è; Nala è «Spia Maestra 4°» senza nessuna capacità
di classe sulla carta. Non bloccano, ma i giocatori chiedono.

### E. Il confine fra quello che sanno i giocatori e quello che so io

**R26 · 🟠 · `LIB` 306-356 contro `LIB` 3-6, 202-203 e `HO` 49-50 ·
`P-CONFINE`.** Il libretto è «lo stesso per tutti» (`LIB` 3), dice che quello
che l'orda sa fare «lo scoprirete sul campo» (`LIB` 202-203), e poi in §12
«Per il DM» elenca ai giocatori tutte le carte dell'orda (giganti, Gorthak,
palla di fuoco, breccia del cancello, Grimjaw, il soffio del drago, la
ritirata al terzo giorno), le probabilità di vittoria per ferocia e gli
obiettivi della tabella dei bonus. L'handout 0 dice che «la posta, in numeri…
non va data ai giocatori». Se distribuisco il libretto intero, la sorpresa del
soffio del terzo giorno e la ritirata sono bruciate stasera.
- *Al tavolo*: le copie dei giocatori sono §1-§11 e §13; §12 lo tengo io.
  «Quanto restare» (`LIB` 392-395) lo lascio: serve alla scelta di ritirarsi.
- *Avrei voluto*: §12 spostato in `SEG`, o una riga in testa al libretto
  «§12 non va nelle copie dei giocatori».

---

## Cosa stampare e avere sotto mano

**Per i giocatori** (quattro):
- l'handout 0 (`HO` 1-28, **senza** la Nota DM 36-51): una copia, o lo
  leggo io;
- le schede 1-4 con la loro carta dei poteri (`HO` 67-227): Borin, Dara e
  Nala una pagina e mezza, Thorin due e mezza;
- il libretto `LIB` §1-§11 e §13, senza §12 (R26): circa sei pagine, una
  copia ogni due giocatori basta;
- un **foglio dei reparti** con i quadratini dei PFU e le tacche: il libretto
  lo chiede (`LIB` 34-36) e **non c'è**. Lo devo fare io (🟠, `P-HANDOUT`);
- due d20 di colore diverso a testa: otto d20 in tutto, quattro rossi e
  quattro bianchi. Non tutti i tavoli li hanno: va detto la settimana prima.

**Per me**:
- `S1` intero, con a margine l'ordine giusto delle scene (R1, R4);
- `SEG` (due pagine);
- `LIB` §12 e §13;
- **un foglio mio** con quello che ho inventato: abilità dei pregen (R7),
  tre statblocchi (R8, R17), la scala dei fallimenti (R9), il box di Dara
  (R10), il mazzo dell'avanguardia (R15), le tre righe «vale/non vale» (R16);
- un tracciatore dell'orda: quattro squadre, fino a due reparti nemici
  ciascuna, coi PFU. Non c'è (🟠, `P-HANDOUT`);
- carta quadrettata per la retroguardia e per l'eventuale scontro con la
  pattuglia: le mappe vere sono in un file che non ho (🟠, `P-IMMAGINI`).

## Dove devo cercare in tre file insieme (`D-SALTO`)

**R27 · 🟠.** Il caso peggiore è la scaramuccia: le regole del round in `LIB`
§2-§5, i numeri in `LIB` §11, le regole speciali in `LIB` §13, le carte in
`SEG` §2, le capacità dei reparti in `SEG` §1, il sergente in `SEG` 43-45 (e
il resto inventato), e la scena non è in `S1`. Durante il round tengo aperti
tre fogli e il mio. La seconda è la retroguardia: `LIB` 383-385 per la regola,
`LIB` 137-143 per il comandante che fugge (vale anche per il sergente?),
`SEG` 43-46 per chi è. La terza è il consiglio, dove `S1` 171-178 non dice
che la decisione vera è la tabella `LIB` 38-45.
- *Avrei voluto*: **una pagina dell'avanguardia** per il DM: scena, mazzo,
  carte per round, sergente, cosa porta all'assedio. Tutto quello che c'è già,
  messo in un posto.

## I primi cinque minuti, quello che direi

Nessun file dice come si apre la serata: `HO` 3 dice «subito dopo il box dello
strappo» di un altro master che non ho, `HO` 57 «all'inizio della Sessione 1,
insieme al libretto», `S1` 10 un box «da leggere la sera prima
dell'avvistamento» (in gioco, non la sera prima nel mondo reale: l'ho dovuto
rileggere). L'ordine lo decido io (🟠, R28 qui sotto).

1. **Minuto 0-1, fuori gioco.** «Stasera e per le prossime due serate non
   giocate i vostri personaggi. Li ritroverete dove li avete lasciati, senza
   un graffio. Giocate quattro nani di Hammerfist, tre giorni prima che
   arrivi l'orda.»
2. **Minuto 1-2.** Leggo il box della visione della Corona (`HO` 12-20).
3. **Minuto 2-4.** Le quattro regole in chiaro (`HO` 25-34), poi le schede:
   le metto sul tavolo, a faccia in su, e propongo l'assegnazione di `HO`
   46-48. Chi non vuole un pregen me lo dice adesso (vedi R21).
4. **Minuto 4-5.** Spengo le luci, parte il basso continuo, e leggo il box
   dell'odore (`S1` 12-14) e poi l'introduzione (`S1` 23).

Il libretto **non** lo spiego adesso (R29).

**R28 · 🟠 · `HO` 3, 57; `S1` 10, 22 · `P-FLUSSO`.** Tre file dicono tre
momenti diversi per la stessa apertura. *Avrei voluto*: in testa a `S1` un
riquadro «Apertura» con l'ordine: handout 0 → schede → box → introduzione.

## Come spiego il libretto

**R29 · 🟠 · `LIB` 3-4, 362-363 · `D-TEMPO`, ritmo.** Il libretto dice di
leggerlo «insieme all'inizio della Sessione 1». Ma la prima battaglia campale
arriva dopo l'avvistamento e il consiglio, cioè a due ore dall'inizio. Leggere
quattrocento righe di regole prima del primo dado ferma la serata prima che
parta, e alla scaramuccia nessuno se le ricorda più.

Quello che farei:
- **all'inizio**, trenta secondi: «più tardi, stasera, guiderete i vostri
  soldati; vi spiego come quando succede»;
- **prima della scaramuccia**, dieci minuti, in piedi, coi dadi in mano:
  1. §1 a voce: reparto, AU, DU, PFU; il rosso è il tuo colpo, il bianco è il
     colpo del nemico che pari tu;
  2. §3 la tabella unica, sul tavolo, a faccia in su: è l'unica cosa da
     guardare;
  3. §4 gli ordini, e il quarto ordine di stasera, Scavare;
  4. §5 i gesti: Combattere e Comandare; Incantesimo solo per Thorin e Nala;
  5. §7 la tacca: «se nel round togliete meno di 2 PFU, l'orda avanza; alla
     terza tacca la vostra squadra scappa»;
- poi il primo round lo giochiamo **lentamente**, tutti insieme, come
  l'esempio di `LIB` §10. Dal secondo si va.
- §6 (morale), §8 (la notte), §9 (i modi) li tengo per la Sessione 2.

*Avrei voluto*: nel libretto una riga «cosa spiegare stasera, cosa la prossima
volta», e una scheda riassuntiva da una facciata per il tavolo (la tabella
unica + ordini + gesti + tacca).

## Quanto dura la serata

**R30 · 🟠 · `S1` tutto · `D-TEMPO`.** `S1` non dà una durata a nessuna scena
né alla serata, e non dice cosa tagliare. L'unico tempo scritto è la mezz'ora
della scaramuccia (`LIB` 397) e i tre-quattro minuti a round (`LIB` 276-277).
La mia stima, con i rimedi qui sopra:

| Blocco | Stima | Cosa taglio se sono in ritardo |
|---|---|---|
| Apertura, schede, box, introduzione | 15' | niente |
| 1A ricognizione (tre fasi, prove, forse la pattuglia) | 45-60' | lo scontro con la pattuglia: lo risolvo a racconto |
| 1B consiglio | 25-30' | le quattro «decisioni»: resta solo chi tiene quale settore |
| pausa | 10' | |
| spiegazione del libretto | 10-15' | (se lo leggessi tutto, 40-45') |
| scaramuccia dell'avanguardia, 4-6 round | 30-40' | i round 5-6: suono il corno di Grimjaw al 4 |
| retroguardia (se qualcuno resta) | 15' | il duello a tre round, poi il sergente fugge |
| 1F il drago, 1E la notte dei fuochi, risultati | 20' | 1E diventa il box e basta |
| **Totale** | **3h10 – 3h45** | **con il libretto letto tutto all'inizio: oltre le 4h** |

*Avrei voluto*: una riga di durata per ogni incontro e la scena da tagliare.

## Dove si ferma il ritmo

1. **La lettura del libretto a inizio serata** (R29). È la sosta più lunga e
   la più evitabile.
2. **Le prove dell'avvistamento senza abilità** (R7): ogni prova è «quanto ho
   in Osservare?» «aspetta che lo calcolo». Quattro pregen, una decina di
   prove: cinque-dieci minuti persi a inventare.
3. **Il consiglio senza opzioni** (R11): quattro decisioni astratte e due PNG
   senza voce. Il tavolo discute in vuoto. Si salva solo se la decisione è
   concreta (i settori).
4. **1C se lo si gioca** (R1, R2): una lista di prove con effetti che il
   libretto non usa. Lo tolgo.
5. **Il primo round della scaramuccia**: quattro squadre, un fronte di uno,
   due colori di dadi, tutto nuovo. È la sosta *giusta* (si impara), ma dal
   round 3 il fronte raddoppia e io devo tenere otto reparti nemici senza un
   tracciatore (R15, R27).
6. **«Attacchiamo il drago»** (R14): senza statistiche né conseguenze mi
   fermo a decidere cosa succede, con Borin che ha in scheda di farlo.

---

## Le undici voci della preparazione (D12)

| Codice | Esito | Nota |
|---|---|---|
| `P-RILIEVI` | fatto | ogni rilievo qui sopra ha la sua risposta al tavolo |
| `P-GRUPPO` | **manca nel materiale** | cosa sanno i giocatori dei Rumbling Stones dell'orda e di Hammerfist non è nei quattro file; `HO` 3-10 presuppone `ARC07-DEF-5`, che non ho |
| `P-MONDO` | in parte | l'orda avanza per conto suo (tre giorni, `S1` 27, 180, 199); il drago si mostra; Grimjaw guarda dalla cresta (`SEG` 42). Cosa fa l'orda se la ricognizione è scoperta: non scritto (R9) |
| `P-STATO` | in parte | i pregen sì (`HO`), salvo abilità (R7); il re, la Madre Superiora, Grimjaw, Gorthak no (R10, R11) |
| `P-STILE` | **manca nel materiale** | nessuna descrizione fissata dei quattro nani né dei PNG, nessuna immagine nei quattro file |
| `P-IMMAGINI` | rilievo | le mappe tattiche sono in un file esterno (`S1` 47, 82, 122); il pendio della scaramuccia non ha mappa (R17) |
| `P-HANDOUT` | rilievo | il foglio dei reparti (`LIB` 34-36) e il tracciatore dell'orda non ci sono |
| `P-FLUSSO` | rilievo | la scaramuccia non è in `S1` (R1), la Fase 3 è in ordine rovesciato (R4), l'apertura in tre versioni (R28) |
| `P-DOMANDE` | fatto, sotto | |
| `P-CONGEGNI` | rilievo | tacche, trappole, ritirata e retroguardia sono chiari; il mazzo dell'avanguardia no (R15); 1A, 1B, 1F non hanno esiti (R9, R11, R14) |
| `P-INTERAZIONI` | in parte | la visione della Corona e la Mente Vuota di Thorik (`HO` 44-45, `[INFERRED]`) e il carry-over del P5 (`S1` 214-224) chiedono file che non ho |
| `P-CONFINE` | rilievo | §12 del libretto nelle mani dei giocatori (R26); il giocatore dell'orda e `SEG` (R21) |

### `P-DOMANDE` · le domande che i giocatori faranno

| Domanda | Risposta | Dove |
|---|---|---|
| Quanti sono? | sette a uno | `S1` 169 |
| Chi li comanda? Chi è Grimjaw? | «un generale con magia demoniaca»; il resto non c'è | `S1` 206, `SEG` 42 — **manca** |
| Quanto ho in Osservare / Nascondersi? | non c'è | **manca** (R7) |
| Nala parla l'orco? | non c'è | **manca** (R7) |
| Posso usare *Silenzio* per la pattuglia? | sì, 6 m, 12 round | `HO` 192 |
| Le baliste arrivano al drago? | no | `S1` 212 |
| Se restiamo un round in più? | con la feroce, dopo il 3°-4° in media 5 trappole; al 6° 2 trappole e tre squadre perse | `LIB` 392-395 |
| A cosa servono le trappole? | ognuna annulla una tacca del primo giorno | `LIB` 200, 387-390 |
| Se il mio nano muore? | «lo trovano perso»; con cosa gioco poi, non c'è | `HO` 31-32 — **manca** (R17) |
| I nostri veri personaggi cosa rischiano? | niente | `HO` 28-29 |
| Quanto dura un round di battaglia? | un minuto | `LIB` 27 |
| *Grazia del Gatto* mi costa il gesto? | non chiaro | R24 |

---

## Terzo passo · il giorno dopo, al tavolo

Senza un agente nuovo: rispondo io dopo aver chiuso gli appunti, quindi la
prova non è indipendente.

- **Chi entra per primo in scena, e cosa dice?** Il narratore col box
  dell'odore; il primo PNG che parla è la Madre Superiora Dana, al consiglio
  («La situazione è grave…», `S1` 169). Prima di lei, nel rapporto delle
  sentinelle e nell'invio in ricognizione, non parla nessuno: il primo PNG
  della serata **l'ho inventato io** (il re che manda i quattro, R12).
- **Se i giocatori chiedono di attaccare il drago, cosa rispondo, e dove lo
  trovo?** `S1` 227 dice solo «molto pericoloso, ma mostra coraggio». La
  risposta (fuori tiro, effetti sul morale) è **mia**, R14.
- **Dove ho dovuto tornare indietro, e quanto tempo ho perso?** Fra `LIB` §13
  e `SEG` §2 per il mazzo dell'avanguardia (R15), che non ho trovato in
  nessuno dei due: cinque minuti di preparazione, e al tavolo sarebbero stati
  due di silenzio. Fra `S1` e `LIB` per capire dove sta la scaramuccia (R1):
  dieci minuti, la cosa più costosa della preparazione.

Invenzioni del DM, segnate come tali: modificatori d'abilità (R7), tre
statblocchi (R8, R17), scala dei fallimenti della ricognizione (R9), box di
Dara e i due comandanti (R10), posto della scaramuccia e taglio di 1C (R1),
morale in uscita (R2), effetti del drago (R14), mazzo dell'avanguardia (R15),
«vale/non vale» (R16), morte del pregen (R17), regole per il capitano e per il
giocatore dell'orda stasera (R21).

Due rilievi in più, già nominati nella lista di stampa e qui numerati:

**R31 · 🟠 · `LIB` 34-36 · `P-HANDOUT`.** Il foglio dei reparti (quadratini
dei PFU, tacche) e un tracciatore dell'orda per il DM non ci sono. Li faccio a
mano: venti minuti della mia ora.

**R32 · 🟠 · `S1` 47, 82, 122; `LIB` 140, 385 · `P-IMMAGINI`.** Le mappe
tattiche sono in `Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md`, fuori dal
materiale; il pendio della scaramuccia e della retroguardia non ha mappa da
nessuna parte. Uso le ASCII di `S1` e carta quadrettata.

---

## L'uscita

| # | Passo | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|
| V1 | 1 | `D-SERATA` | la serata non è dichiarata, e la vista non vede la scaramuccia | 🔴 | vista: «LA SERATA: il master non la dichiara» |
| V2 | 1 | `D-AVVERSARIO` | chi comanda l'orda e cosa vuole | 🟠 | vista: nessun nome di avversario fra titoli e grassetti |
| V3 | 1 | `D-PREPARA` | schede, libretto, dadi, fogli, statblocchi | 🔴 | vista: solo «Griglia ultra-clear» e le CD |
| V4 | 1 | `D-RUMORE` | primo grassetto è il titolo di un altro documento | 🟡 | vista: «4. CAPITOLO 2: LA CAMPAGNA» |
| R1 | 2 | `P-FLUSSO` | la scaramuccia di `LIB` §13 non è in `S1`; 1C si sovrappone | 🔴 | `S1` 27-229, `LIB` 361-363 |
| R2 | 2 | `P-CONGEGNI` | esiti di `S1` (CA mura, morale −2/+4) contro libretto (tacche, morale +1, trappole) | 🔴 | `S1` 182-195, 231-234; `LIB` 154, 387-390; `SEG` 64-66 |
| R3 | 2 | `P-FLUSSO` | il libretto dice che in S1 la battaglia campale c'è e non c'è | 🔴 | `LIB` 238 contro 361-363 |
| R4 | 2 | `P-FLUSSO` | 1E (notte) prima di 1F (alba dello stesso giorno) | 🟠 | `S1` 199-212 |
| R5 | 2 | `D-SALTO` | fasi omonime, manca 1D | 🟡 | `S1` 27, 41, 75, 115, 180, 199 |
| R6 | 2 | `D-SALTO` | sette rimandi a file assenti, nomi dei file diversi | 🟡 | `S1` 5, 16-20, 47; `LIB` 6; `SEG` 3 |
| R7 | 2 | `D-PREPARA` | i pregen non hanno abilità, lingue, tre caratteristiche | 🔴 | `S1` 144-158 contro `HO` 67-114 |
| R8 | 2 | `D-PREPARA` | nessuno statblocco per pattuglia, scout, sergente | 🔴 | `S1` 60-69, 103-105, 145 |
| R9 | 2 | `P-CONGEGNI` | la ricognizione non ha esiti di fallimento | 🟠 | `S1` 160-163 |
| R10 | 2 | `P-CONGEGNI` | niente read-aloud del campo nemico; Grimjaw e Gorthak senza descrizione | 🟠 | `S1` 115-140, `SEG` 42 |
| R11 | 2 | `P-STATO` | consiglio senza opzioni, PNG senza voce, box rivolto ai PG sbagliati | 🟠 | `S1` 169-178 |
| R12 | 2 | `P-FLUSSO` | rapporto delle sentinelle e aggancio di 1A vuoti | 🟠 | `S1` 30, 37-42 |
| R13 | 2 | `P-INTERAZIONI` | eventi per Warlock/Druido/Monaco, classi che i pregen non hanno | 🟡 | `S1` 205-208 |
| R14 | 2 | `P-CONGEGNI` | il drago: niente statistiche, nessuna conseguenza delle tre opzioni | 🟠 | `S1` 226-229, `HO` 70 |
| R15 | 2 | `P-CONGEGNI` | manca il mazzo dell'avanguardia e la ferocia della scaramuccia | 🟠 | `LIB` 365-376, `SEG` 37-41 |
| R16 | 2 | `P-CONGEGNI` | +1 del primo giorno, morale, eroe ferito: valgono nella scaramuccia? | 🟠 | `LIB` 76-77, 151-170, 371-382 |
| R17 | 2 | `D-PREPARA` | sergente senza statblocco, retroguardia senza mappa, morte del pregen | 🔴 | `LIB` 383-385, `SEG` 43-46, `HO` 31-32 |
| R18 | 2 | `P-CONGEGNI` | Scavare + Sbilanciare = −4 al bianco, da dire prima | 🟡 | `LIB` 373-375, `SEG` 23 |
| R19 | 2 | `P-CONGEGNI` | «i dadi li tirate voi» ma il macigno lo tira il DM | 🟡 | `LIB` 29-31, 259 |
| R20 | 2 | `P-CONFINE` | capacità «senza annunciarle» ma i giocatori devono sapere il bersaglio | 🟡 | `SEG` 15-16, `LIB` 66-72 |
| R21 | 2 | `P-STATO` | capitano e orda stasera senza numeri; Dara insostituibile; quanto di `SEG` al giocatore dell'orda | 🟠 | `LIB` 231-240, `HO` 49-51 |
| R22 | 2 | `P-GRUPPO` | handout 0 e assegnazione solo per il gruppo della campagna | 🟡 | `HO` 23-28, 46-48 |
| R23 | 2 | `P-HANDOUT` | «una pagina l'una»: Thorin ne fa più di due | 🟡 | `HO` 61-62, 159-200 |
| R24 | 2 | `P-CONGEGNI` | buff di 1°-2° e gesto del round; *Guarigione* come cura di massa | 🟡 | `HO` 151, 169, 182; `LIB` 126-136 |
| R25 | 2 | `P-STATO` | cannocchiale di Dara, capacità di Spia Maestra di Nala | 🟡 | `S1` 117, `HO` 103-114 |
| R26 | 2 | `P-CONFINE` | §12 del libretto rivela carte, probabilità e posta | 🟠 | `LIB` 3, 202-203, 306-356; `HO` 49-50 |
| R27 | 2 | `D-SALTO` | la scaramuccia richiede quattro sezioni di due file più il mio foglio | 🟠 | `LIB` §2-5, §11, §13; `SEG` §1-2 |
| R28 | 2 | `P-FLUSSO` | apertura della serata in tre versioni | 🟠 | `HO` 3, 57; `S1` 10, 22 |
| R29 | 2 | `D-TEMPO` | «si legge insieme a inizio serata»: due ore prima del primo tiro | 🟠 | `LIB` 3-4, 362-363 |
| R30 | 2 | `D-TEMPO` | nessuna durata né taglio in `S1` | 🟠 | `S1` tutto; `LIB` 397 |
| R31 | 2 | `P-HANDOUT` | foglio dei reparti e tracciatore dell'orda assenti | 🟠 | `LIB` 34-36 |
| R32 | 2 | `P-IMMAGINI` | mappe fuori dal materiale; pendio senza mappa | 🟠 | `S1` 47, 82, 122; `LIB` 385 |
| G1 | 3 | — | primo PNG della serata inventato dal DM | 🟠 | terzo passo, prima domanda |

**Conto**: 🔴 8 (R1, R2, R3, R7, R8, R17, V1, V3) · 🟠 18 · 🟡 11.

**I tre più gravi.**
1. **R1 + R2 + R3**: la serata ha due copioni che non si conoscono. `S1` non
   contiene la scaramuccia che il libretto mette nella Sessione 1, gioca al
   suo posto 1C con esiti (CA delle mura, morale da −2 a +4) che il libretto
   non usa, e il libretto stesso dice in §9 che stasera la battaglia campale
   non c'è.
2. **R7**: la prima metà della serata è fatta di prove d'abilità, e le schede
   dei pregen non hanno abilità.
3. **R8 + R17**: nessun avversario della serata ha statistiche, compreso il
   sergente della retroguardia, l'unico duello sulla mappa che il libretto
   promette.

**Si conduce stasera?** Sì, ma con un'ora di preparazione che va quasi tutta
in invenzioni: abilità, tre statblocchi, il mazzo dell'avanguardia, il posto
della scaramuccia, gli esiti. Il libretto, una volta spiegato a pezzi, regge;
la `SESSIONE-1` è il pezzo che non è stato rifatto per i pregen e per il
libretto.
