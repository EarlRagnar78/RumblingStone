# PIANO — Incantatori memorabili: Mano Rossa e drow di Sonjak

> **Origine**: richiesta DM (2026-08-02). *«Aggiungere fra le file della Mano
> Rossa qualche incantatore forte oltre agli sciamani e ai war adept: un
> generale ogre magi con livelli da elementalista capace di tenere testa al
> gruppo con i loro artefatti, o una combinazione di incantatore e forza bruta
> che sopravviva più di qualche round. Comprimari più brutali, tipo la versione
> sotterranea degli ogre. E per i drow qualche incantatore subdolo in più
> comandato dalla matrona Sonjak.»*
>
> **Stato**: 🟢 eseguito (L1-L5 + **L7 ala orchesca** + **L8 indice fonte
> privata**, 2026-08-02) — **tutto il materiale generato è
> `[INFERRED — needs DM confirmation]`**: sono proposte, non canone. Nessuna
> riga di `campaign/state.md` è stata toccata.

---

## §0 Risposta breve alla domanda del DM

**Sì, si può fare, e l'ogre magi è la scelta giusta** — per una ragione
meccanica precisa, non solo di colore: il suo kit nativo (volo a volontà,
forma gassosa, invisibilità, rigenerazione) è **l'unico modo pulito, dentro
l'SRD, di far sopravvivere un incantatore a Thorik e Tordek per più di due
round**. Non serve inventargli poteri.

**No, però, non basta alzare il GS.** Contro 4 PG di livello 13 con artefatti,
un mostro solo di GS 17 muore comunque nel round 2 se lo si può raggiungere.
La sopravvivenza di un boss incantatore, a questo tavolo, si compra con
**negazione del contatto**, non con punti ferita. Tutto il piano sta in questa
frase.

---

## §1 Cosa minaccia davvero *Il Rumbling Stone* (analisi onesta)

Fonti: `campaign/state.md` §1/§6, `skills/rumblingstone-campaign/references/campaign-party.md`.

| PG | Difese oggi (stato reale al tavolo) | Superficie d'attacco che resta |
|---|---|---|
| **Thorik** | **Mind Blank permanente** + Volontà Adamantina (Rituale 3 della Corona): niente charme, compulsioni, letture del pensiero, divinazioni. RD 5/epico, CA altissima, +2 deflessione | Danno diretto, **illusioni quasi-reali**, effetti d'area senza TS, terreno, RD che la sua ascia non buca |
| **Tordek** | TS da monaco, RD 5/adamantio, Resistenza al fuoco 10, **Ancoraggio della Montagna 2/g** (immune al movimento forzato), lotta i casters | **−2 DES permanente** (Peso del Mondo, 2026-07-31): CA senz'armatura, Riflessi e iniziativa peggiorati. Ancoraggio è **2 volte al giorno**, non sempre |
| **Hella** | Cura, RD 3/—, Res. Freddo 10, rigenerazione su terra, Rinascita Spontanea 1/g | **Vulnerabilità al fuoco ×1,5** (Ibrido Treant). È la falla più grossa e più bella del gruppo |
| **Artemis** | Volo a volontà, Passo d'Ombra, Res. Fuoco 10, Anello | d6 di DV, TS su Tempra il più debole, **tocchi a distanza** (nessun TS), *polvere scintillante* che gli cancella l'invisibilità, dissolvi sull'Anello |
| **Gruppo** | Trinità Divina 1/g (5 round: +4 TS sacri, immunità paura/charme), niente ladro | Nessuna individuazione trappole affidabile; poca AoE; **la Trinità dura 5 round** — se lo scontro ne dura 8, gli ultimi 3 sono nudi |

### Le tre conclusioni che contano

1. **Gli incantatori mentali sono morti come categoria.** Dopo il Rituale 3
   della Corona, ogni villain costruito su *dominare*, *charme*, *suggestione*
   ha metà arsenale spento contro il tank. Chi resta utile: **illusioni
   quasi-reali**, **danni senza tiro salvezza**, **tocchi a distanza**,
   **controllo del terreno**.
