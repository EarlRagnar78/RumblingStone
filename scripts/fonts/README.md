# I caratteri del repo

Tutti i font che servono a **stampare** e a **leggere a schermo** stanno qui, nel
repo, con la loro licenza accanto. È il motivo per cui esiste la catena di stampa
([ADR-0020](../../plans/adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md)):
un PDF che usa i font della macchina che l'ha compilato **cambia faccia** su
un'altra macchina, e un manuale si riconosce dal carattere prima che dal testo.

## Cosa c'è

| File | Uso | Licenza | Provenienza |
|---|---|---|---|
| `EBGaramond[wght].ttf` · `EBGaramond-Italic[wght].ttf` | testo corrente | OFL 1.1 (`OFL-EBGaramond.txt`) | progetto EB Garamond (Georg Duffner, Octavio Pardo) |
| `Cinzel[wght].ttf` | titoli, medaglioni, frontespizio | OFL 1.1 (`OFL-Cinzel.txt`) | Natanael Gama |
| `Inconsolata[wdth,wght].ttf` | blocchi di codice e griglie monospaziate | OFL 1.1 (`OFL-Inconsolata.txt`) | Raph Levien — `google/fonts`, `ofl/inconsolata/` |
| `web/*.woff2` | la catena HTML, incorporati in base64 nel CSS | come sopra | derivati dai `.ttf` qui accanto |

Prima del 2026-08-22 il monospazio **non** era qui: il tema chiedeva
`DejaVu Sans Mono` e se lo faceva dare dal sistema — cioè esattamente il difetto
che ADR-0020 diceva di aver chiuso, sopravvissuto nei blocchi di codice.

## Come si rigenerano i `web/*.woff2`

I `.woff2` sono **artefatti**: si rigenerano dai `.ttf` di questa cartella, non
si modificano a mano (ADR-0003). Servono solo alla catena HTML, dove un `.ttf`
variabile da 800 KB in base64 peserebbe più del booklet.

```bash
pip install fonttools brotli     # solo per rigenerarli, non per usarli
python3 - <<'PY'
from fontTools import subset
from pathlib import Path
src = Path("scripts/fonts"); web = src / "web"; web.mkdir(exist_ok=True)
UNI = ("U+0020-007E,U+00A0-00FF,U+0100-017F,U+0192,U+02C6,U+02DC,U+2000-206F,"
       "U+2070-209F,U+20A0-20BF,U+2122,U+2190-2193,U+2212,U+25A0-25FF,"
       "U+2660-2667,U+2713,U+2716,U+2726,U+2727,U+2736,U+273F,U+2765,U+2766,"
       "U+00A7,U+00B0,U+00B7,U+2020,U+2021,U+2022,U+2026")
for f, nome in (("EBGaramond[wght].ttf", "ebgaramond"),
                ("EBGaramond-Italic[wght].ttf", "ebgaramond-italic"),
                ("Cinzel[wght].ttf", "cinzel")):
    subset.main([str(src / f), f"--unicodes={UNI}", "--flavor=woff2",
                 f"--output-file={web / (nome + '.woff2')}",
                 "--layout-features=*", "--no-hinting", "--desubroutinize",
                 "--drop-tables+=DSIG"])
PY
```

Il sottoinsieme è **latino esteso** (l'italiano ha le accentate) più la
punteggiatura tipografica e i pochi simboli che i temi usano davvero (`§ ⬦ ❦ ·
† ‡ …`). Emoji e simboli fuori elenco restano al font di sistema: in un booklet
sono decorazione, non testo.

## Aggiungere un carattere

1. **Solo licenze verificabili** e solo font che si possono ridistribuire: OFL,
   Apache 2.0, licenze equivalenti. La licenza si legge, non si eredita da questo
   file ([ADR-0019](../../plans/adr/ADR-0019-licenza-dei-pesi-non-del-software.md)
   dice la stessa cosa per i pesi dei modelli).
2. Il testo della licenza entra **qui accanto**, col nome del font.
3. La riga della tabella qui sopra si aggiorna nello stesso commit.
4. Il nome del font si dichiara **una volta sola**, in cima a
   `scripts/typst/tema-rumblingstone.typ` (`SERIF`, `TITOLI`, `MONO`): un nome di
   font sparso in venti punti è un font che un giorno resta indietro in diciannove.
