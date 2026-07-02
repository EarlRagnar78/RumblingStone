# ERRATA CORRIGE PARTE 2 & 3 (3.5 Verification)
## Verifica meccanica D&D 3.5 SRD dei blocchi statistica di P2A/P2B/P2-RHEST/P3 + upscale del boss finale

> **Versione**: v1 (2026-07-02) — task **B5** del `PIANO-REVISIONE-ARC09`.
> **Formato**: gemello di `ERRATA-PARTE1-Quest-Hellas-35-Verification.md`.
> **Regola §0.2 del piano**: **solo 3.5 SRD/MM/FRCS** — nessun termine 5e
> (niente "azione bonus", "vantaggio/svantaggio", "reazione", "CMB/CMD" di PF).
> **Regola §0.3**: dove manca il dato originale, la correzione è marcata `[INFERRED]`.

---

## SOMMARIO VERIFICHE

**File analizzati (blocchi statistica):**
1. `Arco-Post-Hammerfist-P2A-Torre-PARTE*-STATBLOCCHI-*.md` (Torre Invisibile, boss Zalkatar)
2. `Arco-Post-Hammerfist-P2B-Torneo-STATBLOCCHI-COMPLETO.md` (Torneo di Dauth, Xal'thor/Sethrax/monaci)
3. `Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-*-STATBLOCCHI.md` (Saarvith + Regiarix, nido Razorfiend)
4. `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md` (Azarr Kul, Avatar, Erinni, Arcimago)
5. `00_Red Hand Of Doom/Armate-UNITA-NUOVE/*.md` (catalogo unità riusate)

**Status:** ⚠️ Errori sistematici lievi + **1 upscale strutturale** (boss finale) + **1 catch di coerenza** (Tyrgarun).

---

## ERRORI GLOBALI (tutti i file P2/P3)

### 1. AC di contatto / colto alla sprovvista
La maggior parte dei blocchi P3 le riporta (✅), ma diversi blocchi P2A/P2B **le
omettono**. In 3.5 sono **obbligatorie**. Aggiungere sempre:
```
CA: X (componenti), contatto X, colto alla sprovvista X
```

### 2. BAB / Lotta espliciti e matematica della Lotta
- **Lotta** = BAB + mod For + **mod speciale di taglia** (Piccola **−4**, Media 0,
  Grande **+4**, Enorme **+8**). Alcuni blocchi la sbagliano (vedi Saarvith).
- Riportare sempre `BAB +X / Lotta +X`.

### 3. Attacchi naturali secondari a −5
Per i draghi e i mostri con attacchi naturali multipli: **il morso è primario**,
**artigli/ali/coda sono secondari a −5** dal valore pieno (a meno di *Multiattack*,
che porta i secondari a −2). Diversi blocchi draconici elencano i secondari **al
valore pieno** — errato (vedi Regiarix).

### 4. Taglia Piccola: bonus di CA e Osservare/Nascondersi
Le creature Piccole hanno **+1 taglia alla CA e agli attacchi** e **+4 a
Nascondersi**. Alcuni blocchi di goblinoidi lo dimenticano (vedi Saarvith).

### 5. RI (Resistenza agli Incantesimi) razziale
- **Drow**: RI = **11 + livello di classe** (non "livello personaggio + 11" se
  multiclasse: usa i DV di classe che concedono RI).
- **Illithid**: RI 25 base (verificare le schede PNG canoniche, non duplicare).

### 6. Economia delle azioni (5e-ismi)
Passata di `grep` su P2/P3: sostituire ogni residuo
- "azione bonus" → **azione veloce (swift)**;
- "reazione" → **azione immediata**;
- "vantaggio/svantaggio" → riscrivere come **bonus/malus di circostanza** o
  situazione di **fiancheggiamento/copertura** 3.5.

### 7. Gradi di abilità ≤ DV + 3
Verificare che nessun blocco superi il massimo (grado abilità di classe = DV + 3).

---

## 1. UPSCALE DEL BOSS FINALE — AZARR KUL (headline di B5)

**Problema (piano B5, `STATBLOCCHI-EPICI` §1):** Azarr Kul come **Chierico 10 /
Guerriero 4** (14 DV, ~119 pf, CA 28, CR 15) è **sotto benchmark**: per un party
APL 14 con 5 artefatti è un boss da ~2 round. Il Kul originale di RHoD era già
~112 pf per un gruppo di livello 10-12. Serve reggere una **scena CR 17-18** in
tandem con l'Avatar (D8: l'Avatar è richiamato **durante** la battaglia, non al Fane).

