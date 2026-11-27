# Ricerca: uno standard a schede per tutti i prompt del repo

**Data**: 2026-11-08 · **Richiesta del DM** (Jfs): uno standard del repo per
tutti i prompt, in schede, per limitare le allucinazioni e dare una direzione di
sviluppo professionale; nelle scelte di sviluppo, lo standard de facto migliore
della comunità.

**Fonti**: WebSearch e le pagine Markdown della documentazione di Anthropic
(Firecrawl senza crediti quel giorno), il repo. Decisione in
[ADR-0114](adr/ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md), schede in
[GUIDA-SCHEDE-PROMPT](../docs/reference/GUIDA-SCHEDE-PROMPT.md). Misura con
[`misura_prompt.py`](esperimenti/schede-prompt-2026-11-08/misura_prompt.py),
esito prima del lavoro in [`misura-prima.txt`](esperimenti/schede-prompt-2026-11-08/misura-prima.txt).

## 1 · Cosa c'è già (e funziona)

- **18 skill** in `skills/*/SKILL.md`, tutte con frontmatter valido
  (`validate_skills.py`) e con la sezione «Cancelli deterministici» (ADR-0108).
- **Blocco «Vincoli sui fatti»** (ADR-0109) in 10 skill su 18: permesso di dire
  «non so», divieto di inventare statblock e poteri, ordine delle fonti, dati non
  istruzioni, rilettura dei numeri prima di consegnare.
- **Una prova misurata**: la A/B del 2026-11-07 (30 consegne con una trappola
  ciascuna, giudice alla cieca). Fatti inventati senza marca 127 → 73 (−43%),
  marche ben formate 42 → 124; per consegna 11 meglio, 4 peggio, 15 pari
  (p = 0,059 a una coda). È l'unico pezzo dove sappiamo che un prompt riduce le
  allucinazioni, e non per molto margine.
- Modello ADR con alternative e «Da rivedere se», modello di PR con «Note oneste»,
  standard dei prompt immagine (ADR-0015), canali unstable/testing/stable (ADR-0099).

## 2 · Lo stato dell'arte, in breve (con quanto vale ogni fonte)

| Fonte | Cosa dice | Peso |
|---|---|---|
| Anthropic, *Reduce hallucinations* | permesso di dire «non so», estrarre citazioni prima di rispondere, citare la fonte di ogni affermazione; riducono, non eliminano | guida del produttore, nessun numero |
| Anthropic, *Skill authoring best practices* | SKILL.md sotto 500 righe, descrizione in terza persona con «cosa fa e quando usarla», riferimenti a un livello, **niente informazioni datate** (si spostano in «vecchi modelli»), terminologia costante, **almeno 3 prove per skill prima di scrivere molta documentazione**, gradi di libertà secondo il rischio | guida del produttore |
| Anthropic, *Effective context engineering* | il prompt va all'«altitudine giusta»: l'insieme minimo di informazioni ad alto segnale | guida del produttore |
| Gloaguen et al., *Evaluating AGENTS.md* (ETH, ICLR 2026, arXiv 2602.11988) | i file di contesto **non migliorano** il successo degli agenti e costano oltre il 20% di token in più; quelli scritti a mano aiutano poco (≈4%, non significativo); vanno tenuti minimi, solo istruzioni che il repo non dice già | studio indipendente, benchmark Python, non narrativa |
| Jaroslawicz et al., *IFScale* (NeurIPS 2025, arXiv 2507.11538) | più istruzioni nello stesso prompt = meno istruzioni rispettate; i modelli migliori al 68% con 500 istruzioni, e favoriscono quelle in alto | studio su istruzioni di parole chiave, non su regole di gioco |
| He et al., *Does prompt formatting…* (arXiv 2411.10541) | la forma (Markdown, JSON, YAML) cambia il risultato fino al 40% sui modelli piccoli, molto meno sui grandi, e nessuna forma vince ovunque | solo modelli OpenAI |

**Lettura onesta**: le «schede» in sé non riducono le allucinazioni. Le riducono
pochi meccanismi precisi (dire «non so», fonti in ordine, citare, rileggere, un
cancello deterministico) e la *misura* che dice se hanno funzionato. La scheda
serve a due cose più modeste ma reali: che quei meccanismi ci siano **ovunque**, e
che un controllo possa verificarlo. Scrivere di più va nella direzione sbagliata:
le prove dicono che istruzioni lunghe vengono seguite peggio.

## 3 · La misura del repo contro quella checklist

Script e esito: vedi l'intestazione. Nota: `misura_prompt.py` conta «Formato d'uscita» anche in edizione per il titolo «gate d'uscita», quindi 4/18 è in realtà 3/18.

| Criterio | Oggi | Nota |
|---|---|---|
| SKILL.md sotto 500 righe | 18/18 (max 421, module-standard) | ok |
| Descrizione dice «quando» | 17/18 (manca mapmaking) | |
| Lingua della descrizione | 7 inglese, 11 italiano | le richieste del DM arrivano in italiano |
| «Vincoli sui fatti» | 10/18 | mancano art-direction, automation, debugging, edizione, mapmaking, plans, prosa-documenti, dnd-35-rules |
| Formato d'uscita dichiarato | 4/18 | |
| Controllo «prima di consegnare» | 4/18 | |
| Cancelli deterministici | 18/18 | ok |
| Prove (consegne con trappola) | 10 skill × 3, nessuna per le altre 8 | la prova non è uno script del repo: la ha fatta girare un workflow a mano |
| Date e storie nel corpo delle skill | 41 date; editoria 11, mapmaking 7 | contro «niente informazioni datate» |
| AGENTS.md | 481 righe, ≈4.500 parole, ≈32 KB, letto da ogni agente | la «Regola d'oro» (righe 92-247) è in gran parte racconto di come è nata |
| Brief a subagenti e thread | scritti a mano ogni volta, 4 in `plans/esperimenti/`, nessun modello | ogni brief riscrive le stesse regole con parole diverse |

