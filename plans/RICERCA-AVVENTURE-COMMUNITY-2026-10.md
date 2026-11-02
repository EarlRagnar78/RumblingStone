# RICERCA — Le avventure della community 3.5 e PF1e, messe accanto ai nostri DEF

*2026-10-18, su richiesta del DM. Il lotto 1 è applicato in [PIANO-AVVENTURE-COMMUNITY](PIANO-AVVENTURE-COMMUNITY-2026-10.md) e deciso in [ADR-0092](adr/ADR-0092-le-domande-dell-alto-livello.md); il resto è proposta.*

Le note complete delle quattro ricerche, con ogni affermazione marcata LETTO (con l'URL) o DEDOTTO, stanno in [`esperimenti/avventure-community/`](esperimenti/avventure-community/):
[italia](esperimenti/avventure-community/note-italia.md) · [Paizo e PFS](esperimenti/avventure-community/note-paizo.md) · [editori terzi](esperimenti/avventure-community/note-3pp.md) · [metodi di design](esperimenti/avventure-community/note-metodi.md).

---

## 0 · Prima di cominciare

**Informazioni che mi mancano.**

1. Non so quali avventure intendessi con «gruppo Dragons' Lair». Sul sito ci sono 18 avventure 3.5 della community, ma il download richiede l'accesso e nessun PDF è stato letto. Con un account se ne scaricano due o tre (per esempio «La Scelta») e si analizzano come quelle del Gruppo Chimera.
2. Non ho letto per intero un incontro di Frog God, Raging Swan o Paizo con statblock e tattiche. Il testo completo circola solo in copie non autorizzate, che ho escluso. Ho letto le anteprime ufficiali (le prime 6-8 pagine), i saggi degli autori, i giudici di RPG Superstar e le recensioni dettagliate.
3. Non so quale master verrà rifatto per primo. Ho assunto **ARC-08**, perché il prossimo passo dichiarato in memoria è A3 di PIANO-MASTER-DEF, il canone di ARC-08.

**Assunzioni.**

- Il bersaglio è una campagna 3.5 con PG di 13° livello e quattro giocatori fissi, non un torneo né un programma organizzato. Molte pratiche della community nascono per tavoli di estranei a livello basso: le ho filtrate con questo criterio.
- Vale la tua preferenza per la versione più forte. Dove una proposta tocca un numero, la scelta resta quella più potente, e la proposta riguarda la forma.
- Vale la regola d'oro G3: una norma nuova arriva con chi la misura e con il suo lotto di applicazione. Ogni proposta qui sotto dice chi la misurerebbe.

---

## 1 · Il giudizio d'insieme, onesto

Il nostro standard è già **più severo di quasi tutto quello che ho letto**. Area chiave secondo *Dungeon*, tattiche dal punto di vista del mostro agganciate alla mappa, soglie di morale, riscalatura a tre assi con «cosa si perde davvero», Echo Ledger, rilettura a freddo con rubriche fisse e cancelli in CI: nessun editore terzo dichiara un processo così. Endzeitgeist, il recensore più minuzioso delle 3PP PF1e, toglie stelle soprattutto per mappe dei giocatori assenti, errori di statblock e formattazione che non aiuta a condurre. Sono difetti che da noi intercettano già `collaudo_mappe` (D9), `conformita_statblocchi` e il lettore a freddo.

Quello che la community fa meglio non è la profondità. Sono tre cose precise:

1. **L'alto livello.** Gli autori che scrivono per l'11° livello e oltre (Dancey e Moreland nei giudizi di RPG Superstar, la scuola Necromancer) danno per scontato che i PG volino, divinino, scrutino e si teletrasportino, e scrivono ogni luogo e ogni segreto *contro* queste capacità. Noi lo facciamo bene per il combattimento (domanda 2 del developer) e poco per i segreti e i luoghi.
2. **Il sito come sistema.** L'Alexandrian, Bryce Lynch e Frog God trattano un luogo ostile come una popolazione che reagisce: chi c'è, chi si muove, chi arriva e in quanti round. Noi rispondiamo scontro per scontro («chi sente il rumore»), non per sito. Per un assedio come ARC-08 è la differenza più grossa.
3. **Gli indici d'uso.** Tabella degli incontri in testa al modulo (DCC), elenco degli statblocchi con le scene in cui compaiono (Raging Swan), foglio dello scontro con tutti i blocchi e il testo degli incantesimi (il PDF che WotC diede per RHoD). Da noi i dati ci sono, ma vanno cercati.

Le avventure del Gruppo Chimera sono l'unica fonte italiana solida: scritte bene, con un'ottima gestione del tempo reale e dell'indagine contro la magia, ma tarate su un torneo di quattro ore a livello 5-6. Ne vale la pena la forma, non il tono goliardico né il punteggio.

---

## 2 · FASE 1 · Audit: dove siamo, misurato

Ho controllato nel repo, con grep sui cinque master di ARC-07, le cose che le fonti dicono di fare. Sono conteggi grezzi: dicono se la parola c'è, non se la risposta regge.

| Pratica della community | Fonte | Nei DEF di ARC-07 | Esito |
|---|---|---|---|
| Riga di scala per **ogni** combattimento | PFS, «Scaling Encounter» | «Scalare» compare 10 volte in DEF-1, 0 in DEF-2 e DEF-3, 1 in DEF-4 e DEF-5 | **manca fuori dai boss** |
| Ogni segreto ha il suo «e se lo divinano?» | Dancey, RPG Superstar 2011 | divinazione, scrutare, teletrasporto: 0-3 menzioni per master, quasi tutte sul teletrasporto in combattimento | **manca** |
| Statistiche senza buff accanto a quelle stampate | Paizo AP, *Base Statistics* | 0 nei DEF, nessuna nel Bestiario | **manca** |
| Tattiche *Prima / Durante / Morale* | Paizo AP | già prescritte da ADR-0091 | **c'è** |
| Roster dei nemici del sito, normale e in allerta | Alexandrian, *Art of the Key* 4 | «roster» è solo la legenda dei token sulla mappa | **manca** |
| Misura degli anelli e dei punti unici di guasto della mappa | Alexandrian (Xandering), Bryce | nessuna misura | **manca** |
| Vista giocatori senza segreti | tutti, Endzeitgeist | `@vista giocatori` in `collaudo_mappe` | **c'è**, da verificare che tolga anche numeri, trappole e token |
| Segnalibri e PDF da schermo | Raging Swan, Endzeitgeist | Typst con segnalibri (ADR-0020) | **c'è** |
| Lista delle rivelazioni di un'indagine | Alexandrian | i nodi e le sei porte ci sono; la lista con il conteggio no | **parziale** |
| Tabella degli incontri e elenco degli statblocchi | DCC, Raging Swan | Quick-Reference con le CD; nessun indice incrociato | **manca** |
| Blocco breve per gli sgherri | Alexandrian, discussione ENWorld | ADR-0091 ha dossier pieno, dossier breve e Comparse; nessun blocco statistico ridotto | **manca** |

Cosa questo audit non ha potuto verificare: se i master di ARC-08 e ARC-09 hanno già alcune di queste cose (non sono ancora DEF), e se le domande del developer nuove troverebbero difetti veri o solo rumore. Per quello serve il primo lotto, misurato.

---

## 3 · Le proposte, in ordine di valore per noi

Ogni proposta dice **da dove viene**, **cosa si scrive**, **chi la misura** e **dove va**. Le prime sei sono quelle che consiglio; le altre sono buone ma meno urgenti.

### 3.1 · Le sei che consiglio

**P1 · Il test di divinazione, per ogni segreto.** *(Ryan Dancey, giudice di RPG Superstar 2011; Moreland 2012)*
Sopra l'11° livello i segreti non reggono: *divinazione*, *comunione*, *leggende e tradizioni*, *scrutare*, *localizza creatura*. Per ogni segreto del master una riga: quale incantesimo lo rompe, cosa ottiene il PG che lo lancia, e come prosegue il modulo se lo rompono. La risposta giusta non è «lo impedisce una schermatura» (quella è la risposta pigra), ma «il modulo cambia strada e premia chi l'ha lanciato». Al nostro livello è la proposta più specifica e quella con più resa.
Misura: una domanda 9 in `sviluppo-degli-incontri.md`, letta da `domande_developer.py` (cerca, per ogni segreto marcato, la riga «Se lo divinano»). Va accanto alla domanda 2 su volo e invisibilità, che è la stessa idea per il combattimento.

**P2 · Il roster dei nemici del sito, con l'ordine di battaglia.** *(Alexandrian, Art of the Key parte 4; Bryce Lynch; Frog God)*
Per ogni luogo con quattro o più gruppi ostili, un'appendice: *gruppo · tipo (di pattuglia, mobile, fermo) · dove sta · cosa sta facendo · chi chiama e in quanti round arriva*, in due colonne, **normale** e **in allerta** (e giorno/notte dove serve). Tetto di venti gruppi. «Chi sente il rumore» resta nella scena e diventa una riga del roster. Ogni gruppo mobile ha un verbo («porta il prigioniero al pozzo»), non solo una posizione.
Per ARC-08, la battaglia di Hammerfist, è il formato naturale: le ondate della Mano Rossa sono già un roster che il master racconta in prosa.
Misura: `copertura_scene` o `collaudo_mappe` verificano che un sito con quattro o più gruppi abbia il roster e che i numeri coincidano con i token della mappa.

**P3 · La riga di scala per ogni combattimento.** *(Pathfinder Society, sidebar «Scaling Encounter»)*
Oggi la sidebar «Scalare lo scontro» è obbligatoria solo per il boss. PFS la mette a ogni scontro, in una frase, e la lega alla fiction: non «togli un hobgoblin», ma «manca il sergente, che è rimasto al corno, quindi l'allarme parte un round prima». Per un gruppo fisso di quattro serve soprattutto per il PG assente o morto, che al nostro tavolo è già successo (Hella).
Misura: estensione del controllo esistente sul boss, per ogni scena con EL.

**P4 · Statistiche base e i due stati di «prima del combattimento».** *(Paizo AP, Base Statistics)*
Lo statblocco si stampa **già potenziato** (è la versione più forte, ed è coerente con la tua preferenza), e una riga dice cosa cambia senza i potenziamenti: CA, TS, pf, attacchi. «Prima del combattimento» si scrive in due stati, **avvisato** (con i round di preparazione che servono) e **sorpreso**. Oggi un DM che viene sorpreso dai PG deve ricalcolare a mano il boss senza *scudo della fede* e *forza del toro*.
Misura: `conformita_statblocchi` controlla che un blocco che dichiara incantesimi di preparazione abbia la riga «Statistiche base». È un'aggiunta ad ADR-0091 §4.

**P5 · Il foglio dello scontro, generato.** *(WotC per Red Hand of Doom; Alexandrian; Raging Swan)*
Per ogni scontro, una facciata A4 con i blocchi di tutte le creature, la mappa ridotta e **il testo breve degli incantesimi e delle capacità che le tattiche usano** (gittata, TS, effetto). Le pagine A4 di statistiche ci sono già; manca il testo degli incantesimi, che al 13° è la ragione per cui il DM sfoglia il Manuale del Giocatore durante lo scontro. In testa all'elenco degli incantesimi di un PNG, i 5-8 che userà davvero (quelli citati nelle tattiche), poi il resto.
Misura: ogni incantesimo citato nelle tattiche ha il suo effetto nel foglio. Si genera da `componenti.py` (ADR-0074), non si scrive a mano.

**P6 · Le domande del developer che ci mancano.** *(giudici di RPG Superstar 2016: Compton, Helt, Stephens)*
Da aggiungere a `sviluppo-degli-incontri.md`, perché sono domande vere e non doppioni delle nostre otto:

- **Sostituzione**: questo mostro fa qualcosa che un altro dello stesso GS non farebbe? Se no, è un segnaposto.
- **Il pericolo usato**: ogni pericolo della mappa (lava, precipizio, corrente) ha almeno un nemico che ci spinge dentro i PG, e i PG possono usarlo contro i nemici?
- **L'incontro che si spezza**: nell'ordine probabile, lo scontro resta uno o diventa due di seguito, più deboli?
- **Il rinforzo telegrafato**: se arrivano rinforzi, i PG hanno un segno che li avverte? Se lo sa solo il DM, non c'è urgenza.
- **Niente dossi al 13°**: un'orda di GS basso sparisce con un incantesimo ad area. Cosa la tiene in vita (copertura, dispersione, ondate), oppure diventa boss più luogotenente.
- **Tempo senza agire**: per ogni effetto «salva o sei fuori» (dominare, paralizzare, pietrificare), cosa fa il giocatore colpito nei round in cui il suo PG è fermo.

Misura: le prime quattro le legge un agente (non sono forma del testo); la quinta e la sesta sono misurabili da `domande_developer.py` come le domande 2 e 3.

### 3.2 · Buone, meno urgenti

**Struttura del master (DEF)**

- **Intestazione di zona** *(Necromancer Games, Rappan Athuk)*. Ogni dungeon o edificio apre con otto voci fisse: livello di sfida, ingressi, uscite, erranti, schermature, rilevazioni, effetti continui, caratteristiche standard (porte, luce, muri). Al 13° risponde in anticipo alle domande che arrivano al primo minuto (si può scrutare dentro? si può teletrasportarsi?). Va d'accordo con P1.
- **Tabella degli incontri ed elenco degli statblocchi** *(DCC, Raging Swan)*. In testa al master: codice, pagina, tipo (combattimento, sociale, trappola, enigma, esplorazione), EL, numero di vie non combattive. In testa alle appendici: statblocco, GS, appendice, scene dove compare. Rende visibile la miscela dei tipi sull'intero modulo. Generabile da `componenti.py`.
- **«Cosa sanno i PG» in apertura di ogni atto** *(Raging Swan)*. Tre-cinque fatti già in mano al tavolo, in elenco. Serve dopo la pausa fra due serate.
- **Condizione di successo secondaria per atto** *(PFS)*. Una frase verificabile prima della sessione («Durin sopravvive alla notte»), collegata a un'eco nell'Echo Ledger se riesce o se manca.
- **Parità di ricompensa per le soluzioni creative** *(PFS, «Creative Solutions»; Legendary Games)*. Se l'obiettivo si raggiunge senza uccidere, PX e tesoro restano uguali e il testo dice dove si sposta il tesoro (dal cadavere al forziere del campo). Abbiamo già due vie non combattive per incontro; manca la garanzia che non costino al tavolo.
- **Scheda-favore in mano ai giocatori** *(PFS, Chronicle sheet)*. Il gemello lato giocatore dell'Echo Ledger: un favore con un nome, chi lo concede e come si riscatta. È un handout, non canone scritto da script (ADR-0007).
- **Il salvagente a orario** *(Gruppo Chimera, L'Aquila e il Drago e Mala Tempora Currunt)*. Nel blocco contingenze un campo: chi interviene se il tavolo è fermo, dopo quanto stallo, e **cosa costa**. Da loro è un PNG che crolla o agisce per conto suo; da noi il costo va nell'Echo Ledger. Rafforza i «cancelli d'uscita a tempo» che abbiamo, che dicono chi entra ma non cosa si paga.
- **La scena lunga scritta anche corta** *(Gruppo Chimera, «manca meno di un'ora»)*. Per le una-due scene più lunghe di una serata, la versione compressa già scritta, con cosa si salta e quale indizio arriva comunque. L'appendice C di DEF-4 («le versioni veloci») è già questa idea: va resa una voce dello standard.
- **Esiti nominati con la battuta pronta** *(Gruppo Chimera)*. Per ogni incontro chiave, due-quattro esiti etichettati A/B/C, ognuno con la prima battuta del PNG. Il DM non improvvisa la reazione, e l'esito porta dritto all'eco.
- **Il profilo a quattro assi** *(Gruppo Chimera)*. In testa al master, quattro righe a stelle: combattimento, esplorazione, interazione, complessità per il DM. Costa cinque minuti e dice al DM come prepararsi.
- **Rimpiazzi in scena** *(Grey Citadel, Slumbering Tsar)*. Ogni atto con rischio di morte nomina uno o due PNG che possono entrare nel gruppo, e da quale momento consegnarli non rompe la trama.
- **Attrezzi del cattivo** *(Alexandrian, «Don't Prep Plots: Tools, Not Contingencies»)*. Attenzione: la fonte sconsiglia proprio la nostra voce 9, l'albero «se i PG fanno X». Non propongo di toglierla: la riga della sconfitta e le contingenze ovvie restano. Propongo di affiancarle, per ogni antagonista, un riquadro **Risorse** (persone, equipaggiamento, luoghi, informazioni, ognuno con a cosa serve) e la sua **squadra di risposta**. Al 13° i PG fanno piani che nessun albero prevede, e con le risorse il DM risponde senza inventare.

**Indagine** (`rumblingstone-indagine`)

- **La magia contro l'indagine** *(Gruppo Chimera, Il Ladro di Stelle e L'Aquila e il Drago)*. Un riquadro con i TS Volontà di tutti i PNG interrogabili e l'esito di ogni incantesimo d'informazione probabile al livello del gruppo (charme, *zona di verità*, *individuazione dei pensieri*, *parlare con i morti*). È P1 applicato ai testimoni.
- **La lista delle rivelazioni con il conteggio** *(Alexandrian)*. Conclusioni, dove stanno gli indizi, quanti per conclusione. Almeno tre per conclusione e tre entranti per nodo, con la struttura dichiarata (imbuto, torta a strati, anello).
- **L'indizio che paga in vantaggio tattico** *(Grey Citadel)*. Ogni nodo che precede uno scontro dichiara il vantaggio concreto che dà (la debolezza, l'accesso laterale, il rinforzo da tagliare).
- **Le domande scritte sui foglietti** *(Gruppo Chimera, Mala Tempora Currunt)*. Prima di un briefing obbligato (il consiglio di guerra di re Thorek, per esempio), i giocatori scrivono le domande; il DM distribuisce il testo fisso sulle domande e risponde a chi l'ha scritta. Toglie l'infodump e dà spazio a tutti e quattro.

**Mappe** (`rumblingstone-mapmaking`)

- **Topologia misurata** *(Alexandrian, Xandering; Bryce)*. In `collaudo_mappe.py`: ingressi, anelli nel grafo delle aree, profondità delle diramazioni, punti unici di guasto sulla via obbligata. Un avviso, non un errore: un rifugio a corridoio unico può essere voluto, e si dichiara con `@deroga`.
- **Raccordo fra i piani** *(giudici di RPG Superstar, round mappa)*. Ogni scala, botola o porta segreta dice dove arriva, e le due estremità combaciano sulle due mappe.
- **Contrasto e daltonismo** *(stesso round)*. La texture a pergamena non deve nascondere la griglia, e la mappa deve reggere senza distinguere il rosso dal verde.
- **Vista giocatori completa** *(Endzeitgeist, Frog God)*. Verificare che `@vista giocatori` tolga anche numeri, trappole, token nemici e annotazioni, e che la griglia sia attenuata.
- **Mappe di Dyson Logos** come base per i luoghi minori: gratuite anche per uso commerciale, con credito. Prima va letto il suo accordo d'uso completo e passato il gate di `rumblingstone-edizione`; la licenza riserva i diritti morali (legge canadese) e non copre il testo dei post.

**Playtest** (`rumblingstone-playtest`)

- **La prova dei piani non previsti** *(Alexandrian)*. Il playtester a freddo riceve tre piani che il master non contempla (ingresso in volo dal tetto, *scrutare* più *teletrasporto* nella stanza del boss, travestimento) e annota se le cose scritte bastano a risolverli. 🔴 se il DM deve inventare dove stanno i nemici. È la prova che rende misurabili P1, P2 e gli attrezzi del cattivo.
- **Ore di preparazione per una serata** *(Bryce Lynch, scala della complessità per il DM)*. Il DM a freddo cronometra quanto gli serve per essere pronto. È una misura che ci manca: dice se il master aiuta o pesa.
- **Il collaudo dentro il testo** *(Stoneheart Valley, The Wizard's Amulet)*. Una o due frasi nel master con quello che il tavolo ha insegnato e che cambia la conduzione («al tavolo il duello ha preso 50 minuti»). I rilievi numerati restano nei rapporti; qui resta ciò che serve a chi conduce dopo.
- **I criteri di Endzeitgeist nella rubrica del lettore** *(note-3pp §5)*. Ne ho estratti 13 ricorrenti. Almeno tre sono nuovi per noi: le regole corrispondono alla storia, la coerenza fra GS e numeri, l'abilità del giocatore che conta più dei dadi.
- **Due giudizi separati nel debrief**, del DM e dei giocatori *(un giocatore PFS)*. Uno scenario può piacere a chi conduce e annoiare il tavolo.

**Stile** (`rumblingstone-narrative-style`, con il tetto dei box che vince sempre)

- **Solo la storia che cambia il gioco** *(Bryce)*. Ogni paragrafo di storia del luogo finisce in un indizio, una CD, un'eco o un aggancio; altrimenti va in appendice o si taglia.
- **Il dettaglio giocabile** *(Raging Swan)*. Ogni dettaglio d'ambiente segnala un pericolo, nasconde qualcosa o premia chi osserva.
- **Una frase che tutti ripetono** *(Bryce)*. Per ogni luogo che i PG temono prima di arrivarci, una frase sola che torna da più bocche («Non scendete nel Pozzo»). Presagio del cattivo a costo quasi zero.
- **L'handout privato per un PG** *(Goodman, The Wizard's Amulet)*. Da leggere da solo e rivelare quando vuole. Si sposa con gli highlight asimmetrici.
- **Il tesoro che racconta** *(Rise of the Drow)*. Per gli oggetti non banali, aspetto e origine, con la CD per scoprirla, collegata all'Echo Ledger quando l'origine è un PNG.

---

## 4 · Cosa non portare, e perché

| Pratica | Chi | Perché no |
|---|---|---|
| Punteggio da torneo, pregenerati, classifiche | Gruppo Chimera, DCC | abbiamo quattro PG fissi e una campagna. Si salva solo l'idea del costo del salvagente, tradotta in eco |
| Deus ex machina gratuiti e tono goliardico | Gruppo Chimera | tolgono protagonismo ai PG e vanno contro il registro di `narrative-style` |
| Statblock doppi per due sistemi | Gruppo Chimera | raddoppiano il testo da mantenere; noi abbiamo una linea sola (3.5 con forma PF1e, ADR-0091) |
| Subtier, Prestige, Fame, «run as written» | PFS | servono all'equità fra tavoli di estranei. «Run as written» contraddice il mondo vivo e lo *yes-and with teeth* |
| Limiti di parole e «massimo tre combattimenti» | PFS, Moreland | tarati su quattro ore a livello medio. Ne prendiamo il segnale (un combattimento in più costa storia), non il numero |
| Letalità da prima edizione come valore, anti-ecologia | Necromancer | contraddice la sconfitta senza TPK e l'agenda dei PNG |
| Genericità «per inserirlo in qualunque campagna» | Raging Swan, Frog God | noi scriviamo per un canone solo, il 1372 DR |
| Statistiche e mappe in volumi separati, statblock come link | Rappan Athuk Reloaded, AAW | i due difetti d'uso più citati dalle recensioni |
| Abolire il read-aloud | Bryce Lynch | il tetto di 12 righe, un nome proprio e niente parentesi è già la risposta alla sua critica |
| Blocchi corti anche per il boss | Bryce | al 13° in 3.5 un boss senza blocco completo è ingiocabile. Si accorcia lo sgherro, non il boss |
| Regole 5e del Lazy DM (benchmark, vantaggio) | Sly Flourish | sistema diverso. Si salvano solo i segreti senza luogo e l'apertura forte |
| Hexcrawl completo, incontri casuali pesanti nei siti con roster | Alexandrian | la campagna è ad archi; basta il pointcrawl per i viaggi |
| Loop temporali come struttura | Gruppo Chimera, Mala Tempora Currunt | ottimi in una serata singola, ingestibili con la coerenza di un arco lungo (regola 8) |

Una correzione alle note di ricerca: la nota sull'Aquila e il Drago dice che i nostri statblock stanno «vicino all'incontro». Non è così: il nostro standard li mette in appendice A4, come il Gruppo Chimera. La differenza vera è che noi diamo la pagina da tenere aperta, e P5 la completa.

---

## 5 · FASE 2 · Piano di applicazione

Tre lotti, ognuno con la sua misura, come chiede G3. Nessuno richiede di riscrivere i cinque master di ARC-07 già giocati: valgono per i master nuovi e per quelli che un lotto riscrive.

**Lotto 1 · Alto livello e statblocchi** (P1, P3, P4, P6)
1. `fase1.py` sui bersagli, poi il registro delle norme: nessuna di queste è già misurata da qualcuno.
2. Domande 9-14 in `sviluppo-degli-incontri.md`; regole nuove in `domande_developer.py` per le misurabili (divinazione, riga di scala, dossi, tempo senza agire).
3. Riga «Statistiche base» e «Prima del combattimento» a due stati in ADR-0091 §4, con il controllo in `conformita_statblocchi`.
4. Registrazione in `REGISTRO-NORME-EDITORIALI.md` con chi misura.
5. Lotto di applicazione: ARC-08, insieme ad A3 di PIANO-MASTER-DEF. Se lo applicassimo solo alla skill sarebbe «lettera morta», come dice AGENTS.md.

**Lotto 2 · Il sito come sistema e gli indici** (P2, P5, intestazione di zona, tabella degli incontri, elenco degli statblocchi)
1. Formato del roster (normale/allerta) come componente di ADR-0074, per poterlo generare e controllare.
2. Foglio dello scontro e indici generati da `componenti.py --apparato`.
3. Controllo roster↔token in `collaudo_mappe`.
4. Applicazione: le ondate di ARC-08.

**Lotto 3 · Mappe, playtest, indagine, stile** (il resto di §3.2, a scelta)
Si apre solo dopo aver visto se i lotti 1 e 2 hanno trovato difetti veri.

---

## 6 · FASE 3 · Come si verifica che migliora

- **Prima della norma, la misura**: le regole nuove di `domande_developer.py` si eseguono sui cinque master di ARC-07 (sola lettura) e sui file di ARC-08. Si contano i rilievi e, a mano, i falsi positivi, come per la calibrazione di DEF-4. Se una regola dà più falsi positivi che rilievi veri, non entra.
- **Il controllo che conta**: la prova dei piani non previsti, fatta da un playtester a freddo su ARC-08 prima e dopo il lotto 1. Il risultato atteso è meno 🔴 «il DM inventa dove stanno i nemici» e «il segreto cade alla prima divinazione». Se il numero non scende, il lotto non ha funzionato, e va scritto.
- **Il costo**: le ore di preparazione del DM a freddo su ARC-08, prima e dopo il foglio dello scontro. Se il foglio non le riduce, è burocrazia.
- **Il tavolo**: alla prima serata di ARC-08, nel debrief, una domanda sola per il DM («hai sfogliato un manuale durante uno scontro?») e una per i giocatori («c'è stato un momento in cui non potevi fare niente?»).
- **Cosa questa verifica non dirà**: se il modulo è più divertente. Lo dice solo il tavolo.

---

## 7 · Limiti di questa ricerca

- Del Gruppo Chimera ho letto quattro PDF per intero o quasi (*Fino alla Fine del Mondo*, *Il Ladro di Stelle*, *Mala Tempora Currunt*, *L'Aquila e il Drago*); di *L'importante è partecipare* solo un riassunto automatico. L'OCR è sporco in alcune parti (la cronologia di Mala, le mappe ridotte a etichette).
- Dragons' Lair è una fonte debole: i download richiedono l'accesso. Su Revelsh Blind Beholders, goblins.net, Lande di Flanaess e i concorsi di Lucca non ho trovato avventure 3.5/PF vere: non escludo che ci siano.
- Degli editori terzi ho visto struttura e introduzioni, non un incontro completo. Kobold Press è quasi tutto di seconda mano: i saggi non sono liberi.
- Il formato completo di uno scenario PFS1 viene in parte da memoria. Si verifica su uno scenario gratuito ufficiale (per esempio *Master of the Fallen Fortress*), che richiede un account Paizo.
- WebFetch passa le pagine a un modello che le riassume. Le citazioni più affidabili sono quelle estratte alla lettera da Firecrawl: la Guild Guide PFS, il thread di *Rimesoul Nexus* e i PDF del Gruppo Chimera.

---

## Fonti principali

**Italia** · [Gruppo Chimera, avventure 3.5 e PF](http://www.gruppochimera.it/avventure-dd-35-scaricare) · [Fino alla Fine del Mondo](http://www.gruppochimera.it/it/avventura/fino-alla-fine-mondo) · [Il Ladro di Stelle](https://www.gruppochimera.it/it/avventura/ladro-stelle) · [L'Aquila e il Drago (PDF)](https://www.gruppochimera.it/sites/default/files/gc-adventure/files/2020-02/AQUILADRAGO_AVVENTURA_2014.pdf) · [Mala Tempora Currunt (PDF)](https://www.gruppochimera.it/sites/default/files/gc-adventure/files/2020-02/Mala_tempora_currunt_ALL.pdf) · [Valutazione di un torneo](https://www.gruppochimera.it/it/articoli/valutazione-un-torneo-parte-1) · [Dragons' Lair, avventure](https://www.dragonslair.it/files/category/6-avventure/) · [Dragons' Lair, le migliori avventure di sempre](https://www.dragonslair.it/forums/topic/48288-le-migliori-avventure-di-sempre-per-dd/)

**Paizo e PFS** · [RPG Superstar 2016, Rimesoul Nexus](https://paizo.com/threads/rzs2sza4?Rimesoul-Nexus) · [Fellforge Chapel](https://paizo.com/threads/rzs2s04u) · [Reefclaw Brewery, round mappa](https://paizo.com/threads/rzs2rwsp) · [Dancey, il round finale](https://paizo.com/threads/rzs2m05j) · [Reynolds, Superstar Maps](https://paizo.com/blog/design-tuesday-superstar-maps) · [Sutter, Maps, Maps, Maps](https://cdn.paizo.com/blog/maps-maps-maps) · [Moreland, Advice from Your Future](https://paizo.com/blog/rpg-superstar-trade-advice-from-your-future)

**Editori terzi** · [Raging Swan Press](https://www.ragingswanpress.com/) · [Dungeon design tips for beginners](https://www.ragingswanpress.com/swan-blog/dungeon-design-tips-for-beginners) · [Intervista a Broadhurst, Tribality 2015](https://www.tribality.com/2015/01/12/interview-with-creighton-broadhurst-of-raging-swan-press/) · [Necromancer e Frog God, Black Gate](https://www.blackgate.com/2015/11/09/of-necromancers-frog-gods-part-one/) · [ENWorld su The Grey Citadel](https://www.enworld.org/threads/the-grey-citadel.118592/) · [ENWorld, the incredible shrinking stat block](https://www.enworld.org/threads/the-incredible-shrinking-stat-block.310846/) · [ENnies 2014](https://ennie-awards.com/portfolio-item/2014-nominees-and-winners/)

**Metodi** · [Alexandrian, Adversary Rosters](https://thealexandrian.net/wordpress/38547/roleplaying-games/the-art-of-the-key-part-4-adversary-rosters) · [Tools, Not Contingencies](https://thealexandrian.net/wordpress/37422/roleplaying-games/dont-prep-plots-tools-not-contingencies) · [Jaquaying the Dungeon](https://thealexandrian.net/wordpress/13085/roleplaying-games/jaquaying-the-dungeon) · [Xandering techniques](https://thealexandrian.net/wordpress/13103/roleplaying-games/xandering-the-dungeon-part-2-xandering-techniques) · [Party Planning](https://thealexandrian.net/wordpress/37995/roleplaying-games/game-structure-party-planning) · [Pointcrawls](https://thealexandrian.net/wordpress/48666/roleplaying-games/pointcrawls) · [How to Prep a Module](https://thealexandrian.net/wordpress/46535/roleplaying-games/how-to-prep-a-module-part-2) · [Alexandrian, stat block](https://thealexandrian.net/creations/advanced-rules/stat-block.html) · [Bryce Lynch, review standards](https://tenfootpole.org/ironspike/?page_id=1201) · [Sly Flourish, otto passi](https://slyflourish.com/eight_steps_2023.html) · [Dyson Logos, mappe commerciali](https://dysonlogos.blog/maps/commercial-maps/)

---

## 8 · Stato d'attuazione

| Lotto | Cosa | Stato |
|---|---|---|
| 1 | P1, P3, P4, P6: le §9-§16 di `sviluppo-degli-incontri.md`, le regole D9, D10, D15, D16 di `domande_developer.py`, la riga «Statistiche base» e i due stati di «Prima del combattimento» (ADR-0092) | ✅ norma e misura; applicazione con S1 di PIANO-MASTER-DEF |
| 2 | P2, P5, intestazione di zona, tabella degli incontri ed elenco degli statblocchi | ⬜ |
| 3 | il resto della §3.2 | ⬜ dopo la misura del lotto 1 |

La calibrazione delle regole nuove sui nove moduli sotto cancello è nel piano, §2.

