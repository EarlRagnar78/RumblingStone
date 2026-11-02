# Arco 08, giro a freddo del 2026-10-19: le correzioni

Correttore: un agente. Ramo `claude/project-thread-e860p0`. Niente commit, niente push.
I quattro rapporti (DEV 44, PT 31, DM 30, MAP 24: 129 rilievi) si riducono a una sessantina di difetti distinti: molti rilievi descrivono lo stesso difetto visto da un altro lato. Sotto, ogni riga dà il rilievo, l'esito e, per i duplicati, il gruppo in cui è confluito.

Sigle dei file (tutti sotto `08_La Battaglia Di Hammerfist/`):
**A** `ARC08-01-GUIDA-DM.md` · **B** `hammerfist_encounters-…-Guida-agli-Scontri-final.md` · **C** `ARC08-10-ESITI-E-CONTINGENZE.md` · **D** `ARC08-11-PONTE-ARRIVO.md` · **E** `Cerimonia-delle-100-Asce.md` · **F** `Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md` · **G** `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`.
Toccati anche i quattro SVG rigenerati di F (MAPPA 4 e MAPPA 5, temi pergamena e texture). Nulla fuori dalla cartella dell'arco, niente in `_ARCHIVIO/`, `campaign/state.md` intatto, `Bestiario/` intatto.

