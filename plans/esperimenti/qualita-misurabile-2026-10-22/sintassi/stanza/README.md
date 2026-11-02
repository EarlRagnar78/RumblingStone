# Stanza contro spaCy sulle misure sintattiche

Prova del 2026-10-22. Domanda: il parser di Stanza (Stanford, Apache 2.0)
rende le misure di [`scripts/misura_sintassi.py`](../../../../../scripts/misura_sintassi.py)
più affidabili di spaCy `it_core_news_md`? Se sì, entra come backend facoltativo.

**Esito: no.** Stanza non migliora né la precisione dei calchi in modo
apprezzabile né la calibrazione sui voti del DM, e costa da 50 a 100 volte il
tempo più PyTorch. `misura_sintassi.py` resta com'è, solo con spaCy.

## Come è fatta

Stanza entra attraverso `spacy-stanza`, che trasforma la sua analisi in un Doc
di spaCy: i rilevatori di `misura_sintassi` sono gli stessi e cambia solo il
parser. Due varianti di Stanza 1.15: la standard (`combined_charlm`) e quella
con transformer (`default_accurate`, ELECTRA italiano di dbmdz). I modelli
stanno in `~/.cache/stanza` e `~/.cache/huggingface`, mai nel repo.

| File | Cosa contiene | Come si rifà |
|---|---|---|
| `coppie_giro7f.py`, `COPPIE-7F.json` | le 16 coppie decise del voto cieco del lotto 7f (13 V/N, 3 F/O); con le 38 di `COPPIE-VOTATE.json` fanno 54 (la B04, pari, resta fuori) | `python3 .../stanza/coppie_giro7f.py > COPPIE-7F.json` |
| `confronta.py` | rilievi sulla base ARC-07/ARC-08 e calibrazione, per ogni parser | `python3 .../stanza/confronta.py base > RILIEVI-BASE.json`; `... coppie COPPIE-VOTATE.json COPPIE-7F.json` |
| `RILIEVI-BASE.json`, `RILIEVI-BASE-ELECTRA.json` | ogni rilievo, parser per parser | sopra; per ELECTRA `HF_HUB_DISABLE_XET=1 STANZA_PACKAGE=default_accurate BACKEND=stanza` |
| `CALIBRAZIONE-54.txt`, `CALIBRAZIONE-54-ELECTRA.txt` | le misure sulle 54 coppie | sopra |

Dietro il proxy del container `HF_HUB_DISABLE_XET=1` è obbligatorio: il
protocollo Xet di Hugging Face passa da `cas-server.xethub.hf.co`, che è chiuso.

## 1. I calchi sulla base ARC-07/ARC-08 (13 file)

I tre rilevatori che entrano nel totale `calchi` (soggetto preverbale,
aggettivo complesso, stare + gerundio):

| | spaCy md | Stanza | Stanza ELECTRA |
|---|---|---|---|
| rilievi | 30 | 31 | 32 |
| in comune con spaCy | — | 26 | 26 |
| solo suoi, veri a una lettura | 0 su 4 | 2 su 5 | 2 su 6 |
| tempo sui 13 file (4 core, CPU) | **1,8 s** | 93 s | 183 s |

Le 26 in comune comprendono i sette rilievi già letti a mano nel README di
`sintassi/` (5 soggetti preverbali e 2 stare + gerundio, tutti veri).
Le differenze, lette una per una:

| Parser | Dove | Rilievo | Esito | Perché |
|---|---|---|---|---|
| solo spaCy | DEF-1:669 | «dalle ferite pendono» | falso | «ferite» presa per soggetto; è il falso che ha fatto perdere B01 nel giro 7f |
| solo spaCy | DEF-1:517 | «lontanissimo … un cubo» (agg. complesso) | falso | già noto; ha fatto perdere B02 nel giro 7f |
| solo spaCy | ARC08-01:2730 | «la melodia: fiera e furiosa, echeggia» | falso | soggetto definito e già tema |
| solo spaCy | ARC08-01:3059 | «che brillano di luce divina, scudi» | falso | già noto |
| solo Stanza | ARC08-01:3217 | «un silenzio surreale scende sul campo» | **vero** | «scende sul campo un silenzio surreale» |
| solo Stanza | DEF-3:1065 | «o sto ancora sognando?» | **vero** (al limite) | stare + gerundio che spaCy perde per l'avverbio in mezzo; nel dialogo l'aspetto è legittimo |
| solo Stanza | DEF-3:1269 | «due pietre su tre brillano» | falso | le pietre della Corona sono tema noto |
| solo Stanza | Cerimonia:42 | «se mai un nano del nostro Pugno cadrà» | falso | condizionale, il soggetto è il fuoco |
| solo Stanza | ARC08-01:3143 | «un ultimo, disperato grido» | falso | coppia di aggettivi anteposti, italiano letterario normale |
| solo ELECTRA | DEF-1:859 | «alta come tre nani, una madre» | falso | predicativo anteposto, scelta di stile |

