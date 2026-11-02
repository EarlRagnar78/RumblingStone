# Arco 08, giro a freddo del 2026-10-19: la verifica

Verificatore: un agente nuovo, che non ha fatto né le letture né la correzione. Sola lettura sui file dell'arco (modifiche non committate del ramo, `git diff -- "08_La Battaglia Di Hammerfist/"`). Canone giocato: `origin/campaign-group-rumblingstone:campaign/state.md`. SRD: la copia locale in `corpus-prosa/grezzi/test-srd/srd-v3.5-md/`.

Sigle dei file come in `FIX.md`: **A** guida DM · **B** guida agli scontri · **C** esiti · **D** ponte d'arrivo · **E** Cerimonia · **F** `Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md` · **G** schede e regolamento. **Atlante** = `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`, che la correzione non ha toccato.

**Conteggio dei 74 🔴 e 🟠:** CHIUSO 20 · PARZIALE 15 · APERTO 0 · IN ATTESA DEL DM 39.
**NUOVI:** 🔴 0 · 🟠 2 · 🟡 10.

Comandi rifatti: `conformita_statblocchi.py --master` su A, B e G, «0 conti che non tornano» per ciascuno; `collaudo_mappe.py` su F, «5 mappe · 7 errori · 13 avvisi», con MAPPA 5 a «distanza 0» (i 7 errori sono le porte di 3Y e 3Z, che il giro non tocca); `validate_maps.py`, «✓ … 53 SVG … tutti ben formati, tracciabili e allineati». Coincidono con `FIX.md` §4.

---

## 1 · Tabella

Per gli IN ATTESA DEL DM con una parte corretta, la prova cita la parte corretta, che ho controllato.

### DEVELOPER

