# ARCO POST-HAMMERFIST — AUDIT DEL TESORO (WBL 3.5)

> **Versione**: v1 (2026-07-02) — task **B6** del `PIANO-REVISIONE-ARC09`.
> **Scopo**: portare l'economia del tesoro dell'arco (livelli **13 → 16**) in linea
> col **Wealth By Level** del DMG 3.5, e distribuire il loot **per incontro/quest**
> in stile Paizo (dove / cosa / valore).
> **Regola §0.3**: gli oggetti fuori SRD/DMG sono marcati `[INFERRED]`.

---

## 1. Il problema (evidenza)

`INDICE-GENERALE-COMPLETO-CAMPAGNA.md` §Loot dichiarava **~50.000 mo + 15-20 oggetti**
per **tutto** l'arco. È **sotto il WBL di un fattore ~8**.

### 1.1 WBL 3.5 (DMG, per personaggio)

| Livello | WBL/PG |
|---|---|
| 13° | 110.000 mo |
| 14° | 150.000 mo |
| 15° | 200.000 mo |
| 16° | 260.000 mo |

> **Nota**: alcune stampe del DMG danno 210k al 16°; uso la tabella con 260k al 16°
> e resto **conservativo** puntando alla **fascia bassa** (vedi §2). In entrambi i
> casi la conclusione non cambia: servono **centinaia di migliaia** di mo, non 50k.

### 1.2 Delta necessario per l'arco (party di 4 PG)

- Ricchezza attesa **all'ingresso** (13°): 110k × 4 = **440k** (già posseduta —
  include i 5 artefatti legacy, vedi §1.3).
- Ricchezza attesa **all'uscita** (16°): 260k × 4 = **1.040k** (fascia alta) /
  210k × 4 = **840k** (fascia bassa).
- **Delta da distribuire nell'arco**: **~400.000 – 600.000 mo equivalenti**.
- Obiettivo di questo audit (conservativo, fascia bassa, ±20%): **~380.000 mo
  equivalenti** distribuiti sulle quest. Con i drop già presenti nei file (non
  ri-contati qui) si resta nel corridoio WBL.

### 1.3 Gli artefatti legacy NON colmano il delta

I **5 artefatti legacy** (Aegis Fang, Corona di Adamantio, Anello di Chaotic
Illumination, Bracieri Gemelli, Collana) sono **già in mano ai PG al 13°**: fanno
parte della **ricchezza d'ingresso**, non di quella **guadagnata** nell'arco. Sono
inoltre **personali/non vendibili** → non liquidabili per comprare altro. Quindi
**non riducono** il delta di ~400k: l'arco deve comunque erogare loot nuovo.

---

## 2. Distribuzione del tesoro per quest (Paizo-style)

> **Pesatura (dal benchmark)**: **Rhest** (hoard del drago — il veicolo naturale del
> grosso), **Torre** (oggetti arcani di Zalkatar), **Torneo** (premi/scommesse),
> **Rethmar** (ricompense civiche/bottino di battaglia). Le side-quest completano.
> Valori in **mo equivalenti** (coin + gemme + arte + oggetti liquidabili).

| Quest / fonte | Dove | Cosa (sintesi) | Valore (mo eq.) |
|---|---|---|---|
| **Sacred Forest (Hella, P1)** | Cerchio della Quercia; nido drow | Doni druidici, componenti rari, oggetti minori dei piromanti drow | **~25.000** |
| **Rhest — Saarvith** (P2-RHEST) | Campo di guerra sul lago | Arco lungo composito +3, pozioni, cifra di comando, gemme del riscatto | **~30.000** |
| **Rhest — Hoard di Regiarix** (P2-RHEST FASE4) | Tana sommersa del drago | **Il grande hoard**: monete, gemme, arte, 2-3 oggetti magici (vedi §3.1) | **~90.000** |
| **Torre Invisibile (Artemis, P2A)** | Laboratori/biblioteca di Zalkatar | Oggetti arcani, pergamene, bacchette, il "seme di Porta" (se recuperato) | **~70.000** |
| **Torneo di Dauth (Tordek, P2B)** | Borse, scommesse, premio del campione | Premio in mo, contratto mercenari, oggetto-trofeo dell'Orbe (scenico) | **~45.000** |
| **Sabotaggio Campi Drow + Missioni Brevi (P3)** | Campi drow, incontri di viaggio | Bottino misto, veleni, oggetti drow, taglie | **~35.000** |
| **Starsong Hill (elfi)** | Doni dei Tiri Kitor | Frecce speciali, mantello elfico, oggetto naturale | **~15.000** |
| **Ghostlord (Thornwaste)** | Tana "leone di pietra" | Oggetti druidici del lich, componenti, tesoro sepolto | **~25.000** |
| **Rethmar — bottino + ricompense civiche** (P3 finale) | Campo di battaglia + Consiglio | Salvage draconico, ricompense del Consiglio, **titoli/dominio** (C6) | **~45.000** |
| — | | **TOTALE distribuito** | **~380.000** |

