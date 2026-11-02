# Developer a freddo — ARC-08, Sessione 1 (2026-10-21)

**Chi**: developer di incontri a freddo. Non conosco la campagna; ho letto
solo i quattro file di `freddo/` (SESSIONE-1, LIBRETTO, HANDOUT-PREGEN,
SEGRETI-DM) e la rubrica `freddo/sviluppo-degli-incontri.md`. Non ho letto
PLAYTESTER.md né LETTORE.md.

**Come ho controllato i numeri**: `avanguardia.py` e `assedio_v3.py` girati
con `python3 -I` per ferocia 1/2/3, ritirata dopo i round 1-6 e trappole 0-6.
Le varianti (regola scritta invece della regola simulata, ritirata per
squadra, giganti in un settore solo, trappole valide anche il giorno 2,
Tenere/Caricare sempre) sono copie degli script nella scratchpad della
sessione, non nel repo. Seme 1372, 3000 prove ciascuna.

Riferimenti: `S1` = `freddo/SESSIONE-1.md`, `LIB` = `freddo/LIBRETTO.md`,
`HP` = `freddo/HANDOUT-PREGEN.md`, `SEG` = `freddo/SEGRETI-DM.md`. Le righe
sono quelle dei file a oggi.

## Il quadro in una tabella

Ogni incontro della serata contro le sei voci della consegna (scopo, posta,
statistiche, tattiche, terreno, esiti).

| Incontro | Scopo | Posta | Statistiche | Tattiche | Terreno | Esiti V/S/R |
|---|---|---|---|---|---|---|
| 1A Ricognizione (S1:37-163) | sì | parziale: solo premi, nessun costo | **no** (orchi, worg, scout, sergente) | **no** | mappe, scale incoerenti | solo vittoria |
| 1B Consiglio (S1:167-178) | vago | **no** | — | — | — | **no** |
| 1C Difese (S1:182-195) | sì | numeri di un altro sistema | — | — | — | solo successo |
| Avanguardia (LIB:359-397, SEG:37-45) | sì | sì (trappole) | sì per i reparti, **no** per il sergente | parziale | sì | sì, ma con una scelta dominante |
| 1E Presagi (S1:201-208) | atmosfera | — | — | — | — | agganci per classi assenti |
| 1F Il drago (S1:210-229) | sì | **no** | **no** | **no** | **no** | **no** |
| Risultati (S1:231-234) | — | — | numeri che il libretto non legge | — | — | — |

In sintesi: l'unico incontro con regole giocabili è l'avanguardia, e
SESSIONE-1 non la contiene. Il resto della serata produce numeri (morale da
−2 a +4, CA delle fortificazioni da 23 a 27, «+2 iniziativa di massa») che
il libretto, scritto dopo, non sa leggere.

## Rilievi

Ogni rilievo: dove (file:riga), codice della rubrica, gravità, il difetto con
la prova, la correzione con i numeri. La tabella riassuntiva nel formato della
rubrica è in fondo.

### 🔴 Rossi

**R1 · L'avanguardia non è nella sessione.** `LIB:7-8`, `LIB:359-363` contro
`S1:180-229` e `LIB:238-240`. §0 · contraddizione, 🔴.
Il libretto dice che la scaramuccia dell'avanguardia si gioca «nella
Sessione 1, dopo l'avvistamento, il giorno prima che l'orda arrivi alle
mura», ed è «la prima volta che si tira». SESSIONE-1 non ha nessuna scena
con quel nome: il giorno prima (Fase 3, `S1:199`) ha solo 1E e 1F. In più
`LIB:238` dice il contrario: «Nella Sessione 1, dove la battaglia campale
non c'è». Il DM non sa se giocarla né dove.
*Correzione*: un incontro **1D · L'avanguardia** in SESSIONE-1, nella Fase 3,
fra 1F (alba, `S1:212`) e 1E (notte, `S1:203`): l'ordine della Fase 3 diventa
1F → 1D → 1E, e la sigla 1D, che oggi manca nella numerazione, si riempie.
Il blocco rimanda a `LIB §13` e a `SEG §2` e dice solo chi ha davanti chi.
`LIB:238-240` diventa: «Nella Sessione 1 la battaglia campale c'è solo
nell'avanguardia (§13): lì il capitano guida una squadra di guastatori in
più, e chi ha scelto l'orda pesca le carte di `SEG §2`».

**R2 · Due sistemi di trappole e di difese, e il libretto ne legge uno.**
`S1:185-195` e `S1:231-234` contro `LIB:200`, `LIB:387-390`, `SEG:60`.
§1 · contraddizione, 🔴.
1C dà «+2 CA alle mura», «trappole (+2 danni alle unità nemiche)», «+1
morale a tutti i difensori», «−1 al primo assalto»; i Risultati chiedono
«Morale iniziale (da −2 a +4)» ed «Efficacia delle difese (CA delle
fortificazioni da 23 a 27)». Il libretto non ha CA delle mura, non ha danni
delle trappole, fa partire il morale da **+1** (`LIB:154`) e misura le difese
con le trappole dell'avanguardia. `SEG:60` lo ammette: le versioni delle
trappole erano quattro, il libretto ne ha tenuta una. Ma SESSIONE-1 è
rimasta alla versione vecchia: tutto quello che il tavolo fa in 1A, 1B e 1C
non arriva all'assedio, o ci arriva come il DM lo traduce.
*Correzione*: i Risultati della sessione (`S1:231-234`) si riscrivono come
leve del libretto. Proposta, una riga per fonte:

| Esito della serata | Leva del libretto |
|---|---|
| 1A Intelligence completa | per il giorno 1 ogni giocatore vede, a inizio round, il primo reparto del mazzo del suo settore |
| 1A Prigionieri interrogati | +2 al tiro d'attacco nel duello **Sfidare** contro Gorthak (§5) per i primi 3 round del duello |
| 1A Eliminazione silenziosa | la carta **I giganti** il giorno 1 non si gioca (l'orda non ha piazzato le macchine) |
| 1B Diplomazia CD 18 riuscita | il gruppo sceglie i settori e i reparti invece della tabella di `LIB:40-45` (oggi lo fa comunque: vedi A6) |
| 1C Artigianato (Pietra) CD 20 | +1 al bianco in **un** settore a scelta per il giorno 2 (le merlature di `LIB:198`, prestate a un altro settore) |
| 1C Ingegneria CD 18 | **+1 trappola** che si somma a quelle dell'avanguardia |
| 1C Diplomazia CD 16 | morale della rocca **+1** all'alba del giorno 1 |
| 1C Intimidire CD 20 | nel round 1 del giorno 1 l'orda ha −1 ad AU in tutti i settori |
| 1F risposta del gruppo | vedi R5 |

Il morale di partenza resta +1 e si somma, con il tetto ±5 e l'effetto ±2
sui dadi di `LIB:153-157`. La riga «CA delle fortificazioni 23-27» sparisce.
Con questa tabella `S1:231-234` dice: «Annota le leve ottenute: si leggono
all'alba del giorno 1».

**R3 · Le schede dei pregen non hanno le abilità, e la serata è fatta di
prove di abilità.** `HP:73-113` contro `S1:69`, `S1:144-158`, `S1:177-178`,
`S1:186-195`. §0 · manca, 🔴.
1A chiede Nascondersi, Muoversi Silenziosamente, Intimidire CD 18, Osservare
CD 20, Sopravvivenza CD 22, Conoscenze (Religione) CD 18, Nascondersi CD 22;
1B Diplomazia CD 18 e Conoscenze (Ingegneria) CD 15; 1C Artigianato
(Pietra) CD 20, Ingegneria CD 18, Sapienza Magica CD 22, Diplomazia CD 16,
Intimidire CD 20. Le quattro schede danno PF, CA, TS, attacco, sei
caratteristiche al massimo e **nessuna abilità**. Un giocatore non sa se
Nala ha Diplomazia +20 o +4, e il DM inventa ogni modificatore della
serata. Le CD non si possono nemmeno tarare: una CD 22 è certa per un
bardo-spia di 12° e impossibile per un guerriero.
*Correzione*: una riga **Abilità** per scheda, con le 6-8 abilità che la
serata usa, ai gradi massimi dell'SRD (livello + 3 = 15 per le abilità di
classe) più caratteristica. Esempio, da confermare sulle schede del
Bestiario `[INFERRED — needs DM confirmation]`, calcolati con 15 gradi e
le caratteristiche delle schede: Dara Nascondersi +19, Muoversi
Silenziosamente +19, Osservare +17, Sopravvivenza +17; Nala Nascondersi +19,
Diplomazia +21 (con la sinergia di Raggirare), Raggirare +19; Thorin
Concentrazione +20. Le abilità basate su Intelligenza (Conoscenze, Sapienza
Magica) non si calcolano: le schede non danno l'Intelligenza di nessuno.
Con questi numeri le CD di 1A sono **quasi certe** per gli specialisti
(Dara +17 contro CD 20 riesce con 3 o più, il 90%; Nala +19 contro CD 22,
lo stesso): la serata non ha prove che possano andare male, e la posta di
R4 non regge. Le CD di 1A salgono di 5 (Osservare 25, Nascondersi 27,
Sopravvivenza 27) o diventano contrapposte, con i modificatori dei nemici
scritti (R4).

**R4 · 1A non ha né nemici con statistiche né un esito di fallimento.**
`S1:37-69`, `S1:77-109`, `S1:142-163`. §8 · manca, 🔴.
Il testo mette in campo «3 Orchi» su worg (`S1:61-62`, la mappa non dice se
i worg sono uno o tre) e «1 Sergente, 9 guerrieri» hobgoblin (`S1:104`), con
prove contrapposte, ma non dà una riga di statistiche, né Osservare/Ascoltare
dei nemici per le prove contrapposte di `S1:69`. Il «Livello di Sfida 5-12»
(`S1:38`) non dice quale approccio vale quanto. E soprattutto
l'incontro ha solo le **ricompense per successo** (`S1:160-163`): se gli
scout vedono il gruppo, cosa succede? Chi suona l'allarme, in quanti round
arriva chi, e cosa perde la rocca? Le «contromisure» di `S1:163` non sono
scritte da nessuna parte. Senza un costo, la scelta «infiltrarsi o
attaccare» non esiste: quattro PG di GS 12-13 contro tre orchi e dieci
hobgoblin (EL 7-8 al massimo) attaccano e vincono in due round.
*Correzione*: (a) un blocco statistiche compatto per l'orco su worg, il worg,
il guerriero hobgoblin e il sergente (lo stesso di `SEG:44`, che serve anche
alla retroguardia, R7); (b) le **modalità di fallimento** in numeri:

| Cosa succede in 1A | Costo |
|---|---|
| la pattuglia su worg vede il gruppo e uno fugge | l'allarme arriva al campo in 3 round; nell'avanguardia (1D) i **lupi cavalcati** arrivano già al round 1 con fronte due |
| gli scout vedono il gruppo e il sergente suona il corno | niente «Eliminazione silenziosa»; la carta **I giganti** il giorno 1 si gioca in due settori |
| combattimento aperto, nessuno fugge | nessun costo, ma niente Intelligence completa: la vista dall'alto dura 2 round invece di 5 |

(c) la riga di EL di ogni gruppo: pattuglia ~EL 5, scout ~EL 8, entrambi
insieme ~EL 9. Il rango 5-12 di `S1:38` diventa questa riga.

