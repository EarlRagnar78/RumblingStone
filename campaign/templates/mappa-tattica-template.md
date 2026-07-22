# TEMPLATE — MAPPA TATTICA (griglia + companion DM)

> **Scopo (T3, piano trasversale 2026-07-03)**: portare OGNI mappa tattica
> della campagna alla qualità delle mappe drow di ARC-09 e delle tattiche
> degli AP migliori (RHoD, Paizo PF1e): una griglia leggibile da un umano
> **più** un companion DM in tre blocchi — **Ambiente / Tattiche /
> Evoluzione** — così il master legge la mappa E sa come farla vivere.
> Benchmark interno: `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` (ARC-09).
>
> **Regole di compilazione**
> 1. La griglia markdown (emoji, 1 riga = 1 riga di quadretti numerata) è il
>    **MASTER**: umano-leggibile, diffabile, e renderizzabile in SVG con
>    `python3 scripts/render_map_svg.py <file.md>` (palette uniforme,
>    coordinate, barra di scala, legenda). L'SVG in `rendered/` è un
>    artefatto generato: **mai modificarlo a mano**.
> 2. Scala **1,5 m/quadretto** dichiarata in testa (convenzione repo).
> 3. Simboli: usare la **legenda universale** (quella dei campi drow); i
>    simboli locali extra vanno dichiarati nel blocco griglia.
> 4. Meccanica **3.5 SRD in italiano** (CD, Osservare, Nascondersi…); mai
>    inventare statblock — puntare al file `*STATBLOCCHI*` o al catalogo
>    (`scripts/monster_catalog.yaml`); ciò che manca si flagga
>    `[INFERRED — needs DM confirmation]`.
> 5. I tre blocchi companion stanno **nello stesso file della mappa**,
>    subito dopo la griglia: mappa e uso della mappa non si separano.

---

## [NOME MAPPA] — [Parte/Scena, Arco]

