# Crediti — figure degli stemmi del Palio di Channathgate

Le **figure araldiche** degli otto stemmi (`01-oca.svg` … `08-onda.svg`) usano icone di
**[game-icons.net](https://game-icons.net)**, ricolorate nelle livree di Channathgate e
inserite negli scudi originali della campagna.

> **Icons made by Lorc, Delapouite and Caro Asercion** — <https://game-icons.net> — CC BY 3.0

## Licenza

I file di licenza forniti insieme alle icone sono in questa stessa cartella:

- `game-icons/license.txt` — dichiara le icone **CC BY 3.0** (alcuni autori CC0) e chiede
  espressamente di *«include a mention "Icons made by {author}" in your derivative work»*;
- `game-icons/license-svg.txt` — rimanda a <https://creativecommons.org/licenses/by/4.0/deed.en>.

Entrambe le versioni della licenza richiedono **solo l'attribuzione**: l'uso è consentito
anche in opere derivate, modificate e commerciali. Le icone sono state **modificate**
(ricolorate, scalate e ritagliate dal riquadro nero originale); questa pagina assolve
l'obbligo di attribuzione e di indicazione delle modifiche.

## Icona per icona

| Stemma | Distretto | Icona | Autore |
|---|---|---|---|
| `01-oca.svg` | The Golden Plume | `goose` | Delapouite |
| `02-torre.svg` | The Iron Bastion | `white-tower` | Lorc |
| `03-bruco.svg` | The Silver Weft | `caterpillar` | Delapouite |
| `04-istrice.svg` | The Quill-Wood Refuge | `porcupine` | Caro Asercion |
| `05-drago.svg` | The Spell-Wyrm Spires | `spiked-dragon-head` | Delapouite |
| `06-civetta.svg` | The Whispering Shadows | `barn-owl` | Caro Asercion |
| `07-unicorno.svg` | The Gilded Horn | `unicorn` | Delapouite |
| `08-onda.svg` | The Tidal Crest | `big-wave` | Lorc |

**Non utilizzata**: `game-icons/stone-tower-lorc.svg` (Lorc) — variante alternativa per la
Torre, tenuta in archivio. Per usarla, sostituire il `<path>` dentro il blocco `FIGURA` di
`02-torre.svg`.

**Serie Golarion**: `golarion/` riusa **le stesse otto icone** con livree e simboli divini di
Pathfinder. Questa attribuzione copre anche quella cartella. Attenzione: nomi e simboli delle
divinità di Golarion sono **IP di Paizo Inc.** — vedi `golarion/README.md`.

## Cosa NON viene da game-icons

Sono **originali della campagna** e non coperti da questa attribuzione: la sagoma dello
scudo, le livree e i loro codici colore, i cartigli dei motti, e i simboli faerûniani
sovrapposti — moneta di Waukeen, guanto di Torm, stella di Mystra, disco di Shar, falce di
Selûne, catene spezzate dell'Istrice, corno dorato dell'Unicorno.

## Come sostituire una figura

In ogni SVG la figura vive fra i marcatori `<!-- FIGURA … -->` e `<!-- /FIGURA -->`. Il
gruppo esterno porta il `fill` della livrea, quindi **il `<path>` sostituito eredita il
colore giusto**: basta rimpiazzare il path e ricalcolare il `transform` (le icone
game-icons hanno `viewBox="0 0 512 512"`; il riquadro di fondo `M0 0h512v512H0z` va scartato).