2. **Il fuoco è l'asse morale del gruppo.** L'unico modo di spegnere una
   rigenerazione è il fuoco, e il fuoco è il veleno di Hella. Ogni scontro
   costruito su una creatura rigenerante è automaticamente un **Triangolo di
   Rischio**: Tordek e Artemis devono bruciare, Hella deve stare dove non si
   brucia, e la cura arriva da lei.
3. **L'adamantio è il tema nascosto della campagna.** Corona di Adamantio,
   Pelle di Adamantio, Treant Adamantini, Bracieri di adamantio — e **Aegis
   Fang, che adamantina non è**. Un boss con *pelle di pietra* (RD
   10/adamantio) trasforma questa coincidenza in un puzzle: per due round il
   nano che risolve tutto non buca, e a bucare è chi di solito flanchea.

---

## §2 Perché "più GS" non risolve (i numeri)

Formula EL 3.5 (DMG cap. 3, implementata in `scripts/suggest_encounter.py`):
`EL ≈ 2·log2( Σ 2^(GS/2) )`. Tetto della skill di boosting: **EL ≤ APL+4 = 17**.

- Un mostro solo contro 4 PG perde **3:1 sull'economia delle azioni**,
  qualunque sia il GS.
- Un incantatore PNG 3.5 di GS 16 sta **molto sotto** i benchmark PF T1-1 per
  il suo GS (CA 21 contro 31, ~107 pf contro 200, CD 20 contro 24). È un
  difetto strutturale del sistema, non della build: gli slot di uno Stregone 8
  sono quelli e basta (**un solo incantesimo di 4° conosciuto**).
- Quindi: si compensa con **equipaggiamento da tabella PNG** (bastone del
  fuoco, pergamene di *assorbimento vitale*), **due round di preparazione**
  (un caster che si è pre-buffato vale +1/+2 GS effettivi) e **comprimari che
  assorbono azioni**.

### Le quattro leve che funzionano a questo tavolo

| Leva | Come si realizza | Effetto sul tavolo |
|---|---|---|
| **Negazione del contatto** | volo, *velo di dislocamento*, forma gassosa contro la lotta, gittata | il boss agisce 5-6 volte invece di 2 |
| **Danno senza tiro salvezza** | *muro di fuoco*, *assorbimento vitale* (tocco a distanza, 1d4 livelli negativi), *dardo incantato* | aggira i TS altissimi del gruppo |
| **Terreno che divide** | muro di fuoco, *nebbia solida*, chokepoint | separa Hella dai curati: il vero costo |
| **Uscita di scena** | forma gassosa, *porta dimensionale*, *teletrasporto* | il villain torna, e la seconda volta ha imparato |

---

## §3 Il roster proposto (6 schede nuove)

Tutte nel formato standard `Bestiario/`, tutte SRD, tutte flaggate INFERRED.

### Mano Rossa

| Scheda | Cosa fa | GS | File |
|---|---|---|---|
| **Ghaurush «Cenerevento»** — ogre magi / Stregone 8 | Generale elementalista. Vola, taglia il campo col muro di fuoco, *pelle di pietra* (RD 10/adamantio), rigenerazione 5, esce dalla lotta in forma gassosa. **Tratta prima di combattere** | **16** (variante *Advanced* 17) | `Bestiario/villain/Ghaurush_Cenerevento/` (dossier + statblock) |
| **Ogre Frantumapietra** (Barbaro 6) | Comprimario brutale delle gallerie profonde. **Colpo Tremendo**: spedisce un PG Medio a 3 m e prono. Contro-mossa del party: Ancoraggio della Montagna | **9** | `Bestiario/mostri/ogre-frantumapietra-barbaro6-cr9.md` |
| **Ogre Micelio** (Sporeborn, Barbaro 4) | La versione sotterranea e sbagliata: innesto fungino di Sonjak. Ferocia fino a −10 pf, sbuffo di spore (nausea, **non mentale**), berserk 1/10 round, **vulnerabile al fuoco** | **8** | `Bestiario/mostri/ogre-micelio-sporeborn-cr8.md` |

**Perché l'ogre magi e non un mago hobgoblin**: la Mano Rossa ha già i War
Adept KulkorZhul, i chierici Mano del Fato e i warpriest di Tiamat
(`Bestiario/mostri/`). Manca un comandante che sia **incantatore e mole
insieme** e che non creda alla causa. Ghaurush è un appaltatore con quattro
secoli e un registro contabile: dà alla Mano Rossa una faccia che non urla.

