Arco-Post-Hammerfist-HOOKS-INTEGRATION-MASTER.md
=================================================

# Master DM Reference — Hook Integration Post-Hammerfist (v2)
## *Quando, dove, e attraverso chi i 4 PG ricevono i loro hook personali. Coerente con il piano del Red Hand of Doom. No railroad — il party può scegliere split, together, o hybrid.*

> **Status:** canone di campagna RumblingStone (2026-05-04, **rivisto v2**). Questo file è la **fonte autoritativa** per il tempismo e la consegna degli hook personali dei 4 PG nell'arco post-Hammerfist (Arco 09).
>
> **Tono di riferimento:** *Andor* (intel arriva tardi, mai gratis) + *House of David* (i messaggeri sono persone, non meccaniche) + *Tolkien* (lunghe strade portano i loro fardelli).
>
> **Patto di mastering:** ogni hook è **una porta che si apre, mai una mano che spinge**. I PG possono ignorare ogni invito. Il party può **stare insieme** o **separarsi**. Le **conseguenze** dell'ignorare emergono lente.

---

## TL;DR — DM Quick Reference (1 pagina)

```
WHEN → WHERE → WHAT → WHO
─────────────────────────────────────────────────────────────
Day 19  Hammerfist battle won (Sessione 4).
        Lythiel arrives with elven rangers on giant owls.

Day 21  CERIMONIA DELLE 100 ASCE (Hammerfist).
        ├─ Hella    → Acorn from Lythiel (post-cerimonia, intimate)
        ├─ Thorik   → Brenna's private letter from Tempestas + intel exchange
        ├─ Artemis  → Ring of Chaotic Illumination vibrates (Atto 3)
        └─ Tordek   → no formal hook — only Custode Eterno rune

Day 22-23 (notte) — Artemis: Sogno della Doppia Maschera
        (Lathander + Mask reveal Zalkatar's identity)

Day 22  Tempestas departs. Party decides PATH (split / together / hybrid).

Day 24  SACRED FOREST arrival (for those who go).
        ├─ Tordek   → Sorella Maewen offers Tournament invite
        │            (mythic 100-year cadence, 4 days notice)
        └─ Optional: drow scout encounter for Artemis if heading to Tower

Day 25  Saraah's RITO DI DIVINAZIONE.
        ├─ Hella   → 3 visions: Rhest base / Mother of Fungi / Talar in fiamme
        ├─ Hella   → optional EL-11 descent under Quercia Vecchia
        └─ Artemis → optional 4th confirmation of Tower direction

Day 23-28 (anywhere on the road)
        └─ All PG  → Ghostlord refugee caravan (Ren Casadipietra + 30)
                     heading for Talar (which is already sacked)

Day 28-32  Tournament Days 1-3 at Dauth (P2B arc).
Day 32     Vanguard Karruk siege of Dauth (parallel to Day 3 Tournament).
Day 33-35  Hella ritual / Artemis Tower fight.
Day 36+    Convergence on Rethmar.
Day 38-42  Phase 0-4 of Rethmar.

PATHS (party choice):
  PATH-A   split classico (efficient, no support)
  PATH-B   together-sequential (united, but timing-stretched)
  PATH-C   hybrid 2+2 or 3+1 (compromise)

DELIVERY DESIGN (fixed by v2):
  • Tempestas — INTEL AGENT for Rethmar. Carries ONLY Brenna's letter
    to Thorik. Drow chatter for Artemis is MATERIAL CONFIRMATION (not
    initiation), surfaced when Artemis asks or when Tempestas notes
    the Ring glow at the cena.
  • Sal — explicitly NOT a messenger (compromised by Il Collezionista).
  • Lythiel — Hella only (druidic affinity).
  • Maewen — Tordek only (coincidentally found at Sacred Forest).
  • Anello + Sogno + Lathander/Mask — Artemis only (internal + divine).
  • Ren Casadipietra — whole party (encounter-on-road).
```

