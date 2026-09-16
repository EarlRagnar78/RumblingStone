# Changelog dello stato di campagna — append-only

> Lo storico di `campaign/state.md`, scorporato il **2026-09-16** (lotto 4d-2,
> [ADR-0050](../plans/adr/ADR-0050-stato-di-campagna-dati-e-prosa.md)). Erano
> **1.179 righe, il 71%** di quel file: lo stato vivo non si leggeva piu' perche'
> la storia gli stava sopra.
>
> 🔴 **Append-only, e non e' una convenzione gentile.** Ogni riga e' un fatto
> gia' successo al tavolo. Non si cancella, non si riordina e non si
> ricompatta: quando una voce risulta sbagliata si **aggiunge** la correzione
> con la sua data, come si e' fatto il 2026-08-09 annullando l'eco E-07e.
>
> Ci scrive `scripts/state_apply.py`, che appende all'**ultimo** blocco. Le
> righe qui sotto sono quelle che stavano in `state.md` §8, **identiche byte per
> byte**: lo spostamento non ha riscritto niente.

Every state change goes here with date and one-line reason. Never delete
entries — they become campaign history.

```
2026-05-01  Initial state.md created (extracted from campaign-story-arcs.md
            + post-Hammerfist arc notes). Baseline = end of Hammerfist battle,
            party at Hammerfist Holds, Custodi Eterni granted.
2026-05-02  Added Salvatore "Sal" della Luna d'Argento as active villain thread
            (clock 0/6). Added to NPC knowledge table and open narrative threads.
            Files: PNG/Salvatore/Salvatore.md,
            09_Continuazione.../Arco-Post-Hammerfist-P2C-Salvatore-Mercante-TESTO.md
2026-05-02  Full PNG audit: created dedicated character sheets for all major
            villains/NPCs previously missing from PNG/. Files created:
            PNG/Azarr_Kul/Azarr_Kul.md (GS 15, boss Rethmar Phase 3),
            PNG/Sonjak/Sonjak.md (GS 13, Drow Matrona; clarified = Matrona Sajak),
            PNG/Conte_Valerius/Conte_Valerius.md (GS 6 combat / GS 14 political),
            PNG/Varis_Seta_Argento/Varis_Seta_Argento.md (CR 6, urban broker),
            PNG/Ghostlord/Ghostlord.md (GS 13, Lich druidico Thornwaste),
            PNG/Xal_thor/Xal_thor.md (GS 14, Illithid Githyanki commander).
            NPC knowledge table and open threads updated accordingly.
2026-05-03  DM confirmation: the Orbe delle Otto Porte is established
            as a **Githyanki artifact** (campaign canon, RumblingStone —
            not SRD/RHoD). [INFERRED — needs DM confirmation] markers
            removed from OTTO-PORTE-e-ORBE §2.1.1/2.1.2/2.1.3 and PARTE1.
            Origin promoted to canon in
            skills/rumblingstone-campaign/references/campaign-artifacts.md
            and §5 of state.md. All downstream mechanics (Vaereth's claim,
            Sethrax's "seme di Porta" extraction, Githyanki clock-advance
            rule, Eco delle Fenditure vision) are now established
            campaign canon.
2026-05-03  Code-review fixes on the Tournament ↔ Torre integration:
            - Typos in PNG/Sethrax_il_Velato/Sethrax.md (article gender,
              "priorità alla ritirata").
            - Sethrax's *Psionic Dimension Door* aligned to **3/giorno**
              across PARTE2 (was inconsistently 1/giorno) — PNG card and
              STATBLOCCHI now agree.
            - Xal'thor's role and motivation clarified in PNG/Xal_thor,
              state.md, PARTE3, and OTTO-PORTE-e-ORBE: he commands an
              **Illithid** invasion (psionic thralls + a small core of
              dominated Githyanki), NOT the free Githyanki dragon-rider
              force (that's Vaereth — separate and hostile). His unique
              tournament target is the **Bracieri Gemelli** of Tordek;
              he is NOT interested in the Orbe (that's Sethrax/Zalkatar
              and Vaereth) — removes the duplicate-motivation issue.
            - All inferred lore flagged with [INFERRED — needs DM
              confirmation] per AGENTS.md policy: Orb's Githyanki origin
              (OTTO-PORTE §2.1.1), the "Eco delle Fenditure" vision and
              the clock-advance rule (PARTE1 + OTTO-PORTE §2.1.2/2.1.3).
            - Consolidation: Sethrax.md is now the authoritative source
              for unmask triggers, psionic power limits, and cross-arc
              outcome table; OTTO-PORTE-e-ORBE §2.1.3 is the authoritative
              source for the Githyanki clock-advance rule. PARTE1, PARTE2,
              PARTE3, MINIMAPPA, STATBLOCCHI voce 10 now point to those
              sources instead of duplicating mechanics.
2026-05-03  Tournament ↔ Torre Invisibile integration. Added:
            - "Visione Githyanki — Eco delle Fenditure" mechanic (Day 1
              first-Porta-opening cutscene foreshadowing Day 3 Vaereth arrival)
              in PARTE1-Giorno1-Preliminari.md.
            - Orb's Githyanki planar origin lore (it was a ki-psionic resonator
              for Githyanki dragon-riders) in OTTO-PORTE-e-ORBE.md §2.1.1.
            - New PNG: Sethrax il Velato (CR 12, Mind Flayer Psion 5,
              Zalkatar's emissary), infiltrated as masked finalist "Kethran
              Mano di Pietra". Files: PNG/Sethrax_il_Velato/Sethrax.md,
              statblock in STATBLOCCHI-COMPLETO.md voce 10, hooks in
              PARTE2-Giorno2-Semifinali.md (introduction + clues),
              PARTE3-Giorno3-Finale-e-Invasione.md (auto-unmask Round 7,
              triangle of factions), MINIMAPPA-TIMELINE-ALLEANZE.md.
            - Updated PNG/Xal_thor/Xal_thor.md with rival illithid faction
              section (two illithid conclaves do NOT collaborate at Dauth).
            - New villain clock: Sethrax (sync to Tournament).
            - New NPC knowledge rows (Zalkatar via Sethrax; Sethrax's
              own observations of Tordek + Orb).
            - New open narrative thread: cross-arc Tournament ↔ Torre
              Invisibile (Sethrax's fate determines Zalkatar's CR for
              Artemis's P2A finale).
2026-05-04  Post-Hammerfist hooks integration. Canonized two recurring NPCs
            and four PG-personal hook scenes that tie each PG's quest
            track into the Red Hand of Doom timeline (anchored to Azarr
            Kul Clock 9/18 and the Vanguard distaccamento Day 28→33).
            Files added (09_Continuazione.../):
            - HOOKS-INTEGRATION-MASTER.md (DM canonical schedule:
              Hammerfist → Day 22 4 letters → Day 23 split → Day 33
              double climax → Day 38 Rethmar; Sal explicitly NOT used
              as messenger to avoid leak to Sonjak)
            - HOOKS-Hella-SacredForest.md (Lythiel Day 19 Acorn drop +
              Tempestas Day 22 white ash + 3 travel choices)
            - HOOKS-Tordek-DauthInvitation.md (Tempestas delivers
              official Dauth Tournament seal from Magister Veylan +
              Sovrintendente Tordek; refusal cancels 150 lances)
            - HOOKS-Artemis-TorreInvisibile.md (Tempestas's leather
              map of Cannath Vale north + intercepted drow chatter
              about "il dottore della torre invisibile" wanting "il
              portatore dell'anello caotico"; deliberately avoids
              Day 3 overload — keeps Beriah/Mask cult only at Dauth)
            - HOOKS-Thorik-RethmarLetter.md (Brenna Sorvane's private
              sealed letter: 3-4 Council split, Halveth corrupt,
              Lorana alive, request for King Thorek alliance + 150
              lances + Thorik in person)
            New PNG cards:
            - PNG/Tempestas/Tempestas.md (canonized as the "bard
              storm caller" who helped the party escape Lorana's
              city in Arco 00; multi-arc messenger via Shadow Walk;
              GS 14; Cantata della Tempesta Tonante; mental erosion
              vulnerability; 5-charge Polvere di Tonante channel)
            - PNG/Lythiel/Lythiel.md (Wood Elf Ranger 8, Sacred
              Forest druidess-mancata, one of the 12 elven rangers
              on giant owls at Hammerfist Sessione 4 final phase;
              keeper of Saraah's Acorn for Hella; CR 8)
            New active companion entry in §1: Tempestas (recurring,
            not constant). New NPC knowledge rows in §3 (Lythiel,
            Tempestas, Brenna). New open narrative threads in §6:
            6 [HOOKS ↔ *] threads.
            Decision documented: Salvatore "Sal" is NOT used as
            tournament-invitation messenger because he is compromised
            (employed by Il Collezionista + Sonjak); Tempestas serves
            that role exclusively.
2026-05-04  Hooks integration v2 — major refactor of motivation
            and delivery (per DM critique: "why would Tempestas
            deliver letters that aren't his job?"). Changes:
            - Tempestas's mission narrowed: he is an INTELLIGENCE
              AGENT for Rethmar (Brenna Sorvane), not a delivery
              service. Carries ONLY one letter (Brenna → Thorik).
              Primary mission at Hammerfist: honor the dead +
              gather Red Hand intel from Thorik (bidirectional
              exchange: he offers Halveth corruption + Lorana alive
              in return). The drow chatter intel (intercepted 3
              weeks ago in Shadow Walk, Cannath Vale Nord) is
              MAINTAINED but reframed as material confirmation
              for Artemis's Ring vibration, surfaced only when
              Artemis asks OR when Tempestas notes the Ring glow
              at the cena di Hammerfist (Sapienza Magica CD 14).
            - Tordek hook RELOCATED: invitation no longer comes
              from Tempestas at Hammerfist. Comes from new NPC
              Sorella Maewen "Pugno-di-Cedro" (Mezza-elfa Monk 9/
              Cleric 2 of Ilmater, GS 10) — Confraternita
              Monastica di Dauth courier who arrives at Sacred
              Forest Day 24 looking for Aeleth Verdebronzo (dead),
              recognizes Tordek by Custode Eterno rune as the
              4th invitee on her list. Tournament reframed as
              MYTHIC: once every 100 years at Iride star
              alignment, 4 days notice, open to all valorous
              warriors who pass monastic preliminaries (non-
              monks at disadvantage with documented CD modifiers).
              Files: PNG/Maewen/Maewen.md (full PNG card with
              5-invitee list as worldbuilding datapoints).
            - Artemis hook fully INTERNAL: Ring of Chaotic
              Illumination vibrates during Cerimonia delle 100
              Asce Atto 3 (Re Thorek hands runa di pietra). Voice
              "Lui sta camminando. Vieni." in drow antico. Plus
              new SOGNO DELLA DOPPIA MASCHERA Notte 22-23: both
              Lathander and Mask appear in dream with insight on
              Zalkatar (3-century ex-cleric of Mask, became Mind
              Flayer by choice, wants to READ Artemis not kill
              him). Mechanical bonus: +2 TS Vol vs Zalkatar
              psionics; +1d6 first attack each round Phase 3 of
              Tower fight (+2d6 if Atto 2 sub-quest done).
              Tempestas drow chatter MAINTAINED as material
              confirmation. Saraah druidic divination at Sacred
              Forest is third optional confirmation.
            - Hella hook EXTENDED: Lythiel Acorn at Cerimonia
              (canon, kept) + Saraah's RITO DI DIVINAZIONE Day 25
              at Sacred Forest revealing 3 visions (Red Hand base
              at Rhest with Wyrmlord/black dragon; dark shadow
              under the Quercia Vecchia = Mother of Fungi spore
              by Sonjak's drow; Talar in fiamme = already
              destroyed). Optional Mother of Fungi descent
              encounter EL 11. Bonus narrative: Sacred Forest
              ritual base bonus DOUBLES if MoF purified.
            - NEW: HOOKS-Ghostlord-Refugees.md — refugee caravan
              from Loccatella (fled Lich's undead waves out of
              Thornwaste) heads to Talar not knowing it's been
              sacked. 4 PG-party choices (escort to safe city /
              investigate Thornwaste = early Ghostlord arc /
              partial aid / ignore). Echoes: +30 to Lorana's
              Riserva at Rethmar; possible Joran ex-druid CR 5
              ally; Tobi child as RP callback.
            - Master Integration v2: 3 architectures (PATH-A
              split / PATH-B together-sequential / PATH-C hybrid)
              with explicit costs. No railroad. Cerimonia delle
              100 Asce becomes the canonical landing zone for
              Hella + Thorik + Artemis hooks (3 of 4); Tordek's
              landing zone is Sacred Forest.
            - Cerimonia delle 100 Asce canonized as Day 21 closing
              event of Arc 08, file in 08_La Battaglia Di
              Hammerfist/Cerimonia-delle-100-Asce.md (210 dead
              honored with 100 ceremonial axes; party formally
              recognized as Custodi Eterni with rune di pietra).
            New NPC knowledge rows in §3: Maewen, Lathander+Mask
            divine awareness. Tempestas row revised. New PNG
            cards: PNG/Maewen/Maewen.md.
2026-05-05  Army sync v2 — DM realignment: horde baseline rescaled from
            6.161 (AP-original) to ~10.000 (coherent with scaled Channath
            Vale cities); ratio target 3:1-like from Hammerfist (900/300)
            up to max 6:1 worst case / 1.55:1 legendary; PG choices now
            meaningfully shift balance. Introduced DUAL CLOCK separation:
              - MARCH CLOCK (official AP): Day 1 → Day 40 Rethmar
                encampment. Current sync point: **Day 19 = Terrelton
                falls = end of Battle of Hammerfist**.
              - RITUAL CLOCK AZARR KUL: /18 independent (rituals only,
                does NOT advance with march).
            Dragon contingent set at 5 AP-original upscaled: Abithriax
            (Red adult), Regiarix (Black young — Rhest), Ozyrrandion
            (Blue — Tower), Tyrgarun (reserve), Fauci di Palude (Black
            adult, Hammerfist vanguard). Draconic spawn = 8 Razorfiend
            (Tiamat colors) assigned to Wyrmlord villains upscaled.
            NEW: "Compagnia del Teschio Nero" — 650 evil human
            mercenaries (Thay/Mulhorand) joining for power/money.
            Gnoll mercenaries expanded to 1.100 (3 tribes).
            Ghostlord logic: if neutralized by PG → only 400 undead
            already pre-deployed remain; default hostile → +2.400
            undead wave at Rethmar Phase 2.
            No PG interference at Skull Gorge bridge (confirmed). No
            giant alliance PG-side (giants stay with Red Hand).
            Files created/replaced:
            - 00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md
              (rescaled 10k + dragons + Razorfiend + Teschio Nero +
              conditional additives table)
            - 00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md
              (AP March Clock Day 1→40 waypoint ledger)
            - 09_Continuazione.../Arco-Post-Hammerfist-P3-BATTAGLIA-
              FINALE-ARMATE-SYNC.md (5 PG scenarios, force balance)
            §2 Active Forces tracker replaced with dual-clock version.
2026-05-05  Added §2 Active Forces — Live Army Tracker to state.md as the
            session-by-session source of truth for force sizes. Created:
            - 00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md:
              full initial composition (6,161 total), deployment table
              (Hammerfist 793/Dauth 575), dynamic march attrition by week,
              defender coalition scenarios, Dauth multi-faction breakdown.
            - 00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md:
              battle log waypoint-by-waypoint (Nimon Gap ✅ → Drellin ✅ →
              Skull Gorge 🔄 → Talar/Terrelton/Witchcross ⏳), refugee flow
              table (~5.300 civili + ~495 armati verso Rethmar), cumulative
              loss table per scenario (3.783–5.053 MR a Rethmar), session
              checklist, infiltrati nell'onda rifugiati.
            - 00_Red Hand Of Doom/Armate-AGGIORNATO.ods: now 9 sheets
              (aggiunti Registro Battaglie, Rifugiati Rethmar, Tracker
              Dinamico). Forza garantita Rethmar aggiornata a 1.746
              (include rifugiati armati da Nimon+Drellin già arrivati).
            Current confirmed losses MR: −308 (Days 1-9, Nimon+Drellin
            +attrition). Main body: 4.793 → 4.485 active.
2026-05-05  Created DM-CAMPAIGN-PLAYBOOK.md (operational DM guide):
            pre/during/post-session workflow with 2 worked examples
            (session file + state.md diff), dual-clock quick reference,
            reset procedure for new groups (branch-per-group strategy),
            red flags. Added §0 Campaign Status At-a-Glance dashboard
            to state.md. Created templates (state-blank.md,
            session-template.md) and helper script
            scripts/new-campaign-group.sh for one-command group reset.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 1 (A1+A13): global
            spelling fixes, no canon change. "Regiarax" → "Regiarix"
            (D1) across campaign/, skills/, PNG/, 09_Continuazione/.
            "Rethman" → "Rethmar" (D2) across all P3 files; renamed
            Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-RETHMAN-STRUTTURA.md
            → ...-RETHMAR-STRUTTURA.md and updated all references.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 2 (A2+A10): clock
            coherence, no canon change (D6 already won via state.md §2,
            propagated to files that still disagreed). "Day 38/40"
            arrival-of-horde references → Day 42 in HOOKS-INTEGRATION-
            MASTER §1.1/§6.1, P3-BATTAGLIA-FINALE-RETHMAR-STRUTTURA r.12,
            ARMATE-SYNC §1/§2/§4-Fase1, Armate-SINCRONIZZAZIONE-CAMPAGNA
            §4b (Fase 1-3 all land on Day 42 per D13's compressed 3-day
            rhythm), DM-QUICKSTART-ARC09. A10: ESITI-CONSEGUENZE §6
            reworded ("costruire un Fane" → "rifortifica il Fane nel
            Shaar + avamposto avanzato", since the Fane already exists
            per §2.1 Day 1). §3 Azarr Kul row relabeled as the Ritual
            Clock (was ambiguously worded as a march countdown) with
            explicit advance triggers cross-referenced to Armate-
            SINCRONIZZAZIONE-CAMPAGNA §4b.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 3 (A3+A5+A11):
            INDICE-GENERALE refresh, no canon change (all values already
            correct in state.md, only INDICE was stale). A3: Torre/Rhest/
            Torneo durata windows updated to match state.md §0 (Day
            28-35 / 25-32 / 25-34), citing HOOKS-INTEGRATION-MASTER §1.1
            for detailed chronology. A5: Ghostlord numbers in INDICE and
            Ghostlord-LICH-ALLEANZA-TESTO §6 updated to D7 (+2,400
            ostile / +400 neutralizzato / +600 pro-difensori se redento).
            A11: INDICE "Finale improvviso" del Torneo riscritto per
            separare le due fazioni Day-3 fuse per errore (Xal'thor
            Illithid vs Vaereth Githyanki, D5), aggiunto lo smascheramento
            di Sethrax al Round 7.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 4 (A4+A12): no canon
            change. A4: ESITI-CONSEGUENZE §7 usava nomi di PG (Tordek,
            Artemis) come PNG — artefatto di generazione. Sostituiti con
            Sellyria Starsinger/Killiar Arrowswift (leader Tiri-Kitor,
            già canonici in Starsong-TESTO), Magister Veylan [INFERRED]
            (Dauth) e Borin Tozzefort [INFERRED] (comandante 300 nani
            mercenari), incluso il monologo "Vittoria Tattica" che citava
            "Artemis Learmount" come parlante. Corretti anche i refusi
            della sezione (gloriosa-mente, nega-zia, complètamente, lo
            prezzo, stravagato). A12: banner DEPRECATED aggiunto a
            inizio.md e Quest 1 – Druida Hellas (brainstorm storico
            pre-canone, code conversazionali AI rimosse), INDICE li
            etichetta "storico/deprecato".
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 5 (A8+A9): no canon
            change. A8: 3 link rotti a file mai creati (P2B-Torneo-DAUTH-
            CONSEGUENZE-ECHI-LUNGO-PERIODO, -DM-MASTER-REFERENCE,
            -SUBQUEST-Thorik) ripuntati a file esistenti equivalenti
            (MINIMAPPA-TIMELINE-ALLEANZE, PARTE1-3, HOOKS-Tordek-
            DauthInvitation §4). Nota: uno scan repo-wide ha trovato
            altri 5 link rotti (SUBQUEST-Artemis, SUBQUEST-Hella,
            DAY3-DAUTH-CITY-SIEGE, + 2 duplicati) che referenziano
            sotto-quest MAI scritte (non solo rinominate) — richiedono
            contenuto narrativo nuovo, fuori scope per un lotto
            meccanico; lasciati per una sessione dedicata.
            A9: SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO-Description.md
            (0 byte) riempito con le descrizioni narrative dei 3 campi
            drow (il gemello COMPLETO.md ha già mappe/statistiche).
            PARTE1-to-Be_integrated.md marcato DEPRECATED (bozza pre-
            canone: Tetsu/Rihan già adottati nel canone altrove, il
            resto superato da OTTO-PORTE-e-ORBE + PARTE1-3), corretto
            l'unico 5e-ismo reale (attacco "con vantaggio" → regola
            SRD 3.5 di elevazione) e ripulite le code conversazionali.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, sessione 6 (A6+A7) — ULTIMA
            SESSIONE DEL LOTTO A, tutti i 13 task A1-A13 completati.
            A6 (D9/D10): elfi Tiri Kitor +500 → **+120** (100 ranger +
            20 gufi giganti, 1/5 di una tribù di ~500 anime) in state.md
            §2.4, INDICE, STRUTTURA §8, ARMATE-SYNC §2/§4. Nani +400 →
            **300 (torneo) + 150 (Lance di Re Thorek, flusso separato
            condizionato da hook politici) = max 450**. Scenari D/E di
            ARMATE-SYNC §3 ricalcolati (D: 2.650→2.230 difensori,
            2.3:1→2.7:1; E: 4.250→3.980, 1.36:1→1.46:1). Scenari Medio/
            Ottimale/Leggendario del quick-view di state.md §2.4
            aggiornati per delta coerente (nessun altro fattore toccato).
            A7 (D11 v2 + D12): Tyrgarun "Very Old Blue Dragon CR 20,
            cavalcatura di Azarr Kul" → **Old Blue Dragon CR 18, NON
            cavalcatura — terrore dei cieli** (hazard Fase 1, minaccia
            a orologeria Fase 2-3, inchiodato a terra dal Mythal in
            Fase 4). Corretto in INDICE, ARMATE-SYNC, STRUTTURA §4-7,
            PNG/Azarr_Kul/Azarr_Kul.md, campaign-story-arcs.md (+ mirror
            .github/copilot), campaign-history.md, README.md. D12:
            debito Tordek in state.md §5 riformulato "entro il Day 29,
            vigilia delle preliminari" (era "5 giorni", ambiguo).
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, completamento A8 opzione (a):
            no canon change (consolidamento di contenuti esistenti).
            Creati i 3 file "fonte autoritativa" che il piano preferiva
            (prima solo ripuntati come opzione b): DAUTH-DM-MASTER-
            REFERENCE (HUB del Torneo, tono Palio), DAUTH-CONSEGUENZE-
            ECHI-LUNGO-PERIODO (echi ×scelte), DAUTH-SUBQUEST-Thorik
            (150 lance, D10). Un secondo scan link ha trovato altri
            riferimenti orfani a sotto-quest mai scritte (SUBQUEST-
            Artemis/Hella, DAY3-CITY-SIEGE): ripuntati ai file esistenti
            che portano il materiale (HUB §5 con flag [INFERRED — Lotto
            B], SUBQUEST-Thorik §4 per lo schieramento lance), senza
            inventare sotto-quest nuove. Risultato: **zero link rotti
            operativi** (restano solo i riferimenti del piano a
            deliverable futuri B4/B7/C7). INDICE aggiornato con i 3 file.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto B, task B1 (Rhest) completo: no
            canon change (contenuto di modulo, non stato del mondo). I 5
            file FASE di Rhest (FASE1 Blackfens, FASE2 Razorfiend, FASE3
            intrusione, FASE4 boss, CONSEGUENZE) portati da scheletro a
            standard "pacchetto Palio". Le conseguenze citano e rispettano
            i numeri canonici già in §2.3 (Regiarix sconfitto = −1 drago,
            −2 Razorfiend) e §2.4 (D9: 100 ranger + 20 gufi); gli statblock
            restano nei file ENCOUNTER esistenti. Nessun potere d'artefatto
            "riusato" (rispettata §6, poteri attuali).
2026-07-02  PIANO-REVISIONE-ARC09 Lotto A, chiusura orfani sotto-quest:
            no canon change di stato-mondo (contenuto di modulo). I 3
            riferimenti orfani rimasti (prima solo ripuntati) sono ora
            **scritti** come file autonomi a standard Palio, sciogliendo i
            flag [INFERRED — da scrivere in Lotto B] dell'HUB §5:
            - DAUTH-SUBQUEST-Artemis (Beriah / culto della Maschera al
              Mercato di Dauth): sorgente giocata dei bonus già canonici
              in HOOKS-Artemis §3.4 (donna cieca → +2d6 Fase 3 Torre;
              maschera autorizzata da Mask → rottura senza eco). PNG di
              servizio (Vashet) e bonus minori marcati [INFERRED].
            - DAUTH-SUBQUEST-Hella (boschetto morente / Spora-Madre di
              Sonjak fuori Dauth): payoff = pattern Mother of Fungi
              (HOOKS-Hella §2.5.2, HOOKS-Ghostlord-Refugees §5.2); scelta
              purifica/brucia; agganci a cisterne di Dauth e Rethmar Fase 0.
            - DAUTH-DAY3-CITY-SIEGE (promuove a modulo il vecchio orfano
              DAY3-CITY-SIEGE, prima assorbito in SUBQUEST-Thorik §4):
              assedio Vanguard di Dauth in stile carte-crisi (D13),
              prototipo giocabile dell'EVENT-DECK di Rethmar (C7); riusa
              statblock da Armate-UNITA-NUOVE; Karruk/draghi restano
              riservati a Rethmar. HUB §5, SUBQUEST-Thorik §4, INDICE
              aggiornati; zero link rotti operativi residui per gli orfani.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto C, sessione 18 (C1+C2): contenuto di
            modulo (sotto-sistemi al tavolo), non stato del mondo. C1: STRUTTURA
            §9 "Cornice leggera d'assedio" (VP nascosti = "il Fronte" + check di
            Morale per ondata; 4 ruoli di comando PG; d12 eventi di battaglia;
            set-piece Tyrgarun D11 v2 a scalini). C2: contatore Morale Cittadino
            0-10 in PNG/Consiglio_Rethmar. Fix di coerenza residuo A7 (NON nuovo
            canone: D11 v2 già deciso, §2.2 già allineato): statblock Tyrgarun
            rinominato tyrgarun-black-adult-cr13.md → tyrgarun-blue-old-cr18.md e
            riscritto a blue Old CR 18 (era rimasto "black adult CR 13", unica
            scheda ancora fuori allineamento); aggiornati monster_catalog.yaml,
            Armate-COMPOSIZIONE-DETTAGLIATA §5, Armate-UNITA-NUOVE/README.
2026-07-02  PIANO-REVISIONE-ARC09 Lotto C, sessione 19 (C3+C4): contenuto di
            modulo, non stato del mondo. C3: sidebar "SE FALLISCONO" uniforme in
            P1C, P2A-PARTE4, P2B-PARTE3, RHEST-FASE4, Ghostlord-TESTO + nota unica
            §8.5 "Risorse di resurrezione nel Vale" in DM-QUICKSTART-ARC09
            (protocollo morte PG: fonti raise Rethmar/Ilmater/Circolo, "in 3.5 in
            battaglia non si resuscita", ogni raise = debito; Cuore di Moradin
            ribadito speso, §6). C4: MYTHAL-FOCUS §8 varianti per stato dei 4
            PG-focus coerenti con §6 (nessun potere teorico/speso).
2026-07-02  PIANO-REVISIONE-ARC09 Lotto C, sessione 20 (C5+C6): contenuto di
            modulo, non stato del mondo. C5(1): FASE2-RITUALISTI-TESTO §8 —
            altare campale mappato (3 anelli, 3 foci con pf/CD espliciti,
            Artefatto Maligno come 4° focus, scelta esplicita rompere-rituale vs
            tenere-mura con trade-off Fronte). C5(2): ESITI §11 epilogo giocato
            (4 scene con scelta per PG + decisione collettiva sul Fane nel Shaar,
            hook ARC-10). C6: ESITI §12 tabella ricompense di dominio esito×PG
            (Custode di Rethmar / Scuola Monastica / Cerchio Sacro / Ambasciatore
            Arcano, 1 beneficio meccanico ciascuno). Nessun potere d'artefatto
            speso "riusato" (§6 rispettata).
2026-07-02  PIANO-REVISIONE-ARC09 Lotto C, sessioni 21-22 (C7) — CHIUSURA DEL
            LOTTO C, tutti i task C1-C7 completati. Contenuto di modulo, non stato
            del mondo. Creato Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-EVENT-DECK
            .md: 14 carte-crisi giocabili (Day 40-42, Fasi 0-4), la battaglia a
            scene scelte dai PG (D13). Regola tre sorgenti S1:6/S2:6/S3:2 con
            tabella carta→sorgente→file riusato (zero doppioni; nessuno statblock
            inventato — puntatori a Armate-UNITA-NUOVE). Motore nascosto in
            STRUTTURA §9 (C1) + Morale Cittadino Consiglio_Rethmar (C2). STRUTTURA
            §2/§4, FASE1/FASE2-TESTO e INDICE aggiornati per puntare al deck
            (ondate = sfondo). Con il Lotto C l'arco passa da "coerente/completo"
            (A+B) a "memorabile" (piano §5).
2026-07-02  PIANO-REVISIONE-ARC07 Sessione 1 (A7+A9): igiene file e ordine di
            gioco. A7: rimosso temp_sinergie.txt; stub Atlante-Visivo-Mappe.md;
            ripulite coda AI (RicalibrazioneScontriPianoDelFuoco) e 17 watermark
            "OnlineMarkdown.com" (LaCorona_di_Adamantio-DM); git mv filename rotti
            (spazio interno file viaggio Hella; casing Portaleforgia-P6 ->
            PortaleForgia-P6). A9: dichiarato ordine D2 (Terra->resurrezione->
            viaggio) in testa a tutte le versioni P3B/P4/P5. Editoriale.
2026-07-02  PIANO-REVISIONE-ARC07 Sessione 2 (A1+A2): CANONE. A1: il nome
            dell'antenato di Fauci di Palude entra nel canone come **SKULLCRUSHER
            il Nero**; rimossi "Skulldark" (doppio-drago spurio in P5-DEFINITIVO-
            PARTE1) e "Infernotooth Giovane" (P1/P2). L'ARC-08 eredita il nome nel
            ponte "la Forgia ricorda" (B4). A2: profondità temporale uniformata a
            **1.000 anni prima (≈372 DR)**; corretti "2.372 anni", "500 anni fa",
            "bis-bisnonno". Genealogia unica: Skullcrusher = capostipite della
            stirpe, Fauci = discendente diretto. Label "Anno -1000" ridefinita una
            volta nei file P5 come conteggio nanico relativo.
2026-07-02  PIANO-REVISIONE-ARC07 Sessioni 3-8 (A6,B2,B3,B4,A3,A4,A5,A11):
            consolidamento e contenuti. A6: matrice versioni + master eletti.
            A11: compagno di Hella = Durik (maschio) ovunque (anche
            campaign-party.md). B2: master P3B eletto (COMPLETO) coi doni pieni
            del viaggio giocato, Thorik -2 CON, Cuore di Moradin speso, Cintura
            (D17). B3: creato P5-FASTPLAY (formato veloce D1). B4: tabella
            carry-over "la Forgia ricorda le ferite" (esito duello Skullcrusher
            -> effetto su Fauci GS 15 ARC-08); statblock ARC-08 di Fauci rimanda
            alla tabella. A3: deprecata la sezione "1372" di P6 (superata
            dall'ARC-08). A4: sequenza gemme D5/D16 (portale = Topazio+Smeraldo,
            Rubino alla vittoria antica). A5: livello arco = **13°** in §0
            (era 12, scritto in avanti); Terros ricalibrato su 3 PG/APL 12/no
            Therysol (D15). Valori meccanici nuovi tutti [INFERRED] in attesa DM.
2026-07-02  PIANO-REVISIONE-ARC07 Sessioni 9-17 — LOTTI A/B/C COMPLETATI.
            A8: DC->CD ovunque. A10: Cintura della Devastazione (scheda + §6);
            fonte unica artefatti D9 (Corona/Ring). B1: log retroattivi
            (attende intervista DM). B5: ERRATA-ARC07-35-Verification.md. B6+B8:
            ARC07-00-INDICE.md (quickstart + matrice + cronologia March Clock
            [INFERRED]). B7: ARC07-TESORO-WBL-AUDIT.md (delta si colma ad
            ARC-08). B9: raid di Sonjak in scheda + schede post-mortem
            Belkram/Urialle. C1: ARC07-ATLANTE-ASSET.md. C2: ARC07-HANDOUTS.md.
            C3: ARC07-CONSEGUENZE-ECHI.md. Unico residuo aperto: l'intervista
            DM per B1 (date/XP/loot reali) e i valori [INFERRED] da validare.
2026-07-03  PIANO-REVISIONE-ARC07 — PASSAGGIO DI VALIDAZIONE DM. Sciolti i
            principali [INFERRED]: (1) **Compagno di Hella** — il "rinoceronte"
            è **Hella che usa la Wild Shape del Druido** per diventare un
            **rinoceronte VIVO** (non di pietra/animato, non un compagno; il
            "di pietra" era confusione con Durik); l'animal companion è **DURIK**
            (cane maschio riforgiato, evocato dal 3° seme della Collana).
            Propagato in state.md §1, campaign-party.md (+mirror), master P3B,
            log retroattivi. (2) **Carry-over B4** — valori
            **approvati** (canone; statblock Fauci ARC-08 e A12 aggiornati).
            (3) **P4** — doppio master: cornice narrativa (COMPLETO) +
            **combattimento potenziato VOLUTO** (RICALIBRATO/Terros, D8:
            artefatti unici → scontri duri, non da 2 round); unico nodo lasciato
            al DM = Aura di Pietrificazione save-or-die. (4) **Cronologia B6** e
            **custode dell'uovo (C3)** approvati.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, task A0 (REGOLA ZERO — priorità
            assoluta, eseguito per primo): il cruscotto §0 e l'intestazione
            segnavano l'arco come già giocato ("00-08 ✅ completato",
            "Sessions completed: post-Hammerfist", tutte le righe 09
            "in arrivo/pianificato"), mentre il tavolo reale è fermo
            all'Arco 07 (Piano della Terra, P4, IN CORSO — vedi piano
            ARC-07 tabella G0-G6): restano da giocare la resurrezione di
            Hella (P3B), il viaggio ai 1.000 anni fa (P5) e il raccordo
            col Rubino (D16) PRIMA della Battaglia di Hammerfist. Nessun
            cambio di canone di design: solo correzione del cruscotto.
            Modifiche:
            - §0: riga 07 → 🟡 in corso (Piano della Terra in corso,
              livello reale 13 già raggiunto per ARC-07 D8); nuova riga
              propria "07 P3B Resurrezione di Hella + P5 Viaggio 1.000
              anni" ⬜ da giocare (ARC-07 D2); riga 08 → ⬜ pianificato
              — canone preparato, NON giocato, March Clock Day 19
              etichettato "target sync" invece che fatto compiuto; tutte
              le righe 09 → ⬜ preparato in anticipo (erano un mix di
              🟡/⬜ senza criterio).
            - Intestazione: "Party APL" chiarito come da ARC-07 D8 (già
              13 durante il Piano della Terra); "Sessions completed"
              riscritta con il giocato reale (Forgia, Piano del Fuoco/
              Topazio, viaggio spirituale di Hella+Durik, Piano della
              Terra in corso) e nota esplicita che tutto l'Arco 08 e
              l'Arco 09 in questo file sono canone preparato.
            - `campaign/sessions/2026-05-03_session-3.md` (racconta una
              sessione Day 19-20 post-Hammerfist mai giocata): aggiunto
              banner "⚠️ SCRITTO IN ANTICIPO — sessione non giocata" in
              testa, senza toccare il contenuto (resta bozza di design
              valida per quando si giocherà davvero).
            - `skills/rumblingstone-campaign/references/campaign-
              coherence.md` §"Locked events": annotate le due righe
              dell'Arco 08 (morti di Hammerfist, fuga di Fauci di
              Palude) come canone PREPARATO — si bloccano solo quando
              l'arco verrà effettivamente giocato, non prima.
            Materiale narrativo/meccanico degli archi 08-09 NON toccato:
            resta preparazione valida (piano ARC-08 A0, criterio di
            accettazione).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 2 (A7+A6): igiene
            file, nessun cambio di canone. A7: rimosse le code
            conversazionali AI in testa a 5 file 00_ dell'arco
            (Schede_dei_Personaggi, SCHEDE_DI_BATTAGLIA_E_REGISTRO_
            PERDITE, ATLANTE VISIVO ×2, battle_stats_maps-final) e da
            un blocco di riepilogo AI in coda a
            Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md; sostituite con
            header standard (scopo/stato/data revisione). A6: `01_`
            riscritto da stub generico in inglese (inventava "Castle
            Red"/"River Styx"/"Ruins of Eldor") a scheda logistica
            canonica dell'avanguardia di Fauci di Palude (900 unità,
            E8): punto di distacco dall'orda al Fane di Tiamat Day 1
            `[INFERRED]`, composizione a 4 linee + aereo + fianchi
            (riuso Guida DM), opportunità di interferenza per il
            gruppo di ricognizione del flashback D6 (Mappe/Hammerfist-
            Lotto-1-Ricognizione.md), ancoraggio Day 19 (E3, rimando a
            B6 per la cronologia completa). `03_` deprecato con banner
            (D12), contenuto non toccato. Buco di numerazione `02_`
            lasciato aperto per lo schema di rinomina A9.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 3 (A1+A2): esiti
            Fauci di Palude e contabilità perdite riscritti come rami
            condizionali, non fatti compiuti. A1 (D10): "Fauci morto"/
            "Fauci escaped" trattati come fatto in 7 tracker riscritti
            in forma condizionale a rami (default: fugge sotto 50 PF,
            assente da Rethmar salvo ritorno narrativo non garantito;
            alternativa: ucciso dai PG → −1 drago) —
            `00_Red Hand Of Doom/Armate-SINCRONIZZAZIONE-CAMPAGNA.md`
            §4b, `Armate-COMPOSIZIONE-DETTAGLIATA.md`,
            `Armate-CALCOLI-ESERCITI-DINAMICI.md`, questo file §2.2/§2.3,
            `campaign-coherence.md` (5 draghi nominati),
            `campaign-story-arcs.md` (+ mirror .github/copilot),
            `DM-QUICKSTART-ARC09.md`, `Arco-Post-Hammerfist-P3-
            BATTAGLIA-FINALE-ARMATE-SYNC.md`. Statblock di Fauci
            (Hammerfist Schede §1) annotato con lo stesso ramo +
            rimando esplicito al carry-over ARC-07 B4 (A12, non ancora
            consegnato — nessun valore anticipato). Non toccato: la
            "battaglia antica" di ARC-07 P5/P6 (Fauci GS 12, ancestor
            duel) — cross-arc residuo di competenza del piano ARC-07
            A2/A3, non di questo lotto.
            A2 (D11): due aritmetiche divergenti (questo file diceva
            "−500 → ~9.400", il ledger diceva "−900 → 8.610")
            riconciliate sul numero canonico **−900** (~500 morti +
            ~400 dispersi che non si ricongiungono, già coerente con
            Mappe/Hammerfist-Lotto-1-Ricognizione r.192 "conta precisa
            900" e Atlante-Mappe r.1034/1053 "400 superstiti"). Questo
            file §2.2 corretto a **~9.000** attivi post-Day 19; stessa
            cifra propagata con breakdown esplicito (500+400) in
            Armate-SINCRONIZZAZIONE-CAMPAGNA §3 r.81,
            Armate-CALCOLI-ESERCITI-DINAMICI §3, e ARMATE-SYNC ARC-09
            riga Day 19. Non toccata la matrice scenari Day 42 "vista
            rapida legacy" (§2.4 r.197 + mirror DM-QUICKSTART-ARC09 +
            Armate-CALCOLI): resta un diverso checkpoint (Day 42, non
            Day 19), già segnalata nel file come legacy in attesa del
            ricalcolo autoritativo di ARMATE-SYNC/B1 — fuori scope per
            questo lotto meccanico.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 4 (A3+A5): nessun
            cambio di canone di trama, solo XP/terminologia. A3 (D9):
            la sezione "RIASSUNTO XP E RICOMPENSE" (duplicata in
            `hammerfist_encounters-...-final.md` e nella Guida DM
            Appendice C) prometteva 34.400 XP totali (8.600/PG),
            "abbastanza per portare PG da 13° a 15°" — contraddice D9
            (party arriva ED esce al 13°, Hammerfist lo consolida).
            Riscritta in entrambi i file: Sessioni 1-2 + prima metà
            Sessione 3 ("Ultima Resistenza") = **zero PX** ai Rumbling
            Stones (si giocano coi pregen, D6) con bonus da quantificare
            in B1 (non ancora scritto); solo da metà Sessione 3
            ("Rumbling Stones", passaggio di testimone) e Sessione 4 i
            PG reali maturano PX, dosati a **7.200 XP totali (1.800/PG)**
            `[INFERRED — proposta conservativa, da verificare al tavolo
            contro la XP reale bancata dal party]`, esplicitamente non
            sufficienti per il 14°. Aggiunta nota di verifica EL
            (finale dichiarato EL 20 su APL 13, oltre il precedente
            ARC-06 EL 17 — verifica completa rimandata a B5).
            A5: terminologia 5e/inglese ripulita nei file `Mappe/`:
            34 occorrenze `DC n` → `CD n`; skill inglesi (Spot, Hide,
            Climb, Balance, Strength) → nomi italiani 3.5 (Osservare,
            Nascondersi, Scalare, Equilibrio, Forza) nei check
            meccanici; 3 "advantage" colloquiali riformulati in bonus
            di circostanza espliciti. Non toccata la prosa descrittiva
            mista IT/EN pura (es. "nowhere hide" come flavor text) né
            il contenuto di `03_` (deprecato con banner, D12, contenuto
            non toccato per policy A6) — fuori scope per questo lotto
            terminologico.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 5 (A8): quattro
            generazioni di atlante + due generazioni di mappe tattiche
            consolidate, nessun cambio di canone di trama. Eletto
            `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` **master
            visivo** (17 mappe dopo la migrazione, sotto); i tre
            `Hammerfist-L{1,2,3}-REVISED-Ultra-Clear.md` restano
            **master tattici** ma solo per le 3 mappe a griglia
            ultra-precisa che coprono (1A-2, 2A, 3X/H3-1) — non
            deprecati, categoria diversa (non sovrapposti). Banner
            DEPRECATED (D12) su 6 file superati: `00_battle_stats_
            maps-final.md`, `00_ATLANTE VISIVO...md`, `00_ATLANTE
            VISIVO...-complete.md`, `Mappe/Hammerfist-Lotto-{1,2,3}-
            *.md`. Scoperta e sanata una lacuna reale: **MAPPA 3Y "Il
            Ponte Sospeso"** esisteva solo nelle generazioni (b)/(c)
            deprecate e MAI nel master — migrata nel master tra 3X e
            3Z (17ª mappa) prima di deprecare le fonti, per non perdere
            contenuto. Matrice di contenuto (mappa × file × stato)
            aggiunta in testa al master. Riferimenti attivi ripuntati:
            `ARC08-04-MARCIA-MANO-ROSSA.md` (scritto in A6,
            puntava ai Lotto-N deprecati) e la lista file Arc-08 di
            `campaign-history.md`.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 6 (A4, sui soli
            master post-A8): il master visivo dichiarava scale
            incoerenti ("1 quadrato = 3 metri" su alcune mappe, "Grid
            già ottimizzato standard D&D 1,5m" nel riepilogo finale —
            falso, mai stata una griglia uniforme). Corretto senza
            ridisegnare le griglie ASCII (rischio di disallineare
            distanze già citate nel testo — soffio, portate,
            velocità): le 6 mappe tattiche a scala 2m/3m (1A-1, 1A-2,
            2A, 3X, 3Z, 5) ora portano un flag esplicito di deviazione
            dalla convenzione repo (1,5m); le 10 viste non-griglia
            (strategiche/schematiche/cinematiche/architettoniche) ora
            dichiarano esplicitamente "NON è una griglia di
            combattimento"; MAPPA 3Y (migrata in A8) era già a 1,5m,
            nessuna modifica. Riepilogo finale del master corretto
            (16→17 mappe; rimossa l'affermazione falsa di griglia
            uniforme 1,5m). I tre master tattici `L{1,2,3}-REVISED-
            Ultra-Clear` erano già coerenti a 1,5m/quadrato, nessuna
            modifica necessaria.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 7 (A10+A11): audit
            di refusi, nessun cambio di canone di trama. A10 (D2):
            audit occorrenza-per-occorrenza di Thorin/Thorik/Thorek nel
            master `Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md` (52
            occorrenze totali). Trovati e corretti: "Thorik (PG)" nella
            scena del soffio di Sessione 2 (era ancora la fase pregen,
            D6 — non è "PG" lì, solo "Thorin"); l'epiteto spurio
            "Thorik SkullDark" (4 occorrenze — conflazione col nome
            deprecato dell'antenato drago, già corretto altrove in
            ARC-07 D6 a "Skullcrusher") rimosso, resta solo "Thorik".
            Scoperto e sanato un secondo problema mentre si leggeva la
            scena: il duello finale Thorik vs Fauci era scritto come
            uccisione certa ("Killing Blow", "Drago collassa 0 HP"),
            violando il ramo condizionale D10 (A1) — riscritto a rami
            (default: fugge sotto 50 PF; alternativo: ucciso se i PG
            lo bloccano attivamente). Nota di disambiguazione
            "Thorin=pregen, Thorik=PG, Thorek=re" aggiunta in testa ai
            2 file master (Atlante mappe + Schede dei Personaggi).
            A11 (D13): compagnia del Capitano Lunapiena dichiarata
            esplicitamente indipendente/Elsir Vale, di presidio a
            Hammerfist, NON sommata ai difensori di Rethmar — nota
            aggiunta allo statblock (Schede §2), alla sezione PNG
            della Guida DM, a state.md §2.4, e come regola di coerenza
            esplicita in ARMATE-SYNC ARC-09 §7 (prima l'esclusione era
            solo implicita per omissione). Verificato che la Cerimonia
            delle 100 Asce già usa solo Lythiel, nessuna fusione dei
            due comandi elfici.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto A, sessione 8 (A9, parziale) —
            CHIUSURA DEL LOTTO A (A1-A11 completati; A12 resta
            bloccato su ARC-07 B4, non ancora consegnato). Nessun
            cambio di canone di trama, solo `git mv` + fix link.
            Rinominati con `git mv` (schema `ARC08-NN-SLUG.md`) gli 8
            file che avevano il buco di numerazione 00_/01_/03_
            (mancava 02_) e nomi con spazi/maiuscole miste: i 4 file
            00_ ancora canonici → `ARC08-01-GUIDA-DM.md`,
            `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`,
            `ARC08-03-REGISTRO-PERDITE.md`; `01_MANO_ROSSA...` (A6) →
            `ARC08-04-MARCIA-MANO-ROSSA.md`; i 3 file 00_ deprecati
            (A8) + il 03_ deprecato (A6) → `ARC08-9{0,1,2,3}-
            DEPRECATO-*.md` (numerazione alta = fuori dal percorso di
            lettura attivo, banner invariati). Aggiornati TUTTI i
            riferimenti repo-wide trovati (12 file in 07_/08_/09_/PNG/
            campaign/, incluse forme abbreviate con "…" non catturate
            dal primo giro di sostituzione automatica). **Scope
            ridotto rispetto al piano**: NON rinominati
            `hammerfist_encounters-...-final.md`, `Cerimonia-delle-
            100-Asce.md`, `mass_combat_guide_Dm.md`,
            `combat_prompts_guide.md`, né i file di `Mappe/` — questi
            non hanno il problema di numerazione (nessun prefisso
            00_/01_/03_), e includerli avrebbe moltiplicato il rischio
            di rompere riferimenti repo-wide per un beneficio
            marginale; lasciati per una passata dedicata (coordinabile
            con B7/INDICE). `ARC08-00-INDICE.md` (esempio del piano)
            **riservato** per il deliverable di B7, non creato ora
            (nessun file riempitivo). Rinomina immagini e cartella
            `immage_campaign/` NON eseguita, come da istruzione esplicita
            del piano (dopo la tabella immagine→mappa, C3).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto B, sessione 9 (B1): contenuto di
            modulo nuovo, non stato del mondo. Creato
            `08_.../ARC08-10-ESITI-E-CONTINGENZE.md`: (1) i tre scenari
            d'esito — vittoria piena (default E1-E8, numeri D11),
            vittoria costosa (<50 superstiti / Re Thorek morto
            [INFERRED]), caduta di Hammerfist (evacuazione Passaggi
            Antichi, orda +600 a Rethmar [INFERRED]) — ciascuno con
            delta numerici agganciati ai tracker; (2) i rami
            condizionali di Fauci (D10) col gancio al carry-over ARC-07
            B4 (A12, non ancora consegnato — nessun valore anticipato);
            (3) la **tabella di conversione D9** flashback pregen→bonus
            (Sessioni 1/2/3a × obiettivi pieno/parziale/fallito →
            intel, posizioni, PNG vivi, −CR, morale — MAI PX), con
            regola di somma e mappatura ai tre esiti. Sezione
            "Conseguenze a lungo periodo" lasciata come rimando a C2
            (Lotto C, non ancora scritto). Nessun esito dichiarato come
            fatto: tutto preparazione a rami (coerente con A0).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto B, sessione 10 (B6+B2):
            contenuto di modulo nuovo, non stato del mondo. B6: creato
            `ARC08-12-CRONOLOGIA-MARCH-CLOCK.md`, la cronologia
            condivisa Day X→19 (flashback pregen ~settimane prima →
            assedio Day 16-18 → riemersione RS Day 18-19 = Giorno 3
            d'assedio → vittoria Day 19 → Cerimonia Day 21). Tre
            riconciliazioni tra file che divergevano: (a) Cerimonia =
            **Day 21** (dal file canonico Cerimonia §7), non Day 19 come
            proponeva genericamente il piano B6; (b) "Giorno 3
            dell'assedio" (conteggio locale) ≠ March Clock Day 3;
            (c) finestra ricognizione pregen [INFERRED] (D6 "qualche
            settimana" vs proposta B6 "Day 12-16"). B2: creato
            `ARC08-11-PONTE-ARRIVO.md` (snello), la cucitura D16 finora
            mancante — puntatore al master P3B ARC-07 (NON riscritto;
            stato in uscita dalla fonte stabile state.md §1/§6 + D8),
            correzione esplicita su P5-DEF §4.3 (che faceva atterrare i
            PG nella Sala della Forgia; D16, più recente, li fa
            riemergere al Cuore della Montagna Giorno 3 — D16 vince), e
            regia del passaggio pregen→PG (D6) con uno spotlight per
            ciascun PG (Durik incluso, terzo seme della Collana).
            Bonus del flashback rimandati alla tabella B1 §5 (mai PX,
            D9). Aggiornato il rimando in ARC08-04 (marcia) alla
            cronologia B6 ora esistente. Nota: B2 marcato completo
            nonostante il flag "attende ARC-07 B2" — il ponte usa lo
            stato in uscita bloccato in state.md/D8, non la prosa del
            master P3B (che ARC-07 B2 rifinirà); il pointer narrativo
            potrà guadagnare dettaglio, la cucitura no.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto B, sessione 11 (B7): contenuto
            di modulo nuovo, non stato del mondo. Creato
            `ARC08-00-INDICE.md`: posizione nella campagna (dopo ARC-07
            D2/D16, sync Day 19), struttura a due tempi D6/D9 con
            disambiguazione nomi D2, ordine di lettura per il DM (10
            passi), cosa stampare, tabella file→ruolo→stato (canonici /
            deprecati / servizio, dalla matrice A8), elenco deliverable
            ancora da produrre (B3/B4/B5/C1-C4/A12), nota
            branch-per-group. Riempie il buco di numerazione 00_ (dopo
            A9) col deliverable previsto, senza file riempitivi.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto B, sessione 12 (B5): verifica
            meccanica 3.5, correzioni in place + nuovo file registro.
            Creato `ERRATA-ARC08-35-Verification.md`. Correzioni
            applicate in `ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md`:
            (1) Cavaliere Hobgoblin (Guerriero 8/Guardia Nera 2) —
            Punire il Bene "2/giorno … +10 danni" → **1/giorno, +2
            danni** (il bonus è il livello di Guardia Nera, non il
            livello personaggio; 2/giorno solo dal 5°); Aura di
            Disperazione RIMOSSA (si ottiene al 3° liv GN) e sostituita
            con Attacco Furtivo +1d6 (feature reale del 2°); (2) Fauci
            di Palude — "Soffio a Cono 1/giorno" flaggato **house-rule**
            (i draghi neri SRD hanno solo il soffio in linea; mantenuto
            per la scena della picchiata, alternativa SRD indicata). I
            4 pregen verificati e dichiarati stampabili (nessun
            5e-ismo, math coerente, tolleranze [INFERRED] minori). Il
            sistema di massa AU/DU/PFU/Morale verificato compatibile
            con l'action economy 3.5. Gear di Tordek già coerente con
            D17 (unica menzione in ARC-08 è nel ponte B2). Non
            modificati gli statblock estesi dei PNG maggiori nella
            Guida DM (fuori dal campione B5; li coprono B3 + eventuale
            passata dedicata).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto B, sessione 13 (B3): 13 schede
            PNG create in `PNG/` (file piatti, formato AGENTS.md
            Role/Status/Location/Motivation/CR/Key stats/Notes + campo
            "esiti possibili"), stat **puntate** alle appendici (fonte
            unica), non duplicate. Nemici: Fauci_di_Palude (rami D10),
            Generale_Grimjaw, Gorthak_il_Trifronte. Alleati:
            Re_Thorek_Hammerfist (default vive / vittoria costosa
            muore, B1 §2), Dana_Forgiapietra, Capitano_Lunapiena (D13
            indipendente), Signore_Ventolesto, Orion_Pelleorsa. Pregen
            (D14): Borin_Ferropugno, Dara_Occhiolesto, Thorin_Runaforte,
            Nala_Cantapietre. Più Khorn (D5, 150 lance, stat [INFERRED]
            — non nelle appendici). INDICE (ARC08-00) aggiornato con la
            tabella del cast. Scelta: file piatti in PNG/ (precedente
            Il_Collezionista_Rakshasa.md) invece di 13 sottocartelle,
            per non moltiplicare entry filesystem per schede snelle.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto B, sessione 14 (B4) — CHIUSURA
            DEL LOTTO B (B1-B7 completati; A12 resta bloccato su ARC-07
            B4). Creato `ARC08-13-TESORO-WBL-AUDIT.md` (gemello
            dell'audit ARC-09): il party resta al 13° (D9), quindi
            Hammerfist **consolida** il WBL del 13° (110k mo/PG), non lo
            supera. Tabella tesoro per fonte in stile Paizo (gratitudine
            di Re Thorek, armeria, bottino avanguardia, gear dei
            comandanti condizionale, tesoro di Fauci solo nel ramo
            "ucciso"; runa dei Custodi = plot item, 0 mo). Riconciliata
            la "ricompensa 50k/PG" della Guida DM come **top-up al 13°
            WBL**, non "+50k su un party già pieno" (che sforerebbe
            verso il 14°, contro D9). Handoff esplicito: ricchezza
            d'uscita ARC-08 = ingresso ARC-09 (~110k/PG), il numero già
            assunto da `09_.../TESORO-WBL-AUDIT.md` §1.2. Ricchezza
            d'ingresso ARC-08 marcata [INFERRED] (dipende da quanto
            bancato in 01-07). INDICE aggiornato (B4/B5 nella tabella
            canonica; numerazione §7 corretta).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto C, sessione 15 (C1): sistema di
            combattimento di massa consolidato in fonte unica.
            `mass_combat_guide_Dm.md` eletto **fonte normativa**. Sanato
            un conflitto reale: il master usava un motore **2d6** (PF
            1-10), mentre `ARC08-02` §4 usa **AU/DU/PFU (1d20)** — ed è
            quest'ultimo che ARC-09 ha ereditato (STRUTTURA §9) e che B5
            ha verificato 3.5-compatibile. Riconciliazione: dichiarata
            **canonica la risoluzione AU/DU/PFU (1d20)**; il 2d6 resta
            come variante rapida opzionale esplicitamente flaggata (con
            tabella di mappatura tra i due). Aggiunto in fondo al master
            il **raccordo con ARC-09** (cosa STRUTTURA §9 ha ereditato:
            unità/PFU/morale/spotlight/danni strutturali; cosa ha
            cambiato: VP nascosti "il Fronte", eventi scelti via
            EVENT-DECK, ruoli di comando, check morale per ondata — la
            massa da primo piano a Hammerfist diventa sfondo a Rethmar).
            Le altre 3 copie ora puntano al master: `ARC08-02` §4
            (quick-reference), Guida DM Appendice A, `ARC08-03`
            (registro di tracciamento). INDICE aggiornato.
2026-07-02  PIANO-REVISIONE-ARC08 Lotto C, sessione 16 (C2): aggiunta
            la sezione "Conseguenze a lungo periodo" a
            `ARC08-10-ESITI-E-CONTINGENZE.md` §6 (sostituito il rimando
            placeholder). Tabella echi in formato ARC-09 (evento → eco
            → quando riemerge → file), con varianti per ramo d'esito:
            Fauci fugge (nemesi) / uovo di Fauci (ARC-07 C3, eco
            gemella) / Fauci ucciso / runa dei Custodi / 150 lance /
            pregen D14 / raid drow → Fase 0 Rethmar / Lunapiena
            presidio. **Runa dei Custodi Eterni quantificata**
            [INFERRED]: +2 di circostanza Diplomazia coi nani del Vale +
            ospitalità/armeria a Hammerfist + riconoscimento PNG; NON
            magica, 0 mo WBL. Proposta (solo hook+puntatore) della
            carta S2 "Il Ritorno di Fauci di Palude" per l'EVENT-DECK
            ARC-09 (ramo default D10). Nessun eco contraddice gli HOOKS
            ARC-09; EVENT-DECK ARC-09 non modificato (solo proposto).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto C, sessione 17 (C3): atlante
            immagini. Cartella `08_.../immage_campaign/` → **`immagini/`**
            (git mv, typo corretto); aggiornate le 2 referenze vive
            (INDICE, campaign-history.md ×2). Le voci di changelog
            precedenti che citano "immage_campaign" restano intatte
            (append-only, storiche). Creato
            `ARC08-14-ATLANTE-IMMAGINI.md`: classificazione delle ~42
            webp (immagine → mappa/scena → sessione → prompt d'origine
            → quando mostrarla → nome suggerito). 28/42 pinnate a un
            master preciso a vista (visionate ~19 + 6 nomi descrittivi +
            4 varianti bis); 14 "generazioni October 2025" classificate
            al gruppo (mappe/scene dell'arco, campione confermato
            fortezza 2A / torrione 1A-2 / drago / finale) → 100% a
            gruppo, ~67% pin preciso. Aggiunti i puntatori alle
            immagini reali su 9 voci del master visivo
            (`Mappe/Atlante-Hammerfist-Mappe-COMPLETE.md`: 1A-1, 1A-2,
            1A-3, 2A, drago, 3X, 3Y, 5, finale). Rinomina dei singoli
            file allo schema `hammerfist-sNN-*` **differita** (nessun
            .md li referenzia per nome → passata dedicata a basso
            rischio, dopo il pin a vista delle 14 generazioni).
2026-07-02  PIANO-REVISIONE-ARC08 Lotto C, sessione 18 (C4) — CHIUSURA
            DEL LOTTO C e dell'intero piano ARC-08 (A0-C4 completati;
            resta solo A12, bloccato su ARC-07 B4). Creato
            `ARC08-15-HANDOUTS-GIOCATORE.md` (gemello dell'ARC-09
            HANDOUTS): (1) i 4 pregen "Eroi di Hammerfist" resi
            stampabili 1 pagina l'uno, giocabili senza aprire i file
            00_/ARC08-01/02 (stat verificate B5); (2) la runa dei
            Custodi Eterni (descrizione + effetto C2 §6.2 + prompt
            immagine); (3) il canto della cantillazione ("ricordato…"
            + Giuramento delle 90); (4) la mappa giocatore della
            fortezza (versione lato giocatore della MAPPA 2A, privata
            di tunnel segreto/imboscate/meccanismi — nessuna info lato
            DM). Ogni handout con "quando darlo". INDICE aggiornato
            (ARC08-14/15 nella tabella canonica; §6 riscritta a "Lotti
            A/B/C completati", resta solo A12 + coda C3 non bloccante).
2026-07-03  PIANO-REVISIONE-ARC08 A12 (eredità Skullcrusher→Fauci) —
            **COMPLETO: piano ARC-08 interamente chiuso (A0-A12,
            B1-B7, C1-C4)**. Il deliverable ARC-07 B4
            (`07_.../PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`) è
            stato consegnato e validato dal DM (merge PR #18) → A12
            sbloccato. Integrato in ARC-08 come **puntatore, zero valori
            duplicati** (la fonte unica dei numeri resta la tabella
            ARC-07): (1) riconciliata la nota "non ancora consegnata"
            nello statblock di Fauci (`ARC08-02` §1) col banner di
            carry-over già aggiunto da ARC-07; (2) nuova §4.1 in
            `ARC08-10-ESITI-E-CONTINGENZE.md` = mappa qualitativa
            esito-P5→effetto-a-Hammerfist (ucciso/ferito/fuggito +
            ferite ancestrali + gancio Aegis Fang), senza ricopiare i
            valori; (3) nota read-aloud al primo avvistamento di Fauci
            (`ARC08-01` Sessione 2); (4) gancio Aegis Fang al duello
            finale (master mappe MAPPA 4); (5) scheda
            `PNG/Fauci_di_Palude.md` aggiornata. Corretti anche 2
            riferimenti obsoleti in ARC08-10 (C2 "non ancora scritto"
            e "carry-over se disponibile") e l'INDICE §6 (da "A12
            bloccato" a "piano completo"). Follow-up post-merge PR #17:
            branch ripartito da origin/main (sarà un nuovo PR).
2026-07-04  **Chiusura conferme DM del piano trasversale (7 decisioni)**.
            (1) Corona/Stone's Awareness: valgono ENTRAMBE le liste →
            porte segrete + trappole + comprendere linguaggi a volontà
            (master DM, scheda giocatore, campaign-artifacts allineati).
            (2) Corona/Topazio: attivazione = 1 ORA di concentrazione
            (vale l'HTML `02`; «10 minuti» superato). (3) Bracieri:
            Benedizione della Forgia Eterna PERMANENTE per la campagna
            intera (4 cariche/giorno, carica gratis su 18-20,
            Frantumare). (4) Campo Drow 2: canonizzate le dimensioni
            disegnate 65×53 (≈98×80 m); titolo/testo/SVG allineati.
            (5) T6c: §6 di questo file riscritto a DOPPIA COLONNA
            («Today at the table ARC-07 P4» / «Prepared ARC-09 entry»)
            — l'ambiguità dei due tempi [T4-a] è chiusa; nessuna riga
            di storia riscritta, solo etichettatura dei tempi.
            (6) Temporanei Word cartella Aegis (~$gis Fang.docx,
            ~WRL0191.tmp): RIMOSSI (git rm). (7) Nuova libreria
            mostri/villain/PNG: locazione standard = `Bestiario/` a
            repo root (vedi PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN
            e CENSIMENTO-MOSTRI-PNG-VILLAIN).
2026-07-04  Palio di Channathgate (P2D) INDICIZZATO come side-arc canonico
            opzionale di ARC-09 (era scritto ma non referenziato dai file-hub,
            quindi "mai menzionato" nella navigazione). Nessun cambio di stato
            del mondo: solo cross-link. Wired in: INDICE-GENERALE (nuova PARTE
            2D), DM-QUICKSTART-ARC09 §5 (riga P2D), HOOKS-INTEGRATION-MASTER
            §1.1 timeline + §9, Consiglio_Rethmar (File correlati), Torneo
            DAUTH-DM-MASTER-REFERENCE (attività parallela). Canone confermato
            dal DM (2026-07-04): il **Drappellone = Matrice del Mythal** della
            Fase 4 (cross-link aggiunto in FASE4-CIRCOLO-MYTHAL-STATUE-TESTO);
            l'esito del Palio muove il voto del Consiglio (default RESA→DIFESA)
            e sblocca +150 truppe. Collocazione: Day 27-36, parallela a
            P2A/P2B/P2C, deadline rinforzi Day 37-38 → Rethmar Day 42.
2026-07-11  Rinominato il PNG **Borin Tozzefort → Durgan Tozzefort**
            (comandante dei 300 mercenari nani di Dauth, `[INFERRED]`):
            il nome «Borin» confliggeva con **Borin Ferropugno**, l'eroe
            pregen usato nella Battaglia di Hammerfist (rischio di fusione
            dei due PNG). Aggiornati i riferimenti vivi (ESITI-CONSEGUENZE
            §7, STATBLOCCHI-EPICI §7, PIANO-REVISIONE-ARC09, censimento,
            piano libreria). La riga changelog del 2026-07-02 conserva il
            nome storico (append-only, non riscritta).
2026-07-12  CALENDARIO (decisione DM): l'inizio campagna RHoD è in PIENA
            ESTATE nella Valle di Channath → In-world date corretta da
            "Mirtul" a "Flamerule 1372" (conferma la nota "Flamerule —
            Campaign Start" di house-rules.md). Ancora di conversione:
            Giorno di Marcia 1 = 1 Flamerule 1372 (Day 19 = 19 Flamerule;
            Day 42/Rethmar = 11 Eleasis). Applicata in scripts/session_recap.py
            (MARCH_DAY1_HARPTOS); le date nei recap/dossier ora sono Harptos.
2026-07-12  **Khorn e Durgan Tozzefort canonizzati** (conferma DM). Rimossi
            i flag `[INFERRED — needs DM confirmation]`: Khorn (ufficiale
            nanico di Hammerfist, Guerriero 8 CR 8 — `Bestiario/png/Khorn/`)
            e Durgan Tozzefort (comandante 300 mercenari nani di Dauth,
            Guerriero 12 CR 11 — STATBLOCCHI-EPICI §7 + ESITI-CONSEGUENZE
            + `Bestiario/png/dauth-commander-mercenari-nani-cr11.md`) sono
            ora ACCEPTED DM-canon 2026-07-12. Statblock, dossier e censimento
            aggiornati.
2026-07-20  Nuova skill `rumblingstone-narrative-style` (motore di stile a
            8 pilastri: Salvatore, LotR, Casa di Davide, Andor, GoT, Mercer,
            BG3 echi, BG1/2 quest design; protagonismo PG nel bene e nel
            male). Aggiunte sottosezioni §7.E Echo Ledger e §7.R Reputation
            (Fama/Infamia + Anointing Threads) — vuote, da popolare dalla
            prossima sessione. Nessun contenuto di campagna modificato.
2026-07-20c **R4 — Wyrmlord + Blackspawn** (DM). (1) **Hravek Kharn fuso in
            Wyrmlord Karruk**: i Wyrmlord dell'AP non sono reintegrati 1:1;
            il ruolo di Kharn (comandante bruto dell'avanzata) è **Karruk**
            (già gigante-barbaro comandante da campo). Nessuna scheda Hravek
            separata; stats AP solo come seme di variante. (2) **Ulwai
            Stormcaller NON reintegrata 1:1**: nicchia già coperta da Mira
            Serani «l'Aranea» + fronte drow; stats come seme per un caster
            speciale se serve. (3) **Blackspawn rilivellati**: nuovo tier
            **élite CR 13 «Razorfiend Blackspawn Alfa»** (Huge dragon 16 DV,
            `Bestiario/mostri/razorfiend-blackspawn-alfa-cr13.md`, boost da
            razorfiend CR 9 via advancement) — gli **8 spawn assegnati ai
            Wyrmlord** (§2.2) usano questo tier; i razorfiend CR 8-9 restano
            truppa d'ondata. Motivazione DM: orda ~10.000 (>> AP) → servono
            elementi speciali all'altezza dell'APL 13. Coerente con la
            nota del designer AP (dm-guide: "Kharn most in need of re-stat;
            re-stat the razorfiends").
2026-07-20b **Aranea ricalibrata PG 8-9 + rename Nania Seriv** (follow-up
            R7). Lo statblock di Mira Serani è stato **ricalibrato a CR 8**
            (Aranea Stregone 6, `Bestiario/villain/Mira_Serani/mira-serani-
            aranea-cr8.md`, rinominato da -cr11) e reso **canon per PG 8-9**
            su decisione DM: la CR 11 [INFERRED] precedente (per APL 13) era
            troppo forte per PG 8-9. Ramo di ritorno ad APL 13 (CR 11
            skirmisher / CR 13-14 boss) documentato nel dossier §5.
            **Collisione nomi RISOLTA (DM)**: la luogotenente buona di Lorana
            `Mira del Traghetto` → **`Nania Seriv del Traghetto`** (rinominata
            nei 3 file Palio P2D: INTEGRAZIONE, PROVE-AMMISSIONE, STATBLOCCHI).
            Ora «Mira» resta solo alla bambina morta e alla villain che ne ha
            rubato la faccia. (La riga 2026-07-20 qui sotto è append-only e
            conserva i valori originali CR 11 [INFERRED].)
2026-07-20  **Mira Serani «l'Aranea» reintegrata + twist CANONIZZATO** (gate
            R7 del PIANO-REINTEGRAZIONE-PNG-AP-RHOD). Villain AP (aranea spia
            della Mano Rossa, `[Private — RHoD p.44-45]`) assente dal repo,
            ricostruita da base aranea SRD (OGL) → Aranea Stregone 9, CR 11
            `[INFERRED]` (numeri da validare; identità/ruolo = canone DM).
            **Twist DM**: uccise la **figlia di Lorana** (la bambina Mira, 6
            anni, già a canone come morta nel triage del Guado) e ne rubò la
            faccia; si spaccia per lei (bimba/adolescente) tra i profughi; ha
            già incrociato i PG sulla strada per Hammerfist ed è fuggita.
            L'esito bloccato NON cambia (Mira è morta lo stesso); si aggiunge
            solo lo strato nascosto. **Lorana = hard counter** (la smaschera a
            vista). Nessun clock nuovo: la sua intel alimenta i clock
            esistenti (Sal/Sonjak/Fase 0-1). File: `Bestiario/villain/
            Mira_Serani/` (dossier + statblock) + sezione DM-segreta in
            `Bestiario/png/Lorana/…/Lorana.md`. Aggiunte §3 (villain), §4
            (Aranea + Lorana), §7 ([ARANEA]). Collisione «Mira del Traghetto»
            (Palio P2D) segnalata, non risolta (default: codename «l'Aranea»).
2026-07-20  **Profughi del Guado di Drellin + Lirien CANONIZZATI** (conferma
            DM — gate R6 del PIANO-REINTEGRAZIONE-PNG-AP-RHOD, lotti R1+R5).
            Rimossi i flag `[INFERRED — needs DM confirmation]` dai dossier:
            (1) i sei PNG civici dell'AP (Norro Wiston, Sertieren il Saggio,
            Fratello Derny, Delora Zann, Iormel, Kellin Shadowbanks —
            `Bestiario/png/Guado_di_Drellin/`) sono canone come volti
            dell'onda profughi Day 12→25 verso Rethmar; gli esiti alternativi
            restano rami aperti del DM (D13). (2) Lirien Amaranti «Il
            Giullare Spezzato» (`Bestiario/png/Lirien/`) è canone come PNG
            caotico neutrale ricorrente di Rethmar: superstite del Guado,
            ex-apprendista del «Maestro» (fornitore occasionale della rete
            d'arte di Varis/Sal), possibile futura promozione a PG su branch
            di gruppo. Aggiunte righe §1 (companion ricorrente), §3 (Norro,
            Sertieren, Lirien) e §7 ([PROFUGHI], [LIRIEN]).
2026-07-23  **ARC-07 CONSOLIDAMENTO CHIUSO** — l'Arco della Forgia Eterna è
            ora un percorso di **5 master DEFINITIVI** autosufficienti (qualità
            modulo-AP), uno per beat: `ARC07-DEF-1` (Piano della Terra/Terros),
            `-2` (Ritorno & Affreschi, hub), `-3` (Resurrezione di Hella, hub),
            `-4` (Viaggio a ≈372 DR), `-5` (Ritorno a Hammerfist/cucitura del
            Rubino, hub). `ARC07-00-INDICE.md` rigenerato: i DEF sono il
            percorso giocabile, i file-fonte marcati «assorbiti». Fili in uscita
            (Echo Ledger, DEF-5 §7): carry-over B4 (Skullcrusher→Fauci), Debito
            della Radice (§7 [DEBITO DELLA RADICE]), Seme del Ghostlord ([SEME
            DEL GHOSTLORD]), Vatore/Sal ([VATORE/SAL]), Cronaca Vivente,
            Doni-costo della resurrezione. Canone in uscita invariato (§1/§6):
            Corona 3 gemme (Rubino speso), Cuore di Moradin speso, Thorik −2 COS,
            Hella viva (Ibrido Treant/Collana/Durik), party 14° a Hammerfist.
            MIGRAZIONE `_ARCHIVIO/` ESEGUITA: 16 sorgenti assorbiti spostati in
            `07_.../\_ARCHIVIO/`, riferimenti a percorso pieno riscritti nei file
            tracciati (skill-source, archi 08/09, PG/Artefatti, lore) + interni
            all'arco; mirror skill/`build/` gitignored (si rigenerano da
            sorgente); log append-only lasciati intatti come record storici.
            Nuovi handout: `homebrew/HANDOUT-2-hints-per-pg-prossima-sessione.hb.md`
            (hints asimmetrici per la sessione Terros). validate_modules 5/5,
            bestiario/maps/skills/plans verdi.
2026-07-23b **ARC-07 ATLANTE MAPPE DEFINITIVO** — nuovo
            `07_.../Mappe/ARC07-MAPPE-DEFINITIVO.md`: le 12 griglie ultra-clear
            di tutti i beat (T-1…T-6, S-1/S-2, R-1, M7-A/B, CM-1) a piena scheda
            tattica (posizioni PG/PNG/villain, terreno & altitudini, tattiche di
            villain/mostri, evoluzione), standard = Atlante Hammerfist (arco 08)
            + L1/L2 UltraClear + battle map RHoD. ASCII resta la fonte canonica
            (resa SVG = task futuro PIANO-RENDER-MAPPE-FEDELTÀ). Referenziato da
            INDICE, dai 5 master DEF (sezione MAPPE) e dai booklet. Corretti 2
            errori in CM-1 (header 24→15 m / 16→10 righe; typo 🟟→🟡).
2026-07-23c **S-2 e CM-1 riallineate alle geometrie CANONICHE** (decisione DM).
            S-2 Stanza della Corona: griglia rifatta sulla mappa giocata ARC-06
            (`06_.../CoronaDiAdamantio/Tactics_and_maps.md`) — posizionamenti
            INVARIATI (trono E-F12, muro/Cronaca D-F13, portale drow sigillato
            E13, colonne/statue/alcove/macerie, Dipinti Invisibili J11-12,
            ingresso sud D-F02); eliminato il dais inventato; stato ARC-07
            (purificazione) come overlay. CM-1 Cuore della Montagna: griglia
            rifatta sulla MAPPA 5 dell'Atlante-08 (caverna 100×80×40 m, scala
            3 m/quadretto con nota A4, altare +3 m Ø6 m, 10 statue a 20 m, 90
            nani a 30 m, porta mithral 6 m nord, piattaforme ±1,5 m, stalattiti
            4d6/Rifl 18) + ondate 1-4 del 3B + doppio timing dell'Apparizione
            (Round 8 nel 3B completo / porte-che-cedono nel lato ARC-07).
            Aggiornati atlante + DEF-2 + DEF-5 (griglie identiche).
2026-08-05  Approvata l'ala di incantatori e comprimari (PR #93-#97). 13 file
            passano da [INFERRED] a [ACCEPTED - DM-canon]: Ghaurush
            «Cenerevento» (GS 16/17/18), Zin'thara Vel'Ryn (GS 12), Ushgar
            «Occhio Reso» (GS 13), + 7 schede di comprimari. Aggiunte righe
            §3 (3 clock villain: 0/6, 2/8, 0/4), §4 (cosa sanno dei PG),
            §5 (ramo terra di Ushgar, ordine Hella-poi-Thorik), §7.E (E-08a).
            Decisioni DM: (a) ramo Ushgar aperto ma via Hella per prima;
            (b) Ushgar NON ha «Adattamento alla Luce» e il Controllo delle
            Fiamme dei tanarukk FA scattare la cecità alla luce - la faglia
            «i demoni accecano i propri comandanti» si apre; (c) sfida E
            (Ghaurush GS 18, EL 18 = APL+5) NON come primo incontro: si usa
            la variante Advanced GS 17, dentro il tetto; (d) approvati tutti
            e sei gli innesti I1-I6 nei beat giocati; (e) CdP Signore della
            Guerra Orchesco su Ushgar: non presa, resta Barbaro 13.
            Piani: plans/PIANO-INCANTATORI-MEMORABILI-*, PIANO-SFIDE-COMBINATE-*,
            PIANO-INNESTI-SFIDE-*.
```

