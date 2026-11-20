# Hobgoblin Regular (Warrior 4)
**Faction**: red-hand | **Role**: fodder | **Environment**: any | **CR**: 3 | **Source**: PCGen save `Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/hobgoblin regular 4 liv.pcg` + `regolari/hobgoblin_gegular -cr3.pcg` (solo .pcg, nessun export) | **Status**: inferred


```statblocco
gs: 3
tipo: Medium humanoid (goblinoid), Warrior 4, LE
taglia: Media
spazio: 1,5 m
portata: 1,5 m
ca: 19
ca-dettaglio: (+5 cotta di maglia, +3 scudo pesante di acciaio +1, +1 Des)
pf: 26
ts: Temp +9, Rifl +3, Vol +1
attributi: For 14 Des 13 Cos 14 Int 10 Sag 9 Car 8
voci:
  - Equipaggiamento da combattimento: pozione di cura ferite moderate
  - Altro equipaggiamento: cotta di maglia perfetta, scudo pesante di acciaio +1, spada lunga perfetta, arco lungo composito (+1 For), mantello della resistenza +1, abito da esploratore
fonte: valori approssimati nella prosa d'origine (scritti con «~»)
```

> `attributi` del DM (card del 2026-11-20, RC-001): quelli del .pcg citato in testa più i modificatori razziali dell'hobgoblin (+2 Des, +2 Cos). La scheda è uscita dalla marca di `scripts/genera_attributi.py`, come Karruk.

Medium humanoid (goblinoid), Warrior 4, LE. Caratteristiche attestate dal .pcg: For 14, Des 10-11, Cos 12, Int 10, Sag 9-10, Car 8. **Valori derivati** (build senza export, confermati dal DM 2026-10-18; Tempra +8 con Tempra Possente e il mantello): hp 26 (4d8+8); AC 19 come il regular 3 (stesso equip, Des +1); TS Temp +9, Rifl +3, Vol +1 (mantello della resistenza +1 incluso); BAB +4; spada lunga +7 (1d8+2/19-20), arco +5.
Notes: versione veterana-junior del regular 3; il DM confermi i derivati prima dell'uso.

> correzione 3.5 da `scripts/verifica_scheda.py` (2026-11-12, scelta del DM «tenere il numero, dichiarare la sorgente»): *mantello della resistenza +1* aggiunto all'equipaggiamento (SRD, 1.000 mo), perché Riflessi +2 superava il conto senza un bonus dichiarato. Il mantello vale per tutti e tre i tiri salvezza: Tempra +7 → **+8**, Volontà +0 → **+1**. Prezzo da ricontrollare col lotto della ricchezza per livello.

> RC-001 (2026-11-19, ADR-0134): corredo trascritto dall'equipaggiamento del salvataggio PCGen citato in testa (`hobgoblin regular 4 liv.pcg`), lo stesso del regular 3. Valore 3.295 mo contro i 4.300 del livello effettivo 5 (4 DV, hobgoblin +1; DMG 3.5, Tabella 4-23). Nessun numero cambia qui. Il .pcg salva le caratteristiche prima dei modificatori razziali (Des 11, Cos 12 diventano 13 e 14 per un hobgoblin): con quelle la CA 19 torna, Tempra e Riflessi no. Decisione del DM sulla card del 2026-11-20: vedi la riga che segue.

> RC-001 (2026-11-20, ADR-0134) `[CANONE — DM 2026-11-20, RC-001]`: applicati i modificatori razziali dell'hobgoblin (+2 Des, +2 Cos) che il .pcg non scrive, scelta del DM sulla card. Des **11 → 13**, Cos **12 → 14**; Tempra **+8 → +9** (4 base, +2 Cos, +2 Tempra Possente, +1 mantello), Riflessi **+2 → +3** (1 base, +1 Des, +1 mantello); pf 26 come media di 4d8+8; arco **+4 → +5**; la CA 19 ora torna (10, +5 cotta di maglia, +3 scudo pesante +1, +1 Des).
>
> Valori superati il 2026-11-20 (RC-001): Des 11, Cos 12, Tempra +8, Riflessi +2, arco +4, pf «4d8+4».
