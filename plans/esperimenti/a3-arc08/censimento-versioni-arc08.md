# Censimento delle versioni — ARC-08, La Battaglia di Hammerfist

Analisi in sola lettura, 2026-10-16, branch `claude/project-thread-e860p0`
(HEAD b79fcee2). Nessun file del repo è stato toccato. Le righe sono quelle
del branch a quella data. Percorsi relativi a `08_La Battaglia Di Hammerfist/`
salvo dove indicato. Abbreviazioni: **01** = `ARC08-01-GUIDA-DM.md`,
**02** = `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`, **enc** =
`hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md`,
**COMPLETE** = `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`, **L1/L2/L3** =
`Mappe/Hammerfist-L{1,2,3}-REVISED-Ultra-Clear.md`, **Lotto-N** =
`Mappe/_ARCHIVIO/Hammerfist-Lotto-N-*.md`, **DEF-5** =
`07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md`.

La regola applicata, come chiesto dal DM: **un file si archivia solo se
nessuna sua sezione o mappa è la versione migliore**. Per questo la tabella
per sezione (§2) viene prima della proposta, e la proposta (§1) ne discende.

> ⚠️ **PR #241 non è in questo branch.** Tempestas risulta ancora Bardo 12 /
> Arcimago 2, PF 84, GS 14 in 01:443-462 e 02:388-410. Ogni confronto su
> Tempestas va rifatto dopo il merge di #241.

---

## 1. File per file

Date dalla storia git (`git log --follow`): prima versione → ultima modifica.

