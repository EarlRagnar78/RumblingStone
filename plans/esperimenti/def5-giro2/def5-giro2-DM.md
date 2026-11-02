# DEF-5, secondo giro · il DM a freddo

- **Bersaglio**: `07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md` (7 passaggi, letto tutto)
- **Rubrica**: `skills/rumblingstone-playtest/references/dm-a-freddo.md`, più «La lettura a scene» di `lettore-a-freddo.md`
- **Tempo dichiarato**: un'ora. Lettura a scene circa 37 minuti, le undici voci circa 20: totale circa 57 minuti, dentro l'ora ma senza margine. Nessuna voce è finita «oltre l'ora».
- **Corsa**: `plans/esperimenti/def5-giro2/corsa-dm/dm/` (diario in `diario.jsonl`)
- **Tavolo**: Thorik, Tordek, Hella, Artemis, 13° livello; stasera chiudono l'ARC-07 e tornano dal passato.

**Limiti della corsa**

1. La vista è arrivata in due tempi: il messaggio d'invio aveva un segnaposto, la vista vera è arrivata dopo con una correzione. Fra le due ho letto solo la rubrica, nessuna scena. Ho risposto alle quattro domande prima di aprire la prima scena.
2. I tempi del diario sono quelli stimati per un DM umano (circa 200 parole al minuto, più il tempo per prendere appunti). L'agente ci ha messo pochi minuti di orologio: il tempo dichiarato è una stima, non una misura.
3. La testata della vista mostra il percorso del master. L'ho usato solo per elencare i file vicini (le immagini); il master l'ho aperto solo con `lettura_a_scene.py`.
4. Per P-GRUPPO e P-STATO ho letto `state.md` e la sessione 4 dal ramo `origin/campaign-group-rumblingstone`; dei file citati dal master ho guardato solo le righe che servivano (`ARC08-01-GUIDA-DM.md` con grep sui nomi, le pagine degli artefatti, il Bestiario).
5. Non ho caricato la skill `rumblingstone-art-direction`: P-STILE è fatto solo sul confronto fra descrizioni.
6. Non ho letto gli altri rapporti di `def5-giro2/` (lettore, playtester, developer).
7. La sessione 4 si chiude alla Scena 5 di DEF-4. Stasera, prima di questo master, si gioca il resto di DEF-4: gli esiti da cui DEF-5 dipende (il duello, Vatore, il tono del Rubino, il torque) non esistono ancora. Ne tengo conto come dipendenze, non come buchi del repo.

## Primo passo · la vista di chi scorre

Risposte scritte alle 12:19, prima della prima scena.

1. **Cosa succede stasera.** Il Rubino sulla fronte di Thorik riporta i quattro dal −1000 al Cuore della Montagna, sotto Hammerfist, il Giorno 3 dell'assedio, mentre le porte di mithral cedono. La loro apparizione, una sfera dorata, ribalta la disfatta: circa trenta orchi tirano Volontà CD 25 e scappano. Una pulizia breve con uno o due orchi scossi, poi il passaggio all'ARC-08.
2. **Chi si oppone, e cosa vuole.** Gli orchi, circa trenta. Chi li guida e cosa vogliono: non lo so. La vista nomina solo il numero e il TS.
3. **Cosa preparo.** La mappa CM-1 (attenzione, scala 3 m), l'ultimo box di DEF-4 Scena 13, l'handout, le immagini dell'atlante C1, la musica, le schede di Re Thorek e di Madre Dana (la vista non dice dove sono). Degli statblocchi degli orchi la vista non dice niente.
4. **Cosa mi ha fatto rispondere.** Il primo paragrafo del Quickstart, le righe «In scena» delle tre scene, le CD 25 di Volontà «(~30 orchi)». I grassetti non mi hanno detto niente: «MASTER DEFINITIVO», «Sistema: D&D 3.5 SRD», «CD», «1,5 m/quadretto», «;» sono etichette d'apparato.