### Drow di Sonjak

| Scheda | Cosa fa | GS | File |
|---|---|---|---|
| **Zin'thara Vel'Ryn «la Voce di Ragnatela»** — Illusionista 9 / Danzatrice delle Ombre 2 | L'incantatrice che **resta pericolosa dopo il Mind Blank di Thorik**: ombre quasi-reali che fanno danno anche a chi è blindato contro il mentale. Nascondersi in piena vista, 44 pf, non si fa mai toccare. Ha in mano le prove dei traffici di Sonjak col Collezionista → **ramo giocabile** | **12** | `Bestiario/villain/Zin_thara_Vel_Ryn/` (dossier + statblock) |
| **Drow Trickster Arcano** (Ladro 3 / Mago 5 / Trickster 2) | **Prestidigitazione a distanza**: ruba a 9 metri. Non gli artefatti legati — ma pozioni, bacchette, e **quello che sta negli zaini** | **11** | `Bestiario/mostri/drow-trickster-arcano-cr11.md` |
| **Drow Assassina di Lolth** (Ladro 4 / Assassino 5) | Attacco Mortale CD 19 dopo 3 round di studio, +5d6 furtivo, invisibilità. Progettata per uccidere **PNG alleati**, non PG | **10** | `Bestiario/mostri/drow-assassina-lolth-cr10.md` |

### Combinazioni e EL (già calcolati)

| Incontro | EL | Riga della tabella di taratura |
|---|---|---|
| Ghaurush + 2 Frantumapietra | **16,5** | APL+3/+4 — boss d'arco, può costare un PG |
| Ghaurush *Advanced* da solo | **17** | tetto assoluto (APL+4): solo con via di fuga segnalata |
| Zin'thara + Assassina + Trickster | **14,3** | APL+1/+2 — set-piece della Notte dei Drow |
| Trickster + Assassina | **12,5** | facile in combattimento, **duro nelle conseguenze** |
| 2 Frantumapietra | **11** | scontro standard |
| 3 Ogre Micelio | **11,2** | ondata, con rischio fuoco amico |

---

## §4 Come si incastrano nella campagna

- **Ghaurush** → incontro di viaggio ARC-09 Giorni 33-38, oppure Rethmar Fase
  1. **Non** all'Arco 08: l'avanguardia ha già Grimjaw e Gorthak.
- **Frantumapietra / Micelio** → scorta di Ghaurush; gli Ogre Micelio cadono
  col **Sabotaggio Campi Drow** se i PG lo fanno (`state.md` §0, ARC-09 P3).
- **Zin'thara + le sue due mani** → campi drow, **Notte dei Drow** (Rethmar
  Fase 0), infiltrazione fra i profughi (`state.md` §2.5).
- **Eco già armato che si può far esplodere** (`state.md` §7.E): il Trickster
  Arcano che sfila il **Seme-Mercato di Varis** dallo zaino di Tordek (E-07b).
  Oppure Ghaurush che lo **chiede in pegno** nella trattativa. In entrambi i
  casi il ramo cambia: da usare solo con l'ok esplicito del DM.
- **Ramo nuovo aperto**: Ghaurush e Zin'thara, indipendentemente, hanno **prove
  che Sonjak tratta col Collezionista alle spalle della Mano Rossa**. È il
  primo cuneo giocabile fra le due fazioni nemiche, e i PG possono arrivarci
  da due strade diverse.

---

## §5 Cosa NON ho fatto (decisioni che spettano al DM)

1. **Non ho toccato `campaign/state.md`.** Nessun clock, nessuna riga di
   conoscenza PNG, nessun villain aggiunto: sono proposte. Le righe da
   aggiungere in caso di approvazione sono scritte in fondo a ciascun dossier.
2. **Non ho usato materiale non-SRD.** Il fomoriano (il "vero" ogre deforme
   del Sottosuolo) sarebbe la scelta di colore più ovvia, ma sta su fonti
   private: se il DM lo vuole, si aggiunge come scheda a parte citando
   `[Private source]`, senza riprodurre testo.
   → **Risolto in §6 (lotto L7)**: il DM ha scelto la via degli equivalenti
   SRD. `bruto-deforme-sottosuolo-cr11.md` copre la stessa funzione senza
   toccare la fonte privata.
