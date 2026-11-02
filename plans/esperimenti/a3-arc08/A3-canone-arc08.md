# A3 · Il canone di ARC-08 contro lo stato del tavolo

> **Compito**: A3 di `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md`. Analisi in sola lettura, 2026-10-15. Nessun file del repo è stato modificato.
> **Categorie**: (a) contraddizione con il canone · (b) presupposto di un esito non ancora giocato · (c) dubbio che solo il DM può sciogliere.
> **Abbreviazioni**:
> - `ramo:` = `origin/campaign-group-rumblingstone`;
> - `state` = `ramo:campaign/state.md`;
> - `S4` = `ramo:campaign/sessions/2026-09-25_session-4.md`;
> - `DEF-4` / `DEF-5` = `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` / `ARC07-DEF-5-RITORNO-HAMMERFIST.md`;
> - `coh` = `skills/rumblingstone-campaign/references/campaign-coherence.md`;
> - `art` = `skills/rumblingstone-campaign/references/campaign-artifacts.md`;
> - `B4` = `07_…/PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`.
>
> I file di ARC-08 sono citati per nome breve dentro `08_La Battaglia Di Hammerfist/`: `01` = `ARC08-01-GUIDA-DM.md`, `enc` = `hammerfist_encounters-…-final.md`, `Cer` = `Cerimonia-delle-100-Asce.md`, e così via.
> **Dove sta il tavolo** (state:15-29, 86-94; S4:69): ARC-07 è in corso, e la prossima serata riprende da DEF-4 Scena 5, nella notte del ≈372 DR, con 3 tacche su 8. Restano da giocare il duello con Skullcrusher (B4), il Rubino e DEF-5. **ARC-08 non è giocato.** I PG sono al 13°.
> **Gerarchia delle fonti usata**: il ramo, poi i `[CANONE — DM]` dei master ARC07-DEF, poi `coh`/`art`, poi il Bestiario. Quando DEF-5 e ARC-08 divergono, vince DEF-5, che è il master più recente e porta le decisioni D-numerate. ARC-08 non porta nessuna decisione posteriore a DEF-5.
> Le deduzioni mie portano la marca **«dedotto»**.

---

## (a) CONTRADDIZIONI con il canone — 24

