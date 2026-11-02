// Pacchetti vendorizzati (ADR-0026): stanno in `scripts/typst/packages/` e la
// compilazione non scarica niente. `droplet` fa il capolettera annegato,
// `in-dexter` l'indice analitico.
#import "@preview/droplet:0.3.1": dropcap
#import "@preview/in-dexter:0.7.2": index, make-index

// tema-rumblingstone.typ — il tema di stampa del repo (ADR-0020).
//
// Lo usa scripts/export_booklet_typst.py: NON si modifica il .typ generato,
// si modifica questo. Il contenuto arriva dai master markdown (ADR-0003).
// Impaginazione da manuale: due colonne, carta avorio, capolettera, fregi,
// box read-aloud, tabelle a righe alternate, indice cliccabile.
//
// I font sono in `scripts/fonts/` — EB Garamond, Cinzel e Inconsolata, tutti
// OFL, tutti embeddati. Nessun font di sistema: è il motivo per cui esiste
// questa catena (ADR-0020 §Attuazione).

#let avorio    = rgb("#f6efe0")
#let inchiostro = rgb("#241d16")
#let seppia    = rgb("#6b4f2a")
#let rosso     = rgb("#7d2b1f")
#let boxLeggi  = rgb("#ece0c6")
#let boxLato   = rgb("#efe6d2")

#let SERIF = "EB Garamond"
#let TITOLI = "Cinzel"
#let MONO = "Inconsolata"

// Apertura di capitolo: il medaglione + il titolo, su tutta la larghezza delle
// due colonne. È il segno che dice al lettore dov'è prima che legga il titolo.
#let capitolo-aperto(titolo, fregio) = {
  // Un capitolo si apre su una pagina sua. Il titolo è un float in cima alla
  // pagina: se il capitolo di prima finiva a metà pagina, il titolo nuovo
  // saliva SOPRA la coda di quello (volume del −1000, 2026-09-25: le note del
  // carry-over B4 stampate sotto il titolo delle Cronache).
  pagebreak(weak: true)
  // L'heading (voce d'indice + segnalibro PDF) va emesso PRIMA del float:
  // altrimenti la testatina della pagina d'apertura mostra ancora il capitolo
  // precedente, perché la query si risolve prima che il float atterri.
  hide(heading(level: 1, titolo))
  place(top, float: true, scope: "parent", clearance: 14pt)[
    #block(width: 100%, above: 0pt)[
      #line(length: 100%, stroke: 0.6pt + seppia)
      #v(7pt)
      #grid(columns: (1.5cm, 1fr), column-gutter: 10pt, align: horizon,
        if fregio != none { image(fregio, width: 1.5cm) } else { [] },
        text(font: TITOLI, size: 17pt, weight: 600, fill: rosso)[#titolo])
      #v(5pt)
      #line(length: 100%, stroke: 0.6pt + seppia)
    ]
  ]
}

// Typst non ha un «content → string» nativo: serve per leggere il «§N» dai titoli.
#let to-string(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(to-string).join("") }
  else if c.has("body") { to-string(c.body) }
  else if c == [ ] { " " }
  else { "" }
}

// Una figura: se è più larga che alta scavalca le due colonne (le tavole
// d'ambiente), se è verticale sta in colonna (i ritratti). La didascalia è
// l'alt del markdown.
#let figura(percorso, alt, larga: false) = {
  let corpo = block(breakable: false, width: 100%)[
    #image(percorso, width: 100%)
    #v(2pt)
    #text(size: 8pt, style: "italic", fill: seppia)[#alt]
  ]
  if larga { place(top, float: true, scope: "parent", clearance: 12pt, corpo) }
  else { corpo }
}

#let fregio() = align(center)[
  #v(0.3em)
  #text(fill: seppia, size: 11pt)[❦]
  #v(0.3em)
]

// Segno di fine voce: il rombo che i manuali mettono in coda a una sezione per
// dire «questa voce finisce qui» senza spendere una riga bianca.
#let fine = box(baseline: 0%)[#h(0.35em)#text(fill: seppia, size: 8pt)[⬦]]

// Le varianti di impaginazione da provare alla cieca (piano dello standard di
// stampa, I6). Arrivano da `typst compile --input chiave=valore`, cioè da
// `scripts/varianti_stampa.py`; senza --input il libro è quello di sempre.
#let VARIANTE = (
  // l'interlinea del testo, come `leading` di Typst: 0.62em dà 1,30 volte il corpo
  interlinea: sys.inputs.at("interlinea", default: "0.62em"),
  // «riquadro»: il box sul fondo colorato; «colore»: corsivo colorato nel testo,
  // senza riquadro, come fanno WotC e Paizo
  leggi: sys.inputs.at("leggi", default: "riquadro"),
)
#let inchiostroLeggi = rgb("#5b3417")

