# TEMPLATE — AREA CHIAVE (D&D 3.5)

> **Cos'è**: la forma di una stanza o di un luogo con un incontro nei master
> della campagna, quella delle linee guida di *Dungeon* (standard di fatto di
> WotC e Paizo per le aree *keyed*), applicata nel repo da
> `rumblingstone-module-standard` §7 e `read-aloud-adulti.md` §2-bis.
> Fonte e misure: `plans/RICERCA-STANDARD-PROSA-WOTC-PAIZO-2026-09.md` §1.4,
> `plans/PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE.md` §3.3. Decisione: D6 di quel
> piano `[CANONE — DM 2026-11-08, BOX-LUOGO D6]`. Variante PF1e:
> `area-chiave-template-pf1e.md`.
>
> **Regole di compilazione**
> 1. Le voci stanno **in quest'ordine** e quelle che l'area non ha si
>    saltano: Read-aloud → Dati per il DM → Creature → Tattiche → Trappole →
>    Tesoro → Sviluppo → PX ad hoc. Solo l'**EL** nell'intestazione è
>    obbligatorio.
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
>    *Dungeons* dell'SRD).
> 5. La **creatura non si trascrive**: statblock abbreviato (nome, quante,
>    GS, pf, rimando). Il rimando va al file del `Bestiario/` o alla voce
>    SRD; se la creatura non c'è, si cerca prima nel catalogo
>    (`scripts/monster_catalog.yaml`) e solo dopo si scrive, nel Bestiario.
> 6. Le abilità sono quelle della 3.5: Osservare, Ascoltare, Cercare,
>    Nascondersi, Muoversi Silenziosamente, Conoscenze (nobiltà e regalità).
> 7. Un fatto che serve e che nessuna fonte dà si marca
>    `[INFERRED — <domanda al DM>; base: <fonte o dato>]`
>    (`docs/reference/GUIDA-MARCATURE.md`).

---

### [Codice] · [Nome dell'area] (EL [N])

> **Read-aloud (luogo · [voce] lead).** *[Spazio e luce per paragone. Cosa lo
> occupa. Per ultima la cosa strana. Nessuna creatura, nessuna misura.]*

**Dati per il DM (non da leggere).** [Lato] × [lato] m, soffitto a [N] m,
[luce: buio / luce fioca / torce]. Pareti di [pietra grezza (Scalare CD 15) /
muratura (Scalare CD 20)]. [Porta di legno robusta, bloccata: 5 cm; Durezza 5;
pf 20; CD per sfondarla 23.] [Scopo dell'area, se il box non lo dice.] [Vie
d'uscita e prove: Cercare CD …, Disattivare Congegni CD …, Conoscenze (…)
CD ….]

**Creature.** [Nome] ([quante]): GS [N]; pf [N] ciascuno; statblock in
`Bestiario/mostri/[nome]-cr[N].md` [o SRD «[voce]»].

**Tattiche.** [Dal punto di vista della creatura, con le coordinate della
mappa: prima dello scontro, durante, quando smette.]

**Trappole.** [Nome della trappola: GS; tipo; innesco; reset; effetto; Cercare
CD; Disattivare Congegni CD.]

**Tesoro.** [Oggetti specifici, con il valore in mo.]

**Sviluppo.** [Chi sente lo scontro e in quanti round arriva; quando i nemici
si arrendono o fuggono; cosa cambia se i PG ripassano.]

**PX ad hoc.** [Solo se il terreno dà un vantaggio a una parte: EL ±1 e il
perché.]

---

## Esempio compilato

### A3 · La cripta del cavaliere (EL 5)

> **Read-aloud (luogo · Mercer lead).** *La volta è bassa come quella di una
> cantina, e la luce delle vostre torce non arriva agli angoli. Al centro, un
> sarcofago di pietra porta l'effigie di un cavaliere con le mani giunte su
> una spada. Tre torce spente nei loro anelli. Sul fondo, una grata di ferro
> chiusa da una catena e da un lucchetto nuovo.*

**Dati per il DM (non da leggere).** 9 × 9 m, soffitto a 3 m, buio. Pareti
di pietra grezza (Scalare CD 15). Grata di ferro: 5 cm; Durezza 10; pf 60; CD
per sollevarla o sfondarla 25 `[SRD: Doors]`. Il lucchetto: Scassinare
Serrature CD 25. L'effigie: Conoscenze (nobiltà e regalità) CD 15 per
riconoscere lo stemma.

**Creature.** Ombre (2): GS 3; pf 19 ciascuna; SRD «Shadow».

**Tattiche.** Escono dagli angoli quando un PG tocca il sarcofago o la grata.
Passano attraverso le pareti per non farsi circondare e colpiscono chi tiene
la torcia.

**Tesoro.** Nel sarcofago: spada lunga +1 (2.315 mo), 45 mo, due quarzi da
10 mo.

**Sviluppo.** Lo scontro non si sente oltre la grata. Le ombre non fuggono.
Se i PG tornano dopo averle distrutte, la cripta resta vuota.
