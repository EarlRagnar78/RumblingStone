# ADR-0029 — Licenza doppia: CC BY-NC-SA sul testo, MIT sugli script

**Stato**: accettata
**Data**: 2026-09-02
**Decisione-fonte**: DM, lotto F3 di
[PIANO-CHIUSURA-CATENA-EDITORIALE](../PIANO-CHIUSURA-CATENA-EDITORIALE.md) —
*«Doppia: CC BY-NC-SA sul testo, MIT sugli script»*
**Tocca il perimetro di**: [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) (che **non** viene
allargato: vedi §3) · **Nasce da**: P19 dell'audit dell'Abbazia — *«`LICENSE`
GPL-3.0 su un'opera testuale»*

## Contesto

Il repo aveva **un solo `LICENSE`, GPL-3.0**. È una licenza scritta per il
software, applicata a un repo che per tre quarti è prosa: avventure, canone,
guide, ADR, skill. Ne seguivano difetti opposti.

**Sul testo, la GPL non dice la cosa che il repo dichiara da sempre.** ADR-0005
stabilisce che il materiale è a **uso non commerciale**; la GPL, al contrario,
*garantisce* espressamente il diritto di vendere copie. Il file di licenza e la
postura del progetto si contraddicevano, e a contare in un contenzioso è il file.

**Sugli script, la GPL è più restrittiva del necessario e scoraggia il riuso.**
`validate_prosa.py`, `export_booklet_typst.py`, `import_html_module.py` sono utili
a chiunque tenga una campagna in italiano. Sotto GPL, un DM che ne prende uno
eredita la licenza sul proprio progetto. Non è ciò che vogliamo da uno strumento.

## Decisione

**Due licenze, con un taglio dichiarato.**

| Cosa | Licenza | File |
|---|---|---|
| Il **testo** — avventure, canone, guide, piani, ADR, skill, tavole e immagini prodotte qui | **CC BY-NC-SA 4.0** | `LICENSE` |
| Gli **strumenti** — tutto `scripts/` | **MIT** | `scripts/LICENSE` |

La regola per decidere, quando un file è di confine: **se lo legge un essere
umano al tavolo è testo; se lo esegue una macchina è strumento.**

I testi delle due licenze sono presi **verbatim** da
[`spdx/license-list-data`](https://github.com/spdx/license-list-data) al commit
`a522a89` — non riscritti a memoria, che su un testo legale è il modo di
introdurre una differenza che nessuno rileggerà mai.

`LICENSES.md` in radice è la pagina che spiega il taglio e, soprattutto, i **tre
limiti** qui sotto.

### 1. Il contenuto SRD resta sotto OGL 1.0a

⚠️ **È la parte che una licenza doppia rischia di far dimenticare.** Statblocchi,
incantesimi, classi e oggetti derivati dall'**SRD 3.5** sono **Open Game
Content**: restano governati dalla **OGL 1.0a**, non da CC BY-NC-SA. Le due cose
convivono perché riguardano **porzioni diverse** del materiale — la prosa
originale è nostra, ciò che deriva dall'SRD è OGC.

Chi ridistribuisce materiale che contiene OGC deve accompagnarlo con la
**Sezione 15** dell'OGL. Non è un adempimento nostro finché il repo resta a uso
privato: lo diventa nel momento in cui qualcosa esce, ed **entra nel cancello
d'uscita** di `docs/guides/GUIDA-CONDIVISIONE-IP.md` §7.

### 2. I marchi altrui non si licenziano perché si nominano

*Forgotten Realms*, *D&D* e i nomi dei Reami restano di Wizards of the Coast.
Metterli sotto CC BY-NC-SA non li rende nostri da dare.

### 3. Questo ADR **non** allarga ADR-0005

CC BY-NC-SA concede a terzi la rielaborazione non commerciale. ADR-0005 resta la
regola più stretta, e **prevale**: il cancello d'uscita §7 va passato *prima* che
qualcosa lasci il repo, licenza o non licenza. Una licenza dice cosa possono fare
gli altri con ciò che pubblichiamo; ADR-0005 dice **se e cosa** pubblichiamo. Sono
due domande diverse e la seconda viene prima.

### 4. Il vendoring tiene la sua licenza

MIT su `scripts/` **non si applica a `scripts/typst/packages/`**: `droplet` (MIT)
e `in-dexter` (Apache-2.0) hanno il proprio `LICENSE`, integro, come vuole
ADR-0026. Idem `skills/rumblingstone-debugging/` (MIT, ADR-0010).

## Conseguenze

**Buone.**
- Il file di licenza e la postura del progetto dicono **la stessa cosa**. Prima
  si contraddicevano.
- Gli strumenti diventano riusabili senza contaminare chi li prende.
- L'obbligo OGL è scritto dove si guarda, invece di vivere in una skill.

**Il prezzo, dichiarato.**
- **È una rilicenziazione.** È legittima perché il titolare è l'autore, ma la
  storia git conserva i commit sotto GPL-3.0: chi avesse preso una copia prima di
  oggi tiene i diritti che la GPL gli dava su quella copia. Non si revoca a
  posteriori, e non ci proviamo.
- **CC BY-NC-SA è più difficile da comporre di CC BY**: *NonCommercial* e
  *ShareAlike* insieme rendono il testo incompatibile con parecchie raccolte di
  terzi. È il costo scelto di proposito: qui vale più la coerenza con ADR-0005
  della componibilità.
- **«Non commerciale» non è definito con precisione** in CC 4.0 — è
  *«principalmente diretto a o rivolto verso un vantaggio commerciale o un
  compenso monetario»*. Per il caso limite (una campagna su Patreon, un tavolo a
  pagamento) la risposta **non** sta nella licenza: sta in ADR-0005 e nel
  cancello §7, ed è **fermarsi e chiedere**.

**Cosa NON decide.** Non decide l'edizione commerciale, che resta non presa
(ADR-0005). Non tocca le licenze dei pesi dei generatori d'immagini
([ADR-0019](ADR-0019-licenza-dei-pesi-non-del-software.md)), che sono una
questione a sé e più stretta.
