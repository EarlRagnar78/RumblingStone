# Come sono fatti gli stemmi, e come si rifanno

Questa cartella contiene **16 scudi**: otto per Faerûn (`NN-*.svg`) e otto per Golarion
(`golarion/NN-*.svg`). Questo documento è il manuale di manutenzione — cosa toccare, cosa
non toccare, e come verificare invece di sperare.

| File | Cosa fa |
|---|---|
| `NN-*.svg` | i **sorgenti** della serie faerûniana: si modificano a mano |
| `golarion/NN-*.svg` | **generati** da `golarion/build_golarion_shields.py` — non modificare a mano |
| `golarion/build_golarion_shields.py` | genera la serie Golarion riusando le figure di quella faerûniana |
| `tools/build_armorial.py` | pagina autoportante coi 16 scudi affiancati |
| `tools/measure_shields.py` | misura con un vero motore di rendering: verifica testi e bbox delle icone |
| `game-icons/` | icone sorgente + i due testi di licenza |
| `CREDITS.md` | attribuzione CC BY 3.0 e contratto del cartiglio |

---

## 1 · Anatomia di uno scudo

Tela `200×240`. La sagoma è sempre la stessa:

```
M20 20 H180 V150 Q180 210 100 232 Q20 210 20 150 Z
```

Con `stroke-width="6"` centrato sul tracciato, il filo esterno del bordo va da **x=17 a
x=183**. È da lì che viene la larghezza del cartiglio.

Ordine di disegno, dal fondo alla superficie:

1. **campo** — la sagoma riempita col colore della livrea, con il bordo
2. **mezzo campo destro** — `M100 20 H180 V150 Q180 210 100 232 Z`, un tono più scuro; dà
   profondità e, sul Drago di Golarion, *diventa* il simbolo di Nethys
3. **elementi sotto la figura** — bande d'onda, campagna di terra, disco di Shar, banda di seta
4. **`<!-- FIGURA -->` … `<!-- /FIGURA -->`** — l'icona game-icons (vedi §3)
5. **elementi sopra la figura** — simboli divini, catene, corno dorato, muratura
6. **bordo ridisegnato** senza riempimento, così copre tutto ciò che sborda
7. **cartiglio del motto** e **titolo**

I passaggi 3-5 stanno dentro `<g clip-path="url(#…)">`: tutto ciò che eccede la sagoma
viene ritagliato. Il cartiglio del motto sta **fuori** dal clip, per questo attraversa lo
scudo da parte a parte.

---

## 2 · Le livree

Ogni livrea deriva dalla **divinità patrona** e dal **nome del distretto**, mai dalla
contrada senese di partenza — è il vincolo che tiene chiusa la criticità §3.2 del documento
di verifica IP. Le palette canoniche stanno in `...P2D-PALIO-CONTRADE-STEMMI-CANTI.md`
§Livree (Faerûn) e in `golarion/README.md` (Golarion).

Se cambi una livrea, aggiorna **entrambi**: l'SVG e la tabella nel master. Sono due fonti
che devono restare d'accordo, e nessuno script lo verifica.

---

## 3 · Inserire o sostituire una figura

Le icone game-icons sono `viewBox="0 0 512 512"` e contengono **due** path: un riquadro nero
di fondo `M0 0h512v512H0z` da **scartare**, e il glyph vero.

**Passo 1 — misura il glyph.** Il `viewBox` non dice dove sta davvero il disegno:

```bash
python3 tools/measure_shields.py bbox 'game-icons/goose-Delapouite.svg'
# goose-Delapouite.svg    x=35.7  y=18  w=440.5  h=476
```

**Passo 2 — calcola scala e posizione.** Dato un riquadro d'arrivo `(cx, cy, maxw, maxh)`
in coordinate scudo:

```
s  = min(maxw/w, maxh/h)
tx = cx - (x + w/2) * s
ty = cy - (y + h/2) * s
```

**Passo 3 — incastonala.** Il gruppo esterno porta il `fill` della livrea, quindi il path
**eredita il colore giusto** e non va toccato:

```xml
<!-- FIGURA · game-icons.net "goose-Delapouite" di Delapouite, CC BY 3.0 -->
<g fill="#f0eada"><g transform="translate(39.78 39.76) scale(0.23529)"><path d="…"/></g></g>
<!-- /FIGURA -->
```

I riquadri usati stanno tipicamente fra `cx=96..100`, `cy=90..104`, `maxw=108..124`,
`maxh=90..112`. Un riquadro più grande fa uscire la figura dal campo utile.

**Passo 4 — guardala.** Le collisioni non si trovano leggendo l'XML. Quattro difetti reali
sono usciti solo al primo render: il bruco invisibile perché dello stesso colore della banda
sotto, la stella di Mystra impastata nella mascella del drago, la falce di Selûne sepolta
sotto il cavallone, la civetta che sbordava sul cartiglio.

