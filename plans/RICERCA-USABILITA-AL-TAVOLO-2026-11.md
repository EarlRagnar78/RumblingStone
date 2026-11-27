# Ricerca — Cosa rende un'avventura buona e usabile al tavolo, e quanto ci siamo

**Data**: 2026-11-03
**Richiesta**: il DM (Jfs), 2026-11-02, dopo la serata di *Notte e Alba*:

> *«per ogni capitolo accanto alla scheda una descrizione, una sua immagine e
> chi è e cosa vuole credo sia il minimo standard sindacale da adottare, e poi
> lo leggi da DM, così si vede dove e se trova le cose e sono facili da capire e
> applicare. È un gioco, ma il master deve capirlo al volo e adattarlo se serve
> […] Cerca in giro cosa i master reputano caratteristiche chiave per
> un'avventura e misura quante ce ne sono da noi nel repo e come migliorarlo»*

e poco dopo: *«aggiungi ricerca in rete quali sono, dai master, le migliori
avventure e perché, quali caratteristiche e configurazione e qualità devono
avere, e misurare con il nostro repo dove e in che modo migliorarlo con ADR,
skill, plugin, tool»*.

**Esito in una riga**: la ricerca conferma lo standard del DM (è il modello
Paizo della scheda alla prima comparsa e il modello dell'Alexandrian della
scheda della persona). Nei 10 booklet del DM, su **145** coppie capitolo ×
persona che ci compare, solo **6** hanno tutto (scheda, aspetto, ritratto, chi
è, cosa vuole, tattica) e **0** hanno i numeri stampati nel capitolo; su **41**
capitoli con uno scontro, **7** hanno la mappa nel capitolo. La proposta è
[ADR-0107](adr/ADR-0107-chi-si-incontra-sta-nel-capitolo.md), che emenda il
punto 7 di ADR-0105: la scheda nel capitolo **e** l'appendice, come ha chiesto
il DM il 2026-11-03.

---

## 0. Premesse

**Che cosa manca per rispondere meglio, dichiarato.**

- Un voto dei master su un campione ampio. Le classifiche trovate sono
  sondaggi di forum (EN World, RPGnet, Reddit), una classifica di redazione
  (Dungeon n. 116, 2004) e due recensori con criteri scritti. Nessuna è un
  campione rappresentativo.
- I PDF degli AP più votati, a parte *Burnt Offerings* (il DM l'ha fornito il
  2026-10-29) e *Red Hand of Doom* (che il repo adatta). Le altre ragioni
  vengono da recensioni e discussioni, non da una lettura mia dei volumi.
- Reddit non si legge da qui (il servizio di scraping lo rifiuta): ne uso
  solo i titoli e gli estratti dei risultati di ricerca, e lo segno.

**Assunzioni.**

- «Capitolo» è il capitolo del booklet stampato (una voce del manifest), non
  il file master: è quello che il DM ha in mano.
- Una «persona» è un PNG o un cattivo con un nome. Guardie, wyvern e mostri
  senza nome hanno bisogno di numeri e tattica, non di «chi è».

---

## 1. Fonti, e cosa dicono

### 1.1 I criteri scritti dai master che recensiscono