| Rilievo | Gravità | Giudizio | Prova (citazione dal file corretto) |
|---|---|---|---|
| DEV#1 | 🔴 | IN ATTESA DEL DM (D1) | Nessuna scelta fra le versioni. B: «15m [RUMBLING STONES] guardano» c'è ancora, F: «21-23 Duello finale: Thorik + Tordek + Artemis convergono» pure |
| DEV#2 | 🔴 | IN ATTESA DEL DM (D1) | Il denominatore è corretto nei sette file: A «PF Attuali: 180/337 (… i pf di partenza sono una decisione aperta del DM…)», B «220/337», F «PF 232/337». 25d12+175 fa 337. ⚠️ L'Atlante dice ancora «Wounded (-80 HP già, 232 rimanenti)», cioè 312 (NUOVO 1) |
| DEV#3 | 🔴 | CHIUSO | A e B: «per restare aggrappato vince una prova di lotta **contrapposta** (SRD), +24 contro i +43 di Fauci»; A: «una «CD 25» nel 3.5 non c'è»; C: «La presa di Orion da sola non basta, perché la lotta è contrapposta e Fauci ha +43 (SRD)»; F: «il peso da solo non forza la discesa». Nell'Atlante la presa forza ancora la discesa (NUOVO 1) |
| DEV#4 | 🟠 | CHIUSO | A e B: «Aegis Fang lanciata arriva al massimo a 15 m (arma da lancio improvvisata, SRD): contro un drago a 30-45 m non arriva»; «(+2 Ritornante *Dragondoom*, 1d10): un bersaglio per attacco» |
| DEV#5 | 🟠 | IN ATTESA DEL DM (D6) | La parte SRD è giusta in A, B ed F: «vento violento (SRD): TS Tempra CD 15 solo per le creature Piccole o minori»; «−4 agli attacchi a distanza (SRD). ⚠️ Vento violento più pioggia, per l'SRD, è una *tempesta*». Controllato su SRD Table: Wind Effects (Severe, −4, taglia Piccola, CD 15) e §Storms |
| DEV#6 | 🟠 | CHIUSO | A e G: «Morso +33 (2d8+10/19-20), 2 artigli +31 (2d6+5), 2 ali +31 (1d8+5), colpo di coda +31 (2d6+15)»; appendice di A: «Morso +33 (2d8+10)». 25 + 10 − 2 = 33 |
| DEV#7 | 🟠 | CHIUSO | A e G: «25 DV sono i dadi dell'età **Vecchio** (25d12+125, naturale +24, RI 22, soffio 16d4)»; «Percezione cieca 18 m»; «Raggio 90m (potenziamento: l'SRD dà 9 m per categoria d'età, 63 m all'adulto maturo)»; «A volontà (potenziamento: l'SRD dice 1/giorno)». Tutto torna con l'SRD |
| DEV#8 | 🟠 | IN ATTESA DEL DM (D6) | A: «`[INFERRED — needs DM confirmation: la scheda di Tempestas in ARC08-02 §2 non ha questa Sinfonia…]`»; F: «(LI 20) `[INFERRED — needs DM confirmation…]`» |
| DEV#9 | 🟠 | PARZIALE | Corretti la condizione («SE IL CAVALIERE CADE … solo se lo disarcionano davvero») e le opzioni («*caduta morbida* non è nella lista del druido»; «15d6 (media 52): coi suoi 95 pf il cavaliere arriva a terra vivo»). Resta in A e in B la doppia CD: «(PROVA RIFLESSI CD 20)» nello schema e «Tentare di afferrare il cavaliere (Riflessi CD 18)» sotto |
| DEV#10 | 🟠 | IN ATTESA DEL DM (D2) | Parte corretta, controllata sul Bestiario: «orchi berserker = … (GS 2, CA 13, pf 27, grande ascia +9, 1d12+9…)»; hobgoblin «(GS 2, CA 19, pf 23, spada lunga +6, 1d8+1)»; sergente «(GS 5, CA 21, pf 37, spada lunga +9, 1d8+4)». «Bugbear e guardie orog … decisione aperta del DM» |
| DEV#11 | 🟠 | IN ATTESA DEL DM (D11) | A e B, 3B: «Livello di Sfida: 17 (dichiarato, da riconteggiare … `[INFERRED…]`) · PE: Appendice C della guida, 2.600 al gruppo (650 a testa)». In B il 4A non è stato allineato (NUOVO 4) |
| DEV#12 | 🟠 | IN ATTESA DEL DM (D3) | «ROUND 14-15: L'ARRIVO DI GRIMJAW» resta in A e B |
| DEV#13 | 🟠 | PARZIALE | D: «**round 9-10** dell'ultima resistenza (guida, Incontro 3C); i giocatori prendono i loro PG al round 11»; F: «ROUND 9-10 — L'APPARIZIONE» e «cura 2d8 a tutti (`[CANONE — DM 2026-10-18]`…)». Restano due copie al round 8: A r.2133 «MAPPA 5 REVISED (67×53, 1,5 m: altare, statue, ondate, apparizione round 8)» e l'Atlante, «Round 8 combattimento: Sfera dorata tricolore» e «EVENTO CLIMAX (Round 8)». Il round di Grimjaw resta al DM |
| DEV#14 | 🟠 | CHIUSO | A e B: «THORIK … **Aura della Forgia Eterna** (Corona, Rituale 4): 1/settimana, +4 di morale»; «HELLA … 1d4+1 lupi crudeli (dalla lista di 3°: SRD)»; «**Pelle coriacea:** +5»; «**Pugno stordente** con TS su Tempra, CD 16 + mod. di Sag»; «**Deflagrazione occulta 6d6**». Numeri controllati (SRD e matrice degli artefatti del ramo). Il blocco «Effetti dell'Apparizione» contraddice la correzione (NUOVO 3) |
| DEV#15 | 🟠 | CHIUSO | D: «**−4 DES / +2 COS / +4 CAR permanenti** … ⚠️ **Nessun −2 COS.** Al rito di Hella ha donato il **+2 di deflessione della Corona**», identico a `state.md` §1 del ramo |
| DEV#16 | 🟠 | PARZIALE | La nota c'è solo in A: «**Economia d'azione (SRD):** saltare dal gufo è movimento, la forma selvatica è un'azione standard…». In F la sequenza resta in una riga, «SALTA sul dorso del drago → Forma Selvatica Orso Crudele», e in B la nota manca, mentre `FIX.md` dice «in A, B ed F». Corretti la guarigione («torna umano quando tocca terra e il round dopo si cura») e i «6 attacchi» di F |
| DEV#17 | 🟠 | IN ATTESA DEL DM (D2) | I gufi non hanno ancora una scheda |
| DEV#18 | 🟠 | PARZIALE | A e B: «**Morale: vale solo il più alto**»; «**Carica:** +2 al tiro per colpire (SRD); nessun bonus ai danni»; «**TOTALE:** +7 … +11 con la benedizione sacra». La MAPPA 4X di F, che il rilievo citava, è rimasta com'era: «**+2 danni** in carica, +2 morale di circostanza»; «(+4 morale finale, cumulativo)»; Evoluzione «+2 danni carica» |
| DEV#19 | 🟠 | CHIUSO | A e B: «**Le tre unità di testa** (Nani d'élite, AU +9, `ARC08-02` §6): **AU +16** al primo urto … Il cuneo si risolve con AU contro DU, non colpo per colpo»; B: «**Comandare un'unità:** … prova di Carisma CD 15, +2 all'AU», come G §4. Sul +16 c'è un'ambiguità (NUOVO 5) |
| DEV#20 | 🟠 | IN ATTESA DEL DM (D11) | Le righe di scala non ci sono |
| DEV#21 | 🟠 | IN ATTESA DEL DM (D4) | Il tiro che uccide Re Thorek non è scritto |
| DEV#22 | 🟠 | CHIUSO | A: «**~500 morti e ~400 dispersi in rotta** … Se i PG inseguono i fuggiaschi, cambiano i morti, non il totale»; «fuggito gravemente ferito (ramo default D10), o ucciso»; B: «Superstiti: i dispersi»; F: «in tutti e due i casi l'orda perde i 900 dell'avanguardia (D11)» |
| DEV#23 | 🟠 | IN ATTESA DEL DM (D9) | C ed E: «`[INFERRED — needs DM confirmation: 118 + 92 + 9 fa 219]`». Il 210 non compare nello stato del ramo, quindi il flag è legittimo |
| DEV#24 | 🟠 | CHIUSO | E: «**+2 di circostanza a Diplomazia** con i nani del Vale … (`ARC08-10-ESITI-E-CONTINGENZE.md` §6.2, canone del DM 2026-10-18)» |
| DEV#25 | 🟠 | IN ATTESA DEL DM (D8) | E: «`[INFERRED — needs DM confirmation: la guida e ARC08-02 la tengono fuori dalla compagnia di Lunapiena; decisione aperta]`». Sulla posizione del flag, NUOVO 10 |
| DEV#26 | 🟠 | PARZIALE | La scheda c'è: «`Bestiario/mostri/hobgoblin-veterans-warrior6-cr5.md`: GS 5, CA 19, pf 43, spada lunga +10/+5, 1d8+2», e torna col Bestiario. Il rimando «cinque unità di massa, `ARC08-02` §5» però non porta a niente: in G §5 non c'è un'unità di hobgoblin d'élite (ci sono «FANTERIA HOBGOBLIN (Standard)» e «HOBGOBLIN GUERRIERI (Warrior 3)»). La tattica degli «ultimi fedeli» resta un residuo dichiarato |
| DEV#27 | 🟠 | IN ATTESA DEL DM (D7) | Il blocco «Se lo divinano» non c'è |

