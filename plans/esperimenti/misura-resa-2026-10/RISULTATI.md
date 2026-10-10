# La resa delle mappe misurata — prima e dopo la taratura (2026-10-09)

Esperimento di R8 di [PIANO-RESA-E-ASSET-DELLE-MAPPE](../../PIANO-RESA-E-ASSET-DELLE-MAPPE.md),
decisioni D23-D26, [ADR-0086](../../adr/ADR-0086-una-sostituzione-nella-resa-entra-solo-se-misurata-e-preferita.md).
Le misure si rifanno con:

```bash
python3 scripts/misura_resa.py glifi -o glifi.json
python3 scripts/misura_resa.py terreni -o terreni.json
python3 scripts/misura_resa.py tara -o taratura.json
```

## 1 · Cosa misurava il repo prima

Nessun algoritmo misurava l'estetica delle mappe. Quelli che giravano da soli:

| Strumento | Cosa controlla | Cosa non vede |
|---|---|---|
| `validate_maps.py` | l'SVG è identico al byte a quello che il renderer produce dal master | se la resa è buona |
| `build_texture_cc0 --check`, `build_oggetti_cc0 --check`, `build_emoji_noto --check`, `build_font_mappe --check` | impronte e licenze delle risorse | come stanno sulla mappa |
| `collaudo_mappe.py` | se la mappa si gioca (porte nel muro, scale gemelle, linea di vista) | come si legge |
| `build_oggetti_cc0 --misura-stile` | luminanza, saturazione, dettaglio di una tessera da sola | il confronto col glifo e col terreno |

## 2 · Come si misura un'icona su una mappa

La prima versione ricavava la figura dalla differenza fra la cella e la stessa
cella senza il simbolo. Così la figura comprendeva ombra e alone, e l'alone
risultava **peggiorativo**: il contrasto finiva misurato contro il terreno
sotto l'alone, e il bordo diventava quello sfumato dell'alone. La versione
buona rende a parte le sole figure (i `<use>` dei glifi e delle tessere) su
fondo trasparente, e da lì prende la maschera:

- **contrasto**: il decimo più scuro o più chiaro della figura contro la corona
  di tre pixel di cella intorno, nell'immagine finale (WCAG 2.1 §1.4.11: 3:1
  per la parte grafica che serve a riconoscere un oggetto). Un glifo si legge
  per il contorno a inchiostro, non per la tinta media;
- **bordo**: gradiente di Sobel medio sul contorno della figura;
- **somiglianza col vicino**: SSIM (Wang et al. 2004) fra due celle a 28 px;
- **tavolozza**: ΔE CIEDE2000 medio dai 16 colori della casa (k-means sui glifi
  della pergamena).

## 3 · I glifi: la #227 contro la pergamena, e la correzione

Mediane sui 61 simboli-oggetto, contrasto del contorno e bordo:

| Tema | Interni: contrasto · bordo · sotto 3:1 | Esterno: contrasto · bordo · sotto 3:1 |
|---|---|---|
| pergamena | 7,90 · 0,362 · 5 | 6,90 · 0,332 · 10 |
| texture, come nella #227 | **4,46** · 0,244 · **17** | **4,67** · 0,254 · **17** |
| texture, alone 0,35 | 5,97 · 0,303 · 11 | 6,12 · 0,309 · 10 |
| texture, alone 0,55 | 6,85 · 0,331 · 9 | 6,98 · 0,336 · 8 |
| **texture, alone 0,75 (tarato)** | **7,78 · 0,365 · 6** | **7,88 · 0,369 · 6** |

Con l'alone a 0,75 il tema texture torna al livello della pergamena negli
interni (−1,5% di contrasto, dentro la tolleranza) e la supera all'esterno. La
somiglianza col simbolo più vicino sale un poco (da 0,76 a 0,82 nel caso
peggiore), perché l'alone è uguale per tutti; resta pari alla pergamena (0,82).

Le coppie che si confondono di più, in tutti i temi: 🪟 finestra e 🧱 muretto
(SSIM 0,76-0,82), 🚪 porta e 🔒 porta chiusa (0,76-0,78), 🌾 erba alta e ❄
ghiaccio (0,77-0,80). Sono un difetto dei glifi della pergamena, non del tema:
vanno in V3 di COLLAUDO-MAPPE con R7.

## 4 · I terreni

ΔE CIEDE2000 di ogni terreno dal più vicino, prima della taratura (sotto 2,3
l'occhio non separa due colori):

| Terreno | Pergamena | Texture (#227) |
|---|---:|---:|
| ⛰ creste | 4,12 (🟤) | **1,22** (🔳) |
| 🔳 pedana | 7,79 (⬜) | **1,22** (⛰) |
| 🟤 caverna | 4,12 (⛰) | **1,97** (🔳) |
| ⬛ edificio | 12,54 (⛰) | 3,46 (🔳) |
| ⬜ pavimento | 6,70 (🟨) | 10,20 (🟩) |
| 🟫 terra | 7,29 (🟤) | 10,69 (🟨) |

Il contrasto del segnalino 🔴 sul pavimento ⬜ scendeva da 1,89 a 1,07; con
l'alone, che sta anche sotto i segnalini, il segnalino si stacca come i glifi.

**La taratura delle velature**, due giri:

| Giro | Velature scelte | ⛰ | 🔳 | ⬛ | 🟤 | Esito |
|---|---|---:|---:|---:|---:|---|
| primo: sale finché manca il bersaglio | ⛰ 0,80 · ⬛ 0,80 · 🔳 0,70 · 🟤 0,80 | 1,31 | 5,30 | 8,63 | 1,31 | ⬛ e 🔳 si separano, ⛰/🟤 no; la foto su quattro terreni è quasi coperta |
| **secondo: sale solo se la distanza cresce** | ⛰ 0,35 · 🔳 0,40 · 🟨 0,40 | 1,48 | 1,48 | 2,29 | 4,11 | committato; quattro coppie da cambiare: ⛰/⬛, ⛰/🔳, ⛰/🟤, ⬛/🔳 |

La velatura non basta perché le texture di roccia di ⛰, 🔳 e 🟤 hanno la stessa
tonalità: la velatura le porta verso la tinta di pergamena, che per ⛰ e 🟤 è
già vicina (ΔE 4,1). Servono texture di tonalità diversa (D27): tre candidati
per terreno in `build_texture_cc0.CANDIDATI`, scelti da `tara --candidati`.

**Il peso**: i 53 SVG del tema texture passano da 7,59 a 8,44 MB (+0,85),
soprattutto per l'alone, un cerchio sfumato sotto ogni oggetto.

**Il cancello**: `misura_resa.py --check` misura 244 combinazioni di simbolo,
tema e terreno e 20 di terreno e tema in circa un minuto e mezzo.

## 5 · Cosa resta al DM

- Il confronto alla cieca (livello C) delle tessere vere: CC0 e ComfyUI.
- Il livello B sulla sua macchina, come secondo parere.
- Le coppie di terreni che la velatura non separa: servono texture diverse,
  e scaricarle è suo (la rete dell'ambiente non raggiunge Poly Haven):
  `build_texture_cc0.py --candidati`, poi `misura_resa.py tara --candidati
  asset-esterni/texture-candidate`.
