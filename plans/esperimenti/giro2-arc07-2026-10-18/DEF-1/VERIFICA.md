Verifica: CHIUSO 11 · PARZIALE 1 · APERTO 0 · IN ATTESA DM 9 · NUOVI 🔴 0 🟠 1 🟡 2

# ARC07-DEF-1, secondo giro: verifica delle correzioni

Ho controllato sul master corretto (`07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md`) tutti i 21 rilievi 🔴 e 🟠 dei tre rapporti: 8 del developer, 6 del playtester, 7 del DM. Il confronto con `MODULO.md` (diff) mostra 118 righe cambiate, nessuna dentro un box.

Le misure sul master corretto:

- `misura_craft --box`, riga DEF-1: 43 box, 0 sopra le 12 righe, 0 parentesi, 0 con più di un nome proprio nuovo. I 3 box con più di 4 frasi sono un indicatore, non una soglia, e c'erano già prima.
- `validate_modules`: 5 master conformi, 0 errori.
- Date ISO nel testo: 106 prima e 106 dopo. Nomi di file `.md`: 24 prima e 24 dopo. La correzione non ne ha aggiunti. Le battute di dialogo non sono state toccate.
- `vista_di_chi_scorre` sul master corretto: il paragrafo «LA SERATA» adesso dice cosa vuole Terros, chi è Varis, che serve la scheda dei Bracieri e da dove parte l'orologio.