```
2026-07-31  ARC-07 P4 GIOCATO E CHIUSO (Piano della Terra).
            Terros l'Antico SCONFITTO — party entrato senza riposare,
            quindi profilo standard (niente ramo 34 DV). Ultimo suono
            del guardiano: assenso (avevano curato i Cristalli).
            SMERALDO DELLA FORZA forgiato nella Corona: 2 gemme su 3
            accese (Topazio + Smeraldo), manca il Rubino.
            RITO §9 — scelta A, SACRIFICIO MATERIALE: 40.500 mo dal
            bottino dell'arco (Cuore di Terros incluso) + equipaggiamento
            personale. Il Peso nel corpo l'ha preso Thorik (rito dello Smeraldo): il
            -2 DES / +2 COS. Il party entra in ARC-08 sotto WBL: il delta
            si ripaga in ARC-08 come riconoscimento narrato (E-07c).
            SEME-MERCATO DI VARIS: preso, MAI TOCCATO, riposto nello
            zaino di TORDEK. Marchio NON attivo (si chiude col tocco);
            Varis non localizza nessuno. Terza strada non prevista dal
            modulo: registrata come canone in DEF-1 §6-bis.
            OROLOGIO HAMMERFIST: niente riposo prima di Terros -> 3g 20h;
            riposo nella Sala della Forgia (-4 h) -> 3g 16h. Consegna
            attesa all'ARC-08 ~3g 15h = Fase 0 PIENA.
            SBLOCCATA la condizione del potere «Diventare una Collina»
            dei Bracieri (TODO aperto sulla scheda di Tordek: finche' e'
            aperto, il potere NON esiste al tavolo).
            PROSSIMO: resurrezione di Hella (P3B / DEF-3).
```

