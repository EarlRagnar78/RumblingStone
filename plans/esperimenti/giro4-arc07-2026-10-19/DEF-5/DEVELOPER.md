# Giro 4 · DEF-5 · il developer a freddo

Bersaglio: `07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md`
(1.123 righe), letto per intero. Rubrica: `skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md`,
le 16 domande. Confronti: `Bestiario/mostri/hobgoblin-sergente-cr5.md`,
`Bestiario/mostri/treant-di-adamantio-cr10.md` (che rimanda a `DEF-3` App. A.2),
`Bestiario/png/Dana_Forgiapietra.md` e `Re_Thorek_Hammerfist.md` (che rimandano
a `ARC08-01-GUIDA-DM.md` §PNG Alleati), `DEF-3` App. A (Durik), `DEF-4` Scene
8, 11, 12, 13 e §6, `ARC08-11-PONTE-ARRIVO.md`, `ARC08-01-GUIDA-DM.md` Sessioni
3-4, le pagine giocatore della Corona (`03_Corona_3_Gemme.html`) e della Cintura,
lo stato del gruppo (`stato-del-gruppo/sessione-4.md`, `state-ramo-di-gruppo.md`)
e la patch del 2026-10-18. Regole 3.5 controllate su
`skills/dnd-35-srd/references/combat.md`.

## Lo strumento

`python3 scripts/domande_developer.py --file "…DEF-5…"` dà due rilievi, tutti e
due già dichiarati in `plans/domande-developer.json`:

- **D1, Scena 3**, nemico in volo: falso positivo, in volo c'è Artemis. La
  ragione regge.
- **D3**, nessun TS su Tempra: scelta del DM (D90). La ragione regge, ma è
  scritta su un master che non c'è più: dice *«un solo scontro breve, contro
  orchi in fuga»*, e lo scontro adesso è contro cinque hobgoblin sergenti. La
  correzione è in fondo, fra i 🟡.

## I numeri che coincidono

Ho controllato a uno a uno questi numeri, e coincidono con le schede e con l'SRD.

- **Hobgoblin sergente** (A.2 contro la scheda del Bestiario): 37 pf, CA 21 e
  19 senza scudo, velocità 6 m, spada +9 (1d8+4/19-20), arco +6 (1d8/×3), TS
  +6/+2/+1, i cinque talenti, il +1 morale entro 3 m. In corsa fa 18 m a round
  (×3 in armatura pesante) e perde la Destrezza alla CA (`combat.md` r.178).
  La penalità d'armatura è −8 (completa −6, scudo pesante −2).
- **Orco** (A.1): 5 pf, CA 13/10/13, falchion +4 (2d4+4), giavellotto +1
  (1d6+3), TS +3/+0/−2. Contro CD 25 passa solo il 20 naturale.
- **Treant di Adamantio** (A.3): coincide con `DEF-3` A.2 (90 pf, CA 24, RD
  10/adamantio, 9 m, 2 schianti +18 da 2d8+9, un'ora).
- **Durik** (A.4): coincide con `DEF-3` App. A (102 pf, CA 21, morso +15
  2d6+6). La velocità di 12 m in `DEF-3` non c'è: viene da `DEF-4`, e non l'ho
  ricontrollata.
- **Dana** (A.5): CA 29, contatto 14, sprovvista 28, iniziativa +1, 142 pf
  massimi, come la Guida dell'ARC-08. Il *muro di pietra* sta in uno slot
  normale di 5°: lo slot di dominio di quel livello è *Colpo Infuocato*. La
  conversione in cura spontanea si può.
- **Re Thorek** (A.6): CA 30/13/29 da riposato. Da esausto ha −6 Des (13 → 7),
  quindi CA 27/10/27. Da prono +4 contro gli attacchi a distanza e −4 in
  mischia (`combat.md` r.103, r.117). La *Presenza Regale* (+3) e la *Chiamata
  alle Armi* (+5, 3 al giorno) coincidono con la Guida.
- **Le gittate e le CD**: *comando* a gittata vicina, 16,5 m al 13°;
  *intralciare* a gittata lunga, 264 m al 12°; la pergamena di *ristorare* letta
  con Usare Oggetti Magici a CD 27 (20 + LI 7); il salto di 3 m (1d6, o niente
  con Saltare o Acrobazia CD 15); il *muro di spine* (Forza contro 20, 1,5 m
  ogni 5 punti, 30 cm ogni 10 minuti con le lame, il fuoco magico in 10 minuti).
  *Ristorare* e *ristorare inferiore* si lanciano in 3 round, *guarigione* con
  un'azione standard.
- **Il calendario dei round**: porta a 36 m, anello a 30 m, 18 m di corsa a
  round. Nel ramo luminoso gli hobgoblin arrivano ai piedi dell'altare alla fine
  del round 4, nel ramo duro alla fine del round 3: i conti tornano. Il cambio
  d'arma prende un round intero (spada a terra con un'azione gratuita, scudo e
  arco con due azioni di movimento).