// Read-aloud: il testo che si legge ad alta voce al tavolo.
// Il segnaposto <leggi> dice in che pagine stanno i box (scripts/varianti_stampa.py).
#let leggi(body) = [#metadata("leggi") <leggi>] + if VARIANTE.leggi == "colore" {
  block(width: 100%, inset: (left: 0.6em), above: 0.9em, below: 0.9em, breakable: true,
    text(style: "italic", size: 9.8pt, fill: inchiostroLeggi)[#body])
} else {
  block(
    width: 100%, fill: boxLeggi, inset: (x: 9pt, y: 8pt), radius: 2pt,
    stroke: (left: 2pt + seppia),
    breakable: true,
  )[#text(style: "italic", size: 9.4pt, fill: inchiostro)[#body]]
}

// Nota di regia per il DM.
#let nota(body) = block(
  width: 100%, inset: (x: 8pt, y: 6pt),
  stroke: (left: 1.5pt + rgb("#b9a789")),
  breakable: true,
)[#text(size: 9pt, fill: rgb("#4a3f33"))[#body]]

// Riquadro laterale: la regola opzionale, la nota d'ambientazione, la variante.
// È il terzo caso che mancava — `leggi` è per i giocatori, `nota` è per la
// regia, questo è per il regolamento che si può anche non usare.
#let riquadro(titolo: "", body) = block(
  width: 100%, fill: boxLato, inset: (x: 9pt, y: 8pt), radius: 2pt,
  stroke: 0.6pt + seppia.lighten(30%),
  breakable: true,
)[
  #if titolo != "" [
    #text(font: TITOLI, size: 9.5pt, weight: 600, fill: rosso, tracking: 0.4pt)[#upper(titolo)]
    #v(3pt)
    #line(length: 100%, stroke: 0.4pt + seppia.lighten(40%))
    #v(3pt)
  ]
  #text(size: 9pt)[#body]
]

// Capolettera ANNEGATO: la maiuscola d'apertura scende dentro il paragrafo e il
// testo le scorre attorno, come nei manuali.
//
// Il commento che stava qui diceva: «se un giorno si vuole l'annegato, si apre
// un ADR sul vendoring dei pacchetti Typst». Quell'ADR ora esiste — ADR-0026 —
// e `droplet` è vendorizzato in `scripts/typst/packages/`, con la sua licenza
// MIT, quindi il ripiego è scaduto e questa è la cosa vera.
//
// ⚠️ Il versale resta, come `capolettera-versale`, e non per nostalgia: un
// capolettera annegato ha bisogno di **almeno tre righe** di paragrafo sotto di
// sé, altrimenti la lettera esce dal blocco e si porta dietro il testo. Chi
// chiama decide; il ripiego è scritto, non implicito.
// L'indice analitico: le voci marcate nel testo, raccolte in coda al volume con
// il numero di pagina. Lo fa `in-dexter` (ADR-0026), che è vendorizzato.
//
// ⚠️ Le voci NON si annotano a mano: le marca l'esportatore prendendo i nomi
// canonici dal glossario (`campaign/GLOSSARIO-E-LOCALIZZAZIONE.md`). Chiedere a
// chi scrive di marcare a mano ogni ricorrenza è il modo in cui un indice
// analitico resta vuoto per sempre.
#let voce-indice(termine) = index(termine)

#let indice-analitico(colonne: 2) = page(columns: colonne, header: none)[
  #place(top + center, scope: "parent", float: true,
    block(width: 100%, inset: (bottom: 8pt))[
      #align(center)[
        #text(font: TITOLI, size: 13pt, fill: rosso, tracking: 1.2pt)[INDICE ANALITICO]
        #v(2pt)
        #line(length: 38%, stroke: 0.6pt + seppia)
      ]
    ])
  #set text(size: 8.6pt)
  // ⚠️ `section-title` va passato. Il default di in-dexter e' un `heading`, e i
  // nostri `show heading` lo impaginano come un titolo di sezione del volume:
  // la lettera finiva sulla STESSA riga della prima voce, e sembrava ripetuta
  // («C Colpo dell'Alba Oscura»). Qui e' un blocco suo, con l'aria che deve
  // avere: una lettera capitale, sola, sopra il suo gruppo.
  #make-index(
    title: none,
    use-page-counter: true,
    section-title: (lettera, _) => block(above: 9pt, below: 3pt, breakable: false)[
      #text(font: TITOLI, size: 10.5pt, weight: 600, fill: rosso, tracking: 1pt)[#lettera]
      #v(-3pt)
      #line(length: 100%, stroke: 0.4pt + seppia.lighten(35%))
    ],
  )
]

#let capolettera-versale(lettera, corpo) = {
  set par(first-line-indent: 0pt)
  par[#box(baseline: 25%)[
      #text(font: TITOLI, size: 2.6em, weight: 600, fill: rosso)[#lettera]
    ]#h(0.05em)#corpo]
}

#let capolettera(lettera, corpo) = {
  set par(first-line-indent: 0pt)
  dropcap(
    height: 3,
    gap: 6pt,
    hanging-indent: 0pt,
    font: TITOLI,
    weight: 600,
    fill: rosso,
    [#lettera#corpo],
  )
}

