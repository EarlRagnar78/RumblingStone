# ERRATA CORRIGE ARC-07 — Il Portale della Forgia Eterna (3.5 Verification)
## Correzioni meccaniche per conformità D&D 3.5 SRD (task B5)

> **Stato (B5)**: errata dell'arco, stesso formato di
> `09_.../ERRATA-PARTE1-...-35-Verification.md`. Copre: XP per incontro
> (APL 13/D15), statblock dei boss, CD delle prove, action economy, poteri
> della Corona (vs `campaign-artifacts.md`) e della **Cintura della
> Devastazione** (D17). **Le parti GIOCATE non si ritoccano**: dove serve si
> annota "giocato con i valori vecchi" senza retcon. Valori proposti
> `[INFERRED — needs DM confirmation]` dove non attestati.

---

## 0. ACTION ECONOMY (globale) — terminologia 3.5

- ❌ "Bonus Action" / "Reaction" (termini 5e) → ✅ **swift action** /
  **immediate action**. ❌ CMB/CMD (Pathfinder) → in 3.5 usa **Lotta**
  (grapple modifier). I read-aloud narrativi non contano; contano gli
  statblock e le regole di scena.
- **§0 del piano** vieta già 5e: questa errata è la rete di sicurezza.

---

## 1. XP PER INCONTRO (APL 13 / composizione D15)

**Base 3.5 (DMG tab. 2-6)** — PG di 13°:

| Incontro | GS | XP/PG (party 3 PG, APL eff. 12) | Note |
|---|---|---|---|
| Elder Fire Elemental (P3) | 14 | ~4.200/PG `[INFERRED]` | GS = APL+2, "impegnativo" |
| Terros / Golem di Mithral (P4) | **target 14-15** (non 16) | ~4.200-4.800/PG | ricalibrato D15 (sotto) |
| Zog'tar (P5) | 14 | ~4.200/PG | risoluzione veloce (fast-play) |
| Skullcrusher (P5) | 12 | ~2.700-2.925/PG (party 4, APL 13) | Hella è tornata → 4 PG |

- **ERRORE da correggere**: `CORREZIONE-Boss-Fauci.md` assegna a un **GS 12**
  "**8.000 XP (2.000/PG)**". Per PG di 13° vs GS 12 il valore corretto è
  **~2.925 PE a testa** (~11.700 totali per 4 PG) — la cifra dichiarata è
  **sotto di ~30%** ed è comunque su un profilo (GS 12) **superato** (vale il
  GS 15 dell'ARC-08, A3). Correzione annotata in place nel file CORREZIONE.

---

## 2. STATBLOCK DEI BOSS — verifica

### 2.1 Elder Fire Elemental (P3, Fuoco) — GS 14 `[verify]`
- Base SRD: Elder Fire Elemental **24d8+120 = 228 PF**, CA 22 (tocco 12,
  impreparato 18), BAB +18, slam 2d8+7 (fuoco), Lotta +26. La versione
  potenziata dell'arco (RicalibrazioneScontri) alza i numeri: **dichiarare
  esplicitamente Touch/Flat-footed/BAB/Lotta** se si usa la versione avanzata.

### 2.2 Terros / Golem di Mithral (P4) — RICALIBRAZIONE D15
- ⚠️ `Terros.md` era tarato su "Livello 14, 3 PC + Therysol". **Canone
  D8/D15**: **3 PG di 13°, NESSUN supporto → APL effettivo 12**. Conseguenze
  già scritte in `Terros.md` (analisi CR): **target CR 14-15** (non 16); i
  problemi dello statblock RICALIBRATO (PF 380, RD 15/—, Attacco +32, Aura di
  Pietrificazione CD 24 senza guaritore) vanno **abbassati**:
  - PF ≈ 228-260 (Elder Earth base + avanzamento moderato), **RD 10/—**,
    Attacco ≈ +27, danno 2d10+11, **rimuovere l'Aura di Pietrificazione**
    (drenaggio DES = save-or-die senza Hella) o renderla non permanente.
  - Max 4 poteri speciali, non 6 (no "lair actions" 5e). Dettaglio già in
    `Terros.md` §3/§5.

### 2.3 Skullcrusher il Nero (P5, duello) — GS 12
- Statblock giocabile nel `PortaleForgia-P5-FASTPLAY.md`: Drago Nero Adulto
  potenziato **GS 12**, CA 27 (tocco 8, impreparato 25), **PF 240**, Volare 36
  m (scarsa), morso +26 (2d6+9), soffio acido 12d4 (CD 24 Rifl. ½), Presenza
  Terrificante CD 22. **Verifica**: coerente con un Drago Nero Adulto avanzato;
  BAB/Lotta da esplicitare se il DM vuole i sotto-modificatori. Gli esiti del
  duello alimentano **B4** (carry-over su Fauci).

### 2.4 Fauci di Palude (1372) — NON qui
- Profilo canonico **GS 15** nei file ARC-08
  (`00_Schede_dei_Personaggi_...` §FAUCI), modificato dalla tabella **B4**. Il
  profilo "GS 12" di P6/CORREZIONE è **storia superata** (A3). Un solo profilo
  vivo nel repo per il 1372.

---

## 3. CD DELLE PROVE

- Il **fast-play P5** usa CD fisse esplicite (prove di gruppo 18-22): OK 3.5.
- Le "prove God Mode" del `P5-RICALIBRATO` (sintesi) vanno lette con quelle CD
  esplicite del fast-play, non come "auto-successi".
- Viaggio dello spirito (canone giocato): TS Volontà **CD 18/20/20** +
  Conoscenze (religioni) **CD 15** — già espliciti e superati (risultati).

---

## 4. POTERI DELLA CORONA (vs campaign-artifacts.md)

- Coerenza verificata: **solo Topazio attivo** nell'ARC-07 in corso; Smeraldo
  si accende nel P4; **Rubino solo alla vittoria antica** (D5/D16, A4). La
  scheda `campaign-artifacts.md` tratta il Rubino come **single-use speso dopo
  l'arco**: la catena torna (nessun potere teorico/rimasto).

## 5. CINTURA DELLA DEVASTAZIONE (D17)

- = **Devastation Gauntlets** (MIC pag. 93), **slot cintura** (non mani), così
  i Bracieri restano alle mani. Poteri: **~3 cariche/giorno**, +2d6 danni "da
  devastazione" per carica `[verify valore esatto MIC]`; 4/giorno temporaneo
  dopo il rito della Sala (P2). Scheda:
  `PG/Artefatti/Artefatti-Pg/Tordek/00_Cintura_della_Devastazione.md`; riga in
  `state.md §6`.

---

## 6. NOTA SULLE PARTI GIOCATE

P1-P3, il viaggio dello spirito e il P4 in corso **sono stati giocati con i
valori dei file dell'epoca**: questa errata **non li retconna**. Vale da qui in
avanti (P3B/P5) e come riferimento per il DM. Ogni cifra non attestata è
`[INFERRED — needs DM confirmation]`.