| File | Ruolo | Data | Dim. (byte/righe) | Superato da | Contenuto unico (righe) | Proposta |
|---|---|---|---|---|---|---|
| `ARC08-00-INDICE.md` | indice dell'arco | 2026-07-02 → 10-07 | 9828/176 | — | tutto (è l'indice) | **TENERE** vivo. Da aggiornare: riga 23 «tavolo all'ARC-07 Piano della Terra» (A18); «Ultima revisione 2026-07-02»; §4 dichiara canonici anche `enc` e i due ERRATA |
| **01** | master narrativo: PNG, pregen, eserciti, sessioni 1-4, appendici, schede | 2025-12-29 → 10-03 (r1) | 183231/3495 | nessuno | PNG con liste incantesimi complete e talenti di Thorek (147-466); pregen completi, talenti, equipaggiamento, momenti eroici (488-619); bonus di transizione permanenti (624-631); statistiche **di creatura singola** per ogni unità (677-942, assenti in 02); tutte le sessioni (944-3007) con 1B «Consiglio di guerra» (1106-1135), Élite 2A-2E (1433-1585), **2F Incrocio Silenzioso** (1808-1896, l'unico nello stile attuale), le tre righe dell'errata epica (948-959, 2243-2252, 2757-2765), nota carry-over A12 (1153-1163); appendici A-E (3193-3375) | **FONDERE** nei master S1 (DEF-1..4, righe 140-143 del piano). Non archiviabile |
| **enc** | guida agli scontri, generazione parallela della 01 | 2025-12-29 → 07-02 | 56258/1438 | 01 per circa due terzi (222 righe identiche; dopo il confronto fuzzy restano 168 righe significative senza corrispondenza) | **1B «La preparazione delle difese»** intero (136-235: mappa dei bastioni, quattro attività dei pregen con CD ed esiti, eventi collaborativi); **2A in tre fasi** (241-427: bombardamento con azioni dei pregen per round, 40 berserker + 20 veterani + **2 troll rigeneranti**, ritirata, tre mappe); LS e PE di ogni incontro (1A LS 12, 1B LS 10, 2A LS 15, 2B LS 18, 3A LS 16, 4A LS 20); 1A: posizioni iniziali ed eventi dinamici round 1-7 (78-127); read-aloud dei round 9 e 10 di 3A (802, 805); **epilogo**: discorso di Thorek (1320), discorso del PG guerriero (1322-1323), addii degli alleati come tre citazioni (1327-1334), semi d'avventura (1350-1354); **appendice XP**: bonus per il finale di sessione (1373-1384) e «Nota di verifica EL» (1399-1408, richiamata dalla 01) | **FONDERE** le parti uniche in DEF-1..4, **poi ARCHIVIARE**. ⚠️ Prima, decidere la revisione in sospeso `plans/scrittura/revisioni-pilota-ARC08/REVISIONE-hammerfist_encounters-r1.md` (1501 righe, non applicata) |
| **02** | schede PNG/unità + regolamento di massa da tavolo | 2025-12-29 → 07-03 (A12) | 40915/802 | — | errata B5 applicati (92, 141-147); banner carry-over e ramo D10 su Fauci (67-73, 105-119); Gorthak «Tre teste» e Furia sotto 97 PF (204-212); **scheda completa di Lunapiena** (325-357); tattiche di Ventolesto, Orion, Tempestas; regolamento di massa (527-569); **Appendice A danni strutturali** (574-611); unità in AU/DU/PFU con **capacità speciali** assenti nella 01 (616-802) | **TENERE** come materiale comune (piano, righe 145-149). È la fonte a cui puntano le schede del Bestiario di Fauci, Grimjaw, Lunapiena e dei pregen |
| `ARC08-03-REGISTRO-PERDITE.md` | foglio di tracciamento PFU | 2025-12-29 → 10-12 | 14652/269 | — | tutto (strumento) | **TENERE**. Letto solo in testa |
| `ARC08-04-MARCIA-MANO-ROSSA.md` | logistica della colonna | 2026-04-03 → | 6495/128 | — | tutto; §3-bis rimanda al read-aloud dell'orda in 01:948-959 | **TENERE**. Letto solo in testa |
| `ARC08-10-ESITI-E-CONTINGENZE.md` | esiti, ramo D10, carry-over §4.1 | 2026-07-02 → 07-10 | 17606 | — | tutto | **TENERE**. Letto solo in testa |
| `ARC08-11-PONTE-ARRIVO.md` | giunzione pregen → PG (lato ARC-08) | 2026-07-02 → 09-21 | 7235 | in parte da DEF-5, che ne è il lato ARC-07 e la dichiara «già scritta» | tutto il lato ARC-08 | **TENERE**. Revisione r1 in sospeso in `plans/scrittura/revisioni-pilota-ARC08/` |
| `ARC08-12-CRONOLOGIA-MARCH-CLOCK.md` | cronologia unica | 2026-07-02 | 4255 | — | tutto | **TENERE** |
| `ARC08-13-TESORO-WBL-AUDIT.md` | tesoro e WBL | 2026-07-02 | 5243 | — | tutto | **TENERE** |
| `ARC08-14-ATLANTE-IMMAGINI.md` | indice delle immagini | 2026-07-02 | 6616 | — | tutto; coda C3 aperta (14 immagini senza prompt, rinomina) | **TENERE** |
| `ARC08-15-HANDOUTS-GIOCATORE.md` | handout | 2026-07-02 | 8342 | — | tutto | **TENERE**. Revisione r1 in sospeso |
| `ARC08-16-CUE-SONORI.md` | cue sonori (ADR-0018) | 2026-08-23 | 7291 | — | tutto | **TENERE** |
| `ARC08-17-BANCO-HAMMERFIST-1372.md` | il banco (D41/D42) | 2026-10-07, stato «Proposta» | 16614 | — | tutto | **TENERE**. Contraddice 01:2974-2978, 01:3264 ed enc:1338-1342 (50.000 mo e feudo) |
| `Cerimonia-delle-100-Asce.md` | evento canonico finale, Day 21 | 2026-05-04 → | 18603/207 | — | tutto | **TENERE**, componente di DEF-4 da non riscrivere (Q2 del piano). Revisione r1 in sospeso |
| `mass_combat_guide_Dm.md` | fonte normativa del sistema di massa (C1) | 2025-12-29 → | 20449/663 | — | tutto; variante 2d6 | **TENERE**. ⚠️ Rimando circolare: dice «tabella completa in 02 §4» (riga 31), mentre 02 dice che la fonte è lui |
| `combat_prompts_guide.md` | cinque prompt LLM per **generare** il sistema di massa | 2025-12-29 → 2026-01-07 | 4820/142 | `mass_combat_guide_Dm.md`, che ne è il prodotto | nessun contenuto di gioco. ⚠️ Non sono prompt d'immagine, come scrive il piano (riga 152), e in `campaign/ai-media-prompts/` non ci sono | **ARCHIVIARE** (storico di lavorazione) |
| `PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA.md` | stub che punta al piano in `plans/` | — | 213 | `plans/PIANO-REVISIONE-ARC08-…` (592 righe) | nessuno | **ARCHIVIARE** |
| `ERRATA-ARC08-35-Verification.md` | registro della verifica 3.5 (B5) | 2026-07-02 → 07-03 | 5944/124 | — | il registro delle decisioni 3.5 (soffio a cono come house-rule, Punire e Aura corretti) | **TENERE fino a DEF-1**, poi ARCHIVIARE. Applicato in 02 ma **non in 01:204-205** (vedi §4) |
| `ERRATA-ARC08-DESCRIZIONE-EPICA.md` | riconciliazione con il testo del DM | 2026-08-23 | 9663/186 | — | registro della decisione «Thorek non muore», della glossa khuzdul e di Orion ≠ Hella; §6 «debito dichiarato» (riscrittura dei riquadri 3C e 4C) | **TENERE fino a DEF-3/DEF-4**, poi ARCHIVIARE. Tutte le correzioni risultano applicate (§4) |
| `ARC08-90-DEPRECATO-battle-stats-maps.md` | atlante, generazione a | 2025-12-29 → 07-02 | — | 91 ⊂ 92 ⊂ COMPLETE | nessuno. L'unica riga assente nel 92 («SCOPO», 90:104) è anche in 91:146 ed è coperta da COMPLETE:258 | **ARCHIVIARE** |
| `ARC08-91-DEPRECATO-atlante-visivo-v2.md` | atlante, generazione b | 2025-12-29 → 07-02 | — | 92 ⊂ COMPLETE | il banner che dice che l'«Appendice di Gioco Definitiva» non è mai stata scritta, solo nota storica | **ARCHIVIARE** |
| `ARC08-92-DEPRECATO-atlante-visivo-v3-complete.md` | atlante, generazione c | 2025-12-29 → 07-02 | — | COMPLETE (descrizioni, tattica) | **prompt d'immagine** che COMPLETE non contiene (si dichiara «fonte dei prompt» ma ha solo la 3Y, 943-945): MAPPA 1 (92:129), 2A isometrica (92:182), 2B frontale (92:212), MAPPA 4 danni (92:262), 2B-Corretta (92:316), 3X (92:363), 5 (92:469), 4X (92:514), 4 finale (92:545); 1A-1 (92:56), 1A-2 (92:88) e 3Z (92:430) esistono altrove solo parafrasati. Due read-aloud «dal Manuale»: fortezza (92:172), 3X (92:360) | **MIGRARE** i prompt e i due frammenti (in COMPLETE o in `campaign/ai-media-prompts/09_ARC08_battaglia-hammerfist.md`), **poi ARCHIVIARE** |
| `ARC08-93-DEPRECATO-sessione-interrotta.md` | stub in inglese | 2026-04-03 | 1399/22 | — | nessuno | **ARCHIVIARE** |
| **COMPLETE** | master visivo e narrativo delle 17 mappe | 2025-12-29 → 10-03 | 64269/1444 | — | descrizioni di scena, immagini, matrice A8 (21-61), guida all'uso, stile artistico | **TENERE** |
| **L1** | master tattico della Sessione 1 | → 2026-10-08 | 649 righe | — | griglie 1A-1, 1A-2, 1A-3 | **TENERE** |
| **L2** | master tattico della Sessione 2 | → 2026-10-08 | 693 righe | — | griglie 2A (con 2B e 2C come viste), 1, 2, 3, 4, 2B-Corretta | **TENERE** |
| **L3** | master tattico delle Sessioni 3-4 | → 2026-10-08 | 656 righe | — | griglie H3-1/3X, 3Y, 3Z, 5, 4X, 4 | **TENERE** |
| Lotto-1/2/3 + `README.md` | generazione storica delle mappe | archiviati il 2026-09-05 (D1) | 371/544/541 righe | L1/L2/L3 | nessuno di gioco. Lotto-3 ha un finale divergente, superato: Fauci muore per Aegis Fang, Thorik «Paladin» (440-492) | **già in `_ARCHIVIO`**, restano lì |

**Fuori dalla cartella.** Il controllo ha toccato `07_*`, `09_*`, `campaign/` e
`plans/`, esclusi `build/`, `.claude/` e i mirror.

- `07_…/ARC07-DEF-5-RITORNO-HAMMERFIST.md` (748 righe, master DEF) contiene
  già la **versione più nuova** dell'Apparizione e della Sfera (Incontro 3B
  e 3C della 01), con canone DM D38, D77 e D90 del 2026-10-03/15, e la mappa
  CM-1 del Cuore.