| Rilievo | Gravità | Giudizio | Prova (citazione dal master corretto) |
|---|---|---|---|
| DEV#1 · PT#1 · DM#4 · gli Xorn emergono, mordono e si rituffano nello stesso turno | 🔴 | CHIUSO | «Emergere è movimento e il morso è l'azione standard, quindi lo Xorn che emerge e morde finisce il turno in superficie: per tornare sotto nello stesso turno servirebbe *Attacco Rapido*, che nessuno dei tre ha.» Anche il round 1 regge con l'SRD: «è un round di sorpresa, in cui emergere è la loro sola azione». La legenda della T-2: «Chi emerge e morde resta in superficie fino al suo turno». L'Atlante resta sbagliato: vedi il NUOVO 1 |
| DEV#2 · il tipo di Aegis Fang | 🟠 | CHIUSO | La parola «lancia» non compare più. «l'ascia Returning lanciata come gancio» · «ASCIA PIANTATA e peso addosso» · «l'ascia di Thorik, che è tagliente, no». «la lama morde il bordo» regge, perché anche l'ascia ha una lama. Resta un refuso: vedi il NUOVO 2 |
| DEV#7 · un cristallo rotto vale −1 successo o un fallimento | 🟠 | CHIUSO | Zona 3: «1d6 perforante e **un fallimento** allo skill challenge, come al §6». §6: «Se qualcuno stacca o rompe un cristallo vivo, conta un fallimento» |
| DEV#9 · la fisica del salto verso il Tempio | 🟠 | IN ATTESA DM (D1) | È cambiata una parola sola: «chi scivola finisce nell'oceano di roccia». Due righe sotto resta «Attorno al Tempio la gravità è zero, quindi non si cade: si deriva piano verso l'oceano», e il «Saltare CD 25, Take 10 = 26» non dice ancora quanti metri copre né se comprende gravità e Benedizione |
| DEV#12 · la tattica di Terros non funziona con questo gruppo | 🟠 | CHIUSO | «R2: Earth Glide nell'Altare: un'azione di movimento per entrarci, e per un turno è dentro la pietra […] Al turno dopo riemerge (movimento) accanto al PG a terra più fragile […] e lo colpisce con UNO schianto. Ogni riemersione dall'Altare è il momento delle azioni preparate e di «Radice a Terra».» La divergenza sul metallo è dichiarata: «Diverge dall'SRD, dove l'Earth Glide non attraversa il metallo» |
| DEV#13 · DM#5 · quanto del pugno di Tordek diventa sonico | 🟠 | IN ATTESA DM (D2) | Il testo non è cambiato: «i colpi di Tordek sono sonici nel round in cui il gruppo canta la Frequenza». La riga DPR resta «~11 dopo RD 10» |
| DEV#16 · Terros senza la riga di scala per quattro o cinque PG | 🟠 | CHIUSO | «**Quattro o cinque PG** (gruppo nuovo) \| con quattro PG, il profilo a **34 DV** della prima riga; con cinque, i 34 DV e i **due Elementali della Terra Grandi** al round 3, col loro segno.» Usa solo varianti che c'erano già. Le CD del profilo a 34 DV restano `[INFERRED]` (D10) |
| DEV#17 · PT#17 · il duello formale non ha regole | 🟠 | IN ATTESA DM (D3) | Il testo non è cambiato: «Può concedere un **duello formale** (campione singolo, niente aiuti: onore nanico — EL folle, sconsigliato ma leggendario)» · «richiede comunque il guardiano caduto o il duello onorato» |
| PT#2 · il pilastro crolla, ma dove e su chi | 🟠 | IN ATTESA DM (D4) | Il testo non è cambiato: «il pilastro crolla sugli Xorn (**10d6**, Riflessi **CD 22** dimezza)». L'area non c'è ancora |
| PT#10 · la scala cantata | 🟠 | IN ATTESA DM (D5) | La parte di chiarimento c'è: «Le quattro fanno la scala intera, che con la sola Frequenza arriva a metà strada e col Diapason al portale. Canta un PG alla volta, con un'azione standard, come nel §8.» Sui tentativi illimitati, che restano gratis contro il «Mai gratis» dello yes-and, decide il DM |
| PT#23 · DM#8 · Thorik rifiuta il Peso e nessuno paga | 🟠 | IN ATTESA DM (D6) | La Fase 1 non è cambiata e non scrive cosa succede se nessuno paga |
| PT#24 · per il quarto PG non c'è un ruolo, e la giocatrice di Hella non sceglie mai | 🟠 | CHIUSO | Ci sono le righe per il quarto PG. Skill challenge: «Con quattro o cinque PG la soglia resta 6 successi prima di 3 fallimenti». Salto: «Con un quarto o un quinto PG, gli altri sono legati al cavo e salgono la corda come Thorik». Rito: «Ogni round aiuta Tordek o Artemis con un'azione standard (Aiutare, SRD: CD 10, +2 alla loro prova)». Terros ha la riga di scala. La parte su Hella è respinta con una ragione valida: il §1 la dichiara una scelta di regia («Hella **non ha scene "sopra"**: highlight **percettivo**»), quindi il DM sa che è voluta |
| DM#1 · la vista non dice cosa vuole Terros né chi è Varis | 🟠 | CHIUSO | Il paragrafo che la vista mostra: «Terros l'Antico, che non odia nessuno ed esegue un voto: la Forza non si dona, si dimostra. […] una gemma di **Varis**, un mercante di Rethmar, tenta Artemis con un affare.» Rethmar coincide con la scheda di Varis nel Bestiario |
| DM#2 · la vista non mostra l'orologio né le schede esterne | 🟠 | CHIUSO | «Al tavolo servono anche la scheda dei Bracieri di Tordek e l'orologio di Hammerfist, che parte da **3g 20h**.» Il PDF delle Benedizioni non è nella vista, ma i suoi dati stanno nella Scena 1 |
| DM#6 · un'ora non basta per la via breve | 🟠 | PARZIALE | «Della Scena 7 leggi la Sentinella fino alla regia del duello; della Scena 8 i box della soglia, lo statblocco, le Tattiche e le Contingenze; della Scena 9 la Fase 1 e il giro del round.» Il taglio c'è, ma la mia stima per parole fa ancora circa 10.000-11.000 parole: §0 e §0-bis 2.271, Scena 7 fino alla regia ~1.200, soglia ~940, statblocco, Tattiche e Contingenze ~3.500, Fase 1 ~1.390, più i box delle Scene 1-6. È ancora un'ora piena di sola lettura, senza appunti. «Il giro del round» della Scena 9 non corrisponde a nessun titolo: il titolo vero è «FASE 2 — LA REGIA DEI TRE ROUND» |
| DM#7 · la scheda dei Bracieri sta fuori dal file | 🟠 | CHIUSO | Il §7b ha la tabella dei poteri Fuoco: «Pugni di Magma \| 3 al giorno, azione veloce» … «Martello di Fuoco e Pietra \| 1 a round, azione gratuita». L'ho confrontata con il riepilogo di `05_Bracieri_Gemelli_Scheda_PG_Completa.md` (righe 240-248): usi, azioni, CD 18 e i 4d6 coincidono |

