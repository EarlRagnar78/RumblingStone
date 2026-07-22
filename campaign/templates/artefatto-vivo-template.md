# TEMPLATE — ARTEFATTO VIVO (documentazione a 3 livelli)

> **Scopo (T4, piano trasversale 2026-07-03)**: gli artefatti dei PG sono
> "vivi" — si sbloccano a stadi tramite quest e rituali. Senza uno standard,
> ogni artefatto accumula generazioni di file e né il DM né il giocatore
> sanno più quale valga (il caso Corona). Questo template fissa la
> struttura che ha funzionato meglio nel repo (cartella Tordek, benchmark).
>
> **Regola dei 3 documenti** — per ogni artefatto esistono ESATTAMENTE:
> 1. **SCHEDA-DM (master)** — tutto: stadi, trigger, poteri nascosti, hook.
> 2. **SCHEDA-GIOCATORE-STATO-ATTUALE** — una pagina, SOLO poteri sbloccati.
> 3. **La riga in `campaign/state.md` §6** — stato corrente sintetico.
> Tutto il resto della cartella è *annesso* (scene, stadi giocati, export)
> o 📸 snapshot con banner — censito in `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md`.
> File numerati in ordine di progressione (`00_`, `01_`, `02_`…, stile Tordek).

---

## 1. SCHEDA-DM — struttura

```markdown
# [Nome artefatto] — Guida DM (MASTER)

> **Stato**: ⭐ MASTER canonico (D9). Portatore: [PG]. Stato corrente:
> state.md §6. Scheda giocatore: [link]. Matrice: ARTEFATTI-MATRICE-VERSIONI.md.

## Identità
Tipo/slot/peso/allineamento/aura/LI — lore in 5-10 righe — aspetto.
Prerequisiti di legame. Cosa VUOLE l'artefatto (volontà/ego, se senziente).

## TABELLA DI PROGRESSIONE (il cuore della scheda)
| Stadio | Trigger di sblocco (quest/rituale/evento) | Poteri che sblocca | Stato | Documentato in |
|---|---|---|---|---|
| 0 — Base | come si lega | … | ✅/🟡/⬜ | file |
| 1 — [nome stadio] | … | … | … | … |
| …ultimo — Risveglio pieno | … | … | ⬜ | … |

## Poteri per stadio (meccanica 3.5 completa)
Un blocco per stadio: potere, tipo (Str/Mag/Sop), azione, CD, frequenza,
costi. SRD only; nulla di inventato senza flag [INFERRED].

## Costi e vincoli
Cosa costa usarlo (invecchiamento, COS, XP, mo…), quando si rifiuta,
cosa lo spegne. Oggetti/cariche SPESI = elenco esplicito (anti-incoerenza).

## Sinergie
Rimando a PG/Artefatti/SINERGIE-ARTEFATTI-MASTER.md (non duplicare qui).

## Hook e quest legate
Dove l'artefatto "tira" la storia: quest di sblocco future, PNG che lo
cercano, echi (formato ARC-09: evento → eco → quando riemerge).
```

## 2. SCHEDA-GIOCATORE-STATO-ATTUALE — struttura

```markdown
# [Nome] — Scheda Giocatore (STATO ATTUALE)

> DM: unica scheda da dare al giocatore. Solo poteri sbloccati. A ogni
> sblocco: stampare lo snapshot nuovo, ritirare il vecchio.

## PAGINA — [etichetta temporale: "oggi al tavolo (ARC-XX)"]
Descrizione sensoriale breve (come lo vede/sente il PG).
| Potere | Effetto 3.5 | Costo/frequenza |
Accenno NON-spoiler a ciò che manca ("le incastonature fredde").
Vincoli comportamentali visibili al PG.

## Registro sblocchi (compila il DM, a penna)
| Data (sessione) | Sblocco/spesa | Visto dal giocatore? |
```

*Se il repo è "scritto in avanti" (stato preparato oltre il tavolo), la
scheda può avere DUE pagine-snapshot etichettate — vedi l'esemplare
`00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` della Corona.*

## 3. Riga in state.md §6 — formato

`| [Artefatto] | [PG] | [stadio] | [poteri usabili ORA, spesi marcati] |`

---

## Checklist di adozione (lotti T6 del piano trasversale)

① Eleggere/creare la SCHEDA-DM con tabella di progressione →
② generare la SCHEDA-GIOCATORE dallo stadio corrente →
③ allineare la riga §6 →
④ banner 📸/~~DEPRECATO~~ su ogni altro file della cartella →
⑤ aggiornare `ARTEFATTI-MATRICE-VERSIONI.md` →
⑥ `grep` anti-incoerenza sugli oggetti spesi (Rubino, Cuore di Moradin).

**Esemplari nel repo**: Corona (scheda giocatore a 2 snapshot) · Tordek
(file numerati per stadio) · Collana (scheda pronta pre-forgiatura con
slot-dono legati al ramo del rifiuto P3B §2-BIS).
