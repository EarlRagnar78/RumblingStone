# Lettura finale di ARC-07: le correzioni

Correzioni ai rilievi di `DEVELOPER.md`, `PLAYTESTER.md` e `DM.md` di questa
cartella, fatte il 2026-10-19 prima della stampa. Una riga per rilievo:
corretto come, lasciato e perché, o mandato al DM. Le decisioni della sezione
«Esito» di `../DECISIONI-DM.md` non sono state riaperte; le domande nuove sono
lì in fondo, dalla 28 alla 33.

File toccati: `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` e il suo apparato
(rigenerato con `componenti.py --apparato`), in `homebrew/sessione-notte-e-alba/`
l'intro, la regia, il capitolo del Seme e il ✉ del contratto, il ✉ delle
boccette in `homebrew/volume-mille-anni/`, la scheda di Durik in
`homebrew/sessione-resurrezione-mille-anni/`, la sorgente di M7-B in
`Mappe/ARC07-MAPPE-DEFINITIVO.md` con i due SVG rifatti da `render_map_svg.py`,
il JSON di M7-C con il suo `.md` ricompilato da `compile_map_json.py`. DEF-5 e
il Bestiario non avevano rilievi in questo giro. Le fonti in rete sono in
`../VERIFICHE-SRD.md`, sezione «Lettura finale».

## Developer

| Rilievo | Esito |
|---|---|
| O1 · §0-bis senza wyvern, *Ghermire* e *Fluttuare*, Catena, Bane | corretto: quattro righe nel riquadro (wyvern dal round 2, i due talenti con la quota di 15 m, la Catena a CA 41, il Bane che tace e la *Dragondoom* che vale) |
| O2 · *Ghermire* con un PG Medio | corretto: una regola sola, la presa migliorata dell'SRD. Ogni prova di lotta vinta con la sola bocca (+20) fa 2d8+10; il danno automatico di *Ghermire* vale da tre taglie in giù e il PG Medio ne è a due. Testo SRD riletto in rete |
| O3 · «Colpo Possente» e il pieno | corretto: «Attacco Poderoso» in tutta la Scena 8 e su M7-C; il pieno è −15/+30 come A.2 (BAB +15, a due mani il doppio, mirror `combat.md`) |
| Y1 · soffio con la preda in bocca | corretto: «se il soffio è tornato» nella sequenza e nella regia §4 |
| Y2 · la nube nel round inchiodato | corretto: a terra non fluttua e la nube non c'è; viene dopo, quando si ritira |
| Y3 · chi morde in picchiata | corretto: il bersaglio di «Chi sceglie» |
| Y4 · *corrompere l'acqua* | corretto in A.1: al primo turno libero dal soffio |
| Y5 · Durik, danno massiccio e richiamo | corretto: riga 4-bis, regia §1 e scheda di Durik (cap. VI) dicono la stessa cosa: Tempra CD 15 o torna polvere, e la carica rimasta dopo i Treant dell'alba lo riporta per un'ora |
| Y6 · chi attiva la runa su Durik | corretto con proposta marcata: chi la porta, a contatto come l'SRD vuole *resistere all'energia*. Al DM, n. 30 |
| Y7 · il totale PX | corretto: ~7.775/PG con le wyvern |
| Y8 · danno massiccio «della casa» | corretto: regola SRD, tenuta attiva da `campaign/lore/house-rules.md`, che non aggiunge altro |
| Y9 · «regia veloce» | corretto: il §0 della regia dice «il duello in tre scambi, Appendice C.3, al posto della Scena 11» |
| Y10 · «Quattro cose» | corretto: «Cinque cose» |
| Y11 · tutti sulla riga 16 | corretto: nota sotto M7-B nel master e nella sorgente della mappa, posizioni da sfalsare su due righe |
| Y12 · l'Ancoraggio della Montagna | corretto nel modulo: regia §1 (riga Tordek) e Scena 11 «Chi non vola» dicono che è il Dono passato a Hella. Il ramo di gruppo non è toccato: vedi in fondo |
| Y13 · giavellotti delle guardie | al DM, n. 33: le caratteristiche delle guardie non sono scritte e non c'è una fonte per cambiare il numero |
| Y14 · velocità di Zog'tar | al DM, n. 33: manca la velocità base del mezzo-ogre |

## Playtester