**Azione:** portarlo a **Chierico 12 / Guerriero 4** (16 DV), pf ~155, CL 14,
lista di buff pre-cast con **durate esplicite** e **2 effetti a innesco**. CR sale a
**~17** da solo; la scena con l'Avatar resta **CR 18** (non si sommano i CR: la scena
è progettata, non additiva).

### Blocco corretto (SRD 3.5)

```
**Azarr Kul — Alto Wyrmlord di Tiamat (versione B5, CR 17)**
- Taglia/Tipo: Medio Umanoide (hobgoblin, mezzodrago blu)
- DV: Chierico 12 / Guerriero 4 (12d8 + 4d10 + 64 Cos ; pf ~155)  [era 14d8, ~119]
- Iniziativa: +1
- Velocità: 9 m (6 quadretti) in armatura
- CA: 28 (+9 armatura completa +2, +3 scudo +1, +1 Des, +3 naturale mezzodrago,
       +2 deflessione [shield of faith]); contatto 14; colto alla sprovvista 27
       → durante *righteous might*: taglia Grande, CA 27 (−1 taglia, +2 nat), contatto 13
- BAB / Lotta: +13 / +18 (Str 20 ; +19 sotto righteous might, taglia Grande)
- TS: Temp +15, Rif +7, Vol +15  [+2 dai livelli di chierico in più]
- Caratteristiche: For 20, Des 12, Cos 18, Int 12, Sag 20, Car 16

**Attacco:**
- Spadone sacrificale +2 +21/+16/+11 (2d6+9, 19-20/×2; +2d6 vs buoni)
  → sotto *divine power*: +25/+20/+15/+10 e For effettiva superiore
- Soffio mezzodrago blu: linea elettricità 6 m, 6d8, Rif CD 20 metà, ogni 1d4 round

**Incantesimi (Chierico 12, CL 14 con oggetti; domini Guerra + Tirannia/Tiamat):**
- 6°: *blade barrier* (CD 22), *harm* (CD 22)
- 5°: *flame strike* cromatico (CD 21), *righteous might*, *slay living*
- 4°: *divine power*, *freedom of movement*, *unholy blight* (CD 20), *air walk*
- 3°: *dispel magic*, *magic vestment*, *prayer*, *magic circle against good*
- 2°: *bull's strength*, *hold person* (CD 18), *spiritual weapon*, *silence*
- 1°: *divine favor*, *shield of faith*, *command*, *doom*, *bless*
- 0: *detect magic*, *guidance*, *resistance*, *inflict minor wounds*

**Buff pre-combattimento (con durate — da lanciare prima dello scontro):**
| Incantesimo | Effetto | Durata (CL 14) |
|---|---|---|
| *magic vestment* (armatura) | armatura completa +2 → **+3** | 14 ore |
| *magic vestment* (scudo) | scudo +1 → **+2** | 14 ore |
| *freedom of movement* | immune a immobilizzo/grapple/paralisi | 14 min |
| *righteous might* | taglia Grande, +8 For, +4 Cos, RD 5/male | 12 round |
| *divine power* | BAB pieno, +6 For, +12 pf temporanei | 12 round |
| *prayer* | +1 alleati / −1 nemici entro 12 m | 12 round |
| *shield of faith* | +2 deflessione (già in CA sopra) | 140 min |

**2 effetti a innesco (Contingent/oggetti) `[INFERRED — via Craft Contingent Spell
o pergamene sacerdotali, a discrezione DM]`:**
1. *Heal* automatico su di sé quando scende sotto **40 pf** (1/scontro).
2. *Word of recall* / *plane shift* al Fane quando scende sotto **15 pf** (fuga per
   ARC-10) **oppure** *divine power* ri-innescato (se il DM vuole il combattimento
   fino alla morte). Il DM sceglie **uno** dei due prima della scena.

**Capacità speciali:**
- Aura di Comando: alleati hobgoblin entro 9 m +2 morale a colpire e TS Volontà.
- Canali divini di Tiamat: 7/giorno (*smite good*, *rebuke undead*).

**Tattiche:** pre-cast la tabella sopra; apre con *blade barrier* per spezzare la
formazione, poi carica il buffer/guaritore del party sotto *divine power*; usa
*harm* sul PG più corazzato; il soffio elettrico su cluster. Coordina Erinni/Abishai.
```

> **Nota CR-scena (D8):** con l'Avatar di Tiamat (CR 17, `STATBLOCCHI-EPICI` §2) la
> **scena** resta **CR 18** per un party APL 14 + alleati. Il Mythal (Fase 4) resta
> la valvola: −2 a colpire/TS all'Avatar e blocco delle evocazioni. **Non** sommare
> il CR di Tyrgarun: il drago è un **incontro separato** sbloccato dal Mythal (D11 v2).