### PLAYTESTER

| Rilievo | Gravità | Giudizio | Prova (citazione dal file corretto) |
|---|---|---|---|
| PT#1 | 🔴 | IN ATTESA DEL DM (D2) | Come DEV#10: tre schede verificate; «Bugbear e guardie orog di Grimjaw non hanno ancora una scheda nel Bestiario» (nemmeno `ls Bestiario/mostri` ne trova) |
| PT#2 | 🟠 | CHIUSO | Come DEV#14; e in più A e B: «**Thorik:** Aegis Fang +2 Ritornante *Dragondoom*» al posto di «Aegis Fang +3» |
| PT#3 | 🟠 | IN ATTESA DEL DM (D3) | Arrivo dei PG allineato (D, F, A: «ROUND 9-10: L'APPARIZIONE MIRACOLOSA»); Grimjaw resta «Finale \| 9-10» in F e «ROUND 14-15» in A |
| PT#4 | 🟠 | IN ATTESA DEL DM (D4) | F: «⚠️ per l'SRD *guarigione* fa finire la condizione di avvelenato … `[INFERRED…]`», ed è giusto (SRD *Heal*). In A la prova medica dice ancora «Incantesimo Heal: Recupera alcuni PF ma non cura l'avvelenamento da acido», senza flag |
| PT#6 | 🟠 | IN ATTESA DEL DM (D5) | A: «📎 Regia, fra il Cuore della Montagna e i bastioni `[INFERRED…]`: passa mezza giornata … Non c'è il riposo di otto ore». Il default aggiunge un fatto inventato (NUOVO 9) |
| PT#7 | 🔴 | IN ATTESA DEL DM (D1) | Come DEV#1 |
| PT#8 | 🔴 | IN ATTESA DEL DM (D1) | «**Inseguire il Drago** (combattimento aereo finale)» e «**Attacco Finale a Distanza**» sono ancora senza regole |
| PT#9 | 🔴 | IN ATTESA DEL DM (D1) | Come DEV#2 |
| PT#10 | 🟠 | CHIUSO | Come DEV#3; e A: «**Niente lacerazione:** l'orso crudele SRD ha artigli +19 (2d4+10) e morso +14 (2d8+5), e basta» |
| PT#11 | 🟠 | IN ATTESA DEL DM (D6) | Parte corretta in A e B: «*invocare il fulmine*, 3d10 a fulmine nella tempesta (3d6 fuori), gittata media (SRD)» |
| PT#12 | 🟠 | PARZIALE | Opzioni corrette come in DEV#9; la doppia CD 20/18 resta; l'interrogatorio è in D7 |
| PT#13 | 🟠 | PARZIALE | A: «**Risultato atteso del Massacro Aereo** *(… gli esiti non sono un copione…)*» e «**RISULTATI ATTESI DELLE STRAFING**». In B l'intestazione è ancora «**RISULTATI DELLE STRAFING:**» e solo il round 6 ha la riserva; «Round 8: 6 Giganti morti» resta un fatto |
| PT#14 | 🟠 | PARZIALE | Come DEV#18: A e B sono corretti, la MAPPA 4X di F no |
| PT#15 | 🟠 | PARZIALE | A rimanda a «le unità nemiche ancora in campo sono quelle del Registro (`ARC08-03-REGISTRO-PERDITE.md`) a fine Sessione 3», ma il Registro è un foglio di tracciamento vuoto («Quantità Totale: 30 Unità», quadretti da annerire), e col default di C §5.5 nessuno lo ha riempito. L'elenco delle unità nemiche rimaste all'inizio della Sessione 4 continua a mancare |
| PT#19 | 🔴 | CHIUSO (respinto a ragione) | `ARC08-17-BANCO-HAMMERFIST-1372.md` r.151: «Dopo la Cerimonia la fucina riapre per un giorno e mezzo», poi «Cosa compra, e a quanto» e «I servizi». A ora rimanda: «**Vendere, comprare, identificare** … il banco socchiuso dei Giorni 21-22, `ARC08-17` §3» |
| PT#20 | 🟠 | PARZIALE | Corretti i numeri: «**Circa 30.000 mo** in gemme ciascuno», «non subito, dopo Rethmar», confermati da `ARC08-17` §2. Restano senza quantità «**Seguaci:** Giovani nani vogliono servire gli eroi» e «Ciascun PG riceve un feudo nelle montagne»; in C resta l'armeria «a costo nullo», senza tetto (è canone del DM 2026-10-18, ma un tetto ci vuole) |
| PT#25 | 🟠 | IN ATTESA DEL DM (D8) | Come DEV#25 |
| PT#27 | 🟠 | CHIUSO | D: «Nessun −2 COS» e «**Topazio** (Tempo) e **Smeraldo** (Terra) accesi; il **Rubino** … **si consuma** nel salto», in linea con la matrice degli artefatti del ramo («il Rubino si consuma nel ritorno al 1372 (D16)»). Sulla stessa pagina resta «Corona a 3 gemme» (NUOVO 6) |
| PT#28 | 🟠 | IN ATTESA DEL DM (D9) | — |

