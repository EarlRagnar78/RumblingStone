// scheda-pg.typ — una scheda pregenerata su UNA pagina A4 (ADR-0020).
//
// Non è un capitolo di libro: è il foglio che il giocatore tiene in mano per
// tre sessioni. Perciò l'impaginazione è a due pannelli e non a due colonne —
// **a sinistra chi sei** (background in prima persona, equipaggiamento, i
// legami con gli altri cinque), **a destra quanto fai** (CA, pf, TS, i sei
// attributi, abilità, talenti, attacchi, incantesimi) — con la fascia alta a
// fare da testata e «Come si gioca in un minuto» a chiudere in fondo.
//
// Il modello è la scheda pregenerata dei moduli PF1e (We Be Goblins e simili):
// chi arriva in ritardo guarda la fascia alta, il piede, e sa giocare.
//
// Lo riempie scripts/export_booklet_typst.py leggendo i master markdown
// (`PREGEN-*.md` + `FASCICOLO-*.md`). Qui non si scrive contenuto: solo forma.

#import "tema-rumblingstone.typ": avorio, boxLeggi, inchiostro, rosso, seppia

#let bordo = seppia.lighten(45%)
#let campo = rgb("#efe6d2")

// ── mattoncini ───────────────────────────────────────────────────────────────

// Il titoletto di sezione: piccolo, in Cinzel, con la sua riga sotto. È quello
// che rende «scorribile» un foglio denso — l'occhio salta di titolo in titolo.
// La `nota` è la mezza riga di istruzioni («da leggere ad alta voce»). Sta in
// tondo e senza spaziatura allargata: in Cinzel spaziato andrebbe a capo e
// lascerebbe una parola sola sulla seconda riga, che in un titoletto si vede.
#let sezione(titolo, nota: none) = block(above: 7pt, below: 3.5pt, width: 100%)[
  #text(font: "Cinzel", size: 7.8pt, weight: 600, fill: rosso, tracking: 0.9pt)[#titolo]
  #if nota != none {
    text(size: 7.6pt, style: "italic", fill: seppia)[ · #nota]
  }
  #v(1pt)
  #line(length: 100%, stroke: 0.4pt + bordo)
]

// Un valore che si legge da lontano: CA, pf, e i sei attributi.
#let riquadro(etichetta, valore, sotto: none, grande: false) = block(
  width: 100%, fill: campo, radius: 2pt, stroke: 0.5pt + bordo,
  inset: (x: 3pt, y: if grande { 4.5pt } else { 3pt }),
)[
  #set align(center)
  #text(font: "Cinzel", size: 6.9pt, fill: seppia, tracking: 0.7pt)[#etichetta]
  #v(if grande { -4pt } else { -3.5pt })
  #text(size: if grande { 21pt } else { 13.5pt }, weight: 600, fill: inchiostro)[#valore]
  #if sotto != none {
    v(-4pt)
    text(size: 7.1pt, fill: seppia, style: "italic")[#sotto]
  }
]

// La cella di un attributo: sigla, punteggio, modificatore. Il modificatore è
// in rosso perché è il numero che si somma davvero ai dadi.
#let attributo(sigla, punteggio, modificatore) = block(
  width: 100%, fill: campo, radius: 2pt, stroke: 0.5pt + bordo, inset: (y: 3.5pt),
)[
  #set align(center)
  #text(font: "Cinzel", size: 6.7pt, fill: seppia, tracking: 0.5pt)[#sigla]
  #v(-4.5pt)
  #text(size: 15pt, weight: 600)[#punteggio]
  #v(-5pt)
  #text(font: "Cinzel", size: 8.9pt, weight: 600, fill: rosso)[#modificatore]
]

// Voce a etichetta: «Talenti — Attacco Poderoso · …». L'etichetta in Cinzel fa
// da appiglio; il corpo resta prosa giustificata.
#let voce(etichetta, corpo) = block(above: 4pt, below: 0pt, width: 100%)[
  #text(font: "Cinzel", size: 8pt, weight: 600, fill: seppia)[#etichetta]
  #h(3pt)
  #corpo
]

// ── la pagina ────────────────────────────────────────────────────────────────

