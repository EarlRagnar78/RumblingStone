---
name: watabou-generatore
description: Come si pilota il Medieval Fantasy City Generator di Watabou dal container (export, scala, parametri sea/coast, limiti del fiume)
metadata:
  type: reference
  modified: 2026-10-22T11:54:33.285Z
---

Dal 2026-10-22 Jfs ha abilitato watabou.github.io nella rete del container. armoria.herokuapp.com resta bloccato, quindi va abortito con page.route, altrimenti `goto` non finisce mai.

- Si usa Playwright Python (`pip install playwright`) con Chromium /opt/pw-browsers/chromium-1194/chrome-linux/chrome. Si fa `goto(url, wait_until='commit')` dentro `expect_download`: `export=svg|json|png` scarica la pianta appena la scena è pronta.
- La scala: 1 unità del JSON = 1 m.
- La taglia: con le mura, size 21 ≈ 16-19 ha e size 34-36 ≈ 50 ha. Senza mura, size 60-63 dà circa 145-165 ha di quartieri (somma dei poligoni `districts`).
- coast vale 1 se non lo si mette, quindi serve `coast=0` esplicito. `sea` è in radianti, in senso orario da est: -1.571 è il nord, 3.1416 l'ovest. Il generatore legge anche `name`, `population`, `urban_castle`, `greens`, `hub` e `style`.
- Con `river=1` il fiume passa sempre in mezzo alla città: l'acqua su un lato solo si fa con la costa, che non ha la riva opposta. Il rilievo non c'è.
- `scripts/watabou_citta.py` non accetta `sea` e `name`.
- Piante e schede in /mnt/project-files/mappe-valle-2026-10-22/watabou/. Collegato a [[mappe-scala-reale]].