---

## 1. Cornice strategica — Il calendario del Red Hand

> Tutto il calendario degli hook è ancorato al **Clock di Azarr Kul (9/18 giorni)** in `campaign/state.md`. L'orda principale arriva a Rethmar al riempimento del clock. Ogni hook deve essere consegnato **prima** che gli archi convergano verso Rethmar (P3).

### 1.1 Tempi canonici (post-Hammerfist)

```
Giorno 19  Vittoria a Hammerfist (Sessione 4 della battaglia).
           Lythiel arriva con i 12 ranger sui gufi giganti.
           Azarr Kul a 18 giorni da Rethmar.
Giorno 20  Nimon's Gap caduta. Talar minacciata.
Giorno 21  CERIMONIA DELLE 100 ASCE a Hammerfist.
           - Tempestas arriva con missione intel + lettera Brenna a Thorik.
           - Lythiel partecipa, consegna la Ghianda a Hella.
           - Anello di Artemis vibra (Atto 3).
           - Nessun hook formale per Tordek qui.
           Talar saccheggiata (i druidi non sanno ancora).
Giorno 22  Hammerfist a riposo. Tempestas riparte (mattina).
           Lythiel parte verso Sacred Forest avanti del party.
           Party decide architettura del viaggio (vedi §4).
Giorno 23  Partenza dei PG (in qualunque architettura).
Giorno 24  ARRIVO AL SACRED FOREST (per chi ci va).
           - Sorella Maewen atterra in cerca di Aeleth Verdebronzo.
           - Scopre che Aeleth è morto. Riconosce Tordek (se presente)
             come "Pugno di Pietra del Nord" sulla sua lista. Offre
             invito al Torneo di Dauth.
Giorno 25  RITO DRUIDICO DI HELLA + DIVINAZIONE DI SARAAH.
           - Saraah rivela: base Red Hand a Rhest + ombra scura
             sul Cerchio + visione Talar in fiamme.
           - Opzionale: encounter Mother of Fungi sotto la Quercia.
Giorno 23-28 Possibili incontri sulla strada:
           - CAROVANA PROFUGHI dal Thornwaste (Ghostlord hook).
           - Drow scout per Artemis (se va alla Torre).
           - Voci della strada per Tordek.
Giorno 28  Arrivo a Dauth (per chi ci va al Torneo) — preliminari.
Giorno 30  Cerimonia apertura Torneo (Day 1).
Giorno 31  Day 2 Torneo.
Giorno 32  Day 3 Torneo + assedio Vanguard a Dauth.
Giorno 33-35  Hella completa rituale Sacred Forest;
              Artemis affronta Zalkatar nella Torre Invisibile
              (se entro Mirtul = ~Day 30, altrimenti Torre cammina).
Giorno 36  Convoglio dei superstiti del Torneo parte per Rethmar.
Giorno 37  Convergenza dei PG verso Rethmar.
Giorno 38–40  Notte dei Drow (Phase 0) + Assedio (Phase 1).
Giorno 41  Riti & Avatar (Phase 2–3).
Giorno 42  Mythal & finale (Phase 4).
```

> **Nota DM:** la Vanguard del Red Hand è una **forza distaccata** (~600 effettivi). NON è l'orda principale di Azarr Kul. È un **diversivo** mandato a colpire Dauth.

---

## 2. Lo schema dei 4 hook personali (revised v2)

