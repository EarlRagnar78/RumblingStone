# Serie Golarion — gli otto stemmi in versione Pathfinder

Variante **d'ambientazione** degli stemmi del Palio: stessi distretti, stesse figure, stesse
meccaniche. Cambiano **divinità patrona**, **livrea** e **simbolo divino** in campo.

> Le **regole restano D&D 3.5**. Questa serie non converte l'arco a Pathfinder 1e: converte
> solo il pantheon e l'araldica che ne discende. Per una conversione meccanica servirebbe un
> piano a sé (skill `pathfinder-1e-srd`).

Serve un aggancio già scritto nel canone del repo: `...P2D-PALIO-CHANNATHGATE-AVVENTURA.md`
§1 registra che le divinità faerûniane sono una **riconversione da Golarion**. Il pantheon
originale però **non era documentato da nessuna parte** — questa serie lo ricostruisce
partendo dal ruolo di ciascun distretto, non da un elenco perduto.

## Mappatura

| Distretto | Faerûn | Golarion | Perché |
|---|---|---|---|
| The Golden Plume | Waukeen | **Abadar** | Città, ricchezza, legge, mercanti. Corrispondenza quasi esatta. |
| The Iron Bastion | Torm · Tempus | **Iomedae · Gorum** | Onore e giustizia (Iomedae) + guerra (Gorum): la stessa coppia dovere/battaglia. |
| The Silver Weft | Mask | **Norgorber** | Segreti, furto, omicidio — ed è anche il dio del **veleno**, che giustifica il verde-veleno meglio dell'originale. |
| The Quill-Wood Refuge | Ilmater · Chauntea | **Sarenrae · Erastil** | Guarigione e redenzione (Sarenrae) + comunità (Erastil). |
| The Spell-Wyrm Spires | Mystra | **Nethys** | La magia. Corrispondenza esatta. |
| The Whispering Shadows | Shar | **Calistria** | Vendetta, inganno, spie: il mestiere reale del distretto. *(Vedi nota sotto.)* |
| The Gilded Horn | Sune · Milil | **Shelyn** | Bellezza, arte **e** musica in una divinità sola: copre entrambe. |
| The Tidal Crest | Valkur · Selûne | **Gozreh · Desna** | Mare e cielo (Gozreh) + luna, stelle e viaggio (Desna). Desna↔Selûne è quasi 1:1. |

### Nota sulla Civetta

Il candidato tonalmente più vicino a Shar sarebbe **Zon-Kuthon** — tenebra, perdita, invidia.
È stata scelta **Calistria** per due motivi: è funzionalmente esatta (il distretto vive di
spie, ricatto e vendetta politica, che sono il suo dominio), e del simbolo sacro di
Zon-Kuthon non si aveva certezza sufficiente per disegnarlo. **Se il DM preferisce
Zon-Kuthon**, va verificato il simbolo prima di sostituirlo: la livrea tornerebbe nera e
argento, molto vicina a quella faerûniana.

## Livree

| Distretto · Divinità | Livrea | Codici |
|---|---|---|
| The Golden Plume · Abadar | marmo e lapis, bordata d'oro brunito | `#ded3ba` `#22406e` `#8a6416` |
| The Iron Bastion · Gorum/Iomedae | ferro rugginoso e argento, bordata d'oro | `#5a4438` `#e4e9ec` `#dfa93b` |
| The Silver Weft · Norgorber | argento sericeo e nero-fumo, listata di verde-veleno | `#a9b2b8` `#23272b` `#74d98a` |
| The Quill-Wood Refuge · Sarenrae/Erastil | verde legnoferro e bruno di terra, bordata d'oro solare | `#2e4a34` `#7a5230` `#e0a83c` |
| The Spell-Wyrm Spires · Nethys | **partita di nero e d'argento**, listata di viola arcano | `#141418` `#e6e6e2` `#7b52c0` |
| The Whispering Shadows · Calistria | nero e giallo-vespa, listata d'argento freddo | `#101014` `#d9a521` `#aeb8c8` |
| The Gilded Horn · Shelyn | rosa di Shelyn e argento, con l'oro del corno | `#b8496e` `#d7dce2` `#dfa93b` |
| The Tidal Crest · Gozreh/Desna | verde-fiume e argento lunare, bordata di blu profondo, stellata | `#1d6b63` `#e2ecec` `#123a5c` |

## Simboli divini sostituiti

| Faerûn | Golarion |
|---|---|
| moneta di Waukeen | **chiave d'oro** di Abadar |
| guanto di Torm | **spada raggiante** di Iomedae |
| *(nessuno)* | **maschera nera** di Norgorber |
| catene spezzate, rosso Ilmater | catene sciolte nell'**oro solare** + **ankh** di Sarenrae |
| stella di Mystra | il **campo stesso** — partito di nero e d'argento, la dualità di Nethys |
| disco nero di Shar | **disco a fasce di vespa** di Calistria |
| *(nessuno)* | rosa di Shelyn nel campo |
| falce di Selûne | falce e **tre stelle** di Desna |

**Il Drago è il pezzo migliore della serie**: la faccia mezza nera e mezza bianca di Nethys
non è disegnata come emblema, è diventata **la partizione dello scudo**. Lo scudo aveva già
una divisione verticale, e qui quella divisione *significa* qualcosa.

## Licenza e IP

Le **figure** sono le stesse della serie faerûniana: icone game-icons.net in CC BY 3.0 —
attribuzione in `../CREDITS.md`, che vale anche per questa cartella.

> *Icons made by Lorc, Delapouite and Caro Asercion* — <https://game-icons.net> — CC BY 3.0

⚠️ **Nomi e simboli delle divinità di Golarion sono IP di Paizo Inc.** Il loro uso qui è
**non commerciale, da tavolo**, e ricade nel perimetro della *Community Use Policy* di Paizo.
Questa serie **non** rende commercializzabile l'arco: vedi `...P2D-PALIO-VERIFICA-LEGALE-IP.md`
§6 — il blocco assorbente resta l'IP Wizards of the Coast del resto della campagna
(Channathgate, Red Hand of Doom, PNG). Sostituire il pantheon **non** sostituisce quello.

## Come si rigenerano

```bash
python3 build_golarion_shields.py
```

Gli scudi Golarion **riusano le figure della serie faerûniana**: il `transform` e il `<path>`
di ogni icona sono estratti da `../NN-*.svg` invece di essere duplicati, quindi le due serie
non possono divergere sulle figure. Se cambi un'icona nella serie principale, **rigenera anche
questa**. Non modificare questi otto file a mano: la prossima rigenerazione cancella tutto.

Verifica dopo aver rigenerato:

```bash
cd .. && python3 tools/measure_shields.py check --wide
```

Il manuale completo della pipeline è in **`../PROCEDURA.md`**.
