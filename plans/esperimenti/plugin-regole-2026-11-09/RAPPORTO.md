# Audit dei plugin di regole 3.5 e PF1e (2026-11-09)

Richiesta di Jfs: controllare che i plugin di regole per il d20 SRD 3.5 e per
PF1e siano davvero completi, funzionanti e usati, e correggerli misurando il
miglioramento.

`python3 scripts/sistemi.py` dice 16 capacità su 16 «dati» per tutti e due i
sistemi, quindi a guardare il cruscotto è tutto a posto. Il cruscotto però
controlla solo che una capacità sia **dichiarata**. Non controlla se la tabella
dietro è completa, né se i numeri sono quelli della fonte. Questo audit misura
proprio queste due cose.

## Metodo

- Fonti: SRD 3.5 `olimot/srd-v3.5-md@c7f30a0c` e PRD PF1e
  `devonjones/PSRD-Data@76ea4784`, le stesse in cache di `riscontro_srd.py`
  (`python3 scripts/riscontro_srd.py scarica`).
- Misura: [`misura_plugin_regole.py`](misura_plugin_regole.py). Per ogni
  tabella estrae la tabella vera dalla fonte (classi, prestigio, tipi,
  armature, scudi, griglie degli incantesimi al giorno e conosciuti, abilità,
  liste di classe degli incantesimi, PE) e la confronta riga per riga con il
  plugin. Per ogni tabella riporta le righe coperte, quelle giuste, quelle
  sbagliate (con i due valori), quelle non verificabili e i campi che mancano.
  Lavora solo in lettura, senza rete, ed è deterministica.
- Prima: [MISURA-PRIMA.md](MISURA-PRIMA.md) ([json](misura-prima.json)), main 04dbf0bd.
- Dopo: [MISURA-DOPO.md](MISURA-DOPO.md) ([json](misura-dopo.json)), questo ramo.
- Uso: `dmcore.sistemi.regole_diverse(sistema, strumento)` per ogni strumento
  del manifest, più una prova a mano sugli strumenti che hanno `--sistema`.

## La misura in una tabella

| Tabella (3.5) | Fonte | Prima: coperte / sbagliate | Dopo: coperte / sbagliate |
|---|---:|---|---|
| tipi | 15 | 15 / 1 (umanoide, vedi sotto) | 15 / 1 |
| classi base e PNG | 16 | 16 / 0 | 16 / 0 |
| classi di prestigio | 14 | **2** / 0 | **14** / 0 |
| armature | 12 | **9** / 0 | **12** / 0 |
| scudi | 4 | 4 / 0 | 4 / 0 |
| griglie incantesimi al giorno (classi) | 8 | 8 / **3** (ranger, paladino, adepto) | 8 / **0** (ranger, paladino e bardo misurati contro il PRD PF1e: card) |
| conosciuti dello stregone | 20 livelli | 20 / 0 | 20 / 0 |
| conosciuti del bardo | 20 livelli | 20 / **19** | 20 / **0** (contro il PRD PF1e: card) |
| abilità | 36 | **29** / 2 voci in più | **36** / 2 voci in più |
| liste d'incantesimi (classe × funzione) | 626 voci | 626 / **8** a livello sbagliato · 185 non verificabili | 626 / **0** · 185 non verificabili |
| soglie PE | 20 | 20 / 0 | 20 / 0 |

| Tabella (PF1e) | Fonte | Coperte |
|---|---:|---:|
| classi base, ibride e PNG | 26 | **0** |
| classi di prestigio | 18 | **0** |
| armature | 12 | **0** |
| griglie degli incantesimi | 13 classi | **0** |
| abilità | 26 | 26 |
| tipi e taglie | 13 + 9 | tutte (generate dal PRD, cancello in CI) |
| PE, tesoro, incontri | — | generati dal PRD con `estrai_prd_pf1e.py --check` (non rimisurati qui) |

In breve: il plugin 3.5 è quasi completo ma aveva numeri sbagliati in punti
precisi. Il plugin PF1e è corretto dove c'è, ma ha solo il 36% delle tabelle
misurate.

