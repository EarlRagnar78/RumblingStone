# ADR-0005 — Confini IP e uso non commerciale del repo

**Stato**: accettata
**Data**: 2026-07-19
**Decisione-fonte**: verifica legale/IP dell'arco Palio di Channathgate (PR #47, 2026-07-19; rapporto `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md`, datato 2026-07-18)

## Contesto

Il repo mescola tre corpi di proprietà intellettuale di terzi che nessuna
licenza dell'autore può sanare:

1. **Wizards of the Coast** — materiale *Red Hand of Doom* e *Forgotten
   Realms* non-SRD (Channathgate/Channath Vale, divinità FR, PNG e trama
   dell'avventura originale). È un blocco **assorbente per tutto il repo**.
2. **Palio di Siena** — l'arco P2D evoca in modo cumulativo i segni tutelati
   dal Regolamento comunale e dal Consorzio per la Tutela del Palio (CTPS):
   titoli araldici ufficiali riprodotti alla lettera, 8/8 livree identiche,
   motti dichiarati "originali" ma in realtà parafrasi riconoscibili, il
   toponimo "Piazza il Campo" e la geometria a nove spicchi nella tavola
   raster.
3. **Contenuto proprio dell'autore** (testi, stemmi SVG originali, renderer,
   script) — l'unica parte che la GPL-3 del repo può effettivamente coprire.

Era stata posta la domanda se i file «possono essere usati per fini
commerciali senza problemi». La verifica ha stabilito che **non può essere
confermato**.

## Decisione

Il repo è e resta **a uso privato / non commerciale**. La posture per
scenario d'uso è:

- **Uso privato al tavolo** → OK.
- **Pubblicazione gratuita su GitHub** (stato attuale) → rischio basso ma
  non nullo; accettabile finché restano le note IP interne e l'uso non
  commerciale dichiarato.
- **Uso commerciale** (vendita del modulo, merchandising, loghi) → **NON
  conforme** senza (a) la checklist di bonifica §7 del rapporto **e**
  (b) la riambientazione fuori da Forgotten Realms/WotC, **oppure** un
  contratto di autorizzazione oneroso con il CTPS.

La checklist di bonifica §7 (rinominare le contrade, cambiare livree,
riscrivere i motti da zero, rimuovere "Piazza il Campo", riambientare
world-neutral/SRD-only, documentare la provenienza delle tavole raster,
correggere le note IP interne che affermano motti "originali") **non si
esegue ora**: è interamente *gated* su una decisione del DM di perseguire
un'edizione commerciale, decisione **non presa**. Resta tracciata come
item opzionale in `plans/INDEX.md`.

Questa è un'analisi documentale di conformità, **non un parere legale
professionale**: un uso commerciale reale richiederebbe comunque un
avvocato IP.

## Conseguenze

- Chiarito, una volta per tutte, perché il repo non è commercializzabile
  allo stato: il blocco WotC/FR da solo è sufficiente.
- Ogni nuovo contenuto dell'arco Palio va aggiunto sapendo che aumentare
  l'evocazione dei segni senesi peggiora solo lo scenario commerciale, non
  quello privato/gratuito attuale.
- Va corretta la nota IP interna che dichiara i motti "originali" (sono
  parafrasi): è un debito documentale, non un blocco.
- La provenienza/licenza delle tavole PNG "fornite dal DM" va documentata
  prima di qualunque uso pubblico oltre a quello attuale.
- Da rivisitare **solo se** il DM decide di puntare a un'edizione
  pubblicabile/commerciale: allora si apre un piano di bonifica dai §6-§7
  del rapporto.
