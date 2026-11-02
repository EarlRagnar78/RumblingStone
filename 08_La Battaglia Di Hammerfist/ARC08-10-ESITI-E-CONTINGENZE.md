# ARC-08 — Esiti, Contingenze e Conversione Flashback→Bonus

> **Scopo**: il file che permette al DM di arbitrare **qualunque** esito
> della Battaglia di Hammerfist senza improvvisare. Contiene: (1) i tre
> scenari d'esito (vittoria piena / vittoria costosa / caduta) con
> conseguenze numeriche agganciate ai tracker; (2) i rami condizionali
> di Fauci di Palude (D10) col gancio al carry-over ARC-07 (A12); (3)
> la **tabella di conversione D9** che trasforma gli obiettivi del
> flashback dei pregen in bonus concreti per il finale dei Rumbling
> Stones — MAI in PX.
> **Stato**: canonico (contenuto di modulo; canone di trama in
> `campaign/state.md`, non ancora giocato — piano ARC-08 A0/B1).
> **Ultima revisione**: 2026-07-02.
> **Benchmark**: `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ESITI-
> CONSEGUENZE.md` (ARC-09, per struttura); `Cerimonia-delle-100-Asce.md`
> (per tono).

<!-- storico -->
> 🧭 **Perché questo file è cambiato così spesso (ottobre 2026).** Dal
> 2026-10-17 al 2026-10-18 sono state chiuse le marche INFERRED. Il
> 2026-10-19 sono entrate le dodici decisioni del giro (D9-D20) e la presa
> in bocca di Fauci. Il 2026-10-21 il flashback dei pregen ha preso il
> libretto della battaglia campale (ADR-0096), le carte dei poteri e
> l'avanguardia nella Sessione 1, e il §5.3 dà al Re gli 8 pf al Cuore.
<!-- /storico -->

---

## 0. Regola d'oro — gli esiti NON sono un copione

Questo arco **non è ancora stato giocato** (piano ARC-08 A0). Tutto ciò
che segue è **preparazione**: la battaglia quantifica le conseguenze di
ogni ramo, **non** ne decide l'esito. Il ramo **default** — su cui è
costruito tutto l'ARC-09 — è la **vittoria piena** (E1-E8): l'engine e
il DM lo trattano come bersaglio di progetto, ma i gradi dell'esito
restano ai dadi (stessa filosofia di ARC-09 D13).

**Nessun ramo è "game over"**: anche la caduta di Hammerfist (§3) apre
una linea narrativa, non chiude la campagna.

---

## 1. ESITO DEFAULT — Vittoria piena (E1-E8)

**Quando**: i difensori reggono l'assedio; i Rumbling Stones riemergono
al Cuore della Montagna al Giorno 3 (E6, salto del Rubino ARC-07 D16) e
ribaltano la battaglia; l'avanguardia della Mano Rossa è
annientata/dispersa.

**Numeri canonici (D11)**:

| Voce | Valore | Fonte |
|---|---|---|
| Nani difensori iniziali | 300 | E8; Guida DM |
| Nani caduti | **210** = 118 a Hammerfist + 92 nei mesi precedenti. I 9 di Drellin's Ferry si nominano nel Giuramento ma non si contano `[CANONE — DM 2026-10-19, D17]` | E2; Cerimonia §1.1 |
| Nani superstiti | **90**, guidati da Re Thorek. Al tavolo si contano dal Registro: la somma dei PFU rimasti alle unità naniche di `ARC08-03`, un nano per PFU (`ARC08-02` §4) `[CANONE — DM 2026-10-19, D17]` | E2 |
| Orda avanguardia in campo | 900 | E8 |
| Perdite orda | **−900 effettivi** (~500 morti + ~400 dispersi in rotta, non si ricongiungono) | D11; state.md §2.2 |
| Fine battaglia | **Day 19** del March Clock (= caduta di Terrelton, sync ARC-09) | E3 |
| Livello party | 13 in ingresso, **13 consolidato** in uscita (D9 — mai il 14° qui) | E4/D9 |

**Conseguenze immediate**:

- I 4 PG nominati **Custodi Eterni** da Re Thorek (E5) + **Cerimonia
  delle 100 Asce** (Giorno 21, scena già scritta — `Cerimonia-delle-100-
  Asce.md`, D3: NON riscriverla).
