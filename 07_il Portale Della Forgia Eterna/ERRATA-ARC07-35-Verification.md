# ERRATA CORRIGE ARC-07 — Il Portale della Forgia Eterna (3.5 Verification)
## Correzioni meccaniche per conformità D&D 3.5 SRD (task B5)

> **Stato (B5)**: errata dell'arco, stesso formato di
> `09_.../ERRATA-PARTE1-...-35-Verification.md`. Copre: XP per incontro
> (APL 13/D15), statblock dei boss, CD delle prove, action economy, poteri
> della Corona (vs `campaign-artifacts.md`) e della **Cintura della
> Devastazione** (D17). **Le parti GIOCATE non si ritoccano**: dove serve si
> annota "giocato con i valori vecchi" senza retcon. Dove un valore
> non era attestato, quello proposto qui è stato confermato dal DM.

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
| Elder Fire Elemental (P3) | 14 | ~4.200/PG | GS = APL+2, "impegnativo" |
| Terros / Golem di Mithral (P4) | **CR 15+ "Hard"** (power-up voluto, D8) | ~4.800-6.000/PG | tienilo duro (§2.2) |
| Zog'tar (P5) | 14 | ~4.200/PG | risoluzione veloce (fast-play) |
| Skullcrusher (DEF-4 Scena 11) | **14** (Avanzato, vale 15) | **~1.460/PG**: 5.850 PX per un gruppo di 13° diviso per 4; con le 2 wyvern 6.500 → **1.625/PG** | Hella è tornata → 4 PG. Era GS 12 a ~2.700-2.925/PG; ricalcolato il 2026-10-19 sulla tabella PX del DMG (tab. 2-6), come in DEF-4 §8 A (D40) |

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

### 2.2 Terros / Golem di Mithral (P4) — POWER-UP VOLUTO (DM 2026-07-03)
- ⚠️ `_ARCHIVIO/Terros.md` era tarato su "Livello 14, 3 PC + Therysol". **Canone
  D8/D15**: **3 PG di 13°, NESSUN supporto → APL effettivo 12**. MA il
  **power-up è VOLUTO** (D8: artefatti unici e potentissimi): **tienilo duro**,
  **target CR 15+ ("Hard")** — NON depotenziarlo per far quadrare l'APL.
- **Igiene 3.5** (non depotenziamento): dichiara esplicitamente
  **Touch/Flat-footed/BAB/Lotta**; evita i termini 5e (max poteri speciali
  "puliti", niente "lair actions"). PF/RD/attacco possono restare alti se è
  ciò che serve per non chiudere in 2 round.
- **Nodo chiuso (2026-10-18)**: l'**Aura di Pietrificazione** (drenaggio DES
  = *save-or-die* **senza guaritore**) è stata giocata **letale**: Hella è
  morta nel P4, ed è canone. Il master vivo `ARC07-DEF-1` §7 non la riporta più,
  quindi per i gruppi futuri vale lo statblocco del master. La versione vecchia
  resta in `_ARCHIVIO/Terros.md` §3/§5.

### 2.3 Skullcrusher il Nero (duello, DEF-4 Scena 11) — GS 14 Avanzato
- **Statblock in vigore**: `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`, Appendice A.1
  `[CANONE — DM 2026-09-27; Q37 del 2026-10-07]`. Drago nero adulto maturo
  dell'SRD con il template **Avanzato** di PF1e, **GS 14**, CA 33 (contatto 10,
  impreparato 31), **37 con *armatura magica***, che al duello è già addosso;
  **297 pf** (22d12+154), morso +30 (2d8+10), soffio acido **14d4**, linea di
  30 m, **Riflessi CD 30** ½ (Capacità Focalizzata), aderente a scelta (*Soffio Aderente*, `[Private source — Draconomicon, p. 67]`, Boost log del 2026-10-19). Per il party straripante c'è il Vecchio e Avanzato
  di A.1-bis (GS 17). Per i numeri fa fede il master, non questa riga.
- **Versione precedente, superata**: fino al giro del 2026-10-19 questa sezione
  riportava lo statblock del `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md`, un drago
  nero adulto potenziato a **GS 12**, CA 27 (contatto 8, impreparato 25),
  **240 pf**, volare 36 m (scarsa), morso +26 (2d6+9), soffio acido 12d4
  (Riflessi CD 24 ½), Presenza Terrificante CD 22. Resta qui come traccia e
  non si usa al tavolo. Il file del Bestiario è stato rinominato il 2026-10-19 in
  `Bestiario/villain/skullcrusher-il-nero-cr14.md`, con 14 nel campo `CR`.
- Gli esiti del duello alimentano **B4** (carry-over su Fauci).

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
avanti (P3B/P5) e come riferimento per il DM. Le cifre non attestate sono
state confermate dal DM.
