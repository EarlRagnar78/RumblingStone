Verifica: CHIUSO 7 · PARZIALE 3 · APERTO 0 · IN ATTESA DM 9 · NUOVI 🔴 0 🟠 1 🟡 4

# ARC07-DEF-3 · giro 2 · verifica delle correzioni

Master verificato: `07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md`.
Ho confrontato il master con `MODULO.md` della cartella: le differenze sono solo
quelle che `FIX.md` dichiara. Ho controllato i fatti con i fogli veri in
`homebrew/sessione-resurrezione-mille-anni/`, con `ARC07-HANDOUTS.md`, con
`DEF-2` (§0-bis e §7) e con `campaign/state.md`.

Misure: `misura_craft --box` dà per DEF-3 20 box, 0 oltre le 12 righe, 0 con
parentesi, 0 con più di un nome; 7 box oltre le quattro frasi, come prima.
`validate_modules` è verde (5 master conformi, 0 errori). Le righe da leggere
aggiunte (la variante dell'apertura dello Step 5 e quella del box della
Custode) stanno fuori dai box, sono sotto le 40 parole, non hanno nomi nuovi né
date. Nessuna data ISO nuova nel testo stampato.

| Rilievo | Gravità | Giudizio | Prova (citazione dal master corretto, fra «») |
|---|---|---|---|
| DEV#1 · il dono che «attecchisce a metà» non ha regola; chi fallisce aveva rifiutato | 🟠 | IN ATTESA DM | FIX D1. Il testo è invariato: «Hella intera, un dono **attecchisce a metà**» |
| DEV#2 · un PG lascia il suo punto per tenere il Sud: il buco nuovo conta? | 🟠 | IN ATTESA DM | FIX D2. Invariato: «qualcuno occupa il punto vuoto del cerchio, un PG o Therysol […] se lo tiene un PG, tirano lui e gli altri due» |
| DEV#3 · manca la giocatrice di Hella | 🟠 | IN ATTESA DM | FIX D3. Invariato: «Se nemmeno lei risponde, la Custode prende il silenzio per un rifiuto: vale B.» |
| DEV#4 · con quali risorse torna Hella | 🟠 | IN ATTESA DM | FIX D4. §8-bis invariato: «prega, prepara gli incantesimi. Prova *Produce Flame* […] Evoca un orso» |
| DEV#5 · «per una battaglia», «1/battaglia», rinnovo, Pelle di Pietra | 🟠 | IN ATTESA DM | FIX D5 per le durate. Corretti i nomi: «falla valere prima degli scontri di `DEF-4`»; il rinnovo ora c'è e combacia con `DEF-2` §7: «pregando dieci minuti, una volta ogni 24 ore vissute». Resta «mitiga la sua vulnerabilità per una battaglia» e «(1/battaglia)» |
| PT#1 · che cosa sente Durik sull'Altare | 🟠 | PARZIALE | «il DM le dice il vero: dentro la pietra qualcosa batte, sessanta al minuto, e non si sposta. Non le dice che cosa sia. È quello che dà anche la porta di SAG». La risposta c'è, ma non è vero che è la stessa cosa della porta di SAG: quella dà solo «il ritmo è **sessanta al minuto** […] Non dice di chi», senza dire dove. Durik localizza il battito dentro l'Altare, che è quasi tutto il ❌ «che il fondo basso **è il Cuore che batte dentro l'Altare**»: il §3 rischia di diventare la conferma che il ❌ vuole evitare. Vedi N3 |
| PT#2 · Sud occupato prima dello Step 5: testi falsi, cosa cambia, dove compare la Custode | 🟠 | CHIUSO | «Se il Sud è già tenuto: *Dietro chi tiene il Sud l'aria si fa fredda, e qualcosa guarda da lì.*» · «*Alle spalle di chi tiene il Sud, dove un attimo fa c'era solo aria, adesso c'è qualcuno.*» · «Se il richiamo riesce, non cambia niente. Allo Step 5 tirano sempre i tre officianti». Regge; una frase nuova contraddice una riga vicina, vedi N2. Il caso del PG che lascia il suo punto resta in D2 |
| PT#4 · Durik sdraiato al Sud vale? | 🟠 | IN ATTESA DM | FIX D2. Invariato: «Non sa niente che Durik non sappia, e non entra nel cerchio del rito» |
| PT#5 · prendere 10 o 20 sulle prove del rito | 🟠 | IN ATTESA DM | FIX D6. Nessuna riga nuova sul 10 e sul 20 |
| PT#7 · il DM non sa che cosa dicono gli echi privati | 🟠 | CHIUSO | «**Che cosa dicono i fogli, per il DM.**» con una riga per foglio. Controllate sui fogli 03, 04, 05, 06: «due mani piccole e fredde reggevano il Peso con lui», «un uomo che cataloga il suo zaino; […] una cosa messa da Artemis», «l'affresco del Tempo è una porta socchiusa che qualcuno ha già usato». Combaciano |
| PT#11 · un PG si offre: «lo porto io» | 🟠 | PARZIALE | «Se un PG si offre («lo porto io»), la Custode non lo guarda: il debito è della radice, e la radice è di Hella.» La risposta al momento della Custode c'è e regge con la scheda («Non guarda mai chi parla, guarda Hella»). Ma la frase chiude con «Al §8 lei ricorda chi si è offerto», e il §8 non ha nessuna riga per questo caso: ha solo «se hanno offerto Durik: *«Avete dato lui…»*». Il DM arriva al §8 e la battuta promessa non c'è |
| PT#16 · non attraversano e corrono a Hammerfist | 🟠 | IN ATTESA DM | FIX D7. Le tre scelte della soglia sono invariate |
| DM#1 · la vista non mostra gli echi da dare prima né il volume dei giocatori | 🟠 | PARZIALE | Nel master c'è: «Il volume dei giocatori *Il Cuore e la Porta*, con i fogli della tabella qui sotto: **gli echi privati si danno prima di cominciare**», e il PDF Benedizioni è elencato. Ma ho rigenerato la vista con `vista_di_chi_scorre.py`: il riquadro non compare, e fra i 15 grassetti mostrati non c'è quello degli echi. Il DM che sfoglia, cioè quello del rilievo, si siede ancora senza i fogli della prima consegna |
| DM#4 · 92 minuti di lettura, con un'ora ci si ferma prima del §9 | 🟠 | CHIUSO | «**Se hai un'ora per prepararti**, leggi il §0, il §0-bis, la tabella dello Step 5 in fondo al §5 e il §9». La tabella è davvero in fondo al §5 («Lo Step 5 in una tabella»), subito prima del §6. La vista ora stima 95 minuti |
| DM#5 · §1 «nessuna coscienza» contro la frase dalla soglia; come si sente lo spirito | 🟠 | CHIUSO | §1: «tranne la soglia del §6: lì, per una frase sola, la giocatrice lascia Durik e parla da Hella.» §6: «La frase si sente nella Sala con la voce di Hella, bassa, come se venisse dal Cuore sul suo petto; nessuno la vede.» La contraddizione è sciolta e il Cuore allo Step 5 è ancora sul petto |
| DM#6 · Durik al Sud occupa il Sud? | 🟠 | IN ATTESA DM | FIX D2, come PT#4 |
| DM#9 · l'orologio di Hammerfist è fuori dal file | 🟠 | CHIUSO | «L'orologio conta quanto manca alla breccia di Hammerfist, e i PG lo leggono sull'affresco A7, che cambia a ogni riposo. Sotto i **2 giorni** la breccia è aperta e l'ARC-08 parte in Fase 0 dura». Combacia con `DEF-2` §0-bis («**sotto 2g** | **breccia aperta** […] ARC-08 in Fase 0 dura») |
| DM#10 · il DM non sa che cosa dicono preghiera, carte, Cronache | 🟠 | CHIUSO | «le Cronache | Thorgrim Barbadiferro racconta i Quattro Eroi che salvarono Hammerfist dal drago nero e poi svanirono» combacia con `ARC07-HANDOUTS.md`; le carte rimandano al §5, che ha la tabella. La riga della preghiera ha un errore di conto, vedi N4 |
| DM#11 · *Eldritch Blast* 7d6 per un warlock di 13° | 🟠 | CHIUSO | Respinto con fondamento. Master: «***Eldritch Blast*** da **7d6** a **6d6**, **per sempre**». `state.md` §1, Artemis: «**Eldritch Blast 7d6**», e lo stesso numero torna in §7 [I TRE DONI] («7d6 → 6d6»). Il numero che il DM pronuncia è quello del canone. Il master non dice da dove venga il settimo dado: è un 🟡, non un errore |