### DM

| Rilievo | Gravità | Giudizio | Prova (citazione dal file corretto) |
|---|---|---|---|
| DM#1 | 🔴 | IN ATTESA DEL DM (D10) | A e B: «**La serata**: Incontro 3B e Sessione 4 fino al campo della vittoria. La Cerimonia … è un'altra serata», con flag `[INFERRED]` |
| DM#2 | 🔴 | IN ATTESA DEL DM | C §5.5: «Se il flashback coi pregen non è stato giocato `[INFERRED…]`»; le righe tornano con le tabelle §5.1-§5.3 (la riga «parziale» di *Comandanti logorati* è proprio «Uno solo dei due logorato»). D: «vale il default di `ARC08-10-ESITI-E-CONTINGENZE.md` §5.5» |
| DM#3 | 🔴 | IN ATTESA DEL DM (D1) | Come DEV#1 |
| DM#4 | 🟠 | IN ATTESA DEL DM (D3) | Come DEV#13 per la parte corretta |
| DM#5 | 🟠 | CHIUSO | Come DEV#15 |
| DM#6 | 🟠 | PARZIALE | Azioni dei PG corrette, come DEV#14. Ma il castigo *Dragondoom* che il rilievo segnalava («3/giorno contro i draghi … che il master non usa mai contro Fauci») non compare in nessuna riga del 4A. E A, «Effetti dell'Apparizione», ha ancora «**PRESENZA REGALE (Corona di Adamantio):** … +6 bonus morale a tutti i tiri per 1 ora» |
| DM#8 | 🟠 | IN ATTESA DEL DM (D1) | Come DEV#2 |
| DM#9 | 🟠 | IN ATTESA DEL DM (D6) | Come DEV#5 e DEV#8 |
| DM#10 | 🟠 | PARZIALE | Come DEV#18 (F) e DEV#19 |
| DM#11 | 🟠 | IN ATTESA DEL DM (D4) | — |
| DM#12 | 🟠 | IN ATTESA DEL DM (D2) | Come DEV#10; la regia dice anche quando si usa la massa: «Il cuneo si risolve con AU contro DU, non colpo per colpo» |
| DM#13 | 🟠 | IN ATTESA DEL DM (D5) | Come PT#6 |
| DM#14 | 🟠 | CHIUSO | Il box del 3C c'è: «Proprio quando gli orchi sfondano l'ultima barricata…». D: «Ha fiato per una frase sola … *«Moradin ha… ascoltato… la Forgia… eterna…»*», e la frase è nell'Atlante (r.1097) |
| DM#15 | 🟠 | CHIUSO | Come PT#20 per la contraddizione: 30.000 mo in A (corpo e Appendice C) e in B |
| DM#16 | 🟠 | CHIUSO | Come DEV#24 |
| DM#17 | 🟠 | CHIUSO | A: «Le 210 asce sul campo al tramonto sono la sepoltura di guerra; la Cerimonia delle 100 Asce è un altro rito»; E: «le asce dei caduti restano piantate sul campo dalla sera della battaglia, ed è un altro rito»; F: «un altro rito dalla Cerimonia delle 100 Asce del Giorno 21». In B la frase non c'è, ma B non rimanda alla Cerimonia, quindi la confusione non nasce |
| DM#22 | 🟠 | PARZIALE | A: «**In un'ora si legge**: …», con C §5.5 dentro. Le durate delle scene della Sessione 4 restano un residuo dichiarato. Che MAPPA 5, MAPPA 4, C §4-§5 e G §1 si leggano in un'ora non è misurato (la vista dava 83 minuti per tutto F) |