**R5 · Il drago di 1F si può attaccare, e non ha statistiche, tattica né
esito.** `S1:210-229`. §8 · manca e §2, 🔴.
`S1:226-229` offre tre opzioni, la prima «Attaccare il drago». Fauci di
Palude non ha età, PF, CA, quota, velocità, soffio (forma, danni, CD) né
tattica; non si dice cosa fa se Dara gli tira con l'arco (portata massima
dell'arco lungo composito: 10 incrementi da 33 m = 330 m, quindi lo
raggiunge), né cosa portano le tre opzioni. È la §1 della rubrica: in quota,
Borin e Thorin non hanno niente da fare, e il testo non lo affronta.
*Correzione*: 1F non è uno scontro, ed è giusto: va detto e va dato il
perché. Proposta: (a) quota **90 m** `[INFERRED — needs DM confirmation]`,
fuori dalla portata delle baliste (d20+10, `LIB:199`, che il libretto usa
solo sulle torri) ma dentro l'arco di Dara a −4 di gittata; (b) il drago non
risponde alle frecce e non scende: compie il passaggio e va via in 2 round;
(c) le tre opzioni, ognuna con la sua leva: **Attaccare** (Dara colpisce
almeno una volta) → morale **+1**, ma la carta **Il soffio** il giorno 3
colpisce anche la Torre Ovest; **Rispondere con magia** (un incantesimo di
3°+ visibile, Thorin o Nala) → morale **+1**, nessun costo, ma l'incantesimo
è speso per la giornata dell'avanguardia; **Ignorare** → nessun morale, e
nell'avanguardia l'eroe che lo propone ha un gesto Comandare gratis nel
round 1. Così le tre strade costano cose diverse e nessuna domina.

**R6 · L'avanguardia scritta non è l'avanguardia simulata, e quella scritta
ha una scelta dominante.** `LIB:373-385`, `LIB:392-395` contro
`avanguardia.py:24-46`. §0 · regola e scelta dominante, 🔴.
Tre differenze fra testo e script, e due cambiano la risposta:

1. **Le mezze trappole.** `LIB:373-374`: «Ogni **due round** di scavo di
   *una squadra* fanno una trappola». Lo script (`avanguardia.py:34`, `:53`)
   somma mezze trappole di squadre diverse e poi tronca il totale. Con la
   regola scritta, chi si ritira dopo il round 3 ha 1,5 round di trappola
   per squadra, cioè una: lo stesso di chi si ritira dopo il round 2.
2. **La ritirata.** `LIB:377-379`: «il gruppo decide se restare… Chi si
   ritira porta a casa le sue trappole», che si legge per squadra. Lo script
   ritira tutte le squadre insieme a un round fisso.
3. Borin guida «veterani» in `LIB:366` e la Guardia del Cancello nello script
   (`avanguardia.py:17`). Questa pesa poco (5,06 contro 5,07 trappole).

Ferocia feroce (2 nello script), media su 3000 prove:

| Ritirata dopo il round | Script (somma, gruppo) | Regola scritta (per squadra, gruppo) | Regola scritta, ognuno si ritira a 2 tacche o PFU ≤5 |
|---|---|---|---|
| 2 | 4,00 trappole · 0 travolte | 4,00 · 0 | 4,00 · 0 |
| 3 | 5,07 · 0,25 | **3,75** · 0,25 | 3,97 · 0,03 |
| 4 | 5,01 · 0,89 | 4,44 · 0,94 | 5,34 · 0,04 |
| 6 | 2,23 · 2,93 | 1,54 · 3,16 | **5,41 · 0,05** |
| 8 | — | 0,20 · 3,91 | 5,40 · 0,05 |

Con la regola come è scritta succedono due cose. Se la ritirata è di tutto il
gruppo, **ritirarsi dopo il round 2 domina**: quattro trappole certe,
«parziale» sicuro, e il «pieno» (6+) arriva solo il 22% delle volte restando
fino al 4, a costo di una squadra. Se la ritirata è per squadra, il giocatore
che ritira la sua squadra alla seconda tacca **non rischia più niente**: la
squadra travolta scatta solo alla terza tacca (`LIB:380`), e la seconda è un
avviso perfetto. Restare a oltranza vale 5,4 trappole con lo 0,05 di squadre
perse. In tutti e due i casi la frase di `LIB:395`, «Il round in più è
sempre una scommessa», è falsa. Anche `LIB:393-394` («quasi nessuna squadra
travolta» al round 4) non regge: è 0,89, quasi una su quattro.
*Correzione*, la più piccola che rende vero il testo:
- `LIB:373-374`: «Ogni due round di scavo fanno una trappola, **contati su
  tutto il gruppo**: quattro squadre che scavano un round fanno due
  trappole». È quello che lo script già fa.
- `LIB:377-379`: «La ritirata è **di tutto il gruppo**: alla fine di ogni
  round si decide insieme se restare. Una squadra sola non si ritira; può
  solo smettere di scavare e combattere (ordine Colpire o Tenere)».
- `LIB:393-394`: «chi si ritira dopo il terzo round porta a casa in media
  cinque trappole, e una volta su tre sei o più, perdendo una squadra ogni
  quattro serate; dopo il quarto, lo stesso numero di trappole ma una
  squadra persa quasi ogni volta».
Con queste tre righe le colonne «Script» della tabella diventano la regola,
e la scelta fra round 2 (4 certe), round 3 (35% di pieno, 0,25 squadre) e
round 4 (36%, 0,89) è una scommessa vera.

**R7 · Le trappole oltre la terza non cambiano l'assedio.** `LIB:200`,
`LIB:387-390`, `assedio_v3.py:132-136`. §0 · conseguenza non misurabile, 🔴.
La posta dell'avanguardia, l'unica scena della serata con una posta in
numeri, è il numero delle trappole. Nell'assedio, ferocia feroce:

| Trappole | 0 | 2 | 3 | 4 | 6 |
|---|---|---|---|---|---|
| Breccia contenuta, pieno | 67% | 72% | 73% | 73% | 73% |
| Posizioni tenute, pieno | 51% | 54% | 55% | 55% | 55% |