// Una figura. In due colonne un'immagine più larga della colonna va in float a
// piena larghezza, esattamente come le tabelle larghe: dentro la colonna
// verrebbe scalata fino a non vedersi più.
#let figura(percorso, didascalia: none, larga: false, pagina: false, alt: none) = {
  // `pagina`: l'immagine sta su un foglio a una colonna (appendici, mappe) e
  // non deve superarne l'altezza, didascalia compresa.
  // Fuori da una pagina dedicata, un'immagine non supera i 16 cm: un ritratto
  // verticale a tutta larghezza su una colonna sola è più alto del foglio,
  // scivola alla pagina dopo e lascia il suo titolo da solo in fondo a quella
  // prima (la scheda di Hella nel fascicolo dei giocatori, 2026-09-25).
  // Il tetto si applica misurando, mai con un'altezza fissa adattata a
  // «contain»: la cornice sarebbe alta 21 cm anche per una mappa da 16, e
  // la coda della pagina scivolerebbe alla successiva (il Palio, 2026-09-25:
  // una riga sola a pagina 4, un fregio solo a pagina 62).
  let tetto = if pagina { 21cm } else { 16cm }
  let corpo = figure(
    layout(spazio => {
      let alta = measure(image(percorso, width: spazio.width)).height
      if alta > tetto { align(center, image(percorso, height: tetto, alt: alt)) }
      else { image(percorso, width: 100%, alt: alt) }
    }),
    caption: if didascalia == none { none } else {
      text(size: 8.4pt, style: "italic", fill: seppia)[#didascalia]
    },
    supplement: none,
    numbering: none,
  )
  if larga { place(top, float: true, scope: "parent", clearance: 12pt, block(width: 100%, corpo)) }
  else { block(width: 100%, above: 0.8em, below: 0.8em, corpo) }
}

// Una griglia a spaziatura fissa (mappa ASCII, schema, statblocco
// preformattato) non va mai a capo: una mappa che va a capo è una fila di
// simboli. Se è più larga dello spazio, il corpo scende finché ci sta, non
// sotto i 5,5 pt. Che la griglia stia in colonna o su una pagina A4 lo decide
// l'esportatore (`CELLE_COLONNA`); qui si garantisce solo che non si spezzi.
// `larga`: uno schema che non è una mappa e non entra in colonna nemmeno a
// 5,5 pt scavalca le due colonne, come una tabella larga.
#let griglia(testo, corpo: 9pt, minimo: 5.5pt, larga: false) = {
  let dentro = layout(spazio => {
    let fatto(dim) = { show raw: set text(size: dim); raw(testo, block: true) }
    let naturale = measure(fatto(corpo)).width
    let dim = if naturale > spazio.width {
      calc.max(minimo, corpo * (spazio.width / naturale) * 0.98)
    } else { corpo }
    block(breakable: not larga, width: 100%, fatto(dim))
  })
  if larga { place(top, float: true, scope: "parent", clearance: 12pt, dentro) }
  else { dentro }
}

// Una tabella che in una colonna da 8 cm va a capo in ogni cella non si legge:
// si spezzano perfino le parole del titolo. Allora scavalca le due colonne, in
// cima o in fondo alla pagina dove è citata (`auto`), che è quello che fa un
// manuale stampato. Nel punto esatto non si può: Typst 0.15 non bilancia le
// colonne, e un blocco a due colonne interrotto a metà pagina riempie solo
// quella di sinistra (provato il 2026-09-25).
//
// Chi decide:
// - `larga: true` / `false`: l'autore, con `<!-- tabella: larga -->` o
//   `<!-- tabella: colonna -->` sopra la tabella nel master;
// - `auto`: la misura. Da quattro colonne in su scavalca sempre; sotto,
//   scavalca se in colonna diventa più alta di `TABELLA-SOGLIA` volte quanto
//   sarebbe a tutta pagina. Misurato sui tre volumi della #169: 125 tabelle in
//   colonna, e 100 erano alte il doppio o quasi, cioè andavano a capo in ogni
//   cella.
// - una tabella da due o tre colonne più alta di `TABELLA-FLOAT-MAX` a tutta
//   pagina resta in colonna, dove scorre: un float non si spezza. Da quattro
//   colonne in su scavalca comunque, perché in colonna le celle si
//   sovrappongono (l'Abbazia, pagina 26, provato il 2026-09-25); oltre le 30
//   righe l'esportatore la manda su una pagina A4.
// `pagina`: la tabella sta già su un foglio a una colonna, e lì non scavalca
// niente (l'indice delle 48 aree dell'Abbazia si stampava sopra se stesso).
#let TABELLA-SOGLIA = 1.8
#let TABELLA-FLOAT-MAX = 20cm
#let TABELLA-COLONNA = 8.1cm
#let TABELLA-PAGINA = 17.5cm
// `sezione`: il titolo della sezione in cui la tabella è citata. Un float sale
// in cima alla pagina e può finire sopra il suo titolo, o nella pagina dopo;
// scavalcando porta con sé una riga che dice a quale sezione appartiene.
#let tabella(n, pagina: false, larga: auto, sezione: none, ..celle) = {
  let griglia = table(
    columns: n,
    stroke: none,
    inset: (x: 6pt, y: 4.5pt),
    fill: (_, row) => if row == 0 { seppia.lighten(60%) }
                      else if calc.odd(row) { boxLato } else { none },
    ..celle
  )
  let corpo = block(breakable: true, griglia)
  // `clearance` 18pt, non 10: con 10 la riga della `sezione` di un float in
  // fondo alla pagina finiva sulla stessa linea della didascalia di un
  // ritratto nella colonna sopra, 7 pt dentro lo spazio riservato (booklet
  // della serata del −1000, p. 65 e p. 72, 2026-09-26). Il flusso a due colonne
  // di Typst 0.15 sbaglia di quel tanto l'altezza lasciata al float: è una
  // mitigazione misurata, non la cura. `validate_booklets --stampa` la tiene.
  let scavalca = place(auto, float: true, scope: "parent", clearance: 18pt, block(width: 100%)[
    #if sezione != none [
      #text(font: TITOLI, size: 7.5pt, fill: seppia, tracking: 0.3pt)[#upper(sezione)]
      #v(-4pt)
    ]
    #griglia
  ])
  if pagina or larga == false { corpo }
  else if larga == true { context if page.columns < 2 { corpo } else { scavalca } }
  else {
    context {
      // una pagina a una colonna (A5, appendici A4) non ha niente da scavalcare
      if page.columns < 2 { return corpo }
      let alta = measure(griglia, width: TABELLA-PAGINA).height
      let stretta = measure(griglia, width: TABELLA-COLONNA).height
      if n >= 4 { scavalca }
      else if alta > TABELLA-FLOAT-MAX { corpo }
      else if stretta > TABELLA-SOGLIA * alta { scavalca }
      else { corpo }
    }
  }
}