<!-- auto:begin key=changelog -->
```
2026-08-01  ARTEFATTI — audit e sblocchi.
            BRACIERI: sbloccato «Diventare una Collina» (taglia Grande, 1/g).
            Canone DM: la PRIMA attivazione e' automatica e gratuita, quando
            uno scontro con una creatura Enorme o piu' grande porta Tordek
            sotto meta' pf; i Bracieri parlano solo quella volta ("Bestia
            grossa. Ci vuole un martello piu' grosso."). Dalle volte
            successive: azione di movimento, 1/giorno, e SOLO se sul campo
            c'e' una creatura Enorme+, un compagno a 0 pf, o Tordek sotto
            meta' pf. Fuori da quelle condizioni i guanti restano freddi.
            Nota: fra il -2 DES permanente del rito e il -2 dell'ingrandimento,
            da Grande Tordek ha 4 DES in meno di prima del Piano della Terra.
            AEGIS FANG: audit fatto, NESSUNO sblocco da Terros. Resta Stadio 0.
            Il Bane vs Fauci di Palude arriva dall'affresco A7 (prossima
            sessione); il risveglio pieno richiede Assedio della Forgia +
            Corona Senziente, cioe' la stessa sessione del Rubino.
            ANELLO: audit fatto, NESSUNO sblocco da Terros. Resta Riforgiato.
            Caos Ultimo solo se Zalkatar cade alla Torre Invisibile.
            Nuove schede in stile di casa: Aegis Fang Stadio 0 e Anello
            Riforgiato (entrambe con blocco DM "cosa arriva e da dove").

2026-09-12  LOTTO 4c — I DUE TEMPI DI state.md, SEPARATI (D3, DM 2026-09-11).
            §1 collocava i quattro PG DOPO la Battaglia di Hammerfist e in
            viaggio verso le quest dell'Arco 09, mentre §0 marca l'Arco 08
            come NON giocato e l'Arco 07 come in corso: la regola
            dell'intestazione ("tutto cio' che questo file dice dell'Arco 08
            e 09 e' canone preparato") non era applicata alla tabella che
            piu' di tutte descrive il presente. §1 ha adesso due colonne,
            "adesso al tavolo" e "canone preparato": nessun contenuto tolto,
            solo etichettato.
            COSTO MAI VERSATO. Il DM: "non ha ancora giocato la parte della
            resurrezione di Hella". §1 registrava per Thorik "-2 perm CON
            sacrificed for Hella's resurrection (NEVER restored)" e §7 lo
            ripeteva come debito morale contratto, insieme ai "500 PE" di
            Tordek: costi di una scena mai giocata, scritti al passato. Tolti
            dal presente e marcati "si contrae al rito" (ARC07-DEF-3 §5).
            Oggi Thorik ha -4 DES / +2 COS / +4 CAR, e basta.
            Hella e' morta: la riga di §1 lo dice, come gia' faceva la riga
            della Collana dei Semi Eterni in §6 - l'unica delle due che non
            si era sfasata.
            GIORNO DI MARCIA 19. Non e' un difetto di canone ma un tempo
            verbale: "Terrelton just fell as Hammerfist ended" al passato per
            un evento non giocato. Il Giorno 19 e' il punto di SINCRONIA a
            cui il calendario tornera' quando i PG viaggeranno indietro nel
            tempo nel P5 (ARC08-00-INDICE 17-19; ARC07-DEF-5 §94).
            LOG APPEND-ONLY INTATTI: le voci 2026-07-02 e 2026-07-23 citano
            il "-2 COS" perche' e' quel che i piani dicevano in quelle date.
            Sono record storici, e restano.
            DONI v2: la proposta di ridisegno dei tre Doni (§5 di ARC07-DEF-3)
            e' in plans/PROPOSTA-DONI-RESURREZIONE-HELLA.md e NON e' canone
            finche' il DM non la approva. Il master non e' stato toccato.

2026-09-12  I TRE DONI DELLA RESURREZIONE, RIDISEGNATI E APPROVATI (DM).
            ARC07-DEF-3 §5 sostituita. Un Dono non e' piu' una tassa ma un
            TRAPIANTO: il donatore da' un potere DEL PROPRIO ARTEFATTO, che lo
            lascia per sempre e germoglia in un seme della Collana. Il party
            non perde la capacita': cambia mano e cambia forma.
            THORIK dona il +2 di deflessione della Corona e resta a -1 CA
            permanente -> Hella ottiene lo SCUDO DEL CUSTODE (1/g, immediata,
            prende il danno di un alleato entro 9 m dimezzato). ECO DEL
            CUSTODE: ogni volta che lei lo usa, Thorik e' accelerato 3 round e
            si muove VERSO CHI E' STATO PROTETTO.
            TORDEK dona Ancoraggio della Montagna, che lascia i Bracieri ->
            PELLE DI ADAMANTIO, RD 3/adamantino. Verificato: e' la sua UNICA
            RD (l'Ibrido Treant non ne da', e la Via della Guardia non e' la
            strada che ha scelto).
            ARTEMIS dona 1d6 di Eldritch Blast, 7d6 -> 6d6 per sempre -> IL
            ROVO ELDRITCH, a volonta', contatto a distanza 18 m, 2d6. Il DM ha
            visto che il vecchio dono (azione standard extra) si SOVRAPPONEVA
            a quello di Thorik: stessa casella, dare tempo a un altro.
            LA CATENA: colpo da 40 -> dimezzato (20) -> meno la RD (17) ->
            Thorik scatta -> e Hella ha il Rovo, quindi non perde il turno.
            REAZIONI DEGLI ARTEFATTI, al dono e al rifiuto. Aegis Fang (Ego 14)
            smette di dubitare di Thorik, o lo giudica. I Bracieri avvertono un
            round prima, o tacciono una settimana. L'Anello si illumina di
            riflesso, o si spegne 24 ore. La Corona si scalda, o resta fredda
            al Rituale 4. Tutte reversibili: nessun malus permanente.
            RIFIUTO: il seme resta dormiente e l'artefatto reagisce, ma il
            riempimento retroattivo in ARC-09 resta. Il rifiuto e' una quest.
            COLLANA POTERE #6, finalmente definito (era [da definire col DM]
            da quando l'artefatto esiste): il seme RESTITUISCE al donatore cio'
            che ha ricevuto, una volta sola, per una scena, e decide HELLA.
            SUPERATO il vecchio eco «Filo dell'Ascia» su Aegis Fang: toglieva
            il Ritornante fino al Risveglio pieno, e contraddiceva il profilo
            dello Stadio 1 (+4 Sacra RITORNANTE). Il Ritornante resta.
            ARCHIVIO: 12 istantanee dei file toccati in
            07_.../\_ARCHIVIO/doni-v1-2026-09-12/, marcate come congelate.
            Slot ancora NON spesi: il rito non e' stato giocato.
```
<!-- auto:end key=changelog -->
