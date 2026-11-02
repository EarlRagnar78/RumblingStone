# [Nome PNG] — [epiteto o ruolo in una riga] [RIMANDO]

> Modello della scheda di un PNG o villain nominato, [ADR-0091](../../plans/adr/ADR-0091-la-scheda-del-png-ha-una-forma.md)
> (prima: piano libreria, lotto L0, 2026-07-08). Due file al più:
> - il **dossier** (questo): `Bestiario/villain/<Nome>/<Nome>.md` o
>   `Bestiario/png/<Nome>/<Nome>.md`; un PNG minore può stare in un file
>   singolo senza cartella;
> - lo **statblocco** `nome-crN.md` nella stessa cartella (modello in fondo).
>
> I numeri stanno solo nello statblocco: il dossier ci rimanda con
> `[RIMANDO]` nel titolo e la riga `**Key stats**: →`. Regole: D&D 3.5 SRD;
> dato non attestato → `[INFERRED — needs DM confirmation]`; sezione
> obbligatoria senza fonte → `[DA SCRIVERE — …]`, mai riempita a caso; boost
> solo via `skills/npc-villain-boosting/` con `Boost log:`; prima di scrivere
> numeri cercare in `Bestiario/` e in `pregen-pcgen/`.
> Controllo: `python3 scripts/validate_bestiario.py --forma`.

**Role**: ally|villain|neutral (contesto e arco, es. "villain, Arco 08")
**Status**: alive|dead|unknown (+ da quando/perché)
**Location**: dove si trova ORA (allineato a `campaign/state.md`)
**Motivation**: cosa vuole, in 1-2 righe
**CR**: N | **Race/Class**: razza, classi, allineamento
**Key stats**: → `nome-crN.md` (questa cartella)
**Token**: `Bestiario/tokens/...` (se esiste)

---

## In breve
*(facoltativa)* Due o tre righe: chi è per il tavolo, in che archi.

## Chi è
La storia, fino a oggi.

## Aspetto e voce
Com'è, come si muove, come parla.

## Cosa vuole
Il *Want* che non riguarda i PG, e cosa teme.

## Nella campagna
Dove e quando compare, cosa offre, le risorse che porta. Le scene lunghe
(read-aloud, offerte, risorse di campagna) come `###`.

## Con i PG
*(facoltativa)* Una voce `###` per PG.

## Rapporti
*(facoltativa)* Con chi sta, contro chi.

## In combattimento
*(obbligatoria se c'è uno statblocco)* Come combatte, in prosa; i numeri e le
tattiche round per round stanno nello statblocco.

## Esiti possibili
I rami aperti, legati ai dadi e alle scelte dei PG (regola D13: mai copioni).

## Al tavolo
*(facoltativa)* Battute, cose da fare e da non fare.

## Segreti del DM
*(facoltativa)* Quello che i giocatori non devono leggere.

## Fonti e canone
Decisioni del DM con la data, adattamento da *Red Hand of Doom*
(`[Private — Red Hand of Doom, p.X]`), file dove compare.

Boost log: (vuoto finché non boostato)

---

<!-- Modello dello statblocco `nome-crN.md`: si copia in un file a parte. -->

```markdown
# Nome — epiteto (razza, classi) [ACCEPTED — DM-canon YYYY-MM-DD] | [INFERRED — needs DM confirmation]
**Faction**: … | **Role**: … | **Environment**: … | **CR**: N | **Source**: … | **Status**: accepted|inferred|transcribed

(blocco statblocco di ADR-0021)

**Iniziativa** … · **Sensi** …

**Difesa** CA …, contatto …, colto alla sprovvista … · pf … (DV …) · TS Temp …, Rifl …, Vol … · RD, immunità, resistenze · Debolezze

**Attacco** Vel … · Mischia … · Distanza … · Attacchi speciali … · Incantesimi (livello e CD, mai il testo)

**Statistiche** For … Des … Cos … Int … Sag … Car … · BAB …; Lotta … · Talenti … · Abilità … · Linguaggi … · Qualità speciali … · Equipaggiamento …

**Capacità speciali**
- **Nome (Str/Sop/Mag)**: …

**Tattiche**
- *Prima del combattimento*: …
- *Durante il combattimento*: …
- *Morale*: la soglia di pf o la condizione in cui smette, e cosa fa allora

(facoltativi: benchmark PF1e, combinazioni ed EL)

Notes: dove si usa nella campagna, e il rimando al dossier.

Boost log: …
```
