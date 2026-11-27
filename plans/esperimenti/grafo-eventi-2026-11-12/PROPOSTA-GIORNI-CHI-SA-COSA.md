# Proposta: il giorno di gioco su ogni riga di «chi sa cosa» (state §4)

Forma: riferimento, da confermare. Data: 2026-11-12. Scelta del DM: «Sì, li
propongo e confermi tu» (card del 2026-11-12).

**Cosa ti chiedo.** Per ogni riga conferma il giorno, oppure scrivi quello giusto.
Basta rispondere «ok tutte», oppure elencare solo le righe da cambiare (per
esempio «16: Day 25; 23: vedi sotto»). Fra le domande in fondo ce ne sono quattro
che non posso decidere io.

**Cosa entrerà in state.yaml dopo la tua conferma.** Due campi nuovi e facoltativi
per ogni riga di `conoscenze`:
- `dal_giorno`: il giorno del March Clock da cui il PNG lo sa. 0 vuol dire prima del Day 1.
- `informato_da`: il `png_id` di chi glielo ha detto. Serve solo se l'ha saputo da un altro PNG.

`validate_state` controllerà che `informato_da` esista nell'anagrafica.
`coerenza_campagna --state` avrà due regole in più:
- **T1**: un PNG mostra di sapere una cosa in una scena che finisce prima del suo giorno.
- **T2**: chi informa deve saperlo prima.

**Da dove vengono i giorni.** Le date dei capitoli di ARC-07 e ARC-08 sono
quelle approvate: ARC07-00-INDICE §Cronologia (2026-07-03) e
ARC08-12-CRONOLOGIA-MARCH-CLOCK. In particolare la **Cerimonia delle 100 Asce è
al Day 21**, ed è lì che Re Thorek nomina i Custodi Eterni. Tutto il resto è
dedotto, e la colonna «fiducia» lo dice.

