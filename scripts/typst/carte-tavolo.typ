// carte-tavolo.typ — le carte da tavolo di una corsa (voce B3 della ricerca
// su cosa serve a un modulo pubblicabile).
//
// Non sono un capitolo: sono pezzi di cartoncino che stanno sul tavolo per
// tutta la serata e dicono **a che punto è la gara senza che il DM lo
// spieghi**. Nove carte da 63 × 88 mm (il formato delle carte da gioco) per
// foglio A4, tre per tre, con la linea di taglio tratteggiata in comune.
//
// Cinque mazzetti:
//   contrada — il segnaposto: stemma, nome, motto, livrea, e la griglia delle
//              Lunghezze da segnare a matita tratto per tratto;
//   funi     — l'ordine estratto allo Stacco: un numero grande per carta;
//   tratto   — dove è la corsa adesso: giro, tratto, CD e cosa succede se
//              si sbaglia di 5;
//   posto    — dove si è messo un PG non fantino e cosa può fare da lì;
//   patto    — in bianco: il patto stretto si scrive e si mette al centro.
//
// Lo riempie scripts/export_booklet_typst.py con i dati di
// scripts/dmcore/carte_tavolo.py, che li legge dai master. Qui non si scrive
// contenuto: solo forma.

#import "tema-rumblingstone.typ": inchiostro, rosso, seppia, titolo-visibile

#let bordo = seppia.lighten(45%)
#let campo = rgb("#efe6d2")
#let LARGA = 63mm
#let ALTA = 88mm

// Lo stemma senza scritte: gli scudi della serie Golarion portano nel
// cartiglio il motto e il nome del Palio di Channathgate, non quelli di
// Tarsilia (CONTRADE-DI-TARSILIA.md §7). Sulla carta il nome e il motto li
// scrive il modello, quindi le scritte dello scudo si tolgono qui, alla
// lettura, senza copiare il file: le scritte e il cartiglio che le porta
// (il rettangolo scuro 166 × 26 in fondo allo scudo), che vuoto restava una
// barra nera senza senso.
#let stemma(percorso, alt, alto: 21mm) = {
  let svg = read(percorso)
    .replace(regex("<text[^>]*>[^<]*</text>"), "")
    .replace(regex("<rect x=\"17\" y=\"182\" width=\"166\" height=\"26\"[^>]*/>"), "")
  image(bytes(svg), format: "svg", height: alto, alt: alt)
}

// L'intestazione piccola in cima a ogni carta: dice di che mazzetto è.
#let occhiello(testo) = align(center, text(font: "Cinzel", size: 7pt, fill: seppia,
  tracking: 1.2pt)[#upper(testo)])

// Il titolo della carta: un titolo di livello 2 nell'albero dei tag (PDF/UA-1),
// disegnato in Cinzel.
#let nome-carta(testo, size: 13pt) = align(center, titolo-visibile(2,
  text(font: "Cinzel", size: size, weight: 600, fill: rosso)[#testo]))

#let filetto = line(length: 100%, stroke: 0.4pt + bordo)

// La carta: un riquadro 63 × 88 con il bordo tratteggiato che fa da linea di
// taglio. Il contenuto sta dentro 4 mm di margine.
#let carta(corpo) = block(
  width: LARGA, height: ALTA, inset: 4mm, breakable: false,
  stroke: (thickness: 0.4pt, paint: bordo, dash: "dashed"),
)[
  #set align(left)
  #set text(size: 8pt, fill: inchiostro)
  #set par(justify: false, leading: 0.45em, first-line-indent: 0pt, spacing: 0.5em)
  #corpo
]

#let vuota = block(width: LARGA, height: ALTA)

// ── i cinque mazzetti ────────────────────────────────────────────────────────

#let carta-contrada(numero: "", nome: "", dei: "", livrea: "", motto: "",
                    stemma-file: none, giri: 3, tratti: ()) = carta[
  #occhiello("Contrada n. " + numero)
  #v(2pt)
  #align(center, if stemma-file != none {
    stemma(stemma-file, "Stemma della contrada " + nome)
  } else {
    block(width: 18mm, height: 21mm, stroke: (thickness: 0.5pt, paint: bordo, dash: "dashed"))
  })
  #v(1pt)
  #nome-carta(nome, size: 14pt)
  #align(center, text(size: 7.4pt, fill: seppia)[#dei])
  #v(1pt)
  #align(center, text(size: 8pt, style: "italic")[«#motto»])
  #v(1pt)
  #align(center, text(size: 7pt, fill: seppia)[livrea: #livrea])
  #v(2pt)
  #filetto
  #v(1pt)
  #text(size: 7.2pt)[Cavallo #box(width: 1fr, repeat[.]) Ritmo #box(width: 7mm, repeat[.])]
  #v(1pt)
  // La griglia delle Lunghezze: una riga per tratto, una colonna per giro, e
  // lo Stacco in testa. Si segna a matita; la somma è la posizione.
  #let romani = ("I", "II", "III", "IV", "V")
  #table(
    columns: (1fr,) + (6.5mm,) * giri,
    inset: (x: 2pt, y: 3.4pt),
    stroke: 0.4pt + bordo,
    align: (left, center, center, center, center).slice(0, giri + 1),
    table.header(
      text(size: 7pt, font: "Cinzel", fill: seppia)[Lunghezze],
      ..range(giri).map(g => text(size: 7pt, font: "Cinzel", fill: seppia)[#romani.at(g)]),
    ),
    text(size: 7pt)[Stacco], table.cell(colspan: giri, fill: campo)[],
    ..tratti.map(t => (text(size: 7pt)[#t], ..range(giri).map(_ => []))).flatten(),
  )
]

#let carta-funi(posto: "", di: "", finte: ()) = carta[
  #occhiello("Lo Stacco · alle funi")
  #v(5mm)
  #align(center, text(font: "Cinzel", size: 46pt, weight: 600, fill: rosso)[#posto])
  #v(-2mm)
  #nome-carta("Alle funi, " + posto + "º di " + di, size: 9pt)
  #v(3mm)
  #filetto
  #text(font: "Cinzel", size: 7pt, fill: seppia)[Fra le funi si fa una cosa sola:]
  #v(1pt)
  #for f in finte [
    #block(above: 3pt, below: 0pt)[#f]
  ]
]

#let carta-rincorsa(numero: "", regola: []) = carta[
  #occhiello("Lo Stacco · di rincorsa")
  #v(5mm)
  #align(center, text(font: "Cinzel", size: 46pt, weight: 600, fill: rosso)[#numero])
  #v(-2mm)
  #nome-carta("Di rincorsa", size: 11pt)
  #v(3mm)
  #filetto
  #v(2pt)
  #text(size: 8.2pt)[#regola]
]

