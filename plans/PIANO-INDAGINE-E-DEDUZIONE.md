# PIANO — Indagine e deduzione: il nono pilastro

> **Cos'è**: la copertura che mancava al repo per far girare **casi
> investigativi** — misteri, enigmi, indizi che sembrano slegati e che a un
> certo punto si ricompongono in un disegno solo. Nasce da una richiesta del
> DM (2026-08-25) dopo un audit delle skill: il Trono di Spade era già il
> pilastro 5 di `rumblingstone-narrative-style`, ma della deduzione — del
> caso ricomposto — non c'era **niente** in tutto il repo.
>
> **Vincolo che ha dato forma a tutto**: questo tavolo ha personaggi che non
> hanno speso un solo punto in abilità che non massimizzino il danno. Un caso
> che si apre solo con Cercare e Sapienza li esclude. Il piano non risolve il
> problema abbassando le CD: cambia l'unità di misura dell'indizio.

**Stato**: 🟢 eseguito (2026-08-25) · **Decisione-fonte**: richiesta DM in
sessione · **ADR**: [ADR-0022](adr/ADR-0022-competenza-guadagnata-sul-campo.md)

---

## 1. Il divario, misurato

Audit di `skills/` al 2026-08-25 (`grep -ril "sherlock\|indagine\|deduzion\|tre indizi"`):

| Cosa serve a un caso | Dov'era | Verdetto |
|---|---|---|
| Politica grigia, fazioni, tradimenti telegrafati | `style-pillars.md` §5 (Trono di Spade) | ✅ già coperto, e già filtrato dallo splatter (`Avoid` §5) |
| Infiltrazione procedurale, il piano messo sotto stress | `style-pillars.md` §4 (Andor) | ✅ coperto — ma è **come si esegue** un colpo, non come si **legge** una scena |
| Struttura a tappe, fazioni intrecciate | `quest-design-baldur.md` | ✅ coperto |
| **Indizi posati, letti, ricomposti** | — | ❌ **assente** |
| **Prove per chi non ha gradi** | — | ❌ assente |
| **Premio alla testa spremuta** | — | ❌ assente (l'XP premia il combattimento) |
| **Vicolo cieco: cosa fa il DM quando nessuno trova niente** | — | ❌ assente |
| **Enigmi, e il congegno che spiega tutto** | — | ❌ assente |

L'unica riga d'aggancio era il mixer di `SKILL.md:80`
(`Investigation / infiltration | Andor | BG1–2`), che descrive un'altra
cosa: in Andor l'informazione ce l'hai già e il problema è **usarla**; in un
caso l'informazione è sparsa e il climax è **cognitivo**.

## 2. Le quattro decisioni di design

1. **L'indizio non è una CD, è un nodo a tre strati**: *Fatto* (cosa c'è,
   oggettivo), *Lettura* (cosa significa), *Nome* (chi/che cosa
   precisamente). **Il Fatto non si tira mai**: fallire toglie la lettura,
   mai il fatto. È la regola dei tre indizi resa nativa, e chiude il vicolo
   cieco per costruzione invece che per pezza del DM.
2. **Sei porte sullo stesso nodo**: ogni nodo dichiara almeno **tre** delle
   sei caratteristiche come vie d'accesso, e almeno una dev'essere fisica
   (FOR/DES/COS). È la clausola che obbliga chi scrive il modulo a dare
   qualcosa da fare al guerriero, e si controlla a macchina.
3. **Due monete, non una**: *Acume* (per-PG, si spende nel caso, si azzera)
   premia l'intuizione nel momento in cui avviene; *Perizia* (permanente,
   tetto 1 grado/PG/livello) fa sì che un gruppo senza ladro sopperisca nel
   tempo senza sostituire il ladro. Vedi ADR-0022.
4. **L'enigma non è un lucchetto**: risolto dà un vantaggio, non risolto
   non ferma il caso: lo rende più caro. Un enigma che blocca è una trappola
   per il DM, non per i giocatori.

## 3. Lotti

