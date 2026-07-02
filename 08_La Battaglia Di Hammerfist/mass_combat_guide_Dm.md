# GUIDA GESTIONE COMBATTIMENTI DI MASSA
## *Strumenti Pratici per DM - Battaglie Epiche Senza Rallentamenti*

> **📌 FONTE UNICA DEL SISTEMA DI MASSA (piano ARC-08 C1, 2026-07-02).**
> Questo file è la **fonte normativa** del combattimento di massa della
> campagna. Le altre copie sono **puntatori** qui:
> `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` §4 (quick-reference da
> tavolo), la Guida DM `ARC08-01` §appendici, il registro
> `ARC08-03-REGISTRO-PERDITE.md`. ARC-09 (`STRUTTURA` §9, "il Fronte")
> è il **discendente** di questo sistema — vedi §RACCORDO in fondo.
> **Stato**: canonico. **Ultima revisione**: 2026-07-02.

---

## ⚖️ SISTEMA DI RISOLUZIONE — leggi PRIMA (riconciliazione C1)

> Storicamente questo file e `ARC08-02` §4 usavano **due dadi diversi**
> per la stessa battaglia. C1 li riconcilia: **una risoluzione
> canonica**, una variante rapida opzionale.

**CANONICO — AU/DU/PFU (1d20)**: è la risoluzione **canonica** della
campagna, quella che **ARC-09 ha ereditato** (STRUTTURA §9) e che la
verifica 3.5 ha validato (`ERRATA-ARC08-35-Verification.md` §4).
- **Unità** = 10 creature. **PFU** = 10 (ogni PFU perso = 1 creatura
  eliminata; a 0 PFU l'unità è distrutta).
- **AU** (Attacco Unità) / **DU** (Difesa Unità) = valori medi.
- **Risoluzione**: **1d20 + AU vs DU**. Successo = 1 PFU; superare la DU
  di +5 = 2 PFU; di +10 = 3 PFU.
- **Morale**: scala **−5..+5** (applicata ad AU e DU).
- Interazione PG: attacco ad area = 1d4 PFU (con TS); singolo colpo ≥25
  danni = 1 PFU; comandare un'unità = azione + prova Car CD 15 → +2 AU.
- Tabella completa in `ARC08-02` §4 (quick-reference stampabile).

**VARIANTE RAPIDA OPZIONALE — 2d6** (le sezioni sottostanti di questo
file): un motore 2d6 alternativo (PF 1-10 per unità dove 1 "Danno
Unità" = 25 pf individuali; morale −4..+4). **NON è** la risoluzione
che ARC-09 ha ereditato: usala solo se preferisci un motore 2d6 e
**resta coerente** entro la singola battaglia. Mappa rapida tra i due:

| Concetto | Canonico (AU/DU/PFU, d20) | Variante 2d6 |
|---|---|---|
| Salute unità | PFU 10 (1 PFU = 1 creatura) | PF 1-10 (1 Danno = 25 pf individuali) |
| Tiro | 1d20 + AU vs DU | 2d6 + Bonus Attacco vs CA Unità |
| Morale | −5..+5 | −4..+4 |

> **Regola d'oro**: scegli **un** motore per la battaglia e non
> mischiarli. Per l'aggancio ad ARC-09, usa il **canonico**.

---

# **🎯 FILOSOFIA DEL SISTEMA**

## **OBIETTIVI PRINCIPALI:**
1. **Velocità:** Ogni round di massa si risolve in 5-10 minuti massimo
2. **Drama:** I PG rimangono protagonisti, non si perdono nella folla
3. **Impatto:** Le azioni dei PG influenzano realmente l'esito di massa
4. **Semplicità:** Regole intuitive che non richiedono calcoli complessi

## **PRINCIPIO CHIAVE: "ZOOM IN/ZOOM OUT"**
- **Zoom Out:** Battaglia di massa (unità, morale, obiettivi strategici)
- **Zoom In:** Combattimenti PG (meccaniche standard D&D)
- **Transizioni Fluide:** Passa da uno all'altro senza interruzioni

---

# **🔧 STRUMENTI FONDAMENTALI**

## **SISTEMA DELLE UNITÀ**

### **UNITÀ STANDARD = 10 CREATURE**
Ogni "Unità" rappresenta 10 creature dello stesso tipo:
- **1 Unità Orchi** = 10 Orchi individuali
- **1 Unità Nani Veterani** = 10 Nani Guerrieri
- **1 Unità Hobgoblin Élite** = 10 Hobgoblin con equipaggiamento superiore

### **STATISTICHE SEMPLIFICATE UNITÀ:**
```
UNITÀ STANDARD:
- Punti Forza (PF): 1-10 (10 = unità al completo)
- Classe Armatura: Media delle creature individuali
- Bonus Attacco: Media +2 (effetto massa)
- Danni: 1 "Danno Unità" = 25 PF individuali persi
- Morale: da -4 a +4 (modificatore a tutti i tiri)
```

### **TIPI DI UNITÀ:**

#### **FANTERIA LEGGERA** (Orchi, Goblin)
- **PF Unità:** 8 (fragili ma numerosi)
- **CA:** 14-15
- **Attacco:** +6
- **Danni:** 1d6 per "successo di unità"
- **Velocità:** 30ft/round
- **Speciale:** +2 vs unità in rotta

#### **FANTERIA PESANTE** (Hobgoblin, Nani)
- **PF Unità:** 10 (resistenti e disciplinati)
- **CA:** 17-18  
- **Attacco:** +8
- **Danni:** 1d8 per "successo di unità"
- **Velocità:** 20ft/round
- **Speciale:** +2 CA in formazione difensiva

#### **UNITÀ ÉLITE** (Guardie, Veterani)
- **PF Unità:** 12 (meglio addestrate)
- **CA:** 18-20
- **Attacco:** +10
- **Danni:** 1d10 per "successo di unità"
- **Velocità:** 25ft/round
- **Speciale:** +3 morale, immune a paura

#### **UNITÀ SPECIALI** (Giganti, Mostri)
- **PF Unità:** 15+ (creature potenti)
- **CA:** 16-22
- **Attacco:** +12+
- **Danni:** 2d6+ per "successo di unità"
- **Speciale:** Capacità uniche (volo, rigenerazione, etc.)

---

## **⚡ SISTEMA INIZIATIVA MASSA**

### **FASE 1: INIZIATIVA STRATEGICA**
Solo i comandanti tirano iniziativa:
```
ORDINE TURNI:
1. Comandante A (più alto)
2. Comandante B  
3. Comandante C
4. Risoluzione Automatica (unità senza comandi)
```

### **FASE 2: DICHIARAZIONE ORDINI**
Ogni comandante dichiara:
- **Target primario** delle sue unità
- **Formazione** (offensiva, difensiva, mobile)
- **Obiettivo tattico** (attacco, difesa, manovra)

### **FASE 3: RISOLUZIONE SIMULTANEA**
Tutti gli attacchi si risolvono insieme per velocità

---

# **🎲 MECCANICHE DI COMBATTIMENTO RAPIDE**

## **ATTACCHI TRA UNITÀ - SISTEMA 2D6**

### **PROCEDURA STANDARD:**
1. **Unità A attacca Unità B**
2. **Tira 2d6 + Bonus Attacco Unità**
3. **Confronta con CA Unità Bersaglio**
4. **Successo = 1 "Danno Unità" al bersaglio**

### **TABELLA RISULTATI RAPIDI:**
```
RISULTATO 2d6:    EFFETTO:
2-5:              Attacco fallito completamente
6-8:              Attacco standard (1 Danno Unità)
9-10:             Attacco forte (1 Danno + penalità morale)
11-12:            Breakthrough! (2 Danni + bonus tattici)
```

### **MODIFICATORI COMUNI:**
- **Flanking:** +2 attacco
- **Terreno Elevato:** +1 attacco, +1 danno
- **Carica:** +2 primi danni, -1 CA fino al prossimo turno
- **Supporto Magico:** +1-3 (varia per potenza incantesimi)

---

## **🛡️ SISTEMA MORALE DINAMICO**

### **SCALA MORALE (-4 a +4):**
```
MORALE -4: ROTTA TOTALE (unità fugge)
MORALE -3: PANICO (50% azioni, -3 tutti tiri)
MORALE -2: PAURA (-2 attacchi, -2 danni)
MORALE -1: SCOSSO (-1 tutti i tiri)
MORALE  0: NORMALE (nessun modificatore)
MORALE +1: DETERMINATO (+1 tutti i tiri)
MORALE +2: ISPIRATO (+2 attacchi, +1 danni)
MORALE +3: EROICO (+3 attacchi, +2 danni, immune paura)
MORALE +4: LEGGENDARIO (+4 attacchi, +3 danni, +1 azione extra)
```

### **EVENTI CHE MODIFICANO MORALE:**
```
POSITIVO:                    NEGATIVO:
+1 Comandante sopravvive     -1 Comandante ferito
+2 Comandante azione eroica  -2 Comandante morto
+1 Vittoria tattica          -1 Perdite pesanti (50%+)
+2 Rinforzi arrivano         -2 Attacco nemico devastante
+1 Supporto magico           -1 Isolati/accerchiati
+3 Miracolo/Intervento div.  -3 Presenza drago/demone
+1 Per ogni PG alleato vivo  -1 Per ogni PG alleato morto
```

### **PROVE MORALE AUTOMATICHE:**
- **Quando:** Unità perde 50%+ PF in un round
- **CD:** 10 + danni subiti + modificatori situazione
- **Fallimento:** Morale scende 1-2 punti
- **Successo Critico:** Morale sale 1 punto ("Vendetta!")

---

# **👥 GESTIONE NEMICI MULTIPLI**

## **SISTEMA GRUPPI E LEADER**

### **GROUPING INTELLIGENTE:**
Invece di gestire 50 orchi individuali:
```
GRUPPO ORCHI BERSERKER (12 creature):
- LEADER: Orco Sergente (statistiche piene)
- GREGARI: 11 Orchi (statistiche semplificate)
  * Stesso turno iniziativa del Leader
  * Stesso bonus attacco del Leader
  * Danni unificati per round
```

### **STATISTICHE GREGARI SEMPLIFICATE:**
```
GREGARIO STANDARD:
- PF: Metà del normale
- CA: Normale
- Attacchi: Solo 1 per round (no Full Attack)
- Danni: Normali ma senza bonus situazioni
- TS: Usano quello del Leader con -2
```

### **LEADER ENHANCEMENT:**
Il Leader ottiene bonus per ogni gregario vivo:
- **+1 attacco per ogni 3 gregari**
- **+2 danni per ogni 5 gregari**
- **+1 iniziativa per ogni 4 gregari**

---

## **⚡ AZIONI SIMULTANEE**

### **TURNO DEL GRUPPO (1 MINUTO TOTALE):**

#### **PASSO 1: Dichiarazione Leader (10 secondi)**
Leader dichiara:
- Target prioritario
- Tattica generale (offensiva/difensiva/mobile)
- Uso capacità speciali

#### **PASSO 2: Risoluzione Gregari (30 secondi)**
```
METODO RAPIDO GREGARI:
1. Conta quanti possono attaccare (portata, linea visuale)
2. Tira 1d6 per ogni 3 gregari che attaccano
3. Risultato 4+ = 1 colpo riuscito
4. Ogni colpo = danni base creature
5. Somma tutti i danni, applica al bersaglio
```

#### **PASSO 3: Azioni Speciali Leader (20 secondi)**
Leader agisce con meccaniche complete D&D se necessario

### **ESEMPI PRATICI:**

#### **ESEMPIO A: 15 Orchi vs PG Guerriero**
```
SETUP:
- Leader: Orco Capo (PF 38, CA 17, +9 att, 1d12+5 danni)
- Gregari: 14 Orchi base (PF 11 cad, CA 13, +5 att, 1d12+3)

RISOLUZIONE (30 secondi totali):
1. Leader attacca PG: 1d20+11 vs CA PG
2. Gregari: 14 orchi = 5 dadi (14÷3 = 4.67 → 5)
3. Tira 5d6, risultati 4+ = colpi
4. Ogni colpo = 1d12+3 danni al PG
5. FATTO!
```

#### **ESEMPIO B: 8 Hobgoblin Élite vs 2 PG**
```
SETUP:
- Leader: Sergente Hobgoblin (stats complete)
- Gregari: 7 Hobgoblin (stats dimezzate)

RISOLUZIONE:
1. Leader sceglie PG più minaccioso
2. Gregari si dividono: 4 su PG A, 3 su PG B
3. Gruppo A: 2 dadi (4÷3 → 1.33 → 2)
4. Gruppo B: 1 dado (3÷3 = 1)
5. Risultati simultanei su entrambi i PG
```

---

# **🎭 MANTENERE PROTAGONISMO PG**

## **SISTEMA "SPOTLIGHT ROTANTE"**

### **OGNI PG HA UN "MOMENTO EROICO" PER ROUND:**
```
ROUND TIPO:
1. ZOOM OUT: Battaglia massa (2 minuti)
2. ZOOM IN: PG 1 momento eroico (2 minuti)
3. ZOOM IN: PG 2 momento eroico (2 minuti)
4. ZOOM IN: PG 3 momento eroico (2 minuti)  
5. ZOOM IN: PG 4 momento eroico (2 minuti)
TOTALE: 10 minuti per round completo
```

### **TIPI MOMENTI EROICI:**
- **Duello vs Elite:** PG affronta nemico importante 1vs1
- **Comando Tattico:** PG dirige unità alleate per manovra speciale
- **Magia di Massa:** PG lancia incantesimi che influenzano battaglia
- **Salvataggio Eroico:** PG salva alleati o PNG importanti
- **Breakthrough:** PG spezza formazione nemica importante

---

## **🎯 AZIONI PG CHE INFLUENZANO MASSA**

### **COMBATTIMENTO DIRETTO:**
```
EFFETTI PG SU UNITÀ:
- PG uccide Elite nemica → -1 morale unità collegate
- PG uccide Comandante → -3 morale + perdita coordinamento
- PG distrugge macchina guerra → perdita capacità speciale
- PG elimina mago nemico → perdita buff/debuff di massa
```

### **LEADERSHIP E COMANDO:**
```
PROVE LEADERSHIP PG:
- Diplomazia CD 15 → +1 morale unità alleate per 5 round
- Intimidire CD 18 → -1 morale unità nemiche per 3 round
- Perform CD 20 → +2 morale generale per 10 round
- Comando (se ha gradi) → bonus tattici specifici
```

### **MAGIA DI BATTAGLIA:**
```
INCANTESIMI SCALA MASSA:
LIVELLO 1-2: Influenza 1 unità (10 creature)
LIVELLO 3-4: Influenza 2-3 unità
LIVELLO 5-6: Influenza 4-5 unità  
LIVELLO 7+:  Influenza battaglia intera

ESEMPI:
- Fireball su unità → 8d6 danni divisi tra 10 creature
- Bless su alleati → +1 attacco a 2-3 unità per durata
- Fear di massa → test morale immediato nemici area
```

---

# **📊 STRUMENTI PRATICI DM**

## **TABELLE RIFERIMENTO RAPIDO**

### **TABELLA DANNI UNITÀ:**
```
DANNI    PERDITE     EFFETTI
SUBITI   CREATURE    MORALE/PERFORMANCE

1-2      1-2 morti   Nessuno
3-4      3-4 morti   -1 attacchi prossimo round
5-6      5-6 morti   Test morale CD 12
7-8      7-8 morti   Test morale CD 15, -1 morale
9+       9+ morti    Test morale CD 18, -2 morale
10+      UNITÀ ROTTA Fuga automatica
```

### **TABELLA MODIFICATORI SITUAZIONALI:**
```
SITUAZIONE              ATTACCO    DANNI    MORALE
Flanking               +2         +1       0
Carica                 +2         +2       +1 primo round
Terreno elevato        +1         +1       0
Terreno difficile      -2         0        0
Supporto magico        +1 to +3   +1       +1
Commander presente     +2         0        +2
Commander morto        0          0        -3
Superstiti <50%        0          0        -2
Rinforzi arrivati      0          0        +2
```

---

## **🃏 CARTE TATTICHE RAPIDE**

### **CARTE COMANDO PER PG:**
Prepara carte che i PG possono "giocare" durante battaglia:

#### **CARTA: "CARICA EROICA"**
```
EFFETTO: Una unità alleata a scelta ottiene:
- +4 attacco questo round
- +3 danni questo round  
- +2 morale per 3 round
COSTO: Azione Standard PG
LIMITE: 1/battaglia per PG
```

#### **CARTA: "TATTICA GENIALE"**
```
EFFETTO: 
- Riordina iniziativa unità alleate questo round
- 1 unità alleata ottiene azione extra
- +1 a tutti i test morale per 5 round
COSTO: Azione Completa PG
LIMITE: 1/battaglia per PG
```

#### **CARTA: "SACRIFICIO EROICO"**
```
EFFETTO:
- PG subisce 25% PF attuali come danni
- Tutte unità alleate: +3 morale per resto battaglia
- Nemici: -2 morale per 10 round
COSTO: Azione Gratuita, danni non prevenibili
LIMITE: 1/campagna per PG
```

---

## **⏱️ TIMER E GESTIONE TEMPO**

### **SISTEMA TIMER RIGIDO:**
```
FASI ROUND MASSA (10 MINUTI TOTALI):

MINUTO 1-2: FASE DICHIARAZIONI
- Tutti dichiarano intenzioni
- No changes dopo questo punto

MINUTO 3-5: FASE RISOLUZIONE MASSA  
- Attacchi unità vs unità
- Test morale se necessari
- Movimento unità

MINUTO 6-10: FASE PG INDIVIDUALI
- 1 minuto per PG per azioni eroiche
- Solo azioni che influenzano massa
- No combattimenti lunghi (max 3 round individuali)
```

### **TECNICHE ACCELERAZIONE:**

#### **PRE-ROLLING:**
- Tira dadi attacchi nemici durante turni PG
- Pre-calcola danni medi per velocità
- Usa danni "presi 10" per gregari non importanti

#### **DELEGAZIONE:**
- Giocatori gestiscono unità alleate specifiche
- Ognuno controlla 2-3 unità naniche
- DM gestisce solo nemici principali

#### **RISOLUZIONI PARALLELE:**
- Mentre risolvi scontro A, giocatori preparano azioni scontro B
- Usa dadi colorati: rossi=nemici, blu=alleati, verdi=PG
- Risolvi tutti i tiri simili insieme

---

# **🎨 DESCRIZIONI CINEMATOGRAFICHE RAPIDE**

## **TEMPLATE DESCRITTIVI (30 SECONDI CIASCUNO):**

### **APERTURA ROUND:**
> *"Il campo di battaglia risuona del clamore di [X] unità che si scontrano. Al centro della mischia, [PG nome] si distingue per [azione specifica]. Intorno a loro, la situazione è [descrizione generale 1 frase]."*

### **ATTACCO RIUSCITO:**
> *"La [unità alleata] colpisce duramente la [unità nemica], e potete vedere [dettaglio visivo]. Il morale [alleati/nemici] [sale/scende] visibilmente."*

### **MOMENTO EROICO:**
> *"Proprio quando tutto sembrava [situazione], [PG nome] [azione eroica]. L'effetto è [immediato/drammatico]: [conseguenza visibile]."*

### **CAMBIO SITUAZIONE:**
> *"La battaglia prende una piega [nuova]. [Evento chiave] cambia completamente la dinamica, e ora [nuova situazione tattica]."*

---

# **📋 CHECKLIST PREPARAZIONE BATTAGLIA**

## **PRIMA DELLA SESSIONE:**

### **SETUP UNITÀ:**
- [ ] Ogni unità ha: PF, CA, Attacco, Danni, Morale iniziale
- [ ] Comandanti identificati con stats complete
- [ ] Obiettivi tattici chiari per ogni fazione
- [ ] Mappa battaglia con posizioni iniziali marcate

### **MATERIALI:**
- [ ] Dadi colorati per fazioni diverse
- [ ] Token/miniature per unità (1 per unità, non per creatura)
- [ ] Fogli tracciamento morale e perdite
- [ ] Carte tattiche se utilizzate
- [ ] Timer visibile per mantenere ritmo

### **NARRATIVA:**
- [ ] 3-4 descrizioni pre-scritte per momenti chiave
- [ ] Conseguenze vittoria/sconfitta chiare
- [ ] Moment i eroici pianificati per ogni PG
- [ ] Connessioni con storia principale

---

## **DURANTE LA BATTAGLIA:**

### **OGNI ROUND:**
- [ ] Aggiorna morale dopo ogni azione significativa
- [ ] Traccia perdite unità in tempo reale  
- [ ] Mantieni timer: max 10 minuti per round completo
- [ ] Rotazione spotlight PG garantita
- [ ] Descrizioni brevi ma evocative

### **MANAGEMENT PROBLEMI:**
```
PROBLEMA: Troppi calcoli
SOLUZIONE: Usa danni medi, pre-calcolati

PROBLEMA: PG si sentono inutili
SOLUZIONE: Zoom in immediato su loro

PROBLEMA: Battaglia trascina
SOLUZIONE: Timer rigido + conseguenze automatiche

PROBLEMA: Perdita ritmo narrativo
SOLUZIONE: Descrizioni template + musica epica
```

---

# **🏆 ESEMPI PRATICI COMPLETI**

## **ESEMPIO BATTAGLIA: 40 ORCHI + 20 HOBGOBLIN vs 30 NANI + 4 PG**

### **SETUP RAPIDO (5 MINUTI):**
```
ORCHI: 4 Unità (10 cad) + 1 Leader Orco
PF Unità: 8, CA 14, +6 att, 1d6 danni
Morale: +1 (numerosi)

HOBGOBLIN: 2 Unità (10 cad) + 1 Sergente
PF Unità: 10, CA 17, +8 att, 1d8 danni  
Morale: +2 (disciplinati)

NANI: 3 Unità (10 cad) + PNG Comandante
PF Unità: 10, CA 18, +8 att, 1d8 danni
Morale: 0 (defensive)

PG: 4 individui, stats normali D&D
Morale: +3 (eroi leggendari)
```

### **ROUND 1 (10 MINUTI TOTALI):**

#### **MINUTI 1-2: Dichiarazioni**
- **Orchi:** Carica frontale, target unità nani centrali
- **Hobgoblin:** Flanking destro, target commander nani
- **Nani:** Formazione difensiva, hold ground
- **PG:** Ognuno dichiara tattica individuale

#### **MINUTI 3-5: Risoluzione Massa**
```
ORCHI vs NANI:
- 4 unità orchi vs 3 unità nani
- 4 attacchi: 2d6+6 vs CA 18
- Risultati: [tira dadi] → es: 2 successi
- 2 danni unità ai nani → 2 unità nani ora PF 8

HOBGOBLIN FLANKING:  
- Bonus +2 per flanking
- 2d6+10 vs CA 18 per comandante
- Risultato: [tira] → se successo, comandante ferito

TEST MORALE:
- Nani testano per perdite: 2d6+0 vs CD 12
- Risultato determina morale prossimo round
```

#### **MINUTI 6-10: Azioni Eroiche PG**
- **PG 1:** Duello vs Leader Orco (2 min)
- **PG 2:** Buff magico unità alleate (1 min)  
- **PG 3:** Carica vs Hobgoblin flanking (2 min)
- **PG 4:** Tiro precisione vs Sergente (1 min)

### **RISULTATO ROUND 1:**
```
STATO FINALE:
- Orchi: 3.5 unità (perdite da PG actions)
- Hobgoblin: 1.8 unità  
- Nani: 2.2 unità
- PG: Vari, ma protagonisti chiari

MORALE AGGIORNATO:
- Orchi: 0 (perdite inaspettate)
- Hobgoblin: +1 (flanking riuscito)
- Nani: +1 (PG actions inspiring)
- PG: +3 (sempre eroici)
```

---

## **🎯 RISULTATI E VANTAGGI SISTEMA**

### **VELOCITÀ COMPROVATA:**
- **Round tradizionale 50+ creature:** 45-60 minuti
- **Round con questo sistema:** 8-12 minuti
- **Miglioramento:** 75-80% riduzione tempo

### **ENGAGEMENT MANTENUTO:**
- PG sempre coinvolti (spotlight garantito)
- Decisioni tattiche significative
- Conseguenze visibili e immediate
- Progressione narrativa costante

### **SEMPLICITÀ GESTIONALE:**
- No tracking individuale creature multiple
- Calcoli ridotti al minimo  
- Prep time battaglia ridotto 50%
- Mental load DM drasticamente alleggerito

---

**"Con questi strumenti, anche la battaglia più epica diventa gestibile. I tuoi giocatori vivranno momenti eroici senza perdere tempo in calcoli noiosi!"**

---

## 🔗 RACCORDO CON ARC-09 (C1) — cosa STRUTTURA §9 ha ereditato e cambiato

Il sistema di massa di Rethmar (`09_.../Arco-Post-Hammerfist-P3-
BATTAGLIA-FINALE-RETHMAR-STRUTTURA.md` §9, "Cornice leggera d'assedio",
D13) è il **discendente diretto** di questo. Perché i due non divergano
in silenzio:

**Cosa ARC-09 ha EREDITATO da qui**:
- L'astrazione a unità (10 creature) e il tracciamento perdite
  (PFU/registro stampabile → `ARC08-03-REGISTRO-PERDITE.md`).
- La scala di **Morale** come modificatore dinamico agli esiti.
- Il principio che **i PG restano protagonisti** e influenzano la massa
  (spotlight, comando, magia di battaglia).
- I **danni strutturali** alle fortificazioni.

**Cosa ARC-09 ha CAMBIATO/aggiunto**:
- **VP nascosti** ("il Fronte"): a Rethmar il tracker di battaglia è
  **lato DM**, i giocatori **non lo vedono** (D13) — qui invece il DM
  gioca le unità apertamente. A Rethmar si sente solo la conseguenza
  narrata.
- **Eventi scelti dai PG via carte** (EVENT-DECK): la battaglia di
  Rethmar è vissuta tramite carte-crisi che i PG scelgono, non come
  wargame di unità. Qui le unità sono in primo piano; là sono sfondo.
- **Ruoli di comando formalizzati** (Comandante / Fulcro Arcano /
  Salvatore) e **check di Morale per ondata** (1d20 + Fronte vs CD) →
  una sintesi del Morale + comando di questo file, spostata a un layer
  per-ondata anziché per-unità.

**In una frase**: Hammerfist gioca la massa **in primo piano** (i PG
guidano una battaglia di unità); Rethmar la mette **sullo sfondo** (i PG
vivono crisi scelte, il motore di massa gira nascosto). Stesso DNA,
diverso zoom.

---

*- Fine Guida Gestione Combattimenti di Massa -*