Esito: la serata si capisce dalla vista (nessun `D-SERATA`). Scattano `D-AVVERSARIO` (il capo degli orchi non c'è), `D-PREPARA` (la vista non dice cosa stampare né dove stanno gli statblocchi) e `D-RUMORE` (15 grassetti su 15 di servizio).

## Secondo passo · la preparazione a scene

### Il diario in breve

| Passaggio | ago | Cosa ho preparato | Chi parla per primo |
|---|---|---|---|
| 1 · premessa | +1 | stampa §0-bis e CM-1; appunti su Thorik (−4 DES, CA), Aura della Forgia ancora attiva, Tempra CD 15 | nessuno: la Scena 1 rimanda a DEF-4 Scena 13 |
| 2 · Scena 1 | +1 | DEF-4 Scena 13 tenuta aperta, poi il box del filo, poi quattro Tempra | io, col box «Il rosso vi allunga e vi stringe in un filo tirato attraverso mille anni» |
| 3 · §4 | 0 | niente | |
| 4 · Scena 2 | +1 | tre box in fila, ordine aura → sorpresa → iniziativa, distanze, tabella dei gesti, schede d'entrata | Dana dentro il box: «Sono tornati.»; poi Re Thorek: «Tu… portatore… degno. Finalmente… campioni veri.» |
| 5 · §5 | 0 | scelgo la modalità | |
| 6 · Scena 3 | +1 | combattimento completo; 5 hobgoblin (46 pf) e 2 orchi scossi su un foglio; il handoff in battute | io col box «Gli orchi scappano verso la porta»; nel finale Re Thorek: «Campioni di Moradin. Avete salvato il cuore di Hammerfist.» |
| 7 · coda | +1 | §6 aperta accanto alla Scena 3; handout da riempire; PX 3.300 a testa | Re Thorek, poi Dana sul portale |

### Le undici voci (D12)

| Voce | Esito | Cosa ho fatto, e cosa ho trovato |
|---|---|---|
| `P-RILIEVI` | fatto | ogni rilievo dell'uscita ha la sua risposta da tavolo nella colonna «Correzione minima», e per stasera la uso così com'è |
| `P-GRUPPO` | rilievo | dalla sessione 4: tre Doni dati tutti (Thorik il +2 di deflessione, Tordek l'Ancoraggio, Artemis 1d6 di Eldritch Blast), quindi la Senzienza arriva «sveglia» e dice «Tre volte hai pagato tu. La terza non te l'ho chiesta io.»; Thorik ha preso il **Debito della Radice** in un quarto ramo (E-07g), mentre §7 del master conosce solo «pegno al Sogno della Terra (A/B/C)»; nessuno ha dormito, quindi l'orologio in consegna è ≈ 3g 15h, che il master dà già come «il ramo del gruppo di oggi». I PG non sanno: l'orologio, Fauci, la parentela con Skullcrusher, che il re è discendente di Thorek I |
| `P-MONDO` | fatto | cosa si muove senza i PG: la colonna d'orchi dalle gallerie di Zeth, Fauci che devasta le mura, «ogni 10 minuti Fauci abbatte una torre della Porta Ovest» (§6), l'orda al giorno 19 del conto della marcia, il rituale di Azarr Kul a 9/18 (`state.md` §3). Nessuno nella caverna sa del viaggio |
| `P-STATO` | rilievo | PG a pieno, Aura della Forgia attiva, Thorik −4 DES / +2 COS / +4 CAR, immune alla paura, Mind Blank e RD 5/epico e male dalla Corona; Hella con Scudo del Custode, RD 3/adamantino, Rovo Eldritch; nello zaino 4 pergamene di *ristorare*, 5 pozioni di *volare*, 3 di *velocità*. Re Thorek a 8 pf ed esausto, Dana senza guarigioni. Restano aperti: l'esito del duello di DEF-4, Vatore, il tono del Rubino, il torque (si giocano stasera prima di DEF-5) e il totale PX del gruppo, che il repo non ha (la sessione 4 dice che il Fuoco ha «tre versioni che non coincidono») |
| `P-STILE` | fatto in parte | le descrizioni di Re Thorek («barba grigia intrecciata di fili d'oro, occhi azzurri») e di Dana («anziana anche per una nana», scintille dorate) coincidono con `ARC08-01-GUIDA-DM.md` righe 275 e 300. Senza la skill d'art direction non ho confrontato immagini e schede-personaggio |
| `P-IMMAGINI` | rilievo | le due immagini di §9 esistono, ma nessuna mostra quello che il master dice: `ilCuoreDiMoradin.png` è il Cuore di Moradin, l'artefatto (un cuore di rubino su un piedistallo), non la caverna; `PortaleDellaForgiaEterna.webp` è una schermata di testo con un canto in nanico, non l'apparizione. Mancano: Re Thorek sull'altare, Dana, la sfera tricolore che si apre, la Corona a tre gemme. In `Immagini/ritratti/` c'è solo `re-thorek-i.jpg`, l'antenato. Da generare: le quattro qui sopra (questa corsa non può) |
| `P-HANDOUT` | rilievo | «Lo Stato dei Custodi» è un testo dentro il master, non un file da stampare; le due righe vuote si riempiono solo dopo il duello di stasera. Le pagine giocatore degli artefatti ci sono (Corona `03_Corona_3_Gemme.html`, Bracieri `06_Bracieri_S3_Chiavi_della_Forgia.html`, Anello e Collana `…SCHEDA-GIOCATORE-STATO-ATTUALE.md`), ma fra i Bracieri ci sono anche «Completa Final» e «Completa copy 2»: si sceglie per nome dello stadio. La tavola dell'Affresco A8 non l'ho trovata come file |
| `P-FLUSSO` | fatto | Scena 1 → Scena 2 (sorpresa, un gesto a testa) → Scena 3 (pulizia, round 1-4) → handoff → PX e handout → portale → ARC-08. Le opzioni aperte: fast-play o completo, curare il re, murare la porta, inseguire, curarsi, saltare il handoff verso Fauci. Tutte hanno una riga in §6 |
| `P-DOMANDE` | rilievo | trovate: curare il re (§6), perché Dana non lo cura (fine Scena 3), riposare (§6), il viaggio (§6), chiudere la porta (§6). Senza risposta: cosa sa il capo degli orchi se lo interrogano; dove sono Borin, Dara, Thorin e Nala, che la mappa nomina per la regia lunga; se Re Thorek riconosce il torque del suo antenato al collo di Thorik |
| `P-CONGEGNI` | rilievo | l'aura (Volontà CD 25, uno su venti resta) e il round di sorpresa sono chiari e hanno i loro box. L'orologio «una torre ogni 10 minuti» sta solo in una cella di §6, senza box: se il tavolo si attarda non ho la frase per farglielo sentire |
| `P-INTERAZIONI` | rilievo | il master gestisce Corona (Aura di Comando, CD 15, 16,5 m, confermata dalla pagina `03_Corona_3_Gemme.html`), Collana e Treant. Non nomina lo Scudo del Custode di Hella con l'Eco (Thorik accelerato 3 round verso chi lei ha protetto), che in un round con cinque hobgoblin sul re scatta di sicuro. Aegis Fang «canta… (pagina dell'artefatto)», ma `00_Aegis_Fang-MASTER-DM.md` e la scheda giocatore non nominano né Fauci né il canto |
| `P-CONFINE` | rilievo | nella mia preparazione ho separato in ogni riga cosa sanno i PG. Sul master: §1 ha per titolo «cosa riportate a casa», alla seconda persona plurale come se si leggesse ai giocatori, e dentro ci sono cose solo del DM («nessuno al tavolo se n'è accorto», la sincronizzazione di Vatore in ARC-09) |

## Terzo passo · il giorno dopo, al tavolo

Risposte date dal solo diario (`python3 scripts/lettura_a_scene.py diario plans/esperimenti/def5-giro2/corsa-dm/dm`).

**Chi entra per primo in scena, e cosa dice?**
Il primo a parlare sono io, col box della Scena 1: «Il rosso vi allunga e vi stringe in un filo tirato attraverso mille anni». Il primo PNG è Dana, dentro il box delle porte: «Sono tornati.» Poi Re Thorek: «Tu… portatore… degno. Finalmente… campioni veri.» In Scena 3 il capo degli orchi urla in orchesco, ma il diario non ha la sua battuta (il master non gliene dà). Nel finale Re Thorek: «Campioni di Moradin. Avete salvato il cuore di Hammerfist. Ma la battaglia non è finita. SOPRA.» Il diario basta.

**Se i giocatori chiedono di curare Re Thorek, cosa rispondo e dove lo trovo?**
Dal diario: lo tiene giù l'esausto, non i pf; *ristorare inferiore* lo porta ad affaticato, *ristorare* o *guarigione* lo rimettono in piedi; ha 195 pf massimi; la sua *Presenza Regale* (+3) non si somma al +6 dell'apparizione. Sta in §6, non nella Scena 3 dove la domanda arriva. Il gruppo ha quattro pergamene di *ristorare*: la domanda arriverà al primo round. Se chiedono di chiudere la porta, il diario dice solo «ci torno per la porta»: il contenuto (il varco di 6 m si blocca solo con la magia) non è rimasto. È un rilievo sul master, perché la risposta sta in una cella lunga di §6 che non si ricorda.

**Dove ho dovuto tornare indietro, e quanto tempo ho perso?**
Quattro volte, tutte annotate nel diario come `D-SALTO` o `L-ORDINE`: gli hobgoblin nominati in Scena 2 e spiegati in Scena 3 e in fondo a CM-1; la cura del re, dalla Scena 3 a §6; PX e handout, che servono prima del portale e stanno in §8 e §9; l'inizio, che vive in DEF-4 Scena 13. A cui si aggiunge la Senzienza, che rimanda al rito di DEF-3. Stima: fra 30 secondi e un minuto ciascuna, al tavolo circa tre minuti.

Le sette domande del ricordo, in breve, dal solo diario: la serata è il ritorno, l'apparizione e la pulizia; l'avversario sono gli orchi con un capo che vuole uscire vivo e tenersi l'elmo, poi cinque hobgoblin che puntano il re; si parte dallo strappo fra le ere e si arriva al Cuore della Montagna, poi ai bastioni; se il −1000 è andato male l'apparizione è meno luminosa (+4, cinque orchi scossi, scontro di 3-4 round), mai un game-over; il momento più forte è l'apparizione, con i nani che rialzano la testa; finisce con Dana che apre il portale; ho riletto i cinque punti qui sopra.

## L'uscita

| # | Passo | Codice | Cosa manca | Gravità | Prova | Correzione minima |
|---|---|---|---|---|---|---|
| 1 | primo | `D-PREPARA` | la vista non mostra «Cosa stampare» né dove stanno gli statblocchi; gli statblocchi di Re Thorek e Dana sono in ARC-08 e non nell'elenco di stampa | 🟠 | vista: nessuna riga su statblocchi; master: «Cosa stampare. La Quick-Reference §0-bis […]; la mappa CM-1; l'handout», e «statistiche: `ARC08-01-GUIDA-DM`, PNG Alleati» | mettere «Cosa stampare» in grassetto nella prima riga del Quickstart e aggiungere `ARC08-01-GUIDA-DM` §PNG Alleati (Re Thorek, Dana) |
| 2 | secondo | `L-ORDINE` | gli hobgoblin e il muro di scudi compaiono nella tabella dei gesti della Scena 2 prima che il master dica chi sono, quanti e quando | 🟠 | Scena 2, riga di Thorik: «prima che entrino gli hobgoblin»; il numero arriva in Scena 3: «20 hobgoblin sergenti, alla fine del round 1» | una riga in testa alla Scena 2: «Alla fine del round 1 entrano 20 hobgoblin sergenti (Scena 3): l'aura non li tocca» |
| 3 | secondo | `L-ORDINE` | la cura di Re Thorek si decide in Scena 3, la regola (esausto, *ristorare*) sta solo in §6 | 🟠 | Scena 3: «Re Thorek si rialza e guida i suoi»; §6: «Lo tiene giù l'esausto, non i pf: ristorare inferiore lo porta ad affaticato»; il gruppo ha 4 pergamene di *ristorare* (sessione 4) | copiare in Scena 3 la frase sull'esausto e su *ristorare* |
| 4 | secondo | `P-IMMAGINI` | le due immagini di §9 non mostrano quello per cui sono elencate; mancano Re Thorek, Dana, la sfera, la Corona a tre gemme | 🟠 | §9: «Il Cuore della Montagna / l'altare · `ilCuoreDiMoradin.png`»: il file è l'artefatto; `PortaleDellaForgiaEterna.webp` è una schermata di testo | correggere le due righe di §9 e generare le quattro immagini mancanti |
| 5 | secondo | `P-STATO` | il master dipende da esiti di DEF-4 (duello, Vatore, tono del Rubino, torque) ma non li raccoglie: sono sparsi fra §0-bis, §6, §7, §9 | 🟠 | §6: «il duello di `DEF-4` è finito FUGGITO […] o VINTO SPORCO»; §9: «Il duello del −1000 è finito così: ______» | un riquadro in §0: «Prima di aprire, segna da DEF-4: esito del duello, ferite a Fauci, Vatore, tono del Rubino, torque consegnato» |
| 6 | primo | `D-AVVERSARIO` | chi guida gli orchi e cosa vuole non è nella vista; il capo compare dentro una riga della tabella dei gesti | 🟡 | Scena 2, riga di Artemis: «Il capo è l'orco più grosso, con un elmo nanico» | spostare il capo nella riga «In scena» della Scena 2 |
| 7 | primo | `D-RUMORE` | i grassetti della vista sono tutti etichette d'apparato | 🟡 | vista: «MASTER DEFINITIVO · Sistema: D&D 3.5 SRD · CD · 1,5 m/quadretto · ;» | togliere il grassetto dalle etichette e metterlo su porte, aura, re a 8 pf |
| 8 | secondo | `D-SALTO` | la Scena 1 si apre con un box che sta in un altro file | 🟡 | «l'accensione del Rubino e la voce di Moradin stanno là, nelle tre battute della Scena 13» | una riga con la prima battuta di DEF-4 Scena 13 |
| 9 | secondo | `D-RUMORE` | storia delle versioni nel corpo della scena; nella mappa, i round della regia lunga | 🟡 | Scena 1: «Il box di prima faceva accendere il Rubino sulle mura»; CM-1: «✨ SFERA DORATA (R8!)» | spostare la nota nel registro delle modifiche; segnare R8 come «solo regia lunga» |
| 10 | secondo | `D-TEMPO` | la durata della pulizia non torna fra le modalità e gli sviluppi | 🟡 | «in 2 round»; «gioca 2-3 round»; sviluppi «Round 1» e «Round 2-4» | scrivere «4 round, o 2 in fast-play» |
| 11 | secondo | `L-AMBIGUO` | §0-bis dice che Dana tiene giù il re, il Bestiario dice che lo guarisce al finale | 🟡 | §0-bis: «Dana lo tiene giù e lui obbedisce»; `Dana_Forgiapietra.md`: «guarisce Re Thorek al finale» | una nota: la cura di Dana è dell'ARC-08 |
| 12 | secondo | `L-RIFERIMENTO` | il canto di Aegis Fang rimanda a una pagina che non lo contiene | 🟡 | «canta, non parla […] (pagina dell'artefatto)»; `00_Aegis_Fang-MASTER-DM.md` non nomina Fauci | il percorso della pagina, o la regola scritta qui |
| 13 | secondo | `L-RIFERIMENTO` | le Cantitrici della Pietra non hanno una scheda | 🟡 | §6: «le Cantitrici della Pietra […] (Bestiario)»; nel Bestiario c'è solo una riga in `Dana_Forgiapietra.md` | dire «chierica di 5°, *cura ferite gravi*», o il file |
| 14 | secondo | `P-GRUPPO` | §7 conosce solo i rami A/B/C del Debito della Radice | 🟡 | §7: «pegno al Sogno della Terra (A/B/C)»; sessione 4: «Thorik ha detto che il prezzo lo paga lui […] un quarto ramo, fuori da A/B/C» | aggiungere E-07g alla riga |
| 15 | secondo | `P-INTERAZIONI` | lo Scudo del Custode di Hella e l'Eco su Thorik non sono nella Scena 3 | 🟡 | `state.md` §1: «ogni volta che Hella usa lo Scudo lui è accelerato 3 round verso chi lei ha protetto» | una riga nella riga di Hella della tabella dei gesti |
| 16 | secondo | `P-INTERAZIONI` | il torque di Thorek I, se consegnato alla Scena 12, non ha eco quando il discendente apre gli occhi | 🟡 | sessione 4: «Lo consegna lui, di persona, alla Scena 12»; scheda d'entrata: «Eco · la sua stirpe discende dal Re Thorek I» | una battuta di Re Thorek se vede il torque |
| 17 | secondo | `P-CONGEGNI` | l'orologio delle torri non ha box | 🟡 | §6: «ogni 10 minuti Fauci abbatte una torre della Porta Ovest» | due righe di read-aloud sul crollo, sopra |
| 18 | secondo | `P-DOMANDE` | dove sono Borin, Dara, Thorin e Nala nella regia breve | 🟡 | CM-1: «coi PNG giocabili Borin/Dara/Thorin/Nala» | una riga: nella regia breve sono fra i dieci capi, o non ci sono |
| 19 | secondo | `P-HANDOUT` | la copertina è dentro il master; la tavola A8 non è un file; fra le pagine dei Bracieri ci sono copie | 🟡 | §9: «questa copertina, con le righe da riempire al tavolo»; `05_Bracieri_Gemelli_Scheda_PG_Completa copy 2.html` | un file handout a parte e il nome esatto di ogni pagina |
| 20 | secondo | `P-STATO` | il totale PX del gruppo non c'è nel repo | 🟡 manca nel repo | §8: «i PG hanno i PX del 14° già all'arrivo»; sessione 4: il Fuoco ha «tre versioni che non coincidono» | il DM sceglie la versione del Fuoco e registra il totale |
| 21 | secondo | `P-CONFINE` | §1 ha la forma di un testo per i giocatori ma contiene cose solo del DM | 🟡 | titolo «cosa riportate a casa»; dentro: «nessuno al tavolo se n'è accorto» | titolo «per il DM: cosa riporta ciascuno» |

**Verdetto.** Un DM che non ha scritto il modulo lo conduce stasera con un'ora di preparazione, e la usa quasi tutta. Nessun 🔴: la serata si capisce dal Quickstart, i box ci sono e chiudono su «Che fate?», le schede d'entrata dicono chi parla e come. I cinque 🟠 sono ricerche al tavolo (hobgoblin, cura del re), due lavori che l'ora non copre (immagini sbagliate, esiti di DEF-4 da raccogliere) e un elenco di stampa incompleto.