### COLLAUDATORE-MAPPE

| Rilievo | Gravità | Giudizio | Prova (citazione dal file corretto) |
|---|---|---|---|
| MAP#1 | 🔴 | CHIUSO | F r.06: «🏰 … 🏰 ⬜ ⬜ ⬜ ⬜ ⬜ ⬜ 🏰 …» alle colonne 31-36 (AE-AJ), sotto le 🚪 di r.05; `collaudo_mappe`: MAPPA 5 «distanza 0» |
| MAP#2 | 🔴 | CHIUSO | F r.27-29: «⬜ ⬜ ✨ ⬜ ⬜» / «⬜ ⬜ 🔮 ⬜ ⬜» / «🔵 ⬜ ⚫ 🔵 ⬜»; Evoluzione A: «l'altare (AF26-AJ30) è una piattaforma su cui si sale, e solo 🔮 AH28 blocca il passo» |
| MAP#3 | 🟠 | PARZIALE | Corretti i tre schemi citati (A r.2211 «TUNNEL INGRESSO» in testa; «MAPPA 3B: LA SVOLTA» «TUNNEL → 🔴 GRIMJAW 🔴» in testa; «LA TRASFORMAZIONE» «🚪 PORTA DI MITHRAL + TUNNEL 🚪» in testa; idem in B). Resta in A un quarto schema, «MAPPA 5: IL CUORE DELLA MONTAGNA (SESSIONE 3)» (r.2132-2165): «NORD ↑» in testa e «🕳️ TUNNEL PRINCIPALE 🕳️ … (INGRESSO NEMICI)» in fondo |
| MAP#4 | 🟠 | IN ATTESA DEL DM (D3) | — |
| MAP#5 | 🟠 | IN ATTESA DEL DM (D3) | Il residuo dipende da D3, quindi non è un residuo vero: si chiude dopo la scelta |
| MAP#6 | 🟠 | PARZIALE | F: «(60 colonne × 68 righe · 3 m/quadretto)»; A e B: «(schema; griglia 180 m × 204 m)». Ma lo SVG rigenerato in questo giro dice ancora «scala 1,5 m/quadretto» e «7,5 m (5 quadretti)» (`rendered/…map05…svg` e `rendered-texture/…map05…svg`; rifatto il render nello scratchpad: stesso risultato). Il PNG non è il solo a sbagliare (NUOVO 2) |
| MAP#7 | 🟠 | IN ATTESA DEL DM (D1) | — |
| MAP#8 | 🟠 | IN ATTESA DEL DM (D1) | — |
| MAP#9 | 🟠 | IN ATTESA DEL DM (D1) | — |
| MAP#10 | 🟠 | IN ATTESA DEL DM (D1) | — |
| MAP#11 | 🟠 | IN ATTESA DEL DM (D1) | — |