3. **Non ho potenziato PNG esistenti.** Sonjak resta a GS 13 e Zin'thara le
   sta sotto di proposito.
4. **Non ho inventato poteri.** L'unica capacità non attestata è lo **Sbuffo
   di Spore** dell'Ogre Micelio, derivato dalla riga canonica «Sporeborn» di
   `Armate-CALCOLI-ESERCITI-DINAMICI.md` e flaggata.
5. **Aperto**: se il DM vuole Ghaurush come **incantatore puro e più letale**
   invece che caster-bruto, la strada è Ogre magi + Stregone 10 (GS 18), fuori
   dal tetto EL — accettabile solo come «fuggi o muori» segnalato.

---

## §6 L'ala orchesca — equivalenti SRD (lotto L7, 2026-08-02)

> **Origine**: seconda richiesta DM, stessa giornata. *«Le creature tratte da
> [modulo di fonte privata] sono possenti; anche il mostro finale può essere
> usato come gregario. Non pensi agli incantatori della Mano Rossa?»* — con
> nota successiva sull'esistenza di una web enhancement che ne alza i valori.
>
> **Rotta scelta dal DM**: *equivalenti SRD, senza il libro.* Nessuna
> citazione, nessuna pagina, nessun testo ripreso: solo ruoli ricostruiti da
> SRD 3.5 + template semplici PF1e.

### Le tre constatazioni che hanno guidato il lotto

1. **Il DM ha ragione sul dimensionamento.** Un modulo scritto per la fascia
   4-7 chiude su un GS 8-10. Contro 4 PG di livello 13 quello è il gradino dei
   **comprimari** — la stessa banda dei gregari del lotto L3/L4 (GS 8-11). La
   web enhancement sposta il boss verso GS 12-14, che a questo tavolo è
   **mini-boss**, non carne da macello.
2. **Un boss con un nome usato come gregario anonimo è uno spreco.**
   Numericamente regge; drammaturgicamente brucia una scena. Da qui la scelta
   di dare al pezzo forte di quest'ala un **dossier e un ramo politico**, non
   solo uno statblock.
3. **Il canone era già apparecchiato.** Gli orchi nella Mano Rossa non vanno
   giustificati: `campaign/state.md` §2.2 conta **1.800 ausiliari
   Goblin/Orchi/Worg Riders**, la prima ondata è «450 hobgoblin/orc infantry»
   (`campaign/lore/campaign-history.md`) e il **Generale Grimjaw è un Orog**.
   Esiste già una linea di comando orchesca dentro un'orda hobgoblin — e la
   frattura **Gruumsh / Tiamat** è teologia vera, non un espediente.

### Cosa colma davvero il buco «incantatori»

Il roster orchesco è marziale. L'unico incantatore che porta è il **chierico
di Gruumsh**, ed è esattamente quello che mancava: un **divino**, i cui
strumenti migliori (*muro di lame*, *raggio di luce accecante*, *colonna di
fuoco*) non hanno descrittore mentale e quindi **attraversano il Mind Blank di
Thorik per costruzione**, non per eccezione. Complementare a Ghaurush
(arcano) e Zin'thara (illusioni), non sovrapposto.

### Le tre schede

| Scheda | Cosa fa | GS | File |
|---|---|---|---|
| **Chierico di Gruumsh** (Orco, Chierico 11) | Incantatore divino d'appoggio. *Muro di lame* per tagliare il campo, *raggio di luce accecante* senza TS, *libertà di movimento* contro la lotta di Tordek. Dominî Guerra + Forza | **11** | `Bestiario/mostri/chierico-gruumsh-cr11.md` |
| **Bruto Deforme del Sottosuolo** (Gigante di Pietra deforme, Barbaro 2) | L'equivalente SRD del gigante deforme di fonte privata. Enorme, portata 4,5 m, massi a 55 m, **malocchio** non mentale. Unica scheda del piano **in scala col benchmark** | **11** | `Bestiario/mostri/bruto-deforme-sottosuolo-cr11.md` |
| **Ushgar «Occhio Reso»** (Orco, Barbaro 13) | Mini-boss e **leva politica**. Carica 24 m, tre attacchi da 1d12+14, Combattere alla Cieca. Vuole terra scritta, non bottino — e il solo che possa firmargliela è Thorik, che per farlo paga la penale del §5 | **13** | `Bestiario/villain/Ushgar_Occhio_Reso/` (dossier + statblock) |