Dalla terza in poi non succede niente: il giorno 1 è il giorno con le mura
intatte e il +1 al bianco, e i settori ci prendono poche tacche. La
differenza fra «parziale» (3-5) e «pieno» (6+) esiste solo nella riga
**Difese preparate** di `ARC08-10` §5.1, che non ho: se quella riga vale
qualcosa nel finale, va bene, ma allora è l'unica posta, e il libretto la
deve dire ai giocatori. Così com'è, R6 fa scommettere il tavolo su una
differenza che l'assedio non sente.
*Correzione*: la trappola annulla una tacca **del giorno 1 o del giorno 2**
(`LIB:200`, `LIB:387`, `SEG:60`; nello script, `giorno <= 2` a
`assedio_v3.py:135`). Con la stessa ferocia:

| Trappole | 0 | 2 | 4 | 6 | 8 |
|---|---|---|---|---|---|
| Breccia contenuta, pieno | 67% | 75% | 84% | 89% | 92% |
| Posizioni tenute, pieno | 51% | 53% | 58% | 62% | 61% |

Ogni trappola in più ora pesa 3-4 punti di breccia fino alla sesta: la
scommessa di R6 ha un prezzo e un premio. Il prezzo è che la tabella della
ferocia di `LIB:316-320` va rifatta con le trappole valide due giorni
(«Feroce», con 3-6 trappole, passa da 7 a 8-9 su 10 di breccia contenuta).
Se il DM vuole tenere il 7 su 10, si alza la ferocia di default, o le
trappole valgono il giorno 2 solo dal Cancello.

### 🟠 Arancioni

**A1 · Le percentuali della ferocia contano i giganti in tutti e quattro i
settori; il libretto ne concede uno.** `LIB:322`, `LIB:330` contro
`assedio_v3.py:87-89`. §0 · regola, 🟠.
`LIB:322`: «Una [carta] per round al massimo, in un settore a scelta». Lo
script tira il macigno al round 2 dei giorni 1 e 2 **in ogni settore**.
Con un settore solo, ferocia feroce: breccia contenuta 75% (0 trappole) e
**83%** (4 trappole) invece di 67% e 73%; posizioni tenute **73%** invece
di 55%. La riga «Feroce» di `LIB:319` («7 volte su 10», «poco più di
metà») vale solo se il DM gioca quattro carte in un round.
*Correzione*: o `LIB:330` dice «round 2: **un macigno per settore**», ed è
la carta che le prove hanno misurato; o la tabella di `LIB:316-320` si
rifà con un settore solo (Feroce: 8 su 10, tre quarti). La prima è più
semplice e tiene i numeri.

**A2 · Il sergente non si può sfidare quando conta, e non ha statistiche.**
`LIB:383-385`, `SEG:40`, `SEG:43-46`. §8 · manca e §5, 🟠.
Il sergente dà +1 ad AU e DU di tutta l'avanguardia dal round 3
(`SEG:40`); «se cade, il +1 del sergente esce» (`SEG:45`). Ma l'unico modo
di affrontarlo è la retroguardia (`SEG:43`), che si gioca **nel round in cui
gli altri si ritirano** (`LIB:383-384`): quando il sergente cade non c'è più
nessuno a cui togliere il +1. La leva è morta. Il duello poi non ha CA, PF,
attacco né condizione di fuga («poi scappa (o no)», `LIB:385`). Contro
Borin (+21) un guerriero di 6° con armatura completa (CA ~19) dura un round:
il «duello» va scritto anche per non durare zero.
*Correzione*: `LIB:383-385` diventa: «**Sfidare il sergente**: dal round 3,
un eroe può lasciare la sua squadra per un round e sfidare il sergente
sulla mappa, come il gesto Sfidare di §5. In quel round la sua squadra
tira senza di lui e non prende tacche. Se il sergente cade, il suo +1
esce. **La retroguardia** resta: chi resta indietro copre la ritirata di
tutti, e nessuna squadra è travolta in quel round». In `SEG:44` una riga di
statistiche: hobgoblin guerriero 6°, PF ~50, CA 20 (armatura completa,
scudo pesante), attacco +10 (spada lunga 1d8+3), fugge a 15 PF
`[INFERRED — needs DM confirmation]`. Così un eroe scommette un round
della sua squadra contro −1 a tutta l'avanguardia, che dopo il corno vale
molto.

**A3 · Chi arriva dopo il round 3, e quanti.** `LIB:376`, `SEG:37-41`.
§4 · manca, 🟠.
I lupi arrivano nei round 1-2, gli hobgoblin al 3. Quando un reparto
nemico è distrutto, chi lo sostituisce, e il mazzo dell'avanguardia quanti
reparti ha? Lo script mette un reparto di hobgoblin nuovo ogni volta
(`avanguardia.py:27-28`), senza limite. Il DM inventa il mazzo, e la
ritirata decide su un'orda che non sa quanto sia lunga. Non è detto nemmeno
cosa succede a una squadra a 0 PFU (lo script la conta travolta,
`avanguardia.py:44`; il libretto parla solo della terza tacca, `LIB:380`), né
dell'eroe di una squadra travolta.
*Correzione*: in `SEG:37-41`: «Dal round 3 ogni reparto distrutto è
sostituito da un reparto di hobgoblin, senza limite: l'avanguardia è lunga
quanto la pazienza del gruppo». In `LIB:380`: «La squadra travolta: alla
terza tacca, **o a 0 PFU**, la squadra fugge… L'eroe torna con lei, con i
punti ferita che ha».

**A4 · Nala non ha niente da fare nell'avanguardia.** `LIB:373-376`,
`LIB:119-136`, `HP:204-224`. §1, 🟠.
La squadra che scava non tira il rosso: la tacca la evita solo l'eroe, che
deve togliere 2 PFU da solo. Contro i lupi (DU 19) servono 5 sopra la DU;
contro gli hobgoblin col sergente (DU 23) lo stesso. Probabilità di non
prendere la tacca in un round di scavo:

| Eroe | contro i lupi (round 1-2) | contro gli hobgoblin col sergente (3-4) | dopo il corno |
|---|---|---|---|
| Borin +21 | 90% | 70% | 65% |
| Dara +19 | 80% | 60% | 55% |
| Thorin +14 | 55% | 35% | 30% |
| Nala +13 | 50% | 30% | 25% |

Thorin ha un'uscita: *Barriera di Lame* e *Colpo Infuocato* fanno 1d4+1
PFU (sempre 2 o più se il TS del reparto, d20+4 contro CD 21-22, fallisce,
cioè l'85% delle volte). Nala non ha incantesimi d'area che fanno danni, e
il suo canto (+1 ai dadi dei suoi reparti) non serve a una squadra che non
tira il rosso. È il PG di Tier più basso della scena, e la scena non le dà
niente. Suggestione, Affascinare, Immagine Silenziosa e Invisibilità sono
sulla sua carta e il libretto non le traduce.
*Correzione*: una riga in `LIB:371-385`: «**L'inganno** (Nala, o chiunque
abbia un'illusione o un ammaliamento di 1° o più): il reparto nemico davanti
alla tua squadra tira il TS (d20 + 4 contro la CD dell'incantesimo); se lo
fallisce, per quel round non tira il bianco e **il settore non prende la
tacca**». Con *immagine silenziosa* (CD 15) riesce il 50% delle volte, con
*Affascinare* (CD 18) il 65%: Nala diventa quella che protegge lo scavo, e
la sua squadra smette di essere la prima a cadere.

**A5 · 1A non regge al volo, all'invisibilità e al fiuto.** `S1:41-69`,
`S1:77-117`, `S1:150`, `HP:149`, `HP:216-218`. §2 e §17, 🟠.
Il gruppo ha *Silenzio* (Thorin e Nala), *Invisibilità* (Nala, una
persona), *Passare senza Tracce* (Dara, quattro compagni). Il testo non dice
cosa li ferma. I worg hanno **fiuto** (SRD: percepiscono le creature entro
9 m, 18 m sottovento): *Passare senza tracce* toglie le tracce, non l'odore
di chi è lì; l'invisibilità non serve contro il fiuto. Orchi e hobgoblin
hanno scurovisione: se 1A si gioca di notte, il buio non copre nessuno. Il
testo non dice l'ora. Infine l'Osservare di Dara a 400 m (`S1:87`,
`S1:140`, `S1:149`): con la penalità SRD di −1 ogni 3 m è −133, e la CD 20
è impossibile, a meno che il testo dica che un esercito non si «osserva»
come una creatura nascosta.
*Correzione*: tre righe in 1A. «**Il fiuto**: un worg sente chi passa entro
9 m (18 m sottovento), invisibile o no; il sentiero passa a 6 m dalla
pattuglia, quindi si passa sopravvento (Sopravvivenza CD 15 per leggere il
vento) o si aspetta che passi (un round in più, una prova di Nascondersi in
più)». «**L'ora**: all'alba; gli scout hanno scurovisione 18 m, che col
chiarore non conta più». «**La distanza**: per contare l'esercito non c'è
penalità di distanza; la CD 20 vale con il cannocchiale, 30 senza».

**A6 · 1C non ha un tempo né un prezzo, quindi si fa tutto.** `S1:182-195`.
§6, 🟠.
«I PG possono scegliere di aiutare in diverse aree» (`S1:183`): quante
prove a testa, quante volte, con quanto tempo? Due giorni di preparativi e
nessuna pressione permettono di prendere 20 (Artigianato CD 20 riesce a
chiunque abbia un grado), e nessun fallimento costa. «Lanciare incantesimi
difensivi: ogni incantesimo 3° liv+ fornisce bonus» (`S1:191`) non dice
quale bonus, e gli incantesimi tornano ogni mattina (`LIB:210`): è gratis.
La scelta dominante è fare tutto, e la scena diventa una lista da spuntare.
*Correzione*: «Ognuno ha **due azioni**, una per giorno di preparativi, e ne
fa una per area al massimo. Niente prendere 20: si lavora con l'orda in
vista. Fallire di 5 o più spreca l'azione». Le leve sono quelle di R2.
L'opzione B diventa una prova sola: «Sapienza Magica CD 22, o un
incantesimo di 3° o più consumato per il giorno: **+1 al bianco** del
settore di chi lo lancia nel round 1 del giorno 1». Con otto azioni in
tutto e sei leve, il gruppo sceglie.

**A7 · Il Consiglio non ha opzioni né esiti.** `S1:171-178`. §0 · manca, 🟠.
Quattro «Decisioni Strategiche» senza nessuna alternativa scritta, e una
Diplomazia CD 18 per «convincere i comandanti ad adottare tattiche
specifiche» senza dire quali né cosa cambia. Il DM inventa tutto il
Consiglio.
*Correzione*: legare le quattro decisioni al libretto, che le ha già.
**Distribuzione delle forze** = chi tiene quale settore e con quali reparti
(`LIB:40-45`); con la Diplomazia CD 18 il gruppo può scambiare due reparti
fra settori (es. la Guardia sulle Mura). **Difese magiche** = l'opzione B
di 1C. **Resistenza** = il modo di gioco (`LIB:216-229`). **Evacuazione** =
la riga Re Thorek ed evacuazione di `LIB:347`: se la Diplomazia riesce,
l'evacuazione parte il giorno 2 invece del 3 `[INFERRED — needs DM
confirmation]`. Quattro decisioni, quattro leve.

**A8 · Gli agganci di 1E sono per classi che il tavolo non ha.**
`S1:205-208`. §1, 🟠.
«Se presente un Warlock… un Druido… un Monaco»: i pregen sono Guerriero/
Campione Nanico, Ranger/Esploratrice, Chierico/Sacerdote delle Rune,
Bardo/Spia Maestra (`HP:68-104`). Nessuno dei tre agganci scatta, e la scena
non dà niente a nessuno.
*Correzione*: gli stessi tre presagi con i pregen. «**Thorin** (Conoscenze
Religione CD 15): sente nell'aria il fetore di un sacrificio a Tiamat, da
dove viene la magia di Grimjaw. **Dara** (Sopravvivenza CD 15): gli animali
che scendono dai monti dicono da dove arriva l'avanguardia: nella 1D, il
fronte dei round 1-2 è uno anche nel round 3. **Nala** (Ascoltare CD 18,
in lingua goblin): un canto di marcia con il nome di Gorthak: +2 al primo
attacco nel duello con lui».

**A9 · Il libretto avverte su Tenere con un numero sbagliato, e tace
l'altra metà.** `LIB:108-111` contro `assedio_v3.py:58-65` con Tenere e
Caricare sempre. §0 · regola, 🟠.
«Un gruppo che tiene sempre chiude i primi due giorni senza brecce meno di
una volta su dieci». Con l'eroe che combatte, ferocia feroce, 4 trappole:
Tenere sempre **23%** di breccia contenuta (non meno del 10%), e **94%** di
posizioni tenute al pieno; Caricare sempre 12% e 0%. Tenere è la scelta che
massimizza la riga «Posizioni tenute» di `LIB:346`: i due obiettivi tirano
in direzioni opposte, ed è un bel dilemma, ma il libretto lo nasconde dietro
un numero che non torna.
*Correzione*: `LIB:108-111`: «Tenere sempre salva i reparti e perde le mura:
nelle prove, chi tiene sempre arriva alla ritirata con quasi tutti i reparti,
ma chiude i primi due giorni senza brecce solo una volta su quattro.
Caricare sempre perde tutte e due le cose».

**A10 · Gorthak e Grimjaw sono bersagli senza CA né PF.** `S1:162`,
`LIB:137-143`, `LIB:331`, `LIB:334`. §17 · CA e pf, 🟠.
1A dà «+2 ai tiri per colpire contro [Gorthak] per 3 round»; il libretto
dice che i comandanti si sfidano sulla mappa e fuggono sotto metà dei PF.
Nel materiale non c'è un PF, una CA, un attacco di nessuno dei due. Nella
Sessione 1 non si combattono, ma la ricompensa di 1A si annuncia ai
giocatori stasera, ed è bene sapere quanto vale un +2 contro una CA che il
DM non ha.
*Correzione*: in `SEG` §2 o in un §4 nuovo, le due righe dai blocchi di
`ARC08-02`, con il valore di «metà dei PF».

### 🟡 Gialli

**G1 · Nessuna riga di scala, in nessun incontro.** `S1:37-229`,
`LIB:359-397`. §10 e §17 · manca, 🟡.
Con tre giocatori l'avanguardia ha tre squadre, e con la regola di R6 il
«pieno» (6 trappole) chiede due round di scavo in più a testa; con cinque,
la quinta squadra non ha pregen. Nell'assedio il settore senza eroe cede con
1-2 su 1d6 (`LIB:244-246`), il 33% al giorno.
*Correzione*: in `LIB:387-390`: «Con tre giocatori, le soglie sono 5 / 2-4 /
meno di 2; il capitano (modo C) porta la quarta squadra senza eroe, che
scava e non combatte. Con cinque, il quinto guida una squadra di veterani
senza eroe, e le soglie salgono a 7 / 4-6». In 1A: «con tre PG, gli scout
sono sei e il sergente».

**G2 · Le scale delle mappe di 1A dicono tre cose diverse.** `S1:47`,
`S1:49`, `S1:82`, `S1:84`. §0 · contraddizione, 🟡.
1A-1: «Ogni carattere ~ 5 metri» e, una riga sopra, la griglia ultra-clear
a 1,5 m; 1A-2: «~ 3 metri» e 1,5 m. Per Muoversi Silenziosamente e per il
fiuto (A5) la distanza conta.
*Correzione*: lo schizzo ASCII dice «non in scala: la griglia è quella di
`Mappe/…`», e la distanza fra sentiero e pattuglia si scrive in metri
(6 m, A5).

**G3 · Borin guida veterani o Guardia?** `LIB:42`, `LIB:366`,
`avanguardia.py:17`. §0 · contraddizione, 🟡.
Nell'assedio Borin ha la Guardia del Cancello; nell'avanguardia il libretto
gli dà veterani e lo script la Guardia. Il risultato cambia poco (5,06
contro 5,07 trappole al round 3), ma il giocatore deve sapere quale riga di
§11 usare.
*Correzione*: `LIB:366`: «Borin la Guardia del Cancello, Thorin e Nala
veterani, Dara balestrieri», come lo script.

**G4 · Le Mura il primo giorno: +1 o +2?** `LIB:196-198` contro
`assedio_v3.py:84-85`. §0 · regola, 🟡.
Il primo giorno dà +1 a tutti, le merlature +1 alle Mura «tutti i giorni».
Letta così, il primo giorno le Mura hanno +2; lo script dà +1.
*Correzione*: `LIB:198`: «+1 al bianco **dal secondo giorno**, finché le
Mura non hanno ceduto una volta (il primo giorno vale già il +1 di tutti)».

**G5 · I giganti ignorano le merlature, nello script no.** `SEG:24` contro
`LIB:330` e `assedio_v3.py:89`. §0 · contraddizione, 🟡.
`SEG:24`: «il macigno ignora le merlature delle Mura»; `LIB:330`: «contro la
DU di un reparto (con mura e morale)»; lo script mette il bonus delle mura
nella DU anche sulle Mura dal giorno 2.
*Correzione*: `LIB:330`: «(con il +1 del primo giorno e il morale; le
merlature delle Mura non contano)», e lo script toglie il `muro` delle Mura
dal tiro dei giganti.

**G6 · La Formazione tattica: i guerrieri hobgoblin contano?** `SEG:22`,
`LIB:295-296`, `assedio_v3.py:55`. §0 · regola, 🟡.
«Due o più reparti di hobgoblin» e i guerrieri si chiamano «guerrieri
hobgoblin». Lo script conta solo i reparti «hobgoblin». Nell'esempio di
`LIB:252-275` un hobgoblin e un guerriero stanno insieme, e la DU resta 22:
il libretto segue lo script, ma non lo dice.
*Correzione*: `SEG:22`: «due o più reparti di hobgoblin (i guerrieri
hobgoblin non contano: non marciano al tamburo)».

**G7 · L'eroe ferito non succede quasi mai, e non conta.** `LIB:90`,
`LIB:145-147`. §16 · al rovescio, 🟡.
Il bianco manca di 11 o più solo con un reparto debole sotto penalità:
nell'assedio, contro gli hobgoblin il giorno 1, la Guardia non ci arriva
mai (d20+24 contro 34). Nell'avanguardia sì: una squadra di veterani che
scava davanti ai lupi lo prende il 10% delle volte, i balestrieri di Dara il
25%. E 3d6 (10,5) contro 90-142 PF non manda a zero nessuno: «un eroe a zero
esce dalla battaglia» non scatta in una serata.
*Correzione*: tenerlo, ma farlo contare: «l'eroe ferito ha −2 al gesto del
round dopo». Oppure toglierlo, che semplifica il bianco di una riga.

**G8 · Il canto e *velocità* si sommano?** `LIB:133-136`, `HP:209`,
`HP:213`. §0 · regola, 🟡.
«Due uguali non si sommano»: il canto di Nala e la sua *velocità* sono due
cose diverse, e tutte e due danno +1 per il giorno. Con due gesti (il round
1 e il round 2) Nala dà +2 ai suoi reparti, che sui dadi è quanto il morale
al massimo.
*Correzione*: «Gli aiuti che durano tutto il giorno non si sommano fra loro:
un reparto ne ha uno solo».

**G9 · L'ordine della Fase 3 è rovesciato.** `S1:199-212`. §0 · altro, 🟡.
1E è «la notte prima dell'assalto», 1F «all'alba dell'ultimo giorno di
pace». Nel testo 1E viene prima di 1F. Con l'avanguardia (R1) in mezzo,
l'ordine giusto è 1F (alba) → 1D (giorno) → 1E (notte).
*Correzione*: spostare il blocco 1F prima di 1E.

**G10 · «Linguaggi (parlare Orco/Goblin)» non è una prova.** `S1:158`.
§6 · regola, 🟡.
In 3.5 Parlare Linguaggi è un'abilità senza tiro: si sa o non si sa la
lingua. Nala o capisce o no.
*Correzione*: «Nala parla Orchesco e Goblin [da confermare sulla scheda]:
capisce gli ordini se si avvicina a 9 m (Ascoltare CD 15, o Nascondersi
contrapposto se vuole restare)».

**G11 · Il capitano e l'orda nella Sessione 1 non hanno una scena.**
`LIB:238-240`. §0 · manca, 🟡.
«Il capitano guida la pattuglia di nani che accompagna gli eroi»: 1A non ha
nessuna pattuglia di nani (la mappa di `S1:66` mette solo [B, D, T, N]).
«Chi ha scelto l'orda gioca gli esploratori della Mano Rossa»: con quali
prove e quali limiti?
*Correzione*: vedi R1: in 1D il capitano guida la quinta squadra (G1) e il
giocatore dell'orda pesca le carte di `SEG §2`, decidendo lui su quale
squadra cadono i lupi. In 1A, chi gioca l'orda tira l'Osservare e
l'Ascoltare dei nemici.

**G12 · La ferocia dello script e quella del libretto non hanno lo stesso
nome.** `LIB:312-320` contro `avanguardia.py:11`, `assedio_v3.py:7-9`.
§0 · altro, 🟡.
Lo script chiama «2» la ferocia feroce, il libretto la chiama «come in §11»
(e −1 / +1 le altre). Chi ritara al primo tavolo deve saperlo.
*Correzione*: una riga sotto `LIB:320`: «Negli script: normale = 1, feroce =
2, terrificante = 3».

## Cosa regge

- **Il bianco** (`LIB:69-71`, `LIB:92-93`): d20 + DU contro 22 + AU ha la
  stessa probabilità del tiro d'attacco nemico 1d20 + AU contro DU, e le
  fasce spostate di uno tornano (mancare di 1-5 = il nemico supera di 0-4).
- **Il round d'esempio** (`LIB:252-275`): tutti i conti tornano, compresi i
  4 PFU dell'orda e i 3 della Guardia.
- **La tabella della ferocia** (`LIB:316-320`) torna con lo script, con 3-6
  trappole: 90/86, 73/55, 45/18 contro «9 su 10 / quasi 9», «7 su 10 / poco
  più di metà», «meno di 5 / meno di 2». Con la riserva di A1.
- **Le carte dei poteri** (`HP:128-224`): ho controllato portate, durate, CD
  e dadi contro l'SRD al livello d'incantatore della scheda (Thorin 12°,
  Nala 8°, Dara 4°): *guarigione*, *ferire*, *barriera di lame*, *colpo
  infuocato*, *pelle di pietra*, le cure, *preghiera*, *silenzio*, *arma
  spirituale*, *velocità*, *affascinare*, *suggestione*, *intralciare*,
  *grazia del gatto* tornano. Gli incantesimi al giorno di Dara (2 di 1°, 1
  di 2°) e di Nala (4/4/2) tornano con la Saggezza 14 e il Carisma 18.
- **Comandare contro Combattere** per Thorin e Nala (`LIB:119-125`): sui
  conti medi contro gli hobgoblin si equivalgono (Combattere +1,2 PFU
  inflitti; Comandare +0,6 inflitti e 0,6 salvati con due reparti e tre
  nemici). È una scelta vera.
- **Il corno di Grimjaw** (`SEG:41`) è un rinforzo che il tavolo vede
  arrivare (§14): va letto ad alta voce e dice che restare costa.

## Dove il DM deve inventare, stasera

In ordine di serata: le abilità dei quattro pregen (R3); le statistiche e
l'allarme della pattuglia e degli scout (R4); cosa vede Dara e cosa ne
viene (A5, `S1:140`); le opzioni e gli esiti del Consiglio (A7); quante
azioni ha ognuno in 1C e cosa dà un incantesimo (A6); se e quando si gioca
l'avanguardia (R1); chi arriva dopo il round 3 (A3); se la ritirata è per
squadra (R6); il sergente (A2); il drago (R5); come tradurre i risultati
della serata nell'assedio (R2).

## Tabella riassuntiva

| # | Scena | Codice | Cosa manca | Gravità | Prova |
|---|---|---|---|---|---|
| R1 | 1D Avanguardia | §0 · contraddizione | la scena non c'è in SESSIONE-1; `LIB:238` dice che la battaglia campale nella Sessione 1 non c'è | 🔴 | «nella Sessione 1, dopo l'avvistamento» (`LIB:361`) |
| R2 | 1A-1C, Risultati | §1 · contraddizione | i numeri della serata non sono leve del libretto | 🔴 | «CA delle fortificazioni da 23 a 27» (`S1:234`) |
| R3 | tutta la serata | §0 · manca | nessuna abilità sulle schede, 15 prove di abilità | 🔴 | `HP:73-113` |
| R4 | 1A | §8 · manca | statistiche dei nemici, allarme, esito di fallimento | 🔴 | «RICOMPENSE PER SUCCESSO» (`S1:160`) e nient'altro |
| R5 | 1F | §8 · manca, §2 | drago attaccabile senza statistiche, quota, esiti | 🔴 | «Attaccare il drago» (`S1:227`) |
| R6 | 1D | §0 · regola | regola scritta ≠ simulata; ritirata a round 2 o per squadra domina | 🔴 | «Ogni due round di scavo di una squadra» (`LIB:373`) |
| R7 | 1D → assedio | §0 · conseguenza | dalla 3ª trappola l'assedio non cambia (73% = 73%) | 🔴 | «annulla una tacca del primo giorno» (`LIB:200`) |
| A1 | assedio | §0 · regola | percentuali con giganti in 4 settori, regola in 1 | 🟠 | «Una per round al massimo, in un settore a scelta» (`LIB:322`) |
| A2 | 1D | §8 · manca, §5 | il sergente si sfida solo a ritirata fatta; nessuna statistica | 🟠 | «poi scappa (o no)» (`LIB:385`) |
| A3 | 1D | §4 · manca | chi arriva dopo il round 3; squadra a 0 PFU | 🟠 | `SEG:37-41` |
| A4 | 1D | §1 | Nala non ha un gesto che serva allo scavo | 🟠 | «Nala +13» (`LIB:302`) |
| A5 | 1A | §2, §17 | fiuto dei worg, ora del giorno, Osservare a 400 m | 🟠 | «Vista sul campo nemico a 400m» (`S1:85`) |
| A6 | 1C | §6 | nessun tempo, nessun costo, bonus degli incantesimi indefinito | 🟠 | «Ogni incantesimo 3° liv+ fornisce bonus» (`S1:191`) |
| A7 | 1B | §0 · manca | decisioni senza opzioni né esiti | 🟠 | `S1:171-178` |
| A8 | 1E | §1 | agganci per Warlock, Druido, Monaco, assenti fra i pregen | 🟠 | «Se presente un Warlock» (`S1:206`) |
| A9 | assedio | §0 · regola | «meno di una volta su dieci» è 23%; Tenere massimizza le posizioni | 🟠 | `LIB:108-111` |
| A10 | 1A → assedio | §17 · CA e pf | Gorthak e Grimjaw senza CA né PF | 🟠 | «+2 ai tiri per colpire contro di lui» (`S1:162`) |
| G1 | tutti | §10 · manca | nessuna riga di scala | 🟡 | — |
| G2 | 1A | §0 · contraddizione | scale delle mappe | 🟡 | «~ 5 metri» / «1,5 m» (`S1:47-49`) |
| G3 | 1D | §0 · contraddizione | Borin veterani o Guardia | 🟡 | `LIB:366` contro `LIB:42` |
| G4 | assedio | §0 · regola | Mura il giorno 1, +1 o +2 | 🟡 | `LIB:196-198` |
| G5 | assedio | §0 · contraddizione | i giganti e le merlature | 🟡 | `SEG:24` contro `LIB:330` |
| G6 | assedio | §0 · regola | i guerrieri contano nella Formazione tattica? | 🟡 | `SEG:22` |
| G7 | assedio, 1D | §16 | l'eroe ferito quasi non scatta e non conta | 🟡 | `LIB:145-147` |
| G8 | assedio | §0 · regola | canto e *velocità* si sommano | 🟡 | «Due uguali non si sommano» (`LIB:136`) |
| G9 | Fase 3 | §0 · altro | 1E (notte) prima di 1F (alba) | 🟡 | `S1:201-212` |
| G10 | 1A | §6 · regola | Parlare Linguaggi non si tira | 🟡 | `S1:158` |
| G11 | Sessione 1 | §0 · manca | capitano e orda senza scena | 🟡 | `LIB:238-240` |
| G12 | libretto | §0 · altro | nomi della ferocia fra script e libretto | 🟡 | `avanguardia.py:11` |

Totale: 7 🔴, 10 🟠, 12 🟡.
