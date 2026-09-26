# Lo sviluppo degli incontri — le domande del developer

Nei colophon di Paizo e WotC il testo passa da due mani: l'editor chiede *«si
capisce?»*, il developer chiede *«si gioca?»*. Il repo ha già l'editor
(`rumblingstone-prosa-documenti`, il lettore a freddo) e i numeri dei mostri
(`npc-villain-boosting`). Questo file tiene le domande del developer che non
stavano da nessuna parte.

Vengono da due manuali che il DM ha portato il 2026-09-26, controllati uno per
uno: il verdetto su ciascun punto, con le fonti e gli errori trovati, è in
`plans/RICERCA-MANUALE-DEL-MASTER-2026-09.md`. Qui resta solo quello che ha
superato il controllo, riscritto per la 3.5.

Si applica a ogni master nuovo o riscritto, **dopo** la checklist del
`SKILL.md` e **prima** della lettura a freddo (`rumblingstone-playtest` §2-bis).

## 1 · La lente dei Tier: chi resta senza niente da fare

In 3.5 le classi non valgono uguale. La classificazione di JaronK (Giant in the
Playground) mette Mago, Chierico e Druido nel Tier 1, e Guerriero, Monaco e
Paladino nel Tier 5: in gioco i primi cambiano la realtà, i secondi fanno bene
una cosa sola. È il *linear warrior, quadratic wizard* dei forum.

Il gruppo di RumblingStone è sbilanciato in basso: Thorik (Guerriero) e Tordek
(Guerriero/Monaco) sono Tier 5, Artemis (Warlock) sta fra 3 e 4 a seconda della
lista, e Hella (Ranger/Druido) porta la magia del Tier 1 dimezzata dal
multiclasse. La campagna compensa già con gli artefatti.

> **La domanda.** In ogni scontro chiave, il PG di Tier più basso ha **una cosa
> che solo lui può fare**? Se il nemico vola, chi non vola e non ha gittata cosa
> fa nei round in quota?

Esempio vero: la seconda lettura di `ARC07-DEF-4` (playtester #35) ha trovato
Tordek senza azioni per tre round contro un drago che resta in quota, e con la
Cintura che rifiuta di attivarsi.

## 2 · Volo e invisibilità, dal 5° livello

Dal 5° livello un gruppo vola e si rende invisibile. Un luogo che non ha una
risposta per questo non esiste più: lo si sorvola.

> **La domanda.** Per ogni luogo sorvegliato: *e se volano? e se sono
> invisibili?* La risposta non annulla il piano. Lo **premia e sposta il
> rischio**: chi vede l'invisibile, chi fiuta, cosa scatta sulla soglia, quanto
> dura la pozione, cosa succede all'atterraggio.

Esempio vero: la variante «dall'alto» di `ARC07-DEF-4` Scena 6 è nata perché il
tavolo l'ha fatto, e il modulo non aveva risposta.

## 3 · I tre tiri salvezza

Un modulo che chiede solo Volontà bersaglia sempre lo stesso PG, e ne lascia
tranquillo un altro.

> **La domanda.** Negli scontri del master, gli effetti con un tiro salvezza
> toccano **Tempra, Riflessi e Volontà**? Se uno manca, è voluto?

Le scene di rito e di dialogo non contano: `DEF-2` e `DEF-3` chiedono solo
Volontà, ed è giusto così.

## 4 · Chi sente il rumore

Un luogo con più gruppi di nemici è un sistema. Se nella stanza A si combatte,
cosa fanno quelli della stanza B? La domanda viene dall'ecologia del dungeon che
la DMG 3.5 raccomanda di pensare.

> **La domanda.** Per ogni scontro: **chi sente**, **in quanti round arriva**, e
> **cosa lo ferma**. Un allarme che il modulo non descrive diventa un allarme
> che il DM inventa.

Esempio vero: la seconda lettura di `ARC07-DEF-4` (playtester #24, 🔴) chiedeva
se lo scontro nella tenda facesse suonare il corno che chiama il drago. Il
modulo non lo diceva.

## 5 · Il boss cambia, non si allunga

Un boss solo contro quattro PG cade in due round per l'economia d'azione, e la
cura è quella di `npc-villain-boosting` Gate 2: prima gli sgherri, poi i numeri.
Quello che si aggiunge qui riguarda la **forma**.

> **La domanda.** Il boss ha almeno **una soglia** (di pf, di round, di evento)
> in cui **cambia tattica o cambia il terreno**? Esempio del repo: Skullcrusher
> in `DEF-4`, che a un terzo dei pf **esita** per la prima volta nella sua
> vita, e da lì o muore o fugge nelle paludi.

⚠️ Dentro l'SRD. Recuperare pf fra una fase e l'altra, avere azioni in più per
round o immunità nuove sono **meccaniche inventate**: si scrivono
`[INFERRED — needs DM confirmation]`, passano dal tetto EL ≤ APL+4 e lasciano il
loro `Boost log:`. I boss pronti dei due manuali (Valerius, Xar'Kesh) non si
importano: i numeri non sono verificati e uno è sbagliato («RD 5/Magia e Adamo»).

## 6 · Lo skill challenge si scrive per intero

Lo skill challenge viene dalla DMG di D&D 4e (2008): tanti successi prima di tre
fallimenti, da 4 a 12 secondo la complessità. In 3.5 non esiste. Nel repo è una
convenzione, e una convenzione mezza scritta genera due regole in conflitto.
Ne ha trovate proprio così la prima lettura di `DEF-4` (lettore #21, 🔴).

> **La domanda.** Il testo dice **chi tira** (tutti, uno, una prova di gruppo
> SRD), **cosa tira** (abilità 3.5: niente Atletica, Intuizione, Percezione,
> Furtività), **cosa vale un successo**, **quanti ne servono** e **cosa costa
> ogni fallimento**? Il fallimento costa, e non ferma: è la regola dei «modi di
> fallimento» già misurata da `misura_craft`.

Un solo posto per la regola. Se compare anche nella Quick-Reference o in
un'appendice, dice la stessa cosa.

## 7 · Chi si diverte in questa scena

*Robin's Laws of Good Game Mastering* (Robin D. Laws, 2002) distingue sette
modi di stare al tavolo: chi ottimizza, chi vuole menare, il tattico, il
casuale, lo specialista, l'interprete e il narratore.

Per il gruppo di RumblingStone valgono i **profili veri** di
`rumblingstone-campaign/references/campaign-dm-strategy.md`, che sono più
precisi di qualunque tipologia. I sette modi servono dove il gruppo non si
conosce: gli stand-alone e i moduli per un gruppo nuovo.

> **La domanda** (stand-alone e gruppi nuovi). Fra le scene del modulo, ognuno
> dei sette modi trova almeno **una** scena fatta per lui?
