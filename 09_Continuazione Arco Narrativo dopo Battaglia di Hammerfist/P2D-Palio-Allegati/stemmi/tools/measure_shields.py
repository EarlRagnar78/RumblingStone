#!/usr/bin/env python3
"""Misura gli stemmi con un vero motore di rendering, invece che a occhio.

    python3 tools/measure_shields.py check              # i testi stanno dentro?
    python3 tools/measure_shields.py check --wide       # ...anche con un font largo?
    python3 tools/measure_shields.py bbox game-icons/*.svg

`check`  verifica su tutti e 16 gli scudi che il motto stia dentro il suo cartiglio e
         che il titolo non esca dalla tela di 200. Esce con codice 1 se qualcosa sfora,
         così si può mettere in CI.
         Con `--wide` forza monospace e letter-spacing: simula un renderer con un font
         molto più largo del nostro. È il test che conta, perché `Georgia` spesso non è
         installata e i ripieghi sono più larghi.

`bbox`   stampa il bounding box reale dei glyph delle icone game-icons, che serve per
         calcolarne scala e posizione dentro lo scudo (vedi PROCEDURA.md §3).

Richiede un Chromium headless: viene cercato in PLAYWRIGHT_BROWSERS_PATH, poi nel PATH.
Serve perché la larghezza di un testo dipende dal font, e l'unico modo onesto di saperla
è chiederla a chi lo disegna — `getBBox()`.
"""
import glob as globmod
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent


def find_chromium() -> str:
    root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    hits = sorted(globmod.glob(f"{root}/chromium-*/chrome-linux/chrome"))
    if hits:
        return hits[-1]
    for name in ("chromium", "chromium-browser", "google-chrome"):
        found = subprocess.run(["which", name], capture_output=True, text=True)
        if found.returncode == 0:
            return found.stdout.strip()
    sys.exit("Chromium non trovato: imposta PLAYWRIGHT_BROWSERS_PATH o installa chromium.")


def run(html: str) -> list:
    """Apre la pagina in headless e riporta il JSON che lo script vi ha stampato."""
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "m.html"
        page.write_text(html)
        out = subprocess.run(
            [find_chromium(), "--headless", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=4000", "--dump-dom", f"file://{page}"],
            capture_output=True, text=True).stdout
    m = re.search(r"@@(\[.*?\])@@", out, re.S)
    if not m:
        sys.exit("il motore di rendering non ha restituito misure — pagina non caricata?")
    return json.loads(m.group(1))


def shields() -> list:
    return ([("faerun", p) for p in sorted(BASE.glob("*.svg"))] +
            [("golarion", p) for p in sorted((BASE / "golarion").glob("*.svg"))])


def cmd_check(wide: bool) -> int:
    css = ('<style>svg text{font-family:monospace!important;letter-spacing:2px!important}</style>'
           if wide else "")
    divs = "".join(f'<div data-k="{s}/{p.name}">{p.read_text()}</div>' for s, p in shields())
    rows = run(f"""<!doctype html><meta charset=utf-8>{css}<body>{divs}<pre id=o></pre>
<script>
const r=[...document.querySelectorAll('div[data-k]')].map(d=>{{
  const s=d.querySelector('svg');
  const rc=[...s.querySelectorAll('rect')].find(x=>x.getAttribute('y')==='182');
  const m=[...s.querySelectorAll('text')].find(x=>x.getAttribute('y')==='200').getBBox();
  const t=[...s.querySelectorAll('text')].find(x=>x.getAttribute('y')==='14').getBBox();
  return {{k:d.dataset.k, b0:+rc.getAttribute('x'), b1:+rc.getAttribute('x')+ +rc.getAttribute('width'),
           m0:+m.x.toFixed(1), m1:+(m.x+m.width).toFixed(1),
           t0:+t.x.toFixed(1), t1:+(t.x+t.width).toFixed(1)}};
}});
document.getElementById('o').textContent='@@'+JSON.stringify(r)+'@@';
</script></body>""")

    bad = 0
    for r in rows:
        fuori_cartiglio = max(r["b0"] - r["m0"], r["m1"] - r["b1"])
        fuori_tela = max(0 - r["t0"], r["t1"] - 200)
        if fuori_cartiglio > 0.05 or fuori_tela > 0.05:
            bad += 1
            print(f"  ✗ {r['k']}: motto fuori dal cartiglio {fuori_cartiglio:+.1f}, "
                  f"titolo fuori dalla tela {fuori_tela:+.1f}")
    etichetta = "font largo forzato" if wide else "font di sistema"
    if bad:
        print(f"✗ {bad}/{len(rows)} scudi sforano ({etichetta})")
        return 1
    print(f"✓ {len(rows)}/{len(rows)} scudi: testi dentro i limiti ({etichetta})")
    return 0


def cmd_bbox(patterns: list) -> int:
    files = [pathlib.Path(f) for pat in patterns for f in sorted(globmod.glob(pat))]
    if not files:
        sys.exit("nessun file corrisponde ai pattern dati")
    items = []
    for f in files:
        ds = re.findall(r'<path\b[^>]*\sd="([^"]+)"', f.read_text())
        glyph = [d for d in ds if d.strip() != "M0 0h512v512H0z"]   # via il riquadro di fondo
        if len(glyph) != 1:
            print(f"  ! {f.name}: {len(glyph)} glyph invece di 1 — salto")
            continue
        items.append((f.name, glyph[0]))
    svgs = "".join(f'<svg viewBox="0 0 512 512" data-f="{n}"><path d="{d}"/></svg>'
                   for n, d in items)
    rows = run(f"""<!doctype html><meta charset=utf-8><body>{svgs}<pre id=o></pre>
<script>
const r=[...document.querySelectorAll('svg')].map(s=>{{
  const b=s.querySelector('path').getBBox();
  return {{f:s.dataset.f, x:+b.x.toFixed(1), y:+b.y.toFixed(1),
           w:+b.width.toFixed(1), h:+b.height.toFixed(1)}};
}});
document.getElementById('o').textContent='@@'+JSON.stringify(r)+'@@';
</script></body>""")
    for r in rows:
        print(f"{r['f']:40} x={r['x']:>6} y={r['y']:>6} w={r['w']:>6} h={r['h']:>6}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in ("check", "bbox"):
        sys.exit(__doc__)
    if args[0] == "check":
        sys.exit(cmd_check("--wide" in args))
    sys.exit(cmd_bbox(args[1:] or ["game-icons/*.svg"]))