### EL calcolati (script `combine_el`, formula DMG 3.5)

| Incontro | EL |
|---|---|
| Ushgar + Chierico + Bruto Deforme | **15,0** |
| Ushgar + Chierico di Gruumsh | **14,2** |
| Chierico + Bruto Deforme | **13,0** |
| Ushgar da solo | **13,0** |
| Ushgar + Ghaurush (chiusura d'ala in una scena) | **16,9** — tetto APL+4 |

### Il ramo politico (la parte che vale più degli statblock)

Ushgar può **togliere gli ausiliari orcheschi dalla prima ondata** a Rethmar.
Non cambia bandiera: arriva tardi, sbaglia guado, si perde. Il prezzo è un
atto scritto che assegni terra ai suoi, firmato da un nome che i nani
riconoscano — cioè **Thorik**, che in `campaign/state.md` §5 ha già una
promessa aperta con Re Thorek Hammerfist la cui penale è la **perdita dello
status di Custode Eterno**. Il ramo si incastra su un debito che esisteva già.

Uscita laterale documentata nel dossier: **Hella** che non si oppone
all'insediamento invece di Thorik che firma — costa meno al nano e apre un
problema col Cerchio Sacro.

### Vincoli rispettati

- **Zero materiale di fonte privata.** Nessuna citazione, nessuna pagina,
  nessun nome ripreso. La nota di licenza è nel dossier del bruto: le web
  enhancement WotC erano PDF **gratuiti**, e gratuito non è libero — restano
  sotto `AGENTS.md` regola 2 come il modulo base.
- **Dominî di Gruumsh**: usati solo quelli **presenti nell'SRD** (Guerra,
  Forza; disponibili anche Caos e Male). **Caverna** e **Orco** sono di fonte
  privata e sono stati lasciati fuori di proposito.
- **Una sola capacità non attestata** in tutto il lotto: il **Malocchio** del
  Bruto Deforme (*infliggere maledizione* 1/giorno), flaggata nello statblock
  e rimovibile senza toccare il GS.
