# Misure sintattiche con spaCy

Prova del 2026-10-22, seguito della §3 di
[RICERCA-QUALITA-MISURABILE-2026-10](../../../RICERCA-QUALITA-MISURABILE-2026-10.md):
le misure che chiedono un parser a dipendenze, fatte con spaCy 3.8.16 e
`it_core_news_md` (CC BY-NC-SA 3.0, uso non commerciale, fuori dal repo).
Lo script è [`scripts/misura_sintassi.py`](../../../../scripts/misura_sintassi.py).

| File | Cosa contiene | Come si rifà |
|---|---|---|
| `CALIBRAZIONE-SINTASSI.txt` | ogni misura sulle 38 coppie votate | `python3 plans/esperimenti/qualita-misurabile-2026-10-22/sintassi/calibra_sintassi.py plans/esperimenti/qualita-misurabile-2026-10-22/COPPIE-VOTATE.json` |
| `BASE-ARC07-ARC08.json` | i cinque master ARC07-DEF e gli otto file di ARC-08 con read-aloud, box per box | `python3 scripts/misura_sintassi.py --json --per-box` |
| `RIASSUNTO-BASE-ARC07-ARC08.txt` | medie per file, box con più calchi, box oltre i due livelli | `python3 scripts/misura_sintassi.py` |

## La calibrazione

Una sola misura si allontana dal caso: **`livelli_max`**, la catena più lunga
di subordinate nel testo, è più alta nella versione vincente 11 volte su 12
(p 0,006). Con quattordici misure provate la soglia corretta di Bonferroni è
0,0036, quindi non è una prova. Nove delle dodici coppie vengono dal giro 2,
dove la riscrittura spezzava le frasi, e in sette la vincente ha anche più
parole (in cinque di oltre il 10%).
Si legge come un indizio: il DM non premia la paratassi spezzata, e tiene una
o due subordinate quando ci sono. Nessuna frase delle 76 versioni supera i due
livelli, quindi la norma di `read-aloud-adulti.md` §1.2 non è in gioco.

I calchi sono quasi sempre pari (33-37 coppie su 38): le riscritture non li
toccavano, e i box votati ne hanno pochi.

## La precisione dei calchi, letta a mano

Quindici rilievi presi a passo fisso (indici 0, 4, 7 … 50) dai 54 della base.
«Vero» vuol dire che la norma di `italiano-nativo.md` §1 chiederebbe di
riscriverlo.

| # | Dove | Tipo | Rilievo | Esito | Perché |
|---|---|---|---|---|---|
| 1 | DEF-1:418 | soggetto preverbale | «Un rombo basso sale dal pavimento» | vero | «Dal pavimento sale un rombo basso» |
| 2 | DEF-1:1707 | soggetto preverbale | «Una fenditura si apre lungo la parete» | vero | «Lungo la parete si apre una fenditura» |
| 3 | DEF-2:515 | pronome | «mentre voi la riportate indietro» | falso | contrasto con «la parete la disegna» |
| 4 | DEF-3:1049 | pronome | «Poi lei inspira» | falso | ri-ancora il soggetto dopo «il Cuore» (§1.4) |
| 5 | DEF-3:1151 | pronome | «che lui non sa ancora leggere» | falso | due soggetti di terza persona, serve |
| 6 | DEF-4:721 | stare + gerundio | «perché sta già parlando» | vero | la norma chiede il presente; aspetto legittimo, caso al limite |
| 7 | DEF-4:2152 | pronome | «Tu ne hai due» | falso | contrasto nel dialogo |
| 8 | ARC08-01:1350 | pronome | «qualcosa che loro non hanno» | falso | contrasto noi/loro |
| 9 | ARC08-01:1434 | soggetto preverbale | «Un suono di corno echeggia» | vero | «Echeggia tre volte un corno» |
| 10 | ARC08-01:1823 | stare + gerundio | «dove Re Thorek sta dirigendo» | vero | «dove Re Thorek dirige» |
| 11 | ARC08-01:2412 | soggetto preverbale | «quattro figure emergono dal metallo» | vero | il soggetto nuovo va prima dei due punti che lo elencano |
| 12 | ARC08-01:2875 | soggetto preverbale | «Un gufo più piccolo degli altri si stacca» | vero | al limite: posporlo spezza la coordinata |
| 13 | ARC08-01:3275 | pronome | «Voi, Rumbling Stones, avete fatto» | falso | vocativo nel discorso del Re |
| 14 | Cerimonia:42 | pronome | «Voi non siete nani della mia stirpe» | falso | anafora retorica |
| 15 | Cerimonia:42 | pronome | «Voi siete tornati» | falso | stessa anafora, contrasto con «Io» |

**Precisione: 7 su 15 (47%).** Per tipo: soggetto preverbale 5 su 5,
stare + gerundio 2 su 2, pronome soggetto **0 su 8**. Fuori campione, i due
soli rilievi di aggettivo complesso della base sono errori del parser
(«lontanissimo» preso per aggettivo di «cubo», una relativa letta come
anteposta): 0 su 2.

Conseguenza nello script: il totale `calchi` somma soggetto preverbale,
aggettivo complesso e stare + gerundio; il pronome soggetto si stampa a parte
e non va trattato come difetto. Il campione è piccolo: 5 su 5 dice che il
rilevatore del soggetto preverbale non è rumore, non che sbaglia mai.

## Limiti

- `rip_fra_box%` cresce col numero dei box del file: si confronta un master
  con la sua versione precedente, non con un altro master.
- Il lemmatizzatore di `it_core_news_md` sbaglia molti passati remoti
  irregolari: lo script li riconosce anche dalla forma.
- Il modello `md` è il più piccolo che ha un parser utile; `lg` o un modello
  transformer non si scaricano da qui (Hugging Face è bloccato dal proxy).