- [x] **I1 — Piano + ADR.** Questo file + `ADR-0022` (competenza guadagnata
      sul campo: la regola della casa che tocca le schede).
      *Accettazione*: l'ADR dichiara tetto, interazione col massimale 3.5
      (livello+3 / (livello+3)/2) e cosa succede al salire di livello.
- [x] **I2 — Skill `rumblingstone-indagine`.** SKILL.md + quattro reference:
      nodi e sei porte · registro e ricompense · ricomposizione · congegno ed
      enigmi. *Accettazione*: `validate_skills.py` verde, nessuna reference
      orfana, confini con le altre skill dichiarati (ADR-0008 §1).
- [x] **I3 — Nono pilastro in `rumblingstone-narrative-style`.** «Il caso
      ricomposto» come pilastro 9 in `style-pillars.md`, righe nuove nel
      mixer, puntatore in Domain→File. *Accettazione*: il pilastro dichiara
      *take* / *avoid* / *in play* come gli altri otto, e **non nomina il
      film** (non-negoziabile 4: le fonti sono mestiere, non marchi).
- [x] **I7 — Il congegno non è un power-up** (correzione DM, 2026-08-25,
      stessa giornata). Rilievo: *«non deve migliorare il combattimento ma
      rivelare cose che all'inizio non hanno senso… come un gran
      prestigiatore si devono vedere solo alcune parti e non il tutto
      subito… ma bisogna dosare per non creare assuefazione»*.
      Il §5 consegnato in I2 («chi ha indagato bene combatte meglio, i punti
      deboli si sbloccano») **era** il power-up: un boss con dei passaggi.
      Riscritto `congegno-e-enigmi.md` da 6 a 10 sezioni: **§4 la regia del
      prestigiatore** (effetto prima della causa, pezzo fuori contesto,
      misdirection onesta, il congegno intero visto una volta sola),
      **§5 l'innesco in piena vista** (dato gratis e senza tiro, dentro una
      scena che parla d'altro, con due uscite entrambe scenografiche — e
      **se nessuno lo tocca scatta davvero**), **§6 il congegno nell'agenda
      dei villain** (lo cercano / ce l'hanno e non sanno usarlo / lo stanno
      modificando per uno scopo ignoto) più il villain che **lo sa usare** e
      da cui si impara guardando, **§8 il terzo attore** (la macchina è la
      stanza: agisce a scadenza su tutti, si aziona da entrambe le parti,
      cambia quali tattiche funzionano), **§9 il dosaggio**.
      *Accettazione*: nessuna ricompensa dell'indagine espressa come bonus
      numerico; il §9 dichiara una frequenza per ogni elemento.
- [x] **I8 — Il congegno è una famiglia su sei** (correzione DM 2026-08-26:
      *«ma questa skill aggiunge anche misteri non banali da risolvere, non
      solo congegni?»*). Difetto verificato sul testo: l'impianto era già
      indipendente dal congegno, ma **lo scheletro del caso lo rendeva
      obbligatorio** (`IL CONGEGNO` come prima riga del template). Chi
      apriva la skill per scrivere un «chi è stato» non trovava la sua
      casella. Nuovo `references/famiglie-di-caso.md` con sei famiglie
      (chi è stato · impostore · cospirazione · sparizione · accusa falsa ·
      congegno), ciascuna con domanda, firma negli indizi, chiave tipica,
      errore da evitare e come finisce; scheletro generalizzato a
      `IL SEGRETO` / `CHI CI GUADAGNA`, `L'INNESCO` reso opzionale fuori
      dalla famiglia 6. *Accettazione*: lo scheletro regge un caso senza
      alcuna macchina, e il congegno dichiara di essere una famiglia su sei.
