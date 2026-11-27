# TEMPLATE — AREA CHIAVE (Pathfinder 1e)

> **Cos'è**: la forma di una stanza o di un luogo con un incontro nei master
> della campagna, quella delle linee guida di *Dungeon* (standard di fatto di
> WotC e Paizo per le aree *keyed*), applicata nel repo da
> `rumblingstone-module-standard` §7 e `read-aloud-adulti.md` §2-bis.
> Fonte e misure: `plans/RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md` §1.4,
> `plans/PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE.md` §3.3. Decisione: D6 di quel
> piano `[CANONE — DM 2026-11-08, BOX-LUOGO D6]`. È la variante per i moduli in
> Pathfinder 1e (il Drappo, gli stand-alone in PF1e); la campagna gira in
> 3.5 con `area-chiave-template.md`. Le differenze sono solo nelle regole
> 4, 5 e 6 e nell'esempio.
>
> **Regole di compilazione**
> 1. Le voci stanno **in quest'ordine** e quelle che l'area non ha si
>    saltano: Read-aloud → Dati per il DM → Creature → Tattiche → Trappole →
>    Tesoro → Sviluppo → PX ad hoc. Solo l'**EL** nell'intestazione è
>    obbligatorio (in PF1e, il GS dell'incontro).
> 2. Il **box** è il box di luogo di `read-aloud-adulti.md` §2-bis: poche
>    frasi (di norma non più di quattro), spazio e luce per paragone, poi cosa
>    lo occupa, per ultima la cosa strana. **Nessuna creatura** (dove sono e
>    cosa fanno dipende da come arrivano i PG) e **nessuna misura** (ADR-0014,
>    `[CANONE — DM 2026-11-08, BOX-LUOGO D2]`): le misure vanno nei Dati per il
>    DM. Si ferma prima dell'azione. Un testo lungo è un handout, non un box.
> 3. L'etichetta del box **dichiara il tipo**: luogo, ingresso, round,
>    rivelazione o chiusura `[CANONE — DM 2026-11-08, BOX-LUOGO D3]`.
> 4. Ogni oggetto che si può rompere ha la **riga SRD**: spessore; Durezza;
>    pf; CD per sfondarlo o romperlo (tabelle *Doors* e *Walls* del capitolo
>    *Environment* del Core Rulebook PF1e, che per porte e pareti ha gli
>    stessi valori dell'SRD 3.5).
> 5. La **creatura non si trascrive**: statblock abbreviato (nome, quante,
>    GS, pf, rimando). Il rimando va al file del `Bestiario/` o alla voce
>    del Bestiary PF1e con la pagina; se la creatura non c'è, si cerca prima nel catalogo
>    (`scripts/monster_catalog.yaml`) e solo dopo si scrive, nel Bestiario.
> 6. Le abilità sono quelle di PF1e: Percezione (al posto di Osservare,
>    Ascoltare e Cercare), Furtività (al posto di Nascondersi e Muoversi
>    Silenziosamente), Conoscenze (nobiltà), Disattivare Congegni anche per
>    le serrature. Nella creatura abbreviata, se serve una manovra, BMC e DMC
>    al posto della Lotta.
> 7. Un fatto che serve e che nessuna fonte dà si marca
>    `[INFERRED — <domanda al DM>; base: <fonte o dato>]`
>    (`docs/reference/GUIDA-MARCATURE.md`).

---

### [Codice] · [Nome dell'area] (GS [N])

> **Read-aloud (luogo · [voce] lead).** *[Spazio e luce per paragone. Cosa lo
> occupa. Per ultima la cosa strana. Nessuna creatura, nessuna misura.]*

**Dati per il DM (non da leggere).** [Lato] × [lato] m, soffitto a [N] m,
[luce: buio / luce fioca / torce]. Pareti di [pietra grezza (Scalare CD 15) /
muratura (Scalare CD 20)]. [Porta di legno robusta, bloccata: 5 cm; Durezza 5;
pf 20; CD per sfondarla 23.] [Scopo dell'area, se il box non lo dice.] [Vie
d'uscita e prove: Percezione CD …, Disattivare Congegni CD …, Conoscenze (…)
CD ….]

**Creature.** [Nome] ([quante]): GS [N]; pf [N] ciascuno; statblock in
`Bestiario/mostri/[nome]-cr[N].md` [o Bestiary PF1e, «[voce]», p. [N]].

**Tattiche.** [Dal punto di vista della creatura, con le coordinate della
mappa: prima dello scontro, durante, quando smette.]

**Trappole.** [Nome della trappola: GS; tipo; Percezione CD; Disattivare Congegni
CD; innesco; reset; effetto.]

**Tesoro.** [Oggetti specifici, con il valore in mo.]

**Sviluppo.** [Chi sente lo scontro e in quanti round arriva; quando i nemici
si arrendono o fuggono; cosa cambia se i PG ripassano.]

**PE ad hoc.** [Solo se il terreno dà un vantaggio a una parte: GS
dell'incontro ±1 e il perché.]

---

## Esempio compilato

### A3 · La cripta del cavaliere (GS 5)

> **Read-aloud (luogo · Mercer lead).** *La volta è bassa come quella di una
> cantina, e la luce delle vostre torce non arriva agli angoli. Al centro, un
> sarcofago di pietra porta l'effigie di un cavaliere con le mani giunte su
> una spada. Tre torce spente nei loro anelli. Sul fondo, una grata di ferro
> chiusa da una catena e da un lucchetto nuovo.*

**Dati per il DM (non da leggere).** 9 × 9 m, soffitto a 3 m, buio. Pareti
di pietra grezza (Scalare CD 15). Grata di ferro: 5 cm; Durezza 10; pf 60; CD
per sollevarla o sfondarla 25 (Core Rulebook PF1e, *Doors*). Il
lucchetto: Disattivare Congegni CD 25. L'effigie: Conoscenze (nobiltà) CD 15
per riconoscere lo stemma.

**Creature.** Ombre (2): GS 3; pf 19 ciascuna; Bestiary PF1e, «Shadow», p. 245.

**Tattiche.** Escono dagli angoli quando un PG tocca il sarcofago o la grata.
Passano attraverso le pareti per non farsi circondare e colpiscono chi tiene
la torcia.

**Tesoro.** Nel sarcofago: spada lunga +1 (2.315 mo), 45 mo, due quarzi da
10 mo.

**Sviluppo.** Lo scontro non si sente oltre la grata. Le ombre non fuggono.
Se i PG tornano dopo averle distrutte, la cripta resta vuota.