- **I PG**: con il dono dato al rito, Thorik ha +2 di deviazione dalla Corona,
  e la *Protezione dal Male* non si somma. Hella ha lo *Scudo del Custode*. La
  prima battuta della Senzienza è quella del ramo «ha donato». La Cintura fa 4
  cariche da +2d6, come nella patch. L'orologio è a ≈ 3g 15h, come nel registro
  di `DEF-2`.

## Rilievi

### 🟠 1 · §0-bis, box PF1e: le pozioni del 372 «svaniscono all'alba»

> *«Non riportano oggetti del −1000 se non ciò che è «loro» o legato (le
> pozioni antiche svaniscono all'alba; il Sigillo rubato a Vatore è
> l'eccezione»*

La Scena 1 dello stesso master dice il contrario (*«Tutto quello che portano
addosso, comprato al banco della fucina compreso: pozioni, pergamene,
bacchette, rune»*, G2-14), e così anche `DEF-4` §6. Il gruppo si porta dietro
47.967 mo di acquisti del 372, più le 5 *volare* e le 4 CFC del re: è la
domanda che i giocatori fanno appena atterrano. **Correzione:** nel box PF1e,
sostituire la parentesi con «tutto ciò che portano addosso torna, comprato al
banco compreso (Scena 1, G2-14); il Sigillo torna come il resto».

### 🟠 2 · Scena 2 e handout del §9: le gemme brillano tutte e tre, o c'è il vetro scuro?

Il box *«la caverna, voi»* dice *«Sulla fronte di Thorik brillano tre gemme»*,
e il box *«la corona intera»* fa tornare l'oro *«da tutte e tre le pietre»*
**dopo** l'arrivo. La pagina giocatore `03_Corona_3_Gemme.html`, che è metà
dell'handout «Lo Stato dei Custodi» e si consegna nella stessa scena, dice: *«Per la
prima volta l'oro è tornato indietro da tutte e tre le pietre. Poi il Rubino si
è acceso […] e adesso nel suo incasso c'è vetro scuro.»* Il giocatore di
Thorik legge l'opposto di quello che il DM gli ha appena letto. Anche il nome
non coincide: il master dice «Rubino/Leggenda», «Cuore della Leggenda»; la
pagina dice «Rubino — la Possanza Nanica»; `ARC08-11` dice *Gem of Immutable
Time*. **Correzione:** il DM sceglie fra pietra viva e vetro scuro, e il
perdente si allinea. I due box sono il punto più rapido: se resta il vetro
scuro, «brillano due gemme, e la terza è nera».

### 🟠 3 · §7 e §8 B: il Bane di Aegis Fang ha i numeri vecchi

> §7: *«+2 circostanza a Thorik vs Fauci + preavviso soffio»* · §8 B: *«+2
> circostanza vs Fauci (B4)»*

Per il gruppo di oggi il canone è in `DEF-2` §4, A7 (DM 2026-10-15): contro
Fauci **+2 al tiro per colpire, +3d6 ai danni, critico ×4**, più lo *Scosso*
1/incontro (Volontà CD 22). È anche la patch che il brief dice di considerare
canone. Il §7 è la lista che il DM apre all'inizio dell'ARC-08 per Fauci.
**Correzione:** in tutte e due le righe, «Bane di A7 (versione del 25
settembre): +2 colpire, +3d6, ×4, Scosso 1/incontro CD 22».

### 🟠 4 · «Prima di aprire, segna da DEF-4»: mancano tre righe da prendere stasera

È la tabella che il DM compila stasera, alla fine del duello. Mancano tre righe.

- **Thorik affaticato**, se contro Zog'tar ha chiesto la Benedizione della
  Forgia (`DEF-4` Scena 8, «al costo di essere affaticato … peserà su
  Skullcrusher»). Senza riposo arriva affaticato anche nel Cuore della
  Montagna: niente corsa e niente carica, ed è proprio quello che gli serve per
  andare al varco nella Scena 3.
- **La Cintura «assaggiata» o disciplinata** (`DEF-4` Scena 8): Volontà CD 18
  contro Fauci, oppure +1 sacro ai TS contro la paura. Non è nemmeno nel §7.
- **Perché il duello è finito FUGGITO.** `DEF-4` dà due cause a FUGGITO, *«i
  PG scelgono la sopravvivenza / non lo intaccano»*, più la Catena spezzata.
  `DEF-5` manda nel ramo duro solo la prima e nel luminoso la Catena; il caso
  «non l'hanno intaccato» resta senza ramo.

**Correzione:** tre righe in tabella, e in «I due rami» il caso «FUGGITO perché
non l'hanno intaccato → ramo …» (lo decide il DM).

### 🟠 5 · Raccordo ARC-08: dopo il portale il DM non trova la scena

DEF-5 chiude con *«Dana apre il portale. […] continua nel ponte d'arrivo
dell'ARC-08 e nella Guida DM»*, e il §0-bis promette *«prima il Cuore della
Montagna, poi Fauci, poi il consiglio di guerra»*. I due file indicati non
reggono il passaggio.

- `ARC08-11-PONTE-ARRIVO.md` racconta **l'arrivo**, cioè la Scena 2 già
  giocata, e non quello che c'è dopo il portale. In più è fermo al 2026-07-02
  e contraddice il canone: *«Thorik −2 CON permanente (sacrificato per la
  resurrezione)»*, *«il Cuore di Moradin … aggancia i loro spiriti»* (che
  `DEF-5` §3 nega, D32), *«Durik nel terzo seme»*, e il passaggio dai pregen
  ai PG che il gruppo di oggi non ha giocato.
- In nessun file dell'ARC-08 compaiono il portale di Dana o la Porta Ovest.
  La Guida passa dal 3B alla Sessione 4 con *«Dopo mezza giornata di battaglia
  sotterranea, voi e i nani superstiti emergete … sui bastioni»*, cioè l'opposto
  del portale «subito» e della torre ogni 10 minuti del §6.

Non tocca la serata di oggi, ma tocca la prossima. **Correzione:** nel §9,
indicare esplicitamente quale incontro della Guida ARC-08 si gioca all'uscita
dal portale (oppure scrivere che va scritto), e aprire un rilievo su `ARC08-11`
per lo stato in uscita: −4 DES/+2 COS/+4 CAR, i tre Doni, Durik sempre presente.

### 🟡 6 · Scena 3, Round 6: da sotto l'altare il re non si vede

Nel ramo luminoso i cinque si fermano *«ai piedi dell'altare»* e dal round 6
*«tirano al re»*. Il re però è steso in cima a un altare alto 3 m: dai piedi
la linea di vista su un corpo prono passa sopra il bordo, e il testo non dice se
c'è copertura né quanta (il bordo dell'altare in `combat.md` non c'è: da
verificare). **Correzione:** una riga, «per tirare al re si allontanano di 6-9 m
dall'altare» (così fanno già i due in coda nel ramo duro), oppure «dai piedi
dell'altare il re ha copertura (+4)».