- [x] **I9 — Varietà fra gli archi** (richiesta DM 2026-08-26: *«garantire
      equilibrio, novità, misteri e congegni in modo che ogni arco abbia
      variabilità e unicità… non lineare e abbatti abbatti mostro»*).
      **Decisione di design: NON una skill nuova e nessun merge** — la
      varietà non è un dominio (ADR-0008 §1), è una **politica** su
      contenuto che ha già le sue skill, e il suo corpo è un **registro**,
      che in questo repo vive in `campaign/state.md`, non dentro una skill.
      Nuovo `rumblingstone-narrative-style/references/varieta-fra-archi.md`:
      la **tavolozza d'arco** (cinque dichiarazioni), le **sei tinte** con
      il difetto specifico di ciascuna e il contrappunto che lo cura, le
      **sei regole di rotazione**, e **la prova del recap** come diagnosi.
      Casa in `narrative-style` e non in `indagine` per una ragione
      operativa: la decisione «questo arco ha un caso?» va presa *prima* che
      la richiesta parli di misteri, e `narrative-style` è l'unica skill che
      si carica sempre.
      *Accettazione*: un agente che prepara un arco trova il piano per-arco
      senza doverlo chiedere; la proposta di colorazione ARC-08/09 è
      marcata `[PROPOSTA — needs DM confirmation]` e **non** scritta in
      `state.md`.
- [x] **I10 — Quota di modulo e orchestrazione dinamica** (richiesta DM
      2026-08-26: *«per l'arco 9, siccome ci sono più moduli, dare una
      percentuale opportuna per misteri, intrighi e congegni… 1 per arco è
      poco ma 1 per modulo è troppo… usa i migliori metodi per orchestrare
      in maniera dinamica»*). `varieta-fra-archi.md` §6-§7: le **sei assi**
      (battaglia · esplorazione · intrigo · mistero · congegno · villain in
      scena) col difetto per eccesso E per difetto di ciascuna; **la quota
      su ~10 moduli** con la riga più importante che è quella dei **moduli
      puliti** (4-5, ~45%); il **tetto di 2 congegni** per arco modulare,
      riconciliato esplicitamente con la regola 3 (§1 e §3 corretti: non è
      un allentamento, è la stessa densità su durata diversa);
      **l'orchestrazione a tre livelli** — vocazione del modulo (scritta
      col modulo) × conto aperto × assegnazione **al momento in cui il
      tavolo sceglie** —, le **cinque regole anti-ritmo**, **il modulo che
      cambia natura** e la leva finale (cambiare quale asse sorprende).
      *Accettazione*: nessuna assegnazione fissa in anticipo (sarebbe un
      calendario, e un calendario si impara), e la quota ARC-09 è scritta
      come vocazioni, non come compiti.
- [x] **I4 — Deploy e tracciatura.** `build-skills.sh`, mirror per-agente,
      riga in INDEX e CHANGELOG.

## 4. Confini (cosa questo piano NON fa)

- **Non tocca il canone.** Nessun caso scritto, nessun PNG, nessuna riga in
  `state.md`. Questa è infrastruttura di scrittura: il primo caso vero si
  scriverà *usando* la skill, ed è un lavoro a parte.
- **Non è un sistema di abilità alternativo.** Sta dentro il d20 SRD:
  prove di caratteristica grezze (`core-mechanics.md`: d20 + mod, nessun
  grado) e prove d'abilità normali. Niente meccanica nuova da imparare.
- **Non promette che i giocatori dedurranno.** La ricomposizione è
  preparata dal DM come **rete di sicurezza** e ceduta al tavolo quando il
  tavolo ci arriva: è il `[HDYWTDT]` di Mercer applicato alla deduzione.

## 5. Coda (gated sul tavolo)

- ⬜ **I5 — Un caso vero**, scritto con la skill, giocato, e i suoi tempi
  reali riportati in `rumblingstone-playtest`. Senza una sessione vera non
  si sa se un caso da tre strati sta in una serata: **il tetto di Perizia e
  il numero di nodi per caso sono i due numeri da tarare al collaudo.**
- ⬜ **I6 — `validate_modules.py`**: gate meccanico sui nodi (tre porte
  dichiarate, una fisica, il Fatto senza tiro). Ha senso solo quando
  esistono nodi veri da validare — prima sarebbe un validatore senza corpus.
