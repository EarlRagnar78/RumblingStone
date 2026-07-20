# PIANO — REINTEGRAZIONE PNG DELL'AP ORIGINALE (Red Hand of Doom) + Lirien

> **Creato:** 2026-07-20 · **Stato:** 🟡 in corso (Lotto R1 + R5 in questa PR)
> **Origine:** richiesta DM — «nell'avventura originale (Guado di Drellin e
> le altre località dell'AP) ci sono tanti PNG che nel repo mancano o sono
> persi. Reintegrarli per rendere il mondo più vivo; valutare l'inserimento
> di Lirien come PNG caotico che crei scompiglio.»
> **Vincoli:** coerenza (`skills/rumblingstone-campaign/references/campaign-coherence.md`),
> stile (`skills/rumblingstone-narrative-style/`), template
> (`campaign/templates/png-dossier-template.md`), regole IP (ADR-0005: mai
> testo AP verbatim — solo ruoli, adattamenti e puntatori `[Private — Red
> Hand of Doom]`).

---

## §1 — Perché quei PNG "mancano" (diagnosi, non colpa)

Tre cause concorrenti, tutte documentabili:

1. **La campagna è un adattamento, non una riesecuzione.** Gli archi 00-07
   hanno sostituito interi capitoli dell'AP con dungeon custom (Miniera,
   Cittadella, Tomba di Belkram, Forgia Eterna). I capitoli "cittadini"
   dell'AP (Guado di Drellin, Brindol) sono stati compressi: i PNG con una
   funzione al tavolo sono stati adattati o rinominati (Soranna Anitah →
   **Capitana Lorana**; Brindol → **Rethmar** col suo Consiglio, dove
   Jarmaath e Lady Kaal sopravvivono con nome originale), gli altri —
   i PNG "di colore civico" — semplicemente non sono mai emersi in gioco
   e non hanno mai ricevuto una scheda.