| PG | Hook | Dove atterra | Quando | Fonte |
|---|---|---|---|---|
| **Hella** | Ghianda del Cerchio | **Cerimonia delle 100 Asce** (Hammerfist) | Giorno 21 | **Lythiel** (in persona) |
| **Hella** (rinforzo 1) | Cenere implicita | Sacred Forest, Giorno 25 | Giorno 25 | **Saraah** (rito di divinazione) |
| **Hella** (rinforzo 2) | Visione Talar in fiamme | Sacred Forest, Giorno 25 | Giorno 25 | **Saraah** (rito di divinazione) |
| **Hella** (rinforzo 3) | Mother of Fungi sotto la Quercia | Sacred Forest, Giorno 25 | Giorno 25 | **Saraah** (rito di divinazione) |
| **Tordek** | Sigillo Torneo Dauth | **Sacred Forest** | Giorno 24 | **Sorella Maewen** (per coincidenza) |
| **Artemis** | Vibrazione Anello + voce drow antica ("Lui sta camminando. Vieni.") | **Cerimonia delle 100 Asce** Atto 3 | Giorno 21 | **Anello stesso** (interno, no NPC) |
| **Artemis** (conferma 1) | Sogni progressivi notte dopo notte | Notte 22-25 | Notte 22-25 | **Sogno** (interno, no NPC) |
| **Artemis** (conferma 2) | **Sogno della Doppia Maschera — Lathander + Mask offrono insight su Zalkatar** (identità, movente, cortesia futura) | Notte 22 o 23 | Notte 22-23 | **Lathander + Mask** (visione divina, no patto) |
| **Artemis** (conferma 3) | Conversazione drow intercettata 3 settimane fa + mappa approssimativa Cannath Vale Nord | Hammerfist (cena) | Giorno 21-22 | **Tempestas** (su richiesta o nota Anello brillare) |
| **Artemis** (conferma 4 opz.) | Direzione Torre via rito druidico | Sacred Forest, Giorno 25 | Giorno 25 | **Saraah** (rito druidico) |
| **Thorik** | Lettera privata Brenna | **Cerimonia delle 100 Asce** (sala-mappa) | Giorno 21 | **Tempestas** (mission ufficiale) |
| **Thorik** (continuazione) | Scambio intel bidirezionale | Hammerfist | Giorno 21-22 | **Tempestas** (mission dichiarata) |
| **Tutti** | Carovana profughi dal Thornwaste | Strada, Giorno 23-28 | A scelta DM | **Ren Casadipietra** (PNG-incontro) |

> **Confronto con v1 (deprecata):** la v1 prevedeva 4 lettere consegnate da Tempestas. La v2 distribuisce gli hook in **fonti diverse e plausibili**, riducendo Tempestas alla **sua reale funzione** (intel agent + lettera Brenna).

---

## 3. La Cerimonia delle 100 Asce come zona di atterraggio principale (Giorno 21)

> Vedi `08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md` per il file completo.

**Cosa atterra alla Cerimonia:**
- **Hella** riceve la Ghianda da Lythiel (post-cerimonia, intima).
- **Thorik** riceve la lettera privata di Brenna da Tempestas + scambio intel bidirezionale (sala-mappa, prima della cerimonia o durante banchetto).
- **Artemis** sente la vibrazione dell'Anello (Atto 3, durante il riconoscimento del Custode Eterno) — voce drow antica: *"Lui sta camminando. Vieni."* La notte successiva, sogno di **Lathander + Mask** (vedi `Arco-Post-Hammerfist-HOOKS-Artemis-TorreInvisibile.md` §3.4) che rivela identità e movente di Zalkatar. **Tempestas confermerà materialmente** con la conversazione drow intercettata 3 settimane fa, **se** Artemis lo cerca o se Tempestas nota l'Anello brillare alla cena.
- **Tordek** non riceve hook formale — solo la runa di Custode Eterno (atto pubblico).

**Cosa NON atterra qui:**
- L'invito di Tordek al Torneo (arriva al Sacred Forest, vedi §5).
- I drow scout per Artemis (vedi `Arco-Post-Hammerfist-HOOKS-Artemis-TorreInvisibile.md`).
- La carovana profughi (sulla strada, vedi `Arco-Post-Hammerfist-HOOKS-Ghostlord-Refugees.md`).

---

## 4. Architetture del viaggio (party-together vs split — anti-railroad)