| Rilievo | Esito |
|---|---|
| 1 · il PDF del DM è vecchio | lasciato: i PDF li rigenera il DM dai sorgenti corretti |
| 2 · Durik dopo i Treant, e la durata | corretto: Scena 5, Scena 6, cap. VI e stato H di M7-C. Richiamato dal seme resta (D74); distrutto, torna per un'ora (scheda della Collana in `DEF-3` §7); i due Treant dell'alba non spengono l'Evocazione (D65) |
| 3 · Tordek che tocca il Seme a ≈372 DR | corretto nel cappello del capitolo II: vale il paragrafo «A ≈372 DR», nessuna voce; a pelle nuda firma e il resto si accende nel 1372. Il testo incluso da `DEF-1` non è toccato |
| 4 · chi legge le pergamene | corretto: verificato sulla lista SRD del druido. Hella legge cure gravi e critiche e *neutralizza veleno* senza tiro; *ristorare* resta ad Artemis |
| 5 · «Lo derubano» senza gradi | corretto con proposta marcata: senza gradi l'SRD non passa CD 10; il fagotto si strappa di mano e il Cronolito porta via Vatore. Al DM, n. 29. La scheda di Tordek al 12° non ha gradi; le altre schede non sono nel repo |
| 6 · le bombe di Kettra dentro la marca | corretto: la regola del lancio è fuori dalla marca |
| 7 · punteggiatura orfana | corretto in DEF-4 (23 marche spostate in fondo alla riga prima, più le frasi spezzate di Scena 7, Scena 9, A.1, A.5 e della Scena 8 sul *comando*). Ne resta una, «. Non c'è tiro» nel capitolo II: viene dal testo incluso da `DEF-1`, fuori da questo giro |
| 8 · «Quattro cose» | corretto, come Y10 |
| 9 · il contratto nelle tabelle di consegna | corretto: intro (tutte e due le tabelle) e regia §0, Atto I |
| 10 · «in privato» e «per tutto il tavolo» | corretto nel sorgente: le due pagine dicono solo «Per tutto il tavolo». Il PDF dei giocatori, fatto da typst, non stampa il riquadro «in privato»; lo stampa ancora il `.hb.md` di Homebrewery, perché il testo è fisso in `HB_TAGS` di `build_booklet_html.py`, che non ho toccato |
| 11 · la benedizione dei chierici | corretto: riga nella regia §1, +2/+2 morale per 12 ore dal consiglio con la fiducia piena (Scena 4), Via A gratis, non vale sui TS |
| 12 · la cassetta dà per giocato il gesto dell'ascia | lasciato: `ARC07-CASSETTA-DEL-DM.md` è fuori dai file di questo giro. La regia fa chiedere al giocatore, e vince la regia |
| 13 · il re sulla riga dei PG | corretto: L17 sulla griglia del master e della sorgente, SVG rifatti nei due temi |
| 14 · due soglie per FERITO GRAVE | corretto: una riga nella Scena 7 dice che la Catena accorcia la strada (D14) |
| 15 · il totale PX | corretto, come Y7 |
| 16 · CD dell'acido aderente | al DM, n. 32 |
| 17 · Hella in aquila e la soglia | corretto con proposta marcata: la forma alternativa dell'SRD conserva tipo e sottotipo, quindi la runa scatta. Al DM, n. 31 |
| 18 · il dono a metà | corretto: la regia §1 chiede al DM di fissarlo prima di cominciare |
| 19 · lo Smeraldo della Corona | corretto: la regia §1 dice di chiederlo al giocatore, e perché il passaggio non lo ricarica |
| 20 · decisioni 19 e 20 non nel testo | corretto: le due righe sono nella regia §1, che dice anche che valgono sul testo copiato |

## DM a freddo

| Rilievo | Esito |
|---|---|
| 1 · il PDF «STAMPA» vecchio | lasciato, come il 1 del playtester |
| 2 · il contratto senza momento di consegna | corretto, come il 9 del playtester, e il cappello del capitolo II dice che prima del box la pagina resta nel volume |
| 3 · la benedizione dei chierici | corretto, come l'11 del playtester |
| 4 · i Treant fuori dalla lista da un'ora | corretto: tre minuti per la tabella dei Treant e la riga di A.6, tolti alla Scena 6 |
| 5 · punteggiatura orfana | corretto, come il 7 del playtester |
| 6 · chi legge le pergamene | corretto, come il 4 del playtester |
| 7 · «in privato» | corretto nel sorgente, come il 10 del playtester |
| 8 · Durik e la runa, l'ordine | corretto: la riga Durik della regia dice prima +50%, poi −20 |
| 9 · rimandi «§11» e «#4» | corretto nel cappello del capitolo II, che traduce i due rimandi; il testo incluso da `DEF-1` non è toccato |
| 10 · la trattenuta del pesatore | corretto con proposta marcata nella regia §2, passo 0. Al DM, n. 28 |
| 11 · «Quattro cose» | corretto, come Y10 |

## Conti

48 rilievi: 42 corretti (quattro con una proposta `[INFERRED]` e la sua
domanda al DM), 3 lasciati (i due PDF e la cassetta), 3 al DM (Y13 e Y14 in una
domanda sola, e la CD dell'acido).

## Cosa resta fuori, e il ramo

- **Il ramo di gruppo non è d'accordo con sé stesso.** `state-ramo-di-gruppo.md`
  dà a Tordek, nella riga dei Bracieri, «Ancoraggio della Montagna 2/day»;
  la riga di Tordek e quella dei Doni dicono che l'Ancoraggio è passato a
  Hella al rito, e il log della sessione 4 lo conferma. Il modulo segue il log.
  Il ramo va corretto dal DM.
- La riga «in privato» del `.hb.md` dei giocatori viene dal generatore.
- Una marca orfana e i due rimandi del capitolo II stanno nel testo che
  `componenti.py --includi` copia da `DEF-1`, che non era fra i file di
  questo giro.

## I controlli

`validate_modules`, `copertura_scene --check`, `domande_developer --check`,
`componenti --check` (dopo `--apparato`), `validate_bestiario`,
`validate_maps`, `validate_docs --sorgenti` e `decisioni_dm --check` passano.
`validate_docs` chiedeva un percorso relativo in `BRIEF.md` di questa
cartella, ed è corretto.

`ciclo_prosa.py confronta` contro `7e763f0f`, il commit da cui è partito il
giro: HEAD contiene già una parte di queste correzioni, salvate durante il
lavoro, e un confronto con HEAD non le vedrebbe. Nessun file ha segnalazioni
in più, perde dettagli sensoriali o impoverisce un box. Un solo ✗, sul `.md` di
M7-C: «numeri tolti 20 e 10». È la correzione di O3, da −10/+20 a −15/+30.