---

## 2. P2-RHEST — Saarvith & Regiarix

### 2.1 Saarvith (Goblin Ranger 10, Piccolo) — correzioni di taglia
`...P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` §1.
- ❌ **CA 22 / contatto 14** non contano il **+1 taglia (Piccolo)** → ✅ **CA 23,
  contatto 15**, colto alla sprovvista 19.
- ❌ **Lotta +7** → con BAB +10, For +2, taglia Piccola −4 = ✅ **+8**.
- ✅ Attacco a distanza già include il +1 taglia (arco +19 corretto).
- ✅ TS e talenti da arciere corretti.

### 2.2 Regiarix (Drago Nero, Grande) — attacchi naturali
`...P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` §2 (e file gemello ENCOUNTER).
- ❌ **Morso +31** → BAB +22, For +8, taglia −1 = ✅ **+29** (salvo Weapon Focus
  esplicito, che va **dichiarato**).
- ❌ **Artigli/ali +29 al valore pieno**: sono **secondari a −5** → ✅ **artigli +24,
  ali +24** (o −2 se gli dai *Multiattack*: +27).
- ❌ **Colpo di coda 1d8+18**: il colpo di coda usa **1,5 × mod For** (For 27 = +8 →
  +12) → ✅ **1d8+12**, a +24 (secondario).
- ⚠️ **Coerenza (non 3.5, segnalato):** `state.md` §2 elenca Regiarix come **"Black
  young"**, questo blocco lo tratta come **Adulto CR 13**. Non è un errore di regole
  ma di canone: allineare in un futuro passaggio (B1.4 lo gioca come giovane/CR 13
  upscalato — ok se il DM sceglie quella lettura; annotare la scelta).

---

## 3. P2B-TORNEO — Xal'thor, Sethrax, monaci

### 3.1 Xal'thor (Illithid + Psion 6, CR 14) — **POINTER, non duplicare**
`...P2B-Torneo-STATBLOCCHI-COMPLETO.md` e catalogo rimandano a
`PNG/Xal_thor/Xal_thor.md` (fonte unica). ✅ Corretto tenerlo come pointer.
- Verifica sulla scheda PNG: **RI 25** presente? **CA contatto/colto**? **azione
  psionica** espressa come azioni 3.5 (standard/mossa/veloce/immediata), non 5e?

### 3.2 Sethrax il Velato (Illithid covert, CR 12)
Fonte tabella esiti: `PNG/Sethrax_il_Velato/Sethrax.md`. In scena (PARTE3) usa
*Mind Blast*, *Mental Barrier* 3/giorno, *Psionic Plane Shift/Dimension Door*.
- Verificare che *Mind Blast* sia **cono 4,5 m** (15 ft) con **TS Vol** corretto e
  che i PS/azioni psioniche non usino terminologia 5e. Statblock: usare la scheda PNG.

### 3.3 Monaci del Torneo (Rihan Monaco 14, Tetsu Monaco 12, ecc.)
`...P2B-Torneo-STATBLOCCHI-COMPLETO.md`.
- Verificare **CA Saggezza** (bonus Sag alla CA solo senza armatura/scudo e non
  colto alla sprovvista) e **Raffica di Colpi** (penalità corrette per livello:
  Monaco 12 = raffica a −1; Monaco 14 = raffica migliore a −0/−0/−0 con progressione).
- **Movimento veloce** e **danno unarmed** per livello (Monaco 12 = 2d6; 14 = 2d6+…).
- Le "7 Porte" dell'Orbe (Otto Porte) restano **effetti d'artefatto scenici**: già
  espressi come bonus morale + costi in Cos temporanea (SRD-legal, ok).

---

## 4. P2A-TORRE — Zalkatar