| Fonte | Che cos'è | Cosa chiede a un'avventura |
|---|---|---|
| **Justin Alexander**, *Universal NPC Roleplaying Template* (2015) | blog The Alexandrian, ENnie 2024 | una scheda per persona, divisa in voci da usare al tavolo: **Aspetto** (1-2 frasi, un box da leggere), **Battuta**, **Come si interpreta** (2-3 punti, un gesto fisico), **Storia** (breve), **Cosa sa / cosa offre** (a punti), **Statistiche** in fondo. Nasce da un problema preciso: *«la descrizione del PNG era otto paragrafi di testo indifferenziato»*, e il dettaglio importante era *«una frase sola nel quarto paragrafo»*. Il modello viene da Mike Mearls (*In the Belly of the Beast*, 2001), che aveva anche **Goals**, cioè cosa vuole |
| Alexander, *The Art of the Key* 1-4 (2014-2016) | stessa fonte | l'informazione **nell'ordine in cui serve al tavolo**: prima quello che si vede, poi le prove reattive, poi il dettaglio che si scopre cercando. Contro il formato rigido: *«una stanza con un ogre in mezzo parla prima dell'ogre»*. Una **lista degli avversari** separata dalla chiave dei luoghi per chi si muove: *«due blocchi di informazione ordinata invece di una moltitudine»*. Una gerarchia dei rimandi: testo intero, riassunto + pagina, solo pagina, solo nome, man mano che il master conosce il sistema |
| Alexander, *Don't Prep Plots* e *Three Clue Rule* | stessa fonte | **situazioni, non trame**; per ogni conclusione **tre indizi**; per ogni ostacolo che blocca l'avventura **tre strade** |
| **Mike Shea (Sly Flourish)**, *Your Criteria for Selecting Great Published Adventures* (2025) | autore dei *Lazy DM* | struttura chiara che si capisce in fretta; motivazione chiara per i personaggi; **scelte che cambiano la direzione**; **impaginazione facile da consultare al tavolo**; tabelle casuali utili; flessibilità per farla propria; **scrittura economica**; fazioni e cattivi che si muovono; situazioni, non scene a copione. Da evitare: struttura confusa, troppe parole, trama lineare |
| Shea, *Eight Steps of the Lazy DM* | stesso | inizio forte, scene possibili, **segreti e indizi**, luoghi fantastici, **PNG importanti**, mostri, tesori |
| **Bryce Lynch**, *Review Standards*, tenfootpole.org | recensisce migliaia di moduli dal 2011 | atmosfera evocativa; **scrittura asciutta**; **presagi del cattivo principale** (*«nessuno sapeva che Lareth era il cattivo»*); **ordine di battaglia** di chi chiama aiuto; fazioni; mostri che fanno qualcosa; mappe con anelli. Il co-recensore dà voti su: *complessità per il GM* (6 = si apre e si gioca senza preparazione), grafica *«usabile durante il gioco da mostrare ai giocatori»*, lingua *«asciutta ed evocativa»*, mappe *«leggibili e coerenti col testo»* |
| **Ben Milton (Questing Beast)**, *«Control Panel» Page Layout* (2018) | recensore OSR | **tutto quello che serve per un argomento su una pagina o una doppia pagina**, con schemi al posto del testo, per *«assorbire l'informazione più in fretta»* |

### 1.2 Le avventure che i master mettono in cima, e perché

| Avventura | Chi la mette in cima | Perché, secondo chi la loda | Cosa le rimproverano |
|---|---|---|---|
| *Queen of the Spiders*, *Ravenloft* (I6), *Tomb of Horrors*, *Temple of Elemental Evil*, *Keep on the Borderlands* | Dungeon n. 116 (2004), i primi 7 di 30 | la classifica non dà ragioni; nelle discussioni: il cattivo (Strahd), il luogo da esplorare, il sandbox (B2) | sono moduli TSR con chiavi «muro di testo»: Alexander li cita come esempi di cosa *non* fare nella chiave |
| ***Red Hand of Doom*** (WotC 2006) | GiantITP (*«per molti di noi il miglior modulo D&D mai scritto»*), recensori | **un'unica storia coerente** con un orologio (l'orda avanza); ogni scontro ha **una ragione, nemici interessanti e profondità tattica**; **i nemici fuggiti ritornano**; prevede i casi probabili, anche la cattura e la sconfitta; **riquadri grigi dei designer**: perché è così, e come cambiarlo | struttura lineare; l'ultima parte troppo lunga; alcune creature nuove deboli |
| *Rise of the Runelords* (Paizo 2007) | sondaggio EN World (51%), RPGnet | incontri ben costruiti, il primo AP | cattivi che aspettano in una stanza; storia di fondo che i giocatori non scoprono |
| *Curse of the Crimson Throne* (Paizo) | RPGnet, Reddit | *«un sogno da masterizzare: la città e i PNG sono un campo da gioco»* | — |
| *Kingmaker* (Paizo) | RPGnet, Reddit | sandbox | il regno da gestire diventa contabilità |
| *Curse of Strahd* (WotC 2016) | EN World | **un grande cattivo** presente in tutta la campagna; **posta in gioco chiara**; **ambiente chiuso, dettagliato e a tema**, dove ogni luogo porta alleati o pezzi per battere il cattivo | (da altre discussioni: organizzazione che costringe a preparare molto) |
| Le «The Best» di tenfootpole (circa 200 titoli) | Bryce Lynch | ricorrono: *evocativo*, *asciutto*, *situazioni*, *fazioni*, *usabilità*, *«organizzazione e impaginazione»* | — |

Paizo mette la scheda intera di un PNG unico **dove si combatte la prima
volta**, con il ritratto accanto in 8 schede su 15 di *Burnt Offerings* (misura
del 2026-10-29, `standard-stampa/CONFRONTO-PAIZO-AP-2026-10-29.md`); un utente
di r/Pathfinder2e lo indica come la ragione per cui gli AP sono *«più facili da
gestire»*: *«gli statblock unici sono in linea con la loro prima comparsa»*
(estratto di ricerca, pagina non letta).

