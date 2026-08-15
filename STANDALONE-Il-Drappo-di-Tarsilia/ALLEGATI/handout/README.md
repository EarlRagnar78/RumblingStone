# I prop — i quattro fogli che passano di mano

> **La regola** ([ADR-0018](../../../plans/adr/ADR-0018-apparato-uso-obbligatorio.md)):
> ogni documento che la fiction consegna **si consegna davvero**. Un foglio che passa
> di mano al tavolo vale dieci minuti di descrizione.

| # | Prop | Quando si dà | A chi |
|---|---|---|---|
| **1** | **Il contratto di Vesca** | G1 §3, quando Vesca lo posa **piegato in tre** | al tavolo — e possono non aprirlo mai |
| **2** | **La pagina del registro dei morti** | G1, appena comincia | al giocatore di **Melchio**, e resta suo |
| **3** | **La ricevuta del mediatore** | G2 §6, se perquisiscono Sfregio | a chi lo perquisisce |
| **4** | **Il decreto** | G1 §1 | si **appende**, non si dà: al muro o al centro del tavolo, per tre serate |

## Come si stampano

Sono sorgenti **Homebrewery V3**. Due strade:

```bash
# A · il fascicolo completo, HTML + PDF (una pagina per prop)
cd ../../homebrew
python3 ../../scripts/build_booklet_html.py DRAPPO-PROP.manifest.json --format both
python3 ../../scripts/export_booklet_pdf.py DRAPPO-PROP.manifest.json --all
```

**B** · incolla il singolo `.hb.md` in [Homebrewery](https://homebrewery.naturalcrit.com/)
se vuoi ritoccarlo prima di stampare.

**Carta**: se ne hai, usa un foglio più pesante del normale per il **contratto** e per
il **decreto**. È l'unica spesa del modulo e si sente.

## Le note che non si stampano

Ogni prop ha in coda un blocco `<!-- NOTA PER IL DM -->` con: **come si usa**, **cosa
nessuno nota** e **cosa succede se lo firmano, lo stracciano o lo perdono**. Il
generatore del booklet lo tratta come commento e non lo impagina — ma se stampi il
`.hb.md` grezzo, taglia l'ultima pagina.

## Perché sono quattro e non dieci

Perché quattro si consegnano davvero. Un modulo con dodici handout ne fa arrivare al
tavolo tre, e il DM si sente in colpa per gli altri nove.

## Una cosa da non fare

**Non ritirarli mai.** Un prop consegnato resta ai giocatori anche a modulo finito: è
la parte che si portano a casa.