### 🟡 7 · Scena 3, ramo luminoso: due round in cui ai PG non arriva niente (§13)

Gli orchi scossi rimasti, due più i Treant, Durik e novanta nani, cadono nel
round 1. Gli hobgoblin passano l'anello nel round 2 e sono ai piedi dell'altare
alla fine del round 4. Nei round 2 e 3, chi resta sull'altare ha bersagli solo
a 30 m: fuori portata per la mischia e, quasi sempre, per il *Rovo Eldritch* e
l'*Eldritch Blast* (18 m). Lo scontro si spezza in due, ed è il caso della
domanda 13. Il testo lo sa solo a metà (*«Chi vuole fermare gli hobgoblin prima
scende dall'altare e va al varco»*). **Correzione:** «chi scende al round 1 li
incontra a metà strada al round 3», oppure far correre i cinque dal round 2, e
nella regia scrivere che i round 2-3 si giocano in fast-play.

### 🟡 8 · Scena 3, tattiche: lo Scalare «quasi mai» è «mai»

> *«con −8 di penalità d'armatura lo Scalare CD 15 non riesce quasi mai (SRD)»*

For 14 (+2) meno 8 fa −6: anche con 20 si arriva a 14. **Correzione:** «non
riesce mai».

### 🟡 9 · Scena 3: quando si legge il box «il primo round»

Il box fa comparire gli scudi nel varco (*«compare uno scudo, poi un altro»*),
ma nel ramo luminoso gli hobgoblin entrano *«alla fine del round 1»*. Se il DM
lo legge all'inizio del round 1, li fa entrare un round prima, e il preavviso
di Artemis non serve più. **Correzione:** «si legge alla fine del round 1, quando
entrano (nel ramo duro, alla fine del round di sorpresa)».

### 🟡 10 · Scena 1: Thorik tira la Volontà dello strappo?

Lo strappo *«scuote la mente, e si resiste con la Volontà»*. Thorik ha *Mente
Vuota* permanente dalla Corona (*«immune a tutti gli effetti mentali»*,
pagina a tre gemme), e Artemis ha la *Fortezza Mentale* (+2 contro l'influenza
divina). Il giocatore lo chiederà. **Correzione:** una riga, «lo strappo non è
un effetto mentale: tira anche Thorik», oppure «Thorik ne è immune». Lo decide
il DM.

### 🟡 11 · «Se lo divinano»: la *comunione* di Thorik vuole un Nodo

> *«Thorik ha comunione una volta al mese dalla Corona»*

La pagina della Corona dice *«In un Nodo Terrestre, 1/mese: Comunione»*.
**Correzione:** «se il Cuore della Montagna è un Nodo Terrestre
`[INFERRED — needs DM confirmation]`», oppure togliere *comunione* dalla prima
riga.

### 🟡 12 · Scena 2, gesto di Hella: Durik si può richiamare subito

> *«se il drago l'ha distrutto nel duello e non è stato richiamato, torna all'alba»*

`DEF-3` dice che il seme III *«richiama Durik solo se è stato distrutto: torna
subito, per un'ora»*. Manca il gesto. **Correzione:** nella riga di Durik
aggiungere «oppure Hella lo richiama col seme III, con un'azione standard, se il
seme è carico e l'Evocazione non è spenta».

### 🟡 13 · §0 e Scena 2: il torque murato nell'incudine

`DEF-4` Scena 12 ha un ramo: se la scena salta, *«il re fa murare il torque
nell'incudine … e i nani del 1372 lo tirano fuori quando riconoscono la
Corona»*. In più, *«nel 1372 i nani si scoprono il capo davanti a chi lo
porta»* (`DEF-4` §8 B). `DEF-5` copre solo il torque consegnato a mano.
**Correzione:** nella riga «se Re Thorek I ha dato il torque» aggiungere «o se
è murato nell'incudine: lo porta un capo a Thorik, dopo il passaggio di
consegne», e far scoprire il capo ai capi nell'anello nella Scena 2.

### 🟡 14 · §1 Hella: il Debito della Radice l'ha preso Thorik

> *«radici cristalline … il segno … del Debito della Radice (`DEF-3` §6) che la segue»*

Per il gruppo di oggi il debito l'ha preso Thorik (E-07g). Il §7 lo dice, il
§1 no. **Correzione:** «del Debito della Radice, che Thorik ha preso su di sé e
che lei sente ancora suo (E-07g)».

### 🟡 15 · §0-bis, ramo duro: cosa fa l'aura agli orchi, se non tirano?

> *«niente TS: restano cinque orchi scossi e il capo»*

Se nessuno tira, non si capisce perché gli altri venticinque fuggano, né se il
capo sia scosso. **Correzione:** «niente TS: l'aura mette in fuga tutti tranne
cinque orchi e il capo, che restano scossi».

### 🟡 16 · Scena 2, «Dove sono tutti», e la mappa CM-1: gli orchi scossi

La tabella dice che i due orchi scossi *«sono già dentro l'anello»* (G2-32), ma
la mappa li segna 🔴 alle righe 02-03, cioè fuori dall'anello (riga 04).
**Correzione:** nella nota sotto CM-1, «i due scossi che restano sono dentro
l'anello, fra la riga 05 e l'altare».

### 🟡 17 · §6: le Cantitrici non sono nel Bestiario

> *«chierica 8 / barda 4, GS 12 … (Bestiario)»*

Nel `Bestiario/` le Cantitrici non hanno una scheda; lo statblocco è in
`ARC08-01-GUIDA-DM.md` §Cantitrici, e la mappa L2 le dà «Clr/Brd 11».
**Correzione:** il rimando diventa «(Guida DM dell'ARC-08, PNG Alleati)», come
per Dana e Re Thorek.

### 🟡 18 · §8 B: l'inventario d'uscita non conta il 372

Il tesoro in uscita elenca Terra e corredo di Hella, ma non il torque, il
Sigillo se rubato, e gli acquisti e le vendite della fucina (47.967 mo
comprate, 28.364 vendute, e le rune). Il §8 B dice di essere l'**ingresso
dell'ARC-08** per il WBL. **Correzione:** una riga, «Acquisti del 372: `DEF-4`
Scena 5, "Il conto della fucina", e `sessione-4.md`», e una per il torque.

### 🟡 19 · §8 A: il 14° «già all'arrivo» non si può verificare

> *«Con il Fuoco (P3) già alle spalle, i PG hanno i PX del 14° già all'arrivo»*

`sessione-4.md` dice che per il Fuoco il repo ha tre valori che non
coincidono (3.000, 7.200 e 18.000 ÷ 3), e il DM non ha ancora scelto.
**Correzione:** da verificare: «se il Fuoco vale X, il 14° arriva qui».

### 🟡 20 · `plans/domande-developer.json`: la ragione di D3 è ferma al master vecchio

> *«un solo scontro breve, contro orchi in fuga»*

Lo scontro adesso è contro cinque hobgoblin sergenti. **Correzione:** «contro
orchi scossi e cinque sergenti hobgoblin».

## Le sedici domande, una riga ciascuna

| # | Domanda | Esito |
|---|---|---|
| 1 | Chi resta senza niente da fare | Regge: Thorik ha l'ordine e il *comando*, Tordek copre il re o scende a combattere. I nemici non volano. Vedi il 7 per i round vuoti |
| 2 | Volo e invisibilità | Regge: orchi e hobgoblin rispondono a chi vola e a chi è invisibile. Il luogo non è sorvegliato contro i PG |
| 3 | I tre TS | Manca Tempra, dichiarato (D90). Rilievo 20 sulla ragione |
| 4 | Chi sente il rumore | Regge: il fischietto, l'ondata dopo dichiarata dell'ARC-08, il corridoio se inseguono |
| 5 | Il boss cambia | Non si applica: niente boss |
| 6 | Skill challenge | Non si applica |
| 7 | Chi si diverte | Non si applica (gruppo fisso) |
| 8 | Tattiche di ogni scontro possibile | Regge: orchi, capo, sergenti, nani, il corridoio, la porta murata. Manca il Comando 3/giorno di Re Thorek, ma lui «non combatte»: è una scelta |
| 9 | Segreto e divinazione | Regge, con il 11 |
| 10 | Riga di scala | Regge (tre e cinque PG) |
| 11 | Il mostro insostituibile | Regge a metà: il sergente punta il re e passa all'arco. Gli orchi sono un segnaposto, e qui è giusto |
| 12 | Il pericolo che qualcuno usa | Le stalattiti crollano solo con *terremoto*, che nessuno in scena lancia: sono scenografia. Il salto di 3 m dall'altare nessuno lo usa. Accettabile in una transizione |
| 13 | L'incontro resta uno | No nel ramo luminoso (rilievo 7) |
| 14 | Il rinforzo che si vede arrivare | Regge (il fischio, G2-38) |
| 15 | Niente dossi | Regge: venti, ma ne passano cinque |
| 16 | PG fuori per un TS | Non si applica (frastornato 1 round) |

## Raccordo con DEF-4 (Scene 12-13)

Il raccordo con le Scene 12-13 regge. L'ultima battuta della Scena 13 (*«La
luce comincia a tirare e vi porta via»*) passa al filo della Scena 1. L'Aura
della Forgia dura fino all'alba del 1372, il torque arriva alla Scena 12, la
Corona si completa dopo l'uso, e le battute di Aegis Fang e della Senzienza
seguono il ramo del dono. I buchi stanno nella tabella «segna da DEF-4»
(rilievi 4 e 13).

## Lo stato del gruppo verso l'ARC-08

Lo stato del gruppo in uscita (Corona +2 col dono, Hella coi tre Doni, Debito
su Thorik, ≈ 3g 15h) è corretto in `DEF-5`. Il testo che lo riceve, dall'altra
parte, no: il rilievo 5.

🔴 0 · 🟠 5 · 🟡 15
