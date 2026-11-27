---
name: ramo-di-gruppo-campagna
description: Il primo tavolo registra la partita su campaign-group-rumblingstone (ADR-0090, PR #237 unita il 2026-10-12); il ramo vecchio è inservibile
metadata:
  type: project
  modified: 2026-10-11T22:54:39.783Z
---

Al 2026-10-11 il ramo `campaign-group-rumblingstone-dm-gianfranco` non ha storia comune con main (`git merge` → unrelated histories) e contiene solo la sessione 3 di prova di luglio. ADR-0090 (PR #237, unita il 2026-10-12 con il corredo della serata dopo il 25 settembre; l'ADR resta «proposta» finché Jfs non lo accetta) fa ripartire la partita su `campaign-group-rumblingstone` creato da main. Le patch della serata del 2026-09-25 (Hella risorta coi tre Doni; Thorik si prende il Debito della Radice, eco E-07g, prezzo [INFERRED]) sono in /mnt/project-files/sessione-2026-09-25/ con PASSI.md; Jfs le applica in locale con `git am`.

**Why:** ADR-0007 vieta il canone vivo su main; il ramo vecchio non riceve più main.
**How to apply:** la partita si scrive solo su campaign-group-rumblingstone; non committare xp-ledger.md (update_xp parte da 0 PE e dà livello 2). PR #235 (pozioni) unita il 2026-10-11. Seconda serata: corredo in `07_.../homebrew/sessione-notte-e-alba/`, stop sull'esito del duello prima della Scena 12 (rito e torque alla serata dopo). Le tattiche di DEF-4 sono canone (PR #238, 2026-10-12); la scena del Seme di Varis (DEF-1 §6-bis, la pergamena la legge Artemis) è il capitolo II del booklet. Aperta per Jfs: pozioni d'invisibilità del re nella Scena 4 per i gruppi futuri. Vedi [[weekly-audit-routine-scope]].

2026-11-21: il ramo vivo è `campaign-group-rumblingstone` (`-dm-gianfranco` è morto). Il clone dei thread è shallow: senza `git fetch --unshallow` main e il ramo risultano «unrelated histories». Spinti il 21/11 (testa ba754632d): le 4 patch del 05/11, il merge di main (nei conflitti di state si tiene il giocato del ramo), sessione 5 = 13/11 (barili, partenza), sessione 6 = 20/11 (tenda, alba, drago); il 02/11 non si è giocato. PX della 6: 3.412 + premi 500/800 = 4.712 a testa, Hella a 91.066 (14° al primo riposo). Il registro .ods lo aggiorna Jfs. Prossima serata: si parte dai danni del raggio di Artemis su Skullcrusher. Con Zog'tar nell'anagrafica png il controllo di coerenza vuole il residuo in plans/coerenza-residui.json.

Riga spostata dall'indice il 27/11 (tetto ADR-0139):
- Ramo della partita `campaign-group-rumblingstone`: allineato a main il 26/11 (f8a5f4de0), sessioni 5-6 confermate da Jfs (1.300 PX, tutti presenti). Debito della Radice di Thorik: opzione A, anima promessa alla Radice, salda al Cerchio Sacro in ARC-09 (scheda /mnt/project-files/debito-thorik-2026-11-26/). Aperto: quali pergamene ha comprato il gruppo (sessione 4 r.60). Da applicare da Jfs (se non già dentro): patch Bane (/mnt/project-files/sessione-2026-10-15/), patch Cintura (/mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md), canone Belkram. → [[ramo-di-gruppo-campagna]]