#let scheda(
  nome: "",
  ruolo: "",
  numero: "",
  totale: "",
  classe: "",
  occhiello: none,
  ritratto: none,
  rapide: (),
  ca: "", ca-dettaglio: none,
  pf: "", pf-dado: "",
  ts: (), ts-nota: none,
  attributi: (),
  manovre: (),
  attacchi: (),
  destra: (),
  ad-alta-voce: none,
  retro: (),
  equipaggiamento: none,
  legami: (),
  problema: none,
  minuto: none,
  piede: "",
) = page(
  columns: 1,
  margin: (x: 1.0cm, top: 0.9cm, bottom: 0.8cm),
  header: none,
  footer: none,
)[
  // Il segnalibro PDF e la voce d'indice: `place` lo tiene fuori dal flusso,
  // così non ruba una riga alla fascia alta.
  #place(hide(heading(level: 1, nome)))

  #set text(size: 8.9pt)
  #set par(justify: true, leading: 0.52em, first-line-indent: 0pt, spacing: 0.55em)

  // ── fascia alta ───────────────────────────────────────────────────────────
  #block(width: 100%, below: 7pt)[
    #grid(
      columns: (3.9cm, 1fr, 2.6cm),
      column-gutter: 9pt,
      align: horizon,

      if ritratto != none {
        block(radius: 2pt, clip: true, stroke: 0.7pt + seppia, image(ritratto, width: 3.9cm))
      } else {
        block(width: 3.9cm, height: 5.05cm, radius: 2pt, stroke: (thickness: 0.7pt, paint: bordo, dash: "dashed"))[
          #align(center + horizon)[#text(size: 7pt, fill: seppia, style: "italic")[ritratto]]
        ]
      },

      block[
        #text(font: "Cinzel", size: 8.2pt, fill: seppia, tracking: 1.6pt)[
          #upper(ruolo) #h(4pt) · #h(4pt) SCHEDA #numero DI #totale
        ]
        #v(-1pt)
        #block(above: 3pt, below: 3pt)[
          #text(font: "Cinzel", size: 22pt, weight: 600, fill: rosso)[#nome]
        ]
        #line(length: 100%, stroke: 0.6pt + seppia)
        #v(2pt)
        #text(size: 9.4pt, weight: 600, fill: rgb("#4a2c12"))[#classe]
        #if occhiello != none {
          v(1pt)
          text(size: 8.6pt, style: "italic", fill: rgb("#4a3f33"))[#occhiello]
        }
      ],

      // I tre numeri che si consultano a ogni scena, dove l'occhio li ritrova
      // senza cercarli: in alto a destra, sempre.
      block(width: 100%)[
        #stack(spacing: 3.5pt, ..rapide.map(((e, v)) => riquadro(upper(e), v)))
      ],
    )
  ]

  #line(length: 100%, stroke: 1pt + seppia)
  #v(5pt)

  // ── i due pannelli ────────────────────────────────────────────────────────
  #grid(
    columns: (1fr, 1.06fr),
    column-gutter: 11pt,
    inset: (x: 0pt),
    grid.vline(x: 1, stroke: 0.5pt + bordo, position: start),

    // ————— sinistra: chi sei —————
    block(width: 100%)[
      #if ad-alta-voce != none {
        sezione("CHI SEI", nota: "da leggere ad alta voce al tavolo")
        block(
          width: 100%, fill: boxLeggi, inset: (x: 7pt, y: 6pt), radius: 2pt,
          stroke: (left: 2pt + seppia),
        )[#text(style: "italic", size: 8.8pt)[#ad-alta-voce]]
      }

      #if retro.len() > 0 {
        sezione("COME TI PORTI IN SCENA")
        for (e, c) in retro { voce(e, c) }
      }

      #if equipaggiamento != none {
        sezione("EQUIPAGGIAMENTO")
        block(width: 100%)[#text(size: 8.6pt)[#equipaggiamento]]
      }

      #if legami.len() > 0 {
        sezione("IL LEGAME COL GRUPPO", nota: "cosa pensi degli altri cinque")
        for (chi, cosa) in legami {
          block(above: 3pt, below: 0pt, width: 100%)[
            #text(font: "Cinzel", size: 7.8pt, weight: 600, fill: rosso)[#chi]
            #h(3pt)
            #text(size: 8.5pt, style: "italic")[#cosa]
          ]
        }
      }

      #if problema != none {
        sezione("IL TUO PROBLEMA")
        block(
          width: 100%, inset: (x: 7pt, y: 5pt),
          stroke: (left: 1.5pt + rgb("#b9a789")),
        )[#text(size: 8.6pt, fill: rgb("#4a3f33"))[#problema]]
      }
    ],

    // ————— destra: quanto fai —————
    block(width: 100%)[
      #sezione("DIFESA")
      #grid(
        columns: (1fr, 1fr), column-gutter: 6pt,
        riquadro("CLASSE ARMATURA", ca, grande: true),
        riquadro("PUNTI FERITA", pf, sotto: pf-dado, grande: true),
      )
      #if ca-dettaglio != none {
        block(above: 3pt, below: 0pt)[#text(size: 7.9pt, fill: seppia)[#ca-dettaglio]]
      }
      #v(4pt)
      #grid(
        columns: (1fr, 1fr, 1fr), column-gutter: 5pt,
        ..ts.map(((e, v)) => riquadro(upper(e), v)),
      )
      #if ts-nota != none {
        block(above: 3pt, below: 0pt)[#text(size: 7.9pt, fill: seppia, style: "italic")[#ts-nota]]
      }

      #sezione("ATTRIBUTI")
      #grid(
        columns: (1fr,) * attributi.len(), column-gutter: 4pt,
        ..attributi.map(((s, p, m)) => attributo(upper(s), p, m)),
      )

      #sezione("ATTACCO")
      #for (riga, rientro) in attacchi {
        block(above: 2.5pt, below: 0pt, inset: (left: if rientro { 10pt } else { 0pt }))[
          #text(size: 8.7pt)[#riga]
        ]
      }
      #v(4pt)
      #grid(
        columns: (1fr,) * calc.max(manovre.len(), 1), column-gutter: 5pt,
        ..manovre.map(((e, v)) => riquadro(upper(e), v)),
      )

      #for (etichetta, corpo) in destra {
        sezione(upper(etichetta))
        block(width: 100%)[#corpo]
      }
    ],
  )

  // ── il piede ──────────────────────────────────────────────────────────────
  #if minuto != none {
    v(7pt)
    block(
      width: 100%, fill: campo, radius: 2pt, stroke: 0.6pt + seppia,
      inset: (x: 9pt, y: 7pt),
    )[
      #text(font: "Cinzel", size: 8.6pt, weight: 600, fill: rosso, tracking: 1pt)[
        COME SI GIOCA IN UN MINUTO
      ]
      #v(2pt)
      #text(size: 9pt)[#minuto]
    ]
  }
  #if piede != "" {
    v(3pt)
    align(center)[#text(font: "Cinzel", size: 6.9pt, fill: seppia, tracking: 1.2pt)[#piede]]
  }
]