## Rilievi corretti in questa PR

1. **Griglia dell'adepto** (4 righe: 10°, 14°, 18° e 20°). Era diversa sia
   dall'SRD 3.5 sia dal PRD PF1e, che su queste righe coincidono. Esempio:
   l'adepto di 10° aveva 3/3/3/1, la Tabella dell'Adepto dice 3/3/2/1. Prima
   `genera_creatura` lo stampava come «tabella SRD di adepto».
2. **Otto incantesimi al livello sbagliato per la classe.** Ognuno è stato
   rimesso a un incantesimo dello stesso uso, al livello che la lista SRD della
   classe gli dà:
   - chierico: *cura ferite gravi* stava al 4° in due liste (è del 3°), al suo
     posto *cura ferite critiche*;
   - chierico: *manto del caos* (Atlante Planare, non SRD) sostituito da
     *mantello del caos*;
   - druido: *lama di fuoco* (Perfetto Arcanista) sostituita da *lama infuocata*;
   - druido: *rimuovi malattia* stava al 4° (è del 3°), sostituita da *cura
     ferite gravi*, che per il druido è del 4°;
   - druido: *guarigione di massa* al 9° non è nella lista del druido,
     sostituita da *cura ferite critiche di massa*;
   - bardo: *risata incontenibile* al 2° spostata al 1°.

   L'àncora `skills/dnd-35-srd/references/spells.md` aveva gli stessi errori e
   va corretta insieme: il test delle liste confronta i dati con l'àncora, non
   con l'SRD, e per questo non li vedeva.
3. **Tre armature SRD mancanti**: pelle (+3/4), corazza di bande (+6/1) e
   corazza a strisce (+6/0). Aggiunti anche i nomi italiani ufficiali del
   lessico che mancavano: *armatura completa* (42 occorrenze nel repo, prima non
   riconosciuta), *corazza di piastre* e *giaco di maglia*.
4. **Dodici classi di prestigio SRD mancanti**, con il nome italiano del
   lessico. Il Maestro del Sapere resta fuori perché nella fonte in cache non ha
   la tabella.
5. **Sette abilità SRD mancanti** dal controllo delle maiuscole di
   `validate_prosa`: Raggirare, Conoscenze, Intrattenere, Muoversi
   Silenziosamente, Parlare Linguaggi, Utilizzare Corde e Utilizzare Oggetti
   Magici. `validate_prosa --caratteristiche` resta verde su 591 file, quindi
   il controllo copre di più senza bocciare niente.