### I RESPINTO e gli AL DM

- **PT#19**, unico RESPINTO fra i 🔴 e i 🟠: la riga citata esiste («Dopo la Cerimonia la fucina riapre per un giorno e mezzo») e §3 risponde a quello che il rilievo chiedeva (chi compra, a quanto, i servizi). Il rifiuto regge.
- **Respinti fra i 🟡**: PT#31/DM#23 («### **APPENDICE C: RIASSUNTO XP E RICOMPENSE**» c'è, r.3447), DM#29 (3C e 3D ci sono, «#### **INCONTRO 3C: Il Miracolo della Sfera**»), MAP#21 («**MAPPA 3B: LA SVOLTA**», r.2397). Reggono tutti e tre.
- **Le parti «vere in ogni versione» degli AL DM**: denominatore 337, meteo SRD, *invocare il fulmine*, schede del Bestiario, arrivo dei PG ai round 9-10, cura 2d8. Sono corrette nei sette file, salvo le copie dell'Atlante (NUOVO 1) e il rimando di A r.2133 (DEV#13).

---

## 2 · Controlli sui numeri introdotti dalla correzione

| Numero nuovo | Conto rifatto | Esito |
|---|---|---|
| Morso +33, secondari +31 | BAB 25 + For 10 − taglia 2 = 33; −2 di Multiattacco = 31 (SRD Old: +32 con For 29) | ✓ |
| Pf /337 | 25 × 6,5 + 175 = 337,5 | ✓ |
| Presenza terrificante 63 m all'adulto maturo | 30 ft × 7 = 210 ft ≈ 63-64 m | ✓ |
| Vecchio 25d12+125, naturale +24, RI 22, soffio 16d4 | tabella *Black Dragons by Age* | ✓ |
| Percezione cieca 18 m; l'invisibile resta occultato | SRD: *Blindsense* 60 ft, il bersaglio conserva l'occultamento | ✓ |
| Thorik immune alla Presenza col *Mind Blank* della Corona | stato del ramo: «**Mind Blank permanente**»; SRD: «Frightful presence is a mind-affecting fear effect» e *mind blank* «protects against all mind-affecting spells and effects» | ✓ |
| Slot di Orion 6/7/7/6/5/4/4/3 | druido 14° 6/5/5/4/4/3/3/2 + bonus di Sag 24 (+7): 0/2/2/2/1/1/1/1 | ✓ |
| Aegis Fang lanciata: −4, 3 m, max 15 m | SRD, arma da lancio improvvisata, cinque incrementi | ✓ |
| Deflagrazione 6d6 a 18 m | stato del ramo «Eldritch Blast 6d6»; gittata 60 ft | ✓ |
| *Pelle coriacea* +5 a LI 12 | +2 al 3°, +1 ogni 3 livelli, tetto +5 | ✓ |
| *Evocare alleato naturale V*: 1d4+1 lupi crudeli | SRD: 1d4+1 «from a lower-level list»; il lupo crudele è nella lista di 3° | ✓ |
| Pugno stordente CD 16 + Sag | 10 + ½ di 13 (6) = 16 | ✓ |
| *Muro di pietra* di Hella | SRD: «Level: Clr 5, Drd 6, Earth 5, Sor/Wiz 5»; Hella è druida 12 | ✓ |
| Vento: Tempra CD 15 per i Piccoli; pioggia −4; tempesta = niente tiri con armi | SRD Wind Effects (Severe 31-50 mph) e §Storms. 80 km/h ≈ 50 mph | ✓ |
| *Invocare il fulmine* 3d6 / 3d10 | SRD | ✓ |
| Caduta da 45 m = 15d6, media 52 | 150 ft; media 52,5 contro 95 pf | ✓ |
| Frecce della Morte: Fauci muore solo con 1 naturale | CD 20 contro Tempra +21 | ✓ |
| Carica +7 / +11 | morale 4 + carica 2 + altura 1 = 7; +4 sacro = 11 | ✓ come somma; la base è ambigua, NUOVO 5 |
| AU +16 / +20 delle tre unità di testa | AU +9 (G §6) + 7 = 16; +4 = 20 | ✓ come somma; NUOVO 5 |
| «Comandare un'unità»: Car CD 15, +2 AU | G §4: «Effettua una prova di Carisma (CD 15) … **bonus di +2 all'AU**» | ✓ |
| PE 3B 2.600 (650), Sessione 4 4.600 (1.150) | A, Appendice C r.3463-3467 | ✓ in A; B 4A non allineato (NUOVO 4) |
| 30.000 mo a PG; oggetto ~10.000 | `ARC08-17` §2, r.103 e r.111 | ✓ i numeri; la strada B non è un oggetto su misura (NUOVO 7) |
| Schede del Bestiario (berserk, regular, sergente, veterani) | GS, CA, pf, attacco e danno coincidono coi file | ✓ |
| ~500 morti + ~400 in rotta | 900, come C §1 | ✓ |
| Thorik −4 DES / +2 COS / +4 CAR, −1 CA, accelerato 3 round | stato del ramo §1 e r.454 | ✓ |
| Cerimonia «Giorno 21, due giorni dopo» la battaglia del Day 19 | `ARC08-12` r.37-38 | ✓ |
| C §5.5, default del flashback | le righe «pieno/parziale» esistono così in §5.1-§5.3 | ✓ |

