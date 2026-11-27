# Perché il materiale del repo si condivide in modi diversi

> Forma: **spiegazione** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)). I tre corpi di materiale che convivono nel repo e perché ognuno ha regole sue; cosa fare caso per caso sta nella guida. Nato il 2026-11-10 dalle sezioni di spiegazione di [GUIDA-CONDIVISIONE-IP](../how-to/GUIDA-CONDIVISIONE-IP.md). Le sezioni tengono il numero che avevano lì, così un rimando scritto prima («GUIDA-CONDIVISIONE-IP §N») resta vero: nella guida, al posto della sezione, c'è un rimando a questo file.

---

## 1. Perché: i tre corpi di materiale che convivono nel repo

Serve saperlo, perché cambia cosa puoi fare con *quale* file.

| # | Di chi è | Cosa comprende | Effetto |
|---|---|---|---|
| 1 | **Wizards of the Coast** | *Red Hand of Doom* e Forgotten Realms **non-SRD**: Channathgate/Valle del Channath, divinità FR, PNG e trama dell'avventura originale | **blocco assorbente su TUTTO il repo**: da solo basta a escludere l'uso commerciale |
| 2 | **Palio di Siena** (Comune + Consorzio CTPS) | l'arco P2D evoca segni tutelati: titoli araldici, livree, motti, «Piazza il Campo», la geometria della piazza | peggiora **solo** lo scenario commerciale, non quello privato |
| 3 | **Tuo** (l'autore) | testi originali, stemmi SVG, renderer, script, tutta l'automazione | l'**unica** parte che una licenza tua può coprire davvero |

Tradotto: anche se domani riscrivessi tutto il Palio da zero, resterebbe il
blocco WotC. **Conta di cosa adatti il materiale, non quanto lavoro
ci metti.**

### 1-bis. Le due licenze del repo, e le tre cose che NON coprono

Dal 2026-09-02 il repo ha **due licenze**, perché è per tre quarti prosa e per un
quarto strumenti, e una licenza sola ne sbagliava una
([ADR-0029](../../plans/adr/ADR-0029-licenza-doppia-testo-e-script.md), pagina
intera in [`LICENSES.md`](../../LICENSES.md)):

| Cosa | Licenza |
|---|---|
| **Il testo** — avventure, canone, guide, piani, ADR, skill, tavole | **CC BY-NC-SA 4.0** ([`LICENSE`](../../LICENSE)) |
| **Gli strumenti** — tutto `scripts/` | **MIT** ([`scripts/LICENSE`](../../scripts/LICENSE)) |

Nel dubbio: **se lo legge un essere umano al tavolo è testo; se lo esegue una
macchina è strumento.**

Perché due. Il file di licenza e questa guida **si contraddicevano**: qui c'è
scritto «uso non commerciale», e la GPL-3 che il repo aveva prima *garantisce
espressamente* il diritto di vendere copie. In un contenzioso conta il file.

⚠️ **Tre cose che quelle due licenze non coprono**, e ignorarle è il modo di
trasformare una licenza in un problema:

1. **Il contenuto SRD resta Open Game Content sotto OGL 1.0a**, non sotto CC.
   Statblocchi, incantesimi, classi e oggetti derivati dall'SRD 3.5 sono OGC, e
   **chi ridistribuisce materiale che ne contiene deve accompagnarlo con la
   Sezione 15** dell'OGL. Non ti riguarda finché il repo resta privato: ti
   riguarda **nel momento in cui qualcosa esce**, ed è entrato nella checklist della [guida §7](../how-to/GUIDA-CONDIVISIONE-IP.md#7-checklist-prima-di-far-uscire-qualcosa-dal-repo).
2. **I marchi altrui non si licenziano perché si nominano.** *Forgotten Realms*
   non diventa tuo da dare mettendolo sotto CC — vedi la riga 1 della tabella qui
   sopra, che prevale su tutto.
3. **MIT su `scripts/` non copre `scripts/typst/packages/`**: quello è codice di
   terzi (`droplet`, MIT · `in-dexter`, Apache-2.0) con la propria licenza.

E soprattutto: **la [guida](../how-to/GUIDA-CONDIVISIONE-IP.md) prevale sulla licenza.** Una licenza dice cosa
possono fare gli altri con ciò che pubblichi; il [§7 della guida](../how-to/GUIDA-CONDIVISIONE-IP.md#7-checklist-prima-di-far-uscire-qualcosa-dal-repo) dice **se e cosa**
pubblichi. Sono due domande diverse, e la seconda viene prima.
