# PIANO — Il box di luogo e l'area chiave: la forma di *Dungeon* nei moduli

> **Cos'è**: l'applicazione editoriale di quello che il DM ha portato il
> 2026-10-01 sul *boxed text* di WotC e Paizo, verificato sulle linee guida di
> *Dungeon* (`RICERCA-STANDARD-PROSA-WOTC-PAIZO` §1.4-1.5). La misura è già
> fatta (lotto F2.10 di PIANO-MISURA-EDITORIALE-STANDARD); qui sta come si
> scrive, con quali template, e dove si applica.
>
> **Stato**: 🟡 B0 fatto, il resto aspetta D1-D6 · **Decisore**: DM ·
> **Si lavora**: in una chat a parte, svincolata da PIANO-AGENT-SKILLS-ESTERNE
> **Gate**: `misura_craft --box`, `componenti.py --check`, `validate_norme_editoriali.py`

---

## 0 · Perché

Il DM, il 2026-10-01: *«sia Wizards of the Coast sia Paizo strutturano
editorialmente i loro moduli […] ecco come dividono i blocchi di testo e come
puoi emulare il loro stile»*, con un modello di stanza e uno di area chiave in
due versioni, 3.5 e PF1e. Poi: *«metti anche le cose decise e misurate […] i
vari template e il modo di descrizione così non sono persi»*.

Il §3 conserva tutto quel materiale, con il verdetto accanto a ogni punto.

## 1 · Cosa ho guardato prima, e cosa questo piano non rifà

`grep` su `plans/` per *keyed*, *area chiave*, *boxed text*, *template di
stanza*: l'unico piano che tocca l'argomento è PIANO-LETTORE, alla F5 («le
stanze in stile *keyed* dell'Abbazia: decidere col DM se ogni stanza vuole un
box»). `campaign/templates/` non ha un template d'area.

Non rifà:

- **la misura**, che è F2.10 di PIANO-MISURA-EDITORIALE-STANDARD (gli
  indicatori `>4 frasi` e `>500 car`, il registro, la ricerca);
- **i master nuovi**, che sono S1-S4 di PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE:
  qui si decide la forma che useranno, non si scrivono;
- **l'Abbazia**, che resta la F5 di PIANO-LETTORE: qui c'è la decisione D5
  su come trattarne le stanze;
- i **master già giocati** di ARC-07: non si riscrivono per questo (D4).

## 2 · Fatto (2026-10-01, PR #188)