Conto onesto: Stanza toglie i quattro falsi di spaCy (fra cui i due che nel
giro 7f hanno fatto perdere B01 e B02) e ne aggiunge tre suoi, più due veri.
Se le 26 comuni sono tutte vere, la precisione passa da circa 26 su 30 (87%) a
28 su 31 (90%): due rilievi di differenza, dentro il rumore di un campione
così piccolo. ELECTRA trova gli stessi soggetti preverbali di Stanza standard e
un falso in più.

## 2. La calibrazione sulle 54 coppie votate

Nessuna misura passa la soglia di Bonferroni (0,0036 per quattordici misure)
con nessun parser. Le righe che contano:

| Misura | spaCy | Stanza | ELECTRA |
|---|---|---|---|
| `livelli_max` più alto nella vincente | 15 a 5, p 0,041 | 12 a 5, p 0,143 | 13 a 6, p 0,167 |
| `rip_interna%` più alta nella vincente | 21 a 9, p 0,043 | 20 a 10, p 0,099 | 21 a 8, p 0,024 |
| `calchi` più alti nella **vincente** | 8 a 4 | 5 a 3 | 6 a 3 |

L'indizio di prima (il DM non premia la paratassi spezzata) con spaCy regge
anche sulle 54 coppie, con Stanza si indebolisce. I calchi, con tutti e tre
i parser, sono più spesso nella versione che **vince**: come misura del voto
non servono, servono solo come elenco di punti da leggere.

## 3. Aggiunta del 2026-10-23: spaCy `it_core_news_lg`, a rete aperta

Domanda di Jfs: con la rete sbloccata cambia qualcosa? Stanza ed ELECTRA
erano già stati scaricati e provati a rete aperta, quindi su di loro no.
L'unico modello mai provato era spaCy `lg` (stessa licenza del `md`, fuori dal
repo; si scarica da GitHub, non da Hugging Face). UDPipe resta irraggiungibile
(lindat.mff.cuni.cz 403). File: `RILIEVI-BASE-LG.json`, `CALIBRAZIONE-54-LG.txt`,
`BACKEND=spacy-lg`.

| | spaCy md | spaCy lg |
|---|---|---|
| calchi | 30 | 29 |
| in comune | — | 23 |
| solo suoi, veri a una lettura | 4 o 5 su 7 (veri persi da lg, vedi sotto) | 2 su 6 |
| tempo sui 13 file | 1,8 s | 3,1 s |

`lg` **perde cinque soggetti preverbali** che `md` trova, fra cui due già
letti come veri («Un rombo basso sale», «quattro eroi apparvero») e altri tre
dello stesso tipo («fenomeni innaturali cominciano», «un altro vecchio
resta», «un nano veterano … cade»). Tiene invece i due falsi di `md` che
contano («dalle ferite pendono» di B01, «fiera e furiosa, echeggia») e ne
aggiunge di suoi: «Gorthak il Trifronte avanza» (nome proprio, tema noto),
«Dal Tempio interno emerge» (il soggetto è già dopo il verbo), «se mai un
nano del nostro Pugno cadrà», «Poi, lontanissima, la voce» (aggettivo
complesso). Veri in più: «un silenzio surreale scende», «sto ancora sognando».
Toglie i due falsi di aggettivo complesso di `md`.
In calibrazione nessuna misura passa Bonferroni (`livelli_max` p 0,096,
`rip_interna%` p 0,043). **Peggio del `md`**: perde veri e tiene il falso che
ha fatto perdere B01.

## Decisione (ADR breve)

- **Contesto**: spaCy `md` dà falsi rilievi che, riscritti senza controllo,
  hanno perso il voto cieco (B01, B02 nel giro 7f). Hugging Face ora è
  raggiungibile, quindi Stanza e un parser transformer si possono provare.
- **Decisione**: niente backend Stanza in `misura_sintassi.py`. Resta spaCy,
  con la regola già presa nel giro 7f: ogni rilievo si conferma a occhio
  prima di riscrivere.
- **Alternative scartate**: spaCy `lg` (perde cinque soggetti preverbali veri e tiene il falso di B01, provato il 2026-10-23); Stanza standard (precisione +2 rilievi su 31,
  calibrazione più debole, 50 volte più lento, PyTorch); Stanza ELECTRA (come
  la standard, un falso in più, 100 volte più lento); consenso dei due parser
  (rilievo solo se lo vedono entrambi: toglierebbe tutti e sette i falsi delle
  differenze ma perderebbe i due veri, e chiede comunque PyTorch per
  risparmiare la lettura di quattro righe su trenta).
- **Conseguenze**: la pipeline di prosa non guadagna niente cambiando parser;
  il collo di bottiglia è la misura del voto, non la precisione dei rilievi.
- **Da rivedere se**: i rilievi diventano un cancello automatico (allora il
  consenso dei due parser vale il costo), o la base cresce abbastanza da
  rendere i falsi di spaCy un problema di tempo per chi legge.
