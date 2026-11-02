# DEF-5 · Correzioni dopo il giro a freddo

Esiti: CORRETTO 22 · DECISIONE DM 4 · RESPINTO 1 · 🟡 lasciati 9

Master: `07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md`.
Rapporti: DEVELOPER (DEV), PLAYTESTER (PT), DM. I rilievi doppi sono uniti in
una riga sola; i 🟠 sono dieci dopo l'unione, i 🟡 ventisei.

Verifiche dopo le correzioni: `misura_craft.py --box` dà 7 box e nessuno oltre
le 12 righe (l'unico box toccato è «il silenzio», una parola cambiata);
`validate_modules.py` 0 errori; `copertura_scene.py --check` e
`domande_developer.py --check` verdi; `validate_prosa.py` nessun tic oltre
soglia. ⚠️ `componenti.py --check` segnala `APPARATO-ARC07-DEF-5-…` da
rigenerare (ho aggiunto una riga di Comparse nella Scena 3): non l'ho
rigenerato perché è un altro file, va fatto con `python3 scripts/componenti.py
--apparato` da chi chiude il giro.

Fonti usate per i numeri: Guida DM dell'ARC-08 (Dana: CA 29, 142 pf; i suoi
incantesimi), `Bestiario/mostri/hobgoblin-sergente-cr5.md` (talenti e comando,
D78), la pagina giocatore dell'Anello (Ali d'Ombra 18 m, Passo d'Ombra in
penombra), `DEF-4` (Durik, Treant D74, regola dell'alba D65), `state.md` §6
(Cintura), SRD 3.5 per scudo pesante, Scalare, copertura morbida, tempo di
lancio di *guarigione*, conversione spontanea del chierico buono e bonus di
deviazione che non si sommano.

## Rilievi

| Rilievo (rapporto#n) | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| Cure di Dana e Cantitrici contraddittorie (DEV#3, PT#1, DM#9) | 🟠 | CORRETTO | Vince la D92, più recente della D77 e confermata dalla Guida ARC-08 (r.412): hanno speso tutto, resta un *muro di pietra*. Riscritta la riga del §6 «Si fermano a curarsi». Nella Scena 3 aggiunta la conversione spontanea dell'SRD: Dana può trasformare il muro in una cura di 5° o meno (per esempio *cura ferite leggere di massa*), e allora il varco resta aperto; la cura non toglie l'esausto |
| Dana prende il colpo senza CA né pf, ramo «Madre Dana cade» (DEV#4, PT#2, DM#3) | 🟠 | DECISIONE DM | Corretta la parte che si può copiare: CA 29 e 142 pf massimi nella scheda d'entrata, e cosa le resta degli incantesimi. Resta aperto quanti pf ha all'arrivo, da cui dipende se il ramo può scattare (decisione 1) |
| Hobgoblin: arco lungo con scudo pesante (DEV#1) | 🟠 | CORRETTO | SRD: con lo scudo pesante la mano non fa altro. Chi non ha un nemico in mischia si sfila lo scudo (azione di movimento, CA 19) e tira; gli altri restano a scudi alti. L'intento della D77 è lo stesso |
| Hobgoblin ai piedi dell'altare (DEV#2) | 🟠 | CORRETTO | Scalare CD 15 con −8 di penalità d'armatura (completa −6, scudo pesante −2, For +2): non salgono. Si sfilano lo scudo e tirano al re, e il colpo che lo porterebbe sotto 0 lo prende Dana (D92) |
| Inseguimento nel corridoio nord (DEV#5) | 🟠 | CORRETTO | Riga nel §6: la prima fila attacca chi insegue, le altre passano perché l'ordine è il re ed entrano a fine round come sempre; il conto di chi passa l'anello resta quello della Scena 3; gli orchi in panico chiusi in mezzo si rannicchiano e si arrendono (SRD) |
| Orologio delle torri senza tetto né esito, riposo lungo, livello (PT#3) | 🟠 | DECISIONE DM | Il numero delle torri della Porta Ovest non sta in nessun file, e cosa succede a zero cambia l'apertura dell'ARC-08 (decisione 2) |
| Durik non spiegato (PT#4, DM#7) | 🟠 | CORRETTO | Nella riga di Hella: arriva con lei (legato alla Collana, DM 2026-09-24), Medio, 102 pf, CA 21, morso +15 (2d6+6), dalla scheda di `DEF-4`; se il drago l'ha distrutto e non è stato richiamato torna all'alba |
| Artemis a 36 m in un solo movimento (DM#4, DEV#11, PT#6) | 🟠 | CORRETTO | Ali d'Ombra 18 m: 18 nel round di sorpresa e 18 nel round 1 con l'azione di movimento; arriva prima che la fila entri (fine del round 1) e grida il preavviso con l'azione standard. Così la D91 resta possibile con le regole. Detto anche che il *Passo d'Ombra* vuole penombra e qui non funziona |
| Risorse da segnare da DEF-4 (DM#5, DEV#17, PT#8) | 🟠 | CORRETTO | Il §0 elenca ora *Aura di Comando* usata, semi carichi, Evocazione spenta, Durik in piedi, cariche della Cintura, dono della deflessione e *Scudo del Custode* |
| Poteri degli artefatti fuori dal file (DM#8) | 🟠 | CORRETTO | Le pagine giocatore entrano in «Cosa stampare» del §0. Non le copio nel master: sarebbero una seconda versione degli stessi poteri (ADR-0074), e sono già l'handout del §9 |
| Spada +9 / 1d8+4 (DEV#6) | 🟡 | CORRETTO | I numeri sono giusti con Arma Focalizzata e Specializzazione, For 14: aggiunti i talenti, presi dal Bestiario |
| +1 morale entro 3 m senza fonte (DEV#7) | 🟡 | CORRETTO | Citata la fonte: comando del sergente, Bestiario, D78 |
| *Guarigione* in 3 round (DEV#8) | 🟡 | CORRETTO | *Ristorare* e *ristorare inferiore* 3 round, *guarigione* azione standard (SRD) |
| Ramo «meno luminoso»: calendario, box, ordine e preavviso (DEV#9, PT#12, DM#10 seconda metà, DM#11) | 🟡 | DECISIONE DM | Corretti il calendario (varco nel round 1, altare a fine round 3) e la frase da dire al posto di «ne restano due» nel box. Se l'ordine di Thorik e il preavviso valgono ancora è bilanciamento del ramo duro (decisione 3) |
| Soglia di resa degli hobgoblin e fine dello scontro (DEV#10, PT#10) | 🟡 | CORRETTO | La resa diventa «meno della metà di quelli passati»: due su cinque (identico alla D77), uno su tre; se ne passano due combattono fino all'ultimo. La fine scontro è «quando l'ultimo cade o getta le armi». Nel box del silenzio «L'ultimo nemico» diventa «L'ultimo orco», perché gli hobgoblin non fuggono |
| Orchi senza risposta a volo e invisibilità (DEV#12) | 🟡 | CORRETTO | Se nessuno scende tirano i giavellotti al PG più vicino che vedono; chi non vedono non lo cercano. Per gli hobgoblin l'invisibilità non pesa, come nota anche il PT: il loro ordine è il re |
| «Coprirlo col suo corpo» senza effetto (DEV#13) | 🟡 | CORRETTO | Copertura morbida, +4 CA contro gli attacchi a distanza (SRD) |
| Radici di Hella che scadono a vuoto (DEV#14) | 🟡 | CORRETTO | Alla porta nel round di sorpresa prendono gli orchi in fuga: chi resta intralciato non fugge, si rannicchia e si arrende (SRD, panico) |
| Treant senza velocità (DEV#15, PT#7, DM#6) | 🟡 | CORRETTO | Aggiunti velocità 9 m, RD 10/adamantio e durata 1 ora (D74). Corretta anche la frase «se al −1000 li ha già chiamati insieme, è spenta»: vale di notte, all'alba no (D65) |
| Effetto della Cintura non scritto (DEV#16, PT#9) | 🟡 | DECISIONE DM | Scritto l'effetto come in `state.md` §6: azione gratuita prima del colpo, +2d6. Le tre fonti però non coincidono su cariche e danno (decisione 4) |
| Tempra mai chiesta (DEV#18) | 🟡 | CORRETTO | Dichiarato nel §2 che è voluto, perché è una transizione |
| *Protezione dal Male* e Corona, deviazione (DEV#19) | 🟡 | CORRETTO | Nel §0-bis: stesso tipo di bonus, non si sommano, vale il più alto (SRD) |
| «Uno o due» orchi, il capo (DEV#20, PT#11, DM#10 prima metà) | 🟡 | CORRETTO | Restano due orchi, come dice il box; il capo tira a parte e se fa 20 è uno dei due. Scritto cosa fanno i due scossi senza capo |
| Blocchi di nani che «travolgono» (DEV#21) | 🟡 | lasciato | È la regia del DM (D90); dire se un blocco uccide in automatico un hobgoblin impegnato da un PG è una regola nuova |
| Salita a piedi verso le mura (PT#5) | 🟡 | lasciato | Distanza e tempo stanno nelle mappe del 1372; scriverli qui vuol dire fissarli |
| Pergamene di *ristorare*: quante e di chi (PT#13) | 🟡 | lasciato | Le vende Brynja in `DEF-4` (4, 800 mo). Se le pergamene comprate al −1000 tornano col gruppo dipende dalla regola del ritorno del §0-bis («le pozioni antiche svaniscono all'alba»): è da far confermare al DM insieme alla decisione 2 |
| Tempo d'apertura del portale, round o minuto (PT#14) | 🟡 | CORRETTO | Un round, come nella Scena 3 (D77): il §6 ora dice «nel round che serve ad aprire il portale» |
| Cosa sanno i prigionieri (PT#15) | 🟡 | lasciato | Sarebbe canone nuovo sull'orda |
| Luogo abitato: rimedi, riparazioni, identificazioni, prezzi (PT#16) | 🟡 | lasciato | In piena battaglia; il banco del 1372 è dell'ARC-08 (`ARC08-17-BANCO-HAMMERFIST-1372.md`) |
| «In scena» della Scena 3 senza gli hobgoblin (DM#1) | 🟡 | CORRETTO | Aggiunti al contratto, con una riga di Comparse (armatura completa, scudo pesante, il fischietto del Bestiario) |
| Prima frase della Scena 2 parla della Scena 3, grassetti di servizio (DM#2) | 🟡 | lasciato | È ordine della pagina, non un buco; lo spostamento tocca la vista e va fatto con l'apparato |
| 8 pf del capo solo nella cella di Artemis (DM#12) | 🟡 | CORRETTO | Ripetuti nelle statistiche degli orchi della Scena 3 |
| Tavola A8 assente, percentuale ambigua (DM#13) | 🟡 | lasciato | La tavola sta in `DEF-2`; il «60→80%» va deciso con l'arco |
| Nessuna immagine della scena (DM#14) | 🟡 | lasciato | Le immagini non si generano in questo giro |
| «Giorno 3» e «3g 15h» (DM#15) | 🟡 | RESPINTO | Il master lo spiega già sopra la tabella del §0-bis: «Il numero è quanto resta del conto alla rovescia dell'assedio» |
| Durata della serata, quando scegliere il fast-play (DM#16) | 🟡 | lasciato | Una soglia di tempo è una scelta del DM, e nessuna fonte la dà |

## Decisioni per il DM

### 1. Quanti pf ha Madre Dana quando arrivano i PG

Il re non muore in DEF-5 perché Dana prende su di sé il colpo (D92). Adesso il
master le dà CA 29 e 142 pf massimi, ma non dice quanti gliene restano dopo due
giorni sulle mura. Con i pf pieni una freccia da 1d8 non la abbatte mai, e la
riga del §6 «Madre Dana cade», con una Cantitrice che apre il portale, non
scatta.

**Domanda.** Fissa i pf di Dana all'arrivo, prima della guarigione dell'Apparizione.

- **Piena** (142): il colpo non le costa niente, e il ramo della Cantitrice resta sulla carta.
- **Metà** (71): cade solo se gli hobgoblin passano in molti e tirano per più round.
- **Allo stremo** (20, più i 2d8 dell'Apparizione): un critico o due frecce la abbattono, e il portale lo apre una Cantitrice con la voce che trema.

**Raccomandata: allo stremo.** È la versione più terrificante e la più coerente
con «ha speso tutto sulle mura»: il gesto della D92 costa qualcosa, e la
contingenza già scritta prende vita. Cadere non è morire: a −1 si stabilizza,
e resta il named survivor dell'ARC-08.

### 2. Il tetto dell'orologio delle torri, e il riposo nella caverna

Dopo la pulizia «ogni 10 minuti Fauci abbatte una torre della Porta Ovest»
(D77). Nessun file dice quante torri ci sono né cosa succede quando finiscono.
Un gruppo che mura la porta e dorme otto ore consuma 48 tacche, e il §8 dice che
il 14° livello si prende al primo riposo, «dopo la battaglia di Hammerfist».

**Domanda.** Decidi cosa succede quando i PG si fermano più di un'ora.

- **Breccia**: dopo sei tacche (un'ora) la Porta Ovest cade; dormire si può, ma l'ARC-08 si apre sulla riga «breccia aperta» del §0-bis, con il livello preso.
- **Torri contate**: fissi il numero delle torri; ognuna in meno pesa nell'ARC-08, e a zero c'è la breccia.
- **Il re non lo permette**: Re Thorek ordina di salire subito, e la sosta oltre l'ora non si offre.

**Raccomandata: breccia.** Usa una riga del §0-bis che esiste già, fa pagare il
riposo invece di vietarlo, e risponde anche alla domanda del livello. Insieme
conviene dire se le pergamene comprate al −1000 tornano col gruppo (PT#13).

### 3. Il ramo «meno luminoso»: valgono l'ordine di Thorik e il preavviso di Artemis?

Nel ramo duro gli hobgoblin entrano alla fine del round di sorpresa, un round
prima. L'ordine di Thorik è scritto perché il muro di scudi si faccia sul varco
«prima che entrino», e il preavviso di Artemis arriva solo nel round 1. Con il
calendario anticipato nessuno dei due arriva in tempo.

**Domanda.** Stabilisci quanti hobgoblin passano l'anello nel ramo «meno luminoso».

- **Valgono entrambi**: tre con l'ordine, due con il preavviso, come nel ramo luminoso; il ramo duro cambia solo per gli orchi.
- **Solo l'ordine**: ne passano tre, e il preavviso non c'è.
- **Nessuno**: ne passano cinque, qualunque cosa facciano Thorik e Artemis.

**Raccomandata: nessuno.** È la lettura che segue dal calendario, ed è la più
dura: il ramo «meno luminoso» deve pesare, e cinque sergenti con sei orchi
scossi fanno lo «scontro vero di 3-4 round» che la D77 promette.

### 4. La Cintura della Devastazione: quante cariche e quanti danni

Tre fonti non coincidono. `state.md` §6 dice circa 3 al giorno, +2d6. La scheda
della Cintura dice 4 al giorno per sempre dal rito della Sala della Forgia
(decisione DM 2026-07-04), +2d6. `DEF-4` Scena 8 dice 3 al giorno a +2d6, +3d6
e +4d6. DEF-5 ora scrive «3 cariche, +2d6», cioè `state.md`.

**Domanda.** Scegli il valore della Cintura che vale da DEF-4 in poi.

- **Scheda**: 4 cariche al giorno, +2d6 ciascuna; si correggono `state.md`, DEF-4 e DEF-5.
- **DEF-4**: 3 cariche, +2d6, +3d6, +4d6 in crescendo; si corregge la scheda.
- **State**: 3 cariche a +2d6; si correggono la scheda e DEF-4.

**Raccomandata: scheda.** È l'unica con una tua decisione datata. Sul totale
della giornata il crescendo di DEF-4 fa di più (9d6 contro 8d6), ma la scheda dà
una carica in più, e la scelta che il modulo vuole far pesare è proprio quante
cariche Tordek spende qui invece che contro Fauci.

## Secondo giro

Esiti dopo `VERIFICA.md`: CORRETTO 8 (3 PARZIALE, 1 NUOVO 🟠, 4 NUOVI 🟡) · IN ATTESA DM 4, lasciati come sono.

| Voce di VERIFICA | Gravità | Esito | Cosa ho fatto |
|---|---|---|---|
| DEV#1 + NUOVO 1 · l'arco va anche estratto | 🟠 | CORRETTO | Passare all'arco prende un round intero: la spada cade (azione gratuita), lo scudo si sfila e l'arco si prende (due azioni di movimento, senza Estrazione Rapida), e il tiro arriva il round dopo, a CA 19. Ai piedi dell'altare: arrivano a fine round 4, cambiano arma nel round 5, tirano al re dal round 6 se lo scontro dura ancora. ⚠️ Nel ramo luminoso il colpo della D92 quindi arriva solo se lo scontro supera i 5 round: questo pesa sulla decisione 1 (pf di Dana) |
| DEV#2 · ai piedi dell'altare | 🟠 | CORRETTO | Ha preso il tempo del tiro dal NUOVO 1 |
| PT#1 / DM#9 · le Cantitrici del §6 «con *cura ferite critiche*» | 🟠 | CORRETTO | La riga «Madre Dana cade» dice ora: «i loro incantesimi sono spesi sulle mura come quelli di Dana, Scena 3» |
| NUOVO 2 · «uno o due» nella Scena 3 | 🟡 | CORRETTO | «restano due orchi scossi (§0-bis)», come il §0-bis e il box |
| NUOVO 3 · box «il silenzio» | 🟡 | CORRETTO | La prima frase dice ora «*L'ultima spada cade sulla pietra, e il rumore se ne va con lei.*»: va bene sia se gli ultimi cadono sia se gettano le armi. Il box ha sempre 4 righe |
| NUOVO 4 · velocità di Durik | 🟡 | CORRETTO | Velocità 12 m, dalla scheda di Durik (`08-SCHEDA-DURIK.md`) |
| NUOVO 5 · il preavviso costa l'azione standard | 🟡 | CORRETTO | Parlare è un'azione gratuita (SRD): Artemis grida il preavviso e le resta l'azione standard |

Verifiche: `misura_craft.py --box` dà ancora 7 box per DEF-5, nessuno oltre le 12 righe e nessuna parentesi; `validate_modules`, `copertura_scene`, `domande_developer` e `validate_prosa` verdi. Resta da rigenerare l'apparato (`componenti.py --apparato`), come nel primo giro.
