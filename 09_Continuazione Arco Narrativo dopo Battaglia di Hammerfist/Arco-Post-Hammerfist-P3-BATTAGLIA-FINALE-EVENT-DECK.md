# Battaglia di Rethmar — IL MAZZO EVENTI (Event Deck)
## *La battaglia a scene scelte dai PG (D13) — Day 40-42*

> **Versione**: v1 (2026-07-02) — **Lotto C7** del PIANO-REVISIONE-ARC09, il file
> più importante del Lotto C. **APL 13-14. Scala mappe: 1,5 m/quadretto.**
> **Prototipo giocato**: `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md`
> (assedio di Dauth) — stesso schema, qui amplificato sui 3 giorni.
> **Motore nascosto (il Fronte, ruoli di comando, d12 eventi, Tyrgarun)**:
> `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAR-STRUTTURA.md` §9 (C1).
> **Numeri/fasi orda**: `...ARMATE-SYNC.md` §3-§4 · `campaign/state.md` §2.

---

## §0 — VINCOLO DI DESIGN (D13 — leggere prima di tutto)

La Battaglia di Rethmar **NON è un wargame** e **NON è a ondate generiche**. È una
**catena di eventi discreti ad alta posta** (remix della Battle of Brindol, RHoD
Parte 4 — la copia RHoD resta lato DM, **mai riprodurre testo**). I PG vivono la
battaglia come **carte-crisi che SCELGONO loro**:

- Ogni carta è un **incontro tattico completo, da giocare dal vero**: mappa in
  scala, statblock/puntatore, iniziativa, tattiche — **esito NON predefinito,
  deciso dai dadi** (vittoria / parziale / sconfitta, ciascuna con conseguenze).
- A ogni **campana** (2-3 per giorno) il DM presenta **3-4 crisi simultanee**; i
  PG ne scelgono **1-2** (possono dividersi). Le non scelte si risolvono
  **off-screen** con la tabella §4. Nessun evento è obbligatorio: **la pressione
  nasce dallo scegliere a chi non rispondere.**
- **Cosa NON fare**: niente sistema armate alla Kingmaker; niente griglia con 200
  miniature. Le meccaniche di massa di Hammerfist e i calcoli ARMATE-* restano
  **solo lato DM** come sfondo strategico — mai al tavolo. Le ondate di Fase 1
  (FASE1-ASSEDIO-TESTO) diventano **lo sfondo tra le campane**: sono il rumore, le
  carte sono la storia.
- I **VP restano ma nascosti**: sono **"il Fronte"** (STRUTTURA §9.1), tracker del
  DM che colora le descrizioni e determina l'esito, mai un punteggio mostrato.

---

## §1 — REGOLA DELLE TRE SORGENTI (vincolante — riusa > espandi > inventa)

Ogni carta dichiara in testa la propria sorgente. **Se una carta [S3] duplica
qualcosa di esistente, è un errore da correggere.**

- **[S1 — RHoD upscalato]**: eventi della Battle of Brindol originale, **espansi a
  APL 14 e riallineati all'esercito RumblingStone v2** (orda ~10k, 5 draghi, drow
  di Sonjak, Githyanki, Teschio Nero). Mai riprodurre testo RHoD.
- **[S2 — echi di campagna]**: eventi in cui i PG interagiscono con ciò che l'arco
  ha **GIÀ costruito** (Sal, Halveth, Lorana, Ghostlord, Sethrax/Orbe, Zalkatar
  wildcard, statue vive Sal→Varis). Materiale esistente, mai doppiato.
- **[S3 — nuove, solo per i buchi]**: inventate SOLO dove né S1 né S2 coprono un
  momento necessario del ritmo dei 3 giorni.

### 1.1 — Tabella di mappatura CARTA → SORGENTE → FILE RIUSATO