- `07_…/Mappe/ARC07-MAPPE-HAMMERFIST-372-1372.md` e
  `Mappe/hammerfist-372-1372/M7-{D,E,F}-*-1372.md` (2026-10-08) hanno le
  griglie del 1372 della ritirata e della riconquista: M7-E/1372 è «i passaggi
  antichi».
- `07_…/CORREZIONE-Boss-Fauci.md` (377 righe, r1 2026-10-03) è un secondo
  statblock di Fauci (GS 15/GS 12), da passare all'altro thread.
- `07_…/Mappe/_ARCHIVIO/TACTICAL-GRIDS-COMPLETE.md` (MAP 19) è citato come
  storico da 01:1894.

Nei piani, solo `PIANO-MASTER-DEF-…` (riga 151) dichiara fuori dai master
90-93, gli ERRATA, `combat_prompts_guide` e lo stub. Nessun piano dichiara
superati `enc` o la 01.

---

## 2. Sezione per sezione e mappa per mappa: dov'è la versione migliore

«Migliore» vuol dire la più aggiornata e dettagliata per l'uso al tavolo. La
terza colonna dice cosa hanno in più le altre: è quello che va migrato o
fuso prima di archiviare.

### 2.1 Mappe

Per ogni mappa contano due versioni: la **griglia** (L1/L2/L3) e la
**narrativa e immagine** (COMPLETE). Lo dichiara anche la matrice A8
(COMPLETE:21-61). Le mappe dentro 01 ed enc sono schizzi ASCII grossolani,
non griglie. Il confronto esatto riga per riga dei blocchi di codice dà 0-2
righe in comune con L1/L2/L3: sono disegni diversi, non copie.

