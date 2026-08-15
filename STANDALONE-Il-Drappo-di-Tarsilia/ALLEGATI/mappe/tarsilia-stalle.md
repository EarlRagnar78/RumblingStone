# Tarsilia — le stalle dell'Istrice (assalto notturno)

**Dimensioni**: 31,5 m × 22,5 m (21 colonne × 15 righe, scala 1,5 m/quadretto)  
**Origine**: generata da `scripts/compile_map_json.py` (contratto JSON → griglia; non modificare la griglia a mano, rigenerala dal JSON)  
**SVG**: rigenerare con `python3 scripts/render_map_svg.py <questo-file>.md`  
**VTT**: esportare con `python3 scripts/export_uvtt.py <questo-file>.md`

## Griglia

```
Tarsilia — le stalle dell'Istrice (assalto notturno)
COLONNE:  A B C D E F G H I J K L M N O P Q R S T U
01 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫
02 🟫 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
03 🟫 🏰 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟫 🟫 🟫 🟫 🎯 🟫 🟫 🟫 🟫 🟫 🏰
04 🟫 🏰 🟨 🟨 🟨 🟨 ⚫ 🟨 🟨 🟨 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🪓 🟫 🏰
05 🟫 🏰 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🏰
06 🟫 🏰 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🚪
07 🟫 🏰 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🔥 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟫 🏰
08 🟫 🏰 🔴 🟨 🟨 🟨 🟨 🟨 🔵 🟨 🏮 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟨 🟫 🏰
09 🟫 🚪 🔴 🔴 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🟫 🏰
10 🟫 🏰 🟫 🔴 🟫 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🟫 🟫 🏰
11 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🏰
12 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟢 🟫 🏰 🟫 🟢 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🏰
13 🟫 🏰 🟫 🛢 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 📦 🟫 🏰
14 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🟫 🏰 🟫 🟫 🏰
15 🟫 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰

@north N
@mark 1 ; I8 ; Ombra (dorme in stalla) (druida 3)
@mark 2 ; H12 ; Il cavallo della contrada (animale GS 1)
@mark 3 ; L12 ; Regina, la mula (animale)
@mark 4 ; G4 ; Sfregio (ladro 4, GS 3)
@mark 5 ; C9 ; Bravaccio 1 (guerriero 1)
@mark 6 ; C8 ; Bravaccio 2 (guerriero 1)
@mark 7 ; D9 ; Bravaccio 3 (Pico) (guerriero 1)
@mark 8 ; D10 ; Bravaccio 4 (guerriero 1)
```

### 🌍 AMBIENTE (cosa impone il terreno — regole, non prosa)

| Elemento | Dove (coord.) | Effetto meccanico 3.5 |
|---|---|---|
| 🔥 Paglia (tutto il corridoio) | K7 | Se prende fuoco: 1d6/round a chi ci sta. Fumo in 3 round: Tempra CD 15 a round o soffocare, −2 a tutto |
| 🎯 BOTOLA DEL FIENILE (G4) | G4 | Da qui entra Sfregio mentre i bravacci fanno rumore alla porta sul canale. Percezione CD 20 per sentirlo |
| 🎯 FINESTRA ALTA (O3) | O3 | Via di fuga di Sfregio. Acrobazia CD 12 per uscirne senza rallentare |

### ⚔️ TATTICHE (come si comportano i nemici — round per round)

**Forze in campo** (astrazione per unità — un blocco = un'unità, non un token per creatura):

| Fazione | Unità | Token | Q.tà | GS/EL | Area (coord.) |
|---|---|---|---|---|---|
| Istrice | Ombra (dorme in stalla) | 🔵 | 1 | druida 3 | I8 |
| Cavalli | Il cavallo della contrada | 🟢 | 1 | animale GS 1 | H12 |
| Cavalli | Regina, la mula | 🟢 | 1 | animale | L12 |
| Assalitori | Sfregio | ⚫ | 1 | ladro 4, GS 3 | G4 |
| Assalitori | Bravaccio 1 | 🔴 | 1 | guerriero 1 | C9 |
| Assalitori | Bravaccio 2 | 🔴 | 1 | guerriero 1 | C8 |
| Assalitori | Bravaccio 3 (Pico) | 🔴 | 1 | guerriero 1 | D9 |
| Assalitori | Bravaccio 4 | 🔴 | 1 | guerriero 1 | D10 |

- **Disposizione iniziale**: [chi è dove e perché — vedi tabella Forze]
- **Round 1-2**: [reazione al contatto]
- **Round 3+**: [piano B, focus-fire, uso del terreno]
- **Morale**: [soglia di ripiegamento/resa]

### 🔄 EVOLUZIONE (come cambia la mappa — stati, non copione)

| Stato | Trigger | Cosa cambia sulla griglia | Effetto meccanico |
|---|---|---|---|
| A (iniziale) | — | com'è disegnata | — |
| B | [trigger] | Coordinate come nel testo del Giorno 2 §6: B9 porta sul canale, G4 botola del fienile, H12 box del cavallo, O3 finestra alta. | [effetto] |
| B | [trigger] | Obiettivo di Sfregio, in ordine: azzoppare il cavallo con la pasta corrosiva (1 round intero, cavallo fermo) → avvelenare l'abbeveratoio → portarsi via Nocca. | [effetto] |
| B | [trigger] | Se i PG preparano una trappola: iniziativa a loro, +2 CA a chi è in copertura preparata, e Sfregio perde l'attacco furtivo del primo round. | [effetto] |
| B | [trigger] | Sconfitta dei PG: nessuno viene finito. Gli assalitori prendono ciò per cui sono venuti e se ne vanno. | [effetto] |

> Gli stati sono **esiti aperti** (D13): il trigger è dei dadi e delle scelte dei PG, mai del copione.