### 1.3 Che cosa ne tiro fuori

Le fonti si dividono in due famiglie, e servono tutte e due:

- **qualità del gioco**: un cattivo che si sente prima di vederlo, scelte con
  conseguenze, situazioni che si muovono, indizi ridondanti, scontri con una
  ragione;
- **usabilità al tavolo**: trovare in fretta, capire al volo, adattare. Qui il
  DM ha messo il dito: le nostre avventure hanno molta della prima famiglia e
  troppo poco della seconda, e i nostri validatori controllano la forma, non se
  il DM trova le cose.

---

## 2. I criteri, e quali misuriamo già

| # | Criterio | Fonti | Nel repo | Misura |
|---|---|---|---|---|
| K1 | **chi si incontra sta nel capitolo**: numeri, aspetto, ritratto, chi è, cosa vuole, tattica, insieme | Alexander, Paizo, Jfs | scheda d'entrata (ADR-0073), dossier (ADR-0091), riquadro (ADR-0105) | **nuova**: `misura_standard_tavolo.py` |
| K2 | **la mappa dello scontro nel capitolo dello scontro** | Milton, Lynch | ADR-0106 (mappe in pianta) | **nuova**: stessa, colonna `mappa` |
| K3 | l'informazione nell'ordine di gioco (si vede → si prova → si cerca) | Alexander | box per scena (C1 di `copertura_scene`), L-ORDINE di `lettura_a_scene` | in parte |
| K4 | struttura e posta in gioco chiare, una pagina di avvio | Shea, Strahd | §0 QUICKSTART e §0-bis nei DEF | non misurata |
| K5 | situazioni, non trame; scelte con conseguenze visibili | Alexander, Shea, BG3 | D19, Echo Ledger, fronti e orologi (`ARCnn-FRONTI.yaml`) | sì (D19, `validate_*`) |
| K6 | tre indizi per ogni conclusione | Alexander | D21 | sì, dove la rete è marcata |
| K7 | il cattivo si annuncia prima | Lynch, Strahd | D20 | indicatore |
| K8 | il mondo reagisce: chi sente, chi arriva, ordine di battaglia | Lynch, Alexander (lista avversari) | D2, D4 | sì |
| K9 | scrittura asciutta ed evocativa | Lynch, Shea | ADR-0093, Gulpease, `misura_craft` | sì |
| K10 | tattica e morale nell'incontro | Paizo, RHoD | ADR-0091, ADR-0105 §7 | **nuova** (colonna `tatt`) |
| K11 | scontri con una ragione e profondità tattica | RHoD | D1, D5, D10, D15, D16 | sì |
| K12 | note del designer: perché e come cambiarlo | RHoD | §0-ter «quando un giocatore ha un'idea», righe di scala | non misurata |
| K13 | tabelle casuali che aiutano | Shea, Lynch | tabelle di viaggio ARC-09 | non misurata |
| K14 | **letto da DM prima di consegnare** | Jfs, 2026-11-02 | lettura a freddo (skill playtest) | è un processo, non una misura |

La conclusione onesta: dei 14 criteri, i nostri strumenti ne misuravano 8 sul
**master**, nessuno sul **booklet stampato**, e nessuno guardava K1 e K2, cioè
proprio i due che il DM ha pagato al tavolo.

---

## 3. Audit — la misura sul repo (`main` a 7de45df, 2026-11-03)

Comando: `python3 scripts/misura_standard_tavolo.py --dettaglio`. Dieci booklet
del DM, capitoli di gioco (regia, cassetta, introduzione e appendici esclusi).

| Booklet | coppie | complete | num | aspetto | ritratto | chi è | vuole | tattica | mappa nel cap. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ARC-07 Notte e Alba | 24 | 2 | 21% | 50% | 42% | 12% | 50% | 54% | 1/5 |
| ARC-07 Serata resurrezione | 30 | 2 | 13% | 43% | 33% | 10% | 50% | 40% | 3/4 |
| ARC-07 Ritorno alla Forgia | 10 | 0 | 0% | 0% | 0% | 0% | 0% | 20% | 1/2 |
| ARC-07 Sessione Terros | 11 | 0 | 27% | 55% | 0% | 0% | 55% | 64% | 1/2 |
| ARC-07 Volume Mille anni | 19 | 2 | 26% | 63% | 47% | 16% | 63% | 58% | 1/3 |
| Palio | 25 | 0 | 0% | 0% | 0% | 0% | 0% | 28% | 0/9 |
| Giardino di Sale e Calce | 10 | 0 | 0% | 0% | 0% | 0% | 30% | 30% | 0/1 |
| Giardino PF1e | 4 | 0 | 0% | 0% | 0% | 0% | 0% | 25% | 0/1 |
| Drappo (DM) | 6 | 0 | 33% | 0% | 33% | 0% | 33% | 50% | 0/10 |
| Abbazia della Rotta Sicura | 6 | 0 | 67% | 0% | 0% | 0% | 0% | 17% | 0/4 |
| **Totale** | **145** | **6** | 16% | 30% | 21% | **6%** | 34% | 41% | **7/41** |