- **Lythiel Alar-Wen** (Sacred Forest, E7) consegna la Ghianda a Hella
  alla Cerimonia (hook ARC-09).
- Hammerfist **consolida il 13°** dominio nanico del Vale.
- La compagnia ranger di **Lunapiena** (indipendente, D13) resta di
  presidio a Hammerfist — NON parte per Rethmar.

**Handoff ai tracker (già propagato)**:

- `state.md` §2.2: orda principale ~9.000 attivi post-Day 19.
- `Armate-SINCRONIZZAZIONE-CAMPAGNA.md` §3 Day 19: −900.
- Le **150 lance di Re Thorek** NON sono promesse qui: partono per
  Rethmar SOLO se gli hook politici di ARC-09 riescono (D4).

---

## 2. ESITO ALTERNATIVO — Vittoria costosa

**Quando**: i difensori vincono, ma il prezzo è più alto del default
(tiri di dado sfavorevoli nel finale, obiettivi del flashback mancati —
vedi §5 bonus non maturati).

**Soglia** (canone del DM 2026-10-18): **meno di 50
superstiti** invece di 90, contati dal Registro PFU delle unità naniche
(`ARC08-03`) `[CANONE — DM 2026-10-19, D17]`, e/o **Re Thorek muore** nel
finale: a 8 pf nell'Incontro 3B, tira Guarigione CD 25 a ogni round finché
nessuno lo cura per magia, e **al terzo fallimento muore**
(`ARC08-01-GUIDA-DM.md`, «Prove Mediche») `[CANONE — DM 2026-10-19, D12]`.

**Varianti da applicare**:

| Elemento | Variante vittoria costosa |
|---|---|
| Superstiti nani | <50 (invece di 90) → Hammerfist può presidiare ma non proiettare forza |
| Re Thorek | **Morto** → la Cerimonia delle 100 Asce è officiata da **Madre Superiora Dana** (o da Thorin Runaforte pregen se Dana è caduta, D14); il riconoscimento dei Custodi Eterni avviene comunque, per volontà testamentaria del re |
| 150 lance di Re Thorek | Il flusso politico (D4) si **complica**: senza il re, l'erede/consiglio nanico è più esitante → hook ARC-09 con CD Diplomazia +2 |
| Cerimonia | Tono più cupo; il Giuramento delle 90 diventa "Giuramento dei <50"; la runa dei Custodi ha peso funebre doppio |
| Perdite orda | Invariate (−900, D11): l'orda perde comunque l'avanguardia |