2. **La standardizzazione del Bestiario (lotti L0-L5, 2026-07) trascriveva
   solo ciò che esisteva già nel repo** (sorgenti `pregen-pcgen/`, statblock
   d'arco). I PNG presenti *solo nel manuale AP* non stavano in nessun file
   sorgente, quindi il censimento non li ha mai contati: debito invisibile.
3. **Il March Clock è già passato oltre le loro località.** Guado di
   Drellin è bruciato (Day 12-13), Terrelton è appena caduta (Day 19). La
   finestra in cui quei PNG vivevano "a casa loro" è chiusa — ma è
   un'opportunità, non una perdita: **~1.500 profughi del Guado sono in
   marcia/arrivati a Rethmar** (`campaign/state.md` §2.5). I PNG civici
   dell'AP rientrano come **volti dell'onda profughi** negli Archi 09
   (Day 20-42), esattamente il "mondo vivo" richiesto.

**Regola di reintegrazione (vale per tutti i lotti):** nessun destino viene
bloccato. Ogni PNG reintegrato ha `Status` con flag
`[INFERRED — needs DM confirmation]` e una sezione *Esiti possibili* (regola
D13 — mai copioni). Il DM canonizza al tavolo; finché non lo fa, nulla di
questo piano è canone.

---

## §2 — Censimento gap: PNG dell'AP ↔ stato nel repo

Legenda: ✅ = già a catalogo · 🔁 = rinominato/adattato (esiste) ·
❌ = assente (da reintegrare) · 🔗 = statblock d'arco esistente, manca solo
il dossier.

### §2.1 Guado di Drellin (Drellin's Ferry — nome mantenuto, vedi `fr-cannath-vale.md`)

| PNG AP | Ruolo AP | Stato repo | Azione |
|---|---|---|---|
| Capitana Soranna Anitah | capitano della guardia | 🔁 = **Capitana Lorana** (`png/Lorana/capitana-lorana-cr7.md`) | nessuna (canone) |
| Jorr Natherson | boscaiolo, guida del Witchwood | ✅ `png/jorr-natherson-cr7.md` | nessuna |
| Avarthel | druido mezzelfo, custode del ponte | ✅ `png/avarthel-druido-cr9.md` | nessuna |
| Morlin Coalhewer | fabbro nano | ✅ `png/morlin-coalhewer-cr12.md` (riusato fazione Dauth) | nessuna |
| **Norro Wiston** | Portavoce (capo politico) del Guado | ❌ (1 sola citazione in `dm-guide-to-be-adapted`) | **R1** ✅ |
| **Sertieren il Saggio** | mago halfling, saggio di Moonwatch Hill | ❌ (già *usato* dal `dm-expansion-toolkit` in 3 quest, senza scheda!) | **R1** ✅ |
| **Fratello Derny** | giovane chierico del tempio | ❌ | **R1** ✅ |
| **Delora Zann** | ex-avventuriera, stalliera/carrettiera | ❌ | **R1** ✅ |
| **Iormel** | possidente avaro | ❌ | **R1** ✅ |
| **Kellin Shadowbanks** | locandiere halfling del Vecchio Ponte | ❌ | **R1** ✅ |
| **Vecchio Warklegnaw** | gigante delle foreste del Witchwood | ❌ | **R3** ⬜ |

### §2.2 Rethmar (ex-Brindol)

| PNG AP | Ruolo AP | Stato repo | Azione |
|---|---|---|---|
| Lord Jarmaath | comandante/nobile | ✅ `png/Consiglio_Rethmar/` (seggio Militare) | nessuna |
| Lady Kaal | nobildonna | ✅ `png/Consiglio_Rethmar/` (Presidente) | nessuna |
| **Tredora Goldenbrow** | somma sacerdotessa (Pelor → **Lathander** in FR) | ❌ (1 citazione) | **R2** ⬜ |
| **Immerstal il Rosso** | mago cittadino | ❌ (1 citazione) | **R2** ⬜ |
| **Capitano Ulverth** | capitano della Guardia del Leone | ❌ (1 citazione) | **R2** ⬜ |
| **Teyani Sura** | ufficiale della Guardia del Leone (strada per Talar) | ❌ (1 citazione) | **R2** ⬜ |

Nota R2: il Consiglio di Rethmar ha già 7 seggi definiti (Sorvane, Pyriel,
Thornwall sono *sostituti funzionali* di alcuni ruoli AP). R2 reintegra i 4
sopra come **secondo anello** (tempio, torre di magia, caserma) senza
toccare i seggi — servono alle Fasi 0-4 della battaglia (guarigione di
massa, controspionaggio arcano, sortite).

### §2.3 Starsong Hill / Witchwood / Wyrmlord (villain)

| PNG AP | Stato repo | Azione |
|---|---|---|
| Sellyria Starsinger, Killiar Arrowswift, Illian Snowmantle | 🔗 statblock in `09_.../P3-Starsong-Hill-ALLEANZA-ELFI-STATBLOCCHI.md` | **R3** ⬜ mini-dossier cross-link |
| **Trellara Nightshadow** (barda Tiri Kitor in lutto) | ❌ | **R3** ⬜ |
| Vecchio Warklegnaw | ❌ | **R3** ⬜ (vedi §2.1) |
| Wyrmlord Ulwai Stormcaller | ❌ (4 citazioni, nessuna scheda) | **R4** ⬜ (villain/) |
| Wyrmlord Hravek Kharn | ❌ (1 citazione) | **R4** ⬜ (valutare: la campagna ha già Karruk custom — possibile fusione, decide il DM) |

---

## §3 — Lotti

- [x] **R1 — Profughi del Guado di Drellin** (questa PR): dossier collettivo
  `Bestiario/png/Guado_di_Drellin/Profughi_Guado_di_Drellin.md` — 6 PNG
  civici come volti dell'onda profughi Day 12→25, con agganci ai thread
  esistenti (mulino dei bambini, infiltratori §2.5, Morale Cittadino,
  Sertieren già citato dal dm-expansion-toolkit). Tutti `[INFERRED]`.
- [ ] **R2 — Secondo anello di Rethmar**: Tredora Goldenbrow (Lathander),
  Immerstal il Rosso, Capitano Ulverth, Teyani Sura — mini-dossier col
  template, agganci alle Fasi 0-4. Gate: nessuno (preparazione).
- [ ] **R3 — Witchwood & Tiri Kitor**: Vecchio Warklegnaw, Trellara
  Nightshadow + mini-dossier cross-link per i 3 elfi già statblockati.
  Gate: prima di giocare P3-Starsong (Day 30-35).
- [ ] **R4 — Wyrmlord mancanti (villain)**: Ulwai Stormcaller; decisione DM
  su Hravek Kharn vs Karruk. Gate: decisione DM.
- [x] **R5 — Lirien Amaranti, "Il Giullare Spezzato"** (questa PR): dossier
  `Bestiario/png/Lirien/Lirien.md` — PNG caotico neutrale ricorrente,
  proposta completa `[INFERRED — needs DM confirmation]`: adattamento FR
  del background, aggancio all'onda profughi, 3 intrecci con PNG esistenti
  (rete-statue di Varis/Sal, Tempestas, infiltratori §2.5), meccanica
  "scompiglio" a esiti aperti, guardia di protagonismo PG. Possibile
  promozione a PG in un futuro branch di gruppo.
- [ ] **R6 — Canonizzazione DM**: il DM rivede R1+R5, scioglie i flag
  `[INFERRED]`, e applica (a mano o via wizard) le righe proposte per
  `state.md` §3/§7 elencate nei dossier. Gate: **decisione DM** — fino ad
  allora nessun file di canone (`state.md`) viene toccato da questo piano.

**Regola d'oro:** ogni lotto chiuso aggiorna questa checklist +
`plans/INDEX.md` + `plans/CHANGELOG.md` nello stesso commit.

---

## §4 — Criteri di qualità (validi per ogni scheda reintegrata)

1. **IP-safe (ADR-0005):** ruolo e funzione, mai testo AP; stats solo come
   stima `[INFERRED]` o puntatore `[Private — Red Hand of Doom]`.
2. **Coerenza timeline:** nessun PNG può "essere ancora al Guado" — il
   paese è bruciato (Day 12-13, locked). Ogni scheda dichiara dove il PNG
   è *ora* rispetto al March Clock, con esiti alternativi (morto/disperso)
   lasciati al DM.
3. **Protagonismo PG:** i PNG reintegrati creano *situazioni*, non
   soluzioni. Nessuno di loro risolve una quest al posto dei PG (test di
   protagonismo della skill narrativa).
4. **Tre agganci minimi** per scheda: un thread esistente di `state.md`,
   un PNG già a catalogo, una fase/quest degli Archi 09.