`num` conta il riquadro nel capitolo; in tutti e dieci i booklet le schede
vanno in appendice (ADR-0105 §7), quindi **i numeri stampati nel capitolo sono
0 su 145**.

**Il caso della serata.** Nel capitolo VII (il barile) Zog'tar è citato 60
volte e Balvar 27: niente aspetto, ritratto, chi è, cosa vuole. La sua scheda
d'entrata, completa e col ritratto, c'è, ma nel capitolo IV (Scena 7), e il
capitolo VII non ha la mappa (M7-C e M7-H stanno nell'Appendice D del
capitolo IV). Lo script lo vede da solo, senza saperlo prima.

**Dove siamo forti.** Le schede d'entrata di ARC-07 (Durin, Zog'tar, Balvar,
Thorek, Thorgrim, Zeth, Vatore, Skullcrusher) hanno quasi tutto: le 6 coppie
complete sono Zog'tar e Balvar nel DEF-4, in tre booklet. Il Drappo ha una
**tabella del cast** con Ruolo e Vuole per ogni PNG, che è la lista avversari
dell'Alexandrian; sta però nella cassetta, non nel capitolo dove si incontra.

**Dove siamo deboli.**
1. **Chi è**: 6%. La scheda d'entrata non ha la riga; c'è solo l'epiteto nel
   titolo («il generale»). Il DM l'ha chiesta per nome.
2. **Mappa**: 7 capitoli su 41. Le mappe stanno in appendici di altri capitoli.
3. **Numeri**: tutti in appendice. È la D5 del 29 ottobre, che il DM ha pagato
   al tavolo.
4. **Stand alone e Palio**: descrivono le persone in prosa («Karkator, un
   aboleth che…, vuole quello che vuole ogni aboleth») e non in voci da
   trovare a colpo d'occhio. È esattamente il difetto che l'Alexandrian
   descrive.

**Limiti della misura, dichiarati.** Conta le voci con un'etichetta
(**Aspetto**, **Vuole**…): una descrizione buona scritta in prosa non conta, ed
è voluto, perché il criterio è trovarla al volo. Una persona citata tre volte
in un capitolo dove non si incontra conta lo stesso: per questo è un
indicatore e non ancora un cancello. Le divinità e i dossier di gruppo sono
esclusi da una lista scritta nello script. La qualità (una descrizione che si
capisce) la giudica solo la lettura da DM.

---

## 4. Implementazione — dove e come migliorare