`...P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` (fonte). Boss dell'arco di Artemis.
- Tenere la **fonte unica** nel file PARTE4; non duplicare.
- Verifica: **RI 25** (illithid) + eventuale RI da Warlock/classe drow **non
  cumulativa** (usare la più alta, non sommare); CA contatto/colto presenti; poteri
  di *extract brain*/*mind blast* con azioni 3.5.
- I bonus di Artemis dalla sub-quest/sogno (**+2 TS Vol vs psionici**, **+1d6/+2d6
  Fase 3**) sono **del PG**, non di Zalkatar: non modificano il CR del boss (coerente
  con A7: il finale resta CR 16-18 senza sommare il drago).

---

## 5. P3 — Avatar, Erinni, Arcimago

- **Avatar di Tiamat (CR 17)** `STATBLOCCHI-EPICI` §2: ✅ CA contatto/colto presenti,
  soffi ridotti (3 teste), RI 28, debolezza-Mythal esplicita. **Ok.** Unica nota:
  gli attacchi secondari (2 morsi minori) già a −2 → coerente con *Multiattack*
  implicito; **dichiararlo**.
- **Erinni (MM CR 8)** §3: il testo la dà "CR 8-9 leggermente pompata". Se le si
  aggiungono DV/pf, **ricalcolare il CR** (una Erinni a 90 pf resta ~CR 9). Ok come
  scorta; dichiarare il CR effettivo usato.
- **Arcimago del Circolo (Mago 17, CR 14)** §4: PNG da proteggere. CA 21 bassa è
  **intenzionale** (non è un combattente). Ok; aggiungere contatto/colto per completezza.

---

## 6. CATCH DI COERENZA (trovato durante la verifica — fuori 3.5 ma importante)

`00_Red Hand Of Doom/Armate-UNITA-NUOVE/azarr-kul-final-cr15.md` (riga Summary)
diceva ancora **"mounts Tyrgarun"** — **contraddice D11 v2 e la sessione A7**
(Azarr Kul **NON** cavalca Tyrgarun; il drago è terrore dei cieli separato,
inchiodato dal Mythal). **Corretto in place** (vedi §7). Anche il CR del file
(15) va letto come **base**: il boss giocato è la versione B5 **CR 17** qui sopra.

---

## 7. CORREZIONI APPLICATE IN PLACE (con nota)

1. **`...P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md` §1** — Azarr Kul portato a
   **Chierico 12/Guerriero 4, ~155 pf, CR 17**, con tabella buff pre-cast e 2
   effetti a innesco (blocco §1 di questa errata), **nota di versione B5** in testa
   alla sezione.
2. **`.../Armate-UNITA-NUOVE/azarr-kul-final-cr15.md`** — rimosso "mounts Tyrgarun";
   riallineato a D11 v2 e rimando alla versione B5.

Le altre correzioni (§2-§5) sono **puntuali e non-strutturali**: si applicano in
place quando si tocca il file, o si tengono come **checklist di verifica al tavolo**
(come fa la ERRATA-PARTE1). Priorità:

### PRIORITÀ ALTA (meccanica)
1. ✅ Azarr Kul upscalato (fatto in place).
2. ❌ Regiarix: morso +29, secondari a −5 (artigli/ali +24), coda 1d8+12.
3. ❌ Saarvith: CA 23/contatto 15 (+1 taglia), Lotta +8.

### PRIORITÀ MEDIA (coerenza)
4. ⚠️ Aggiungere CA contatto/colto ai blocchi P2A/P2B che le omettono.
5. ⚠️ Dichiarare *Multiattack* dove i secondari sono a −2.
6. ⚠️ Verificare RI non cumulativa (Zalkatar) e RI drow = 11 + liv. classe.

### PRIORITÀ BASSA (fluff / pointer)
7. ✓ Xal'thor/Sethrax/Zalkatar restano pointer alle schede PNG (non duplicare).
8. ✓ Passata `grep` anti-5e su P2/P3.

---

## 8. FILE DA AGGIORNARE (quando si toccano)

1. `Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` — Saarvith taglia, Regiarix attacchi naturali.
2. `Arco-Post-Hammerfist-P2B-Torneo-STATBLOCCHI-COMPLETO.md` — CA contatto/colto, raffica monaci, RI.
3. `Arco-Post-Hammerfist-P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` — RI non cumulativa, azioni 3.5.
4. `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md` — ✅ Azarr Kul fatto; Erinni/Avatar note.
5. `00_Red Hand Of Doom/Armate-UNITA-NUOVE/azarr-kul-final-cr15.md` — ✅ Tyrgarun coerenza fatta.

---

## 9. Cross-link

- **Errata gemella P1:** `ERRATA-PARTE1-Quest-Hellas-35-Verification.md`
- **Boss finale (in place):** `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md` §1
- **Canone Tyrgarun/Azarr Kul (D11 v2):** `campaign/state.md` §2, `PNG/Azarr_Kul/Azarr_Kul.md`
- **Schede PNG (fonti uniche):** `PNG/Xal_thor/Xal_thor.md` · `PNG/Sethrax_il_Velato/Sethrax.md`
- **Regole 3.5:** `skills/dnd-35-srd/` · `skills/dnd-35-rules/`

**Status:** ✅ **Errata prodotta; boss finale upscalato in place; catch Tyrgarun corretto.**
