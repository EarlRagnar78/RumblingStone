# ADR-0057 — La quarta colonna è di tutto il repo: il dettaglio che non dici appartiene a chi fa la domanda

- **Stato**: accettata (2026-09-18), **attuata** sul solo blocco che oggi esiste
- **Decisore**: DM — *«l'unica cosa da prendere è l'ADR quarta colonna, che può
  essere usata in diversi contesti nel repo RumblingStone nei vari archi. Gli
  ADR interni li lascerei all'Abbazia [...] ma ovviamente la versione
  nell'Abbazia rimane così com'è senza estensione»*
- **Rapporti**: promuove `ADR-12` interno a
  `10-stand-alone/L'abbazia Della Rotta Sicura` · rafforza
  [ADR-0014](ADR-0014-regia-sensoriale-obbligatoria.md) §2 (*il mostro
  spiegato*) · registrato in `skills/REGISTRO-NORME-EDITORIALI.md`
  ([ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md))

---

## Contesto

L'Abbazia della Rotta Sicura porta **39 schede sensoriali** e, dal suo
`ADR-12` interno, una **quarta colonna** accanto a Occhi / Orecchie /
Pelle-naso: **«Cosa NON dire»**.

> *Contesto:* il rischio del dettaglio atmosferico è che il DM racconti anche
> la scoperta.
> *Decisione:* ogni scheda ha una colonna «cosa NON dire» che è vincolante
> quanto le altre tre.
> *Conseguenze:* le tabelle raddoppiano di larghezza e diventano meno
> stampabili su A4 verticale. È il prezzo giusto: senza quella colonna
> l'atmosfera divora l'indagine.

Il congegno era **l'unico** del repo che un banco avesse e nessun altro: la
misura del 2026-09-18 lo trovava in un documento su cento.

## Decisione

**La quarta colonna diventa norma del repo principale.** Dove un documento
descrive un ambiente per sensi, porta anche ciò che il DM **non** deve dire.

Due precisazioni che il DM ha dato esplicitamente, e che sono la decisione:

1. **Si prende solo questa.** Gli altri dodici ADR interni dell'Abbazia
   restano dell'Abbazia. Non diventano un formato per gli archi.
2. **L'Abbazia non si tocca.** La sua versione resta esattamente com'è, nella
   sua forma a tabella, senza essere riscritta per somigliare allo standard
   nuovo. La promozione è **additiva verso l'esterno**, non retroattiva verso
   la fonte.

### La forma, che negli archi non è una colonna

⚠️ **Negli archi le schede sensoriali non sono tabelle: sono elenchi.** DEF-1
scrive `- **Vista**: …` / `- **Udito**: …`. Imporre la tabella dell'Abbazia
significherebbe riscrivere la forma per portare il contenuto, che è il
contrario dello scopo.

La norma è quindi sul **blocco**, non sulla colonna: un blocco sensoriale — in
qualunque forma, tabella o elenco — chiude con una voce **«Cosa NON dire»**,
vincolante quanto le altre. In tabella è la quarta colonna; in elenco è
l'ultimo punto.

## 🔎 Il raggio vero, misurato prima di scrivere la norma

Cercando i blocchi sensoriali in **tutto** il repo giocabile (archi 00-09 e
stand-alone, esclusi archivi e booklet generati):

| Dove | Blocchi sensoriali | Con «cosa NON dire» |
|---|---:|---:|
| Abbazia *(non si tocca)* | 39 schede | 39 |
| **Tutto il resto del repo** | **1** | 0 → **1** |

🔴 **Uno.** `ARC07-DEF-1` §4, l'arrivo al Piano della Terra. Non c'è nessun
altro blocco sensoriale strutturato in nove archi: gli archi il sensoriale lo
scrivono **dentro la prosa dei read-aloud**, non in schede.

**Questo cambia cosa ci si può aspettare dalla norma, e va detto.** Come
*retrofit* vale un posto solo. Il suo valore è **prospettico**: diventa la
regola dei blocchi che verranno, e in particolare dei lotti **S4-S6** di
`PIANO-PORTARE-IL-MESTIERE-DEI-BANCHI` — DEF-5, la Torre e la Battaglia Finale
hanno **zero read-aloud narrativi** e vanno scritti da capo.

⚠️ **Non ho allargato la norma per farle trovare più lavoro.** Il principio
(«il dettaglio che non dici appartiene a chi fa la domanda») si applicherebbe
anche a ogni read-aloud che sta sopra un indizio, e sarebbe una norma molto
più grossa. Il DM ha detto *«serve solo dove ci sono tabelle sensoriali»*, e
la decisione resta quella.

## Cosa è stato scritto, nel blocco che esiste

`ARC07-DEF-1` §4 descrive l'arrivo: cristalli, silenzio, un **BOOM** lontano,
aria densa, ozono. Tre cose che quel blocco può rovinare:

| Non dire | Perché |
|---|---|
| che il BOOM sono i cristalli **vivi** | è la rivelazione dell'**Incontro 2** (§6). Detto qui, §6 diventa una conferma |
| che il *pull* laterale **indica la strada** | la bussola è **Aegis Fang che vibra**, e si guadagna. Il pull è una stranezza del posto |
| **«magia elementale»** | i PG sentono **ozono**. La categoria sta nello statblock (ADR-0014 §2) |

⚠️ **DEF-1 è 🟡 in corso al tavolo**, e l'aggiunta rispetta l'assunzione D3 del
piano: è **additiva e rivolta al DM**, non riscrive prosa che i giocatori
hanno già sentito.

## Conseguenze

**Buone.**
- Il congegno migliore del banco esce dal banco, che era la domanda.
- Ha già un rilevatore (`quarta colonna sensoriale` in `misura_craft.py`),
  esteso qui a riconoscere la forma «Cosa NON dire» degli archi.

**Costi, dichiarati.**
- ⚠️ **Il prezzo dell'Abbazia vale anche qui**: in stampa la riga in più
  allarga il blocco. In elenco costa meno che in tabella — è il motivo per cui
  la forma a elenco è ammessa.
- ⚠️ **Non è un cancello bloccante.** Non esiste modo automatico di sapere se
  un blocco sensoriale *avrebbe dovuto* avere un «non dire»: il rilevatore
  conta chi ce l'ha, non accusa chi non ce l'ha. Un gate che pretendesse la
  riga su ogni blocco sarebbe verde su una riga vuota.
- 🔴 **Con un solo blocco, la norma è quasi tutta credito.** Se i lotti S4-S6
  non arrivano, questo ADR resta la quarta cosa scritta e non applicata del
  repo — ed è esattamente il difetto che ADR-0056 ha appena documentato.
  Questa riga esiste per rendere quel fallimento riconoscibile.

## Alternative scartate

1. **Portare tutti e 13 gli ADR interni negli archi.** Scartata dal DM: 13 ADR
   dentro un modulo servono a chi lo pubblica, non a chi l'ha scritto.
2. **Riscrivere le 39 schede dell'Abbazia nella forma nuova.** Scartata dal
   DM, e giustamente: l'Abbazia è il banco perché funziona così com'è.
3. **Estendere il principio a ogni read-aloud sopra un indizio.** Scartata:
   sarebbe una norma molto più grossa di quella decisa, e allargarla da solo
   sarebbe la stessa presunzione di misurare senza leggere la fonte.