## Controlli sui numeri introdotti dalla correzione

Tutti questi numeri reggono con l'SRD:

- **Fauci di Diamante.** Morso +29 (BAB 21, FOR +8, taglia −1, Arma Focalizzata +1). Spaccare +37 (+4 di Spaccare Migliorato, +4 di taglia).
- **Blast contro gli Xorn.** ~25, cioè 7d6 = 24,5.
- **Sentinella.** BAB/Lotta +13/+25: 3/4 di 18 fa 13, poi +4 taglia e +8 FOR. TS +6/+8/+6: scarsi a 18 DV fanno +6, più DES +2 sui Riflessi. Media SRD 129 pf (99 + 30). CA 30 / contatto 11 / colto 28.
- **Tordek.** Raffica +12/+12/+7: BAB +10 al monaco 9 senza penalità, più FOR +2.
- **Round di sorpresa.** «agisce ogni PG pronto, con un'azione standard o di movimento a testa».
- **Spingere.** «al massimo di una taglia più grande».

## NUOVI

1. 🟠 **L'Atlante Mappe contraddice il master sulla regola che chiudeva il 🔴.**

   `Mappe/ARC07-MAPPE-DEFINITIVO.md`, righe 140-144: «emergono, colpo pieno (3 artigli + morso), riaffondano con azione preparata — NON restano 2 round in superficie (colpiscili solo quando sono fuori)» e «bersagliare gli Xorn *nel round in cui emergono* (readied)». Qui è peggio della versione vecchia del master, perché dà allo Xorn anche l'attacco completo fra i due movimenti.

   Restano vecchie anche altre due righe dell'Atlante:
   - la riga 260: «pareti di magnetite LETALI»;
   - la riga 329: «tienilo in zero-G → perde la rigenerazione», che il master ora smentisce («il gruppo non ha come spingercelo»).

   Il master manda all'Atlante come «Versione a piena scheda tattica» e scrive «**I booklet includono l'Atlante.**». Un DM che stampa il booklet ha quindi le due regole una accanto all'altra. FIX.md lo dichiara, ma la correzione non è arrivata nel file.

2. 🟡 **Un refuso nato dalla sostituzione da «lancia» ad «ascia».**

   Lo yes-and del §7a, righe 1341-1342: «(la l'ascia di Thorik come rampino, un detrito cavalcato…)». L'articolo è doppio. Va scritto «(l'ascia di Thorik come rampino…)».

3. 🟡 **«Rigenerazione» resta in due punti, dopo che la correzione l'ha dichiarata sbagliata.**

   Lo statblocco e la Quick-Reference adesso dicono «guarigione rapida, non la Rigenerazione dell'SRD: il danno resta letale». Altrove però il nome è ancora quello vecchio:
   - Scalare lo scontro, riga «Party logorato»: «la Rigenerazione scende a 10/round», con la maiuscola, cioè proprio il nome della regola SRD;
   - la Radice a Terra: «(NIENTE RIGENERAZIONE)».

   Un DM che legge la sidebar da sola torna al dubbio del DEV#19. Basta scrivere «la guarigione scende a 10/round» e «niente guarigione».