| Mappa | Griglia migliore | Narrativa migliore | Cosa hanno in più le altre |
|---|---|---|---|
| 1A-1 Sentiero Nascosto | L1:335-533 (20×100, rocce, skill challenge) | COMPLETE:102-142 | 92: prompt (92:56). 01:985-1019 e Lotto-1:16-107: niente oltre L1 |
| 1A-2 Torrione di Vedetta | L1:18-334 (tre viste, coordinate, pattern di pattuglia) | COMPLETE:143-198 | 92: prompt (92:88) |
| 1A-3 Campo della Mano Rossa | L1:534-649 (40×50, 6 m/q, intelligence a soglie) | COMPLETE:199-248 | nessuna |
| enc «Valle dell'avvistamento» (enc:47-76) | **nessuna griglia corrispondente**: è una panoramica 120×80 m che unisce torrione, sentiero e pattuglia | — | enc:78-127: posizioni iniziali dei pregen, pattuglia di 5 orchi + sergente, 3 scout su worg, eventi dinamici round 1-7. **Da fondere in DEF-1** (testo, non la mappa) |
| enc «Bastioni di Hammerfist» per 1B (enc:142-179) | L2 2A (120×80) per la geometria | — | la mappa enc colloca i pregen nelle attività di preparazione 1B, che **esistono solo in enc** (181-235). Fondere il testo |
| MAPPA 1 Disposizione Giorno 1 | L2:372-531 (60×108, 3 m/q) | COMPLETE:251-308 | 92: prompt (92:129). 90 e 91 dicono «il nemico attacca da Nord verso Sud», che contraddice L2 e L3 (nemico da sud): superato, non migrare |
| 2A Fortezza dall'alto | L2:22-371 (griglia 120×80, legenda delle coordinate, sezione, prospettiva, punti deboli) | COMPLETE:309-376 | 92: prompt isometrico (92:182) e read-aloud «capolavoro di ingegneria nanica» (92:172). 01:1293-1376 («2-BIS») e 01:3111-3184: tre viste ASCII ora mappate su L2 VISTA 1/3/4 |
| 2B frontale / 2C laterale | L2:593-600 (= VISTA 4 e VISTA 3 di 2A, con modificatori e cadute) | COMPLETE:377-500 | 92: prompt 2B frontale (92:212) |
| MAPPA 2 Schieramento difensivo | L2:561-580 (tabella su coordinate 2A) | COMPLETE:501-569 | 01:1253-1292 e 01:3074-3110: schizzo con le postazioni PG, duplicato due volte nella 01 |
| MAPPA 3 Movimenti e fasi | L2:532-560 (rotte sulla griglia della MAPPA 1) | COMPLETE:570-678 | 01:1377-1408: schizzo. enc:241-427: **tre fasi per round con posizioni B/D/T/N** (round 1-3, 4-8, 9-12), che L2 non ha per round. Fondere il testo delle fasi |
| MAPPA 4 Evoluzione danni | L2:581-592 (pannelli A-C su coordinate 2A) | COMPLETE:679-769 | 92: prompt «tre schizzi» (92:262). 01:1409-1477: i tre pannelli, ora assorbiti da L2 |
| 2B-Corretta Attacco del drago | L2:601-693 (40×26, cono, opzioni PNG) | COMPLETE:770-841 | 92: prompt (92:316). enc:436-474 e 01:1589-1648: schizzi del round. «Zona d'impatto» identica in enc:497-521 e 01:1651-1675 |
| 3X / H3-1 Passaggi antichi, evacuazione | L3:22-162 (40×40, timeline dell'evacuazione) | COMPLETE:844-926 | **M7-E/1372 e M7-D/1372 in `07_…/Mappe/hammerfist-372-1372/`** (2026-10-08, generate da JSON): i livelli −1 e −2 della ritirata, che L3 non ha. 92: prompt (92:363) e read-aloud «il cortile è un inferno… statua» (92:360). «Ritirata verso il Cuore» identica in enc:590-612 e 01:1751-1773 |
| 3Y Ponte Sospeso | L3:163-253 (33×27) | COMPLETE:927-962 (con il prompt, migrato in A8) | nessuna |
| 3Z Incrocio Silenzioso | L3:254-357 (33×33, stalagmiti S1-S8) | COMPLETE:963-1049 | 01:1808-1896: **il testo dell'incontro 2F è il migliore** (stile attuale). 92: prompt solo parafrasato (92:430). Lotto-3:161-262 e `07_…/Mappe/_ARCHIVIO/TACTICAL-GRIDS-COMPLETE.md` MAP 19: storici |
| MAPPA 5 Cuore della Montagna | L3:358-493 (67×53, stati A-F, ondate) | COMPLETE:1050-1155 | **DEF-5 CM-1** (`07_…/ARC07-DEF-5…`:637-) per la scena dell'Apparizione: stessa geometria in scala 3 m (33×27), con il canone D38/D77/D90. ⚠️ **Due scale per lo stesso luogo** (L3 1,5 m, CM-1 3 m). 92: prompt (92:469). Gli schizzi delle ondate (enc:640-787 = 01:1999-2149) sono resi da L3 come stati B-D |
| 4X Campo finale, profilo | L3:494-508 (tabella delle quote) | COMPLETE:1158-1220 (illustrazione) | 92: prompt «inquadratura laterale» (92:514), **esiste solo nel 92** |
| 4 Battaglia finale aerea e terrestre | L3:509-656 (60×68, vista delle altitudini, stati A-E) | COMPLETE:1221-1342 | enc:1042-1063: «mappa aerea 3D» (solo 4 righe su 13 nella 01:2551-2565). Gli schizzi della carica (01:2768-2904 = enc:1161-1269) sono resi da L3 come stati B-E. 92: prompt «sciame di gufi» (92:545) |
| «Campo della Memoria» (4B) | L3:636-637 (stato E) | — | 01:2928-2946 = enc:1296-1312: **210 asce piantate sul campo**. Cerimonia: **100 asce** nella Sala di Pietra Antica. Possono stare insieme (il campo il Day 19, la sala il Day 21), ma nessun file lo dice → domanda D8 |

**Conclusione sulle mappe.** Nessuna mappa di 90, 91 e Lotto-1/2/3 è la
migliore. Il 92 non ha nessuna mappa migliore, ma ha **prompt e due frammenti
di read-aloud** che nessun file vivo contiene. Le mappe di 01 ed enc sono
schizzi superati da L1/L2/L3. Le uniche cose che portano in più sono le
**posizioni dei pregen per fase e round** (enc 1A, 1B, 2A) e il **testo
dell'incontro 2F** (01).

### 2.2 Incontri e sessioni

| Sezione | Versione migliore | Cosa hanno in più le altre |
|---|---|---|
| Apertura della Sessione 1, «l'orda si sente prima» | 01:948-959 (dall'errata epica) | — |
| 1A Ricognizione | 01:976-1105 (a fasi, rimandi a L1, obiettivi e conseguenze) | enc:41-135: LS 12/3.600 PE (la 01 dice «variabile 5-12»), posizioni iniziali, eventi dinamici round 1-7, azioni secondarie per pregen (95-110) |
| 1B | **due incontri diversi con la stessa sigla**: 01:1106-1135 «Consiglio di guerra» e enc:136-235 «Preparazione delle difese» | enc 1B esiste solo lì (attività, CD, esiti, eventi collaborativi Borin+Dara e Thorin+Nala). La 01 ha poi un 1C generico. → domanda D9 |
| 2A Assalto alle mura | per completezza enc:241-427 (tre fasi, troll, mappe); per il collegamento alle griglie 01:1207-1432 | enc: 6 giganti contro gli 8 di 01 e 02; troll rigeneranti presenti solo in enc |
| Élite 2A-2E (Gorthak, drago, duello dei comandanti, Cantitrici, «Soffio della Morte») | 01:1433-1585 | non sono in enc |
| 2B Soffio della disperazione | 01:1586-1807 (TS Riflessi, giusto per SRD; rimando a L2) | enc:430-626: iniziative speciali (482-490), LS 18/5.700 PE. ⚠️ enc:527 «Tempra CD 25» contro 01:1680 «Riflessi CD 25»; enc:532 «Forza CD 20» contro 01:1698 «CD 25» |
| 2F Incrocio Silenzioso | 01:1808-1896 | non è in enc |
| 3A Ultima resistenza | 01:1908-2166 (con L3). Le ondate dentro la 01 si contraddicono: 1986-1989 (50/30/20) contro 2038-2041 (30/20/15) | enc:632-819: LS 16/4.800 PE, read-aloud dei round 9 e 10 (802, 805) diversi dalla 01:2169-2171 |
| 3B/3C Apparizione e Sfera | **DEF-5 §3-§5** (`07_…`:189-497, canone DM fino al 2026-10-15). Effetti: +6 morale, Thorek stabilizzato a 8 pf ed esausto, Volontà CD 25 per gli orchi | 01:2167-2237 e 01:2304-2449 (= enc:821-955): versione vecchia, che il piano lascia a DEF-5. 01 e enc: Sfera 2d4+4 / CD 20; Lotto-3 e DEF-5: 2d8 / CD 25 |
| 3D Vendetta dei nani | 01:2238-2303 (con il veterano dell'errata, 2243-2252, e la glossa giusta a 2240) | — |
| 4A Battaglia aerea | 01:2457-2672 | enc:961-1271: LS 20/6.000 PE; enc:1028 «PF 220/312» contro 01:2578 «180/312»; «mappa aerea 3D» (enc:1042-1063) |
| 4B Pioggia elfica / 4C Carica / Boss 4D | 01:2673-2906 (con l'eco dell'errata a 2757-2765 e la regia A5) | enc:1189-1199: **bonus della carica, 6 voci per un totale di +23** (con «Presenza Due Re» e «Vendetta») contro 01:2815-2822 (5 voci, «TOTALE +15») e 01:2828 «Attacco +23». La 01 si contraddice da sola |
| Epilogo / Vittoria agrodolce | 01:2907-3007 | enc:1273-1354: discorso di Thorek (1320), discorso del PG guerriero (1322-1323), addii in tre citazioni (1327-1334), semi d'avventura (1350-1354). Perdite alleate diverse: enc 3 ranger feriti e 1 gufo, 01:2923-2925 5 ranger e 2 gufi. Onori (feudo, 50.000 mo) in tutte e due, contro D41/D42 e ARC08-17 |
| Cerimonia (Day 21) | `Cerimonia-delle-100-Asce.md` | — |
| PX / Appendice C | per i pregen 01:3237-3263 (D9: 0 PX, bonus in ARC08-10); per la verifica EL enc:1360-1408 | 01:3237-3263 dice che enc è la «fonte unica per i dettagli» e che B1 «non è ancora scritta», ma B1 esiste (ARC08-10) |
| Checklist del DM | identica in enc:1412-1432 e 01:3284-3302 | — |
| Regolamento di massa | `mass_combat_guide_Dm.md` (norma) + 02:527-569 (tabella da tavolo) | 01:3193-3236 (Appendice A): morale «Rinforzi» +2 (01:3228) contro +3 (02:567) |
| Danni strutturali | **conflitto**: 02:574-611 (cancello 800 PF, CA 23, durezza 20; mura 1.800; torri 2.500) contro L2:171 e COMPLETE (cancello 120 PF, CA 25, durezza 15) | legenda di 01:120-142: mura «PF 1800 per sezione di 30 m»; legenda di enc:8-35: «PF 180 per sezione di 3 m» (stesso valore per metro) |

### 2.3 PNG, unità, pregen

I dettagli sono nel secondo file
(`statblocchi-arc08-per-schede.md`). In breve:

| Blocco | Versione migliore | Cosa hanno in più le altre |
|---|---|---|
| Fauci, Cavaliere hobgoblin | 02 (errata B5 applicati, ramo D10, carry-over) | 01:151-186: più incantesimi e tattiche per round. `07_…/CORREZIONE-Boss-Fauci.md`: effetti narrativi del soffio (−2 CA permanente alle armature) |
| Grimjaw, Gorthak | 02 per la Furia; 01 per l'equipaggiamento completo | — |
| Re Thorek, Dana, Ventolesto, Orion | 01:147-466 (le schede del Bestiario puntano lì) | 02: tattiche |
| Lunapiena | 02:325-357 (la 01 ha un paragrafo) | — |
| Ranger elfici (12) | 01:400-415 | — |
| Tempestas | `Bestiario/png/Tempestas/Tempestas.md` (2026-09-24) per il dossier; nel branch, 01 e 02 sono pre-#241 | — |
| Pregen (4) | per il gioco 02:419-522 (stampabili, verificati ERRATA §3); per la regia 01:488-631 (talenti, equipaggiamento, momenti eroici, bonus di transizione) | le schede stampabili di 01:3380-3496 duplicano 02 §3 |
| Unità | numeri di unità **identici** fra 01:677-942 e 02:616-802 | 01: statistiche SRD della creatura singola. 02: movimento e capacità speciali (Furia orchesca, Guardia del Re, Spezzare la carica, balista nanica). Divergenze minori: Formazione tattica (01:685 «+2 CA con 2 alleati» contro 02 «DU 19 con 1 alleato»); balista (02:800 «AU +10, 3d8, 120 m» contro L2 «+18, 3d8+10») |

---

## 3. Gruppi che si sovrappongono

**01 ⟷ enc (ADR-0074).** enc è una generazione parallela, mai aggiornata dopo
il 2026-07-02. Hanno 222 righe esatte in comune, compresi i 37 paragrafi
copiati alla lettera e quasi tutti gli schizzi di 3A, 3B, 4A, 4B, 4C ed
epilogo, che coincidono blocco per blocco. enc **non è un sottoinsieme**: le
sue 168 righe senza corrispondenza sono elencate in §1 e §2.2 e vanno fuse in
DEF-1..4. Non c'è una sola proposta per tutto il file: la 01 è migliore per la
struttura, i rimandi alle griglie e la parte dalle Élite in poi; enc è
migliore per 1B, 2A, i valori LS/PE e i discorsi dell'epilogo.

**02 ⟷ 01.** Condividono 111 righe. Nessuno dei due contiene l'altro: 02 ha
gli errata, D10, Lunapiena, le capacità delle unità e le strutture; 01 ha gli
incantesimi completi, i talenti, i pregen completi e le statistiche delle
singole creature. 02 resta materiale comune; le parti della 01 vanno in DEF-1.

**90 ⊂ 91 ⊂ 92 ⟷ COMPLETE.** COMPLETE è una riscrittura, con circa 6 righe
esatte in comune: non una copia. Vince su descrizioni e tattica. I prompt
del 92 restano unici (§1).

**Lotto-1/2/3 ⟷ L1/L2/L3.** Assorbiti, come verificato a campione: cancello
120/25/15, baliste +18 3d8+10, Re Thorek XIII, corno con 50 orchi, dirupo
40d6, ingegneri 1d4/round, pozze d'acido, statua For CD 20. L3 riconcilia
esplicitamente il Lotto-3 (L3:467-471 per 2d8 contro 2d4+4 e CD 25 contro
CD 20; L3:633-634 per il ramo D10). Restano in archivio.

**Fuori cartella: DEF-5 ⟷ 01 3B/3C e L3 MAPPA 5.** DEF-5 è più nuovo e
dichiara di non riscrivere la battaglia. Però la sua versione dell'Apparizione
(effetti, Thorek a 8 pf ed esausto) è quella canonica: DEF-3 deve importarla,
non riprendere 01:2167-2449. Lo stesso vale per **M7-D, M7-E e M7-F/1372
⟷ L3 H3-1** (la ritirata del Giorno 3).

---

## 4. Stato degli errata

### `ERRATA-ARC08-35-Verification.md`

| # | Correzione | Bersaglio dichiarato | Applicata? |
|---|---|---|---|
| 1.1 | Punire il Bene 1/giorno, +2 danni | 02 | **Sì**, 02:141. **No** in 01:204 («2/giorno … +10 (livello)») |
| 1.2 | Aura di Disperazione rimossa, Attacco furtivo +1d6 | 02 | **Sì**, 02:142 e 02:145-147. **No** in 01:205 (l'aura c'è ancora) |
| 2 | Soffio a cono come house-rule esplicita | 02 | **Sì**, 02:92 (nota). In 01:171 c'è senza nota → **parziale** |
| 2b | Soffio in linea: TS Riflessi CD 29 | verifica | 01 e 02 corretti. **enc:527 «Tempra CD 25»** nella 2B è sbagliato e nessun errata lo copre |
| 3 | Pregen verificati (Borin +20/+15/+10, Dara, Thorin, Nala) | 02 §3 | **Sì**, 02:431 e seguenti. Restano le divergenze 01 ⟷ 02 sulla scomposizione della CA e sul Canto di guerra (vedi file statblocchi) |
| 4 | Sistema di massa compatibile 3.5 | 02 §4 | verifica, nessuna modifica. Il consolidamento C1 ha generato il rimando circolare citato in §1 |
| 5 | Gear di Tordek (D17) | — | non verificato: nessuna occorrenza nella cartella |
| §5 | PNG della 01 «fuori scope» | — | **aperto**. È questo che lascia 01:204-205 scorretti |

### `ERRATA-ARC08-DESCRIZIONE-EPICA.md`

| # | Correzione | Applicata? |
|---|---|---|
| 1 | «Baruk Stonebeard» → Thorek | **Sì**: 0 occorrenze di «Stonebeard» nella cartella |
| 2 | Thorek non muore (−80 PF; la morte è un ramo) | **Sì**: 01:1738 e 01:1741. DEF-5 aggiunge «stabilizzato a 8 pf, esausto» (D77) |
| 3 | Glossa «Asce dei Nani! I Nani sono su di voi!» | **Sì** in 01:2240. Il titolo 4C (01:2751), il riquadro 01:2755 e enc:1158 non hanno glossa: nessun errore |
| 3-bis | Tre righe recuperate | **Sì**: 01:948-959 (orda), 01:2243-2252 (veterano), 01:2757-2765 (eco). Il rimando in ARC08-04 §3-bis (riga 83) c'è |
| 4 | Niente «Aghâd-un» e niente «Dúrin» | **Sì**: l'unica occorrenza (01:2250) è la nota che dice di non usarla |
| 5 | Orion ≠ Hella | **Sì**: nessuna confusione nella 01 |
| 6 | Niente «venticinque giorni» | **Sì**: 0 occorrenze |
| 7 | «Antico re» e «nano con la corona» sono la stessa persona (Thorik) | **non verificabile**: il testo del DM non è nel repo. 01:2753 tiene Thorek e «il Guerriero della Corona di Adamantio» distinti, che è corretto |
| §6 | Riscrittura dei riquadri 3C e 4C | **No**, debito aperto: tocca a DEF-3 e DEF-4 |

---

## 5. Domande per il DM

Si risponde con una parola. Tra parentesi la risposta consigliata.

Le **Q1-Q12** di `A3-canone-arc08.md` restano valide e non le ripeto:
Salta, No, No, DEF-4, Viva, Integrare, Presente, Pregen, 118→109, +2, Sì, D90.
Si aggiungono queste:

| # | Domanda | Consigliata |
|---|---|---|
| D1 | 2B, TS del soffio: Riflessi o Tempra? | **Riflessi** (SRD; enc:527 è un errore) |
| D2 | Fauci, PF all'inizio del finale: 180 (01), 220 (enc), 232 (L3) o il massimo della scheda meno il carry-over B4? | **Carry-over**, contato dal massimo della scheda di Fauci, che dipende dal suo statblock (337 pf sulla PR #241, 2026-10-17), non da un numero scritto qui |
| D3 | Bonus della carica: +15 o +23? | **Ricalcolare** (ricostruirlo per tipo di bonus, che in 3.5 non si sommano fra uguali) |
| D4 | Cancello: 120 PF (mappe) o 800 PF (02)? | **120** (L2, COMPLETE, Lotto-2 e i tre master tattici sono d'accordo) |
| D5 | Prompt del 92: migrarli? | **Sì** (in `campaign/ai-media-prompts/09_ARC08…`) |
| D6 | enc dopo la fusione | **Archiviare** |
| D7 | 2A: i due troll rigeneranti di enc entrano? | **Sì** |
| D8 | Asce: 210 sul campo e 100 nella sala, tutte e due? | **Entrambe** |
| D9 | 1B: Consiglio (01) o Preparazione (enc)? | **Entrambi** (Consiglio, poi Preparazione) |
| D10 | Giganti in 2A: 6 (enc) o 8 (01 e 02)? | **8** |
| D11 | Morale «Rinforzi»: +2 o +3? | **+3** (02, la tabella da tavolo) |
| D12 | Revisione r1 di enc in sospeso | **Scartare** (enc viene fusa e archiviata) |
| D13 | Scala del Cuore: 1,5 m (L3) o 3 m (CM-1)? | **1,5** (L3, la griglia più nuova del lotto MAPPE-UC) |
| D14 | Onori: 50.000 mo e feudo (01, enc) o ARC08-17? | **ARC08-17** (D41/D42) |
| D15 | ERRATA: archiviarli quando i DEF li hanno assorbiti? | **Sì** |
| D16 | `combat_prompts_guide`: archiviarlo? | **Sì** |

---

## 6. Cosa non ho letto per intero

- 01: letta a sezioni (1-640, sessioni ed epilogo per confronto, indice dei
  titoli). La parte degli eserciti (636-942) l'ho confrontata con 02 solo sui
  valori di unità, non riga per riga.
- 03, 04, 10, 11, 12, 13, 15, 16, 17, Cerimonia, `mass_combat_guide_Dm`:
  letti solo in testa e con grep mirati. Nessuna verifica di contenuto unico
  al loro interno (sono file a scopo unico, senza sovrapposizioni con 01 ed
  enc).
- COMPLETE, L1/L2/L3, Lotto-1/2/3: indici, matrice A8, sezioni di evoluzione e
  grep. Le griglie non le ho confrontate cella per cella.
- DEF-5, M7-*/1372, `CORREZIONE-Boss-Fauci`: solo intestazioni e
  quick-reference.
- Le revisioni r1 in sospeso in `plans/scrittura/revisioni-pilota-ARC08/`:
  solo intestazioni.
- Schede del Bestiario: solo GS e classe, e a chi puntano.
