# Guida completa — condividere il materiale (cosa si può fare, cosa no)

> **Cosa copre**: la procedura pratica per ogni modo in cui potresti far
> uscire materiale da questo repo — mandarlo ai tuoi giocatori, stamparlo,
> farlo vedere a un amico, metterlo online, venderlo — con cosa fare prima
> in ciascun caso.
>
> **Base**: [ADR-0005 — confini IP e uso non commerciale](../../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md)
> e il rapporto `09_…/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md`.
>
> ⚠️ **Non è un parere legale.** È l'analisi documentale già fatta nel repo,
> messa in forma operativa. Per un uso commerciale reale serve un avvocato IP.

---

## 0. La risposta in dieci secondi

| Cosa vuoi fare | Si può? | Cosa devi fare prima |
|---|---|---|
| Usarlo **al tuo tavolo** (anche stampato) | ✅ **sì**, liberamente | niente |
| **Mandarlo ai tuoi giocatori** (PDF, chat, cloud privato) | ✅ **sì** | solo il filtro anti-spoiler (§2) |
| **Farlo vedere a un amico DM** / prestarglielo | ✅ sì | nulla di legale; semmai togli gli spoiler del tuo gruppo |
| **Pubblicarlo gratis** (GitHub, forum, Discord pubblico) | 🟡 rischio **basso ma non nullo** | mantieni le note IP e la dicitura non-commerciale (§3) |
| **Venderlo** o usarlo per fare soldi (Patreon a pagamento, PDF a pagamento, merchandising) | ❌ **no, non conforme** allo stato attuale | vedi §4: servirebbero bonifiche pesanti **e** riambientazione |

---

## 1. Perché: i tre corpi di materiale che convivono nel repo

Serve saperlo, perché cambia cosa puoi fare con *quale* file.

