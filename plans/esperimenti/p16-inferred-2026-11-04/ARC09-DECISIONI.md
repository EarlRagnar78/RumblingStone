# P16 · lotto 3: le marcature aperte di ARC-09

Origine: P16 dell'indice §0 di `plans/STATO-E-ORDINE-DEI-PIANI.md`, dopo il lotto
2-bis (PR #312). Regola del DM del 2026-11-04: si chiude solo ciò che è già fatto,
risolto o superato, con la prova; il resto va a card di decisione vere, ognuna con
la consigliata, e la consigliata è la versione più forte, non la più semplice.

## 1. Il conto

`inventory_inferred.py` su main dopo la PR #312 (fcf66422): **61 aperte nel repo, 3
in ARC-09**. Nessuna delle tre è già risolta: tutte e tre vanno a card.

| # | Dove | Cosa |
|---|---|---|
| 1 | `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE1-ASSEDIO-MAPPA.md` r. 24 | Quanti uomini servono sulle mura di Rethmar |
| 2 | `Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md` r. 307 | Quanti uomini servono sulle mura di Dauth (manca la guarnigione nanica) |
| 3 | `Arco-Post-Hammerfist-P1C-Rituale-COMPLETO-SCALE.md` r. 894 | Quota del Cerchio Sacro nella Witchwood: 300 m sul mare |

## 2. Il nodo: la leva si somma o no?

La regola usata (Burghal Hidage del Wessex: circa 0,8 uomini per metro di mura) viene
dalla ricerca del 2026-10-22 (`plans/esperimenti/mappe-citta-2026-10-22/RICERCA-DIMENSIONI-CITTA.md`
§6-§7). Il DM ha reso canone piante, quote e taglie, ma non il conto dei difensori.

Il testo di Rethmar somma la leva degli uomini abili (circa 3.240) ai difensori degli
scenari di `Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md` §3 (da circa 1.280
a circa 3.980). Così però i rapporti di forza della tabella cambiano: nello scenario
peggiore si passa da 5,8 contro 1 a circa 1,6 contro 1, e la regola 6 dello stesso file
(«la battaglia è perduta senza PG») non regge più. Le due cose non possono essere vere
insieme: va deciso se la leva combatte sulle mura o no.

Per Dauth il conto non si chiude perché la guarnigione nanica non ha un numero in nessun
file del repo (lo segnala anche la ricerca, §7).

## 3. Card

1. **Chi difende le mura** (Rethmar e Dauth insieme).
2. **La guarnigione nanica di Dauth**.
3. **La quota della Witchwood**.

## 4. Risposte del DM


- Card 1 (chi difende le mura): **la leva non sale sulle mura** (DM 2026-11-05).
  Combattono solo i difensori degli scenari di ARMATE-SYNC §3. Rethmar copre i
  3.400 uomini della regola solo nel Leggendario; Dauth senza nani e lance tiene
  solo sud e ovest. La leva porta l'acqua, tiene le cisterne e spegne i fuochi.
- Card 2 (guarnigione di Dauth): **200 nani** (DM 2026-11-05). Da soli tengono la
  Porta Sud; con i 300 mercenari (se Tordek vince) e le 150 lance (se parte il
  sigillo di Thorik) si arriva a 650 soldati, un terzo dei 2.000 della regola.
- Card 3 (quota della Witchwood): **300 m sul mare, come scritto** (DM 2026-11-05).
  Il fondovalle dell'Elsir sta sotto la piana di Hammerfist (520 m) e lo sperone di
  Dauth (530 m).

Applicate come `[CANONE — DM 2026-11-05, P16, <tema>]` nei tre file; il testo vecchio
dei conti delle mura resta in un commento `<!-- storico -->`. ARC-09: 3 → 0 aperte.

**Da rivedere se** il DM cambia le taglie delle città o i difensori degli scenari.