## 4 · La proposta: tre schede, una prova, un cancello (ADR-0114)

**Scheda skill** — un ordine fisso di sezioni in ogni SKILL.md, corte, con le
norme lunghe nei `references/`:

1. frontmatter: `description` con *cosa fa* e *quando usarla*;
2. **Quando no** (confini con le altre skill, in due righe);
3. **Fonti, in ordine** (o rimando);
4. **Vincoli sui fatti** (rimando a GUIDA-MARCATURE, già scritto);
5. **Procedura** (passi numerati, gradi di libertà secondo il rischio);
6. **Formato d'uscita** (un modello o un esempio concreto);
7. **Prima di consegnare** (domande a cui si risponde con un comando dove si può);
8. **Cancelli deterministici** (c'è già);
9. **Prove**: dove stanno le sue consegne con trappola.

La storia («nasce da un fallimento il …») esce dal corpo e va nell'ADR che la
racconta già, con un rimando di una riga.

**Scheda brief** — un modello unico per ogni prompt a un subagente, a un thread
o a un agente di workflow (§2 di `docs/reference/GUIDA-SCHEDE-PROMPT.md`): Obiettivo · Stato vero
(file con il percorso, cosa è canone) · Cosa puoi toccare · Vincoli (rimando) ·
Formato d'uscita · Fatto quando · Se non sai. Le regole non si riscrivono: si
richiamano.

**Scheda prova** — `consegne.json` diventa un file per skill
(`skills/<nome>/prove.json`), almeno 3 consegne con trappola ciascuna, e uno
script del repo che esegue la A/B e scrive l'esito. La CI controlla che le prove ci
siano e siano ben formate; la A/B costa agenti, quindi gira a mano o in workflow
quando cambia una skill, non a ogni commit.

**Cancello** — `validate_skills.py` controlla le sezioni della scheda skill e la
presenza delle prove; parte non bloccante nel canale testing, l'audit settimanale
propone di renderlo bloccante dopo due settimane (come ADR-0109).

**Regola di adozione** (come vuole Jfs dal 2026-10-31): una skill riscritta in
scheda entra solo se la A/B non peggiora gli inventati senza marca. Se peggiora, si
corregge e si rimisura; se resta peggio, si tiene la vecchia.

## 5 · Cosa non risolve

- Non elimina le allucinazioni: la prova migliore che abbiamo è −43% sugli
  inventati, con 30 consegne e p = 0,059.
- Il giudice della A/B è un modello: conta le invenzioni, ma può sbagliare a
  contarle. Il voto del DM resta il riscontro vero.
- Gli studi su AGENTS.md misurano compiti di codice, non prosa di gioco: dicono
  che accorciare non fa danni, non che accorciare aiuta la narrativa.
- Le guide di Anthropic valgono per Claude; Gemini, Codex e gli altri agenti di
  `agents.conf` ricevono le stesse skill compresse e non li abbiamo misurati.

## 6 · Piano

1. **Verifica** (fatta): fotografia e fonti, qui sopra.
2. **Sviluppo**, dopo le scelte: ADR-0114; MODELLO-BRIEF; scheda skill nelle 18
   skill a lotti (prima le 8 senza vincoli né prove); prove per le 8; script A/B
   nel repo; cancello non bloccante; AGENTS.md snellito se scelto.
3. **Prova**: A/B sulle 30 consegne vecchie + 24 nuove, vecchia contro nuova, giudice
   alla cieca; conteggio dei token prima e dopo; test del cancello; `validate_skills`,
   `validate_docs` e CI verdi.

## 7 · Scelte del DM e standard di fatto (2026-11-08)

- **Perimetro**: skill e brief agli agenti; i prompt immagine restano ad ADR-0015.
- **AGENTS.md**: si snellisce, con misura prima e dopo (standard agents.md e studio ETH).
- **Forma delle prove**: quella dei casi di `claude plugin eval` (`evals/<caso>/prompt.md`,
  `case.yaml`, `graders/`), che è la forma documentata dalla skill-creator di
  Anthropic; il `prove.json` nostro della proposta è scartato.
- **Dimensione della A/B**: 54 consegne, circa 110 agenti.
- **Lingua**: italiano, con i termini di gioco originali fra parentesi o fra virgolette.

## 8 · Esito del lotto 2 (2026-11-08)

A/B alla cieca, 108 esecuzioni e 18 giudici: inventati senza marca 32 → 30, marche
con domanda e base 74 → 95, per caso 4 meglio, 4 peggio, 46 pari (p = 0,64).
`dnd-35-srd` sembrava peggiorare (0 → 3); rimisurata con due esecuzioni per
versione è pari (3 a 3). La scheda si adotta perché non peggiora; non è dimostrato
che riduca le invenzioni. AGENTS.md passa da 485 a 367 righe. Dettagli in
[ab-lotto2/ESITO](esperimenti/schede-prompt-2026-11-08/ab-lotto2/ESITO.md).