**La prosa dei box.** La correzione ha toccato tre box. Il ponte cambia «le porte di mithral si spezzano» in «l'ultima barricata si spezza», per allinearsi al box del 3C: si perde il mithral, ma le porte restano nell'elenco sopra e il box resta uno, senza tagli. Il box «Un mese dopo» cambia solo l'origine delle scaglie e tiene il resto. Nel box dell'Atto 2 della Cerimonia le figure passano da tre a due e sparisce «coordinato — non casuale» (NUOVO 8). Nessun monologo spezzato, nessun box allungato.

---

## 3 · NUOVI

| # | Gravità | Errore introdotto o lasciato dalla correzione | Prova |
|---|---|---|---|
| 1 | 🟠 | **L'Atlante non è stato allineato.** La regola del giro (`module-standard`, passo 4) vuole la stessa mappa corretta anche nell'Atlante, che invece conserva quasi tutto quello che il giro ha corretto in F: l'Apparizione al round 8, la presa di Orion che forza la discesa, i 312 pf, la Deflagrazione da 7d6, la tempesta di Tempestas col *controllare tempo* | Atlante r.1069 «Round 8 combattimento: Sfera dorata tricolore materializza 3m sopra altare»; r.1142 «EVENTO CLIMAX (Round 8)»; r.1149 «TS Will CD 25 O shaken»; r.1272 «Wounded (-80 HP già, 232 rimanenti)»; r.1287-1290 «Grapple check (+18) vs Fauci … Riding drago forced downward»; r.1293 «Eldritch Blast spam (7d6, 250ft range)»; r.1266 «*Control Weather* + *Call Lightning Storm* combo» |
| 2 | 🟠 | **La scala di MAPPA 4 è sbagliata nello SVG che il giro ha rigenerato.** `FIX.md` dice che «la barra da 1,5 m sta nel PNG, fuori da questo giro»: ce l'hanno anche i due SVG rigenerati. Il renderer non legge la scala dalla riga «Dimensioni» fuori dal blocco della griglia. Chi misura sullo SVG dimezza ancora tutte le distanze | `rendered/Hammerfist-L3-REVISED-Ultra-Clear_map05_…svg`: «scala 1,5 m/quadretto», «7,5 m (5 quadretti)»; lo stesso in `rendered-texture/`; rifatto con `render_map_svg.py --map 5`: «scala 1,5 m/quadretto» |
| 3 | 🟡 | Il blocco degli effetti dell'Apparizione dà ancora alla Corona una «Presenza Regale» da +6, che la correzione, dieci righe più in là, dichiara inesistente | A r.2423-2425: «**PRESENZA REGALE (Corona di Adamantio):** … +6 bonus morale a tutti i tiri per 1 ora» contro A r.2556: «La «Presenza Regale +6 a 18 m» della prima stesura non è un potere della Corona» |
| 4 | 🟡 | I PE sono allineati all'Appendice C nel 4A di A, non in quello di B | A: «PE: Appendice C della guida, 4.600 al gruppo per la Sessione 4 (1.150 a testa)»; B r.964: «*Livello di Sfida: 20 (6.000 PE)*» |
| 5 | 🟡 | L'AU +16 della carica non dice se il +4 di morale prende il posto del morale dell'unità o si somma. Le unità di testa hanno già «Morale Iniziale: +2», e «Guardia del Re: … +2 al morale» entro 9 m da Re Thorek, su una scala da −5 a +5. Si può arrivare a +16, +18 o +20 per la stessa unità | A e B: «**AU +16** al primo urto (+20 con la benedizione sacra)»; G §6: «**Morale Iniziale:** +2», «**Guardia del Re:** Se entro 9m da Re Thorek, ottiene +2 al morale»; G §4: «Il morale è un valore da -5 a +5 che si applica all'AU» |
| 6 | 🟡 | Nel ponte la riga dello stato e il beat d'ingresso dicono due Corone diverse | D, tabella: «**Topazio** (Tempo) e **Smeraldo** (Terra) accesi; il **Rubino** … **si consuma** nel salto»; D §3.2: «**Thorik** (guerriero, Corona a 3 gemme)» |
| 7 | 🟡 | La ricompensa «oggetto su misura» viene attribuita alla strada B, che dà invece le reliquie del 372, e contraddice `ARC08-17` §2. L'Appendice C promette ancora l'oggetto dei fabbri | A: «**Un oggetto su misura per PG** (~10.000 mo, `ARC08-13` §3), per la strada B di `ARC08-17` §2»; `ARC08-17` §2: «L'oggetto magico su misura … **non in tempo**» e «**B · Le reliquie del 372**»; Appendice C: «un oggetto magico personalizzato creato dai mastri fabbri nanici» |
| 8 | 🟡 | Nel box dell'Atto 2 la correzione ha riscritto canone senza decisione: le figure scendono da tre a due ed è sparito «coordinato — non casuale». È lo stesso file che la cronologia chiama «il file canonico della Cerimonia (D3, da non riscrivere)». La riscrittura si allinea alle note per il DM, ma il DM va avvisato | E §3: «**due figure venute da fuori** … Non sono venute insieme»; prima: «**tre figure straniere** … Il loro arrivo è coordinato — **non casuale**»; `ARC08-12` r.47-48 |
| 9 | 🟡 | Il default D5 inventa una causa per i bastioni riconquistati, e quella causa non regge nel luogo: la Sfera esplode nella caverna sotto la montagna. Che i nani «risalgono dalle gallerie della cittadella», poi, la H3-1 non lo dice: per lei il tunnel porta lontano da Hammerfist | A: «la retroguardia nemica sui bastioni ha ceduto alla luce della Sfera»; «I nani risalgono dalle gallerie della cittadella»; F, H3-1: «Nord = tunnel (dentro la montagna, LONTANO da Hammerfist)» (citato da DM#13) |
| 10 | 🟡 | Due `[INFERRED]` stanno dove il canone c'è già. In F la regola «Dana riposata» è segnata come inferita, ma A la dà come decisione del DM. In E il flag su Lythiel sta sulla riga che coincide col canone del ramo, mentre le righe di A e G che lo contraddicono restano senza flag | F: «… è il ramo «Dana riposata», e allora Re Thorek non è a 8 pf `[INFERRED — needs DM confirmation]`»; A r.419: «Vale per Dana riposata, cioè il mattino della battaglia … (DM 2026-10-18)». Stato del ramo: «Direct recognition during Hammerfist Battle Sessione 4; canonized 2026-05-04»; A r.532: «che compare solo alla Cerimonia delle 100 Asce» |
| 11 | 🟡 | Lo schema del contrattacco promette ancora quello che il testo sotto ha tolto | A e B, «CONTRATTACCO COORDINATO»: «[WARLOCK] ELDRITCH STORM / ATTACCHI AREA»; sotto: «Deflagrazione occulta 6d6 sui fuggitivi; ad area solo con l'invocazione di forma che la sua scheda abbia» |
| 12 | 🟡 | I bonus della carica sono corretti in A e B ma non nella MAPPA 4X di F, che il giro ha toccato: la stessa carica ha due regole in due file aperti sul tavolo (è il residuo di DEV#18, PT#14 e DM#10, contato qui una volta come contraddizione fra copie) | F r.501: «**+2 danni** in carica, +2 morale di circostanza»; r.505: «(+4 morale finale, cumulativo)»; r.651: «+2 danni carica»; A e B: «**Carica:** +2 al tiro per colpire (SRD); nessun bonus ai danni» |

Il conteggio dei NUOVI nell'intestazione (🟠 2 · 🟡 10) è quello di questa tabella.