| # | Cosa presuppone ARC-08 (file:riga) | Cosa dice il canone (fonte:riga) | Correzione minima o domanda | Raccomandazione |
|---|---|---|---|---|
| A1 | `11`:31: Thorik ha «−2 CON permanente», sacrificato per la resurrezione | state:91: −4 DES / +2 COS / +4 CAR, «⚠️ Nessun −2 COS»; DEF-5:26 | sostituire la riga con i valori di state:91 | correggere subito: è un errore di scheda e cambia i pf |
| A2 | `11`:47-50: il Cuore di Moradin «aggancia» gli spiriti; il Rubino è la *Gem of Immutable Time* | DEF-5:196-199 (D32): il Cuore è speso e fuori dalla meccanica; art:127: il Rubino è *Dwarven Might*, si consuma come motore del viaggio, resta nell'incastro e la Corona si completa (+3, Senzienza) | riscrivere il paragrafo del ponte sul Rubino di art:127; togliere il Cuore come meccanica | correggere |
| A3 | `03`:14-24: banner dei «doni rifiutati» con la mappatura vecchia (Thorik sangue → RD 3/−; Artemis → Spontaneous Rebirth), con fonte in `_ARCHIVIO` | S4:10-15, 30; state:91-94 e 454: **tutti e tre i Doni sono stati dati**. Scudo del Custode da Thorik, RD 3/adamantino da Tordek, Rovo Eldritch da Artemis | sostituire il banner con «tutti e tre i Doni dati (S4)»; il ramo del rifiuto va solo nelle note per un gruppo futuro | correggere |
| A4 | Livello «13 consolidato, mai il 14°»: `01`:3257-3263; `10`:51; `13`:15-29; `enc`:1393-1397 | DEF-5:546-548 (D90): i PX del 14° sono già maturati all'arrivo, e il livello si prende al primo riposo dopo la battaglia di Hammerfist | allineare a D90; l'audit WBL di `13` va rifatto contro il 14° in uscita *(dedotto)* | correggere: D90 è posteriore a D9 |
| A5 | Effetti dell'Apparizione e della Sfera: `01`:2184-2187 e 2219-2232; `enc`:814-816 (TS Volontà CD 20 o spaventati, 2d4+4 pf, Daylight, armi +1, Bless, Grimjaw CD 18) | DEF-5:92-94 (D38/D90): +6 morale (netto +2), 2d8 pf, immunità alla paura per 1 ora, +3 m di velocità; orchi Volontà CD 25 o in panico | sostituire i numeri con quelli di DEF-5 §0-bis, oppure rimandare a DEF-5 | correggere: DEF-5 la gioca prima, ARC-08 la eredita |
| A6 | Dana e il re nella caverna: `01`:2034 (Dana «a metà incantesimi»); `01`:2059 e `enc`:700 (Dana lancia *Guarigione* sul re, «risana completamente»); `11`:65-66 (re «morente», Dana tenta di guarirlo) | DEF-5:488-491 (D92): Dana e le Cantitrici «hanno speso tutto sulle mura, niente ristorare», a Dana resta solo un *muro di pietra*; DEF-5:66 e 93: re a 8 pf, cosciente, stabilizzato ed esausto | togliere la *Guarigione*; Dana è senza incantesimi di cura; il re resta a 8 pf, esausto, finché lo curano i PG (DEF-5:451-459) | correggere |
| A7 | Cantitrici «Chierico 8 / Bardo 4, GS 11»: `01`:338, `02`:272. *CFG di massa* nel finale: `10`:200 | DEF-5:505 (D91): «chieriche di 5°, con *cura ferite gravi*»; DEF-5:489: hanno speso tutto | ~~ridurre lo statblock a chierica 5~~ **Superato dal DM il 2026-10-17** (thread delle schede, PR #241): le Cantitrici restano Chierico 8 / Bardo 4, GS 12, e DEF-5:505 si alza a quel livello. Resta vero che a fine assedio hanno speso tutto (D92) | segue la #241 |
| A8 | Ondate nella caverna: `01`:1986-1989 dice 50 / 30 / 20; `01`:2038-2041 dice 30 / 20 / 15 (ARC-08 si contraddice da solo) | DEF-5:726-732: 30 orchi, 20 hobgoblin sergenti, 15 bugbear, Grimjaw + 10 orog | tenere le cifre di DEF-5 e cancellare 1986-1989 | correggere |
| A9 | Round d'arrivo: `11`:63 dice Round 2; `01`:2165 e `16`:353 dicono Round 9-10 | DEF-5:243-249: nella regia breve (stasera) i PG arrivano a fine Round 2; nella regia lunga (Incontro 3B di ARC-08) al Round 8 | una cifra sola per ciascuna regia, citando DEF-5 | correggere |
| A10 | I pregen «svaniscono» e lasciano bonus permanenti ai PG: `01`:474-481, 624-631 | DEF-5:734-736: nella regia breve i pregen sono fra i dieci capi al centro e non parlano; state non registra nessun bonus permanente | togliere i bonus permanenti, oppure portarli in state con una decisione D | correggere: un bonus permanente non registrato è canone fantasma |
| A11 | Sessione 4: «dopo mezza giornata di battaglia sotterranea» si emerge ai bastioni: `01`:2453; Fasi 2-3 di `01`:2262-2270 | DEF-5:476-493: il portale di Dana porta i PG ai bastioni della Porta Ovest; DEF-5:507: ogni 10 minuti di sosta Fauci abbatte una torre (D77) | sostituire la mezza giornata con il portale di DEF-5; il tempo diventa un orologio di torri | correggere |
| A12 | Struttura del finale: il climax è Fauci contro gufi e Orion, con i PG «a terra» che «guardano» (`01`:2568, 2618-2622; `enc`:1059); ARC-08 non ha né Fase 0 né consiglio di guerra dopo l'arrivo | DEF-5:111-115 (D77/D38), ramo del gruppo di oggi (3g 15h): «prima il Cuore, poi Fauci [ai bastioni], poi il consiglio di guerra per le ondate che restano», e quella è la Fase 0 di ARC-08; DEF-5:476-480: il drago viene a cercare i PG | ristrutturare ARC-08 a partire dalla Fase 0 di DEF-5; Fauci è un duello dei PG, con gli alleati come supporto | correggere: è il punto più grosso, ed è domanda Q1 |
| A13 | Il veterano grida «IL RE È TORNATO»: `01`:2175 | DEF-5:308: i nani gridano il nome della fortezza | allineare la battuta a DEF-5 | minore |
| A14 | Tordek atterra fra le porte, in mischia: `11`:116-118 | DEF-5:279-283: altare a 36 m, nessuno in mischia nel round di sorpresa | allineare la posizione a DEF-5 | correggere |
| A15 | Poteri inventati per i PG: `01`:2275-2293 e 2346-2364; `enc`:862-880 («Warlock della Cerebromorfosi», *Eldritch Blast* 5d6 su 8 bersagli, volo a 18 m con un mantello, «Presenza del Re» +4 For, «Lancio Leggendario», Presenza Regale +6 entro 18 m, lupi crudeli evocati con 1d4+2) | coh §2.1 (non inventare poteri); state:94: Artemis ha *Eldritch Blast* **6d6**; state:91-94: le schede vere | sostituire con un rimando alle schede dei PG; tenere solo le scelte tattiche | correggere |
| A16 | Aegis Fang «+3»: `01`:2429; `enc`:942 | art:45-53: allo Stadio 0 è +2 Returning *Dragondoom* più il bane contro Fauci. art:59-65 (D15): dopo il Rituale 4, Scena 12 di DEF-4, è **+4 Holy Returning**, Ego 20, nani entro 18 m **immuni alla paura**, *guarigione* 1/giorno sui nani, e tiene *Dragondoom* | scrivere lo Stadio 1 (se la Scena 12 è giocata) e ricalcolare la caverna: l'immunità alla paura cambia tutte le prove di morale dei nani *(dedotto)* | correggere, poi Q11 |
| A17 | Nel consiglio 1B, con i pregen, Dana guarda «voi, gli eroi leggendari tornati»: `01`:1108. Righe «se presente un Warlock / Druido / Monaco»: `01`:1145-1147 | DEF-5:320 e 334: nessuno sa del viaggio; i PG arrivano solo al Giorno 3 | togliere i PG dalla Sessione 1 | correggere |
| A18 | `00`:23-24: «il tavolo reale è all'ARC-07, Piano della Terra» | state:18-26: il tavolo è nella notte del ≈372 DR, DEF-4 Scena 5 | aggiornare il banner (meglio: rimandare a state §0) | minore |
| A19 | Bonus cumulativi della carica: +15 (`01`:2815-2822) e «+23» (`enc`:1189-1199), costruiti sommando più bonus morali | DEF-5:503 e SRD: bonus dello stesso tipo non si sommano, vale il più alto | ricalcolare per tipo (morale, sacro, competenza, circostanza) | correggere |
| A20 | `Cer`:74: Lythiel è «una dei 12 ranger elfici sui gufi giganti» arrivati alla Sessione 4 | state:245-250 (D13): i 12 ranger sono la compagnia di **Lunapiena**, indipendente, «da non confondere… né con Lythiel Alar-Wen» | Lythiel arriva per conto suo, da ospite, come dice `Cer`:32 | correggere |
| A21 | `Cer`:44, il re ai quattro: «tre lo siete, una no» | state:93-94: Hella è *Dream Dwarf*; il non-nano è Artemis, umano e maschio | «tre lo siete, uno no» | minore |
| A22 | 210 = 118 + 92 + 9: `Cer`:23; `15`:227-231 («NON modificare»); `10`:46 | aritmetica: 118 + 92 + 9 = **219** | domanda al DM: quale delle tre cifre cambia (Q9) | correggere la fonte, poi le copie |
| A23 | «210 asce, una per ogni caduto»: `enc`:1303-1306 | `Cer`:19: **100** asce, simboliche, non una per caduto | allineare `enc` a `Cer` | minore |
| A24 | Ricompense di 50.000 mo, feudo e armi su misura: `01`:2974-2978; `enc`:1338-1342 | `17`:99-140 (D41, D42 `[CANONE — DM 2026-10-07]`): gemme circa 30.000 mo per PG, reliquie del 372 al posto dell'oggetto su misura, forziere da 5.000 / 20.000; `13` §2-§3 | sostituire la lista con un rimando a `17` §2 | correggere: oggi `01` e `enc` danno più di quanto il canone deciso conceda |

## (b) PRESUPPOSTI di esiti non ancora giocati — 10

| # | Cosa presuppone ARC-08 (file:riga) | Cosa dice il canone (fonte:riga) | Correzione minima o domanda | Raccomandazione |
|---|---|---|---|---|
| B1 | Fauci «fuggito gravemente ferito», come esito fisso: `01`:2919, 2993; `enc`:1104-1112, 1281, 1351; `16`:369 | coh:248-250, state:186 e 218-219: ramo D10 non risolto; la fuga è il default, non un fatto | una tabella a tre esiti (fugge, muore, vince e se ne va), con la fuga come default | rendere condizionale |
| B2 | Fauci a 180/312 pf (`01`:2578) o a 220/312 (`enc`:1028), senza carry-over (e le due cifre non coincidono) | B4: dopo il duello con Skullcrusher, ucciso dà 281 pf e Presenza CD 23, ferito grave dà soffio solo in linea a CD 27, fuggito dà +2 iniziativa e fuga sotto 75 pf; ferite segnate +N; cicatrice d'ala. DEF-4:2850-2866, 3092-3093. art:53: bane contro Fauci (+2 / +3d6 / ×4 / scosso CD 22) | i pf partono da 312 meno il B4; aggiungere la riga del bane | aspettare l'esito del duello (si gioca prima di ARC-08) |
| B3 | Le scaglie di Fauci, fuse, fanno le mura in «acciaio draconico»: `01`:2989 | B1: Fauci può fuggire. `17`:215 lo condiziona già («se il drago è morto») | condizionare `01`:2989 come fa `17` | minore |
| B4 | «Re Thorek, miracolosamente guarito dalle preghiere dei chierici»: `01`:2753 | DEF-5:451-459 e 503: il re lo curano i PG (*ristorare* toglie l'esausto); i chierici non hanno più incantesimi (A6) | «guarito da chi lo ha curato», con due varianti: curato / ancora a 8 pf | condizionare |
| B5 | La «vittoria costosa» con il re ucciso: `10`:80-81, 207 | DEF-5:282-283 (D92): in DEF-5 il re non muore, perché il colpo lo prende Dana | tenere il ramo della morte del re solo per il finale di ARC-08, e dirlo | domanda Q5 |
| B6 | 210 caduti e 90 superstiti come numeri chiusi: `10`:46-47; `01`:2902, 2923; `Cer`:15 («locked event»); `17`:24, 152; `enc`:1288 | coh:63-64: le 210 vittime sono canone *preparato*, non giocato. DEF-5:113: nel ramo di oggi le mura tengono ancora e solo una colonna è scesa *(dedotto: i superstiti possono essere più di 90)* | un contatore dal `03` Registro, con il 210/90 come default | condizionare |
| B7 | Il carry-over «se il gruppo NON ha giocato il P5»: `02`:72-73, 119; `10`:167 | state:15-29: il gruppo **lo sta giocando**; B4 si applica | sostituire con «leggi l'esito del duello in state» | aggiornare |
| B8 | La Cerimonia del Giorno 21 e il titolo di Custodi Eterni come esito certo: `Cer`:7, 50; `15`:186 | state:346: «Awarded post-siege», canone preparato | default tenuto, ma legato alla vittoria | lasciare, con una nota |
| B9 | I pregen vivi a Hammerfist nel 1372 (Borin in prima linea, Thorin alla porta, Nala con gli ordini): `17`:54-58, 159-162. Ma `01`:2954 / `enc`:1315 incidono sulle asce «Borin Manodura» e «Dara Passolesto» | la loro sorte dipende dalle Sessioni 1-3 con i pregen, oppure dai default D9 se il flashback salta (Q1); DEF-5:734-736 li tiene vivi fra i capi | `17`: «se vivi»; asce: Q8 | condizionare |
| B10 | `17`:73-75: l'ascia con la brina c'è «solo se nel 372 i PG non l'hanno comprata» `[INFERRED]` | S4:54: il gruppo ha comprato l'ascia d'adamantio +2 e lo scudo con gli spuntoni gelidi, **non** l'ascia +1 del gelo; DEF-4:1409-1415 | si può già togliere l'`[INFERRED]`: l'ascia c'è, citando S4:54. Ma la Scena 10 non è giocata: la guardia che la porta può ancora morire (DEF-4:1413) | aggiornare con una nota |

## (c) DUBBI che solo il DM può sciogliere — 9

| # | Cosa presuppone ARC-08 (file:riga) | Cosa dice il canone (fonte:riga) | Domanda | Raccomandazione |
|---|---|---|---|---|
| C1 | Tre sessioni e mezza di flashback con i pregen *prima* dell'arrivo: `00`:28-39; `10` §5; `15`:117-121; `enc`:1362-1371 | DEF-5:243-249 e 726-736: la regia breve fa arrivare i PG già stasera, e i pregen sono comparse. Giocare il flashback dopo l'arrivo rompe il ritmo *(dedotto)* | Q1 | i bonus D9 restano ai default |
| C2 | ARC-08 non nomina il bane di A7 | art:53 (bane +2 TxC) e B4 §4 («Aegis sente Fauci»: +2 di circostanza e preavviso del soffio). Per l'SRD si sommano, perché i tipi sono diversi; raccontano però lo stesso fatto *(dedotto)* | Q2 | — |
| C3 | — | B4: ferite segnate N≤3; non dice se si sommano tra fonti diverse | Q3 | — |
| C4 | `03`:39: il dado dei caduti del 372 non arriva nel 1372; `17`:83 fa tirare sul Registro per le cure comprate nel 1372 | S4:60: «Quattro tiri sul *Registro delle Perdite* di ARC-08… da fare alla Scena 10», contro DEF-4:1148-1152 e 1405-1407 (dado dei caduti, D64) | Q4 | errore della fonte di canone: si corregge S4, non ARC-08 |
| C5 | ARC-08 dà Dana viva alla carica, alla Cerimonia e al banco (`17`:54, 159, 176) | DEF-5:282-283 (D92): il colpo destinato al re lo prende Dana; non è chiaro se muore | Q5 | — |
| C6 | ARC-08 non accoglie nessuno degli echi di DEF-4 (grep vuoto su Aura della Forgia, torque, Senzienza, Balvar, Zog'tar) | DEF-4:2968-3008 (Aura della Forgia, che dura fino all'alba; DEF-5:99, D17/D91); DEF-4:3010-3034 e 3163 (torque +1 sacro contro la paura, reliquia; DEF-5:322); DEF-4:2096-2108 (pannello di Balvar; Aegis lo riconosce); DEF-4:2251 (Zog'tar vivo dà un generale in più alla Mano Rossa); DEF-4:1436-1443 (i pezzi del capo fabbro riconosciuti nel 1372); DEF-4:3109 (il tono del Rubino è il colore della Corona); art:103/111/127 (Corona +3 o +2, Senzienza); S4:54 (consumabili comprati per circa 48k, assenti dall'audit WBL di `13`) | Q6 | elenco da integrare nella Fase 0 e in `13` |
| C7 | Maestro Tempestas evoca la tempesta in battaglia: `enc`:1017-1021, 1333 | state:107 e 352: messaggero via *Shadow Walk*, agente d'intelligence di Rethmar, «not constantly present». Una battaglia non lo esclude *(dedotto)* | Q7 | — |
| C8 | Nomi sulle asce «Borin Manodura», «Dara Passolesto, occhio delle montagne»: `01`:2954; `enc`:1315 | i pregen si chiamano Borin **Ferropugno** e Dara **Occhiolesto** (`15`:124, 139). Sembrano gli stessi con il cognome sbagliato *(dedotto)* | Q8 | — |
| C9 | Runa dei Custodi: «−4 alle CD diplomatiche» (`Cer`:52) contro «+2 di circostanza a Diplomazia» (`15`:199, `[INFERRED]`, rimanda a `10` §6.2) | nessuna fonte di canone | Q10 | — |

**Note sulle fonti, che non sono difetti di ARC-08**:
- state:376-377 è ancora 🔵 «non ancora contratto» per il debito di Thorik, mentre S4 dice che il Debito della Radice è contratto (E-07g; state:91). Va corretta la fonte (render da `state.yaml`).
- S4:60, vedi C4.

---

## Domande per il DM (una parola ciascuna)

| Q | Domanda | Opzioni | Consigliata, e perché |
|---|---|---|---|
| Q1 | ARC-08 si rifà sulla struttura di DEF-5 (Cuore → Fauci ai bastioni → consiglio di guerra / Fase 0), e il flashback con i pregen come si gioca? | **Salta** / Dopo / Prima | **Salta**: DEF-5 ha già fatto arrivare i PG, e i bonus D9 vanno ai default. Il flashback resta materiale per un gruppo futuro *(dedotto)* |
| Q2 | Il bane di A7 (+2) si somma al +2 di circostanza «Aegis sente Fauci» del B4? | Sì / **No** | **No**: tecnicamente i tipi sono diversi, ma è lo stesso fatto narrativo pagato due volte; il B4 tiene solo il preavviso del soffio |
| Q3 | Le ferite segnate del B4 si sommano fra loro oltre N=3? | Sì / **No** | **No**: il tetto N≤3 resta un tetto |
| Q4 | S4:60 («quattro tiri sul Registro di ARC-08») si corregge a favore di DEF-4 (dado dei caduti nel 372)? | **DEF-4** / Registro | **DEF-4**: lo dicono DEF-4:1148-1152, 1405-1407 e ARC08-03:39 |
| Q5 | Dana, quando prende il colpo destinato al re (D92), sopravvive? | **Viva** / Morta | **Viva** (ferita): ARC-08 e ARC-09 la usano come chierica 12 al banco, alla Cerimonia e nei servizi |
| Q6 | Gli echi di DEF-4 (Aura della Forgia, torque, Senzienza della Corona, Balvar, Zog'tar, pezzi del capo fabbro, consumabili comprati) entrano in ARC-08? | **Integrare** / Ignorare | **Integrare**: senza, il viaggio dei mille anni non ha conseguenze sul 1372 |
| Q7 | Tempestas è presente nella battaglia con la tempesta controllata? | **Presente** / Assente | **Presente**: compatibile con state:107, e la Cerimonia lo vuole già lì al Giorno 21 |
| Q8 | I nomi «Borin Manodura» e «Dara Passolesto» sulle asce sono i pregen caduti? | **Pregen** / Omonimi | **Pregen**, con il cognome corretto e solo se nel flashback, o nel default, muoiono; altrimenti si cambiano |
| Q9 | 118 + 92 + 9 = 219: quale cifra cambia per arrivare a 210? | **118→109** / 92→83 / Totale→219 | **118→109**: i caduti della battaglia sono ancora da giocare (B6), e 92 e 9 sono passato |
| Q10 | La runa dei Custodi Eterni dà +2 di circostanza a Diplomazia o −4 alle CD? | **+2** / −4 | **+2**: è il formato SRD |
| Q11 | All'arrivo nel 1372 Aegis Fang è allo Stadio 1 (+4 Holy, nani immuni alla paura entro 18 m)? | **Sì** / No | **Sì**, se la Scena 12 si gioca come scritta (art:63) |
| Q12 | Il 14° si prende al primo riposo dopo Hammerfist (D90) e l'audit WBL di ARC08-13 si rifà su quello? | **D90** / D9 | **D90**: è la decisione più recente |

---

## Cosa ho letto, e cosa no

- **Letti per intero**:
  - ARC-08: `00`, `01` (3.495 righe), `02`, `03`, `04`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `Cer`, `enc` (1.438 righe);
  - DEF-5 (748 righe);
  - sul ramo: state (500 righe), session-4, session-3 (scritta in anticipo, non giocata).
- **Letti in parte**:
  - `mass_combat_guide_Dm.md`: righe 1-50 e 625-663, il resto solo per titoli e grep. È uno strumento di regole senza fatti di canone;
  - DEF-4 (3.763 righe): solo le sezioni 73-160, 1140-1155, 1395-1445, 1998-2010, 2094-2110, 2244-2256, 2850-2875, 2959-3215;
  - `art` e `coh`: solo le righe citate.
- **Non letti**:
  - `ERRATA-ARC08-35-Verification.md`, `ERRATA-ARC08-DESCRIZIONE-EPICA.md`, `PIANO-REVISIONE-ARC08-…`, `combat_prompts_guide.md`, i quattro `ARC08-9x-DEPRECATO`, la cartella `Mappe/`;
  - le schede di Bestiario (Re Thorek, Dana, Fauci, pregen);
  - DEF-1, DEF-2, DEF-3.
- `fase1.py`: rami non misurati (clone shallow), misure dei box a 0.