**Dimensioni**: [X]m × [Y]m ([C] colonne × [R] righe, scala 1,5 m/quadretto)
**Incontro**: [chi c'è — EL — link al file statblock]
**Quando si usa**: [scena/trigger — link alla parte master]
**SVG**: `rendered/[nome]_mapNN_[slug].svg` (rigenerare dopo ogni modifica)

### Griglia

```
[griglia emoji con COLONNE →  A B C … e righe numerate 01, 02, …
 callout inline per porte, trappole, pattuglie — stile Ultra-Clear]
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| Luce | … | [luce/oscurità, scurovisione a X m] |
| Terreno | … | [difficile ×2, copertura +4 CA, occultamento 20%…] |
| Pericoli | … | [danno/round, TS con CD, attivazione] |
| Rumore/odore | … | [modificatori ad Ascoltare/Osservare, CD] |
| Elevazioni | … | [+1 attacco da posizione alta, Scalare CD] |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

- **Disposizione iniziale**: [chi è dove e perché — coord.]
- **Round 1-2**: [reazione al contatto: chi carica, chi arretra, chi lancia]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [a quale soglia fuggono/si arrendono/chiamano aiuto — es.
  "sotto il 50% dei pf il comandante ordina il ripiegamento su …"]
- **Se i PG fanno X**: [1-2 contromosse alle tattiche ovvie del party —
  contro invisibilità, volo, evocazioni…]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [evento/round/allarme] | [celle che cambiano: fuoco si propaga, porta sfondata, rinforzi da …] | [nuove CD/danni/EL] |
| C | [evento] | … | … |

> Gli stati sono **esiti aperti** (principio D13): il trigger è dei dadi e
> delle scelte dei PG, mai del copione. Se uno stato altera l'EL, dichiararlo.

---
---

# ESEMPIO COMPILATO — Campo Drow 1: Burning Operations Base (ARC-09, P1C)

> Consolidato dal benchmark `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md`
> (nessun dato inventato: solo riorganizzato nei tre blocchi).

**Dimensioni**: 80m × 60m (53 colonne × 40 righe, scala 1,5 m/quadretto)
**Incontro**: 30 drow — 20 Guerrieri (Ftr 6-8), 8 Pyromancer (Wiz 8),
2 Commander (Ftr 10) — **EL 12 se tutti in allerta**
**Quando si usa**: sabotaggio opzionale pre-battaglia (P1C / P3 Sabotaggio)
**SVG**: `rendered/SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO_map01_….svg`

### 🌍 AMBIENTE

| Elemento | Dove | Effetto meccanico 3.5 |
|---|---|---|
| Foresta densa | perimetro (righe 01-03, colonne A-D/AS+) | Furtività +5, copertura totale oltre 4,5 m |
| Tripwire perimetrale | riga 04, colonne E-AJ | Osservare CD 22 per notarlo, Disattivare Congegni CD 20; se scatta: campana 🔔, TUTTI i drow in allerta, sorpresa persa |
| Fuochi tattici | area centrale 💥 (righe 20-23) | 1d6 fuoco/round nel quadretto, luce 18 m |
| Pattuglie | riga 06 (M06 e AI06, loop di 20 min) | Guerriero drow: Osservare +8, Ascoltare +8, scurovisione 36 m |
| Tende | righe 08-20 e 25-32 (blocchi ⬛ 3×3) | bloccano linea di vista; dentro: −4 Ascoltare per chi dorme |

### ⚔️ TATTICHE

- **Disposizione iniziale**: Commander a J25/J27; Pyromancer a O12, V12,
  U25, U27, M30 + 3 nelle tende; Guerrieri distribuiti su pattuglie e posti
  di guardia.
- **Approccio furtivo dei PG** (ordine consigliato dal file): eliminare le
  pattuglie PRIMA del tripwire → disattivare l'allarme (CD 20) →
  neutralizzare i Commander (senza di loro niente coordinazione) →
  sabotare scorte/armeria (rallenta l'orda).
- **Round 1-2 (se allarme)**: tutti i 30 drow in allerta entro 2 round.
- **Round 3+ (se allarme)**: formazione — Commander al centro, Pyromancer
  in seconda linea a distanza, Guerrieri a muro di scudi. Battaglia dura,
  EL 12 pieno.
- **Senza allarme**: i PG ingaggiano 5-6 drow alla volta (gestibile);
  bottino intatto (2.500 mo + mappe tattiche dell'orda + intel sugli altri
  2 campi).
- **Morale** `[INFERRED — needs DM confirmation]`: morti entrambi i
  Commander, i superstiti sotto il 25% ripiegano verso il Campo 2 (Hex D08)
  portando l'allarme.

### 🔄 EVOLUZIONE

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A — Notte, routine | — | pattuglie in loop riga 06; 2/3 delle forze nelle tende | sorpresa possibile, ingaggi 5-6 alla volta |
| B — Allarme | tripwire o pattuglia dà l'allarme (campana 🔔) | tutti fuori dalle tende in 2 round; formazione al centro campo | EL 12 pieno, niente sorpresa |
| C — Campo in fiamme | i PG incendiano scorte/fuochi tattici (💥 righe 20-23) | il fuoco si propaga 1 quadretto/round nelle celle adiacenti alle fiamme `[INFERRED]` | 1d6 fuoco/round per cella; fumo: occultamento 20% entro 3 m |
| D — Rotta | entrambi i Commander morti + superstiti <25% `[INFERRED]` | i drow superstiti fuggono verso NE (Campo 2) | se ne scappa anche uno solo: Campo 2 in allerta permanente |

---

> **Checklist di adozione per mappa esistente** (per i lotti del piano
> trasversale): ① scala dichiarata → ② simboli conformi alla legenda
> universale → ③ blocco AMBIENTE compilato → ④ blocco TATTICHE (fonte:
> sezioni tattiche/statblock esistenti; niente invenzioni) → ⑤ blocco
> EVOLUZIONE (2-4 stati) → ⑥ SVG rigenerato → ⑦ link incrociato dal file
> di parte (TESTO) alla mappa e viceversa.