> **Il party può scegliere come muoversi.** Tre architetture canoniche con costi diversi. **Nessuna è "giusta"** — sono trade-off.

### 4.1 PATH-A — *Split classico* (BG3-style efficient)

I PG si separano il Giorno 22-23.
- **Hella** → Sacred Forest (3 giorni viaggio, Giorno 23-25 arrivo).
- **Tordek** → Dauth direttamente, da solo (5 giorni viaggio, Giorno 23-27, arrivo Giorno 28).
- **Artemis** → Torre Invisibile, da solo (4 giorni viaggio veloce con Wings of Shadow, Giorno 23-26).
- **Thorik** → resta a Hammerfist o va a Rethmar (decisione di Thorik).

**Beneficio:** ogni arco si completa nei tempi. Possibile completare TUTTO prima di Rethmar.

**Costo:**
- **Tordek non incontra Maewen** (lei va al Sacred Forest, non a Dauth direttamente). Nessun sigillo formale → 150 lance senza copertura politica.
- **Hella non ha conferma di Saraah** se non chiama Tempestas via Polvere di Tonante.
- **Artemis arriva alla Torre con solo la vibrazione dell'Anello** — niente conferme esterne.
- **Drama RP del party diviso**: nessun PG ha supporto del proprio gruppo nei momenti critici.

### 4.2 PATH-B — *Together sequenziale* (party unito, archi a tappe)

Il party **resta unito**. Va a Sacred Forest per primo (Giorno 23-26 — rito + sub-quest Mother of Fungi). Poi va tutti insieme verso Dauth.

**Beneficio:**
- **Hella ha supporto del party** per Mother of Fungi (encounter EL 11 più gestibile).
- **Tordek incontra Maewen** al Sacred Forest → riceve invito ufficiale.
- **Artemis riceve conferma di Saraah** + (opzionalmente) si separa per la Torre il Giorno 26 mentre il resto va a Dauth.
- **Drama RP unito**: il party affronta i grandi momenti insieme.

**Costo:**
- **Tempo:** Hella + Sacred Forest + viaggio = il party arriva a Dauth solo Giorno 30-31. **Probabilmente perde Day 1 o Day 2 del Torneo.** Tordek deve fare le preliminari da solo o saltare.
- **Artemis ha finestra Mirtul stretta** (Day 30 = fine Mirtul). Se parte solo Giorno 26 dal Sacred Forest, arriva Torre Giorno 28-29. Stretto ma fattibile.
- **Niente sub-quest Beriah/Mask cult al Torneo** se Artemis va alla Torre invece di a Dauth.

### 4.3 PATH-C — *Hybrid* (2+2 o 3+1)

Compromesso: il party si divide in **2 gruppi**.
- **Esempio:** Thorik + Tordek vanno a Dauth (Tordek concorrente, Thorik supporta). Hella + Artemis vanno al Sacred Forest. Artemis si separa il Giorno 26 per la Torre, Hella torna verso Dauth o va direttamente a Rethmar.
- **Esempio variante:** Hella + Tordek vanno al Sacred Forest (Tordek riceve invito da Maewen). Thorik + Artemis vanno a Dauth (Artemis sub-quest Beriah). Tordek raggiunge Dauth Giorno 30+.

**Beneficio:** ognuno riceve il proprio hook organicamente (se ben coordinato). Drama RP gestibile.

**Costo:** **coordinazione di tavolo richiesta**. DM e giocatori devono concordare chi va dove.

### 4.4 Tabella di confronto

| Path | Hella ritual | Tordek invito | Artemis Torre | Thorik politica | Drama RP |
|---|---|---|---|---|---|
| A (split) | Solo, CD ↑ | NO sigillo (–150 lance) | OK ma alla cieca | Solo |  Diviso |
| B (together) | Pieno, CD ↓ | Sigillo via Maewen | Stretto Mirtul | Pieno |  Unito |
| C (hybrid) | Variabile | Variabile | Variabile | Variabile | Misto |