> **Bilancio**: 380k ± 20% = **304k – 456k**, dentro il corridoio WBL della §1.2
> (fascia bassa). Se il gruppo salta quest (echi negativi), riceve **meno** loot —
> coerente col principio "ogni quest è un moltiplicatore" (§5 del piano).

---

## 3. Dettaglio dei due contenitori-chiave

### 3.1 Hoard di Regiarix (il pezzo grosso, ~90k)

Da benchmark, l'hoard di un drago nero è il veicolo naturale del grosso del loot.
Ripartizione tipo (DMG "hoard triplo" per CR 13, arrotondato):

| Voce | Valore |
|---|---|
| Monete (mp/mo miste, corrose dall'acido — ripulibili) | ~25.000 mo |
| Gemme (12-20 pietre, palude/rovine elfiche) | ~20.000 mo |
| Oggetti d'arte (reliquie elfiche di Rhest sommersa) | ~15.000 mo |
| **Oggetto magico 1** — armatura/scudo (es. *+2 resistenza all'acido*) | ~10.000 mo |
| **Oggetto magico 2** — arma o bacchetta | ~8.000 mo |
| **Oggetto magico 3** — meraviglioso (es. *lenti/anello* utility SRD) | ~12.000 mo |

> Tutti gli oggetti **da SRD/DMG**. Se il DM vuole un pezzo unico legato a Rhest
> elfica, marcarlo `[INFERRED]` e assegnargli un valore coerente.

### 3.2 Bottino della Torre di Zalkatar (~70k)

Zalkatar è uno **scienziato arcano**: il suo loot è **magia utility/consumabile**,
non tesoro da drago.

| Voce | Valore |
|---|---|
| Pergamene (divinazione, teletrasporto, planari) | ~15.000 mo |
| Bacchette (2-3, semi-cariche) | ~15.000 mo |
| Oggetti meravigliosi (aiuti allo studio: *lenti*, *veste*, *ioun stone* SRD) | ~20.000 mo |
| Componenti/materiali di laboratorio liquidabili | ~10.000 mo |
| **"Seme di Porta"** (se recuperato da Sethrax/Orbe) `[INFERRED — plot item, valore a discrezione]` | ~10.000 mo |

---

## 4. Aggancio a C6 (ricompense di dominio) e agli echi

- Le **ricompense civiche di Rethmar** (~45k della tabella) **includono** i benefici
  di dominio/titolo di **C6** (Custode di Rethmar, seggio, scuola/cerchio, rendita).
  Parte del "valore" è **rendita ricorrente** (es. 1.000 mo/mese) e **servizi**, non
  liquido — utile per ARC-10, non per WBL immediato: contarlo a parte.
- **Loot condizionato**: quest saltate = loot non ricevuto. La tabella §2 è il
  **massimo**; il DM sottrae le quest non giocate.

---

## 5. Azione sull'INDICE

`INDICE-GENERALE-COMPLETO-CAMPAGNA.md` §Loot aggiornato da "~50.000 mo + 15-20
oggetti" a **~380.000 mo equivalenti** distribuiti (coerente WBL 13→16), con rimando
a questo file. Il conteggio **oggetti magici** sale di conseguenza (l'hoard di Rhest
+ Torre da soli ne portano ~8-10).

---

## 6. Checklist di sessione (DM)

- [ ] Il gruppo è nel corridoio WBL a ogni salto di livello (14/15/16)?
- [ ] L'hoard di Regiarix è stato erogato per intero (è il pezzo grosso)?
- [ ] Gli oggetti sono **SRD/DMG** o marcati `[INFERRED]` con valore?
- [ ] Le quest saltate hanno **ridotto** il loot di conseguenza?
- [ ] Rendite/titoli di dominio (C6) contati **a parte** dal WBL liquido?

---

## 7. Cross-link

- **INDICE (§Loot):** `INDICE-GENERALE-COMPLETO-CAMPAGNA.md`
- **Rhest (hoard):** `Arco-Post-Hammerfist-P2-RHEST-FASE4-SAARVITH-REGIARIX-BOSS-CR13.md` · `...P2-RHEST-CONSEGUENZE-ESITI.md`
- **Torre (Zalkatar):** `Arco-Post-Hammerfist-P2A-Torre-PARTE4-FINALE-Boss-Zalkatar.md`
- **Torneo (premi):** `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md`
- **Ricompense di dominio (C6):** `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ESITI-CONSEGUENZE.md`
- **Regole tesoro 3.5:** `skills/dnd-35-srd/` (DMG WBL, magic item tables)
- **Stato PG / artefatti legacy:** `campaign/state.md` §6 · `skills/rumblingstone-campaign/references/campaign-party.md`