| # | Carta | Sorgente | Materiale/file riusato (mai doppiato) | Spotlight |
|---|---|---|---|---|
| 1 | Le Cripte del Tempio | **S2** | FASE0-NOTTE-DEI-DROW-TESTO/MAPPA; Halveth (Consiglio_Rethmar §2) | Thorik |
| 2 | Il Cecchino nella Notte | **S1** | archetipo Brindol (assassino); `deathlock-cr8` / assassino [INFERRED] | Artemis |
| 3 | La Marea alle Porte | **S3** | *(buco di ritmo Day 41 — crisi civile, non coperta da S1/S2)* | Hella |
| 4 | L'Olio di Sabotaggio di Sal | **S2** | clock Sal (state.md §3); `PNG/Salvatore/Salvatore.md` | Tordek |
| 5 | Il Tradimento di Halveth | **S2** | Consiglio_Rethmar §2 (Halveth); state.md §7 | Thorik |
| 6 | Il Convoglio di Lorana | **S2** | `capitana-lorana-cr7`; state.md §7 (Riserva Lorana) | Hella |
| 7 | La Breccia della Porta Ovest | **S1** | FASE1-ASSEDIO §3; `ondata-giganti-fanteria-cr15` | Thorik |
| 8 | Tyrgarun sui Bastioni | **S1** | STRUTTURA §9.4 (C1.d); `tyrgarun-blue-old-cr18` | Artemis |
| 9 | Combattimenti di Strada | **S1** | archetipo Brindol; `hobgoblin-*`, `gnoll-hyenodon-rider-cr4` | Tordek |
| 10 | I Leoni del Ghostlord | **S2** | `ghost-lion-spettrale-cr8`; Ghostlord-TESTO (3 rami, D7) | Hella |
| 11 | La Difesa del Tempio-Ospedale | **S1** | archetipo Brindol (cappella); eco Fase 0 | Hella |
| 12 | L'Altare Campale (Ritualisti) | **S2** | FASE2-RITUALISTI §8; Sethrax/Orbe, Zalkatar wildcard; statue Sal→Varis | Tordek/Artemis |
| 13 | Il Duello di Karruk | **S1** | archetipo Brindol (duello Wyrmlord); `wyrmlord-karruk-cr10` | Tordek/Thorik |
| 14 | Il Falso Segnale | **S3** | *(buco di ritmo — finta/diversivo che forza una scelta)* | Artemis/party |

**Mix**: S1 = 6 (2,7,8,9,11,13) · S2 = 6 (1,4,5,6,10,12) · S3 = 2 (3,14) — coerente
con il target ~S1:5-6 / S2:5-6 / S3:2-4. **Nessun doppione**: ogni S3 copre un buco
non coperto da S1/S2.

---

## §2 — RITMO DEI 3 GIORNI (quando escono le carte)

| Giorno | Fase | Campane | Carte in gioco | Note |
|---|---|---|---|---|
| **Day 40 (notte)** | Fase 0 | 2 | 1, 2 (infiltrazione) | Notte dei Drow; furtività, alta posta bassa scala |
| **Day 41 (orda in vista)** | pre-assedio | 2 | 3, 4, 5, 6 (crisi civile + sabotaggio interno) | **1 riposo lungo** scandito a fine giornata |
| **Day 42 (alba→notte)** | Fasi 1-4 | 3-4 | 7-14 (assedio + ritualisti + finale) | Campane serrate, **solo riposi brevi**, carte sempre più gravi |

**Regola risorse (onestà del climax)**: tieni il conteggio di slot/pf onesto. La
**scarsità è parte del climax**: dopo il riposo lungo del Day 41, il Day 42 si
gioca in economia calante. Le carte tardive (12-14) presumono un party affaticato.

---

## §3 — COME SI GIOCA UNA CAMPANA (menù di crisi)

1. Il DM applica **prima** i modificatori fissi al Fronte (quest completate,
   alleati, Morale Cittadino C2) — STRUTTURA §9.1.
2. Presenta **3-4 carte** della finestra corrente come **crisi simultanee**.
3. I PG scelgono **1-2** (possono dividersi; un PG può spendere la campana in un
   **ruolo di comando**, STRUTTURA §9.2, invece di una carta).
4. Le carte scelte si **giocano dal vero** (mappa + statblock + iniziativa).
5. Le carte **non scelte** si risolvono **off-screen** (§4).
6. Si aggiornano Fronte e Morale Cittadino; si passa alla campana successiva.

> **Regola spotlight**: ogni carta ha un **PG designato**, ma è giocabile da
> chiunque. Se lo spotlight è altrove/caduto, la carta resta aperta agli altri o
> va off-screen.

---

## §4 — RISOLUZIONE OFF-SCREEN DELLE CARTE NON SCELTE

Per ogni carta **non giocata**, tira **1d20 + Fronte corrente** vs **CD 18**:

- **≥ CD**: la guarnigione/gli alleati tengono da soli (nessun Δ).
- **CD-1 … CD-5**: tiene ma con perdite → **−1 Fronte** + la conseguenza narrata
  della carta ("Se ignorata").
- **< CD-5**: la crisi va **male** → **−2 Fronte** + conseguenza grave della carta.

> Applica i modificatori fissi **prima** di tirare, così le scelte a monte (quest,
> Consiglio, Morale) pesano davvero sull'esito delle crisi lasciate aperte.

---

# §5 — LE CARTE

> Formato: **Sorgente · Spotlight · Fase/Giorno**; Trigger; Read-aloud (3 righe);
> Mappa (griglia 1,5 m/q); Nemici (EL + puntatore statblock); Tattica; Posta;
> **3 esiti aperti** (Vittoria/Parziale/Sconfitta, decisi dai dadi) con Δ Fronte;
> **Se ignorata** (off-screen).

---