| # | Di chi è | Cosa comprende | Effetto |
|---|---|---|---|
| 1 | **Wizards of the Coast** | *Red Hand of Doom* e Forgotten Realms **non-SRD**: Channathgate/Valle del Channath, divinità FR, PNG e trama dell'avventura originale | **blocco assorbente su TUTTO il repo**: da solo basta a escludere l'uso commerciale |
| 2 | **Palio di Siena** (Comune + Consorzio CTPS) | l'arco P2D evoca segni tutelati: titoli araldici, livree, motti, «Piazza il Campo», la geometria della piazza | peggiora **solo** lo scenario commerciale, non quello privato |
| 3 | **Tuo** (l'autore) | testi originali, stemmi SVG, renderer, script, tutta l'automazione | l'**unica** parte che la GPL-3 del repo copre davvero |

Tradotto: anche se domani riscrivessi tutto il Palio da zero, resterebbe il
blocco WotC. **Non è una questione di quanto lavoro ci metti: è di cosa
adatta il materiale.**

---

## 2. Mandare materiale ai tuoi giocatori (il caso di ogni settimana)

Legalmente non c'è nulla da fare: è uso privato. L'unico filtro che conta è
quello **anti-spoiler**, ed è già codificato.

**Procedura:**

1. genera i file col flusso normale:
   ```bash
   python3 scripts/dm.py booklet <manifest-gruppo>.json --pdf      # per il gruppo
   python3 scripts/dm.py booklet <manifest-booklet>.json --pdf-all # hint pg- + schede dm-
   ```
2. manda **solo i file col prefisso `pg-`** (e il file del gruppo). Le schede
   `dm-` restano tue;
3. controlla che nel materiale ✉ non ci siano nome dello scontro, CD, pf,
   clock o deadline — **nemmeno nei piè di pagina** (ADR-0013 §3);
4. un handout a testa, in privato: gli hint personali non vanno nel gruppo
   (perdono valore, ADR-0013 §3-bis/§3-ter).

Dettagli: [GUIDA-BOOKLET-E-PDF](GUIDA-BOOKLET-E-PDF.md) §9 (checklist di consegna).

---

## 3. Pubblicare gratis (GitHub, forum, Discord aperto)

**Stato attuale**: il repo è già pubblicato gratuitamente su GitHub sotto
GPL-3. La posture è **rischio basso ma non nullo**, accettabile finché
restano vere queste tre condizioni:

- [ ] **uso non commerciale dichiarato** — nessuna monetizzazione, diretta o indiretta;
- [ ] **note IP interne mantenute** — la sezione *Licensing Information* del
      README, ADR-0005 e il rapporto restano nel repo e aggiornati;
- [ ] **niente rivendicazione di paternità** su ciò che è di terzi (il
      materiale RHoD/FR resta attribuito a chi appartiene).

**Se pubblichi un singolo pezzo fuori dal repo** (es. posti un booklet su un
forum), aggiungi in calce una nota tipo:

> *Materiale amatoriale non ufficiale, a uso privato e non commerciale.
> Basato su «Red Hand of Doom» e sull'ambientazione Forgotten Realms
> (Wizards of the Coast); meccaniche D&D 3.5 OGL/SRD. Nessuna affiliazione,
> nessuna rivendicazione sui marchi citati.*

**Cosa NON pubblicare**, anche gratis:
- gli export **PCGen** e i sorgenti storici in `Bestiario/pregen-pcgen/` (sono
  materiale di terzi, non tuo);
- testo **verbatim non-SRD** (descrizioni di incantesimi, blocchi
  dell'avventura originale): nel repo è già vietato dalle regole editoriali,
  ma se copi-incolli a mano, controlla;
- immagini di terzi usate come reference (vedi §5).

---

## 4. Vendere / monetizzare — perché oggi è **no**

Non è un «forse»: la verifica ha stabilito che **non può essere confermata**
la conformità. Due blocchi indipendenti, e basterebbe il primo:

1. **WotC/Forgotten Realms non-SRD** — assorbente su tutto il repo;
2. **Palio di Siena** — segni tutelati evocati in modo cumulativo.

Perché sia anche solo discutibile servirebbero **entrambe** queste cose:

- la **checklist di bonifica §7** del rapporto legale: rinominare le
  contrade, cambiare le livree, riscrivere i motti da zero, rimuovere
  «Piazza il Campo», documentare la provenienza delle tavole raster,
  correggere le note IP interne;
- la **riambientazione fuori da Forgotten Realms**, world-neutral / solo SRD.

Oppure, in alternativa al secondo blocco, un contratto di autorizzazione
oneroso col Consorzio.

**Nota pratica**: la bonifica **non è stata eseguita** ed è *gated* su una
tua decisione di perseguire un'edizione commerciale — decisione mai presa.
È tracciata come item opzionale in [`plans/INDEX.md`](../../plans/INDEX.md).
Se un giorno cambi idea: prima l'avvocato, poi il lavoro.

⚠️ **Attenzione alla monetizzazione indiretta**: un Patreon con contenuti
riservati ai paganti, una campagna a pagamento, o merchandising con gli
stemmi rientrano nel caso commerciale anche se «non stai vendendo un PDF».

---

## 5. Immagini e illustrazioni (il punto che si sbaglia più spesso)

Vale per handout, copertine, splash e hero map:

- ✅ **si descrivono le convenzioni** di stile: posa, luce, palette, tecnica,
  epoca («illustrazione dipinta digitale, manuale fantasy classico anni 2000»);
- ❌ **mai** `by <nome>` o «in the style of <artista vivente>»;
- ❌ **mai** usare immagini altrui come style reference o input di training;
- ✅ le tavole che **carichi tu** nel repo: assicurati di averne il diritto e
  annotane la provenienza.

Regola completa: `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md`
(sezione «Confine IP»), che a sua volta discende da ADR-0005.

---

## 6. Casi pratici, risolti

| Situazione | Cosa fare |
|---|---|
| «Mando il booklet del Palio a un amico che vuole giocarlo» | ✅ liberamente. È uso privato: nessun adempimento |
| «Lo stampo in copisteria» | ✅ sì — stai stampando per uso privato |
| «Lo carico su un Drive condiviso col mio gruppo» | ✅ sì, purché il link non sia pubblico e indicizzabile |
| «Lo posto su r/DnD o su un Discord aperto» | 🟡 si può: aggiungi la nota di §3 e non toglierne l'attribuzione |
| «Faccio un video/stream della sessione» | 🟡 uso privato-divulgativo: evita di mostrare a schermo testo verbatim non-SRD |
| «Ci metto una donazione/Patreon» | ❌ diventa commerciale → §4 |
| «Vendo le mappe generate dal renderer» | ❌ il renderer e gli stemmi sono tuoi, ma le mappe **rappresentano** luoghi FR/RHoD → §4 |
| «Uso solo gli script su un'altra campagna mia» | ✅ sì: gli script sono codice tuo, GPL-3. Portali via senza il contenuto di campagna |

---

## 7. Checklist prima di far uscire qualcosa dal repo

- [ ] So in quale caso rientro (§0)
- [ ] Se va ai giocatori: solo file `pg-`, filtro anti-spoiler passato
- [ ] Se va in pubblico: nota di §3 in calce, niente `pregen-pcgen/`, niente verbatim non-SRD
- [ ] Se ci sono illustrazioni: nessun nome di artista vivente, provenienza delle tavole nota
- [ ] Se c'è di mezzo del denaro: **fermati** e leggi §4

---

## 8. Dove sta il resto

| Cosa | Dove |
|---|---|
| La decisione e il perché | [ADR-0005](../../plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md) |
| Il rapporto completo (criticità punto per punto, checklist §7) | `09_…/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md` |
| Licenza del codice e nota IP | [`LICENSE`](../../LICENSE) · [`README.md`](../../README.md) «Licensing Information» |
| Confini IP per le illustrazioni | `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md` |
| Regole anti-spoiler del materiale giocatori | [ADR-0013](../../plans/adr/ADR-0013-standard-generazione-booklet-sessioni.md) §3 |
| Come generare i file da condividere | [GUIDA-BOOKLET-E-PDF](GUIDA-BOOKLET-E-PDF.md) |
