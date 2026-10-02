# ADR-0077 — La correzione della prosa passa per una revisione a due giri

- **Stato**: accettata
- **Data**: 2026-10-02
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, il 2026-10-02, sulle decisioni D15 e D16 di
  PIANO-AGENT-SKILLS-ESTERNE: *«D15 ok ma per fare la verifica deve proporre un
  documento che faccia leggere cosa e cambiato rispetto all originale così si
  possono approvare le modifiche e il documento diventa definitivo esattamente
  come le correzioni fatte sugli articoli di ricerca dei revisori che passano
  alla autore e alla fine di nuovo al revisore per vedere se e rimasto
  qualcosa? Forse puo aiutare un meccanismo di versioning del def ?»* e *«D16
  cerca le migliori soluzioni della community con licenza applicabile e
  applicale»*
- **Rapporti**: applica [ADR-0010](ADR-0010-vendoring-skill-terzi.md) (si
  prende il pezzo che serve, mai la collezione) e
  [ADR-0076](ADR-0076-adozione-da-awesome-llm-apps.md) (un ADR per ogni cosa
  presa da fuori); estende ai testi la riga di revisione di
  [ADR-0023](ADR-0023-colophon-di-edizione.md) e
  [ADR-0071](ADR-0071-gli-artefatti-crescono-per-stadi-e-ogni-pagina-ha-una-versione.md)

## Contesto

Fino a L11 i rilevatori del repo segnalavano e basta. La misura di L11
(`plans/scrittura/RISULTATI.md`) dice che le skill alzano la conformità dall'81%
al 100% sui testi nuovi; sui testi che ci sono già, i master DEF-1..4 di ARC-07
hanno da 13 a 30 segnalazioni ciascuno, e nessuno strumento le porta a una
correzione.

Correggere con una regex non è sicuro. Il repo l'ha già misurato due volte: un
trattino dipende dalla frase in cui sta, e «sembra» si toglie solo riscrivendo
quello che la frase voleva dire. La riscrittura la fa un modello o una persona;
quello che manca è un modo di leggerla, approvarla pezzo per pezzo e sapere
cosa è rimasto.

## Decisione

**1. Tre comandi, tre ruoli.** `scripts/ciclo_prosa.py` fa il revisore, due
volte:

| Comando | Ruolo | Cosa produce |
|---|---|---|
| `segnala FILE` | revisore, primo giro | i passaggi da correggere, ognuno con la norma e il rimedio |
| `revisione ORIGINALE RISCRITTO` | l'autore risponde | il documento `REVISIONE-*.md`: ogni modifica numerata, in CriticMarkup, con la norma che la motiva e una casella `[ ]` |
| `applica REVISIONE.md --data` | revisore, secondo giro | l'originale con le sole modifiche spuntate, la riga di revisione alzata, i residui |

La riscrittura sta fra il primo e il secondo comando, e lo script non la fa.

**2. Due garanzie, scritte in testa al documento di revisione.** Nessun
controllo peggiora: il conto delle segnalazioni per norma non cresce. E nessun
fatto cambia: i nomi propri del registro (`misura_craft`, Bestiario e
`state.md`), i numeri e le CD sono gli stessi prima e dopo. Se una delle due
manca, il comando esce 1; `applica` ricontrolla i fatti sulle sole modifiche
accettate e rifiuta.

**3. Una modifica senza una norma si guarda per prima.** Il documento le conta
e le segna «⚠️ non motivata». Possono essere giuste, ma sono quelle dove il
modello ha riscritto per gusto suo.

**4. Le modifiche si leggono come frasi.** Il diff è per parole, e due cambi
separati da tre parole o meno, senza una fine di frase in mezzo, diventano una
modifica sola. Sulla prima prova (l'eco privata di Hella della corsa
A-senza-4) undici modifiche di una parola sono diventate tre.

**5. Il versionamento è una riga, non un sistema.** `applica` scrive o alza
`<!-- revisione-testo: rN · AAAA-MM-GG -->` in testa al file, dopo il
frontmatter se c'è. La storia vera resta in git; la riga serve a chi legge il
master stampato o aperto fuori dal repo, come il `r<rev>` di ADR-0071. La data
si passa a mano (`--data`), perché ADR-0023 non la fa dedurre.

**6. Tre sbarramenti su `applica`.** Non scrive su `main` né su `master`
(regola di sempre del DM: niente canone su main via script). Non applica una
revisione se l'originale o il riscritto sono cambiati dopo: l'impronta SHA-256
dei due testi sta nella testata del documento, perché i numeri delle modifiche
valgono solo su quel diff. E non applica se le modifiche spuntate cambiano un
fatto.

## Che cosa si prende dalla comunità, e con che licenza

Nessuna riga di codice di terzi entra nel repo. Si prendono una sintassi e due
idee, riscritte con la sola stdlib (`difflib`, `hashlib`).

| Fonte | Licenza | Che cosa | Dove |
|---|---|---|---|
| **CriticMarkup**, Gabe Weatherhead ed Erik Hess ([criticmarkup.com](https://criticmarkup.com), `CriticMarkup/CriticMarkup-toolkit`) | Apache 2.0 | la sintassi di revisione: `{~~vecchio~>nuovo~~}`, `{++aggiunto++}`, `{--tolto--}`, `{>>commento<<}` | il testo marcato del documento di revisione |
| **Humanizer**, blader (`blader/humanizer`) | MIT | la regola «weak alone»: un segnale minore da solo non prova niente, conta il gruppo; e il divieto di inventare fatti mentre si riscrive | il controllo «tic minori in gruppo» e la garanzia sui fatti |
| ***Wikipedia: Signs of AI writing*** | CC BY-SA 4.0 | la stessa regola, nella forma di una guida per i revisori | citata, nessun testo copiato |
| Anthropic, ***Building effective agents*** | documentazione pubblica | il modello *evaluator-optimizer*: chi scrive e chi valuta sono due ruoli, e si gira finché il valutatore non ha più niente | l'ordine dei tre comandi |

I tic minori sono quelli che `italiano-nativo.md` §9.2-ter e §9.2-quater elenca
già e lascia fuori da ogni controllo, con la ragione scritta: da soli sono
italiano corretto. Ora contano quando due diversi cadono nella stessa unità di
prosa, che è un paragrafo, una voce d'elenco o un box. Il trattino
dell'etichetta di regia non conta, perché il giocatore non lo sente.

### Che cosa si è scartato

- **Vale** e **proselint**: le regole sono in inglese, e tradurle vorrebbe dire
  scrivere un altro rilevatore senza la loro taratura.
- **LanguageTool**, le regole italiane di `grammar.xml`: LGPL, e si appoggiano
  alle etichette morfologiche del suo motore, che il repo non ha. Restano
  un'idea per quando servirà un'analisi grammaticale vera.

## Conseguenze

- Un master DEF si corregge per revisioni approvate, e ognuna lascia un
  documento che dice cosa è cambiato e perché. Il DM approva modifiche, non
  file interi.
- Il controllo «tic minori in gruppo» entra nel registro come 🟡 e fuori dal
  punteggio MQM: la soglia di due tic diversi viene da Humanizer e non è
  ancora tarata su questo repo.
- La prima prova ha trovato un buco nel metro di D13: `SEMBRA` non vedeva il
  participio («ti è sembrato») né il passato remoto. Corretto in
  `voto_scrittura.py`; i conti di L11 non cambiano (34 box sui file di gioco,
  stessi voti sulle corse).
- Lo script non riscrive. Se un giorno lo farà, la riscrittura passerà dagli
  stessi tre comandi.
