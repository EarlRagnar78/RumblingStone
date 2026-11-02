# ADR-0097 — La skill esterna scrittura-italiana entra come eccezione, non come norma

**Stato**: accettata il 2026-10-21 (la prova su DEF-4 e DEF-5 ha passato il cieco del DM: nuova 10, vecchia 3, soglia 10 su 13)
**Data**: 2026-10-21
**Decisione-fonte**: il DM, il 2026-10-21 («il contratto del seme è risultato incomprensibile da capire in italiano per Artemis […] non è che in rete c'è una skill filologica che migliora la scrittura in italiano?»; dopo il cieco: «X.md si capisce meglio oggettivamente»; poi «preferirei inserire la nuova skill come eccezione inserendo la reference quando necessario […] fai una prova di riscrittura sul def 4 e def 5 dell'arc07»)

## Contesto

Al tavolo il giocatore di Artemis non ha capito il contratto del Seme
(ARC07-DEF-1 §6-bis), letto a voce. Le norme di `rumblingstone-narrative-style`
non segnalavano niente: zero tic, zero rilievi di `validate_prosa`.

In rete l'unica skill seria per l'italiano è
[scrittura-italiana](https://github.com/hypnosdesign/claude-skill-scrittura-italiana)
(CC BY-SA 4.0, 75 commit, una batteria di prove). Due agenti hanno riscritto
il contratto dallo stesso brief, uno con le sole norme del repo e uno con in
più la skill esterna. Il DM ha scelto alla cieca la seconda versione.
`misura_craft` non distingueva le due versioni. L'unica misura che le separava
era l'indice di leggibilità Gulpease: 67,1 l'originale, 70,0 la versione con
le sole norme del repo, 72,6 quella con la skill esterna.
Dati in `/mnt/project-files/contratto-seme/`.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Eccezione con una reference che dice quando aprirla**, testo esterno fuori dal repo, prova su DEF-4 e DEF-5 | si usa dove ha vinto; la licenza non tocca il repo; una prova vera prima di allargarla | chi scrive deve clonarla; tre casi d'uso da riconoscere a mano |
| Copiarla nel repo come skill vendorizzata, sul modello di `rumblingstone-debugging` (ADR-0010) | sempre disponibile, versione fissa | CC BY-SA: la copia resta CC BY-SA e ogni sua modifica pure; diciannovesima skill da orchestrare |
| Farla norma per tutta la prosa di gioco | il cieco l'ha preferita | una coppia sola contro i 14 su 20 di ADR-0093; due fonti sullo stesso italiano (ADR-0058) |
| Non usarla | nessun costo | il problema del contratto resta senza strumento |

## Decisione

1. **La reference `rumblingstone-narrative-style/references/scrittura-italiana-eccezione.md`**
   dice i tre casi in cui la skill esterna si apre: un documento in gioco fatto
   di regole, un testo che il tavolo non ha capito, un box con Gulpease sotto
   60. Fuori da quei casi non si carica.
2. **Il testo della skill non entra nel repo.** Si clona fuori, al commit
   verificato `e397599`. Le parti in cui la skill e il repo si contraddicono
   sono nella reference, e vince il repo.
3. **`misura_craft --stile` ha una colonna `Gulp.`**, l'indice Gulpease dei
   box. È un indicatore senza peso, come le altre colonne di `--stile`.
4. **La prova** riscrive 35 box di DEF-4 e DEF-5 con la reference: tutti
   quelli sopra le 25 parole, tranne gli 8 già votati al giro 3. Si misura con
   `cieco_versioni.py` secondo ADR-0093. Campione e misure stanno in
   `plans/esperimenti/prova-scrittura-italiana-2026-10-21/`.

## Esito della prova

Il 2026-10-21 il DM ha votato le 13 coppie alla cieca. La versione con la
reference ha vinto 10 a 3, alla soglia esatta (Wilson 95% da 0,50 a 0,92).
Le tre vecchie vincitrici (Scena 3, la targa di bronzo; le due del «grigio»
di Zog'tar) sono state rimesse intatte. Il margine è il minimo che la soglia
consente, quindi una seconda prova che perda basta a riaprire la decisione.

## Conseguenze

- Il contratto del Seme ha due handout, uno per il DM e uno per il giocatore,
  scritti con la skill esterna. Il thread dei PNG li porta in ARC-07.
- Se la prova vince il cieco (14 su 20, riproporzionato), questo ADR diventa
  accettata. Il DM decide allora se allargare i casi della reference o farne
  una norma. Se la prova perde, la reference resta per i soli documenti in
  gioco fatti di regole, dove ha vinto.

**Da rivedere se**: la skill esterna cambia licenza o sparisce; una seconda
prova contraddice la prima; il Gulpease sale senza che il DM preferisca i
testi (allora la colonna premia le frasi corte e basta).
