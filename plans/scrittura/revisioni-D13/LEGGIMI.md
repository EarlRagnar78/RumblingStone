# Il lotto D13 · «sembra» e «pare» nei box, da approvare

D13 (2026-10-01): nel read-aloud niente «sembra» né «pare», perché dicono al
tavolo che il narratore non sa cosa c'è. Questi undici documenti propongono la
correzione, file per file.

✅ **Approvato dal DM il 2026-10-03 e applicato**: tutte le 27 modifiche, le
quattro da guardare comprese. Due documenti (DEF-4 e ARC08-01) sono stati
rigenerati sul testo di oggi prima di applicarli, perché i due master erano
cambiati dopo la revisione; le modifiche sono le stesse. Il conto è in
`plans/scrittura/miglioramenti.json`: segnalazioni da 293 a 265, punteggio MQM
+2,52 punti sugli undici file. Sui tre box «sembra… e invece» il DM ha deciso
con D17: restano.

## Come si approva

Ogni documento ha in testa le garanzie e la lettura prima e dopo, poi la
tabella delle modifiche. Si spunta `[x]` nella colonna «ok» di quelle che vanno
bene, poi, su un ramo che non sia `main`:

```
python3 scripts/ciclo_prosa.py applica plans/scrittura/revisioni-D13/REVISIONE-….md --data AAAA-MM-GG
```

Con `--auto` si applicano anche le modifiche segnate ✓ nella colonna «auto», e
il documento le riscrive come `[x] auto`. Il comando rimisura il file e dice
cosa resta.

## I numeri

Il rilevatore contava 34 box; 4 usavano «appare» nel senso di «diventa
visibile», che la norma non vieta: tolto dal rilevatore, i box sono **30 su
501**. Di questi:

| | box | modifiche |
|---|---:|---:|
| corretti in questo lotto | 25 | 27 |
| … applicabili senza lettore (colonna «auto») | | 23 |
| … lasciati al lettore | | 4 |
| lasciati come sono, con la ragione sotto | 5 | |

Tutti e undici i documenti: nessun controllo peggiora, nessun nome, numero o
CD cambia, nessuna modifica senza una norma.

| File | Modifiche | Auto | Gulpease prima → dopo |
|---|---:|---:|---|
| `ARC07-DEF-1-PIANO-TERRA-TERROS.md` | 1 | 1 | 65,1 → 65,1 |
| `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` | 1 | 1 | 69,3 → 69,2 |
| `ARC08-01-GUIDA-DM.md` | 8 | 8 | 59,7 → 59,8 |
| `PortaleForgia-P1-REVISED-Corretta.md` | 2 | 2 | 86,7 → 86,8 |
| `PortaleForgia-P2-REVISED-Corretta-PARTE1.md` | 6 | 3 | 83,7 → 83,6 |
| `PortaleForgia-P3-PianoFuoco-PARTE1.md` | 3 | 3 | 84,3 → 84,0 |
| `PortaleForgia-P3-PianoFuoco-PARTE2.md` | 2 | 2 | 90,0 → 89,7 |
| `La_Piramide_Ricalibrata.md` | 1 | 1 | 79,3 → 78,8 |
| `CORREZIONE-Boss-Fauci.md` | 1 | 1 | 100 → 100 |
| `Arco-Post-Hammerfist-P2D-PALIO-PROVE-AMMISSIONE.md` | 1 | 0 | 81,4 → 80,3 |
| `Arco-Post-Hammerfist-HOOKS-Hella-SacredForest.md` | 1 | 1 | 75,9 → 75,9 |

## Le quattro che vanno guardate

- **P2-PARTE1, #3 e #4**: «Un secondo sembra minuto. Un minuto sembra
  istante.» Vanno approvate insieme: corretta da sola, ognuna lascia l'altra
  nel box, e la segnalazione non scende.
- **P2-PARTE1, #1**: «singolo» → «un», il ritocco della stessa frase della #2.
  Da solo non corregge niente.
- **P2D-PALIO**: «La cassa sembra… respirare» → «si gonfia e si sgonfia».
  Corretta per la norma, ma il box perde 1,1 punti di Gulpease, appena oltre
  la tolleranza di uno, e l'automatico la lascia a chi legge.

## I cinque box che restano, e perché

| File, riga | Il passaggio | Perché resta |
|---|---|---|
| `ARC07-DEF-1`, r.1189 | «quella che **sembrava** una parete — è una palpebra» | l'apparenza è il contenuto: la frase dopo la smentisce |
| `PortaleForgia-P3-PianoFuoco-PARTE2`, r.31 | «**Sembra** luogo riposo sicuro… e non lo è» | come sopra |
| `ARC08-01-GUIDA-DM`, r.961 | «quello che inizialmente **sembrava** una macchia scura si rivela…» | come sopra |
| `ARC08-01-GUIDA-DM`, r.1441 | l'ettin: «Attenti, **sembrano** pericolosi» | è un PNG che parla: la norma è sulla voce narrante |
| `mass_combat_guide_Dm.md`, r.475 | «Proprio quando tutto **sembrava** [situazione]…» | è un modello da riempire, con le parentesi quadre |

I tre box «sembra… e invece» sono un confine che la norma non scrive. È la
**D17** di PIANO-AGENT-SKILLS-ESTERNE: se il DM lo approva, entra in
`read-aloud-adulti.md` §1 punto 7 e nel rilevatore.

## Cosa questo lotto non fa

Le riscritture toccano solo la frase con «sembra» o «pare». I box di
`PortaleForgia-P1/P2/P3` hanno altri difetti misurati (traduttese telegrafico,
parentesi, box oltre le 12 righe, metrature): `ciclo_prosa.py segnala` li
elenca, e sono un lavoro per un'altra revisione.