| Leva | Che cosa | Stato |
|---|---|---|
| **ADR** | [ADR-0107](adr/ADR-0107-chi-si-incontra-sta-nel-capitolo.md): chi si incontra sta nel capitolo, con i sei elementi; la mappa dello scontro nel capitolo; la scheda d'entrata ha la riga **Chi è**; emenda ADR-0105 §7 | proposta, in questa PR; nel capitolo e in appendice |
| **Tool** | `scripts/misura_standard_tavolo.py` (questa PR), indicatore; quando il primo booklet è convertito diventa un cricchetto in CI come `misura_statblocchi_booklet` (tetti che scendono) | fatto (indicatore) |
| **Tool** | il generatore Typst (`export_booklet_typst.py`) mette nel capitolo la scheda d'entrata, il ritratto e il riquadro della persona anche quando il capitolo viene da un altro master (un'ancora `#persona(Nome)` accanto a `#scheda` di `componenti.py`, che prende chi è, aspetto, vuole dal dossier di ADR-0091); l'appendice con i riquadri resta com'è, per tutte le creature (il DM, 2026-11-03: *«voglio che aggiungi anche l'appendice con le schede perché erano fatte bene»*) | da fare, dopo il sì all'ADR |
| **Tool** | la mappa nel capitolo: un campo `mappe` nel capitolo del manifest, che ripete la pianta di stampa (ADR-0106) dove si gioca | da fare |
| **Tool** | «quante voltate di pagina»: dal PDF, la distanza in pagine fra l'inizio di una scena e la scheda, il ritratto e la mappa di chi ci combatte. Misura quello che il DM ha sentito al tavolo, sul PDF e non sul sorgente | da fare, seconda fase |
| **Skill** | `rumblingstone-module-standard`: la riga **Chi è** nella scheda d'entrata e il controllo «capitolo per capitolo»; `rumblingstone-playtest`: una rubrica di **lettura da DM con il PDF** nell'ordine della serata (per ogni scontro: mappa, scheda, ritratto, tattica entro una voltata di pagina), con l'elenco di cosa si è letto nel messaggio di consegna | da fare, dopo il sì all'ADR |
| **Contenuto** | aggiungere **Chi è** alle schede d'entrata (ARC-07 prima), e convertire in voci le persone di Palio, Giardino, Drappo e Abbazia (Karkator, Tariq, Sonjak, Vidalia, Madre Ilaria…) | da fare, un booklet alla volta |
| **Plugin** | nessuno. Le misure stanno in script del repo, la lettura del PDF si fa con gli strumenti già nel container. Un plugin aggiungerebbe una dipendenza senza misurare niente di più | scelta: no |

L'ordine consigliato: prima il booklet della prossima serata (lo sta già
rifacendo il thread di *Notte e Alba*, PR #305, e può usare questo script per
misurarsi), poi il generatore, poi gli altri booklet uno alla volta.

---

## 5. Validazione — come sapremo che è migliorato

1. **Misura**: `misura_standard_tavolo.py` su ogni booklet toccato. Criterio:
   le coppie complete salgono e nessuna colonna scende; la colonna `mappa`
   arriva a tutti i capitoli con uno scontro. Prima/dopo nel messaggio della
   PR.
2. **Lettura da DM con il PDF**, nell'ordine della serata: per ogni scontro,
   mappa, scheda, ritratto e tattica entro una voltata di pagina. Si consegna
   con l'elenco di cosa si è letto davvero (memoria `booklet-letto-da-dm`).
3. **Il tavolo**: dopo la serata, il DM dice se ha dovuto cercare qualcosa.
   È l'unico giudizio che conta; la misura serve a non regredire.
4. **Non regressione della stampa**: `misura_stampa.py --tutti --check` e
   `misura_statblocchi_booklet.py --check` restano nei tetti. Se le pagine in
   più fanno salire un tetto, lo si dice e lo decide il DM.

---

## Fonti

- J. Alexander, *Universal NPC Roleplaying Template*, 2015 — https://thealexandrian.net/wordpress/37916/roleplaying-games/universal-npc-roleplaying-template
- J. Alexander, *The Art of the Key* (parti 1-4), 2014-2016 — https://thealexandrian.net/wordpress/35180/roleplaying-games/the-art-of-the-key
- J. Alexander, *Don't Prep Plots* — https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots
- M. Shea, *Your Criteria for Selecting Great Published Adventures*, 2025 — https://slyflourish.com/great_adventure_criteria.html
- M. Shea, *The Eight Steps of the Lazy DM*, 2023 — https://slyflourish.com/eight_steps_2023.html
- B. Lynch, *Review Standards* — https://tenfootpole.org/ironspike/?page_id=1201 ; *My Favorite…* — https://tenfootpole.org/ironspike/?page_id=844
- B. Milton, *«Control Panel» Page Layout in the OSR*, 2018 — https://questingblog.com/control-panel-book-layout-osr/
- Dungeon n. 116, *30 Greatest D&D Adventures*, 2004 — elenco in https://shopontheborderlands.co.uk/2014/08/dungeon-magazines-30-greatest-dd-adventures-time/
- *Module Retrospective: Red Hand of Doom*, 2010 — https://nitessine.wordpress.com/2010/08/29/module-retrospective-red-hand-of-doom/
- *The (New) 3.5 Red Hand of Doom Handbook for DMs*, GiantITP — https://forums.giantitp.com/showthread.php?645018
- RPGnet, *[Pathfinder] Which Adventure Paths are good…* — https://forum.rpg.net/index.php?threads/pathfinder-which-adventure-paths-are-good-which-are-awesome-which-stink.704807/
- EN World, *Why "Curse of Strahd" Is Great* — https://www.enworld.org/threads/why-curse-of-strahd-is-great-spoilers.671586/
- Il confronto con *Burnt Offerings* del 2026-10-29: `/mnt/project-files/standard-stampa/CONFRONTO-PAIZO-AP-2026-10-29.md` (fuori repo)