## CARTA 1 — LE CRIPTE DEL TEMPIO  ·  [S2]  ·  *spotlight: Thorik*  ·  Fase 0 / Day 40 notte
- **Trigger**: le campane del Tempio suonano a mezzanotte; un commando drow è già nelle cripte (Notte dei Drow). **Eco Halveth**: se **non rimosso** (Consiglio_Rethmar §2), i drow hanno la pianta e la posizione delle sentinelle → **+1 CR**.
- **Read-aloud**: *Le campane impazziscono. Dal quartiere sacro sale una luce verde-malata e l'odore di funghi marci. Sotto i vostri piedi, la pietra trema: qualcosa di grosso sta sfondando le colonne delle cripte, verso la Camera dell'Artefatto.*
- **Mappa**: navata + discesa cripte, **riuso** `FASE0-...-MAPPA.md` (18×24, 1,5 m/q); colonne = copertura; cripte = spazi stretti (l'Aberrazione Alfa fatica a manovrare).
- **Nemici (EL 14-15)**: 1 High Priestess drow (`drow-priestess9-cr11` pompata) + 4 Drow Fungal Minion + 1 Aberrazione Fungina Alfa CR 12. Se **Sabotaggio Campi Drow** fatto: −Alfa, 5-8 drow (EL 12).
- **Tattica**: la Priestess usa *darkness*/ragnatele e tenta il rito di sblocco dell'Artefatto (3 round); l'Alfa fa da ariete vivente contro le colonne.
- **Posta**: l'**Artefatto Maligno**. Se rubato → potenzia il rituale di Fase 2 (FASE2 §8.2: +2 CD/+20 pf ai foci).
- **Esiti**: **Vittoria** (Artefatto salvo/distrutto, commando respinto) → +2 Fronte. **Parziale** (Artefatto salvo ma tempio danneggiato) → +0, −1 Morale Cittadino. **Sconfitta** (Artefatto rubato) → −2 Fronte + Fase 2 peggiorata.
- **Se ignorata**: l'Artefatto è rubato → −2 Fronte e la Carta 12 (Altare) parte con il 4° focus attivo.

---

## CARTA 2 — IL CECCHINO NELLA NOTTE  ·  [S1]  ·  *spotlight: Artemis*  ·  Fase 0 / Day 40 notte
- **Trigger**: durante il caos della Notte dei Drow, un assassino punta a un **comandante** (Lady Kaal, Brenna Sorvane o Lorana). **Eco Halveth**: se al potere, ha "aperto la porta" all'assassino.
- **Read-aloud**: *Un balenio di balestra dal tetto del municipio. Il primo dardo manca Lady Kaal di un palmo e si conficca nella trave. Il secondo è già incoccato. Chi protegge i comandanti stanotte, li tiene vivi per la battaglia di domani.*
- **Mappa**: tetti e vicoli del quartiere nobile, **8×12** (1,5 m/q); dislivelli (Scalare CD 15), comignoli = copertura, corda tesa per la fuga.
- **Nemici (EL 13)**: 1 assassino (Ladro 7/Assassino 3 [INFERRED — needs DM confirmation]) + 2 `drow-fighter3-cr4` o `deathlock-cr8` di scorta. Tattica: colpo furtivo, veleno (CD 16), fuga sui tetti.
- **Posta**: la vita di un comandante = un pilastro del morale e del Consiglio.
- **Esiti**: **Vittoria** (assassino catturato/ucciso, bersaglio salvo) → +1 Fronte, +intel su Halveth/Sonjak. **Parziale** (bersaglio salvo, assassino fugge) → +0. **Sconfitta** (comandante ferito grave/ucciso) → −2 Fronte, −2 Morale Cittadino (d12 evento §9.3-3).
- **Se ignorata**: il comandante bersaglio cade → −2 Fronte; se è Brenna, la milizia perde coordinamento (Consiglio_Rethmar §4).

---

## CARTA 3 — LA MAREA ALLE PORTE  ·  [S3]  ·  *spotlight: Hella*  ·  pre-assedio / Day 41
- **Trigger** (Campana 1, Day 41): l'orda è **in vista**; migliaia di rifugiati e civili premono alle porte in preda al panico, mentre gli infiltrati (state.md §2.5) tentano di entrare nascosti tra loro.
- **Read-aloud**: *La strada per la Porta Est è un fiume di gente: carri rovesciati, bambini urlanti, un vecchio che stringe una gallina come fosse oro. In mezzo alla marea, tre volti che non guardano indietro con paura — guardano avanti, con metodo.*
- **Mappa**: piazzale della Porta Est **14×10** (1,5 m/q); ressa = terreno difficile e ingombro; carri = copertura/ostacoli; la porta è un imbuto.
- **Nemici (EL 12)**: 3-5 infiltrati (2 hobgoblin travestiti + 1 `drow-fighter3-cr4` + 2 gnoll) — Individuare CD 18 / *detect magic*. **Non** è un incontro frontale: è **crowd control + smascheramento** (Diplomazia/Intimidire per gestire la ressa, Sense Motive per gli infiltrati).
- **Posta**: se gli infiltrati entrano → +1 CR Fase 0/1 + 20 difensori avvelenati (state.md §2.5); la gestione della ressa muove il **Morale Cittadino** (C2).
- **Esiti**: **Vittoria** (infiltrati presi, ressa incanalata) → +1 Fronte, +1 Morale Cittadino, −2 CR Fase 0. **Parziale** (ressa salva, 1-2 infiltrati sfuggiti) → +0. **Sconfitta** (calca/infiltrati dentro) → −1 Fronte, −1 Morale, morti da calpestamento.
- **Se ignorata**: infiltrati dentro → +1 CR alle carte 1/5; −1 Morale Cittadino.

---

## CARTA 4 — L'OLIO DI SABOTAGGIO DI SAL  ·  [S2]  ·  *spotlight: Tordek*  ·  pre-assedio / Day 41
- **Trigger**: il clock di **Sal** (state.md §3, 0/6) matura — l'Olio di Sabotaggio applicato alle armi/difese sta per cedere "al momento peggiore". I PG possono scoprirlo *ora* (Day 41) o subirlo in battaglia.
- **Read-aloud**: *L'armiere di Rethmar ti mostra una lama: sotto la luce sembra unta di un olio iridescente che non si asciuga. "Metà dell'arsenale è così, Custode. Non so da quanto. Non so chi." Ma tu conosci quell'odore: mercante, deserto, sorriso facile.*
- **Mappa**: arsenale/fucina cittadina **10×8** (1,5 m/q); scaffali d'armi (copertura), forgia (hazard fuoco), botole verso i magazzini.
- **Nemici (EL 12-13)**: se Sal è ancora in zona, un suo agente (Ladro/Esperto) + 2 guardie corrotte; **oppure** solo skill challenge (Individuare/Artigianato/Sapienza Magica CD 18-20 per identificare e neutralizzare l'olio prima della battaglia).
- **Posta**: se non neutralizzato, in Fase 3 le armi dei difensori (e forse dei PG) rischiano **fallimento TS** contro il boss (state.md §3).
- **Esiti**: **Vittoria** (olio neutralizzato, agente preso) → +1 Fronte, intel su Sal/Collezionista. **Parziale** (olio in parte rimosso) → +0, malus dimezzato in Fase 3. **Sconfitta** (non scoperto) → l'olio scatta in Fase 3 (−2 a un TS chiave del boss).
- **Se ignorata**: l'olio scatta al momento peggiore (Fase 3) → conseguenza sopra; le statue Sal→Varis (Carta 12) sono a piena forza.

---

## CARTA 5 — IL TRADIMENTO DI HALVETH  ·  [S2]  ·  *spotlight: Thorik*  ·  pre-assedio / Day 41
- **Trigger**: se **Halveth non è stato rimosso** dal Consiglio (Consiglio_Rethmar §2), Day 41 fa "sparire" convenientemente ordini di difesa e/o apre una via ai drow. **Se rimosso prima: questa carta non entra nel mazzo.**
- **Read-aloud**: *Un paggio ansante: "Custode! Il Consigliere Halveth ha ordinato di richiamare le guardie dal magazzino delle polveri — dice per 'riorganizzare'. Ma il magazzino ora è sguarnito, e ho visto uomini che non conosco scendere verso i condotti."*
- **Mappa**: magazzino polveri + condotti **12×10** (1,5 m/q); barili di polvere = hazard esplosivo (fuoco → 6d6 area); scale ai condotti sotterranei.
- **Nemici (EL 13)**: Halveth (GS 5, non combattente — fugge) + 2-3 sicari (`drow-fighter3-cr4` / mercenari) + guastatori con la chiave della poterna.
- **Posta**: smascherare Halveth con prove **davanti al Consiglio** (perde il seggio, −1 CR Fase 0/1) e impedire il sabotaggio della polveriera.
- **Esiti**: **Vittoria** (Halveth smascherato + polveriera salva) → +2 Fronte, +1 Morale (esecuzione/cattura pubblica), voto difesa passa. **Parziale** (sabotaggio fermato, Halveth fugge) → +0, resta minaccia. **Sconfitta** (polveriera salta) → −2 Fronte, breccia interna, −2 Morale.
- **Se ignorata**: Halveth ritarda la risposta drow di 2 round (Consiglio §Seduta 3) → +1 CR Fase 0 e −1 Fronte.

---

## CARTA 6 — IL CONVOGLIO DI LORANA  ·  [S2]  ·  *spotlight: Hella*  ·  pre-assedio / Day 41
- **Trigger**: la **Riserva di Lorana** (rifugiati armati + rifornimenti, state.md §7) arriva da est ma un'avanguardia nemica la intercetta prima delle mura.
- **Read-aloud**: *All'orizzonte a est, la polvere di un lungo convoglio: i carri di Lorana, la riserva che può reggere un intero settore. E, tagliando i campi per intercettarli, una colonna di cavalcatori di iene che ulula al passo.*
- **Mappa**: strada di campagna + carri **20×8** (1,5 m/q); i carri sono asset mobili (copertura + da proteggere); fossi ai lati (terreno difficile).
- **Nemici (EL 14)**: 6 `gnoll-hyenodon-rider-cr4` + 1 `gnoll-chieftain-cr10` (o `teschio-nero-commander-cr10`). Tattica: colpire i carri, disperdere i rifugiati.
- **Posta**: il convoglio = **+150 fanteria civile di riserva** a Rethmar (Consiglio_Rethmar §Tabella; Morale 7+ aggiunge altri 150 volontari, C2).
- **Esiti**: **Vittoria** (convoglio salvo) → +2 Fronte, +150 riserva, Lorana integrata. **Parziale** (convoglio danneggiato) → +1 Fronte, +75 riserva. **Sconfitta** (convoglio disperso) → +0, Lorana ferita (d12 §9.3), rifugiati in fuga (−1 Morale).
- **Se ignorata**: convoglio decurtato del 50% → +75 riserva invece di +150; Lorana arriva comunque ma amareggiata (state.md §7).

---

*(Fine Day 40-41. Le carte 7-14 coprono il Day 42, Fasi 1-4 — vedi seguito.)*

---

## CARTA 7 — LA BRECCIA DELLA PORTA OVEST  ·  [S1]  ·  *spotlight: Thorik*  ·  Fase 1 / Day 42
- **Trigger** (Campana 1, Day 42): l'Ondata 1 (fanteria & giganti, FASE1 §3) sfonda i battenti della Porta Ovest.
- **Read-aloud**: *Il portone di quercia e ferro regge tre colpi d'ariete, poi il quarto — vibrato da uno stone giant — lo apre come un guscio. Nella polvere, una testuggine di scudi rossi avanza al tempo di tamburo. Se entra in piazza, l'Ovest è perso.*
- **Mappa**: androne della Porta Ovest + piazzetta **14×10** (1,5 m/q); il varco è 3 q (imbuto); macerie = terreno difficile + copertura +4; camminamenti sui lati (scale).
- **Nemici (EL 15)**: `ondata-giganti-fanteria-cr15` (2-3 giganti + hobgoblin élite + 1 warcaster). Tattica: i giganti sfondano, la fanteria dilaga in ventaglio.
- **Posta**: tenere/richiudere il varco (3 round di lavoro dei genieri, 1 se Thorik li comanda — ruolo Comandante §9.2). **300 nani** (se presenti) coprono metà del varco.
- **Esiti**: **Vittoria** (varco richiuso, giganti abbattuti) → +2 Fronte. **Parziale** (varco tenuto, qualche hobgoblin dilaga → Carta 9) → +0. **Sconfitta** (varco perso) → −2 Fronte, quartiere Ovest invaso.
- **Se ignorata**: check Morale (§9.1); tipicamente −1 Fronte e quartiere Ovest danneggiato.

---

## CARTA 8 — TYRGARUN SUI BASTIONI  ·  [S1]  ·  *spotlight: Artemis*  ·  Fase 1-3 / Day 42
- **Trigger**: il **drago blu Old Tyrgarun** (CR 18) plana sui bastioni con passate di soffio. **Questa carta È il set-piece C1.d** (STRUTTURA §9.4): si gioca come **hazard con contromosse**, non come scontro frontale.
- **Read-aloud**: *Il cielo si oscura di una sola ala. Tyrgarun scende in picchiata e il suo soffio corre lungo il bastione come un fiume di fulmini: torri di guardia diventano cenere. Poi risale, intoccabile, e i suoi occhi cercano chi tra voi maneggia la magia.*
- **Mappa**: tratto di bastione **20×5** (1,5 m/q) + cielo (quote: camminamento / volo basso / volo alto); balliste (2-4, riusabili dai PG: colpo 4d6) come contromosse; copertura sotto le merlature.
- **Nemici**: Tyrgarun **profilo aereo** (`tyrgarun-blue-old-cr18.md`; soffio linea 30 m 20d8 elettr., Ref CD 29). **Non si abbatte** — si **nega** con le 4 contromosse di STRUTTURA §9.4 (balliste, gufi Tiri-Kitor, missione-esca, Fulcro Arcano di Artemis).
- **Posta**: negare le passate a un settore; è la prova di Rethmar della grammatica anti-drago (già assaggiata a Dauth col Razorfiend, DAY3-CITY-SIEGE Carta B).
- **Esiti**: **Vittoria** (passate negate ripetutamente) → +1 Fronte; Tyrgarun ripiega a ricaricare. **Parziale** (contromosse a intermittenza) → +0, balliste perse. **Sconfitta** (2+ passate a segno) → −2 Fronte, un settore cede (breccia → Carta 7/9).
- **Se ignorata**: Tyrgarun brucia le difese aeree → −2 Fronte; le altre carte aeree diventano più dure. **Fase 4**: quando il Mythal lo inchioda (§7 STRUTTURA), il DM può aprire una **coda** di questa carta col profilo a terra (CR ~16-17).

---

## CARTA 9 — COMBATTIMENTI DI STRADA COI CIVILI  ·  [S1]  ·  *spotlight: Tordek*  ·  Fase 1 / Day 42
- **Trigger**: nemici filtrati da una breccia (Carta 7/8) dilagano in un quartiere abitato; barricate improvvisate, civili intrappolati.
- **Read-aloud**: *La battaglia non è più sulle mura: è nella tua via. Una madre trascina due bambini dietro un carro rovesciato mentre tre hobgoblin avanzano tra le case. Un vecchio fabbro brandisce un martello troppo pesante per lui. Qui si combatte casa per casa.*
- **Mappa**: isolato urbano **16×16** (1,5 m/q); vicoli stretti (nega la carica dei giganti — vantaggio dei PG mobili), barricate (copertura), porte/finestre (posizioni), civili = "ostacoli viventi" da proteggere.
- **Nemici (EL 14)**: 6-8 hobgoblin élite + 2 `gnoll-hyenodon-rider-cr4` (o 1 troll da guerra). Tattica nemica: terrore sui civili per spezzare il morale.
- **Posta**: salvare i civili = **Morale Cittadino** (C2); il quartiere è la casa di qualcuno.
- **Esiti**: **Vittoria** (nemici puliti, civili salvi) → +1 Fronte, +1 Morale. **Parziale** (nemici respinti, alcuni civili persi) → +0. **Sconfitta** (quartiere perso) → −1 Fronte, −2 Morale.
- **Se ignorata**: il quartiere è saccheggiato → −1 Fronte, −2 Morale Cittadino, rifugiati in più (Carta 3 aggravata).

---

## CARTA 10 — I LEONI DEL GHOSTLORD  ·  [S2]  ·  *spotlight: Hella*  ·  Fase 1-2 / Day 42
- **Trigger**: l'esito della quest Ghostlord (Ghostlord-TESTO, D7) decide **da che parte** arrivano i non-morti.
- **Read-aloud**: *Un ululato che non appartiene a nessuna gola viva. Dalla nebbia emergono leoni di luce spettrale — e per un istante, chi ha combattuto a Hammerfist riconosce quegli occhi. Sono anime. La domanda è: contro chi corrono, stanotte?*
- **Mappa**: fianco della città/cimitero **18×12** (1,5 m/q); lapidi (copertura), nebbia (occultamento), terreno consacrato/sconsacrato (rilevante per non-morti).
- **Nemici / alleati (EL 15 se ostile)**: **Ramo ostile** (Ghostlord nemico): 4-6 `ghost-lion-spettrale-cr8` + non-morti minori → +2.400 ondata (state.md §2.3), i PG devono contenerla. **Ramo neutrale**: 1-2 leoni isolati (colore). **Ramo alleato/redento**: i leoni colpiscono la **retroguardia Red Hand** → i PG possono dirigerli (Diplomazia/Natura) contro un'altra minaccia.
- **Posta**: contenere l'ondata (ostile) o **sfruttare** l'alleanza (redento → +600 pro-difensori, riduce un'altra carta).
- **Esiti (ramo ostile)**: **Vittoria** (ondata contenuta) → +1 Fronte. **Parziale** → +0, un settore logorato. **Sconfitta** → −2 Fronte, non-morti in città.
- **Esiti (ramo alleato)**: **Vittoria** (leoni ben diretti) → +2 Fronte, −1 carta nemica successiva. 
- **Se ignorata**: ostile → −2 Fronte; alleato → i leoni agiscono da soli, bonus dimezzato.

---

## CARTA 11 — LA DIFESA DEL TEMPIO-OSPEDALE  ·  [S1]  ·  *spotlight: Hella*  ·  Fase 1-2 / Day 42
- **Trigger**: il tempio (già colpito in Fase 0) è ora **ospedale da campo** stracolmo di feriti; una squadra nemica punta a raderlo al suolo per spezzare il morale.
- **Read-aloud**: *Il chiostro è un mare di barelle. Un chierico con le mani rosse fino ai gomiti ti afferra: "Guaritrice, non reggiamo — e c'è chi vuole finire i feriti prima di noi." Fuori, il rumore di stivali ferrati che si avvicina alla porta della corsia.*
- **Mappa**: chiostro-ospedale **12×12** (1,5 m/q); barelle (terreno ingombro), colonnato (copertura), pozzi/cisterne (eco DAY3 Carta C se avvelenate).
- **Nemici (EL 13-14)**: 1 `emissario-red-hand-cr12` (o warpriest) + 4-6 hobgoblin; se Fase 0 fallita, +2 aberrazioni fungine minori dai pozzi.
- **Posta**: proteggere feriti e chierici = **Morale Cittadino** + capacità di cura del Fronte; Hella in ruolo **Salvatore** (§9.2) qui rende al massimo.
- **Esiti**: **Vittoria** (ospedale tenuto) → +1 Fronte, +1 Morale, cure disponibili tra le campane. **Parziale** (tenuto ma feriti persi) → +0. **Sconfitta** (ospedale raso) → −2 Fronte, −2 Morale, niente cure.
- **Se ignorata**: strage nell'ospedale → −2 Fronte, −2 Morale Cittadino.

---

## CARTA 12 — L'ALTARE CAMPALE (RITUALISTI)  ·  [S2]  ·  *spotlight: Tordek / Artemis*  ·  Fase 2 / Day 42
- **Trigger** (Ritual Clock Azarr Kul, non March Clock): i ritualisti draconici completano il rito che richiama l'Avatar. **È il "quinto atto"** (FASE2-RITUALISTI §8): la squadra speciale PG va **oltre le linee**.
- **Read-aloud**: *Oltre le mura, su un pianoro annerito, tre altari elementali pulsano al canto di dodici ritualisti. Al centro, la gola del mondo si apre round dopo round. Andare là significa lasciare le mura ad altri. Ma se il canto finisce, sarà stato tutto inutile.*
- **Mappa**: pianoro rituale a 3 anelli, **riuso** `FASE2-RITUALISTI-MAPPA.md` (40×30, 1,5 m/q); 3 foci distruttibili (FASE2 §8.2: CA 5, 60 pf, RD 10/magia); cerchio runico (Will CD 18).
- **Nemici (EL 15-16)**: anello esterno (hobgoblin + `githyanki-knight-elite-cr10`), medio (drago guardiano `Abithriax` + `warpriest-tiamat-cr7`), interno (`tiamat-warpriest-elite-cr11` ×3-5). **Echi S2**: se **Sethrax è fuggito col Seme** o **Zalkatar è vivo** (wildcard), aggiungi il loro potenziamento (state.md §3: +2 RI). Se l'**Artefatto Maligno** è stato rubato (Carta 1), è il 4° focus.
- **Posta / scelta esplicita**: interrompere il rituale (Avatar depotenziato in Fase 3) **vs** tenere le mura — **non entrambe senza alleati** (FASE2 §8.3). **Coda Fase 4**: la vittoria qui alimenta l'attivazione delle **Statue-Golem** (MYTHAL-FOCUS §5) e chiude la filiera delle **statue vive Sal→Varis** (Consiglio_Rethmar: Halveth/Sorvane).
- **Esiti**: **Vittoria** (rito rotto 0-4 round) → +3 Fronte, Fase 3 a CR 15-16. **Parziale** (5-8 round) → +1 Fronte, Avatar ridotto. **Sconfitta** (9-10 round) → −2 Fronte, Avatar pieno + Azarr Kul buffato.
- **Se ignorata**: il rito riesce → Avatar a piena potenza in Fase 3 (−2 Fronte).

---

## CARTA 13 — IL DUELLO DI KARRUK  ·  [S1]  ·  *spotlight: Tordek / Thorik*  ·  Fase 1-3 / Day 42
- **Trigger**: il **Wyrmlord Karruk** (CR 10) sfida pubblicamente un campione dei difensori sulle mura — un rituale di guerra hobgoblin per spezzare il morale.
- **Read-aloud**: *Un corno grave, tre volte. Sui gradini della breccia, un hobgoblin enorme in armatura di scaglie rosse pianta l'ascia nella pietra e ruggisce, nella lingua comune: "Il vostro migliore contro di me! O guardate i vostri morire senza onore!" Tutta la mura trattiene il fiato.*
- **Mappa**: sommità di un bastione/breccia **10×10** (1,5 m/q); arena improvvisata delimitata dai soldati (i due eserciti guardano — nessuno interviene finché dura il duello); dislivelli, bordo (caduta).
- **Nemici (EL 12-14)**: `wyrmlord-karruk-cr10.md` + 1 Razorfiend di scorta (se il duello degenera). Tattica: Karruk combatte d'onore finché è avvantaggiato, bara se perde.
- **Posta**: **ruolo Campione** (§9.2): se un PG vince il duello, l'ondata di quel settore perde 1 grado di CD e +1 Fronte; rifiutare/perdere = −1 Fronte e morale nemico su.
- **Esiti**: **Vittoria** (Karruk battuto in duello) → +2 Fronte, ondata Ovest indebolita. **Parziale** (duello inconcluso, Karruk ripiega) → +0. **Sconfitta** (campione PG cade) → −2 Fronte, +1 CR Fase 1 di quel settore.
- **Se ignorata**: nessun campione accetta → il morale difensori cala (−1 Fronte); Karruk guida di persona la prossima breccia (Carta 7 +1 CR).

---

## CARTA 14 — IL FALSO SEGNALE  ·  [S3]  ·  *spotlight: Artemis / party*  ·  Fase 1-2 / Day 42
- **Trigger** (Campana centrale, Day 42): il nemico inscena una **finta** — un finto cedimento in un settore per attirare le riserve, mentre il colpo vero arriva altrove. Buco di ritmo non coperto da S1/S2: **la carta che punisce la lettura sbagliata del campo**.
- **Read-aloud**: *Un messaggero trafelato: "La Porta Nord cede! Mandate tutto!" Ma qualcosa non torna — i fuochi a nord sono troppo ordinati, troppo… teatrali. Da qualche parte, qualcuno vuole che guardiate nella direzione sbagliata.*
- **Mappa**: sala del comando + due settori a scelta **(astratta + zoom sul settore giusto, 12×10, 1,5 m/q)**; la scena chiave è la **lettura** (Sapienza Magica/Conoscenze/Sense Motive CD 20) prima del combattimento.
- **Nemici (EL 14)**: dipende da dove cade il colpo vero — un pacchetto d'assalto (`teschio-nero-commander-cr10` + Teschio Nero, `thayan-knight-cr8`) contro il settore **davvero** debole.
- **Posta**: indovinare la finta = concentrare le riserve dove serve; sbagliare = una breccia reale non presidiata.
- **Esiti**: **Vittoria** (finta smascherata, colpo vero respinto) → +2 Fronte. **Parziale** (capito in ritardo) → +0, un settore logorato. **Sconfitta** (riserve sprecate a nord) → −2 Fronte, breccia reale aperta (→ Carta 7/9).
- **Se ignorata / non letta**: le riserve vanno alla finta → −2 Fronte, il colpo vero apre un settore.

---

## §6 — CHECKLIST DI SESSIONE (DM)

- [ ] Deciso **chi** dei PG è libero per la campana e **quali** carte sono in gioco (finestra §2)?
- [ ] Applicati i **modificatori fissi** al Fronte (quest, Consiglio, Morale Cittadino C2) **prima** dei tiri?
- [ ] A ogni campana: **3-4 crisi** presentate, **1-2** scelte, le altre risolte off-screen (§4)?
- [ ] Ogni carta giocata **dal vero** (mappa in scala + statblock/puntatore + iniziativa), esito **ai dadi**?
- [ ] Segnati gli esiti (V/P/S) e aggiornati **Fronte** e **Morale Cittadino**?
- [ ] Rispettato il **ritmo risorse** (riposo lungo Day 41, solo brevi Day 42)?
- [ ] Propagato agli esiti (ESITI-CONSEGUENZE §2 matrice VP) e a `state.md` §2/§8?
- [ ] Tyrgarun giocato come **hazard** (Carta 8) finché il Mythal non lo inchioda (§7 STRUTTURA)?

---

## §7 — CROSS-LINK

- **Motore nascosto (Fronte, ruoli, d12, Tyrgarun)**: `...RETHMAR-STRUTTURA.md` §9
- **Prototipo giocato**: `...P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md`
- **Fasi/ondate di sfondo**: `...FASE0-...-TESTO`, `...FASE1-ASSEDIO-TESTO`, `...FASE2-RITUALISTI-TESTO` (§8), `...FASE3-...`, `...FASE4-...`
- **Statue-Golem & scena eroica**: `...MYTHAL-FOCUS-PG-SCENA-EROICA.md`
- **Esiti/VP e ricompense**: `...ESITI-CONSEGUENZE.md` §2, §11-§12
- **Numeri/composizione orda**: `...ARMATE-SYNC.md` §3-§4 · `campaign/state.md` §2-§3
- **Statblock riusati**: `00_Red Hand Of Doom/Armate-UNITA-NUOVE/` (ondata-giganti, tyrgarun-blue-old, wyrmlord-karruk, ghost-lion-spettrale, githyanki-knight-elite, tiamat-warpriest-elite, teschio-nero-commander, gnoll-hyenodon-rider, drow-*, capitana-lorana, emissario-red-hand, thayan-*)
- **Consiglio & morale**: `PNG/Consiglio_Rethmar/Consiglio_Rethmar.md` (§Halveth, §Morale Cittadino C2)
- **PNG chiave**: `PNG/Salvatore/`, `PNG/Sethrax_il_Velato/`, `PNG/Xal_thor/` (Zalkatar wildcard), `PNG/Ghostlord/`, `PNG/Lorana/`