| # | PNG | sa che (in breve) | dal giorno | da dove viene il giorno | informato da | fiducia |
|---:|---|---|---:|---|---|---|
| 0 | Sonjak | il gruppo ha liberato i Guerrieri di Cristallo (non sa delle 3 gemme) | 0 | scout drow all'assalto della miniera, arco 01 | — | alta |
| 1 | Ghaurush | i Custodi Eterni portano artefatti divini, non sa quali | 22 | il titolo nasce il Day 21; un giorno per i rapporti dell'avanguardia | — | media |
| 2 | Zin'thara | i Custodi hanno liberato i Guerrieri di Cristallo; nulla della Corona | 22 | usa il titolo, quindi dopo il Day 21; rete drow | — | media |
| 3 | Ushgar | i Custodi viaggiano con artefatti, non sa quali | 22 | voci di caserma, dopo il Day 21 | — | media |
| 4 | Sonjak | Sal opera sulla strada del deserto; non sa chi sia davvero | 23 | Sal parte dopo il briefing del Collezionista (riga 16) | — | bassa |
| 5 | Ghostlord | non sa che il gruppo esiste; sa che la Mano Rossa usa la sua tana | 0 | la tana serve l'orda da prima della marcia | — | bassa |
| 6 | Conte Valerius | il gruppo è stato a Hammerfist; non sa della Corona né di Sal | 23 | dispacci pubblici: due giorni dalla fine della battaglia (Day 21) alla capitale | — | media |
| 7 | Azarr Kul | il gruppo sono i Custodi Eterni; non sa i dettagli degli artefatti | 22 | scout della Mano Rossa, dopo il Day 21 | — | media |
| 8 | Xal'thor | Tordek porta i Bracieri Gemelli | 19 | i Bracieri escono dalla Forgia in ARC-07 (Day 14-19); osservazione planare | — | bassa |
| 9 | Zalkatar | l'Orbe di Dauth emette un Seme di Porta | — | dal giorno di Sethrax, lo stesso giorno (dispaccio telepatico quotidiano) | sethrax | alta |
| 10 | Sethrax | Tordek è il monaco legato all'Orbe; non sa del piano di Xal'thor | 26 | «Day 1-2 del Torneo»; il Torneo si apre al Day 25 (finestra P2B 25-34) | — | media |
| 11 | Varis | alcune statue potrebbero essere vive | 0 | «tre mesi fa» | — | alta |
| 12 | Il Collezionista | Artemis porta l'Anello del Caos | 0 | visto nella tana del minotauro, prima della marcia | — | alta |
| 13 | Il Collezionista | Therysol è vivo e gli dà la caccia | 0 | agenti spariti nel Sottosuolo | — | bassa |
| 14 | Re Thorek | il gruppo sono i Custodi Eterni, li ha nominati lui | 21 | la Cerimonia (ARC08-12) | — | alta |
| 15 | Varis | Artemis compra reliquie del Sottosuolo | 0 | tre transazioni finora | — | media |
| 16 | Salvatore | il gruppo sono i Custodi, con nomi, capacità e rotte degli artefatti | 23 | briefing del Collezionista prima della partenza | il-collezionista | media |
| 17 | Conte Valerius | il gruppo è stato a Hammerfist; non sa ancora della Corona | 23 | **doppione della riga 6** | — | — |
| 18 | Cerchio Sacro | Hella sta arrivando per il rituale | 22 | lettera di Hella «di due giorni fa»: Hella parte dopo la Cerimonia | — | media |
| 19 | Lythiel | Hella è la druida a cui Saraah ha promesso la Ghianda | 19 | riconoscimento in battaglia, Sessione 4 = Day 19 | — | alta |
| 20 | Tempestas | il gruppo sono i Custodi; porta la lettera di Brenna il Day 21; sa della torre per voci drow | 21 | è alla Cerimonia (HOOKS-Thorik r.7); la consegna è al Day 21 o 22, vedi D1 | — | media |
| 21 | Maewen | Aeleth è morto (lo scopre all'arrivo); Tordek somiglia al quarto invitato | 24 | arriva alla Foresta Sacra il Day 24 | — | alta |
| 22 | Lathander + Mask | il rifiuto di Artemis a Belkram, l'Anello, Zalkatar | 0 | consapevolezza divina (la visione arriva la notte 22-23) | — | alta |
| 23 | Brenna Sorvane | Hammerfist ha vinto; i Custodi includono Thorik; Halveth è corrotto; Lorana è viva a Rethmar | **?** | vedi la domanda D1 | tempestas (solo per Hammerfist) | — |
| 24 | Therysol | la gilda del Collezionista ha una cella a Dauth | 0 | agente catturato e interrogato | — | bassa |
| 25 | Norro Wiston | il gruppo sono i Custodi; Thorik è morto e risorto al Guado | 0 / **?** | Guado: arco 00. Il titolo: vedi la domanda D3 | — | — |
| 26 | Sertieren | il suo *inviare* è bloccato da un rituale | 14 | tentativi falliti Day 14-18 | — | alta |
| 27 | Lirien | riconosce la mano del Maestro nelle statue | 0 | apprendistato | — | alta |
| 28 | Mira Serani | ha già incontrato il gruppo; frammenti di artefatti e rotte; non sa che Lorana è viva | 12 | spia dal Traghetto di Drellin (Day 12-13) | — | alta |
| 29 | Lorana | crede che Mira sia morta; non sa dell'aranea | 0 | lutto e spilla | — | alta |
| 30 | Tiri Kitor | niente, primo contatto a Starsong Hill | — | non sanno nulla: niente giorno | — | — |

## Quattro domande che solo tu puoi chiudere

**D1. La lettera di Brenna e il titolo (riga 23 contro le righe 14 e 20).**
Brenna scrive che «i Custodi Eterni includono Thorik», e Tempestas consegna la
lettera **il Day 21**. Ma il titolo nasce alla Cerimonia **del Day 21**, a
Hammerfist, e Brenna è a Rethmar. Come può già saperlo? Le strade possibili:
- (a) la lettera non usa il titolo, e la correggo;
- (b) la consegna slitta a dopo il Day 21, e cambio la riga 20;
- (c) «Custodi Eterni» circolava già prima della Cerimonia, e allora l'origine del titolo è un'altra.

È la regola temporale che lo trova sui dati, senza leggere la prosa. Leggendo
poi `Arco-Post-Hammerfist-HOOKS-Thorik-RethmarLetter.md` si vedono altre due cose:
- r.7 dice che la consegna avviene il **Day 21**, mentre r.32 la mette al **Giorno 22**, prima della cena;
- r.28 dice che a Rethmar «gli uccelli messaggeri sono arrivati il Giorno 19», cioè lo stesso giorno in cui la battaglia finisce.

Propongo questo:
- Brenna sa della vittoria dal Day 19 (uccelli);
- la consegna è al Day 22;
- la lettera parla di Thorik come comandante, non di «Custodi Eterni».

Questa è la strada (a) più la correzione della riga 20, ma la scelta resta tua.

**D2. Il Collezionista e il briefing di Salvatore (riga 16 contro la 12).**
Salvatore sa nomi, capacità e rotte degli artefatti «dal Collezionista», ma §4
dice che il Collezionista sa solo dell'Anello di Artemis. Le strade possibili:
- (a) aggiungo una riga «il Collezionista sa dei Custodi e dei loro artefatti», con il giorno e la fonte (per esempio la rete di Sonjak o Mira);
- (b) Salvatore ne sa meno di quanto dice la riga 16.

**D3. Norro Wiston e il titolo (riga 25).** Norro è a Rethmar dal Day 16-18,
mentre la Cerimonia è al Day 21 a Hammerfist. Come lo sa?
- (a) per notizia, e allora dal Day 23 circa;
- (b) la riga non deve dire «Custodi Eterni».

**D4. Brenna e Lorana (riga 23).** Brenna sa che Lorana è viva «dai rapporti di
Tempestas», ma Brenna e Lorana sono tutte e due a Rethmar. Propongo che lo sappia
**direttamente**, dal Day 16-18, e che Tempestas resti la fonte solo per
Hammerfist. Così sparisce anche la catena rotta Tempestas → Brenna.

## Da sistemare comunque

- **Righe 6 e 17**: sono la stessa riga, con due formulazioni. Propongo di tenerne una sola.
- **`ARC07-DEF-1-PIANO-TERRA-TERROS.md:69`**: «I Custodi Eterni sono entrati nel Portale» sta in ARC-07 (Day 14-19), prima del titolo. Le possibilità sono due:
  - è una scorciatoia del DM, e allora la riga resta;
  - è un anacronismo, e allora diventa «I Rumbling Stones».