| Dove | Cosa |
|---|---|
| `read-aloud-adulti.md` §2-bis | il box di luogo: poche frasi, l'ordine spazio e luce → cosa lo occupa → la cosa strana, nessuna creatura dentro, si ferma prima dell'azione; il box d'area è l'apertura di scena da 8-12 righe; un esempio che passa tutti i rilevatori del repo |
| `rumblingstone-module-standard` §7 | l'area chiave nelle voci di *Dungeon*: read-aloud → Dati per il DM (con la riga SRD degli oggetti) → creature → tattiche → trappole → tesoro → sviluppo → PX ad hoc |
| `misura_craft --box` | due indicatori senza peso, `>4 frasi` e `>500 car`, con quattro test |
| `REGISTRO-NORME-EDITORIALI.md` | tre righe (poche frasi 🟡, niente creature 🔴, l'ordine ⚪) e l'area chiave 🟡 |
| `RICERCA-STANDARD-PROSA-WOTC-PAIZO` | §1.4 le prescrizioni di *Dungeon* dalla fonte; §1.5 il testo del DM verificato riga per riga, lo statblock sbagliato, le misure |

**Le misure di partenza**: 501 box nei file di gioco, mediana 347 caratteri,
122 (24%) oltre i 500 e 28 oltre gli 800. Master DEF di ARC-07: 104 box, 61
oltre le quattro frasi, 27 oltre i 500 caratteri. Abbazia: 11 box, uno oltre le
quattro frasi, nessuno oltre i 500.

## 3 · Il materiale del 2026-10-01, conservato

### 3.1 · Le regole, con il verdetto

| Regola del testo | Verdetto | Nel repo |
|---|---|---|
| **Testo d'introduzione della sezione**, 800-1.200 caratteri, uno o due paragrafi: il clima, la geografia, la storia, la luce; letto una volta, all'inizio di una fase nuova | ⚠️ i caratteri non hanno fonte; *Dungeon* mette luce e porte in un testo **per il DM** | è l'**apertura di scena** (8-12 righe) di `read-aloud-adulti.md` §2; la storia ci entra solo come cosa che si vede (§2-bis) |
| **Box di stanza o scena**, un paragrafo, 3-4 frasi, 300-500 caratteri (circa 350-450) | 🟢 le frasi hanno fonte; ⚠️ i caratteri no | §2-bis; misura `>4 frasi`, `>500 car`; D1 |
| **Ordine visivo**: la prima frase dà dimensioni e luce, la seconda l'arredo principale, la terza il dettaglio strano o il pericolo | 🟡 pratica di mestiere, nessuna fonte primaria; la **prima metà** contraddice ADR-0014 | §2-bis tiene l'ordine con il **paragone** al posto delle misure; D2 |
| **Niente anticipazioni**: mai «sentite un brivido», «vi guardate intorno stupiti»; solo l'ambiente oggettivo | 🟢 è la norma P1 di *Dungeon* | `misura_craft --p1` |
| **Regola dell'interruzione**: il box si ferma un istante prima dell'azione o dell'iniziativa | 🟢 il repo ce l'ha | congegno «chiusura su decision point» (*Che fate?*) |
| **Perché è lo standard**: si legge in meno di 15 secondi; offre elementi con cui interagire subito; la prima frase dà le misure a chi disegna la mappa | 🟢 le prime due; la terza vale per i **Dati per il DM**, non per la voce | §2-bis, `module-standard` §7 |
| **3.5 o PF1e**: il template 3.5 per chi tiene l'ingombro e le abilità separate (Ascoltare, Osservare), quello PF1e per uno statblock più compatto | ⚪ già deciso | la campagna gira su 3.5, il Drappo su PF1e |

### 3.2 · Il modello di stanza, e la sua versione del repo

Il testo proponeva questo box, con il titolo della stanza in grassetto sopra:

> *Un soffitto a volta crollato si apre verso il cielo notturno in questa
> camera quadrata di quaranta piedi. Al centro, circondata da macerie di marmo,
> si trova una fontana a forma di drago che zampilla un liquido cremisi e
> denso. Tre porte di legno marcio si affacciano sulle pareti, mentre un
> persistente odore di zolfo satura l'aria stagnante.*

Circa 380 caratteri, quattro frasi, tre cose con cui interagire. Contro le
norme del repo inciampa su due punti: «quaranta piedi» (ADR-0014 e unità
imperiali, il repo usa i metri) e «in questa camera», che guarda la stanza da
architetto. La versione del repo, in `read-aloud-adulti.md` §2-bis:

> *La volta è crollata a metà, e dalla breccia scende la luce della luna.
> Fra i blocchi di marmo caduti, una fontana a forma di drago getta un liquido
> rosso e denso che non fa schiuma. Tre porte di legno marcio, una per parete.
> L'aria sa di zolfo.*

244 caratteri, quattro frasi, nessuna misura, nessun rilievo di
`misura_craft` (`--box`, `--p1`, `--metrature`).

### 3.3 · Il template dell'area chiave

Il testo portava un'area chiave completa (un sarcofago, una grata, due ombre).
Ecco la sua struttura, con i numeri **controllati sull'SRD 3.5** il 2026-10-01
(d20srd.org, *Dungeons*, *Climb*, *Shadow*):

| Voce | Nel testo | Verifica |
|---|---|---|
| intestazione | nome della stanza in grassetto | *Dungeon* vuole anche l'**EL** nell'intestazione |
| dati della stanza | lato 9 m, soffitto 3 m | 🟢 vanno nei **Dati per il DM** |
| pareti | pietra grezza, Scalare CD 15 | 🟢 SRD: *unworked stone*, Climb DC 15 |
| porta | grata di ferro sbarrata: Spezzare CD 25, Durezza 10, pf 60 | 🟢 SRD: *portcullis, iron*, 5 cm, Durezza 10, pf 60, CD 25 |
| read-aloud | 365 caratteri, tre frasi: il sarcofago con l'effigie, tre torce spente, la grata con catena e lucchetto | 🟢 nessuna creatura dentro, come vuole *Dungeon* |
| creature | «se i PG toccano il sarcofago o la grata, due ombre escono dagli angoli», con statblock | 🔴 **lo statblock è sbagliato**, vedi sotto |
| tattiche | le ombre passano nei muri per non farsi circondare | 🟢 la forma; ⚠️ il talento citato («Furtività Rapida») l'ombra non ce l'ha |
| sviluppo | tre vie: esaminare la catena (Percezione CD 15), aprire il lucchetto (Disattivare Congegni CD 22), riconoscere l'effigie (Conoscenze (Nobiltà) CD 15) | ⚠️ in *Dungeon* lo **Sviluppo** è un'altra cosa (chi sente, resa, cosa cambia dopo); queste sono **vie d'uscita** e stanno nei Dati per il DM. Percezione e Conoscenze (Nobiltà) sono abilità PF1e: in 3.5 sono Cercare od Osservare e Conoscenze (nobiltà e regalità) |
| tesoro | spada lunga +1, 45 mo, due quarzi da 10 mo | 🟢 la forma |

🔴 **Lo statblock delle ombre** mescola 3.5 e PF1e e sbaglia in tutti e due
(tabella completa in `RICERCA-STANDARD-PROSA-WOTC-PAIZO` §1.5): GS 2 invece di
3, CA e talenti sbagliati, DMC 15 invece di 17, pagina 218 invece di 245. Nel
template del repo la creatura **non si trascrive**: *Dungeon* stesso prescrive,
per una creatura non modificata, lo statblock **abbreviato** (nome, quante, pf,
rimando al manuale), e il repo ha il Bestiario.

```markdown
### A3 · La cripta del cavaliere (EL 5)

**Dati per il DM (non da leggere).** 9 × 9 m, soffitto a 3 m, buio. Pareti di
pietra grezza (Scalare CD 15). Grata di ferro: 5 cm; Durezza 10; pf 60; CD per
sfondarla 25. [Scopo della stanza, se il box non lo dice.]

> **Read-aloud (luogo · pilastro lead).** *[Spazio e luce per paragone. Cosa
> lo occupa. Per ultima la cosa strana. Nessuna creatura, nessuna misura.]*

**Creature.** Ombre (2): GS 3; pf 19 ciascuna; statblock nel Bestiario
(`Bestiario/mostri/…`) o SRD «Shadow».

**Tattiche.** [Dal punto di vista del mostro, con le coordinate della mappa.]

**Trappole.** [Statblock della trappola, se c'è.]

**Tesoro.** [Oggetti specifici, con il valore.]

**Sviluppo.** [Chi sente lo scontro e in quanti round arriva; quando i nemici
si arrendono o fuggono; cosa cambia se i PG ripassano.]
```

La versione **PF1e** (per il Drappo e gli stand-alone in PF1e) è la stessa,
con le abilità di PF1e (Percezione, Furtività, Conoscenze (nobiltà)) e la
creatura dal Bestiario PF1e: *Shadow*, GS 3, pf 19, Bestiary p. 245.

## 4 · I lotti

| | Lotto | Dipende da | Cosa produce |
|---|---|---|---|
| ✅ | **B0** · la misura e le norme | — | F2.10 di PIANO-MISURA (PR #188) |
| ⬜ | **B1** · il template in `campaign/templates/` | D6 | `area-chiave-template.md` (3.5) e la variante PF1e, dal §3.3; riga nell'indice dei template, se ce n'è uno |
| ⬜ | **B2** · il tipo del box | D3 | la convenzione `**Read-aloud (tipo · pilastro).**` in `editorial-standards.md`, e `componenti.py --check` che la legge sui master che dichiarano il contratto; sblocca la norma 🔴 «niente creature» (`superficie_norme.py`) |
| ⬜ | **B3** · la soglia pesata | D1, B2 | `≤ 4 frasi` per il box di luogo entra in `punteggio_mqm`, con la riga del registro da 🟡 a 🟢 |
| ⬜ | **B4** · la riga degli oggetti | — | una forma fissa che `componenti.py` riconosce nei Dati per il DM (spessore; Durezza; pf; CD), misurata sui master nuovi |
| ⬜ | **B5** · l'Abbazia | D5, F5 di PIANO-LETTORE | un box di luogo breve per stanza nell'ordine di *Dungeon* |
| ⬜ | **B6** · i master nuovi | B1, B2 | S1-S4 di PIANO-MASTER-DEF nascono con l'area chiave; qui si controlla solo che la usino |

[engine e qualità per lotto: B1 e B4 **M** (inline, un gate dice se è giusto) ·
B2 e B3 **C** (Sonnet, test che mordono) · B5 **K** (tocca uno stand-alone:
Opus, ciclo del master) · B6 **R** (ricognizione sui master nuovi)]

## 5 · Decisioni aperte al DM

<!-- decisioni-dm: BOX-LUOGO -->

| # | Lotto | Domanda |
|---|---|---|
| D1 | B3 | **Il tetto del box di luogo: righe, frasi o caratteri?** Oggi la norma è ≤ 12 righe; *Dungeon* conta le frasi; i 300-500 caratteri non hanno fonte. Proposta: si tiene ≤ 12 righe come norma pesata; **≤ 4 frasi** diventa norma **minore** per il solo box di luogo, pesata quando i box dichiarano il tipo (D3), perché oggi colpirebbe anche le aperture di scena da 8-12 righe, che sono legittime; i caratteri restano un indicatore |
| D2 | B0 | **Le dimensioni nella prima frase del box** («camera quadrata di quaranta piedi»), come nel modello del 2026-10-01, o il paragone di ADR-0014 con le misure nei Dati per il DM? Proposta: resta ADR-0014. Dal modello esterno si prende la struttura (le caratteristiche della stanza fuori dal box), non le misure nella voce |
| D3 | B2 | **Ogni box dichiara il suo tipo?** Per esempio `**Read-aloud (luogo · Salvatore lead).**`, con i tipi luogo, ingresso, round, rivelazione, chiusura. Sblocca la norma «niente creature nel box di luogo» e le soglie per tipo della tabella del §2 di `read-aloud-adulti.md`, che oggi nessuno può misurare. Proposta: sì, sui master nuovi (S1-S4 di PIANO-MASTER-DEF), scritto da chi scrive il box e controllato da `componenti.py`; non sui DEF già giocati |
| D4 | — | **I box già giocati fuori dalle nuove misure**: nei DEF di ARC-07, 27 box oltre i 500 caratteri e 61 oltre le quattro frasi. Proposta: non si toccano, come per D9 di PIANO-LETTORE: si spezzano solo se lo chiedi, e senza cambiare una parola |
| D5 | B5 | **L'Abbazia con le stanze *keyed*** (è la F5 di PIANO-LETTORE, «decidere col DM se ogni stanza vuole un box»). Proposta: sì, un box di luogo breve per stanza nell'ordine di *Dungeon*, quando F5 tocca l'Abbazia; è il banco del repo e già oggi ha 1 box su 11 oltre le quattro frasi |
| D6 | B1 | **Il template d'area va in `campaign/templates/`**, accanto a quelli di sessione e di mappa, in due versioni (3.5 e PF1e)? Proposta: sì, tutte e due, con la creatura sempre come rimando al Bestiario e mai trascritta |

## 6 · Validazione

- ogni lotto: `fase1.py` sui bersagli prima di toccarli (G6), poi
  `misura_craft --box`, `validate_norme_editoriali.py`,
  `superficie_norme.py --check`, `decisioni_dm.py --check`, i test dello
  script toccato
- B5 tocca uno stand-alone: segue i sette passi del ciclo del master
  (ADR-0075), letture a freddo comprese