## NUOVI

| # | Gravità | Dove | Cosa | Prova |
|---|---|---|---|---|
| N1 | 🟠 | §9, riga del sonno | La correzione di DEV#10/PT#10 ha esteso la tariffa delle otto ore al sonno **prima del rito**: «**Vogliono dormire, prima del rito o prima della soglia** \| Si dorme […] Otto ore di sonno: l'orologio di Hammerfist scende di otto ore». Prima del rito vale senza dubbio `DEF-2`, che possiede l'orologio: «Ogni riposo extra **nella Sala** = **−4 h** (tariffa divina)». Prima la contraddizione riguardava solo il sonno dopo il rito; adesso tocca anche quello in cui `DEF-2` è esplicito. È la questione di D11, ma la correzione l'ha allargata: se il DM sceglie «Vale DEF-2», questa riga va riscritta per intero, non in due parole | «prima del rito o prima della soglia» |
| N2 | 🟡 | §9, «Quattro regole» | La frase nuova «chi tiene il Sud tira solo nel ritiro» dice che chi tiene il Sud tira nel ritiro. Due righe sotto, nella riga «0 su 3», il master dice il contrario per Therysol: «Se il Sud lo tiene Therysol, tirano i tre PG agli altri punti». Va bene solo per un PG al Sud. Basta «chi tiene il Sud non tira allo Step 5» | «Allo Step 5 tirano sempre i tre officianti; chi tiene il Sud tira solo nel ritiro.» |
| N3 | 🟡 | §2, percezione di Durik | La frase dice che Durik ottiene «quello che dà anche la porta di SAG», ma la porta dà solo il ritmo; Durik ottiene anche il luogo, «dentro la pietra». Detto così, il §3 perde metà della rivelazione. Più sicuro: «sotto i piedi qualcosa batte, sessanta al minuto, e non si sposta», cioè il ritmo e la fermezza, non la pietra | «dentro la pietra qualcosa batte, sessanta al minuto» |
| N4 | 🟡 | §0, «Che cosa dicono i fogli» | La riga della preghiera dice «tre strofe in italiano; la seconda chiude su *«Quello che manca…»*». Nel foglio 10 le strofe in italiano sono quattro: due prima, «Abbiamo portato le pietre che volevi…» come terza, che chiude su quel verso, e poi «l'ultima strofa», «Hella, figlia della pietra che sogna». Il verso dei Doni chiude la terza | «il nanico e tre strofe in italiano; la seconda chiude su» |
| N5 | 🟡 | §0, tabella delle consegne | La riga nuova dice che la giocatrice «legge ad alta voce la prima metà, «Mentre gli altri dormono»». Nel foglio 06 quella metà finisce con la riga privata «**Solo per te.** La forma che aspetta è **Durik**. La voce è quella di **Tordek**». Il master non dice di saltarla, e letta ad alta voce brucia il nome di Tordek, che è anche il punto ancora aperto di D12 (il master dice ancora «ha già sentito Thorik dire il suo nome nel sonno») | «che legge ad alta voce la prima metà, «Mentre gli altri dormono»» |

Non ho trovato regole 3.5 sbagliate nelle correzioni. I TS di Hella tornano con
le tabelle SRD: Tempra +2 da ranger e +8 da druido, Riflessi +2 e +4, Volontà
+0 e +8, poi COS +4, DES +0, SAG +5 e mantello +2, cioè +16/+8/+15. Il
Treant da Grande con COS 21 contro i 17 dell'SRD è dichiarato. *Augurio* che
risponde «bene» è conforme all'SRD.