#let carta-tratto(giro: "", nome: "", cd: "", nota: [], numero: "", totale: "", esito: []) = carta[
  #occhiello("Giro " + giro + " · tratto " + numero + " di " + totale)
  #v(3mm)
  #nome-carta(nome, size: 14pt)
  #v(1mm)
  #align(center, block(fill: campo, radius: 2pt, stroke: 0.5pt + bordo, inset: (x: 8pt, y: 4pt))[
    #text(font: "Cinzel", size: 8pt, fill: seppia)[CD]
    #h(4pt)
    #text(size: 26pt, weight: 600)[#cd]
  ])
  #v(2mm)
  #text(size: 9pt)[#nota]
  #v(1fr)
  #filetto
  #text(size: 7.2pt, fill: seppia)[#esito]
]

#let carta-posto(nome: "", chi: "", azioni: [], quando: []) = carta[
  #occhiello("Il posto in corsa")
  #v(3mm)
  #nome-carta(nome, size: 11.5pt)
  #align(center, text(size: 7.4pt, fill: seppia, style: "italic")[ci sta bene: #chi])
  #v(2mm)
  #filetto
  #v(2pt)
  #text(size: 8.2pt)[#azioni]
  #v(1fr)
  #filetto
  #text(size: 7.2pt, fill: seppia)[#quando]
]

#let carta-patto(vale: [], rompere: []) = carta[
  #occhiello("I Partiti")
  #v(2mm)
  #nome-carta("Patto", size: 14pt)
  #v(2mm)
  #text(size: 7.6pt)[fra #box(width: 1fr, repeat[.])]
  #v(2pt)
  #text(size: 7.6pt)[e #box(width: 1fr, repeat[.])]
  #v(3mm)
  #text(font: "Cinzel", size: 7pt, fill: seppia)[Clausole]
  #for _ in range(7) {
    v(3.2mm)
    line(length: 100%, stroke: 0.3pt + bordo)
  }
  #v(1fr)
  #text(size: 7.2pt, fill: seppia)[#vale #rompere]
]

// ── il foglio ────────────────────────────────────────────────────────────────

// Un foglio A4 di carte, nove per pagina, con il titolo del mazzetto in cima.
// Le carte stanno a contatto: la linea tratteggiata è il taglio, uno solo
// fra due carte vicine.
#let foglio-carte(titolo, carte) = page(
  columns: 1,
  margin: (x: 1.0cm, top: 0.9cm, bottom: 0.8cm),
  header: none,
  footer: none,
)[
  #{
    show heading: set block(above: 0pt, below: 0pt, sticky: false)
    heading(level: 1, text(font: "Cinzel", size: 10pt, weight: 600, fill: seppia, tracking: 1.2pt)[#titolo])
  }
  #v(2.5mm)
  #align(center, grid(
    columns: (LARGA,) * 3,
    rows: (ALTA,) * 3,
    ..carte,
    ..range(9 - carte.len()).map(_ => vuota),
  ))
]
