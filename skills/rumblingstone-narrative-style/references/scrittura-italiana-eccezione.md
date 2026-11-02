# La skill esterna scrittura-italiana, quando serve

**Cos'è.** [scrittura-italiana](https://github.com/hypnosdesign/claude-skill-scrittura-italiana)
è una skill editoriale per l'italiano, pubblicata dall'utente GitHub hypnosdesign. Si
fonda su Mortara Garavelli, Serianni e Giunta e copre punteggiatura,
coesione, chiarezza e i tic della prosa generata. Licenza **CC BY-SA 4.0**.
Commit verificato: `e397599` del 2026-10-12.

**Perché è un'eccezione e non una norma.** Il 2026-10-21 il giocatore di
Artemis non ha capito il contratto del Seme letto a voce. Riscritto con e
senza questa skill, il DM ha scelto alla cieca la versione che la usava, e
l'indice Gulpease era salito da 67,1 a 72,6 (70,0 senza). Era però una
coppia sola, e ADR-0093 vuole 14 coppie su 20 prima di cambiare uno standard
([ADR-0097](../../../plans/adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md)).
Prova e misure in `plans/esperimenti/prova-scrittura-italiana-2026-10-21/`.

## Quando si apre

Si apre in tre casi, e solo in quelli:

1. **un documento in gioco fatto di regole**: contratto, patto, statuto,
   regolamento di gara, clausole di un artefatto. È il caso che l'ha portata;
2. **un testo che il tavolo ha detto di non aver capito**, al tavolo o al
   collaudo (`rumblingstone-playtest`);
3. **un box con l'indice Gulpease sotto 60** in `misura_craft --stile`,
   prima di riscriverlo.

Per tutto il resto bastano le norme di questa skill. Caricarla sempre
sarebbe il danno che [ADR-0058](../../../plans/adr/ADR-0058-orchestrazione-a-strati-delle-skill.md)
descrive: due fonti sullo stesso italiano danno un testo che sbaglia in tutti
e due i modi.

## Come si usa

Il testo della skill **non entra nel repo**: è CC BY-SA, e copiarne righe
in `references/` porterebbe la stessa licenza su quelle righe. Si clona in
una cartella di lavoro, fuori dal repo, al commit verificato:

```bash
git clone https://github.com/hypnosdesign/claude-skill-scrittura-italiana "$SCRATCH/si"
git -C "$SCRATCH/si" checkout e397599
```

Si leggono, prima di scrivere: `SKILL.md`; `references/spiegare-con-chiarezza.md`
(§5 il termine tecnico, §9 la glossa); `references/retorica-efficacia.md` §4 (i
testi per l'ascolto); `references/coesione-e-connettivi.md`. Il compito, nel
vocabolario della skill, è un «deep rewrite» di un testo che si ascolta.

Un handout scritto **applicando** i suoi criteri non copia il suo testo e
non ne eredita la licenza. Il gate d'uscita resta quello di
`rumblingstone-edizione`.

## Dove vince il repo

La prova del 2026-10-21 ha trovato quattro conflitti. In tutti vince il repo:

| La skill esterna dice | Il repo dice | Vince |
|---|---|---|
| glossa subito il termine tecnico, anche con una parentesi | il documento in gioco non spiega sé stesso, e nel box niente parentesi (`read-aloud-adulti.md` §1) | il repo. La glossa e il nome inglese vanno nel riquadro regole, fuori dalla finzione |
| una serie di frasi brevi è sospetta | al massimo due livelli di subordinate (`read-aloud-adulti.md` §1) | il repo. La coesione la tengono le parole ripetute, che la skill stessa ammette |
| nessun tetto di lunghezza | i tetti del box (`read-aloud-adulti.md` §2) | il repo, salvo un handout che il DM dichiara fuori tetto |
| non togliere fatti | non rivelare ciò che il personaggio non sa | il repo e il canone (`campaign-coherence.md`) |

## Chi la misura

Nessun cancello. L'effetto si vede in due posti: la colonna `Gulp.` di
`misura_craft --stile` e il cieco di `cieco_versioni.py`. Decide il cieco.