> **DM nota:** non spingere il party verso una path. Lascialo emergere dalla discussione di tavolo. Qualunque scelta sia gestibile narrativamente.

---

## 5. Salvatore (Sal) — perché NON usarlo come messaggero

> **Decisione canonica (mantenuta da v1):** Sal **non** consegna nulla ai PG.

### Ragioni (sintetiche):
1. **Sal è compromesso** — serve Il Collezionista e Sonjak. Far passare informazioni per le sue mani significa darle al nemico.
2. **Sal ha il proprio Clock attivo** (0/6 → Sabotage Oil su armi).
3. **Tono incompatibile**: Sal è teatrale e manipolativo. Tempestas e Maewen sono onesti.

---

## 6. Coerenza con il piano del Red Hand of Doom

### 6.1 Movimento dell'orda principale (Azarr Kul)

```
Giorno 19  Hammerfist (libera).  Azarr Kul a 18 giorni da Rethmar.
Giorno 20  Nimon's Gap caduta.
Giorno 21  Talar saccheggiata (al Cerimonia delle 100 Asce nessuno
           lo sa ancora — la notizia arriverà via Saraah Day 25
           o via la carovana profughi sulla strada).
Giorno 28  Distaccamento Vanguard di Wyrmlord Karruk a Dauth.
Giorno 32  Vanguard assalta Dauth (Day 3 Torneo).
Giorno 38  Azarr Kul arriva a Rethmar.
Giorno 42  Battaglia finale.
```

### 6.2 Cosa il DM deve ricordarsi

- **Se i PG ritardano l'arco P1 (Sacred Forest) oltre il Giorno 27**: rituale di Hella in pericolo.
- **Se i PG ritardano l'arco P2B (Torneo)**: Tordek squalificato (se ha l'invito) o non riconosciuto (se senza invito).
- **Se i PG ritardano l'arco P2A (Torre)**: Clock di Zalkatar (6/8 → 8/8) si riempie. La Torre **diventa mobile**.
- **Se i PG ignorano del tutto Tempestas**: Brenna pensa che Hammerfist non risponderà → Halveth domina → Phase 0 +2 difficoltà.
- **Se i PG ignorano del tutto Maewen**: Tordek senza invito → 150 lance senza copertura politica.
- **Se i PG ignorano del tutto Lythiel**: Druid Circle severo → Sacred Forest CD +4.

---

## 7. Scelte morali (Andor / House of David / LotR — riassunto)

> Ogni hook ha **GRAY-A / GRAY-B / DARK** branches. Vedi i singoli file per dettaglio.

| Hook | GRAY-A | GRAY-B | DARK |
|---|---|---|---|
| Hella + Lythiel | Accetta Ghianda; promessa a Saraah | Accetta usandola in modo non-canonico | Rifiuta |
| Hella + Saraah divinazione | Accetta tutte e 3 le visioni | Selettiva | Rifiuta rito |
| Hella + Mother of Fungi sotto Quercia | Discende e affronta | Lascia ai druidi | Ignora |
| Tordek + Maewen | Accetta sigillo, parte | Accetta + party intero a Dauth | Rifiuta |
| Artemis + Anello | Parte presto da solo | Resta col party, separa al Sacred Forest | Ignora completamente |
| Thorik + Brenna | Accetta lettera + va personalmente | Accetta con condizioni | Rifiuta |
| Thorik + scambio intel | Dà info veritiera, riceve | Niente scambio | Inganna Tempestas |
| Carovana profughi | Scorta a città sicura | Aiuto parziale (provviste, info) | Ignora |
| Carovana → indagare Thornwaste | Apertura precoce arco Ghostlord | — | — |

---

## 8. Echi a lungo periodo (BG3-style)

> Per la fonte autoritativa di tutti gli echi del Torneo: `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md`. Per gli echi specifici dei hook, vedi i singoli file.