**Conteggio degli esiti, solo 🔴 e 🟠 (74 rilievi):** CORRETTO 37 (due con una parte RESIDUA: DEV#26 e DM#22) · AL DM 35 (dodici con una parte già CORRETTA) · RESPINTO 1 · RESIDUO 1. Molti AL DM hanno anche una parte CORRETTA: è corretto quello che vale in tutte le versioni (numeri, regole SRD), mentre resta al DM la scelta fra le versioni.

---

## 1 · Tabella

### DEVELOPER

| Rilievo | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| DEV#1 | 🔴 | AL DM (D1) | Il boss in mano ai PNG: dipende dalla versione di Fauci scelta. Raccomando F, dove i PG lo affrontano |
| DEV#2 | 🔴 | AL DM (D1) + CORRETTO | Le versioni restano al DM. Corretto il denominatore dei pf ovunque, in A, B ed F: «/312» → «/337», il valore della scheda (25d12+175). I pf di partenza (180/220/232) restano una scelta, con un rimando a C §4.1 |
| DEV#3 | 🔴 | CORRETTO | La presa di Orion in A, B, F e C ora è una lotta contrapposta (SRD): niente CD 25, niente «lacerazione». Con +24 contro +43 da sola non tiene: lo scrive anche il ramo «ucciso» di C. Il congegno che fa cadere Fauci resta in D1 |
| DEV#4 | 🟠 | CORRETTO | Aegis Fang in A e B: +2 *ritornante*, lanciata −4 come arma impropria, incremento 3 m, massimo 15 m; in fase aerea è fuori portata |
| DEV#5 | 🟠 | AL DM (D6) + CORRETTO | In A, B ed F il meteo ora segue l'SRD: Tempra CD 15 solo per i Piccoli, −4 a distanza, e l'avvertenza che vento violento e pioggia fanno una *tempesta*, dove gli attacchi a distanza con armi sono impossibili. Chi lancia la tempesta, e se gli archi tirano, lo decide il DM |
| DEV#6 | 🟠 | CORRETTO | Fauci in A e G: morso +33 (BAB +25, For +10, taglia −2), attacchi secondari +31. Corretta anche la riga dell'appendice di A (+35 → +33) |
| DEV#7 | 🟠 | CORRETTO | La nota «Verifica» di A e G è riscritta: 25 DV sono un drago *vecchio* per l'SRD, e la scheda è un adulto maturo potenziato. Percezione cieca 18 m al posto di vista cieca; 90 m di presenza terrificante e *corrompere acqua* a volontà segnati come potenziamento sopra l'SRD (63 m, 1/giorno) |
| DEV#8 | 🟠 | AL DM (D6) | Tre Tempestas diversi. Ho segnato `[INFERRED]` il «LI 20» di F; chi fa i danni della tempesta lo decide il DM |
| DEV#9 | 🟠 | CORRETTO | In A e B la caduta del cavaliere è condizionata («se il cavaliere cade»), non più scritta a copione. Corrette le opzioni: niente Deviare Frecce, la *caduta morbida* non è da druido, 15d6 fanno 52 in media contro 95 pf |
| DEV#10 | 🟠 | AL DM (D2) + CORRETTO | Nuovo blocco «📎 Regia, prima di sedersi» in A e B, con le schede che esistono in `Bestiario/mostri/`: orco berserk (`orco-berserk-barbaro2-cr2.md`, GS 2, CA 13, pf 27, grande ascia +9, 1d12+9), hobgoblin (`hobgoblin-regular-warrior3-cr2.md`, GS 2, CA 19, pf 23, +6, 1d8+1), sergente (`hobgoblin-sergente-cr5.md`, GS 5, CA 21, pf 37, +9, 1d8+4). Bugbear e guardie orog non ci sono: vanno al DM |
| DEV#11 | 🟠 | AL DM (D11) | L'EL 17 di uno scontro che è una rotta. L'intestazione rimanda ora all'Appendice C (2.600 PE al gruppo, 650 a testa), con una nota `[INFERRED]` |
| DEV#12 | 🟠 | AL DM (D3) | La rotta in tre tempi ognuno più debole del precedente dipende dal round di Grimjaw |
| DEV#13 | 🟠 | AL DM (D3) + CORRETTO | D allineato alla guida (PG ai round 9-10, controllo al round 11). In F l'Apparizione passa dal round 8 ai round 9-10 e la cura diventa 2d8 `[CANONE — DM 2026-10-18]`, come in A e B. Resta al DM il round di Grimjaw |
| DEV#14 | 🟠 | CORRETTO | «AZIONI INIZIALI» di A e B riscritte su Thorik, Hella, Tordek e Artemis con i numeri dello stato del gruppo: Aura della Forgia +4 morale, Deflagrazione 6d6 `[Private source — Complete Arcane]`, 1d4+1 lupi crudeli, pelle coriacea +5, Pugno stordente CD 16 |
| DEV#15 | 🟠 | CORRETTO | In D tolto il «−2 COS permanente» di Thorik; la riga ora riporta lo stato del gruppo (−4 DES / +2 COS / +4 CAR, la deviazione data a Hella, il Debito della Radice) |
| DEV#16 | 🟠 | CORRETTO | Orion: aggiunta in A, B ed F una nota d'economia d'azione (salto, forma selvatica e presa non stanno in un round solo) |
| DEV#17 | 🟠 | AL DM (D2) | I gufi giganti non hanno CA né pf, e il Bestiario non ha una loro scheda |
| DEV#18 | 🟠 | CORRETTO | Carica in A e B: dei bonus morali vale solo il più alto (SRD), il +4 sacro è `[INFERRED]`, carica +2, altura +1. Totale +7/+11 al posto di +15/+23 |
| DEV#19 | 🟠 | CORRETTO | La carica ora si risolve col sistema di massa di G §4: tre unità di testa con AU +16/+20 e 1d8+4, e una riga «comandare un'unità» in B |
| DEV#20 | 🟠 | AL DM (D11) | Mancano le righe di scala per 3 o 5 PG. Le scrivo solo quando il DM avrà fissato il dosaggio dei PE |
| DEV#21 | 🟠 | AL DM (D4) | Il tiro che uccide Re Thorek non è scritto |
| DEV#22 | 🟠 | CORRETTO | In A, B ed F il conteggio è condizionato: ~500 morti e ~400 in rotta se i PG lasciano fuggire (D11 di C), e Fauci risulta «fuggito o ucciso». I mitragliamenti diventano «attesi» o «fino a» |
| DEV#23 | 🟠 | AL DM (D9) | 118 + 92 + 9 fa 219. In C ed E ho segnato `[INFERRED]` la riga del 210 |
| DEV#24 | 🟠 | CORRETTO | La runa di E dà ora +2 di circostanza a Diplomazia, come C §6.2 (canone del DM del 2026-10-18) |
| DEV#25 | 🟠 | AL DM (D8) | Lythiel. Ho messo un flag `[INFERRED]` in E |
| DEV#26 | 🟠 | CORRETTO / RESIDUO | Agli «ultimi 50 hobgoblin élite» di A e B do una scheda: `hobgoblin-veterans-warrior6-cr5.md`, GS 5, CA 19, pf 43, +10/+5, 1d8+2 `[INFERRED]`. Resta RESIDUO la tattica degli «ultimi fedeli» della 4D, che dipende da D1 |
| DEV#27 | 🟠 | AL DM (D7) | Il blocco «Se lo divinano» per Fauci in fuga: la Corona e lo *scrutare* di Hella cambiano il ramo, e prima va scelta la versione |

### PLAYTESTER

| Rilievo | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| PT#1 | 🔴 | AL DM (D2) + CORRETTO | Come DEV#10: le tre schede trovate sono nella regia di A e B; bugbear e orog vanno al DM |
| PT#2 | 🟠 | CORRETTO | Come DEV#14 |
| PT#3 | 🟠 | AL DM (D3) + CORRETTO | Come DEV#13 |
| PT#4 | 🟠 | AL DM (D4) | Re Thorek, la cura e il veleno: in F ho aggiunto una nota SRD `[INFERRED]` (*guarigione* cura anche il veleno) |
| PT#6 | 🟠 | CORRETTO `[INFERRED]` (D5) | Nuovo blocco «📎 Regia fra il Cuore della Montagna e i bastioni» in A: mezza giornata, niente riposo lungo, i chierici di Dana curano Re Thorek, le unità sono in ARC08-03. Il DM lo conferma |
| PT#7 | 🔴 | AL DM (D1) | Come DEV#1 |
| PT#8 | 🔴 | AL DM (D1) | «E se volano?»: la reazione del drago ai PG in volo con le pozioni è nelle opzioni di D1 |
| PT#9 | 🔴 | AL DM (D1) | Come DEV#2 |
| PT#10 | 🟠 | CORRETTO | Come DEV#3 |
| PT#11 | 🟠 | AL DM (D6) + CORRETTO | Come DEV#5. *Invocare il fulmine* ora fa 3d6, o 3d10 in tempesta |
| PT#12 | 🟠 | CORRETTO + AL DM (D7) | Le regole della caduta sono corrette come in DEV#9. Cosa sa il cavaliere, se lo interrogano, è in D7 |
| PT#13 | 🟠 | CORRETTO | Come DEV#22 |
| PT#14 | 🟠 | CORRETTO | Come DEV#18 |
| PT#15 | 🟠 | CORRETTO | La carica rimanda a G §4 e alle unità di ARC08-03 (come DEV#19) |
| PT#19 | 🔴 | RESPINTO | Il banco esiste. ARC08-17 §3: «Dopo la Cerimonia la fucina riapre per un giorno e mezzo». In A ho aggiunto il rimando, perché il DM lo trovi |
| PT#20 | 🟠 | CORRETTO | Ricompense di A e B: 30.000 mo a PG (ARC08-13 §3, non 50.000), opere perfette solo dopo Rethmar (ARC08-17 §2), un oggetto su misura da ~10.000, il banco in ARC08-17 §3. Corretta anche l'Appendice C |
| PT#25 | 🟠 | AL DM (D8) | Come DEV#25 |
| PT#27 | 🟠 | CORRETTO | Come DEV#15. Anche la riga della Corona in D: Topazio e Smeraldo; il Rubino si è consumato nel salto (D16) |
| PT#28 | 🟠 | AL DM (D9) | Il legame fra i caduti nel gioco e la soglia «meno di 50 superstiti» |

### DM

| Rilievo | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| DM#1 | 🔴 | CORRETTO `[INFERRED]` (D10) | La regia di A dichiara la serata: 3B e Sessione 4; la Cerimonia va alla serata dopo. Il DM lo conferma |
| DM#2 | 🔴 | CORRETTO `[INFERRED]` | Nuovo §5.5 in C, «Se il flashback coi pregen non è stato giocato»: Re Thorek a 8 pf con la riga piena, gli altri bonus a metà, Grimjaw logorato del 20%, le Cantitrici a metà; se il P5 non è stato giocato la scheda di Fauci resta com'è. A, B e D lo richiamano |
| DM#3 | 🔴 | AL DM (D1) | Come DEV#2 |
| DM#4 | 🟠 | AL DM (D3) + CORRETTO | Come DEV#13 |
| DM#5 | 🟠 | CORRETTO | Come DEV#15 |
| DM#6 | 🟠 | CORRETTO | Come DEV#14 |
| DM#8 | 🟠 | AL DM (D1) + CORRETTO | Come DEV#2. Il carry-over resta in C §4.1, e lo richiamo dove compaiono i pf |
| DM#9 | 🟠 | AL DM (D6) | Come DEV#5 e DEV#8 |
| DM#10 | 🟠 | CORRETTO | Come DEV#18 e DEV#19 |
| DM#11 | 🟠 | AL DM (D4) | Come DEV#21 |
| DM#12 | 🟠 | AL DM (D2) + CORRETTO | Come DEV#10 |
| DM#13 | 🟠 | CORRETTO `[INFERRED]` (D5) | Come PT#6 |
| DM#14 | 🟠 | CORRETTO | Il box c'è nella guida, al 3C: «Proprio quando gli orchi sfondano l'ultima barricata…». In D ho aggiunto la battuta di Re Thorek presa dall'Atlante e il round giusto (9-10) |
| DM#15 | 🟠 | CORRETTO | Come PT#20 |
| DM#16 | 🟠 | CORRETTO | Come DEV#24 |
| DM#17 | 🟠 | CORRETTO | Ora i riti sono due e distinti, in A, B, E ed F: il Campo della Memoria al tramonto, con le asce piantate sul campo, e la Cerimonia del Giorno 21 nella Sala, con 100 asce |
| DM#22 | 🟠 | CORRETTO / RESIDUO | La regia di A dà l'elenco di lettura per un'ora e mette C §5.5 dentro. Restano RESIDUO le durate delle scene della Sessione 4: senza un dry-run non si possono stimare |

### COLLAUDATORE-MAPPE

| Rilievo | Gravità | Esito | Cosa ho fatto / perché |
|---|---|---|---|
| MAP#1 | 🔴 | CORRETTO | In F, MAPPA 5, la riga 06 AE-AJ passa da 🏰 a ⬜: la porta di mithral ora dà sulla caverna |
| MAP#2 | 🔴 | CORRETTO | L'altare AF26-AJ30 passa da ⬛ a ⬜, tenendo 🔮 AH28, ✨ AH27, ⚫ AH29 e 🔵. Una nota sull'altare nello stato A |
| MAP#3 | 🟠 | CORRETTO | In A e B gli schemi 3A, «La Trasformazione» e «Mappa 3B: La Svolta» mettono ora il tunnel e la porta a NORD, come F e l'Atlante |
| MAP#4 | 🟠 | AL DM (D3) | Grimjaw ai round 9-10 o 14-15 |
| MAP#5 | 🟠 | RESIDUO | Le posizioni dello stato F (3B) dipendono da D3: le disegno quando il DM avrà scelto |
| MAP#6 | 🟠 | CORRETTO | La riga «Dimensioni» di MAPPA 4 in F dice ora «60 colonne × 68 righe · 3 m/quadretto». In A e B l'etichetta «(300m x 200m)» diventa «(schema; griglia 180 m × 204 m)». La barra da 1,5 m sta nel PNG, fuori da questo giro |
| MAP#7 | 🟠 | AL DM (D1) | Il round del contatto segue la versione scelta |
| MAP#8 | 🟠 | AL DM (D1) | Come DEV#2 |
| MAP#9 | 🟠 | AL DM (D1) | Il cuneo di F (Thorik in punta) fa parte della versione raccomandata |
| MAP#10 | 🟠 | AL DM (D1) | Grimjaw manca dalla griglia di MAPPA 4: va messo dove la versione scelta lo vuole |
| MAP#11 | 🟠 | AL DM (D1) | PG sui bastioni o già nel campo ai round 1-5: dipende dalla versione |

---

## 2 · Decisioni per il DM

**D1 · Quale battaglia con Fauci di Palude?** *(DEV#1, #2 · PT#7, #8, #9 · DM#3, #8, #25 · MAP#7-#13)*
A e B: Fauci fugge al round 5 della fase aerea e lo combattono i PNG. F: si schianta ai round 18-20 e duella coi PG ai round 21-23, con Thorik in punta al cuneo. In ogni versione corretta, la causa dello schianto dev'essere legale: la presa di Orion da sola non lo tiene.
- **F, schianto e duello** → i PG affrontano il boss dell'arco, Thorik regola il conto. Vanno riconciliati i round interni di F e scritta la reazione del drago ai PG in volo.
- **A/B, fuga al round 5** → la fase aerea resta dei PNG; i PG combattono a terra. Fauci torna come minaccia aperta (C D10).
- **Ibrido**: fuga sotto i 50 pf, salvo che i PG lo inseguano in volo (5 pozioni) → la scelta passa al tavolo, ma servono due rami pieni.
- **Raccomandata: F.** È l'unica in cui i PG affrontano il boss. Pf di partenza: 337 meno il carry-over di C §4.1 (232, se il P5 non è stato giocato).

**D2 · Le schede che mancano: bugbear, guardie orog di Grimjaw, gufi giganti** *(DEV#10, #17 · PT#1 · DM#12)*
- **Aggiungerle a `Bestiario/mostri/` dall'SRD** (bugbear GS 2; orog come orco élite; gufo gigante SRD) → una scheda per tipo, citabile da A e B.
- **Sostituirle con le schede esistenti** (orco berserk al posto degli orog, hobgoblin al posto dei bugbear) → zero lavoro, ma si perde la varietà.
- **Raccomandata: aggiungerle dall'SRD.** Sono creature SRD, quindi niente da inventare, e senza CA e pf i gufi non reggono il soffio.

**D3 · Quando arriva Grimjaw nel 3B?** *(DEV#12, #13, #29 · PT#3 · DM#4 · MAP#4, #5)*
Ho già allineato l'arrivo dei PG ai round 9-10, con il controllo al round 11.
- **Round 12, con un corno al round 11** → la rotta e l'arrivo del campione si saldano, e il tavolo ha un segnale.
- **Round 9-10 (F)** → arriva insieme ai PG, e lo scontro si fa duro subito.
- **Round 14-15 (A)** → prima una lunga rotta, poi Grimjaw: è il rischio di calo che segnala DEV#12.
- **Raccomandata: round 12 col corno all'11.**

**D4 · Re Thorek: il tiro che lo uccide e la cura** *(DEV#21, #39 · PT#4, #5 · DM#11)*
- **Guarigione CD 25 a ogni round finché nessuno lo cura per magia; tre fallimenti e muore** (la proposta di DM#11) → il tiro esiste e la «vittoria costosa» ha un innesco. La cura segue l'SRD.
- **La morte solo per scelta narrativa del DM** → niente tiro, ma la vittoria costosa resta arbitraria.
- **Raccomandata: la prima.** Va fissato anche lo stato di Dana: 20 pf e un muro (A), oppure metà delle risorse (F)?

**D5 · Il passaggio dalla caverna ai bastioni** *(PT#6 · DM#13)* — Ho scritto un default `[INFERRED]` in A: mezza giornata, niente riposo lungo, i chierici di Dana curano.
- **Confermare** → Hella non riprepara: la Sessione 4 si gioca con risorse ridotte.
- **Riposo di 8 ore** → i PG ripartono pieni, e gli scontri della Sessione 4 vanno alzati.
- **Raccomandata: confermare il default.**

**D6 · Chi lancia la tempesta, e gli archi tirano?** *(DEV#5, #8 · PT#11 · DM#9)*
- **Orion lancia *controllare il tempo* prima della battaglia; i fulmini sono la Cantata di Tempestas e *invocare il fulmine* di Orion; agli arcieri alleati una deroga dichiarata (l'occhio della tempesta sopra i bastioni)** → c'è una fonte, e gli archi restano in gioco.
- **Vento violento senza pioggia** → solo −4 e Tempra CD 15 per i Piccoli, nessuna deroga.
- **Tempesta piena, SRD** → nessun attacco a distanza con armi, e i ranger sui gufi diventano inutili.
- **Raccomandata: la prima.**

**D7 · Che cosa sa il cavaliere, e se Fauci si può divinare** *(PT#12 · DEV#27)*
- **Scrivere tre cose che il cavaliere sa e un blocco «Se lo divinano»** (Fauci verso le montagne meridionali, lo *scrutare* di Hella) → i PG hanno una pista. Prima va scelta la versione in D1.
- **Il cavaliere muore o tace** → niente pista; Fauci torna quando lo decide il DM.
- **Raccomandata: la prima, dopo D1.**

**D8 · Lythiel** *(DEV#25 · PT#25 · DM#18)*
- **Seguire lo stato del gruppo: cavalca coi gufi, ospite della Foresta Sacra (non della compagnia di Lunapiena), e riconosce Hella in Sessione 4** → coerente con `state.md`. Va aggiunta una battuta in 4A.
- **Rimandare il riconoscimento alla Cerimonia** → lo stato del gruppo va corretto sul ramo.
- **Raccomandata: la prima.** Lo stato del gruppo dice «Direct recognition during Hammerfist Battle Sessione 4».

**D9 · Il 210 e il conto dei caduti** *(DEV#23 · PT#28 · DM#19)*
- **210 = 118 + 92; i 9 di Drellin's Ferry si nominano nel Giuramento ma non si contano** → basta una frase in C ed E.
- **Portare il numero a 219** → si riscrivono il Giuramento e le asce.
- Per i superstiti: legarli al Registro PFU delle unità naniche, così la soglia «meno di 50» si conta in gioco.
- **Raccomandata: 210 = 118 + 92, e superstiti dal Registro PFU.**

**D10 · La serata** *(DM#1)* — Ho scritto un default `[INFERRED]`: 3B e Sessione 4 nella stessa serata, la Cerimonia in quella dopo.
- **Confermare** → la serata è lunga ma chiude la battaglia.
- **Solo il 3B** → la serata è corta, e la Sessione 4 parte fredda.
- **Raccomandata: confermare.**

**D11 · EL e PE del 3B e della 4A, e la scala per 3 o 5 PG** *(DEV#11, #20 · PT#31 · DM#23)*
- **Tenere l'Appendice C (3B: 2.600 PE al gruppo, 650 a testa; Sessione 4: 4.600 e 1.150) e togliere l'EL 17 dichiarato** → i PE di una rotta sono quelli di una rotta. Poi scrivo le righe di scala.
- **Tenere l'EL 17** → 5.100 PE, ma lo scontro va reso davvero da EL 17.
- **Raccomandata: l'Appendice C.**

---

## 3 · 🟡 lasciati

- **DEV**: #28 (i 20 orchi senza movente per restare), #32 (cosa fanno drago e cavaliere contro Artemis a 15 m), #33 (*nube maleodorante* e Ghermire contro i nani), #34 (un solo TS nel 3B), #37 (i randelli Enormi di Gorthak e il suo +21: è una scheda in G, da rivedere col DM), #44 (le stalattiti: un pericolo per una sola classe).
- **DM**: #20 (il movente degli avversari sepolto), #21 (i grassetti di servizio), #27 (i nomi sulle asce ricalcano Borin e Dara: dipende dalla decisione sul flashback), #30 (le etichette 4A e 4B ripetute).
- **PT**: #16 (Hella in due posti: dipende da D1).
- **MAP**: #13 (la picchiata «su Thorik» finisce nella zona ⚡: D1), #14 (le misure di porta e tunnel), #15 (il ⚡ senza testo in AH11), #16 (Re Thorek con il gettone ⚫ dei boss), #17 (lo stesso colore con significati diversi), #18 (i gettoni non tornano coi numeri del testo), #19 (le Cantitrici in 3 celle invece di 5), #20 (il pendio misura 69 m, non 120 m), #23 (le quote della vista laterale).
- **Corretti** fra i 🟡: DEV#29 (in D3), #30, #31, #35, #36, #38, #40, #41, #42, #43 · PT#17, #18, #21, #22, #23, #24, #26, #29, #30 · DM#7, #24, #25, #26, #28, #18 in parte · MAP#12 (solo il denominatore; i valori in D1), #22, #24.
- **Respinti** fra i 🟡: PT#31 e DM#23, perché l'Appendice C c'è («### **APPENDICE C: RIASSUNTO XP E RICOMPENSE**»); DM#29, perché i 3C e 3D esistono nella guida; MAP#21, perché la guida ha «MAPPA 3B: LA SVOLTA».
- **Al DM** fra i 🟡: DEV#39 e PT#5 (D4), DM#19 (D9).
- Fuori perimetro, da segnalare: ARC-07 DEF-5 e `ARC07-MAPPE-DEFINITIVO` hanno un'altra mappa del Cuore della Montagna (33×27, 3 m), che va confrontata con MAPPA 5.

---

## 4 · Esiti dei comandi

| Comando | Prima | Dopo |
|---|---|---|
| `collaudo_mappe.py` su F | 5 mappe · 8 errori · 15 avvisi (MAPPA 5: 🔮 AH28 chiude l'unico varco, 2 zone separate, 13 unità in AH01 irraggiungibili) | 5 mappe · 7 errori · 13 avvisi. MAPPA 5 a distanza 0, solo le euristiche M1/M2/M4. I 7 errori restanti sono porte «nel muro» sul bordo di H3-1, 3Y e 3Z, mappe che questo giro non tocca |
| `validate_maps.py` | ✓ 53 SVG allineati | ❌ 4 errori dopo la modifica (SVG di MAPPA 4 e 5 non allineati). Rigenerati con `render_map_svg.py --map 4/5`, temi pergamena e texture: ✓ 53 SVG allineati |
| `conformita_statblocchi.py --master A G` | — | 2 file, 0 conti che non tornano |
| `validate_modules.py` | — | ✓ 5 master conformi, 0 errori (un avviso preesistente su ARC07-DEF-2) |
| `misura_craft.py --box` | non accetta un file come argomento | girato sul repo. ARC-08: 86 box, **0 oltre le 12 righe**, 7 con parentesi, 40 con più di un nome proprio, 16 con più di 4 frasi, 15 oltre i 500 caratteri. Non ho tagliato i box: il mandato chiedeva di toccare la prosa solo dove serviva |
| `validate_docs.py --sorgenti` | — | ✓ 1077 documenti, nessun percorso inesistente |

Nessun comando rosso alla fine.

---

## Secondo giro (dopo `VERIFICA.md`)

Ho letto la verifica per intera e ho ripreso i 15 PARZIALI e i 12 NUOVI, con gli stessi vincoli del primo giro. Nulla fuori da `08_La Battaglia Di Hammerfist/`, niente in `_ARCHIVIO/`, `Bestiario/` o `state.md`, nessun commit. Rispetto al primo giro tocco un file in più, l'**Atlante** (`Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`).

### I parziali

| Rilievo | Esito | Cosa ho fatto |
|---|---|---|
| DEV#9 · PT#12 | CORRETTO | In A e B c'è ora una CD sola: lo schema dice «CHI LO AFFERRA: RIFLESSI CD 20», e l'opzione di Thorik ripete la CD 20 `[INFERRED]` (l'SRD non ha una regola per afferrare chi cade). L'interrogatorio del cavaliere resta in D7 |
| DEV#13 | CORRETTO | In A il rimando di MAPPA 5 dice «apparizione round 9-10». Nell'Atlante «Round 8» diventa «Round 9-10» in quattro punti, e l'«EVENTO CLIMAX» è al round 9-10. Il round di Grimjaw resta in D3 |
| DEV#16 | CORRETTO | La nota sull'economia d'azione ora sta anche in B (blocco di Orion) e in F (riga di Orion), con la stessa lettura di A: Orion arriva già orso solo se ha cambiato forma il round prima. Allineato anche l'Atlante |
| DEV#18 · PT#14 · DM#10 · NUOVO 12 | CORRETTO | In F, MAPPA 4X: via i «+2 danni» della carica (al loro posto carica +2 al tiro e altura +1; dei morali vale il più alto; rimando al totale +7/+11 della guida). Via «cumulativo» dal discorso del Re, e la riga «B — Urto» dice «carica +2 al tiro (SRD)» |
| DEV#26 | CORRETTO / RESIDUO | Il rimando ora porta a un'unità che esiste: «HOBGOBLIN GUERRIERI (Warrior 3)» di `ARC08-02` §5 `[INFERRED]`, perché un'unità d'élite di hobgoblin lì non c'è. Resta RESIDUO la tattica degli «ultimi fedeli», che dipende da D1 |
| PT#13 | CORRETTO | In B l'intestazione dice ora «RISULTATI ATTESI DELLE STRAFING *(sono medie: gli esiti si tirano, non sono un copione)*», e copre anche il round 8 |
| PT#15 | AL DM (D5) | Il Registro `ARC08-03` è un foglio vuoto, e l'elenco delle unità nemiche all'inizio della Sessione 4 non si ricava da nessun file: va in D5 |
| PT#20 | CORRETTO `[INFERRED]` | In A e B i seguaci hanno ora una riga: quanti e con che statistiche lo decide il DM (*Comando*, DMG, non SRD). Il feudo di B rimanda ad `ARC08-17` §2. In C l'armeria «a costo nullo» ha un tetto: oggetti perfetti e consumabili già in magazzino, niente magia su misura (`ARC08-17` §2-§3) |
| DM#6 | CORRETTO | Il castigo *Dragondoom* è nel 4A di A e B: 3/giorno, +2d6 contro Fauci, che è Enorme. La fonte è lo stato del ramo («3/day smite vs Large+ dragons, +1d6 per size above Medium», D14) [Private source — Magic Item Compendium]. La «Presenza Regale +6» è tolta dagli «Effetti dell'Apparizione» (NUOVO 3) |
| DM#22 | RESIDUO | Non ho misurato se la lista si legge in un'ora: servono il cronometro di un lettore a freddo e un dry-run, che con un correttore da solo non si fanno |
| MAP#3 | CORRETTO | Il quarto schema di A, «MAPPA 5: IL CUORE DELLA MONTAGNA (SESSIONE 3)», ha ora porta e tunnel in testa, sotto «NORD ↑», come F e l'Atlante. B non ha questo schema |
| MAP#6 · NUOVO 2 | CORRETTO | Il renderer legge la scala da una riga **dentro il blocco della griglia** che contenga «N colonne × M righe · X m» (`scripts/render_map_svg.py`, `parse_block`, regex `righe\s*·\s*([\d.,]+)\s*m`). La riga «Dimensioni» di F sta fuori dal blocco e non conta. Ho aggiunto nel blocco di MAPPA 4 la riga «DIMENSIONI: 60 colonne × 68 righe · 3 m/quadretto» e rigenerato i due SVG: ora dicono «scala 3 m/quadretto» e «15 m (5 quadretti)». Il renderer non l'ho toccato |

### I nuovi

| # | Esito | Cosa ho fatto |
|---|---|---|
| 1 🟠 | CORRETTO | Ho allineato l'Atlante. L'Apparizione è ai round 9-10, con la cura di 2d8 dal canone e senza il «+6 morale»; i nemici tirano Volontà CD 20 o sono spaventati per 10 round, come negli «Effetti dell'Apparizione» della guida. Fauci è a 232/337, col rimando a C §4.1. La presa di Orion è una lotta contrapposta +24 contro +43, e il peso da solo non forza la discesa. La Deflagrazione fa 6d6 a 18 m [Private source — Complete Arcane]. La tempesta non ha più il *controllare tempo* di Tempestas: ora c'è il meteo SRD e chi la lancia è una decisione aperta (D6). Il *punire il male* di Thorik è diventato il castigo *Dragondoom* |
| 2 🟠 | CORRETTO | Vedi MAP#6 |
| 3 🟡 | CORRETTO | Il punto 1 degli «Effetti dell'Apparizione» ora si chiama «LA LUCE DELLA SFERA»: 2d8 dal canone, l'Aura della Forgia +4 se Thorik la usa, e la Presenza Regale +6 dichiarata inesistente |
| 4 🟡 | CORRETTO | Il 4A di B ha la stessa riga di A: EL 20 dichiarato `[INFERRED]` e i PE dell'Appendice C, 4.600 al gruppo e 1.150 a testa |
| 5 🟡 | CORRETTO | In A e B: **AU +17** (+21 con la benedizione sacra). Il conto è scritto: AU +9, più il morale dell'unità, che in G §4 è un valore da −5 a +5 (Iniziale +2, Guardia del Re +2, discorso +4: si sommano sulla scala, con il tetto a +5), più carica +2 e altura +1 |
| 6 🟡 | CORRETTO | Nel beat d'ingresso di D, Thorik ha la «Corona con Topazio e Smeraldo; il Rubino si è consumato nel salto» |
| 7 🟡 | CORRETTO | In A, corpo e Appendice C: niente più oggetto su misura dei fabbri. Al suo posto le reliquie del 372 il Giorno 21 (`ARC08-17` §2, strada B, `[CANONE — DM 2026-10-07, D41]`) |
| 8 🟡 | AL DM (D12) | Il box dell'Atto 2 non l'ho rimesso com'era: vedi la carta qui sotto |
| 9 🟡 | CORRETTO | Ho tolto dal default D5 la causa inventata: niente più «ha ceduto alla luce della Sfera» né «risalgono dalle gallerie». Il testo dice ora che il ritorno ai bastioni non è scritto, e che per la H3-1 il tunnel nord porta lontano: decisione aperta del DM (D5) |
| 10 🟡 | CORRETTO | Ho tolto i due `[INFERRED]` e messo al loro posto il canone. **Dana**: in F, la decisione del DM del 2026-10-18 citata da A («Vale per Dana riposata, cioè il mattino della battaglia»). **Lythiel**: in E, lo stato del ramo («Direct recognition during Hammerfist Battle Sessione 4; canonized 2026-05-04»), e lei viene come inviata del Sacred Forest, non come una dei ranger di Lunapiena (D13). Ho corretto anche le righe di A e G che dicevano «compare solo alla Cerimonia» |
| 11 🟡 | CORRETTO | Lo schema del contrattacco, in A e B, dice ora «[ARTEMIS] DEFLAGRAZIONE 6d6 / SUI FUGGITIVI» |
| 12 🟡 | CORRETTO | Vedi DEV#18 |

Correzione a una riga di D2, trovata in questo giro: le **guardie orog** esistono come unità di massa in G §5 («OROG GUARDIE NERE»: PFU 13, DU 19, AU +12, 1d12+7). La regia di A e B ora le cita; uno contro uno restano senza scheda. I bugbear non ci sono né nel Bestiario né in G.

### Decisione nuova per il DM

**D12 · Il box dell'Atto 2 della Cerimonia: due figure o tre?** *(NUOVO 8)*
Nel primo giro ho riscritto il box: le «tre figure straniere» dal «arrivo coordinato — non casuale» sono diventate «due figure venute da fuori, non venute insieme». La riscrittura segue le note per il DM dello stesso file («I due arrivi (Tempestas, Lythiel) sono discreti … non per coordinamento»), ma tocca un box di prosa di un file che la cronologia chiama canonico.
- **Tenere due figure non coordinate** → box e note dicono la stessa cosa; si perde il presagio del «coordinato».
- **Tornare alle tre coordinate** → il box resta quello originale, ma vanno trovati il terzo ospite e il motivo del coordinamento, e riscritte le note.
- **Raccomandata: tenere le due figure.** È l'unica lettura in cui il box e le note per il DM non si smentiscono.

Si aggiunge a **D5**: l'elenco delle unità nemiche ancora in campo all'inizio della Sessione 4 (PT#15). Il Registro `ARC08-03` è vuoto, e senza la scelta del DM su come si è chiusa la Sessione 3 l'elenco non si ricava.

### I comandi, rifatti

| Comando | Esito |
|---|---|
| `collaudo_mappe.py` su F | 5 mappe · 7 errori · 13 avvisi, come prima: la riga DIMENSIONI nel blocco non cambia nulla. I 7 errori restano porte «nel muro» di H3-1, 3Y e 3Z |
| `validate_maps.py` | ✓ 53 SVG allineati, in tutti e due i temi, dopo il nuovo render di MAPPA 4 |
| `conformita_statblocchi.py --master` A, B, G | 3 file, 0 conti che non tornano |
| `validate_modules.py` | ✓ 5 master, 0 errori |
| `misura_craft.py --box` (sul repo) | ARC-08: 86 box, 0 oltre le 12 righe (gli stessi numeri del primo giro) |
| `validate_docs.py --sorgenti` | ✓ 1077 documenti |

Nessun comando rosso.