- **`Boost log:`** presente su entrambe le schede costruite per derivazione,
  con benchmark PF T1-1 dichiarato **anche dove sta sotto** (il chierico) e
  con la mitigazione scritta (comporre l'incontro, non ritoccare i numeri).
- **Ripetizione sorvegliata**: la RD 10/adamantio del chierico (via *pelle di
  pietra*) è lo stesso puzzle di Ghaurush. Nota esplicita in scheda: se i due
  compaiono nello stesso arco, sostituire il dominio Forza con Male.

---

## §7 Indice d'uso della fonte privata (lotto L8, 2026-08-02)

> **Origine**: il DM ha caricato il PDF — la web enhancement *Tougher Sons of
> Gruumsh* (Eric Cagle, 2006, 9 pagine) — chiedendo se contenga «mostri
> interessanti da citare come forza bruta».
>
> Con il file effettivamente in mano, la rotta **(a) citazione con pagina**
> diventa praticabile: è il precedente `[Private — Red Hand of Doom, p.X]` già
> in uso. Prodotto: `Bestiario/INDICE-SONS-OF-GRUUMSH-FONTE-PRIVATA.md`.

### La correzione che il documento impone

Nel dialogo che ha aperto L7 avevo stimato che un boss potenziato «atterra
nella fascia GS 12-14, cioè mini-boss e non carne da macello». **I numeri
stampati dicono il contrario e danno ragione al DM.** Il pezzo grosso del
documento, **Thrull** (p. 9, GS dichiarato **14 o 16**), ha **118 pf e CA 13**,
perché lo si incontra senza corazza addosso. Contro 4 PG di livello 13 è un
gregario con un titolo.

| | pf | attesi (PF T1-1) | rapporto |
|---|---|---|---|
| Thrull come GS 14 | 118 | 200 | **59%** |
| Thrull come GS 16 | 118 | 240 | **49%** |
| Daazlag GS 14 | 67 | 200 | **34%** |
| Jurrg GS 11 | 41 | 145 | **28%** |

Non è un difetto del prodotto: serve un gruppo di **8° livello**, ed è lo
stesso fenomeno già descritto in §2 — il GS nominale di un PNG 3.5 costruito
su livelli di classe diverge dalla sua sopravvivenza reale, e diverge sempre
di più salendo di grado.

### Cosa è utilizzabile

- **Senza interventi**, come gregari: **Dregthaug** (viverna avanzata GS 10, il
  meglio proporzionato del file: 84% del pf attesi), **Vhazror** (GS 11, 107
  pf, alabarda con portata e Sventrare Superiore — il miglior gregario del
  documento), **ambush drake** in branco da 3-4 (GS 9), **Naazlog** (GS 9).
- **Con un intervento**: **Thrull** — la correzione è narrativa prima che
  meccanica (dargli l'armatura già addosso: CA 13 → 24) e poi, se serve,
  template PF1e *Advanced*; oppure lasciarlo GS 14 e circondarlo (Thrull + 2
  Vhazror = **EL 15,5**, sotto il tetto). **Daazlag** solo come infiltrato
  contro PNG, mai in campo aperto. **Jurrg** da rifare sul telaio: la sua
  lista (*muro di fuoco*, *fulmine*, *raggio rovente*, *oscurità profonda*) è
  il brief giusto, ma 41 pf e CA 13 non arrivano al primo turno — lo slot è
  già coperto da `chierico-gruumsh-cr11.md`.
- **Fuori**: Zhentarim (fazione non in campagna), geografia Thar / Mare della
  Luna.

### Il ritrovamento che vale più delle schede

Tre dei quattro pezzi grossi (**Thrull**, **Daazlag**, **Naazlog**) sono
**orog**. Il **Generale Grimjaw è già un orog** in questa campagna: il
documento gli consegna uno **stato maggiore pronto** — un guerriero anziano,
un furtivo, un picchiatore, stessa razza e stessa cecità alla luce. E si
incastra con L7: **Ushgar comanda orchi di superficie e vuole terra scritta,
Grimjaw comanda orog e ha scelto il grado**. La faglia dell'ala orchesca ha
adesso due schieramenti con facce diverse.

### Errata trovati leggendo

- **p. 9, Thrull**: i valori di CA con armatura risultano invertiti fra
  vestizione affrettata e completa. Il calcolo da zero dà **24**.
- **p. 8, Naazlog**: velocità stampata «30 ft. (40 squares)» — sono **6**.

### Vincolo di licenza, verificato sul documento

La web enhancement dichiara **in prima pagina** di non contenere Open Game
Content e di non essere riproducibile senza permesso scritto. Conferma la
nota già messa a verbale in L7: **gratuito non è libero**. L'indice contiene
solo puntatori (nome, pagina, GS), misure usate come metro di paragone e
ricette di adattamento originali. **Nessuno statblock trascritto.**

---

## Checklist lotti

- [x] **L1** — Analisi difese/superfici del party e leve di design (§1-§2)
- [x] **L2** — Ghaurush: statblock GS 16 + variante *Advanced* GS 17 + dossier
- [x] **L3** — Comprimari ogre sotterranei: Frantumapietra GS 9, Micelio GS 8
- [x] **L4** — Drow subdoli: Zin'thara GS 12 (statblock + dossier), Trickster
      Arcano GS 11, Assassina di Lolth GS 10
- [x] **L5** — Catalogo rigenerato (`build_monster_catalog.py`) e
      `validate_bestiario.py` verde
- [ ] **L6** — *(gated su DM)* approvazione: flag INFERRED → ACCEPTED, righe
      in `state.md` §3/§4, assegnazione token
- [x] **L7** — Ala orchesca in equivalenti SRD (§6): Chierico di Gruumsh GS 11,
      Bruto Deforme del Sottosuolo GS 11, Ushgar «Occhio Reso» GS 13
      (statblock + dossier + ramo politico su `state.md` §5)
- [x] **L8** — Indice d'uso della fonte privata (§7): roster valutato scheda
      per scheda contro il benchmark, ricette di adattamento, errata, aggancio
      orog ↔ Grimjaw — `Bestiario/INDICE-SONS-OF-GRUUMSH-FONTE-PRIVATA.md`
