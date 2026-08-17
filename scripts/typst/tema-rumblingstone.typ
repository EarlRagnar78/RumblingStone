// tema-rumblingstone.typ — il tema di stampa del repo (ADR-0020).
//
// Lo usa scripts/export_booklet_typst.py: NON si modifica il .typ generato,
// si modifica questo. Il contenuto arriva dai master markdown (ADR-0003).
// Impaginazione da manuale: due colonne, carta avorio, capolettera, fregi,
// box read-aloud, tabelle a righe alternate, indice cliccabile.

#let avorio    = rgb("#f6efe0")
#let inchiostro = rgb("#241d16")
#let seppia    = rgb("#6b4f2a")
#let rosso     = rgb("#7d2b1f")
#let boxLeggi  = rgb("#ece0c6")

// Apertura di capitolo: il medaglione + il titolo, su tutta la larghezza delle
// due colonne. È il segno che dice al lettore dov'è prima che legga il titolo.
#let capitolo-aperto(titolo, fregio) = {
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
        text(font: "Cinzel", size: 17pt, weight: 600, fill: rosso)[#titolo])
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

#let fregio() = align(center)[
  #v(0.3em)
  #text(fill: seppia, size: 11pt)[❦]
  #v(0.3em)
]

// Read-aloud: il testo che si legge ad alta voce al tavolo.
#let leggi(body) = block(
  width: 100%, fill: boxLeggi, inset: (x: 9pt, y: 8pt), radius: 2pt,
  stroke: (left: 2pt + seppia),
  breakable: true,
)[#text(style: "italic", size: 9.4pt, fill: inchiostro)[#body]]

// Nota di regia per il DM.
#let nota(body) = block(
  width: 100%, inset: (x: 8pt, y: 6pt),
  stroke: (left: 1.5pt + rgb("#b9a789")),
  breakable: true,
)[#text(size: 9pt, fill: rgb("#4a3f33"))[#body]]

// Una tabella da 4+ colonne in una colonna da 8 cm diventa illeggibile: si
// spezzano perfino le parole del titolo. Sopra quella soglia scavalca le due
// colonne, che è quello che fa un manuale stampato.
#let tabella(n, ..celle) = {
  let corpo = block(breakable: true)[
  #table(
    columns: n,
    stroke: none,
    inset: (x: 6pt, y: 4.5pt),
    fill: (_, row) => if row == 0 { seppia.lighten(60%) }
                      else if calc.odd(row) { rgb("#efe6d2") } else { none },
    ..celle
  )
]
  if n >= 4 { place(top, float: true, scope: "parent", clearance: 10pt, corpo) }
  else { corpo }
}

// `apparato: false` toglie frontespizio e indice. Serve a un fascicolo di
// schede: sei fogli da stampare e dare in mano, dove una copertina e un indice
// sarebbero due pagine da saltare ogni volta che si va alla fotocopiatrice.
#let libro(titolo: "", sottotitolo: "", brand: "", meta: "", capitolo: "",
           apparato: true, corpo) = {
  set document(title: titolo)
  set page(
    paper: "a4",
    margin: (top: 2.1cm, bottom: 2.0cm, x: 1.7cm),
    fill: avorio,
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
      align(center)[#counter(page).display()]
    },
  )
  set text(font: "EB Garamond", size: 10.2pt, fill: inchiostro, lang: "it")
  set par(justify: true, leading: 0.62em, first-line-indent: 1.1em)

  // Il § nei TITOLI diventa un numero dentro un medaglione — la stessa cornice
  // circolare dei fregi di capitolo, così il libro ha un segno solo invece di
  // due. Nei RIMANDI dentro il testo il § resta piatto: serve a ritrovare la
  // sezione («vedi §4»), e sostituirlo lì romperebbe i riferimenti.
  let medaglione(n) = box(baseline: 16%)[
    #circle(radius: 0.52em, stroke: 0.7pt + seppia, fill: none)[
      #align(center + horizon)[
        #text(font: "Cinzel", size: 0.66em, fill: seppia, weight: 600)[#n]
      ]
    ]
  ]
  show heading: it => {
    set text(font: "Cinzel", fill: if it.level == 1 { rosso } else { seppia })
    set block(above: 1.1em, below: 0.65em)
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
  show raw: set text(font: "DejaVu Sans Mono", size: 8.6pt)

  if not apparato {
    corpo
    return
  }

  // Frontespizio
  align(center)[
    #v(3.2cm)
    #text(font: "Cinzel", size: 11pt, fill: seppia, tracking: 3pt)[#brand]
    #v(0.6cm)
    #line(length: 45%, stroke: 0.6pt + seppia)
    #v(0.5cm)
    #text(font: "Cinzel", size: 27pt, weight: 600, fill: rosso)[#titolo]
    #v(0.25cm)
    #text(size: 11.5pt, style: "italic", fill: seppia)[#sottotitolo]
    #v(0.5cm)
    #line(length: 45%, stroke: 0.6pt + seppia)
    #v(0.8cm)
    #text(font: "Cinzel", size: 8.5pt, fill: seppia, tracking: 1.5pt)[#meta]
    #v(1.2cm)
    #text(fill: seppia, size: 15pt)[❦]
  ]
  pagebreak()

  // Indice cliccabile (e segnalibri PDF dagli heading)
  align(center)[#text(font: "Cinzel", size: 13pt, fill: rosso)[Indice]]
  v(0.4cm)
  outline(title: none, depth: 3, indent: 1em)
  pagebreak()

  set page(columns: 2)
  corpo
}