6. **`derive_statblocks` leggeva armature e scudi per pezzi di parola**, ed è
   il difetto con l'effetto più grosso. Prima prendeva il primo nome trovato
   nel testo, anche dentro un'altra parola:
   - «sh**ield**» dentro *Oaken**shield***, e «torre» nella Torre del conclave,
     davano uno scudo +4 a 11 creature che non ne hanno uno (costrutti, golem,
     Urialle, Zin'thara…);
   - «corazza» dentro *corazzati* dava una corazza a Gorthak, «maglia» dentro
     *guardamaglia* dava un giaco di maglia al Conte Valerius: due blocchi
     proposti «scrivibili» con una CA inventata (non erano stati scritti nelle
     schede);
   - «corazza di piastre» veniva letta come «piastre» (+8 invece di +5).

   Adesso cerca prima il nome più lungo, solo a parola intera, e «torre» da
   sola non conta più (resta *scudo torre*). Con *armatura completa*
   riconosciuta, Zog'tar diventa derivabile.

Banco d'invarianza: `impronta_creature.py --confronta` cambia solo nelle 14
creature dette sopra e nel nome «Assassin» → «Assassino» in 3 schede (stessi
numeri: il nome italiano ora è riconosciuto). `impronte.py --confronta`
(ADR-0111) cambia solo `derive_statblocks`. Le altre 11 impronte sono
identiche e le basi sono state riscritte. `conformita_statblocchi` dà gli
stessi numeri (119 statblocchi, 114 tornano, 4 uguali alla fonte), il cancello
dei moduli PF1e è verde e la suite intera passa (2.563, più il test di
validate_docs che fallisce solo in parallelo, già noto).

## Rilievi che chiedono una scelta del DM (card)

Il **livello d'incantatore** «livello − 3» di ranger e paladino è una scelta del
DM (card del 2026-11-09, #361) e non è un rilievo. I rilievi qui sotto
riguardano le **griglie degli slot**, che sono un'altra tabella.

7. **Ranger e paladino: la griglia degli incantesimi non è quella 3.5.** Il
   plugin dice «SRD 3.5», ma i numeri sono quasi tutti quelli della tabella PF1e
   del ranger. Esempio: ranger di 5° con 1 incantesimo di 1° (SRD: 0) e di 10°
   con 2/1/0 (SRD: 1/1). Al 20° non tornano con nessuna delle due fonti (plugin
   4/3/3/3, SRD 3/3/3/3, PF1e 4/4/3/3). In PF1e paladino e ranger hanno la
   stessa griglia, come nel 3.5. L'àncora della skill dnd-35-srd
   («Verified anchor rows») riporta gli stessi numeri del plugin, quindi il
   test era verde ma confrontava due copie dello stesso errore.
8. **Bardo: gli incantesimi conosciuti sono quelli PF1e, quelli al giorno sono
   3.5.** Il risultato è un bardo che non esiste in nessuno dei due manuali.
   Esempio: al 10° conosce 6/5/5/4/2 (PF1e), mentre l'SRD dice 6/4/4/4/2.

Proposta per tutti e due: scegliere una tabella intera, non metà e metà, e
scriverne la fonte. La consigliata è la tabella PF1e completa (ranger, paladino
e bardo, anche per gli incantesimi al giorno), segnata come divergenza
dall'SRD. Il motivo è la stessa regola che ha deciso il livello d'incantatore
del ranger «−3» (card del 2026-11-09): la versione più forte, purché
ricostruibile da una scheda legale. L'alternativa è tornare alle tabelle SRD
3.5, più deboli ma coerenti con il nome del plugin.

**Esito della card (Jfs, 2026-11-09): «Tabelle PF1e intere, segnate».** Nel
plugin 3.5 ora:

- ranger e paladino hanno la griglia PF1e intera (20°: 4/4/3/3), con il
  livello d'incantatore −3 che resta e la caratteristica che resta Saggezza;
- il bardo ha la griglia PF1e al giorno, con i trucchetti a volontà (lo 0 non
  è uno slot, `genera_creatura` scrive «trucchetti a volontà»), e i conosciuti
  PF1e.

Ogni griglia ha nel file la fonte e «⚠ Non SRD 3.5», e le classi sono elencate
in `incantatori_regole.griglia_pf1e`. Il conto di `genera_creatura` dice
«tabella PF1e (scelta del DM, non SRD 3.5)». La misura confronta queste tre
classi con il PRD, non con l'SRD, e lo scrive nel nome della tabella: 8/8
griglie e 20/20 conosciuti giusti. Le àncore di `dnd-35-srd/references/classes.md`
sono riscritte con i numeri PF1e e l'etichetta «not SRD 3.5».

Dopo la card il 3.5 è a 605 righe giuste su 606 verificabili. L'unica che
resta è il TS dell'umanoide, una scelta ancora da scrivere.

## Rilievi aperti, lavoro successivo (non in questa PR)

9. **PF1e senza classi, armature e griglie.** `genera_creatura --sistema pf1e`
   rifiuta i livelli di classe («non ancora supportati»), e `derive_statblocks`,
   `genera_attributi`, `impronta_creature` e `conformita_statblocchi` saltano
   le schede PF1e oppure fanno solo una parte dei conti (BMC, scurovisione PF1e
   e corrompere l'acqua mancano, come già scritto in `conformita.toml`). La
   correzione è estendere `estrai_prd_pf1e.py` perché generi dal PRD le 26
   classi (DV, BAB, TS, gradi), le 18 classi di prestigio, le armature (in PF1e
   la corazza è +6 e l'armatura completa +9) e le 13 griglie, con lo stesso
   `--check` in CI, e poi far leggere quei dati a chi costruisce le creature.
   Va fatto dopo #363 e #364, che toccano gli stessi file di conformità.
10. **185 incantesimi delle liste (30%) hanno un nome italiano che non è quello
    del lessico ufficiale.** Esempi: *spruzzo di colori* invece di *Spruzzo
    colorato*, *grasso* invece di *Unto*. Non si può quindi verificare che
    siano della classe e del livello giusti. Va allineato con il lessico
    (ADR-0110) e rimisurato con questo stesso script.
11. **«scaglie» è una voce di armatura** (scale mail). Nel testo di un drago o
    di una creatura con le scaglie può dare un'armatura che non c'è. Non è
    cambiato niente in questa PR (nessuna impronta lo mostra), ma la parola è a
    rischio.
12. **Campi 3.5 non presenti**: i gradi di abilità per DV e per livello non
    sono nel plugin 3.5. Oggi nessuno strumento 3.5 li usa, quindi non è un
    difetto. Lo diventa se un generatore 3.5 dovesse contare le abilità.
13. **Umanoide 3.5**: il plugin gli dà Tempra come TS buono fisso, la fonte
    dice «uno a scelta». È una scelta legittima, ma non è scritta. Il plugin
    PF1e lo modella come `ts_a_scelta = 1`.

## Uso: chi legge davvero il plugin

| Strumento | Con un file PF1e |
|---|---|
| update_xp, suggest_encounter, suggest_loot | usano i dati PF1e (`--sistema pf1e`) ✅ |
| genera_creatura | converte i DV razziali in PF1e; rifiuta i livelli di classe ⚠ |
| conformita_statblocchi | cancello dei moduli PF1e con 6 conti su 9 (lotta, scurovisione e corrompere l'acqua saltati) ⚠ |
| derive_statblocks, genera_attributi, impronta_creature | saltano le schede PF1e e lo dicono (`regole_diverse`) ⚠ |
| validate_prosa, domande_developer, coerenza_campagna, lessico_regole | usano il lessico PF1e ✅ |
| build_booklet_html, export_booklet_typst, validate_* di struttura | dati d20 comuni ✅ |

Il cruscotto `sistemi.py` dà tutti ✅ anche per le righe ⚠, perché misura la
dichiarazione e non la copertura. Una proposta per dopo: far leggere a
`sistemi.py` la copertura misurata da questo script, così il cruscotto smette
di sembrare più verde di quanto è.

## Riprodurre

    python3 scripts/riscontro_srd.py scarica
    python3 plans/esperimenti/plugin-regole-2026-11-09/misura_plugin_regole.py
    python3 scripts/impronta_creature.py --confronta
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/impronte.py --confronta

## Lotto PF1e (dopo la #365)

Il DM ha chiesto di completare il PF1e e di chiuderne tutti i limiti. Il lavoro
è diviso in due.
- **Thread della #363:** i dati, generati dal PRD con `estrai_prd_pf1e.py`:
  - `sistemi/pf1e/dati/classi.toml`;
  - `liste_incantesimi.toml`;
  - `[armature]`, `[scudi]` e `[pf_bonus_costrutti]` in `creature.toml`.
- **Questo thread:** costruttore, strumenti e misura.

Prima: [MISURA-PRIMA-PF1E.md](MISURA-PRIMA-PF1E.md) (main 421dbd0, con la
misura nuova). Dopo: [MISURA-DOPO-PF1E.md](MISURA-DOPO-PF1E.md).

| Tabella PF1e | Fonte | Prima: coperte / giuste | Dopo: coperte / giuste |
|---|---:|---|---|
| classi base, ibride, PNG, alternativa | 37 | 0 / 0 | 37 / 37 |
| classi di prestigio | 18 | 0 / 0 | 18 / 18 |
| armature · scudi | 12 · 6 | 0 · 0 | 12 · 6, tutte giuste |
| griglie al giorno (anche estratti) | 22 | 0 / 0 | 22 / 22 |
| conosciuti | 8 | 0 / 0 | 8 / 8 |
| **uso:** classi generate e passate al cancello PF1e, con gli incantesimi scelti | 55 | 0 (rifiutate) | **55 / 55** |
| **uso:** tipi di creatura portati in PF1e che passano il cancello | 20 | 20 / **7** | 20 / **20** |
| abilità · tipi e taglie | 26 · 13 | tutte giuste | tutte giuste |
| **totale** | 217 | 59 coperte, 46 giuste | **217 / 217** |

**Cosa è cambiato negli strumenti:**
- **`genera_creatura --sistema pf1e --classe`.** Costruisce da zero dalle
  tabelle del PRD con `genera_png_pf1e`: tutte le 55 classi e la multiclasse
  (`mago:5,mistificatore arcano:3`). Le classi di prestigio fanno avanzare la
  classe incantatrice; il teurgo mistico ne fa avanzare due. Vengono dal PRD o
  dalle sue tabelle:
  - pf col primo dado al massimo;
  - BAB e TS per classe;
  - BMC/DMC e gradi;
  - CA dalle armature PF1e;
  - griglie, estratti e conosciuti, LI = livello − 3 per le classi che
    cominciano al 4°;
  - GS = livelli − 1 (PRD, Encounters);
  - incantesimi scelti dalla lista PF1e della classe, con i nomi italiani del
    lessico, preferendo quelli che le liste curate mettono nella funzione
    chiesta.

  Prima rifiutava i livelli di classe.
- **`creature_pf1e.converti`** (DV razziali):
  - `pf-dado` porta il bonus, così il cancello lo legge;
  - i costrutti hanno i pf bonus per taglia, ricostruiti dalle schede del
    Bestiary perché la tabella manca nel PRD in cache.

  Prima 13 tipi su 20 non passavano il cancello PF1e.
- **Misura.** Il lettore è esteso alle classi ACG, all'antipaladino (dado vita
  dalla sezione «Hit Die») e all'investigatore. Corretti cinque difetti del
  lettore:
  - TS buono di prestigio;
  - gradi «at Each Level»;
  - intestazione dello Swashbuckler;
  - cella Special omessa all'Hunter 16°;
  - colonne «Extracts per Day».

  Due righe nuove misurano l'**uso**, non solo i dati.
- **Difetto del cancello trovato e corretto dal thread della #363.** Le classi
  scritte sia nel nome sia nel tipo erano contate due volte, e BAB e TS
  venivano saltati.

**Limiti che restano, dichiarati:**
- ~~**Costrutti fine e diminutive:** nessuna scheda di costrutto nel PRD, quindi
  niente pf bonus.~~ **Chiuso il 2026-11-10 (regole complete, lotto 5):** la
  tabella «Construct Size» del PRD pubblicato (legacy.aonprd.com,
  bestiary/creatureTypes.html) dà «—» a Fine, Diminutive e Tiny; l'estrattore
  la usa per le taglie senza schede ed esige che concordi con le schede per le
  altre (concorda su 7 su 7, compreso il Colossal +80 del Wickerman).
- ~~**Requisiti delle classi di prestigio:** non si controllano.~~ **Chiuso dal
  lotto 4 delle regole complete:** requisiti delle 18 classi letti dal PRD
  (18/18) e controllati dal generatore, vie d'ingresso legali 18/18; gradi,
  allineamento e requisiti narrativi restano al DM, scritti nel conto.
- ~~**Sciamano:** non ha il livello 0 nel PRD in cache.~~ **Chiuso dal lotto 4:**
  le 17 orazioni vengono dal testo «0-Level Shaman Spells» dell'ACG.
- **Incantesimi:** se la funzione chiesta non ha abbastanza voci, la scelta si
  completa dal resto della lista PF1e della classe; il conto lo dice. I nomi
  senza voce nel lessico italiano PF1e restano inglesi e il conto li conta.