// Dove sta il riquadro intero (ADR-0105 punto 7, D5 del piano dello standard di
// stampa). «appendice»: nel punto dell'incontro esce una riga col nome, il GS,
// CA e pf e il rimando alla pagina, più la tattica di quell'incontro; il
// riquadro intero va nell'appendice in fondo (`appendice-creature`), una volta
// sola per creatura. «qui»: il riquadro intero esce dove è scritto, come nei
// fascicoli di schede da dare in mano. L'esportatore sceglie dal manifest.
#let modo-schede = state("modo-schede", "qui")

// Blocco statistiche: il riquadro del mostro/PNG, coi numeri dove il DM li
// cerca invece che dentro un paragrafo (ADR-0021). I campi arrivano già
// strutturati da `dmcore.statblock`: qui c'è solo la forma.
//
// La forma è una sola per ogni creatura, dal goblin al drago (ADR-0105): il
// nome e il GS sulla barra, il tipo sotto, la riga dell'iniziativa, poi le
// fasce DIFESA, ATTACCO, STATISTICHE, CAPACITÀ SPECIALI e TATTICHE, come nelle
// AP. Le fasce si riempiono con le righe leggibili di ADR-0091 (`sezioni`)
// quando la scheda le ha, e se no coi campi del blocco: la forma non cambia,
// cambia solo quanto è piena. Una fascia senza niente dentro non si stampa.
#let statblocco(
  nome: "", tipo: "", gs: "", iniziativa: "", sensi: "",
  ca: "", pf: "", ts: "", velocita: "",
  attributi: (), attacchi: (), voci: (), tattica: "", fonte: "",
  sezioni: (:),
  larga: false,
) = {
  let fascia(titolo, corpo) = if corpo != none [
    #v(3.5pt)
    #block(width: 100%, below: 3pt, stroke: (bottom: 0.6pt + rosso), inset: (bottom: 1.5pt))[
      #text(font: TITOLI, size: 7.4pt, weight: 600, fill: rosso, tracking: 0.8pt)[#upper(titolo)]
    ]
    #corpo
  ]
  // Dai campi, le voci di una fascia stanno su una riga sola separate da «·»,
  // come le righe di ADR-0091: le due vie danno lo stesso riquadro.
  let in-riga(coppie) = {
    let piene = coppie.filter(c => c.at(1) != "" and c.at(1) != [])
    if piene.len() == 0 { none } else { piene.map(c => [*#c.at(0)* #c.at(1)]).join([ · ]) }
  }
  let difesa = sezioni.at("Difesa", default: in-riga((("CA", ca), ("pf", pf), ("TS", ts))))
  let attacco = sezioni.at("Attacco", default: in-riga(
    (("Vel", velocita),) + attacchi.map(a => (a.at(0), a.at(1)))))
  // La griglia delle caratteristiche solo quando ci sono tutte e sei: con
  // tre colonne su sei il riquadro sembra rotto. Altrimenti stanno in riga.
  let griglia-car = attributi.len() == 6
  let statistiche = {
    let testo = sezioni.at("Statistiche", default: in-riga(
      (if griglia-car { () } else { attributi.map(((k, v)) => (k, v)) }) + voci.map(v => (v.at(0), v.at(1)))))
    if not griglia-car and testo == none { none } else [
      #if griglia-car [
        #grid(columns: (1fr,) * attributi.len(), column-gutter: 4pt,
          ..attributi.map(((k, v)) => align(center)[
            #text(font: TITOLI, size: 7pt, fill: seppia)[#upper(k)] \
            #text(size: 9pt, weight: 600)[#v]
          ]))
        #v(2pt)
      ]
      #testo
    ]
  }
  let capacita = sezioni.at("Capacità speciali", default: none)
  let tattiche = sezioni.at("Tattiche", default: if tattica == "" { none } else [#tattica])
  let apertura = sezioni.at("Iniziativa", default: {
    let pezzi = ()
    if iniziativa != "" { pezzi.push([*Iniziativa* #iniziativa]) }
    if sensi != "" { pezzi.push([*Sensi* #sensi]) }
    if pezzi.len() == 0 { none } else { pezzi.join([ · ]) }
  })

  let testa = grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
    par(justify: false, text(font: TITOLI, size: 12pt, weight: 600, fill: rosso, hyphenate: false)[#nome]),
    if gs != "" { text(font: TITOLI, size: 9pt, fill: seppia)[#gs] } else { [] })
  let resto(tattiche) = [
    #if tipo != "" [ #v(1pt) #text(size: 8.6pt, style: "italic", fill: seppia)[#tipo] ]
    #set text(size: 8.8pt)
    #set par(spacing: 0.5em, first-line-indent: 0pt, justify: false)
    #if apertura != none { v(2pt); apertura }
    #fascia("Difesa", difesa)
    #fascia("Attacco", attacco)
    #fascia("Statistiche", statistiche)
    #fascia("Capacità speciali", capacita)
    #if tattiche != none [
      #fascia("Tattiche", text(size: 8.5pt)[#tattiche])
    ]
    #if fonte != "" [ #v(3pt) #text(size: 7.4pt, fill: seppia)[#fonte] ]
  ]
  let intero(tattiche, spezzabile: true) = block(
    width: 100%, fill: boxLato, inset: (x: 9pt, y: 8pt), radius: 2pt,
    stroke: (top: 1.4pt + rosso, bottom: 1.4pt + rosso),
    breakable: spezzabile,
  )[
    // Segnaposti invisibili per la misura di stampa (scripts/misura_stampa.py):
    // la pagina del primo e dell'ultimo segnaposto dice se il riquadro si spezza.
    #metadata(to-string(nome)) <sb-inizio>
    #testa
    #resto(tattiche)
    #metadata(to-string(nome)) <sb-fine>
  ]
  // Il riquadro più alto di una colonna, in appendice: si spezza per forza, e
  // allora fa come Red Hand of Doom. In fondo al pezzo «continua» e dove; in
  // cima al pezzo dopo il nome ripetuto con «(segue)». Testata e piede sono
  // quelli di una tabella, che Typst ripete a ogni pezzo; il contesto dice se
  // il pezzo è il primo o l'ultimo.
  // `accanto`: il riquadro comincia nella colonna di sinistra e finisce in
  // quella di destra della stessa pagina, in due pezzi. Allora la colonna
  // basta a dire quale pezzo è, senza chiedere a Typst dove sono la testa e
  // la fine: meno giri di impaginazione.
  let lungo(chiave, accanto: false) = {
    let inizio() = query(<sb-app>).filter(m => m.value == chiave).first().location()
    let fine() = query(selector(<sb-fine>).after(inizio())).first().location()
    table(columns: 1, stroke: none, inset: (x: 9pt, y: 0pt), fill: boxLato,
      table.header(repeat: true, table.cell(inset: (x: 9pt, top: 8pt, bottom: 2pt),
        stroke: (top: 1.4pt + rosso))[
        #context {
          let primo = if accanto { here().position().x < page.width / 2 } else {
            here().page() == inizio().page() and calc.abs(here().position().y - inizio().position().y) < 30pt and calc.abs(here().position().x - inizio().position().x) < 40pt }
          if primo { testa } else {
            text(font: TITOLI, size: 9.5pt, weight: 600, fill: rosso, hyphenate: false)[#nome]
            text(size: 8pt, style: "italic", fill: seppia)[ (segue)]
          }
        }
      ]),
      table.cell(inset: (x: 9pt, y: 2pt))[
        #metadata(to-string(nome)) <sb-inizio>
        #resto(none)
        #metadata(to-string(nome)) <sb-fine>
      ],
      table.footer(repeat: true, table.cell(inset: (x: 9pt, top: 2pt, bottom: 6pt),
        stroke: (bottom: 1.4pt + rosso))[
        #context {
          let qui = here().position()
          let ultimo = if accanto { qui.x >= page.width / 2 or fine().position().x < page.width / 2 } else {
            // La colonna, non la x esatta: il piede è allineato a destra e
            // la sua x cade lontano da quella del segnaposto di fine.
            let f = fine()
            here().page() == f.page() and (qui.x < page.width / 2) == (f.position().x < page.width / 2) }
          // Il piede ha la stessa altezza con e senza «continua»: se cambiasse,
          // cambierebbe anche dove si spezza il riquadro e Typst non
          // troverebbe un'impaginazione stabile.
          let dove = if page.columns > 1 and qui.x < page.width / 2 [nella colonna accanto] else [a pagina #(counter(page).get().first() + 1)]
          let riga = align(right, text(size: 8pt, style: "italic", fill: seppia)[continua #dove])
          if ultimo { hide(riga) } else { riga }
        }
      ]),
    )
  }
  // La chiave dice se due comparse sono la stessa creatura: stesso nome e
  // stessi numeri. La tattica non conta, perché cambia da un incontro all'altro.
  let chiave = to-string(nome) + "|" + repr(intero(none))
  context {
    if modo-schede.get() != "appendice" {
      let corpo = intero(tattiche)
      if larga { place(top, float: true, scope: "parent", clearance: 10pt, corpo) } else { corpo }
      return
    }
    [#metadata((chiave: chiave, nome: to-string(nome), intero: intero(none, spezzabile: false),
                lungo: lungo(chiave), accanto: lungo(chiave, accanto: true))) <sb-dato>]
    // La riga dell'incontro: quanto serve per tenere il conto al tavolo, e la
    // pagina dove sta il resto. I campi brevi, non le fasce: CA e pf.
    let pagina = {
      let qui = query(<sb-app>).filter(m => m.value == chiave)
      if qui.len() > 0 { counter(page).at(qui.first().location()).first() } else { none }
    }
    let pezzi = ()
    if ca != "" and ca != [] { pezzi.push([*CA* #ca]) }
    if pf != "" and pf != [] { pezzi.push([*pf* #pf]) }
    // Spezzabile: sotto un float a tutta pagina Typst 0.15 sbaglia lo spazio
    // che resta in colonna, e un blocco che non si spezza finiva sopra il piede
    // (Abbazia, p. 26, 2026-10-29). Il nome resta attaccato alla prima riga.
    block(width: 100%, breakable: true, above: 0.9em, below: 0.6em,
      stroke: (left: 2pt + rosso), inset: (left: 7pt, y: 3pt))[
      #set par(first-line-indent: 0pt, justify: false, spacing: 0.4em)
      #text(font: TITOLI, size: 9.5pt, weight: 600, fill: rosso, hyphenate: false)[#nome]
      #if gs != "" { h(0.4em); text(font: TITOLI, size: 8pt, fill: seppia)[#gs] }
      #if pagina != none {
        h(1fr); text(size: 8.4pt, style: "italic", fill: seppia)[scheda a pagina #pagina]
      }
      #if pezzi.len() > 0 [ \ #text(size: 8.8pt)[#pezzi.join([ · ])] ]
      #if tattiche != none [
        #v(2pt)
        #text(font: TITOLI, size: 7.4pt, weight: 600, fill: rosso, tracking: 0.8pt)[TATTICHE]
        #v(1pt)
        #text(size: 8.6pt)[#tattiche]
      ]
    ]
  }
}

// L'appendice delle creature: ogni riquadro intero una volta sola, in ordine
// di nome, a due colonne. Un riquadro non si spezza mai a pagina girata
// (criterio WotC del piano, I6): nella colonna di destra, se non entra, passa
// intero alla pagina dopo; in quella di sinistra continua nella colonna
// accanto, col «continua» in fondo e il nome ripetuto in cima. Se
// nessuna scheda è andata in appendice, la pagina non esiste.
#let appendice-creature(titolo: "Appendice: le creature") = context {
  let viste = (:)
  for m in query(<sb-dato>) {
    if m.value.chiave not in viste { viste.insert(m.value.chiave, m.value) }
  }
  if viste.len() == 0 { return }
  let elenco = viste.values().sorted(key: v => lower(v.nome))
  capitolo-aperto(titolo, none)
  [#metadata(none) <sb-app-inizio>]
  // Le misure della pagina. La larghezza della colonna è quella delle tabelle
  // (`TABELLA-COLONNA`); l'altezza è la pagina meno i margini.
  let a5 = page.width < 16cm
  let due = page.columns > 1
  let larghezza = if due { TABELLA-COLONNA } else { page.width - if a5 { 2.6cm } else { 3.5cm } }
  let colonna = page.height - if a5 { 2.9cm } else { 4.1cm }
  let cima = if a5 { 1.5cm } else { 2.1cm }
  let fondo-col = page.height - if a5 { 1.4cm } else { 2.0cm }
  // Dove cade ogni riquadro si calcola qui, sommando le altezze, e non con
  // `here()`: un riquadro che non si spezza si porta dietro anche la propria
  // posizione nella colonna dopo, e una scelta presa sulla posizione chiede
  // a Typst giri di impaginazione in più che non convergono. Il conto è
  // prudente (spazio fra i riquadri largo, colonna destra della prima pagina
  // presa alla stessa altezza della sinistra): sbaglia solo nel senso di
  // spostare un riquadro che sarebbe entrato, come prima.
  let inizio = query(<sb-app-inizio>)
  let y-prima = if inizio.len() > 0 { inizio.first().location().position().y } else { cima }
  let spazio = 12pt
  let col = 0
  let y = y-prima
  let cima-destra = y-prima
  for v in elenco {
    let alto = measure(v.intero, width: larghezza).height
    let resta = fondo-col - y
    // Nella colonna di sinistra un riquadro che non entra continua nella
    // colonna accanto, sulla stessa pagina, invece di lasciare bianca metà
    // della colonna (ARC-07 Notte e Alba p. 100, colonna piena al 29%,
    // rimisura del 2026-10-29). Non gira pagina: il criterio WotC regge.
    let nella-accanto = due and col == 0 and resta > 6cm and alto > resta and alto - resta < (fondo-col - cima-destra) * 0.9
    if nella-accanto {
      [#metadata(v.chiave) <sb-app>]
      block(width: 100%, below: 1em, v.accanto)
      col = 1
      y = cima-destra + alto - resta + 30pt + spazio
    } else if alto < colonna * 0.92 {
      [#metadata(v.chiave) <sb-app>]
      block(width: 100%, breakable: false, below: 1em, v.intero)
      if alto > resta {
        if due and col == 0 { col = 1; y = cima-destra } else { col = 0; y = cima; cima-destra = cima }
      }
      y += alto + spazio
    } else {
      // Più alto di una colonna: comincia in cima a una pagina, così due
      // colonne lo tengono senza girare pagina; più alto di due, comincia su
      // una pagina pari e si legge sulle due facciate aperte.
      pagebreak(weak: true, to: if due and alto > colonna * 1.85 { "even" } else { none })
      [#metadata(v.chiave) <sb-app>]
      block(width: 100%, below: 1em, v.lungo)
      cima-destra = cima
      if not due or alto <= colonna { col = 0; y = cima + alto + spazio }
      else if alto <= colonna * 2 { col = 1; y = cima + alto - colonna + 30pt + spazio }
      else { col = 0; y = cima + alto - colonna * 2 + 60pt + spazio }
    }
  }
}

// La pagina dei crediti, sul verso del frontespizio — dov'e' in un manuale
// stampato. Prima del 2026-09-02 i volumi di questo repo uscivano anonimi: senza
// autore, senza data, senza versione e senza la riga che dice su cosa si basano.
// Due PDF dello stesso capitolo, stampati a un mese di distanza, erano
// indistinguibili sul tavolo.
//
// La `data` arriva SEMPRE dal manifest, mai da `datetime.today()`: un volume che
// prende la data dall'orologio cambia a ogni compilazione e smette di essere
// byte-identico, che e' la proprieta' su cui poggia il gate di stampa in CI.
#let colophon(voci: (), licenza: "", nota: "") = page(columns: 1, header: none)[
  #v(1fr)
  #align(center)[
    #text(font: TITOLI, size: 10pt, fill: seppia, tracking: 2.5pt)[COLOPHON]
    #v(0.35cm)
    #line(length: 30%, stroke: 0.5pt + seppia)
  ]
  #v(0.7cm)
  #block(width: 100%, inset: (x: 2.2cm))[
    #set text(size: 9pt, fill: inchiostro)
    #set par(justify: false, first-line-indent: 0pt, leading: 0.7em)
    #for (etichetta, valore) in voci {
      if valore != "" {
        grid(columns: (3.4cm, 1fr), column-gutter: 0.5em, row-gutter: 0.5em,
          text(font: TITOLI, size: 8pt, fill: seppia)[#upper(etichetta)],
          [#valore])
        v(0.18cm)
      }
    }
    #if licenza != "" [
      #v(0.5cm)
      #line(length: 100%, stroke: 0.4pt + seppia.lighten(45%))
      #v(0.35cm)
      #text(size: 8.5pt, style: "italic", fill: seppia)[#licenza]
    ]
    #if nota != "" [
      #v(0.35cm)
      #text(size: 8pt, fill: seppia)[#nota]
    ]
  ]
  #v(1fr)
  #align(center)[#text(fill: seppia, size: 12pt)[⬦]]
]

// `apparato: false` toglie frontespizio e indice. Serve a un fascicolo di
// schede: sei fogli da stampare e dare in mano, dove una copertina e un indice
// sarebbero due pagine da saltare ogni volta che si va alla fotocopiatrice.
//
// `carta: "bianca"` toglie il fondo avorio. Sessanta pagine di fondo pieno su
// una stampante di casa sono una cartuccia: il volume «da leggere» e il volume
// «da stampare stasera» non sono lo stesso file.
#let libro(titolo: "", sottotitolo: "", brand: "", banner: "", meta: "", capitolo: "",
           apparato: true, carta: "avorio", formato: "a4", copertina: none, intro: none,
           crediti: none,
           corpo) = {
  // A5 è il formato «libretto»: **una colonna sola**, perché in A5 due colonne
  // sarebbero da 5 cm e nessuno impagina un manuale così.
  //
  // Sta accanto all'imposizione (ADR-0027), non al posto suo, e la differenza è
  // il corpo del testo: `pdfcpu booklet` prende il volume A4 e ne mette due per
  // foglio, cioè **scala tutto al 71%** — 10.2 pt diventano ~7.2, che si
  // stampano ma non si leggono al tavolo. Comporre in A5 e poi imporre due
  // pagine per foglio A4 tiene il corpo a 9.6 pt, che è la misura di un manuale
  // tascabile vero.
  let a5 = formato == "a5"
  let fondo = if carta == "bianca" { white } else { avorio }
  set document(title: titolo)
  set page(
    paper: if a5 { "a5" } else { "a4" },
    // Margini SPECULARI: rilegato o pinzato, il margine interno finisce nella
    // piega. `inside`/`outside` è ciò che distingue un libro da una risma.
    margin: if a5 { (inside: 1.5cm, outside: 1.1cm, top: 1.5cm, bottom: 1.4cm) }
            else { (inside: 2.0cm, outside: 1.5cm, top: 2.1cm, bottom: 2.0cm) },
    binding: left,
    fill: fondo,
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8pt, fill: seppia, style: "italic")
        // La testatina destra segue il CAPITOLO corrente: è ciò che rende
        // sfogliabile un volume di sessanta pagine.
        let qui = query(selector(heading.where(level: 1)).before(here()))
        grid(columns: (1fr, 1fr),
          align(left)[#titolo],
          align(right)[#if qui.len() > 0 { qui.last().body } else { capitolo }],
        )
        v(-6pt)
        line(length: 100%, stroke: 0.4pt + seppia.lighten(40%))
      }
    },
    footer: context {
      set text(size: 9pt, fill: seppia)
      align(center)[#text(size: 7pt)[⬦]~#counter(page).display()~#text(size: 7pt)[⬦]]
    },
  )
  set text(font: SERIF, size: if a5 { 9.6pt } else { 10.2pt },
           fill: inchiostro, lang: "it")
  set par(justify: true, leading: eval(VARIANTE.interlinea), first-line-indent: 1.1em)

  // Il § nei TITOLI diventa un numero dentro un medaglione — la stessa cornice
  // circolare dei fregi di capitolo, così il libro ha un segno solo invece di
  // due. Nei RIMANDI dentro il testo il § resta piatto: serve a ritrovare la
  // sezione («vedi §4»), e sostituirlo lì romperebbe i riferimenti.
  let medaglione(n) = box(baseline: 16%)[
    #circle(radius: 0.52em, stroke: 0.7pt + seppia, fill: none)[
      #align(center + horizon)[
        #text(font: TITOLI, size: 0.66em, fill: seppia, weight: 600)[#n]
      ]
    ]
  ]
  // Un titolo in fondo alla colonna, col suo testo nella colonna dopo, è il
  // difetto che si nota per primo sfogliando: `sticky` lo tiene attaccato.
  show heading: set block(above: 1.1em, below: 0.65em, sticky: true)
  show heading: it => {
    set text(font: TITOLI, fill: if it.level == 1 { rosso } else { seppia })
    if it.level == 1 { text(size: 15pt, weight: 600)[#it.body] }
    else {
      // «§3 · Titolo» → medaglione(3) + Titolo. Se il titolo non comincia con
      // un §, resta esattamente com'è.
      let grezzo = to-string(it.body)
      let m = grezzo.match(regex("^§\s*([0-9]+(?:[-–][a-z]+)?)\s*(?:·|-|—)?\s*(.*)$"))
      let dim = if it.level == 2 { 11.5pt } else { 10pt }
      if m != none {
        text(size: dim, weight: 600)[#medaglione(m.captures.at(0))~#m.captures.at(1)]
      } else {
        text(size: dim, weight: 600)[#it.body]
      }
    }
  }
  show strong: set text(fill: rgb("#4a2c12"), weight: 600)
  show raw: set text(font: MONO, size: 9pt)
  // Un percorso in `codice` è una parola sola: senza punti di rottura esce
  // dalla colonna e si stampa sopra quella accanto (il volume del −1000 e la
  // sessione di Terros, 2026-09-25). Si spezza dopo / _ . - e fra una
  // minuscola e una maiuscola (`PortaleDellaForgiaEterna`), e non altrove.
  show raw.where(block: false): it => {
    show regex("[/_.\-]"): c => c + sym.zws
    show regex("\p{Ll}\p{Lu}"): c => c.text.first() + sym.zws + c.text.last()
    it
  }

  if not apparato {
    corpo
    return
  }

  // Frontespizio
  align(center)[
    #v(if copertina == none { 3.2cm } else { 1.4cm })
    #text(font: TITOLI, size: 11pt, fill: seppia, tracking: 3pt)[#brand]
    #v(0.6cm)
    #line(length: 45%, stroke: 0.6pt + seppia)
    #v(0.5cm)
    #text(font: TITOLI, size: 27pt, weight: 600, fill: rosso)[#titolo]
    #v(0.25cm)
    #text(size: 11.5pt, style: "italic", fill: seppia)[#sottotitolo]
    #v(0.5cm)
    #line(length: 45%, stroke: 0.6pt + seppia)
    #if copertina != none [
      #v(0.7cm)
      #block(clip: true, radius: 2pt, stroke: 0.7pt + seppia,
        image(copertina, width: 11cm, alt: titolo))
    ]
    #v(0.8cm)
    #text(font: TITOLI, size: 8.5pt, fill: seppia, tracking: 1.5pt)[#banner]
    #if meta != "" [
      #v(0.35cm)
      #text(size: 8.5pt, style: "italic", fill: seppia)[#meta]
    ]
    #v(1.2cm)
    #text(fill: seppia, size: 15pt)[❦]
  ]
  pagebreak()

  // Il colophon sta sul verso del frontespizio: e' la prima cosa che si trova
  // aprendo il volume, come in un manuale stampato.
  if crediti != none { crediti }

  // La pagina d'introduzione del manifest (`intro_md`): la catena HTML la
  // stampa da sempre, questa la ignorava in silenzio.
  if intro != none {
    intro
    pagebreak()
  }

  // Indice cliccabile (e segnalibri PDF dagli heading)
  align(center)[#text(font: TITOLI, size: 13pt, fill: rosso)[Indice]]
  v(0.4cm)
  outline(title: none, depth: 3, indent: 1em)
  pagebreak()

  set page(columns: if a5 { 1 } else { 2 })
  corpo
}