**Handoff ARC-09**: la vittoria costosa NON cambia i totali dell'orda a
Rethmar (l'avanguardia è comunque persa), ma **riduce o ritarda** i
rinforzi nanici opzionali (150 lance) e cambia il tono degli hook di
Thorik (lettera Brenna → il re a cui portare l'alleanza potrebbe non
esserci più).

---

## 3. CONTINGENZA — Caduta di Hammerfist

**Quando**: i difensori NON reggono (fallimento sistematico nel finale;
i Rumbling Stones arrivano troppo tardi o vengono sopraffatti).

> ⚠️ **Questo ramo NON è il default e rompe le assunzioni di ARC-09.**
> Se il DM lo gioca, ARC-09 va rinegoziato al tavolo. Resta comunque
> una linea narrativa viva, non un "game over".

**Cosa accade**:

- **Evacuazione per i Passaggi Antichi**: i superstiti fuggono dal
  tunnel segreto (mappa già esistente — `Mappe/Hammerfist-L3-REVISED-
  Ultra-Clear.md`, MAPPA H3-1 / master `Atlante-Hammerfist-Mappe-
  COMPLETE.md` MAPPA 3X-3Y-3Z-5). La regia dell'evacuazione è già
  pronta come scena.
- **La Mano Rossa guadagna una base**: Hammerfist Holds cade in mani
  nemiche → l'orda ottiene una fortezza nel North Wall, controllo dei
  passaggi montani, e le fucine naniche.

**Delta sui tracker (scenario caduta)** (canone del DM 2026-10-18):

| Tracker | Default (vittoria) | Caduta |
|---|---|---|
| Perdite orda Day 19 | −900 | **~−300** (l'avanguardia vince, subisce solo perdite d'assalto) → l'orda avanza su Rethmar con ~600 unità in più rispetto al default |
| Custodi Eterni / Cerimonia | Sì | **No** (Re Thorek morto o in fuga; la Cerimonia non avviene o è un lutto in esilio) |
| Lythiel → Ghianda a Hella | Alla Cerimonia (E7) | **Rilocare**: Lythiel consegna la Ghianda durante l'evacuazione o più avanti nel Vale |
| 150 lance | Condizionale (D4) | **Perse** (Hammerfist non esiste più come alleato) |
| ARMATE-SYNC ARC-09 | Baseline | Orda a Rethmar **+600 circa**; morale nanico del Vale a picco |

**Hook**: la riconquista di Hammerfist può diventare una sotto-quest di
ARC-09/10; l'uovo di Fauci (ARC-07 C3) e Fauci stesso (§4) trovano qui
un covo naturale.

---

## 4. RAMI DI FAUCI DI PALUDE (D10) + gancio carry-over (A12)

La sorte di Fauci **non è un fatto**: è un ramo condizionale, identico
in tutti i tracker (piano ARC-08 A1, D10). Vale in **ogni** scenario
d'esito sopra.

| Ramo | Trigger | Effetto |
|---|---|---|
| **Default — fugge** | Fauci scende sotto i **50 pf** e nessuno lo blocca attivamente (soglia di ritirata **alzata** se nel P5 Skullcrusher fuggì — valore in §4.1/tabella B4) | Decolla gravemente ferito verso le montagne meridionali; rimosso dall'assedio ma **vivo**; può tornare come nemesi (hook ARC-10; carta S2 proposta all'EVENT-DECK di Rethmar — vedi §6.3). Nessun cambio ai totali orda |
| **Alternativo — ucciso** | I PG lo portano a 0 pf prima che fugga: lo inseguono in volo, o lo tengono a terra. La presa di Orion da sola non basta, perché la lotta è contrapposta e Fauci ha +43 (SRD) | Morto; **−1 drago** nel pool di Rethmar (`state.md` §2.3 Conditional Additives) |

### 4.1 Carry-over dall'eredità di Skullcrusher (A12, [CROSS-ARC con ARC-07])