---

## 4 · Dorare una parte di una figura

Le icone sono **glyph a path unico**: becco, zampe, faccia non sono elementi separati e non
si possono colorare da soli. La tecnica è **una copia dorata dello stesso path, ritagliata**:

```xml
<defs><clipPath id="g1-or">
  <rect x="406" y="84" width="92" height="74"/>     <!-- becco -->
  <rect x="188" y="450" width="234" height="62"/>   <!-- zampe -->
</clipPath></defs>
…
<g transform="translate(39.78 39.76) scale(0.23529)">
  <path d="…" fill="#f0eada"/>
  <g clip-path="url(#g1-or)"><path d="…" fill="#dfa93b"/></g>
</g>
```

Le coordinate del `clipPath` sono in **spazio icona** (0..512), perché il gruppo che lo
riferisce è dentro la `transform`. Vantaggio: registrazione esatta, e regge se l'icona viene
riscalata.

La **muratura della Torre** usa lo stesso principio al contrario: un reticolo di corsi a
giunti sfalsati ritagliato *sulla sagoma della torre*, usando **il glyph stesso** come
`clipPath`. Segue profilo e rastremazione senza una riga di geometria in più.

> Regola araldica del *masoned*: i giunti vanno in un tono **più scuro del metallo della
> torre**, non in un colore nuovo. Per questo sono `#8d9aa6` sull'argento `#dce3e8`.

---

## 5 · Cartiglio e testi — il contratto

Su tutti e 16: `<rect x="17" y="182" width="166" height="26" rx="4">`. Da filo a filo del
bordo esterno, simmetrico. **Non cambiarlo su un singolo scudo**: l'uniformità è il punto.

Motto e titolo portano `textLength` + `lengthAdjust="spacingAndGlyphs"`. Il renderer è
obbligato a stare dentro quella misura **con qualunque font**. Serve perché `Georgia` spesso
non è installata e i ripieghi sono più larghi: senza il vincolo il motto usciva dal cartiglio
e finiva illeggibile sul campo.

⚠️ **Se cambi il testo di un motto o di un titolo devi ricalcolarne il `textLength`.**
Lasciare il valore vecchio con un testo più lungo lo comprime, con uno più corto lo stira.
Per ricalcolarlo: togli l'attributo, lancia `tools/measure_shields.py check`, leggi la
larghezza naturale, rimettila. Massimi utili: **150** per il motto, **176** per il titolo.

Il **titolo** sopra lo scudo non ha alcun fondo: sta sulla pergamena nuda. È una scelta, non
una dimenticanza — ma vuol dire che su un fondo scuro sparisce. Per questo l'armoriale monta
gli scudi su pergamena anche in tema scuro.

---

## 6 · La serie Golarion

Non si modifica a mano. È **generata** dalla serie faerûniana:

```bash
python3 golarion/build_golarion_shields.py
```

Lo script estrae `transform` e `<path>` delle icone da `../NN-*.svg` invece di duplicarli:
le due serie **non possono divergere sulle figure**. Cambia solo livrea, simboli divini e
titoli, che sono nella tabella in testa allo script.

**Se cambi un'icona nella serie faerûniana, rigenera anche questa**, altrimenti le due serie
si disallineano.

---

## 7 · Verifica prima di consegnare

```bash
# i testi stanno dentro, col font di sistema e con uno molto più largo
python3 tools/measure_shields.py check
python3 tools/measure_shields.py check --wide

# l'XML è valido
python3 -c "import xml.etree.ElementTree as ET,glob; [ET.parse(f) for f in glob.glob('*.svg')+glob.glob('golarion/*.svg')]; print('ok')"

# guardali davvero, in entrambi i temi
python3 tools/build_armorial.py /tmp/armoriale.html
```

Poi rigenera il booklet, che incorpora gli SVG inline:

```bash
cd ../../homebrew && python3 ../../scripts/build_booklet_html.py PALIO-BOOKLET.manifest.json --format both
```

> Il booklet mette **tutti** gli SVG in **un'unica pagina HTML**. Per questo negli scudi non
> si usano né `<style>` né `class`: collidono fra file. Gli `id` dei `clipPath` sono unici
> per scudo (`g1`, `t2`, `b3`, …, `ga1`, `gt2`, …) proprio per questo.

---

## 8 · Cosa non è nostro

Le **figure** sono icone game-icons.net in **CC BY 3.0** — attribuzione obbligatoria in
`CREDITS.md`. I **nomi e simboli delle divinità di Golarion** sono **IP di Paizo Inc.**, uso
non commerciale nel perimetro della Community Use Policy (vedi `golarion/README.md`).

Sagoma, livree, cartigli e simboli faerûniani sono originali della campagna.
