# Gnoll Hyenodon Rider [CANONE — DM 2026-05-05]
**Faction**: gnoll | **Role**: mounted-melee | **Environment**: plain | **CR**: 4 | **Source**: MM Gnoll + MM Dire Hyena (Hyenodon) | **Status**: inferred


```statblocco
gs: 4
tipo: Medium humanoid (gnoll), 2d8+2 — in sella a un ienodonte 5d8+12
taglia: Media
spazio: 1,5 m (in sella 3 m, quello della cavalcatura Grande)
portata: 1,5 m (3 m con la lancia da cavaliere, e allora non i quadretti adiacenti)
sensi: scurovisione 18 m
ca: 16
ca-dettaglio: (+4 cuoio borchiato +1, +2 scudo)
pf: 11
pf-dado: 2d8+2
ts: Temp +4, Rifl +0, Vol +0
velocita: 9 m (a piedi) / 15 m in sella
iniziativa: +0
attributi: For 15 Des 10 Cos 13 Int 8 Sag 11 Car 8
attacchi:
  - Mischia lancia da carica +3 (1d8+3; in carica +5 e danno ×2)
voci:
  - Talenti: Combattere in Sella
  - **Cavalcatura — ienodonte**: 5d8+12, 34 pf, CA 14, morso +9 (1d8+7) e far inciampare; TS Temp +6, Rifl +6, Vol +2
  - Impiego: 60 cavalieri, gli Abbattitori
fonte: letto dalla prosa (CA, pf, attacchi e talenti li dichiara la scheda); derivati dalle tabelle SRD i soli TIRI SALVEZZA di cavaliere e cavalcatura, che la prosa non dava. ⚠️ Il blocco descrive il CAVALIERE: i numeri della cavalcatura stanno in una voce, perché una scheda sola non può avere due CA e due mucchi di punti ferita
```

Rider HD 2d8+2 (11 HP) + Hyenodon HD 5d8+12 (34 HP) mount. Rider AC 16 (studded+shield). Mount AC 14. Charge lance +5 (1d8+3 x2 on charge). Mount bite +9 (1d8+7) + trip. Feats: Mounted Combat. Notes: 60 cavalry Abbattitori.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12, lotto 1-bis, regola del DM «il numero più forte, se si ricostruisce»): con Des 10 non c'è bonus di Destrezza: la CA 16 si tiene dichiarando il cuoio borchiato +1. La CA non cambia.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12, lotto 1-bis): campo `sensi` aggiunto, gnoll: scurovisione 18 m (SRD). La scheda non la scriveva.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-13, decisione del DM sulla card): 2 DV danno 1 talento e la scheda ne aveva 3. Resta **Combattere in Sella**; tolti Attacco in Sella e Carica Poderosa. La lancia in carica a cavallo fa danno doppio di suo (SRD): nessun numero cambia. Per riaverli serve un livello da guerriero, che alza il GS.