I **numeri di partenza** di Fauci (statblock `ARC08-02-SCHEDE-
PERSONAGGI-REGOLAMENTO.md` §1) sono modificati dall'esito del duello con
l'antenato **Skullcrusher** nell'ARC-07 P5 ("la Forgia ricorda le
ferite"). La tabella di carry-over è stata **consegnata e validata dal
DM (2026-07-03)**: **`07_.../PortaleForgia-P5-B4-CARRYOVER-Forgia-
Ricorda.md`** è la **fonte unica dei valori** — qui si dà solo la mappa
qualitativa (nessun valore duplicato, per non divergere).

| Esito del duello P5 (Skullcrusher) | Effetto su Fauci a Hammerfist (sintesi — valori nella tabella B4) |
|---|---|
| **Skullcrusher ucciso** | *Cicatrice ancestrale*: Fauci entra in campo con **PF ridotti** e **Presenza Terrificante meno efficace** contro i portatori d'artefatto |
| **Skullcrusher ferito grave** (fugge) | **−1 uso del soffio** (il primo Soffio a Cono indisponibile; prima linea a CD ridotta) |
| **Skullcrusher fuggito** (quasi illeso) | Fauci **vi riconosce** (+2 iniziativa, niente sorpresa) ma **morale fragile** → soglia di ritirata **alzata** (fugge prima) |
| **Ferite ancestrali segnate (N≤3)** | I portatori d'artefatto scelgono **+N al colpire** *oppure* **+Nd6 danni** contro Fauci; cicatrice fisica su un'ala = **−Volare** + bonus a colpirlo in volo |
| **Gancio inverso — Aegis Fang** | Quando Fauci entra in scena, Aegis Fang "canta" → **Thorik +2 di circostanza** contro Fauci e preavviso del primo soffio |

**Se il gruppo NON ha giocato il P5**: usa lo statblock di `ARC08-02`
§1 **invariato** (nessun carry-over). L'applicazione va fatta **prima
della battaglia** leggendo la tabella B4.

**Pf di partenza nella Sessione 4** `[CANONE — DM 2026-10-19, D9]`: 337
meno il carry-over qui sopra; **337 se il P5 non è stato giocato**, come dice il paragrafo qui sopra.
Il duello coi PG è ai round 21-23, dopo la picchiata dei round 18-20, in
cui Fauci prende Thorik in bocca e lo lascia cadere (`ARC08-02` §1, «La
presa di Thorik», `[CANONE — DM 2026-10-19]`; `ARC08-01-GUIDA-DM.md`, Incontro 4A): i due rami della tabella di §4 sono
i due esiti possibili di quel duello.

### 4.2 Che cosa sa il cavaliere, e se lo divinano `[CANONE — DM 2026-10-19, D15]`

Il cavaliere di Fauci (Guerriero 6 / Guardia Nera 4, scheda in `ARC08-02`
§1 e `ARC08-01`) resta in sella finché Fauci vola, e sotto i 30 pf,
disarcionato e col drago lontano, combatte fino alla morte. Lo si
interroga solo se lo prendono vivo: incosciente, legato, o con un
incantesimo. È una Guardia Nera e non parla per paura: servono *charme*,
*dominare* o *zona di verità*, e il suo TS Volontà è +6 (scheda).

**Tre cose che sa:**

1. **Dove va Fauci se fugge**: verso le montagne meridionali (§4; `ARC08-02`
   §1, *Esito della battaglia*). Il punto preciso della tana i file non lo
   danno `[INFERRED — needs DM confirmation]`.
2. **A cosa serviva l'avanguardia**: tenere chiusi i nani a nord mentre
   l'Orda prende Terrelton, lo stesso Day 19, e poi scende verso Rethmar
   (`09_…/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md`, Day 19).
   Che il cavaliere conosca il piano oltre Terrelton è una deduzione
   `[INFERRED — needs DM confirmation]`.
3. **Perché Fauci vuole Thorik**, e perché prima di finirlo lo prende in
   bocca (`ARC08-02` §1, «La presa di Thorik»): è della stirpe di Skullcrusher e odia
   chi porta le armi dei nani (`ARC08-02` §1, Odio della stirpe;
   `Bestiario/villain/Fauci_di_Palude.md`). Dell'uovo di Fauci (ARC-07 C3)
   il cavaliere non sa niente: è un'eco per ARC-10, e resta coperta
   `[INFERRED — needs DM confirmation]`.

**Se lo divinano** *(una riga per segreto: chi lo rompe, cosa ottiene, come
prosegue il modulo; `skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md` §9)*

| Segreto | Chi lo rompe | Cosa ottiene | Come prosegue |
|---|---|---|---|
| **Fauci in fuga, dov'è** | Lo *scrutare* di Hella (SRD): Fauci tira Volontà +19 contro la CD della sua scheda. L'hanno visto da vicino (nessun modificatore di conoscenza); con una **scaglia** strappata in battaglia il TS ha −10 (parte del corpo, SRD) | Lo vede ferito e a terra, nelle montagne meridionali; il posto i file non lo descrivono `[INFERRED — needs DM confirmation]` | La carta S2 (§6.3) si può anticipare: i PG lo cacciano prima di Rethmar, e se lo uccidono vale il ramo «ucciso» di §4 (−1 drago a Rethmar) `[INFERRED — needs DM confirmation]` |
| **Tornerà?** | La **Corona** di Thorik: *comunione* una volta al mese da un Nodo (`campaign/state.md` del ramo di gruppo, Corona di Adamantio) | Moradin risponde sì o no, una domanda per livello dell'incantatore (SRD); il livello della comunione della Corona i file non lo danno `[INFERRED — needs DM confirmation]` | Se chiedono del ritorno, la risposta segue la carta S2 (§6.3): se il DM la tiene nel mazzo, è «sì» `[INFERRED — needs DM confirmation]`. Il modulo non cambia; il tavolo sa che il conto è aperto |
| **Che cosa sa il cavaliere** | *Zona di verità*, *charme*, *dominare*, *parlare con i morti* se è caduto | Le tre cose qui sopra; con *parlare con i morti* risponde col TS Volontà +6 (SRD) | Nessuna scena nuova: le tre risposte agganciano §4 e §6.3 |

---

## 5. TABELLA DI CONVERSIONE D9 — flashback pregen → bonus al finale

> **Il cuore meccanico di D9/D6.** Le sessioni giocate coi pregen "Eroi
> di Hammerfist" (Sessioni 1-2 + prima metà della 3) **NON danno PX ai
> Rumbling Stones** (D9). Ogni obiettivo raggiunto produce invece un
> **bonus concreto e quantificato** che matura per il finale dei PG
> reali. I bonus sono **posizioni, PNG vivi, risorse, −CR a un incontro,
> intel** — MAI esperienza.

**Come si usa**: durante ogni sessione pregen, il DM segna quali
obiettivi sono stati raggiunti (pieno / parziale / fallito). Alla
riemersione dei Rumbling Stones (B2, ponte d'arrivo), si sommano i bonus
maturati e si applicano al finale.

### 5.1 Sessione 1 — Ricognizione (pregen)

| Obiettivo | Pieno | Parziale | Fallito |
|---|---|---|---|
| **Ricognizione della colonna** (skill challenge, `ARC08-04-MARCIA-MANO-ROSSA.md`) | Intel completa: i Rumbling Stones conoscono composizione e posizioni nemiche → **+2 iniziativa di massa** nel finale + **−1 sorpresa** nemica | Intel parziale: solo composizione, non posizioni → +1 iniziativa di massa | Allarme dato: nemici allertati → **nessun bonus**, +50 rinforzi orda nel finale |
| **Difese preparate** (trappole di 1D e della Preparazione) | Baliste piazzate + trappole pronte → **1 ondata nemica affronta un −2 CA da terreno preparato** nel finale | Metà difese → bonus dimezzato (1 uso) | Difese non pronte → nessun bonus |

### 5.2 Sessione 2 — Assedio (pregen)

| Obiettivo | Pieno | Parziale | Fallito |
|---|---|---|---|
| **Breccia contenuta** (Assedio Mura) | La fortezza regge più a lungo → **1 incontro del finale a −1 CR** (meno nemici filtrati all'interno) | Breccia rallentata → mezzo bonus (−1 CR a un solo round) | Breccia aperta subito → il finale inizia con **+1 ondata** |
| **Comandanti nemici logorati** (Grimjaw / Gorthak feriti durante l'assedio) | Grimjaw e/o Gorthak arrivano al finale **feriti**: −20% pf iniziali, −2 morale all'orda | Uno solo dei due logorato | Entrambi freschi al finale |
| **Cantitrici della Pietra protette** (Soffio del Drago) | Le Cantitrici sopravvivono → nel finale forniscono **Cura Ferite Gravi di Massa 1/incontro** + Ispirare Coraggio ai 90 | Metà Cantitrici → un solo uso di cura | Cantitrici perse → nessun supporto divino di massa nel finale |

### 5.3 Sessione 3a — Ultima Resistenza (pregen, fino al passaggio di testimone)

| Obiettivo | Pieno | Parziale | Fallito |
|---|---|---|---|
| **Posizioni difensive tenute** (ritirata ordinata al Cuore della Montagna) | I 90 arrivano al finale **in formazione** → cuneo di carica ottimale, +2 morale iniziale | Ritirata caotica → formazione ma senza bonus morale | Rotta → i 90 iniziano il finale **shaken** (−2), la carica costa un round in più |
| **Re Thorek stabilizzato** (Thorin Runaforte lo tiene in vita) | Re Thorek vivo a 8 pf per la riscossa (E6, default) → pronuncia il discorso della carica finale (+4 morale) | Thorek incosciente ma vivo → nessun discorso, +0 | Thorek muore prima della riemersione → **ramo vittoria costosa** (§2) |
| **Evacuazione dei civili/feriti** (Passaggi Antichi) | Tutti evacuati → nessun ostaggio, i PG combattono liberi | Evacuazione parziale → 1 round del finale speso a proteggere feriti | Evacuazione fallita → il finale ha un obiettivo secondario "proteggi i feriti" sotto pressione |

### 5.4 Regola di somma

- I bonus si **sommano** (sono cumulativi tra obiettivi diversi).
- Un flashback giocato **alla perfezione** (tutti "pieno") produce il
  finale del **default** (§1, vittoria piena): E1-E8.
- Un flashback **mediocre** (mix parziale/fallito) spinge verso la
  **vittoria costosa** (§2).
- Un flashback **disastroso** (molti "fallito") mette in gioco la
  **caduta** (§3) — ma i Rumbling Stones al finale possono ancora
  ribaltarla: è il loro momento (E6).
- **In nessun caso** questi bonus diventano PX (D9). Il finale assegna
  PX da APL 13 dosati a parte (`ARC08-01-GUIDA-DM.md` Appendice C /
  `hammerfist_encounters-...-final.md` §RIASSUNTO XP).


### 5.4-bis Se l'assedio si gioca con il libretto `[CANONE — DM 2026-10-21]`

L'assedio dei pregen si gioca con il libretto della battaglia campale
(`ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md`, ADR-0096). Le sessioni coi pregen
sono tre. La **Sessione 1** è l'avvistamento, col libretto spiegato a pezzi,
e finisce con la scaramuccia dell'avanguardia (libretto §13): le squadre di
guastatori dei pregen scavano trappole sul pendio finché l'orda non le
scaccia. È scritta nel master `ARC08-DEF-1-OMBRA-SULLA-MONTAGNA.md`, e la sua
**tabella delle leve** (§7) dice cosa porta ogni esito della serata
nell'assedio e in quale riga di questa tabella. Seguono la **Sessione 2** e
la **Sessione 3a**.

- **Ricognizione della colonna** si legge come sopra.
- **Difese preparate** si legge dalle trappole portate a casa: 6 o più
  «pieno», 3-5 «parziale», meno di 3 «fallito». Ogni trappola annulla anche
  una tacca del Giorno 1 o del Giorno 2 d'assedio. Contano le trappole
  dell'avanguardia e quella della Preparazione delle difese.
- Le righe di §5.2 e §5.3 si leggono con la tabella di `ARC08-19` §4
  (brecce dei giorni 1 e 2, comandanti fuggiti feriti, Mura del giorno 2,
  reparti vivi alla ritirata). Nell'assedio i comandanti non muoiono: sotto
  metà dei punti ferita fuggono, così arrivano al finale feriti come vuole
  §5.2. Re Thorek e l'evacuazione restano come sopra.

### 5.5 Se il flashback coi pregen non è stato giocato `[INFERRED — needs DM confirmation]`

Sul ramo di gruppo l'Arco 08 non è giocato, né le sessioni coi pregen né il P5
(`campaign/state.md` §0). Finché il DM non decide se giocarli, il finale parte
da qui:

- **Re Thorek stabilizzato**: riga «pieno», cioè il default E6. Re Thorek è a 8 pf per la riscossa.
- **Tutte le altre righe** di §5.1-§5.3: «parziale».
- **Comandanti logorati**: Grimjaw e Gorthak sono vivi; Grimjaw è quello logorato (−20% pf iniziali).
- **Cantitrici**: metà, un solo uso di cura.
- **P5 non giocato**: statblock di Fauci invariato, e in Sessione 4 Fauci parte da 337 pf (§4.1) `[CANONE — DM 2026-10-19, D9]`.

---

## 6. Conseguenze a lungo periodo (C2)

> Formato echi ARC-09 (`09_.../...DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md`):
> **evento → eco → quando riemerge → file che lo gestisce**, con
> varianti per ramo d'esito. Nessun eco contraddice gli HOOKS ARC-09.

### 6.1 Tabella degli echi

| Evento a Hammerfist | Eco | Quando riemerge | File che lo gestisce |
|---|---|---|---|
| **Fauci di Palude fugge ferito** (ramo default D10) | Nemesi draconica: il drago torna per vendetta contro Thorik/la Corona | Rethmar (carta S2 all'EVENT-DECK, §6.3) o ARC-10 | `ARC08-10` §4; EVENT-DECK ARC-09 (S2, §6.3) |
| **Uovo di Fauci** (eco gemella, ARC-07 C3) | Un secondo drago nero cresce nell'ombra — semina per ARC-10 | ARC-10, qualunque sia l'esito ARC-08 (`07_…/ARC07-CONSEGUENZE-ECHI.md`, Echo ledger) | ARC-07 C3 (fonte); da agganciare alla stessa carta S2 |
| **Fauci ucciso** (ramo alternativo D10) | −1 drago a Rethmar; nessuna nemesi (ma l'uovo resta) | Day 42 Rethmar | `campaign/state.md` §2.3 |
| **Runa dei Custodi Eterni** (Cerimonia Atto 3) | Status sociale presso i nani del Vale (§6.2) | Ogni interazione coi nani in ARC-09/10 | `Cerimonia-delle-100-Asce.md` §2; questa §6.2 |
| **150 lance di Re Thorek** (D4) | Rinforzo condizionale a Rethmar | Day 42, se gli hook politici riescono | `state.md` §2.5; `Bestiario/png/Khorn/Khorn.md`; HOOKS-Thorik |
| **Eroi di Hammerfist pregen** (D14, se sopravvivono) | Borin campione / Dara staffette / Thorin culto / Nala a Dauth | Sparsi in ARC-09 | schede `PNG/Borin_...`, `PNG/Dara_...`, `Bestiario/png/Thorin_Runaforte.md`, `PNG/Nala_...` |
| **Raid drow al tempio di Hammerfist** (Sonjak, `state.md` §3) | Prefigura la Fase 0 (Notte dei Drow) di Rethmar | Day 40, Fase 0 Rethmar | `state.md` §3; ARC-09 FASE0 |
| **Lunapiena resta di presidio** (D13) | Hammerfist difesa, ma NON rinforza Rethmar | Statico | `Bestiario/png/Capitano_Lunapiena.md`; ARMATE-SYNC §7 |

**Varianti per ramo d'esito**: nella **vittoria costosa** (Re Thorek
morto) la runa dei Custodi ha peso funebre doppio e il canale delle 150
lance è più freddo (§2); nella **caduta** (§3) la maggior parte di
questi echi decade (niente Cerimonia, niente runa, lance perse) e
subentra l'eco "Hammerfist in mani nemiche" (base per una riconquista in
ARC-09/10).

### 6.2 Runa dei Custodi Eterni — quantificata

La runa di pietra che Re Thorek consegna ai 4 PG (Cerimonia Atto 3;
5 cm, al collo) non era mai stata quantificata meccanicamente.

**Effetto** (canone del DM 2026-10-18):
- **+2 di circostanza a Diplomazia** con i nani del Vale (e con chi
  riconosce il titolo di Custode Eterno) mentre la runa è portata a
  vista.
- **Ospitalità a Hammerfist**: vitto, alloggio, accesso all'armeria
  della cittadella e alle fucine (aggancio al tesoro `ARC08-13` §3) a
  costo nullo. Il tetto dell'armeria è quello del banco: oggetti
  perfetti e consumabili già in magazzino, niente magia su misura
  (`ARC08-17` §2-§3) `[INFERRED — needs DM confirmation]`.
- **Riconoscimento** da PNG nanici in ARC-09 (es. Maewen riconosce
  Tordek "dalla runa di Custode Eterno" — già canonico in `state.md`
  §4): la runa è il segno visibile.
- **NON** è un oggetto magico: nessun bonus numerico in combattimento;
  non commerciabile (valore 0 mo nel WBL, `ARC08-13` §3).

### 6.3 Carta-evento proposta per l'EVENT-DECK di Rethmar (solo hook)

Per il ramo **"Fauci fugge"** (default D10), proposta di carta S2 (echi
di campagna) da aggiungere a
`09_.../Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-EVENT-DECK.md`:

> **"Il Ritorno di Fauci di Palude" [S2 — eco di campagna]**
> — Spotlight: **Thorik**. Se Fauci è fuggito da Hammerfist (non
> ucciso), può ricomparire come minaccia aerea a Rethmar (o come
> nemesi ARC-10). Riusa lo statblock di `ARC08-02` §1 (col carry-over
> ARC-07 B4 applicato, §4.1). Eco gemella: l'**uovo di Fauci**
> (ARC-07 C3). *Qui solo l'hook e il puntatore*: la scrittura piena
> della carta è compito dell'EVENT-DECK ARC-09, non di questo file.

---

---

## 7. Riepilogo — cosa aggancia cosa

| Esito | Superstiti | Re Thorek | Perdite orda | Custodi/Cerimonia | 150 lance | ARC-09 |
|---|---|---|---|---|---|---|
| **Vittoria piena** (default) | 90 | Vivo (8 pf) | −900 | Sì | Condizionale (D4) | Baseline E1-E8 |
| **Vittoria costosa** | <50 | Morto | −900 | Sì (officiata da Dana) | Complicate (+CD) | Hook Thorik cambiano tono |
| **Caduta** | Sparsi | Morto/in fuga | ~−300 | No | Perse | Orda +600 a Rethmar; rinegoziare |

Il ramo di Fauci (§4) e i bonus del flashback (§5) si applicano
**trasversalmente** a tutti e tre.
