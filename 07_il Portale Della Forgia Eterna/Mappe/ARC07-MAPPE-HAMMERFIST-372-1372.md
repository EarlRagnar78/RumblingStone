# ARC-07 · Hammerfist dall'alto in basso, nel 372 e nel 1372

## Le mappe del lotto D28: la fortezza, le sale sotto la montagna, i due tempi

> **A cosa serve.** Le stesse sale servono due volte. Nel **372** i PG le
> attraversano di notte (`DEF-4`, Scene 4-5 e 11-12). Nel **1372** sono il campo
> della **ritirata** dei difensori verso il Cuore della Montagna e poi della
> **riconquista** (`DEF-5`, ARC-08). Ogni griglia sotto la montagna ha quindi due
> stati, e la sezione M7-S dice come si passa da un livello all'altro.
>
> **Cosa è canone e cosa no.** Il 372 viene dal master (`DEF-4` Scena 5) e dalle
> decisioni del DM del 2026-10-08 (D44-D47 di
> [LETTORE-E-PLAYTESTER](../../plans/PIANO-LETTORE-E-PLAYTESTER.md)). Le
> misure delle stanze e gli stati del 1372, che nessun master descriveva, li ha
> decisi il DM lo stesso giorno con la **D48**.

| Decisione | Cosa fissa |
|---|---|
| **D44** | la postierla è nel muro sud, all'angolo sud-est, sotto la torre est |
| **D45** | tre fucine, una per livello: la fucina originale sul cortile, la fucina di Gunnvor al livello −1, la fucina grande sotto le gallerie |
| **D46** | il 372 è il nucleo della fortezza del 1372: fossato, cortile esterno, torri da 20 m e bastioni vengono dopo |
| **D47** | l'armeria è accanto alla fucina di Gunnvor |
| **D48** | il percorso del 1372 (ritirata e riconquista), le misure delle griglie; le rune di Zeth sono glifi di interdizione contro chi non è nano; i leoni di pietra sono vuoti |

---

## Le mappe, nei due tempi

| | Luogo | Livello | 372 (`DEF-4`) | 1372 (`DEF-5`, ARC-08) |
|---|---|---|---|---|
| **M7-A** | la fortezza, il campo, il bosco | superficie | [Atlante](ARC07-MAPPE-DEFINITIVO.md), strategica | la vista del 1372 è l'Atlante di Hammerfist, MAPPA 1 e 2A |
| **M7-B** | il cortile del duello | 0 | [Atlante](ARC07-MAPPE-DEFINITIVO.md), Scena 11 | H3-1, il cortile sfondato (`08_…/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`) |
| **M7-C** | la tenda del comando | campo | [M7-C](ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md), Scene 7-8 | — (il campo del 372 non esiste più) |
| **M7-D** | il corridoio della fucina: quartieri, cappella, alchimista, fucina di Gunnvor, armeria | −1 | [M7-D 372](hammerfist-372-1372/M7-D-livello-1-372.md), Scena 5 | [M7-D 1372](hammerfist-372-1372/M7-D-livello-1-1372.md) |
| **M7-E** | le gallerie di Zeth | −2 | [M7-E 372](hammerfist-372-1372/M7-E-gallerie-372.md), Scena 5 | [M7-E 1372](hammerfist-372-1372/M7-E-gallerie-1372.md), i passaggi antichi |
| **M7-F** | la fucina grande | −3 | [M7-F 372](hammerfist-372-1372/M7-F-fucina-grande-372.md), vista dall'affaccio | [M7-F 1372](hammerfist-372-1372/M7-F-fucina-grande-1372.md) |
| **CM-1** | il Cuore della Montagna | il più profondo | — | [Atlante](ARC07-MAPPE-DEFINITIVO.md), MAPPA 5 dell'Atlante di Hammerfist |

Le griglie M7-D, M7-E e M7-F si generano dai loro contratti JSON nella stessa
cartella (`compile_map_json.py`): si cambia il JSON e si ricompila, mai la
griglia a mano.

---

## MAPPA M7-S — Hammerfist in sezione, nord a sinistra

<!-- render: none -->
```
════════════════════════════════════════════════════════════════════════════════
 HAMMERFIST IN SEZIONE — non in scala · più si scende, più le sale sono ampie
════════════════════════════════════════════════════════════════════════════════
  NORD (la montagna)                                          SUD (il campo)
  ⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️
  ⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️ 🔔🗼          🗼▫
  ⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️⛰️ ║ CORTILE  ║  mura +4,5 m      ⛺⛺⛺⛺
   0  sala del consiglio ═══🚪══ ║  M7-B    ║🚪 porta (targa)   campo dell'orda
      (lunga quanto una strada)  ║ forgia · statua ║
  ────────────── 🪜 ──────────────────────────────────────────────────────────
  −1  quartieri · cappella · alchimista                         M7-D
      fucina di Gunnvor (21 × 12 m) · armeria
  ────────────── 🪜 sotto la fucina ──────────────────────────────────────────
  −2  le gallerie di Zeth: strette, puntellate                  M7-E
      ─ ─ l'affaccio sulla fucina grande ─ ─      ⇠ imbocco delle miniere
  ────────────── 🪜 ──────────────────────────────────────────────────────────
  −3  la FUCINA GRANDE (36 × 24 m, volta alta)                  M7-F
  ────────────── ⇣ le miniere profonde ──────────────────────────────────────
      1372: ponte sospeso (3Y) → incrocio silenzioso (3Z)
  ▼   IL CUORE DELLA MONTAGNA (100 × 80 m, soffitto 40 m)        CM-1
════════════════════════════════════════════════════════════════════════════════
 372: si scende dalla scala del livello 0 alla fucina di Gunnvor, da lì alle
      gallerie (Zeth), e dall'affaccio si vede la fucina grande.
 1372 (D48): la ritirata del Giorno 3 parte dal cortile per il tunnel dietro
      la statua del Re Antenato (H3-1), entra nelle gallerie di Zeth, scende alla
      fucina grande e per il ponte sospeso e l'incrocio arriva al Cuore. Gli
      orchi saccheggiano il livello −1 dal corridoio principale. La riconquista
      fa la strada al contrario, dal Cuore verso l'alto.
LEGENDA · ⛰️ roccia · 🔔 campane · 🗼 torri · ▫ postierla · 🚪 porte ·
🪜 scale fra i livelli · ⇣ discesa · ═ corridoio principale.
════════════════════════════════════════════════════════════════════════════════
```

- **Tipo**: sezione schematica, solo per il DM. Non è una griglia di
  combattimento: le griglie sono M7-B, M7-D, M7-E e M7-F.
- **I livelli**: le quote non sono scritte in nessun master, quindi la sezione
  dà l'ordine e non i metri. Le misure delle sale vengono dalle griglie.
- **Il 1372, in tre righe**: le rune che Zeth scrive col gesso nel 372 sono
  colore; nel 1372 sono le difese del Ghostlord (D30), accese nelle gallerie:
  **glifi di interdizione** dell'SRD legati alla razza, che esplodono su chi non
  è nano (4d8, Riflessi CD 14 dimezza, come una pergamena al 9° livello
  dell'incantatore; Cercare e Disattivare Congegni CD 28; D48). Nella ritirata
  colpiscono gli orchi inseguitori, nella riconquista anche i PG che non sono
  nani. I leoni di pietra della sua promessa (*«proteggeranno queste gallerie
  per sempre»*) stanno in due nicchie e sono **vuoti**: gli spiriti sono andati
  con Zeth, e in ARC-09 sono i leoni spettrali del Ghostlord. L'armeria del 1372
  è il banco nanico di ARC-08 B4.