Sintesi rapida per i 4 PG:

| Variabile | Eco a Rethmar |
|---|---|
| Lance Hammerfist (150) arrivano coperte politicamente | +150 difensori Phase 1 |
| Lance arrivano in caserma esterna (no copertura) | +150 ma in ritardo Day 3 + meno coordinati |
| Lance non arrivano (no invito) | +0 |
| Druid Circle reinforcement (Saraah) | +3 druidi + 6 Treant minori Phase 1 |
| Lythiel + 2 ranger Phase 1 | +1 squadrone aerea (CR 8 each) |
| Mother of Fungi spore distrutta sotto Quercia | Sonjak Phase 0 –1 CR effettivo |
| Mother of Fungi ignorata | Sonjak Phase 0 +1 CR effettivo |
| Saarvith disturbato a Rhest | Saarvith Phase 1 –1 CR (drago meno preparato) |
| Saarvith ignorato | Saarvith Phase 1 al CR pieno |
| Lorana mobilita Riserva volontari | +30 a +150 difensori (depending on relationship) |
| Lorana ignorata | +0 |
| Carovana profughi salvata (30 vivi) | +30 alla Riserva di Lorana + Joran CR 5 alleato |
| Carovana profughi ignorata (DARK) | +0; eco morale RP |
| Brenna alleata via lettera + intel scambio | +1 voto Consiglio (per la difesa); Phase 0 normale |
| Brenna ignorata | Halveth domina; Phase 0 +2 difficoltà |
| Sethrax catturato vivo (al Torneo) | Zalkatar P2A finale –1 CR |
| Sethrax fuga col seme (al Torneo) | Zalkatar P2A finale +2 CR |
| Tordek apre Porta 4 (al Torneo) | A Rethmar 1 ulteriore Risveglio Porta 4 a costo dimezzato |
| Tordek rifiuta Porta 4 | Rihan alleato CR 14 a Rethmar 1 fight |

---

## 9. Cross-link

- **PNG Tempestas (recurring intel agent):** `PNG/Tempestas/Tempestas.md`
- **PNG Lythiel (Hella's Hammerfist hook):** `PNG/Lythiel/Lythiel.md`
- **PNG Sorella Maewen (Tordek's Sacred Forest hook):** `PNG/Maewen/Maewen.md`
- **Hook Hella scena (Lythiel + Saraah):** `Arco-Post-Hammerfist-HOOKS-Hella-SacredForest.md`
- **Hook Tordek scena (Maewen al Sacred Forest):** `Arco-Post-Hammerfist-HOOKS-Tordek-DauthInvitation.md`
- **Hook Artemis scena (Anello vibra alla Cerimonia):** `Arco-Post-Hammerfist-HOOKS-Artemis-TorreInvisibile.md`
- **Hook Thorik scena (lettera Brenna + intel):** `Arco-Post-Hammerfist-HOOKS-Thorik-RethmarLetter.md`
- **Hook Ghostlord (carovana profughi):** `Arco-Post-Hammerfist-HOOKS-Ghostlord-Refugees.md`
- **Cerimonia delle 100 Asce (zona principale):** `08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md`
- **PNG Lorana (riserva profughi a Rethmar):** `PNG/Lorana/Lorana.md`
- **Battle of Hammerfist final phase:** `08_La Battaglia Di Hammerfist/00_Final_hammerfist_battle…`
- **Sacred Forest (P1) quest:** `Arco-Post-Hammerfist-P1A-Timeline-Quest-Hellas-COMPLETA.md`
- **Tournament (P2B) arc:** `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DM-MASTER-REFERENCE.md`
- **Torre Invisibile (P2A) arc:** `Arco-Post-Hammerfist-P2A-Torre-PARTE*.md`
- **Ghostlord arc files:** `Arco-Post-Hammerfist-P3-Ghostlord-LICH-ALLEANZA-TESTO.md`
- **Stato campagna:** `campaign/state.md`
